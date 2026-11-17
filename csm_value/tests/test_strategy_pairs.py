"""Ensure the two standalone pairs preserve data and execution behavior."""
import contextlib
import inspect
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import csm_value_strategy as value
import csm_value_experimental_strategy as experiment
import run_csm_value_backtest as value_runner
import run_csm_value_experimental_backtest as experimental_runner


class StrategyPairsTest(unittest.TestCase):
    def test_gross_cap_preserves_weights_without_open(self):
        weights = pd.Series({'FROZEN': .35, 'A': .40, 'B': .35})
        for runner in (value_runner, experimental_runner):
            capped = runner._cap_gross_weights(weights, {'FROZEN'})
            self.assertAlmostEqual(capped.sum(), 1.)
            self.assertEqual(capped['FROZEN'], .35)
            self.assertAlmostEqual(capped['A'] / capped['B'], .40 / .35)
            pd.testing.assert_series_equal(runner._cap_gross_weights(weights * .5, {'FROZEN'}), weights * .5)

    def test_zero_capacity_entry_does_not_leave_phantom_holding(self):
        days = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-29',
                               '2024-03-01', '2024-03-04', '2024-03-05'])
        px = pd.DataFrame({'ABC': 100., 'XYZ': 100.}, index=days)
        opens = px.copy()
        opens.loc['2024-03-01', 'ABC'] = float('nan')
        months = pd.to_datetime(['2024-01-31', '2024-02-29'])
        for module, runner in ((value, value_runner), (experiment, experimental_runner)):
            with self.subTest(pair=module.__name__), contextlib.redirect_stdout(io.StringIO()):
                st = module.CSMValue(px, px * 1000, opens_df=opens, benchmark_series=px.ABC,
                    ranking_mode='value', top_n=2, use_crash_guard=False, use_liquid_mf=False,
                    leverage_bear=1., leverage_bull=1., leverage_panic=1.,
                    rebalance_exit_buffer_months=0, use_trade_deadband=False)
                st.positions = pd.DataFrame({'ABC': [1., .5], 'XYZ': [0., .5]}, index=months)
                st.factors = st.positions.copy()
                st.momentum_returns = st.positions.copy()
                st.all_ranks = pd.DataFrame({'ABC': [1., 1.], 'XYZ': [2., 2.]}, index=months)
                st.factor_legs = {'EP': st.positions.copy()}
                st._signal_age = st.positions.copy()
                st._prepare_stop_indicators(px.resample('ME').last())
                st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
                result = runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
                self.assertEqual(result['executed_weights'].loc['2024-03-01', 'XYZ'], 0.)
                self.assertAlmostEqual(result['executed_weights'].loc['2024-03-01'].sum(), 1.)
                self.assertGreater(result['executed_weights'].loc['2024-03-04', 'XYZ'], 0.)

    def test_cap_filling_allocates_available_capacity_without_leverage(self):
        cases = [(pd.Series([.01, .02, .04], index=list('ABC')), .25, .75),
                 (pd.Series([.01, .02, .04, .08], index=list('ABCD')), .30, 1.0),
                 (pd.Series([.01, .02, .03], index=list('ABC')), 0., 0.)]
        for module in (value, experiment):
            for vols, cap, target in cases:
                with self.subTest(pair=module.__name__, cap=cap):
                    w = module.capped_inverse_vol_weights(vols, cap)
                    self.assertAlmostEqual(w.sum(), target)
                    self.assertTrue((w >= 0).all())
                    self.assertTrue((w <= cap + 1e-12).all())
            w = module.capped_inverse_vol_weights(cases[1][0], .30)
            self.assertAlmostEqual(w['C'] / w['D'], 2.0)

    def test_distinct_strategy_and_runner_defaults(self):
        base = inspect.signature(value.CSMValue).parameters
        exp = inspect.signature(experiment.CSMValue).parameters
        expected = {'ranking_mode': ('value', 'value_growth_pullback'),
                    'top_n': (20, 20), 'buffer_ratio': (1., 1.),
                    'max_weight_per_stock': (.05, .05),
                    'risk_pct_per_trade': (.0075, .0075),
                    'hard_stop_from_peak': (.20, .20),
                    'vol_target': (.20, .22),
                    'rebalance_exit_buffer_months': (2, 3),
                    'leverage_bear': (.8, .5)}
        for key, (left, right) in expected.items():
            self.assertEqual(base[key].default, left)
            self.assertEqual(exp[key].default, right)
        main = inspect.signature(experimental_runner.main).parameters
        self.assertEqual(main['ranking_mode'].default, 'value_growth_pullback')
        self.assertEqual(main['risk_profile'].default, 'default')
        for runner in (value_runner, experimental_runner):
            self.assertEqual(runner.RISK_PROFILES['legacy_value']['top_n'], 10)
            self.assertEqual(runner.RISK_PROFILES['exploratory_10_12_bear50']['top_n'], 10)

    def test_fundamentals_are_identical_and_not_available_on_filing_day(self):
        periods = [('2023-04-01', '2023-06-30', '20-Jul-2023', 1),
                   ('2023-07-01', '2023-09-30', '20-Oct-2023', 2),
                   ('2023-10-01', '2023-12-31', '20-Jan-2024', 3),
                   ('2024-01-01', '2024-03-31', '20-Apr-2024', 4)]
        quarters = {f'Q{i}': {'standalone': {'period': {'start': start, 'end': end},
                    'filed_date': filed, 'income_statement': {'net_profit': profit,
                    'paid_up_equity_share_capital': 100, 'face_value_per_share': 1}}}
                    for i, (start, end, filed, profit) in enumerate(periods, 1)}
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, 'ABC.json').write_text(json.dumps({'fiscal_years': {'FY': {'quarters': quarters}}}))
            a, b = value.load_results(directory=temp), experiment.load_results(directory=temp)
            pd.testing.assert_frame_equal(a, b)
            dates = pd.to_datetime(['2024-04-20', '2024-04-21'])
            for module, results in ((value, a), (experiment, b)):
                observed = module.monthly_frame(results, 'np_ttm', dates, ['ABC'])
                self.assertTrue(pd.isna(observed.iloc[0, 0]))
                self.assertEqual(observed.iloc[1, 0], 10)

    def test_next_open_stop_and_exit_day_weight_are_identical(self):
        days = pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-01',
                               '2024-02-02', '2024-02-05', '2024-02-06'])
        close = pd.DataFrame({'ABC': [100., 100., 100., 80., 70., 70.]}, index=days)
        opens = pd.DataFrame({'ABC': [100., 100., 100., 100., 70., 70.]}, index=days)
        runs = []
        for module, runner in ((value, value_runner), (experiment, experimental_runner)):
            with contextlib.redirect_stdout(io.StringIO()):
                strategy = module.CSMValue(close, close * 1000, opens_df=opens,
                    benchmark_series=pd.Series(100., index=days), ranking_mode='value',
                    hard_stop_from_peak=.20, use_crash_guard=False, min_hold_days=0,
                    use_liquid_mf=False, leverage_bull=1., leverage_bear=1.,
                    leverage_panic=1., rebalance_exit_buffer_months=0, use_trade_deadband=False)
                strategy.positions = pd.DataFrame({'ABC': [.05]}, index=pd.to_datetime(['2024-01-31']))
                strategy.factors = strategy.positions.copy()
                strategy.all_ranks = pd.DataFrame({'ABC': [1.]}, index=strategy.positions.index)
                strategy.factor_legs = {'EP': strategy.positions.copy()}
                strategy._signal_age = strategy.positions.copy()
                strategy._prepare_stop_indicators(close.resample('ME').last())
                strategy._panic_threshold_series = strategy._bench_vol_monthly = None
                strategy.atr = strategy._bvol_daily = None
                result = runner.backtest_event_driven(strategy, transaction_cost=0., risk_free_rate=0.)
            self.assertEqual(result['executed_weights'].loc['2024-02-05', 'ABC'], 0.)
            self.assertEqual(strategy.position_metadata[0]['Exit_Price'], 70.)
            runs.append(result)
        pd.testing.assert_series_equal(runs[0]['net_returns'], runs[1]['net_returns'])
        pd.testing.assert_frame_equal(runs[0]['executed_weights'], runs[1]['executed_weights'])

    def test_rebalance_buffer_counts_months_and_retries_missing_open(self):
        days = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-29',
                               '2024-03-01', '2024-03-28', '2024-04-01',
                               '2024-04-30', '2024-05-01', '2024-05-02', '2024-05-03'])
        close = pd.DataFrame({'ABC': 100.}, index=days)
        opens = close.copy()
        opens.loc['2024-05-01', 'ABC'] = float('nan')
        months = pd.to_datetime(['2024-01-31', '2024-02-29', '2024-03-31', '2024-04-30'])
        for module, runner in ((value, value_runner), (experiment, experimental_runner)):
            for buffer, expected in ((0, '2024-03-01'), (1, '2024-04-01'), (2, '2024-05-02')):
                with self.subTest(pair=module.__name__, buffer=buffer), contextlib.redirect_stdout(io.StringIO()):
                    st = module.CSMValue(close, close * 1000, opens_df=opens,
                        benchmark_series=close.ABC, ranking_mode='value',
                        use_crash_guard=False, use_liquid_mf=False, leverage_bear=1.,
                        rebalance_exit_buffer_months=buffer, use_trade_deadband=False)
                    st.positions = pd.DataFrame({'ABC': [.05, 0., 0., 0.]}, index=months)
                    st.factors = st.positions.copy()
                    st.momentum_returns = st.positions.copy()
                    st.all_ranks = pd.DataFrame({'ABC': [1., 1., 1., 1.]}, index=months)
                    st.factor_legs = {'EP': st.positions.copy()}
                    st._signal_age = st.positions.copy()
                    st._prepare_stop_indicators(close.resample('ME').last())
                    st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
                    result = runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
                    closed = next(t for t in st.position_metadata if t['Exit_Reason'] == 'REBALANCE')
                    self.assertEqual(closed['Exit_Date'], pd.Timestamp(expected))
                    if buffer == 2:
                        self.assertGreater(result['executed_weights'].loc['2024-05-01', 'ABC'], 0)
                        self.assertEqual(result['executed_weights'].loc['2024-05-02', 'ABC'], 0)

    def test_protective_stop_remains_active_during_long_buffer(self):
        days = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-29',
                               '2024-03-01', '2024-03-28', '2024-04-01', '2024-04-02'])
        close = pd.DataFrame({'ABC': [100., 100., 100., 100., 70., 70., 70.]}, index=days)
        opens = close.copy()
        months = pd.to_datetime(['2024-01-31', '2024-02-29', '2024-03-31'])
        for module, runner in ((value, value_runner), (experiment, experimental_runner)):
            with self.subTest(pair=module.__name__), contextlib.redirect_stdout(io.StringIO()):
                st = module.CSMValue(close, close * 1000, opens_df=opens,
                    benchmark_series=pd.Series(100., index=days), ranking_mode='value',
                    use_crash_guard=False, use_liquid_mf=False, leverage_bear=1.,
                    rebalance_exit_buffer_months=3, use_trade_deadband=False)
                st.positions = pd.DataFrame({'ABC': [.05, 0., 0.]}, index=months)
                st.factors = st.positions.copy()
                st.momentum_returns = st.positions.copy()
                st.all_ranks = pd.DataFrame({'ABC': [1., 1., 1.]}, index=months)
                st.factor_legs = {'EP': st.positions.copy()}
                st._signal_age = st.positions.copy()
                st._prepare_stop_indicators(close.resample('ME').last())
                st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
                result = runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
                closed = next(t for t in st.position_metadata if t['Exit_Reason'] == 'STOP_HIT')
                self.assertEqual(closed['Exit_Date'], pd.Timestamp('2024-04-01'))
                self.assertEqual(result['executed_weights'].loc['2024-04-01', 'ABC'], 0.)

    def test_buffer_count_resets_when_stock_returns_to_target(self):
        days = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-29', '2024-03-01',
                               '2024-03-28', '2024-04-01', '2024-04-30', '2024-05-01',
                               '2024-05-31', '2024-06-03', '2024-06-28', '2024-07-01'])
        px = pd.DataFrame({'ABC': 100.}, index=days)
        months = pd.to_datetime(['2024-01-31', '2024-02-29', '2024-03-31',
                                 '2024-04-30', '2024-05-31', '2024-06-30'])
        for module, runner in ((value, value_runner), (experiment, experimental_runner)):
            with self.subTest(pair=module.__name__), contextlib.redirect_stdout(io.StringIO()):
                st = module.CSMValue(px, px * 1000, opens_df=px, benchmark_series=px.ABC,
                    ranking_mode='value', use_crash_guard=False, use_liquid_mf=False,
                    leverage_bear=1., rebalance_exit_buffer_months=2, use_trade_deadband=False)
                st.positions = pd.DataFrame({'ABC': [.05, 0., .05, 0., 0., 0.]}, index=months)
                st.factors = st.positions.copy()
                st.momentum_returns = st.positions.copy()
                st.all_ranks = pd.DataFrame({'ABC': 1.}, index=months)
                st.factor_legs = {'EP': st.positions.copy()}
                st._signal_age = st.positions.copy()
                st._prepare_stop_indicators(px.resample('ME').last())
                st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
                runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
                closed = next(t for t in st.position_metadata if t['Exit_Reason'] == 'REBALANCE')
                self.assertEqual(closed['Exit_Date'], pd.Timestamp('2024-07-01'))

    def test_each_pair_imports_without_other_strategy_or_loader(self):
        pairs = [('csm_value_strategy.py', 'run_csm_value_backtest.py', 'run_csm_value_backtest', 'csm_value_experimental_strategy'),
                 ('csm_value_experimental_strategy.py', 'run_csm_value_experimental_backtest.py', 'run_csm_value_experimental_backtest', 'csm_value_strategy')]
        for strategy, runner, module, forbidden in pairs:
            with self.subTest(pair=module), tempfile.TemporaryDirectory() as temp:
                for name in (strategy, runner):
                    shutil.copy(ROOT / name, Path(temp) / name)
                script = (f'import sys; sys.path.insert(0, {temp!r}); import {module}; '
                          f'assert "fundamentals_loader" not in sys.modules; '
                          f'assert {forbidden!r} not in sys.modules')
                env = dict(os.environ, MPLCONFIGDIR=temp)
                subprocess.run([sys.executable, '-I', '-c', script], cwd=temp,
                               env=env, check=True, capture_output=True, text=True)


if __name__ == '__main__':
    unittest.main()

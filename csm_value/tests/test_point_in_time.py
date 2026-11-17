import json
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import fundamentals_loader as loader
from csm_value_strategy import CSMValue


def block(start, end, filed, profit, capital=100):
    return {'filed_date': filed, 'period': {'start': start, 'end': end},
            'income_statement': {'net_profit': profit, 'revenue_from_operations': 1000,
                                 'paid_up_equity_share_capital': capital,
                                 'face_value_per_share': 1}}


def fixture(root, late=True):
    quarters = {
        'Q1': {'standalone': block('2023-04-01', '2023-06-30', '20-Jul-2023 20:00:01', 1)},
        'Q2': {'standalone': block('2023-07-01', '2023-09-30', '20-Oct-2023 20:00:01', 2)},
        'Q3': {'standalone': block('2023-10-01', '2023-12-31', '20-Jan-2024 20:00:01', 3)},
        'Q4': {'standalone': block('2024-01-01', '2024-03-31', '20-Apr-2024 20:00:01', 4)},
    }
    if late:
        # Filing arrives after Q1 of the next year. It must not leak into May.
        quarters['Q3']['standalone']['filed_date'] = '25-Apr-2024 20:00:01'
    fy = {'FY2023-24': {'quarters': quarters},
          'FY2024-25': {'quarters': {'Q1': {'standalone': block('2024-04-01', '2024-06-30', '20-Jul-2024 20:00:01', 5)}}}}
    doc = {'symbol': 'ABC', 'fiscal_years': fy}
    (root / 'ABC.json').write_text(json.dumps(doc))


class PointInTimeTest(unittest.TestCase):
    def test_dates_include_seconds_and_same_day_is_not_visible(self):
        self.assertEqual(str(loader._parse_filed('30-Oct-2026 21:32:05')), '2026-10-30 21:32:05')
        r = pd.DataFrame([{'symbol': 'ABC', 'filed': pd.Timestamp('2024-01-31'),
                           'result_filed': pd.Timestamp('2024-01-31'), 'value': 9}])
        dates = pd.to_datetime(['2024-01-31', '2024-02-01'])
        f = loader.monthly_frame(r, 'value', dates, ['ABC'])
        self.assertTrue(pd.isna(f.iloc[0, 0]))
        self.assertEqual(f.iloc[1, 0], 9)

    def test_late_filing_cannot_complete_earlier_ttm(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root)
            r = loader.load_results(directory=str(root))
            self.assertTrue((r.filed >= pd.Timestamp('2024-04-25')).all())
            self.assertEqual(r.iloc[0].np_ttm, 10)
            self.assertEqual(r.iloc[0].result_filed, pd.Timestamp('2024-04-20'))
            self.assertEqual(r.iloc[1].np_ttm, 14)

    def test_future_changes_do_not_change_prior_result(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root, late=False)
            before = loader.load_results(directory=str(root))
            path = root / 'ABC.json'
            doc = json.loads(path.read_text())
            doc['fiscal_years']['FY2024-25']['quarters']['Q2'] = {'standalone': block('2024-07-01', '2024-09-30', '20-Oct-2024 20:00:01', 99999, 200)}
            path.write_text(json.dumps(doc))
            after = loader.load_results(directory=str(root))
            pd.testing.assert_frame_equal(before.reset_index(drop=True), after[after.filed <= '2024-07-20'].reset_index(drop=True))

    def test_later_consolidated_filing_does_not_replace_earlier_standalone(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            fixture(root, late=False)
            path = root / 'ABC.json'
            doc = json.loads(path.read_text())
            for q, entry in doc['fiscal_years']['FY2023-24']['quarters'].items():
                consolidated = dict(entry['standalone'])
                consolidated['income_statement'] = dict(consolidated['income_statement'], net_profit=100.)
                if q == 'Q4':
                    consolidated['filed_date'] = '30-Apr-2024 19:00:00'
                entry['consolidated'] = consolidated
            path.write_text(json.dumps(doc))
            r = loader.load_results(directory=str(root))
            dates = pd.to_datetime(['2024-04-21', '2024-04-30', '2024-05-01'])
            got = loader.monthly_frame(r, 'np_ttm', dates, ['ABC'])['ABC']
            self.assertEqual(got.iloc[0], 10.)
            self.assertEqual(got.iloc[1], 10.)
            self.assertEqual(got.iloc[2], 400.)

    def test_future_share_unit_heuristic_is_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Future-inferred'):
            loader.load_results(restore_units=True)

    def test_sme_six_month_results_not_mistaken_for_quarters(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / 'sme').mkdir()
            fixture(root, late=False)
            doc = json.loads((root / 'ABC.json').read_text())
            doc['fiscal_years']['FY2023-24']['quarters']['Q4']['standalone']['period']['start'] = '2023-10-01'
            (root / 'ABC.json').unlink()
            (root / 'sme' / 'ABC.json').write_text(json.dumps(doc))
            r = loader.load_results(directory=str(root))
            self.assertTrue(r.empty)

    def test_signal_uses_last_trading_session_not_weekend_month_end(self):
        idx = pd.bdate_range('2024-01-01', '2024-03-29')
        px = pd.DataFrame({'ABC': 100., 'XYZ': 100.}, index=idx)
        res = pd.DataFrame([
            {'symbol': 'ABC', 'filed': pd.Timestamp('2024-03-30'), 'result_filed': pd.Timestamp('2024-03-30'), 'np_ttm': 20., 'shares_adj': 1., 'sg_np': 1.},
            {'symbol': 'XYZ', 'filed': pd.Timestamp('2024-03-28'), 'result_filed': pd.Timestamp('2024-03-28'), 'np_ttm': 10., 'shares_adj': 1., 'sg_np': 1.},
        ])
        st = CSMValue(px, px * 10, benchmark_series=px.ABC, results_df=res,
                      valuation_prices_df=px, min_eligible=1,
                      use_ca_mask=False)
        st.calculate_factors()
        self.assertTrue(pd.isna(st._legs_unfiltered['EP'].loc['2024-03-31', 'ABC']))
        self.assertAlmostEqual(st._legs_unfiltered['EP'].loc['2024-03-31', 'XYZ'], .1)

    def test_share_count_is_stale_after_post_period_split(self):
        idx = pd.bdate_range('2023-12-01', '2024-03-29')
        px = pd.DataFrame({'ABC': 100., 'XYZ': 100.}, index=idx)
        px.loc['2024-02-15':, 'ABC'] = 50.
        rows = [dict(symbol=sym, period_end=pd.Timestamp('2023-12-31'),
                     filed=pd.Timestamp('2024-01-20'), result_filed=pd.Timestamp('2024-01-20'),
                     np_ttm=10., shares_adj=1., sg_np=1.) for sym in ('ABC', 'XYZ')]
        st = CSMValue(px, px * 10, benchmark_series=px.XYZ,
                      results_df=pd.DataFrame(rows), valuation_prices_df=px,
                      min_eligible=1, results_max_age_days=365)
        st.calculate_factors()
        self.assertFalse(st.ca_stale_mask.loc['2024-01-31', 'ABC'])
        self.assertTrue(st.ca_stale_mask.loc['2024-02-29', 'ABC'])
        self.assertTrue(pd.isna(st._legs_unfiltered['EP'].loc['2024-02-29', 'ABC']))

    def test_adjusted_price_ratio_detects_split_without_future_knowledge(self):
        idx = pd.bdate_range('2023-12-01', '2024-03-29')
        adjusted = pd.DataFrame({'ABC': 50., 'XYZ': 100.}, index=idx)
        raw = adjusted.copy()
        raw.loc[:'2024-02-14', 'ABC'] = 100.
        rows = [dict(symbol=sym, period_end=pd.Timestamp('2023-12-31'),
                     filed=pd.Timestamp('2024-01-20'), result_filed=pd.Timestamp('2024-01-20'),
                     np_ttm=10., shares_adj=1., sg_np=1.) for sym in ('ABC', 'XYZ')]
        st = CSMValue(adjusted, adjusted * 10, benchmark_series=adjusted.XYZ,
                      results_df=pd.DataFrame(rows), valuation_prices_df=raw,
                      min_eligible=1, results_max_age_days=365)
        st.calculate_factors()
        self.assertFalse(st.ca_stale_mask.loc['2024-01-31', 'ABC'])
        self.assertTrue(st.ca_stale_mask.loc['2024-02-29', 'ABC'])
        self.assertAlmostEqual(st._legs_unfiltered['EP'].loc['2024-01-31', 'ABC'], .1)

    def test_later_uniform_price_adjustment_does_not_change_valuation(self):
        idx = pd.bdate_range('2023-12-01', '2024-03-29')
        raw = pd.DataFrame({'ABC': 100., 'XYZ': 120.}, index=idx)
        rows = [dict(symbol=sym, period_end=pd.Timestamp('2023-12-31'),
                     filed=pd.Timestamp('2024-01-20'), result_filed=pd.Timestamp('2024-01-20'),
                     np_ttm=10., shares_adj=1., sg_np=1.) for sym in ('ABC', 'XYZ')]
        legs = []
        for factor in (1., .5):
            adjusted = raw * factor
            st = CSMValue(adjusted, adjusted * 10, benchmark_series=adjusted.XYZ,
                          results_df=pd.DataFrame(rows), valuation_prices_df=raw,
                          min_eligible=1, results_max_age_days=365)
            st.calculate_factors()
            legs.append(st._legs_unfiltered['EP'].loc['2024-03-31', 'ABC'])
        self.assertAlmostEqual(legs[0], .1)
        self.assertAlmostEqual(legs[0], legs[1])

    def test_nse_monthly_price_loader_filters_and_rejects_duplicates(self):
        import run_csm_value_backtest as runner
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'nse.csv'
            path.write_text('datetime,symbol,series,close\n2024-01-31,ABC,EQ,100\n2024-01-31,XYZ,EQ,200\n')
            prices = runner.load_nse_monthly_prices(symbols={'ABC'}, path=path)
            self.assertEqual(prices.loc['2024-01-31', 'ABC'], 100)
            self.assertEqual(list(prices.columns), ['ABC'])
            with path.open('a') as f:
                f.write('2024-01-31,ABC,BE,101\n')
            with self.assertRaisesRegex(ValueError, 'ambiguous'):
                runner.load_nse_monthly_prices(path=path)

    def test_empty_signal_month_clears_target_positions(self):
        idx = pd.bdate_range('2024-01-01', '2024-04-30')
        px = pd.DataFrame({'ABC': np.linspace(100., 120., len(idx))}, index=idx)
        st = CSMValue(px, px * 10, benchmark_series=px.ABC, min_eligible=1,
                      use_swap_gap=False)
        months = pd.to_datetime(['2024-03-31', '2024-04-30'])
        st.factors = pd.DataFrame({'ABC': [1., np.nan]}, index=months)
        st.momentum_returns = pd.DataFrame({'ABC': [1., np.nan]}, index=months)
        positions = st.get_positions()
        self.assertGreater(positions.loc['2024-03-31', 'ABC'], 0.)
        self.assertEqual(positions.loc['2024-04-30', 'ABC'], 0.)

    def test_no_price_volume_rank_cutoff(self):
        idx = pd.bdate_range('2024-01-01', '2024-04-30')
        px = pd.DataFrame({'LIQUID': 100., 'THIN': 100.}, index=idx)
        volume = pd.DataFrame({'LIQUID': 1_000_000., 'THIN': 0.}, index=idx)
        st = CSMValue(px, volume, benchmark_series=px.LIQUID)
        monthly = px.resample('ME').last()
        eligible = pd.DataFrame(True, index=monthly.index, columns=monthly.columns)
        mask = st.filter_universe(monthly, None, px, fundamentals_eligible=eligible, valuation_prices=monthly)
        self.assertTrue(mask.loc['2024-04-30', 'LIQUID'])
        self.assertTrue(mask.loc['2024-04-30', 'THIN'])

    def test_missing_verified_valuation_prices_fails_closed(self):
        idx = pd.bdate_range('2024-01-01', periods=2)
        px = pd.DataFrame({'ABC': [1., 1.]}, index=idx)
        st = CSMValue(px, px, benchmark_series=px.ABC)
        with self.assertRaisesRegex(ValueError, 'verified as-traded'):
            st.calculate_factors()


class ExecutionTest(unittest.TestCase):
    def test_close_stop_uses_next_open_and_exit_day_zero_weight(self):
        import run_csm_value_backtest as runner
        dates = pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-01',
                                '2024-02-02', '2024-02-05', '2024-02-06'])
        close = pd.DataFrame({'ABC': [100., 100., 100., 80., 70., 70.]}, index=dates)
        opening = pd.DataFrame({'ABC': [100., 100., 100., 100., 70., 70.]}, index=dates)
        st = CSMValue(close, close * 1000, opens_df=opening,
                      benchmark_series=pd.Series(100., index=dates),
                      use_crash_guard=False, min_hold_days=0,
                      use_liquid_mf=False, leverage_bull=1., leverage_bear=1.,
                      leverage_panic=1., rebalance_exit_buffer_months=0,
                      use_trade_deadband=False)
        st.positions = pd.DataFrame({'ABC': [.05]}, index=pd.to_datetime(['2024-01-31']))
        st.factors = st.positions.copy()
        st.all_ranks = pd.DataFrame({'ABC': [1.]}, index=st.positions.index)
        st.factor_legs = {'EP': st.positions.copy()}
        st._signal_age = st.positions.copy()
        st._prepare_stop_indicators(close.resample('ME').last())
        st._panic_threshold_series = None
        st._bench_vol_monthly = None
        st.atr = None
        st._bvol_daily = None
        result = runner.backtest_event_driven(st, initial_capital=100000,
                                              transaction_cost=0., risk_free_rate=0.)
        stop = next(x for x in st.position_metadata if x['Exit_Reason'] == 'STOP_HIT')
        self.assertEqual(stop['Entry_Date'], pd.Timestamp('2024-02-01'))
        self.assertEqual(stop['Exit_Date'], pd.Timestamp('2024-02-05'))
        self.assertEqual(stop['Exit_Price'], 70.)
        self.assertEqual(result['executed_weights'].loc['2024-02-05', 'ABC'], 0.)
        self.assertAlmostEqual(result['net_returns'].loc['2024-02-02'], -.01)
        self.assertAlmostEqual(result['net_returns'].loc['2024-02-05'], 0.)

    def test_pending_stop_waits_through_a_missing_bar(self):
        import run_csm_value_backtest as runner
        dates = pd.to_datetime(['2024-01-30', '2024-01-31', '2024-02-01',
                                '2024-02-02', '2024-02-05', '2024-02-06'])
        close = pd.DataFrame({'ABC': [100., 100., 100., 80., np.nan, 70.]}, index=dates)
        opening = pd.DataFrame({'ABC': [100., 100., 100., 100., np.nan, 70.]}, index=dates)
        st = CSMValue(close, close.fillna(0) * 1000, opens_df=opening,
                      benchmark_series=pd.Series(100., index=dates),
                      use_crash_guard=False, min_hold_days=0, use_liquid_mf=False,
                      leverage_bull=1., leverage_bear=1., leverage_panic=1.,
                      rebalance_exit_buffer_months=0, use_trade_deadband=False)
        st.positions = pd.DataFrame({'ABC': [.05]}, index=pd.to_datetime(['2024-01-31']))
        st.factors = st.positions.copy()
        st.all_ranks = pd.DataFrame({'ABC': [1.]}, index=st.positions.index)
        st.factor_legs = {'EP': st.positions.copy()}
        st._signal_age = st.positions.copy()
        st._prepare_stop_indicators(close.resample('ME').last())
        st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
        result = runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
        stop = next(x for x in st.position_metadata if x['Exit_Reason'] == 'STOP_HIT')
        self.assertEqual(stop['Exit_Date'], pd.Timestamp('2024-02-06'))
        self.assertEqual(stop['Exit_Price'], 70.)
        self.assertAlmostEqual(result['net_returns'].loc['2024-02-05'], 0.)
        self.assertAlmostEqual(result['net_returns'].loc['2024-02-06'], 0.)

    def test_period_drawdown_includes_first_day_loss(self):
        import run_csm_value_backtest as runner
        r = pd.Series([-.10, .05], index=pd.to_datetime(['2024-01-02', '2024-01-03']))
        metrics = runner.window_metrics(r, '2024-01-02', '2024-01-03')
        self.assertAlmostEqual(metrics['max_drawdown'], -.10)

    def test_rebalance_trade_log_uses_open_fill(self):
        import run_csm_value_backtest as runner
        dates = pd.to_datetime(['2024-01-02', '2024-01-03'])
        px = pd.DataFrame({'ABC': [100., 90.]}, index=dates)
        st = CSMValue(px, px, benchmark_series=px.ABC)
        holding = {'entry_price': 100., 'entry_date': dates[0], 'entry_idx': 0,
                   'peak_price': 100., 'atr_stop': 85., 'weight': .05}
        runner._record_closed_trade(st, 'ABC', holding, dates[1], exit_price=90.,
                                    fill_price=80., exit_reason='REBALANCE',
                                    stop_price_at_exit=85., exit_idx=1)
        self.assertEqual(st.position_metadata[-1]['Exit_Price'], 80.)

    def test_position_cap_includes_buffered_exit(self):
        import run_csm_value_backtest as runner
        dates = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-29',
                                '2024-03-01', '2024-03-28', '2024-04-01', '2024-04-02'])
        px = pd.DataFrame({'ABC': 100., 'XYZ': 100.}, index=dates)
        st = CSMValue(px, px * 1000, opens_df=px, benchmark_series=px.ABC,
                      top_n=1, use_crash_guard=False, use_liquid_mf=False,
                      leverage_bear=1., rebalance_exit_buffer_months=1,
                      use_trade_deadband=False)
        months = pd.to_datetime(['2024-01-31', '2024-02-29', '2024-03-31'])
        st.positions = pd.DataFrame({'ABC': [.05, 0., 0.], 'XYZ': [0., .05, .05]}, index=months)
        st.factors = pd.DataFrame({'ABC': [1., 0., 0.], 'XYZ': [0., 1., 1.]}, index=months)
        st.all_ranks = st.factors.rank(axis=1, ascending=False)
        st.momentum_returns = pd.DataFrame(1., index=months, columns=px.columns)
        st.factor_legs = {'EP': st.factors.copy()}
        st._signal_age = st.factors.copy()
        st._prepare_stop_indicators(px.resample('ME').last())
        st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
        result = runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
        w = result['executed_weights']
        self.assertLessEqual((w > 1e-6).sum(axis=1).max(), 1)
        self.assertGreater(w.loc['2024-03-01', 'ABC'], 0.)
        self.assertEqual(w.loc['2024-03-01', 'XYZ'], 0.)
        self.assertGreater(w.loc['2024-04-01', 'XYZ'], 0.)
        self.assertTrue(any(x['Reject_Reason'] == 'MAX_POSITIONS' for x in st.reject_log))

    def test_weekend_month_end_trades_next_session(self):
        import run_csm_value_backtest as runner
        dates = pd.to_datetime(['2024-03-27', '2024-03-28', '2024-03-29',
                                '2024-04-01', '2024-04-02'])
        px = pd.DataFrame({'ABC': 100.}, index=dates)
        st = CSMValue(px, px * 1000, opens_df=px, benchmark_series=px.ABC,
                      use_crash_guard=False, use_liquid_mf=False,
                      leverage_bear=1., rebalance_exit_buffer_months=0)
        st.positions = pd.DataFrame({'ABC': [.05]}, index=pd.to_datetime(['2024-03-31']))
        st.factors = st.positions.copy()
        st.all_ranks = pd.DataFrame({'ABC': [1.]}, index=st.positions.index)
        st.factor_legs = {'EP': st.positions.copy()}
        st._signal_age = st.positions.copy()
        st._prepare_stop_indicators(px.resample('ME').last())
        st._panic_threshold_series = None
        st._bench_vol_monthly = None
        st.atr = None
        st._bvol_daily = None
        runner.backtest_event_driven(st, transaction_cost=0., risk_free_rate=0.)
        self.assertEqual(st.position_metadata[0]['Entry_Date'], pd.Timestamp('2024-04-01'))


if __name__ == '__main__':
    unittest.main()

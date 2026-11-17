"""Execution-book and turnover tests for the experimental backtest."""
import contextlib
import io
import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from csm_value_experimental_strategy import CSMValue
import run_csm_value_experimental_backtest as runner


def run_fixture(dates, closes, opens, positions, cost=0.):
    idx = pd.to_datetime(dates)
    prices = pd.DataFrame({'ABC': closes}, index=idx, dtype=float)
    opening = pd.DataFrame({'ABC': opens}, index=idx, dtype=float)
    with contextlib.redirect_stdout(io.StringIO()):
        st = CSMValue(prices, prices * 1000, opens_df=opening,
                      benchmark_series=pd.Series(100., index=idx), ranking_mode='value',
                      use_crash_guard=False, use_liquid_mf=False,
                      leverage_bull=1., leverage_bear=1., leverage_panic=1.,
                      hard_stop_from_entry=.8, hard_stop_from_peak=.8, min_hold_days=0,
                      rebalance_exit_buffer_months=0, use_trade_deadband=False)
        st.positions = pd.DataFrame({'ABC': list(positions.values())},
                                    index=pd.to_datetime(list(positions)))
        st.factors = st.positions.copy()
        st.momentum_returns = st.positions.copy()
        st.all_ranks = pd.DataFrame({'ABC': 1.}, index=st.positions.index)
        st.factor_legs = {'EP': st.positions.copy()}
        st._signal_age = st.positions.copy()
        st._prepare_stop_indicators(prices.resample('ME').last())
        st._panic_threshold_series = st._bench_vol_monthly = st.atr = st._bvol_daily = None
        result = runner.backtest_event_driven(st, initial_capital=100000,
                                               transaction_cost=cost, risk_free_rate=0.)
        result['_fixture_strategy'] = st
    return result


class DriftAccountingTest(unittest.TestCase):
    def test_drift_is_not_rebalanced_daily_and_monthly_trade_is_charged(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-02',
                         '2024-02-05', '2024-02-29', '2024-03-01'],
                        [100, 100, 120, 120, 120, 120],
                        [100, 100, 100, 120, 120, 120],
                        {'2024-01-31': .5, '2024-02-29': .5}, cost=.01)
        # Entry buys 50% and charges 0.5% of opening NAV. After the 20%
        # rise, the actual book is 60,000 in stock and 49,500 in cash.
        self.assertAlmostEqual(r['transaction_costs'].loc['2024-02-01'], .005)
        self.assertAlmostEqual(r['execution_book_value'].loc['2024-02-02'], 109500.)
        drifted = 60000 / 109500
        self.assertAlmostEqual(r['executed_weights'].loc['2024-02-05', 'ABC'], drifted)
        self.assertEqual(r['turnover'].loc['2024-02-05'], 0.)
        self.assertAlmostEqual(r['turnover'].loc['2024-03-01'], drifted - .5)
        self.assertAlmostEqual(r['transaction_costs'].loc['2024-03-01'], (drifted - .5) * .01)
        tx = r['transactions']
        self.assertEqual(list(tx['Side']), ['BUY', 'SELL'])
        self.assertAlmostEqual(tx.iloc[1]['Trade_Value'], -5250.)
        self.assertAlmostEqual(tx.iloc[1]['Transaction_Cost'], 52.5)
        # With no full exit, the reported return path and the self-financing
        # execution book agree exactly, including transaction costs.
        for date in r['equity_curve'].index:
            self.assertAlmostEqual(r['equity_curve'].loc[date] * 100000,
                                   r['execution_book_value'].loc[date])
        with contextlib.redirect_stdout(io.StringIO()):
            trade = runner.get_trade_log(r['_fixture_strategy']).iloc[0]
        self.assertAlmostEqual(trade['Quantity'], 500.)
        self.assertAlmostEqual(trade['Position_Size'], 50000.)
        self.assertAlmostEqual(trade['PnL_Abs'], 9447.5)

    def test_overnight_gap_marks_the_open_before_trading(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-02'],
                        [100, 100, 120], [100, 100, 120], {'2024-01-31': .5})
        self.assertAlmostEqual(r['executed_weights'].loc['2024-02-02', 'ABC'], .6 / 1.1)
        self.assertEqual(r['turnover'].loc['2024-02-02'], 0.)
        self.assertAlmostEqual(r['execution_book_value'].loc['2024-02-02'], 110000.)
        self.assertAlmostEqual(r['net_returns'].loc['2024-02-02'], .10)

    def test_new_entry_does_not_receive_pre_entry_overnight_return(self):
        r = run_fixture(['2024-01-31', '2024-02-01'], [100, 120], [100, 120],
                        {'2024-01-31': .5})
        self.assertAlmostEqual(r['executed_weights'].loc['2024-02-01', 'ABC'], .5)
        self.assertEqual(r['net_returns'].loc['2024-02-01'], 0.)

    def test_overnight_rebalance_and_intraday_move_match_execution_book(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-29', '2024-03-01'],
                        [100, 100, 100, 110], [100, 100, 100, 120],
                        {'2024-01-31': .5, '2024-02-29': .4}, cost=.01)
        # Opening NAV 109,500; sell 16,200, pay 162; the remaining
        # position loses 3,650 from the open to the close.
        self.assertAlmostEqual(r['execution_book_value'].iloc[-1], 105688.)
        self.assertAlmostEqual(r['equity_curve'].iloc[-1] * 100000, 105688.)
        self.assertAlmostEqual(r['transactions'].iloc[-1]['Trade_Value'], -16200.)

    def test_reporting_slice_rebases_book_and_transaction_amounts_consistently(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-02',
                         '2024-02-05', '2024-02-29', '2024-03-01'],
                        [100, 100, 120, 120, 120, 120],
                        [100, 100, 100, 120, 120, 120],
                        {'2024-01-31': .5, '2024-02-29': .5}, cost=.01)
        with contextlib.redirect_stdout(io.StringIO()):
            runner.slice_results(r, '2024-02-01', risk_free_rate=0.)
            trade = runner.get_trade_log(r['_fixture_strategy']).iloc[0]
        scale = 100000 / 99500
        self.assertAlmostEqual(r['execution_book_value'].iloc[0], 100000.)
        self.assertAlmostEqual(r['transactions'].iloc[0]['Trade_Value'], 50000 * scale)
        self.assertAlmostEqual(trade['PnL_Abs'], round(9447.5 * scale, 2))

    def test_exit_day_convention_is_preserved_with_real_open_turnover(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-29', '2024-03-01'],
                        [100, 100, 100, 90], [100, 100, 100, 80],
                        {'2024-01-31': .5, '2024-02-29': 0.})
        self.assertEqual(r['executed_weights'].loc['2024-03-01', 'ABC'], 0.)
        self.assertEqual(r['net_returns'].loc['2024-03-01'], 0.)
        self.assertAlmostEqual(r['turnover'].loc['2024-03-01'], .4 / .9)
        # The separate open/close execution book captures the gap. Reported
        # returns deliberately retain the requested zero exit-day weight.
        self.assertAlmostEqual(r['execution_book_value'].loc['2024-03-01'], 90000.)

    def test_exit_fee_accounts_for_overnight_change_in_book_value(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-29', '2024-03-01'],
                        [100, 100, 100, 80], [100, 100, 100, 80],
                        {'2024-01-31': .5, '2024-02-29': 0.}, cost=.01)
        # Previous-close book: 50,000 stock and 49,500 cash. The 80 open
        # sells 40,000 of stock for a 400 fee, or 400 / 99,500 of prior NAV.
        self.assertAlmostEqual(r['turnover'].loc['2024-03-01'], 40000 / 89500)
        self.assertAlmostEqual(r['transaction_costs'].loc['2024-03-01'], 400 / 99500)
        self.assertAlmostEqual(r['net_returns'].loc['2024-03-01'], -400 / 99500)

    def test_fully_invested_target_funds_fees_without_borrowing(self):
        before = pd.Series({'A': 0., 'B': 0.})
        desired = pd.Series({'A': .5, 'B': .5})
        after, cash, trades, turnover, cost = runner._execute_weight_targets(before, desired, .01)
        self.assertAlmostEqual(turnover, 1 / 1.01)
        self.assertAlmostEqual(after.sum() + cash + cost, 1.)
        self.assertGreaterEqual(cash, 0.)
        self.assertAlmostEqual(trades.sum(), after.sum())

    def test_missing_open_does_not_create_a_trade(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-02', '2024-02-05'],
                        [100, 100, 110, 110], [100, 100, float('nan'), 110],
                        {'2024-01-31': .5})
        self.assertEqual(r['turnover'].loc['2024-02-02'], 0.)
        self.assertEqual(len(r['transactions']), 1)
        self.assertAlmostEqual(r['execution_book_value'].loc['2024-02-02'], 105000.)

    def test_resize_deferred_by_missing_open_retries_next_session(self):
        r = run_fixture(['2024-01-31', '2024-02-01', '2024-02-29',
                         '2024-03-01', '2024-03-04'],
                        [100, 100, 100, 100, 100],
                        [100, 100, 100, float('nan'), 100],
                        {'2024-01-31': .5, '2024-02-29': .4})
        self.assertEqual(r['turnover'].loc['2024-03-01'], 0.)
        self.assertAlmostEqual(r['executed_weights'].loc['2024-03-01', 'ABC'], .5)
        self.assertAlmostEqual(r['turnover'].loc['2024-03-04'], .1)
        self.assertAlmostEqual(r['executed_weights'].loc['2024-03-04', 'ABC'], .4)

    def test_opening_trade_does_not_use_that_days_close(self):
        dates = ['2024-01-31', '2024-02-01', '2024-02-29', '2024-03-01']
        opens = [100, 100, 100, 100]
        pos = {'2024-01-31': .5, '2024-02-29': .4}
        low = run_fixture(dates, [100, 100, 100, 80], opens, pos)
        high = run_fixture(dates, [100, 100, 100, 120], opens, pos)
        pd.testing.assert_frame_equal(low['transactions'], high['transactions'])
        self.assertNotEqual(low['execution_book_value'].iloc[-1], high['execution_book_value'].iloc[-1])

    def test_crash_guard_retries_missing_open_and_charges_actual_sale(self):
        idx = pd.to_datetime(['2024-01-31', '2024-02-01', '2024-02-02', '2024-02-05'])
        prices = pd.DataFrame({'ABC': [100., 100., 80., 80.]}, index=idx)
        opens = pd.DataFrame({'ABC': [100., 100., float('nan'), 80.]}, index=idx)
        with contextlib.redirect_stdout(io.StringIO()):
            st = CSMValue(prices, prices * 1000, opens_df=opens,
                benchmark_series=pd.Series(100., index=idx), ranking_mode='value',
                use_crash_guard=True, use_liquid_mf=False, leverage_bear=1.,
                hard_stop_from_entry=.8, hard_stop_from_peak=.8,
                rebalance_exit_buffer_months=0, use_trade_deadband=False)
            st.positions = pd.DataFrame({'ABC': [.5]}, index=pd.to_datetime(['2024-01-31']))
            st.factors = st.positions.copy()
            st.momentum_returns = st.positions.copy()
            st.all_ranks = pd.DataFrame({'ABC': [1.]}, index=st.positions.index)
            st.factor_legs = {'EP': st.positions.copy()}
            st._signal_age = st.positions.copy()
            st._prepare_stop_indicators(prices.resample('ME').last())
            st._bvol_daily = pd.Series([0., 0., 1., 0.], index=idx)
            st._panic_threshold_series = pd.Series(.5, index=idx)
            st._bench_vol_monthly = None
            st.atr = None
            r = runner.backtest_event_driven(st, initial_capital=100000,
                                             transaction_cost=.01, risk_free_rate=0.)
        self.assertEqual(r['turnover'].loc['2024-02-02'], 0.)
        self.assertGreater(r['executed_weights'].loc['2024-02-02', 'ABC'], 0.)
        self.assertEqual(r['executed_weights'].loc['2024-02-05', 'ABC'], 0.)
        self.assertAlmostEqual(r['execution_book_value'].loc['2024-02-05'], 89100.)
        self.assertAlmostEqual(r['transactions'].iloc[-1]['Transaction_Cost'], 400.)
        self.assertEqual(st.position_metadata[0]['Exit_Reason'], 'CRASH_GUARD')


if __name__ == '__main__':
    unittest.main()

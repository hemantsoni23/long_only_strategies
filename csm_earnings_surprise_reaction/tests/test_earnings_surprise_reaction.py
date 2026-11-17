import os
import sys
import contextlib
import io
import tempfile
import unittest

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from earnings_surprise_reaction_fundamentals import _parse_date, build_events
from earnings_surprise_reaction_strategy import EarningsSurpriseReactionStrategy


def facts():
    rows = []
    for i, end in enumerate(pd.date_range('2018-03-31', periods=20, freq='QE')):
        rows.append({'symbol': 'ABC', 'basis': 'standalone', 'period_end': end,
                     'filed_date': end + pd.Timedelta(days=20), 'eps': float(i * i + i % 3),
                     'shares': 100., 'net_profit': float(i * i + 2), 'revenue': 100., 'ebit': 10.})
    return pd.DataFrame(rows)


def engine(missing_open=False, stop=False):
    dates = pd.bdate_range('2023-01-02', periods=8)
    close = pd.DataFrame({'ABC': [100., 100., 90. if stop else 110., 111., 112., 113., 114., 115.]}, index=dates)
    opens = pd.DataFrame({'ABC': [100., 100., 105., np.nan if missing_open else 106., 107., 108., 109., 110.]}, index=dates)
    st = EarningsSurpriseReactionStrategy(close, close * 1000, opens_df=opens, benchmark_series=pd.Series(1., index=dates),
                      max_positions=1, hold_days=1 if not stop else 60, cash_annual_rate=0,
                      transaction_cost=0, stop_slippage_pct=0, hard_stop=.15 if not stop else .16)
    st._dates = dates; st._cols = {'ABC': 0}; st._C = close.to_numpy(); st._Craw = close.to_numpy()
    st._O = opens.to_numpy(); st._prev_close = close.shift().to_numpy(); st._circ = np.zeros((len(dates), 1))
    st._gate_ok = np.ones(len(dates), dtype=bool)
    st.candidates = pd.DataFrame([{'symbol': 'ABC', 'sig_idx': 1, 'sig_date': dates[1],
                                   'filed': dates[0], 'score': 1., 'sue_eps': 2., 'ear': .1}])
    return st


class EarningsSurpriseReactionTests(unittest.TestCase):
    def test_iso_and_exchange_filing_dates_are_not_swapped(self):
        self.assertEqual(_parse_date('2020-11-05'), pd.Timestamp('2020-11-05'))
        self.assertEqual(_parse_date('05-Nov-2020 17:30:00'), pd.Timestamp('2020-11-05'))

    def test_later_filings_and_future_basis_do_not_change_earlier_events(self):
        f = facts()
        cutoff = pd.Timestamp('2022-06-30')
        first = build_events(facts=f[f.filed_date <= cutoff])
        full = build_events(facts=f)
        pd.testing.assert_frame_equal(first, full[full.filed <= cutoff].reset_index(drop=True))
        self.assertGreater(len(first), 0)
        # A later consolidated filing for the same quarter cannot replace
        # an already emitted standalone event at an earlier date.
        row = f.iloc[-2].copy(); row['basis'] = 'consolidated'; row['filed_date'] += pd.Timedelta(days=1)
        later = build_events(facts=pd.concat([f, row.to_frame().T], ignore_index=True))
        pd.testing.assert_frame_equal(full, later)

    def test_share_change_does_not_manufacture_sue(self):
        f = facts(); baseline = build_events(facts=f)
        self.assertGreater(len(baseline), 0)
        f.loc[f.period_end < pd.Timestamp('2021-06-30'), 'shares'] = 50.
        guarded = build_events(facts=f)
        self.assertNotIn(pd.Timestamp('2021-06-30'), set(guarded.period_end))

    def test_backtest_buys_and_sells_at_later_valid_opens(self):
        st = engine(missing_open=True)
        res = st.simulate()
        trade = res['trades'].iloc[0]
        self.assertEqual(trade.Entry_Date, st._dates[2])
        self.assertEqual(trade.Entry_Price, 105.)
        # Held one trading day on date 3: decision at close, sold date 4 open.
        self.assertEqual(trade.Exit_Date, st._dates[4])
        self.assertEqual(trade.Exit_Price, 107.)
        self.assertEqual(trade.Reason, 'TIME_STOP')

    def test_stop_retry_and_calendar_limit(self):
        st = engine(missing_open=True, stop=True)
        st.hard_stop = .10
        res = st.simulate()
        trade = res['trades'].iloc[0]
        self.assertEqual(trade.Reason, 'STOP_HIT')
        self.assertEqual(trade.Exit_Date, st._dates[4])
        self.assertEqual(trade.Exit_Price, 107.)
        with self.assertRaises(ValueError):
            st.simulate(end='2025-01-02')

    def test_missing_entry_open_is_not_replaced_with_close(self):
        st = engine()
        st._O[2, 0] = np.nan
        res = st.simulate()
        self.assertEqual(res['trades'].iloc[0].Entry_Date, st._dates[3])
        self.assertEqual(res['trades'].iloc[0].Entry_Price, 106.)

    def test_live_time_exit_is_scheduled_for_next_open(self):
        st = engine()
        result = st.get_exit_signals({'ABC': {'entry_price': 105., 'entry_date': st._dates[2]}},
                                     {'ABC': {'close': 111.}}, today=st._dates[3])
        self.assertEqual(result['exits']['ABC']['reason'], 'TIME_STOP')
        self.assertEqual(result['exits']['ABC']['action'], 'exit_next_open')

    def test_report_rebases_returns_and_includes_partial_first_year(self):
        import backtest_report as report
        dates = pd.to_datetime(['2020-12-29', '2020-12-30', '2020-12-31', '2021-01-04'])
        equity = pd.Series([100., 110., 121., 133.1], index=dates)
        result = {'equity_curve': equity, 'portfolio_value': equity,
                  'net_returns': equity.pct_change().fillna(0),
                  'executed_weights': pd.DataFrame({'ABC': .5}, index=dates),
                  'turnover': pd.Series(.1, index=dates)}
        with tempfile.TemporaryDirectory() as tmp:
            report.configure('test', 'test', tmp)
            with contextlib.redirect_stdout(io.StringIO()) as capture:
                sliced = report.slice_results(result, '2020-12-30', risk_free_rate=0)
                report.print_yearly_returns(sliced['portfolio_value'])
            self.assertEqual(sliced['net_returns'].iloc[0], 0)
            self.assertEqual(sliced['turnover'].iloc[0], 0)
            self.assertAlmostEqual(sliced['total_return'], .21)
            self.assertIn('2020', capture.getvalue())
            self.assertIn('10.00%', capture.getvalue())

    def test_no_top_1000_cutoff(self):
        st = engine()
        self.assertTrue(st._universe_ok(2, 0))
        with self.assertRaises(ValueError):
            EarningsSurpriseReactionStrategy(st.prices, st.volumes, benchmark_series=st.benchmark, universe_top_n=1000)

    def test_signals_and_portfolio_survive_future_data_truncation(self):
        dates = pd.bdate_range('2023-01-02', periods=160)
        x = np.arange(len(dates))
        close = pd.DataFrame({'ABC': 100 * np.exp(.001 * x + .04 * np.sin(x / 8)),
                              'XYZ': 100 * np.exp(.0005 * x + .05 * np.cos(x / 7))}, index=dates)
        op = close.shift(1).fillna(close.iloc[0]) * 1.002
        vol = close * 1000
        benchmark = pd.Series(np.exp(.0003 * x), index=dates)
        events = pd.DataFrame([{'symbol': sym, 'filed': dates[i], 'sue_eps': float(k + j * .7 + 1),
                                'dm_ebit': 0.1} for k, i in enumerate(range(8, 120, 9))
                               for j, sym in enumerate(('ABC', 'XYZ'))])
        def run(end):
            st = EarningsSurpriseReactionStrategy(close.loc[:end], vol.loc[:end], opens_df=op.loc[:end],
                              benchmark_series=benchmark.loc[:end], events_df=events, min_pool=2,
                              top_pct=.8, hold_days=10, max_positions=2)
            candidates = st.calculate_factors()
            return st, candidates, st.simulate()
        full, c1, r1 = run(dates[-1])
        cut, c2, r2 = run(dates[130])
        check_end = dates[125]
        a = c1[c1.sig_date <= check_end].reset_index(drop=True)
        b = c2[c2.sig_date <= check_end].reset_index(drop=True)
        self.assertGreater(len(a), 0)
        pd.testing.assert_frame_equal(a, b)
        self.assertTrue((a.sig_date > a.filed).all())
        pd.testing.assert_series_equal(r1['equity'].loc[:check_end], r2['equity'].loc[:check_end])
        self.assertTrue((r1['trades'].Entry_Date > r1['trades'].Signal_Date).all())
        np.testing.assert_allclose(r1['transactions'].Transaction_Cost,
                                   r1['transactions'].Trade_Value * full.transaction_cost)


if __name__ == '__main__':
    unittest.main()

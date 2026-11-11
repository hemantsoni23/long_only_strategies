"""Regression tests runnable in an isolated copy: python -m unittest discover."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd

from residual_momentum_v2_strategy import ResidualMomentumV2
import residual_momentum_v2_backtest as bt


def sample_panel():
    rng = np.random.default_rng(4242)
    days = pd.bdate_range('2019-01-01', periods=800)
    cols = [f'STOCK{i:02}' for i in range(16)]
    close = pd.DataFrame(100 * np.exp(np.cumsum(rng.normal(0.0007, 0.013, (len(days), len(cols))), axis=0)), index=days, columns=cols)
    volume = pd.DataFrame(500000., index=days, columns=cols)
    return close, volume, close * 1.01, close * 0.99, close * 0.999


class StandaloneTests(unittest.TestCase):
    def make_strategy(self):
        st = ResidualMomentumV2(*sample_panel(), universe_rank_min=1, universe_top_n=16,
                                cash_sweep_etf=None, min_adv=0, min_price=0,
                                n=8, enter_rank=8, exit_rank=12, pos_cap=0.2)
        st.calculate_factors()
        st.get_positions('2021-01-01')
        return st

    def test_cash_and_sweep_backtests(self):
        st = self.make_strategy()
        cash, turnover = bt.backtest_event_driven(st, aum=100000)
        self.assertGreater(len(cash), 100)
        self.assertTrue(np.isfinite(cash).all())
        self.assertGreater(turnover, 0)
        st.cash_sweep_etf = 'GOLDBEES'
        prices = pd.Series(np.linspace(20, 25, len(st.days)), index=st.days)
        etf = pd.DataFrame({'open': prices, 'close': prices, 'volume': 1e7}, index=prices.index)
        with patch.object(bt, 'load_etf_data', return_value=etf):
            sweep, _ = bt.backtest_event_driven(st, aum=100000)
            self.assertEqual(list(sweep.index), list(cash.index))
            self.assertTrue(np.isfinite(sweep).all())
            self.assertFalse(sweep.equals(cash))
            with self.assertRaisesRegex(ValueError, 'stagger'):
                bt.backtest_event_driven(st, stagger=True)
        with patch.object(bt, 'load_etf_data', return_value=etf.iloc[:-10]):
            with self.assertRaisesRegex(ValueError, 'ETF data missing'):
                bt.backtest_event_driven(st)

    def test_flat_zero_cost_etf_matches_cash(self):
        st = self.make_strategy()
        cash, _ = bt.backtest_event_driven(st, aum=100000, fixed_bps=0, impact_k=0)
        st.cash_sweep_etf = 'GOLDBEES'
        etf = pd.DataFrame({'open': 100., 'close': 100., 'volume': 1e9}, index=st.days)
        with patch.object(bt, 'load_etf_data', return_value=etf):
            sweep, _ = bt.backtest_event_driven(st, aum=100000, fixed_bps=0, impact_k=0)
        np.testing.assert_allclose(sweep, cash, rtol=0, atol=1e-12)

    def test_calendar_cagr_and_initial_drawdown(self):
        dates = pd.to_datetime(['2020-01-01', '2021-01-01'])
        net = pd.Series([-0.1, 0.2], index=dates)
        m = bt.metrics(net, pd.Series(0., index=dates))
        self.assertEqual(m, bt.metrics(net, pd.Series(0., index=dates), rf_annual=0))
        expected = (0.9 * 1.2) ** (365.2425 / 366) - 1
        self.assertAlmostEqual(m['CAGR'], expected)
        self.assertAlmostEqual(m['MaxDD'], -0.1)
        expected_downside = np.sqrt((0.1 ** 2) / 2)
        self.assertAlmostEqual(m['Sortino'], net.mean() / expected_downside * np.sqrt(252))

    def test_cash_default_earns_no_interest(self):
        from types import SimpleNamespace
        days = pd.bdate_range('2020-01-01', periods=40)
        close = pd.DataFrame(100., index=days, columns=['S'])
        st = SimpleNamespace(days=days, close=close, opn=close.copy(), tv=close * 1e6,
            atr=close * 0, low=close.copy(), high=close.copy(), drift_band=0,
            breaker=None, atr_k=None, trading_days=252, cash_sweep_etf=None,
            positions=pd.DataFrame({'S': [0.]}, index=days[[20]]))
        net, _ = bt.backtest_event_driven(st, aum=100000)
        self.assertTrue((net == 0).all())

    def test_sweep_costs_and_long_only_accounting(self):
        from types import SimpleNamespace
        days = pd.bdate_range('2020-01-01', periods=45)
        close = pd.DataFrame(100.0, index=days, columns=['S'])
        st = SimpleNamespace(days=days, close=close, opn=close.copy(), tv=close * 1e6,
            atr=close * 0, low=close.copy(), high=close.copy(), drift_band=0,
            breaker=None, atr_k=None, trading_days=252)
        weights = pd.DataFrame({'S': [0., 1., 0.]}, index=days[[20, 25, 30]])
        etf = pd.Series(100.0, index=days)
        volume = pd.Series(1e6, index=days)
        net, _, fraction = bt._simulate_with_sweep(st, weights, 100000, 15, 0, .25, 10,
                                                   .05, 75, etf, etf, volume)
        self.assertLess(net.iloc[0], 0, 'initial ETF purchase fee must be in returns')
        self.assertGreater(st.cash_sweep_costs['etf_buy_orders'], 0)
        self.assertGreater(st.cash_sweep_costs['etf_sell_orders'], 0)
        self.assertGreaterEqual(fraction.min(), 0)
        self.assertGreaterEqual(st.cash_sweep_cash.min(), 0)
        trades = st.cash_sweep_trades
        np.testing.assert_allclose(trades['value'] / trades['price'], np.round(trades['value'] / trades['price']), rtol=0, atol=1e-9)
        self.assertTrue(all(item['Quantity'] == int(item['Quantity']) for item in st.position_metadata))
        np.testing.assert_allclose(trades['cost'], trades['value'] * .0015, rtol=1e-10)
        self.assertAlmostEqual(trades['cost'].sum(), st.cash_sweep_costs['etf'], places=6)
        expected = 1 - (st.cash_sweep_costs['etf'] + st.cash_sweep_costs['stock']) / 100000
        self.assertAlmostEqual((1 + net).prod(), expected, places=9)
        # Missing ETF bar: the prior close marks value but cannot execute an order.
        missing = days[26]
        st2 = SimpleNamespace(**{k: v for k, v in vars(st).items() if k in
            ['days', 'close', 'opn', 'tv', 'atr', 'low', 'high', 'drift_band', 'breaker', 'atr_k', 'trading_days']})
        bt._simulate_with_sweep(st2, weights, 100000, 15, 0, .25, 10, .05, 75,
                                etf.drop(missing), etf.drop(missing), volume.drop(missing))
        self.assertNotIn(missing, list(st2.cash_sweep_trades['date']))
        self.assertGreaterEqual(st2.cash_sweep_cash.min(), 0)

    def test_stock_execution_waits_for_real_open(self):
        from types import SimpleNamespace
        days = pd.bdate_range('2020-01-01', periods=40)
        close = pd.DataFrame(100., index=days, columns=['S'])
        opens = close.copy()
        opens.loc[days[26], 'S'] = np.nan
        st = SimpleNamespace(days=days, close=close, opn=opens, tv=close * 1e6,
            atr=close * 0, low=close.copy(), high=close.copy(), drift_band=0,
            breaker=None, atr_k=None, trading_days=252)
        weights = pd.DataFrame({'S': [1., 0.]}, index=days[[20, 25]])
        etf = pd.Series(100., index=days)
        bt._simulate_with_sweep(st, weights, 100000, 15, 0, .25, 10, .05, 75,
                                etf, etf, etf * 10000)
        self.assertGreater(st.cash_sweep_costs['skipped_stock_fills'], 0)
        self.assertTrue(all(row['Exit_Date'] != days[26] for row in st.position_metadata))

    def test_etf_timestamps_use_indian_calendar_date(self):
        with tempfile.TemporaryDirectory() as temp:
            Path(temp, 'GOLDBEES.csv').write_text('timestamp,open,close,volume\n2021-01-04T00:00:00+05:30,10,11,1000\n')
            with patch.object(bt, 'DATA_DIR', temp):
                opn, close = bt.load_etf_prices('GOLDBEES')
            self.assertEqual(opn.index[0], pd.Timestamp('2021-01-04'))
            self.assertEqual(close.iloc[0], 11)

    def test_etf_short_gap_uses_previous_close_and_long_gap_fails(self):
        dates = pd.to_datetime(['2021-01-04', '2021-01-05', '2021-01-06', '2021-01-07'])
        opn = pd.Series([9., 11., 13.], index=dates[[0, 2, 3]])
        close = pd.Series([10., 12., 14.], index=dates[[0, 2, 3]])
        eo, ec, missing = bt._align_etf_prices(opn, close, dates)
        self.assertEqual(list(missing), [dates[1]])
        self.assertEqual(eo.loc[dates[1]], 10.)
        self.assertEqual(ec.loc[dates[1]], 10.)
        long_days = pd.date_range('2021-01-04', '2021-02-01')
        sparse = pd.Series([10., 20.], index=long_days[[0, -1]])
        with self.assertRaisesRegex(ValueError, 'extended period'):
            bt._align_etf_prices(sparse, sparse, long_days)
        with self.assertRaisesRegex(ValueError, 'edge'):
            bt._align_etf_prices(close, close, dates.append(pd.DatetimeIndex(['2021-01-08'])))

    def test_strategy_file_imports_without_other_project_files(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(__file__).resolve().parent / 'residual_momentum_v2_strategy.py'
            shutil.copy(source, temp)
            run = subprocess.run([sys.executable, '-c',
                'from residual_momentum_v2_strategy import ResidualMomentumV2, load_data; print("ok")'],
                cwd=temp, env=dict(os.environ, PYTHONPATH=temp, PYTHONDONTWRITEBYTECODE='1'),
                text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('ok', run.stdout)

    def test_copy_runs_without_repository(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(__file__).resolve().parent
            for name in ('residual_momentum_v2_strategy.py',
                         'residual_momentum_v2_backtest.py', 'run_residual_momentum_v2.py'):
                shutil.copy(root / name, temp)
            run = subprocess.run([sys.executable, str(Path(temp, 'run_residual_momentum_v2.py')), '--help'],
                                 cwd=temp, env=dict(os.environ, PYTHONPATH='', PYTHONDONTWRITEBYTECODE='1'), text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('--data-dir', run.stdout)


    def test_runner_end_to_end_from_copy(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(__file__).resolve().parent
            deploy = Path(temp, 'deploy')
            deploy.mkdir()
            for name in ('residual_momentum_v2_strategy.py',
                         'residual_momentum_v2_backtest.py', 'run_residual_momentum_v2.py'):
                shutil.copy(root / name, deploy)
            stock, etfs = Path(temp, 'stocks'), Path(temp, 'etfs')
            stock.mkdir()
            etfs.mkdir()
            close, volume, high, low, opn = sample_panel()
            for symbol in close.columns:
                pd.DataFrame(dict(datetime=close.index, open=opn[symbol].values,
                    high=high[symbol].values, low=low[symbol].values,
                    close=close[symbol].values, volume=volume[symbol].values)).to_csv(stock / f'{symbol}.csv', index=False)
            pd.DataFrame(dict(timestamp=close.index.strftime('%Y-%m-%dT00:00:00+05:30'),
                              open=np.linspace(20, 25, len(close)), close=np.linspace(20, 25, len(close)), volume=1e7)).to_csv(etfs / 'GOLDBEES.csv', index=False)
            env = dict(os.environ, PYTHONPATH='', PYTHONDONTWRITEBYTECODE='1', RESIDUAL_MOM_ETF_DATA_DIR=str(etfs))
            for sweep in ('none', 'GOLDBEES'):
                run = subprocess.run([sys.executable, str(deploy / 'run_residual_momentum_v2.py'),
                    '--data-dir', str(stock), '--cash-sweep-etf', sweep, '--report-start', '2021-01-01',
                    '--universe-rank-min', '1', '--universe-top-n', '16', '--min-adv', '0'],
                    cwd=temp, env=env, text=True, capture_output=True)
                self.assertEqual(run.returncode, 0, run.stderr)
                self.assertTrue((deploy / 'output' / 'v2_yearly.csv').exists())

            # Default dates select the last block and cap the end to ETF coverage.
            etf = pd.read_csv(etfs / 'GOLDBEES.csv')
            timestamps = pd.to_datetime(etf['timestamp'], utc=True).dt.tz_convert('Asia/Kolkata')
            mask = ~timestamps.between(pd.Timestamp('2020-12-18', tz='Asia/Kolkata'),
                                       pd.Timestamp('2021-01-04', tz='Asia/Kolkata'))
            etf.loc[mask].iloc[:-10].to_csv(etfs / 'GOLDBEES.csv', index=False)
            run = subprocess.run([sys.executable, str(deploy / 'run_residual_momentum_v2.py'),
                '--data-dir', str(stock), '--universe-rank-min', '1', '--universe-top-n', '16',
                '--min-adv', '0'], cwd=temp, env=env, text=True, capture_output=True)
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertIn('Default report_start moved to 2021-01-05', run.stdout)
            self.assertIn('Default data_end capped at', run.stdout)


if __name__ == '__main__':
    unittest.main()

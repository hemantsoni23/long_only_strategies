#!/usr/bin/env python3
"""
run_residual_momentum_v2.py
==============================
Thin orchestrator for ResidualMomentumV2 -- mirrors Old_live_strategies/
run_residual_momentum_strategy.py's structure. Loads data, instantiates the strategy
(universe band + entry-spike filter + gold/silver cash sweep -- see
residual_momentum_v2_strategy.py's docstring), generates positions, runs the backtest, and
prints the full report (metrics at both rf=0% and rf=6.5%, yearly performance, trade log,
trade stats, exit breakdown).

Four-file layout, following the live engine's own three-file convention plus this runner:
  * residual_momentum_v2_strategy.py  -- strategy core (universe, entries, cash-sweep config)
  * residual_momentum_v2_backtest.py  -- backtest engine (delegates to the live engine when
                                         no cash sweep is requested; extends it when one is)
  * run_residual_momentum_v2.py (this file) -- orchestration only
  * README.md -- full rationale and the evidence behind every default below

See README.md for why each default was chosen and what was tested and rejected along the way.
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
_STRAT_DIR = os.path.join(os.path.dirname(_HERE), "Old_live_strategies")
sys.path.insert(0, _STRAT_DIR)

import pandas as pd

from residual_momentum_strategy import load_data, LOCAL_DIR
from residual_momentum_v2_strategy import ResidualMomentumV2
from residual_momentum_v2_backtest import (backtest_event_driven, metrics, print_report,
                                           print_yearly_performance, get_trade_log,
                                           populate_trade_stats, print_exit_breakdown,
                                           ETF_START_DATE)

OUT_DIR = os.path.join(_HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

DEFAULT_REPORT_START = {
    None: "2002-01-01",
    "GOLDBEES": "2007-04-01",
    "SILVERBEES": "2022-03-01",
}


def print_trade_stats(m):
    print("=" * 78)
    print("TRADE STATISTICS")
    print("=" * 78)
    print(f"  Total trades        : {m.get('total_trades_count', 0)}")
    print(f"  Trade win rate      : {m.get('trade_win_rate', float('nan')):.1%}")
    print(f"  Avg / median return : {m.get('avg_trade_return', float('nan')):+.2f}% / "
          f"{m.get('median_trade_return', float('nan')):+.2f}%")
    print(f"  Avg holding days    : {m.get('avg_holding_days', float('nan')):.1f}")
    print(f"  Payoff ratio        : {m.get('payoff_ratio', float('nan')):.2f}")
    print(f"  Profit factor (%)   : {m.get('profit_factor', float('nan')):.2f}")
    print(f"  Profit factor ($)   : {m.get('profit_factor_dollar', float('nan')):.2f}")
    print(f"  Exit mix            : STOP_HIT {m.get('pct_stops', float('nan')):.1f}%  "
          f"REBALANCE {m.get('pct_rebalance', float('nan')):.1f}%  "
          f"END_OF_PERIOD {m.get('pct_end_period', float('nan')):.1f}%")
    print("=" * 78)


def main(load_start="2000-01-01", data_end="2026-09-04", report_start=None,
         universe_rank_min=50, universe_top_n=1000,
         spike_filter=True, spike_lookback=5, spike_quantile=0.80,
         cash_sweep_etf="GOLDBEES", aum=1e5, min_price=20.0, min_adv=1e7):
    if report_start is None:
        report_start = DEFAULT_REPORT_START[cash_sweep_etf]
    if cash_sweep_etf is not None and pd.Timestamp(report_start) < ETF_START_DATE[cash_sweep_etf]:
        raise ValueError(f"report_start={report_start} is before {cash_sweep_etf}'s own data "
                         f"start ({ETF_START_DATE[cash_sweep_etf].date()}); pass a later "
                         f"report_start or cash_sweep_etf=None.")

    print("=" * 78)
    print("ACTIVE CONFIG")
    print("=" * 78)
    print(f"  load_start={load_start}  data_end={data_end}  report_start={report_start}")
    print(f"  universe band: rank {universe_rank_min}-{universe_top_n}   "
          f"({'validated v2 default' if (universe_rank_min, universe_top_n) == (50, 1000) else 'MODIFIED'})")
    print(f"  spike_filter={spike_filter}  lookback={spike_lookback}d  quantile={spike_quantile}   "
          f"({'validated v2 default' if (spike_filter, spike_lookback, spike_quantile) == (True, 5, 0.80) else 'MODIFIED'})")
    print(f"  cash_sweep_etf={cash_sweep_etf}   "
          f"({'validated v2 default' if cash_sweep_etf == 'GOLDBEES' else 'MODIFIED -- see README.md'})")
    print(f"  AUM=Rs{aum:,.0f}")
    print("=" * 78)
    print()

    prices, volumes, highs, lows, opens = load_data(LOCAL_DIR, start=load_start, end=data_end)
    assert prices.index.max() <= pd.Timestamp(data_end), \
        "data leaked past the IS cut -- aborting before touching the strategy"

    strat = ResidualMomentumV2(prices, volumes, highs, lows, opens,
                               universe_rank_min=universe_rank_min, universe_top_n=universe_top_n,
                               spike_filter=spike_filter, spike_lookback=spike_lookback,
                               spike_quantile=spike_quantile, cash_sweep_etf=cash_sweep_etf,
                               min_price=min_price, min_adv=min_adv)
    strat.calculate_factors()
    strat.get_positions(start=report_start)

    if cash_sweep_etf is not None:
        # The trade log (per-trade entry/exit price, PnL%, holding days) reflects only the
        # STOCK-side trades and is identical regardless of how idle cash is invested -- the
        # sweep day-loop doesn't populate it (it only tracks the swept ETF + stock mark-to-
        # market), so populate it first from a plain equity-only pass over the same
        # strat.positions, then run the real sweep backtest for the reported equity curve.
        strat.cash_sweep_etf = None
        backtest_event_driven(strat, aum=aum)
        strat.cash_sweep_etf = cash_sweep_etf

    net, turn = backtest_event_driven(strat, aum=aum)
    label = f"RESIDUAL MOMENTUM V2 ({report_start[:4]}-{data_end[:4]}, AUM=Rs{aum:,.0f})"
    m0 = print_report(net, turn, strat.mkt.reindex(net.index), rf_annual=0.0, label=f"{label}, rf=0%")
    m65 = metrics(net, strat.mkt.reindex(net.index), rf_annual=0.065)
    print(f"  [rf=6.5% check] Sharpe={m65['Sharpe']:.2f}  Sortino={m65['Sortino']:.2f}")
    if cash_sweep_etf is not None:
        print(f"  Avg {cash_sweep_etf} fraction of equity: {strat.cash_sweep_frac.mean():.1%}")
    print()

    yearly = print_yearly_performance(net)
    yearly.to_csv(os.path.join(OUT_DIR, "v2_yearly.csv"))

    trade_log = get_trade_log(strat)
    if not trade_log.empty:
        trade_log.to_csv(os.path.join(OUT_DIR, "v2_trade_log.csv"))
        print(f"(trade log saved to output/v2_trade_log.csv, {len(trade_log)} trades)")
    print()
    m0 = populate_trade_stats(m0, trade_log)
    print_trade_stats(m0)
    print()
    print_exit_breakdown(trade_log)

    return dict(net=net, turnover=turn, metrics=m0, strategy=strat, yearly=yearly, trade_log=trade_log)


def _parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="Run Residual Momentum V2. With no flags, reproduces the validated "
                    "v2 default config (see README.md). Every flag is an opt-in experiment.")
    p.add_argument("--load-start", default="2000-01-01")
    p.add_argument("--data-end", default="2026-09-04")
    p.add_argument("--report-start", default=None,
                   help="defaults depend on --cash-sweep-etf (gold needs 2007-04-01+, "
                        "silver needs 2022-03-01+, plain cash can go back to 2002-01-01)")
    p.add_argument("--universe-rank-min", type=int, default=50)
    p.add_argument("--universe-top-n", type=int, default=1000)
    p.add_argument("--no-spike-filter", action="store_true")
    p.add_argument("--spike-lookback", type=int, default=5)
    p.add_argument("--spike-quantile", type=float, default=0.80)
    p.add_argument("--cash-sweep-etf", default="GOLDBEES", choices=["GOLDBEES", "SILVERBEES", "none"])
    p.add_argument("--aum", type=float, default=1e5)
    p.add_argument("--min-price", type=float, default=20.0)
    p.add_argument("--min-adv", type=float, default=1e7)
    return p.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    cash_sweep_etf = None if args.cash_sweep_etf == "none" else args.cash_sweep_etf
    main(load_start=args.load_start, data_end=args.data_end, report_start=args.report_start,
         universe_rank_min=args.universe_rank_min, universe_top_n=args.universe_top_n,
         spike_filter=not args.no_spike_filter, spike_lookback=args.spike_lookback,
         spike_quantile=args.spike_quantile, cash_sweep_etf=cash_sweep_etf, aum=args.aum,
         min_price=args.min_price, min_adv=args.min_adv)

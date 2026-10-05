#!/usr/bin/env python3
"""
run_residual_momentum_strategy.py
===================================
Thin orchestrator for the Residual Momentum strategy. Loads data, instantiates the strategy,
runs Stage-1-lite data-integrity diagnostics, generates positions, runs the event-driven
backtest, and prints the report (including trade log, trade stats, and exit breakdown).

Three-file layout — no other project file is imported:
  * residual_momentum_strategy.py  — strategy core (load_data, factors, universe, positions)
  * residual_momentum_backtest.py  — backtest engine + metrics
  * run_residual_momentum_strategy.py (this file) — orchestration only

See STRATEGY_OVERVIEW.md for the full strategy writeup and the rationale behind each default.
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import numpy as np
import pandas as pd

from residual_momentum_strategy import (load_data, ResidualMomentumStrategy, LOCAL_DIR,
                                        build_universe_card,
                                        print_universe_card, spot_check_returns, print_spot_check)
from residual_momentum_backtest import (backtest_event_driven, print_report,
                                        get_trade_log, populate_trade_stats, print_exit_breakdown,
                                        print_yearly_performance, plot_performance,
                                        print_turnover_attribution)

OUT_DIR = os.path.join(_HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)


def diagnose_sizing_gaps(strat, start):
    """Reads strat.held_by_t / strat.positions -- set by strat.get_positions(start), which
    MUST already have been called with this same `start` -- to measure, for THIS run:
      (1) how many rebalance dates hit the `if iv.empty: continue` branch in _size_weights
          -> that month's target weights go to flat zero for everyone.
      (2) how many (date, targeted-name) pairs have NaN/zero trailing ADV, the condition
          under which the backtest's order-size cap silently collapses to ~0 for that name.

    This now reuses the exact selection/sizing that actually ran (rather than a second,
    independently-recomputed pass), so it's a true read of what happened -- not a replay that
    could silently diverge from it -- and it doesn't re-run the heaviest part of the pipeline
    a second time purely for instrumentation.
    """
    if strat.positions is None or strat.held_by_t is None:
        raise RuntimeError("diagnose_sizing_gaps: call strat.get_positions(start) first")

    held_by_t, rebs, WT = strat.held_by_t, strat.rebalance_dates, strat.positions

    empty_iv_months = []
    for t, names in held_by_t.items():
        if not names:
            continue
        iv = (1.0 / strat.ivol.loc[t, names]).replace([np.inf, -np.inf], np.nan).dropna()
        if iv.empty:
            empty_iv_months.append(str(pd.Timestamp(t).date()))

    adv = strat.tv.rolling(21, min_periods=10).median()
    nan_adv_events, nan_adv_months = 0, set()
    for t in WT.index:
        targeted = WT.loc[t][WT.loc[t] > 0].index
        if len(targeted) == 0:
            continue
        a = adv.loc[t, targeted]
        bad = a.isna() | (a <= 0)
        if bad.any():
            nan_adv_events += int(bad.sum())
            nan_adv_months.add(str(pd.Timestamp(t).date()))

    return dict(
        n_rebalance_months=len(rebs),
        empty_iv_months=empty_iv_months,
        n_empty_iv_months=len(empty_iv_months),
        nan_or_zero_adv_events=nan_adv_events,
        nan_or_zero_adv_months=sorted(nan_adv_months),
    )


def print_sizing_gaps(gaps):
    print("=" * 78)
    print("SIZING-GAP INSTRUMENTATION (non-invasive replay of strat._select_holdings/_size_weights)")
    print("=" * 78)
    print(f"Rebalance months in report window            : {gaps['n_rebalance_months']}")
    print(f"Months hitting empty-inverse-vol branch        : {gaps['n_empty_iv_months']}"
          + (f"  {gaps['empty_iv_months']}" if gaps['n_empty_iv_months'] else ""))
    print(f"(date,name) pairs with NaN/zero ADV, targeted  : {gaps['nan_or_zero_adv_events']}"
          + (f"  across {len(gaps['nan_or_zero_adv_months'])} months" if gaps['nan_or_zero_adv_events'] else ""))
    print("=" * 78)


def print_trade_stats(m):
    print("=" * 78)
    print("TRADE STATISTICS")
    print("=" * 78)
    print(f"  Total trades        : {m.get('total_trades_count', 0)}")
    print(f"  Trade win rate      : {m.get('trade_win_rate', float('nan')):.1%}")
    print(f"  Avg / median return : {m.get('avg_trade_return', float('nan')):+.2f}% / "
          f"{m.get('median_trade_return', float('nan')):+.2f}%")
    print(f"  Avg holding days    : {m.get('avg_holding_days', float('nan')):.1f}")
    print(f"  Best / worst trade  : {m.get('best_trade', float('nan')):+.2f}% / "
          f"{m.get('worst_trade', float('nan')):+.2f}%")
    print(f"  Avg MAE / MFE       : {m.get('avg_mae', float('nan')):+.2f}% / "
          f"{m.get('avg_mfe', float('nan')):+.2f}%")
    print(f"  Avg win / loss      : {m.get('avg_win_pct', float('nan')):+.2f}% / "
          f"-{m.get('avg_loss_pct', float('nan')):.2f}%")
    print(f"  Payoff ratio        : {m.get('payoff_ratio', float('nan')):.2f}")
    print(f"  Profit factor (%)   : {m.get('profit_factor', float('nan')):.2f}")
    print(f"  Profit factor ($)   : {m.get('profit_factor_dollar', float('nan')):.2f}")
    print(f"  Exit mix            : STOP_HIT {m.get('pct_stops', float('nan')):.1f}%  "
          f"REBALANCE {m.get('pct_rebalance', float('nan')):.1f}%  "
          f"END_OF_PERIOD {m.get('pct_end_period', float('nan')):.1f}%")
    print("=" * 78)


def main(load_start="2001-01-01", data_end="2013-12-31", report_start="2002-01-01",
         universe_top_n=500, min_price=20.0, min_adv=1e7, plot=True,
         # All default to the validated config (see STRATEGY_OVERVIEW.md); override any to
         # A/B test without touching strategy code.
         rebalance_freq_months=1,
         z9_weight=1.0, high52_weight=1.0, illiq_weight=0.0, lowpx_weight=0.0,
         beta_shrink=0.0):
    print("=" * 78)
    print("ACTIVE CONFIG")
    print("=" * 78)
    print(f"  load_start={load_start}  data_end={data_end}  report_start={report_start}")
    print(f"  universe_top_n={universe_top_n}  min_price={min_price}  min_adv={min_adv:,.0f}   "
          f"({'validated default tradability floor' if (min_price, min_adv) == (20.0, 1e7) else 'MODIFIED tradability floor'})")
    print(f"  rebalance_freq_months={rebalance_freq_months}   "
          f"(1=monthly/validated default; this run is {'MONTHLY (default)' if rebalance_freq_months == 1 else f'every {rebalance_freq_months} months'})")
    print(f"  z9_weight={z9_weight}  high52_weight={high52_weight}  "
          f"illiq_weight={illiq_weight}  lowpx_weight={lowpx_weight}  "
          f"({'validated default composite' if (z9_weight, high52_weight, illiq_weight, lowpx_weight) == (1.0, 1.0, 0.0, 0.0) else 'MODIFIED composite'})")
    print(f"  beta_shrink={beta_shrink}   "
          f"({'raw rolling beta (default)' if beta_shrink == 0.0 else 'SHRUNK beta'})")
    print("=" * 78)
    print()
    print(f"Local-CSV load window: {load_start} .. {data_end}  (report window starts {report_start})")
    print()

    prices, volumes, highs, lows, opens = load_data(LOCAL_DIR, start=load_start, end=data_end)
    assert prices.index.max() <= pd.Timestamp(data_end), \
        "data leaked past the IS cut — aborting before touching the strategy"

    strat = ResidualMomentumStrategy(prices, volumes, highs, lows, opens,
                                     universe_top_n=universe_top_n,
                                     min_price=min_price, min_adv=min_adv,
                                     rebalance_freq_months=rebalance_freq_months,
                                     z9_weight=z9_weight, high52_weight=high52_weight,
                                     illiq_weight=illiq_weight, lowpx_weight=lowpx_weight,
                                     beta_shrink=beta_shrink)
    strat.calculate_factors()

    card = build_universe_card({"close": strat.close, "univ": strat.univ},
                                top_n=universe_top_n, start=report_start)
    print_universe_card(card)
    print()

    summary, outliers = spot_check_returns({"close": strat.close})
    print_spot_check(summary, outliers)
    outliers.to_csv(os.path.join(OUT_DIR, "spot_check_outliers_is.csv"), index=False)
    print(f"\n(outlier table saved to output/spot_check_outliers_is.csv)")
    print()

    strat.get_positions(start=report_start)

    gaps = diagnose_sizing_gaps(strat, report_start)
    print_sizing_gaps(gaps)
    print()

    net, turn = backtest_event_driven(strat)
    m = print_report(net, turn, strat.mkt, label=f"IS-LOCAL ({report_start[:4]}-{data_end[:4]})")
    print_turnover_attribution(strat)
    print()

    assert all(pd.notna(v) and abs(v) != float("inf") for v in
               (m['CAGR'], m['Vol'], m['Sharpe'], m['MaxDD'])), \
        "NaN/Inf in core metrics — investigate before trusting"
    print("Sanity: no NaN/Inf in core metrics. Data never extended past", data_end,
          "- confirmed by assert above load.")
    print()

    trade_log = get_trade_log(strat)
    if not trade_log.empty:
        trade_log.to_csv(os.path.join(OUT_DIR, "residual_momentum_trade_log.csv"))
        print(f"(trade log saved to output/residual_momentum_trade_log.csv, {len(trade_log)} trades)")
    print()
    m = populate_trade_stats(m, trade_log)
    print_trade_stats(m)
    print()
    print_exit_breakdown(trade_log)
    print()

    yearly = print_yearly_performance(net)

    plot_files = None
    if plot:
        plot_files = plot_performance(net, strat.mkt, strat=strat,
                                      filename=os.path.join(OUT_DIR, "residual_momentum_performance.png"))

    return dict(net=net, turnover=turn, metrics=m, strategy=strat, yearly=yearly,
                plot_files=plot_files, trade_log=trade_log)


def _parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="Run the Residual Momentum strategy. With no flags, reproduces the "
                    "validated default config (see STRATEGY_OVERVIEW.md). Every flag below "
                    "is an opt-in experiment -- omit a flag to keep its validated default.")
    p.add_argument("--load-start", default="2000-01-01")
    p.add_argument("--data-end", default="2025-12-31")
    p.add_argument("--report-start", default="2002-01-01")
    p.add_argument("--universe-top-n", type=int, default=500)
    p.add_argument("--min-price", type=float, default=20.0,
                    help="live-tradability price floor, applied before the top-N turnover "
                         "rank (validated default 20); pass 0 to disable")
    p.add_argument("--min-adv", type=float, default=1e7,
                    help="live-tradability trailing-63d median $-volume floor (validated "
                         "default 1e7 = Rs 1 crore/day); pass 0 to disable")
    p.add_argument("--no-plot", action="store_true", help="skip saving performance plots")
    p.add_argument("--rebalance-freq-months", type=int, default=1,
                    help="1=monthly (validated default), 3=quarterly, 6=semi-annual, ...")
    p.add_argument("--z9-weight", type=float, default=1.0)
    p.add_argument("--high52-weight", type=float, default=1.0)
    p.add_argument("--illiq-weight", type=float, default=0.0,
                    help="validated default is 0.0 (see STRATEGY_OVERVIEW.md); pass 0.5 to "
                         "reproduce the old, not-recommended composite")
    p.add_argument("--lowpx-weight", type=float, default=0.0,
                    help="validated default is 0.0 -- see --illiq-weight")
    p.add_argument("--beta-shrink", type=float, default=0.0,
                    help="0.0=raw rolling beta (validated default); try 0.3-0.5 to shrink toward 1.0")
    return p.parse_args()


if __name__ == "__main__":
    print("=" * 78)
    print(f"RAW sys.argv RECEIVED: {sys.argv}")
    print("=" * 78)
    args = _parse_args()
    print(f"PARSED FLAGS: rebalance_freq_months={args.rebalance_freq_months}  "
          f"z9_weight={args.z9_weight}  high52_weight={args.high52_weight}  "
          f"illiq_weight={args.illiq_weight}  lowpx_weight={args.lowpx_weight}  "
          f"beta_shrink={args.beta_shrink}  min_price={args.min_price}  min_adv={args.min_adv:,.0f}")
    print("(if the two lines above don't show the values you typed, your flags never")
    print(" reached this process -- check how you're invoking the script, not this file)")
    print()
    main(load_start=args.load_start, data_end=args.data_end, report_start=args.report_start,
         universe_top_n=args.universe_top_n, min_price=args.min_price, min_adv=args.min_adv,
         plot=not args.no_plot,
         rebalance_freq_months=args.rebalance_freq_months,
         z9_weight=args.z9_weight, high52_weight=args.high52_weight,
         illiq_weight=args.illiq_weight, lowpx_weight=args.lowpx_weight,
         beta_shrink=args.beta_shrink)
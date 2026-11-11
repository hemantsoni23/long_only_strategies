#!/usr/bin/env python3
"""Run the standalone v2 research backtest.

This script generates historical target weights and simulated returns. It does
not connect to a broker, submit orders, or manage live positions.
"""
import os

_HERE = os.path.dirname(os.path.abspath(__file__))
import pandas as pd

if __package__:
    from .residual_momentum_v2_strategy import load_data, LOCAL_DIR, ResidualMomentumV2
    from .residual_momentum_v2_backtest import (backtest_event_driven, metrics, print_report,
        print_yearly_performance, get_trade_log, populate_trade_stats, print_exit_breakdown,
        ETF_START_DATE, load_etf_prices)
else:
    from residual_momentum_v2_strategy import load_data, LOCAL_DIR, ResidualMomentumV2
    from residual_momentum_v2_backtest import (backtest_event_driven, metrics, print_report,
        print_yearly_performance, get_trade_log, populate_trade_stats, print_exit_breakdown,
        ETF_START_DATE, load_etf_prices)

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


def main(load_start="2000-01-01", data_end=None, report_start=None, data_dir=LOCAL_DIR,
         universe_rank_min=50, universe_top_n=1000,
         spike_filter=True, spike_lookback=5, spike_quantile=0.80,
         cash_sweep_etf="GOLDBEES", aum=1e5, min_price=20.0, min_adv=1e7):
    default_start = report_start is None
    if default_start:
        report_start = DEFAULT_REPORT_START[cash_sweep_etf]
    if cash_sweep_etf is not None:
        _, etf_close = load_etf_prices(cash_sweep_etf)
        if data_end is None:
            data_end = etf_close.index.max().strftime("%Y-%m-%d")
            print(f"[ETF data] Default data_end capped at {data_end}, the last {cash_sweep_etf} bar.")
        elif pd.Timestamp(data_end) > etf_close.index.max():
            raise ValueError(f"data_end={data_end} exceeds {cash_sweep_etf} coverage ending "
                             f"{etf_close.index.max().date()}; update the ETF CSV or choose an earlier end")
        available = etf_close.loc[:pd.Timestamp(data_end)]
        if available.empty:
            raise ValueError(f"No {cash_sweep_etf} data on or before {data_end}")
        if default_start:
            dates = available.index
            gaps = dates.to_series().diff() > pd.Timedelta(days=7)
            block_start = dates[gaps.to_numpy()][-1] if gaps.any() else dates[0]
            selected = max(pd.Timestamp(report_start), block_start)
            if selected > pd.Timestamp(report_start):
                print(f"[ETF data] Default report_start moved to {selected.date()} to avoid an "
                      f"extended gap in {cash_sweep_etf} history.")
            report_start = selected.strftime("%Y-%m-%d")
        if pd.Timestamp(report_start) < etf_close.index.min():
            raise ValueError(f"report_start={report_start} is before {cash_sweep_etf} data starts "
                             f"({etf_close.index.min().date()})")
    if data_end is not None and pd.Timestamp(report_start) >= pd.Timestamp(data_end):
        raise ValueError("report_start must be before data_end")

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

    prices, volumes, highs, lows, opens = load_data(data_dir, start=load_start, end=data_end)
    if data_end is not None and prices.index.max() > pd.Timestamp(data_end):
        raise ValueError("data contains dates after data_end")

    strat = ResidualMomentumV2(prices, volumes, highs, lows, opens,
                               universe_rank_min=universe_rank_min, universe_top_n=universe_top_n,
                               spike_filter=spike_filter, spike_lookback=spike_lookback,
                               spike_quantile=spike_quantile, cash_sweep_etf=cash_sweep_etf,
                               min_price=min_price, min_adv=min_adv)
    strat.calculate_factors()
    strat.get_positions(start=report_start)


    cash_net = None
    if cash_sweep_etf is not None:
        # The comparison uses the same targets/window and explicitly zero cash interest.
        strat.cash_sweep_etf = None
        try:
            cash_net, _ = backtest_event_driven(strat, aum=aum, rf=0.0)
        finally:
            strat.cash_sweep_etf = cash_sweep_etf
    net, turn = backtest_event_driven(strat, aum=aum, rf=0.0)
    label = f"RESIDUAL MOMENTUM V2 ({report_start[:4]}-{prices.index.max().year}, AUM=Rs{aum:,.0f})"
    m0 = print_report(net, turn, strat.mkt.reindex(net.index), rf_annual=0.0, label=f"{label}, rf=0%")
    if cash_sweep_etf is not None:
        print(f"  Avg {cash_sweep_etf} fraction of equity: {strat.cash_sweep_frac.mean():.1%}")
        cash_metrics = metrics(cash_net, strat.mkt.reindex(cash_net.index), rf_annual=0.0)
        print(f"  Same-period cash comparison (cash interest 0%): CAGR={cash_metrics['CAGR']:+.2%} "
              f"Sharpe={cash_metrics['Sharpe']:.2f} MaxDD={cash_metrics['MaxDD']:.2%}")
        costs = strat.cash_sweep_costs
        print(f"  ETF costs: Rs{costs['etf']:,.2f} across {costs['etf_buy_orders']} buys "
              f"and {costs['etf_sell_orders']} sells")
        print(f"  Stock costs: Rs{costs['stock']:,.2f}; stock orders skipped for missing prices: "
              f"{costs['skipped_stock_fills']}")
    print()

    yearly = print_yearly_performance(net)
    yearly.to_csv(os.path.join(OUT_DIR, "v2_yearly.csv"))

    if cash_sweep_etf is not None:
        print("Trade statistics use sweep-portfolio stock sale fills; partial sales are separate records.")
    trade_log = get_trade_log(strat)
    if not trade_log.empty:
        trade_log.to_csv(os.path.join(OUT_DIR, "v2_trade_log.csv"))
        print(f"(trade log saved to output/v2_trade_log.csv, {len(trade_log)} trades)")
    print()
    m0 = populate_trade_stats(m0, trade_log)
    print_trade_stats(m0)
    print()
    print_exit_breakdown(trade_log)

    return dict(net=net, turnover=turn, metrics=m0, strategy=strat, yearly=yearly, trade_log=trade_log, cash_net=cash_net)


def _parse_args():
    import argparse
    p = argparse.ArgumentParser(
        description="Run the standalone Residual Momentum V2 backtest (see README.md).")
    p.add_argument("--load-start", default="2000-01-01")
    p.add_argument("--data-end", default=None, help="last data date (default: latest available, capped by ETF coverage for sweep)")
    p.add_argument("--data-dir", default=LOCAL_DIR, help="directory of stock OHLCV CSVs")
    p.add_argument("--report-start", default=None,
                   help="first rebalance date (default: latest continuous ETF history for sweep)")
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
         data_dir=args.data_dir,
         universe_rank_min=args.universe_rank_min, universe_top_n=args.universe_top_n,
         spike_filter=not args.no_spike_filter, spike_lookback=args.spike_lookback,
         spike_quantile=args.spike_quantile, cash_sweep_etf=cash_sweep_etf, aum=args.aum,
         min_price=args.min_price, min_adv=args.min_adv)

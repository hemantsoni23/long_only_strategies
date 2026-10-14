"""
residual_capital_v9.py
=========================
Characterizes idle/unallocated capital in v9's IS backtest (2003-2012):
residual(t) = max(0, 1 - positions_df.sum(axis=1)) on every trading day.
Pure diagnostic, no strategy changes -- this is the direct analogue of
run_csm_absolute_etf_overlay.py's residual(t) formula, computed against
v9's own positions_df (the "executed_weights" equivalent in this codebase --
already reflects regime leverage/corr-scale/vol-scale, same as csm_absolute's
executed_weights does).
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v9 as S


def main():
    print("Loading OHLCV data + building factors...")
    prices, volumes, highs, lows, opens = S.load_data(S.DATA_FOLDER)
    members = S.build_sector_membership(prices, S.INSTRUMENTS_CSV)
    universe_mask = S.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = S.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = S.build_sector_rank(prices, members, universe_mask,
                                                          sector_price, daily_ret)
    sma_slow, trend_ok, persistence, stock_quality = S.build_stock_factors(prices)
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, stock_quality=stock_quality,
    )

    equity_w_sum = positions_df.sum(axis=1)
    residual = (1.0 - equity_w_sum).clip(lower=0.0)

    # Also pull the T-1 regime label (bull/bear/panic) each day was actually
    # trading under, for the breakdown -- reconstructed the same way
    # compute_regime() derives leverage internally.
    bench = sector_price.mean(axis=1, skipna=True)
    bench_sma200 = bench.rolling(S.BENCH_SMA200_PERIOD, min_periods=150).mean()
    is_bull_series = (bench.shift(1) > bench_sma200.shift(1)).fillna(True)
    regime = pd.Series("bull", index=positions_df.index)
    regime[~is_bull_series.reindex(positions_df.index).fillna(True)] = "bear"
    regime[is_panic.reindex(positions_df.index).fillna(False)] = "panic"

    print(f"\n{'='*80}\nRESIDUAL (UNALLOCATED) CAPITAL -- v9, IS 2003-2012\n{'='*80}")
    n_days = len(residual)
    print(f"  Total trading days in backtest: {n_days}")
    print(f"  Avg equity allocation: {equity_w_sum.mean()*100:.1f}%   "
          f"Avg residual (idle): {residual.mean()*100:.1f}%")
    print()
    for label, cond in [
        ("Fully allocated (residual < 1%)", residual < 0.01),
        ("Partially idle (1-25% residual)", (residual >= 0.01) & (residual < 0.25)),
        ("Materially idle (25-50% residual)", (residual >= 0.25) & (residual < 0.50)),
        ("Mostly/fully idle (>=50% residual)", residual >= 0.50),
        ("Completely empty (residual > 99%)", residual > 0.99),
    ]:
        n = cond.sum()
        print(f"  {label:38s}: {n:5d} days ({n/n_days*100:5.1f}%)")

    print(f"\n  'Capital-days' of idle capital (sum of residual across all days, "
          f"in units of 1 full day fully idle): {residual.sum():.0f} "
          f"(~{residual.sum()/252:.1f} portfolio-years of fully-idle-equivalent capital "
          f"over the {n_days/252:.1f}-year backtest)")

    print(f"\n{'='*80}\nRESIDUAL BY REGIME\n{'='*80}")
    reg_summary = pd.DataFrame({"residual": residual, "regime": regime.reindex(residual.index)})
    print(reg_summary.groupby("regime")["residual"].agg(["mean", "count"]).rename(
        columns={"mean": "avg_residual", "count": "n_days"}).round(3).to_string())

    print(f"\n{'='*80}\nRESIDUAL BY YEAR\n{'='*80}")
    yearly = residual.groupby(residual.index.year).agg(["mean", "max"])
    yearly.columns = ["avg_residual", "max_residual"]
    print((yearly * 100).round(1).to_string())

    out = os.path.join(os.path.dirname(__file__), "residual_capital_v9.csv")
    residual.to_frame("residual").assign(regime=regime).to_csv(out)
    print(f"\nSaved daily residual series to {out}")


if __name__ == "__main__":
    main()

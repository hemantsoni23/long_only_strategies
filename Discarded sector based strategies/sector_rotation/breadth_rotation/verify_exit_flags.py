"""
verify_exit_flags.py
=======================
Sanity check for the newly-added per-exit-mechanism flags: run each one OFF
individually and confirm the corresponding exit reason actually disappears
from the trade log (not just that the backtest runs without error).
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v6 as S

CELLS = [
    ("stop_loss OFF",           dict(use_stop_loss=False),           "STOP_LOSS"),
    ("crash_guard OFF",         dict(use_crash_guard=False),         "CRASH_GUARD"),
    ("stock_rank_decline OFF",  dict(use_stock_rank_decline=False),  "STOCK_RANK_DECLINE"),
    ("sector_rank_decline OFF", dict(use_sector_rank_decline=False), "SECTOR_RANK_DECLINE"),
    ("chandelier OFF",          dict(use_chandelier=False),          "ATR_STOP"),
]


def main():
    print("Loading OHLCV data + building factors...")
    prices, volumes, highs, lows, opens = S.load_data(S.DATA_FOLDER)
    members = S.build_sector_membership(prices, S.INSTRUMENTS_CSV)
    universe_mask = S.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = S.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = S.build_sector_rank(prices, members, universe_mask,
                                                          sector_price, daily_ret)
    sma_slow, trend_ok, persistence = S.build_stock_factors(prices)
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    common = dict(prices=prices, opens=opens, sector_rank=sector_rank, members=members,
                  universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
                  persistence=persistence, bench_ok=bench_ok, atr=atr, is_panic=is_panic,
                  leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
                  falling_knife=falling_knife)

    print(f"\n{'='*80}\nBaseline (all ON) exit counts:\n{'='*80}")
    positions_df, trade_log_df = S.run_backtest(**common)
    print(trade_log_df["Exit_Reason"].value_counts().to_string())

    for label, kwargs, disappearing_reason in CELLS:
        positions_df, trade_log_df = S.run_backtest(**common, **kwargs)
        counts = trade_log_df["Exit_Reason"].value_counts()
        n = counts.get(disappearing_reason, 0)
        status = "PASS -- 0 occurrences" if n == 0 else f"FAIL -- still {n} occurrences"
        print(f"\n{label}: {disappearing_reason} count = {n}  [{status}]")
        print(counts.to_string())


if __name__ == "__main__":
    main()

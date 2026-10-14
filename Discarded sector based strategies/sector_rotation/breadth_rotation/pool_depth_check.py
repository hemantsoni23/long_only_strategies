"""
pool_depth_check.py
=====================
The IC diagnostic said Industry_clean should be BETTER (stronger IC, much
lower overlap with the baseline), but the full backtest came out worse than
Sector_clean (CAGR 25.4%->12.4%, Sharpe 1.42->0.79, MaxDD -49%->-55%,
SECTOR_RANK_DECLINE exits 240->372). IC only measures whether the SECTOR-level
ranking predicts the SECTOR index's forward return -- it says nothing about
whether there are enough good STOCK candidates inside each top-ranked
industry bucket, or whether the finer buckets rotate more violently.

This checks two concrete hypotheses at every weekly rebalance in the IS
window, for both granularities side by side:
  1. Candidate pool depth: how many (universe-eligible AND trend_ok) stocks
     are actually available inside each top-N selected sector, BEFORE the
     top-STOCKS_PER_SECTOR cut? Thin pools = weak stock selection even if
     the sector-level signal is good.
  2. Sector churn: how often does the top-N sector SET change from one
     rebalance to the next? Finer buckets could mean noisier per-bucket
     breadth stats and more whipsaw.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

warnings.filterwarnings("ignore")

import sector_breadth_strategy_v1 as SEC
import industry_breadth_strategy_v1 as IND

IS_START = pd.Timestamp("2003-01-01")
IS_END = pd.Timestamp("2012-12-31")
REBALANCE_EVERY = 5


def analyze(mod, label):
    prices, volumes, highs, lows, opens = mod.load_data(mod.DATA_FOLDER)
    members = mod.build_sector_membership(prices, mod.INSTRUMENTS_CSV)
    universe_mask = mod.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = mod.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = mod.build_sector_rank(prices, members, universe_mask,
                                                            sector_price, daily_ret)
    sma_slow, trend_ok, persistence = mod.build_stock_factors(prices)

    dates = prices.index
    start_i = dates.searchsorted(IS_START)
    end_i = dates.searchsorted(IS_END, side="right")

    pool_sizes = []
    zero_pool_count = 0
    n_top_sector_checks = 0
    prev_top_set = None
    churn_events = []

    for i in range(start_i, end_i):
        if (i - start_i) % REBALANCE_EVERY != 0:
            continue
        idx = i - 1
        row = sector_rank.iloc[idx].dropna().sort_values(ascending=False)
        top_sectors = list(row.index[:mod.N_SECTORS])

        if prev_top_set is not None:
            shared = len(set(top_sectors) & prev_top_set)
            churn_events.append(mod.N_SECTORS - shared)   # how many slots changed
        prev_top_set = set(top_sectors)

        for sector in top_sectors:
            if sector not in members:
                continue
            pool = mod.rank_sector_stocks(idx, sector, members, persistence, universe_mask, trend_ok)
            pool_sizes.append(len(pool))
            n_top_sector_checks += 1
            if len(pool) == 0:
                zero_pool_count += 1

    pool_sizes = np.array(pool_sizes)
    churn_events = np.array(churn_events)

    print(f"\n{'='*80}\n{label}\n{'='*80}")
    print(f"  Total sectors qualifying overall: {len(members)}")
    print(f"  Top-N selected per rebalance: {mod.N_SECTORS}   Stocks needed per sector: {mod.STOCKS_PER_SECTOR}")
    print(f"  Candidate pool depth (eligible + trend_ok stocks) inside each top-N sector:")
    print(f"    mean={pool_sizes.mean():.2f}  median={np.median(pool_sizes):.1f}  "
          f"min={pool_sizes.min()}  p10={np.percentile(pool_sizes,10):.1f}")
    print(f"    % of top-sector-slots with ZERO candidates: {zero_pool_count/n_top_sector_checks*100:.1f}%  "
          f"({zero_pool_count}/{n_top_sector_checks})")
    print(f"    % of top-sector-slots with < {mod.STOCKS_PER_SECTOR} candidates "
          f"(can't fill both slots): {(pool_sizes < mod.STOCKS_PER_SECTOR).mean()*100:.1f}%")
    print(f"  Sector-set churn per rebalance (slots changed out of {mod.N_SECTORS}):")
    print(f"    mean={churn_events.mean():.2f}  "
          f"({churn_events.mean()/mod.N_SECTORS*100:.1f}% of slots turn over per week on average)")
    return pool_sizes, churn_events


def main():
    pool_sec, churn_sec = analyze(SEC, "SECTOR_CLEAN (11 buckets)")
    pool_ind, churn_ind = analyze(IND, "INDUSTRY_CLEAN (~92 buckets)")


if __name__ == "__main__":
    main()

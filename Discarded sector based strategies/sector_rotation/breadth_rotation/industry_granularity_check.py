"""
industry_granularity_check.py
================================
Checks Industry_clean coverage against the ACTUAL tradeable universe
(universe_mask: top-1000 63d $vol, min price Rs10, circuit <=5/63d) instead
of the Cap-label proxy used in the first pass. Answers two questions, per
month-end across the IS window (2003-2012):

  1. What % of the ELIGIBLE (tradeable) universe has an Industry_clean tag?
  2. How many Industry_clean buckets clear >=8 / >=5 ELIGIBLE+TAGGED stocks
     on a typical day -- i.e. how many groups could the breadth factor
     actually rotate among if we required real-time universe eligibility?

Same numbers computed for Sector_clean as a baseline for comparison.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "HR_breakout"))
from hr_breakout_v2 import load_data  # noqa: E402

DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
INSTRUMENTS_CSV = os.path.join(REPO_ROOT, "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"

IS_START = pd.Timestamp("2003-01-01")
IS_END   = pd.Timestamp("2012-12-31")

UNIVERSE_TOP_N   = 1000
MIN_PRICE        = 10.0
MAX_CIRCUIT_DAYS = 5
MIN_STOCKS_BUCKET_A = 8
MIN_STOCKS_BUCKET_B = 5


def build_universe_mask(prices, volumes, highs, lows):
    prev_close = prices.shift(1)
    price_ok = prev_close >= MIN_PRICE
    dvol = (prices * volumes).rolling(63, min_periods=21).mean().shift(1)
    dvol_rank = dvol.rank(axis=1, ascending=False, method="min")
    dvol_ok = dvol_rank <= UNIVERSE_TOP_N
    if not highs.empty and not lows.empty:
        circuit_count = (highs == lows).rolling(63, min_periods=1).sum().shift(1)
        circuit_ok = circuit_count <= MAX_CIRCUIT_DAYS
    else:
        circuit_ok = pd.DataFrame(True, index=prices.index, columns=prices.columns)
    return (price_ok & dvol_ok & circuit_ok).fillna(False)


def analyze(universe_mask, ticker_tag_map, label, min_a=MIN_STOCKS_BUCKET_A, min_b=MIN_STOCKS_BUCKET_B):
    month_ends = universe_mask.resample("ME").last().index
    month_ends = month_ends[(month_ends >= IS_START) & (month_ends <= IS_END)]

    coverage_pcts, n_buckets_a, n_buckets_b, eligible_counts, tagged_counts = [], [], [], [], []

    for date in month_ends:
        if date not in universe_mask.index:
            # nearest prior trading day
            idx = universe_mask.index[universe_mask.index <= date]
            if len(idx) == 0:
                continue
            date = idx[-1]
        row = universe_mask.loc[date]
        eligible = set(row[row].index)
        if not eligible:
            continue
        eligible_counts.append(len(eligible))

        tagged = {t: ticker_tag_map[t] for t in eligible if t in ticker_tag_map and pd.notna(ticker_tag_map[t])}
        tagged_counts.append(len(tagged))
        coverage_pcts.append(len(tagged) / len(eligible) * 100)

        bucket_sizes = pd.Series(list(tagged.values())).value_counts()
        n_buckets_a.append((bucket_sizes >= min_a).sum())
        n_buckets_b.append((bucket_sizes >= min_b).sum())

    print(f"\n{'='*80}\n{label}\n{'='*80}")
    print(f"  Month-ends analyzed: {len(eligible_counts)}")
    print(f"  Avg eligible (tradeable) universe size: {np.mean(eligible_counts):.0f}")
    print(f"  Avg tagged among eligible: {np.mean(tagged_counts):.0f}  "
          f"({np.mean(coverage_pcts):.1f}% coverage, min={np.min(coverage_pcts):.1f}%, max={np.max(coverage_pcts):.1f}%)")
    print(f"  Avg buckets with >={min_a} eligible+tagged stocks: {np.mean(n_buckets_a):.1f}  "
          f"(min={np.min(n_buckets_a)}, max={np.max(n_buckets_a)})")
    print(f"  Avg buckets with >={min_b} eligible+tagged stocks: {np.mean(n_buckets_b):.1f}  "
          f"(min={np.min(n_buckets_b)}, max={np.max(n_buckets_b)})")
    return dict(coverage_pcts=coverage_pcts, n_buckets_a=n_buckets_a, n_buckets_b=n_buckets_b)


def main():
    print("Loading OHLCV data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)
    universe_mask = build_universe_mask(prices, volumes, highs, lows)

    inst = pd.read_csv(INSTRUMENTS_CSV)
    sector_clean_map = dict(zip(inst[SYMBOL_COL], inst["Sector_clean"]))
    industry_clean_map = dict(zip(inst[SYMBOL_COL], inst["Industry_clean"]))

    analyze(universe_mask, sector_clean_map, "SECTOR_CLEAN  (baseline, 11 buckets)")
    analyze(universe_mask, industry_clean_map, "INDUSTRY_CLEAN  (202 buckets)")


if __name__ == "__main__":
    main()

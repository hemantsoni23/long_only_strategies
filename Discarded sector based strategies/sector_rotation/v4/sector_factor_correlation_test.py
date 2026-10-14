"""
sector_factor_correlation_test.py
====================================
Follow-up to sector_factor_library_ic_test.py: checks whether the
strongest factors from the library are actually independent sources of
information, or just re-detecting each other (e.g. Dispersion_21 rising
mechanically alongside momentum in a trending sector).

Two checks:
  1. Pairwise average cross-sectional rank correlation among the top
     candidates -- high correlation means two factors rank sectors
     almost the same way on any given day, i.e. redundant.
  2. Equal-weight percentile-rank composites of promising pairs/triples,
     run through the SAME evaluate_signal IC harness as the library test.
     If a composite's ICIR beats its best individual component, the
     combination is adding real information, not just averaging noise.

Candidates carried forward from the library results: Mom_126 (best pure
momentum), Mom_Slope_21 (flagged as a likely smoothed re-statement of
momentum, not true acceleration), Avg_Constituent_RS_126 and
Dispersion_21 (the two most structurally different strong performers),
plus Breadth_SMA200 and UpDownVol_Ratio_20 as secondary reference points.

Run: python sector_rotation/sector_factor_correlation_test.py
Outputs (written next to this script):
    sector_factor_correlation_matrix.csv
    sector_factor_correlation_matrix.png
    sector_factor_composite_results.csv
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hr_breakout_v2 import load_data
from sector_factor_library_ic_test import (
    DATA_FOLDER, INSTRUMENTS_CSV, HORIZONS,
    build_sector_membership, build_masked_daily_returns, build_sector_index,
    build_bucket_weighted_index, build_momentum_factors, build_acceleration_factors,
    build_breadth_factors, build_participation_factors, build_capital_flow_factors,
    evaluate_signal,
)

SCRIPT_DIR = os.path.dirname(__file__)

CANDIDATES = [
    "Mom_126", "Mom_Slope_21", "Avg_Constituent_RS_126",
    "Dispersion_21", "Breadth_SMA200", "UpDownVol_Ratio_20",
]

COMPOSITES = {
    "Mom126_Dispersion21":            ["Mom_126", "Dispersion_21"],
    "Mom126_AvgRS126":                ["Mom_126", "Avg_Constituent_RS_126"],
    "Mom126_Dispersion21_AvgRS126":   ["Mom_126", "Dispersion_21", "Avg_Constituent_RS_126"],
    "Mom126_MomSlope21":              ["Mom_126", "Mom_Slope_21"],   # expect little/no improvement -- redundancy check
}

SAMPLE_EVERY = 21   # trading days between correlation samples, avoids near-duplicate adjacent-day rows


# ══════════════════════════════════════════════════════════════════════════
# PAIRWISE RANK CORRELATION
# ══════════════════════════════════════════════════════════════════════════

def pairwise_rank_correlation(signals, candidates, sample_every=SAMPLE_EVERY):
    dates = signals[candidates[0]].index[::sample_every]
    pair_corrs = {(a, b): [] for i, a in enumerate(candidates) for b in candidates[i + 1:]}

    for d in dates:
        rows = {c: signals[c].loc[d] for c in candidates}
        for a, b in pair_corrs:
            sa, sb = rows[a].dropna(), rows[b].dropna()
            common = sa.index.intersection(sb.index)
            if len(common) < 4:
                continue
            corr, _ = spearmanr(sa[common], sb[common])
            if not np.isnan(corr):
                pair_corrs[(a, b)].append(corr)

    mat = pd.DataFrame(np.nan, index=candidates, columns=candidates)
    for c in candidates:
        mat.loc[c, c] = 1.0
    for (a, b), vals in pair_corrs.items():
        avg = np.mean(vals) if vals else np.nan
        mat.loc[a, b] = avg
        mat.loc[b, a] = avg
    return mat.round(3)


def plot_correlation_matrix(mat, out_png):
    fig, ax = plt.subplots(figsize=(9, 7.5))
    im = ax.imshow(mat.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(mat.columns)))
    ax.set_xticklabels(mat.columns, rotation=45, ha="right")
    ax.set_yticks(range(len(mat.index)))
    ax.set_yticklabels(mat.index)
    for i in range(len(mat.index)):
        for j in range(len(mat.columns)):
            v = mat.values[i, j]
            if pd.notna(v):
                ax.text(j, i, f"{v:.2f}", ha="center", va="center",
                        color="white" if abs(v) > 0.55 else "black", fontsize=9)
    ax.set_title("Sector Factor Pairwise Rank Correlation\n(average daily cross-sectional Spearman, sampled every 21d)")
    fig.colorbar(im, ax=ax, shrink=0.8, label="Avg Spearman correlation")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
    print(f"Saved chart  -> {out_png}")


# ══════════════════════════════════════════════════════════════════════════
# COMPOSITE SCORES (equal-weight percentile rank blend)
# ══════════════════════════════════════════════════════════════════════════

def build_composite(signals, factor_names):
    pct_ranks = [signals[name].rank(axis=1, pct=True) for name in factor_names]
    return sum(pct_ranks) / len(pct_ranks)


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading price data...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)
    prices = prices.ffill()

    members, ticker_cap = build_sector_membership(prices, INSTRUMENTS_CSV)
    daily_ret = build_masked_daily_returns(prices)
    sector_price, sector_ret = build_sector_index(daily_ret, members)
    bucket_price = build_bucket_weighted_index(daily_ret, members, ticker_cap)
    bench_price = sector_price.mean(axis=1)

    signals = {}
    mom_factors, mom126_for_accel = build_momentum_factors(sector_price)
    signals.update(mom_factors)
    signals.update(build_acceleration_factors(sector_price, mom_factors["Mom_21"], mom126_for_accel))
    signals.update(build_breadth_factors(prices, members, bench_price))
    signals.update(build_participation_factors(sector_price, bucket_price, daily_ret, members))
    signals.update(build_capital_flow_factors(prices, volumes, daily_ret, members))

    # ── 1. Pairwise rank correlation ──────────────────────────────────────
    print(f"\nComputing pairwise rank correlation among: {CANDIDATES}")
    corr_mat = pairwise_rank_correlation(signals, CANDIDATES)
    corr_csv = os.path.join(SCRIPT_DIR, "sector_factor_correlation_matrix.csv")
    corr_mat.to_csv(corr_csv)
    print(f"Saved matrix -> {corr_csv}\n")
    print(corr_mat.to_string())
    plot_correlation_matrix(corr_mat, os.path.join(SCRIPT_DIR, "sector_factor_correlation_matrix.png"))

    # ── 2. Composite ICIR vs best individual component ────────────────────
    print("\nEvaluating composites...")
    composite_results = []
    for comp_name, components in COMPOSITES.items():
        composite_signal = build_composite(signals, components)
        for h in HORIZONS:
            row = evaluate_signal(composite_signal, sector_price, h)
            row["Signal"] = comp_name
            row["Horizon"] = h
            composite_results.append(row)
            print(f"  {comp_name:<32} h={h:<4} N={row['N']:<4} ICIR={row['ICIR']:.3f}")

    # Individual components' own ICIR, for direct side-by-side comparison
    individual_results = []
    for name in CANDIDATES:
        for h in HORIZONS:
            row = evaluate_signal(signals[name], sector_price, h)
            row["Signal"] = name
            row["Horizon"] = h
            individual_results.append(row)

    cols = ["Signal", "Horizon", "N", "IC_mean", "IC_std", "ICIR", "IC_tstat"]
    comp_df = pd.DataFrame(composite_results)[cols].round(4)
    indiv_df = pd.DataFrame(individual_results)[cols].round(4)
    indiv_df.insert(0, "Type", "Individual")
    comp_df.insert(0, "Type", "Composite")
    combined = pd.concat([indiv_df, comp_df], ignore_index=True)

    out_csv = os.path.join(SCRIPT_DIR, "sector_factor_composite_results.csv")
    combined.to_csv(out_csv, index=False)
    print(f"\nSaved results -> {out_csv}\n")
    print(combined.sort_values(["Horizon", "Type", "Signal"]).to_string(index=False))


if __name__ == "__main__":
    main()

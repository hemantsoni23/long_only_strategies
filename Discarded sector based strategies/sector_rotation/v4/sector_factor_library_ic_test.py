"""
sector_factor_library_ic_test.py
==================================
Factor Research for Sector Rotation -- a broader IC/ICIR/t-stat library
test, NOT a strategy variant. Extends sector_signal_ic_test.py's harness
(same non-overlapping-horizon sampling, same IC/ICIR/t-stat/top-K-spread
methodology) to a wider set of sector-ranking factors, organized into
five families, so the sector ranking rule can be chosen from evidence
rather than intuition before any strategy code changes.

Data availability notes (checked before building this):
  - Delivery % is NOT present anywhere in the OHLCV files (open/high/low/
    close/volume only) -- dropped from the library, not approximated.
  - instruments_clean.csv has no numeric market cap or shares outstanding,
    only a 3-bucket Cap tag (Large/Mid/Small). "Cap-weighted return" is
    therefore a labelled PROXY (Large=3x/Mid=2x/Small=1x bucket weights),
    not a true float/cap-weighted return -- treat Participation_Gap_126
    with that caveat in mind.

FACTOR LIBRARY (dates x 11 sectors each):
  Momentum      : Mom_21, Mom_63, Mom_126, Mom_Weighted
  Acceleration  : Accel_21, Rank_Improve_21, Mom_Slope_21
  Breadth       : Breadth_SMA200, Breadth_NewHigh_20, Avg_Constituent_RS_126
  Participation : Participation_Gap_126, Dispersion_21
  Capital Flow  : UpDownVol_Ratio_20, Turnover_Growth_20

Run: python sector_rotation/sector_factor_library_ic_test.py
Outputs (written next to this script):
    sector_factor_library_results.csv   - one row per (signal, horizon)
    sector_factor_library_icir.png      - grouped bar chart, ICIR by horizon
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr, ttest_1samp
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from hr_breakout_v2 import load_data


# ══════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════

DATA_FOLDER     = "/home/chirag1205/Downloads/output_stocks"
SCRIPT_DIR      = os.path.dirname(__file__)
INSTRUMENTS_CSV = os.path.join(SCRIPT_DIR, "..", "..", "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"
SECTOR_COL      = "Sector_clean"
CAP_COL         = "Cap"

MIN_STOCKS      = 8
HORIZONS        = [21, 63, 126, 252]
TOP_K           = [3, 5]
CA_DROP_THRESH  = 0.40
CA_GAIN_THRESH  = 3.00

CAP_BUCKET_WEIGHTS = {"Large": 3.0, "Mid": 2.0, "Small": 1.0}   # proxy only -- see module docstring

FACTOR_FAMILIES = {
    "Mom_21": "Momentum", "Mom_63": "Momentum", "Mom_126": "Momentum", "Mom_Weighted": "Momentum",
    "Accel_21": "Acceleration", "Rank_Improve_21": "Acceleration", "Mom_Slope_21": "Acceleration",
    "Breadth_SMA200": "Breadth", "Breadth_NewHigh_20": "Breadth", "Avg_Constituent_RS_126": "Breadth",
    "Participation_Gap_126": "Participation", "Dispersion_21": "Participation",
    "UpDownVol_Ratio_20": "Capital Flow", "Turnover_Growth_20": "Capital Flow",
}


# ══════════════════════════════════════════════════════════════════════════
# SECTOR MEMBERSHIP / INDEX
# ══════════════════════════════════════════════════════════════════════════

def build_sector_membership(prices, instruments_csv, symbol_col=SYMBOL_COL,
                             sector_col=SECTOR_COL, min_stocks=MIN_STOCKS):
    inst = pd.read_csv(instruments_csv).dropna(subset=[symbol_col, sector_col])
    ticker_sector = dict(zip(inst[symbol_col], inst[sector_col]))
    ticker_cap    = dict(zip(inst[symbol_col], inst[CAP_COL]))

    members = {}
    for ticker, sector in ticker_sector.items():
        if ticker in prices.columns:
            members.setdefault(sector, []).append(ticker)
    members = {s: m for s, m in members.items() if len(m) >= min_stocks}

    print(f"[factor_lib] {len(members)} sectors qualify (>= {min_stocks} stocks):")
    for s, m in members.items():
        print(f"    {s:<25} {len(m)} stocks")

    return members, ticker_cap


def build_masked_daily_returns(prices):
    """CA/bad-tick-guarded daily returns, shared input for every factor below."""
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    return daily_ret.where(~bad_tick)


def build_sector_index(daily_ret, members):
    sector_ret = pd.DataFrame({s: daily_ret[m].mean(axis=1, skipna=True) for s, m in members.items()})
    sector_price = (1 + sector_ret.fillna(0)).cumprod()
    return sector_price, sector_ret


def build_bucket_weighted_index(daily_ret, members, ticker_cap):
    """Proxy 'cap-weighted' index using the 3-bucket Cap tag -- see module docstring."""
    weighted_cols = {}
    for s, tickers in members.items():
        w = pd.Series({t: CAP_BUCKET_WEIGHTS.get(ticker_cap.get(t), 1.0) for t in tickers})
        sub = daily_ret[tickers]
        w_arr = w.reindex(sub.columns).values
        vals = sub.values
        mask = ~np.isnan(vals)
        weighted_sum = np.nansum(vals * w_arr, axis=1)
        weight_total = (mask * w_arr).sum(axis=1)
        weighted_cols[s] = np.where(weight_total > 0, weighted_sum / weight_total, np.nan)

    bucket_ret = pd.DataFrame(weighted_cols, index=daily_ret.index)
    bucket_price = (1 + bucket_ret.fillna(0)).cumprod()
    return bucket_price


# ══════════════════════════════════════════════════════════════════════════
# FACTOR LIBRARY
# ══════════════════════════════════════════════════════════════════════════

def _rolling_slope(series, window):
    x = np.arange(window)
    x_mean = x.mean()
    x_var = ((x - x_mean) ** 2).sum()

    def slope(y):
        if np.isnan(y).any():
            return np.nan
        return ((x - x_mean) * (y - y.mean())).sum() / x_var

    return series.rolling(window).apply(slope, raw=True)


def build_momentum_factors(sector_price):
    mom21  = sector_price.pct_change(21,  fill_method=None)
    mom63  = sector_price.pct_change(63,  fill_method=None)
    mom126 = sector_price.pct_change(126, fill_method=None)
    mom_weighted = 0.5 * mom21 + 0.3 * mom63 + 0.2 * mom126
    return {"Mom_21": mom21, "Mom_63": mom63, "Mom_126": mom126, "Mom_Weighted": mom_weighted}, mom126


def build_acceleration_factors(sector_price, mom21, mom126):
    accel_21 = mom21 - mom21.shift(21)

    rank_today = mom126.rank(axis=1, ascending=False)
    rank_prev  = rank_today.shift(21)
    rank_improve_21 = rank_prev - rank_today   # positive = rank number decreased = improved

    log_price = np.log(sector_price.replace(0, np.nan))
    mom_slope_21 = pd.DataFrame(
        {c: _rolling_slope(log_price[c], 21) for c in log_price.columns}, index=log_price.index
    )

    return {"Accel_21": accel_21, "Rank_Improve_21": rank_improve_21, "Mom_Slope_21": mom_slope_21}


def build_breadth_factors(prices, members, bench_price):
    sma200 = prices.rolling(200, min_periods=200).mean()
    above200 = prices > sma200
    breadth_sma200 = pd.DataFrame({s: above200[m].mean(axis=1, skipna=True) for s, m in members.items()})

    new_high_20 = prices >= prices.rolling(20, min_periods=20).max()
    breadth_newhigh_20 = pd.DataFrame({s: new_high_20[m].mean(axis=1, skipna=True) for s, m in members.items()})

    stock_mom126 = prices.pct_change(126, fill_method=None)
    bench_mom126 = bench_price.pct_change(126, fill_method=None)
    stock_rs = stock_mom126.sub(bench_mom126, axis=0)
    avg_constituent_rs = pd.DataFrame({s: stock_rs[m].mean(axis=1, skipna=True) for s, m in members.items()})

    return {
        "Breadth_SMA200": breadth_sma200,
        "Breadth_NewHigh_20": breadth_newhigh_20,
        "Avg_Constituent_RS_126": avg_constituent_rs,
    }


def build_participation_factors(sector_price, bucket_price, daily_ret, members):
    participation_gap = (
        sector_price.pct_change(126, fill_method=None)
        - bucket_price.pct_change(126, fill_method=None)
    )

    daily_dispersion = pd.DataFrame(
        {s: daily_ret[m].std(axis=1, skipna=True) for s, m in members.items()}
    )
    dispersion_21 = daily_dispersion.rolling(21).mean()

    return {"Participation_Gap_126": participation_gap, "Dispersion_21": dispersion_21}


def build_capital_flow_factors(prices, volumes, daily_ret, members):
    up_vol   = volumes.where(daily_ret > 0, 0.0)
    down_vol = volumes.where(daily_ret < 0, 0.0)
    sector_up_vol   = pd.DataFrame({s: up_vol[m].sum(axis=1) for s, m in members.items()}).rolling(20).sum()
    sector_down_vol = pd.DataFrame({s: down_vol[m].sum(axis=1) for s, m in members.items()}).rolling(20).sum()
    updown_ratio_20 = sector_up_vol / sector_down_vol.replace(0, np.nan)

    turnover = prices * volumes
    sector_turnover = pd.DataFrame({s: turnover[m].sum(axis=1, skipna=True) for s, m in members.items()})
    turnover_avg20 = sector_turnover.rolling(20).mean()
    turnover_growth_20 = turnover_avg20.pct_change(20, fill_method=None)

    return {"UpDownVol_Ratio_20": updown_ratio_20, "Turnover_Growth_20": turnover_growth_20}


# ══════════════════════════════════════════════════════════════════════════
# EVALUATION (same methodology as sector_signal_ic_test.py)
# ══════════════════════════════════════════════════════════════════════════

def evaluate_signal(signal_df, sector_price, horizon):
    dates = signal_df.index
    n_dates = len(dates)

    ics = []
    topk_spreads = {k: [] for k in TOP_K}

    for idx in range(0, n_dates - horizon, horizon):
        d, d_fwd = dates[idx], dates[idx + horizon]

        sig_row = signal_df.loc[d].dropna()
        if len(sig_row) < 3:
            continue

        fwd_ret = sector_price.loc[d_fwd, sig_row.index] / sector_price.loc[d, sig_row.index] - 1
        fwd_ret = fwd_ret.dropna()
        common = sig_row.index.intersection(fwd_ret.index)
        if len(common) < 3:
            continue
        sig_c, fwd_c = sig_row[common], fwd_ret[common]

        ic, _ = spearmanr(sig_c, fwd_c)
        if not np.isnan(ic):
            ics.append(ic)

        ranked = sig_c.sort_values(ascending=False).index
        for k in TOP_K:
            top = ranked[:k]
            topk_spreads[k].append(fwd_c[top].mean() - fwd_c.mean())

    ics = np.array(ics)
    n = len(ics)
    ic_mean = ics.mean() if n else np.nan
    ic_std  = ics.std(ddof=1) if n > 1 else np.nan
    icir    = ic_mean / ic_std if ic_std else np.nan
    ic_tstat = icir * np.sqrt(n) if n and not np.isnan(icir) else np.nan

    row = {"N": n, "IC_mean": ic_mean, "IC_std": ic_std, "ICIR": icir, "IC_tstat": ic_tstat}
    for k in TOP_K:
        arr = np.array(topk_spreads[k])
        if len(arr) > 1:
            t, _ = ttest_1samp(arr, 0.0)
            row[f"Top{k}_spread_mean"]  = arr.mean()
            row[f"Top{k}_spread_tstat"] = t
        else:
            row[f"Top{k}_spread_mean"]  = np.nan
            row[f"Top{k}_spread_tstat"] = np.nan
    return row


def plot_icir(results_df, out_png):
    pivot = results_df.pivot(index="Signal", columns="Horizon", values="ICIR")
    fig, ax = plt.subplots(figsize=(16, 7))
    pivot.plot(kind="bar", ax=ax)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("ICIR")
    ax.set_title("Sector Factor Library — Predictive Power (ICIR by Horizon)")
    ax.legend(title="Horizon (days)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()
    print(f"Saved chart  -> {out_png}")


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

    print(f"\nFactor library built: {len(signals)} factors x {len(HORIZONS)} horizons\n")

    results = []
    for name, sig_df in signals.items():
        for h in HORIZONS:
            row = evaluate_signal(sig_df, sector_price, h)
            row["Signal"]  = name
            row["Family"]  = FACTOR_FAMILIES[name]
            row["Horizon"] = h
            results.append(row)
            print(f"  {row['Family']:<14} {name:<24} h={h:<4} N={row['N']:<4} ICIR={row['ICIR']:.3f}")

    cols = (["Family", "Signal", "Horizon", "N", "IC_mean", "IC_std", "ICIR", "IC_tstat"]
            + [f"Top{k}_spread_mean" for k in TOP_K]
            + [f"Top{k}_spread_tstat" for k in TOP_K])
    results_df = pd.DataFrame(results)[cols].round(4)

    out_csv = os.path.join(SCRIPT_DIR, "sector_factor_library_results.csv")
    results_df.to_csv(out_csv, index=False)
    print(f"\nSaved results -> {out_csv}\n")
    print(results_df.sort_values(["Family", "Signal", "Horizon"]).to_string(index=False))

    plot_icir(results_df, os.path.join(SCRIPT_DIR, "sector_factor_library_icir.png"))


if __name__ == "__main__":
    main()

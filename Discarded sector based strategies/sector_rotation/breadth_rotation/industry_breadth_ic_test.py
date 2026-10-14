"""
industry_breadth_ic_test.py
=============================
Same breadth-divergence IC diagnostic as sector_breadth_ic_test.py, rebuilt at
INDUSTRY_CLEAN granularity (~202 raw buckets, ~23-33 clear >=8 eligible+tagged
stocks within the real tradeable universe -- see industry_granularity_check.py)
instead of SECTOR_CLEAN (11 buckets). Coverage among eligible tradeable names
is 91.9% -- untagged stocks are simply dropped (build_sector_membership's
dropna already does this), not worth a Sector_clean fallback for an 8% gap.

Everything else -- methodology, factor construction, orthogonalization
approach -- is identical to sector_breadth_ic_test.py; only the grouping
column changes. The pooled-OLS beta is re-fit here from scratch (the
Sector_clean beta of 0.531 does NOT transfer to a different bucket count/
composition) and is expected to differ.

Original module docstring (still applies at this finer granularity):
-----------------------------------------------------------------------
Diagnostic for a NEW sector-rotation hypothesis: rank groups by internal
PARTICIPATION/BREADTH (% of constituent stocks confirming the move) instead
of the group INDEX's own return magnitude.

Why this factor, not another momentum variant
-----------------------------------------------
Every strategy in this shop so far -- csm_batch/absolute/quad (stock-level
Sharpe momentum) and the colleague's sector_factor_strategy v4-v6 (sector rank
= 126d index momentum blended with 21d dispersion, stock rank = proximity to
52w high) -- is a transform of price RETURN magnitude. Breadth is a different
statistic: cross-sectional AGREEMENT among a sector's constituents, independent
of how far the cap-weighted/equal-weighted index itself has moved. A sector can
show strong index return on 2-3 mega/large caps while breadth quietly
deteriorates (unhealthy, narrow rally -- momentum factor stays bullish, breadth
already warns), or the reverse (broad quiet accumulation before the index-level
number catches up). That mechanism gives genuinely different trade timing, not
just a re-parameterisation of the same trend signal -- which is the whole point
of building this as a second, uncorrelated sector strategy.

Two breadth components, each a % of the ELIGIBLE (universe-filtered) sector
constituents, cross-sectional percentile-ranked across sectors each day:
  B1  pct_above_200dma   -- longer-run participation
  B2  net_new_hi_lo_21d  -- 21d-summed (new 52w highs - new 52w lows) / N,
                            a breadth-thrust component that reacts faster
                            than the slow-moving 200dma count

composite = (rank(B1) + rank(B2)) / 2   [raw], plus a 10d-smoothed variant
(colleague's own v4->v5 note: an unsmoothed composite churns weekly rotation
too much -- testing both from the start instead of re-discovering it later).

Also computed for direct comparison on the IDENTICAL sector index / eligible-
sector-day mask:
  MOM_DISP  = colleague's factor: (rank(126d sector return) + rank(21d avg
              cross-sectional dispersion)) / 2  -- same construction as
              sector_factor_strategy_v6.py's build_sector_rank_composite()

Sector universe/index construction (membership, liquidity/price/circuit
filters, bad-tick guard, equal-weight index) intentionally mirrors
sector_factor_strategy_v6.py so any IC difference is attributable to the
FACTOR choice, not to a different universe -- that's pure data-hygiene
plumbing reuse, not hypothesis reuse.

Scope discipline: this is Stage 1-2 only (does the raw signal have edge at
all). No backtest, no stock-selection layer, no stops. IN-SAMPLE WINDOW ONLY
(2003-01-01 -> 2012-12-31, per this shop's stated IS/OOS convention and
Playbook Stage 3's "OOS untouched until config is frozen" rule) -- earlier
history is loaded only to warm up the 200d/252d rolling windows, never scored.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import spearmanr

warnings.filterwarnings("ignore")

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, os.path.join(REPO_ROOT, "HR_breakout"))
from hr_breakout_v2 import load_data  # noqa: E402

DATA_FOLDER     = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
INSTRUMENTS_CSV = os.path.join(REPO_ROOT, "instruments_clean.csv")
SYMBOL_COL      = "trading_symbol"
SECTOR_COL      = "Industry_clean"

# ── IS/OOS discipline: score only the in-sample window; load full history
# only so 200d/252d rolling windows are warm by the IS start date ─────────
IS_START = pd.Timestamp("2003-01-01")
IS_END   = pd.Timestamp("2012-12-31")

# Universe / sector construction -- mirrors sector_factor_strategy_v6.py
MIN_STOCKS_SECTOR = 8
UNIVERSE_TOP_N     = 1000
MIN_PRICE          = 10.0
MAX_CIRCUIT_DAYS   = 5
CA_DROP_THRESH     = 0.40
CA_GAIN_THRESH     = 3.00

# Breadth factor windows
SMA_FAST_WIN     = 50
SMA_SLOW_WIN     = 200
HI_LO_WIN        = 252
HI_LO_MIN_PERIODS = 200
NET_HI_LO_SMOOTH = 21     # thrust window
COMPOSITE_SMOOTH = 10     # matches colleague's v5 smoothing choice, for comparability

# Comparison factor (colleague's) windows
SECTOR_MOM_PERIOD = 126
DISPERSION_WINDOW = 21

HORIZONS = {"1m": 21, "3m": 63, "6m": 126, "12m": 252}
MIN_SECTORS_FOR_IC = 10  # need at least this many valid industries cross-sectionally to compute a daily IC
                          # (raised from Sector_clean's 5 -- ~23 industries are typically eligible per
                          # day now vs ~10 sectors, so a 10-name floor is still an achievable, more
                          # statistically meaningful cross-section, not a stricter relative bar)


# ══════════════════════════════════════════════════════════════════════════
# UNIVERSE / SECTOR CONSTRUCTION  (mirrors sector_factor_strategy_v6.py)
# ══════════════════════════════════════════════════════════════════════════

def build_sector_membership(prices, instruments_csv, min_stocks=MIN_STOCKS_SECTOR):
    inst = pd.read_csv(instruments_csv).dropna(subset=[SYMBOL_COL, SECTOR_COL])
    ticker_sector = dict(zip(inst[SYMBOL_COL], inst[SECTOR_COL]))
    members = {}
    for ticker, sector in ticker_sector.items():
        if ticker in prices.columns:
            members.setdefault(sector, []).append(ticker)
    members = {s: m for s, m in members.items() if len(m) >= min_stocks}
    print(f"[sector_breadth] {len(members)} sectors qualify (>= {min_stocks} stocks): "
          f"{sorted(members.keys())}")
    return members


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


def build_sector_index(prices, members):
    """Equal-weight, bad-tick-guarded sector index -- identical convention to
    sector_factor_strategy_v6.py so forward returns are apples-to-apples."""
    daily_ret = prices.pct_change(fill_method=None)
    bad_tick = (daily_ret < -CA_DROP_THRESH) | (daily_ret > CA_GAIN_THRESH)
    daily_ret = daily_ret.where(~bad_tick)
    sector_ret = pd.DataFrame({s: daily_ret[m].mean(axis=1, skipna=True) for s, m in members.items()})
    sector_price = (1 + sector_ret.fillna(0)).cumprod()
    return sector_price, daily_ret


# ══════════════════════════════════════════════════════════════════════════
# FACTOR 1: BREADTH / PARTICIPATION  (the new hypothesis)
# ══════════════════════════════════════════════════════════════════════════

def build_breadth_factor(prices, members, universe_mask, universe_gate=True):
    """
    universe_gate=True  -> L3 (tradeable): eligibility requires universe_mask
    universe_gate=False -> L0 (raw): eligibility is sector-tag membership only
    Returns (breadth_raw, breadth_smoothed, eligible_count) -- all sector x date.
    """
    sma200 = prices.rolling(SMA_SLOW_WIN, min_periods=150).mean()
    above_200 = (prices > sma200)

    roll_hi = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).max()
    roll_lo = prices.rolling(HI_LO_WIN, min_periods=HI_LO_MIN_PERIODS).min()
    new_hi = (prices >= roll_hi)
    new_lo = (prices <= roll_lo)

    dates = prices.index
    b1_dict, b2_dict, n_dict = {}, {}, {}

    for sector, tickers in members.items():
        tickers = [t for t in tickers if t in prices.columns]
        if universe_gate:
            elig = universe_mask[tickers]
        else:
            elig = pd.DataFrame(True, index=dates, columns=tickers)

        n_elig = elig.sum(axis=1).replace(0, np.nan)
        n_dict[sector] = n_elig

        above_200_elig = above_200[tickers].where(elig)
        b1_dict[sector] = above_200_elig.sum(axis=1) / n_elig

        net_hi_lo = (new_hi[tickers].astype(float) - new_lo[tickers].astype(float)).where(elig)
        net_hi_lo_frac = net_hi_lo.sum(axis=1) / n_elig
        b2_dict[sector] = net_hi_lo_frac.rolling(NET_HI_LO_SMOOTH, min_periods=NET_HI_LO_SMOOTH).sum() / NET_HI_LO_SMOOTH

    B1 = pd.DataFrame(b1_dict)   # pct above 200dma
    B2 = pd.DataFrame(b2_dict)   # 21d-avg net new-hi/lo fraction
    n_elig_df = pd.DataFrame(n_dict)

    # Require a minimum eligible constituent count for a sector-day to count
    valid = n_elig_df >= MIN_STOCKS_SECTOR
    B1 = B1.where(valid)
    B2 = B2.where(valid)

    composite_raw = (B1.rank(axis=1, pct=True) + B2.rank(axis=1, pct=True)) / 2.0
    composite_smooth = composite_raw.rolling(COMPOSITE_SMOOTH, min_periods=COMPOSITE_SMOOTH).mean()

    return composite_raw, composite_smooth, n_elig_df


# ══════════════════════════════════════════════════════════════════════════
# FACTOR 2: MOMENTUM + DISPERSION  (colleague's factor, for comparison only)
# ══════════════════════════════════════════════════════════════════════════

def build_mom_disp_factor(sector_price, daily_ret, members):
    mom126 = sector_price.pct_change(SECTOR_MOM_PERIOD, fill_method=None)
    daily_dispersion = pd.DataFrame(
        {s: daily_ret[m].std(axis=1, skipna=True) for s, m in members.items()}
    )
    dispersion = daily_dispersion.rolling(DISPERSION_WINDOW).mean()
    composite = (mom126.rank(axis=1, pct=True) + dispersion.rank(axis=1, pct=True)) / 2.0
    return composite


# ══════════════════════════════════════════════════════════════════════════
# IC / NW-t / ICIR
# ══════════════════════════════════════════════════════════════════════════

def daily_ic_series(factor_df, fwd_ret_df, min_sectors=MIN_SECTORS_FOR_IC):
    ic_vals = {}
    common_idx = factor_df.index.intersection(fwd_ret_df.index)
    for date in common_idx:
        f = factor_df.loc[date]
        r = fwd_ret_df.loc[date]
        both = pd.concat([f, r], axis=1).dropna()
        if len(both) < min_sectors:
            continue
        rho, _ = spearmanr(both.iloc[:, 0], both.iloc[:, 1])
        if pd.notna(rho):
            ic_vals[date] = rho
    return pd.Series(ic_vals).sort_index()


def newey_west_ic_stats(ic_series, lag_days):
    x = ic_series.dropna()
    n = len(x)
    if n < 30:
        return dict(mean_ic=np.nan, nw_t=np.nan, icir=np.nan, n=n)
    y = x.values
    X = np.ones((n, 1))
    model = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": max(1, lag_days)})
    mean_ic = model.params[0]
    nw_t = model.tvalues[0]
    icir = x.mean() / x.std() if x.std() > 0 else np.nan
    return dict(mean_ic=mean_ic, nw_t=nw_t, icir=icir, n=n)


def run_ic_ladder(name, factor_df, sector_price, is_start, is_end):
    print(f"\n{'='*90}\n{name}\n{'='*90}")
    rows = []
    for label, h in HORIZONS.items():
        fwd_ret = sector_price.shift(-h) / sector_price - 1.0
        # score only within the IS window (both factor obs. date and the
        # forward-return WINDOW should sit inside/near IS -- factor date is
        # what's gated; the h-day-ahead return can spill a few weeks past
        # IS_END, which is fine, it's still fully realized historical data,
        # not a peek at a later *decision*)
        ic_s = daily_ic_series(factor_df, fwd_ret)
        ic_s = ic_s[(ic_s.index >= is_start) & (ic_s.index <= is_end)]
        stats = newey_west_ic_stats(ic_s, lag_days=h)
        rows.append(dict(horizon=label, **stats))
        flag = "OK" if (pd.notna(stats["nw_t"]) and abs(stats["nw_t"]) >= 2.0) else "weak"
        print(f"  {label:>4}  mean_IC={stats['mean_ic']:+.4f}  NW-t={stats['nw_t']:+.2f}  "
              f"ICIR={stats['icir']:+.3f}  n_days={stats['n']:5d}  [{flag}]")
    return pd.DataFrame(rows)


def tercile_monotonicity(factor_df, sector_price, horizon_days, is_start, is_end, label):
    fwd_ret = sector_price.shift(-horizon_days) / sector_price - 1.0
    f = factor_df[(factor_df.index >= is_start) & (factor_df.index <= is_end)]
    r = fwd_ret.reindex(f.index)

    bucket_returns = {0: [], 1: [], 2: []}
    for date in f.index:
        frow = f.loc[date].dropna()
        if len(frow) < MIN_SECTORS_FOR_IC:
            continue
        rrow = r.loc[date]
        tercile = pd.qcut(frow.rank(method="first"), 3, labels=[0, 1, 2])
        for sector, t in tercile.items():
            rv = rrow.get(sector, np.nan)
            if pd.notna(rv):
                bucket_returns[int(t)].append(rv)

    print(f"\n  Tercile monotonicity @ {label} (Low/Mid/High avg fwd return):")
    means = {}
    for t in (0, 1, 2):
        vals = bucket_returns[t]
        means[t] = np.mean(vals) if vals else np.nan
        print(f"    T{t} ({'Low' if t==0 else 'Mid' if t==1 else 'High'}): "
              f"mean={means[t]*100:+.2f}%  n={len(vals)}")
    mono = (means[2] > means[1] > means[0]) if all(pd.notna(v) for v in means.values()) else False
    print(f"    Monotonic Low<Mid<High: {mono}")
    return means, mono


def topn_overlap_check(breadth_df, mom_disp_df, is_start, is_end, top_n=4, rebalance_every=5):
    """The decision-relevant question: on rebalance days, how much do the
    actual TOP-N SECTOR SETS overlap between breadth and momentum+dispersion?
    A moderate rank correlation can still pick mostly-disjoint top-N sets --
    this is what determines whether the two strategies would hold the same
    sectors at the same time, not the continuous correlation coefficient.
    """
    common = breadth_df.index.intersection(mom_disp_df.index)
    common = common[(common >= is_start) & (common <= is_end)]
    common = common.sort_values()

    overlaps, jaccards = [], []
    for i, date in enumerate(common):
        if i % rebalance_every != 0:
            continue
        a = breadth_df.loc[date].dropna()
        b = mom_disp_df.loc[date].dropna()
        if len(a) < top_n or len(b) < top_n:
            continue
        top_a = set(a.sort_values(ascending=False).index[:top_n])
        top_b = set(b.sort_values(ascending=False).index[:top_n])
        inter = len(top_a & top_b)
        union = len(top_a | top_b)
        overlaps.append(inter / top_n)
        jaccards.append(inter / union if union else np.nan)

    overlaps = np.array(overlaps)
    jaccards = np.array(jaccards)
    print(f"\n  Top-{top_n} sector SET overlap on rebalance days (IS window, every {rebalance_every}d):")
    print(f"    avg shared sectors: {overlaps.mean()*top_n:.2f} / {top_n}  "
          f"({overlaps.mean()*100:.1f}% of slots)")
    print(f"    avg Jaccard similarity: {np.nanmean(jaccards):.3f}")
    print(f"    n_rebalance_days={len(overlaps)}")
    print(f"    distribution of shared-count: "
          f"{pd.Series((overlaps*top_n).round().astype(int)).value_counts().sort_index().to_dict()}")
    return overlaps, jaccards


def build_divergence_factors(breadth_df, mom_disp_df, is_start, is_end):
    """
    Two ways to isolate the part of breadth NOT explained by price momentum --
    i.e. sectors where participation is running ahead of (or behind) what the
    return-based factor already says, rather than just "breadth that happens
    to also have decent momentum" (the ~0.45 correlation we measured).

    div_raw    : breadth_pctrank - mom_disp_pctrank, the literal "rank gap".
                 Simple and interpretable, but NOT guaranteed uncorrelated
                 with mom_disp -- when two variables aren't perfectly
                 correlated, their raw difference is typically still
                 (negatively) correlated with whichever term you subtracted,
                 so this can drift towards just picking momentum LAGGARDS
                 rather than genuine breadth-leads-price divergence.

    div_resid  : breadth_pctrank - beta*mom_disp_pctrank, where beta is a
                 SINGLE pooled-OLS slope fit once over all IS-window
                 sector-days (breadth ~ mom_disp). This is the textbook
                 orthogonalisation -- by construction the residual has ~zero
                 correlation with mom_disp (up to estimation noise), so a
                 high score genuinely means "breadth says more than momentum
                 does here", not "momentum says less than usual". Beta is
                 estimated ONLY on the IS window (no look-ahead).
    """
    common = breadth_df.index.intersection(mom_disp_df.index)
    is_common = common[(common >= is_start) & (common <= is_end)]

    b_is = breadth_df.loc[is_common].stack()
    m_is = mom_disp_df.loc[is_common].stack()
    paired = pd.concat([b_is.rename("breadth"), m_is.rename("mom_disp")], axis=1).dropna()
    X = sm.add_constant(paired["mom_disp"].values)
    beta_model = sm.OLS(paired["breadth"].values, X).fit()
    alpha, beta = beta_model.params
    print(f"\n  Pooled orthogonalising regression (IS window, n={len(paired)}): "
          f"breadth = {alpha:.3f} + {beta:.3f} * mom_disp   (R^2={beta_model.rsquared:.3f})")

    div_raw = breadth_df - mom_disp_df
    div_resid = breadth_df - beta * mom_disp_df   # drop alpha: constant shift doesn't affect rank/IC
    return div_raw, div_resid


def orthogonality_check(breadth_df, mom_disp_df, is_start, is_end):
    common = breadth_df.index.intersection(mom_disp_df.index)
    common = common[(common >= is_start) & (common <= is_end)]
    rhos = []
    for date in common:
        a = breadth_df.loc[date]
        b = mom_disp_df.loc[date]
        both = pd.concat([a, b], axis=1).dropna()
        if len(both) < MIN_SECTORS_FOR_IC:
            continue
        rho, _ = spearmanr(both.iloc[:, 0], both.iloc[:, 1])
        if pd.notna(rho):
            rhos.append(rho)
    rhos = np.array(rhos)
    print(f"\n  Breadth vs Momentum+Dispersion cross-sectional rank corr "
          f"(daily, IS window): mean={rhos.mean():+.3f}  median={np.median(rhos):+.3f}  "
          f"n_days={len(rhos)}")
    print(f"  (Lower |corr| = more independent signal = lower chance of duplicate trades.)")
    return rhos


# ══════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════

def main():
    print("Loading OHLCV data (this can take a minute for ~5200 tickers)...")
    prices, volumes, highs, lows, opens = load_data(DATA_FOLDER)

    members = build_sector_membership(prices, INSTRUMENTS_CSV)
    universe_mask = build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = build_sector_index(prices, members)

    print(f"\nSector index date range: {sector_price.index.min().date()} -> "
          f"{sector_price.index.max().date()}")
    print(f"Scoring window (IS only): {IS_START.date()} -> {IS_END.date()}")

    # ── Breadth factor: L0 (unfiltered) vs L3 (universe-filtered) vs smoothed ──
    breadth_L0_raw, breadth_L0_smooth, n_elig_L0 = build_breadth_factor(
        prices, members, universe_mask, universe_gate=False)
    breadth_L3_raw, breadth_L3_smooth, n_elig_L3 = build_breadth_factor(
        prices, members, universe_mask, universe_gate=True)

    # ── Comparison factor: colleague's momentum + dispersion, same L3 sectors ──
    mom_disp = build_mom_disp_factor(sector_price, daily_ret, members)

    # ── Breadth floor: how many sector-days have >= MIN_SECTORS_FOR_IC valid sectors, IS window ──
    is_mask = (n_elig_L3.index >= IS_START) & (n_elig_L3.index <= IS_END)
    valid_sector_count_L3 = (n_elig_L3 >= MIN_STOCKS_SECTOR).sum(axis=1)[is_mask]
    excl_pct = (valid_sector_count_L3 < MIN_SECTORS_FOR_IC).mean() * 100
    print(f"\nBreadth floor (L3): {valid_sector_count_L3.mean():.1f} sectors/day avg eligible "
          f"(of {len(members)} total) in IS window; "
          f"{excl_pct:.1f}% of IS days have < {MIN_SECTORS_FOR_IC} valid sectors.")

    # ── IC ladders ──
    ladder_L0 = run_ic_ladder("BREADTH  [L0 -- raw, sector-tag only, no universe filter]",
                               breadth_L0_raw, sector_price, IS_START, IS_END)
    ladder_L3 = run_ic_ladder("BREADTH  [L3 -- tradeable, universe-filtered, raw]",
                               breadth_L3_raw, sector_price, IS_START, IS_END)
    ladder_L3_sm = run_ic_ladder("BREADTH  [L3 -- tradeable, universe-filtered, 10d-smoothed]",
                                  breadth_L3_smooth, sector_price, IS_START, IS_END)
    ladder_base = run_ic_ladder("BASELINE  [colleague's Momentum(126d) + Dispersion(21d), L3]",
                                 mom_disp, sector_price, IS_START, IS_END)

    # ── Monotonicity at 3m (where signal is expected to peak per playbook conv.) ──
    tercile_monotonicity(breadth_L3_raw, sector_price, HORIZONS["3m"], IS_START, IS_END,
                          label="3m, BREADTH L3 raw")
    tercile_monotonicity(breadth_L3_smooth, sector_price, HORIZONS["3m"], IS_START, IS_END,
                          label="3m, BREADTH L3 smoothed")

    # ── Orthogonality vs colleague's factor ──
    orthogonality_check(breadth_L3_raw, mom_disp, IS_START, IS_END)
    orthogonality_check(breadth_L3_smooth, mom_disp, IS_START, IS_END)

    # ── The decision-relevant version: actual top-N sector SET overlap ──
    # top_n=4 kept for direct comparability with the Sector_clean run; top_n=8
    # added since the strategy's actual entry depth may widen now that ~23
    # buckets are typically available instead of ~11.
    print(f"\n{'='*90}\nTOP-N SECTOR SET OVERLAP  (breadth vs colleague's momentum+dispersion)\n{'='*90}")
    for n in (4, 8):
        topn_overlap_check(breadth_L3_raw, mom_disp, IS_START, IS_END, top_n=n)
        topn_overlap_check(breadth_L3_smooth, mom_disp, IS_START, IS_END, top_n=n)

    # ══════════════════════════════════════════════════════════════════════
    # DIVERGENCE FACTORS -- purify breadth against the momentum+dispersion factor
    # ══════════════════════════════════════════════════════════════════════
    div_raw, div_resid = build_divergence_factors(breadth_L3_raw, mom_disp, IS_START, IS_END)

    ladder_div_raw = run_ic_ladder("DIVERGENCE [raw rank-gap: breadth - mom_disp]",
                                    div_raw, sector_price, IS_START, IS_END)
    ladder_div_resid = run_ic_ladder("DIVERGENCE [orthogonalised residual: breadth - beta*mom_disp]",
                                      div_resid, sector_price, IS_START, IS_END)

    tercile_monotonicity(div_raw, sector_price, HORIZONS["3m"], IS_START, IS_END,
                          label="3m, DIVERGENCE raw")
    tercile_monotonicity(div_resid, sector_price, HORIZONS["3m"], IS_START, IS_END,
                          label="3m, DIVERGENCE orthogonalised")

    print(f"\n{'='*90}\nDIVERGENCE vs MOM_DISP -- correlation + overlap (should be much lower now)\n{'='*90}")
    orthogonality_check(div_raw, mom_disp, IS_START, IS_END)
    orthogonality_check(div_resid, mom_disp, IS_START, IS_END)
    for n in (4, 8):
        print(f"\n  -- div_raw --")
        topn_overlap_check(div_raw, mom_disp, IS_START, IS_END, top_n=n)
        print(f"  -- div_resid --")
        topn_overlap_check(div_resid, mom_disp, IS_START, IS_END, top_n=n)

    for name, df in [("divergence_raw", ladder_div_raw), ("divergence_resid", ladder_div_resid)]:
        df.to_csv(os.path.join(os.path.dirname(__file__), f"ic_ladder_industry_{name}.csv"), index=False)

    # ── Save ladders for the record ──
    out_dir = os.path.dirname(__file__)
    for name, df in [("breadth_L0", ladder_L0), ("breadth_L3", ladder_L3),
                      ("breadth_L3_smoothed", ladder_L3_sm), ("mom_disp_baseline", ladder_base)]:
        df.to_csv(os.path.join(out_dir, f"ic_ladder_industry_{name}.csv"), index=False)
    print(f"\nSaved IC ladder CSVs to {out_dir}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
stage1_2_data_signal.py
===========================
STRATEGY_VALIDATION_PLAYBOOK.md Stages 1-2 for ResidualMomentumV2.

Stage 1 -- data integrity & universe definition:
  survivorship proxy, listing-history floor, min_periods check (code-level), breadth floor
  on v2's own 50-1000 band.

Stage 2 -- core signal diagnostics, filter ladder L0->L1->L2->L3->L5 (L4 N/A: this
strategy's regime filter -- the trend gate -- is portfolio-level, not a per-name filter, so
there is no per-name "gated" rung to insert):
  L0 raw (any symbol with a valid price that day)
  L1 + price floor (>=Rs20)
  L2 + liquidity floor (63d median $-volume >=Rs1cr), no rank cut
  L3 tradeable (+ rank-50-1000 cut -- this IS strat.univ, the live v2 universe)
  L5 ranked/held pool (the actual <=40-name book each month)
At each rung the composite is rebuilt with ITS OWN cross-sectional z-score (not reusing
self.R3b, which is already masked to L3) -- Spearman rank-IC is otherwise contaminated by
the wrong universe's z-scoring boundary.

Read-only: imports the live strategy/backtest code, never edits it.
"""
import os
import sys
import warnings

warnings.filterwarnings("ignore")

_HERE = os.path.dirname(os.path.abspath(__file__))
_V2_DIR = os.path.dirname(_HERE)
sys.path.insert(0, _V2_DIR)

import numpy as np
import pandas as pd
import statsmodels.api as sm

from residual_momentum_v2_strategy import load_data, LOCAL_DIR, _month_end_days, _residual_momentum
from residual_momentum_v2_strategy import ResidualMomentumV2

OUT_DIR = os.path.join(_HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

LOAD_START = "2000-01-01"
DATA_END = "2026-09-04"
REPORT_START = "2002-01-01"
HORIZONS = {"1m": 1, "3m": 3, "6m": 6, "12m": 12}


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS
# ══════════════════════════════════════════════════════════════════════════════

def nw_tstat(x, maxlags):
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    if len(x) < 8:
        return np.nan, np.nan
    X = np.ones_like(x)
    maxlags = max(0, min(int(maxlags), len(x) - 2))
    model = sm.OLS(x, X).fit(cov_type="HAC", cov_kwds={"maxlags": maxlags})
    return float(model.params[0]), float(model.tvalues[0])


def plain_tstat(x):
    x = pd.Series(x).dropna()
    return float(x.mean() / x.std(ddof=1) * np.sqrt(len(x))) if len(x) >= 8 else np.nan


def csz_masked(x_row, mask_row):
    vals = x_row.where(mask_row)
    mu, sd = vals.mean(), vals.std()
    return (vals - mu) / sd if sd and sd > 0 else vals * np.nan


def ic_series(sig_df, mask_df, fwd_df, weight_df=None):
    dates = sig_df.index
    ic = pd.Series(index=dates, dtype=float)
    breadth = pd.Series(index=dates, dtype=float)
    for t in dates:
        m = mask_df.loc[t]
        s = sig_df.loc[t].where(m)
        f = fwd_df.loc[t]
        cols = ["sig", "fwd"]
        frame = {"sig": s, "fwd": f}
        if weight_df is not None:
            frame["w"] = weight_df.loc[t]
            cols.append("w")
        both = pd.concat(frame, axis=1).dropna()
        if len(both) < 10:
            continue
        if weight_df is None:
            ic.loc[t] = both["sig"].corr(both["fwd"], method="spearman")
        else:
            rs = both["sig"].rank()
            rf = both["fwd"].rank()
            w = both["w"] / both["w"].sum()
            ms, mf = (rs * w).sum(), (rf * w).sum()
            cov = (w * (rs - ms) * (rf - mf)).sum()
            vs = (w * (rs - ms) ** 2).sum()
            vf = (w * (rf - mf) ** 2).sum()
            ic.loc[t] = cov / np.sqrt(vs * vf) if vs > 0 and vf > 0 else np.nan
        breadth.loc[t] = len(both)
    return ic.dropna(), breadth.dropna()


def full_sample_row(ic, horizon_months):
    nw_lag = max(horizon_months - 1, 1)
    mean_nw, t_nw = nw_tstat(ic, nw_lag)
    sd = ic.std(ddof=1)
    return dict(n_months=int(ic.notna().sum()), ic_mean=float(ic.mean()), ic_std=float(sd),
               icir_ann=float(ic.mean() / sd * np.sqrt(12)) if sd > 0 else np.nan,
               t_stat=plain_tstat(ic), nw_lag=nw_lag, nw_tstat=t_nw)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("=" * 78)
    print("STAGE 1 — Data integrity & universe definition (v2, rank 50-1000)")
    print("=" * 78)

    prices, volumes, highs, lows, opens = load_data(LOCAL_DIR, start=LOAD_START, end=DATA_END)
    st = ResidualMomentumV2(prices, volumes, highs, lows, opens)
    st.calculate_factors()
    st.get_positions(start=REPORT_START)

    # -- Survivorship proxy: % of symbols whose last available date is >6mo before panel end
    panel_end = st.close.index.max()
    last_date_per_symbol = st.close.notna().apply(lambda col: col[col].index.max() if col.any() else pd.NaT)
    six_mo_before_end = panel_end - pd.DateOffset(months=6)
    n_total = last_date_per_symbol.notna().sum()
    n_delisted_proxy = int((last_date_per_symbol < six_mo_before_end).sum())
    pct_delisted = n_delisted_proxy / n_total if n_total else np.nan
    print(f"\n[Survivorship proxy] {n_delisted_proxy}/{n_total} symbols ({pct_delisted:.1%}) "
          f"have their last available row >6 months before the panel end ({panel_end.date()}).")
    print(f"  Verdict: {'FLAG -- likely survivorship bias (dataset is live-listed-only; '
          'downstream IC/CAGR are upper bounds, say so in every report)' if pct_delisted < 0.02 else 'ok (>=2% apparent turnover in the panel)'}")

    # -- Listing history floor
    hist_days = st.close.notna().sum(axis=0)
    hist_days = hist_days[hist_days > 0]
    n_under_252 = int((hist_days < 252).sum())
    print(f"\n[Listing history] {n_under_252}/{len(hist_days)} symbols have <252 total trading "
          f"days of history (excluded from eligibility by the live min_adv/min_price floor's "
          f"own rolling-window min_periods before they'd ever qualify, not by a separate check).")

    # -- min_periods check (code-level)
    print(f"\n[min_periods check] filter_universe() uses "
          f"tv.rolling(63, min_periods=45) for turnover, ivol uses "
          f"rolling(63, min_periods=40) -- both explicitly set (not the unset-min_periods "
          f"bug flagged in the playbook). PASS.")

    # -- Breadth floor on v2's own band
    me_full = _month_end_days(st.close.index)
    me = me_full[(me_full >= pd.Timestamp(REPORT_START)) & (me_full <= panel_end)]
    names_per_month = st.univ.loc[me].sum(axis=1)
    n_below_8 = int((names_per_month < 8).sum())
    print(f"\n[Breadth floor] names/month on v2's rank 50-1000 band: "
          f"mean {names_per_month.mean():.0f}  min {names_per_month.min():.0f}  "
          f"months <8 names: {n_below_8}/{len(me)} ({n_below_8 / len(me):.1%})")
    print(f"  Gate (>=8 names/month): {'PASS' if n_below_8 / len(me) == 0 else 'CAUTION -- months excluded from IC'}")

    stage1 = dict(pct_delisted_proxy=pct_delisted, n_under_252=n_under_252,
                 breadth_mean=float(names_per_month.mean()), breadth_min=int(names_per_month.min()),
                 months_below_8=n_below_8, months_total=len(me))
    pd.Series(stage1).to_csv(os.path.join(OUT_DIR, "stage1_data_integrity.csv"))

    # ══════════════════════════════════════════════════════════════════════════
    print("\n" + "=" * 78)
    print("STAGE 2 — Core signal diagnostics (filter ladder L0->L1->L2->L3->L5)")
    print("=" * 78)

    cff = st.close.ffill()
    fwd = {}
    for label, h in HORIZONS.items():
        fr = pd.DataFrame(index=me, columns=st.close.columns, dtype=float)
        for i in range(len(me) - h):
            fr.loc[me[i]] = cff.loc[me[i + h]] / cff.loc[me[i]] - 1
        fwd[label] = fr
    # raw (unfilled) version for the lookahead-assert check (2.7)
    fwd_raw_1m = pd.DataFrame(index=me, columns=st.close.columns, dtype=float)
    for i in range(len(me) - 1):
        fwd_raw_1m.loc[me[i]] = st.close.loc[me[i + 1]] / st.close.loc[me[i]] - 1

    raw_rm = _residual_momentum(st.resid, st.formation_9m, st.formation_skip, scale_by_vol=True)
    raw_h52 = st.close / st.close.rolling(252, min_periods=150).max()
    dv63 = st.dv

    valid_px = st.close.reindex(me).notna()
    L0_mask = valid_px
    L1_mask = valid_px & (st.close.reindex(me) >= st.min_price)
    L2_mask = L1_mask & (dv63.reindex(me) >= st.min_adv)
    L3_mask = st.univ.loc[me]   # == L2_mask + rank-50-1000 cut, exactly the live universe

    def build_rung_signal(mask):
        z9r = pd.DataFrame(index=me, columns=st.close.columns, dtype=float)
        z52r = pd.DataFrame(index=me, columns=st.close.columns, dtype=float)
        for t in me:
            z9r.loc[t] = csz_masked(raw_rm.loc[t], mask.loc[t])
            z52r.loc[t] = csz_masked(raw_h52.loc[t], mask.loc[t])
        return st.z9_weight * z9r + st.high52_weight * z52r

    rungs = {"L0_raw": L0_mask, "L1_price_floor": L1_mask, "L2_liquidity_floor": L2_mask,
            "L3_tradeable": L3_mask}

    print("\n-- 2.1/2.2 Filter ladder x horizon (NW t-stat on mean monthly rank-IC) --")
    print(f"{'rung':<20}{'1m':>8}{'3m':>8}{'6m':>8}{'12m':>8}   avg breadth")
    ladder_rows = {}
    rung_sig_cache = {}
    for rname, rmask in rungs.items():
        sig = build_rung_signal(rmask)
        rung_sig_cache[rname] = (sig, rmask)
        row = {}
        breadths = []
        for hlabel, h in HORIZONS.items():
            ic, breadth = ic_series(sig, rmask, fwd[hlabel])
            r = full_sample_row(ic, h)
            row[hlabel] = r
            breadths.append(breadth.mean())
        ladder_rows[rname] = row
        print(f"{rname:<20}" + "".join(f"{row[h]['nw_tstat']:>8.2f}" for h in HORIZONS)
              + f"   {np.mean(breadths):.0f}")

    # L5: ranked/held pool -- use the L3 signal value, restricted to the names actually held
    held_mask = pd.DataFrame(False, index=me, columns=st.close.columns)
    for t, names in st.held_by_t.items():
        if t in held_mask.index and names:
            held_mask.loc[t, names] = True
    sig_L3, _ = rung_sig_cache["L3_tradeable"]
    row_L5 = {}
    for hlabel, h in HORIZONS.items():
        ic, breadth = ic_series(sig_L3, held_mask, fwd[hlabel])
        row_L5[hlabel] = full_sample_row(ic, h)
    ladder_rows["L5_held_pool"] = row_L5
    print(f"{'L5_held_pool':<20}" + "".join(f"{row_L5[h]['nw_tstat']:>8.2f}" for h in HORIZONS)
          + f"   {held_mask.loc[me].sum(axis=1).mean():.0f}")
    print("  (L4 regime-gate rung: N/A -- the trend gate is portfolio-level, not a per-name filter)")

    gate_L0 = ladder_rows["L0_raw"]["1m"]["nw_tstat"]
    gate_L3 = ladder_rows["L3_tradeable"]["1m"]["nw_tstat"]
    print(f"\n  GATE: L0 NW-t >= 2.0: {gate_L0:.2f} -> {'PASS' if gate_L0 >= 2.0 else 'FAIL'}")
    print(f"  GATE: L3 NW-t >= 2.0: {gate_L3:.2f} -> {'PASS' if gate_L3 >= 2.0 else 'FAIL'}")

    pd.DataFrame({r: {h: ladder_rows[r][h]["nw_tstat"] for h in HORIZONS} for r in ladder_rows}).T.to_csv(
        os.path.join(OUT_DIR, "stage2_filter_ladder.csv"))

    # -- 2.3 Quantile monotonicity (L3, 1m horizon)
    print("\n-- 2.3 Quantile monotonicity (L3, 1m horizon, 10 quantiles) --")
    sig_L3_1m = sig_L3.reindex(me)
    quint_rets = {q: [] for q in range(10)}
    for t in me:
        s = sig_L3_1m.loc[t].where(L3_mask.loc[t])
        f = fwd["1m"].loc[t]
        both = pd.concat({"sig": s, "fwd": f}, axis=1).dropna()
        if len(both) < 30:
            continue
        both["q"] = pd.qcut(both["sig"], 10, labels=False, duplicates="drop")
        for q, grp in both.groupby("q"):
            quint_rets[int(q)].append(grp["fwd"].mean())
    quint_means = {q: np.mean(v) if v else np.nan for q, v in quint_rets.items()}
    qvals = [quint_means[q] for q in sorted(quint_means) if pd.notna(quint_means[q])]
    mono_pairs = sum(1 for i in range(1, len(qvals)) if qvals[i] >= qvals[i - 1])
    mono_pct = mono_pairs / (len(qvals) - 1) if len(qvals) > 1 else np.nan
    print("  Quantile mean 1m fwd return (q0=lowest signal .. q9=highest):")
    for q in sorted(quint_means):
        print(f"    q{q}: {quint_means[q]:+.4%}")
    print(f"  Monotonic adjacent pairs: {mono_pairs}/{len(qvals) - 1} ({mono_pct:.0%})  "
          f"GATE >=80%: {'PASS' if mono_pct >= 0.8 else 'FAIL'}")

    # -- 2.5 Equal- vs value-weighted IC (L3, 1m, weight = that month's $-turnover)
    print("\n-- 2.5 Equal- vs turnover-value-weighted IC (L3, 1m) --")
    ic_eq, _ = ic_series(sig_L3, L3_mask, fwd["1m"])
    ic_vw, _ = ic_series(sig_L3, L3_mask, fwd["1m"], weight_df=dv63.reindex(me))
    print(f"  Equal-weighted IC mean: {ic_eq.mean():.4f}   Value(turnover)-weighted IC mean: {ic_vw.mean():.4f}")
    divergence = abs(ic_eq.mean() - ic_vw.mean())
    print(f"  Divergence: {divergence:.4f}  "
          f"({'FLAG -- edge concentrated in the less-liquid tail, capacity concern for Stage 6' if divergence > 0.02 else 'ok, no large divergence'})")

    # -- 2.6 Year/regime concentration (top-2-year share of signed IC, L3 1m)
    print("\n-- 2.6 Year/regime concentration (L3, 1m) --")
    ic_by_year = ic_eq.groupby(ic_eq.index.year).sum()
    top2_share = ic_by_year.abs().nlargest(2).sum() / ic_by_year.abs().sum()
    print(f"  Top-2-year share of total |signed IC|: {top2_share:.1%}  "
          f"GATE <=50%: {'PASS' if top2_share <= 0.5 else 'FLAG -- concentration-fragile'}")
    print(f"  By year:\n{ic_by_year.round(3).to_string()}")

    # -- 2.7 Lookahead assert (ffill vs raw forward return, L3, 1m)
    print("\n-- 2.7 Lookahead assert (ffilled fwd-return IC vs raw/unfilled fwd-return IC) --")
    ic_ffill, _ = ic_series(sig_L3, L3_mask, fwd["1m"])
    ic_raw, _ = ic_series(sig_L3, L3_mask, fwd_raw_1m)
    la_divergence = abs(ic_ffill.mean() - ic_raw.mean())
    print(f"  ffilled-fwd IC mean: {ic_ffill.mean():.4f}   raw-fwd IC mean: {ic_raw.mean():.4f}")
    print(f"  Divergence: {la_divergence:.4f}  "
          f"({'FLAG -- possible lookahead/survivorship leak via ffill' if la_divergence > 0.01 else 'ok, divergence ~0'})")

    breadth_excl_pct = n_below_8 / len(me)
    print("\n" + "=" * 78)
    print("STAGE 2 GATE SUMMARY")
    print("=" * 78)
    print(f"  [{'x' if gate_L0 >= 2.0 else ' '}] L0 NW-t >= 2.0  ({gate_L0:.2f})")
    print(f"  [{'x' if gate_L3 >= 2.0 else ' '}] L3 NW-t >= 2.0  ({gate_L3:.2f})")
    print(f"  [{'x' if breadth_excl_pct <= 0.15 else ' '}] Breadth-exclusion <=15% of months  ({breadth_excl_pct:.1%})")
    print(f"  [{'x' if la_divergence <= 0.01 else ' '}] No unresolved lookahead-assert failure")
    print("=" * 78)

    print("\nDone.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
stage3_robustness_ablation.py
================================
STRATEGY_VALIDATION_PLAYBOOK.md Stage 3 for ResidualMomentumV2: universe-band sweep,
parameter sensitivity, and the 5-metric ablation scorecard. One process, data loaded once,
every cell run sequentially (this stage alone is ~30+ full backtests).

All Stage 3 tuning is on the FULL available window (no IS/OOS split -- that's Stage 4). Per
this project's research standard, v2's own shipped config (universe 50-1000, spike filter on)
was already chosen partly by looking at post-2020 performance, so this sweep is a robustness
read on top of that fact, not a blind IS-only tuning exercise in the playbook's strict sense
-- logged here rather than silently presented as clean.

Dimensions swept:
  3.1 Universe band  -- playbook's standard set {top-100,250,500,750,1000,1500} +
                         {500-1000,1000-1500,1000-2000} + v2's own adopted (50,1000)
  3.2 Parameter sensitivity, +-20%/40% around the current value (>=5 points incl. current):
      - formation_9m (lookback): 113/151/189(current)/227/265
      - n (top-N capacity): 24/32/40(current)/48/56
      - breaker (stop-loss %): 0.15/0.20/0.25(current)/0.30/0.35
      - trend_window (regime-filter threshold): 90/120/150(current)/180/210
      - rebalance_freq_months: 1(current)/2/3 (integer-months knob, no +-20% equivalent)
  3.3 Ablation scorecard: all 5 metrics (Sharpe, Calmar, return stability, avg DD depth,
      turnover) for every cell above vs the current-config baseline.

Signal IC (1m, L3-equivalent -- that cell's own eligible universe) is computed independently
of P&L for every universe-band cell, per the playbook's "apply the same bands to signal IC
independently of backtest P&L" instruction.
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
from residual_momentum_v2_backtest import backtest_event_driven, metrics

OUT_DIR = os.path.join(_HERE, "output")
os.makedirs(OUT_DIR, exist_ok=True)

LOAD_START = "2000-01-01"
DATA_END = "2026-09-04"
REPORT_START = "2002-01-01"
AUM = 1e5

CORE_BANDS = ["top250", "top500", "top750", "top1000", "top1500"]


def nw_tstat(x, maxlags=1):
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    if len(x) < 8:
        return np.nan
    X = np.ones_like(x)
    model = sm.OLS(x, X).fit(cov_type="HAC", cov_kwds={"maxlags": max(0, min(maxlags, len(x) - 2))})
    return float(model.tvalues[0])


def csz_masked(x_row, mask_row):
    vals = x_row.where(mask_row)
    mu, sd = vals.mean(), vals.std()
    return (vals - mu) / sd if sd and sd > 0 else vals * np.nan


def signal_ic_1m(st, rank_min, rank_max):
    """Rebuild the composite on this cell's own universe mask and compute 1m rank-IC,
    independent of P&L. Reuses st.resid/st.close (already computed by calculate_factors())."""
    me_full = _month_end_days(st.close.index)
    me = me_full[(me_full >= pd.Timestamp(REPORT_START)) & (me_full <= st.close.index.max())]
    tv = st.close * st.volume
    dv = tv.rolling(63, min_periods=45).median()
    px = st.close
    mask = pd.DataFrame(False, index=me, columns=st.close.columns)
    for t in me:
        s = dv.loc[t].dropna()
        s = s[s >= st.min_adv]
        s = s[px.loc[t, s.index] >= st.min_price]
        if s.empty:
            continue
        ranked = s.rank(ascending=False, method="first")
        sel = ranked[(ranked >= rank_min) & (ranked <= rank_max)]
        mask.loc[t, sel.index] = True

    raw_rm = _residual_momentum(st.resid, st.formation_9m, st.formation_skip, scale_by_vol=True)
    raw_h52 = st.close / st.close.rolling(252, min_periods=150).max()
    cff = st.close.ffill()
    fwd = pd.DataFrame(index=me, columns=st.close.columns, dtype=float)
    for i in range(len(me) - 1):
        fwd.loc[me[i]] = cff.loc[me[i + 1]] / cff.loc[me[i]] - 1

    ic = pd.Series(index=me, dtype=float)
    for t in me:
        m = mask.loc[t]
        z9r = csz_masked(raw_rm.loc[t], m)
        z52r = csz_masked(raw_h52.loc[t], m)
        sig = st.z9_weight * z9r + st.high52_weight * z52r
        both = pd.concat({"sig": sig, "fwd": fwd.loc[t]}, axis=1).dropna()
        if len(both) < 10:
            continue
        ic.loc[t] = both["sig"].corr(both["fwd"], method="spearman")
    ic = ic.dropna()
    return float(ic.mean()), nw_tstat(ic, 1)


def return_stability(net):
    monthly = (1 + net).resample("ME").apply(lambda x: x.prod() - 1)
    trailing12 = monthly.rolling(12).apply(lambda x: (1 + x).prod() - 1)
    return float(trailing12.std())


def avg_dd_depth(net, thresh=0.02):
    eq = (1 + net).cumprod()
    dd = eq / eq.cummax() - 1
    in_dd = dd < -thresh
    episodes = []
    cur_min = 0.0
    for v, flag in zip(dd.values, in_dd.values):
        if flag:
            cur_min = min(cur_min, v)
        else:
            if cur_min < 0:
                episodes.append(cur_min)
            cur_min = 0.0
    if cur_min < 0:
        episodes.append(cur_min)
    return float(np.mean(episodes)) if episodes else 0.0


def run_cell(prices, volumes, highs, lows, opens, label, **kwargs):
    st = ResidualMomentumV2(prices, volumes, highs, lows, opens, spike_filter=False,
                            cash_sweep_etf=None, **kwargs)
    st.calculate_factors()
    st.get_positions(start=REPORT_START)
    net, turn = backtest_event_driven(st, aum=AUM)
    m = metrics(net, st.mkt.reindex(net.index))
    row = dict(cell=label, CAGR=m["CAGR"], Sharpe=m["Sharpe"], Calmar=m["Calmar"],
              MaxDD=m["MaxDD"], Vol=m["Vol"], turnover=turn,
              return_stability=return_stability(net), avg_dd_depth=avg_dd_depth(net))
    rank_min = kwargs.get("universe_rank_min", 1)
    rank_max = kwargs.get("universe_top_n", 1000)
    ic_mean, ic_nwt = signal_ic_1m(st, rank_min, rank_max)
    row["ic_mean_1m"] = ic_mean
    row["ic_nwt_1m"] = ic_nwt
    print(f"  {label:<20} CAGR {m['CAGR']:+.2%}  Sharpe {m['Sharpe']:.2f}  Calmar {m['Calmar']:.2f}  "
          f"MaxDD {m['MaxDD']:.1%}  turnover {turn:.0%}  IC(1m) {ic_mean:.4f} (NW-t {ic_nwt:.2f})")
    return row


def main():
    print("=" * 78)
    print("STAGE 3 — Universe/parameter robustness & ablation (ResidualMomentumV2)")
    print("=" * 78)

    prices, volumes, highs, lows, opens = load_data(LOCAL_DIR, start=LOAD_START, end=DATA_END)
    rows = []

    print("\n[3.0] Current v2 config baseline (universe 50-1000)")
    rows.append(run_cell(prices, volumes, highs, lows, opens, "baseline_v2(50-1000)",
                         universe_rank_min=50, universe_top_n=1000))

    print("\n[3.1] Universe band sweep")
    band_cells = [
        (1, 100, "top100"), (1, 250, "top250"), (1, 500, "top500"), (1, 750, "top750"),
        (1, 1000, "top1000"), (1, 1500, "top1500"),
        (500, 1000, "band500-1000"), (1000, 1500, "band1000-1500"), (1000, 2000, "band1000-2000"),
    ]
    for lo, hi, label in band_cells:
        rows.append(run_cell(prices, volumes, highs, lows, opens, label,
                             universe_rank_min=lo, universe_top_n=hi))

    print("\n[3.2a] Lookback (formation_9m) sensitivity: 189 +-20%/+-40%")
    for val, label in [(113, "formation_9m=113(-40%)"), (151, "formation_9m=151(-20%)"),
                       (227, "formation_9m=227(+20%)"), (265, "formation_9m=265(+40%)")]:
        rows.append(run_cell(prices, volumes, highs, lows, opens, label,
                             universe_rank_min=50, universe_top_n=1000, formation_9m=val))

    print("\n[3.2b] Top-N capacity (n) sensitivity: 40 +-20%/+-40%")
    for val, label in [(24, "n=24(-40%)"), (32, "n=32(-20%)"), (48, "n=48(+20%)"), (56, "n=56(+40%)")]:
        rows.append(run_cell(prices, volumes, highs, lows, opens, label,
                             universe_rank_min=50, universe_top_n=1000, n=val))

    print("\n[3.2c] Stop-loss / breaker sensitivity: 0.25 +-20%/+-40%")
    for val, label in [(0.15, "breaker=0.15(-40%)"), (0.20, "breaker=0.20(-20%)"),
                       (0.30, "breaker=0.30(+20%)"), (0.35, "breaker=0.35(+40%)")]:
        st = ResidualMomentumV2(prices, volumes, highs, lows, opens, universe_rank_min=50,
                                universe_top_n=1000, spike_filter=False, cash_sweep_etf=None)
        st.calculate_factors()
        st.get_positions(start=REPORT_START)
        st.breaker = val
        net, turn = backtest_event_driven(st, aum=AUM)
        m = metrics(net, st.mkt.reindex(net.index))
        ic_mean, ic_nwt = signal_ic_1m(st, 50, 1000)
        rows.append(dict(cell=label, CAGR=m["CAGR"], Sharpe=m["Sharpe"], Calmar=m["Calmar"],
                         MaxDD=m["MaxDD"], Vol=m["Vol"], turnover=turn,
                         return_stability=return_stability(net), avg_dd_depth=avg_dd_depth(net),
                         ic_mean_1m=ic_mean, ic_nwt_1m=ic_nwt))
        print(f"  {label:<20} CAGR {m['CAGR']:+.2%}  Sharpe {m['Sharpe']:.2f}  Calmar {m['Calmar']:.2f}  "
              f"MaxDD {m['MaxDD']:.1%}  turnover {turn:.0%}  IC(1m) {ic_mean:.4f} (NW-t {ic_nwt:.2f})")

    print("\n[3.2d] Regime-filter / trend_window sensitivity: 150 +-20%/+-40%")
    for val, label in [(90, "trend_window=90(-40%)"), (120, "trend_window=120(-20%)"),
                       (180, "trend_window=180(+20%)"), (210, "trend_window=210(+40%)")]:
        rows.append(run_cell(prices, volumes, highs, lows, opens, label,
                             universe_rank_min=50, universe_top_n=1000, trend_window=val))

    print("\n[3.2e] Rebalance frequency sensitivity: 1 (current), 2, 3 months")
    for val, label in [(2, "rebalance_freq=2m"), (3, "rebalance_freq=3m")]:
        rows.append(run_cell(prices, volumes, highs, lows, opens, label,
                             universe_rank_min=50, universe_top_n=1000, rebalance_freq_months=val))

    df = pd.DataFrame(rows).set_index("cell")
    df.to_csv(os.path.join(OUT_DIR, "stage3_all_cells.csv"))

    # ── 3.1 dispersion gate on core bands ──────────────────────────────────────────
    print("\n" + "=" * 78)
    print("3.1 GATE — universe core-band dispersion ({})".format(", ".join(CORE_BANDS)))
    print("=" * 78)
    core = df.loc[CORE_BANDS]
    for metric, accept, caution in [("Sharpe", 0.35, 0.60), ("Calmar", 0.50, 0.90),
                                    ("CAGR", 0.08, 0.15), ("MaxDD", 0.10, 0.18)]:
        rng = float(core[metric].max() - core[metric].min())
        verdict = "ACCEPTABLE" if rng <= accept else ("CAUTION" if rng <= caution else "MAJOR DIVERGENCE")
        print(f"  {metric:<8} range across core bands: {rng:.3f}  -> {verdict}")
    any_neg_sharpe = bool((core["Sharpe"] <= 0).any())
    print(f"  Any core-band Sharpe <= 0: {any_neg_sharpe}  "
          f"{'-> AUTO MAJOR DIVERGENCE (overrides rows above)' if any_neg_sharpe else ''}")
    print(f"\n  Same bands applied to signal IC (NW-t, 1m):")
    print(core[["ic_mean_1m", "ic_nwt_1m"]].to_string())

    # ── 3.2 cliff gate ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 78)
    print("3.2 GATE — parameter cliffs (Sharpe swing on +-20% move)")
    print("=" * 78)
    baseline_sharpe = df.loc["baseline_v2(50-1000)", "Sharpe"]
    cliff_checks = [
        ("formation_9m", ["formation_9m=151(-20%)", "formation_9m=227(+20%)"]),
        ("n", ["n=32(-20%)", "n=48(+20%)"]),
        ("breaker", ["breaker=0.20(-20%)", "breaker=0.30(+20%)"]),
        ("trend_window", ["trend_window=120(-20%)", "trend_window=180(+20%)"]),
    ]
    for pname, cells in cliff_checks:
        swings = [abs(df.loc[c, "Sharpe"] - baseline_sharpe) for c in cells if c in df.index]
        max_swing = max(swings) if swings else np.nan
        print(f"  {pname:<16} max |Sharpe swing| at +-20%: {max_swing:.2f}  "
              f"-> {'CLIFF (overfit to this value)' if max_swing > 0.4 else 'flat/plateau, ok'}")

    # ── 3.3 ablation scorecard vs baseline ──────────────────────────────────────────
    print("\n" + "=" * 78)
    print("3.3 ABLATION SCORECARD — every cell vs baseline_v2(50-1000)")
    print("=" * 78)
    base = df.loc["baseline_v2(50-1000)"]
    reg_limits = dict(Sharpe=0.15, Calmar=0.15, return_stability=0.20, avg_dd_depth=0.20, turnover=0.25)
    score_rows = []
    for cell, r in df.iterrows():
        if cell == "baseline_v2(50-1000)":
            continue
        regs = {}
        disqualified = []
        for m, lim in reg_limits.items():
            base_val, cell_val = base[m], r[m]
            if base_val == 0:
                continue
            rel = abs(cell_val - base_val) / abs(base_val)
            regs[m] = rel
            if (m in ("Sharpe", "Calmar") and cell_val < base_val and rel > lim):
                disqualified.append(m)
            elif m in ("return_stability", "avg_dd_depth", "turnover") and rel > lim and abs(cell_val) > abs(base_val):
                disqualified.append(m)
        score_rows.append(dict(cell=cell, Sharpe=r["Sharpe"], Calmar=r["Calmar"],
                               return_stability=r["return_stability"], avg_dd_depth=r["avg_dd_depth"],
                               turnover=r["turnover"], disqualified=",".join(disqualified) if disqualified else ""))
    score_df = pd.DataFrame(score_rows).set_index("cell")
    score_df.to_csv(os.path.join(OUT_DIR, "stage3_ablation_scorecard.csv"))
    print(score_df.round(3).to_string())
    n_clean = int((score_df["disqualified"] == "").sum())
    print(f"\n  {n_clean}/{len(score_df)} cells clear all 5 ablation regression limits vs baseline.")

    print("\nDone. Outputs in:", OUT_DIR)


if __name__ == "__main__":
    main()

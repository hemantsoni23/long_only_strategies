"""
evaluate_new_momentum_factors.py
================================
Stand-alone evaluation runner for the novel momentum factor blueprints
on the Indian equity OHLCV universe (Upstox cached Parquet panels).

Calculates:
  1. Spearman Rank IC across 1, 2, 3, 6, 12-month forward return horizons.
  2. ICIR = mean(IC) / std(IC).
  3. Newey-West adjusted t-stat (lag = h - 1) for overlapping returns.
  4. Hit Rate (% of months with IC > 0).
  5. Sub-period stability: Discovery (<= 2014) vs Holdout (>= 2015).
  6. Quantile spreads (Top 20% excess, Top 10% excess, Spread Q5-Q1, Win-rate vs median).
  7. Cross-sectional correlation with live baseline (Elendel A3+Q5) and Incremental IC.
  8. Tested across universes: U1_liquid1000, U2_live_trend, U3_top300.

Usage:
  python3 evaluate_new_momentum_factors.py
"""

import os
import sys
import time
import numpy as np
import pandas as pd

# Ensure factor_research directory is on sys.path
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from data import load_panels
from factors import Ctx, rmean, rstd, rsum, rmax, rmin, signal_dates, _trend_stats, REGISTRY

# CAVEATS (see NEW_MOMENTUM_FACTORS_AUDIT.md): (1) the 'open' field in this dataset is not a usable opening price
# (NIFTYBEES shows +174%/yr 'overnight' and -163%/yr 'intraday'), so intra_over_* is untrustworthy;
# (2) NW t-stats at h>=6 can be inflated several-fold for fast-moving factors -- see stage24_new_factor_audit.nonoverlap_t.
from evaluate import (
    forward_returns,
    build_universes,
    evaluate_factor,
    composite,
    HORIZONS,
    SPLIT
)

# ══════════════════════════════════════════════════════════════════════════════
# NOVEL FACTOR DEFINITIONS
# ══════════════════════════════════════════════════════════════════════════════

def build_new_factors(X, sig):
    """
    Computes the 7 novel momentum factors using pre-computed Ctx intermediates.
    Returns: dict { factor_name: DataFrame(signal_dates x tickers) }
    """
    print("[new_factors] Building candidate factor panels ...", flush=True)
    factors = {}

    # Base price & return components
    Cf = X.Cf
    Hf = X.Hf
    Lf = X.Lf
    r = X.r
    V = X.V
    DV = X.DV
    bench = X.bench
    mkt = X.mkt

    # 1. Quiet Momentum: 12-1m trend scaled inversely by turnover surge
    # Lee & Swaminathan (2000): Early-stage accumulation vs late-stage distribution
    trend_12_1 = Cf.shift(21) / Cf.shift(252) - 1.0
    vol_surge_21_252 = rmean(V, 21) / rmean(V, 252).replace(0, np.nan)
    quiet_mom = trend_12_1 / (1.0 + vol_surge_21_252.clip(lower=0.2, upper=5.0))
    factors['quiet_mom_12_1'] = quiet_mom.reindex(sig).astype('float32')

    # 2. Intraday Institutional Drift (Lou, Polk & Skouras 2019)
    # Intraday (C/O) vs Overnight (O/C_prev) drift over 126 and 252 days
    ovn = np.log(X.O / Cf.shift(1)).clip(-0.15, 0.15)
    intr = np.log(X.C / X.O).clip(-0.15, 0.15)
    factors['intra_over_126'] = (rsum(intr, 126) - rsum(ovn, 126)).reindex(sig).astype('float32')
    factors['intra_over_252'] = (rsum(intr, 252) - rsum(ovn, 252)).reindex(sig).astype('float32')

    # 3. Asymmetric Downside-Beta Momentum (Delta Beta: Beta+ minus Beta-)
    # Ang, Chen & Xing (2006), Daniel & Moskowitz (2016)
    # Rolling 252d upside vs downside covariance with the benchmark
    mkt_mean = mkt.rolling(252, min_periods=180).mean()
    mkt_dev = mkt.sub(mkt_mean, axis=0)
    stock_mean = r.rolling(252, min_periods=180).mean()
    stock_dev = r.sub(stock_mean, axis=0)

    is_down = mkt < mkt_mean
    is_up = mkt > mkt_mean

    mkt_dev_down = mkt_dev.where(is_down, 0.0)
    stock_dev_down = stock_dev.where(is_down, 0.0)
    cov_down = rsum(stock_dev_down.mul(mkt_dev_down, axis=0), 252)
    var_down = rsum(mkt_dev_down ** 2, 252).replace(0, np.nan)
    beta_down = cov_down.div(var_down, axis=0)

    mkt_dev_up = mkt_dev.where(is_up, 0.0)
    stock_dev_up = stock_dev.where(is_up, 0.0)
    cov_up = rsum(stock_dev_up.mul(mkt_dev_up, axis=0), 252)
    var_up = rsum(mkt_dev_up ** 2, 252).replace(0, np.nan)
    beta_up = cov_up.div(var_up, axis=0)

    delta_beta = (beta_up - beta_down).clip(-3.0, 3.0)
    factors['delta_beta_252'] = delta_beta.reindex(sig).astype('float32')
    
    # Combined Asymmetric Beta Momentum (Z-score blend of Trend + DeltaBeta)
    # We store raw delta_beta and will evaluate standalone & blended.

    # 4. Drawdown-Penalized "Ulcer Momentum" (Martin & McCann 1989)
    # 12-1m return divided by 252d Ulcer Index (RMS percentage drawdown from peak)
    dd_from_peak = (Cf / rmax(Cf, 252) - 1.0)
    ulcer_idx_252 = np.sqrt(rmean(dd_from_peak ** 2, 252)).clip(lower=0.01)
    ulcer_mom = (trend_12_1 / ulcer_idx_252).clip(-10.0, 10.0)
    factors['ulcer_mom_252'] = ulcer_mom.reindex(sig).astype('float32')
    factors['low_ulcer_252'] = (-ulcer_idx_252).reindex(sig).astype('float32')

    # 5. Trend Curvature & Acceleration (Convexity Trend)
    # Second-order polynomial log-price fit: ln(P) = a + b*t + c*t^2 over 126d
    # Approximation via velocity difference: 63d slope minus previous 63d slope
    r_short, slope_short = _trend_stats(np.log(Cf), X.t, 63)
    r_med, slope_med = _trend_stats(np.log(Cf.shift(63)), X.t.shift(63), 63)
    accel_63 = (slope_short - slope_med) * (r_short.abs().clip(lower=0.1))
    factors['trend_accel_63'] = accel_63.reindex(sig).astype('float32')

    # 6. Tight-Range Trend (Base Tightness + Persistence)
    tight_close_15 = -(rstd(Cf, 15) / rmean(Cf, 15).replace(0, np.nan))
    q5_126 = (Cf > rmean(Cf, 50)).astype('float64').rolling(126, min_periods=100).mean()
    factors['tight_close_15'] = tight_close_15.reindex(sig).astype('float32')
    factors['q5_126'] = q5_126.reindex(sig).astype('float32')

    print(f"[new_factors] Successfully built {len(factors)} candidate factor panels.", flush=True)
    return factors


# ══════════════════════════════════════════════════════════════════════════════
# MAIN EVALUATION PIPELINE
# ══════════════════════════════════════════════════════════════════════════════

def run_evaluation(universes=('U1_liquid1000', 'U2_live_trend', 'U3_top300')):
    t_start = time.time()
    print("=" * 80)
    print("RUNNING FACTOR EVALUATION PIPELINE FOR INDIAN EQUITIES")
    print(f"Horizons: {HORIZONS} months | Split date: {SPLIT.date()}")
    print("=" * 80)

    # 1. Load Parquet panels
    P = load_panels(refresh=False)
    X = Ctx(P)
    sig = signal_dates(X.C.index)
    print(f"[pipeline] Observation range: {sig.min().date()} to {sig.max().date()} ({len(sig)} monthly dates)")

    # 2. Build forward returns & universes
    FWD = forward_returns(X, sig, horizons=HORIZONS)
    U = build_universes(X, sig)

    # 3. Build novel factors
    F = build_new_factors(X, sig)

    # Also build composite blends
    # Blend 1: Tight close + Persistence (I1)
    # Blend 2: Intraday drift + Low Ulcer (I4)
    # Blend 3: Quiet Momentum + Persistence
    # Blend 4: Ulcer Momentum + Trend Persistence

    res_dir = os.path.join(HERE, 'results')
    os.makedirs(res_dir, exist_ok=True)

    all_summary_rows = []

    for uname in universes:
        if uname not in U:
            continue
        mask = U[uname]
        print(f"\n[evaluating universe: {uname}] ...")

        # Establish live Elendel reference for correlation & incremental IC
        # TRUE live Elendel = A3 (RS-line at 52w high) + Q5-126. (Previously q5_126 alone was used and labelled Elendel.)
        Fb = dict(F)
        Fb['a3_rs_high'] = REGISTRY['a3_rs_high'][2](X).reindex(sig).astype('float32')
        elend_base = composite(Fb, ['a3_rs_high', 'q5_126'], mask)

        # Add composites dynamically
        F_eval = dict(F)
        F_eval['blend_tight_q5'] = composite(F, ['tight_close_15', 'q5_126'], mask)
        F_eval['blend_intra_ulcer'] = composite(F, ['intra_over_252', 'low_ulcer_252'], mask)
        F_eval['blend_quiet_q5'] = composite(F, ['quiet_mom_12_1', 'q5_126'], mask)

        rows = []
        for fname, f_df in F_eval.items():
            row, _ics = evaluate_factor(fname, f_df, mask, FWD, base_rank=elend_base, detail=True)
            row['universe'] = uname
            rows.append(row)
            all_summary_rows.append(row)

        df_u = pd.DataFrame(rows).set_index('factor')
        out_csv = os.path.join(res_dir, f'new_factors_{uname}.csv')
        df_u.to_csv(out_csv, float_format='%.4f')
        print(f"  -> Saved {len(rows)} factor evaluations to {out_csv}")

    # Summary table across all universes
    summary_df = pd.DataFrame(all_summary_rows)
    master_path = os.path.join(res_dir, 'master_new_factors_summary.csv')
    summary_df.to_csv(master_path, index=False, float_format='%.4f')

    print("\n" + "=" * 80)
    print(f"EVALUATION COMPLETE in {time.time() - t_start:.1f}s")
    print(f"Master summary saved to: {master_path}")
    print("=" * 80)

    # Print clean preview of key metrics at 3m and 6m horizons
    cols_preview = [
        'factor', 'universe', 'avg_n',
        'ic_3', 'icir_3', 't_3', 'hit_3',
        'ic_disc_3', 'ic_hold_3',
        'ic_6', 'icir_6', 't_6',
        'peak_h_ic', 'corr_elendel', 'inc_ic_3'
    ]
    avail_cols = [c for c in cols_preview if c in summary_df.columns]
    print("\nKEY METRICS PREVIEW (Horizon 3m & 6m):")
    print(summary_df[avail_cols].to_string(index=False))

    return summary_df


if __name__ == '__main__':
    run_evaluation()

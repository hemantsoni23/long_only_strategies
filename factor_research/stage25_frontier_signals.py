"""Research OHLCV signals not covered by the existing 122-factor catalog.

The script deliberately freezes signal orientation before evaluation.  It reuses the
existing point-in-time monthly universes and T+1 forward-return construction.

Run:
    python3 factor_research/stage25_frontier_signals.py

Outputs:
    factor_research/.cache/stage25_factors.pkl
    factor_research/results/stage25_frontier_full.csv
    factor_research/results/stage25_frontier_summary.csv
    factor_research/results/stage25_frontier_yearly_ic.csv
"""
from __future__ import annotations

import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from data import load_panels
from evaluate import SPLIT, composite, evaluate_factor, nw_tstat, rank_ic
from factors import Ctx, rmean, rstd, rsum
from portfolio_lab import stats, topn_book

CACHE = os.path.join(HERE, ".cache")
RESULTS = os.path.join(HERE, "results")
os.makedirs(RESULTS, exist_ok=True)


def _at(df: pd.DataFrame, sig: pd.DatetimeIndex) -> pd.DataFrame:
    return df.reindex(sig).astype("float32")


def _price_delay(X: Ctx, sig: pd.DatetimeIndex) -> pd.DataFrame:
    """Hou-Moskowitz D1 using 52 weekly observations and four market lags.

    D1 = 1 - R2(contemporaneous market only) / R2(market plus four lags).
    Weekly closes are Friday-resampled.  A stock needs >=48 of 52 returns; the few
    remaining missing returns are replaced by zero only after this coverage gate.
    """
    wp = X.C.resample("W-FRI").last()
    wr = wp.pct_change(fill_method=None).clip(-0.40, 3.0)
    wm = X.mkt.resample("W-FRI").apply(lambda z: np.prod(1.0 + z) - 1.0)
    xall = pd.concat([wm.shift(k).rename(f"m{k}") for k in range(5)], axis=1)
    out = np.full((len(sig), wr.shape[1]), np.nan, dtype="float32")
    widx = wr.index
    for j, d in enumerate(sig):
        end = widx.searchsorted(d, side="right")
        beg = end - 52
        if beg < 4:
            continue
        Y = wr.iloc[beg:end].to_numpy(dtype="float64")
        X5 = xall.iloc[beg:end].to_numpy(dtype="float64")
        xok = np.isfinite(X5).all(axis=1)
        if xok.sum() < 48:
            continue
        Y = Y[xok]
        X5 = X5[xok]
        good = np.isfinite(Y).sum(axis=0) >= 48
        if not good.any():
            continue
        Yg = Y[:, good]
        means = np.nanmean(Yg, axis=0)
        Yg = np.where(np.isfinite(Yg), Yg, means)
        Yc = Yg - Yg.mean(axis=0)
        sst = (Yc * Yc).sum(axis=0)
        Xc = np.column_stack([np.ones(len(X5)), X5])
        b5 = np.linalg.pinv(Xc) @ Yg
        e5 = Yg - Xc @ b5
        r2_5 = 1.0 - (e5 * e5).sum(axis=0) / np.where(sst > 1e-12, sst, np.nan)
        X1 = Xc[:, :2]
        b1 = np.linalg.pinv(X1) @ Yg
        e1 = Yg - X1 @ b1
        r2_1 = 1.0 - (e1 * e1).sum(axis=0) / np.where(sst > 1e-12, sst, np.nan)
        delay = 1.0 - np.clip(r2_1, 0, None) / np.where(r2_5 > 1e-8, r2_5, np.nan)
        out[j, good] = np.clip(delay, 0.0, 1.0).astype("float32")
    return pd.DataFrame(out, index=sig, columns=wr.columns)


def build_factors(sig: pd.DatetimeIndex) -> dict[str, pd.DataFrame]:
    P = load_panels()
    X = Ctx(P)
    r = X.r.clip(-0.40, 3.0)
    m = X.mkt.clip(-0.40, 0.40)
    F: dict[str, pd.DataFrame] = {}

    # De Bondt-Thaler long-run reversal; the recent 12 months are excluded so this
    # is not merely the negative of ordinary momentum.
    F["longrev_36_13"] = _at(-(X.Cf.shift(273) / X.Cf.shift(756) - 1.0), sig)
    F["longrev_60_13"] = _at(-(X.Cf.shift(273) / X.Cf.shift(1260) - 1.0), sig)

    # Preference for less lottery-like / less extreme return distributions.
    F["low_kurt_252"] = _at(-r.rolling(252, min_periods=200).kurt(), sig)

    # Harvey-Siddique systematic coskewness.  Higher signal means more negative
    # coskewness (the a-priori direction associated with a positive risk premium).
    w = 252
    er = r.rolling(w, min_periods=200).mean()
    em = m.rolling(w, min_periods=200).mean()
    em2 = (m * m).rolling(w, min_periods=200).mean()
    erm = r.mul(m, axis=0).rolling(w, min_periods=200).mean()
    erm2 = r.mul(m * m, axis=0).rolling(w, min_periods=200).mean()
    cov_r_m2 = erm2.sub(er.mul(em2, axis=0)).sub(erm.mul(2 * em, axis=0)).add(
        er.mul(2 * em * em, axis=0)
    )
    denom = rstd(r, w).mul(m.rolling(w, min_periods=200).var(), axis=0)
    F["neg_coskew_252"] = _at(-(cov_r_m2 / denom.replace(0, np.nan)), sig)

    # Return sensitivity specifically on the market's worst rolling-quintile days.
    # Higher = the stock historically lost less in market-tail observations.
    q20 = m.rolling(252, min_periods=200).quantile(0.20)
    crash = m.le(q20)
    crash_sum = r.where(crash, axis=0).rolling(252, min_periods=40).sum()
    crash_scale = m.abs().where(crash).rolling(252, min_periods=40).sum()
    F["tail_resilience_252"] = _at(crash_sum.div(crash_scale, axis=0), sig)

    # Stock-level Amihud shock.  Scale is irrelevant because the signal is ranked.
    ami = r.abs() / X.DV.replace(0, np.nan)
    liq_shock = rmean(ami, 21) / rmean(ami, 252).replace(0, np.nan)
    F["illiq_shock_21_252"] = _at(np.log(liq_shock.clip(1e-3, 1e3)), sig)
    recent5 = X.Cf / X.Cf.shift(5) - 1.0
    F["liqshock_reversal_5"] = _at(-recent5 * np.log(liq_shock.clip(lower=1.0)), sig)

    # Participation stability and staleness: distinct from dollar-volume level.
    logdv = np.log(X.DV.replace(0, np.nan))
    F["stable_dvol_63"] = _at(-rstd(logdv, 63), sig)
    stale = (r.abs() < 1e-8).astype(float).where(r.notna())
    F["low_stale_63"] = _at(-rmean(stale, 63), sig)

    F["price_delay_52w"] = _price_delay(X, sig)
    return F


def main() -> None:
    t0 = time.time()
    state = pickle.load(open(os.path.join(CACHE, "state.pkl"), "rb"))
    sig, old, fwd, universes = state["sig"], state["F"], state["FWD"], state["U"]
    F = build_factors(sig)
    pickle.dump(F, open(os.path.join(CACHE, "stage25_factors.pkl"), "wb"))

    rows = []
    yearly = []
    for uname in ("U1_liquid1000", "U2_live_trend", "U3_top300"):
        mask = universes[uname]
        elen = composite(old, ["a3_rs_high", "q5_126"], mask)
        for name, frame in F.items():
            row, store = evaluate_factor(name, frame, mask, fwd, base_rank=elen)
            row["universe"] = uname
            ic3 = store[3].dropna()
            row["t3_nw"] = nw_tstat(ic3, 2)
            row["accuracy3"] = (ic3 > 0).mean()
            # A simple top-15 diagnostic, same stripped monthly engine as prior scans.
            book = topn_book(frame, mask, fwd[1])
            net = book["net"]
            all_s = stats(net)
            hold_s = stats(net[net.index > SPLIT])
            row["book_sharpe"] = all_s.get("sharpe")
            row["book_sharpe_hold"] = hold_s.get("sharpe")
            row["book_cagr"] = all_s.get("cagr")
            row["book_maxdd"] = all_s.get("maxdd")
            row["book_turnover"] = book["turnover"].mean()
            rows.append(row)
            for year, value in ic3.groupby(ic3.index.year).mean().items():
                yearly.append({"universe": uname, "factor": name, "year": year, "ic3": value})
        print(f"[stage25] evaluated {uname}", flush=True)

    full = pd.DataFrame(rows)
    full.to_csv(os.path.join(RESULTS, "stage25_frontier_full.csv"), index=False)
    cols = [
        "universe", "factor", "avg_n", "ic_1", "ic_3", "icir_3", "accuracy3", "t3_nw",
        "ic_6", "ic_12", "peak_h_ic", "ic_disc_3", "ic_hold_3", "t_hold_3",
        "top10_ex_3", "top20_ex_3", "top20_winmed_3", "corr_elendel", "inc_ic_3",
        "rank_autocorr_1m", "book_cagr", "book_sharpe", "book_sharpe_hold", "book_maxdd",
        "book_turnover",
    ]
    summary = full[[c for c in cols if c in full.columns]].copy()
    summary.to_csv(os.path.join(RESULTS, "stage25_frontier_summary.csv"), index=False)
    pd.DataFrame(yearly).to_csv(os.path.join(RESULTS, "stage25_frontier_yearly_ic.csv"), index=False)
    print(summary.to_string(index=False))
    print(f"[stage25] done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()

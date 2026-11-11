"""Robustness and add-on tests for the pre-oriented stage-25 frontier signals."""
from __future__ import annotations

import os
import pickle
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from evaluate import SPLIT, composite, nw_tstat, rank_ic, winsor_rows, zscore
from portfolio_lab import stats, topn_book

CACHE = os.path.join(HERE, ".cache")
RES = os.path.join(HERE, "results")


def nonoverlap_t(x: pd.Series, h: int) -> float:
    vals = []
    for off in range(h):
        y = x.iloc[off::h].dropna()
        if len(y) > 8 and y.std() > 0:
            vals.append(y.mean() / (y.std() / np.sqrt(len(y))))
    return float(np.mean(vals)) if vals else np.nan


def residual_ic(f: pd.DataFrame, base: pd.DataFrame, ret: pd.DataFrame) -> pd.Series:
    fp, bp = f.rank(axis=1, pct=True), base.rank(axis=1, pct=True)
    fz = fp.sub(fp.mean(axis=1), axis=0)
    bz = bp.sub(bp.mean(axis=1), axis=0)
    beta = (fz * bz).sum(axis=1) / (bz * bz).sum(axis=1)
    return rank_ic(fz.sub(bz.mul(beta, axis=0)), ret)[0].dropna()


def main() -> None:
    state = pickle.load(open(os.path.join(CACHE, "state.pkl"), "rb"))
    new = pickle.load(open(os.path.join(CACHE, "stage25_factors.pkl"), "rb"))
    old, fwd, U = state["F"], state["FWD"], state["U"]
    diagnostic = []
    quintiles = []
    for uname in ("U1_liquid1000", "U2_live_trend", "U3_top300"):
        mask = U[uname]
        elen = composite(old, ["a3_rs_high", "q5_126"], mask)
        for name, raw in new.items():
            f = raw.where(mask)
            row = {"universe": uname, "factor": name}
            for h in (1, 3, 6, 12):
                ic = rank_ic(f, fwd[h].where(mask))[0].dropna()
                row[f"ic{h}"] = ic.mean()
                row[f"t{h}_nw"] = nw_tstat(ic, h - 1)
                row[f"t{h}_nonoverlap"] = nonoverlap_t(ic, h)
                row[f"hit{h}"] = (ic > 0).mean()
            ric = residual_ic(f, elen, fwd[3].where(mask))
            row["inc_ic3_elen"] = ric.mean()
            row["inc_t3_elen"] = nw_tstat(ric, 2)
            ic3 = rank_ic(f, fwd[3].where(mask))[0].dropna()
            yr = ic3.groupby(ic3.index.year).mean()
            row["years_positive"] = (yr > 0).mean()
            row["ic3_2015plus"] = ic3[ic3.index > SPLIT].mean()
            row["t3_2015plus"] = nw_tstat(ic3[ic3.index > SPLIT], 2)
            row["ic3_2019plus"] = ic3[ic3.index >= "2019-01-01"].mean()
            row["t3_2019plus"] = nw_tstat(ic3[ic3.index >= "2019-01-01"], 2)
            diagnostic.append(row)

            R = fwd[3].where(mask)
            valid = f.notna() & R.notna()
            pct = f.where(valid).rank(axis=1, pct=True)
            rw = winsor_rows(R.where(valid))
            ex = rw.sub(rw.mean(axis=1), axis=0)
            qrow = {"universe": uname, "factor": name}
            for q in range(1, 6):
                lo, hi = (q - 1) / 5, q / 5
                s = ex.where((pct > lo) & (pct <= hi)).mean(axis=1).dropna()
                qrow[f"q{q}_ex3"] = s.mean()
                qrow[f"q{q}_t"] = nw_tstat(s, 2)
            quintiles.append(qrow)

    pd.DataFrame(diagnostic).to_csv(os.path.join(RES, "stage25_robustness.csv"), index=False)
    pd.DataFrame(quintiles).to_csv(os.path.join(RES, "stage25_quintiles.csv"), index=False)

    # Add-on tests are intentionally limited to the three signals that cleared or
    # approached the IC hurdle in at least one broad/large-cap universe.
    mask = U["U2_live_trend"]
    bases = {
        "elendel": composite(old, ["a3_rs_high", "q5_126"], mask),
        "zenith": composite(old, ["a1_52wh", "q5_189"], mask),
    }
    picks = ("low_kurt_252", "tail_resilience_252", "price_delay_52w")
    books = []
    for bn, base in bases.items():
        variants = [("base", 0.0, base)]
        for name in picks:
            for w in (0.25, 0.50, 1.00):
                variants.append((name, w, zscore(base) + w * zscore(new[name].where(mask))))
        for name, w, score in variants:
            b = topn_book(score, mask, fwd[1])
            all_s = stats(b.net)
            d_s = stats(b.net[b.index <= SPLIT])
            h_s = stats(b.net[b.index > SPLIT])
            books.append({
                "base": bn, "factor": name, "w": w,
                "sharpe_all": all_s.get("sharpe"), "sharpe_disc": d_s.get("sharpe"),
                "sharpe_hold": h_s.get("sharpe"), "cagr_all": all_s.get("cagr"),
                "maxdd_all": all_s.get("maxdd"), "turnover": b.turnover.mean(),
            })
    books = pd.DataFrame(books)
    for bn in bases:
        b0 = books[(books.base == bn) & (books.factor == "base")].iloc[0]
        ix = books.base == bn
        for c in ("sharpe_all", "sharpe_disc", "sharpe_hold"):
            books.loc[ix, "delta_" + c] = books.loc[ix, c] - b0[c]
    books.to_csv(os.path.join(RES, "stage25_addon_books.csv"), index=False)

    # Natural one-sided safety filters: remove the bottom factor quintile, then
    # rank the survivors on the untouched live base.  This tests whether the IC
    # comes from avoiding fragile names rather than selecting the highest scores.
    filters = []
    for bn, base in bases.items():
        for name in ("low_kurt_252", "tail_resilience_252", "price_delay_52w"):
            pct = new[name].where(mask).rank(axis=1, pct=True)
            for cutoff in (0.10, 0.20, 0.30):
                gated = mask & (pct > cutoff)
                b = topn_book(base, gated, fwd[1])
                sa = stats(b.net); sd = stats(b.net[b.index <= SPLIT]); sh = stats(b.net[b.index > SPLIT])
                filters.append({"base": bn, "factor": name, "exclude_bottom": cutoff,
                                "sharpe_all": sa.get("sharpe"), "sharpe_disc": sd.get("sharpe"),
                                "sharpe_hold": sh.get("sharpe"), "cagr_all": sa.get("cagr"),
                                "maxdd_all": sa.get("maxdd"), "turnover": b.turnover.mean()})
    filters = pd.DataFrame(filters)
    filters.to_csv(os.path.join(RES, "stage25_filter_books.csv"), index=False)
    print(pd.DataFrame(diagnostic).query("universe == 'U2_live_trend'").to_string(index=False))
    print(books.to_string(index=False))
    print(filters.to_string(index=False))


if __name__ == "__main__":
    main()

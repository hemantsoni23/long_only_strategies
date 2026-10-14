"""PREREG_GOLD2.md post-look #1: untimed metal weight cap grid, then timing/tilt/silver comparisons at the recommended weight."""
import os, numpy as np, pandas as pd, gold_common as gc
from gold_study2 import *
W = [0.025, 0.05, 0.075, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 1.0]
def run2(daily, cg, cs, target, w_good, w_bad, timing="none", silver=False, cost=0.0015):
    cal = daily.index; rb = daily["eq"].pct_change().fillna(0.0).to_numpy(); idle = (1.0 - daily.expo).shift(1).fillna(1.0).clip(lower=0).to_numpy(); n = len(cal)
    badreg = (daily.bear | daily.panic).to_numpy().astype(bool); rg = scen_returns(cg, "GOLDBEES", target); rs = scen_returns(cs, "SILVERBEES", target)
    s_avail = np.array(cal >= cs["first"] + pd.Timedelta(days=330)); sg, ss = cg["ssma"], cs["ssma"]
    capv = np.where(badreg, w_bad, w_good); tot = rb.copy(); curg = curs = 0.0; traded = 0.0; wsum = 0.0; vg = cg["valid"]; vs = cs["valid"] & s_avail
    for t in range(n):
        gate_g = sg[t] if timing == "sma" else 1.0; gate_s = ss[t] if timing == "sma" else 1.0
        if silver and s_avail[t]: tg_ = min(idle[t], capv[t]) * 0.5 * gate_g; ts_ = min(idle[t], capv[t]) * 0.5 * gate_s
        else: tg_ = min(idle[t], capv[t]) * gate_g; ts_ = 0.0
        tg = tg_ if vg[t] else 0.0; ts = ts_ if vs[t] else 0.0
        cg0 = min(curg, idle[t]) if vg[t] else 0.0; cs0 = min(curs, max(idle[t] - cg0, 0.0)) if vs[t] else 0.0
        ng = tg if abs(tg - cg0) > DEADBAND else cg0; ns = ts if abs(ts - cs0) > DEADBAND else cs0
        tr = abs(ng - curg) + abs(ns - curs); traded += tr; curg, curs = ng, ns; tot[t] = rb[t] + curg * rg[t] + curs * rs[t] - cost * tr; wsum += curg + curs
    yrs = (cal[-1] - cal[0]).days / 365.25
    return pd.Series(tot, index=cal), wsum / n * 100, traded / yrs * 100
SC = {"4%": 0.04, "8%": 0.08, "FULL": FULL, "REAL": None}
def grid():
    out = []
    for cap in CAPS:
        for off in ANCH:
            d = pd.read_csv(os.path.join(DIRS[f"B0_{cap}|{off}"], "daily.csv"), index_col=0, parse_dates=True); cg = ctx("GOLDBEES", d.index); cs = ctx("SILVERBEES", d.index)
            out.append(dict(cap=cap, anchor=off, spec="G0", scen="-", w=0.0, avg_w=0.0, turn=0.0, **m0(d["eq"].pct_change().dropna())))
            for w in W:
                for sn, tg in SC.items():
                    r, aw, tr = run2(d, cg, cs, tg, w, w); out.append(dict(cap=cap, anchor=off, spec=f"U{w}", scen=sn, w=w, avg_w=aw, turn=tr, **m0(r.iloc[1:])))
    return pd.DataFrame(out)
def dl(df, cap, spec, sn, base="G0"):
    g = df[(df.cap == cap) & (df.spec == spec) & (df.scen == sn)].set_index("anchor"); b = df[(df.cap == cap) & (df.spec == base)].set_index("anchor") if base == "G0" else df[(df.cap == cap) & (df.spec == base) & (df.scen == sn)].set_index("anchor")
    return dict(dSh0=(g.Sh0 - b.Sh0).mean(), dA=(g.Sh0_A - b.Sh0_A).mean(), dB=(g.Sh0_B - b.Sh0_B).mean(), pos=int(((g.Sh0 - b.Sh0) > 0).sum()), dDD=(g.MaxDD - b.MaxDD).mean(), dCAGR=(g.CAGR - b.CAGR).mean(), dCalmar=(g.Calmar - b.Calmar).mean(), avg_w=g.avg_w.mean(), turn=g.turn.mean())
if __name__ == "__main__":
    df = grid(); df.to_csv("gold2_sizing_raw.csv", index=False)
    rows = []
    for w in W:
        for cap in CAPS:
            for sn in SC: rows.append(dict(w=w, cap=cap, scen=sn, **dl(df, cap, f"U{w}", sn)))
    T = pd.DataFrame(rows); T.to_csv("gold2_sizing_table.csv", index=False)
    for sn in ["8%", "4%"]:
        print(f"\n=== untimed weight cap grid, scenario {sn}: dSh0 | dCAGR | dMaxDD | dCalmar by book size ==="); 
        for m in ["dSh0", "dCAGR", "dDD", "dCalmar"]: print(m); print(T[T.scen == sn].pivot(index="w", columns="cap", values=m)[CAPS].round(3).to_string())
    print("\nREAL scenario dSh0:"); print(T[T.scen == "REAL"].pivot(index="w", columns="cap", values="dSh0")[CAPS].round(3).to_string())
    ok = []
    for w in W:
        a = T[(T.w == w) & (T.scen == "8%")]; b = T[(T.w == w) & (T.scen == "4%")]
        q = bool((a.dSh0 >= 0).all() and (a.dCalmar >= 0).all() and (a.dDD >= -3).all() and (a.dA > 0).all() and (a.dB > 0).all() and (b.dSh0 >= -0.03).all()); ok.append(q)
    print("\nweights meeting the recommendation rule:", {w: q for w, q in zip(W, ok)}); wstar = max([w for w, q in zip(W, ok) if q], default=None); print("w* =", wstar)
    if wstar is not None:
        rows = []
        for cap in CAPS:
            for off in ANCH:
                d = pd.read_csv(os.path.join(DIRS[f"B0_{cap}|{off}"], "daily.csv"), index_col=0, parse_dates=True); cg = ctx("GOLDBEES", d.index); cs = ctx("SILVERBEES", d.index)
                for sn in ["4%", "8%", "FULL"]:
                    tg = SC[sn]
                    for nm, kw in [("untimed", dict(w_good=wstar, w_bad=wstar)), ("trend-gated", dict(w_good=wstar, w_bad=wstar, timing="sma")), ("bear-tilt", dict(w_good=wstar / 2, w_bad=2 * wstar)), ("gold+silver", dict(w_good=wstar, w_bad=wstar, silver=True))]:
                        r, aw, tr = run2(d, cg, cs, tg, **kw); rows.append(dict(cap=cap, anchor=off, spec=nm, scen=sn, avg_w=aw, turn=tr, **m0(r.iloc[1:])))
        C = pd.DataFrame(rows); C.to_csv("gold2_wstar_compare.csv", index=False)
        print(f"\n=== comparisons at w* = {wstar} (vs untimed, scenario 8% unless noted) ===")
        for nm in ["trend-gated", "bear-tilt", "gold+silver"]:
            for sn in ["8%", "4%"]:
                r = [dict(cap=cap, **dl(C, cap, nm, sn, base="untimed")) for cap in CAPS]; print(f"\n{nm} vs untimed, {sn}:"); print(pd.DataFrame(r).set_index("cap")[["dSh0", "dA", "dB", "pos", "dDD", "dCAGR", "dCalmar", "avg_w"]].round(3).to_string())

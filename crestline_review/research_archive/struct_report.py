"""Reports for PREREG_STRUCT.md: T1 staggering (blends of anchor equity curves), T2/T3 single-variant gates, T4 capacity gates."""
import os, sys, json, numpy as np, pandas as pd
pd.set_option("display.width", 250)
RF = (1.065) ** (1 / 252) - 1
def mt(r):
    yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod(); f = lambda x: (x.mean() - RF) / x.std() * np.sqrt(252)
    return dict(CAGR=(eq.iloc[-1] ** (1 / yrs) - 1) * 100, Sh65=f(r), MaxDD=(eq / eq.cummax() - 1).min() * 100, Sh65_A=f(r[:"2014-12-31"]), Sh65_B=f(r["2015-01-01":]))
def eqs(tag):
    dirs = json.load(open(f"dirs_struct_{tag}.json")); out = {}
    for k, d in dirs.items():
        v, a = k.split("|"); out.setdefault(v, {})[int(a)] = pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
    return out
# ---------------- T1
def stagger():
    E = eqs("books"); A = sorted(next(iter(E.values())).keys()); start = max(E[v][a].index[0] for v in E for a in A)
    N = {v: {a: E[v][a][start:] / E[v][a][start:].iloc[0] for a in A} for v in E}
    single = {v: pd.DataFrame([mt(N[v][a].pct_change().dropna()) for a in A]).mean() for v in N}
    def blend(v, K):
        out = []
        for g in range(60 // 5 // K):
            anchors = [A[g + j * (12 // K)] for j in range(K)]; out.append(mt(pd.concat([N[v][a] for a in anchors], axis=1).mean(axis=1).pct_change().dropna()))
        return pd.DataFrame(out)
    print(f"common window {start.date()} .. {E['N25'][0].index[-1].date()}\n\nSINGLE BOOKS (mean of 12 anchors):"); print(pd.DataFrame(single).T.round(2).to_string())
    res = {}
    for v, K in [("N25", 2), ("N25", 3), ("N25", 4), ("N25", 6), ("N25", 12), ("N8", 3), ("N4", 6)]: res[(v, K)] = blend(v, K)
    rows = [dict(book=v, K=K, groups=len(b), **b.mean().to_dict()) for (v, K), b in res.items()]
    print("\nBLENDS (K sub-accounts of 1/K capital):"); print(pd.DataFrame(rows).round(2).to_string(index=False))
    def cmp(name, bl, sg):
        d = bl.Sh65 - single[sg].Sh65; ok = (d.mean() >= 0.08) and (d > 0).all() and ((bl.Sh65_A - single[sg].Sh65_A).mean() > 0) and ((bl.Sh65_B - single[sg].Sh65_B).mean() > 0) and (bl.MaxDD.mean() - single[sg].MaxDD >= -3)
        print(f"{name}: blend Sh65 {bl.Sh65.mean():.2f} vs single {single[sg].Sh65:.2f}  d {d.mean():+.3f}  groups+ {(d>0).sum()}/{len(d)}  dP_A {(bl.Sh65_A - single[sg].Sh65_A).mean():+.2f} dP_B {(bl.Sh65_B - single[sg].Sh65_B).mean():+.2f}  CAGR {bl.CAGR.mean():.1f} vs {single[sg].CAGR:.1f}  MaxDD {bl.MaxDD.mean():.1f} vs {single[sg].MaxDD:.1f}  -> {'PASS' if ok else 'fail'}")
        return ok
    print("\nQ1 (GATED: staggering at constant total names, vs single N24):"); q3 = cmp("K=3 x N8 ", res[("N8", 3)], "N24"); q6 = cmp("K=6 x N4 ", res[("N4", 6)], "N24"); print("Q1 verdict:", "PASS (both)" if (q3 and q6) else "NOT PASSED")
    print("\nQ2 (descriptive: stagger vs buying the breadth directly):"); cmp("K=3 x N25 vs single N75 ", res[("N25", 3)], "N75"); cmp("K=6 x N25 vs single N150", res[("N25", 6)], "N150")
    print("\nQ0 (descriptive: stagger vs single N25):"); [cmp(f"K={K} x N25 vs single N25", res[("N25", K)], "N25") for K in [2, 3, 4, 6, 12]]
# ---------------- generic gate table vs a base within a results csv
def gates(csv, base, label_filter=None, fam=None):
    st = pd.read_csv(csv); b = st[st.variant == base].set_index("offset"); rows = []
    for v, g in st.groupby("variant", sort=False):
        g = g.set_index("offset"); d = g.sh65 - b.sh65
        rows.append(dict(variant=v, CAGR=g.cagr.mean(), dCAGR=g.cagr.mean() - b.cagr.mean(), Sh65=g.sh65.mean(), dSh65=d.mean(), dPA=(g.sh65_h1 - b.sh65_h1).mean(), dPB=(g.sh65_h2 - b.sh65_h2).mean(), pos=int((d > 0).sum()),
                         MDD=g.mdd.mean(), dMDD=g.mdd.mean() - b.mdd.mean(), expo=g.expo.mean(), turn=g.turn.mean()))
    t = pd.DataFrame(rows).set_index("variant"); t["pass"] = (t.dSh65 >= 0.08) & (t.dPA > 0) & (t.dPB > 0) & (t.pos >= 5) & (t.dMDD >= -3); t.loc[base, "pass"] = False; return t
if __name__ == "__main__":
    what = sys.argv[1]
    if what == "stagger": stagger()
    if what == "sing": print(gates("results_struct_sing.csv", "B").round(2).to_string())
    if what == "cap":
        for c in ["c1", "c5", "c20"]:
            st = pd.read_csv("results_struct_cap.csv"); sub = st[st.variant.str.endswith("_" + c)].copy(); sub["variant"] = sub.variant.str.replace("_" + c, ""); sub.to_csv(f"diag/_cap_{c}.csv", index=False)
            print(f"\n== capital {c} (full window) =="); print(gates(f"diag/_cap_{c}.csv", "B").round(2).to_string())

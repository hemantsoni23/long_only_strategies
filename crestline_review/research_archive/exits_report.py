"""Applies PREREG_EXITS.md rules N1-N6."""
import sys, numpy as np, pandas as pd
pd.set_option("display.width", 250)
st = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "results_exits.csv"); mech = pd.read_csv("results_exits_mech.csv", index_col=0)
b = st[st.variant == "B"].set_index("offset"); rows = []
for v, g in st.groupby("variant", sort=False):
    g = g.set_index("offset"); d = g.sh65 - b.sh65
    rows.append(dict(variant=v, CAGR=g.cagr.mean(), dCAGR=g.cagr.mean() - b.cagr.mean(), Sh65=g.sh65.mean(), dSh65=d.mean(), dPA=(g.sh65_h1 - b.sh65_h1).mean(), dPB=(g.sh65_h2 - b.sh65_h2).mean(),
                     pos=int((d > 0).sum()), MDD=g.mdd.mean(), dMDD=g.mdd.mean() - b.mdd.mean(), expo=g.expo.mean(), turn=g.turn.mean()))
t = pd.DataFrame(rows).set_index("variant").join(mech[["hold_d", "capture", "reentry_pct", "sa_cata", "trades"]])
t["N1"] = t.dSh65 >= 0.08; t["N2"] = (t.dPA > 0) & (t.dPB > 0); t["N3"] = t.pos >= 5; t["N4"] = t.dMDD >= -3.0
bh, bc = t.loc["B", "hold_d"], t.loc["B", "capture"]
fam = lambda v: v[:2]
t["N5"] = [(r.hold_d >= 1.10 * bh and r.capture >= bc + 3) if fam(v) in ("SA", "PW") else (r.reentry_pct >= 5 if fam(v) == "RE" else True) for v, r in t.iterrows()]
t["N14"] = t.N1 & t.N2 & t.N3 & t.N4
t["N6"] = [(t[[fam(x) == fam(v) and x != "B" for x in t.index]].N14.sum() >= 2) if fam(v) in ("SA", "RE", "PW") else True for v in t.index]
t["status"] = np.where(t.N14 & t.N5 & t.N6, "ADOPT-ELIGIBLE", np.where(t.N14 & t.N5, "isolated", np.where(t.N14, "N5 fails", np.where((t.dCAGR >= 1.5) & (t.dSh65 < 0.08), "risk-dial", "-"))))
t.loc["B", "status"] = "base"
cols = ["CAGR", "dCAGR", "Sh65", "dSh65", "dPA", "dPB", "pos", "MDD", "dMDD", "expo", "hold_d", "capture", "reentry_pct", "sa_cata", "status"]
print(t[cols].round(2).to_string())
pref = {"SA": ["SA1", "SA3", "SA2", "SA4"], "RE": ["RE2", "RE1", "RE3"], "PW": ["PW3", "PW1", "PW4", "PW2"], "PN": ["PN1"]}
adopt = {}
for f, order in pref.items():
    for v in order:
        if t.loc[v, "status"] == "ADOPT-ELIGIBLE" or (f == "PN" and t.loc[v, "N14"]): adopt[f] = v; break
print("\nADOPTED per family (closest to base among eligible):", adopt)
t.to_csv("exits_table.csv")

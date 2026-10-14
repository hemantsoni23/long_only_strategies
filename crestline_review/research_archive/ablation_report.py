"""Applies PREREG_ABLATION.md rules A1-A5 to results_ablation.csv."""
import re, sys, numpy as np, pandas as pd
pd.set_option("display.width", 250); pd.set_option("display.max_rows", 500)
df = pd.read_csv(sys.argv[1] if len(sys.argv) > 1 else "results_ablation.csv")
b = df[df.variant == "base"].set_index("offset")
rows = []
for v, g in df.groupby("variant", sort=False):
    if v == "base": continue
    g = g.set_index("offset"); d = g.sh65 - b.sh65
    rows.append(dict(variant=v, CAGR=g.cagr.mean(), dCAGR=g.cagr.mean() - b.cagr.mean(), Sh65=g.sh65.mean(), dSh65=d.mean(), dPA=(g.sh65_h1 - b.sh65_h1).mean(),
                     dPB=(g.sh65_h2 - b.sh65_h2).mean(), pos=int((d > 0).sum()), MDD=g.mdd.mean(), dMDD=g.mdd.mean() - b.mdd.mean(), expo=g.expo.mean(), turn=g.turn.mean()))
t = pd.DataFrame(rows).set_index("variant")
t["A1"] = t.dSh65 >= 0.08; t["A2"] = (t.dPA > 0) & (t.dPB > 0); t["A3"] = t.pos >= 5; t["A4"] = t.dMDD >= -3.0
# A5 plateau: next grid value on the far side of base must be >= 0
def param_of(v): return re.split(r"[=|]", v)[0]
def val_of(v):
    x = v.split("=", 1)[1]; m = re.findall(r"[-\d.]+", x); return float(m[-1]) if "(" in x else float(x)
basev = {"TOP_N": 15, "EXIT_RANK_MULT": 2, "REBALANCE_FREQ_DAYS": 60, "HP_WINDOW": 252, "TP_LOOKBACK": 189, "TP_SMA_WINDOW": 50, "HARD_STOP_PCT": .20, "PEAK_STOP_PCT": .15,
         "VOLSTOP_K": 2.5, "VOLSTOP_CLIP": .25, "BEAR_SCALE": .6, "PANIC_SCALE": .3, "PANIC_PCTL": .95, "BENCH_SMA": 200, "MIN_PRICE": 20, "UNIVERSE_TOP_N_MAX": 1000, "MAX_CIRCUIT_DAYS": 5, "COST_ONE_WAY": .003}
t["A5"] = True; t["param"] = [param_of(v) if "=" in v else "ablation" for v in t.index]
for p, bv in basev.items():
    sub = t[t.param == p]
    if sub.empty: continue
    vals = sorted([(val_of(v), v) for v in sub.index])
    for i, (x, v) in enumerate(vals):
        far = [vv for xx, vv in vals if (xx > x if x > bv else xx < x)]
        if far:
            nxt = far[0] if x > bv else far[-1]
            t.loc[v, "A5"] = t.loc[nxt, "dSh65"] >= 0
t["adopt"] = t.A1 & t.A2 & t.A3 & t.A4 & t.A5
t["status"] = np.where(t.adopt, "ADOPT", np.where(t.A1 & t.A2 & t.A3 & t.A4, "spike", np.where((t.dCAGR >= 1.5) & (t.dSh65 < 0.08) & (t.dSh65 > -0.08), "risk-dial", "-")))
t.loc[t.param == "COST_ONE_WAY", "status"] = "info"; t.loc[t.param == "ablation", "status"] = "ablation"
cols = ["CAGR", "dCAGR", "Sh65", "dSh65", "dPA", "dPB", "pos", "MDD", "dMDD", "expo", "turn", "status"]
bs = b.mean(numeric_only=True)
print(f"BASE: CAGR {bs.cagr:.2f} Sh0 {bs.sh0:.2f} Sh65 {bs.sh65:.2f} MaxDD {bs.mdd:.2f} expo {bs.expo:.1f} turn {bs.turn:.0f}  (P_A {bs.sh65_h1:.2f} / P_B {bs.sh65_h2:.2f})\n")
print("== PART 1: component ablation (negative dSh65 = the component helps) =="); print(t[t.param == "ablation"][cols].round(2).to_string())
for p in basev:
    sub = t[t.param == p]
    if sub.empty: continue
    sub = sub.assign(_x=[val_of(v) for v in sub.index]).sort_values("_x")
    rng = np.r_[sub.Sh65.values, bs.sh65]
    print(f"\n== {p} (base {basev[p]}) :  Sh65 range over grid {rng.min():.2f} .. {rng.max():.2f} =="); print(sub[cols].round(2).to_string())
print("\n== ADOPTED / SPIKE / RISK-DIAL =="); print(t[t.status.isin(["ADOPT", "spike", "risk-dial"])][cols].sort_values("dSh65", ascending=False).round(2).to_string())
t.to_csv("ablation_table.csv")

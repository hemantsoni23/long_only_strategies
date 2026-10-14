import os, json, numpy as np, pandas as pd, anchor_report as ar
import gold_study2 as g2, gold_sizing_study as gs
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
dl = lambda d: pd.read_csv(os.path.join(d, "daily.csv"), index_col=0, parse_dates=True); ok_all = True
def check(n, ok, det=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + n + (" -- " + det if det else ""))
V24 = os.path.join(ar.HERE, "crestline_v2_4.py"); V25 = os.path.join(ar.HERE, "crestline_v2_5.py")
def run(script, ovr, off): ar.SCRIPT = script; return ar.run_anchor(ovr, off, cache=False)
for off in [0, 30]:
    ref = eq(run(V24, {}, off)); a = eq(run(V25, {"CASH_RATE_ANNUAL": 0.065, "GOLD_CAP": 0}, off)); check(f"1. v2.5 with GOLD_CAP=0 and 6.5% cash == v2.4 (anchor {off})", np.allclose(a.values, ref.values, rtol=0, atol=1e-9))
DIRS0 = json.load(open("dirs_gold2_engine.json"))
for off in [0, 20, 40]:
    for nm, tgt, ov in [("real", None, {}), ("8%", 0.08, {"GOLD_TARGET_RET": 0.08})]:
        d = run(V25, ov, off); nat = dl(d); r_nat = nat["eq"].pct_change().dropna()
        base = pd.read_csv(os.path.join(DIRS0[f"B0_c0|{off}"], "daily.csv"), index_col=0, parse_dates=True); cg = g2.ctx("GOLDBEES", base.index); cs = g2.ctx("SILVERBEES", base.index)
        r_post, w_post, _ = gs.run2(base, cg, cs, tgt, 0.25, 0.25)
        j = r_nat.index.intersection(r_post.index); c = np.corrcoef(r_nat[j], r_post[j])[0, 1]
        cg_ = lambda r: ((1 + r).prod() ** (365.25 / (r.index[-1] - r.index[0]).days) - 1) * 100
        check(f"2. native sleeve vs post-processing, anchor {off}, gold {nm}", c >= 0.999 and abs(cg_(r_nat[j]) - cg_(r_post[j])) <= 0.30, f"daily corr {c:.5f}; CAGR native {cg_(r_nat[j]):.2f}% vs post {cg_(r_post[j]):.2f}%; avg gold wt {nat.gold_w.mean()*100:.1f}% vs {w_post:.1f}%")
d = run(V25, {}, 0); nat = dl(d)
check("3. no gold held in the 2011-14 data gap", (nat.gold_w["2011-01-01":"2014-12-31"] == 0).all() and nat.gold_w.max() > 0.1, f"max gold weight {nat.gold_w.max()*100:.1f}%")
check("4. stock exposure + gold weight never exceed 100% of equity; gold weight stays near its cap", ((nat.expo + nat.gold_w) <= 1.0 + 1e-6).all() and nat.gold_w.max() <= 0.25 * 1.35, f"max (expo+gold) {(nat.expo+nat.gold_w).max()*100:.1f}%")
full = eq(run(V25, {}, 0)); part = eq(run(V25, {"END_DATE": "2019-12-31"}, 0)); j = part.index.intersection(full.index)
check("5. truncation at 2019-12-31 leaves earlier equity unchanged", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
base = pd.read_csv(os.path.join(DIRS0["B0_c0|0"]), "daily.csv") if False else pd.read_csv(os.path.join(DIRS0["B0_c0|0"], "daily.csv"), index_col=0, parse_dates=True)
fl = dl(run(V25, {"GOLD_FLAT": True, "GOLD_COST": 0.0}, 0)); jj = base.index.intersection(fl.index)
check("6. frozen gold price + zero cost: native equity equals the no-gold book exactly", np.allclose(fl["eq"][jj].values, base["eq"][jj].values, rtol=1e-9))
o = run(V25, {"GOLD_FILL": "open"}, 0); c_ = run(V25, {}, 0)
cg_ = lambda r: ((1 + r).prod() ** (365.25 / (r.index[-1] - r.index[0]).days) - 1) * 100
check("7. previous-close fills are the default and are NOT more flattering than open fills", cg_(dl(c_)["eq"].pct_change().dropna()) <= cg_(dl(o)["eq"].pct_change().dropna()) + 1e-9, f"close fills {cg_(dl(c_)['eq'].pct_change().dropna()):.2f}% vs open fills {cg_(dl(o)['eq'].pct_change().dropna()):.2f}%")
print("\nALL PASS" if ok_all else "\nSOME FAILED")

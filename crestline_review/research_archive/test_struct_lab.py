import os, numpy as np, pandas as pd, anchor_report as ar
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
tr = lambda d: pd.read_csv(os.path.join(d, "trade_log_full.csv")); ok_all = True
def check(n, ok, det=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + n + (" -- " + det if det else ""))
V24 = os.path.join(ar.HERE, "crestline_v2_4.py"); LAB = os.path.join(ar.HERE, "crestline_struct_lab.py")
def run(script, ovr, off): ar.SCRIPT = script; return ar.run_anchor(ovr, off, cache=False)
for off in [0, 30]:
    ref = eq(run(V24, {}, off)); a = eq(run(LAB, {}, off)); check(f"1. struct lab defaults == v2.4 (anchor {off})", np.allclose(a.values, ref.values, rtol=0, atol=1e-9))
base = run(LAB, {}, 0); bt = tr(base)
d = run(LAB, {"SIZE_MODE": 1}, 0); t = tr(d); check("2. SIZE_MODE=1 changes entry weights (non-uniform)", t.Intended_Weight.std() > 1e-4 and abs(t.Intended_Weight.mean() / bt.Intended_Weight.mean() - 1) < 0.04, f"weight mean {bt.Intended_Weight.mean():.4f} -> {t.Intended_Weight.mean():.4f}, std {bt.Intended_Weight.std():.4f} -> {t.Intended_Weight.std():.4f}")
d = run(LAB, {"SIZE_MODE": 2, "VS_LO": 0.33, "VS_HI": 2.0}, 0); t = tr(d); check("3. SIZE_MODE=2 high-vol names get smaller weights", np.corrcoef(t.Intended_Weight, t.ATR_At_Entry / t.Entry_Price)[0, 1] < -0.2, f"corr(weight, ATR%) = {np.corrcoef(t.Intended_Weight, t.ATR_At_Entry / t.Entry_Price)[0,1]:.2f}")
d = run(LAB, {"RS_SUP": 0.05}, 0); t = tr(d); check("4. RS_SUP: RS_CATA exits appear, hold lengthens", (t.Exit_Reason == "RS_CATA").sum() > 0 and t.Holding_Days.mean() > bt.Holding_Days.mean(), f"RS_CATA {(t.Exit_Reason=='RS_CATA').sum()}, hold {bt.Holding_Days.mean():.1f}->{t.Holding_Days.mean():.1f}")
c = {"INITIAL_CAPITAL": 5e7}; b5 = run(LAB, c, 0); w5 = run(LAB, dict(c, CAPWALK_DEPTH=3), 0)
s5 = pd.read_json(os.path.join(b5, "summary.json"), typ="series"); sw = pd.read_json(os.path.join(w5, "summary.json"), typ="series")
check("5. CAPWALK raises exposure when the ADV cap binds (5 cr)", sw["m"]["AvgExpo"] > s5["m"]["AvgExpo"] + 3, f"exposure {s5['m']['AvgExpo']:.1f} -> {sw['m']['AvgExpo']:.1f}")
full = eq(run(LAB, {"CAPWALK_DEPTH": 3, "INITIAL_CAPITAL": 5e7, "SIZE_MODE": 1, "RS_SUP": 0.05}, 0)); part = eq(run(LAB, {"CAPWALK_DEPTH": 3, "INITIAL_CAPITAL": 5e7, "SIZE_MODE": 1, "RS_SUP": 0.05, "END_DATE": "2019-12-31"}, 0))
j = part.index.intersection(full.index); check("6. truncation at 2019-12-31 leaves earlier equity unchanged (all features on)", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
print("\nALL PASS" if ok_all else "\nSOME FAILED")

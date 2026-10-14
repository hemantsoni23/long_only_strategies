import os, json, numpy as np, pandas as pd, anchor_report as ar
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
tr = lambda d: pd.read_csv(os.path.join(d, "trade_log_full.csv"), parse_dates=["Entry_Date", "Exit_Date"]); sm = lambda d: json.load(open(os.path.join(d, "summary.json")))
ok_all = True
def check(n, ok, det=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + n + (" -- " + det if det else ""))
V25 = os.path.join(ar.HERE, "crestline_v2_5.py"); V26 = os.path.join(ar.HERE, "crestline_v2_6.py")
def run(script, ovr, off): ar.SCRIPT = script; return ar.run_anchor(ovr, off, cache=False)
cg = lambda r: ((1 + r).prod() ** (365.25 / (r.index[-1] - r.index[0]).days) - 1) * 100
for off in [0, 30]:
    ref = eq(run(V25, {}, off)); a = eq(run(V26, {"EXIT_MODE": "honest"}, off)); check(f"1. EXIT_MODE=honest == v2.5 bit-exact (anchor {off})", np.allclose(a.values, ref.values, rtol=0, atol=1e-9))
dz = run(V26, {"EXIT_MODE": "zenith"}, 0); dr = run(V26, {"EXIT_MODE": "resting"}, 0); dh = run(V26, {"EXIT_MODE": "honest"}, 0)
tz, trs = tr(dz), tr(dr); stz = tz[tz.Exit_Reason.isin(["HARD_STOP", "PEAK_STOP", "VOLSTOP"])]; strs = trs[trs.Exit_Reason.isin(["HARD_STOP", "PEAK_STOP", "VOLSTOP"])]
check("2. zenith: stop exits are BOOKED at the previous close (Exit_Price == Close_At_Exit) while the logged fill is lower", np.allclose(stz.Exit_Price, stz.Close_At_Exit) and (stz.Fill_Logged <= stz.Close_At_Exit + 1e-9).mean() > 0.95, f"{len(stz)} stops; logged fill below prev close in {(stz.Fill_Logged < stz.Close_At_Exit).mean()*100:.0f}% (mean fill vs prev close {((stz.Fill_Logged/stz.Close_At_Exit-1).mean())*100:.2f}%)")
intr = np.isclose(stz.Fill_Logged, stz.Stop_Price_At_Exit * 0.997, rtol=1e-6)
check("3. zenith fills never above the stop level; intraday breaches fill at level x (1 - 0.3%), gaps at the open (<= level)", (stz.Fill_Logged <= stz.Stop_Price_At_Exit + 1e-9).all() and intr.mean() > 0.4, f"{intr.mean()*100:.0f}% of stops filled at level x 0.997, {100-intr.mean()*100:.0f}% at a gap-through open")
check("4. no stop exit on the entry day", (stz.Exit_Date > stz.Entry_Date).all())
check("5. resting: booked at the fill (Exit_Price == Fill_Logged)", np.allclose(strs.Exit_Price, strs.Fill_Logged))
hz, hr, hh = sm(dz)["hidden_pct_yr"], sm(dr)["hidden_pct_yr"], sm(dh)["hidden_pct_yr"]
check("6. hidden (unbooked) exit P&L: zenith negative and material, resting ~0, honest 0", hz < -1.0 and abs(hr) < 1e-9 and abs(hh) < 1e-9, f"zenith {hz:.2f}%/yr, resting {hr:.2f}, honest {hh:.2f}")
r_z, r_r, r_h = [eq(d).pct_change().dropna() for d in (dz, dr, dh)]
check("7. ordering of CAGR: zenith (convention) >= resting (gap charged)", cg(r_z) >= cg(r_r), f"zenith {cg(r_z):.2f}%  resting {cg(r_r):.2f}%  honest {cg(r_h):.2f}%")
full = eq(run(V26, {}, 0)); part = eq(run(V26, {"END_DATE": "2019-12-31"}, 0)); j = part.index.intersection(full.index)
check("8. no look-ahead: truncation at 2019-12-31 leaves earlier equity unchanged (zenith mode)", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
print("\nALL PASS" if ok_all else "\nSOME FAILED")

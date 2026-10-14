"""Parity and mechanism tests for crestline_exits_lab.py (python3 test_exits_lab.py)."""
import os, json, numpy as np, pandas as pd, anchor_report as ar
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
tr = lambda d: pd.read_csv(os.path.join(d, "trade_log_full.csv"))
ok_all = True
def check(n, ok, det=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + n + (" -- " + det if det else ""))
V24 = os.path.join(ar.HERE, "crestline_v2_4.py"); LAB = os.path.join(ar.HERE, "crestline_exits_lab.py")
def run(script, ovr, off):
    ar.SCRIPT = script; return ar.run_anchor(ovr, off, cache=False)
for off in [0, 30]:
    ref = eq(run(V24, {}, off))
    a = eq(run(LAB, {}, off)); check(f"1. lab defaults == v2.4 (anchor {off})", np.allclose(a.values, ref.values, rtol=0, atol=1e-9), f"maxdiff {np.abs(a.values-ref.values).max():.1e}")
    b = eq(run(LAB, {"MON_FREQ_DAYS": 5}, off)); check(f"2. monitor grid on, no feature == v2.4 (anchor {off})", np.allclose(b.values, ref.values, rtol=0, atol=1e-9), f"maxdiff {np.abs(b.values-ref.values).max():.1e}")
base_t = tr(run(LAB, {"MON_FREQ_DAYS": 5}, 0))
d = run(LAB, {"MON_FREQ_DAYS": 5, "SA_RANK": 25, "SA_CATA_PCT": 0.25}, 0); t = tr(d)
check("3. SA: SA_CATA exits appear and the mean hold lengthens", (t.Exit_Reason == "SA_CATA").sum() > 0 and t.Holding_Days.mean() > base_t.Holding_Days.mean(), f"SA_CATA exits {(t.Exit_Reason=='SA_CATA').sum()}  mean hold {base_t.Holding_Days.mean():.1f} -> {t.Holding_Days.mean():.1f} days")
d = run(LAB, {"MON_FREQ_DAYS": 5, "RE_RANK": 25, "RE_COOLDOWN": 5}, 0); t = tr(d)
check("4. RE: more entries than baseline", len(t) > len(base_t), f"trades {len(base_t)} -> {len(t)}")
d = run(LAB, {"PW_GAIN": 0.15, "PW_MULT": 2.0}, 0); t = tr(d)
check("5. PW: mean hold lengthens", t.Holding_Days.mean() > base_t.Holding_Days.mean(), f"{base_t.Holding_Days.mean():.1f} -> {t.Holding_Days.mean():.1f}")
# 6. no look-ahead from the monitor ranks: truncating the sample must not change earlier equity
full = eq(run(LAB, {"MON_FREQ_DAYS": 5, "SA_RANK": 25, "RE_RANK": 25}, 0)); part = eq(run(LAB, {"MON_FREQ_DAYS": 5, "SA_RANK": 25, "RE_RANK": 25, "END_DATE": "2019-12-31"}, 0))
j = part.index.intersection(full.index); check("6. truncation at 2019-12-31 leaves earlier equity unchanged (SA+RE on)", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
print("\nALL PASS" if ok_all else "\nSOME FAILED")

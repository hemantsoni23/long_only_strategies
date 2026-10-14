"""Regression tests for crestline_v2_3.py  (python3 test_v2_3.py).  Each run is a full backtest (~30 s)."""
import os, sys, json, numpy as np, pandas as pd
import anchor_report as ar
HERE = ar.HERE
ORIG = os.path.join(HERE, "..", "Crestine", "crestline_v2_2.py")
ok_all = True
def check(name, ok, detail=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + name + ("  -- " + detail if detail else ""))
def eq(d): return pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
def trades(d): return pd.read_csv(os.path.join(d, "trade_log_full.csv"))

# 1. fixes OFF == colleague's original, bit for bit (original is copied to a temp dir and run there; Crestine/ is never written to)
import subprocess, tempfile, shutil
td = tempfile.mkdtemp(); shutil.copy(ORIG, os.path.join(td, "orig.py"))
subprocess.run([sys.executable, "orig.py"], cwd=td, capture_output=True)
ref = os.path.join(td, "crestline_v2_2_output")
legacy = ar.run_anchor({"CA_ADJUST": False, "CASH_RATE_ANNUAL": 0.0, "START_DATE": "2015-01-01"}, 0, cache=False)
a, b = eq(legacy), eq(ref)
check("1. v2.3 with fixes off reproduces v2.2 equity curve exactly", len(a) == len(b) and np.allclose(a.values, b.values, rtol=0, atol=1e-6), f"n={len(a)} maxdiff={float(np.abs(a.values-b.values).max()):.2e}")
check("1b. ... and the trade log (same count, same tickers/exits)", len(trades(legacy)) == len(trades(ref)) and (trades(legacy).Ticker.values == trades(ref).Ticker.values).all())

# 2. split-neutrality: no position may take a split-sized loss
raw = ar.run_anchor({"CA_ADJUST": False}, 0, cache=False); fx = ar.run_anchor({}, 0, cache=False)
tr_raw, tr_fx = trades(raw), trades(fx)
n_raw = int((tr_raw.Net_PnL_Pct < -60).sum()); n_fx = int((tr_fx.Net_PnL_Pct < -60).sum())
check("2. trades losing >60% net: masked engine has them, adjusted engine has none", n_raw >= 5 and n_fx == 0, f"masked={n_raw} adjusted={n_fx}")
hs_raw = tr_raw[tr_raw.Exit_Reason == "HARD_STOP"].Net_PnL_Pct.mean(); hs_fx = tr_fx[tr_fx.Exit_Reason == "HARD_STOP"].Net_PnL_Pct.mean()
check("3. average hard-stop loss is stop-sized (> -35%) after the fix", hs_fx > -35, f"masked avg {hs_raw:.1f}%  adjusted avg {hs_fx:.1f}%  (n={int((tr_fx.Exit_Reason=='HARD_STOP').sum())})")

# 4. accounting: fixed baseline equals the lab's corrected engine used for the study
import runner
from experiments import V
d_lab = runner.run(V(CA_ADJUST=True), 0)
check("4. v2.3 defaults == lab (CA_ADJUST, cash 6.5%, start 2006) used in REVIEW.md", np.allclose(eq(fx).values, eq(d_lab).values, rtol=0, atol=1e-6))
# 5. no look-ahead introduced by the adjustment: truncating the data after a date must not change earlier equity
cut = ar.run_anchor({"END_DATE": "2019-12-31"}, 0, cache=False)
full, part = eq(fx), eq(cut); j = part.index.intersection(full.index)
check("5. truncating the sample at 2019-12-31 leaves the earlier equity curve unchanged (no look-ahead from back-adjustment)", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6), f"{len(j)} common days")
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

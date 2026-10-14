"""Tests for crestline_v2_6.py.   python3 test_crestline.py            (behaviour tests, ~3 min)
                           python3 test_crestline.py --parity   (+ bit-exact parity against the frozen pre-cleanup reference research_archive/crestline_v2_6_precleanup.py, if present, ~8 min)
Each backtest is a separate process (config via CL_OVR, output via CL_OUT, schedule anchor via CRESTLINE_OFFSET)."""
import os, sys, json, subprocess, tempfile, hashlib
import numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__)); SCRIPT = os.path.join(HERE, "crestline_v2_6.py")
REF = next((p for p in (os.path.join(HERE, "research_archive", "crestline_v2_6_precleanup.py"),) if os.path.exists(p)), None)
TMP = tempfile.mkdtemp(prefix="crestline_test_"); ok_all = True
def check(name, ok, detail=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + name + (("  -- " + detail) if detail else ""), flush=True)
def run(script, ovr, off=0):
    d = os.path.join(TMP, hashlib.md5(json.dumps([script, ovr, off], sort_keys=True).encode()).hexdigest()[:12])
    if not os.path.exists(os.path.join(d, "summary.json")):
        os.makedirs(d, exist_ok=True)
        env = dict(os.environ, CL_OVR=json.dumps(ovr), CL_OUT=d, CRESTLINE_OFFSET=str(off), OMP_NUM_THREADS="1")
        r = subprocess.run([sys.executable, script], env=env, capture_output=True, text=True)
        if r.returncode: raise RuntimeError(r.stderr[-600:])
    return d
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
dl = lambda d: pd.read_csv(os.path.join(d, "daily.csv"), index_col=0, parse_dates=True)
tr = lambda d: pd.read_csv(os.path.join(d, "trade_log_full.csv"), parse_dates=["Entry_Date", "Exit_Date"])
sm = lambda d: json.load(open(os.path.join(d, "summary.json")))
cg = lambda r: ((1 + r).prod() ** (365.25 / (r.index[-1] - r.index[0]).days) - 1) * 100

# 0. configuration guard
r = subprocess.run([sys.executable, SCRIPT], env=dict(os.environ, CL_OVR='{"SIZE_MODE": 1}'), capture_output=True, text=True)
check("0. a removed switch is rejected (no silent no-op overrides)", r.returncode != 0 and "unknown override" in (r.stdout + r.stderr))
r = subprocess.run([sys.executable, SCRIPT], env=dict(os.environ, CL_OVR='{"EXIT_MODE": "bogus"}'), capture_output=True, text=True)
check("0b. EXIT_MODE is validated", r.returncode != 0)

modes = {m: run(SCRIPT, {"EXIT_MODE": m}) for m in ("zenith", "resting", "honest")} if False else None
with ThreadPoolExecutor(4) as ex:
    futs = {m: ex.submit(run, SCRIPT, {"EXIT_MODE": m}) for m in ("zenith", "resting", "honest")}
    futs["trunc"] = ex.submit(run, SCRIPT, {"END_DATE": "2019-12-31"}); futs["nogold"] = ex.submit(run, SCRIPT, {"GOLD_CAP": 0.0, "EXIT_MODE": "honest"})
    D = {k: f.result() for k, f in futs.items()}
tz, trs, th = tr(D["zenith"]), tr(D["resting"]), tr(D["honest"])
stz = tz[tz.Exit_Reason.isin(["PEAK_STOP", "VOLSTOP"])]; strs = trs[trs.Exit_Reason.isin(["PEAK_STOP", "VOLSTOP"])]
check("1. zenith: stop exits are BOOKED at the previous close while the logged fill is lower", np.allclose(stz.Exit_Price, stz.Close_At_Exit) and (stz.Fill_Logged <= stz.Close_At_Exit + 1e-9).mean() > 0.95, f"{len(stz)} stops, mean fill vs previous close {((stz.Fill_Logged/stz.Close_At_Exit-1).mean())*100:.2f}%")
intr = np.isclose(stz.Fill_Logged, stz.Stop_Price_At_Exit * 0.997, rtol=1e-6)
check("2. zenith fills never above the stop level; intraday breaches fill at level x (1 - 0.3%), gaps at the open", (stz.Fill_Logged <= stz.Stop_Price_At_Exit + 1e-9).all() and intr.mean() > 0.4, f"{intr.mean()*100:.0f}% at level x 0.997")
check("3. no stop exit on the entry day (all modes)", (stz.Exit_Date > stz.Entry_Date).all() and (strs.Exit_Date > strs.Entry_Date).all() and (th.Exit_Date > th.Entry_Date).all())
check("4. resting: booked at the fill", np.allclose(strs.Exit_Price, strs.Fill_Logged))
hz, hr, hh = sm(D["zenith"])["hidden_pct_yr"], sm(D["resting"])["hidden_pct_yr"], sm(D["honest"])["hidden_pct_yr"]
check("5. unbooked exit P&L: zenith negative and material, resting and honest zero", hz < -1.0 and abs(hr) < 1e-9 and abs(hh) < 1e-9, f"zenith {hz:.2f}%/yr")
rz, rr, rh = [eq(D[m]).pct_change().dropna() for m in ("zenith", "resting", "honest")]
check("6. CAGR ordering: zenith convention >= resting (gap charged)", cg(rz) >= cg(rr), f"zenith {cg(rz):.2f}%  honest {cg(rh):.2f}%  resting {cg(rr):.2f}%")
check("7. honest mode exits on the close signal and fills the next day (stop exits are PEAK/VOL, held at least one night)", set(th.Exit_Reason) <= {"PEAK_STOP", "VOLSTOP", "REBAL_EXIT"} and (th.Exit_Date > th.Entry_Date).all())
full, part = eq(D["zenith"]), eq(D["trunc"]); j = part.index.intersection(full.index)
check("8. no look-ahead: truncating the data at 2019-12-31 leaves earlier equity unchanged", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
check("9. split-neutral positions: no closed trade loses more than 60% net", (tz.Net_PnL_Pct > -60).all() and (th.Net_PnL_Pct > -60).all(), f"worst {tz.Net_PnL_Pct.min():.1f}% / {th.Net_PnL_Pct.min():.1f}%")
d_all, d_ng = dl(D["zenith"]), dl(D["nogold"])
check("10. gold sleeve: nothing held in the 2011-14 data gap, never above ~cap, stocks + gold <= 100% of equity", (d_all.gold_w["2011-01-01":"2014-12-31"] == 0).all() and d_all.gold_w.max() > 0.1 and d_all.gold_w.max() <= 0.25 * 1.4 and ((d_all.expo + d_all.gold_w) <= 1 + 1e-6).all(), f"max gold weight {d_all.gold_w.max()*100:.1f}%")
check("11. GOLD_CAP=0 turns the sleeve off", (d_ng.gold_w == 0).all())

if "--parity" in sys.argv:
    if REF is None:
        check("P. pre-cleanup reference found", False)
    else:
        cfgs = [({}, "default (zenith, gold 25%)"), ({"EXIT_MODE": "honest"}, "honest"), ({"EXIT_MODE": "resting"}, "resting"), ({"EXIT_MODE": "honest", "GOLD_CAP": 0.0}, "honest, no gold"),
                ({"GOLD_TARGET_RET": 0.08}, "gold re-centred to 8%"), ({"TOP_N": 15, "CASH_RATE_ANNUAL": 0.065}, "TOP_N 15, cash 6.5%"), ({"INITIAL_CAPITAL": 5e7}, "5 cr book"),
                ({"REBALANCE_FREQ_DAYS": 40, "EXIT_MODE": "honest"}, "rebalance 40, honest")]
        jobs = [(c, n, off) for c, n in cfgs for off in (0, 30)]
        with ThreadPoolExecutor(5) as ex:
            res = list(ex.map(lambda j: (j, run(SCRIPT, j[0], j[2]), run(REF, j[0], j[2])), jobs))
        for (c, n, off), a, b in res:
            ea, eb = eq(a), eq(b); ta, tb = tr(a), tr(b)
            same_eq = len(ea) == len(eb) and np.allclose(ea.values, eb.values, rtol=0, atol=1e-9)
            same_tr = len(ta) == len(tb) and np.allclose(ta.Quantity.values, tb.Quantity.values, rtol=0, atol=1e-9) and np.allclose(ta.Exit_Price.values, tb.Exit_Price.values, rtol=0, atol=1e-9)
            same_gold = np.allclose(dl(a).gold_w.values, dl(b).gold_w.values, rtol=0, atol=1e-12)
            check(f"P. identical to the pre-cleanup v2.6 -- {n}, anchor {off}", same_eq and same_tr and same_gold, f"equity maxdiff {np.abs(ea.values-eb.values).max():.1e}" if len(ea) == len(eb) else "different length")
print("\nALL PASS" if ok_all else "\nSOME FAILED"); sys.exit(0 if ok_all else 1)

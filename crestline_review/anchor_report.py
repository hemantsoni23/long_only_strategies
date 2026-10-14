"""Honest results for crestline_v2_3.py: runs the 6 schedule anchors in parallel and prints the per-anchor table, the mean, and the staggered blend.
usage: python3 anchor_report.py ['{"TOP_N": 25}']     (optional JSON config overrides; extra keys in env CL_OVR are passed to every anchor)"""
import os, sys, json, hashlib, subprocess
import numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.environ.get("CL_SCRIPT", os.path.join(HERE, "crestline_v2_6.py"))
ANCHORS = [0, 10, 20, 30, 40, 50]

def run_anchor(ovr, off, cache=True):
    key = json.dumps([os.path.basename(SCRIPT), ovr, off] + [os.stat(SCRIPT).st_mtime_ns], sort_keys=True)   # v2.5/v2.6 are still being edited: its edits must invalidate its cached runs
    d = os.path.join(HERE, ".anchor_cache", hashlib.md5(key.encode()).hexdigest()[:12])
    if not (cache and os.path.exists(os.path.join(d, "summary.json"))):
        os.makedirs(d, exist_ok=True)
        env = dict(os.environ, CL_OVR=json.dumps(ovr), CL_OUT=d, CRESTLINE_OFFSET=str(off))
        r = subprocess.run([sys.executable, SCRIPT], env=env, capture_output=True, text=True)
        open(os.path.join(d, "stdout.txt"), "w").write(r.stdout + r.stderr)
        if r.returncode:
            raise RuntimeError(r.stderr[-600:])
    return d

def metrics(r, rf=0.065):
    yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod()
    return dict(CAGR=(eq.iloc[-1] ** (1 / yrs) - 1) * 100, Sharpe0=r.mean() / r.std() * np.sqrt(252),
                Sharpe65=(r.mean() - ((1 + rf) ** (1 / 252) - 1)) / r.std() * np.sqrt(252), MaxDD=(eq / eq.cummax() - 1).min() * 100)

def report(ovr=None, label=""):
    ovr = ovr or {}
    with ThreadPoolExecutor(6) as ex:
        dirs = list(ex.map(lambda o: run_anchor(ovr, o), ANCHORS))
    rets, rows = [], []
    for off, d in zip(ANCHORS, dirs):
        r = pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0].pct_change().dropna()
        s = json.load(open(os.path.join(d, "summary.json")))
        rets.append(r.rename(off)); rows.append(dict(anchor=off, **metrics(r), Expo=s["m"]["AvgExpo"], Turn=s["m"]["Turnover"], Trades=s["n_trades"]))
    R = pd.concat(rets, axis=1).dropna()
    t = pd.DataFrame(rows).set_index("anchor")
    mean = t.mean(); lo = t.min(); hi = t.max()
    bl = metrics(R.mean(axis=1))
    print(f"\n=== Crestline {label} {json.dumps(ovr) if ovr else '(defaults)'}  [{R.index[0].date()} -> {R.index[-1].date()}] ===")
    print(t.round(2).to_string())
    print("mean   ", " ".join(f"{k} {v:.2f}" for k, v in mean.items()))
    print("min/max", " ".join(f"{k} {lo[k]:.2f}/{hi[k]:.2f}" for k in ["CAGR", "Sharpe65", "MaxDD"]))
    print("6-anchor staggered blend:", " ".join(f"{k} {v:.2f}" for k, v in bl.items()))
    return t, bl

if __name__ == "__main__":
    report(json.loads(sys.argv[1]) if len(sys.argv) > 1 else None)

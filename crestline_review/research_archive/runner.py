"""Run lab variants in parallel and tabulate. usage: python3 runner.py <experiment_name>   (variants defined in experiments.py)"""
import os, sys, json, subprocess, itertools, hashlib
import numpy as np, pandas as pd
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")

def run(ovr, offset=0, tag=None):
    key = json.dumps(dict(ovr, _off=offset, _v=("floor2" if ovr.get("CA_ADJUST") else "")), sort_keys=True)
    d = os.path.join(RUNS, hashlib.md5(key.encode()).hexdigest()[:12])
    if not os.path.exists(os.path.join(d, "summary.json")):
        os.makedirs(d, exist_ok=True)
        env = dict(os.environ, CL_OVR=json.dumps(ovr), CL_OUT=d, CRESTLINE_OFFSET=str(offset))
        r = subprocess.run([sys.executable, os.path.join(HERE, "crestline_lab.py")], env=env, capture_output=True, text=True)
        open(os.path.join(d, "stdout.txt"), "w").write(r.stdout + r.stderr)
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-800:])
    return d

def stats(d, rf=0.065):
    eq = pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
    s = json.load(open(os.path.join(d, "summary.json")))
    r = eq.pct_change().dropna()
    def blk(x):
        if len(x) < 50:
            return dict(cagr=np.nan, sh0=np.nan, sh65=np.nan, mdd=np.nan)
        yrs = (x.index[-1] - x.index[0]).days / 365.25
        return dict(cagr=((1 + x).prod() ** (1 / yrs) - 1) * 100, sh0=x.mean() / x.std() * np.sqrt(252),
                    sh65=(x.mean() - ((1 + rf) ** (1 / 252) - 1)) / x.std() * np.sqrt(252),
                    mdd=((1 + x).cumprod() / (1 + x).cumprod().cummax() - 1).min() * 100)
    a = blk(r); h1 = blk(r[:"2014-12-31"]); h2 = blk(r["2015-01-01":])
    return dict(cagr=a["cagr"], sh0=a["sh0"], sh65=a["sh65"], mdd=a["mdd"], sh0_h1=h1["sh0"], sh0_h2=h2["sh0"],
                sh65_h1=h1["sh65"], sh65_h2=h2["sh65"], expo=s["m"]["AvgExpo"], hold=s["m"]["AvgHold"], turn=s["m"]["Turnover"],
                trades=s["n_trades"], win=s["win"], pf=s["pf"], ic60=[x for x in s["ic"] if x["Horizon"] == 60][0]["MeanIC"])

def sweep(variants, offsets, workers=5):
    jobs = [(n, o, off) for n, o in variants.items() for off in offsets]
    with ThreadPoolExecutor(workers) as ex:
        dirs = list(ex.map(lambda j: run(j[1], j[2]), jobs))
    rows = []
    for (n, o, off), d in zip(jobs, dirs):
        rows.append(dict(variant=n, offset=off, **stats(d)))
    return pd.DataFrame(rows)

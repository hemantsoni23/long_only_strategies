import os, json, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_gold_lab.py")
CAPS = {"c0": 1e5, "c1": 1e7, "c5": 5e7, "c20": 2e8}
R1 = ["GOLDBEES", "SILVERBEES"]; R2 = ["GOLDBEES"]
V = {}
for k, c in CAPS.items(): V[f"B_{k}"] = dict(INITIAL_CAPITAL=c)
for k in ["c0", "c1"]:
    for nm, lst in [("R1", R1), ("R2", R2)]:
        for lam in [0.0, 1.0]:
            V[f"{nm}_{k}_l{int(lam)}"] = dict(INITIAL_CAPITAL=CAPS[k], ETF_LIST=lst, **({"ETF_DRIFT_LAMBDA": lam} if lam else {}))
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]).to_csv("results_gold_engine.csv", index=False)
    pd.Series({f"{n}|{a}": d for (n, o, a), d in zip(jobs, dirs)}).to_json("dirs_gold_engine.json"); print("done")

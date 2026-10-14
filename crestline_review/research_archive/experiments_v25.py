import os, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_v2_5.py")
CAPS = {"c0": 1e5, "c1": 1e7, "c5": 5e7, "c20": 2e8}
V = {}
for k, c in CAPS.items():
    b = dict(INITIAL_CAPITAL=c)
    V[f"G25_real_{k}"] = dict(b); V[f"G25_8_{k}"] = dict(b, GOLD_TARGET_RET=0.08); V[f"G25_4_{k}"] = dict(b, GOLD_TARGET_RET=0.04); V[f"G20_8_{k}"] = dict(b, GOLD_CAP=0.20, GOLD_TARGET_RET=0.08)
    V[f"G25_8_cost2_{k}"] = dict(b, GOLD_TARGET_RET=0.08, COST_ONE_WAY=0.006, GOLD_COST=0.003); V[f"N_cost2_{k}"] = dict(b, GOLD_CAP=0.0, COST_ONE_WAY=0.006)
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]).to_csv("results_v25.csv", index=False)
    pd.Series({f"{n}|{a}": d for (n, o, a), d in zip(jobs, dirs)}).to_json("dirs_v25.json"); print("done")

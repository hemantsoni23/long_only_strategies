import os, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_v2_6.py")
CAPS = {"c0": 1e5, "c1": 1e7, "c5": 5e7, "c20": 2e8}
V = {}
for k, c in CAPS.items():
    for m in ["zenith", "resting", "honest"]:
        V[f"{m}_g8_{k}"] = dict(INITIAL_CAPITAL=c, EXIT_MODE=m, GOLD_TARGET_RET=0.08)
for m in ["zenith", "resting", "honest"]:
    V[f"{m}_nogold_c0"] = dict(EXIT_MODE=m, GOLD_CAP=0.0)
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]).to_csv("results_v26.csv", index=False)
    pd.Series({f"{n}|{a}": d for (n, o, a), d in zip(jobs, dirs)}).to_json("dirs_v26.json"); print("done")

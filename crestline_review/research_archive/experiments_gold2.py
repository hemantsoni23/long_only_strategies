import os, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_gold_lab.py")
CAPS = {"c0": 1e5, "c1": 1e7, "c5": 5e7, "c20": 2e8}
V = {f"B0_{k}": dict(INITIAL_CAPITAL=c, CASH_RATE_ANNUAL=0.0) for k, c in CAPS.items()}
V["B0_c0_N15"] = dict(CASH_RATE_ANNUAL=0.0, TOP_N=15)      # information item: v2.3 breadth at cash 0
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]).to_csv("results_gold2_engine.csv", index=False)
    pd.Series({f"{n}|{a}": d for (n, o, a), d in zip(jobs, dirs)}).to_json("dirs_gold2_engine.json"); print("done")

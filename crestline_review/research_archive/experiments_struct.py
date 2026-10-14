import os, sys, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_struct_lab.py")
A12 = list(range(0, 60, 5))
WIDE = dict(VOLSTOP_K=5.0, VOLSTOP_MIN_PCT=0.15, VOLSTOP_MAX_PCT=0.35)
BOOKS = {"N25": {}, "N75": dict(TOP_N=75), "N150": dict(TOP_N=150), "N24": dict(TOP_N=24), "N8": dict(TOP_N=8, MAX_ENTRY_PCT=1.0), "N4": dict(TOP_N=4, MAX_ENTRY_PCT=1.0)}
SING = {"B": {}, "VS1": dict(SIZE_MODE=1, VS_LO=0.5, VS_HI=1.5), "VS2": dict(SIZE_MODE=1, VS_LO=0.33, VS_HI=2.0), "VS3": dict(SIZE_MODE=2, VS_LO=0.5, VS_HI=1.5), "VS4": dict(SIZE_MODE=2, VS_LO=0.33, VS_HI=2.0),
        "WIDE": dict(WIDE), "RS1": dict(RS_SUP=0.05), "RS2": dict(RS_SUP=0.10)}
CAP = {}
for nm, cap in [("c1", 1e7), ("c5", 5e7), ("c20", 2e8)]:
    CAP[f"B_{nm}"] = dict(INITIAL_CAPITAL=cap); CAP[f"CW3_{nm}"] = dict(INITIAL_CAPITAL=cap, CAPWALK_DEPTH=3); CAP[f"CW6_{nm}"] = dict(INITIAL_CAPITAL=cap, CAPWALK_DEPTH=6)
def sweep(V, anchors, tag):
    jobs = [(n, o, a) for n, o in V.items() for a in anchors]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    df = pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]); df.to_csv(f"results_struct_{tag}.csv", index=False)
    pd.Series({f"{n}|{a}": d for (n, o, a), d in zip(jobs, dirs)}).to_json(f"dirs_struct_{tag}.json"); print("done", tag, flush=True)
if __name__ == "__main__":
    sweep(SING, ar.ANCHORS, "sing"); sweep(CAP, ar.ANCHORS, "cap"); sweep(BOOKS, A12, "books")

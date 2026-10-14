import json, sys, numpy as np, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
mp = lambda w: int(round(w * 0.8))
S0 = {}
S1 = dict(TOP_N=25)
S2 = dict(S1, TP_SMA_WINDOW=20, TP_SMA_MIN_PERIODS=mp(20))
S3 = dict(S2, TP_LOOKBACK=126, TP_MIN_PERIODS=mp(126))
checks = {"S3_cost6": dict(S3, COST_ONE_WAY=0.006), "B_cost6": dict(COST_ONE_WAY=0.006),
          "S3_cash0": dict(S3, CASH_RATE_ANNUAL=0.0), "B_cash0": dict(CASH_RATE_ANNUAL=0.0),
          "S3_2015": dict(S3, START_DATE="2015-01-01"), "B_2015": dict(START_DATE="2015-01-01")}
V = {"B": S0, "S1": S1, "S2": S2, "S3": S3, **checks}
jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
df = pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]); df.to_csv("results_joint.csv", index=False); print("done")

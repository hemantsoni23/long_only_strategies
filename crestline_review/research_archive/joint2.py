import pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
mp = lambda w: int(round(w * 0.8))
S1 = dict(TOP_N=25); S3p = dict(S1, TP_LOOKBACK=126, TP_MIN_PERIODS=mp(126))
V = {"S3p": S3p, "S3p_cost6": dict(S3p, COST_ONE_WAY=0.006), "S3p_cash0": dict(S3p, CASH_RATE_ANNUAL=0.0), "S3p_2015": dict(S3p, START_DATE="2015-01-01"),
     "S1_cost6": dict(S1, COST_ONE_WAY=0.006), "S1_cash0": dict(S1, CASH_RATE_ANNUAL=0.0), "S1_2015": dict(S1, START_DATE="2015-01-01")}
jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]).to_csv("results_joint2.csv", index=False); print("done")

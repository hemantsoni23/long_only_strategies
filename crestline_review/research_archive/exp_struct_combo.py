import os, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
from experiments_struct import SING, WIDE
ar.SCRIPT = os.path.join(ar.HERE, "crestline_struct_lab.py")
V = {"VS2+WIDE": dict(SING["VS2"], **WIDE)}
jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
new = pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)])
st = pd.concat([pd.read_csv("results_struct_sing.csv"), new]); st.to_csv("results_struct_sing2.csv", index=False)

import os, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_exits_lab.py")
V = {"RF": dict(USE_SLOT_REFILL=True, REFILL_FREQ_DAYS=20, REFILL_COOLDOWN_DAYS=30)}
jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
st = pd.concat([pd.read_csv("results_exits.csv").query("variant=='B'"), pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)])])
st.to_csv("results_exits_rf.csv", index=False)
b = st[st.variant == "B"].set_index("offset"); g = st[st.variant == "RF"].set_index("offset"); d = g.sh65 - b.sh65
print(f"RF vs B: CAGR {g.cagr.mean():.2f} ({g.cagr.mean()-b.cagr.mean():+.2f})  Sh65 {g.sh65.mean():.2f} ({d.mean():+.3f})  dPA {(g.sh65_h1-b.sh65_h1).mean():+.3f} dPB {(g.sh65_h2-b.sh65_h2).mean():+.3f}  anchors+ {(d>0).sum()}/6  MaxDD {g.mdd.mean():.2f} ({g.mdd.mean()-b.mdd.mean():+.2f})  expo {g.expo.mean():.1f}")

import os, json, numpy as np, pandas as pd, anchor_report as ar, runner
from concurrent.futures import ThreadPoolExecutor
ar.SCRIPT = os.path.join(ar.HERE, "crestline_exits_lab.py")
M = dict(MON_FREQ_DAYS=5)
V = {"B": {},
 "SA1": dict(M, SA_RANK=25, SA_CATA_PCT=0.25), "SA2": dict(M, SA_RANK=50, SA_CATA_PCT=0.25), "SA3": dict(M, SA_RANK=25, SA_CATA_PCT=0.35), "SA4": dict(M, SA_RANK=50, SA_CATA_PCT=0.35),
 "RE1": dict(M, RE_RANK=25, RE_COOLDOWN=5), "RE2": dict(M, RE_RANK=25, RE_COOLDOWN=10), "RE3": dict(M, RE_RANK=50, RE_COOLDOWN=10),
 "PW1": dict(PW_GAIN=0.15, PW_MULT=1.5), "PW2": dict(PW_GAIN=0.15, PW_MULT=2.0), "PW3": dict(PW_GAIN=0.30, PW_MULT=1.5), "PW4": dict(PW_GAIN=0.30, PW_MULT=2.0),
 "PN1": dict(PANIC_PCTL=0.90)}
def mech(dirs):
    t = pd.concat([pd.read_csv(os.path.join(d, "trade_log_full.csv"), parse_dates=["Entry_Date", "Exit_Date"]).assign(a=i) for i, d in enumerate(dirs)])
    big = t[t.MFE_Pct >= 30]
    t = t.sort_values(["a", "Ticker", "Entry_Date"]); t["prev_exit"] = t.groupby(["a", "Ticker"]).Exit_Date.shift(); t["prev_reason"] = t.groupby(["a", "Ticker"]).Exit_Reason.shift()
    re = ((t.Entry_Date - t.prev_exit).dt.days <= 90) & t.prev_reason.isin(["VOLSTOP", "PEAK_STOP", "HARD_STOP", "SA_CATA"])
    return dict(hold_d=t.Holding_Days.mean(), capture=big.Net_PnL_Pct.mean() / big.MFE_Pct.mean() * 100, n_big=len(big) / len(dirs), reentry_pct=re.mean() * 100, trades=len(t) / len(dirs),
                sa_cata=(t.Exit_Reason == "SA_CATA").sum() / len(dirs))
if __name__ == "__main__":
    jobs = [(n, o, a) for n, o in V.items() for a in ar.ANCHORS]
    with ThreadPoolExecutor(5) as ex: dirs = list(ex.map(lambda j: ar.run_anchor(j[1], j[2]), jobs))
    st = pd.DataFrame([dict(variant=n, offset=a, **runner.stats(d)) for (n, o, a), d in zip(jobs, dirs)]); st.to_csv("results_exits.csv", index=False)
    byv = {}
    for (n, o, a), d in zip(jobs, dirs): byv.setdefault(n, []).append(d)
    pd.DataFrame({n: mech(ds) for n, ds in byv.items()}).T.to_csv("results_exits_mech.csv"); print("done")

import os, json, numpy as np, pandas as pd
pd.set_option("display.width", 250)
st = pd.read_csv("results_v26.csv"); D = json.load(open("dirs_v26.json")); A = [0, 10, 20, 30, 40, 50]
SIZES = {"c0": "1 lakh", "c1": "1 cr", "c5": "5 cr", "c20": "20 cr"}
def summ(v): return [json.load(open(os.path.join(D[f"{v}|{a}"], "summary.json"))) for a in A]
def row(v, label):
    g = st[st.variant == v]; hid = np.mean([s["hidden_pct_yr"] for s in summ(v)]); ex = np.mean([s["m"]["AvgExpo"] for s in summ(v)])
    return dict(case=label, CAGR=g.cagr.mean(), Sh0=g.sh0.mean(), MaxDD=g.mdd.mean(), Calmar=g.cagr.mean() / abs(g.mdd.mean()), Sh0_A=g.sh0_h1.mean(), Sh0_B=g.sh0_h2.mean(), stock_expo=ex, hidden_pnl_pct_yr=hid)
rows = []
for k, nm in SIZES.items():
    for m, lab in [("zenith", "ZENITH exits (live convention)"), ("resting", "RESTING (zenith fill, gap charged)"), ("honest", "HONEST next-open (v2.5)")]:
        r = row(f"{m}_g8_{k}", lab); r["size"] = nm; rows.append(r)
T = pd.DataFrame(rows)[["size", "case", "CAGR", "Sh0", "MaxDD", "Calmar", "Sh0_A", "Sh0_B", "stock_expo", "hidden_pnl_pct_yr"]]
print("gold sleeve 25% @ 8%/yr, 6 anchors, 2006-25, idle cash 0%, rf=0:"); print(T.round(2).to_string(index=False)); T.to_csv("v26_headline.csv", index=False)
print("\nno gold, 1 lakh:"); print(pd.DataFrame([dict(size="1 lakh", **row(f"{m}_nogold_c0", m)) for m in ["zenith", "resting", "honest"]])[["case", "CAGR", "Sh0", "MaxDD", "Calmar", "hidden_pnl_pct_yr"]].round(2).to_string(index=False))
# exit-reason mix and stop counts, anchor 0, 1 lakh
print("\nstop exits per mode (anchor 0, 1 lakh, gold 8%):")
for m in ["zenith", "resting", "honest"]:
    t = pd.read_csv(os.path.join(D[f"{m}_g8_c0|0"], "trade_log_full.csv")); print(f"  {m:8s}", t.Exit_Reason.value_counts().to_dict(), " mean hold days %.1f" % t.Holding_Days.mean())

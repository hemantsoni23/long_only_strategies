import os, json, numpy as np, pandas as pd, anchor_report as ar
eq = lambda d: pd.read_csv(os.path.join(d, "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
dl = lambda d: pd.read_csv(os.path.join(d, "daily.csv"), index_col=0, parse_dates=True); ok_all = True
def check(n, ok, det=""):
    global ok_all; ok_all &= bool(ok); print(("PASS " if ok else "FAIL ") + n + (" -- " + det if det else ""))
V24 = os.path.join(ar.HERE, "crestline_v2_4.py"); LAB = os.path.join(ar.HERE, "crestline_gold_lab.py")
def run(script, ovr, off): ar.SCRIPT = script; return ar.run_anchor(ovr, off, cache=False)
for off in [0, 30]:
    ref = eq(run(V24, {}, off)); a = eq(run(LAB, {}, off)); check(f"1. gold lab defaults == v2.4 (anchor {off})", np.allclose(a.values, ref.values, rtol=0, atol=1e-9))
base = run(LAB, {}, 0); bd = dl(base)
check("2. daily dump is consistent with the summary", abs(bd.expo.mean() * 100 - json.load(open(os.path.join(base, "summary.json")))["m"]["AvgExpo"]) < 0.5, f"mean expo {bd.expo.mean()*100:.2f}%")
d = run(LAB, {"ETF_LIST": ["GOLDBEES", "SILVERBEES"]}, 0); dd = dl(d); et = pd.read_csv(os.path.join(d, "etf_trades.csv"), parse_dates=["Entry_Date"]) if os.path.getsize(os.path.join(d, "etf_trades.csv")) > 5 else pd.DataFrame()
check("3. benchmark regime flags unchanged by adding ETFs", (dd.bear == bd.bear.reindex(dd.index)).all() and (dd.panic == bd.panic.reindex(dd.index)).all())
if len(et):
    first = et.groupby("Ticker").Entry_Date.min()
    check("4. no ETF trade in 2011-14 or before eligibility (GOLDBEES >= 2016, SILVERBEES >= 2023)", not ((et.Entry_Date >= "2011-01-01") & (et.Entry_Date < "2016-01-01")).any() and (first.get("SILVERBEES", pd.Timestamp("2030-01-01")) >= pd.Timestamp("2023-01-01")), f"first entries {first.to_dict()}")
    print("   ETF trades:", len(et), et.groupby("Ticker").size().to_dict())
else:
    check("4. (no ETF trades taken at all)", True, "R1 never selected an ETF at anchor 0")
# 5 drift placebo: reconstruct the zero-drift series the same way and check its mean excess
c = pd.read_csv("/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data/GOLDBEES.csv"); c["t"] = pd.to_datetime(c.timestamp.str[:10]); c = c.set_index("t").close
r = c.pct_change(); r[c.index.to_series().diff().dt.days > 5] = np.nan; dlg = np.nanmean(np.log1p(r.dropna())) - np.log1p(1.065 ** (1 / 252) - 1)
f = np.exp(-1.0 * dlg * r.notna().cumsum()); c2 = c * f; r2 = c2.pct_change(); r2[c.index.to_series().diff().dt.days > 5] = np.nan
ann = lambda x: ((1 + x.dropna()).prod() ** (252 / x.notna().sum()) - 1) * 100
check("5. zero-drift placebo: GOLDBEES annual return falls to the liquid-fund rate", abs(ann(r2) - 6.5) < 0.6, f"real {ann(r):.1f}% -> placebo {ann(r2):.1f}%")
a1 = {"ETF_LIST": ["GOLDBEES", "SILVERBEES"]}
full = eq(run(LAB, a1, 0)); part = eq(run(LAB, dict(a1, END_DATE="2019-12-31"), 0)); j = part.index.intersection(full.index)
check("6. truncation at 2019-12-31 leaves earlier equity unchanged (ETFs on)", np.allclose(full[j][:"2019-06-30"].values, part[j][:"2019-06-30"].values, rtol=1e-6))
print("\nALL PASS" if ok_all else "\nSOME FAILED")

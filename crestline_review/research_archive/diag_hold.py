"""Holding-period diagnostics (PREREG_DIAG.md items 1-6) on v2.4 (TOP_N=25) trade logs, 6 anchors pooled."""
import os, json, numpy as np, pandas as pd, anchor_report as ar
pd.set_option("display.width", 250)
D = np.load("diag/diag.npz", allow_pickle=True); close = np.load("diag/close.npy"); opn = np.load("diag/open.npy"); F = np.load("diag/fwd_cache.npz")
alld = pd.to_datetime(D["all_dates"]); nb = len(alld); me_pos = D["me_pos"]; pool = D["pool"]; rank = D["rank"]; cols = list(D["cols"]); cidx = {c: i for i, c in enumerate(cols)}
tr = []
for off in ar.ANCHORS:
    d = ar.run_anchor({"TOP_N": 25}, off); t = pd.read_csv(os.path.join(d, "trade_log_full.csv"), parse_dates=["Entry_Date", "Exit_Date"]); t["anchor"] = off; tr.append(t)
tr = pd.concat(tr, ignore_index=True)
pos = {d: i for i, d in enumerate(alld)}
tr["e"] = tr.Entry_Date.map(pos); tr["x"] = tr.Exit_Date.map(pos); tr["c"] = tr.Ticker.map(cidx); tr = tr.dropna(subset=["e", "x", "c"]); tr[["e", "x", "c"]] = tr[["e", "x", "c"]].astype(int)
tr["hold"] = tr.x - tr.e
uniq = tr.drop_duplicates(["Ticker","Entry_Date","Exit_Date"]); print(f"unique (ticker, entry, exit) trades: {len(uniq)} of {len(tr)} pooled -> effective sample is smaller than the pooled N")
print(f"{len(tr)} trades pooled over {len(ar.ANCHORS)} anchors\n")
# 1. holding distribution
print("== 1. holding time (trading days) ==")
g = tr.groupby("Exit_Reason").hold
print(pd.concat([g.size().rename("N"), g.mean().rename("mean"), g.median().rename("median"), (tr.assign(a=tr.hold < 20).groupby("Exit_Reason").a.mean() * 100).rename("%<20d"), (tr.assign(a=tr.hold < 60).groupby("Exit_Reason").a.mean() * 100).rename("%<60d")], axis=1).round(1).to_string())
w = tr.Position_Size
print(f"ALL: mean {tr.hold.mean():.1f}  median {tr.hold.median():.0f}  capital-weighted mean {np.average(tr.hold, weights=w):.1f}  | share <20d {np.mean(tr.hold<20)*100:.0f}%  <40d {np.mean(tr.hold<40)*100:.0f}%  <60d {np.mean(tr.hold<60)*100:.0f}%  <120d {np.mean(tr.hold<120)*100:.0f}%  >=120d {np.mean(tr.hold>=120)*100:.0f}%")
# 2. counterfactual no-stop hold, same entries
CF = 0.006
for h in [20, 60, 120]:
    ok = tr.e + h < nb
    tr[f"cf{h}"] = np.where(ok, close[np.clip(tr.e + h, 0, nb - 1), tr.c] / tr.Entry_Price - 1 - CF, np.nan) * 100
print("\n== 2. same entries, realised vs hold-H with no stops (net of 0.6% round trip), % per trade ==")
rows = []
for h in [20, 60, 120]:
    m = tr[f"cf{h}"].notna(); rows.append(dict(H=h, N=int(m.sum()), realised_mean=tr.Net_PnL_Pct[m].mean(), cf_mean=tr[f"cf{h}"][m].mean(), realised_median=tr.Net_PnL_Pct[m].median(), cf_median=tr[f"cf{h}"][m].median(),
                                                realised_win=(tr.Net_PnL_Pct[m] > 0).mean() * 100, cf_win=(tr[f"cf{h}"][m] > 0).mean() * 100,
                                                realised_pct_per_held_day=tr.Net_PnL_Pct[m].sum() / tr.hold[m].clip(lower=1).sum(), cf_pct_per_day=tr[f"cf{h}"][m].sum() / (h * m.sum())))
print(pd.DataFrame(rows).round(2).to_string(index=False))
# 3. post-exit drift vs pool
def pool_mean(bar, K):
    i = np.searchsorted(me_pos, bar - 1, side="right") - 1
    if i < 0: return np.nan
    f = F[f"f{K}"][i]; m = pool[i] & ~np.isnan(f); return f[m].mean() if m.sum() > 50 else np.nan
for K in [20, 60, 120]:
    ok = tr.x + K < nb
    xr = np.where(ok, close[np.clip(tr.x + K, 0, nb - 1), tr.c] / tr.Exit_Price - 1, np.nan)
    pm = np.array([pool_mean(b, K) if o else np.nan for b, o in zip(tr.x, ok)])
    tr[f"post{K}"] = (xr - pm) * 100
print("\n== 3. post-exit EXCESS return vs pool mean (exit open -> +K bars), % ==")
rows = []
for r, gg in tr.groupby("Exit_Reason"):
    for K in [20, 60, 120]:
        v = gg[f"post{K}"].dropna(); rows.append(dict(reason=r, K=K, N=len(v), mean=v.mean(), median=v.median(), pct_pos=(v > 0).mean() * 100))
print(pd.DataFrame(rows).pivot_table(index="reason", columns="K", values=["N", "mean", "median", "pct_pos"]).round(2).to_string())
# 4. winners
big = tr[tr.cf120.notna() & (tr.cf120 > 30)]
print(f"\n== 4. big winners (no-stop 120-bar return > +30%): {len(big)} of {int(tr.cf120.notna().sum())} entries ({len(big)/tr.cf120.notna().sum()*100:.0f}%) ==")
print(f"   exited before day 20: {np.mean(big.hold<20)*100:.0f}%   before day 60: {np.mean(big.hold<60)*100:.0f}%   before day 120: {np.mean(big.hold<120)*100:.0f}%")
print(f"   avg realised net {big.Net_PnL_Pct.mean():.1f}%  vs no-stop 120d {big.cf120.mean():.1f}%  -> capture {big.Net_PnL_Pct.mean()/big.cf120.mean()*100:.0f}%")
print("   exit reasons of big winners:", big.Exit_Reason.value_counts().to_dict())
mf = tr[tr.MFE_Pct >= 30]; print(f"   trades with MFE >= 30%: {len(mf)}; mean MFE {mf.MFE_Pct.mean():.1f}%, mean realised net {mf.Net_PnL_Pct.mean():.1f}% -> {mf.Net_PnL_Pct.mean()/mf.MFE_Pct.mean()*100:.0f}% of peak captured")
srt = tr.sort_values("Net_PnL_Abs", ascending=False); tot = tr.Net_PnL_Abs.sum(); n10 = int(len(tr) * 0.1)
print(f"   top 10% of trades by P&L = {srt.Net_PnL_Abs.head(n10).sum()/tot*100:.0f}% of total net P&L; their mean hold {srt.hold.head(n10).mean():.0f}d, exit reasons {srt.Exit_Reason.head(n10).value_counts().to_dict()}")
# 5. signal state at exit
stp = tr[tr.Exit_Reason.isin(["VOLSTOP", "PEAK_STOP", "HARD_STOP"])].copy()
def rk_at(bar, c):
    i = np.searchsorted(me_pos, bar - 1, side="right") - 1
    return rank[i, c] if i >= 0 else np.nan
stp["rk"] = [rk_at(b, c) for b, c in zip(stp.x, stp.c)]
stp["grp"] = np.where(stp.rk <= 25, "still top-25", np.where(stp.rk <= 50, "rank 26-50", np.where(stp.rk <= 150, "rank 51-150", "rank >150 / out of pool")))
print(f"\n== 5. rank (latest grid date before exit) of the {len(stp)} stop-exited names ==")
agg = stp.groupby("grp").agg(N=("rk", "size"), post20=("post20", "mean"), post60=("post60", "mean"), post120=("post120", "mean"), real=("Net_PnL_Pct", "mean"), hold=("hold", "median"))
agg["share%"] = agg.N / agg.N.sum() * 100; print(agg.round(2).to_string())
tr.to_pickle("diag/trades_enriched.pkl")

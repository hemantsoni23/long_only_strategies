"""Part 0: is gold's correlation with the stock market / the Crestline book really low, and when?"""
import os, json, numpy as np, pandas as pd, gold_common as gc
pd.set_option("display.width", 250)
D = np.load("diag/diag.npz", allow_pickle=True); alld = pd.to_datetime(D["all_dates"]); bench = pd.Series(D["bench"], index=alld); br = bench.pct_change()
dirs = json.load(open("dirs_gold_engine.json")); d0 = pd.read_csv(os.path.join(dirs["B_c0|0"], "daily.csv"), index_col=0, parse_dates=True)
book = d0["eq"].pct_change()
g = gc.etf("GOLDBEES"); rg = gc.valid_returns(g.close, br.index); s = gc.etf("SILVERBEES"); rs = gc.valid_returns(s.close, br.index)
df = pd.DataFrame({"gold": rg, "silver": rs, "mkt": br, "book": book.reindex(br.index)}).dropna(subset=["gold", "mkt"])
df = df["2007-03-20":"2025-12-31"]; df["reg"] = d0[["bear", "panic"]].reindex(df.index).apply(lambda r: "panic" if r.panic else ("bear" if r.bear else "bull/other"), axis=1)
print("daily corr gold vs EW stock index:"); rows = []
for nm, m in [("all usable (2007-10 + 2015-25)", slice(None)), ("2007-03..2010-12", df.index <= "2010-12-31"), ("2015-25", df.index >= "2015-01-01"), ("2020-25", df.index >= "2020-01-01")]:
    x = df[m] if not isinstance(m, slice) else df; rows.append(dict(sample=nm, n=len(x), corr_mkt=x.gold.corr(x.mkt), corr_book=x.gold.corr(x.book)))
print(pd.DataFrame(rows).round(3).to_string(index=False))
print("\nby engine regime (day t flag):"); rr = []
for rg_, x in df.groupby("reg"): rr.append(dict(regime=rg_, days=len(x), pct_days=len(x) / len(df) * 100, corr_mkt=x.gold.corr(x.mkt), gold_ann_ret=x.gold.mean() * 252 * 100, mkt_ann_ret=x.mkt.mean() * 252 * 100, gold_vol=x.gold.std() * np.sqrt(252) * 100))
print(pd.DataFrame(rr).round(2).to_string(index=False))
num = df[["gold", "silver", "mkt", "book"]]; w = num.resample("W").apply(lambda a: (1 + a).prod() - 1); m = num.resample("ME").apply(lambda a: (1 + a).prod() - 1)
print(f"\nweekly corr gold-mkt {w.gold.corr(w.mkt):.3f}   monthly corr {m.gold.corr(m.mkt):.3f}   monthly gold-book {m.gold.corr(m.book):.3f}")
roll = df.gold.rolling(252).corr(df.mkt).dropna(); print(f"rolling 1y daily corr: min {roll.min():.2f}  median {roll.median():.2f}  max {roll.max():.2f}; share of days above +0.3: {(roll>0.3).mean()*100:.0f}%")
# worst equity-index drawdown episodes
mk = (1 + df.mkt).cumprod(); dd = mk / mk.cummax() - 1; ep = []; inep = False
for t, v in dd.items():
    if v < -0.10 and not inep: inep = True; start = t
    if inep and v > -0.02: ep.append((start, dd[start:t].idxmin(), dd[start:t].min())); inep = False
print("\nEW stock index drawdown episodes (< -10%): gold and book over peak->trough")
rows = []
for a, b, depth in sorted(ep, key=lambda e: e[2])[:8]:
    seg = df[a:b]; rows.append(dict(peak_to_trough=f"{a.date()}..{b.date()}", mkt=((1 + seg.mkt).prod() - 1) * 100, gold=((1 + seg.gold).prod() - 1) * 100, book=((1 + seg.book.fillna(0)).prod() - 1) * 100))
print(pd.DataFrame(rows).round(1).to_string(index=False))
print("\nsilver (2022-02..2025): corr with mkt", round(df.dropna(subset=['silver']).silver.corr(df.dropna(subset=['silver']).mkt), 3), " with gold", round(df.dropna(subset=['silver']).silver.corr(df.dropna(subset=['silver']).gold), 3), " silver ann ret", round(df.silver.dropna().mean() * 252 * 100, 1), " vol", round(df.silver.dropna().std() * np.sqrt(252) * 100, 1))

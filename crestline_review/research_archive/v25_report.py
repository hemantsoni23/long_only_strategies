import os, json, numpy as np, pandas as pd
pd.set_option("display.width", 250)
st = pd.concat([pd.read_csv("results_gold2_engine.csv"), pd.read_csv("results_v25.csv")]); D = {**json.load(open("dirs_gold2_engine.json")), **json.load(open("dirs_v25.json"))}
SIZES = {"c0": "1 lakh", "c1": "1 cr", "c5": "5 cr", "c20": "20 cr"}; A = [0, 10, 20, 30, 40, 50]
def agg(v): g = st[st.variant == v].set_index("offset"); return g
def curve(v, a): return pd.read_csv(os.path.join(D[f"{v}|{a}"], "equity_curves.csv"), index_col=0, parse_dates=True).iloc[:, 0]
def mt(r):
    yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod(); cagr = (eq.iloc[-1] ** (1 / yrs) - 1) * 100; dd = (eq / eq.cummax() - 1).min() * 100
    return dict(CAGR=cagr, Sh0=r.mean() / r.std() * np.sqrt(252), MaxDD=dd, Calmar=cagr / abs(dd))
rows = []
for k, nm in SIZES.items():
    b = agg(f"B0_{k}")
    rows.append(dict(size=nm, case="no gold (idle at 0%)", CAGR=b.cagr.mean(), Sh0=b.sh0.mean(), MaxDD=b.mdd.mean(), Calmar=b.cagr.mean() / abs(b.mdd.mean()), dSh0=0.0, anchors="-", P_A=b.sh0_h1.mean(), P_B=b.sh0_h2.mean()))
    for v, lab in [(f"G25_real_{k}", "gold 25%, REAL gold"), (f"G25_8_{k}", "gold 25%, gold 8%/yr (planning)"), (f"G25_4_{k}", "gold 25%, gold 4%/yr"), (f"G20_8_{k}", "gold 20%, gold 8%/yr")]:
        g = agg(v); d = g.sh0 - b.sh0
        rows.append(dict(size=nm, case=lab, CAGR=g.cagr.mean(), Sh0=g.sh0.mean(), MaxDD=g.mdd.mean(), Calmar=g.cagr.mean() / abs(g.mdd.mean()), dSh0=d.mean(), anchors=f"{int((d>0).sum())}/6", P_A=g.sh0_h1.mean(), P_B=g.sh0_h2.mean()))
T = pd.DataFrame(rows); print(T.round(2).to_string(index=False)); T.to_csv("v25_headline.csv", index=False)
print("\nDOUBLE COST (stock 0.6% + gold 0.3% one way) vs no-gold at double cost, gold 8%/yr:")
for k, nm in SIZES.items():
    g = agg(f"G25_8_cost2_{k}"); b = agg(f"N_cost2_{k}"); d = g.sh0 - b.sh0
    print(f"  {nm:7s} no-gold {b.cagr.mean():5.2f}% / Sh0 {b.sh0.mean():.2f} / DD {b.mdd.mean():6.2f}   gold {g.cagr.mean():5.2f}% / Sh0 {g.sh0.mean():.2f} / DD {g.mdd.mean():6.2f}   dSh0 {d.mean():+.3f} ({int((d>0).sum())}/6)")
print("\n2015-25 ONLY and 6-anchor STAGGERED BLEND (equal-weight of the six anchor accounts), gold 8%/yr:")
for k, nm in SIZES.items():
    out = {}
    for lab, v in [("no gold", f"B0_{k}"), ("gold25@8%", f"G25_8_{k}")]:
        cs = [curve(v, a) for a in A]; start = max(c.index[0] for c in cs); cs = [c[start:] / c[start:].iloc[0] for c in cs]
        blend = pd.concat(cs, axis=1).mean(axis=1).pct_change().dropna(); r15 = [c["2015-01-01":].pct_change().dropna() for c in cs]
        out[lab] = dict(blend=mt(blend), y15=pd.DataFrame([mt(x) for x in r15]).mean())
    b, g = out["no gold"], out["gold25@8%"]
    print(f"  {nm:7s} blend: no-gold {b['blend']['CAGR']:.1f}% Sh0 {b['blend']['Sh0']:.2f} DD {b['blend']['MaxDD']:.1f} Calmar {b['blend']['Calmar']:.2f} | gold {g['blend']['CAGR']:.1f}% Sh0 {g['blend']['Sh0']:.2f} DD {g['blend']['MaxDD']:.1f} Calmar {g['blend']['Calmar']:.2f}   ||  2015-25: no-gold {b['y15'].CAGR:.1f}% Sh0 {b['y15'].Sh0:.2f} DD {b['y15'].MaxDD:.1f} | gold {g['y15'].CAGR:.1f}% Sh0 {g['y15'].Sh0:.2f} DD {g['y15'].MaxDD:.1f}")

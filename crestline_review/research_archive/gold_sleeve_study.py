"""Part A of PREREG_GOLD.md: gold/silver sleeve funded by the book's idle cash, exact post-processing of the stock engine's daily output."""
import os, sys, json, numpy as np, pandas as pd, gold_common as gc
pd.set_option("display.width", 250)
DIRS = json.load(open("dirs_gold_engine.json")); CAPS = ["c0", "c1", "c5", "c20"]; ANCH = [0, 10, 20, 30, 40, 50]
VARIANTS = ["G1", "G2", "G3", "G4", "G5", "G6"]; DEADBAND = 0.02
_cache = {}
def etf_ctx(sym, cal):
    k = (sym, cal[0], cal[-1], len(cal))
    if k not in _cache:
        c = gc.etf(sym).close; ssma, sper = gc.signals(c); r = gc.valid_returns(c, cal)
        prev = lambda s: s.reindex(cal).ffill(limit=3).shift(1).fillna(0.0).to_numpy()
        _cache[k] = dict(r=r.to_numpy(), valid=r.notna().to_numpy(), ssma=prev(ssma), sper=prev(sper), mean_excess=None)
    return _cache[k]
def drift_adjust(ctx, lam, lo="2007-03-01", hi="2025-12-31", cal=None):
    r = ctx["r"].copy()
    if lam > 0:
        m = np.nanmean(r) - gc.CASH_D; r = r - lam * m
    return np.where(ctx["valid"], r, 0.0)
def multiplier(variant, ctx, bear, panic):
    s = ctx["ssma"]; w = (bear | panic).astype(float)
    return {"G1": np.full(len(s), 0.5), "G2": s, "G3": ctx["sper"], "G4": s * np.where(w > 0, 1.0, 0.5), "G5": s * w, "G6": s}[variant]
def run_sleeve(daily, variant, ctx, lam=0.0, cost=0.0015, cap=None):
    cal = daily.index; rb = daily["eq"].pct_change().fillna(0.0).to_numpy(); idle = (1.0 - daily.expo).shift(1).fillna(1.0).clip(lower=0).to_numpy()
    bear = daily.bear.to_numpy().astype(bool); panic = daily.panic.to_numpy().astype(bool)
    m = multiplier(variant, ctx, bear, panic); rg = drift_adjust(ctx, lam); valid = ctx["valid"]
    cap_ = 0.10 if variant == "G6" else 1.0
    n = len(cal); a = np.zeros(n); tot = rb.copy(); cur = 0.0; traded = 0.0
    for t in range(n):
        tgt = min(idle[t] * m[t], cap_) if valid[t] else 0.0
        c0 = min(cur, idle[t]) if valid[t] else 0.0
        new = tgt if abs(tgt - c0) > DEADBAND else c0
        tr = abs(new - cur); traded += tr; cur = new; a[t] = cur
        tot[t] = rb[t] + cur * (rg[t] - gc.CASH_D) - cost * tr
    return pd.Series(tot, index=cal), pd.Series(a, index=cal), traded
def study(asset="GOLDBEES", variants=VARIANTS, lams=(0.0, 0.5, 1.0), costs=(0.0015,), window=None):
    out = []
    for cap in CAPS:
        for off in ANCH:
            daily = pd.read_csv(os.path.join(DIRS[f"B_{cap}|{off}"], "daily.csv"), index_col=0, parse_dates=True)
            if window: daily = daily[window[0]:window[1]]
            ctx = etf_ctx(asset, daily.index)
            base = gc.metrics(daily["eq"].pct_change().dropna()); out.append(dict(cap=cap, anchor=off, variant="G0", lam=0.0, cost=0.0, **base, avg_w=0.0, turn=0.0))
            for v in variants:
                for lam in lams:
                    for cost in costs:
                        r, a, tr = run_sleeve(daily, v, ctx, lam, cost)
                        out.append(dict(cap=cap, anchor=off, variant=v, lam=lam, cost=cost, **gc.metrics(r.iloc[1:]), avg_w=a.mean() * 100, turn=tr / ((daily.index[-1] - daily.index[0]).days / 365.25) * 100))
    return pd.DataFrame(out)
def gates(df):
    rows = []
    for cap in CAPS:
        for v in sorted(df.variant.unique()):
            if v == "G0": continue
            res = {}
            for lam in sorted(df.lam.unique()):
                for cost in sorted(df[df.variant == v].cost.unique()):
                    g = df[(df.cap == cap) & (df.variant == v) & (df.lam == lam) & (df.cost == cost)].set_index("anchor"); b = df[(df.cap == cap) & (df.variant == "G0")].set_index("anchor")
                    res[(lam, cost)] = dict(dSh=(g.Sh65 - b.Sh65).mean(), dA=(g.Sh65_A - b.Sh65_A).mean(), dB=(g.Sh65_B - b.Sh65_B).mean(), pos=int(((g.Sh65 - b.Sh65) > 0).sum()), dDD=(g.MaxDD - b.MaxDD).mean(), dCAGR=(g.CAGR - b.CAGR).mean(), w=g.avg_w.mean(), turn=g.turn.mean())
            costs = sorted(set(k[1] for k in res)); c1 = costs[0]; r0 = res[(0.0, c1)]; rh = res.get((0.5, c1)); rz = res.get((1.0, c1)); rc = res.get((0.0, costs[-1]))
            passed = (r0["dSh"] >= 0.08 and r0["dA"] > 0 and r0["dB"] > 0 and r0["pos"] >= 5 and r0["dDD"] >= -3 and rh["dSh"] >= 0.03 and rz["dSh"] >= -0.01 and rc["dSh"] > 0)
            rows.append(dict(cap=cap, variant=v, dCAGR=r0["dCAGR"], dSh65=r0["dSh"], dP_A=r0["dA"], dP_B=r0["dB"], anchors_pos=r0["pos"], dMaxDD=r0["dDD"], dSh_half=rh["dSh"], dSh_zero=rz["dSh"], dSh_cost30=rc["dSh"], avg_gold_w=r0["w"], turn=r0["turn"], PASS=passed))
    return pd.DataFrame(rows)
if __name__ == "__main__":
    df = study(costs=(0.0015, 0.0030)); df.to_csv("gold_sleeve_raw.csv", index=False)
    G = gates(df); G.to_csv("gold_sleeve_gates.csv", index=False)
    b = df[df.variant == "G0"].groupby("cap")[["CAGR", "Sh65", "MaxDD", "Sh65_A", "Sh65_B"]].mean(); print("G0 (idle cash in the liquid fund):"); print(b.round(2).to_string())
    for cap in CAPS: print(f"\n== book size {cap} =="); print(G[G.cap == cap].drop(columns="cap").round(3).to_string(index=False))

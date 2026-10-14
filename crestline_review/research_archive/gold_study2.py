"""PREREG_GOLD2.md: gold/silver sleeve vs idle cash at 0%, Sharpe rf=0, gold-return scenarios."""
import os, sys, json, numpy as np, pandas as pd, gold_common as gc
pd.set_option("display.width", 250)
DIRS = json.load(open("dirs_gold2_engine.json")); CAPS = ["c0", "c1", "c5", "c20"]; ANCH = [0, 10, 20, 30, 40, 50]; DEADBAND = 0.02
VARS = ["H1", "H2", "H3", "H4", "H5", "H6", "H7"]
def m0(r):
    r = r.dropna(); yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod(); f = lambda x: x.mean() / x.std() * np.sqrt(252) if len(x) > 50 else np.nan
    cagr = (eq.iloc[-1] ** (1 / yrs) - 1) * 100; dd = (eq / eq.cummax() - 1).min() * 100
    return dict(CAGR=cagr, Sh0=f(r), MaxDD=dd, Calmar=cagr / abs(dd), Sh0_A=f(r[:"2014-12-31"]), Sh0_B=f(r["2015-01-01":]))
_ctx = {}
def ctx(sym, cal):
    k = (sym, len(cal), cal[0], cal[-1])
    if k not in _ctx:
        c = gc.etf(sym).close; ssma, sper = gc.signals(c); r = gc.valid_returns(c, cal); prev = lambda s: s.reindex(cal).ffill(limit=3).shift(1).fillna(0.0).to_numpy()
        _ctx[k] = dict(r=r.to_numpy(), valid=r.notna().to_numpy(), ssma=prev(ssma), sper=prev(sper), first=c.index[0])
    return _ctx[k]
def sample_stats(sym):
    c = gc.etf(sym).close["2007-03-01":"2025-12-31"]; r = c.pct_change(fill_method=None); r[c.index.to_series().diff().dt.days > 5] = np.nan; r = r.dropna()
    yrs = (c.index[-1] - c.index[0]).days / 365.25
    return dict(mean_daily=r.mean(), ann_arith=r.mean() * 252 * 100, usable_days=len(r), point_to_point_cagr=((c.iloc[-1] / c.iloc[0]) ** (1 / yrs) - 1) * 100, vol=r.std() * np.sqrt(252) * 100)
STATS = {s: sample_stats(s) for s in ["GOLDBEES", "SILVERBEES"]}
FULL = STATS["GOLDBEES"]["point_to_point_cagr"] / 100
def scen_returns(cx, sym, target):          # target None = REAL; else re-centre the usable-day mean to the annual target
    r = cx["r"].copy()
    if target is not None: r = r - (STATS[sym]["mean_daily"] - ((1 + target) ** (1 / 252) - 1))
    return np.where(cx["valid"], r, 0.0)
def run(daily, v, cg, cs, target, cost=0.0015):
    cal = daily.index; rb = daily["eq"].pct_change().fillna(0.0).to_numpy(); idle = (1.0 - daily.expo).shift(1).fillna(1.0).clip(lower=0).to_numpy()
    bear = (daily.bear | daily.panic).to_numpy().astype(bool); n = len(cal)
    rg = scen_returns(cg, "GOLDBEES", target); rs = scen_returns(cs, "SILVERBEES", target)
    sg, sp = cg["ssma"], cg["sper"]; ss = cs["ssma"]
    s_first = cs["first"]; s_avail = np.array(cal >= s_first + pd.Timedelta(days=330))
    mg = {"H1": np.ones(n), "H2": np.full(n, 0.5), "H3": sg, "H4": sp, "H5": sg * np.where(bear, 1.0, 0.5), "H7": sg}.get(v)
    if v == "H6": mg = np.where(s_avail, 0.5 * sg, sg); ms = np.where(s_avail, 0.5 * ss, 0.0)
    else: ms = np.zeros(n)
    cap = 0.10 if v == "H7" else 1.0; tot = rb.copy(); curg = curs = 0.0; traded = 0.0; wsum = 0.0
    vg = cg["valid"]; vs = cs["valid"] & s_avail
    for t in range(n):
        tg = min(idle[t] * mg[t], cap) if vg[t] else 0.0; ts = idle[t] * ms[t] if vs[t] else 0.0
        if tg + ts > idle[t]: sc = idle[t] / (tg + ts); tg, ts = tg * sc, ts * sc
        cg0 = min(curg, idle[t]) if vg[t] else 0.0; cs0 = min(curs, max(idle[t] - cg0, 0.0)) if vs[t] else 0.0
        ng = tg if abs(tg - cg0) > DEADBAND else cg0; ns = ts if abs(ts - cs0) > DEADBAND else cs0
        tr = abs(ng - curg) + abs(ns - curs); traded += tr; curg, curs = ng, ns
        tot[t] = rb[t] + curg * rg[t] + curs * rs[t] - cost * tr; wsum += curg + curs
    yrs = (cal[-1] - cal[0]).days / 365.25
    return pd.Series(tot, index=cal), wsum / n * 100, traded / yrs * 100
SCEN = {"REAL": None, "FULL": FULL, "8%": 0.08, "4%": 0.04, "0%": 0.0}
def study(variants=VARS, scen=SCEN, costs=(0.0015,)):
    out = []
    for cap in CAPS:
        for off in ANCH:
            d = pd.read_csv(os.path.join(DIRS[f"B0_{cap}|{off}"], "daily.csv"), index_col=0, parse_dates=True); cg = ctx("GOLDBEES", d.index); cs = ctx("SILVERBEES", d.index)
            out.append(dict(cap=cap, anchor=off, variant="G0", scen="-", cost=0.0, avg_w=0.0, turn=0.0, **m0(d["eq"].pct_change().dropna())))
            for v in variants:
                for sn, tg in scen.items():
                    for c in costs:
                        r, w, tr = run(d, v, cg, cs, tg, c); out.append(dict(cap=cap, anchor=off, variant=v, scen=sn, cost=c, avg_w=w, turn=tr, **m0(r.iloc[1:])))
    return pd.DataFrame(out)
def delta(df, cap, v, sn, cost=0.0015):
    g = df[(df.cap == cap) & (df.variant == v) & (df.scen == sn) & (df.cost == cost)].set_index("anchor"); b = df[(df.cap == cap) & (df.variant == "G0")].set_index("anchor")
    return dict(dSh0=(g.Sh0 - b.Sh0).mean(), dA=(g.Sh0_A - b.Sh0_A).mean(), dB=(g.Sh0_B - b.Sh0_B).mean(), pos=int(((g.Sh0 - b.Sh0) > 0).sum()), dDD=(g.MaxDD - b.MaxDD).mean(), dCAGR=(g.CAGR - b.CAGR).mean(),
                dCalmar=(g.Calmar - b.Calmar).mean(), CAGR=g.CAGR.mean(), Sh0=g.Sh0.mean(), MaxDD=g.MaxDD.mean(), w=g.avg_w.mean(), turn=g.turn.mean())
def gates(df):
    rows = []
    for cap in CAPS:
        for v in VARS:
            p = delta(df, cap, v, "8%"); lo = delta(df, cap, v, "4%"); c30 = delta(df, cap, v, "8%", 0.0030)
            ok = (p["dSh0"] >= 0.08, p["dA"] > 0 and p["dB"] > 0, p["pos"] >= 5, p["dDD"] >= -3, lo["dSh0"] > 0, c30["dSh0"] >= 0.05)
            rows.append(dict(cap=cap, variant=v, dCAGR_8=p["dCAGR"], dSh0_8=p["dSh0"], dA=p["dA"], dB=p["dB"], anch=p["pos"], dMaxDD_8=p["dDD"], dCalmar_8=p["dCalmar"], dSh0_4=lo["dSh0"], dSh0_cost30=c30["dSh0"], w=p["w"], turn=p["turn"],
                             K1=ok[0], K2=ok[1], K3=ok[2], K4=ok[3], K5=ok[4], K6=ok[5], PASS=all(ok)))
    return pd.DataFrame(rows)
if __name__ == "__main__":
    print("SAMPLE STATS (usable days 2007-03..2025-12):"); print(pd.DataFrame(STATS).T.round(2).to_string()); print(f"FULL-HISTORY gold CAGR used for scenario FULL: {FULL*100:.1f}%\n")
    df = study(costs=(0.0015, 0.0030)); df.to_csv("gold2_raw.csv", index=False); G = gates(df); G.to_csv("gold2_gates.csv", index=False)
    print("G0' (idle cash 0%):"); print(df[df.variant == "G0"].groupby("cap")[["CAGR", "Sh0", "MaxDD", "Calmar", "Sh0_A", "Sh0_B"]].mean().loc[CAPS].round(2).to_string())
    cols = ["variant", "dCAGR_8", "dSh0_8", "dA", "dB", "anch", "dMaxDD_8", "dCalmar_8", "dSh0_4", "dSh0_cost30", "w", "turn", "K1", "K2", "K3", "K4", "K5", "K6", "PASS"]
    for cap in CAPS: print(f"\n== book size {cap} (planning scenario: gold/silver return 8%/yr) =="); print(G[G.cap == cap][cols].round(3).to_string(index=False))
    print("\nPASS count by variant:", G.groupby("variant").PASS.sum().to_dict())

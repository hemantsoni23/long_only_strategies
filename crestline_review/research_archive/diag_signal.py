"""Signal diagnostics over time (PREREG_DIAG.md). usage: python3 diag_signal.py"""
import numpy as np, pandas as pd
D = np.load("diag/diag.npz", allow_pickle=True); close = np.load("diag/close.npy"); opn = np.load("diag/open.npy")
me_pos = D["me_pos"]; dates = pd.to_datetime(D["dates"]); score = D["score"].astype(float); pool = D["pool"]; hp = D["hp"].astype(float); tp = D["tp"].astype(float)
alld = pd.to_datetime(D["all_dates"]); nb = len(alld); H = [5, 10, 20, 40, 60, 90, 120, 180, 252]; TOPN = 25
def rank_rows(x):  # rank within row, NaN-safe (mean rank not needed: continuous scores)
    out = np.full(x.shape, np.nan); 
    for i in range(x.shape[0]):
        m = ~np.isnan(x[i]); 
        if m.sum() > 2: out[i, m] = pd.Series(x[i, m]).rank().to_numpy()
    return out
def nw_t(x, lags):
    x = np.asarray(x, float); x = x[~np.isnan(x)]; n = len(x)
    if n < 8: return np.nan
    xc = x - x.mean(); s = xc @ xc / n
    for l in range(1, min(lags, n - 1) + 1): s += 2 * (1 - l / (lags + 1)) * (xc[l:] @ xc[:-l] / n)
    return x.mean() / np.sqrt(s / n) if s > 0 else np.nan
# forward returns per (row, h)
n_r, n_s = score.shape
fwd = {h: np.full((n_r, n_s), np.nan) for h in H}
for i, p in enumerate(me_pos):
    o = opn[p + 1] if p + 1 < nb else None
    if o is None: continue
    o = np.where(np.isnan(o) | (o <= 0), close[p], o)
    for h in H:
        if p + h < nb: fwd[h][i] = close[p + h] / o - 1.0
R_sc = rank_rows(np.where(pool, score, np.nan)); R_hp = rank_rows(np.where(pool & ~np.isnan(hp), hp, np.nan)); R_tp = rank_rows(np.where(pool & ~np.isnan(tp), tp, np.nan))
def ic_series(Rx, h):
    out = np.full(n_r, np.nan)
    for i in range(n_r):
        f = fwd[h][i]; m = ~np.isnan(Rx[i]) & ~np.isnan(f)
        if m.sum() < 30: continue
        a = Rx[i, m]; b = pd.Series(f[m]).rank().to_numpy(); a = a - a.mean(); b = b - b.mean()
        out[i] = (a @ b) / np.sqrt((a @ a) * (b @ b))
    return out
IC = {("score", h): ic_series(R_sc, h) for h in H}
for nm, Rx in [("HP", R_hp), ("TP", R_tp)]:
    for h in [20, 60, 120]: IC[(nm, h)] = ic_series(Rx, h)
# top-N / top-decile excess vs pool mean
TOPX = {}
for h in H:
    ex = np.full(n_r, np.nan); dx = np.full(n_r, np.nan); sp = np.full(n_r, np.nan)
    for i in range(n_r):
        f = fwd[h][i]; m = ~np.isnan(R_sc[i]) & ~np.isnan(f)
        if m.sum() < 100: continue
        s = R_sc[i, m]; ff = f[m]; order = np.argsort(-s); n = len(ff)
        ex[i] = ff[order[:TOPN]].mean() - ff.mean(); k = max(n // 10, 1)
        dx[i] = ff[order[:k]].mean() - ff.mean(); sp[i] = ff[order[:k]].mean() - ff[order[-k:]].mean()
    TOPX[h] = (ex, dx, sp)
blocks = [("2006-03..2008", "2006-01-01", "2008-12-31"), ("2009..2011", "2009-01-01", "2011-12-31"), ("2012..2014", "2012-01-01", "2014-12-31"), ("2015..2017", "2015-01-01", "2017-12-31"),
          ("2018..2020", "2018-01-01", "2020-12-31"), ("2021..2023", "2021-01-01", "2023-12-31"), ("2024..2025", "2024-01-01", "2025-12-31"), ("ALL", "2006-01-01", "2025-12-31")]
def summ(series, h, mask):
    x = series[mask]; x = x[~np.isnan(x)]
    if len(x) < 8: return dict(n=len(x), mean=np.nan, std=np.nan, icir=np.nan, hit=np.nan, t=np.nan)
    return dict(n=len(x), mean=x.mean(), std=x.std(ddof=1), icir=x.mean() / x.std(ddof=1), hit=(x > 0).mean() * 100, t=nw_t(x, int(np.ceil(h / 5))))
rows = []
for name, a, b in blocks:
    mk = (dates >= a) & (dates <= b)
    for h in H:
        r = dict(block=name, h=h, **summ(IC[("score", h)], h, mk)); ex, dx, sp = TOPX[h]
        e = ex[mk]; e = e[~np.isnan(e)]; r.update(top25_excess=e.mean() * 100 if len(e) else np.nan, top25_t=nw_t(e, int(np.ceil(h / 5))) if len(e) > 8 else np.nan,
                                                   topdec_excess=np.nanmean(dx[mk]) * 100, decile_spread=np.nanmean(sp[mk]) * 100)
        rows.append(r)
B = pd.DataFrame(rows); B.to_csv("diag_ic_blocks.csv", index=False)
legs = []
for name, a, b in blocks:
    mk = (dates >= a) & (dates <= b)
    for leg in ["score", "HP", "TP"]:
        for h in [20, 60, 120]:
            legs.append(dict(block=name, leg=leg, h=h, **summ(IC[(leg, h)], h, mk)))
L = pd.DataFrame(legs); L.to_csv("diag_ic_legs.csv", index=False)
# rolling 3y
rr = []
for y in range(2006, 2023):
    mk = (dates >= f"{y}-01-01") & (dates <= f"{y+2}-12-31")
    for h in [20, 60, 120]:
        rr.append(dict(start=y, h=h, **summ(IC[("score", h)], h, mk)))
RL = pd.DataFrame(rr); RL.to_csv("diag_ic_rolling.csv", index=False)
pd.set_option("display.width", 250)
print("== IC by 3-year block (score) ==")
for h in [20, 60, 120, 252]:
    print(f"\n-- horizon {h} bars --"); print(B[B.h == h].drop(columns="h").set_index("block").round(3).to_string())
print("\n== all-sample IC curve =="); print(B[B.block == "ALL"].set_index("h")[["n", "mean", "std", "icir", "hit", "t", "top25_excess", "top25_t", "topdec_excess", "decile_spread"]].round(3).to_string())
print("\n== legs =="); print(L[L.h.isin([60, 120])].pivot_table(index="block", columns=["leg", "h"], values="mean").round(3).to_string())
print("\n== rolling 3y IC =="); print(RL.pivot_table(index="start", columns="h", values=["mean", "t"]).round(3).to_string())
# verdict
def verdict(h):
    s = []
    for name, *_ in blocks[:7]:
        r = B[(B.block == name) & (B.h == h)].iloc[0]; s.append("WORKING" if (r["mean"] > 0 and r.t >= 2) else ("WEAK" if r["mean"] > 0 else "BROKEN"))
    return s
for h in [60, 120]:
    s = verdict(h); print(f"\nh={h}: {dict(zip([b[0] for b in blocks[:7]], s))}  working {s.count('WORKING')}/7 broken {s.count('BROKEN')}")
    f = B[(B.h == h) & B.block.isin(["2006-03..2008", "2009..2011"])]["mean"].mean(); l = B[(B.h == h) & B.block.isin(["2018..2020", "2021..2023"])]["mean"].mean()
    print(f"   first-two-block mean IC {f:.3f}  last-two-full-block mean IC {l:.3f}  ratio {l/f:.2f}  ->", "DECAYING" if l < 0.5 * f else "not decaying")
np.savez("diag/fwd_cache.npz", **{f"f{h}": fwd[h].astype(np.float32) for h in H})

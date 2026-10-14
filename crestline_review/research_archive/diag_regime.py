"""T5: do simple market-state variables predict the long-only top-25 payoff? (PREREG_STRUCT.md T5)"""
import numpy as np, pandas as pd
D = np.load("diag/diag.npz", allow_pickle=True); close = np.load("diag/close.npy").astype(np.float32); F = np.load("diag/fwd_cache.npz")
alld = pd.to_datetime(D["all_dates"]); me_pos = D["me_pos"]; dates = pd.to_datetime(D["dates"]); score = D["score"].astype(float); pool = D["pool"]
bench = pd.Series(D["bench"], index=alld); f60 = F["f60"].astype(float)
n = len(me_pos); y = np.full(n, np.nan); sp = np.full(n, np.nan)
for i in range(n):
    f = f60[i]; m = pool[i] & ~np.isnan(f) & ~np.isnan(score[i])
    if m.sum() < 100: continue
    s = score[i][m]; ff = f[m]; o = np.argsort(-s); k = max(m.sum() // 10, 1)
    y[i] = ff[o[:25]].mean() - ff.mean(); sp[i] = ff[o[:k]].mean() - ff[o[-k:]].mean()
sma200 = bench.rolling(200, min_periods=150).mean(); r21 = bench.pct_change().rolling(21).std()
sma50 = pd.DataFrame(close).rolling(50, min_periods=40).mean().to_numpy(dtype=np.float32)
S = {}
S["bench_above_sma200"] = np.array([float(bench.iloc[p] > sma200.iloc[p]) if not np.isnan(sma200.iloc[p]) else np.nan for p in me_pos])
S["bench_ret_126"] = np.array([bench.iloc[p] / bench.iloc[p - 126] - 1 if p >= 126 else np.nan for p in me_pos])
S["bench_dd_252"] = np.array([bench.iloc[p] / bench.iloc[max(p - 251, 0):p + 1].max() - 1 for p in me_pos])
disp, brd, vol = [], [], []
for i, p in enumerate(me_pos):
    idx = np.where(pool[i])[0]; c0 = close[p - 60, idx] if p >= 60 else None
    disp.append(np.nanstd(close[p, idx] / c0 - 1) if c0 is not None else np.nan); brd.append(np.nanmean(close[p, idx] > sma50[p, idx]))
    vol.append(r21.iloc[p])
S["dispersion_60"] = np.array(disp); S["breadth_sma50"] = np.array(brd)
v = pd.Series(vol); S["bench_vol_21_pctile"] = v.expanding(min_periods=100).apply(lambda a: (a[:-1] < a[-1]).mean() if len(a) > 1 else np.nan, raw=True).to_numpy()
def hac_t_slope(x, yv, lags=12):
    m = ~np.isnan(x) & ~np.isnan(yv); x = x[m]; yv = yv[m]; n_ = len(x)
    if n_ < 40: return np.nan, np.nan
    xs = (x - x.mean()) / (x.std() + 1e-12); X = np.c_[np.ones(n_), xs]; beta = np.linalg.lstsq(X, yv, rcond=None)[0]; e = yv - X @ beta
    u = X * e[:, None]; S0 = u.T @ u / n_
    for l in range(1, lags + 1): G = u[l:].T @ u[:-l] / n_; S0 += (1 - l / (lags + 1)) * (G + G.T)
    XtXi = np.linalg.inv(X.T @ X / n_); V = XtXi @ S0 @ XtXi / n_
    return beta[1], beta[1] / np.sqrt(V[1, 1])
rows = []
half = dates < "2015-01-01"
for nm, x in S.items():
    for out, yy in [("top25_excess", y), ("decile_spread", sp)]:
        m = ~np.isnan(x) & ~np.isnan(yy); rho = pd.Series(x[m]).corr(pd.Series(yy[m]), method="spearman")
        b, t = hac_t_slope(x, yy); _, tA = hac_t_slope(np.where(half, x, np.nan), yy); _, tB = hac_t_slope(np.where(~half, x, np.nan), yy)
        bA, _ = hac_t_slope(np.where(half, x, np.nan), yy); bB, _ = hac_t_slope(np.where(~half, x, np.nan), yy)
        rows.append(dict(state=nm, outcome=out, n=int(m.sum()), spearman=rho, slope_pct_per_sd=b * 100, hac_t=t, t_2006_14=tA, t_2015_25=tB, same_sign=np.sign(bA) == np.sign(bB)))
R = pd.DataFrame(rows); R["predicts"] = (R.spearman.abs() >= 0.15) & (R.hac_t.abs() >= 3) & R.same_sign
pd.set_option("display.width", 250); print(R.round(3).to_string(index=False)); R.to_csv("diag_regime.csv", index=False)
# block context
print("\nBLOCK CONTEXT (signal-date means)")
blocks = [("2006-03..2008", "2006-01-01", "2008-12-31"), ("2009..2011", "2009-01-01", "2011-12-31"), ("2012..2014", "2012-01-01", "2014-12-31"), ("2015..2017", "2015-01-01", "2017-12-31"),
          ("2018..2020", "2018-01-01", "2020-12-31"), ("2021..2023", "2021-01-01", "2023-12-31"), ("2024..2025", "2024-01-01", "2025-12-31")]
rows = []
for nm, a, b in blocks:
    mk = (dates >= a) & (dates <= b); br = bench[a:b]; yrs = (br.index[-1] - br.index[0]).days / 365.25
    rows.append(dict(block=nm, top25_exc60=np.nanmean(y[mk]) * 100, spread60=np.nanmean(sp[mk]) * 100, market_cagr=((br.iloc[-1] / br.iloc[0]) ** (1 / yrs) - 1) * 100, market_maxdd=((br / br.cummax()) - 1).min() * 100,
                     pct_bull=np.nanmean(S["bench_above_sma200"][mk]) * 100, dispersion=np.nanmean(S["dispersion_60"][mk]), breadth=np.nanmean(S["breadth_sma50"][mk]) * 100))
print(pd.DataFrame(rows).round(2).to_string(index=False))

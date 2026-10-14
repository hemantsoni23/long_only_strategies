"""PREREG_DIAG item 6: pure-signal hold-H portfolios, no stops. top-25 equal weight, K=H/20 staggered sub-portfolios, 0.3%/side, 
ungated (fully invested) and bear-gated (cash at 6.5% when EW benchmark < SMA200 at formation)."""
import numpy as np, pandas as pd
D = np.load("diag/diag.npz", allow_pickle=True); close = np.load("diag/close.npy").astype(float); opn = np.load("diag/open.npy").astype(float)
alld = pd.to_datetime(D["all_dates"]); nb = len(alld); me_pos = D["me_pos"]; score = D["score"].astype(float); pool = D["pool"]; bench = pd.Series(D["bench"], index=alld)
sma = bench.rolling(200, min_periods=150).mean(); bear_at = (bench < sma).to_numpy()
COST, TOPN, RF = 0.003, 25, 0.065; cash_d = (1 + RF) ** (1 / 252) - 1
def tranche(i, H):
    p = me_pos[i]; e = p + 1
    if e >= nb - 1: return None
    s = np.where(pool[i], score[i], np.nan); o = opn[e]; ok = ~np.isnan(s) & (o > 0) & ~np.isnan(o) & ~np.isnan(close[e])
    if ok.sum() < 60: return None
    idx = np.where(ok)[0]; pick = idx[np.argsort(-s[idx])[:TOPN]]
    end = min(e + H - 1, nb - 1); V = np.nanmean(close[e:end + 1][:, pick] / o[pick], axis=1) * (1 - COST)
    r = np.empty(len(V)); r[0] = V[0] - 1; r[1:] = V[1:] / V[:-1] - 1
    if e + H - 1 <= nb - 1: r[-1] = (1 + r[-1]) * (1 - COST) - 1
    return e, r
def sub_returns(j, H, gated):
    ret = np.full(nb, np.nan); step = H // 5; i = j * 4
    while i < len(me_pos):
        p = me_pos[i]; e = p + 1
        if e >= nb - 1: break
        end = min(e + H - 1, nb - 1)
        if gated and bear_at[p]: ret[e:end + 1] = cash_d
        else:
            t = tranche(i, H)
            if t is None: i += step; continue
            ret[t[0]:t[0] + len(t[1])] = t[1]
        i += step
    return ret
def run(H, gated, start):
    K = H // 20; R = np.vstack([sub_returns(j, H, gated) for j in range(K)])
    R = R[:, start:]; eq = np.cumprod(1 + np.nan_to_num(R, nan=0.0), axis=1)  # subs not yet started hold cash flat (0 return) until their first tranche
    tot = eq.mean(axis=0); r = pd.Series(tot, index=alld[start:]).pct_change().dropna(); return r
def metrics(r):
    yrs = (r.index[-1] - r.index[0]).days / 365.25; eq = (1 + r).cumprod()
    f = lambda x: dict(Sh0=x.mean() / x.std() * np.sqrt(252), Sh65=(x.mean() - cash_d) / x.std() * np.sqrt(252))
    d = dict(CAGR=(eq.iloc[-1] ** (1 / yrs) - 1) * 100, Vol=r.std() * np.sqrt(252) * 100, **f(r), MaxDD=(eq / eq.cummax() - 1).min() * 100)
    d["Sh65_A"] = f(r[:"2014-12-31"])["Sh65"]; d["Sh65_B"] = f(r["2015-01-01":])["Sh65"]; return d
start = int(me_pos[0]) + 1 + 12 * 20     # common window: after the slowest (K=12) sub-portfolio has started
mk = bench.pct_change().dropna()[alld[start]:]
rows = [dict(H="market (EW pool)", **metrics(mk))]
for H in [20, 40, 60, 100, 120, 180, 240]:
    for g in [False, True]:
        rows.append(dict(H=f"{H}{' gated' if g else ''}", **metrics(run(H, g, start))))
T = pd.DataFrame(rows).set_index("H"); pd.set_option("display.width", 250)
print(f"window {alld[start].date()} .. {alld[-1].date()}  (identical for every row)"); print(T.round(2).to_string()); T.to_csv("diag_hold_portfolios.csv")

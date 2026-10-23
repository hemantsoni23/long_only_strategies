"""Validation battery for the HR / VCP backtests: reconstruct from trade log, outlier dependence, liquidity cap, costs, artifacts."""
import sys, os, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels(); close = P['close'].ffill(); raw = P['close']; vol = P['volume']
dvol = (P['close'] * vol).rolling(63, min_periods=21).median().shift(1)       # rupee ADV known at entry
dates = close.index; col = {s: j for j, s in enumerate(close.columns)}
CL = close.values; RET = close.pct_change().values
def replay(tl, w_scale=None, cost=0.003, drop=None, C0=None, adv_cap=None):
    """Equity simulation from the trade log with DRIFTING positions (shares fixed after entry, like the engine).
    v0 = Weight * equity_prev (or min(that, adv_cap_i) when a rupee liquidity cap is given; equity starts at C0 rupees)."""
    n = len(dates); di = {d: i for i, d in enumerate(dates)}
    paths = {}; starts = {}; ends = {}
    for k, t in enumerate(tl.itertuples()):
        if drop is not None and k in drop: continue
        j = col.get(t.Ticker); ie = di.get(pd.Timestamp(t.Entry_Date)); ix = di.get(pd.Timestamp(t.Exit_Date))
        if j is None or ie is None or ix is None: continue
        if ie == ix: p = np.array([t.Exit_Price / t.Entry_Price - 1])
        else:
            p = np.empty(ix - ie + 1); p[0] = CL[ie, j] / t.Entry_Price - 1
            if ix - ie > 1: p[1:-1] = np.nan_to_num(RET[ie + 1:ix, j])
            p[-1] = t.Exit_Price / CL[ix - 1, j] - 1
        paths[k] = np.clip(np.nan_to_num(p), -0.99, 5.0); starts.setdefault(ie, []).append(k); ends[k] = ix
    E = 1.0 if C0 is None else C0; eq = np.empty(n); rets = np.zeros(n); active = {}
    W = tl.Weight.values
    for i in range(n):
        e0 = E; pnl = 0.0
        for k in starts.get(i, []):
            v = W[k] * e0 * (1.0 if w_scale is None else w_scale[k])
            if adv_cap is not None: v = min(v, adv_cap[k])
            active[k] = [v, 0]; pnl -= v * cost
        done = []
        for k, a in active.items():
            idx = i - (ends[k] - len(paths[k]) + 1)
            r = paths[k][idx]; pnl += a[0] * r; a[0] *= (1 + r)
            if i == ends[k]: pnl -= a[0] * cost; done.append(k)
        for k in done: del active[k]
        E = e0 + pnl; rets[i] = pnl / e0 if e0 else 0.0; eq[i] = E
    return pd.Series(rets, index=dates), pd.Series(eq, index=dates)
def stats(r, label=''):
    r = r[r.index >= r[r != 0].index.min()]
    yrs = len(r) / 252; eq = (1 + r).cumprod()
    return dict(label=label, cagr=eq.iloc[-1] ** (1 / yrs) - 1, sharpe=r.mean() / r.std() * np.sqrt(252), maxdd=(eq / eq.cummax() - 1).min())
out = {}
for w in ('hr', 'vcp'):
    d = pickle.load(open(f'{C.CACHE}/bt_{w}_cy0.0.pkl', 'rb')); tl = d['trades'].reset_index(drop=True)
    tl['Entry_Date'] = pd.to_datetime(tl['Entry_Date']); tl['Exit_Date'] = pd.to_datetime(tl['Exit_Date'])
    rows = [stats(d['net'], 'engine (0% cash)')]
    base, ex = replay(tl); rows.append(stats(base, 'trade-log replay (drifting)'))
    print(w, 'replay vs engine daily corr', round(np.corrcoef(base.reindex(d['net'].index).fillna(0), d['net'].fillna(0))[0, 1], 4))
    # outlier dependence
    order = tl.PnL_Abs.sort_values(ascending=False).index
    for k in (5, 10, 25):
        r, _ = replay(tl, drop=set(order[:k])); rows.append(stats(r, f'drop top {k} winners'))
    for pct in (0.01, 0.05):
        r, _ = replay(tl, drop=set(order[:int(len(tl) * pct)])); rows.append(stats(r, f'drop top {int(pct*100)}% winners'))
    # costs
    for c in (0.006, 0.010):
        r, _ = replay(tl, cost=c); rows.append(stats(r, f'cost {c*100:.1f}% one-way'))
    # liquidity cap at fixed capital C
    adv = np.array([dvol.iat[di, col[t]] if t in col else np.nan for t, di in zip(tl.Ticker, [dates.get_indexer([e])[0] for e in tl.Entry_Date])])
    for Ccr in (1, 10, 50):
        capr = 0.05 * adv                                    # max rupee position = 5% of 63d median rupee ADV
        r, eq = replay(tl, C0=Ccr * 1e7, adv_cap=np.nan_to_num(capr, nan=0.0)); s_ = stats(r, f'liquidity cap 5% ADV, start Rs{Ccr}cr (compounding)'); s_['final_Rs_cr'] = float(eq.iloc[-1] / 1e7); rows.append(s_)
    # artifacts: single-day moves inside hold
    flag = []
    for k, t in enumerate(tl.itertuples()):
        j = col.get(t.Ticker); ie = dates.get_indexer([t.Entry_Date])[0]; ix = dates.get_indexer([t.Exit_Date])[0]
        seg = RET[ie + 1:ix + 1, j] if j is not None else np.array([])
        flag.append(np.nanmax(np.abs(seg)) if len(seg) else 0)
    tl['max_1d_move'] = flag
    out[w] = (pd.DataFrame(rows), tl)
    print(pd.DataFrame(rows).round(3).to_string()); 
    print(w, 'trades with an in-hold 1-day |move| > 25%:', int((tl.max_1d_move > .25).sum()), 'of', len(tl), '| their share of total PnL_Abs:', round(tl.loc[tl.max_1d_move > .25, 'PnL_Abs'].sum() / tl.PnL_Abs.sum(), 3))
    print(w, 'median participation proxy: weight*C/ADV at Rs10cr =', round(float(np.nanmedian(tl.Weight.values * 10e7 / adv)), 3), '| share of trades >10% ADV @10cr:', round(float(np.nanmean(tl.Weight.values * 10e7 / adv > .10)), 3))
pickle.dump({k: v[0] for k, v in out.items()}, open(f'{C.OUT}/bt_checks.pkl', 'wb'))
for k, v in out.items(): v[0].to_csv(f'{C.OUT}/bt_checks_{k}.csv', index=False)

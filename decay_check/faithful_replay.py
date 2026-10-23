"""Faithful re-booking of a breakout backtest from its trade log: drifting positions (shares fixed), entry-day open->close,
exit-day prev-close->fill CHARGED, gross exposure capped at 100% of equity, costs on both legs. Equity starts at 1.0 (or C0 rupees)."""
import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
_P = None
def panels():
    global _P
    if _P is None:
        P = C.load_panels(); cl = P['close'].ffill()
        _P = dict(dates=cl.index, col={s: j for j, s in enumerate(cl.columns)}, CL=cl.values, RET=cl.pct_change().values,
                  adv=(P['close'] * P['volume']).rolling(63, min_periods=21).median().shift(1), bench_ret=P['bench_ret'])
    return _P
def replay(tl, cost=0.003, drop=None, C0=None, adv_frac=None, cap_gross=1.0, weight_mult=1.0, exits_first=False):
    p = panels(); dates, col, CL, RET, advdf = p['dates'], p['col'], p['CL'], p['RET'], p['adv']
    n = len(dates); di = {d: i for i, d in enumerate(dates)}
    tl = tl.reset_index(drop=True); paths = {}; starts = {}; ends = {}; advv = {}
    for k, t in enumerate(tl.itertuples()):
        if drop is not None and k in drop: continue
        j = col.get(t.Ticker); ie = di.get(pd.Timestamp(t.Entry_Date)); ix = di.get(pd.Timestamp(t.Exit_Date))
        if j is None or ie is None or ix is None: continue
        if ie == ix: q = np.array([t.Exit_Price / t.Entry_Price - 1])
        else:
            q = np.empty(ix - ie + 1); q[0] = CL[ie, j] / t.Entry_Price - 1
            if ix - ie > 1: q[1:-1] = np.nan_to_num(RET[ie + 1:ix, j])
            q[-1] = t.Exit_Price / CL[ix - 1, j] - 1
        paths[k] = np.clip(np.nan_to_num(q), -0.99, 5.0); starts.setdefault(ie, []).append(k); ends[k] = ix
        if adv_frac is not None: advv[k] = advdf.iat[ie, j] if not np.isnan(advdf.iat[ie, j]) else 0.0
    E = 1.0 if C0 is None else float(C0); rets = np.zeros(n); expo = np.zeros(n); active = {}
    W = tl.Weight.values
    for i in range(n):
        e0 = E; pnl = 0.0
        if exits_first:
            for k in [k for k in list(active) if ends[k] == i]:
                a = active[k]; idx = i - (ends[k] - len(paths[k]) + 1); r = paths[k][idx]; pnl += a[0] * r; a[0] *= (1 + r); pnl -= a[0] * cost; del active[k]
        new = starts.get(i, [])
        if new:
            want = {k: W[k] * weight_mult * e0 for k in new}
            if adv_frac is not None: want = {k: min(v, adv_frac * advv[k]) for k, v in want.items()}
            room = max(0.0, cap_gross * e0 - sum(a[0] for a in active.values())); tot = sum(want.values())
            sc = min(1.0, room / tot) if tot > 0 else 0.0
            for k, v in want.items():
                active[k] = [v * sc]; pnl -= v * sc * cost
        done = []; gross = 0.0
        for k, a in active.items():
            idx = i - (ends[k] - len(paths[k]) + 1); r = paths[k][idx]; pnl += a[0] * r; a[0] *= (1 + r); gross += a[0]
            if i == ends[k]: pnl -= a[0] * cost; done.append(k)
        for k in done: del active[k]
        E = e0 + pnl; rets[i] = pnl / e0 if e0 else 0.0; expo[i] = gross / E if E else 0.0
    return pd.Series(rets, index=dates), pd.Series(expo, index=dates)
def chunk_stats(r, first, bench):
    rows = []
    for lab, s, e in C.chunk_bounds(first) + [('ALL', first, C.ANCHOR)]:
        x = r.loc[(s + 1).to_timestamp():(e + 1).to_timestamp(how='end')]
        if len(x) < 100: continue
        yrs = len(x) / 252; eq = (1 + x).cumprod(); b = bench.reindex(x.index).fillna(0)
        rows.append(dict(chunk=lab, cagr=eq.iloc[-1] ** (1 / yrs) - 1, bench_cagr=(1 + b).prod() ** (1 / yrs) - 1,
                         sharpe=x.mean() / x.std() * np.sqrt(252), maxdd=(eq / eq.cummax() - 1).min(),
                         excess_nw_t=C.nw_t(x - b, 10)))
    return pd.DataFrame(rows)

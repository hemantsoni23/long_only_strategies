import numpy as np, pandas as pd
def met(r, a='2005-01-01', b=None):
    r = r.loc[a:b] if b else r.loc[a:]; r = r[r.index >= r[r != 0].index.min()]; yrs = len(r) / 252; eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
    ep, cur = [], 0.0
    for v in dd.values:
        if v < 0: cur = min(cur, v)
        else:
            if cur < -0.02: ep.append(cur)
            cur = 0.0
    if cur < -0.02: ep.append(cur)
    m12 = (1 + r).rolling(252).apply(np.prod, raw=True) - 1; cagr = eq.iloc[-1] ** (1 / yrs) - 1
    return dict(cagr=cagr, sharpe=r.mean() / r.std() * np.sqrt(252), maxdd=dd.min(), calmar=cagr / abs(dd.min()), avg_dd=float(np.mean(ep)) if ep else 0.0, stab=float(m12.std()))

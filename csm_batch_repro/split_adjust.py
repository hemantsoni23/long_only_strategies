"""Detect unadjusted splits/bonuses/consolidations in raw OHLCV and back-adjust. Conservative:
event if close and open both jump by (nearly) the same standard corporate-action ratio."""
import numpy as np, pandas as pd
RATIOS = np.array([1/2, 2/3, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/20, 1/50, 3/4, 4/5,
                   2.0, 1.5, 3.0, 4.0, 5.0, 10.0, 20.0])
def detect(p, op, v=None, tol=0.04, min_move=0.20, ratios=None, vol_sig=True):
    pc = p.ffill().shift(1)
    rc = p / pc
    ro = op / pc
    ev = pd.DataFrame(1.0, index=p.index, columns=p.columns)
    big = ((rc < 1 - 0.30) | (rc > 1 / (1 - 0.30)))      # |move| beyond circuit-ish (-30% / +43%)
    ratios = RATIOS if ratios is None else np.asarray(ratios)
    if vol_sig and v is not None:
        vb = v.where(v > 0).rolling(20, min_periods=8).median().shift(1)
        va_ = v.where(v > 0)[::-1].rolling(5, min_periods=2).median()[::-1]   # median of day d..d+4
        vr = va_ / vb
    for R in ratios:
        m = big & ((rc / R - 1).abs() < tol) & ((ro / R - 1).abs() < 3 * tol)
        if vol_sig and v is not None:
            m = m & (vr > 0.6 / R) & (vr < 2.0 / R) if R < 1 else m & (vr > 0.5 / R) & (vr < 1.7 / R)
        ev = ev.where(~m, R)
    return ev
def adjust(p, v, hi, lo, op, ratios=None, vol_sig=True):
    ev = detect(p, op, v, ratios=ratios, vol_sig=vol_sig)
    f_after = ev[::-1].shift(1).fillna(1.0).cumprod()[::-1]    # product of events strictly after d
    f_after = f_after.where(ev == ev, 1.0)
    P = lambda d: d * f_after
    return P(p), v / f_after, P(hi), P(lo), P(op), ev
if __name__ == '__main__':
    import sys, os, pickle; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import harness as h
    p, v, hi, lo, op = h.data()
    STRONG = [1/2, 1/3, 1/4, 1/5, 1/6, 1/8, 1/10, 1/20, 1/50, 2.0, 3.0, 4.0, 5.0, 10.0, 20.0]
    import sys as _s
    novol = len(_s.argv) > 1 and _s.argv[1] == 'novol'
    pa, va, ha, la, oa, ev = adjust(p, v, hi, lo, op, ratios=STRONG, vol_sig=not novol)
    n = (ev != 1.0).sum()
    print("events detected:", int(n.sum()), "in", int((n > 0).sum()), "tickers")
    e = ev.stack(); e = e[e != 1.0]
    print(e.groupby(e.index.get_level_values(0).year).size().to_dict())
    print(e.round(3).value_counts().head(12))
    r = pa.loc['2012':'2025'].pct_change(fill_method=None)
    print("after adj: <-50% days:", int((r < -0.5).sum().sum()), " >+100%:", int((r > 1.0).sum().sum()))
    pickle.dump((pa, va, ha, la, oa), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), ('data_adj_strong_novol.pkl' if novol else 'data_adj_strong.pkl')), 'wb'))

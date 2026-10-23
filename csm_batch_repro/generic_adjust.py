"""Ratio-agnostic, symmetric corporate-action / bad-tick adjuster.
Event = close/prev_close (consecutive rows, both non-NaN) < LO or > HI.  Indian stocks are price-band limited, so such
one-day moves are corporate actions (split/bonus/demerger/rights repricing) or bad ticks, not tradeable returns.
Adjustment removes the whole day's return from history (prices before the event are scaled by the observed ratio)."""
import os, sys, pickle, numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def build(p, v, hi, lo, op, LO=0.55, HI=1.80):
    r = p / p.shift(1)                                  # NaN if either side missing -> no event across gaps
    ev = pd.DataFrame(1.0, index=p.index, columns=p.columns)
    m = (r < LO) | (r > HI)
    ev = ev.where(~m, r)
    f_after = ev[::-1].shift(1).fillna(1.0).cumprod()[::-1]   # product of events strictly after d
    P = lambda d: d * f_after
    return P(p), v / f_after, P(hi), P(lo), P(op), ev
if __name__ == '__main__':
    import harness as h
    p, v, hi, lo, op = h.data()
    out = build(p, v, hi, lo, op)
    ev = out[-1]; e = ev.stack(); e = e[e != 1.0]
    print("events:", len(e), "tickers:", e.index.get_level_values(1).nunique(), " drops:", int((e < 1).sum()), " jumps:", int((e > 1).sum()))
    print("by year:", e.groupby(e.index.get_level_values(0).year).size().to_dict())
    pickle.dump(out[:5], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data_adj_generic.pkl'), 'wb'))

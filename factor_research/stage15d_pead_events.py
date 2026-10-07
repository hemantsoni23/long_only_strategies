"""
stage15d_pead_events.py -- post-earnings-announcement drift as an EVENT strategy (Sadka 2006; CJL 1996; Novy-Marx 2012).

Unlike every month-end ranking so far, entries here are triggered by each company's own results date (filed_date), so the book is
spread over the calendar and is structurally different from the live monthly momentum books.

Event = a quarterly result filing (point-in-time `filed_date`), liquid universe at that date (price>20, top-1000 63d median traded
value, <=5 circuit days).  Entry = close of the 3rd trading day on/after the filing date (so the announcement reaction window
[d-1, d+2] is already known: EAR = stock return less equal-weight market over that window).  Exit = close h trading days later.
Excess return = stock - equal-weight liquid-universe return over the same days.

Signals ranked cross-sectionally within the same calendar month of filing:  SUE (eps), EAR, margin change, growth, and the combination
"good news confirmed by price" (SUE & EAR both in the top 30% of that month).  Reported: mean excess %, win-rate vs universe, NW-free
t-stat clustered by filing month, and the same split by period (2020-22 / 2023+).
Caveat: 2020-06 .. 2025-03, ~58 filing months; entry assumes a fill at the close three days after results (liquid names only).
"""
import os
import pickle
import warnings

import numpy as np
import pandas as pd

from data import load_panels
from stage15_fundamental_momentum import build_quarter_table, announcement_returns

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
HOLDS = (20, 40, 60)


def main():
    P = load_panels(); C = P['close']; V = P['volume']; H = P['high']; L = P['low']
    idx = C.index; Cff = C.ffill()
    q = build_quarter_table(); q = q[q.symbol.isin(C.columns)].reset_index(drop=True)
    q = q[q.filed >= '2020-06-01'].reset_index(drop=True)
    q['ear3'] = announcement_returns(q, C, P['bench_ret'])
    col = {s: i for i, s in enumerate(C.columns)}
    pos = idx.searchsorted(q.filed.values) + 3
    ok = (pos + max(HOLDS) < len(idx)) & q.symbol.map(col).notna().values
    q = q[ok].reset_index(drop=True); pos = pos[ok]
    q['entry_pos'] = pos
    cj = q.symbol.map(col).astype(int).values

    # universe test at the entry date
    dv = (C * V).rolling(63, min_periods=21).median().shift(1)
    circ = ((H == L) & H.notna()).astype('float64').rolling(63, min_periods=1).sum().shift(1)
    liq_ok = np.zeros(len(q), bool)
    rank_cache = {}
    for k, (p, j) in enumerate(zip(pos, cj)):
        if p not in rank_cache:
            rank_cache[p] = dv.iloc[p].rank(ascending=False, method='min')
        r = rank_cache[p].iat[j]
        liq_ok[k] = (r <= 1000) and (Cff.iat[p, j] > 20) and (circ.iat[p, j] <= 5)
    q['liq'] = liq_ok

    # forward returns: stock and liquid-universe equal-weight benchmark over the same window
    r_all = Cff.pct_change(fill_method=None).where(lambda x: (x > -0.4) & (x < 3.0), 0.0).fillna(0.0)
    liq_mkt = {}
    Lg = np.log1p(r_all.values)
    cum = np.cumsum(Lg, axis=0)
    st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
    U1 = st['U']['U1_liquid1000']
    U1d = U1.reindex(idx.union(U1.index)).ffill().shift(1).reindex(idx).fillna(False).astype(bool)   # month-end mask applies from the next day
    rr = r_all.where(U1d.reindex(columns=r_all.columns, fill_value=False))
    bench = rr.mean(axis=1, skipna=True).fillna(0.0).values            # equal-weight LIQUID universe, daily
    bcum = np.cumsum(np.log1p(bench))
    for h in HOLDS:
        a = pos; b = pos + h
        q[f'ret{h}'] = np.expm1(cum[b, cj] - cum[a, cj])
        q[f'mkt{h}'] = np.expm1(bcum[b] - bcum[a])
        q[f'ex{h}'] = q[f'ret{h}'] - q[f'mkt{h}']
    q = q[q.liq].reset_index(drop=True)
    q['m'] = q.filed.dt.to_period('M')

    def pr(c):  # rank within filing month
        return q.groupby('m')[c].rank(pct=True)
    for c in ('sue_eps', 'sg_np', 'dm_ebit', 'ear3', 'sue_np', 'accel_np'):
        q['r_' + c] = pr(c)
    q['eps_pos'] = q.sue_eps > 0

    sets = {
        'ALL events': pd.Series(True, index=q.index),
        'SUE top30%': q.r_sue_eps > 0.7,
        'SUE bottom30%': q.r_sue_eps < 0.3,
        'EAR top30%': q.r_ear3 > 0.7,
        'EAR bottom30%': q.r_ear3 < 0.3,
        'margin-chg top30%': q.r_dm_ebit > 0.7,
        'growth top30%': q.r_sg_np > 0.7,
        'SUE&EAR top30% (confirmed)': (q.r_sue_eps > 0.7) & (q.r_ear3 > 0.7),
        'SUE top30% & EAR<median (unconfirmed)': (q.r_sue_eps > 0.7) & (q.r_ear3 < 0.5),
        'SUE&EAR&margin top40%': (q.r_sue_eps > 0.6) & (q.r_ear3 > 0.6) & (q.r_dm_ebit > 0.6),
        'SUE&EAR bottom30% (bad news)': (q.r_sue_eps < 0.3) & (q.r_ear3 < 0.3),
    }
    rows = []
    for name, m in sets.items():
        d = q[m]
        r = {'set': name, 'events': len(d)}
        for h in HOLDS:
            x = d[f'ex{h}'].clip(-0.6, 1.5)
            by_m = x.groupby(d['m']).mean()
            r[f'ex{h}%'] = x.mean() * 100
            r[f'win{h}'] = (d[f'ret{h}'] > d[f'mkt{h}']).mean()
            r[f'med{h}%'] = x.median() * 100
            r[f't{h}'] = by_m.mean() / (by_m.std() / np.sqrt(len(by_m))) if len(by_m) > 10 else np.nan
        for tag, sl in (('2020-22', d.filed < '2023-01-01'), ('2023+', d.filed >= '2023-01-01')):
            r[f'ex60%_{tag}'] = d[sl]['ex60'].clip(-0.6, 1.5).mean() * 100
        rows.append(r)
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(HERE, 'results', 'stage15d_pead_events.csv'), index=False, float_format='%.3f')
    pd.set_option('display.width', 250, 'display.max_columns', 40)
    print(res.round(2).to_string(index=False))
    print(f"\nliquid events {len(q)}; mean mkt60 {q.mkt60.mean()*100:.1f}%")
    q.to_pickle(os.path.join(HERE, '.cache', 'stage15d_events.pkl'))


if __name__ == '__main__':
    main()

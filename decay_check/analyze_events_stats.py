import os, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
HZ = (5, 10, 20, 40, 60); PRIMARY = 20
CTRL = pd.read_pickle(f'{C.CACHE}/controls.pkl')
chunk_rows, verdict_rows = [], []
for w in ('hr', 'vcp'):
    E = pd.read_pickle(f'{C.CACHE}/events_{w}.pkl'); E = E[E.month <= C.ANCHOR]
    cnt = E.groupby('month').size().reindex(pd.period_range(E.month.min(), C.ANCHOR, freq='M')).fillna(0)
    t12 = cnt.rolling(12).sum()
    first = t12[t12 >= 30].index.min()
    bounds = C.chunk_bounds(first) + [('ALL', first, C.ANCHOR)]
    for base, pre in (('trend-peers', 'xt'), ('market', 'xm'), ('raw', 'raw')):
        for h in HZ:
            col = f'{pre}{h}'
            for lab, s, e in bounds:
                d = E[(E.month >= s) & (E.month <= e)].dropna(subset=[col])
                mon = d.groupby('month')[col].mean()
                lag = int(np.ceil(h / 21))
                st = C.summarize(mon, lag + 1)
                st.update(chunk=lab, h=h, base=base, strategy=w, n_events=len(d),
                          mean_event=d[col].mean(), hit_event=(d[col] > 0).mean(), median_event=d[col].median())
                chunk_rows.append(st)
        for pre2, base2 in (('xt', 'trend-peers'), ('xm', 'market')):
            pass
    for base, pre in (('trend-peers', 'xt'), ('market', 'xm')):
        mon = E.dropna(subset=[f'{pre}{PRIMARY}']).groupby('month')[f'{pre}{PRIMARY}'].mean()
        v = C.verdict_tests(mon, CTRL, first, 2, min_cov=0.5); v.update(strategy=w, metric=f'event-excess@20d vs {base}')
        verdict_rows.append(v)
pd.DataFrame(chunk_rows).to_csv(f'{C.OUT}/ev_chunks.csv', index=False)
V = pd.DataFrame(verdict_rows); V.to_csv(f'{C.OUT}/ev_verdicts.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(V[['strategy','metric','latest_chunk','latest_mean','full_mean','T1_nw_t','T1','T2_slope_per_yr','T2_t','T3_pct','T4_adj_latest','T4_pct_adj','T4_adj_slope_t','T4_excused','T5_persist','verdict']].round(3).to_string())
c = pd.DataFrame(chunk_rows)
x = c[(c.h == 20) & (c.base.isin(['trend-peers', 'market']))][['strategy','base','chunk','n_events','mean_event','hit_event','n','ir','nw_t']]
print(x.round(3).to_string())

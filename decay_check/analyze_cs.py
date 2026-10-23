"""Cross-sectional decay analysis for the 6 factor-ranked strategies."""
import os, pickle, sys
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

P = C.load_panels()
FWD = {h: C.fwd_returns(P['close'], h) for h in C.HORIZONS}
CTRL = C.regime_controls(P)
CTRL.to_pickle(os.path.join(C.CACHE, 'controls.pkl'))
names = ['residual', 'absolute', 'batch', 'elendel', 'zenith', 'quad']

chunk_rows, verdict_rows, leg_rows, series_store = [], [], [], {}
for nm in names:
    d = pickle.load(open(os.path.join(C.CACHE, f'factors_{nm}.pkl'), 'rb'))
    F, top_n = d['F'], d['top_n']
    first = F.dropna(how='all').index.min() + 12          # first 12 months are warm-up transients
    first = max(first, F.index[F.notna().sum(axis=1) >= C.MIN_XS][0])
    S = {h: C.xs_stats(F, FWD[h], top_n) for h in C.HORIZONS}
    series_store[nm] = S
    ct = C.chunk_table(S, first); ct['strategy'] = nm; chunk_rows.append(ct)
    v = C.verdict_tests(S[C.PRIMARY_H]['ic'], CTRL, first, C.PRIMARY_H); v['strategy'] = nm; v['metric'] = 'IC@3m'
    verdict_rows.append(v)
    v2 = C.verdict_tests(S[C.PRIMARY_H]['exc'], CTRL, first, C.PRIMARY_H); v2['strategy'] = nm; v2['metric'] = f'top{top_n}-excess@3m'
    verdict_rows.append(v2)
    for leg, L in d['legs'].items():
        SL = {h: C.xs_stats(L, FWD[h], top_n) for h in (1, 3)}
        lt = C.chunk_table(SL, first, tag_cols=('ic',)); lt['strategy'] = nm; lt['leg'] = leg; leg_rows.append(lt)
    print(nm, 'first', first, 'done', flush=True)

pd.concat(chunk_rows).to_csv(f'{C.OUT}/cs_chunks.csv', index=False)
pd.DataFrame(verdict_rows).to_csv(f'{C.OUT}/cs_verdicts.csv', index=False)
pd.concat(leg_rows).to_csv(f'{C.OUT}/cs_legs.csv', index=False)
pickle.dump(series_store, open(f'{C.CACHE}/cs_series.pkl', 'wb'))

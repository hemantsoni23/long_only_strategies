import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels(); FWD = {h: C.fwd_returns(P['close'], h) for h in (1, 3, 6, 12)}; CT = pd.read_pickle(f'{C.CACHE}/controls.pkl')
V = pickle.load(open(f'{C.CACHE}/quad_variants.pkl', 'rb')); B = pickle.load(open(f'{C.CACHE}/factors_batch.pkl', 'rb'))['F']
# Q3 sanity: Quad(1-1000, 6/12) vs Batch
a, b = V['b1-1000'], B.reindex(index=V['b1-1000'].index, columns=V['b1-1000'].columns)
both = a.notna() & b.notna(); print('Q3: max |Quad(1-1000) - Batch| on common cells', float((a - b).abs().where(both).max().max()), ' cell overlap', round(both.sum().sum() / max(a.notna().sum().sum(), b.notna().sum().sum()), 4))
rows, vrows, ch = [], [], []
for name, F in V.items():
    first = F.index[F.notna().sum(axis=1) >= C.MIN_XS][0] + 12
    S = {h: C.xs_stats(F, FWD[h], 15) for h in (1, 3, 6, 12)}
    t = C.chunk_table(S, first); t['config'] = name; ch.append(t)
    for met in ('ic', 'exc'):
        v = C.verdict_tests(S[3][met], CT, first, 3); v.update(config=name, metric=met); vrows.append(v)
pd.concat(ch).to_csv(f'{C.OUT}/q_chunks.csv', index=False); VV = pd.DataFrame(vrows); VV.to_csv(f'{C.OUT}/q_verdicts.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(VV[['config', 'metric', 'latest_chunk', 'latest_mean', 'full_mean', 'T1_nw_t', 'T1', 'T2_t', 'T3_pct', 'T4_pct_adj', 'T4_excused', 'T5_persist', 'verdict']].round(3).to_string())
c = pd.concat(ch); x = c[(c.metric == 'ic') & (c.h == 3)].pivot(index='config', columns='chunk', values='mean')
print(x.round(3).to_string()); print(c[(c.metric == 'ic') & (c.h == 3)].pivot(index='config', columns='chunk', values='nw_t').round(1).to_string())
print(c[(c.metric == 'exc') & (c.h == 3)].pivot(index='config', columns='chunk', values='mean').round(4).to_string())
for h in (1, 6, 12):
    last = c[(c.metric == 'ic') & (c.h == h) & c.chunk.str.endswith('2026-05')].set_index('config')
    print('latest chunk IC h', h, last[['mean', 'nw_t']].round(3).T.to_string())

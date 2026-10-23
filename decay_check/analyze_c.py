"""Part C: why did the momentum books decay? Diagnostics only."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels(); close = P['close']
FWD3, FWD1 = C.fwd_returns(close, 3), C.fwd_returns(close, 1)
me = C.month_end_days(close.index)
def at_me(df):
    x = df.loc[me]; x.index = pd.PeriodIndex(x.index, freq='M'); return x[~x.index.duplicated(keep='last')]
cf = close.ffill(); ret = close.pct_change(fill_method=None)
VOL = at_me(ret.rolling(63, min_periods=40).std())
LIQ = at_me((close * P['volume']).rolling(63, min_periods=45).median())
M = {nm: pickle.load(open(f'{C.CACHE}/factors_{nm}.pkl', 'rb')) for nm in ('residual', 'absolute', 'batch', 'elendel', 'zenith', 'quad')}
chunks = {}
def chunk_of(p):
    for lab, s, e in CH:
        if s <= p <= e: return lab
CH = C.chunk_bounds(pd.Period('2005-06', 'M'))
def mean_by_chunk(s):
    s = s.dropna(); d = pd.DataFrame({'v': s, 'c': [chunk_of(p) for p in s.index]}).dropna()
    return d.groupby('c').v.mean()
# C1: IC by vol / liquidity tercile
def ic_tercile(F, key, R):
    out = {}
    idx = F.index.intersection(R.index).intersection(key.index)
    for t in range(3):
        rows = {}
        for p in idx:
            f = F.loc[p].dropna(); k = key.loc[p].reindex(f.index); r = R.loc[p].reindex(f.index)
            ok = k.notna() & r.notna(); f, k, r = f[ok], k[ok], r[ok]
            if len(f) < 60: continue
            q = pd.qcut(k.rank(method='first'), 3, labels=False)
            g = q == t
            if g.sum() >= 20: rows[p] = np.corrcoef(f[g].rank(), r[g].rank())[0, 1]
        out[t] = mean_by_chunk(pd.Series(rows))
    return pd.DataFrame(out).rename(columns={0: 'low', 1: 'mid', 2: 'high'})
res_c1 = {}
for nm, d in M.items():
    for kname, key in (('vol', VOL), ('liq', LIQ)):
        t = ic_tercile(d['F'], key, FWD3); t['book'] = nm; t['by'] = kname; res_c1[(nm, kname)] = t
c1 = pd.concat(res_c1.values()); c1.to_csv(f'{C.OUT}/c1_ic_terciles.csv')
# C2: variant ICs on a common pool (elendel eligible mask)
pool = M['elendel']['F'].notna()
mp = to_ = close.ffill().resample('ME').last(); mp.index = pd.PeriodIndex(mp.index, freq='M'); mp = mp[~mp.index.duplicated(keep='last')]
mret = mp.pct_change(fill_method=None)
raw121 = mp.shift(1) / mp.shift(13) - 1
volm = mret.rolling(12).std().shift(1)
var = {'raw 12-1m return': raw121, 'vol-scaled 12-1m (Sharpe-style)': raw121 / (volm * np.sqrt(12)),
       'raw 6-1m return': mp.shift(1) / mp.shift(7) - 1,
       '52w-high proximity': at_me(close.ffill() / close.ffill().rolling(252, min_periods=200).max()),
       'residual R3b (live)': M['residual']['F'], 'Elendel A3 leg': M['elendel']['legs']['A3'], 'Elendel Q5 leg': M['elendel']['legs']['Q5'],
       'Zenith composite (live)': M['zenith']['F'], 'Elendel composite (live)': M['elendel']['F']}
first = pd.Period('2005-06', 'M'); rows = []
for name, V in var.items():
    V = V.reindex(columns=close.columns).where(pool.reindex(columns=close.columns))
    S = C.xs_stats(V, FWD3, 15)
    for lab, s, e in CH + [('ALL', first, C.ANCHOR)]:
        d = S.loc[s:e]; rows.append(dict(variant=name, chunk=lab, ic=d.ic.mean(), ic_t=C.nw_t(d.ic, 2), exc=d.exc.mean(), exc_t=C.nw_t(d.exc, 2), n=d.ic.notna().sum()))
c2 = pd.DataFrame(rows); c2.to_csv(f'{C.OUT}/c2_variants.csv', index=False)
# C3: market state
CT = pd.read_pickle(f'{C.CACHE}/controls.pkl'); mk = P['bench']; mkm = mk.resample('ME').last(); mkm.index = pd.PeriodIndex(mkm.index, freq='M'); mkm = mkm[~mkm.index.duplicated(keep='last')]
mk3 = mkm.pct_change(3); mkf1 = mkm.pct_change(1).shift(-1)
SER = pickle.load(open(f'{C.CACHE}/cs_series.pkl', 'rb'))
rows = []
for nm in M:
    ic3 = SER[nm][3]['ic']; ic1 = SER[nm][1]['ic']
    df = pd.DataFrame({'ic3': ic3, 'ic1': ic1, **CT[['mkt12', 'mktvol3']]}).dropna(subset=['ic3'])
    for col in ('mkt12', 'mktvol3'):
        q = pd.qcut(df[col], 3, labels=['low', 'mid', 'high'])
        for k, g in df.groupby(q, observed=True): rows.append(dict(book=nm, state=f'{col} {k}', ic3=g.ic3.mean(), n=len(g)))
    reb = (mk3.reindex(df.index) < -0.10) & (mkf1.reindex(df.index) > 0.05)
    ic1r = df.ic1[reb].dropna()
    rows.append(dict(book=nm, state='rebound month (3m mkt < -10% then fwd 1m mkt > +5%) 1m IC', ic3=ic1r.mean(), n=len(ic1r)))
    rows.append(dict(book=nm, state='all other months 1m IC', ic3=df.ic1[~reb].mean(), n=int((~reb).sum())))
c3 = pd.DataFrame(rows); c3.to_csv(f'{C.OUT}/c3_state.csv', index=False)
# C4: quintile spreads
rows = []
for nm, d in M.items():
    F = d['F'].reindex(columns=close.columns); idx = F.index.intersection(FWD3.index)
    for p in idx:
        f = F.loc[p].dropna(); r = FWD3.loc[p].reindex(f.index); ok = r.notna(); f, r = f[ok], r[ok]
        if len(f) < 60: continue
        q = pd.qcut(f.rank(method='first'), 5, labels=False); um = r.mean()
        rows.append(dict(book=nm, p=p, chunk=chunk_of(p), q1=r[q == 0].mean() - um, q3=r[q == 2].mean() - um, q5=r[q == 4].mean() - um, top=r[f.rank(ascending=False) <= d['top_n']].mean() - um))
c4 = pd.DataFrame(rows).dropna(subset=['chunk']); c4.to_csv(f'{C.OUT}/c4_quintiles.csv', index=False)
# C5: overlap of top-15 sets across books, month by month
tops = {nm: {p: set(M[nm]['F'].loc[p].dropna().nlargest(15).index) for p in M[nm]['F'].index} for nm in ('absolute', 'batch', 'elendel', 'zenith', 'quad', 'residual')}
pairs = [(a, b) for i, a in enumerate(tops) for b in list(tops)[i + 1:]]
rows = []
for a, b in pairs:
    for p in set(tops[a]) & set(tops[b]):
        A, B = tops[a][p], tops[b][p]
        if A and B: rows.append(dict(a=a, b=b, p=p, jac=len(A & B) / len(A | B)))
c5 = pd.DataFrame(rows); c5['chunk'] = [chunk_of(p) for p in c5.p]; c5.to_csv(f'{C.OUT}/c5_overlap.csv', index=False)
print('done')

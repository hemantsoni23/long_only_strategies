"""Part D: pre-registered improvement candidates evaluated inside each incumbent's own pool."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels(); close = P['close']
FWD = {h: C.fwd_returns(close, h) for h in (1, 3)}
CT = pd.read_pickle(f'{C.CACHE}/controls.pkl')
M = {nm: pickle.load(open(f'{C.CACHE}/factors_{nm}.pkl', 'rb')) for nm in ('absolute', 'batch', 'elendel', 'zenith', 'quad')}
R3 = pickle.load(open(f'{C.CACHE}/r3b1000.pkl', 'rb'))['R3b']
me = C.month_end_days(close.index)
h52 = (close.ffill() / close.ffill().rolling(252, min_periods=200).max()).loc[me]; h52.index = pd.PeriodIndex(h52.index, freq='M'); h52 = h52[~h52.index.duplicated(keep='last')]
mp = close.ffill().resample('ME').last(); mp.index = pd.PeriodIndex(mp.index, freq='M'); mp = mp[~mp.index.duplicated(keep='last')]
raw121 = mp.shift(1) / mp.shift(13) - 1
def z(df, pool):
    x = df.reindex(columns=pool.columns).where(pool); return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)
def evaluate(F, top_n, FW=FWD[3]):
    return C.xs_stats(F, FW, top_n)
def summ(S):
    last2 = S.loc[pd.Period('2020-06', 'M'):C.ANCHOR]; h1 = S.loc[:pd.Period('2016-12', 'M')]; h2 = S.loc[pd.Period('2017-01', 'M'):]
    return dict(exc_all=S.exc.mean(), exc_t_all=C.nw_t(S.exc, 2), exc_last2=last2.exc.mean(), exc_t_last2=C.nw_t(last2.exc, 2), ic_last2=last2.ic.mean(),
                exc_h1=h1.exc.mean(), exc_h2=h2.exc.mean(), ic_all=S.ic.mean(), n=S.exc.notna().sum())
rows = []
for nm, d in M.items():
    F0, N = d['F'], d['top_n']; pool = F0.notna()
    cands = {'incumbent': F0,
             'I1 raw 12-1m return': z(raw121, pool),
             'I2 residual R3b': z(R3, pool),
             'I3 incumbent + R3b': z(F0, pool) + z(R3, pool),
             'I4 incumbent + 52w-high': z(F0, pool) + z(h52, pool)}
    if nm != 'zenith': cands['I3b Zenith composite + R3b'] = None
    for k, V in cands.items():
        if V is None: V = z(M['zenith']['F'].reindex(columns=pool.columns), pool) + z(R3, pool)
        V = V.where(pool)
        S = evaluate(V, N); r = summ(S); r.update(book=nm, variant=k); rows.append(r)
D = pd.DataFrame(rows)
inc = D[D.variant == 'incumbent'].set_index('book')
def verdict(r):
    i = inc.loc[r.book]
    a = r.exc_t_last2 > i.exc_t_last2; b = r.exc_all >= i.exc_all; c = (r.exc_h1 >= i.exc_h1) and (r.exc_h2 >= i.exc_h2); dd = r.ic_last2 >= i.ic_last2
    return pd.Series(dict(a_last2_t=a, b_full=b, c_halves=c, d_ic_last2=dd, IMPROVEMENT=bool(a and b and c and dd)))
D = pd.concat([D, D.apply(verdict, axis=1)], axis=1); D.to_csv(f'{C.OUT}/d_improvements.csv', index=False)
# I5 vol gate: incumbent basket 3m return in gate-on vs gate-off months
rows = []
bench3 = close.ffill().resample('ME').last(); 
for nm, d in M.items():
    F0, N = d['F'], d['top_n']; R = FWD[3]
    idx = F0.index.intersection(R.index)
    top = {}; uni = {}
    for p in idx:
        f = F0.loc[p].dropna(); r = R.loc[p].reindex(f.index).dropna(); f = f.reindex(r.index)
        if len(f) >= C.MIN_XS: top[p] = r[f.rank(ascending=False) <= N].mean(); uni[p] = r.mean()
    s = pd.DataFrame({'top': top, 'uni': uni}); s['exc'] = s.top - s.uni; s['vol'] = CT['mktvol3'].reindex(s.index)
    for lab, g in (('gate ON (vol z<=1)', s[s.vol <= 1]), ('gate OFF (vol z>1)', s[s.vol > 1]), ('all', s)):
        rows.append(dict(book=nm, gate=lab, n=len(g), top_ret_3m=g.top.mean(), exc_3m=g.exc.mean(), uni_3m=g.uni.mean(), exc_t=C.nw_t(g.exc, 2)))
G = pd.DataFrame(rows); G.to_csv(f'{C.OUT}/d_volgate.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30)
print(D[['book', 'variant', 'exc_all', 'exc_t_all', 'exc_last2', 'exc_t_last2', 'ic_last2', 'exc_h1', 'exc_h2', 'IMPROVEMENT']].round(4).to_string())
print(G.round(4).to_string())

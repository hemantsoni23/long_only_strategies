"""Part 1 of Addendum 4: full battery + decay status for every non-sector signal in MOMENTUM_SIGNALS_EXPLAINED.md."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
S = pickle.load(open(f'{C.CACHE}/signals_all.pkl', 'rb')); P = C.load_panels()
U = (S['_uni'] > 0).loc[:C.ANCHOR]
FWD = {h: C.fwd_returns(P['close'], h) for h in (1, 3, 6, 12)}; CT = pd.read_pickle(f'{C.CACHE}/controls.pkl')
NAMES = ['BASE', 'CTRL', 'A1', 'A2', 'A3', 'A4', 'Q5', 'Q4', 'Q3', 'Q1', 'Q2', 'R1', 'V1', 'V2', 'M1', 'M2', 'M3', 'T1']
def pool(n): return S[n].where(U).loc[:C.ANCHOR].astype('float64')
def z(df):
    x = df.where(U); return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)
Fz = {n: pool(n) for n in NAMES}
ELEN = z(pool('A3')) + z(pool('Q5')); ZEN = z(pool('A1')) + z(pool('Q5'))
def quint(F, R, minn=50):
    rows = {}
    for p in F.index.intersection(R.index):
        f = F.loc[p]; r = R.loc[p]; ok = f.notna() & r.notna()
        if ok.sum() < minn: continue
        f, r = f[ok], r[ok]; q = pd.qcut(f.rank(method='first'), 5, labels=False); m = r.mean(); med = r.median()
        qm = [r[q == k].mean() for k in range(5)]
        rows[p] = dict(top_exc=qm[4] - m, q5q1=qm[4] - qm[0], mono=float(np.mean([qm[i + 1] > qm[i] for i in range(4)])),
                       acc_top=float((r[q == 4] > med).mean()), n=int(ok.sum()))
    return pd.DataFrame(rows).T
def incr(F, R, ctrls):
    out = {}
    for p in F.index.intersection(R.index):
        cols = [F.loc[p]] + [c.loc[p] for c in ctrls] + [R.loc[p]]; d = pd.concat(cols, axis=1).dropna()
        if len(d) < 50: continue
        rk = d.rank(); y = rk.iloc[:, 0].values; X = np.column_stack([np.ones(len(d))] + [rk.iloc[:, j].values for j in range(1, 1 + len(ctrls))])
        b = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ b
        if res.std() > 0: out[p] = np.corrcoef(res, rk.iloc[:, -1].values)[0, 1]
    return pd.Series(out)
def avg_corr(F, G):
    out = {}
    for p in F.index.intersection(G.index):
        d = pd.concat([F.loc[p], G.loc[p]], axis=1).dropna()
        if len(d) >= 50: out[p] = d.rank().corr().iloc[0, 1]
    return pd.Series(out).mean()
summ, hrows, crows, vrows = [], [], [], []
dv = S['_dvol'].loc[:C.ANCHOR]
for n in NAMES:
    F = Fz[n]; first = F.index[F.notna().sum(axis=1) >= C.MIN_XS][0] + 12 if n != 'T1' else F.index[F.notna().sum(axis=1) >= C.MIN_XS][0]
    st = {h: C.xs_stats(F, FWD[h], 15) for h in (1, 3, 6, 12)}
    for h in st:
        s = C.summarize(st[h].ic.loc[first:], h); s.update(signal=n, h=h); hrows.append(s)
    ic3 = st[3].ic.loc[first:]; q = quint(F.loc[first:], FWD[3]); exc15 = st[3].exc.loc[first:]
    ct = C.chunk_table(st, first, tag_cols=('ic',)); ct['signal'] = n; crows.append(ct)
    v = C.verdict_tests(st[3].ic, CT, first, 3); v.update(signal=n); vrows.append(v)
    bi = incr(F.loc[first:], FWD[3], [Fz['BASE']]); ei = incr(F.loc[first:], FWD[3], [ELEN, ZEN])
    last6 = slice(pd.Period('2020-06', 'M'), C.ANCHOR)
    # large vs small cap IC (median dvol split) and breadth / year concentration
    ic_big, ic_small = {}, {}
    for p in F.index.intersection(FWD[3].index):
        if p < first: continue
        d = pd.concat([F.loc[p], FWD[3].loc[p], dv.loc[p]], axis=1).dropna()
        if len(d) < 60: continue
        big = d.iloc[:, 2] >= d.iloc[:, 2].median()
        ic_big[p] = d[big].iloc[:, :2].rank().corr().iloc[0, 1]; ic_small[p] = d[~big].iloc[:, :2].rank().corr().iloc[0, 1]
    yr = ic3.dropna(); yr.index = yr.index.to_timestamp(); ys = yr.groupby(yr.index.year).sum(); top2 = ys.abs().nlargest(2).sum() / ys.abs().sum() if len(ys) else np.nan
    nm = F.notna().sum(axis=1).loc[first:ic3.index.max()]
    s3 = C.summarize(ic3, 3); qa = q.mean(numeric_only=True)
    summ.append(dict(signal=n, first=str(first), n_months=s3['n'], ic3=s3['mean'], icir3=s3['ir'], hit3=s3['hit'], t3=s3['t'], nw3=s3['nw_t'],
                     top_exc3=qa['top_exc'], top_exc_nw=C.nw_t(q.top_exc, 2), q5q1=qa['q5q1'], mono=qa['mono'], acc_topq=qa['acc_top'], acc_top15=st[3].acc.loc[first:].mean(),
                     exc15=exc15.mean(), exc15_nw=C.nw_t(exc15, 2), corr_base=avg_corr(F.loc[first:], Fz['BASE']),
                     inc_base_ic=bi.mean(), inc_base_nw=C.nw_t(bi, 2), inc_live_ic=ei.mean(), inc_live_nw=C.nw_t(ei, 2),
                     inc_live_ic_last6=ei.loc[last6].mean(), inc_live_nw_last6=C.nw_t(ei.loc[last6], 2), ic_bigcap=pd.Series(ic_big).mean(), ic_smallcap=pd.Series(ic_small).mean(),
                     top2yr_share=top2, pct_months_lt8=float((nm < 8).mean()), pct_months_lt20=float((nm < 20).mean())))
    print(n, 'IC3', round(s3['mean'], 3), 'NW', round(s3['nw_t'], 1), flush=True)
A = pd.DataFrame(summ); A.to_csv(f'{C.OUT}/battery_summary.csv', index=False)
pd.DataFrame(hrows).to_csv(f'{C.OUT}/battery_horizons.csv', index=False); pd.concat(crows).to_csv(f'{C.OUT}/battery_chunks.csv', index=False)
V = pd.DataFrame(vrows); V.to_csv(f'{C.OUT}/battery_verdicts.csv', index=False)
pd.set_option('display.width', 250); pd.set_option('display.max_columns', 40)
print(A[['signal', 'ic3', 'icir3', 'hit3', 'nw3', 'top_exc3', 'top_exc_nw', 'mono', 'acc_topq', 'corr_base', 'inc_base_nw', 'inc_live_ic', 'inc_live_nw', 'inc_live_ic_last6', 'inc_live_nw_last6']].round(3).to_string())
print(V[['signal', 'latest_chunk', 'latest_mean', 'full_mean', 'T1_nw_t', 'T1', 'T2_t', 'T3_pct', 'T4_excused', 'T5_persist', 'verdict']].round(3).to_string())

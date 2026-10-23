import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine as SE, faithful_replay as FR
D = SE.data(); S = D['S']; P = C.load_panels()
IDX = pd.read_parquet('../factor_research/.cache/index_data_close.parquet')['Nifty_500'].dropna().pct_change()
R = SE.run(sel='R1'); tl = R['trades'].copy()
# ---- Stage 2 ladder for R1
per = D['per']; cols = D['cols']
def frame(arr_fn):
    return pd.DataFrame([arr_fn(k) for k in range(len(per))], index=per, columns=cols)
R1 = S['R1'].reindex(per).astype('float64')
px = D['close_me'].copy(); px.index = per
rk = D['dv_me'].rank(axis=1, ascending=False, method='min'); rk.index = per
circ = D['circ_me'].copy(); circ.index = per; sma = D['sma200_me'].copy(); sma.index = per
m3 = S['M3'].reindex(per).astype('float64')
FWD3 = C.fwd_returns(P['close'], 3)
L0 = R1; L1 = R1.where(px >= 10); L2 = R1.where((px >= 10) & (rk <= 1000)); L3 = R1.where((px >= 20) & (rk <= 1000) & (circ <= 5))
L4m = (px >= 20) & (rk <= 1000) & (circ <= 5) & (px > sma)
thr = m3.where(L4m).quantile(0.20, axis=1); L4 = R1.where(L4m & ~(m3.lt(thr, axis=0)))
rows = []
first = pd.Period('2005-09', 'M')
for name, F in (('L0 raw', L0), ('L1 price>=10', L1), ('L2 +liquidity top1000', L2), ('L3 tradeable (px>=20, circuit)', L3), ('L4 strategy pool (SMA200 + M3 excl.)', L4)):
    st = C.xs_stats(F.loc[first:C.ANCHOR], FWD3, 20); ic = st.ic
    # quintile avg returns (monotonic pairs on time-averaged quintile means)
    qm = []
    for p in F.loc[first:C.ANCHOR].index.intersection(FWD3.index):
        f = F.loc[p]; r = FWD3.loc[p]; ok = f.notna() & r.notna()
        if ok.sum() < 50: continue
        q = pd.qcut(f[ok].rank(method='first'), 5, labels=False); qm.append([r[ok][q == k].mean() for k in range(5)])
    qm = np.array(qm); avg = qm.mean(axis=0); spread = qm[:, 4] - qm[:, 0]
    yr = ic.dropna(); yr.index = yr.index.to_timestamp(); ys = yr.groupby(yr.index.year).sum()
    isA = ic.loc[:pd.Period('2012-12', 'M')]; isB = ic.loc[pd.Period('2013-01', 'M'):]
    rows.append(dict(rung=name, ic=ic.mean(), nw_t=C.nw_t(ic.dropna(), 2), icir=ic.mean() / ic.std(), hit=(ic.dropna() > 0).mean(), n_avg=st.n.mean(), mono_pairs=float(np.mean([avg[i + 1] > avg[i] for i in range(4)])),
                     q_means_pct=[round(x * 100, 2) for x in avg], spread_nw_t=C.nw_t(spread, 2), nw_2005_12=C.nw_t(isA.dropna(), 2), nw_2013_26=C.nw_t(isB.dropna(), 2), top2yr_share=ys.abs().nlargest(2).sum() / ys.abs().sum(),
                     pct_months_lt8=float((st.n < 8).mean())))
L = pd.DataFrame(rows); L.to_csv(f'{C.OUT}/aegis_stage2.csv', index=False); pd.set_option('display.width', 250); pd.set_option('display.max_columns', 30); print(L.round(3).to_string(), flush=True)
# ---- distinctness
jr = []
for nm in ('elendel', 'zenith', 'residual', 'batch', 'absolute', 'quad'):
    F = pickle.load(open(f'{C.CACHE}/factors_{nm}.pkl', 'rb'))['F']
    for p, mine in R['picks'].items():
        if p in F.index:
            theirs = set(F.loc[p].dropna().nlargest(20).index)
            if theirs: jr.append(dict(book=nm, p=p, jac=len(set(mine) & theirs) / len(set(mine) | theirs)))
J = pd.DataFrame(jr); Jm = J.groupby('book').jac.mean(); Jl = J[J.p >= pd.Period('2023-06', 'M')].groupby('book').jac.mean()
print('top-20 Jaccard vs live books, all / latest 3y:'); print(pd.DataFrame({'all': Jm, 'latest3y': Jl}).round(3).to_string(), flush=True); pd.DataFrame({'all': Jm, 'latest3y': Jl}).to_csv(f'{C.OUT}/aegis_distinct.csv')
# ---- exits by reason + post-exit
cl = P['close'].ffill(limit=10); dates = cl.index; bench = P['bench']; ex = []
for t in tl.itertuples():
    if t.reason == 'END_OF_PERIOD': continue
    i = dates.get_loc(pd.Timestamp(t.exit)); j = cl.columns.get_loc(t.ticker); row = dict(reason=t.reason)
    for h in (20, 60):
        if i + h < len(dates):
            a, b = cl.iat[i, j], cl.iat[i + h, j]; row[f'post{h}'] = (b / a - 1) - (bench.iat[i + h] / bench.iat[i] - 1)
    ex.append(row)
EX = pd.DataFrame(ex); g = EX.groupby('reason'); T = tl.groupby('reason').agg(n=('pnl_pct', 'size'), avg_pnl=('pnl_pct', 'mean'), win=('pnl_pct', lambda s: (s > 0).mean())); T = T.join(g[['post20', 'post60']].mean()); T['post_avg'] = (T.post20 + T.post60) / 2
T['verdict'] = np.where(T.post_avg <= -0.01, 'working', np.where(T.post_avg >= 0.01, 'too early', 'neutral')); T['share_exits'] = T.n / T.n.sum() * 100
T.to_csv(f'{C.OUT}/aegis_stage5.csv'); print(T.round(3).to_string(), 'END_OF_PERIOD trades:', int((tl.reason == 'END_OF_PERIOD').sum()), flush=True)
# ---- concentration
tl['contrib'] = tl.w_rel * tl.pnl_pct / 100; tc = tl.sort_values('contrib', ascending=False); tot = tl.contrib.sum()
print('trades', len(tl), 'win rate', round((tl.pnl_pct > 0).mean(), 3), 'median pnl%', round(tl.pnl_pct.median(), 2), 'mean', round(tl.pnl_pct.mean(), 2), 'payoff', round(tl[tl.pnl_pct > 0].pnl_pct.mean() / -tl[tl.pnl_pct < 0].pnl_pct.mean(), 2))
for k in (5, 10, 25, 50): print(f'top {k} trades share of summed contribution: {tc.contrib.head(k).sum() / tot:.2f}')
print(tc.head(8)[['ticker', 'entry', 'exit', 'pnl_pct', 'reason']].to_string())
# ---- placebo by chunk
pl = {}
for s in range(100):
    r = SE.run(sel='random', seed=s)['ret']; pl[s] = FR.chunk_stats(r, pd.Period('2008-06', 'M') - 1, IDX).set_index('chunk').cagr
PLc = pd.DataFrame(pl).T; mine = FR.chunk_stats(R['ret'], pd.Period('2008-06', 'M') - 1, IDX).set_index('chunk').cagr
cmp = pd.DataFrame({'AEGIS': mine, 'placebo_mean': PLc.mean(), 'placebo_p95': PLc.quantile(.95), 'pct_beaten': [(PLc[c] < mine[c]).mean() for c in mine.index]}); cmp.to_csv(f'{C.OUT}/aegis_placebo_chunks.csv'); print(cmp.round(3).to_string(), flush=True)
# ---- rolling 36m sharpe / cagr
r = R['ret']; r = r[r.index >= '2005-01-01']; roll = (1 + r).rolling(756).apply(np.prod, raw=True) ** (1 / 3) - 1; sh = r.rolling(756).mean() / r.rolling(756).std() * np.sqrt(252)
print('rolling 36m CAGR: min %.3f  latest %.3f  pct rank of latest %.2f' % (roll.min(), roll.iloc[-1], (roll.dropna() <= roll.iloc[-1]).mean())); print('rolling 36m Sharpe: min %.2f latest %.2f' % (sh.min(), sh.iloc[-1]))
pd.DataFrame({'roll36_cagr': roll, 'roll36_sharpe': sh}).to_csv(f'{C.OUT}/aegis_rolling36.csv')

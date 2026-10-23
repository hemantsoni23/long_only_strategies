"""Addendum 6, signals S1 (R1+A1) and S2 (R1+Ulcer): full battery in the tradeable (L3) and strategy (L4) pools."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine as SE
D = SE.data(); S = pickle.load(open(f'{C.CACHE}/signals_all.pkl', 'rb')); P = C.load_panels(); per = D['per']; cols = D['cols']; CT = pd.read_pickle(f'{C.CACHE}/controls.pkl')
def fr(a): return pd.DataFrame(a, index=per, columns=cols)
px = D['close_me'].copy(); px.index = per; rk = D['dv_me'].rank(axis=1, ascending=False, method='min'); rk.index = per
circ = D['circ_me'].copy(); circ.index = per; sma = D['sma200_me'].copy(); sma.index = per
raw = {n: S[n].reindex(per).astype('float64') for n in ('R1', 'A1', 'ULC', 'M3', 'A3', 'Q5')}
L3m = (px >= 20) & (rk <= 1000) & (circ <= 5); thr = raw['M3'].where(L3m & (px > sma)).quantile(0.20, axis=1); L4m = L3m & (px > sma) & ~(raw['M3'].lt(thr, axis=0))
def z(df, m): x = df.where(m); return x.sub(x.mean(axis=1), axis=0).div(x.std(axis=1), axis=0)
FWD = {h: C.fwd_returns(P['close'], h) for h in (1, 3, 6, 12)}
def quint(F, R):
    qm = []; acc = []; ex = []
    for p in F.index.intersection(R.index):
        f = F.loc[p]; r = R.loc[p]; ok = f.notna() & r.notna()
        if ok.sum() < 50: continue
        q = pd.qcut(f[ok].rank(method='first'), 5, labels=False); rr = r[ok]; qm.append([rr[q == k].mean() for k in range(5)]); acc.append((rr[q == 4] > rr.median()).mean()); ex.append(rr[q == 4].mean() - rr.mean())
    qm = np.array(qm); avg = qm.mean(axis=0); return avg, float(np.mean(acc)), pd.Series(ex)
def incr(F, R, ctrl):
    out = {}
    for p in F.index.intersection(R.index):
        d = pd.concat([F.loc[p], ctrl.loc[p], R.loc[p]], axis=1).dropna()
        if len(d) < 50: continue
        rk_ = d.rank(); y = rk_.iloc[:, 0].values; X = np.column_stack([np.ones(len(d)), rk_.iloc[:, 1].values]); b = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ b
        if res.std() > 0: out[p] = np.corrcoef(res, rk_.iloc[:, 2].values)[0, 1]
    return pd.Series(out)
rows = []; res = {}
for pool_name, m in (('L3 tradeable', L3m), ('L4 strategy pool', L4m)):
    sig = {'R1 (current)': z(raw['R1'], m), 'A1 alone': z(raw['A1'], m), 'Ulcer alone (-UI)': z(raw['ULC'], m), 'S1 = R1 + A1': z(raw['R1'], m) + z(raw['A1'], m), 'S2 = R1 + (-Ulcer)': z(raw['R1'], m) + z(raw['ULC'], m)}
    for name, F in sig.items():
        F = F.where(m); first = pd.Period('2005-09', 'M'); F = F.loc[first:C.ANCHOR]
        st = {h: C.xs_stats(F, FWD[h], 20) for h in (1, 3, 6, 12)}; v3 = C.verdict_tests(st[3].ic, CT, first, 3); v6 = C.verdict_tests(st[6].ic, CT, first, 6)
        avg, acc, ex = quint(F, FWD[3]); inc = incr(F, FWD[3], sig['R1 (current)'].loc[first:C.ANCHOR]) if name != 'R1 (current)' else pd.Series(dtype=float)
        # overlap of top-20 with R1's top-20 and live books
        ov = []
        for p in F.index.intersection(sig['R1 (current)'].index):
            a = set(F.loc[p].dropna().nlargest(20).index); b = set(sig['R1 (current)'].loc[p].dropna().nlargest(20).index)
            if a and b: ov.append(len(a & b) / len(a | b))
        r = dict(pool=pool_name, signal=name, **{f'ic{h}': st[h].ic.mean() for h in (1, 3, 6, 12)}, **{f'nw{h}': C.nw_t(st[h].ic.dropna(), max(h - 1, 0)) for h in (1, 3, 6, 12)}, icir3=st[3].ic.mean() / st[3].ic.std(),
                 hit3=(st[3].ic.dropna() > 0).mean(), top20_exc3=st[3].exc.mean(), top20_exc3_nw=C.nw_t(st[3].exc.dropna(), 2), topq_exc=ex.mean(), topq_nw=C.nw_t(ex, 2), acc_topq=acc,
                 mono=float(np.mean([avg[i + 1] > avg[i] for i in range(4)])), q_means=[round(x * 100, 2) for x in avg], jac_vs_R1=float(np.mean(ov)),
                 inc_vs_R1=inc.mean() if len(inc) else np.nan, inc_nw=C.nw_t(inc, 2) if len(inc) else np.nan, v3=v3['verdict'], v3_latest_nw=v3['T1_nw_t'], v6=v6['verdict'], v6_latest_nw=v6['T1_nw_t'], v3_pct=v3['T3_pct'])
        rows.append(r); print(pool_name, name, 'IC3 %.3f NW %.1f | IC6 %.3f NW %.1f | top20 exc %.2f%% | acc %.3f | jac vs R1 %.2f | 3m %s 6m %s' % (r['ic3'], r['nw3'], r['ic6'], r['nw6'], r['top20_exc3'] * 100, r['acc_topq'], r['jac_vs_R1'], r['v3'], r['v6']), flush=True)
A = pd.DataFrame(rows); A.to_csv(f'{C.OUT}/upgrade_signals.csv', index=False)
# correlation of R1+Ulcer pieces
cc = pd.DataFrame({'R1~A1': [raw['R1'].where(L4m).corrwith(raw['A1'].where(L4m), axis=1, method='spearman').mean()], 'R1~Ulcer': [raw['R1'].where(L4m).corrwith(raw['ULC'].where(L4m), axis=1, method='spearman').mean()], 'A1~Ulcer': [raw['A1'].where(L4m).corrwith(raw['ULC'].where(L4m), axis=1, method='spearman').mean()]}); print(cc.round(2).to_string())
# live-book top-20 overlap for S1/S2 in L4
jr = []
for nm in ('elendel', 'zenith', 'residual', 'batch'):
    Fb = pickle.load(open(f'{C.CACHE}/factors_{nm}.pkl', 'rb'))['F']
    for name, F in (('R1', z(raw['R1'], L4m)), ('S1', z(raw['R1'], L4m) + z(raw['A1'], L4m)), ('S2', z(raw['R1'], L4m) + z(raw['ULC'], L4m))):
        v = [len(set(F.loc[p].dropna().nlargest(20).index) & set(Fb.loc[p].dropna().nlargest(20).index)) / len(set(F.loc[p].dropna().nlargest(20).index) | set(Fb.loc[p].dropna().nlargest(20).index)) for p in F.index.intersection(Fb.index) if F.loc[p].notna().sum() > 30 and Fb.loc[p].notna().sum() > 20]
        jr.append(dict(book=nm, sel=name, jaccard=np.mean(v)))
print(pd.DataFrame(jr).pivot(index='book', columns='sel', values='jaccard').round(2).to_string()); pd.DataFrame(jr).to_csv(f'{C.OUT}/upgrade_overlap.csv', index=False)

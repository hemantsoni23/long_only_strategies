"""Where does PEAD's 0.7 correlation come from, and which kind of book is genuinely less correlated with the live engines?
(1) PEAD daily returns regressed on the liquid equal-weight market;  (2) monthly correlation with live engines of: PEAD, E/P-only top-N book, momentum proxy book."""
import os, sys, pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
FR = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'; sys.path.insert(0, FR)
from evaluate import zscore
from portfolio_lab import topn_book
st = pickle.load(open(os.path.join(FR, '.cache', 'state.pkl'), 'rb')); sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
S = pickle.load(open(os.path.join(FR, '.cache', 'stage15_sigs.pkl'), 'rb'))
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache'
live = {n: pickle.load(open(f'{LIVE}/engine_{n}.pkl', 'rb'))['net_returns'] for n in ('elendel', 'zenith', 'quad')}
pead = pd.read_csv('output/pead_daily_returns.csv', index_col=0, parse_dates=True)['net_return']
pead = pead.loc['2020-09-01':'2025-06-30']
mon = lambda r: (1 + r).resample('ME').prod() - 1
lm = {n: mon(r.loc['2020-09-01':'2025-06-30']) for n, r in live.items()}
trio_m = pd.concat(lm, axis=1).mean(axis=1)
print('PEAD vs live trio, monthly corr:', round(mon(pead).corr(trio_m), 2))
# (1) market regression (liquid EW market from the research universe, daily)
import importlib; sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies')
from data import load_panels
P = load_panels(); C = P['close'].ffill(); r = C.pct_change(fill_method=None).where(lambda x: (x > -0.4) & (x < 3), 0).fillna(0)
U1 = U['U1_liquid1000']; U1d = U1.reindex(r.index.union(U1.index)).ffill().shift(1).reindex(r.index).fillna(False).astype(bool)
mk = r.where(U1d).mean(axis=1).loc['2020-09-01':'2025-06-30']
j = pead.index.intersection(mk.index)
X = np.c_[np.ones(len(j)), mk[j].values]; b = np.linalg.lstsq(X, pead[j].values, rcond=None)[0]
res = pead[j].values - X @ b
print(f'PEAD on liquid EW market (daily): beta {b[1]:.2f}  corr {pead[j].corr(mk[j]):.2f}  R2 {1-res.var()/pead[j].var():.2f}  alpha {b[0]*252*100:+.1f}%/yr')
for n, rr in live.items():
    rr = rr.loc['2020-09-01':'2025-06-30']; jj = rr.index.intersection(mk.index)
    Xl = np.c_[np.ones(len(jj)), mk[jj].values]; bl = np.linalg.lstsq(Xl, rr[jj].values, rcond=None)[0]
    print(f'  {n:<8} on market: beta {bl[1]:.2f}  corr {rr[jj].corr(mk[jj]):.2f}  alpha {bl[0]*252*100:+.1f}%/yr')
# (2) proxy books monthly correlation vs live
def book(sc, mask, n=15):
    b = topn_book(sc, mask, FWD[1], n=n); return b['net']
rows = {}
for un in ('U1_liquid1000',):
    m = U[un]
    ep = zscore(S['ep_ttm'].where(m)); rows['E/P only top-15 (U1)'] = book(ep, m, 15)
    rows['E/P only top-30 (U1)'] = book(ep, m, 30)
    mom = zscore(F['a3_rs_high'].where(m)) + zscore(F['q5_126'].where(m)); rows['Elendel-score proxy top-15'] = book(mom, m, 15)
    ep_pos = zscore(S['ep_ttm'].where(m & (S['ep_ttm'] > 0.05))); rows['E/P>5% only top-15'] = book(ep_pos, m & (S['ep_ttm'] > 0.05), 15)
print('\nmonthly-return correlation with the live engines (2020-09..2025-03):')
for k, bk in rows.items():
    bk = bk.copy(); bk.index = bk.index + pd.offsets.MonthEnd(1)
    j = bk.loc['2020-09-01':'2025-03-31'].index.intersection(trio_m.index)
    print(f'  {k:<28} vs trio {bk[j].corr(trio_m[j]):+.2f} | ' + ' '.join(f'{n} {bk[j].corr(lm[n][j]):+.2f}' for n in lm) + f' | ann.mean {((1+bk[j]).prod()**(12/len(j))-1)*100:.0f}%')

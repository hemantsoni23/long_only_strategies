"""Which earnings-yield book design is least correlated with the live engines while still adding to them? (proxy equal-weight top-N books, monthly, 2020-09..2025-03)
Adding an asset with Sharpe S_n and correlation rho to a portfolio with Sharpe S_p raises the portfolio Sharpe only if S_n > rho * S_p."""
import os, sys, pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
FR = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'; sys.path.insert(0, FR)
from evaluate import zscore
from portfolio_lab import topn_book, stats
st = pickle.load(open(os.path.join(FR, '.cache', 'state.pkl'), 'rb')); sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
S = pickle.load(open(os.path.join(FR, '.cache', 'stage15_sigs.pkl'), 'rb'))
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache'
mon = lambda r: (1 + r).resample('ME').prod() - 1
live = {n: mon(pickle.load(open(f'{LIVE}/engine_{n}.pkl', 'rb'))['net_returns'].loc['2020-09-01':'2025-06-30']) for n in ('elendel', 'zenith', 'quad')}
trio = pd.concat(live, axis=1).mean(axis=1)
sp = stats(trio)['sharpe']; print(f'live trio monthly Sharpe (rf6) {sp:.2f}; break-even rule: new Sharpe must exceed rho*{sp:.2f}')
U1 = U['U1_liquid1000']; U3 = U['U3_top300']; mid = U1 & ~U3
ep = S['ep_ttm']; ok_growth = (S['sg_np'] > 0); ok_sue = (S['sue_eps'] > 0); ok_m = (S['dm_ebit'] > 0)
designs = {
 'E/P, liquid-1000, top-15': (ep, U1, 15),
 'E/P, ranks 301-1000, top-15': (ep, mid, 15),
 'E/P + profit growth>0, liquid-1000': (ep.where(ok_growth), U1, 15),
 'E/P + profit growth>0, 301-1000': (ep.where(ok_growth), mid, 15),
 'E/P + SUE>0 & margin up, 301-1000': (ep.where(ok_sue & ok_m), mid, 15),
 'E/P + growth>0, 301-1000, top-25': (ep.where(ok_growth), mid, 25),
 'E/P + growth>0, uptrend (>SMA200) 301-1000': (ep.where(ok_growth), mid & st['U']['U2_live_trend'], 15),
}
rows = []
for k, (sc, m, n) in designs.items():
    mm = m & sc.notna(); mm = mm.where(mm.sum(axis=1) >= 60, False)
    b = topn_book(zscore(sc.where(mm)), mm, FWD[1], n=n)
    bn = b['net'].copy(); bn.index = bn.index + pd.offsets.MonthEnd(1)
    j = bn.loc['2020-09-01':'2025-03-31'].index.intersection(trio.index); r = bn[j]
    s = stats(r); rho = r.corr(trio[j])
    rows.append(dict(design=k, months=len(j), cagr=s['cagr'] * 100, sharpe=s['sharpe'], maxdd=s['maxdd'] * 100, corr_trio=rho, breakeven=rho * sp,
                     adds=s['sharpe'] > rho * sp, turnover=b['turnover'][b.index >= '2020-08-01'].mean(), **{f'corr_{n_}': r.corr(live[n_][j]) for n_ in live}))
print(pd.DataFrame(rows).round(2).to_string(index=False))

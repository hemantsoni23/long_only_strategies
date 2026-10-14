"""Health audit A1-A2 of CSMIndustryBook (INDUSTRY_BOOK_PREREG.md section 7).  python3 test_health.py"""
import os, sys, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); FR = os.path.join(ROOT, 'factor_research')
sys.path.insert(0, HERE); sys.path.insert(0, FR); os.chdir(FR)
from industry_book_strategy import CSMIndustryBook
from data import load_panels

P = load_panels()
INS = os.path.join(ROOT, 'instruments_clean.csv')
mk = lambda cut=None: CSMIndustryBook(*(P[k] if cut is None else P[k].loc[:cut] for k in ('close', 'volume', 'high', 'low', 'open')), instruments_path=INS)
full = mk(); full.calculate_factors(); full.get_positions(); full.backtest()

print('A1 truncation test (target weights on every signal row before the cut must be identical)')
ok_all = True
for cut in ('2013-12-31', '2017-06-30', '2021-03-31'):
    s = mk(cut); s.calculate_factors(); s.get_positions()
    rows = s.positions.index[s.positions.index < pd.Timestamp(cut) - pd.offsets.MonthEnd(1)]       # exclude the cut month itself
    a = s.positions.loc[rows].values; b = full.positions.reindex(rows).values
    d = float(np.nanmax(np.abs(a - b)))
    print(f'  cut {cut}: {len(rows)} rows compared, max|diff| = {d:.2e}'); ok_all &= d == 0.0
print('  A1', 'PASS' if ok_all else 'FAIL')

print('A2 live-row sanity')
lo = full.live_orders(); w = lo['weights']; k = len(full.sig) - 1
labelled = full.ind_code[[full.cols.get_loc(t) for t in w.index]] >= 0
newest = [full.cols[i] for i in np.where(full.cohorts[k] > 0)[0]]
in_pool = bool(full.U2.iloc[k][newest].all())
stale = int((~full.U2.iloc[k][w.index].astype(bool)).sum())
ind_of = pd.Series(full.ind_code[[full.cols.get_loc(t) for t in w.index]], index=w.index)
checks = {
    'weights >= 0': bool((w >= 0).all()), 'sum(eff weights) <= 1': bool(lo['effective_weights'].sum() <= 1 + 1e-9), 'no NaN': bool(w.notna().all()),
    'newest cohort entirely in SMA200 pool': in_pool, 'older-tranche names now below SMA200 (by design, held to tranche end)': stale, 'all labelled': bool(labelled.all()), '<= 2 names per industry (single cohort)': True,
    'industries <= 8': len(lo['industries']) <= 8, 'distinct industries held across 6 tranches': int(ind_of.nunique()),
}
last = full.cohorts[k]; names = np.where(last > 0)[0]
cnt = pd.Series(full.ind_code[names]).value_counts(); checks['<= 2 names per industry (single cohort)'] = bool((cnt <= 2).all())
for kk, v in checks.items(): print(f'  {kk}: {v}')
print(f"  signal {lo['signal_date'].date()}  gate_up {lo['gate_up']}  vol scale {lo['vol_scale']:.2f}  names {len(w)}  cash {lo['cash_weight']*100:.1f}%  max single weight {w.max()*100:.1f}%")
print('  top-8 industries now:', lo['industries'])
print('  panel last date', full.dates[-1].date(), '| signal dates', full.sig[-2].date(), full.sig[-1].date())

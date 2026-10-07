"""
Checks for the residual-momentum tilt (run:  python3 test_resid_tilt.py)
 1. weight 0  -> factors identical to the live engine (Zenith & Elendel)
 2. native residual momentum == the factor_research version used in the evidence (month-end rank correlation, then final scores)
 3. no look-ahead: truncating the data at a month-end leaves that month's tilted score unchanged
 4. tilted engine daily returns ~ the research variant stored in momentum_value/.cache/impr_*.pkl (same engine, same hook)
 5. universe/eligibility untouched: tilted score is non-NaN exactly where the live score is
"""
import os, sys, pickle, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from resid_tilt_strategies import CSMZenithResid, CSMElendelResid, residual_momentum_daily, LIVE
from csm_zenith_strategy import CSMZenith
from csm_elendel_strategy import CSMElendel
ele = importlib.import_module('run_csm_elendel_backtest'); zen = importlib.import_module('run_csm_zenith_backtest')
RQ = '/Users/hemantsoni/Documents/long_only_strategies/factor_research'
sys.path.insert(0, RQ)
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else '')); (None if ok else fails.append(name))

prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2026-07-16']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
kw = dict(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)

live = {'zenith': CSMZenith(**kw), 'elendel': CSMElendel(**kw)}
for c in live.values(): c.calculate_factors()
til = {'zenith': CSMZenithResid(resid_weight=0.5, **kw), 'elendel': CSMElendelResid(resid_weight=0.5, **kw)}
for c in til.values(): c.calculate_factors()
zero = {'zenith': CSMZenithResid(resid_weight=0.0, **kw), 'elendel': CSMElendelResid(resid_weight=0.0, **kw)}
for c in zero.values(): c.calculate_factors()

for n in live:
    a, b = live[n].factors, zero[n].factors
    check(f'1. {n}: weight 0 identical to live factors', a.equals(b) or np.allclose(a.fillna(-99).values, b.fillna(-99).values))
    t = til[n].factors; base = til[n].base_factors
    check(f'5. {n}: tilted score defined exactly where live score is (inside months with a tilt)', bool((t.notna() == base.reindex(t.index).notna()).all().all()))

# 2. versus harness
st = pickle.load(open(os.path.join(RQ, '.cache', 'state.pkl'), 'rb')); Fh = st['F']['mom_resid_12_1']
rm = til['elendel'].resid_mom
ics = []
for d in Fh.index[Fh.index >= '2008-01-01'][::6]:
    me = d + pd.offsets.MonthEnd(0)
    if me not in rm.index: continue
    a = rm.loc[me].dropna(); b = Fh.loc[d].dropna(); j = a.index.intersection(b.index)
    if len(j) > 200: ics.append(a[j].rank().corr(b[j].rank()))
check('2. native residual momentum vs research factor (mean month-end rank corr >= 0.995, min >= 0.95; not bit-identical: the engine calendar keeps holiday placeholder rows the research panels drop)', np.mean(ics) >= 0.995 and np.min(ics) >= 0.95, f'mean {np.mean(ics):.5f} over {len(ics)} dates, min {np.min(ics):.5f}')

# 3. look-ahead: truncate at three month-ends
for cut in ('2012-06-29', '2019-12-31', '2024-03-28'):
    p2, v2, h2, l2, o2 = [d.loc[:cut] for d in (prices, volumes, highs, lows, opens)]
    b2 = ele.build_benchmark(p2)
    c2 = CSMZenithResid(prices_df=p2, volumes_df=v2, highs_df=h2, lows_df=l2, opens_df=o2, benchmark_series=b2, resid_weight=0.5); c2.calculate_factors()
    me = pd.Timestamp(cut) + pd.offsets.MonthEnd(0)
    r2 = c2.resid_mom.loc[me].dropna(); r1 = til['zenith'].resid_mom.loc[me].dropna(); j = r1.index.intersection(r2.index)
    check(f'3. no look-ahead at {cut} (residual momentum row unchanged by truncation)', len(j) > 300 and np.allclose(r1[j], r2[j], rtol=1e-9, atol=1e-12), f'{len(j)} names compared; max abs diff {np.abs(r1[j]-r2[j]).max():.2e}')

# 4. engine returns vs research variant
for n, mod in (('zenith', zen), ('elendel', ele)):
    c = til[n]; c.get_positions()
    res = mod.backtest_event_driven(c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    ref = pickle.load(open('/Users/hemantsoni/Documents/long_only_strategies/momentum_value/.cache/impr_%s.pkl' % n, 'rb'))[('live', '+0.5*resid')]['net_returns']
    r = res['net_returns']; j = r.index.intersection(ref.index)
    d = (r[j] - ref[j]).abs()
    cg = lambda x: (1+x).prod()**(252/len(x))-1
    check(f'4. {n}: native tilted engine ~ research variant (daily corr >= 0.99 and |CAGR diff| <= 1.5 pt)', r[j].corr(ref[j]) > 0.99 and abs(cg(r[j])-cg(ref[j])) <= 0.015,
          f'max abs daily diff {d.max():.2e}, corr {r[j].corr(ref[j]):.5f}, CAGR {res["cagr"]*100:.2f}% vs research {((1+ref).prod()**(252/len(ref))-1)*100:.2f}%')
print('\nALL PASS' if not fails else f'\nFAILED: {fails}'); sys.exit(1 if fails else 0)

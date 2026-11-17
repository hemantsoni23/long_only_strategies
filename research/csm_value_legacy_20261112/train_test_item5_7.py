"""
train_test_item5_7.py -- Item 5 (earnings-quality / one-off profits) and Item 7 (profit definition, idle cash) evaluated with the train/test discipline.
The return booking is NOT touched (the runner's headline stays the engine booking; the faithful booking is reported alongside, unchanged).

Pre-declared grid (idle-cash sweep into a 6.5% liquid fund is on in every grid cell because it is a mechanical, not a fitted, choice):
    profit definition  {total net profit, owners_consistent, core (net profit less other income and exceptional items, 25% tax)}
  x one-off filter     {off, drop names whose TTM other income + exceptional gains exceed 50% / 25% of TTM pre-tax profit (banks exempt)}
Selection: highest TRAIN (2019-06-03..2021-12-31) Sharpe on the headline (engine) booking; the chosen cell is scored on TEST (2022-01-03..2025-06-30) once.
Reference rows: the committed strategy (total, no filter, idle cash 0%) and 'idle-cash sweep only'.
    python3 train_test_item5_7.py -> output/train_test_item5_7.txt
"""
import os, sys, io, contextlib, itertools, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue
W = {'FULL': ('2019-06-03', '2025-06-30'), 'TRAIN': ('2019-06-03', '2021-12-31'), 'TEST': ('2022-01-03', '2025-06-30')}
def q(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)
def m(r):
    r = r.dropna(); eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25
    return eq.iloc[-1] ** (1 / y) * 100 - 100, r.mean() / r.std() * np.sqrt(252), ((eq / eq.cummax()) - 1).min() * 100
prices, volumes, highs, lows, opens = q(rb.load_data, rb.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = q(rb.mask_corporate_actions, prices, highs, lows, opens); bench = rb.build_benchmark(prices)
def run(**kw):
    c = CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, **kw)
    q(c.calculate_factors); q(c.get_positions); q(rb.backtest_event_driven, c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    return c._net_by_booking, c
lines = []
def say(s=''): print(s, flush=True); lines.append(s)
def row(lab, nb, w):
    a, b = W[w]; e = m(nb['engine'].loc[a:b]); f = m(nb['faithful'].loc[a:b])
    return f"  {lab:<44} engine: CAGR {e[0]:5.1f}% Sh {e[1]:4.2f} DD {e[2]:6.1f}%  |  faithful: CAGR {f[0]:5.1f}% Sh {f[1]:4.2f} DD {f[2]:6.1f}%"
res = {}
base_nb, _ = run(use_liquid_mf=False); res['REF committed (total, no filter, idle cash 0%)'] = base_nb
sw_nb, _ = run(use_liquid_mf=True); res['REF idle-cash sweep only'] = sw_nb
grid = {}
for pb, mo in itertools.product(('total', 'owners_consistent', 'core'), (None, 0.50, 0.25)):
    key = f"{pb}, one-off filter {'off' if mo is None else int(mo*100)}%"
    nb, _ = run(profit_basis=pb, max_oneoff_share=mo); grid[key] = nb; res[key] = nb
say('=' * 130); say(' TRAIN 2019-06-03 .. 2021-12-31 (selection uses ONLY the engine-booking Sharpe on this window)'); say('=' * 130)
for k, nb in res.items(): say(row(k, nb, 'TRAIN'))
trs = {k: m(nb['engine'].loc[W['TRAIN'][0]:W['TRAIN'][1]]) for k, nb in grid.items()}
best = max(trs, key=lambda k: trs[k][1]); say(f'\n  SELECTED on train: {best}')
for w in ('TEST', 'FULL'):
    say(''); say('=' * 130); say(f' {w} {W[w][0]} .. {W[w][1]}' + ('   (scored once for the selected cell; others shown for transparency, not used)' if w == 'TEST' else '')); say('=' * 130)
    for k, nb in res.items(): say(row(('>> ' if k == best else '') + k, nb, w))
open(os.path.join(HERE, 'output', 'train_test_item5_7.txt'), 'w').write('\n'.join(lines) + '\n')

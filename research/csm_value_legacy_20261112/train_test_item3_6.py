"""
train_test_item3_6.py -- Item 6 (re-entry churn) and Item 3 (capacity) with train/test discipline.  Costs, slippage and the return booking are unchanged (0.30% per side, 0.30% stop slippage).

ITEM 6.  The Elendel cooldown is loss-scaled: a stop that exits at a PROFIT gets a cooldown of 0 days, so a name stopped out by the peak stop can be bought again the next day if it is still in the
target set (this is why 41% of trades are re-entries within 30 days).  `min_cooldown_days` puts a floor under every stop.  Pre-declared grid: floor in {0 (current), 21, 42, 63, 126} calendar days.
Selection: highest TRAIN (2019-06-03..2021-12-31) Sharpe, engine booking; TEST (2022-01-03..2025-06-30) scored once for the chosen floor.
ITEM 3.  Capacity-aware sizing: position <= 10% of the name's 63-day median traded value for an assumed book of B crore (excess weight stays in cash, which earns 6.5%).  A pre-declared curve
B in {none, 20, 10, 5, 3, 1} crore on top of the Item-6 choice -- not a selection: the book size is a decision about capital, this shows what each size costs.
    python3 train_test_item3_6.py -> output/train_test_item3_6.txt
"""
import os, sys, io, contextlib, numpy as np, pandas as pd, warnings
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
    q(c.calculate_factors); q(c.get_positions); res = q(rb.backtest_event_driven, c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    tl = q(rb.get_trade_log, c); Wt = res['executed_weights'].loc[W['FULL'][0]:W['FULL'][1]]
    tl = tl[tl.Entry_Date >= pd.Timestamp(W['FULL'][0])].sort_values(['Ticker', 'Entry_Date']); gap = (tl.Entry_Date - tl.groupby('Ticker').Exit_Date.shift(1)).dt.days
    info = dict(trades=len(tl), reentry30=float((gap <= 30).mean()), turnover=float(Wt.diff().abs().sum(axis=1).mean() * 252 * 100), invested=float(Wt.sum(axis=1).mean() * 100), pos=float((Wt > 1e-6).sum(axis=1).mean()))
    return c._net_by_booking, info
lines = []
def say(s=''): print(s, flush=True); lines.append(s)
def fmt(nb, w):
    a, b = W[w]; e, f = m(nb['engine'].loc[a:b]), m(nb['faithful'].loc[a:b])
    return f"engine {e[0]:5.1f}% / {e[1]:4.2f} / {e[2]:6.1f}%  |  faithful {f[0]:5.1f}% / {f[1]:4.2f} / {f[2]:6.1f}%"
say('=' * 140); say(' ITEM 6 -- minimum re-entry cooldown after any stop (CAGR / Sharpe / max DD)'); say('=' * 140)
res6 = {}
for fl_ in (0, 21, 42, 63, 126):
    nb, info = run(min_cooldown_days=fl_); res6[fl_] = (nb, info)
    say(f" floor {fl_:>3}d | TRAIN {fmt(nb, 'TRAIN')} | trades {info['trades']:>3}  re-entries<=30d {info['reentry30']:.0%}  one-way turnover {info['turnover']:.0f}%/yr  invested {info['invested']:.0f}%")
best = max(res6, key=lambda k: m(res6[k][0]['engine'].loc[W['TRAIN'][0]:W['TRAIN'][1]])[1]); say(f'\n SELECTED on train: floor {best}d')
for w in ('TEST', 'FULL'):
    say(f'\n {w} {W[w][0]}..{W[w][1]}' + ('  (scored once for the selected floor; others shown for transparency)' if w == 'TEST' else ''))
    for k, (nb, info) in res6.items(): say(f"  {'>>' if k == best else '  '} floor {k:>3}d | {fmt(nb, w)}")
say(''); say('=' * 140); say(f' ITEM 3 -- capacity curve on top of floor {best}d: position <= 10% of 63-day median traded value (book size B in Rs crore)'); say('=' * 140)
for B in (None, 20, 10, 5, 3, 1):
    nb, info = run(min_cooldown_days=best, book_size_cr=B)
    say(f" B = {'none' if B is None else str(B)+' cr':<7}| FULL {fmt(nb, 'FULL')} | TEST {fmt(nb, 'TEST')} | invested {info['invested']:.0f}%  positions {info['pos']:.1f}")
open(os.path.join(HERE, 'output', 'train_test_item3_6.txt'), 'w').write('\n'.join(lines) + '\n')

"""Parity: the self-contained CSMIndustryBook must reproduce the research simulator (factor_research/industry_book.py, D1v spec) exactly.  python3 test_parity.py"""
import os
import sys
import time
import warnings
import numpy as np
import pandas as pd
warnings.filterwarnings('ignore')

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FR = os.path.join(ROOT, 'factor_research')
sys.path.insert(0, HERE); sys.path.insert(0, FR)
os.chdir(FR)
from industry_book_strategy import CSMIndustryBook          # noqa: E402
import industry_book as ib                                   # noqa: E402
from data import load_panels                                 # noqa: E402

t = time.time()
P = load_panels()
SCORE = sys.argv[1] if len(sys.argv) > 1 else 'zen'
s = CSMIndustryBook(P['close'], P['volume'], P['high'], P['low'], P['open'], instruments_path=os.path.join(ROOT, 'instruments_clean.csv'), score=SCORE)
s.calculate_factors(); s.get_positions(); r_new = s.backtest()
print(f'new class ({SCORE} score): {time.time()-t:.0f}s')

bd = ib.load_book_data()
res = ib.run(bd, ib.Spec(vol_target=0.15, score=SCORE))
r_old = res['ret']

same_idx = r_new.index.equals(r_old.index)
d = (r_new - r_old.reindex(r_new.index)).abs().max() if same_idx else float('nan')
used = s.b >= 0                                              # rows the backtest can trade; the newest row (no fill bar yet) is the live-order row
dc = float(np.abs(s.cohorts[used] - res['C'][used]).max())
print(f'index equal: {same_idx} ({len(r_new)} vs {len(r_old)})   max|d cohort weights| = {dc:.2e}   max|d daily net returns| = {d:.2e}')
m = lambda x: ib.metrics(x, 0.0)
for lbl, x in (('class', r_new), ('research', r_old)):
    mm = m(x); print(f'{lbl:<9} CAGR {mm["cagr"]*100:5.2f}%  vol {mm["vol"]*100:4.1f}%  Sharpe {mm["sharpe"]:.3f}  MaxDD {mm["maxdd"]*100:6.2f}%')
assert dc == 0.0 and d < 1e-9, 'PARITY FAILED'
print('PARITY PASS')
lo = s.live_orders()
print('latest signal', lo['signal_date'].date(), '| gate_up', lo['gate_up'], '| vol scale %.2f' % lo['vol_scale'], '| names', len(lo['weights']), '| cash %.1f%%' % (lo['cash_weight'] * 100))
print('industries:', lo['industries'])

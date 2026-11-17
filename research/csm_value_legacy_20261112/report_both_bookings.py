"""CSM Value default configuration, both return bookings side by side on FULL / TRAIN / TEST (Sharpe rf 0).  python3 report_both_bookings.py -> output/both_bookings.txt
engine booking   = the Elendel engine's own (executed weight x same-day close-to-close return) -- comparable with the Elendel / Zenith / Quad backtests
faithful booking = also charges the gap to the real stop / sell fill (AUDIT.md)"""
import os, sys, numpy as np, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue
W = {'FULL  2019-06-03..2025-06-30': ('2019-06-03', '2025-06-30'), 'TRAIN 2019-06-03..2021-12-31': ('2019-06-03', '2021-12-31'), 'TEST  2022-01-03..2025-06-30': ('2022-01-03', '2025-06-30')}
def m(r):
    r = r.dropna(); eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25; dd = eq / eq.cummax() - 1
    return eq.iloc[-1] ** (1 / y) * 100 - 100, r.std() * np.sqrt(252) * 100, r.mean() / r.std() * np.sqrt(252), dd.min() * 100
prices, volumes, highs, lows, opens = rb.load_data(rb.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens); bench = rb.build_benchmark(prices)
c = CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)
c.calculate_factors(); c.get_positions(); rb.backtest_event_driven(c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
lines = []
for wn, (a, b) in W.items():
    lines.append(wn)
    for k, lab in (('engine', 'engine booking (headline, = Elendel/Zenith/Quad convention)'), ('faithful', 'execution-faithful booking')):
        cg, vol, sh, dd = m(c._net_by_booking[k].loc[a:b]); lines.append(f'  {lab:<58} CAGR {cg:5.1f}%  vol {vol:4.1f}%  Sharpe {sh:4.2f}  MaxDD {dd:6.1f}%')
txt = '\n'.join(lines); print(txt); open(os.path.join(HERE, 'output', 'both_bookings.txt'), 'w').write(txt + '\n')

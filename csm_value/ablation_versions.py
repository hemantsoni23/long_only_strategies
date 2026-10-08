"""Ablation of the three data-handling versions on identical windows (same chassis, default configuration: net profit = total, liquidity ranks 301-1000, profit growth on, top 15).
   v1 'leaky'      : filed share counts used as-is with split-adjusted prices           (restore_units=False, use_ca_mask=False)
   v2 'units'      : share counts restored to today's units                              (restore_units=True,  use_ca_mask=False)
   v3 'units + CA mask' (current default): v2 + price-cliff awareness and stale-share mask (restore_units=True, use_ca_mask=True)
python3 ablation_versions.py -> output/ablation_versions.txt"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue
W = {'FULL 2019-06-03..2025-06-30': ('2019-06-03', '2025-06-30'), 'TRAIN 2019-06-03..2021-12-31': ('2019-06-03', '2021-12-31'), 'TEST 2022-01-03..2025-06-30': ('2022-01-03', '2025-06-30')}
def metrics(r):
    r = r.dropna(); eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25; dd = eq / eq.cummax() - 1
    return r.add(1).prod() ** (1 / y) * 100 - 100, r.mean() / r.std() * np.sqrt(252), dd.min() * 100
prices, volumes, highs, lows, opens = rb.load_data(rb.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens); bench = rb.build_benchmark(prices)
out = {}
for name, kw in (('v1 leaky (raw filed shares)', dict(restore_units=False, use_ca_mask=False)), ('v2 units restored', dict(restore_units=True, use_ca_mask=False)), ('v3 units + CA mask (default)', dict())):
    c = CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, **kw)
    c.calculate_factors(); c.get_positions()
    out[name] = rb.backtest_event_driven(c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)['net_returns']
lines = []
for wn, (a, b) in W.items():
    lines.append(f'\n{wn}   (CAGR %, Sharpe rf0, MaxDD %)')
    for n, r in out.items():
        cg, sh, dd = metrics(r.loc[a:b]); lines.append(f'  {n:<30} CAGR {cg:5.1f}  Sharpe {sh:4.2f}  MaxDD {dd:6.1f}')
txt = '\n'.join(lines); print(txt); open(os.path.join(HERE, 'output', 'ablation_versions.txt'), 'w').write(txt + '\n')

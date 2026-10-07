"""Native tilted engines vs the unmodified live engines (daily returns, same data/costs).  python3 compare_to_live.py -> output/compare_to_live.txt, output/daily_returns_*.csv
Live baselines are the cached unmodified runs in momentum_gold/.cache (identical settings: 0.3% cost, rfr 0, universe 1-1000 / 1-1000)."""
import os, sys, pickle, importlib, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from resid_tilt_strategies import CSMZenithResid, CSMElendelResid
ele = importlib.import_module('run_csm_elendel_backtest'); zen = importlib.import_module('run_csm_zenith_backtest')
OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
def metrics(r, rf=0.06):
    r = r.dropna(); eq = (1+r).cumprod(); y = len(r)/252
    return dict(cagr=eq.iloc[-1]**(1/y)-1, vol=r.std()*np.sqrt(252), sharpe=((r-((1+rf)**(1/252)-1)).mean()/r.std())*np.sqrt(252), maxdd=(eq/eq.cummax()-1).min())
def boot(d, B=4000, blk=21, seed=7):
    d = np.asarray(d.dropna()); n = len(d); rng = np.random.default_rng(seed); k = int(np.ceil(n/blk)); o = []
    for _ in range(B):
        st = rng.integers(0, n, k); o.append(d[((st[:, None]+np.arange(blk)) % n).ravel()[:n]].mean()*252)
    o = np.array(o); return (o > 0).mean(), np.percentile(o, 5)*100, np.percentile(o, 95)*100
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2026-07-16']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
kw = dict(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)
lines = []
def say(s=''): print(s); lines.append(s)
for n, cls, mod in (('zenith', CSMZenithResid, zen), ('elendel', CSMElendelResid, ele)):
    live = pickle.load(open(f'/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache/engine_{n}.pkl', 'rb'))['net_returns']
    rows = {'live': live}
    for w in (0.5,):
        c = cls(resid_weight=w, **kw); c.calculate_factors(); c.get_positions()
        res = mod.backtest_event_driven(c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
        rows[f'tilt w={w}'] = res['net_returns']
    pd.DataFrame(rows).to_csv(os.path.join(OUT, f'daily_returns_{n}.csv'))
    say(f'\n=== {n.upper()}  (idle cash as in the engine: {"6.5% liquid fund" if n=="zenith" else "0%"})')
    for wn, (a, b) in {'2005+': ('2005-01-01', '2026-07-16'), '2015+': ('2015-01-01', '2026-07-16'), '2020+': ('2020-01-01', '2026-07-16')}.items():
        ml = metrics(live.loc[a:b])
        for k, r in rows.items():
            m = metrics(r.loc[a:b]); s = f"  {wn:<6} {k:<10} CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:4.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['maxdd']*100:6.1f}%"
            if k != 'live':
                p, lo, hi = boot(r.loc[a:b] - live.loc[a:b]); s += f"  | dCAGR {100*(m['cagr']-ml['cagr']):+5.1f}pt dSharpe {m['sharpe']-ml['sharpe']:+.2f}  P(better) {p:.2f}  90% CI of annual excess [{lo:+.1f}, {hi:+.1f}]%"
            say(s)
    yr = pd.DataFrame({k: (1+r.loc['2003':]).groupby(r.loc['2003':].index.year).prod()-1 for k, r in rows.items()})*100
    yr['delta'] = yr['tilt w=0.5'] - yr['live']; say('  year-by-year delta (pts): ' + '  '.join(f'{y}:{v:+.1f}' for y, v in yr['delta'].items()))
    say(f'  years better: {(yr["delta"]>0).sum()} of {len(yr)}')
open(os.path.join(OUT, 'compare_to_live.txt'), 'w').write('\n'.join(lines)+'\n')

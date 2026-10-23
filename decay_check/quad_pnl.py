"""Live Quad engine (read-only import) under several bands/lookbacks, faithful re-booking via csm_value/execution_replay."""
import sys, os, io, contextlib, pickle, gc
import numpy as np, pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'); sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/csm_value'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
from execution_replay import faithful_net_returns
P = C.load_panels(); px, vol, hi, lo, op, bench = P['close'], P['volume'], P['high'], P['low'], P['open'], P['bench']
CFG = [('b500-1000 LIVE', 500, 1000, (6, 12)), ('b1-1000', 1, 1000, (6, 12)), ('b1-500', 1, 500, (6, 12)), ('b500-1500', 500, 1500, (6, 12)), ('b250-1000', 250, 1000, (6, 12)), ('b500-1000 (3,6)', 500, 1000, (3, 6))]
out = {}
with contextlib.redirect_stdout(io.StringIO()):
    import run_csm_quad_momentum_backtest as Q
    from csm_quad_momentum_strategy import CSMQuadMomentum
for name, a, b, lb in CFG:
    with contextlib.redirect_stdout(io.StringIO()):
        s = CSMQuadMomentum(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench, lookbacks=lb, universe_top_n_min=a, universe_top_n_max=b)
        s.calculate_factors(); s.get_positions()
        res = Q.backtest_event_driven(s, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
        rate = ((1 + s.liquid_mf_annual_rate) ** (1 / 252) - 1) if s.use_liquid_mf else 0.0
        net, info = faithful_net_returns(s, res, 0.003, rate)
    meta = pd.DataFrame(s.position_metadata)
    out[name] = dict(engine=res['net_returns'], faithful=net, ntrades=len(meta), stops=int((meta.Exit_Reason == 'STOP_HIT').sum()))
    r = net.loc['2003-01-01':]; print(name, 'faithful CAGR', round((1 + r).prod() ** (252 / len(r)) - 1, 4), 'engine CAGR', round((1 + res['net_returns'].loc['2003-01-01':]).prod() ** (252 / len(r)) - 1, 4), 'trades', len(meta), flush=True)
    del s, res; gc.collect()
pickle.dump(out, open(f'{C.CACHE}/quad_pnl.pkl', 'wb'))

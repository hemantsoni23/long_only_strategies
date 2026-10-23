"""Quad signal under different universe bands / lookbacks (live CSMQuadMomentum class, read-only import)."""
import sys, os, io, contextlib, pickle, gc
import numpy as np, pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels(); px, vol, hi, lo, op, bench = P['close'], P['volume'], P['high'], P['low'], P['open'], P['bench']
from csm_quad_momentum_strategy import CSMQuadMomentum
CFG = [('b1-500', (1, 500), (6, 12)), ('b1-1000', (1, 1000), (6, 12)), ('b250-1000', (250, 1000), (6, 12)), ('b500-1000 LIVE', (500, 1000), (6, 12)),
       ('b500-1500', (500, 1500), (6, 12)), ('b1000-3000', (1000, 3000), (6, 12)),
       ('b500-1000 (3,6)', (500, 1000), (3, 6)), ('b500-1000 (3,6,12)', (500, 1000), (3, 6, 12)), ('b500-1000 (3,6,9,12)', (500, 1000), (3, 6, 9, 12)),
       ('b1-1000 (3,6)', (1, 1000), (3, 6)), ('b1-1000 (3,6,12)', (1, 1000), (3, 6, 12)), ('b1-1000 (3,6,9,12)', (1, 1000), (3, 6, 9, 12))]
out = {}
for name, (a, b), lb in CFG:
    with contextlib.redirect_stdout(io.StringIO()):
        s = CSMQuadMomentum(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench, lookbacks=lb, universe_top_n_min=a, universe_top_n_max=b)
        s.calculate_factors()
    F = C.to_period_index(s.factors.astype('float64')).loc[:C.ANCHOR]
    out[name] = F; print(name, F.shape, round(F.notna().sum(axis=1).mean(), 1), flush=True)
    del s; gc.collect()
pickle.dump(out, open(f'{C.CACHE}/quad_variants.pkl', 'wb'))

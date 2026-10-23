import sys, os, io, contextlib, pickle
import pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
P = C.load_panels()
with contextlib.redirect_stdout(io.StringIO()):
    from residual_momentum_strategy import ResidualMomentumStrategy
    s = ResidualMomentumStrategy(P['close'], P['volume'], P['high'], P['low'], P['open'], universe_top_n=1000, min_price=20.0, min_adv=1e7,
                                 rebalance_freq_months=1, z9_weight=1.0, high52_weight=1.0, illiq_weight=0.0, lowpx_weight=0.0, beta_shrink=0.0)
    s.calculate_factors()
    F = C.to_period_index(s.R3b.loc[C.month_end_days(P['close'].index)].astype('float64')).loc[:C.ANCHOR]
    Z9 = C.to_period_index(s.z9.loc[C.month_end_days(P['close'].index)].astype('float64')).loc[:C.ANCHOR]
pickle.dump(dict(R3b=F, z9=Z9), open(f'{C.CACHE}/r3b1000.pkl', 'wb')); print(F.shape, F.notna().sum(axis=1).mean())

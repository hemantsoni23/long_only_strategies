"""Instantiate each LIVE strategy class (imported read-only from Old_live_strategies) with its runner/production parameters and
save its monthly factor frame (month x stock, period index) + top_n.  usage: python build_factors.py <name>"""
import sys, os, io, contextlib, pickle, gc
import numpy as np, pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

name = sys.argv[1]
P = C.load_panels()
px, vol, hi, lo, op, bench = P['close'], P['volume'], P['high'], P['low'], P['open'], P['bench']
quiet = io.StringIO()
TOP_N = dict(residual=40, absolute=25, batch=30, elendel=15, zenith=15, quad=15)

with contextlib.redirect_stdout(quiet):
    if name == 'residual':
        from residual_momentum_strategy import ResidualMomentumStrategy
        s = ResidualMomentumStrategy(px, vol, hi, lo, op, universe_top_n=500, min_price=20.0, min_adv=1e7,
                                     rebalance_freq_months=1, z9_weight=1.0, high52_weight=1.0,
                                     illiq_weight=0.0, lowpx_weight=0.0, beta_shrink=0.0)
        s.calculate_factors()
        me = C.month_end_days(px.index)
        F = s.R3b.loc[me]
    elif name == 'absolute':
        from csm_absolute import IndividualMomentumStrategy
        s = IndividualMomentumStrategy(px, vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench,
            lookback_months=9, lookback_short_months=4, atr_period=13, atr_multiplier=2.0, lag_months=1,
            sharpe_threshold=0.6, capacity_limit=25, universe_top_n=1000, leverage_bull=1.0, leverage_bear=0.8,
            leverage_panic=0.5, min_price=20.0, max_circuit_days=8, max_weight_per_stock=0.12, stop_std_devs=3.0,
            use_rebalance=True, rebalance_months=3, use_trailing=True, reentry_cooldown_days=7, rank_buffer=1.5,
            cooldown_losers_only=True, use_take_profit=True)
        s.calculate_factors(); F = s.factors
    elif name == 'batch':
        from csm_batch_strategy import CrossSectionalMomentum
        s = CrossSectionalMomentum(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op,
            benchmark_series=bench, lookback_months=12, lag_months=1, top_n=30, min_price=20.0, universe_top_n=1000,
            max_circuit_days=5, buffer_ratio=0.20, atr_period=14, atr_multiplier=3.0, atr_multiplier_high_vol=2.0,
            hard_stop_from_entry=0.15, hard_stop_from_peak=0.20, stop_slippage_pct=0.003, use_trailing_stop=False,
            stop_cooldown_days=20, min_hold_days=0, use_crash_guard=True, crash_guard_cooldown=10,
            corr_guard_threshold=0.8, vol_target=0.13, max_weight_per_stock=0.05, rebalance_months=3,
            rank_exit_dynamic=True, rank_exit_drop_frac=0.33, rank_exit_floor_frac=0.67)
        s.calculate_factors(); F = s.factors
    elif name == 'elendel':
        from csm_elendel_strategy import CSMElendel
        s = CSMElendel(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench,
                       universe_top_n_min=1, universe_top_n_max=1000)
        s.calculate_factors(); F = s.factors
    elif name == 'zenith':
        from csm_zenith_strategy import CSMZenith
        s = CSMZenith(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench,
                      universe_top_n_min=1, universe_top_n_max=1000)
        s.calculate_factors(); F = s.factors
    elif name == 'quad':
        from csm_quad_momentum_strategy import CSMQuadMomentum
        s = CSMQuadMomentum(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op, benchmark_series=bench,
                            universe_top_n_min=500, universe_top_n_max=1000)
        s.calculate_factors(); F = s.factors
    else:
        raise SystemExit('unknown')

F = C.to_period_index(F.astype('float64'))
F = F.loc[:C.ANCHOR]
legs = {}
if hasattr(s, 'factor_legs') and isinstance(getattr(s, 'factor_legs'), dict):
    for k, v in s.factor_legs.items():
        legs[str(k)] = C.to_period_index(v.astype('float64')).loc[:C.ANCHOR]
with open(os.path.join(C.CACHE, f'factors_{name}.pkl'), 'wb') as f:
    pickle.dump(dict(F=F, legs=legs, top_n=TOP_N[name]), f)
print(name, F.shape, F.index.min(), F.index.max(), 'avg names/month', round(F.notna().sum(axis=1).mean(), 1), 'legs', list(legs))

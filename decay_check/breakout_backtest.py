"""Run the LIVE breakout engines (imported read-only from Old_live_strategies) over the full history with runner parameters.
usage: python breakout_backtest.py hr|vcp [cash_yield]   -> .cache/bt_<w>_cy<cash>.pkl  (net_returns, exposure, trade log)"""
import sys, os, io, contextlib, pickle
import numpy as np, pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
w = sys.argv[1]; cy = float(sys.argv[2]) if len(sys.argv) > 2 else 0.0; var = sys.argv[3] if len(sys.argv) > 3 else 'base'
P = C.load_panels(); px, vol, hi, lo, op = P['close'], P['volume'], P['high'], P['low'], P['open']
quiet = io.StringIO()
with contextlib.redirect_stdout(quiet):
    if w == 'hr':
        import run_hr_breakout_v2 as R
        from hr_breakout_v2 import HRBreakoutStrategy
        S = HRBreakoutStrategy(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op,
            universe_top_n=500, universe_min_n=1, min_price=10.0, max_circuit_days=5, prior_month_min_ret=-0.15,
            benchmark_sma_period=50, benchmark_streak_max=5, ema_fast=50, ema_mid=150, ema_slow=200, ema_slope_window=20,
            high_band_pct=0.75, rs_lookback=126, rs_top_pct=0.25, peak_wing=2, cluster_lookback=60, cluster_min_peaks=3,
            cluster_spread_pct=0.015, breakout_buffer=0.005, entry_gap_cancel_pct=0.03, momentum_rank_window=30,
            max_positions=10, risk_pct_per_trade=0.01, position_ceil=0.15, position_floor=0.02, atr_period=14,
            atr_multiplier_max=2.5, atr_multiplier_min=1.5, atr_pct_calm=0.020, atr_pct_volatile=0.045,
            chandelier_clamp_min=0.12, chandelier_clamp_max=0.30, hard_stop_from_entry=0.15, hard_stop_from_peak=0.15,
            stop_slippage_pct=0.0, stop_cooldown_days=20, min_hold_days=20, time_stop_min_days=45,
            time_stop_min_profit=-0.05, warmup_days=252)
    else:
        import run_vcp_v4 as R
        from vcp_v4 import VCPBreakoutStrategy
        S = VCPBreakoutStrategy(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op,
            universe_top_n=1000, universe_min_n=500, min_price=10.0, max_circuit_days=5, ca_drop_thresh=0.40, ca_gain_thresh=3.00,
            bench_sma_period=50, bench_consec_days=5, sma_fast=50, sma_mid=150, sma_slow=200, sma_slope_lookback=20,
            high_52w_period=252, within_52w_high_pct=0.25, rs_period=252, rs_min_percentile=75, vcp_base_window=15,
            vcp_base_tight_pct=0.15, vcp_vol_contract_pct=0.80, vcp_vol_base_window=30, vcp_breakout_window=20,
            vcp_near_high_pct=0.10, max_positions=10, entry_gap_cancel_pct=0.03, risk_pct_per_trade=0.01,
            weight_min=0.02, weight_max=0.20, liquidity_cap_pct=0.10, hard_stop_pct=0.15, trail_activate_pct=0.10,
            trail_pct=0.05, trail_floor_pct=0.001, trail_atr_mult_max=2.5, trail_atr_mult_min=1.5, trail_atr_pct_calm=0.020,
            trail_atr_pct_volatile=0.045, min_hold_days=15, stale_days=60, stale_ret_pct=0.05, lockout_days=30, warmup_days=252)
    S.calculate_factors()
    if var == 'noregime':
        S._compute_regime_flags = lambda: pd.Series(True, index=S._prices_ff.index)
    elif var == 'nopattern':
        if w == 'hr': S._find_hr_signal = lambda stock, i: (True, np.nan)
        else: S._vcp_signal_matrix[:] = True
    elif var == 'notrend':
        if w == 'hr': S._trend_gate = lambda i, universe_mask=None: pd.Series(True, index=S._prices_ff.columns)
        else: S._trend_mask_matrix[:] = True
    res = R.backtest_event_driven(S, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0, cash_yield=cy)
    tl = R.get_trade_log(S)
out = dict(net=res['net_returns'], expo=res['executed_weights'].sum(axis=1), trades=tl, bench=S._bench_series)
pickle.dump(out, open(f'{C.CACHE}/bt_{w}_cy{cy}' + ('' if var == 'base' else '_' + var) + '.pkl', 'wb'))
print(w, var, 'cash_yield', cy, 'days', len(out['net']), 'trades', len(tl), 'CAGR', round((1 + out['net']).prod() ** (252 / len(out['net'])) - 1, 4))

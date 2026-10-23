import sys, os, pickle, io, contextlib
import pandas as pd, numpy as np
OLD='/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
sys.path.insert(0, OLD)
SP=os.path.dirname(os.path.abspath(__file__))
CACHE=os.environ.get('CSM_DATA') or f'{SP}/data.pkl'
FOLDER='/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'

def data():
    if os.path.exists(CACHE):
        return pickle.load(open(CACHE,'rb'))
    from csm_batch_strategy import load_data
    d = load_data(FOLDER)
    pickle.dump(d, open(CACHE,'wb'))
    return d

BASE = dict(lookback_months=12, lag_months=1, top_n=30, min_price=20.0, universe_top_n=1000,
    max_circuit_days=5, buffer_ratio=0.20, atr_period=14, atr_multiplier=3.0,
    atr_multiplier_high_vol=2.0, hard_stop_from_entry=0.15, hard_stop_from_peak=0.20,
    stop_slippage_pct=0.003, use_trailing_stop=False, stop_cooldown_days=20, min_hold_days=0,
    use_crash_guard=True, crash_guard_cooldown=10, corr_guard_threshold=0.8, vol_target=0.13,
    max_weight_per_stock=0.05, rebalance_months=3, rank_exit_dynamic=True,
    rank_exit_drop_frac=0.33, rank_exit_floor_frac=0.67)

def run(cfg=None, bt='csm_batch_backtest1', load=('2012-01-01','2025-12-31'), report='2013-01-01',
        txn=0.003, rfr=0.0, quiet=True, strat_mod='csm_batch_strategy'):
    import importlib
    S = importlib.import_module(strat_mod); B = importlib.import_module(bt)
    prices, volumes, highs, lows, opens = data()
    sl = lambda df: df.loc[load[0]:load[1]] if not df.empty else df
    prices, volumes, highs, lows, opens = map(sl,(prices, volumes, highs, lows, opens))
    bench = (1 + prices.pct_change(fill_method=None).clip(-0.5,0.5).mean(axis=1,skipna=True).fillna(0.0)).cumprod()
    c = dict(BASE); c.update(cfg or {})
    buf = io.StringIO()
    ctx = contextlib.redirect_stdout(buf) if quiet else contextlib.nullcontext()
    with ctx:
        csm = S.CrossSectionalMomentum(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows,
                                        opens_df=opens, benchmark_series=bench, **c)
        csm.calculate_factors(); csm.get_positions()
        res = B.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=txn, risk_free_rate=rfr)
        res = B.slice_results(res, report, risk_free_rate=rfr)
        log = B.get_trade_log(csm)
        log = log[log['Entry_Date'] >= pd.Timestamp(report)] if not log.empty else log
        B.populate_trade_stats(res, log)
    return res, log, csm

def summ(res, log, tag=''):
    pv = res['portfolio_value']
    y = pv.resample('YE').last().pct_change()
    y.iloc[0] = pv.resample('YE').last().iloc[0]/pv.iloc[0]-1
    return (f"{tag:<28} CAGR {res['cagr']*100:6.2f}  Vol {res['volatility']*100 if 'volatility' in res else float('nan'):5.2f}  "
            f"MDD {res['max_drawdown']*100:6.2f}  Sharpe {res.get('sharpe',float('nan')):5.2f}  "
            f"Trades {len(log):5d}  WR {res.get('trade_win_rate',float('nan'))*100:5.1f}")

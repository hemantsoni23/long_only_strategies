"""Runs the UNMODIFIED live engines (Old_live_strategies) end-to-end and stores what the gold study needs.
Nothing in Old_live_strategies is edited; modules are imported and their functions called with the live defaults
(cost 0.3% one-way, rfr 0, factors/positions from the strategy classes' own defaults)."""
import os, sys, pickle, time, importlib
import numpy as np, pandas as pd
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
sys.path.insert(0, LIVE)
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache'); os.makedirs(OUT, exist_ok=True)
END = '2026-07-16'; LOAD_START = '2001-01-01'
which = sys.argv[1:] or ['elendel', 'zenith']

ele = importlib.import_module('run_csm_elendel_backtest')
t0 = time.time()
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc[LOAD_START:END] if not d.empty else d
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
print(f'data ready in {time.time()-t0:.0f}s  {prices.shape}  {prices.index[0].date()} -> {prices.index[-1].date()}', flush=True)

def run(name):
    t1 = time.time()
    if name == 'elendel':
        from csm_elendel_strategy import CSMElendel as S; mod = ele
    elif name == 'quad':
        q = importlib.import_module('run_csm_quad_momentum_backtest'); from csm_quad_momentum_strategy import CSMQuadMomentum as S; mod = q
    else:
        zen = importlib.import_module('run_csm_zenith_backtest'); from csm_zenith_strategy import CSMZenith as S; mod = zen
    csm = S(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench,
            universe_top_n_min=(500 if name == 'quad' else 1), universe_top_n_max=1000)   # each runner's own live default
    csm.calculate_factors(); csm.get_positions()
    res = mod.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    daily_cash_rate = ((1 + csm.liquid_mf_annual_rate) ** (1 / 252) - 1) if csm.use_liquid_mf else 0.0
    payload = dict(name=name, net_returns=res['net_returns'], executed_weights=res['executed_weights'], regime=res['regime'],
                   equity=res['equity_curve'], daily_cash_rate=daily_cash_rate, cagr=res['cagr'], sharpe=res['sharpe'], max_drawdown=res['max_drawdown'],
                   vol_scale=res['vol_scale'], params=dict(top_n=csm.top_n, max_weight=csm.max_weight_per_stock, leverage_bear=csm.leverage_bear,
                                                         leverage_panic=csm.leverage_panic, use_liquid_mf=csm.use_liquid_mf, liquid_mf_annual_rate=csm.liquid_mf_annual_rate))
    with open(os.path.join(OUT, f'engine_{name}.pkl'), 'wb') as f:
        pickle.dump(payload, f, protocol=4)
    print(f'[{name}] done in {time.time()-t1:.0f}s  CAGR {res["cagr"]*100:.2f}%  Sharpe {res["sharpe"]:.2f}  MaxDD {res["max_drawdown"]*100:.1f}%', flush=True)

for n in which:
    run(n)

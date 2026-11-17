"""Read-only CSM Absolute reference audit using observations through 2024.

The alternate accounting is an isolated diagnostic of return sensitivity; it
does not alter either live strategy or the user's requested CSM Value booking.
"""
import importlib.util
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2];OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'Old_live_strategies'))
from csm_absolute import IndividualMomentumStrategy,load_data
from limit_ordder_manager import LimitOrderManager
import csm_absolute_backtest as bt
import run_csm_absolute as config

spec=importlib.util.spec_from_file_location('absolute_prior_audit',ROOT/'research/csm_absolute_crash_guard/compare.py')
audit=importlib.util.module_from_spec(spec);spec.loader.exec_module(audit)

def synthetic_checks():
    obj=object.__new__(IndividualMomentumStrategy)
    try:obj.get_exit_signals(portfolio={},live_data={},benchmark_close=pd.Series([100.,101.]))
    except Exception as e:guard={'type':type(e).__name__,'message':str(e)}
    else:raise AssertionError('Expected current instance guard failure was not reproduced')
    m=LimitOrderManager(verbose=False,fill_assumption='limit_price')
    m._place_order(ticker='XYZ',order_type='STOP_LOSS',limit_price=100,
                   placed_date=pd.Timestamp('2024-01-01'),current_weight=.05,reason='audit')
    point=lambda x:pd.Series({'XYZ':x})
    weights,meta=m.process_day(date=pd.Timestamp('2024-01-02'),current_weights=point(.05),
        entry_prices={'XYZ':110},peak_highs={'XYZ':110},atr_values={'XYZ':5},atr_multiplier=2,
        today_open=point(80),today_high=point(90),today_low=point(75),today_close=point(85),prev_close=point(105))
    sessions=pd.to_datetime(['2024-08-30','2024-09-02','2024-09-03'])
    signal=pd.DataFrame({'XYZ':[1.]},index=pd.to_datetime(['2024-08-31']))
    applied=signal.reindex(sessions,method='ffill').shift(1).fillna(0.)
    first_active=str(applied.index[applied.XYZ>0][0].date())
    result={'guard_instance_error':guard,'guard_tested_method':'get_exit_signals',
            'limit_order_bar':{'open':80,'high':90,'low':75,'close':85,
            'limit':100,'simulated_fill':float(meta['fills'][0].fill_price),'resulting_weight':float(weights.XYZ)},
            'weekend_month_end_example':{'signal_label':'2024-08-31','last_trading_session':'2024-08-30',
            'next_trading_session':'2024-09-02','engine_first_active_session':first_active}}
    if result['limit_order_bar']['simulated_fill']<=90:raise AssertionError('Expected out-of-range fill was not reproduced')
    if first_active!='2024-09-03':raise AssertionError('Expected weekend month-end delay was not reproduced')
    return result

def metrics(r,start='2020-01-01',end='2024-12-31'):
    r=r.loc[start:end];eq=(1+r).cumprod();years=(r.index[-1]-r.index[0]).days/365.25
    return {'start':str(r.index[0].date()),'end':str(r.index[-1].date()),
            'cagr':float(eq.iloc[-1]**(1/years)-1),
            'max_drawdown':float((eq/eq.cummax().clip(lower=1)-1).min())}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    findings=synthetic_checks();print('SYNTHETIC',json.dumps(findings),flush=True)
    frames=[x.loc['2019-01-01':'2024-12-31'].sort_index() for x in load_data(config.DATA_FOLDER)]
    prices,volumes,highs,lows,opens=frames
    bench=(1+prices.pct_change().clip(-.5,.5).mean(axis=1)).cumprod()
    s=IndividualMomentumStrategy(prices,volumes,highs_df=highs,lows_df=lows,opens_df=opens,
        benchmark_series=bench,lookback_months=config.LOOKBACK_MONTHS,
        lookback_short_months=config.LOOKBACK_SHORT_MONTHS,atr_period=config.ATR_PERIOD,
        atr_multiplier=config.ATR_MULTIPLIER,lag_months=config.LAG_MONTHS,
        sharpe_threshold=config.SHARPE_THRESHOLD,capacity_limit=config.CAPACITY_LIMIT,
        universe_top_n=config.UNIVERSE_TOP_N,leverage_bull=config.LEVERAGE_BULL,
        leverage_bear=config.LEVERAGE_BEAR,leverage_panic=config.LEVERAGE_PANIC,
        min_price=config.MIN_PRICE,max_circuit_days=config.MAX_CIRCUIT_DAYS,
        max_weight_per_stock=config.MAX_WEIGHT_PER_STOCK,stop_std_devs=config.STOP_STD_DEVS,
        use_rebalance=config.USE_REBALANCE,rebalance_months=config.REBALANCE_MONTH,
        use_trailing=config.USE_TRAILING,reentry_cooldown_days=config.REENTRY_COOLDOWN_DAYS,
        rank_buffer=config.RANK_BUFFER,cooldown_losers_only=config.COOLDOWN_LOSERS_ONLY,
        use_take_profit=config.USE_TAKE_PROFIT)
    s.calculate_factors();s.get_positions()
    ref=bt.backtest_event_driven(s,**config.BT_KWARGS)
    trades=bt.generate_detailed_trade_log(s)
    selected=trades[(pd.to_datetime(trades.Entry_Date)>='2020-01-01') & (pd.to_datetime(trades.Entry_Date)<='2024-12-31')]
    s._research_guard=audit.guards(bench)['sma200']
    alternative=audit.research_engine()(s,**config.BT_KWARGS)
    weights_equal=bool(np.allclose(ref['executed_weights'],alternative['executed_weights'],equal_nan=True))
    if not weights_equal:raise AssertionError('Reference and accounting diagnostic changed holdings')
    source_files=['Old_live_strategies/csm_absolute.py','Old_live_strategies/csm_absolute_backtest.py',
                  'Old_live_strategies/run_csm_absolute.py','Old_live_strategies/limit_ordder_manager.py']
    findings.update({'cutoff':'2024-12-31','source_sha256':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in source_files},
       'universe':'original CSM Absolute settings, all OHLCV symbols, top 1000 turnover filter',
       'source_note':'Reference audit of a separate strategy; not a same-universe comparison with CSM Value.',
       'reference_zero_exit_weight':metrics(ref['net_returns']),
       'alternative_prior_weight_on_complete_exit':metrics(alternative['net_returns']),
       'same_executed_weights':weights_equal,'trades_entered_2020_2024':len(selected),
       'mean_holding_days':float(selected.Holding_Days.mean()),'median_holding_days':float(selected.Holding_Days.median())})
    pd.DataFrame({'reference':ref['net_returns'],'alternative':alternative['net_returns']}).loc[:'2024-12-31'].to_csv(OUT/'absolute_daily_accounting.csv',index_label='date')
    (OUT/'absolute_audit.json').write_text(json.dumps(findings,indent=2)+'\n')
    print('ABSOLUTE_RESULT',json.dumps(findings),flush=True)

if __name__=='__main__':main()

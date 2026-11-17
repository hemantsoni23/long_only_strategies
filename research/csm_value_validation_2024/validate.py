"""Frozen, pre-2025 robustness checks; no claim of an unseen holdout.

The candidate was chosen after this historical period was examined. Bootstrap
resamples fixed realized return streams; it is not a new market or a simulation
of the strategy under resampled prices.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('live_signal_research',ROOT/'research/csm_value_live_signals/study.py')
live=importlib.util.module_from_spec(spec);spec.loader.exec_module(live)
import run_csm_value_backtest as rb

START='2019-06-03';END='2024-12-31'
WINDOWS={'full':(START,END),'development':(START,'2021-12-31'),'previously_examined':('2022-01-03',END)}
MODES=('value','value_growth_pullback')
SCENARIOS=('reference','double_cost','zero_cash','tighter_close_stops','absolute_signal_gate')

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def signal_absolute(s):
    """Absolute's 9m/4m vol-scaled, 1m-lagged score and >0.6 gate only."""
    p=s.prices.resample('ME').last();r=p.pct_change(fill_method=None)
    legs=[]
    for n in (9,4):
        ret=p.shift(1)/p.shift(n+1)-1
        vol=(r.rolling(n).std().shift(1)*np.sqrt(12)).replace(0,np.nan)
        legs.append(ret/vol)
    score=((legs[0]+legs[1])/2).clip(-5,5)
    long_ret=p.shift(1)/p.shift(10)-1
    return (score>.6)&(long_ret>0)&score.notna()

def max_drawdown(r):
    eq=np.cumprod(1+r);peak=np.maximum.accumulate(np.r_[1.,eq])[1:]
    return float(np.min(eq/peak-1))

def bootstrap(a,b,seed=83119,n=2000,block=126):
    """Paired circular block resampling of daily realized returns."""
    a=np.asarray(a,float);b=np.asarray(b,float)
    if len(a)!=len(b) or len(a)<block:raise ValueError('insufficient paired daily returns')
    rng=np.random.default_rng(seed);N=len(a);idx=np.arange(block)
    d_cagr=[];d_dd=[];both=0
    for _ in range(n):
        starts=rng.integers(0,N,size=int(np.ceil(N/block)))
        sample=((starts[:,None]+idx)%N).ravel()[:N]
        x,y=a[sample],b[sample]
        ca=np.expm1(np.log1p(x).sum()*252/N);cb=np.expm1(np.log1p(y).sum()*252/N)
        da=max_drawdown(x);db=max_drawdown(y)
        d_cagr.append(cb-ca);d_dd.append(db-da);both+=int(cb>ca and db>da)
    return {'iterations':n,'block_sessions':block,'paired_days':N,'seed':seed,
            'fraction_candidate_higher_cagr':float(np.mean(np.array(d_cagr)>0)),
            'fraction_candidate_smaller_drawdown':float(np.mean(np.array(d_dd)>0)),
            'fraction_both':both/n,'cagr_delta_percentiles_2_5_50_97_5':np.quantile(d_cagr,[.025,.5,.975]).tolist(),
            'drawdown_delta_percentiles_2_5_50_97_5':np.quantile(d_dd,[.025,.5,.975]).tolist()}

def metrics(res, trades, start, end):
    m=rb.window_metrics(res['net_returns'],start,end)
    w=res['executed_weights'].loc[start:end]
    dur=(m['end']-m['start']).days/365.25
    selected=trades[(pd.to_datetime(trades.Entry_Date)>=pd.Timestamp(start)) &
                    (pd.to_datetime(trades.Entry_Date)<=pd.Timestamp(end))]
    return {'cagr':float(m['cagr']),'max_drawdown':float(m['max_drawdown']),'sharpe':float(m['sharpe']),
            'turnover_per_year':float(res['turnover'].loc[start:end].sum()/dur),
            'mean_exposure':float(w.sum(axis=1).mean()),'max_positions':int((w>1e-6).sum(axis=1).max()),
            'trades_entered':len(selected),'mean_hold_days':float(selected.Holding_Days.mean()) if len(selected) else None,
            'median_hold_days':float(selected.Holding_Days.median()) if len(selected) else None}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    paths=[ROOT/'csm_value/csm_value_strategy.py',ROOT/'csm_value/fundamentals_loader.py',
           ROOT/'csm_value/run_csm_value_backtest.py',ROOT/'Old_live_strategies/csm_absolute.py',
           ROOT/'Old_live_strategies/run_csm_absolute.py']
    manifest={'candidate':'value_growth_pullback','cutoff':END,'code_sha256':{str(p.relative_to(ROOT)):sha(p) for p in paths},
              'scenarios':list(SCENARIOS),'data_sources':['fundamentals','upstox_data_folder/ohlcv_data','csm_value/data/nse_monthly_prices.csv'],
              'warning':'Same 2019–2024 data used to choose the candidate; no genuinely independent market holdout.'}
    (OUT/'frozen_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    tmp,results,data=live.make_inputs()
    all_results={};reference_returns={}
    try:
        for mode in MODES:
            s=live.core.make_strategy(data,results,live.core.CUTOFF)
            if mode!='value':
                s.ranking_mode=mode;s.components=('EP','PROFIT_GROWTH','PULLBACK');s.calculate_factors()
            original=s.factors.copy();gate=signal_absolute(s).reindex_like(original).fillna(False)
            for scenario in SCENARIOS:
                s.factors=original.where(gate) if scenario=='absolute_signal_gate' else original.copy()
                s.use_liquid_mf=True;s.liquid_mf_annual_rate=0.0 if scenario=='zero_cash' else .065
                s.hard_stop_from_entry=.08 if scenario=='tighter_close_stops' else .15
                s.hard_stop_from_peak=.12 if scenario=='tighter_close_stops' else .20
                s.get_positions()
                res=rb.backtest_event_driven(s,initial_capital=100000,
                     transaction_cost=.006 if scenario=='double_cost' else .003,risk_free_rate=0.)
                trades=rb.get_trade_log(s).reset_index(drop=True)
                row={'mode':mode,'scenario':scenario,'windows':{k:metrics(res,trades,*v) for k,v in WINDOWS.items()}}
                all_results[f'{mode}:{scenario}']=row
                if scenario=='reference':reference_returns[mode]=res['net_returns'].loc[START:END].copy()
                print('RESULT',json.dumps(row),flush=True)
        paired=pd.concat(reference_returns,axis=1).dropna().loc[START:END]
        boot={name:bootstrap(paired.loc[a:b,'value'],paired.loc[a:b,'value_growth_pullback']) for name,(a,b) in WINDOWS.items()}
        paired.to_csv(OUT/'paired_daily_returns.csv',index_label='date')
        out={'manifest':manifest,'results':all_results,'paired_return_bootstrap':boot}
        (OUT/'robustness.json').write_text(json.dumps(out,indent=2)+'\n')
        print('BOOTSTRAP',json.dumps(boot),flush=True)
        print('COMPLETED',flush=True)
    finally:tmp.cleanup()

if __name__=='__main__':main()

"""Compare fundamentals-led rankings with selected live-strategy signals.

Research only. Inputs and results are truncated to 2024; execution mechanics
and the user-requested zero exit-day weight are shared between all candidates.
"""
import gc
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'research'/'csm_value_ohlcv_2024'))
_core_spec=importlib.util.spec_from_file_location('csm_value_ohlcv_2024_study',ROOT/'research'/'csm_value_ohlcv_2024'/'study.py')
core=importlib.util.module_from_spec(_core_spec)
_core_spec.loader.exec_module(core)
import fundamentals_loader as fl
import run_csm_value_backtest as rb

CANDIDATES=('value','value_a3','value_q5','value_elendel','value_zenith',
            'value_quad','value_earnings_quality')
BENCHMARKS=('ohlcv_elendel_common','ohlcv_elendel_universe')

def calc_signals(s):
    p=s.prices.reindex(columns=s.factors.columns)
    pff=p.ffill(); h=s.highs.reindex(columns=p.columns).ffill()
    benchmark=s.benchmark.reindex(p.index).ffill()
    rs=pff.div(benchmark,axis=0)
    a3=rs/rs.rolling(252,min_periods=200).max()
    sma=pff.rolling(50,min_periods=40).mean()
    above=(pff>sma).where(pff.notna() & sma.notna()).astype(float)
    q5=above.rolling(126,min_periods=100).mean()
    q5_zen=above.rolling(189,min_periods=150).mean()
    a1=pff/h.rolling(252,min_periods=200).max()
    labels=s.factors.index
    sessions=pd.Series(p.index,index=p.index).resample('ME').last().reindex(labels)
    mask=sessions.notna(); dates=pd.DatetimeIndex(sessions[mask].values); labs=labels[mask]
    def sample(x):return x.reindex(dates).set_axis(labs).reindex(labels)
    monthly=p.resample('ME').last();ret=monthly.pct_change(fill_method=None)
    legs=[]
    for n in (6,12):
        mom=monthly.shift(1)/monthly.shift(n+1)-1
        vol=(ret.rolling(n).std().shift(1)*np.sqrt(12)).replace(0,np.nan)
        legs.append((mom/vol).clip(-5,5))
    quad=(legs[0]+legs[1])/2
    abs_mom=monthly.shift(1)/monthly.shift(13)-1
    def fundamental(field):
        return fl.monthly_frame(s._results_in,field,dates,p.columns,max_age=s.results_max_age_days).set_axis(labs).reindex(labels)
    oneoff=fundamental('oneoff_share')
    return {'a3':sample(a3),'q5':sample(q5),'a1':sample(a1),'q5_zen':sample(q5_zen),
            'quad':quad.reindex(labels),'absolute':abs_mom.reindex(labels),
            'oneoff':oneoff,'growth':fundamental('sg_np')}

def cross_rank(x,eligible):
    return x.where(eligible).rank(axis=1,pct=True,method='average')

def rank_value(base,signals,name):
    if name=='value':return base.copy()
    eligible=base.notna()
    if name=='value_earnings_quality':return base.where(signals['oneoff']<=.5)
    v=cross_rank(base,eligible)
    if name=='value_a3': f=cross_rank(signals['a3'],eligible)
    elif name=='value_q5': f=cross_rank(signals['q5'],eligible)
    elif name=='value_elendel': f=(cross_rank(signals['a3'],eligible)+cross_rank(signals['q5'],eligible))/2
    elif name=='value_zenith':f=(cross_rank(signals['a1'],eligible)+cross_rank(signals['q5_zen'],eligible))/2
    elif name=='value_quad':f=cross_rank(signals['quad'],eligible)
    else:raise ValueError(name)
    return (.75*v+.25*f.fillna(.5)).where(eligible)

def rank_technical(eligible,signals):
    def z(x):
        y=x.where(eligible)
        return y.sub(y.mean(axis=1),axis=0).div(y.std(axis=1),axis=0)
    return z(signals['a3'])+z(signals['q5'])

def evaluate(s,base,base_momentum,signals,name,start,end):
    s.momentum_returns=base_momentum.copy()
    if name in BENCHMARKS:
        eligible=base.notna() if name=='ohlcv_elendel_common' else base_momentum.notna().reindex_like(base).fillna(False)
        s.factors=rank_technical(eligible,signals)
        s.momentum_returns=signals['absolute'].where(eligible)
    else:s.factors=rank_value(base,signals,name)
    s.get_positions()
    result=rb.backtest_event_driven(s,initial_capital=100000,transaction_cost=.003,risk_free_rate=0.)
    met=rb.window_metrics(result['net_returns'],start,end)
    if met is None or met['max_drawdown']>=0:raise ValueError(f'Invalid metrics: {name}')
    w=result['executed_weights'].loc[start:end]
    years=(met['end']-met['start']).days/365.25
    years_data={}
    for year in range(pd.Timestamp(start).year,pd.Timestamp(end).year+1):
        r=result['net_returns'].loc[f'{year}-01-01':f'{year}-12-31']
        r=r.loc[max(pd.Timestamp(start),r.index.min()):min(pd.Timestamp(end),r.index.max())] if len(r) else r
        if len(r):years_data[str(year)]=float((1+r).prod()-1)
    return {'candidate':name,'cagr':float(met['cagr']),'max_drawdown':float(met['max_drawdown']),
            'calmar':float(met['cagr']/abs(met['max_drawdown'])),'sharpe':float(met['sharpe']),
            'annual_turnover':float(result['turnover'].loc[start:end].sum()/years),
            'mean_exposure':float(w.sum(axis=1).mean()),'max_positions':int((w>1e-6).sum(axis=1).max()),
            'annual_returns':years_data}

def make_inputs():
    tmp=tempfile.TemporaryDirectory(prefix='csm_live_2024_')
    staged_symbols=core.stage_fundamentals(Path(tmp.name))
    results=fl.load_results(symbols=staged_symbols,directory=tmp.name)
    # The normal runner builds its equal-weight market benchmark from every
    # OHLCV symbol with a fundamentals JSON, even if that JSON has no eligible
    # quarterly result yet. Match that universe while keeping every input fact
    # filed and dated before 2025. Membership still has survivorship bias.
    symbols={p.stem for folder in (ROOT/'fundamentals',ROOT/'fundamentals'/'sme') for p in folder.glob('*.json')}
    print('RUNNER_UNIVERSE_FILES',len(symbols),'PRE2025_FACT_SYMBOLS',len(staged_symbols),flush=True)
    data=[p.loc['2001-01-01':core.CUTOFF] for p in rb.load_data(rb.data_folder_path,symbols=symbols)]
    data.append(rb.load_nse_monthly_prices(symbols=symbols).loc['2001-01-01':core.CUTOFF])
    assert (results.filed<=core.CUTOFF).all() and (results.period_end<=core.CUTOFF).all()
    assert all(p.index.max()<=core.CUTOFF for p in data)
    return tmp,results,data

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    tmp,results,data=make_inputs()
    try:
        s=core.make_strategy(data,results,core.IS_END);base=s.factors.copy();mom=s.momentum_returns.copy();signals=calc_signals(s)
        train=[]
        for name in (*CANDIDATES,*BENCHMARKS):
            row=evaluate(s,base,mom,signals,name,core.IS_START,str(core.IS_END.date()))
            train.append(row);print('IS_RESULT',json.dumps(row),flush=True)
        winner=max((r for r in train if r['candidate'] in CANDIDATES),key=lambda r:(r['calmar'],r['sharpe'],r['candidate']=='value'))['candidate']
        frozen={'cutoff':str(core.CUTOFF.date()),'development_start':core.IS_START,'development_end':str(core.IS_END.date()),
                'selection':'highest development Calmar, then Sharpe, then value baseline',
                'candidates':list(CANDIDATES),'benchmarks':list(BENCHMARKS),'selected':winner,'development':train,
                'warning':'2022–2024 and strategy ideas have been researched before; no pristine holdout.'}
        (OUT/'frozen_selection.json').write_text(json.dumps(frozen,indent=2)+'\n')
        print('FROZEN',winner,flush=True)
        del s,base,mom,signals;gc.collect()
        s=core.make_strategy(data,results,core.CUTOFF);base=s.factors.copy();mom=s.momentum_returns.copy();signals=calc_signals(s)
        comparison=[]
        for name in dict.fromkeys(('value',winner,*BENCHMARKS)):
            row=evaluate(s,base,mom,signals,name,core.TEST_START,str(core.CUTOFF.date()))
            comparison.append(row);print('COMPARISON_RESULT',json.dumps(row),flush=True)
        out={**frozen,'previously_examined_2022_2024':comparison}
        (OUT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
        print('COMPLETED',flush=True)
    finally:tmp.cleanup()

if __name__=='__main__':main()

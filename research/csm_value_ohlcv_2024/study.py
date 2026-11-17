"""Pre-specified OHLCV additions to CSM Value, using only pre-2025 observations.

IS selection is performed before the previously examined 2022–24 comparison.
This script is research-only and does not change the production strategy.
"""
import contextlib
import gc
import json
import os
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'csm_value'))
import fundamentals_loader as fl
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue

CUTOFF=pd.Timestamp('2024-12-31')
IS_END=pd.Timestamp('2021-12-31')
IS_START='2019-06-03'
TEST_START='2022-01-03'
CANDIDATES=('baseline','momentum_12_1','momentum_6_1','near_52w_high','low_vol_63','above_200d')

def stage_fundamentals(target):
    """Only supply individual quarterly facts filed and ended by the cutoff."""
    symbols=set()
    for folder in (ROOT/'fundamentals',ROOT/'fundamentals'/'sme'):
        for path in sorted(folder.glob('*.json')):
            doc=json.loads(path.read_text());years={}
            for fy,node in (doc.get('fiscal_years') or {}).items():
                quarters={}
                for q,blocks in (node.get('quarters') or {}).items():
                    keep={}
                    for basis in ('standalone','consolidated'):
                        b=blocks.get(basis)
                        if not b:continue
                        filed=fl._parse_filed(b.get('filed_date'))
                        end=(b.get('period') or {}).get('end')
                        if filed is None or not end:continue
                        try: pe=pd.Timestamp(end[:10])
                        except (ValueError,TypeError):continue
                        if pd.Timestamp(filed).normalize()<=CUTOFF and pe<=CUTOFF:
                            keep[basis]={'filed_date':b['filed_date'],'period':b['period'],
                                         'income_statement':b.get('income_statement') or {}}
                    if keep:quarters[q]=keep
                if quarters:years[fy]={'quarters':quarters}
            if years:
                (target/path.name).write_text(json.dumps({'fiscal_years':years}))
                symbols.add(path.stem)
    return symbols

def load_ohlcv(symbols):
    folder=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
    panels={k:[] for k in ('close','volume','high','low','open')}
    for path in sorted(folder.glob('*.csv')):
        if path.stem not in symbols:continue
        try:
            d=pd.read_csv(path,usecols=lambda x:x in {'datetime',*panels},parse_dates=['datetime'])
            d=d[(d.datetime>='2017-01-01') & (d.datetime<=CUTOFF)].drop_duplicates('datetime',keep='last').set_index('datetime')
            for col in panels:
                if col in d:
                    s=d[col].rename(path.stem)
                    if col!='volume':s=s.mask(s<=0)
                    panels[col].append(s)
        except (OSError,ValueError,KeyError) as exc:
            raise RuntimeError(f'{path}: {exc}') from exc
    return tuple(pd.concat(panels[col],axis=1).sort_index() for col in ('close','volume','high','low','open'))

def monthly_at_session(panel, sessions, labels):
    return panel.reindex(sessions).set_axis(labels)

def overlays(s):
    prices=s.prices.reindex(columns=s.factors.columns)
    labels=s.factors.index
    session_series=pd.Series(prices.index,index=prices.index).resample('ME').last().reindex(labels)
    valid=session_series.notna();dates=pd.DatetimeIndex(session_series[valid].values);labs=labels[valid]
    def sample(x):return monthly_at_session(x,dates,labs).reindex(labels)
    # Use daily sessions and no stale-price forward fill in candidate inputs.
    mom12=sample(prices.shift(21)/prices.shift(252)-1)
    mom6=sample(prices.shift(21)/prices.shift(126)-1)
    high52=sample(prices/prices.rolling(252,min_periods=200).max())
    vol63=sample(prices.pct_change(fill_method=None).rolling(63,min_periods=50).std())
    trend200=sample(prices/prices.rolling(200,min_periods=180).mean())
    return {'momentum_12_1':mom12,'momentum_6_1':mom6,'near_52w_high':high52,
            'low_vol_63':-vol63,'above_200d':trend200}

def candidate_factors(base, signals, name):
    if name=='baseline':return base.copy()
    eligible=base.notna()
    if name=='above_200d':return base.where(signals[name]>1.0)
    # Value determines 75% of percentile score. Missing secondary signal is
    # neutral; it does not silently discard an otherwise valid value name.
    value=base.rank(axis=1,pct=True,method='average')
    secondary=signals[name].where(eligible).rank(axis=1,pct=True,method='average').fillna(.5)
    return (.75*value+.25*secondary).where(eligible)

def make_strategy(data,results,end):
    prices,volumes,highs,lows,opens,valuations=data
    def until(f):return f.loc[:end]
    p,v,h,l,o,nse=map(until,(prices,volumes,highs,lows,opens,valuations))
    p,h,l,o=rb.mask_corporate_actions(p,h,l,o)
    known=results[results.filed<=end].copy()
    benchmark=rb.build_benchmark(p)
    # Freeze the previous research baseline; production defaults now target
    # longer holdings and higher exposure.
    s=CSMValue(prices_df=p,volumes_df=v,highs_df=h,lows_df=l,opens_df=o,
               valuation_prices_df=nse,benchmark_series=benchmark,results_df=known,top_n=10,
               buffer_ratio=.2, risk_pct_per_trade=.01, max_weight_per_stock=.05,
               hard_stop_from_peak=.20, leverage_bear=.8, vol_target=.15,
               rebalance_exit_buffer_months=1, fill_weight_caps=False)
    s.calculate_factors()
    return s

def evaluate(s,base,signals,name,start,end):
    s.factors=candidate_factors(base,signals,name)
    s.get_positions()
    res=rb.backtest_event_driven(s,initial_capital=100000,transaction_cost=.003,risk_free_rate=0.)
    m=rb.window_metrics(res['net_returns'],start,end)
    if not m:raise ValueError(f'no window metrics for {name}')
    w=res['executed_weights'].loc[start:end]
    days=(m['end']-m['start']).days/365.25
    return {'candidate':name,'start':str(m['start'].date()),'end':str(m['end'].date()),
            'cagr':float(m['cagr']),'drawdown':float(m['max_drawdown']),
            'sharpe':float(m['sharpe']),'calmar':float(m['cagr']/abs(m['max_drawdown'])),
            'annual_turnover':float(res['turnover'].loc[start:end].sum()/days),
            'exposure':float(w.sum(axis=1).mean()),'max_positions':int((w>1e-6).sum(axis=1).max())}

def main():
    OUT.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='csm_value_pre2025_') as tmp:
        symbols=stage_fundamentals(Path(tmp))
        print('PRE2025_UNIVERSE',len(symbols),flush=True)
        res=fl.load_results(symbols=symbols,directory=tmp)
        assert (res.filed<=CUTOFF).all() and (res.period_end<=CUTOFF).all()
        data=list(load_ohlcv(symbols));nse=rb.load_nse_monthly_prices(symbols=symbols).loc[:CUTOFF];data.append(nse)
        assert all(d.index.max()<=CUTOFF for d in data)
        print('DATA_LOADED',res.shape,[x.shape for x in data],flush=True)
        s=make_strategy(data,res,IS_END);base=s.factors.copy();sigs=overlays(s)
        train=[]
        for name in CANDIDATES:
            print('IS_START',name,flush=True)
            row=evaluate(s,base,sigs,name,IS_START,str(IS_END.date()));train.append(row)
            print('IS_RESULT',json.dumps(row),flush=True)
        winner=max(train,key=lambda x:(x['calmar'],x['sharpe'],x['candidate']=='baseline'))['candidate']
        frozen={'cutoff':str(CUTOFF.date()),'candidates':list(CANDIDATES),
                'selection_rule':'maximum 2019-06-03 to 2021-12-31 Calmar, then Sharpe, then baseline',
                'selected':winner,'is_results':train,'warning':'2022–24 has been examined in prior research; not a blind holdout.'}
        (OUT/'frozen_selection.json').write_text(json.dumps(frozen,indent=2)+'\n')
        print('FROZEN_SELECTION',winner,flush=True)
        del s,base,sigs;gc.collect()
        s=make_strategy(data,res,CUTOFF);base=s.factors.copy();sigs=overlays(s)
        test=[]
        for name in dict.fromkeys(('baseline',winner)):
            print('HISTORICAL_COMPARISON_START',name,flush=True)
            row=evaluate(s,base,sigs,name,TEST_START,str(CUTOFF.date()));test.append(row)
            print('HISTORICAL_COMPARISON_RESULT',json.dumps(row),flush=True)
        out={**frozen,'previously_examined_2022_2024':test}
        (OUT/'results.json').write_text(json.dumps(out,indent=2)+'\n')
        print('COMPLETED',flush=True)

if __name__=='__main__':main()

"""V3 actual strategy and share-engine sweep; data read only, flat-start windows."""
import os,sys,copy,time,gc
from pathlib import Path
import numpy as np,pandas as pd
OUT=Path(__file__).resolve().parent; ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
import csm_stock_backtest_v3 as bt
from csm_signal_filters import compute_filter_masks
window,mode=sys.argv[1:3]
P,V,H,L,O=bt.load_data(bt.DATA_FOLDER)
windows={'early':('2005-01-01','2014-12-31'),'late':('2015-01-01','2025-12-31'),'full':('2002-01-01','2025-12-31'),'playbook_early':('2001-01-01','2012-12-31'),'playbook_late':('2013-01-01',str(P.index.max().date()))}
start,end=windows[window];a=pd.Timestamp(start);b=pd.Timestamp(end);p=P.loc[a-pd.Timedelta(days=450):b];v=V.reindex_like(p);h=H.reindex_like(p);l=L.reindex_like(p);o=O.reindex_like(p);del P,V,H,L,O
base=bt.CrossSectionalMomentum(p,v,h,l,o,lookback_months=bt.LOOKBACK_MONTHS,lag_months=bt.LAG_MONTHS,top_n=bt.TOP_N,min_price=bt.MIN_PRICE,universe_top_n=2000,corp_action_filter=bt.USE_CORP_ACTION_FILTER,ca_max_drop=bt.CA_MAX_DROP,ca_max_gain=bt.CA_MAX_GAIN,max_circuit_days=bt.MAX_CIRCUIT_DAYS,buffer_ratio=bt.BUFFER_RATIO,atr_period=bt.ATR_PERIOD,hard_stop_from_entry=bt.HARD_STOP_FROM_ENTRY,stop_slippage_pct=bt.STOP_SLIPPAGE_PCT,vol_stop_k=bt.VOL_STOP_K,vol_stop_min_pct=bt.VOL_STOP_MIN_PCT,vol_stop_max_pct=bt.VOL_STOP_MAX_PCT,stop_cooldown_days=bt.STOP_COOLDOWN_DAYS,min_hold_days=bt.MIN_HOLD_DAYS,rebalance_months=bt.REBALANCE_MONTHS,rebalance_min_fill_frac=bt.REBALANCE_MIN_FILL_FRAC,rank_exit_dynamic=bt.RANK_EXIT_DYNAMIC,rank_exit_drop_frac=bt.RANK_EXIT_DROP_FRAC,rank_exit_floor_frac=bt.RANK_EXIT_FLOOR_FRAC,signal_filters=bt.SIGNAL_FILTERS)
base.calculate_factors();p=base.prices;v=base.volumes;h=base.highs;l=base.lows;del o
m=p.resample('ME').last();mr=m.pct_change(fill_method=None);elig=base.filter_universe(m,p);dvol=(p*v).rolling(63,min_periods=21).median().shift(1).resample('ME').last().reindex(m.index);ranks=dvol.rank(axis=1,ascending=False,method='min');del dvol
filters=compute_filter_masks(p,v,h,l,bt.SIGNAL_FILTERS); gates={k:z.shift(1,fill_value=False).resample('ME').last().reindex(index=m.index,columns=m.columns).fillna(False).astype(bool) for k,z in filters.items()};del filters
fac={}
def factor(n):
 if n not in fac:
  S=max(1,n//2);rl=m.shift(1)/m.shift(1+n)-1;rs=m.shift(1)/m.shift(1+S)-1
  vl=(mr.rolling(n).std().shift(1)*np.sqrt(12)).replace(0,np.nan);vs=(mr.rolling(S).std().shift(1)*np.sqrt(12)).replace(0,np.nan)
  fac[n]=((rl/vl).clip(-5,5).add((rs/vs).clip(-5,5))/2,rl)
 return fac[n]
cells=[('baseline',{})]
if mode=='universe':
 cells += [(f'top_{n}',{'band':(0,n)}) for n in [100,250,500,750,1000,1500]]
 cells += [(f'band_{x}_{y}',{'band':(x,y)}) for x,y in [(0,500),(500,1000),(1000,1500),(1000,2000)]]
if mode=='sweep':
 cells += [(f'lookback_{n}',{'lookback':n}) for n in [7,10,12,14,17]]
 cells += [(f'rebalance_{n}',{'rebalance_months':n}) for n in [1,2,3]]
 cells += [(f'positions_{n}',{'top_n':n}) for n in [9,12,15,18,21]]
 cells += [(f'stop_{n:.2f}',{'hard_stop_from_entry':n}) for n in [.09,.12,.15,.18,.21]]
 cells += [(f'high52_{n:.2f}',{'high52_level':n}) for n in [.51,.68,.85,.95,1.00]]
 cells += [('cost_0.006',{'cost':.006}),('cost_0.009',{'cost':.009})]
 cells += [('ablate_rank_exit',{'rank_exit_dynamic':False}),('ablate_vol_stop',{'vol_stop_min_pct':0.,'vol_stop_max_pct':0.}),('ablate_adx',{'drop_gate':'adx'}),('ablate_high52',{'drop_gate':'high52'}),('ablate_both_gates',{'drop_gate':'both'}),('ablate_positive_momentum',{'positive_off':True})]
if mode=='adx':
 cells += [(f'adx_{n}',{'adx_level':n}) for n in [12,16,20,24,28]]
if mode=='extra':
 cells += [('cost_0.006',{'cost':.006}),('cost_0.009',{'cost':.009}),('ablate_vol_stop',{'vol_stop_min_pct':0.,'vol_stop_max_pct':0.})]
# Precompute alternate high52 filters only if necessary; same implementation and lag.
hi_gates={}
if mode=='sweep':
 for n in [.51,.68,.95,1.00]:
  z=compute_filter_masks(p,v,h,l,{'high52':dict(enabled=True,min_pct=n)})['high52'];hi_gates[n]=z.shift(1,fill_value=False).resample('ME').last().reindex(index=m.index,columns=m.columns).fillna(False).astype(bool)
adx_gates={}
if mode=='adx':
 for n in [12,16,24,28]:
  z=compute_filter_masks(p,v,h,l,{'adx':dict(enabled=True,period=14,min_adx=n,require_di=True)})['adx'];adx_gates[n]=z.shift(1,fill_value=False).resample('ME').last().reindex(index=m.index,columns=m.columns).fillna(False).astype(bool)
out=OUT/f'{window}_{mode}_cells.csv';years=OUT/f'{window}_{mode}_yearly.csv'
for file in [out,years]:
 if file.exists():file.unlink()
def dd_avg(curve):
 d=curve/curve.cummax()-1;v=d.groupby(d.eq(0).cumsum()).min();v=v[v<-.02];return -v.mean() if len(v) else 0.
for name,cfg in cells:
 tic=time.time();print('CELL',window,name,flush=True);s=copy.copy(base);x,y=cfg.get('band',(0,1000));f,ret=factor(cfg.get('lookback',12));mask=elig&(ranks>x)&(ranks<=y)
 for k in gates:
  if cfg.get('drop_gate') not in (k,'both'):
   mask &= (hi_gates[cfg['high52_level']] if k=='high52' and cfg.get('high52_level') in hi_gates else adx_gates[cfg['adx_level']] if k=='adx' and cfg.get('adx_level') in adx_gates else gates[k])
 anchor=a-pd.offsets.MonthEnd(1);s.factors=f.where(mask).dropna(how='all').loc[anchor:];s.momentum_returns=ret.where(mask).dropna(how='all').loc[anchor:]
 if cfg.get('positive_off'):s.momentum_returns=s.momentum_returns.where(s.momentum_returns.isna(),1.)
 for key in ('rebalance_months','top_n','hard_stop_from_entry','rank_exit_dynamic','vol_stop_min_pct','vol_stop_max_pct'):
  if key in cfg:setattr(s,key,cfg[key])
 s.get_positions();bt.COST_ONE_WAY=cfg.get('cost',.003);run=bt.run_backtest(s);bt.COST_ONE_WAY=.003
 assert (run['expo'].loc[run['expo'].index<a].abs()<1e-12).all()
 if len(run['trades_df']):assert (run['trades_df'].Entry_Date>=a).all()
 res=bt.slice_to_report_window(run,start,end,bt.INITIAL_CAPITAL);met=bt.metrics(res,0);stats=bt.trade_pnl_stats(res['trades_df']);eq=res['equity_curve'];r=res['net_returns'];trail=eq.resample('ME').last().pct_change(12,fill_method=None).dropna()
 row={'window':window,'cell':name,'start':start,'end':end,'cagr_pct':met['CAGR'],'sharpe':met['Sharpe0'],'sortino':met['Sortino'],'calmar':met['Calmar'],'maxdd_pct':met['MaxDD'],'vol_pct':met['Vol'],'turnover_pct':met['Turnover'],'cost_drag_pct':met['CostDrag'],'stability':trail.std(),'average_dd_pct':100*dd_avg(eq),'exposure_pct':met['AvgExpo'],'avg_hold':met['AvgHold'],'trade_win_pct':stats['win_rate'],'profit_factor':stats['profit_factor'],'payoff':stats['payoff_ratio'],'hold_days':stats['avg_holding_days'],'trades':stats['n_trades'],'first_entry':str(res['trades_df'].Entry_Date.min().date()) if len(res['trades_df']) else '', 'events':len(s.corp_action_events),'masked_bars':s.corp_action_bars,'seconds':time.time()-tic}
 pd.DataFrame([row]).to_csv(out,mode='a',header=not out.exists(),index=False);print('RESULT',row,flush=True)
 yr=[]
 for year,g in r.groupby(r.index.year):
  curve=(1+g).cumprod();curve=pd.concat([pd.Series([1.],index=[g.index[0]-pd.Timedelta(days=1)]),curve]);yr.append({'window':window,'cell':name,'year':year,'return_pct':100*((1+g).prod()-1),'sharpe':g.mean()/g.std()*np.sqrt(252) if g.std()>0 else np.nan,'maxdd_pct':100*(curve/curve.cummax()-1).min()})
 pd.DataFrame(yr).to_csv(years,mode='a',header=not years.exists(),index=False)
 if mode=='universe':r.to_csv(OUT/f'{window}_universe_{name}_returns.csv')
 if name=='baseline':
  tag=f'{window}_{mode}';eq.to_csv(OUT/f'{tag}_equity.csv');r.to_csv(OUT/f'{tag}_returns.csv');res['trades_df'].to_csv(OUT/f'{tag}_trades.csv',index=False);s.factors.notna().to_parquet(OUT/f'{tag}_universe.parquet');s.positions.to_parquet(OUT/f'{tag}_positions.parquet');run['turnover'].to_csv(OUT/f'{tag}_turnover.csv');s.corp_action_events.to_csv(OUT/f'{tag}_events.csv',index=False)
 del s,run,res;gc.collect()
print('DONE',window,mode,flush=True)

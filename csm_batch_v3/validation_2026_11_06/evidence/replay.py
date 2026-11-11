"""Replay exact event engine on raw read-only source. Usage: python backtest.py early|late|full|parity [sweep|baseline]."""
import ast, copy, gc, os, sys, time, warnings
from pathlib import Path
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
from csm_stock_strategy_v3 import CrossSectionalMomentum,load_data
warnings.filterwarnings('ignore',message='All-NaN slice encountered');warnings.filterwarnings('ignore',message='Mean of empty slice');warnings.filterwarnings('ignore',category=RuntimeWarning)
window=sys.argv[1];mode=sys.argv[2] if len(sys.argv)>2 else 'sweep'
source=ast.parse((ROOT/'csm_stock_backtest_v3.py').read_text()); want={'_trade_row','run_backtest','load_secondary_etf','apply_etf_sweep','build_equity_curve','slice_to_report_window','metrics','trade_pnl_stats'}
ns={'np':np,'pd':pd,'os':os,'COST_ONE_WAY':.003,'EXIT_REASONS':['REBAL_EXIT','RANK_EXIT','ATR_STOP_HIT','HARD_STOP_HIT','PEAK_STOP_HIT','VOL_STOP_HIT','FORCE_EXIT','CRASH_GUARD','END_OF_PERIOD']}
exec(compile(ast.Module(body=[n for n in source.body if isinstance(n,ast.FunctionDef) and n.name in want],type_ignores=[]),str(ROOT/'csm_stock_backtest_v3.py'),'exec'),ns)
p,v,h,l,o=load_data('/private/tmp/csm_batch_v3_validation_snapshot/ohlcv');last=p.index.max(); last_full_year=last.year-1 if last.month<12 or last.day<31 else last.year
windows={'early':('2005-01-01','2014-12-31'),'late':('2015-01-01','2025-12-31'),'full':('2002-01-01','2025-12-31'),'playbook_early':('2001-01-01','2012-12-31'),'playbook_late':('2013-01-01',str(last.date())),'parity':('2005-01-01','2015-12-31')}
start,end=windows[window];start_ts=pd.Timestamp(start);end_ts=pd.Timestamp(end);actual_start=p.index[p.index.searchsorted(start_ts-pd.Timedelta(days=450))]
p=p.loc[actual_start:end_ts];v=v.reindex(index=p.index,columns=p.columns);h=h.reindex(index=p.index,columns=p.columns);l=l.reindex(index=p.index,columns=p.columns);o=o.reindex(index=p.index,columns=p.columns)
# Predetermined data-quality sensitivity only: source CSVs are never altered.
exclude=os.environ.get('EXCLUDE_TICKERS','').split(',')
exclude=[c for c in exclude if c and c in p.columns]
if exclude:
 p=p.drop(columns=exclude);v=v.drop(columns=exclude);h=h.drop(columns=exclude);l=l.drop(columns=exclude);o=o.drop(columns=exclude)
 print('EXCLUDED TICKERS FOR SENSITIVITY ONLY:',exclude,flush=True)
bench=(1+p.pct_change(fill_method=None).clip(-.5,.5).mean(axis=1,skipna=True).fillna(0)).cumprod()
print('WINDOW',window,'start',start,'end',end,'load',actual_start,'rows',len(p),flush=True)
base=CrossSectionalMomentum(prices_df=p,volumes_df=v,highs_df=h,lows_df=l,opens_df=o,benchmark_series=bench,lookback_months=12,lag_months=1,top_n=30,min_price=10,universe_top_n=2000,max_circuit_days=5,buffer_ratio=.2,atr_period=14,atr_multiplier=3,atr_multiplier_high_vol=2,hard_stop_from_entry=.15,hard_stop_from_peak=.2,stop_slippage_pct=.003,use_trailing_stop=False,use_vol_scaled_stop=True,vol_stop_k=4,vol_stop_min_pct=.1,vol_stop_max_pct=.25,stop_cooldown_days=20,min_hold_days=5,use_crash_guard=False,crash_guard_cooldown=10,corr_guard_threshold=.8,vol_target=.2,use_bear_regime_exposure=True,bear_regime_sma_days=150,bear_regime_return_days=63,bear_regime_return_cutoff=-.1,bear_regime_scale=.6,severe_bear_regime_scale=.3,max_weight_per_stock=.05,rebalance_months=2,rebalance_min_fill_frac=.5,rank_exit_dynamic=True,rank_exit_drop_frac=.34,rank_exit_floor_frac=.67)
base.calculate_factors(); monthly=p.resample('ME').last(); eligibility=base.filter_universe(monthly,p);mr=monthly.pct_change(fill_method=None)
dvol=(p*v).rolling(63,min_periods=21).median().shift(1).resample('ME').last().reindex(monthly.index);ranks=dvol.rank(axis=1,ascending=False,method='min');del dvol
factors={}
def factor(L):
 if L not in factors:
  S=max(1,L//2);rl=monthly.shift(1)/monthly.shift(1+L)-1;rs=monthly.shift(1)/monthly.shift(1+S)-1
  vl=(mr.rolling(L).std().shift(1)*np.sqrt(12)).replace(0,np.nan);vs=(mr.rolling(S).std().shift(1)*np.sqrt(12)).replace(0,np.nan)
  factors[L]=((rl/vl).clip(-5,5).add((rs/vs).clip(-5,5))/2,rl)
 return factors[L]
cells=[('baseline',{})]
if mode in ('sweep','universe','probe'):
 cells += [(f'top_{n}',{'band':(0,n)}) for n in [100,250,500,750,1000,1500]]
 cells += [(f'band_{a}_{b}',{'band':(a,b)}) for a,b in [(0,500),(500,1000),(1000,1500),(1000,2000)]]
 cells += [(f'lookback_{n}',{'lookback':n}) for n in [7,10,12,14,17]]
 cells += [(f'rebalance_{n}',{'rebalance_months':n}) for n in [1,2,3]]
 cells += [(f'positions_{n}',{'top_n':n}) for n in [18,24,30,36,42]]
 cells += [(f'stop_{n:.2f}',{'hard_stop_from_entry':n}) for n in [.09,.12,.15,.18,.21]]
 cells += [(f'regime_{n:.2f}',{'bear_regime_return_cutoff':n}) for n in [-.06,-.08,-.10,-.12,-.14]]
 cells += [('ablate_rank_exit',{'rank_exit_dynamic':False}),('ablate_vol_stop',{'use_vol_scaled_stop':False}),('ablate_bear_exposure',{'use_bear_regime_exposure':False}),('ablate_vol_target',{'vol_target':100.}),('ablate_corr_guard',{'corr_guard_threshold':100.}),('ablate_positive_momentum',{'positive_off':True})]
if mode=='universe':cells=[cell for cell in cells if cell[0]=='baseline' or cell[0].startswith(('top_','band_'))]
if mode=='probe':cells=[cell for cell in cells if cell[0] in os.environ.get('CELL_ONLY','').split(',')]
if mode=='sweep':cells=[cell for cell in cells if not cell[0].startswith(('top_','band_'))]
suffix='_no_TIL' if 'TIL' in exclude else ''
output=OUT/(f'{window}_{mode}_cells{suffix}.csv');completed=set()
if mode=='universe' and (OUT/f'{window}_cost_stress.csv').exists():(OUT/f'{window}_cost_stress.csv').unlink()
yearly_file=OUT/f'{window}_{mode}_yearly{suffix}.csv'
if os.environ.get('RESUME')=='1' and output.exists():completed=set(pd.read_csv(output).cell)
elif output.exists():output.unlink()
if os.environ.get('RESUME')!='1' and yearly_file.exists():yearly_file.unlink()
def dd_avg(eq):
 d=eq/eq.cummax()-1;episodes=d.groupby(d.eq(0).cumsum()).min();v=episodes[episodes<-.02];return float(-v.mean()) if len(v) else 0.
for label,cfg in cells:
 if label in completed:continue
 tic=time.time();print('CELL',window,label,flush=True)
 s=copy.copy(base);a,b=cfg.get('band',(0,1000));f,raw=factor(cfg.get('lookback',12));mask=eligibility&(ranks>a)&(ranks<=b)
 # Warm indicators on prior history, but initialize the selection state flat.
 # Start at the last calendar month-end before the report; no trades are allowed before start.
 anchor=start_ts-pd.offsets.MonthEnd(1)
 s.factors=f.where(mask).dropna(how='all').loc[anchor:];s.momentum_returns=raw.where(mask).dropna(how='all').loc[anchor:]
 if cfg.get('positive_off'):s.momentum_returns=s.momentum_returns.where(s.momentum_returns.isna(),1.)
 for k in ['rebalance_months','top_n','hard_stop_from_entry','bear_regime_return_cutoff','rank_exit_dynamic','use_vol_scaled_stop','use_bear_regime_exposure','vol_target','corr_guard_threshold']:
  if k in cfg:setattr(s,k,cfg[k])
 if 'bear_regime_return_cutoff' in cfg or 'use_bear_regime_exposure' in cfg:s._prepare_bear_regime_scale()
 s.get_positions();ns['csm']=s;run=ns['run_backtest'](s)
 warm=run['executed_weights'].loc[run['executed_weights'].index < start_ts]
 if (warm.abs().to_numpy()>1e-12).any():raise RuntimeError('A position was opened during the warmup window')
 if not run['trades_df'].empty and (run['trades_df']['Entry_Date'] < start_ts).any():raise RuntimeError('Pre-start trade found in a flat-start run')
 etf=ns['load_secondary_etf'](str(OUT),'GOLDBEES',p.index);etf['first']=max(etf['first'],start_ts);eq=ns['build_equity_curve'](run,100000,.003,0,etf=etf);res=ns['slice_to_report_window'](eq,run['trades_df'],start,end,100000)
 met=ns['metrics'](res,100000,0);trade=ns['trade_pnl_stats'](res['trades_df']);curve=res['equity_curve'];returns=res['net_returns'];trailing=curve.resample('ME').last().pct_change(12,fill_method=None).dropna()
 br=bench.pct_change(fill_method=None).reindex(returns.index).fillna(0);beta=returns.cov(br)/br.var() if br.var()>0 else np.nan
 row={'window':window,'cell':label,'start':start,'end':end,'load_start':str(actual_start.date()),'cagr_pct':met['CAGR'],'sharpe':met['Sharpe0'],'sortino':met['Sortino'],'calmar':met['Calmar'],'maxdd_pct':met['MaxDD'],'vol_pct':met['Vol'],'turnover_pct':met['Turnover'],'stability':trailing.std(),'average_dd_pct':100*dd_avg(curve),'beta':beta,'alpha_pct':100*(returns.mean()-beta*br.mean())*252,'etf_exposure_pct':met['AvgETFExpo'],'etf_cost_drag_pct':met['ETFCostDrag'],'etf_forced_untradable':eq['etf_forced_untradable'],'exposure_pct':met['AvgExpo'],'trade_win_pct':trade['win_rate'],'profit_factor_pct':trade['profit_factor'],'payoff':trade['payoff_ratio'],'hold_days':trade['avg_holding_days'],'trades':trade['n_trades'],'first_entry':str(res['trades_df']['Entry_Date'].min().date()) if not res['trades_df'].empty else '', 'seconds':time.time()-tic}
 pd.DataFrame([row]).to_csv(output,mode='a',header=not output.exists(),index=False);print('RESULT',row,flush=True)
 yearrows=[]
 for year,part in returns.groupby(returns.index.year):
  part=part.dropna(); yearly_curve=(1+part).cumprod(); yearly_curve=pd.concat([pd.Series([1.],index=[part.index[0]-pd.Timedelta(days=1)]),yearly_curve]); yearly_dd=(yearly_curve/yearly_curve.cummax()-1).min()
  yearrows.append({'window':window,'cell':label,'year':year,'return_pct':100*((1+part).prod()-1),'vol_pct':100*part.std()*np.sqrt(252),'sharpe':part.mean()/part.std()*np.sqrt(252) if part.std()>0 else np.nan,'maxdd_pct':100*yearly_dd,'n_days':len(part)})
 pd.DataFrame(yearrows).to_csv(yearly_file,mode='a',header=not yearly_file.exists(),index=False)
 if mode=='universe':
  for cs in [.003,.006,.009]:
   eqc=ns['build_equity_curve'](run,100000,cs,0,etf=etf);rc=ns['slice_to_report_window'](eqc,run['trades_df'],start,end,100000);mc=ns['metrics'](rc,100000,0);cf=OUT/f'{window}_cost_stress.csv';pd.DataFrame([{'window':window,'cell':label,'one_way_cost_pct':100*cs,'cagr_pct':mc['CAGR'],'sharpe':mc['Sharpe0'],'calmar':mc['Calmar'],'maxdd_pct':mc['MaxDD']}]).to_csv(cf,mode='a',header=not cf.exists(),index=False)
  returns.to_csv(OUT/f'{window}_universe_{label}_returns.csv')
  res['turnover'].to_csv(OUT/f'{window}_universe_{label}_turnover.csv')
 if label=='baseline' or mode=='probe':
  cash=ns['build_equity_curve'](run,100000,.003,0);cashr=ns['slice_to_report_window'](cash,run['trades_df'],start,end,100000);cashm=ns['metrics'](cashr,100000,0);pd.DataFrame([{'window':window,'cell':label,'cash_cagr':cashm['CAGR'],'cash_sharpe':cashm['Sharpe0'],'cash_calmar':cashm['Calmar'],'cash_maxdd':cashm['MaxDD'],'etf_cagr':met['CAGR'],'etf_sharpe':met['Sharpe0'],'etf_calmar':met['Calmar'],'etf_maxdd':met['MaxDD'],'etf_first_usable':str(etf['first'].date()),'etf_exposure_pct':met['AvgETFExpo'],'etf_cost_drag_pct':met['ETFCostDrag'],'forced_untradable':eq['etf_forced_untradable']}]).to_csv(OUT/f'{window}_{mode}_{label}_etf_comparison{suffix}.csv',index=False)
  tag=(f'{window}_{mode}_{label}' if mode=='probe' else f'{window}_{mode}')+suffix
  curve.to_csv(OUT/f'{tag}_equity.csv');returns.to_csv(OUT/f'{tag}_returns.csv');res['trades_df'].to_csv(OUT/f'{tag}_trades.csv',index=False);s.factors.notna().to_parquet(OUT/f'{tag}_universe.parquet');s.positions.to_parquet(OUT/f'{tag}_positions.parquet')
 del run,eq,res,s;gc.collect()
print('DONE',window,mode,flush=True)

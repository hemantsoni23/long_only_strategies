"""Causal regression for a scheduled open exit on a day with a later intraday stop breach."""
import ast,sys,json
from pathlib import Path
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent;ROOT=P.parents[1];sys.path.insert(0,str(ROOT));from csm_stock_strategy import CrossSectionalMomentum
source=ast.parse((ROOT/'csm_stock_backtest.py').read_text());names={'_trade_row','run_backtest'};ns={'np':np,'pd':pd,'COST_ONE_WAY':.003,'EXIT_REASONS':['REBAL_EXIT','RANK_EXIT','ATR_STOP_HIT','HARD_STOP_HIT','PEAK_STOP_HIT','VOL_STOP_HIT','FORCE_EXIT','CRASH_GUARD','END_OF_PERIOD']};exec(compile(ast.Module(body=[x for x in source.body if isinstance(x,ast.FunctionDef) and x.name in names],type_ignores=[]),str(ROOT/'csm_stock_backtest.py'),'exec'),ns)
def run(low_on_exit):
 idx=pd.bdate_range('2024-01-02',periods=5);df=lambda x:pd.DataFrame({'X':x},index=idx)
 p=df([100]*5);h=df([102]*5);lo=df([98,98,low_on_exit,98,98]);op=df([100]*5)
 s=CrossSectionalMomentum(p,p*1000,h,lo,op,benchmark_series=None,hard_stop_from_entry=.15,use_trailing_stop=False,use_vol_scaled_stop=False,use_crash_guard=False,use_bear_regime_exposure=False,min_hold_days=0,stop_cooldown_days=20,vol_target=1.0)
 s.positions=df([.5,0,.5,.5,.5]);s.rank_exit_mask=df([False]*5);s.atr=df([2]*5);s._high_vol_threshold_series=None;s._panic_threshold_series=None;s._prepare_stop_indicators(p.resample('ME').last())
 result=ns['run_backtest'](s);trade=result['trades_df'];first=trade.iloc[0]
 return {'exit_date':str(first.Exit_Date.date()),'reason':first.Exit_Reason,'exit_price':float(first.Exit_Price),'next_day_weight':float(result['executed_weights'].iloc[3,0])}
a=run(90);b=run(80);result={'scheduled_open':100,'same_signal_and_open':True,'no_later_breach':a,'later_low_breaches_stop':b,'test':'FAIL' if a!=b else 'PASS'}
(P/'synthetic_open_test.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2));assert result['test']=='FAIL' and a['reason']=='REBAL_EXIT' and b['reason']=='HARD_STOP_HIT' and a['next_day_weight']>0 and b['next_day_weight']==0

"""Deterministic tests against the unmodified v3 share engine."""
import json,sys
from pathlib import Path
import numpy as np,pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT))
import csm_stock_backtest_v3 as bt
from csm_stock_strategy_v3 import CrossSectionalMomentum

def run_stop(low):
 idx=pd.bdate_range('2024-01-02',periods=6);df=lambda x:pd.DataFrame({'X':x},index=idx)
 p=df([100]*6);high=df([102]*6);lo=df([98,98,low,98,98,98]);op=df([100]*6)
 s=CrossSectionalMomentum(p,p*1000,high,lo,op,hard_stop_from_entry=.15,min_hold_days=0,stop_cooldown_days=20,vol_stop_k=0,corp_action_filter=False)
 s.positions=df([.5,0,.5,.5,.5,.5]);s.rank_exit_mask=df([False]*6);s.atr=df([np.nan]*6);s._prepare_stop_indicators();out=bt.run_backtest(s);trade=out['trades_df'].iloc[0]
 return {'reason':trade.Exit_Reason,'exit_price':trade.Exit_Price,'holdings_next_day':int(out['nheld'].iloc[3])}

def run_mask(close):
 idx=pd.bdate_range('2024-01-02',periods=5);df=lambda x:pd.DataFrame({'X':x},index=idx)
 p=df([100,close,100,100,100]);op=df([90,100,100,100,100]);hi=df([105,max(close,105),105,105,105]);lo=df([95]*5)
 s=CrossSectionalMomentum(p,p*1000,hi,lo,op,corp_action_filter=True,min_hold_days=0)
 s._nullify_corporate_actions();s._prepare_stop_indicators();s.positions=df([.5]*5);s.rank_exit_mask=df([False]*5);s.atr=df([2]*5)
 out=bt.run_backtest(s);return {'event_count':len(s.corp_action_events),'open_used_on_day':float(s._opens_ff.iloc[1,0]),'entry_price':float(out['trades_df'].iloc[0].Entry_Price)}
def run_circuit(locked):
 idx=pd.bdate_range('2024-01-02',periods=5);df=lambda x:pd.DataFrame({'X':x},index=idx)
 p=df([100]*5);op=df([100]*5);hi=df([105,100 if locked else 105,105,105,105]);lo=df([95,100 if locked else 95,95,95,95])
 s=CrossSectionalMomentum(p,p*1000,hi,lo,op,corp_action_filter=False);s._prepare_stop_indicators();s.positions=df([.5]*5);s.rank_exit_mask=df([False]*5);s.atr=df([2]*5);out=bt.run_backtest(s)
 return {'held_on_entry_day':int(out['nheld'].iloc[1]),'entry_date':str(out['trades_df'].iloc[0].Entry_Date.date())}
a,b=run_stop(90),run_stop(80);c,d=run_mask(100),run_mask(500);e,f=run_circuit(False),run_circuit(True)
result={'stop_order':{'same_known_open':100,'later_low_90':a,'later_low_80':b,'result':'FAIL' if a!=b else 'PASS'},'mask_at_open':{'same_known_open':100,'no_large_close_jump':c,'close_later_500':d,'result':'FAIL' if c['entry_price']!=d['entry_price'] else 'PASS'},'circuit_at_open':{'same_known_open':100,'later_range_nonzero':e,'later_range_zero':f,'result':'FAIL' if e!=f else 'PASS'}}
assert a['reason']=='REBAL_EXIT' and b['reason']=='HARD_STOP_HIT' and a['holdings_next_day']>b['holdings_next_day']
assert c['entry_price']==100 and d['entry_price']==90
assert e['held_on_entry_day']==1 and f['held_on_entry_day']==0
(OUT/'execution_causality.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

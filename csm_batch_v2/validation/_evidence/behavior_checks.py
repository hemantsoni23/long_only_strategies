import sys,json
from pathlib import Path
import numpy as np
import pandas as pd
P=Path(__file__).resolve().parent;sys.path.insert(0,str(P.parents[1]));from csm_stock_strategy import CrossSectionalMomentum
r={}
s=CrossSectionalMomentum(pd.DataFrame(),pd.DataFrame(),use_vol_scaled_stop=True);h={'entry_price':100.,'peak_price':100.,'atr_stop':0.,'vs_width':.2}
a,_,_,st,_=s._check_stop_exit('X',110.,100.,1.,100.,h,curr_high=150.);b,fill,stop,_,_=s._check_stop_exit('X',110.,100.,1.,110.,st,curr_high=150.);r['stop_prior_peak']={'same_day_triggered':bool(a),'next_day_triggered':bool(b),'next_day_stop':stop,'next_day_fill':fill}
s=CrossSectionalMomentum(pd.DataFrame(),pd.DataFrame(),hard_stop_from_entry=.15,stop_slippage_pct=.003);h={'entry_price':100.,'peak_price':100.,'atr_stop':0.,'vs_width':np.nan};hit,fill,stop,_,reason=s._check_stop_exit('X',80.,35.,1.,100.,h,curr_high=105.);r['force_vs_standing']={'fired':bool(hit),'standing_hard_stop':85,'reported_stop':stop,'reported_fill':fill,'reason':reason}
idx=pd.to_datetime(['2020-01-02','2020-01-03']);p=pd.DataFrame({'X':[100.,np.nan]},index=idx);s=CrossSectionalMomentum(p,p,opens_df=p);s._prepare_stop_indicators(p.resample('ME').last());r['missing_open']={'current_open_missing':bool(pd.isna(p.iloc[1,0])),'filled_open':float(s._opens_ff.iloc[1,0])}
idx=pd.bdate_range('2020-01-01','2020-03-31');cols=[f'S{i:02d}' for i in range(30)];p=pd.DataFrame({c:100+np.arange(len(idx))*.1+np.sin(np.arange(len(idx))) for c in cols},index=idx);s=CrossSectionalMomentum(p,p*100,top_n=30,rebalance_months=1,rank_exit_dynamic=False,rebalance_min_fill_frac=.5);dates=pd.to_datetime(['2020-02-29','2020-03-31']);s.factors=pd.DataFrame([np.arange(30),np.arange(30)],index=dates,columns=cols);s.momentum_returns=pd.DataFrame([np.ones(30),-np.ones(30)],index=dates,columns=cols);positions=s.get_positions();r['guard']={'raw_ranked':30,'positive_momentum':0,'old_weights_retained':int((positions.iloc[1]>0).sum())}
idx=pd.bdate_range('2020-01-01',periods=400);a=np.arange(400);p=pd.DataFrame({'X':100+a*.1},index=idx);s=CrossSectionalMomentum(p,p*1000,p*1.01,p*.99,min_price=10,min_listing_days=252);m=p.resample('ME').last();mask=s.filter_universe(m,p);n=p.notna().cumsum().shift(1).resample('ME').last().reindex(m.index);r['listing_age']={'eligible_below_252':int(mask.where(n<252,False).sum().sum()),'eligible_at_or_above_252':int(mask.where(n>=252,False).sum().sum())}
(P/'behavior.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

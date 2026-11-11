"""Full-window per-reason forward returns and same-date grouped rotation comparison."""
from pathlib import Path
import glob
import os
import numpy as np
import pandas as pd
OUT=Path(__file__).resolve().parent;FOLDER=os.environ.get('IC_DATA_FOLDER','/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');tr=pd.read_csv(OUT/'late_universe_trades.csv',parse_dates=['Entry_Date','Exit_Date']);series=[]
for path in glob.glob(FOLDER+'/*.csv'):
 try:
  d=pd.read_csv(path,usecols=['datetime','close'],parse_dates=['datetime']).drop_duplicates('datetime',keep='last').set_index('datetime')['close'];d=d.loc['2013-10-08':];d.name=Path(path).stem;series.append(d)
 except Exception as ex:print('READ ERROR',path,repr(ex))
p=pd.concat(series,axis=1).sort_index();idx=p.index
uni=pd.read_parquet(OUT/'late_universe_universe.parquet').reindex(columns=p.columns,fill_value=False);uni=uni.reindex(pd.date_range(uni.index.min(),uni.index.max(),freq='ME'),fill_value=False)
daily=uni.reindex(p.index,method='ffill').shift(1).fillna(False).astype(bool);bench=(1+p.pct_change(fill_method=None).clip(-.5,.5).where(daily).mean(axis=1).fillna(0)).cumprod();del daily,uni
horizons=[1,3,5,10,20,40,60]
def forward(frame,datekey):
 rows=[]
 for _,r in frame.iterrows():
  dt=r[datekey];sym=r.Ticker;i=idx.searchsorted(dt);z={'ticker':sym,'date':dt,'reason':r.Exit_Reason}
  for n in horizons:
   z[f'raw_{n}']=np.nan;z[f'excess_{n}']=np.nan
   if i<len(idx) and idx[i]==dt and i+n<len(idx) and sym in p.columns:
    j=p.columns.get_loc(sym);a=p.iat[i,j];b=p.iat[i+n,j]
    if pd.notna(a) and pd.notna(b) and a>0 and b>0:
     ret=b/a-1;z[f'raw_{n}']=ret;z[f'excess_{n}']=ret-(bench.iloc[i+n]/bench.iloc[i]-1)
  rows.append(z)
 return pd.DataFrame(rows)
ex=forward(tr[tr.Exit_Reason!='END_OF_PERIOD'],'Exit_Date');en=forward(tr,'Entry_Date');results=[]
for reason,g in ex.groupby('reason'):
 sample=g.dropna(subset=['excess_20','excess_60']);mean=(sample.excess_20+sample.excess_60).mean()/2
 if reason=='END_OF_PERIOD':verdict='excluded'
 elif reason=='REBAL_EXIT':verdict='paired comparison'
 else:verdict=('working' if mean<=-.01 else ('too early' if mean>=.01 else 'neutral')) if len(sample) else 'unavailable'
 results.append({'reason':reason,'exits':len(g),'available_both':len(sample),'mean20_pct':sample.excess_20.mean()*100,'mean60_pct':sample.excess_60.mean()*100,'mean20_60_pct':mean*100,'verdict':verdict})
rot=[]
for reason in ('REBAL_EXIT','RANK_EXIT'):
 g=ex[ex.reason==reason]
 for n in (20,60):
  a=g.groupby('date')[f'raw_{n}'].agg(['mean','count']).rename(columns={'mean':'out','count':'n_out'});b=en.groupby('date')[f'raw_{n}'].agg(['mean','count']).rename(columns={'mean':'in','count':'n_in'});z=a.join(b,how='inner').dropna();z=z[(z.n_out>0)&(z.n_in>0)]
  rot.append({'reason':reason,'horizon_days':n,'dates':len(z),'entered_mean_pct':z['in'].mean()*100,'exited_mean_pct':z['out'].mean()*100,'difference_pp':(z['in']-z['out']).mean()*100})
pd.DataFrame(results).to_csv(OUT/'exit_summary.csv',index=False);pd.DataFrame(rot).to_csv(OUT/'exit_rotations.csv',index=False);ex.to_csv(OUT/'exit_forward.csv',index=False)
print(pd.DataFrame(results).round(3).to_string(index=False));print(pd.DataFrame(rot).round(3).to_string(index=False))
# Reconstruct the prior-close target on each stop date to quantify open-exit ordering.
pos=pd.read_parquet(OUT/'late_universe_positions.parquet');events=[];stop_reasons=['HARD_STOP_HIT','VOL_STOP_HIT','FORCE_EXIT','ATR_STOP_HIT','PEAK_STOP_HIT']
for row in tr[tr.Exit_Reason.isin(stop_reasons)].itertuples():
 i=idx.searchsorted(row.Exit_Date);j=pos.index.searchsorted(idx[i-1],side='right')-1 if i>0 and i<len(idx) else -1
 if j<0 or row.Ticker not in pos.columns:continue
 target=float(pos.at[pos.index[j],row.Ticker]);events.append({'ticker':row.Ticker,'date':row.Exit_Date,'reason':row.Exit_Reason,'target_at_open':target,'scheduled_zero_target':bool(target<=1e-6),'exit_price':row.Exit_Price})
events=pd.DataFrame(events);events.to_csv(OUT/'stop_open_ordering.csv',index=False)
print('STOP OPEN ORDERING',len(events),'stop exits with target zero at open',int(events.scheduled_zero_target.sum()) if len(events) else 0)

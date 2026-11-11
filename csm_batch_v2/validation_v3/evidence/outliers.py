"""Trace extreme portfolio days to raw observed returns for names spanning the day."""
from pathlib import Path
import pandas as pd
import numpy as np
P=Path(__file__).resolve().parent;DATA=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');results=[]
for tag in ['early_sweep','late_probe_band_500_1000','late_probe_positions_36','late_probe_positions_42']:
 r=pd.read_csv(P/f'{tag}_returns.csv',index_col=0,parse_dates=True).iloc[:,0];t=pd.read_csv(P/f'{tag}_trades.csv',parse_dates=['Entry_Date','Exit_Date']);dates=r.abs().nlargest(2).index
 for day in dates:
  held=t[(t.Entry_Date<=day)&(t.Exit_Date>=day)]; candidates=[]
  for row in held.itertuples():
   file=DATA/(str(row.Ticker)+'.csv')
   if not file.exists():continue
   q=pd.read_csv(file,usecols=['datetime','close'],parse_dates=['datetime']).drop_duplicates('datetime',keep='last').set_index('datetime').sort_index()['close'];i=q.index.searchsorted(day)
   if i>0 and i<len(q) and q.index[i]==day and q.iloc[i-1]>0 and pd.notna(q.iloc[i]):candidates.append((abs(q.iloc[i]/q.iloc[i-1]-1),row.Ticker,float(q.iloc[i-1]),float(q.iloc[i])))
  if not candidates:continue
  _,ticker,p0,p1=max(candidates);z=r.copy();z.loc[day]=0;year=(r.index[-1]-r.index[0]).days/365.25
  results.append({'cell':tag,'date':str(day.date()),'portfolio_day_pct':r.loc[day]*100,'ticker':ticker,'previous_close':p0,'close':p1,'stock_day_pct':(p1/p0-1)*100,'sharpe':r.mean()/r.std()*np.sqrt(252),'zero_day_sharpe':z.mean()/z.std()*np.sqrt(252),'cagr_pct':((1+r).prod()**(1/year)-1)*100,'zero_day_cagr_pct':((1+z).prod()**(1/year)-1)*100})
df=pd.DataFrame(results);df.to_csv(P/'outliers.csv',index=False);print(df.round(3).to_string(index=False))

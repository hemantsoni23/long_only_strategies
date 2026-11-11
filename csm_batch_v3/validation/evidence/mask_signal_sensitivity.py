import os
"""Compare raw and event-masked forward outcomes using identical v3 eligible signals."""
import sys
from pathlib import Path
import numpy as np,pandas as pd
OUT=Path(__file__).resolve().parent;ROOT=OUT.parents[1];sys.path.insert(0,str(ROOT));from csm_stock_strategy_v3 import load_data
P,V,H,L,O=load_data(os.environ.get('IC_DATA_FOLDER','/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'));p=P.loc['2013-10-08':'2025-12-31'];del P,V,H,L,O
ret=p.pct_change(fill_method=None);bad=(ret<-.4)|(ret>3.);clean=p.mask(bad|bad.shift(1,fill_value=False));m=clean.resample('ME').last();raw=p.resample('ME').last();mr=m.pct_change(fill_method=None);long=m.shift(1)/m.shift(13)-1;short=m.shift(1)/m.shift(7)-1;f=((long/(mr.rolling(12).std().shift(1)*np.sqrt(12))).clip(-5,5)+(short/(mr.rolling(6).std().shift(1)*np.sqrt(12))).clip(-5,5))/2
mask=pd.read_parquet(OUT/'late_universe_universe.parquet').reindex(index=m.index,columns=m.columns,fill_value=False)
rows=[]
for d in m.loc['2015-01-01':'2025-09-30'].index:
 fc=m.shift(-3).loc[d]/m.loc[d]-1;fr=raw.shift(-3).loc[d]/raw.loc[d]-1;valid=mask.loc[d]&f.loc[d].notna();cm=valid&fc.notna()&np.isfinite(fc);rm=valid&fr.notna()&np.isfinite(fr);both=cm&rm
 def corr(sel,y):return f.loc[d,sel].corr(y[sel],method='spearman') if sel.sum()>=8 else np.nan
 rows.append({'date':d,'eligible':int(valid.sum()),'clean_n':int(cm.sum()),'raw_n':int(rm.sum()),'both_n':int(both.sum()),'clean_ic':corr(cm,fc),'raw_ic':corr(rm,fr),'clean_common_ic':corr(both,fc),'raw_common_ic':corr(both,fr)})
df=pd.DataFrame(rows);df.to_csv(OUT/'mask_signal_comparison.csv',index=False);print(df.mean(numeric_only=True).to_string());print('total raw only',(df.raw_n-df.both_n).sum(),'clean only',(df.clean_n-df.both_n).sum())

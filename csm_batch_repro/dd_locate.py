import sys, os, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h, pandas as pd, numpy as np
pd.set_option('display.width',250)
res,log,csm = h.run({}, bt='csm_batch_backtest1')
eq=res['equity_curve']; dd=eq/eq.cummax()-1
trough=dd.idxmin(); peak=eq.loc[:trough].idxmax()
print("peak",peak.date(),"trough",trough.date(),"MDD",round(dd.min()*100,1))
pv=res['portfolio_value']; ye=pv.resample('YE').last(); r=ye.pct_change()*100; r.iloc[0]=(ye.iloc[0]/pv.iloc[0]-1)*100; r.index=r.index.year
ew=res['executed_weights'].sum(axis=1); al=ew.groupby(ew.index.year).mean()*100
yrdd=dd.groupby(dd.index.year).min()*100
print(pd.DataFrame({'ret':r,'alloc':al,'minDD':yrdd}).round(1).T.to_string())
# monthly path through the drawdown
seg=res['net_returns'].loc[peak:trough]
print((1+seg).resample('ME').prod().sub(1).mul(100).round(1).to_string())
# worst trades in the window
l=log[(log.Exit_Date>=peak)&(log.Exit_Date<=trough)].copy()
l['contrib']=l.Weight*l.PnL_Pct
print(l.sort_values('contrib').head(12)[['Ticker','Entry_Date','Exit_Date','Entry_Price','Exit_Price','Exit_Reason','Weight','PnL_Pct','contrib']].to_string())
print(l.groupby('Exit_Reason').agg(n=('PnL_Pct','size'),avg=('PnL_Pct','mean'),contrib=('contrib','sum')).round(2))

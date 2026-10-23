import sys, os, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h, pandas as pd, numpy as np
pd.set_option('display.width',250)
res,log,csm=h.run({}, bt='csm_batch_backtest1')
# (a) panic-day frequency by year
bv=csm._bvol_daily.reindex(csm.prices.index).ffill(); thr=csm._panic_threshold_series.reindex(csm.prices.index).ffill()
pan=(bv>thr).fillna(False)
print("panic days/yr:", pan.groupby(pan.index.year).sum().to_dict())
print("bench vol (21d, ann%) median by yr:", (bv*np.sqrt(252)*100).groupby(bv.index.year).median().round(0).to_dict())
print("threshold (ann%) at year end:", (thr*np.sqrt(252)*100).groupby(thr.index.year).last().round(0).to_dict())
print("n stocks w/ price by yr:", csm.prices.notna().sum(axis=1).groupby(csm.prices.index.year).mean().round(0).to_dict())
# (c) exit reason economics over whole window
log=log.copy(); log['contrib']=log.Weight*log.PnL_Pct
print(log.groupby('Exit_Reason').agg(n=('PnL_Pct','size'),avg=('PnL_Pct','mean'),hold=('Holding_Days','mean'),contrib=('contrib','sum')).round(2))
cg=log[log.Exit_Reason=='CRASH_GUARD']; print("crash-guard exits by yr:", cg.groupby(cg.Exit_Date.dt.year).size().to_dict())
# (d) cost drag
r0,l0,_=h.run({}, bt='csm_batch_backtest1', txn=0.0)
print(f"cost drag: CAGR txn0.3% {res['cagr']*100:.2f} vs txn0 {r0['cagr']*100:.2f}; ann turnover {res['ann_turnover']*100:.0f}%")
# (b) top_n=50 anomaly
r50,l50,c50=h.run(dict(top_n=50), bt='csm_batch_backtest1')
nr=r50['net_returns']; print("top_n50 worst/best days:\n", nr.sort_values().head(3).round(3).to_dict(), nr.sort_values().tail(5).round(3).to_dict())
d=nr.sort_values().index[-1]; w=r50['executed_weights'].loc[d]; print(d.date(), w[w>0].sort_values(ascending=False).head(5).round(3).to_dict())
l50=l50.copy(); print(l50.sort_values('PnL_Pct').tail(5)[['Ticker','Entry_Date','Exit_Date','Entry_Price','Exit_Price','Weight','PnL_Pct']])

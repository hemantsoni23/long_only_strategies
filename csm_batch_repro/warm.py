import sys, os, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h, pandas as pd, numpy as np
def go(tag, cfg=None, **kw):
    res,log,csm=h.run(cfg, bt='csm_batch_backtest1', report='2013-01-01', **kw)
    bv=csm._bvol_daily.reindex(csm.prices.index).ffill(); thr=csm._panic_threshold_series.reindex(csm.prices.index).ffill()
    pan=((bv>thr).fillna(False)).loc['2013':]
    print(f"{tag:<30} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} Shp {res['sharpe']:5.2f} N {len(log):5d} cg% {res['pct_crash_guard']:3.0f} panic days {int(pan.sum())}  by yr {pan.groupby(pan.index.year).sum().to_dict()}", flush=True)
for ls in ['2012-01-01','2010-01-01','2008-01-01','2005-01-01','2003-01-01']:
    go(f'load from {ls}', load=(ls,'2025-12-31'))
go('load 2003, crash guard OFF', dict(use_crash_guard=False), load=('2003-01-01','2025-12-31'))
# glitch hunt in baseline & top_n=50
for tn in (30,50):
    res,log,csm=h.run(dict(top_n=tn), bt='csm_batch_backtest1', report='2013-01-01')
    dr=csm.prices.pct_change(fill_method=None); ew=res['executed_weights']
    m=(ew.shift(1)>0)&(dr.abs()>0.35)
    s=dr.where(m).stack(); s=s[s.notna()]
    print(f"top_n={tn}: held-name daily moves beyond +/-35% (n={len(s)}):"); print(s.sort_values().round(2).to_string()[:1500])

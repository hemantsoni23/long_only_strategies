import sys, os, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h, pandas as pd, numpy as np
def go(tag, cfg=None, bt='csm_batch_backtest1', **kw):
    res,log,_=h.run(cfg, bt=bt, **kw)
    print(f"{tag:<34} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} Shp {res['sharpe']:5.2f} N {len(log):5d} WR {res['trade_win_rate']*100:5.1f} stop% {res['pct_stops']:4.0f} cg% {res['pct_crash_guard']:3.0f} alloc {res['avg_allocation']*100 if res['avg_allocation']<=1.5 else res['avg_allocation']:4.0f}", flush=True)
    return res
# benchmark context
p,v,hi,lo,op=h.data()
r=p.loc['2012-01-01':'2025-12-31'].pct_change(fill_method=None).clip(-0.5,0.5).mean(axis=1).fillna(0).loc['2013-01-01':]
eq=(1+r).cumprod(); n=(eq.index[-1]-eq.index[0]).days/365.25
print(f"EW all-stock benchmark 2013-25: CAGR {(eq.iloc[-1]**(1/n)-1)*100:.2f} MDD {((eq/eq.cummax()-1).min())*100:.1f}")
ye=eq.resample('YE').last(); print((ye.pct_change().mul(100).round(1)).rename(lambda d:d.year).to_dict())
go('current')
go('bt old (same-day stops)', bt='csm_batch_backtest')
go('trailing ON', dict(use_trailing_stop=True))
go('monthly rebalance', dict(rebalance_months=1))
go('rank_exit OFF', dict(rank_exit_dynamic=False))
go('crash guard OFF', dict(use_crash_guard=False))
go('vol_target 1.0 (off)', dict(vol_target=1.0))
go('hard stop 10%', dict(hard_stop_from_entry=0.10))
go('hard stop 25%', dict(hard_stop_from_entry=0.25))
go('top_n 15', dict(top_n=15))
go('top_n 50', dict(top_n=50))
go('universe_top_n 500', dict(universe_top_n=500))
go('universe_top_n 300', dict(universe_top_n=300))
go('v2.4 params (15,trail,mh5,mo)', dict(top_n=15,use_trailing_stop=True,min_hold_days=5,vol_target=0.15,rebalance_months=1,rank_exit_dynamic=False))

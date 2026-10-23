import sys, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import harness as h, pandas as pd
W=dict(load=('2003-01-01','2012-12-31'), report='2004-01-01')
V24=dict(top_n=15, use_trailing_stop=True, min_hold_days=5, vol_target=0.15, rebalance_months=1, rank_exit_dynamic=False)
def go(tag, cfg, bt, rfr=0.0, yrs=False):
    res,log,csm=h.run({**V24,**cfg}, bt=bt, rfr=rfr, **W)
    print(f"{tag:<44} rf{rfr:.2f} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} N {len(log):5d} WR {res['trade_win_rate']*100:5.1f} stop% {res['pct_stops']:5.1f} cg% {res['pct_crash_guard']:4.1f}", flush=True)
    if yrs:
        pv=res['portfolio_value']; ye=pv.resample('YE').last(); r=ye.pct_change()*100; r.iloc[0]=(ye.iloc[0]/pv.iloc[0]-1)*100; r.index=r.index.year; print("   ",r.round(1).to_dict())
for bt in ('csm_batch_backtest','csm_batch_backtest1'):
    go(f'v24-params / {bt}', {}, bt, 0.0)
    go(f'v24-params / {bt}', {}, bt, 0.08, yrs=True)
go('v24-params no-trail / bt', dict(use_trailing_stop=False), 'csm_batch_backtest', 0.08)
go('v24-params + quarterly / bt', dict(rebalance_months=3), 'csm_batch_backtest', 0.08)

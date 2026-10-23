import sys, os, warnings, importlib; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h
D=os.path.dirname(os.path.abspath(__file__))
def go(tag, pkl, cfg=None, **kw):
    h.CACHE = f'{D}/{pkl}'
    res,log,_=h.run(cfg, bt='csm_batch_backtest1', **kw)
    print(f"{tag:<26} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} Shp {res['sharpe']:5.2f} N {len(log):5d} WR {res['trade_win_rate']*100:5.1f}", flush=True)
for kw,name in [({}, '2013-2025'), (dict(load=('2003-01-01','2013-12-31'), report='2004-01-01'), '2004-2013')]:
    print('---',name)
    go('raw','data.pkl',**kw); go('generic adj (+/-)','data_adj_generic.pkl',**kw)

import sys, os, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness as h, bt1_x, pandas as pd, numpy as np
pd.set_option('display.width',250)
def go(tag, ent, ex, **kw):
    bt1_x.BOOK.update(entry=ent, exit=ex)
    res,log,_=h.run(None, bt='bt1_x', **kw)
    print(f"{tag:<44} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} Shp {res['sharpe']:5.2f} N {len(log)}", flush=True)
for kw,name in [({}, '2013-2025 current runner config'), (dict(load=('2003-01-01','2013-12-31'), report='2004-01-01'), '2004-2013 current config')]:
    print('---',name)
    go('as written (entry fix + exit gap charged)', True, True, **kw)
    bt1_x._GAPS.clear()
    go('Zenith-style (entry fix, exit day = 0)', True, False, **kw)
    go('no fixes (Elendel/Quad-style raw)', False, False, **kw)
    if not kw:
        g=pd.DataFrame(bt1_x._GAPS, columns=['date','tkr','reason','prev_w','gap']); g=g[g.date>='2013-01-01']
        g['contrib']=g.prev_w*g.gap
        print(g.groupby('reason').agg(n=('gap','size'), mean_gap_pct=('gap',lambda s: s.mean()*100), median_gap_pct=('gap',lambda s: s.median()*100), pct_neg=('gap',lambda s:(s<0).mean()*100), sum_w_gap_pct=('contrib',lambda s:s.sum()*100)).round(2))
        n=(g.date.max()-g.date.min()).days/365.25
        print("total exit-gap drag, pts of equity per year (simple sum / yrs): %.2f"%(g.contrib.sum()*100/n))

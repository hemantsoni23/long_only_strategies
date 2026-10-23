import sys, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import harness as h, bt_x
W=dict(load=('2003-01-01','2012-12-31'), report='2004-01-01')
V24=dict(top_n=15, use_trailing_stop=True, min_hold_days=5, vol_target=0.15, rebalance_months=1, rank_exit_dynamic=False)
print("ORIGINAL v2.4 engine (same data/window): rf0 CAGR 20.17 MDD -25.92 vol 10.04 N 1394 | rf8 CAGR 25.28")
for ent,ex in [(True,True),(False,True),(True,False),(False,False)]:
    bt_x.BOOK.update(entry=ent, exit=ex)
    for rfr in (0.0,0.08):
        res,log,_=h.run(V24, bt='bt_x', rfr=rfr, **W)
        print(f"entry_patch={ent!s:5} exit_gap={ex!s:5} rf{rfr:.2f} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} N {len(log)}", flush=True)

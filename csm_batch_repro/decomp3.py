import sys, warnings; warnings.filterwarnings('ignore'); sys.path.insert(0, __import__('os').path.dirname(__import__('os').path.abspath(__file__)))
import harness as h, bt_x
W=dict(load=('2003-01-01','2012-12-31'), report='2004-01-01')
V24=dict(top_n=15, use_trailing_stop=True, min_hold_days=5, vol_target=0.15, rebalance_months=1, rank_exit_dynamic=False)
print("ORIGINAL v2.4: rf0 CAGR 20.17 MDD -25.92 vol 10.04 N 1394 | rf8 CAGR 25.28 MDD -23.02")
bt_x.BOOK.update(entry=False, exit=False, cap=True)
for rfr in (0.0,0.08):
    res,log,_=h.run(V24, bt='bt_x', rfr=rfr, strat_mod='strat_x', **W)
    print(f"ATR-noshift + orig booking (cap) rf{rfr} CAGR {res['cagr']*100:6.2f} Vol {res['ann_volatility']*100:5.2f} MDD {res['max_drawdown']*100:7.2f} N {len(log)}", flush=True)

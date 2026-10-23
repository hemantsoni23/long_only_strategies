import sys, warnings, io, contextlib; warnings.filterwarnings('ignore')
sys.dont_write_bytecode=True
sys.path.insert(0,'/Users/hemantsoni/Documents/final_momentum_strategies')
import pandas as pd, numpy as np
sys.path.insert(1, __import__('os').path.dirname(__import__('os').path.abspath(__file__))); import harness as h
import csm_stock_strategy as S
def run_v24(rfr=0.0, load=('2001-01-01','2012-12-31'), report='2003-01-01', **over):
    prices, volumes, highs, lows, opens = h.data()
    sl=lambda d: d.loc[load[0]:load[1]]
    prices, volumes, highs, lows, opens = map(sl,(prices,volumes,highs,lows,opens))
    bench=(1+prices.pct_change(fill_method=None).fillna(0.0).mean(axis=1)).cumprod()
    kw=dict(lookback_months=12, lag_months=1, top_n=15, min_price=20.0, universe_top_n=1000, max_circuit_days=5,
      buffer_ratio=0.20, atr_period=14, atr_multiplier=3.0, atr_cap_percentile=0.75, atr_cap_window=63,
      hard_stop_from_entry=0.15, hard_stop_from_peak=0.20, stop_slippage_pct=0.003, use_crash_guard=True,
      crash_guard_cooldown=10, corr_guard_threshold=0.8, stop_cooldown_days=20, min_hold_days=5,
      atr_multiplier_high_vol=2.0, max_weight_per_stock=0.05, vol_target=0.15); kw.update(over)
    buf=io.StringIO()
    with contextlib.redirect_stdout(buf):
        csm=S.CrossSectionalMomentum(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, **kw)
        csm.calculate_factors(); csm.get_positions()
        res=csm.backtest_event_driven(initial_capital=100_000, transaction_cost=0.003, risk_free_rate=rfr)
    eq=res['equity_curve']; i=eq.index.searchsorted(report); st=eq.index[i]; eq=eq.loc[st:]; eq=eq/eq.iloc[0]
    ret=res['net_returns'].loc[st:]; n=(eq.index[-1]-eq.index[0]).days/365.25
    cagr=eq.iloc[-1]**(1/n)-1; dd=(eq/eq.cummax()-1).min()
    tl=csm.get_trade_log(); tl=tl[tl['Entry_Date']>=pd.Timestamp(report)]
    wr=(tl.PnL_Pct>0).mean()*100; gw=tl.loc[tl.PnL_Pct>0,'PnL_Pct'].sum(); gl=tl.loc[tl.PnL_Pct<0,'PnL_Pct'].abs().sum()
    ye=eq.resample('YE').last(); yr=ye.pct_change()*100; yr.iloc[0]=(ye.iloc[0]-1)*100; yr.index=yr.index.year
    print(f"v2.4 orig rfr={rfr}: CAGR {cagr*100:.2f} MDD {dd*100:.2f} vol {ret.std()*np.sqrt(252)*100:.2f} trades {len(tl)} WR {wr:.2f} PF% {gw/gl:.3f}")
    return res, tl, yr, csm
if __name__=='__main__':
    for r in (0.0, 0.08):
        res,tl,yr,_=run_v24(r)
        print(yr.round(1).to_dict())

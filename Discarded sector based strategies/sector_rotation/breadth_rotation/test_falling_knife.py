"""
test_falling_knife.py
========================
A/B test: the recommended config (StopCooldown + InverseVolSizing + CorrGuard
+ VolTarget=0.20, MinHold off) with vs without the falling-knife gate --
the one item left over from the original CSM audit table. trend_ok already
requires price>SMA50>SMA200, which likely already excludes most genuine
crashes, so this is a real test of marginal value, not an assumed win.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v4_full_risk as S

RECOMMENDED_VOL_TARGET = 0.20


def run_cell(label, prices, opens, sector_rank, members, universe_mask,
             sma_slow, trend_ok, persistence, bench_ok, atr,
             is_panic, leverage, stock_daily_ret, stock_vol, falling_knife):
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        use_min_hold=False, use_stop_cooldown=True,
        use_inverse_vol_sizing=True,
        use_corr_guard=True, use_vol_target=True,
        vol_target=RECOMMENDED_VOL_TARGET,
        falling_knife=falling_knife,
    )
    port_ret = S.compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
    n_years = len(port_ret) / 252.0
    ann_turnover = S.compute_turnover(positions_df, n_years)
    trades = S.enrich_trade_log(trade_log_df, equity)
    trade_stats = S.compute_trade_stats(trades)
    print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
          f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
          f"Trades={trade_stats['TotalTrades']}")
    return dict(Cell=label, CAGR=metrics["CAGR"]*100, Sharpe=metrics["Sharpe"],
                Sortino=metrics["Sortino"], Calmar=metrics["Calmar"],
                MaxDD=metrics["MaxDD"]*100, AnnVol=metrics["AnnVol"]*100,
                Turnover=ann_turnover*100, Trades=trade_stats["TotalTrades"])


def main():
    print("Loading OHLCV data + building factors...")
    prices, volumes, highs, lows, opens = S.load_data(S.DATA_FOLDER)
    members = S.build_sector_membership(prices, S.INSTRUMENTS_CSV)
    universe_mask = S.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = S.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = S.build_sector_rank(prices, members, universe_mask,
                                                          sector_price, daily_ret)
    sma_slow, trend_ok, persistence = S.build_stock_factors(prices)
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    common = dict(prices=prices, opens=opens, sector_rank=sector_rank, members=members,
                  universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
                  persistence=persistence, bench_ok=bench_ok, atr=atr, is_panic=is_panic,
                  leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol)

    rows = [
        run_cell("Recommended config, NO falling-knife gate", falling_knife=None, **common),
        run_cell("Recommended config, WITH falling-knife gate", falling_knife=falling_knife, **common),
    ]

    scorecard = pd.DataFrame(rows).set_index("Cell")
    print(f"\n{'='*100}\nFALLING-KNIFE A/B\n{'='*100}")
    print(scorecard.round(3).to_string())


if __name__ == "__main__":
    main()

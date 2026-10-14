"""
tune_stock_quality_weight.py
===============================
The 50/50 persistence/low-vol blend made Calmar WORSE (0.687->0.594) --
the low-vol tilt was too heavy, pulling in stocks that are low-vol because
they're weaker compounders, not smooth ones. Sweeps the blend weight to
find whether a LIGHTER low-vol tilt captures some MaxDD benefit without
giving up as much CAGR -- same process as the VOL_TARGET sweep. weight=1.0
is pure persistence (reproduces v6 exactly).
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v7_work as S

WEIGHT_GRID = [1.0, 0.99, 0.98, 0.97, 0.96, 0.95, 0.94, 0.93, 0.92, 0.91, 0.90]


def main():
    print("Loading OHLCV data + building factors (once, per-weight refactor for stock_quality only)...")
    prices, volumes, highs, lows, opens = S.load_data(S.DATA_FOLDER)
    members = S.build_sector_membership(prices, S.INSTRUMENTS_CSV)
    universe_mask = S.build_universe_mask(prices, volumes, highs, lows)
    sector_price, daily_ret = S.build_sector_index(prices, members)
    sector_rank, breadth, mom_disp = S.build_sector_rank(prices, members, universe_mask,
                                                          sector_price, daily_ret)
    sma_slow, trend_ok, persistence, _ = S.build_stock_factors(prices)   # persistence/trend_ok/sma_slow don't depend on weight
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    common = dict(prices=prices, opens=opens, sector_rank=sector_rank, members=members,
                  universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
                  persistence=persistence, bench_ok=bench_ok, atr=atr, is_panic=is_panic,
                  leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
                  falling_knife=falling_knife)

    rows = []
    for w in WEIGHT_GRID:
        label = f"weight={w:.2f}" + ("  (=v6 persistence-only)" if w >= 1.0 else "")
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        _, _, _, stock_quality_w = S.build_stock_factors(prices, quality_weight=w)
        positions_df, trade_log_df = S.run_backtest(
            **common, stock_quality=stock_quality_w,
            use_vol_aware_stock_factor=(w < 1.0),
        )
        port_ret = S.compute_portfolio_returns(positions_df, prices)
        metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
        n_years = len(port_ret) / 252.0
        ann_turnover = S.compute_turnover(positions_df, n_years)
        trades = S.enrich_trade_log(trade_log_df, equity)
        trade_stats = S.compute_trade_stats(trades)

        rows.append(dict(Weight=w, CAGR=metrics["CAGR"]*100, Sharpe=metrics["Sharpe"],
                          Sortino=metrics["Sortino"], Calmar=metrics["Calmar"],
                          MaxDD=metrics["MaxDD"]*100, AnnVol=metrics["AnnVol"]*100,
                          Trades=trade_stats["TotalTrades"]))
        print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
              f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%")

    scorecard = pd.DataFrame(rows).set_index("Weight")
    print(f"\n{'='*100}\nSTOCK_QUALITY_WEIGHT SWEEP\n{'='*100}")
    print(scorecard.round(3).to_string())


if __name__ == "__main__":
    main()

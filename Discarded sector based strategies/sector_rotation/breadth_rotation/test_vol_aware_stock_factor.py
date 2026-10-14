"""
test_vol_aware_stock_factor.py
=================================
Tests the §9 stock-level factor redesign: does blending trend persistence
with a low-volatility tilt (same equal-weight percentile-blend pattern as
the sector-level breadth composite) improve Calmar/MaxDD beyond what the
risk-overlay layer alone could achieve? Sector-selection layer (breadth-
divergence) is completely untouched -- only the within-sector stock pick
changes.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v7_work as S


def run_cell(label, use_vol_aware, prices, opens, sector_rank, members, universe_mask,
             sma_slow, trend_ok, persistence, bench_ok, atr,
             is_panic, leverage, stock_daily_ret, stock_vol, falling_knife, stock_quality):
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, stock_quality=stock_quality,
        use_vol_aware_stock_factor=use_vol_aware,
    )
    port_ret = S.compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
    n_years = len(port_ret) / 252.0
    ann_turnover = S.compute_turnover(positions_df, n_years)
    trades = S.enrich_trade_log(trade_log_df, equity)
    trade_stats = S.compute_trade_stats(trades)
    print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
          f"Sortino={metrics['Sortino']:.3f}  Calmar={metrics['Calmar']:.3f}  "
          f"MaxDD={metrics['MaxDD']*100:.2f}%  AnnVol={metrics['AnnVol']*100:.2f}%  "
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
    sma_slow, trend_ok, persistence, stock_quality = S.build_stock_factors(prices)
    atr = S.build_atr(prices, highs, lows)
    bench_ok, is_panic, leverage = S.compute_regime(sector_price)
    stock_daily_ret, stock_vol = S.build_stock_vol(prices)
    falling_knife = S.build_falling_knife_gate(prices)

    common = dict(prices=prices, opens=opens, sector_rank=sector_rank, members=members,
                  universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
                  persistence=persistence, bench_ok=bench_ok, atr=atr, is_panic=is_panic,
                  leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
                  falling_knife=falling_knife, stock_quality=stock_quality)

    rows = [
        run_cell("0_baseline (=v6, persistence only)", False, **common),
        run_cell("1_vol-aware blend (0.5 persistence / 0.5 low-vol)", True, **common),
    ]

    scorecard = pd.DataFrame(rows).set_index("Cell")
    print(f"\n{'='*100}\nSCORECARD\n{'='*100}")
    print(scorecard.round(3).to_string())


if __name__ == "__main__":
    main()

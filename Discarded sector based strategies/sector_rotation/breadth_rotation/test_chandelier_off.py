"""
test_chandelier_off.py
=========================
Exit breakdown showed ATR_STOP as the largest bucket (187/346 trades) and
worst by total Rs P&L. Tests the direct hypothesis: what happens if the
chandelier is disabled entirely (only the fixed -15% stop remains) --
matching CSM Quad's OWN default (use_chandelier=False), where exits are
signal-driven (rank decay) rather than price-trail-driven. Those 187
positions don't vanish if the chandelier is removed -- they ride until the
next rank-decay check or the -15% floor instead, which could be better or
worse. This is the empirical test, not an assumption either way.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v6_work as S


def run_cell(label, use_chandelier, prices, opens, sector_rank, members, universe_mask,
             sma_slow, trend_ok, persistence, bench_ok, atr,
             is_panic, leverage, stock_daily_ret, stock_vol, falling_knife):
    print(f"\n{'='*70}\n{label}\n{'='*70}")
    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, use_chandelier=use_chandelier,
    )
    port_ret = S.compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
    n_years = len(port_ret) / 252.0
    ann_turnover = S.compute_turnover(positions_df, n_years)
    trades = S.enrich_trade_log(trade_log_df, equity)
    trade_stats = S.compute_trade_stats(trades)
    exit_bd = S.compute_exit_breakdown(trades)

    print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
          f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
          f"Trades={trade_stats['TotalTrades']}")
    print(exit_bd.round(2).to_string())

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
                  leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
                  falling_knife=falling_knife)

    rows = [
        run_cell("0_baseline (=v6, chandelier ON)", True, **common),
        run_cell("1_chandelier OFF (fixed -15% only)", False, **common),
    ]

    scorecard = pd.DataFrame(rows).set_index("Cell")
    print(f"\n{'='*100}\nSCORECARD\n{'='*100}")
    print(scorecard.round(3).to_string())


if __name__ == "__main__":
    main()

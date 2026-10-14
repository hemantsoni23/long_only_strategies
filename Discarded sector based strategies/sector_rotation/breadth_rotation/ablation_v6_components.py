"""
ablation_v6_components.py
============================
Ablation for the two components found on a closer re-read of CSM Quad's
code (missed in the original high-level audit table):
  §6 chandelier floor -- ATR stop ratchets + clamped to [3%,30%] of peak
     (v5 baseline never ratcheted/persisted the ATR stop at all -- a
     same-day ATR spike could make the effective stop retreat even though
     peak never fell)
  §7 swap-gap displacement -- a much-better-ranked new candidate can evict
     the worst-ranked HELD name in the same sector when full

Cell 0 (both flags False) reproduces sector_breadth_strategy_v5.py exactly
(CAGR 15.94%/Sharpe 1.168/Calmar 0.688/MaxDD -23.17%) -- verified below,
not assumed.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v5_work as S

CELLS = [
    ("0_baseline (=v5)",          False, False),
    ("1_+ChandelierFloor",        True,  False),
    ("2_+SwapGap",                False, True),
    ("3_+Both (candidate v6)",    True,  True),
]


def main():
    print("Loading OHLCV data + building factors (once, reused for all cells)...")
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

    rows = []
    for label, use_cf, use_sg in CELLS:
        print(f"\n{'='*70}\nCell: {label}\n{'='*70}")
        positions_df, trade_log_df = S.run_backtest(
            prices, opens, sector_rank, members, universe_mask,
            sma_slow, trend_ok, persistence, bench_ok, atr,
            is_panic, leverage, stock_daily_ret, stock_vol,
            falling_knife=falling_knife,
            use_chandelier_floor=use_cf, use_swap_gap=use_sg,
        )
        port_ret = S.compute_portfolio_returns(positions_df, prices)
        metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
        n_years = len(port_ret) / 252.0
        ann_turnover = S.compute_turnover(positions_df, n_years)
        trades = S.enrich_trade_log(trade_log_df, equity)
        trade_stats = S.compute_trade_stats(trades)

        rows.append(dict(
            Cell=label, CAGR=metrics["CAGR"]*100, Sharpe=metrics["Sharpe"],
            Sortino=metrics["Sortino"], Calmar=metrics["Calmar"], MaxDD=metrics["MaxDD"]*100,
            AnnVol=metrics["AnnVol"]*100, Turnover=ann_turnover*100,
            Trades=trade_stats["TotalTrades"],
        ))
        if not trades.empty and "SWAP_GAP" in trades["Exit_Reason"].values:
            n_swap = (trades["Exit_Reason"] == "SWAP_GAP").sum()
            print(f"  (SWAP_GAP fired {n_swap} times)")
        print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
              f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
              f"Trades={trade_stats['TotalTrades']}")

    scorecard = pd.DataFrame(rows).set_index("Cell")
    baseline = scorecard.iloc[0]
    delta = scorecard.copy()
    for col in ["CAGR", "Sharpe", "Sortino", "Calmar", "MaxDD", "AnnVol", "Turnover"]:
        delta[col] = scorecard[col] - baseline[col]

    print(f"\n{'='*100}\nSCORECARD\n{'='*100}")
    print(scorecard.round(3).to_string())
    print(f"\n{'='*100}\nDELTA vs 0_baseline (=v5)\n{'='*100}")
    print(delta.round(3).to_string())


if __name__ == "__main__":
    main()

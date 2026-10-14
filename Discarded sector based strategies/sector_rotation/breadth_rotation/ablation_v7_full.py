"""
ablation_v7_full.py
======================
Comprehensive leave-one-out ablation against the FINAL v7 baseline (CAGR
16.14%/Sharpe 1.291/Calmar 0.786/MaxDD -20.52%) -- not the historical
piecemeal bases used when each component was first tested (v3/v4/v5/v6),
since interactions between components may differ now that the vol-aware
stock factor is in the mix. Every toggleable flag in v7 gets its own cell,
each one component flipped OFF (or ON, for min_hold which defaults OFF)
from the full v7 configuration, one at a time.

use_crash_guard, use_stock_rank_decline, use_sector_rank_decline were only
ever verified to mechanically work before (each correctly zeroes its exit
reason) -- never actually ablation-tested for PERFORMANCE impact. This is
the first time they get that test.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v7 as S

# label, kwargs override (relative to v7's own defaults)
CELLS = [
    ("0_baseline (=v7)",              dict()),
    ("1_MinHold ON (v7 default OFF)", dict(use_min_hold=True)),
    ("2_StopCooldown OFF",            dict(use_stop_cooldown=False)),
    ("3_InverseVolSizing OFF",        dict(use_inverse_vol_sizing=False)),
    ("4_CorrGuard OFF",               dict(use_corr_guard=False)),
    ("5_VolTarget OFF",               dict(use_vol_target=False)),
    ("6_ChandelierFloor OFF",         dict(use_chandelier_floor=False)),
    ("7_SwapGap OFF",                 dict(use_swap_gap=False)),
    ("8_Chandelier OFF (ATR_STOP)",   dict(use_chandelier=False)),
    ("9_StopLoss OFF",                dict(use_stop_loss=False)),
    ("10_CrashGuard OFF",             dict(use_crash_guard=False)),
    ("11_StockRankDecline OFF",       dict(use_stock_rank_decline=False)),
    ("12_SectorRankDecline OFF",      dict(use_sector_rank_decline=False)),
    ("13_FallingKnife OFF",           dict(falling_knife=None)),
    ("14_VolAwareStockFactor OFF",    dict(use_vol_aware_stock_factor=False)),
]


def main():
    print("Loading OHLCV data + building factors (once, reused for all cells)...")
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
    falling_knife_gate = S.build_falling_knife_gate(prices)

    base_kwargs = dict(
        prices=prices, opens=opens, sector_rank=sector_rank, members=members,
        universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
        persistence=persistence, bench_ok=bench_ok, atr=atr, is_panic=is_panic,
        leverage=leverage, stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
        falling_knife=falling_knife_gate, stock_quality=stock_quality,
    )

    rows = []
    for label, override in CELLS:
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        kwargs = {**base_kwargs, **override}
        positions_df, trade_log_df = S.run_backtest(**kwargs)
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
        print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
              f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
              f"Trades={trade_stats['TotalTrades']}")

    scorecard = pd.DataFrame(rows).set_index("Cell")
    baseline = scorecard.iloc[0]
    delta = scorecard.copy()
    for col in ["CAGR", "Sharpe", "Sortino", "Calmar", "MaxDD", "AnnVol", "Turnover"]:
        delta[col] = scorecard[col] - baseline[col]

    print(f"\n{'='*110}\nFULL ABLATION SCORECARD  (vs 0_baseline = v7)\n{'='*110}")
    print(scorecard.round(3).to_string())
    print(f"\n{'='*110}\nDELTA  (positive Calmar delta = removing/adding this component HELPED)\n{'='*110}")
    print(delta.round(3).to_string())

    out = os.path.join(os.path.dirname(__file__), "ablation_v7_full_scorecard.csv")
    scorecard.to_csv(out)
    print(f"\nSaved scorecard to {out}")


if __name__ == "__main__":
    main()

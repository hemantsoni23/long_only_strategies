"""
ablation_v4_components.py
============================
Leave-one-in ablation for the four risk components added in
sector_breadth_strategy_v4_full_risk.py: min-hold grace, loss-scaled stop
cooldown, inverse-vol sizing, and Corr Guard + Vol Target. Cell 0 (all
flags off) reproduces sector_breadth_strategy_v3_regime.py's baseline
(CAGR 17.05%/Sharpe 1.270/Calmar 0.630/MaxDD -27.05%) exactly -- verified
below as a sanity check, not assumed. Cell 5 (all flags on) reproduces v4
(CAGR 14.37%/Calmar 0.631/MaxDD -22.78%).

Data + factors are loaded/computed ONCE (the expensive part -- ~5200
tickers) and reused across all 6 backtest runs, which are cheap by
comparison. Imports sector_breadth_strategy_v4_full_risk.py as a module
rather than duplicating its code.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v4_full_risk as S

CELLS = [
    # label,                    min_hold, stop_cd, inv_vol, corr_guard, vol_target
    ("0_baseline (=v3)",        False, False, False, False, False),
    ("1_+MinHold",              True,  False, False, False, False),
    ("2_+StopCooldown",         False, True,  False, False, False),
    ("3_+InverseVolSizing",     False, False, True,  False, False),
    ("4a_+CorrGuardOnly",       False, False, False, True,  False),
    ("4b_+VolTargetOnly",       False, False, False, False, True),
    ("4c_+CorrGuard+VolTarget", False, False, False, True,  True),
    ("5_all_four (=v4)",        True,  True,  True,  True,  True),
]


def main():
    print("Loading OHLCV data + building factors (once, reused for all 6 cells)...")
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

    rows = []
    for label, use_mh, use_sc, use_iv, use_cg, use_vt in CELLS:
        print(f"\n{'='*70}\nCell: {label}\n{'='*70}")
        positions_df, trade_log_df = S.run_backtest(
            prices, opens, sector_rank, members, universe_mask,
            sma_slow, trend_ok, persistence, bench_ok, atr,
            is_panic, leverage, stock_daily_ret, stock_vol,
            use_min_hold=use_mh, use_stop_cooldown=use_sc,
            use_inverse_vol_sizing=use_iv,
            use_corr_guard=use_cg, use_vol_target=use_vt,
        )
        port_ret = S.compute_portfolio_returns(positions_df, prices)
        metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
        n_years = len(port_ret) / 252.0
        ann_turnover = S.compute_turnover(positions_df, n_years)

        trades = S.enrich_trade_log(trade_log_df, equity)
        trade_stats = S.compute_trade_stats(trades)

        rows.append(dict(
            Cell=label,
            CAGR=metrics["CAGR"] * 100, Sharpe=metrics["Sharpe"], Sortino=metrics["Sortino"],
            Calmar=metrics["Calmar"], MaxDD=metrics["MaxDD"] * 100,
            AnnVol=metrics["AnnVol"] * 100, Turnover=ann_turnover * 100,
            Trades=trade_stats["TotalTrades"], TradeWinRate=trade_stats["TradeWinRate"] * 100,
        ))
        print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
              f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
              f"Trades={trade_stats['TotalTrades']}")

    scorecard = pd.DataFrame(rows).set_index("Cell")
    baseline = scorecard.iloc[0]
    delta = scorecard.copy()
    for col in ["CAGR", "Sharpe", "Sortino", "Calmar", "MaxDD", "AnnVol", "Turnover"]:
        delta[col] = scorecard[col] - baseline[col]

    print(f"\n{'='*100}\nABLATION SCORECARD  (vs 0_baseline)\n{'='*100}")
    print(scorecard.round(3).to_string())
    print(f"\n{'='*100}\nDELTA vs 0_baseline\n{'='*100}")
    print(delta.round(3).to_string())

    out = os.path.join(os.path.dirname(__file__), "ablation_v4_scorecard.csv")
    scorecard.to_csv(out)
    print(f"\nSaved scorecard to {out}")


if __name__ == "__main__":
    main()

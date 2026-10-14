"""
tune_vol_target.py
=====================
Ablation (ablation_v4_components.py) found: Corr Guard is a complete no-op
at CORR_GUARD_THRESHOLD=0.8 (identical to baseline on every metric -- an
8-position/4-sector book apparently never crosses portfolio-vol/avg-stock-
vol > 0.8 in this sample), and Vol Target alone explains 100% of the §4
group's drag (-3.1pp CAGR, -0.034 Calmar vs baseline -- WORSE than not
having it, despite cutting MaxDD the most of any single component).

Hypothesis: VOL_TARGET=0.15 is tighter than this strategy's natural vol
during genuinely productive (not crash) high-vol periods -- e.g. 2007's
+132% year likely carries high realized vol from the sheer size of daily
moves in an uptrend, and a 15% target would chronically clip that upside,
not just react to real tail risk.

Sweeps VOL_TARGET on top of the two components ablation showed as clear
standalone net-positives (StopCooldown, InverseVolSizing -- both improved
Calmar AND cut MaxDD). MinHold excluded (ablation: worsened BOTH Calmar and
MaxDD, only a marginal CAGR uptick -- not worth it against the "MaxDD as
low as possible" objective). Corr Guard left ON (harmless no-op here, kept
for robustness against future/OOS periods where correlation genuinely
spikes).
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v4_full_risk as S

VOL_TARGET_GRID = [0.15, 0.18, 0.20, 0.25, 0.30, 0.35, 1.0]   # 1.0 ~= effectively off


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

    rows = []
    for vt in VOL_TARGET_GRID:
        label = f"VOL_TARGET={vt:.2f}" + ("  (~off)" if vt >= 1.0 else "")
        print(f"\n{'='*70}\n{label}\n{'='*70}")
        positions_df, trade_log_df = S.run_backtest(
            prices, opens, sector_rank, members, universe_mask,
            sma_slow, trend_ok, persistence, bench_ok, atr,
            is_panic, leverage, stock_daily_ret, stock_vol,
            use_min_hold=False, use_stop_cooldown=True,
            use_inverse_vol_sizing=True,
            use_corr_guard=True, use_vol_target=True,
            vol_target=vt,
        )
        port_ret = S.compute_portfolio_returns(positions_df, prices)
        metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
        n_years = len(port_ret) / 252.0
        ann_turnover = S.compute_turnover(positions_df, n_years)
        trades = S.enrich_trade_log(trade_log_df, equity)
        trade_stats = S.compute_trade_stats(trades)

        rows.append(dict(
            VolTarget=vt, CAGR=metrics["CAGR"] * 100, Sharpe=metrics["Sharpe"],
            Sortino=metrics["Sortino"], Calmar=metrics["Calmar"], MaxDD=metrics["MaxDD"] * 100,
            AnnVol=metrics["AnnVol"] * 100, Turnover=ann_turnover * 100,
            Trades=trade_stats["TotalTrades"],
        ))
        print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
              f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%")

    scorecard = pd.DataFrame(rows).set_index("VolTarget")
    print(f"\n{'='*100}\nVOL_TARGET SWEEP  (StopCooldown + InverseVolSizing always ON, MinHold OFF)\n{'='*100}")
    print(scorecard.round(3).to_string())

    out = os.path.join(os.path.dirname(__file__), "vol_target_sweep.csv")
    scorecard.to_csv(out)
    print(f"\nSaved sweep to {out}")


if __name__ == "__main__":
    main()

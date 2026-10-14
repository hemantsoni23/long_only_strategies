"""
retune_sizing_voltarget.py
=============================
Ablation flagged InverseVolSizing and VolTarget as possibly stale against
the new v7 base (vol-aware stock factor already does some of what they
were compensating for). Both act on portfolio-level volatility, so tested
jointly rather than one at a time: InverseVolSizing {True, False} x
VolTarget level {off, 0.15, 0.20 (v7 current), 0.25, 0.30}.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v7 as S

VOL_TARGET_GRID = [0.15, 0.20, 0.25, 0.30, 1.0]   # 1.0 ~= effectively off


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
    for use_ivs in (True, False):
        for vt in VOL_TARGET_GRID:
            label = f"InvVolSizing={use_ivs}  VolTarget={vt:.2f}" + ("(~off)" if vt >= 1.0 else "")
            print(f"\n{'='*70}\n{label}\n{'='*70}")
            positions_df, trade_log_df = S.run_backtest(
                **base_kwargs, use_inverse_vol_sizing=use_ivs, vol_target=vt,
            )
            port_ret = S.compute_portfolio_returns(positions_df, prices)
            metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
            n_years = len(port_ret) / 252.0
            ann_turnover = S.compute_turnover(positions_df, n_years)
            trades = S.enrich_trade_log(trade_log_df, equity)
            trade_stats = S.compute_trade_stats(trades)

            rows.append(dict(
                InvVolSizing=use_ivs, VolTarget=vt, CAGR=metrics["CAGR"]*100,
                Sharpe=metrics["Sharpe"], Sortino=metrics["Sortino"], Calmar=metrics["Calmar"],
                MaxDD=metrics["MaxDD"]*100, AnnVol=metrics["AnnVol"]*100,
                Turnover=ann_turnover*100, Trades=trade_stats["TotalTrades"],
            ))
            print(f"  CAGR={metrics['CAGR']*100:+.2f}%  Sharpe={metrics['Sharpe']:.3f}  "
                  f"Calmar={metrics['Calmar']:.3f}  MaxDD={metrics['MaxDD']*100:.2f}%  "
                  f"Turnover={ann_turnover*100:.0f}%")

    scorecard = pd.DataFrame(rows).set_index(["InvVolSizing", "VolTarget"])
    print(f"\n{'='*110}\nJOINT SWEEP\n{'='*110}")
    print(scorecard.round(3).to_string())


if __name__ == "__main__":
    main()

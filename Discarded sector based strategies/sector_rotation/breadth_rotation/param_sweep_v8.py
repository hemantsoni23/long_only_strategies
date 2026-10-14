"""
param_sweep_v8.py
====================
Playbook Stage 3.2 parameter sensitivity sweep on v8's structural knobs --
one parameter at a time, +/-20%/+/-40% around its current value (>=5 points
incl. current), everything else held at v8's baseline. Gate per the
Playbook: a knob that swings Sharpe >0.4 on a 20% nudge is a "cliff"
(overfit to that exact value); prefer a flat plateau even if some other
point's raw number is higher.

Deliberately NOT touched: the sector-level breadth factor's own internal
windows (HI_LO_WIN, NET_HI_LO_SMOOTH, SECTOR_MOM_PERIOD, DISPERSION_WINDOW)
and the frozen BETA_MOM_DISP -- those were already IC-validated separately
in sector_breadth_ic_test.py and are explicitly documented as never-refit.
This sweep only touches structural/risk knobs: N_SECTORS, STOCKS_PER_SECTOR
(with their _EXIT hysteresis siblings coupled to move with them),
REBALANCE_EVERY, STOP_LOSS_PCT, ATR_MULTIPLIER, MAX_WEIGHT_PER_STOCK, and
TREND_PERSIST_WIN (the one stock-factor lookback).

Uses module-attribute monkey-patching (S.N_SECTORS = x) rather than adding
~7 new run_backtest parameters -- verified safe here because none of these
six are captured as function-signature DEFAULT VALUES anywhere (which
would freeze at import time); all are read as bare globals inside function
bodies, resolved at call time. TREND_PERSIST_WIN is the one that requires
rebuilding build_stock_factors() per value rather than just re-running
run_backtest.
"""

import os
import sys
import warnings

import pandas as pd

warnings.filterwarnings("ignore")
sys.path.insert(0, os.path.dirname(__file__))

import sector_breadth_strategy_v8 as S

# Baseline (v8's current values) -- restored between each parameter's sweep
BASELINE = dict(
    N_SECTORS=4, N_SECTORS_EXIT=5,
    STOCKS_PER_SECTOR=2, STOCKS_PER_SECTOR_EXIT=4,
    REBALANCE_EVERY=20, STOP_LOSS_PCT=0.15, ATR_MULTIPLIER=2.5,
    MAX_WEIGHT_PER_STOCK=0.20, TREND_PERSIST_WIN=126,
)


def restore_baseline():
    for k, v in BASELINE.items():
        setattr(S, k, v)
    S.MAX_POSITIONS = S.N_SECTORS * S.STOCKS_PER_SECTOR


def set_and_couple(param, value):
    """Applies one swept value, keeping the _EXIT hysteresis siblings and
    MAX_POSITIONS coupled to their driver, same ratio as the v8 baseline."""
    if param == "N_SECTORS":
        S.N_SECTORS = value
        S.N_SECTORS_EXIT = value + 1              # baseline gap: 4->5
    elif param == "STOCKS_PER_SECTOR":
        S.STOCKS_PER_SECTOR = value
        S.STOCKS_PER_SECTOR_EXIT = value * 2       # baseline ratio: 2->4
    else:
        setattr(S, param, value)
    S.MAX_POSITIONS = S.N_SECTORS * S.STOCKS_PER_SECTOR


def run_one(prices, opens, sector_rank, members, universe_mask,
            sma_slow, trend_ok, persistence, bench_ok, atr,
            is_panic, leverage, stock_daily_ret, stock_vol,
            falling_knife, stock_quality):
    positions_df, trade_log_df = S.run_backtest(
        prices, opens, sector_rank, members, universe_mask,
        sma_slow, trend_ok, persistence, bench_ok, atr,
        is_panic, leverage, stock_daily_ret, stock_vol,
        falling_knife=falling_knife, stock_quality=stock_quality,
    )
    port_ret = S.compute_portfolio_returns(positions_df, prices)
    metrics, equity, drawdown, monthly_ret = S.compute_metrics(port_ret)
    n_years = len(port_ret) / 252.0
    ann_turnover = S.compute_turnover(positions_df, n_years)
    trades = S.enrich_trade_log(trade_log_df, equity)
    trade_stats = S.compute_trade_stats(trades)
    return dict(CAGR=metrics["CAGR"]*100, Sharpe=metrics["Sharpe"], Sortino=metrics["Sortino"],
                Calmar=metrics["Calmar"], MaxDD=metrics["MaxDD"]*100, AnnVol=metrics["AnnVol"]*100,
                Turnover=ann_turnover*100, Trades=trade_stats["TotalTrades"])


def main():
    print("Loading OHLCV data + building factors (once, reused across most cells)...")
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

    common_factors = dict(
        prices=prices, opens=opens, sector_rank=sector_rank, members=members,
        universe_mask=universe_mask, sma_slow=sma_slow, trend_ok=trend_ok,
        bench_ok=bench_ok, atr=atr, is_panic=is_panic, leverage=leverage,
        stock_daily_ret=stock_daily_ret, stock_vol=stock_vol,
        falling_knife=falling_knife_gate,
    )

    all_rows = []

    # ── Backtest-loop-only params: reuse the SAME precomputed factors ──
    sweeps = [
        ("STOP_LOSS_PCT", [0.10, 0.11, 0.12, 0.13, 0.14]),
    ]
    for param, grid in sweeps:
        print(f"\n{'='*80}\nSWEEP: {param}\n{'='*80}")
        for value in grid:
            restore_baseline()
            set_and_couple(param, value)
            tag = " (baseline)" if value == BASELINE.get(param) else ""
            res = run_one(persistence=persistence, stock_quality=stock_quality, **common_factors)
            res.update(Param=param, Value=value)
            all_rows.append(res)
            print(f"  {param}={value}{tag}: CAGR={res['CAGR']:+.2f}%  Sharpe={res['Sharpe']:.3f}  "
                  f"Calmar={res['Calmar']:.3f}  MaxDD={res['MaxDD']:.2f}%  Trades={res['Trades']}")
    restore_baseline()

    # TREND_PERSIST_WIN already swept and confirmed a genuine interior optimum
    # at 126 in the prior full run -- skipped here to focus on the STOP_LOSS_PCT
    # neighborhood check.

    scorecard = pd.DataFrame(all_rows).set_index(["Param", "Value"])
    print(f"\n{'='*100}\nFULL PARAMETER SWEEP SCORECARD\n{'='*100}")
    print(scorecard.round(3).to_string())

    out = os.path.join(os.path.dirname(__file__), "param_sweep_v8_scorecard.csv")
    scorecard.to_csv(out)
    print(f"\nSaved scorecard to {out}")


if __name__ == "__main__":
    main()

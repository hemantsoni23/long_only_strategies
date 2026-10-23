# CSM Aegis

CSM Aegis is a long-only Indian-equity momentum strategy. It selects liquid, trending names with a residual-momentum and smoothness composite, then manages them through a close-based execution and risk wrapper.

**Status: research / paper-trade candidate.** It is not live-validated. Results use survivorship-biased OHLCV data and must not be used as a live-return forecast.

## Production configuration

`v1.2` is the only production preset. Its backtest has **no return on idle cash**: the strategy return is solely the equity-book return after modeled transaction costs. Any return earned by cash outside the strategy must be accounted for separately by the portfolio/accounting layer.

| Block | Rule |
|---|---|
| Universe | Price >= Rs 20; 63-day rupee-volume rank 1-1000; <= 5 circuit-locked sessions in 63 days; close above SMA-200; exclude the worst 20% by M3 single-day-spike risk. |
| Signal | `z(R1) + z(-Ulcer252)` within the eligible pool. R1 is 12-month residual momentum skipping the latest month; Ulcer rewards smoother compounders. |
| Selection | Top 20 at month-end. Existing holdings stay until rank > 40 or they leave the pool. |
| Entry filters | Reject entries more than 25% above SMA-50; block new entries in the high-volatility state. |
| Market gate | Exit all and do not enter when the equal-weight market is at/below its 120-day average. |
| Exits | Close-based -15% entry stop, -20% trailing stop, 45-day weak-position time stop, rank/pool exit, or market-gate exit; execute at the next close. |
| Sizing | 1% risk / stop distance, clamped to 3-8% per name; gross exposure capped at 100%; no leverage. |
| Execution | Next-close fills and 0.3% transaction cost on each entry and exit. Idle cash return is 0%. |

Historical v1.2 research result (2005-01 through 2026-07, close fills, 0.3% per leg, no cash yield): **24.2% CAGR, 1.69 Sharpe, -29% max drawdown**. This is a backtest result, not a target.

## Files

| File | Responsibility |
|---|---|
| `csm_aegis_strategy.py` | All strategy logic: data loading, factors, universe, ranking, selection, sizing, stops, gates, presets, and live position/exit helpers. |
| `csm_aegis_backtest.py` | Backtest booking, metrics, diagnostics, plots, output generation, and the command-line runner. |
| `test_parity.py` | Regression/parity checks against the research engine and live exit rules. |

The first two are the complete runnable strategy package. `test_parity.py` is a verification script, not a third production component. `CSM_AEGIS_REPORT.md` is the chronological research record and can contain superseded historical configurations.

## Run

```bash
cd csm_aegis
python3 csm_aegis_backtest.py
python3 csm_aegis_backtest.py --compare --stress
python3 csm_aegis_backtest.py --set top_n=15 --set stop_from_entry=0.12
python3 csm_aegis_backtest.py --asof 2026-06-30
python3 csm_aegis_backtest.py --holdings my_holdings.csv
python3 test_parity.py
```

Set `CSM_AEGIS_DATA_FOLDER` if the OHLCV folder is not at the configured local default. `my_holdings.csv` requires `ticker`, `entry_date`, and `entry_price` columns.

`output/` receives the trade, rejection, daily, return, yearly-return, and selection files plus the run log and performance plot.

## Next research objective

The next workstream is drawdown reduction, learned from the existing live books. We will test each candidate control against the frozen v1.2 baseline, require a drawdown improvement without unacceptable return/robustness degradation, and retain only changes that survive cost, delay, capacity, and recent-period checks.

Before paper trading, also resolve the existing data-quality and live-order-sheet issues recorded in `REVIEW_AND_IMPROVEMENT_PLAN.md`.

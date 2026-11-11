# CSM Aegis

CSM Aegis is a long-only Indian-equity momentum strategy. It selects liquid, trending names with a residual-momentum and smoothness composite, then manages them through a close-based execution and risk wrapper.

**Status: research / paper-trade candidate.** It is not live-validated. Results use survivorship-biased OHLCV data and must not be used as a live-return forecast.

For a portable testing-team handoff, follow [TESTING_HANDOFF.md](TESTING_HANDOFF.md). It documents the input schemas, explicit-path command, expected v1.4 characteristics, manifests, and mandatory execution-integrity checks.

## Production configuration

`v1.4_low_dd` is the current drawdown-focused production preset. It retains v1.3's five-day-spike and two-name industry controls, then admits a fresh entry only when daily ADX(14) is at least 25 and `+DI > -DI`. All ordinary idle cash is invested in GOLDBEES through the raw-bar-validated secondary sleeve; this is an actual ETF return, **not** a risk-free-rate assumption. `v1.3` remains frozen as the equity-only, no-idle-cash-return comparator.

| Block | Rule |
|---|---|
| Universe | Price >= Rs 20; 63-day rupee-volume rank 1-1000; <= 5 circuit-locked sessions in 63 days; close above SMA-200; exclude the worst 20% by M3 single-day-spike risk. |
| Signal | `z(R1) + z(-Ulcer252)` within the eligible pool. R1 is 12-month residual momentum skipping the latest month; Ulcer rewards smoother compounders. |
| Selection | Top 20 at month-end. Existing holdings stay until rank > 40 or they leave the pool. |
| Entry filters | Reject entries more than 25% above SMA-50 or above the eligible-universe 80th percentile of five-day raw-close returns; block new entries in the high-volatility state. |
| Trend-quality gate | v1.4 only: fresh entries require ADX(14) >= 25 and bullish DMI (`+DI > -DI`). Rejected top-20 candidates do not backfill from below rank 20, matching the validated experiment. |
| Concentration | At most two names per `Industry_clean` label for new entries; unlabelled names are treated individually rather than guessed into a group. |
| Market gate | Exit all and do not enter when the equal-weight market is at/below its 120-day average. |
| Exits | Close-based -15% entry stop, -20% trailing stop, 45-day weak-position time stop, rank/pool exit, or market-gate exit; execute at the next close. |
| Sizing | 1% risk / stop distance, clamped to 3-8% per name; gross exposure capped at 100%; no leverage. |
| Execution | Next-close fills only on a raw, positive-volume, non-circuit OHLC bar; unfillable entries are cancelled and unfillable exits remain pending until a valid bar. Transaction cost is 0.3% on each executed leg; idle cash return is 0%. |

Historical v1.4 result (2007-03 through 2026-07, close fills, 0.3% per leg, ADX/DMI gate, GOLDBEES sleeve): **24.11% CAGR, 1.51 Sharpe, -24.4% max drawdown**. The matched equity-only v1.3 control has **23.09% CAGR, 1.66 Sharpe, -33.8% max drawdown**. This is a backtest result, not a target. Both use raw-bar fill validation and deferred exits; prior reports that filled at forward-filled/stale prices are superseded. See `IMPROVEMENT_LOG.md` for the decision record.

## Optional metal ETF cash sleeve

`secondary_etf="GOLDBEES"` invests ordinary idle cash in gold rather than assigning it a risk-free return. This is an actual, separately traded sleeve—not an RFR assumption—and remains opt-in while it is validated. It sweeps cash at every valid ETF close, including the cash created by market-gate, bearish, or panic periods; it is not a bear-only hedge. A stock entry sells ETF units only on a valid raw ETF bar. ETF fills require observed positive price and volume plus a non-circuit OHLC range; otherwise the cash/ETF order is deferred and recorded. The ETF sleeve is charged 0.3% per leg by default (configurable separately).

On the common 2007-03-19 to 2026-07-17 window, the raw-bar v1.3 comparison was:

| Configuration | CAGR | Sharpe | MaxDD |
|---|---:|---:|---:|
| Equity only, idle cash 0% | 23.09% | 1.66 | -33.8% |
| GOLDBEES idle-cash sleeve | 27.99% | 1.54 | -30.6% |

The sleeve improved CAGR and maximum drawdown in this first test but lowered Sharpe slightly. The existing regime-leverage, volatility-target, and correlation overlays also rebalance the sleeve faithfully: stock risk-off sales fund the ETF, while risk-on increases sell the ETF only on a valid raw ETF bar. SILVERBEES is supported only as short-history research (its data starts in 2022); it is not a production recommendation.

## Files

| File | Responsibility |
|---|---|
| `csm_aegis_strategy.py` | All strategy logic: data loading, factors, universe, ranking, selection, sizing, stops, gates, presets, and live position/exit helpers. |
| `csm_aegis_backtest.py` | Backtest booking, metrics, diagnostics, plots, output generation, and the command-line runner. |
| `test_parity.py` | Regression/parity checks against the research engine and live exit rules. |
| `test_execution_integrity.py` / `test_secondary_etf.py` | Raw-bar fill regression tests for stocks and the optional ETF sleeve. |
| `IMPROVEMENT_LOG.md` | Sequential drawdown-reduction experiments, including rejected candidates and reproduction commands. |

The first two are the complete runnable strategy package. `test_parity.py` is a verification script, not a third production component. `CSM_AEGIS_REPORT.md` is the chronological research record and can contain superseded historical configurations.

## Run

```bash
cd csm_aegis
python3 csm_aegis_backtest.py
python3 csm_aegis_backtest.py --preset v1.3  # frozen equity-only comparator
python3 csm_aegis_backtest.py --compare --stress
python3 csm_aegis_backtest.py --set top_n=15 --set stop_from_entry=0.12
python3 csm_aegis_backtest.py --preset v1.3 --set secondary_etf=GOLDBEES
python3 csm_aegis_backtest.py --preset v1.3 --set secondary_etf=SILVERBEES  # short-history research only
python3 csm_aegis_backtest.py --asof 2026-06-30
python3 csm_aegis_backtest.py --holdings my_holdings.csv
python3 test_parity.py
python3 test_execution_integrity.py
python3 test_secondary_etf.py
```

Set `CSM_AEGIS_DATA_FOLDER` if the OHLCV folder is not at the configured local default. `my_holdings.csv` requires `ticker`, `entry_date`, and `entry_price` columns.

`output/` receives the trade, rejection, deferred-order, daily, return, yearly-return, and selection files plus the run log and performance plot. A sleeve run also writes `secondary_etf_trades_*.csv`.

## Next research objective

The drawdown-reduction workstream is in [IMPROVEMENT_LOG.md](IMPROVEMENT_LOG.md). It tests one control at a time against the frozen v1.2 baseline and records both isolated and combined outcomes. `v1.3` promotes the spike and industry controls; frozen `v1.2` remains available for comparison.

Before paper trading, also resolve the existing data-quality and live-order-sheet issues recorded in `REVIEW_AND_IMPROVEMENT_PLAN.md`.

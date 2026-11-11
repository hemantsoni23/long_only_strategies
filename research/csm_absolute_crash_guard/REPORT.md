# CSM Absolute crash-guard comparison

## Decision

The tested volatility guard is **not yet a convincing replacement** for the daily SMA guard. The 21-day, 95th-percentile version gained about 0.62 percentage points of annualized return versus the SMA rule, but its maximum drawdown was 0.50 percentage points worse. Both strategies were approximately flat after the modeled costs. The 90th and 97.5th percentile alternatives had worse full-period returns and drawdowns than the SMA guard. This is an exploratory historical comparison, not evidence that any variant is ready for live deployment.

The volatility rule may still be worth investigating: the 95th-percentile variant had a better 2020–2022 annualized return than SMA (5.49% versus 4.10%); in 2023–2025 it was slightly worse (-4.94% versus -4.87%). These are slices of continuous runs, not independent flat-start tests, and are not blind holdouts.

## Results

2020-01-01 through 2025-12-31. CAGR, maximum drawdown and volatility are percentages. Sharpe uses a zero risk-free rate. Average exposure is the mean end-of-day sum of portfolio weights. Guard days and crash exits are different things: a guard may be active while no position is held.

| Daily guard | CAGR | Max drawdown | Volatility | Sharpe | Average exposure | Guard days | Crash exits |
|---|---:|---:|---:|---:|---:|---:|---:|
| Existing SMA200 | -0.48% | -37.14% | 11.38% | 0.01 | 48.25% | 231 | 50 |
| No daily crash guard | -0.79% | -43.42% | 12.79% | 0.00 | 59.16% | 0 | 0 |
| Volatility, 90th percentile | -2.73% | -42.10% | 10.26% | -0.22 | 41.12% | 328 | 88 |
| Volatility, 95th percentile | 0.14% | -37.64% | 11.49% | 0.07 | 50.87% | 126 | 71 |
| Volatility, 97.5th percentile | -1.42% | -44.54% | 12.44% | -0.05 | 56.98% | 37 | 48 |
| Volatility, 95th with 2.6% daily-volatility floor | -0.79% | -43.42% | 12.79% | 0.00 | 59.16% | 0 | 0 |

The 2.6% floor is **daily** volatility, not annualized. It never triggered in this dataset, including 2020, and therefore exactly matched no daily crash guard. The synthetic equal-weight benchmark has its own volatility scale; a floor taken from a different benchmark is not portable.

Modeled annual turnover, measured as the sum of absolute daily changes in target weights, was 31.80× for SMA and 33.55× for the 95th-percentile guard. At 0.3% per unit of turnover, that corresponds to approximately 9.54% and 10.07% of starting daily portfolio value per year in additive modeled cost drag, respectively. It is not a broker-verified cost estimate. Returns above already include this cost.

## Setup

The experiment loads the same 5,205 CSV files and 2019–2025 window as `Old_live_strategies/run_csm_absolute.py`, using its parameters, existing synthetic equal-weight universe benchmark, 0.3% one-way transaction cost, 0.3% stop slippage, zero cash return, limit-order assumptions and 10-session crash cooldown. Statistics start in 2020 after a 2019 warmup. Same selection, monthly exposure controls, stock-level trend filter, position sizing and stops are retained. The "no guard" case disables only the daily liquidation guard; monthly SMA and volatility exposure controls and stock-level trend filters still operate.

SMA baseline reproduces the backtest: on execution day D, compare D-1's benchmark close to an SMA ending D-2, using its 200-day window and 180-observation minimum. For volatility, the daily benchmark close-to-close return standard deviation uses 21 observations through D-1. The trigger compares that value to an expanding historical percentile of the same lagged volatility series, with a minimum of 126 volatility observations and no annualization. Each day's signal is known before that day's simulated close execution. The rule stays active until volatility falls below its threshold, with the same 10-day cooldown after the last active day.

The guard's trades use the existing event engine's timing and fill assumptions. A research-only change corrects a concrete omission: when a holding is fully exited, the original engine multiplies the exit-day return by the zero end-of-day weight, omitting the exit leg. The experiment uses the previous day's weight for such exits. The separate check in `test_compare.py` verifies a -10% crash-day exit is counted. This is a partial accounting repair, not a complete cash-and-shares execution simulator: reweighting, fill sequencing, stop and limit-order behavior, and stale prices require further audit.

For scale, running the original engine with the same SMA configuration produces a 43.66% CAGR and -8.70% maximum drawdown for the reporting window, versus -0.48% and -37.14% with the research exit-day correction. The two runs have the same reported turnover and average exposure; the difference comes from how exit-day returns are credited. This very large discrepancy means historical performance reported by the original engine should not be relied on without fixing and independently auditing its accounting. The corrected figures are also provisional because the repair does not address every execution issue.

## Issues to resolve before live use

- The existing edited `get_exit_signals` currently calls `self.volatility_crash_guard(benchmark_close)`, but `volatility_crash_guard` has no `self` parameter and is not declared static. An ordinary instance call raises `AttributeError: 'IndividualMomentumStrategy' object has no attribute 'dropna'`. The method also documents `benchmark_close` as a scalar, while the new guard requires a historical series. This affects the current working copy, and was not changed by the experiment.
- The actual event backtest still uses its hardcoded SMA guard, not the live method's volatility logic. A future implementation needs one explicitly timed shared signal, historical benchmark input, matching exit fills, missing-data behavior, and matching re-entry/cooldown behavior. The existing monthly SMA and volatility exposure controls must be considered separately.
- This study uses the existing synthetic benchmark and the current dataset, which may have survivorship bias and corporate-action or stale-data problems. Prior validation in this repository identified data-adjustment, delisting and execution-order issues. The benchmark includes the available dataset universe and is not necessarily a benchmark available in live trading.
- There is only a short observed history and one major pandemic crash in the reporting window. Percentile thresholds were compared on the same data; nearby parameter sensitivity is unfavorable. Treat this as model selection on historical data, not out-of-sample validation. Research on signal selection also documents the risk of overfitting: https://www.nber.org/papers/w21329.
- The backtest executes an already-known guard at the next day's close using model fills; it does not model market impact, opening execution of a prior-close signal, gaps, liquidity/circuit constraints, taxes, or guaranteed stop fills. Stress costs and execution timing, test an actual investable benchmark, validate corporate actions and delistings, then evaluate on untouched later data and in paper trading.

## Files and reproduction

- `compare.py`: source of the research signals, isolated engine patch, metrics and experiment configuration.
- `metrics.csv`, `yearly.csv`, `daily_returns.csv`, `guard_signals.csv`: numerical output. Annual slices are not independent tests.
- `test_compare.py`: signal prefix-causality and exit-day accounting checks.
- `run.log`: detailed run output. The backtest banner always says SMA200 because the research script overrides the guard after the banner; `Running ...` in the log and output filenames identify the actual variants.
- `original_accounting/metrics.csv` and `original_accounting.log`: diagnostic SMA run through the unmodified engine.

Run from the repository root:

```sh
MPLCONFIGDIR=/tmp/csm_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/csm_absolute_crash_guard/compare.py
MPLCONFIGDIR=/tmp/csm_mpl OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python3 research/csm_absolute_crash_guard/original_accounting.py
MPLCONFIGDIR=/tmp/csm_mpl OPENBLAS_NUM_THREADS=1 python3 -m unittest discover -s research/csm_absolute_crash_guard -p 'test_*.py' -v
```

The data path defaults to the runner's existing local path and may be overridden with `CSM_DATA_FOLDER`. CSV files and the source files are read from their current state, so later changes to data or production settings can change the results. Source SHA-256 at the time of this run: strategy `0127d724d81cac2fb30728e08c27fb2521fa09dda7d87a2cbe099add9ce10190`; backtest `fb6a314f08ef7cdcefa857ade63073f883d58e36149760f3e2dc6721807b8613`; runner `552fbdf5b6bc24bd0e9f5c8222bafa06a4bbf2ee4530014637a08a94dc84bc4d`.

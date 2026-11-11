**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Stage 4 — IS/OOS and regime checks

**Verdict: NOT VALIDATED.** The numerical tables below are retrospective comparisons, not blind validation; the reverse playbook split’s Calmar ratio is in the caution band and the early window fails the breadth gate. Both halves and this related strategy family have been inspected; the complete development and post-OOS-modification history is unavailable. Thus neither direction can establish a fresh untouched holdout. Stage 3 sweeps were computed separately within each historical half, but no configuration was selected or changed as a result of these runs.

| Label | Flat-start report window | Indicator warmup |
| --- | --- | --- |
| Early reference | 2005-01-01 to 2014-12-31 | 450 calendar days |
| Late reference | 2015-01-01 to 2025-12-31 | 450 calendar days |
| Playbook early | 2001-01-01 to 2012-12-31 | Up to 450 calendar days, limited by actual data |
| Playbook late | 2013-01-01 to 2026-10-30 | 450 calendar days |
| Full informational | 2002-01-01 to 2025-12-31 | Up to 450 calendar days, limited by actual data |

The position state is reset at the last month-end before each reporting window, so there are no warmup trades; actual first-entry dates are below. Stock-level indicators warm up before reporting. The two-month rebalance phase is anchored to each reset window.

## Breadth and IC coverage

| window | months | median | mean | below8_pct | below30_pct |
| --- | --- | --- | --- | --- | --- |
| early | 120 | 126.500 | 149.917 | 9.167 | 20.833 |
| late | 132 | 183.500 | 209.280 | 0.758 | 4.545 |
| playbook_early | 144 | 57.500 | 92.931 | 34.028 | 45.833 |
| playbook_late | 166 | 183.000 | 210.127 | 0.602 | 3.614 |

Breadth includes calendar month-ends in each report window, including months with no eligible names; IC additionally requires observable forward outcomes.

## Flat-start vs source-main window convention

| run | cagr_pct | sharpe | calmar | maxdd_pct | prestart_entries | prestart_positions_crossing_boundary | reported_trade_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source main convention (pre-start book allowed) | 31.553 | 1.724 | 1.640 | -19.243 | 16 | 6 | 1251 |
| flat-start comparison used in reports | 32.139 | 1.840 | 1.523 | -21.108 | 0 | 0 | 1280 |

Source main allows trading during warmup, so its report window can start with an existing portfolio; its trade log excludes positions entered before the window. The split tests here reset selection and holdings at each boundary.

## Baseline scorecards

| Window | First entry | CAGR % | Sharpe | Sortino | Max DD % | Calmar | Vol % | Exposure % | Turnover %/yr | Trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 2005-01-03 | 45.237 | 2.303 | 3.594 | -29.981 | 1.509 | 17.074 | 80.617 | 699.803 | 1061 |
| late | 2015-01-01 | 32.139 | 1.840 | 2.765 | -21.108 | 1.523 | 16.086 | 79.550 | 767.624 | 1280 |
| playbook_early | 2001-03-01 | 30.533 | 1.895 | 2.957 | -29.981 | 1.018 | 14.772 | 60.077 | 511.895 | 933 |
| playbook_late | 2013-01-01 | 36.544 | 2.041 | 3.109 | -21.108 | 1.731 | 16.153 | 79.710 | 764.035 | 1596 |
| full | 2002-02-01 | 36.195 | 2.037 | 3.080 | -23.935 | 1.512 | 15.997 | 72.575 | 647.695 | 2347 |

Full-window metrics are descriptive only, never a promotion gate. Stage 4 compares values with risk-free rate 0.

### Trade scorecard

| Window | Win rate % | Profit factor (trade %) | Payoff ratio | Avg hold days |
| --- | --- | --- | --- | --- |
| early | 50.330 | 2.598 | 2.564 | 40.902 |
| late | 47.422 | 2.048 | 2.271 | 37.127 |
| playbook_early | 49.196 | 2.512 | 2.594 | 41.622 |
| playbook_late | 48.997 | 2.224 | 2.315 | 37.437 |
| full | 49.127 | 2.469 | 2.556 | 39.932 |

Trade win rate and profit factor use the engine’s per-trade percentage-return convention, not dollar-weighted profit factor. Dollar-weighted profit factor, benchmark beta and alpha are unavailable because no verified point-in-time market benchmark or position-level realized P&L series was supplied.

## Full-sample calendar years

| Year | Return % | Sharpe | Within-year max DD % |
| --- | --- | --- | --- |
| 2002.000 | 1.452 | 0.648 | -1.393 |
| 2003.000 | 9.025 | 3.143 | -1.785 |
| 2004.000 | 76.699 | 3.722 | -11.499 |
| 2005.000 | 83.711 | 3.429 | -13.074 |
| 2006.000 | 57.270 | 3.052 | -16.553 |
| 2007.000 | 91.365 | 3.531 | -9.750 |
| 2008.000 | -17.033 | -0.896 | -22.872 |
| 2009.000 | 68.041 | 3.022 | -9.796 |
| 2010.000 | 43.934 | 2.713 | -9.156 |
| 2011.000 | -13.304 | -1.002 | -16.167 |
| 2012.000 | 63.343 | 4.211 | -5.779 |
| 2013.000 | 7.743 | 0.731 | -17.598 |
| 2014.000 | 143.769 | 4.758 | -6.715 |
| 2015.000 | 54.872 | 2.769 | -9.945 |
| 2016.000 | 47.652 | 2.308 | -17.207 |
| 2017.000 | 54.603 | 3.004 | -6.676 |
| 2018.000 | 6.260 | 0.432 | -17.716 |
| 2019.000 | -2.388 | -0.172 | -13.385 |
| 2020.000 | 70.790 | 3.057 | -10.648 |
| 2021.000 | 70.228 | 3.030 | -7.462 |
| 2022.000 | 10.246 | 0.673 | -19.243 |
| 2023.000 | 48.278 | 2.960 | -11.771 |
| 2024.000 | 23.425 | 1.101 | -14.418 |
| 2025.000 | -4.451 | -0.183 | -15.981 |

These are informational annual returns from the continuously run full-sample portfolio; within-year drawdown is reset at each year’s first day.

## Reference split A: 2005–2014 IS → 2015–2025 OOS

| Metric | Result | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 0.799 | ≥0.60 | PASS |
| Calmar OOS/IS | 1.009 | ≥0.60 | PASS |
| CAGR OOS/IS | 0.710 | ≥0.50 | PASS |
| Max DD OOS/IS | 0.704 | ≤1.50 | PASS |
| OOS Sharpe | 1.840 | >0 | PASS |
| OOS L0 3m IC NW-t | 2.402 | ≥1.50 | PASS |
| OOS L3 3m IC NW-t | 1.603 | ≥1.50 | PASS |
| Δ Sharpe (OOS − IS) | -0.463 | informational | — |
| Δ Calmar (OOS − IS) | 0.014 | informational | — |

## Reference split B: 2015–2025 IS → 2005–2014 OOS

| Metric | Result | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 1.251 | ≥0.60 | PASS |
| Calmar OOS/IS | 0.991 | ≥0.60 | PASS |
| CAGR OOS/IS | 1.408 | ≥0.50 | PASS |
| Max DD OOS/IS | 1.420 | ≤1.50 | PASS |
| OOS Sharpe | 2.303 | >0 | PASS |
| OOS L0 3m IC NW-t | 3.861 | ≥1.50 | PASS |
| OOS L3 3m IC NW-t | 4.416 | ≥1.50 | PASS |
| Δ Sharpe (OOS − IS) | 0.463 | informational | — |
| Δ Calmar (OOS − IS) | -0.014 | informational | — |

## Playbook split A: 2001–2012 IS → 2013–latest OOS

| Metric | Result | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 1.077 | ≥0.60 | PASS |
| Calmar OOS/IS | 1.700 | ≥0.60 | PASS |
| CAGR OOS/IS | 1.197 | ≥0.50 | PASS |
| Max DD OOS/IS | 0.704 | ≤1.50 | PASS |
| OOS Sharpe | 2.041 | >0 | PASS |
| OOS L0 3m IC NW-t | 2.831 | ≥1.50 | PASS |
| OOS L3 3m IC NW-t | 2.211 | ≥1.50 | PASS |
| Δ Sharpe (OOS − IS) | 0.146 | informational | — |
| Δ Calmar (OOS − IS) | 0.713 | informational | — |

## Playbook split B: 2013–latest IS → 2001–2012 OOS

| Metric | Result | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 0.928 | ≥0.60 | PASS |
| Calmar OOS/IS | 0.588 | ≥0.60 | CAUTION |
| CAGR OOS/IS | 0.836 | ≥0.50 | PASS |
| Max DD OOS/IS | 1.420 | ≤1.50 | PASS |
| OOS Sharpe | 1.895 | >0 | PASS |
| OOS L0 3m IC NW-t | 3.025 | ≥1.50 | PASS |
| OOS L3 3m IC NW-t | 4.274 | ≥1.50 | PASS |
| Δ Sharpe (OOS − IS) | -0.146 | informational | — |
| Δ Calmar (OOS − IS) | -0.713 | informational | — |

All numerical gates must pass in both directions; results remain invalid as formal promotion evidence when the implementation has unresolved execution lookahead or the holdout is not blind. Ratio denominators are positive here; Max DD uses absolute depth. Both windows include stress regimes: early includes 2008, and late includes 2018, 2020 and 2022. Early data coverage and IC breadth should be judged from the actual sample, not assumed from calendar years.

Playbook-window parameter and ablation results: [2001–2012](evidence/playbook_early_sweep_cells.csv), [2013–latest](evidence/playbook_late_sweep_cells.csv). In a genuine bidirectional process, each direction also requires a separately frozen IS configuration and a fresh OOS record; these simulations use the same user-provided default throughout.

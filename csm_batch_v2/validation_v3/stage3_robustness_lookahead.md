# Stage 3 — Lookahead, year concentration and parameter robustness

### Point-in-time prefix tests

| Data truncated after | Factor availability mismatches | Max factor difference | Position cells changed | Max position difference | Max ATR difference | Max regime difference | Result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2018-12-31 | 0 | 0.000000000000 | 0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | PASS |
| 2020-03-31 | 0 | 0.000000000000 | 0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | PASS |
| 2022-12-30 | 0 | 0.000000000000 | 0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | PASS |
| 2024-12-31 | 0 | 0.000000000000 | 0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | PASS |
| 2025-06-30 | 0 | 0.000000000000 | 0 | 0.000000000000 | 0.000000000000 | 0.000000000000 | PASS |

### Execution-order causality test

| Scenario: same scheduled open, same prior information | Intraday low | Exit reason | Exit fill | Next-day weight |
| --- | --- | --- | --- | --- |
| No later stop breach | 90 | REBAL_EXIT | 100.00 | 0.50 |
| Later stop breach | 80 | HARD_STOP_HIT | 84.75 | 0.00 |

| Test | Result | Meaning |
| --- | --- | --- |
| Prefix signal / positions / ATR / regime | PASS | Truncating future history should not change earlier values |
| Scheduled-open exit vs later intraday stop | FAIL | Changing the later low changes the earlier execution path and next-day re-entry. |
| Historical stop exits on dates with zero target at open | 16 / 1258 | Candidate conflicts: engine checks the stop before the scheduled rebalance exit. |
| Exit-day accounting | User convention | Separate from the timing and cooldown test. |

### Remove-one-year sensitivity — fixed baseline daily returns

| Window | Removed year | That year return | Remaining-days Sharpe | Δ Sharpe | Remaining Calmar | Remaining max DD |
| --- | --- | --- | --- | --- | --- | --- |
| 2005–2014 | 2005 | 53.11% | 2.42 | -0.04 | 1.22 | -27.66% |
| 2005–2014 | 2006 | 37.85% | 2.45 | -0.01 | 1.28 | -27.66% |
| 2005–2014 | 2007 | 71.98% | 2.34 | -0.12 | 1.16 | -27.66% |
| 2005–2014 | 2008 | -21.04% | 2.87 | 0.41 | 3.29 | -13.40% |
| 2005–2014 | 2009 | 74.54% | 2.32 | -0.15 | 1.14 | -27.81% |
| 2005–2014 | 2010 | 32.05% | 2.47 | 0.00 | 1.30 | -27.66% |
| 2005–2014 | 2011 | -4.19% | 2.68 | 0.21 | 1.48 | -27.66% |
| 2005–2014 | 2012 | 38.52% | 2.38 | -0.08 | 1.28 | -27.66% |
| 2005–2014 | 2013 | 9.73% | 2.56 | 0.09 | 1.41 | -27.66% |
| 2005–2014 | 2014 | 110.09% | 2.11 | -0.35 | 1.05 | -27.66% |
| 2015–2025 | 2015 | 19.24% | 1.68 | 0.04 | 1.35 | -17.00% |
| 2015–2025 | 2016 | 30.43% | 1.62 | -0.03 | 1.29 | -17.00% |
| 2015–2025 | 2017 | 42.83% | 1.51 | -0.13 | 1.22 | -17.00% |
| 2015–2025 | 2018 | -3.23% | 1.80 | 0.16 | 1.51 | -17.00% |
| 2015–2025 | 2019 | 7.06% | 1.69 | 0.04 | 1.43 | -17.00% |
| 2015–2025 | 2020 | 42.67% | 1.53 | -0.11 | 1.22 | -17.00% |
| 2015–2025 | 2021 | 65.95% | 1.43 | -0.22 | 1.11 | -17.00% |
| 2015–2025 | 2022 | 4.70% | 1.80 | 0.15 | 1.53 | -16.15% |
| 2015–2025 | 2023 | 51.51% | 1.48 | -0.17 | 1.18 | -17.00% |
| 2015–2025 | 2024 | 17.36% | 1.71 | 0.06 | 1.37 | -17.00% |
| 2015–2025 | 2025 | -9.71% | 1.86 | 0.21 | 1.56 | -17.00% |

| Year concentration | 2005–2014 | 2015–2025 | Interpretation |
| --- | --- | --- | --- |
| Largest contribution year | 2014 | 2021 | Annual log-return contribution |
| Top year / total signed log growth | 24.70% | 22.87% | Diagnostic |
| Top two years / total signed log growth | 43.22% | 41.63% | Negative years can make shares exceed 100% |
| Remove-one-year method | Fixed daily return series | Fixed daily return series | Not a re-run with history removed |

### Parameter sensitivity — Sharpe

| Parameter setting | 2005–2014 | 2015–2025 |
| --- | --- | --- |
| lookback_7 | 2.51 | 1.61 |
| lookback_10 | 2.68 | 1.76 |
| lookback_12 | 2.46 | 1.65 |
| lookback_14 | 2.44 | 1.57 |
| lookback_17 | 2.63 | 1.79 |
| rebalance_1 | 2.45 | 1.59 |
| rebalance_2 | 2.46 | 1.65 |
| rebalance_3 | 2.51 | 1.77 |
| positions_18 | 2.35 | 1.51 |
| positions_24 | 2.49 | 1.65 |
| positions_30 | 2.46 | 1.65 |
| positions_36 | 2.46 | 1.73 |
| positions_42 | 2.47 | 0.66 |
| stop_0.09 | 2.57 | 1.99 |
| stop_0.12 | 2.50 | 1.80 |
| stop_0.15 | 2.46 | 1.65 |
| stop_0.18 | 2.39 | 1.59 |
| stop_0.21 | 2.36 | 1.57 |
| regime_-0.06 | 2.43 | 1.63 |
| regime_-0.08 | 2.44 | 1.62 |
| regime_-0.10 | 2.46 | 1.65 |
| regime_-0.12 | 2.45 | 1.68 |
| regime_-0.14 | 2.46 | 1.69 |

| Window | Approximate ±20% test | Sharpe range | Bar | Result |
| --- | --- | --- | --- | --- |
| 2005–2014 | Lookback 10 vs 14 months | 0.24 | ≤0.40 | PASS |
| 2005–2014 | Positions 24 vs 36 | 0.03 | ≤0.40 | PASS |
| 2005–2014 | Hard stop 12% vs 18% | 0.11 | ≤0.40 | PASS |
| 2005–2014 | Regime cutoff −8% vs −12% | 0.01 | ≤0.40 | PASS |
| 2005–2014 | 2-month rebalance ±20% | N/A: rounds to 2 months | 5 points requested | INCOMPLETE |
| 2015–2025 | Lookback 10 vs 14 months | 0.19 | ≤0.40 | PASS |
| 2015–2025 | Positions 24 vs 36 | 0.08 | ≤0.40 | PASS |
| 2015–2025 | Hard stop 12% vs 18% | 0.21 | ≤0.40 | PASS |
| 2015–2025 | Regime cutoff −8% vs −12% | 0.06 | ≤0.40 | PASS |
| 2015–2025 | 2-month rebalance ±20% | N/A: rounds to 2 months | 5 points requested | INCOMPLETE |

| Window | Approximate ±40% stress | Sharpe range | Interpretation |
| --- | --- | --- | --- |
| 2005–2014 | Lookback 7 vs 17 months | 0.12 | Stress; ±20% gate is reported separately |
| 2005–2014 | Positions 18 vs 42 | 0.12 | Stress; ±20% gate is reported separately |
| 2005–2014 | Hard stop 9% vs 21% | 0.21 | Stress; ±20% gate is reported separately |
| 2005–2014 | Regime cutoff −6% vs −14% | 0.03 | Stress; ±20% gate is reported separately |
| 2015–2025 | Lookback 7 vs 17 months | 0.17 | Stress; ±20% gate is reported separately |
| 2015–2025 | Positions 18 vs 42 | 0.85 | Stress; ±20% gate is reported separately |
| 2015–2025 | Hard stop 9% vs 21% | 0.42 | Stress; ±20% gate is reported separately |
| 2015–2025 | Regime cutoff −6% vs −14% | 0.05 | Stress; ±20% gate is reported separately |

### 2005–2014 ablation — value (relative change vs baseline)

| Cell | Sharpe | Calmar | Std 12m return | Avg DD depth % | One-way turnover %/yr | Regression flags |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 2.46 (+0.0%) | 1.27 (+0.0%) | 0.29 (+0.0%) | 5.22 (+0.0%) | 642.89 (+0.0%) | None |
| ablate_rank_exit | 2.51 (+1.7%) | 1.30 (+2.7%) | 0.30 (+1.6%) | 5.34 (+2.2%) | 611.84 (-4.8%) | None |
| ablate_vol_stop | 2.07 (-16.1%) | 1.10 (-13.7%) | 0.31 (+6.2%) | 6.15 (+17.7%) | 505.89 (-21.3%) | sharpe |
| ablate_bear_exposure | 2.28 (-7.4%) | 1.06 (-16.4%) | 0.30 (+4.9%) | 5.71 (+9.4%) | 682.96 (+6.2%) | calmar |
| ablate_vol_target | 2.45 (-0.5%) | 1.22 (-4.1%) | 0.29 (+0.7%) | 5.26 (+0.7%) | 641.74 (-0.2%) | None |
| ablate_corr_guard | 2.46 (-0.0%) | 1.27 (-0.0%) | 0.29 (-0.0%) | 5.23 (+0.0%) | 642.69 (-0.0%) | None |
| ablate_positive_momentum | 2.45 (-0.4%) | 1.24 (-2.2%) | 0.29 (-0.3%) | 5.22 (-0.2%) | 639.76 (-0.5%) | None |

### 2015–2025 ablation — value (relative change vs baseline)

| Cell | Sharpe | Calmar | Std 12m return | Avg DD depth % | One-way turnover %/yr | Regression flags |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 1.65 (+0.0%) | 1.31 (+0.0%) | 0.26 (+0.0%) | 6.36 (+0.0%) | 718.74 (+0.0%) | None |
| ablate_rank_exit | 1.68 (+2.1%) | 1.33 (+1.6%) | 0.25 (-3.5%) | 6.19 (-2.6%) | 691.21 (-3.8%) | None |
| ablate_vol_stop | 1.07 (-35.0%) | 0.71 (-45.6%) | 0.28 (+8.3%) | 7.42 (+16.8%) | 594.76 (-17.2%) | sharpe, calmar |
| ablate_bear_exposure | 1.78 (+8.3%) | 1.51 (+15.0%) | 0.27 (+3.4%) | 6.28 (-1.2%) | 709.78 (-1.2%) | None |
| ablate_vol_target | 1.65 (-0.1%) | 1.31 (-0.5%) | 0.26 (+0.0%) | 6.36 (+0.0%) | 718.69 (-0.0%) | None |
| ablate_corr_guard | 1.65 (+0.0%) | 1.31 (+0.0%) | 0.26 (+0.0%) | 6.36 (+0.0%) | 718.74 (+0.0%) | None |
| ablate_positive_momentum | 1.64 (-0.6%) | 1.30 (-0.6%) | 0.26 (-0.2%) | 6.37 (+0.2%) | 718.75 (+0.0%) | None |

### Price anomaly sensitivity: omit TIL in memory

| Cell | Source | CAGR | Sharpe | Calmar | Max DD |
| --- | --- | --- | --- | --- | --- |
| band_500_1000 | all source tickers | 42.15% | 0.62 | 2.52 | -16.74% |
| band_500_1000 | TIL excluded | 27.56% | 1.88 | 1.65 | -16.74% |
| positions_36 | all source tickers | 22.95% | 1.73 | 1.43 | -16.07% |
| positions_36 | TIL excluded | 22.95% | 1.73 | 1.43 | -16.07% |
| positions_42 | all source tickers | 32.89% | 0.66 | 2.09 | -15.70% |
| positions_42 | TIL excluded | 21.67% | 1.69 | 1.38 | -15.70% |

| Cell | Date | Ticker | Previous close → close | Stock-day return | Portfolio-day return |
| --- | --- | --- | --- | --- | --- |
| late_probe_band_500_1000 | 2017-12-07 | TIL | 2.85 → 146.50 | 5040.35% | 253.73% |
| late_probe_band_500_1000 | 2017-12-06 | TIL | 147.00 → 2.85 | -98.06% | -5.74% |
| late_probe_positions_42 | 2017-12-07 | TIL | 2.85 → 146.50 | 5040.35% | 178.30% |
| late_probe_positions_42 | 2017-12-06 | TIL | 147.00 → 2.85 | -98.06% | -4.16% |

| Method | Interpretation |
| --- | --- |
| Outlier sensitivity | TIL removed from the in-memory panel for all history; ranks, benchmark and trades are recomputed. It is not an adjusted-data backtest. |
| Stop-order test | The scheduled open exit is identical; only the later intraday low changes. This can alter exit reason and stop cooldown. |
| Prefix tests | Passing finite cutoffs is evidence, not proof for every date or execution path. |
| Parameter grid | Lookback 7/10/12/14/17 months; positions 18/24/30/36/42; hard stop 9/12/15/18/21%; regime cutoff −6/−8/−10/−12/−14%. |
| Rebalance | 1/2/3 months; ±20% cannot produce five distinct integer-month settings. |
| Ablation limits | Sharpe/Calmar regression ≤15%; 12m stability and average DD depth ≤20%; turnover ≤25%. |
| Selection | Baseline was frozen; no parameter winner or ablation was adopted. |

[Synthetic timing test](evidence/test_open_timing.py) · [Prefix results](evidence/prefix_tests.csv) · [Stop/open observations](evidence/stop_open_ordering.csv) · [Backtest engine](../csm_stock_backtest.py#L350)

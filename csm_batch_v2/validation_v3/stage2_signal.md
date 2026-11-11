# Stage 2 — Signal IC, accuracy and decay

2015–2025; 12-month and 6-month volatility-normalized momentum, 1-month lag. Returns are raw close-to-close; overlapping horizons use Newey–West lag equal to horizon.

| 3m signal rung | Months | Mean IC | ICIR | t-stat | NW-t | Positive IC months | Avg names |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L0_long | 129 | 0.0258 | 0.331 | 3.76 | 2.58 | 65.89% | 2572 |
| L0_short | 129 | 0.0186 | 0.260 | 2.96 | 2.09 | 59.69% | 2747 |
| L0_composite | 129 | 0.0234 | 0.303 | 3.44 | 2.41 | 61.24% | 2570 |
| L1_price | 129 | 0.0337 | 0.422 | 4.80 | 3.47 | 72.09% | 2130 |
| L2_liquidity_circuit_age | 129 | 0.0579 | 0.530 | 6.02 | 4.26 | 72.09% | 896 |
| L3_tradeable | 129 | 0.0369 | 0.364 | 4.14 | 2.91 | 62.02% | 504 |
| L4_positive_momentum | 129 | 0.0244 | 0.278 | 3.16 | 2.35 | 61.24% | 419 |
| L5_top30 | 129 | -0.0064 | -0.033 | -0.38 | -0.33 | 47.29% | 30 |

| Horizon | Months | Mean IC | ICIR | t-stat | NW-t | Positive IC months | Top-30 above pool median | Top-30 positive return | Top-30 excess / pool |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | 131 | 0.0352 | 0.358 | 4.10 | 4.16 | 64.12% | 51.79% | 52.58% | 0.16 pp |
| 3m | 129 | 0.0369 | 0.364 | 4.14 | 2.91 | 62.02% | 51.94% | 54.11% | 0.37 pp |
| 6m | 126 | 0.0329 | 0.328 | 3.68 | 2.02 | 65.87% | 50.82% | 56.48% | 0.84 pp |
| 12m | 120 | 0.0023 | 0.024 | 0.26 | 0.13 | 53.33% | 48.60% | 56.57% | -2.78 pp |

| Horizon | Q1 | Q2 | Q3 | Q4 | Q5 | Increasing pairs | Q5−Q1 | Spread NW-t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1m | 0.97% | 2.54% | 1.56% | 1.99% | 2.02% | 3/4 | 1.05 pp | 3.62 |
| 3m | 3.98% | 5.98% | 5.06% | 5.93% | 6.08% | 3/4 | 2.10 pp | 2.98 |
| 6m | 9.24% | 10.89% | 11.59% | 12.24% | 12.70% | 4/4 | 3.46 pp | 2.56 |
| 12m | 22.39% | 26.03% | 25.20% | 24.95% | 24.42% | 1/4 | 2.03 pp | 0.80 |

### Accuracy

| Three-month accuracy measure | Measured | Definition |
| --- | --- | --- |
| Top-30 stocks above pool median | 51.94% | Mean within-month fraction |
| Top-30 stocks with positive return | 54.11% | Mean within-month fraction |
| Top-30 return − pool mean | 0.37 pp | NW-t 0.65; 129 months |
| Average selected names with forward data | 29.91 | Out of target 30 |

### Is the signal decaying over time?

| Time-decay check | Measured | Assessment |
| --- | --- | --- |
| Prior 2015–2022 mean 3m IC | 0.0377 | 96 months |
| Recent 2023–2025 mean 3m IC | 0.0347 | 33 months; NW-t 1.79 |
| Recent minus prior | -0.0030 | HAC t-stat -0.12; NO SIGNIFICANT CHANGE / INCONCLUSIVE |
| 2024–2025 post-hoc IC | 0.0010 | 21 months vs 2021–2023 IC 0.0565 |
| Post-hoc 2024–2025 change | -0.0555 | HAC t-stat -2.19; unadjusted exploratory comparison |
| Top two years share of signed IC | 60.65% | Playbook caution >50% |

| Fixed 3m-IC period | Months | Mean IC | ICIR | NW-t | Positive IC | Top-30 above median | Top-30 excess |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-2017 | 36 | 0.0157 | 0.231 | 1.20 | 55.56% | 49.50% | 0.58 pp |
| 2018-2020 | 36 | 0.0595 | 0.420 | 1.77 | 69.44% | 56.99% | 1.15 pp |
| 2021-2023 | 36 | 0.0565 | 0.637 | 2.67 | 69.44% | 51.30% | -0.19 pp |
| 2024-2025 | 21 | 0.0010 | 0.015 | 0.07 | 47.62% | 48.57% | -0.36 pp |

### Three-month IC and accuracy by year

| Year | Months | 3m IC | NW-t | Positive IC | Top-30 above median | Top-30 excess |
| --- | --- | --- | --- | --- | --- | --- |
| 2015 | 12 | 0.0068 | 0.23 | 41.67% | 49.72% | -0.70 pp |
| 2016 | 12 | 0.0138 | 1.03 | 58.33% | 45.99% | -1.04 pp |
| 2017 | 12 | 0.0266 | 1.36 | 66.67% | 52.78% | 3.49 pp |
| 2018 | 12 | 0.0733 | 3.19 | 83.33% | 56.84% | 0.55 pp |
| 2019 | 12 | 0.1334 | 3.25 | 83.33% | 60.67% | 1.75 pp |
| 2020 | 12 | -0.0282 | -0.59 | 41.67% | 53.46% | 1.15 pp |
| 2021 | 12 | 0.1075 | 7.40 | 91.67% | 55.00% | 1.00 pp |
| 2022 | 12 | -0.0315 | -1.83 | 16.67% | 42.78% | -3.11 pp |
| 2023 | 12 | 0.0936 | 7.02 | 100.00% | 56.11% | 1.54 pp |
| 2024 | 12 | 0.0053 | 0.27 | 41.67% | 49.17% | 0.01 pp |
| 2025 | 9 | -0.0047 | -0.21 | 55.56% | 47.78% | -0.85 pp |

| Signal limitation | Measured / definition |
| --- | --- |
| Value-weighted vs equal-weighted IC | 0.0381 vs 0.0369; weighted by traded value, not market cap |
| Raw vs forward-filled 3m IC | 0.0369 vs 0.0368; 17 added symbol-months; delistings not verified |
| Accuracy definition | The top-30 current factor ranks passing the positive-momentum gate are compared with that month’s L3 median; not executed holdings, hysteresis or after-cost returns. |
| Time-decay test | 2023–2025 vs 2015–2022 was specified before the run. The 2024–2025 vs 2021–2023 test was added after inspecting the chunks; its t-stat is unadjusted for multiple comparisons. |
| Year concentration | Top two annual signed IC sums divided by all signed IC; negative years can make the share exceed 100%. |
| Lookahead | See Stage 3 for point-in-time and execution-order tests. |
| Yearly statistics | Each annual NW-t uses at most 12 monthly observations and is noisy. |
| Data bias | Raw prices and unknown delisting coverage may distort IC and accuracy. |

[Signal statistics](evidence/signal_late_summary.csv) · [Monthly IC](evidence/signal_late_series.csv) · [Recent-decay check](evidence/signal_recent_posthoc.csv)

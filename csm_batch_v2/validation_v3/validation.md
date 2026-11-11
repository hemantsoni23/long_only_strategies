# CSM Batch v2 validation summary

**Overall verdict: NOT VALIDATED for live use.** This is a fresh historical replay of the existing source and data using the Aegis report structure. The universe, signal, robustness, split and exit numbers below are descriptive; the data and previously viewed holdouts limit promotion claims. The exit-day accounting convention remains as requested.

| Test | Verdict | Key result | Report |
| --- | --- | --- | --- |
| 1. Universe sweep | CAUTION | Core Sharpe range early/late 0.42/0.32; Calmar 0.27/0.39 | [Details](stage1_universe.md) |
| 2. Signal / accuracy | PASS basic IC / quantile caution | L0/L3 NW-t 2.41 / 2.91; monotone 3/4; top-30 above median 51.94% | [Details](stage2_signal.md) |
| 2. Signal time decay | RECENT WEAKNESS / EXPLORATORY | 2024–2025 IC 0.0010 vs 2021–2023 0.0565; post-hoc HAC t -2.19 | [Details](stage2_signal.md) |
| 3. Lookahead | FAIL | Synthetic scheduled-open ordering fails; 16 real stop exits occurred on dates with zero opening target | [Details](stage3_robustness_lookahead.md) |
| 3. Parameter sensitivity | PASS tested / cadence incomplete | ±20% Sharpe range 0.08; ±40% range 0.85; TIL sensitivity measured | [Details](stage3_robustness_lookahead.md) |
| 4. Bidirectional split | FAIL / NOT BLIND | Δ Sharpe -0.82; reverse DD ratio 1.63× | [Details](stage4_is_oos.md) |
| 5. Exit rules | DIAGNOSTIC | VOL_STOP mean 20/60d excess 1.22%; 2200 exits; same-date rotation proxy | [Details](stage5_exits.md) |

## Universe sweep: 2015–2025

| Liquidity rank | CAGR | Sharpe | Δ Sharpe vs 1–1000 | Max DD | Calmar | Δ Calmar vs 1–1000 | 3m IC NW-t | Median pool | Months pool <30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 15.49% | 1.25 | -0.39 | -16.72% | 0.93 | -0.39 | 1.94 | 61 | 8.33% |
| 1–250 | 20.90% | 1.56 | -0.09 | -16.79% | 1.24 | -0.07 | 2.54 | 145 | 0.76% |
| 1–500 | 21.59% | 1.64 | -0.01 | -17.81% | 1.21 | -0.10 | 3.25 | 278 | 0.00% |
| 1–750 | 25.24% | 1.82 | 0.18 | -16.60% | 1.52 | 0.21 | 2.98 | 396 | 0.00% |
| 1–1000 | 22.31% | 1.65 | 0.00 | -17.00% | 1.31 | 0.00 | 2.91 | 504 | 0.00% |
| 1–1500 | 25.65% | 1.88 | 0.23 | -15.96% | 1.61 | 0.29 | 2.72 | 686 | 0.00% |
| 501–1000 | 42.15% | 0.62 | -1.03 | -16.74% | 2.52 | 1.21 | 1.30 | 234 | 2.27% |
| 1001–1500 | 32.54% | 2.29 | 0.65 | -17.95% | 1.81 | 0.50 | 1.86 | 164 | 5.30% |
| 1001–2000 | 33.20% | 2.35 | 0.70 | -20.29% | 1.64 | 0.32 | 2.68 | 240 | 3.03% |

| Core 1–250 through 1–1500 | Measured range | Pass / caution / major | Result |
| --- | --- | --- | --- |
| Sharpe | 0.32 | ≤0.35 / ≤0.6 / >0.6 | PASS |
| Calmar | 0.39 | ≤0.5 / ≤0.9 / >0.9 | PASS |
| CAGR (pp) | 4.75 | ≤8 / ≤15 / >15 | PASS |
| Max DD (pp) | 1.85 | ≤10 / ≤18 / >18 | PASS |
| Any core Sharpe ≤0 | 0 | 0 | PASS |

The 501–1000 band includes the anomalous TIL observations: its raw Sharpe is 0.62; removing TIL from an in-memory rerun changes it to 1.88. This is a sensitivity test, not a corrected dataset.

| 1–1000 cost / leg | CAGR | Sharpe | Max DD | Calmar |
| --- | --- | --- | --- | --- |
| 0.30% | 22.31% | 1.65 | -17.00% | 1.31 |
| 0.60% | 17.13% | 1.29 | -19.48% | 0.88 |
| 0.90% | 12.16% | 0.95 | -23.45% | 0.52 |

## Independent IS/OOS comparison

| Window | CAGR | Sharpe | Calmar | Max DD | Trade win | Profit factor | One-way turnover / yr | First entry |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| IS 2005–2014 | 35.11% | 2.46 | 1.27 | -27.66% | 51.04% | 2.48 | 6.43× | 2005-01-03 |
| OOS 2015–2025 | 22.31% | 1.65 | 1.31 | -17.00% | 47.14% | 2.04 | 7.19× | 2015-01-01 |
| Full 2002–2025 | 27.75% | 1.95 | 1.00 | -27.66% | 48.97% | 2.42 | 6.19× | 2002-01-01 |

| Direction | IS Sharpe | OOS Sharpe | Δ Sharpe | IS Calmar | OOS Calmar | Δ Calmar |
| --- | --- | --- | --- | --- | --- | --- |
| A: early → late | 2.46 | 1.65 | -0.82 | 1.27 | 1.31 | 0.04 |
| B: late → early | 1.65 | 2.46 | 0.82 | 1.31 | 1.27 | -0.04 |

| Direction | Metric | Measured | Playbook bar | Result |
| --- | --- | --- | --- | --- |
| A: early → late | Sharpe OOS / IS | 0.669 | ≥0.60 | PASS |
| A: early → late | Calmar OOS / IS | 1.034 | ≥0.60 | PASS |
| A: early → late | CAGR OOS / IS | 0.635 | ≥0.50 | PASS |
| A: early → late | Max DD OOS / IS | 0.614 | ≤1.50 | PASS |
| A: early → late | OOS Sharpe | 1.647 | >0 | PASS |
| A: early → late | OOS L0 3m NW-t | 2.414 | ≥1.50 | PASS |
| A: early → late | OOS L3 3m NW-t | 2.914 | ≥1.50 | PASS |
| B: late → early | Sharpe OOS / IS | 1.495 | ≥0.60 | PASS |
| B: late → early | Calmar OOS / IS | 0.967 | ≥0.60 | PASS |
| B: late → early | CAGR OOS / IS | 1.574 | ≥0.50 | PASS |
| B: late → early | Max DD OOS / IS | 1.628 | ≤1.50 | FAIL |
| B: late → early | OOS Sharpe | 2.463 | >0 | PASS |
| B: late → early | OOS L0 3m NW-t | 3.859 | ≥1.50 | PASS |
| B: late → early | OOS L3 3m NW-t | 3.404 | ≥1.50 | PASS |

The two windows are separate flat-start backtests with indicator warmup; the late window includes 2018, 2020 and 2022. Both periods have previously been viewed, so the comparisons are not blind. [Full split details](stage4_is_oos.md).

## Signal diagnostics: 2015–2025

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

| Three-month accuracy measure | Measured | Definition |
| --- | --- | --- |
| Top-30 stocks above pool median | 51.94% | Mean within-month fraction |
| Top-30 stocks with positive return | 54.11% | Mean within-month fraction |
| Top-30 return − pool mean | 0.37 pp | NW-t 0.65; 129 months |
| Average selected names with forward data | 29.91 | Out of target 30 |

| Time-decay check | Measured | Assessment |
| --- | --- | --- |
| Prior 2015–2022 mean 3m IC | 0.0377 | 96 months |
| Recent 2023–2025 mean 3m IC | 0.0347 | 33 months; NW-t 1.79 |
| Recent minus prior | -0.0030 | HAC t-stat -0.12; NO SIGNIFICANT CHANGE / INCONCLUSIVE |
| 2024–2025 post-hoc IC | 0.0010 | 21 months vs 2021–2023 IC 0.0565 |
| Post-hoc 2024–2025 change | -0.0555 | HAC t-stat -2.19; unadjusted exploratory comparison |
| Top two years share of signed IC | 60.65% | Playbook caution >50% |

The full signal report includes quantiles, yearly IC, three-year chunks, t-statistics, Newey–West statistics, liquidity bands and the forward-fill sensitivity. [Signal details](stage2_signal.md).

## Lookahead and year dependence

| Test | Measured | Verdict |
| --- | --- | --- |
| Signal/target prefix invariance | 5/5 cutoffs pass | PASS |
| Scheduled-open exit vs future low | Open 100; exit 100.00 vs 84.75; next-day weight 0.50 vs 0.00 | FAIL |
| Historical stop exits on zero-target dates | 16/1258 | Execution-order conflicts to investigate |
| One-year sensitivity | Sharpe range 1.43–1.86 | Fixed-return-series sensitivity, not a fresh backtest |
| Extreme TIL sensitivity | 42-stock Sharpe 0.66 with all tickers vs 1.69 without TIL | In-memory exclusion, not corrected prices |

## Exit diagnostics: 2015–2025

| Reason | Exits | 20d & 60d available | 20d excess | 60d excess | Mean excess | Purpose verdict | Sample |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HARD_STOP_HIT | 406 | 401 | 0.98% | 0.12% | 0.55% | neutral | ≥30 |
| VOL_STOP_HIT | 850 | 841 | -0.05% | 2.49% | 1.22% | too early | ≥30 |
| FORCE_EXIT | 2 | 2 | -30.07% | -2.85% | -16.46% | working | <30: directional |
| RANK_EXIT | 683 | 683 | 0.06% | 1.08% | 0.57% | neutral | ≥30 |
| REBAL_EXIT | 230 | 227 | 2.58% | 2.48% | 2.53% | paired comparison | ≥30 |
| CRASH_GUARD | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| ATR_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| PEAK_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |

| Reason | Horizon | Paired dates | Entered mean | Exited mean | Entered − exited |
| --- | --- | --- | --- | --- | --- |
| REBAL_EXIT | 20d | 54 | 2.68% | 3.72% | -1.04 pp |
| REBAL_EXIT | 60d | 54 | 5.53% | 7.99% | -2.45 pp |
| RANK_EXIT | 20d | 63 | 1.56% | 0.97% | 0.59 pp |
| RANK_EXIT | 60d | 63 | 4.55% | 4.12% | 0.43 pp |

## Data and next validation work

| Item | Result |
| --- | --- |
| Source data | 5,205 CSVs; 946 extreme adjacent valid-close changes require review |
| Survivorship proxy | 57/5205 = 1.10% end >6 months before panel end; delistings not independently verified |
| Source folder metadata | 0 added / 0 removed / 0 changed |
| Strategy / backtest files | Unchanged: True / True |
| Parity with strategy class | Maximum target / equity difference: 0 / 1.78e-15; warmup exposure 0 |
| Next | Resolve scheduled-open/stop ordering; verify corporate actions and delisting coverage on a derived dataset; rerun with fresh holdout evidence. |


Supporting scripts and raw CSVs are in [evidence](evidence/). No files in the source data folder or strategy code were changed.

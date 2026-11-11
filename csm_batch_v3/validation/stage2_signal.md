**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Stage 2 — Signal, horizons and decay

**Verdict: FAIL for the configured 2015–2025 signal.** L0 NW-t = 2.40 passes, configured L3 NW-t = 1.60 falls below 2.0; quantile ordering is 3/4 and two years account for 81.3% of total signed IC.

**Gate:** L0 composite and configured L3 each require 3-month NW-t ≥2.0, and <8-name exclusions ≤15%. Five-quantile monotonicity and spread are separate checks. IC is cross-sectional Spearman correlation of the factor at month-end with subsequent close-to-close returns; Newey–West lag equals the forward horizon in months. The response is calculated on the in-memory masked prices, with the caveat in Stage 1.

## 3-month filter ladder: 2015–2025

| Rung | Months | Mean IC | ICIR | t-stat | NW-t | IC >0 % | Mean names | <8 % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L3_before_optional_gates | 129 | 0.0370 | 0.3647 | 4.1419 | 2.9189 | 62.0155 | 503.6047 | 0.0000 |
| L0_long | 129 | 0.0257 | 0.3307 | 3.7562 | 2.5729 | 65.8915 | 2571.5349 | 0.0000 |
| L0_short | 129 | 0.0185 | 0.2580 | 2.9304 | 2.0726 | 59.6899 | 2746.9535 | 0.0000 |
| L0_composite | 129 | 0.0233 | 0.3011 | 3.4195 | 2.4023 | 61.2403 | 2570.0310 | 0.0000 |
| L1_price | 129 | 0.0336 | 0.4213 | 4.7855 | 3.4674 | 71.3178 | 2129.8062 | 0.0000 |
| L2_liquidity_circuit_age | 129 | 0.0579 | 0.5298 | 6.0170 | 4.2634 | 72.0930 | 896.4806 | 0.0000 |
| L3_tradeable | 128 | 0.0220 | 0.1813 | 2.0511 | 1.6029 | 59.3750 | 210.4341 | 0.7752 |
| L4_positive_momentum | 127 | 0.0144 | 0.1168 | 1.3160 | 0.9856 | 55.9055 | 180.9225 | 1.5504 |
| L5_top15 | 127 | -0.0496 | -0.1720 | -1.9383 | -1.6808 | 40.9449 | 14.7597 | 1.5504 |

## 3-month filter ladder: 2005–2014

| Rung | Months | Mean IC | ICIR | t-stat | NW-t | IC >0 % | Mean names | <8 % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L3_before_optional_gates | 114 | 0.0620 | 0.4598 | 4.9094 | 3.4035 | 72.8070 | 351.1453 | 2.5641 |
| L0_long | 117 | 0.0588 | 0.4894 | 5.2933 | 3.3679 | 70.0855 | 1212.1453 | 0.0000 |
| L0_short | 117 | 0.0650 | 0.6040 | 6.5331 | 4.1038 | 76.9231 | 1308.5556 | 0.0000 |
| L0_composite | 117 | 0.0672 | 0.5624 | 6.0834 | 3.8614 | 76.0684 | 1211.7094 | 0.0000 |
| L1_price | 117 | 0.0793 | 0.6599 | 7.1376 | 4.6438 | 78.6325 | 949.9744 | 0.0000 |
| L2_liquidity_circuit_age | 117 | 0.1010 | 0.7767 | 8.4013 | 5.6255 | 78.6325 | 682.9402 | 0.0000 |
| L3_tradeable | 106 | 0.0712 | 0.4845 | 4.9882 | 4.4163 | 78.3019 | 146.5897 | 9.4017 |
| L4_positive_momentum | 104 | 0.0691 | 0.5027 | 5.1270 | 4.5690 | 74.0385 | 123.0855 | 11.1111 |
| L5_top15 | 103 | -0.0057 | -0.0216 | -0.2197 | -0.2210 | 51.4563 | 13.4615 | 11.9658 |

L0 = raw factor; L1 = price floor; L2 = price, liquidity, circuit and listing age; L3 before optional gates adds the strategy’s trend and falling-knife filters; configured L3 additionally applies ADX and 52-week-high. L4 adds positive 12-month momentum; L5 limits to the first 15 factor ranks. L5 IC measures ordering **within** the small selected group; it is not a portfolio return or an equal-weight top-vs-pool accuracy test.

## Horizon decay: configured L3

### 2015–2025

| Months ahead | N | IC | ICIR | t-stat | NW-t | IC >0 % | Ordered pairs /4 | Q5−Q1 pp | Spread NW-t | Liquidity-weighted IC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 130.0000 | 0.0213 | 0.1670 | 1.9046 | 1.8092 | 56.1538 | 3.0000 | 0.6807 | 1.6300 | -0.0176 |
| 3.0000 | 128.0000 | 0.0220 | 0.1813 | 2.0511 | 1.6029 | 59.3750 | 3.0000 | 1.8753 | 2.0986 | 0.0063 |
| 6.0000 | 125.0000 | 0.0160 | 0.1224 | 1.3689 | 0.9494 | 57.6000 | 3.0000 | 4.1082 | 2.4939 | 0.0000 |
| 12.0000 | 119.0000 | -0.0158 | -0.1211 | -1.3212 | -0.8771 | 51.2605 | 2.0000 | 0.8922 | 0.2908 | -0.0193 |

### 2005–2014

| Months ahead | N | IC | ICIR | t-stat | NW-t | IC >0 % | Ordered pairs /4 | Q5−Q1 pp | Spread NW-t | Liquidity-weighted IC |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1.0000 | 108.0000 | 0.0554 | 0.4080 | 4.2402 | 3.9822 | 70.3704 | 3.0000 | 1.3346 | 2.3815 | 0.0518 |
| 3.0000 | 106.0000 | 0.0712 | 0.4845 | 4.9882 | 4.4163 | 78.3019 | 3.0000 | 3.1542 | 2.5821 | 0.0766 |
| 6.0000 | 103.0000 | 0.0585 | 0.4135 | 4.1961 | 2.9558 | 73.7864 | 3.0000 | 2.5406 | 1.1278 | 0.0616 |
| 12.0000 | 97.0000 | 0.0152 | 0.0944 | 0.9294 | 0.5573 | 59.7938 | 2.0000 | 0.7924 | 0.1514 | 0.0360 |

Liquidity-weighted IC weights ranked observations by median traded value; it is a **liquidity proxy**, not value-weighted IC by point-in-time market capitalization, which is unavailable. Equal-weighted quintile mean returns and ordering:

| window | horizon | quantile | mean_return_pct |
| --- | --- | --- | --- |
| late | 1 | 1 | 1.406 |
| late | 1 | 2 | 1.792 |
| late | 1 | 3 | 1.827 |
| late | 1 | 4 | 2.289 |
| late | 1 | 5 | 2.087 |
| late | 3 | 1 | 4.630 |
| late | 3 | 2 | 5.431 |
| late | 3 | 3 | 6.322 |
| late | 3 | 4 | 5.543 |
| late | 3 | 5 | 6.505 |
| late | 6 | 1 | 10.052 |
| late | 6 | 2 | 11.881 |
| late | 6 | 3 | 12.960 |
| late | 6 | 4 | 11.887 |
| late | 6 | 5 | 14.161 |
| late | 12 | 1 | 24.246 |
| late | 12 | 2 | 26.103 |
| late | 12 | 3 | 26.104 |
| late | 12 | 4 | 25.463 |
| late | 12 | 5 | 25.138 |

## Annual IC concentration: configured L3, 3 months

| window | n_months | mean_ic | top2_year_share_pct |
| --- | --- | --- | --- |
| early | 106 | 0.071 | 38.689 |
| late | 128 | 0.022 | 81.319 |

Top-two share divides the two largest annual signed-IC sums by total signed IC, including negative years; >50% is flagged in the playbook.

## Accuracy: theoretical signal picks by horizon

### 2015–2025

| Horizon months | Months | Selected mean | Above pool median % | Positive % | Excess vs pool pp | Excess NW-t |
| --- | --- | --- | --- | --- | --- | --- |
| 1.000 | 130.000 | 14.862 | 49.420 | 51.914 | 0.010 | 0.027 |
| 3.000 | 128.000 | 14.852 | 50.679 | 54.253 | 0.450 | 0.545 |
| 6.000 | 125.000 | 14.832 | 50.366 | 57.699 | 1.049 | 0.872 |
| 12.000 | 119.000 | 14.832 | 48.619 | 58.317 | -1.465 | -0.593 |

### 2005–2014

| Horizon months | Months | Selected mean | Above pool median % | Positive % | Excess vs pool pp | Excess NW-t |
| --- | --- | --- | --- | --- | --- | --- |
| 1.000 | 108.000 | 14.611 | 52.842 | 58.698 | 0.352 | 0.953 |
| 3.000 | 106.000 | 14.604 | 53.913 | 62.998 | 1.721 | 1.607 |
| 6.000 | 103.000 | 14.592 | 52.765 | 62.509 | 1.107 | 0.574 |
| 12.000 | 97.000 | 14.526 | 50.321 | 60.186 | 0.857 | 0.195 |

Top-15 accuracy is the monthly mean fraction of selected stocks above their contemporaneous eligible-pool median and above zero. Top excess is their equal-weight forward return minus the pool’s; it is not the executed portfolio, because it ignores hysteresis, stops, trading and costs.

## Time decay: configured L3, 3-month IC

| window | prior_months | prior_ic | recent_start | recent_months | recent_ic | recent_nw_t | difference | difference_nw_t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 74 | 0.0595 | 2012-01-01 | 32 | 0.0984 | 2.9526 | 0.0389 | 1.0404 |
| late | 95 | 0.0289 | 2023-01-01 | 33 | 0.0022 | 0.0896 | -0.0267 | -0.9091 |
| playbook_early | 60 | 0.0510 | 2010-01-01 | 32 | 0.1005 | 5.5969 | 0.0495 | 1.7499 |
| playbook_late | 131 | 0.0429 | 2024-01-01 | 31 | -0.0237 | -0.9075 | -0.0666 | -2.2371 |

The 2015–2025 comparison is 2023–2025 vs 2015–2022. The additional playbook-late comparison uses 2024–July 2026 signal months, with forward outcomes through October 2026, vs 2013–2023. Because these historical periods have already been examined, treat the latter as exploratory and do not treat its t-statistic as a fresh confirmation. Difference NW-t uses an intercept plus recent-period indicator with HAC lag 3. A non-significant difference is inconclusive, not proof the signal has remained stable. Results by year and three-year block make the sample size visible; annual tests are noisy.

### Annual IC and selected-stock accuracy: 2015–2025

| year | months | mean_ic | icir | t_stat | nw_t | positive_ic_pct | top15_above_median_pct | top15_positive_pct | top15_excess_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015.0000 | 12.0000 | -0.0025 | -0.0251 | -0.0871 | -0.1181 | 41.6667 | 51.1111 | 48.8889 | -0.0232 |
| 2016.0000 | 12.0000 | -0.0019 | -0.0211 | -0.0733 | -0.0657 | 41.6667 | 44.5635 | 56.7460 | 1.6949 |
| 2017.0000 | 12.0000 | 0.0544 | 0.7190 | 2.4908 | 2.1473 | 83.3333 | 55.5556 | 64.4444 | 3.4776 |
| 2018.0000 | 12.0000 | 0.0314 | 0.3158 | 1.0940 | 1.3130 | 75.0000 | 52.2222 | 37.2222 | -0.9555 |
| 2019.0000 | 12.0000 | 0.0688 | 0.4355 | 1.5087 | 1.3592 | 75.0000 | 51.6087 | 48.3791 | -0.2027 |
| 2020.0000 | 11.0000 | 0.0327 | 0.2911 | 0.9654 | 0.9620 | 54.5455 | 59.0909 | 67.0563 | 3.8667 |
| 2021.0000 | 12.0000 | 0.1206 | 1.1998 | 4.1562 | 5.3895 | 91.6667 | 58.3333 | 68.3333 | 3.6591 |
| 2022.0000 | 12.0000 | -0.0717 | -0.4330 | -1.5000 | -1.3532 | 33.3333 | 42.2222 | 41.6667 | -3.3710 |
| 2023.0000 | 12.0000 | 0.0706 | 0.9026 | 3.1268 | 4.8214 | 75.0000 | 55.5556 | 73.8889 | 1.0252 |
| 2024.0000 | 12.0000 | -0.0002 | -0.0026 | -0.0092 | -0.0107 | 41.6667 | 46.1111 | 43.8889 | -1.2743 |
| 2025.0000 | 9.0000 | -0.0858 | -0.7190 | -2.1569 | -2.3160 | 33.3333 | 38.8360 | 45.0265 | -3.6940 |

### Three-year blocks

| period | months | mean_ic | icir | nw_t | positive_ic_pct | top15_above_median_pct | top15_excess_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-2017 | 36 | 0.0167 | 0.1830 | 0.9083 | 55.5556 | 50.4101 | 1.7164 |
| 2018-2020 | 35 | 0.0446 | 0.3608 | 1.7235 | 68.5714 | 54.1706 | 0.8182 |
| 2021-2023 | 36 | 0.0399 | 0.2781 | 1.3493 | 66.6667 | 52.0370 | 0.4378 |
| 2024-2025 | 21 | -0.0369 | -0.3331 | -1.5766 | 38.0952 | 42.9932 | -2.3113 |

## Forward-fill sensitivity

| window | rung | horizon | n | raw_ic | ffill_ic | extra_observations |
| --- | --- | --- | --- | --- | --- | --- |
| late | L0_composite | 1 | 131 | 0.0147 | 0.0146 | 1271 |
| late | L3_tradeable | 1 | 130 | 0.0213 | 0.0213 | 0 |
| late | L0_composite | 3 | 129 | 0.0233 | 0.0231 | 1855 |
| late | L3_tradeable | 3 | 128 | 0.0220 | 0.0219 | 7 |
| late | L0_composite | 6 | 126 | 0.0286 | 0.0283 | 2249 |
| late | L3_tradeable | 6 | 125 | 0.0160 | 0.0155 | 16 |
| late | L0_composite | 12 | 120 | 0.0092 | 0.0091 | 2868 |
| late | L3_tradeable | 12 | 119 | -0.0158 | -0.0163 | 24 |

This compares masked-price forward outcomes with forward-filled masked outcomes. Added observations and IC changes are an empirical missing-data sensitivity, **not** proof there is no survivorship bias. Raw-vs-masked outcomes on the same configured eligible signals are compared below; common-pair IC uses only tickers with both outcomes.

| Months | Raw IC | Masked IC | Raw IC, common names | Masked IC, common names | Raw-only name-months | Masked-only name-months |
| --- | --- | --- | --- | --- | --- | --- |
| 129.0000 | 0.0220 | 0.0220 | 0.0220 | 0.0220 | 0.0000 | 0.0000 |

[Monthly mask comparison](evidence/mask_signal_comparison.csv). [Detailed IC data](evidence/signal_late_summary.csv), [monthly IC](evidence/signal_late_series.csv).

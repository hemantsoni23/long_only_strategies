**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Stage 2 — Signal IC, accuracy and decay

**Verdict: PASS basic IC, FAIL quantile ordering; concentration flagged.** The configured 2015–2025 3-month L0 NW-t is 2.41 and L3 NW-t is 2.91; each must be ≥2.0. Quantile ordering is 3/4 (75%, below the 80% gate) and its spread NW-t is 2.98. Interpret the gate in conjunction with the unresolved data-adjustment caveat in Stage 1.

IC is cross-sectional Spearman correlation between the stock factor and its subsequent return. NW uses lag equal to the forward horizon (in months); ordinary t-statistics are displayed separately. The ETF does not enter the stock-factor IC.

## 3-month filter ladder: 2015–2025

| rung | n_months | mean_ic | icir | t_stat | nw_t | positive_ic_pct | average_names | months_lt8_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0_long | 129 | 0.0258 | 0.3315 | 3.7647 | 2.5780 | 65.8915 | 2571.5349 | 0.0000 |
| L0_short | 129 | 0.0186 | 0.2604 | 2.9573 | 2.0900 | 59.6899 | 2746.9302 | 0.0000 |
| L0_composite | 129 | 0.0234 | 0.3027 | 3.4386 | 2.4142 | 61.2403 | 2570.0078 | 0.0000 |
| L1_price | 129 | 0.0337 | 0.4222 | 4.7953 | 3.4703 | 72.0930 | 2129.7907 | 0.0000 |
| L2_liquidity_circuit_age | 129 | 0.0579 | 0.5296 | 6.0152 | 4.2604 | 72.0930 | 896.4496 | 0.0000 |
| L3_tradeable | 129 | 0.0369 | 0.3642 | 4.1364 | 2.9135 | 62.0155 | 503.6357 | 0.0000 |
| L4_positive_momentum | 129 | 0.0244 | 0.2780 | 3.1573 | 2.3510 | 61.2403 | 418.8527 | 0.0000 |
| L5_top30 | 129 | -0.0064 | -0.0334 | -0.3798 | -0.3290 | 47.2868 | 29.9070 | 0.0000 |

## 3-month filter ladder: 2005–2014

| rung | n_months | mean_ic | icir | t_stat | nw_t | positive_ic_pct | average_names | months_lt8_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L0_long | 117 | 0.0589 | 0.4898 | 5.2980 | 3.3711 | 70.0855 | 1212.1538 | 0.0000 |
| L0_short | 117 | 0.0648 | 0.6016 | 6.5071 | 4.0880 | 76.9231 | 1308.5726 | 0.0000 |
| L0_composite | 117 | 0.0673 | 0.5621 | 6.0797 | 3.8595 | 76.0684 | 1211.7265 | 0.0000 |
| L1_price | 117 | 0.0793 | 0.6601 | 7.1396 | 4.6449 | 79.4872 | 949.9915 | 0.0000 |
| L2_liquidity_circuit_age | 117 | 0.1011 | 0.7769 | 8.4039 | 5.6260 | 78.6325 | 682.9487 | 0.0000 |
| L3_tradeable | 114 | 0.0622 | 0.4601 | 4.9130 | 3.4037 | 72.8070 | 351.1624 | 2.5641 |
| L4_positive_momentum | 111 | 0.0510 | 0.4205 | 4.4305 | 3.1719 | 71.1712 | 278.7094 | 5.1282 |
| L5_top30 | 111 | -0.0409 | -0.2166 | -2.2825 | -1.9662 | 44.1441 | 28.1197 | 5.1282 |

L0 is the raw factor, L1 adds price, L2 adds liquidity/circuit/listing age, L3 adds trend and falling-knife, L4 adds positive 12-month momentum, and L5 is the top-30 ranked portion. L5 measures ranking within the small selected group, not the portfolio P&L.

## Forward horizons and theoretical stock-selection accuracy

### 2015–2025

| Horizon months | IC months | IC | ICIR | t-stat | NW-t | Positive IC % | Top30 above median % | Top30 positive % | Top30 excess pp | Ordered quintile pairs /4 | Q5−Q1 NW-t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 131 | 0.0352 | 0.3581 | 4.0982 | 4.1595 | 64.1221 | 51.7870 | 52.5832 | 0.1559 | 3.0000 | 3.6194 |
| 3 | 129 | 0.0369 | 0.3642 | 4.1364 | 2.9135 | 62.0155 | 51.9389 | 54.1108 | 0.3712 | 3.0000 | 2.9785 |
| 6 | 126 | 0.0329 | 0.3281 | 3.6825 | 2.0155 | 65.8730 | 50.8188 | 56.4841 | 0.8350 | 4.0000 | 2.5632 |
| 12 | 120 | 0.0023 | 0.0238 | 0.2603 | 0.1300 | 53.3333 | 48.6042 | 56.5684 | -2.7786 | 1.0000 | 0.8004 |

### 2005–2014

| Horizon months | IC months | IC | ICIR | t-stat | NW-t | Positive IC % | Top30 above median % | Top30 positive % | Top30 excess pp | Ordered quintile pairs /4 | Q5−Q1 NW-t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 116 | 0.0553 | 0.3835 | 4.1305 | 3.8157 | 71.5517 | 53.6883 | 57.1879 | 0.7950 | 4.0000 | 2.8781 |
| 3 | 114 | 0.0622 | 0.4601 | 4.9130 | 3.4037 | 72.8070 | 55.4633 | 59.7554 | 1.6770 | 4.0000 | 2.7590 |
| 6 | 111 | 0.0455 | 0.3042 | 3.2045 | 1.6202 | 69.3694 | 53.4410 | 59.1116 | 1.2306 | 3.0000 | 1.2536 |
| 12 | 105 | 0.0193 | 0.1344 | 1.3775 | 0.5566 | 60.0000 | 51.0437 | 57.0065 | 0.1611 | 3.0000 | 0.2852 |

Accuracy is the average fraction of theoretical top-30 stocks above their eligible-pool median or above zero; excess is their equal-weight forward return minus the pool average. This is not an executed portfolio: hysteresis, stops, costs and ETF are excluded. Quintile returns are equal-weighted; the 3-month ordered-pairs gate is ≥80% and Q5−Q1 NW-t gate is ≥2.

### Quintile returns: 2015–2025

| window | horizon | quantile | mean_return_pct |
| --- | --- | --- | --- |
| late | 1 | 1 | 0.965 |
| late | 1 | 2 | 2.540 |
| late | 1 | 3 | 1.563 |
| late | 1 | 4 | 1.986 |
| late | 1 | 5 | 2.020 |
| late | 3 | 1 | 3.978 |
| late | 3 | 2 | 5.978 |
| late | 3 | 3 | 5.060 |
| late | 3 | 4 | 5.929 |
| late | 3 | 5 | 6.081 |
| late | 6 | 1 | 9.242 |
| late | 6 | 2 | 10.895 |
| late | 6 | 3 | 11.588 |
| late | 6 | 4 | 12.238 |
| late | 6 | 5 | 12.703 |
| late | 12 | 1 | 22.385 |
| late | 12 | 2 | 26.030 |
| late | 12 | 3 | 25.196 |
| late | 12 | 4 | 24.945 |
| late | 12 | 5 | 24.416 |

## Equal-weight vs liquidity-weighted IC proxy

| window | horizon | mean_ic | weighted_liquidity_ic | top2_year_share_pct |
| --- | --- | --- | --- | --- |
| early | 1 | 0.0553 | 0.0569 | 37.3287 |
| early | 3 | 0.0622 | 0.0700 | 40.6802 |
| early | 6 | 0.0455 | 0.0495 | 72.5957 |
| early | 12 | 0.0193 | 0.0779 | 191.5872 |
| late | 1 | 0.0352 | 0.0279 | 46.8121 |
| late | 3 | 0.0369 | 0.0381 | 60.6543 |
| late | 6 | 0.0329 | 0.0317 | 73.0396 |
| late | 12 | 0.0023 | 0.0142 | 751.9801 |

Liquidity weighting uses median traded value as a proxy; point-in-time market-cap weights were unavailable. Top-two-year share divides the two largest signed annual IC sums by total signed IC and is flagged above 50%.

## Time decay: 3-month L3 IC

| window | prior_months | prior_ic | recent_start | recent_months | recent_ic | recent_nw_t | difference | difference_nw_t |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 82 | 0.0456 | 2012-01-01 | 32 | 0.1046 | 3.6757 | 0.0590 | 1.6360 |
| late | 96 | 0.0377 | 2023-01-01 | 33 | 0.0347 | 1.7928 | -0.0030 | -0.1222 |
| playbook_early | 68 | 0.0132 | 2010-01-01 | 32 | 0.1055 | 6.3173 | 0.0924 | 2.8569 |
| playbook_late | 132 | 0.0550 | 2024-01-01 | 31 | 0.0165 | 0.9063 | -0.0384 | -1.6809 |

The late-window comparison is 2023–2025 vs 2015–2022. The playbook-late comparison uses recent 2024–July 2026 signal months with outcomes observed through October 2026, versus earlier years. These historical windows have been examined and are not blind tests. NW-t for the difference uses HAC lag 3. A non-significant result does not prove stability.

### Yearly signal behavior: 2015–2025

| year | months | mean_ic | icir | t_stat | nw_t | positive_ic_pct | top30_above_median_pct | top30_positive_pct | top30_excess_pct |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 12 | 0.0068 | 0.0858 | 0.2973 | 0.2344 | 41.6667 | 49.7222 | 44.7222 | -0.7009 |
| 2016 | 12 | 0.0138 | 0.2027 | 0.7023 | 1.0260 | 58.3333 | 45.9866 | 56.6188 | -1.0431 |
| 2017 | 12 | 0.0266 | 0.4425 | 1.5328 | 1.3631 | 66.6667 | 52.7778 | 64.1667 | 3.4851 |
| 2018 | 12 | 0.0733 | 0.8734 | 3.0256 | 3.1896 | 83.3333 | 56.8391 | 41.8199 | 0.5495 |
| 2019 | 12 | 0.1334 | 1.0249 | 3.5505 | 3.2507 | 83.3333 | 60.6705 | 51.3848 | 1.7465 |
| 2020 | 12 | -0.0282 | -0.1773 | -0.6141 | -0.5931 | 41.6667 | 53.4579 | 65.2011 | 1.1515 |
| 2021 | 12 | 0.1075 | 1.6168 | 5.6009 | 7.3985 | 91.6667 | 55.0000 | 63.6111 | 1.0025 |
| 2022 | 12 | -0.0315 | -0.4230 | -1.4654 | -1.8253 | 16.6667 | 42.7778 | 40.8333 | -3.1105 |
| 2023 | 12 | 0.0936 | 1.9225 | 6.6599 | 7.0237 | 100.0000 | 56.1111 | 70.5556 | 1.5410 |
| 2024 | 12 | 0.0053 | 0.0818 | 0.2832 | 0.2709 | 41.6667 | 49.1667 | 45.5556 | 0.0078 |
| 2025 | 9 | -0.0047 | -0.0576 | -0.1727 | -0.2052 | 55.5556 | 47.7778 | 49.6296 | -0.8516 |

### Three-year blocks

| period | months | mean_ic | icir | nw_t | positive_ic_pct | top30_above_median_pct | top30_excess_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015-2017 | 36 | 0.0157 | 0.2314 | 1.2012 | 55.5556 | 49.4955 | 0.5804 |
| 2018-2020 | 36 | 0.0595 | 0.4199 | 1.7704 | 69.4444 | 56.9891 | 1.1491 |
| 2021-2023 | 36 | 0.0565 | 0.6366 | 2.6651 | 69.4444 | 51.2963 | -0.1890 |
| 2024-2025 | 21 | 0.0010 | 0.0145 | 0.0660 | 47.6190 | 48.5714 | -0.3605 |

## Raw vs forward-filled outcomes

| window | rung | horizon | n | raw_ic | ffill_ic | extra_observations |
| --- | --- | --- | --- | --- | --- | --- |
| late | L0_composite | 1 | 131 | 0.0148 | 0.0148 | 1271 |
| late | L3_tradeable | 1 | 131 | 0.0352 | 0.0352 | 3 |
| late | L0_composite | 3 | 129 | 0.0234 | 0.0232 | 1854 |
| late | L3_tradeable | 3 | 129 | 0.0369 | 0.0368 | 17 |
| late | L0_composite | 6 | 126 | 0.0287 | 0.0284 | 2249 |
| late | L3_tradeable | 6 | 126 | 0.0329 | 0.0326 | 31 |
| late | L0_composite | 12 | 120 | 0.0092 | 0.0091 | 2868 |
| late | L3_tradeable | 12 | 120 | 0.0023 | 0.0019 | 57 |

Forward-fill comparison is a missing-data sensitivity; small differences do not prove the absence of delisting or survivorship bias. [Detailed IC series](evidence/signal_late_series.csv) · [All filter and horizon results](evidence/signal_late_summary.csv).

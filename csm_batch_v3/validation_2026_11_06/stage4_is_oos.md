**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Stage 4 — IS/OOS, ETF sleeve and full-sample results

**Verdict: NOT VALIDATED.** The numerical comparisons below are retrospective, not blind OOS. The v2 strategy family and both periods have already been inspected; complete development and post-OOS modification history are unavailable. Unresolved timing and source-data issues also block promotion regardless of ratio results. Parameter/ablation sweeps were rerun separately for each period; no configuration was selected or changed after viewing them.

| Comparison | Flat-start period | Warmup |
| --- | --- | --- |
| Reference early | 2005-01-01–2014-12-31 | 450 calendar days where available |
| Reference late | 2015-01-01–2025-12-31 | 450 calendar days |
| Playbook early | 2001-01-01–2012-12-31 | Up to 450 calendar days, limited by data |
| Playbook late | 2013-01-01–2026-10-30 | 450 calendar days |
| Full descriptive | 2002-01-01–2025-12-31 | Up to 450 calendar days |

Stock selection and holdings start flat; the ETF sweep is also prevented from buying before each report start. The baseline cannot invest in GOLDBEES before its first data point in 2007-03-19; the supplied file also has no observations in 2011–2014.

## Breadth and ETF coverage

| window | months | median | mean | below8_pct | below30_pct |
| --- | --- | --- | --- | --- | --- |
| early | 120 | 330.000 | 360.692 | 2.500 | 5.833 |
| late | 132 | 503.500 | 502.765 | 0.000 | 0.000 |
| playbook_early | 144 | 214.500 | 234.979 | 28.472 | 31.250 |
| playbook_late | 166 | 498.000 | 494.343 | 0.000 | 0.000 |

| window | days | days_before_first_etf_close | days_before_first_etf_close_pct | calendar_aligned_first_valid | tradable_bars | tradable_bars_pct | abs_return_clipped_days |
| --- | --- | --- | --- | --- | --- | --- | --- |
| early | 2483 | 552 | 22.231 | 2007-03-19 | 938 | 37.777 | 0 |
| late | 2730 | 0 | 0.000 | 2015-01-01 | 2721 | 99.670 | 0 |
| playbook_early | 2996 | 1559 | 52.036 | 2007-03-19 | 938 | 31.308 | 0 |
| playbook_late | 3429 | 494 | 14.407 | 2015-01-01 | 2926 | 85.331 | 0 |
| full | 5972 | 1311 | 21.952 | 2007-03-19 | 3659 | 61.269 | 0 |

The supplied ETF file has **zero observations in 2011–2014**: its last pre-gap close is 2010-12-31 and the next is 2015-01-01. The engine forward-fills the last mark for valuation during this gap and may assume sales on untradable bars. This makes early-window and full-sample ETF performance, and split comparisons containing the gap, unreliable even if their numerical ratios pass. The late-only 2015–2025 sample does not include this gap.

| year | source_rows |
| --- | --- |
| 2005 | 0 |
| 2006 | 0 |
| 2007 | 198 |
| 2008 | 246 |
| 2009 | 243 |
| 2010 | 253 |
| 2011 | 0 |
| 2012 | 0 |
| 2013 | 0 |
| 2014 | 0 |
| 2015 | 248 |
| 2016 | 246 |
| 2017 | 247 |
| 2018 | 245 |
| 2019 | 244 |
| 2020 | 252 |
| 2021 | 248 |
| 2022 | 248 |
| 2023 | 246 |
| 2024 | 249 |
| 2025 | 249 |
| 2026 | 208 |

## Baseline scorecards

| Window | First stock entry | CAGR % | Sharpe | Sortino | Max DD % | Calmar | Vol % | Stock exposure % | ETF exposure % | ETF cost drag %/yr | Trades |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 2005-01-03 | 38.199 | 2.321 | 3.529 | -29.170 | 1.310 | 14.601 | 67.001 | 13.461 | 0.835 | 1871 |
| late | 2015-01-01 | 27.742 | 1.826 | 2.675 | -18.278 | 1.518 | 14.172 | 71.413 | 28.580 | 2.315 | 2200 |
| playbook_early | 2001-03-01 | 28.592 | 1.802 | 3.147 | -29.170 | 0.980 | 14.672 | 49.068 | 11.156 | 0.695 | 1659 |
| playbook_late | 2013-01-01 | 30.038 | 1.871 | 2.710 | -24.203 | 1.241 | 14.862 | 70.448 | 24.833 | 1.988 | 2745 |
| full | 2002-01-01 | 31.548 | 1.991 | 3.169 | -29.170 | 1.082 | 14.470 | 62.772 | 18.665 | 1.410 | 4219 |

## Additional trade and benchmark scorecard

| window | trade_win_pct | profit_factor_pct_units | payoff | hold_days | beta_proxy | alpha_pct_proxy |
| --- | --- | --- | --- | --- | --- | --- |
| early | 51.042 | 2.478 | 2.377 | 43.958 | 0.396 | 24.324 |
| late | 47.136 | 2.042 | 2.291 | 41.799 | 0.513 | 10.484 |
| playbook_early | 49.186 | 2.614 | 2.701 | 44.427 | 0.214 | 19.779 |
| playbook_late | 48.780 | 2.201 | 2.311 | 41.997 | 0.527 | 12.402 |
| full | 48.969 | 2.417 | 2.518 | 43.155 | 0.355 | 17.465 |

Win rate, profit factor and payoff use per-trade percentage returns; dollar-weighted profit factor is unavailable. Beta and annual alpha use an equal-weight raw-stock return proxy with daily returns clipped to ±50%, not an independently verified investable index.

## ETF sweep vs idle cash on the same stock-weight path

| window | cash_cagr | cash_sharpe | cash_calmar | cash_maxdd | etf_cagr | etf_sharpe | etf_calmar | etf_maxdd | etf_first_usable | etf_exposure_pct | etf_cost_drag_pct | forced_untradable |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 35.108 | 2.463 | 1.269 | -27.665 | 38.199 | 2.321 | 1.310 | -29.170 | 2007-03-19 | 13.461 | 0.835 | 2 |
| late | 22.309 | 1.647 | 1.313 | -16.995 | 27.742 | 1.826 | 1.518 | -18.278 | 2015-01-01 | 28.580 | 2.315 | 1 |
| playbook_early | 26.192 | 1.851 | 0.947 | -27.665 | 28.592 | 1.802 | 0.980 | -29.170 | 2007-03-19 | 11.156 | 0.695 | 2 |
| playbook_late | 25.548 | 1.889 | 1.503 | -16.995 | 30.038 | 1.871 | 1.241 | -24.203 | 2015-01-01 | 24.833 | 1.988 | 1 |
| full | 27.754 | 1.953 | 1.003 | -27.665 | 31.548 | 1.991 | 1.082 | -29.170 | 2007-03-19 | 18.665 | 1.410 | 3 |

`etf_first_usable` is the sweep activation bound (the later of the first usable close in the loaded panel and the report start); an actual purchase also requires a tradable bar. It is not necessarily ETF inception or the first actual purchase. `forced_untradable` counts sales the backtest assumes even when its completed-bar tradability test is false. ETF cost drag is estimated from traded weight, not actual market impact. Both runs share the same simulated stock decisions; differences are the modeled ETF, its costs and the cash return convention.

## Flat-start vs source-main warmup convention, 2015–2025

| run | cagr_pct | sharpe | calmar | maxdd_pct | prestart_entries | prestart_holdings_crossing_boundary | reported_trade_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source main convention with pre-start holdings | 27.363 | 1.764 | 1.707 | -16.030 | 31 | 12 | 2188 |
| flat-start validation | 27.742 | 1.826 | 1.518 | -18.278 | 0 | 0 | 2200 |

The source main permits positions during warmup, while the split tests reset stock and ETF holdings. Its reported trade log excludes entries made before the report starts. Main-comparable results are provided to explain why the two conventions can disagree.

## Source-configured 2005–2015 period

| run | cagr_pct | sharpe | calmar | maxdd_pct | prestart_entries | prestart_holdings_crossing_boundary | reported_trade_rows |
| --- | --- | --- | --- | --- | --- | --- | --- |
| source main convention with pre-start holdings | 37.940 | 2.297 | 1.405 | -26.994 | 30 | 28 | 1978 |
| flat-start validation | 35.824 | 2.203 | 1.228 | -29.170 | 0 | 0 | 2064 |

The first row uses the current source `START_DATE` and `END_DATE` with its warmup-active convention; the second resets at the same start. The actual source-default ETF exposure during the 2011–2014 missing-data gap is summarized below.

| gap_days | gap_days_etf_weight_positive | gap_average_etf_weight_pct | gap_max_etf_weight_pct | gap_untradable_sale_days | pre_resume_etf_weight_pct | resume_day_etf_contribution_pct |
| --- | --- | --- | --- | --- | --- | --- |
| 992 | 315 | 0.003 | 0.009 | 1 | 0.000 | 0.000 |

The gap calculation uses the source-default warmup-active portfolio, so it need not equal the independently flat-start splits. ETF weight during the missing interval was very small in this run; the major limitation is that the model could not buy the intended ETF through the missing years, so it cannot establish what a continuously available sweep would have earned.

## Reference split A: 2005–2014 IS → 2015–2025 OOS

| Metric | Value | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 0.787 | ≥0.60 | PASS |
| Calmar OOS/IS | 1.159 | ≥0.60 | PASS |
| CAGR OOS/IS | 0.726 | ≥0.50 | PASS |
| Max DD OOS/IS | 0.627 | ≤1.50 | PASS |
| OOS Sharpe | 1.826 | >0 | PASS |
| OOS L0 IC NW-t | 2.414 | ≥1.50 | PASS |
| OOS L3 IC NW-t | 2.914 | ≥1.50 | PASS |
| OOS L3 IC months <8 % | 0.000 | ≤15 | PASS |
| Δ Sharpe (OOS − IS) | -0.496 | informational | — |
| Δ Calmar (OOS − IS) | 0.208 | informational | — |

## Reference split B: 2015–2025 IS → 2005–2014 OOS

| Metric | Value | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 1.271 | ≥0.60 | PASS |
| Calmar OOS/IS | 0.863 | ≥0.60 | PASS |
| CAGR OOS/IS | 1.377 | ≥0.50 | PASS |
| Max DD OOS/IS | 1.596 | ≤1.50 | FAIL |
| OOS Sharpe | 2.321 | >0 | PASS |
| OOS L0 IC NW-t | 3.859 | ≥1.50 | PASS |
| OOS L3 IC NW-t | 3.404 | ≥1.50 | PASS |
| OOS L3 IC months <8 % | 2.564 | ≤15 | PASS |
| Δ Sharpe (OOS − IS) | 0.496 | informational | — |
| Δ Calmar (OOS − IS) | -0.208 | informational | — |

## Playbook split A: 2001–2012 IS → 2013–2026 OOS

| Metric | Value | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 1.039 | ≥0.60 | PASS |
| Calmar OOS/IS | 1.266 | ≥0.60 | PASS |
| CAGR OOS/IS | 1.051 | ≥0.50 | PASS |
| Max DD OOS/IS | 0.830 | ≤1.50 | PASS |
| OOS Sharpe | 1.871 | >0 | PASS |
| OOS L0 IC NW-t | 2.841 | ≥1.50 | PASS |
| OOS L3 IC NW-t | 3.902 | ≥1.50 | PASS |
| OOS L3 IC months <8 % | 0.000 | ≤15 | PASS |
| Δ Sharpe (OOS − IS) | 0.070 | informational | — |
| Δ Calmar (OOS − IS) | 0.261 | informational | — |

## Playbook split B: 2013–2026 IS → 2001–2012 OOS

| Metric | Value | Gate | Verdict |
| --- | --- | --- | --- |
| Sharpe OOS/IS | 0.963 | ≥0.60 | PASS |
| Calmar OOS/IS | 0.790 | ≥0.60 | PASS |
| CAGR OOS/IS | 0.952 | ≥0.50 | PASS |
| Max DD OOS/IS | 1.205 | ≤1.50 | PASS |
| OOS Sharpe | 1.802 | >0 | PASS |
| OOS L0 IC NW-t | 3.032 | ≥1.50 | PASS |
| OOS L3 IC NW-t | 2.033 | ≥1.50 | PASS |
| OOS L3 IC months <8 % | 29.078 | ≤15 | FAIL |
| Δ Sharpe (OOS − IS) | -0.070 | informational | — |
| Δ Calmar (OOS − IS) | -0.261 | informational | — |

OOS/IS Sharpe and Calmar 0.40–0.60 are caution and below 0.40 fail; CAGR must be ≥0.50, drawdown depth ≤1.5×, OOS Sharpe positive, and L0/L3 OOS NW-t ≥1.5. The IC breadth row repeats the Stage 2 ≤15% exclusion gate; it is not an extra Stage 4 ratio threshold. Δ means OOS minus IS. A fresh frozen configuration and genuinely untouched OOS evidence would still be needed even if retrospective numeric gates passed. The early window includes 2008; the later window includes 2018, 2020 and 2022. ETF inception changes the opportunity set across the early split.

## Full-sample calendar years, informational only

| year | return_pct | sharpe | maxdd_pct |
| --- | --- | --- | --- |
| 2002 | 1.888 | 1.105 | -0.855 |
| 2003 | 4.339 | 2.808 | -1.273 |
| 2004 | 80.221 | 2.377 | -5.994 |
| 2005 | 53.892 | 2.838 | -9.812 |
| 2006 | 37.854 | 2.573 | -12.417 |
| 2007 | 76.121 | 3.425 | -8.708 |
| 2008 | -14.600 | -0.609 | -29.170 |
| 2009 | 90.767 | 3.708 | -6.361 |
| 2010 | 36.750 | 2.581 | -8.894 |
| 2011 | -4.207 | -0.565 | -9.091 |
| 2012 | 38.520 | 3.589 | -6.290 |
| 2013 | 9.728 | 1.381 | -6.032 |
| 2014 | 112.477 | 5.346 | -6.236 |
| 2015 | 12.608 | 0.909 | -15.240 |
| 2016 | 24.256 | 1.513 | -15.850 |
| 2017 | 42.983 | 3.169 | -5.405 |
| 2018 | -3.910 | -0.299 | -10.330 |
| 2019 | 20.873 | 2.268 | -3.821 |
| 2020 | 56.602 | 2.602 | -13.258 |
| 2021 | 78.360 | 3.856 | -7.813 |
| 2022 | 7.983 | 0.586 | -18.278 |
| 2023 | 55.308 | 3.524 | -9.271 |
| 2024 | 19.667 | 1.199 | -11.283 |
| 2025 | 12.134 | 0.931 | -8.267 |

[Early playbook sweep](evidence/playbook_early_sweep_cells.csv) · [Late playbook sweep](evidence/playbook_late_sweep_cells.csv) · [ETF data audit](evidence/etf_audit.json).

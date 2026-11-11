# Stage 3 — Universe, parameter robustness & ablation

**Verdict: FAIL / DATA-CONDITIONAL**

| Universe card | Setting |
| --- | --- |
| Source | 5,205 raw OHLCV CSVs; 2000-01-03 to 2026-10-30 |
| Eligibility | ₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters |
| Portfolio / costs | 30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0% |
| Windows | Early 2001–2012; late 2013–2026-10-30; full 2002–2025-12-31 |
| Accounting convention | Exit-day gains/losses omitted at user request |
| Stage 1 status | Data adjustment unresolved; survivorship coverage flagged |

### Early window: universe sweep

| Liquidity rank | Sharpe | Calmar | CAGR | Max DD | Volatility |
| --- | --- | --- | --- | --- | --- |
| top_100 | 1.47 | 0.73 | 19.47% | -26.84% | 12.75% |
| top_250 | 1.52 | 0.77 | 21.95% | -28.57% | 13.77% |
| top_500 | 1.78 | 0.87 | 25.14% | -28.86% | 13.15% |
| top_750 | 1.75 | 0.86 | 24.45% | -28.31% | 13.09% |
| top_1000 | 1.85 | 0.95 | 26.19% | -27.66% | 13.14% |
| top_1500 | 1.84 | 0.94 | 26.03% | -27.77% | 13.14% |
| band_0_500 | 1.78 | 0.87 | 25.14% | -28.86% | 13.15% |
| band_500_1000 | 1.72 | 0.57 | 15.79% | -27.67% | 8.85% |
| band_1000_1500 | 1.01 | 0.39 | 6.51% | -16.68% | 6.52% |
| band_1000_2000 | 1.39 | 0.60 | 8.83% | -14.71% | 6.27% |

| Core top-250–1500 metric | Range | Pass bar | Result |
| --- | --- | --- | --- |
| Sharpe | 0.33 | ≤0.35 | PASS |
| Calmar | 0.18 | ≤0.50 | PASS |
| CAGR (pp) | 4.24 | ≤8 pp | PASS |
| Max DD (pp) | 1.19 | ≤10 pp | PASS |
| Any core Sharpe ≤0 | 0 | 0 | PASS |

| 3m signal liquidity band | Mean IC | ICIR | NW-t | Months excluded |
| --- | --- | --- | --- | --- |
| band_0_100 | 0.0608 | 0.288 | 2.21 | 29.79% |
| band_0_250 | 0.0493 | 0.263 | 1.85 | 29.08% |
| band_0_500 | 0.0422 | 0.261 | 1.75 | 29.08% |
| band_0_750 | 0.0380 | 0.256 | 1.71 | 29.08% |
| band_0_1000 | 0.0427 | 0.302 | 2.03 | 29.08% |
| band_0_1500 | 0.0409 | 0.293 | 1.97 | 28.37% |
| band_500_1000 | 0.0847 | 0.434 | 2.96 | 52.48% |
| band_1000_1500 | 0.0822 | 0.414 | 3.17 | 71.63% |
| band_1000_2000 | 0.0750 | 0.398 | 3.05 | 71.63% |

| IC robustness measure | Measured | Reference | Result |
| --- | --- | --- | --- |
| Core ICIR range | 0.046 | ≤0.35 Sharpe analogue | PASS |

### Late window: universe sweep

| Liquidity rank | Sharpe | Calmar | CAGR | Max DD | Volatility |
| --- | --- | --- | --- | --- | --- |
| top_100 | 1.35 | 1.15 | 16.78% | -14.56% | 12.25% |
| top_250 | 1.77 | 1.55 | 23.90% | -15.40% | 12.77% |
| top_500 | 1.83 | 1.46 | 25.78% | -17.64% | 13.19% |
| top_750 | 1.89 | 1.54 | 26.86% | -17.48% | 13.24% |
| top_1000 | 1.88 | 1.52 | 26.57% | -17.43% | 13.19% |
| top_1500 | 1.97 | 1.63 | 26.94% | -16.48% | 12.70% |
| band_0_500 | 1.83 | 1.46 | 25.78% | -17.64% | 13.19% |
| band_500_1000 | 0.63 | 1.96 | 38.97% | -19.92% | 69.85% |
| band_1000_1500 | 2.70 | 1.96 | 38.91% | -19.82% | 12.69% |
| band_1000_2000 | 2.57 | 1.86 | 36.24% | -19.44% | 12.55% |

| Core top-250–1500 metric | Range | Pass bar | Result |
| --- | --- | --- | --- |
| Sharpe | 0.20 | ≤0.35 | PASS |
| Calmar | 0.17 | ≤0.50 | PASS |
| CAGR (pp) | 3.04 | ≤8 pp | PASS |
| Max DD (pp) | 2.24 | ≤10 pp | PASS |
| Any core Sharpe ≤0 | 0 | 0 | PASS |

| 3m signal liquidity band | Mean IC | ICIR | NW-t | Months excluded |
| --- | --- | --- | --- | --- |
| band_0_100 | 0.0530 | 0.251 | 2.40 | 0.61% |
| band_0_250 | 0.0540 | 0.360 | 3.33 | 0.00% |
| band_0_500 | 0.0567 | 0.457 | 4.14 | 0.00% |
| band_0_750 | 0.0490 | 0.429 | 3.81 | 0.00% |
| band_0_1000 | 0.0477 | 0.436 | 3.90 | 0.00% |
| band_0_1500 | 0.0440 | 0.418 | 3.83 | 0.00% |
| band_500_1000 | 0.0338 | 0.256 | 2.60 | 0.61% |
| band_1000_1500 | 0.0375 | 0.257 | 2.97 | 6.75% |
| band_1000_2000 | 0.0433 | 0.334 | 3.70 | 6.13% |

| IC robustness measure | Measured | Reference | Result |
| --- | --- | --- | --- |
| Core ICIR range | 0.097 | ≤0.35 Sharpe analogue | PASS |

### Parameter sweeps — Sharpe

| Setting | Early | Late |
| --- | --- | --- |
| lookback_7 | 1.80 | 1.80 |
| lookback_10 | 1.72 | 1.96 |
| lookback_12 | 1.85 | 1.88 |
| lookback_14 | 1.80 | 1.90 |
| lookback_17 | 2.11 | 1.99 |
| rebalance_1 | 1.86 | 1.87 |
| rebalance_2 | 1.85 | 1.88 |
| rebalance_3 | 1.81 | 1.75 |
| positions_18 | 1.87 | 1.79 |
| positions_24 | 1.61 | 1.92 |
| positions_30 | 1.85 | 1.88 |
| positions_36 | 1.93 | 0.95 |
| positions_42 | 1.97 | 1.04 |
| stop_0.09 | 1.92 | 1.98 |
| stop_0.12 | 1.87 | 1.92 |
| stop_0.15 | 1.85 | 1.88 |
| stop_0.18 | 1.80 | 1.84 |
| stop_0.21 | 1.79 | 1.81 |
| regime_-0.06 | 1.83 | 1.87 |
| regime_-0.08 | 1.83 | 1.87 |
| regime_-0.10 | 1.85 | 1.88 |
| regime_-0.12 | 1.84 | 1.92 |
| regime_-0.14 | 1.84 | 1.92 |

| Window | Approximate ±20% setting | Sharpe range | Bar | Result |
| --- | --- | --- | --- | --- |
| early | Lookback 10 vs 14 months | 0.08 | ≤0.40 | PASS |
| early | Positions 24 vs 36 | 0.32 | ≤0.40 | PASS |
| early | Hard stop 12% vs 18% | 0.07 | ≤0.40 | PASS |
| early | Regime cutoff −8% vs −12% | 0.01 | ≤0.40 | PASS |
| early | Rebalance ±20% | N/A: monthly integer rounds to 2 | five points requested | INCOMPLETE |
| late | Lookback 10 vs 14 months | 0.06 | ≤0.40 | PASS |
| late | Positions 24 vs 36 | 0.97 | ≤0.40 | FAIL |
| late | Hard stop 12% vs 18% | 0.07 | ≤0.40 | PASS |
| late | Regime cutoff −8% vs −12% | 0.05 | ≤0.40 | PASS |
| late | Rebalance ±20% | N/A: monthly integer rounds to 2 | five points requested | INCOMPLETE |

### Early ablation — value (relative change vs baseline)

| Cell | Sharpe | Calmar | 12m return std | Avg DD depth % | Annual turnover % | Regression flags |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 1.85 (+0.0%) | 0.95 (+0.0%) | 0.28 (+0.0%) | 5.44 (+0.0%) | 473.85 (+0.0%) | None |
| ablate_rank_exit | 1.89 (+2.2%) | 0.97 (+2.1%) | 0.29 (+1.5%) | 5.49 (+0.9%) | 450.55 (-4.9%) | None |
| ablate_vol_stop | 1.62 (-12.7%) | 0.82 (-13.0%) | 0.30 (+7.6%) | 6.26 (+15.0%) | 382.39 (-19.3%) | None |
| ablate_bear_exposure | 1.74 (-6.0%) | 0.77 (-18.4%) | 0.30 (+5.7%) | 6.01 (+10.4%) | 493.89 (+4.2%) | calmar |
| ablate_vol_target | 1.77 (-4.1%) | 1.00 (+5.2%) | 0.35 (+24.0%) | 5.45 (+0.1%) | 486.57 (+2.7%) | stability |
| ablate_corr_guard | 1.85 (-0.2%) | 0.95 (-0.1%) | 0.28 (-0.1%) | 5.39 (-1.0%) | 473.66 (-0.0%) | None |
| ablate_positive_momentum | 1.84 (-0.6%) | 0.93 (-2.2%) | 0.28 (-0.3%) | 5.43 (-0.2%) | 471.11 (-0.6%) | None |

### Late ablation — value (relative change vs baseline)

| Cell | Sharpe | Calmar | 12m return std | Avg DD depth % | Annual turnover % | Regression flags |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 1.88 (+0.0%) | 1.52 (+0.0%) | 0.29 (+0.0%) | 5.45 (+0.0%) | 688.88 (+0.0%) | None |
| ablate_rank_exit | 1.93 (+2.4%) | 1.68 (+10.2%) | 0.29 (-1.2%) | 5.49 (+0.8%) | 658.29 (-4.4%) | None |
| ablate_vol_stop | 1.36 (-27.9%) | 0.92 (-39.9%) | 0.32 (+11.0%) | 6.68 (+22.6%) | 559.68 (-18.8%) | sharpe, calmar, average_dd_pct |
| ablate_bear_exposure | 1.97 (+4.6%) | 1.83 (+20.2%) | 0.29 (-0.8%) | 5.46 (+0.3%) | 696.17 (+1.1%) | None |
| ablate_vol_target | 1.89 (+0.3%) | 1.54 (+0.9%) | 0.29 (-0.1%) | 5.48 (+0.5%) | 687.42 (-0.2%) | None |
| ablate_corr_guard | 1.88 (+0.0%) | 1.52 (+0.0%) | 0.29 (+0.0%) | 5.45 (+0.0%) | 688.88 (+0.0%) | None |
| ablate_positive_momentum | 1.88 (-0.1%) | 1.52 (-0.2%) | 0.29 (-1.3%) | 5.45 (+0.0%) | 689.18 (+0.0%) | None |

### Extreme-day sensitivity

| Cell | Date | Portfolio day | Candidate name | Close before → after | Stock day | Sharpe → zero whole day |
| --- | --- | --- | --- | --- | --- | --- |
| early | 2004-04-28 | 22.49% | BAJAJHIND | 44.16 → 462.88 | 948.19% | 1.85 → 1.96 |
| early | 2004-07-08 | 11.22% | BOSCHLTD | 1386.12 → 13324.50 | 861.28% | 1.85 → 1.84 |
| late_probe_band_500_1000 | 2017-12-07 | 253.07% | TIL | 2.85 → 146.50 | 5040.35% | 0.63 → 1.89 |
| late_probe_band_500_1000 | 2021-04-12 | -5.96% | PANAMAPET | 168.55 → 150.20 | -10.89% | 0.63 → 0.63 |
| late_probe_positions_36 | 2018-02-07 | 119.22% | TIL | 2.85 → 149.10 | 5131.58% | 0.95 → 1.88 |
| late_probe_positions_36 | 2024-06-04 | -8.01% | BHEL | 311.45 → 246.55 | -20.84% | 0.95 → 0.97 |

| Method / limitation | Setting |
| --- | --- |
| Sweep | Lookback 7/10/12/14/17 months; positions 18/24/30/36/42; stops 9/12/15/18/21%; regime cutoffs −6/−8/−10/−12/−14%. |
| Rebalance | Integer monthly cadence 1/2/3; ±20% of 2 rounds to 2. |
| Ablation | Six leave-one-out components; Sharpe/Calmar ≤15% regression; stability/DD ≤20%; turnover ≤25%. No winner selected. |
| Extreme-day test | Sets the entire portfolio day to zero without recomputing holdings; not an adjusted backtest. Candidate ticker is based on trade dates, not exact intraday attribution. |
| Costs | Same 0.3% one-way cost in every liquidity band; wider-band performance has a capacity caveat. Turnover is half the absolute weight-change sum. |
| Status | Numerical cliffs and data-quality issues prevent a robustness pass. |

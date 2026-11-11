# Stage 2 — Core signal diagnostics

**Verdict: FAIL / INCOMPLETE**

| Universe card | Setting |
| --- | --- |
| Source | 5,205 raw OHLCV CSVs; 2000-01-03 to 2026-10-30 |
| Eligibility | ₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters |
| Portfolio / costs | 30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0% |
| Windows | Early 2001–2012; late 2013–2026-10-30; full 2002–2025-12-31 |
| Accounting convention | Exit-day gains/losses omitted at user request |
| Stage 1 status | Data adjustment unresolved; survivorship coverage flagged |

### Filter ladder — three-month forward return

| Window | Rung | Months | Mean IC | ICIR | NW-t | Excluded |
| --- | --- | --- | --- | --- | --- | --- |
| early | L0_raw | 104 | 0.0598 | 0.476 | 3.03 | 26.24% |
| early | L1_price | 104 | 0.0690 | 0.551 | 3.54 | 26.24% |
| early | L2_liquidity | 104 | 0.0816 | 0.603 | 3.88 | 26.24% |
| early | L3_tradeable | 100 | 0.0427 | 0.302 | 2.03 | 29.08% |
| early | L4_positive | 97 | 0.0329 | 0.252 | 1.74 | 31.21% |
| early | L5_top30 | 97 | -0.0276 | -0.142 | -1.22 | 31.21% |
| late | L0_raw | 163 | 0.0295 | 0.332 | 2.84 | 0.00% |
| late | L1_price | 163 | 0.0416 | 0.449 | 3.95 | 0.00% |
| late | L2_liquidity | 163 | 0.0671 | 0.576 | 5.07 | 0.00% |
| late | L3_tradeable | 163 | 0.0477 | 0.436 | 3.90 | 0.00% |
| late | L4_positive | 163 | 0.0332 | 0.344 | 3.09 | 0.00% |
| late | L5_top30 | 163 | -0.0021 | -0.011 | -0.12 | 0.00% |

### Horizon decay

| Window | Months forward | L0 IC | L0 NW-t | L3 IC | L3 NW-t | L3 excluded |
| --- | --- | --- | --- | --- | --- | --- |
| early | 1 | 0.0437 | 3.22 | 0.0408 | 2.54 | 28.67% |
| early | 3 | 0.0598 | 3.03 | 0.0427 | 2.03 | 29.08% |
| early | 6 | 0.0677 | 2.39 | 0.0347 | 1.11 | 29.71% |
| early | 12 | 0.0429 | 1.22 | 0.0108 | 0.28 | 30.30% |
| late | 1 | 0.0194 | 2.90 | 0.0442 | 5.30 | 0.00% |
| late | 3 | 0.0295 | 2.84 | 0.0477 | 3.90 | 0.00% |
| late | 6 | 0.0320 | 2.15 | 0.0405 | 2.55 | 0.00% |
| late | 12 | 0.0140 | 0.76 | 0.0106 | 0.62 | 0.00% |

### L3 quantiles

| Window | Horizon | Q1 | Q2 | Q3 | Q4 | Q5 | Increasing pairs | Spread NW-t | ≥80% and ≥2 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| early | 1 | 1.43% | 2.25% | 2.33% | 2.31% | 2.43% | 3/4 (75%) | 1.96 | FAIL |
| early | 3 | 4.98% | 5.92% | 6.77% | 6.56% | 6.94% | 3/4 (75%) | 1.67 | FAIL |
| early | 6 | 10.46% | 12.24% | 13.37% | 13.11% | 12.93% | 2/4 (50%) | 0.95 | FAIL |
| early | 12 | 22.21% | 24.45% | 26.33% | 22.47% | 23.43% | 3/4 (75%) | 0.21 | FAIL |
| late | 1 | 0.99% | 2.44% | 1.82% | 2.13% | 2.28% | 3/4 (75%) | 4.58 | FAIL |
| late | 3 | 4.29% | 6.58% | 5.95% | 6.64% | 6.93% | 3/4 (75%) | 3.59 | FAIL |
| late | 6 | 10.60% | 12.59% | 13.19% | 13.70% | 14.46% | 4/4 (100%) | 2.62 | PASS |
| late | 12 | 26.07% | 28.68% | 28.23% | 27.97% | 28.34% | 2/4 (50%) | 0.91 | FAIL |

### Three-month gate checks

| Window | Check | Measured | Bar | Result |
| --- | --- | --- | --- | --- |
| early | L0 / L3 NW-t | 3.03 / 2.03 | both ≥2 | PASS |
| early | L3 months excluded | 29.08% | ≤15% | FAIL |
| early | Top two years share of signed IC | 67.19% | ≤50% | CONCENTRATED |
| early | Equal / traded-value-weighted IC | 0.0427 / 0.0465 | market-value weighting requested | INCOMPLETE: no point-in-time market cap |
| early | Raw / forward-filled IC | 0.0427 / 0.0425 | delta -0.00029 | PROXY ONLY: delistings unverified |
| late | L0 / L3 NW-t | 2.84 / 3.90 | both ≥2 | PASS |
| late | L3 months excluded | 0.00% | ≤15% | PASS |
| late | Top two years share of signed IC | 38.29% | ≤50% | PASS |
| late | Equal / traded-value-weighted IC | 0.0477 / 0.0506 | market-value weighting requested | INCOMPLETE: no point-in-time market cap |
| late | Raw / forward-filled IC | 0.0477 / 0.0475 | delta -0.00018 | PROXY ONLY: delistings unverified |

| Method | Setting |
| --- | --- |
| Signal | Spearman rank correlation; month-end close-to-close forward returns. |
| NW-t | Bartlett Newey–West lag = horizon; missing calendar months remain gaps. |
| Ranking | L3 includes trend, falling-knife and age; L5 is top 30 before hysteresis. |
| Weighting | Traded-value weights are a liquidity proxy, not market-cap weights. |
| Survivorship | IC is a potentially survivorship-biased upper bound; forward-fill sensitivity is not verified delisting treatment. |
| Stage result | Three-month early breadth and both windows’ monotonicity fail; data prerequisites remain unresolved. |

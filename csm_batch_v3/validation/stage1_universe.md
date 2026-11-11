**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Stage 1 — Universe and data integrity

**Verdict: MAJOR DIVERGENCE in the 2015–2025 core universes; source adjustment and survivorship remain unresolved.** Core set = liquidity ranks 1–250, 1–500, 1–750, 1–1000 and 1–1500; separate bands are stress tests. A band `500–1000` means rank >500 and ≤1000. Ranks are based on the 63-day median traded value, with 21 observations minimum and a one-day shift. Filters use price > ₹10, listing age ≥252 observed bars within the loaded panel, circuit count ≤5, trend/falling-knife tests and the configured ADX/high52 gates. Portfolios start flat after a 450-calendar-day indicator warmup.

## 2015–2025 universe sweep

| Liquidity rank | CAGR % | Sharpe | Δ Sharpe | Max DD % | Calmar | Δ Calmar | 3m IC | IC NW-t | Median eligible | Months <8 % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 19.428 | 1.235 | -0.605 | -23.862 | 0.814 | -0.708 | 0.020 | 0.724 | 23.000 | 14.394 |
| 1–250 | 22.940 | 1.404 | -0.436 | -31.948 | 0.718 | -0.805 | 0.037 | 1.550 | 57.000 | 3.030 |
| 1–500 | 30.161 | 1.790 | -0.051 | -22.320 | 1.351 | -0.171 | 0.027 | 1.589 | 116.500 | 1.515 |
| 1–750 | 29.833 | 1.736 | -0.104 | -22.623 | 1.319 | -0.204 | 0.017 | 1.187 | 147.000 | 1.515 |
| 1–1000 | 32.139 | 1.840 | 0.000 | -21.108 | 1.523 | 0.000 | 0.022 | 1.603 | 183.500 | 0.758 |
| 1–1500 | 37.241 | 2.092 | 0.251 | -19.025 | 1.957 | 0.435 | 0.027 | 2.253 | 225.500 | 0.758 |
| 0–500 | 30.161 | 1.790 | -0.051 | -22.320 | 1.351 | -0.171 | 0.027 | 1.589 | 116.500 | 1.515 |
| 500–1000 | 32.653 | 1.755 | -0.085 | -22.056 | 1.480 | -0.042 | 0.012 | 0.647 | 75.000 | 3.788 |
| 1000–1500 | 36.548 | 1.986 | 0.146 | -22.327 | 1.637 | 0.114 | 0.015 | 1.000 | 41.000 | 7.576 |
| 1000–2000 | 36.250 | 2.019 | 0.178 | -32.005 | 1.133 | -0.390 | 0.023 | 1.542 | 66.500 | 5.303 |

## 2005–2014 universe sweep

| Liquidity rank | CAGR % | Sharpe | Δ Sharpe | Max DD % | Calmar | Δ Calmar | 3m IC | IC NW-t | Median eligible | Months <8 % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 23.139 | 1.306 | -0.997 | -37.328 | 0.620 | -0.889 | 0.103 | 3.582 | 20.000 | 25.833 |
| 1–250 | 37.793 | 1.944 | -0.359 | -27.669 | 1.366 | -0.143 | 0.099 | 4.800 | 49.500 | 14.167 |
| 1–500 | 39.546 | 2.137 | -0.166 | -24.290 | 1.628 | 0.119 | 0.075 | 4.263 | 93.500 | 9.167 |
| 1–750 | 44.326 | 2.284 | -0.019 | -27.306 | 1.623 | 0.114 | 0.067 | 3.890 | 116.500 | 9.167 |
| 1–1000 | 45.237 | 2.303 | 0.000 | -29.981 | 1.509 | 0.000 | 0.071 | 4.416 | 126.500 | 9.167 |
| 1–1500 | 45.495 | 2.311 | 0.008 | -31.343 | 1.452 | -0.057 | 0.079 | 4.815 | 131.500 | 9.167 |
| 0–500 | 39.546 | 2.137 | -0.166 | -24.290 | 1.628 | 0.119 | 0.075 | 4.263 | 93.500 | 9.167 |
| 500–1000 | 27.872 | 1.696 | -0.607 | -43.841 | 0.636 | -0.873 | 0.105 | 5.700 | 19.000 | 35.833 |
| 1000–1500 | 18.977 | 1.644 | -0.659 | -21.301 | 0.891 | -0.618 | 0.166 | 4.789 | 0.500 | 72.500 |
| 1000–2000 | 18.932 | 1.637 | -0.666 | -21.301 | 0.889 | -0.620 | 0.168 | 4.756 | 0.500 | 72.500 |

Δ is each universe minus 1–1000 in the same window; negative Max DD is loss from peak. IC is the strategy’s 3-month cross-sectional Spearman IC, with HAC lag 3. Months <8 are computed on eligible factor breadth before requiring future observations.

## Core-universe dispersion gates

| Window | Sharpe range | Calmar range | CAGR range pp | DD range pp | Minimum Sharpe |
| --- | --- | --- | --- | --- | --- |
| early | 0.367 | 0.262 | 7.703 | 7.052 | 1.944 |
| late | 0.688 | 1.239 | 14.301 | 12.923 | 1.404 |

| Metric | Pass | Caution | Major divergence |
| --- | --- | --- | --- |
| Sharpe range | ≤0.35 | 0.35–0.60 | >0.60 |
| Calmar range | ≤0.50 | 0.50–0.90 | >0.90 |
| CAGR range | ≤8 pp | 8–15 pp | >15 pp |
| Max DD range | ≤10 pp | 10–18 pp | >18 pp |
| Any core Sharpe | >0 | — | ≤0 |

## Returns by year and universe (%)

| year | 1000–1500 | 1000–2000 | 500–1000 | 1–100 | 1–1000 | 1–1500 | 1–250 | 1–500 | 1–750 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2005.00 | 0.00 | 0.00 | -1.72 | 23.76 | 70.05 | 70.05 | 51.75 | 70.05 | 70.05 |
| 2006.00 | 0.00 | 0.00 | 8.82 | 37.44 | 58.30 | 58.30 | 47.80 | 58.30 | 58.30 |
| 2007.00 | 0.00 | 0.00 | 95.65 | 74.18 | 91.23 | 91.23 | 80.97 | 79.90 | 91.23 |
| 2008.00 | -5.55 | -7.32 | -29.98 | -26.72 | -19.92 | -21.47 | -15.14 | -10.61 | -16.36 |
| 2009.00 | 20.60 | 23.16 | 92.25 | 72.71 | 76.85 | 76.85 | 116.73 | 66.72 | 72.87 |
| 2010.00 | 61.66 | 61.66 | 30.41 | 17.69 | 49.02 | 52.34 | 33.60 | 25.45 | 30.64 |
| 2011.00 | -15.96 | -15.88 | -20.75 | -9.45 | -14.95 | -12.17 | -8.47 | -13.91 | -13.18 |
| 2012.00 | 58.72 | 58.72 | 71.29 | 41.24 | 58.86 | 57.50 | 39.22 | 65.10 | 61.93 |
| 2013.00 | -9.00 | -9.00 | -1.34 | 4.88 | 15.72 | 15.72 | 8.50 | 15.06 | 15.28 |
| 2014.00 | 153.86 | 152.17 | 137.01 | 35.15 | 144.95 | 142.96 | 78.41 | 88.50 | 147.98 |

| year | 1000–1500 | 1000–2000 | 500–1000 | 1–100 | 1–1000 | 1–1500 | 1–250 | 1–500 | 1–750 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015.00 | 19.53 | 20.00 | 73.84 | 1.39 | 41.05 | 46.86 | 13.19 | 33.29 | 32.94 |
| 2016.00 | 62.60 | 73.88 | 40.13 | 11.10 | 49.79 | 63.69 | 6.64 | 27.71 | 29.07 |
| 2017.00 | 58.70 | 53.34 | 49.31 | 28.34 | 38.10 | 41.15 | 79.52 | 38.04 | 48.14 |
| 2018.00 | 2.35 | -13.29 | 0.10 | 6.48 | -5.98 | -3.67 | 1.56 | -1.53 | -3.89 |
| 2019.00 | -9.20 | -12.39 | -9.58 | 13.50 | 7.01 | 6.78 | 7.93 | 10.66 | 5.44 |
| 2020.00 | 92.37 | 88.28 | 69.79 | 51.52 | 76.09 | 78.16 | 77.66 | 80.27 | 83.64 |
| 2021.00 | 134.49 | 138.69 | 76.32 | 45.03 | 104.07 | 105.20 | 76.57 | 103.83 | 109.28 |
| 2022.00 | 18.09 | 7.13 | 18.47 | 15.15 | 11.35 | 3.57 | -5.17 | -6.71 | 4.60 |
| 2023.00 | 42.77 | 42.31 | 40.13 | 60.45 | 78.16 | 64.36 | 43.73 | 71.22 | 65.42 |
| 2024.00 | 36.29 | 61.11 | 37.93 | 2.16 | 10.76 | 41.91 | 7.89 | 21.02 | 13.58 |
| 2025.00 | 3.50 | 11.91 | -0.88 | -2.76 | -7.52 | 5.49 | -11.54 | -0.16 | -9.22 |

## Year concentration: 1–1000

| Window | Positive years | Negative years | Top 2 positive years / total signed log growth % |
| --- | --- | --- | --- |
| early | 8 | 2 | 41.42 |
| late | 9 | 2 | 42.11 |

The contribution of the two highest positive years is divided by total signed log growth, including down years. This is a concentration diagnostic, not an independent-sample test.

## Leave one year out: 1–1000

These are fixed-return-series diagnostics: the omitted year is removed, remaining daily returns are stitched together and annualized using 252 trading days. They are **not** fresh backtests or causal estimates of each year’s contribution.

### 2005–2014

| Year omitted | CAGR % | Sharpe | Max DD % |
| --- | --- | --- | --- |
| 2005.00 | 43.48 | 2.21 | -29.98 |
| 2006.00 | 44.62 | 2.27 | -29.98 |
| 2007.00 | 41.54 | 2.18 | -29.98 |
| 2008.00 | 56.05 | 2.73 | -22.82 |
| 2009.00 | 42.66 | 2.23 | -29.98 |
| 2010.00 | 45.66 | 2.24 | -29.98 |
| 2011.00 | 55.03 | 2.61 | -29.98 |
| 2012.00 | 44.58 | 2.19 | -32.54 |
| 2013.00 | 49.82 | 2.39 | -29.98 |
| 2014.00 | 37.55 | 1.98 | -29.98 |

### 2015–2025

| Year omitted | CAGR % | Sharpe | Max DD % |
| --- | --- | --- | --- |
| 2015.00 | 31.82 | 1.81 | -21.11 |
| 2016.00 | 31.02 | 1.79 | -21.11 |
| 2017.00 | 32.13 | 1.79 | -21.11 |
| 2018.00 | 37.33 | 2.04 | -21.11 |
| 2019.00 | 35.52 | 1.92 | -21.11 |
| 2020.00 | 28.94 | 1.68 | -21.11 |
| 2021.00 | 26.97 | 1.58 | -21.11 |
| 2022.00 | 35.02 | 1.96 | -21.11 |
| 2023.00 | 28.70 | 1.64 | -21.11 |
| 2024.00 | 35.11 | 1.97 | -19.40 |
| 2025.00 | 37.63 | 2.05 | -17.92 |

## Source audit

| Check | Result | Meaning |
| --- | --- | --- |
| CSV files | 5205 | OHLCV source |
| First / last valid close | 2000-01-03 / 2026-10-30 | Data observed |
| Last seen >183 days before panel end | 57 / 5205 (1.10%) | Survivorship proxy; below the playbook’s 2% flag; not proof of delistings |
| Duplicate-date observations | 54930 | Audit counts same-date rows; loader keeps the last exact duplicate timestamp |
| Out-of-order observations | 805 | Loader sorts date index |
| Invalid/nonpositive closes | 1008 | Source audit count |
| Adjacent valid close jumps below −40% or above +300% | 946 | Adjustment/anomaly review needed; not automatically confirmed errors or corporate actions |
| Mask events / nullified bars, late load including warmup | 327 / 634 | Events are based on the loaded 2013–2025 panel; counts differ from the full-source audit |
| Source CSV metadata changed during validation | 1020 | An independent updater changed the live source; added 0, removed 0. Final tests use the frozen snapshot. |

The mask drops an event bar and its next bar in memory; it does **not** adjust a price series for a split or establish that remaining raw observations are economically comparable. It can also use the event-day close to alter that day’s opening fill: see [Stage 3](stage3_robustness_lookahead.md). All P&L and IC results retain this unresolved caveat. [Full audit](evidence/data_audit.json), [data manifest](evidence/data_manifest.csv), [universe runs](evidence/late_universe_cells.csv).

**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Stage 1 — Universe, data and year robustness

**Verdict: PASS core-universe dispersion in both reference windows; caution for source adjustment, survivorship and the 501–1000 anomaly.** A band 500–1000 means ranks >500 and ≤1000. Liquidity rank uses shifted 63-day median traded value, minimum 21 observations; entry filters include price, 252 observed listing bars, circuit days, trend and falling-knife rules. ETF exposure is part of every portfolio.

## 2015–2025 universe sweep

| Liquidity rank | CAGR % | Sharpe | Δ Sharpe | Max DD % | Calmar | Δ Calmar | 3m IC | NW-t | Median pool | Months <8 % | ETF exposure % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 20.028 | 1.436 | -0.390 | -17.989 | 1.113 | -0.404 | 0.047 | 1.936 | 61.000 | 0.758 | 26.994 |
| 1–250 | 26.254 | 1.750 | -0.076 | -17.748 | 1.479 | -0.039 | 0.043 | 2.536 | 145.000 | 0.000 | 27.928 |
| 1–500 | 26.897 | 1.811 | -0.015 | -19.240 | 1.398 | -0.120 | 0.045 | 3.248 | 278.500 | 0.000 | 28.012 |
| 1–750 | 30.672 | 1.978 | 0.152 | -16.747 | 1.831 | 0.314 | 0.039 | 2.980 | 396.500 | 0.000 | 28.090 |
| 1–1000 | 27.742 | 1.826 | 0.000 | -18.278 | 1.518 | 0.000 | 0.037 | 2.914 | 503.500 | 0.000 | 28.580 |
| 1–1500 | 31.264 | 2.041 | 0.215 | -16.759 | 1.866 | 0.348 | 0.032 | 2.722 | 686.500 | 0.000 | 28.513 |
| 0–500 | 26.897 | 1.811 | -0.015 | -19.240 | 1.398 | -0.120 | 0.045 | 3.248 | 278.500 | 0.000 | 28.012 |
| 500–1000 | 50.420 | 0.693 | -1.133 | -15.963 | 3.159 | 1.641 | 0.018 | 1.303 | 234.000 | 0.758 | 30.573 |
| 1000–1500 | 39.630 | 2.468 | 0.643 | -20.241 | 1.958 | 0.440 | 0.023 | 1.856 | 163.500 | 0.758 | 31.513 |
| 1000–2000 | 40.338 | 2.522 | 0.696 | -19.495 | 2.069 | 0.551 | 0.029 | 2.684 | 240.500 | 0.000 | 31.545 |

## 2005–2014 universe sweep

| Liquidity rank | CAGR % | Sharpe | Δ Sharpe | Max DD % | Calmar | Δ Calmar | 3m IC | NW-t | Median pool | Months <8 % | ETF exposure % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 29.279 | 1.712 | -0.609 | -28.348 | 1.033 | -0.277 | 0.068 | 2.538 | 62.500 | 3.333 | 14.745 |
| 1–250 | 31.907 | 1.981 | -0.341 | -28.955 | 1.102 | -0.208 | 0.063 | 2.521 | 144.500 | 2.500 | 14.133 |
| 1–500 | 34.778 | 2.157 | -0.165 | -29.558 | 1.177 | -0.133 | 0.062 | 2.849 | 250.500 | 2.500 | 13.501 |
| 1–750 | 36.040 | 2.222 | -0.099 | -30.439 | 1.184 | -0.126 | 0.056 | 2.851 | 312.000 | 2.500 | 13.455 |
| 1–1000 | 38.199 | 2.321 | 0.000 | -29.170 | 1.310 | 0.000 | 0.062 | 3.404 | 330.000 | 2.500 | 13.461 |
| 1–1500 | 37.935 | 2.305 | -0.016 | -29.305 | 1.294 | -0.015 | 0.061 | 3.380 | 335.500 | 1.667 | 13.550 |
| 0–500 | 34.778 | 2.157 | -0.165 | -29.558 | 1.177 | -0.133 | 0.062 | 2.849 | 250.500 | 2.500 | 13.501 |
| 500–1000 | 35.478 | 2.329 | 0.008 | -25.574 | 1.387 | 0.078 | 0.093 | 4.241 | 67.000 | 21.667 | 14.948 |
| 1000–1500 | 22.537 | 1.667 | -0.654 | -19.526 | 1.154 | -0.155 | 0.116 | 4.322 | 4.500 | 52.500 | 23.995 |
| 1000–2000 | 23.866 | 1.764 | -0.557 | -19.526 | 1.222 | -0.087 | 0.113 | 4.177 | 5.000 | 52.500 | 24.179 |

## Core-universe dispersion: 1–250, 1–500, 1–750, 1–1000, 1–1500

| Period | Sharpe range | Calmar range | CAGR range pp | MaxDD range pp | Min Sharpe |
| --- | --- | --- | --- | --- | --- |
| early | 0.341 | 0.208 | 6.292 | 1.484 | 1.981 |
| late | 0.291 | 0.468 | 5.010 | 2.493 | 1.750 |

| Measure | Pass | Caution | Major divergence |
| --- | --- | --- | --- |
| Sharpe range | ≤0.35 | 0.35–0.60 | >0.60 |
| Calmar range | ≤0.50 | 0.50–0.90 | >0.90 |
| CAGR range | ≤8 pp | 8–15 pp | >15 pp |
| MaxDD range | ≤10 pp | 10–18 pp | >18 pp |
| Any core Sharpe | >0 | — | ≤0 |

## Annual returns (%) by universe

| year | 1000–1500 | 1000–2000 | 500–1000 | 1–1000 | 1–1500 | 1–250 | 1–500 | 1–750 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2005 | 0.00 | 0.00 | -0.54 | 53.11 | 53.11 | 45.29 | 53.11 | 53.11 |
| 2006 | 0.00 | 0.00 | 4.24 | 37.85 | 37.85 | 30.55 | 37.82 | 37.85 |
| 2007 | 11.69 | 11.69 | 84.86 | 76.12 | 76.12 | 64.98 | 73.75 | 76.12 |
| 2008 | 11.73 | 11.73 | -11.36 | -14.60 | -14.76 | -15.09 | -15.75 | -16.35 |
| 2009 | 81.88 | 79.17 | 116.69 | 90.77 | 90.58 | 93.60 | 83.91 | 81.61 |
| 2010 | 41.07 | 61.60 | 54.59 | 36.75 | 38.30 | 37.50 | 47.05 | 33.91 |
| 2011 | -5.97 | -12.06 | -6.47 | -4.21 | -5.75 | -10.02 | -6.89 | -6.42 |
| 2012 | 13.56 | 36.67 | 41.98 | 38.52 | 37.54 | 29.00 | 29.02 | 31.25 |
| 2013 | 5.96 | 7.41 | 12.33 | 9.73 | 10.64 | 10.20 | 4.32 | 9.64 |
| 2014 | 110.26 | 81.88 | 144.66 | 110.09 | 107.48 | 75.80 | 88.39 | 112.57 |

| year | 1000–1500 | 1000–2000 | 500–1000 | 1–1000 | 1–1500 | 1–250 | 1–500 | 1–750 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 34.84 | 37.29 | 37.56 | 13.89 | 19.37 | 7.89 | 10.96 | 12.09 |
| 2016 | 32.41 | 35.63 | 16.66 | 24.26 | 31.90 | -2.98 | 3.70 | 18.65 |
| 2017 | 84.99 | 84.55 | 403.81 | 42.98 | 40.98 | 41.85 | 41.52 | 49.08 |
| 2018 | -1.76 | -6.86 | 1.27 | -3.91 | -3.45 | -2.65 | -3.70 | -2.15 |
| 2019 | 4.90 | 4.80 | 12.86 | 20.87 | 19.13 | 21.10 | 19.25 | 21.12 |
| 2020 | 67.69 | 67.61 | 76.61 | 56.60 | 52.31 | 67.66 | 58.17 | 58.65 |
| 2021 | 79.14 | 82.04 | 119.27 | 78.36 | 89.41 | 88.04 | 78.40 | 93.72 |
| 2022 | 36.92 | 20.80 | 11.06 | 7.98 | 6.54 | 10.59 | 7.90 | 16.05 |
| 2023 | 53.65 | 49.20 | 47.86 | 55.31 | 55.76 | 53.67 | 63.09 | 63.33 |
| 2024 | 43.55 | 58.60 | 35.28 | 19.67 | 36.01 | 18.62 | 21.42 | 20.49 |
| 2025 | 27.31 | 42.04 | 12.11 | 12.13 | 19.84 | 16.74 | 21.78 | 14.93 |

## Leave one year out: baseline

These are fixed daily return series with one calendar year removed and remaining observations stitched together; CAGR is annualized using 252 trading days. They are not new backtests.

| removed_year | removed_year_return_pct | remaining_days | sharpe | delta_sharpe | calmar | cagr_tradingyear_pct | maxdd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2005 | 53.11 | 2232 | 2.26 | -0.06 | 1.28 | 37.28 | -29.17 |
| 2006 | 37.85 | 2233 | 2.30 | -0.02 | 1.33 | 38.89 | -29.17 |
| 2007 | 76.12 | 2234 | 2.18 | -0.14 | 1.20 | 35.09 | -29.17 |
| 2008 | -14.60 | 2237 | 2.91 | 0.59 | 3.62 | 46.50 | -12.85 |
| 2009 | 90.77 | 2240 | 2.14 | -0.18 | 1.16 | 33.77 | -29.17 |
| 2010 | 36.75 | 2231 | 2.30 | -0.02 | 1.34 | 39.06 | -29.17 |
| 2011 | -4.21 | 2236 | 2.51 | 0.19 | 1.53 | 44.65 | -29.17 |
| 2012 | 38.52 | 2232 | 2.25 | -0.07 | 1.33 | 38.84 | -29.17 |
| 2013 | 9.73 | 2233 | 2.41 | 0.09 | 1.46 | 42.52 | -29.17 |
| 2014 | 110.09 | 2239 | 2.00 | -0.32 | 1.11 | 32.34 | -29.17 |

| removed_year | removed_year_return_pct | remaining_days | sharpe | delta_sharpe | calmar | cagr_tradingyear_pct | maxdd_pct |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 13.89 | 2482 | 1.91 | 0.09 | 1.63 | 29.72 | -18.28 |
| 2016 | 24.26 | 2482 | 1.86 | 0.03 | 1.56 | 28.58 | -18.28 |
| 2017 | 42.98 | 2480 | 1.72 | -0.11 | 1.47 | 26.78 | -18.28 |
| 2018 | -3.91 | 2484 | 2.00 | 0.17 | 1.75 | 31.95 | -18.28 |
| 2019 | 20.87 | 2485 | 1.81 | -0.01 | 1.58 | 28.90 | -18.28 |
| 2020 | 56.60 | 2478 | 1.73 | -0.09 | 1.40 | 25.64 | -18.28 |
| 2021 | 78.36 | 2482 | 1.60 | -0.22 | 1.31 | 23.94 | -18.28 |
| 2022 | 7.98 | 2482 | 1.96 | 0.14 | 1.92 | 30.42 | -15.85 |
| 2023 | 55.31 | 2484 | 1.67 | -0.15 | 1.40 | 25.67 | -18.28 |
| 2024 | 19.67 | 2481 | 1.90 | 0.08 | 1.59 | 29.08 | -18.28 |
| 2025 | 12.13 | 2480 | 1.91 | 0.08 | 1.64 | 29.95 | -18.28 |

## Transaction-cost stress (stocks and ETF)

| cell | one_way_cost_pct | cagr_pct | sharpe | maxdd_pct | calmar |
| --- | --- | --- | --- | --- | --- |
| baseline | 0.300 | 27.742 | 1.826 | -18.278 | 1.518 |
| baseline | 0.600 | 19.525 | 1.334 | -20.195 | 0.967 |
| baseline | 0.900 | 11.822 | 0.849 | -26.278 | 0.450 |
| top_500 | 0.300 | 26.897 | 1.811 | -19.240 | 1.398 |
| top_500 | 0.600 | 18.902 | 1.320 | -21.107 | 0.895 |
| top_500 | 0.900 | 11.396 | 0.837 | -28.240 | 0.404 |
| band_500_1000 | 0.300 | 50.420 | 0.693 | -15.963 | 3.159 |
| band_500_1000 | 0.600 | 40.772 | 0.607 | -18.721 | 2.178 |
| band_500_1000 | 0.900 | 31.725 | 0.521 | -25.121 | 1.263 |
| band_1000_1500 | 0.300 | 39.630 | 2.468 | -20.241 | 1.958 |
| band_1000_1500 | 0.600 | 30.328 | 1.953 | -23.250 | 1.304 |
| band_1000_1500 | 0.900 | 21.631 | 1.441 | -27.454 | 0.788 |
| band_1000_2000 | 0.300 | 40.338 | 2.522 | -19.495 | 2.069 |
| band_1000_2000 | 0.600 | 30.940 | 1.998 | -23.293 | 1.328 |
| band_1000_2000 | 0.900 | 22.157 | 1.480 | -31.400 | 0.706 |

The cost sensitivity recomputes both stock and ETF charges from the same target-weight path; stop slippage remains fixed, and market impact is not modeled.

## Source-data checks

| Check | Result | Interpretation |
| --- | --- | --- |
| Stock files / last valid bar | 5205 / 2026-10-30 | Fixed test snapshot |
| Symbols last seen >183 days before panel end | 57 / 5205 (1.10%) | <2% flag; proxy, not verified delistings |
| Extreme adjacent valid-close changes ≤−40% or ≥+300% | 946 | Suspected actions/data anomalies, not individually verified |
| Duplicate-date observations | 54930 | Audit counts same-date rows; loader keeps last exact duplicate timestamp |
| First valid GOLDBEES close | 2007-03-19 | No ETF sleeve before availability |
| GOLDBEES largest observation gap | 2010-12-31 → 2015-01-01 (1462 calendar days) | No ETF rows for 2011–2014; marks are forward-filled and untradable sales may be forced |
| Snapshot hash mismatches | 0 / 5205 | See [snapshot verification](evidence/snapshot_verification.json) |

Corporate-action adjustment is not verified; returns are subject to source artifacts. See [Stage 3](stage3_robustness_lookahead.md) for TIL sensitivity and [ETF coverage](evidence/etf_coverage.csv).

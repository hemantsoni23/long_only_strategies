# Stage 1 — Strategy performance across liquidity universes

| Run setting | Value |
| --- | --- |
| Report window | 2015-01-01 to 2025-12-31; earlier history used only to warm indicators |
| Execution | Independent portfolio starts flat; first monthly decision anchored to 2014-12-31 |
| Baseline | Ranks 1–1000; 30 holdings; rebalance every 2 months |
| Costs / cash | 0.3% per leg; 0% cash return |
| Accounting | Exit-day gains/losses omitted at user request |

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

### Earlier window: 2005–2014

| Liquidity rank | CAGR | Sharpe | Δ Sharpe vs 1–1000 | Max DD | Calmar | Δ Calmar vs 1–1000 | 3m IC NW-t | Median pool | Months pool <30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1–100 | 25.19% | 1.67 | -0.79 | -26.84% | 0.94 | -0.33 | 2.54 | 62 | 20.00% |
| 1–250 | 28.41% | 2.05 | -0.42 | -28.57% | 0.99 | -0.27 | 2.52 | 144 | 9.17% |
| 1–500 | 31.64% | 2.27 | -0.19 | -28.86% | 1.10 | -0.17 | 2.85 | 250 | 5.83% |
| 1–750 | 33.02% | 2.35 | -0.11 | -28.31% | 1.17 | -0.10 | 2.85 | 312 | 5.83% |
| 1–1000 | 35.11% | 2.46 | 0.00 | -27.66% | 1.27 | 0.00 | 3.40 | 330 | 5.83% |
| 1–1500 | 34.84% | 2.44 | -0.02 | -27.77% | 1.25 | -0.01 | 3.38 | 336 | 5.00% |
| 501–1000 | 32.06% | 2.54 | 0.07 | -27.67% | 1.16 | -0.11 | 4.24 | 67 | 35.00% |
| 1001–1500 | 17.01% | 1.79 | -0.67 | -16.68% | 1.02 | -0.25 | 4.32 | 4 | 72.50% |
| 1001–2000 | 18.44% | 1.96 | -0.50 | -14.71% | 1.25 | -0.02 | 4.18 | 5 | 72.50% |

| Core 1–250 through 1–1500 | Measured range | Pass / caution / major | Result |
| --- | --- | --- | --- |
| Sharpe | 0.42 | ≤0.35 / ≤0.6 / >0.6 | CAUTION |
| Calmar | 0.27 | ≤0.5 / ≤0.9 / >0.9 | PASS |
| CAGR (pp) | 6.70 | ≤8 / ≤15 / >15 | PASS |
| Max DD (pp) | 1.19 | ≤10 / ≤18 / >18 | PASS |

### One-way transaction-cost stress

| Universe | Cost per leg | CAGR | Sharpe | Max DD | Calmar |
| --- | --- | --- | --- | --- | --- |
| baseline | 0.30% | 22.31% | 1.65 | -17.00% | 1.31 |
| baseline | 0.60% | 17.13% | 1.29 | -19.48% | 0.88 |
| baseline | 0.90% | 12.16% | 0.95 | -23.45% | 0.52 |
| top_500 | 0.30% | 21.59% | 1.64 | -17.81% | 1.21 |
| top_500 | 0.60% | 16.63% | 1.29 | -19.21% | 0.87 |
| top_500 | 0.90% | 11.85% | 0.95 | -22.84% | 0.52 |
| band_500_1000 | 0.30% | 42.15% | 0.62 | -16.74% | 2.52 |
| band_500_1000 | 0.60% | 36.20% | 0.56 | -19.26% | 1.88 |
| band_500_1000 | 0.90% | 30.49% | 0.51 | -23.34% | 1.31 |
| band_1000_1500 | 0.30% | 32.54% | 2.29 | -17.95% | 1.81 |
| band_1000_1500 | 0.60% | 26.78% | 1.92 | -22.98% | 1.17 |
| band_1000_1500 | 0.90% | 21.25% | 1.56 | -28.47% | 0.75 |
| band_1000_2000 | 0.30% | 33.20% | 2.35 | -20.29% | 1.64 |
| band_1000_2000 | 0.60% | 27.39% | 1.97 | -25.99% | 1.05 |
| band_1000_2000 | 0.90% | 21.83% | 1.60 | -31.29% | 0.70 |

### Calendar-year returns by universe

| Year | 1–250 | 1–500 | 1–1000 | 1–1500 | 501–1000 | 1001–1500 | 1001–2000 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2015 | 13.16% | 15.67% | 19.24% | 24.61% | 42.18% | 38.52% | 40.40% |
| 2016 | -0.85% | 7.88% | 30.43% | 35.58% | 20.48% | 32.68% | 36.18% |
| 2017 | 42.40% | 42.15% | 42.83% | 39.95% | 392.62% | 83.94% | 83.15% |
| 2018 | -2.13% | -2.98% | -3.23% | -2.92% | -1.41% | -1.79% | -6.93% |
| 2019 | 7.35% | 5.84% | 7.06% | 5.47% | -0.73% | -7.97% | -7.86% |
| 2020 | 53.28% | 45.35% | 42.67% | 38.48% | 57.18% | 50.15% | 51.13% |
| 2021 | 79.42% | 67.97% | 65.95% | 77.69% | 102.66% | 71.74% | 74.59% |
| 2022 | 7.80% | 4.35% | 4.70% | 2.60% | 7.18% | 31.95% | 15.99% |
| 2023 | 48.23% | 59.17% | 51.51% | 53.37% | 45.75% | 50.20% | 44.85% |
| 2024 | 15.27% | 17.64% | 17.36% | 33.15% | 28.14% | 34.13% | 49.53% |
| 2025 | -5.19% | -1.16% | -9.71% | -1.27% | -9.12% | 5.82% | 17.54% |

### Data and interpretation

| Check | Measured | Reading |
| --- | --- | --- |
| Last observed >183 days before data end | 57/5205 = 1.10% | Flag proxy <2%; not verified delistings |
| Extreme adjacent positive-close changes ≤−40% or ≥+300% | 946 | Candidates for data/action review; not all confirmed errors |
| Cost-stress method | 0.3%, 0.6%, 0.9% per leg | Weight path unchanged; stop slippage fixed; not a market-impact estimate |
| Band boundaries | 501–1000 means rank >500 and ≤1000 | No overlap with ranks 1–500 |
| Outliers | Raw source retained | See Stage 3 for ticker-exclusion sensitivity |

[2015–2025 universe results](evidence/late_universe_cells.csv) · [2005–2014 universe results](evidence/early_universe_cells.csv) · [Annual results](evidence/late_universe_yearly.csv) · [Cost stress](evidence/cost_stress.csv)

# Stage 4 — Independent IS/OOS and full-sample comparison

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

### Original playbook date split — supplemental

| Supplemental playbook split | OOS/IS Sharpe | OOS/IS Calmar | OOS/IS CAGR | OOS/IS max DD | OOS L0 3m NW-t | OOS L3 3m NW-t | OOS IC months <8 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A: 2001–2012 → 2013–present | 1.020 | 1.588 | 0.975 | 0.614 | 2.84 | 3.90 | 0.00% |
| B: 2013–present → 2001–2012 | 0.980 | 0.630 | 1.025 | 1.628 | 3.03 | 2.03 | 29.08% |

### Calendar-year baseline performance

| Window | Year | Return | Sharpe | Within-year max DD |
| --- | --- | --- | --- | --- |
| early | 2005 | 53.11% | 2.80 | -9.81% |
| early | 2006 | 37.85% | 2.57 | -12.42% |
| early | 2007 | 71.98% | 3.35 | -8.69% |
| early | 2008 | -21.04% | -2.64 | -26.02% |
| early | 2009 | 74.54% | 3.58 | -6.31% |
| early | 2010 | 32.05% | 2.43 | -8.55% |
| early | 2011 | -4.19% | -0.56 | -9.09% |
| early | 2012 | 38.52% | 3.59 | -6.29% |
| early | 2013 | 9.73% | 1.38 | -6.03% |
| early | 2014 | 110.09% | 5.27 | -6.24% |
| late | 2015 | 19.24% | 1.32 | -13.25% |
| late | 2016 | 30.43% | 1.91 | -16.15% |
| late | 2017 | 42.83% | 3.18 | -5.47% |
| late | 2018 | -3.23% | -0.26 | -9.61% |
| late | 2019 | 7.06% | 1.22 | -3.67% |
| late | 2020 | 42.67% | 2.74 | -7.58% |
| late | 2021 | 65.95% | 3.53 | -8.47% |
| late | 2022 | 4.70% | 0.38 | -17.00% |
| late | 2023 | 51.51% | 3.41 | -10.49% |
| late | 2024 | 17.36% | 1.14 | -11.93% |
| late | 2025 | -9.71% | -0.97 | -12.79% |

### Additional full scorecard

| Window | Sortino | Beta | Alpha / yr | Profit factor ($) | Payoff ratio | Average hold days |
| --- | --- | --- | --- | --- | --- | --- |
| 2005–2014 | 3.81 | 0.41 | 21.40% | N/A | 2.38 | 43.96 |
| 2015–2025 | 2.36 | 0.51 | 5.89% | N/A | 2.29 | 41.80 |
| 2002–2025 | 3.14 | 0.36 | 14.09% | N/A | 2.52 | 43.15 |

| Condition | Evidence |
| --- | --- |
| Independent starts | Each window is flat through warmup; indicator history only, selection starts at prior month-end. |
| Cost / cash | 0.3% per weight turnover; zero cash yield. |
| Exit accounting | Exit-day gains and losses omitted at user request; trade statistics follow the supplied convention. |
| Reporting periods | Early 2005–2014; late 2015–2025; no 2026 partial year in main comparison. |
| Stress regimes | 2008 in early; 2018, 2020 and 2022 in late. |
| OOS-look log | 2026-11-02–03: both periods and strategy results were viewed before this rerun; prior modification count is unknown. Ratios are retrospective, not blind holdouts. |
| Absolute IS/OOS Sharpe shift | 0.82; playbook specifies a ratio gate, not an absolute-delta gate. |
| Configuration selection | Original settings frozen; sweeps were run but no candidate was selected. |
| Replay consistency | Universe vs parameter baseline max equity difference 0 |
| Parity with original strategy class | Target-weight difference 0; equity difference 1.78e-15; warmup weight 0. |
| Benchmark / alpha | Equal-weight observed-stock return, daily clipped ±50%; zero cash yield. |
| PF ($) | Not derivable reliably from the weight-based trade log. |
| Full sample | 2002–2025 is informational and cannot replace independent split gates. |

[2005–2014 results](evidence/early_sweep_cells.csv) · [2015–2025 results](evidence/late_universe_cells.csv) · [Full-sample results](evidence/full_baseline_cells.csv)

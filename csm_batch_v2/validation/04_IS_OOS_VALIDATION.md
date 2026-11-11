# Stage 4 — Bidirectional IS/OOS validation

**Verdict: FAIL / NOT BLIND**

| Universe card | Setting |
| --- | --- |
| Source | 5,205 raw OHLCV CSVs; 2000-01-03 to 2026-10-30 |
| Eligibility | ₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters |
| Portfolio / costs | 30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0% |
| Windows | Early 2001–2012; late 2013–2026-10-30; full 2002–2025-12-31 |
| Accounting convention | Exit-day gains/losses omitted at user request |
| Stage 1 status | Data adjustment unresolved; survivorship coverage flagged |

### Scorecard

| Window | Sharpe | Sortino | Calmar | CAGR | Max DD | Beta | Alpha / yr | Trade win | PF (%) | PF ($) | Payoff | Avg hold days |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2001–2012 | 1.85 | 3.43 | 0.95 | 26.19% | -27.66% | 0.22 | 17.39% | 49.19% | 2.61 | N/A | 2.70 | 44.43 |
| 2013–2026-10-30 | 1.88 | 2.69 | 1.52 | 26.57% | -17.43% | 0.52 | 9.55% | 49.50% | 2.23 | N/A | 2.27 | 43.13 |
| 2002–2025-12-31 | 1.95 | 3.11 | 1.09 | 28.59% | -26.17% | 0.37 | 14.55% | 49.79% | 2.51 | N/A | 2.53 | 44.55 |

### Playbook split gates

| Direction | IS → OOS | Metric | Measured | Bar | Result |
| --- | --- | --- | --- | --- | --- |
| A | early → late | Sharpe OOS / IS | 1.017 | ≥0.60 | PASS |
| A | early → late | Calmar OOS / IS | 1.610 | ≥0.60 | PASS |
| A | early → late | CAGR OOS / IS | 1.014 | ≥0.50 | PASS |
| A | early → late | Max DD OOS / IS | 0.630 | ≤1.50 | PASS |
| A | early → late | OOS Sharpe | 1.882 | >0 | PASS |
| A | early → late | OOS L0 3m NW-t | 2.841 | ≥1.50 | PASS |
| A | early → late | OOS L3 3m NW-t | 3.902 | ≥1.50 | PASS |
| B | late → early | Sharpe OOS / IS | 0.983 | ≥0.60 | PASS |
| B | late → early | Calmar OOS / IS | 0.621 | ≥0.60 | PASS |
| B | late → early | CAGR OOS / IS | 0.986 | ≥0.50 | PASS |
| B | late → early | Max DD OOS / IS | 1.587 | ≤1.50 | FAIL |
| B | late → early | OOS Sharpe | 1.851 | >0 | PASS |
| B | late → early | OOS L0 3m NW-t | 3.032 | ≥1.50 | PASS |
| B | late → early | OOS L3 3m NW-t | 2.033 | ≥1.50 | PASS |

| Validation condition | Evidence | Verdict |
| --- | --- | --- |
| Replay vs original runner | 2731 rows; max difference 0 | PASS |
| Strategy file SHA-256 | 57c1171f6541e44a6db72ca65b759ae7196749eb422a95733c0871272ca08ba0 | VERSION |
| Backtest file SHA-256 | d3be9fac90075608287885005bd0788e5deb6fcc1401e20b4ffe30a82c39bea7 | VERSION |
| Both split directions clear all numeric gates | A and B above | FAIL |
| Previously untouched OOS | Both halves previously viewed | NOT BLIND |
| Independent tuning per direction | Baseline fixed before sweeps; no winner selected | No independent tuning claimed |
| Stress regime A OOS | 2018, 2020, 2022 present | COVERED |
| Stress regime B OOS | 2008 present | COVERED |
| Full sample | 2002 → latest complete year | INFORMATIONAL ONLY |
| Profit factor in currency | No reliable share-level P&L | N/A |
| Beta / alpha benchmark | Runner’s observed-stock equal-weight benchmark; return clipping ±50% | PROXY |

| OOS-look log | Date / result |
| --- | --- |
| Prior review | 2026-11-02: both full split windows and 2002–2025 viewed; user modified strategy during earlier review; modification count unknown |
| This validation | 2026-11-03: both full split windows and 2002–2025 full period viewed; no strategy changes |
| Post-look modification count | Unknown from available record; fresh untouched holdout not established |


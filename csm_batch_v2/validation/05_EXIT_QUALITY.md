# Stage 5 — Exit quality

**Verdict: DIAGNOSTIC / INCOMPLETE**

| Universe card | Setting |
| --- | --- |
| Source | 5,205 raw OHLCV CSVs; 2000-01-03 to 2026-10-30 |
| Eligibility | ₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters |
| Portfolio / costs | 30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0% |
| Windows | Early 2001–2012; late 2013–2026-10-30; full 2002–2025-12-31 |
| Accounting convention | Exit-day gains/losses omitted at user request |
| Stage 1 status | Data adjustment unresolved; survivorship coverage flagged |

### Post-exit continuation

| Reason | Exits | 20d & 60d available | 20d excess | 60d excess | Mean excess | Rule verdict | Sample |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HARD_STOP_HIT | 775 | 761 | 0.71% | -0.47% | 0.12% | neutral | ≥30 |
| VOL_STOP_HIT | 1669 | 1629 | -0.48% | -0.52% | -0.50% | neutral | ≥30 |
| FORCE_EXIT | 13 | 13 | 11.29% | 0.76% | 6.02% | too early | <30; directional |
| RANK_EXIT | 1178 | 1170 | 0.18% | 0.39% | 0.29% | neutral | ≥30 |
| REBAL_EXIT | 432 | 421 | 0.54% | -1.30% | -0.38% | paired comparison | ≥30 |
| CRASH_GUARD | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| ATR_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| PEAK_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |

### Rotation comparisons — entered vs exited on same date

| Exit reason | Horizon | Matched dates | Entered mean | Exited mean | Difference |
| --- | --- | --- | --- | --- | --- |
| REBAL_EXIT | 20d | 108 | 2.89% | 0.67% | 2.22 pp |
| REBAL_EXIT | 60d | 108 | 5.43% | 2.75% | 2.68 pp |
| RANK_EXIT | 20d | 123 | 2.72% | 1.91% | 0.80 pp |
| RANK_EXIT | 60d | 122 | 6.34% | 5.74% | 0.60 pp |

| Check | Measured | Bar | Result |
| --- | --- | --- | --- |
| END_OF_PERIOD outside final month | 0 / 4093 | <5% | PASS |
| END_OF_PERIOD total | 26 / 4093 (0.64%) | <5% | PASS |
| FORCE_EXIT trades | 13 | ≥30 | DIRECTIONAL |
| Paired REBAL_EXIT | Same-date entry and exit groups | true replacement pairs | INCOMPLETE |

| Method / limitation | Setting |
| --- | --- |
| Excess return | Post-exit close-to-close return less equal-weight signal-eligible universe; 20d and 60d. |
| Benchmark | Daily constituent returns clipped ±50%; final membership carried forward after final factor month. |
| Verdict rule | Mean ≤−1% working; ≥+1% too early; otherwise neutral. |
| Rotation | Mean entries versus exits on same date; no one-to-one replacement mapping. |
| Data | Raw prices and missing/delisted endpoints limit reliability; fewer than 30 trades is directional only. |

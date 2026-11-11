# Stage 5 — Exit diagnostics, 2015–2025

| Reason | Exits | 20d & 60d available | 20d excess | 60d excess | Mean excess | Purpose verdict | Sample |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HARD_STOP_HIT | 406 | 401 | 0.98% | 0.12% | 0.55% | neutral | ≥30 |
| VOL_STOP_HIT | 850 | 841 | -0.05% | 2.49% | 1.22% | too early | ≥30 |
| FORCE_EXIT | 2 | 2 | -30.07% | -2.85% | -16.46% | working | <30: directional |
| RANK_EXIT | 683 | 683 | 0.06% | 1.08% | 0.57% | neutral | ≥30 |
| REBAL_EXIT | 230 | 227 | 2.58% | 2.48% | 2.53% | paired comparison | ≥30 |
| CRASH_GUARD | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| ATR_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |
| PEAK_STOP_HIT | 0 | 0 | N/A | N/A | N/A | Not triggered | <30 |

| Reason | Horizon | Paired dates | Entered mean | Exited mean | Entered − exited |
| --- | --- | --- | --- | --- | --- |
| REBAL_EXIT | 20d | 54 | 2.68% | 3.72% | -1.04 pp |
| REBAL_EXIT | 60d | 54 | 5.53% | 7.99% | -2.45 pp |
| RANK_EXIT | 20d | 63 | 1.56% | 0.97% | 0.59 pp |
| RANK_EXIT | 60d | 63 | 4.55% | 4.12% | 0.43 pp |

| Check | Measured | Threshold | Result |
| --- | --- | --- | --- |
| END_OF_PERIOD outside final month | 0/2200 | <5% | PASS |
| END_OF_PERIOD including final month | 29/2200 = 1.32% | <5% | PASS |
| Stop exits with zero opening target | 16/1258 | No later-bar override of scheduled open exit | FLAG |
| REBAL_EXIT matching | Same-date mean entrant vs mean exited | One-to-one replacement data | PROXY |
| FORCE_EXIT usable 20/60d | 2 | ≥30 | DIRECTIONAL |

| Method / scope | Definition |
| --- | --- |
| Stop and rank exit | Average of 20- and 60-trading-day forward return less equal-weight L3 benchmark. ≤−1% working; ≥+1% too early; otherwise neutral. |
| Rebalance and rank rotation | Same-date average entrant return minus average exited return; not one-to-one stock replacement. |
| Benchmark | Signal-eligible equal-weight universe; daily constituent returns clipped ±50%; last membership carried forward after 2025. |
| Closed trades | Independent flat-start 2015–2025 portfolio; END_OF_PERIOD excluded from continuation verdict. |
| Limitations | Raw unadjusted prices, missing follow-ups and the execution-order problem limit validity; fewer than 30 is directional. |

[Exit summary](evidence/exit_summary.csv) · [Rotation comparisons](evidence/exit_rotations.csv) · [Trade log](evidence/late_universe_trades.csv)

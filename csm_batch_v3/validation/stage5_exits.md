**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Stage 5 — Exit quality

**Verdict: diagnostic only; rank exits are followed by +1.52% benchmark-relative return on average (n=116), meeting the playbook’s too-early threshold. Interpret all exits under the Stage 3 execution failures.** This analysis uses 2015–2025 baseline trades, and checks each exit against its intended purpose. All `END_OF_PERIOD` records are excluded from post-exit continuation. Results use source raw closes after each exit, with the same unresolved adjustment and survivorship limitations.

| Check | Result | Playbook reference |
| --- | --- | --- |
| Total exit records including artificial close-out | 1280 | — |
| END_OF_PERIOD count / share | 14 / 1.09% | <5% outside final months |
| END_OF_PERIOD outside final month | 0 | Expected 0 |
| Stop exits with a prior-bar target of zero | 12 / 682 | Candidate open-order conflicts; not all necessarily executable errors |

## Forward performance by exit reason

| reason | exits | available_both | mean20_pct | mean60_pct | mean20_60_pct | verdict | sample_quality |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FORCE_EXIT | 2 | 2 | -30.057 | -2.007 | -16.032 | working | directional (<30) |
| HARD_STOP_HIT | 201 | 198 | -1.561 | -0.511 | -1.036 | working | ≥30 |
| RANK_EXIT | 116 | 116 | 1.607 | 1.438 | 1.522 | too early | ≥30 |
| REBAL_EXIT | 468 | 467 | 0.577 | 1.177 | 0.877 | paired comparison | ≥30 |
| VOL_STOP_HIT | 479 | 473 | -1.292 | 0.236 | -0.528 | neutral | ≥30 |

Benchmarks are equal-weight signal-eligible-universe returns with daily constituent returns clipped to ±50% and the last monthly universe carried forward after the signal sample. Excess return is stock minus this benchmark. Mean20_60 is the simple average of the 20-day and 60-day means on exits having both observations. A stop mean ≤−1% is classified working, ≥+1% too early, otherwise neutral; buckets below 30 observations are directional only. This threshold should not be applied mechanically to rebalance exits.

## Same-date entrant vs exit group comparison

| reason | horizon_days | dates | entered_mean_pct | exited_mean_pct | difference_pp |
| --- | --- | --- | --- | --- | --- |
| REBAL_EXIT | 20 | 64 | 1.529 | 1.715 | -0.186 |
| REBAL_EXIT | 60 | 64 | 4.513 | 5.935 | -1.422 |
| RANK_EXIT | 20 | 46 | 1.302 | 1.023 | 0.279 |
| RANK_EXIT | 60 | 46 | 4.899 | 4.870 | 0.030 |

Entrants and exits are averaged as groups on the same dates. This is a **rotation proxy**, not one-to-one position matching and not a full causal counterfactual. It includes only dates where both sides have observable forward prices. The REBAL_EXIT row is relevant to the rebalance question; the RANK_EXIT row is supplementary. [Trade records](evidence/late_universe_trades.csv), [per-exit observations](evidence/exit_forward.csv), [open-order candidates](evidence/stop_open_ordering.csv).

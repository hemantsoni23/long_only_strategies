**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Stage 5 — Exit quality

**Verdict: diagnostic only.** Volatility-stop mean benchmark-relative continuation is +1.16% across 20 and 60 days on 831 exits, above the +1% too-early threshold. Rank exits are neutral at +0.62% on 692 exits. Interpret the per-reason table using the playbook thresholds and the execution-timing caveats in Stage 3.

| Check | Result | Gate |
| --- | --- | --- |
| Total exits, including artificial end-of-period | 2200 | — |
| END_OF_PERIOD share | 29/2200 (1.32%) | <5% outside final month |
| END_OF_PERIOD before final month | 0 | Expected 0 |
| Stop exits with zero prior-bar target | 0/1242 | Candidate ordering conflicts only; eligibility to exit must be checked individually |

## Per-exit forward outcome

| reason | exits | available_both | mean20_pct | mean60_pct | mean20_60_pct | verdict | sample_quality |
| --- | --- | --- | --- | --- | --- | --- | --- |
| HARD_STOP_HIT | 402 | 397 | 1.009 | 0.003 | 0.506 | neutral | ≥30 |
| RANK_EXIT | 692 | 692 | 0.073 | 1.174 | 0.624 | neutral | ≥30 |
| REBAL_EXIT | 237 | 234 | 2.201 | 2.788 | 2.494 | paired comparison | ≥30 |
| VOL_STOP_HIT | 840 | 831 | -0.061 | 2.379 | 1.159 | too early | ≥30 |

Post-exit benchmark is the equal-weight signal-eligible universe, with daily constituent returns clipped at ±50%; its final membership is carried forward. The mean is the average of 20- and 60-trading-day benchmark-relative returns on exits with both values. For stops, ≤−1% suggests working; ≥+1% suggests too early; between is neutral. Rank exits use the same diagnostic shape but call for a different review. Buckets under 30 are directional only. END_OF_PERIOD rows are excluded entirely. Raw source data and unresolved adjustment issues affect this analysis.

## Same-date entrant vs exit group comparison

| reason | horizon_days | dates | entered_mean_pct | exited_mean_pct | difference_pp |
| --- | --- | --- | --- | --- | --- |
| REBAL_EXIT | 20 | 54 | 2.681 | 3.749 | -1.069 |
| REBAL_EXIT | 60 | 54 | 5.535 | 8.323 | -2.788 |
| RANK_EXIT | 20 | 63 | 1.557 | 1.051 | 0.506 |
| RANK_EXIT | 60 | 63 | 4.547 | 4.636 | -0.089 |

This compares same-date group averages, not individually matched replacements. ETF performance is not attributed to stock exit rules. [Exit observations](evidence/exit_forward.csv) · [Trade log](evidence/late_universe_trades.csv).

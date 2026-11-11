**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Final verdict — CSM Batch v3

**NOT VALIDATED.** Three proven execution-timing lookahead failures and unresolved price-adjustment/survivorship limitations make the reported backtests unsuitable for a promotion decision. Core-universe dispersion and the configured 3-month signal also fail playbook checks in 2015–2025.

| Stage | Verdict | Key numbers | Report |
| --- | --- | --- | --- |
| 1. Universe & data | **Major divergence / data caveat** | 2015–2025 core Sharpe range 0.688 (limit 0.35), Calmar range 1.239 (limit 0.50); 1.10% stale-symbol proxy; 946 extreme source jumps | [Stage 1](stage1_universe.md) |
| 2. Signal | **Fail** | 2015–2025 L0 NW-t 2.40, configured L3 1.60 (both require ≥2); pre-ADX/high52 L3 2.92; quantile order 3/4; top-two-year signed-IC share 81.3% | [Stage 2](stage2_signal.md) |
| 3. Robustness & lookahead | **Fail** | 3/3 synthetic execution timing tests fail; actual-class parity max equity difference 3.6e-15; parameter and ablation details in report | [Stage 3](stage3_robustness_lookahead.md) |
| 4. IS/OOS | **Not blind; not validated** | Reference baseline Sharpe 2.30 → 1.84; Calmar 1.51 → 1.52; playbook early breadth <8: 34.0% of months; see both directional ratio tables | [Stage 4](stage4_is_oos.md) |
| 5. Exits | **Diagnostic only** | END_OF_PERIOD 14/1280 (1.09%); HARD_STOP_HIT: -1.04% (working, n=198), RANK_EXIT: +1.52% (too early, n=116), VOL_STOP_HIT: -0.53% (neutral, n=473) | [Stage 5](stage5_exits.md) |

The 3-month configured L3 IC decreased from 0.0289 in 2015–2022 to 0.0022 in 2023–2025; difference NW-t -0.91. The exploratory 2024–July 2026 signal IC is -0.0237 versus 0.0429 in 2013–2023 (difference NW-t -2.24); forward outcomes end in October 2026 and these periods are not fresh holdouts. These findings warrant review rather than a definitive causal conclusion.

Fix and independently retest execution timing and obtain verifiably adjusted, survivorship-aware data before interpreting the P&L as evidence. After fixes, rerun all five stages and evaluate a genuinely untouched holdout or future shadow data. The validation scripts did not modify the strategy source or data folder. A separate updater changed the live source during validation; all final tests use the fixed snapshot.

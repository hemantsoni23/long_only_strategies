**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# CSM Batch v3 validation summary

Read the [final verdict](VERDICT.md) for the concise decision. The five detailed, metric-first reports are:

1. [Universe and data](stage1_universe.md) — universe sweeps, year returns, dispersion, data quality.
2. [Signal and decay](stage2_signal.md) — factor IC, ICIR, ordinary and Newey–West t-statistics, horizons and accuracy.
3. [Robustness and lookahead](stage3_robustness_lookahead.md) — parameter sweeps, ablations, cost stress and causal tests.
4. [IS/OOS](stage4_is_oos.md) — both bidirectional historical comparisons and the full-window scorecard.
5. [Exit quality](stage5_exits.md) — per-reason continuation and rotation diagnostics.

The tested configuration is the source backtest’s default:

| Setting | Value |
| --- | --- |
| Factor | 12m and 6m volatility-normalized momentum; one-month lag |
| Universe | Liquidity rank ≤1000; price >₹10; ≥252 observed listing bars; ≤5 circuit bars |
| Signal gates | ADX ≥20 with +DI > −DI; price ≥85% of rolling 52-week high |
| Target | 15 equal-weight slots; 20% rank buffer; rebalance every 2 months |
| Stops | 15% from entry; ATR-at-entry trailing width 4×ATR/price, bounded 10%–25%; 5-calendar-day minimum hold; 20-calendar-day stop cooldown |
| Data mask | Daily raw close loss >40% or gain >300% masks event and next bar |
| Costs | 0.3% one-way traded value; configured stop slippage 0.3% |

The validated files have these SHA-256 hashes:

| File | SHA-256 |
| --- | --- |
| Strategy | `f483945a6a84c1efa508a3398e4a82744791d41a114f4e506a0b6a246a82d6ab` |
| Backtest | `575036b2aa07a2db55e418eb80cf5436a6fae6cba4174c91be4f1c0f5afb3b49` |
| Signal filters | `56bcd2b84c0b7aac3a8e599bdbb463c33948fabca134cbe9282670ec64e0ce10` |

[Raw evidence and reproducible scripts](evidence/) contain the complete cells and logs. The frozen snapshot is `/private/tmp/csm_batch_v3_validation_snapshot/ohlcv`; its [file hashes](evidence/snapshot_manifest.csv) are recorded. [Snapshot creation](evidence/make_snapshot.py) rebuilds and verifies this copy from the initially recorded byte lengths if the source prefixes remain available. The snapshot ends 2026-10-30 because the source was being updated during this work. An audit verified all 5,205 current file prefixes against hashes recorded during the initial audit; the 166 files updated before that audit were not content-hashed before their updates, so the initial prefix cannot be independently proven for those files. [Data integrity fingerprint](evidence/fingerprint_result.json) covers file count/size/modified-time metadata, not a before-and-after content hash of every CSV.

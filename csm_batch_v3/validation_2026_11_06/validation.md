**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Updated CSM Batch v3 validation

The [final verdict](VERDICT.md) summarizes the five stage reports. The current stock strategy has changed from the previous v3 validation; it no longer uses that version’s ADX/high52 gates or its corporate-action mask, and it now has a GOLDBEES sleeve. Returns are therefore not directly comparable as a one-variable change:

1. [Universe and data](stage1_universe.md)
2. [Signal and decay](stage2_signal.md)
3. [Robustness, ablation and lookahead](stage3_robustness_lookahead.md)
4. [Bidirectional IS/OOS and ETF](stage4_is_oos.md)
5. [Exit quality](stage5_exits.md)

| Default setting | Value |
| --- | --- |
| Factor | 12/6-month risk-normalized momentum, one-month lag |
| Stock universe | Liquidity ranks 1–1000, price >₹10, ≥252 observed listing bars; trend, circuit and falling-knife filters |
| Sizing / cadence | 30 stocks, inverse-volatility sizing, 2-month rebalance, maximum stock weight 5% |
| Risk | Bear scaling 60% / 30%, 20% vol target, correlation guard; 15% hard entry stop and 4× ATR-based volatility trail |
| Secondary sleeve | GOLDBEES, idle-cash sweep; ETF one-way cost 0.30%; buy band zero |
| Signal filter configuration | The prior ADX/52-week-high gates are not part of the current strategy source |

| Reviewed artifact | SHA-256 |
| --- | --- |
| Strategy | `57c1171f6541e44a6db72ca65b759ae7196749eb422a95733c0871272ca08ba0` |
| Backtest | `4de0b12cf908990f99a2cfda898c89d998fd1f6787d1b0e803274ed96b4f963d` |
| GOLDBEES source and copied data | `298ecb0afc7314b026050cf4f0e8529b1ac7e78242110d59e71695d6cee0d927` |

[Stock snapshot manifest](evidence/snapshot_manifest.csv) · [Snapshot verification](evidence/snapshot_verification.json) · [Source fingerprint](evidence/fingerprint_result.json) · [Raw results and scripts](evidence/). The fixed stock snapshot is `/private/tmp/csm_batch_v3_validation_snapshot/ohlcv`; it ends 2026-10-30 to preserve an apples-to-apples comparison and avoid the prior session's concurrently changing data source. Its 5,205 files were verified against the stored SHA-256 manifest. The original source is read only; source metadata before/after is tracked separately.

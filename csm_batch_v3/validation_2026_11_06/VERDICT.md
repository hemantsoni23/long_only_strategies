**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Final verdict — updated CSM Batch v3

**NOT VALIDATED.** The previously reported scheduled-open exit issue passes its specific regression test, but stock circuit handling and the new GOLDBEES sleeve still show opening-time lookahead. The source has unresolved corporate-action and survivorship limitations; historical return figures therefore cannot support promotion.

| Stage | Verdict | Key numbers | Report |
| --- | --- | --- | --- |
| 1. Universes | **PASS core; data anomaly** | 2015–2025 core Sharpe range 0.291, Calmar range 0.468; 501–1000 band is sensitive to the raw TIL jump; GOLDBEES has no 2011–2014 bars | [Stage 1](stage1_universe.md) |
| 2. Signal | **IC pass; quantile fail** | 2015–2025 L0 NW-t 2.41, L3 2.91; ordered quintile pairs 3/4; top-two-year signed-IC share 60.7% | [Stage 2](stage2_signal.md) |
| 3. Robustness & lookahead | **FAIL** | Scheduled-exit regression PASS; circuit-at-open FAIL; integrated stock-stop/ETF-open-sale FAIL | [Stage 3](stage3_robustness_lookahead.md) |
| 4. IS/OOS | **Not blind; not validated** | Reference Sharpe 2.32 → 1.83; Calmar 1.31 → 1.52; reverse MaxDD ratio 1.60× (limit 1.50×) | [Stage 4](stage4_is_oos.md) |
| 5. Exit quality | **Diagnostic** | 29/2200 END_OF_PERIOD records; volatility-stop continuation +1.16% on 831 observations (too early); rank exit +0.62% (neutral) | [Stage 5](stage5_exits.md) |

For 2015–2025, the configured ETF simulation reports CAGR 27.74%, Sharpe 1.83 and max drawdown -18.28%; the same stock-weight path with idle cash reports CAGR 22.31% and Sharpe 1.65. The ETF timing issue means the improvement is not established as executable.

The user-requested omission of exit-day stock P&L was preserved. The source strategy files and source data folders were only read. Stock tests used the same fixed snapshot through 2026-10-30 as the previous validation; GOLDBEES was copied and hashed separately. The supplied ETF file has no observations in 2011–2014, making early-period and full-sample ETF metrics unreliable. [Scope, configuration and reproducibility](validation.md).

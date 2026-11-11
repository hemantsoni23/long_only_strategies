# CSM Batch v2 — verdict

**OVERALL: NOT VALIDATED FOR LIVE USE**

| Test | Verdict | Key result | Detail |
| --- | --- | --- | --- |
| 1. Universe sweep | CAUTION | Core Sharpe range early/late 0.42/0.32; Calmar 0.27/0.39 | [Details](stage1_universe.md) |
| 2. Signal / accuracy | PASS basic IC / quantile caution | L0/L3 NW-t 2.41 / 2.91; monotone 3/4; top-30 above median 51.94% | [Details](stage2_signal.md) |
| 2. Signal time decay | RECENT WEAKNESS / EXPLORATORY | 2024–2025 IC 0.0010 vs 2021–2023 0.0565; post-hoc HAC t -2.19 | [Details](stage2_signal.md) |
| 3. Lookahead | FAIL | Synthetic scheduled-open ordering fails; 16 real stop exits occurred on dates with zero opening target | [Details](stage3_robustness_lookahead.md) |
| 3. Parameter sensitivity | PASS tested / cadence incomplete | ±20% Sharpe range 0.08; ±40% range 0.85; TIL sensitivity measured | [Details](stage3_robustness_lookahead.md) |
| 4. Bidirectional split | FAIL / NOT BLIND | Δ Sharpe -0.82; reverse DD ratio 1.63× | [Details](stage4_is_oos.md) |
| 5. Exit rules | DIAGNOSTIC | VOL_STOP mean 20/60d excess 1.22%; 2200 exits; same-date rotation proxy | [Details](stage5_exits.md) |

| Reference: 2015–2025 ranks 1–1000 | Measured |
| --- | --- |
| CAGR | 22.31% |
| Sharpe | 1.65 |
| Calmar | 1.31 |
| Max drawdown | -17.00% |
| First entry | 2015-01-01 |
| Convention | 0.3% per leg; 0% cash; exit-day return omitted at user request |

Historical periods have already been viewed; data-adjustment and execution-order issues remain. See the [full validation summary](validation.md) for context.

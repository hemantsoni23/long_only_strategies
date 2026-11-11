# Stages 1–5 — final verdict

**OVERALL: NOT VALIDATED**

| Stage | Test | Verdict | Key result |
| --- | --- | --- | --- |
| 1 | [Data integrity](01_DATA_INTEGRITY.md) | FAIL | 946 extreme price changes; delisting proxy 1.10% vs 2% flag |
| 2 | [Signal diagnostics](02_SIGNAL_DIAGNOSTICS.md) | FAIL | Early excluded 29.08% vs ≤15%; early/late monotonic 75% / 75% vs ≥80% |
| 3 | [Robustness](03_ROBUSTNESS_ABLATION.md) | FAIL / CONDITIONAL | Late ±20% position-count Sharpe swing 0.97 vs ≤0.40; extreme TIL price observation |
| 4 | [IS/OOS](04_IS_OOS_VALIDATION.md) | FAIL / NOT BLIND | Reverse-split drawdown ratio 1.59 vs ≤1.50 |
| 5 | [Exit quality](05_EXIT_QUALITY.md) | INCOMPLETE | Stop verdicts and same-date rotation tables computed; true paired replacement and clean prices unavailable |

| Reference figure | Measured | Interpretation |
| --- | --- | --- |
| Full-sample CAGR / Sharpe / max DD | 28.59% / 1.95 / -26.17% | Informational; raw data and user-specified accounting |
| Historical holdouts | Both periods previously viewed | Not independently blind |
| Source folder metadata changed | 0 files; 0 added; 0 removed | Read-only audit |
| Replay versus original runner | Max absolute equity difference 0 | PASS |

| Next required step | Requirement |
| --- | --- |
| Data | Verify corporate actions and delisted names in a separate read-only or derived dataset. |
| Validation | Re-run failed checks on clean data and establish an independent holdout. |

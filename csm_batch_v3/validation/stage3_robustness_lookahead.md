**Scope and conventions.** Default `csm_stock_backtest_v3.py` configuration: 15 equal-weight target slots, 12/6-month volatility-normalized momentum, ADX and 52-week-high gates enabled, two-month rebalance, 0.30% one-way trade cost, plus the configured stops and corporate-action mask. Equity uses the engine’s intentional omission of exit-day P&L. Returns are historical simulations, not investable or blind OOS estimates. All final figures use a fixed OHLCV snapshot through 2026-10-30, created outside the source data folder and only read during the tests. The source folder was only read by this workflow.

# Stage 3 — Robustness, ablation and lookahead

**Verdict: FAIL the no-lookahead requirement.** The following are deterministic tests of the actual unmodified engine. Same known-at-open state and opening price were held fixed; only later bar information changed. They show timing failures independent of the intentionally omitted exit-day P&L.

| Test | Same open / later-bar variation | Observed outcome | Verdict |
| --- | --- | --- | --- |
| Stop before scheduled open exit | Open 100; later low 90 vs 80 | REBAL_EXIT at 100 and next-day holding 1 vs HARD_STOP_HIT at 84.745 and next-day holding 0 | FAIL |
| Corporate-action mask at open | Open 100; later close 100 vs 500 | Entry fill 100.0 vs 90.0 (stale prior open) | FAIL |
| Full-day circuit check at open | Open 100; later high/low differ vs are equal | Held on scheduled day 1 vs 0; entry delayed a day | FAIL |

Stop ordering arises because the loop checks the complete day’s low before processing target exits at the open. The mask knows an event from its close, yet removes the event day’s open and the engine forward-fills it. The circuit condition uses completed-day high and low for opening decisions. These are proven synthetic counterexamples, not claims that every historical trade is affected. [Reproducible tests](evidence/test_execution_causality.py); see [engine](../csm_stock_backtest_v3.py) and [strategy](../csm_stock_strategy_v3.py).

## Actual-class parity and history truncation

| equity_max_abs_diff | position_cells_changed | passed |
| --- | --- | --- |
| 0.00000000 | 0 | True |

| cutoff | mask_mismatches | max_factor_difference | position_cells_changed | max_atr_difference | result |
| --- | --- | --- | --- | --- | --- |
| 2018-12-31 | 0 | 0.00000000 | 0 | 0.00000000 | PASS |
| 2020-03-31 | 0 | 0.00000000 | 0 | 0.00000000 | PASS |
| 2022-12-30 | 0 | 0.00000000 | 0 | 0.00000000 | PASS |
| 2024-12-31 | 0 | 0.00000000 | 0 | 0.00000000 | PASS |
| 2025-06-30 | 0 | 0.00000000 | 0 | 0.00000000 | PASS |

Prefix checks compare historical factor values, eligible masks, position targets and ATR to independently truncated runs. Passing them does not validate open execution timing. Actual-class parity compares the default v3 class and engine against the reconstructed baseline; both use identical flat-start selection.

## Parameter sensitivity: 2015–2025

| Configuration | CAGR % | Sharpe | Calmar | Max DD % | Turnover %/yr |
| --- | --- | --- | --- | --- | --- |
| baseline | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| lookback_7 | 28.015 | 1.683 | 1.050 | -26.679 | 782.339 |
| lookback_10 | 31.076 | 1.783 | 1.402 | -22.167 | 780.459 |
| lookback_12 | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| lookback_14 | 34.062 | 1.876 | 1.702 | -20.016 | 752.968 |
| lookback_17 | 30.944 | 1.775 | 1.436 | -21.541 | 751.376 |
| rebalance_1 | 30.002 | 1.660 | 1.048 | -28.618 | 947.789 |
| rebalance_2 | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| rebalance_3 | 38.310 | 2.086 | 1.916 | -19.994 | 640.770 |
| positions_9 | 33.046 | 1.708 | 1.305 | -25.331 | 784.388 |
| positions_12 | 34.016 | 1.874 | 1.418 | -23.988 | 775.380 |
| positions_15 | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| positions_18 | 28.985 | 1.758 | 1.394 | -20.797 | 758.675 |
| positions_21 | 28.539 | 1.774 | 1.443 | -19.781 | 757.451 |
| stop_0.09 | 35.092 | 2.125 | 1.727 | -20.317 | 865.012 |
| stop_0.12 | 32.739 | 1.931 | 1.486 | -22.034 | 801.627 |
| stop_0.15 | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| stop_0.18 | 30.162 | 1.724 | 1.214 | -24.844 | 753.887 |
| stop_0.21 | 29.557 | 1.684 | 1.167 | -25.334 | 748.714 |
| high52_0.51 | 32.752 | 1.838 | 1.545 | -21.200 | 770.967 |
| high52_0.68 | 32.673 | 1.835 | 1.541 | -21.200 | 770.369 |
| high52_0.85 | 32.139 | 1.840 | 1.523 | -21.108 | 767.624 |
| high52_0.95 | 27.683 | 1.677 | 1.125 | -24.618 | 755.798 |
| high52_1.00 | 24.333 | 1.484 | 0.945 | -25.756 | 654.265 |

## Parameter sensitivity: 2005–2014

| Configuration | CAGR % | Sharpe | Calmar | Max DD % | Turnover %/yr |
| --- | --- | --- | --- | --- | --- |
| baseline | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| lookback_7 | 44.135 | 2.370 | 1.667 | -26.472 | 707.198 |
| lookback_10 | 42.564 | 2.216 | 1.440 | -29.554 | 695.318 |
| lookback_12 | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| lookback_14 | 43.871 | 2.304 | 1.301 | -33.720 | 685.339 |
| lookback_17 | 37.950 | 2.173 | 1.416 | -26.803 | 654.457 |
| rebalance_1 | 39.655 | 2.132 | 1.541 | -25.738 | 857.787 |
| rebalance_2 | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| rebalance_3 | 41.737 | 2.078 | 0.954 | -43.729 | 626.501 |
| positions_9 | 38.402 | 1.936 | 1.121 | -34.252 | 720.889 |
| positions_12 | 44.446 | 2.209 | 1.477 | -30.100 | 699.873 |
| positions_15 | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| positions_18 | 42.682 | 2.311 | 1.720 | -24.809 | 679.179 |
| positions_21 | 43.644 | 2.443 | 1.777 | -24.557 | 667.053 |
| stop_0.09 | 46.803 | 2.509 | 1.896 | -24.691 | 800.084 |
| stop_0.12 | 45.586 | 2.386 | 1.592 | -28.633 | 736.865 |
| stop_0.15 | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| stop_0.18 | 44.691 | 2.251 | 1.275 | -35.049 | 680.264 |
| stop_0.21 | 44.684 | 2.225 | 1.234 | -36.225 | 666.555 |
| high52_0.51 | 40.269 | 2.089 | 1.115 | -36.124 | 713.771 |
| high52_0.68 | 42.035 | 2.179 | 1.208 | -34.790 | 701.006 |
| high52_0.85 | 45.237 | 2.303 | 1.509 | -29.981 | 699.803 |
| high52_0.95 | 49.137 | 2.247 | 1.165 | -42.169 | 704.281 |
| high52_1.00 | 35.678 | 1.977 | 1.019 | -35.021 | 633.214 |

## ADX threshold sensitivity

| window | cell | cagr_pct | sharpe | calmar | maxdd_pct |
| --- | --- | --- | --- | --- | --- |
| early | baseline | 45.237 | 2.303 | 1.509 | -29.981 |
| early | adx_12 | 41.539 | 2.207 | 1.167 | -35.593 |
| early | adx_16 | 41.307 | 2.190 | 1.316 | -31.388 |
| early | adx_20 | 45.237 | 2.303 | 1.509 | -29.981 |
| early | adx_24 | 45.249 | 2.354 | 1.629 | -27.785 |
| early | adx_28 | 50.939 | 2.362 | 1.608 | -31.673 |
| late | baseline | 32.139 | 1.840 | 1.523 | -21.108 |
| late | adx_12 | 30.930 | 1.808 | 1.591 | -19.446 |
| late | adx_16 | 31.596 | 1.837 | 1.406 | -22.475 |
| late | adx_20 | 32.139 | 1.840 | 1.523 | -21.108 |
| late | adx_24 | 31.698 | 1.786 | 1.563 | -20.285 |
| late | adx_28 | 33.251 | 1.841 | 1.624 | -20.475 |

ADX thresholds 16 and 24 are ±20% around the configured 20; 12 and 28 are ±40%.

## ±20% Sharpe sensitivity

### 2015–2025

| Parameter | Sharpe min | Sharpe max | Swing | ≤0.4 |
| --- | --- | --- | --- | --- |
| Lookback 10–14 months | 1.783 | 1.876 | 0.093 | PASS |
| Slots 12–18 | 1.758 | 1.874 | 0.116 | PASS |
| Hard stop 12–18% | 1.724 | 1.931 | 0.207 | PASS |
| High52 0.68–1.00 (bounded) | 1.484 | 1.840 | 0.356 | PASS |
| ADX 16–24 | 1.786 | 1.840 | 0.055 | PASS |

### 2005–2014

| Parameter | Sharpe min | Sharpe max | Swing | ≤0.4 |
| --- | --- | --- | --- | --- |
| Lookback 10–14 months | 2.216 | 2.304 | 0.089 | PASS |
| Slots 12–18 | 2.209 | 2.311 | 0.102 | PASS |
| Hard stop 12–18% | 2.251 | 2.386 | 0.135 | PASS |
| High52 0.68–1.00 (bounded) | 1.977 | 2.303 | 0.326 | PASS |
| ADX 16–24 | 2.190 | 2.354 | 0.164 | PASS |

The 2-month rebalance setting is discrete, so 1 and 3 months are ±50% stress tests rather than ±20% tests. High52 cannot exceed 1.00 when defined as close divided by its rolling high: the +20% point is unattainable, so 1.00 is a boundary sensitivity, not a symmetric +20% point. Lookback 10/14 are the nearest integer points to ±20%.

## Ablation scorecard: 2015–2025

| Ablation | Sharpe | Δ % | Calmar | Δ % | 12m σ | Δ % | Avg DD % | Δ % | Turnover % | Δ % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1.840 | 0.000 | 1.523 | 0.000 | 0.382 | 0.000 | 7.168 | 0.000 | 767.624 | 0.000 |
| ablate_rank_exit | 1.890 | 2.678 | 1.648 | 8.241 | 0.380 | -0.720 | 6.764 | -5.634 | 765.222 | -0.313 |
| ablate_vol_stop | 1.283 | -30.256 | 0.912 | -40.092 | 0.381 | -0.350 | 8.778 | 22.470 | 619.940 | -19.239 |
| ablate_adx | 1.942 | 5.513 | 1.962 | 28.861 | 0.303 | -20.765 | 6.269 | -12.532 | 697.980 | -9.073 |
| ablate_high52 | 1.838 | -0.136 | 1.545 | 1.461 | 0.385 | 0.695 | 6.879 | -4.028 | 770.967 | 0.435 |
| ablate_both_gates | 1.740 | -5.475 | 1.450 | -4.752 | 0.308 | -19.325 | 6.800 | -5.123 | 699.301 | -8.901 |
| ablate_positive_momentum | 1.798 | -2.301 | 1.478 | -2.941 | 0.374 | -2.069 | 7.340 | 2.405 | 770.067 | 0.318 |

## Ablation scorecard: 2005–2014

| Ablation | Sharpe | Δ % | Calmar | Δ % | 12m σ | Δ % | Avg DD % | Δ % | Turnover % | Δ % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 2.303 | 0.000 | 1.509 | 0.000 | 0.370 | 0.000 | 5.836 | 0.000 | 699.803 | 0.000 |
| ablate_rank_exit | 2.284 | -0.815 | 1.429 | -5.300 | 0.359 | -2.938 | 5.851 | 0.251 | 695.021 | -0.683 |
| ablate_vol_stop | 2.066 | -10.307 | 1.213 | -19.598 | 0.374 | 1.030 | 6.646 | 13.880 | 545.731 | -22.017 |
| ablate_adx | 2.346 | 1.870 | 1.119 | -25.820 | 0.393 | 6.384 | 6.246 | 7.012 | 657.545 | -6.039 |
| ablate_high52 | 2.056 | -10.741 | 1.098 | -27.255 | 0.369 | -0.239 | 5.881 | 0.775 | 711.901 | 1.729 |
| ablate_both_gates | 2.220 | -3.593 | 1.068 | -29.239 | 0.409 | 10.563 | 6.834 | 17.100 | 672.634 | -3.882 |
| ablate_positive_momentum | 2.221 | -3.577 | 1.443 | -4.393 | 0.368 | -0.592 | 5.869 | 0.568 | 715.675 | 2.268 |

Δ is relative to baseline. Lower 12-month rolling-return standard deviation, average drawdown depth and turnover are preferable. Playbook disqualification limits: Sharpe/Calmar regression >15%; stability/average DD worsening >20%; turnover increase >25%. These are diagnostic single-feature removals, not a recommendation to optimize against the test window.

## Transaction-cost stress (fully rerun share engine)

### 2015–2025

| cell | cagr_pct | sharpe | calmar | maxdd_pct | cost_drag_pct |
| --- | --- | --- | --- | --- | --- |
| baseline | 32.139 | 1.840 | 1.523 | -21.108 | 4.606 |
| cost_0.006 | 26.231 | 1.535 | 1.034 | -25.359 | 9.207 |
| cost_0.009 | 20.572 | 1.232 | 0.669 | -30.730 | 13.805 |

### 2005–2014

| cell | cagr_pct | sharpe | calmar | maxdd_pct | cost_drag_pct |
| --- | --- | --- | --- | --- | --- |
| baseline | 45.237 | 2.303 | 1.509 | -29.981 | 4.199 |
| cost_0.006 | 39.319 | 2.041 | 1.171 | -33.569 | 8.395 |
| cost_0.009 | 33.625 | 1.778 | 0.903 | -37.221 | 12.589 |

Costs are 0.3%, 0.6%, 0.9% one way on traded value, respectively. Stop-fill assumptions remain those of the source engine. Higher transaction costs do not cure the timing or adjustment issues. [Early sweep](evidence/early_sweep_cells.csv), [late sweep](evidence/late_sweep_cells.csv), [original early split sweep](evidence/playbook_early_sweep_cells.csv), [original late split sweep](evidence/playbook_late_sweep_cells.csv).

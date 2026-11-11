**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.

# Stage 3 — Robustness, ablation and lookahead

**Verdict: FAIL no-lookahead tests.** The earlier scheduled-open exit ordering is fixed in the ordinary non-circuit synthetic case, but two opening-time causal problems remain.

| Test | Held constant / changed later | Observed | Result |
| --- | --- | --- | --- |
| Scheduled open exit | Same open 100; later stock low 90 vs 80 | Both REBAL_EXIT at 100.00; next-day weight 0.50 in both | PASS |
| Stock circuit test at open | Same open 100; later high/low nonzero range vs equal | First-day stock weight 0.50 vs 0.00 | FAIL |
| Stock stop and ETF funding | Same opening purchase of B, weight 0.40; A's later low 90 vs 80 | ETF assumed opening sale 0.40 vs 0.00; ETF contribution 2.80% vs 6.00% | FAIL |

The last row runs the actual stock event loop and ETF sweep: the later stop changes end-of-day stock weight, which changes the ETF sale treated as occurring earlier at the open. This is independent of the intentionally omitted exit-day stock P&L. The circuit test uses the whole day’s high and low to decide an opening fill. These are deterministic counterexamples, not claims that every historical event is affected. [Test code](evidence/test_execution.py) · [Detailed results](evidence/execution_tests.json).

## Historical ETF sale / stock-stop overlap, 2015–2025

| Measure | Count |
| --- | --- |
| Days with modeled ETF sale | 552 |
| Days with a stock stop and modeled ETF sale | 80 |
| Days with a stock stop | 715 |
| ETF sale days flagged untradable | 1 |

This overlap identifies potentially affected days; it does not prove that each sale was caused by a later stop or measure the resulting bias. [Daily overlap data](evidence/late_etf_open_sales.csv).

## Actual-class parity and prefix tests

| Check | Measured |
| --- | --- |
| Baseline reconstructed equity maximum absolute difference | 1.78e-15 |
| Maximum target weight difference | 0 |
| Warmup stock exposure | 0 |
| Prefix tests passing | 5 / 5 |

| cutoff | monthly_rows | eligible_mask_mismatches | max_factor_difference | position_cells_changed | max_position_difference | max_atr_difference | max_regime_difference | result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2018-12-31 | 49 | 0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 | PASS |
| 2020-03-31 | 64 | 0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 | PASS |
| 2022-12-30 | 96 | 0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 | PASS |
| 2024-12-31 | 121 | 0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 | PASS |
| 2025-06-30 | 127 | 0 | 0.000000 | 0 | 0.000000 | 0.000000 | 0.000000 | PASS |

Prefix tests compare factor eligibility, factor values, target weights, ATR and regime values through each cutoff. They do not verify opening execution timing.

## Parameter sweeps: 2015–2025

| cell | cagr_pct | sharpe | calmar | maxdd_pct | turnover_pct | etf_exposure_pct |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| lookback_7 | 26.970 | 1.816 | 1.641 | -16.435 | 764.528 | 27.622 |
| lookback_10 | 29.857 | 1.941 | 1.791 | -16.674 | 735.941 | 28.390 |
| lookback_12 | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| lookback_14 | 26.774 | 1.765 | 1.552 | -17.254 | 702.942 | 29.063 |
| lookback_17 | 30.051 | 1.951 | 1.832 | -16.405 | 673.105 | 30.423 |
| rebalance_1 | 27.185 | 1.757 | 1.616 | -16.822 | 878.438 | 27.557 |
| rebalance_2 | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| rebalance_3 | 28.400 | 1.890 | 1.701 | -16.697 | 630.887 | 28.672 |
| positions_18 | 26.987 | 1.795 | 1.547 | -17.443 | 623.000 | 38.940 |
| positions_24 | 28.800 | 1.846 | 1.633 | -17.637 | 705.681 | 29.774 |
| positions_30 | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| positions_36 | 28.495 | 1.910 | 1.656 | -17.210 | 714.528 | 28.327 |
| positions_42 | 39.442 | 0.747 | 2.361 | -16.703 | 694.077 | 29.791 |
| stop_0.09 | 31.568 | 2.144 | 2.225 | -14.186 | 786.704 | 33.524 |
| stop_0.12 | 29.468 | 1.971 | 1.886 | -15.627 | 744.004 | 30.459 |
| stop_0.15 | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| stop_0.18 | 27.246 | 1.777 | 1.386 | -19.651 | 708.163 | 27.634 |
| stop_0.21 | 27.105 | 1.755 | 1.338 | -20.257 | 703.898 | 27.241 |
| regime_-0.06 | 27.497 | 1.810 | 1.546 | -17.791 | 714.698 | 30.059 |
| regime_-0.08 | 27.384 | 1.805 | 1.509 | -18.143 | 717.503 | 29.224 |
| regime_-0.10 | 27.742 | 1.826 | 1.518 | -18.278 | 718.745 | 28.580 |
| regime_-0.12 | 28.455 | 1.865 | 1.591 | -17.887 | 702.521 | 28.160 |
| regime_-0.14 | 28.671 | 1.876 | 1.603 | -17.887 | 700.286 | 27.860 |

## Parameter sweeps: 2005–2014

| cell | cagr_pct | sharpe | calmar | maxdd_pct | turnover_pct | etf_exposure_pct |
| --- | --- | --- | --- | --- | --- | --- |
| baseline | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| lookback_7 | 39.280 | 2.345 | 1.498 | -26.230 | 684.759 | 13.804 |
| lookback_10 | 42.039 | 2.507 | 1.450 | -29.000 | 644.435 | 13.716 |
| lookback_12 | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| lookback_14 | 39.122 | 2.353 | 1.464 | -26.718 | 604.175 | 13.621 |
| lookback_17 | 40.026 | 2.460 | 1.422 | -28.150 | 582.955 | 13.747 |
| rebalance_1 | 39.222 | 2.346 | 1.587 | -24.720 | 762.459 | 12.834 |
| rebalance_2 | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| rebalance_3 | 39.187 | 2.396 | 1.275 | -30.736 | 565.439 | 13.670 |
| positions_18 | 34.334 | 2.182 | 1.243 | -27.622 | 543.921 | 21.408 |
| positions_24 | 39.734 | 2.355 | 1.364 | -29.140 | 635.609 | 14.590 |
| positions_30 | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| positions_36 | 36.920 | 2.303 | 1.271 | -29.045 | 633.183 | 13.317 |
| positions_42 | 36.289 | 2.304 | 1.219 | -29.770 | 634.787 | 13.396 |
| stop_0.09 | 37.031 | 2.348 | 1.242 | -29.807 | 695.501 | 15.206 |
| stop_0.12 | 37.676 | 2.325 | 1.252 | -30.095 | 659.477 | 14.206 |
| stop_0.15 | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| stop_0.18 | 37.233 | 2.259 | 1.195 | -31.165 | 633.710 | 13.296 |
| stop_0.21 | 37.155 | 2.249 | 1.181 | -31.463 | 629.064 | 13.159 |
| regime_-0.06 | 37.634 | 2.288 | 1.477 | -25.480 | 636.608 | 14.055 |
| regime_-0.08 | 37.692 | 2.293 | 1.371 | -27.490 | 647.712 | 13.768 |
| regime_-0.10 | 38.199 | 2.321 | 1.310 | -29.170 | 642.885 | 13.461 |
| regime_-0.12 | 37.876 | 2.308 | 1.267 | -29.902 | 651.823 | 13.176 |
| regime_-0.14 | 37.992 | 2.322 | 1.222 | -31.102 | 633.853 | 12.959 |

## ±20% Sharpe sensitivity

### 2015–2025

| Parameter | Min Sharpe | Max Sharpe | Swing | ≤0.4 |
| --- | --- | --- | --- | --- |
| Lookback 10–14 | 1.765 | 1.941 | 0.177 | PASS |
| Positions 24–36 | 1.826 | 1.910 | 0.084 | PASS |
| Hard stop 12–18% | 1.777 | 1.971 | 0.194 | PASS |
| Bear cutoff −8% to −12% | 1.805 | 1.865 | 0.060 | PASS |

### 2005–2014

| Parameter | Min Sharpe | Max Sharpe | Swing | ≤0.4 |
| --- | --- | --- | --- | --- |
| Lookback 10–14 | 2.321 | 2.507 | 0.185 | PASS |
| Positions 24–36 | 2.303 | 2.355 | 0.052 | PASS |
| Hard stop 12–18% | 2.259 | 2.325 | 0.066 | PASS |
| Bear cutoff −8% to −12% | 2.293 | 2.321 | 0.028 | PASS |

Integer lookbacks 10 and 14 are approximations to ±20% around 12. The rebalance tests 1, 2 and 3 months are discrete ±50% stresses; the ±20% gate cannot be evaluated exactly.

## Ablation scorecards

Each row includes all five playbook measures and relative changes from baseline. Lower return instability, average drawdown depth and turnover are preferable. Limits: Sharpe/Calmar regression >15%; instability/average drawdown worsening >20%; turnover increase >25%.

### 2015–2025

| Cell | Sharpe | Δ % | Calmar | Δ % | 12m σ | Δ % | Avg DD % | Δ % | Turnover % | Δ % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 1.826 | 0.000 | 1.518 | 0.000 | 0.260 | 0.000 | 5.981 | 0.000 | 718.745 | 0.000 |
| ablate_rank_exit | 1.854 | 1.561 | 1.541 | 1.498 | 0.250 | -3.989 | 5.906 | -1.257 | 691.207 | -3.831 |
| ablate_vol_stop | 1.224 | -32.943 | 0.967 | -36.305 | 0.271 | 4.043 | 7.706 | 28.843 | 594.763 | -17.250 |
| ablate_bear_exposure | 1.932 | 5.799 | 1.632 | 7.555 | 0.274 | 5.358 | 6.130 | 2.487 | 709.778 | -1.248 |
| ablate_vol_target | 1.825 | -0.029 | 1.514 | -0.277 | 0.261 | 0.020 | 5.982 | 0.016 | 718.690 | -0.008 |
| ablate_corr_guard | 1.826 | 0.000 | 1.518 | 0.000 | 0.260 | 0.000 | 5.981 | 0.000 | 718.745 | 0.000 |
| ablate_positive_momentum | 1.817 | -0.494 | 1.510 | -0.542 | 0.260 | -0.177 | 5.989 | 0.128 | 718.748 | 0.000 |

### 2005–2014

| Cell | Sharpe | Δ % | Calmar | Δ % | 12m σ | Δ % | Avg DD % | Δ % | Turnover % | Δ % |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| baseline | 2.321 | 0.000 | 1.310 | 0.000 | 0.298 | 0.000 | 5.312 | 0.000 | 642.885 | 0.000 |
| ablate_rank_exit | 2.360 | 1.652 | 1.354 | 3.399 | 0.302 | 1.495 | 5.270 | -0.783 | 611.838 | -4.829 |
| ablate_vol_stop | 2.009 | -13.466 | 1.124 | -14.191 | 0.320 | 7.392 | 6.136 | 15.520 | 505.888 | -21.310 |
| ablate_bear_exposure | 2.268 | -2.310 | 1.159 | -11.478 | 0.311 | 4.321 | 5.680 | 6.937 | 682.955 | 6.233 |
| ablate_vol_target | 2.305 | -0.684 | 1.226 | -6.361 | 0.300 | 0.625 | 5.359 | 0.880 | 641.742 | -0.178 |
| ablate_corr_guard | 2.321 | -0.011 | 1.309 | -0.013 | 0.298 | -0.004 | 5.313 | 0.013 | 642.687 | -0.031 |
| ablate_positive_momentum | 2.295 | -1.151 | 1.284 | -1.916 | 0.294 | -1.239 | 5.317 | 0.099 | 639.756 | -0.487 |

## TIL raw-price sensitivity

| Observation | Value |
| --- | --- |
| TIL close, 2017-12-06 → 2017-12-07 | ₹2.85 → ₹146.50 (+5,040.35%) |
| 501–1000 portfolio return on 2017-12-07 | +253.63% |

| Cell | Data sensitivity | CAGR % | Sharpe | Calmar | MaxDD % |
| --- | --- | --- | --- | --- | --- |
| band_500_1000 | Raw snapshot | 50.420 | 0.693 | 3.159 | -15.963 |
| band_500_1000 | Exclude TIL in memory | 34.399 | 2.103 | 2.155 | -15.963 |
| positions_36 | Raw snapshot | 28.495 | 1.910 | 1.656 | -17.210 |
| positions_36 | Exclude TIL in memory | 28.495 | 1.910 | 1.656 | -17.210 |
| positions_42 | Raw snapshot | 39.442 | 0.747 | 2.361 | -16.703 |
| positions_42 | Exclude TIL in memory | 27.132 | 1.866 | 1.624 | -16.703 |

The exclusion is retrospective and is not an adjusted-data backtest: the ticker is removed only in memory, then universe ranks, benchmark, positions, stock engine and ETF sleeve are recomputed. Compare the raw and excluded 501–1000 and 42-position cells to identify sensitivity to this price series; do not treat the cleaned result as proof of investability.

[Early sweep](evidence/early_sweep_cells.csv) · [Late sweep](evidence/late_sweep_cells.csv) · [2001–2012 sweep](evidence/playbook_early_sweep_cells.csv) · [2013–latest sweep](evidence/playbook_late_sweep_cells.csv).

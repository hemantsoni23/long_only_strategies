> **Warning (2026-10-08):** absolute CAGR/Sharpe/drawdown figures in this document come from the Elendel engine's original booking (same-day weight × close-to-close return), which overstates results by ~17-26 CAGR points (see `csm_value/AUDIT.md`). Relative comparisons between variants may or may not survive; they have not been re-run.

# csm_resid_tilt — residual-momentum tilt for Zenith and Elendel

**What it is.** `CSMZenithResid` and `CSMElendelResid` subclass the live `CSMZenith` / `CSMElendel` (imported from `Old_live_strategies`, never copied or edited) and change one thing:

```
score = z(live score) + resid_weight · z(residual momentum 12-1)        resid_weight = 0.5 (fixed in advance, not tuned)
```

Universe, absolute-momentum gate, hysteresis, inverse-vol sizing, stops, Crash Guard, regimes and costs are all inherited. `resid_weight=0` is bit-identical to the live engine (tested).
Residual momentum = sum of the last 231 daily returns net of beta × the engine's equal-weight benchmark return (beta: 252d rolling, lagged a day), skipping the latest 21 days, read at month-end.
Missing values are neutral; a month with fewer than 60 residual values keeps the live score. Details: docstring of `resid_tilt_strategies.py`.

## Result (native implementation, unmodified live engines as baseline, 0.3% cost, 2003→2026-07)

| | Window | Live CAGR / Sharpe / MaxDD | Tilted | ΔCAGR / ΔSharpe | P(better) | 90% CI annual excess |
|---|---|---|---|---|---|---|
| **Zenith** | 2005+ | 30.8% / 1.87 / −14.0% | 37.4% / 2.23 / −14.5% | +6.6 pt / +0.36 | 1.00 | +2.8 to +7.1 % |
| | 2015+ | 25.8% / 1.48 / −11.9% | 34.8% / 1.99 / −13.0% | +9.0 pt / +0.50 | 1.00 | +4.0 to +10.0 % |
| | 2020+ | 34.1% / 1.87 / −11.9% | 41.2% / 2.25 / −13.0% | +7.1 pt / +0.38 | 0.99 | +1.4 to +9.0 % |
| **Elendel** | 2005+ | 33.6% / 1.81 / −19.9% | 37.9% / 2.02 / −20.7% | +4.3 pt / +0.21 | 0.97 | +0.4 to +5.9 % |
| | 2015+ | 32.2% / 1.66 / −18.5% | 36.0% / 1.84 / −19.5% | +3.9 pt / +0.18 | **0.86** | **−1.4** to +7.1 % |
| | 2020+ | 40.6% / 2.02 / −12.8% | 44.7% / 2.22 / −12.8% | +4.2 pt / +0.20 | 0.87 | −1.4 to +7.2 % |

Zenith was better in 21 of 24 calendar years; Elendel in 16 of 24. (Zenith's idle cash earns 6.5% as in the engine; Elendel's earns 0%, as in its runner. Deltas are unaffected.)
**Reading:** Zenith's evidence is strong and consistent; Elendel's is positive but weaker since 2015 (interval includes zero) — ship Zenith first, paper-trade Elendel longer.
Planning expectation (judgement): about half of the 2015+ gain — Zenith +4 to +5 pt CAGR / +0.2 to +0.25 Sharpe; Elendel +2 pt / +0.1; max drawdown about 1 pt deeper in both.

## Checks (`python3 test_resid_tilt.py` — all pass)
1. weight 0 reproduces the live factors exactly (both engines); 5. tilted score is defined exactly where the live score is (universe untouched);
2. native residual momentum vs the factor-research version: month-end rank correlation 0.998 (min 0.979) — not bit-identical because the engine calendar keeps holiday placeholder rows the research panels drop;
3. **no look-ahead**: truncating the data at 2012-06, 2019-12 and 2024-03 month-ends leaves that month's residual momentum unchanged (max diff 0.0);
4. native tilted engines vs the research variants: daily correlation 0.993, CAGR within 0.6 pt.

## Use
```
python3 run_resid_tilt_backtest.py zenith            # full live-style report (logs, plots, IC) into ./output — nothing is written to Old_live_strategies
python3 run_resid_tilt_backtest.py elendel --weight 0.5
python3 compare_to_live.py                           # tilted vs unmodified live engines, windows, bootstrap, years -> output/compare_to_live.txt
```
Live integration: wherever the live job does `from csm_zenith_strategy import CSMZenith`, import `CSMZenithResid` from here instead and construct it with the same arguments (+ optional `resid_weight`). `calculate_factors()`, `get_positions()`, `get_exit_signals()` and the backtests work unchanged; the extra attributes `base_factors` (live score) and `resid_mom` are kept for audit.
The per-leg IC printout of the runner still lists only A1/Q5 (the residual term is not a registered leg).

## Overlap with your live residual-momentum strategy
This term is the 12-1 CAPM-residual version tested in `factor_research`, not the 9-month composite inside `residual_momentum_strategy.py`; they are related. Before running Zenith-Resid alongside the residual strategy, compare daily-return correlations of the live books (not done here).

## Kill / review rules
Revert (set `resid_weight=0`) if, over any rolling 12 months, the tilted engine trails the unmodified one by more than 5 CAGR points, or its max drawdown is more than 3 points worse over the same period.

## Caveats
Survivorship (only currently listed names); weight 0.5 pre-set but ~39 engine/universe/variant comparisons were run in total; the bootstrap describes this one history. Paper-trade for at least a full month-end cycle before capital.

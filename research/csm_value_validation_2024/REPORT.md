# CSM Value robustness and CSM Absolute review — through 2024

## Scope and decision

At the user's direction, all performance work stays at or before 31 December 2024. The value-growth-pullback ranking was selected after examining part of this same history. The local older fundamentals sources begin around 2018–2019 and are derived from the same NSE disclosures; the alternate Upstox OHLCV copy is not an independent source. A check of RELIANCE, HDFCBANK, TCS, INFY and SBIN found all 1,488 overlapping 2019–2024 closes identical in each pair. There is therefore **no genuinely untouched, independent performance holdout** in the inputs used here. The findings below are robustness and engineering checks on previously used data, not independent proof of an edge.

The candidate remains experimental. The normal ranking and the user's intentional zero exit-day weight remain unchanged. All variations below use the existing fundamental/OHLCV intersection, no liquidity-rank cutoff, the 10-position maximum, the 5% weight cap, and CSM Value's current signal and next-session execution flow.

## Frozen strategy and stress scenarios

The tested candidate was frozen as 55% earnings-yield rank + 20% filing-aware profit-growth rank + 25% inverse Elendel A3/Q5 rank. `frozen_manifest.json` records code fingerprints and assumptions. Reference models use 0.30% cost per unit of weight change and 6.5% annual cash interest. Cost stress uses 0.60%; zero-cash stress sets the cash yield to zero. Tighter stops use 8% below entry and 12% below peak under CSM Value's existing close-confirmed, next-open flow: they do **not** reproduce CSM Absolute's intraday ATR or limit-order engine. The Absolute signal gate uses its 9/4-month, one-month-lagged return/volatility average above 0.6, plus positive long momentum; it does not import a top-1,000 liquidity filter.

2019-06-03 through 2024-12-31. Max DD is negative. Turnover is annualized total absolute weight changes, including buys and sells. Mean holding includes positions administratively closed in the trade report at the end of the sample.

| Scenario | Original value CAGR / DD | Frozen candidate CAGR / DD | Candidate avg holding | Candidate turnover |
|---|---:|---:|---:|---:|
| Reference | 24.48% / -13.86% | 27.54% / -13.46% | 67.0 days | 496% |
| Double transaction cost | 22.83% / -14.38% | 25.67% / -14.01% | 67.0 days | 496% |
| Zero cash yield | 20.12% / -14.49% | 23.09% / -14.08% | 67.0 days | 496% |
| 8% / 12% close-confirmed stops | 25.94% / -10.88% | 23.38% / -12.91% | 38.3 days | 800% |
| CSM Absolute-style momentum/volatility gate | 23.87% / -12.62% | 25.42% / -13.99% | 59.6 days | 557% |

The reference candidate's 2022–2024 CAGR/DD was 29.07% / -10.39%; with the tighter close-confirmed stops it was 23.90% / -11.18%. The Absolute-style gate also made the candidate's full-period and 2022–2024 CAGR and drawdown worse. These are explorations, not precommitted out-of-sample selections. Do not adopt tighter stops or the gate on the strength of these results.

## Return-stream resampling and prefix checks

As a sensitivity check, 2,000 paired circular block samples of 126 daily sessions were drawn from the **fixed realized 2019–2024 daily return streams**, using the same blocks for both strategies. The 2.5th to 97.5th percentiles of the candidate-minus-baseline CAGR spread were approximately -3.54 to +9.53 percentage points; the corresponding maximum-drawdown spread was -3.84 to +3.34 percentage points, where a positive difference means a smaller drawdown. These are descriptive resampling ranges, not probabilities of future success, independently validated confidence intervals, or an adjustment for all prior strategy selection. Resampling realized return streams does not recalculate positions on the rearranged market history. See `robustness.json` for full methodology and results.

For both rankings, complete runs through 2024 were compared against runs truncated at 30 December 2022 and 29 December 2023. Earlier factor values agreed to floating-point tolerance, and positions and daily returns agreed to within 1e-10. This supports the tested prefix-causality implementation; it cannot validate filing versions, unobserved delistings, vendor price adjustments or all possible leaks. The frozen reference daily returns also matched the normal runner's saved output exactly for all 1,385 reporting sessions.

## CSM Absolute — code review

The production runner uses 9- and 4-month lagged momentum divided by annualized monthly-return volatility, with a 0.6 gate. It also uses 25 positions, a top-1,000 traded-value universe, 12% maximum per-name weight, quarterly rebalancing, 8%/12% hard stops, 2× ATR trailing stop, partial take profit, and limit-order simulation. It differs substantially from CSM Value; its volatility-normalized score alone cannot explain a shorter holding period or performance.

1. **Live guard error:** `IndividualMomentumStrategy.volatility_crash_guard` is declared without `self` or `@staticmethod`, but `get_exit_signals` invokes it as an instance method. A direct reproduction raises `AttributeError: 'IndividualMomentumStrategy' object has no attribute 'dropna'`. The declared `benchmark_close` parameter at the call site is also documented as a scalar, whereas the guard requires a time series. This identifies a failure in the supplied method, not proof about how an external live process calls it.
2. **Live/backtest guard mismatch:** `get_exit_signals` calls the volatility guard, while the backtest's daily crash guard uses an SMA-based rule. Their outcomes and required inputs can differ.
3. **Limit-order fill outside the daily range:** With a pending sell stop-limit at ₹100 and an OHLC bar open ₹80, high ₹90, low ₹75, close ₹85, the limit-order manager returns a fill at ₹100. This is above the observed high. The recorded entry/exit events, trade log and execution simulation need separate investigation; the effect on the reported portfolio return also depends on the user's exit-day weighting convention.
4. **Weekend month-end lag:** For a monthly label of Saturday 31 August 2024, the last trading session was Friday 30 August. The engine's month-end reindex plus one-session shift first activates the new position on Tuesday 3 September, not Monday 2 September. That differs from the next-session timing used in the current CSM Value runner.

The supplied original engine patches individual trade fill returns but multiplies them by same-day executed weights; a fully exited stock has zero weight. This is consistent with the user-requested booking convention, but it differs from an execution ledger. The separate Absolute replay and an alternative return-accounting sensitivity are recorded in `absolute_audit.json`. The alternative is a diagnostic, not a proposed change to CSM Value and not a validated cash/share ledger. Its original universe, position limits and exit rules differ from CSM Value, so its returns are not an apples-to-apples comparison.

For the separate original CSM Absolute configuration, a fresh 2019–2024 load with a 2020–2024 reporting window produced the following. Both rows used identical executed weights, decisions and modeled costs; the only changed calculation was whether a fully exited holding's prior weight was applied to its exit-day fill return. The reported trade log had 2,305 entries in the window, with a mean holding period of 11.15 calendar days and median of 9 days.

| Return calculation | 2020–2024 CAGR | Max DD |
|---|---:|---:|
| Original zero exit-day weight | 56.46% | -6.09% |
| Prior weight applied to full-exit fill return, sensitivity only | 5.03% | -23.13% |

The large difference shows that reported performance is highly sensitive to the booking convention for this short-hold strategy. The sensitivity is not a reliable estimate of realized P&L: it is a partial weight-based calculation, and the simulated stop-limit fill and other execution assumptions still need correction. The requested zero exit-day convention remains unchanged in CSM Value.

## Reproduction

- `validate.py` reruns the frozen CSM Value reference and stress scenarios and writes `robustness.json`, `paired_daily_returns.csv` and `frozen_manifest.json`.
- `prefix_check.py` checks full-run versus truncated-run signals, positions and daily returns and writes `prefix_checks.json`.
- `check_absolute.py` performs read-only synthetic error reproductions and a separate 2019–2024 CSM Absolute replay; no live file is edited.
- `test_validation.py` checks paired-bootstrap equality and the Absolute gate's prefix causality.

The remaining route to independent performance validation is an independently sourced, verified, previously unseen dataset. The user chose to stay within 2024 for this work. Corporate-action, original/revision filing history, security identity, delistings, stale quotes, market impact, stop-limit fills and reporting-frequency issues remain relevant.

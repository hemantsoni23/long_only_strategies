# Holding-period and exposure study

**Historical accounting notice:** The experimental results in this report
predate the experimental runner's drift and transaction-cost correction.
They are preserved as prior research and are not the current backtest. The
corrected runner changes execution weights and the timing of non-exit returns,
so the differences cannot be attributed to transaction costs alone. The
standard value runner has not received that correction.

## Goal and scope

The requested research targets were roughly 3–6 months' average holding time
and 80–100% average equity exposure in favorable conditions. These are
**targets, not guarantees**. All results use the already-examined data through
31 December 2024. The parameters were selected after inspecting these results,
so the study is not an independent performance test.

Both versions retain filing-date-aware fundamentals, no top-1,000
price-volume universe filter, next-open execution and the user-requested zero
exit-day weight. The model assumes 6.5% annual cash return and 0.30% one-way
transaction costs. It does not establish realistic capacity for illiquid
stocks. Returns are weight-based, not a cash-and-shares execution ledger.

The sample is 3 June 2019–31 December 2024. Holding statistics are calendar
days for trades that actually closed in the period; positions still open at
the sample end are excluded rather than treated as completed trades. Favorable
exposure is averaged on sessions labelled `BULL` by the engine: the benchmark
is not in its bear, high-volatility or panic state. This is an average, not a
minimum exposure on every such day. Max drawdown is signed.
In the full sample, exposure was at least 80% on 69.4% of favorable sessions
for value and 69.1% for the experimental version.

## Chosen settings and comparison

| Version | Configuration | CAGR | Max DD | Mean hold | Median hold | Mean equity exposure | Favorable-session exposure |
|---|---|---:|---:|---:|---:|---:|---:|
| Value | Previous | 24.48% | -13.86% | 75.3 days | 62 days | 42.5% | 48.2% |
| Value | Longer-term | 36.51% | -24.75% | 92.6 days | 84 days | 73.5% | 83.8% |
| Experimental | Previous | 33.20% | -14.08% | 43.5 days | 37 days | 52.3% | 61.9% |
| Experimental | Longer-term | 40.30% | -18.03% | 97.0 days | 96 days | 70.7% | 83.7% |

The higher historical CAGR comes with a **larger historical drawdown**,
particularly for value. The 3–6-month goal was reached on average over the
full sample, but not uniformly: the value configuration averaged 83.5 days in
the 2019–2021 subperiod. Exposure can fall below the target when there are too
few eligible stocks or when risk controls, stops, crash guard or missing
opening quotes prevent full allocation.

The comparison's 2024-only results, also previously examined, are:

| Version | CAGR | Max DD | Mean hold | Favorable-session exposure |
|---|---:|---:|---:|---:|
| Value | 27.32% | -13.75% | 120.1 days | 84.3% |
| Experimental | 51.83% | -13.72% | 110.0 days | 86.5% |

The normal runners report 36.50% and 40.29% full-period CAGR, respectively,
approximately 0.01 percentage points below the table because the study includes
the first reporting day's return whereas the normal report rebases at that
day's close. Their reported drawdowns match the table.

Value's full-period CAGR at doubled one-way costs (0.60%) was 33.54%; the
experimental version's was 37.37%. This sensitivity holds decisions fixed;
it does not simulate market impact. Resampling or repeatedly tuning this
same history would not turn it into an untouched holdout.

## Rules

Both default to at most 20 positions and 5% per stock, so the target portfolio
can allocate up to 100% before risk overlays. The risk budget is 0.75% of
portfolio value per stock at the initial 15% stop, consistent with a 5% cap.
The existing inverse-volatility weighting and correlation/crash guards remain.

Both use a 100% rank buffer, so a previously selected stock may remain in the
monthly selection through rank 40, subject to the existing swap-gap rule. Both
use a 20% close-confirmed trailing stop and a 15% entry stop. The value version
uses a two-month rebalance-exit buffer and a 20% volatility target; the
experimental version uses a three-month buffer and a 22% volatility target.
Their existing bear exposure multipliers are 0.8 and 0.5 respectively.

The buffer counts **distinct consecutive monthly signal drops**. A two-month
buffer defers the first two drops and exits on the third; a three-month buffer
defers the first three and exits on the fourth. A return to the target resets
the count. If the open is missing when an exit becomes due, the engine retains
the pending exit and retries at the next valid open. Stops and crash-guard
exits continue during the buffer. The buffer also defers rebalance exits when
the reason for dropping out is a failed fundamental condition; it is not a
guarantee of continued fundamental strength.

The engine now prevents deadband adjustments from pushing tradeable weights
above 100% gross exposure. It preserves a holding's previous weight when its
open is missing; any needed reduction is applied to adjustable holdings.

An alternative inverse-volatility allocator that fills available weight
capacity was researched but is **not enabled by default**: it increased
exposure, but in the tested 20-position case it also increased drawdown and
did not improve full-period CAGR versus the original allocation. The feature
remains available to the research script as `fill_weight_caps`.

## Reproduction and previous settings

Run `python3 research/csm_value_studies/long_horizon_exposure_study.py` to
repeat all cases, or pass individual case names. The selected calibration
cases are `long20_cal_t20_v20` for value and `long20_cal_t20_b3_v22` for the
experimental ranking. Results include the pre-2022 and 2022–2024 slices,
2024-only values, exposure, completed-trade statistics and doubled-cost
sensitivity. `long_horizon_exposure_calibration_results.json` records those
calibrations; other JSON files record the earlier exploratory variations.
The old research baseline is explicitly frozen in the research loader so it
does not silently change when strategy defaults change.

The selected settings were rerun on a dataset truncated at 29 December 2023
and compared with the corresponding prefix of the full 2024 run. Factors,
target positions, executed weights and daily returns agreed within 1e-10 for
both rankings. See `long_horizon_prefix_check.py` and
`long_horizon_prefix_checks.json`. This check cannot validate historical
filing versions, delistings, market impact or the booking convention.

Both normal runners accept `--risk-profile legacy_value` for the former
10-position value-risk configuration, and `--risk-profile
exploratory_10_12_bear50` for the previous 10-position experimental-risk
configuration. Ranking can still be selected independently.

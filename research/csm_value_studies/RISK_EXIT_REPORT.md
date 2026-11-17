# CSM Value: position sizing, stops, market risk and exits

This report records the earlier 10-position study. Strategy defaults were
subsequently changed for the holding-period and exposure objectives; see
[the later study](LONG_HORIZON_REPORT.md). The historical baselines below
remain frozen for comparison. Experimental figures also predate the later
drift, transaction-cost and return-timing correction and are not current
performance estimates.

## Scope

These are historical, exploratory comparisons through 31 December 2024. This
history has already been used repeatedly for strategy research; neither 2024
nor 2022–2024 is an untouched holdout. The three combined cases were added
after seeing the individual cases. No winner should be interpreted as a
validated prediction or an automatic live-trading recommendation. Testing
multiple choices on a reused sample increases selection bias; see
[Bailey et al. on backtest overfitting](https://ssrn.com/abstract=2308659).

Both rankings use the existing point-in-time fundamentals, Upstox OHLCV,
as-traded NSE valuation prices, 10-position limit, no price-volume rank
cutoff, and next-open engine. The intentional zero exit-day weight booking is
unchanged. Cash is assumed to earn 6.5% annually; the ordinary one-way cost is
0.30%. Existing data-quality, delisting, capacity and execution limitations
remain. Max drawdown is signed; a value closer to zero is smaller.

Cases change one group of parameters against each ranking's baseline:

* 8% and 10% weights raise *both* the weight cap and the stop-based risk-budget
  parameter, otherwise the latter remains an effective cap.
* Trailing cases change only the close-confirmed trailing percentage; the
  15% entry stop remains.
* Short cooldown sets loss-scaled base/floor/cap to 5/2/15 calendar days. The
  separate 10-session portfolio-wide crash-guard cooldown is unchanged, but
  the same base parameter also shortens the stock-level cooldown after a
  crash-guard exit from 20 to 5 calendar days.
* Bear cases change the 0.8 benchmark-regime exposure multiplier to 1.0 or
  0.5; the crash guard and other overlays remain active.
* No rebalance delay removes the one-signal-month exit buffer.
* The SMA50 gate requires a stock's actual month-end-session close to exceed
  its 50-session average for both selection and continued selection. It is
  applied after the factor ranks, so an ineligible top-10 stock is not replaced
  by reranking every stock. Exit handling still uses the normal rebalance
  buffer; it is not a separate daily SMA stop and gets logged as REBALANCE.

## Results: one change at a time

Full: 3 June 2019–31 December 2024. 2024: 1 January–31 December 2024. Columns
are annualized CAGR / maximum drawdown; the 2024 column is an approximately
one-year CAGR, not a separate independent test. Mean exposure is the average
sum of stock weights over the full window.

| Ranking | Case | Full CAGR / DD | Mean exposure | 2024 CAGR / DD |
|---|---|---:|---:|---:|
| Value | Baseline | 24.48% / -13.86% | 42.5% | 19.21% / -10.18% |
| Value | 8% cap | 31.23% / -19.13% | 55.1% | 22.93% / -10.43% |
| Value | 10% cap | 33.57% / -18.61% | 56.8% | 26.17% / -11.37% |
| Value | 12% trail | 26.11% / -11.25% | 41.2% | 23.87% / -7.37% |
| Value | 16% trail | 24.18% / -14.01% | 42.5% | 21.28% / -10.48% |
| Value | Short cooldown | 24.21% / -16.59% | 43.2% | 23.90% / -10.59% |
| Value | Bear exposure 1.0 | 25.15% / -15.66% | 44.3% | 19.21% / -10.18% |
| Value | Bear exposure 0.5 | 24.56% / -11.51% | 40.7% | 19.21% / -10.18% |
| Value | No rebalance delay | 23.50% / -13.92% | 41.1% | 17.18% / -8.52% |
| Value | Monthly SMA50 gate | 18.13% / -9.90% | 30.6% | 18.78% / -9.90% |
| Blend | Baseline | 27.54% / -13.46% | 42.6% | 31.98% / -8.79% |
| Blend | 8% cap | 35.30% / -18.79% | 54.0% | 28.61% / -12.79% |
| Blend | 10% cap | 37.30% / -18.34% | 54.4% | 31.59% / -11.16% |
| Blend | 12% trail | 25.13% / -11.82% | 42.0% | 26.65% / -7.65% |
| Blend | 16% trail | 27.00% / -12.92% | 42.9% | 34.92% / -7.78% |
| Blend | Short cooldown | 25.68% / -16.18% | 43.4% | 27.81% / -8.79% |
| Blend | Bear exposure 1.0 | 28.41% / -17.23% | 44.8% | 31.98% / -8.79% |
| Blend | Bear exposure 0.5 | 26.73% / -10.65% | 40.7% | 31.98% / -8.79% |
| Blend | No rebalance delay | 25.64% / -12.53% | 41.9% | 19.33% / -6.94% |
| Blend | Monthly SMA50 gate | 19.32% / -8.17% | 26.9% | 18.71% / -7.47% |

The blend is the experimental 55% value / 20% profit-growth / 25% inverse
price-strength ranking. The ordinary runner still defaults to pure value.

## Post-hoc combinations

These combinations were tested only after examining the individual cases.
They retain the original entry stop and cooldown and use a 0.5 bear multiplier.

| Ranking | Weight cap / trail | Full CAGR / DD | 2022–2024 CAGR / DD | 2024 CAGR / DD | Full CAGR at double cost |
|---|---|---:|---:|---:|---:|
| Value | 8% / 12% | 31.48% / -14.16% | 37.50% / -9.93% | 22.38% / -9.09% | 27.74% |
| Value | 10% / 12% | 34.40% / -13.84% | 41.56% / -10.93% | 26.62% / -9.67% | 30.17% |
| Value | 10% / 16% | 32.75% / -15.61% | 36.92% / -11.89% | 30.24% / -10.21% | 29.39% |
| Blend | 8% / 12% | 31.73% / -13.52% | 32.20% / -12.92% | 25.50% / -12.24% | 27.57% |
| Blend | 10% / 12% | 33.20% / -14.08% | 32.98% / -14.08% | 28.56% / -11.39% | 28.59% |
| Blend | 10% / 16% | 33.14% / -15.78% | 33.52% / -15.78% | 33.87% / -9.97% | 29.29% |

The full-period value baseline at double cost is 22.83% CAGR. The value
10%/12% combination trades much more: annualized absolute weight turnover is
1,066% versus 445% for baseline, and median holding periods for the
entry-date cohort are 36 versus 62 calendar days. Doubling cost to 0.60%
reduces its CAGR from 34.40% to 30.17%. Cost stress holds the decisions fixed;
it does not model market impact or establish realistic fills.

The user's zero-exit-day-weight rule remains in effect. Faster exits alter how
often that convention applies, so gains from a tighter stop should not be
treated as actual cash-and-shares P&L. See the prior
[Absolute accounting review](../csm_value_validation_2024/REPORT.md) for a
demonstration of how sensitive a different short-hold strategy was to return
booking. This observation does not quantify the sensitivity of these runs.

## Reproduce

`python3 research/csm_value_studies/risk_exit_experiments.py` runs all listed
cases. Pass one or more case names to run a subset into a separate output file.
The full individual results, including 2019–2021, 2022–2024, transaction-cost
stress and exit counts, are in `risk_exit_results.json`; the post-hoc combined
case results are in `risk_exit_selected_results.json`.

An opt-in runner profile, `--risk-profile exploratory_10_12_bear50`, reproduces
the 10% / 12% / 0.5 combination and writes separately named output files. The
current default is documented in the later study. This profile was chosen after inspection and
has no clean holdout. A normal runner check reported 34.39% CAGR and -13.84%
drawdown for plain value. Its CAGR differs from the table by about 0.01
percentage points because the normal report rebases at the first reporting
close, while the study compounds the first reporting day's return as well.

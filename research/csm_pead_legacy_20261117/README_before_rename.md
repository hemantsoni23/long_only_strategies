# CSM PEAD — earnings-event research

This is a research strategy, not a validated live strategy. It combines an
earnings surprise with the subsequent price reaction. Reports and figures in
the old `output/` and `output_run.log` use an obsolete data cache, a different
universe, close fills and data beyond 2024. They do not describe the corrected
implementation and must not be used as evidence for it. New runs write to
`output_audited/` by default, preserving the old results.
The old `diag_*.py` research scripts still depend on historical caches or
older assumptions and have not been updated or validated for this version.

## Data and signal

* Uses matching OHLCV and `fundamentals/` JSON files, including `sme/`. SME
  half-year results are not treated as separate quarters. There is no
  top-1,000 liquidity-rank filter; the price and flat-price-day filters remain.
* The default data and simulation boundary is **2024-12-31**. Later data is
  excluded pending revalidation.
* Quarterly events are constructed from each filing date using only prior or
  same-day filings; a filing's signal is never used on its filing date. The
  earliest PEAD signal is the close of the second trading session after the
  first session on or after filing. A buy is possible at the following open.
* Earnings surprise is seasonal EPS change divided by the standard deviation
  of at least four prior seasonal EPS changes. To reduce split/bonus errors,
  EPS comparisons are omitted when filed share counts differ by more than 3%.
  This conservative check can exclude genuine diluted issuers and does not
  prove EPS was never retrospectively restated. The current JSON is a snapshot,
  not a complete revision history; historical point-in-time values cannot be
  fully independently verified without original filing versions.
* The present-day list of matching stock files may omit delisted or renamed
  companies, so the universe is not guaranteed free of survivorship bias.
* An announcement return uses the stock's observed close before the event to
  its signal-day close, less the return of an equal-weight index built from the
  loaded fundamentals-matched stock files. The 70th percentile for each
  measure is computed from the trailing 120 calendar days of eligible events,
  including the current signal date, with at least 150 events. A candidate
  must meet both thresholds. The score used when slots are scarce combines
  standardized distances above the two thresholds.

## Portfolio and timing

* Up to 20 stocks, each initially sized at 1/20 of available portfolio equity;
  individual weights drift as prices change. New entries can be attempted for
  up to five trading sessions after their signal when slots are available.
* A holding is reviewed after 60 trading sessions. A close at or below 85% of
  its entry price also schedules a stop. Both sell at a **later valid open**;
  a missing open leaves the order pending. Stops apply 0.3% modeled slippage.
  There is no same-day fallback to a closing price that was unknown at the open.
* The strategy uses a cash-and-shares ledger, charges 0.3% of each modeled buy
  or sell, and assumes idle cash earns 6.5% per year. Sales include their actual
  overnight price movement in the book. This differs from the user-requested
  zero exit-day return convention in CSM Value; PEAD does not silently adopt
  that CSM Value-specific reporting convention. Missing closing prices are
  forward-filled for marking existing holdings, not for executing trades.
* The model does not establish that opening orders could fill given exchange
  limits, spreads or market depth. There is no position-capacity limit.

## Run and test

```
python3 csm_pead/test_pead.py
python3 csm_pead/run_csm_pead_backtest.py
```

The default report is 2020-09-01 to 2024-12-31, after indicator warmup. These
years have already been inspected during earlier research. No period is
claimed to be an untouched out-of-sample test, and no same-universe technical
baseline has yet been established for a clean contribution comparison.
The report starts at the selected first day's close; trades CSV covers modeled
transactions after that close. Trade amounts refer to the original continuous
cash book, while the displayed reporting portfolio is rebased to ₹100,000.
The detailed report's trade win rate and trade PnL compare entry and exit
prices before trading fees; portfolio returns include the modeled fees. The
completed-trade statistics include only positions entered within the report
window, so positions carried into that window are excluded from the count.

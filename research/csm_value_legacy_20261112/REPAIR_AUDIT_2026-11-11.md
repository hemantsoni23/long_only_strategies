> **Later user direction:** CSM Value now deliberately uses Elendel's zero
> exit-day-weight accounting and has no price-volume rank universe cutoff.
> Earlier sections below describe the superseded implementation.

> **Update, 11 November 2026:** The project now includes locally downloaded NSE
> historical month-end closes and uses them automatically. See
> [PRICE_DATA.md](PRICE_DATA.md). References below to missing as-traded prices
> and the mandatory environment variable describe the earlier state.

# CSM Value repair audit — 11 November 2026

This audit supersedes the earlier clean-lookahead and performance claims in
`README.md`, `AUDIT.md`, and existing output files. Those documents and outputs
are historical; they have not been regenerated for the repaired implementation.
No new CAGR, drawdown or investment-performance claim is made here.

## Problems found and changes

- A filing on the signal date was included. Filings are now available strictly
  after their local filing calendar date, and timestamps with seconds are parsed
  and retained. Shareholding is not currently used by this strategy.
- Trailing earnings and basis selection used complete-period data before mapping
  results to dates. A quarter filed later could enter an earlier result, and a
  later consolidated filing could displace an earlier standalone filing. The
  loader now updates a per-company filing-event history and computes each value
  only from already-filed quarterly observations. Current-period age is not
  reset by a late older filing. It reads the main and SME directories, but
  excludes half-year statements from this quarterly strategy rather than
  treating them as quarters. It does not reconstruct missing XBRL revisions.
- The old default fundamentals path pointed outside this workspace, and its date
  parser skipped the newer timestamps. The loader now uses the supplied
  `fundamentals_data` folder, including `sme/`, by default. The
  `CSM_FUNDAMENTALS_DIR` override remains available.
- A calendar month-end may fall after the last trading session. Fundamentals
  are now checked as of the actual signal session, and a weekend-labelled
  signal is mapped back to that session before scheduling its next-open order.
- Entirely empty factor months were dropped, so old targets could persist
  indefinitely. Empty months now emit zero targets; the configured rebalance
  exit buffer can still defer an actual sale.
- Liquidity ranking previously included the full OHLCV collection, even where
  fundamentals were unavailable. The runner limits files to matching
  fundamentals symbols, and the ranking only includes stocks with eligible
  as-of fundamentals and valuation prices for that month. The minimum-price
  filter also uses as-traded valuation prices rather than back-adjusted prices.
- Future share-count changes were used to infer split adjustments, and a later
  filing could alter an earlier valuation. That inference can also confuse an
  issuance with a split. It is disabled. Market cap now uses the filed share
  count and a separately supplied, verified as-traded (unadjusted) close. The
  run fails closed if such prices are not supplied. Apparent post-period split
  cliffs cause the stale share count to be excluded until a later period;
  this heuristic is not a substitute for a verified corporate-action history.
- The default stop mode was labelled `close_next_open`, but the runner checked
  the intraday low and could fill on the same day. It now checks the close and
  queues the order for the next session's open. It rejects the other stop modes
  and the unaudited optional crystallisation/time-stop paths. It no longer uses
  the full day's high and low to decide an opening fill, and it no longer
  invents opening prices from forward-filled opens or the later close.
- The legacy return booking omitted parts of the actual exposure on entry and
  exit days. The headline now separates overnight exposure before open orders
  from intraday exposure after them; it includes the exit gap and uses this
  return history for the in-loop risk buffer. The original engine booking is
  retained only as a historical comparison. The new booking is still a
  **weight-based approximation**, not an independently reconciled cash and
  share ledger. It assumes target weights at each open, uses an approximate
  transaction-cost and cash-interest treatment, and does not model order-book
  depth, opening-auction fills or circuit-limit fill availability.

## Required data and running

The supplied Upstox series has evidence of retroactive price adjustment; the
other local Upstox copy inspected for HDFCBANK, RELIANCE and TCS shared its
historical values. Neither establishes verified as-traded price units. Before a
credible backtest, supply a directory of **independently verified unadjusted
as-traded daily CSVs** with `datetime` and `close` columns, in the same symbol
names and rupee units as the filed share counts. Coverage and security identity
must be checked by the researcher. Set `CSM_UNADJUSTED_PRICE_DIR` to that
folder. The code cannot verify the data provider's adjustment convention.

The runner and `train_test_protocol.py` accept this directory. Their existing
2019–2025 windows were previously researched and are not a pristine OOS test.
The other old experimental and reporting scripts were not migrated; do not
use their output without separately updating and validating them. A fully
validated cash/share ledger, a point-in-time security master and corporate
changes, and filing-version history are still needed to establish robust live
or historical performance.

## Verification

Run `python3 csm_value/test_csm_value.py`. The focused synthetic tests cover
same-day exclusion, seconds in filing timestamps, late and future filings,
late consolidated results, SME period length, actual month-end session timing,
valuation-data fail-closed behaviour, and a close-triggered next-open stop with
an overnight gap. A scan of the supplied files was also run through the loader;
no strategy performance was computed because verified as-traded prices were
not available. These checks do not prove the data is free of all lookahead or
that all order fills are executable.

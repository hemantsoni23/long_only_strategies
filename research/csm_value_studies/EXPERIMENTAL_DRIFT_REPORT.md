# Experimental CSM Value: drift and trading-cost correction

## What changed

The earlier experimental engine compared successive target weights to
estimate turnover. That could retain a target weight across changing prices
without charging for the trades needed to restore it. The corrected engine:

1. Marks existing stock holdings and cash from the previous close to the
   current open, using the latest available mark when an open is missing.
2. Lets holdings drift between new monthly signals and changes in the applied
   risk multiplier. Entry and exit orders, and a resize deferred by a missing
   open, remain actionable on later sessions. The trade deadband is compared
   with the open-marked holding.
3. Calculates signed buys and sells as the difference between actual modeled
   open holdings and executed weights. It charges the configured one-way
   cost on the absolute amount traded. Buys are reduced if necessary to fund
   costs from available cash; untradeable positions are not resized.
4. Marks the execution book from open to close and carries those holdings and
   cash to the next session. Daily turnover is a fraction of opening book
   NAV; daily cost in the return series is expressed relative to the previous
   close. The transaction ledger records prices, weights, quantities, rupee
   trade values and costs in the model's execution-book units.

Reported strategy returns attribute overnight and intraday price movements to
the positions held during those intervals. On a **full exit**, the requested
zero exit-day stock contribution is preserved. The separate execution book
does include the actual modeled opening gap on a sale, because the sale value,
available cash and cost depend on the opening price. As a consequence, the
reported equity curve is not a cash-and-shares P&L ledger and can diverge from
execution-book NAV. When there is no full exit, the two books' return paths
agree, subject to numerical tolerance.

The source OHLCV prices can be adjusted. Modeled quantities are therefore in
the supplied price units, not guaranteed exchange-share quantities. The
0.30% one-way cost is a fixed model assumption; it does not separately model
bid-ask spreads, taxes, order-book depth, market impact or fill failures beyond
missing opens. It cannot establish that noisy or illiquid stocks are tradable
at those prices. No top-1,000 liquidity filter was added.

## Historical comparison

Both runs use the experimental 20-position long-horizon settings and the
previously examined 3 June 2019–31 December 2024 sample. The old output was
retained; the corrected output uses the `_drift` suffix. The first column uses
the requested zero-exit-day convention.

| Measure | Previous | Corrected |
|---|---:|---:|
| Reported CAGR | 40.29% | 38.32% |
| Reported maximum drawdown | -18.03% | -18.43% |
| Annualized absolute turnover | 706.05% | 724.34% |

The change cannot be assigned solely to costs: the corrected run also lets
weights drift, changes rebalance scheduling and attributes overnight and
intraday returns to the applicable holdings. On the same corrected sample,
the separate execution book has approximately 39.36% CAGR and -18.62% maximum
drawdown. This is a diagnostic for the modeled trade path, not an independent
validation or a claim about actual live performance. The two curves use
different full-exit return conventions.

The corrected reporting window contains 2,287 modeled opening trades across
314 sessions. Their signed trade weights aggregate to the daily turnover to
floating-point tolerance; per-trade fees equal 0.30% of absolute modeled trade
value, and daily fees reconcile to the preceding execution-book NAV. Average
holding time for completed positions was 97.0 calendar days; average equity
exposure on sessions labelled favorable was 86.0%.

## Reproduction and tests

Run `python3 csm_value/run_csm_value_experimental_backtest.py`. Daily output
includes `Turnover`, `Transaction_Cost` and `Execution_Book_Value`; the
separate `_transactions.csv` lists the modeled orders. Prior output files are
not overwritten.

Synthetic tests cover drift without daily rebalancing, monthly turnover,
overnight gaps, entry timing, exit-day zero contribution, costs, fully funded
buys, missing opens, deferred resizes, crash-guard liquidation, report rebasing
and transaction-level P&L. The point-in-time prefix comparison is run with
`python3 research/csm_value_studies/experimental_drift_prefix_check.py`.
In the 2023-prefix check, factors and target positions matched exactly;
executed weights, turnover and returns matched to within 1.3e-15, and the
execution-book NAV matched within 3e-9 currency units. Neither those checks nor
the reused historical sample independently validate the strategy, filing
history, delistings or trading capacity.

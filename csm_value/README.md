# CSM Value strategies

There are two separate strategy/backtest pairs. Each strategy file contains
its own point-in-time fundamentals loader, factor calculation and position
logic. Each backtest file contains the execution, risk management, reporting
and chart logic for that version. The pairs do not import each other.

| Version | Strategy logic | Backtest runner |
|---|---|---|
| Value | `csm_value_strategy.py` | `run_csm_value_backtest.py` |
| Experimental | `csm_value_experimental_strategy.py` | `run_csm_value_experimental_backtest.py` |

Run the value version from the project root:

```bash
python3 csm_value/run_csm_value_backtest.py
```

It defaults to earnings-yield ranking, 20 positions and a 5% maximum stock
weight. The 20% trailing stop remains, the rank buffer is 100%, a rebalance
exit is deferred for two monthly signal drops, and the volatility target is
20%. Bear-market exposure is multiplied by 0.8. This permits up to 100%
equity exposure before the risk overlays, subject to eligible stocks and
available opening prices; actual exposure may be lower.

Run the combined experimental version:

```bash
python3 csm_value/run_csm_value_experimental_backtest.py
```

It defaults to 55% earnings-yield rank, 20% quarterly-profit-growth rank and
25% pullback rank. It also has 20 positions, a 5% stock cap, a 20% trailing
stop and a 100% rank buffer. Its rebalance exit buffer is three monthly signal
drops, its volatility target is 22%, and its bear-market multiplier is 0.5.
The 15% entry stop and loss-scaled cooldown remain active in both versions.
Stops and crash-guard exits are not delayed by the rebalance buffer.

Both sets of long-term settings were selected after examining historical data
and have **not** been independently validated. A longer buffer also delays
rebalancing when a stock stops meeting a fundamental eligibility condition.
The higher volatility targets and equity exposure can materially increase
drawdown. See the [holding and exposure study](../research/csm_value_studies/LONG_HORIZON_REPORT.md).

To compare earlier settings, pass `--risk-profile legacy_value` to either
runner for the old 10-position value-risk settings, or
`--risk-profile exploratory_10_12_bear50` for the earlier 10-position,
10%-cap, 12%-trail experimental risk settings. The runner's ranking remains
the selected runner's ranking unless `--ranking` is specified separately.
On the experimental runner these flags restore the settings, not the former
constant-weight accounting.

Both versions preserve the requested next-session execution rules and the
Elendel convention of zero stock weight on its exit day. They use data only
through **31 December 2024**, and quarterly results become usable only after
their filing date. Their weight-based backtests are not cash-and-shares
execution ledgers. There is no price × volume top-1,000 universe filter.

The default inputs are `fundamentals/` (including `sme/`), the configured
Upstox OHLCV folder and the NSE month-end close file in `data/`. Set
`CSM_FUNDAMENTALS_DIR` to use a different fundamentals folder. Most half-year
SME filings do not meet the current four-quarter requirement. See
[PRICE_DATA.md](PRICE_DATA.md) for data limitations.

Outputs go into `output/`. The standard pair uses the
`csm_value_ey_value_long_term_` prefix; the experimental pair uses
`csm_value_ey_growth_pullback_experimental_long_term_drift_`. Each produces
daily, trade and reject logs and performance charts. Legacy profiles use
separate output names, so earlier reports are preserved.

The experimental runner models a self-financing execution book. Existing
weights drift with prices and cash; at the next opening quote it rebalances
on a new monthly signal or a change in the applied risk multiplier. Entries,
exits and previously blocked orders are processed as they become executable.
The deadband is compared with the actual opening weights, and one-way costs
are charged on each modeled buy and sell. A fully invested target is reduced
as necessary to pay fees without borrowing. The separate `transactions.csv`
lists opening trades, quantities and modeled costs; the daily log includes
turnover, costs and the execution-book value. Daily turnover is expressed
relative to opening book value; the fee in daily returns is expressed relative
to the preceding close, so an overnight gap can make it differ slightly from
`Turnover × fee rate`. Trade-log `PnL_Abs` aggregates modeled cash flows and
fees, while `PnL_Pct` is the entry-to-exit price change.

The execution book is used for position drift, cash availability, trade sizes
and costs. Reported returns attribute overnight and intraday changes to the
positions held during those intervals, while retaining the requested zero stock
contribution for a full exit on its exit day. Consequently the reported NAV
can diverge from the execution-book NAV; it is not the P&L of those trades.
Transactions and quantities use the supplied OHLCV price units, which can be
adjusted, and do not model market impact. The original value runner still uses
its previous target-weight accounting and has not received this correction.

`fundamentals_loader.py` is a small compatibility import for older research
scripts; neither pair needs it to run. `fetch_nse_monthly_prices.py`, `data/`
and `tests/` support the strategies. Run the regression checks with:

```bash
python3 csm_value/test_csm_value.py
```

The pairs intentionally contain separate copies of the engine and fundamentals
logic. Future fixes to shared behavior must therefore be applied and tested in
both pairs. Historical research is retained under `research/`.

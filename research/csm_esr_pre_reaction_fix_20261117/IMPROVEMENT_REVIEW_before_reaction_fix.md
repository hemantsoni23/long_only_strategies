# CSM ESR — problems and improvement candidates

This is a review of the **current** CSM ESR implementation, not a set of
changes already made. The aim is to distinguish a demonstrated limitation
from an idea that still needs an experiment. All backtest numbers below are
historical, use information through **31 December 2024**, and are not an
independent out-of-sample result.

The default 1 September 2020–31 December 2024 report shows **46.98% CAGR**,
**−26.01% maximum drawdown**, and **357 completed trades entered during the
reporting window**. Trade-level returns below are before the modeled buy and
sell fees unless otherwise stated. See [STRATEGY_LOGIC.md](STRATEGY_LOGIC.md)
for the implemented rules and [the report](output/csm_esr_report.txt) for the
full results.

## Priority 1 — establish whether the results and signals are trustworthy

### 1. The supplied fundamentals are snapshots, not a verified filing history

**Confirmed limitation.** The loader respects the supplied filing date and
does not deliberately use a later filing early. However, the JSON snapshot may
contain a revised EPS value labeled with an earlier date. The existing tests
cannot prove what was actually available in the original announcement. A
present-day stock-file list can also omit delisted or renamed stocks.

**Next check:** Compare a sample of original exchange filings, including large
winning trades, large SUE values and split/bonus cases, with the stored EPS,
filing date and reporting basis. Measure coverage of delisted and renamed
securities before drawing conclusions about historical performance. Keep the
existing next-day filing rule.

### 2. The price-reaction window can include movement before an announcement

**Confirmed implementation issue.** Filing timestamps are reduced to calendar
dates. The price-reaction calculation starts at the close before the filing
date's first trading session. If a company reports **after the market close**,
the return therefore includes that day's price movement, even though the
report had not yet been published. This does not mean the strategy trades on
the filing day, and it is not by itself lookahead: it means part of the
measured reaction can be unrelated to the public announcement.

In the 357 completed-trade sample, **199** have a filing date on the report's
trading calendar for which all matching stored timestamps for that symbol and
date are after **3:30 p.m.** This is a conservative count from the supplied
filing timestamps; it is not an independently verified publication-time audit.

**Next check:** Preserve the timestamp and compare reaction windows for
before-market, after-market and non-trading-day filings. Daily OHLCV cannot
isolate the exact pre- and post-announcement movement of an intraday filing,
so disclose that limitation. Signals must still use a report only after its
public date.

### 3. Fundamentals' contribution has not been isolated

**Confirmed research gap.** A company filing is the trigger, and both the
earnings-surprise and price-reaction tests are required. The ranking then adds
the two standardized scores with equal coefficients. We do not yet know
whether using the EPS information improves results compared with a comparable
price-only method. This matters because the user's goal is for fundamentals to
be an important driver, while price data provides supporting information.

**Next test:** Compare the current rules with an event-date-matched version
that retains the same filing dates, stock universe, execution and costs but
does not use EPS values to select or rank stocks. That is a **price-only score
on filing events**, not a fully fundamentals-free strategy: the filing date
still determines when it can trade. Also compare with an independently defined
OHLCV-only strategy under matched dates and execution. Report wins, losses,
average win/loss, CAGR, drawdown, turnover and exposure separately.

### 4. There is no genuinely untouched out-of-sample period

**Confirmed research gap.** The pre-2025 period was already examined during
earlier research. Splitting it into an earlier and a later period is useful as
a historical robustness check, but the later period cannot honestly be
described as an untouched test of rules developed with knowledge of it.

**Next check:** Freeze the research design before any new comparison, report
earlier and later windows separately with this limitation, and obtain a new
unseen period only after its fundamentals are repaired and independently
validated. Do not use 2025–2026 fundamentals in the meantime.

### 5. Extreme EPS-surprise values can dominate the scale

**Confirmed sensitivity, not proof of bad data.** The surprise divides the
latest EPS change by the variability of four to eight previous changes. A
very small denominator can produce a very large score. Among the 357 trades,
**20** entered with SUE above **10**, and the largest recorded value was about
**120.37**. The final ranking term is capped, but raw SUE values also affect
the pool's standard deviation before that cap.

**Next test:** Audit the underlying quarters for the extreme cases. Compare
the current score against a carefully designed minimum-denominator rule,
longer required history or robust scaling, using only data available at each
signal date. Retain and test the current rule as a baseline.

### 6. Share actions and EPS comparability remain only partly checked

**Confirmed limitation.** The 3% share-count rule can exclude split-affected
comparisons, but it can also exclude ordinary issuance and cannot establish
whether historical EPS was retrospectively restated. The portfolio holds a
fixed share quantity; it does not explicitly process a later split or bonus
for an already-held position. Whether the adjusted OHLCV files make the price
returns internally consistent needs verification, especially for volume,
quantity and real execution. The data mask is not a complete corporate-action
ledger.

**Next check:** Reconcile a sample of split/bonus and share-issuance events
against the EPS, share capital, price adjustment and volume convention. Audit
corporate actions that occur after entry. Do not assume a 3% share change is
always an error or remove the guard before validating an alternative.

## Priority 2 — portfolio and trading risks

### 7. The strategy stays heavily invested without a market-wide risk rule

**Confirmed behavior.** Average stock exposure in the reported period was
**92.87%**. The strategy has no default market-trend exposure reduction,
portfolio volatility target or crash exit. Its largest drawdown was **26.01%**;
the portfolio's earlier high on 17 January 2022 was not recovered until
5 July 2023.

**Next test:** Compare the existing always-invested design with a small,
predefined set of market-trend or portfolio-volatility controls. Evaluate
growth, drawdown, time to recover, costs and market re-entry together. A risk
control can also cut returns, so an improvement is not assumed.

### 8. The 15% stop is a trigger, not a limit on actual losses

**Confirmed from trade logs.** The strategy checks the close and sells at a
later open; a gap and the modeled stop slippage can worsen the sale. Of **82**
stop exits, **63** showed an entry-to-exit price loss worse than 15%. Their
average price loss was **16.68%**, and the worst reported trade loss was
**22.81%**, before the separate trading fees.

**Next test:** Examine the individual gap-down events and compare alternative
stop distances, position sizes and realistic execution assumptions. A tighter
stop may reduce some losses but increase churn or miss recoveries; it cannot
guarantee a maximum loss when prices gap.

### 9. Entry fills do not model trade size, order-book depth or current limits

**Confirmed execution-model gap.** A valid opening price is treated as
fillable even for thin stocks; the model has no participation limit or
market-depth/auction model. It applies a flat transaction fee and stop
slippage, but no separate entry slippage. The historical high-equals-low
filter does not prove a stock can actually be bought or sold at the open.

For perspective only, a rough check of the supplied price × volume files found
**10 of 357** trade entries where the median of the preceding 63 available
stock rows was below **₹5 lakh per day**. A 5% target for a ₹1 crore account
is ₹5 lakh, so this illustrates a possible capacity problem. The check is a
proxy: price/volume adjustment conventions and actual opening-auction depth
must be validated before relying on the figure.

**Next test:** Model participation-based sizing, entry and exit slippage,
and orders that do not fill. Preserve the user's request **not** to impose a
blanket top-1,000 traded-value universe filter.

### 10. Portfolio size and exposure are not adapted to stock-specific risk

**Confirmed behavior.** Each new position targets roughly **5%**, regardless
of the stock's volatility, the distance to a realistic fill or trading
capacity; weights can then drift above or below 5%. There is no sector or
common-risk concentration cap.

**Next test:** Compare the current sizing with volatility- or risk-based
sizing and a capacity ceiling, and examine position counts and group/sector
concentration where reliable classifications exist. Measure both growth and
drawdown; fewer or larger positions are not automatically better.

### 11. A fixed 60-session exit dominates the completed trades

**Confirmed behavior; whether it is suboptimal is unknown.** Of the 357
closed trades, **275** exited on time expiry and **82** on a stop. The
time-expiry trades had an average price gain of **18.38%** before fees. The
strategy has no trailing profit-protection rule or exit on a subsequent
earnings deterioration.

**Next test:** Compare the existing 60-session rule with a small, fixed set
of holding periods and with earnings- or price-based continuation/exit rules.
Account for the trades displaced by longer holdings, changed exposure and
costs; a stock rising after an exit alone does not prove holding it was better
for the portfolio. Keep the existing rule as the baseline.

### 12. Gap-ups, the entry window and cooldown need separate evaluation

**Confirmed behavior.** There is no entry gap-up limit, pending signals expire
after five trading sessions, and every stop sale causes a **20-trading-session**
cooldown for that stock, even if the opening fill is profitable. A check of
the logged entries against each stock's previous available close found **33
of 357** entries opened more than **2%** higher. That observation does not
establish whether those entries helped or hurt.

**Next test:** Break down outcomes by opening gap, attempted entry day and
cooldown, including candidates that were not filled. Test alternatives without
using the subsequent outcome to decide whether an individual historical order
would have been placed.

## Priority 3 — reporting and operational readiness

### 13. Cash and trading-cost assumptions need stress testing

**Confirmed assumptions.** Idle cash earns a fixed **6.5% annually**, while
modeled buys and sells cost **0.30% per side**. Reported annual turnover is
approximately **830.89%** of portfolio value. At 0.30% per unit traded,
that is roughly **2.49% of portfolio value per year** in modeled trading fees
before compounding and separate stop slippage; the backtest's net portfolio
result already includes those modeled charges.

**Next test:** Re-run with different cost, slippage and cash-rate assumptions,
including size-dependent costs. Keep price and fundamental signals identical
so the effect of assumptions can be understood.

### 14. Reported trade win rate is gross, and open positions are excluded

**Confirmed reporting limitation.** The displayed **62.75%** win rate uses
entry versus exit price without the separate buy/sell fees. Applying the
modeled **0.30%** fee on each side to those same 357 closed-trade price
returns gives approximately **61.90%** winners and changes average trade
return from **10.32% gross to 9.66% net**. This simple calculation includes
the stop slippage already reflected in recorded exit prices, but it does not
produce a portfolio return. Positions entered before the reporting window or
still open at its end are not counted in those completed-trade statistics.

**Next improvement:** Show both before-fee and after-fee trade statistics,
the number of carried/open positions and an index comparison over identical
dates. Preserve the separate CSM Value zero-exit-day convention; ESR's
cash-and-shares accounting includes price movement before its opening sale.

### 15. The current live-style interfaces are not ready for today's market

**Confirmed operational limitation.** Research data and signals are capped
at 2024. If asked for an entry date beyond loaded history, the current
`get_entry_candidates` method can fall back to the last available session.
For exit dates beyond loaded history, `get_exit_signals` estimates trading
days using weekdays and does not account for all exchange holidays. These
interfaces should not be used to place live orders in their current form.

**Next improvement:** Once a refreshed source is validated, reject stale or
future-as-of requests explicitly, use an exchange trading calendar, and test
the daily live process against the historical execution rules.

## Suggested order of work

1. Audit filing history, timestamp handling and corporate-action examples.
2. Establish matched price-only and event-matched controls; document which
   historical windows are already contaminated by earlier research.
3. Add realistic capacity and transaction-cost stress tests without a
   top-1,000 universe filter.
4. Experiment with a few portfolio-risk, sizing and exit variants only after
   the baseline and measurement rules are fixed.
5. Improve the live interfaces only after the post-2024 data is validated.

## How the quick checks were calculated

- Daily exposure and drawdown use `output/csm_esr_daily_log.csv`; completed
  trades use `output/csm_esr_trade_log.csv`. The log excludes open positions
  and positions entered before the reporting window from trade statistics.
- Entry gaps compare each recorded entry price with the previous available
  raw OHLCV close. Capacity uses the median of price × volume for the last 63
  available stock rows before entry; it is not an opening-auction estimate.
- The filing-time check matches each traded ticker and stored filing date
  against both reporting bases in the supplied JSON. A case is counted as
  after 3:30 p.m. only when every same-date match has a later timestamp and
  the filing date appears in the report's trading calendar.
- Net closed-trade price return is calculated as `exit ÷ entry × (1 − 0.003)
  ÷ (1 + 0.003) − 1`. These trade-level statistics are not a replacement for
  the portfolio's cash-and-shares accounting.

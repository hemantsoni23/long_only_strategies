# CSM ESR (Earnings Surprise & Reaction) — complete strategy logic

Former name: **CSM PEAD Confirmed-Drift**. This document describes the current
default implementation and the historical backtest, not a proposed change or
a promise of future results.

The idea is to identify a quarterly earnings announcement that is unusual for
the company and is followed by a strong share-price reaction. The strategy
then buys eligible candidates and holds them for a limited period unless the
stop is triggered first. Fundamentals supply the event and earnings-surprise
signal; OHLCV supplies the price-reaction condition, price checks, execution
prices and stops.

**Flow:** matching stock files → usable quarterly filing → earnings surprise →
announcement price reaction → compare both with recent events → select a
candidate → buy at an eligible open → hold and monitor → sell at a later open.

## 1. Data and universe

| Item | Implemented default |
| --- | --- |
| Fundamentals | JSON files in `fundamentals/` and `fundamentals/sme/`; override with `CSM_FUNDAMENTALS_DIR`. A stock needs usable filing history for the earnings calculation. |
| Prices | Daily OHLCV files in `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data`. The shared loader starts from OHLCV symbols with a matching fundamentals filename. A filename match alone does not prove historical security identity. |
| Research boundary | Filings and simulation prices are limited to **31 December 2024**. The default reporting window is **1 September 2020–31 December 2024**. Earlier available prices and results are used for warmup. |
| Ranking-based universe filter | **None.** There is no top-1,000 filter based on traded value and no default minimum daily volume. This does not mean all stocks are tradable. |
| Price check | At an attempted entry, the previous available close, forward-filled if necessary, must be **above ₹20**. This is also checked when building the signal pool, using the signal-day information available before the next session. |
| Flat-price check | Count days with a recorded high equal to low over the previous **63 trading sessions**; at most **5** may be flat. The count is shifted by one session for entry decisions. Missing high/low observations do not prove a flat day; if the entire high/low dataset is absent, this check defaults to passing. |
| Corporate-action/outlier mask | A day's OHLC prices are masked if its raw close-to-close change is **less than −40% or greater than +300%**. This is a data-cleaning rule, not proof that all splits, bonuses or erroneous prices have been corrected. |
| Market comparison series | Built from the daily returns of the loaded, fundamentals-filename-matched stock files. Each observed daily stock return is clipped to **−50% to +50%** before the available returns are averaged equally and compounded. This is an internal comparison series, **not Nifty**. |

The present-day file list may omit stocks that delisted or changed names. It is
not a verified historical list of every stock that was investable at the time.

## 2. Which quarterly results can create an event?

| Check | Implemented rule |
| --- | --- |
| Actual quarter | Period start-to-end must be **80–100 days**, and the period must end on a calendar quarter-end. A six-month SME report is not counted as a single quarter. |
| Public filing date | A valid filing date is required and must be from the period end through **120 calendar days** afterward. A result cannot be acted on during its filing date. |
| What is known | Process facts in filing-date order and use only facts filed by that event. Same-date facts are processed together. Later filings do not replace an event already emitted for an earlier date. |
| Reporting basis | Standalone and consolidated histories are kept separate. If both bases have a valid surprise for the same period on the same filing date, consolidated is preferred. A later consolidated filing does not retrospectively replace an earlier standalone event. |
| Old or repeated periods | Only a filing for the newest known quarter can create a new event; an older late result does not create a fresh event after a newer quarter is known. At most one valid event is emitted per stock and period. |
| Required fields | Basic EPS and a valid share count are needed for the current quarter and for the historical quarters actually used in its comparison. Share count = paid-up equity share capital ÷ face value. Face value must be one of **₹0.50, ₹1, ₹2, ₹5, ₹10 or ₹100**. |
| Share-count guard | Each historical EPS observation used in the calculation must have a share count within **3% of the current quarter's** share count. A missing or more-different observation is excluded from that calculation. This may reject genuine share issuances as well as split/bonus effects. |

**Important limitation:** the JSON files are snapshots. The code does not
backdate a value before its supplied filing date, but a snapshot cannot prove
whether a later revision or retrospective EPS restatement replaced the value
originally published. The share-count guard reduces one problem; it cannot
verify the full revision history.

## 3. Fundamental factor: earnings surprise

EPS means earnings per share. The strategy compares the latest quarterly EPS
with the EPS from the **same quarter one year earlier**, then asks how large
that difference is compared with the company's past quarterly differences.

| Component | Formula or rule |
| --- | --- |
| Current seasonal difference | `latest quarter EPS − EPS for the same quarter a year earlier` |
| Prior differences | Calculate the same year-over-year EPS difference for up to the preceding **8 quarters**. Use only EPS observations that were already filed and pass the share-count guard. |
| Minimum history | At least **4 valid prior differences** are needed. Their **sample standard deviation** must be positive. Otherwise there is no valid surprise for that event. |
| Standardized unexpected earnings, or SUE | `current seasonal difference ÷ standard deviation of valid prior differences` |
| Fundamental eligibility | A valid SUE is required. The default does **not** separately require positive EPS, positive annual profit, rising net profit or an improved margin. A high percentile can still be negative if other eligible events are even lower. |
| Optional margin filter | Available but **off by default**. If enabled, the latest year-over-year change in `(profit before tax + finance costs) ÷ operating revenue` must be positive and available. |

**Example:** Suppose current EPS is ₹8 and EPS in the same quarter last year
was ₹5. The difference is ₹3. If the standard deviation of the usable earlier
year-over-year EPS differences is ₹1.50, SUE is **3 ÷ 1.50 = 2.0**. This is a
relative score, not a 200% investment return.

## 4. OHLCV factor: announcement price reaction

| Step | Implemented rule |
| --- | --- |
| First eligible session `A` | The first trading session **strictly after** the public filing date. The result is not usable on its filing date. |
| Starting price | The last trading close **on or before** the filing date, immediately before `A`. This close is a price reference, not permission to use the report on its filing day. |
| Signal session `S` | The **second trading session strictly after the filing date**: `S` is the session after `A`. The signal is known after that day's close. |
| Stock return | `stock close on S ÷ stock starting close − 1`. Both stock closing prices must be actually observed; stale forward-filled stock closes are not used for this calculation. |
| Market return | `internal market series on S ÷ the series on the starting-close session − 1`. |
| Excess announcement return, or EAR | `stock return − market return` over the same interval. A larger number means the stock reacted more strongly than the internal comparison series. |
| Outlier check | If the stock's return over the announcement interval is **less than −60% or greater than +200%**, the reaction is treated as unavailable. |
| Other price filters | There is no default requirement for the stock to be above a moving average and no absolute-momentum entry gate. The optional market-wide moving-average gate is off. |

**Example:** A result is filed on Monday. If the following sessions are normal,
Tuesday is the first eligible session, Wednesday is the signal session, and the
stock and market returns are measured from **Monday's close to Wednesday's
close**. The earliest possible purchase is Thursday's open. If a filing happens
on Saturday, Friday is the starting-close session, Monday is the first eligible
session, Tuesday is the signal session and Wednesday is the earliest possible
purchase. Holidays can shift these dates.

This deliberately excludes the filing-day price movement, including a reaction
that may have occurred after a pre-market or intraday announcement. It avoids
mistaking price movement before an after-market filing for a reaction, but daily
OHLCV cannot isolate the exact moment an intraday announcement became public.

## 5. Selection thresholds and ranking

| Stage | Implemented rule |
| --- | --- |
| Comparison pool | At signal close, collect eligible events whose signal dates fall within the preceding **120 calendar days**, including the current signal date. Events from the same signal date are processed together. This is a count of **events**, not necessarily distinct companies. |
| Minimum pool | At least **150** events must have valid SUE, valid EAR and pass the price/flat-day checks. Otherwise no candidate is created for that event. |
| Fundamental threshold | SUE must be at or above the pool's **70th percentile**: the top 30% threshold. |
| Price threshold | EAR must independently be at or above its pool's **70th percentile**. Passing one condition is not enough; **both** must pass. Neither threshold is required to be above zero. |
| Score for scarce slots | `score = clip((SUE − SUE threshold) ÷ pool SUE standard deviation, 0, 5) + clip((EAR − EAR threshold) ÷ pool EAR standard deviation, 0, 5)`. Both terms use the pool's population standard deviation. If either required standard deviation is zero, the score is unavailable and the event is not a candidate. |
| Meaning of the score | The two standardized terms have equal coefficients in the sum; each is measured in its own units and capped at 5. This is **not** a 55%/20%/25% value score, and the coefficients do not determine portfolio allocation. |
| Candidate order | Pending candidates are tried from highest combined score to lowest when a slot is available. Ties follow their existing order. |

**Score example:** If SUE is 1.8, its threshold is 1.2 and its pool standard
deviation is 0.3, the SUE term is 2.0. If EAR is 9%, its threshold is 5% and
its pool standard deviation is 2 percentage points, the EAR term is 2.0. The
combined score is **4.0**. Both individual thresholds were passed first.

## 6. Entry: when does a selected stock actually get bought?

| Step | Implemented rule |
| --- | --- |
| First opportunity | A signal at `S` close can first be bought at the **next trading session's open**. The strategy does not buy using the closing price on the signal day. |
| Entry window | Retry a pending candidate on trading sessions **S+1 through S+5**, inclusive. After that the candidate expires. The stock can enter later than S+1 if a slot or valid opening price becomes available within this window. |
| Slot limit | Maximum **20** simultaneous holdings. A held stock, including one waiting for an exit because its opening price is missing, occupies a slot. |
| Other entry checks | A stock must not already be held, be within its stop cooldown or have exited that same day. It must pass the current previous-close price and flat-day checks and have a valid positive opening price. The optional market gate, if enabled, must also pass. |
| No valid open | No purchase is modeled at that session's close or at an invented open. The candidate can be retried while its entry window remains open. |
| Same-day sale and new purchase | Scheduled exits are processed first at the open. Cash and slots they free can be used for another candidate, but the stock just sold is not repurchased that same day. |

The completed-trade log records `Filed`, `Reaction_Base_Date`,
`Available_Date` (the first eligible **trading session**), `Signal_Date` and
`Entry_Date` so this sequence can be audited for each trade.

## 7. Position sizing and portfolio management

| Item | Implemented rule |
| --- | --- |
| Initial target | Up to **1 ÷ 20 = 5%** of the portfolio's value at the open for each new stock. The amount is limited by available cash after providing for the buy fee. |
| Example | For a ₹10 lakh portfolio, a new position targets up to ₹50,000 of stock before its buy fee. If cash is limited, the actual purchase can be smaller. |
| Fewer positions | With ten newly sized 5% positions, roughly 50% is initially invested and the remainder is cash, before price moves and fees. There is no rule that forces 80–100% exposure. |
| Weight drift | Shares are held until a sale; their portfolio weights move with prices. The strategy does **not** rebalance every day to restore each stock to 5%. A holding's weight can grow above 5% after entry. |
| Idle cash | Modeled as earning **6.5% per year**, converted to a trading-day rate of `(1 + 0.065)^(1/252) − 1`. This is a simulation assumption, not a guaranteed cash return. |
| Transaction costs | Charge **0.30% of traded value on each buy and each sell**. Turnover is based on actual modeled transaction amounts, not price-driven changes in holding weights. |
| Liquidity and sector limits | No default trade-size participation cap, sector cap or market-depth model. The backtest cannot ensure that a real order would fill at the assumed open. |

## 8. Stop, holding period and exits

| Rule | Implemented default |
| --- | --- |
| Initial hard stop | `entry price × 0.85`: **15% below the opening purchase price**. It is a closing-price trigger, not a guaranteed fill price. |
| Stop decision | On any held session, including the entry day, a valid close at or below the hard stop schedules a **STOP_HIT** sale at the next valid open. There is no five-day minimum holding period. |
| Stop fill | The next valid opening price is reduced by **0.30% modeled stop slippage**; the separate **0.30% sell fee** is also charged. Gaps can produce a much larger loss than 15%. |
| Time exit | At the close of the **60th trading session after entry**, the holding period is considered expired and a **TIME_STOP** sale is scheduled for the next valid open. Under normal availability, the sale is on the 61st session after entry. The time-expiry check takes priority if both rules are true on the same close. |
| Missing open on a scheduled exit | The holding remains in the book and the sale is retried at a later valid open. It continues to occupy a position slot. |
| After a stop | The same stock is blocked for the next **20 trading sessions** after its stop sale. The cooldown check allows it again from the 21st session, if a still-valid or new signal permits. A normal time exit has no stop cooldown. |
| Trailing/profit exits | No trailing stop, profit target, partial profit-taking rule or earnings-deterioration exit is enabled in the default implementation. A new quarterly result does not automatically sell an existing holding. |
| End of backtest | Remaining holdings are marked at the final available close; this is not a simulated sale. Missing closes are forward-filled for marking holdings, which can understate the difficulty of valuing an illiquid stock. |

**Stop example:** A stock is bought at ₹100. Its trigger is ₹85. If it closes
at ₹84, the strategy schedules a sale for the next valid open. If that open is
₹80, modeled stop slippage gives a fill of ₹79.76 before the separate sell fee.
The stock is blocked for the following 20 trading sessions after that sale.

## 9. Market-level risk management

| Control | Current default |
| --- | --- |
| Market trend gate | **Off.** If explicitly enabled, new entries require the previous close of the internal market series to be above its previous 200-session moving average; the average requires at least 160 observations. This gate blocks entries rather than automatically selling holdings. |
| Volatility target or crash exit | **None.** There is no default portfolio volatility targeting, market crash liquidation, exposure multiplier or drawdown-based reduction. |
| Market-regime labels in the report | `BULL`, `BEAR`, `HIGH_VOL` and `PANIC` are descriptive report labels. They do **not** by themselves change exposure or cause an exit in this implementation. |
| Position-level protection | The 20-stock limit, initial 5% target and 15% hard-stop trigger are the main default controls. A 5% initial position losing 15% implies approximately 0.75% of initial portfolio value before gaps, fees, weight drift and other positions; it is **not** a maximum guaranteed portfolio loss. |

## 10. Return accounting and reports

| Item | How to interpret it |
| --- | --- |
| Portfolio return | A cash-and-shares book records price movements, cash interest, actual modeled buys and sells, fees and stop slippage. It includes a stock's overnight movement before its opening sale. |
| Difference from CSM Value | The user's intentional **zero exit-day stock-weight convention** for CSM Value is not applied to this cash-and-shares book. Compare reported results with care; the accounting conventions differ. |
| Win rate in the detailed trade report | A completed trade wins when its exit price exceeds its entry price. The displayed trade percentage is before trading fees; portfolio performance includes the modeled fees. Only trades **entered** within the reporting window are included in those trade statistics. |
| Reporting starting point | The displayed portfolio is rebased to ₹100,000 at the first reporting day's close. The transaction CSV covers trades after that close. Actual modeled rupee trade values use the original continuous cash book. |
| In-sample and out-of-sample | A research split must be chosen and documented before tuning. The currently available pre-2025 history was already inspected during earlier research, so neither a split nor the default backtest should be called an untouched independent test. A matched technical-only baseline is also still needed to measure the incremental contribution of fundamentals. |

## 11. Worked stock journey

1. A company files its quarterly report on Monday; the report has a usable EPS
   history and comparable share counts.
2. The strategy may use the result from Tuesday onward. It waits until
   Wednesday's close and measures the stock's reaction from Monday's close,
   comparing it against the internal market series over the same period.
3. At that close, the event is compared with the last 120 calendar days of
   eligible events. If at least 150 are available and the stock passes both
   top-30% thresholds, it becomes a candidate with a combined score.
4. Starting at Thursday's open, the runner checks its rank among pending
   candidates, the available slots, cooldown, price and opening quote. If it
   can buy, it targets up to 5% of the portfolio. It can retry through S+5.
5. If bought at ₹100, its initial closing-price stop is ₹85. Its share weight
   drifts with the market; it is not reset to 5% every day.
6. A close at or below ₹85 schedules a next-open stop sale. Otherwise, after
   the 60-session holding-period check, a time exit is scheduled for the next
   valid open. Missing opens delay the sale.

This is the implemented default flow. The historical results are affected by
the available stock files, filing snapshots, modeled execution, transaction
costs and the cash-rate assumption; they should not be treated as a live
trading guarantee.

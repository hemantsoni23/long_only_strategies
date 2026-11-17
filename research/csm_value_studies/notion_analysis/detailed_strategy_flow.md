## Detailed strategy logic: from stock list to exit

The first table is a quick overview. The tables below show the default settings used for the normal and experimental results in this document. They describe the historical backtest, including its assumptions; they do not imply that an order would always fill in a live market. The two versions share most rules, so “same” means the full rule in the normal column applies to the experimental version too.

**The journey:** Stock files → usable company results → price and profit checks → ranking → monthly selection → opening trade when allowed → daily risk and stop checks → sale or continued holding.

### 1. Starting stock list and available information

| Step | Normal value | Experimental value |
| --- | --- | --- |
| Starting files | Uses OHLCV files whose symbol also has a JSON fundamentals file, including the `sme` folder. For a stock to get a factor, usable results and a matching as-traded valuation price are also required. | Same. |
| End date | Research is limited to **31 December 2024**; 2025–2026 fundamentals are not used in these runs. | Same. |
| Publication date | A result filed on 2 November is available from 3 November onward. The month-end decision uses the actual last trading session, not a later weekend month-end date. A filing on the decision day cannot be used that day. | Same. |
| Which reports qualify? | Uses separate quarters lasting 80–100 days, filed no more than 120 days after the reporting period ends. Requires four consecutive quarter-end results with profits and a valid share count. Half-year reports alone do not qualify as four quarters. | Same. |
| Result age and choice | The latest quarter's filing must be no more than **140 calendar days** old at the signal date. Uses the newest complete reporting period, preferring consolidated results if both bases have that period. | Same. |
| Price for company value | Share count = paid-up equity share capital ÷ face value. Company value = share count × that month's as-traded closing price. It does not fill an older valuation price into a missing signal-day quote. | Same. |

### 2. Checks before a stock can be ranked

| Check | Normal value | Experimental value |
| --- | --- | --- |
| Minimum price | Previous month-end's as-traded price must be **above ₹20**. | Same. |
| Flat-price days | In the preceding 63-session window, after shifting the daily high/low test by one session, no more than **5 days** may have high equal to low. This is a rough filter, not proof of an exchange circuit. | Same. |
| Earlier monthly fall | The previous month's return must be **at least −15%**; a worse fall fails the check. | Same. |
| Profit and growth | Sum of net profit from the latest four consecutive quarters must be **positive**. The latest quarter's profit must also be higher than the same quarter a year earlier. The prior-year quarter must therefore be available for this check. | Same. |
| Earnings yield | Earnings yield = four-quarter net profit ÷ company value. It must be valid and **no more than 50%**; positive four-quarter profit is required separately. | Same. |
| Corporate-action check | The strategy checks whether the filed share count and price units might have changed after the reporting period. An unclear reference or detected split-like change can exclude the stock until the figures are usable. | Same. |
| Minimum passing stocks | At least **60** stocks must pass the checks for that month's factor signal. If fewer pass, the month has no ranked selection; the ordinary exit buffer still governs existing holdings. | Same. |
| Liquidity ranking and extra gates | There is **no top-1,000 price × volume filter** and no default minimum-volume or position-capacity limit. There is also no absolute-momentum gate or mandatory stock-price-above-moving-average entry rule. | Same. Price movement is used in the ranking, but being above a moving average is not a mandatory entry condition. |

**Earnings-yield example:** If four-quarter profit is ₹10 crore and company value is ₹100 crore, earnings yield is 10%. This compares company profit with company value; it is not a promised 10% investment return.

### 3. Factor calculations and ranking

| Calculation | Normal value | Experimental value |
| --- | --- | --- |
| Value component | Eligible stocks are ranked by **earnings yield**: a higher yield receives a better rank. The code standardizes yields across the eligible stocks before ranking; this preserves their order. | **55% of the final score** comes from the stock's percentile rank for earnings yield. |
| Profit-growth component | Profit must be rising to pass the filter, but its growth rate does not add a separate ranking score. | **20% of the score** comes from percentile rank of symmetric profit growth = (latest quarter profit − profit in the same quarter a year earlier) ÷ [(absolute latest profit + absolute earlier profit) ÷ 2]. Higher gets a better rank. |
| Price component | No price factor is added to the ranking score. Price data still affects eligibility, sizing, market risk and exits. | **25% of the score** comes from a price-weakness score: 1 − average of the percentile ranks of the two measures below. Lower relative strength and lower trend persistence increase this component. |
| Price measure 1 | Not used for ranking. | Stock close ÷ the strategy's market indicator creates a relative-strength line. Divide that line by its highest level in the last **252 sessions**; at least **200 observations** are required. |
| Price measure 2 | Not used for ranking. | The proportion of the last **126 sessions** for which the stock was above its 50-session average. The moving average requires 40 observations and the proportion requires 100. |
| Final score | **100% value ranking** among stocks that pass the common checks. | **0.55 × value percentile + 0.20 × growth percentile + 0.25 × price-weakness score**. The three weights add to 100%; they do not mean 75% of portfolio money is invested in fundamentals. |
| Missing secondary measure | A stock without valid earnings yield cannot be ranked. | Missing growth or price sub-measure receives a neutral percentile of **0.50** in the score, but the separate profit-growth eligibility check still applies. Tied percentile ranks are averaged. |

**Score example:** If value percentile = 0.80, growth percentile = 0.60, and the two price-measure percentiles are 0.25 and 0.75, the price-weakness score is 1 − (0.25 + 0.75) ÷ 2 = 0.50. Final score = 0.55 × 0.80 + 0.20 × 0.60 + 0.25 × 0.50 = **0.685**. Stocks are ordered from higher to lower scores.

### 4. Monthly stock selection and the actual purchase

| Step | Normal value | Experimental value |
| --- | --- | --- |
| Decision timing | Calculate and rank using information available by the **last trading close of the month**. A new selection becomes actionable at the **next trading session's open**. | Same. |
| New candidates | A stock not on the previous monthly selection list normally needs to rank **1–20** to become a new candidate. | Same. |
| Existing selections | A stock on the previous monthly selection list can remain selected through **rank 40**, provided it still qualifies. This is a selection-list rule, not a guarantee that it is currently held. | Same. |
| Replacing a selected stock | Fill free selection slots with the best-ranked new candidates first. If all 20 slots are full, a new candidate must rank at least **10 places better** than the weakest retained selection it replaces. Example: rank 15 can replace rank 27; rank 20 cannot replace rank 27. | Same. |
| Purchase checks at the open | A selection is not automatically a purchase. A slot must actually be free, the stock must not be in cooldown or already exited that day, and a valid open and sufficient modeled capacity must be available. Candidates are tried in rank order. Buffered holdings can occupy slots. | Same, with available cash and modeled transaction costs also checked in the execution book. |
| Gap filter | The standard results use the event-driven mode: **no 2% gap-up entry filter**. The optional live-replica mode skips a new entry when the opening price is more than 2% above the previous close. | Same. |

### 5. Position size and portfolio risk

| Rule | Normal value | Experimental value |
| --- | --- | --- |
| Starting weight | Up to **20 positions**. Uses each selected stock's previous-day-shifted 21-session return volatility: a calmer stock gets a relatively larger starting share. Missing or zero volatility is replaced with 2% daily volatility. | Same initial target calculation. |
| Per-stock target limit | The effective limit is the smaller of **5%** and risk budget ÷ stop distance = **0.75% ÷ 15% = 5%**. Twenty stocks at 5% can target 100% before portfolio risk reductions. With fewer stocks, the 5% cap leaves cash. | Same initial target cap. Actual weights can drift above or below target between trades as prices move. |
| Market indicator | An internally constructed equal-weight series from daily returns of loaded stocks with a fundamentals file; it is **not Nifty**. Each stock's daily return is clipped to −50% to +50% before averaging. | Same. |
| Weak-market multiplier | If the market indicator's previous close is below its previous 200-session average, use **0.80** of planned exposure; otherwise the ordinary multiplier is **1.00**. | Weak-market multiplier is **0.50**; ordinary multiplier is **1.00**. |
| Portfolio movement limit | Estimate annualized movement from past portfolio stock returns. After 21 observations, use the latest 21 until 63 are available, then use 63. Scale = smaller of **1** and **20% ÷ measured annualized volatility**. It can reduce exposure, not increase it above the target. | Same method, but target is **22%**. |
| Stocks moving together | If 21-session portfolio movement divided by the weighted average movement of its stocks exceeds **0.80**, the correlation-guard multiplier becomes **0.50**; otherwise it is 1. This is a movement ratio, not a calculated pairwise correlation of 0.80. | Same. |
| Combining risk controls | Planned stock targets are multiplied by the movement-limit scale × correlation-guard scale × the market multiplier. The combined movement/correlation scale is updated at least every **5 sessions** or sooner when it changes by **0.05** or more. | Same risk calculation. Continuing holdings are adjusted at a monthly signal or when the applied risk multiplier changes, subject to the trading band below. |
| Small adjustments | For a continuing position, skip a modeled resize smaller than **0.25 percentage points** of portfolio value. New entries and full exits are not skipped by this band. | Same 0.25-point band, measured against the position's actual open-marked drifting weight. |
| Turbulent-market protection | Daily crash guard compares the previous-session 21-day market movement with its expanding historical **95th percentile**. If triggered, it attempts to sell all holdings at that session's open and blocks new purchases for **10 trading sessions**; a missing open delays that stock's sale. A crash-sold stock also receives a separate **20-calendar-day** stock cooldown. Repeated panic signals can restart the market-wide wait. Separately, the monthly panic setting can reduce the market multiplier to **0.50**. | Same. |

**Sizing example:** A ₹10 lakh portfolio with a 5% target would put up to ₹50,000 in one stock before risk reductions. If the market multiplier is 0.50, the volatility scale is 0.80 and the correlation scale is 1.00, the indicative target is ₹50,000 × 0.50 × 0.80 = **₹20,000**. Actual trades can differ because of the trading band, cash, price changes or missing opens.

### 6. Holding, stops and exits

| Rule or event | Normal value | Experimental value |
| --- | --- | --- |
| Stop at purchase | Initial stop = higher of **entry price × 0.85** and **entry price × 0.80**, so initially it is 15% below entry. The stop is checked using closing prices; no separate ATR trailing stop is enabled by default. | Same. |
| Trailing stop | After entry, track the highest of the entry price and subsequent closing prices. Stop = higher of the previous stop, **85% of entry price**, and **80% of that peak**. It can rise but cannot fall. | Same. |
| Stop trigger and sale | Once held for at least **5 calendar days**, a close at or below the stop schedules a sale at the **next valid session's open**. A gap can make the fill worse than the stop. The five-day rule applies to stock stops, not all other exit types. | Same. |
| Extreme fall | A close more than **60% below entry** is separately flagged as an extreme stop; under the default close-confirmed mode it also schedules a later opening sale, subject to the five-day stop holding rule. | Same. |
| Leaving monthly selection | If an actual holding is absent from the new selection, it is retained for the first **2 consecutive monthly signals**. If still absent on the **third**, it is scheduled for sale at a valid open. Returning to the selection resets the count. | Retained for the first **3 consecutive monthly signals**; sale is due on the **fourth**. Returning to the selection resets the count. |
| Other exits | A market crash can cause a sale. A failed profit or other eligibility check can remove a stock from the selection and start the monthly exit buffer; it is not a separate immediate fundamental exit. No fixed profit target, default time-stop exit or partial profit-taking rule is enabled. | Same. |
| After a losing stop | Wait in calendar days = clip[20 × loss percentage ÷ 10, minimum 10, maximum 60], rounded down to an integer. Examples: −5% → 10 days; −10% → 20; −15% → 30. A stop at break-even or profit normally gets zero loss-based cooldown. | Same. A stock sold by crash guard instead gets the separate flat 20-calendar-day stock cooldown described above. |
| End of test | A still-open position is marked at the final close for reporting; it is not treated as a real sale. | Same. |

**Stop example:** Buy at ₹100. The initial stop is ₹85. If the highest later close reaches ₹150, the trailing level becomes ₹120. If a later close is ₹119 after the five-day minimum, a sale is scheduled for the next valid open; that open could be below ₹120.

### 7. Trade costs and how returns are recorded

| Rule | Normal value | Experimental value |
| --- | --- | --- |
| Modeled cost and cash | Charges **0.30% of modeled buy or sell value**. Uninvested cash is assumed to earn **6.5% per year**, converted to a daily rate over 252 sessions. These are backtest assumptions. | Same cost and cash-rate assumptions. |
| Weight changes | Uses executed target weights in the return calculation. It does not fully model the trading needed to maintain those weights as market prices change, so its modeled costs can be too low. | Holdings drift as prices move; on an actual modeled resize, buy or sale, costs are charged on the calculated trade amount. |
| Entry-day return | Uses the day's executed weight multiplied by the stock's close-to-close return, even though the modeled entry is at the open. | The reported return uses open-to-close movement for a new position, with prior holdings' overnight movement handled separately. |
| Full exit day | As requested for this strategy, a fully exited stock has **zero stock-return weight for that day** in the reported curve. | The requested full-exit-day exclusion is also applied; the reported curve therefore differs from the separate execution-book value and from ordinary broker profit and loss. |


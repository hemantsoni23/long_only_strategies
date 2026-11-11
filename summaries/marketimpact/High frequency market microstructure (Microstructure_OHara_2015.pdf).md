# High frequency market microstructure

Maureen O’Hara. *Journal of Financial Economics* 116 (2015), 257–270. DOI: 10.1016/j.jfineco.2015.01.003. Available online January 29, 2015.

Source: [original PDF](../../Finance/Microstructure_OHara_2015.pdf), 14 pages. References use printed journal pages. This is a conceptual research-agenda article with two empirical illustrations, not a newly specified equilibrium model or a complete survey of HFT. All institutional descriptions below refer to the article's historical setting, principally 2013–2014; they are not current exchange specifications or legal guidance.

## Why this matters

A trade recorded as seller-initiated can be one small execution of a large institutional **buy** decision. This observation changes the interpretation of one of empirical microstructure's most familiar variables: the sign of a trade. The sign of the aggressor describes who demanded immediate execution, not necessarily which side possesses information or which direction the underlying investor wants to trade.

O’Hara's central argument is that high-frequency trading changes the economic meaning of market data, not just its sampling frequency. Institutional investors, retail brokers and exchanges adapt strategically as well. Their responses alter order routing, displayed liquidity, execution size, the visibility of trading intentions and the relationship between a reported price and an available execution opportunity.

The paper's most concrete evidence is a 2013 sample of **243,772 institutional VWAP parent orders**, producing **13,468,847 child executions**. By dollar value, only **12.57%** of execution is aggressive, compared with **65.53% passive** and **21.90% within the spread**. A model that treats each aggressive trade as an independent information-bearing decision can therefore miss most of the underlying order and assign the wrong direction to its passive fills.

The contribution is diagnostic rather than a finished replacement model. The article identifies what a better model or empirical design must represent: parent orders and strategic execution, heterogeneous access latency, linked venues, inventory limits, hidden liquidity and horizon-dependent information. It does not estimate a single causal effect of HFT on welfare, prove that passive traders are always informed, or establish that trade signs contain no useful information.

## 1. The market mechanism: speed interacts with design

### Fragmentation and heterogeneous information sets

The historical setting combines multiple exchanges, alternative trading systems, crossing networks, internalizing brokers and related derivatives markets. Competition and access rules make liquidity portable across venues, while different fees, order types and priority rules make those venues economically distinct. Routing is a search and scheduling problem, not simply choosing the exchange with the largest displayed book.

Direct data feeds and co-location create different observation and response times. A price may already have changed on one exchange while another trader still sees an older consolidated quote. Speed consequently has two effects: it helps a trader act on a signal sooner and helps avoid executing against a signal already observed by someone else. A stale quote can be adversely selected even when the underlying news was publicly released.

The paper reports historical Tokyo Stock Exchange access latencies ranging from several milliseconds for standard service to **260 microseconds** for a priority connection and **15.7 microseconds** for co-location. These are examples of deliberately differentiated access, not universal latency parameters for a model. It also cites SEC statistics that **23% of canceled orders and 38% of canceled quotes** were canceled within **50 milliseconds**. Frequent updating therefore changes what an apparently available order means to a slower participant.

An empirical researcher needs both event time and the information-arrival time available to the trader being modeled. A perfectly reconstructed universal chronology does not imply that every participant saw that chronology in real time. This is an identification issue, not solely a database-cleaning problem.

### Queue position, order types and exchange fees

With price–time priority, better prices execute first and earlier orders at the same price have priority. Faster submission and cancellation can then have value even without superior fundamental forecasts. Pro rata or size-sensitive priority changes that optimization problem: a strategy adapted to one matching rule cannot be evaluated as if it faced another.

Maker–taker pricing rewards passive liquidity provision through rebates and charges liquidity takers. Taker–maker reverses those incentives; other venues use symmetric fees or subscriptions. An economically relevant execution price must therefore include applicable fees and rebates, but a rebate is only one component of cost. Queue delay, fill probability and adverse selection can dominate a nominally attractive fee schedule.

The article describes the historical “hide not slide” order type as illustrating how an apparently small rule can affect queue priority when markets unlock. It also discusses differentiated rebates for setting versus joining a best price, retail-specific liquidity programs and the then-emerging use of latency delays. These examples demonstrate endogenous market design: venues choose rules to attract a desired mixture of order flow, while traders optimize against those rules.

They are not controlled experiments isolating the welfare effect of a particular order type. The paper gives no common dataset, treatment assignment or counterfactual that would support such a causal estimate. Reproducing an example's strategy today would require the applicable historical rulebook, fee tiers and data feeds, none of which is fully embedded in the PDF.

### HFT is a family of strategies

The article distinguishes market making and cross-asset arbitrage from strategies that exploit predictable execution patterns or deliberately disrupt market processes. It emphasizes that fast market making can supply useful liquidity and improve price alignment, while some fast strategies harm other traders. Aggregating them under one HFT label can obscure the mechanism being studied.

A high-frequency market maker may buy one instrument and sell a related one across venues, managing a network of correlated positions. This can connect liquidity conditions across markets. It also need not create a continuous two-sided commitment in each security. Risk controls can withdraw or freeze quoting when inventory or strategy outcomes hit preset limits.

The relevant information horizon can be milliseconds or seconds rather than the weeks associated with some traditional dealer inventories. Knowing an impending parent-order schedule, observing a related-market price first, or anticipating a queue change can be economically valuable over that horizon even without information about long-run fundamental value.

## 2. Why inventory and information cannot be cleanly separated

Canonical models often divide traders into privately informed traders, uninformed liquidity traders and market makers who learn from their trades. Purchases suggest good news and sales bad news. The article argues that this decomposition becomes insufficient when execution strategies strategically choose whether to supply or demand liquidity and when liquidity providers face hard inventory controls.

A large investor can be uninformed about asset value but informed about its own future execution needs. An extended one-sided program can impose losses or binding inventory constraints on liquidity suppliers. From the supplier's short horizon, learning about that program is valuable information. Conversely, a fundamentally informed investor can work a passive order patiently and avoid revealing its intent by crossing the spread.

Latency adds another information dimension. Receiving the same public event sooner can temporarily create a private advantage. Fundamental information, order-flow information and relative observation speed are therefore different state variables. A model that labels all of them with one binary informed/uninformed indicator can confound distinct sources of adverse selection.

The paper does not provide a structural equation disentangling those states, nor does it quantify how much price discovery each explains. Its proposed research direction is to connect inventory, information and participation decisions in one framework. In particular, replacing risk-neutral competitive market making with an algorithm having binding position limits changes the supply of liquidity during stress.

Market quality also has more than one dimension. Narrow average spreads and efficient prices can coexist with episodic withdrawal of liquidity. Cross-market arbitrage may align prices in ordinary conditions while transmitting a shock or a common risk-limit response. These are mechanisms and research hypotheses in the article, not estimated systemic-risk coefficients.

## 3. Reconstructing the parent-order execution experiment

### Sample and unit of observation

Section 3.2 and Table 2 use execution records from Investment Technology Group's standard VWAP algorithm during **2013**. The sample includes buy-side institutional parent orders of at least **100 shares**, with no parent limit price, completely executed within the trading day. These are market instructions to the broker, but the broker can fulfill them through passive, aggressive or within-spread child executions.

This sample restriction is important. “Parent market order” does not mean every child is a market order. Fully executed intraday orders exclude partially filled or canceled parents, so the results need not describe the behavior or cost of all client intentions. The article discloses that the author chaired ITG's board; the execution records and technical analysis were supplied by ITG personnel.

Parent identifiers link the child fills. There are **243,772 parents** and **13,468,847 executions**, yielding the count-weighted ratio

$$
\frac{13{,}468{,}847}{243{,}772}\approx55.25
$$

child executions per parent. The prose prints 55.325; the counts give approximately 55.25. This ratio is an average count, distinct from the dollar-weighted aggressiveness shares below.

### Classification rule

For a parent buy, a fill at or below the contemporaneous bid is passive, at or above the ask is aggressive, and strictly inside the spread is assigned to the “midpoint” category. For a parent sale, the sides reverse: at or above the ask is passive, at or below the bid is aggressive, and inside the spread is in the third category. Despite its label, “midpoint” includes prices within the spread, not exclusively the exact arithmetic midpoint.

Locked quotes are eliminated from fill-aggressiveness and trade-statistic calculations. The article does not specify every stale-quote, crossed-market, routing timestamp or synchronization rule. To implement the classification, a researcher must freeze the quote source and observation time convention; otherwise a fill can change categories because of feed latency rather than execution behavior.

Let $d_j$ be the dollar value of eligible child execution $j$, and $I_{jk}$ indicate its category. The reported share for category $k$ within a bucket is reconstructed as

$$
A_k=\frac{\sum_jd_j I_{jk}}{\sum_jd_j}.
$$

This is the natural dollar-weighted aggregation described by the source. It is not the fraction of parent orders that use a category, or necessarily the fraction of child executions by count. The article says share-weighted averages are similar, but does not supply them.

Parents are bucketed in two ways. Participation rate measures the order's share of market volume over its execution interval; parent size measures the order relative to the full day's volume. These differ for a parent that trades quickly during part of the day. The source identifies the concepts but does not fully document the interval endpoints, market-coverage denominator, exact boundary handling or the aggregation of variable participation rates over an order's life.

### Participation-rate results

| Participation bucket | Parents | Child executions | Passive value share | Aggressive value share | Within-spread value share |
|---|---:|---:|---:|---:|---:|
| 0–1% | 144,121 | 4,112,103 | 77.18% | 7.26% | 15.57% |
| 1–5% | 69,341 | 4,921,553 | 68.27% | 7.93% | 23.79% |
| 5–10% | 16,161 | 2,268,437 | 61.22% | 12.53% | 26.25% |
| 10–25% | 10,047 | 1,785,376 | 52.18% | 23.87% | 23.95% |
| 25–50% | 2,627 | 341,559 | 32.90% | 47.93% | 19.10% |
| 50–100% | 1,475 | 39,819 | 12.42% | 68.80% | 18.79% |
| Total | 243,772 | 13,468,847 | 65.53% | 12.57% | 21.90% |

Slowly participating orders are overwhelmingly passive or within-spread. Aggressive execution becomes much more common at high participation. This is consistent with urgency reducing the ability to wait for fills, but the table is descriptive: participation is chosen, not randomized. Order difficulty, stock liquidity, client instructions and market conditions can jointly determine both participation and aggressiveness.

The dominant total result uses **65.53%**, as printed in the table, rather than the prose's 65.3%. The rounded 25–50% row adds to 99.93%, so those entries should not be force-normalized as if an exact underlying dataset were available. The source provides no standard errors or confidence intervals for these shares.

### Order-size results and arithmetic qualifications

For parents below 1% of full-day volume, the table contains **210,557 parents**, **6,254,707 executions**, and value shares **71.90% passive, 10.62% aggressive and 17.48% within-spread**. In the 5–10% size bucket, the corresponding shares are **57.95%, 16.49% and 25.56%**. The >50% bucket contains only **13 parents** and **994 executions**, with **89.87% aggressive** value share. This extreme category is too small to support a broad universal conclusion about very large institutional programs.

Two percentages in the prose are inconsistent with the table counts. Thirteen parents out of 243,772 are approximately **0.00533%**, not 0.0005%. Parents in the three buckets above 10% sum to $1,448+137+13=1,598$, approximately **0.656%** of the sample, not 0.06%. These corrections preserve the conclusion that such parents are rare while avoiding an order-of-magnitude exaggeration.

The 10–25% size row's reported category shares sum to **98.59%**, leaving a **1.41-percentage-point** gap. The source gives no explanation that would justify assigning that residual to one category. A numerical reproduction should flag the row rather than silently repair it.

### What the evidence says about signed trades

If a parent buy fills passively at the bid, the initiating counterparty is selling. A data vendor's aggressor flag correctly labels that child execution as a sell even though the institutional intention being fulfilled is a buy. There is no trade-sign-classification error in that example; there is an error in interpreting aggressor sign as the parent decision's sign.

The aggregate passive-plus-within-spread share is **87.43% by dollar value**. This establishes the prevalence of non-aggressive execution in the sample. It does not establish that all within-spread fills are oppositely signed, that 87.43% of count-weighted trades reverse the parent sign, or that every passive parent is informed. The paper's rhetorical “up to 87%” interpretation requires these distinctions when turning its argument into a measurement model.

## 4. Reconstructing the trade-imbalance illustration

Figure 1 examines all Nasdaq-executed continuous-market trades in three stocks during **October 2010**, excluding opening, closing and intraday crosses. The Nasdaq HFT dataset contains 120 selected stocks. The authors divide the universe into capitalization terciles and select the largest stock in each: Apple, Intuitive Surgical (ISRG), and NxStage Medical (NXTM). Apple's ticker is AAPL; the prose prints APPL.

The dataset supplies aggressor-side flags, avoiding a need to infer trade direction from a Lee–Ready rule in this illustration. Observations are aggregated into **ten-minute intervals**. The horizontal variable is the absolute signed-trade imbalance

$$
I_b=\left|\frac{B_b-S_b}{B_b+S_b}\right|.
$$

It lies between zero and one when both inputs are nonnegative. The caption labels $B_b$ and $S_b$ as buys and sells but does not explicitly settle whether they are counts, shares or dollar volumes. Given the paper's emphasis on signed trades, counts are a plausible reconstruction, but an exact replication must confirm the underlying code rather than assume that all definitions are equivalent.

The vertical variable is described as the log of the high–low price measure in each interval. The displayed axis is labeled “Hi_lo,” and the paper does not spell out a formula resolving whether it means a log price ratio, a difference of log prices, or a transformed absolute range and its scaling. These distinctions affect units, particularly across stocks with very different prices. The exact number of nonempty intervals, treatment of zero-trade intervals and zero ranges, session boundaries and scaling are also not given.

The plotted clouds show no clear increasing relationship between absolute aggressor imbalance and the within-interval range. The paper interprets this as consistent with aggressiveness reflecting willingness to pay the spread rather than fundamental information. It supplies no regression slope, significance test, uncertainty band, control variables or out-of-sample validation.

This illustration therefore cannot establish a general zero relation between signed order flow and price changes. It concerns an unsigned range and an absolute imbalance on one venue, three selected stocks and one month. Directional price response, conditional nonlinear dependence and cross-venue information could still be present. The supported lesson is to question an assumed interpretation and specify the target carefully, not to discard signed-flow variables categorically.

## 5. Market-data quality and time horizons

The article distinguishes missing observations, misleading chronology and changing economic definitions. All three can affect research even when a data file appears large and detailed.

Historically, odd lots were omitted from the consolidated tape. The cited research finds that odd lots are about **20% of trades on average** and **50% or more for some stocks**, and may have meaningful information content. Their omission is therefore not necessarily random. Historical datasets cannot be made complete simply by applying a better classifier to their surviving round-lot observations.

Trade reports from different venues can arrive at different latencies. A receipt timestamp is not necessarily an execution timestamp, and coarse timestamps can reorder quotes and trades. The cited comparison between second-stamped monthly TAQ and millisecond-stamped daily TAQ reports material measurement differences: effective spreads **54% larger**, quoted spreads **47% smaller**, negative quoted spreads **37 times more frequent**, outside-NBBO trades **eight times more frequent**, and measured price impact **109% larger** in the coarser dataset. These are reported findings from another study, not estimates newly produced in this article.

Higher timestamp precision reduces one source of error but does not align all traders' information sets. The trader using a slower feed may legitimately act on a quote that was obsolete from the perspective of a co-located observer. A strategy evaluation needs to reconstruct what the strategy could have known, not just the fastest possible ex post market state.

Quote cancellation and replacement also affect the meaning of the midpoint. It can be a useful reference price while being a poor description of executable liquidity for a given order size and access latency. The paper highlights quote-volatility decomposition over sliding horizons, including intervals as short as **50 milliseconds**, and questions whether conventional fixed horizons remain appropriate for realized-spread measures.

A five-minute realized spread need not approximate a fast market maker's gain from an individual trade when the position is hedged or closed across correlated instruments much sooner. Negative estimates do not mechanically prove that market making loses money; nor does changing the horizon guarantee a correct profit measure. Fees, rebates, hedge transactions, inventory and selection into executions are omitted from a simple trade-to-future-midpoint calculation.

The same concern applies to labels such as permanent and transitory impact. An effect may be persistent at a millisecond horizon and transient over a day. The paper asks researchers to state the economic holding or response horizon rather than treating these terms as universal categories. It discusses volume time and event-sequence methods as potentially useful tools, but supplies no single optimal clock or sampling estimator.

## 6. Research design and policy implications

The article proposes examining order additions, cancellations, revisions, sequences and cross-market activity rather than only isolated completed trades. Parent–child linkage is especially valuable because it reveals the difference between an investment decision and its execution. Without linkage, a researcher should model that latent structure or describe its absence as an identification limitation.

A reproducible follow-up to the ITG evidence would require parent IDs, intended side and quantity, arrival and completion times, child fills, quote histories from the relevant feeds, venue and fee information, and comparable market-volume denominators. It should separate count-, share- and dollar-weighted statistics and retain unfilled parents for any claim about execution quality generally. These are implications of the evidence, not extra data supplied by the source.

For causal HFT analysis, defining treatment by “fast versus slow” alone is insufficient. A speed upgrade can change market-making behavior, arbitrage, queue competition and routing simultaneously. Outcomes should distinguish spreads, depth, fill probability, price discovery, tail liquidity and costs for different clienteles. The review does not choose an econometric instrument or identify one preferred natural experiment; it motivates why those design choices matter.

Its policy discussion focuses on how fragmented venues are linked and how heterogeneous traders are treated. Matching another venue's best displayed price can promote competition but reduce incentives to establish that price, and can make routing predictable. Requiring execution at the venue that sets the price can strengthen display incentives while concentrating order flow. These are tradeoffs in the historical discussion, not a finding that one rule is universally optimal.

Fairness is presented as a separate, difficult-to-measure objective. Differential access, complex order types and data sales can affect participation and trust even if narrow average trading-cost metrics improve. O’Hara argues for research connecting these mechanisms to participation, risk sharing and capital formation. The paper does not provide a scalar fairness index, an estimated welfare function or an approved regulatory design.

## Main limitations and supported takeaway

The central execution evidence comes from one broker's VWAP algorithm, one year, institutional clients and fully completed parents. Selection, proprietary routing logic and omitted order characteristics prevent it from identifying population-wide causal effects. The three-stock imbalance illustration is deliberately narrow and visually assessed. Several table/prose arithmetic inconsistencies and missing implementation definitions constrain exact numerical replication.

The narrative also includes a mistaken date for the Flash Crash and historical venue, regulatory and product descriptions that should not be carried forward as current facts. Its discussion of that episode is used to illustrate how parent intentions and execution styles can differ; this PDF does not independently resolve the event's entire causal history.

What survives these limitations is a precise measurement warning: an execution, its aggressor flag, a parent investment decision, a displayed quote and a trader's available information are different objects. Speed, fragmentation and strategic algorithms widen the gaps between them. Research that makes these objects explicit can use microstructure data more effectively; research that substitutes one for another can misread both information and liquidity even with an enormous number of observations.

# ‘Real’ Trading Volume

Charles Crow and Simon Emrich. Morgan Stanley Quantitative and Derivative Strategies, *Quant Times*, April 11, 2012. [Supplied PDF](../../Finance/TradingVolume_CrowEmrich_2012.pdf), eight pages. The cover precedes six numbered analytical pages and one disclosure page; references below use the printed analytical page numbers. All pages and Exhibits 1–8 were inspected. This is a contemporaneous practitioner argument supported by descriptive data, not a peer-reviewed causal study or a tested execution algorithm.

## Why this matters

An execution schedule expressed as a percentage of average daily volume implicitly treats reported turnover as a measure of available liquidity. Crow and Emrich question that interpretation. A share passing through several intermediaries generates several trades even if the ultimate transfer between investors has not increased. Total volume can therefore rise while finding a durable counterparty for a large institutional position becomes more difficult. A small quoted spread and low realized volatility do not resolve this distinction: they describe the cost or variability of small transactions, not necessarily the capacity to absorb a persistent parent order.

The note's contribution is a holdings-based proxy for the part of turnover attributable to changes in longer-horizon investors' positions. It compares quarterly position changes with consolidated share volume, separately for purchases and sales, and interprets the difference between gross exchange activity and these position changes as evidence about intermediation. The central reported result is that institutional purchases and sales together represented 47% of volume in 2001–2006 but 29% in 2008–2011. That is an 18-percentage-point decline, or approximately 38.3% relative to the earlier figure. The paper's “around 40%” characterization refers to this relative change.

The distinction is useful for capacity analysis even if the proposed causal explanation remains unproven. It asks whether an order is small relative to durable risk transfer or merely small relative to repeated handling of the same risk. The statistic is a slow ownership-flow diagnostic, however. Quarterly reporting cannot locate an available counterparty at a particular minute, and the study does not establish that a strategy conditioned on the statistic improves implementation shortfall.

## The ownership evidence and its different denominators

The argument starts with a shift from direct household equity ownership toward institutionally managed portfolios. Exhibit 1 uses Federal Reserve corporate-equity ownership categories. At the time of the note, households and nonprofit organizations hold 37% of approximately \$22 trillion of corporate equity, down from about 50% around the turn of the century. The authors stress that this category includes endowments, foundations, and onshore hedge funds. It is therefore not a clean measure of households making their own stock-selection decisions.

Exhibit 2 uses LionShares and the December 31, 2011 filings to examine S&P 1500 constituents. Average reported institutional long ownership is just over 90% of free float. The figure displays individual companies against log market capitalization and a moving average over 50 stocks. This is not the same denominator or universe as the corporate-equity ownership series. Values above 100% are possible in reported long holdings: securities lending and short positions can create offsetting claims, and the note's measure does not net long institutional ownership against shorts. The source also states that its reporting data omit some over-the-counter equity exposures, such as total-return swaps.

The principal time-series analysis uses a deliberately simpler large-cap universe: stocks still trading when the analysis was conducted that had belonged to the S&P 500 at some point since December 2001. This selects on survival to the endpoint. The authors acknowledge possible survivorship bias but believe it is not material for their concentration argument; they provide no survivor-versus-full-universe comparison to quantify that judgment. The study consequently does not represent an annually reconstituted, point-in-time S&P 500 panel.

For this large-cap universe, institutional ownership rises from 54% to 81%. The text calls the first endpoint March 2000, while the stated sample and Exhibit 4 start in December 2001. The discrepancy cannot be resolved from the supplied note and should be retained in any reconstruction. Mutual-fund ownership increases from 20% in December 2001 to 39% at the end of 2011; hedge-fund-company ownership increases from 1.8% to 6.1%. Other reported categories change less. The growth in total institutional ownership slows after 2008.

Exhibit 3 supplies related mutual-fund industry evidence from the ICI Factbook. Assets grow substantially while the number of funds is comparatively stable after 2000. The source reports an 85% nominal asset increase from 2002 to 2010 and roughly 30% after adjusting for the increase in equity-market capitalization, proxied by the S&P 500. This supports growth in assets per fund but does not directly measure the number of independently acting trading decision makers. Multiple funds can share a manager; one manager can operate several independent teams.

The data assembly also tries to separate mutual funds from the managers that report aggregate holdings. Pension assets managed in segregated external accounts may appear under investment advisers rather than pension funds. Classification is thus a reporting relationship, not necessarily the identity of the ultimate beneficial owner. The source explains the motivation for a separate mutual-fund category but does not publish a deduplication algorithm linking individual fund reports to manager-level filings. That omission matters because counting both levels would inflate institutional position changes.

## Reconstructing the holdings-change measure

The note gives the calculation in prose rather than as a formal estimator. The following notation makes that calculation explicit without claiming to recover unpublished processing code. Let $H_{ijq}$ be the reported share holding of institution $j$ in stock $i$ at quarter-end $q$, and let $V_{iq}$ be that stock's consolidated share volume during the quarter. Define changes after placing consecutive holdings on a consistent share basis:

$$
\Delta H_{ijq}=H_{ijq}-H_{ij,q-1}.
$$

Aggregate positive and negative changes separately:

$$
B_{iq}=\sum_j\max(\Delta H_{ijq},0),
\qquad
S_{iq}=\sum_j\max(-\Delta H_{ijq},0).
$$

Here both $B$ and $S$ are nonnegative share quantities. The stock-level ratios are $b_{iq}=B_{iq}/V_{iq}$ and $s_{iq}=S_{iq}/V_{iq}$. The authors describe averaging these percentages across stocks. The natural implementation is the arithmetic mean of stock-level ratios, rather than the ratio of total position changes to total volume:

$$
\bar b_q=\frac1{N_q}\sum_i b_{iq},
\qquad
\bar s_q=\frac1{N_q}\sum_i s_{iq}.
$$

These two aggregations need not agree. A volume-weighted mean places greater influence on the most heavily traded stocks. Exact stock eligibility within each quarter, treatment of zero volume, missing reports, and the averaging of quarters into the two reported subperiods are not specified. The note's wording supports an average across stocks, but a replication should state its convention rather than silently choose a ratio of aggregates.

The calculation requires split-adjusted share quantities or another consistent treatment of corporate actions. A stock split changes the reported number of shares without being a purchase; a merger, manager consolidation, account transfer, or reporting reclassification can also change reported holdings without an exchange trade. Conversely, an institution can buy and sell repeatedly within the quarter and finish near its initial holding. The end-to-end change misses that turnover. The source explicitly acknowledges intraperiod rebalancing but does not document the full set of adjustments needed to separate economic trades from accounting changes.

The lower-bound intuition follows from a pathwise inequality. If an institution's adjusted position changes only through signed trades $x_1,\ldots,x_K$, then

$$
\left|\sum_{k=1}^K x_k\right|\le\sum_{k=1}^K|x_k|.
$$

Observed net position change cannot exceed gross trading under those assumptions. This is a bound on that institution's trading, not an unconditional bound on correctly classified market-wide end-investor transactions. It becomes unreliable if position changes contain nontrade transfers, reporting errors, unmatched manager/fund duplicates, or corporate-action effects. It also says nothing about unobserved institutions or short positions. The source's lower-bound language is best understood conditional on clean, comparable holdings data.

The timing is retrospective. A position is measured at quarter-end and subsequently reported. The paper does not build a forecast using actual filing availability dates, amendments, or publication lags. Using quarter-end holdings as if they were known during that quarter would introduce look-ahead bias in a trading application. No present-day reporting rule is needed to see the issue: the economic measurement date and the information-availability date are different objects, and the supplied study does not reconcile them.

## What the volume shares actually show

Exhibit 5 and the accompanying discussion report the following averages:

| Period | Institutional purchases / total volume | Institutional sales / total volume | Sum of the two ratios |
|---|---:|---:|---:|
| 2001–2006 | 27% | 20% | 47% |
| 2008–2011 | 16% | 13% | 29% |

Purchases exceed sales in both periods, consistent with growing institutional ownership. The purchase-minus-sale difference narrows from seven to three percentage points of reported trading volume. The sum falls because both sides decline; it is not only a shift from institutional buying to institutional selling. The transition is concentrated around 2007–2008.

The period overlaps a sharp increase in total trading. Exhibit 6 reports consolidated average daily volume of 4.8 billion shares in 2006 and 8.8 billion in 2008. The 2012 year-to-date figure available for the April note is 6.9 billion shares. These are share counts, not dollar volume, turnover relative to shares outstanding, or risk transferred. Changes in price levels and the mix of securities therefore complicate economic interpretation of the aggregate quantity.

Exhibit 7 normalizes institutional changes by their own total and shows a comparatively stable mixture across institution categories. The authors interpret this as indicating that the fall in institutions' share of overall volume reflects growth in another source of trading, rather than withdrawal by one particular institutional category. Stable composition does not establish that inference by itself. All categories could experience similar increases in unobserved within-quarter turnover, or the denominator could expand while their measured net changes remained stable. The evidence is consistent with greater intermediary activity, but it does not identify individual intermediaries or their trades.

The study itself offers a measurement-based alternative. If institutional strategies rebalance faster, quarterly changes capture a shrinking share of their actual activity. The cited mutual-fund turnover series rises from 47% in 2006 to 64% in 2009, then falls to 53% in 2010, against a stated long-run average since 1974 of 58%. This is not a monotonic rise, but it demonstrates that the mapping from quarterly net change to gross activity need not be stable. No adjustment converts these fund turnover rates into corrected stock-level trading shares.

## Counting transactions versus counting sides

The reported 47% and 29% figures add purchases and sales measured against a single market-volume denominator. A transaction between two observed institutions can contribute once to each side of the numerator but only once to exchange volume. The source recognizes this and develops two stylized interpretations on printed page 5.

If institutional purchases and sales meet directly as far as possible, the number of distinct transactions touching these investors is bounded below by the larger of the two side counts. If purchases and sales instead occur in separate transactions against intermediaries, the relevant count can approach their sum. Thus the source places the earlier share between 27% and 47% and the later share between 16% and 29%. More generally, for well-defined buy and sell transaction sets, their union has size $B+S-C$, where $C$ is the overlap in which both counterparties are observed institutions. Its bounds are $\max(B,S)$ and $B+S$.

This set-counting interpretation is a useful explanation, but the actual inputs are net quarterly changes, not identified transactions. Applying the same bounds to those inputs is therefore illustrative. The note cannot observe the overlap $C$, distinguish direct institution-to-institution trades from intermediary chains, or measure how many times an intermediary passes inventory along. Its preference for the later share being nearer 29% than 16% rests on the rise of small algorithmic trades, not a counterparty-classification estimate.

The bounds also show why “real volume” is not an established additive decomposition of the tape. The residual after subtracting 29% is not a measured 71% high-frequency-trading share. It contains unobserved within-quarter institutional activity, uncovered investors, measurement discrepancies, and intermediation. Describing it entirely as HFT would exceed the evidence.

## Trade-size evidence and the proposed mechanism

Exhibit 8 uses NYSE data. Average trade size declines from more than 1,000 shares in 2003 to around 250 shares by 2011. Block trades, defined as individual prints greater than 10,000 shares, fall from roughly 30% to just above 5% of volume. These are child-trade statistics. Splitting a large parent order into many small executions reduces average print size without reducing the parent order or the amount of risk its owner wants to transfer.

The authors connect this fragmentation to concentrated asset ownership. Larger institutional parent orders meet fewer natural counterparties, so specialized liquidity providers intermediate the imbalance. When their inventory capacity is exhausted before the parent order finishes, they may trade with other intermediaries. More trades can then be required to transfer a given end-investor position. This mechanism explains how gross activity can coexist with difficult execution, but the note estimates neither intermediary inventories nor risk limits.

The discussion describes market-making strategies as typically mean reverting. Persistent one-sided institutional demand can make a position that initially looked like temporary inventory increasingly risky. Flattening sooner transfers that exposure to someone else and adds prints. No stochastic inventory model, objective function, impact curve, or equilibrium is specified. The paper's mechanism should therefore be reproduced as an economic interpretation of the descriptive evidence, not as a solved model whose parameters have been calibrated.

The claim that household-to-institution transfers had largely run their course is similarly a historical interpretation. The ownership charts support slowing growth after 2008; they do not establish a permanent saturation level, and the note supplies no forecast model for subsequent ownership. All claims here concern the information available in April 2012.

## Execution implications and evidential limits

The most operational number is a claimed reduction in the amount that a VWAP-style strategy can execute without undue impact: approximately 4–5% of ADV in the contemporary environment versus 10–15% before 2007. The source supplies no transaction-level sample, impact threshold, stock controls, confidence interval, horizon specification, or estimated response curve supporting that range. It is practitioner guidance, not an estimated universal capacity law. Its decline is also larger than a mechanical 40% reduction across much of the quoted range; the note does not derive one directly from the other.

The recommended response is to allow more flexibility in timing, seek blocks and natural counterparties, and use opportunistic execution. The paper discusses Morgan Stanley venues and algorithms by name. This commercial context matters: the final page identifies the document as a marketing communication prepared by sales/trading personnel, not a product of the research department. The descriptive statistics remain inspectable, but recommendations for proprietary products are not independent evidence of their execution quality.

There is a real tradeoff in waiting for a counterparty. Less urgent execution can lower the cost of demanding immediate liquidity, but it can also increase opportunity cost, noncompletion risk, adverse selection, and exposure to signal decay. The note acknowledges that institutions cannot all wait indefinitely, yet it does not solve this tradeoff quantitatively. There is no backtest, training/validation split, out-of-sample experiment, or comparison of realized net costs between execution policies.

A reconstruction can credibly target the ownership and holdings-change exhibits: obtain the stated universe and historical filings, reconcile reporting entities, align share units, document corporate actions and survivorship, calculate positive and negative changes separately, and match the per-stock averaging. It cannot recover the stated ADV limits or product benefits from the information provided. The paper's durable contribution is the challenge to a simple volume-based capacity denominator. Its strongest numerical evidence concerns historical ownership and net position changes; its explanation of intermediary behavior and recommended execution changes remain hypotheses to test with richer trade and inventory data.

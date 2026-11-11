# All That Glitters: The Effect of Attention and News on the Buying Behavior of Individual and Institutional Investors

Brad M. Barber and Terrance Odean, *The Review of Financial Studies* 21(2), 2008, pp. 785–818; advance publication December 24, 2007. DOI: 10.1093/rfs/hhm079. Source: [All that Glitters- The Effect of Attention and News on Buying Behavior.pdf](../../Finance/All%20that%20Glitters-%20The%20Effect%20of%20Attention%20and%20News%20on%20Buying%20Behavior.pdf). All thirty-four PDF pages were read, including the formal model and proofs on pp. 814–816. Rotated tables and all four figures were checked visually. Journal pagination equals PDF page number plus 784.

## Why this matters

Attention can determine which investments reach an investor's consideration set before preferences determine the final choice. An individual deciding what to buy searches among thousands of securities; deciding what to sell usually involves only a handful already held. Thus an event that makes a stock conspicuous can increase purchases more than sales even if the event is bad news. The distinctive prediction is a buy–sell asymmetry, not merely higher trading volume after news.

The paper tests that prediction with brokerage transactions, a small institutional-manager sample, market data, and news records. Retail investors tend to become net buyers when stocks have unusually high volume, extreme previous-day returns, or news coverage. Institutions exhibit weaker or different patterns. The most distinctive return result is a U-shaped purchase imbalance: both large gains and large losses attract buying, particularly at the large discount brokerage.

The contribution combines a search-based behavioral explanation, direct identification of investor categories from transactions, tests separating attention from short-sale constraints, and a Kyle-style model whose noise-trading intensity depends on attention. It is not a causal experiment or a fully specified profitable attention strategy. The empirical design measures executed order imbalance, while the model explains how attention-sensitive uninformed demand can increase informed traders' expected profits.

For implementation, the useful lesson is to distinguish participation, direction, and execution. High total volume does not imply that a particular group buys rather than sells. Conversely, a positive trade-count imbalance need not imply a positive dollar imbalance. A model of retail demand can fail if it treats buying and selling as symmetric reactions to the same information signal.

## Transaction samples and eligibility

The first dataset comes from a large discount brokerage and begins with 78,000 households having an open account during 1991. Roughly half opened accounts before 1987 and half during 1987–1991. Position records run January 1991–December 1996; transaction records end in November 1996. Of those households, 66,465 held common stocks in at least one month. Common stocks represented roughly 60% of account market value and slightly more than 60% of trades. The study excludes mutual funds, including closed-end funds, ADRs, warrants, and options.

There are 1,082,107 common-stock purchases and 887,594 sales in this sample. Average purchase value is \$11,205 and sale value \$13,707, making aggregate purchase and sale dollars approximately equal at \$12.1 billion and \$12.2 billion despite more buy tickets. The mean household held an average 4.3 stocks worth \$47,334, while the median held 2.61 worth \$16,210. Only 0.29% of positions, or 0.78% when value weighted, were short. These facts support the proposed asymmetry in the search sets for purchases and sales.

The small discount brokerage emphasizes execution quality and may attract more active, sophisticated customers. Its main transaction sample runs January 1996–June 15, 1999. Excluding accounts the broker labels professional leaves 14,667 individual accounts, 214,273 purchases, and 198,541 sales. Mean ticket values are \$55,077 and \$55,999 respectively. The 159 separately identified professionals are too few to produce clear patterns in the authors' separate analysis.

The large retail brokerage sample covers January 1997–June 1999. It contains 665,533 investors in nondiscretionary accounts with at least one common-stock trade. Ownership codes include individual, joint-with-survivorship, and custodial-for-minor accounts. Common-stock transactions comprise 3,974,998 purchases averaging \$15,209 and 3,219,299 sales averaging \$21,169. An advisor-assisted retail brokerage is not interchangeable with a self-directed discount broker, which helps explain differences across the three groups.

The institutional dataset comes from Plexus and covers January 1993–March 1996, with some managers present for only part of the period. There are eighteen momentum, eleven value, and fourteen diversified managers, totaling forty-three. The data include completed trades and decision timestamps, although the main imbalance definition uses executed trades. Institutional tickets are much larger: momentum purchases average about \$886,346, value purchases \$500,949, and diversified purchases \$450,474. The authors describe these institutions as illustrative rather than representative of all professional investors. They do not observe the entire institutional sector or every counterparty to retail orders.

The samples are proprietary and span different periods. A reproduction requires transaction-level buy/sell signs, account or investor classifications, share quantities, execution values, stock identifiers, and holdings for the already-owned-stock tests. The paper does not release an executable join specification, account-selection code, corporate-action handling rules, or all missing-data decisions. Results should be reproduced within each sample's actual calendar, not by assuming a shared panel of investors.

## Attention proxies and daily sorting

The market universe uses CRSP daily data for NYSE, AMEX/ASE, and Nasdaq stocks. For stock $i$ on trading day $t$, abnormal volume is

$$
AV_{it}=\frac{V_{it}}{\overline V_{it}},\qquad
\overline V_{it}=\frac1{252}\sum_{d=t-252}^{t-1}V_{id}.
$$

The text defines $V$ as dollar volume. A reproduction must therefore construct dollar turnover consistently rather than automatically substituting raw share volume. The denominator excludes day $t$. The source does not fully specify eligibility for firms with less than 252 observations or zero denominators; those are unresolved implementation inputs to document.

Each day, rank stocks by contemporaneous $AV$ into ten deciles, then split the highest decile into two 5% groups, denoted 10a and 10b. Measure the investor group's trading in those stocks that same day. Thus the core volume test is descriptive and contemporaneous. It is not a signal known before the start of that trading day. The article reports similar patterns when today's abnormal volume is related to tomorrow's imbalance, but does not print the complete auxiliary results.

For return sorts, rank stocks using the previous trading day's one-day CRSP return. Form deciles and split both tails into 5% groups: 1a, 1b, 10a, and 10b. The outcome is today's imbalance. This lag allows investors to respond after observing the previous day's move and reduces immediate reverse causality from today's own trading to the sorting return. It does not eliminate every omitted-variable or dynamic feedback explanation.

Zero-return ties need special treatment. A large group of zero-return stocks can straddle more than one partition. Before calculating partition imbalances, the authors replace each zero-return stock's purchase count, sale count, purchase dollars, and sale dollars with the corresponding mean over all zero-return stocks that day. This avoids arbitrary imbalance differences across bins created by tie placement. Reproducing the paper by an arbitrary identifier-based rank among zero-return stocks changes its method.

The news feed is Dow Jones News Service, 1994–1999, with ticker symbols identifying firms mentioned in stories. A stock is classified as news if at least one story mentions it that day; otherwise it is no-news, conditional on news coverage actually being available that day. On an average covered day, 91% of CRSP firms have no recorded news. Some dates are missing because of collection and storage problems. A missing feed date must not automatically become a no-news date for every stock.

News is a binary occurrence measure, not sentiment, readership, prominence, or story importance. Routine releases and major events receive the same indicator. Volume may reflect institutional blocks rather than broad retail interest, and extreme returns can arise from liquidity shocks. The research uses their converging patterns as evidence about attention while acknowledging that none directly observes what investors considered.

## The outcome and statistical aggregation

For investor group $g$, partition $p$, and day $t$, sum completed purchases and sales over stocks in the partition. The count imbalance is

$$
BSI_{gpt}=\frac{\sum_{i\in p}N^B_{git}-\sum_{i\in p}N^S_{git}}
{\sum_{i\in p}N^B_{git}+\sum_{i\in p}N^S_{git}}.
$$

Replace counts with execution dollars for the value imbalance. Report these quantities in percentage points, so a raw fraction of 0.295 appears as 29.50. Exclude a day/partition/group observation with fewer than five trades, then average eligible daily imbalances over time. This is an equally weighted time-series mean of daily ratios, not a ratio of all buys and sells pooled across the entire sample. Different partitions can therefore have different numbers of eligible days.

Standard errors use a Newey–West serial-dependence correction applied to each daily imbalance time series. The main text and table captions do not state the lag-bandwidth choice. Exact standard-error reproduction requires that choice; choosing a conventional bandwidth is a reconstruction, not a reported input. Differences between two bin means also require their covariance, so the standard error of a high-minus-low contrast cannot be inferred by treating printed bin standard errors as independent.

Only executed orders enter the outcome. A limit order counts when it executes, not when it is submitted, and the datasets do not distinguish executed limit orders from market orders. Falling prices can execute resting retail buy limits while rising prices execute sell limits. This is a competing contribution to some return-conditioned patterns, especially contemporaneous news comparisons. The distinction between attention at order submission and attention inferred from execution is not identified away.

Every completed trade has a buyer and seller, so aggregate market-wide dollar imbalance is zero. A positive imbalance for an observed category requires offsetting demand elsewhere; it is not a market-wide excess of purchases over sales. Count imbalances need not match dollar imbalances because ticket sizes differ. The original sample's overall purchase-count surplus also means that the relevant attention result concerns the variation across bins, not whether every bin has zero imbalance under a null.

## Main empirical results

Table 1, p. 797, shows the strongest volume pattern for large-discount investors. Their count imbalance rises from $-18.15$ percentage points in the lowest abnormal-volume decile, standard error 0.98, to 29.50 in the highest 5%, standard error 0.49. The corresponding dollar imbalances are $-16.28$ and 17.67. These are large shifts in trading direction, not just more trades on busy days.

The large retail brokerage moves from $-25.26$ to 19.34 in count imbalance, while the small discount brokerage moves from $-20.49$ to 17.31. The relationships are not perfectly monotone in every series: large-retail count imbalance, for example, is 22.25 in group 10a and 19.34 in 10b. The broad slope is the finding; enforcing strict monotonicity would overstate it.

Institutions show a different volume pattern. Value managers' count imbalance falls from 34.57 in the lowest-volume decile to 4.83 in the highest 5%. Momentum managers fall from 14.68 to 6.72. Institutions can remain net buyers in both bins, so “opposite tendency” refers to the slope relative to attention, not necessarily an unconditional negative imbalance or a directly observed one-for-one offset to retail.

Table 2, p. 802, gives the return-sort results. For large-discount investors, count imbalance is 29.38 after the worst 5% of daily returns, falls to 1.82 in decile 8, and rises to 23.98 after the best 5%. Corresponding dollar values are 29.07, $-8.62$, and 11.13. Both tails attract retail purchases, which is inconsistent with explaining the whole pattern as either pure momentum chasing or pure contrarianism.

The large retail brokerage also has a two-tail count pattern, but its best-return-tail dollar imbalance is $-7.93$. The small discount broker's strongest response is to losers; its highest-return-tail count imbalance is only 3.80 and its dollar imbalance is $-3.59$. Thus the pronounced U shape is not equally strong under every broker and weighting convention.

Institutional style predicts direction. Momentum managers have count imbalance $-21.03$ after the worst 5% and 21.50 after the best 5%; value managers have 17.26 and $-17.32$. A professional buying a winner or loser may simply be implementing a style criterion. The contrast is that no one institutional style displays the same strong buying response at both extremes seen for large-discount retail customers.

Table 3, p. 804, compares news and no-news days. Large-discount count imbalance is 9.35 with news versus 2.70 without, with standard errors 0.72 and 0.43. Large-retail values are 16.17 versus $-1.84$, while small-discount values are 6.76 versus $-0.66$. Dollar imbalances qualify the interpretation: large-discount news-day imbalance is only 0.07, and large-retail news-day dollar imbalance remains negative at $-2.36$, though both exceed their no-news values.

Conditional on a positive, negative, or zero same-day return, retail count imbalances are generally higher with news than without. Negative-return days show stronger net buying than positive-return days. The authors discuss both disposition effects and differential limit-order execution as possible contributors. The news comparison measures an association with recorded coverage; it is not an estimate of the causal effect of publishing an additional story.

## Joint sorts and alternative explanations

The joint analysis independently sorts abnormal volume and previous-day returns into bottom 30%, middle 40%, and top 30% groups, then splits each of the nine intersections by news status. It uses count imbalances. Figure 3 shows higher buying with volume within each return bin. The large-discount sample retains a two-tail return pattern within volume strata; the other brokers have weaker winner responses. Volume is the most consistent of the three indicators, followed by returns and then the crude news measure.

Size tests retain the original all-stock volume and return breakpoints, then subdivide by market capitalization. Monthly NYSE market-equity cutoffs define small stocks at or below the 30th percentile, middle stocks above the 30th through 70th percentiles, and large stocks above the 70th. These NYSE thresholds apply to stocks from all exchanges. Sorting volume separately within size groups would answer a different question.

The effects are not confined to small firms. For large stocks at the large discount broker, the count imbalance runs from $-31.89$ in the lowest-volume decile to 28.26 in the top 5%. Following the worst return tail it is 38.73, compared with 7.76 following the best tail. Similar attention-related differences across sizes do not imply equal price impact: retail's share of total demand can differ greatly between small and large firms.

Earnings and dividend announcement windows run from day $t-1$ through $t+2$ around the event date. Earnings dates come from Compustat and dividend dates from CRSP; all dividend types are included. The paper compares announcement windows with other periods and finds qualitatively similar volume and return patterns. Figure 4's top x-axis is mislabeled as prior return although its caption and monotone curve identify the volume sort; the bottom panel is the return sort. This matters when reproducing figures from extracted labels alone.

The principal short-sale-constraint alternative is that attention produces disagreement, bullish individuals can buy, and bearish nonowners cannot sell. To distinguish this from search asymmetry, Table 5 restricts each investor's trades to stocks already owned. These investors can sell without shorting. Their imbalances remain more purchase-oriented on high-attention days, although nearly all levels are negative because selling existing holdings is much more common than adding to them.

For large-discount investors in already-owned stocks, count imbalance rises from $-54.22$ in the lowest-volume decile to $-24.97$ in the highest 5%. News days show $-40.91$ compared with $-45.05$ without news. Those differences support a role for attention beyond inability to short a new stock. The prior-return pattern is asymmetric: loss-day buying remains strong, while winner buying does not robustly rise across samples, consistent with the disposition effect. The small-discount holdings test ends in December 1998 according to Table 5, earlier than its main transaction sample. Its shorter holdings window should be preserved.

An additional unprinted check compares stocks with and without exchange-traded options. Similar patterns are reported, weakening an explanation relying entirely on short-sale constraints. Options availability is not a randomized treatment and does not prove all retail investors can or will use options. These checks narrow the competing explanation without fully identifying a structural attention effect.

## The appendix model: assumptions and equilibrium

There are dates 0 through 3, trading at 1 and 2, a zero-return riskless asset, and a risky terminal payoff $v=y_1+y_2$. Independent innovations satisfy $y_t\sim N(0,\phi^2)$. Before trading at date $t$, a risk-neutral insider learns $y_t$; it becomes public at $t+1$. Thus $y_1$ is public when date-2 trading occurs. The market maker is competitive and risk neutral, observes aggregate order flow, and prices at its conditional expected terminal value. The initial price is normalized to zero, and final price is $y_1+y_2$.

Noise traders submit Gaussian buy quantity $b_t$ and sell quantity $s_t$, with means and variances specified separately. At date 2,

$$
\widehat b_2=m(A+y_1^2),\qquad
\widehat s_2=m\bigl(A+\kappa y_1^2+(1-\kappa)\phi^2\bigr),
$$

where $A,m,\psi>0$ and $0\leq\kappa<1$. Conditional variances are $\widehat b_2/\psi^2$ and $\widehat s_2/\psi^2$. Date-1 means both equal $m(A+\phi^2)$ with the analogous variance rule. Attention is $y_1^2$, so both positive and negative large news shocks increase purchases. Selling responds more weakly because its attention coefficient is $\kappa$.

The equilibrium calculations use conditionally Gaussian, independent buy/sell noise and independence from the new private signal. In particular, the variance of net noise demand is the sum of the two variances. The source's prose gives the marginals and its proof imposes this covariance structure; correlated order components would require a modified solution.

Define conditional net noise mean and total variance by

$$
n=m(1-\kappa)(y_1^2-\phi^2),\qquad
Q=\frac{m}{\psi^2}\left[2A+(1+\kappa)y_1^2+(1-\kappa)\phi^2\right].
$$

Unconditional buying and selling means are equal because $E[y_1^2]=\phi^2$. Therefore the model's positive conditional imbalance in high-attention states does not require unconditional net noise buying.

Let informed demand be $x_2=\alpha+\beta y_2$, total demand $d_2=x_2+b_2-s_2$, and price $P_2=\mu+\lambda d_2$. Lemma 1 gives

$$
\alpha=0,\quad \beta=\frac{\sqrt Q}{\phi},\quad
\lambda=\frac{\phi}{2\sqrt Q},\quad \mu=y_1-\lambda n.
$$

These compact equations are equivalent to the article's equations (6)–(9). The insider's first-order condition gives $\beta=1/(2\lambda)$. Gaussian conditional expectation gives $\lambda=\beta\phi^2/(\beta^2\phi^2+Q)$. Equating them yields $\beta^2\phi^2=Q$ and the positive trading-intensity solution above. The intercept removes predictable net noise demand, so the market maker does not mechanically mistake the mean attention effect for information.

Increased attention raises $Q$, lowers price impact per unit order flow, and lets the insider trade more aggressively. Expected informed profit, equal to aggregate expected noise-trader loss because the market maker breaks even, is

$$
E[x_2(v-P_2)\mid y_1]
=\frac{\phi\sqrt Q}{2}
=\frac{\phi}{2\psi}\sqrt{m\left[2A+(1+\kappa)y_1^2+(1-\kappa)\phi^2\right]}.
$$

Its derivative with respect to $y_1^2$ is positive. This is an aggregate expected-loss result, not a theorem that every attention-driven trade loses or that loss per share necessarily rises. It also relies on the chosen variance–mean relationship. The model assumes attention-driven buying rather than deriving it from an optimized information-acquisition problem; its role is to demonstrate consequences and consistency with the observed shapes.

## Simulation and implementation limits

The paper simulates 100,000 independent realizations with $\phi=A=m=\psi=2$ and $\kappa=0.5$. A reconstruction draws $y_1,y_2$, draws date-1 buy and sell noise with their common means and variances, solves the first trading-round Kyle equilibrium, then draws date-2 noise conditional on $y_1$ and uses the formulas above. Sort realizations by date-1 price change and date-2 volume, split the same tails as in the empirical tests, and calculate noise-trader buy–sell imbalances in the partitions. Figure 1 reproduces a rising volume relation and a U-shaped relation to the prior price change.

The price normalization $P_0=0$ means “period-1 return” in this simulation must be understood as a price change, not a conventional percentage return dividing by $P_0$. The source gives no random seed and does not fully specify the exchange-volume convention when informed and market-maker trades are included, nor every aggregation choice within simulated partitions. Those details should be declared in a reconstruction rather than presented as recovered author code. Gaussian gross quantities can be negative; the authors report none in their chosen simulation. Truncating negative draws changes the model's distribution and should not be done silently.

No raw brokerage data, executable code, transaction-cost strategy, or fully reported auxiliary price-impact study accompanies the supplied article. Its strongest conclusion is about which stocks retail investors choose to buy relative to sell. The broad pattern survives several alternative partitions and tests of selling constraints, but proxy endogeneity, selection into brokerages, unobserved order types, and different sample calendars remain. A useful application would model the consideration set and executed demand separately, then test any return forecast on a distinct, implementable information timeline. The observed attention pattern alone is not a license to trade against every conspicuous stock.

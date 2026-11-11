# Dimensional Analysis, Leverage Neutrality, and Market Microstructure Invariance

Albert S. Kyle and Anna A. Obizhaeva. Working-paper draft dated July 30, 2017; first draft September 17, 2015.

Source: [MarketImpact_Kyle_Obizhaeva_2017.pdf](../../Finance/MarketImpact_Kyle_Obizhaeva_2017.pdf), 31 PDF pages, including title page and references. Numbered page $p$ appears on PDF page $p+1$. This note covers the full draft and its empirical figures and tables. It concerns this dimensional-analysis paper, not the authors’ separate *Market Microstructure Invariance: Empirical Hypotheses* or dynamic-equilibrium paper.

## Why this matters and the precise contribution

The paper develops a restricted family of transaction-cost models whose normalization respects currency units, share units, time units, and economically neutral changes in leverage. Its central implication is that percentage trading costs can be written as an asset-specific illiquidity scale times a universal function of normalized bet size. Under an additional invariance hypothesis, the scale is proportional to the cube root of return variance divided by dollar trading volume.

This is useful when fitting costs across stocks: a model should not change its economic prediction merely because a stock splits, the quotation currency changes, or the time unit changes. More substantively, adding cash to the same risky claim should not alter the cost of transferring that claim’s risk in the paper’s frictionless-cash benchmark. These restrictions substantially reduce the number of free arguments a cost model needs.

The contribution is a derivation and a method for extending that derivation to omitted frictions. It is not a proof that dimensional consistency alone selects the square-root law, that every market has an identical dollar cost per institutional decision, or that a universal optimal execution schedule follows. The authors separate three ingredients: dimensional analysis, leverage neutrality, and empirical invariance of two constants. The last two are economic restrictions, not identities.

The original evidence consists of 2015 Russian and U.S. equity panels testing spread and transaction-count exponents. Daily pooled spread slopes are close to the predicted value. Transaction-count slopes are economically nearby but statistically far from the exact restriction, and individual-stock slopes often differ substantially from pooled slopes. The paper’s policy and execution extensions are proposed scaling benchmarks; their functional forms and proportionality constants are not estimated here.

## Variables, units, and the first reduction

Suppress stock-date subscripts initially. A **bet** is a decision to buy or sell an institutional quantity based on a common informational or hedging motive. It can be implemented through many orders and trades. Let $Q$ be signed shares in the bet, $P$ price, $V$ share volume per unit time, $\sigma^2$ return variance per unit time, and $G\ge0$ expected impact cost divided by the unsigned traded value $P|Q|$. The unconditional expected dollar cost of a bet is

$$
C=E[G P|\widetilde Q|].
$$

Here the tilde indicates a random bet drawn from the population; a specific proposed trade has a chosen $Q$. The model starts from the **complete-list assumption**

$$
G=g(Q,P,V,\sigma^2,C).
$$

The same function $g$ applies across assets and dates. If important variables such as urgency, ticks, funding restrictions, or order-book state are missing, this initial specification is not complete and its implications need modification.

Using currency, shares, and days as the three base units,

$$
[P]=\frac{\mathrm{currency}}{\mathrm{share}},\quad [Q]=\mathrm{share},\quad [V]=\frac{\mathrm{share}}{\mathrm{day}},\quad [\sigma^2]=\frac1{\mathrm{day}},\quad [C]=\mathrm{currency},\quad [G]=1.
$$

Thus volatility has units $\mathrm{day}^{-1/2}$, not inverse days. The variance-rate convention assumes the relevant diffusion-like time scaling; it is not a general result for any irregularly sampled price process. Daily volume and annualized variance must be put on a consistent time basis before applying the formulas.

With five dimensional inputs and three independent units, the Buckingham-$\pi$ argument leaves two independent dimensionless combinations. The authors choose, in equation (4),

$$
L=\left(\frac{m^2PV}{\sigma^2C}\right)^{1/3},\qquad Z=\frac{PQ}{CL},
$$

where $m^2$ is a dimensionless normalization constant. It follows that $G=g(L,Z)$. The argument is that $P,Q,\sigma^2$ span the original units, while $L,Z$ supply the remaining independent information. A dimensionless outcome cannot depend on the numerical values of the three dimensional coordinates when units can be changed freely. This establishes a two-variable representation, not yet the final one-variable function.

The cube root is strategically chosen to make leverage transformations simple. It is not forced by dimensional consistency alone. The quantities called “dimensionless” retain their definition only if $C$ is transformed with the currency unit. Dropping $C$ from an empirical index is permissible when its constant contribution is absorbed by an intercept, but that index’s numerical level then depends on the units chosen.

## Leverage neutrality and proof of the cost representation

Imagine adding cash worth $P(A-1)$ to each share, where $A>0$. The new bundle has price $AP$ and the same dollar risk per original share. Under the paper’s benchmark, exchanging cash is costless, so transferring $Q$ bundles has the same dollar economic cost as transferring $Q$ original risky shares. The transformation is

$$
P\mapsto AP,\quad \sigma\mapsto\sigma/A,\quad Q\mapsto Q,\quad V\mapsto V,\quad C\mapsto C.
$$

Consequently $L\mapsto AL$, $Z\mapsto Z$, and percentage cost $G\mapsto G/A$. The required functional equation is

$$
g(AL,Z)=A^{-1}g(L,Z).
$$

Set $A=1/L$ and define $f(Z)=g(1,Z)$. Then

$$
G=\frac1L f(Z)=\left(\frac{\sigma^2C}{m^2PV}\right)^{1/3}f\!\left[\frac{PQ}{C}\left(\frac{\sigma^2C}{m^2PV}\right)^{1/3}\right].
$$

This is Proposition 2 and equations (7)–(8). The derivation fixes how liquidity scales the cost function but leaves the shape of $f$ unrestricted. Buy/sell symmetry would further require $f(Z)=f(-Z)$; dimensional analysis itself does not impose it. In the paper’s power examples, the nonnegative cost uses $|Z|$.

Equivalent interpretations are changing riskless corporate leverage through a cash distribution, or changing a cash-equivalent margin component without altering the risky claim. These are idealized neutrality statements. A real funding constraint can alter trading volume, volatility, feasible positions, counterparty risk, or forced-liquidation behavior; the authors expressly acknowledge that richer models can have such equilibrium effects. Neutrality should not be turned into a claim that actual margin regulation has no market consequences.

A useful mechanical check is $A=2$: the bundle doubles in price, its percentage volatility halves, its liquidity index doubles, and percentage impact halves. The traded dollar amount doubles, leaving dollar trading cost unchanged. A model passing a stock-split test but failing this cash-bundle test satisfies a weaker restriction than the paper imposes.

## Bet size, business time, and normalization

Choose $m$ so that $E|\widetilde Z|=1$. Then equations (10)–(13) imply

$$
Z=\frac{Q}{E|\widetilde Q|},\qquad E[P|\widetilde Q|]=CL,\qquad \gamma=\frac{V}{E|\widetilde Q|}=\frac{\sigma^2L^2}{m^2}.
$$

Here $\gamma$ is bets per calendar day. The volume identity implicitly uses the same economic counting convention for share volume and bets. If intermediation generates several reported trades per underlying bet, reported trade count is not automatically $\gamma$.

The index $1/L$ has two interpretations. First,

$$
\frac1L=\frac{E[GP|\widetilde Q|]}{E[P|\widetilde Q|]},
$$

so it is a value-weighted expected percentage cost, not necessarily the simple mean $E[G]$. Second,

$$
\frac1L=\frac{\sigma}{m\sqrt\gamma},
$$

so illiquidity scales with return volatility per bet, or per unit of business time. Holding volatility fixed, higher $L$ increases mean dollar bet size proportionally and bet arrival rate quadratically. More trading activity is therefore apportioned between larger bets and a still faster arrival rate.

The paper provides an optional additional normalization based on all return variance being generated by martingale impact of bets. Under $E[G^2]=\sigma^2/\gamma$, one obtains $m^2=E[f(\widetilde Z)^2]$. Since the cost definition also gives $E[f(\widetilde Z)|\widetilde Z|]=1$, a power cost $f(Z)=\bar\lambda|Z|^\omega$ implies

$$
\bar\lambda=\frac1{E|\widetilde Z|^{1+\omega}},\qquad m^2=\frac{E|\widetilde Z|^{2\omega}}{\{E|\widetilde Z|^{1+\omega}\}^2}.
$$

Absolute values are essential for noninteger powers of signed bet sizes; the displayed source formula suppresses them in places. For linear impact, $\omega=1$,

$$
m=\frac{E|\widetilde Q|}{\sqrt{E[\widetilde Q^2]}}\le1.
$$

The inequality is a direct consequence of Cauchy–Schwarz. The optional impact-variance condition is stronger than dimensional analysis and requires an interpretation of price innovations and cost magnitudes consistent with the assumed martingale mechanism. It should not be imposed on an arbitrary execution-cost dataset containing spread, fees, adverse selection, and independent public-news volatility.

## What invariance adds and what it does not

Assumption 5 makes $C$ and $m^2$ constant across securities and time. Equal $C$ is motivated by allocation of research effort: resources devoted to generating bets may move until expected economic costs are comparable. A common bet-size distribution supports a common $m$. Neither assertion follows from units or leverage neutrality.

Across countries, the source allows $C$ to vary with local productivity-adjusted wages. If $w$ is a financial professional’s nominal wage per day and $b$ is bets processed per day, it suggests $C=cw/b$ for an invariant dimensionless $c$. Accordingly, its country-specific regressions do not test a literal identical currency cost worldwide. Inflation, currency conversion, and productivity normalization matter for levels.

The draft cites an external preliminary calibration from portfolio-transition orders of $C\approx\$2,000$ and $m^2\approx0.25$. It does not reestimate those constants using its 2015 quote panels. In dollar units, these numbers give equation (17):

$$
\frac1L=20\left(\frac{\sigma^2\,(1\ \mathrm{USD})}{PV}\right)^{1/3}.
$$

The explicit currency unit keeps the expression dimensionless. As a calculated illustration using the source’s representative price \$40, volume one million shares/day, and daily volatility 2%, the calibration gives $L=232.08$, value-weighted cost $1/L=0.004309$ or 43.09 basis points, mean dollar bet about \$464,159, and $\gamma\approx86.18$ bets/day. These are implications of the stated calibration, not observed outcomes or a prediction that every individual trade costs 43 basis points. The cost of a chosen $Q$ still requires $f(Z)$.

With $f(Z)=\bar\lambda|Z|^\omega$, Proposition 4 gives three important cases:

| Cost shape | Percentage-cost scaling, with constant factors suppressed |
|---|---|
| Constant proportional component, $\omega=0$ | $G\propto L^{-1}$ |
| Linear in bet size, $\omega=1$ | $G\propto P\lvert Q\rvert/(CL^2)$ |
| Square root, $\omega=1/2$ | $G\propto\sigma\sqrt{\lvert Q\rvert/V}$ |

The square-root case cancels $P$ and $C$ from the variable part. A linear combination of these terms can represent spread plus impact. The derivation does not choose which case is empirically best, determine its coefficient, or establish whether its “impact cost” is terminal price displacement rather than average implementation shortfall. Applying it to data requires a consistent cost definition.

Section VI explains a consequential specification issue. If $C$ is omitted from the initial variable list, the remaining dimensionless signed combination is $Q\sigma^2/V$, and leverage neutrality forces the square-root dependence on its magnitude. The draft’s prose prints an inconsistent product/quotient at this point; $Q\sigma^2/V$ is the dimensionally correct combination. Thus deriving a square-root law from a restricted variable list is conditional on excluding a relevant monetary scale. A dimensional constant cannot simply be omitted because it is empirically constant.

## Reconstructing the empirical experiment

Section V studies contemporaneous stock-day relationships, not forecasts or a trading strategy. Both panels cover January–December 2015 and freeze index membership as of June 15, 2015. A reproduction must use those membership lists rather than present-day constituents or a daily changing universe.

The Russian panel contains 50 RTS Index stocks from Moscow Exchange data supplied by Interfax, with 250 trading days. Each day’s proportional quoted spread is the arithmetic mean of end-of-minute proportional spreads during 10:00–18:50. The market uses a consolidated limit-order book. Tick sizes were adjusted by the exchange, and lot sizes were described as generally small.

The U.S. panel contains 500 S&P 500 stocks from daily TAQ, with 252 trading days. Each day’s spread is the mean of end-of-minute spreads during 9:30–16:00, using best bids and offers across exchanges. The historical market description has a one-cent minimum tick for most stocks and a usual 100-share round lot. These conventions are features of the 2015 experiment, not a statement about current rules.

For both samples the authors construct realized volatility from squared one-minute changes in quote midpoints. To be consistent with their equations, these changes must be expressed as **returns**, yielding a daily return-variance estimate. The prose does not explicitly distinguish log midpoint returns from simple relative changes or give the precise treatment of the first interval, overnight moves, stale quotes, crossed markets, or missing minutes. Summing squared raw price changes without normalization would have the wrong units.

A reasonable implementation is to construct midpoint $M_{jdt}=(A_{jdt}+B_{jdt})/2$, minute proportional spread $(A-B)/M$, and $\widehat\sigma^2_{jd}=\sum_t[\Delta\log M_{jdt}]^2$. This log-return formula is a documented reconstruction choice, not an exact recovered code specification. Aggregate traded value consistently to obtain $D_{jd}=P_{jd}V_{jd}$ and count eligible transactions to obtain $N_{jd}$. The draft does not specify which price enters $PV$, whether dollar turnover is computed trade by trade, treatment of auctions and corrected trades, or all eligibility filters.

Compute the empirical index with constant factors absorbed into intercepts:

$$
L^0_{jd}=\left(\frac{D_{jd}}{\widehat\sigma^2_{jd}}\right)^{1/3}.
$$

Then fit, separately by country,

$$
\log\bar s_{jd}=a+b\log(1/L^0_{jd})+u_{jd},\qquad H_0:b=1,
$$

$$
\log N_{jd}=c+d\log(\widehat\sigma_{jd}L^0_{jd})+v_{jd},\qquad H_0:d=2.
$$

Use positive, finite inputs and record every excluded observation. Estimate unrestricted pooled OLS, a line with the theoretical slope fixed and only intercept estimated, and separate stock-level regressions. The Russian spread experiment also reports a regression using monthly averages. The exact order of monthly averaging and logarithms is not fully documented; a faithful replication must resolve that rather than treating mean-log and log-mean as interchangeable. Standard errors in the main spread results are clustered by trading day; the numerical trade-count standard errors are reported in the same empirical discussion, but a separate detailed covariance implementation is not supplied.

There are 12,426 Russian stock-days, compared with the nominal $50\times250=12,500$. U.S. spread regressions have 124,170 observations, and U.S. transaction-count regressions 121,760, compared with $500\times252=126,000$. The draft does not explain all dropped rows. Figure 4’s caption says 250 days while the U.S. sample text says 252. These are unresolved sample-reconciliation inputs, not grounds to manufacture missing observations.

For broad scale checks, Table 1 reports Russian average daily turnover of RUB 542 million, volatility 189 basis points per square-root day, proportional spread 20 basis points, and 7,328 trades/day. The medians are RUB 73 million, 180 basis points, 13 basis points, and 2,792 trades/day. Table 2 reports U.S. averages of \$205 million, 110 basis points, 4 basis points, and 21,048 trades/day; medians are \$124 million, 90 basis points, 3 basis points, and 15,735 trades/day. The source labels summary statistics “as of June 2015” while using full-year daily observations for the regressions, so the exact aggregation behind every summary-table percentile should be checked against the original data. The U.S. maximum volatility is printed as 4,050 basis points; the draft does not explain this extreme observation.

## Results: approximate scaling versus exact restrictions

The principal unrestricted estimates are:

| Outcome and panel | Intercept (SE) | Slope (SE) | Theoretical slope | $R^2$ |
|---|---:|---:|---:|---:|
| Russian daily spread | 2.093 (0.040) | 0.998 (0.005) | 1 | 0.876 |
| Russian monthly spread | 2.817 (0.164) | 1.078 (0.019) | 1 | 0.923 |
| U.S. daily spread | 1.011 (0.225) | 0.961 (0.024) | 1 | 0.450 |
| Russian daily trade count | −3.085 (0.038) | 2.239 (0.008) | 2 | 0.882 |
| U.S. daily trade count | 1.005 (0.054) | 1.842 (0.011) | 2 | 0.702 |

The daily spread restrictions are not rejected at conventional two-sided 5% levels using the reported standard errors: the calculated deviations are approximately $-0.40$ standard errors for Russia and $-1.63$ for the United States. The Russian monthly slope differs by about $4.11$ standard errors. Thus averaging improves fit while rejecting the exact unit slope.

For trade counts, the deviations from two are about $29.88$ standard errors in Russia and $-14.36$ in the United States. These calculations use the paper’s reported coefficients and standard errors; they are not separate empirical estimates. The authors describe the slopes as broadly consistent economically. That description must not be mistaken for statistical acceptance of exact invariance.

The fixed-slope spread intercepts are 2.112 for Russia and 1.371 for the United States. The fixed-slope trade-count intercepts are −1.937 and 0.251. Their latter difference implies $\exp(0.251+1.937)\approx8.92$, which the authors interpret as roughly nine times more transactions at a matched scaled activity level in the more fragmented U.S. market. This is not a causal fragmentation estimate. Cross-country intercepts also absorb currency units, omitted $C,m$, productivity differences, and trade-count conventions. A comparison of structural levels requires a common documented normalization; separate native-currency regressions do not establish it by themselves.

Figures 1–4 reveal substantial heterogeneity that the pooled slopes obscure. Russian stock-specific spread slopes range from 0.249 to 1.011, with most near 0.70; ten are below 0.50 and six above 0.90. U.S. spread slopes range from −0.052 to 1.667, with most between 0.90 and 1.30. Russian stock-specific trade-count slopes range from 1.156 to 1.795, all below two. U.S. trade-count slopes range from 0.416 to 2.646, mostly around 1.50–1.70. Intercepts vary as well.

This difference between pooled and within-stock relationships matters operationally. A cross-sectional scaling benchmark that organizes large and small stocks well need not describe tomorrow’s change in a single stock’s spread or transaction intensity. The authors offer measurement error, endogenous volume/spread responses, and tick/lot restrictions as possible explanations. They do not identify their relative contributions or provide an instrumented causal regression.

## Extending the framework without losing consistency

The methodological procedure is to list all potentially relevant variables, record their unit and leverage exponents, scale the outcome into a dimensionless leverage-neutral quantity, and construct independent invariant combinations from the remaining arguments. Three independent unit restrictions plus one independent leverage restriction reduce the number of unrestricted arguments by four, provided the corresponding exponent matrix has full rank. Redundant dimensions or transformations must not be counted twice.

For execution horizon $T$, minimum price increment $K^{\min}$, and minimum lot $Q^{\min}$, define

$$
B=T\gamma=\frac{T\sigma^2L^2}{m^2},\qquad k=\frac{K^{\min}L}{P},\qquad q=\frac{Q^{\min}\sigma^2L^2}{V}.
$$

All three are dimensionless and leverage neutral. $B$ is expected bets during the execution horizon; $k$ compares the tick with the dollar cost scale; $q$ compares lot size with the implied economic trade scale, up to constants. Equation (27) becomes

$$
G=\frac1L f(Z,B;k,q).
$$

The paper illustrates a term linear in size and execution rate. For a symmetric nonnegative cost this is $G=L^{-1}(\lambda|Z|+\kappa|Z|/B)$. The source prints signed $Z$; that formula must be interpreted on the buy side or as a signed-impact convention, because its initially defined $G$ is nonnegative for either trade direction. Larger urgency raises the second term. No value of $\lambda$ or $\kappa$ is estimated in this draft.

For an optimal horizon, the framework only says that participation rate can have the form

$$
\frac{|Q|}{VT^*}=t^*(Z;k,q).
$$

Constant participation follows **if** the unknown function is constant; a 1% participation rate is an illustration, not an optimum derived from a specified risk/alpha objective. In particular, the illustrative cost decreasing with $T$ has no finite unconstrained optimum without an additional urgency, risk, or opportunity-cost mechanism.

If optimal ticks and lots depend only on $P,V,\sigma^2,C$, their permissible scales are

$$
K^{\min *}=a_K\frac P L,\qquad Q^{\min *}=a_Q\frac V{\sigma^2L^2}.
$$

The constants require an economic welfare or execution criterion that the paper does not solve. For actual quoted spread, equation (32) generalizes to $S/P=L^{-1}s(k,q)$. This provides a natural regression extension: explain deviations from the base spread law using normalized ticks and lots, rather than raw tick values that confound price and liquidity.

For dollar collateral per share $H$, equation (33) gives

$$
\frac H P=\frac1L h(k,q,B).
$$

The simplified proportionality $H/P\propto1/L$ requires that the relevant normalized frictions and liquidation horizon be appropriately fixed or optimized. It is a scaling conjecture, not a calibrated haircut rule with a specified default probability or stressed liquidation-loss distribution. A sentence in the source refers to $H\propto1/L$; the dimensionally consistent statement concerns $H/P$.

Finally, if $X$ is the size of a child trade, its normalized distribution may satisfy $\Pr(P\widetilde X/(CL)<x)=F(x;k,q)$, while transaction rate has the form

$$
N=\sigma^2L^2 n(k,q).
$$

A constant $n$ recovers the tested count exponent. This makes explicit the additional assumption linking child trades to institutional bets: execution frictions must produce a stable relationship between the two. A binding lot size or a changing degree of order fragmentation can violate that assumption while leaving some bet-level scaling relationships approximately intact.

## What can be implemented from this source

The paper supplies enough algebra to implement invariant feature construction, the pooled scaling regressions, fixed-slope benchmark lines, and normalized residual diagnostics. It also supplies a transparent way to enlarge a transaction-cost model when ticks, lots, or horizons matter. A researcher should retain the fitted function separately from the dimensional normalization so that a change in cost shape is not confused with a change in units.

Exact numerical replication still requires the original 2015 membership lists and raw feeds, quote/trade filters, currency and turnover conventions, missing-minute rules, the precise realized-return formula, monthly aggregation order, and reconciliation of sample counts. The external calibration of $C,m$ cannot be re-created from this PDF alone. There is no held-out validation, execution experiment, portfolio construction rule, or demonstration of net trading profitability.

The defensible practical conclusion is that volume and variance, transformed through these economic restrictions, provide useful low-dimensional benchmarks. Their success is strongest as a pooled organization of spread and activity data. The empirical deviations, within-stock slope differences, and unestimated extension functions define the work remaining before the framework becomes an order-specific execution or margin engine.

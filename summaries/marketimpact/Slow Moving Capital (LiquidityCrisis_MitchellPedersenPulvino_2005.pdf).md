# Slow Moving Capital

Mark Mitchell, Lasse Heje Pedersen, and Todd Pulvino. *American Economic Review, Papers and Proceedings* 97(2), May 2007, pp. 215–220. The local filename says 2005, but the file contains the six-page published 2007 article, including its references and four figures. It has no appendix.

Source: [LiquidityCrisis_MitchellPedersenPulvino_2005.pdf](../../Finance/LiquidityCrisis_MitchellPedersenPulvino_2005.pdf). Printed pages equal PDF pages plus 214. This note covers the entire short article; its length reflects the available evidence rather than a generic paper-length target.

## Why this matters

A security can become cheaper precisely when the investors best equipped to value and hedge it are forced to sell. The relevant constraint is then the capital and organizational capacity of the specialist intermediary, not the wealth of all investors combined. An apparent convergence trade must survive the time needed for replacement capital to arrive. The paper documents this mechanism in convertible bonds during 2005 and the 1998 LTCM crisis, and in merger arbitrage during October 1987.

The distinctive contribution is the combination of specialist holdings, relative valuations, and event timing. Price declines alone could reflect deteriorating fundamentals. Specialist sales alone could be an orderly transfer to better-capitalized buyers. Here, sales coincide with widening deviations from modeled values, while natural replacement buyers respond slowly or sell as well. The result is descriptive evidence for limits to arbitrage and delayed capital reallocation, including within multistrategy firms.

This is not a structural estimation of a financing constraint, a controlled experiment, or a complete trading strategy. The authors do not estimate a price-impact coefficient, arbitrage-capital adjustment speed, or optimal position size. They argue that observed sequences are inconsistent with frictionless instantaneous capital substitution. Their language sometimes assigns causality more strongly than the available event comparisons alone can establish.

## Mechanism and the securities being compared

A convertible combines corporate debt with the right to exchange it for shares. A specialist buys the convertible and shorts underlying stock to reduce equity exposure. The source also mentions interest-rate hedges, short straight debt or purchased credit protection, and short stock options to hedge volatility exposure. These transactions can make the position substantially less exposed to fundamental shocks; they do not remove funding, liquidity, model, borrowing, or imperfect-hedging risk.

Convertibles facilitate rapid issuance because specialist investors can value and hedge them. The article describes the Rule 144A market as commonly completing issuance in one or two days, sometimes under 24 hours, versus at least a month for public issuance. This institutional observation explains why issuers may pay a liquidity premium. It is background for the 2005 episode, not a measured treatment effect in this paper.

Suppose a bond has modeled value $V$ and observed price $P$. Define its price ratio $q=P/V$ and discount $d=1-q$. This notation makes the empirical comparisons explicit; the source presents the ratios graphically rather than as numbered equations. Even if $V$ stays constant, an increase in $d$ generates losses for an existing long position. With bond exposure approximately three times equity, an incremental 2.7% cheapening implies an approximate 8.1% equity loss before financing, hedge profits, and other changes. This arithmetic explains the scale of losses; it is not a fitted return attribution.

Losses can induce redemptions, internal risk-budget reductions, or margin pressure. Forced sales then deepen the discount, creating another round of losses for other holders. Replacement investors may lack information, infrastructure, staff, or committed capital. A multistrategy fund can have firm-level capital yet restrict a losing desk because headquarters cannot distinguish temporary mispricing from a deficient strategy. The article offers this as an interpretation of trading patterns and staff changes, not as a directly measured information barrier.

## Convertible holdings in the 2005 episode

Section I and Figure 1, pp. 216–218, use quarterly SEC 13-F holdings from the first quarter of 2004 through the third quarter of 2006. Classification is fixed using year-end 2004 holdings, before the main liquidation episode. A reporting entity is classified as a convertible-arbitrage specialist if it is a hedge fund, more than 50% of its reported assets are convertible securities, and it owns at least \$100 million of convertibles at that date.

The resulting 28 specialists own approximately \$40 billion of convertible bonds at year-end 2004, about 15% of the US convertible market. This is a large observed subset, not the whole arbitrage industry. The statement that hedge funds account for up to 75% of the convertible market describes a broader industry estimate and should not be substituted for sample coverage.

To separate selling from changing valuations, the authors adjust holding values with returns on the Merrill Lynch All US Convertibles Index. A transparent reconstruction would deflate each quarter's total holdings by the cumulative index return from the comparison date, then measure changes relative to the year-end 2004 base. The article does not give its exact adjustment formula or fund-level weighting, so this is an implementable interpretation of the stated procedure, not a claim to recovered code. Index adjustment also leaves residual error when particular portfolios have returns unlike the index; it is not an exact bond-quantity measure.

By year-end 2005, the specialists had sold 35% of their holdings, with a reported $t$-statistic of −2.75 against no change. By the third quarter of 2006 the decline was 41%, with $t=-3.02$. The article does not report the covariance calculation or whether the test weights firms by size. Figure 1 shows the fall as a persistent reduction rather than a one-quarter reversal.

The source separately cites the Barclay Group: more than 20% of convertible-arbitrage capital was redeemed during the first quarter of 2005, and assets under management had fallen by half by the first quarter of 2006. Redemptions, assets under management, and adjusted bond holdings are different quantities and come from different samples. They should not be treated as interchangeable flow measures.

Coverage creates several limitations. Small and some foreign managers are absent; Wall Street desk positions are mixed with their parent institutions' other holdings; and reporting entities may have names different from their fund brands. The authors could not locate filings for several known liquidations and believe the measured decline understates actual selling. A missing filing must therefore not automatically be encoded as either zero holdings or unchanged holdings. Figure 1 cannot identify the ultimate buyers because every sale has a counterparty, many outside the observed specialist groups.

The paper's footnote describes a 15-day reporting deadline. That statement is not needed to construct its historical quarter-end panel, and this note does not use it to infer when holdings were publicly tradable information. A replication should preserve both the reporting date and actual filing date rather than assume immediate observability.

## Convertible prices and modeled values

The valuation panel contains 550 US convertible bonds during 2005–2006. Market prices come from several Wall Street trading desks. The theoretical prices use a finite-difference model incorporating each bond's terms and four sets of inputs: the issuer's stock price; volatility inferred from historical and option-implied volatility; credit spreads informed by credit default swaps, straight-debt yields, investment-bank estimates, and ratings; and the interest-rate term structure.

The source does not supply the partial differential equation, numerical grid, boundary conditions, call and put treatment, conversion schedule coding, recovery convention, volatility blending weights, credit-source hierarchy, quote side, observation time, or pricing code. Consequently the numerical theoretical values cannot be independently recovered from the paper alone. Giving a generic convertible model and calling it the authors' implementation would conceal the main replication limitation.

The sample is restricted to bonds whose underlying stock price is at least 65% of the conversion price. If $S_{it}$ denotes stock price and $K^{\mathrm{conv}}_{it}$ conversion price, the reported screen is $S_{it}/K^{\mathrm{conv}}_{it}\geq0.65$. This retains more equity-sensitive bonds, whose prices should depend less on poorly measured credit spreads. A reconstruction should apply the screen on each valuation date; the article does not fully describe entry, exit, and missing-price treatment.

Figure 2, p. 217, plots the cross-sectional median of $P_{it}/V_{it}$ from January 2005 through September 2006, with a December 2004 starting point in the figure, and a convertible-hedge-fund return index on the other axis. The median reduces sensitivity to extreme valuation errors but does not eliminate a systematic bias in the model or input estimates.

The largest reported discount is 2.7% in mid-May 2005. Relative to the historical distribution over 1985–2004, that deviation is roughly 2.5 standard deviations from the average. These are deviations relative to the historical average discount; the article does not provide the mean and standard deviation needed to recompute that standardized statistic. It is also not a conventional regression significance test.

Discounts become especially large around redemption-notice deadlines, described as 45 days before the ends of June and December. The authors say daily data confirm this timing, but the daily observations and test are not reported. Figure 2 therefore supports the broad time pattern, while the precise deadline effect remains an unreported analysis.

Convertible-arbitrage hedge-fund returns were −7.2% during January–May 2005. The authors compare this with the 2.7% bond cheapening under typical 3:1 leverage. They argue that imperfect hedging contributed little because volatility and credit spreads changed relatively little. This is an approximate economic consistency check, not an audited decomposition of every fund's performance. The subsequent 2006 recovery supports a temporary price-dislocation interpretation but does not prove that every part of the original discount was nonfundamental.

## Did plausible replacement investors buy?

The authors identify 27 multistrategy hedge funds already holding convertibles at year-end 2004 but with convertibles below 50% of their portfolios. Requiring existing exposure is intended to isolate investors with relevant trading infrastructure. These funds increased aggregate holdings by 36% by year-end 2005 and 18% by the third quarter of 2006, relative to the initial base. The increase came after the first-quarter sell-off, and one fund accounted for much of it. More than half of the 27 reduced exposure between year-end 2004 and the third quarter of 2006.

Thus the aggregate buying statistic does not describe the behavior of a typical multistrategy fund. The source also reports that large multistrategy funds without initial convertible positions did not buy material quantities during 2005. Two large firms reportedly replaced their convertible trading staff after losses. The data are consistent with slow internal reallocation, although waiting for still cheaper securities is another explanation acknowledged in the article.

The CRSP Mutual Funds Database supplies 16 convertible mutual funds with at least \$100 million of net assets at year-end 2004. These experienced modest redemptions and reduced holdings rather than absorbing the hedge-fund liquidation. The article interprets limited leverage capacity as another restriction on their ability to provide replacement capital. It does not estimate their unused borrowing capacity or investor demand curve.

## The 1998 comparison

Figure 3, p. 218, repeats the valuation comparison around LTCM using a proprietary convertible portfolio and a method described as similar to the 2005 exercise. The graph runs from December 1997 through December 1999. After losses on macroeconomic bets, LTCM liquidated convertibles; falling marks then created losses and selling pressure for other convertible funds.

The discount exceeded 4%, nearly four historical standard deviations below normal valuation, and prices required several months to return toward normal. This supplies a second episode with the same economic sequence. However, the source does not report the number of bonds, identities, individual positions, credit and volatility inputs, or statistical testing procedure for 1998. Treat it as corroborating event evidence rather than an independently complete replication design or a second estimate of an identical parameter.

## Merger arbitrage during October 1987

Section II and Figure 4, pp. 218–220, examine 107 ongoing mergers involving US publicly traded targets. A cash-deal arbitrageur buys the target; a stock-deal arbitrageur also shorts acquirer shares in the exchange ratio. The spread compensates for time, financing, and deal failure risk. An acquirer hedge does not remove the risk that the deal fails or its terms change.

The authors cite their separate 2001 study for a market beta near zero in normal months and about 0.50 in severely declining markets. That nonlinear-risk estimate is not newly estimated here. The current contribution is the event sequence and direct evidence about specialist trading desks.

On October 1 the median merger spread was 3.3%. During October 14–16, proposed antitakeover legislation from the House Ways and Means Committee raised concerns about leveraged buyouts and hostile transactions; the median spread reached 5.4% on October 16. It then widened to 9.7% on October 19 and 15.1% on October 20. Many Nasdaq stocks did not trade on October 19, making October 20 a more informative market-wide mark. These figures are unannualized quoted deal spreads, not expected riskless returns.

The article describes a spread as offer price minus target price but does not explicitly state the denominator used for the percentage series, the stock-deal updating rule, or how terminated deals leave the panel. A replication must resolve those conventions instead of silently equating the percentage discount to the return on purchase price. It also needs the initial deal list, subsequent terms, prices, and portfolio weighting used in Figure 4's return series.

Confidential data cover 18 Wall Street proprietary merger-arbitrage desks during October 1987 only. These desks held more than 10% of aggregate takeover-target value at the beginning of the month. The chart reports aggregate net purchases as a percentage of their total long portfolio value. They were net buyers on October 1–13, began selling on October 14, cut holdings by 6% on October 19, and sold more than 12% on October 20. They remained net sellers every subsequent trading day that month, despite a 5% market rebound and indications that Congress would withdraw the proposal.

The persistence of selling after some adverse news reversed is the key observation supporting constrained capital. It does not establish that deal risk had already returned to its precrash level. The source interprets closures of desks and funds as additional evidence of capital withdrawal. The confidential data, originally gathered for Mitchell–Netter's earlier work, are not reproduced transaction by transaction, and the article gives no regression, confidence interval, or causal instrument for the desk-sale effect.

## What a reconstruction can and cannot establish

The study can be reconstructed as three linked datasets: a quarterly manager-holdings panel, a bond-price/model-value panel, and a daily merger-event/desk-trading panel. The essential operations are to fix manager classifications before the 2005 shock; distinguish valuation changes from trades; compare market marks with contemporaneous modeled values; align discount changes with redemption and legislative events; and measure whether investors with demonstrated infrastructure actually supply capital.

The strongest reported quantitative evidence is the size and persistence of specialist sales and price discounts. The mechanism is plausible because it appears across securities with relatively observable contractual payoffs and across distinct capital shocks. The weakest step is identifying a pure deviation from fundamental value: a convertible model can misprice credit and liquidity, while merger failure probabilities can genuinely change during a crash. Financing and liquidity premia may be part of equilibrium required returns even when conventional fundamental inputs move little.

For an investor, the supported implication is to distinguish a convergence opportunity from the ability to finance it through interim losses. Leverage, redemption terms, organizational authority to add risk, and readiness to deploy capital matter alongside estimated cheapness. The paper supplies no universal discount threshold, expected recovery horizon, or optimal leverage. Its empirical message is narrower and useful: replacement capital took months in these episodes, and the likely buyers were not automatically the actual buyers.

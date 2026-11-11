# Risk premia: asymmetric tail risks and excess returns

Yves Lempérière, Cyril Deremble, Trung-Tu Nguyen, Philip Seager, Marc Potters, and Jean-Philippe Bouchaud, *Quantitative Finance* 17(1), 1–14 (2017); published online June 21, 2016. DOI: 10.1080/14697688.2016.1183035. Source: [RiskPremia_Bouchaud_2016.pdf](../../Finance/RiskPremia_Bouchaud_2016.pdf), fourteen pages including the ranked-P&L appendix.

## Why this matters

A strategy can earn a high average return by accepting infrequent large losses, while another can earn returns with little negative tail asymmetry. Volatility alone does not distinguish these payoff profiles. This paper compares equities, size and momentum factors, credit, currency carry, and short-volatility strategies using a ranked-return diagnostic designed to reveal how the largest moves contribute to cumulative performance.

Its contribution has two parts: a low-moment measure of asymmetry derived from ranked P&L, and broad empirical evidence that many conventional risk-premium strategies have higher Sharpe ratios when their returns are more negatively skewed. The authors summarize that association with a suggestive line, $S\approx1/3-\zeta^*/4$. They explicitly caution that it is not a convincing universal linear law or a prediction derived from a valuation theory.

Trend following, value, and low-volatility strategies are important counterexamples in their classification. Positive returns together with positive measured skewness lead the authors to describe these as anomalies or “pure alpha.” That is an interpretation within their definition of risk premium, not a proof that the strategies have no omitted, unobserved, liquidity, funding, or regime risk.

## Ranked P&L and an implementable skew measure

Start with periodic strategy returns or P&L increments $r_t$. For the main statistic, center them and divide by their sample standard deviation, obtaining $z_t$. Sort observations by increasing $|z_t|$, retaining their original signs. If $z_{(k)}$ is the observation of amplitude rank $k$, define an empirical ranked cumulative function consistently with Appendix A as

$$
F_0(k/n)=\frac1n\sum_{j=1}^{k}z_{(j)}.
$$

Then $F_0(0)=F_0(1)=0$, apart from numerical error. The division by $n$ matters: the population integral is an average truncated return, and omitting it would make the reported skew statistic grow with sample length. Integrate this curve over rank fraction using a declared quadrature convention:

$$
\zeta^*=-100\int_0^1F_0(p)dp.
$$

The factor 100 is an arbitrary presentation scale. A single positive hump means small-to-medium moves contribute positively while the largest moves reverse those gains, producing negative $\zeta^*$. An inverted hump indicates the opposite asymmetry. Sorting destroys chronology deliberately; it diagnoses the distribution, not drawdown duration, clustering, or recovery time.

For a centered unit-variance density $P$, Appendix A writes

$$
F_0(p)=\int_0^{x(p)}y[P(y)-P(-y)]dy,
\qquad P(|r|\leq x(p))=p.
$$

This is preferable to the appendix's Equation A5 as printed, whose conditional-expectation notation and threshold signs do not reproduce the truncated-moment definition. For zero-mean returns, an equivalent tail identity is

$$
F_0(p)=E[|r|1_{\{r<-x(p)\}}]-E[|r|1_{\{r>x(p)\}}].
$$

These are probability-weighted tail contributions, not unweighted conditional tail means. This distinction is necessary for a correct implementation.

The authors also plot uncentered raw cumulative P&L sorted by amplitude and compare it with a symmetrized return series $m+\varepsilon_t(r_t-m)$, where independent signs $\varepsilon_t$ take values plus or minus one. In expectation, the symmetric comparison preserves the mean and removes asymmetry. A finite random-sign realization need not preserve the sample mean exactly without an additional adjustment; for the standardized statistic the population symmetric ranked curve is zero.

## Robustness and mathematical qualifications

The ranked statistic avoids directly averaging cubed returns, making it less dominated by extreme observations than conventional third-moment skewness. This is useful when financial tails put third moments near nonexistence. It does not eliminate estimation uncertainty: the centering, volatility normalization, large ranks, and historical sample all remain influential.

The appendix discusses extensions whose integrals can remain finite with very heavy tails. Those claims should not be confused with the operational definition requiring a mean and standard deviation. A distribution with infinite mean or variance cannot literally be standardized to zero mean and unit variance by population moments. An alternative location/scale convention would have to be specified before applying the extended heavy-tail claim.

For weak departures from Gaussianity, Equation A7 prints $25/(6\pi)$ multiplying conventional skewness and also gives an approximate decimal 1.273. These do not agree: $25/(6\pi)\approx1.3263$. The note therefore does not use the printed decimal as an exact conversion. The empirical ranked-area algorithm is independently specified and does not require that expansion.

The utility interpretation also has conditions. Positive third derivative can imply preference for positively skewed alternatives within an appropriate distribution ordering; equal mean and variance plus a larger third moment alone is not a universal expected-utility ordering. The appendix uses a single-hump ranked curve to motivate “skewness comparable” distributions. This is a restricted comparison, not a license to rank arbitrary multimodal payoff distributions by one scalar.

## Risk scaling and comparison conventions

Many strategy backtests are scaled to approximately constant recent risk. The source variously describes a twenty-day exponential volatility moving average, a twenty-day moving average, and a moving average of absolute returns. These are closely related risk controls but not identical estimators. Exact decay, annualization, leverage normalization, lagging, floors, and treatment of initial observations are not fully specified. A reproducible implementation must declare them and use only completed past data in position scaling.

Sharpe ratios make comparisons less dependent on constant leverage, but time-varying leverage changes the return distribution itself. Skewness measured after volatility management is therefore a property of the managed strategy, not necessarily of the bare asset. Monthly and daily skewness can also differ materially. The paper's results should retain their sampling frequency and risk-management convention.

Dollar-neutral small-minus-large or high-yield-minus-AAA portfolios are not automatically beta-neutral or duration-neutral. The text calls several factors orthogonal or market neutral, but nominal long-short construction does not guarantee zero realized market covariance. A replication needs the actual factor and hedge definitions rather than treating the terminology as an algebraic identity.

## International equity premium evidence

Global Financial Data supplies total-return equity indices and ten-year government rates for twenty-seven countries, with heterogeneous start dates and a common January 2014 endpoint. Monthly histories range from Germany in 1870 and the US in 1871 to Indonesia in 2009. Excess performance is constructed relative to the ten-year government rate. That reference is the authors' convention; it is not the same as subtracting a one-month bill return, and a quoted long yield is not an instantaneous risk-free holding-period return.

The history-length-weighted equity premium is approximately 5% annually, with cross-country dispersion around three percentage points. The equally invested portfolio over indices available at each date has reported t-statistic 4.2. All countries except the Philippines have positive reported excess returns. The US entry is 5.33% premium, 15.2% volatility, and Sharpe 0.35; Japan is 2.04%, 18.7%, and 0.11. Heterogeneous samples make these cross-country comparisons descriptive rather than a controlled common-period experiment.

Figure 2 reports a correlation around -0.27 between Sharpe and index volatility. Premium itself has a small negative, statistically insignificant correlation with volatility, around -0.1. Cross-country correlation of negative ranked skew with premium is only about 0.2, which the authors themselves call weak evidence. Table 7 later gives an international-index correlation using a different comparison summary; its values should not be silently substituted for Figure 2's statistic.

For the daily risk-managed US market since 1928, the reported Sharpe is approximately 0.57 and $\zeta^*\approx-1.47$. The largest 5% of absolute moves erase approximately half the gains contributed by the smaller 95%. Monthly US ranked skew is much milder, about -0.32, while conventional monthly third-moment skew in the long historical sample is positive. This illustrates both frequency dependence and sensitivity of conventional skew to extremes; it does not mean the two statistics measure an identical population feature with interchangeable units.

## Equity factors, size, and exceptions

For ten country/index families, the authors form daily dollar-neutral portfolios long a small-cap index and short a large-cap index, then risk-manage the spread. Nine have positive Sharpe ratios; Australia is the exception at -0.27. Reported examples include the S&P family at 0.32, France at 0.40, Italy at 0.70, and South Africa at 0.26. The corresponding size-index volatilities are not systematically greater for small stocks, but ranked skew generally becomes more negative as capitalization falls.

US Fama–French decile histories begin in 1950. In Table 3, the smallest-cap decile has daily volatility 0.83%, ranked skew -1.83, and Sharpe 0.56; the largest has 0.96%, -0.39, and 0.39. The small-cap premium thus does not correspond to higher volatility in that table. For momentum, the loser decile has ranked skew 0.00 and Sharpe -0.07, while the winner decile has -0.90 and 0.67. Positive momentum performance is associated with more negative asymmetry.

The long-short SMB and UMD factors have daily ranked skews approximately -1.39 and -1.38. The source says the largest 5% of moves remove nearly all smaller-move SMB gains and about 20% of UMD gains. Figure 4 reports Sharpe ratios 0.14 for SMB, 0.67 for UMD, and 0.64 for HML.

HML differs: its ranked curve has positive asymmetry. The running text gives +0.25, while Figure 4's caption and Section 7.2 give +0.43. This internal discrepancy should remain visible rather than be resolved by inventing an undocumented variant. The later value is the one used in the outlier discussion. Its monthly ranked skew is reported as -0.56, reversing the daily sign and weakening a horizon-invariant “pure alpha” classification.

The low-volatility deciles show Sharpe rising from 0.49 for the most volatile group to 1.01 for the least volatile, without a monotone negative-skew increase. The market-neutral low-volatility strategy is reported to have positive daily ranked skew +0.27. Trend following on diversified futures with a fifty-day horizon is an even clearer outlier, with daily ranked skew +0.18 and monthly +1.72. Its detailed contract universe, signal, and execution design are referred to another paper, not specified completely here. Cross-sectional stock momentum and time-series futures trend following are different strategies; their opposite skew signs are not a direct contradiction.

## Credit and currency carry

The credit study uses BofA US corporate total-return indices through Global Financial Data, with daily data since 1997. Table 4 spans AAA to CCC and below. Reported annual yield rises from 4.7% for AAA to 15.5% for CCC and below, while volatility is broadly around 4–5% except the lowest grade at 7.3%. Ranked skew is approximately -0.8 for investment grade and near -1.8 to -2.0 for BB and lower. Yield is not the same as realized excess total return, and differences in duration or index composition are not separately neutralized in this table.

Risk-managed spreads long CCC or BB and short AAA have Sharpe ratios 0.54 and 0.45, t-statistics 2.2 and 1.9, and ranked skews -0.84 and -0.43. This is modest statistical evidence rather than a uniformly overwhelming premium. A high-yield/AAA spread also retains credit, liquidity, and potentially duration exposures.

FX data cover January 1974 through January 2014. The twenty currencies/countries are Australia, Canada, Switzerland, Czech Republic, Germany, Hungary, Israel, Iceland, Japan, Korea, Mexico, Norway, New Zealand, Poland, Sweden, Singapore, Thailand, UK, US, and South Africa. Spot rates and short rates come from Global Financial Data, using interbank rates when available and central-bank discount rates otherwise. Data availability and currency/regime transitions require care; the article does not supply a complete daily panel or transition rules.

Each day, the 190 unordered currency pairs are oriented to buy the higher-rate currency and finance in the lower-rate one. Pairs are sorted into ten interest-differential deciles. These positions overlap heavily because currencies appear in many pairs; 190 pairs are not 190 independent bets. The caption's repeated description of both end deciles as small carry is a typo; the text orders from smallest to largest differential.

The lowest-carry decile has Sharpe -0.28, daily volatility 0.45%, and skew -0.41; the highest has 1.04, 0.93%, and -1.05. Across deciles, Sharpe correlates -0.76 with skew and +0.78 with volatility. Carry is therefore an explicit case where volatility and reward are positively associated as well. The diversified equal-pair carry strategy has Sharpe around 0.85 and skew -0.94.

The authors dispute an external claim that out-of-the-money hedging leaves carry profitable. Their own at-the-money option hedge removes the carry P&L; they infer that more expensive out-of-the-money protection would be unfavorable. Exact option expiries, strikes, hedge notionals, rebalancing, transaction costs, and dataset are not provided here. The inference should not be reported as a fully reproducible out-of-the-money hedge experiment.

## Short variance and the cross-strategy plot

The short-variance exercise begins in January 1996 and ends in January 2014. It covers S&P 500, DAX, crude oil, gold, EUR/USD, and GBP/USD variance swaps. Each position sells variance and is scaled by recent P&L volatility. A short variance swap receives a fixed variance strike and pays realized variance, subject to contract conventions; the article does not provide maturity, strike sampling, rolls, realized-variance definition, bid/ask, financing, or exact P&L marking.

| Underlying | Sharpe | Ranked skew |
|---|---:|---:|
| S&P 500 | 1.47 | -4.64 |
| DAX | 0.79 | -5.53 |
| Crude oil | 0.74 | -5.28 |
| Gold | 0.71 | -4.79 |
| EUR/USD | 0.88 | -5.32 |
| GBP/USD | 0.38 | -5.01 |
| Diversified total | 1.26 | -4.61 |

The aggregate has t-statistic above four and much more negative ranked skew than the other examples. Short VIX futures have lower Sharpe and less negative skew in the comparison, but are not interchangeable with variance swaps because their payoff and term-structure exposure differ.

Figure 7 combines strategies into the empirical relation $S\approx1/3-\zeta^*/4$. The line's intercept implies positive Sharpe even at zero measured skew, another reason not to read it as an exact equilibrium pricing formula. Samples overlap, portfolio variants are correlated, horizons differ, and several measurements contain sizable error. The authors explicitly call the plot suggestive.

Table 8 gives bootstrap skew errors and Sharpe errors. For example, market-factor errors are 0.12 and 0.13, trend errors 0.16 and 0.14, and aggregate variance-swap errors 0.22 and 0.24. The text says standard bootstrap for skew but does not specify block length, serial-dependence treatment, number of replications, or all Sharpe-error calculations. The plotted two-sigma channel based on selected factor errors is not a uniformly valid prediction interval for every new strategy.

HFRX's net Sharpe 0.48 is tentatively adjusted to 0.85 before fees, assuming roughly 10% volatility and a conventional two-and-twenty fee structure. This is an approximate fee correction, not an observed gross-return series. A synthetic equal-weight combination of equity, short volatility, carry, and CDS portfolios lies above the line, illustrating potential diversification of asymmetry. No complete implementable allocation and rebalance specification accompanies that point.

## Mechanisms, classification, and limits

The authors investigate whether a single global factor could support a co-skewness pricing interpretation. They report no clear separation between the first two eigenvalues of the strategy correlation matrix and an unstable leading eigenvector. Co-skewness with the US equity market does not reproduce the Sharpe pattern. This evidence fails to identify their chosen global factor; it cannot rule out all state-dependent common tail exposures. Linear correlation is also insufficient to establish independence during extreme losses.

Their proposed mechanisms are qualitative. Cash flows attract investors, crowding creates deleveraging risk, and expected returns and skew adjust together. Alternatively, an inherently negatively asymmetric insurance payoff requires compensation to attract sellers. The paper acknowledges that direct evidence for the crowding mechanism would be desirable. A drifting skew estimate is not a causal test of changing crowdedness.

For reproduction, first implement the centered ranked-area statistic with sample-size normalization, then keep frequency and volatility scaling identical within each comparison. Rebuild each historical universe and its stated date range, use lagged risk estimates, and distinguish yields, total returns, and excess returns. A complete reproduction further needs instrument conventions, costs, exact data identifiers, signal definitions referred elsewhere, and the bootstrap settings absent here. The printed appendix identities and HML discrepancy warrant checks against the direct ranked algorithm.

The practical takeaway is a diagnostic question: how much performance comes from small frequent gains paid back in large losses? The paper gives a useful way to see and quantify that pattern across strategies. It does not establish a universal price of skewness, prove that positive-skew strategies are riskless alpha, or demonstrate that ordinary diversification removes crisis tail risk. Those stronger conclusions require additional identification and out-of-sample evidence.

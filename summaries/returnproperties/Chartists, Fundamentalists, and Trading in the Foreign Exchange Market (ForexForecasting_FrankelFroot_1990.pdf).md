# Chartists, Fundamentalists, and Trading in the Foreign Exchange Market

**Jeffrey A. Frankel and Kenneth A. Froot — American Economic Review, 80(2), May 1990, pp. 181–185, Papers and Proceedings.**

**Source:** [ForexForecasting_FrankelFroot_1990.pdf](../../Finance/ForexForecasting_FrankelFroot_1990.pdf). The local file contains a JSTOR cover followed by the complete five-page article. Page references below use printed article pages. This is a short empirical and conceptual paper: its companion studies contain fuller econometric and structural treatments. No appendix, executable model, or trading backtest is supplied in this PDF.

## Why this matters

Exchange-rate movements can reflect changes in how market participants form expectations, even when conventional macroeconomic fundamentals move little or move in the opposite direction. Frankel and Froot investigate a mechanism in which short-horizon extrapolators and longer-horizon fundamentalists coexist. Recent success changes the influence of their forecasts on aggregate demand for currency. A sustained appreciation can therefore increase the weight placed on forecasts of further appreciation, rather than immediately attracting enough stabilizing fundamentalist capital to reverse the move.

The paper is useful for a researcher trying to distinguish three objects that are often conflated: disagreement across forecasters, differences between short- and long-horizon forecasts, and changes in the composition of forecasting methods. It supplies evidence on all three. It does not establish that any technical signal earns an investable return after costs. Its central practical implication is about model specification: a representative forecast with a fixed relationship to fundamentals can miss important state dependence in market expectations.

The motivating episode is the dollar's appreciation in the early 1980s. Rising real interest differentials provide a plausible explanation through much of 1981–1984. Between June 1984 and February 1985, however, the dollar rose approximately another 20% while the real interest differential declined; much of this additional rise reversed over the following nine months. The authors regard this as difficult for a simple overshooting account. An econometrician should not treat that observation alone as proof of a bubble: omitted or poorly measured fundamentals remain an alternative explanation.

## The proposed expectations mechanism

The conceptual distinction is between **chartists**, who infer near-term direction from recent prices and technical patterns, and **fundamentalists**, whose longer-horizon forecasts put weight on measures such as purchasing power parity. A currency perceived to be above its long-run value can simultaneously be expected to appreciate over the next week and depreciate over the next year. Those forecasts need not contradict one another because their horizons differ.

The authors' account of the dollar episode is a feedback process. Fundamentalist predictions of depreciation repeatedly failed during the appreciation. Market participants consequently reduced the influence of fundamentalist forecasts and increased the influence of chartist forecasts. Even without a new favorable macroeconomic shock, this shift could raise dollar demand and its current price. Continuing appreciation then made extrapolative forecasting appear successful for longer.

It is important to identify what is and is not specified. The article describes learning and changing forecast weights, but does not give a likelihood, a Bayesian updating recursion, a forecast-error loss function, a wealth accumulation rule for competing trader classes, or a fully specified market-clearing equation. It also does not estimate the elasticity of currency demand with respect to an aggregate forecast. An implementation that chooses those ingredients is an extension, not a replication of a completely identified structural model in this paper.

A useful notation for organizing the evidence is to let $a_t$ denote a recent percentage dollar appreciation and $f_{t,h}$ the survey expectation of dollar appreciation over horizon $h$. The central empirical question is whether the response of $f_{t,h}$ to $a_t$ changes sign with the horizon. A schematic regression is

$$
f_{t,h}=b_{0,h}+b_{1,h}a_t+u_{t,h}.
$$

This equation restates the reported regressions in a consistent sign convention; it is not a new estimated result. The article describes regressions of expected depreciation on recent actual depreciation. Reversing both dependent and explanatory signs leaves the slope unchanged. A positive slope therefore indicates extrapolation, and a negative slope indicates expected reversal, under either consistent convention.

Do not infer from the notation that the source provides a complete definition of $a_t$ for every survey observation. Exact observation alignment, currency pooling, regression intercept treatment, and some econometric implementation details are not specified in this short article. Those omissions matter for reproducing its numerical coefficients.

## Forecast horizons: the most direct quantitative evidence

Table 1 on p. 184 reports the following estimates. Standard-error calculations underlying the reported $t$ ratios use generalized-method-of-moments methods. The table does not supply an implementation-ready covariance estimator with a stated kernel and bandwidth.

| Survey and sample | Forecast horizon | Slope on recent exchange-rate change | Reported $t$ ratio |
|---|---:|---:|---:|
| Money Market Services, October 1984–January 1988 | 1 week | 0.13 | 4.32 |
| Money Market Services, October 1984–January 1988 | 4 weeks | 0.08 | 1.60 |
| Economist, June 1981–August 1988 | 3 months | −0.08 | −2.98 |
| Economist, June 1981–August 1988 | 6 months | −0.17 | −4.98 |
| Economist, June 1981–August 1988 | 12 months | −0.33 | −5.59 |

On a percentage-point interpretation, an additional 1% recent dollar appreciation is associated with approximately 0.13% more expected appreciation over one week. The four-week point estimate has the same sign but is not conventionally significant. The corresponding expected change at one year is approximately 0.33% more depreciation. The one-week result and all three Economist results carry the table's 99% significance indication; the four-week estimate does not.

These are responses of **expectations**, not realized future returns. A statistically clear relation between past prices and forecasts can coexist with poor realized forecasting accuracy. The slopes also do not directly measure the percentage of traders following each method or the capital allocated to them.

The comparison has a design limitation: short and long horizons come from different survey providers over different sample windows. Horizon, respondent composition, and historical period are therefore partly confounded. The table is strong descriptive evidence for different expectation patterns, but not a controlled experiment varying only forecast horizon. A new study should obtain multiple horizons from the same respondents at the same timestamp to isolate this distinction; that is a proposed extension, not the design reported here.

## Disagreement, volume, and volatility

The authors first establish that exchange-rate forecasts are dispersed. In the Financial Report survey associated with the Economist, the average high–low range of six-month forecasts is 15.2%. In the MMS one-month forecasts, average cross-respondent standard deviation is approximately 2.2% for the yen/dollar rate, with somewhat larger values for the mark, pound, and Swiss franc.

These statistics measure different things. A range is especially sensitive to extreme respondents and survey size, whereas a standard deviation uses the distribution of responses. Neither directly measures the uncertainty of an individual forecaster. One should not substitute the 15.2% range for a volatility parameter in a pricing or portfolio model.

The trading-volume context is substantial. The paper reports adjusted daily U.S. foreign-exchange turnover of approximately \$128.9 billion in April 1989, 120% above March 1986. London and Tokyo turnover are approximately \$187 billion and \$115 billion, respectively, and worldwide turnover exceeds \$430 billion. Nonfinancial counterparties account for only 4.9% of bank and 4.4% of nonbank activity in the cited evidence. These facts motivate a role for financial trading beyond transactions directly linked to trade in goods. They do not establish that every financial trade is noise trading or that gross turnover measures net speculative exposure.

The econometric exercise uses weekly observations from **October 1984 through February 1988** for the British pound, German mark, Japanese yen, and Swiss franc. Its variables are unusually specific:

- Volume is the weekly number of contracts traded in the nearest-term currency futures contract at the IMM division of the Chicago Mercantile Exchange.
- Volatility is the weekly mean of squared percentage futures-price changes measured at 15-minute intervals.
- Dispersion is the percentage standard deviation of the MMS forecasts across respondents.

The volatility measure is an average of intraday squared changes. It is not the variance of weekly returns and should not silently be replaced with the sum of intraday squared changes. The latter scales with the number of sampled intervals, so conventions about trading hours, missing observations, and holidays would affect comparisons. Likewise, futures turnover is a proxy for activity in a much larger foreign-exchange market, not a complete measure of spot and over-the-counter trading.

The authors use prewhitened Granger-causality tests. Dispersion predicts subsequent volume at the 95% confidence level for three of the four currencies. They also report that dispersion predicts volatility. Exact test statistics, lag selections, filtering coefficients, and the currency-specific results are not supplied here; the referenced companion study contains the fuller investigation.

Volume and volatility are strongly contemporaneously correlated, but the exercise does **not** find a statistically significant direct Granger-causal effect from volume to volatility. This distinction prevents an easy but unsupported chain of inference: finding dispersion before volume and observing volume with volatility does not establish that volume transmits the effect of disagreement to volatility. A same-period relationship may also escape tests based only on lagged predictors.

The reverse direction matters as well. Volatility predicts dispersion. One possible mechanism is genuinely different interpretations of market events. Another is survey measurement: MMS respondents are interviewed at different times within the day. Large intraday price changes can mechanically widen the distribution of forecasts recorded at different timestamps, even if respondents would agree when conditioned on identical information. The paper expressly recognizes this timing problem. A replication should preserve survey timestamps where available and distinguish dispersion in forecasts of a common future level from dispersion caused by different contemporaneous spot rates.

## Evidence on the changing composition of forecasting methods

Table 2 on p. 184 summarizes Euromoney surveys of forecasting services. The unit is a **service**, and one firm can offer more than one service. This is not a panel of investment capital or a count of individual market participants.

| Survey year | Total services | Chartist | Fundamental | Both |
|---|---:|---:|---:|---:|
| 1978 | 23 | 3 | 19 | 0 |
| 1981 | 13 | 1 | 11 | 0 |
| 1983 | 11 | 8 | 1 | 1 |
| 1984 | 13 | 9 | 0 | 2 |
| 1985 | 24 | 15 | 5 | 3 |
| 1988 | 31 | 18 | 7 | 6 |

The early category counts do not always add to the stated total. The source does not supply a complete reconciliation, so the table above preserves the published values. It would be inappropriate to invent an unclassified category or alter the total merely to make the arithmetic balance.

Using the reported total as denominator, the pure-chartist share rises from $3/23\approx13.0\%$ in 1978 to $18/31\approx58.1\%$ in 1988. The pure-fundamental share falls from $19/23\approx82.6\%$ to $7/31\approx22.6\%$. These percentages are calculations from the source table, not separately reported estimates. Changing survey coverage and entry or exit of services limit any interpretation as within-firm switching.

The surrounding prose also reports firm counts: in 1978, eighteen firms emphasized fundamental analysis and two technical analysis; in 1985, one fundamental firm and twelve technical firms are described. Those numbers differ from the service counts because the unit differs. Combining them into a single series would create a false precision about the migration toward chartism.

The survey evidence supports the plausibility of changing forecasting composition. It does not estimate the market-clearing forecast weight: a service's existence or popularity does not reveal its clients' trading volumes, balance sheets, leverage, or price impact. The link from service composition to exchange rates remains a proposed economic mechanism.

## Reproducing the paper's figures and tests

Figure 1 on p. 182 compares the real dollar and real interest differentials over 1973–1989. The dollar measure uses CPI-adjusted exchange rates against the foreign G10 countries plus Switzerland, with trade weights based on the foreign countries' world exports and imports during 1978–1983. The index is normalized to March 1973 equal to 100. The real interest differential is the U.S. measure minus the weighted foreign measure. The figure's data are credited to Peter Hooper and Catherine Mann at the Federal Reserve Board.

An empirical reproduction has three separate modules. First, reconstruct that macroeconomic comparison with the specified weights and normalization. Second, obtain the actual MMS and Economist survey observations for Table 1 and reproduce the horizon-specific expectation regressions. Third, construct weekly futures volume, intraday volatility, and forecast dispersion and reproduce the prewhitened lead–lag tests. The modules use different frequencies and sample periods; forcing them into a single panel would change the experiment.

The article does not give enough detail to regenerate exact results from raw vendor data alone. Missing inputs include the survey respondent panel and missing-response treatment, exact regression alignment, intraday observation and futures-roll conventions, prewhitening order, test lag lengths, and GMM covariance implementation. The appropriate replication output is therefore a documented reconstruction with sensitivity to these choices, unless the original companion material and data can be recovered.

For the conceptual mechanism, further choices are required before simulation is possible: definitions of the fundamental exchange rate and extrapolative signal, a forecast-weight updating rule, demand elasticities, constraints on positions, and a price-clearing rule. The paper mentions moving-average rules illustratively, including a one-week versus twelve-week comparison. It does not report a calibrated or evaluated strategy based on that rule.

## What the evidence establishes—and what remains open

The most distinctive finding is the sign change in forecast extrapolation across horizons, accompanied by evidence that the forecasting-services industry shifted toward technical analysis during the dollar appreciation. This is consistent with heterogeneous expectations influencing currency demand. The volume results add a possible connection between disagreement and market activity, but offer no clean causal identification of excess volatility generated by technical trading.

The article compares three broad views of volume: it may improve price discovery and reduce unnecessary volatility, be irrelevant when prices already reflect information efficiently, or amplify volatility through noise trading. Its evidence does not decisively select one of these views. Nor does it rule out rational responses to unobserved fundamentals.

For quantitative work, the productive use of this paper is to formulate measurable hypotheses about forecast heterogeneity and endogenous model weights. Preserve the distinction between survey expectations and profitable predictions; preserve horizon and timestamp conventions; and treat structural forecast-weight dynamics as an extension requiring explicit assumptions. Those boundaries are essential to making a reproduction informative rather than turning the paper's narrative into an unsupported trading algorithm.

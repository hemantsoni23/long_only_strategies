# High idiosyncratic volatility and low returns: International and further U.S. evidence

Andrew Ang, Robert J. Hodrick, Yuhang Xing, and Xiaoyan Zhang. *Journal of Financial Economics* 91 (2009), pp. 1–23, DOI 10.1016/j.jfineco.2007.12.005. [Source PDF](../../Finance/High%20Idiosyncratic%20Volatility%20and%20Low%20Returns.pdf). The complete 23-page article, including footnotes and references, was read. Tables 2, 4, 6, 7, 10, and 12 were checked against rendered pages. This is the international extension and additional U.S. analysis, distinct from the authors' 2006 paper, “The Cross-Section of Volatility and Expected Returns.”

## Why this matters and what is new

A stock's recent residual volatility is easy to estimate and usually persistent. A conventional intuition is that bearing difficult-to-diversify stock-specific risk should require compensation. Ang, Hodrick, Xing, and Zhang instead find that stocks with high past idiosyncratic volatility have low subsequent average returns. This paper tests whether their earlier U.S. result generalizes across developed markets, whether the associated strategy returns move together internationally, and whether several candidate mechanisms account for the pattern.

The main global portfolio result is a monthly world three-factor alpha of −1.307% for high-volatility minus low-volatility quintiles, with a robust $t$-statistic of −5.68. Excluding the United States reduces the alpha to −0.670%, with $t=-3.16$. The effect is therefore not solely a U.S. sample result, although U.S. stocks materially strengthen it. The raw spreads are smaller: −0.893% and −0.396% per month, respectively, with the latter statistically insignificant at conventional two-sided levels.

The second contribution is common variation in these spreads. A U.S. high-minus-low volatility portfolio explains part of the corresponding foreign strategies, and their intercepts become insignificant when its return is included. This is evidence of shared variation, not proof that the U.S. portfolio is a priced economic risk factor. The authors explicitly decline that stronger interpretation without a theory of why investors demand the stocks that earn low returns.

Third, detailed U.S. tests retain a negative volatility relation after controlling for informed trading, trading-friction proxies, analyst coverage, institutional ownership, price delay, skewness, leverage, and forecasts of future volatility. These controls narrow the explanatory problem. They do not rule out every information or friction mechanism, nor do they turn gross portfolio alphas into realized arbitrage profits.

## Returns, universes, and factor construction

The international universe consists of firms in 23 developed markets corresponding to the MSCI developed-country universe. U.S. stock returns come from CRSP and U.S. accounting data from Compustat; non-U.S. stock data come from Datastream. The underlying international sample generally starts in January 1980 and ends in December 2003. Finland and Spain begin in 1986, Greece and Portugal in 1987, New Zealand in 1985, and Sweden in 1982. The other markets are Australia, Austria, Belgium, Canada, Denmark, France, Germany, Hong Kong, Ireland, Italy, Japan, the Netherlands, Norway, Singapore, Switzerland, the United Kingdom, and the United States.

The smallest 5% of firms by market capitalization are excluded in each non-U.S. country. This is not stated as a corresponding 5% exclusion for the U.S. sample. The detailed U.S. analysis uses data beginning in July 1963 and ending in December 2003, with actual test dates varying by characteristic availability. International return tests requiring lagged characteristics run from September 1980 to December 2003, or 280 monthly observations for the major markets. Several captions use the broader January 1980 start; the text identifies the shorter usable return interval.

Most analyses express stock and factor returns in U.S. dollars, subtracting the one-month U.S. Treasury-bill return. Local-currency robustness tests also use the stated U.S. Treasury-bill convention. They are not automatically returns funded at local cash rates. The distinction matters when reconstructing a currency-hedged investment strategy, which the paper does not provide.

For each country $j$, the local factor model has market, size, and value factors. The local market is the value-weighted market excess return. The size factor buys the smallest third of firms and sells the largest third; the value factor buys the highest book-to-market third and sells the lowest third. The paper follows the Fama–French approach but describes these local factors through country thirds. A replication should not substitute a different global factor construction while claiming to reproduce the supplied estimates.

Regional factors combine country factors using value weights within North America, Europe, and Asia. World factors combine the regional factors, again using value weights. Thus the local, regional, and world models differ in the common variation removed before calling the remainder “idiosyncratic.” Residual volatility is model-dependent; a residual to three world factors can still contain country, industry, or other systematic variation.

For model $a\in\{L,R,W\}$, estimate within a formation month

$$
r_{i,d}^e=\alpha_{i}^{a}
+\beta_{i,M}^{a}MKT_d^{a}
+\beta_{i,S}^{a}SMB_d^{a}
+\beta_{i,H}^{a}HML_d^{a}+\varepsilon_{i,d}^{a}.
$$

The signal is the standard deviation of the fitted daily residuals. Annualized volatility uses $\sqrt{250}$ times the daily standard deviation. The baseline formation window is the preceding calendar month; robustness windows are three, six, and twelve months. The supplied methods do not fully identify every residual degrees-of-freedom convention, minimum-observation rule, Datastream return filter, or missing-accounting treatment. These choices are particularly consequential for a short daily regression and should be documented in a replication.

Table 1 shows the much larger U.S. cross-section: an average of 5,441 firms, versus 1,453 in Japan and 1,077 in the United Kingdom. Average world-model annualized residual volatility is 51% in the United States and 26% in the United Kingdom. The U.S. 25th-to-75th-percentile range is 25.0%–61.1%, substantially wider than the typical non-U.S. range. Total, regional-residual, and world-residual volatility are correlated above 95% within each country, so alternative volatility definitions often lead to similar rankings in this sample.

## Cross-sectional regression design and timing

For every month, the authors estimate a Fama–MacBeth cross-sectional regression of next-month excess returns on past volatility, factor loadings, and characteristics. A notation that makes the information dates explicit is

$$
r_{i,t+1}^{e}=c_t+\gamma_t\sigma_{i,t}
+\lambda_{\beta,t}'\widehat\beta_{i,t+1}
+\lambda_{z,t}'z_{i,t}+e_{i,t+1}.
$$

Here $\sigma_{i,t}$ uses daily data in month $t$, while $z_{i,t}$ contains log beginning-of-holding-period market capitalization, book-to-market information available six months earlier, and returns over the preceding six months. Pooled international regressions also include country indicators: separate indicators for the six non-U.S. G7 countries and a residual non-U.S. group, with the United States as the benchmark where present.

The factor loadings in the baseline regression are estimated using daily returns during the same month as the dependent return, $t+1$. This is an explanatory asset-pricing regression, not a fully ex ante return-prediction model. The authors motivate contemporaneous loadings by the covariance restriction of factor models and state that using lagged loadings gives nearly identical unreported results. The volatility signal itself is observable at formation. Keeping these roles separate avoids assigning a trading interpretation to every right-hand-side variable.

Average cross-sectional coefficients are tested using Newey–West standard errors with four monthly lags. Returns are in percentage points while annualized volatility enters as a decimal. Thus a coefficient near −2 means a one-unit change in annualized volatility, not a one-percentage-point volatility change, is associated with about −2 percentage points of monthly return. The coefficient has to be multiplied by the relevant volatility difference before its economic magnitude can be interpreted.

The market-cap-weighted variation is a weighted cross-sectional regression. Written as an objective, it minimizes $\sum_i MC_{i,t}e_{i,t+1}^2$, up to normalization. The source describes generalized least squares with inverse market capitalizations in the covariance/weighting-matrix discussion; the stated intention and table are value weighting. A software implementation should be explicit about whether its matrix is an error-covariance matrix or the matrix multiplying squared residuals, since confusing these conventions would reverse the weights.

## International regression estimates

Table 2's U.S.-dollar results are:

| Country | Coefficient on world residual volatility | Robust $t$ | Predicted monthly return change, volatility 25th to 75th percentile |
|---|---:|---:|---:|
| Canada | −1.224 | −2.46 | −0.31% |
| France | −1.439 | −2.14 | −0.26% |
| Germany | −2.003 | −3.85 | −0.37% |
| Italy | −1.572 | −2.10 | −0.27% |
| Japan | −1.955 | −5.18 | −0.32% |
| United Kingdom | −0.871 | −2.54 | −0.15% |
| United States | −2.014 | −6.67 | −0.73% |

For the United States, $-2.014(0.611-0.250)=-0.727$ percentage points per month. This is a fitted partial association holding the other regressors fixed. It is not the causal effect of raising a particular company's volatility while everything else stays unchanged. The source itself observes that the news causing such a large volatility change would probably also change other firm characteristics.

The local-currency coefficients are similar, but the statement in the prose that all are highly significant is too broad. France's local-currency coefficient is −1.057 with $t=-1.64$, short of a conventional two-sided 5% threshold. The remaining reported non-U.S. G7 local-currency estimates have $t$-statistics from −2.59 to −5.89. The U.S.-dollar all-G7 significance claim and the local-currency qualification can both be true.

Pooling countries, Table 3 reports volatility coefficients of −0.668 for Europe, −1.177 for Asia, −1.747 for the G7, −1.069 for the G7 excluding the United States, −1.536 for all countries, and −0.604 for all countries excluding the United States. Their robust $t$-statistics are −2.33, −3.17, −6.40, −4.14, −5.82, and −2.32. The worldwide interquartile volatility range is 20.3%–50.5%; multiplying by −1.536 gives an approximately −0.47-point monthly fitted return difference.

Table 4 strengthens rather than eliminates the association when firms receive market-cap weights. The U.S. estimate becomes −2.243, $t=-7.00$; all countries give −1.750, $t=-6.41$; and all excluding the United States give −0.846, $t=-3.26$. The prose on p. 9 repeats the equal-weighted all-country estimate −1.54 and $t=-5.82$ while discussing the weighted table. The values here follow the rendered Table 4. Stronger value-weighted coefficients show that the result is not simply an artifact of giving tiny firms equal influence, but do not alone identify a monotonic causal size interaction.

Longer formation windows retain negative coefficients. For the United States, three-, six-, and twelve-month signals yield −2.461, −2.091, and −1.273, with $t=-5.68,-4.35,-2.60$. For all countries excluding the United States, the corresponding estimates are −0.930, −0.685, and −0.605, with $t=-2.93,-2.07,-1.98$. Three months can improve measurement precision; longer windows may dilute current ranking information. These are alternative historical specifications, not a rolling validation exercise that selects an optimal horizon without looking at subsequent performance.

## Portfolio construction and alpha versus return

At every month-end, firms are sorted within each country into quintiles of world-model residual volatility. The country quintiles are then aggregated into regional or global quintiles using their U.S.-dollar market capitalizations. The portfolios are value weighted and rebalanced monthly. This procedure preserves a within-country ranking before aggregation; it is not a single pooled global sort that lets a high-volatility country dominate the high-volatility bucket.

For each portfolio, the full monthly excess-return series is regressed on the world market, size, and value factors. The intercept is a world three-factor alpha. The paper uses the direction “5–1”: long the highest-volatility quintile and short the lowest, so the documented anomaly appears as a negative number. Reversing the trade reverses its gross return and alpha but does not remove shorting or financing costs.

| Region | 5–1 alpha, %/month | Robust $t$ | Raw 5–1 return, %/month | Robust $t$ |
|---|---:|---:|---:|---:|
| Europe | −0.723 | −3.01 | −0.412 | −1.50 |
| Asia | −0.529 | −1.84 | −0.270 | −0.83 |
| G7 | −1.353 | −5.46 | −0.927 | −2.55 |
| G7 excluding U.S. | −0.651 | −2.77 | −0.388 | −1.36 |
| All countries | −1.307 | −5.68 | −0.893 | −2.62 |
| All excluding U.S. | −0.670 | −3.16 | −0.396 | −1.49 |

The low global quintile's alpha is 0.163% per month and the highest quintile's alpha is −1.144%. Much of the spread is a high-volatility short-leg phenomenon. Outside the United States, the low quintile's alpha is 0.040% and the high quintile's is −0.629%. This matters for investors able to avoid expensive stocks but unable to short them: the headline long–short alpha is not the same as an incremental return achievable in a long-only allocation.

Asia illustrates the distinction between regression coefficients and portfolio significance. Its cross-sectional volatility coefficient is significant, yet its quintile alpha spread has $t=-1.84$. A narrower distribution of residual volatility and portfolio-level return noise contribute to the difference. The text reports a larger extreme-decile effect, with magnitude 0.79% and $t=-2.23$, but prints its spread with a positive sign despite the negative direction and statistic. The quintile table is the unambiguous numerical baseline.

An alpha obtained by subtracting full-sample factor exposures is an ex post adjusted return. The factors may be tradable in theory, but the paper does not construct a real-time hedge-estimation rule or charge for implementing the factors. Calling the alpha “investable” in the source does not make its fitted factor hedge available at the beginning of the sample.

## International common variation

Let $VOL^{US}$ be the U.S. high-minus-low residual-volatility portfolio. Table 7 compares regressions of foreign high-minus-low portfolios on world factors, on $VOL^{US}$ alone, and on both. The useful specifications exclude U.S. stocks from the dependent portfolio, avoiding an obvious mechanical overlap.

With $VOL^{US}$ alone, Europe has loading 0.370, $t=14.1$, and adjusted $R^2=0.42$; Asia has loading 0.271, $t=7.29$, and $R^2=0.16$. The G7 excluding the United States has loading 0.362 and all countries excluding the United States 0.348. Their intercepts are small and insignificant.

After including world factors, Europe's loading remains 0.317 with $t=8.61$, while Asia's falls to 0.028 with $t=0.56$. The G7-ex-U.S. loading is 0.208 with $t=5.40$, and the all-ex-U.S. loading is 0.198 with $t=5.73$. Their respective intercepts are −0.245% and −0.283% per month, with $t=-1.04$ and −1.34. Europe has alpha −0.104%, $t=-0.46$; Asia has −0.475%, $t=-1.57$.

The prose on p. 14 mistakenly attaches the larger G7/all-country coefficients that include U.S. stocks to the excluding-U.S. discussion. The values above follow Table 7. The distinction is material: the actual foreign loadings support common variation but are smaller than the mechanically overlapping portfolios' loadings of 0.635 and 0.580.

Statistically insignificant intercepts do not prove that true intercepts are zero. Nor does spanning by another anomaly portfolio explain why either portfolio earns its average return. Shared discount-rate shocks, common investor behavior, correlated characteristics, or omitted systematic exposures could each generate comovement. The paper's strongest justified claim is that international replication is not equivalent to many independent national bets.

## The detailed U.S. tests

U.S. regressions control for local three-factor loadings and size, book-to-market, and six-month returns, then add one candidate explanatory characteristic at a time. The controls are the probability of informed trading, or PIN; the fraction of zero daily returns as a transaction-cost proxy; analyst counts; institutional ownership; a price-delay statistic; and individual return skewness.

PIN is based on intraday trading information and limits its sample to January 1984–December 2001. Analyst coverage uses current-fiscal-year earnings forecasts in I/B/E/S and the reported sample is July 1976–June 2001. Institutional ownership uses Standard & Poor's data, July 1981–June 2000. Delay uses the improvement in explanatory power from adding lagged market returns to a weekly market-model regression, with data beginning in July 1965. The zero-return and skewness specifications use the long 1963–2003 history. Some return regressions start seven months after the listed input-data start because lagged characteristics are needed.

The PIN, analyst, ownership, and delay datasets also reduce the stock count. Average monthly cross-sections in Table 8 range from 3,447 for the broad zero-return/skewness samples to 556 for the combined-control specification. Therefore differences across specifications combine control effects with sample composition and dates. They are not clean causal decompositions of the original coefficient.

The volatility coefficient remains negative in every reported specification: −1.117 with PIN, −1.023 with zero-return frequency, −1.767 with analyst coverage, −0.789 with institutional ownership, −0.759 with delay, and −0.937 with skewness. The combined specification, excluding PIN, is −1.813 with $t=-4.27$. Replacing local residual volatility with total volatility or world residual volatility gives −1.730 and −1.873 in that combined specification, with $t=-4.10$ and −4.25.

The corresponding portfolio tests first sort on the control characteristic, then sort on residual volatility within each control quintile, and average equal-ranked volatility portfolios across control groups. Constituent portfolios are value weighted. These are sequential double sorts, unlike an unconditional intersection of two independent sets of breakpoints. Each row controls one characteristic at a time; the three-factor alpha provides a separate ex post factor adjustment.

For August 1963–December 2003, the unrestricted U.S. 5–1 local-factor alpha is −1.290% per month, $t=-6.71$, and the raw spread is −0.97%. The low quintile's alpha is 0.103%, $t=2.15$, versus −1.186%, $t=-7.12$, for the high quintile. Controlling for PIN gives −1.004%; zero-return frequency −1.101%; institutional ownership −1.152%; and skewness −1.204%. Analyst coverage and delay shrink the spread most, to −0.687%, $t=-2.13$, and −0.667%, $t=-4.28$.

These findings reject the proposition that those particular measured characteristics completely subsume the signal in the reported designs. They do not establish that trading costs are economically unimportant. Zero-return frequency is a proxy, not an execution simulation; the study does not report borrow fees, locate availability, spread crossing, market impact, turnover, or capital requirements for shorting the highest-volatility stocks.

## Leverage and the option interpretation

The paper considers an interpretation of equity as a call option on firm assets. In the cited framework, excess equity return takes the form

$$
\frac{dP_t}{P_t}-r_fdt
=\frac{\pi\Delta S_t}{P_t}dt
+\frac{\sigma_a\Delta S_t}{P_t}dW_t,
$$

where $S_t$ is the underlying unlevered asset claim, $P_t$ equity value, $\Delta=\partial P/\partial S$, $\pi$ the asset risk premium, and $\sigma_a$ asset volatility. A proposed mechanism links volatility or uncertainty to option delta and predicts a stronger negative return–volatility relation at higher leverage.

This is a candidate economic story, not a general theorem that Black–Scholes delta always decreases with volatility. Delta's derivative can depend on moneyness and parameter values, and equity elasticity involves both delta and price. The authors themselves discuss richer stochastic-volatility models in which the sign may change. Their empirical test concerns the specific leverage-interaction prediction rather than all structural equity models.

Leverage is book debt divided by book debt plus market equity. Table 10 adds leverage and its interaction with residual volatility. The volatility coefficient changes from −0.935, $t=-2.24$, to −1.135, $t=-4.45$. The leverage coefficient is −0.921, $t=-3.66$, while the interaction is positive, 1.585, $t=2.48$, contrary to the proposed stronger-negative-effect prediction.

Sequential leverage/volatility sorts reinforce that result. The 5–1 alpha is −1.592% per month in the lowest-leverage quintile and −1.157% in the highest. Averaging across leverage groups leaves −1.265%, $t=-7.25$. Thus the effect is present where the simple high-leverage option explanation would not predict its greatest strength.

## Past, forecast, and realized volatility

The core signal is realized volatility in the preceding month. It is not the latent conditional volatility investors expect over the next month. The authors forecast next-month residual volatility using cross-sectional regressions with lagged volatility, size, book-to-market, six-month return, past-month skewness, and turnover. Turnover is prior-month trading volume divided by month-end shares outstanding. Coefficients are estimated using data available through formation time and refreshed each month; the article does not give every operational window choice needed to recreate this forecasting pipeline exactly.

Forecast and lagged volatility have a cross-sectional correlation of 0.95. Including both linearly would invite collinearity, so the paper first sorts on predicted volatility and then on past volatility. The high-minus-low past-volatility alpha is −1.073% per month after averaging across predicted-volatility groups, with $t=-9.44$. Within the highest predicted-volatility group it is −2.175%, $t=-7.52$; within the lowest it is only −0.139%, $t=-1.14$. The remaining information in the lagged signal is consequently concentrated where forecast volatility is already high.

A separate exercise sorts first on realized volatility during the future holding month. Those portfolios are explicitly not tradable. They ask whether the association with past volatility survives after conditioning on an outcome that the investor could not know at formation. To reduce mechanical correlation between realized means and variances caused by skewness, the authors use log returns for this exercise. Average daily-return skewness across firms falls from 1.33 for simple returns to 0.09 for log returns.

The past-volatility anomaly itself changes little under log returns: the simple-sort alpha spread is −1.27% with $t=-6.68$, versus −1.29% with $t=-6.71$ using simple returns. After controlling for future realized log-return volatility, the past-volatility spread remains −1.205%, $t=-6.63$. This is an explanatory robustness result, not a deployable signal using clairvoyance.

One should also distinguish conditional variance from a noisy realized residual standard deviation. The discussion's rational-expectations expression is heuristic about volatility measurement, not a complete observation equation with identified measurement-error distribution. Persistence, forecast error, and skewness can complicate attempts to interpret these sorts as holding the true conditional variance exactly fixed.

## What a reproduction can and cannot claim

A faithful implementation should preserve the signal clock, country-first ranking, value weights, USD conversion, risk-free convention, and six-month accounting lag. It should separately reproduce the monthly cross-sectional regressions, the monthly rebalanced portfolios, and the full-sample alpha regressions. Using only lagged factor betas in a deployable version is sensible, but that is a variant of the baseline explanatory regression and should be labeled as such.

The supplied source does not release a complete point-in-time security master, factor-building code, accounting-field map, detailed Datastream cleaning rules, or transaction-cost specification. It also reports several checks only as available on request: alternative currency/factor definitions, sector controls, pre-1998 endpoints, conditional-volatility estimators, and some stochastic-volatility illustrations. Those findings can be described as author-reported robustness, not independently reconstructed evidence from the printed tables.

International evidence mitigates the concern that the original anomaly is peculiar to one national sample. It is geographic validation, not a clean chronological out-of-sample trading test: much of the international data overlaps the period that generated the initial hypothesis, and global comovement reduces independence across markets. Multiple related specifications also create a broader research-selection issue not addressed by a single reported $t$-statistic.

The practical lesson is to treat recent residual volatility as an empirical characteristic with a strong historical association and unusually concentrated short-leg underperformance. Its international reach and robustness are substantive. Its economic source remains unresolved, and neither high gross alpha nor international comovement by itself supplies an executable, cost-adjusted strategy or a structural risk explanation.

## Source map and bibliography

Ang, Andrew, Robert J. Hodrick, Yuhang Xing, and Xiaoyan Zhang (2009), “High idiosyncratic volatility and low returns: International and further U.S. evidence,” *Journal of Financial Economics* 91, 1–23. Data and factor definitions: equations (1)–(3), pp. 3–5, Table 1. Regression timing and inference: equation (4), pp. 5–6. International coefficients: Tables 2–5, pp. 7–11. Portfolio spreads and comovement: Tables 6–7, pp. 12–14. U.S. controls and double sorts: Tables 8–9, pp. 15–18. Leverage and volatility forecasts: equation (5), Tables 10–12, pp. 18–22. References occupy pp. 22–23; there is no separate appendix in the supplied file. The unrelated journal banner on the first PDF page does not override the article's consistent *JFE* 91 (2009), 1–23 identification.

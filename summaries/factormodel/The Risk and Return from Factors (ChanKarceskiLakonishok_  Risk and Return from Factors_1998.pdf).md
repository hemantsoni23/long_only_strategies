# The Risk and Return from Factors

**Louis K. C. Chan, Jason Karceski, and Josef Lakonishok. Journal of Financial and Quantitative Analysis 33(2), June 1998, pp. 159–188.** Source: [original PDF](../../Finance/ChanKarceskiLakonishok_%20%20Risk%20and%20Return%20from%20Factors_1998.pdf), 31 scanned PDF pages including the final copyright page. All article pages, tables, and appendices were inspected visually. The source studies factor risk and factor returns in the United States, Japan, and the United Kingdom.

## Why this matters

A variable can help explain covariance even if its associated portfolio has no reliable positive mean return. Conversely, a characteristic associated with high average returns need not be an efficient summary of common risk. Chan, Karceski, and Lakonishok evaluate these two questions separately. Their central experiment constructs portfolios using information available before the holding period and asks how much their subsequent returns move together, as well as whether the high-minus-low spread earns a premium.

The most instructive methodological contribution is a demanding benchmark for factor relevance. Sorting stocks on exposures to a randomly shuffled factor can still create portfolios with substantial future return variation. Estimated exposures are weighted averages of past stock returns; stocks that historically comove can therefore receive similar exposures even when the weighting series has no economic meaning. Comparing a proposed factor only with randomly assigned stock portfolios is too easy a test.

The paper's practical conclusion favors a limited collection of market, fundamental, and past-return factors over many individual macroeconomic series. It does not establish a uniquely correct asset-pricing model, nor does it demonstrate that every factor with a large spread volatility should be traded. The empirical design concerns covariance representation and gross return patterns, with no transaction-cost or short-sale implementation model.

## US sample, timing, and return construction

The main universe consists of domestic primary common equities on the NYSE and AMEX in CRSP. NASDAQ is not included in the US analysis. Investment trusts, mutual funds, units, and other nonordinary securities are excluded. Accounting information comes from the annual Compustat files. The narrative describes 1968–1993; the table captions identify the realized portfolio-return period more precisely as **May 1968 through December 1993**, 308 months. Earlier return histories are required for the 60-month loading estimates.

The core construction forms five portfolios at the end of April each year. For accounting characteristics, the design allows four months after the fiscal year-end before using the annual observation. It uses NYSE quintile breakpoints, then assigns eligible NYSE and AMEX stocks to these groups. Returns within each group are equally weighted. The classifications are held for the following twelve months, except for the explicitly faster past-return strategies described below. Equal weighting of monthly constituent returns implies a different return process from a capitalization-weighted or buy-and-hold portfolio; the source does not spell out every intra-year constituent and delisting treatment.

For factor $j$, define the subsequent spread return by

$$
f_{j,t}=\frac{1}{N_{5,t}}\sum_{i\in Q_{5,j}}r_{i,t}
-\frac{1}{N_{1,t}}\sum_{i\in Q_{1,j}}r_{i,t}.
$$

This is a zero-net-dollar long–short return, with one unit long the high group and one unit short the low group. It has gross exposure two per unit of the long leg; the paper does not define a financed margin-account return. All reported percentages below use the original high-minus-low orientation. In particular, its **SIZE factor is large minus small**, the reverse of the familiar SMB convention.

Returns are CRSP returns adjusted for distributions and corporate actions. An exact replication still needs security-share-code details, treatment of missing accounting values, delisting returns, stock entrances and exits within the annual groups, and the original data vintage. The paper's four-month accounting convention is a fixed availability assumption rather than a verified point-in-time release-date database.

## Observable characteristics

The five fundamental sorting variables are book-to-market, cash-flow-to-price, dividend yield, earnings-to-price, and firm size. Market capitalization is CRSP price times shares, aggregating multiple common issues where required. Their accounting definitions, given in Appendix A, are:

- **BM:** common book equity, Compustat item 60, divided by market capitalization.
- **CP:** income before extraordinary items adjusted for common-stock equivalents, item 20, plus depreciation and amortization, item 14, divided by capitalization. Financial firms, identified by the leading SIC digit 6, are excluded from this construction.
- **DP:** common dividends, item 21, divided by capitalization.
- **EP:** item 20 earnings divided by capitalization.
- **SIZE:** market capitalization itself.

Nonpositive observations for a given valuation ratio are excluded from that ratio's sorts. Consequently different fundamental factors need not use identical stock universes. A researcher should not impose a single complete-case universe without recognizing that it changes the experiment.

The three return-history variables deliberately separate horizons. $R(-7,-1)$ uses the six-month interval ending one month before formation, skipping the most recent month; those portfolios are reformed in April and October. $R(-60,-12)$ uses the four-year interval ending one year before formation and is updated annually in April. $R(-1,0)$ is the immediately preceding month's return and is updated monthly. Past returns are compounded over the designated intervals. The first variable is a momentum sort; the latter two test longer-horizon and very short-horizon reversals.

It is important to keep the skip period and update frequency separate. The six-month momentum signal does not hold a fixed portfolio for a year, and the one-month reversal signal is not an annual accounting sort. Calendar conventions should be implemented explicitly rather than inferred from a generic factor-building routine.

## Macroeconomic, market, and statistical factors

Macroeconomic portfolios are formed on **estimated stock exposures**, not on the macroeconomic observations themselves. For each stock and each macro series $z$, use the preceding 60 months to estimate an intercept, exposure to the value-weighted market excess return, and exposure to $z$:

$$
r_{i,t}-r_{f,t}=a_i+b_{i,M}(r_{M,t}-r_{f,t})+b_{i,z}z_t+u_{i,t}.
$$

Rank stocks on $\widehat b_{i,z}$, assign quintiles, and measure their returns after formation. Market controls distinguish an incremental macro exposure from a proxy for broad market beta. The main annual updating schedule applies. The source does not provide a fully specified missing-observation or minimum-valid-history rule for every loading regression; a replication must disclose its own if the exact original cannot be recovered.

The macro variables are:

| Label | Construction |
|---|---|
| DIP | Monthly percentage change in seasonally adjusted industrial production, from the Department of Commerce's Survey of Current Business. |
| DEF | Salomon Brothers high-yield bond index return minus the Ibbotson long-term government bond return. |
| RTB | One-month Treasury-bill return minus monthly CPI inflation. |
| TERM | Long-term government bond return minus the one-month Treasury-bill return. |
| SLOPE | Long-term government yield minus the three-month Treasury-bill yield, as specified in Appendix A. |
| DEI | Change in expected inflation from an ARIMA(0,1,1) specification for monthly CPI inflation. |
| UI | Unexpected inflation, the innovation relative to that inflation model. |

The distinction between TERM and SLOPE is substantive: one is a realized bond-return spread and the other a yield spread. RTB is an ex post real short return. Except for UI, these variables should not automatically be described as newly identified macroeconomic shocks. The inflation-model estimation window, initialization, and vintage treatment are not sufficiently documented to reproduce its exact real-time forecast errors.

Market exposure sorts use CRSP value-weighted and equally weighted market excess returns, producing VWM and EWM mimicking portfolios. Their reported standard deviations are the volatilities of beta-sorted high-minus-low portfolios, **not the volatilities of the market indices themselves**.

Statistical portfolios use the first four asymptotic principal components of the prior 60 months of excess returns. Stocks are sorted on estimated component loadings and held out of sample. Principal components are re-estimated annually. The first component's sign is oriented to agree with the equally weighted market portfolio and the second with the value-weighted market portfolio. Details of the matrix normalization, handling of incomplete histories, and precise time interval used to set these signs are not fully given. A causal implementation should fix signs using training data only; this is an explicit reconstruction rule rather than a verified feature of the original program.

Orthogonality of the estimated component series within a training matrix does not imply that quintile long–short portfolios are orthogonal during subsequent holding periods. Ranking, truncating to tails, equal weighting, and moving to new data all change the object being measured.

## Factor risk requires a nontrivial null

The simplest benchmark randomly assigns stocks to portfolios. Its US high-minus-low standard deviation is only 0.79% per month. Almost every proposed economic factor easily exceeds that number, but this does not establish economic specificity.

The authors therefore permute the observations of a factor series, estimate exposures to the shuffled sequence, and sort on these exposures. Shuffling preserves the marginal distribution of the factor while removing its original alignment with stock returns; it does not preserve its serial structure. The resulting portfolios still select coherent directions in the historical return panel. A shuffled industrial-production factor produces a 1.80% monthly spread standard deviation, and a shuffled TERM series produces 2.17%.

The mechanism can be seen in a simplified univariate loading regression. If $z_t$ is demeaned and normalized, the estimated loading is

$$
\widehat b_i=\sum_t w_t r_{i,t},\qquad
w_t=\frac{z_t-\bar z}{\sum_s(z_s-\bar z)^2}.
$$

Conditional on the chosen weighting sequence, for any two stocks,

$$
\operatorname{Cov}(\widehat b_i,\widehat b_j)
=\sum_{s,t}w_sw_t\operatorname{Cov}(r_{i,s},r_{j,t}).
$$

Common stock-return movements therefore induce related loadings even when $z$ is unrelated to economic fundamentals. Persistent covariance can carry this historical grouping into the next holding period. With a market control, the same reasoning applies to the appropriately residualized regression. This explains why a random time-series factor and random stock assignment are different null experiments.

The article does not give a random seed, number of independent shuffle repetitions, or sufficient detail to determine whether the permutation was redrawn for each estimation window. The reported shuffled-factor figures are useful benchmarks, not a documented Monte Carlo null distribution with calibrated p-values. A modern extension would repeat the entire estimation-and-holding exercise across many randomizations, but those additional tests are not results of this paper.

## US factor-return and risk results

Tables 1–2 separate means from standard deviations. The principal results, converted from decimal monthly returns to percentages, are:

| High-minus-low factor | Mean per month | Standard deviation per month |
|---|---:|---:|
| BM | 0.59% | 3.79% |
| CP | 0.55% | 2.97% |
| DP | 0.08% | 3.72% |
| EP | 0.36% | 2.69% |
| SIZE, large minus small | −0.34% | 5.11% |
| Six-month momentum, skipping one month | 0.64% | 4.16% |
| Four-year past return, skipping one year | −0.46% | 4.15% |
| Prior-month return | −1.79% | 3.75% |

Size and dividend yield exemplify the difference between factor risk and premium. SIZE is highly volatile despite a negative mean in its large-minus-small orientation. DP has a near-zero average spread but almost the same volatility as BM. A covariance model that discards DP solely because its mean is small would lose information about an important axis of comovement.

The tails are economically substantial. SIZE's monthly fifth and ninety-fifth percentiles are −8.57% and 7.24%; its observed minimum and maximum are −28.62% and 14.55%. Because the portfolio is large minus small, a positive extreme means small stocks underperform large stocks. BM's fifth and ninety-fifth percentiles are −4.15% and 6.44%; momentum's are −5.73% and 5.73%. These are empirical distribution summaries, not estimated normal-theory risk limits.

Several macroeconomic portfolios show only modest incremental common variation. DIP's standard deviation is 2.01%, close to its 1.80% shuffled counterpart. The values for RTB, SLOPE, DEI, and UI are respectively 2.53%, 2.37%, 1.75%, and 2.27%. DEF and TERM are more substantial at 2.97% and 3.39%. These comparisons motivate retaining some bond-market exposure variables while treating many individual macro series cautiously.

The statistical and broad-market sorts are stronger: PC1 through PC4 have monthly standard deviations of 5.78%, 3.50%, 2.76%, and 2.22%. VWM and EWM have standard deviations of 4.69% and 5.70%. The first component is especially close to the market direction, while the fourth is already near the shuffled-factor scale. There is no theorem here that precisely four or fewer factors suffice in every universe.

## Calendar and market-state dependence

January accounts for striking average-return effects. Table 1 reports January means of 6.46% for BM, 3.44% for CP, 1.73% for DP, 2.07% for EP, and −8.54% for SIZE. Momentum's January mean is −5.61%; the longer-horizon and prior-month return spreads are −6.40% and −7.22%. In December, BM averages −0.83%, SIZE 1.40%, and momentum 2.26%. These conditional patterns are consistent with mechanisms involving tax trading or institutional window dressing, but the portfolio-return evidence does not identify a causal mechanism uniquely.

The risk does not vanish outside January. Table 4 reports a January SIZE standard deviation of 7.50%, versus 3.51% for the April–September grouping, 5.35% in February, 4.04% in March, 4.66% in October, 4.13% in November, and 4.47% in December. Thus a factor can have a concentrated seasonal mean and still be a material year-round covariance exposure.

Conditioning retrospectively on positive or negative market excess returns also reveals asymmetry. DP averages −1.68% in up markets and 2.19% in down markets. BM averages −0.07% and 1.37%; SIZE −0.90% and 0.35%; momentum 0.53% and 0.77%. These partitions use the realized market state and are descriptions of exposure, not implementable forecasts that know the market sign in advance.

An additional past-return construction uses the six-month block ending thirteen months before formation, $R(-19,-13)$, and still generates a 3.33% monthly spread standard deviation. This is relevant to the shuffled-factor argument: common past-return histories can identify risk groupings even when the specific interval is not the conventional strongest momentum predictor.

## Joint cross-sectional model

To examine incremental effects, the paper estimates a separate cross-sectional regression each month:

$$
r_{i,t}-r_{f,t}=\gamma_{0,t}+\sum_j\gamma_{j,t}X_{i,j,t}
+\sum_n\delta_{n,t}Z_{i,n,t}+e_{i,t}.
$$

$X$ contains start-of-month attributes converted to ordinal ranks scaled between zero and one. This common scale makes coefficient variation more comparable across attributes: one coefficient unit represents moving across the full rank range, not changing a raw accounting ratio by one. $Z$ consists of Fama–French industry indicators; an industry is included only if it has at least ten stocks on average. An implementation must omit a reference industry or impose a normalization if it includes an intercept, since all industry dummies plus an intercept are collinear. The exact normalization is not specified in the article.

The selected eight attributes are BM, DP, SIZE, six-month momentum, four-year past return, DEF exposure, TERM exposure, and EWM exposure. Redundant correlated characteristics are removed before this regression. This selection uses earlier empirical findings, so subsequent evidence is not a completely untouched model-selection holdout. Each month's ordinary least squares coefficient is interpreted as a realized return to the corresponding ranked characteristic conditional on the others and industry.

Table 5 gives the following time-series summaries of those coefficients:

| Attribute | Mean | Standard deviation | Mean t-statistic |
|---|---:|---:|---:|
| BM | 0.009 | 0.024 | 6.70 |
| DP | 0.001 | 0.026 | 0.84 |
| SIZE | −0.004 | 0.054 | −1.35 |
| Momentum | 0.007 | 0.036 | 3.42 |
| Four-year past return | −0.001 | 0.032 | −0.73 |
| DEF | 0.000 | 0.028 | 0.25 |
| TERM | 0.001 | 0.030 | 0.49 |
| EWM | −0.003 | 0.036 | −1.31 |

The entries are decimal returns per full rank unit; 0.009 is 0.9% per month. Rounding prevents exact reconstruction of every t-statistic from displayed means and dispersions. A pseudo-factor benchmark constructed to match the attributes' pairwise correlations has coefficient standard deviation around 1.5%, below those of the retained attributes. Nevertheless coefficient volatility can be inflated by multicollinearity, so large dispersion alone is not proof of unique economic content.

A joint Hotelling-type test of factor means gives an F-statistic of 10.73 with p-value below 0.01. The source reports similar conclusions with an errors-in-variables adjustment. Industry means are not jointly significant at 10%. The covariance-adequacy check applies the Connor–Korajczyk test to additional statistical factors in residuals: non-January and January US statistics are 1.02 and 1.52, with reported p-values 0.15 and 0.08. Failure to reject at conventional thresholds supports parsimony but does not prove that the model spans every relevant covariance direction.

## International evidence and data differences

Japan uses first- and second-section Tokyo Stock Exchange stocks in PACAP, with portfolio returns from May 1976 through December 1994. The UK uses the ABP/Robeco database from May 1973 through December 1994. These are different windows and database conventions, not a matched global panel. Appendix A gives Japan-specific accounting items, including book equity BAL21 and market value, earnings INC9 minus INC8, and depreciation JAF74 for cash flow. Japan's short rate is the one-month gensaki rate. The Japanese yield slope uses a ten-year government yield minus gensaki, while the UK slope uses the long government yield minus a three-month bill rate. Industrial production comes from International Financial Statistics. Only DIP and SLOPE are included as macro factors abroad.

The principal comparison survives these changes. In Japan, BM averages 0.88% per month with standard deviation 3.19%; DP 1.05% with 4.01%; SIZE −0.81% with 5.04%. Momentum averages 0.30% with standard deviation 3.70%, weaker in mean than in the US but still a substantial risk direction. Long-horizon reversal averages −0.73% and prior-month reversal −1.68%. Japan's random stock-group spread has standard deviation 0.80%, whereas DIP has 2.07%, slightly below the shuffled DIP benchmark of 2.14%. PC1, PC2, and PC3 have standard deviations 5.58%, 5.10%, and 3.11%.

In the UK, BM averages 0.95% with standard deviation 2.42%; DP 0.72% with 2.18%; SIZE −0.55% with 4.47%; momentum 0.60% with 2.83%. Long-horizon reversal averages −0.64%, while prior-month reversal is only −0.13%. The random stock-group standard deviation is 0.90%; DIP is 1.50%, compared with 1.42% for shuffled DIP. UK PC1, PC2, and PC3 have standard deviations 3.04%, 3.07%, and 1.93%.

The residual-factor adequacy tests again do not reject strongly: Japan's non-January and January statistics are 0.28 and 0.56, with p-values 0.39 and 0.29; the UK values are 1.12 and −0.02, with p-values 0.13 and 0.51. These corroborating markets are useful, but internationally correlated returns and different local data definitions preclude interpreting them as perfectly independent replications.

## Correlation, interpretation, and replication limits

Appendix B shows why separate univariate factor portfolios can overlap heavily. BM–CP correlation is 0.841, CP–EP 0.851, BM–SIZE −0.650, and BM–long-horizon-return −0.735. DEF and TERM have correlation −0.865; RTB and UI −0.905. PC1 correlates 0.977 with EWM and 0.925 with VWM. These patterns support reducing redundant candidates and retaining orientation conventions carefully. A portfolio neutral to one factor may still have large exposure to several closely related definitions.

The evidence distinguishes three levels of claim. First, substantial future spread variance demonstrates persistent grouping of stock returns. Second, surviving a shuffled-factor benchmark makes an economic variable more distinctive than a generic projection of past returns. Third, a nonzero conditional mean concerns compensation or mispricing. The first does not imply the second, and neither proves the third. Distress, institutional demand, and investor extrapolation are possible economic interpretations, not separately identified causal explanations in these tests.

To rebuild the experiment, archive monthly universe membership and all formation dates; compute the stated accounting and return-history variables; fit each 60-month macro, market, and component model; construct annual, semiannual, or monthly quintiles as appropriate; save subsequent equal-weighted spreads; and calculate unconditional, seasonal, and ex post market-state moments. Then run the rank-based monthly cross-sectional model and residual factor tests. Preserve all orientation and decimal-versus-percent conventions when comparing tables.

Exact numerical reproduction additionally requires historical database vintages, loading-regression missing-data rules, original inflation forecasting choices, component sign and normalization details, the shuffle protocol, industry normalization, and delisting treatment. None should be silently supplied as if reported. Turnover, bid–ask spreads, market impact, borrow availability, and financing are absent, particularly important for the very large prior-month reversal mean. The durable result is methodological: evaluate candidate risk factors against realistic statistical alternatives, keep covariance relevance separate from mean-return evidence, and require that exposures estimated from the past actually organize returns afterward.

# On the Out-of-Sample Predictability of Stock Market Returns

Hui Guo. *Journal of Business* 79(2), 2006, 645-670. Source: [AssetPrediction_Guo_2006.pdf](../../Finance/AssetPrediction_Guo_2006.pdf). All 26 pages were read, including the appendix comparing $cay$ with $tay$, Tables 1-12 and A1, figures, footnotes, and references. Journal page $p$ corresponds to PDF page $p-644$. Numerical tables and critical portfolio equations were checked visually.

## Why this matters

A weak predictor on its own can be useful after conditioning on a second variable with which it is negatively correlated. Guo's central example is aggregate stock-market variance and the consumption-wealth ratio, $cay$. Both have positive partial relationships with subsequent quarterly excess returns, but they are negatively correlated with each other. Omitting either suppresses the apparent forecasting power of the other. The paper uses this interaction to challenge the inference that failure of individual predictive regressions implies an absence of useful aggregate return predictability.

For implementation, the distinction between knowing the population cointegrating relation and estimating it recursively is decisive. The augmented model's reported out-of-sample $R^2$ falls from 11.94% with full-sample $cay$ and immediate macro availability to only 0.04% with recursive $cay$ and a publication delay. Adding the relative short rate improves the latter to 2.19%, but all recursively estimated models have negative $R^2$ over 1976-2002. Those results are more qualified than the abstract's broad claim of substantial out-of-sample predictability.

The portfolio evidence is nevertheless economically interesting. With recursive estimation, lagged macro information, no shorting or borrowing, and 25-basis-point proportional trading costs, the variance-augmented allocation rule produces an annualized mean of 13.35%, volatility of 14.56%, and reported adjusted Sharpe ratio of 0.5757, versus 11.32%, 18.01%, and 0.2873 for buy-and-hold. Its reported certainty-equivalent gain is 2.51% per year. The paper therefore distinguishes predictive squared-error performance from useful state-dependent investment decisions, while leaving an actual vintage-data test unresolved.

## Economic hypothesis and regression structure

The proposed economic interpretation comes from Guo's limited-participation model: investors demand a market-risk premium and an additional liquidity premium. Realized market variance proxies for risk; $cay$ proxies for the liquidity component. This article does not derive that equilibrium or identify the two premiums structurally. It tests reduced-form forecasting implications motivated by it.

Let $e_t=r_{m,t}-r_{f,t}$ be quarterly market excess return, $v_t=\sigma^2_{m,t}$ quarterly realized variance, and $q_t=cay_t$. The core regressions are

$$
e_t=a+bq_{t-1}+u_t,
$$

$$
e_t=a+cv_{t-1}+u_t,
$$

and

$$
e_t=a+bq_{t-1}+cv_{t-1}+d\,rrel_{t-1}+u_t,
$$

with $d=0$ in the principal augmented-$cay$ specification. For the feasible-information version, $q_{t-1}$ is replaced by $q_{t-2}$. The paper calls $cay+v$ “augmented $cay$”; that label does not automatically include the interest-rate variable.

The omitted-variable mechanism is exact in a population linear projection. If the correctly specified conditional linear projection uses both $q$ and $v$, the slope from regressing returns on $q$ alone is

$$
b_{\text{single}}=b+c\frac{\operatorname{Cov}(q,v)}{\operatorname{Var}(q)}.
$$

For $b,c>0$ and negative predictor covariance, this is below $b$. Similarly, the variance-only coefficient is reduced by $b\operatorname{Cov}(q,v)/\operatorname{Var}(v)$. This algebra is a reconstruction of the paper's stated omitted-variable argument. It does not prove causality or rule out other omitted predictors; it explains why the univariate and joint estimates need not agree.

The consumption-wealth ratio is the residual from a cointegrating relation among log consumption, log aggregate net worth, and log labor income. Writing the long-run coefficients as $\beta_a,\beta_y$, the relevant object is schematically

$$
q_t=c_t-\beta_a a_t-\beta_y y_t-\text{constant}.
$$

The source obtains consumption, net worth, labor income, and the supplied $cay$ series from Martin Lettau. For recursive construction it estimates the cointegrating parameters by dynamic least squares using eight leads and lags. The exact original series definitions, deflators, and historical vintage construction are referred to the antecedent data rather than fully specified here. A replication cannot substitute arbitrary household wealth and consumption series and regard the result as the same predictor.

## Data, dates, and transformations

Consumption-related data cover 1952:Q2-2002:Q3. Quarterly return tests extend through 2002:Q4. The market return is the CRSP value-weighted stock-market return, and the risk-free series is from CRSP. Daily returns for realized variance come from Schwert before July 1962 and CRSP thereafter. Variance is constructed from daily market returns following Merton; a practical baseline is a quarterly sum of squared daily returns. The PDF does not print a complete code-level rule covering daily demeaning, missing days, or endpoint treatment.

The 1987:Q4 variance is adjusted downward following Campbell and coauthors because the crash is judged to confound the variance measure. This is a substantive intervention in a variable used as a predictor. The paper does not print the replacement value or exact adjustment formula. That omission prevents an exact replication from this article alone and should be kept separate from a robustness result using unadjusted realized variance.

The relative short rate is the nominal risk-free rate less its last four-quarter average. The wording should be retained when reproducing the author specification; an implementation must explicitly settle whether its moving average includes the current quarter. It is not a Treasury term spread or an innovation from a fitted interest-rate model.

Table 1 reports contemporaneous descriptive statistics, not predictive correlations. Over 1952:Q2-2002:Q4, quarterly excess returns average 0.017 with standard deviation 0.084. The means of $cay$, variance, and $rrel$ are approximately 0, 0.004, and 0; their standard deviations are 0.013, 0.004, and 0.003. Their first-order autocorrelations are 0.831, 0.488, and 0.720. Thus the regressors are persistent, but none has sample autocorrelation above 0.90 in the reported periods.

The correlation of $cay$ with realized variance is -0.392 over the full period, -0.104 in 1952:Q2-1977:Q4, and -0.633 in 1978:Q1-2002:Q4. This strengthening negative association is central to the omitted-variable interpretation. Contemporaneous excess returns correlate -0.415 with variance, which must not be confused with the positive relationship between lagged variance and future returns in the predictive regression. The market can fall when volatility rises while subsequently offering a higher expected return.

Figures 1-3 show $cay$ declining and variance increasing in the late 1990s; short rates then fall steeply during 2001-2002. Those final observations weaken the apparent predictive power of variance and $rrel$ alone. The paper says excluding 2001-2002 strengthens those coefficients, but its main reported results retain them.

## In-sample estimates and stability

Table 2 uses OLS with heteroskedasticity- and autocorrelation-adjusted $t$ statistics. Full-sample $cay$ is used even in the subsample regressions. Hence these are conditional association and stability exercises, not pseudo-real-time tests of a newly estimated consumption relation.

| Full-sample specification, 1952:Q3-2002:Q4 | $cay$ slope ($t$) | Variance slope ($t$) | Relative-rate slope ($t$) | Adjusted $R^2$ |
|---|---:|---:|---:|---:|
| $cay$ alone | 1.911 (4.062) | - | - | 8.2% |
| Variance alone | - | 2.559 (1.315) | - | 1.1% |
| $cay$ and variance | 2.639 (5.278) | 5.832 (3.585) | - | 14.7% |
| Add $rrel$ | 2.448 (5.137) | 5.336 (3.372) | -4.365 (-2.571) | 16.3% |
| Add $rrel$, two-quarter $cay$ lag | 2.065 (4.027) | 5.099 (3.058) | -4.643 (-2.579) | 12.5% |

Returns and predictors use their source units, not standardized-score units. For orientation, multiplying the joint-model $cay$ coefficient 2.639 by its full-sample standard deviation 0.013 gives about 3.43 percentage points of next-quarter excess return; multiplying 5.832 by variance's standard deviation 0.004 gives about 2.33 percentage points. These are derived partial-effect scales, not independent expected-return contributions that can be added without considering predictor covariance.

The joint model's $cay$/variance slopes are 3.329/7.687 in 1952:Q3-1977:Q4 and 2.543/6.066 in 1978:Q1-2002:Q4. Corresponding adjusted $R^2$ values are 23.4% and 9.6%. The signs and broad magnitudes survive, while explanatory power falls materially. The relative rate is significant in the early half but not the later half; its later $t$ is -1.496 when included with one-quarter-lagged $cay$ and variance. Other conventional predictors, including dividend yield, default premium, and term premium, reportedly add little, but those regressions are not tabulated.

## Forecast experiment: two different information assumptions

Both forecast exercises expand the estimation sample through time. The first target is 1968:Q2, using data available through 1968:Q1 for the forecasting regression. After forecasting, one observation is added, the coefficients are reestimated, and the next quarter is forecast. The historical-mean model is also recursively estimated. The principal evaluation window contains 139 quarters from 1968:Q2 through 2002:Q4; a second window begins in 1976:Q1 and contains 108 quarters.

In the fixed-parameter exercise, the cointegrating coefficients are estimated from the entire sample and macro data are assumed observed without delay. The return-prediction coefficients are recursive, but the generated regressor embeds future information. Guo motivates this as a full-information rational-expectations thought experiment. It is not a historical executable forecast.

In the recursive exercise, macro quantities are available with one quarter's delay. For the initial forecast, the cointegrating relation is fitted using 1952:Q2-1967:Q4, then the forecasting regression is fitted through 1968:Q1 with $cay$ lagged twice. Figure 4 shows substantial early variation in the labor-income and wealth coefficients, with greater stability only in the 1990s. This generated-regressor uncertainty is an important source of forecast deterioration.

The author explicitly uses current-vintage macroeconomic data. Recursive estimation and a publication lag therefore do not make this a vintage-correct real-time experiment. Revisions to consumption, labor income, and net worth remain potential differences between the simulated and historically available signals. The source acknowledges this and leaves the effect for future work.

The reported metrics are RMSE, MAE, forecast/realization correlation, sign-hit rate, and

$$
R^2_{OS}=1-\frac{\sum_t(e_t-\widehat e_t)^2}{\sum_t(e_t-\bar e_{t-1})^2}.
$$

| 1968:Q2-2002:Q4 | RMSE | MAE | Correlation | Sign rate | $R^2_{OS}$ |
|---|---:|---:|---:|---:|---:|
| Historical mean | 0.0909 | 0.0701 | -0.1838 | 59.71% | 0 |
| Fixed $cay$ | 0.0884 | 0.0668 | 0.2332 | 61.15% | 5.42% |
| Fixed $cay$ + variance | 0.0853 | 0.0637 | 0.3135 | 64.03% | 11.94% |
| Fixed $cay$ + variance + rate | 0.0858 | 0.0647 | 0.3379 | 62.59% | 10.91% |
| Recursive $cay$ | 0.0927 | 0.0704 | 0.1214 | 62.59% | -4.00% |
| Recursive $cay$ + variance | 0.0907 | 0.0678 | 0.2586 | 61.87% | 0.04% |
| Recursive $cay$ + variance + rate | 0.0899 | 0.0674 | 0.3035 | 61.87% | 2.19% |

The recursive augmented model's RMSE and $R^2$ do not agree exactly if one recomputes from the rounded displayed RMSE values. The source reports 0.0004 for pseudo-$R^2$; it should be preserved as reported, with the difference attributed to an unresolved table inconsistency or rounding rather than silently recalculated as an exact result. Since the gap is larger than simple four-decimal rounding appears to explain, original forecasts would be needed to adjudicate it.

For 1976:Q1-2002:Q4, fixed-$cay$ $R^2$ values are -2.15%, 3.29%, and 2.59%; the recursive counterparts are -8.72%, -4.56%, and -2.39%. Thus variance improves $cay$'s forecasts in both regimes, but improvement over a weak model is not the same as beating the historical mean. Figures 5-6 vary the starting forecast date through 1996:Q4 while retaining at least 25 evaluation observations. Fixed augmented $cay$ consistently improves the relevant RMSE ratios; the recursive model's gain over the historical mean becomes clearer for starts after 1990. These overlapping subsample comparisons do not constitute independent replications.

## Nested-model inference

Table 5 reports Clark-McCracken encompassing statistics, ENC-NEW, and McCracken equal-accuracy statistics, MSE-F, with nonstandard nested-model critical values. In normalized notation with $P$ forecast errors, restricted error $u_{0t}$, and augmented error $u_{1t}$, the usual representations are

$$
MSE\!\text{-}F=P\frac{MSE_0-MSE_1}{MSE_1},
\qquad
ENC\!\text{-}NEW=P\frac{P^{-1}\sum_tu_{0t}(u_{0t}-u_{1t})}{MSE_1}.
$$

These formulas reconstruct the named test statistics; the article reports their results and references rather than a full derivation. The encompassing test asks whether the extra forecast contains relevant information. The accuracy test asks whether that information improves mean squared error enough to overcome estimation noise. They need not agree.

For fixed $cay$, augmented $cay$ versus the historical mean gives ENC-NEW 24.47 against a 95% critical value 2.96 and MSE-F 18.85 against 1.52. Against $cay$ alone, the values are 14.02 against 2.13 and 10.25 against 1.70. In the recursive case, augmented $cay$ versus the historical mean gives 14.81 against 2.96 but only 0.40 against 1.52; only the encompassing null is rejected. Against recursive $cay$ alone, both tests reject: 10.22 against 2.13 and 5.97 against 1.70. This is the sharp statistical conclusion: variance reliably improves the consumption signal, but recursive augmented $cay$ does not demonstrate a significant MSE gain over the historical mean in the full evaluation window.

## Mapping forecasts into positions

All reported economic tests use recursive cointegrating coefficients and the lagged macro information convention. Two rules allocate between stocks and the risk-free asset, called bonds in the paper.

The switching rule is

$$
w_t=\mathbf 1\{\widehat e_{t+1|t}>0\}.
$$

It holds either 100% stocks or 100% bills. This only uses the forecast sign; improvements in squared error or forecast magnitude may have little effect on decisions if the sign is unchanged.

The optimal-weight rule solves the static mean-variance problem

$$
\max_{0\leq w\leq1}\left\{w\widehat e_{t+1|t}-\frac{\gamma}{2}w^2\widehat v_{t+1|t}\right\},
$$

and hence, when estimated variance is positive,

$$
w_t=\operatorname{clip}_{[0,1]}
\left(\frac{\widehat e_{t+1|t}}{\gamma\widehat v_{t+1|t}}\right).
$$

The paper calls this a static CAPM allocation. Risk aversion is $\gamma=5$. Conditional variance is the fitted value from a regression of realized market variance on a constant and its two lags. Estimation uncertainty is ignored. The PDF does not give a positive-variance safeguard, precise recursive variance-fitting initialization, or a dynamic transaction-cost optimization. Costs are deducted after applying the frictionless target rule.

At 25 basis points proportional cost, switching incurs 0.25% when moving entirely between stocks and bills. The fractional strategy deducts $0.0025|w_t-w_{t-1}|$ under the paper's stated rule. A production implementation would distinguish prior target weights from the drifted pretrade stock weight, account for timing of cash flows, and specify whether stock-sale and bill-purchase costs are combined. Those details are not all documented here; the tabulated rule is the research convention.

| 1968:Q2-2002:Q4, after costs | Annual mean | Annual SD | Reported adjusted Sharpe | Annual CE gain |
|---|---:|---:|---:|---:|
| Buy-and-hold | 11.32% | 18.01% | 0.2873 | - |
| Switching, $cay$ | 13.63% | 14.22% | 0.6171 | 2.82% |
| Switching, $cay+v$ | 12.82% | 16.47% | 0.4369 | 1.72% |
| Switching, $cay+v+rrel$ | 13.15% | 15.62% | 0.5005 | 2.16% |
| Fractional, $cay$ | 11.41% | 12.34% | 0.5831 | 0.82% |
| Fractional, $cay+v$ | 13.35% | 14.56% | 0.5757 | 2.51% |
| Fractional, $cay+v+rrel$ | 13.63% | 14.59% | 0.5929 | 2.78% |

Before costs, the augmented fractional rule has annual mean 13.55%, SD 14.54%, adjusted Sharpe 0.5902, and CE gain 2.70%. The corresponding switching rule has 12.97%, 16.45%, 0.4471, and 1.88%. The magnitude-sensitive rule makes better use of the augmented signal, while the univariate signal actually wins among switching rules. This directly demonstrates why a forecast horse race depends on the allocation rule.

The paper's adjusted Sharpe first scales the managed return to the market's volatility and then computes a Sharpe measure. These reported figures should not be relabeled as a conventional excess-return Sharpe without reproducing the leverage/funding convention. Table 7 contains apparent arithmetic errors in the mean/SD row: for augmented $cay$, $0.1282/0.1647\approx0.7784$, not the printed 0.6917; with the rate, $0.1315/0.1562\approx0.8419$, not 0.7031. The note retains the mean, SD, and reported adjusted Sharpe as separate source statistics rather than using the erroneous ratios.

Subperiod performance varies. The largest market-timing improvements often occur in the 1970s. For the augmented fractional strategy before costs, adjusted Sharpe is 0.5140 in 1968:Q2-1979:Q4, 0.6158 in the 1980s, and 0.6217 in 1990:Q1-2002:Q4; market values are 0.0840, 0.4795, and 0.3354. Figures 7-8 show that weights remain at one through long stretches of the 1980s and 1990s, explaining modest modeled turnover. An initial \$100 grows to \$5,338 under switching and \$7,227 under the augmented fractional rule, versus \$2,793 for buy-and-hold, before the transaction-cost adjustment illustrated separately.

## Timing tests, alpha, welfare, and appendix

The Cumby-Modest test regresses realized market excess returns on a constant and the indicator that the model forecast is positive. A positive indicator coefficient means that forecast-positive states have higher realized returns. Table 10 reports coefficients 0.050 and 0.047 for $cay$ and augmented $cay$, with $t$ statistics 2.490 and 2.271. For the model including $rrel$, the printed coefficient is 0.448 with $t=2.453$. Visual inspection confirms 0.448; its magnitude is anomalous relative to the other columns. A value around 0.0448 might look plausible, but it is not an established correction and should not replace the printed result without original output.

Table 11's factor regressions use quarterly portfolio excess returns. The augmented fractional strategy's CAPM alpha before costs is 0.010 per quarter, $t=2.678$; its three-factor alpha is 0.008, $t=1.926$. After costs these become 0.009 ($t=2.542$) and 0.007 ($t=1.801$). Adding $rrel$ gives after-cost three-factor alpha 0.008 with $t=1.984$. Thus the unconditional CAPM rejects more clearly than the three-factor model; the statement that neither explains all managed returns should not be read as every three-factor alpha being significant. A timing rule can also create conditional beta variation that an unconditional regression fails to capture, so alpha is a benchmark-relative result, not proof of irrational pricing.

The welfare calculation uses the quadratic-return objective

$$
U=W_0\sum_t\left[R_{p,t+1}-\frac{\gamma}{2(1+\gamma)}R_{p,t+1}^2\right].
$$

The fee $\Delta$ is defined by replacing the managed return with $R_{mp,t+1}-\Delta$ and equating sample utility to buy-and-hold utility. Table 12 reports annualized gains. This is the source's particular certainty-equivalence exercise, not automatically the simpler $\mu-\gamma\sigma^2/2$ statistic used in other predictability papers. No standard errors or confidence intervals for the fee are supplied, and parameter uncertainty is not integrated into the investor's optimization.

The appendix confronts Brennan-Xia's observation that replacing consumption with calendar time gives a cointegration residual $tay$ that can rival $cay$. With both alone in the full-sample forecast, $cay$ has $t=1.801$ and $tay$ $t=1.749$. Adding variance raises $cay$'s $t$ to 2.969, leaves variance at 3.439, and reduces $tay$ to 0.999. Adding $rrel$ yields $t$ statistics 3.045, 3.312, -2.418, and 0.457 respectively. The two-quarter-lagged version likewise favors $cay$. Claimed out-of-sample superiority over augmented $tay$ is not tabulated. The appendix strengthens the partial-information argument but does not solve vintage revisions or generated-regressor uncertainty.

## Decision sensitivity and the fee calculation

The constrained allocation has three regimes. With positive variance forecast, a nonpositive expected excess return gives zero stock weight. A forecast above $\gamma\widehat v$ gives full stock weight. Only forecasts between those boundaries affect the position continuously. In that interior, the derivatives are $\partial w/\partial\widehat e=1/(\gamma\widehat v)$ and $\partial w/\partial\widehat v=-\widehat e/(\gamma\widehat v^2)$. These are derived implications of the stated rule. They explain why variance forecasting can matter economically even when return RMSE differences are small: the same return forecast produces a larger position when risk is lower, unless the upper constraint already binds.

They also explain why the economic comparison is not a pure test of the mean forecast. The switching rule has a discontinuity at zero and ignores risk magnitude. The fractional rule adds a variance forecast estimated from the same underlying market data. Its reported advantage combines forecast calibration, clipping, and volatility timing. Figure 8's long stretches at weight one imply that much of the unconstrained signal variation has no effect on realized holdings. Measuring an unconstrained information ratio would therefore not reproduce the reported utility ranking.

The quadratic fee can be solved without iterative optimization. Let $a=\gamma/[2(1+\gamma)]$, let $\mu_p$ and $q_p$ denote sample mean and second raw moment of the managed return under the paper's convention, and define $G=(\mu_p-aq_p)-(\mu_m-aq_m)$. Expanding the fee equation gives

$$
a\Delta^2+(1-2a\mu_p)\Delta-G=0.
$$

The economically relevant root is the one continuous at zero as $G\to0$ in the locally increasing-utility region. This derivation is useful for reproduction because applying a fee to a return changes both its first and second moments; subtracting the utility gap directly as a fee is only a first-order approximation. The source does not provide the unrounded return moments needed to reproduce its Table 12 fees exactly. Nor does the derivation remove the need to match the original return and annualization conventions.

## Replication boundary and research judgment

A faithful reconstruction needs the Lettau data vintage, exact dynamic-OLS design and endpoint handling, the 1987 variance correction, the short-rate moving-average convention, initial forecast observations, and precise portfolio compounding and Sharpe definitions. The source variously refers to 1952:Q2, Q3, or Q4 around initial estimation, so a replicator should reconcile effective observations after lagging rather than silently treat all those dates as identical. The paper provides no code, forecast series, bootstrap inference for utility gains, or trading-capacity analysis.

The strongest transferable result is methodological: assess correlated predictors jointly and evaluate them through an explicit portfolio rule. The strongest statistical qualifier is equally transferable: full-sample construction of a generated regressor can make a nominally out-of-sample exercise look far stronger than a recursive information set supports. The economic results justify further testing of the combination, but the paper itself does not establish a post-2002, vintage-correct, executable timing edge.

## Source map and related work

Tables 1-2 and Figures 1-4, pp. 648-652, document predictors and in-sample associations. Tables 3-5 and Figures 5-6, pp. 653-658, separate fixed and recursive forecast designs and nested inference. Tables 6-9 and Figures 7-8, pp. 659-665, define the two allocation rules and costs. Tables 10-12, pp. 666-668, contain timing, alpha, and fee results. Table A1, p. 669, tests $cay$ against $tay$.

The essential antecedents are Lettau and Ludvigson (2001), “Consumption, Aggregate Wealth, and Expected Stock Returns,” for $cay$; Guo (2004), “Limited Stock Market Participation and Asset Prices in a Dynamic Economy,” for the economic mechanism; Clark and McCracken and McCracken for nested forecast tests; Cumby and Modest (1987) for timing inference; and Fleming, Kirby, and Ostdiek (2001) for the welfare comparison. These references locate the article's contribution; the claims above are grounded in the supplied Guo source rather than an independent reanalysis of those works.

# Predicting returns with financial ratios

Jonathan Lewellen. *Journal of Financial Economics* 74 (2004), 209–235. DOI: 10.1016/j.jfineco.2002.11.002. Source: `Finance/PredictableReturns_Lewellen_2004.pdf`, 27 PDF pages. References below use journal pages; PDF page 1 is journal page 209. This note summarizes the supplied published article, including the statistical appendix, rather than an updated test on subsequent data.

## Research question and contribution

The paper asks whether aggregate valuation ratios predict stock returns once the unusual statistical behavior of persistent predictors is handled correctly. Dividend yield, book-to-market, and earnings-price ratios all combine slowly moving fundamentals with a volatile price denominator. An unexpected positive return therefore tends to coincide with an unexpected decline in the predictor. This creates a strong relation between estimation errors in the predictive-return regression and estimation errors in the predictor's autoregression. Conventional small-sample corrections acknowledge that relation but normally integrate over every possible realization of the estimated autoregressive coefficient.

Lewellen's contribution is to use information in the *observed* autoregressive coefficient. If the true predictor persistence cannot exceed one, and its estimated persistence is already close to one, the sample's downward persistence error cannot be very large. Consequently, the upward error in the estimated return-prediction coefficient cannot be very large either. A correction based on the unconditional average bias can then remove far too much of the estimated predictive relation. Conditioning also removes a large source of uncertainty, reducing the relevant standard error.

The main empirical finding is particularly sharp for dividend yield. With monthly NYSE value-weighted returns over 1946–2000, the ordinary least-squares slope is 0.917, a conventional Stambaugh correction reduces it to 0.196, but the new conservative conditional estimate is 0.663. The respective one-sided significance levels are 0.027, 0.308, and below the table's three-decimal reporting threshold. Thus a sample that appears unconvincing under the familiar bias correction can reject constant expected returns strongly under an economically motivated persistence bound.

This is primarily an inference paper. It does not propose a new trading signal, demonstrate profitable market timing after transaction costs, or identify whether predictable returns represent rationally varying risk compensation or mispricing. Both economic interpretations can generate a positive relation between valuation ratios and subsequent returns. Its innovation is the construction and interpretation of a more informative statistical experiment.

## Model and source of the bias

The maintained model, equations (3a)–(3b), is

$$
r_t=\alpha+\beta x_{t-1}+\varepsilon_t,
$$

$$
x_t=\phi+\rho x_{t-1}+\mu_t.
$$

Here $r_t$ is the return in month $t$ and $x_{t-1}$ is information available before that month. The principal predictor is the natural logarithm of the dividend yield. The alternative is directional: high valuation ratios should predict high returns, so tests concern $\beta>0$. The predictor is modeled as a stationary first-order autoregression, with $\rho<1$. The statistical construction remains valid at $\rho=1$, although the paper generally states stationarity to match earlier research and its economic interpretation. Gaussian disturbances make the exact conditional distribution available.

The crucial nuisance parameter is the relation between contemporaneous shocks. Define

$$
\gamma=\frac{\operatorname{Cov}(\varepsilon_t,\mu_t)}{\operatorname{Var}(\mu_t)},\qquad
\varepsilon_t=\gamma\mu_t+\nu_t.
$$

Since unexpected price increases lower valuation ratios, $\gamma$ is negative. Under the Gaussian assumptions, the residual $\nu_t$ is independent of the predictor innovations, hence of the entire sequence of predictor observations. This produces the estimation-error identity

$$
\widehat\beta-\beta=\gamma(\widehat\rho-\rho)+\eta,
$$

where $\eta$ has conditional mean zero and a variance determined by $\sigma_\nu^2$ and the regressor matrix. The familiar downward bias in estimated persistence, approximately $-(1+3\rho)/T$, creates an upward bias in the return-prediction slope because it is multiplied by negative $\gamma$. The same identity explains positive skewness and unusually high variance of the predictive coefficient: these are inherited from the nonstandard finite-sample behavior of autoregressive estimates.

A conventional correction uses

$$
E[\widehat\beta-\beta]=\gamma E[\widehat\rho-\rho].
$$

That is an average over hypothetical samples. It does not answer what the bias can be in the sample actually observed. If $\widehat\rho=0.99$ and $T=300$, the approximate unconditional persistence bias is about $-0.016$. Yet the bound $\rho\leq1$ implies that the realized persistence error cannot be below $-0.010$. Subtracting the full unconditional bias from the estimated predictive slope can therefore be excessively pessimistic.

The argument does not say that the Stambaugh distribution is wrong. Lewellen repeatedly states that it is generally appropriate. The improvement arises because an additional economically defensible restriction becomes particularly informative in samples with unusually high observed persistence. When the estimate is far below one, the upper bound supplies little information and the conditional method may be inferior.

## Conditional estimator and exact implementation

For a specified true persistence, the adjusted estimator is

$$
\widehat\beta_{\mathrm{adj}}(\rho)=\widehat\beta-\gamma(\widehat\rho-\rho).
$$

If $\rho$ were known, this would remove the problematic part of the sampling error. With $\gamma<0$, the smallest adjusted slope permitted by $\rho\leq1$ occurs at the upper boundary. The empirical tables implement that boundary as $\rho=0.9999$. If the true persistence is lower, this choice understates the predictive coefficient. The resulting statistic tests a conservative lower bound; it is not an ordinary symmetric confidence interval around a point estimate of the unrestricted economic effect.

The appendix gives a practical regression representation that automatically handles estimation of $\gamma$ and the innovation variance. For the chosen $\rho_0$, construct $z_t=x_t-\rho_0 x_{t-1}$, then estimate

$$
r_t=a+b x_{t-1}+g z_t+v_t.
$$

The coefficient $b$ equals the conditional adjusted slope. The unknown autoregressive intercept is absorbed by $a$. The usual regression standard error on $b$ is the appropriate one under the maintained model, and its null statistic has a Student distribution with $T-3$ degrees of freedom. This representation is more reliable for replication than estimating the two equations separately and informally combining standard errors.

The appearance of $x_t$ in this auxiliary regression does not create a deployable forecasting rule that uses future information. It is an inference device exploiting the joint distribution of returns and predictor innovations. An investor at the end of $t-1$ cannot know $z_t$. Conflating the augmented test regression with a live predictor would turn a valid statistical construction into a look-ahead-biased trading strategy.

The appendix also checks a subtle issue: when $\gamma$ must be estimated, the standard error varies slightly with the assumed persistence. A lower coefficient alone would not automatically imply the most conservative $t$-statistic. Lewellen derives the relevant variance and shows that the boundary remains conservative under conditions satisfied in the application. In the full-sample value-weighted regression, the estimate of $\gamma$ is approximately $-90.4$ with standard error 1.1, so its negative sign is overwhelmingly clear. The statistic for that sign is about 82.1, much larger than the statistic for return predictability.

## Choosing between tests without overstating significance

The conditional and unconditional tests have different power functions. It would be invalid to examine both, keep whichever rejects more strongly, and report its significance as if no choice had occurred. Section 2.4 therefore discusses joint inference. A safe simple adjustment doubles the smaller standalone $p$-value, using Bonferroni's inequality.

The proposed refinement is

$$
p_{\mathrm{joint}}=\min(2P,P+D),
$$

where $P$ is the smaller standalone significance level and $D$ is the significance level of a unit-root test based on the sampling distribution of $\widehat\rho$. If estimated persistence is far from one, the boundary test contributes little and doubling the unconditional significance level is unnecessarily conservative. If persistence is very close to one, ordinary Bonferroni protection is retained.

An important qualification is that the paper does not provide a general proof for every intermediate persistence value. It proves limiting cases and supports the proposed bound with calibrated simulations. The reported rejection frequency remains at or below the nominal 5% level over persistence values from 0.9 to 0.9999. A replication should distinguish this simulation-supported refinement from the ordinary Bonferroni bound, whose validity does not depend on the intermediate-case argument. The main dividend-yield conclusions survive simple doubling, so their strength does not depend on accepting the tighter formula.

## Data and experimental design

Prices, dividends, and NYSE index returns come from CRSP. Book equity and operating earnings come from Compustat. The indices are restricted to NYSE firms to preserve consistency with earlier research and avoid changes in market composition as AMEX and NASDAQ firms enter the database. Both equal-weighted and value-weighted NYSE returns are tested, but all predictors are constructed for the value-weighted market. An equal-weighted dependent return is therefore not paired with an equal-weighted valuation ratio.

Dividend yield equals dividends paid during the preceding year divided by the current index level. It is a rolling annual-dividend measure observed monthly. The regressions use its logarithm. This reduces skewness and the mechanical dependence of the raw ratio's volatility on its level. A change from percentage units to decimal units inside the logarithm changes the intercept, not its slope, but return units must remain explicit: the reported return coefficients use monthly returns in percent.

The principal sample is January 1946 through December 2000, or 660 months. The Depression era is omitted because pre-1945 return volatility and predictor persistence differ materially. Separate samples cover 1946–1972, with 324 months, and 1973–2000, with 336 months. A further experiment truncates the data at December 1994, yielding 588 months, to assess the influence of the unusual late-1990s market rise.

Book-to-market and earnings-price tests begin in June 1963 because of Compustat availability. The full accounting sample has 451 months through December 2000; its truncated counterpart has 379 months through December 1994. Book equity and earnings are taken from the previous fiscal year and are not updated until four months after fiscal year-end. A firm must have three years of accounting history before entering the sample, a precaution against selection issues in the historical accounting database.

Earnings are operating earnings before depreciation rather than bottom-line net income. This choice matters both numerically and conceptually. The average earnings-price ratio is roughly 20%, which should not be read as an ordinary net-income yield. The corresponding net-income yield averages about 7%. Operating earnings are chosen because their innovations are less noisy and more closely related to market returns. The paper reports that results using net income are similar but marginally weaker; it does not present every alternative table.

The dependent variables are nominal total returns and excess returns above the one-month Treasury bill rate. Regressions predict a single month and do not use overlapping long-horizon returns. This deliberately removes a separate source of inference difficulty. The experiment does not pool markets, include macroeconomic controls in the main tables, or evaluate a multivariable forecasting contest.

## Descriptive evidence and full-sample results

Table 1 documents the conditions that make the proposed method relevant. Monthly value-weighted NYSE returns average 1.04% with standard deviation 4.08%; equal-weighted returns average 1.11% with standard deviation 4.80%. Dividend yield averages 3.80% with standard deviation 1.20 percentage points. Its logarithm has standard deviation 0.33 and first-order persistence 0.997. The raw yield is slightly less persistent, at 0.992. Log book-to-market and log earnings-price have persistence 0.995 and 0.990, respectively.

Table 2 shows that the dividend-yield autoregression has innovation standard deviation 0.043. Its innovations correlate with nominal value-weighted return innovations at $-0.955$, and with equal-weighted return innovations at $-0.878$. These exceptionally negative correlations make knowledge about persistence especially useful. A method applied to a predictor with weakly correlated innovations would gain much less from conditioning.

| Monthly return series | OLS slope | Conventional adjusted slope | Conditional adjusted slope | Conditional standard error |
|---|---:|---:|---:|---:|
| Value-weighted nominal | 0.917 | 0.196 | 0.663 | 0.142 |
| Equal-weighted nominal | 1.388 | 0.615 | 1.115 | 0.268 |
| Value-weighted excess | 0.915 | 0.192 | 0.661 | 0.145 |
| Equal-weighted excess | 1.387 | 0.611 | 1.112 | 0.268 |

All four conditional significance levels are reported as 0.000, meaning rounded values rather than literal zero probabilities. Conventional corrected significance levels range from 0.183 to 0.311. The result comes from both a smaller subtraction for bias and a much smaller standard error. For value-weighted nominal returns, the conventional adjusted standard error is 0.670, versus 0.142 conditionally.

Economic and statistical significance must be kept separate. The OLS coefficient and log-yield standard deviation imply a roughly 0.30-percentage-point variation in expected monthly returns for a one-standard-deviation predictor change. The conservative conditional estimate implies approximately 0.22 percentage point. Yet the ordinary regression's adjusted $R^2$ is only 0.004 for value-weighted returns and 0.008 for equal-weighted returns. A small fraction of unpredictable monthly volatility is removed even though the hypothesis of no predictable component is rejected strongly.

## Subperiods and the late-1990s stress test

Table 3 is useful because it avoids presenting the full-sample result as homogeneous across return definitions. For 1946–1972, the conditional nominal value-weighted slope is 0.844, with significance level 0.001, but the nominal equal-weighted slope is only 0.425, with significance level 0.152. Excess-return slopes are 1.156 and 0.736, with significance levels 0.000 and 0.037. Thus the first-half equal-weighted nominal specification does not reject at conventional levels.

For 1973–2000, conditional slopes are 0.641 for nominal value-weighted returns and 1.608 for nominal equal-weighted returns. Both are strongly significant. Excess-return slopes are 0.304 and 1.271; the value-weighted excess result is weaker, with a standalone significance level of 0.041. The distinction matters if a reader applies an additional joint-test correction. The paper's statement of strong overall evidence should not be converted into a claim that every individual subperiod specification is overwhelming.

The most counterintuitive result concerns 1995–2000. Dividend yield fell from about 2.9% in January 1995 to 1.5% in December 2000 while the value-weighted index nearly doubled. A model linking low yields with low subsequent returns performed poorly during that episode. Adding these observations cuts the OLS value-weighted coefficient from 2.230 to 0.917. Conventional adjusted significance deteriorates from 0.068 to 0.308.

The conditional coefficient falls more modestly, from 0.980 to 0.663, and its statistic remains around 4.8 and 4.7. Estimated yield persistence rises from 0.986 to 0.997. The maximum admissible upward bias in the predictive slope therefore falls from approximately 1.25 to 0.25. Of the 1.31 decline in the OLS slope, about 1.00 is attributed to the changed sampling error connected to persistence. For equal-weighted returns, the conditional estimate actually rises, from 1.031 to 1.115.

This does not rehabilitate the realized late-1990s forecast performance. It changes the inferential interpretation of that performance under the maintained joint model. The same unusually large price increase both lowers the predictive coefficient and raises predictor persistence. Treating the first effect as evidence against predictability while ignoring the second throws away information. Nevertheless, an investor cares about the realized forecasting loss, so this distinction is crucial when translating the paper into allocation decisions.

## Book-to-market and earnings-price evidence

Tables 5 and 6 show a less uniform result for accounting ratios. For 1963–1994, the conditional book-to-market slopes for nominal value-weighted and equal-weighted returns are 0.731 and 1.107, with standalone significance levels 0.017 and 0.022. For 1963–2000, they become 0.276 and 1.032, with significance levels 0.149 and 0.005. The extended sample supports prediction of the equal-weighted index much more clearly than the value-weighted index.

Book-to-market does not convincingly predict value-weighted excess returns in either accounting sample. In the full period its conditional slope is $-0.075$, while the equal-weighted excess slope is 0.681 with significance level 0.047. These results should not be summarized as universal support for a market value-timing strategy. They suggest that aggregation and the risk-free-rate adjustment affect the conclusion materially.

For earnings-price, conditional nominal slopes over 1963–2000 are 0.403 for the value-weighted index and 0.983 for the equal-weighted index. Their standalone significance levels are 0.088 and 0.012. A one-standard-deviation earnings-price change corresponds to about 0.14 and 0.34 percentage point in expected monthly nominal returns. Excess-return evidence is weaker: the full-sample value-weighted coefficient is effectively zero, and the equal-weighted coefficient has significance level 0.093.

Conditional inference consistently looks more favorable than the conventional correction, but the method cannot manufacture equally strong economic content across predictors. Earnings and book values can contain different information from dividends, their innovation correlations with returns are less extreme, and their samples are shorter. The paper appropriately concludes that their forecasting power is limited relative to the dividend-yield evidence.

## Simulation evidence and power trade-off

The appendix calibrates simulations to the 1946–1972 value-weighted dividend-yield regression. It considers predictive slopes from zero to 1.6 in increments of 0.4, and persistence from 0.999 down to 0.975 in increments of 0.002. Table A.1 uses 5,000 simulations. Figure 1 separately illustrates the marginal and joint coefficient distributions with 20,000 and 2,000 simulations, respectively, using $T=300$, $\rho=0.99$, zero predictive slope, disturbance correlation $-0.92$, return disturbance standard deviation 0.04, and predictor disturbance standard deviation 0.002.

At a true slope of 1.2, conditional-test power is 91.4% when persistence is 0.999, 50.0% at 0.993, and only 3.2% at 0.985. The corresponding conventional test has power around 13–15% across these cases. The conditional procedure is powerful near the boundary but can become almost useless when its deliberately pessimistic persistence assumption is far from reality.

For a slope of 1.6 and persistence 0.993, conditional power is 80.8%, compared with 18.9% conventionally; the joint procedure achieves 76.9%. At smaller persistence, the joint procedure retains some power from the unconditional test when the conditional procedure loses almost all of it. Under zero predictability, the conditional and proposed joint tests tend to under-reject, consistent with their conservative construction. This is the substantive reason to retain both tests rather than declaring one universally superior.

## Replication boundaries and interpretation

A faithful replication should first reproduce the observation counts, return units, accounting lags, NYSE aggregation, and predictor persistence. It should then estimate both original equations, retain their residual covariance, run the augmented regression at 0.9999, and compare all coefficient and standard-error entries in Tables 2–6. The conditional test can be implemented with ordinary regression software; reproduction of the conventional finite-sample comparator and modified joint significance requires simulation of the joint return-predictor process.

The article specifies economic definitions and timing but does not supply a complete executable data-construction program, database vintage, random seed, or every accounting mapping in the text. Modern CRSP and Compustat revisions may therefore prevent exact numerical equality. Historical accounting availability, dividend aggregation, and whether returns are represented in percentages must be audited before interpreting deviations as failures of the statistical result.

The central limitation is the maintained persistence bound and joint process. Changes in payout policy, permanent shifts in mean valuation ratios, heteroskedasticity, non-Gaussian disturbances, or richer predictor dynamics can complicate the exact distribution. Lewellen argues that a permanent fall in discount rates is itself evidence of varying expected returns, but that does not eliminate every possible structural-break concern. The paper also notes sensitivity to the sample start and to using raw instead of log dividend yield, particularly when predicting excess returns.

The durable takeaway is that inference about return predictability should use the relationship between the forecast regression and the predictor's own dynamics. A persistence estimate is not merely an ancillary diagnostic. When predictor and return shocks are closely linked, it changes what coefficient estimates can plausibly arise under the null. The result supports a predictable component in historical aggregate returns under an explicit model, while leaving the design, stability, and economic value of a live allocation strategy as separate empirical questions.

## Further technical distinctions useful for implementation

The difference between conditional and marginal uncertainty deserves explicit treatment when results are passed into another model. Let $X$ contain the intercept and lagged predictor. If $\gamma$ and the true persistence were known, the conditional variance of the adjusted slope would be

$$
\operatorname{Var}(\widehat\beta_{\mathrm{adj}}\mid X)=\sigma_\nu^2[(X'X)^{-1}]_{22}.
$$

The relevant innovation variance is the variance left after projecting return shocks onto predictor shocks, not the full return-innovation variance. If their correlation is $c$, the residual variance is $\sigma_\varepsilon^2(1-c^2)$. With correlation near $-0.955$, this fraction is roughly 0.088. That calculation explains why a substantial reduction in conditional standard error is possible without increasing the number of months. It is an explanation derived from the model, not a substitute for the appendix's regression standard error once $\gamma$ is estimated.

Conditioning technically involves the regressor realization as well as the estimated persistence. Conditioning only on $\widehat\rho$ leaves a mixture over different regressor variances; treating that mixture as one normal distribution would be imprecise. The augmented regression provides a straightforward implementation of the correct conditioning and avoids having to manipulate that mixture explicitly. Its residuals are unchanged by shifting the assumed persistence because changing $\rho_0$ adds a multiple of $x_{t-1}$ to the other regressor. Coefficients change in a controlled manner even though the fit is identical.

Another distinction concerns what the conservative estimate measures. The boundary estimate has expectation $\beta-\gamma(\rho-1)$ when the true persistence is below one. Since both $\gamma$ and $\rho-1$ are negative, their product is positive and the estimated slope is biased downward. It is therefore inappropriate to treat the conditional coefficient as an unbiased forecast parameter and simultaneously treat its small conditional standard error as complete uncertainty about the economic slope. The paper uses it to reject a null robustly over an admissible persistence region, not to eliminate parameter uncertainty in portfolio optimization.

Finally, the comparison with Bayesian methods is narrower than an equivalence of philosophies. A point prior at unit persistence reproduces the boundary calculation under a diffuse prior for the predictive coefficient. Allowing posterior weight on lower persistence usually strengthens evidence for a positive slope, but the result depends on beliefs and integration over the persistence distribution. The frequentist construction avoids choosing those beliefs by adopting the most pessimistic boundary. This is why it can be transparent and conservative while also wasting substantial power when true mean reversion is faster. The practical choice is between different uses of information and different inferential targets, not between a corrected estimator and an uncorrected estimator alone.

# Risk, Return, and Equilibrium: Empirical Tests

Eugene F. Fama and James D. MacBeth. *Journal of Political Economy* 81(3), May–June 1973, 607–636. Source: [CAPMtest_FamaMcBeth_1973.pdf](../../Finance/CAPMtest_FamaMcBeth_1973.pdf), 31 PDF pages including the archive cover. All pages, the appendix, and the rotated empirical tables were inspected. References below use printed journal pages. The title and original PDF basename identify the work.

## Why this matters

The paper turns an equilibrium restriction on unobservable expected returns into a sequence of measurable monthly cross-sectional regressions. Its lasting methodological contribution is to estimate prices of risk separately each month and use the time series of those estimates for inference. It also designs portfolio formation and beta estimation to reduce errors-in-variables problems without using future returns to construct explanatory variables.

The economic conclusion is more qualified than “the CAPM passes.” In this NYSE sample, the authors find a positive average reward for market beta, no compelling average curvature in the beta–return relation, and no compelling additional average premium for residual risk. But the stronger Sharpe–Lintner restriction equating the zero-beta expected return with the Treasury-bill rate does poorly. Moreover, coefficients associated with curvature and residual risk fluctuate through time more than pure estimation noise would predict, even when their averages are close to zero.

Those findings separate three questions that are often conflated: whether mean returns are approximately linear in beta; whether the intercept equals a known riskless rate; and whether one market factor captures the covariance of realized returns. The paper can support the first proposition while challenging the latter two. A replicator should preserve these distinctions rather than use one omnibus “CAPM” label for every specification.

## From efficient portfolios to testable restrictions

Sections I–II derive the pricing relation from portfolio efficiency. Investors are price takers, transactions and information are costless, and investors are risk averse. The exposition uses normally distributed returns, while discussing an extension to symmetric stable distributions. Homogeneous correct expectations and unrestricted short selling provide conditions under which the market portfolio is efficient in Black's equilibrium. Riskless borrowing and lending are an additional assumption, introduced separately.

For an efficient portfolio $m$, write $\sigma_m$ for its return standard deviation and $S_m$ for the local slope of the expected-return–standard-deviation frontier. The first-order portfolio-efficiency condition gives

$$
E[R_i]=E[R_m]-S_m\sigma_m+S_m\sigma_m\beta_i,
\qquad
\beta_i=\frac{\operatorname{Cov}(R_i,R_m)}{\operatorname{Var}(R_m)}.
$$

Define the zero-beta expected return $E[R_0]=E[R_m]-S_m\sigma_m$. Then the familiar relation is

$$
E[R_i]=E[R_0]+\beta_i\{E[R_m]-E[R_0]\}.
$$

The risk of an asset is its contribution to portfolio dispersion, not its stand-alone variance. In particular, zero beta means zero covariance with the reference portfolio, not a constant payoff. Without unrestricted riskless borrowing and lending, the zero-beta expected return need not equal the Treasury-bill rate.

The paper extracts three restrictions. C1 says the expected-return relation is linear in beta. C2 says beta is sufficient for the relevant risk premium; another risk measure should not earn a separate average reward. C3 says the expected premium per unit beta is positive for risk-averse investors holding the efficient market portfolio. The Sharpe–Lintner restriction adds $E[R_0]=R_f$.

To test these statements with realized returns, equation (7) introduces stochastic monthly coefficients:

$$
R_{it}=\gamma_{0t}+\gamma_{1t}\beta_i
       +\gamma_{2t}\beta_i^2+\gamma_{3t}s_i+\eta_{it}.
$$

Here $s_i$ is a risk measure not deterministically fixed by beta. The mean restrictions are $E[\gamma_{2t}]=0$, $E[\gamma_{3t}]=0$, and $E[\gamma_{1t}]>0$. The nonlinear and residual-risk coefficients need not equal zero in every realized month. The disturbances have mean zero and are assumed independent of the other components in the stochastic model. The normal or stable formulation requires the relevant random coefficients and disturbances to have compatible joint distributions.

This stochastic formulation is an essential innovation. A factor can contribute to realized return variation while having zero average price. Testing whether its coefficient is identically zero is therefore different from testing whether its expected coefficient is zero. The paper investigates both hypotheses with different statistics.

## Universe, calendar, and three separate data windows

The source data are CRSP monthly returns on all NYSE common stocks, January 1926–June 1968. Returns include dividends and capital gains and are adjusted for splits, stock dividends, and related capital changes. The market proxy is Fisher's Arithmetic Index, an equally weighted return on stocks listed on the NYSE that month. It is not the later conventional value-weighted CRSP market factor. The riskless rate used in the Sharpe–Lintner tests is the one-month Treasury-bill yield.

The test months run from January 1935 through June 1968, or 402 monthly cross sections. Nine portfolio-formation cycles are used. Each cycle separates three tasks: ranking securities, estimating explanatory variables, and observing subsequent returns. The first ranking window is only four years because the data begin in 1926; later ranking windows are seven years. Initial beta-estimation windows are five years. Most test blocks last four years; the last lasts eighteen months.

| Ranking window | Initial estimation window | Test window | Available stocks at start | Eligible stocks |
|---|---|---|---:|---:|
| 1926–1929 | 1930–1934 | 1935–1938 | 710 | 405 |
| 1927–1933 | 1934–1938 | 1939–1942 | 779 | 576 |
| 1931–1937 | 1938–1942 | 1943–1946 | 804 | 607 |
| 1935–1941 | 1942–1946 | 1947–1950 | 908 | 704 |
| 1939–1945 | 1946–1950 | 1951–1954 | 1,011 | 751 |
| 1943–1949 | 1950–1954 | 1955–1958 | 1,053 | 802 |
| 1947–1953 | 1954–1958 | 1959–1962 | 1,065 | 856 |
| 1951–1957 | 1958–1962 | 1963–1966 | 1,162 | 858 |
| 1955–1961 | 1962–1966 | 1967–June 1968 | 1,261 | 845 |

Table 1, pp. 618–619, supplies this calendar and the eligibility counts. A stock available in the first test month must have data for all five preceding estimation years and at least four years of the ranking window. This excludes recent listings and securities with inadequate histories; it is not the same as requiring survival until the end of the test block. Delistings during a test block change the membership used in monthly averages.

For a cycle with $N$ eligible stocks, rank individual beta estimates from the ranking window and form 20 portfolios. Let $q=\lfloor N/20\rfloor$ and $r=N-20q$. Each of the middle 18 portfolios has $q$ stocks. The low-beta portfolio has $q+\lfloor r/2\rfloor$, and the high-beta portfolio receives $q+\lceil r/2\rceil$. Thus any indivisible extra stock goes to the high-beta extreme. The design preserves a wide beta range instead of using random portfolios, which would concentrate exposures near one.

The reason for the separate ranking window is selection on estimation noise. If portfolios are ranked and measured with the same noisy betas, extreme estimated betas also select extreme errors. Averaging those securities does not remove the selection bias. Reestimating betas with fresh subsequent data makes within-portfolio errors less systematically aligned with the original sort. This mitigates the problem; it does not prove that every errors-in-variables bias disappears.

## Exact construction of the monthly regressors

For every eligible stock, estimate the market model over the initial five-year estimation window:

$$
R_{i\tau}=a_i+\beta_i R_{m\tau}+\epsilon_{i\tau},\qquad
\hat\beta_i=\frac{\widehat{\operatorname{Cov}}(R_i,R_m)}{\widehat{\operatorname{Var}}(R_m)}.
$$

Record the residual standard deviation $s(\hat\epsilon_i)$. It is the selected proxy for non-beta risk. Under the population regression orthogonality condition,

$$
\operatorname{Var}(R_i)=\beta_i^2\operatorname{Var}(R_m)+\operatorname{Var}(\epsilon_i).
$$

The paper displays the more general expansion including the covariance term, which vanishes when beta is the population market-regression coefficient. Residual standard deviation is therefore associated with the part of total volatility not directly accounted for by beta, but it is not necessarily statistically independent of beta across stocks.

Within portfolio $p$, the first regressor is the arithmetic average of individual estimated betas. The second is the arithmetic average of **individual squared estimated betas**. The third is the arithmetic average of individual residual standard deviations:

$$
b_{pt}=\frac{1}{N_{pt}}\sum_{i\in p,t}\hat\beta_i,
\qquad
c_{pt}=\frac{1}{N_{pt}}\sum_{i\in p,t}\hat\beta_i^2,
\qquad
s_{pt}=\frac{1}{N_{pt}}\sum_{i\in p,t}s(\hat\epsilon_i).
$$

The paper labels the second object as portfolio beta squared but explicitly warns that this notation is misleading. In general $c_{pt}\ne b_{pt}^2$. Their difference is the within-portfolio cross-sectional variance of estimated individual betas, using the corresponding population divisor. Similarly, $s_{pt}$ is not the standard deviation of the portfolio's market-model residual. Replacing either regressor with its superficially similar portfolio statistic changes the test.

The first test year uses the initial five-year estimates. Estimates are updated annually using expanding windows within the cycle: for the first cycle, January–December 1936 uses 1930–1935 data, 1937 uses 1930–1936, and 1938 uses 1930–1937. Thus estimation histories become six, seven, and eight years. The estimates are not refit every month and are not rolling fixed-five-year windows. Portfolio averages do change monthly to reflect delistings. The next cycle reforms portfolios using its own ranking window.

Portfolio returns are equal-weighted across constituent securities each month. All explanatory estimates precede the month whose returns are regressed. This predictive timing is central: a normative portfolio model has practical content only if risk estimates available to an investor bear some relationship to subsequent returns.

For each test month, estimate by OLS across the 20 portfolios:

$$
R_{pt}=\hat\gamma_{0t}+\hat\gamma_{1t}b_{p,t-1}
 +\hat\gamma_{2t}c_{p,t-1}+\hat\gamma_{3t}s_{p,t-1}+\hat\eta_{pt}.
$$

Table 3 reports four nested specifications: A includes beta only; B includes beta and the squared-beta average; C includes beta and residual-risk average; D includes all three. Each has an intercept. The dependent variable is the raw stock return, not a market-adjusted or excess return. The riskless rate is used afterward to assess the intercept restriction.

## Time-series inference: what is averaged and what is not

For each coefficient $j$ and a test period of $T$ months, form

$$
\bar\gamma_j=\frac{1}{T}\sum_{t=1}^T\hat\gamma_{jt},\qquad
s_j^2=\frac{1}{T-1}\sum_{t=1}^T(\hat\gamma_{jt}-\bar\gamma_j)^2,
\qquad t_j=\frac{\bar\gamma_j}{s_j/\sqrt T}.
$$

The uncertainty comes from month-to-month variation in estimated prices of risk. One must not pool all portfolio-month observations and then use an ordinary independent-observation standard error, nor replace this standard error with the average of monthly cross-sectional standard errors. Those monthly cross-sectional errors serve a different purpose in Table 5.

The paper checks first-order and higher-order serial correlations of coefficient and residual series. For restrictions requiring a zero mean, it sometimes calculates serial correlations about zero; for the beta premium it uses the sample mean as a proxy for a constant expected premium. Approximate standard errors of serial correlations are $1/\sqrt T$, about 0.05 for the whole sample, 0.09 for decade-scale blocks, and 0.13 for five-year blocks. These checks support the authors' fair-game interpretation but do not constitute a modern omnibus test of conditional mean independence.

The reported t-statistics use the simple time-series formula above, not a Newey–West adjustment or a later Shanken correction. An updated replication could add such inference, but it would be an additional analysis rather than a literal reconstruction of the 1973 tables. Serial dependence, persistent estimated exposures, and estimated-regressor errors are relevant reasons to distinguish the historical statistic from a generally valid standard error in a new application.

The paper discusses fat tails at length. It cites evidence for return distributions approximated by symmetric stable laws with characteristic exponent around 1.8, while also entertaining finite-variance distributions with slow normal convergence. These are different probabilistic cases. A genuinely stable law with exponent below two does not have a finite population variance, so ordinary variance-based asymptotic reasoning cannot simply be imposed without qualification. The authors use t-statistics as approximate evidence and caution against overly literal tail probabilities. A modern reader should preserve that qualification rather than regard their normal reference distribution as exact.

## Main numerical findings

The full-sample values below come from Table 3, pp. 622–623. Returns are expressed as decimals in the original table; percentages here are monthly percentage points. The residual-risk coefficient is left in its original units because it multiplies a residual standard deviation expressed as a decimal return.

| Specification | Mean intercept | Mean beta premium | Beta-premium t | Mean quadratic coefficient | Quadratic t | Residual-risk coefficient | Residual-risk t |
|---|---:|---:|---:|---:|---:|---:|---:|
| A: beta | 0.61% | 0.85% | 2.57 | — | — | — | — |
| B: beta, quadratic | 0.49% | 1.05% | 1.79 | −0.08% | −0.29 | — | — |
| C: beta, residual risk | 0.54% | 0.72% | 2.20 | — | — | 0.0198 | 0.46 |
| D: all three | 0.20% | 1.14% | 1.85 | −0.26% | −0.86 | 0.0516 | 1.11 |

The evidence for a positive beta premium is most precise in the parsimonious specification. It is weaker after collinear regressors are included; the full model's t-statistic of 1.85 should not be described as an overwhelming rejection at conventional two-sided levels. The nonlinear and residual-risk means are small relative to their sampling variation. Full-sample average adjusted monthly cross-sectional $R^2$ is 0.29, 0.32, 0.32, and 0.34 for A–D respectively. This is the average of monthly adjusted fits, not the fit of a regression of average returns on average betas.

Subperiod estimates explain why long samples are needed. In 1935–1940, the beta-only average premium is 1.09% per month, but the monthly coefficient standard deviation is 11.6%, yielding a t-statistic of only 0.79. A large economically interesting mean can coexist with little statistical precision. The 1956–1960 beta-only premium is −0.59% per month with t-statistic −1.37. Thus the paper's positive full-period result is not a claim that realized beta premia are always positive.

One curvature exception is 1951–1955: the quadratic-only augmentation produces a coefficient t-statistic around −2.72. The full-model quadratic statistic is about −2.54 in that interval. The authors emphasize that neighboring or overlapping subperiod results are not independent pieces of evidence. The aggregate result is nonrejection of an average linear relation, with some episodic realized nonlinearities.

Portfolio aggregation materially improves exposure precision. Table 2 compares residual volatility of portfolios with the average residual volatility of their constituent stocks. The ratio is generally between roughly one-third and one-seventh, implying a similar proportional reduction in beta standard errors under the stated market-regression assumptions. The improvement is weaker in extreme-beta portfolios. For 1950–1954, estimated portfolio betas range from 0.418 to 1.527; the corresponding low- and high-end standard errors are approximately 0.042 and 0.086. These values show both the useful exposure spread and the remaining measurement uncertainty.

## The zero-beta rate and the stronger CAPM rejection

Table 4 reports a mean market return of 1.43% per month for 1935–June 1968, a mean Treasury-bill rate of 0.13%, and hence a mean market premium of 1.30%. The beta-only cross-sectional premium is 0.85%, while its mean intercept is 0.61%. The mean intercept exceeds the bill rate by 0.48% per month, with t-statistic 2.55. This rejects the additional riskless-borrowing-and-lending restriction more clearly than it rejects the broader linear beta relation.

The distinction has a geometric interpretation. In the one-regressor specification, averaging the OLS fitted relation across portfolios approximately gives

$$
\hat\gamma_{1t}\simeq R_{mt}-\hat\gamma_{0t}.
$$

This is approximate because the eligible test portfolios do not contain every stock in the market index and their average beta is not exactly one. The paper explicitly notes this approximation in footnote 9. The intercept itself is the realized return on a portfolio whose weights sum to one and whose estimated beta is zero. Under additional Gauss–Markov assumptions on cross-sectional disturbances it is the minimum-variance zero-beta portfolio among the 20 portfolios. Without those assumptions, the linear-combination interpretation remains, but minimum variance is not guaranteed.

Adding quadratic and residual-risk regressors raises the intercept's sampling error markedly. It also changes which zero-beta portfolio the intercept represents: the full-model intercept portfolio must additionally have zero exposure to the squared-beta and residual-risk regressors. Since these constraints involve positive characteristics, the portfolio can require substantial offsetting positive and negative weights. Its return need not resemble the simpler intercept portfolio.

The authors expose a parameterization problem by replacing $\beta_i^2$ with $(1-\beta_i)^2$. The fitted model span does not change, but

$$
\gamma_{0t}=\gamma'_{0t}+\gamma_{2t},\qquad
\gamma_{1t}=\gamma'_{1t}-2\gamma_{2t}.
$$

A test that treats either regression constant by itself as the economically appropriate zero-beta return can therefore change despite identical fitted returns. Once nonlinear terms are admitted, the economically relevant restriction must be mapped through the parameterization. The paper regards the simple beta-only specification as providing its most precise available test of the Sharpe–Lintner intercept, while acknowledging the ambiguity in the augmented models.

## Realized common variation and the appendix's factor interpretation

Table 5 separates total monthly coefficient variance from estimated cross-sectional sampling variance. For coefficient $j$, let $v_{jt}$ be the monthly OLS variance estimate and $\bar v_j=T^{-1}\sum_t v_{jt}$. The estimated variance of the underlying stochastic coefficient is

$$
\widehat{\operatorname{Var}}(\gamma_j)=s_j^2-\bar v_j,
\qquad F_j=s_j^2/\bar v_j.
$$

The historical F reference uses numerator degrees of freedom $T-1$ and denominator $T(20-K)$, where $K$ is the total number of monthly regression coefficients, including the intercept. Its justification invokes independent, identical normal cross-sectional disturbances and stationarity; it is not a heteroskedasticity-robust variance-components test.

For the beta-only full sample, the beta coefficient's total variance is 0.00436 and mean sampling variance is 0.00035, giving $F=12.46$ and estimated true variance 0.00401. The intercept has total variance 0.00142 and sampling variance 0.00037, giving $F=3.84$. In the full model, the quadratic coefficient has $F=1.21$ and the residual-risk coefficient $F=1.47$ for the whole sample. Some subperiod values are larger. These results motivate stochastic common influences beyond a single market return even though the additional coefficients' unconditional means are not significantly different from zero.

Appendix A1 rewrites the beta-only relation as

$$
R_{pt}\simeq b_pR_{mt}+(1-b_p)\hat\gamma_{0t}+\hat\eta_{pt}.
$$

This is a two-factor return-generating representation. A single-factor market-model residual includes a component associated with the zero-beta return. Its contribution is larger when beta is farther from one, so it also explains why residual dependencies and beta-estimation errors are stronger at the exposure extremes. The full specification adds centered quadratic and residual-risk directions to produce a four-factor representation.

For event studies, removing the additional zero-beta common component can reduce residual variance over much of the beta range. Moving from two to four factors produces more modest improvements, concentrated at extreme-beta portfolios. Including residual-risk exposure in addition to beta and the quadratic term never produces a noticeable additional residual-variance reduction in their reported calculations. These are covariance-model observations, not evidence that each added factor earns a nonzero premium.

Appendix A2 notes that a multifactor data-generating process makes ordinary single-market-regression beta estimates inefficient and their errors correlated across stocks. In principle one could estimate exposures using the true zero-beta factor, but that factor is itself estimated from the noisy exposures. The appendix does not solve this circular measurement problem. It refers readers to an earlier-version appendix for a more detailed errors-in-variables analysis; that additional document is not included in the supplied source.

## What the two-stage uncertainty calculation accomplishes

The monthly cross-sectional coefficient is a linear combination of that month's portfolio returns. With design matrix $X_t$ containing the lagged exposures, it is $\hat\gamma_t=(X_t'X_t)^{-1}X_t'R_t$. Common shocks to many portfolios therefore enter the same monthly coefficient. Taking the empirical time-series variance of these coefficients incorporates their realized common variation without pretending that twenty portfolios provide twenty independent estimates of the economy's monthly price of risk.

That advantage does not mean every estimation problem is solved. The design matrices contain estimated betas, and their errors can persist across the twelve months sharing one annual estimate. Cross-sectional diversification reduces those errors but does not remove correlated components. The paper's appendix explicitly recognizes this limitation. The simple time-series standard error is justified by the maintained behavior of the coefficient process, not by an assertion that the generated regressors are exact.

The practical audit is to retain the entire monthly coefficient vector, its cross-sectional standard error, and the lagged exposure matrix. The variance of monthly estimates supports the mean-premium test; the average cross-sectional variance supports the separate Table 5 variance-component comparison. Interchanging these two variance estimators would change both conclusions. Keeping this intermediate record also permits a later serial-dependence sensitivity check without reconstructing portfolios or inadvertently changing the original economic regressors.

## Replication boundaries and practical takeaways

A reconstruction should audit every stage separately: reproduce eligible stock counts, portfolio sizes, and formation calendars; verify that annual estimate updates use only past observations; preserve average individual squared betas and average individual residual standard deviations; then recover monthly regressions before comparing means and t-statistics. Decimal-versus-percent return scaling must be consistent across the market model, residual-risk regressor, and second pass. Scaling only the dependent variable or only residual volatility will change reported coefficients.

The manuscript does not provide executable code, permanent security identifiers for each portfolio, precise handling of every missing-return or delisting convention, a return-data vintage, or a Treasury-bill construction file. Modern CRSP histories can differ from the vintage used here. Consequently the calendar and formulas can be implemented precisely, but an exact last-decimal match requires historical data and conventions beyond the article.

The economic result is conditional on the equal-weighted NYSE proxy being approximately efficient. It does not identify the true aggregate wealth portfolio, including assets outside listed US equities. Long backward estimation windows trade precision against changing exposures, and eligibility rules favor stocks with substantial histories. No transaction-cost or turnover study is supplied because these portfolios are test instruments rather than proposed implementable investment products.

The strongest transferable lesson is the experimental discipline: risk measures are estimated before test returns; estimation uncertainty is reduced through carefully constructed portfolios; average pricing restrictions are tested through time; and covariance misspecification is separated from mean-pricing failure. The historical empirical verdict is appropriately narrower: a positive average beta tradeoff and nonrejection of linearity in this sample coexist with an intercept that is too high for the unrestricted-borrowing version of the CAPM and with realized common return variation beyond one market factor.

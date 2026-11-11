# Economic forces and the stock market revisited

Jay Shanken and Mark I. Weinstein. *Journal of Empirical Finance* 13 (2006), 129–144; accepted September 23, 2005. DOI: 10.1016/j.jempfin.2005.09.001. Source: [MacroAssetPricing_ShankenWeinstein_2006.pdf](../../Finance/MacroAssetPricing_ShankenWeinstein_2006.pdf), the complete 16-page article. References below use printed pages, with PDF page 1 corresponding to page 129. Earlier versions circulated as *Macroeconomic Variables and Asset Pricing: Further Results*. The similarly named library PDF `MacroEconomicFactor_ShankenWeinstein_2006.pdf` is not treated as a separate research contribution.

## Why this matters

Chen, Roll, and Ross (CRR) found persuasive evidence that several intuitive macroeconomic factors were priced in stocks. Shanken and Weinstein ask whether those inferences survive changes to portfolio formation and beta estimation that are entirely conventional in empirical asset pricing. Their answer is largely negative. The economically important design choice is whether the history used to estimate a portfolio's beta is constructed using information already available at each historical ranking date, or is reconstructed using a later size ranking.

The paper is also an implementation guide to restrictions imposed by traded factors. A corporate-minus-government bond return spread is already a zero-investment portfolio. If the factor pricing relation holds for its underlying bonds, its price of risk equals its own expected return. This gives a direct, relatively efficient test of whether the spread is priced, independent of noisy stock-beta estimates. In this sample its mean is insignificantly negative, despite the strong positive premium previously inferred from equity cross sections.

The innovations are the controlled reassessment of the earlier experimental design, incorporation of errors-in-variables uncertainty, and estimation and testing methods that impose bond-factor pricing restrictions. The paper does not offer a new macroeconomic equilibrium model or a new profitable trading strategy. It clarifies what an empirical beta-pricing result can support and how sensitive that support is to implementation choices.

## Model, economic interpretation, and notation

For portfolio $p$ and month $t$, let $R_{pt}$ be the return in excess of a one-month Treasury bill. The baseline first-pass model, equation (1), is

$$
R_{pt}=a_p+\beta_{1p}MP_t+\beta_{2p}DEI_t+\beta_{3p}UI_t+\beta_{4p}UPR_t+\beta_{5p}UTS_t+\epsilon_{pt}.
$$

The factors retain the CRR definitions:

| Factor | Definition and timing |
|---|---|
| $MP$ | Percentage growth in industrial production, led by one month relative to the stock-return month |
| $DEI$ | Change in expected inflation |
| $UI$ | Contemporaneous unanticipated inflation |
| $UPR$ | Low-grade corporate-bond return minus long-term government-bond return |
| $UTS$ | Long-term government-bond return minus the one-month Treasury-bill return |

The factor data were supplied by Richard Roll and begin in 1953. The authors intentionally use the original series without trying to re-estimate innovations. Detailed inflation-expectation construction and underlying bond-series specifications are referred to CRR rather than reproduced in this article. The one-month lead for production is a specification for measuring contemporaneous economic exposure; it is not information a trader could have used at the beginning of the return month.

The pricing restriction is a separate equation:

$$
E[R_{pt}]=\gamma_0+\sum_{k=1}^{5}\gamma_k\beta_{kp}.
$$

$\gamma_0$ is an **excess zero-beta rate**. It is not set to zero merely because dependent returns are measured in excess of Treasury bills. For a nontraded macro factor, $\gamma_k$ is the price of its particular beta normalization, not generally its sample mean. Scaling a factor changes its beta and corresponding price inversely, leaving fitted expected returns invariant.

The maintained economic condition is that the residual returns are uncorrelated with the appropriate equilibrium pricing benchmark, such as market wealth or marginal utility. This is a joint claim about the factors and the pricing model. An unrestricted statistical regression on macro series alone does not prove it. The paper emphasizes that a large-market no-asymptotic-arbitrage approximation does not by itself impose an exact finite-asset restriction of this form.

For the inference developed here, disturbances have conditional mean zero and a covariance matrix constant conditional on factors; factors and returns are taken to be independent and identically distributed over time. These assumptions are most natural for the full-period, contemporaneous-beta case. They are stronger than needed for many modern robust procedures, but replacing them with a different inference method changes the experiment being reproduced. In particular, production growth need not be an innovation and may be serially correlated.

## The portfolio-formation difference that drives the reassessment

The earlier CCH/CRR design considers six-year intervals. Choose NYSE firms present at the start and with the required price information at the end of year five. Rank them by size at the end of year five, place them into 20 portfolios, and estimate portfolio betas using the first five years of returns for those **later-selected constituents**. Use the sixth year's monthly returns in second-pass cross-sectional regressions.

This history is conditioned on the later ranking. Firms whose prices fell during the estimation window are more likely to be classified as small at its end, and winners as large. If leverage or cash-flow risk changes with performance, their historical average beta need not represent risk after ranking. The paper discusses the possibility that small-firm risk is understated and large-firm risk overstated, compressing the estimated beta spread and distorting the inferred prices of risk. In a multifactor model the sign need not follow a simple one-factor attenuation story.

The alternative constructs a continuous series for each size-ranked “fund.” At every December end, sort securities on total market equity and form equally weighted size portfolios. Compute their returns in the following calendar year. At the next December, reconstitute them. The smallest portfolio in different years contains different companies, but consistently represents the same investable ranking rule. Every historical return in its time series is a post-ranking return, with membership based on a ranking already known at that date.

Two estimation schemes use these same fund-return histories. In the **prior-beta** scheme, estimate betas from the 60 monthly fund returns ending in December immediately before the cross-sectional-regression year; hold those betas fixed for its twelve monthly cross sections; update annually. In the **contemporaneous-beta** scheme, estimate one beta vector per fund using the same full sample over which the return cross sections are evaluated. The latter is a model-evaluation exercise using estimated unconditional exposures, not an out-of-sample forecasting strategy.

The main second-pass sample is January 1958–December 1983, 312 months. The 1953–1957 data initialize prior-beta estimation. The authors also analyze 1968–1977, 120 months, because CRR's strongest evidence occurs there. CRR's original analysis extended through 1984, but Shanken and Weinstein align their own prior- and contemporaneous-beta experiments through 1983. They report that adding 1953–1957 to the contemporaneous sample did not substantially change the conclusion.

Run both 20- and 60-portfolio versions. More portfolios can create additional cross-sectional information but also more beta and covariance estimation noise. An earlier 120-portfolio version was omitted because its smallest stocks would be exceptionally thinly traded; its qualitative conclusions were similar. The source does not provide a complete modern security-code filter, delisting-return convention, or every tie-handling rule. A replication needs to state these choices and must not label them as fully specified by the article.

## Two-pass estimation and the uncertainty correction

For each month form the matrix $X_t=[\mathbf1,\widehat B_t]$, where $\widehat B_t$ is the $N\times K$ matrix of first-pass slopes. The monthly second-pass coefficient estimate can be represented as

$$
\widehat\Gamma_t=(X_t'W_tX_t)^{-1}X_t'W_tR_t,
\qquad \widehat\Gamma=T^{-1}\sum_{t=1}^{T}\widehat\Gamma_t.
$$

The main reported implementation is weighted least squares, as in CCH. The authors say OLS gives similar findings. They also investigate GLS with the inverse first-pass residual covariance matrix as weight. The article does not fully specify the numerical WLS weighting construction in its methodological description; that is an input to recover from original programs or accompanying earlier methodology for exact numerical reproduction. It should not be silently replaced by a claimed source-prescribed weight formula.

Conventional Fama–MacBeth inference uses the time-series variance of $\widehat\Gamma_t$ divided by $T$. It does not fully incorporate uncertainty in the beta regressors. For factor $k$, let $s^2(\gamma_k)$ be that conventional variance of the mean estimate, and let $s_k^2=\operatorname{Var}(F_k)/T$, with $s_0^2=0$. The paper's equation (4) is

$$
\operatorname{Avar}(\widehat\gamma_k)=\big[s^2(\gamma_k)-s_k^2\big](1+c)+s_k^2,
\qquad c=\widehat\gamma'S_F^{-1}\widehat\gamma.
$$

Here $\widehat\gamma$ contains the **factor prices only**, excluding the zero-beta intercept, and $S_F$ is the $K\times K$ factor covariance matrix. Including the intercept in this quadratic form would be dimensionally incorrect. For prior-beta estimation the paper multiplies $c$ by $1-1.6/n$, where $n$ is the number of years of cross-sectional regressions. Thus $n=26$ for the full period and $n=10$ for the ten-year subperiod.

The correction enlarges only the part of pricing uncertainty attributable to estimated exposures, not the factor-mean component. It corrects an asymptotic standard error; it does not remove the finite-sample bias of two-pass slope estimates. This is why forming portfolios remains relevant even after applying the correction. Under the joint null that all factor prices are zero, beta estimation error has no first-order effect, so the joint zero-pricing test does not require that EIV adjustment.

Two alternatives were investigated and abandoned. A correction to the beta cross-product matrix often produced a matrix that was not positive definite, defeating its large-cross-section motivation. A maximum-likelihood implementation with diagonal residual covariance produced economically extreme estimates. These are reported implementation failures, not competing successful specifications. The GLS experiment is restricted to 20 portfolios because inverse-covariance noise and unaccounted-for weight-estimation uncertainty become troublesome as $N$ increases; it yields no individually significant factor prices.

## Unrestricted results and their units

All tabulated prices and standard errors are multiplied by 100. For return-factor prices these are monthly percentage points; for a macro factor they describe the monthly expected-return premium attached to a unit beta under that factor's reported scale. Bracketed standard errors below are EIV adjusted. The most informative comparisons in Table 1 are:

| Design | $N$ | $MP$ estimate [SE] | $UPR$ estimate [SE] | Joint zero-pricing test $p$ |
|---|---:|---:|---:|---:|
| Contemporaneous, unrestricted | 20 | 0.32 [0.50] | 0.12 [0.28] | 0.23 |
| Contemporaneous, unrestricted | 60 | 0.55 [0.32] | 0.22 [0.22] | 0.21 |
| Prior five-year betas, unrestricted | 20 | 1.19 [0.50] | 0.23 [0.30] | 0.02 |
| Prior five-year betas, unrestricted | 60 | 0.91 [0.30] | 0.37 [0.20] | 0.06 |

No factor has a price more than two EIV-adjusted standard errors from zero in the contemporaneous specifications. With prior betas, industrial production is individually significant, while the other factors fail to exceed two standard errors. Increasing the portfolio count lowers the $MP$ point estimate and its standard error. Yet the joint test becomes less significant, from 0.02 to 0.06. The most impressive individual $t$-ratio and the multivariate hypothesis answer different questions.

The comparison with CRR is particularly controlled in the prior-beta design: both use five years of information before the return cross section, but differ in whether those five years are returns of backward-selected fixed constituents or of annually reconstituted post-ranking portfolios. CRR reported $t$-statistics of 3.6, −2.0, and 2.6 for production, unexpected inflation, and the bond spread in its comparable specification. Shanken and Weinstein replicated the earlier findings with the original portfolio data and with an older CRSP reconstruction. Their reassessment is therefore not simply a failure to run the earlier code correctly.

In 1968–1977, no factor is more than two **uncorrected** standard errors from zero in their Table 2; none of the joint tests is significant at 10%. For $N=20$, the unrestricted $UPR$ estimate changes from −0.17 with contemporaneous betas to 0.42 with prior betas, versus CRR's 1.27. CRR had found absolute $t$-statistics above 2.5 for all five factors in this same economically important subperiod. A further experiment estimates fixed-constituent portfolio betas using five years **after** the return-cross-section year; it also fails to recover the earlier pricing evidence. That experiment diagnoses sensitivity and is plainly not a feasible trading rule.

## Restrictions implied by the bond portfolios

The government-bond excess return is $UTS$ itself, so its factor regression has loading one on $UTS$ and zero on all other factors. Its expected return must therefore satisfy

$$
E[UTS]=\gamma_0+\gamma_5.
$$

The low-grade corporate-minus-government spread is a difference of two fully invested portfolios. Their zero-beta terms cancel. Its loading difference is one on $UPR$ and zero elsewhere, giving

$$
E[UPR]=\gamma_4.
$$

The distinction matters: the spread's price equals its mean even when the zero-beta rate differs from the Treasury-bill rate. By contrast, equating the $UTS$ price to its excess-return mean would incorrectly impose $\gamma_0=0$.

Substitute these restrictions into the expected-return equation. In each monthly restricted regression use

$$
Y_{pt}=R_{pt}-UTS_t\widehat\beta_{5p}-UPR_t\widehat\beta_{4p}
$$

as the dependent variable and

$$
1-\widehat\beta_{5p},\quad\widehat\beta_{1p},\quad\widehat\beta_{2p},\quad\widehat\beta_{3p}
$$

as regressors. There is no additional unrestricted intercept: the coefficient on $1-\widehat\beta_{5p}$ is $\gamma_0$. Average the monthly estimates, then recover $\widehat\gamma_5=\overline{UTS}-\widehat\gamma_0$ and $\widehat\gamma_4=\overline{UPR}$. This uses the bond pricing information without estimating a separate arbitrary price for a known traded spread.

Under the maintained assumptions the sample-mean estimator for the $UPR$ price is unbiased and more efficient than its equity-CSR counterpart. A beta-mimicking equity portfolio includes residual model risk; the actual factor portfolio has none relative to the factor model that includes itself. Its zero-investment mean can consequently be tested with an ordinary mean-return $t$-test. This efficiency statement is conditional on model and sampling assumptions, not a universal claim about arbitrary nonlinear or serially dependent estimators.

In Table 1, restricted $UPR$ is −0.02 with standard error 0.13 monthly percentage points. In the shorter period it is −0.03 with standard error 0.21. These estimates do not establish a negative true premium; they show that this sample cannot establish the positive premium suggested by the earlier stock cross sections. The finding cannot be fixed merely by changing the stock-beta estimation window because that estimator uses no stock betas.

Bond restrictions strengthen production pricing: with contemporaneous betas, $MP$ estimates are 2.92 [1.33] and 2.70 [1.04] for 20 and 60 portfolios; with prior betas they are 2.29 [0.84] and 1.80 [0.54]. But the restrictions also produce problematic excess zero-beta estimates. For contemporaneous betas these are −1.08 [0.52] and −0.95 [0.41] percentage points per month. The associated $UTS$ prices, 0.91 [0.54] and 0.78 [0.43], are less than two adjusted standard errors from zero. A large fitted term premium partly reflects the extremely low fitted intercept, not an independently established bond reward.

## Three distinct tests, and what non-rejection means

The joint zero-pricing test asks whether the factor-price vector is zero. The model-linearity test instead asks whether expected returns lie in the affine span of the beta vectors, allowing nonzero prices. A factor can have a significant price while leaving material pricing errors, or no factor can be individually significant while the overall linearity restriction remains unrejected.

For contemporaneous betas let $e$ be the vector of mean GLS cross-sectional residuals and $\widehat\Sigma_\epsilon$ the first-pass residual covariance. Equation (6) uses

$$
Q=\frac{T e'\widehat\Sigma_\epsilon^{-1}e}{1+c}.
$$

Asymptotically $Q$ is chi-squared with $N-K-1$ degrees of freedom. The authors prefer a finite-sample Hotelling $T^2$ approximation with degrees of freedom $N-K-1$ and $T-K-1$, motivated by poorer chi-squared approximations when many assets are used. The source does not tabulate the actual linearity statistics; it reports that none rejects the unrestricted five-factor model at 10%. The residual covariance becomes singular if $N>T-K-1$, so this test is not available for arbitrarily many assets without changing its construction.

For the restricted model, replace $e$ and $c$ by their restricted counterparts. The cross-sectional degrees of freedom become $N-K_1-1$, where $K_1=3$ counts factors without traded-portfolio restrictions; the time-series degree remains $T-K-1$. Neither 20- nor 60-portfolio restricted-model linearity test rejects at 5%. Given weak pricing evidence and noisy macro betas, the authors caution that these failures to reject may reflect low power.

A third test compares the monthly restricted and unrestricted $UPR$ and $UTS$ price estimates, using an EIV-adjusted Hotelling statistic for their mean differences. It tests the bond restrictions conditional on the equity pricing relation. The adjustment is calculated from unrestricted prices to avoid imposing potentially false restrictions inside its own scale. No five-factor specification rejects these restrictions at 10%, even though their imposition sometimes increases rather than decreases standard errors. Finite-sample non-rejection should not erase the economic concern raised by radically different fitted prices.

## Adding the stock market

The five macro factors explain only about 25–30% of the time-series variation of the 20 size portfolios. Adding the value-weighted CRSP excess market return, $VW$, raises this to about 80%. In the restricted six-factor model it obeys $\gamma_{VW}=E[VW]-\gamma_0$, like $UTS$. The transformed dependent return subtracts $VW_t\beta_{VW,p}$ as well, and the zero-beta regressor becomes $1-\beta_{UTS,p}-\beta_{VW,p}$.

Table 3 finds positive market prices in most specifications. For unrestricted contemporaneous betas, $VW$ prices are 1.48 [0.61] and 0.85 [0.38] monthly percentage points for 20 and 60 portfolios. For restricted prior-beta estimates they are 0.87 [0.35] and 0.80 [0.30]. Production retains significant pricing mainly in the prior-beta specifications; its unrestricted contemporaneous estimates are −0.13 [0.52] and 0.40 [0.33]. Thus greater covariance fit is accompanied by a different division of the apparent risk premia.

The six-factor joint zero-pricing tests are significant at 1% only for restricted models. Linearity tests do not reject at 10%. The test of traded-factor restrictions does reject in one case, contemporaneous betas with 60 portfolios, with $p=0.01$; other reported specifications have $p>0.10$. Again, the zero-beta rates are implausibly low. These results challenge both the idea that the market is redundant once macro factors enter and the claim that the selected macro model is economically satisfactory.

## Replication boundaries and practical conclusions

A faithful reconstruction should retain separate switches for portfolio-history construction, number of size portfolios, prior versus contemporaneous beta estimation, restricted versus unrestricted pricing, and five versus six factors. It should report raw and adjusted standard errors, individual prices, joint zero-pricing tests, linearity tests, and restriction tests separately. These are a deliberately structured robustness exercise; selecting the strongest single estimate would miss its purpose.

The article supplies no transaction-cost model, portfolio turnover study, tuning exercise, or trading-validation holdout, because it evaluates pricing relations rather than a deployable strategy. Historical factor input files, detailed WLS settings, security eligibility rules, and exact source-vintage treatment remain needed for bit-for-bit replication. Its iid inference and conditional covariance assumptions should be stress-tested in a modern extension, but such an extension is distinct from reproducing the published numbers.

Finally, even the comparatively favorable production result is qualified. The authors note that CCH found its significance marginal after simple autoregressive prewhitening. The current study deliberately does not replace growth by a newly estimated innovation, so it cannot settle whether innovation risk is priced. The defensible takeaway is that seemingly modest data-construction choices materially change macro-factor pricing conclusions, and economically required traded-factor restrictions are useful independent checks on what an equity cross section appears to say.

# Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models

**Robert Engle (2002).** *Journal of Business & Economic Statistics* 20(3), 339–350, DOI 10.1198/073500102288618487. Source: [original PDF](../../Finance/DynamicCorrelation_Engle_2002.pdf), twelve pages including the full simulation comparison, empirical figures, and Appendices A–B. Printed page and equation references refer to that version. This note separates the implementable likelihood-based model from some stronger moment interpretations asserted in the source.

## Why this matters

Estimating a separate dynamic coefficient for every covariance quickly becomes impractical as the number of assets grows. Yet setting correlations constant can miss changes that matter directly for hedge ratios, diversified portfolio risk, and option payoffs involving several assets. Engle's contribution is to separate the problem into univariate conditional variances and a parsimonious dynamic correlation process.

The key architecture is $H_t=D_tR_tD_t$. Each asset receives its own variance model; standardized residuals feed a common correlation recursion; normalization ensures unit diagonal and an admissible correlation matrix. In its scalar form only two correlation-dynamics parameters are optimized, whatever the number of assets. The static target matrix still contains many entries, and matrix operations still grow with dimension, so the benefit is parameter parsimony rather than dimension-free computation.

The article establishes feasibility through bivariate Monte Carlo experiments and historical stock, bond-proxy, and currency examples. The mean-reverting DCC version performs particularly well in the simulated comparisons, while empirical diagnostic tests reject many specifications. The result is a useful modeling compromise, not evidence that this early specification eliminates real-world volatility misspecification.

One practical advantage is modularity. Adding assets need not change existing univariate variance forecasts. It can change jointly estimated correlation parameters and therefore correlations, however; the article's statement that correlations may remain unchanged depends on how the larger model is constructed.

## Conditional covariance, marginal scaling, and model timing

Let $r_t$ be an $n\times1$ vector of mean-zero return innovations, and let $\mathcal F_{t-1}$ be information known before the date-$t$ return. Define

$$
H_t=E(r_tr_t^{\mathsf T}\mid\mathcal F_{t-1}),
\qquad D_t=\operatorname{diag}(\sqrt{h_{1t}},\ldots,\sqrt{h_{nt}}),
\qquad \varepsilon_t=D_t^{-1}r_t.
$$

Then $E(\varepsilon_t\varepsilon_t^{\mathsf T}\mid\mathcal F_{t-1})=R_t$ and

$$
H_t=D_tR_tD_t.
$$

Each standardized component has conditional variance one. Conditional correlation equals conditional covariance for these standardized innovations. This is why DCC smooths standardized cross-products instead of raw-return cross-products: the latter mix changes in correlation with changes in marginal scale.

A baseline first-stage specification is

$$
h_{it}=\omega_i+a_i r_{i,t-1}^2+b_i h_{i,t-1}.
$$

Standard sufficient restrictions are $\omega_i>0$, $a_i,b_i\ge0$, and $a_i+b_i<1$ for finite unconditional variance in this basic model. The DCC architecture can use other univariate volatility models or predetermined regressors; the simulation and displayed system use GARCH(1,1).

All recursions use shocks from $t-1$ to forecast date $t$. Once $r_t$ arrives, it updates the forecast for $t+1$. The historical graphs are fitted conditional correlations, not estimates based on contemporaneous returns sneaked into the forecasting information set. Full-sample parameter estimation is nonetheless retrospective; causal recursions by themselves do not establish a genuine held-out forecast design.

## Scalar DCC recursion and positivity

Let $S$ be the sample correlation target constructed from first-stage standardized residuals, and introduce an auxiliary symmetric matrix $Q_t$:

$$
Q_t=(1-\alpha-\beta)S
+\alpha\varepsilon_{t-1}\varepsilon_{t-1}^{\mathsf T}
+\beta Q_{t-1}.
$$

The normalized conditional correlation is

$$
R_t=\operatorname{diag}(Q_t)^{-1/2}Q_t
\operatorname{diag}(Q_t)^{-1/2},
\qquad
\rho_{ij,t}=\frac{q_{ij,t}}{\sqrt{q_{ii,t}q_{jj,t}}}.
$$

Here $\operatorname{diag}(Q_t)$ denotes the diagonal matrix of diagonal entries. The inverse square roots are essential. The compact matrix notation in printed Eq. (25) is ambiguous about this operation; elementwise Eq. (21) supplies the unambiguous normalization. Using inverse diagonal entries instead would not give a unit diagonal.

With $S\succ0$, $Q_0\succ0$, $\alpha,\beta\ge0$, and $\alpha+\beta<1$, each new $Q_t$ is positive definite: the strictly positive weight on $S$ supplies a positive-definite term, and the other terms are positive semidefinite. Diagonal rescaling then preserves positive definiteness and sets every diagonal element to one. Combined with positive marginal variances, $H_t$ is positive definite.

The boundary version is the integrated smoother

$$
Q_t=(1-\lambda)\varepsilon_{t-1}\varepsilon_{t-1}^{\mathsf T}
+\lambda Q_{t-1},\qquad 0<\lambda<1.
$$

It has no fixed target contribution and corresponds to $\alpha=1-\lambda$, $\beta=\lambda$. A positive-definite initialization remains important, especially with few observations relative to dimension. The initial matrix's influence decays geometrically, but the recursion need not inherit stationary mean reversion to a fixed target.

There is a notation trap: Appendix A labels the integrated innovation-weight estimate “lambdaDCC” and reports values around .02–.05. Those small values naturally represent the new-shock weight; Eq. (17)'s $\lambda$ denotes the large retention weight. A reproduction must establish the convention in code and should not insert .03 as a retention coefficient merely because the table calls it lambda.

The paper also presents a matrix-parameter extension using Hadamard products:

$$
Q_t=S\odot(\mathbf1\mathbf1^{\mathsf T}-A-B)
+A\odot(\varepsilon_{t-1}\varepsilon_{t-1}^{\mathsf T})
+B\odot Q_{t-1}.
$$

Positive-semidefinite restrictions on $A$, $B$, and the intercept coefficient matrix support admissibility through the Schur product theorem. This is more flexible but gives up some scalar-model simplicity. The empirical comparisons emphasize the scalar dynamics.

## Auxiliary moments are not normalized correlations

$Q_t$ is an auxiliary state. Its entries are not generally the conditional covariances of $\varepsilon_t$, which are the entries of $R_t$. Also, an average of normalized matrices is not the normalization of an average matrix. Thus $E(Q_t)=S$, when justified by the targeted moment construction, does not by itself imply $E(R_t)=S$ entry by entry.

This distinction matters in the source's alternative ARMA argument. With $e_{ij,t}=\varepsilon_{it}\varepsilon_{jt}$, algebra rearranges the $Q$ recursion into an ARMA-like expression involving $e_{ij,t}-q_{ij,t}$. The paper calls that difference a martingale innovation. Under the normalized conditional covariance model, however,

$$
E(e_{ij,t}-q_{ij,t}\mid\mathcal F_{t-1})
=\rho_{ij,t}-q_{ij,t},
$$

which is not generally zero. The rearrangement is algebraically valid, but its claimed innovation interpretation needs an additional approximation or condition. This note therefore treats the likelihood recursion as the primary procedure and does not infer unconditional consistency of the alternative ARMA/IMA estimator from that argument alone.

The same issue cautions against blindly forecasting $Q$ several periods ahead with an ordinary scalar AR(1) formula having persistence $\alpha+\beta$. Conditional expected standardized cross-products are normalized $R$ matrices. For longer horizons, use a clearly specified recursion or simulation that respects normalization, rather than equating $Q_t$ with $R_t$. The article's central evidence concerns one-period conditional correlations.

## Two-stage likelihood estimation

For conditionally Gaussian returns, up to constants,

$$
L=-\frac12\sum_t\left[
\log|H_t|+r_t^{\mathsf T}H_t^{-1}r_t\right].
$$

Using the decomposition gives

$$
L=L_V+L_C,
$$

$$
L_V=-\frac12\sum_t\sum_i
\left[\log h_{it}+r_{it}^2/h_{it}\right],
$$

$$
L_C=-\frac12\sum_t
\left[\log|R_t|+\varepsilon_t^{\mathsf T}R_t^{-1}\varepsilon_t
-\varepsilon_t^{\mathsf T}\varepsilon_t\right].
$$

First maximize each univariate term separately. Compute standardized residuals and their target correlation. Then hold those first-stage estimates fixed and optimize the correlation parameters. The final subtraction in $L_C$ does not depend on the second-stage parameters and can be omitted during that optimization.

The source calls the stationary likelihood version DCC LL MR and the integrated version DCC LL INT. It also estimates an integrated-moving-average alternative, DCC IMA. The two-stage estimator is convenient but generally not identical to jointly maximizing the full likelihood over all parameters. Conditional Gaussianity supplies a literal likelihood interpretation; under appropriate conditions Gaussian quasi-likelihood can still estimate a specified conditional covariance structure with nonnormal innovations.

For implementation, use a Cholesky factorization of $R_t$ to compute log determinants and quadratic forms, rather than explicitly inverting matrices. This is a numerical implementation of the displayed criterion, not an additional model. Reject parameter proposals that violate admissibility or produce nonpositive diagonals. Record initialization, optimization tolerances, treatment of mean returns, target-matrix normalization, and any regularization. These settings are not all specified in the article, and they can affect near-boundary fits.

Second-stage uncertainty must include first-stage estimation error. Let $s_{V,t}$ and $s_{C,t}$ be the relevant score contributions, and let $A_{VV}$, $A_{CC}$, and $A_{CV}$ denote expected derivative blocks. The adjusted correlation score has the form

$$
\widetilde s_{C,t}=s_{C,t}-A_{CV}A_{VV}^{-1}s_{V,t}.
$$

A sandwich covariance uses $A_{CC}^{-1}$ around the covariance of this adjusted score, scaled by sample size as appropriate. Equation (33) gives this two-step correction. Using only the Hessian of the conditional second-stage optimization understates or otherwise misstates uncertainty when first-stage errors matter. The paper refers detailed regularity arguments to Engle and Sheppard (2001).

The published asymptotic discussion is conditional on correctly specified moments and regularity. Its continuity argument should not be read as establishing validity for any arbitrary marginal models, singular sample targets, or the auxiliary-innovation identification just discussed.

## Competing estimators

The simulation compares eight procedures. Scalar and diagonal BEKK model raw conditional covariances with variance targeting. The first-order form is $H_t=\Omega+A r_{t-1}r_{t-1}^{\mathsf T}A^{\mathsf T}+BH_{t-1}B^{\mathsf T}$; targeting sets the long-run covariance to the sample covariance through the corresponding intercept restriction.

Orthogonal GARCH first forms unconditionally uncorrelated linear combinations, fits their marginal GARCH variances, and assumes their conditional correlations remain zero. That latter assumption is much stronger than unconditional orthogonality. Reconstructing the original covariance requires the appropriate inverse transformation; it is not another normalization of standardized residuals.

The remaining comparators are the three DCC versions, a 100-observation rolling covariance/correlation estimate, and RiskMetrics-style exponential smoothing. EX .06 uses a new-observation weight .06 and retention .94. The same decay parameter is used throughout the covariance system to preserve a coherent matrix. The rolling and exponential procedures operate on raw returns, unlike DCC's standardized innovations.

These distinctions isolate several possible sources of performance: responsiveness, marginal variance specification, correlation dynamics, and matrix constraints. A rejection of a full covariance forecast cannot always be assigned uniquely to the correlation submodel.

## Monte Carlo data-generating processes

The experiment uses 200 replications of 1,000 bivariate observations per correlation design, approximately four years of daily data. The marginal variances are

$$
h_{1t}=0.01+0.05r_{1,t-1}^2+0.94h_{1,t-1},
$$

$$
h_{2t}=0.5+0.2r_{2,t-1}^2+0.5h_{2,t-1}.
$$

Conditional innovations are bivariate Gaussian with variances one and imposed correlation $\rho_t$, and returns are generated by marginal standard-deviation scaling. The first variance is highly persistent; the second is much less persistent. Their stationary marginal means, derived from the reported coefficients, are 1 and $5/3$ respectively.

Five deterministic correlation paths are specified: constant .9; slow sine $.5+.4\cos(2\pi t/200)$; fast sine $.5+.4\cos(2\pi t/20)$; a step from .9 to .4 after observation 500; and a repeating ramp taking the fractional part of $t/200$. Figure 1 confirms the ramp resets every 200 observations. A sixth reported case repeats the slow sine with $t(4)$ innovations. The article does not fully document the Student distribution construction and standardization, initial variance states, burn-in, seeds, or optimizer settings. Those omissions limit bit-for-bit reproduction.

The imposed correlations are not generated by the fitted DCC or BEKK recursions. The experiment therefore evaluates approximation to several styles of changing dependence rather than selecting an estimator known to be correctly specified. The paper repeats the entire Monte Carlo twice more with different random numbers and reports similar rankings, but provides no full replication-level output or uncertainty intervals for every difference.

No separate rolling training/test split is described. The reported results should be understood as fitted simulation comparisons unless additional original implementation information establishes another design.

## Evaluation statistics and exact portfolio definitions

The first loss is mean absolute correlation error,

$$
MAE=\frac1T\sum_t|\widehat\rho_t-\rho_t|.
$$

It is measured in correlation units, so .14 is not a fourteen-percent relative error. This statistic is available in simulation because the imposed correlation is known, but not in the historical application.

The second diagnostic uses triangularly standardized residuals:

$$
\nu_{1t}=r_{1t}/\sqrt{H_{11,t}},
$$

$$
\nu_{2t}=\frac{r_{2t}/\sqrt{H_{22,t}}-
\widehat\rho_t r_{1t}/\sqrt{H_{11,t}}}
{\sqrt{1-\widehat\rho_t^2}}.
$$

Each squared standardized residual is regressed on an intercept and five lags of the two squares and their cross-product. An $F$ test checks whether the lagged terms jointly explain remaining variation. The first residual depends only on the first marginal variance; the second also depends on correlation. This ordering explains why the second test is more revealing about DCC performance. Near-perfect correlations make its denominator small and require careful numerical handling.

For portfolio weights $w$, the normal 5% loss threshold is $1.65\sqrt{w^{\mathsf T}H_tw}$. Define the centered breach indicator

$$
\operatorname{hit}_t=\mathbf1\{w^{\mathsf T}r_t<-VaR_t\}-0.05.
$$

The dynamic quantile test regresses this indicator on an intercept, five lagged hits, and current forecast VaR, testing all coefficients jointly. The portfolios are $(0.5,0.5)$ and $(1,-1)$. The second has gross exposure two and net exposure zero; it is not represented by simply choosing a different scalar $w$ in $(w,1-w)$. Use its actual weight vector in the covariance quadratic form.

VaR rejection mixes errors in covariance, tail distribution, and temporal calibration. In particular, a normal threshold need not be correct for Student innovations even when covariance is estimated well. Passing one portfolio's VaR test does not establish correct full dependence.

## Simulation results

Table 1's MAE results for three representative procedures are:

| Correlation path | DCC LL MR | DCC LL INT | Rolling 100 |
|---|---:|---:|---:|
| Fast sine | .2260 | .2555 | .2599 |
| Slow sine | .1381 | .1455 | .3038 |
| Step | .0709 | .0686 | .0652 |
| Ramp | .1546 | .1596 | .2828 |
| Constant | .0070 | .0067 | .0185 |
| Student-4 slow sine | .1478 | .1583 | .3016 |

Mean-reverting DCC has the smallest MAE in four of six cases. The rolling estimator narrowly wins the step case, and integrated DCC wins the constant case. Scalar BEKK's slow-sine MAE is .1422, close to .1381 for DCC LL MR; thus the result is not that every conventional multivariate model fails badly. Fast changes remain difficult for all methods: even the best fast-sine MAE is .2260.

For autocorrelation in the second squared standardized residual, slow-sine rejection frequencies are .1400 for DCC LL MR, .1850 for integrated DCC, .2677 for diagonal BEKK, .7600 for exponential smoothing, and 1.0000 for the rolling estimator. For the step case they are .2778, .3250, .6700, .8550, and .9950 respectively. The DCC improvement is substantial, but its rejection rates still greatly exceed the nominal .05 in these misspecified designs.

For the constant case, mean-reverting DCC's second-residual rejection frequency is .0788. For fast sine, diagonal BEKK does better on this diagnostic: .0950 versus .1300 for DCC LL MR. These comparisons show why no single score should replace a suite of diagnostics.

The equal-weighted portfolio's dynamic-quantile rejection frequencies for slow sine are .0250 for mean-reverting DCC and .0350 for integrated DCC, versus .4100 for rolling 100. In the fast-sine case integrated DCC gives .0300. For the long-short portfolio, step-case frequencies are .0404 for DCC LL MR and .0600 for integrated DCC, versus .4600 for rolling 100. But fast-sine long-short frequencies rise to .0900 and .2550 respectively, while orthogonal GARCH gives .0850. Correlation mistakes have different consequences for positively weighted diversification and hedging.

The tables report frequencies across replications without standard errors. Some fractions are not exact multiples of $1/200$, suggesting varying effective denominators or other implementation details not explained in the text. They should be transcribed as reported, not treated as exact binomial counts without the underlying successful-run sample sizes.

## Historical applications and parameters

Appendix A identifies stock and bond-proxy observations from March 23, 1990 to March 22, 2000; dollar exchange-rate observations for deutschemark, lira, and sterling from January 1, 1985 to February 13, 1995; and euro-convergence currency observations from January 1, 1993 to January 15, 1999. Returns are described as log differences. The main text defines the bond return proxy as minus the change in the 30-year Treasury benchmark yield, whereas the appendix broadly labels RATE a Treasury return. This is a yield-change proxy, not a fully specified duration-adjusted total-return series, and the return-construction discrepancy should be preserved as a replication limitation.

The NASDAQ–Dow mean-reverting fit has $\alpha=.039029$ and $\beta=.941958$, with robust $t$ statistics 6.9168 and 92.7274. The sum is .980987. The reported integrated shock weight is .030255569. These numbers concern correlation dynamics; marginal GARCH coefficients are not printed for all historical series.

For the Dow/bond-proxy pair, the corresponding coefficients are .037372 and .950269. For NASDAQ/bond proxy they are .029972 and .953244. Deutschemark/lira in the earlier sample has .0991 and .863885, while deutschemark/sterling has .03264 and .963504. In the euro-convergence sample, deutschemark/franc has .059413 and .934458; deutschemark/lira has .056675 and .943001, a sum .999676 extremely close to the integrated boundary.

The NASDAQ–Dow integrated correlation graph stays mostly between .6 and .9, with marked declines below .4 in 1993 and near March 2000. The stock/bond-proxy correlations are often around .4 but turn strongly negative during the summer of 1998 and approach zero near the end of the sample. These are historical fitted relationships; proposed sector-rotation explanations are descriptive interpretations.

Currency figures show major regime changes around the early-1990s exchange-rate disruptions and convergence toward nearly perfect correlation before the euro's launch. Such structural changes are precisely where a fixed mean-reverting target can be restrictive. The euro-convergence deutschemark/lira pair's second-stage likelihood comparison is only about 1.4565, whereas NASDAQ–Dow's is 33.5784.

The appendix defines its LR number as twice the second-stage log-likelihood difference. The text explicitly warns that these are not jointly maximized full likelihoods, and nonnormality also changes conventional reference distributions. Consequently, the ordinary chi-square LR interpretation is not established by the displayed numbers alone, even though the empirical discussion uses rejection language.

## Diagnostic failures and implementation limits

Appendix B reports four diagnostics across seven datasets, 28 opportunities for rejection per method. At a 5% threshold, the article counts ten rejections for diagonal BEKK, twelve for DCC LL MR, scalar BEKK, orthogonal GARCH, and exponential smoothing, and fourteen for integrated DCC; moving average 100 is worst. If the tests were correctly sized under correct models, roughly 1.4 rejections would be expected, far fewer than observed. Dependence among tests means these counts are descriptive rather than a new formal comparison test.

At a 1% threshold, exponential smoothing has the fewest rejections, and DCC LL MR, integrated DCC, and diagonal BEKK tie at nine. The ranking therefore depends on threshold and criterion. The article itself concludes that larger systematic comparisons are needed and that real data are more complicated than all tested models.

Exact reproduction requires original price sources, calendars, handling of missing observations, mean-return specifications, initialization, volatility-model details, and optimization settings. The article supplies sufficient recursions to implement DCC but not a complete historical data pipeline. Its scaling motivation is not tested with thousands of assets in this paper; all direct comparisons are bivariate. In a large system, estimating a stable target matrix and repeatedly factoring $R_t$ remain substantive problems.

DCC's durable contribution here is the separation of marginal risk from changing dependence, with a normalized matrix recursion and an inexpensive parameterization. Its best-supported empirical claim is competitive approximation across several bivariate correlation paths. For practical use, retain the full two-stage uncertainty correction, diagnose marginal and correlation failures separately, distinguish $Q$ from $R$, and evaluate forecasts on the particular portfolios and information dates for which the risk model will be used.

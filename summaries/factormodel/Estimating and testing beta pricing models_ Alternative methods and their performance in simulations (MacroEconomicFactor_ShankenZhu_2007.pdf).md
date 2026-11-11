# Estimating and testing beta pricing models: Alternative methods and their performance in simulations

Jay Shanken and Guofu Zhou. *Journal of Financial Economics* 84 (2007), 40–86. DOI: 10.1016/j.jfineco.2006.02.003.

Source: [complete 47-page PDF](../../Finance/MacroEconomicFactor_ShankenZhu_2007.pdf). The filename misspells Zhou as “Zhu” and suggests a macroeconomic-factor focus; the actual paper is a general comparison of beta-pricing estimators and tests. It includes analytical derivations and two appendices, Monte Carlo tables, and an empirical Fama–French application. Page references use journal pagination.

## Why this matters

A cross-sectional factor premium is estimated using betas that are themselves estimated from returns. OLS, weighted least squares, generalized least squares, maximum likelihood, and GMM handle this estimation error differently. They can have similar probability limits under a correctly specified pricing model yet very different finite-sample biases, tail behavior, and rejection rates. Under misspecification, they need not even estimate the same population quantity.

The authors' central contribution is a systematic comparison of these procedures using realistic return calibrations, together with several analytical results that make the comparison interpretable and implementable. They derive misspecification-adjusted asymptotic covariances for two-pass estimators, provide analytical constructions for likelihood and GMM estimators, and establish a numerical equivalence between a commonly used GMM specification and maximum likelihood. Their simulations then ask whether asymptotic standard errors and tests behave well at the sample lengths actually used in asset-pricing research.

There is no universal winner. GLS often has low root mean squared error even though it is biased toward zero. Truncated maximum likelihood can reduce bias but retains difficult inference. A sequential GMM method performs differently across premia and sample designs. Ordinary least squares is often less precise but can have more reliable nominal test size in short samples. Misspecification can make conventional reported standard errors too small, and apparently dramatic intercept estimates may correspond to economically implausible compensating factor-premium estimates.

This is a methodology and inference paper. It does not propose a return forecast, a trading signal, or a portfolio strategy with costs. Its sample designs are estimation experiments, and its “power” comparisons are rejection probabilities for pricing hypotheses, not investment performance.

## Common notation and population restrictions

For $N$ test assets and $K$ observed factors, write the time-series projection

$$
R_t=\alpha+\beta f_t+\varepsilon_t,
\qquad E(\varepsilon_t\mid f_t)=0.
$$

The $N\times K$ loading matrix is $\beta$, the residual covariance is $\Sigma$, the factor mean is $\mu_f$, and the factor covariance is $D$. The initial analysis assumes independent observations through time and a constant conditional residual covariance; normality is added where needed for likelihood or particular covariance expressions. The maintained beta-pricing restriction is

$$
\mu_R=\gamma_0\mathbf1_N+\beta\gamma_a=X\Gamma,
\qquad X=[\mathbf1_N,\beta],
\qquad \Gamma=(\gamma_0,\gamma_a')'.
$$

The intercept $\gamma_0$ and $K$ factor premia $\gamma_a$ are cross-sectional pricing parameters. They are not the time-series regression intercepts $\alpha$. If the factors are traded excess-return portfolios and the model has a zero pricing intercept, their own expected excess returns provide the corresponding premium restriction; the unrestricted cross-sectional regressions examined here need not impose it.

Estimate each asset's time-series regression on a constant and the same $K$ factors using all $T$ observations. Let $\hat\beta$, $\hat\alpha$, $\bar R$, $\bar f$, $\hat D$, and $\hat\Sigma$ denote the resulting estimates. In the likelihood formulas the sample second moments use divisor $T$. Keep this convention explicit: substituting a degrees-of-freedom-adjusted residual covariance in one formula but not another changes finite-sample results.

The two-pass estimate for a positive-definite weight $W$ is

$$
\hat\Gamma_W=(\hat X'W\hat X)^{-1}\hat X'W\bar R.
$$

OLS uses $W=I_N$, WLS uses $W=\operatorname{diag}(\hat\Sigma)^{-1}$, and GLS uses $W=\hat\Sigma^{-1}$. GLS requires an invertible residual covariance, which becomes problematic when the number of assets approaches the time-series sample size. The same full-sample betas are used in each cross-sectional regression. Averaging monthly cross-sectional estimates is then algebraically equivalent to regressing the average returns once. This is not a rolling-beta Fama–MacBeth design.

## Correctly specified two-pass inference

Let $A=(X'WX)^{-1}X'W$, $c=\gamma_a'D^{-1}\gamma_a$, and let $D_*$ be a $(K+1)\times(K+1)$ matrix with a zero intercept row and column and $D$ in its factor block. The asymptotic covariance of $\sqrt T(\hat\Gamma_W-\Gamma)$ is

$$
U=(1+c)A\Sigma A'+D_*.
$$

Divide its estimated version by $T$ to obtain the covariance of the premium estimator. The multiplier $1+c$ is the errors-in-variables correction associated with estimated betas. The $D_*$ term reflects uncertainty in average factor realizations. A conventional time-series covariance of monthly cross-sectional estimates does not, by itself, supply the full estimated-beta adjustment.

For GLS, write $\hat\eta=\bar R-\hat X\hat\Gamma_{GLS}$. The cross-sectional specification statistic is based on

$$
Q_C=\frac{T\hat\eta'\hat\Sigma^{-1}\hat\eta}{1+\hat c}.
$$

Its asymptotic reference is chi-squared with $N-K-1$ restrictions. The paper also uses the finite-sample approximation

$$
\frac{T-N+1}{T(N-K-1)}Q_C
\approx F_{N-K-1,T-N+1}.
$$

This approximation is not an exact distribution-free theorem for every return process. It is one of the procedures evaluated in the simulations.

The difference between OLS and GLS estimates provides another specification diagnostic. With $P=A_{GLS}-A_{OLS}$, its correctly specified asymptotic covariance is $(1+c)P\Sigma P'$. A Wald statistic based on the observed premium difference has a chi-squared reference with $K+1$ degrees of freedom when this covariance has full rank. If the model is correct, different weighting schemes should agree asymptotically. If it is not, they generally project expected returns onto the beta space differently.

## What changes under misspecification

Under misspecification define the population target separately for each weight:

$$
\Gamma_W=(X'WX)^{-1}X'W\mu_R,
\qquad
\eta_W=\mu_R-X\Gamma_W.
$$

The residual satisfies $X'W\eta_W=0$, but it need not vanish. OLS, WLS, and GLS now estimate different weighted approximations. Calling all of them biased estimates of one “true premium” is conceptually wrong unless an external target is specified.

Estimated betas perturb the fitted projection space. Estimated weights also matter when the population residual is nonzero. The paper's covariance result can be organized as

$$
U_{mis}=U+U_1+U_1'+U_2.
$$

Let $M=(X'WX)^{-1}$, $H=\operatorname{diag}(0,D^{-1})$, and let $V_W$ be the asymptotic covariance of $\sqrt T\operatorname{vec}(\hat W-W)$. One representation of the additional terms is

$$
U_1=-M
\begin{bmatrix}
0_{1\times N}\\
D^{-1}\gamma_a\eta_W'W\Sigma
\end{bmatrix}
WX M,
$$

$$
U_2=M\left[
(\eta_W'W\Sigma W\eta_W)H
+(\eta_W'\otimes X')V_W(\eta_W\otimes X)
\right]M.
$$

These expressions show why simply applying the familiar estimated-beta multiplier is insufficient when pricing errors persist. They also show why adding a universal positive “misspecification penalty” is too simplistic: the cross terms $U_1+U_1'$ need not be positive semidefinite.

For OLS the weight is fixed, so $V_W=0$. The derivation of the OLS extension does not require all the conditional-normal assumptions used to simplify the covariance of estimated WLS or GLS weights. For GLS, the weighted orthogonality condition eliminates $U_1$, and the remaining term simplifies to

$$
U_2=(\eta'\Sigma^{-1}\eta)\left(MHM+M\right),
\qquad M=(X'\Sigma^{-1}X)^{-1}.
$$

For WLS, covariance estimation contributes a matrix with entries proportional to $2\Sigma_{ij}^2\eta_i\eta_j/(\Sigma_{ii}^2\Sigma_{jj}^2)$ under the stated normal assumptions. Cross-asset residual dependence therefore matters even though the WLS point estimate uses only diagonal weights.

Appendix A makes the mechanism explicit by expanding the premium estimator into mean residual noise, estimated-beta noise, and the change in the projection of the nonzero pricing error. The population projection of $\eta$ is zero, but its sample projection is not. Ignoring that last random term is exactly what understates uncertainty in a misspecified model.

## Maximum likelihood: objective, computation, and extreme estimates

Define $\lambda_0=\gamma_0$ and $\lambda_a=\gamma_a-\mu_f$. The pricing restriction on the time-series intercept is

$$
\alpha=\lambda_0\mathbf1_N+\beta\lambda_a.
$$

Under the conditional-normal model, concentration over the loadings and covariance leads to minimizing

$$
Q(\lambda)=
\frac{(\hat\alpha-\lambda_0\mathbf1_N-\hat\beta\lambda_a)'
\hat\Sigma^{-1}
(\hat\alpha-\lambda_0\mathbf1_N-\hat\beta\lambda_a)}
{1+(\bar f+\lambda_a)'\hat D^{-1}(\bar f+\lambda_a)}.
$$

GLS minimizes a closely related quadratic numerator while holding the time-series beta estimates fixed. Likelihood allows the denominator and constrained beta fit to change. This distinction is responsible for its different finite-sample behavior; it is not merely GLS with a better standard error.

There is a convenient generalized-eigenvalue implementation. First remove the weighted constant from $\hat\alpha$ and every column of $\hat\beta$, giving $\alpha_*$ and $\beta_*$. Set

$$
A=[\alpha_*,-\beta_*]'\hat\Sigma^{-1}[\alpha_*,-\beta_*],
$$

$$
B=
\begin{bmatrix}
1+\bar f'\hat D^{-1}\bar f&\bar f'\hat D^{-1}\\
\hat D^{-1}\bar f&\hat D^{-1}
\end{bmatrix}.
$$

Solve $Av=\zeta Bv$ for the smallest generalized eigenvalue. If the first component $v_0$ is nonzero, normalize it to one and set $\hat\lambda_a=v_{1:K}/v_0$. Then

$$
\hat\lambda_0=
\frac{\mathbf1'\hat\Sigma^{-1}(\hat\alpha-\hat\beta\hat\lambda_a)}
{\mathbf1'\hat\Sigma^{-1}\mathbf1},
\qquad
\hat\gamma_a=\hat\lambda_a+\bar f.
$$

**Source implementation correction:** the main-text ordinary-eigenvalue construction whitens the generalized problem but does not explicitly restore the eigenvector to the original coordinates before normalizing it. If $L'L=B^{-1}$ and $u$ is an eigenvector of $LAL'$, the required vector is $v=L'u$. Normalizing $u$ directly as $(1,\lambda_a')'$ is generally incorrect. Solving the generalized problem directly, as suggested by the Appendix A Rayleigh quotient, avoids this omission. A nearly zero $v_0$ corresponds to extreme or boundary premium estimates; it is not a harmless sign-normalization issue.

Given the likelihood pricing parameters, constrained loadings can be obtained by regressing $R_t-\lambda_0\mathbf1$ on $f_t+\lambda_a$ without an intercept. Recompute the constrained residual covariance from that fit. The paper also supplies likelihood first-order conditions that can be used as a numerical check on the eigenvalue solution.

For a one-factor model the likelihood premium has the same sign as GLS and is farther from zero. More seriously, the untruncated likelihood estimator can have no finite moments in the relevant model. A Monte Carlo mean or RMSE of raw ML can then be dominated by rare extreme draws and need not stabilize as the simulation size grows.

The reported comparison therefore truncates ML: in the single-parameter description, if the absolute ML estimate is more than twice the absolute GLS estimate, replace it by GLS; otherwise retain ML. The source does not fully specify whether its multivariate implementation applies this componentwise or replaces an entire parameter vector when one component triggers the rule. The authors mention that a small positive floor can be needed for asymptotic reasoning when the population premium is zero; a complete operational floor convention is not specified. A sensitivity exercise with a multiplier of five is described as similar but not fully tabulated. This estimator should be called truncated ML, not untreated likelihood.

For specification testing the Bartlett-adjusted likelihood ratio has the form

$$
\left[T-\frac{N+K+3}{2}\right]
\log\frac{|\tilde\Sigma|}{|\hat\Sigma|}
\overset{a}{\sim}\chi_{N-K-1}^2.
$$

The distinction between the raw constrained-likelihood fit and a truncated premium vector should be retained in code and output. The publication's shorthand “ML” after introducing truncation is not a complete executable specification of every intermediate test calculation.

## GMM1: why a different label may conceal the same estimator

The first GMM method uses conditional pricing residuals

$$
\varepsilon_t(\theta)=R_t-\lambda_0\mathbf1-\beta(f_t+\lambda_a),
\qquad
z_t=(1,f_t')',
\qquad
E[\varepsilon_t(\theta)\otimes z_t]=0.
$$

There are $N(K+1)$ moments and $NK+K+1$ parameters, leaving $N-K-1$ overidentifying restrictions. With a separable weight $W_1\otimes W_2$, the problem can be reduced to a rank-$K$ multivariate regression and a one-dimensional optimization over $\lambda_0$.

For a reproducible orientation, let $Z$ be the $T\times(K+1)$ instrument matrix, $Y=R_{time}-\lambda_0\mathbf1_T\mathbf1_N'$, and define

$$
P=ZW_2Z',\qquad
S=Z'PZ/T^2,\qquad
C=Z'PY/T^2.
$$

Take the $K$ leading eigenvectors $E_K$ of $S^{-1/2}CW_1C'S^{-1/2}$ and form $\tilde A=S^{-1/2}E_K$. Partition $\tilde A$ into its first row $A_1$ and its remaining $K\times K$ block $A_2$. When $A_2$ is invertible,

$$
\lambda_a'=A_1A_2^{-1}.
$$

With $X_*=Z\tilde A$, the corresponding loading matrix satisfies

$$
\beta'=A_2(X_*'PX_*)^{-1}X_*'PY.
$$

The concentrated criterion is $\operatorname{tr}(W_1Y'PY/T^2)-\sum_{j=1}^K\zeta_j$, where $\zeta_j$ are the selected eigenvalues. Minimize it over $\lambda_0$, checking singular $A_2$ and boundary solutions. This gives a concrete implementation instead of an unspecified large nonlinear optimization over all betas and premia.

For the commonly used weight

$$
W_1=\hat\Sigma^{-1},\qquad
W_2=(Z'Z/T)^{-1},
$$

the GMM1 estimate is numerically equivalent to maximum likelihood. Appendix A proves this by concentrating the regression and recovering the same profile criterion. Merely changing the estimator's name does not remove ML's extreme-value problem or supply a different finite-sample point estimate.

For nonoptimal GMM weights, standard errors require a sandwich covariance using the derivative of the moments and their long-run covariance. A raw minimized quadratic form with an arbitrary weight is not automatically a chi-squared specification test. The appropriate projected-moment covariance must be used, or an optimal weighting scheme must be justified. When converting $\lambda_a$ to $\gamma_a$, uncertainty in the factor sample mean must also be incorporated. The paper discusses HAC inference in general, but does not supply a single universal lag rule for every application.

## GMM2: sequential estimation and nuisance adjustment

The second GMM construction first estimates return means, factor means, and factor covariances using their sample moments. It then uses pricing moments that contain the covariance-based beta representation. With $\mu_R$, $\mu_f$, and $D$ as nuisance parameters, a useful form is

$$
h_{2,t}=R_t-\gamma_0\mathbf1
-(R_t-\mu_R)(f_t-\mu_f)'D^{-1}\gamma_a.
$$

At the sample nuisance estimates, its mean is $\bar R-\hat X\Gamma$. The first-stage moments $h_{1,t}$ contain $R_t-\mu_R$, $f_t-\mu_f$, and all distinct entries of $(f_t-\mu_f)(f_t-\mu_f)'-D$. For multiple factors, omitting off-diagonal covariance moments would change the estimator and is particularly problematic when factors are correlated.

Let $D_{11}$ be the derivative of the first-stage moments with respect to nuisance parameters and $D_{21}$ the derivative of the pricing moments with respect to those parameters. The effective second-stage moment innovation is

$$
\psi_t=h_{2,t}-D_{21}D_{11}^{-1}h_{1,t}.
$$

This adjusts for estimating the nuisance moments. Use its covariance, or long-run covariance where appropriate, to construct the optimal second-stage weight $W_2$. Conditional on a given estimated weight,

$$
\hat\Gamma_2=(\hat X'W_2\hat X)^{-1}\hat X'W_2\bar R,
\qquad
\operatorname{Avar}(\hat\Gamma_2)
=\frac1T(X'W_2X)^{-1}.
$$

The specification statistic is $T\bar h_2'W_2\bar h_2$, with $N-K-1$ asymptotic degrees of freedom under correct specification and optimal weighting.

The effective covariance depends on pricing parameters through $h_2$ and $D_{21}$. An implementation therefore needs a preliminary consistent estimate and a stated choice about whether to iterate the weight. The conditional analytical formula does not eliminate this operational choice, which is not fully documented in the numerical study. Likewise, a displayed negative derivative $D_{22}=-X$ must be handled consistently when translating the source's notation into the positive regression formula above.

The authors tried an additional one-step optimal-GMM scoring approach but found severe finite-sample overrejection, exceeding 90% for a nominal 5% test even with 960 observations in some designs. It is not one of the reliable procedures endorsed by the comparison.

## Monte Carlo design

The calibration uses monthly data from January 1964 through December 2003: 25 Fama–French size/book-to-market portfolios or 48 industry portfolios, with either one market factor or three factors. Betas and residual covariances are estimated from the 480-month historical sample. The full calibrated coefficient and covariance matrices and the exact historical data vintage are not printed, so the experiment is reproducible in design but not bit-for-bit from the article alone.

In the Gaussian design, factor realizations and residuals are generated from the calibrated moments, and the asset intercepts are set to satisfy the chosen pricing restriction. There are 10,000 replications per experiment. With 25 assets, sample lengths are 60, 120, 240, 360, 480, and 960 months. The 48-asset experiments omit the shortest case because covariance estimation becomes too close to singularity.

The one-factor premium is 0.6667% per month, corresponding to 8% by simple annual multiplication. The pricing intercept is 0.0833% monthly, corresponding to a 1% annual difference from the risk-free return. In the three-factor simulation, the premium ordering is market, book-to-market, and size: 0.6667%, 0.3333%, and 0.1667% monthly. The empirical application later uses the familiar market, SMB, HML display order; confusing those orders would swap the latter two calibration values.

For parameter tests, the parameter being tested is set to zero in the null simulation while the remaining values retain their calibration. Nominal tests are two-sided 5% tests. Power comparisons are intended to use empirical null critical values so that size distortion is not counted as power. This adjustment should be regenerated independently for each estimator and design.

The nonnormal experiment uses a multivariate Student distribution with eight degrees of freedom and the same covariance calibration. A common scale mixture induces conditional heteroskedasticity. It is not a fitted GARCH or serially persistent stochastic-volatility simulation. A covariance-preserving Student generator must scale the Gaussian component appropriately; using an unadjusted $t_8$ draw would inflate covariance by $8/6$.

For a rejection probability near 5%, the ordinary Monte Carlo standard error with 10,000 independent replications is about 0.00218, or 0.22 percentage points. This is a calculation from the simulation size, not an uncertainty figure reported by the authors. Differences of several percentage points in size are much larger than this simulation noise.

## Main finite-sample results

All premium numbers in this section are percentages per month. In the 25-asset, one-factor, 360-month design, the true market premium is 0.6667. Table 1 gives:

| Estimator | Mean estimate | RMSE |
|---|---:|---:|
| OLS | 0.6554 | 0.5041 |
| WLS | 0.6511 | 0.4953 |
| GLS | 0.6153 | 0.3492 |
| GMM2 | 0.6152 | 0.3498 |
| Truncated ML | 0.6639 | 0.3730 |

GLS gives up some mean accuracy in return for substantially lower dispersion. Truncated ML is close to unbiased here, but its RMSE is still higher than GLS. With 48 assets and 360 months, market-premium means and RMSEs are 0.6372 and 0.3865 for OLS, 0.6042 and 0.3185 for GLS, and 0.6716 and 0.3480 for truncated ML.

Raw ML is especially unstable in short samples. For the 25-asset 60-month example discussed in the text, its sample RMSE is about 6.4, versus 1.1241 after truncation. Because raw ML can lack finite moments, the first number is a finite simulation diagnostic rather than a well-defined population RMSE estimate. At 960 months, precision differences still remain: the 25-asset market-premium RMSE is about 0.3114 for OLS, 0.2153 for GLS, and 0.2206 for truncated ML. An informal claim that all methods become essentially identical should not override those table values.

Percentage bias can exaggerate the visual importance of small intercept errors. In the 25-asset 360-month design, the GLS intercept mean is 0.1304 against a true 0.0833, a relative bias near 56%, but its RMSE is 0.2698. The absolute signal is small compared with its sampling uncertainty.

Estimated standard errors can be much too optimistic. For the 48-asset 120-month intercept, the ML RMSE is 0.5826, the asymptotic standard error evaluated at population parameters is 0.3822, and the average estimated asymptotic standard error is 0.2609. There are two problems: the asymptotic approximation itself understates finite-sample uncertainty, and plugging in noisy estimates worsens it. The comparable OLS values are 0.5312, 0.5699, and 0.5035, much closer to one another.

This translates into size distortion. In the 25-asset 60-month intercept test, nominal 5% rejection rates are 5.87% for OLS, 28.42% for GLS, and 38.08% for ML. Even at 480 months with 48 assets, the ML intercept rejection rate is about 10.05%. A premium estimate with a small conventional p-value can therefore look more decisive than its actual sampling behavior warrants.

GLS and ML often have more ability to detect a nonzero market premium than OLS once size is considered, but the source's power tables need one caution. The ML intercept entries in Table 4a track the heavily distorted nominal rejection rates unusually closely; for example, the short-sample reported value is about 0.3902 versus null rejection near 0.3808. This is difficult to reconcile with a clean size-adjusted interpretation. The corresponding Table 4b entries behave differently. A replication should recompute empirical critical values rather than use those cells as unambiguous evidence of power gains.

Three-factor results are also premium specific. With 48 assets and 360 months, the book-to-market premium has mean/RMSE pairs 0.3398/0.2237 for OLS, 0.3319/0.1975 for GLS, 0.3065/0.1836 for GMM2, and 0.3331/0.2060 for ML, against a true 0.3333. GMM2 has lower RMSE at the cost of noticeable downward bias. Choosing a method solely by unbiasedness would miss that tradeoff.

Specification tests generally behave better than some individual-parameter tests, but not perfectly. For 25 assets, one factor, and 360 months, the GLS cross-sectional test rejects about 4.87% under the null, while the likelihood ratio rejects about 6.05%. In the three-factor design, likelihood and GMM2 rejection rates are approximately 7.5% and 6.71% in the corresponding comparison. No method's nominal chi-squared calibration should be treated as guaranteed in every dimension/sample configuration.

## Misspecification experiments and empirical application

To study misspecification, the authors add empirically calibrated pricing errors to the 25-portfolio CAPM or fixed simulated pricing errors to the 48-industry design. For the latter, the pricing-error standard deviation is 0.1667% monthly. Betas and residual covariance remain calibrated as before. The true target is then the weight-specific population projection, not the original imposed premium.

For the 25-asset misspecified example, population intercept projections are about 1.03%, 0.76%, and 1.01% monthly under OLS, WLS, and GLS; associated market slopes are approximately −0.06%, 0.14%, and −0.25%. For 48 assets, the corresponding intercepts are about 0.22%, 0.28%, and 0.52%, with market slopes 0.55%, 0.48%, and 0.20%. These differences are not Monte Carlo bias. They are different population objects induced by different weights.

Misspecification-adjusted standard errors can improve agreement with actual dispersion. In the 25-asset 360-month GLS slope example, the asymptotic standard error rises from about 0.3408 to 0.3719 when misspecification is incorporated, versus RMSE about 0.3647. The full correction is relevant even though the point estimate remains the same weighted projection.

The direct pricing-error test is more powerful than the OLS-versus-GLS comparison in these examples. With 25 assets, the former's power is about 81.49% at 240 months and 96.60% at 360 months, versus 45.75% and 63.24% for the estimator-difference test. With 48 assets and 360 months, the comparison is about 92.15% versus 31.46%. Agreement between OLS and GLS is therefore not strong evidence that a pricing model is correct.

The empirical application uses the 25 size/book-to-market portfolios over 1964–2003, with returns in excess of the 30-day Treasury-bill return. Imposing a zero pricing intercept gives sample factor means of approximately 0.45% monthly for the market, 0.27% for SMB, and 0.43% for HML, with standard errors 0.21%, 0.15%, and 0.14%.

Allowing a free cross-sectional intercept changes the market premium sharply. OLS estimates an intercept of 1.42% monthly and a market premium of −0.93%; GLS estimates 1.60% and −1.09%; ML estimates approximately 1.85% and −1.35%. The size and value premia remain much closer to their constrained values. For OLS, misspecification adjustment raises the intercept standard error from 0.32% to 0.36% and the market-premium standard error from 0.38% to 0.42%. For GLS, the corresponding changes are approximately 0.29% to 0.32% and 0.35% to 0.38%.

These negative cross-sectional market slopes should not be described as direct estimates of a negative expected market return. The test portfolios have market betas clustered around one, so a high fitted intercept can be offset by a negative market coefficient with relatively little change in fitted expected returns. This is a projection and identification problem within a rejected model.

Allowing the intercept reduces mean absolute pricing errors from about 10.5 to 8.9 basis points per month, roughly a 15% reduction. The small-growth portfolio still has a large negative alpha: around −45 basis points under the constrained model and approximately −32 to −37 under the unrestricted alternatives. The model continues to be rejected by the reported specification tests. Table probabilities printed as 0.00 are rounded, not literally zero. The OLS–GLS difference test has statistic about 8.80 and probability 0.07, illustrating again that weak disagreement between estimators does not rescue a rejected pricing model.

## Reimplementation checklist and interpretive limits

A serious replication should preserve monthly percentage units, factor ordering, divisor conventions, and the separation between time-series intercepts, cross-sectional intercepts, $\lambda$ parameters, and $\gamma$ premia. Use a generalized eigenproblem for ML, retain raw and truncated estimates separately, and diagnose singular or nearly singular normalizations. Verify GMM1/ML numerical equivalence under the matching separable weight before treating them as independent benchmarks. For GMM2, record the initial estimate and weight-update rule.

The Monte Carlo output should separate bias, RMSE, asymptotic standard errors evaluated at true parameters, estimated standard errors, nominal size, and size-adjusted power. Under misspecification, compare estimates with their own population weighted-projection targets. Inference on a premium and inference on model specification are distinct tests with distinct finite-sample behavior.

The missing exact calibration matrices, data vintage, random seeds, truncation-floor convention, some GMM weighting details, and ambiguities in particular power-table cells prevent exact numerical regeneration from the paper alone. They do not prevent reproducing the central econometric comparison. Its lasting lesson is that point-estimation efficiency, bias, tail stability, standard-error accuracy, and specification-test power are different objectives. A method can improve one while materially worsening another, and weighting choices become part of the estimand once the pricing model is wrong.

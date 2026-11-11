# Empirical Evaluation of Asset-Pricing Models: A Comparison of the SDF and Beta Methods

**Ravi Jagannathan and Zhenyu Wang (2002).** *Journal of Finance* 57(5), 2337–2367. Source: [StochasticDiscount_JagannathanWang_2002.pdf](../../Finance/StochasticDiscount_JagannathanWang_2002.pdf). The local file contains all 31 published pages, including the proof appendix. Printed page 2337 is PDF page 1. This note follows the published version, not the earlier working paper entitled *Efficiency of the Stochastic Discount Factor Method for Estimating Risk Premiums*.

## Why this matters and what is new

Equivalent population asset-pricing restrictions need not produce equivalent estimates when an empirical comparison changes the information set, the parameter being estimated, or the moment conditions. The paper disentangles those issues in the debate over stochastic discount factor (SDF) estimation versus beta regressions. Its central innovation is a fair comparison: transform both estimators into the same risk-premium parameter, propagate uncertainty in the factor mean and variance, and supply both estimators with the same information.

Under the paper's i.i.d. joint-normal one-factor model, optimally weighted GMM applied to the SDF and beta representations has the same asymptotic precision for the transformed risk-premium parameter. In calibrated finite samples the precision is also similar. If the population mean and variance of the factor really are known, adding their moment restrictions to SDF estimation recovers the efficiency that a beta regression already obtains from that knowledge. Standardizing a factor using population moments and then treating those moments as known is therefore not an innocuous computational normalization.

There are two distinct results about testing. The sample SDF pricing-error vector has a larger asymptotic covariance than its appropriately transformed beta counterpart. Nevertheless, the two GMM overidentification statistics have the same null degrees of freedom, and the simulations find similar power against specified nonzero-alpha alternatives. Neither equal null distributions nor these particular experiments prove identical power against every misspecification. In particular, they do not dispose of the useless-factor experiments emphasized by Kan and Zhou (1999). Keeping this distinction is essential when applying the paper to weakly identified macroeconomic factors.

The application is an estimator experiment calibrated to historical portfolios, not a profitable trading strategy or a successful empirical test of the CAPM. There is no out-of-sample investment rule, transaction-cost model, or claimed investable Sharpe ratio.

## Population model, normalization, and parameter map

Let $r_t$ be an $n\times1$ vector of excess returns, $f_t$ one scalar factor, $\mu=E[f_t]$, and $\sigma^2=\operatorname{Var}(f_t)>0$. Define the beta vector and beta risk premium by

$$
\beta=\frac{\operatorname{Cov}(r_t,f_t)}{\sigma^2},\qquad E[r_t]=\delta\beta.
$$

The corresponding regression is

$$
r_t=(\delta-\mu+f_t)\beta+\varepsilon_t,
\qquad E[\varepsilon_t]=0,\qquad E[\varepsilon_t f_t]=0.
$$

The intercept in an unrestricted regression on $f_t$ is $(\delta-\mu)\beta$ under the model. For a traded excess-return factor included consistently in the pricing system, $\delta=\mu$. The primary analysis treats the factor as nontraded, so this equality is not imposed. Calibrating a simulated factor to market-return moments does not automatically impose the traded-factor restriction.

For excess returns, the same restrictions can be written using the normalized linear kernel $m_t=1-\lambda f_t$:

$$
E[r_t(1-\lambda f_t)]=0,
\qquad
\lambda=\frac{\delta}{\sigma^2+\mu\delta},
\qquad
\delta=\frac{\lambda\sigma^2}{1-\mu\lambda}.
$$

These maps require their denominators to be nonzero. They also show why $\lambda$ and $\delta$ are different statistical targets. Changing the units of $f$ by a factor of 100 multiplies $\delta$ by 100 and divides $\lambda$ by 100. A comparison of their raw variances would consequently change by eight orders of magnitude without changing the economic problem. Even if $\mu=0$ and $\sigma^2=1$ make the true numerical values equal, their estimators can inherit different sampling uncertainty.

Here an SDF is a pricing functional for excess returns. Its level is normalized by setting the intercept to one. The authors deliberately omit the additional restriction that it correctly prices the nominal risk-free security, citing persistent interest rates and the desire to match earlier comparisons (pp. 2342–2343). Positivity of this linear kernel is not imposed. The analysis therefore must not be read as constructing a globally positive consumption marginal-utility process or as jointly fitting a risk-free term structure.

Let $\alpha=E[r]-\delta\beta$ denote Jensen's alpha, and let $\pi=E[r]-\lambda E[rf]$ denote SDF pricing errors. Algebra gives

$$
\pi=\frac{\sigma^2}{\sigma^2+\mu\delta}\alpha.
$$

Thus their population zeros agree wherever the transformation is defined. Their sample versions and standard errors still must be transformed before comparison.

## Estimation systems that can be implemented directly

The beta method estimates $\theta=(\delta,\beta',\mu,\sigma^2)'$ from the $2n+2$ moments

$$
g_{b,t}(\theta)=
\begin{pmatrix}
r_t-(\delta-\mu+f_t)\beta\\
[r_t-(\delta-\mu+f_t)\beta]f_t\\
f_t-\mu\\
(f_t-\mu)^2-\sigma^2
\end{pmatrix}.
$$

There are $n+3$ parameters and hence $n-1$ overidentifying restrictions. The factor variance moment can be dropped when variance is not needed for the chosen target, but it is necessary for the explicit $\delta$-to-$\lambda$ comparison. Estimate all nuisance parameters jointly; do not plug in sample moments and then treat them as constants in inference.

The basic SDF method estimates only $\lambda$, using

$$
g_{s,t}(\lambda)=r_t(1-\lambda f_t).
$$

It also has $n-1$ overidentifying restrictions. For either system let $\bar g_T$ be its sample mean and $\widehat S$ an estimated covariance or long-run covariance of the moments. Efficient GMM minimizes

$$
\widehat\theta=\arg\min_\theta\bar g_T(\theta)'\widehat S^{-1}\bar g_T(\theta),
\qquad J=T\bar g_T(\widehat\theta)'\widehat S^{-1}\bar g_T(\widehat\theta).
$$

For fixed weighting matrix $W$, the scalar SDF update is particularly simple. Set $a=T^{-1}\sum r_t$ and $b=T^{-1}\sum r_tf_t$; then $\widehat\lambda=(b'Wb)^{-1}b'Wa$, provided $b'Wb>0$. Recompute moments and weights and iterate. This is an implementation consequence of the displayed objective; it is not an extra estimator proposed by the authors.

The simulations iterate between the weighting matrix and parameters until convergence, following Ferson–Foerster. They do not give a starting-weight convention, numerical tolerance, optimizer, singular-matrix rule, or random seed. Those inputs must be specified in a reproduction and checked for sensitivity. Their simulations are independent over time, so a lag-zero covariance suffices for the intended design; a serially dependent real-data application requires an appropriate long-run covariance estimator and cannot inherit the normal-i.i.d. closed forms automatically.

From the beta fit construct

$$
\widehat\lambda_b=\frac{\widehat\delta}{\widehat\sigma^2+\widehat\mu\widehat\delta},
\quad
\widehat\alpha_b=\bar r-\widehat\delta\widehat\beta,
\quad
\widehat\pi_b=\frac{\widehat\sigma^2}{\widehat\sigma^2+\widehat\mu\widehat\delta}\widehat\alpha_b.
$$

The SDF counterpart is $\widehat\pi_s=\bar r-\widehat\lambda_s\overline{rf}$. Standard errors for transformed parameters use the joint covariance, including estimated factor moments. Equivalently, reparameterize the beta moments in terms of $\lambda$ and estimate jointly. The latter is a useful numerical cross-check.

## Exact efficiency result and proof mechanism

The analytic comparison assumes i.i.d. joint normality of returns and factor, $\varepsilon_t$ independent of $f_t$, a nonsingular residual covariance $\Omega$, and the usual identification and GMM regularity conditions. Write

$$
H=\beta'\Omega^{-1}\beta,\qquad K=\sigma^2+\mu\delta.
$$

The appendix's asymptotic variances are variances of the $\sqrt T$ limits. Divide by $T$ for approximate estimator variance. Equations A4 and A14 imply

$$
\operatorname{Avar}(\widehat\lambda_s)
=\operatorname{Avar}(\widehat\lambda_b)
=\frac{\sigma^2(\sigma^2+\delta^2)}{K^4}H^{-1}
+\frac{\sigma^2(\sigma^4+\delta^4)}{K^4}.
$$

For the beta premium itself, equation A13 gives

$$
\operatorname{Avar}(\widehat\delta)
=\frac{\sigma^2+\delta^2}{\sigma^2}H^{-1}+\sigma^2.
$$

The proof computes the covariance of each moment vector and its expected derivative, applies $(D'S^{-1}D)^{-1}$, and uses the delta method on the beta estimate. In particular,

$$
S_s=\frac{\sigma^2}{K^2}
\left[(\sigma^4+\delta^4)\beta\beta'+(\sigma^2+\delta^2)\Omega\right],
\qquad D_s=-K\beta.
$$

This rank-one-plus-residual form permits direct matrix inversion. The beta moment covariance is block diagonal between the regression moments and the factor-mean/variance moments under normality. Its inverse and Jacobian yield the extra uncertainty associated with estimating $\mu$ and $\sigma^2$. That uncertainty is precisely what is lost in an unfair known-moments comparison.

For pricing errors define the positive-semidefinite matrix

$$
Q=\Omega-H^{-1}\beta\beta'.
$$

Equations A7 and A19 give

$$
\operatorname{Avar}(\widehat\pi_s)
=\frac{\sigma^2(\sigma^2+\delta^2)}{K^2}Q,
\qquad
\operatorname{Avar}(\widehat\pi_b)
=\frac{\sigma^6}{(\sigma^2+\delta^2)K^2}Q.
$$

Their difference is positive semidefinite, and their scalar covariance multipliers have ratio $(1+\delta^2/\sigma^2)^2$. This is a statement about fitted pricing-error vectors. It does not contradict equal efficiency for the risk premium, nor does it by itself establish a uniformly more powerful specification test.

For the traded-factor restriction $\delta=\mu$, correctly imposing the restriction makes the premium estimate reduce asymptotically to the factor sample mean. Both representations then have that mean's asymptotic variance. Applying the nontraded calibration to a traded-factor claim without imposing the restriction would compare different models.

## Known moments, standardization, and the information advantage

If $\mu$ and $\sigma^2$ are known population constants, beta GMM can omit their estimating equations and parameters. Its transformed-premium variance becomes only the first term in the preceding common variance:

$$
\operatorname{Avar}(\widehat\lambda_{b,\mathrm{known}})
=\frac{\sigma^2(\sigma^2+\delta^2)}{K^4}H^{-1}.
$$

Basic SDF moments contain neither nuisance parameter, so simply declaring the factor moments known does not change their estimator. The information must enter through additional moments:

$$
E\begin{bmatrix}
r_t(1-\lambda f_t)\\
f_t-\mu\\
(f_t-\mu)^2-\sigma^2
\end{bmatrix}=0.
$$

With fixed known $\mu,\sigma^2$, these are additional restrictions, not additional parameters, and efficient GMM attains the known-moments beta variance (equations 22–25, A32–A37). When those moments instead estimate two unknown parameters, the two new equations do not supply the same information gain.

The general lemmas explain the mechanism. Fixing nuisance parameters weakly lowers an efficient GMM estimator's variance. Adding valid moments also weakly lowers variance, with no gain if the added moments are orthogonal in the long-run covariance metric to the original ones under the stated sufficient conditions. The regression residual moments are orthogonal to known factor-moment restrictions in the normal model, while SDF pricing moments are not. Information can therefore be implicit in one representation but absent from another.

Sample standardization is different: estimating and subtracting $\bar f$ and dividing by a sample standard deviation introduces generated-data dependence. It cannot be treated as if the transformed observations were independent draws with population moments known for free. A replication should either keep raw factor units and estimate their moments or carry the entire transformation through the joint influence function.

## Reconstructing the Monte Carlo experiment

Section III calibrates to CRSP monthly January 1926–December 1998 returns for ten size-decile portfolios, a value-weighted NYSE/AMEX/Nasdaq market index, and one-month Treasury bills. Subtract bills to obtain excess returns. Fit ten OLS time-series regressions on the market excess return. Set $\beta$ to their slopes, $\Omega$ to their residual covariance, and factor moments to the market's sample moments. Set $\delta$ from the cross-sectional regression of mean returns on betas. The paper supplies the resulting parameter matrix, so the main simulation can be reproduced without rebuilding historical CRSP deciles.

Use decimal monthly returns. The calibration is $\mu=0.006914$, $\sigma=0.055154$, $\delta=0.013740$, and $\lambda=4.3790$. The caption explicitly describes percentage scaling for $\mu,\sigma,\alpha$ and covariance scaling by 10,000; the displayed $\delta=1.3740$ must likewise be interpreted as percent to satisfy its defining map. Inserting 1.3740 as a decimal premium would be inconsistent with $\lambda=4.3790$.

The beta vector, ordered smallest to largest, is $(1.460,1.395,1.309,1.265,1.241,1.227,1.183,1.122,1.090,0.947)'$. The calibrated alternative-alpha vector in percentage points is $(0.494,0.126,0,-0.004,0,-0.002,0.020,-0.042,0.023,0.003)'$. Divide it by 100. The full $10^4\Omega$ matrix is:

```text
55.680 37.110 28.820 22.300 17.390 14.450 10.160  6.375  3.890 -2.808
37.110 29.830 22.620 17.880 13.960 11.870  8.296  5.466  3.172 -2.243
28.820 22.620 20.480 15.180 11.860 10.300  7.265  4.932  2.784 -1.918
22.300 17.880 15.180 13.670 10.120  8.860  6.638  4.770  2.633 -1.687
17.390 13.960 11.860 10.120  9.290  7.432  5.616  4.134  2.404 -1.422
14.450 11.870 10.300  8.860  7.432  7.312  5.097  3.838  2.334 -1.301
10.160  8.296  7.265  6.638  5.616  5.097  4.901  3.289  1.944 -1.036
 6.375  5.466  4.932  4.770  4.134  3.838  3.289  3.254  1.776 -0.840
 3.890  3.172  2.784  2.633  2.404  2.334  1.944  1.776  1.775 -0.572
-2.808 -2.243 -1.918 -1.687 -1.422 -1.301 -1.036 -0.840 -0.572  0.312
```

These signs were checked against the rendered Table I; text extraction can turn a minus into a leading 2. Printed rounding may affect positive definiteness in a numerical recreation. Report any regularization rather than silently altering the covariance.

For each $T\in\{60,120,360,600\}$, draw independent $f_t\sim N(\mu,\sigma^2)$ and $\varepsilon_t\sim N(0,\Omega)$ and set $r_t=(\delta-\mu+f_t)\beta+\varepsilon_t$. Repeat 1,000 times for estimator standard deviations. Estimate four variants: ordinary beta, ordinary SDF, beta with known factor moments, and SDF augmented with the known factor moments. The normal experiment imposes the pricing null exactly; it does not use raw empirical returns as if the null were true.

For the heavy-tailed version, draw the factor and residual vector jointly from a covariance-matched multivariate Student distribution with five degrees of freedom. One reproducible construction is a block-independent Gaussian vector multiplied by the same random scale $\sqrt{(\nu-2)/U}$, $U\sim\chi^2_\nu$, with $\nu=5$. This common scale induces dependence despite zero unconditional covariance. It gives the paper's conditional residual covariance

$$
\operatorname{Var}(\varepsilon_t\mid f_t)
=\frac{\nu-2+(f_t-\mu)^2/\sigma^2}{\nu-1}\Omega.
$$

Five degrees of freedom preserve finite fourth moments while creating conditional heteroskedasticity. This is cross-sectional factor-dependent heteroskedasticity in independent draws, not a persistent GARCH time series.

The empirical-distribution experiment jointly resamples the observed market factor and the corresponding vector of regression residuals, then reconstructs returns under the pricing model. Do not resample each coordinate separately. The paper reports the bootstrap version; an alternative smoothed empirical generator gave similar results. Exact replication of this panel requires the original return/residual observations, which the PDF does not provide.

## Numerical evidence and the size–power distinction

Table II reports standard deviations of estimated $\lambda$, not standard deviations of $\delta$. At $T=360$, the normal asymptotic benchmark is 0.9007 for both ordinary methods; the simulated beta and SDF values are 0.9616 and 0.9560. The known-moments counterparts are both 0.0270 in simulation, against asymptotic 0.0266. Thus the apparently dramatic roughly 35-fold precision difference is obtained by comparing unequal information treatments.

At $T=60$, ordinary beta/SDF standard deviations are 3.1193/2.8903 under normality and 4.3511/3.4108 under the five-degree Student distribution. These are similar in broad scale but not numerically equal; small-sample asymptotic approximations are imperfect. At $T=600$, normal values are 0.7307/0.7279, Student values 0.8235/0.8127, and empirical-bootstrap values 0.7321/0.7306. The main equality becomes a good approximation with longer samples.

Table III demonstrates that pricing-error precision is a separate object. At $T=360$, asymptotic pricing-error standard deviations for the smallest decile are 0.3699 percentage points for beta and 0.3928 for SDF; for the largest decile they are 0.0267 and 0.0283. The normal simulated values for those two portfolios are 0.3863/0.4115 and 0.0454/0.0491. The beta advantage is real but modest in this calibration, and finite-sample behavior is especially different for very small theoretical errors.

For specification tests, repeat the simulation 10,000 times to estimate tail rejection probabilities at nominal 10%, 5%, and 1%. For size set $\alpha=0$; for power use the supplied nonzero alpha vector in

$$
r_t=\alpha+(\delta-\mu+f_t)\beta+\varepsilon_t.
$$

Ordinary beta and SDF have nine null degrees of freedom. With known factor moments, beta still has nine; the augmented SDF has twelve moments and one parameter, hence eleven. Its additional overidentifying restrictions also test the known factor moments. The caption describes null-distribution critical points, while the surrounding text discusses chi-square critical values; the PDF does not give a separate numerical critical-value vector or an explicit size-adjustment algorithm. A reproduction should disclose which convention it implements.

At nominal 5%, normal-null rejection rates at $T=60$ are 2.9% beta and 3.2% SDF, rising at $T=360$ to 4.7% for both. Normal-alternative power is 4.6%/5.3% at 60, 36.7%/36.9% at 360, and 62.3%/62.3% at 600. These results establish that both methods have limited power in short samples against this alternative, not that a nonsignificant result verifies a pricing model.

With Student draws, ordinary-method null rates at $T=360$ are 4.1%/4.3%, and alternative rates are 35.9%/36.9%. The augmented known-moment SDF deserves separate caution: its nominal-5% null rate is 14.4% at $T=60$ and 8.8% even at $T=600$. Its elevated alternative rejection rate therefore cannot be interpreted wholly as superior power. With 10,000 independent repetitions, a rejection probability near 5% has binomial Monte Carlo standard error about 0.22 percentage points; near 50% it is about 0.5 points. These are calculated diagnostics, not confidence intervals printed by the authors.

## Limits, source errors, and practical conclusions

The theoretical equality is established in the stated regular normal model; Student and empirical simulations support robustness for these designs. They are not a proof covering arbitrary nonnormality, serial dependence, weak identification, changing betas, or misspecification. A factor with little covariance with returns can make $b'Wb$ nearly zero and the SDF parameter unstable. Equal asymptotic variances under a well-identified null do not repair that problem.

The article itself recognizes that alternative hypotheses differ across studies. Its calibrated-alpha experiment is not the useless-factor experiment in Kan–Zhou. Moreover, two statistics having the same central chi-square null limit does not imply equal noncentral limits under every local alternative. The broad abstract language about testing power should be read with Section III's narrower design in mind.

There are printed algebraic traps in the appendix. In A34 the upper-right covariance entry has denominator $\sigma^4+\mu\delta$, while its transposed lower-left entry has $\sigma^2+\mu\delta$. A covariance matrix must be symmetric; direct evaluation from the defining moments gives $-2\delta\sigma^4\beta/K$ in both transposed positions. Implement the moment covariance from its definition, or use this symmetric expression. The proof's main variance formulas A4, A13, A14, A19, A32, and A37 are the operational formulas used above. Numerical matrix calculations offer a useful independent check before reproducing the displayed intermediate inverses.

Other missing implementation inputs include full-precision calibration estimates, raw historical bootstrap observations, convergence tolerances, and failed-fit handling. The paper reports no trading frictions because the experiment concerns statistical efficiency, not realized investment performance. It also does not establish the economic correctness of the calibrated single-factor model: its unusually large fitted monthly premium partly reflects the relation between size and beta in the chosen deciles.

For an empirical implementation, decide first whether the factor is traded, whether its population moments are known, and which economic premium is the target. Then write all moments explicitly, retain nuisance-parameter uncertainty, use common units, and compare like with like. This makes the paper useful even when its normal-theory equality is only an approximation: it gives a disciplined way to detect an information advantage masquerading as a superior estimation framework.

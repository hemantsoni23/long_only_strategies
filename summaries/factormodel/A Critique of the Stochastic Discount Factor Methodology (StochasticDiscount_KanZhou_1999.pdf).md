# A Critique of the Stochastic Discount Factor Methodology

**Raymond Kan and Guofu Zhou (1999).** *Journal of Finance* 54(4), 1221–1248. DOI: [10.1111/0022-1082.00145](https://doi.org/10.1111/0022-1082.00145). Source: [StochasticDiscount_KanZhou_1999.pdf](../../Finance/StochasticDiscount_KanZhou_1999.pdf). The local PDF has 33 pages: one JSTOR cover, the 28-page published article including its appendix, and four appended linked-reference pages. Printed page 1221 is PDF page 2. The full article and appendix were read; equations missing from the text layer and the three tables were inspected as rendered pages. This note preserves the 1999 argument while distinguishing it from later qualifications to the efficiency comparison.

## Why this matters

A factor can satisfy a pricing restriction without being a persuasive description of systematic return risk. Moreover, a high GMM specification-test p-value may reflect poor identification, imprecise moments, or weak power rather than a good model. This paper makes those dangers concrete using linear-factor algebra and calibrated Monte Carlo experiments.

There are three substantive components. First, explicit noisy and residual-based factors price the chosen assets even though they have a weaker economic interpretation than the true return-generating factor. Second, in the paper's standardized-factor experiment, regression-based moments estimate the premium much more precisely than the basic SDF moments. Third, omitting the dominant factor from a two-factor model produces a particularly severe power failure for the basic SDF overidentification test.

The second component requires a prominent qualification. The experiment treats the factor's population mean as zero and its variance as one without estimating them. These known moments provide information that the basic SDF estimator does not explicitly use. A later direct comparison, Jagannathan and Wang (2002), shows that when factor moments are estimated and both estimators target the same transformed parameter, asymptotic precision agrees in their regular i.i.d. normal model. If moments truly are known, supplying the associated moment restrictions to SDF GMM restores that efficiency. Thus the 1999 simulation is a valid comparison of the particular implementations it defines, not proof that the SDF representation is inherently inefficient. The later source is [Empirical Evaluation of Asset-Pricing Models](../../Finance/StochasticDiscount_JagannathanWang_2002.pdf), especially Section II; it was read separately for this qualification.

That distinction does not negate the factor-interpretation or weak-power examples. It tells the reproducing researcher what must be held fixed: the population model, information available to each estimator, parameter units, and the alternative hypothesis used to evaluate power.

## Model, normalization, and what is being tested

Let $r_t$ be an $N$-vector of returns in excess of a risk-free return. The return-generating process is

$$
r_t=\alpha+\beta f_t+\varepsilon_t,
\qquad E[\varepsilon_t\mid f_t,\mathcal F_{t-1}]=0,
\qquad \operatorname{Var}(\varepsilon_t)=\Sigma.
$$

The factor is a martingale difference, $E[f_t\mid\mathcal F_{t-1}]=0$, and the main comparison sets its unconditional variance to one. Expected excess returns are the constant vector $\alpha$; $\beta$ is a constant vector of loadings. The trivial all-zero expected-return case is excluded. Conditional heteroskedasticity in residuals is allowed in the broader GMM setup; constant conditional residual covariance is imposed for the normal likelihood benchmark.

The exact beta-pricing restriction is

$$
\alpha=\beta\lambda.
$$

Here $\lambda$ is the premium on a factor standardized to unit volatility, so it is dimensionless if returns and betas use matching decimal units. It is not directly an unstandardized monthly market mean. For a true standardized market factor under the CAPM it equals the market Sharpe ratio.

The corresponding normalized SDF restriction is

$$
E[r_t(1-\lambda f_t)]=0.
$$

Because $E[f_t]=0$ and $E[f_t^2]=1$, $E[r_tf_t]=\beta$, so both displayed restrictions use the same numerical population coefficient. The kernel is normalized to have intercept one because excess-return pricing is unchanged by multiplying the kernel by a nonzero constant. The paper does not jointly price the risk-free asset or impose positivity of $1-\lambda f_t$. With a nondegenerate Gaussian factor and nonzero $\lambda$, that affine kernel is negative with positive probability. It is therefore a linear pricing functional for the selected excess returns, not automatically a positive state-price density for all contingent claims.

The tests are unconditional tests of an unconditional model. They do not multiply pricing errors by an extensive set of dated instruments or estimate time-varying betas and premiums. The fact that the initial setup mentions $\mathcal F_{t-1}$ should not be mistaken for an implemented conditional pricing experiment.

## Two estimation systems and a likelihood benchmark

For the traditional GMM method define $z_t=(1,f_t)'$ and

$$
g_{1,t}(\lambda,\beta)
=z_t\otimes[r_t-\beta(\lambda+f_t)].
$$

These $2N$ moments combine mean-zero regression residuals and their orthogonality to the factor. There are $N+1$ parameters. The estimator minimizes $\bar g_1'W_1\bar g_1$, where efficient weighting uses the inverse covariance of the limiting moment process. The specification statistic is $J_1=T\bar g_1'\widehat S_1^{-1}\bar g_1$, asymptotically $\chi^2_{N-1}$ under regular correct specification.

For a fixed $\lambda$ and fixed weight matrix, the moments are affine in $\beta$ and the criterion is quadratic. Let $v=\operatorname{vec}(T^{-1}\sum r_tz_t')$ in the same stacking order as $z\otimes r$, and let $a(\lambda)=T^{-1}\sum z_t(\lambda+f_t)$. Then $\bar g_1=v-[a(\lambda)\otimes I_N]\beta$. Solve the weighted least-squares normal equations for $\beta$ and perform a scalar search over $\lambda$. This makes the larger system computationally manageable. The source's wording that the objective is “linear in beta” is best read as referring to the moments; the minimized squared criterion is quadratic.

The basic SDF method uses only

$$
g_{2,t}(\lambda)=r_t(1-\lambda f_t).
$$

There are $N$ moments and one parameter. With $\bar r=T^{-1}\sum r_t$ and $b_T=T^{-1}\sum r_tf_t$, its fixed-weight solution is

$$
\widehat\lambda_s=(b_T'W_2b_T)^{-1}b_T'W_2\bar r.
$$

The overidentification statistic $J_2=T\bar g_2'\widehat S_2^{-1}\bar g_2$ also has $N-1$ null degrees of freedom. A nonoptimal weighting matrix changes the limiting law to a weighted sum of chi-square variables unless an appropriate transformed test is used. Identical null degrees of freedom do not imply equal finite-sample behavior or equal power.

The reported simulations use two-stage GMM: first identity weights, then a weight estimated from first-stage moments. Third- and fourth-stage experiments were similar and omitted. Do not replace this with continuously updated or fully iterated GMM and expect the identical small-sample tables. The source does not give optimizer tolerances, search intervals, failed-fit handling, random seeds, or exact covariance centering/divisor conventions.

Under conditionally normal homoskedastic residuals, the paper also uses a likelihood-ratio benchmark. With $X=[\mathbf1_T,f]$, return matrix $Y$, and

$$
A=(X'X)^{-1}(X'Y)(Y'Y)^{-1}(Y'X),
$$

let $\xi_1\ge\xi_2$ be the two eigenvalues and $a_{ij}$ entries of $A$. Then

$$
\widehat\lambda_{ML}=\frac{a_{12}}{\xi_1-a_{11}},
\qquad
LRT=-\left(T-\frac{N+3}{2}\right)\log(1-\xi_2).
$$

The Bartlett-corrected LRT is compared with $\chi^2_{N-1}$. Singular sample matrices and near-zero denominators require numerical care. The normal experiment intentionally favors this distributionally correct likelihood benchmark; its performance cannot be presumed under arbitrary return distributions.

## Factors that price correctly without being the intended economic factor

Let $n_t$ be independent measurement noise, mean zero, variance $\sigma_n^2$, uncorrelated with factor and residuals. Define a standardized noisy factor

$$
g_t=\frac{f_t+n_t}{\sqrt{1+\sigma_n^2}},
\qquad \lambda_g=\lambda\sqrt{1+\sigma_n^2}.
$$

Then $E[r_tg_t]=\beta/\sqrt{1+\sigma_n^2}$ and $E[r_t(1-\lambda_gg_t)]=0$. The same expected returns are explained using smaller exposures and a larger premium. A nonrejection cannot identify how much of this factor is economic signal versus measurement noise. As noise increases without bound, the limiting useless-factor case is nonregular: the required premium diverges, so one should not interpret it as a finite well-identified pricing model.

A more striking construction uses only idiosyncratic residuals. With $H=\beta'\Sigma^{-1}\beta$, define

$$
h_t=\frac{\beta'\Sigma^{-1}\varepsilon_t}{\sqrt H},
\qquad \lambda_h=\lambda\sqrt H.
$$

This factor has unit variance and is uncorrelated with the true systematic factor. Yet $E[r_th_t]=\beta/\sqrt H$, so it also satisfies the pricing equation. It is constructed using the population residuals and coefficients; it is not an independently observed macroeconomic candidate or a feasible causal discovery procedure.

The authors acknowledge that traditional beta-pricing tests also cannot reject these alternatives merely because their economic interpretation is unattractive: they satisfy the same exact linear pricing relation with transformed loadings and premium. The proposed advantage of traditional practice is to inspect whether the factor explains time-series return variation before declaring it systematic. High explanatory power is additional diagnostic evidence, not a theorem establishing unique economic identification.

The distinction between size and power is crucial here. Noisy and residual-based factors in this section are economically “wrong” relative to the generating story but statistically correctly specified for the pricing restrictions. Their rejection probabilities are size experiments, not power against false pricing restrictions. Calling every nonrejection of them a statistical test failure would misstate the null.

## Efficiency proposition and proof logic

The appendix compares efficient GMM variances in the standardized-factor setup. Let $d=(1,-\lambda)'$, and write

$$
U=(d'\otimes I_N)S_1(d\otimes I_N).
$$

Under the contemporaneous covariance conditions used in the proof, $U=E[\varepsilon_t\varepsilon_t'(1-\lambda f_t)^2]$. A partitioned-matrix inverse shows that the traditional estimator's asymptotic variance is $(\beta'U^{-1}\beta)^{-1}$. Decompose the SDF pricing moment as

$$
r_t(1-\lambda f_t)
=\varepsilon_t(1-\lambda f_t)
+\beta(\lambda+f_t)(1-\lambda f_t).
$$

Conditional mean-zero residuals eliminate the relevant cross terms. Therefore its covariance is

$$
S_2=U+c\beta\beta',
\qquad
c=E[(\lambda+f_t)^2(1-\lambda f_t)^2].
$$

Applying the Sherman–Morrison identity gives

$$
\operatorname{Avar}(\widehat\lambda_s)
=(\beta'U^{-1}\beta)^{-1}+c
>\operatorname{Avar}(\widehat\lambda_b),
$$

provided $c>0$. A continuous factor distribution rules out concentrating all mass at the roots $-\lambda$ and $1/\lambda$. For normal homoskedastic residuals, the traditional variance is $(1+\lambda^2)/H$, the same as the likelihood estimator. If the factor is also standard normal, $c=1+\lambda^4$. All these are variances of $\sqrt T$ limits; divide by $T$ for approximate finite-sample variances.

The added term has a transparent source: SDF moments contain a common-factor component that the regression moments remove. However, removing it exploits the model's standardized population factor moments. It is not free information in an application where those moments must be estimated. This is the precise link to the later qualification stated at the beginning of the note.

The appendix defines $S_1$ and $S_2$ as contemporaneous second moments even though the earlier general GMM discussion allows serial dependence. The clean decomposition above is directly justified for the independent-draw simulations and cases where moment autocovariances vanish. With arbitrary serial dependence, use long-run covariance matrices and verify the corresponding cross-lag orthogonality conditions; do not carry the printed scalar $c$ formula over automatically.

Proposition 2 asks whether adding all SDF moments to the traditional system increases precision. Of the combined $3N$ moments, only $2N+1$ are nonredundant in the one-factor setup. For an asset with nonzero beta, one SDF moment plus the $2N$ regression moments algebraically generates the other SDF moments. The appendix's block inverse shows that the augmented information matrix equals the original traditional information matrix. Thus those extra moments provide no asymptotic gain in this experiment. This is a statement about particular moment contents, not a general rule that more valid moments never help.

## One-factor calibration and Monte Carlo reconstruction

The calibration uses monthly January 1926–December 1997 returns for ten size-ranked NYSE portfolios and the NYSE value-weighted market excess return. Standardize the latter using its historical mean and standard deviation, regress each portfolio's excess return on that factor, and use the residual covariance as $\Sigma$. Choose $\lambda$ to minimize $\|\bar r-\beta\lambda\|^2$. The resulting premium is 0.1373, close to the historical market Sharpe ratio 0.1248.

Table I supplies these rounded inputs, ordered smallest to largest:

| Portfolio | Mean excess return, % monthly | Standardized-factor beta |
|---|---:|---:|
| 1 | 1.129 | 0.082 |
| 2 | 1.070 | 0.078 |
| 3 | 0.993 | 0.072 |
| 4 | 0.954 | 0.069 |
| 5 | 0.923 | 0.067 |
| 6 | 0.911 | 0.066 |
| 7 | 0.875 | 0.064 |
| 8 | 0.833 | 0.061 |
| 9 | 0.810 | 0.059 |
| 10 | 0.709 | 0.052 |

The beta numbers use decimal returns; the displayed means use percent. Dividing means by 100 makes them approximately $\beta\lambda$, with discrepancies due to rounding. Preserve the pricing restriction exactly in simulation by choosing full-precision calibrated betas and setting $\alpha=\beta\lambda$. Do not treat rounded table means and rounded betas as jointly exact inputs.

For each $T\in\{120,240,360,480,600,720\}$, draw independent $f_t\sim N(0,1)$ and $\varepsilon_t\sim N(0,\Sigma)$, set $r_t=\beta(\lambda+f_t)+\varepsilon_t$, and estimate the three methods. Repeat 10,000 times. Population standardization is held fixed across draws; restandardizing each generated factor sample would change the experiment. There is no trading rebalancing schedule, cost assumption, or training/test portfolio strategy because the outcome is statistical estimation accuracy.

The numerical residual covariance matrix is not printed, nor are exact portfolio identifiers and all historical formation conventions. This prevents an exact table reproduction from the article alone. Rebuilding it requires the original historical series and regression specification. A bounded check of [Guofu Zhou's publication page](https://guofuzhou.github.io/zpublications.html) located the article link but no associated simulation-data or covariance supplement. The unreported matrix should remain an explicit missing input, not be borrowed from a different paper's later calibration.

For nonnormal experiments draw $(f_t,\varepsilon_t')'$ jointly from a covariance-matched multivariate Student distribution with five or ten degrees of freedom and covariance $\operatorname{diag}(1,\Sigma)$. One construction multiplies a block-independent Gaussian vector by a common $\sqrt{(\nu-2)/V}$, with $V\sim\chi_\nu^2$. The common scale makes residual variance depend on the factor:

$$
\operatorname{Var}(\varepsilon_t\mid f_t)
=\frac{\nu-2+f_t^2}{\nu-1}\Sigma.
$$

This preserves the required zero conditional mean and finite fourth moments for $\nu>4$. It creates conditional heteroskedasticity without serial GARCH dynamics. Drawing separate independent Student scales for factor and residuals would miss the intended experiment.

## Estimation results: scale and limitations

Under normality at $T=120$, Table I reports mean/standard deviation of estimated premium as 0.1374/0.0020 for ML, 0.1375/0.0045 for traditional GMM, and 0.1497/0.1049 for SDF GMM. At $T=360$ these are 0.1373/0.0011, 0.1373/0.0014, and 0.1417/0.0553. At $T=720$ ML and traditional GMM both have standard deviation 0.0008, while SDF GMM has mean 0.1396 and standard deviation 0.0386.

Thus the small-sample SDF premium is upward biased and much noisier in this particular known-moments design. At 360 months its standard deviation is about 39.5 times traditional GMM's and about 50 times ML's; the headline “more than 40 times” is a broad description, not a universal ratio for every row or comparator.

With five-degree Student draws, traditional GMM at $T=120$ has mean 0.1374 and standard deviation 0.0046, while SDF has 0.1611 and 0.1162. At 720 they are 0.1373/0.0008 and 0.1432/0.0411. Ten-degree results at 120 are 0.1374/0.0045 versus 0.1511/0.1088. Heavy tails worsen the basic SDF implementation's bias and dispersion here. They do not establish dominance for arbitrary nonnormal factor processes or unknown-population standardization.

The practical error to avoid is reporting these as standard errors for an unstandardized economic premium, or treating the tiny traditional standard deviations as attainable after estimating the factor mean and variance from a short sample. A fair empirical comparison must propagate that uncertainty and use the appropriate nonlinear map between SDF and beta coefficients.

## Size tests using true, noisy, and residual factors

Table II repeats the one-factor null experiment using three candidate factors: the true $f_t$; $g_t=(f_t+n_t)/\sqrt5$ with independent $n_t\sim N(0,4)$; and the residual-based $h_t$ above. For each length, use 10,000 repetitions and the asymptotic $\chi^2_9$ thresholds at nominal 10%, 5%, and 1%.

For the true factor at 360 months, nominal-5% rejection rates are 4.8% ML, 4.9% traditional GMM, and 4.8% SDF GMM. For the noisy factor they are 4.3%, 4.5%, and 4.3%. For the residual factor they fall to 1.2%, 1.0%, and 0.6%. At 720 months the residual-factor rates remain only 2.4%, 2.0%, and 0.8%.

These are substantial underrejections relative to the nominal size, particularly for SDF with the residual factor. But the true pricing restriction is satisfied in all three experiments. The result warns that asymptotic critical values can be poorly calibrated when factor explanatory power is weak; it does not show that a correct pricing null ought to be rejected merely because the factor was constructed from residuals.

With 10,000 repetitions, a rejection probability around 5% has a binomial Monte Carlo standard error of about 0.22 percentage points. A 0.6% versus 5% difference is much larger than simulation noise. This calculated diagnostic does not account for calibration uncertainty, which the paper holds fixed.

## Omitted-factor alternatives and the main power result

The power experiment generates

$$
r_t=\alpha+\beta_1f_{1t}+\beta_2f_{2t}+\varepsilon_t,
\qquad \alpha=\beta_1\lambda_1+\beta_2\lambda_2.
$$

The two standardized factors proxy for NYSE market and long-term Treasury excess returns. Their contemporaneous covariance is 0.2, with both variances one; they are independently drawn over time, **not independent of one another**. Wording about independent generation must be interpreted consistently with equation 35 and Table III's explicit covariance. Set $\lambda_1=0.1225$ and $\lambda_2=-0.3047$.

The rounded loadings are $\beta_1=(0.084,0.079,0.073,0.070,0.068,0.067,0.064,0.061,0.059,0.052)'$ and $\beta_2=(-0.0083,-0.0063,-0.0035,-0.0027,-0.0031,-0.0024,-0.0017,-0.0001,0.0006,0.0001)'$. Displayed monthly percentage means are $(1.280,1.163,1.001,0.940,0.926,0.891,0.836,0.748,0.703,0.628)'$. Again the residual covariance comes from the historical two-factor regression and is not printed. Rounded coefficients do not exactly reproduce all displayed means.

The first factor has mean time-series explanatory power of 84.73%; the second only 2.51%. Fit a one-factor model using only the first factor or only the second. Because factors correlate, the population single-factor regression loading is not simply the corresponding structural loading: for example the first-factor projection loading is $\beta_1+0.2\beta_2$. The supplied expected-return vector is not proportional to either relevant one-factor loading vector, so both fitted pricing models are false.

When retaining only the strong first factor, all methods have similarly low power. At $T=360$ and nominal 5%, rejection rates are 12.3% ML, 12.2% traditional GMM, and 12.0% SDF. At 720 they are 22.2%, 22.2%, and 21.3%. Omission of the weak factor is hard to detect for every method in this calibration.

When retaining only the weak second factor, the contrast is large:

| Months | ML rejection, 5% test | Traditional GMM | Basic SDF GMM |
|---|---:|---:|---:|
| 120 | 5.2% | 5.0% | 1.7% |
| 240 | 18.5% | 18.2% | 2.3% |
| 360 | 33.8% | 34.1% | 3.7% |
| 480 | 48.1% | 48.7% | 6.2% |
| 600 | 60.8% | 61.3% | 11.0% |
| 720 | 71.7% | 71.0% | 17.6% |

At 360 months the SDF test rejects the seriously misspecified model less often than its nominal 5% level. This is an operational warning: weak covariance exposures and estimated moment weights can make a bad model look statistically comfortable.

The authors explain the mechanism through the weight matrix. Under misspecification, pricing errors make the estimated covariance of SDF moments large. Its inverse downweights those directions, potentially producing a small quadratic test statistic in finite samples. Large-sample consistency does not guarantee useful power at 120–720 monthly observations. They also report, without tables, that an identity-weight nonstandard GMM test did not remedy the issue; its null distribution still depends on estimated moment covariance.

These are rejection probabilities using nominal asymptotic thresholds, not uniformly size-adjusted power curves. A full comparison should distinguish power losses due to underrejection under a relevant null from sensitivity under the alternative. The authors explicitly caution that simulation results cannot be generalized automatically to other scenarios.

## What a replication and an application should retain

A faithful replication needs separate one-factor and two-factor residual covariance calibrations, exact historical return definitions, the population-standardized simulated factors, two-stage weighting, the same six sample lengths, and 10,000 independent repetitions. It should record estimator failures and unstable denominators instead of deleting them silently. The paper gives enough algebra to implement the estimators and experimental logic, but not enough numerical input to reproduce every printed decimal without rebuilding the original calibration.

For a modern application, inspect factor–return covariances, exposure precision, return explanatory power, and pricing errors alongside the specification-test p-value. A p-value is not a model-selection score measuring economic explanatory power. The residual-factor construction shows why satisfying Euler equations on a finite collection of assets does not uniquely identify the underlying economic risk. The omitted-factor simulation shows why nonrejection is particularly weak evidence when exposures are small.

At the same time, do not promote the paper's information-asymmetric precision comparison into a universal indictment of SDF methods. The later Jagannathan–Wang analysis identifies the role of nuisance-moment estimation and equivalent parameterization. The durable result is a demand for careful estimator design and identification diagnostics: the elegance of a compact pricing equation does not remove the need to understand which information its moments use, what alternatives its tests can detect, and what economic interpretation the data can actually support.

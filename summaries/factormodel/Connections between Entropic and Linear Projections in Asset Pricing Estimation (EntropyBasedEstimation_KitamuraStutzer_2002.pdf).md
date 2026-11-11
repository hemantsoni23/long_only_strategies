# Connections between Entropic and Linear Projections in Asset Pricing Estimation

**Yuichi Kitamura and Michael Stutzer (2002).** *Journal of Econometrics* 107, pp. 159–174. PII S0304-4076(01)00118-X.

**Source:** [EntropyBasedEstimation_KitamuraStutzer_2002.pdf](../../Finance/EncyclopediaQuantFinance/EntropyBasedEstimation_KitamuraStutzer_2002.pdf). All 16 pages were read; the principal equations, simulation tables, and information-bound figure were checked against rendered pages. Printed pages are cited below. The 1997 estimator paper is a distinct theoretical predecessor.

## Why this matters

GMM estimation and Hansen–Jagannathan bounds are usually introduced through quadratic loss and linear projection. Entropy methods appear to introduce a different statistical philosophy. This paper shows how a large-deviations criterion connects them: when the relevant moment process is Gaussian, its rate function is quadratic and reproduces familiar GMM and variance-bound objects; when it is not Gaussian, higher cumulants can affect the criterion.

The practical question is not whether entropy is intrinsically preferable. It is whether a quadratic approximation loses material information in the model and data being analyzed. The paper provides a common language for estimation and stochastic-discount-factor diagnostics, develops the connection for stationary dependent processes, and illustrates finite-sample differences with a variance-estimation experiment and a mutual-fund pricing example.

Two distinctions govern any reimplementation. First, the distribution of the moment vector is what matters: Gaussian raw data do not make nonlinear moments Gaussian automatically. Second, population equivalence under a Gaussian model is not exact equality between every pair of feasible finite-sample estimators. An empirical exponential moment-generating function contains features that a fitted quadratic criterion does not.

## Rate functions and probability interpretation

Let $f(x_t,\beta)\in\mathbb R^r$ be a moment vector, $\beta$ the structural parameter, and $\bar f_T(\beta)=T^{-1}\sum_t f(x_t,\beta)$. Expectations under the stationary objective distribution are denoted $E$. Equations (1)–(2) define the normalized log moment-generating function of partial sums:

$$
\phi_T(\gamma;\beta)=\frac1T\log E\left[\exp\left(\gamma'\sum_{t=1}^T f(x_t,\beta)\right)\right],\qquad
\phi(\gamma;\beta)=\lim_{T\to\infty}\phi_T(\gamma;\beta).
$$

Its convex conjugate is the rate function

$$
I(c;\beta)=\sup_\gamma\{\gamma'c-\phi(\gamma;\beta)\}.
$$

Under the large-deviations regularity conditions summarized in Proposition 2.1, for closed sets $C$ and open sets $O$,

$$
\limsup_T\frac1T\log\Pr(\bar f_T\in C)\leq-\inf_{c\in C}I(c;\beta),
$$

$$
\liminf_T\frac1T\log\Pr(\bar f_T\in O)\geq-\inf_{c\in O}I(c;\beta).
$$

Thus a mean far from its population value is exponentially unlikely, with the rate describing its asymptotic rarity. The rate is nonnegative and zero at the population mean under the conditions used. It is not a finite-sample tail probability, and simply substituting $e^{-TI}$ does not supply an exact p-value or a confidence interval.

The source requires existence of the limiting log moment-generating function, differentiability on the interior of its effective domain, and a boundary steepness condition. Its footnote discusses sufficient mixing conditions. These assumptions deserve scrutiny for heavy-tailed financial moments: existence of means and variances alone does not establish the needed exponential integrability.

For IID observations, independence factorizes the partial-sum expectation, so

$$
\phi(\gamma;\beta)=\log E[e^{\gamma'f(x,\beta)}],\qquad
I(c;\beta)=\sup_\gamma\{\gamma'c-\log E[e^{\gamma'f}]\}.
$$

For Gaussian $f$ with mean $\mu_f$ and nonsingular covariance $\Sigma_f$, this becomes

$$
I(c;\beta)=\frac12(c-\mu_f)'\Sigma_f^{-1}(c-\mu_f).
$$

The maximizing multiplier for general $c$ is $\Sigma_f^{-1}(c-\mu_f)$. Example 2.1 prints the special-case expression $-\Sigma_f^{-1}\mu_f$ while discussing general $c$; that multiplier is correct at $c=0$, the case used subsequently for estimation. This note keeps the general and zero-target cases separate.

## Entropic projection and tilted probabilities

The IID first-order condition for the multiplier is a mean condition under an exponentially tilted distribution. If $\mu$ denotes the objective probability measure, define

$$
\frac{dP^*}{d\mu}=\frac{e^{\gamma^{*'}f(x,\beta)}}{E[e^{\gamma^{*'}f(x,\beta)}]}.
$$

Then $E_{P^*}[f]=c$. Kullback’s lemma, Proposition 2.2, states that this distribution minimizes

$$
D(P\Vert\mu)=\int\log\left(\frac{dP}{d\mu}\right)dP
$$

over distributions satisfying that mean restriction, with minimum equal to $I(c;\beta)$. The direction of the divergence matters: the logarithm is integrated under the tilted measure. This is an information projection of the original distribution onto the moment-constrained set.

Proposition 2.3 adds a frequentist interpretation. Under the stated support condition, conditioning a long IID sample on its mean lying in an increasingly small neighborhood of $c$ produces limiting conditional probabilities given by the same Gibbs tilt. The change of measure is therefore connected to conditioning on a rare mean event, not only to an abstract optimization penalty. The result has both a long-sample and shrinking-neighborhood limit; it is not a claim that a finite sample has exactly the tilted conditional distribution.

## Stochastic discount factors and the variance bound

Let $R$ be a vector of real gross one-period asset returns and let $m$ be a stochastic discount factor. The pricing equations are

$$
E[Rm]=\mathbf1.
$$

The source writes $d=E[m]=E[1/r]>0$ using the conditionally riskless gross return $r$ and the relevant conditional pricing implication. To interpret $m/d$ as a probability density, the candidate SDF must be nonnegative and integrable; arbitrary signed solutions of the linear pricing equations do not define probability measures.

An affine benchmark SDF is

$$
m_a=(R-E[R])'\theta_a+d,\qquad
\theta_a=-\operatorname{Cov}(R)^{-1}(dE[R]-\mathbf1).
$$

Its variance gives the familiar lower bound, equation (17):

$$
\operatorname{Var}(m_a)
=(dE[R]-\mathbf1)'\operatorname{Cov}(R)^{-1}(dE[R]-\mathbf1)
\leq\operatorname{Var}(m).
$$

This bound follows from a linear projection. A candidate with insufficient variance cannot price the chosen assets. The affine benchmark itself need not be a positive SDF in every state, which is one reason the probability-projection viewpoint is informative.

Normalize a positive SDF to obtain $dP/d\mu=m/d$. Pricing then becomes

$$
E_P[R-\mathbf1/d]=0.
$$

The target vector is the return vector minus $1/d$, not necessarily the observed period-by-period risk-free return. The paper calls it an approximate population risk-premium vector. Substituting a time-varying realized risk-free series changes the moment definition and must not be done silently.

## Two diagnostics with different meanings

Diagnostic Criterion 3.1 uses the objective return distribution to calculate the rate of the sample risk-premium vector approaching zero. In the IID case,

$$
I(0;d)=\max_\gamma-\log E[e^{\gamma'(R-\mathbf1/d)}].
$$

It is the minimum relative entropy among probability changes satisfying the pricing restriction. Consequently, a valid positive candidate must have sufficient entropy:

$$
I(0;d)\leq E\left[\frac{m}{E[m]}\log\frac{m}{E[m]}\right].
$$

For IID Gaussian returns, equation (22) gives

$$
I(0;d)=\frac12E[R-\mathbf1/d]'\operatorname{Cov}(R)^{-1}E[R-\mathbf1/d]
=\frac{\operatorname{Var}(m_a)}{2d^2}.
$$

This is the exact proportionality connecting the information bound to the variance bound in the Gaussian case. Outside it, the exponential criterion can depend on higher moments and tail shape. Adding additional asset pricing restrictions cannot reduce the minimum information needed to satisfy them; a small asset set therefore gives a weaker diagnostic.

Diagnostic Criterion 3.2 instead starts under the candidate pricing measure $\nu$, defined by $d\nu/d\mu=m(\beta)/E[m(\beta)]$. It calculates

$$
I_\nu(0;d)=\max_\gamma-\log E_\nu[e^{\gamma'(R-\mathbf1/d)}].
$$

When the candidate has already removed the pricing error, the target mean is zero and the rate is zero, with maximizing multiplier zero under the regularity conditions. Otherwise the positive rate measures the remaining distortion needed under that candidate measure. This is a pricing-error diagnostic, distinct from comparing the candidate’s information content to the minimum information bound under the objective measure.

The Gaussian quadratic representation of this second diagnostic uses expectations and covariances under $\nu$. One must check Gaussianity under that measure; Gaussianity under the original measure need not survive an arbitrary candidate SDF tilt. The source’s discussion motivates comparison to the later Hansen–Jagannathan specification-error measure without claiming the two numerical distances are generally identical.

## Estimation and dependent observations

For an identified model $E[f(x,\beta^*)]=0$, Estimation Criterion 3.1 selects $\arg\min_\beta I(0;\beta)$. For IID data this is exponential tilting:

$$
\arg\min_\beta\max_\gamma-\log E[e^{\gamma'f(x,\beta)}].
$$

If the moment vector is Gaussian, the population criterion is the optimally weighted quadratic moment criterion. For stationary Gaussian moment processes, define the lag covariance matrices $\Gamma_j$ and the finite positive definite long-run covariance $S=\sum_{j=-\infty}^{\infty}\Gamma_j$. The partial sum is Gaussian, with covariance

$$
T\Gamma_0+\sum_{j=1}^{T-1}(T-j)(\Gamma_j+\Gamma_{-j}).
$$

Dividing its log moment-generating function by $T$ and taking the limit gives

$$
\phi(\gamma;\beta)=\gamma'E[f]+\tfrac12\gamma'S\gamma,\qquad
I(0;\beta)=\tfrac12E[f]'S^{-1}E[f].
$$

This is Proposition 4.1. Serial dependence changes the correct quadratic weight through all autocovariances, not only contemporaneous variation.

For a stable linear state-space system, equations (34)–(36) show how non-Gaussian innovations enter the rate criterion. With state transition $x_{t+1}=Fx_t+v_t$ and observed moment process $B'z_t+H'x_t+w_t$, the innovations and exogenous process are IID and mutually independent as specified. Under existence and boundary conditions, the limiting cumulant function is the sum of the log moment-generating functions of $H'(I-F)^{-1}v$, $B'z$, and $w$. Higher cumulants survive when these components are non-Gaussian. Closed-form rate functions are generally unavailable.

For a feasible distribution-free analogue, use the smoothed moments

$$
\tilde f_t(\beta)=\frac1L\sum_{k=-K}^{K}f(x_{t-k},\beta),\qquad L=2K+1.
$$

Equation (40) estimates the parameter by profiling

$$
\hat I_K(0;\beta)=\max_\gamma-\frac1L\log\left[\frac1T\sum_t e^{\gamma'\tilde f_t(\beta)}\right].
$$

The factor $1/L$ does not affect the parameter argmin at a fixed bandwidth, but it does affect reported rate values and test statistics. Proposition 4.2 derives this as an analogue of the large-deviations criterion and connects it to the 1997 smoothed estimator. Under that predecessor’s regularity conditions, with $K\to\infty$ and $K^2/T\to0$, the estimator is first-order equivalent to efficient GMM. This does not mean a fixed finite bandwidth exactly reproduces the population rate function for every dependent process.

## Variance-estimation experiment

Section 5 first isolates nonnormality in an IID setting. For each replication, draw ten independent samples from a Student $t$ distribution, each of length $T$. The grid is $T\in\{50,100,200\}$ and degrees of freedom $\nu\in\{5,10,15,50\}$. For each cell repeat the experiment 1,000 times.

For sample $i$, compute its sample mean $\bar x_i$ and squared centered observations $z_{it}=(x_{it}-\bar x_i)^2$. The ten moments are $f_{it}(\beta)=z_{it}-\beta$, so a single variance parameter is estimated from ten sample variances using denominator $T$. GMM minimizes the quadratic moment criterion with the sample inverse covariance of these moments. Exponential tilting uses the same moments in the empirical log moment-generating function.

The printed equation (42) has visibly misplaced summation/exponential notation. The reproducible expression implied by equations (27), (40), and the preceding ten-moment definition is

$$
\hat\beta_{ET}=\arg\min_\beta\max_{\gamma\in\mathbb R^{10}}
-\log\left\{\frac1T\sum_{t=1}^{T}
\exp\left[\sum_{i=1}^{10}\gamma_i(z_{it}-\beta)\right]\right\}.
$$

This is a reconstruction of the intended algorithm, not a literal transcription of the damaged expression. The $t$-sum belongs outside the exponential, and the multiplier applies separately to each moment. Summing all moments into a single scalar before tilting would change the estimation problem.

Tables 1–2 report GMM’s absolute MSE and bias, plus how much worse each is than ET in percentage terms:

| Degrees of freedom | T | GMM MSE | MSE worse than ET | GMM bias | Absolute bias worse than ET |
|---:|---:|---:|---:|---:|---:|
| 5 | 50 | 0.048 | 28% | −0.197 | 14% |
| 5 | 100 | 0.020 | 37% | −0.123 | 23% |
| 5 | 200 | 0.009 | 45% | −0.080 | 29% |
| 10 | 50 | 0.022 | 20% | −0.118 | 11% |
| 10 | 100 | 0.007 | 27% | −0.062 | 20% |
| 10 | 200 | 0.003 | 26% | −0.033 | 30% |
| 15 | 50 | 0.016 | 14% | −0.095 | 7% |
| 15 | 100 | 0.005 | 21% | −0.050 | 19% |
| 15 | 200 | 0.002 | 20% | −0.027 | 27% |
| 50 | 50 | 0.012 | 8% | −0.077 | 4% |
| 50 | 100 | 0.004 | 16% | −0.042 | 12% |
| 50 | 200 | 0.002 | 12% | −0.019 | 21% |

Both estimators are negatively biased in the reported experiment, but ET has smaller absolute bias and MSE in every cell. If GMM is 45% worse by the table’s relative-MSE convention, ET’s MSE is GMM’s divided by 1.45, about 31% lower than GMM, not 45% lower. At $\nu=5,T=200$, the rounded entries imply an ET MSE near 0.00621; that is derived from the published ratio, not a separately reported estimate.

The MSE advantage generally rises with heavier tails at fixed sample size. The bias-percentage cells do not all obey a strict monotonic ordering: at $T=200$, the 10-degree case is 30% while the 5-degree case is 29%. Rounded simulation evidence should not be converted into a universal monotonic theorem.

The paper does not state the random seed, generator, exact scale normalization of the Student draws, optimizer tolerances, failure handling, or Monte Carlo standard errors. In particular, standard $t_\nu$ draws have variance $\nu/(\nu-2)$ whereas variance-normalized draws do not; matching the absolute reported MSE and bias requires resolving that implementation detail. Squared Student draws also lack a two-sided neighborhood of finite exponential moments. The finite-sample objective is still computable, but this experiment is not itself verification of every population large-deviations assumption.

## Market-data diagnostic

The second exercise asks whether logarithmic, time- and state-separable utility can be consistent with the selected returns. Such a model motivates the reciprocal of the market portfolio’s gross return as an SDF. The paper uses the S&P 500 return as the market proxy, so the candidate is $m_t=1/R_{M,t}$.

Monthly observations run from January 1976 through December 1994, an inclusive span of 228 months before any smoothing losses. The single test asset is CRSP domestic equity fund No. 8161. A one-asset restriction is deliberately weak: adding assets cannot reduce the information bound. Using another domestic equity fund also gives the market-based candidate a favorable, closely related comparison.

For a grid of $1/d$ values, the IID bound is estimated by replacing the expectation with the time average and optimizing over the scalar multiplier. The dependent versions smooth the excess-return sequence using $K=3$ and $K=6$, giving 7- and 13-month windows, and apply the $1/L$ normalization in equation (45). The source redefines $T$ as the number of smoothed observations but does not spell out every boundary convention.

The candidate information value is the empirical average of $(m/\bar m)\log(m/\bar m)$, plotted at $1/d=1/\bar m$. Figure 1 on p. 173 shows the three estimated bound curves close together and above that candidate point at its corresponding mean. Visually the grid spans monthly gross rates approximately 1.002–1.039; exact plotted coordinates are not tabulated. The figure therefore supports a violation in this sample without supplying an exact numerical test statistic to quote.

The paper interprets this as evidence against reciprocal S&P 500 returns being a valid SDF even for domestic equity funds. It does not report a p-value, sampling confidence band, fund-selection adjustment, or holdout validation. Fund No. 8161 is described as having performed strongly over the period; the exercise does not establish an ex ante implementable manager-selection rule. The similarity of bandwidth results is specific to these returns, not a general argument that dependence corrections are unnecessary.

## Reproduction priorities and limits

An implementation should keep the objective measure, candidate pricing measure, and fitted entropy-projection measure distinct. It should normalize SDFs correctly, declare whether returns are real or nominal, use gross returns, and preserve the source’s $1/d$ target convention. The empirical section does not fully document inflation adjustment, return-source fields, missing observations, fund fees, or selection procedures, so those choices must be recorded as additional replication inputs.

Numerically, profile the convex multiplier problem using log-sum-exp, verify the weighted moment condition, and check whether zero is feasible in the sample convex hull. For dependent versions, log the bandwidth and effective sample size. Reproduce the simulation tables with several seeds and report optimization failures before treating differences as statistical performance. Such checks implement the method; they are not experimental results provided by the authors.

The paper’s core result is a unification: entropy-based methods and quadratic projection methods can be traced to the same probability-decay criterion, with Gaussian moments delivering the quadratic form. Its evidence suggests that nonlinear distributional information can matter in small samples, while its market example illustrates a concrete SDF rejection mechanism. The limits are equally explicit: the numerical advantage is design-specific, the empirical bound is an illustration without formal uncertainty bands, and the population theory requires more than finite second moments.

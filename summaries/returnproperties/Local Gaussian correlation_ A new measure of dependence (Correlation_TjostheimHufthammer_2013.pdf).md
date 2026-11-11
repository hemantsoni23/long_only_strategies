# Local Gaussian correlation: A new measure of dependence

**Dag Tjøstheim and Karl Ove Hufthammer (2013).** *Journal of Econometrics* 172, 33–48, DOI 10.1016/j.jeconom.2012.08.001. Source: [original PDF](../../Finance/Correlation_TjostheimHufthammer_2013.pdf), sixteen pages including proofs, bandwidth illustrations, dependence maps, and the three-stock application. References below use printed pages. The authors introduce a local dependence estimator, not a portfolio strategy or a time-varying conditional covariance model.

## Why this matters

A single correlation coefficient can conceal opposite dependence in different parts of a joint distribution. For example, a parabola can have zero global correlation while being almost deterministic. Financial returns can also exhibit different dependence when both assets fall and when both rise. Simply computing ordinary correlation after selecting a downside subsample changes the estimand and can create apparent variation even for a globally Gaussian population.

The paper proposes fitting a bivariate Gaussian density locally around each evaluation point and using the fitted Gaussian's correlation parameter as a dependence measure. For a globally Gaussian distribution, the population local Gaussian is the same everywhere and its correlation equals the global Gaussian correlation. The procedure is symmetric in the two variables and retains a bounded signed correlation scale. It can therefore reveal nonlinear dependence patterns without forcing one variable into the role of a regression response.

The price is estimation difficulty. Five local parameters must be learned at each point, their information degenerates as neighborhoods shrink, and tail regions have little data. Local Gaussian correlation is consequently a function with an explicit localization scale, uncertainty, and regularity assumptions. It should not be read as an exactly observed state variable or as a free replacement for every ordinary covariance in portfolio algebra.

The most useful empirical finding is qualitative but concrete: after marginal GARCH filtering, the Boeing–Alcoa and Boeing–Caterpillar pairs exhibit greater local dependence in joint negative returns, while Caterpillar–Alcoa exhibits the opposite slope along the diagonal. A common positive global correlation does not describe these differences.

## The estimand: a Gaussian fit around a point

Let $X_i=(X_{1i},X_{2i})^{\mathsf T}$ have joint density $f$. Fix an evaluation point $x=(x_1,x_2)$. The approximating Gaussian density is

$$
\psi(v;\mu,\Sigma)=
\frac{\exp[-\tfrac12(v-\mu)^{\mathsf T}\Sigma^{-1}(v-\mu)]}
{2\pi|\Sigma|^{1/2}},
$$

with local parameters $\theta_b(x)=(\mu_1,\mu_2,\sigma_1^2,\sigma_2^2,\rho)$. Its covariance matrix is

$$
\Sigma=\begin{pmatrix}
\sigma_1^2&\rho\sigma_1\sigma_2\\
\rho\sigma_1\sigma_2&\sigma_2^2
\end{pmatrix}.
$$

Require $\sigma_i>0$ and $|\rho|<1$ for a nondegenerate density. Boundary values ±1 describe limiting functional dependence, not an ordinary nonsingular Gaussian density one should pass to the numerical optimizer.

The local mean is not constrained to equal the evaluation point. If the true density is Gaussian with mean zero, a local fit around a point far in its tail should still recover that same mean zero and covariance. Centering every local Gaussian at $x$ would change the method and destroy this calibration property.

For product kernel $K_b(v-x)=(b_1b_2)^{-1}K((v_1-x_1)/b_1)K((v_2-x_2)/b_2)$, define the population penalty

$$
q_b(\theta;x)=\int K_b(v-x)
\left[\psi(v;\theta)-f(v)\log\psi(v;\theta)\right]dv.
$$

Its unique minimizer, when it exists, is $\theta_b(x)$. The finite-bandwidth dependence measure is the correlation component $\rho_b(x)$. The limiting quantity $\rho(x)$ is defined through $\theta_b(x)\to\theta(x)$ as the bandwidth shrinks under the paper's existence and uniqueness assumptions. Reporting a fitted map should therefore record its bandwidth; estimates at different bandwidths deliberately describe dependence at different degrees of locality.

This is not conditional correlation given $X$ lies in a region. Nor is it a conditional correlation given past time-series information. In a stationary return-pair application it describes the shape of a bivariate marginal distribution at different return values. Time enters only through the observations or through the construction of lagged pairs.

## Modified local likelihood and why the correction is indispensable

The empirical criterion is Eq. (6):

$$
L_n(\theta;x)=
\frac1n\sum_{i=1}^nK_b(X_i-x)\log\psi(X_i;\theta)
-\int K_b(v-x)\psi(v;\theta)dv.
$$

Maximize it separately at each evaluation point. The integral term is not constant in the Gaussian parameters. Removing it leaves a weighted Gaussian fit to a locally selected sample, which is the wrong density-approximation problem. In particular, ordinary weighted sample means and covariances generally do not solve the proposed estimator.

Writing $u(v;\theta)=\partial\log\psi(v;\theta)/\partial\theta$, the estimating equation is

$$
\frac1n\sum_i K_b(X_i-x)u(X_i;\theta)
-\int K_b(v-x)u(v;\theta)\psi(v;\theta)dv=0.
$$

At the population optimum the same equation replaces the empirical distribution with $f(v)dv$. Thus a correctly specified Gaussian density solves the equation at every point, whatever the finite neighborhood, because $f-\psi$ vanishes. In a non-Gaussian density the equation balances local score-weighted approximation errors.

A particularly convenient implementation uses a normalized Gaussian kernel with covariance $B=\operatorname{diag}(b_1^2,b_2^2)$. Then the penalty integral is a Gaussian convolution:

$$
\int\phi_B(v-x)\phi_\Sigma(v-\mu)dv
=\phi_{B+\Sigma}(x-\mu).
$$

Consequently the exact numerical objective is a weighted sum of Gaussian log densities minus a single Gaussian density evaluated at $x$. This convolution identity is an implementation derivation consistent with the paper's statement that Gaussian-kernel integrals are analytic. It avoids numerical integration and makes finite-difference or automatic-differentiation checks straightforward.

Parameterize standard deviations by exponentials and correlation by a hyperbolic tangent, or parameterize $\Sigma$ through a Cholesky factor. Optimize all five parameters jointly. Record convergence and compare multiple starts, especially in sparse regions. A previous nearby grid point can supply a warm start, but agreement across starts is evidence about the numerical fit rather than a proof of population uniqueness. These practical choices make the stated criterion implementable; the source does not specify its original optimizer, tolerance, or restart rules.

## Existence and uniqueness: what the assumptions do

Matching the density at one point is insufficient: infinitely many Gaussian surfaces can pass through the same positive density value. The local neighborhood criterion, not pointwise interpolation alone, identifies the intended approximation. For a globally Gaussian density, identification is straightforward. The paper also constructs piecewise affine transformations of independent Gaussian variables, whose interiors have locally Gaussian densities; with a sufficiently small compact-support kernel, the local parameters are exact there.

General existence and uniqueness are more delicate. The source assumes a unique minimizer for all sufficiently small bandwidths and a well-behaved limit. These conditions should not be paraphrased as a universal theorem that every smooth density possesses a uniquely identified five-parameter local Gaussian at every point. Uniform densities and support boundaries illustrate degeneracy, and the authors explicitly discuss them.

The argument on p. 36 moves from convergence of the scalar density value to convergence of the five-dimensional parameter vector. Scalar density convergence alone cannot establish that implication; local identifiability over a neighborhood and control of curvature are needed. Similarly, a unique minimum does not by itself imply a strictly positive-definite Hessian. A careful use of the later asymptotic results must retain the nondegeneracy and information assumptions rather than derive them merely from uniqueness.

In finite samples, useful diagnostics are the fitted covariance's eigenvalues, the objective Hessian, sensitivity to starts, local data density, and stability under a modest bandwidth change. A correlation estimate close to ±1 in a nearly empty region may reflect numerical boundary behavior. The paper's substantive maps are accompanied by density restrictions and uncertainty calculations for this reason.

## Fixed-bandwidth inference and dependence over time

For independent observations and fixed $b$, the local estimator is an M-estimator. The paper writes its asymptotic covariance in sandwich form, with a curvature matrix

$$
J_b=\int K_b uu^{\mathsf T}\psi\,dv
-\int K_b(\nabla_\theta u)(f-\psi)\,dv.
$$

All functions are evaluated at the population local fit. The score covariance involves the variance of $K_b(X-x)u(X;\theta_b)$, with the source's $b_1b_2$ scaling convention. The second curvature term vanishes under exact local Gaussian specification but need not vanish otherwise. Using only a Gaussian information matrix would overlook misspecification.

Theorem 1 extends the framework to stationary geometrically ergodic bivariate series, assuming a unique local population fit, support on the plane, and finite score moments of order greater than two. Its proof uses an ergodic law for the gradient and Hessian, a mixing central limit theorem for the score, and a Taylor expansion of the first-order conditions. The existence statement is formulated on events with probability arbitrarily close to one rather than as an unconditional global numerical-optimization guarantee.

For an actual fixed-bandwidth dependent-data implementation, the score's long-run covariance must account for serial covariances:

$$
\Omega_b=\sum_{k=-\infty}^{\infty}
\operatorname{Cov}(s_t,s_{t-k}),
\qquad s_t=K_b(X_t-x)u(X_t;\theta_b).
$$

The corresponding estimator covariance is $J_b^{-1}\Omega_bJ_b^{-\mathsf T}/n$, in unscaled notation. The source emphasizes the zero-lag integral as a leading contribution under localization and proposes ergodic plug-in estimates. An ergodic theorem justifies time averages but does not by itself remove fixed-bandwidth serial score covariance. This qualification is important when the data are lagged pairs with overlapping observations or incompletely filtered returns.

The article offers an ordinary bootstrap for independent observations and an analytic plug-in alternative. It explicitly notes that the ordinary bootstrap is not suitable for dependent data and suggests trying a block bootstrap, without prescribing a block length. A replication should not invent a source-reported dependence correction or block rule.

## Shrinking neighborhoods and the unusual convergence rate

The difficult feature of the five-parameter fit is that leading local score information collapses toward rank one as $b\to0$. The first-order term has the form $u(x)u(x)^{\mathsf T}f(x)$. Recovering all five parameter directions requires higher-order expansion over the neighborhood, making the estimator slower than a conventional bivariate kernel-density estimate.

The paper reports scaling $\sqrt{n(b_1b_2)^3}$ for the local parameter vector. For equal bandwidths $b_1=b_2=b$, this corresponds to variance of order $(nb^6)^{-1}$, rather than the usual density-estimation order $(nb^2)^{-1}$. Substantially larger bandwidths or more observations are therefore needed to resolve local correlations. This is the central practical implication of the asymptotic theory.

Theorem 2 gives a shrinking-bandwidth result for globally Gaussian stationary series with geometric ergodicity and a Lipschitz kernel. Theorem 3 extends the claimed result to a non-Gaussian density with a nondegenerate local Gaussian approximation and score-moment conditions. General non-Gaussian inference also needs approximation-bias control: an interval centered as though $\theta_b(x)=\theta(x)$ can be misleading when the finite-bandwidth target differs appreciably from its limit.

There is a technical bandwidth ambiguity in the printed conditions. They display $\log n/(nb_1b_2)^5\to0$, while the proof rescales a uniform stochastic error of order $\sqrt{\log n/(nb_1b_2)}$ by $(b_1b_2)^{-2}$. That step instead requires $\log n/[n(b_1b_2)^5]\to0$. These are different conditions. The note does not silently replace the stated theorem with a fully repaired one. For reproducible practical work, finite-bandwidth estimation with explicitly assessed bias and uncertainty is better grounded than applying the printed general limit formula mechanically.

## Transformation and symmetry properties

Under a nonsingular affine transformation $Y=a+AX$, the corresponding local fit transforms as $\mu_Y=a+A\mu_X$ and $\Sigma_Y=A\Sigma_XA^{\mathsf T}$, provided the bandwidth geometry is transformed consistently. The proof changes variables in both terms of the local objective; the resulting multiplicative and additive constants do not affect the maximizer.

This consistency requires the bandwidth matrix to change with the data. Rotating observations while keeping an axis-aligned kernel of the same shape does not reproduce that exact finite-bandwidth transformation. Positive separate rescalings preserve correlation values at corresponding points; reversing one axis reverses the sign. General nonlinear marginal transformations require additional analysis and should not be assumed irrelevant to the five-parameter finite-bandwidth fit.

For a radially symmetric density $f(-x)=f(x)$, local correlation is radially symmetric and local means change sign. For reflection symmetry around either coordinate axis, correlation is odd across that axis, so it is zero along the axes. Exchange symmetry of the density implies symmetry when the variables are exchanged. GARCH lag pairs need not have exchange symmetry because time reversal generally changes their distribution.

Independence implies $\rho(x)=0$ everywhere under the local representation. The paper's stated necessary-and-sufficient characterization also requires that each local mean and variance depend only on its own coordinate. It does not establish that $\rho(x)\equiv0$ alone is a universal equivalence to independence; the authors state that they have not found a dependent counterexample. A single point with zero local correlation certainly does not establish independence.

For deterministic smooth functional dependence, the local Gaussian degenerates and correlation tends to +1 or −1 according to the local tangent direction. The endpoint behavior is a limiting geometric statement outside the nonsingular-density assumptions used for estimation and asymptotic normality.

## A nonlinear example that can be reconstructed

Take $X_1\sim N(0,\sigma_X^2)$ and $X_2=X_1^2+\epsilon$, where $\epsilon\sim N(0,\sigma_\epsilon^2)$ is independent. Global correlation is zero by symmetry, despite strong dependence. Along the parabola $x_2=x_1^2$, the paper's local transformation calculation gives

$$
\Sigma(x_1,x_1^2)=
\begin{pmatrix}
\sigma_X^2&2\sigma_X^2x_1\\
2\sigma_X^2x_1&4\sigma_X^2x_1^2+\sigma_\epsilon^2
\end{pmatrix},
$$

and

$$
\rho(x_1,x_1^2)=
\frac{2x_1}{\sqrt{4x_1^2+\sigma_\epsilon^2/\sigma_X^2}}.
$$

It is negative on the left branch, positive on the right, and zero at the turning point. As noise becomes small, it approaches the appropriate endpoint away from zero. This furnishes a useful implementation example, although finite-bandwidth estimates have bias and the paper distinguishes general nonunique transformation representations from special computable cases.

The article also derives copula-specific diagonal expressions in collaboration with companion work. Those formulas and their normalizations should be checked against a Gaussian benchmark before using them as numerical truth; the directly defined local-likelihood objective is the main implementation route here. This note does not need an unreported copula parameter to reconstruct the estimator.

## Tail interpretation and its limits

Ordinary Gaussian dependence has zero asymptotic upper and lower tail-dependence coefficients unless correlation is one. The authors suggest that a local correlation approaching one in a joint extreme region can describe the increased dependence often discussed during market crashes. They explicitly say that they lack general exact monotonicity conditions linking local correlation limits to tail-dependence coefficients.

Their tail argument is therefore suggestive and supported by particular copula examples, not a universal equivalence theorem. Local correlation is a function of a point or neighborhood; a tail-dependence coefficient is a limit of conditional exceedance probabilities. The rate at which the correlation changes, the accuracy of the Gaussian approximation in the tail, and marginal transformations can all matter. A finite-sample value .8 at a negative return pair is not an estimate of an asymptotic probability .8.

The univariate transformation formula illustrates why local scales can grow in heavy tails:

$$
\sigma(x)=\frac{\phi(\Phi^{-1}(F(x)))}{f(x)}.
$$

The paper defines tail heaviness relative to matched Gaussian quantiles, not simply through a finite-moment threshold. Its terminology includes some distributions, such as exponential tails, that are not normally called heavy-tailed in the regular-variation sense. This convention must be preserved when interpreting the stated local-scale divergence.

## Bandwidth selection and a concrete computational workflow

Section 7 balances parameter-estimation variance against density-approximation discrepancy. Standardize the two data coordinates to unit sample variance. For candidate equal scaled bandwidth $b$, fit local parameters at selected observation locations, estimate the variance of the correlation component, and compare the fitted density value with a separate kernel-density estimate $\widetilde f$.

Define

$$
V(b)=\frac1m\sum_{j\in\mathcal J}
\widehat{\operatorname{Var}}[\widehat\rho_b(X_j)],
$$

$$
D(b)=\frac1m\sum_{j\in\mathcal J}
[\psi(X_j;\widehat\theta_b(X_j))-\widetilde f(X_j)]^2.
$$

The set $\mathcal J$ excludes sufficiently low-density locations so extreme variance estimates do not dominate. Choose a bandwidth minimizing a weighted combination $pV(b)+(1-p)D(b)$, then transform coordinate bandwidths back to the original units. The article also illustrates an unweighted sum. It does not specify one universal value of $p$, an exact density cutoff, or a fully automated bandwidth for the stock example.

The discrepancy $D$ is a density-fit proxy, not squared bias of the correlation itself. That distinction limits claims of optimal correlation bandwidth. The heuristic orders $(nb^6)^{-1}$ and $b^4$ suggest $b$ of order $n^{-1/10}$ when balancing these terms, but the paper does not establish a complete optimal-bandwidth theorem. A practical report should show sensitivity across nearby bandwidths.

A Gaussian benchmark uses means zero, variances one, correlation .5, sample sizes 100, 200, 500, and 1,500, and bandwidths .5–2.5. Figure 4's total criterion tends to fall as the bandwidth grows, consistent with a globally Gaussian model requiring no localization. The plotted density-discrepancy component need not monotonically decrease with bandwidth; it is the combined criterion and the absence of a clear finite optimum that matter.

The contrasting GARCH benchmark uses

$$
Y_t=\sigma_t\epsilon_t,\qquad
\sigma_t^2=0.1+0.7Y_{t-1}^2+0.2\sigma_{t-1}^2,
\qquad \epsilon_t\sim N(0,1).
$$

Form adjacent pairs $(Y_t,Y_{t+1})$. The variance is finite with unconditional mean one, but higher-moment conditions are more restrictive; one should not assume all ordinary fourth-moment approximations automatically hold at these parameters. Figure 4 shows an interior bandwidth compromise moving downward as sample size grows. Initial state, burn-in, seeds, and full optimizer settings are not supplied.

## Simulated dependence maps and stock evidence

The bivariate Student example uses 5,000 observations, four degrees of freedom, and zero global correlation. Its map has positive local correlation in joint-sign quadrants and negative correlation in opposite-sign quadrants, illustrating dependence despite zero linear correlation. Figure 3 uses 2,000 GARCH observations and $b_1=b_2=1$. Most points lie within ±2; the plot is limited to ±3. Reported standard errors are roughly .03–.05 in the central square and can reach .2 near its displayed extremes. The much larger tail uncertainty is part of the finding.

The GARCH map is approximately radially and reflection symmetric but not exchange symmetric. Its positive joint-sign and negative opposite-sign regions reflect magnitude dependence in successive returns. This does not imply a profitable signed-return predictor; zero ordinary return autocorrelation and nonlinear volatility dependence can coexist.

The financial sample contains daily $100\log$ returns on Boeing, Alcoa, and Caterpillar from January 1, 1973 to December 31, 2007. Zero returns are removed, and each marginal is filtered by a GARCH(1,1) with conditional Student innovations to reduce kurtosis and time dependence. The paper does not identify the price vendor, exact split/dividend adjustment, final sample size, or whether zero-return removal is performed jointly or pairwise. The alignment rule matters for a paired estimator and should be recovered before exact replication.

Figure 5 plots $\widehat\rho(x,x)$, not time-varying correlation. Approximate readings from the figure are about .43 near $x=-4$ versus .22 near $x=+4$ for Boeing–Alcoa; about .40 versus .22 for Boeing–Caterpillar; and about .31 versus .46 for Caterpillar–Alcoa. These are visual approximations, not tabulated estimates. The $x$ coordinate belongs to the processed data scale and should not automatically be interpreted as an unfiltered raw return percentage after GARCH standardization.

At diagonal points ±2, the authors report standard errors near .015 and tests supporting nonconstancy and asymmetry at significance .01 or better. They explicitly prefer a future whole-curve test to isolated point comparisons. No simultaneous confidence band or multiplicity-adjusted map test is reported in this paper. The results reject simple symmetric descriptions for these processed pairs at the examined points; they do not identify economic causes of asymmetry.

The diversification implication is conditional on location: the two Boeing pairs show stronger dependence in joint negative returns, while the Caterpillar–Alcoa slope goes the other way. To convert this into portfolio loss probabilities or optimal weights one needs local variances and a coherent joint density, not correlation values alone. Independently fitting three pairwise maps does not automatically produce a positive-semidefinite trivariate correlation matrix. The authors identify multivariate extension and dimensionality reduction as further work.

## Reimplementation boundaries and research use

The modified local objective, Gaussian-kernel integral, parameter constraints, and score-based estimation are sufficient to build the estimator from paired data. A reproducible implementation should store the entire local fit, bandwidth, objective value, Hessian condition, local density, and convergence status at each evaluation point, then verify constant correlation under Gaussian simulation and the predicted symmetry patterns under Student and GARCH examples. These diagnostics test the actual estimator rather than merely recreating attractive plots.

Exact replication of the published empirical curves additionally requires the original marginal filtering estimates, data-cleaning/alignment rules, chosen bandwidth and kernel-density settings, low-density cutoff, and numerical optimization details. The source says the algorithm was available from the authors on request; it does not embed complete code or all these settings.

The contribution is a signed, spatially resolved description of dependence calibrated to Gaussian correlation, with a local-likelihood estimator and an analysis of its statistical difficulty. Its most defensible use is exploratory dependence modeling and checking whether a proposed bivariate distribution captures asymmetric joint behavior. Tail probability, independence, causal contagion, and portfolio optimization claims require the additional conditions highlighted above. Treating the fitted map as an estimated function with scale and uncertainty preserves the method's value without overstating what local Gaussian approximation proves.

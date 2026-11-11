# Continuous Record Asymptotics for Rolling Sample Variance Estimators

Dean P. Foster and Dan B. Nelson, *Econometrica* 64(1), January 1996, pp. 139–174. This note follows the published article, including its proof appendix. Printed journal p. 139 is PDF p. 2; the local file includes a JSTOR cover.

Source: [VolatilityEstimation_FosterNelson_1996.pdf](../../Finance/VolatilityEstimation_FosterNelson_1996.pdf).

## Why this matters

A rolling sample variance contains two different errors. Squared returns are noisy measurements of variance, so collecting more observations helps. But the conditional variance changes while those observations are collected, so extending the window eventually measures an average of different risks. Foster and Nelson derive the joint effect, rather than treating variance as constant within a convenient calendar month. They obtain standard errors, optimal window lengths, and optimal weight shapes for an instantaneous conditional variance or covariance.

The target is local risk at a particular time. It is not the realized integrated variance over an entire day, nor an unrestricted optimal forecast of variance many months ahead. Historical smoothing may use observations on both sides of the target date; a usable current estimate must use only past observations. The paper quantifies the efficiency cost of that information constraint. Its exponentially declining weights arise from a local stochastic-variation argument and do not require fitting a complete GARCH likelihood.

The contribution also reaches conditional betas, through the delta method. Most important for replication, the standard error depends on an innovation correlation that returns alone cannot generally identify. Knowing the optimal one-sided weight shape therefore does not automatically identify the uncertainty around its output.

## Target, asymptotic experiment, and notation

Sections 1–2 consider increasingly frequent observations separated by $h$, while calendar time remains meaningful. Write the return increment as

$$
\Delta_h X_t=h\mu_t+\Delta_h M_t,
\qquad E_{t-h}[\Delta_h M_t]=0,
\qquad E_{t-h}[\Delta_h M_t\Delta_h M_t']=h\Omega_t.
$$

Here $X$ can be a vector of log prices, $\mu_t$ is a drift, and $\Omega_t$ is the instantaneous conditional covariance matrix relative to a specified information set. The paper works with triangular arrays, so the processes and information sets can depend on $h$. For readability that prefix is suppressed here. A diffusion example has stochastic volatility with its own martingale innovation; discrete models can also satisfy the assumptions.

A scalar variance evolves locally as

$$
\Delta_h\Omega_t=hA_t+\Delta_h M_t^*,
\qquad E_{t-h}[(\Delta_h M_t^*)^2]=h\Lambda_t.
$$

$A_t$ denotes variance drift, whereas $\Lambda_t$ is the instantaneous variance of variance innovations. These are different quantities. The symbol $\Omega$ already denotes variance, so $\Omega^2$ is variance squared, not volatility squared in a second independent convention.

Define the squared-return measurement innovation by

$$
\Delta_h B_t=h^{-1/2}\{(\Delta_h M_t)^2-h\Omega_t\}.
$$

Its local variance is $h\theta_t$. If the standardized return innovation has conditional kurtosis $\kappa_t$, then $\theta_t=(\kappa_t-1)\Omega_t^2$; conditional normality gives $2\Omega_t^2$. The multivariate paper uses four-index tensors for cross-covariances among entries of $\Omega$, $B$, and $M^*$.

The third local parameter, $\rho_t$, measures correlation between the squared-return measurement innovation and the relevant next variance innovation. It is not the familiar correlation between a signed return shock and a volatility shock. The distinction is essential: a continuous stochastic-volatility diffusion can have leverage while the paper's $\rho$ is zero. In the GARCH examples $\rho=1$, because updating conditional variance is driven by squared-return surprises.

The observation window has calendar width proportional to $\sqrt h$, while its number of observations is proportional to $h^{-1/2}$. Thus the window shrinks in time but contains more observations. Measurement error is of order $h^{1/4}$, and $h^{-1/4}(\widehat\Omega_T-\Omega_T)$ has a nondegenerate limiting distribution. The quarter-power rate reflects rough stochastic movement of variance. Smoother deterministic volatility assumptions can yield faster rates, but those are a different experiment.

## Conditions and the error decomposition

Assumptions A–D impose locally controlled drift and conditional moments, nondegenerate innovation variances, and sufficiently slow variation of $\theta$, $\Lambda$, and $\rho$ within the shrinking window. The relevant innovations must satisfy moment and martingale central-limit conditions. Weights have bounded local support, peak order $h^{-1/2}$, and normalization $\sum_t h w(t-T)=1$. Mean estimation contributes only lower-order terms under the stated boundedness conditions; that does not mean a grossly inconsistent or explosive mean correction is harmless.

For residuals $e_t=\Delta_hX_t-h\widehat\mu_t$, the scalar estimator is

$$
\widehat\Omega_T=\sum_t w(t-T)e_t^2.
$$

The normalization compensates for $e_t^2$ having conditional expectation approximately $h\Omega_t$. Equivalently, define normalized observations $z_t=e_t/\sqrt h$ and ordinary averaging weights $a_t=hw(t-T)$; then $\widehat\Omega_T=\sum a_t z_t^2$ and $\sum a_t=1$. This alternative is convenient in code and prevents an accidental extra factor of sampling frequency.

Theorem 1 decomposes the normalized error into a weighted sum of squared-return innovations plus a weighted sum of variance innovations. The second sum involves cumulative weights: past observations differ from the target because intervening changes in variance must be subtracted; future observations differ because later changes must be added. Drift remainders vanish at the leading order. Theorem 2 applies a martingale central limit theorem to those two sums jointly.

For a scalar entry, the resulting variance takes the form

$$
C=\theta S_{ww}+2\rho\sqrt{\theta\Lambda}S_{w\Psi}+\Lambda S_{\Psi\Psi}.
$$

$S_{ww}$ measures concentration of observation weights, $S_{\Psi\Psi}$ measures exposure to intervening variance innovations, and $S_{w\Psi}$ measures their overlap. The first term decreases when observations are averaged more broadly; the last generally increases. The middle term can offset or reinforce the other two and changes sign when lead weights are exchanged for lag weights.

The appendix proves the decomposition by expanding residual products, interchanging the cumulative sums, and separating drift from martingale increments. It bounds the mean-estimation and local-drift remainders, computes the conditional covariance, and invokes a martingale CLT. This proof structure matters: the result is not an ordinary independent-sample variance formula applied inside a window.

## Flat windows and a printed inconsistency

Let $n=n_0h^{-1/2}$ lagged observations and $m=m_0h^{-1/2}$ led observations receive equal weight. Equation (9), repeated on journal p. 153, gives

$$
C(n_0,m_0)=\frac{\theta}{n_0+m_0}
+\rho\sqrt{\theta\Lambda}\frac{m_0-n_0}{m_0+n_0}
+\Lambda\frac{m_0^3+n_0^3}{3(n_0+m_0)^2}.
$$

For past-only estimation, differentiation yields $n_0^*=\sqrt{3\theta/\Lambda}$. For future-only estimation, $m_0^*$ is the same. These lengths do not depend on $\rho$, because the cross term is constant within either one-sided class.

There is a material printed inconsistency in Theorem 4(i)–(ii). Substituting the optimal length into equation (9) gives

$$
C_{\mathrm{past}}^*=\left(\frac{2}{\sqrt3}-\rho\right)\sqrt{\theta\Lambda},
\qquad
C_{\mathrm{future}}^*=\left(\frac{2}{\sqrt3}+\rho\right)\sqrt{\theta\Lambda}.
$$

The theorem prints $(2\mp\rho)\sqrt{\theta\Lambda/3}$ instead. These expressions agree at $\rho=0$ but not generally. The formulas above are a direct algebraic derivation from the displayed objective, and are labeled as such rather than silently attributed to the theorem. They also match the interior solution continuously at its one-sided boundary.

When $|\rho|\le\sqrt{3/4}$, the theorem's interior optimum is

$$
n_0^*=\sqrt{3(1-\rho^2)\theta/\Lambda}+\rho\sqrt{\theta/\Lambda},
\qquad
m_0^*=\sqrt{3(1-\rho^2)\theta/\Lambda}-\rho\sqrt{\theta/\Lambda},
$$

with $C^*=\sqrt{\theta\Lambda(1-\rho^2)/3}$. Beyond that range, nonnegative window lengths force the appropriate one-sided solution. Positive $\rho$ favors lagged observations; negative $\rho$ favors future observations.

At $\rho=0$, the optimal two-sided estimator uses equal lead and lag lengths, each equal to the optimal one-sided length. It therefore uses twice as many observations, and its asymptotic error variance is half as large. This is a smoothing advantage obtained by adding future information, not a free improvement available to a real-time trading system.

## Exponential weights and dominance

Theorem 5 minimizes over weight shapes as well as lengths. In rescaled local time, let $\alpha=\sqrt{\Lambda/\theta}$. The optimal past-only kernel is

$$
w(s)=\alpha e^{\alpha s}\mathbf1_{\{s<0\}},
\qquad C_{\mathrm{past,exp}}=\sqrt{\theta\Lambda}(1-\rho).
$$

The future-only kernel reverses time and has variance $\sqrt{\theta\Lambda}(1+\rho)$. With both sides available, define $p=(1-\rho)/2$. Then

$$
w(s)=\begin{cases}
p\alpha e^{-\alpha s},&s\ge0,\\
(1-p)\alpha e^{\alpha s},&s<0,
\end{cases}
\qquad
C_{\mathrm{two,exp}}=\tfrac12\sqrt{\theta\Lambda}(1-\rho^2).
$$

The kernel's decay rate is identical on both sides, while total mass shifts with $\rho$. The proof holds that mass fixed, minimizes the squared-weight and integrated-cumulative-weight terms, and then optimizes the division of mass. Writing any candidate as the exponential kernel plus a zero-integral perturbation leaves nonnegative squared terms, establishing optimality within the class.

At $\rho=0$, the optimal flat-window variance divided by the optimal exponential variance is $2/\sqrt3$. Its square root is about 1.075, the roughly 7% standard-error disadvantage illustrated in Figure 1. A decay rate is not a window length; substituting the estimated number of observations directly as an exponential coefficient would be a dimensional error.

The theorem's ideal exponential kernel has infinite support, whereas the formal regularity assumptions use compact support. The paper handles this by arbitrarily close truncation. A numerical implementation should specify a tail cutoff, discard the corresponding tail mass, and renormalize; no particular cutoff is supplied in the article. Discrete weights proportional to $e^{-\alpha j}$ are a practical approximation in daily units. The distinction between the continuous approximation and the exact finite-grid normalization should be retained.

Theorem 6 gives a useful weaker result requiring no estimates of the local nuisance parameters. Keep a flat window's total lead and lag masses, but replace each side's constant weights by appropriately scaled exponential decline. This lowers leading error variance for every admissible $\theta$, $\Lambda$, and $\rho$. Thus uncertainty about the exact optimal decay rate does not vindicate flat weights as generally efficient.

## Calendar blocks and conditional betas

A monthly sample variance estimates the same value for every point inside a block. It is effectively future-only at the beginning, past-only at the end, and two-sided in the middle. For a block of rescaled length $k_0$, equation (16) gives position-dependent error variance. At $\rho=0$ it is smallest near the midpoint, producing the bowed confidence-interval pattern in Figures 1–2.

Averaged across the block, the error variance is $\theta/k_0+\Lambda k_0/6$. A centered rolling flat window with the same total length has $\theta/k_0+\Lambda k_0/12$. The sampling component is unchanged, but the variance-drift contribution halves. Treating the block's variance as actually constant drops the entire second term and overstates measurement precision.

Section 4 applies the joint covariance CLT to $\beta_j=\Omega_{1j}/\Omega_{11}$, with market return indexed by 1. If $C$ is the asymptotic covariance tensor, the beta error variance is

$$
C_\beta=\Omega_{11}^{-2}\{C_{1j1j}+\beta_j^2C_{1111}-2\beta_j C_{111j}\}.
$$

The numerator's covariance term cannot be discarded: estimated covariance and estimated market variance use the same returns. If identical weights estimate numerator and denominator, the estimator is a weighted regression slope. Applying the same delta-method combination to $\theta$, $\Lambda$, and their cross-covariance produces beta-specific nuisance parameters, after which the same exponential-weight and dominance results apply. A market variance bounded away from zero is necessary for a stable ratio approximation.

Entry-specific optimal covariance weights need not preserve positive semidefiniteness of the assembled matrix. The paper studies unconstrained linear estimation and explicitly leaves eigenvalue and factor restrictions for future work. A common nonnegative weight sequence preserves positive semidefiniteness of weighted outer products, but that additional implementation restriction may sacrifice entrywise optimality.

## Estimating nuisance parameters and the identification limit

Section 2.3 estimates $\theta$ and $\Lambda$ using differences between adjacent local variance estimates at two block lengths. Such differences combine squared-return noise, which declines inversely with block length, with true variance variation, which increases with length. Estimation occurs over a wider neighborhood than the final local-risk window, but still one over which the nuisance parameters can be treated as sufficiently stable.

A useful daily-unit restatement makes the mechanism explicit. Suppose $\theta_t=\theta_0\Omega_t^2$ and $\Lambda_t=\Lambda_0\Omega_t^2$, as in the empirical application. Let $V^-_L(t)$ and $V^+_L(t)$ average squared residuals in adjacent past and future blocks of length $L$, and form a suitably normalized block difference. To leading local order its average squared value satisfies

$$
D(L)\approx\frac{2\theta_0}{L}+\frac{2\Lambda_0 L}{3}.
$$

Using two different lengths $L_s,L_l$ therefore gives the moment solution

$$
\widehat\Lambda_0=\frac{3\{L_lD(L_l)-L_sD(L_s)\}}{2(L_l^2-L_s^2)},
\qquad
\widehat\theta_0=\frac{L_sD(L_s)}2-\frac{\widehat\Lambda_0 L_s^2}{3}.
$$

These equations express the paper's two-scale logic in observation units; they are not a claim that the publication supplies those exact programming conventions. Its equations (10′)–(11′) use normalized adjacent-block differences and variance-level rescaling. Equation (12) instead uses squared log ratios of neighboring one-sided variance estimates and subtracts the sampling-noise correction. A first-order expansion of the logarithm connects the approaches. The appendix proves consistency for trimmed versions of the moment averages, not arbitrary unbounded averages without additional integrability assumptions.

Crucially, $\rho$ cannot generally be estimated from returns alone. The same observed-return law can be represented using a latent-volatility information set with $\rho=0$, or an observable-return information set with GARCH-like $\rho=1$. The target conditional variance changes with that information set. Selecting $\rho=0$ is an identifying assumption, not a test result. One-sided optimal decay rates remain available because they depend on $\Lambda/\theta$, but their standard errors still depend on $\rho$.

## S&P 500 experiment and implementation sequence

Section 5 uses daily continuously compounded capital gains on the S&P 500 from January 1928 through December 1990. These are capital gains rather than an explicitly documented dividend-reinvested total-return series. The return autocorrelation at lag one is approximately 6%, with little longer-lag correlation. The authors prewhiten using an AR(1), then divide each residual by $\sqrt{1+0.228N_t}$, where $N_t$ counts preceding nontrading days. The 0.228 coefficient is imported from Nelson's estimate of nontrading-day variance accumulation.

They assume constant conditional kurtosis, conditionally homoskedastic log variance, and $\rho=0$. Thus $\theta_t/\Omega_t^2=\theta_0$ and $\Lambda_t/\Omega_t^2=\Lambda_0$ can be estimated across the sample. This use of the whole history, and of two-sided weights, makes the application retrospective smoothing. It is not an out-of-sample forecast competition.

The operational sequence is: construct the adjusted residual series; initialize a two-sided flat-window variance; estimate the nuisance ratios using the adjacent-block method; calculate optimal equal lead and lag lengths; rebuild the variance estimates; and iterate until the suggested length stabilizes. Starting from lengths below 52 observations suggested larger windows, and lengths above 54 suggested smaller ones. The authors settle on 52 observations in total.

Their estimates are $\widehat\theta_0=2.72$ and $\widehat\Lambda_0=0.0120$, giving exponential decay $\alpha=0.0665$ in daily units. Repeating with unadjusted capital gains gives 2.668 and 0.0124, total flat-window length 51, and decay 0.068. The adjustment matters conceptually, but its effect on these reported smoothing choices is small.

The source does not supply the raw-data vendor, exact AR coefficient and fitting convention, all calendar exclusions, block lengths used for nuisance estimation, boundary handling, trimming cutoff, convergence tolerance, or exponential truncation rule. Those details must be documented in a reproduction. The printed parameter formulas and reported fitted values support an independently specified implementation; they do not support a claim of bit-for-bit reproduction from the article alone.

## Simulation, uncertainty, and source qualifications

The Monte Carlo uses 600 replications, each with 16,885 observations, calibrated to the equity example:

$$
\log\Omega_t=-0.4246+0.9944\{\log\Omega_{t-1}+0.4246\}+Z_{2t},
\qquad r_t=\sqrt{\Omega_t}Z_{1t}.
$$

$Z_{2t}\sim N(0,0.0120)$ and $Z_{1t}$ is an independent standardized Student distribution with 12 degrees of freedom and variance one. Its kurtosis is 3.75, so the true $\theta_0$ is 2.75. The simulation repeats the empirical estimation procedure. Initialization and burn-in of log variance, random seeds, and exact finite-sample edge treatment are not specified.

Tables I–II show downward bias in both nuisance parameters. With the log-ratio equation (12), mean estimated $\Lambda_0$ is 0.01051 with across-replication standard deviation 0.0012; mean $\theta_0$ is 2.480 with standard deviation 0.082. With equation (11′), the corresponding means are 0.007 and 2.527, with standard deviations 0.00088 and 0.088. Reported true values are 0.0120 and 2.75.

The text reports an optimal true total flat length of 52.4 and estimated lengths of about 53 and 64, but its method attribution is difficult to reconcile with the displayed parameter means. Plugging the equation (12) means into $\sqrt{12\theta_0/\Lambda_0}$ gives approximately 53.2, while the equation (11′) means give approximately 65.8. A ratio of means need not equal the mean of ratios, but the direction suggests a labeling problem in the surrounding prose. The tables should be retained separately instead of silently resolving the ambiguity. Table II also prints a Monte Carlo standard error of 0.001 for $\Lambda_0$, inconsistent with 0.00088 divided by $\sqrt{600}$; that parenthetical figure should not be used as a verified standard error.

Coverage is the clearer diagnostic. For equation (12), intervals of one, two, and three estimated standard deviations cover 0.6393, 0.9306, and 0.9929 of simulated errors, versus normal benchmarks 0.6827, 0.9545, and 0.9973. Their Monte Carlo standard errors are 0.0007, 0.0004, and 0.0001. Equation (11′) gives 0.5915, 0.8991, and 0.9848, with standard errors 0.0008, 0.0006, and 0.0002. The intervals are too narrow, particularly for the level-difference estimator; the log-ratio method is materially better but not exactly calibrated.

Figures 5–6 use a log scale for standard deviation. Delta-method transformation gives log-variance uncertainty from variance uncertainty, and another factor of one-half converts log variance to log standard deviation. The plotted intervals are pointwise, not simultaneous bands for an entire sample path. A 95% pointwise construction does not imply a 95% probability that the whole volatility trajectory lies inside it.


## Translating the local solution into daily calculations

For a daily implementation of the empirical approximation, work directly with the standardized nuisance ratios $\theta_0$ and $\Lambda_0$. A past-only exponential estimator can be formed with discrete weights $a_j=(1-q)q^j$, $j=0,1,\ldots$, where $q=e^{-\alpha}$ and $\alpha=\sqrt{\Lambda_0/\theta_0}$. Here $j=0$ denotes the most recent squared residual available at the specified information cutoff. Shifting that convention by one observation changes whether the estimate is described as current filtered risk or next-period risk; write down the index rather than relying on a software package's label.

At the reported $\alpha=0.0665$, the implied daily decay is about 0.9357 and the half-life $\log(2)/\alpha$ is about 10.4 observations. These are calculations from the reported parameter, not additional estimates. The nominal 52-observation flat window and the exponential half-life describe different aspects of the weighting distribution. A two-sided symmetric smoother assigns half of its total mass to each side, with finite-grid treatment of the central observation handled explicitly. It should not count the same squared return twice without compensating normalization.

For an infinitely long one-sided geometric sequence, $\sum_j a_j^2=(1-q)/(1+q)$, giving an effective sample size $(1+q)/(1-q)$ of roughly 30 at that decay rate. This familiar constant-variance measure captures only sampling noise. It does not include the changing-target contribution represented by $\Lambda$, and therefore cannot replace the paper's full error formula. The example explains why a conventional weighted-sample standard error may look much smaller than the true local-risk uncertainty.

The empirical scale restrictions also make approximate uncertainty interpretable. At $\rho=0$, the optimal two-sided exponential variance of the variance-estimation error, divided by $\Omega_t^2$, is approximately $\tfrac12\sqrt{\theta_0\Lambda_0}$. Substituting 2.72 and 0.0120 gives about 0.0903, corresponding to a relative standard error around 0.300 for variance. Applying the delta method to log standard deviation halves that scale to about 0.150. These are daily-unit plug-in calculations under the paper's local approximation, not separately reported empirical confidence limits.

A nominal 95% pointwise interval for standard deviation could therefore be expressed approximately as the estimated standard deviation multiplied by $\exp(\pm1.96\times0.150)$, giving factors near 0.75 and 1.34. This calculation should be accompanied by the Monte Carlo undercoverage evidence: nominal asymptotic calibration is not the same as demonstrated finite-sample coverage. It also presumes the $\rho=0$ information-set choice and fixed nuisance estimates; changing either affects the interpretation.

Boundary handling deserves particular attention. Near the start or end of an observed sample, truncating a two-sided kernel and renormalizing changes its lead/lag mass. The interior standard-error expression no longer applies unchanged. A centered historical smoother computed through December 1990 cannot honestly supply its usual symmetric estimate at the final date without later observations. Options include reporting a shorter interior sample or using a separately derived one-sided boundary estimate; the article does not provide an explicit production boundary convention.

These steps permit independent code to reproduce the mathematical estimator while keeping its assumptions visible. They also provide numerical checks: weights must sum to one, the forecast must respect its information cutoff, and the chosen unit for returns must propagate consistently into $\Omega$, $\theta$, and $\Lambda$. Doubling the return unit multiplies variance by four and both local nuisance variances by sixteen, leaving the optimal ratio-based decay unchanged.

## Limits and practical interpretation

The local theory excludes important counterexamples. A return jump process may generate mostly zero increments and occasional enormous squared returns; shrinking windows then usually miss jumps, and the required local moment argument fails. Variance jumps can make estimation very accurate away from jumps but generate unusually large errors at jump times. Neither behavior is covered by treating the same Gaussian local CLT as universally valid.

Continuity alone is insufficient. The paper gives a moving-average volatility example whose shocks disappear abruptly after a fixed lag. Although sample paths can be continuous, predictable and unpredictable short-run changes have comparable order, violating the condition that local martingale noise dominates drift. Exponential weights are therefore optimal under the stated local dynamics, not for every process that visually appears smooth.

The paper also does not solve conditional-mean estimation, which requires long time spans rather than merely dense observations, or establish simultaneous inference for an evolving risk-return relation. Heavy conditional tails raise $\theta$ and reduce the efficiency of squared-return estimators. Robust absolute-return or constrained covariance alternatives are suggested, not developed and validated here.

For research implementation, the durable result is a three-part error budget: return measurement noise, movement in the latent risk target, and covariance between the two. A window choice should correspond to that target and information set. Retrospective smoothing, current filtering, and future integrated-risk forecasting should be labeled separately, and uncertainty should include changing volatility rather than only the sample variance's constant-risk formula.

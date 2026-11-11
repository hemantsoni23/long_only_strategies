# Systematic stress tests with entropic plausibility constraints

**Thomas Breuer and Imre Csiszár (2013).** *Journal of Banking & Finance* 37, 1552–1559; available online 28 April 2012. DOI: 10.1016/j.jbankfin.2012.04.013. [Source PDF](../../Finance/StressTestingEntropyEstimation_BreuerCsiszar_2013.pdf). All eight pages were read, including the proof and macroeconomic application in Appendices A–B. Equations and all three tables were checked visually. The text contains overlapping character layers; the visual document, rather than duplicated extraction, determines the transcription.

## Why this matters

A hand-selected adverse scenario can miss a more damaging scenario of comparable plausibility. Conversely, an alarming result can be produced by an implausible scenario. The paper replaces the choice of a few factor realizations by a search over alternative probability distributions close to a reference distribution. “Worst case” then means the largest expected portfolio loss obtainable within a specified information-distance budget.

The mathematical contribution is a maximum-loss theorem for general loss functions and reference distributions satisfying exponential-integrability conditions. It identifies the worst distribution as an exponential tilt and reduces the optimization over distributions to a scalar equation. The applications show why a worst distribution can change covariance as well as means, and can stress discrete migration or joint-default outcomes that are awkward to represent through a Mahalanobis ellipsoid.

The method does not remove judgment. The reference distribution, loss function, and entropy radius remain choices. Nor does it repair an incorrect mapping from factors to portfolio loss. The authors explicitly distinguish uncertainty about the factor distribution from misspecification of the loss function and acknowledge that system-wide feedback is difficult to capture without system-wide data.

## Object being stressed and exact optimization problem

Let $r$ denote the complete risk-factor state or path, $\nu$ its reference probability distribution, and $L(r)$ the portfolio loss, with positive values denoting losses. A mixed scenario is another distribution $Q$ on the same state space. It can represent a changed forecast distribution, uncertainty about parameters, or an alternative regime. It is not a single realized factor vector.

Relative entropy is directional:

$$
D(Q\Vert\nu)=\int \log\!\left(\frac{dQ}{d\nu}\right)dQ
$$

when $Q$ is absolutely continuous with respect to $\nu$, and is infinite otherwise. The ambiguity set and objective are

$$
\mathcal Q_k=\{Q:D(Q\Vert\nu)\leq k\},\qquad
\operatorname{MaxLoss}(L,k)=\sup_{Q\in\mathcal Q_k}E_Q[L].
$$

The direction $Q\Vert\nu$ is essential. Reversing it generally produces another optimizer. Absolute continuity means that the method cannot assign positive probability to an event the reference model declares impossible. An empirical reference with finitely many scenarios only permits reweighting those scenarios; it does not discover absent failure modes.

Under a fixed ambiguity set, the objective is a supremum of linear expectation operators. This explains its monotonicity, translation behavior, positive homogeneity, and subadditivity, where the expectations exist. Its dependence on the reference law of loss also explains the paper’s law-invariance claim. One-to-one changes of factor coordinates preserve the objective and relative entropy; the construction is not tied to the first two factor moments.

The comparison with traditional systematic stress testing is specific. The traditional problem maximizes $L(r)$ over a Mahalanobis ellipsoid of factor realizations. The proposed problem maximizes $E_Q[L]$ over distributions. A point mass is not generally a finite-entropy alternative to a continuous reference law, so these are not merely two parameterizations of the same feasible set.

## Maximum-loss theorem and existence conditions

Define the log moment-generating function

$$
\Lambda(\theta)=\log E_\nu[e^{\theta L}],\qquad \theta\geq0.
$$

For a nonconstant loss and an admissible positive radius, the theorem gives a parameter $\bar\theta>0$ satisfying

$$
\bar\theta\Lambda'(\bar\theta)-\Lambda(\bar\theta)=k.
$$

The worst distribution and loss are

$$
\frac{d\bar Q}{d\nu}(r)=e^{\bar\theta L(r)-\Lambda(\bar\theta)},\qquad
\operatorname{MaxLoss}(L,k)=\Lambda'(\bar\theta).
$$

Higher-loss states gain relative weight exponentially. This is an Esscher transform, with its parameter fixed by the entropy budget rather than chosen arbitrarily. At $k=0$, the feasible distribution is the reference and the result is $E_\nu[L]$; the strictly positive-root statement concerns positive radii.

The source’s conditions must be retained. First, $\theta_{\max}=\sup\{\theta:\Lambda(\theta)<\infty\}$ must be positive. Second, if $b=\operatorname{ess\,sup}L$ is finite, the regular formula is stated for $k<-\log\nu(L=b)$. If there is a positive reference atom on the largest loss, sufficient entropy can put all mass on that atom and the maximum saturates at $b$. Third, when $\theta_{\max}$, $\Lambda(\theta_{\max})$, and $\Lambda'(\theta_{\max})$ are all finite, the theorem restricts the radius to the entropy attainable at that boundary. Beyond it, the stated exponential-family solution need not apply.

These conditions materially limit the claim of generality. A loss distribution with no positive exponential moment does not satisfy the theorem. Heavy-tailed losses cannot be handled by evaluating a finite-sample exponential tilt and assuming it solves the population problem. A finite simulation sample always has a largest observation and can conceal an integrability failure in the underlying model.

## Proof mechanism and computational consequence

For the exponential tilt $Q_\theta$, differentiation gives

$$
E_{Q_\theta}[L]=\Lambda'(\theta),\qquad
D(Q_\theta\Vert\nu)=\theta\Lambda'(\theta)-\Lambda(\theta).
$$

The key identity for an arbitrary feasible distribution is

$$
D(Q\Vert\nu)=D(Q\Vert Q_{\bar\theta})
+\bar\theta E_Q[L]-\Lambda(\bar\theta).
$$

Since the first term on the right is nonnegative and the left is at most $k=\bar\theta\Lambda'(\bar\theta)-\Lambda(\bar\theta)$, it follows that $E_Q[L]\leq\Lambda'(\bar\theta)$. The tilt attains the bound. Appendix A establishes the corresponding existence and uniqueness properties through convexity and the convex conjugate of $\Lambda$.

A useful implementation identity is

$$
\frac{d}{d\theta}\left[\theta\Lambda'(\theta)-\Lambda(\theta)\right]
=\theta\Lambda''(\theta)
=\theta\operatorname{Var}_{Q_\theta}(L)\geq0.
$$

Thus a bracketed one-dimensional root solver is natural. The source says the method avoids numerical optimization; that means it avoids a general search over distributions or factor vectors. Computing expectations, integrals, derivatives, and the scalar root can still be expensive, especially for a nonlinear portfolio.

For discrete or simulated scenarios with reference probabilities $p_i$ and losses $l_i$, calculate $a_i=\log p_i+\theta l_i$ and use log-sum-exp for $\Lambda$. Obtain normalized tilted weights $q_i$, compute $\Lambda'=\sum q_i l_i$, and solve $\theta\Lambda'-\Lambda=k$. Verify weight normalization and the achieved entropy, and record whether the solution approaches the support’s maximum loss. The paper does not prescribe a tolerance, quadrature scheme, random seed, or Monte Carlo error estimator.

## Choosing the entropy radius

The paper relates $k$ to a tail probability: conditioning the reference law on an event $A$ costs entropy $-\log\nu(A)$. Consequently, a worst conditional mean over events of probability at least $e^{-k}$ is bounded by MaxLoss. A 1% tail corresponds to $k=-\log(0.01)\simeq4.605$. This is a useful scale comparison, not an assertion that MaxLoss equals expected shortfall at that tail probability for arbitrary losses.

Another proposed calibration compares a crisis-regime distribution with a quiet-regime distribution and measures their relative entropy. That requires estimating both distributions and does not come with a finite-sample confidence guarantee in this paper. For a linear Gaussian portfolio, the radius also has an exact geometric relation to a mean-shift distance, $h=\sqrt{2k}$.

Entropy is dimensionless but its numerical value depends on the full distributions being compared. The same $k$ does not necessarily correspond to the same severity after changing the horizon, dependence model, or scenario representation. A reproducible stress exercise must state those elements and the economic interpretation of its chosen radius.

## Gaussian linear and quadratic portfolios

For the linear example, $r\sim N(\mu,\Sigma)$ and $L(r)=l^T(\mu-r)$. The tilted distribution has unchanged covariance and mean

$$
\bar\mu=\mu-\sqrt{2k}\frac{\Sigma l}{\sqrt{l^T\Sigma l}},\qquad
\operatorname{MaxLoss}=\sqrt{2k}\sqrt{l^T\Sigma l}.
$$

The same loss is obtained from the worst pure realization in the Mahalanobis ellipsoid of radius $h=\sqrt{2k}$. This equality is a special property of the linear Gaussian case, not a general equivalence between mixed and pure stress testing. Zero variance in the loss direction is a degenerate case handled separately.

Section 5 defines its quadratic example as

$$
L(r)=-\frac12(\mu-r)^T\Gamma(\mu-r)-l^T(\mu-r).
$$

Its linear sign convention differs from the preceding section. Setting $x=r-\mu$, this is $l^Tx-\tfrac12x^T\Gamma x$. Preserve that sign when reproducing the stressed mean. Take symmetric $\Gamma$, $\Sigma=U^TU$, $A=U\Gamma U^T$, $v=Ul$, and

$$
S(\theta)=(I+\theta A)^{-1}.
$$

Where $I+\theta A$ is positive definite, completing the Gaussian square gives

$$
\Sigma_\theta=U^TS(\theta)U,\qquad
\mu_\theta=\mu+\theta U^TS(\theta)Ul.
$$

For eigenvalues $\gamma_i$ of $A$, the entropy equation in Proposition 2 is

$$
\frac12\left[\theta^2v^TS(\theta)^2v
-\sum_i\left(\frac{\theta\gamma_i}{1+\theta\gamma_i}
-\log(1+\theta\gamma_i)\right)\right]=k.
$$

The corresponding expected loss is

$$
\frac{\theta}{2}v^T\left[S(\theta)+S(\theta)^2\right]v
-\frac12\sum_i\frac{\gamma_i}{1+\theta\gamma_i}.
$$

If an eigenvalue is negative, the admissible positive parameter is bounded above by $-1/\min_i\gamma_i$. The positive-definiteness check must be inside the root-search procedure; crossing that boundary does not merely create a poor approximation but invalidates the tilted normal density.

The quadratic tilt changes covariance as well as means. It need not increase every variance: positive curvature in $\Gamma$ penalizes large squared moves in this loss convention and can contract covariance, while negative curvature can expand it. The macroeconomic example happens to show variance increases. Generalizing that observed direction to every quadratic portfolio would be incorrect.

## Discrete rating migration: complete inputs and reproduced scale

Section 6 considers an A-rated bond over one year, with terminal migration losses based on five-year industrial-bond credit spreads from Bloomberg. At $k=2$, Table 1 reports:

| Final rating | AA1–2 | AA3 | A | BBB | BB | Default |
|---|---:|---:|---:|---:|---:|---:|
| Loss, percent of value | −3.20 | −1.07 | 0.00 | 3.75 | 15.83 | 51.80 |
| Reference probability, percent | 0.09 | 2.60 | 90.75 | 5.50 | 1.00 | 0.06 |
| Reported worst probability, percent | 0.036 | 1.34 | 53.53 | 5.37 | 4.91 | 34.8 |

The exact formula is $q_i=p_i e^{\bar\theta l_i}/\sum_jp_je^{\bar\theta l_j}$. Concentrating entirely on the maximum-loss class requires $k\geq-\log p_{\mathrm{default}}$, approximately 7.419 for the displayed 0.06% default probability. Below that threshold, the scalar tilt determines the solution.

The source reports an expected loss increase from 0.37% to 19.07%. Using precisely the displayed rounded inputs, an independent scalar calculation gives $\bar\theta\simeq13.301674$ when losses are fractions of value, an achieved entropy of 2, and expected loss **18.9936%**. The result is close but does not exactly reproduce 19.07%; the displayed stressed weights themselves also give a slightly different mean. Unreported precision or an internal inconsistency prevents claiming exact numerical agreement.

The prose says downgrades receive higher probabilities, but BBB falls from 5.50% to 5.37% in its table. Exponential tilting increases relative odds of more harmful outcomes; it does not require every positive-loss state’s absolute probability to rise. The normalization can reduce probabilities of moderate losses when severe losses gain enough weight.

## Two-name default example and a formula correction

Section 7 starts with correlated standard-normal latent asset values, default thresholds $K_i=\Phi^{-1}(p_i)$, and joint default probability $p_{AB}=\Phi_{2,\rho}(K_A,K_B)$. Portfolio loss is the sum of losses on defaulted names. The reference probabilities of no default, A only, B only, and both are

$$
1-p_A-p_B+p_{AB},\quad p_A-p_{AB},\quad p_B-p_{AB},\quad p_{AB}.
$$

Apply the same discrete tilt to losses $0,l_A,l_B,l_A+l_B$. In particular,

$$
\bar p_{A\text{ only}}=e^{\bar\theta l_A-\Lambda(\bar\theta)}(p_A-p_{AB}),
$$

and similarly for B only. The printed formulas instead subtract the stressed joint probability after tilting the marginal reference probability; that does not produce the correct region probability. The exponential factor must multiply the reference region probability as a whole. This correction follows directly from the stated density and preserves normalization.

The numerical text uses $p_A=1.33\%$, $p_B=0.02\%$, asset correlation 0.5, $l_A=0.5$, and $l_B=0.4$. The table caption reverses the order in which the two LGDs are mentioned; the stated expected loss is consistent with the body’s assignment. At $k=2$, reported outcome probabilities are:

| Outcome | No default | A only | B only | Both |
|---|---:|---:|---:|---:|
| Reference, percent | 98.66 | 1.32 | 0.013 | 0.007 |
| Stressed, percent | 43.02 | 47.94 | 0.19 | 8.85 |

Default-indicator correlation rises from 4.23% to 26.15%, and expected portfolio loss from 0.67% to 32.01%. These are not stressed latent Gaussian correlations: the tilted joint asset-value distribution is no longer normal. Nor is correlation being changed while holding the individual default probabilities fixed; the stressed default marginals change dramatically as well.

Using the rounded four-state reference probabilities yields expected loss 31.9854% and indicator correlation approximately 26.00%, close to the table. Recovering its precise figures requires the unrounded bivariate-normal probabilities. Correlation can be reconstructed from $\bar p_{AB}$ and the stressed marginal probabilities through the ordinary Bernoulli covariance formula.

## Macroeconomic credit stress application

Appendix B uses a sectoral credit model and parameter estimates from Breuer and coauthors (2012), based on Spanish central-credit-register default data from **1984 Q1 to 2006 Q4**. The register covers loans exceeding **€6,000**. Loan loss is $D_{i,t}LGD_kEAD_i$, with sector-homogeneous LGD and default probabilities. The object stressed is expected cumulative loan loss conditional on the future macroeconomic path, integrating the other modeled shocks.

Sector default probabilities are $\pi_{k,t}=\Phi(z_{k,t})$, with

$$
z_{k,t}=\alpha_k+\rho_kz_{k,t-1}
+\sum_j\gamma_{k,j}\Delta x_{t-j}+\beta_kf_t+u_{k,t}.
$$

The implementation retains lags two, three, and four; it sets the first and higher-than-fourth lag coefficients to zero. The macro vector is $x_t=[GDP_t/GDP_{t-4}-1,\ d_t]^T$, with $d_t$ the real interest rate. Its changes follow

$$
\Delta x_t=A_0+A_1\Delta x_{t-1}+r_t,
$$

where $A_1$ is diagonal, $r_t$ is i.i.d. normal with covariance $\Sigma$, $f_t$ is i.i.d. standard normal, and sector shocks $u_{k,t}$ are i.i.d. normal with variance $\sigma_k^2$. The three shock families are mutually independent. The primitive macro stress factors are the future residual path, which determines the macro path given initial conditions. The distinction between year-on-year GDP growth in $x_t$ and its subsequent first difference in $\Delta x_t$ is necessary for reproduction.

The benchmark imposes a three-standard-deviation first-quarter GDP decline with other macro factors at expected levels. Its Mahalanobis distance is 3.34, corresponding to $k\simeq5.58$. The alternatives approximate the conditional expected-loss function linearly or quadratically and apply the Gaussian formulas. They are exact worst distributions for those approximations, not exact solutions for the original nonlinear credit-loss mapping.

Table B.1 reports loss increases of **18.11%** for the hand-picked realization, **24.81%** for the linear mixed-scenario approximation, and **29.53%** for the quadratic approximation. The final discussion instead says **29.67%** for the quadratic result; the two printed numbers conflict. Both should remain visible rather than silently selecting a supposedly exact value.

The table’s six listed GDP mean shifts under the quadratic tilt are −1.91, −0.74, −0.90, −0.52, −0.30, and −0.07 reference standard deviations. Interest-rate shifts are 1.16, 1.34, 1.24, 1.00, 0.67, and 0.31. Linear-tilt shifts are similar, but its covariance is unchanged. Quadratic-tilt variance increments are positive: GDP entries 0.062, 0.032, 0.036, 0.020, 0.007, 0.002; interest entries 0.028, 0.042, 0.040, 0.030, 0.016, 0.004 in the table’s normalization. This illustrates the additional expected loss attributable to altered dispersion rather than simply a more negative first-quarter GDP mean.

## What is reproducible and what remains missing

The discrete stress examples are reconstructible up to the source’s input rounding and formula issues. The Gaussian cases require a covariance factorization, symmetric curvature matrix, admissible tilt domain, and a scalar root solve. A useful verification computes the resulting Gaussian KL divergence directly from its mean and covariance and compares it with $k$; the achieved expected loss should also agree with the transformed quadratic expectation.

Exact reproduction of the macro table requires the referenced sector exposures, LGDs, coefficient estimates, initial state, precise horizon alignment, and the fitted linear or quadratic approximation. These inputs are not reproduced completely in the eight-page article. The lag structure makes it especially important to specify which future macro innovations can influence losses before the terminal horizon; the six displayed factor coordinates alone are insufficient to infer every timing choice. The paper provides no raw loan panel, numerical integration code, approximation-error assessment, confidence interval, or out-of-sample validation.

The method’s main benefit is a transparent optimization criterion over a declared model neighborhood. It does not make the reference law correct, guarantee that the entropy radius includes a future crisis, or endogenize fire sales and institutional responses. For a nonlinear portfolio, the loss mapping and positive exponential moments deserve at least as much scrutiny as the convenience of the exponential-tilt solution.

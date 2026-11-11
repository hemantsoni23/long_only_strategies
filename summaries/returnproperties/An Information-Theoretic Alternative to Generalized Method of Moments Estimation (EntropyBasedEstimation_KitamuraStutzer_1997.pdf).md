# An Information-Theoretic Alternative to Generalized Method of Moments Estimation

**Yuichi Kitamura and Michael Stutzer (1997).** *Econometrica* 65(4), July, pp. 861–874. Manuscript received May 1995; final revision August 1996.

**Source:** [EntropyBasedEstimation_KitamuraStutzer_1997.pdf](../../Finance/EncyclopediaQuantFinance/EntropyBasedEstimation_KitamuraStutzer_1997.pdf). The PDF has 14 scanned pages, all including the proof appendix inspected visually. Printed page numbers are used below. This note concerns the 1997 estimator and inference paper, a distinct work from the authors’ 2002 asset-pricing interpretation and experiments.

## Why this matters

Many financial models imply moments rather than a complete distribution: a pricing error is orthogonal to instruments, an innovation has zero conditional mean, or several observations share a variance parameter. Generalized method of moments estimates parameters by making sample moments small under a quadratic metric. Efficient GMM estimates that metric from the same data. In small samples, errors in moments and errors in their estimated covariance can interact unfavorably.

Kitamura and Stutzer propose a different objective: find the smallest change in the probability distribution that makes the model’s moments exactly valid, and choose the parameter that requires the least change. The change is measured by a particular direction of Kullback–Leibler divergence. Convex duality converts the probability problem into exponential tilting, so implementation does not require optimizing one unconstrained probability per observation alongside the structural parameters.

The distinctive contribution is an estimator that accommodates weak serial dependence by smoothing the moment observations before tilting. Under stated assumptions it has the same first-order asymptotic covariance as optimally weighted GMM. The authors also derive overidentification and parameter-restriction tests with the correct smoothing normalization. The paper does not prove universal finite-sample superiority or present a large numerical comparison. Its main deliverable is a theoretically justified alternative objective and a precise inference framework.

## Moment model and the GMM comparator

Let $x_t$, $t=1,\ldots,T$, be a stationary vector process; let $\beta\in\Theta\subset\mathbb R^m$ be the parameter; and let $f(x,\beta)\in\mathbb R^r$ collect the observable moment functions. The population probability measure is $\mu$. The maintained model is

$$
E_\mu[f(x,\beta^*)]=0,
$$

with a unique identified $\beta^*$. Define $f_t(\beta)=f(x_t,\beta)$ and $\bar f_T(\beta)=T^{-1}\sum_t f_t(\beta)$. GMM chooses

$$
\hat\beta_{\mathrm{GMM}}=\arg\min_{\beta\in\Theta}
\bar f_T(\beta)'\hat W_T\bar f_T(\beta).
$$

The efficient weight is the inverse long-run covariance of the moment process, rather than merely its contemporaneous covariance. The source calls optimally weighted GMM optimal minimum distance, or OMD. It stresses an existing small-sample concern: the estimated weighting matrix and the sample moments can have correlated sampling errors. Equal weighting sometimes improves finite-sample behavior in earlier studies, but sacrifices asymptotic efficiency. The proposed estimator aims to preserve that efficiency without using a separately plugged-in quadratic weighting objective.

The dimensional distinction matters. There are $m$ structural parameters and $r$ moment restrictions. Overidentification testing requires $r>m$ together with rank and identification assumptions; the difference $r-m$ determines the asymptotic degrees of freedom.

## The probability projection and its direction

For each parameter, consider probability measures absolutely continuous with respect to $\mu$ that satisfy the moments:

$$
\mathcal P(\beta)=\{P:E_P[f(x,\beta)]=0,\ P\ll\mu\}.
$$

The population projection is equation (4):

$$
\min_{P\in\mathcal P(\beta)}D(P\Vert\mu),\qquad
D(P\Vert\mu)=\int\log\left(\frac{dP}{d\mu}\right)dP.
$$

The integration is with respect to the altered distribution $P$. Reversing the arguments produces a different criterion. The authors explain on p. 864 that using the reversed divergence leads to empirical likelihood; exponential tilting and empirical likelihood should not be treated as two names for the same finite-sample estimator.

Relative entropy is nonnegative and vanishes when the distributions agree almost everywhere. At the correct parameter, the original measure already satisfies the moments, so the required change is zero. At an incorrect identified parameter, making the restrictions true requires a nonzero change in measure. Estimation seeks the parameter whose projection is closest to the original distribution.

This is a statistical distributional adjustment. It does not assert that the data were physically generated under the tilted probabilities, nor does it grant an incorrectly specified economic model truth by reweighting observations. The size of the necessary adjustment is precisely what the specification test uses.

## Dual formulation and exponential tilting

Let $\gamma\in\mathbb R^r$ be the multiplier on the moment restrictions and define

$$
\mathcal M(\beta,\gamma)=E_\mu[\exp(\gamma'f(x,\beta))].
$$

For a fixed $\beta$, solve the convex problem $\gamma(\beta)=\arg\min_\gamma\mathcal M(\beta,\gamma)$. Its first-order condition is the exponentially weighted zero-moment condition. Equations (5)–(7) give

$$
\frac{dP(\beta)}{d\mu}
=\frac{\exp(\gamma(\beta)'f(x,\beta))}{\mathcal M(\beta,\gamma(\beta))},\qquad
D(P(\beta)\Vert\mu)=-\log\mathcal M(\beta,\gamma(\beta)).
$$

To verify the entropy expression, insert the log density into its expectation under $P$. The term $\gamma'E_P[f]$ is zero by the constraint, leaving minus the log normalizer. Hence the parameter minimizes this nonnegative divergence, equivalently maximizing the minimized exponential moment:

$$
\beta^*=\arg\max_\beta\min_\gamma\mathcal M(\beta,\gamma).
$$

The signs and order of optimization are essential. The structural parameter is on the maximizing side of a saddle problem; the multiplier is on the minimizing side. Jointly minimizing the raw exponential objective over both variables is not the proposed estimator. The value at the correctly specified population solution is one and its multiplier is zero.

In a finite IID sample, the corresponding tilted probability of observation $t$ is proportional to $\exp(\gamma'f_t)$. These weights are positive and sum to one after normalization. A finite interior solution requires a feasible moment geometry: zero must be in the appropriate convex hull of the observed moment vectors. This practical feasibility check follows from the weighted-moment equation. The paper’s asymptotic assumptions do not guarantee that every short realized sample has a well-behaved interior optimizer.

## Serial dependence: smooth the moments before tilting

Simply replacing the population expectation by the sample average produces a consistent estimator under the source’s assumptions, but one that is generally inefficient with serial dependence. To recover efficient weighting, equation (8) constructs a flat-kernel average:

$$
\tilde f_t(\beta)=\frac{1}{2K+1}\sum_{k=-K}^{K}f(x_{t-k},\beta).
$$

Let $L=2K+1$. The bandwidth grows with the sample, subject to $K\to\infty$ and $K^2/T\to0$. The feasible criterion, equation (9), is

$$
\hat Q_T(\beta,\gamma)=\frac1T\sum_{t=1}^{T}
\exp(\gamma'\tilde f_t(\beta)),\qquad
(\hat\beta_T,\hat\gamma_T)=\arg\max_\beta\min_\gamma\hat Q_T(\beta,\gamma).
$$

The model functions are evaluated first and then averaged. For a nonlinear moment function, applying the function to an averaged raw observation would generally define a different estimator. The overlapping windows do not create independent observations. They encode serial covariance in the curvature of the tilting criterion.

The flat kernel is selected for ease of derivation, not claimed optimal in all applications. On p. 867 the authors connect the smoothed second moments to a Bartlett-weighted long-run covariance estimate. The covariance of an average over $L$ consecutive observations contains each lag with a triangular multiplicity. Multiplying its second moment by $L$ therefore approximates the long-run covariance.

The formulas sum over $t=1,\ldots,T$ despite needing observations outside the nominal endpoints. The appendix treats endpoint differences as asymptotically negligible but does not prescribe one production convention. A reproducible implementation must choose, for example, complete-window trimming and an effective sample size, or a documented boundary treatment. It must use that convention consistently in the objective, covariance estimate, and test scaling. This is a source omission to record, not an invitation to silently mix denominators.

For IID data set $K=0$. For dependent data a fixed zero bandwidth is not generally efficient. The source notes a Bartlett bandwidth growth rate of order $T^{1/3}$ as compatible with its rate restriction, but supplies neither a calibrated constant nor a data-driven bandwidth selection algorithm.

## Numerical implementation

The paper suggests starting with an equal-weight GMM estimate for $\beta$ and zero for $\gamma$, then using Newton–Raphson on the saddle first-order conditions. The unknown vector has $m+r$ components. Analytical derivatives with respect to the multiplier are especially simple:

$$
\nabla_\gamma\hat Q_T=\frac1T\sum_t e^{\gamma'\tilde f_t}\tilde f_t,\qquad
\nabla^2_{\gamma\gamma}\hat Q_T=\frac1T\sum_t e^{\gamma'\tilde f_t}\tilde f_t\tilde f_t'.
$$

A practical equivalent is nested optimization: solve the convex multiplier problem for each candidate structural parameter, then minimize the resulting entropy over $\beta$. Numerical recommendations here are implementation deductions, not settings supplied by the authors. Work with the log-sum-exp objective to prevent overflow; its multiplier gradient is the weighted mean and its Hessian is the weighted covariance. Warm-start successive inner solves and verify the tilted moment residual, objective ordering, and final stationarity.

The profile objective can be nonconvex in the structural parameter even though the inner problem is convex. Multiple starting values, identification checks, and parameter-bound handling may therefore be necessary. A failed inner solve must not be passed to the outer optimizer as a valid high-quality fit. Very concentrated weights or large multipliers can indicate difficult moment geometry or weak identification, although the paper does not provide a formal diagnostic threshold.

The authors also describe a computational shortcut: one Newton step from a sufficiently good initial estimate can retain the first-order asymptotic properties under additional regularity. The p. 865 footnote requires integrable bounds on the first three derivatives of the moment function near the true parameter. It mentions Guo’s separate simulation in a latent-variable setting, with lower bias and nearly identical root mean squared errors relative to a two-step GMM comparator. It does not provide the numerical design or results needed to reproduce that simulation within this paper.

## Assumptions and what the theorems actually cover

The source states eleven assumptions on p. 866. Their roles should be preserved when transferring the method to financial data:

- The process is stationary and ergodic; the parameter space is compact and $m$ dimensional; the correct parameter is uniquely identified.
- Moment functions are almost surely continuous in the parameter. Their uncentered second-moment matrix is nonsingular throughout the parameter space.
- A local exponential-envelope condition controls the supremum over nearby parameters for multipliers near zero. This is stronger than the ordinary finite-moment conditions often used for GMM.
- For asymptotic normality, strong mixing coefficients satisfy a summability requirement: for some $b>1$, $\sum_{n\ge1}\alpha_n^{1-1/b}<\infty$.
- The variance of the normalized partial sum of true moments converges to a positive definite matrix $S$.
- The moment functions are continuously differentiable near $\beta^*$, with locally bounded derivative envelopes having slightly more than two moments. The expected derivative matrix has full column rank $m$.

The precise exponential-envelope condition appears as Assumption 4 and is a material restriction for heavy-tailed finance applications. Finite variance alone does not establish the existence of exponential moments in a neighborhood of zero. A finite sample always has a computable finite exponential sum for finite multipliers, but that fact does not make the population theorem applicable to the generating process.

Define

$$
D=E\left[\frac{\partial f(x,\beta^*)}{\partial\beta'}\right],\qquad
S=\sum_{j=-\infty}^{\infty}E[f(x_t,\beta^*)f(x_{t+j},\beta^*)'].
$$

The zero-mean condition makes these lag products covariances at truth. Under Assumptions 1–6, Theorem 1 gives consistency in probability. With Assumptions 7–11 and the smoothing conditions, Theorem 2 gives

$$
\sqrt T(\hat\beta_T-\beta^*)\ \Rightarrow\ N(0,V),\qquad
V=(D'S^{-1}D)^{-1}.
$$

Thus the covariance of the estimated parameter is approximately $V/T$. The statement is first-order asymptotic equivalence to efficient GMM, not an exact finite-sample identity or a claim that standard errors need no covariance estimation.

Without smoothing, let $M=E[f_tf_t']$. Corollary 1 instead gives

$$
V_0=(D'M^{-1}D)^{-1}D'M^{-1}SM^{-1}D(D'M^{-1}D)^{-1}.
$$

This becomes the efficient covariance when the moment observations are IID, so $S=M$. Under serial dependence it is the covariance of an inefficiently weighted GMM analogue. The distinction is the reason for the smoothing step.

## Proof mechanism

The appendix, pp. 869–873, supplies the proofs rather than relying only on a local quadratic analogy. For consistency, correct specification makes the population profiled objective attain one at the true parameter, while identified alternatives have smaller values. Compactness and continuity permit a finite covering argument; the exponential envelope controls deviations uniformly in local parameter neighborhoods. Convexity of the exponential function relates the smoothed criterion to unsmoothed averages, with endpoint effects controlled separately. The true-parameter criterion converges to one while alternatives remain separated.

For asymptotic normality, expand the weighted-moment first-order condition around multiplier zero. The curvature estimate

$$
\hat S_T=\frac{L}{T}\sum_t\tilde f_t(\hat\beta_T)\tilde f_t(\hat\beta_T)'
$$

converges to the long-run covariance under the assumptions. The multiplier is of order $L/\sqrt T$, so smoothing changes its convergence rate. Combining the multiplier and parameter first-order conditions gives the asymptotic linear representation

$$
\sqrt T(\hat\beta_T-\beta^*)
=-(D'S^{-1}D)^{-1}D'S^{-1}
\frac1{\sqrt T}\sum_t f_t(\beta^*)+o_p(1).
$$

The central limit theorem for the moment process then yields the efficient covariance. This representation also explains why a method based on a nonlinear entropy objective can share GMM’s first-order behavior: locally, the multiplier translates moment errors through the inverse long-run covariance. Higher-order and finite-sample terms remain different.

## Specification and parameter tests

Because $\gamma=0$ gives $\hat Q_T=1$ and the multiplier minimizes the criterion, the fitted value is at most one and positive when a finite solution exists. Theorem 3 uses the resulting entropy as an overidentification statistic:

$$
\hat\kappa_T=-\frac{2T}{L}\log\hat Q_T(\hat\beta_T,\hat\gamma_T)
\ \Rightarrow\ \chi^2_{r-m}.
$$

The division by $L=2K+1$ is essential. Reusing the IID factor $2T$ with smoothed moments changes the statistic’s scale. Large values reject the maintained moment restrictions under the theorem’s null and regularity conditions. The test is not a probability that the model is true; it also does not identify which moment restriction failed.

For $s$ smooth parameter restrictions $R(\beta^*)=a$, let $\hat\beta_T^c$ be the constrained estimate, and let $A$ be the Jacobian of $R$, assumed full row rank. With consistent estimates of $D,S,V,A$, Theorem 4 supplies three asymptotically equivalent statistics:

$$
W_T=T[R(\hat\beta_T)-a]'[A_TV_TA_T']^{-1}[R(\hat\beta_T)-a],
$$

$$
LM_T=T\bar f_T(\hat\beta_T^c)'S_T^{-1}D_TV_TD_T'S_T^{-1}
\bar f_T(\hat\beta_T^c),
$$

$$
LR_T=\frac{2T}{L}\left\{
\log\hat Q_T(\hat\beta_T,\hat\gamma_T)
-\log\hat Q_T(\hat\beta_T^c,\hat\gamma_T^c)\right\}.
$$

Each converges to $\chi^2_s$ under the parameter null. The unrestricted profiled value is at least as large as the constrained one, so the displayed LR-like statistic has the correct nonnegative sign. It is likelihood-ratio-like because it compares entropy criteria; the paper has not posited a fully parametric likelihood for the observations. The LM expression uses the unsmoothed sample moment vector as written in the source.

## Reimplementation boundary and takeaways

To implement the method, specify the moment functions and their derivatives, parameter domain, observation timing, moment dimension, and missing-data treatment. Choose and report a bandwidth and endpoint convention; compute smoothed moments; solve the inner convex tilt and outer profile problem; recover normalized weights; and verify the weighted moments vanish. For inference, estimate long-run covariance and the expected derivative matrix, then apply the appropriate $T/L$ scaling rather than treating overlapping windows as independent data.

The paper supplies no empirical universe, sample dates, trading rule, transaction costs, bootstrap recipe, optimizer tolerances, numerical seed, or finite-sample rejection table. Those are absent because this is primarily an estimator-and-theory paper. Its concluding section explicitly identifies extensive small-sample simulations and higher-order efficiency as future work. The isolated simulation reference in a footnote cannot support an invented performance table.

The durable result is a way to replace quadratic moment matching with a probability projection while retaining efficient first-order inference for weakly dependent data. The equally important limitation is that the theoretical guarantees depend on identification, smoothness, dependence control, and exponential integrability. In financial applications, checking those assumptions and the finite-sample feasibility of the tilt is part of implementing the paper, not an optional afterthought.

# Asymptotic Distribution of the Markowitz Portfolio

Steven E. Pav, working paper dated December 3, 2013, arXiv:1312.0557v1. Source: [Markowitz_Pav_2013.pdf](../../Finance/Markowitz_Pav_2013.pdf), twelve pages including references. This note concerns the supplied early version. It contains useful structural ideas but also matrix-calculus and parameter-space problems that must be addressed before implementing its printed inference formulas.

## Why this matters and the contribution

The paper packages return means and second moments into one augmented matrix. Its inverse contains both the Markowitz direction $\nu=\Sigma^{-1}\mu$ and the precision matrix $\Sigma^{-1}$. A central limit theorem for sample second moments followed by the delta method can therefore produce joint sampling inference for weights, precision entries, and risk-normalized portfolios. Under Gaussian returns the paper also proposes likelihood-ratio tests for linear restrictions on these quantities, extending covariance-selection ideas.

The intended benefit is inference about an estimated optimizer rather than treating its holdings as known constants. This does not solve mean estimation, certify a superior future portfolio, or establish a high-dimensional limit when the asset count grows with the sample. The paper presents derivations, not an empirical strategy evaluation or simulation study with reported coverage rates.

## Objects, scaling, and the optimization problem

Let $x\in\mathbb R^p$ have mean $\mu$ and positive-definite covariance $\Sigma$. The unscaled Markowitz direction is $\nu=\Sigma^{-1}\mu$, and $q=\mu^\top\Sigma^{-1}\mu=\zeta^2$. For risk budget $R>0$ and $\mu\ne0$, the paper studies

$
\max_{v^\top\Sigma v\leq R^2}
\frac{v^\top\mu-r_0}{\sqrt{v^\top\Sigma v}},\qquad r_0\geq0.
$

Its solution at the risk boundary is $v_R=R\nu/\zeta$, with objective $\zeta-r_0/R$. If $r_0>0$ the scale is pinned to the boundary; if $r_0=0$, all positive scalings along the optimal direction within the budget attain the same ratio. This is the paper's stated objective, with a constant $r_0$ subtracted from total mean. It is not automatically the usual fully invested portfolio Sharpe optimization. A reader using excess asset returns or an explicit risk-free financing account must state that convention consistently.

There is no constraint $\mathbf1^\top v=1$, no short-sale bound, or trading cost in this problem. The risk normalization and budget normalization are distinct. In particular, $\nu/(\mathbf1^\top\nu)$ can be unstable when its denominator approaches zero, and results for the unscaled direction cannot be applied blindly to that ratio.

## Augmented second moments and exact identities

Prepend a constant to returns, $\widetilde x=(1,x^\top)^\top$, and define

$
\Theta=E[\widetilde x\widetilde x^\top]
=\begin{pmatrix}1&\mu^\top\\\mu&\Sigma+\mu\mu^\top\end{pmatrix}.
$

The block inverse is

$
P=\Theta^{-1}
=\begin{pmatrix}1+q&-\nu^\top\\-\nu&\Sigma^{-1}\end{pmatrix}.
$

This is equation (4), and is the paper's central exact identity. The first column below its top element gives minus the Markowitz direction. The upper-left element minus one gives squared optimal signal-to-noise ratio. The lower block gives the precision matrix.

For observations $x_1,\ldots,x_n$, use $\widehat\Theta=n^{-1}\sum_i\widetilde x_i\widetilde x_i^\top$. Its implied covariance is $\widehat\Sigma=n^{-1}\sum_i(x_i-\bar x)(x_i-\bar x)^\top$, using divisor $n$. Substituting an $n-1$ covariance without changing the augmented matrix breaks the exact sample identity, although the difference can be asymptotically negligible at fixed dimension. Invertibility requires sufficient observations and nonsingular sample variation; merely writing an inverse does not handle collinearity.

## General delta-method inference and a needed repair

Let $z_i=\operatorname{vech}(\widetilde x_i\widetilde x_i^\top)$, with lower-triangular entries stacked in a fixed column order. Under iid observations and finite fourth moments, the multivariate CLT yields

$
\sqrt n\{\operatorname{vech}(\widehat\Theta)-\operatorname{vech}(\Theta)\}
\Rightarrow N(0,\Omega),\qquad\Omega=\operatorname{Var}(z_i).
$

The first coordinate of $z_i$ is always one, so its variance and all corresponding covariances are zero. This structural degeneracy is part of the model, not a numerical defect to eliminate by adding arbitrary noise.

For symmetric perturbations, define the elimination matrix $L$ by $\operatorname{vech}(A)=L\operatorname{vec}(A)$ and the duplication matrix $D$ by $\operatorname{vec}(A)=D\operatorname{vech}(A)$. Then $LD=I$, while $L^\top$ is generally not $D$. Matrix inversion gives

$
dP=-P(d\Theta)P,\qquad
J=\frac{\partial\operatorname{vech}(P)}{\partial\operatorname{vech}(\Theta)^\top}
=-L(P\otimes P)D.
$

The correct delta-method covariance, in this column-Jacobian convention, is

$
\sqrt n\{\operatorname{vech}(\widehat P)-\operatorname{vech}(P)\}
\Rightarrow N(0,J\Omega J^\top).
$

These expressions are an explicit reconstruction and correction of the paper's intended argument. Lemma 2.1 prints $L^\top$ in place of $D$, and Theorem 2.2 propagates that derivative. For an off-diagonal coordinate of a symmetric input, both symmetric entries change together; $L^\top$ inserts only one. This can be checked directly by finite differences or by the scalar component identity $\partial P_{ij}/\partial\Theta_{ab}=-(P_{ia}P_{bj}+P_{ib}P_{aj})$ for $a\ne b$.

An implementation should therefore not copy the printed sandwich unchanged. It can avoid explicit duplication matrices altogether by applying the differential $-P(d\Theta)P$ to each symmetric basis perturbation and extracting the chosen lower triangle. This also makes coordinate conventions auditable.

For iid data, estimate $\Omega$ with the sample covariance of the $z_i$. For dependent data, use a consistent long-run covariance estimator of these moment vectors and assume the additional stationarity/dependence conditions required for their CLT. Fourth moments alone do not justify arbitrary serial dependence. The paper points to robust covariance estimators but does not specify a bandwidth, kernel, or finite-sample adjustment.

## Extracting weights, normalization, and error components

Let $S$ select the first-column entries below $P_{00}$, so $\nu=-S\operatorname{vech}(P)$. Its asymptotic covariance is $SJ\Omega J^\top S^\top$. The covariance of the estimated weights themselves is that expression divided by $n$. Confusing the CLT covariance with the finite-sample covariance exaggerates standard errors by a factor $\sqrt n$.

For the risk-normalized vector $v_R=-R b/\sqrt{a-1}$, where $a=P_{00}$ and $b=P_{1:p,0}$, the derivatives are

$
\frac{\partial v_R}{\partial a}=-\frac{v_R}{2\zeta^2},\qquad
\frac{\partial v_R}{\partial b^\top}=-\frac{R}{\zeta}I_p.
$

These derivatives multiply the inverse-moment covariance in a further delta step. Corollary 2.4 prints a common factor $-R$ before a block already containing $v_R$, which introduces an extra $R$ in its first-coordinate derivative. The expressions above follow directly from differentiating the normalized vector and state the repair explicitly. The approximation becomes ill conditioned as $q\to0$, since the direction and its risk normalization then become weakly determined.

The paper motivates separating mean and covariance estimation error. The direct first-order identity is

$
d\nu=\Sigma^{-1}d\mu-\Sigma^{-1}(d\Sigma)\nu.
$

This supports a covariance decomposition into a mean term, a covariance-estimation term, and their cross terms. Under non-Gaussian or dependent observations the cross terms need not vanish. There is no unique scalar fraction of total error until a loss metric or coordinate is specified; summing diagonal variances, measuring risk-weighted error, and measuring one holding answer different questions. The source supplies no empirical percentage demonstrating which component dominates in a particular portfolio.

For Gaussian iid returns, the usual mean/covariance asymptotics provide an independent check on the repaired general method:

$
\operatorname{Avar}\{\sqrt n(\widehat\nu-\nu)\}
=(1+q)\Sigma^{-1}+\nu\nu^\top.
$

This expression is derived here from the differential above, Gaussian mean/covariance independence, and the Wishart covariance of the centered sample covariance. It is not a numerical result reported in the paper. For one asset it becomes $1/\sigma^2+2\mu^2/\sigma^4$, an accessible check for code.

## Gaussian likelihood and the augmented parameter space

For actual Gaussian returns, $|\Theta|=|\Sigma|$ and $\widetilde x^\top P\widetilde x-1=(x-\mu)^\top\Sigma^{-1}(x-\mu)$. Up to constants, the sample negative log likelihood is

$
\ell(\Theta)=\frac n2\left[\log|\Theta|+\operatorname{tr}(\Theta^{-1}\widehat\Theta)\right].
$

The parameter space is positive-definite $\Theta$ with $\Theta_{00}=1$. In precision coordinates the same normalization becomes nonlinear. The augmented observations are not unrestricted $(p+1)$-dimensional Gaussian draws: their first coordinate is deterministic. The paper describes a conditional-Wishart representation, but that does not permit dropping the normalization in Fisher information calculations.

In particular, its Theorem 3.7 gives an inverse-information expression positive definite on all symmetric augmented coordinates. The true free parameter dimension is one smaller because the first moment entry is fixed. The induced covariance of the full inverse-moment vector must respect the corresponding constraint. Together with the elimination/duplication error, this prevents treating the printed Gaussian covariance as a ready-to-use replacement for the general sandwich. The direct Gaussian weight covariance above is a simpler check for the weights alone.

## Linear restrictions and the proposed likelihood-ratio algorithm

The null is $\operatorname{tr}(A_iP)=a_i$ for symmetric $A_i$, $i=1,\ldots,m$. Suitable choices test weight components or precision entries. Scaling of off-diagonal entries must be handled correctly: to select a single symmetric entry by a trace, two symmetric coefficients of one half select that entry once.

The paper proposes the restricted solution

$
\Theta_0=\widehat\Theta-\sum_i\lambda_i A_i,
$

with multipliers chosen to satisfy the restrictions. Define residuals

$
e_i(\lambda)=\operatorname{tr}(A_i\Theta_0^{-1})-a_i.
$

Its Jacobian is $H_{i\ell}=\operatorname{tr}(A_i\Theta_0^{-1}A_\ell\Theta_0^{-1})$, and the proposed Newton update is $\lambda_{k+1}=\lambda_k-H^{-1}e$. At every step $\Theta_0$ must remain positive definite. A damped step or line search is an implementation safeguard, not a convergence guarantee reported in the paper. The source gives no stopping tolerance, initialization algorithm, or simulation coverage study.

The normalization needs explicit checking. If every $A_i$ has zero upper-left entry, as for many restrictions on weights and the lower precision block, the proposed affine $\Theta_0$ preserves $\Theta_{00}=1$. For general $A_i$ it does not automatically do so. A properly constrained Gaussian likelihood then needs the normalization imposed as well. The arbitrary-linear-restriction statement should not be implemented without this check.

For admissible restricted and unrestricted estimates, equation (27) gives

$
LR=n\left[\log|\Theta_0\widehat\Theta^{-1}|+
\operatorname{tr}(\Theta_0^{-1}\widehat\Theta)-(p+1)\right].
$

Under regularity, an interior true parameter, fixed dimension, and $m$ independent restrictions within the actual parameter manifold, the reference is asymptotic $\chi_m^2$. Redundant or infeasible restrictions, boundary singularities, or failed Newton convergence invalidate that simple calibration. Non-Gaussian robust covariance inference does not by itself validate this Gaussian likelihood-ratio reference law.

## Implementation checklist and limits

A reconstruction should form the augmented sample moments with the divisor-$n$ convention, verify the block inverse, estimate the moment covariance, apply symmetric perturbations through the inversion differential, and extract the desired weights. It should compare the resulting Gaussian special case with the independent formula above and finite-difference-check any normalization Jacobian. For likelihood tests, verify positive definiteness, normalization, restriction rank, and final residuals before computing the likelihood difference.

No universe, sample dates, validation windows, transaction costs, or empirical holdings appear in this paper. Asset deletion and shrinkage are suggested applications of estimated uncertainty, not algorithms validated by results here. Multiple testing and post-selection inference would matter if many holdings were screened, but are not developed.

The useful innovation is the augmented-moment representation and delta-method route to joint inference. The supplied version's errors make direct transcription unsafe. Corrected symmetric calculus yields a practical framework under fixed-dimensional CLT assumptions, while weak signals, near-singular covariance, heavy tails without fourth moments, or unconstrained reliance on asymptotic approximations remain important failure modes.

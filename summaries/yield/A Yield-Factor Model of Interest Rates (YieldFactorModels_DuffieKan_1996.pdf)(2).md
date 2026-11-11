# A Yield-Factor Model of Interest Rates

**Authors:** Darrell Duffie and Rui Kan. **Publication:** *Mathematical Finance* 6(4), October 1996, 379–406. **Source:** [YieldFactorModels_DuffieKan_1996.pdf](../../Finance/YieldFactorModels_DuffieKan_1996.pdf). References below use printed pages and source equation numbers; PDF page 1 corresponds to page 379. The full paper, numerical tables, and SDE appendix were inspected. This is a theoretical and numerical-methods paper, not an empirical estimation or investment-performance study.

## Why this matters

Duffie and Kan give a framework in which a few observed fixed-maturity bond yields can be the state variables of an arbitrage-consistent model for the entire yield curve. Yields at other maturities are affine functions of these factors, and zero-coupon prices are exponential-affine. The model allows state-dependent volatility while retaining bond pricing through a small system of ordinary differential equations. More general contingent claims can be priced through a low-dimensional partial differential equation.

The practical attraction is that the factors can be measured from the curve rather than assigned unobservable economic labels. But naming a state variable “the five-year yield” does not make it the model-implied five-year yield. The paper's key consistency restrictions ensure that pricing a five-year bond from the stochastic model actually recovers that state variable. This is a much stronger requirement than estimating a multivariate diffusion for a handful of observed rates.

The main reusable contributions are the affine characterization, the conversion between abstract factors and observed yields, restrictions keeping square-root volatility inside its admissible domain, and an implementable two-factor pricing construction. The numerical examples are illustrations of ODE and PDE methods. Their printed stochastic-volatility parameter values contain internal inconsistencies discussed below; they should not be adopted as an admissible production calibration without checking the restrictions directly.

## Pricing setting and notation

Let $X_t\in D\subset\mathbb R^n$ be a time-homogeneous Markov state. The domain $D$ is open in the basic diffusion analysis. Write $\tau=T-t$ for time to maturity, and $P(t,T)=f(X_t,\tau)$ for the price of a default-free zero-coupon claim paying one unit at $T$. Yields are continuously compounded:

$$
Y(X_t,\tau)=-\frac{\log f(X_t,\tau)}{\tau}.
$$

The short rate is the maturity-zero limit, $r_t=R(X_t)$. Under the selected equivalent martingale measure $Q$,

$$
dX_t=\mu(X_t)\,dt+\sigma(X_t)\,dW_t^Q,
\qquad
f(x,\tau)=E_x^Q\left[\exp\left(-\int_0^\tau R(X_s)\,ds\right)\right].
$$

Equivalence of measures, existence of the state process, integrability, and the regularity needed for the pricing equation remain assumptions. The paper distinguishes the physical-measure drift from $\mu$, which is the risk-neutral drift. The latter prices bonds; it is not automatically a forecast of actual rate changes. The authors explicitly defer econometric estimation and risk-premium identification to other studies.

Let $V(x)=\sigma(x)\sigma(x)'$ denote instantaneous covariance. For a smooth function $h$ define the spatial generator

$$
\mathcal Lh=\mu(x)'\nabla h+\frac12\operatorname{tr}\!\left[V(x)\nabla^2h\right].
$$

The bond equation is $\partial_\tau f=\mathcal L f-Rf$, with $f(x,0)=1$. A claim with payoff $g(X_T)$ has calendar-time price $F$ satisfying $F_t+\mathcal LF-RF=0$ and terminal condition $F(x,T)=g(x)$. These signs matter when translating between maturity-time Riccati integration and backward calendar-time PDE stepping.

## Exponential-affine prices and the Riccati system

The proposed form is

$$
f(x,\tau)=\exp\{A(\tau)+B(\tau)'x\},
\qquad A(0)=0,\quad B(0)=0.
$$

Thus yields are affine, while prices generally are not. Assume

$$
\mu(x)=b+Mx,\qquad
V(x)=V_0+\sum_{i=1}^n x_iV_i,\qquad
R(x)=r_0+r'x.
$$

Here $M$ is a drift matrix, $b$ and $r$ are vectors, and the symmetric matrices $V_i$ define covariance on the admissible state space. The $V_i$ need not individually be covariance matrices; their affine combination must be positive semidefinite wherever the process can move.

Substituting the exponential-affine form into the bond PDE and matching the constant term and each coefficient of $x_i$ gives

$$
A'=b'B+\frac12B'V_0B-r_0,
$$

$$
B_i'=(M'B)_i+\frac12B'V_iB-r_i.
$$

These equations state the source's Riccati construction in explicit matrix notation. In particular, the drift contribution is $M'B$, not $MB$. Once $B$ is integrated, $A$ is obtained by scalar integration. The source uses a plus sign in the exponential, so familiar formulas written as $\exp(A-B'x)$ must have their loadings converted before use.

The matching argument requires the equality to hold on an open state domain. Under the paper's compatibility, uniqueness, and regularity assumptions, affine drift, affine covariance, and an affine short rate yield exponential-affine bond prices when the Riccati solution remains finite. Local ODE existence is not global existence: the right-hand side is locally Lipschitz but quadratic, and finite-time blow-up is possible in general. A numerical implementation must monitor the maturity horizon over which the solution exists and the associated discounted expectation is finite.

The converse has an explicit nondegeneracy condition. Stack the $n$ drift components and $n(n+1)/2$ distinct covariance entries into a vector $H(x)$ of dimension $N=n(n+3)/2$. At each maturity, the pricing equation gives a linear combination of these entries with coefficients determined by $B(\tau)$ and its products. If $N$ maturity choices make the resulting $N\times N$ coefficient matrix nonsingular, solving the system expresses every element of $H$ as an affine function of $x$.

This is the sense in which the paper characterizes affine dynamics as generically necessary. It is not an unconditional claim that observing exponential-affine bond prices identifies every drift and covariance component in a degenerate model. Nor does it say that the diffusion loading $\sigma$ itself is affine: it is the **covariance** $\sigma\sigma'$ that must be affine. Square-root loadings are the central non-Gaussian example.

## Admissible square-root dynamics

The paper studies a representation

$$
dX_t=(MX_t+b)\,dt+C\operatorname{diag}\left(\sqrt{v_1(X_t)},\ldots,\sqrt{v_n(X_t)}\right)dW_t^Q,
$$

$$
v_i(x)=\alpha_i+\beta_i'x,\qquad
D=\{x:v_i(x)>0\text{ for all }i\}.
$$

The constant matrix $C$ is the source's $\Sigma$. Its columns, weighted by the affine variance factors, generate the covariance. A zero $\beta_i$ produces a constant variance factor. If all are zero, the model is Gaussian and may naturally live on all of $\mathbb R^n$.

For stochastic variance factors, square roots are not Lipschitz at zero, and an unconstrained diffusion could leave the region where they are real. Condition A, page 387, gives sufficient restrictions for a unique strong solution remaining strictly inside $D$. For each nontrivial variance boundary, it requires

$$
\beta_i'(Mx+b)>\frac12\beta_i'CC'\beta_i
\quad\text{when }v_i(x)=0,
$$

and, for every Brownian component $j$ with $(\beta_i'C)_j\ne0$, it requires $v_j=v_i$. Proportional positive variance factors can be absorbed into $C$ so that equality is obtained. Constant positive variance factors have no zero boundary to test.

The second restriction is crucial. At a point where $v_i=0$, noise from an unrelated still-positive variance factor must not push $v_i$ negative. The first restriction makes the inward drift strong enough to avoid hitting the zero boundary under the paper's strict inequality. It is substantially stronger than merely starting with positive variances. The result should be used as the sufficient theorem stated, not as a claim that every admissible affine process must satisfy a strict inequality in all boundary cases.

The proof in the appendix proceeds by stopping the process at successively smaller positive variance levels. Away from zero, ordinary Lipschitz existence and uniqueness apply. A one-dimensional square-root comparison process has sufficiently strong positive drift to remain strictly positive. A comparison lemma adapted to a Yamada-type modulus of continuity bounds the true variance process below by that positive process. Consequently the limiting boundary-hitting time is infinite. With several variance factors, the noise-alignment part of Condition A permits the same comparison separately for each one.

The appendix also motivates the constant-matrix square-root representation. It works with a canonical state space defined by the affine diagonal covariance inequalities, independent boundary normals, and covariance positive definite at an interior point. Positive semidefiniteness forces a covariance row to vanish where its diagonal variance vanishes. Under those assumptions, the affine covariance can be organized into blocks and diagonalized by a constant congruence transformation. This yields $V(x)=C\operatorname{diag}(v_i(x))C'$. The domain and nondegeneracy assumptions are part of the result; the argument should not be extrapolated without qualification to every affine covariance on an arbitrary curved or restricted state space.

Strict positivity of variance is different from positivity of every yield. One may choose a nonnegative combination of the positive $v_i$ as the short-rate function, but an arbitrary affine $R$ need not be positive. The later numerical examples allow negative rate states, a fact relevant to boundary behavior of discounted claims.

## Making the factors actual yields

Suppose component $X_i$ is intended to equal the zero-coupon yield at fixed remaining maturity $\tau_i>0$. The required identities are

$$
A(\tau_i)=0,\qquad B(\tau_i)=-\tau_i e_i.
$$

They enforce $-\log f(x,\tau_i)/\tau_i=x_i$ for every admissible state. These are maturity boundary restrictions in addition to $A(0)=B(0)=0$. One cannot freely choose all drift and covariance parameters and assume these identities will follow.

There are two construction routes. The indirect route begins with an admissible abstract affine model, solves its bond loadings, and chooses maturities with linearly independent loading rows. Define

$$
K_{ij}=-\frac{B_j(\tau_i)}{\tau_i},\qquad
k_i=\frac{A(\tau_i)}{\tau_i},\qquad
Y=KX-k.
$$

If $K$ is nonsingular, then $X=K^{-1}(Y+k)$ and

$$
\mu_Y(y)=K\mu\!\left(K^{-1}(y+k)\right),\qquad
\sigma_Y(y)=K\sigma\!\left(K^{-1}(y+k)\right).
$$

The new price loadings are $A_Y(\tau)=A(\tau)+B(\tau)'K^{-1}k$ and $B_Y(\tau)'=B(\tau)'K^{-1}$. This transforms the entire domain as well as the dynamics; it is not merely a relabeling of observations. Near-singularity of $K$ would amplify measurement errors even when exact invertibility holds.

The direct route declares the factors to be yields at the outset, fixes some covariance parameters from calibration or estimation, and solves for drift parameters satisfying the maturity identities and admissibility conditions simultaneously. The authors report practical success in two-factor cases but do not prove that arbitrary preselected covariance parameters admit such a drift solution. Counting equations and unknowns motivates a numerical search; it does not guarantee existence, uniqueness, or a well-conditioned calibration.

A finite-factor model spans a restricted family of yield curves. Unlike an unrestricted initial-curve HJM specification, it cannot generally match every observed initial curve exactly with fixed parameters. Time-dependent calibration can expand the fit, but changes the model and introduces further assumptions. The paper also notes that using the instantaneous short rate as a factor is convenient algebraically but problematic empirically because the exact maturity-zero rate is not directly observed.

## Two factors with a common stochastic variance

For the worked model, index factors by $0$ and $1$, take $R(x)=x_0$, and let

$$
v(x)=\alpha+\beta_0x_0+\beta_1x_1,\qquad
V(x)=v(x)G,\qquad G=CC'.
$$

Both coordinates share one variance scalar. Instantaneous correlation is therefore the constant $G_{01}/\sqrt{G_{00}G_{11}}$, though conditional volatilities change with the state. Write $M=(a_{ij})$ and $b=(b_0,b_1)'$. The bond ODEs are

$$
q(B)=G_{00}B_0^2+2G_{01}B_0B_1+G_{11}B_1^2,
$$

$$
B_0'=a_{00}B_0+a_{10}B_1+\frac{\beta_0}{2}q(B)-1,
$$

$$
B_1'=a_{01}B_0+a_{11}B_1+\frac{\beta_1}{2}q(B),
\qquad
A'=b_0B_0+b_1B_1+\frac{\alpha}{2}q(B).
$$

All three start at zero. For the positive-maturity factor $X_1$, require $B_0(\tau_1)=0$, $B_1(\tau_1)=-\tau_1$, and $A(\tau_1)=0$. The short-rate identity follows from the derivative at maturity zero.

Normalize $\beta_1=1$ when nonzero. On the zero-variance line $x_1=-\alpha-\beta_0x_0$, the variance drift becomes $k_0+k_1x_0$, where

$$
k_0=\beta_0b_0-\alpha\beta_0a_{01}+b_1-\alpha a_{11},
$$

$$
k_1=\beta_0a_{00}-\beta_0^2a_{01}+a_{10}-\beta_0a_{11}.
$$

The paper prints $k_0>0$ and $k_1=0$ in Equation (7.2). The zero slope is needed for a uniformly inward drift along the entire unbounded line. For the **strict interior theorem of Section 4**, the earlier stronger condition is $k_0>\beta'G\beta/2$, not merely $k_0>0$. This distinction is obtained directly by substituting the common-variance model into Condition A.

When variance is constant, the Riccati system for $B$ is linear: $B'=M'B-e_0$, hence $B(\tau)=-\int_0^\tau e^{M's}e_0\,ds$. This integral form remains useful when $M$ is singular or has repeated eigenvalues, unlike an eigenvalue formula requiring distinct roots. The two eigenvalues printed in the paper are $(a_{00}+a_{11}\pm\sqrt{(a_{00}-a_{11})^2+4a_{01}a_{10}})/2$. Integrating $A$ then completes the Gaussian bond model.

## Calibration algorithm and the printed stochastic example

Section 9 integrates the two $B$ equations with fourth-order Runge–Kutta. It fixes covariance coefficients and uses Newton–Raphson to adjust drift coefficients until both yield-loading residuals have absolute value below $10^{-4}$. The authors recommend initializing the nonlinear solve with a solution of the deterministic-volatility model. They subsequently integrate $A$ and adjust drift constants so that $A(\tau_1)=0$.

The example has $\tau_1=1$, as confirmed by the one-unit bond whose exact price is $e^{-x_1}$. The fixed inputs are $b_0=-0.1$, $a_{01}=0.76$, $G_{00}=G_{11}=0.9$, $G_{01}=0.7$, $\alpha=0.05$, $\beta_0=-1.08$, and $\beta_1=1$. The implied instantaneous correlation is $0.7/0.9\approx0.7778$. These are illustrative parameters, not estimated market quantities, and the time unit is the model's chosen unit.

Table 9.1 reports:

| ODE grid size | $a_{00}$ | $a_{11}$ | $a_{10}$ | $b_1$ |
|---|---:|---:|---:|---:|
| 10,001 | −0.6419 | 3.7377 | −3.900 | 0.1278 |
| 20,001 | −0.6418 | 3.7374 | −3.900 | 0.1278 |

The source describes grid size as the reciprocal of the ODE step size. It does not supply the original code, full-precision solutions, numerical Jacobian details, or a Newton damping rule. Rounded parameter values can leave slightly larger residuals than the original stopping tolerance.

There is also a more substantive inconsistency. Direct substitution of the second printed row gives $k_0\approx0.08997$, $k_1\approx-0.056928$, and $\beta'G\beta/2=0.21888$. Thus the row does not satisfy $k_1=0$ or the strict boundary-drift inequality, despite the text's statement that the resulting parameters satisfy Condition A. With the other printed coefficients fixed, $k_1=0$ would require $a_{10}\approx-3.843072$, which is not explained by rounding −3.900 to three decimals. Changing that coefficient alone would change the bond-loadings solution and would not repair the full calibration.

As a separate arithmetic check for this note, a 10,000-step RK4 integration using the rounded second-row coefficients produced $B_0(1)\approx0.0001434$, $B_1(1)\approx-1.0001889$, and $A(1)\approx8.77\times10^{-6}$. These nearly satisfy the yield identities, supporting the interpretation that the printed row describes the intended bond-loading example, but they do not cure its admissibility problem. The note's calculations are checks of the published inputs, not new empirical results or a claim to have reproduced the original program.

A usable reconstruction should solve the pricing and boundary restrictions jointly and report all residuals, rather than accept Table 9.1 as globally admissible. The paper supplies the framework for that exercise but does not provide a corrected parameter set.

## Derivative PDE and coordinate transformation

For a European claim, solve $F_t+\mathcal LF-x_0F=0$ with its terminal payoff. A call on a bond with maturity $T_b$ and exercise date $T_e<T_b$ has payoff $\max\{f(x,T_b-T_e)-K,0\}$. American exercise requires an obstacle or equivalent exercise treatment throughout the allowable interval; the European terminal-value PDE alone is insufficient.

For common stochastic variance, Sections 8–9 transform the unbounded state domain to bounded coordinates while eliminating the mixed second derivative. Define

$$
\theta_0=\beta_1G_{11}+\beta_0G_{01},\qquad
\theta_1=\beta_0G_{00}+\beta_1G_{01},
$$

$$
y=\frac{1}{1+k\sqrt{v(x)}},\qquad
z=\arctan\{h(\theta_1x_1-\theta_0x_0)\},
$$

with positive grid-concentration parameters $h,k$. Then $0<y<1$ and $-\pi/2<z<\pi/2$. Set $v=(1-y)^2/(k^2y^2)$, $w=\tan(z)/h$, and $d=\beta_0\theta_1+\beta_1\theta_0=\beta'G\beta$. When $d>0$, the inverse map is

$$
x_0=\frac{\theta_1(v-\alpha)-\beta_1w}{d},\qquad
x_1=\frac{\theta_0(v-\alpha)+\beta_0w}{d}.
$$

If $d=0$, this transformation is singular and another coordinate choice is needed. The source's transformation is not a universal mapping for every parameter degeneration.

For implementation, the transformed coefficients can be calculated directly from Itô's formula rather than transcribing the long expanded expressions on page 393. With $u_1(x)=y$ and $u_2(x)=z$, define

$$
\widetilde\mu_i=\nabla u_i'\mu+\frac12\operatorname{tr}\{V\nabla^2u_i\},\qquad
\widetilde V_{ij}=\nabla u_i'V\nabla u_j.
$$

Then solve the ordinary transformed generator equation using these coefficients and the inverse map. Here $\widetilde V_{12}=0$: the gradients of $v$ and $w$ satisfy $\beta'G(-\theta_0,\theta_1)'=0$. This orthogonality is the reason alternating-direction implicit finite differences become convenient. The source multiplies its expanded PDE by a coordinate-dependent factor to clear denominators; the unmultiplied generator above is an equivalent interior formulation and makes the factors of one-half explicit.

The mapping concentrates original-rate grid points according to $h$ and $k$. Bounded coordinates do not eliminate numerical boundary problems: they move infinite rates and the variance boundary to finite coordinate edges. The authors observe divergence near some edges and truncate the domain to $y\in[\delta_1,1-\delta_2]$, $z\in[-\pi/2+\delta_3,\pi/2-\delta_4]$. The truncation changes the numerical problem and requires suitable boundary conditions.

The paper names ADI and reports grids but does not fully specify the splitting scheme, time-step schedule, boundary-value approximation, interpolation between nodes, or American exercise algorithm. These are necessary for exact reproduction. A new solver should document them and test both spatial and temporal refinement as well as boundary sensitivity; the three published spatial grids alone are not a convergence theorem.

## Numerical pricing results

The stochastic example uses $h=k=12.5$, $\delta_1=0.01$, $\delta_2=\delta_3=0$, and $\delta_4=0.01$. Table 9.2 reports one-unit zero-coupon prices and an American call with exercise maturity 0.5, bond maturity 1, and strike 0.9:

| $(x_0,x_1)$ | Bond, grid 111 | Bond, grid 221 | Bond, grid 331 | Exact bond $e^{-x_1}$ | American call, grids 111 / 221 / 331 |
|---|---:|---:|---:|---:|---|
| (0.1070, 0.1584) | 0.8464 | 0.8531 | 0.8532 | 0.8535 | 0.0578 / 0.0610 / 0.0606 |
| (0.0336, 0.0791) | 0.9179 | 0.9251 | 0.9246 | 0.9240 | 0.0888 / 0.0926 / 0.0922 |
| (0.0710, 0.0593) | 0.9411 | 0.9420 | 0.9421 | 0.9424 | 0.0879 / 0.0886 / 0.0883 |

At grid 331, displayed bond errors are −0.0003, +0.0006, and −0.0003 per unit principal. The option column has no exact benchmark; apparent stabilization is weaker evidence than an independently known option value. These numerical observations do not establish global admissibility of the printed diffusion parameters.

The constant-volatility example provides a stronger pricing benchmark because European bond calls have a closed form. Let $P_b=f(x,T_b-t)$, $P_e=f(x,T_e-t)$ and

$$
s^2=\int_t^{T_e}\Delta B(u)'G\Delta B(u)\,du,
\qquad
\Delta B(u)=B(T_b-u)-B(T_e-u).
$$

Then

$$
C=P_b\Phi(d_1)-KP_e\Phi(d_2),\qquad
d_1=\frac{\log(P_b/(KP_e))}{s}+\frac{s}{2},\quad d_2=d_1-s.
$$

This is a forward-bond lognormal formula under Gaussian factor dynamics with deterministic integrated relative-bond volatility. For $s=0$, use its deterministic limit. It does not imply that the same formula applies unchanged to stochastic-volatility or American options.

Section 10 uses $\alpha=1$, $\beta=0$, $b_0=-0.1$, $b_1=0.6453$, $a_{00}=-0.9651$, $a_{01}=0.59$, $a_{10}=-3.21$, $a_{11}=3.5802$, $G_{00}=G_{11}=1$, and $G_{01}=0.6$. Its coordinates are $y=\arctan(kx_0)$ and $z=\arctan[h(G_{00}x_1-G_{01}x_0)]$, again orthogonalizing the diffusion. It takes $h=k=12.5$, $\delta_1=\delta_3=0.01$, $\delta_2=\delta_4=0$, bond maturity 1, option maturity 0.5, and strike 0.9.

For states (0.1106, 0.1751), (0.05849, 0.03509), and (0.02635, 0.07344), exact European call prices are 0.1065, 0.1679, and 0.1421. Grid-331 values are 0.1065, 0.1681, and 0.1424. Corresponding exact bond prices are 0.8394, 0.9655, and 0.9292, versus grid-331 values 0.8403, 0.9668, and 0.9309. Coarse-grid bond values include 1.0001 in the second state, compared with exact 0.9655, illustrating meaningful discretization error. Refinement improves the example overall but not monotonically at every entry.

## Jump extension

Section 11 adds jumps with affine nonnegative intensity $\lambda(x)=\lambda_0+\ell'x$ and a fixed jump-size distribution $\nu$. The generator adds $\lambda(x)\int[h(x+z)-h(x)]\nu(dz)$. With $M_\nu(B)=\int e^{B'z}\nu(dz)$ finite at the needed loadings, the exponential-affine ansatz remains compatible: add $\lambda_0[M_\nu(B)-1]$ to $A'$ and $\ell_i[M_\nu(B)-1]$ to $B_i'$.

These formulas follow by substituting the ansatz into the displayed jump generator. The jump additions need not be quadratic, so the resulting generalized ODEs need not be ordinary quadratic Riccati equations. Convenient transforms include fixed jumps, Gaussian jumps on an unrestricted Gaussian state space, and positive exponential jumps in suitable square-root domains. A jump law must preserve the state space from every admissible starting state; an arbitrary Gaussian jump law is unsuitable for a constrained positive-variance half-space.

The derivative equation becomes an integro-differential equation. Its nonlocal jump term changes the implicit linear system, so ordinary nearest-neighbor tridiagonal ADI machinery cannot simply be reused unchanged. Jumps can also create incomplete markets: a finite collection of bond positions may not span every jump payoff. The paper prices under a selected martingale measure and does not supply a unique empirical jump-risk premium or a universal replication strategy.

## Reimplementation priorities and interpretation

A reimplementation should begin with the state domain and covariance restrictions, then solve the Riccati system and verify that the intended basis yields reproduce themselves. Only after those checks should it price other maturities or contingent claims. For the direct two-factor route, report maturity residuals, boundary-drift residuals, and full-precision parameters together. A small pricing residual is not evidence that a square-root SDE remains admissible globally.

For derivatives, the Gaussian option formula provides a meaningful independent check of the numerical solver. Separately vary time steps, spatial grids, and truncation boundaries; implement American exercise explicitly when required. Distinguish parameters under $Q$ from physical dynamics, and do not interpret the paper's illustrative prices as estimated market fit or profitable trading opportunities.

The framework's enduring insight is that observable yield factors, no-arbitrage pricing, stochastic volatility, and numerical tractability can coexist, provided their consistency restrictions are enforced. The mathematical construction supplies a model family and a path to implementation. It does not remove the empirical choice of factor maturities, guarantee exact fitting of arbitrary curves, or justify overlooking printed calibration inconsistencies.

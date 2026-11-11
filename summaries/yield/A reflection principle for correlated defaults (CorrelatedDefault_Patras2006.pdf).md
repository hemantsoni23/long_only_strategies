# A reflection principle for correlated defaults

Frédéric Patras. *Stochastic Processes and their Applications* 116 (2006), 690–698. DOI: 10.1016/j.spa.2005.11.005. Received 3 February 2005, revised 20 May 2005, accepted 10 November 2005; available online 7 December 2005. Source: [original PDF](../../Finance/CorrelatedDefault_Patras2006.pdf). These notes cover all nine PDF pages, including the proofs, geometric figure, financial application, and references. Journal pages equal PDF pages plus 689.

## Why this matters

The paper develops a geometric reflection principle for two correlated Brownian default drivers. In a one-name structural model, reflecting Brownian paths across a barrier yields an explicit first-passage probability. With two names, decorrelation turns two barriers into the sides of a wedge. A naive single reflection no longer accounts correctly for paths interacting with both boundaries. Patras constructs a Brownian-like process on a cone with the appropriate angular period, uses a reflection on that space, and obtains the killed transition density in the wedge.

The wedge density itself has predecessors in analytic heat-equation and correlated-barrier work, notably He, Keirstead, and Rebholz and Zhou, which the paper cites. Its contribution is the probabilistic and geometric construction, with a relatively direct drift adjustment and an application to maturity-settled digital default payoffs. It is not a new empirical correlation estimator or a general calibrated basket model.

This matters because joint default is a path event. A bivariate distribution of asset values at maturity does not tell us whether either firm crossed its default barrier earlier and subsequently recovered. The wedge solution preserves continuous monitoring, correlated first passages, and nonzero drifts. It can serve as an analytic benchmark for numerical solvers or Monte Carlo engines used for two-name credit and barrier derivatives.

The phrase “closed formula” requires care. The final price contains an infinite Bessel-function series and a two-dimensional integral over a wedge. It removes simulation and the need to solve a PDE for each parameter set, but a numerical implementation still needs reliable special functions, quadrature, truncation control, and limiting-case tests. The article reports no runtimes, pricing-error tolerances, numerical tables, calibrated issuer pair, or realized investment performance.

## Geometric setup and the new process

Start with a standard planar Brownian motion $X^x_t$ from $x\ne0$. The survival region is a wedge

$$
D=\{(x_1,x_2):x_2\ge0,\ \cos(2\alpha)x_1+\sin(2\alpha)x_2\ge0\},
\qquad -\frac\pi4<\alpha<\frac\pi4.
$$

Its opening angle is $\beta=\pi/2+2\alpha$, so $0<\beta<\pi$. In polar coordinates the interior is $\rho>0$ and $0<\theta<\beta$. Write $\tau$ for the first boundary hit. The desired transition law is the law of $X_t$ restricted to paths that remain inside $D$ until time $t$.

The construction uses the skew-product representation of planar Brownian motion:

$$
X_1(t)+iX_2(t)=R_t\exp\{i(\theta_0+\Gamma_{C_t})\},
\qquad C_t=\int_0^t R_s^{-2}\,ds.
$$

Here $R$ is the radial Bessel process and $\Gamma$ is an independent one-dimensional Brownian motion. The angle is an unwrapped winding angle. Brownian paths starting away from the origin almost surely do not hit the origin, which permits the lift to the covering space $(0,\infty)\times\mathbb R$.

Project the winding angle modulo $2\beta$, rather than modulo $2\pi$. This gives a process $X_\alpha$ on $(0,\infty)\times\mathbb R/(2\beta\mathbb Z)$. Locally it has Brownian geometry, but globally the angular period is different. Proposition 1 says that its distribution is determined by the starting radius, starting angle, and $\alpha$.

One can map this cone to the ordinary punctured plane by multiplying the angle by $\pi/\beta$. The transformed process is $Y_\alpha$. This map is not a local isometry. It simplifies the barrier geometry but does not make $Y_\alpha$ an ordinary planar Brownian motion. Retaining that distinction is essential: using a Gaussian planar transition density after rescaling the angle would lose the very geometry the construction is designed to preserve.

Figure 1 on journal p. 694 shows the original wedge and the rescaled upper-half-plane picture. The two absorbing sides become one straight boundary in the rescaled angular representation. Reflection across that line is then compatible with the cone process. The proof uses the symmetry of the angular process and the strong Markov property, rather than assuming a finite collection of ordinary planar images works for every wedge angle.

A minor source typo on journal p. 692 describes $\mathbb R_+$ as strictly positive integers. The radial coordinate and all subsequent integrals require strictly positive real numbers. The interpretation here follows those equations. This is a local mathematical reading, not an official erratum.

## Transition density before and after absorption

Let the starting polar point be $(\rho,\theta)$ and the terminal point $(\mu,\kappa)$. The generator in terminal coordinates is

$$
\mathcal L=\frac12\left(\partial_{\mu\mu}+\frac1\mu\partial_\mu+\frac1{\mu^2}\partial_{\kappa\kappa}\right).
$$

The heat kernel is periodic in $\kappa$ with period $2\beta$. Separation of variables yields angular modes $\cos(n\pi(\kappa-\theta)/\beta)$ and radial Bessel functions $J_{n\pi/\beta}$. The order is usually noninteger. Orthogonality fixes the normalization, including half weight on the zeroth angular mode. Theorem 2 gives

$$
f_\alpha((\rho,\theta),(\mu,\kappa),t)
=\frac1\beta\int_0^\infty \lambda e^{-\lambda^2t/2}
\left[\frac12J_0(\lambda\mu)J_0(\lambda\rho)
+\sum_{n=1}^\infty J_{n\pi/\beta}(\lambda\mu)J_{n\pi/\beta}(\lambda\rho)
\cos\left(\frac{n\pi(\kappa-\theta)}\beta\right)\right]d\lambda.
$$

The density is relative to the natural area element $\mu\,d\mu\,d\kappa$, not plain $d\mu\,d\kappa$. The initial condition is correspondingly $\rho^{-1}\delta(\rho-\mu)\delta(\theta-\kappa)$. Missing the Jacobian produces an incorrectly normalized survival probability even if every Bessel coefficient is correct.

The paper checks the ordinary-plane limit $\beta=\pi$ using Neumann's Bessel expansion and Weber's first integral. In that limit, the cone kernel reduces to the familiar Gaussian heat kernel at distance $R$, $e^{-R^2/(2t)}/(2\pi t)$. This is a normalization check on the unconstrained process, not an assertion that correlation one can be inserted into the later nonsingular whitening transform.

The generalized reflection principle, Theorem 3, permits subtracting the reflected cone density to remove paths that have crossed the boundary. The cosine difference becomes a product of sine functions, the zeroth mode cancels, and Proposition 4 produces

$$
f_D((\rho,\theta),(\mu,\kappa),t)
=\frac2\beta\int_0^\infty\lambda e^{-\lambda^2t/2}
\sum_{n=1}^\infty J_{n\pi/\beta}(\lambda\rho)J_{n\pi/\beta}(\lambda\mu)
\sin\left(\frac{n\pi\theta}\beta\right)
\sin\left(\frac{n\pi\kappa}\beta\right)d\lambda.
$$

Weber's second exponential integral evaluates the radial spectral integral. The equivalent kernel most convenient for pricing is

$$
f_D((\rho,\theta),(\mu,\kappa),t)
=\frac{2}{\beta t}e^{-(\rho^2+\mu^2)/(2t)}
\sum_{n=1}^\infty I_{n\pi/\beta}\!\left(\frac{\rho\mu}{t}\right)
\sin\left(\frac{n\pi\theta}\beta\right)
\sin\left(\frac{n\pi\kappa}\beta\right),
\quad 0<\theta,\kappa<\beta.
$$

$J_\nu$ is the ordinary Bessel function of the first kind and $I_\nu$ its modified counterpart. They are not interchangeable. The sine factors impose zero density on either absorbing side. Integrating $f_D\mu\,d\mu\,d\kappa$ over the wedge gives the probability of no boundary hit; the missing mass is the probability of at least one hit. Although individual series terms can be negative through the sine factors, the exact summed kernel is nonnegative.

The source derives the kernel constructively rather than postulating it. For reimplementation, the important chain is angular period $2\beta$, modes of order $n\pi/\beta$, odd reflection, and polar area measure. Losing any one of these factors changes the price.

## Structural credit model and whitening

For firm $i=1,2$, risk-neutral asset value follows

$$
\frac{dV_i(t)}{V_i(t)}=(r-k_i)dt+\sigma_i\,dB_i(t),
\qquad d\langle B_1,B_2\rangle_t=\varrho\,dt.
$$

The short rate $r$, payout rate $k_i$, volatility $\sigma_i>0$, correlation $\varrho\in(-1,1)$, barrier scale $K_i>0$, and barrier growth $\gamma_i$ are constant. Default occurs on first passage below $v_i(t)=K_ie^{\gamma_it}$. Initial firms are assumed alive, $V_i(0)>K_i$. The log distance above the moving barrier is

$$
Y_i(t)=\log\frac{V_i(t)}{K_ie^{\gamma_it}}
=y_i^0+\nu_it+\sigma_iB_i(t),
\quad y_i^0=\log\frac{V_i(0)}{K_i},
\quad \nu_i=r-k_i-\gamma_i-\frac12\sigma_i^2.
$$

Default is the first hit of $Y_i=0$. The source introduces a sign-reversed process $W_i=y_i^0-Y_i$; these notes use $Y_i$ directly to make the survival inequalities transparent.

Whiten the covariance by setting

$$
Z_1(t)=\frac{Y_1(t)/\sigma_1-\varrho Y_2(t)/\sigma_2}{\sqrt{1-\varrho^2}},
\qquad Z_2(t)=\frac{Y_2(t)}{\sigma_2}.
$$

Then $dZ=\phi\,dt+dX$, where $X$ is standard planar Brownian motion and

$$
\phi_1=\frac{\nu_1/\sigma_1-\varrho\nu_2/\sigma_2}{\sqrt{1-\varrho^2}},
\qquad\phi_2=\frac{\nu_2}{\sigma_2}.
$$

The survival inequalities become $Z_2>0$ and $\sqrt{1-\varrho^2}Z_1+\varrho Z_2>0$. Thus

$$
\beta=\frac\pi2+\arcsin\varrho=\arccos(-\varrho).
$$

Positive correlation opens the wedge and negative correlation narrows it. Define $z_0=(Z_1(0),Z_2(0))=\rho(\cos\theta,\sin\theta)$. Compute $\theta$ with a two-argument arctangent: $Z_1(0)$ may be negative even when both firms are initially alive. A one-argument arctangent can assign the starting point to the wrong part of the wedge.

The original PDF's equation for $dW_i$ on journal p. 697 writes a drift term $-\nu_i t$ instead of $-\nu_i\,dt$. The latter is required by the preceding definition and the immediately following drifted Brownian equation. This notation issue does not change the intended model.

## Drift adjustment and digital price

The paper uses a change of measure to remove the constant drift from $Z$, applies the driftless wedge kernel, and transforms back. In these notes $P$ denotes the financial risk-neutral measure used in the paper's application and $Q$ an auxiliary driftless measure. Confusing that auxiliary measure with the pricing measure would remove the drift adjustment incorrectly.

For a terminal point $z=(\mu\cos\kappa,\mu\sin\kappa)$, the killed density under $P$ equals the driftless killed density times

$$
\exp\left[\phi\cdot(z-z_0)-\frac12\|\phi\|^2T\right].
$$

Consequently the joint survival probability is

$$
q_{12}(T)=P(\tau_1>T,\tau_2>T)
=\int_0^\infty\int_0^\beta
\exp\left[\phi\cdot(z-z_0)-\frac12\|\phi\|^2T\right]
f_D((\rho,\theta),(\mu,\kappa),T)\,\mu\,d\kappa\,d\mu.
$$

This compact expression contains the full integral in Theorem 5. It also separates the components to test: covariance whitening, wedge survival without drift, and exponential tilting. The exponent is a Cartesian dot product even though quadrature uses polar coordinates:

$$
\phi\cdot(z-z_0)=\phi_1[\mu\cos\kappa-\rho\cos\theta]
+\phi_2[\mu\sin\kappa-\rho\sin\theta].
$$

The single-name first-passage probability is the usual Brownian-barrier formula,

$$
p_i(T)=\Phi\!\left(\frac{-y_i^0-\nu_iT}{\sigma_i\sqrt T}\right)
+e^{-2\nu_iy_i^0/\sigma_i^2}
\Phi\!\left(\frac{-y_i^0+\nu_iT}{\sigma_i\sqrt T}\right).
$$

This differs from the terminal probability $P(Y_i(T)\le0)$ by the reflected-path term. The factor multiplying the second Gaussian CDF can be large for negative drift; stable log-domain evaluation may be needed when computing very small probabilities.

The contract pays $A$ at maturity $T$ if exactly one name has defaulted by then, $B$ if both have defaulted, and zero if neither has defaulted. It is a contingent terminal payment, with no premium-leg schedule in this paper. Let $u=1-q_{12}$ be the probability of at least one default and $b=p_1+p_2-u$ the probability of both. Its price is

$$
S=e^{-rT}\left[A(p_1+p_2-2b)+Bb\right]
=e^{-rT}\left[(B-A)(p_1+p_2)+(2A-B)(1-q_{12})\right].
$$

This is Theorem 5 expressed through reusable marginal and survival components. The replication in the source is two single-name digitals paying $B-A$, plus a first-to-default digital paying $2A-B$. The coefficients can be negative; this is an algebraic replication, not a claim that each component is a nonnegative standalone long position.

When $A=0$, only two defaults trigger payment and $S=Be^{-rT}b$. When $A=B$, either one or two defaults triggers the same payment and $S=Ae^{-rT}u$. When $B=2A$, the payoff is additive in individual defaults and the joint term vanishes. That final case is a particularly strong software check: the price must become independent of correlation even though the underlying joint survival probability changes.

A contract paying at the instant of the first or second default has a different discounting problem. Likewise a CDS with running premiums, accrued premium at default, recovery-based protection, or counterparty risk needs additional legs. The paper does not price those contractual features merely by calling the illustrated payoff a swap.

## Numerical implementation and validation

No empirical experiment or numerical price example appears in the paper. The only figure depicts the geometry. There is no named issuer universe, calendar sample, estimation window, spread curve, recovery series, calibration objective, or comparison against market quotes. An implementation can reproduce the mathematics from the stated assumptions, but there is no published numeric result to match within an error tolerance.

A reproducible solver would accept $(V_i(0),K_i,\gamma_i,k_i,\sigma_i)_{i=1,2}$ together with $r,\varrho,T,A,B$. Before invoking special functions, check $T>0$, positive volatilities and barriers, both initial distances positive, and $|\varrho|<1$. An initially defaulted name should be treated separately. Compute $\nu_i$, the whitening transform, $(\rho,\theta)$, and $\beta$, then evaluate the marginals and the integral for $q_{12}$. Convert the results into probabilities of zero, one, and two defaults before assembling the cash payoff.

For the kernel, sum orders $\eta_n=n\pi/\beta$. Modified Bessel functions grow exponentially in their argument $x=\rho\mu/T$. A useful derived rewrite uses the exponentially scaled function $\widetilde I_\eta(x)=e^{-x}I_\eta(x)$:

$$
e^{-(\rho^2+\mu^2)/(2T)}I_\eta(\rho\mu/T)
=e^{-(\rho-\mu)^2/(2T)}\widetilde I_\eta(\rho\mu/T).
$$

This removes the largest cancellation between Bessel growth and the Gaussian factor. It is an implementation recommendation derived from the formula; it is not an algorithm benchmarked in the article. The drift exponential must still be combined carefully with the radial Gaussian to avoid overflow at large $\mu$ or extreme drifts.

Integrate angle over $(0,\beta)$ and radius over $(0,\infty)$ using adaptive quadrature or a finite radial truncation with an explicit tail check. Repeat with more angular modes, a larger radial cutoff, and tighter integration tolerances until the price and probability identities stabilize. A single small last term is not a universal truncation certificate because the sine series can oscillate and cancellation can be material. Extremely narrow wedges, very small maturities, and starting points close to a boundary are useful stress cases for numerical convergence.

For zero correlation the two original log-distance processes are independent, giving the exact check

$$
q_{12}(T)=[1-p_1(T)][1-p_2(T)],\qquad b(T)=p_1(T)p_2(T).
$$

At zero log drift, $p_i(T)=2\Phi[-y_i^0/(\sigma_i\sqrt T)]$. As an analyst-derived test case, take $y_1^0=y_2^0=0.2$, $\sigma_1=\sigma_2=0.2$, $T=1$, $\nu_1=\nu_2=0$, and $\varrho=0$. Each default probability is approximately 0.3173105; the joint-default probability is approximately 0.10068596, and the probability of at least one default is approximately 0.53393506. With $r=0$ and unit digital payoff these are the second- and first-to-default terminal prices. These numbers are consequences of the independent limit, not results reported by Patras.

Probability constraints provide further checks. Joint survival must lie between $\max(0,1-p_1-p_2)$ and $\min(1-p_1,1-p_2)$. The derived joint-default probability must lie between $\max(0,p_1+p_2-1)$ and $\min(p_1,p_2)$. The probabilities of zero, exactly one, and two defaults must sum to one. Violations larger than numerical tolerance often point to a missing polar Jacobian, a wrong angle, an incorrect sign in the drift tilt, or inadequate series convergence.

Monte Carlo can provide an independent implementation check, but coarse time-grid simulation underestimates continuous barrier crossings. A comparison must either control the time-discretization bias or use an appropriate bridge-based crossing procedure. The paper supplies the continuous-monitoring analytic target; it does not prescribe a two-dimensional bridge algorithm. Agreement with a coarse path simulation is therefore weaker evidence than agreement with exact independent and half-plane limiting cases.

## Assumptions, scope, and research use

The model has constant asset volatility, constant instantaneous asset correlation, a deterministic exponentially moving barrier, and a constant risk-free rate. Default is completely determined by continuous asset paths. It excludes jumps, stochastic barriers, stochastic recovery, liquidity-driven default, and feedback from one firm's default to the other's drift or volatility. For nonsingular correlation, a common jump producing an atom of simultaneous default is outside this construction.

Asset correlation is not a default-indicator correlation. The mapping depends on barrier distances, drift, volatility, and horizon. A calibration that substitutes a historical default correlation directly for $\varrho$ would generally be incoherent. Likewise equity values and volatilities are not automatically the asset values and volatilities appearing in the SDE. The article assumes these structural inputs rather than providing a debt-capital-structure inversion or a robust estimation procedure.

The whitening transform becomes singular as $\varrho$ approaches either endpoint. Exactly perfect correlation or anticorrelation requires a separate lower-dimensional argument; blindly evaluating $1/\sqrt{1-\varrho^2}$ near the boundary can amplify rounding and calibration errors. The wedge angle has a sensible geometric limit, but that alone does not make the whole parameter transformation numerically stable.

The maturity digital form is particularly useful for isolating joint event probabilities from recovery and premium conventions. It can test whether a two-name engine handles path dependence correctly and can support comparative statics under an explicitly chosen structural scenario. To use it for investment decisions, one would still need observable-input mapping, a calibration dataset, quote conventions, transaction costs, parameter uncertainty, and empirical tests. None is claimed in the source.

The paper's main deliverable is therefore a reusable analytic kernel and its financial transformation. Its geometric explanation clarifies why generalized Bessel orders appear in correlated barrier problems and where normalization, reflection, and measure-change factors enter. That clarity is valuable for reimplementation even when a numerical PDE or simulation method is ultimately used for contracts with richer state dynamics.

# Back to the Future: Generating Moment Implications for Continuous-Time Markov Processes

Lars Peter Hansen and José Alexandre Scheinkman. *Econometrica* 63(4), July 1995, pp. 767–804.

Source: [SimulatedMoments_HansenScheinkman_1995.pdf](../../Finance/SimulatedMoments_HansenScheinkman_1995.pdf), 39 PDF pages including a JSTOR cover. The full article, proofs, and examples were read. The [same published article on Hansen's website](https://larspeterhansen.org/wp-content/uploads/2016/10/Back-To-the-Future-Generating-Moment-Implications-for-Continuous-Time-Markov-Processes.pdf) supplied searchable text; its 38 pages correspond to local PDF pages 2–39. Central operator identities, identification arguments, and variance/boundary formulas were checked against local page images. Page references below use printed pagination.

## Why this matters

Continuous-time economic models are specified locally: a drift, a diffusion matrix, a jump intensity, and boundary behavior describe how a state moves over an infinitesimal interval. Observations arrive at finite intervals. Recovering the exact likelihood at those intervals can require solving a transition-density partial differential equation repeatedly for every parameter and starting state. Replacing the model with a simple discrete approximation can introduce bias that does not vanish when the observation interval remains fixed.

The paper constructs exact moment restrictions from the infinitesimal generator, without requiring the transition density or a simulated path between observations. One family uses the stationary marginal distribution. A second uses pairs of observations and the generator of the process viewed backward in time. These restrictions can support GMM estimation and specification tests for nonlinear diffusions and jump processes.

The identification analysis is as important as the computational shortcut. The proposed moments do not generally identify the entire continuous-time law. For regular stationary scalar diffusions, the full families determine the drift and local variance only up to a common time scale. Yet the full discrete-time transition operator does identify a reversible continuous-time process without aliasing. Failure of identification by these moments is therefore different from an intrinsic inability of the sampled data to identify the model.

The article is theoretical. It contains no estimated interest-rate parameters, asset universe, sample dates, forecast test, simulation performance table, or trading strategy. Its financial examples motivate model classes and boundary conditions. The output to reproduce is a set of exact restrictions, identification results, and sufficient asymptotic conditions, not an absent empirical backtest.

## State process, semigroup, and generator

Let $X_t$ be a strictly stationary continuous-time Markov process with invariant distribution $Q$. Work in the real Hilbert space $L^2(Q)$, with inner product $\langle f,g\rangle=\int fg\,dQ$. Define the transition operators

$$
P_tf(x)=E[f(X_t)\mid X_0=x].
$$

Conditional expectation makes $P_t$ a contraction in $L^2(Q)$, and the Markov property gives $P_{t+s}=P_tP_s$. The maintained strong-continuity assumption is $\|P_tf-f\|_2\to0$ as $t\downarrow0$. The generator is

$$
Af=\lim_{h\downarrow0}\frac{P_hf-f}{h},
$$

where the limit is in $L^2(Q)$. Its domain $\mathcal D(A)$ consists only of functions for which that limit exists. It is generally a proper dense subset of $L^2(Q)$, and $A$ is generally unbounded. The distinction between an operator and its formal differential expression becomes essential at reflecting boundaries and when selecting test functions.

The generator is closed, satisfies $\langle Af,f\rangle\leq0$, and commutes with $P_t$ on its domain. For an admissible $f$,

$$
P_tf-f=\int_0^tP_sAf\,ds.
$$

This identity links local dynamics to finite-horizon conditional expectations without replacing a finite horizon by an infinitesimal one. In particular, $P_\Delta$ is not generally $I+\Delta A$ at a fixed observation interval $\Delta$.

For a scalar diffusion

$$
dX_t=\mu(X_t)\,dt+\sigma(X_t)\,dW_t,
$$

the generator's differential expression is

$$
Af(x)=\mu(x)f'(x)+\tfrac12\sigma^2(x)f''(x).
$$

The local variance is $a(x)=\sigma^2(x)$, not $\sigma(x)$. Multiplying the generator by a positive constant multiplies both drift and local variance by that constant; the Brownian loading itself is multiplied by its square root. Confusing these scalings would invalidate the main identification result.

Under the paper's scalar regularity and recurrence conditions, define a scale-density derivative

$$
s(x)=\exp\left\{-\int^x\frac{2\mu(z)}{a(z)}\,dz\right\}.
$$

If $1/[s(x)a(x)]$ is integrable and the boundary specification is compatible, the stationary density is

$$
q(x)=\frac{[s(x)a(x)]^{-1}}
{\int[s(z)a(z)]^{-1}\,dz}.
$$

Initializing the diffusion from this distribution gives stationarity. Smooth drift and variance coefficients alone do not establish a normalizable stationary law; the integrability and boundary conditions do real work.

For smooth test functions, Itô's formula gives a martingale after subtracting the integrated generator. The source requires the relevant terms to be square integrable, including $\sigma f'$ and $Af$, to identify the differential expression with the $L^2$ generator. A polynomial test function that looks convenient can fail these conditions in a heavy-tailed invariant distribution.

## Two exact families of moments

Stationarity implies $E[f(X_t)]$ is constant in time. Taking its generator derivative gives the first family, C1:

$$
E[Af(X_t)]=0,
\qquad f\in\mathcal D(A).
$$

These moments involve only one observed state and are exact for every sampling interval. For a scalar diffusion they become expectations of $\mu f'+af''/2$. They use the marginal stationary law and, by themselves, do not pin down how quickly the process moves through that law.

For C2, introduce the reverse-time operator

$$
P_t^*g(x)=E[g(X_0)\mid X_t=x].
$$

Stationarity makes $P_t^*$ the adjoint of $P_t$ in $L^2(Q)$. Its generator $A^*$ is the adjoint of $A$. Applying the commutation relation $AP_\Delta=P_\Delta A$ and moving the generator across the inner product yields

$$
E\left[(Af)(X_{t+\Delta})g(X_t)
-f(X_{t+\Delta})(A^*g)(X_t)\right]=0,
$$

for $f\in\mathcal D(A)$ and $g\in\mathcal D(A^*)$. This is C2, source p. 775. The forward generator acts on the later observation and the reverse generator on the earlier one. They cannot be interchanged casually in a nonreversible model.

A useful derivation writes the first expectation as $\langle P_\Delta Af,g\rangle$. Commutation changes this to $\langle AP_\Delta f,g\rangle$, and the adjoint relation changes it to $\langle P_\Delta f,A^*g\rangle$, which is the second expectation. No small-$\Delta$ expansion is involved. Choosing $g=1$ reduces C2 to C1 because $A^*1=0$.

If the process is reversible, $A=A^*$ and the same differential operator appears on both sides. Reversibility is a restriction on the stationary path law, not merely symmetry of the invariant density. For regular scalar diffusions with the boundary conditions used here, the generator can be expressed as

$$
Af=\frac{1}{2q}(aqf')'.
$$

Integration by parts makes it symmetric on appropriate test functions; extension through a core establishes self-adjointness. This supplies the practical simplification for many one-factor models.

The resulting moment variables are not generally martingale differences. Their unconditional means vanish, but the conditional expectation given the earlier state need not. Standard errors therefore require their time-series covariance structure. Treating successive C2 observations as independent is particularly inappropriate because neighboring pairs overlap.

## Boundaries and admissible model classes

For a reflecting diffusion on $[\ell,u]$, the stochastic equation contains a boundary-pushing term. Itô's formula then includes $f'(X_t)$ times that term. To make the usual interior generator apply without an extra boundary contribution, admissible test functions satisfy

$$
f'(\ell)=f'(u)=0.
$$

The invariant speed-density formula remains valid under the stated regularity conditions. One reflecting boundary and one nonattracting boundary can be handled similarly. A function such as $f(x)=x$ fails the reflecting derivative condition, so inserting it into C1 without qualification can create a false moment restriction.

Independent stationary reversible scalar factors remain reversible jointly. A time-invariant transformation $X_t=F(Z_t)$ preserves stationarity and reversibility. To ensure that the observed process is itself Markov in the paper's construction, the factors must be recoverable: $F$ is one-to-one. Continuous second derivatives then permit an Itô representation for the transformed diffusion. A many-to-one observation map does not automatically preserve the Markov property, even though it preserves time reversibility of the observed path law.

For a multivariate diffusion with drift $\mu$ and local covariance matrix $a$, the forward generator is

$$
Af=\mu'\nabla f+\tfrac12\operatorname{tr}(a\nabla^2f).
$$

The stationary reverse diffusion has the same local covariance but drift

$$
\mu_i^*(x)=-\mu_i(x)
+\frac1{q(x)}\sum_j\partial_j[q(x)a_{ij}(x)].
$$

Thus C2 can remain usable even without reversibility if $q$ and its logarithmic derivatives are tractable. The authors suggest nonparametric estimation of these derivatives as a computational device, but do not prove a complete generated-moment inference theorem for that proposal. Its smoothing error and extra uncertainty cannot simply be omitted from an application.

Stationarity in this multivariate setting corresponds to the forward density equation

$$
-\sum_i\partial_i(\mu_iq)
+\tfrac12\sum_{i,j}\partial_{ij}(a_{ij}q)=0.
$$

This is the stationary forward density equation on p. 778; zero divergence of the probability current does not, in a general multivariate model, require the current itself to vanish. Together with normalization, positivity, and appropriate boundaries, it determines the candidate invariant law; an arbitrary density is not automatically compatible with the proposed drift and covariance.

The jump-process example broadens the method beyond diffusions. Let jumps arrive with bounded state-dependent intensity $\eta(x)$ and let $K$ be the transition operator of the embedded jump chain. Then

$$
Af(x)=\eta(x)[Kf(x)-f(x)].
$$

If the embedded chain has invariant measure $\widetilde Q$ and $\int\eta^{-1}\,d\widetilde Q<\infty$, the calendar-time invariant distribution is proportional to $\eta^{-1}d\widetilde Q$. Slowly exited states receive more calendar-time weight. The reverse generator replaces $K$ by its adjoint in the embedded-chain invariant measure while retaining the state intensity.

Uniformization uses a constant intensity $\bar\eta=\sup_x\eta(x)$ and a modified chain that stays put with probability $1-\eta(x)/\bar\eta$. This explains boundedness of the jump generator and the relation between the two invariant measures. The method does not require observing how many jumps occurred between sampled states. However, computing $Kf$ and its reverse counterpart may itself be hard for nonlinear jump kernels; computational tractability is not universal.

## What the moments identify

Proposition 1 states that, under the specified generator/domain framework, satisfying all C1 restrictions is equivalent to sharing the true invariant distribution. Hence C1 is strong enough to reject a wrong stationary marginal law, but cannot discriminate among different dynamics with that law. The result uses all admissible test functions or an adequate core, not merely a handful of moments.

For scalar diffusions, the stationary relation is

$$
\mu(x)=\tfrac12\left[a'(x)+a(x)\frac{q'(x)}{q(x)}\right].
$$

Given $q$, many positive variance functions $a$ can be paired with a drift through this equation. In the source's example,

$$
\frac{q'(x)}{q(x)}=\sum_{j=-k}^{l}\alpha_jx^j,
\qquad a(x)=\rho x^\gamma,
$$

with restrictions ensuring a valid density and diffusion. C1 can identify the density-shape parameters $\alpha$, but it cannot identify $\gamma$ or the overall variance scale $\rho$ when these vary while $q$ stays fixed. C2 can identify the variance elasticity $\gamma$ in the scalar diffusion class, yet leaves $\rho$ unresolved.

Proposition 2 identifies the incremental content of C2. A candidate generator $\widetilde A$ that already satisfies C1 satisfies all C2 moments if and only if it commutes with the true sampled transition operator $P_\Delta$, including the appropriate domain mapping. Thus the moments ask whether the candidate dynamics have compatible operator structure; they do not force its entire transition operator to equal the observed one.

If both true and candidate generators are self-adjoint, spectral arguments strengthen the result. Commuting with $P_\Delta$ implies commuting with the full true semigroup and, on the relevant domains, with the true generator. The spectral representation is

$$
A=\int_{(-\infty,0]}\lambda\,dE(\lambda),
\qquad
P_\Delta=\int_{(-\infty,0]}e^{\lambda\Delta}\,dE(\lambda).
$$

Here $E$ is a projection-valued spectral measure, not an empirical expectation. Constants occupy the zero-generator eigenvalue and unit-transition eigenvalue. Spectra can also have continuous portions; a finite eigenvector decomposition is not assumed for every model.

For regular scalar diffusions, common invariant density plus this commutation property restricts the drift and local variance to a common scalar multiple. The proof first uses a compact reflecting interval, where Sturm–Liouville theory gives simple nonconstant eigenfunctions. A common eigenfunction $f$ satisfies, for each generator,

$$
(aqf')'=2\lambda qf.
$$

Integrating from the reflecting boundary gives

$$
a(x)q(x)f'(x)=2\lambda\int_\ell^xf(z)q(z)\,dz.
$$

The boundary condition removes the integration constant. Comparing the true and candidate versions forces their variance functions to be proportional; the stationary drift relation forces the same proportionality for the drifts. The paper extends the argument to the line by localization on compact reflecting intervals and smooth extensions. It does not assume that every whole-line generator has a convenient nonzero discrete eigenvalue.

The unavoidable scalar ambiguity is intuitive. Replacing $A$ by $cA$, $c>0$, changes the speed at which the process runs but leaves C1 equal to zero and multiplies each C2 restriction by $c$. If scale is left unconstrained in a sample minimum-distance problem, shrinking it toward zero can also shrink every sample residual. A practical estimator must normalize it or add a genuinely scale-identifying restriction, rather than report a spurious optimum near a zero generator.

The ambiguity is larger outside the scalar diffusion class. Independent factors can each have their own positive speed multiplier. More generally, for positive $c,d$,

$$
\widetilde Af=cAf+d\{E_Qf-f\}
$$

combines a speed change with resets to an independent invariant-distribution draw. It shares $Q$ and commutes with the original dynamics, so C1 and C2 cannot distinguish it even though its path behavior differs. This counterexample prevents extending the scalar up-to-scale result to arbitrary Markov generators.

## No aliasing under reversibility is a different result

Suppose the entire $P_\Delta$ is known and both candidate generators are reversible. The exponential map $\lambda\mapsto e^{\lambda\Delta}$ is one-to-one on the nonpositive real line. Uniqueness of the self-adjoint spectral representation therefore implies a unique generator. Proposition 5 establishes this no-aliasing result.

Without reversibility, complex spectral components can create different continuous-time dynamics with identical fixed-interval observations. The result does not say that finite samples identify an unrestricted operator accurately, nor that the two proposed moment families extract all of its information. It says the population transition operator has a unique reversible embedding in the stated class.

The source suggests restoring scalar time scale when an eigenfunction is explicitly available. If $Af=\lambda f$, then

$$
E[f(X_{t+\Delta})\mid X_t]
=e^{\lambda\Delta}f(X_t).
$$

For a centered nondegenerate eigenfunction, its lagged covariance relative to variance identifies $e^{\lambda\Delta}$ and hence $\lambda$. This condition supplies information omitted by the homogeneous C1/C2 equations. The paper also sketches a variational route using the leading nonconstant eigenvalue, but explicitly leaves formal nonparametric estimation over the infinite-dimensional function space for future work.

As a reconstruction example rather than a reported experiment, an Ornstein–Uhlenbeck model $dX=\kappa(m-X)dt+\sigma dW$ has stationary mean $m$ and variance $v=\sigma^2/(2\kappa)$. Marginal moments identify $m,v$, while a separate lag-correlation condition identifies $e^{-\kappa\Delta}$. Then $\kappa=-\log r_\Delta/\Delta$ and $\sigma^2=2\kappa v$. This illustrates exactly where the missing time scale enters. It is not an instruction to use an empirical correlation outside $(0,1)$ without addressing model fit and finite-sample uncertainty.

## Test functions, cores, and usable moment selection

An arbitrary dense set of functions is not sufficient for an unbounded generator. A core is dense in the generator's graph norm: both $f_n\to f$ and $Af_n\to Af$ must hold. Section 6 uses cores to justify replacing an abstract full domain by functions on which the generator is readily evaluated.

For regular whole-line scalar diffusions under the stated smoothness/growth conditions, smooth compactly supported functions provide such a core. The paper transfers core results from continuous functions under the sup norm to $L^2(Q)$ and constructs a countable family by approximating functions and their first two derivatives on expanding compact sets. Reflecting models require the corresponding derivative boundary restrictions. Bounded jump generators are simpler because a dense function family is enough when the operator is bounded.

These are population reductions, not a guarantee that any finite basis identifies the chosen finite-dimensional parameterization. A finite application must inspect the Jacobian of its selected moments after any scale normalization. Bounded test functions are particularly useful for C2: products of two square-integrable variables need only be integrable, not square integrable, whereas bounded test functions together with square-integrable generator images yield the second moments needed for a central limit theorem.

A concrete GMM implementation can choose test functions $f_j,g_j$, form

$$
h_{1j,t}(\beta)=(A_\beta f_j)(X_t),
$$

$$
h_{2j,t}(\beta)=(A_\beta f_j)(X_{t+\Delta})g_j(X_t)
-f_j(X_{t+\Delta})(A_\beta^*g_j)(X_t),
$$

stack the desired restrictions, and minimize their sample mean quadratic form. This is a direct implementation of the paper, but the article specifies no universal basis count, knot locations, support widths, weighting update, optimizer tolerance, or bandwidth. Those are application inputs to report and assess, not hidden constants recoverable from the source.

After identification and regularity checks, conventional GMM covariance uses the derivative of the stacked mean and its long-run covariance. An overidentification statistic tests only the selected restrictions and requires the usual rank and covariance conditions. Neither the finite number of moments nor an accepted test establishes that the whole continuous-time model is correct.

## Ergodicity and central limit justification

Continuous-time ergodicity is characterized by the generator kernel: among zero-mean functions in its domain, $Af=0$ must imply $f=0$. Sampled-process ergodicity instead requires that $P_\Delta f=f$ have no nonzero zero-mean solution. These are distinct requirements. A periodic component can be invisible at a particular observation interval, corresponding to imaginary generator eigenvalues whose exponentials equal one.

Reversible generators have real nonpositive spectra, so continuous-time ergodicity rules out this sampling-period problem. The article gives related sufficient arguments for bounded-intensity jump processes and suitable nondegenerate multivariate diffusions. Stationarity alone only gives time averages conditional on invariant events; it does not justify replacing them by the unconditional $Q$ expectation for every initial component.

For a continuous record and a test function $f$, the martingale

$$
M_T=-f(X_T)+f(X_0)+\int_0^TAf(X_t)\,dt
$$

approximates the integrated moment up to a boundary term with bounded $L^2$ norm. Dividing by $\sqrt T$ removes that term. Under the ergodic martingale central limit conditions, the asymptotic variance is

$$
-2\langle f,Af\rangle.
$$

For scalar diffusions this equals $E[a(X)(f'(X))^2]$ after integration by parts. It is nonnegative, and can be zero for a degenerate direction. This continuous-record variance is not automatically the variance for a sequence of monthly or daily observations.

For the sampled chain, put $P=P_\Delta$ and consider a centered $\psi\in L^2(Q)$. If $P$ is a strict contraction on the centered subspace, the Poisson equation has solution $u=(I-P)^{-1}\psi$. The martingale increments are $u(X_j)-Pu(X_{j-1})$. Their partial sum differs from $\sum_j\psi(X_j)$ by an endpoint term, and the long-run variance is

$$
\|u\|_2^2-\|Pu\|_2^2
=\langle\psi,\psi\rangle
+2\langle\psi,P(I-P)^{-1}\psi\rangle.
$$

This is equation (7.9), p. 798. It is the operator form of the variance plus twice the sum of lagged covariances. For C2 variables $v(X_{j+1},X_j)$, first separate the martingale difference $v-E(v\mid X_j)$ from its conditional mean, then apply the Poisson construction to the latter. Their combined covariance, including cross terms, governs inference.

The generator condition used to guarantee sufficient contraction is the coercivity or spectral-gap inequality

$$
-\langle Af,f\rangle\geq\delta\operatorname{Var}_Q(f),
\qquad\delta>0,
$$

on a core and hence the full domain. It yields $\|P_tf\|_2\leq e^{-\delta t}\|f\|_2$ for centered functions. In the reversible case it means zero is an isolated spectral point and all centered directions are separated from it. This is stronger than recurrence or ergodicity alone.

Proposition 8 states an equivalence between fixed-interval strict contraction and the generator condition. For implementation, the sufficient direction above is the safe requirement; a converse inferred solely from a finite-horizon contraction can require care for general non-self-adjoint semigroups. In the reversible setting used for the scalar identification results, spectral calculus supplies the clean equivalence. This note does not extend that equivalence without qualification to arbitrary nonnormal dynamics.

For scalar diffusions the gap condition is a weighted Poincaré inequality. Fix an interior point $z$. A useful pair of sufficient tail checks is

$$
\sup_{z<r<u}Q([r,u))\int_z^r\frac{dy}{a(y)q(y)}<\infty,
$$

$$
\sup_{\ell<r<z}Q((\ell,r])\int_r^z\frac{dy}{a(y)q(y)}<\infty.
$$

They balance invariant tail mass against local mobility. Proposition 9 gives simpler boundary limits involving $\sigma q$ and, when that product tends to zero, the ratio $\sigma/(2\mu-\sigma\sigma')$. The assumptions include an integrable speed density, positive interior volatility, and reflecting behavior at attainable finite boundaries. A vanishing variance at a boundary is therefore not automatically disqualifying: the square-root process is an example satisfying the source's sufficient conditions. Conversely, weak inward drift can permit recurrence while leaving no spectral gap.

## Practical implications and limits

The method is attractive when the whole Markov state is observed at discrete dates and the generator is simpler than the transition law. The main analysis assumes that observability. Filtering latent volatility or latent economic factors and then treating estimates as exact states adds an observation problem absent from the theorem. The factor-model example avoids it through an invertible mapping from factors to observed variables.

Sampling need not be infinitesimally frequent. The authors note that the moment identities extend to systematic calendar patterns or suitably exogenous stationary sampling, allowing weekends and holidays in principle. Such sampling can change central limit approximations, and state-dependent observation times cannot be treated as exogenous without justification. Time units must also be declared when adding the scale-identifying eigenvalue restriction.

No efficiency-optimal finite test-function selection is established, and no finite-sample Monte Carlo comparison is supplied. Nonparametric recovery, growing moment families, and density-derivative substitution are outlined as directions rather than completed estimation packages. The strongest reusable conclusion is therefore a disciplined separation: local generator formulas produce exact restrictions, domains and boundaries determine which restrictions are valid, identification determines what they can recover, and dependence conditions determine whether estimated moments have usable standard errors. Keeping these four steps distinct prevents an easy-to-compute GMM system from being mistaken for a fully identified and statistically justified model.

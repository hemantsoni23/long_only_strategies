# Measuring Distribution Model Risk

**Thomas Breuer and Imre Csiszár (2016).** *Mathematical Finance* 26(2), 395–411, DOI 10.1111/mafi.12050. Source: [ModelRiskStressTesting_BauerCsiszar_2013.pdf](../../Finance/ModelRiskStressTesting_BauerCsiszar_2013.pdf). The filename misspells Breuer and uses the 2013 revision/copyright year; the issue is April 2016. All 17 PDF pages, including proofs and references, are covered. This is a theoretical article without empirical data, simulation tables, or a separate appendix.

## Why this matters

A portfolio can have a reassuring expected loss under one estimated distribution and a much worse expectation under a nearby alternative. The paper turns that concern into an optimization problem: minimize expected payoff over a divergence ball around a baseline distribution. It derives both the worst expectation and, when one exists, the probability distribution that attains it.

The practical distinction is between computing a number and exhibiting a valid worst-case model. An optimization may have a finite infimum without an attaining distribution. It may also become completely uninformative for arbitrarily small divergence radius if the baseline payoff has an insufficiently controlled loss tail. A numerical solver operating on a finite sample can conceal both issues.

The contribution is a unified convex-integral framework for relative entropy, general $f$-divergences, and Bregman distances, with explicit existence and finiteness conditions. Entropic robustness and exponential tilting are not claimed as new: the authors connect their results to prior robust-control, convex-risk, and entropy-minimization work. The extension clarifies why generalized exponential families solve several superficially different problems and what happens at nonregular boundaries.

## Payoff convention and the uncertainty set

Let $X:\Omega\to\mathbb R$ be a one-horizon portfolio payoff and $P_0$ an estimated baseline distribution of risk factors. Positive $X$ is a gain. For a divergence $D$ and radius $k>0$, define

$$
\Gamma_k=\{P:D(P\Vert P_0)\le k\},\qquad
V(k)=\inf_{P\in\Gamma_k}E_P[X],\qquad
\operatorname{MR}_k(X)=-V(k).
$$

The source's model-risk measure is the worst expected loss, including the baseline level. The incremental deterioration is instead

$$
\Delta_k(X)=E_{P_0}[X]-V(k).
$$

It is nonnegative when $P_0$ is feasible and vanishes at a singleton baseline set. These two quantities should not be interchanged. For example, a strictly positive payoff can have negative $\operatorname{MR}$ while its uncertainty surcharge $\Delta_k$ remains positive.

For a fixed common ambiguity set, the worst-loss functional is coherent on an appropriate payoff domain: monotonicity, cash translation, positive homogeneity, and subadditivity follow from its supremum-of-linear-expectations representation. The normalized deterioration is unchanged by adding cash and hence is not the same monetary risk functional. Changing the uncertainty set separately for every portfolio can also destroy properties that hold for a fixed set.

The radius is chosen by the user. The paper supplies no sampling-confidence interpretation, Basel mapping, fitted radius, or estimation procedure for it. With natural-log relative entropy, $k$ is dimensionless. A radius in one divergence has no universal numerical equivalence to the same radius in another divergence.

The payoff function is treated as known. Misspecified valuation maps, omitted risk factors, incorrect contractual cash flows, or a wrong state space are outside the modeled distribution uncertainty. If $X$ represents utility rather than currency payoff, the same mathematics evaluates multiple-priors preferences, but the result has utility units and should not be labeled a monetary capital requirement.

## Divergences and support restrictions

For densities $p,p_0$ relative to a reference measure $\mu$, relative entropy is

$$
I(p\Vert p_0)=\int\left[p\log\frac p{p_0}-p+p_0\right]d\mu.
$$

For probability densities the linear terms integrate to zero. Finite $I(P\Vert P_0)$ requires $P\ll P_0$. Thus a baseline assigning zero probability to a scenario cannot acquire positive probability there through a finite forward-KL perturbation. An empirical distribution with finitely many observations permits reweighting those observations, not creating an unseen crisis state.

An $f$-divergence has the dominated form $D_f(P\Vert P_0)=\int f(dP/dP_0)dP_0$, with a convex generator normalized at one. The full measure-theoretic definition also allows a singular component $P_s$ and adds

$$
P_s(\Omega)\lim_{s\to\infty}\frac{f(s)}s.
$$

If that limit is infinite, the generator is cofinite and finite divergence enforces domination by $P_0$. If it is finite, the full divergence ball can contain singular alternatives. The paper's subsequent choice $\mu=P_0$ then solves the dominated subset, not automatically the whole full-measure ball. This restriction is explicit in Section 5 and materially affects interpretation.

For differentiable strictly convex $f$, the Bregman construction is

$$
B_{f,\mu}(P,P_0)=\int\left[f(p)-f(p_0)-f'(p_0)(p-p_0)\right]d\mu.
$$

The source also accommodates nondifferentiable generators using appropriate directional derivatives. Unlike an $f$-divergence between probability measures, a general Bregman distance depends on the chosen dominating measure and density representation. That reference measure is an input, not disposable notation. Squared $L^2$ density distance and Itakura–Saito distance are examples; the entropic generator reproduces KL.

For reverse KL the normalized generator is $f_0(s)=-\log s+s-1$. PDF page 5 prints a final $+1$ in its earlier example, which would give $f_0(1)=2$ and would not vanish for identical probabilities. Section 5 on PDF page 13 gives the consistent $-1$ form. The equations here use that latter normalization. Forward KL and reverse KL are distinct and generally have different worst-case solutions and tail requirements.

Expected shortfall can be represented by a density cap $0\le dP/dP_0\le1/\alpha$, where $\alpha$ is the tail probability in the paper's remark. Its corresponding indicator generator is not strictly convex and is not a divergence in the paper's restrictive sense. The remark establishes a conceptual relationship, not license to apply every strict-convexity uniqueness theorem to expected shortfall unchanged.

## General convex-integral formulation

Work with nonnegative densities $p$ relative to a finite or sigma-finite $\mu$. Let

$$
H(p)=\int\beta(\omega,p(\omega))\,d\mu(\omega),
$$

where $\beta$ is measurable in the state and strictly convex in its positive density argument. Extend it to zero by the one-sided limit and set it to infinity for negative arguments. Assume $H(p)\ge H(p_0)=0$ for probability densities, and let

$$
m=\mu\text{-ess inf }X<b_0=E_{P_0}[X]<M=\mu\text{-ess sup }X.
$$

The finite baseline mean and strict inequalities exclude the trivial constant-payoff case. The lower and upper support endpoints may be infinite. The problem becomes

$$
V(k)=\inf_{p\ge0,\ \int p\,d\mu=1,\ H(p)\le k}\int Xp\,d\mu.
$$

Introduce the minimum divergence needed to reach a specified expectation,

$$
F(b)=\inf_{p\ge0,\ \int p\,d\mu=1,\ \int Xp\,d\mu=b}H(p),
\qquad k_{\max}=\lim_{b\downarrow m}F(b).
$$

For $0<k<k_{\max}$, Proposition 3.1 says that there is a unique $b\in(m,b_0)$ satisfying $F(b)=k$, and $V(k)=b$. Attainment of the original minimum is equivalent to attainment of the moment-constrained minimum at that $b$. At zero radius, $V(0)=b_0$; once the radius reaches the effective threshold, the infimum is the essential lower endpoint $m$. Endpoint attainment and uniqueness require separate treatment.

The reasoning is useful for implementation. For an expectation below the crossing, the least possible divergence already exceeds $k$, so that expectation is infeasible. Expectations just above the crossing can be attained with divergence below $k$, even when the crossing itself has no minimizing density. Taking their limit identifies the infimum. The printed proof on PDF page 7 contains a reversed/incorrect expression after introducing $t\in(b,b_0)$: the needed statement is existence of densities with $H(p)<k$, not the printed $F(t)>k$. Its concluding lower-bound symbol should establish $V(k)\ge b$. These repairs follow from the stated definitions and do not alter the proposition.

## Duality reduces the distribution search to two parameters

Define the pointwise conjugate and its integrated version,

$$
\beta^*(\omega,x)=\sup_{s\ge0}\{xs-\beta(\omega,s)\},
\qquad
K(\theta_1,\theta_2)=\int\beta^*(\omega,\theta_1+\theta_2X(\omega))\,d\mu.
$$

Allowing the density mass to vary gives the two-moment value function $J(a,b)$ with constraints $\int p=a$ and $\int Xp=b$. The source shows $K=J^*$ and, in the relevant interior, $J=K^*$. In particular,

$$
F(b)=\sup_{\theta_1,\theta_2}\{\theta_1+\theta_2b-K(\theta_1,\theta_2)\},\qquad m<b<M.
$$

The generalized exponential family is

$$
p_\theta(\omega)=(\beta^*)'(\omega,\theta_1+\theta_2X(\omega)).
$$

Its admissible parameter set $\Theta$ requires finite $K$ and $\theta_1+\theta_2X<\beta'(\omega,+\infty)$ almost everywhere. These functions need not integrate to one. Calling a candidate a density before checking normalization is an error, particularly at the domain boundary.

In the interior of $\operatorname{dom}K$,

$$
K_{\theta_1}=\int p_\theta\,d\mu,
\qquad K_{\theta_2}=\int Xp_\theta\,d\mu.
$$

Theorem 4.2 identifies a worst-case density, in the active-radius regime, by three conditions:

$$
\theta_2<0,\qquad \int p_\theta\,d\mu=1,
\qquad \theta_1+\theta_2\int Xp_\theta\,d\mu-K(\theta)=k.
$$

The worst expectation is then $\int Xp_\theta d\mu$. Under the theorem's assumptions, an attaining density exists exactly when a member of this family meets these conditions, and the attaining density is unique. Essential smoothness of $K$ is a sufficient existence condition, not a necessary one. Interior solutions can be found from the two derivative equations in Corollary 4.3; boundary solutions must not be excluded merely because those interior derivatives are unavailable.

A short independent verification follows from Fenchel's inequality. For any feasible $p$,

$$
\theta_1+\theta_2E_p[X]\le H(p)+K(\theta)\le k+K(\theta).
$$

Because $\theta_2<0$, division reverses the inequality and gives $E_p[X]\ge[k+K(\theta)-\theta_1]/\theta_2$. The candidate attains equality pointwise in Fenchel's inequality and uses the full radius, proving its optimality. This also explains the negative sign of the payoff tilt: it emphasizes low-payoff states. In the printed proof of Theorem 4.2, the interval following equation (4.7) is not consistent as written; substituting $t=b_0$ directly yields the needed contradiction if $b\ge b_0$.

## When the risk number is meaningful

Theorem 4.5 gives the critical condition:

$$
k_{\max}>0
\quad\Longleftrightarrow\quad
\exists\,(\theta_1,\theta_2)\in\operatorname{dom}K\text{ with }\theta_2<0.
$$

If this condition holds, every probability density with finite $H$ has expected payoff greater than negative infinity. The same Fenchel inequality provides the proof. If the condition fails, every positive radius collapses the worst expectation to the essential infimum. For an unbounded-below payoff that means infinite worst expected loss, however small the divergence radius.

A payoff bounded below is sufficient for a positive threshold. With $m=-\infty$, a positive threshold is necessarily infinite, so every finite positive radius remains in the active regime. For autonomous noncofinite generators, boundedness below is also necessary. These results warn against assuming that an estimated finite variance alone makes an entropic robust risk finite.

## Relative entropy: exponential tilting and its boundary

For forward KL, take $\mu=P_0$ and $\beta(s)=s\log s-s+1$, whose conjugate is $e^x-1$. Define the baseline cumulant-generating function

$$
\Lambda(\tau)=\log E_{P_0}[e^{\tau X}].
$$

Then $K(\theta_1,\theta_2)=e^{\theta_1+\Lambda(\theta_2)}-1$. Normalization sets $\theta_1=-\Lambda(\tau)$, leaving a one-parameter family

$$
\frac{dP_\tau}{dP_0}=e^{\tau X-\Lambda(\tau)},\qquad \tau<0.
$$

Where the derivative is finite, its expectation is $\Lambda'(\tau)$ and its relative entropy is $\tau\Lambda'(\tau)-\Lambda(\tau)$. Solve

$$
\tau\Lambda'(\tau)-\Lambda(\tau)=k
$$

for a negative $\tau$. If an admissible solution exists, the worst expectation is $V(k)=\Lambda'(\tau)$ and the tilted measure attains it. The density ratio is dimensionless; $\tau$ has reciprocal-payoff units. The payoff unit must therefore be consistent between exponentiation and the reported expectation.

The necessary and sufficient nondegeneracy condition is existence of some negative $\tau$ with finite $\Lambda(\tau)$. In loss notation $L=-X$, this requires a finite positive exponential moment of $L$ at some positive argument. Heavy-tailed loss distributions can fail this even if they have several finite ordinary moments. A finite historical scenario table always has exponential moments, so passing this check in the table does not validate an underlying unbounded-tail model.

Let $\tau_{\min}=\inf\{\tau:\Lambda(\tau)<\infty\}$. The regular exponential-tilt solution covers the active range when the negative domain extends indefinitely, or up to the boundary radius

$$
k_c=-\Lambda(\tau_{\min})+\tau_{\min}\Lambda'(\tau_{\min})
$$

when the displayed boundary quantities are finite. If $\tau_{\min}<0$ is finite, the boundary derivative is finite, and $k>k_c$ within the active regime, the root equation has no negative solution. Nevertheless, the convex-conjugate formula yields

$$
V(k)=\frac{k+\Lambda(\tau_{\min})}{\tau_{\min}}.
$$

The infimum is not attained by any feasible distribution in this case. A failed tilt root is therefore not sufficient evidence that the value is undefined. Conversely, renormalizing a numerical boundary candidate and calling it the worst distribution can misstate the result. The source's nearby nested $\Lambda(\Lambda'(\tau_{\min}))$ expression is a typographical problem; the linear conjugate branch applies below $b=\Lambda'(\tau_{\min})$.

For a finite scenario model, if the minimum payoff has baseline probability mass $q_{\min}>0$, the minimum KL needed to concentrate on that minimum-payoff event is $-\log q_{\min}$. Beyond that radius the worst expectation is the minimum payoff itself. This is a derived useful specialization; at and beyond the threshold, uniqueness conclusions from the interior active regime should not be extrapolated.

## Power divergences and tail tradeoffs

The power-divergence generators are

$$
f_\alpha(s)=\frac{s^\alpha-\alpha(s-1)-1}{\alpha(\alpha-1)},
$$

with limits $f_1(s)=s\log s-s+1$ and $f_0(s)=-\log s+s-1$. For $\alpha\ne0,1$, the conjugate on its finite domain is

$$
f_\alpha^*(x)=\frac{[1+(\alpha-1)x]_+^{\alpha/(\alpha-1)}-1}{\alpha}.
$$

For $\alpha>1$ it is finite for all real $x$. For $\alpha<1$ it is infinite above $1/(1-\alpha)$, with the boundary interpreted by the appropriate limit. The candidate likelihood ratio is

$$
p_\theta=[1+(\alpha-1)(\theta_1+\theta_2X)]_+^{1/(\alpha-1)}.
$$

When $\alpha<1$, the argument must be strictly positive in $\Theta$, so the positive-part notation can be omitted there. This density formula also has the stated $\alpha=0$ interpretation; the exponential limit handles $\alpha=1$.

For $\alpha>1$, the exact condition for a positive useful threshold is

$$
E_{P_0}[(X_-)^{\alpha/(\alpha-1)}]<\infty,
\qquad X_-=\max(-X,0).
$$

For $\alpha<1$, the corresponding condition in the dominated problem is essential boundedness of $X$ below. Thus divergence choice and tail admissibility are linked. At $\alpha=2$, a finite second moment of the loss part suffices, unlike KL's exponential-moment requirement. However, this does not make the same numerical radius equally conservative across the two choices.

Unlike KL, normalization generally does not eliminate a parameter analytically. Solve the normalization and divergence-budget equations jointly and respect the positivity/domain constraints. Clipped zero weights for some scenarios when $\alpha>1$ are part of the mathematics, not necessarily numerical failure.

## Bregman balls retain the baseline density explicitly

For differentiable $f$ and baseline density $p_0$ relative to the specified $\mu$, the integrand is

$$
\beta(\omega,s)=f(s)-f(p_0(\omega))-f'(p_0(\omega))(s-p_0(\omega)).
$$

Its conjugate is $\beta^*(\omega,x)=f^*(x+f'(p_0))-f^*(f'(p_0))$, giving

$$
p_\theta(\omega)=(f^*)'[\theta_1+\theta_2X(\omega)+f'(p_0(\omega))].
$$

Insert that expression into the same two equations for unit mass and radius. The source does not claim a universal simpler closed form for this case. If $f'(0)=-\infty$, its specialization assumes strictly positive $p_0$; if $f'(0)>-\infty$, that extra positivity requirement is unnecessary. Setting $\mu=P_0$ and normalizing $f(1)=f'(1)=0$ reduces this construction to an $f$-divergence, so a genuinely different Bregman specification must retain its intended reference measure.

## Penalized divergence preferences

The related problem fixes a penalty multiplier $\lambda>0$ rather than a radius:

$$
W_\lambda(X)=\inf_{p\ge0,\int p\,d\mu=1}
\left[\int Xp\,d\mu+\lambda H(p)\right].
$$

The source shows that this becomes a one-dimensional dual optimization:

$$
W_\lambda=\lambda\sup_{\theta_1}
\left[\theta_1-K\left(\theta_1,-\frac1\lambda\right)\right].
$$

It is greater than negative infinity exactly when some $(\theta_1,-1/\lambda)$ lies in $\operatorname{dom}K$. If the associated generalized exponential function normalizes to one, it attains the primal minimum. Otherwise the maximizing first parameter is a boundary value and the associated function has mass below one; the source explicitly separates that dual optimum from an ordinary normalized worst-case density.

For KL the result reduces to

$$
W_\lambda(X)=-\lambda\log E_{P_0}[e^{-X/\lambda}],
$$

whenever the exponential moment is finite, with the exponential tilt as the candidate minimizer. The usual expected-payoff-plus-divergence interpretation also requires the relevant terms to be defined, rather than evaluating an indeterminate infinity-minus-infinity expression at a domain boundary. The convex-integral formulation is the appropriate object for diagnosing such cases.

If $X$ has currency units, $\lambda$ has currency units because divergence is dimensionless. The risk functional $-W_\lambda$ is convex but generally not positively homogeneous. It is therefore distinct from the coherent fixed-radius worst-loss measure. Under regularity, a fixed-radius solution has multiplier $\lambda=-1/\theta_2$, but one must solve for that multiplier; a fixed penalty does not impose a fixed divergence distance across different portfolios.

## Reproducible implementation and analytic validation

For discrete scenarios $x_i$ with positive baseline probabilities $q_i$, a KL implementation can evaluate the log-sum-exp $\Lambda(\tau)=\log\sum_iq_ie^{\tau x_i}$. The tilted probabilities are $w_i=q_ie^{\tau x_i-\Lambda(\tau)}$. Evaluate their sum, mean, and divergence directly after solving the scalar radius equation. Stable exponentiation is essential when adverse scenarios receive very large likelihood ratios.

The radius function has derivative $\tau\Lambda''(\tau)$, which is nonpositive for negative $\tau$ because $\Lambda''$ is the tilted variance. Thus moving the tilt farther negative increases divergence until an endpoint is reached. Bracket the root in the valid domain, check the endpoint threshold, and distinguish a regular solution, an attained minimum-payoff boundary, and a nonattained infinite-support boundary. Report normalization and radius residuals rather than only a solver success flag.

For general $H$, evaluate $\beta^*$ and its derivative, construct $K$, and solve the two moment equations while enforcing $\Theta$. Independently verify the primal divergence, expected payoff, and Fenchel lower bound. Finite quadrature error, Monte Carlo error in expectations, parameter-estimation error in $P_0$, and ambiguity-radius judgment are different uncertainty sources.

A useful derived validation example is Gaussian payoff $X\sim N(\mu_X,\sigma_X^2)$ with $\sigma_X>0$. Since $\Lambda(\tau)=\mu_X\tau+\tfrac12\sigma_X^2\tau^2$, the exact KL solution is

$$
\tau^*=-\frac{\sqrt{2k}}{\sigma_X},\qquad
V(k)=\mu_X-\sigma_X\sqrt{2k},\qquad
\Delta_k=\sigma_X\sqrt{2k}.
$$

For the penalty formulation, $W_\lambda=\mu_X-\sigma_X^2/(2\lambda)$. These are analytic checks derived from the paper's formulas, not empirical examples it reports. For a more general distribution with sufficient exponential moments near zero, expansion of $\Lambda$ gives the small-radius approximation $\Delta_k=\sigma_X\sqrt{2k}+O(k)$. It is exact for Gaussian payoff but is not a universal finite-radius variance formula.

## Scope and unresolved choices

The paper has no asset universe, historical sample, calibrated payoff, transaction costs, out-of-sample forecasts, or empirical benchmark. Reproducing its mathematical method requires a specified state space, payoff function, baseline distribution, divergence orientation and normalization, reference measure where relevant, radius or penalty multiplier, and a numerical integration scheme. A business application additionally needs a defensible reason for its ambiguity set and stress scenarios beyond the baseline support.

Dominated divergence balls cannot generally compare continuous and discrete distributions through ordinary weak approximation: mutually singular measures can have a constant or infinite divergence even when their payoff implications are close. Similarly, different volatility laws on path space may be mutually singular, so this one-stage dominated framework is not automatically a dynamic uncertain-volatility model. The source acknowledges these limitations.

The strongest conclusion is conditional and constructive: under explicit integrability and dual-domain conditions, distributional robustness can be computed through one or two scalar parameters, and the associated adverse reweighting can be identified. Outside those conditions, the correct output may be a finite unattained bound or an infinite worst loss. Treating either as an ordinary calibrated worst-case probability model would erase the central mathematical distinction of the paper.

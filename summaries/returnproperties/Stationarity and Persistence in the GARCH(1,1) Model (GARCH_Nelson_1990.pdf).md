# Stationarity and Persistence in the GARCH(1,1) Model

Daniel B. Nelson, *Econometric Theory* 6 (1990), pp. 318–334, DOI 10.1017/S0266466600005296. Source: [GARCH_Nelson_1990.pdf](../../Finance/GARCH_Nelson_1990.pdf). All 17 PDF pages, including all six theorem statements, the three figures, and the proof and simulation appendix, were read. Central inequalities and the simulation specification were checked against page images. Printed page numbers are used below.

## Why this matters

An estimated GARCH persistence sum near one is frequently interpreted as evidence that volatility has no stable long-run distribution. Nelson shows why that inference confuses different mathematical questions. A process may have a stationary distribution even though its unconditional variance is infinite. An initial condition may disappear on almost every realized path even while its contribution to an expected future variance remains constant or grows. A shock can therefore be nonpersistent under one criterion and persistent under another.

The most consequential example is IGARCH. With a positive intercept and nondegenerate standardized innovations, IGARCH(1,1) admits a strictly stationary, ergodic solution but does not have a finite unconditional second moment for returns. With zero intercept, the conditional variance process converges to zero almost surely even though its expectation can remain unchanged. These facts matter for long-horizon risk forecasts, simulation initialization, moment-based inference, and interpretations of volatility mean reversion.

The paper is theoretical, with numerical parameter-region plots and a Monte Carlo illustration of stationary IGARCH distributions. It does not estimate a model on a financial dataset, rank forecast methods, or construct a trading strategy. Its contribution is a set of stationarity, moment, and persistence criteria, together with proofs that explain why familiar unit-root intuition can mislead.

## Model, assumptions, and two constructions

Write $V_t=\sigma_t^2$ for the conditional scale squared. The process is

$$
\varepsilon_t=\sigma_t z_t,\qquad
V_t=\omega+\beta V_{t-1}+\alpha\varepsilon_{t-1}^2
     =\omega+A_{t-1}V_{t-1},\qquad A_t=\beta+\alpha z_t^2.
$$

The assumptions are $\omega\geq0$, $\beta\geq0$, $\alpha>0$, iid finite real-valued $z_t$, and nondegenerate $z_t^2$. The expectation $E[\log A_t]$ must exist in the extended sense: its positive and negative parts cannot both have infinite expectations. It may equal $-\infty$. If $\beta>0$, the negative part is bounded, which simplifies this requirement.

The usual normalization $E[z_t]=0$, $E[z_t^2]=1$ is not required for the main stationarity results. Under that normalization $V_t$ is the conditional variance of $\varepsilon_t$. If only $E[z_t^2]=1$ is imposed, it is the conditional second moment. When the second moment of $z_t$ is infinite, $V_t$ is a scale parameter and calling it a conditional variance is incorrect. This is particularly relevant to the paper's Cauchy example.

The **conditional construction** starts at time zero with $0<V_0<\infty$ almost surely, independently of subsequent innovations. Repeated substitution gives

$$
V_t=V_0\prod_{j=1}^{t}A_{t-j}
+\omega\left(1+\sum_{k=1}^{t-1}\prod_{j=1}^{k}A_{t-j}\right).
$$

The first term carries the initial condition; the second accumulates intercept contributions. The **infinite-past construction**, denoted here $V_t^*$, is

$$
V_t^*=\omega\left(1+\sum_{k=1}^{\infty}\prod_{j=1}^{k}A_{t-j}\right),\qquad
\varepsilon_t^*=\sqrt{V_t^*}\,z_t.
$$

At first this is an extended-valued random variable: convergence of the infinite series must be established. When $\omega=0$, the paper defines the infinite-past construction to be identically zero and studies the nontrivial dynamics through the conditional construction instead. Consequently, statements about the zero-intercept model should not be casually transferred to the positive-intercept stationary distribution.

## The governing log-growth criterion

Define the average log multiplier

$$
\gamma=E[\log(\beta+\alpha z_t^2)].
$$

For $\omega=0$, the model becomes a random product. Whenever logs are finite,

$$
\log V_t=\log V_0+\sum_{j=0}^{t-1}\log A_j.
$$

Theorem 1, p. 320, gives the complete classification: $V_t\to0$ almost surely when $\gamma<0$; $V_t\to\infty$ almost surely when $\gamma>0$; and at $\gamma=0$ the log process is a driftless random walk with $\liminf V_t=0$ and $\limsup V_t=\infty$ almost surely under the theorem's nondegeneracy assumptions. Thus equality at the log boundary is not a stable positive variance. If a multiplier can be exactly zero, the product may be absorbed at zero; the extended negative-log case belongs with contraction rather than the ordinary finite-log random-walk description.

For $\omega>0$ and $\gamma<0$, Theorem 2 establishes a finite, nondegenerate, strictly stationary and ergodic infinite-past solution. It satisfies

$$
\frac{\omega}{1-\beta}\leq V_t^*<\infty\quad\text{almost surely}.
$$

The condition $\gamma<0$ itself implies $\beta<1$, since $A_t\geq\beta$. The lower bound follows by replacing every multiplier by its minimum $\beta$ in the positive series. It is a support bound, not the mean of the stationary distribution.

A conditional process driven by the same future innovations approaches the stationary process in the coupling sense

$$
V_t-V_t^*\longrightarrow0\quad\text{almost surely}.
$$

The distribution of $V_t$ consequently converges weakly to the stationary law. This does not say that $V_t$ converges to a constant random variable: both paths continue fluctuating, but their difference disappears. Weak convergence of distributions also does not imply convergence of unbounded moments without additional integrability conditions.

The printed Theorem 2 groups $\gamma\geq0$ together and states almost-sure divergence of the conditional process as well as divergence of the infinite-past series. Its zero-log-growth boundary assertion is stronger than is needed for the stationary-region results summarized here. A reproduction of the paper should record that as the source's stated boundary claim; the arguments and simulation recipe in this note use the strict negative region, and no almost-sure convergence claim at the positive-intercept equality boundary is needed to implement them.

## Why the stationary construction works

The central proof mechanism is contraction of products, not a calculation of $E[V_t]$. For a fixed time and finite $\gamma<0$, the strong law implies that sufficiently long products satisfy, almost surely,

$$
\prod_{j=1}^{k}A_{t-j}\leq\exp(\gamma k/2)
$$

after a random finite cutoff. If $\gamma=-\infty$, truncating the negative log tail and applying the strong law instead gives eventual decay at any chosen finite negative exponential rate; substituting $-\infty$ into the displayed bound would be invalid. The tail of the stationary series is then dominated by a convergent geometric series. The proof in the appendix, pp. 331–332, turns this observation into finiteness and establishes stationarity and ergodicity because the result is a measurable function of the infinite iid innovation history.

For two conditional paths with starting values $v$ and $\widetilde v$ and identical innovations,

$$
V_t-\widetilde V_t=(v-\widetilde v)\prod_{j=0}^{t-1}A_j.
$$

That product disappears almost surely in the contracting region. This identity is useful for choosing a burn-in in simulation: run coupled paths or monitor the accumulated log product. It is more directly connected to forgetting the initial condition than judging whether a sample mean of variance appears stable. The latter can be particularly unreliable when the theoretical mean does not exist.

Nondegeneracy of the stationary law follows because a fixed positive solution would require $v=\omega+(\beta+\alpha z_t^2)v$ almost surely. With $\alpha>0$ and nondegenerate $z_t^2$, that equality cannot hold for one fixed finite $v$. The exceptional deterministic-scale cases excluded by the assumptions should therefore not be treated as counterexamples to the theorem's random-law statement.

## IGARCH: a stationary law with infinite variance

Under $E[z_t^2]=1$, IGARCH imposes $\alpha+\beta=1$. Because $A_t$ is nondegenerate and logarithm is strictly concave,

$$
E[\log A_t]<\log E[A_t]=0.
$$

This puts IGARCH inside the strict-stationarity region. If $\omega=0$ and $E[V_0]<\infty$, $V_t$ is a nonnegative martingale that converges almost surely to zero, while $E[V_t]=E[V_0]$ at every finite time. The expectation cannot be interchanged with the almost-sure limit. Rare, very large values maintain the expectation while typical paths shrink.

With $\omega>0$, the conditional forecast is

$$
E[V_{t+k}\mid V_t]=V_t+k\omega.
$$

The forecast mean increases linearly even though the stationary construction is strictly stationary and ergodic. The resolution is that the stationary mean of $V_t^*$ is infinite. Conditional expectations from a finite current state are finite at each finite horizon; the unconditional expectation under the invariant distribution is not. Neither fact contradicts the other.

A finite unconditional return variance would require $E[V_t^*]<\infty$, since the current unit-variance innovation is independent of its past-determined scale. IGARCH fails that condition. Thus covariance stationarity is absent even though strict stationarity holds. Classical standard errors or risk measures requiring second or fourth moments cannot be justified merely by observing a stationary simulated histogram.

The paper gives an even stronger counterexample to expectation-based intuition. With normal innovations, $\beta=0$, $\alpha=3$, and $\omega=0$,

$$
V_t=3z_{t-1}^2V_{t-1},\qquad E[V_t]=3^tE[V_0].
$$

Yet $E[\log(3z^2)]<0$, so $V_t\to0$ almost surely. Adding any positive $\omega$ produces a strictly stationary positive-scale model with infinite mean. The coefficient sum exceeds one by a wide margin; that alone does not determine strict stationarity.

## Arbitrary moments and the correct moment order

Let

$$
q(p)=E[A_t^p]=E[(\beta+\alpha z_t^2)^p],\qquad p>0.
$$

For $\omega>0$ in the stationary region, the corollary to Theorem 3 states

$$
E[(V_t^*)^p]<\infty\quad\Longleftrightarrow\quad q(p)<1.
$$

The distinction between scale-squared and return moments is crucial. Since $\varepsilon_t^*=\sqrt{V_t^*}z_t$ and the two factors are independent,

$$
E[|\varepsilon_t^*|^{2p}]=E[(V_t^*)^p]E[|z_t|^{2p}].
$$

Thus $p=1$ concerns the return second moment, $p=2$ its fourth moment, and $p=1/2$ its first absolute moment. Existence of a formal symmetric distribution does not by itself establish a well-defined mean: absolute integrability is needed to avoid an undefined difference of infinite positive and negative parts.

For a finite-time conditional process, moment existence also depends on the starting law. The paper distinguishes three questions: finiteness at each fixed date, boundedness uniformly over dates, and convergence to a stationary moment. With $E[V_0^p]<\infty$, fixed-date finiteness requires $q(p)<\infty$, whereas a finite stationary $p$th moment requires the stronger inequality $q(p)<1$. If the latter holds, conditional moments converge to the stationary moment. When $q(p)\geq1$, the stationary moment is infinite and finite-time moments can diverge as the horizon grows.

Theorem 3 proves these results with explicit bounds. For $0<p\leq1$, writing $q=q(p)$,

$$
\omega^p\left(\sum_{k=0}^{\infty}q^{k/p}\right)^p
\leq E[(V_t^*)^p]\leq
\omega^p\sum_{k=0}^{\infty}q^k.
$$

For $p\geq1$, the inequality directions reverse. The two sums converge exactly when $q<1$, giving necessity as well as sufficiency. These bounds arise from Minkowski-type inequalities applied to the positive series; they do not require integer moments. Negative moments are finite when $\omega>0$ because the scale is bounded away from zero after the first conditional step and in the stationary construction.

Theorem 4 gives a useful margin result. If the process is in the negative-log-growth region and the innovations have some finite positive absolute moment, then the stationary scale has some finite positive, possibly fractional moment. If a particular moment condition is strict and the innovations have a higher finite moment, there is a small additional positive margin in the admissible order. This matters for limit theorems that require $1+\delta$ or $2+\delta$ rather than exactly the first or second moment.

## Persistence depends on the perturbation and the convergence criterion

Section 2, pp. 323–325, defines persistence by decomposing future variance into a part containing a fixed past shock and a remainder. It considers almost-sure convergence, convergence in probability, and convergence of positive absolute moments. These are not interchangeable.

For standardized shocks $z_t$, the relevant propagated component contains products of future $A$ multipliers. Within the stationary region, that component disappears almost surely and in probability. Its $p$th moment disappears only under $q(p)<1$, with appropriate initial moments for a conditional model. In a stationary IGARCH model, concavity gives $q(p)<1$ for $0<p<1$, while $q(1)=1$ and convexity gives $q(p)>1$ for larger admissible orders. The same shock can therefore disappear along paths and in low-order moments while remaining persistent in first and higher moments of variance.

For unstandardized shocks $\varepsilon_t$, an algebraic expansion instead isolates a direct term proportional to

$$
\alpha\beta^{m-1}\varepsilon_t^2
$$

in $V_{t+m}$. Holding the later observed innovations in that representation fixed leads to a direct-effect decay criterion governed by $\beta$, not $\alpha+\beta$. The bracketed remainder is not independent of the selected $\varepsilon_t$, unlike the corresponding decomposition using standardized innovations. This is why the two definitions answer different questions; neither should be called the unique impulse response without specifying what future quantities are held fixed.

Under the standard innovation normalization, the familiar conditional-mean forecast is

$$
E[V_{t+m}\mid V_t]=V_t(\alpha+\beta)^m+\omega\sum_{k=0}^{m-1}(\alpha+\beta)^k.
$$

Its initial-state term disappears when $\alpha+\beta<1$. This is persistence in the forecast mean, not a test for existence of the whole forecast distribution or for pathwise forgetting. A volatility half-life calculated from $\alpha+\beta$ is meaningful only for that particular expected-variance response, and the usual positive finite formula does not extend to an infinite-mean stationary law.

## Normal and Cauchy examples that make the criteria computable

Theorem 6 expresses the log-growth and power expectations through special functions. A numerical implementation can alternatively integrate their defining one-dimensional expectations. For normal innovations and $\beta=0$, the closed forms simplify to

$$
\gamma=\log(2\alpha)+\psi(1/2),\qquad
q(p)=\frac{(2\alpha)^p\Gamma(p+1/2)}{\sqrt\pi}.
$$

Here $\psi(1/2)\approx-1.96351$ is the digamma value. The strict-stationarity threshold is therefore $\alpha<\exp[-\psi(1/2)]/2\approx3.562$. In contrast, a finite return variance requires $\alpha<1$, and a finite fourth moment requires $3\alpha^2<1$. These calculated thresholds expose the large region between a finite stationary distribution and finite moments of practical interest.

For general nonnegative $\beta$ under normal innovations, $q(1)=\alpha+\beta$ and

$$
q(2)=3\alpha^2+2\alpha\beta+\beta^2.
$$

The four regions in Figure 1 distinguish failure of the finite stationary construction, stationary returns without a first absolute moment, stationary returns with a mean but infinite variance, and the covariance-stationary region. These are model regions determined by population integrals, not confidence regions for estimated coefficients.

For standard Cauchy innovations,

$$
\gamma=2\log(\sqrt\beta+\sqrt\alpha).
$$

The stationary-scale region is $\sqrt\beta+\sqrt\alpha<1$. With $\beta=0$, $q(p)=\alpha^p/\cos(\pi p)$ for $0<p<1/2$, while $q(p)=\infty$ for $p\geq1/2$. Stationarity of scale does not rescue the return mean or variance, because the contemporaneous Cauchy innovation has neither. Figure 2 illustrates the stationary-scale boundary without counterparts to the normal case's finite-return-mean and finite-return-variance regions.

## Reproducing the IGARCH density illustration

Figure 3 on p. 329 plots densities of $X=\log V^*$ for normal-innovation IGARCH. The specified values are $\alpha=1,0.75,0.5,0.25,0.1$, $\beta=1-\alpha$, $\omega=\alpha$, and $V_0=1$. The common lower stationary support is one, so $X$ has support above zero. The recursion is

$$
V_t=\alpha+\bigl(1-\alpha+\alpha z_{t-1}^2\bigr)V_{t-1},\qquad z_t\sim N(0,1).
$$

The appendix uses $T=5,000$ to approximate a stationary draw by $V_T$. It reports that the initial-condition multiplier was typically extremely small, on the order of $10^{-40}$ for the selected cases. This is an empirical check from the simulation, not a uniform deterministic error guarantee or a probability bound valid for every draw.

For each parameter case, the density estimate uses 7,000 draws of the terminal scale. The paper names the GAUSS normal random-number generator. It does not provide a seed or enough random-stream details to duplicate the exact plotted lines. An explicit reconstruction can generate independent paths of length 5,000 for the 7,000 terminal draws, recording that path-independence convention as an implementation choice.

The smoothing is performed on $Y=\log(\log V_T)$, which has unbounded real support, rather than directly on positive $X=\log V_T$. A Gaussian kernel uses bandwidth

$$
h=0.9\,\min\left(s_Y,\frac{\operatorname{IQR}(Y)}{1.34}\right)n^{-1/5},\qquad n=7,000.
$$

After estimating $f_Y$, transform back using $f_X(x)=f_Y(\log x)/x$ for $x>0$. The Jacobian is necessary. The plotted bandwidths, in descending $\alpha$ order, are approximately 0.23, 0.14, 0.11, 0.08, and 0.06. Doubling or halving the bandwidth reportedly makes little difference to the qualitative densities.

The figures illustrate frequent extreme scale values and different shapes as $\alpha$ changes. They do not estimate a finite population mean, compare investment performance, or establish a tail-index estimator. Since $\omega$ scales the stationary variance distribution, changing it shifts the distribution of $\log V^*$ without changing its shape. Retaining this normalization is necessary to reproduce the cross-parameter display.

## Implementation consequences and limits

A faithful implementation should evaluate both $\gamma$ and the moment-specific $q(p)$ required by its downstream calculation. It should distinguish a finite positive starting value from initialization in the invariant distribution, preserve common innovations when measuring contraction, and avoid using an infinite theoretical mean as a numerical initialization target. For high persistence, convergence of sample moments can be much slower or fail entirely even when pathwise initialization error becomes tiny.

The paper supplies no estimation uncertainty for these criteria because it is not an empirical estimation study. With fitted parameters, uncertainty near $\gamma=0$ or $q(p)=1$ becomes an additional problem, and a point estimate on one side of a boundary is not evidence that the true process lies there with certainty. Innovation misspecification can change both expectations even when the reported $\alpha$ and $\beta$ are unchanged.

The practical contribution is to attach each conclusion to its precise mathematical object: a stationary law, a finite moment, a forecast mean, or a pathwise shock effect. Nelson's results explain why those objects can disagree without contradiction. That discipline is essential whenever GARCH output is used in inference, long-horizon simulation, or risk decisions whose validity depends on moments that the fitted process may not possess.

# Integrated volatility and round-off error

Mathieu Rosenbaum. *Bernoulli* 15(3), August 2009, 687–720. DOI: 10.3150/08-BEJ170. [Source PDF](../../Finance/RealizedVariance_Rosenbaum_2009.pdf). The supplied file has 35 pages: a JSTOR cover followed by the complete 34-page article. Printed page 687 is PDF page 2. All pages, including the proofs and bibliography, were read. Page references below use the printed pagination.

## Why this matters

The paper studies a specific source of microstructure error: a continuous efficient price is observed only after rounding down to a discrete price grid. This error is determined by the latent price, has a nonzero conditional mean, and is serially dependent. Treating it as independent additive observation noise loses the mechanism that drives the estimation problem. When the tick size is large compared with a typical sampled price move, most observed increments vanish; the surviving moves are mainly one tick. Squaring these increments then measures essentially the same crossing activity as taking their absolute values, rather than recovering the efficient price's quadratic variation.

Rosenbaum constructs estimators of weighted integrated variance by first estimating local averages of volatility with absolute rounded increments, then squaring those local averages using a Haar decomposition. A second estimator compensates for the omitted fine-scale wavelet energy and for a signed bias introduced by evaluating a nonconstant weight at rounded prices. The resulting stable central limit theorems cover three relations between tick size and observation frequency. Their common error scale is the larger of the tick size and the ordinary diffusion sampling scale.

This is an estimation theory paper. It contains no market-data application, simulation study, performance table, trading strategy, transaction-cost calculation, or finite-sample coverage result. Its numerical constants are asymptotic constants, not empirical improvements. The useful contribution for a quant researcher is a coherent way to exploit the structure of rounding, together with a warning that standard quadratic-variation intuition can fail even without independently added noise.

## Model, target, and scope

On the fixed observation interval $[0,1]$, the latent price satisfies

$$
dX_t=\sigma(X_t)\,dW_t+a_t\,dt,\qquad X_0=x_0.
$$

$W$ is a Brownian motion, $a_t$ is a progressively measurable drift, and $\sigma$ is an unknown deterministic function of the current price. The observed sample consists of $n+1$ equally spaced rounded prices

$$
Y_i=\alpha_n\left\lfloor X_{i/n}/\alpha_n\right\rfloor,
\qquad i=0,\ldots,n,
\qquad \alpha_n\downarrow0.
$$

The rounding convention is floor rounding, including for negative values. It is not rounding to the nearest tick. In particular $Y_i-X_{i/n}\in[-\alpha_n,0]$. Changing that convention can change the bias terms. The paper does not include an additional bid–ask component, independent measurement noise, asynchronous sampling, price jumps, or market closures.

The parameter of interest is

$$
\theta=\int_0^1 g(X_s)^2\sigma(X_s)^2\,ds,
$$

where $g$ is known. With $g=1$, this is integrated variance in price-squared units. With $g(x)=1/x$ on a positive price domain, it is the integrated squared diffusion coefficient of log price. The paper calls these absolute and relative integrated volatility, respectively; neither target is the square root of the displayed integral. A unit of calendar time other than the source's unit interval requires an explicit time normalization.

Write

$$
\beta_n=\alpha_n\sqrt n,\qquad
r_n=\max(\alpha_n,n^{-1/2}).
$$

The first quantity selects the asymptotic regime; the second gives the convergence rate. Locally, the actual tick-to-move ratio also depends on $\sigma(X_t)$: a typical efficient move has size $\sigma(X_t)/\sqrt n$. Thus the same $\beta_n$ need not mean the same practical degree of discreteness across price processes with different scales.

Assumption B requires that $X$ stay in an open interval $(\nu,\mu)$, that $\sigma$ be strictly positive and twice continuously differentiable there, and that $\int_0^1a_s^2ds$ be finite almost surely. The interval can be unbounded. Assumption C requires positive, twice continuously differentiable $g$. For the central limit theorem, C1 additionally requires $g'$ to have a constant sign and $|g'|^{1/2}$ to be twice continuously differentiable. A constant $g$ is allowed; its derivative correction vanishes. The paper extends $g$ and $g'$ by zero outside the price interval for evaluating the stated formulas.

The tick-size assumptions are stronger than merely $\alpha_n\to0$. The rate result assumes

$$
\sup_n\alpha_n(\log n)^2<\infty.
$$

The central limit theorem assumes that for some $\rho>0$,

$$
\sup_n\alpha_n^{1-\rho}(\log n)^2<\infty.
$$

An admissible $\rho$ can be taken below one. Polynomially decreasing ticks satisfy these restrictions. They do not authorize a fixed-tick, increasing-frequency consistency claim. Section 3.1 expressly distinguishes the shrinking-tick framework from pure rounding with a constant tick.

The introductory discussion begins with a general Itô process, but the proved central limit theorem uses $\sigma(X_t)$. A separate stochastic volatility factor is outside this theorem. Section 3.1 explains that the proof needs a representation of the price as a function of Brownian motion after a change of probability. It mentions an extension of the rate result to separable time dependence $\sigma(x,t)=g_1(x)g_2(t)$, with positive $g_1\in C^2$ and $g_2\in C^1$. That statement is not a general stochastic-volatility central limit theorem.

## Why absolute increments survive rounding

The exact increment identity behind the method is equation (3), p. 695:

$$
Y_i-Y_{i-1}
=\alpha_n\left\lfloor
\{X_{(i-1)/n}/\alpha_n\}
+\frac{X_{i/n}-X_{(i-1)/n}}{\alpha_n}
\right\rfloor,
$$

where braces denote fractional part. Smooth density estimates allow the fractional part to behave approximately as a uniform phase when averaged appropriately. This does not make the sequence of rounding errors independent.

For an independent uniform $U$ on $[0,1]$ and an integrable random variable $Z$, the elementary identity

$$
\mathbb E|\lfloor U+Z\rfloor|=\mathbb E|Z|
$$

explains the special role of absolute increments. Conditional on any fixed real $z$, the two possible integer values of $\lfloor U+z\rfloor$ have the correct weighted average absolute magnitude $|z|$. Under local Gaussian diffusion scaling, therefore,

$$
\frac{\sqrt{\pi/2}}{\sqrt n}\sum_{i=1}^n|Y_i-Y_{i-1}|
\quad\hbox{estimates}\quad
\int_0^1\sigma(X_s)\,ds.
$$

This quantity estimates integrated volatility in the unsquared sense. Squaring the single full-period average would generally yield $(\int\sigma)^2$, not $\int\sigma^2$. The local decomposition is essential.

Section 3.2 also recalls the large-$\beta_n$ behavior of general power variations. In that regime, for $p>0$, their leading scaled limit is

$$
\frac{\alpha_n^{1-p}}{\sqrt n}
\sum_{i=1}^n|Y_i-Y_{i-1}|^p
\;\longrightarrow\;
\sqrt{\frac2\pi}\int_0^1\sigma(X_s)\,ds.
$$

The limit involves $\sigma$, not $\sigma^p$. At $p=2$, this implies that realized variance divided by $\alpha_n\sqrt n$ approaches $\sqrt{2/\pi}\int\sigma$. When $\beta_n\to\infty$, ordinary realized variance is consequently on the wrong scale for estimating $\theta$ with $g=1$. This conclusion follows from the paper's recalled variation result; it is not an empirical variance-signature estimate.

In the large-tick interpretation, a move exceeding several ticks in a single sampling interval is uncommon. Hence $|\Delta Y|^p$ is close to $\alpha_n^{p-1}|\Delta Y|$ for the moves that occur. Using ever higher powers does not manufacture the missing local information about $\sigma^p$. The estimator instead recovers $\sigma$ over short time blocks and combines the blocks quadratically.

## The basic Haar estimator

Let $I_{jk}=(k2^{-j},(k+1)2^{-j}]$ for $k=0,\ldots,2^j-1$. Use the source's Haar convention

$$
\psi(u)=-1_{(0,1/2]}(u)+1_{(1/2,1]}(u),
\qquad
\psi_{jk}(s)=2^{j/2}\psi(2^js-k).
$$

Define $f_s=g(X_s)\sigma(X_s)$ and its scaling and wavelet coefficients

$$
c_{jk}=2^{j/2}\int_{I_{jk}}f_s\,ds,
\qquad
d_{jk}=\int_0^1\psi_{jk}(s)f_s\,ds.
$$

Parseval's identity gives, for any nonnegative integer $j$,

$$
\theta=\sum_{k=0}^{2^j-1}c_{jk}^2+
\sum_{\ell=j}^{\infty}\sum_{k=0}^{2^\ell-1}d_{\ell k}^2.
$$

The observed scaling coefficient is

$$
\widehat c_{jk}
=\sqrt{\frac\pi2}\frac{2^{j/2}}{\sqrt n}
\sum_{i=1}^n1_{I_{jk}}(i/n)\,
g(Y_{i-1})\,|Y_i-Y_{i-1}|.
$$

The weight uses the rounded price at the beginning of the increment. The block is selected using the increment's ending time. These conventions matter at boundaries and for the bias correction.

Set

$$
j_{0,n}=\left\lfloor\log_2(\alpha_n^{-1}\wedge\sqrt n)\right\rfloor
=\left\lfloor\log_2r_n^{-1}\right\rfloor,
\qquad
\widetilde\theta_n=\sum_{k=0}^{2^{j_{0,n}}-1}\widehat c_{j_{0,n},k}^2.
$$

Theorem 1, pp. 690–691, states that $r_n^{-1}(\widetilde\theta_n-\theta)$ is tight under A, B, and C. Equivalently, the error is $O_P(r_n)$. The localized proof obtains an $L^1$ bound, but the general theorem is presented as tightness. This is not a finite-sample confidence interval, an unbiasedness result, or a minimax lower bound.

The rate emerges from competing errors. Individual coefficient mean-squared errors are bounded by a constant times $r_n^2$. Summing over $2^j$ coefficients creates a squared-estimation contribution of order $2^jr_n^2$. The unobserved fine-scale energy is of order $2^{-j}$. With $2^j$ of order $r_n^{-1}$, both terms are of order $r_n$, as is the leading cross-product fluctuation. Choosing much finer blocks adds estimation noise; much coarser blocks omit too much within-block variation.

The basic estimator is nonnegative and computationally simple. It requires the tick size, the observation count, and the known weight, but no fitted parametric volatility function. It does not solve an optimization problem or fit a likelihood. Its resolution is prescribed asymptotically; the paper gives no finite-sample tuning rule that minimizes mean-squared error on market data.

## Compensation and the estimator with a central limit theorem

The basic balancing choice leaves squared coefficient errors and omitted wavelet energy at the same order as the limiting fluctuation. For a central limit theorem, Rosenbaum chooses a coarser main resolution so squared estimation error becomes negligible, then estimates the omitted energy through a second, still coarser pilot resolution.

Write $S=(a,j_{1,n},j_{2,n})$, with $0<a<1$. The source's admissible class in Section 2.4 imposes all the following conditions:

$$
\sup_n\alpha_n^{1-a}(\log n)^2<\infty,
\qquad
r_n2^{2j_{2,n}-j_{1,n}}\to0,
$$

$$
r_n^{-1}2^{j_{1,n}/2}
\big(\alpha_n^2\log n+n^{-1}\big)\to0,
\qquad
r_n2^{j_{1,n}}\to0,
$$

$$
r_n^{-1}2^{-3j_{1,n}/2}\to0,
\qquad
2^{j_{2,n}-j_{1,n}}\to0,
\qquad
r_n^{-1}2^{-(j_{1,n}+j_{2,n}/2)}\to0.
$$

A concrete source-provided choice is

$$
j_{1,n}=\lfloor\log_2r_n^{-3/4}\rfloor,
\qquad
j_{2,n}=\lfloor\log_2r_n^{-2/3}\rfloor,
$$

with an admissible $a$ from the stronger tick assumption. These are asymptotic prescriptions. At small sample sizes, flooring can make the two resolutions equal; that does not contradict their asymptotic separation, but it can undermine the pilot interpretation in finite samples.

Estimate the pilot wavelet coefficients and energy by

$$
\widehat d_{jk}
=\sqrt{\frac\pi2}\frac1{\sqrt n}
\sum_{i=1}^n\psi_{jk}(i/n)g(Y_{i-1})|Y_i-Y_{i-1}|,
\qquad
\widehat Q_j=\sum_k\widehat d_{jk}^2.
$$

For $J_n=\lfloor(1+a)\log_2r_n^{-1}\rfloor$, the tail compensator is

$$
R_n(S)=\sum_{j=j_{1,n}}^{J_n}
2^{j_{2,n}-j}\widehat Q_{j_{2,n}}.
$$

Only one pilot energy is estimated. The finer levels are extrapolated geometrically; the procedure does not estimate every high-frequency wavelet separately. For implementation, the same quantity can be calculated as

$$
R_n(S)=
2^{j_{2,n}-j_{1,n}+1}
\left[1-2^{-(J_n-j_{1,n}+1)}\right]\widehat Q_{j_{2,n}},
$$

when $J_n\ge j_{1,n}$. This closed form is a derived geometric-sum identity, not an additional estimator proposed by the author.

For nonconstant $g$, a second correction uses

$$
\widehat e_{j_{0,n},k}
=\sqrt{\frac\pi2}\frac{2^{j_{0,n}/2}}{\sqrt n}
\sum_{i=1}^n1_{I_{j_{0,n},k}}(i/n)
|g(Y_{i-1})g'(Y_{i-1})|^{1/2}|Y_i-Y_{i-1}|.
$$

Let $s_g=1$ when $g'$ is nonnegative and $s_g=-1$ when it is negative. Since the derivative has constant sign, this is a single sign, not an observation-specific trading signal. The final estimator, p. 692, is

$$
\widehat\theta_n(S)
=\sum_{k=0}^{2^{j_{1,n}}-1}\widehat c_{j_{1,n},k}^2
+R_n(S)
+\alpha_ns_g\sum_{k=0}^{2^{j_{0,n}}-1}
\widehat e_{j_{0,n},k}^2.
$$

For $g=1$, the final term is zero. For relative variance with $g(x)=1/x$ on positive prices, $g'<0$, the auxiliary increment weight is $x^{-3/2}$, and the correction is subtracted. The uncorrected weighted estimator has a first-order bias of $-\alpha_n\int gg'\sigma^2$, so the sign follows the floor-rounding convention. A nearest-tick convention cannot be substituted without revisiting this calculation.

The signed correction also means that nonnegativity is no longer mechanically guaranteed for every finite sample and every decreasing $g$. Truncating at zero would be an implementation modification, not part of the reported formula. The source does not measure how often this issue arises.

## Stable limits and the variance normalization issue

Theorem 2, pp. 692–693, gives stable convergence to stochastic integrals against a Brownian motion $B$ independent of the original filtration. Conditionally on the latent path these limits are normal, with random path-dependent variances. Stable convergence preserves joint convergence with original-data quantities and is stronger than an isolated marginal central limit theorem.

For negligible rounding, $\beta_n\to0$,

$$
\sqrt n(\widehat\theta_n-\theta)
\;\longrightarrow_{\mathrm{st}}\;
\sqrt{2(\pi-2)}\int_0^1g(X_t)^2\sigma(X_t)^2\,dB_t.
$$

Its conditional variance is $2(\pi-2)\int g^4\sigma^4$. The constant is approximately $2.283185$. For comparison, the usual noise-free realized-variance constant for the corresponding continuous diffusion target is $2$. Thus the absolute-variation construction has a limiting variance multiplier $\pi-2\approx1.141593$ relative to that benchmark in the negligible-rounding regime. This 14.1593% difference is derived from the theorem constants, not a measured forecasting or portfolio-performance loss.

For intermediate rounding, $\beta_n\to\beta\in(0,\infty)$,

$$
\sqrt n(\widehat\theta_n-\theta)
\;\longrightarrow_{\mathrm{st}}\;
2\int_0^1g(X_t)^2\sigma(X_t)
\sqrt{\Delta_\beta(X_t)}\,dB_t.
$$

The corresponding conditional variance is $4\int g^4\sigma^2\Delta_\beta$. This regime retains the dependence structure of rounded Brownian increments through a long-run variance function.

For dominant rounding, $\beta_n\to\infty$,

$$
\alpha_n^{-1}(\widehat\theta_n-\theta)
\;\longrightarrow_{\mathrm{st}}\;
\frac2{\sqrt3}\int_0^1g(X_t)^2\sigma(X_t)\,dB_t,
$$

with conditional variance $\frac43\int g^4\sigma^2$. Here the estimator's error scale is the tick size. Increasing $n$ while retaining a practically large tick need not deliver the improvement suggested by a noise-free $\sqrt n$ calculation.

For example, with $\alpha_n=c n^{-\kappa}$, the theorem's rate is $n^{-\min(\kappa,1/2)}$ up to the scale constant. The three regimes correspond to $\kappa>1/2$, $\kappa=1/2$, and $0<\kappa<1/2$. These are derived classifications of the theoretical sequence, not recommended sampling frequencies.

There is a printed normalization problem in the definition of $\Delta_\beta$ on p. 692. With $U$ uniform and independent of Brownian motion, define the stationary-phase increments

$$
Z_i=
\beta\sqrt{\frac\pi2}
\left|
\left\lfloor
\{U+\beta^{-1}\sigma(x)W_{i-1}\}
+\beta^{-1}\sigma(x)(W_i-W_{i-1})
\right\rfloor
\right|-\sigma(x).
$$

The printed formula places $n^{-1/2}$ outside $(\sum_{i=1}^nZ_i)^2$ inside the expectation. The standard variance normalization consistent with a $\sqrt n$ central limit theorem is instead

$$
\Delta_\beta(x)
=\lim_{m\to\infty}
\mathbb E\left[
\left(m^{-1/2}\sum_{i=1}^mZ_i\right)^2
\right]
=\lim_{m\to\infty}\frac1m
\mathbb E\left[\left(\sum_{i=1}^mZ_i\right)^2\right].
$$

This note uses that long-run variance interpretation when explaining the intermediate-regime theorem. It is a mathematically motivated reconstruction, not a verified publisher erratum. If partial-sum variance grows linearly, the printed $m^{-1/2}$ multiplier would make the expression grow as $\sqrt m$, rather than converge to the required finite variance. Lemma 12 on p. 717 uses $\Delta_\beta$ in a $\sqrt n$ limit and refers to Delattre's variation limit results, reinforcing the variance interpretation without explicitly repairing the displayed definition.

Where autocovariances are summable, the reconstructed quantity is also $\operatorname{Var}(Z_1)+2\sum_{h\ge1}\operatorname{Cov}(Z_1,Z_{1+h})$. Replacing it by a single-increment variance would discard the rounded-phase dependence. The paper supplies neither a numerical lookup table for this function nor an implemented studentization procedure. A feasible confidence interval therefore needs additional consistent variance estimation and its justification; a mixed-normal limit alone does not provide a calibrated standard error from an observed sample.

## What the proof establishes

The main proof has three distinct tasks: control fractional-phase sampling error, reconstruct the unobserved wavelet tail, and isolate a stable limiting martingale term. These tasks explain both the estimator and its restrictive assumptions.

First, Section 4.1 localizes the diffusion to regions where the volatility and weight have bounded derivatives and the volatility is bounded away from zero. It also stops paths with excessive drift energy. The probability of leaving the localized model tends to zero as the localization expands. A Girsanov change of probability then replaces the drift by $\frac12\sigma\sigma'$. Under this representation,

$$
X_t=h(W_t),\qquad
h(w)=S^{-1}(w+S(x_0)),\qquad
S(x)=\int_0^x\frac{dy}{\sigma(y)}.
$$

The transition density is explicitly

$$
p_t(x,y)=\frac1{\sigma(y)\sqrt{2\pi t}}
\exp\left[-\frac{(S(y)-S(x))^2}{2t}\right].
$$

Its derivative bounds support averaging over the fractional part of $X/\alpha_n$. The probability change is a proof device, not a risk-neutral pricing assumption or a proposal to estimate an economic drift.

Second, Proposition 1 on p. 698 considers sampling functions of the current price, fractional phase, and rescaled increment. Gaussian and uniform-phase averaging define an operator $M$. For the unweighted absolute increment function

$$
f_n(x,u,y)=\sqrt{\pi/2}\,\beta_n
|\lfloor u+\beta_n^{-1}y\rfloor|,
$$

the identity above gives $Mf_n(x)=\sigma(x)$. The proposition bounds each local sampling coefficient's mean-squared approximation error by $Cr_n^2$, uniformly over resolutions up to $\lfloor\log_2r_n^{-1}\rfloor$. The stronger tick assumption extends the allowed resolution range. Its proof decomposes the error into a martingale, a Gaussian-transition approximation, a Riemann error, and terms controlling the serial dependence of the fractional phase. Independent-error arguments would not supply the same result.

Lemma 5 gives $\mathbb E[d_{jk}^2]\le C2^{-2j}$, hence total energy at resolution $j$ is of order $2^{-j}$. Together with the coefficient bounds and a separate bound on the cross-product, this proves the basic rate. One cannot obtain that rate merely by taking Cauchy–Schwarz over every coefficient; the martingale structure is used to avoid an unnecessarily loose cross-term bound.

Third, consider the exact decomposition at the main resolution:

$$
\sum_k\widehat c_{jk}^2-\theta
=\sum_k(\widehat c_{jk}-c_{jk})^2
+2\sum_kc_{jk}(\widehat c_{jk}-c_{jk})
-\sum_{\ell\ge j}Q_\ell,
\qquad Q_\ell=\sum_kd_{\ell k}^2.
$$

At $j=j_{1,n}$, $2^jr_n\to0$ makes the first term negligible after division by $r_n$. The third term is too large to ignore. Lemmas 7–8 exploit the near-geometric scale behavior of wavelet energy to estimate it with $R_n(S)$.

Lemma 7's notation needs care. Earlier $h$ represents the price transformation $X=h(W)$, but $d_{jk}$ are coefficients of $g(X)\sigma(X)$. Its displayed limiting energy on p. 707 uses $h'(W)^2$. For consistency, the $h$ in that lemma must be reinterpreted as the transformed volatility function

$$
H(w)=(g\sigma)(h(w)),
$$

which is $\sigma(h(w))$ in the unweighted proof. With this interpretation the wavelet-energy relation is

$$
2^jQ_j\approx c(\psi)\int_0^1H'(W_u)^2\,du,
\qquad
c(\psi)=\int_0^1\left(\int_0^u\psi(v)\,dv\right)^2du=\frac1{12}.
$$

The constant $1/12$ is directly calculated for the displayed Haar function. The lemma gives an $L^1$ approximation bound of order $2^{-j/2}$. Reading its $h$ literally as the earlier price transformation cannot work: with constant $\sigma$ and $g=1$, every volatility wavelet coefficient is zero, while the earlier $h'$ equals the nonzero constant $\sigma$. This is a function-notation ambiguity in the scaling argument, not evidence that the compensator theorem is false. The estimator uses ratios of energies across scales and does not require direct estimation of $H'$.

Lemma 8 controls the extrapolation error by terms of orders

$$
2^{-3j_1/2},\quad
2^{-(j_1+j_2/2)},\quad
2^{2j_2-j_1}r_n^2,\quad
2^{j_2-j_1}r_n,
$$

and the tail beyond $J_n$ is negligible because $a>0$. Dividing these terms by $r_n$ produces the corresponding admissibility restrictions. This shows why the pilot scale must be separated from the main scale and why estimating the omitted coefficients individually would be too noisy.

Finally, Lemmas 9–11 remove volatility-freezing and Riemann remainders. Lemma 12 obtains the stable limit of $C_j=\sum_kc_{jk}(\widehat c_{jk}-c_{jk})$ by applying the rounded-variation limit theory to the remaining term. The factor two in the estimator decomposition produces the theorem's final constants. For general $g$, Lemma 13 identifies an additional drift in the limit: $-\frac12\int gg'\sigma^2$ after scaling $C_j$ by $\alpha_n^{-1}$ in the dominant-rounding regime, or the same expression multiplied by $\beta$ under $\sqrt n$ scaling in the intermediate regime. Meanwhile $\sum_k\widehat e_{j_0,k}^2$ converges to $\int|gg'|\sigma^2$. These two statements explain the signed correction exactly.

## Reimplementation and evidence still needed

A faithful implementation begins with a single regularly sampled price path and a known tick size in the same units as the prices. Keep zero increments: dropping them changes the sampling scheme and destroys the normalization. Calculate absolute price increments before applying the lagged weight. For dyadic block membership, use the right-closed intervals defined above; an observation exactly on a boundary belongs to the preceding block. The source assumes $n2^{-j}$ is an integer for technical convenience in the proofs. Choosing a power-of-two sample count is one clean way to match this convention in a controlled experiment.

For the basic estimator, accumulate weighted absolute increments in the $2^{j_0}$ blocks, multiply each block sum by $\sqrt{\pi/2}\,2^{j_0/2}/\sqrt n$, square, and sum. For the compensated estimator, repeat this operation at $j_1$, calculate signed Haar sums at $j_2$, square and sum those into $\widehat Q_{j_2}$, and apply the geometric multiplier. If $g$ is nonconstant, make one further pass at $j_0$ with weight $|gg'|^{1/2}$ and apply the signed tick correction. These operations can be accumulated in linear time in $n$ for fixed selected resolutions. No regression training window, cross-validation split, or estimated trading signal is part of the procedure.

The source supplies no asset universe, calendar dates, exchange filters, corporate-action adjustments, stale-price rule, treatment of overnight returns, or sampling-frequency selection. Applying it to transaction data would require those choices to be declared and would need evidence that deterministic rounding is an adequate observation model. Splits or changes in tick rules cannot be left inside a supposedly constant-$\alpha_n$ sample without an explicit modification. Log-transforming rounded prices first also does not reproduce the paper's relative-variance estimator: it uses rounded price increments with $g(Y_{i-1})=1/Y_{i-1}$ and a specific correction.

A useful validation design, proposed here rather than reported in the article, would simulate the latent path and retain its integrated-variance truth; impose floor rounding only after sampling; and vary $n$ and $\alpha_n$ jointly to hold each asymptotic regime. Constant volatility provides a basic normalization check, while a positive state-dependent volatility tests omitted wavelet energy. A positive-price model with $g=1/x$ is needed to test the derivative correction. Compare the basic and compensated estimators with ordinary realized variance and with the same statistics on unrounded observations. Report bias, root-mean-squared error, and the distribution of errors under the theorem's appropriate scaling. Monte Carlo standard errors, seeds, path-discretization error, and the definition of truth must be disclosed. None of these numerical outcomes can be inferred from the article.

Further diagnostics should separately change the rounding convention, add independent noise, or introduce a separate stochastic volatility factor. These are tests of model robustness beyond the proved setup, not replications of a theorem that already covers them. In the intermediate regime, a numerical estimate of $\Delta_\beta$ should use a long rounded Brownian phase path or a justified dependence-aware method, record the corrected variance normalization, and assess truncation or simulation error. A one-step Gaussian variance calculation is insufficient.

For inference, the unresolved practical inputs are a feasible conditional-variance estimator, a justified finite-sample choice of resolutions, and demonstrated coverage. For a strategy application, additional inputs would include forecast construction, timing, portfolio constraints, turnover, execution costs, and a validation period. The paper estimates a latent risk quantity on a fixed interval; it does not establish that the quantity forecasts returns or generates a profitable trading rule.

The result's strongest supported interpretation is therefore specific: under shrinking deterministic floor rounding of a smooth local diffusion, absolute-increment wavelet estimators recover weighted integrated variance at rate $\alpha_n\vee n^{-1/2}$, and carefully compensated versions have stable limits with distinct rounding regimes. The source provides enough mathematical structure to implement those estimators, but no evidence for an empirical advantage outside that observation model.

## Source map

Rosenbaum, M. (2009), “Integrated volatility and round-off error,” *Bernoulli* 15(3), 687–720. [Local full source](../../Finance/RealizedVariance_Rosenbaum_2009.pdf).

- Pages 687–689: motivation, observation model, regularity and tick-size assumptions.
- Pages 690–692: Haar coefficients, basic estimator, admissible compensation scales, final bias-corrected estimator, and printed long-run variance definition.
- Pages 692–695: stable limit theorem, scope restrictions, power-variation behavior, fractional-phase explanation.
- Pages 696–705: localization, probability change, sampling-function proposition, martingale decomposition, and proof of the basic rate.
- Pages 706–718: wavelet-tail compensation, limiting cross-product, and general-weight bias correction.
- Pages 719–720: bibliography. Delattre and Delattre–Jacod supply important variation and fractional-part results invoked by the proof; those referenced works were not independently audited for this note.

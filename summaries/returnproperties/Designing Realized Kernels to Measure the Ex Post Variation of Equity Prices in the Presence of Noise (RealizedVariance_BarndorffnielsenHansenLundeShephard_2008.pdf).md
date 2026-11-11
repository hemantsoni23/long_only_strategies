# Designing Realized Kernels to Measure the Ex Post Variation of Equity Prices in the Presence of Noise

Ole E. Barndorff-Nielsen, Peter Reinhard Hansen, Asger Lunde, and Neil Shephard, *Econometrica* 76(6), November 2008, 1481–1536, DOI 10.3982/ECTA6495. [Source PDF](../../Finance/RealizedVariance_BarndorffnielsenHansenLundeShephard_2008.pdf).

## Why this paper matters

At sufficiently high sampling frequencies, squaring observed returns measures trading frictions as well as efficient-price variation. Increasing the number of observations then makes ordinary realized variance worse: independent noise in prices produces negatively correlated noise in returns, and its contribution to realized variance grows with the observation count. This paper constructs an estimator that uses that autocorrelation structure to cancel noise bias and then uses many additional return autocovariances to reduce the variance of the correction.

The contribution is a theory of how the kernel's shape, its bandwidth, and the treatment of endpoints jointly determine statistical performance. Smooth kernels attain the $n^{1/4}$ convergence rate under fixed, independent price noise and general continuous stochastic volatility. Their asymptotic variance can approach the Gaussian constant-volatility likelihood benchmark. The paper supplies feasible noise and quarticity estimates, considers departures from independent noise, and studies both simulation inference and General Electric transaction data.

This is an ex post measurement paper. The target is variation accumulated during an observed interval, rather than a return forecast or a trading rule. Better daily volatility measurements can improve risk models and volatility forecasting inputs, but the empirical application does not establish out-of-sample forecasting gains, transaction-cost savings, or profitable signals. Its robustness extensions also require more care than the independent-noise central limit theorem: consistency under a broader noise model does not automatically justify the original standard errors.

The estimator here is specifically the 2008 **flat-top** realized kernel, with weights $k((h-1)/H)$ and an optimal bandwidth of order $\sqrt n$. It should not be silently replaced by the non-flat positive semidefinite kernel and different bandwidth prescription in the authors' separate 2009 “trades and quotes” paper.

## Observation model and estimation target

For clarity, normalize one estimation interval to $[0,1]$. This removes time-unit factors that appear when the paper works over a general interval $[0,t]$. Let the efficient log price satisfy

$$
dY_s=a_s\,ds+\sigma_s\,dW_s,
\qquad
I=\int_0^1\sigma_s^2\,ds,
\qquad
Q=\int_0^1\sigma_s^4\,ds.
$$

Here $I$ is integrated variance and $Q$ is integrated quarticity. They are random path functionals. The drift is predictable and locally bounded; volatility is càdlàg, with $\sigma^2$ almost surely pathwise positive on every compact interval. For the central limit results the paper imposes a continuous semimartingale structure on volatility, with both a component driven by $W$ and an independent Brownian component. Its volatility coefficients are adapted and càdlàg, and the volatility drift is additionally predictable and locally bounded. This accommodates leverage, meaning correlation between price and volatility innovations. The main theory does not assume constant volatility or a finite-dimensional volatility model.

Observed log prices are $X_s=Y_s+U_s$. In the basic model, noise at distinct observation times is independent and independent of the efficient-price process, with

$$
E[U_s]=0,\qquad E[U_s^2]=\omega^2,\qquad
\operatorname{Var}(U_s^2)=\lambda^2\omega^4.
$$

The fourth moment is finite; Gaussian noise has $\lambda^2=2$. The noise assumption concerns **price levels**, not returns. With equally spaced observations at $\delta=1/n$, the noise return is $U_{j\delta}-U_{(j-1)\delta}$, an MA(1) sequence with variance $2\omega^2$ and lag-one covariance $-\omega^2$. Consequently, the noise contribution to ordinary realized variance has mean $2n\omega^2$.

Write $r_j=X_{j\delta}-X_{(j-1)\delta}$ and define the unnormalized, non-demeaned realized autocovariances

$$
\gamma_h(X)=\sum_{j=1}^n r_jr_{j-h}.
$$

This definition uses returns outside the target interval when $h\ne0$. In particular, $\gamma_h$ and $\gamma_{-h}$ are not identical finite-sample quantities under the paper's endpoint convention. An implementation that simply replaces their sum by twice an in-sample, truncated autocovariance has changed the estimator. The paper also discusses discarding observations near the boundaries and rescaling, but exact boundary choices must be recorded in a replication.

For an integer bandwidth $H$ and a kernel with $k(0)=1$, $k(1)=0$, the realized kernel is

$$
K(X)=\gamma_0(X)+
\sum_{h=1}^{H}k\!\left(\frac{h-1}{H}\right)
\{\gamma_h(X)+\gamma_{-h}(X)\}.
$$

The first autocovariance pair receives weight exactly one. This cancels the $2n\omega^2$ noise mean against the two lag-one contributions. The higher-lag noise autocovariances have zero means, yet are valuable because their covariance with the correction can reduce its variance. Bias cancellation alone is insufficient: using only the first lag leaves noise variance that grows with $n$. Without noise, adding the first-lag correction also raises the asymptotic variance of ordinary realized variance from $2Q$ to $6Q$ at the usual $\sqrt n$ scaling. Thus the correction has an explicit statistical cost when contamination is negligible.

Unlike an estimator constructed from a positive semidefinite covariance window, this flat-top estimator need not be nonnegative in finite samples. The paper truncates negative estimates at zero in its numerical work and reports fewer than 25 such occurrences in millions of simulated estimates using its principal Tukey–Hanning kernel. It does not give a precise denominator for that statement.

## Endpoints, kernel smoothness, and the variance decomposition

The paper “jitters” the two endpoints by replacing their observed prices with averages of $m$ distinct observations in shrinking neighborhoods of the endpoints. For independent level noise this reduces endpoint noise variance to approximately $\omega^2/m$. The efficient-price distortion vanishes as the neighborhoods shrink. Jittering does not create the convergence rate, but it matters for the limiting variance: under fixed noise and the smooth-kernel bandwidth, $m\to\infty$ removes a boundary term. Merely choosing a small fixed $m$ does not literally deliver that boundary-free limit.

Define three deterministic kernel functionals:

$$
k^{0,0}=\int_0^1 k(x)^2\,dx,\qquad
k^{1,1}=\int_0^1 k'(x)^2\,dx,\qquad
k^{2,2}=\int_0^1 k''(x)^2\,dx.
$$

Decomposing $K(X)$ into efficient-price, price–noise cross, and pure-noise contributions explains the bandwidth trade-off. To leading order, on the unit interval,

$$
\operatorname{Var}\{K(Y)\mid\sigma\}
\simeq 4\frac{H}{n}Q\,k^{0,0},
$$

$$
\operatorname{Var}\{\text{cross contribution}\mid\sigma\}
\simeq \frac{8\omega^2I}{H}k^{1,1},
$$

$$
\operatorname{Var}\{K(U)\}
\simeq4\omega^4\left[
\frac{n}{H^2}\{k'(0)^2+k'(1)^2\}
+\frac{n}{H^3}k^{2,2}
+\frac{k^{1,1}}{Hm}
\right].
$$

These are the components behind Theorem 3 and equation (12), rather than three unrelated sources of error. Increasing $H$ adds more efficient-return autocovariances and raises the first component; it smooths differences in the weights and lowers the latter components.

If at least one endpoint derivative is nonzero, the $n/H^2$ term dominates the smooth interior contribution. Balancing it with $H/n$ requires $H\asymp n^{2/3}$ and produces only the $n^{1/6}$ rate. The Bartlett kernel is in this class. If

$$
k'(0)=k'(1)=0,
$$

the leading boundary derivative term disappears. Balancing $H/n$, $1/H$, and $n/H^3$ then gives $H\asymp\sqrt n$ and an $n^{1/4}$ rate. Smoothness is therefore a rate condition, not merely a way of making weights look less abrupt.

Let

$$
\xi^2=\frac{\omega^2}{\sqrt Q},
\qquad
\rho=\frac{I}{\sqrt Q}\in(0,1].
$$

Cauchy–Schwarz gives the upper bound on $\rho$, with equality for constant volatility on the normalized interval. With $H=c\xi\sqrt n$, suitable smoothness, and the endpoint conditions above,

$$
n^{1/4}\{K(X)-I\}
\;\xrightarrow{\mathrm{st}}\;
MN\!\left(0,\omega Q^{3/4}g(c,\rho)\right),
$$

$$
g(c,\rho)=4\left(
ck^{0,0}+\frac{2\rho}{c}k^{1,1}
+\frac{1}{c^3}k^{2,2}
\right).
$$

Stable convergence, stronger than ordinary weak convergence, supports combining the limiting Gaussian innovation with the random integrated variance and quarticity. The notation $MN$ denotes a mixed normal law: the conditional variance depends on the realized volatility path.

The rate statement is about fixed nonzero price noise as sampling becomes denser. It does not say that a low-noise finite sample is already well approximated by this limit, nor that the $n^{1/4}$ rate is universal for every possible, known noise distribution.

## Bandwidth optimization and attainable efficiency

For a fixed smooth kernel, minimizing $g(c,\rho)$ gives

$$
k^{0,0}c^4-2\rho k^{1,1}c^2-3k^{2,2}=0,
$$

and hence the positive optimum

$$
c_*^2=
\frac{\rho k^{1,1}
+\sqrt{\rho^2(k^{1,1})^2+3k^{0,0}k^{2,2}}}
{k^{0,0}}.
$$

This expression follows directly from the variance objective. There is a consequential printed discrepancy in equation (16), p. 1494: after defining $d=k^{0,0}k^{2,2}/(k^{1,1})^2$, its factored square root contains $1+3d/\rho$. The first-order condition requires $1+3d/\rho^2$. The displayed correction here is an algebraic derivation, not a claim about an official erratum. Values tabulated at $\rho=1$ are unaffected.

The following prose on p. 1495 also states that the optimized factor increases as $\rho$ decreases. At fixed kernel, the objective implies the opposite:

$$
\frac{\partial g(c_*(\rho),\rho)}{\partial\rho}
=\frac{8k^{1,1}}{c_*(\rho)}>0.
$$

This is an envelope calculation. It does not imply that introducing stochastic volatility lowers the total estimator variance: the multiplier $\omega Q^{3/4}$ changes when the volatility path changes.

Table II reports the following constants at $\rho=1$, rounded as in the paper:

| Kernel | $k^{0,0}$ | $k^{1,1}$ | $k^{2,2}$ | Optimal $c$ | Variance factor $g$ |
|---|---:|---:|---:|---:|---:|
| Cubic | 0.371 | 1.20 | 12.0 | 3.68 | 9.04 |
| Parzen | 0.269 | 1.50 | 24.0 | 4.77 | 8.54 |
| Modified Tukey–Hanning, $p=1$ | 0.375 | 1.23 | 12.1 | 3.70 | 9.18 |
| Modified Tukey–Hanning, $p=2$ | 0.219 | 1.71 | 41.7 | 5.74 | 8.29 |

The cubic is $k(x)=1-3x^2+2x^3$. The Parzen kernel is

$$
k(x)=
\begin{cases}
1-6x^2+6x^3,&0\le x\le1/2,\\
2(1-x)^3,&1/2<x\le1.
\end{cases}
$$

The modified Tukey–Hanning family is

$$
k(x)=\sin^2\!\left\{\frac{\pi}{2}(1-x)^p\right\}.
$$

The $p=2$ member, denoted TH2, is the principal numerical choice. Higher polynomial order alone does not guarantee efficiency: the fifth-order kernel is less efficient than the cubic in this comparison. The gain depends on all three integrals, especially the curvature penalty $k^{2,2}$, rather than endpoint smoothness considered in isolation.

For constant volatility and Gaussian independent noise, the likelihood benchmark has limiting variance $8\omega\sigma^3$ for estimating $\sigma^2$ at the $n^{1/4}$ rate. TH2's factor 8.29 lies close to that benchmark; Parzen gives 8.54 and cubic gives 9.04. This comparison is conditional on the benchmark's model. It is not a proof of semiparametric efficiency under every stochastic-volatility or endogenous-noise model.

Allowing kernels with infinite support yields a sharper design result. For $\rho=1$, the kernel

$$
k(x)=(1+x)e^{-x},\qquad x\ge0,
$$

has integrals $5/4$, $1/4$, and $1/4$, respectively. With $c=1$, its variance factor is exactly 8. An integration-by-parts representation of the objective leads to the Euler equation

$$
k''''-2c^2k''+c^4k=0.
$$

The repeated roots are $\pm c$; decay at infinity and the conditions $k(0)=1$, $k'(0)=0$ select the exponentially decaying solution. This gives a kernel-class optimum at constant volatility. Infinite support requires a practical truncation and additional observations outside the interval; the paper's main simulations and empirical comparisons instead use finite-support kernels.

Finite samples need not inherit the asymptotic ranking exactly. Table III evaluates normalized finite-sample variance, not a Monte Carlo table of estimator means. At $\xi^2=0.001$ and $n=256$, the optimal finite-sample benchmark is 15.1, versus 15.4 for TH2, 16.2 for Parzen, and 16.1 for cubic. At $n=4096$, the corresponding figures are 9.22, 10.0, 10.3, and 10.4. The asymptotic limits are 8, 8.29, 8.54, and 9.04. Small $\xi$ can imply a very short selected bandwidth, making the large-$H$ approximation poor even when absolute estimation error is small.

The flat-top placement is also essential for bias. Replacing the weights by $k(h/H)$ generally leaves noise bias $2n\omega^2\{1-k(1/H)\}$. With $k'(0)=0$ but $k''(0)\ne0$ and $H\asymp\sqrt n$, that bias is of constant order. Additional vanishing derivatives can restore asymptotic negligibility, but Table V shows that the finite-sample squared-bias penalty can remain large. This paper's conclusions cannot be transferred between these weight conventions without redoing the bias calculation.

## Feasible estimation and a reproducible calculation

The simplest noise-variance pilot is

$$
\widehat\omega^2=\frac{\gamma_0(X)}{2n}.
$$

Its leading efficient-price bias is $I/(2n)$. Under the basic model, its $\sqrt n$ asymptotic variance is $\omega^4(1+\lambda^2)$. The lag-one alternative $-\{\gamma_1+\gamma_{-1}\}/(2n)$ cancels the leading efficient-price mean but can be negative and has a larger variance, $\omega^4(5+\lambda^2)$. Equation (22) proposes the positive correction

$$
\widetilde\omega^2=
\widehat\omega^2
\exp\!\left\{-\frac{K(X)}{\gamma_0(X)}\right\}.
$$

This is a first-order bias reduction, not an exact unbiasedness identity. It also creates a pilot-selection issue because $K$ requires a bandwidth. One reproducible implementation starts with the raw noise pilot and a sparse realized-variance estimate, selects a preliminary bandwidth, computes $K$, and then updates the noise estimate. The paper does not fully specify a universal iteration count or stopping rule; such an iteration is an implementation choice that must be disclosed.

Quarticity estimation uses coarser returns, subsampling, and removal of the noise mean before multiplying squared returns. On the unit interval, let $\widetilde n=1/\widetilde\delta$ and define an average over $S$ phases,

$$
x_j^2=\frac1S\sum_{s=0}^{S-1}
\left[
X_{\widetilde\delta(j+s/S)}
-X_{\widetilde\delta(j-1+s/S)}
\right]^2.
$$

The proposed building block is

$$
B_Q=\frac1{\widetilde n}\sum_{j=1}^{\widetilde n}
\widetilde\delta^{-2}
(x_j^2-2\omega^2)(x_{j-2}^2-2\omega^2),
\qquad
\widehat Q=\max\{K^2,B_Q\}.
$$

The separation by two coarse intervals avoids the immediate overlap in level-noise endpoints. Using this displayed index range literally requires presample coarse bins; trimming instead should be explicit. Replace $\omega^2$ by a feasible pilot. The lower bound $K^2$ enforces the unit-interval inequality $Q\ge I^2$. The paper derives a noise-variance contribution of order $72\omega^8\widetilde n^3/S^2$ and a sufficient condition $\widetilde\delta^{3/2}S\to\infty$, with $S$ around $\sqrt n$ suggested numerically. Its discussion does not identify a single fully specified coarse-grid choice suitable for every dataset.

A general plug-in bandwidth uses $\widehat\xi^2=\widetilde\omega^2/\sqrt{\widehat Q}$, $\widehat\rho=K/\sqrt{\widehat Q}$, and the corrected optimizer above. The simulations also study a simpler rule of thumb based on $\rho=1$:

$$
H\approx c_*\widetilde\omega
\sqrt{\frac{n}{RV_{\mathrm{sparse}}}},
$$

where the feasible sparse pilot uses ten-minute returns. This replaces $\sqrt Q$ by $I$ and is not identical to estimating the general $\rho$-dependent optimum. Integer rounding and minimum-bandwidth conventions are additional replication inputs.

For sufficiently large smooth-kernel bandwidths, the feasible leading variance is

$$
\widehat V=
4\frac Hn\widehat Q\,k^{0,0}
+\frac{8\widetilde\omega^2K}{H}k^{1,1}
+4\widetilde\omega^4\frac n{H^3}k^{2,2}.
$$

A fixed-$m$ implementation must retain the endpoint correction when material. For short bandwidths, the paper uses finite-$H$ matrix expressions instead of replacing every weight difference by a derivative integral. Its matrices $A,B,C,D,E$ in Section 3.1, Theorem 1 (pp. 1488–1490), give the approximation

$$
V_H\simeq\frac{2Q}{n}w^\top Aw
+8\omega^2I\,w^\top Bw
+4\omega^4w^\top(nC+D+m^{-1}E)w,
$$

with $w=(1,1,k(1/H),\ldots,k((H-1)/H))^\top$. In particular, $w^\top Aw=1+2\sum_{h=1}^H w_h^2$, and $w^\top Bw=\sum_{h=1}^H(w_h-w_{h+1})^2$, setting $w_{H+1}=0$. These formulas make the distinction between the actual discrete estimator and its continuous-kernel approximation operational.

A direct way to verify the pure-noise component in code is to form the symmetric matrix $M$ such that $K=r^\top Mr$, construct a differencing-and-endpoint-averaging matrix $L$ from independent raw price errors to returns, and set $F=L^\top ML$. Then

$$
\operatorname{Var}(U^\top FU)=
2\omega^4\operatorname{tr}(F^2)
+(\lambda^2-2)\omega^4\sum_i F_{ii}^2.
$$

This last identity is a standard quadratic-form calculation supplied here as a replication check, not as software delivered by the authors. It also catches accidental changes in boundary conventions.

The paper favors a logarithmic studentization when estimates are positive:

$$
Z_{\log}=
\frac{\log(K+d)-\log(I+d)}
{\sqrt{\widehat V}/(K+d)},\qquad d=10^{-6}.
$$

Inverting it gives an approximate interval with endpoints $(K+d)\exp\{\pm1.96\sqrt{\widehat V}/(K+d)\}-d$. The offset handles numerical issues near zero; it does not establish validity after arbitrary truncation or under a misspecified noise model.

## How the arguments work, and what the extensions establish

The proof first analyzes the joint realized-autocovariance vector for a fixed number of lags. Its efficient-price, cross, and pure-noise components have different normalizations and covariance structures. Locally Gaussian efficient returns give the stable mixed-normal limit involving quarticity. Conditional on the efficient path, the cross term becomes a weighted sum of independent noise variables, with the largest weights becoming negligible. The pure-noise vector is decomposed into interior products and boundary products, which yields explicit finite-sample covariance matrices.

The growing-bandwidth argument then translates weighted quadratic forms into integrals involving $k$, $k'$, and $k''$. Summation by parts is particularly revealing: first differences of kernel weights govern the cross term, while second differences govern the interior noise term. The leading boundary pieces contain $k'(0)$ and $k'(1)$. Setting both to zero removes the larger $n/H^2$ contribution and exposes the $n/H^3$ curvature contribution. A martingale-array central limit argument handles the remaining noise-product sum. Endpoint averaging removes the residual boundary randomness. These steps explain both the rate distinction and why simply adding more autocovariances with arbitrary weights is not enough.

Appendix A contains a separate qualification relevant to a rigorous reconstruction. Some general joint-convergence statements are insufficient as printed. Proposition 5 combines marginal stable convergence with conditional convergence of another sequence, but without adequate joint conditions the claimed joint limit does not follow. With a trivial conditioning sigma-field, let $Y_n$ have the same standard normal law for every $n$ and set $Z_n=(-1)^nY_n$. The two marginal laws remain fixed, but their joint correlation alternates between $+1$ and $-1$. Similarly, independence of two sequences in Lemma 3 does not imply independence from the conditioning sigma-field: take $Y_n=0$, $Z$ Rademacher, $\mathcal G=\sigma(Z)$, and $Z_n=(-1)^nZ$. The marginal law of $Z_n$ is constant, but stable convergence relative to $\mathcal G$ fails.

These are condition gaps in the auxiliary statements, not counterexamples to the paper's realized-kernel limit under its full model. The first application involving efficient-price quantities has additional measurability structure; a later application involving noise requires a genuine conditional joint argument. A formal proof implementation should establish those model-specific conditions directly rather than invoking the general propositions without qualification.

Sections 4.7 and 5 broaden the observation setting in several distinct directions:

1. **Small noise.** If $\omega^2=\omega_0^2n^{-a}$ for $0<a<1$, a smooth kernel uses $H\asymp n^{(1-a)/2}$ and attains rate $n^{(1+a)/4}$. This interpolates between the fixed-noise and nearly noiseless regimes. For a kernel with nonzero endpoint derivatives, the corresponding orders are $H\asymp n^{2(1-a)/3}$ and rate $n^{(1+2a)/6}$. These rates follow by rebalancing the same variance terms; they should not be confused with a different asymptotic theory merely because the observed noise happens to be small.
2. **Irregular observations through a time change.** With $T_t=\int_0^t\tau_u^2du$, positive càdlàg $\tau$, and compatible filtration assumptions, the business-time process is $Y_{T_t}$. Its volatility is $\sigma_{T_t}\tau_t$, and its drift is $a_{T_t}\tau_t^2$. The latter follows from $dT_t=\tau_t^2dt$; the prose following Proposition 2 prints only one power of $\tau$ in that drift. Integrated variance is preserved under the time change, but quarticity and thus precision depend on the sampling clock. This result does not license every endogenous stopping-time sampling scheme.
3. **Dependent price noise.** The consistency arguments impose short-memory controls in the observation clock. Increasing the bandwidth more aggressively can suppress remaining noise terms, at the cost of precision. Proposition 4 supplies a more specific AR(1) result with $|\phi|<1$ and extra kernel restrictions, including $k''(0)=0$ and finite $k'''(0)$. The pure-noise variance acquires the factor $(1+\phi^2)/(1-\phi^2)$ relative to its independent-noise counterpart. The independent-noise central limit variance cannot simply be reused, and the extra kernel condition excludes some otherwise attractive basic-model kernels.
4. **A particular endogenous-noise filter.** The paper permits $U_i=\sum_{j=0}^{\bar H}\beta_j\Delta Y_{i-j}+\widetilde U_i$, with a finite filter and independent residual noise. The exact autocovariance identity is

$$
\gamma_h(Y,U)-\gamma_h(Y,\widetilde U)
=\sum_{j=0}^{\bar H}\beta_j
\{\gamma_{h+j}(Y)-\gamma_{h+j+1}(Y)\}.
$$

For a continuous efficient price, the leading contribution at $h=-k$ is $(\beta_k-\beta_{k-1})I$, with coefficients zero outside the filter. As the nearby kernel weights approach one, these terms telescope. The abbreviated two-case expression on p. 1508 involving only $\pm\beta_0$ describes the zero-length filter, not the entire general filter. The telescoping rationale survives this distinction. It establishes robustness for a structured class of endogeneity, not for arbitrary dependence between trading noise and prices.

The discussion of jumps is explicitly more tentative. It first considers an independent jump added to a continuous process under simplifying independence conditions and then discusses finite activity. Squared jump sizes enter the quadratic-variation target, while jump–diffusion and jump–noise cross terms affect the limit. This is not a jump-robust estimator of the continuous component alone, nor does the paper provide a fully general feasible jump inference procedure.

## Simulation design and the actual inference results

Section 6 uses 100,000 replications per design. One day is generated on a one-second Euler grid with $N=23{,}400$ steps, corresponding to 6.5 hours. The reported observation counts are $n=195,390,780,1560,4680,7800,11700,23400$, and noise-to-signal ratios are $\xi^2=0.01,0.001,0.0001$. These are estimation experiments; there are no training, validation, or forecast-testing splits.

The one-factor stochastic-volatility model is

$$
dY_t=0.03\,dt+\sigma_t\,dW_t,\qquad
\sigma_t=\exp(\beta_0+0.125\tau_t),
\qquad
d\tau_t=-0.025\tau_t\,dt+dB_t,
$$

with correlation $-0.3$ between $W$ and $B$, $\tau_0\sim N(0,20)$, and $\beta_0=0.125^2/(2(-0.025))=-0.3125$. This normalization gives $E[\sigma_t^2]=1$ in stationarity.

The two-factor design uses the paper's function s-exp,

$$
\sigma_t=\mathrm{s\mbox{-}exp}(-1.2+0.04\tau_{1,t}+1.5\tau_{2,t}),
$$

$$
d\tau_{1,t}=-0.00137\tau_{1,t}\,dt+dB_{1,t},
\qquad
d\tau_{2,t}=-1.386\tau_{2,t}\,dt+
(1+0.25\tau_{2,t})\,dB_{2,t}.
$$

The drift remains 0.03; each stated price–factor innovation correlation is $-0.3$. The first factor starts from its Gaussian stationary distribution and the second from zero. The detailed s-exp convention, numerical simulation details, and some distributional inputs are deferred to the working-paper treatment. The supplied article does not provide a complete random-seed and innovation specification that would enable bit-for-bit reproduction. In particular, one should not silently infer an unstated correlation between the two factor innovations.

Tables VI–IX compare infeasible studentization using population inputs, feasible raw studentization, and feasible logarithmic studentization. Although the captions call the tail entries “empirical quantiles,” the columns labeled 0.5%, 2.5%, 5%, 95%, 97.5%, and 99.5% report percentages below the corresponding standard-normal critical values. Treating a number such as 98.61 as a realized quantile of the studentized statistic would misread the table.

At $n=390$ and $\xi^2=0.001$, the key results are:

| Model and pivot | Mean | Standard deviation | Average $H$ | Below nominal 2.5% cutoff | Below nominal 97.5% cutoff | Implied central coverage |
|---|---:|---:|---:|---:|---:|---:|
| One-factor, infeasible | -0.004 | 1.007 | 4.00 | 1.81% | 96.76% | 94.95% |
| One-factor, feasible raw | -0.181 | 1.019 | 5.94 | 5.38% | 99.57% | 94.19% |
| One-factor, feasible log | -0.097 | 0.964 | 5.94 | 3.09% | 98.61% | 95.52% |
| Two-factor, feasible log | -0.203 | 1.188 | 6.34 | 7.12% | 96.91% | 89.79% |

The coverage column is calculated here by subtracting the two reported cumulative percentages; the other values are reported results. The feasible raw statistic has pronounced tail imbalance even when its aggregate central coverage is not far from 95%. Logging improves that balance in the one-factor case. The two-factor design remains substantially less well calibrated at this sample size.

At $n=23{,}400$ and the same noise ratio, the one-factor log statistic has mean $-0.028$, standard deviation 0.983, and cumulative tail entries 2.56% and 97.86%, implying 95.30% central coverage. The two-factor counterpart has mean $-0.067$, standard deviation 1.064, and tail entries 4.00% and 97.36%, implying 93.36% coverage. Thus denser sampling improves the difficult design, but “approximately Gaussian” should not be read as exact coverage across all volatility specifications.

With 100,000 independent replications, the Monte Carlo standard error of a 95% coverage proportion is approximately 0.069 percentage points, calculated as $100\sqrt{0.95(0.05)/100000}$. Deviations of several percentage points therefore cannot be attributed to ordinary simulation counting noise. Parameter estimation, finite bandwidth, volatility dynamics, and the choice of pivot matter more.

## General Electric: measurement differences, not a trading backtest

The empirical application uses General Electric transactions on the NYSE during 2004. The main estimator takes every $S$th transaction, choosing $S$ day by day to obtain roughly 360 returns, about one observation per minute. It is therefore approximately one-minute sampling in transaction time, not an exact common calendar grid and not an empirical use of the simulation's $n=390$ design.

Table X gives 20 listed trading days in November. Transaction counts commonly lie in the thousands, while the selected $S$ values are 13–16, retained return counts 335–361, and kernel bandwidths 4–6. The raw noise estimate and the exponentially corrected noise estimate occupy separate columns and should not be conflated. Their displayed ranges are approximately 0.0009–0.0028 and 0.0004–0.0011, respectively, in the table's squared-return units.

On November 1, 4,631 transactions yield $S=13$, $n=357$, and $H=5$. Twenty-minute realized variance is 0.83 with an interval of 0.48–1.46, while the realized kernel is 0.69 with an interval of 0.49–0.95. The raw noise estimate is 0.0016 and its correction is 0.0007. On November 19, the comparison is 1.73 with interval 0.83–3.62 for twenty-minute realized variance, against 1.31 with interval 0.97–1.76 for the kernel. These examples illustrate the precision gain available from using more observations while correcting noise.

That gain is not universal day by day. On November 24, twenty-minute realized variance is 0.36 with interval 0.19–0.68, whereas the kernel is 0.79 with interval 0.48–1.30; the latter interval is wider. The article reports positive kernel estimates throughout 2004 and only three days with nonoverlapping intervals between the two methods. Agreement and overlap do not establish coverage, because latent integrated variance is not observed in the empirical data.

Table XI compares daily estimates over the year:

| Estimator | Mean | Daily standard deviation | Correlation with TH2 |
|---|---:|---:|---:|
| TH2 kernel | 0.908 | 0.541 | 1.000 |
| Parzen kernel | 0.914 | 0.546 | 0.999 |
| Cubic kernel | 0.915 | 0.542 | 0.998 |
| Fifth-order kernel | 0.919 | 0.530 | 0.999 |
| Eighth-order kernel | 0.912 | 0.550 | 0.995 |
| Bartlett kernel | 0.934 | 0.551 | 0.988 |
| Twenty-minute realized variance | 0.879 | 0.524 | 0.794 |
| Five-minute realized variance | 0.948 | 0.518 | 0.954 |
| One-minute realized variance | 0.941 | 0.382 | 0.887 |
| Ten-second realized variance | 1.330 | 0.389 | 0.803 |
| Tick realized variance | 2.183 | 0.569 | 0.733 |

These are the source's displayed daily variation units, not annualized percentage volatility or dollar variance. The supplied article does not fully document the return scaling and all data-preparation details in the empirical section; preserve the table's units rather than inventing an annualization or square-root transformation. Table XI's parenthesized “HAC” entries are also distinct from the daily standard deviations above: TH2 has daily standard deviation 0.541 and parenthesized HAC value 1.168. Without the full normalization convention, 1.168 should not be presented as a standard error of the sample mean.

The smooth kernels are extremely similar in this application despite different theoretical efficiency constants. The rise in the mean of ordinary realized variance at ten-second and tick frequencies is consistent with noise contamination. TH2 has first-order daily autocorrelation 0.34; the twenty-minute realized variance counterpart is 0.28. The paper interprets greater persistence as compatible with less measurement error, but it does not test a predictive model that turns this observation into a forecasting gain.

Section 7.2 deliberately pushes beyond the basic inference setting by using all transactions with a bandwidth proportional to $n^{2/3}$. The coefficient is calibrated from the roughly one-minute analysis. This is a robustness exercise motivated by dependent and endogenous noise, and the authors relinquish a corresponding formal inference claim. It is neither the smooth independent-noise optimum nor the later 2009 practice bandwidth rule.

In Table XII, the all-transaction TH2 estimate has mean 0.894, daily standard deviation 0.497, and correlation 0.991 with the main TH2 series. All-transaction Parzen and cubic have means 0.901 and 0.907 and correlations 0.990 and 0.991. Their proximity suggests that the main daily series is not driven entirely by the initial thinning choice, but it cannot establish robustness for untested assets or noise dynamics.

The comparisons include subsampled realized variance and two two-scale estimators. The Zhang–Mykland–Aït-Sahalia estimator has mean 0.544 before adjustment and 0.596 after adjustment, with correlations 0.842 and 0.854. The Aït-Sahalia–Mykland–Zhang estimator has mean 0.736, rising to 0.946 after the paper's area adjustment, with correlation 0.944 in both cases. Its numerical implementation imposes a scale constraint of at least five times the shorter scale when the nominal choice is infeasible. These details matter: the comparison is not simply between unmodified population-optimal formulas.

There is a minor figure-description inconsistency worth preserving in replication records. The surrounding discussion refers to five-minute subsampled realized variance in connection with Figure 4, while the caption and legend specify twenty-minute returns with 1,200 starting positions. The caption and legend identify what is plotted. Figure 4 reuses the approximately one-minute kernel confidence bands from Figure 3; these are not newly established all-transaction robust confidence intervals. Figure 3 also displays twenty-minute realized-variance intervals.

## Replication requirements and remaining limits

A source-faithful reimplementation should make the following choices explicit before comparing estimates:

1. Fix the time normalization and the target: continuous integrated variance for the main diffusion model, or quadratic variation including jumps for a separately justified extension. Keep volatility, variance, and quarticity units distinct.
2. Specify transaction selection, timestamp handling, session boundaries, and returns available before and after the estimation interval. Implement both signed-lag autocovariances exactly, or document the chosen trimmed alternative.
3. Record endpoint averaging neighborhoods and $m$, the flat-top lag argument $(h-1)/H$, the kernel formula, integer bandwidth rounding, and any nonnegativity truncation.
4. Estimate the noise pilot and the sparse variance pilot with their actual sampling intervals. Distinguish the $\rho=1$ rule of thumb from a quarticity-based plug-in optimum. If pilots are iterated, retain their order and stopping rule.
5. Define the quarticity coarse grid, number and placement of subsamples, noise correction, and treatment of the two presample coarse bins. Apply finite-$H$ variance formulas when the selected bandwidth is only a few lags.
6. Validate estimator bias, variance, pivot tail probabilities, and interval coverage separately. Match the simulation's noise-to-signal ratios and stochastic-volatility models before claiming reproduction of the tables. Compare raw and logarithmic pivots, not merely point estimates.
7. Treat dependent noise, endogenous noise, and jumps as model changes. Recalibrate inference to the extension actually assumed; similarity of empirical point estimates does not supply a missing central limit theorem.

The article leaves several inputs to its longer working-paper and data documentation: full transaction-cleaning rules, vendor and trade-filter details, exact session exclusions, the complete empirical return-unit convention, some simulation innovations and discretization choices, and a universally specified feasible-pilot iteration. Those omissions prevent exact numerical reconstruction from this PDF alone. There is no estimation or trading cost function, portfolio constraint, execution model, transaction-cost assumption, or realized investment return to reproduce.

For applied quant work, the most reusable result is the mechanism connecting the covariance structure of noisy returns to the smoothness of the correction weights. The first lag removes the leading noise bias; the remaining lags make that correction statistically usable; endpoint derivative restrictions determine the attainable rate; and finite-sample inference depends on implementing those choices as a single estimator. The near-likelihood efficiency result is powerful within its stated model, while the simulations show why that asymptotic statement must be supplemented by finite-bandwidth and volatility-dynamics checks.

## Source map and bibliography

The complete supplied PDF has 56 pages, corresponding to printed pp. 1481–1536. All pages, including the appendices and references, were read for this note. The central locations are:

- Section 2, pp. 1484–1488: observation model, flat-top estimator, and endpoint treatment.
- Section 3, pp. 1488–1492: fixed-lag covariance results, Theorem 1, and finite-sample matrices.
- Section 4, pp. 1492–1503: growing-bandwidth limits, equation (12), bandwidth optimization, equation (16), kernel comparisons, non-flat alternatives, and small-noise analysis.
- Section 5, pp. 1503–1510: noise estimation, equation (22), subsampled quarticity, time changes, dependence, endogeneity, and jumps.
- Section 6, pp. 1510–1512 for the narrative and pp. 1513–1516 for Tables VI–IX: simulation designs and inference results.
- Section 7, pp. 1513–1521: General Electric application, Tables X–XII, and Figures 3–4.
- Appendix A, pp. 1522–1524, and Appendix B, pp. 1524–1532: stable-convergence tools, covariance calculations, growing-bandwidth proofs, kernel optimization, and dependent-noise calculations.

Primary reference: Barndorff-Nielsen, O. E., P. R. Hansen, A. Lunde, and N. Shephard (2008), “Designing Realized Kernels to Measure the Ex Post Variation of Equity Prices in the Presence of Noise,” *Econometrica* 76(6), 1481–1536. [Local source](../../Finance/RealizedVariance_BarndorffnielsenHansenLundeShephard_2008.pdf).

Related works enter this note only through the source's comparisons: Zhang, Mykland, and Aït-Sahalia (2005), “A Tale of Two Time Scales”; Aït-Sahalia, Mykland, and Zhang (2006), “Ultra High Frequency Volatility Estimation With Dependent Microstructure Noise”; and Zhang (2006), “Efficient Estimation of Stochastic Volatility Using Noisy Observations: A Multi-Scale Approach.” Their numerical comparisons here are the 2008 paper's implementations, not independent replications of those studies.

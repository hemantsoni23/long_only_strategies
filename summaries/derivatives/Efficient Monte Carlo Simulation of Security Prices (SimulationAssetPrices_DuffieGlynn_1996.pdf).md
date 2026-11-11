# Efficient Monte Carlo Simulation of Security Prices

Darrell Duffie and Peter Glynn. *The Annals of Applied Probability* 5(4), November 1995, pp. 897–905. Received April 1993; revised May 1995. The local filename says 1996, but the source is the published 1995 article. Its 11 PDF pages consist of a JSTOR wrapper, nine article pages, and a linked-citation page; there is no separate appendix.

Source: [SimulationAssetPrices_DuffieGlynn_1996.pdf](../../Finance/SimulationAssetPrices_DuffieGlynn_1996.pdf). Printed pp. 897–905 correspond to PDF pp. 2–10. Equations and both numerical tables were checked visually because the text extraction omits substantial mathematical material. Corrections below distinguish the printed source from mathematical reconstruction.

## Why this matters

A Monte Carlo price can have a tiny standard error and still be inaccurate because the simulated dynamics use a coarse time grid. Conversely, a very fine grid wastes computation when too few independent paths leave large sampling noise. The paper determines how these two controls should grow together when computational resources are limited.

Its main contribution is an asymptotic allocation theorem. If discretization bias is of order $h^p$ and the resource cost per independent path is of order $h^{-q}$, the useful time-step scale at budget $t$ is $h\asymp t^{-1/(q+2p)}$. The resulting error scale is $t^{-p/(q+2p)}$. For ordinary time-stepping, $q=1$: first-order weak schemes have a budget error rate $t^{-1/3}$ and second-order weak schemes have rate $t^{-2/5}$. These rates include approximation bias as well as sampling error.

The result concerns ordinary independent-path simulation of a biased approximation. It is not a statement that every Monte Carlo estimator must obey these rates. Exact simulation, different estimators, and methods that couple multiple resolutions change the problem. Nor does the paper provide a turnkey adaptive implementation with estimated constants and guaranteed finite-budget confidence intervals. It establishes the rate relationship and illustrates it numerically.

## Target expectation and simulation model

Let $X_t\in\mathbb R^N$ solve

$$
dX_t=a(X_t,t)\,dt+b(X_t,t)\,dB_t,\qquad X_0=x,
$$

where $B$ is a $d$-dimensional standard Brownian motion and $b$ is an $N\times d$ diffusion matrix. The desired value is $\alpha=E[f(X_T)]$. For pricing, expectation is taken under an appropriate pricing measure and the payoff includes discounting or an equivalent state augmentation. The allocation theorem itself is probabilistic and does not identify that pricing measure.

Take $h=T/n$ for an integer number of intervals. Euler simulation is

$$
\widehat X_{j+1}=\widehat X_j+a(\widehat X_j,jh)h
+b(\widehat X_j,jh)\sqrt h\,\varepsilon_{j+1},
\qquad \varepsilon_j\overset{\mathrm{iid}}\sim N(0,I_d).
$$

The printed Euler formula suppresses the time argument of $b$; retaining it is necessary for the general time-inhomogeneous SDE. One simulated observation is $Z(h)=f(\widehat X_n)$. Repeating complete paths independently produces the estimator

$$
\widehat\alpha_{h,k}=\frac1k\sum_{i=1}^k Z_i(h).
$$

For fixed $h$, increasing $k$ converges to $\alpha(h)=E[Z(h)]$, not necessarily to $\alpha$. The basic error decomposition is

$$
\widehat\alpha_{h,k}-\alpha
=\underbrace{\widehat\alpha_{h,k}-\alpha(h)}_{\text{sampling error}}
+\underbrace{\alpha(h)-\alpha}_{\text{discretization bias}}.
$$

Strong approximation controls the closeness of coupled paths. Weak approximation controls expectations such as this price. The exponent $p$ in this paper is a weak-bias exponent; inserting a strong convergence order into the allocation formula can choose the wrong budget split.

Condition A on p. 898 assumes a smooth payoff of polynomial growth and infinitely differentiable drift and diffusion with bounded derivatives of every order. Under the cited weak-error results, Euler has a first-order expansion, and suitable higher-order schemes have a second-order expansion. These are sufficient conditions, not a claim that nonsmooth options or square-root diffusions satisfy them. Later sections explicitly discuss departures from the formal assumptions.

## General resource-allocation theorem

Section 2 replaces the diffusion with a general target random variable $Z$. It requires: $Z(h)$ converges in distribution to $Z$; second moments converge to the finite second moment of $Z$, giving the relevant uniform integrability; the mean has expansion $\alpha(h)=\alpha+\beta h^p+o(h^p)$ with $\beta\ne0$ and $p>0$; and deterministic cost per observation satisfies $\tau(h)=\gamma h^{-q}+o(h^{-q})$, with $\gamma,q>0$.

Write $\sigma_Z^2=\operatorname{Var}(Z)$. At budget $t$, the number of independent paths is $k(t,h)=\lfloor t/\tau(h)\rfloor$. A nondegenerate sampling problem has $\sigma_Z^2>0$. The asymptotic regime also needs $h_t\to0$ and enough completed paths for the triangular-array central limit theorem. These regularity qualifications matter when interpreting the theorem's extreme allocation cases; selecting a grid so expensive that no path is completed is not an admissible price estimator.

If

$$
h_t t^{1/(q+2p)}\longrightarrow c\in(0,\infty),
$$

Theorem 1 gives

$$
t^{p/(q+2p)}\bigl(\widehat\alpha_{t,h_t}-\alpha\bigr)
\ \Rightarrow\ 
\sigma_Z\sqrt{\gamma/c^q}\,W+\beta c^p,
\qquad W\sim N(0,1).
$$

Thus the limit is normal with a generally nonzero mean. A standard error based only on the dispersion of simulated payoffs describes the sampling component, not the full error relative to the continuous-time price. The limiting bias does not disappear relative to the standard deviation at the rate-optimal allocation.

To see the rate without invoking the theorem, use $k\approx th^q/\gamma$. The sampling standard deviation is approximately $\sigma_Z\sqrt\gamma\,t^{-1/2}h^{-q/2}$, while bias magnitude is approximately $|\beta|h^p$. Equating their orders gives $h^{p+q/2}\asymp t^{-1/2}$ and the stated exponent. The proof formalizes this calculation by centering each row of independent simulated payoffs, applying a Lindeberg–Feller limit theorem using the moment assumptions, and adding the deterministic bias expansion.

If the grid becomes coarse relative to this scale, bias dominates. If it becomes too fine while the number of paths still grows, sampling error dominates. The source expresses both cases as divergence of the error under the optimal normalization. The theorem's assumptions exclude zero leading bias; if $\beta=0$, one must use the first nonzero bias term or recognize that a different special case is operating. Zero payoff variance is another degenerate case outside the ordinary balance argument.

The practical relation between paths and resolution is particularly simple:

$$
k\asymp h^{-2p}\asymp n^{2p}.
$$

Doubling the time intervals requires four times as many paths for $p=1$, and sixteen times as many for $p=2$. With $q=1$, those changes cost approximately factors eight and thirty-two, respectively. They reduce the asymptotic error scale by factors two and four. The small improvement in the budget exponent explains why higher weak order can still require considerable computation, especially before its smaller bias becomes dominant.

## Choosing the allocation constant: a derived implementation

Theorem 1 characterizes every positive finite constant $c$ as rate-optimal; it does not make their error constants equal. A useful reconstruction, derived from the paper's assumptions, minimizes leading mean-squared error:

$$
\operatorname{MSE}(h,t)\approx\beta^2h^{2p}
+\frac{\sigma_Z^2\gamma}{t h^q}.
$$

Differentiating gives

$$
h_*=
\left(\frac{q\sigma_Z^2\gamma}{2p\beta^2t}\right)^{1/(q+2p)}.
$$

At this optimum, the leading variance equals $(2p/q)$ times squared bias. Equalizing the two errors exactly is therefore not generally the MSE-optimal constant, although it gives the correct rate. Cost to obtain root-mean-squared error $\epsilon$ is of order $\epsilon^{-(2+q/p)}$: $\epsilon^{-3}$ for ordinary Euler and $\epsilon^{-5/2}$ for second-order weak simulation.

A practical pilot can estimate payoff variance, time per path, and the bias coefficient from two or three resolutions. Under the assumed expansion,

$$
\beta\approx\frac{\alpha(2h)-\alpha(h)}{(2^p-1)h^p}.
$$

Using common Brownian increments for fine and coarse pilot paths can reduce uncertainty in that difference. This is a suggested implementation of the theorem, not an experiment reported in the article. It requires checking that the resolution differences are large relative to their sampling errors and approximately follow the claimed power law. An almost zero noisy bias estimate should not be allowed to recommend an arbitrarily coarse final grid.

The paper's first-order discussion on p. 898 prints $C_h=2(f_{2h}-f_h)/h$ after defining $f_h=\alpha+Ch+O(h^2)$. Those definitions imply $(f_{2h}-f_h)/h=C+O(h)$; the printed formula instead approaches $2C$. This is an algebraic factor-of-two inconsistency, not a change in the rate theorem. Use the consistent difference formula when calibrating a constant.

For reproducible implementation, specify an independent final-production stream after the pilot, record how grid rounding changes $h$, and report both a sampling standard error and an estimated bias diagnostic. If variance reduction introduces dependent pairs, treat the independent pair average as the simulation observation and charge its full cost. Counting two antithetic members as independent incorrectly shrinks the reported standard error.

## The second-order scalar scheme actually used

The source's Eq. (3), p. 898, is more elaborate than the familiar first-order Milstein update. For a time-homogeneous scalar diffusion with drift $\mu(x)$ and diffusion coefficient $s(x)$, its update is

$$
\Delta\widehat X
=\mu h+s\sqrt h\,\varepsilon
+\frac12ss'h(\varepsilon^2-1)
+\nu h^{3/2}\varepsilon+\eta h^2,
$$

where all functions are evaluated at the old state and

$$
\nu=\frac12\mu s'+\frac12\mu's+\frac14s^2s'',
\qquad
\eta=\frac12\mu\mu'+\frac14\mu''s^2.
$$

The last two terms are essential to the stated second-order weak construction. Dropping them and retaining only the $ss'$ correction is not a replication of this formula. The paper refers to separate multidimensional schemes rather than presenting an arbitrary-dimensional update here.

For the CEV example, write $s(x)=a x^\delta$, with $a=0.2$ and elasticity $\delta\in\{1/2,1\}$, to avoid confusing the elasticity with the theorem's cost constant. If drift is $\mu(x)=m x$, the functions become

$$
ss'=a^2\delta x^{2\delta-1},\qquad
\nu=\frac12ma(\delta+1)x^\delta
+\frac14a^3\delta(\delta-1)x^{3\delta-2},
\qquad \eta=\frac12m^2x.
$$

These expressions are direct substitutions into Eq. (3), not separately stated formulas in the article. At elasticity one-half, derivatives become singular near zero. The source extends the diffusion coefficient as zero for negative states, but does not specify the numerical extension of all derivative terms, clipping rules, or absorbing-boundary handling. That omission matters for a general implementation even if the chosen experiment rarely visits zero.

The paper also experiments with Gaussian and uniform innovations and says alternative zero-mean unit-variance distributions can be used under technical conditions. That sentence should not be read as permitting arbitrary moment substitutions while preserving weak order two. For example, standardized continuous uniform noise has fourth moment $9/5$, while Gaussian noise has fourth moment 3. In the scalar geometric case, the $h(\varepsilon^2-1)$ term contributes to the next-step second moment through $E[(\varepsilon^2-1)^2]$. Replacing Gaussian noise directly changes a coefficient at order $h^2$, which generally changes global weak order unless the scheme is adjusted.

Accordingly, reproduce the Gaussian branch first. The uniform branch is a reported numerical experiment whose exact distribution normalization and any moment corrections are not fully documented. It is not a proof of universal second-order validity for continuous uniform increments.

## Option experiment and source inconsistencies

Section 3 considers a constant-elasticity-of-variance process and a call-like payoff. Its printed Eq. (8), p. 901, has drift **$-rX_t$**. The surrounding text calls $Q$ the pricing measure and discounts terminal cash flows by $e^{-rT}$. For an ordinary non-dividend-paying asset under that pricing convention, the drift should be **$+rX_t$**. No dividend specification explains the negative sign. Thus the printed dynamics and claimed standard pricing interpretation are inconsistent.

A literal mathematical replication can simulate drift $m=-r$ and evaluate the resulting expectation, but should not call it the standard risk-neutral call price. A financially consistent reconstruction uses $m=+r$. The paper does not reveal which sign its code used. This note reports the table values without pretending that this ambiguity has been resolved.

The authors rescale the security's payoff to $e^{rT}(X_T-K)^+$ so that the target expectation is simply $E[(X_T-K)^+]$. For a conventional call with payoff $(X_T-K)^+$, multiply that target by $e^{-rT}$. Mixing the discounted and undiscounted targets changes both price and absolute errors by a constant factor.

The numerical parameters are $a=0.2$, $r=0.1$, $K=40$, $X_0=42$, and $T=0.5$, with elasticities $\delta=1$ and $1/2$, both discretizations, and both innovation choices. Reported error is sample root-mean-squared error over ten trials. A reconstruction computes a full price estimate for each trial, subtracts a trustworthy exact or numerical reference price for the *same* dynamics and payoff, then takes the square root of the average squared error. The paper does not provide seeds, random-number generator, exact benchmark values, timing measurements, or trial-level errors.

For the nonsmooth call, p. 902 introduces the smooth approximation

$$
f_\zeta(x)=\frac{x-K+\sqrt{(x-K)^2+\zeta}}2.
$$

Its maximum excess above $(x-K)^+$ is $\sqrt\zeta/2$. The printed recommendation $\zeta\asymp h^{-2p}$ has the wrong direction: the smoothing error then increases as the grid is refined. To keep this *payoff approximation error* at order $h^p$, one needs $\zeta=O(h^{2p})$, or smaller for negligible smoothing bias. Moreover, fixed-payoff weak-error constants need not remain bounded as derivatives of $f_\zeta$ grow when $\zeta\to0$. This elementary correction alone does not prove a uniform weak-order theorem for the joint limit. The article cites separate work allowing nonsmooth payoffs without this smoothing argument.

For CEV elasticity below one, the authors explicitly acknowledge that Condition A does not hold. Distributional convergence of the simulated payoff is not sufficient by itself to establish the nonzero bias expansion, rate, or all moment requirements. The reported square-root examples are therefore numerical illustrations beyond the paper's directly verified smooth setting.

## Numerical results and what they demonstrate

Table 1, p. 902, uses Euler grids $n=8,16,32,64,128,256,512,1024$ with $k=n^2$ paths. Thus the first row uses 64 paths and the last 1,048,576. The reported root-mean-squared errors are:

| Intervals | Paths | Elasticity 1, Gaussian | Elasticity 1, uniform | Elasticity 1/2, Gaussian | Elasticity 1/2, uniform |
|---:|---:|---:|---:|---:|---:|
| 8 | 64 | 0.33386 | 0.59804 | 0.13023 | 0.11984 |
| 32 | 1,024 | 0.14807 | 0.11988 | 0.01742 | 0.03525 |
| 128 | 16,384 | 0.02606 | 0.04554 | 0.00854 | 0.00428 |
| 512 | 262,144 | 0.00636 | 0.01040 | 0.00160 | 0.00171 |
| 1,024 | 1,048,576 | 0.00616 | 0.00468 | 0.00064 | 0.00065 |

The source's reported average reduction factors across all adjacent doublings are 1.97, 2.16, 2.22, and 2.23, respectively. Individual rows fluctuate: the final Gaussian geometric-model error barely improves, illustrating the noisiness of a ten-trial RMSE rather than refuting an asymptotic rate.

Table 2, p. 903, uses the second-order update with $(n,k)=(32,15),(64,240),(128,3840),(256,61440)$. Paths multiply by sixteen for each grid doubling. Gaussian geometric-case errors are 1.19471, 0.21429, 0.04765, and 0.02003. Uniform geometric-case errors are 1.22362, 0.41149, 0.08138, and 0.02069. For elasticity one-half, the Gaussian series is 0.00041, 0.00009, 0.00001, and 0.000002; the uniform series is 0.00030, 0.00006, 0.000005, and 0.000001.

The reported average reduction factors are 4.15, 3.99, 6.11, and 7.43. The two geometric cases broadly illustrate the predicted factor four. The faster reductions in the square-root examples are finite-experiment observations, not proof of a better universal order. Small payoff variance, a small leading bias coefficient, special parameter choices, rounding of tiny errors, and trial noise can all affect observed ratios.

There is another consequential printed inconsistency: the paragraph below Table 2 says path counts increase by factors two and four for Euler and Milshtein. The actual tables and the theorem require factors **four and sixteen**. The former numbers describe expected error-reduction factors, not path-count multipliers. Reimplement the table schedules above.

These experiments do not establish that second-order simulation is faster for every desired accuracy. The two tables use different starting path counts and do not supply measured wall-clock costs for derivative evaluation or random-number generation. Comparing error at the same interval count alone is not an efficiency comparison. To evaluate an implementation, compare error at equal measured budget, including the larger per-step constant of the higher-order scheme.

## Extensions and limits

Section 4 explains how a terminal-payoff framework can include some path dependence. Add an integrated state $Y_t=\int_0^t X_s\,ds$ using $dY_t=X_tdt$; a payoff involving the integral then becomes a terminal function of $(X_T,Y_T)$. The example prints $(X_T-\int_0^T X_tdt)^+$, without division by $T$. A conventional average-price contract requiring $T^{-1}\int X_tdt$ must include that normalization explicitly; changing it changes the security.

Stochastic discounting can be included with $D_0=1$ and $dD_t=-R(X_t)D_tdt$, so the value becomes $E[D_T f(X_T)]$. Smoothness and growth assumptions must hold for the augmented system; state augmentation is not an automatic guarantee of high weak order.

A running minimum for lookback payoffs similarly makes the payoff terminal in an enlarged state, but that state is not an ordinary smooth diffusion. Boundary stopping, reflection, and discretely missed extrema require appropriate approximation results before assigning $p$. The general allocation theorem remains useful once a valid bias expansion is available. Its flexibility lies in separating the allocation calculation from the difficult proof of weak approximation for each contract.

The paper's operational lesson is to measure or justify the bias order of the actual payoff, boundary convention, innovation scheme, and discretization being run, then allocate paths and steps jointly. Reporting only Monte Carlo standard errors or citing a nominal scheme order is insufficient. Its rate theorem is clean and reusable; its short numerical illustration contains enough omissions and printed inconsistencies that exact table reproduction requires further implementation provenance.

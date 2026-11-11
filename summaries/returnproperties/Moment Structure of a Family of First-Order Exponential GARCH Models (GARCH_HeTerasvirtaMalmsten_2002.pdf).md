# Moment Structure of a Family of First-Order Exponential GARCH Models

Changli He, Timo Teräsvirta, and Hans Malmsten, *Econometric Theory* 18 (2002), pp. 868–885, DOI 10.1017/S0266466602184039. Source: [GARCH_HeTerasvirtaMalmsten_2002.pdf](../../Finance/GARCH_HeTerasvirtaMalmsten_2002.pdf). All 18 pages, including the full proof appendix, were read. The central formulas, Table 1, Figure 1, and distributional qualifications were checked visually. Page references below are printed journal pages.

## Why this matters

A volatility model's persistence parameter does not fully describe the dependence of observed squared returns. Standard GARCH(1,1) implies a geometrically decaying autocorrelation function for squared observations when fourth moments exist. An EGARCH(1,1) model with an equally persistent log variance can produce a much faster initial decline in squared-return autocorrelations, followed by slower decay at distant lags. It can also combine extremely high unconditional kurtosis with that rapid initial decline.

The paper derives the moments and autocorrelations needed to quantify this distinction. Its novel object is the autocorrelation of positive powers of absolute observations, including squares, absolute values, and square roots of absolute values. Prior log-volatility results do not automatically answer this question because exponentiation is nonlinear. The authors give general expectation-product formulas, specialize them to normal and generalized-error innovations, and compare the implied dependence patterns numerically with standard GARCH.

This is a theoretical and numerical study. It contains no fitted financial dataset or return-forecast competition. Its value for implementation is that an estimated or proposed EGARCH specification can be checked against unconditional moment and dependence implications without relying entirely on long, potentially unstable Monte Carlo samples.

## Model and notation

The observations are

$$
\varepsilon_t=h_tz_t,\qquad
\log h_t^2=a_0+g(z_{t-1})+\beta\log h_{t-1}^2.
$$

The innovations $z_t$ are iid with mean zero. The positive scale $h_t$ is measurable with respect to past innovations. Denote absolute innovation moments by $\nu_q=E|z_t|^q$. When $\nu_2=1$, $h_t^2$ is the conditional variance. If the innovations have another finite variance, that conditional variance is $\nu_2h_t^2$ instead.

The function $g$ specifies the response of log variance to news. The standard asymmetric EGARCH example is

$$
g(z)=\phi z+\psi\bigl(|z|-E|z|\bigr).
$$

Here $\phi$ controls sign asymmetry, $\psi$ the response to shock magnitude, and $\beta$ the persistence of log variance. For shocks of equal magnitude $x>0$, $g(-x)-g(x)=-2\phi x$. Thus a negative $\phi$ makes negative shocks raise the next log variance more than positive shocks. This statement concerns the response holding magnitude fixed; it is not itself a causal interpretation of leverage.

The class also contains logarithmic GARCH by choosing $g(z)=\alpha\log z^2$. Substituting $\log z_{t-1}^2=\log\varepsilon_{t-1}^2-\log h_{t-1}^2$ shows how the log-variance recursion relates to lagged log-squared observations. The paper concentrates on first-order models and does not derive a general higher-order moment system.

## Stationarity and exponential-integrability requirements

Theorem 1, p. 870, gives $|\beta|<1$ as the stationarity condition under finite innovation second moment and finite variance of $g(z)$. The relevant causal stationary representation is

$$
\log h_t^2=\frac{a_0}{1-\beta}+\sum_{j=0}^{\infty}\beta^j g(z_{t-1-j}).
$$

The geometric coefficients make this a stationary function of past iid shocks under the stated regularity conditions. As usual, a necessity statement for a stochastic AR recursion should be understood in the nondegenerate setting: specially chosen constant-news, deterministic-scale cases are not the substantive model considered in the paper.

Stationarity of log variance does not, by itself, guarantee finite ordinary return moments. Exponentiating the stationary series requires exponential moments of $g$. Define the moment-generating transform

$$
M(u)=E[e^{u g(z)}].
$$

A reproducible implementation must check that this expectation exists at the arguments used, not merely that $\nu_2$ exists or that the simulated recursion stays finite over a short run. This is the reason normal innovations and Student innovations can behave very differently in EGARCH even when both have finite variance.

Theorem 2 is stated using $E[e^{mg(z)}]<\infty$ and $\nu_{2m}<\infty$ for $m>0$. For the nonnegative $\beta$ values in the numerical examples, intermediate arguments $m\beta^j$ lie between zero and $m$, making the required domain transparent. For negative $\beta$, the arguments alternate sign: finiteness only at a positive endpoint does not by itself establish the required negative exponential moments. This note therefore retains the full transform-domain requirement for implementation. Normal innovations with the linear/absolute-value news function have finite transforms at every finite real argument, so that qualification does not affect the paper's normal examples.

## Arbitrary absolute moments as infinite products

Introduce

$$
P(a)=\prod_{j=0}^{\infty}M(a\beta^j).
$$

Using independence across innovation dates and independence of $z_t$ from $h_t$, the central moment formula, equation (6), becomes

$$
E|\varepsilon_t|^{2m}=\nu_{2m}\exp\left(\frac{ma_0}{1-\beta}\right)P(m).
$$

The absolute-value notation is essential for noninteger $2m$; a fractional power of a negative return is not the intended statistic. The paper sometimes writes an even-moment shorthand, while its general analysis concerns positive powers of absolute observations.

The proof first iterates the log recursion over a finite number of lags, exponentiates, and factors the expectation of the resulting product. It then establishes convergence of the infinite product. Near zero, $M(u)$ is close to one, with a first-order term involving $E[g(z)]$ and higher-order remainder. The geometric sequence of arguments makes the deviations summable when the needed exponential-integrability and moment conditions hold. This is why a finite truncation can evaluate the formula, although the truncation error must still be controlled numerically.

The intercept $a_0$ changes the scale of moments but cancels from standardized kurtosis and autocorrelations. This permits the paper's comparison tables to omit a numerical intercept. A researcher wishing to simulate returns at a particular variance level must nevertheless choose one. For example, under unit innovation variance a target unconditional variance $v$ implies, by algebraic inversion of the moment formula,

$$
a_0=(1-\beta)\bigl[\log v-\log P(1)\bigr].
$$

This normalization is a derived implementation option, not an estimated intercept in the article. It differs from simply setting the mean log variance to $\log v$, because exponentiation introduces a Jensen effect.

## Kurtosis and what its inequality assumes

The ordinary kurtosis, not excess kurtosis, is

$$
\kappa_4=\frac{\nu_4}{\nu_2^2}\frac{P(2)}{P(1)^2}
=\kappa_4(z)\prod_{j=0}^{\infty}\frac{M(2\beta^j)}{M(\beta^j)^2}.
$$

Each ratio is at least one by the second-moment inequality for $e^{\beta^jg(z)}$. The paper states strict inequality relative to innovation kurtosis. The appropriate qualification is that strictness requires nondegenerate stochastic scale; a constant $g$ can give equality. Finite transforms alone do not make a deterministic scale random.

For normal innovations and $\psi=0$, $g(z)=\phi z$ and

$$
P(a)=\exp\left(\frac{a^2\phi^2}{2(1-\beta^2)}\right),\qquad
\kappa_4=3\exp\left(\frac{\phi^2}{1-\beta^2}\right).
$$

All positive moments exist when $|\beta|<1$ in this Gaussian case, but they can be enormous. Existence should not be confused with easy estimation from a finite sample. The denominator $1-\beta^2$ makes the moment implications highly sensitive to persistence near one.

The comparison with ordinary GARCH is structural. Standard GARCH generally imposes increasingly restrictive coefficient conditions as the desired moment order rises. In normal EGARCH, every exponential moment needed for a finite order exists once the stable log recursion is specified, even though those moments grow rapidly. The authors note that this property relates to the moving-average conditional-heteroskedasticity structure; it is not a unique benefit of using the word “exponential.”

## General autocorrelation formula with implementable components

Let $X_t^{(m)}=|\varepsilon_t|^{2m}$ and define

$$
J_q(u)=E\bigl[|z|^q e^{u g(z)}\bigr],\qquad
B_n(m)=\prod_{j=0}^{n-2}M(m\beta^j),
$$

where $B_1(m)=1$ is an empty product. Equation (13), expressed in this notation, is

$$
\rho_n(m)=\frac{\nu_{2m}J_{2m}(m\beta^{n-1})B_n(m)P\bigl(m(1+\beta^n)\bigr)-\nu_{2m}^2P(m)^2}{\nu_{4m}P(2m)-\nu_{2m}^2P(m)^2},\qquad n\geq1.
$$

This expression is sufficient to compute every dependence statistic in the normal examples without implementing the paper's longer parabolic-cylinder formulas. The relevant moment assumptions include a finite $\nu_{4m}$, finite weighted exponential expectation $J_{2m}(m)$ in the stated theorem, and finite $M(2m)$, along with the intermediate transform arguments actually used. The denominator is the scale-free part of $\operatorname{Var}(X_t^{(m)})$ and must be positive for an autocorrelation to be defined.

The mixed expectation $J_{2m}$ is not replaceable by $\nu_{2m}M$. The earlier innovation appears twice: directly in the earlier observation and through its effect on subsequent log volatility. Omitting that shared-shock dependence is an easy implementation error and changes the answer, especially at short lags.

The proof in equations (A.5)–(A.7) separates three innovation sets. The contemporary $z_t$ contributes its ordinary moment. Innovations strictly between the two dates contribute $B_n(m)$. Innovations older than both observations affect the shared old variance and contribute the combined argument $m(1+\beta^n)$ in $P$. The boundary innovation at the earlier observation contributes $J_{2m}(m\beta^{n-1})$. Multiplying these independent pieces gives the cross moment; subtracting the squared mean and dividing by the variance gives the correlation. The common intercept factor cancels exactly.

This derivation also explains why the dependence of log-squared observations and that of squared observations differ. The log representation is linear in past news, whereas powers of the original scale combine news through products of exponential transforms. A single geometric coefficient in log space does not imply a constant ratio of successive autocorrelations after exponentiation.

## Evaluating the normal case without special-function ambiguity

For $z\sim N(0,1)$, write $c=\sqrt{2/\pi}$. Directly splitting the normal integral at zero gives

$$
M(u)=e^{-u\psi c}\left[e^{u^2(\psi+\phi)^2/2}\Phi\bigl(u(\psi+\phi)\bigr)+e^{u^2(\psi-\phi)^2/2}\Phi\bigl(u(\psi-\phi)\bigr)\right].
$$

Here $\Phi$ is the standard normal distribution function. An equally direct one-dimensional integral is

$$
J_q(u)=\frac{e^{-u\psi c}}{\sqrt{2\pi}}\int_0^\infty x^q e^{-x^2/2}\left[e^{u(\psi+\phi)x}+e^{u(\psi-\phi)x}\right]dx.
$$

Also $\nu_q=2^{q/2}\Gamma((q+1)/2)/\sqrt\pi$. These are algebraic reconstructions of the expectations underlying the appendix. They avoid possible normalization differences between special-function libraries and provide a clear route to quadrature. For $q=0$, the integral must agree with the closed form for $M$; at $u=0$, it must agree with $\nu_q$.

When $\psi=0$ and $m=1$, equation (17) gives a particularly useful exact check:

$$
\rho_n(1)=\frac{\left(1+\phi^2\beta^{2(n-1)}\right)\exp\left(\frac{\phi^2\beta^n}{1-\beta^2}\right)-1}{3\exp\left(\frac{\phi^2}{1-\beta^2}\right)-1}.
$$

The short-lag correction $1+\phi^2\beta^{2(n-1)}$ is part of the formula. Dropping it loses the direct contribution of the lagged shock. Under $0<\beta<1$, the authors can prove in this special squared-observation case that the local decay ratio is below $\beta$ at finite lag and tends to $\beta$ at large lag. Their broader analogous claim for other powers is explicitly described as a numerical conjecture, not a theorem established for the entire class.

## Numerical design and principal results

Table 1, p. 876, fixes $\beta=0.99$ and standard normal innovations. It varies $\phi$ over $0,-0.2,-0.4$ and $\psi$ over $0,0.3,0.6$, omitting the trivial constant-scale corner. For every parameter combination it evaluates kurtosis and, for $m=1,1/2,1/4$, the first autocorrelation and local ratios $\rho_2/\rho_1$ and $\rho_{51}/\rho_{50}$. These powers correspond respectively to squared returns, absolute returns, and square roots of absolute returns.

Selected reported values show the mechanism:

| $\phi$ | $\psi$ | Kurtosis | $\rho_1(1)$ | $\rho_2(1)/\rho_1(1)$ | $\rho_{51}(1)/\rho_{50}(1)$ |
|---:|---:|---:|---:|---:|---:|
| −0.2 | 0 | 22.4 | 0.309 | 0.976 | 0.983 |
| −0.4 | 0 | 9,310 | 0.357 | 0.921 | 0.951 |
| 0 | 0.3 | 19.2 | 0.385 | 0.975 | 0.982 |
| −0.2 | 0.3 | 483 | 0.417 | 0.940 | 0.965 |
| −0.4 | 0.3 | $6\times10^6$ | 0.422 | 0.840 | 0.911 |
| 0 | 0.6 | $1\times10^4$ | 0.497 | 0.907 | 0.946 |
| −0.2 | 0.6 | $2\times10^6$ | 0.485 | 0.844 | 0.916 |
| −0.4 | 0.6 | $4\times10^{12}$ | 0.457 | 0.699 | 0.834 |

The last row combines a log-volatility coefficient of 0.99 with an initial squared-return correlation ratio of only 0.699. That ratio has risen to 0.834 around lag 50 but is still well below 0.99. Reporting only the log-persistence parameter would obscure the early decay of the observable volatility proxy.

Lower powers can retain considerably stronger dependence. For $\phi=-0.4$, $\psi=0.6$, the first correlations for $m=1,1/2,1/4$ are 0.457, 0.694, and 0.818. Their first local ratios are 0.699, 0.942, and 0.982. At the lower-kurtosis combination $\phi=0$, $\psi=0.3$, the corresponding first correlations are 0.385, 0.455, and 0.421. Thus absolute returns need not dominate their square roots for every parameter value; the ordering changes with the distributional shape.

These are population implications calculated from the model, not sample autocorrelations with sampling standard errors. The paper supplies no Monte Carlo replication count or confidence interval for Table 1 because it is evaluating formulas. Finite samples from the very-high-kurtosis cases may give poor estimates of these population quantities even though all required moments exist mathematically.

## Matched comparison with ordinary GARCH

Figure 1 holds the asymptotic persistence parameter at 0.99 and compares models at ordinary kurtosis 20 and $10^6$. In symmetric EGARCH, $\phi=0$ and $\beta=0.99$, with $\psi=0.3032$ for kurtosis 20 and $\psi=0.7225$ for kurtosis $10^6$. In standard GARCH, the ARCH coefficients are 0.09196 and 0.09975, respectively, with the GARCH coefficient chosen so the sum is 0.99. Both use standard normal innovations. The intercept is irrelevant to the plotted standardized dependence.

At kurtosis 20, the squared-return autocorrelations have comparable magnitude, although EGARCH decays somewhat faster initially. At kurtosis $10^6$, the EGARCH squared-return curve falls sharply while the standard-GARCH curve changes much less in shape. The log-squared EGARCH series retains a geometrically decaying autocorrelation structure and can have a very different initial level. The figure therefore compares both model families and different transformations of the same family.

This experiment does not prove that EGARCH forecasts better. It establishes additional flexibility in the relationship between tail thickness and observable volatility dependence. Whether that flexibility is useful requires empirical estimation and evaluation absent from the paper. Nor does the limiting ratio near one establish true long memory: the illustrated first-order models ultimately have geometric dependence rates under the stated conditions.

## Generalized-error innovations and heavy-tail limits

The generalized-error distribution, GED, adds a tail-shape parameter $v$. In the paper's unit-variance normalization,

$$
f(z)=\frac{v\exp[-|z/\lambda|^v/2]}{\lambda 2^{1+1/v}\Gamma(1/v)},\qquad
\lambda=\left[2^{-2/v}\frac{\Gamma(1/v)}{\Gamma(3/v)}\right]^{1/2}.
$$

Normal innovations correspond to $v=2$. For $v>1$, the tail decay is sufficiently fast that the linear and absolute-linear exponential tilts used in $M$ and $J_q$ remain integrable for finite arguments. Corollary 5.4 and the appendix provide series expansions for those expectations. For implementation, evaluating the defining GED integrals and inserting them into the general autocorrelation formula is an alternative to the printed nested-series expression.

The ordinary absolute GED moment is

$$
\nu_q=2^{q/v}\lambda^q\frac{\Gamma((q+1)/v)}{\Gamma(1/v)}.
$$

The power $\lambda^q$ is required by a scale change of variable. The displayed appendix equation (A.18) prints only $\lambda$; the preceding integral formulas contain the corresponding powers. Likewise, equation (21) prints two identical $(\psi-\phi)^k$ terms, whereas the two half-lines require $(\psi-\phi)^k+(\psi+\phi)^k$, as shown in appendix equation (A.15). These are bounded transcription-level discrepancies verified against the page images and the defining integrals. The expectation-based implementation above avoids propagating them.

For $v\leq1$, the source warns that additional restrictions on news coefficients are needed for exponential moments. Student innovations with polynomial tails typically fail the required positive exponential-moment conditions for usual unbounded positive news responses, even when several ordinary innovation moments exist. One should check the actual signs and tails of $g$ rather than assert failure for every imaginable coefficient choice. Merely swapping normal innovations for Student innovations in an EGARCH simulator does not preserve the Gaussian moment conclusions.

## A computational recipe and the remaining reproducibility gaps

For the normal examples, choose the stated parameter grid and compute $M$, $J_q$, and $\nu_q$. Accumulate $\log P(a)=\sum_j\log M(a\beta^j)$ rather than multiplying many factors directly. Evaluate the finite $B_n$ products in log form as well. Increase the lag truncation until kurtosis and each target autocorrelation stabilize to a declared tolerance. The article does not report its truncation length, quadrature tolerances, floating-point precision, or evaluation library, so those are implementation choices that should be recorded.

The centering term $-\psi E|z|$ cancels from kurtosis and autocorrelation ratios, but retaining it consistently is a useful check and is necessary when computing levels of unconditional moments for a fixed intercept. In mixed-moment calculations, use the same innovation distribution and scaling everywhere. Normalizing innovations to variance one in one component and using an unnormalized GED scale in another produces apparently plausible but incorrect results.

Near zero transform arguments, use accurate small-number arithmetic for $\log M(u)$, and for differences of nearly equal exponentials use an `expm1`-style evaluation. At distant lags the cross moment approaches the squared mean; directly subtracting two large nearly equal products can destroy significant digits. In the highest-kurtosis cases, evaluate ratios after subtracting a common log scale to avoid overflow. These are numerical consequences of the displayed formulas, not a numerical algorithm specified by the authors.

Validation can use three identities with distinct purposes: $M(0)=1$ checks normalization, $J_q(0)=\nu_q$ checks weighted integration, and the exact $\psi=0$ squared-return formula checks the lag indexing and shared-shock term in the general expression. Check the code against Table 1 before exploring new innovation distributions, while distinguishing printed values from independently evaluated formulas. A numerical evaluation of the expectation-based equation (13) for this note reproduces the squared-observation rows to the displayed precision. Some fractional-power entries differ beyond rounding: at $\phi=-0.4$, $\psi=0.6$, and $m=1/2$, direct integration gives $\rho_1\approx0.70426$, whereas Table 1 prints 0.694. The table values quoted above remain the source's reported values; the integral formula provides a separate reproducible calculation. The source gives too little numerical implementation detail to determine the origin of that discrepancy. An optional simulated sample can check qualitative behavior, but it should not be expected to estimate kurtosis in the millions or trillions accurately at ordinary sample sizes.

The paper's conclusions concern the first-order family and require the stated moment existence. They do not provide estimation consistency, forecast-loss comparisons, transaction-cost results, or a universal theorem for every power's local decay ratio. The central usable result is more precise: transformed-return autocorrelations can be calculated from one-dimensional innovation expectations, and their shape can differ markedly from the persistence of log variance. That gives a reproducible way to assess what an EGARCH model actually implies for the volatility statistics observed in data.

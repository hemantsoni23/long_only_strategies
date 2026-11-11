# Modeling the Term Structure of Interest Rates: An Introduction

**Mark Fisher (2004).** Federal Reserve Bank of Atlanta, *Economic Review*, Third Quarter, pp. 41–62. Source: [YieldCurveModeling_Fisher_2004.pdf](../../Finance/YieldCurveModeling_Fisher_2004.pdf). All 22 PDF pages, including Appendices A–C, are covered. Printed page numbers below run from 41 to 62.

## Why this matters and what the article contributes

A yield curve combines forecasts of short interest rates, compensation for bearing risk, and the nonlinear conversion between bond prices and rates. Treating the curve as a pure forecast confounds these components. Fisher constructs a tractable example in which each component is explicit and bond prices satisfy no arbitrage. The result is useful as a reproducible reference implementation against which more elaborate term-structure models can be checked.

This is an expository article, not a claim to a new affine model or a new profitable trading strategy. Its central contribution is the route from a positive state-price deflator to bond pricing, using a finite time step throughout and then displaying continuous-time limits. The model is a discrete Gaussian short-rate specification closely related to Vasicek. A representative-agent appendix derives the deflator from consumption and inflation; another supplies the lognormal algebra; a third derives forecasts and their uncertainty. These are part of the implementation, not optional background.

The empirical exercise estimates short-rate dynamics and illustrates yield curves; it does not perform an out-of-sample bond-return test. Several printed formulas and calibration captions do not reproduce literally. This note identifies the discrepancies and follows the internally consistent primitive equations, while keeping reported results separate from reconstructed quantities.

## Time, prices, rates, and returns

Let $t$ be calendar time measured in years, $h>0$ one time step, $T=t+nh$ a maturity date, and $\tau=T-t=nh$. A default-free zero-coupon bond pays one unit at $T$ and has price $p(t,T)$, with $p(T,T)=1$. All rates are continuously compounded and annualized. A quoted 5% rate is entered as $0.05$.

The yield and the one-period short rate are

$$
y(t,T)=-\frac{\log p(t,T)}{T-t},\qquad r_t=-\frac{\log p(t,t+h)}h.
$$

The forward rate $f(t,T)$ applies to the future interval $[T-h,T]$, not the interval starting at $T$:

$$
f(t,T)=-\frac{\log p(t,T)-\log p(t,T-h)}h.
$$

Consequently,

$$
y(t,t+nh)=\frac1n\sum_{i=1}^n f(t,t+ih),\qquad
f(t,T)=y(t,T)+(T-t-h)\frac{y(t,T)-y(t,T-h)}h.
$$

The first identity is an arithmetic average of continuously compounded forward rates. As $h\to0$, it becomes the corresponding maturity integral; the second becomes $f=y+\tau\partial_Ty$. A forward contract can be synthesized by buying the longer bond and financing it with the shorter one, so the quoted forward is an enforceable borrowing/lending rate for that future interval, not intrinsically an expectation.

Fisher defines the conditional expected holding return by

$$
\mu(t,T)=\frac1h\log E_t\left[\frac{p(t+h,T)}{p(t,T)}\right].
$$

It is the log of an expected gross return. It differs from $E_t[\log(p(t+h,T)/p(t,T))]/h$ when returns are random. The one-period bond satisfies $\mu(t,t+h)=r_t$. The cash account obeys $B_{t+h}=B_te^{r_th}$: next-period growth is known today, whereas growth over several periods is uncertain because future short rates are unknown.

## The pricing object and no arbitrage

Write the strictly positive state-price deflator as $\pi_t$, distinct from the bond price $p(t,T)$. Its ratio $\pi_s/\pi_t$ is the stochastic discount factor. A future dividend rate $d(t+ih)$ produces a payment $h\,d(t+ih)$, and its ex-dividend value is

$$
v_t=E_t\left[\sum_{i=1}^{\infty}\frac{\pi_{t+ih}}{\pi_t}d(t+ih)h\right].
$$

The infinite sum requires integrability and convergence. A payment at maturity is entered as a lump sum, or as rate $1/h$ over the corresponding period; confusing rates of payment with payments introduces an unwanted factor of $h$.

For a self-financing portfolio that starts at $t$ and is liquidated at $T$, interim dividends are reinvested and additional financing is funded within the portfolio. Its value satisfies

$$
\pi_tv_t=E_t[\pi_Tv_T].
$$

If $v_t=0$, $v_T\ge0$, and positive terminal value has positive probability, strict positivity of $\pi_T$ contradicts the identity. This gives the direction of the no-arbitrage argument used in the article. The converse requires the appropriate asset-market setting; it is not a license to price arbitrary inadmissible trading strategies by an unrestricted martingale assertion.

In particular,

$$
p(t,T)=E_t[\pi_T/\pi_t].
$$

Bond pricing therefore follows from the deflator's dynamics. Different deflator components can be irrelevant for bonds if they multiply by a conditionally mean-one factor with the required independence or zero covariance; other asset classes can still depend on those components. An observed yield curve need not identify every part of an economy's discount factor.

A perpetuity paying one unit per year at discrete dates is worth $h\sum_{i\ge1}p(t,t+ih)$. For a constant rate $r>0$, this is $h/(e^{rh}-1)$, approaching $1/r$ as $h\to0$. The exclusion of a time-zero payment matters for this finite-step formula.

## Primitive dynamics and their units

The physical short-rate process is

$$
r_{t+h}=r_t+\kappa(\theta-r_t)h+\sigma_r\varepsilon_{t+h},\qquad
\varepsilon_{t+h}\overset{\mathrm{iid}}\sim N(0,h).
$$

Here $\kappa$ is the annual mean-reversion speed, $\theta$ the long-run short rate, and $\sigma_r$ the diffusion loading. Simulation uses $\varepsilon=\sqrt h\,Z$ with $Z\sim N(0,1)$. The conditional variance of the increment is $\sigma_r^2h$. An exact stationary discrete AR(1) exists when $|1-\kappa h|<1$; monotone decay of forecasts additionally uses $0<1-\kappa h<1$. The article works in that latter small-step regime.

The deflator is specified by

$$
\log\pi_{t+h}-\log\pi_t
=-\left(r_t+\frac{\lambda^2}{2}\right)h-\lambda\varepsilon_{t+h}.
$$

There is a single common shock and a constant price of risk $\lambda$. Both are substantive restrictions. By the normal moment-generating function, the conditional mean of the deflator ratio is $e^{-r_th}$, precisely the one-period bond price. The $\lambda^2/2$ correction is needed to make that equality hold.

**Source correction, pp. 47–48:** Eq. (13), Eq. (16), and the distribution stated after Eq. (18) divide stochastic increments by $h$ but print their variance without dividing by $h$. Under the explicitly defined $N(0,h)$ shock, the correct distribution is

$$
\frac{r_{t+h}-r_t}{h}\mid\mathcal F_t
\sim N\left(\kappa(\theta-r_t),\frac{\sigma_r^2}{h}\right),
$$

and likewise the deflator log-change divided by $h$ has variance $\lambda^2/h$. The later forecasting and estimation formulas use increment variances correctly. The note follows the primitive difference equations rather than the inconsistent annualized-distribution displays.

Suppose the bond's log-price increment is

$$
\Delta\log p=\left(\mu(t,T)-\frac{s(t,T)^2}{2}\right)h+s(t,T)\varepsilon_{t+h}.
$$

The signed loading $s$ may be negative. It is not a nonnegative standard deviation. The expected product of the deflator ratio and bond gross return equals one if and only if

$$
\mu(t,T)=r_t+\lambda s(t,T).
$$

To verify this, the product's log has mean $(\mu-r-\lambda^2/2-s^2/2)h$ and variance $(s-\lambda)^2h$. Adding half the variance leaves $(\mu-r-\lambda s)h$. This is the core risk-return restriction, obtained without designing separate arbitrage portfolios.

## Solving the affine model

Conjecture

$$
p(t,t+\tau)=\exp[-a(\tau)-b(\tau)r_t],\qquad a(0)=b(0)=0.
$$

The coefficients depend on maturity but not absolute calendar time. This excludes a deterministic time-varying drift introduced solely to fit today's curve. Define $\xi=\kappa\theta-\lambda\sigma_r$. Matching the risk-return restriction for every possible $r_t$ gives Fisher's Eqs. (29)–(30):

$$
\frac{a(\tau)-a(\tau-h)}h
=\xi b(\tau-h)-\frac12\sigma_r^2 b(\tau-h)^2,
$$

$$
\frac{b(\tau)-b(\tau-h)}h=1-\kappa b(\tau-h).
$$

These recursions are an especially transparent implementation. Starting at zero, update both from the old value of $b$; do not update $b$ first and then accidentally use the new value in the $a$ step. For $q=1-\kappa h$ and $\tau=nh$,

$$
b(nh)=\frac{1-q^n}{\kappa},\qquad
a(nh)=h\sum_{j=0}^{n-1}\left[\xi b(jh)-\frac12\sigma_r^2b(jh)^2\right].
$$

This finite sum is equivalent to the source's $K_1\xi+K_2\sigma_r^2$ expression and avoids cancellation in a long algebraic formula. For a one-step bond it gives $b(h)=h$, $a(h)=0$, and $p=e^{-r_th}$ exactly. It also gives a useful check at $\kappa=0$ by taking the recursion directly, rather than dividing by zero in a closed form.

In the continuous-time limit,

$$
b(\tau)=\frac{1-e^{-\kappa\tau}}\kappa,
$$

$$
a(\tau)=\xi\left[\frac\tau\kappa-\frac{1-e^{-\kappa\tau}}{\kappa^2}\right]
+\sigma_r^2\left[\frac{3+e^{-2\kappa\tau}-4e^{-\kappa\tau}}{4\kappa^3}-\frac\tau{2\kappa^2}\right].
$$

These solve $a'=\xi b-\sigma_r^2b^2/2$ and $b'=1-\kappa b$. They are exact for the continuous-time model and approximations to the finite-step model. Mixing their coefficients with an unrelated discrete transition should be an explicit approximation, not an unnoticed implementation choice.

Bond sensitivity is $\partial_r\log p=-b(\tau)$. Its one-step shock loading is $s(t,t+\tau)=-\sigma_rb(\tau-h)$, which uses the **remaining maturity after the step**. A positive short-rate shock lowers the price of a longer bond. The expected return obtained from the price dynamics is

$$
\mu=f(t,t+\tau)-b(\tau-h)\kappa(\theta-r_t)
+\frac12\sigma_r^2b(\tau-h)^2.
$$

This separates price roll-down, expected movement in the state, and the lognormal convexity correction. Substitution into $\mu-r=\lambda s$ recovers the recursions.

Only $(\kappa,\sigma_r,\xi)$ enter the cross-sectional bond-price solution. Consequently $\theta$ and $\lambda$ cannot be separately identified from a single curve under this specification. Physical time-series information is needed to identify $\theta$ and then infer $\lambda$.

## Expectations, risk compensation, and convexity

Appendix C gives

$$
E_t[r_{t+nh}]=\theta+q^n(r_t-\theta).
$$

The forward rate for the interval ending at $t+\tau$ decomposes as

$$
f(t,t+\tau)=E_t[r_{t+\tau-h}]
-\lambda\sigma_rb(\tau-h)-\frac12\sigma_r^2b(\tau-h)^2.
$$

The second term is risk compensation, the third a negative convexity adjustment. Both depend on the horizon but not on the date or state. Thus the model satisfies the weak expectations hypothesis: a forward equals the expected corresponding future short rate plus a constant horizon-specific premium. The strong hypothesis requires that premium to vanish, not merely that $\lambda=0$, because convexity can remain.

For small $h$ and weak mean reversion over the horizon, $b(\tau)\approx\tau$, giving the approximation $f\approx E_tr_{t+\tau}-\lambda\sigma_r\tau-\sigma_r^2\tau^2/2$. It explains the first-order slope and second-order curvature locally; it should not be extrapolated to arbitrary maturities because $b$ saturates at $1/\kappa$. The zero-coupon yield averages the forward decomposition over its $n$ intervals.

With $\sigma_r>0$, positive average short-end risk compensation requires $\lambda<0$. **A sign error in the accompanying prose on p. 51 should not be propagated:** the covariance between the deflator's log shock and the short-rate shock is $-\lambda\sigma_rh$, which is then positive, not negative. The deflator's covariance with the bond's log return is $-\lambda s h$ and is negative in this case. Distinguishing rate shocks from bond returns resolves the economic interpretation.

The limitation of constant premiums is severe. Changes in a fixed-maturity forward consist of forecast revisions plus a deterministic change in the horizon premium. There is no independent stochastic premium variation. Fisher proposes an additional state affecting the price of risk as a route toward the empirical failure of the expectations hypothesis, but does not solve or estimate that extended model.

## Estimation and uncertainty: what is actually reported

The exercise uses ten years of monthly zero-coupon Treasury yield-curve data from December 1987 through November 1997, derived from CRSP U.S. Treasury bond files. There are 120 observations and $N=119$ transitions, with $h=1/12$. The elapsed time between first and last observation is $Nh$, although the source counts $(N+1)h$ when describing the span represented by monthly observations. The article does not provide the raw observations or the full zero-curve construction and bond-exclusion protocol.

Define residuals

$$
e_i=r_{ih}-r_{(i-1)h}-\kappa(\theta-r_{(i-1)h})h.
$$

The three sample moment conditions are $\sum e_i=0$, $\sum r_{(i-1)h}e_i=0$, and $N^{-1}\sum e_i^2=\sigma_r^2h$. They can be implemented by OLS of $r_{ih}=A+Br_{(i-1)h}+e_i$, then

$$
\widehat\kappa=(1-\widehat B)/h,\qquad
\widehat\theta=\widehat A/(1-\widehat B),\qquad
\widehat\sigma_r=\sqrt{\frac1{Nh}\sum e_i^2}.
$$

The residual divisor is $N$ for these moments, not the degrees-of-freedom-adjusted OLS variance. This mapping is a reconstruction of Eqs. (37)–(39). A small $1-\widehat B$ makes the long-run mean imprecise. A negative estimated $\kappa$ is not stationary merely because the estimator returns a number.

Table 2 reports:

| Parameter | Estimate | Asymptotic standard error |
|---|---:|---:|
| Long-run rate $\theta$ | 0.050 | 0.030 |
| Reversion $\kappa$ | 0.124 | 0.217 |
| Diffusion loading $\sigma_r$ | 0.0086 | 0.0007 |

The standard errors use a Newey–West correction with five lags. The paper does not specify all finite-sample covariance conventions, but a reproducible choice is the usual Bartlett-weighted HAC covariance of the three moment vectors with lags 1–5 and the corresponding moment Jacobian. There is no reported holdout set, tuning search, forecast comparison, or transaction-cost calculation.

For a forecast $n$ steps ahead, the exact finite-step conditional variance is

$$
V_n=\sigma_r^2h\sum_{j=0}^{n-1}q^{2j}
=\frac{\sigma_r^2(1-q^{2n})}{2\kappa-\kappa^2h}.
$$

Its stationary limit is $\sigma_r^2/(2\kappa-\kappa^2h)$, approximated by $\sigma_r^2/(2\kappa)$. Forecast revisions are independent under the iid innovation assumption; a one-step revision for a target $n$ steps away is $q^{n-1}\sigma_r\varepsilon_{t+h}$. Summing their variances proves the formula. The exact half-life is $-h\log2/\log q$, approximately $\log2/\kappa$.

For the table estimates, the monthly-model half-life is about 5.561 years; Fisher reports the continuous approximation of 5.6 years. The stationary standard deviation is approximately 1.731 percentage points. The probability of a negative rate is about 0.002, as the article reports. Its discussion treats negative nominal rates as impossible under costless currency substitution; that is an assumption about market frictions in this illustration, not a mathematical restriction of the Gaussian model.

Starting at 1.25%, the mean at the half-life is 3.125%. Two conditional standard deviations are about 3 percentage points, excluding parameter uncertainty. The source's explicit interval of 0.4%–6.4% is inconsistent with its stated center and coefficients. Using the nearest monthly horizon, 67 months, gives a mean 3.130%, standard deviation 1.501 percentage points, and interval approximately **0.129%–6.132%**. These are reconstructed values, not a revised author estimate. Wide standard errors on $\kappa$ and $\theta$ mean that conditional process uncertainty is only part of forecast uncertainty.

## Recovering inference and risk-neutral dynamics from the same primitives

The reported five-lag covariance correction can be made operational by collecting the moment vector

$$
g_i(\vartheta)=\left(e_i,\ r_{i-1}e_i,\ e_i^2-\sigma_r^2h\right)^\top,
\qquad \vartheta=(\kappa,\theta,\sigma_r)^\top,
$$

where $r_{i-1}$ abbreviates the previous monthly observation. The residual derivatives are $\partial_\kappa e_i=-(\theta-r_{i-1})h$, $\partial_\theta e_i=-\kappa h$, and $\partial_{\sigma_r}e_i=0$. Accordingly, the third moment's first two derivatives are $2e_i$ times the residual derivatives, and its last derivative is $-2\sigma_rh$. These specify the sample moment Jacobian $D=N^{-1}\sum_i\partial g_i/\partial\vartheta^\top$ without numerical differentiation.

With moment lag covariance matrices $\widehat\Gamma_\ell$, the usual five-lag Bartlett choice is $S=\widehat\Gamma_0+\sum_{\ell=1}^5(1-\ell/6)(\widehat\Gamma_\ell+\widehat\Gamma_\ell^\top)$. In this exactly identified system, the asymptotic parameter covariance estimate is $D^{-1}S(D^{-1})^\top/N$. Centering and finite-sample denominator conventions should be retained in a replication log because the article does not fully specify them. This elaborates its moment estimator; it does not claim recovery of the unprovided original implementation.

A second useful deduction concerns pricing versus forecasting. Normalize the one-period deflator by its conditional mean to form

$$
\frac{\pi_{t+h}/\pi_t}{e^{-r_th}}
=\exp\left(-\lambda\varepsilon_{t+h}-\frac12\lambda^2h\right).
$$

This exponential tilt gives the innovation mean $-\lambda h$ under the one-step risk-neutral transition while preserving its variance $h$. Hence the pricing transition for the short rate has conditional drift

$$
\kappa(\theta-r_t)-\lambda\sigma_r=\xi-\kappa r_t.
$$

For $\kappa>0$, its long-run level is $\theta^Q=\theta-\lambda\sigma_r/\kappa$. Discounting at the current short rate and averaging tomorrow's affine bond price under this transition reproduces the same $a,b$ recursions. This is a derived cross-check on the deflator approach. It makes the identification issue explicit: curve prices identify pricing drift, while historical rate forecasts require the physical drift. Using $\theta^Q$ to forecast actual future rates would turn a risk-premium adjustment into a spurious change in expected monetary conditions.

## Yield-curve illustrations and a calibration discrepancy

Figures 1–2 use a curve dated July 29, 1994. Figure 3 compares reversion speeds 0.01, 0.10, and 1.00 with a long-run rate of 5%. Its caption states a current rate of 1%, but the plotted paths start near 9% and decline toward 5%. Starting at 1% instead produces increasing paths; this additional caption mismatch should be recorded when reproducing the figure. Figure 6 uses the time-series estimates, a current rate of 5%, and prices of risk $-1,-0.5,0,0.5,1$. The curve for $\lambda=-0.5$ is described as reasonably plausible, but the model does not fit every feature of the data. The figures are illustrations, not confidence bands for estimated yield curves.

Figures 7–8 claim an alternative fit to the average curve with $\kappa=0.203$, $\sigma_r=0.0041$, $\theta=0.050$, and $\lambda=-0.245$, using current rates 5% and 1%, respectively. The article supplies no objective function, maturity weights, curve sample definition, optimizer, or standard errors for that fit.

More seriously, the printed coefficients do not reproduce the plotted yield levels. At $h=1/12$, the exact coefficient recursions give 30-year yields of **5.398%** and **4.743%** for Figures 7 and 8, respectively. The curves shown approach roughly 7.7% and 7.0% by 30 years. The continuous-time limiting yield implied by the printed parameters is only

$$
y_\infty=\theta-\frac{\lambda\sigma_r}{\kappa}-\frac{\sigma_r^2}{2\kappa^2}
\approx5.4744\%.
$$

Thus the mismatch is far too large to attribute to the monthly approximation. A changed volatility digit can materially alter the curve, but the actual intended parameters are not established by the source. A faithful implementation should preserve the captions as reported, record its own reconstructed curve, and flag the unresolved discrepancy rather than silently tuning parameters to match a picture.

## Representative-agent construction: Appendix A

A representative agent has expected discounted utility of consumption flow $c_t>0$, with time preference $\delta$ and CRRA coefficient $\gamma>0$. Utility is $(c^{1-\gamma}-1)/(1-\gamma)$ for $\gamma\ne1$, and $\log c$ for $\gamma=1$. The first-order condition for feasible marginal investment-induced changes in consumption yields the real deflator

$$
\widehat\pi_t=e^{-\delta t}c_t^{-\gamma}.
$$

With price level $z_t>0$, nominal asset values and dividends equal their real counterparts times $z_t$, whereas the nominal deflator is **divided** by $z_t$:

$$
\pi_t=e^{-\delta t}c_t^{-\gamma}/z_t.
$$

This reciprocal conversion preserves the pricing equation. The text before Eq. (A.10) accidentally writes $-z_t$ rather than $-\log z_t$ in $\log\pi_t$; Eq. (A.10) itself correctly uses log-price-level increments.

Assume the same normal shock drives log consumption growth, inflation, and expected inflation:

$$
\Delta\log c=\mu_ch+\sigma_c\varepsilon,\qquad
\Delta\log z=x_th+\sigma_z\varepsilon,
$$

$$
x_{t+h}-x_t=\kappa_x(\theta_x-x_t)h+\sigma_x\varepsilon.
$$

Here $\mu_c$ and $x_t$ are expected **log** growth rates; log expected gross inflation instead equals $x_t+\sigma_z^2/2$. Matching the deflator dynamics gives

$$
\lambda=\gamma\sigma_c+\sigma_z,\qquad
r_t=\delta+\gamma\mu_c+x_t-\frac12(\gamma\sigma_c+\sigma_z)^2.
$$

Therefore $\kappa=\kappa_x$, $\sigma_r=\sigma_x$, and $\theta=\delta+\gamma\mu_c+\theta_x-(\gamma\sigma_c+\sigma_z)^2/2$. Shock loadings can have signs; imposing all of them positive would rule out the negative nominal price of risk used in some curve illustrations.

The real rate and real price of risk are constants:

$$
\widehat r=\delta+\gamma\mu_c-\frac12\gamma^2\sigma_c^2,
\qquad \widehat\lambda=\gamma\sigma_c.
$$

Combining them gives the uncertainty-adjusted Fisher equation

$$
r_t=\widehat r+x_t-\widehat\lambda\sigma_z-\frac12\sigma_z^2.
$$

The covariance term reflects consumption-inflation comovement under the common shock. The variance term follows from the log-growth convention. Preferences link risk aversion and intertemporal substitution through the same $\gamma$; the article notes that recursive preferences can separate them, but does not implement that extension.

Real zero-coupon prices are $\widehat p(t,T)=e^{-\widehat r(T-t)}$, so real yields are flat and real bonds have no stochastic holding-return component in this special economy. The intermediate real-price ansatz on p. 58 drops an exponential; the terminal solution makes the intended form unambiguous. This real-curve flatness is a model consequence, not an empirical finding about inflation-indexed bonds.

## A reproducible implementation and its limits

A minimal implementation stores the step size and compounding conventions with the parameters. It estimates the AR(1) from consecutive monthly short-rate observations, maps coefficients to $(\kappa,\theta,\sigma_r)$, and computes the specified HAC uncertainty. Given a chosen or separately calibrated $\lambda$, it builds $a,b$ on a maturity grid, prices zero coupons, and derives yields and forwards from prices. It then verifies $p(t,t)=1$, $p(t,t+h)=e^{-r_th}$, the forward-average yield identity, the risk-return restriction, and the analytic forecast mean and variance.

For simulation, draw one normal innovation per date and reuse it in the short rate, deflator, and bond evolution. Drawing independent shocks for these objects breaks the intended covariance and pricing restriction. A Monte Carlo estimate of the deflator-weighted bond gross return should converge to one. This is a diagnostic implied by the model; the article does not report such a simulation or prescribe its replication count.

The supplied formulas are sufficient to reproduce the analytical model, estimation moments, and several numerical illustrations. They are insufficient to reproduce every market-data chart exactly because the underlying zero curves, filters, fitting loss, and some intended caption values are absent or inconsistent. The Gaussian specification permits negative rates, a constant risk price rules out stochastic premiums, one factor forces perfect instantaneous comovement across maturities, and constant coefficients omit regime shifts. No conclusion about trading profitability, hedging performance under costs, or out-of-sample forecasting follows from the illustrations. The useful deliverable is a transparent baseline with explicit price, forecast, and risk-premium accounting—and a clear record of the details that require additional evidence before empirical deployment.

# Leverage Effect, Volatility Feedback, and Self-Exciting Market Disruptions

Peter Carr and Liuren Wu (2017), *Journal of Financial and Quantitative Analysis* 52(5), 2119–2156. [Main source PDF](../../Finance/leverage_effect_volatility_feedback_and_selfexciting_market_disruptions.pdf). The complete 38-page article and the 20-page [publisher's Internet Appendix](https://static.cambridge.org/content/id/urn:cambridge.org:id:article:S0022109017000564/resource/name/S0022109017000564sup001.zip) were read. The appendix supplies the pricing transform, quadrature, filtering algorithm, and model-comparison results.

## Why this matters

A negative relation between equity returns and volatility does not identify financial leverage as its cause. The same relation can arise from repricing systematic business risk or from negative jumps that raise subsequent crash risk. Carr and Wu build a three-state option model that assigns different dynamics to these channels and uses the maturity and strike dimensions of the option surface to distinguish them.

The model combines a CEV leverage factor, a square-root diffusion variance factor, and a self-exciting negative-jump factor. Its tractability comes from making the leverage innovation independent of the risky-asset innovations under the pricing measure, then integrating an affine asset-option price over the leverage distribution. The result connects an economically motivated decomposition to an implementable option-pricing and filtering system.

The interpretation remains conditional on the model. Option data identify a standardized equity-to-risky-asset ratio, not raw balance-sheet leverage. The five-company exercise is deliberately small and illustrative. Strong in-sample pricing performance does not independently establish causal capital-structure behavior, and the estimated error dependence limits conventional likelihood-based inference.

## Economic decomposition and identified scale

Let $F_t$ be the forward equity value over a fixed horizon, $A_t$ the forward value of risky assets, and $X_t=F_t/A_t$ the equity-to-risky-asset ratio:

$$
F_t=X_tA_t.
$$

This identity alone is not a structural model. The restrictions on the dynamics give it content. Cash can offset debt in the risky-asset accounting interpretation, so $X_t$ need not be bounded above by one. A larger $X_t$ means less financial leverage relative to risky assets.

Under the physical measure, the leverage ratio follows

$$
\frac{dX_t}{X_t}
=X_t^{-p}(a_X-\kappa_{XX}X_t-\kappa_{XZ}v_t^Z-\kappa_{XJ}v_t^J)\,dt
+\delta X_t^{-p}dW_t.
$$

Here $p>0$ governs the elasticity of equity volatility to the leverage ratio, $\delta>0$ sets its volatility scale, and the drift permits active capital-structure adjustment. Positive $\kappa_{XX}$ tends to restore $X$ toward a conditional target. Positive $\kappa_{XZ}$ means that greater diffusion risk lowers $X$, increasing leverage; negative $\kappa_{XJ}$ means that greater crash risk raises $X$, reducing leverage.

Under the risk-neutral measure, the ratio has zero drift:

$$
dX_t=\delta X_t^{1-p}dW_t.
$$

The Brownian motion $W$ is independent of the risky-asset Brownian shocks. The pricing construction also treats the leverage and asset components as independent conditional on their current states. This is a substantive restriction, not a consequence of the balance-sheet identity.

Options identify

$$
\widetilde X_t=\delta^{-1/p}X_t,\qquad
v_t^X=\delta^2X_t^{-2p}=\widetilde X_t^{-2p}.
$$

They cannot separately identify $X_t$ and $\delta$. With standardized coefficients

$$
\widetilde a_X=a_X/\delta,\quad
\widetilde\kappa_{XX}=\delta^{(1-p)/p}\kappa_{XX},\quad
\widetilde\kappa_{XZ}=\kappa_{XZ}/\delta,\quad
\widetilde\kappa_{XJ}=\kappa_{XJ}/\delta,
$$

the standardized ratio has unit diffusion scale. A time-varying true leverage volatility would further mix raw leverage changes and scale changes in the extracted factor. The paper explicitly recognizes this identification limitation.

Applying Itô's formula under the pricing measure gives

$$
dv_t^X=p(2p+1)(v_t^X)^2dt-2p(v_t^X)^{3/2}dW_t.
$$

Thus a CEV ratio becomes a constrained $3/2$ variance process. The leverage contribution to equity return and its own variance innovation are perfectly negatively correlated. This is not an unrestricted $3/2$ model: its drift and diffusion coefficients are linked by the single parameter $p$.

## Risky-asset diffusion, self-exciting jumps, and measure changes

Use $z_t=v_t^Z$ for diffusion variance and $j_t=v_t^J$ for jump activity. To avoid confusing the activity state with the jump-size parameter, write $\nu=v_J$ and $\nu_P=v_J^P$. For negative log jumps $x<0$, define

$$
\pi_Q(x)=e^{-|x|/\nu}|x|^{-1},\qquad
\pi_P(x)=e^{-|x|/\nu_P}|x|^{-1}.
$$

The compensator of the jump random measure $\mu(dx,dt)$ under measure $M$ is $j_t\pi_M(x)\,dx\,dt$. Under $Q$,

$$
\frac{dA_t}{A_{t-}}
=\sqrt{z_t}\,dZ_t+
\int_{-\infty}^0(e^x-1)\{\mu(dx,dt)-j_t\pi_Q(x)\,dx\,dt\},
$$

$$
dz_t=\kappa_Z(\theta_Z-z_t)dt+\sigma_Z\sqrt{z_t}\,dZ_t^v,
\qquad d\langle Z,Z^v\rangle_t=\rho\,dt,
$$

$$
dj_t=\kappa_J(\theta_J-j_t)dt
-\sigma_J\int_{-\infty}^0x\{\mu(dx,dt)-j_t\pi_Q(x)\,dx\,dt\}.
$$

A negative log jump $x$ raises activity by $-\sigma_Jx>0$, increasing the chance of further negative jumps. The diffusion feedback channel is represented by $\rho<0$. Calling it feedback is an economic interpretation of the covariance restriction; the SDE does not separately observe the cost-of-capital mechanism.

This is an infinite-activity, finite-variation negative-jump specification: $\int\pi_Q(x)\,dx$ diverges near zero, but $\int|x|\pi_Q(x)\,dx=\nu$ is finite. Accordingly, $j_t$ is an activity multiplier rather than a finite Poisson event rate, and $\nu$ is a jump-size scale rather than the mean of a normalized distribution over all jumps. The article's informal “average jump size” terminology should not be implemented as a compound-Poisson process with mean jump $\nu$.

The physical equations have the corresponding compensated-jump terms, physical mean-reversion parameters, and an asset-return risk premium. Diffusion and jump risk prices imply

$$
\kappa_Z=\kappa_Z^P+\gamma_v\sigma_Z,\qquad
\kappa_Z\theta_Z=\kappa_Z^P\theta_Z^P,
$$

$$
\nu=\frac{\nu_P}{1-\gamma_J\nu_P},\qquad
\kappa_J=\kappa_J^P+\sigma_J(\nu_P-\nu),\qquad
\kappa_J\theta_J=\kappa_J^P\theta_J^P.
$$

The denominator in the jump-scale transformation must be positive. For replication from the reported risk-neutral parameters and risk prices, use $\nu_P=\nu/(1+\gamma_J\nu)$ and then recover the physical mean-reversion speeds. The independent Brownian asset-return risk price $\gamma_Z$ affects the physical asset drift but is not identified as a separately reported parameter in the option-only estimation.

The aggregate equity-forward dynamics combine the two independent diffusions and the asset jumps:

$$
\frac{dF_t}{F_{t-}}
=\sqrt{v_t^X}\,dW_t+\sqrt{z_t}\,dZ_t+
\int_{-\infty}^0(e^x-1)\{\mu-j_t\pi_Q(x)\,dx\,dt\}.
$$

For log-return quadratic variation, the instantaneous contribution is

$$
v_t^X+z_t+\nu^2j_t,
$$

because $\int x^2\pi_Q(x)\,dx=\nu^2$. This is the variance convention used in the reported decomposition. The exact instantaneous variance of the simple relative-return jump term instead uses

$$
j_t\int(e^x-1)^2\pi_Q(x)\,dx
=j_t\{2\log(1+\nu)-\log(1+2\nu)\}.
$$

For the estimated SPX scale $\nu=0.1951$, these factors are $0.038064$ and $0.027012$, respectively. They coincide only to leading order for small jumps. The reported $\nu^2j_t$ numbers are preserved as log-jump variation, rather than silently interpreted as exact simple-return variance.

## Pricing algorithm from the Internet Appendix

Conditional independence under $Q$ permits iterated expectations. If $C(A,K,T)$ is the forward value of a call on the risky asset, then the equity call is

$$
c(F_t,K,T)=E_t^Q[X_TC(A_t,K/X_T,T)].
$$

Compute the risky-asset option first, then integrate over the CEV ratio distribution. Discount the resulting forward option value with the relevant discount factor to obtain a present value. The source's estimation uses forward option values, so mixing discounted prices with forward vegas would change the objective.

For $\tau=T-t$, the characteristic function of log asset returns is

$$
\phi(u)=E_t^Qe^{iu\log(A_T/A_t)}
=\exp[-a_Z(\tau)-b_Z(\tau)z_t-a_J(\tau)-b_J(\tau)j_t].
$$

All four coefficients start at zero. They solve

$$
b_Z'=\psi_Z(u)-\kappa_Z^M b_Z-\tfrac12\sigma_Z^2b_Z^2,\qquad
a_Z'=\kappa_Z\theta_Zb_Z,
$$

$$
b_J'=\psi_J(u)-(\kappa_J+\sigma_J\nu)b_J+
\log(1+\sigma_Jb_J\nu^M),\qquad
a_J'=\kappa_J\theta_Jb_J,
$$

where

$$
\psi_Z(u)=\tfrac12(iu+u^2),\quad
\kappa_Z^M=\kappa_Z-iu\rho\sigma_Z,\quad
\psi_J(u)=\log(1+iu\nu)-iu\log(1+\nu),\quad
\nu^M=\frac{\nu}{1+iu\nu}.
$$

The diffusion Riccati system has a closed form. With $\xi=\sqrt{(\kappa_Z^M)^2+2\sigma_Z^2\psi_Z}$ and a consistent complex branch,

$$
b_Z(\tau)=
\frac{2\psi_Z(1-e^{-\xi\tau})}
{2\xi-(\xi-\kappa_Z^M)(1-e^{-\xi\tau})},
$$

$$
a_Z(\tau)=\frac{\kappa_Z\theta_Z}{\sigma_Z^2}
\left[
2\log\left(1-\frac{\xi-\kappa_Z^M}{2\xi}(1-e^{-\xi\tau})\right)
+(\xi-\kappa_Z^M)\tau
\right].
$$

The appendix uses fourth-order Runge–Kutta for the jump coefficients. Frequency-grid and time-step refinement are required numerical checks. At $u=0$ the transform must equal one; at $u=-i$ it must also equal one in the martingale domain. Both checks follow from the zero values of the corresponding exponents.

Let $k=\log(K/A_t)$ and $c_A(k)=C(A_t,K,T)/A_t$. Its damped transform is

$$
\chi(u)=\frac{\phi(u-i)}{(iu)(iu+1)}.
$$

For admissible $\alpha>0$, a directly implementable inversion is

$$
c_A(k)=\frac{e^{-\alpha k}}{\pi}
\operatorname{Re}\int_0^\infty e^{-iuk}\chi(u-i\alpha)\,du.
$$

The real-part operator is necessary in a one-sided complex integral. On a grid $u_m=m\eta$, $k_\ell=-b+\lambda\ell$, $\lambda=2\pi/(\eta N)$, $b=\lambda N/2$, a consistent FFT implementation is

$$
c_A(k_\ell)\approx
\frac{e^{-\alpha k_\ell}\eta}{\pi}
\operatorname{Re}\sum_{m=0}^{N-1}
w_m e^{iu_mb}\chi(u_m-i\alpha)e^{-2\pi im\ell/N}.
$$

The initial trapezoid weight is one half, with the high-frequency endpoint handled consistently with the chosen truncation. This expression is derived from the inversion. Printed equation A-17 changes the Fourier-exponent sign and places a strike-index-dependent damping factor inside a purported frequency-only vector. The formula above fixes the convention explicitly; it is not a claim about the authors' actual code. Damping requires finite moments on the chosen contour, and numerical branch continuity must be checked.

For $x>0$, the appendix gives the CEV transition density

$$
f(x\mid X_t)=
\frac{x^{2p-3/2}X_t^{1/2}}{\delta^2p\tau}
\exp\left[-\frac{X_t^{2p}+x^{2p}}{2\delta^2p^2\tau}\right]
I_{1/(2p)}\left(\frac{X_t^px^p}{\delta^2p^2\tau}\right).
$$

For numerical stability, replace $I_\nu(s)$ by its exponentially scaled version $e^{-s}I_\nu(s)$ and replace the exponent by $-(X_t^p-x^p)^2/(2\delta^2p^2\tau)$. This avoids multiplying an exponentially large Bessel value by an exponentially small factor.

Boundary treatment matters. The positive-state density need not integrate to one; it corresponds to a possible absorbing mass at zero. As a derived check, when $p=\delta=X_t=\tau=1$, the density reduces to the difference of two normal densities, integrates to $0.682689$, and has first moment one. The missing probability is at zero. A positive-strike call receives zero payoff there, so the integral over positive $x$ is sufficient; renormalizing that density would misprice the call.

The appendix maps Gauss–Hermite nodes $s_j$ to $x_j=X_t\exp(\sqrt{2V_X}s_j-V_X/2)$ and uses weights

$$
W_j=f(x_j\mid X_t)x_j\sqrt{2V_X}\,e^{s_j^2}w_j,\qquad
c(F_t,K,T)\approx\sum_jW_jx_jC(A_t,K/x_j,T).
$$

For the standardized ratio, $\delta=1$ and $V_X=\widetilde X_t^{-2p}\tau$ as printed. If working with unstandardized $X$, the frozen instantaneous variance is $\delta^2X_t^{-2p}\tau$. The lognormal map chooses quadrature locations; it does not replace the CEV density. The number of nodes, FFT resolution, damping value, interpolation rule, and ODE tolerances are not reported.

## Estimation as an approximate state-space system

The filtered state is $V_t=(\widetilde X_t,z_t,j_t)'$. Weekly spacing is $\Delta=7/365$ years. The conditional mean used in the Euler approximation is

$$
f(V)=
\begin{pmatrix}
\widetilde X+\widetilde X^{1-p}
(\widetilde a_X-\widetilde\kappa_{XX}\widetilde X-\widetilde\kappa_{XZ}z-\widetilde\kappa_{XJ}j)\Delta\\
\kappa_Z\theta_Z\Delta+(1-\kappa_Z^P\Delta)z\\
\kappa_J\theta_J\Delta+(1-\kappa_J^P\Delta)j
\end{pmatrix}.
$$

Its innovation covariance is approximated by a diagonal matrix with entries

$$
\widetilde X^{2-2p}\Delta,\qquad
\sigma_Z^2z\Delta,\qquad
\sigma_J^2\nu_P^2j\Delta.
$$

The printed first row of equation (21), also A-25, uses time-$t$ ratio terms inside a forecast based on time $t-1$. The expression above evaluates every state on the previous state vector, as required by the stated Euler transition. This indexing reconstruction is explicit.

Observations are out-of-the-money forward option prices divided by Black–Scholes vega. The model prices undergo the same scaling. Measurement errors are assumed iid normal with a common variance. This makes approximate implied-volatility errors receive comparable weight, rather than allowing high-vega option prices to dominate solely by scale.

For three states, the unscented filter uses seven sigma points. Given posterior mean $m$ and covariance $P$, take $m$, and $m\pm$ each column of $\sqrt{(3+\eta)P}$. Weights are $\eta/(3+\eta)$ for the center and $1/[2(3+\eta)]$ for each remaining point, with $\eta>0$. Propagate the points through $f$, form their weighted mean and covariance, and add the process-noise covariance. Regenerate sigma points from that predicted state distribution before evaluating the option-pricing map.

If predicted observations have mean $\bar y$, covariance $S$, and state–observation covariance $C$, update using

$$
K=CS^{-1},\qquad
\widehat V=\bar V+K(y-\bar y),\qquad
\widehat P=P^- -KSK'.
$$

The quasi-log likelihood, apart from parameter-independent constants, is

$$
\ell_t=-\tfrac12\log|S_t|
-\tfrac12(y_t-\bar y_t)'S_t^{-1}(y_t-\bar y_t).
$$

Maximize its sum over weeks. The paper has nine pricing parameters and six additional physical-dynamics parameters, as well as the measurement-error variance needed by the filter. Pricing parameters mainly govern the average surface; physical dynamics are identified through its time series. This division is a useful interpretation, not strict statistical separability.

The filter is approximate in two ways: Euler discretization of nonlinear and jump states, and Gaussian moment closure by sigma points. It is not the exact likelihood of the continuous-time model. Positivity of sigma points and filtered states requires explicit numerical handling; the source does not report that handling, initial state/covariance, the chosen $\eta$, optimizer settings, or starting values. The fitted square-root parameters also violate the strict Feller inequality: $2\kappa_Z\theta_Z=0.15123<\sigma_Z^2=0.35748$. The continuous-time variance can reach zero, so silently assuming a strictly positive interior process is inappropriate.

## Data and empirical design

The SPX estimation uses proprietary OTC implied-volatility quotes from a major bank, January 8, 1997–October 29, 2014, sampled each Wednesday. At every date there are eight maturities—1, 3, 6, 12, 24, 36, 48, and 60 months—and five strikes at 80%, 90%, 100%, 110%, and 120% of spot. The balanced panel has 930 weeks and 37,200 observations. Long maturities are central to identification of the persistent leverage and jump channels.

The individual-company sample uses OptionMetrics options for GE, WMT, JPM, DUK, and XOM. The authors choose out-of-the-money puts below spot and calls above spot, retain maturities over 21 days, and filter log strike relative to forward to lie within two standard deviations of its mean. The exact volatility normalization for that filter is not fully operationalized in the main text. OptionMetrics American-option implied volatilities are converted into European Black–Scholes prices before fitting; the model does not directly price early exercise.

Counts are 71,344 options for JPM, 54,859 for WMT, 52,918 for XOM, 52,592 for GE, and 22,785 for DUK. The listed-stock sample is concentrated below one year and has maximum maturities below three years. This differs materially from the five-year OTC index panel, so apparent cross-sectional differences can partly reflect information coverage.

The descriptive three-month volatility level averages the standardized 50-delta call and put volatilities. The positive skew statistic is the 25-delta put volatility minus the 25-delta call volatility, divided by that level and by $1.349=\Phi^{-1}(.75)-\Phi^{-1}(.25)$, expressed as a percentage. A larger positive statistic corresponds to a more negative conventional implied-volatility slope.

For OTC options, the analogous skew uses 80% minus 120% strike volatility, relative to the 100% strike level, divided by the distance in standardized moneyness $\log(K/S)/(IV\sqrt{\tau})$. The Table 3 caption abbreviates the normalization; the accompanying prose supplies the division by the ATM volatility level. This statistic is a smile-slope proxy, not the standardized third moment of the return distribution.

SPX ATM mean volatility rises from 19.19% at one month to 23.52% at five years, while its time-series standard deviation declines from 7.74 to 4.37 percentage points. The correlation of weekly returns with weekly changes in volatility is $-.81$ at one month, $-.83$ at three months, and $-.60$ at five years. Mean percentage skew rises from 16.30 to 25.06; its return-change correlation is most negative at three months, $-.34$, and approximately zero by three years.

## Estimated mechanisms and quantitative implications

The principal SPX estimates are:

| Channel | Parameters |
|---|---|
| Standardized leverage | $p=3.4922$, $\widetilde\kappa_{XX}=0.0000$, $\widetilde\kappa_{XZ}=17.4087$, $\widetilde\kappa_{XJ}=-0.0743$, $\widetilde a_X=0.0009$ |
| Diffusion variance | $\rho=-0.8879$, $\kappa_Z=3.0125$, $\theta_Z=0.0251$, $\sigma_Z=0.5979$, $\gamma_v=-17.8608$ |
| Jump activity | $\nu=0.1951$, $\kappa_J=0.0010$, $\kappa_J\theta_J=0.1155$, $\sigma_J=5.6460$, $\gamma_J=0.4513$ |

The paper reports very small standard errors, including values rounded to zero. For example, the standard errors for $p,\rho,\kappa_Z,\sigma_Z,\gamma_v,\sigma_J,\gamma_J$ are $.0084,.0023,.0089,.0019,.0731,.0107,.0006$. These are model-based estimates from an approximate likelihood with acknowledged error dependence, not evidence that all economic uncertainty is negligible.

From the reported values, the risk-neutral diffusion half-life is about $0.2301$ years. The risk-neutral jump-activity half-life is approximately 693 years; this conveys near-zero estimated mean reversion over the data horizon, rather than a credible forecast over centuries. Recovering physical parameters gives $\nu_P\approx0.179312$, $\kappa_J^P\approx0.090140$, and $\kappa_Z^P\approx13.69147$. The corresponding physical diffusion long-run mean is approximately $0.005523$. These are derived from rounded estimates, not separately reported point estimates.

Average variance contributions are $0.0115$ from leverage, $0.0257$ from diffusion, and $0.0168$ from log jumps. Their square roots are approximately 10.73%, 16.04%, and 12.96% annualized volatility. They are not additive volatilities: the variance total is $0.0540$, whose square root is 23.24%. The shares are approximately 21.3%, 47.6%, and 31.1%.

The state-shock exercise moves one factor from its sample mean to its 10th or 90th percentile while holding the other factors at their means. Greater leverage raises volatility broadly across maturities, with a relatively persistent effect. Diffusion variance shocks affect short maturities most strongly and dissipate quickly. Jump-activity shocks raise low-strike volatility more than high-strike volatility and have their largest term-structure response around three to six months. These are model comparative statics, not estimated causal impulse responses with orthogonalized empirical shocks.

The extracted factor history associates the 1998 crisis particularly with jump activity and the 2008–2009 crisis with both diffusion and jump risk. Such historical interpretation depends on the chosen three-factor model and the option panel. Figure 2's third panel is the activity state $j_t$, not directly $\nu^2j_t$, despite its variance-oriented caption.

## Variance risk compensation and cross-sectional evidence

The paper reports several different physical-minus-risk-neutral quantities. Leverage-variance drifts average $0.0089$ under $P$ and $0.0050$ under $Q$, a difference $+0.0039$. The diffusion-variance drift difference $\gamma_v\sigma_Zz_t$ averages $-0.2746$. The physical and risk-neutral log-jump variance levels average $0.0142$ and $0.0168$, a difference $-0.0026$. The jump-activity drift difference averages $-0.0393$.

These are not four numbers that can be added to obtain a variance-swap premium: some are variance levels, some variance-state drifts, and one is an activity drift that must be multiplied and propagated appropriately. Finite-horizon compensation requires integrating the relevant conditional dynamics under each measure and matching the instrument's payoff. The reported decomposition supports the claim that diffusion and crash channels contribute negative compensation while the leverage channel need not, within the model.

Across the five stocks, the estimated leverage powers are $3.8216$ for GE, $2.6433$ for WMT, $1.6368$ for JPM, $1.1315$ for DUK, and $0.5777$ for XOM. JPM has the strongest ratio mean reversion, $\widetilde\kappa_{XX}=0.7465$, consistent with the authors' active-capital-management interpretation. XOM has very little accounting leverage yet the most negative diffusion correlation, $\rho=-0.9637$.

That XOM estimate is more negative than SPX's $-0.8879$. The text's assertion that all five stock correlations are less negative than the index is therefore contradicted by its own Table 5. The remaining values are GE $-.2333$, WMT $-.4619$, JPM $-.4542$, and DUK $-.3610$. The average-stock-versus-index interpretation can still be plausible; the universal statement cannot.

The paper also prints WMT's diffusion-target coefficient as $-2.1296$ in Table 5 and $-2.2196$ in the prose. The table value is retained here. All five jump-target coefficients are negative, but their standard errors differ greatly; negative signs alone do not prove significance for every company.

For external comparison, define accounting measures $A_1=1-TD/TA$ and $A_2=MC/(MC+TD)$. A third measure is Merton distance to default, estimated from equity capitalization and one-year historical equity volatility with zero interest and a ten-year debt horizon. Solve

$$
MC=A\Phi(d_1)-TD\Phi(d_2),\qquad
\sigma_E=\Phi(d_1)\sigma_AA/MC,
$$

$$
d_2=\frac{\log(A/TD)-\sigma_A^2T/2}{\sigma_A\sqrt T},\qquad
d_1=d_2+\sigma_A\sqrt T,
$$

and set $A_3=d_2$. Across the five stocks plus SPX, correlations with option-implied $\widetilde X$ average $.11,.16,.62$ in levels for $A_1,A_2,A_3$, and $.11,.21,.46$ in annual changes. This favors a volatility-standardized comparison, but it does not establish identity between the two latent quantities. Figure 4 rescales accounting series to match the option factor's location and scale, so visual proximity does not validate their absolute levels.

## Pricing performance, inference, and remaining replication inputs

The appendix compares the full model with a two-factor benchmark that removes the leverage factor. Mean absolute pricing error across the 40 SPX implied-volatility series is 0.69 percentage points versus 0.95, a reduction of about 27.4%. At one-month, 120% strike, errors remain large: 2.50 versus 2.74 points. At five-year ATM, they are 0.56 versus 0.77 points. These are in-sample fit statistics, not held-out forecasting performance.

Average weekly pricing-error autocorrelations are $0.91$ and $0.93$, incompatible with the maintained iid measurement-error assumption. The appendix motivates the diagonal measurement covariance as a numerical stabilization device. It helps condition the update matrix, but it does not make the actual pricing errors independent or repair standard errors automatically. From the rounded autocorrelations, AR(1) half-lives are 7.35 and 9.55 weeks; the prose gives roughly eight and 10.5, possibly reflecting unreported precision.

Maximized quasi-log likelihoods are 70,264 and 58,582, yielding twice their difference of 23,364. The appendix compares this with a chi-square distribution with 935 degrees of freedom, counting five parameter restrictions plus 930 additional weekly states. That reference distribution is not justified by ordinary fixed-parameter likelihood-ratio theory for a latent-state filter. Removing an entire stochastic factor also raises boundary and identification issues, while the measurement errors are misspecified and serially dependent. The large fit improvement is directly documented; the stated chi-square calibration should not be accepted as a validated significance test without an appropriate simulation or asymptotic argument.

Reproduction still requires the proprietary OTC panel, cleaned individual-option data, rates and dividends/forward conventions, exact strike filtering, the measurement variance, filter initialization and sigma-point parameter, positivity handling, numerical pricing grids and tolerances, optimization constraints and starting values, and the method used for reported standard errors. The appendix closes the major algorithmic gap but does not supply these implementation choices.

A sensible verification sequence is to check the transform's normalization and martingale values, recover simple limiting option models, validate CEV density mass and first moment without renormalizing away absorption, compare FFT prices with direct integration, and refine both quadratures. Then validate state propagation and filtering on simulated data with known parameters before interpreting the fitted factors economically. The paper's central achievement is a tractable separation of three option-surface mechanisms. Its strongest economic claims remain conditional on that separation, the standardized leverage interpretation, and the adequacy of the approximate observation model.

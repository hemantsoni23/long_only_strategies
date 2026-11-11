# Commodity Price Modeling That Matches Current Observables: A New Approach

Kristian R. Miltersen. Manuscript dated September 2002, version January 30, 2003, Norwegian School of Economics and Business Administration. [Source PDF](../../Finance/CommodityPrices_Miltersen.pdf). The supplied file has fifteen pages, one numerical parameter table, four figures, and no separate appendix. This note covers the complete manuscript; page references are also PDF page numbers.

## Why this matters

A commodity model can have plausible long-run behavior and still misprice the futures contracts that are liquid today. For derivatives valuation, today's curve is a boundary condition: the model should reproduce observed delivery prices before it is used to value an option, a supply contract, or a production decision. A constant-parameter convenience-yield model usually does not fit a seasonal initial curve exactly. Miltersen shows how to retain a low-dimensional Gaussian state model while deriving a time-dependent risk-neutral convenience-yield drift from that curve.

The contribution is an explicit commodity analogue of the Hull–White curve-fitting construction. It combines a futures-convenience-yield term structure with deterministic, calendar-dependent volatilities, correlations, and mean-reversion speed. The central result is equation (13): the risk-neutral mean-reversion level must include the initial curve's derivative, an accumulated variance term, and an instantaneous spot/yield covariance term. These adjustments are necessary for consistency; inserting an arbitrary seasonal mean into a two-factor diffusion does not by itself guarantee an exact initial fit.

The article provides a modeling construction and a fictitious numerical illustration. It does not estimate the model on a historical sample, evaluate forecasting performance, or report trading returns. Its assertion of matching “all observables” should be understood within the admissible volatility family and the available calibration inputs. A two-Brownian-factor model cannot fit an arbitrary cross-maturity covariance matrix or option smile.

## Prices, yields, and the probability measure

Let $S_t>0$ be the physical commodity spot price, $F(t,T)$ its forward delivery price, $G(t,T)$ its futures price, and $B(t,T)$ the price of a zero-coupon bond paying one unit at $T$. The net convenience yield is the flow of services from possessing the physical commodity, less storage and other carrying disadvantages, per unit commodity value per unit time. It can be negative. It is not a cash dividend observed independently of the commodity curve.

In a deterministic setting with constant interest rate $r$ and net convenience yield $\delta$, the carry identity is

$$
F(t,T)=S_t e^{(r-\delta)(T-t)}.
$$

Positive convenience yield lowers the forward relative to an otherwise identical financing-only carry. The source decomposes net convenience into gross convenience minus carrying cost. The interpretation is operational: physical stocks permit immediate use in production, whereas a promise of delivery later does not. The pricing model treats these benefits through an equivalent yield and assumes the perfect-market conditions needed for its no-arbitrage restrictions; it does not solve the physical inventory allocation that creates the benefit.

With stochastic interest rates, the source distinguishes

$$
F(t,T)=\frac{E_t^Q[e^{-\int_t^T r_u\,du}S_T]}{B(t,T)}=E_t^{Q^T}[S_T],
\qquad G(t,T)=E_t^Q[S_T].
$$

Here $Q$ is the money-market risk-neutral measure and $Q^T$ the $T$-forward measure. Their difference reflects stochastic discounting and futures marking to market. Neither formula is a physical conditional forecast unless additional risk-premium assumptions hold. From Section 3 onward, Miltersen sets $r$ constant, so forwards and futures coincide and $B(t,T)=e^{-r(T-t)}$. He motivates this by the comparatively small interest-rate effects in earlier commodity estimates, not by a new empirical test in this paper.

Let $f(t,T)$ be the instantaneous forward interest rate. Define forward convenience yield $\delta(t,T)$ and futures convenience yield $\epsilon(t,T)$ by

$$
F(t,T)=\frac{S_t}{B(t,T)}e^{-\int_t^T\delta(t,u)\,du},
\qquad
G(t,T)=\frac{S_t}{B(t,T)}e^{-\int_t^T\epsilon(t,u)\,du}.
$$

Both diagonal values equal the spot convenience yield: $\delta(t,t)=\epsilon(t,t)=\delta_t$. With constant interest, the two surfaces coincide. In particular, a smooth initial futures curve supplies

$$
\epsilon_0(T)\equiv\epsilon(0,T)=r-\partial_T\log G(0,T).
$$

Initial consistency also requires $G(0,0)=S_0$ and $\delta_0=\epsilon_0(0)$. The yield drift derived below uses $\epsilon_0'(T)$, so the fitted log futures curve needs two derivatives, not just a visual interpolation through delivery prices. Differentiation amplifies quote noise and makes the interpolation/extrapolation convention economically consequential.

## The term-structure drift restriction

Write the spot and futures-yield dynamics under $Q$ as

$$
\frac{dS_t}{S_t}=(r-\epsilon(t,t))dt+\boldsymbol\sigma_S(t)\cdot dW_t,
$$

$$
d\epsilon(t,T)=\mu_\epsilon(t,T)dt+\boldsymbol\sigma_\epsilon(t,T)\cdot dW_t.
$$

The same vector Brownian motion drives both processes; vector loadings encode covariance. In the constant-rate specialization, equation (9) is

$$
\mu_\epsilon(t,T)=\boldsymbol\sigma_\epsilon(t,T)\cdot
\left[\int_t^T\boldsymbol\sigma_\epsilon(t,u)\,du-\boldsymbol\sigma_S(t)\right].
$$

A short derivation makes the sign and normalization transparent. Set $A(t,T)=\int_t^T\boldsymbol\sigma_\epsilon(t,u)\,du$. The log of the futures price is $\log S_t+r(T-t)-\int_t^T\epsilon(t,u)du$. Moving the lower integration limit cancels the $r-\epsilon(t,t)$ drift from spot. Its remaining drift is $-\tfrac12\|\boldsymbol\sigma_S\|^2-\int_t^T\mu_\epsilon(t,u)du$, and its diffusion is $\boldsymbol\sigma_S-A$. For the futures price itself to be a $Q$ martingale, Itô's correction requires

$$
\int_t^T\mu_\epsilon(t,u)du
=\tfrac12\|A(t,T)\|^2-\boldsymbol\sigma_S(t)\cdot A(t,T).
$$

Differentiating with respect to $T$ gives equation (9). The negative covariance term is therefore required by absence of drift in futures; it is not a discretionary risk-premium parameter.

The manuscript also states the more general stochastic-interest-rate restriction on p. 6. With forward-rate volatility $\boldsymbol\sigma_f$ and HJM drift $\mu_f(t,T)=\boldsymbol\sigma_f(t,T)\cdot\int_t^T\boldsymbol\sigma_f(t,u)du$, it is

$$
\mu_\epsilon(t,T)=\mu_f(t,T)+[\boldsymbol\sigma_f(t,T)-\boldsymbol\sigma_\epsilon(t,T)]\cdot
\left[\boldsymbol\sigma_S(t)+\int_t^T(\boldsymbol\sigma_f(t,u)-\boldsymbol\sigma_\epsilon(t,u))du\right].
$$

That identity places the constant-rate construction in the broader term-structure framework. The numerical example and subsequent calibration recipe do not estimate or use this additional interest-rate factor.

## Deterministic volatility family

Define the decay kernel and integrated kernel

$$
K(t,T)=\exp\left[-\int_t^T\kappa(u)du\right],
\qquad H(t,T)=\int_t^T K(t,u)du.
$$

Let $a(t)=\sigma_S g_S(t)$ and $b(t)=\sigma_\epsilon g_\epsilon(t)$. Equations (10)–(11) specify two independent Brownian coordinates through

$$
\boldsymbol\sigma_S(t)=a(t)(1,0),
\qquad
\boldsymbol\sigma_\epsilon(t,T)=b(t)K(t,T)(\rho(t),\sqrt{1-\rho(t)^2}).
$$

All functions are deterministic. The correlation must satisfy $|\rho(t)|\le1$, and square-integrability is needed on finite horizons. Positive $\kappa$ gives mean reversion and decaying yield shocks across maturity. If the seasonal functions are interpreted as nonnegative volatility amplitudes, their parameterization should preserve that sign. The source's sinusoidal example uses amplitudes well below one.

Under this specification the yield drift becomes

$$
\mu_\epsilon(t,T)=b(t)^2K(t,T)H(t,T)-a(t)b(t)\rho(t)K(t,T).
$$

Thus the entire surface is explicitly Gaussian:

$$
\epsilon(t,T)=\epsilon_0(T)+\int_0^t[b(u)^2K(u,T)H(u,T)-a(u)b(u)\rho(u)K(u,T)]du
+\int_0^t b(u)K(u,T)\mathbf e(u)\cdot dW_u,
$$

where $\mathbf e(u)=(\rho(u),\sqrt{1-\rho(u)^2})$. Gaussian convenience yields can be negative, consistent with a net rather than gross convenience interpretation. The spot price remains positive and its log is Gaussian. Although the source calls spot a geometric Brownian motion, its convenience-dependent stochastic drift distinguishes it from the elementary constant-drift, constant-volatility GBM.

## Recovering the spot convenience-yield process

The diagonal process $\delta_t=\epsilon(t,t)$ is not obtained by holding maturity fixed and merely substituting $T=t$ into the drift. Calendar time and maturity move together, so the maturity derivative contributes. Define

$$
q(t)=\int_0^t b(u)^2K(u,t)^2du,
\qquad q'(t)=b(t)^2-2\kappa(t)q(t),\quad q(0)=0.
$$

Here $q(t)$ is the variance of the spot convenience yield conditional on the deterministic initial state, not a commodity price. Differentiating the explicit surface gives

$$
\partial_T\epsilon(t,T)\big|_{T=t}
=\epsilon_0'(t)+\kappa(t)[\epsilon_0(t)-\delta_t]+q(t).
$$

The fixed-maturity yield drift at the diagonal is $\mu_\epsilon(t,t)=-a(t)b(t)\rho(t)$. Adding the two contributions yields

$$
d\delta_t=\left[\epsilon_0'(t)+\kappa(t)\epsilon_0(t)+q(t)-a(t)b(t)\rho(t)-\kappa(t)\delta_t\right]dt
+b(t)\mathbf e(t)\cdot dW_t.
$$

Consequently, when $\kappa(t)\ne0$,

$$
d\delta_t=\kappa(t)[\widehat\theta(t)-\delta_t]dt+b(t)\mathbf e(t)\cdot dW_t,
\qquad
\widehat\theta(t)=\epsilon_0(t)+\frac{\epsilon_0'(t)+q(t)-a(t)b(t)\rho(t)}{\kappa(t)}.
$$

This is equation (13). The undivided drift remains well defined when a chosen $\kappa$ reaches zero, whereas a formula expressed as a mean-reversion level can become singular. Positive mean-reversion speed should be enforced if that economic interpretation is intended.

The source proves the result using an integrating factor $Y(t,T)=\epsilon(t,T)\exp[\int_0^T\kappa(u)du]$ and then restricting to $Y(t,t)$. Its p. 9 intermediate change of integration order writes the inner upper limit as the integration variable rather than $\min(t,\cdot)$ for a general off-diagonal $Y(t,T)$. That intermediate equality is valid on the diagonal used next, but not generally for $t<T$. The direct derivative above avoids this issue and confirms the final spot-yield equation. This is a bounded algebraic qualification, not a rejection of equation (13).

For implementation over an interval $[s,t]$, the linear yield equation has exact conditional mean

$$
E_s^Q[\delta_t]=K(s,t)\delta_s+\int_s^t K(u,t)\kappa(u)\widehat\theta(u)du
$$

and conditional variance $\int_s^t b(u)^2K(u,t)^2du$. The log spot equation is $d\log S_t=[r-\delta_t-\tfrac12a(t)^2]dt+a(t)dW_{1,t}$. These identities permit exact Gaussian transition simulation with deterministic numerical quadrature, instead of an unnecessary Euler discretization. A joint simulation must retain the covariance between integrated yield innovations and spot innovations; independently simulating the two Gaussian components would alter the futures term structure.

## Futures volatility, joint dependence, and valuation

The instantaneous futures-return loading is

$$
\mathbf v(t,T)=\left(a(t)-b(t)\rho(t)H(t,T),\;-b(t)\sqrt{1-\rho(t)^2}H(t,T)\right).
$$

Equation (14) is its squared norm:

$$
V(t,T)=a(t)^2+b(t)^2H(t,T)^2-2a(t)b(t)\rho(t)H(t,T).
$$

This is instantaneous variance per unit time of percentage futures changes. It is not the variance of a terminal spot level, an option-implied volatility without a maturity integration, or a physical expected return. Positive spot/yield correlation can reduce near-to-intermediate futures volatility because a positive spot shock also raises convenience yield, lowering the expected future spot drift under $Q$.

A useful derived covariance formula for two delivery dates is

$$
\mathbf v(t,T_1)\cdot\mathbf v(t,T_2)
=a^2-ab\rho(H_1+H_2)+b^2H_1H_2.
$$

This supplies the full instantaneous cross-maturity covariance, which matters for calendar-spread hedges and multi-delivery claims. The covariance matrix has rank at most two at a fixed instant. Its correlations are model predictions once the loading functions are chosen; fitting each maturity's marginal variance does not independently fit every pairwise correlation.

Since the futures volatility is deterministic, an exact representation for a fixed delivery date is

$$
G(t,T)=G(0,T)\exp\left[-\frac12\int_0^t V(u,T)du+\int_0^t\mathbf v(u,T)\cdot dW_u\right].
$$

This derived implementation form reproduces the initial curve by construction and makes the martingale test immediate. For a European option expiring at $\tau\le T$, its log futures variance is $w=\int_t^\tau V(u,T)du$. Under the constant-rate assumptions, a call paying $(G(\tau,T)-K_o)^+$ has value

$$
C_t=e^{-r(\tau-t)}[G(t,T)\Phi(d_1)-K_o\Phi(d_2)],
\qquad d_{1,2}=\frac{\log(G(t,T)/K_o)\pm w/2}{\sqrt w}.
$$

This is a consequence of the model's lognormal futures distribution, not a numerical option-pricing experiment reported by Miltersen. A deterministic Gaussian loading cannot generate a strike-dependent smile for one futures maturity. Nonlinear or path-dependent claims can use the same joint simulation, but would require their contractual exercise and delivery rules.

Mean reversion of convenience yield does not imply stationarity of the spot price level. With constant $a,b,\rho,\kappa$, the long-horizon variance rate of log spot is

$$
\lim_{T\to\infty}\frac{\operatorname{Var}(\log S_T)}{T}
=a^2+\frac{b^2}{\kappa^2}-\frac{2ab\rho}{\kappa}
=\left(a-\frac{b\rho}{\kappa}\right)^2+\frac{b^2}{\kappa^2}(1-\rho^2).
$$

It is normally positive. The price can show a temporary reversal response while retaining a permanent stochastic component. This derived qualification prevents an overinterpretation of the paper's phrase “mean-reversion effect.” Under physical probabilities, market prices of risk can alter the drifts further. The initial pricing curve alone does not identify a unique physical forecasting process or a unique investor-preference model.

## Calibration recipe and feasibility restrictions

The source's five-step recipe first parameterizes the observed curve and extracts $\epsilon_0$ and $\epsilon_0'$. It then estimates the spot volatility's calendar pattern, calibrates the maturity-decay function $\kappa$, jointly estimates convenience-yield volatility and correlation from long-maturity futures behavior, and finally computes $\widehat\theta$. The third and fourth steps must be simultaneous, as the footnote on p. 10 states. The manuscript specifies neither a likelihood nor a least-squares weighting scheme, optimization constraints, confidence intervals, or a data-cleaning protocol.

Its suggested seasonal functions are

$$
g_S(t)=1+A_S\sin[2\pi(t+B_S)],\qquad
g_\epsilon(t)=1+A_\epsilon\sin[2\pi(t+B_\epsilon)].
$$

Time is measured in years, the $A$ terms are relative amplitudes, and the $B$ terms are phase shifts. One could estimate the spot pattern from historical squared returns and use futures covariance observations for the remaining functions, but that is an implementation choice beyond the specified source. Convenience yields are latent and inferred from noisy curves; treating a backed-out yield as error-free can distort the calibration.

There are nontrivial restrictions behind an exact volatility fit. At time zero, write $a=a(0)$, $b=b(0)$, $\rho=\rho(0)$, and $H(T)=H(0,T)$. Then

$$
V(0,T)=b^2\left[H(T)-\frac{a\rho}{b}\right]^2+a^2(1-\rho^2),
$$

for $b>0$. Moreover, $H(0)=0$, $H'(0)=1$, $H'(T)>0$, and $\kappa(T)=-H''(T)/H'(T)$. Positive mean reversion requires $H''(T)<0$. A proposed variance curve must admit a smooth increasing kernel satisfying these conditions. Formally solving the quadratic gives

$$
H(T)=\frac{a\rho\pm\sqrt{V(0,T)-a^2(1-\rho^2)}}{b},
$$

but branch choice, nonnegative discriminant, the initial conditions, and smoothness cannot be ignored. With positive $\rho$, the branch issuing from $H(0)=0$ initially uses the minus sign. A switch can occur at the variance minimum only if the resulting kernel remains admissible. Also $\partial_T V(0,0)=-2ab\rho$, constraining the initial variance slope. Thus arbitrary observed volatility surfaces are not guaranteed to be exactly representable by the chosen family.

Instantaneous futures-volatility estimates and option-implied integrated variances are different calibration objects. The paper's recipe refers to the former. Matching option prices instead requires integrating $V(u,T)$ over option life and distinguishing option expiry from underlying delivery. For a fixed tenor $L$, the relevant kernel is $H(t,t+L)$. Step (4) on p. 11 labels a fixed-tenor futures volatility but prints an integral with upper limit $T$ rather than $t+T$; retaining an absolute upper date while calling it a constant tenor would change the calibration. The corrected distinction follows from equation (14).

## Numerical example and checks

Table 1 uses a fictitious commodity with $S_0=145$, $\sigma_S=0.40$, $\sigma_\epsilon=0.50$, $A_S=A_\epsilon=0.10$, $B_S=B_\epsilon=-0.25$, $r=0.05$, $\kappa=1.8$, and $\rho=0.75$. It lists $\delta_0=0.10$. The parameters are described as inspired by earlier crude-oil estimates; they are not new estimated coefficients. No sample dates, standard errors, estimation objective, or actual market quotes accompany them.

The stated phases give $g_S(0)=g_\epsilon(0)=0.9$, so the initial instantaneous spot-return volatility is 36%, not the 40% base parameter. Its calendar range is 36%–44%. Convenience-yield diffusion ranges from 0.45 to 0.55 in yield units per square-root year. It should not be confused with a 45%–55% percentage volatility of the yield itself. The convenience-yield half-life is $\log(2)/1.8=0.3851$ years, a derived calculation holding coefficients constant.

For this example, $H(0,T)=(1-e^{-1.8T})/1.8$. Direct evaluation of equation (14) gives initial futures volatilities of 36.00% at zero maturity, 26.74% at half a year, 24.59% at one year, 23.96% at two years, and an asymptote of 23.8956%. These derived numbers agree with the shape and approximate levels of Figure 3. The maturity curve is smooth even though calendar-time amplitudes are seasonal: at a fixed valuation date, $a(t)$ and $b(t)$ are fixed, while constant $\kappa$ determines their maturity attenuation. One must not shift calendar time together with delivery date when interpreting that figure.

Figure 1 is a downward-trending initial futures curve with annual oscillations. Figure 4 shows the resulting futures convenience yield and a more strongly oscillating risk-neutral mean-reversion target, roughly ranging from −0.65 to 0.8 in the plotted target. The large target swings counteract mean reversion strongly enough to fit the prescribed seasonal curve; they are not observations of producers' physical expected convenience yields. The source does not provide the formula or data points for the initial curve, so exact reproduction of Figures 1 and 4 is underdetermined.

There are two visible illustration inconsistencies. The prose on p. 11 reverses Figure 2's color assignments; the caption and actual ranges identify blue as spot volatility and red as convenience-yield diffusion. More materially, Figure 4's red initial convenience yield appears negative, around −0.1, whereas Table 1 lists positive 0.1. Figure 1 initially rises, while $\delta_0=0.1$ and $r=0.05$ would require initial log-curve slope −0.05. The identity $\delta_0=r-\partial_T\log G(0,T)|_{T=0}$ makes the conflict explicit. The note preserves the table value and flags the plotted inconsistency; it does not silently infer an undisclosed curve formula or an author-approved correction.

## Limits and source map

A working implementation needs synchronized spot and futures quotes, delivery conventions, an initial curve interpolator with stable derivatives, a calendar-time scale, volatility and correlation observations, admissibility constraints, and a numerical estimation objective. It should verify exact initial-price fit, futures martingale behavior, cross-maturity covariance, and the equivalence of direct futures simulation with the spot/yield construction. These are reconstruction requirements. The source does not report a completed calibration, hedge backtest, costs, margin policy, rebalancing frequency, or out-of-sample error.

The extension to weather and quantity-linked products on p. 14 is conceptual. A convenience-yield variable can parameterize a nontraded underlying's drift consistently with observed forward prices, but a nontraded underlying generally leaves market prices of unspanned risk undetermined. Observing a curve does not establish unique derivative values for every payoff. Likewise, obtaining a time-dependent risk-neutral mean does not by itself reveal a unique physical mean or preference system.

Pages 2–6 define convenience yield and the HJM-style restrictions. Pages 7–10 derive the deterministic loading family and equation (13). Pages 10–11 give the volatility formula and calibration sequence. Table 1 and Figures 1–4 are on pp. 11–13; the conclusion and bibliography are on pp. 14–15. The relevant antecedents identified by the paper are Gibson–Schwartz's stochastic convenience-yield model, the HJM forward-rate framework, Hull–White initial-curve fitting, and Miltersen–Schwartz's 1998 commodity term-structure model. The present source's distinct result is the explicit, curve-consistent time-dependent spot convenience-yield drift. The feasibility conditions, simulation formulas, and numerical cross-checks in this note are derived consequences, clearly separated from the manuscript's reported illustration.

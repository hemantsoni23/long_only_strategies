# Valuation of Commodity Futures and Options Under Stochastic Convenience Yields, Interest Rates, and Jump Diffusions in the Spot

Jimmy E. Hilliard and Jorge Reis, *Journal of Financial and Quantitative Analysis* 33(1), March 1998, pp. 61–86. [Source PDF](../../Finance/CommodityPrices_HilliardReis_1998.pdf). The supplied file contains 27 pages, including its cover, the complete article, Appendices A–C, and references. Printed page 61 is PDF page 2.

## Why this matters

A commodity futures curve is not generally obtained by extending today's convenience yield unchanged into the future. The service value of physical inventory can revert quickly even when spot prices are high, and stochastic interest rates distinguish a continuously marked futures contract from a forward contract. Jumps add a further distinction: a compensated jump component can preserve the conditional mean used to price linear claims while changing the tails relevant to options.

Hilliard and Reis build an analytical framework that separates these effects. Convenience yield is an Ornstein–Uhlenbeck factor with a specified risk premium. Interest rates follow a model fitted to the initial bond curve. Spot prices may additionally experience lognormal proportional jumps. The paper derives futures, forwards, European futures options, and the present value of a future physical delivery. It also gives a numerical illustration of American exercise under time-varying futures volatility.

The contribution is theoretical, with synthetic comparisons and an oil-delivery application using previously estimated parameters. It is not a new empirical calibration study or an out-of-sample test. Its practical value is a family of internally connected pricing formulas and limiting cases. A reproduction must distinguish model inputs from estimated quantities and must repair several visible printing inconsistencies before coding the equations literally. The formulas below use covariance integrals to make the reconstruction explicit; corrections to the printed expressions are identified separately.

## Model primitives and the risk-neutral convention

Trading is continuous, and transaction costs, taxes, and short-sale restrictions are absent. Let $S_t$ denote spot price, $\delta_t$ the instantaneous net convenience-yield rate, and $r_t$ the short rate. Convenience yield includes the benefits of physical ownership less storage costs; it is a rate, not the dollar service flow used in some inventory models. The physical spot process initially is $dS/S=\mu\,dt+\sigma_s\,dW_s$. Its risk-neutral drift is $r-\delta$.

The physical convenience yield follows

$$
d\delta_t=\kappa_c(\alpha-\delta_t)dt+\sigma_c\,dW_{c,t},
\qquad \kappa_c>0.
$$

The Gaussian specification permits negative net convenience yields. With constant market price of convenience-yield risk $\lambda_c$, the pricing-measure process is

$$
d\delta_t=\kappa_c(\bar\alpha-\delta_t)dt+\sigma_c\,dW_{c,t}^{Q},
\qquad \bar\alpha=\alpha-\frac{\lambda_c\sigma_c}{\kappa_c}.
$$

The distinction between $\alpha$ and $\bar\alpha$ is essential. Historical mean reversion alone does not determine the pricing mean. The convenience factor is not directly traded, so no-arbitrage does not determine its market price of risk without additional spanning or equilibrium assumptions. The paper takes the premium as constant. It embeds preference information there while fitting interest-rate risk through observed bond prices.

Brownian correlations are $\rho_{sc}$, $\rho_{sr}$, and $\rho_{cr}$. A numerical implementation must use a positive-semidefinite correlation matrix. Choosing each pair in $[-1,1]$ independently is insufficient. All volatilities and reversion speeds use a common time unit; the examples use years. $P(t,T)$ denotes the zero-coupon bond price, $J(t,T)$ the commodity forward delivery price, and $F(t,T)$ the futures price. A forward contract's initial value is zero even though its agreed delivery price $J$ is positive. Neither should be confused with the prepaid value of receiving the commodity at $T$.

For deterministic rates and constant convenience yield, the benchmark is $F=J=S_t\exp((r-\delta_t)(T-t))$. With a stochastic convenience yield, equations (5)–(9) replace the fixed carry rate by a two-factor pricing problem. The futures PDE has no $-rF$ term because a futures position has no initial purchase price. The resulting terminal condition is $F(S,\delta,0)=S$.

## Two-factor forwards and futures in implementable form

Write $\tau=T-t$, and define

$$
H_k(u)=\frac{1-e^{-ku}}{k},\qquad
I_1(k,u)=\int_0^u H_k(v)dv=\frac{u-H_k(u)}{k},
$$

$$
I_2(k,u)=\int_0^u H_k(v)^2dv
=\frac{u-H_k(u)-\tfrac12kH_k(u)^2}{k^2}.
$$

Use the continuous limits when $k$ is close to zero; evaluating $1-e^{-ku}$ with a numerically stable exponential-difference routine avoids cancellation. Set $H_c=H_{\kappa_c}(\tau)$. The prepaid forward value is

$$
B(t,T)=S_t\exp\left[
-H_c\delta_t-\bar\alpha(\tau-H_c)
+\frac12\sigma_c^2I_2(\kappa_c,\tau)
-\rho_{sc}\sigma_s\sigma_cI_1(\kappa_c,\tau)
\right].
$$

With deterministic interest rates,

$$
F(t,T)=J(t,T)=\frac{B(t,T)}{P(t,T)}.
$$

This is equation (10) expressed through elementary integrals. Appendix A derives it by integrating the OU yield and applying the Gaussian exponential-moment formula to discounted spot price. The $\sigma_s^2\tau/2$ contribution cancels between the log-price drift and its variance. The remaining convexity term arises from randomness in integrated convenience yield; the spot–yield covariance contributes with a negative sign.

The formula recovers spot at $\tau=0$. If convenience yield is deterministic and constant, it reduces to the usual carry relation. Setting only $\sigma_c=0$ while retaining $\kappa_c>0$ instead gives deterministic *mean-reverting* convenience yield, which is not generally constant carry. This distinction matters when using model reductions as unit checks.

The implied average convenience yield is defined by

$$
\Delta(t,T)=R(t,T)-\frac{\log(F(t,T)/S_t)}{T-t},
\qquad R(t,T)=-\frac{\log P(t,T)}{T-t}.
$$

In the two-factor setting this equals

$$
\Delta(t,T)=\frac{H_c\delta_t+\bar\alpha(\tau-H_c)
-\tfrac12\sigma_c^2I_2(\kappa_c,\tau)
+\rho_{sc}\sigma_s\sigma_cI_1(\kappa_c,\tau)}{\tau}.
$$

It tends to $\delta_t$ at zero maturity. The instantaneous forward convenience yield is the maturity derivative of $\tau\Delta(t,T)$, not the average itself. Equation (14) establishes that distinction. The source's Taylor-series footnote is not needed for evaluation; the exact $H_k$ function gives the limit directly.

Table 1 uses $S=100$, $r=0.10$, $\sigma_s=0.25$, $\alpha=-0.01$, $\lambda_c=0$, $\rho_{sc}=0$, and $\sigma_c=0.10$. It varies current yield from −0.01 to 0.11, reversion speed over 0.5, 5, and 15, and maturity over three, six, and nine months. At nine months and current yield 0.11, constant carry gives 99.25, whereas the two-factor prices are 100.80, 106.09, and 107.74. Recalculation from the formula gives 100.80172, 106.09410, and 107.73610. When the current yield equals the long-run mean, the differences are much smaller: the nine-month row is 108.60 for constant carry and 108.66, 108.61, and 108.60 for the three reversion speeds. These are comparative statics under the listed parameters, not estimated pricing errors.

## Futures volatility and options with deterministic rates

For a futures contract expiring at $T$, applying Itô's formula gives

$$
\frac{dF(u,T)}{F(u,T)}
=\sigma_s\,dW_s^Q(u)-\sigma_cH_{\kappa_c}(T-u)\,dW_c^Q(u).
$$

Its instantaneous variance rate is

$$
v_F(u,T)=\sigma_s^2+\sigma_c^2H_{\kappa_c}(T-u)^2
-2\rho_{sc}\sigma_s\sigma_cH_{\kappa_c}(T-u).
$$

It is deterministic conditional on model parameters and the two dates, but varies as maturity approaches. It converges to spot variance at delivery. It need not decrease monotonically with maturity: the positive yield-variance term and signed covariance term compete. Its lack of dependence on current spot or yield levels allows the observed futures price to be used as the state variable for option pricing.

For a European call expiring at $T_1\le T$, let

$$
V=\int_t^{T_1}v_F(u,T)du.
$$

Equations (22)–(24) give

$$
C=P(t,T_1)[F(t,T)N(d_1)-XN(d_2)],
\qquad d_1=\frac{\log(F/X)+V/2}{\sqrt V},\quad d_2=d_1-\sqrt V.
$$

The variance integration must stop at the option expiration $T_1$, while the volatility kernel retains the futures expiration $T$. Substituting $T_1=T$ without justification prices a different contract. Either integrate the displayed variance or evaluate equation (24)'s exponential terms. For example, the integral of $H_{\kappa_c}(T-u)$ is

$$
\frac{T_1-t}{\kappa_c}
-\frac{e^{-\kappa_c(T-T_1)}-e^{-\kappa_c(T-t)}}{\kappa_c^2}.
$$

A Black formula with a constant volatility chosen so that its total variance equals $V$ produces the same European price. Therefore the paper's European formula does not claim an additional premium merely for naming convenience yield as a factor. The extra structure relates implied variances across futures maturities, supplies an evolution through time, and connects options to the spot and yield processes. Taking market $F$ as an input also differs from generating $F$ through the structural pricing formula: in the latter case, a misspecified yield curve affects both the underlying futures level and the option price.

American options require the variance path, not just its integral. The source constructs a binomial tree in the transformed state $x=\log F/\sigma(u)$, with drift $-\sigma/2-x\sigma_u/\sigma$ and unit diffusion, then transforms back. It uses 500 steps and adjusts the American tree price by the discrepancy between the analytical and tree European prices. A reconstructable implementation discounts continuation values and compares them with immediate exercise at each node. The exact node-placement and boundary conventions are not provided, so reproducing the last quoted digit requires additional implementation choices.

Table 2 fixes $r=0.05$, spot diffusion volatility 0.25, strike 100, and option life 0.75 years. The four variance totals 0.1078, 0.0454, 0.0301, and 0.0856 correspond to $(\sigma_c,\kappa_c,\rho_{sc})$ equal to (1,1,0.2), (0.5,1,0.4), (0.5,0.5,0.7), and (1,1,0.4). Recomputing the integrals shows that these totals are consistent with coincident option and futures expiration; this is a reconstruction from the numbers, since the table's parameter line does not separately state $T$.

In the first block, futures levels 80, 100, and 120 give European calls 4.152, 12.560, and 25.500. The constant-volatility American values are 4.172, 12.662, and 25.808; the time-varying-volatility values are 4.188, 12.724, and 25.947. The deep-in-the-money difference between the American models is about 0.139. The printed 8.06% premium beside 12.662 is inconsistent with both prices: $(12.662-12.560)/12.560$ is 0.8121%, not 8.06%. This is a derived arithmetic correction. The surrounding text's statement that the illustrated premiums are below 2% is consistent with the corrected percentage.

## Stochastic rates, and why forwards and futures separate

For general rates, the definitions are

$$
J(t,T)=\frac{E_t^Q[e^{-\int_t^T r_u du}S_T]}{P(t,T)},
\qquad F(t,T)=E_t^Q[S_T].
$$

The source initially allows an HJM rate model calibrated to the initial forward-rate curve. Discounting $S_T$ cancels the accumulated short rate in its log drift. Under the maintained constant spot volatility and rate-independent convenience-yield coefficients, the prepaid value $B$ is consequently the same expression derived above. Matching the same initial bond price gives the same forward delivery price in the deterministic- and stochastic-rate specifications. This is a property of these processes, not a statement that stochastic rates never matter for commodity forwards. State-dependent volatilities or rate-dependent yield dynamics can destroy the cancellation's distributional implication.

For futures and options, the paper specializes to a one-factor Gaussian rate model. With $f(t,u)$ the initial instantaneous forward-rate curve, the pricing SDE in equation (29) is

$$
dr_u=\left[\partial_u f(t,u)+\kappa_rf(t,u)
+\frac{\sigma_r^2}{2\kappa_r}(1-e^{-2\kappa_r(u-t)})
-\kappa_rr_u\right]du+\sigma_r dW_r^Q(u).
$$

Its deterministic drift fits the input bond curve. The solution has conditional mean

$$
E_t^Q[r_u]=f(t,u)+\frac{\sigma_r^2}{2\kappa_r^2}
(1-e^{-\kappa_r(u-t)})^2,
$$

and stochastic part $\sigma_r\int_t^u e^{-\kappa_r(u-v)}dW_r^Q(v)$. This solution, obtained directly from equation (29), is the one used below. The printed intermediate equation (B-6) contains an inconsistent coefficient/exponential in its deterministic correction; its subsequent integrated mean (B-7) agrees with the solution above.

Define the cross-kernel integral

$$
I_{cr}(\tau)=\int_0^\tau H_{\kappa_c}(v)H_{\kappa_r}(v)dv
=\frac{\tau-H_{\kappa_c}(\tau)-H_{\kappa_r}(\tau)
+H_{\kappa_c+\kappa_r}(\tau)}{\kappa_c\kappa_r}.
$$

The three-factor futures price can then be implemented as

$$
F(t,T)=J(t,T)\exp\left[
\sigma_r^2I_2(\kappa_r,\tau)
+\rho_{sr}\sigma_s\sigma_rI_1(\kappa_r,\tau)
-\rho_{cr}\sigma_c\sigma_rI_{cr}(\tau)
\right].
$$

These are, respectively, the integrated-rate variance adjustment, spot–rate covariance adjustment, and convenience–rate covariance adjustment. This form is equivalent to the multiplicative factors $D_1D_2D_3$ in equation (31). The integral representation also makes the zero-rate-volatility limit transparent: all three adjustments vanish in the exponent, giving $F=J$. Appendix B derives the factors through Gaussian exponential moments.

The corresponding futures diffusion has loadings

$$
\frac{dF(u,T)}{F(u,T)}=
\sigma_s dW_s^Q-\sigma_cH_{\kappa_c}(T-u)dW_c^Q
+\sigma_rH_{\kappa_r}(T-u)dW_r^Q.
$$

Its variance is the quadratic form of these loadings and the correlation matrix. Expanded, it is

$$
v_F=\sigma_s^2+\sigma_c^2H_c^2+\sigma_r^2H_r^2
-2\rho_{sc}\sigma_s\sigma_cH_c
+2\rho_{sr}\sigma_s\sigma_rH_r
-2\rho_{cr}\sigma_c\sigma_rH_cH_r.
$$

Here the $H$ functions use remaining futures maturity. Equations (36) and (38) give these loadings and their variance. A direct quadratic-form calculation provides a useful implementation check and ensures nonnegative variance when the correlation matrix is admissible.

## Compensated jumps and the European option mixture

The jump extension specifies the risk-neutral spot process

$$
\frac{dS}{S}=(r-\delta-\lambda^*\bar k)dt
+\sigma_s dW_s^Q+k\,dN_t,
$$

where $N$ has intensity $\lambda^*$, $1+k>0$, $E^Q[k]=\bar k$, and

$$
\log(1+k)\sim N(\gamma-\omega^2/2,\omega^2),
\qquad \gamma=\log(1+\bar k).
$$

The source uses starred jump notation; the simplified $k,\bar k,\gamma$ here all denote pricing-measure quantities. Jump sizes, arrival process, and Brownian factors must have the independence used in the derivation. Pairwise zero covariances alone would not establish the exponential-moment factorization. Risk-neutral intensity and mean jump need not equal historical estimates.

The compensator $-\lambda^*\bar k$ makes the jump multiplier's expected contribution equal to one. Under these assumptions, adding jumps leaves $E^Q[S_T]$ and the discounted expectation unchanged. Hence futures and forwards retain their diffusion-model prices. This result does not mean that any introduction of jumps leaves prices unchanged: it holds after the risk-neutral drift has been compensated and the stated independence is imposed. Jumps alter option prices because a positive-part payoff depends on more than the first moment. Their proportional size passes unchanged into futures because the futures pricing function is linear in spot.

Let $\tau_1=T_1-t$, $V=\int_t^{T_1}v_F(u,T)du$, and define the discount-covariance adjustment

$$
\log Z=-\int_t^{T_1}\sigma_rH_{\kappa_r}(T_1-u)
\left[\rho_{sr}\sigma_s
-\rho_{cr}\sigma_cH_{\kappa_c}(T-u)
+\sigma_rH_{\kappa_r}(T-u)\right]du.
$$

Equivalently, $Z$ is the ratio $E^Q[e^{-\int_t^{T_1}rdu}F(T_1,T)]/[P(t,T_1)F(t,T)]$ for the continuous diffusion. It is one only when the *integrated* covariance vanishes. This integral expression reconstructs the discount adjustment directly from Appendix C equations (C-9)–(C-10), without relying on a transcription of the expanded maturity terms in equation (40). The negative covariance sign also follows by observing that positive futures–rate comovement lowers the expectation after discounting high-rate outcomes more heavily.

For $n$ jumps, define $V_n=V+n\omega^2$ and $M_n=F(t,T)Z\exp(-\lambda^*\bar k\tau_1+n\gamma)$. The reconstructable version of equation (39) is

$$
C=P(t,T_1)\sum_{n=0}^{\infty}
\frac{e^{-\lambda^*\tau_1}(\lambda^*\tau_1)^n}{n!}
\left[M_nN(d_{1n})-XN(d_{2n})\right],
$$

$$
d_{1n}=\frac{\log(M_n/X)+V_n/2}{\sqrt{V_n}},
\qquad d_{2n}=d_{1n}-\sqrt{V_n}.
$$

Conditioning on the Poisson count makes the terminal log futures price Gaussian; the normal jump mean and variance add to the continuous ones. Changing to the option-payment forward measure shifts the Gaussian mean through $Z$ without changing its variance. This explains why discount covariance modifies $M_n$ while $V_n$ retains the integrated futures variance. At zero jump intensity the formula reduces to the Gaussian three-factor call; with deterministic rates $Z=1$; with no yield or rate volatility it reduces to the usual constant-volatility compensated-jump mixture.

For computation, sum Poisson terms until the omitted contribution is negligible for the desired price tolerance. A probability-tail tolerance alone need not bound the first-moment-weighted call tail when large positive jump means are allowed, so monitor the weighted asset term as well. The paper gives the infinite sum but does not specify a truncation tolerance or report a jump-parameter calibration. There is no numerical evidence in this article estimating how much jumps improve actual option-price fit.

## Oil delivery values and replication limits

A claim to one barrel at $T$ has current value $B(t,T)=P(t,T)J(t,T)$, equation (41). It is a prepaid physical-delivery value, not a futures price or the value of an operating oilfield. Summing appropriately scaled delivery values can price fixed future commodity cash flows; extraction flexibility, costs, taxes, and capacity constraints require an additional model.

Table 3 uses parameters attributed to Gibson and Schwartz estimates over January 1984–November 1988: $\kappa_c=16.0747$, $\alpha=0.1861$, $\sigma_c=1.1211$, $\rho_{sc}=0.3200$, $\sigma_s=0.3534$, and $\lambda_c=-1.796$. The very fast annual reversion implies that a temporarily extreme current yield should not be carried unchanged through a ten-year horizon. The paper evaluates three observation dates with different spot and current-yield inputs:

| Date and initial state | 1-year two-factor / constant-yield value | 5-year values | 10-year values |
|---|---:|---:|---:|
| 6 July 1984: $S=29.65$, $\delta=3.30\%$ | 21.98 / 28.69 | 6.19 / 25.14 | 1.27 / 21.32 |
| 21 March 1986: $S=13.94$, $\delta=-13.71\%$ | 10.44 / 15.99 | 2.94 / 27.67 | 0.60 / 54.91 |
| 23 May 1989: $S=19.05$, $\delta=65.50\%$ | 13.59 / 9.90 | 3.83 / 0.72 | 0.78 / 0.03 |

Values are dollars per barrel. Direct substitution reproduces these rounded numbers. The quoted bond yields are 11.60%, 6.90%, and 8.80%, treated as flat across maturities in the table, but cancel from the prepaid-delivery expression under the model. Constant-yield values equal $S\exp(-\delta\tau)$, so the negative-yield 1986 benchmark grows with the delivery horizon. The article calls deviations from the two-factor calculation mispricing; empirically these are model-to-model differences, not discrepancies against observed ten-year delivery transactions. Its footnote says differences from the earlier Gibson–Schwartz table reflect a parameter-reporting typo in that earlier paper; this article does not independently re-estimate the parameter set.

The model assumes time-homogeneous convenience-yield parameters, Gaussian rates and yields, constant Brownian correlations, and independent compensated jumps. It does not introduce seasonal yield means or seasonal jump intensities, despite discussing weather-driven energy shocks. The initial interest-rate curve is fitted exactly, while the commodity curve is constrained by the parametric yield process; the latter is not automatically fitted to every observed maturity. There are no transaction costs, delivery-location basis risks, discrete-margining adjustments, collateral conventions, or tests of long-horizon parameter stability. The useful output is a transparent pricing architecture, together with explicit conditions under which linear claims are insensitive to jumps or rate dynamics—not evidence that those conditions hold in every commodity market.

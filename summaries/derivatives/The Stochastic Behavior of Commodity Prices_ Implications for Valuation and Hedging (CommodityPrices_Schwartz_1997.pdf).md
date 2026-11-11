# The Stochastic Behavior of Commodity Prices: Implications for Valuation and Hedging

Eduardo S. Schwartz, *Journal of Finance* 52(3), July 1997, pp. 923–973. [Source PDF](../../Finance/CommodityPrices_Schwartz_1997.pdf). The supplied 53-page file includes the cover, a portrait page, the complete article, and references. PDF page 2 is printed page 923; after the portrait, printed page 924 is PDF page 4. No separate appendix appears in the supplied article.

## Why this matters

A model can fit the liquid end of a commodity curve and still imply poor long-dated valuations and hedges. Schwartz makes this problem concrete by comparing three models estimated from futures prices: a mean-reverting log spot price; a spot price with stochastic mean-reverting convenience yield; and the latter with stochastic interest rates. All three have log futures prices affine in their latent states, allowing Kalman-filter estimation even when spot prices and instantaneous convenience yields are not directly observable.

The central empirical distinction is between forcing long-dated futures volatility to zero and allowing a nonzero long-horizon limit. The one-factor log-price model forces all curves toward the same long-run price and removes sensitivity to current spot as maturity grows. The convenience-yield models retain a persistent price component. Their short-end pricing can be very similar, yet assumptions about long-run interest rates produce substantial differences in long-dated futures prices, hedge positions, and investment thresholds.

The paper combines a state-space estimation design, cross-sectional maturity holdouts, a limited time-series prediction exercise, and model-based hedging and real-investment examples. It finds much stronger evidence of mean-reverting commodity conditions for oil and copper than for gold. This does not mean that every model makes the spot level stationary: in the two- and three-factor specifications it is convenience yield that is an OU factor. The distinction matters for extrapolation and for interpreting the empirical claim of mean reversion.

Several numerical and typographical inconsistencies are visible in the source. This note preserves the reported estimates and separately identifies algebraic reconstructions. In particular, the copper one-factor risk-premium sign, two Enron limiting volatilities, and the normalization of a bond hedge cannot all be used literally as printed.

## Model 1: mean reversion of log spot

The physical spot process is

$$
dS=\kappa(\mu-\log S)Sdt+\sigma S\,dW,
\qquad \kappa>0.
$$

With $X=\log S$, Itô's formula gives

$$
dX=\kappa(\alpha-X)dt+\sigma dW,
\qquad \alpha=\mu-\frac{\sigma^2}{2\kappa}.
$$

The source parameterizes the pricing-measure mean as $\alpha^*=\alpha-\lambda$. Thus $\lambda$ in this model is a shift in the long-run log-price mean; it is not numerically the same risk-premium convention used in Model 2. Under the pricing measure, $X_{t+\tau}$ is Gaussian with mean $e^{-\kappa\tau}X_t+(1-e^{-\kappa\tau})\alpha^*$ and variance $\sigma^2(1-e^{-2\kappa\tau})/(2\kappa)$. With constant rates, the futures and forward price is

$$
F_1(S,\tau)=\exp\left[e^{-\kappa\tau}\log S
+(1-e^{-\kappa\tau})\alpha^*
+\frac{\sigma^2}{4\kappa}(1-e^{-2\kappa\tau})\right].
$$

This is an exact solution of the model, not a small-volatility approximation. The last term is essential because the mean of a lognormal level differs from the exponential of its mean log. Futures return variance is $\sigma^2e^{-2\kappa\tau}$, and

$$
F_1(S,\infty)=\exp\left(\alpha^*+\frac{\sigma^2}{4\kappa}\right)
=\exp\left(\mu-\lambda-\frac{\sigma^2}{4\kappa}\right).
$$

Both the long-run futures price and zero limiting futures volatility are independent of today's spot price. This sharply restricts the curve's response to new information. It does not imply that every finite-maturity curve is strictly monotone: differentiating the displayed log-price expression gives $e^{-\kappa\tau}[-\kappa(X-\alpha^*)+\sigma^2e^{-\kappa\tau}/2]$, which can change sign. The robust criticism is the fixed long-run anchor and vanishing sensitivity, not a universal monotonicity theorem.

Price units matter because the state is a logarithm. Copper estimates based on cents must be transformed consistently before applying a valuation example in dollars. Dividing prices by 100 subtracts $\log100$ from $X$, $\mu$, and the corresponding long-run log levels; it does not change diffusion volatility or reversion speed.

## Models 2 and 3: spot, yield, and rates

Model 2 has physical dynamics

$$
\frac{dS}{S}=(\mu-\delta)dt+\sigma_1dW_1,
\qquad d\delta=\kappa(\alpha-\delta)dt+\sigma_2dW_2,
\qquad dW_1dW_2=\rho\,dt.
$$

The net convenience yield $\delta$ is the instantaneous service rate from physical ownership. Positive spot–yield correlation reflects the scarcity mechanism: lower inventories can raise both spot prices and marginal inventory services. The paper imposes a diffusion representation rather than modeling stocks explicitly. Under the pricing measure, spot drift becomes $r-\delta$ and yield drift becomes $\kappa(\widehat\alpha-\delta)$, where $\widehat\alpha=\alpha-\lambda/\kappa$. Here $\lambda$ is a drift adjustment in the yield equation, not Model 1's mean shift.

For a compact reconstruction, define

$$
H_k(\tau)=\frac{1-e^{-k\tau}}k,\quad
I_1(k,\tau)=\int_0^\tau H_k(u)du=\frac{\tau-H_k(\tau)}k,
$$

$$
I_2(k,\tau)=\int_0^\tau H_k(u)^2du
=\frac{\tau-H_k(\tau)-kH_k(\tau)^2/2}{k^2}.
$$

Then equations (18)–(20) are

$$
\log F_2=X-\delta H_\kappa(\tau)+A(\tau),
$$

$$
A(\tau)=r\tau-\widehat\alpha[\tau-H_\kappa(\tau)]
+\frac12\sigma_2^2I_2(\kappa,\tau)
-\rho\sigma_1\sigma_2I_1(\kappa,\tau).
$$

This integral representation is algebraically equivalent to the source's expanded exponent. It is convenient near coincident reversion speeds and for validating limits. $S$ retains an unattenuated coefficient in log futures prices, while the current yield loading tends to $-1/\kappa$. Consequently, stationary yield does not make log spot stationary: the integrated shocks generally leave a nonzero long-horizon diffusion component.

Model 3 adds the risk-neutral Vasicek process

$$
dr=a(m^*-r)dt+\sigma_3dW_3,
$$

with $\rho_1=\operatorname{corr}(dW_1,dW_2)$, $\rho_2=\operatorname{corr}(dW_2,dW_3)$, and $\rho_3=\operatorname{corr}(dW_1,dW_3)$. The full correlation matrix must be positive semidefinite. Define

$$
I_{\kappa a}(\tau)=\int_0^\tau H_\kappa(u)H_a(u)du
=\frac{\tau-H_\kappa(\tau)-H_a(\tau)+H_{\kappa+a}(\tau)}{\kappa a}.
$$

The futures solution can be written

$$
\log F_3=X-\delta H_\kappa(\tau)+rH_a(\tau)+C(\tau),
$$

$$
\begin{aligned}
C(\tau)={}&m^*[\tau-H_a(\tau)]-\widehat\alpha[\tau-H_\kappa(\tau)]
+\tfrac12\sigma_2^2I_2(\kappa,\tau)+\tfrac12\sigma_3^2I_2(a,\tau)\\
&-\rho_1\sigma_1\sigma_2I_1(\kappa,\tau)
+\rho_3\sigma_1\sigma_3I_1(a,\tau)
-\rho_2\sigma_2\sigma_3I_{\kappa a}(\tau).
\end{aligned}
$$

A unit discount bond has value

$$
B(r,\tau)=\exp[-rH_a(\tau)-m^*(\tau-H_a(\tau))
+\tfrac12\sigma_3^2I_2(a,\tau)].
$$

The prepaid value $P(S,\delta,r,\tau)$ of one unit delivered later is

$$
P=S\exp[-\delta H_\kappa(\tau)-\widehat\alpha(\tau-H_\kappa(\tau))
+\tfrac12\sigma_2^2I_2(\kappa,\tau)
-\rho_1\sigma_1\sigma_2I_1(\kappa,\tau)].
$$

It is independent of current $r$ under these assumptions, but the forward delivery price $P/B$ is not. Futures equal $E^Q[S_T]$; forwards involve a discounted expectation divided by the bond price. Unlike a curve-fitted HJM model, this Vasicek specification imposes a parametric bond curve through its estimated or fixed rate inputs.

The source treats the Enron forward observations as futures, citing approximately zero spot–rate correlation in footnote 22. That is an empirical approximation, not an exact implication of $\rho_3=0$. The formulas imply

$$
\log\frac{F_3}{P/B}=\sigma_3^2I_2(a,\tau)
+\rho_3\sigma_1\sigma_3I_1(a,\tau)
-\rho_2\sigma_2\sigma_3I_{\kappa a}(\tau).
$$

Integrated-rate variance and rate–yield covariance can survive when instantaneous spot–rate correlation is zero. This matters particularly for the long maturities used to motivate the paper.

## State-space estimation: what was actually fitted

At observation date $t$, the measurement vector contains log futures prices at their actual remaining maturities $\tau_{it}$, rather than fixed-maturity interpolated observations. The generic equation is $y_t=d_t+Z_tz_t+\epsilon_t$. Measurement errors have zero mean, are serially uncorrelated, and are cross-sectionally uncorrelated, with diagonal covariance $H$. They accommodate bid–ask effects, price limits, nonsynchronous observations, and data error. The diagonal assumption attributes systematic cross-maturity dependence to the latent factors.

For Model 1, $z_t=X_t$, the $i$th row of $Z_t$ is $e^{-\kappa\tau_{it}}$, and $d_{it}$ is the non-state part of the log futures formula. Equation (33) uses the Euler transition

$$
X_t=\kappa\alpha\Delta t+(1-\kappa\Delta t)X_{t-1}+\eta_t,
\qquad \operatorname{Var}(\eta_t)=\sigma^2\Delta t.
$$

The source footnote gives the exact OU mean transition and says weekly approximation yields parameter estimates identical through the fourth significant digit. The exact innovation variance is $\sigma^2(1-e^{-2\kappa\Delta t})/(2\kappa)$; merely replacing the mean coefficient while retaining Euler variance is not a fully exact discretization.

For Model 2, $z_t=(X_t,\delta_t)'$, measurement rows are $(1,-H_\kappa(\tau_{it}))$, and intercepts are $A(\tau_{it})$. The fitted transition is

$$
z_t=\begin{pmatrix}(\mu-\sigma_1^2/2)\Delta t\\\kappa\alpha\Delta t\end{pmatrix}
+\begin{pmatrix}1&-\Delta t\\0&1-\kappa\Delta t\end{pmatrix}z_{t-1}+\eta_t,
$$

$$
Q=\operatorname{Var}(\eta_t)=\Delta t
\begin{pmatrix}\sigma_1^2&\rho\sigma_1\sigma_2\\
\rho\sigma_1\sigma_2&\sigma_2^2\end{pmatrix}.
$$

Equation (35) visibly prints $\sigma_1^2\Delta t$ in the lower-right cell. The yield SDE requires $\sigma_2^2\Delta t$, as written here. This is a derived correction to the display; the article does not supply code establishing which value was used numerically.

An exact discretization is available because the physical state system is linear Gaussian. As a reconstruction beyond the paper's fitted approximation, its transition matrix is $\left(\begin{smallmatrix}1&-H_\kappa(\Delta)\\0&e^{-\kappa\Delta}\end{smallmatrix}\right)$; the intercept is $((\mu-\sigma_1^2/2-\alpha)\Delta+\alpha H_\kappa(\Delta),\,\alpha(1-e^{-\kappa\Delta}))'$. Its covariance entries are

$$
Q_{11}=\sigma_1^2\Delta+\sigma_2^2I_2(\kappa,\Delta)
-2\rho\sigma_1\sigma_2I_1(\kappa,\Delta),
$$

$$
Q_{12}=\rho\sigma_1\sigma_2H_\kappa(\Delta)
-\frac12\sigma_2^2H_\kappa(\Delta)^2,
\qquad Q_{22}=\frac{\sigma_2^2(1-e^{-2\kappa\Delta})}{2\kappa}.
$$

Using these exact transitions would be a documented variant, not a literal reproduction of equation (35).

Model 3 is estimated in a simplified two-stage fashion. Rate inputs are first obtained separately; the commodity filter still estimates only $X$ and $\delta$. Its measurement intercept adds observed $r_tH_a(\tau_{it})+C(\tau_{it})$, and its transition remains equation (35). It is therefore not a joint three-state maximum-likelihood fit to commodity and bond observations.

For any candidate parameter vector, a reproducible Kalman implementation predicts the state and covariance, forms innovations $v_t=y_t-d_t-Z_t\widehat z_{t|t-1}$ with covariance $\Omega_t=Z_tP_{t|t-1}Z_t'+H$, accumulates the Gaussian log likelihood, and updates with gain $P_{t|t-1}Z_t'\Omega_t^{-1}$. The likelihood contribution is $-[N\log(2\pi)+\log|\Omega_t|+v_t'\Omega_t^{-1}v_t]/2$. The optimizer estimates process parameters, risk premia, and measurement-error standard deviations $\xi_i$. Several $\xi_i$ hit zero; this is not evidence that all contracts are observed without noise. Covariance definiteness, stable factorization, initialization, and boundary constraints matter. The article does not give initial-state priors, diffuse-initialization choices, optimizer starts, tolerances, or code, so these must be recorded as replication choices.

## Data, maturity selection, and rate calibration

Daily Knight–Ridder observations are reduced to approximately weekly observations by taking every fifth observation. This is not necessarily a fixed weekday calendar. Five contracts are fitted in each public-data experiment; contract number means order by delivery, not a fixed number of months. Actual time to maturity changes as contracts roll, as Figure 1 shows.

| Sample | Dates and observations | Fitted contracts | Longest average maturity |
|---|---|---|---:|
| Oil A | 2 January 1985–17 February 1995; 510 | F1, F3, F5, F7, F9 | 0.710 years |
| Oil B | 2 January 1990–17 February 1995; 259 | Same as A | 0.709 years |
| Oil C | Same dates and count as B | F1, F5, F9, F13, F17 | 1.374 years |
| Copper | 29 July 1988–13 June 1995; 347 | F1, F3, F5, F7, F9 | 1.663 years |
| Gold A | 2 January 1985–13 June 1995; 527 | F1, F3, F6, F9, F11 | 1.749 years |
| Gold B | 21 November 1990–13 June 1995; 230 | Same as gold A | 1.745 years |
| Gold C | Same dates and count as B | F1, F5, F9, F13, F18 | 4.703 years |

The corresponding earliest average maturities are 0.043 years for oil, 0.109 for copper, and 0.084 for gold. Mean oil-A prices decline from 19.99 at F1 to 19.21 at F9; copper means decline from 110.04 to 99.78 cents, whereas gold-A means rise from 379.27 to 418.87 dollars. These summaries describe the sample curves, not a forecastable expected return.

Enron supplied proprietary oil forward curves dated 15 January 1993–16 May 1996, with 163 approximately weekly observations. Ten fitted maturities are two, five, and eight months; one, one-and-a-half, two, three, five, seven, and nine years. Their mean remaining maturities range from 0.122 to 8.955 years. Mean prices range from 18.16 at the first point to 20.92 at the last. The author explicitly does not know exactly how these curves were constructed. They provide useful long-horizon information, but are not a transparent transaction-price dataset.

Model 2 assumes a constant rate of 6%, except 5% for Enron's later period. Variation in actual interest rates can consequently be absorbed into inferred convenience yield. Model 3 uses three-month Treasury-bill yields, with rate volatility estimated from contemporaneous yield changes. It fixes $a=0.2$, corresponding to a half-life $\log2/0.2\approx3.47$ years, rather than estimating it jointly. It chooses $m^*$ to make the asymptotic bond yield 7%:

$$
R(\infty)=m^*-\frac{\sigma_3^2}{2a^2}=0.07.
$$

The commodity–rate correlations are approximated using weekly rate observations and Model-2 inferred states. These are plug-in inputs, and their uncertainty is not propagated through a full joint likelihood. The treatment of yield conversion, day counts, missing quotes, delivery specifications, and exact rolling dates is not fully supplied. No portfolio formation, trading costs, or executable hedging backtest is part of the estimation design.

## Parameter estimates and an important sign inconsistency

For one-factor oil, the estimated reversion speed is 0.301 (SE 0.005) in sample A, 0.694 (0.010) in B, 0.428 (0.008) in C, and 0.099 (0.003) for Enron. Extending the maturity range materially changes inferred reversion. Associated volatilities are 0.334, 0.326, 0.257, and 0.129. The much lower Enron volatility also reflects a later sample without the Gulf War, so maturity and sample effects should not be conflated. Model 1 could not be fitted to gold.

Table V reports copper $\kappa=0.369$ (0.009), $\mu=4.854$ (0.230), $\sigma=0.233$ (0.007), and $\lambda=-0.339$ (0.230). However, the prose calls the risk premium positive, and the later claimed limiting futures price is 88.08 cents. Using the printed negative sign in equations (3), (4), and (38) gives 173.507 cents. Changing only the sign to $+0.339$ gives 88.07765 cents, consistent with the later discussion and mine example. Thus the sign change is strongly supported as a reconstruction of the intended calibration, but the original table and missing estimation code prevent treating it as independently verified numerical output.

There is also a smaller long-oil discrepancy. Table IV's sample-C parameters $\mu=2.991$, $\lambda=0.002$, $\sigma=0.257$, and $\kappa=0.428$ imply a limit of 19.11398 dollars, whereas the text says 20.13. The Enron parameters imply 22.98811, agreeing with the stated 22.99. These differences should be resolved before using the one-factor parameters to reproduce long-horizon valuations.

The central two-factor estimates are:

| Parameter | Long oil C | Copper | Enron oil |
|---|---:|---:|---:|
| $\mu$ | 0.238 (0.160) | 0.326 (0.110) | 0.082 (0.120) |
| $\kappa$ | 1.488 (0.027) | 1.156 (0.041) | 1.187 (0.026) |
| $\alpha$ | 0.180 (0.126) | 0.248 (0.098) | 0.090 (0.086) |
| $\sigma_1$ | 0.358 (0.010) | 0.274 (0.012) | 0.212 (0.011) |
| $\sigma_2$ | 0.426 (0.017) | 0.280 (0.017) | 0.187 (0.012) |
| $\rho$ | 0.922 (0.006) | 0.818 (0.020) | 0.845 (0.024) |
| $\lambda$ | 0.291 (0.190) | 0.256 (0.114) | 0.093 (0.101) |

Oil-A yield reversion is even faster, 1.876 (0.024), with correlation 0.766 (0.013). The two-factor oil-A log likelihood is 10267 versus 8130 for one factor. Copper values are 6473 versus 5482. The estimated average convenience yields are instantaneous rates; copper's 0.248 is not the average carry rate across a long futures interval. Several drift and premium estimates have large standard errors despite precise covariance and reversion estimates.

Three-factor long-oil estimates are $\kappa=1.314$ (0.027), $\alpha=0.249$ (0.093), $\sigma_1=0.344$ (0.009), $\sigma_2=0.372$ (0.014), $\rho_1=0.915$ (0.007), and $\lambda=0.353$ (0.123). Copper gives 1.045 (0.030), 0.255 (0.078), 0.266 (0.011), 0.249 (0.014), 0.805 (0.022), and 0.243 (0.082), respectively. Enron gives 0.976 (0.022), 0.038 (0.077), 0.196 (0.009), 0.145 (0.008), 0.809 (0.027), and 0.013 (0.075). Rate volatilities are 0.0081, 0.0096, and 0.0073 for those three samples.

Gold changes the interpretation. Model 2's long-maturity sample estimates $\kappa=0.298$ (0.018), but Model 3 reduces it to 0.023 (0.023). Its rate–yield correlation is −0.4005, and its spot–yield correlation is only 0.208 (0.069). The apparently mean-reverting yield in the constant-rate model may partly proxy for omitted rate variation. This is evidence against transferring the oil/copper interpretation mechanically to a monetary precious metal.

The empirical models are not straightforward nested likelihood comparisons. Model 1 is not nested in the fitted Model 2, while Model 3's rate inputs are partly fixed externally. Higher likelihood is useful descriptive evidence, but a routine chi-square likelihood-ratio test is not justified by counting added theoretical factors.

## Pricing comparisons and their information sets

The cross-sectional tests price maturities excluded from the estimation vector, using parameters fitted over the entire sample and the contemporaneously inferred states. They hold out 12 oil contracts, four copper contracts, and ten Enron maturities. Thus they test interpolation or extrapolation across contracts, with dependence among contracts and full-period parameter information; they are not rolling future-date forecasts.

Tables XII–XIV report aggregate percentage RMSE for Models 1/2/3 of 2.740/0.920/1.011 for oil, 2.284/0.713/0.692 for copper, and 4.072/2.582/2.224 for Enron. Corresponding monetary RMSE values are 0.668/0.193/0.210 dollars for oil, 2.612/0.819/0.794 cents for copper, and 0.789/0.532/0.459 dollars for Enron. Shortest-maturity errors are often the largest: oil F2 percentage RMSE is 6.203/2.574/2.795. Model 2 slightly beats Model 3 for public oil, whereas Model 3 is better for copper and the longer Enron data.

A separate time-series exercise examines the last 50 observations. Panel A uses parameters estimated over the entire sample; Panel B estimates parameters after excluding those last 50 observations and then holds those parameters fixed while computing prediction errors. States are updated through the filter. The author describes these as lower and upper error bounds relative to continually re-estimating parameters. They are comparison procedures, not mathematically guaranteed bounds: updating a noisy parameter estimate need not improve realized prediction error monotonically.

Aggregate log-price RMSE in Panels A/B is oil 0.0435/0.0477 for Model 1, 0.0300/0.0303 for Model 2, and 0.0299/0.0299 for Model 3. Copper gives 0.0296/0.0297, 0.0260/0.0273, and 0.0253/0.0261. Enron gives 0.0483/0.0594, 0.0225/0.0279, and 0.0251/0.0258. These are errors in log price, distinct from the percentage errors in the earlier cross-sectional tables. The strongest gains are against Model 1; ranking Models 2 and 3 depends on the data and parameter-information convention. No standard errors for differences in forecast loss or formal predictive-accuracy tests are supplied.

## Volatility and long-horizon extrapolation

Model 2's futures variance is

$$
\sigma_F^2(\tau)=\sigma_1^2+\sigma_2^2H_\kappa(\tau)^2
-2\rho\sigma_1\sigma_2H_\kappa(\tau).
$$

Model 3 adds $\sigma_3^2H_a^2+2\rho_3\sigma_1\sigma_3H_a-2\rho_2\sigma_2\sigma_3H_\kappa H_a$. These are instantaneous proportional-return variances, not the variance of a terminal spot level or an option's total integrated variance. Their limits use $H_\kappa\to1/\kappa$ and $H_a\to1/a$. Figure 9 compares them with sample futures-return volatility, which was not separately fitted as a target.

Table XVIII gives zero-maturity/infinite-maturity volatility 0.358/0.145 for two-factor oil and 0.344/0.146 for three-factor oil; copper gives 0.274/0.159 and 0.266/0.166. Model 1 tends to zero for every sample. The Enron infinite-maturity entries are printed as 0.159 and 0.166, identical to copper's. Direct substitution of Enron's reported parameters into equations (41) and (43) gives 0.1154098 and 0.1191276, respectively, consistent with the approximately 0.12 plateau in Figure 9C. These are derived corrections using rounded parameters, not re-estimates of the underlying sample volatility.

The maturity slope of log futures converges in Model 2 to

$$
g_2=r-\widehat\alpha+\frac{\sigma_2^2}{2\kappa^2}
-\frac{\rho\sigma_1\sigma_2}{\kappa}.
$$

Model 3 replaces $r$ with $m^*$ and adds $\sigma_3^2/(2a^2)+\rho_3\sigma_1\sigma_3/a-\rho_2\sigma_2\sigma_3/(\kappa a)$. The reported limits are 2.71% versus 4.19% per year for oil, and 0.85% versus 2.70% for copper. These are forward-curve growth rates with maturity, not expected physical returns. Reducing the imposed infinite-horizon bond yield from 7% to 6% changes Model-3 limits to 3.56% for oil and 2.00% for copper, despite little change in the other fitted parameters.

Table XIX estimates models using only the first five Enron maturities, two months through one-and-a-half years, and prices the remaining two-to-nine-year contracts. Aggregate percentage RMSE is 6.95 for Model 1, 5.81 for Model 2, 8.54 for Model 3 with the 7% long rate, and 3.85 for Model 3 with 6%. At nine years the corresponding errors are 10.53%, 10.22%, 15.68%, and 6.38%. The exercise shows substantial sensitivity to a rate assumption that short commodity contracts cannot tightly identify. It does not establish 6% as a universal correct long-run rate.

## Hedging a future physical delivery

The hedge matches the sensitivities of the prepaid delivery value to the traded futures portfolio. With one factor, $wF_S(S,t_1)=e^{-rT}F_S(S,T)$. With two factors, two futures maturities match both $S$ and $\delta$ derivatives. With three factors, a third futures contract or a discount bond is needed to match the rate exposure. The number of factors is a count of independent risks to span, not a guarantee that arbitrary chosen contracts produce a well-conditioned sensitivity matrix.

For Models 2 and 3, futures derivatives are $F_S=F/S$, $F_\delta=-H_\kappa(\tau)F$, and, in Model 3, $F_r=H_a(\tau)F$. The prepaid claim has $P_S=P/S$, $P_\delta=-H_\kappa(T)P$, and $P_r=0$. These formulas give a direct implementation of equations (46)–(48) without finite-difference noise. Hedge positions change over time and require rebalancing; the source does not evaluate transaction costs, funding needs, or finite-interval hedging error.

Using Enron parameters for a ten-year oil delivery, Model 1 gives about 0.25 one-month contracts when spot is 20 dollars. Model 2 at $\delta=0.10$ gives 1.09 long one-year futures and 0.34 short one-month futures. Model 3 at $\delta=0.10$, $r=0.05$ gives approximately 1.96 long six-month futures and 1.29 short one-month futures, with a bond position to offset their rate exposure.

The source quotes 0.94 long one-year unit discount bonds and says the hedge ratios are independent of spot. Futures contract counts do cancel the common spot factor. Dollar-unit bond counts do not, because a bond's rate sensitivity is independent of commodity spot while the futures' dollar sensitivities scale with spot. Reconstructing the source calculation gives −1.285856 one-month futures, +1.959979 six-month futures, and $0.940610S$ bonds paying one dollar at maturity. The printed 0.94 is reproduced when spot is normalized to one; at spot 20 the bond count is 18.8122. The missing normalization should be made explicit rather than transferring 0.94 unchanged to an arbitrary oil price.

## The real-investment example

The toy copper project produces one unit at each year-end for ten years after investment. Initial cost is 2 dollars and operating cost is 0.40 per unit. The source describes the output as an ounce while its earlier copper prices are quoted per pound; for replication, the cash-flow unit and spot-price unit must be made consistent. Once undertaken, production is committed: there is no abandonment, temporary closure, reopening, or endogenous extraction rate. The only flexibility analyzed is when to invest.

Immediate investment has value

$$
\operatorname{NPV}(S,\delta,r)
=\sum_{j=1}^{10}P(S,\delta,r,j)
-0.40\sum_{j=1}^{10}B(r,j)-2.
$$

The investment option is an optimal stopping problem whose exercise payoff is this NPV. In the continuation region its value satisfies the model's pricing generator minus $rV=0$, with value at least $\max(\operatorname{NPV},0)$ and equality at optimal exercise. The source discusses a perpetual option but notes that the numerical PDE calculations assume a ten-year option maturity. This differs from the ten-year *operating* life beginning after exercise. A reproduction needs both horizons, terminal payoff, boundary conditions, and a discretization; grid dimensions and convergence tolerances are not supplied.

The discounted-cash-flow benchmark assumes flat future spot price and discounts at 10%, 12%, or 15%. Break-even prices and immediate-investment triggers are 0.73, 0.76, and 0.82 dollars. At spot 1 dollar, project values are 1.61, 1.29, and 0.88. These discount rates do not explicitly price the option to wait.

Model 0 is a GBM benchmark with constant convenience yield $c=0.118$, $r=0.06$, and $\sigma=0.266$, using the nearest contract as a spot proxy and the average first-to-last-contract implied yield. Put $\beta_1=\sum_{j=1}^{10}e^{-cj}$ and $\beta_2=0.40\sum_{j=1}^{10}e^{-rj}+2$, so NPV is $S\beta_1-\beta_2$. The perpetual option's positive root is

$$
d=\frac12-\frac{r-c}{\sigma^2}
+\sqrt{\left(\frac12-\frac{r-c}{\sigma^2}\right)^2+\frac{2r}{\sigma^2}},
\qquad S^*=\frac{\beta_2d}{\beta_1(d-1)}.
$$

Below the trigger, $V=(S^*\beta_1-\beta_2)(S/S^*)^d$; above it, immediate NPV applies. Recalculation gives $d=3.173802$, $S^*=1.298372$, and $V(1)=0.987903$, reproducing Table XX's 1.30 and 0.99. The zero-NPV point is about 0.89, well below the investment trigger.

Table XX's mean-reverting Model 1 reports zero NPV at 0.26 and investment at 0.97, with value 1.75 at spot 1. This uses the approximately 0.88 long-run copper price discussed earlier, so reproducing it requires resolving the printed risk-premium sign inconsistency. Model 2 with $\delta=0.10,0.25,0.40$ gives triggers 1.12, 1.20, and 1.32; the corresponding zero-NPV prices are 0.70, 0.80, and 0.90. At spot 1 their option values are 2.38, 1.68, and 1.15. An instantaneous yield of 0.25 is not directly comparable to Model 0's maturity-averaged 0.118.

Model 3 at $r=0.06$ gives triggers 1.02, 1.14, and 1.26 for those same yields, with values at spot 1 of 2.55, 1.69, and 1.05. At yield 0.25, varying the rate from 0.03 to 0.06 to 0.09 changes the trigger from 1.10 to 1.14 to 1.24. The rate affects discounting, dynamics, and the opportunity cost of waiting, so an isolated NPV comparison does not determine the investment threshold.

These calculations demonstrate model sensitivity rather than proving which valuation rule is empirically correct. The paper explicitly says actual project transaction prices would be needed to judge superiority. The useful lesson is that a fit to short contracts does not settle long-lived real-asset decisions, especially when the model imposes a fixed terminal price, uncertain long-rate assumptions, or a convenience-yield process without explicit inventory and production constraints.

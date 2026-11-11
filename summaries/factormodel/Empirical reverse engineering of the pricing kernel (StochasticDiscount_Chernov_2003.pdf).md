# Empirical reverse engineering of the pricing kernel

**Mikhail Chernov (2003).** *Journal of Econometrics* 116, 329–364. DOI: 10.1016/S0304-4076(03)00111-8. Source: [StochasticDiscount_Chernov_2003.pdf](../../Finance/StochasticDiscount_Chernov_2003.pdf). All 36 PDF pages, including Appendices A–D, were read. Printed page 329 is PDF page 1. Key equations and Tables 2, 4, and 5 were checked visually because the PDF text layer corrupts Greek symbols. This note reconstructs the published model and identifies places where the printed formulas or data definitions do not fully specify a reproducible implementation.

## Why this matters and the actual contribution

The paper estimates a positive stochastic discount factor (SDF) without choosing a consumption utility function or observing consumption. It first estimates a joint continuous-time model for several asset markets under the physical and risk-neutral measures. The change of measure determines the latent pricing kernel. It then simulates that kernel and observable asset prices together, learns a flexible conditional density, and uses it to recover the kernel from actual contemporaneous and lagged observations. This second stage is called reprojection.

The novelty is the combination of a common multi-asset pricing model, derivative information identifying prices of risk, and nonlinear filtering of an unobserved SDF. It separates the law of the kernel from a state-price density for one particular terminal asset price. The empirical design compares kernels filtered on different information sets and evaluates them using additional option returns and a later sample.

The preferred reprojection uses only S&P 500 returns at the filtering stage, although its structural parameters were estimated using several markets. It is a nonlinear function of current and lagged index returns. Therefore “uses only the index” does not mean that the full estimation procedure used only index data. A separate kernel inferred by inverting Treasury prices has smaller reported pricing errors but visibly violates the model's innovation assumptions.

The paper is also an informative misspecification exercise. A common latent state drives both short rates and equity volatility, there are no jumps, and option returns are difficult to price. The preferred daily filtered kernel remains above one throughout the sample. These facts qualify the abstract's claim of consistency with observed prices: the model is internally arbitrage-consistent under its assumptions, but its empirical fit is imperfect. No consumption model is identified uniquely by this procedure.

## State variables and physical-measure dynamics

Use $U_t$ for the paper's common variance state $U_2(t)$, $V_{i,t}$ for asset-specific variance states, and $L_{i,t}=\log S_{i,t}$. Let $W_1,W_2,Z_i,B_i$ be independent Brownian motions. The parameter $\rho$ creates correlation between asset shocks and the common variance shock; it is not correlation between the primitive Brownian motions. Writing the paper's $\iota_i$ as $k_i$ for readability,

$$
\frac{dS_i}{S_i}=(r_0+\alpha_iU)dt
+\beta_i\sqrt U\left(\sqrt{1-\rho^2}\,dW_1+\rho\,dW_2\right)
+\gamma_i\sqrt{V_i}\,dZ_i,
$$

$$
dU=(\theta-\kappa U)dt+\sqrt U\,dW_2,
\qquad
dV_i=(\eta_i-k_iV_i)dt+\sqrt{V_i}\,dB_i.
$$

The state diffusion coefficients are normalized to one; asset loading scales reside in $\beta_i$ and $\gamma_i$. The log-price drift is $r_0+\alpha_iU-\tfrac12\beta_i^2U-\tfrac12\gamma_i^2V_i$. The common state affects both expected returns and variance. Idiosyncratic variance is stochastic but receives no risk premium in the selected pricing measure.

For positive mean-reversion parameters the stationary means are $\theta/\kappa$ and $\eta_i/k_i$, and shock half-lives are $\log2/\kappa$ and $\log2/k_i$. Nonnegativity and boundary handling must be respected numerically. The sufficient Feller condition for a strictly positive common CIR state is $2\theta\ge1$ under this normalization, with analogous $2\eta_i\ge1$ for idiosyncratic states. These are useful implementation conditions; the PDF does not state its optimizer's exact admissibility constraints or its Euler boundary rule.

The instantaneous short rate is $r_t=r_0+r_1U_t$. The S&P 500 is assumed fully diversified, imposing $\gamma_0=0$ and eliminating its idiosyncratic state. Other $S_i$ represent gold spot and the POM and NSM equities. Gold futures are derived prices of the gold spot process, not observations to be inserted directly as $S_1$ in the spot SDE.

## Prices of risk and the latent kernel

The market prices of the two common Brownian risks are $\lambda_1\sqrt U$ and $\lambda_2\sqrt U$. Prices of $Z_i$ and $B_i$ risks are zero. Set

$$
dW_j^Q=dW_j+\lambda_j\sqrt U\,dt,
\qquad
\kappa^Q=\kappa+\lambda_2,
$$

and impose the common pricing restriction

$$
\alpha_i=r_1+\beta_i\left(\lambda_1\sqrt{1-\rho^2}+\lambda_2\rho\right).
$$

Then the risk-neutral asset drift is $r_t$, the common variance mean reversion becomes $\kappa^Q$, and idiosyncratic-state dynamics are unchanged. This is a substantive selection among pricing measures in an incomplete market. No-arbitrage alone does not imply zero premiums on every unspanned variance shock.

The likelihood-ratio increment is the stochastic exponential

$$
\frac{dQ}{dP}\Big|_{[t,t+h]}
=\exp\left[-\frac12(\lambda_1^2+\lambda_2^2)\int_t^{t+h}U_sds
-\sum_{j=1}^2\lambda_j\int_t^{t+h}\sqrt{U_s}\,dW_{j,s}\right].
$$

Discounting it yields the kernel ratio $m_{t+h}=\Lambda_{t+h}/\Lambda_t$, with

$$
\frac{d\Lambda}{\Lambda}
=-(r_0+r_1U)dt-\lambda_1\sqrt U\,dW_1-\lambda_2\sqrt U\,dW_2.
$$

For daily simulation, generate $n_t=\log m_t$ using

$$
n_t=-\int_{t-1}^{t}\left[r_0+\left(r_1+\frac12(\lambda_1^2+\lambda_2^2)\right)U_s\right]ds
-\sum_{j=1}^2\lambda_j\int_{t-1}^{t}\sqrt{U_s}\,dW_{j,s}.
$$

The time interval here denotes one observed trading day, represented as $1/250$ of a year. Exponentiating $n_t$ preserves positivity. Using a linear Euler update directly on $m$ can produce negative values and would not reproduce that property.

The construction makes expected excess asset returns equal to minus their instantaneous covariance with the kernel return. It also sets the expected kernel drift to minus the short rate. It does not empirically solve a representative-agent equity-premium puzzle; those relations are imposed restrictions that may cause rejection of the joint asset-dynamics model.

A technical qualification to footnote 6 is needed: pathwise boundedness of a continuous CIR trajectory on a finite interval does not itself establish the exponential integrability required by Novikov's condition. A reproduction should verify a valid martingale condition for the chosen parameters/horizon or use an appropriate affine-diffusion argument. The positive stochastic exponential alone is not a proof that its expectation is one.

## Derivative pricing and a correction needed in Appendix A

The generalized transform is

$$
F(t,h;z,v)=E_t^Q\exp\left[izL_{t+h}+iv\int_t^{t+h}r_sds\right]
=\exp\{izL_t+C(h)+A_u(h)U_t+A_v(h)V_t\}.
$$

A zero-coupon bond with unit face value is $F(t,h;0,i)$; a gold futures price is $F(t,h;-i,0)$. The affine transform permits consistent inclusion of different maturities without adding separate pricing parameters for every derivative.

A robust implementation can solve the Riccati equations instead of copying complex-root formulas:

$$
A_u'=\tfrac12A_u^2-(\kappa^Q-iz\beta\rho)A_u
-\tfrac12\beta^2z(z+i)+ir_1(z+v),
$$

$$
A_v'=\tfrac12A_v^2-k_iA_v-\tfrac12\gamma_i^2z(z+i),
\qquad
C'=\theta A_u+\eta_iA_v+ir_0(z+v),
$$

with all three functions zero at $h=0$. These equations follow directly from the stated risk-neutral generator and supply an auditable version of Appendix A. The published A6 instead prints the idiosyncratic forcing as $+\tfrac12\gamma^2z(z-i)$. That is inconsistent with the log-price drift and diffusion in equations 6–8: the generator requires $-\tfrac12\gamma^2(z^2+iz)$. At $z=-i$, the correct idiosyncratic forcing vanishes, as it must for the conditional expected spot level; the printed one does not. This is a source-level discrepancy, not a text-extraction artifact.

With $c_j$ denoting the respective forcing term and $k_u=\kappa^Q-iz\beta\rho$, $k_v=k_i$, the closed-form Riccati solution can equivalently use roots $a_{j,\pm}=k_j\pm\sqrt{k_j^2-2c_j}$ and

$$
A_j(h)=\frac{2c_j(e^{h(a_{j,+}-a_{j,-})/2}-1)}{a_{j,+}e^{h(a_{j,+}-a_{j,-})/2}-a_{j,-}}.
$$

Complex square-root/log branches must be chosen continuously. Integrating $C'$ is a convenient check against branch mistakes. For bond prices, $A_v=0$, so the common-state affine bond formula supports the later inversion $U_t=[\log B_t-C(h)]/A_u(h)$.

## Data construction, clocks, and evaluation assets

The complete data span March 1, 1988–August 29, 1997, 2,353 daily observations. The start excludes the October 1987 crash and its immediate aftermath because the diffusion has no explicit extreme-move component. The reported estimation sample ends August 29, 1996; the later evaluation interval is September 1996–August 29, 1997. This is one historical split, not rolling cross-validation.

The five fitting series are S&P 500 index data from CBOE; short-dated COMEX gold futures (GC); Potomac Electric Power (POM) and National Semiconductor (NSM) stock data from CRSP; and three-month Treasury bill bank-discount yields from FRED. Equity and gold series enter as log returns; the Treasury yield enters in levels. It is not substituted directly for the instantaneous short rate.

Markets close at different times: gold 2:30 p.m., Treasury quotes 3:30 p.m., equities 4 p.m., and evaluation index options 4:15 p.m. Simulation is sampled at these separate clocks. The paper describes successive intraday increments of 2 hours, 1 hour, half an hour, and a quarter hour from 12:30 p.m., with an eight-hour business day equal to $1/250$ year. Those four increments alone sum to 3.75 hours, not eight. The treatment of the remaining interval and overnight transition is not fully described; it must be resolved in implementation rather than silently assigning a whole day only to those four increments.

For the index the simulation assumes a continuous dividend rate of 2% annually. It does not fully specify all CRSP corporate-action/dividend adjustments for the two stocks. For Treasury prices, convert bank-discount yield $Y$ to $B=F(1-Yd/360)$, where $F$ is face value and $d$ calendar days to maturity. The quote cycle uses 89 days on Tuesday, 88 Wednesday, 87 Thursday, 86 Friday, and 83 on Monday before switching to the next bill. Calendar holidays and exact matching rules are not supplied.

Gold uses the shortest available maturity subject to at least seven business days remaining, with maturities described as ranging from 7 to 28 business days. The prose describes an increasing countdown followed by a downward reset, which is inconsistent with the ordinary passage of time for a held contract. Reproduce the contract-selection rule using actual expiration dates and flag that sentence rather than reverse the time axis.

Options are held out from structural fitting. Four added return series target: S&P 500 puts with moneyness near 1.00 and 50 days; S&P 500 puts near 1.06 and 6 days; NSM calls near 1.00 and 6 days; and NSM calls near 0.94 and 100 days. Appendix B calls the second and fourth out-of-the-money. Footnote 24 says moneyness is “option price divided by strike,” which is incompatible with these categories; the listed values are consistent with underlying-price/strike moneyness. The correct original contract selection cannot be established from the footnote alone. Treat underlying/strike as an explicitly documented reconstruction, not a verified definition.

One-day derivative gross returns match the same contract on adjacent days: $C_{t+1}(h-\Delta,K)/C_t(h,K)$, and likewise for puts and futures prices. This avoids taking ratios of different contracts on roll dates. Treasury returns cannot be formed consistently at the weekly bill switch, so Treasuries are excluded from the HJ return tests. The four-asset tests use index, gold, POM, and NSM; eight-asset tests add the four options.

A futures-price ratio is the source's diagnostic convention, not the self-financing return on a zero-cost futures position. With stochastic rates, futures prices are martingales under the risk-neutral measure, while discounted futures *price levels* need not be. A financial implementation must distinguish this convention from a collateralized futures investment return. The PDF supplies no collateral or funding rule that resolves that difference.

## Simulated moments: objective, parameters, and missing controls

The structural parameter vector has twenty entries: seven common parameters $(r_0,r_1,\lambda_1,\lambda_2,\rho,\theta,\kappa)$; four $\beta_i$; and three each of $\gamma_i,\eta_i,k_i$ for nonindex assets. Risk-premium slopes $\alpha_i$ and $\kappa^Q$ are derived rather than independently estimated.

The 31 matching moments are, for five fitting series $r_{i,t}$: five $E|r_i|$; fifteen unique contemporaneous second cross-moments $E[r_ir_j]$; five lag-one products $E[r_{i,t}r_{i,t-1}]$; five lag-one squared products $E[r_{i,t}^2r_{i,t-1}^2]$; and one leverage moment $E[r_{0,t}^2r_{0,t-1}]$. The Treasury $r_4$ is a yield level despite the common return notation. These are raw products, not automatically demeaned covariances.

For candidate parameters, simulate the latent states, spot processes, and derived quotes; sample the proper market clocks; compute the same 31 moments; and minimize the weighted discrepancy from empirical moments. The author uses a diagonal continuously updated weighting matrix for numerical stability instead of optimal full covariance weighting. This loses asymptotic efficiency but reduces difficult numerical interactions. The moment Jacobian is checked to have full local rank. Experiments from just identification to 46 moments did not improve the practical exercise reliably.

The simulator is Euler–Maruyama of strong order one-half. The article does not supply structural simulation length, burn-in, random-number seed, common-random-number policy, exact diagonal long-run covariance calculation, optimizer tolerances, or the response to negative Euler variance states. These are real reproducibility gaps. The separate 100,000-observation simulation count below belongs to reprojection and must not be silently assigned to the first-stage SMM run.

Table 2 reports common estimates, with standard errors in parentheses: $\theta=0.7172$ (0.42), $\kappa=1.8077$ (1.07), $r_0=0.0214$ (0.01), $r_1=0.0894$ (0.03), $\lambda_1=0.5581$ (0.66), $\lambda_2=-0.8371$ (0.28), and $\rho=-0.4817$ (0.71). The volatility-price parameter is relatively precise; the first risk-price and leverage-correlation estimates are not. Do not interpret every point estimate as statistically established.

| Asset | $\beta_i$ | $\gamma_i$ | $\eta_i$ | $k_i$ |
|---|---:|---:|---:|---:|
| S&P 500 | 0.2705 | 0 imposed | — | — |
| Gold spot underlying GC | −0.1984 | $0.2668\times10^{-4}$ | 2.5805 | 4.1597 |
| POM | 0.2850 | 0.6803 | 1.3155 | 0.9418 |
| NSM | 0.9326 | 0.1378 | 16.2226 | 5.0421 |

The corresponding standard errors for the beta row are 0.04, 0.02, 0.04, and 0.14. For gold/POM/NSM, gamma standard errors are $0.34\times10^{-4}$, 0.09, and 0.01; eta standard errors 0.92, 0.13, 3.21; and mean-reversion standard errors 0.88, 0.31, 1.07. Gold's idiosyncratic component is essentially redundant at this estimate.

The common state's stationary mean is 0.3967 and half-life 0.3834 years, about 96 business days. Mean short rate is 5.69%. Reported model-implied annual risk premiums are 9.58% index, −7.02% gold spot, 10.09% POM, and 33.02% NSM. These are structural implications, not sample return means. POM's implied total variance, about 0.6787 annually, is dramatically above its observed annualized standard deviation of 17.54% squared. The index likewise has model volatility around 17%, versus Table 1's observed 12.67%. Those differences should remain visible; they are not cured by the paper's qualitative claim that relative volatility rankings agree.

## Reprojection: learning and using the nonlinear filter

Fix the structural estimate and simulate 100,000 joint observations of log kernel $n_t$ and candidate observable series. Fit a semi-nonparametric (SNP) conditional density $f_K(n\mid x)$ using a regression component plus Gaussian-based Hermite-polynomial departures. A generic normalized positive implementation takes a squared polynomial multiplying a Gaussian density, divided by its integral. Polynomial coefficients depend on current and lagged observables. Exact fitted coefficients and the full model-search grid are not printed, so reconstructing the original numerical filter requires re-estimation.

The quantity of interest is

$$
\widetilde m_t=E[m_t\mid x_t]=\int e^n f_K(n\mid x_t)dn,
\qquad
\widetilde m_{2,t}=E[m_t^2\mid x_t]=\int e^{2n}f_K(n\mid x_t)dn.
$$

Use the **actual** observed $x_t$ when applying the fitted density. This is filtering today's kernel from today's prices, not forecasting tomorrow's kernel using yesterday's information. The conditional variance is $\widetilde m_{2,t}-\widetilde m_t^2$, not the square of the conditional mean or a time-series variance of filtered means.

Schwarz BIC selects the following SNP specifications in the paper's notation: index-only VR(1)-H(4,2,7); Treasury-only VR(1)-H(9,1,3); index-plus-Treasury VR(1)-H(4,1,1); index-plus-gold VR(1)-H(4,2,2). The three H arguments are polynomial degree in the kernel innovation, degree of polynomial coefficient dependence on conditioning variables, and conditioning-lag order. VR(1) has a contemporaneous regression component, not an autoregression on lagged latent kernels. The nonlinear density supplies the richer dynamics.

The four filtered kernels occupy very different ranges: approximately 1.004–1.010 for index only; 0.9260–0.9280 Treasury only; 0.9375–0.9395 index plus Treasury; and roughly 0.976–0.986 index plus gold. This lack of overlap is a warning about model/filter misspecification, not evidence of four distinct true SDFs identified from the same model.

A useful benchmark replaces the rich SNP density by Gaussian $n\mid x\sim N(a+bx,s^2)$ with $x=\log(1+r_M)$. Then $E[e^n\mid x]=e^{a+s^2/2}(1+r_M)^b\approx A+Ab r_M$. The linear index-kernel representation is a first-order approximation to this special nonlinear filter. Equation 25 prints $\sigma^3/2$ in one exponent but $\sigma^2/2$ immediately afterward; the Gaussian moment-generating formula requires half the variance. The first-order expansion has a generic $O(r_M^2)$ remainder, not necessarily the printed little-o remainder.

## Implied kernel and diagnostics

An alternative uses the affine bond price to recover $\widehat U_t$. Since the index has no idiosyncratic diffusion, discretized $U$ and index equations form a two-by-two system for Brownian innovations. For a simple daily step,

$$
\Delta\widehat W_2=\frac{\Delta U-(\theta-\kappa U)\Delta}{\sqrt U},
$$

$$
\Delta\widehat W_1=
\frac{\Delta L_0-[r_0+(\alpha_0-\beta_0^2/2)U]\Delta-\beta_0\rho\sqrt U\,\Delta\widehat W_2}
{\beta_0\sqrt{1-\rho^2}\sqrt U}.
$$

Insert these into the log-kernel increment. Dividend adjustments and nonsynchronous clocks need consistent treatment. In the correct model the innovations should be independent normal increments of variance $1/250$. In practice they absorb model errors. Figures 3–4 show heavy tails, heteroskedasticity, negative skew in the variance innovation, and slowly decaying serial correlation in that innovation. These are substantive failures of the assumed state dynamics. The implied kernel's higher variation is partly a consequence of using inverted state information and partly misspecification contamination.

HJ diagnostics use gross-return pricing errors $g=\mathbf1-E[mR]$. With $M=E[RR']$, the population squared HJ distance is $g'M^{-1}g$. The sample analogue has the same form; a factor $T$ produces a scaled criterion rather than the unscaled squared distance. Appendix C says that distance equals the minimand of an objective containing $T$, while Table 4 labels its entries HJ distances without clearly specifying a square-root or scale convention. Preserve the printed values for ranking; do not translate them into percentage pricing errors or claim exact replication of their normalization without resolving this ambiguity.

The volatility-bound test uses $E[m^2]\ge (E[m],\mathbf1')E[\widetilde R\widetilde R']^{-1}(E[m],\mathbf1')'$, where $\widetilde R=(1,R')'$. If the sample gap is negative, optimal-distance GMM projects the mean/second-moment pair to the boundary. Under its null the statistic has a half-point-mass-at-zero, half-$\chi_1^2$ distribution. Filter $m^2$ directly for this test. Squaring the filtered $m$ discards conditional variance and biases the second-moment input downward.

Table 4's printed HJ entries are:

| Sample/assets | Index | Treasury | Index + Treasury | Index + gold | Implied |
|---|---:|---:|---:|---:|---:|
| Estimation, 4 | 2.90 | 4.33 | 3.96 | 2.99 | 2.35 |
| Estimation, 8 | 8.94 | 9.50 | 9.34 | 8.97 | 8.81 |
| Evaluation, 4 | 2.82 | 3.03 | 2.97 | 2.83 | 2.55 |
| Evaluation, 8 | 3.63 | 3.79 | 3.74 | 3.63 | 3.41 |

The implied kernel is best by the numerical criterion; the index-only filter is best or tied among reprojections. Adding options sharply worsens the criterion, especially in sample. There is no supplied significance test for differences between these distances, because the structural parameters were estimated from a different moment objective.

For the index filter, optimal-distance statistics/p-values are 1.55/0.11 and 1.94/0.08 in sample for four/eight assets, and 1.15/0.14 and 1.10/0.15 out of sample. The implied kernel lies on or inside the bound in sample (0, p=0.50), but yields about 2.00/0.08 and 1.97/0.08 out of sample. Failure to reject a volatility bound is weaker than correctly pricing every asset. The author also warns that finite-sample bound tests can overreject.

## Appendix D, interpretation, and reproduction limits

Appendix D checks a bivariate index/Treasury submodel with approximate maximum likelihood. It inverts Treasury prices to $U$, uses the exact noncentral-chi-square CIR transition, and approximates the conditional log-index density. The reported estimates include $\theta=0.5158$, $\kappa=1.7466$, $r_0=0.0252$, $r_1=0.1566$, $\lambda_1=0.5580$, $\lambda_2=-0.9091$, $\rho=-0.4816$, and $\beta_0=0.5441$. Implied index volatility is about 29%, versus SMM's 17%; the paper reports no statistically significant parameter differences.

The printed D6–D7 conditional Gaussian approximation is incomplete for the displayed model: it lacks the log-price Itô correction and the conditioning contribution from the correlated $W_2$ shock. Conditional on a full variance path, a consistent derivation has mean

$$
L_t+r_0\Delta+(\alpha_0-\tfrac12\beta_0^2)I
+\beta_0\rho\,[U_{t+\Delta}-U_t-\theta\Delta+\kappa I],
$$

and variance $\beta_0^2(1-\rho^2)I$, where $I=\int_t^{t+\Delta}U_sds$. Approximating $I$ by endpoint trapezoidal integration gives an implementable correction, but it is not proof that this was the author's code. The Jacobian also needs its absolute value and consistent price-level/log-price coordinates. A reproduction should document these source discrepancies before trying to match the ML table exactly.

The economic interpretation is suggestive rather than identified. A filtered kernel above one is possible for an individual realization; persistently high filtered values may reflect misspecification or selection of the historical sample. Without consumption observations, the claimed exclusion of standard time-separable preferences is not a direct test of their marginal-utility equations. Habit formation can accommodate declining surplus consumption during rising aggregate consumption, but its parameters and habit process are not estimated here.

Finally, larger conditional SDF variance raises an upper bound on attainable Sharpe ratios. It does not demonstrate that a tradable high-Sharpe portfolio exists or that a contraction is a forecastable investment opportunity. The filter uses contemporaneous prices, and no transaction-cost-adjusted trading experiment is reported.

The reproducible core is the sequence: estimate a joint physical/risk-neutral model; simulate the latent log kernel with observables; estimate normalized conditional densities; integrate exponentials to filter first and second moments; and evaluate on both held-out time periods and new payoff types. Exact numerical replication still requires the original data and contract-selection decisions, SNP coefficients/search details, simulator boundary and clock conventions, and clarification of the printed derivative and diagnostic formulas. These limitations do not erase the methodological contribution, but they prevent treating the reported filter as a fully specified executable model supplied by the PDF alone.

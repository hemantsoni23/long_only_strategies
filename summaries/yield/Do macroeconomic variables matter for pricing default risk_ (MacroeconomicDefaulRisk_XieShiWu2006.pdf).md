# Do macroeconomic variables matter for pricing default risk?

Yan Alice Xie, Jian Shi, and Chunchi Wu. *International Review of Economics and Finance*, article-in-press version accepted August 11, 2006, DOI 10.1016/j.iref.2006.08.006. [Source PDF](../../Finance/MacroeconomicDefaulRisk_XieShiWu2006.pdf). This local version has 13 pages and placeholder volume and pagination, so the bibliographic date here follows that version. All pages, including Appendices A and B and the references, were read; equations, Figure 1, and Tables 1–5 were also inspected visually. Source page references below mean PDF pages.

## Why this matters

A credit model can fit most yield variation while systematically missing the same economic shock across ratings and maturities. That matters for valuation and portfolio risk: residuals that look small bond by bond can become a large common exposure when aggregated. This paper diagnoses such a failure in a three-factor affine model comprising two Treasury factors and a rating-specific credit factor.

The contribution is empirical diagnosis rather than a new default-pricing formula. The authors estimate rating-specific spot curves, fit a version of Duffee's reduced-form model using a Kalman filter, examine residual principal components, and regress the residuals on aggregate variables. The main finding is strong common residual variation and a consistently negative association with contemporaneous S&P 500 returns. Lagged equity returns are also negative but less uniformly significant. Inflation and industrial-production growth add little in the reported specification.

The paper interprets this pattern as evidence that the model misses business-cycle variation in risk aversion. The evidence more directly establishes a conditional association and model misspecification. It does not separately identify changes in expected default losses, liquidity, risk prices, or the state of investor preferences. A useful implementation must preserve that distinction and address several ambiguities in the printed formulas before treating the article as executable documentation.

## Sample, measurement, and information timing

The estimation period is January 1988 through December 1996: 108 calendar months before any losses associated with lag construction. The source is the Lehman Brothers Fixed Income Database distributed by Warga. Corporate observations are industrial bonds rated AA, A, or BBB, with maturities from two through ten years. The rating is the rating on the observation date, not permanently the rating at issuance. Thus the curve represents a changing rating-class portfolio; it is not the longitudinal credit process of one fixed issuer.

The authors remove matrix-priced bonds, embedded options including calls, puts and sinking funds, floating rates, irregular coupon-payment frequencies, bonds outside the Lehman Brothers indexes, problematic returns, and observations whose pricing error against the estimated spot curve exceeds a stated \$5 filter. The article does not provide the par-value convention for that dollar filter, an exact iterative filtering procedure, or retained bond counts by month and rating. Treasury exclusions similarly remove special provisions, variable rates, irregular coupon frequencies and flower bonds.

Because zero-coupon corporate issues are scarce, monthly spot yields are extracted from coupon bonds using Nelson–Siegel curves. The paper does not print that curve's formula or fitting objective. A conventional reconstruction would use a continuously compounded yield curve

$$
y_t(\tau)=a_t+b_t\frac{1-e^{-\tau/\ell_t}}{\tau/\ell_t}
+c_t\left(\frac{1-e^{-\tau/\ell_t}}{\tau/\ell_t}-e^{-\tau/\ell_t}\right),
$$

and price each coupon cash flow using $\exp[-\tau y_t(\tau)]$. This is a reconstruction of the named method, not a disclosed original implementation: whether the fit minimizes price or yield errors, its weights, the treatment of accrued interest, the day count, and the handling of $\ell_t$ are missing. Those choices can affect cross-maturity residual correlation.

The Treasury measurement vector has 13 maturities: one through ten years, then 15, 20, and 30 years. Each corporate rating has nine maturities, two through ten years. Figure 1 averages monthly corporate-minus-Treasury spot spreads at matched maturity. All three curves slope upward and flatten at longer maturities. Visually, AA spreads rise from roughly 45 to 58 basis points, A from approximately 65 to 80, and BBB from around 75 to 118; these are figure readings, not a tabulated data series.

The macroeconomic variables are monthly log differences of the S&P 500 closing price, seasonally adjusted CPI, and seasonally adjusted industrial-production index, obtained from the Federal Reserve Bank of St. Louis. The stock measure is therefore a price-index return as described, not explicitly a dividend-reinvested total return. The regression includes current-month and one-month-lagged stock returns. Current-month information is explanatory information, not a predictor known before that month's yield was observed. The source does not specify historical data vintages, release lags, or revisions to the macro series.

## State processes and what is identified

Let $s_{1t},s_{2t}$ be independent square-root interest-rate factors and let $r_t$ be the nominal short rate. Under the physical measure $P$,

$$
r_t=\alpha_r+s_{1t}+s_{2t},\qquad
ds_{jt}=\kappa_j(\theta_j-s_{jt})\,dt+\sigma_j\sqrt{s_{jt}}\,dW^P_{jt}.
$$

Under the pricing measure $Q$, the same diffusion has drift

$$
ds_{jt}=[\kappa_j\theta_j-(\kappa_j+\mu_j)s_{jt}]\,dt
+\sigma_j\sqrt{s_{jt}}\,dW^Q_{jt}.
$$

Here $\kappa_j$ is physical mean reversion, $\theta_j$ the physical long-run mean, $\sigma_j$ the diffusion parameter, and $\mu_j$ the parameter changing the drift under $Q$. The rate of mean reversion under $Q$ is $\kappa_j+\mu_j$, not $\kappa_j$. The first factor is interpreted as a slope factor and the second as a long-rate-level factor; these are economic interpretations of latent factors, not direct observations.

For rating $i$, write $x_{it}=\lambda^*_{it}$ for the additional square-root factor, independent of both Treasury Brownian motions. Its physical and pricing drifts have the same respective forms with parameters $\kappa_i,\theta_i,\mu_i,\sigma_i$. The translated intensity is

$$
\lambda_{it}=\frac{\alpha_i+x_{it}
+\beta_{1i}(s_{1t}-\bar s_1)
+\beta_{2i}(s_{2t}-\bar s_2)}{1-\delta_i}.
$$

The bars denote factor means. The implementation must specify whether these are fitted stationary means or full-sample state averages; the notation in the source does not resolve that choice. They are treated as constants in the affine pricing reconstruction. If allowed to vary unpredictably over the remaining life of a bond, they would require additional dynamics.

The stated bond price is

$$
P_i(t,T)=E_t^Q\left[\exp\left\{-\int_t^T[r_u+(1-\delta_i)\lambda_{iu}]\,du\right\}\right].
$$

This effective discount-rate representation is consistent with fractional recovery of market value under its usual assumptions. It is not the general cash-flow formula for arbitrary recovery of par. Substitution shows that $\delta_i$ cancels: the fitted yield model identifies the loss-adjusted intensity term, not default intensity and recovery separately. Moreover, $\alpha_i$ intentionally includes liquidity and tax effects, making it especially inappropriate to read all fitted spread as an expected default loss.

A related derivative qualification concerns the source's interpretation of $\beta_{ji}$. Precisely, a unit increase in $s_j$ changes $(1-\delta_i)\lambda_i$ by $\beta_{ji}$ and changes $\lambda_i$ by $\beta_{ji}/(1-\delta_i)$. The text's direct default-intensity interpretation suppresses this recovery factor. No numerical recovery calibration is supplied here to restore it.

The square-root factors are nonnegative for admissible CIR parameters. That does not ensure the translated intensity is globally nonnegative. Negative $\beta$ coefficients and unbounded positive Treasury-factor support can make its numerator negative. The paper does not report a positivity restriction, truncation rule, or frequency of negative fitted intensities. Adding a truncation would alter the exact affine pricing formula. This is a model-domain limitation to resolve in a replication, not evidence that the reported historical filtered paths actually became negative.

## A consistent affine pricing implementation

It is convenient to define one transform that handles both Treasury and corporate factor loadings. For a factor with $Q$ dynamics $dX=(a-bX)dt+\sigma\sqrt X\,dW$, let

$$
E_x^Q\left[e^{-q\int_0^\tau X_u\,du}\right]
=\mathcal A_q(\tau)e^{-\mathcal B_q(\tau)x},
\quad a=\kappa\theta,\quad b=\kappa+\mu.
$$

With $g_q=\sqrt{b^2+2\sigma^2q}$, define

$$
D_q(\tau)=2g_qe^{-g_q\tau}+(b+g_q)(1-e^{-g_q\tau}),
$$

$$
\mathcal B_q(\tau)=\frac{2q(1-e^{-g_q\tau})}{D_q(\tau)},\qquad
\mathcal A_q(\tau)=
\left[\frac{2g_qe^{(b-g_q)\tau/2}}{D_q(\tau)}\right]^{2\kappa\theta/\sigma^2}.
$$

These functions solve $\mathcal B'_q=q-b\mathcal B_q-\sigma^2\mathcal B_q^2/2$ and $(\log\mathcal A_q)'=-\kappa\theta\mathcal B_q$, with initial values zero for $\mathcal B_q$ and one for $\mathcal A_q$. Evaluation should use stable exponential differences near $\tau=0$ and logarithms for $\mathcal A$.

The Treasury formula is

$$
P_F(t,T)=e^{-\alpha_r\tau}
\prod_{j=1}^2\mathcal A_{j,1}(\tau)
\exp\left[-\sum_{j=1}^2\mathcal B_{j,1}(\tau)s_{jt}\right].
$$

For corporate bonds, set $q_{ji}=1+\beta_{ji}$ and $c_i=\alpha_r+\alpha_i-\sum_j\beta_{ji}\bar s_j$. Then

$$
P_i(t,T)=e^{-c_i\tau}\mathcal A_{i,1}(\tau)
\prod_{j=1}^2\mathcal A_{j,q_{ji}}(\tau)
\exp\left[-\mathcal B_{i,1}(\tau)x_{it}
-\sum_{j=1}^2\mathcal B_{j,q_{ji}}(\tau)s_{jt}\right].
$$

This weighted-factor representation makes the dependence coefficients explicit. Appendix A instead rescales $s_j^*=(1+\beta_{ji})s_j$, with correspondingly rescaled means and volatilities; that is equivalent when the scaling is positive, as in the reported estimates. Reusing unmodified Treasury coefficients while simply adding a credit factor would omit the very interest-credit dependence being tested.

There is a visually verified sign discrepancy in Eq. (7) on p. 4 and Eq. (A.11) on p. 12: both print $e^{+A(T-t)}$, although Eq. (A.10) defines $A$ as the positive constant contribution to the discount rate. The expectation in Eqs. (4) and (A.7) requires $e^{-A(T-t)}$. In a constant-only illustration with $A=0.03$ and five years, discounting gives 0.860708; the printed positive sign gives 1.161834. This is an algebraic correction made in this note, not an official erratum or proof of what the authors' estimation code used.

An independent numerical check of the reconstructed transform used $\kappa=.55,\theta=.006,\mu=-.08,\sigma=.10,q=.90,\tau=5$. The closed form gives $\mathcal B=1.71148435211589$ and $\log\mathcal A=-0.0192994793795778$. Fourth-order Runge–Kutta integration of the two Riccati equations with 20,000 steps agrees to about $4\times10^{-15}$ for $\mathcal B$. This checks the reconstruction; it is not a replication of the empirical estimates.

## Estimation with a conditionally Gaussian filter

For maturity $\tau$, the model spot yield is $-\log P(t,t+\tau)/\tau$. Thus the measurement intercept and factor loadings are the negative logarithm of the price prefactor divided by $\tau$, and the $\mathcal B$ coefficients divided by $\tau$. The source's statement that measurement $A,B$ are simply the price coefficients of Appendix A should not be implemented literally: the logarithm and maturity division are essential.

With monthly interval $\Delta=1/12$, the exact physical CIR conditional moments are

$$
E[X_t\mid X_{t-1}]=\theta(1-e^{-\kappa\Delta})+e^{-\kappa\Delta}X_{t-1},
$$

$$
\operatorname{Var}(X_t\mid X_{t-1})=
\frac{\sigma^2}{\kappa}\left[
X_{t-1}(e^{-\kappa\Delta}-e^{-2\kappa\Delta})
+\frac\theta2(1-e^{-\kappa\Delta})^2\right].
$$

The Treasury transition matrix is diagonal with entries $e^{-\kappa_j/12}$ and intercepts $\theta_j(1-e^{-\kappa_j/12})$. Measurement errors have diagonal covariance $H$ across the 13 Treasury maturities, with separately denoted variance parameters. The corporate step similarly uses one credit factor and a diagonal measurement covariance across nine maturities; the text denotes its entries by a common rating-specific variance $\Sigma_i$.

The procedure first estimates the Treasury model, then plugs the estimated Treasury states into each rating's credit model. For a concrete reconstruction, predict the state and covariance using the transition moments, form the yield innovation $v_t=Y_t-a_t-B_t\widehat X_{t|t-1}$ and innovation covariance $F_t=B_tP_{t|t-1}B_t'+H$, update with gain $K_t=P_{t|t-1}B_t'F_t^{-1}$, and maximize the Gaussian innovation criterion

$$
\ell=-\frac12\sum_t\left[n_t\log(2\pi)+\log|F_t|+v_t'F_t^{-1}v_t\right].
$$

This is a quasi-likelihood approximation because CIR transitions are not Gaussian. Matching the conditional moments does not make the Kalman filter the exact nonlinear conditional filter. Gaussian updates can also produce negative state estimates unless constrained or otherwise handled. The source does not state initialization, parameter constraints, optimizer settings, state-positivity treatment, or the exact handling of state uncertainty inside the conditional variance. These are necessary replication inputs.

Appendix B gives a White sandwich construction using numerical central differences for scores and Hessians. For per-observation scores $g_t$ and average negative Hessian $H_\ell$, a consistent notation is $\widehat{\operatorname{Var}}(\widehat\psi)=H_\ell^{-1}(n^{-1}\sum_tg_tg_t')H_\ell^{-1}/n$, under the corresponding assumptions. Standard errors are square roots of diagonal variances. The source says they are the diagonals of the displayed covariance of $\sqrt n(\widehat\psi-\psi)$; that statement omits square roots and the sample-size scaling needed for estimates themselves. The printed finite-difference formulas are ordinary central differences, but step sizes are unspecified. There is no stated joint correction for uncertainty from Nelson–Siegel fitting and first-stage Treasury estimation, nor a time-series HAC construction for these parameter standard errors.

## Estimated parameters and model fit

Table 1 reports the following Treasury estimates with standard errors in parentheses:

| Factor | $\kappa$ | $\theta$ | $\mu$ | $\sigma$ |
|---|---:|---:|---:|---:|
| 1 | .535 (.034) | 1.166 (.044) | −.013 (.001) | .013 (.001) |
| 2 | .047 (.002) | .065 (.009) | −.020 (.001) | .049 (.002) |

The printed constant is $\alpha_r=1.150$ with standard error .0483. Table 1 does not label yield/factor rescaling or print a minus sign on this constant. Those values should be preserved as reported rather than silently converted into an assumed decimal-rate calibration. Without the original data convention and state series, their absolute rate levels cannot be safely reconstructed. Physical half-lives $\log 2/\kappa$ do not depend on that unit ambiguity: they are approximately 1.296 and 14.748 years, matching the narrative's 1.3 and 15 years.

Table 2 explicitly scales the constant and long-run credit mean by 100:

| Rating | $100\alpha_i$ | $\kappa_i$ | $100\theta_i$ | $\mu_i$ | $\sigma_i$ | $\beta_{1i}$ | $\beta_{2i}$ |
|---|---:|---:|---:|---:|---:|---:|---:|
| AA | .730 | .559 | .120 | −.076 | .155 | −.035 | −.014 |
| A | .870 | .562 | .580 | −.311 | .082 | −.101 | −.037 |
| BBB | 1.150 | .614 | .760 | −.246 | .071 | −.137 | −.005 |

The credit-factor half-lives are 1.240, 1.233 and 1.129 years. All reported parameter estimates are described as significant at 1%; the source's very small standard errors on several credit-process parameters should be interpreted with the estimation qualifications above. The larger constants for lower ratings are consistent with higher nondefault spread components, but no separate liquidity and tax measurements identify that decomposition. Negative $\mu_i$ raises the pricing-measure mean relative to the physical mean when other parameters are fixed, consistent with compensation for credit-factor risk.

Negative $\beta_{1i}$ shows the estimated inverse interest-credit relation becoming stronger for poorer ratings. The second loading is smaller in magnitude, particularly for BBB. The article reports adjusted $R^2$ from regressing observed spot yields on fitted spot yields, not a likelihood-based fit measure or a direct out-of-sample pricing error. Across the 27 rating-maturity series the values range from .7100 to .8347. AA's two-year value is .7125, A's four-year value .8152, and BBB's three-year value .8347; ten-year values are .7733, .7551, and .7100 respectively. Such regressions can fit the broad time-series level while retaining systematic yield discrepancies.

## Residual principal components

Define the residual in yield units as $R^i_{m,t}=y^{\mathrm{observed},i}_{m,t}-y^{\mathrm{model},i}_{m,t}$. A positive residual means the model understates the yield. The PCA uses standardized residuals, hence correlation matrices, rather than covariance matrices in original yield units.

For each maturity, form the $3\times3$ correlation matrix across AA, A and BBB residual series. Its trace is three, so a principal component with eigenvalue $e$ explains $e/3$ of standardized variation. Table 3's two-year first eigenvalue is 2.859, accounting for 95.30%; the second is .126, giving 99.50% cumulatively. At ten years the corresponding values are 2.881 and .109, with reported shares 96.02% and 99.67%. Across maturities the first component explains roughly 90–96%, and two explain about 99% or more.

Two printed statements require care. The p. 8 text says an uncorrelated correlation matrix has an eigenvalue zero. In fact the identity matrix has all eigenvalues one. At perfect positive correlation the eigenvalues are three, zero, zero. Also, Table 3's five-year row prints first eigenvalue 2.720 with 90.06%, and second .271 with cumulative 99.08%. Arithmetic from those eigenvalues gives 90.667% and 99.700%. This visually verified inconsistency cannot establish which original estimates were intended; the qualitative commonality conclusion survives either set of percentages.

For each rating, a separate $9\times9$ correlation matrix spans maturities two through ten years. Table 4 reports:

| Rating | First eigenvalue | First share | Second eigenvalue | First two cumulative share |
|---|---:|---:|---:|---:|
| AA | 7.563 | 84.04% | 1.342 | 98.95% |
| A | 7.489 | 83.21% | 1.494 | 99.82% |
| BBB | 7.612 | 84.57% | 1.374 | 99.84% |

The remaining components are very small. The result establishes low-dimensional structure in fitted-curve residuals. It does not alone prove that the omitted variables are macroeconomic: common curve-extraction errors, restrictions shared across maturities, liquidity shocks and state-estimation errors can also generate commonality. Nelson–Siegel smoothing itself imposes a low-dimensional representation before this diagnostic is run. The article does not provide a null simulation separating mechanical smoothing from economic omitted factors.

## Aggregate-variable regressions and actual magnitudes

For each rating and maturity the empirical regression is

$$
R^i_{m,t}=a^i_m+b^i_{1m}\Delta\log\mathrm{CPI}_t
+b^i_{2m}\Delta\log\mathrm{IPI}_t
+b^i_{3m}\Delta\log\mathrm{SP}_t
+b^i_{4m}\Delta\log\mathrm{SP}_{t-1}+u^i_{m,t}.
$$

The note writes constant coefficients within each estimated series; the time subscripts on coefficients in printed Eq. (14) are not accompanied by any time-varying-parameter law. To account for serially correlated errors the authors use iterated Yule–Walker estimation. Table 5 reports autoregressive order two for all AA maturities; order two for A through seven years and three for eight through ten; and order two for BBB through six years and three for seven through ten. The rule selecting the order is not supplied.

Selected estimates, with contemporaneous and lagged stock-return $t$ statistics, show the size and heterogeneity of the result:

| Rating/maturity | Current stock coefficient ($t$) | Lagged stock coefficient ($t$) | Adjusted $R^2$ | Adjusted DW |
|---|---:|---:|---:|---:|
| AA, 2 years | −.0405 (−4.58) | −.0201 (−2.23) | .18 | 1.96 |
| AA, 5 years | −.0365 (−6.32) | −.0119 (−2.02) | .33 | 1.87 |
| AA, 10 years | −.0358 (−5.82) | −.0096 (−1.54) | .30 | 1.78 |
| A, 2 years | −.03055 (−4.24) | −.0062 (−.85) | .21 | 1.89 |
| A, 5 years | −.0340 (−5.92) | −.0114 (−1.96) | .30 | 1.85 |
| A, 10 years | −.0359 (−5.74) | −.0142 (−2.23) | .29 | 1.77 |
| BBB, 2 years | −.0273 (−2.95) | −.0190 (−2.01) | .09 | 1.92 |
| BBB, 5 years | −.0365 (−6.16) | −.0111 (−1.86) | .33 | 1.80 |
| BBB, 10 years | −.0400 (−6.15) | −.0099 (−1.50) | .33 | 1.75 |

All contemporaneous stock coefficients are negative and reported significant at 1%. Lagged coefficients are negative throughout, but significance varies: AA's long maturities and BBB's seven- through ten-year lags are not significant even at 10%, while A's longer-maturity lags are significant at 5%. CPI and industrial-production coefficients are insignificant across the reported rows. The full-model adjusted $R^2$ ranges from .09 to .35, so describing every regression as explaining 30% would obscure the weak BBB two-year fit. Moreover, these are full four-regressor results, not a separately reported incremental $R^2$ for the two stock terms alone.

The coefficient units require the same care as the underlying yield units. If both residual yields and log returns are in decimal units, the AA five-year coefficient implies that a one-percentage-point current stock return is associated with $-.0365\times.01=-.000365$ in yield, or −3.65 basis points, holding other regressors fixed. This is an explicitly conditional unit conversion, not a confirmed original-data scaling. It must not be quoted as an unqualified causal effect.

Footnote 8 describes additional regressors—house sales, retail sales, unemployment, consumer credit, purchasing managers' index, money supply and capacity utilization—as insignificant while the stock-return terms remain significant. Their detailed coefficients, sample changes and test statistics are not supplied. This supports the authors' stated robustness claim only at the level documented; it is not an independently reproducible battery of tests.

## Interpretation, remaining inputs, and limits

A negative stock coefficient means falling stock markets coincide with higher observed-minus-fitted yields. That does not, by itself, demonstrate that absolute pricing error or squared-error goodness of fit worsens in every downturn: the level of the intercept and the starting residual matter. The paper's language about deterioration in bad states is an economic interpretation of the sign, not a reported comparison of downturn and expansion RMSE.

Likewise, pricing under an equivalent martingale measure does not assume investors are literally risk neutral, nor does it preclude time-varying risk aversion. The restrictions lie in the selected state variables and risk-price specification. A richer affine or nonaffine pricing model could encode aggregate risk prices while still using risk-neutral valuation. The study does not estimate such an augmented structural model or compare its out-of-sample pricing performance.

A replication can follow the sequence of filtered bond selection, four monthly spot-curve fits, Treasury quasi-likelihood estimation, three conditional credit fits, residual construction, correlation-matrix PCA, and 27 serial-correlation-adjusted macro regressions. It still needs original bond identifiers and prices, coupon conventions, yield scales, curve-fit weights, filtering iteration, optimizer constraints and initialization, the mean-centering convention, fitted states, measurement-error estimates, parameter covariance details, macro vintages, lag-order selection and effective regression sample sizes. The article supplies no code or data files with this local PDF.

No trading rule, rolling calibration window, held-out evaluation, transaction costs, shorting constraints or realized portfolio returns are reported. Its useful result is a specification diagnostic for a historically fitted credit-curve model. The documented commonality motivates adding and testing economically interpretable aggregate states; it does not establish a profitable credit-equity signal or identify one unique source of the omitted risk premium.

# Expectation Puzzles, Time-varying Risk Premia, and Affine Models of the Term Structure

Qiang Dai and Kenneth J. Singleton. Working paper, April 30, 2001 version; first version June 7, 2000. Source: [AffineTermStructure_DaiSingleton_2001.pdf](../../Finance/AffineTermStructure_DaiSingleton_2001.pdf). All 27 PDF pages, including Appendices A–C and references, were read. Page numbers below are both PDF and printed page numbers. This is the supplied working-paper version, not an assertion about a later published version.

## Why this matters

A term-structure model can price the observed yield curve closely yet imply the wrong population predictability of bond returns. Dai and Singleton make this distinction operational. They ask whether affine models can explain the familiar negative Campbell–Shiller regression coefficients and whether their estimated risk premiums remove those coefficients' apparent contradiction with the expectations hypothesis. These are separate tests: one concerns the model's unconditional dynamics; the other combines observed yield changes with model-implied premium adjustments.

The main finding is that Gaussian affine models with state-dependent prices of risk and correlated factors can reproduce both sets of restrictions. Canonical square-root models cannot. A model with one volatility factor can improve when restrictions prevent the likelihood from buying a better volatility fit at the expense of the conditional mean. Thus a stochastic-volatility specification with a slightly better likelihood need not be a better expected-return model.

This is useful for a rates investor because the decomposition of a forward rate into an expected future short rate and a premium directly affects duration forecasts. It is also useful for model validation: fitting a cross-section, matching regressions on fitted historical yields, and generating the correct population forecasting relationships are three different accomplishments. The paper establishes an in-sample specification result, not an out-of-sample trading strategy or a uniquely identified economic mechanism.

## What is new, and what is inherited

The rejection of constant-premium expectations hypotheses is inherited from Fama, Fama–Bliss, Campbell–Shiller, and related work. Affine bond pricing and the classification of models by the number of stochastic-volatility factors are inherited from Duffie–Kan and Dai–Singleton. The richer price-of-risk parameterization follows Duffee's contemporary work. The contribution here is to join those ingredients in a demanding comparison of model-implied population projections and premium-adjusted historical projections, estimate the models by likelihood rather than targeting only those regressions, and diagnose which restrictions obstruct the match.

The paper also gives a general decomposition of excess returns into a premium component and revisions to expected short rates. It shows why an average forward premium equals an average excess holding return under stationarity. The Gaussian appendix supplies the conditional moments and affine premium formulas needed to make the exercise reproducible. The monetary-policy and habit-formation interpretations in the conclusion are proposed economic rationalizations, not separately estimated or tested structural explanations.

## The projection being explained

Let $P_t^n$ denote the time-$t$ price of an $n$-period zero-coupon bond and define its continuously compounded yield in units of one period by $R_t^n=-\log P_t^n/n$. The one-period yield is $r_t=R_t^1$. An investor buys the $n$-period bond and sells it one period later with $n-1$ periods remaining. Its realized excess log return is

$$
D_{t+1}^n=\log(P_{t+1}^{n-1}/P_t^n)-r_t
=-(n-1)(R_{t+1}^{n-1}-R_t^n)+(R_t^n-r_t).
$$

Writing $e_t^n=E_t[D_{t+1}^n]$ and $x_t^n=(R_t^n-r_t)/(n-1)$ gives

$$
E_t[R_{t+1}^{n-1}-R_t^n]=x_t^n-\frac{e_t^n}{n-1}.
$$

The Campbell–Shiller projection regresses the realized yield change on an intercept and $x_t^n$. A constant expected excess log return implies a slope of one. A negative slope instead means that expected excess returns covary sufficiently positively with the yield spread to reverse the constant-premium prediction. In particular, direct covariance algebra gives

$$
\phi_n=1-\frac{\operatorname{Cov}(e_t^n,R_t^n-r_t)}{\operatorname{Var}(R_t^n-r_t)}.
$$

This last expression is a derived restatement of equations (1), (2), and (17), under the usual orthogonality of the forecast error to time-$t$ information. A negative coefficient does not mechanically identify irrational expectations: it can arise from a time-varying premium larger, in this covariance sense, than the expectations component.

Table 1 reports the following sample evidence. Maturity is in months; coefficients and their standard errors are dimensionless.

| Maturity | 3 | 6 | 9 | 12 | 24 | 36 | 48 | 60 | 84 | 120 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Slope | −0.428 | −0.883 | −1.228 | −1.425 | −1.705 | −1.190 | −2.147 | −2.433 | −3.096 | −4.173 |
| Standard error | 0.481 | 0.640 | 0.738 | 0.825 | 1.120 | 1.295 | 1.418 | 1.519 | 1.705 | 1.985 |

The broad maturity pattern is downward, but it is not literally monotone: the 36-month estimate is less negative than the 24-month estimate. Uncertainty is considerable at the long end. The target is the joint shape and magnitude, not a claim that every individual coefficient differs significantly from zero.

## Premium decomposition and the second test

Define the yield premium and the one-period forward premium by

$$
c_t^n=R_t^n-\frac1n\sum_{i=0}^{n-1}E_t[r_{t+i}],
\qquad
p_t^n=f_t^n-E_t[r_{t+n}],
\qquad
f_t^n=-\log(P_t^{n+1}/P_t^n).
$$

Because a zero-coupon yield is an average of successive forward rates, $c_t^n=n^{-1}\sum_{i=0}^{n-1}p_t^i$. These premiums include the implications of using log yields and physical conditional expectations; they should not be confused with an instantaneous Sharpe ratio or a simple expected arithmetic return.

Equations (6)–(8) decompose the excess return as

$$
D_{t+1}^n=D_{t+1}^{*n}+\sum_{i=1}^{n-1}(E_t[r_{t+i}]-E_{t+1}[r_{t+i}]),
$$

$$
D_{t+1}^{*n}=-(n-1)(c_{t+1}^{n-1}-c_t^{n-1})+p_t^{n-1}.
$$

The second term in the first equation has zero conditional expectation. Consequently, $e_t^n=E_t[D_{t+1}^{*n}]$. Under the paper's stationarity and finite-moment assumptions,

$$
E[e_t^n]=E[p_t^{n-1}]=E[f_t^{n-1}-r_t].
$$

Equality of average forward spreads and average excess holding returns is therefore an identity under these assumptions, not an additional empirical success for a particular premium theory. In finite samples their means need not coincide exactly.

The adjusted yield change is

$$
z_{t+1}^n=R_{t+1}^{n-1}-R_t^n-(c_{t+1}^{n-1}-c_t^{n-1})+\frac{p_t^{n-1}}{n-1}.
$$

For a correctly specified model, $E_t[z_{t+1}^n]=x_t^n$, so its projection on $x_t^n$ has coefficient one. The authors call the two requirements LPY(i) and LPY(ii): match the negative population slopes for unadjusted changes, and restore slopes of one after adding estimated premiums to historical yield changes.

The distinction is crucial. Computing the adjusted projection wholly inside any internally consistent model produces one by construction. That is not a test. LPY(ii) instead uses actual historical yields and premiums evaluated at the estimated historical states. Conversely, LPY(i) uses model population moments, not regressions on the fitted time series. This avoids letting actual historical state movements substitute for the model's own transition law.

## Affine dynamics and admissible risk compensation

The physical state process is

$$
dY_t=\kappa(\theta-Y_t)\,dt+\Sigma\sqrt{S_t}\,dW_t,
\qquad
(S_t)_{ii}=\alpha_i+\beta_i'Y_t,
$$

with short rate $r(t)=a_0+b_0'Y_t$. A model in $A_m(N)$ has $N$ state variables and $m$ state variables driving conditional variances. Its state space and drift restrictions must keep the variances nonnegative and ensure a well-defined diffusion. Under the pricing measure the drift is reduced by $\Sigma\sqrt{S_t}\Lambda_t$.

The conventional specification is $\Lambda_t=\sqrt{S_t}\ell_0$. It ties compensation for risk to the same state dependence as volatility. The extension is

$$
\Lambda_t=\sqrt{S_t}\lambda_0+\sqrt{S_t^-}\lambda^Y Y_t,
$$

where $S_t^-$ has zero entries for the square-root volatility coordinates and inverse variance entries for eligible remaining coordinates whose variance is bounded strictly away from zero. The added term supplies state-dependent compensation without requiring matching changes in conditional volatility. It is constrained by admissibility; it is not permissible to insert arbitrary inverse square-root exposures at attainable zero-volatility boundaries.

If $P_t(\tau)=\exp[-A(\tau)-B(\tau)'Y_t]$, instantaneous expected excess bond return is

$$
\mu^e(t,\tau)=-B(\tau)'\Sigma\sqrt{S_t}\Lambda_t.
$$

For Gaussian models, volatility is constant but the extension permits changing expected returns. For a full square-root $A_N(N)$ model, the extension is unavailable in the specification considered. Hybrid models occupy the middle ground. Increasing volatility flexibility therefore reduces available premium flexibility within this family; it is not a free enlargement of every economically relevant dimension.

The canonical empirical short rate is $r(t)=\delta_0+Y_{1t}+Y_{2t}+Y_{3t}$. $\Sigma$ is diagonal. Square-root factors are mutually independent in the estimated implementation, though the authors acknowledge that richer admissible drift dependence exists outside their likelihood implementation. The drift is block restricted and long-run means of non-volatility coordinates are normalized. Factor correlations can still arise through drift feedback. Gaussian models permit the richest such structure. Numerical risk-price coefficients depend on these normalizations, so their magnitudes cannot be compared with a different state scaling as if they were invariant economic prices.

## Gaussian implementation and a useful population calculation

Appendix A uses a slightly different parameterization: $dY_t=\kappa(\theta-Y_t)dt+\sigma dW_t$ and $\Lambda_t=\sigma^{-1}(\lambda_0+\lambda^Y Y_t)$. Then

$$
\widetilde\kappa=\kappa+\lambda^Y,
\qquad
\widetilde\theta=\widetilde\kappa^{-1}(\kappa\theta-\lambda_0).
$$

Here $\lambda_0$ and $\lambda^Y$ are drift-adjustment coefficients, not numerically the same convention as equation (15). Under the physical measure,

$$
E_t[Y_{t+h}]=\theta+e^{-\kappa h}(Y_t-\theta),
\qquad
\operatorname{Var}_t(Y_{t+h})=\int_0^h e^{-\kappa u}\sigma\sigma'e^{-\kappa'u}\,du.
$$

The integral form avoids the need for the real diagonalization assumed in the appendix and handles repeated eigenvalues continuously. Stationarity requires eigenvalues of $\kappa$ with positive real parts. The stationary covariance $V$ solves $\kappa V+V\kappa'=\sigma\sigma'$.

Yield loadings are $b(\tau)=\tau^{-1}\int_0^\tau e^{-\widetilde\kappa'u}b_0\,du$. The intercept incorporates the risk-neutral long-run mean and the Gaussian convexity adjustment. Forward and yield premiums are affine because both market yields and physical short-rate forecasts are affine in the same state. Equations (38)–(43) make the forward premium's coefficients explicit.

For replication, let $R_t^n=a_n+b_n'Y_t$, $h$ be one observation period, and $g_n=(b_n-b_1)/(n-1)$. A derived population formula is

$$
\phi_n=\frac{(b_{n-1}'e^{-\kappa h}-b_n')Vg_n}{g_n'Vg_n}.
$$

It follows by writing the future state as its conditional mean plus an innovation orthogonal to $Y_t$. This is the population object the paper needs. Estimating the same regression on states extracted from historical yields generally uses the historical covariance and persistence, which need not equal $V$ and $e^{-\kappa h}$. The latter exercise can look successful even when the former fails.

## Estimation design and missing implementation inputs

Section 4 reports 312 monthly observations of Treasury zero-coupon yields during 1970–1995. The fitted maturities are six months and two, three, five, seven, and ten years. Six-month, two-year, and ten-year yields are treated as exact, allowing inversion for three factors. The other yields have independent normal measurement errors with zero means. Serially independent pricing errors force the state dynamics to explain predictive information rather than burying it in persistent residuals.

The exact-yield assumption is economically strong. Curve construction and interpolation errors can be systematic, and an exact maturity becomes an anchor for the factor history. A replication should store observed and fitted yields separately and compare the results with alternative anchors or a measurement-error filter. Those are proposed robustness checks, not results reported in the paper.

Gaussian and independent square-root models use their known transition densities, respectively Gaussian and noncentral chi-square. Hybrid models use an approximation to the conditional density following Duffie, Pedersen, and Singleton. Standard errors use outer products of likelihood scores; the authors say Hessian-based errors are mostly comparable. The Gaussian model is pruned by setting six weakly identified parameters to zero with essentially no likelihood loss.

The source does not give complete numerical optimization tolerances, initializations, the code for the approximate density, or the full measurement-error variance estimates. It also contains a date discrepancy: the data footnote says February 1970–December 1995, which is 311 months, while the estimation section says 312 observations over 1970–1995. The post-1983 discussion says January 1983–December 1995 and 156 observations, whereas the figure caption says February 1983. The underlying date index must resolve these differences; silently choosing one version would not be exact replication.

All maturity and yield units must be harmonized. The initial algebra uses period yields, while the continuous-time appendix introduces an explicit interval $\Delta$. A monthly implementation using annualized yields needs $\Delta=1/12$ in transition matrices and return conversions. The printed appendix sometimes suppresses this interval. That is a notation shortcut only if the time coordinate is rescaled consistently.

## What the estimates show

Table 2 gives likelihood values of 33.43, 33.54, 33.54, and 33.14 for $A_{0C}(3)$ through $A_{3C}(3)$. The displayed values are not enough to reconstruct an information criterion or likelihood-ratio statistic without their precise normalization and full parameter counts. Their ranking is enough to show that the best likelihood and best mean-dynamics fit do not coincide.

The Gaussian model's smallest diagonal mean-reversion coefficient is 0.378, with standard error 0.122; its other diagonal entries are 3.012 and 0.466. The one-volatility-factor model has a very persistent coordinate, $\kappa_{11}=0.002$ with standard error 0.001. Its volatility factor correlates 0.93 with the first principal component of yield changes. Several Gaussian state-dependent risk-price estimates are strongly different from zero, including $\lambda^Y_{11}=-101.8$ with standard error 36.91 and $\lambda^Y_{31}=158.0$ with standard error 30.90. These large numbers reflect the state normalization and should not be read as bond Sharpe ratios.

Figure 2 shows that only the Gaussian canonical model reproduces the strongly declining population regression slopes. The two- and three-volatility-factor models produce slopes close to one. The one-volatility-factor model produces a much flatter, insufficiently negative curve. Nevertheless, regressions on fitted historical yields look similar across all four models. This is the paper's cleanest demonstration of the danger of confusing fitted observations with an implied data-generating process.

Figure 3 finds that Gaussian and one-volatility-factor models approximately restore premium-adjusted slopes of one beyond about two years. The two- and three-volatility-factor models hardly change the unadjusted regression. The one-volatility-factor model therefore passes one part of the test without passing the other. The source's broad language about matching should be understood as a graphical and specification comparison; it does not supply a complete simultaneous confidence region for every adjusted maturity coefficient and estimated parameter.

For the Gaussian model, 500 simulations of length 312 produce average sample slopes close to the model population slopes. Historical coefficients fall within the displayed Monte Carlo bands. Parameters are treated as true for this experiment. The exercise checks finite-sample regression behavior conditional on the fitted model; it does not propagate parameter uncertainty or establish that the Gaussian model is the true data-generating mechanism.

## Restrictions that explain the differences

Constraining the one-volatility-factor model to be stationary under the pricing measure changes which state acts like level versus slope. Population slopes become downward sloping but still not negative enough; adjusted slopes deteriorate. Further setting $\beta_{21}=\beta_{31}=0$ confines stochastic volatility to the first factor. This makes that factor relatively fast reverting and improves both long-maturity tests, despite reducing the displayed likelihood from 33.54 to 33.42.

The inference is narrower than “stochastic volatility is bad.” In this parameter family, the likelihood's attempt to fit changing variances competes with the flexibility needed to fit first moments. The Gaussian model avoids that conflict by assuming constant conditional volatility. It may therefore be the better conditional-mean model while remaining knowingly incomplete as a joint yield-distribution model.

Re-estimating the one-volatility-factor model over the post-monetary-experiment subsample leaves the main projection patterns nearly unchanged. This weakens the claim that one unusual historical volatility regime alone drives the result. It does not establish stability over genuinely unseen future observations.

Figure 6 varies factor correlation and state-dependent risk compensation separately. Constant-risk-price Gaussian models fail with or without correlated factors. Allowing state dependence while forcing independent drift dynamics improves the result but is insufficient. Both drift correlation and flexible risk prices are needed for the successful Gaussian specification.

At maturities below two years, the three-factor model misses the adjusted slopes. A four-factor Gaussian model treats one- and six-month, two-year, and ten-year yields as exact. Figure 7 brings the short-end adjusted curve close to one. The fourth factor is useful for this diagnostic even though three principal components already explain most overall yield variation: a low-variance component can be consequential for a local forecast relationship.

## Printed-equation issues and proof scope

The premium decomposition on pages 5–6 is internally sufficient for the main result. Equation (23), visually checked on page 19, does not transcribe that decomposition consistently: it prints $p_t^n$ instead of $p_t^{n-1}$, omits a divisor $n-1$ on the expectation-revision sum, and gives the revision with the opposite sign to the identity implied by equations (2), (6), and (7). With the definitions above, the derived identity is

$$
z_{t+1}^n=x_t^n+\frac1{n-1}\sum_{i=1}^{n-1}(E_{t+1}[r_{t+i}]-E_t[r_{t+i}]).
$$

The conditional-mean conclusion survives because the revision has zero conditional expectation, but a programmer should use the coherent identity rather than copying equation (23).

Appendix B argues that an affine price of Gaussian risk yields a true exponential martingale on finite horizons using a linear-growth-in-Brownian-maximum condition, rather than a restrictive application of Novikov's condition. For a mean-zero scalar Ornstein–Uhlenbeck state, integration by parts bounds $|Y_t|$ by $(2-e^{-\kappa T})\sup_{s\le t}|W_s|$ when $\kappa>0$. The printed integration-by-parts display has a plus sign where differentiation with respect to the integration variable gives a minus sign; the ensuing absolute-value bound is unaffected. Initial states add a deterministic bounded term on a fixed horizon. These finite-horizon arguments should not be interpreted as requiring pricing-measure stationarity or as proving an infinite-horizon stationary distribution.

## Replication and investment interpretation

A faithful reproduction should first rebuild Table 1 using the original smoothed Fama–Bliss curve and exact monthly date index. Next fit each constrained model with documented state normalizations, transition density, exact-maturity inversion, and multistart likelihood optimization. Reproduce population slopes from model stationary moments, then compute historical adjusted slopes using observed yields and fitted premiums. Keep the two calculation paths separate. Recreate the 500-sample simulation with its 312-month length and separately add parameter resampling if uncertainty about the fitted structure is of interest.

The trading extension would require genuinely prospective estimation, a specified maturity portfolio and financing convention, and a comparison with simple forward-spread and random-walk benchmarks. The paper contains none of the transaction-cost, bid–ask, turnover, leverage, margin, or drawdown inputs needed to infer attainable PnL. Nor does it prescribe an objective such as mean–variance utility or a duration-risk constraint. A yield-premium forecast is a research output, not yet a complete portfolio rule.

The decision-relevant conclusion is that expectations-hypothesis failures are compatible with a tractable no-arbitrage model once compensation for risk can move independently of volatility and factors can interact. The stronger empirical lesson is methodological: assess the model's population dynamics and the target forecast moments explicitly, because a good yield fit and a higher likelihood can conceal the wrong expected returns.

## Source and bibliographic pointers

Dai, Qiang, and Kenneth J. Singleton, “Expectation Puzzles, Time-varying Risk Premia, and Affine Models of the Term Structure,” April 30, 2001 working paper. Core identities: equations (1)–(11), pages 5–6. Affine specification and test definitions: equations (12)–(20), pages 7–9. Data and likelihood: pages 9–11. Main evidence: Tables 1–3 and Figures 1–7, pages 3 and 11–19. Gaussian pricing and premium formulas: Appendix A, pages 22–24. Martingale argument: Appendix B, page 24. Auxiliary parameters: Appendix C, page 25. The bibliography on pages 25–27 identifies the underlying expectations-hypothesis, affine-pricing, and monetary-policy literature; this note does not independently verify those external works.

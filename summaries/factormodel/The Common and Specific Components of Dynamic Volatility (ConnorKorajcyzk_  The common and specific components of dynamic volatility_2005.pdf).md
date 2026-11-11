# The Common and Specific Components of Dynamic Volatility

Gregory Connor, Robert A. Korajczyk, and Oliver Linton. *Journal of Econometrics* 132 (2006), 231–255. DOI: 10.1016/j.jeconom.2005.01.029. The article became available online in March 2005; the library filename uses that year.

Source: [original PDF](../../Finance/ConnorKorajcyzk_%20%20The%20common%20and%20specific%20components%20of%20dynamic%20volatility_2005.pdf). References below use printed journal pages; PDF page 1 is journal page 231.

## Why this matters

A common shock to return *variance* need not be a common factor in return *levels*. Thousands of stock-specific residual returns can be approximately uncorrelated while their magnitudes rise together. Treating a factor model's residual covariance as constant therefore misses a potentially important source of changes in portfolio risk. Conversely, an increase in average individual-stock volatility does not necessarily mean that the variance of a broadly diversified portfolio has risen.

This paper separates three objects: variation in factor-related returns, a common scale for asset-specific returns, and each asset's remaining volatility dynamics. Its distinctive contribution is their joint organization in a large-cross-section model, with a rotation-invariant measure of factor-related volatility and a common residual-volatility state that becomes approximately observable through cross-sectional averaging. It applies existing heteroskedastic factor-extraction ideas rather than introducing an entirely new principal-components estimator.

The empirical application uses monthly US stock returns from January 1926 through December 2000. Common factor volatility and common residual volatility both peak around the Great Depression. Their subsequent paths differ: common residual volatility increases substantially after the mid-1960s, while factor volatility has much less secular increase. Innovations in factor volatility show business-cycle associations that are largely absent for innovations in common residual volatility. Individual residuals retain additional heteroskedasticity after the common scale is removed.

These are full-sample decomposition and fit results. The paper does not provide a rolling portfolio experiment, an out-of-sample volatility forecast competition, or transaction-cost-adjusted trading returns.

## Return model and the cross-sectional identification argument

Let $r_t$ be the $n$-vector of excess returns, $B$ an $n\times k$ loading matrix, $f_t$ a $k$-vector of factor returns, and $e_t$ the asset-specific return vector. The starting model is

$$
r_t=Bf_t+e_t.
$$

Loadings are fixed within an estimation block. Factors are not assigned particular economic names. Their scale, sign, and nonsingular rotation are arbitrary: replacing $f_t$ by $Lf_t$ and $B$ by $BL^{-1}$ leaves returns unchanged. Claims about the recovered factor space and fitted returns are meaningful without claiming that a particular estimated principal component is a structural economic shock.

The assumptions in equations (2)–(5), pp. 234–235, require conditional mean orthogonality of residuals to factors at every lead and lag; convergence $B'B/n\to M$, with $M$ positive definite; bounded operator norm of the residual covariance as the cross-section grows; and the cross-sectional law of large numbers

$$
\frac{e_t'e_s}{n}\xrightarrow{p}
\begin{cases}
0,&t\ne s,\\
\phi_t>0,&t=s.
\end{cases}
$$

This last condition is substantive. Cross-sectional averaging must eliminate off-diagonal time products of residual returns while retaining a date-specific average residual variance. Arbitrary serial and cross-sectional residual dependence is not permitted merely because the model is called approximate. The paper refers to mixing and moment conditions behind this law of large numbers and assumes the required uniform version in its application.

Write $R=(r_1,\ldots,r_T)$ and $F=(f_1,\ldots,f_T)$, of dimensions $n\times T$ and $k\times T$. The time-by-time cross-product matrix satisfies

$$
\widehat\Omega=\frac{R'R}{n}
\xrightarrow{p}F'MF+D_\phi,
\qquad D_\phi=\operatorname{diag}(\phi_1,\ldots,\phi_T).
$$

If every $\phi_t$ is the same, adding a scalar multiple of the identity changes eigenvalues but not eigenvectors. The leading $k$ eigenvectors then recover the row space of $F$. If the diagonal noise varies through time, ordinary principal components can mistake exceptionally noisy dates for important common-factor directions. Jones's correction whitens the time dimension by $D_\phi^{-1/2}$ before extracting components, then undoes that whitening.

For a matrix whose first $k$ eigenvectors are returned as rows, the operational expression is

$$
\widehat F=
\operatorname{eigvec}_k\!\left(D_\phi^{-1/2}\widehat\Omega D_\phi^{-1/2}\right)
D_\phi^{1/2}.
$$

It estimates a rotation of $F$. A stable leading subspace requires a suitable eigenvalue separation; nonsingularity by itself does not make individual eigenvectors uniquely defined or smooth when eigenvalues coincide. This is a qualification to the paper's compressed eigenvector argument, not an additional empirical result.

## Three volatility components

The scalar $\phi_t$ is the common asset-specific variance. Equation (10) models its logarithm as a smooth deterministic trend plus stationary short-run variation:

$$
\log\phi_t=g_\phi(t/T)+u_t,
\qquad a(L)u_t=b(L)c_t.
$$

The roots of the autoregressive polynomial are outside the unit circle. The central specification identifies $c_t$ as a martingale difference. A robust alternative imposes a zero conditional quantile at a selected probability instead of a zero conditional mean. The disturbances can themselves be conditionally heteroskedastic. The smooth trend accommodates long changes in volatility without imposing a unit root.

The asset-specific return is then scaled:

$$
e_t=\sqrt{\phi_t}\,Z_t,
\qquad \frac1n E[Z_t'Z_t]=1.
$$

The normalization fixes the otherwise arbitrary split between the common scale and individual residual magnitude. Unlike an ordinary low-dimensional stochastic-volatility state, $\phi_t$ can be estimated directly from a large cross-section of squared residuals. That approximate observability is central to the paper's sequential estimation strategy.

Each normalized residual may retain its own conditional variance:

$$
Z_{it}=\sqrt{h_{it}}z_{it},
\qquad E[z_{it}\mid\mathcal I_{t-1}]=0,
\quad E[z_{it}^2\mid\mathcal I_{t-1}]=1.
$$

Consequently the residual's conditional variance has both the common scale and the individual component. A coherent conditional covariance forecast would also need the appropriate conditioning and dependence assumptions for the scale and innovations; multiplying arbitrary separately estimated expectations is not automatically justified.

The paper fits three individual variance models. Suppressing the asset index, its GARCH and asymmetric GJR specifications are

$$
h_t=\omega_0+\omega_1h_{t-1}+\omega_2Z_{t-1}^2,
$$

$$
h_t=\omega_0+\omega_1h_{t-1}
+\omega_2Z_{t-1}^2\mathbf1\{Z_{t-1}<0\}
+\omega_3Z_{t-1}^2\mathbf1\{Z_{t-1}\ge0\}.
$$

With a positive intercept, nonnegative coefficients ensure nonnegative variances. Finite unconditional variance in the usual GARCH setting requires $\omega_1+\omega_2<1$, strictly. With symmetric unit-variance innovations, the corresponding GJR restriction is $\omega_1+(\omega_2+\omega_3)/2<1$. The paper prints weak inequalities; the boundary does not generally give finite stationary variance with a positive intercept. With asymmetric innovations, the half-weights need replacement by the relevant truncated second moments.

For factor-related volatility, the paper avoids attaching a variance process to an arbitrary rotation of each factor. Define

$$
\gamma_t=f_t'Mf_t
=\lim_{n\to\infty}\frac1n\|Bf_t\|^2.
$$

This quadratic form is invariant to nonsingular factor rotations. Cross-sectional mean squared return approximately decomposes as

$$
\frac1n r_t'r_t\simeq\gamma_t+\phi_t.
$$

The approximation drops the cross-product between fitted common returns and residuals. The factor-related scalar is modeled analogously:

$$
\log\gamma_t=g_\gamma(t/T)+v_t,
\qquad c(L)v_t=d(L)\xi_t.
$$

Here $\gamma_t$ is a realized squared common-return magnitude. It is not the full conditional $k\times k$ covariance matrix of $f_t$. Despite broader multivariate-volatility language in the article, these scalar equations alone do not identify all conditional factor correlations or supply a complete covariance forecast for arbitrary portfolios.

## Reconstructing the factor-extraction procedure

The CRSP sample comprises 900 months and 21,598 assets appearing at some point during January 1926–December 2000. Entry and exit make the panel unbalanced. Estimation divides the sample into fifteen nonoverlapping 60-month blocks, permitting the loadings to change between blocks. Within each block the authors try five, ten, and fifteen factors and use five in the reported application. This is a chosen specification, not a demonstrated information-criterion optimum.

For each pair of dates $t,s$, the unbalanced analogue of $\widehat\Omega_{ts}$ averages $r_{it}r_{is}$ over assets observed at both dates. The denominator therefore varies by date pair. Such a pairwise matrix need not be positive semidefinite in finite samples; the paper does not describe a repair if this occurs. It also does not provide all CRSP inclusion flags, return-adjustment and delisting conventions, or a complete data-cleaning program.

The iteration is implementable as follows. Initialize $D_\phi=I$. Obtain five factor series with the whitened eigenvector formula. For each stock with at least 36 observed months in the 60-month block, regress its excess returns on a constant and those factor series over its available observations. Compute residuals. At each date, update $\widehat\phi_t$ by the cross-sectional mean of squared fitted residuals. Repeat the eigenvector extraction and regressions until the factor space stabilizes. The constant is part of the empirical regression even though the theoretical return equation is written without a separate intercept.

The paper assesses convergence by regressing each new factor on all five factors from the previous iteration. This compares factor spaces rather than arbitrary signs or rotations. It examines the minimum adjusted $R^2$ over factors and blocks. Table 2 reports this minimum as 0.252 at iteration 2, 0.847 at iteration 3, and 0.999 at iteration 8, reaching 1.000 after rounding at iteration 9. The reported calculations run fifteen iterations. A numerical tolerance and maximum-iteration rule suitable for software are not supplied.

Two printed formulas should not be implemented literally without resolving their conventions. Equation (20), p. 241, writes a residual diagonal involving $\widehat F'\widehat\Lambda^2\widehat F$, while defining $\widehat\Lambda$ as eigenvalues; the square is inconsistent with the usual eigenvalue reconstruction unless the symbol instead denotes singular values and other transformations are matched. The unbalanced-panel residual-regression description gives the safer operational definition of $\widehat\phi_t$. Footnote 4's objective sums squared residuals across assets but gives only one copy of the log-variance penalty. Its scale-consistent Gaussian form is proportional to

$$
\sum_t\left[\frac{n^{-1}\sum_i(r_{it}-b_i'f_t)^2}{\phi_t}
+\log\phi_t\right],
$$

or the same expression multiplied by $n$. For an unbalanced panel, date-specific observation counts require corresponding care. These clarifications explain the algorithm; they are not claims that the authors' unavailable code used a particular correction.

In the first five-year block there are 494–730 stocks per month, averaging 610; the corresponding pairwise cross-products have 429–722 contributing stocks, averaging 539. In 1996–2000 the monthly counts are 6,664–7,687, averaging 7,293, and pairwise counts are 4,012–7,628, averaging 6,072 (Table 1). Reporting both counts matters because the effective sample for a covariance entry is not the total number of distinct securities.

The average adjusted stock-regression $R^2$ is 0.365 for ordinary asymptotic principal components and 0.358 after heteroskedastic adjustment. The range across blocks changes from 0.137–0.649 to 0.131–0.650. Fourteen of fifteen blocks have slightly lower average fit after adjustment. This does not contradict the estimator's purpose: it corrects heteroskedastic measurement noise rather than optimizing unweighted reconstruction fit at every iteration.

## Time-series estimation and the evidence on long-run change

After residual extraction, the authors estimate $\phi_t$ by residual mean squares and $\gamma_t$ by the mean squared fitted common return over the same eligible cross-section. These are stitched into 900-month time series. Full-sample smoothing uses observations on both sides of a date. The resulting estimated trend and factors are retrospective quantities; using them directly in a historical trading simulation would introduce future information.

The trend regressions use Chebyshev polynomials and autoregressive disturbances, with joint estimation by the Hildreth–Lu approach and heteroskedasticity-robust standard errors. The reported autoregressive orders are two for common residual volatility and four for factor volatility. The text describes a five-term polynomial specification for the full sample and a lower-order postwar choice selected by AIC, while Table 4 displays coefficients through $b_5$ in both panels. Exact polynomial normalization and this order-description discrepancy should be resolved before claiming an exact numerical replication.

The authors also graph nearest-neighbor estimates of means and the 25th, 50th, and 75th percentiles. The text specifies a 61-observation neighborhood, whereas the figure caption refers to 60 months. The graph is a local descriptive smoother, not a forecast with a strictly trailing information set. The formal dynamics concern logarithms, while some graph/table descriptions refer more loosely to variance levels; the transformed series must be recorded explicitly in an implementation.

Table 4 gives full-sample fit $R^2=0.502$ for the common residual series and $0.221$ for the factor-related series. The corresponding postwar values are 0.526 and 0.164. For the full-sample common-residual log process, AR coefficients are 0.191 and 0.100, with robust $t$ statistics 2.92 and 1.76. For the factor-related process, the four coefficients are 0.136, 0.106, 0.106, and 0.041, with $t$ statistics 3.73, 3.04, 2.96, and 1.24. These coefficients describe dynamics after detrending; they are not persistence estimates for the raw squared-return series.

Augmented Dickey–Fuller and Phillips–Perron exercises consider levels and logarithms, constant-only and linear-trend specifications, and zero through eight lags (Table 3). Their overall evidence favors stationarity around a trend, but not every reported statistic rejects at conventional levels. For example, a constant-only level ADF statistic at eight lags is −2.711. The corresponding logarithmic statistic is −3.569. Model choice should not be justified by asserting unanimous rejection across all specifications.

The graphical economic conclusion is that the rise in individual-stock risk after the mid-1960s is mainly a rise in common asset-specific variance, rather than an equivalent rise in factor variance. For an approximately diversified portfolio, more names may then be needed to attain a fixed residual-risk target even when broad-market volatility is comparatively stable. The paper does not estimate a universal required number of stocks, and a specific portfolio's answer depends on residual covariances and weights.

## Business-cycle comparisons and their timing

Section 4.3 examines contemporaneous and lead–lag correlations with six macroeconomic series: an NBER indicator equal to one in expansions and zero in contractions; the long-government-bond minus one-month Treasury-bill yield spread; the Baa minus Aaa corporate-yield spread; a trailing-three-month S&P dividend yield; and the Stock–Watson experimental leading and coincident indices. The last two are available only from February 1959 through December 2000. The bond and dividend series are attributed to Ibbotson; an exact vintage and treatment of publication delays are not given.

The tables define lag $\ell$ through $\operatorname{Corr}(X_t,\mathrm{Macro}_{t-\ell})$. Positive lags therefore compare a volatility shock with earlier macro information; negative lags compare it with later macro observations. These are not automatically real-time predictive relations because the macro series may be revised and the volatility innovations themselves are estimated with full-sample trends.

The distinction between variance levels and innovations is essential. Tables 5–6 focus on $c_t$ and $\xi_t$, the unexpected components after trend and autoregressive adjustment. At lag zero the $t$ statistic for correlation with the expansion indicator is 1.08 for the common residual-volatility innovation and −4.29 for the factor-volatility innovation. For the leading index the corresponding values are 0.67 and −4.12. Factor-volatility innovations are therefore associated with weaker business-cycle conditions, whereas the residual-volatility innovations show little analogous evidence.

For the default spread, the contemporaneous statistics are 1.26 and 2.34. The factor-volatility innovation has negative correlations with several lagged term-spread observations: for example, $t=-2.61$ at lag 3 and −3.16 at lag 12. The conclusion's positive term-premium wording is not an accurate description of those innovation/positive-lag entries. A replication should preserve the specific variable, lag convention, and table sign instead of flattening all associations into a single sign claim.

Ljung–Box-style joint correlation tests cover groups of 3, 6, 9, and 12 leads or lags. For factor shocks and past term spreads, the reported $p$ values are 0.029, 0.001, and values rounded to 0.000 for the longer groups. Common-residual shocks do not show the same strength. Such rounded values mean small positive probabilities, not literal probability zero. The paper does not supply a multiple-testing correction for the many series, leads, lags, and separate tests; it also does not identify a causal economic mechanism.

## Asset-specific likelihood fits and numerical results

The individual-volatility exercise retains stocks with at least 90 consecutive months of returns, yielding 7,054 assets. Each stock receives six fits: GARCH, GJR, and EGARCH, each with Gaussian and Student-type innovations. Estimation is asset by asset using the Berndt–Hall–Hall–Hausman routine. Nonnegativity restrictions are imposed for GARCH and GJR, but covariance-stationarity restrictions are not imposed in optimization. Convergence and stationarity are subsequently reported separately.

For GARCH and GJR, variance targeting replaces the intercept with a sample-variance estimate. In the GARCH case, with target $\bar h$, the fitted recursion is

$$
h_t=\bar h+\omega_1(h_{t-1}-\bar h)
+\omega_2(Z_{t-1}^2-\bar h).
$$

This is algebraically the usual recursion with intercept $(1-\omega_1-\omega_2)\bar h$. Variance targeting thus removes one nonlinear parameter; it does not remove the need to consider stationarity or the distributional normalization. The analogous GJR transformation is used. The authors do not apply variance targeting to EGARCH.

The comparison loss is in-sample mean absolute error between fitted variance and the normalized squared residual:

$$
\mathrm{MAE}_i=\frac1{T_i}\sum_t|\widehat h_{it}-Z_{it}^2|.
$$

It is a variance-proxy loss, not a return-forecast error, percentage return, or trading-profit measure. Table 7's cross-model MAE comparison uses only the intersection of stocks for which all six fits converge. The size of that intersection and a full failure-by-model breakdown are not reported.

| Model | Converged, % | Stationary, % | MAE lower quartile | Median MAE | MAE upper quartile | Best MAE, % of assets |
|---|---:|---:|---:|---:|---:|---:|
| Gaussian GARCH | 99.9 | 97.1 | 1.58 | 2.97 | 5.92 | 0.1 |
| Student GARCH | 99.6 | 98.0 | 1.62 | 3.11 | 6.19 | 0.1 |
| Gaussian GJR | 89.4 | 89.1 | 1.41 | 2.61 | 5.09 | 21.7 |
| Student GJR | 93.3 | 92.3 | 1.33 | 2.45 | 4.69 | 16.8 |
| Gaussian EGARCH | 96.0 | 91.0 | 1.58 | 3.03 | 6.43 | 0.5 |
| Student EGARCH | 95.4 | 93.6 | 1.18 | 2.16 | 4.04 | 61.0 |

Student EGARCH has the lowest median MAE and wins for 61.0% of the comparison assets; it is worst for only 0.3%. Student GARCH is worst for 38.7%. These are descriptive rankings on fitted data, with an intentionally noisy squared-return proxy. They do not establish that the winner forecasts a latent variance best out of sample.

Table 8 suggests heavy-tailed innovations and some negative-return asymmetry. The Gaussian GJR median difference between negative- and nonnegative-return coefficients is 0.008; the Student GJR median difference is 0.200. Asset-level significance is often weak. Median estimated Student degrees of freedom are 4.15 for GARCH and 2.86 for EGARCH, but 1.49 for GJR, with a lower quartile of 0.673. A conventional Student distribution with degrees of freedom at or below two lacks finite variance, conflicting with the earlier unit-variance innovation assumption. The source does not reconcile this or fully document its density scaling. One cannot silently call every reported fit a finite-variance standardized-t GARCH.

## Mathematical and reproducibility boundaries

The printed EGARCH equation (16), also repeated in Table 8's note, divides $Z_{t-1}$ by $h_{t-1}$ even though $h$ is explicitly a variance. Standard variance normalization would divide by $\sqrt{h_{t-1}}$. For a coherent EGARCH reimplementation, define $z_{t-1}=Z_{t-1}/\sqrt{h_{t-1}}$ and model log variance using magnitude and signed standardized shocks, with centering conventions absorbed or explicitly included in the intercept. That is a corrected implementation choice, not evidence of what the original code actually computed. The text additionally refers to an $\omega_4$ asymmetry parameter although the displayed equation labels only $\omega_0$ through $\omega_3$.

The asymptotic justification for treating generated factors and variance states as known in subsequent root-$T$ inference requires strong uniform convergence. The paper states a necessary growth condition $n/T^2\to\infty$. A large total count of distinct stocks is not itself evidence that this approximation is quantitatively accurate in every 60-month block, especially early in the sample. Nor does the paper provide a complete finite-sample correction for factor-estimation uncertainty.

An exact reproduction further needs the return and risk-free data definitions, pairwise-missing-data implementation, numerical eigensolver and normalization, lower bounds for variance updates, smoothing basis normalization, innovation likelihood scaling, initialization, optimizer tolerances, and handling of failed fits. These are incompletely specified. The principal reproducible scientific idea survives those omissions: estimate common return directions under heteroskedastic residual noise, distinguish a shared residual-variance state from factor-related variation, then examine what individual conditional variance dynamics remain. Applying it operationally requires a causal estimation window and an explicitly defined covariance forecast, followed by independent out-of-sample evaluation.

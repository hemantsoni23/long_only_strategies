# Forecasting multivariate realized stock market volatility

**Gregory H. Bauer and Keith Vorkink (2011).** *Journal of Econometrics* 160, 93–101, DOI 10.1016/j.jeconom.2010.03.021. Source: [original PDF](../../Finance/Volatility_BauerVorkink_2011.pdf), nine pages, including four tables and the elasticity figure. Page references below use printed journal pages. This is the published article; its empirical evidence primarily concerns fitted conditional covariance dynamics over 1988–2002.

## Why this matters

A useful covariance forecast must satisfy two different requirements: its matrix must be mathematically admissible, and its dynamics must be estimated without spending more parameters than the available data support. Modeling each variance and covariance independently can violate positive definiteness. Fully unrestricted systems can also waste a large number of coefficients on correlated predictors. Bauer and Vorkink combine a matrix logarithm with a reduced-rank predictive system to address both problems.

Their innovation is a particular architecture: transform a realized covariance matrix into unrestricted symmetric log-matrix coordinates; forecast those coordinates with a small number of latent factors formed from many observed predictors; then exponentiate the fitted matrix. Two predictive factors are not rejected for any of four predictor sets in the five-portfolio application. Past continuous variation, represented by principal components of weekly and monthly bipower covariation, is informative. Some variables associated with expected returns retain additional information, especially dividend yield.

The distinction between the two dimension reductions is essential. Principal components compress the lagged bipower-covariation predictors. Separately, the reduced-rank model restricts how those predictors affect the fifteen elements of tomorrow's log covariance matrix. These are not two ways of naming the same factors. Nor are the resulting factors the common return shocks in an ordinary linear return factor model.

The article offers a tractable forecasting method and an in-sample investigation of conditional risk. It does not provide a trading strategy, portfolio turnover calculation, or documented rolling out-of-sample horse race. A reader should not turn the title's forecasting language into an unsupported claim of demonstrated live portfolio improvement.

## Covariance coordinates and the exact positivity result

Let $V_t$ denote a daily $P\times P$ realized covariance matrix and define

$$
A_t=\logm(V_t),\qquad a_t=\operatorname{vech}(A_t),\qquad p=P(P+1)/2.
$$

The vech operator retains one triangle, including the diagonal, in a fixed order. In the application $P=5$ and $p=15$. The matrix logarithm is not an elementwise logarithm. In particular, off-diagonal covariances can be negative without preventing a matrix logarithm, provided the whole covariance matrix is positive definite. Conversely, applying a scalar logarithm to the covariance entries would be a different and often undefined operation.

For a symmetric positive-definite matrix with eigendecomposition $V=U\Lambda U^{\mathsf T}$,

$$
\logm(V)=U\operatorname{diag}(\log\lambda_1,\ldots,\log\lambda_P)U^{\mathsf T}.
$$

For any finite real symmetric forecast $\widehat A$,

$$
\widehat V=\expm(\widehat A)
=\sum_{n=0}^{\infty}\frac{\widehat A^n}{n!}
=U\operatorname{diag}(e^{a_1},\ldots,e^{a_P})U^{\mathsf T}
$$

is strictly positive definite. No sign restrictions on regression coefficients are needed for this conclusion. This is the main mathematical advantage of the construction.

There is a qualification to the article's wording on p. 94: a merely positive-semidefinite input can have zero eigenvalues, for which no finite real symmetric logarithm exists. The realized inputs must therefore be strictly positive definite in an implementation. The paper does not specify an eigenvalue floor, nearest-positive-definite projection, or alternative treatment of singular daily matrices. Such a remedy should be documented as an additional design choice, rather than silently attributed to the authors. Exponentiating a finite symmetric fitted matrix does give a strictly positive-definite output, even where the article calls it semidefinite.

The entries of $A_t$ are transformed coordinates of the entire covariance matrix. A diagonal entry is not simply the log variance of the correspondingly numbered portfolio, and an off-diagonal entry is not the log correlation. This complicates economic interpretation but prevents separate positivity constraints from proliferating across fifteen equations.

## Predictive reduced-rank model

Write $Z_{t-1}$ for an $N\times1$ vector of predictors available before day $t$. The unrestricted predictive system is

$$
a_t=\gamma_0+\Gamma Z_{t-1}+\varepsilon_t.
$$

The proposed restriction is

$$
\Gamma=\beta\theta,\qquad
\beta\in\mathbb R^{p\times K},\quad
\theta\in\mathbb R^{K\times N},
$$

so that

$$
a_t=\gamma_0+\beta\theta Z_{t-1}+\varepsilon_t,
\qquad \nu_t=\theta Z_{t-1}.
$$

The $K$ components of $\nu_t$ are latent predictive factors whose realizations are linear combinations of observable predictors. Each log-matrix coordinate has its own row of loadings in $\beta$. Factors are not separately measured innovations; their weights and cross-equation loadings are jointly estimated.

Without normalization, replacing $\beta$ by $\beta Q$ and $\theta$ by $Q^{-1}\theta$ leaves every prediction unchanged for invertible $Q$. The paper identifies the model by setting the first $K$ rows of $\beta$ equal to $I_K$. The vech ordering must therefore be fixed consistently when reproducing the normalization and Table 3. For $K=2$, the normalized coordinates are the first diagonal and first off-diagonal elements displayed there. The normalization presupposes a suitable nonsingular loading block; it is not a substantive economic restriction that those two coordinates are the only sources of risk.

With this normalization, the parameter count is $p+K(p-K)+KN$. The unrestricted count is $p(N+1)$, and the number of rank restrictions is $(p-K)(N-K)$. For the actual two-factor systems, the four predictor counts are 4, 6, 5, and 11, giving 26, 52, 39, and 117 restrictions respectively. These agree with Table 2's reported degrees of freedom.

The article's parameter-count illustration uses twenty lags of all fifteen daily log-bipower coordinates plus five economic variables: $15(1+300+5)=4,590$ unrestricted coefficients. Replacing those dynamics with three principal components at each of three horizons, plus five other predictors, gives $N=14$ and 69 coefficients under two factors. That illustration is distinct from the final selected predictor sets, which omit daily components and most weekly components.

## Predictors, horizons, and information timing

The initial volatility predictors are bipower-covariation matrices aggregated over $d=1,5,20$ days. Bipower covariation targets the continuous component of variation under its maintained high-frequency assumptions, whereas the dependent realized covariance includes the realized total covariance measure used by the authors. They cite Definition 3 of Barndorff-Nielsen and Shephard (2005) for the multivariate bipower construction.

For each horizon, take the matrix logarithm of the bipower-covariation matrix, vectorize it, and obtain principal-component scores. The source reports that the first three components explain 48.5%, 85.3%, and 94.2% of variation in the daily, five-day, and twenty-day series respectively. The longer aggregates are much more compressible in this sense. The published article does not spell out whether PCA uses covariance or correlation scaling, its exact standardization convention, or every normalization of the multiday aggregation. These choices matter for reproducing reported factor coefficients, although consistent linear rescaling need not change fitted values.

The final model variants are:

| Model | Lagged predictors |
|---|---|
| MHAR-RV-BP | First five-day component and first three twenty-day components |
| MHAR-RV-BPA | BP predictors plus negative small- and large-portfolio returns |
| MHAR-RV-X | Treasury-bill rate, credit spread, term spread, scorecard, dividend yield |
| MHAR-RV-BPAX | All eleven predictors from the preceding sets |

The negative-return variables mean the return itself when negative and zero otherwise, conceptually $R_{i,t-1}\mathbf1\{R_{i,t-1}<0\}$. They are not simply binary indicators for a down day. The scorecard is the prior-return-based sensitivity-to-news variable of McQueen and Vorkink (2004); its full recursion is not reproduced here. The term spread is the long government-bond yield minus the three-month bill yield. Exact maturity/data-provider details for all interest-rate and dividend series are not completely specified in the article.

One-day components were considered but omitted because of multicollinearity and weaker stability; adding them reportedly did not improve estimates. This selection is part of the reported empirical design, not a theorem that daily variation never forecasts well. Both the five- and twenty-day windows must end before the target date. A live extension must also estimate PCA loadings, transformations, and any bias correction using only the training window; the article's full-sample results are not evidence that those objects were estimated recursively.

## GMM implementation and generated-regressor issue

The model is estimated by iterated GMM, with a maximum of 25 iterations and a Newey–West weighting matrix. An Andrews procedure selects 46 lags for the HAC covariance calculation. The general moment vector can be written

$$
g_T(\psi)=\frac1T\sum_t h_{t-1}\otimes
\left(a_t-\gamma_0-\beta\theta Z_{t-1}\right),
$$

with objective $g_T(\psi)^{\mathsf T}Wg_T(\psi)$ and normalized parameter vector $\psi$. Include an intercept in the instrument vector as needed to identify the equation intercepts. Update the weighting matrix from the fitted moment series, respecting the same parameter normalization at each step.

The article initially describes the predictors as instruments, then qualifies this for measurement error: the bipower matrices, and hence their PCA scores, are estimated rather than perfectly observed. Following a lagged-instrument strategy, it uses twice-lagged component values in the instrument set. Thus the regression uses $Z_{t-1}$ but the noisy volatility-component instruments use information at $t-2$. The precise bookkeeping of every instrument and constant is not printed as a complete design matrix. The numerical degrees of freedom provide a useful consistency check on any reconstruction.

Using an extra lag is a proposed response to errors in variables, not automatic proof of valid instruments. Overlapping five- and twenty-day windows share underlying returns, and serially correlated measurement errors can persist. A replication should examine instrument relevance and the required orthogonality; the published evidence does not eliminate those concerns. HAC standard errors address dependence in the moment sequence under their assumptions, but do not repair an invalid moment condition.

For each fitted date, reconstruct the symmetric matrix from $\widehat a_t$ and exponentiate it. Store both log-space residuals and realized-space errors because the transformation makes these distinct loss systems. The published $J$ tests concern rank-restricted moment fit, not equality between every predicted covariance and its realized value.

## Median rescaling and its limitations

Exponentiating fitted log coordinates does not generally produce the conditional mean covariance. Nonlinearity implies that the exponentiated conditional location differs from the expectation of the exponentiated random matrix. The article avoids a parametric normal-error correction because its log-space residuals are not normally distributed.

It decomposes realized and fitted matrices into standard deviations and correlations, then estimates one scale factor per portfolio:

$$
c_i=\frac{\operatorname{median}_t\sqrt{V_{ii,t}}}
{\operatorname{median}_t\sqrt{\widehat V_{ii,t}}},
\qquad C=\operatorname{diag}(c_1,\ldots,c_P).
$$

The corrected matrix is equivalently

$$
\widehat V_t^{\,bc}=C\widehat V_t C.
$$

This preserves correlations and positive definiteness when all $c_i$ are positive. A variance is multiplied by $c_i^2$, and a covariance by $c_ic_j$. Applying the standard-deviation scale directly to a variance would be an implementation error.

The correction aligns marginal median scales. It is not an exact matrix-Jensen correction, a conditional-mean-unbiasedness theorem, or a remedy for correlation forecast bias. In a prospective experiment, estimating these factors from held-out realized variances would introduce look-ahead. The article presents the correction as a simple pragmatic procedure and acknowledges that more sophisticated corrections could improve it.

## Data and what must be supplied for reproduction

The high-frequency sources are ISSM quotes for January 1988–December 1992 and TAQ quotes for January 1993–December 2002. The earlier ISSM period was not used because missing days interfere with the desired contiguous series. CRSP supplies prior-month-end prices and shares outstanding. Stocks must appear in both CRSP and the corresponding quote database, and only CRSP share codes 10 and 11 are retained, excluding preferred shares and warrants.

Five size portfolios are formed using prior-month-end capitalization, and their high-frequency returns are value weighted. The text describes NYSE securities, whereas Table 1's caption describes NYSE, AMEX, and NASDAQ portfolios. This exchange-universe discrepancy remains unresolved in the supplied article and should not be hidden by choosing one description. The complete security list, detailed quote cleaning, handling of crossed/stale quotes, intraday sampling grid, portfolio weight updating, and corporate-action synchronization are not reported as executable rules.

The realized covariance estimator follows the Hansen–Lunde (2006) Newey–West-type correction for serial dependence in high-frequency returns. This is consequential for smaller stocks, whose price response may arrive slowly. Overnight information is incorporated using Hansen–Lunde (2005). The article cites these methods but does not reproduce the full multivariate kernel formula, selected high-frequency bandwidth, or exact overnight weights. Consequently, this note specifies the predictive system completely but cannot honestly supply source-reported values for all upstream realized-measure settings. Those must be obtained from original code, authors, or a documented reconstruction of the cited estimators.

The estimator's lag correction already incorporates some interportfolio timing effects. A finding of weak additional predictive influence from yesterday's large-stock negative return therefore cannot be interpreted as showing that large stocks never lead small stocks. Part of that dependence may already enter the constructed target.

Table 1 illustrates the matrix-log distribution: small-portfolio diagonal coordinate mean −11.880, standard deviation 1.228, and AR(1) 0.452; large-portfolio values are −11.450, 1.187, and 0.420. These are log-matrix coordinates, despite percentage labels in the table, and should not be read as negative variances or annual volatility percentages. The prose says all univariate normality tests reject, but Table 1 reports $p=0.110$ and $0.137$ for two off-diagonal coordinates. Many, rather than every, coordinate rejects at conventional levels; multivariate normality also rejects.

## Empirical results and their proper interpretation

One-factor models are rejected for every predictor set. With two factors, Table 2 reports:

| Predictor set | $J$ statistic | Degrees of freedom | $p$ value |
|---|---:|---:|---:|
| BP | 32.82 | 26 | 0.167 |
| BPA | 48.48 | 52 | 0.613 |
| X | 41.95 | 39 | 0.344 |
| BPAX | 72.32 | 117 | 0.999 |

These tests fail to reject the two-factor restrictions even at 10%. Failure to reject does not identify the true number of economic volatility shocks, nor establish that rank two forecasts best out of sample. The exceptionally high BPAX $p$ value should be reported rather than converted into a probability that the model is correct.

The variance-ratio diagnostics compare the time-series variance of fitted values from the restricted system with that of fitted values from an unrestricted regression. They are not $R^2$, mean-square-error ratios, or forecast improvement percentages. In log space the BP ratio is 0.984 for the smallest-portfolio diagonal and 0.961 for the largest; an off-diagonal ratio is only 0.029. Some ratios exceed one because GMM rank restrictions are not imposed by orthogonal least-squares projection under the same metric.

In realized space the diagonal comparison also includes the nonlinear transformation and rescaling; off-diagonals instead use Fisher-transformed correlations. BPAX's smallest diagonal ratio is 1.062 and largest 0.795, while the smallest–largest correlation ratio is 0.236. BP's corresponding correlation ratio is 0.678. More economic predictors do not uniformly preserve more fitted correlation variation. None of these numbers alone proves lower prediction loss.

Table 3's BPAX loadings help describe the fitted coordinates. The first factor has diagonal loadings 1.000, 0.729, 0.699, 0.545, and −0.025; the last is imprecise, with standard error 0.058. The second has diagonal loadings 0, 2.159, 3.719, 3.790, and 5.686. Since the factors are normalized and matrix exponentiation mixes coordinates, these coefficients are not direct percentage sensitivities of stock variances.

## Interpreting predictor effects correctly

For predictor $z$, form the symmetric derivative matrix

$$
B_z=\frac{\partial\widehat A}{\partial z}
=\operatorname{vech}^{-1}\!\left(\beta\theta_{\cdot z}\right).
$$

The derivative of a matrix exponential is generally not $e^{\widehat A}B_z$, since the two matrices need not commute. The paper uses the block identity

$$
\exp\begin{pmatrix}\widehat A&B_z\\0&\widehat A\end{pmatrix}
=\begin{pmatrix}e^{\widehat A}&D_z\\0&e^{\widehat A}\end{pmatrix},
\qquad D_z=\frac{\partial\widehat V}{\partial z}.
$$

For diagonal elements its reported sensitivity is $D_{z,ii}\sigma_z/\widehat V_{ii}$. For off-diagonals the denominator is instead $\sqrt{\widehat V_{ii}\widehat V_{jj}}$ to avoid exploding ratios around zero covariance. These are local, standard-deviation-scaled derivatives. They are not conventional percentage-on-percentage elasticities, and off-diagonal values are not percentage changes relative to the covariance itself. A finite one-standard-deviation shock need not equal the derivative approximation when the transformation is nonlinear. If applying median correction, transform derivatives by the same $C$ matrices while holding the estimated scale factors fixed.

For BP, a positive one-standard-deviation movement in the second twenty-day component has mean local sensitivities +0.116 for small-stock variance, −0.337 for large-stock variance, and −0.105 for standardized small–large covariance. The first five-day component instead gives +0.392, +0.448, and +0.305. Thus the second monthly component changes the cross-sectional pattern, while the first weekly component mainly raises common risk. These are variance sensitivities; volatility in the standard-deviation sense has approximately half the proportional local response.

For BPA, the own-negative-return sensitivities are −0.142 for small-stock variance and −0.119 for large-stock variance. A movement toward a more negative return reverses the sign of the predictor change and therefore raises forecast variance. This interpretation is lost if the negative-return variable is incorrectly replaced by a down-day dummy.

With economic variables alone, the small-stock variance sensitivity to the credit spread is 0.534; in BPAX it falls to 0.102. The bill-rate sensitivity falls from 0.285 to 0.043. Dividend yield remains comparatively substantial: −0.151 for small variance, −0.240 for large variance, and −0.139 for standardized small–large covariance. Persistent economic variables can proxy for omitted volatility persistence, so their apparent effects shrink when the bipower predictors enter.

A source inconsistency deserves explicit notice: the p. 99 prose says BPAX's first-factor credit-spread coefficient becomes insignificant, but Table 4 gives 21.062 with standard error 5.218, a ratio of about 4.04. Its coefficient is much smaller than the X-only estimate 234.593, but the displayed numbers do not support insignificance. Table 4 should govern that numerical inference. The authors report very small HAC $p$ values for average elasticities, while Figure 1 shows meaningful variation in sensitivities through time. Neither is a causal identification strategy.

## Reimplementation boundaries and takeaways

An implementation should retain the following separations: the observed realized target versus its conditional expectation; principal-component compression versus predictive rank restriction; log-coordinate loss versus covariance-space loss; median scale alignment versus unbiased expectation; and local derivative effects versus finite counterfactual shocks. Each separation changes what can legitimately be concluded from the fitted model.

The core system can be rebuilt from positive-definite daily covariance inputs, lagged bipower components, and the stated predictor sets. Exact replication remains limited by omitted high-frequency cleaning and bandwidth settings, unresolved exchange coverage, incomplete scorecard and macro-series definitions, PCA scaling, and full instrument bookkeeping. The published tables do not include all intercepts and every transformation required to reconstruct the authors' fitted matrices solely from printed coefficients.

For research use, the method supplies a coherent way to compress many predictors into a small number of covariance dynamics while guaranteeing admissible forecast matrices. The economic conclusion is narrower: in these historical size portfolios, two predictive factors fit the imposed moments, lagged continuous variation matters strongly, and some additional return predictors contain risk information. Establishing portfolio value would require a separate prospective experiment with training-only transformations, explicit forecast losses, realistic constraints and costs, and independently specified evaluation windows.

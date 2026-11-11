# Evaluating latent and observed factors in macroeconomics and finance

Jushan Bai and Serena Ng. *Journal of Econometrics* 131 (2006), 507–537. DOI: 10.1016/j.jeconom.2005.01.015. The supplied article was available online in February 2005; its journal year is 2006.

Source: [local PDF](../../Finance/MacroLatentFactorModels_BaiNg_2006.pdf), 31 pages, including the proof appendix and all six tables. References below use journal pages and the article's equation numbers. This is the proxy-evaluation paper, not Bai and Ng's separate papers on selecting the number of static factors or primitive shocks.

## Why this matters

A named economic series can correlate strongly with returns without being a satisfactory proxy for the latent common component of those returns. Conversely, an exact factor can explain little of an individual noisy stock's variance. Regressing individual returns on a candidate factor therefore confounds proxy quality with the amount of idiosyncratic noise in the test assets.

Bai and Ng move the comparison to the factor space. Estimate that space from a large panel, project observed candidate variables onto it, and ask how much discrepancy remains after allowing for the sampling error in the estimated factors. Their contribution is a set of diagnostics that distinguishes exact factor membership, approximate proxy quality, and the joint span of several proxies. The large cross-section is essential: factor-estimation error shrinks with the number of indicators, making a direct latent-versus-observed comparison possible.

The empirical conclusion is differentiated. Fama–French variables closely approximate important directions in size/book-to-market portfolios, especially at annual frequency. The market factor remains a strong proxy for individual-stock factors, while SMB and HML become substantially weaker. Conventional macroeconomic variables do not closely reproduce the full macroeconomic or return-factor spaces. These are covariance-space findings, not demonstrations that particular factors earn prices of risk or that a trading strategy is profitable.

## Panel model, assumptions and normalization

For series $i=1,\ldots,N$ and dates $t=1,\ldots,T$, use the approximate factor model

$$
x_{it}=\lambda_i'F_t+e_{it},\qquad F_t\in\mathbb R^r.
$$

The factors have bounded fourth moments and a positive-definite limiting time covariance. Loadings have bounded magnitude or bounded fourth moments and satisfy $\Lambda'\Lambda/N\to\Sigma_\Lambda\succ0$. These conditions make all $r$ factors pervasive. The idiosyncratic errors have bounded eighth moments, weak enough temporal and cross-sectional dependence for the paper's covariance sums and central limit arguments, and may be heteroskedastic. Factors, loadings and idiosyncratic errors are mutually independent groups under Assumption D. These are stronger restrictions than merely noticing a few large sample eigenvalues.

Let $X$ be $T\times N$, with dates in rows. Center and standardize each input series as in the empirical work. Compute the leading $r$ eigenvectors of $XX'/(NT)$, collect them in $U_r$, and define

$$
\widetilde F=\sqrt T U_r,\qquad
\widetilde F'\widetilde F/T=I_r,\qquad
\widetilde\Lambda=X'\widetilde F/T,\qquad
\widetilde e_{it}=x_{it}-\widetilde\lambda_i'\widetilde F_t.
$$

Write $\widetilde V$ for the diagonal matrix of the selected eigenvalues. A nonsingular rotation $H$ relates estimated factors to true factors. The mean squared factor-estimation error is of order $1/\min(N,T)$. For a fixed date, when $\sqrt N/T\to0$, the scaled error $\sqrt N(\widetilde F_t-HF_t)$ is asymptotically normal with covariance driven by

$$
\Gamma_t=\lim_{N\to\infty}\frac1N
\sum_{i=1}^N\sum_{\ell=1}^N
E[\lambda_i\lambda_\ell'e_{it}e_{\ell t}].
$$

The important object is the span of $F$, which is invariant to $H$. Individual principal components are not uniquely identified economic factors. A comparison that changes when the PCA basis is rotated is not the comparison developed here.

The paper selects $r$ using panel information criteria based on residual variance. In implementation these criteria must be **minimized**: residual variance plus a positive complexity penalty, or log residual variance plus a penalty. The supplied text prints “argmax,” which is inconsistent with the criteria's purpose. The requirements are $g(N,T)\to0$ and $\min(N,T)g(N,T)\to\infty$. The empirical penalties include $(N+T)\log[NT/(N+T)]/(NT)$ and $(N+T)\log\min(N,T)/(NT)$. The analysis treats consistent factor-count selection as asymptotically equivalent to knowing $r$; it does not remove finite-sample sensitivity to an over- or underestimated factor dimension.

## Testing one proxy: exact membership

Let $G_{jt}$ be an observed candidate. The exact null is that one fixed vector $d_j$ satisfies

$$
G_{jt}=d_j'F_t\quad\text{for every }t.
$$

Estimate $G_j=\widetilde F\gamma_j+\text{error}$ by OLS and set $\widehat G_{jt}=\widehat\gamma_j'\widetilde F_t$. With centered inputs, the normalization gives $\widehat\gamma_j=\widetilde F'G_j/T$. The null involves a constant linear relationship across the sample. A rejection can therefore reflect changing coefficients, proxy noise, or a component outside the latent factor space.

The key statistic is

$$
\widehat\tau_t(j)=
\frac{\widehat G_{jt}-G_{jt}}
{\sqrt{\widehat v_{jt}}},\qquad
\widehat v_{jt}=
\frac1N\widehat\gamma_j'\widetilde V^{-1}
\widetilde\Gamma_t\widetilde V^{-1}\widehat\gamma_j.
$$

Under the exact null and the stated growth condition, it is factor-estimation error, rather than ordinary OLS residual noise, that supplies the leading variance. The proof writes the fit error as a coefficient-estimation part plus $\widehat\gamma_j'(\widetilde F_t-HF_t)$. The first part is negligible at the $\sqrt N$ scale under the null; the second inherits the factor central limit theorem. Using the usual OLS prediction standard error alone would omit the central uncertainty being tested.

The article aggregates these standardized discrepancies in two ways:

$$
A(j)=\frac1T\sum_{t=1}^T
1\{|\widehat\tau_t(j)|>z_{1-\alpha}\},\qquad
M(j)=\max_{1\le t\le T}|\widehat\tau_t(j)|.
$$

With $\alpha=0.025$, $A(j)$ should approach 0.05 under exact membership. It is the fraction of dates exceeding a pointwise two-sided threshold, not a conventional regression p-value and not a binary test with finite-sample size 5% merely because one compares it to 0.05. The paper provides its probability limit; a formal finite-sample rejection band around that limit would require additional calibration.

For $M(j)$ the stated approximation requires serially uncorrelated idiosyncratic errors. Then the limiting datewise normal discrepancies are independent and

$$
P\{M(j)\le c\}\approx[2\Phi(c)-1]^T.
$$

A familywise level $\eta$ threshold is consequently

$$
c_{T,\eta}=\Phi^{-1}\!\left(\frac{1+(1-\eta)^{1/T}}2\right).
$$

Use this expression with the actual sample length, rather than a fixed 1.96 cutoff for the maximum. The source's tabulated 5% cutoffs are approximately 3.283 for $T=50$, 3.467 for $T=100$, 3.656 for $T=200$ and 3.830 for $T=400$. Serial correlation invalidates the independent-normal maximum calibration; the law-of-large-numbers result for $A$ is less restrictive. The source suggests extreme-value alternatives but does not implement a general dependent-error maximum test.

## Choosing the factor-error covariance estimator

Equations (4)–(6), p. 514, describe three distinct covariance models. They are not interchangeable robustness options.

When idiosyncratic errors are cross-sectionally uncorrelated but can be heteroskedastic over dates and series, use

$$
\widetilde\Gamma_t=\frac1N\sum_{i=1}^N
\widetilde e_{it}^{2}\widetilde\lambda_i\widetilde\lambda_i'.
$$

This is the estimator used in the reported empirical applications. It does not protect inference against arbitrary residual cross-sectional correlation. Approximate factor consistency permits weak cross-sectional dependence more generally, but the selected standard-error estimator still has its own narrower requirements.

If errors are cross-sectionally uncorrelated and have a common variance across dates and units, pool that variance:

$$
\widehat\sigma_e^2=\frac1{NT}\sum_{i,t}\widetilde e_{it}^2,\qquad
\widetilde\Gamma=\widehat\sigma_e^2\widetilde\Lambda'\widetilde\Lambda/N.
$$

For cross-correlated errors with a time-invariant covariance structure, the source instead proposes CS-HAC:

$$
\widetilde\Gamma=
\frac1n\sum_{i=1}^{n}\sum_{\ell=1}^{n}
\widetilde\lambda_i\widetilde\lambda_\ell'
\left(\frac1T\sum_t\widetilde e_{it}\widetilde e_{\ell t}\right),
\qquad \frac{n}{\min(N,T)}\to0.
$$

The smaller cross-sectional subset is important. Summing all $N^2$ estimated residual covariances is not the estimator justified here: factor and loading estimation error contaminates that operation. Repeated observations through time make covariance estimation possible under stationarity. The article refers the formal CS-HAC treatment to separate work and does not give a universally applicable rule for selecting $n$ or an ordering-independent empirical subset. Those choices must be recorded by a reproducing researcher.

## Approximate proxies and measurement-error paths

The exact null can be rejected even when a proxy is economically useful. The alternative representation is

$$
G_{jt}=d_j'F_t+\epsilon_{jt},\qquad
\widehat\epsilon_{jt}=G_{jt}-\widehat G_{jt}.
$$

The residual variance consistently estimates the variance of the component not explained by the factor space. The label “measurement error” is generic: $\epsilon$ may be systematic omitted variation, not literal recording error. The relevant OLS projection imposes orthogonality to the factor regressors; interpreting $d_j$ structurally requires more.

There are now two sources of uncertainty in estimating the error path. Coefficients are estimated with $T$ observations, and factor values with $N$ indicators. Under conditional homoskedasticity the feasible variance for $\widehat\epsilon_{jt}-\epsilon_{jt}$ is

$$
\widehat s_{jt}^2=
\frac1T\widetilde F_t'\widetilde F_t\widehat\sigma_{\epsilon,j}^2
+\widehat v_{jt}.
$$

For conditionally heteroskedastic proxy errors, replace the first term with

$$
\frac1T\widetilde F_t'
\left[\frac1T\sum_s\widetilde F_s\widetilde F_s'
\widehat\epsilon_{js}^2\right]\widetilde F_t.
$$

The second term remains the factor-estimation contribution. The convergence rate is $\min(\sqrt N,\sqrt T)$, with no relative growth restriction of the form needed for the exact-null simplification. Pointwise 95% intervals are $\widehat\epsilon_{jt}\pm1.96\widehat s_{jt}$. They are not simultaneous bands over all dates. Enlarging only $N$ cannot eliminate coefficient uncertainty when $T$ stays small.

Two scale-free descriptive measures are

$$
NS(j)=\frac{\widehat{\operatorname{Var}}(\widehat\epsilon_j)}
{\widehat{\operatorname{Var}}(\widehat G_j)},\qquad
R^2(j)=\frac{\widehat{\operatorname{Var}}(\widehat G_j)}
{\widehat{\operatorname{Var}}(G_j)}.
$$

For centered OLS using the same sample, residual orthogonality implies $NS=(1-R^2)/R^2$. Thus these communicate the same decomposition in different units. Their interpretation is proxy fit, not the share of an individual stock's variance explained by economic factors. The paper's suggested practical cutoffs are judgments, not theorem-backed universal acceptance thresholds.

## Joint factor spaces and canonical correlations

Individual membership and joint spanning are different questions. Several excellent proxies can all represent nearly the same factor direction. Conversely, a candidate set can contain irrelevant variables yet span the latent factors through an appropriate linear combination.

Given $r$ latent factors and $m$ proxies, calculate sample covariance matrices and the eigenvalues of

$$
S_{FF}^{-1}S_{FG}S_{GG}^{-1}S_{GF}.
$$

The $p=\min(r,m)$ nontrivial eigenvalues are squared canonical correlations $\rho_k^2$. In practice replace $F$ with $\widetilde F$. Numerically, whiten the two covariance matrices and use an SVD of the cross-covariance to avoid a nonsymmetric eigenproblem. This computes the same canonical correlations and is an implementation restatement, not a different estimator.

If $m<r$, the proxies cannot span the entire latent space. If $m\ge r$, complete spanning requires all $r$ canonical correlations to equal one. This does not require every proxy to be an exact factor: extra irrelevant directions in $G$ can receive zero weight. The article's simulation Set 3 illustrates that distinction.

Proposition 3 establishes that estimating $F$ has no first-order effect on canonical-correlation inference when $\sqrt T/N\to0$. This is a different growth condition from the exact datewise test's $\sqrt N/T\to0$. In the iid normal case the displayed standard error for an interior squared canonical correlation is

$$
\operatorname{se}(\widetilde\rho_k^2)
\approx\frac{2\widetilde\rho_k(1-\widetilde\rho_k^2)}{\sqrt T}.
$$

Equation (12) forms normal intervals with this scale; for a single proxy it also gives an interval for $R^2$. These regular normal approximations should not be extrapolated blindly to exactly zero or one, where the scale degenerates, or to repeated canonical roots. In particular, an interval near one is a descriptive approximation rather than a universally valid boundary test of exact spanning.

The source discusses elliptical-distribution kurtosis adjustments and proposes prewhitening finite VARs when factors and proxies are serially dependent. It explicitly phrases the generated-factor extension after VAR fitting as an expectation, not a proved general dependent-data result. Its empirical normal intervals therefore warrant caution for persistent macroeconomic series. This note retains the Gaussian interior formula rather than turning the briefly stated nonnormal extension into an unqualified recipe.

## Simulation design and what it demonstrates

Section 4 generates two iid standard-normal latent factors, independent standard-normal loadings, and independent normal idiosyncratic errors, then standardizes all $x$ and $G$ series. There are 1,000 replications, implemented in Matlab 6.5, with known $r=2$. The reported sample configurations include $(N,T)=(50,50),(100,50),(50,100),(200,100),(100,200)$.

Two candidates are exact: $G_1=F_1+F_2$ and $G_2=F_1$. Candidates 3 and 4 have the same respective signals plus Gaussian noise with standard deviation 0.2 times the signal standard deviation, giving population $NS=0.04$. Candidates 5 and 6 use multiplier 2, giving $NS=4$. Candidate 7 is an independent standard normal, not a zero-variance variable despite the zero signal coefficients in the compact parameter table.

Table 1 reports average datewise exceedance fractions, rejection frequencies of the maximum test, noise ratios, and coverage of measurement-error intervals. With the homogeneous-error estimator and $N=T=50$, exact candidates have $A=0.03$, maximum rejection 0.02–0.03, and $R^2=0.97$. Mildly noisy candidates have $A=0.16$–0.17 and maximum rejection 0.60–0.64. Strongly noisy candidates have maximum rejection one; the unrelated candidate has $R^2=0.04$. At $(200,100)$ the mildly contaminated candidates are always rejected by the maximum test despite $R^2\approx0.96$.

These values show why exactness and usefulness must be separated. They also show conservative size in some finite configurations. Under CS-HAC, exact-case exceedance and rejection frequencies can be near zero, while mild-noise power is notably weaker. The main text does not fully specify the CS-HAC subset rule or all variance settings needed to recreate every panel of Table 1. The heteroskedastic covariance version performs closer to nominal pointwise coverage in its reported panel.

Four joint proxy sets test a mildly noisy pair plus an unrelated variable, a strongly noisy pair plus an unrelated variable, an exact pair plus an unrelated variable, and four unrelated variables. For $(N,T)=(200,100)$, their smallest relevant squared canonical correlations are 0.88, 0.08, 0.99 and 0.02, respectively. The first set's interval is 0.83–0.92; the exact pair's is 0.99–1.00. An irrelevant additional proxy does not prevent joint spanning if the exact factors are already present.

## Empirical construction and results

All applications cover 1960–1996, with subsample comparisons. Candidate financial factors are Market, SMB and HML from the Fama–French data. Market is the value-weighted NYSE/AMEX/Nasdaq return less the one-month Treasury bill return. Macroeconomic proxies include innovations to consumption growth (PCEND), industrial production growth (IP), inflation (PUNEW), a term spread between ten-year government and three-month bill yields, and a risk spread between BAA yields and ten-year government yields. Annual innovation regressions use two autoregressive lags; monthly regressions use six. The consumption candidate is described as the first lag of innovations to annual consumption growth. Exact alignment and vintage information beyond these statements must be recovered from the original data construction, not guessed from the modern series names.

The first panel uses size/book-to-market sorted portfolios from Kenneth French's library. Information criteria select four to six factors; the reported proxy tests use six. There is an internal sample-count inconsistency: the text says 89 portfolios are continuously available, whereas Table 3 reports $N=94$ annually and Table 4 reports $N=95$ for the full monthly sample, reaching 101 in later subsamples. These numbers must be reconciled against original portfolio files before claiming an exact replication.

Annual Table 3, with $T=37$, reports Market/SMB/HML $R^2$ values 0.984/0.971/0.962 and $NS$ values 0.016/0.030/0.039. The market fit interval is 0.974–0.994. Macroeconomic fits are much lower: consumption 0.238, industrial production 0.146, inflation 0.198, term spread 0.249 and risk spread 0.313. High fit does not imply exact membership: Market has $M=4.343$, which exceeds the relevant independent-normal maximum cutoff. The prose's suggestion that the annual market exact null is not rejected is inconsistent with its displayed statistic; this note follows the table and test formula.

At monthly frequency, full-sample portfolio fits decline to 0.973 for Market, 0.926 for SMB and 0.886 for HML. Market's 95% interval is 0.968–0.978. Macroeconomic $R^2$ values are only 0.011–0.075. The first three squared canonical correlations of the full eight-proxy set with the six-dimensional factor space are 0.992, 0.917 and 0.832, while the next three are 0.039, 0.019 and 0.005. The proxies therefore reproduce some strong directions but do not span the complete estimated space. The canonical roots are properties of the set and must not be attributed row by row to individual candidate variables just because the table places them beside those variables.

The individual-stock application retains 190 CRSP firms with uninterrupted data, explicitly exposing the analysis to survivorship bias. It again uses six factors despite criteria choosing four to six. Table 5 gives Market $R^2=0.967$ and $NS=0.034$, SMB 0.603 and 0.660, and HML 0.436 and 1.294. Market's interval is 0.961–0.973; SMB's is 0.545–0.660. Macroeconomic fits range from 0.011 for the term spread to 0.059 for the risk spread. The latter's $NS=15.880$ is hundreds of times Market's, not evidence that it is a comparably good return-factor proxy.

Finally, 150 monthly macroeconomic series from the Stock–Watson dataset cover output, consumption, employment, investment, prices, wages, rates, exchange rates and other financial variables. Unemployment (LHUR) is an additional proxy. In Table 6, full-sample fits are 0.442 for industrial production, 0.463 for the risk spread, 0.353 for unemployment and 0.258 for inflation. The three Fama–French series have fits of only 0.008, 0.019 and 0.010. This does not imply economic independence between markets and macro activity: it is a contemporaneous linear spanning comparison of the particular transformed panels.

Relations vary across periods. Inflation's macro-factor fit falls from 0.290 in 1960–1982 to 0.133 in 1983–1996, while unemployment's rises from 0.325 to 0.542. Industrial production rises from 0.400 to 0.544. Such differences may reflect changing loadings or changing noise composition; the diagnostics do not separately identify those explanations.

## Reimplementation limits and research use

The method is an in-sample statistical audit, with no held-out forecast exercise, portfolio optimization, cost model or return backtest. A faithful implementation must reproduce panel membership, transformations, proxy timing, standardization, factor count, covariance model and sample-specific maximum thresholds before interpreting small p-values. Important missing inputs include exact security and portfolio lists, historical data vintages, complete macro-series transformation codes, and the CS-HAC subset rule.

The most useful operational output is not a single accept/reject flag. It is the combination of factor-space dimension, datewise error paths, approximate fit/noise ratios, and the full canonical spectrum. This separates a redundant but accurate proxy from a new factor direction, exposes episodic proxy failures, and measures the part of a proposed economic interpretation unsupported by the panel. Exact rejections should then be assessed against practical error size and model assumptions, rather than equated automatically with an economically useless factor.

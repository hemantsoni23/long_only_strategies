# Bayesian Estimation of Stochastic Discount Factors

Stephen Gordon, Lucie Samson, and Benoît Carmichael, *Journal of Business & Economic Statistics* 14(4), October 1996, 412–420. Source: [StochasticDiscount_Gordon_1995.pdf](../../Finance/StochasticDiscount_Gordon_1995.pdf), twelve PDF pages: an archive cover, nine article pages, and two linked-reference pages. The filename's 1995 refers neither to the displayed publication year nor to a separate empirical sample.

## Why this matters

A candidate stochastic discount factor can satisfy a mean–standard-deviation bound and still move at the wrong times. This paper develops a Bayesian way to infer a time path of discount factors from observed returns, then compare structural asset-pricing candidates with that inferred path while integrating parameter uncertainty. It complements Hansen–Jagannathan (HJ) moment diagnostics with a temporal-fit diagnostic.

The innovation comes at a price: returns alone do not identify a unique stochastic discount factor. The authors impose a joint lognormal model, constant conditional covariance parameters, priors, and a minimum-variance choice for an unidentified log-discount-factor component. Their inferred path is therefore a model-dependent benchmark, not an observed true pricing kernel. The empirical conclusion—that a market-return-based Epstein–Zin proxy fits temporal fluctuations better than the tested consumption-habit proxies—must be read conditional on that benchmark.

The source provides the main likelihood, sampler structure, priors, and model grids. Several printed expressions require mathematical clarification, particularly a sign in the regression representation, a degenerate covariance boundary, and the normalization of a statistic called a correlation.

## Data and empirical objects

The sample is monthly, January 1969–December 1992, with 288 observations. CRSP NYSE value-weighted returns include capital gains and dividends. Firms are grouped by standard industrial classification into five portfolios: primary industries; manufacturing; transportation and public utilities; wholesale and retail trade; and services including finance, real estate, and insurance.

The risk-free proxy is the secondary-market three-month Treasury-bill series FYGM3 from Citibase, expressed as a monthly return. Nominal returns are deflated using consumption expenditures on nondurable goods and services. Consumption for the structural comparisons is per-capita monthly nondurable-and-service expenditure in constant 1987 dollars. The NYSE value-weighted return proxies the return on market wealth.

An implementer needs the exact SIC ranges, portfolio weighting/reconstitution rules, historical CRSP treatment, bill-yield-to-monthly-return conversion, and consumption-deflator alignment. These are not fully enumerated in the article. Deflating a nominal bill with realized inflation also does not make the resulting real return literally known at the previous date. The theoretical likelihood assumes a known real risk-free return; the empirical proxy introduces an additional approximation that should be documented.

## Joint lognormal specification and pricing restrictions

Let $M_{t+1}>0$ price gross real returns $R_{i,t+1}$ through

$$
E_t[M_{t+1}R_{i,t+1}]=1.
$$

Write $m=\log M$, $r_i=\log R_i$, and suppose

$$
\begin{pmatrix}m_{t+1}\\r_{t+1}\end{pmatrix}\bigg|\mathcal F_t
\sim N\left[\begin{pmatrix}\mu_t\\\eta_t\end{pmatrix},
\begin{pmatrix}\sigma_{mm}&a^\top\\a&\Sigma\end{pmatrix}\right].
$$

Here $a=\operatorname{Cov}_t(r,m)$ is a five-vector and $\Sigma=\operatorname{Var}_t(r)$ a $5\times5$ positive-definite matrix. Covariances are constant; conditional means can move with the risk-free log return $r^f_{t+1}$. The source uses $\sigma_{mr}$ and $\Sigma_{rr}$ for $a$ and $\Sigma$.

Lognormal moments convert the pricing equation into

$$
\mu_t+\eta_{it}+\tfrac12\sigma_{mm}+\tfrac12\Sigma_{ii}+a_i=0.
$$

The risk-free restriction is $\mu_t+\sigma_{mm}/2=-r^f_{t+1}$, so

$$
\eta_{it}=r^f_{t+1}-\tfrac12\Sigma_{ii}-a_i.
$$

Integrating out the unobserved discount factor gives the likelihood

$$
r_{t+1}\mid r^f_{t+1},a,\Sigma
\sim N\left(r^f_{t+1}\mathbf1-\tfrac12\operatorname{diag}\Sigma-a,\Sigma\right).
$$

This identifies $a$ and $\Sigma$ within the distributional model, while $\sigma_{mm}$ drops out of the return likelihood. Negative $a_i$ corresponds to positive expected gross excess return: $E_tR_i/R^f=\exp(-a_i)$. The expected **log** excess return is instead $-a_i-\Sigma_{ii}/2$. These are distinct risk-premium conventions.

The five portfolio returns provide a low-dimensional pricing restriction. Joint lognormality ensures positivity of the constructed discount factor, but it also excludes many conditional tail and regime behaviors. Inferring a path with additional structure is fundamentally different from obtaining an unconditional HJ bound from moments alone.

## A sign correction needed for the Gibbs step

Define $y_{it}=r_{i,t+1}-r^f_{t+1}+\Sigma_{ii}/2$. The likelihood above implies

$$
y_t=-a+u_t,\qquad u_t\sim N(0,\Sigma).
$$

Equation 8 in the source prints a positive $a$ on the right, inconsistent with Equations 5–6. A direct implementation should use the likelihood's minus sign, or explicitly reparameterize $b=-a$ everywhere, including priors and discount-factor reconstruction. Mixing the two signs reverses the inferred risk-premium relationship.

With prior $a\sim N(\tau,D^{-1})$, the conditional posterior under the likelihood-consistent parameterization is

$$
\overline D=D+T\Sigma^{-1},
\qquad \overline\tau=\overline D^{-1}(D\tau-T\Sigma^{-1}\bar y),
\qquad a\mid\Sigma,\text{data}\sim N(\overline\tau,\overline D^{-1}).
$$

This expression is independently derived from the displayed likelihood. The printed posterior's positive sample-mean term corresponds to the alternate sign representation, so it cannot be copied with the original covariance definition unchanged. The article's reported negative posterior covariances under informative priors are consistent with positive premia, but code is needed to determine exactly how the published sampler handled the notation discrepancy.

## Covariance sampling and priors

Covariance elements also enter the mean through $\operatorname{diag}\Sigma/2$. Therefore the covariance conditional is not the ordinary inverse-Wishart update based only on demeaned residual cross-products. The source parameterizes $\Sigma=K^\top K$ with an upper Cholesky root and uses Metropolis–Hastings for its free entries. Up to the declared prior, its likelihood kernel is

$$
|K^\top K|^{-T/2}\exp\left[-\tfrac12\sum_tu_t^\top(K^\top K)^{-1}u_t\right],
$$

where residuals must be recomputed as the covariance changes. Positive-definite matrices require nonsingular Cholesky factors, conventionally with positive diagonal. If a prior is specified on standard deviations/correlations but sampling occurs in Cholesky coordinates, the induced density and change-of-variable Jacobian must be handled consistently. The article does not give every transformation detail, so a naive flat density in different coordinates is not the same prior.

Prior A uses marginal monthly standard deviations distributed around $0.12/\sqrt{12}$ with standard deviation $0.02/\sqrt{12}$, and pairwise correlations around 0.75 with standard deviation 0.1, restricted to valid covariance matrices. Each $a_i$ has prior mean -0.0056 and standard deviation 0.002. These priors reflect beliefs about approximately 12% annual volatility and 6% annual risk premia drawn from presample literature.

Prior B uses a flat covariance-root prior and a diffuse covariance-vector prior constrained to $a_i<0$. Prior C uses flat priors for both $a$ and the covariance root. Flat is parameterization dependent and should not be described as absence of assumptions. The article finds materially different implications under C, which produces positive posterior means for all five $a_i$, hence negative expected gross excess premia within the model.

The main sampler is Metropolis-within-Gibbs with sequential random-walk normal proposals, starting at prior means and using prior-scale proposal innovations. The first 500 draws are discarded and the next 1,000 retained. Visual convergence is reported after roughly 200–300 iterations. Acceptance rates are usually around 0.6, with a minimum around 0.4. Numerical standard errors for most means are below 0.5% of their estimated values using the cited Geweke procedure. This is a report about Monte Carlo precision, not proof of posterior correctness, identification, or convergence from multiple chains. Seeds, all proposal scales in transformed coordinates, and full chain output are absent.

## Reconstructing the discount-factor path

For a parameter draw, the Gaussian conditional is

$$
m_{t+1}\mid r_{t+1},a,\Sigma,\sigma_{mm}
\sim N\left(\mu_t+a^\top\Sigma^{-1}(r_{t+1}-\eta_t),
\sigma_{mm}-a^\top\Sigma^{-1}a\right).
$$

The unidentified variance obeys the Schur-complement restriction $\sigma_{mm}\geq a^\top\Sigma^{-1}a$ for positive semidefiniteness, with strict inequality for a strictly positive-definite joint covariance. The authors choose the smallest possible value rather than place a genuinely dispersed prior on it.

At the exact minimum, the conditional variance is zero and the joint covariance is singular. Thus the phrase “smallest value consistent with positive definiteness” is technically an infimum on the semidefinite boundary. A numerical implementation must either use that degenerate conditional exactly or specify a positive slack. Adding an unspecified small variance changes posterior path uncertainty.

With the exact minimum, each draw gives

$$
m_{t+1}=-r^f_{t+1}-\tfrac12a^\top\Sigma^{-1}a
+a^\top\Sigma^{-1}\left(r_{t+1}-r^f_{t+1}\mathbf1+\tfrac12\operatorname{diag}\Sigma+a\right),
\qquad M_{t+1}=e^{m_{t+1}}.
$$

Posterior dispersion still arises from uncertainty in $a$ and $\Sigma$. It is not arbitrary residual SDF noise. More general pricing kernels can add orthogonal components without changing the observed return restrictions, so this selected path should not be called the uniquely identified economic discount factor.

Table 1's posterior-A covariance-vector means are approximately $(-0.0030,-0.0039,-0.0012,-0.0050,-0.0064)$. The selected log-SDF variance has mean 0.0528 and posterior standard deviation 0.0218. Under B its mean is only 0.0115; under C, 0.0455. Prior sensitivity is economically important, not just a small numerical adjustment.

## What the fitted SDF statistics mean

Figure 1's time series of posterior mean discount factors has sample mean 1.0631 and time-series standard deviation 0.2227. The average pointwise posterior standard deviation is 0.1147. These three quantities summarize different axes of variation: time averages, variation of the posterior-mean path, and uncertainty at each date.

Table 2 instead computes sample moments for each of 1,000 complete posterior paths and then averages those moments:

| Statistic | Prior A | Prior B | Prior C |
|---|---:|---:|---:|
| Mean | 1.0631 | 1.0105 | 1.0982 |
| Standard deviation | 0.2484 | 0.1029 | 0.2240 |
| Skewness | 0.7406 | 0.6209 | 0.9269 |
| Kurtosis | 4.2297 | 5.7855 | 6.7352 |

Posterior-A standard deviations of these sample statistics are 0.0346, 0.0608, 0.2453, and 1.4966. In particular, 0.2484 is not in conflict with 0.2227: the mean path's sample standard deviation differs from the posterior mean of path standard deviations. Positive skew is partly inherited from exponentiating a Gaussian log factor, so it is not an unrestricted empirical discovery.

Table 3 gives lag-one autocorrelation 0.1525 with posterior standard deviation 0.0341 under A, versus 0.0592 with 0.0823 under B. The authors find modest persistence under informative priors but no comparably clear pattern under B. That sensitivity limits claims about an objectively recovered persistent pricing kernel. All these paths are inferred retrospectively from observed contemporaneous returns and full-sample parameters, not forecasts available before returns occur.

## HJ bounds with parameter uncertainty

For the HJ exercise the source uses a separate model of iid lognormal **returns**, without imposing the conditional pricing specification above. A normal prior for their log means and an inverse-Wishart covariance prior permit a conjugate Gibbs sampler. It retains 2,000 draws after a 100-draw burn-in; the prior covariance degrees of freedom are thirty, roughly one tenth of the sample size. The prior log-return means use an annual 7% convention converted to months.

For gross-return mean vector $\mu_R$ and covariance $\Sigma_R$, the familiar unrestricted-SDF variance lower bound at proposed SDF mean $m$ is

$$
\sigma_{\rm HJ}^2(m)=(\mathbf1-m\mu_R)^\top\Sigma_R^{-1}(\mathbf1-m\mu_R).
$$

Moments must be transformed from log returns to gross-return levels before using this formula. For a multivariate lognormal, $E[R_i]=\exp(\eta_i+\Omega_{ii}/2)$ and $\operatorname{Cov}(R_i,R_j)=E[R_i]E[R_j](e^{\Omega_{ij}}-1)$. Positivity restrictions on an SDF can impose additional constraints beyond this basic moment bound.

For a fixed candidate path $X$, compute its mean $\bar X$ and standard deviation $s_X$. The reported probability $\widehat P$ is the fraction of posterior return-moment draws for which $s_X>\sigma_{\rm HJ}(\bar X)$. It measures uncertainty in the estimated bound conditional on a supplied candidate path. It is not the posterior probability that the entire structural asset-pricing model is true, nor an out-of-sample likelihood score. Candidate parameter search on the same data is another reason to avoid that interpretation.

## Structural candidates and parameter grids

The discount factor called CAPM here is the particular proxy $1/R_{M,t+1}$. It should not be conflated with every possible linear SDF representation of the static CAPM. With consumption growth $g_t=c_t/c_{t-1}$, power utility gives $M_{t+1}=\beta g_{t+1}^{-\gamma}$; the Abel catching-up specification is $\beta g_{t+1}^{-\gamma}g_t^{\gamma-1}$. The time preference parameter $\beta$ corresponds to 3% annually, converted to the monthly period.

The Epstein–Zin candidate uses

$$
M_{t+1}=[\beta g_{t+1}^{\rho-1}]^{\alpha/\rho}
(1/R_{M,t+1})^{(\rho-\alpha)/\rho},
\qquad \delta=(1-\rho)^{-1}.
$$

The search varies $\alpha$ from -0.9 to 0.9 in steps of 0.2 and elasticity $\delta$ from 0.05 to 0.95 in steps of 0.05. The market return is a proxy for total wealth return, an acknowledged approximation. Seven grid combinations exceed HJ-pass probability one half.

For internal habit, the candidate is

$$
M_{t+1}=\beta g_t^{-\gamma}
\frac{(g_{t+1}-\lambda)^{-\gamma}-\beta\lambda g_{t+1}^{-\gamma}E_{t+1}(g_{t+2}-\lambda)^{-\gamma}}
{(g_t-\lambda)^{-\gamma}-\beta\lambda g_t^{-\gamma}E_t(g_{t+1}-\lambda)^{-\gamma}}.
$$

Consumption growth is assumed iid so the expectations are replaced by sample averages. This is not an estimated time-varying conditional consumption model. The grid uses $\lambda=0.1,\ldots,0.7$ in steps of 0.1 and $\gamma=2,4,\ldots,20$. Positivity and finite fractional powers require the relevant consumption-surplus and marginal-utility terms to be admissible; these should be checked in a numerical implementation.

The reciprocal-market proxy has HJ-pass probability about 0.02. Power utility gives less than 0.001 for $\gamma<100$, and the catching-up model less than 0.001 for $\gamma<50$. These are results for the displayed sample and candidate construction, not universal rejections of all CAPM or habit formulations.

## Temporal fit distinguishes candidates with similar moment fit

The HJ-compatible Epstein–Zin examples have mean SDF near one and standard deviations around 0.15–0.19. For $\alpha=0.3,\delta=0.90$, the mean is 0.9971, standard deviation 0.1861, and HJ-pass probability 0.689. Other accepted combinations have probabilities 0.523–0.639. The three accepted habit cases are $(\lambda,\gamma)=(0.4,20),(0.5,10),(0.5,12)$, with probabilities 0.622, 0.527, and 0.577.

For each posterior benchmark path, the source compares correlation with a candidate path and root mean squared difference, then averages these diagnostics across draws. The printed formula called a correlation omits division by the two standard deviations. That omission is substantive: reported values around 0.45 cannot be raw covariances when both series' standard deviations are around 0.2. Reproducing the stated correlation interpretation therefore requires the usual normalization; the exact original code is needed to settle the display discrepancy.

Reported Epstein–Zin correlations are approximately 0.446–0.450, with RMS differences about 0.237–0.250. For the three habit cases the correlations are only 0.0563, 0.0512, and 0.0501, with RMS differences 0.3201, 0.2942, and 0.3101. Raising habit-induced volatility enough to meet HJ bounds does not align that volatility with the return-implied benchmark path.

The correlation between log SDF and negative log consumption growth is only 0.0980 under A and 0.0471 under B. The reciprocal-market candidate has correlation 0.4575 and RMS difference 0.2412 despite its low HJ-pass probability. This is the paper's central methodological demonstration: matching first two moments and matching temporal fluctuations are different criteria, and either can favor a model that fails the other.

## Reproduction boundaries and takeaways

A rigorous reconstruction should begin from the pricing-restricted likelihood, resolve its regression sign convention, and implement both parameter priors and the covariance-coordinate density consistently. Declare whether the unidentified variance is set on the exact semidefinite boundary or given slack. Preserve whole posterior paths for moment and fit calculations; averaging a path first is not interchangeable with averaging nonlinear diagnostics afterward.

For the HJ exercise, run the separate return-moment sampler, transform lognormal moments correctly, and keep the pass probability distinct from a model posterior. Reproduce the candidate grids, consumption timing, iid expectation approximation, and normalized temporal correlation. Exact replication remains limited by missing data identifiers and adjustment conventions, some prior/Jacobian details, sampler code and seeds, and the printed sign/normalization inconsistencies.

The paper's useful conclusion is that a volatility-bound pass is insufficient evidence of a good asset-pricing explanation. Temporal fit provides an additional diagnostic, with uncertainty propagated through posterior draws. Its benchmark remains conditional on lognormality, priors, aggregation, and a minimum-variance SDF selection. The reported preference for market-return-based candidates is informative within that framework; it is not recovery of a unique true discount factor or a complete Bayesian model-selection result.

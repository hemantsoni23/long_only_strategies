# The empirical properties of large covariance matrices

Gilles Zumbach, RiskMetrics Group. Working paper dated January 14, 2009, SSRN abstract 1346412. The library basename contains 2010, but this note summarizes the dated draft supplied, not an assumed later version.

Source: [LargeCovarianceMatrix_Zumbach_2010.pdf](../../Finance/LargeCovarianceMatrix_Zumbach_2010.pdf), 21 pages. References below are to PDF/printed pages, which coincide.

## Why this matters

A nearly unchanged covariance eigenvalue spectrum does not imply a nearly unchanged risk model. The associated eigenspaces can move substantially, including well below the first few components. Zumbach makes this distinction empirically useful by analyzing averages of orthogonal projectors, their dispersion, and their time dependence alongside the usual eigenvalues.

The practical motivation is covariance inversion. A large empirical matrix can be mathematically nonsingular yet numerically and statistically unstable to invert because its eigenvalues become very small. A factor model or spectral truncation addresses this problem by retaining some directions and discarding others. The paper asks whether the observed spectrum supplies a natural boundary separating a stable signal subspace from noise. In three universes it finds a gradual transition, rather than a conspicuous cutoff, and considerable movement in the estimated subspaces.

This is a descriptive empirical study, not a new optimal shrinkage estimator or an out-of-sample portfolio comparison. Its useful output is a collection of diagnostics and evidence about the matrices to which regularization will be applied. The stronger claims that separate volatility/correlation estimators are unnecessary, or that truncation necessarily gives poor results, exceed what the displayed diagnostics alone establish. The paper motivates those views but leaves comparative regularization and process-inference performance to subsequent work.

## Returns, transformations, and covariance estimator

For each asset or risk-factor time series, define a mapped price $x_i(t)$ and its daily increment

$$
r_i(t)=x_i(t)-x_i(t-\delta t).
$$

For equities, equity indexes, currencies, and commodities, $x_i(t)=\log p_i(t)$. For an interest rate $R_i(t)$ at fixed maturity, the footnote on p. 3 specifies

$$
x_i(t)=\log\left(1+\frac{R_i(t)}{R_0}\right),\qquad R_0=4\%.
$$

This is not a bond total return or simply a basis-point change in the yield. Rates and $R_0$ must be in the same units. The transformation is only defined when $1+R/R_0>0$, a relevant boundary if extending the dataset outside the sample. Its purpose is to temper dependence of rate volatility on the rate level.

Write the $N$-vector of increments as $r_t$. The effective covariance is an uncentered weighted second-moment estimator:

$$
\Sigma_t=\sum_{i=0}^{L-1}w_i r_{t-i}r_{t-i}',\qquad w_i\geq0,\quad\sum_iw_i=1.
$$

This notation uses an explicit observation count $L$. The paper writes a sum from zero through $i_{max}$ while describing $i_{max}=260$ as 260 historical business days; that leaves an endpoint convention to settle in code. There is no rolling sample-mean subtraction in the displayed estimator. At daily frequency this is a common approximation, but centering would change rank and numerical values and should not be added invisibly.

The main specification uses a slowly decaying long-memory kernel. Its qualitative form is proportional to $1-\log(i\delta t)/\log\tau_0$, with a characteristic parameter of approximately six years, and the empirical history is truncated at about one business year. This is an asymptotic shape description, not an executable formula at $i=0$. The exact recursion and parameter settings are delegated to Zumbach's RiskMetrics 2006 methodology. The exponential comparison on p. 3 also prints a positive exponent while describing decay; the decaying convention is $\mu^i=\exp(-i\delta t/\tau)$ with $0<\mu<1$.

The referenced [RiskMetrics 2006 methodology](https://www.msci.com/resources/research/technical_documentation/RM2006.pdf) describes a mixture of exponential variance filters on geometrically spaced time scales. A primary-source retrieval located that document, but the full file exceeded the browser extraction limit and local download was unavailable. Thus the precise kernel initialization and truncation convention are not claimed recovered here. In a replication, retain the actual normalized weight vector as an input artifact rather than substituting the approximate logarithmic expression.

The correlation matrix is obtained from the same covariance estimate:

$$
D_t=\operatorname{diag}(\Sigma_t),\qquad C_t=D_t^{-1/2}\Sigma_tD_t^{-1/2}.
$$

Positive diagonal entries are required. The study compares the spectrum and subspaces of $\Sigma_t$ and $C_t$; it does not estimate correlations on a separate historical window. Covariance eigenvectors depend on variable units and the mapped-price choices, whereas correlation eigenvectors remove contemporaneous marginal scale. A direction dominated by one volatile short-term rate is therefore not necessarily the direction with the largest economic capital exposure.

## Data and the experiment

Section 3 describes three panels, with daily histories from January 1, 1999 to January 1, 2008, reported as 2,515 observations. The matrix analysis begins January 1, 2000, reserving approximately 260 business days for initialization, and ends January 1, 2008. This includes the early subprime episode but not the major late-2008 crisis.

| Panel | Reported composition | Intended dimension |
|---|---|---:|
| ICM, International Capital Market | 19 commodities, 78 FX rates, 52 equity indexes, 127 interest rates, 54 stocks from the US, France, and Switzerland | 330 |
| G10 | 5 commodities, 6 FX rates, 13 equity indexes, 31 rates | 55 |
| USA | S&P 500 and Nasdaq indexes, 8 government/swap rates, 44 large-company stocks | 54 |

The ICM paragraph says 340 series, but its categories sum to 330 and the abstract and introduction say 330. The note therefore uses 330 as the intended dimension while preserving that discrepancy. Instrument identifiers, exact contracts and rolls, selected exchange rates, corporate-action adjustments, missing observations, holiday alignment, and the original data file are not provided. The stated 2,515-day count is also not enough to reconstruct the trading calendar.

FX observations are snapshots at a common GMT time, while other series use their market closes. The international panels are therefore asynchronous. The USA panel is described as synchronous at the US close and shows qualitatively similar results. This comparison supports robustness of the broad picture, but it does not quantify or eliminate asynchronous-trading bias in individual covariance elements.

There is no training/test division beyond the warm-up history. Matrices are estimated each day from past data, but the reported averages, density plots, and persistence measures summarize the analysis sample. There are no optimized portfolio weights, expected-return forecasts, rebalancing rules, fees, transaction costs, or realized investment-performance statistics in this paper.

## Spectra and spectral densities

At each date diagonalize the symmetric matrix:

$$
\Sigma_t=\sum_{\alpha=1}^{N}e_{\alpha t}v_{\alpha t}v_{\alpha t}',\qquad e_{1t}\geq\cdots\geq e_{Nt}\geq0.
$$

The eigenvectors are orthonormal. The mean spectrum is the geometric, not arithmetic, time average at each ordered rank:

$$
\bar e_\alpha^{geo}=\exp\left(\frac1T\sum_t\log e_{\alpha t}\right).
$$

Sorting is redone at every date. A rank-specific eigenvalue series is not the variance of one permanently identified economic factor. Near eigenvalue crossings, the economic composition of the vector at that rank can change.

The spectral density in a bin centered at $e$ with half-width $\Delta$ is

$$
\widehat\rho(e)=\frac{1}{2\Delta NT}\sum_{t=1}^{T}\sum_{\alpha=1}^{N}\mathbf1\{e-\Delta<e_{\alpha t}<e+\Delta\}.
$$

It pools dates and eigenvalues. With disjoint bins spanning the full support, bin probabilities sum to one. If logarithmically spaced bins are used for a log-axis plot, divide counts by the actual linear eigenvalue-bin widths when estimating density with respect to $de$; otherwise one estimates a density in log eigenvalue instead. The paper does not supply a full binning specification.

For $N>L$, the rank of an uncentered covariance is at most $L$. Zero eigenvalues then occur by construction; they are not evidence that the underlying economic covariance is singular. Geometric means cannot be computed over exact zeros. Figure 5 uses rank normalized by $N_{pos}$, the number of positive eigenvalues, whereas several equations use $N$. Reproduction must specify a numerical positivity tolerance, treatment of roundoff-negative eigenvalues, and whether the plotted positive spectral density is renormalized after excluding a zero atom. These conventions are not fully stated.

The correlation matrix obeys $\operatorname{tr}C=N$, so its eigenvalues sum to $N$ and lie between zero and $N$. A rank-one system of perfectly positively correlated standardized returns attains $e_1=N$. The Figure 3 caption refers to $N_{pos}$ as the maximum; the mathematical upper bound for an $N$-variable correlation matrix is $N$, regardless of sample rank. This distinction matters for the singular ICM panel.

## What the eigenvalues show

Figures 1–2 plot the covariance eigenvalues through time. Figure 1 samples every tenth rank for ICM and every fifth for G10 and USA; Figure 2 displays the leading eleven eigenvalues. The deep spectrum moves mainly through a slow common scale, whereas roughly the top three to ten eigenvalues have much stronger and more individual dynamics. September 2001 and the onset of the subprime episode in August 2007 affect more of the spectrum than ordinary fluctuations.

The largest ICM eigenvalue is not a universal equity-market factor. The paper links a major 2001 episode to the Argentine currency crisis and emphasizes single-series or regional-rate events. For G10, the leading direction often contains equity indexes but major peaks also reflect natural gas and short-term euro rates. In the USA panel the equity market dominates more consistently, with individual-stock and sector episodes and a later role for rates. These are interpretations of inspected loadings, not a formal event-study identification design.

Figure 3 shows a more stable correlation spectrum, although approximately three to five leading eigenvalues still exhibit distinct dynamics. Comparing covariance and correlation plots suggests similar characteristic fluctuation horizons, on the order of a month for some prominent movements. This challenges a literally constant correlation matrix for these data. It does not by itself estimate an optimal correlation forecast horizon or show that all entries share one decay rate.

For covariance, the paper proposes the descriptive rank-spectrum approximation

$$
x=\frac12-\frac\alpha N,\qquad \log e_\alpha=\log e_{N/2}+\frac{ax}{1-(2x/b)^4}.
$$

Here $a$ governs the central slope and $b$ controls curvature toward the ends. The paper does not report a complete table of fitted $(a,b)$ values, confidence intervals, or an objective function for their estimation. In the central region the curvature term is small, yielding $e_\alpha\propto\exp(-a\alpha/N)$. This is an empirical shape approximation, not a claimed population eigenvalue law.

The density relation follows from counting eigenvalues above a threshold:

$$
\alpha(e)=N\int_e^{e_{max}}\rho(u)\,du,\qquad \rho(e)=-\frac1N\frac{d\alpha}{de}.
$$

For the central exponential rank curve, this gives $\rho(e)\approx1/(ae)$. Figure 6 overlays $0.1/e$, which visually describes the middle density over roughly two to three orders of magnitude. Such a reciprocal density cannot be normalized on all positive values; the approximation requires finite cutoffs and curvature in the tails. Its importance is the abundance of small positive eigenvalues, not a scale-free distribution extending to zero without qualification.

## Random-matrix comparison and its limits

The comparison distribution is the Marchenko–Pastur law for an equally weighted sample covariance of independent, unit-variance variables. With $q=N/L$ and $e_\pm=(1\pm\sqrt q)^2$, its continuous part is

$$
\rho_{MP}(e)=\frac{\sqrt{(e_+-e)(e-e_-)}}{2\pi qe},\qquad e\in[e_-,e_+].
$$

For $q>1$, a complete probability distribution also includes a point mass $1-1/q$ at zero. The paper prints only the continuous expression. Figure 4 overlays a curve with $q=0.93$, chosen for visual overall fit; it is not the literal $330/260$, $55/260$, or $54/260$ sample-dimension ratio.

The empirical correlation densities have broadly similar shapes across the three universes, although their literal dimension/history ratios differ by approximately sixfold. No visually sharp transition separates a noise bulk from large outlying modes. The reference curve does not fit the lower spectrum particularly well either.

The paper emphasizes non-Gaussian returns, unequal weights, and the mismatch between finite historical kernels and asymptotic sample regimes. More generally, the null also lacks the actual cross-sectional covariance and time dependence. Non-Gaussianity alone should not be interpreted as automatically invalidating every random-matrix approximation: appropriate universality results can permit non-Gaussian observations. The defensible conclusion from this experiment is that the particular fitted independent, equally weighted null does not supply an empirically obvious cutoff. Absence of a visible gap is not a proof that no useful factor dimension or shrinkage model exists.

## Mean projectors: separating eigenvector motion from eigenvalue motion

Averaging signed eigenvectors is unreliable because $v$ and $-v$ are equivalent. The sign-invariant rank-$k$ projector is

$$
P_{k,t}=\sum_{\alpha=1}^{k}v_{\alpha t}v_{\alpha t}',\qquad \bar P_k=\frac1T\sum_tP_{k,t}.
$$

Rotations within the retained subspace also leave $P_{k,t}$ unchanged. Crossings strictly within that subspace therefore do not create spurious changes, although crossings at the $k/(k+1)$ boundary still change the selected subspace. Near-ties across that boundary can create large estimation noise and should not automatically be interpreted as economic rotation.

Every instantaneous projector is symmetric and idempotent, with trace $k$. Its average has trace $k$ and eigenvalues between zero and one, but generally is not idempotent. The paper says that rank is preserved by averaging; strictly, trace is preserved, while the average can have rank greater than $k$ and even full rank. A fixed subspace gives $k$ unit eigenvalues and $N-k$ zeros. Completely isotropic exploration gives $\bar P_k=(k/N)I$.

Figure 7 plots eigenvalues of $\bar P_k$ over a range of $k$. Rather than a crisp block of stable directions separated from unstable ones, the curves decline gradually. The authors identify bends near ranks two and seven for ICM, two and six for G10, and a weaker feature around three to four for USA. These are visual descriptions, not estimated change-points with uncertainty bands.

The economically interpreted mean-projector directions again depend on the universe. G10's first direction is almost entirely gas futures; a subsequent direction is broadly long currencies and commodities and short stocks and rates. USA's first direction loads positively on equities, the second contrasts technology and energy, and the third has an approximately 0.9 loading on Apple. ICM's early directions prominently involve overnight Russian, Croatian, and Slovak rates, while its broad global-equity direction appears later. These loading magnitudes are vector coordinates under the paper's normalization, not dollar portfolio weights or recommended trades.

## Fluctuation index and persistence

The projector fluctuation statistic is

$$
\gamma_k=1-\frac1k\operatorname{tr}(\bar P_k^2).
$$

Because $P_{k,t}^2=P_{k,t}$, this also equals the average squared Frobenius deviation from the mean, divided by $k$:

$$
\gamma_k=\frac{1}{kT}\sum_t\|P_{k,t}-\bar P_k\|_F^2.
$$

The second identity is a direct derivation clarifying the measure. The minimum is zero for a fixed subspace. Since the eigenvalues of $\bar P_k$ sum to $k$, Cauchy–Schwarz implies $\operatorname{tr}(\bar P_k^2)\geq k^2/N$, giving the maximum $1-k/N$. The displayed relative fluctuation is $\gamma_k/(1-k/N)$; it is undefined at $k=N$, where both numerator and denominator vanish.

Figure 8 reports relative fluctuations typically at least about 40% of the isotropic upper bound. The USA covariance curve rises toward one at larger ranks; some low-rank correlation subspaces are more stable than their covariance counterparts. ICM's covariance curve has a low-rank local stability feature around rank eight, while USA's minimum is at rank one. These are descriptive sample statistics without null distributions or bootstrap intervals. Large values combine genuine movement with sampling uncertainty in estimated eigenspaces.

To study persistence without building in the long-memory estimation kernel, Section 9 recomputes matrices with a **21-observation equal-weight window**, and checks 42 as a sensitivity exercise. This change is essential. Using the original long-memory weights would mechanically create autocorrelation in overlapping estimates and obscure the question.

For a symmetric matrix series $A_t$, the scalar lagged correlation is

$$
\rho_A(\tau)=\frac{\operatorname{tr}E[(A_t-\bar A)(A_{t+\tau}-\bar A)]}{\operatorname{tr}E[(A_t-\bar A)^2]}.
$$

It is a Frobenius-inner-product correlation of the entire centered matrix series, not the average of separately normalized entrywise correlations. Apply it to covariance matrices, correlation matrices, and projectors of varying rank. In code, use only available time pairs at each lag and document whether lag-dependent or full-sample means and denominators are used; the paper does not enumerate every finite-sample convention.

Figure 9, for USA, shows a steep initial decline through approximately 21 days, attributable to the overlap of the estimation windows. Beyond that horizon, covariance dependence decays slowly and remains approximately 20% at six months. The correlation-matrix curve has similar shape but a lower level, around 10% near the far end of the displayed range. Projector persistence is strongest for the leading ranks and weaker deeper in the spectrum. The paper reports similar qualitative findings for the other two universes and no material change at the 42-day window, without displaying a complete set of alternative plots.

## What can be implemented, and what remains unverified

The diagnostic pipeline is straightforward once the data and weights are fixed. Transform prices and rates; compute the weighted second-moment matrix and its correlation normalization; sort eigenvalues daily; record spectra and density bins; construct projectors over an explicit rank grid; average them and diagonalize those averages; calculate the fluctuation index; then repeat the lag-correlation exercise using compact 21- and 42-day windows. Check positive semidefiniteness, trace identities, projector idempotence, and bounds on the fluctuation statistic. Keep zero eigenvalues separate from small positive ones and avoid including arbitrary null-space directions in an allegedly informative projector.

The paper's broad results suggest that covariance validation should inspect eigenspaces as well as variance explained. They also explain why an unregularized inverse is hazardous: $\Sigma^{-1}$ weights direction $v_\alpha$ by $1/e_\alpha$, so small estimation errors in tiny eigenvalues or their vectors can produce large changes in optimized exposures. That mechanism is exact linear algebra. The paper does not measure resulting turnover, allocation losses, or forecast-risk improvements, so those outcomes require separate validation.

Several limitations govern interpretation. Three particular universes over 2000–2007 do not establish a universal law. No confidence intervals distinguish structural eigenspace movement from estimation noise. A rolling-window projector can be unstable even under a fixed population covariance when eigenvalue gaps are small. The use of asynchronous international closes, uneven economic representation, and mapped-rate scales complicates cross-universe comparisons. A covariance spectral shape depends on the units of the input variables; a correlation shape depends on the volatility estimates used for normalization.

Exact numerical replication remains blocked by the missing instrument list, original daily panel, kernel recursion/initialization, binning and eigenvalue-tolerance conventions, and inconsistent ICM size and window endpoint descriptions. Those omissions do not prevent reproducing the methodology on a clearly documented new panel. They do prevent claiming that a newly generated curve is the paper's original numerical result. The core contribution is a disciplined way to ask whether apparently stable risk spectra hide moving risk directions, while keeping regularization choice an empirical forecasting question.

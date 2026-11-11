# Market Liquidity as Dynamic Factors

Marc Hallin, Charles Mathias, Hugues Pirotte, and David Veredas. *Journal of Econometrics* 163 (2011), 42–50. Available online 12 November 2010. DOI: 10.1016/j.jeconom.2010.11.005.

Source: [DynamicFactorModelsLiquidity_Hallin_2011.pdf](../../Finance/DynamicFactorModelsLiquidity_Hallin_2011.pdf). All nine pages were read, including the seven figures and descriptive-statistics table. References below use printed journal pages.

## Why this matters

Bid–ask spreads and traded volume measure different aspects of liquidity. A spread describes the cost of immediate execution, while realized volume describes how much actually traded. Their aggregate movements need not coincide contemporaneously, and individual stocks can react to the same market disturbance at different speeds. Consequently, an average spread or a static principal component can be a poor representation of the information shared across liquidity measures.

The paper's contribution is to define market liquidity through the dynamic common information in a large panel and test whether spreads and volumes share that information. It applies the generalized dynamic factor model, or GDFM, with a block structure: one block contains spreads and the other volumes. Each block and their joint panel select one dynamic factor. Within the model's assumptions, that result implies that the two blocks share a single common innovation space. The authors interpret its innovation as a market liquidity shock.

The finding is narrower than equivalence of spreads and volumes. Their responses to the shared shock differ, and most individual-series variation remains idiosyncratic. The average common variance share is 12% for relative spreads and 18% for dollar volume. A researcher interested in systematic liquidity risk could therefore use either block to identify the common space in this sample, but could not substitute one raw measure for the other when predicting stock-specific execution conditions.

This is an identification and descriptive decomposition exercise. It does not estimate a liquidity risk premium, an optimal trading schedule, a transaction-cost function, or an out-of-sample liquidity forecasting gain. Its empirical environment is a selected sample of large US stocks during 2004–2006, a period chosen to avoid a liquidity crisis. Those boundaries are central to interpreting the result.

## Observable measures, universe, and sample construction

The panel contains 426 S&P 500 constituents listed from Monday 5 January 2004 through Friday 29 December 2006 and still listed in November 2008. The final requirement uses information after the measurement sample and introduces survivor selection. It is not a historical point-in-time S&P 500 universe that includes all firms entering, leaving, or disappearing during the period.

For each stock $i$ and date $t$, Reuters 3000 Xtra supplies the daily closing best bid, closing best ask, and realized dollar volume. Define the midquote and relative spread as

$$
M_{it}=\frac{A_{it}+B_{it}}{2},\qquad
SPR_{it}=\frac{A_{it}-B_{it}}{M_{it}}.
$$

The spread is a pre-trade measure of displayed tightness at the closing observation. It is not an effective spread calculated from actual transaction prices. The second series, $VOL_{it}$, is realized dollar volume, a post-trade measure of transacted depth. It is not available order-book depth, and it does not measure how much could have traded without moving the price. These conceptual differences motivate examining commonality rather than assuming the measures are interchangeable.

The source reports the following cleaning sequence. Remove dates on which trading in more than 80% of stocks was suspended. Remove any date on which at least one stock has a negative spread. Interpolate missing spread or volume observations. This leaves $T=747$ dates. Multiply relative spreads by $10^3$ and dollar volumes by $10^{-6}$ to avoid numerical problems caused by their very different raw magnitudes.

The paper does not specify the interpolation rule, maximum interpolated gap, exact list of removed dates, detailed handling of corporate actions, or the retained stock identifiers. It also does not clearly describe whether each series is subsequently standardized by its own variance before spectral estimation. The documented common rescalings of the two measures should not be silently replaced by individual z-scores: that changes the finite-panel spectral geometry and can change estimated common components. Centering is necessary to implement the zero-mean representation used in the theory; the empirical centering convention is not described in detail.

Unit-root and weekly-seasonality checks support the authors' chosen working specification. Phillips–Perron tests reject a unit root in all spread and volume series at the 1% significance level. Fewer than 5% of series show significant weekly seasonality. Detailed test results, bandwidths, and other settings are available only on request. Unit-root rejection is evidence against a particular nonstationary alternative, not a proof of second-order stationarity, stable cross-sectional loadings, or absence of breaks. The authors explicitly do not rule out stationary long memory.

## The dynamic factor representation

Let $x_{it}$ stand for a centered liquidity series. Consider the double-indexed process $\{x_{it}:i\in\mathbb N,t\in\mathbb Z\}$, and stack its first $n$ coordinates into $x_{n,t}$. Both the number of series and the time-series length are large in the underlying asymptotics. Each coordinate is second-order stationary with a finite spectral density; the paper assumes its diagonal spectral entry is uniformly bounded over frequencies for that coordinate.

Write $\Sigma_n(\omega)$ for the spectral density matrix and order its eigenvalues as $\lambda_{n,1}(\omega)\geq\cdots\geq\lambda_{n,n}(\omega)$. The defining separation is that a finite number $q$ of eigenvalues diverge as the panel grows, whereas the remaining eigenvalues stay bounded, almost everywhere in frequency. Under the referenced representation theorem,

$$
x_{it}=\chi_{it}+\xi_{it},\qquad
\chi_{it}=\sum_{j=1}^{q}B_{ij}(L)u_{jt},
$$

where $u_t$ is a $q$-dimensional orthonormal white-noise process and each loading filter is square summable. The common and idiosyncratic components are orthogonal at every lead and lag:

$$
\operatorname{Cov}(\chi_{it},\xi_{js})=0
\quad\text{for every }i,j,t,s.
$$

This permits serial dependence in both components. It also permits weak residual cross-sectional dependence, provided it does not create additional diverging spectral eigenvalues. The paper describes idiosyncratic dependence using finite groups of related stocks, a useful example rather than the only possible weak-dependence pattern. A dense collection of sufficiently small residual correlations can also be compatible with a bounded residual spectrum.

The decomposition into $\chi$ and $\xi$ is unique in the infinite-panel representation. The shock coordinates and loading filters are not unique without further normalizations. In particular, recovering one common dynamic dimension does not identify a unique sign, scale convention, or structural economic cause. The authors associate market liquidity shocks with innovations in the common information space, that is, an orthonormal innovation process generating the same current-and-past common information. This distinguishes the fundamental innovation from an arbitrary filtered factor coordinate.

For a given stock, orthogonality implies the exact variance decomposition

$$
\operatorname{Var}(x_{it})
=\operatorname{Var}(\chi_{it})+\operatorname{Var}(\xi_{it}).
$$

Define its common share $s_i=\operatorname{Var}(\chi_{it})/\operatorname{Var}(x_{it})$. This is an unconditional variance share. It is not a conditional forecast-error decomposition, an asset-pricing loading, or an estimate of how much of a specific trade's implementation shortfall is caused by market liquidity.

The dynamic dimension $q$ counts primitive common innovations. It need not equal the number of contemporaneous factors needed in a static representation. Heterogeneous distributed responses can require many static components even when only one dynamic shock is present. This is why the question “Do spread and volume have one common factor?” must be asked using the model's dynamic definition rather than by inspecting only the largest eigenvalue of a contemporaneous covariance matrix.

## Comparing the two common spaces

Let the spread and volume blocks be

$$
SPR_{n,t}=(SPR_{1t},\ldots,SPR_{nt})',\qquad
VOL_{n,t}=(VOL_{1t},\ldots,VOL_{nt})',
$$

and let the joint vector be $LIQ_{2n,t}=(SPR_{n,t}',VOL_{n,t}')'$. The separate panels have 426 series each; the joint panel has 852. Their time index and cleaning mask must agree for a coherent comparison.

The block method distinguishes information common to both blocks, information pervasive only in one block, and information idiosyncratic to both. Under the strong block structure required for orthogonal decomposition, an individual series can be written schematically as

$$
x_{it}=\phi_{it}+\psi_{it}+\nu_{it}+\xi_{it}.
$$

For a spread series, $\phi$ lies in the spread-common and volume-common space; $\psi$ is spread-common but volume-idiosyncratic; $\nu$ is spread-idiosyncratic but volume-common; and $\xi$ is idiosyncratic to both. The corresponding labels reverse appropriately for a volume series. Thus “weakly common” and “weakly idiosyncratic” refer to a component's status across blocks, not merely to a small coefficient in a regression. Figure 1 and Equation (5), p. 45, describe this geometry.

The empirically selected case is especially simple:

$$
q_{SPR}=q_{VOL}=q_{LIQ}=1.
$$

Using the referenced block result, each block's nonzero common information must then coincide with the one-dimensional dynamic common information of the joint panel. There is no additional dynamic common direction unique to either block. The weakly common and weakly idiosyncratic pieces disappear, leaving

$$
SPR_{it}=\phi_{SPR,i,t}+\xi_{SPR,i,t},\qquad
VOL_{it}=\phi_{VOL,i,t}+\xi_{VOL,i,t}.
$$

This conclusion depends on identifying the dimensions correctly and on the block representation conditions. In a finite noisy sample, three selections of one are not a proof that every possible additional weak factor is absent. A sector-specific liquidity disturbance could remain in the idiosyncratic component if its cross-sectional importance stays limited, or could be too weak to be selected. The paper's suggestion of market homogeneity should be read with those qualifications.

Even when the spaces coincide, response filters need not. With one innovation $u_t$, it is entirely possible that $\phi_{SPR,i,t}=B_{SPR,i}(L)u_t$ and $\phi_{VOL,i,t}=B_{VOL,i}(L)u_t$ exhibit different persistence and lead–lag behavior. The result concerns common information after appropriate dynamic filtering, not equality of daily levels or contemporaneous correlation.

## Dimension selection and reconstructing the components

The authors use the Hallin–Liška information criterion, specifically its $IC_2$ logarithmic version with penalty $p_1(n,T)$ from the cited 2007 paper. Its penalty is multiplied by a positive tuning constant $c$. For a grid of increasing panel sizes and/or time spans $(n_\ell,T_\ell)$, $\ell=1,\ldots,L$, estimate a factor count $q_\ell(c)$ for each $c$ and each grid point.

The diagnostic plot contains the empirical variance

$$
V(c)=\frac1L\sum_{\ell=1}^{L}
\left(q_\ell(c)-\overline q(c)\right)^2,
\qquad
\overline q(c)=\frac1L\sum_{\ell=1}^{L}q_\ell(c),
$$

and the count selected for the largest panel, $q_L(c)$. Choose $c$ in the second stable interval, moving from small to large $c$, on which $V(c)=0$, and read the corresponding $q_L(c)$. This avoids the initial stable plateau associated with an insufficient penalty and the maximum allowed candidate count. Figure 4 displays this procedure separately for spread, volume, and the joint panel; all select one.

The article names the exact criterion family and penalty but does not reproduce their formulas. It also omits the numerical grid of $(n_\ell,T_\ell)$, ordering or resampling of stocks for nested panels, frequency grid, spectral kernel and bandwidth, candidate maximum rank, and exact selected $c$. These are material replication inputs. The identification procedure can be reconstructed conceptually from this paper, but reproducing its dimension plots exactly requires the cited methodological definition and additional implementation choices or original code.

The following spectral operations explain what the common-component estimator must accomplish. They are a reconstruction of the referenced GDFM machinery, not claimed settings supplied by this application. Estimate lagged covariances $\widehat\Gamma(h)$ on the centered panel and obtain a smoothed spectral estimate such as

$$
\widehat\Sigma_n(\omega)
=\frac1{2\pi}\sum_{h=-M}^{M}
K(h/M)\widehat\Gamma(h)e^{-ih\omega}.
$$

At each frequency retain the leading $q$ eigenvectors in $P_q(\omega)$. The rank-$q$ projection is $P_qP_q^*$, and its implied common spectrum is $P_qD_qP_q^*$. Fourier inversion of the projection defines a generally two-sided filter for reconstructing common observations. The remaining spectrum and filtered observations describe the idiosyncratic component. Integrating diagonal common and total spectra gives estimated variance shares, provided the same normalization is used for both.

A reproduction should verify Hermitian symmetry, nonnegative eigenvalues within numerical tolerance, orthogonality of fitted common and residual spectra, and stability of the extracted space to bandwidth and rank choices. It should separately record how finite-sample endpoints of the two-sided filter are handled. Using future observations to reconstruct an interior historical component is appropriate for this descriptive exercise; treating the same output as an investable real-time signal would require a causal estimator or a strictly historical refit. No such forecast protocol is tested in the article.

## Descriptive results and measurement units

Table 1 reports cross-sectional summaries of each stock's time-series mean and variance after the stated rescaling. For relative spreads, the cross-sectional average mean is 0.96, the interquartile range of means is 0.35, the average variance is 0.58, and the interquartile range of variances is 0.29. Since spreads were multiplied by 1,000, the mean corresponds to a raw relative spread of 0.00096, or 9.6 basis points. A variance reported in these rescaled units must be divided by $10^6$ to recover the raw relative-spread variance.

For volume the corresponding entries are 2.59, 2.07, 6.70, and 2.23 in the source's million-dollar scaling. They are statistics of the reported dollar-volume variable, not turnover normalized by shares outstanding. The source does not supply transaction-level data with which to independently check this scaling.

Stocks are also divided into quartiles separately by their average spread or average volume. Mean spread rises from 0.62 in the lowest-spread quartile to 1.46 in the highest; average spread variance rises from 0.26 to 1.26. Mean scaled volume rises from 0.56 to 6.14 between its lowest and highest quartiles; average volume variance rises from 0.16 to 18.51. These are separately sorted groups, so the table does not establish that the highest-spread firms are also the highest-volume firms.

The spread and volume averages show substantial serial dependence. The contemporaneous scatter plot has no clear linear direction, but the cross-correlogram shows negative lagged relations, particularly at positive orders under the paper's convention, indicating that spread tends to lead volume. Negative orders correspond to past volume related to current spread. These are descriptive correlations, not a causal ordering or a reported Granger-causality test. The prose mistakenly refers to Figure 6 for the scatter plot; the actual scatter plot and cross-correlogram are Figure 3.

## Common variance shares and heterogeneous propagation

Figure 5 gives the central numerical decomposition:

| Liquidity block | Shared market component | Idiosyncratic component |
|---|---:|---:|
| Relative spread | 12% | 88% |
| Dollar volume | 18% | 82% |

These percentages are averaged individual-series variance proportions. They should not be interpreted as a single pooled regression $R^2$ or as the share of variance of the cross-sectional average. The idiosyncratic share need not be economically unimportant noise: it can contain forecastable stock-specific dynamics and weakly correlated disturbances shared by related firms.

The common shares exceed the roughly 2%–4% estimates cited from Chordia et al. and the 8%–14% comparisons cited from Hasbrouck–Seppi, while being comparable to some Korajczyk–Sadka results. The paper explicitly warns that the samples, frequencies, measures, and extraction methods differ. These numbers therefore do not identify how much improvement is caused solely by dynamic rather than static estimation.

Figure 6 orders stocks by average spread and, separately, average volume, then plots each common variance share. There is substantial heterogeneity. Below the 75th percentile, no clear monotone pattern emerges. Above it, the market share tends to increase with the liquidity measure, especially for volume. The spread pattern is noisier. The proposed economic explanation is that wide-spread stocks have thinner books and respond more to marketwide liquidity conditions, while high-volume blue chips react strongly in trading activity. This is interpretation, not a separately controlled cross-sectional regression.

Figure 7 compares averages of individual autocorrelograms. Common volume has a much stronger short-lag autocorrelation than common spread, but decays more quickly. Approximate visual readings at lag one are about 0.5 for common volume and 0.15 for common spread. The spread component maintains a small persistent tail. Idiosyncratic volume is also materially autocorrelated; idiosyncratic spread autocorrelation is relatively small. No numerical impulse-response functions are estimated, so interpreting these shapes as literal responses to an identified unit liquidity shock goes beyond the displayed autocorrelation evidence.

## Why averaging can conceal the relevant dynamics

There are two different aggregation operations in the figures: autocorrelation of an average series, and average of individual autocorrelations. They need not agree. The autocovariance of $\overline x_t=n^{-1}\sum_i x_{it}$ contains every cross-stock lagged covariance,

$$
\operatorname{Cov}(\overline x_t,\overline x_{t-h})
=\frac1{n^2}\sum_i\sum_j
\operatorname{Cov}(x_{it},x_{j,t-h}).
$$

An average of individual autocovariances uses only the diagonal terms; an average of individual autocorrelations additionally normalizes each series separately. Heterogeneous loadings, timing, and cancellation consequently make the two objects different. This explains why a market-average spread can exhibit dynamics that are not representative of a typical stock or its common component.

For each individual stock, lead–lag orthogonality gives the exact identity

$$
\rho_{x_i}(h)=s_i\rho_{\chi_i}(h)
+(1-s_i)\rho_{\xi_i}(h).
$$

After averaging across stocks, the correct expression is the average of these weighted terms. It does not generally equal the average common share multiplied by the unweighted average common autocorrelation plus the analogous idiosyncratic product. That simplification requires additional conditions on the cross-sectional relation between shares and autocorrelations. The article's qualitative explanation using average variance ratios should therefore not be copied as an unconditional algebraic identity for averaged autocorrelograms.

The broader point is that commonality is a property of the joint dynamic information set. A simple average can be a useful descriptive series, but its innovation is not automatically the innovation of the identified common space. This matters if one wants to use a liquidity index as a risk factor: the index's construction can obscure shared information or introduce unnecessary idiosyncratic variation.

## Limits and a faithful reproduction

The empirical application deliberately excludes crisis conditions, small-cap universes, and a separate resiliency block. It measures tightness and transacted depth, while the time needed for prices to recover from an order-flow disturbance remains unobserved. The fact that two blocks share one dynamic dimension does not prove that a richer panel including resiliency, order-book depth, or small illiquid firms would also have one dimension.

Second-order stationarity and a finite pervasive dynamic factor structure are substantive requirements. The authors describe the method as representation-based rather than imposing a restrictive finite VAR or static factor equation, but this should not be read as assumption-free inference. Regime shifts, insufficient panel breadth, weak factors, and bandwidth choices can all affect the finite-sample conclusion. No confidence intervals for the 12% and 18% shares or formal uncertainty bands for the selected rank are supplied.

A faithful implementation should retain the documented survivor universe and cleaning rules for an initial replication, then disclose a separate point-in-time-universe robustness analysis if undertaken. It should build the aligned spread and volume panels, record transformations and interpolation, estimate the three spectral systems, reproduce the stability-based rank choices, recover common and residual components, and compare both types of autocorrelation aggregation. Original code or additional methodological materials are needed for the omitted spectral and criterion settings. The paper's figures alone do not determine them uniquely.

The supported conclusion is that, for this selected large-cap sample and calm period, marketwide spread and volume movements can be represented by the same single dynamic innovation space, while individual measurement dynamics and idiosyncratic risks remain different. That is a useful organizing result for liquidity research. It does not establish a universally sufficient liquidity index or a ready-made causal, pricing, or execution model.

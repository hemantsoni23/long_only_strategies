# International comovement of stock market returns: A wavelet analysis

António Rua and Luís C. Nunes, *Journal of Empirical Finance* 16 (2009), 632–639. DOI: 10.1016/j.jempfin.2009.02.002. Source: [PredictableReturnsWavelet_RuaNunes2009.pdf](../../Finance/PredictableReturnsWavelet_RuaNunes2009.pdf), eight pages including the figures, descriptive table, and references. Despite the source basename, the paper studies comovement rather than return prediction.

## Why this matters

A single correlation estimate can conceal two different forms of variation: correlations can change through calendar time, and common movements can be stronger at some oscillation periods than others. This paper uses continuous wavelet squared coherency to study both dimensions together for four national equity markets and their sectors. Its investment motivation is that diversification may look more effective for short fluctuations than for persistent ones, and that historical integration may alter those benefits.

The contribution is an empirical application of an established time–frequency tool to international equity comovement. It is not a new forecasting algorithm or a causal test of market integration. The central findings concern strong lower-frequency links among Germany, the United States, and the United Kingdom; weaker broad-market links involving Japan; and an extension of German comovement toward shorter periods after the late 1990s.

For reproduction, the wavelet transform is only part of the specification. Smoothing, scale selection, boundary treatment, and the simulated significance threshold also determine the plotted coherency. The paper leaves some of those implementation choices to references rather than fully specifying them. Its VaR illustration additionally contains an ambiguity between variance ratios and standard-deviation ratios that should be made explicit.

## Data, observations, and exceptions

The source is Thomson Financial Datastream. The authors use Datastream broad market **price** indices for Germany, Japan, the UK, and the US, together with ten economic sectors: oil and gas, basic materials, industrials, consumer goods, healthcare, consumer services, telecommunications, utilities, financials, and technology. The paper does not describe total-return reinvestment, so these should not be silently replaced with dividend-reinvested series.

The principal sample runs from January 1973 through December 2007, with 420 monthly end-of-period observations stated. Monthly returns are log first differences of price indices. The exact initial price needed to produce 420 return observations, rather than 419 differences from 420 prices, is not specified. A reproducer should retain and report the initial-price convention rather than silently shifting the sample.

The main comovement analysis uses each market's home-currency returns. The authors say a common-currency version gives qualitatively similar results, with bilateral FX rates also from Datastream. The later equal-weight portfolio risk illustration is explicitly in US dollars. A common-currency portfolio covariance therefore requires converted returns; it is not obtained by directly treating the four home-currency returns as the investable dollar portfolio's returns.

Several sectors have shorter histories. German oil and gas is omitted because its span is too short. German technology starts in December 1988; UK telecommunications starts in December 1981; UK utilities starts in January 1987. These exclusions and starts affect both country-pair sample lengths and the number of usable low-frequency cycles. They should not be filled with later-history proxies without declaring a changed experiment.

Table 1 reports broad-market stock counts of 250 for Germany, 992 for the US, 547 for the UK, and 1,000 for Japan. Those counts describe the vendor indices and are not a supplied survivorship-free constituent panel. Rounded monthly standard deviations are 0.05, 0.04, 0.06, and 0.05, respectively. Means round to 0.01 for Germany, US, and UK and 0.00 for Japan. The rounded means are too coarse for exact covariance or expected-return reconstruction. Index identifiers, historical constituent handling, and detailed vendor adjustment conventions are not provided.

## Continuous wavelet model

A daughter wavelet translates and scales a mother wavelet:

$$
\psi_{\tau,s}(t)=s^{-1/2}\psi((t-\tau)/s),\qquad s>0.
$$

The position parameter $\tau$ localizes time and scale $s$ controls oscillation period. Large scales correspond to lower frequencies and longer fluctuations. The normalization keeps energy comparable across scales. Wavelet admissibility includes a zero mean and an integrability condition on the Fourier transform. For a complex wavelet, unit energy is stated correctly as $\int|\psi(t)|^2dt=1$; the source's general discussion writes a square without emphasizing the modulus.

The continuous transform is

$$
W_x(\tau,s)=\int x(t)\psi_{\tau,s}^*(t)dt,
$$

or, for the discrete monthly observations in the source,

$$
W_x(\tau,s)=s^{-1/2}\sum_{t=1}^{N}x_t\psi^*((t-\tau)/s).
$$

The implementation can compute this convolution in Fourier space. The transform uses neighboring observations on both sides of $\tau$ unless deliberately modified. Thus historical contour plots are smoothed retrospective descriptions, not real-time signals available at the plotted date.

The chosen mother is the Morlet wavelet. With wavenumber $\omega_0=6$, the commonly used approximation is

$$
\psi(t)=\pi^{-1/4}e^{i\omega_0t}e^{-t^2/2}.
$$

The full expression subtracts $e^{-\omega_0^2/2}$ inside the complex exponential term to obtain zero mean. At six this correction is extremely small, motivating its omission. Gaussian localization is not compact support: distant observations receive small rather than exactly zero weights. Unit energy alone also does not imply a wavelet is confined to a finite interval, despite loose wording in the source's exposition.

The paper's display axes express oscillation periods in years, approximately from a quarter year to eight years in the main plots. The exact numerical scale grid and conversion from scale to Fourier period are not separately documented in the text. A reproducer must specify them, especially if using a library whose Morlet convention differs.

## Cross-wavelet coherency and smoothing

The cross-wavelet spectrum should be

$$
W_{xy}(\tau,s)=W_x(\tau,s)W_y(\tau,s)^*.
$$

The sentence introducing it on page 634 prints a second $x$ subscript where the second series should be $y$. That is a notation error: using $W_xW_x^*$ would produce a power spectrum rather than cross-market comovement. Equation 8's denominator and the surrounding two-series discussion make the intended definition clear.

The actual measure is squared coherency,

$$
R^2(\tau,s)=\frac{|\mathcal S(s^{-1}W_{xy}(\tau,s))|^2}
{\mathcal S(s^{-1}|W_x(\tau,s)|^2)\,\mathcal S(s^{-1}|W_y(\tau,s)|^2)},
$$

where $\mathcal S$ smooths in both time and scale. It lies between zero and one under the intended positive smoothing construction. High values identify strong local linear dependence in that time–frequency neighborhood. Smoothing is essential: without it, numerator and denominator cancel and the squared measure is identically one wherever the denominator is nonzero.

The source cites a smoothing method but does not give complete kernel shapes, bandwidths, scale discretization, normalization, or edge-renormalization details in this article. Those are not cosmetic choices. They determine the effective neighborhood, degrees of freedom, and appearance of significant regions. Two implementations using the same Morlet wavelet can differ materially if smoothing differs.

Squared coherency loses sign and, on its own, does not distinguish in-phase positive dependence from persistent opposite-phase dependence. The authors also calculate phase, which can reveal lead-lag relationships, but do not report it because they find no noteworthy lead-lag result. That unreported phase exercise cannot be reconstructed from the displayed coherency alone. Causal direction is not identified by either measure.

## Statistical design and boundary effects

All six unordered country pairs are studied: US–Germany, UK–Germany, US–UK, Japan–Germany, Japan–US, and Japan–UK. Sectoral calculations apply the same country-pair analysis within each sector, subject to the shorter-history exceptions. The paper does not provide a pooled regression or a joint multivariate common-factor estimator.

Significance is assessed by Monte Carlo simulation of 10,000 pairs of white-noise time series with the same length as the data. Bold contours delimit regions called significant at 5%. Computations are performed in Matlab. The source does not specify the complete white-noise distribution/standardization, random seed, precise pointwise threshold construction, or multiple-comparison correction. Consequently, the contours should not be described as controlling a 5% familywise error rate over every time, scale, pair, and sector.

White-noise significance is a particular null model. It does not preserve conditional heteroskedasticity, heavy tails, serial structure, or structural changes in the observed returns. The descriptive table itself suggests non-Gaussian features. Rejection against white noise is not a causal integration test, and it is not the same as rejection against independently generated series preserving each market's temporal dependence.

The authors explicitly warn that the transform uses neighboring data and is less reliable near the start and end of the sample. Large scales are especially affected because they use wider windows and contain fewer independent cycles. The published figure does not supply a separate numerical boundary mask or a complete cone-of-influence specification. Claims of persistent eight-year comovement near 2007 therefore require more caution than a short-period interior feature. Extending the historical plot into a live risk forecast would require a causal estimation design absent here.

## Aggregate-market results

Figure 1 shows strong lower-frequency comovement between Germany and the US and between Germany and the UK over much of the sample. After the late 1990s, strong comovement extends toward shorter fluctuations. The interpretation is not simply that a single correlation rises: the part of the frequency spectrum exhibiting strong dependence broadens.

US–UK comovement is strong across much of the sample and most plotted periods except the shortest ones. For fluctuations shorter than about one year it is generally weaker, with temporary high-coherency episodes around the 1987 crash and the turn-of-the-century technology bubble. The figures support a distinction between persistent lower-frequency association and episodic shorter-frequency co-movement.

Japan's broad market generally shows lower comovement with each other market across the displayed sample and scales. This is a relative historical finding for these indices and dates. It does not establish stable independence, immunity to future crises, or low tail dependence. Coherency is a local second-order relationship and need not track extreme-loss dependence.

The published figures give contours rather than a table of exact point estimates with standard errors. It is reasonable to describe the broad periods and high/low regions, but not to manufacture exact coherency values at particular months or formal break dates. The paper does not estimate a structural-break date with a confidence interval.

## Sector findings

The sixty possible sector/pair combinations are discussed selectively; their figures are omitted and said to be available from the authors on request. The PDF therefore supplies the narrative results, not the complete underlying sector surfaces. Reproduction of those surfaces requires the vendor series and implementation choices above.

Japan remains weakly linked in most sectors, with notable exceptions in consumer goods and technology. Consumer goods exhibits stronger lower-frequency comovement across all countries. In technology, Japan's relations with the US and UK also strengthen at some other frequencies from the mid-1990s. Thus low aggregate Japanese comovement cannot be applied uniformly to every industry allocation.

Among Germany, the US, and the UK, oil and gas has strong US–UK comovement at several scales. Basic materials shows long-period US–Germany comovement over the sample, with UK–Germany and US–UK strengthening from the 1990s; US–UK also exhibits strong fluctuations from roughly half a year to three years since the mid-1980s. Industrials show increased lower-to-middle-frequency links for US–Germany and US–UK since the 1990s, with UK–Germany strengthening later.

Healthcare's strongest relation is US–UK. Consumer services shows German links with US and UK increasing across much of the spectrum around the turn of the century, while US–UK links concentrate around business-cycle periods. Telecommunications has stronger fluctuations longer than four years for UK–Germany and US–UK over much of the sample, and US–Germany from the late 1980s. Utilities show lower-frequency links between the UK and the others. Financials show German comovement increasing from the mid-1990s, alongside persistent US–UK dependence. Technology shows strong long-period comovement from the 1990s and increasing US–UK association across scales from the mid-1990s.

These are source-reported qualitative patterns. They are not independently verified sector-level numerical estimates because the relevant figures and data are not included. They also should not be turned into a ranked optimal allocation: sector variances, expected returns, constraints, and costs would all matter to that separate problem.

## VaR illustration and a ratio ambiguity

The authors consider an equally weighted four-country broad-index portfolio in US dollars. They compare Gaussian VaR using full covariance with Gaussian VaR after setting cross-country covariances to zero. With initial value $V_0$ and tail probability $\alpha$,

$$
\operatorname{VaR}(\alpha)=V_0\Phi^{-1}(1-\alpha)\sigma_p,
$$

and

$$
\sigma_p^2=\sum_iw_i^2\sigma_i^2+\sum_{i\ne j}w_iw_j\operatorname{Cov}(r_i,r_j).
$$

The source uses wavelet counterparts of variance and covariance to display a time–frequency risk ratio. The intended comparison isolates the effect of comovement while retaining individual variances and equal weights. It is an artificial no-covariance benchmark, not an attainable portfolio whose markets can be made independent.

For identical $V_0$ and confidence level, the VaR ratio is the ratio of **standard deviations**:

$$
\frac{\operatorname{VaR}_{\rm full}}{\operatorname{VaR}_{\rm diagonal}}
=\sqrt{\frac{\sigma_{p,\rm full}^2}{\sigma_{p,\rm diagonal}^2}}.
$$

The prose instead says the comparison reduces to a ratio of portfolio variances. Those statements cannot both be correct. A variance ratio of 1.8 implies a VaR ratio of about 1.342, a 34.2% increase; a VaR ratio of 1.8 implies a variance ratio of 3.24. This independent arithmetic check identifies a reproducibility ambiguity. The source code or intermediate variance arrays would be needed to determine which quantity the plotted surface actually uses.

Figure 2 is labeled a VaR ratio and the authors describe long-period VaR as about 80% higher with comovement. That is the paper's reported interpretation, not a separately verified numerical risk estimate. The robust qualitative conclusion is that including positive comovement materially raises the illustrated risk relative to the diagonal benchmark, especially at lower frequencies and increasingly across scales later in the sample. The precise percentage should remain qualified because of the variance/standard-deviation inconsistency.

Gaussian VaR also assumes a parametric relation between volatility and quantiles. It is not a nonparametric tail-loss estimate, and local wavelet variance at an oscillation period is not automatically the variance of a buy-and-hold return over that many years. A wavelet period describes a component of fluctuations; a holding-period aggregate combines components and their temporal dependence. The paper's investor-horizon language is motivation, not a proved equivalence between each scale and a complete investment-horizon risk forecast.

## Reproduction boundaries and implications

An implementer should obtain the exact monthly price and FX series, preserve the sector exclusions and start dates, compute declared log returns, and reproduce the six broad-market transform pairs before adding sectors. Fix Morlet wavenumber six, disclose scale-to-period conversion, smoothing kernels, boundary handling, and zero-padding conventions. Run the 10,000-pair null simulation through the identical transform and smoothing procedure. Keep the output clearly retrospective unless a one-sided method is separately designed and validated.

For the risk illustration, convert to dollar returns, retain the signed real cross-covariance rather than infer it from squared coherency, and construct both the full and diagonal wavelet covariance portfolios. Calculate variance and volatility ratios separately to resolve the source ambiguity. Exact index identifiers, smoothing choices, simulation settings, sector surfaces, and the risk-ratio code are not supplied in the article; they must remain documented gaps rather than invented defaults.

The useful empirical conclusion is that historical diversification relationships vary across both time and oscillation period. Persistent broad-market links and brief crisis-related short-period links should not be collapsed into a single full-sample correlation. The paper does not demonstrate a causal contagion mechanism, an out-of-sample allocation improvement, or a cost-adjusted investment strategy. Its evidence is a richer descriptive map, with particularly important qualifications for boundaries, significance multiplicity, missing sector results, and the VaR calculation.

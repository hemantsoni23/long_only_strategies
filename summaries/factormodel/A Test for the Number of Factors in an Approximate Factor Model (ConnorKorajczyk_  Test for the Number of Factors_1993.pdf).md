# A Test for the Number of Factors in an Approximate Factor Model

Gregory Connor and Robert A. Korajczyk. *The Journal of Finance* 48(4), September 1993, 1263–1291.

Source: [original PDF](../../Finance/ConnorKorajczyk_%20%20Test%20for%20the%20Number%20of%20Factors_1993.pdf). The local PDF contains a JSTOR cover followed by the complete 29-page article. References below use the printed journal pages. This is the factor-number testing paper, distinct from the authors' work on estimating factor loadings, empirical APT implementation, and dynamic volatility.

## Why this matters

A strict factor model requires asset residuals to be mutually uncorrelated. A factor-counting procedure that insists on this restriction can keep adding factors to absorb local industry dependence, even when that dependence disappears from sufficiently diversified portfolios. The approximate-factor perspective asks a different question: does an additional factor explain a nonvanishing amount of average variance as the cross-section grows? This is the relevant distinction between a pervasive source of portfolio risk and a correlation pattern confined to a small collection of securities.

Connor and Korajczyk develop a test based on changes in cross-sectional mean squared residuals. Its main innovation is an asymptotic framework that permits weak cross-sectional residual dependence, together with a way to compare adjacent factor dimensions without relying on the degenerating same-period difference between two nested fits. They estimate statistical factors using asymptotic principal components, correct residual squares for estimated parameters, and compare residual variances from different dates. Their empirical conclusion is deliberately imprecise: the data support roughly one to six pervasive factors, depending especially on whether January returns are examined separately.

The method is a historical precursor to modern large-dimensional factor selection, not a ready-made information criterion with a single stable answer. Its Monte Carlo results reveal finite-sample overrejection after the true factor count. The sample splitting and seasonal variation materially affect the selected dimension. A faithful implementation must retain those qualifications rather than reduce the paper to a claim that the US equity market has a particular fixed number of factors.

## Model and meaning of a pervasive factor

For $n$ assets at date $t$, write

$$
r_t^{(n)}=c^{(n)}+B^{(n)}f_t+\varepsilon_t^{(n)}.
$$

Here $r_t^{(n)}$ is $n\times1$, $B^{(n)}$ is $n\times k$, and $f_t$ contains the $k$ common factor realizations. The intercept accommodates unconditional means. Factor rotations do not affect the fitted common component or the number of factors. Errors have zero conditional mean given the factors; the initial theoretical development assumes independence and identical distribution over time. The cross-sectional dependence restrictions are the distinctive part of the analysis.

The loading condition is

$$
\frac{1}{n}B^{(n)\prime}B^{(n)}\longrightarrow\Xi,
\qquad \Xi\succ0.
$$

Thus every retained factor has nonvanishing average squared exposure. A factor that loads on only a fixed number of securities fails this condition as $n$ grows. The residual covariance $V^{(n)}$ need not be diagonal, but its largest eigenvalue must remain bounded. Consequently, it cannot hide a second pervasive component whose variance grows proportionally with the number of securities.

The paper gives sufficient conditions using cross-sectional strong mixing. There must exist an ordering of the securities under which the mixing coefficient satisfies $\alpha(m)=O(m^{-\lambda})$, with $\lambda>2$. The ordering is a theoretical device; the actual test does not require the researcher to know it. Uniformly bounded sufficiently high moments and sufficiently rapid decay of dependence imply an absolute covariance bound of the form

$$
|\operatorname{Cov}(\varepsilon_i,\varepsilon_j)|
\leq M|i-j|^{-s},\qquad s>1.
$$

Summability bounds the absolute column sums of $V^{(n)}$, and hence its spectral norm. Theorem 1 obtains this implication from a moment parameter $\delta>2/(\lambda-2)$ and exponent $s=\lambda\delta/(2+2\delta)$. This is a sufficient condition, not an empirical assertion that stocks can actually be ordered into a simple spatial dependence model.

Useful examples are correlations that decay geometrically with cross-sectional separation, or a collection of independent blocks whose sizes remain bounded as more assets are added. A growing industry containing a fixed fraction of the entire universe is different: a common residual shock within that industry can become pervasive. Calling a component “industry specific” does not establish that it is asymptotically diversifiable.

The law of large numbers then motivates

$$
\mu_{k,t}^{(n)}=\frac{1}{n}\sum_{i=1}^n\varepsilon_{i,t}^{2}
\longrightarrow\sigma_\varepsilon.
$$

The limit also requires the cross-sectional average of the individual error variances to converge. Bounded individual variances alone do not ensure existence of that average limit. The paper uses a common limiting average in its statements; it should be treated as part of the regularity conditions when constructing a new application.

## Why the test compares different dates

Suppose the true model has $k$ factors and an additional candidate $f_t^*$ is not one of the pervasive factors. Project the existing errors onto it:

$$
\varepsilon_t^{(n)}=\beta^{*(n)}f_t^*+\varepsilon_t^{*(n)}.
$$

Under the null, the sum of squared loadings on this pseudo-factor remains bounded, so $n^{-1}\|\beta^{*(n)}\|^2\to0$. Adding it does not remove a positive limiting fraction of average residual variance. If it were a missing pervasive factor, the corresponding average squared loading would remain positive and the reduction would not disappear.

One might therefore compare $\mu_{k,t}^{(n)}$ and $\mu_{k+1,t}^{(n)}$ at the same date. But their dominant cross-sectional sampling fluctuations are shared. Under the null, the nested-fit difference collapses faster than the individual cross-sectional averages fluctuate. A conventional central limit approximation to their same-date difference is therefore degenerate.

The authors instead use different dates. With an even number $T=2M$ of observations, a basic sequence is

$$
\Delta_s^{(n)}=\mu_{k,2s-1}^{(n)}-\mu_{k+1,2s}^{(n)},
\qquad s=1,\ldots,M.
$$

Under identical time distributions, the two residual-variance sequences have the same mean under the null. Their cross-sectional fluctuations do not cancel date by date. Theorem 3 establishes a joint normal limit for $\sqrt n\Delta^{(n)}$, with covariance $2\psi I$ under the initial time-independence assumptions. The scalar $\psi$ is the limiting variance of the cross-sectional sum of centered squared residuals after $n^{-1/2}$ scaling. It must be positive and stable across the relevant dates and cross-sectional starting positions.

For an ordinary sample mean test, the conventional statistic is

$$
t_\Delta=\frac{\sqrt M\,\bar\Delta}{s_\Delta},
\qquad
s_\Delta^2=\frac{1}{M-1}\sum_{s=1}^{M}(\Delta_s-\bar\Delta)^2.
$$

A positive value supports an additional factor. Under independent Gaussian differences, its reference distribution is $t_{M-1}$. **Implementation correction:** the displayed normalization around p. 1270 does not transparently include the required $\sqrt M$ and describes the degrees of freedom inconsistently with a sample-variance denominator of $M-1$. The expression above is the standard mean-test construction; it should not be replaced by an unscaled mean divided by a sample standard deviation. This note does not infer the authors' unpublished code from that printing issue.

The central limit theorem concerns squared errors, not merely errors. In extending the result, the moment and mixing assumptions must be strong enough for those squared quantities. Finite second moments alone cannot justify the test when residual squares have infinite variance. The source's stated error-moment conditions and the proof's use of a central limit theorem for squares require care; a robust replication should state the stronger moment conditions it actually relies on rather than assume all finite-variance return distributions are covered.

## Estimated residuals, leverage, and factor estimation

The empirical residuals are estimated, so their raw squares are biased downward. Let $F$ be the $(k+1)\times T$ regressor matrix containing a constant and the $k$ factor series. Define the residual-maker

$$
M_F=I_T-F'(FF')^{-1}F.
$$

For asset $i$, the OLS residual vector is $M_Fr_i$. With conditionally homoskedastic errors over dates and observed factors,

$$
E(\hat\varepsilon_{i,t}^2\mid F)
=\sigma_i^2(M_F)_{tt}.
$$

The exact date-specific leverage correction in equation (7) is therefore $\hat\varepsilon_{i,t}^2/(M_F)_{tt}$. High-leverage dates require larger corrections. Replacing this by a global degrees-of-freedom multiplier is an approximation unless leverage is constant.

A small algebraic qualification matters here. Although $\operatorname{tr}(M_F)=T-k-1$, this implies only that the mean diagonal of $M_F$ is $(T-k-1)/T$. It does not imply that the mean of the reciprocals of those diagonals equals $T/(T-k-1)$. The discussion on p. 1272 should not be read as an exact reciprocal-average identity for arbitrary factor realizations.

When factors themselves are estimated from the same return panel, the empirical implementation uses equation (10):

$$
\hat\sigma_{i,t,k}
=
\frac{\hat\varepsilon_{i,t,k}^{2}}
{1-(k+1)/T-k/n}.
$$

For a model with $k+1$ factors, the corresponding denominator is $1-(k+2)/T-(k+1)/n$. This counts the asset-specific regression parameters and the estimated time series of factors against the $nT$ observations. It is a practical correction, not an exact finite-sample unbiasedness theorem for every PCA normalization. Factor rotations introduce parameter redundancies, and estimated-factor leverage need not be uniform. The denominator must remain positive.

The relevant cross-sectional average is then

$$
\hat\mu_{k,t}=\frac1n\sum_{i=1}^{n}\hat\sigma_{i,t,k}.
$$

Fitting common parameters across dates induces dependence even if the original errors were independent over time. Theorem 4 allows a general limiting covariance matrix for the vector of differences, rather than $2\psi I$. This motivates inference that accounts for serial correlation and heteroskedasticity in the empirical difference sequence.

Theorem 5 extends the argument to estimated factors. Its proof uses convergence of the estimated factor space and compares the two residual projection matrices. This is best understood as a result for sufficiently accurate factor-space estimation under the surrounding large-cross-section assumptions. Mere consistency, without control of rates and quadratic projection errors, does not automatically preserve a $\sqrt n$ central limit theorem. For example, a squared factor-estimation error multiplied by $\sqrt n$ must vanish; an $o_p(n^{-1/4})$ factor-space error is one sufficient rate for that particular term, with additional cross-product control required. That rate illustration is a reconstruction of what the expansion needs, not a rate assumption explicitly supplied by the authors.

## Principal-component extraction and eigenvalue interpretation

The factor estimator is asymptotic principal components: form the $T\times T$ cross-product matrix $R'R/n$, extract its leading $k$ eigenvectors, and use their time-series span as the estimated factor space. The procedure is computationally attractive when $n\gg T$. Factor scale and rotation are immaterial for the fitted residuals, provided the OLS regression uses the same span.

The empirical construction uses excess returns and subsequently includes a constant in the asset regressions. A replication should not silently substitute a differently standardized correlation matrix. Cross-sectional volatility standardization would change the target average-variance criterion, and removing each stock's sample mean before extraction is not automatically identical to the stated excess-return extraction followed by a constant.

The paper explains why a familiar population eigenvalue intuition can fail for a sample covariance matrix when $n$ is large and $T$ fixed. The nonzero eigenvalues of the $n\times n$ return covariance are linked to those of the much smaller time cross-product. Schematically,

$$
\frac1T R'R
\approx \frac nT\left(F'\Xi F+\sigma_\varepsilon I_T\right).
$$

Even residual directions then have eigenvalues growing with $n/T$, despite bounded eigenvalues of the population residual covariance. One cannot count sample eigenvalues exceeding a fixed constant and call the result the number of pervasive factors. If returns have been demeaned, this expression must be interpreted on the $(T-1)$-dimensional centered subspace; the centering direction has zero eigenvalue, and the noise term is the centering projector rather than a full-rank identity on all $T$ directions.

## Empirical design and reported evidence

The empirical universe is CRSP monthly NYSE and AMEX common stocks, January 1967 through December 1991. The 300-month sample is divided into five nonoverlapping 60-month blocks. A stock must have all 60 returns in a block to enter that block's panel. The data section reports block sizes of 1,647, 1,796, 1,869, 1,651, and 1,626. The first count is described slightly differently elsewhere in the simulation discussion; an exact historical replication needs the original security list.

Returns are measured in excess of the CRSP Treasury-bill return. Nasdaq is absent. The balanced-within-block requirement creates a survival and data-availability screen; the paper does not provide modern share-code, delisting-return, and missing-observation conventions in enough detail to reproduce the security lists from a current CRSP vintage.

For each block and each $k=0,\ldots,15$, the authors estimate factors, regress each stock on the factors and a constant, apply equation (10), and average the adjusted squared residuals across stocks at each month. Concatenating the blocks produces 300 monthly observations of $\hat\mu_{k,t}$. Factors are reestimated at each block boundary, rather than carried forward from a training window. These are in-sample explanatory tests, not tradable real-time factor portfolios.

Seasonality is important. Regressions of the residual-variance series on monthly indicators identify January as the significant seasonal effect. January and non-January observations are therefore tested separately. January differences compare Januaries across years. Non-January comparisons exclude December–January and January–February transitions. The authors report two configurations: A assigns the lower-dimensional fit to odd observations and the higher-dimensional fit to even observations; B reverses the assignment. These are not independent experiments, and the paper notes their negative correlation.

For non-January differences, the robust mean test uses Newey–West adjustment with one lag. January tests do not use an autocorrelation adjustment. The source does not give complete executable date-pairing rules for endpoints, omitted boundaries, and odd remaining observations; these should be recorded explicitly in a replication. Treating all overlapping adjacent differences as independent would be a different procedure. The combined statistic gives equal weight to the January and non-January standardized statistics and divides their sum by $\sqrt2$, with one-sided normal probabilities.

Table I scales monthly variances by 1,200: multiplication by 12 annualizes variance and multiplication by 100 expresses it in percentage units. These are variance levels, not annualized percentage volatilities. Selected reported levels are:

| Number of factors | All months | January | Non-January |
|---|---:|---:|---:|
| 0 | 18.08 | 32.67 | 16.61 |
| 1 | 12.86 | 16.84 | 12.39 |
| 2 | 12.23 | 15.49 | 11.84 |
| 4 | 11.43 | 12.52 | 11.35 |
| 15 | 9.36 | 7.19 | 9.58 |

The first common component explains much more variation than later components. January has much larger unconditional average variance and gives later factors more explanatory power. **Source inconsistency:** the table's separately printed marginal-reduction columns do not always equal the differences between its adjacent variance levels. For example, January's 32.67 to 16.84 change is 15.83, while the reported first reduction is 14.62. These discrepancies exceed rounding. The table above transcribes levels; its marginal columns should not be used as an internally exact decomposition without the underlying calculations.

The tests in Table II do not deliver a stable unique factor count. Non-January evidence supports one or two factors, depending on configuration. January evidence ranges from one to six at the 10% threshold; configuration B is especially supportive of additional January factors. Combining the two seasonal tests produces initial support for roughly one to four factors. The authors ultimately favor a range of three to six when January evidence is given economic weight, not a formally identified point estimate.

Some representative statistics show the sensitivity. The first non-January factor has robust standardized statistics 4.95 in A and 5.07 in B. The second factor's corresponding figures are 0.80 and 1.79, with one-sided probabilities about 0.21 and 0.04. In B, January statistics for the third through sixth factors are approximately 1.89, 1.54, 1.88, and 1.50. Their significance depends on accepting the less stringent 10% threshold and on the particular date assignment. Isolated high-order rejections also appear after earlier failures to reject. A mechanically imposed “stop at first failure” rule is not equivalent to reporting every test in the paper, and no familywise multiple-testing correction is supplied.

## Simulation design and what it actually validates

The Monte Carlo model has four equally important Gaussian factors, independent Gaussian idiosyncratic errors, and independent cross-sectional loadings. Each loading vector has mean equal to a vector of ones and covariance $\sigma_b I_4$. Each factor has variance $\sigma_f$ and premium $\pi$; each idiosyncratic return has variance $\sigma_\varepsilon$. The symbols $\sigma_b$, $\sigma_f$, and $\sigma_\varepsilon$ denote variances in this calibration, not standard deviations.

There are 1,718 assets and 60 months in a simulated block. The authors generate 1,000 blocks, drawing new betas for each block, and group five blocks into each of 200 artificial 25-year samples. The same extraction, residual adjustment, seasonal partition, and factor tests are applied. All dates have the same population distribution: simulated “January” differs only because it has far fewer observations.

The printed calibration is

$$
\sigma_b=0.4151,\qquad
\sigma_f=0.0009569,\qquad
\pi=0.0010417,\qquad
\sigma_\varepsilon=0.009525.
$$

The intended targets are an equally weighted monthly excess return of 0.004167, equally weighted return variance 0.0039162, and average individual monthly return variance 0.01507. The paper derives $\pi=E(r_{EW})/4$, $\sigma_f\approx\operatorname{Var}(r_{EW})/4$, and

$$
\sigma_b=\frac{\sigma_r-\sigma_\varepsilon}{4\sigma_f}-1.
$$

**Calibration ambiguity:** the printed $\sigma_f=0.0009569$ differs from $0.0039162/4=0.00097905$. The latter is consistent with $\sigma_b\approx0.4159$, close to 0.4151 after the rounding of the reported inputs; the printed factor variance instead gives a different loading variance. A source-faithful reconstruction should run and label both the printed parameter vector and the moment-implied alternative, rather than pretend they are identical. The code and unrounded calibration inputs are not supplied.

Factor estimation itself works well in this design. Table VI reports average $R^2$ values of 99.870%, 98.620%, 98.058%, and 97.117% when the four estimated factors are explained by the true factor space; the corresponding reported minima are 99.727%, 97.368%, 95.236%, and 92.855%. This supports the use of a large cross-section to estimate the factor span. It does not validate the factor-count test under weak loadings, changing loadings, heavy tails, or common idiosyncratic volatility, none of which is generated here.

The factor-count tests have two distinct weaknesses. First, January tests have low power for the later true factors: configuration A's 5% type-II error probabilities for factors two, three, and four are about 0.70, 0.71, and 0.75. Their powers are therefore only 30%, 29%, and 25%. A small seasonal subsample can fail to detect genuinely pervasive factors even when their estimated span is accurate in the full data.

Second, after the fourth factor, finite-sample residual improvements remain slightly positive. They are economically small but statistically detectable with a large cross-section. For the fifth-factor null in the non-January configuration A, the reported rejection rates are about 22% at a nominal 5% and 36% at a nominal 10%. Configuration B gives about 15% and 27%. Even at the fifteenth factor, A's corresponding rates are roughly 12% and 19%. Thus the asymptotic reference test is materially oversized in this simulation. A summary claiming that the method always recovers four factors would conceal the main finite-sample warning in the paper.

## Reimplementation priorities and limits

A minimal faithful program should preserve the block-specific security universes, use the time cross-product PCA rather than full covariance eigenvalue thresholds, estimate each requested factor dimension, include regression constants, and implement both the observed-factor leverage correction and the paper's estimated-factor correction as clearly labeled alternatives. It should save every monthly residual-variance series before forming the seasonal paired differences. That makes the unusual table arithmetic and endpoint choices auditable.

Report the entire sequence of one-sided test statistics for A and B, with the January and non-January components separately. Also report how any selected count changes with the threshold, seasonal weighting, and date-pairing choices. A single selected count hides information the original paper considered central. The Monte Carlo should reproduce the four-factor design before testing richer approximate-factor structures, and should explicitly measure size beyond the true count rather than only power for the first four factors.

The strongest practical lesson is the distinction between pervasive risk and residual correlation. The method provides a reason to avoid fitting every local correlation with an additional factor. Its weakest practical point is the stability of the actual test calibration: sample length is short, factor estimation and residual corrections interact, January supplies little information, and small systematic finite-sample reductions can cause excess rejections. It does not determine which economic factors are priced, establish an investable anomaly, or provide a transaction-cost-adjusted strategy. It is a test of statistical factor dimension under a particular asymptotic structure, with an empirical range that remains sensitive to design choices.

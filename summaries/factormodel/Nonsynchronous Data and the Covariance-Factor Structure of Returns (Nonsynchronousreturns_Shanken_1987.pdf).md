# Nonsynchronous Data and the Covariance-Factor Structure of Returns

Jay Shanken, *The Journal of Finance* 42(2), June 1987, pp. 221–231. Source: [Nonsynchronousreturns_Shanken_1987.pdf](../../Finance/Nonsynchronousreturns_Shanken_1987.pdf). All 11 pages, including six tables and the inference appendix, were read. The delay model, covariance identity, numerical tables, and appendix argument were checked visually. References below use printed pages, with PDF page 1 corresponding to p. 221.

## Why this matters

Daily closing returns are not necessarily observations of simultaneous economic price changes. Different securities trade at different times, and a common information shock can enter one recorded price today and another tomorrow. A same-day covariance matrix then misses part of the common variation, even if the underlying economic returns have no serial dependence.

Shanken shows that this is a material problem for statistical factor models, not only for single-stock beta estimation. In the examined CRSP sample, adding lead–lag covariance terms almost doubles average estimated cross-security covariance and the fraction of individual return variance explained by five factors. It also changes the estimated factor-loading space. Since two-stage asset-pricing tests use that space to explain expected returns, the correction can alter their effective explanatory variables rather than simply rescale all betas.

The paper's contribution is an empirical diagnosis using an existing price-delay model and covariance adjustment. It does not invent the underlying Cohen–Hawawini–Maier–Schwartz–Whitcomb identity, prove a new asset-pricing model, or establish a profitable signal. Its strongest finding is that ignoring timing can substantially change the statistical representation of common risk. The exact number of factors remains unresolved because the usual factor-analysis significance tests are not valid automatically after this adjustment.

## The latent-return and observation model

Let $r_{jt}$ denote the true return of security $j$ generated during period $t$, and let $r^o_{jt}$ denote its observed return. In the framework used in Section I, p. 222,

$$
r^o_{jt}=\sum_{n=0}^{L}\gamma_{j,t-n,n}r_{j,t-n}.
$$

The weight $\gamma_{j,t-n,n}$ is the portion of a true return generated at $t-n$ that appears in the recorded return $n$ periods later. A return is recognized immediately when the weight at lag zero is one and all later weights are zero. Delays can arise from infrequent trading or other price-adjustment frictions; the paper discusses specialist inventory and stabilization behavior as well as investors' intermittent trading decisions.

The delay weights are random, independent of true returns, and independent across securities. The analysis also assumes stationarity of the weight process and independence of sufficiently separated elements of that process. True return vectors are iid over time for the consistency argument. Their contemporaneous components can be correlated: that is the covariance to be recovered. The economic idea is that information can be spread across reporting dates without changing the total return ultimately attributed to it.

These assumptions are restrictive. For example, trading delays that systematically lengthen during large market shocks violate independence between the delay process and true returns. Genuine lagged economic responses or time-varying factor exposures can create lead–lag patterns that are not exclusively delayed recognition. The empirical adjustment identifies the latent contemporaneous covariance under the maintained model; the presence of cross-serial covariance alone does not prove that the delay mechanism is the sole cause.

For distinct securities $j\ne k$, the population identity is

$$
\operatorname{Cov}(r_{jt},r_{kt})=
\operatorname{Cov}(r^o_{jt},r^o_{kt})+
\sum_{n=1}^{L}\operatorname{Cov}(r^o_{jt},r^o_{k,t-n})+
\sum_{n=1}^{L}\operatorname{Cov}(r^o_{j,t-n},r^o_{kt}).
$$

This is equation (2), attributed to the earlier CHMSW work. A common innovation can show up at a positive or negative lag in the observed pair, so both directions are necessary. Adding only one security's lagged covariance is not the same estimator.

The identity is explicitly restricted to off-diagonal elements. It does not establish an analogous consistent variance estimator for $j=k$ under the random delay model. Shanken retains ordinary sample variances on the diagonal, citing earlier evidence that the variance distortion can be small. That empirical expedient is a qualification of the matrix procedure, not a theorem that all its entries are consistently recovered by the same formula.

## A direct implementation of the adjusted matrix

For a synchronized panel of recorded daily returns, estimate the contemporaneous sample covariance matrix $\widehat C_0$ and lag matrices

$$
\widehat C_n(j,k)=\widehat{\operatorname{Cov}}(r^o_{jt},r^o_{k,t-n}),\qquad n=1,\ldots,L.
$$

Then use

$$
\widehat V^A_{jk}=\widehat C_0(j,k)+\sum_{n=1}^{L}\left[\widehat C_n(j,k)+\widehat C_n(k,j)\right],\qquad j\ne k,
$$

and $\widehat V^A_{jj}=\widehat C_0(j,j)$. The unadjusted comparison is $\widehat V^U=\widehat C_0$. A common set of sample variances converts both matrices to correlations. If $D_s$ is the diagonal matrix of sample standard deviations, set $\widehat R^A=D_s^{-1}\widehat V^AD_s^{-1}$ and similarly for $\widehat R^U$.

This notation makes the symmetric construction explicit. Finite-sample choices about whether lagged products use full-sample means or aligned-subperiod means, and whether the denominator is $T$, $T-n$, or a degrees-of-freedom correction, must be documented. The paper says to replace the population covariances by their sample counterparts but does not provide all those coding conventions. They are asymptotically minor but can affect exact printed values.

The lagged covariance sum resembles a truncated long-run covariance calculation, but its target here is a latent same-period covariance under the delay model. It should not be interpreted as a general theorem that adding lags recovers instantaneous covariance under arbitrary return dynamics. The off-diagonal-only construction also has no automatic positive-definiteness guarantee for every finite sample. A modern implementation should check eigenvalues and report any regularization separately; silently projecting to a positive-definite matrix changes the historical procedure.

## Sample formation, timing, and what is not reported

Section II uses CRSP daily returns from July 3, 1962, through December 31, 1972. Ten groups of thirty securities are formed alphabetically, giving 300 analyzed securities. Securities with missing daily data are eliminated. The full-history requirement plausibly favors more actively traded firms, which the author argues could bias against finding large nonsynchronous-return effects. It also means the sample is not an unrestricted historical cross-section and requires careful reconstruction.

Each group contains $30\times29/2=435$ distinct contemporaneous off-diagonal pairs. The article's covariance summaries average these elements within group and then summarize the ten groups. It does not fit one joint 300-security factor model; all the factor analyses discussed below are separate thirty-security models.

A preliminary exploratory analysis suggests that three trading-day lags capture most, but not necessarily all, of the effect. All reported adjusted estimates therefore use $L=3$. The source does not give the exploratory selection criterion, an exhaustive lag-length sensitivity table, or a formal procedure proving that delays beyond three days are negligible. This is a chosen truncation parameter, not an estimated universal maximum delay.

The factor-analysis stage introduces an additional selection rule. If either the adjusted or unadjusted fit produces a Heywood case, meaning a negative estimated residual variance, the security is eliminated and replaced. The article does not list the affected securities, their identifiers, or the exact replacement order. These missing inputs, along with the original CRSP extraction details, prevent an exact recovery of the historical thirty-stock groups from the paper alone.

There is no portfolio sorting strategy, holding period, execution lag, rebalancing rule, transaction-cost model, or out-of-sample evaluation. The chronological lags refer to covariance estimation, not signals available for trade. Because lead information enters the correction, using a covariance estimate in a live decision requires an estimation window ending before the decision date; this is a prospective application choice, not a backtest conducted in the paper.

## Covariance evidence and numerical scale

Table I reports covariance entries multiplied by 1,000. Its full group-level results are:

| Group | Unadjusted covariance ×1,000 | Adjusted covariance ×1,000 | Fraction of pair estimates increasing |
|---:|---:|---:|---:|
| 1 | 0.052 | 0.102 | 97% |
| 2 | 0.057 | 0.106 | 97% |
| 3 | 0.059 | 0.111 | 97% |
| 4 | 0.054 | 0.101 | 98% |
| 5 | 0.038 | 0.079 | 97% |
| 6 | 0.054 | 0.099 | 94% |
| 7 | 0.056 | 0.106 | 98% |
| 8 | 0.049 | 0.092 | 99% |
| 9 | 0.058 | 0.117 | 98% |
| 10 | 0.047 | 0.095 | 99% |
| Average | 0.052 | 0.101 | 97% |

The overall ratio from the displayed averages is about 1.94. Restoring the original covariance scale gives 0.000052 versus 0.000101, rather than treating 0.052 and 0.101 as unscaled return variances or percentage returns. These are averages of off-diagonal covariance estimates; the result does not state that every individual stock's variance doubles.

Table II isolates a one-day lag. The average lagged covariance multiplied by 1,000 is 0.017, with average t-statistic 1.86. The reported proportions significantly positive using one-sided tests are 67% at 10%, 56% at 5%, and 36% at 1%. Fewer than 1% of the statistics are significantly negative at the stated levels. Across groups, average t-statistics range from 1.63 to 2.07.

The two directions of the first lag contribute approximately $2\times0.017=0.034$ on the displayed scale. That is about one third of the adjusted average 0.101. Footnote 5 reports average lag-two and lag-three covariances of 0.003 and 0.004, with t-statistics 0.33 and 0.47. The rounded accounting $0.052+2(0.017+0.003+0.004)=0.100$ is close to 0.101; the small discrepancy is consistent with reporting precision. Most of the average correction is therefore associated with the first day, while the complete estimator retains all three days.

## Inference for cross-serial covariance

The appendix derives the asymptotic distribution of a one-lag sample covariance under the null of no temporal dependence in observed return vectors. With centered returns, define

$$
x_t=r^o_{jt}r^o_{k,t-1}.
$$

Under the null, $E[x_t]=0$. Consecutive products share a date and therefore need not be independent: $r^o_{j,t-1}$ and $r^o_{k,t-1}$ can be contemporaneously dependent. Nevertheless, the zero means and temporal independence imply $E[x_tx_{t-1}]=0$. Products separated by more than one date are independent under the maintained null. The sequence is therefore one-dependent, with zero lag-one covariance.

Assuming finite fourth moments, an appropriate central limit theorem makes the usual t-statistic of the product mean asymptotically standard normal. Replacing population means by sample means changes the statistic by a term vanishing in probability. An implementable statistic is $\sqrt{T_1}\bar x/s_x$, with $T_1$ the number of aligned lag-one products and $s_x$ their sample standard deviation. This is a reconstruction of the appendix's ordinary product-mean test, with finite-sample denominator conventions left to the implementation.

The result is not a generic permission to use iid standard errors for lagged products under arbitrary serial dependence. Its null assumes enough temporal independence for the factorization in the proof. When applying the estimator in a different setting with volatility dependence or other dynamics, the sampling covariance requires its own analysis.

Shanken also gives a deliberately conservative aggregate argument. Every asymptotically standardized t-statistic has variance one. The variance of their equally weighted mean cannot exceed one, since perfect positive correlation is the largest possible common dependence. The overall mean 1.86 is therefore significantly positive at about the 4% level even under that crude upper bound. Assuming independent subgroups while allowing perfect dependence inside each gives the illustrative statistic $1.86\sqrt{10}=5.88$. The subgroup-independence assumption is stronger and is presented as an illustration, not established by the data. Neither calculation treats the thousands of security pairs as independent observations.

## Factor analysis and the doubling of common variation

For each thirty-security correlation matrix, the paper fits a five-factor maximum-likelihood model following the earlier Roll–Ross design. In covariance notation,

$$
V=BB'+D,
$$

where $B$ is $30\times5$, factor covariance is the identity, and $D$ is diagonal residual variance. On the correlation scale, a security's communality is the sum of its five squared loadings and represents the fraction of its total variance assigned to the common factors.

Table III reports average communality of 0.16 using the ordinary estimator and 0.33 using the adjusted estimator. Group means lie between 0.15 and 0.17 before adjustment and between 0.31 and 0.35 afterward. All 300 individual-security communalities increase. The first factor's average squared loading rises from 0.10 to 0.18; the second rises from 0.03 to 0.06. The remaining reported averages rise from about 0.01 each to 0.03, 0.02, and 0.02. Rounding means the displayed factor contributions need not sum exactly to the displayed communality.

A diagonal variance error affects the residual-variance component of a factor model while leaving the off-diagonal factor restrictions potentially identifiable. Footnote 7 argues that loadings can remain consistently estimated if the diagonal misspecification does not force a residual variance to be nonpositive. This qualification is related to the observed Heywood cases and their treatment. It does not eliminate the need to inspect whether the corrected covariance matrix is compatible with the chosen factor model in the actual finite sample.

The higher communality is not evidence that adjusted factors explain twice as much expected return. It concerns covariance and variance decomposition. The paper does not report a new cross-sectional estimate of factor risk premia or a comparison of pricing errors from the two procedures.

## Rescaling loadings versus changing their span

A simple explanation of doubled covariance would be uniform attenuation. If observed-return loadings were approximately $B^o=0.7B$, their common covariance would be $B^o(B^o)'\approx0.5BB'$. The common variance would shrink without changing the number of factors or the linear space generated by their loadings. In that special case, a cross-sectional pricing regression could compensate by rescaling coefficients.

Table IV examines correlations between adjusted and unadjusted thirty-security loading vectors for each factor. The averages are 0.66, 0.34, 0.34, 0.14, and 0.11 for factors one through five. Even the leading factor is far from a perfect linear correspondence. The table gives a first-factor range of 0.38 to 0.85; the prose states an upper value of 0.84, a small internal rounding/reporting discrepancy. Several other factor correlations are negative.

Individual factor comparisons must be interpreted with care because an orthogonal factor model permits sign changes and rotations without changing $BB'$. Low correspondence between arbitrarily named factors can partly reflect that indeterminacy. The paper's next exercise is therefore more relevant to asset-pricing applications: it tests whether each adjusted loading vector can be represented by the entire set of unadjusted loading vectors plus a constant.

Let $b_k^A$ be the adjusted thirty-security loading vector for factor $k$, and let $B^U$ contain all five unadjusted vectors. Estimate the cross-sectional regression

$$
b_k^A=c_k\mathbf1+B^Ud_k+u_k.
$$

If the two augmented loading spaces are the same, this regression fits perfectly in the population for every factor. Table V gives average R-squared values 0.78, 0.56, 0.34, 0.35, and 0.43. More than one quarter of the fifty group-factor regressions have R-squared below 0.30. The result suggests a change in the relevant span, not merely uniform rescaling or relabeling.

The fit of each individual dependent vector can vary with its chosen orientation, but exact containment of the entire column space is invariant to nonsingular changes of factor coordinates. This makes the joint conceptual question robust to factor labels. In finite samples, however, both loading matrices are estimated. Shanken explicitly acknowledges that estimation error is ignored in this descriptive analysis; no formal confidence interval for subspace distance is supplied. Low R-squared values are evidence of sensitivity, not a fully specified statistical rejection of identical population spaces.

## The number-of-factors evidence is suggestive, not definitive

Table VI reports conventional likelihood-ratio-type factor-analysis statistics for five factors in thirty securities. The nominal degrees of freedom are

$$
\frac{(30-5)^2-30-5}{2}=295.
$$

With the ordinary covariance estimator, statistics range from 284 to 337 and reported p-values from 0.67 to 0.05. With the adjusted estimator, they range from 2,106 to 2,771 and all p-values round to 0.00. The additional common variation is much harder to reconcile with five factors under the criterion being used.

The author immediately warns against treating these adjusted p-values as valid calibrated probabilities. The likelihood-ratio reference distribution is derived for the ordinary sample covariance, not automatically for a sum of contemporaneous and lagged covariances. Its sampling covariance changes after adjustment. At the same time, substantial serial dependence undermines the assumptions behind the unadjusted test as well. The paper therefore does not establish a reliable numerical count of true factors, and it does not claim that one can simply substitute the adjusted matrix into any likelihood procedure without modifying inference.

The descriptive result and the inference limitation should be retained together. Discarding the test table loses useful evidence of model sensitivity; treating its nominal chi-square p-values as definitive overstates what the article has shown. A new study would need an asymptotic covariance appropriate to the estimator or a carefully designed resampling method that preserves the relevant dependence. That is proposed follow-up work, not an implemented robustness check in this source.

## Reproduction sequence and practical limits

A faithful reconstruction begins with the complete-case CRSP panel and the original alphabetical grouping rule. Compute both covariance estimators on exactly the same securities and dates, with $L=3$, and preserve the same variance diagonal. Check the displayed covariance scaling and the contributions of each lag before proceeding to factor estimation. The average covariance ratio and the sign of pairwise changes are the first numerical targets; they do not depend on factor rotations.

Next fit the two five-factor models within each group, recording every Heywood replacement and the factor-identification convention. Compare communalities, then loading correlations, then the regressions on the full competing loading space. Finally report the historical five-factor statistics with their original reference-distribution caveat. The source omits identifiers, replacement details, exact software, numerical optimizer and tolerance, factor rotation convention, and some sample-covariance endpoint choices. Those omissions should be visible in any claimed replication rather than silently resolved as though they were original settings.

The full-history sample and the use of one historical decade limit external validity. Effects may vary with trading frequency, exchange design, sample composition, and return horizon. Monthly returns offer an alternative way to reduce the timing problem but discard information and are not guaranteed to reproduce the daily correction. The author notes that some related work obtained similar conclusions at daily and monthly frequency, reinforcing that the importance of the issue is study-specific.

The practical takeaway is to distinguish measured covariance at a reporting timestamp from economic comovement over the information-adjustment interval. In this sample the distinction is large enough to change both common-risk magnitudes and the loading space used in asset-pricing tests. The paper motivates re-examining conclusions built on ordinary daily covariance matrices; it does not establish that every corrected factor model prices returns correctly or that all lead–lag covariance reflects tradable predictability.

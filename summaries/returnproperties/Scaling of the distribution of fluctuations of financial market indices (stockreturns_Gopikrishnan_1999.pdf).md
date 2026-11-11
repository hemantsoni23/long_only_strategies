# Scaling of the distribution of fluctuations of financial market indices

Parameswaran Gopikrishnan, Vasiliki Plerou, Luís A. Nunes Amaral, Martin Meyer, and H. Eugene Stanley. *Physical Review E* 60, 5305–5316 (November 1999).

Source: [published paper](../../Finance/stockreturns_Gopikrishnan_1999.pdf), 12 PDF pages. This note uses the published version, including Appendices A and B. The longer, similarly named Gopikrishnan–Plerou–Amaral–Stanley file in Finance is a version of this work, not another empirical study. References below use printed pages and figure/equation numbers.

## Why this matters

A market return can have a finite variance and still be very far from Gaussian at economically important horizons. This paper examines that distinction using intraday, daily, and monthly index data. Its central empirical claim is that standardized return tails are approximately power laws with survival exponent near three, outside the non-Gaussian stable Lévy range, while the overall distribution changes unusually slowly under time aggregation. Shuffling the observations accelerates convergence toward a Gaussian shape. The combination points toward temporal dependence, including persistent volatility, as an important part of the explanation.

For a reproducing researcher, the goal is to establish which properties concern marginal tails, which concern the central part of the distribution, and which depend on observation order. A model that matches a histogram but produces the wrong aggregation behavior misses a major feature of these data. Conversely, near square-root-of-time variance scaling does not establish Gaussian quantile scaling. The paper supplies descriptive evidence and diagnostic experiments, not an estimated trading strategy, a calibrated option model, or a causal identification of a unique volatility process.

## Data, sampling, and return definition

Section III uses five datasets. The main high-frequency S&P 500 sample covers 1984–1996, with more than 4.5 million index observations, typically recorded at 15-second intervals. Sampling at one minute yields approximately 1.2 million points. Two longer S&P histories contain 8,686 daily observations during 1962–1996 and 852 monthly observations during 1926–1996. International comparisons use 3,560 daily Nikkei observations from 1984–1997 and 4,649 daily Hang Seng observations from 1980–1997.

The datasets support different horizons; they are not one homogeneous panel. For example, the long-horizon daily analysis uses a longer historical interval than the intraday analysis. Agreement across the overlapping one-day horizon is therefore a useful consistency check, but differences can reflect the sample period as well as the sampling method. The international samples also have different dates and lengths. The source describes the S&P 500 as a capitalization-weighted index; a replication should use a consistently defined index series, rather than construct an unadjusted sum of current constituent capitalizations.

For index level $S(t)$, the return over horizon $\Delta$ is

$$
G_\Delta(t)=\log S(t+\Delta)-\log S(t).
$$

This is a log return. Its approximation by a relative price change is valid for small moves, but should not replace it when reproducing the extreme observations. For each horizon, compute the full-sample mean and variance, then normalize:

$$
\bar G_\Delta=\langle G_\Delta\rangle_T,\qquad
v_\Delta^2=\langle G_\Delta^2\rangle_T-\bar G_\Delta^2,
\qquad
g_\Delta(t)=\frac{G_\Delta(t)-\bar G_\Delta}{v_\Delta}.
$$

Here $\langle\cdot\rangle_T$ is a time average over the applicable dataset. This normalization is unconditional and uses the whole sample. It is not an out-of-sample volatility forecast, nor does it remove volatility clustering. Re-estimate the scale separately for every horizon before comparing distributions or fractional moments.

Table I expresses horizons in minutes and converts one trading day to 390 minutes. A source footnote acknowledges the earlier shorter trading day but ignores that difference. The paper does not provide a complete modern data-cleaning specification: the exact interpolation or previous-tick rule, missing records, timestamp conventions, return overlap/stride at every horizon, and all boundary/overnight treatments are not sufficiently documented for bitwise reproduction. Those choices should be recorded as replication assumptions, not attributed to the authors. The three S&P source datasets should retain separate identifiers throughout the analysis.

## What is estimated: survival tails versus density tails

For the positive tail, the object is the complementary cumulative distribution

$$
\Pr(g>x)\sim C_+x^{-\alpha_+}.
$$

For the negative tail, use $\Pr(g<-x)$ for positive $x$. If a differentiable density has the corresponding power-law asymptotic behavior, its exponent is $1+\alpha$, not $\alpha$. An inverse-cubic survival tail therefore corresponds to a density decaying approximately as $x^{-4}$. Confusing the two conventions would substantially change the moment implications.

The one-minute S&P data are first analyzed with log-log regression fits over $3\le |g|\le50$. Equation (5) reports $\alpha_+=2.95\pm0.07$ and $\alpha_-=2.75\pm0.13$. The density fits in Figure 4 imply survival indices $3.01\pm0.11$ and $3.02\pm0.08$. These are broadly compatible tail estimates, not identical statistics. The paper does not supply a full dependence-robust inference procedure, so the quoted fit errors should not be interpreted as comprehensive uncertainty about the population tail index.

The central region behaves differently. Over approximately $0.5\le |g|\le3$, reported slopes are about 1.6 for positive returns and 1.7 for negative returns. Changing the fit region produces slopes from roughly 1.35 to 1.8. Those central slopes cannot establish a non-Gaussian stable tail. The small-return distribution also reflects price discreteness in underlying stocks. Estimating an exponent from the origin or from a narrow central range and extrapolating it to extreme losses is precisely the inference the paper challenges.

For an exact power-law survival tail, a moment of order $q$ exists only when $q<\alpha$, subject to the behavior of both tails. Values near three are consistent with finite variance and potentially infinite fourth moments. They do not establish a finite third moment: three is a boundary, the estimates differ by sign and method, and finite data cannot settle an asymptotic assertion. Every moment of a finite empirical sample is numerically finite even when the corresponding population moment does not exist.

## Reconstructing the modified Hill procedure

Appendix B provides the local-slope estimator used as an alternative to direct regression. Apply it separately to positive return magnitudes and to magnitudes of negative returns. Sort the relevant magnitudes in descending order, $x_1>x_2>\cdots>x_N$, and associate rank $k$ with empirical survival probability approximately $k/N$. Ties and strict-versus-weak inequalities require an implementation convention that the source does not spell out.

Define the positive inverse logarithmic slope by

$$
\zeta(x)=-\left(\frac{d\log P(x)}{d\log x}\right)^{-1}.
$$

A finite-difference version is

$$
\zeta_k=-\frac{\log(x_{k+1}/x_k)}{\log((k+1)/k)}.
$$

For large $k$, the consistent approximation is

$$
\zeta_k\approx k\bigl(\log x_k-\log x_{k+1}\bigr).
$$

**Source correction:** printed equation (B4), p. 5315, has the opposite sign in this approximation. Since the observations are descending, its printed expression is negative, contradicting equation (B3), the definition, and the positive curves. The expression above follows directly from (B3); it is a correction needed for implementation.

Average local inverse slopes over a window, plot the average against inverse return magnitude $1/x$, and extrapolate to $1/x=0$. The intercept estimates $1/\alpha$. Figure 5 averages 100 local slopes per plotted point. Appendix B also describes averaging all events beyond a threshold as an alternative. The exact window assignment, regression weighting, threshold selection, and tuning across horizons are not fully provided. A reproducible implementation should save these choices and show sensitivity to them.

This extrapolation should not be silently replaced by the usual fixed-threshold Hill estimator. A useful separately labeled comparison is

$$
\widehat\alpha_{\rm Hill}(k)=
\left[\frac{1}{k}\sum_{i=1}^k\log\frac{x_i}{x_{k+1}}\right]^{-1},
$$

but a conventional Hill curve and the authors' local-slope extrapolation need not give identical results. Appendix B validates the diagnostic with survival laws $(1+x)^{-3}$ and $e^{-x}$: extrapolated inverse indices should approach $1/3$ and zero, respectively. Zero inverse index denotes a tail lighter than any finite power in this example, not a zero tail exponent.

Equation (6) and Figure 5's caption report positive-tail $\alpha=3.45\pm0.07$ and negative-tail $\alpha=3.29\pm0.07$. **Table I reverses these two one-minute Hill entries.** Figure 5's panel labels and caption also disagree about which panel is positive. A replication should retain the sign-specific results from equation (6) as the main-text convention and document the table discrepancy rather than infer a precise asymmetry from it.

## Time aggregation and numerical results

Figures 6–8 examine whether separately standardized distributions collapse across horizons. At intraday horizons, the power-law fit is broadly persistent, although fitted exponents move appreciably. For positive returns, Figure 6 reports 2.69 ± 0.04 at 16 minutes, 2.53 ± 0.06 at 32 minutes, 2.83 ± 0.18 at 128 minutes, and 3.39 ± 0.03 at 512 minutes. Approximate similarity of the distributions is not equality of every estimated exponent.

The table below reproduces selected rows of Table I. Here the Hill columns follow the **table's own entries**, including its one-minute sign discrepancy noted above. A dagger identifies observations derived from the separate daily database.

| Horizon | Survival-fit positive | Survival-fit negative | Hill positive | Hill negative |
|---|---:|---:|---:|---:|
| 1 minute | 2.95 ± 0.07 | 2.75 ± 0.13 | 3.29 ± 0.07 | 3.45 ± 0.07 |
| 4 minutes | 3.41 ± 0.14 | 3.36 ± 0.11 | 3.18 ± 0.09 | 3.22 ± 0.10 |
| 16 minutes | 2.69 ± 0.04 | 2.74 ± 0.10 | 3.07 ± 0.26 | 2.75 ± 0.16 |
| 64 minutes | 2.78 ± 0.05 | 2.52 ± 0.05 | 2.97 ± 0.14 | 2.71 ± 0.09 |
| 256 minutes | 2.53 ± 0.23 | 2.32 ± 0.09 | 3.33 ± 0.30 | 2.63 ± 0.23 |
| 1 day † | 3.66 ± 0.11 | 3.61 ± 0.11 | 3.19 ± 0.17 | 3.33 ± 0.16 |
| 2 days † | 3.75 ± 0.41 | 3.58 ± 0.22 | 3.06 ± 0.26 | 4.67 ± 0.38 |
| 4 days † | 3.77 ± 0.29 | 3.58 ± 0.14 | 3.58 ± 0.29 | 2.99 ± 0.32 |
| 8 days † | 3.31 ± 0.30 | 3.52 ± 0.04 | 4.9 ± 0.6 | 3.85 ± 0.45 |
| 16 days † | 3.49 ± 0.31 | 2.89 ± 0.05 | 4.9 ± 1.1 | 3.97 ± 0.48 |
| 32 days † | 4.3 ± 1.0 | 2.45 ± 0.32 | 8.7 ± 2.0 | 4.5 ± 2.2 |
| 64 days † | 3.00 ± 0.23 | 2.21 ± 0.21 | 4.1 ± 1.1 | 7.7 ± 2.4 |

The one-day comparison between the intraday-derived sample and the longer daily sample gives positive-tail fit estimates of $3.75\pm0.30$ and $3.66\pm0.11$, respectively. The daily fits discussed in Section V use approximately $1\le g\le10$. Those ranges differ from the one-minute tail fit. Figure 9 reports a separate S&P comparison estimate of $3.34\pm0.12$; it should not be substituted for Table I's one-day value without recognizing the different comparison/fit presentation.

Distributional similarity appears to persist up to approximately four trading days. At 8 and 16 days, curves and fractional moments move toward Gaussian behavior. Four days is an empirical crossover description for this sample, not an exact theorem or a universal calendar rule. The long-horizon table is noisy and does not show a monotone increase in every exponent; some negative-tail regression estimates remain small. The strongest claim concerns the evolving shape and moments, not proof that a particular horizon eliminates extreme tails.

The moment diagnostic is

$$
\mu_q(\Delta)=\langle|g_\Delta|^q\rangle_T,\qquad 0<q<3.
$$

The source deliberately avoids orders at or above the approximate tail index. For implementation, the standard-normal benchmark can be calculated as $2^{q/2}\Gamma((q+1)/2)/\sqrt\pi$. This expression supplies a reproducible benchmark for the plotted Gaussian line. Since all series are standardized, the second moment is fixed; agreement at $q=2$ is mechanical and cannot validate the distributional model.

The daily Nikkei and Hang Seng positive-tail estimates are $3.05\pm0.16$ and $3.03\pm0.16$, respectively. Their broadly similar distributions support external comparison across these three historical indices. They do not establish universality across all securities, exchanges, periods, or observation conventions.

## Correlations and why variance scaling is insufficient

Figure 3 estimates an approximately exponential decay of one-minute return autocorrelation, with characteristic time about four minutes and correlations reaching the noise level by approximately 20 minutes. Absolute-return autocorrelation decays much more slowly. A power-law fit across the displayed range gives exponent $0.29\pm0.05$. Discussion of a crossover around 1.5 days refers to other work, rather than a newly estimated universal breakpoint here.

The return standard deviation obeys approximate scaling $v_\Delta\propto\Delta^\delta$. Reported slopes are $\delta=0.67\pm0.03$ below approximately 20 minutes and $0.51\pm0.06$ above that scale. Short-lag linear dependence helps explain the former; the latter is near square-root scaling.

The distinction can be expressed through the variance identity

$$
\operatorname{Var}\left(\sum_{j=1}^nG_j\right)
=n\operatorname{Var}(G_1)+2\sum_{h=1}^{n-1}(n-h)\operatorname{Cov}(G_1,G_{1+h}),
$$

under stationarity. Small signed-return covariances can give approximately linear variance growth while nonlinear dependence in magnitudes remains strong. Consequently, the second-moment scaling cannot establish independence, a Gaussian sum distribution, or reliable Gaussian extreme quantiles. This identity is an explanatory reconstruction, not an additional empirical estimate in the paper.

## The two surrogate experiments

The first benchmark generates 40 million independent random variables with survival tail proportional to $x^{-3}$. The authors sum blocks of $n=1,16,256$ observations and compare standardized distributions and fractional moments. At 256, the plotted distribution is close to Gaussian, markedly faster than the original financial series. The exact full generating law, its center, sign allocation, cutoff, and random seed are not reported. Appendix B's shifted-Pareto and exponential examples test the estimator; they should not automatically be assumed to specify this separate 40-million-observation experiment.

The second experiment randomly permutes the empirical one-minute S&P returns. It preserves the sample's marginal observations but destroys their original ordering. Consecutive shuffled observations are added and renormalized. Figure 12 uses block sizes 1, 32, 128, and 512. The distribution and fractional moments approach Gaussian benchmarks faster than in the unshuffled series. Although the caption calls convergence slow, the main-text comparison is faster convergence relative to actual chronological returns. A finite permutation is sampling without replacement, so it is not literally an infinite iid process; that distinction does not invalidate the practical ordering diagnostic.

These tests support the importance of temporal organization. They do not uniquely isolate persistent volatility from every other form of serial structure. Shuffling also removes intraday seasonal patterns, regime sequences, and other time dependence. A stronger causal claim would require additional controls, such as seasonality-preserving or block-based surrogates; these are potential extensions, not reported results.

## Proposed mechanism and limits of the model

The discussion suggests a multiplicative representation

$$
g(t)=\epsilon(t)v(t),
$$

where innovations are iid and independent of the volatility process, and volatility has a heavy-tailed marginal distribution with long persistence. If volatility controls the far tail and innovations are sufficiently light-tailed, return and volatility tails can have similar indices. This is a proposed explanation, not a jointly estimated model with fitted parameters, likelihood, forecast validation, or demonstrated innovation independence.

The source's schematic ARCH expression uses $v(t)=a+bg(t-1)^2$ despite introducing $v$ as the multiplicative standard-deviation scale. In the usual convention, the recursion is for $v(t)^2$. A reproducing agent should choose one consistent convention rather than implement that expression literally. Standard finite-order stationary GARCH specifications have geometrically decaying dependence under suitable moment conditions; GARCH also has an infinite ARCH representation, so the source's informal description in terms of a finite number of remembered events should not be taken as a precise theorem about all volatility models.

Appendix A reviews stable distributions to explain why an estimated survival exponent above two is incompatible with a non-Gaussian stable law. Convergence statements require properly centered and scaled sums. The Gaussian boundary has finite variance, and a stable-law location parameter is not generally a finite mean when the stability index is at most one. Infinite variance restricts variance-based risk methods; it does not make every conceivable valuation or risk calculation mathematically impossible.

## Reproduction priorities and takeaways

An implementation should retain separate raw-data provenance, build log returns under explicit boundary rules, compute per-horizon full-sample normalization, and save both signed tails before pooling any information. It should reproduce direct survival regressions, density comparisons, and local-slope extrapolation independently. Every exponent needs its fit interval, number of tail observations, and estimator label. Reproduce Table I by data source, then plot fractional moments and the original/shuffled aggregation experiments using a documented block convention.

The central unresolved inputs are original vendor extracts and their cleaning, sampling/overlap details, tail-estimator tuning across horizons, random-generation and permutation seeds, and a complete uncertainty calculation under dependence. The paper supplies enough structure to reconstruct the analyses conceptually, but not enough to guarantee the printed estimates digit for digit.

The useful empirical conclusion is a joint constraint: heavy but apparently finite-variance index returns, weak long-lag linear predictability, persistent magnitudes, and slow distributional aggregation can coexist. Tail extrapolation should therefore be assessed jointly with temporal dependence and horizon. The approximate inverse-cubic pattern is a historical empirical regularity with estimation and sample limitations, not a fixed risk constant.

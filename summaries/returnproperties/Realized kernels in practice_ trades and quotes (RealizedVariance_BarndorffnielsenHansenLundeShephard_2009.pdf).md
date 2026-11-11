# Realized kernels in practice: trades and quotes

Ole E. Barndorff-Nielsen, Peter R. Hansen, Asger Lunde and Neil Shephard. *The Econometrics Journal* 12 (2009), C1–C32. DOI: 10.1111/j.1368-423X.2008.00275.x.

Source: [RealizedVariance_BarndorffnielsenHansenLundeShephard_2009.pdf](../../Finance/RealizedVariance_BarndorffnielsenHansenLundeShephard_2009.pdf). All 32 pages, including the equations, tables and diagnostic figures, were inspected. References below use the printed C-page numbers.

## Why this matters

A high-frequency variance estimator is an entire measurement procedure: the choice of prices, data cleaning, endpoint treatment and bandwidth can matter as much as the estimator's name. This paper turns realized-kernel theory into a practical daily measurement method and evaluates whether it produces similar answers from trades and quotes. That is a demanding diagnostic because transaction returns often have negative short-lag autocorrelation, while single-exchange midquotes can be smoothed and positively autocorrelated.

The innovative contribution is the implementation and diagnostic evidence for a non-negative Parzen realized kernel. The paper explains how to estimate its bandwidth with robust preliminary measures, gives a reproducible TAQ cleaning sequence, and demonstrates both successful noise correction and a specific failure mode: price moves that appear gradually over several minutes. It does not introduce the complete underlying asymptotic theory anew; that is drawn from the authors' earlier work. Nor does trade–quote agreement establish ground-truth accuracy by itself. The value is a coherent empirical procedure whose assumptions and sensitivities can be checked.

The application is primarily Alcoa over the first half of 2007. The practical lesson is to retain high-frequency information while controlling short-run noise, but inspect the behavior across bandwidths and sampling frequencies. A nearly invariant estimate is reassuring. A strong trend in a signature plot can reveal either unresolved frictions or excessive smoothing of real variation. The paper supplies examples of both, rather than an automatic rule that one setting is always best.

## Latent process, target and noisy observations

Over a measurement interval $[0,T]$, the efficient log price is a Brownian semimartingale with finite-activity jumps:

$$
Y_t=\int_0^t a_u\,du+\int_0^t\sigma_u\,dW_u+J_t,
\qquad J_t=\sum_{i=1}^{N_t}C_i.
$$

The drift is predictable and locally bounded, volatility is càdlàg, and all components are adapted to the stated filtration. Finite activity means finitely many jumps on every bounded interval. The target is

$$
[Y]_T=\int_0^T\sigma_u^2du+\sum_{i=1}^{N_T}C_i^2.
$$

This is total quadratic variation, including squared jumps. It equals integrated variance only when there are no jumps. The paper sometimes labels plotted quantities “IV estimates,” but the kernel's stated target includes jumps; a replication should not interpret it as a jump-robust continuous-variance estimator.

Observed log prices at irregular times satisfy

$$
X_{\tau_j}=Y_{\tau_j}+U_{\tau_j},\qquad 0=\tau_0<\cdots<\tau_N=T.
$$

The simple benchmark has centered noise with variance $\omega^2$, mutually independent across observations and independent of $Y$. The authors denote that case $U\in WN$. Independence is useful for bandwidth calculations, but the consistency argument allows substantially more general noise when its realized-kernel contribution vanishes. In particular, weak serial dependence and dependence between efficient-price innovations and noise are not automatically fatal.

The distinction is important for midquotes. A price-setting mechanism can smooth a movement in the efficient value, making observed high-frequency midquote variance too low. Treating all market microstructure noise as independent additive variance would then predict the wrong sign of the distortion. A procedure that only subtracts a positive noise-bias estimate from a sparse variance can aggravate this problem.

## The non-negative Parzen realized kernel

After cleaning and constructing endpoint-adjusted log prices $X_0,\ldots,X_n$, form returns $x_j=X_j-X_{j-1}$. Define unnormalized realized autocovariances

$$
\gamma_h=\sum_{j=|h|+1}^{n}x_jx_{j-|h|}.
$$

The estimator in equation (1.2) is

$$
K(X)=\sum_{h=-H}^{H}k\left(\frac{h}{H+1}\right)\gamma_h
=\gamma_0+2\sum_{h=1}^{H}k\left(\frac{h}{H+1}\right)\gamma_h.
$$

Use the even extension of the Parzen function, whose definition for $z\ge0$ is

$$
k(z)=\begin{cases}
1-6z^2+6z^3,&0\le z\le1/2,\\
2(1-z)^3,&1/2\le z\le1,\\
0,&z>1.
\end{cases}
$$

Several implementation details distinguish this from a generic long-run variance routine. Returns are not demeaned in the definition. Autocovariances are not divided by $n$ or by $n-h$. The lag weight uses $H+1$. Symmetric positive and negative lags double the positive-lag contribution. Ignoring any of these details changes the statistic. Under the stated Parzen construction the quadratic form is non-negative, up to numerical roundoff, which is useful for variance interpretation and for extensions to covariance matrices.

Smoothness at both ends of the weight function helps eliminate noise. With $H\propto n^\eta$, the simple independent-noise case needs $\eta>1/3$ to remove the noise variance term and $\eta>1/2$ to remove its bias; efficient-price consistency needs $\eta<1$. The recommended compromise is $H\propto n^{3/5}$, producing an $n^{1/5}$ rate for this non-flat-top estimator. It gives up the faster rate of certain flat-top alternatives in exchange for non-negativity and useful robustness.

The consistency mechanism can be understood through the quadratic form. If $K(U)\to0$ and $K(Y)\to[Y]$, the mixed term is controlled by a Cauchy–Schwarz bound associated with the positive-semidefinite kernel matrix. Thus dependence between $Y$ and $U$ is not separately required to vanish under an independence assumption. This is a statement conditional on those component limits, not a guarantee for arbitrarily persistent or nonstationary measurement error.

An ordinary Bartlett/Newey–West substitution is inappropriate here. Its kink at the origin leaves a noise bias whose required bandwidth growth conflicts with the efficient-price condition. Standard HAC intuition about a large sample average cannot be transferred unchanged to an unnormalized quadratic-variation estimator. The source's footnote 2 has an abbreviated condition that does not by itself demonstrate the contradiction; the substantive bias/variance argument is the relevant reason to retain the specified smooth kernel.

## Daily bandwidth selection

The asymptotic MSE-optimal expression given in equations (1.3) and Section 2.1 is

$$
H^*=c^*\xi^{4/5}n^{3/5},\qquad
\xi^2=\frac{\omega^2}{\sqrt{T\int_0^T\sigma_u^4du}},
\qquad c^*=3.5134
$$

for the Parzen kernel. The constant comes from its curvature at zero and the integral of its squared weights: $c^*=(12^2/0.269)^{1/5}$. The integrated-quarticity quantity in the denominator is difficult to estimate precisely. In practice, the paper uses

$$
\widehat\xi^2=\frac{\widehat\omega^2}{RV_{sparse}},
\qquad
\widehat H=3.5134(\widehat\xi^2)^{2/5}n^{3/5}.
$$

The equality in the last expression is an implementation rewrite: the exponent is $2/5$ when the supplied argument is the variance ratio $\widehat\xi^2$, not $4/5$. Confusing these two representations is a consequential coding error.

The preliminary $RV_{sparse}$ averages 1,200 realized variances based on 20-minute returns. Each grid shifts the first observation by one second. This reduces sensitivity to the arbitrary start of a sparse grid. The approximation uses $IV^2\approx T\int\sigma^4$ when intraday variance is not very variable; it is chosen for stability, not claimed to be a consistently estimated quarticity ratio in every stochastic-volatility environment. By Cauchy–Schwarz, strong volatility variation makes these quantities differ. Jumps can also affect optimal tuning even though they do not invalidate the stated total-QV consistency target.

To estimate noise variance, take every $q$th trade or quote and repeat for all $q$ offsets. For offset $i$, compute $RV_{dense}^{(i)}$ and let $n^{(i)}$ be the number of nonzero returns used in that realized variance. Then

$$
\widehat\omega_i^2=\frac{RV_{dense}^{(i)}}{2n^{(i)}},\qquad
\widehat\omega^2=\frac1q\sum_{i=1}^{q}\widehat\omega_i^2.
$$

Choose $q$ so observations on each such grid are about two minutes apart on average. Typical values are approximately 25 for transactions and 70 for midquotes. This is intended to make the noise covariance across selected prices small; using every tick for this preliminary noise estimate would be especially questionable for dependent quote noise.

The efficient-price component is not subtracted from this preliminary noise estimate. With small post-decimalization noise, that can make $\widehat\omega^2$ upward biased and the selected bandwidth conservative. The authors prefer this direction because an excessively small bandwidth leaves more noise, while a somewhat larger bandwidth is more robust to serial dependence. This is a practical tradeoff, not an unconditional assertion that oversmoothing is harmless; their January 24 example demonstrates the contrary.

The paper does not completely specify integer rounding of $H$ and $q$, exact price interpolation onto the 20-minute calendar grids, or all zero-denominator edge cases. Those choices need to be explicit in executable code. Applying the method to a nearly inactive asset without a valid positive sparse-variance input is outside a simple plug-in recipe. One should not hide such failures by clipping results without recording the rule.

## Endpoint jittering and its theoretical role

Because the autocovariances are unnormalized, the first and last noisy observations leave contributions that do not disappear merely because the interior becomes dense. Without endpoint adjustment, the paper describes a residual noise term converging to $U_0^2+U_T^2$. Replace boundary observations with local averages to reduce those terms.

The empirical analysis takes two observations at each end. With original cleaned log prices $X_{\tau_0},\ldots,X_{\tau_N}$, use their first-pair average, retain the interior observations starting at index 2 and ending at $N-2$, and end with the last-pair average. In symbols,

$$
X_0=\frac{X_{\tau_0}+X_{\tau_1}}2,\quad
X_j=X_{\tau_{j+1}}\ (1\le j\le n-1),\quad
X_n=\frac{X_{\tau_{N-1}}+X_{\tau_N}}2,
\qquad n=N-2.
$$

The relationship $n=N-2$ follows from the displayed indexing and prevents overlap or omission errors. Average log prices at this stage; averaging prices before taking a logarithm is a slightly different operation. The main estimator then uses successive differences of the resulting sequence.

For a formal noise-elimination limit, the number $m$ of averaged observations increases while the averaged intervals remain suitably local. Under ergodicity, the average endpoint noise approaches zero. The practical implementation keeps $m=2$, so its favorable finite-sample behavior should not be described as satisfying an asymptotic $m\to\infty$ condition literally.

On Alcoa, using $m=1,2,3,4$ changed estimates by less than 0.5% on average in absolute relative terms. The authors argue that endpoint effects are small for actively traded equities whose total daily variation dominates squared endpoint noise. This can fail on an illiquid, low-volatility day, for example when squared spread is a material fraction of daily variance. The endpoint check is therefore part of adapting the method to another market.

## Reconstructing the TAQ cleaning procedure

The measurement window is 9:30 a.m.–4:00 p.m. The main application uses NYSE-originating observations rather than pooling all venues. Cleaning is applied before return formation and bandwidth estimation. The order matters because timestamp aggregation, outlier thresholds and observation counts determine later inputs.

For all data, retain only the stated session, remove zero bids, asks or transaction prices, and keep a single exchange. For quotes, collapse a repeated timestamp to the median bid and median ask separately. Remove crossed quotes with negative spreads, then spreads exceeding 50 times that day's median spread. The final quote outlier screen removes a midquote more than ten mean absolute deviations from a centered rolling median of 50 neighboring observations, excluding the tested observation and using 25 before and 25 after. This is mean absolute deviation about the median, not the usual median absolute deviation statistic.

For trades, discard records whose correction indicator is nonzero. Discard abnormal sale-condition letter codes except E and F under the historical TAQ convention. Collapse multiple transactions at one timestamp to their median price. Then remove a trade above the ask plus the bid–ask spread or below the bid minus the spread. That last rule uses quotes to discipline trades; when quote data are unavailable, the authors suggest substituting the quote-style rolling outlier filter on trade prices.

The centered quote screen is retrospective. It is appropriate for an ex-post daily variance study but cannot be claimed to be a causal filter available at the instant of the quote. Historical condition codes and reporting conventions also need to be matched to the specific database vintage. The source does not specify every matching detail for aligning trades with quotes, nor the boundary handling of the centered window. These are genuine implementation inputs to document.

Table 2 checks five alternatives for same-timestamp trade aggregation: highest aggregate-volume price, volume-weighted price, log-volume-weighted price, trade-count-weighted price, and median price. The median is the baseline. Kernel estimates are usually quite insensitive across these choices after basic cleaning, although particular outliers can matter. The experiment does not justify skipping cleaning entirely.

Pooling venues is especially problematic because reporting delays and asynchronous updates create artificial variation. Across the full Alcoa sample, minimally cleaned all-exchange RV averages 83.83 in the paper's variance scale, versus 4.91 for NYSE alone. After median timestamp aggregation those values fall to 17.61 and 3.27. The all-exchange kernel moves from 2.70 to 2.54, much less dramatically but not negligibly. The authors recommend estimating separately by exchange and averaging estimates rather than concatenating raw records as though they formed one coherent price sequence.

## Empirical design and numerical findings

The main sample has 123 trading days from January 3 through June 29, 2007, for Alcoa, ticker AA, using TAQ data extracted through WRDS. The paper studies both transactions and midquotes, compares tick kernels with approximately one-minute kernels, and compares ordinary RV at tick, one-, five- and twenty-minute spacings. Table 3 adds trade–quote disagreement results for AIG, American Express, Boeing, Bank of America and Citigroup.

This is a measurement study without a return-prediction target, training/test split or tradable portfolio. Its key empirical check is agreement between estimates obtained from two different noisy views of the same underlying process. For day $t$, define

$$
d_t=\frac{|V_{T,t}-V_{Q,t}|}{\sqrt2},
$$

the Euclidean distance from the trade/quote estimate pair to the equality line. Table 3 averages $d_t$ over the sample. For Alcoa, the distances are 0.089 for the tick kernel, 0.105 for the one-minute kernel, 1.119 for tick RV, 0.170 for one-minute RV, 0.312 for five-minute RV and 0.406 for twenty-minute RV. Relative to the tick kernel, the latter four RV distances are 12.62, 1.922, 3.523 and 4.575. Thus the prose claim that every RV disagreement exceeds twice the kernel's is too strong: one-minute RV is 1.922 times for Alcoa, and some other stocks also lie below two.

The tick kernel is not uniformly the least-disagreeing method across the additional stocks. American Express has distance 0.079 for tick RK and 0.060 for one-minute RK. The general empirical pattern favors kernels, but that exception prevents turning the default recommendation into a universal ordering.

Table 4 reports Alcoa tick-kernel means of 2.401 from trades and 2.402 from midquotes, with time-series standard deviations 1.750 and 1.720. The corresponding reported HAC standard errors of the means are 0.268 and 0.258; these measure uncertainty about the means, not daily variability. Their correlation is 0.997. In contrast, tick RV means are 3.210 and 1.897. The latter contrast is consistent with upward trade noise and smoothed midquotes, while the kernel largely reconciles them. Five-minute RV means are much closer, 2.458 and 2.464, but their daily variability is larger and their agreement weaker than the tick kernel's.

These values are variance estimates in the article's reported scale, not annualized volatility percentages. The table does not state its numeric return-scaling convention explicitly; a replication should verify whether returns were multiplied by 100 before squaring before comparing raw numbers. Means and standard deviations alone cannot establish estimation-error variance, since underlying daily variance also changes. Likewise, correlation with a chosen kernel does not establish that kernel as observed truth.

Figure 4 reinforces the agreement result in logarithms. For tick RK, the regression of trade-based on quote-based log estimates has slope 1.014 with reported standard error 0.011, intercept −0.017 with standard error 0.009, and $R^2=0.987$. Tick RV instead has slope 0.799 and intercept 0.671. The plot's near-equality pattern is informative about differential noise; shared bias could still remain in both price series.

## Diagnostic cases and the limits of automatic correction

The paper studies four selected days in detail. They are illustrative cases, not randomly assigned treatments or an independent validation sample.

**May 4: an ordinary day.** Kernel estimates are almost flat as observations are thinned and bandwidths vary, while raw trade and quote RV start on opposite sides. The figure labels show first-order return correlations −0.1778 for trades and +0.0725 for midquotes. The nearby prose gives somewhat different values, −0.24 and +0.088, and different observation counts. These discrepancies should be retained as source inconsistencies; the sign contrast and the stability of the kernel do not depend on selecting one set of approximate values.

**May 8: strong changing variance.** A volatility increase around 2:30 p.m. and large price changes do not destroy the stable kernel signature. Figure 6 has trade extrema −0.11 and +0.25 in price units, and quote extrema −0.14 and +0.13. The prose's +0.19 quote movement does not match that figure. The important inference is limited: jumps and intraday heteroskedasticity need not make the method unusable, although they affect optimal tuning and the uncertainty of a specific daily estimate.

**January 26: gradual information incorporation.** Between roughly 12:13 and 12:20, the observed price rises almost linearly by about 1.5%. The magnified interval contains 96 upticks and 43 downticks, with large trading volumes. Kernel estimates rise sharply with bandwidth, unlike the ordinary day's nearly flat curve. The authors speculate that limited immediately available liquidity allows information to enter observed prices progressively rather than in a single efficient-price jump.

They describe a possible mechanism through

$$
U_{\tau_j}=V_{\tau_j}+\varepsilon_{\tau_j},\qquad
V_{\tau_j}=\rho V_{\tau_{j-1}}-\theta_{\tau_j}\Delta Y_{\tau_j},
\qquad0\le\rho<1.
$$

For a gradual jump, $\theta=1$ offsets the immediate efficient-price innovation in observed $X$, after which the offset decays. For an immediately incorporated announcement, $\theta=0$. The model illustrates strongly endogenous noise; it is not estimated or statistically selected against alternative explanations in this paper.

Deleting observations between 12:13 and 12:21 converts the sequence into a large adjacent price change and makes the signature plots much more stable. This is a diagnostic intervention whose success depends on the economic interpretation. It is not a general outlier-cleaning rule and the authors explicitly lack an automatic gradual-jump detector. An observed trend is also not, by itself, proof that a price is outside the entire semimartingale class; the concern is its incompatibility with the locally martingale-like efficient-price and short-memory noise interpretation at the chosen resolution.

**January 24: genuine rapid variation can be smoothed away.** Prices fluctuate rapidly within a narrow band late in the day while bid and ask move together and the spread remains about two cents. Coarse returns can be small despite substantial intraperiod movement. Both sparse sampling and an excessively large bandwidth suppress this variation. The authors favor a kernel estimate around 0.90, nearly twice the twenty-minute subsampled RV estimate. Their judgment uses the narrow-spread evidence; it is not a direct observation of latent quadratic variation.

These two January cases warn against a simple rule that a smoother estimate is better. Increasing bandwidth can help reveal a gradual latent jump but erase fast efficient-price oscillation. Signature plots make the tension visible; they do not automatically resolve the economic identification problem.

## A reproducible implementation sequence and remaining uncertainty

Implement the historical cleaning rules and preserve counts at each stage. Form trade and quote log-price sequences separately. Compute the sparse 20-minute grid average and the offset-averaged two-minute noise proxy. Apply the two-observation endpoint averages, calculate the actual return count, choose an explicitly rounded bandwidth, and evaluate the unnormalized Parzen quadratic form. Repeat for thinned tick-time samples and for a grid of fixed bandwidths. Store the preliminary variance ratio, bandwidth, endpoint choices, trade–quote difference and cleaning counts with the daily result.

The paper's frequency labels are average durations in activity-based tick sampling, not promises that every interval has that clock duration. A replication must distinguish that construction from previous-tick interpolation onto a fixed calendar grid. It must also label confidence intervals correctly: the shaded signature-plot region is based on the sparse twenty-minute RV inference method, not a universally valid confidence band for every kernel point or for the gradual-jump model.

Several details require code or data clarification: numeric return scaling, integer rounding, exact quote alignment, initial/terminal interpolation, and the inconsistent counts in some captions. Figure 5 refers to 102 days while the main sample is repeatedly described as 123; the source does not explain that discrepancy. None of these should be replaced by invented observations or a claim of exact numerical replication.

The enduring contribution is a transparent measurement workflow and a set of failure diagnostics. The kernel can recover a consistent daily measure from price streams with very different short-run distortions, but its useful robustness depends on cleaning, endpoints, bandwidth and the time scale at which efficient-price variation is being distinguished from delayed information incorporation.

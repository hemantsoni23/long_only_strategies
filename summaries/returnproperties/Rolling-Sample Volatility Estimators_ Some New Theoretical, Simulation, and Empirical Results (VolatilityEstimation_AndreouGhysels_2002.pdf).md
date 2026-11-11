# Rolling-Sample Volatility Estimators: Some New Theoretical, Simulation, and Empirical Results

**Authors:** Elena Andreou and Eric Ghysels. **Publication:** Journal of Business & Economic Statistics 20(3), July 2002, 363–376; DOI 10.1198/073500102288618504. **Source:** [VolatilityEstimation_AndreouGhysels_2002.pdf](../../Finance/VolatilityEstimation_AndreouGhysels_2002.pdf), 15 PDF pages including a JSTOR cover. Printed page 363 is PDF page 2. The appendix on printed page 375 supplies filter definitions and simulation sizes; it is included in this note's inspection.

## Why this matters and the authors' contribution

A sum of intraday squared returns can estimate a day's integrated variance much more accurately than a squared daily return, yet it still contains measurement noise. This paper asks whether smoothing a succession of overlapping realized-variance measures can improve extraction and subsequent forecasting. The proposed historical quadratic-variation filters average rolling intraday estimates, using flat or exponential weights, and compare them with ordinary block averages across days. The economically relevant tradeoff is between reducing measurement noise and lagging a changing variance process.

The new object is a filter of realized variance, not a new return-prediction signal. The authors connect its design to Foster–Nelson continuous-record spot-variance filtering, then examine the connection in GARCH-based Monte Carlo experiments and exchange-rate/equity data. Absolute-return analogues explore robustness to heavy tails. The practical conclusion is that window length, weighting, and sampling frequency jointly matter; a one-day or one-month raw variance sum need not be the best input for forecasting.

Several qualifications are essential. The paper does not derive a complete joint asymptotic theory for the two sampling frequencies it introduces. It assumes that appropriate Foster–Nelson regularity conditions can be transferred to the rolling quadratic-variation setting, and omits the formal proof. Some printed formulas and sample counts are internally inconsistent. This note separates a directly implementable family of filters from the stronger theoretical and exact-replication claims that the supplied article does not fully establish.

## Targets, observations, and the two-frequency design

The starting model has continuous log-price and variance paths:

$$
dp_t=\mu(p_t,\sigma_t)dt+\sigma_t\,dW_{1t},
\qquad d\sigma_t^2=\xi(p_t,\sigma_t)dt+\delta(p_t,\sigma_t)dW_{2t},
$$

with possibly correlated Brownian motions, continuous coefficient functions, and positive volatility-of-variance coefficient in the starting diffusion setup. Jumps are excluded. The target over a trailing interval of length $H$ is

$$
Q_t^H=\int_{t-H}^{t}\sigma_s^2\,ds.
$$

This is integrated variance, despite the paper's frequent use of “volatility” for variance-valued objects. Spot variance $\sigma_t^2$ and integrated variance $Q_t^H$ are distinct targets. Filtering a noisy estimate of the second does not automatically inherit every optimality result for filtering the first.

Let $r^{(m)}_t=p_t-p_{t-1/m}$ be an observed return with $m$ observations per benchmark period. A benchmark is a day in the intraday application or a month in the daily-data application. A clean trailing realized-variance definition is

$$
QV_{m,t}^{H}=\sum_{j=0}^{Hm-1}\left(r^{(m)}_{t-j/m}\right)^2,
$$

assuming $Hm$ is integral. This convention contains exactly $Hm$ increments. The paper sometimes writes inclusive sums from zero through $Hm$, which would contain one extra observation, and its appendix labels day intervals differently. The convention above makes the endpoint information set explicit rather than relying on those inconsistent indices.

The general filter uses one frequency $m_2$ to build each realized-variance observation and another frequency $m_1$ to slide and average those observations:

$$
\widehat Q^H_{m_1,m_2,t}=\sum_iw_{m_1,i}\,QV^H_{m_2,t-i/m_1},
\qquad \sum_iw_{m_1,i}=1.
$$

If $m_1=1$ and $H=1$, the researcher samples one realized variance per day. If $m_1=m_2$, a new trailing one-day realized variance becomes available at every intraday observation. Adjacent observations in this latter sequence overlap almost completely. They are not independent new measurements of the same target, and their dependence matters for asymptotic analysis and uncertainty estimates.

For a continuously sampled frictionless diffusion, raw realized variance converges to integrated variance as $m_2$ grows. The source cites a normalized error using the quarticity estimate $(2/3)\sum r^4$, with convergence at rate $\sqrt{m_2}$. That is a different limiting experiment from shrinking a local smoothing window around a changing target and obtaining a fourth-root rate. A fast rate in one sampling dimension cannot be substituted for the other without checking which object is held fixed.

## A precise implementation of the filter family

It is easiest to code every filter using one master intraday return grid and a declared endpoint $t$. For one-day variance define $V_t=QV^1_{m,t}$. The block filters averaging $k$ nonoverlapping day estimates are

$$
QV_k(t)=\frac1k\sum_{d=0}^{k-1}V_{t-d},\qquad k\in\{1,2,3\}.
$$

Each estimates a daily variance level, not a $k$-day total, because of division by $k$. It uses $k$ days of returns. The historical quadratic-variation counterpart averages a succession of overlapping one-day estimates:

$$
HQV_k(t)=\frac1{km}\sum_{j=0}^{km-1}V_{t-j/m}.
$$

This formula expresses the intended extension of the appendix's one-day historical filter to $k$ days. It uses approximately $k+1$ days of underlying returns, because the earliest one-day window begins another day before the outer averaging window. Comparing $HQV_k$ with $QV_k$ therefore does not hold raw data span fixed; the fairer span comparison is $HQV_k$ against $QV_{k+1}$, subject to boundary conventions.

Substituting the definition of $V_t$ reveals the mechanism. $HQV_k$ is a convolution of two rectangular weighting kernels on squared returns. For $k=1$, the effective weights rise and then fall approximately triangularly over two days. Central observations occur in many overlapping variance windows, while boundary observations occur in few. Averaging those windows does not create new data; it changes the weighting of existing squared returns. It can also be expressed as summing smoothed spot-variance estimates, though the induced spot weights need not be individually optimal.

The exponentially weighted version applies geometrically declining weights to overlapping $V$ values. An explicit endpoint-consistent implementation of the stated intent is

$$
EHQV_k(t;a)=\frac{\sum_{j=0}^{km-1}a^jV_{t-j/m}}{\sum_{j=0}^{km-1}a^j},\qquad 0<a<1.
$$

The denominator is $(1-a^{km})/(1-a)$ and guarantees unit weight sum. This equation is a clarification of the authors' intended declining-weight filter, not a literal transcription of Appendix Equation A.5. A.5 prints $a^{-j}$ for decay parameters 0.940, 0.960, and 0.999; those powers increase with age. It also shifts the $QV$ date differently from A.3. Both discrepancies should be resolved against the original code before claiming exact numerical reproduction. The note's implementation assigns the largest weight to the newest available estimate and uses no future prices.

The numerical decay parameter applies per outer observation. Its meaning changes with sampling frequency. For example, $a=0.999$ has an untruncated geometric half-life of approximately 693 outer observations: about 2.4 days at 288 observations a day, versus almost nine trading sessions at 78 a day. These are explanatory calculations, not reported estimates. The finite window truncates the actual kernel, so a half-life longer than the window implies nearly flat weights over the retained span.

Absolute-return filters replace each square with an absolute value:

$$
CAR^H_{m,t}=\sum_{j=0}^{Hm-1}|r^{(m)}_{t-j/m}|,
\qquad HCAR_k(t)=\frac1{km}\sum_{j=0}^{km-1}CAR^1_{m,t-j/m}.
$$

At a fixed frequency these may be useful scale proxies less dominated by extreme returns. They are not variance-valued without a further transformation and calibration. For a Brownian diffusion, an unnormalized absolute-increment sum grows with sampling frequency; it does not converge to $\int\sigma^2dt$. The authors explicitly acknowledge that their limiting argument for quadratic variation does not apply to the absolute-return sums. Cross-frequency CAR comparisons require a scale convention, and CAR-relative error ratios should not be read as directly comparable absolute variance-estimation errors.

## The asymptotic argument and its boundary

Section 1.2 presents a flat-weight continuous-record expression. Write $n_L,n_R$ for scaled left and right window lengths, and suppress time and sampling subscripts on the local quantities $\theta^Q$, $\Lambda^Q$, and $\rho^Q$. Its stated limiting variance is

$$
C^{QF}=\frac{\theta^Q}{n_R+n_L}
+\sqrt{\theta^Q\Lambda^Q}\,\rho^Q\frac{n_R-n_L}{n_R+n_L}
+\Lambda^Q\frac{n_R^3+n_L^3}{3(n_R+n_L)^2}.
$$

The authors attach this to $m^{1/4}(\widehat Q^H_{m,m,t}-Q_t^H)$ and a locally Gaussian limit. The first term is measurement-noise cost, falling as the window widens. The last captures target movement, rising with the span. The middle term depends on asymmetry and correlation between noise and changes in the latent quantity; it vanishes for symmetric windows. For a one-sided filter with $n_R=0$, the expression becomes $\theta^Q/n_L-\rho^Q\sqrt{\theta^Q\Lambda^Q}+\Lambda^Q n_L/3$. Minimizing its two window-dependent terms gives $n_L=\sqrt{3\theta^Q/\Lambda^Q}$ when both constants are strictly positive. This is an algebraic consequence of the displayed expression, conditional on its applicability.

The attraction is a bias/noise tradeoff with an optimal span, and the paper invokes Foster–Nelson results to motivate exponential weighting. It does not supply estimators for all local constants or a complete feasible plug-in rule for choosing the span in real time. The reported empirical decay is selected from a small prespecified grid, not computed from a verified local asymptotic optimum.

There is a deeper regularity caution. Under the stated continuous variance paths and fixed $H$, the trailing integrated process obeys

$$
\frac{dQ_t^H}{dt}=\sigma_t^2-\sigma_{t-H}^2.
$$

It is pathwise finite variation. Therefore its being a semimartingale alone does not establish the nondegenerate diffusion fluctuations used in a direct spot-variance transplantation. One also has to handle strongly overlapping measurement errors. The source acknowledges an unproved transfer of assumptions and the absence of general double-index asymptotics. Consequently its $m^{1/4}$ expression and generic exponential optimality should be presented as the proposed extension under additional conditions, rather than an established universal theorem for every fixed-horizon integrated-variance process. The finite-sample filter definitions and their numerical comparisons remain meaningful independently of this gap.

## Monte Carlo design and what must be reconstructed

The simulation uses GARCH-based return processes calibrated to yen/US-dollar and S&P 500 returns. At a selected sampling frequency,

$$
r_t=\sqrt{h_t}z_t,\qquad
h_t=\phi+\alpha r_{t-1}^2+\beta h_{t-1},
$$

with zero conditional mean and initially normal standardized innovations. The variance recursion supplies a latent comparator. The “true” daily integrated variance is approximated by the sum of one-minute conditional variances; monthly truth is built from daily conditional variances. Forecast experiments ignore parameter uncertainty in the Monte Carlo design.

The reported daily parameters are $(\phi,\alpha,\beta)=(0.026,0.104,0.844)$ for yen and $(0.033130,0.028523,0.967347)$ for S&P 500. The implied unconditional levels are 0.500 and about 8.0218. S&P calibration is described in the text as April 2, 1986–August 29, 1997 with 2,884 observations, but Table 1 gives a different start-date string. That discrepancy requires the original data/code for resolution.

Drost–Nijman temporal aggregation/disaggregation and Drost–Werker results are used to obtain other frequencies. Intraday counts are 288 five-minute or 1,440 one-minute intervals per 24-hour FX day; equity has 78 five-minute or 390 one-minute observations per 6.5-hour session. Table 1's one-minute parameters are $(0.0000185,0.0041994,0.9957635)$ for FX and $(0.0000851,0.0016560,0.9983334)$ for equity. The five-minute entries are $(0.000093,0.009267,0.990550)$ and $(0.000426,0.003670,0.996276)$. Monthly aggregation uses 22 trading days, with parameters $(0.34556,0.05944,0.24943)$ and $(0.69811,0.07704,0.83594)$ respectively.

These table values preserve approximately the same unconditional variance across frequencies, although unscaled diffusion return variance must shrink with interval length. The article refers to benchmark-frequency normalization but does not give an entirely transparent implementation of that scaling. A reproducer must distinguish normalized returns/variance states from raw interval increments before summing them into daily truth. Exact weak-GARCH aggregation also does not imply that every aggregated series simultaneously has a strong Gaussian-GARCH representation with iid Gaussian standardized shocks. The table's frequency-dependent kurtosis entries reinforce the need to use the intended mapping rather than assume identical conditional distributional structure at every frequency.

The printed continuous-time Equation 2.1 has an additional problem: its variance equation uses a drift involving $\sigma_t$ and a constant diffusion term, which is not a directly usable positivity-preserving GARCH variance diffusion. The discrete recursion and supplied parameter tables are the more concrete simulation specification. No unreported correction to that SDE is imposed here.

There are 500 replications per experiment. Daily experiments use five- and ten-year samples, with 250 days per year and an additional year's presample data for one-sided filters. Thus five-year one-minute counts are 1,800,000 for FX and 487,500 for equity. The appendix's five-minute equity count of 97,000 conflicts with $1{,}250\times78=97{,}500$. Its monthly experiment says 30 years and 360 months but 4,320 daily observations; 360 months at 22 days would require 7,920. Exact monthly sample length is therefore unresolved in the printed source. Seeds, initialization beyond the presample span, software version, and all aggregation formulas are not included.

The sensitivity experiments introduce MA(1) return effects with coefficients including 0.2, ±0.5, and 0.85, and Student innovations; the reported tail table uses eight degrees of freedom. Strong positive or moderately negative MA effects make quadratic-variation filters' relative errors more similar. Details of the MA noise normalization and distributional scaling are not fully specified.

## Evaluation and numerical simulation results

Extraction error is true integrated variance minus its filter. MSE and MAE are divided by the corresponding error for $QV_1$ in daily experiments or $QV_{22}$ in monthly experiments. A ratio 0.5749 means a 42.51% reduction in MSE, not a 57% reduction. The paper's prose sometimes describes the remaining percentage as an efficiency improvement; the ratios are safer to interpret directly.

Table 2 gives S&P daily extraction-MSE ratios of 0.5903 for $QV_2$, 0.5749 for $QV_3$, 0.6735 for $HQV_1$, 0.6213 for $HQV_2$, and 0.6123 for $EHQV_2$. Thus extending the block window makes a substantial improvement, while changing flat historical weights to exponential weights at the same span yields a much smaller improvement. For FX, $QV_2$ is 0.6753, $QV_3$ 0.6783, $HQV_1$ 0.7446, and $EHQV_1$ 0.7220. The best candidate differs by process; “three days is always optimal” is not supported by this table.

Monthly S&P extraction ratios are 0.2762 for $QV_{44}$, 0.1265 for $QV_{66}$, 0.3507 for $HQV_{22}$, 0.1372 for $HQV_{44}$, and 0.1234 for $HQV_{66}$. FX instead favors the shorter block window: 0.4362 for $QV_{44}$ versus 0.5630 for $QV_{66}$. Comparing historical and block filters requires remembering their different underlying spans.

Forecasts use the weak-GARCH cumulative-return-variance projection. Put $b=\alpha+\beta$, $\bar h=\phi/(1-b)$, and $N=mh$. The printed Equation 2.5 has the form

$$
P_t(R_{t,t+h}^2)=N\bar h+\frac{b(1-b^N)}{1-b}(h_t-\bar h).
$$

Here $R_{t,t+h}$ is an aggregate return over the horizon, not merely the return on its last day. The sum of geometric variance forecasts explains the factor $b(1-b^N)/(1-b)$. Substituting a filtered variance state requires normalization to the same per-step scale as $h_t$. If $N$ is large and $b<1$, sensitivity to the current state becomes small relative to the unconditional component, explaining why differences between extraction filters can disappear at long horizons.

For S&P, the daily one-day forecast-MSE ratio for $QV_3$ is 0.6489; at twenty days it is 0.4847, while $HQV_3$ is 0.4595. In FX, twenty-day ratios are near one: 0.9857 for $QV_3$ and 0.9851 for $HQV_3$. Twelve-month ratios are 0.9474 for S&P $QV_{66}$ and essentially one for yen. Better contemporaneous measurement need not deliver a commensurate long-horizon forecast gain.

The Student-eight experiment gives daily S&P ratios 0.1114 for $QV_3$, 0.0620 for $HQV_3$, and 0.1106 for $EHQV_3$. Monthly $HQV_{66}$ is 0.0339 relative to raw monthly quadratic variation. These large relative gains reflect a noisy benchmark under heavy tails. The historical absolute-return filters also show low ratios relative to their own CAR benchmark, but this does not establish their absolute superiority for variance without resolving the scale/target issue noted earlier.

Additional diagnostics include regression $R^2$, correlation of extraction errors with filtered estimates, and discrepancies between estimated and true autocorrelation functions. High $R^2$ can coexist with level bias, and autocorrelation fidelity is a different objective from contemporaneous MSE. Reported extraction-error correlations range from roughly 1% to 26%; the filters are not generally orthogonal projections exhausting all information.

## Empirical design and results

The FX sample contains Olsen five-minute DM/US-dollar and yen/US-dollar returns from December 1, 1986 to November 30, 1996. After exclusions for predictable market closures, the final sample is 705,024 returns, exactly $2{,}448\times288$. The source's original-count description is inconsistent: 1,052,064 observations is not $2{,}653\times288$. Closure details are delegated to the cited Andersen et al. paper, and the precise quote filtering and daily boundary rules are not reproduced. Filters are evaluated at five-, fifteen-, and thirty-minute spacings and horizons of 1, 5, and 20 days.

Table 4 supplies fitted daily parameter vectors for yen $(\alpha,\beta,\phi)=(0.0511,0.919,0.0028)$ and DM $(0.0548,0.9240,0.0112)$, estimated using the ten-year sample. Thus although forecasts use lagged filter information, the supplied description does not establish a fully recursive out-of-sample parameter-estimation exercise. The exact evaluation target and scale alignment in the empirical extraction notation are also not specified as clearly as in the Monte Carlo design. These are constraints on exact reconstruction, not grounds to invent a training/test split.

At five minutes and one day, DM forecast-MSE ratios are 0.6333 for $QV_3$, 0.6078 for $HQV_3$, and 0.5589 for $EHQV_3$. At twenty days they are 0.5727, 0.5506, and 0.5053. Yen at one day gives 0.6423, 0.6349, and 0.6514: exponential weighting is worse than flat historical weighting in that cell. At fifteen minutes, yen $EHQV_3$ reaches 0.6050 versus 0.6099 for $HQV_3$. The table supports modest, setting-dependent weighting gains, not uniform dominance. Nor do ratios decline monotonically from five to thirty minutes for every horizon.

Equity evidence uses 18,571 daily S&P composite-index observations from January 3, 1928 to August 29, 1997. Monthly filters use 22, 44, and 66 trading-day windows and forecast horizons 1, 6, and 12 months. Table 5 uses the monthly parameters in Table 1 for consistency with simulation, rather than documenting a rolling refit over the long historical equity sample.

For one-month forecasts, uncorrected $QV_{66}$ and $HQV_{66}$ MSE ratios are 0.6273 and 0.6142, but their MAE ratios are 1.0005 and 1.0042. The gains are concentrated in squared errors, with no corresponding typical absolute-error improvement. At six months the MSE ratios become 0.5118 and 0.5015. At twelve months they are 0.8719 and 0.8752.

The serial-correlation extension augments squared-return sums with adjacent-return cross products in the spirit of French–Schwert–Stambaugh. A variance-of-aggregated-return reconstruction normally uses twice the adjacent covariance sum; the supplied article describes the correction but does not print a complete coefficient and boundary formula. Its table reports $HQV_{22}+SC_{22}$ at 0.4964 relative to $QV_{22}+SC_{22}$ for one-month MSE, with MAE 0.8904. This supports an advantage within that corrected family. Because different panels use different denominators, comparing ratios across panels alone does not prove that adding the correction reduces absolute MSE. At twelve months the longest corrected historical filter has MSE ratio 1.6015 and MAE 1.3914, an important failure case.

The article supplies ratios without confidence intervals or a fully specified sampling-uncertainty procedure. Its occasional language of significant gains should therefore be read as reported performance differences rather than reconstructed hypothesis-test conclusions. A replicator should preserve all spans and targets, resolve the documented formula and normalization conflicts, and use uncertainty estimates suitable for overlapping filters and forecast horizons. The lasting contribution is the explicit separation of raw realized-variance measurement from filtering design; the paper's stronger asymptotic and optimality claims require additional verification.

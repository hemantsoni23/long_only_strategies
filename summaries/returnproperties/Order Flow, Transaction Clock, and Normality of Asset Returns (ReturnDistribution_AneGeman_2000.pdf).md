# Order Flow, Transaction Clock, and Normality of Asset Returns

**Authors:** Thierry Ané and Hélyette Geman. **Publication:** *Journal of Finance* 55(5), October 2000, pp. 2259–2284. **Source:** [ReturnDistribution_AneGeman_2000.pdf](../../Finance/ReturnDistribution_AneGeman_2000.pdf). This note covers all 26 pages, including Appendices A–B, the rotated numerical tables, and the density and quantile plots. Printed page 2259 is PDF page 1.

## Why this matters and what is contributed

A heavy-tailed return distribution in calendar time need not imply that the elementary price innovation is itself heavy-tailed. A Gaussian innovation observed over a random amount of business activity produces a mixture of variances, which can have a sharp center and substantial tails. The economically important question is then which observable activity variable measures that random clock. Trading volume and transaction count are related, but a few large transactions and many small transactions can have the same volume while conveying different information about market activity.

Ané and Geman compare these candidates using high-frequency Cisco and Intel data. Their principal empirical contribution is that transaction count explains short-interval volatility better than volume, and that a return transformation associated with a recentered transaction clock passes their normality tests. Their modeling contribution is to separate a general stochastic time change from a Lévy subordinator, whose stationary independent increments are much more restrictive. They estimate clock moments through constrained moment-generating-function matching rather than impose a lognormal clock distribution.

The useful result is an architecture connecting activity, conditional variance, and unconditional tails. The paper does not establish that all stock returns become independent Gaussian observations when indexed by trades. Several essential steps of the reconstruction are incompletely specified, and the printed clock moments and one appendix formula need special care. Those qualifications are important because a nonnegative random clock and an unconstrained collection of fitted moments are different mathematical objects.

## Model: distinguish the return increment from cumulative business time

For clarity, use $C(t)$ for a cumulative increasing business clock and $H_t=C(t)-C(t-\Delta)$ for its increment over one calendar observation interval. Let $N_t$ and $V_t$ denote the transaction count and traded volume within that interval. This notation makes explicit a distinction that the source sometimes suppresses by using cumulative-process notation for variables whose empirical tables describe interval observations.

The return-mixture model is

$$
Y_t=\mu H_t+\sigma\sqrt{H_t}Z_t,
\qquad Z_t\sim N(0,1),\qquad H_t\geq0,
$$

with $Z_t$ independent of $H_t$. Equivalently, a cumulative process has the representation $\mu C(t)+\sigma B_{C(t)}$ for a Brownian motion independent of the clock. Conditional on the increment,

$$
Y_t\mid H_t=h\sim N(\mu h,\sigma^2h).
$$

Here $\mu$ is drift per unit of business time and $\sigma^2$ is variance per business-time unit. Neither is automatically a daily or annualized volatility parameter. A definition of business-time units is part of identification.

The source considers an affine relationship between the clock and cumulative volume or transaction count, ultimately favoring the latter. If an affine model is imposed on interval increments, $H_t=a+bN_t$, it must remain nonnegative over the observed and modeled support. At the cumulative-process level, adding a constant to $C(t)$ does not change its increments. Adding a constant to every interval clock is instead a deterministic calendar-time drift in the cumulative clock. These operations should not be confused when implementing the paper's recentering argument.

A subordinator is an increasing, right-continuous process with stationary independent increments. Poisson, gamma, and suitable stable subordinators are examples. A general increasing stochastic clock may have persistent or nonstationary increments. This broader class can accommodate clustered trading activity without forcing independent increments in calendar time. Continuous clock paths preserve continuity of Brownian time-changed paths; jumps in the clock can produce jumps in the observed price process.

The article invokes the representation of semimartingales by time-changed Brownian motion. Such a representation result does not identify the economic clock with transaction count, make the Brownian motion independent of that clock, or imply the conditional Gaussian mixture above. Independence is introduced separately in equations (10)–(11) and Appendix A. It is an economically restrictive assumption, particularly if price innovations influence trading intensity or both respond to common news.

## Data and observation construction

The sample is January 2 through December 31, 1997. Reuters tick records contain prices, transaction timestamps, and volumes for two Nasdaq technology stocks. Trades that leave the last recorded price unchanged are retained, which matters for both the transaction clock and the mass of zero short-interval returns.

The paper constructs equally spaced calendar-time series at one and ten minutes for Cisco and five and fifteen minutes for Intel. Returns are log price changes; volumes and transaction counts are increments over the same intervals. Table I gives these observation counts and return moments:

| Series | Observations | Mean log return | Return variance | Skewness | Ordinary kurtosis |
|---|---:|---:|---:|---:|---:|
| Cisco, 1 minute | 101,707 | $4.229270\times10^{-6}$ | $4.997559\times10^{-7}$ | 0.226555 | 40.85210 |
| Cisco, 10 minutes | 10,171 | $4.228270\times10^{-5}$ | $3.475961\times10^{-6}$ | 0.319438 | 17.04383 |
| Intel, 5 minutes | 20,352 | $-5.2863\times10^{-6}$ | $1.024171\times10^{-6}$ | −0.095227 | 21.22836 |
| Intel, 15 minutes | 6,784 | $-1.5839\times10^{-5}$ | $7.096932\times10^{-7}$ | −0.174604 | 12.26814 |

Kurtosis is compared with the Gaussian value 3, not zero. The unusually high one-minute Cisco value is the main distributional problem the clock model seeks to explain. Variances across horizons should be reproduced as printed before imposing a variance-proportional-to-time benchmark; Intel's displayed fifteen-minute variance is below its five-minute variance. The PDF does not resolve whether all surprising cross-horizon differences arise from sampling, scaling, or construction choices.

Several necessary data decisions are absent: the precise exchange-session calendar; endpoint interpolation or previous-tick rule; treatment of intervals without trades; overnight returns; split adjustments; trade corrections and outlier screening; and the scaling applied to the activity variables in the tables. The paper says the plotted activity axes are in real values but does not provide a complete units ledger. A replicator should establish these choices from the raw data and report them, rather than infer a trade-size unit from the apparent magnitude of a coefficient.

There is also no holdout sample or rolling training design. The exercise estimates relationships and transformations within the same year for two actively traded technology companies. Claimed supporting evidence from futures and an additional index refers to other research, not a separately documented replication sample in this PDF.

## Comparing volume and transaction count as volatility regressors

The first stage removes short-horizon conditional-mean dependence with twelve lagged returns:

$$
Y_t=\sum_{j=1}^{12}d_jY_{t-j}+\epsilon_t.
$$

The displayed equation contains no intercept. The authors report similar results with ten to fifteen lags. They form

$$
\widehat s_t=\sqrt{\frac{\pi}{2}}|\widehat\epsilon_t|.
$$

For a zero-mean Gaussian innovation with conditional standard deviation $s_t$, the expectation of this transformed absolute residual equals $s_t$. For a non-Gaussian innovation, unbiasedness does not follow merely from the multiplier. This is a proxy for the level of conditional volatility, despite the source's language of a volatility “change”; no first difference is taken.

Three regressions compare activity measures while retaining twelve lags of the volatility proxy:

$$
\widehat s_t=\alpha+\beta V_t+\sum_{j=1}^{12}\rho_j\widehat s_{t-j}+u_t,
$$

$$
\widehat s_t=\alpha+\gamma N_t+\sum_{j=1}^{12}\rho_j\widehat s_{t-j}+v_t,
$$

$$
\widehat s_t=\alpha+\beta V_t+\gamma N_t+
\sum_{j=1}^{12}\rho_j\widehat s_{t-j}+w_t.
$$

Thus the phrase “transactions alone” means transactions are the sole contemporaneous activity regressor, not that the regression omits lagged volatility. Current volume and counts are observed over the return interval; these regressions explain contemporaneous volatility rather than forecast it using only prior information.

Table II reports adjusted fits:

| Series | Volume plus lags | Count plus lags | Both plus lags |
|---|---:|---:|---:|
| Cisco, 1 minute | 0.167614 | 0.214708 | 0.215899 |
| Cisco, 10 minutes | 0.140566 | 0.199388 | 0.201327 |
| Intel, 5 minutes | 0.203811 | 0.286968 | 0.287031 |
| Intel, 15 minutes | 0.182301 | 0.227614 | 0.229031 |

The table's panel headings are awkward: the right-hand upper block is labeled ten-minute returns, while the left-hand lower block is five-minute returns. The allocation above follows the explicit sample construction and interval labels rather than interpreting each column as one company throughout.

The count measure adds substantial fit relative to volume in every comparison. Once count is included, the extra adjusted fit from volume ranges from 0.000063 to 0.001939. That supports a small incremental contribution, not an exact zero coefficient or proof that transaction size contains no information.

For example, Cisco's one-minute count coefficient is $3.82534\times10^{-4}$ with reported standard error $1.08\times10^{-5}$ in the count specification, and $3.54379\times10^{-4}$ with standard error $9.8\times10^{-6}$ when volume is added. The volume coefficient remains positive, $1.09674\times10^{-5}$ with standard error $3.78\times10^{-6}$. Statistical significance of that coefficient and a very small incremental fit can coexist in a sample exceeding 100,000 intervals. The source does not describe a dependence-robust standard-error procedure sufficiently to reconstruct it.

## Density estimation and what smoothing does not establish

The Gaussian kernel density estimator is

$$
\widehat f(x)=\frac{1}{nh}\sum_{i=1}^n
\frac{1}{\sqrt{2\pi}}
\exp\left[-\frac{(x-x_i)^2}{2h^2}\right],
\qquad h=s\left(\frac43\right)^{1/5}n^{-1/5},
$$

where $s$ is the sample standard deviation. The inverse fifth power of $n$ is essential. Figures 1–3 apply this smoothing to returns, volume, and counts. Calendar-time return densities have more mass near the center and in the tails than the comparable normal shape, while the activity distributions are asymmetric and vary across sampling intervals.

A finite Gaussian kernel mixture has moments of every order. That fact does not prove that the unknown population return distribution has six finite moments. The article's smoothness argument should therefore be interpreted as a property of its fitted density, not a general resolution of the high-order-moment existence problem. Likewise, smoothing a nonnegative count with an unrestricted Gaussian kernel assigns some fitted mass to negative values unless a boundary correction is imposed. No boundary correction is specified.

These qualifications matter because the next stage matches high-order moments and exponential moments. Those quantities are especially sensitive to rare observations, finite-sample smoothing, and the assumed support of the mixing variable.

## Moment equations and a corrected route to implementation

Let $m=E[H]$ and $c_j=E[(H-m)^j]$, with $c_2=\operatorname{Var}(H)$. Conditional expectation yields

$$
E[Y]=\mu m,\qquad
\operatorname{Var}(Y)=\sigma^2m+\mu^2c_2,
$$

$$
E[(Y-EY)^3]=3\mu\sigma^2c_2+\mu^3c_3,
$$

$$
E[(Y-EY)^4]
=\mu^4c_4+6\mu^2\sigma^2(c_3+mc_2)
+3\sigma^4(c_2+m^2).
$$

With negligible drift, the ordinary kurtosis becomes approximately $3E[H^2]/E[H]^2=3(1+c_2/m^2)$. Random clock increments can therefore produce substantial leptokurtosis even when every conditional innovation is Gaussian. This is a mixture mechanism, not evidence that the observed clock has been uniquely identified.

Appendix A prints formulas through order six. A robust implementation can derive every central moment directly from the conditional Gaussian representation:

$$
E[(Y-EY)^n]=
\sum_{j=0}^{\lfloor n/2\rfloor}
\binom{n}{2j}(2j-1)!!\,
\mu^{n-2j}\sigma^{2j}
E[(H-m)^{n-2j}H^j],
$$

with $(-1)!!=1$. Expand $H^j=((H-m)+m)^j$ to express each term in $m,c_2,\ldots,c_n$. This formula follows by retaining only even powers of the independent standard normal innovation.

It also exposes a specific printed error: the last term of the fifth-central-moment formula should be $30\mu\sigma^4mc_2$, whereas Appendix A prints $30\mu\sigma^4c_2$, omitting the clock mean. Indeed, the relevant expectation is $15\mu\sigma^4E[(H-m)H^2]=15\mu\sigma^4(c_3+2mc_2)$. The corrected equation is a derivation in this note; the actual original estimation code is unavailable, so its use or nonuse of the printed error cannot be determined.

Six return moments alone leave eight unknown quantities if estimating $\mu,\sigma^2,m,c_2,\ldots,c_6$. The authors add matching conditions involving exponential transforms. There is also a time-unit invariance: replacing $H$ by $cH$, $\mu$ by $\mu/c$, and $\sigma$ by $\sigma/\sqrt c$ leaves the return distribution unchanged. Linking the clock to observed transaction units or imposing another scale normalization is necessary to interpret parameter magnitudes.

## Constrained exponential-moment matching

For a real evaluation point $b$, independence gives

$$
M_Y(b)=E[e^{bY}]=E[e^{A(b)H}],
\qquad A(b)=b\mu+\tfrac12b^2\sigma^2.
$$

Appendix B approximates this expectation with a fourth-order expansion around the clock mean:

$$
\widetilde M_Y(b)=e^{A(b)m}
\left[1+\frac{A(b)^2c_2}{2}
+\frac{A(b)^3c_3}{6}
+\frac{A(b)^4c_4}{24}\right].
$$

The empirical counterpart is $\widehat M_Y(b)=n^{-1}\sum_i e^{bY_i}$. Choose evaluation points $b_1,\ldots,b_k$ and minimize

$$
\sum_{j=1}^k[\widetilde M_Y(b_j)-\widehat M_Y(b_j)]^2
$$

subject to equality between the selected empirical return moments and their theoretical expressions. The source reports essentially unchanged estimates under different sets of evaluation points and when using uncentered rather than centered moment constraints.

This is not exact maximum likelihood, nor an exact use of the clock's unknown transform: it truncates the centered expansion. The PDF supplies neither the actual $b_j$ values and their count, the exact constraint set, optimizer and initialization, parameter bounds, identification normalization, nor the standard-error calculation behind Table III. It merely cautions against extremely small or large $b$ values. An exact numerical reproduction cannot recover those missing settings from the displayed criterion.

Population exponential moments may fail to exist even when many polynomial moments exist. In particular, a lognormal nonnegative clock has no finite positive-argument moment-generating function. A finite empirical exponential sum is still computable, but that does not validate its interpretation as a consistent estimate of a finite population transform at every selected $b$. A reproducing researcher should check transform existence or use a separately justified transform-based alternative, explicitly labeling any departure from the paper.

## Reported clock estimates and a nonnegativity check

For Cisco at one minute, Table III reports $\mu=1.371329\times10^{-5}$, $\sigma^2=1.619712\times10^{-6}$, clock mean 0.3084067, variance 1.2028836, and third central moment −0.01967611. Their reported standard errors are $6.48208\times10^{-6}$, $3.56967\times10^{-7}$, 0.00237, 0.57329, and 0.00474 respectively. These are uncertainty estimates attached to the optimization, not a fully specified sampling distribution supplied for the fitted clock process.

The higher central moments approximately match those of transaction counts. For example, the empirical one-minute count variance is 1.201186697 and its third central moment −0.01931194, while its mean is 2.176064578. Matching centered moments after shifting the mean is the evidence behind the recentered-count interpretation. It does not determine a complete probability law from a finite moment list.

There is a stronger feasibility problem if the printed estimated clock moments are interpreted literally as moments of a nonnegative increment. Cauchy–Schwarz requires

$$
(E[H^2])^2\leq E[H]E[H^3].
$$

Using the one-minute estimates, $E[H^2]=c_2+m^2\approx1.298$ and $E[H^3]=c_3+3mc_2+m^3\approx1.123$. The left side is about 1.685 and the right side about 0.346, violating the inequality by far more than rounding. Thus that point-estimate moment vector cannot describe a nonnegative random variable as written. This diagnostic is calculated here from Table III; it is not a test reported by the authors.

Recentering the clock upward to match the count mean can change feasibility, but it also changes the conditional return mean and variance unless other parameters or the transformation are adjusted. The PDF does not give a complete operational recipe reconciling this step with the fitted mixture. One should not directly insert the published moment vector into a positive-clock simulator or assume that an additive shift leaves the original return law intact.

## Normality findings and their proper scope

Figures 4 and 5 display near-Gaussian fitted densities and approximately straight quantile plots after conditioning on the recentered number of trades. The reported chi-square statistics, in the sequence Cisco one/ten minutes and Intel five/fifteen minutes, are 5.21, 7.09, 6.34, and 8.25. The stated one-percent critical value is 11.6. Corresponding Jarque–Bera statistics are 0.337, 3.256, 1.440, and 3.907, all below the stated one-percent critical value 9.21.

These are failures to reject normality under the paper's transformation and tests. They do not prove exact Gaussian tails, independence across intervals, or stable behavior in other years and securities. The chi-square bin definitions, degrees of freedom, treatment of fitted parameters, and dependence corrections are not specified. Those omissions prevent reconstruction of test size from the statistics alone.

If positive interval clocks were observed and the model held, the natural standardized residual would be $(Y_t-\mu H_t)/(\sigma\sqrt{H_t})$. That is a model-implied diagnostic, not an explicitly supplied formula for the exact “conditional recentered series” behind the published plots. The article does not fully explain whether that series uses resampling into fixed transaction blocks, residual standardization, or another conditioning-and-recentering operation. A replication should state its transformation and distinguish it from a claim to have recovered the authors' undocumented procedure.

## Stochastic volatility, option discussion, and practical use

For an absolutely continuous clock $C(t)$, its instantaneous rate controls calendar-time variance: $d\langle\sigma B_C\rangle_t=\sigma^2dC(t)$. Variable trading intensity therefore supplies a stochastic-volatility mechanism; a jumping clock can additionally generate discontinuous returns. Neither a static clock-moment fit nor the contemporaneous regressions estimate a complete dynamic law for that intensity.

Section IV illustrates a variance-budget stopping time, defined by $\int_0^{\tau_b}\sigma_s^2ds=b^2T$, and discusses a Hull–White-style lognormal variance process. It points to external Laplace-transform results for the distribution of this hitting time. The current article supplies no numerical pricing or hedging experiment. Meeting an integrated-variance budget is not by itself a proof that an arbitrary stochastic-volatility hedge perfectly replicates the original fixed-calendar-maturity option. Risk-neutral clock dynamics, dependence between prices and variance, interest and dividend timing, and the contract's stopping-time interpretation must also be specified.

The practical research takeaway is to compare transaction activity with volume while keeping the information timing explicit, then ask whether a positive, dynamically coherent clock removes distributional misspecification. Reproduction should first match the four raw-data panels and the lag-controlled regressions, then resolve scale identification, support restrictions, moment formulas, and the exact conditioning transformation before using the clock for simulation or risk. The article provides suggestive evidence that transaction count is informative about volatility; its printed numerical procedure is not a complete ready-to-run positive-clock model.

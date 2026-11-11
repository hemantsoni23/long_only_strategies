# Estimating Quadratic Variation Using Realized Variance

**Ole E. Barndorff-Nielsen and Neil Shephard (2002).** *Journal of Applied Econometrics* 17, 457–477. DOI: 10.1002/jae.691. Source: [RealizedVariance_BarndorffNielsenShephard_2002.pdf](../../Finance/RealizedVariance_BarndorffNielsenShephard_2002.pdf). All 21 supplied pages, including the technical examples and references, were read. Central equations and all five figures were checked visually. Printed journal pages are used below.

## Why this matters and the paper's contribution

Realized variance is often treated as if it were observed volatility. This article explains why consistency does not justify that practice. The sum of squared intraperiod returns converges to quadratic variation under broad assumptions, but finite-sample measurement error can remain large. Moreover, quadratic variation need not equal the latent conditional variance one intended to measure in a model with jumps or a discontinuous random clock.

The authors specialize to a stochastic-volatility model in which quadratic variation is integrated variance and a feasible central limit theorem is available. They construct standard errors using fourth powers of the same observed returns, prefer a log transformation for confidence intervals, and apply the method to intraday exchange rates and annual stock-index volatility. The main empirical finding is that measurement uncertainty is economically significant even with hundreds of observations per interval, particularly when movement is concentrated into a few large returns.

This paper presents and applies limit theory developed in companion work; it is not the original proof of every asymptotic result cited. Its distinctive contribution is the disciplined separation of the target, estimator, and estimation precision, together with the first empirical interval illustrations emphasized by the authors. For a reproducing researcher, the key output is a variance estimate accompanied by a conditional measurement-error estimate, not a new return forecast or a trading strategy.

## Observation scheme and the target

Let $Y_t$ be a log-price process. Fix a reporting interval of length $h$, such as a day or a year, and sample $M+1$ equally spaced prices. For reporting interval $i$, define

$$
r_{j,i}=Y_{(i-1)h+jh/M}-Y_{(i-1)h+(j-1)h/M},
\qquad j=1,\ldots,M.
$$

The observed statistic is

$$
RV_i=\sum_{j=1}^{M}r_{j,i}^2.
$$

The paper reserves “realized volatility” for $\sqrt{RV_i}$ and uses “realized variance” for the sum itself. Neither statistic is a sample variance divided by $M$. The unscaled sum estimates accumulated variation over the entire reporting interval. Using percentage instead of decimal log returns multiplies $RV$ by $10^4$ and fourth-power sums by $10^8$, so data and reported units must remain consistent.

For a semimartingale $Y=A+M^Y$, where $A$ has locally finite variation and $M^Y$ is a local martingale, quadratic variation is the probability limit of the sum of squared increments along refining partitions. If the mesh tends to zero,

$$
RV_i\xrightarrow{p}[Y]_{ih}-[Y]_{(i-1)h}.
$$

In general,

$$
[Y]_t=[Y^c]_t+\sum_{0<s\le t}(\Delta Y_s)^2,
$$

where $Y^c$ denotes the continuous local-martingale component. If the finite-variation component $A$ is continuous, it contributes no quadratic variation, and $[Y]=[M^Y]$. If it jumps, jump squares and cross terms matter. Thus one should not identify quadratic variation with continuous integrated variance without a restriction excluding price jumps.

Convergence in probability alone gives neither a usable finite-sample variance nor a convergence rate. Nor does it establish convergence of expectations. These are separate assertions requiring additional regularity or integrability. The authors' comments about the limitations of general semimartingale theory describe the scope of their argument and the literature available at publication, rather than a claim about all subsequent probability results.

## A counterexample: a random clock is not recovered exactly by quadratic variation

Section 2.3 considers Brownian motion evaluated at an independent subordinator, $Y_t=B_{\tau_t}$. Conditional on the clock, $Y_t$ has variance $\tau_t$. The pure-jump clock case is fundamentally different from continuous integrated variance.

For the simple example where $\tau_t=N_t$ is a Poisson process,

$$
Y_t=\sum_{k=1}^{N_t}Z_k,\qquad Z_k\overset{iid}{\sim}N(0,1),
$$

$$
[Y]_t=\sum_{k=1}^{N_t}Z_k^2.
$$

Conditional on $N_t$, the quadratic variation is chi-squared with $N_t$ degrees of freedom. It has conditional mean $N_t$ and variance $2N_t$, so knowing quadratic variation is not equivalent to knowing the clock. Arbitrarily frequent observations remove discretization error in measuring $[Y]$, but do not remove the difference between $[Y]$ and $N_t$.

This example explains why a model's economically meaningful latent variance must be specified before an estimator is interpreted. The source describes subordinators as pure-jump processes in this discussion; technically a general subordinator may also have deterministic drift. The example and the stated distinction concern the pure-jump clocks being used, not every possible increasing time change.

## The stochastic-volatility model and its actual assumptions

The principal model is

$$
Y_t=A_t+\int_0^t\sigma_s\,dW_s,\qquad \sigma_s>0.
$$

The article assumes that the pair $(A,\sigma)$ is independent of the driving Brownian motion $W$. Its stated sufficient regularity conditions in Section 3.1 are:

1. $A$ and $\sigma^2$ have locally bounded-variation paths.
2. For each finite horizon and mesh $\delta=t/M$, the maximum $\delta^{-1}|A_{j\delta}-A_{(j-1)\delta}|$ remains bounded as $\delta$ decreases.

The second condition is implied by a local Lipschitz condition and makes $A$ continuous. It holds, for example, for an integrated drift $A_t=\int_0^t g(\sigma_s)ds$ under the stated path regularity and a suitably smooth $g$.

These assumptions allow deterministic intraday seasonality, jumps in spot volatility, serial dependence, nonstationarity, and even the absence of some unconditional moments. They do not allow jumps in the log price. Independence from $W$ also excludes the usual contemporaneous leverage correlation between return shocks and volatility shocks. Bounded variation of $\sigma^2$ is a particular sufficient path assumption; a general diffusion variance process does not satisfy it. References to Heston and other stochastic-volatility models motivate the literature but do not remove the assumptions of the result stated here.

Conditionally on the drift and volatility path, the return over interval $i$ is normal with mean $A_{ih}-A_{(i-1)h}$ and variance

$$
IV_i=\int_{(i-1)h}^{ih}\sigma_s^2\,ds.
$$

The continuous-path model gives $[Y]_{ih}-[Y]_{(i-1)h}=IV_i$, so $RV_i$ consistently estimates exactly this target. The target is the variance accumulated over a realized volatility path. It is not automatically the variance of tomorrow's return conditional only on today's information, which involves an expectation over future volatility and possibly drift uncertainty.

## Feasible measurement-error inference

Define the fourth-power sum and integrated quarticity,

$$
Q_i=\sum_{j=1}^{M}r_{j,i}^4,
\qquad IQ_i=\int_{(i-1)h}^{ih}\sigma_s^4\,ds.
$$

The realized-quarticity consistency result is

$$
\widehat{IQ}_i=\frac{M}{3h}Q_i\xrightarrow{p}IQ_i.
$$

The factor three is the fourth moment of a standard normal innovation. Locally, a return has variance about $\sigma_s^2h/M$, and its fourth moment is about $3\sigma_s^4(h/M)^2$. Summing and rescaling recovers the quarticity integral. This argument explains the normalization; the rigorous result is attributed to the authors' companion power-variation work.

The asymptotic distribution in equations (5) and (20) is

$$
\frac{RV_i-IV_i}{\sqrt{(2/3)Q_i}}\xrightarrow{\mathcal L}N(0,1).
$$

Equivalently, the unobservable but theoretically informative normalization is

$$
\frac{\sqrt M(RV_i-IV_i)}{\sqrt{2h\,IQ_i}}
\xrightarrow{\mathcal L}N(0,1).
$$

Thus the standard error is of order $M^{-1/2}$, with a random scale determined by the realized quarticity. The unstandardized limit is mixed Gaussian. Treating that scale as a fixed common variance across days loses the central source of heteroskedasticity in the measurement error.

The feasible raw-scale estimate of measurement-error variance is $s_i^2=(2/3)Q_i$. Its square root does not require fitting a particular parametric drift or volatility process. “Model free” in this limited sense means no such parametric specification is needed within the model class; it does not mean robust to arbitrary microstructure noise, jumps, endogenous observations, or violations of the independence assumption.

A raw normal interval for $IV_i$ is $RV_i\pm1.96s_i$. This can have a negative lower endpoint. More importantly, the authors' companion simulations indicate that a log transformation improves finite-sample approximation. Equation (6), repeated as (21), gives

$$
\frac{\log RV_i-\log IV_i}{s_i/RV_i}
\xrightarrow{\mathcal L}N(0,1).
$$

For $RV_i>0$, a 95% interval for integrated variance is therefore

$$
\left[RV_i\exp\left(-1.96\frac{s_i}{RV_i}\right),
RV_i\exp\left(1.96\frac{s_i}{RV_i}\right)\right].
$$

Taking the square roots of these endpoints gives an interval for integrated volatility $\sqrt{IV_i}$. Its equivalent log-volatility standard error is $s_i/(2RV_i)$. The direct delta-method standard error for $\sqrt{RV_i}$ is

$$
\frac{s_i}{2\sqrt{RV_i}}=\sqrt{\frac{Q_i}{6RV_i}},
$$

matching equation (7). A zero realized variance makes the log construction undefined; the source gives no data-repair rule for that case. An implementation must report or separately handle it, not insert an arbitrary positive constant and claim exact replication.

### Why concentration of movement matters

Quarticity weights large intraperiod returns heavily. The Cauchy–Schwarz inequality implies $h\,IQ_i\ge IV_i^2$, with equality for constant spot variance over the interval. Hence the asymptotic relative standard error is at least approximately $\sqrt{2/M}$ in the ideal model, and it increases when volatility is concentrated in time. This lower-bound calculation is a direct implication of the displayed theory, not a separately reported empirical result.

For constant volatility and $M=288$, the benchmark relative standard error is about 8.33%; at $M=144$, about 11.79%. Bursts can make the error substantially larger. Two years with equally large integrated variance can therefore have quite different measurement precision if one year's movement is concentrated in a few days and the other's is distributed broadly.

The theory does not require an unconditional fourth moment of returns merely to formulate this pathwise, mixed-limit statement under the given assumptions. If that unconditional moment does not exist, however, the unconditional variance or mean squared error of the estimator may not exist. A conditional asymptotic pivot and an unconditional MSE calculation are different claims.

## Conditional expectations: when realized variance can support forecasting

Section 2.4 writes the conditional return variance as

$$
\operatorname{Var}(Y_h\mid\mathcal F_0)
=E([M^Y]_h\mid\mathcal F_0)
+\operatorname{Var}(A_h\mid\mathcal F_0)
+2\operatorname{Cov}(A_h,M^Y_h\mid\mathcal F_0).
$$

The moment identities require the relevant integrability, such as square-integrability of the martingale; they should not be invoked for every arbitrary local martingale without checking expectations exist. If the drift-variance and covariance terms vanish and $A$ is continuous, conditional expected quadratic variation equals conditional return variance. If the terms are merely small, the equality is only an approximation.

For conditional expected realized variance to converge to that object, the discretized drift's squared-increment sum and its cross sum with martingale increments must also have conditional expectations tending to zero. Probability convergence alone is insufficient. The paper lists these five sufficient conditions explicitly: continuous drift, zero conditional drift-return covariance, zero conditional drift variance, and vanishing expectations of the two discretized drift terms.

A useful quantitative condition in Section 3.3 is

$$
E[(A_{t+\delta}-A_t)^2\mid\mathcal F_t]
=O(\delta^{1+\gamma}),\qquad \gamma>0,
$$

uniformly in $t$. Summing $O(\delta^{-1})$ intervals gives an $O(\delta^\gamma)$ drift-square contribution. The OU example takes a nonnegative stationary process $\tau$ driven by a subordinator,

$$
d\tau_t=-\lambda\tau_tdt+dz_{\lambda t},
\qquad A_t=\int_0^t\tau_u\,du,
$$

with an independent Brownian return driver. Its finite-moment bounds illustrate $\gamma=1$. The printed integral defining $A$ on p. 470 has a malformed differential; the finite-variation interpretation above follows the immediately subsequent identity $A_t=\lambda^{-1}[z_{\lambda t}-\tau_t+\tau_0]$. No Brownian differential can replace $du$ while preserving that identity.

The example also emphasizes that missing moments can defeat a conditional-expectation argument even when a pathwise consistency statement survives. A forecast model for tomorrow's $RV$ should therefore acknowledge both today's measurement error and the assumptions connecting conditional expected quadratic variation to the desired return variance.

## Exchange-rate experiment

The exchange-rate series is USD/Deutsche Mark from the Olsen Group, using the most recent Reuters quote every five minutes from 1 December 1986 through 30 November 1996. A day supplies up to 288 five-minute returns. The available evenly spaced subsamplings have

$$
M\in\{288,144,96,72,48,36,32,24,18,16,12,9,8,6,4,3,2,1\}.
$$

The authors make small missing-data adjustments that differ from an earlier Andersen and coauthors study and refer to companion work for full cleaning details. The supplied article does not specify all quote filters, day-boundary conventions, weekend exclusions, or interpolation choices. It also does not explicitly state the plotted return rescaling in a way that should be guessed from the axes alone. Exact numerical reproduction requires the original cleaned series or those additional conventions.

Figure 1 shows the first nine days, varying $M$ from 8 to 288 and plotting the log-based 95% intervals. Increasing frequency usually narrows uncertainty, but the intervals can remain wide at the finest five-minute resolution. Figure 2 fixes $M=144$, corresponding to ten-minute returns, for the first 50 days. Large realized-variance days often have much larger absolute uncertainty. These plots establish that consistency does not justify treating a ten-minute-based variance estimate as error-free.

The paper's statement that intervals can exceed the level of volatility is descriptive, not a calibrated frequency claim. It does not supply a table of coverage percentages or observed latent variance, which is unavailable in these real data. The intervals are approximate inference under the maintained continuous stochastic-volatility model.

### Signature plots and a normalization issue

For all 2,448 included days, Figure 3 plots $N^{-1}\sum_iRV_i$ against $M$. If the idealized model accurately described the observation process, changes in sampling frequency should not systematically change the target mean integrated variance. Instead, the figure turns upward at high frequencies; the paper describes an increase of around 10% and points to problems above about 50 observations per day. These are sample-specific diagnostics, not a universally optimal sampling frequency.

There is a consequential normalization issue in printed equation (24). It gives the variance of an average measurement error as $(2/3N)\sum_iQ_i$. Summing the individual conditional measurement-error variances and dividing by $N^2$ instead gives the leading-order estimated variance

$$
\widehat{\operatorname{Var}}\left(\frac1N\sum_i(RV_i-IV_i)\right)
=\frac{2}{3N^2}\sum_iQ_i
$$

when cross-interval measurement errors are orthogonal under the maintained model. The printed expression is larger by a factor of $N$; it is an average of individual error variances rather than a variance of their average. Cross-interval covariances would need separate treatment if the assumptions failed. The available article does not establish whether its plotting code used the printed scaling, so the figure's confidence bands should not be reverse-engineered by silently assuming either version.

The authors themselves caution that the signature-plot standard errors rely on several assumptions. Moreover, if market microstructure already invalidates the observation model at large $M$, model-based confidence intervals do not automatically give correctly sized tests there. The upward pattern is evidence that the ideal model requires scrutiny, not an implemented correction for noise.

## Annual Dow Jones illustration

The stock series contains daily Dow Jones Industrial Average closes from 26 May 1896 through 31 December 2001, obtained from the index's website. The index is narrow; it was chosen in part because its history was publicly downloadable. The authors note small recording breaks and changes from six-day to five-day trading weeks. Annual realized volatility is calculated by taking the square root of the sum of daily squared log returns, with the log-based interval transformation above.

The paper reports a large 1914 recording break from 30 July to 31 December, with the index changing from 71.42 to 54. Rather than assigning the entire observed endpoint change to a single daily return, the authors stochastically interpolate log prices with a Brownian bridge around the line joining endpoints. These are the source's stated dates and levels; they describe its series treatment.

For reconstruction, if the missing segment spans $L$ daily steps, a compatible log bridge is the linear endpoint interpolation plus $\sqrt q[B_s-(s/L)B_L]$, where $q=.04/110$ is the stated variance per day and the Brownian increments are on the daily time scale. This formula makes explicit the source's described construction. The paper says this corresponds to annual movement standard deviation around .33 and regards that as moderately high for the period. It does not disclose the random seed or a complete calendar of inserted observations, so the precise interpolated path is not reproducible from the PDF alone.

This treatment replaces missing observations with a model-conditioned path. It does not recover the actual hidden daily history, and the later intervals do not separately propagate uncertainty over alternative bridge imputations. The claim that 1914 is not exceptionally volatile in the resulting plot depends partly on the stipulated interpolation.

Figure 5 provides the striking contrast between 1987 and the 1930s. The 1987 volatility spike has a wide interval because daily data concentrate much of the year's movement in a very short span. Elevated 1930s volatility is sustained over many observations and can be measured more precisely relative to its level. The plot supports this qualitative comparison; the paper does not tabulate exact annual endpoints that would justify reporting highly precise numbers read from the graphic.

## Reimplementation and limits

A minimal implementation needs aligned log prices, the reporting intervals, and the sampling grid. Compute $RV$, the fourth-power sum, $s^2=2Q/3$, and the log variance interval. Convert to volatility only after the variance calculation. Preserve the actual count of observations and units, and record any repairs of missing or invalid prices. Do not use a Gaussian confidence formula for a noise-contaminated or jump-dominated series merely because it is easy to calculate.

The article's empirical programs are named `se_realised.ox` and `schwert.ox`, written in Ox. They are referenced, not embedded in the PDF. The article supplies no out-of-sample forecasting design, fitted forecasting hyperparameters, risk-managed portfolio, or trading-cost comparison. Its practical result is an inference layer for a measured input that other financial models often treat as known.

The strongest takeaway is that more frequent sampling changes both discretization precision and exposure to observation problems. Under the specified model, quarticity quantifies measurement error and explains why turbulent intervals can remain uncertain. In actual data, the target, sampling convention, missing-data treatment, and microstructure assumptions must be fixed before those standard errors can be interpreted as reliable measures of precision.

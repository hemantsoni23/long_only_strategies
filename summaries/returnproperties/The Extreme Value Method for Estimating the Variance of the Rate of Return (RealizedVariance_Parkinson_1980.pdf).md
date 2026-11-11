# The Extreme Value Method for Estimating the Variance of the Rate of Return

**Michael Parkinson (1980).** *The Journal of Business* 53(1), January, 61–65. Source: [RealizedVariance_Parkinson_1980.pdf](../../Finance/RealizedVariance_Parkinson_1980.pdf). All seven supplied PDF pages were read visually: five article pages followed by two citation pages. The paper is a short theoretical and simulation contribution; it does not estimate the method on a sample of traded stocks.

## Why this matters

A closing return records where a price finished but discards the distance it traveled during the interval. The high and low retain information about that movement even when the close happens to be near the open. Parkinson shows that the squared log high-low range estimates the variance of a driftless Brownian log-price much more precisely than a squared endpoint return using the same number of observation intervals.

The innovative component is an explicit estimator, its normalization from the Brownian range distribution, and an analytical comparison of sampling variances. It makes daily high-low records useful for estimating variance without requiring a complete intraday transaction history. Under the model, the range estimator needs about one-fifth as many intervals for the same variance of estimation error. That gain is conditional on continuous observation of the range, negligible drift, and a constant diffusion coefficient. It is not a universal assertion that any reported high and low improve every risk estimate fivefold.

For implementation, the central distinction is between variance over an interval and variance per unit time. A second distinction is between averaging squared ranges and squaring their average. The paper uses both moment relations and its numerical illustration switches between these two constructions. They have different finite-sample properties and should not be implemented as if they were the same estimator.

## The diffusion model and its conventions

Let $x_t$ follow a one-dimensional driftless Brownian motion with variance rate $D>0$. Its transition density from $x_0$ over elapsed time $t$ is

$$
f(x,t\mid x_0)=\frac{1}{\sqrt{2\pi Dt}}
\exp\left[-\frac{(x-x_0)^2}{2Dt}\right].
$$

Thus $\operatorname{Var}(x_t-x_0)=Dt$. Although the paper calls $D$ a diffusion constant, its convention is the variance rate, not the coefficient $D/2$ that would appear in the corresponding diffusion partial differential equation. Confusing these conventions introduces a factor of two.

For financial use set $x_t=\log S_t$, where $S_t>0$ is a stock price. The endpoint log return over length $\Delta$ is $r_i=x_{i\Delta}-x_{(i-1)\Delta}$. The model assumes independent increments with distribution $N(0,D\Delta)$. It does not assume that the arithmetic price increment has zero mean. Indeed, exponentiating a driftless Gaussian log price produces a positively biased arithmetic gross return.

The target is the variance $V=D\Delta$ of a log return over the measurement interval. Estimating an annual variance rate additionally requires a declared time scale. The article does not specify an annualization convention or a number of trading sessions per year. One should not silently multiply by an assumed trading-day count and call that a reported result.

The original statistical problem on p. 62 allows a sample mean to be removed from endpoint displacements. For unit intervals $d_i=x_i-x_{i-1}$, the conventional estimate is

$$
\widehat D_x=\frac{1}{n-1}\sum_{i=1}^n(d_i-\bar d)^2,
\qquad \bar d=\frac1n\sum_{i=1}^n d_i.
$$

In the financial application on p. 64, the mean is instead assumed zero and the baseline is $n^{-1}\sum_i r_i^2$. With unequal observation lengths these formulas require modification; the paper's comparison is for equal intervals.

## Brownian range moments and the estimator

Define the continuously observed range within one interval by

$$
R_\Delta=\sup_{0\le s\le\Delta}x_s-\inf_{0\le s\le\Delta}x_s.
$$

The starting level is irrelevant because the range is translation invariant. Brownian scaling implies $R_\Delta$ has the same distribution as $\sqrt{D\Delta}$ times the range of a standard Brownian motion over a unit interval. Parkinson uses the known extreme-value distribution, citing Feller, rather than deriving a new distribution of maxima and minima.

The decisive first and second moments on p. 62 are

$$
E[R_\Delta]=\sqrt{\frac{8D\Delta}{\pi}},
\qquad E[R_\Delta^2]=4\log(2)D\Delta.
$$

Consequently,

$$
D\Delta=\frac{\pi}{8}\{E[R_\Delta]\}^2
=\frac{1}{4\log 2}E[R_\Delta^2].
$$

The rounded coefficients printed in the paper are .393 and .361. A numerical implementation should use the exact constants, approximately .392699 and .360674. The distinction is small relative to many data problems, but using exact constants costs nothing and makes theoretical comparisons reproducible.

For $n$ nonoverlapping equal-length intervals, the squared-range estimator is

$$
\widehat V_P=\frac{1}{4n\log 2}\sum_{i=1}^nR_i^2,
\qquad \widehat D_P=\widehat V_P/\Delta.
$$

Under the maintained model it is unbiased for interval variance and variance rate respectively. No open or closing price is required once each interval's high and low have been accurately recorded. Positivity of the statistic follows directly from the squared ranges.

Since logarithm is monotone, a stock's high $H_i$ and low $L_i$ over exactly the same interval satisfy

$$
R_i=\log H_i-\log L_i=\log(H_i/L_i).
$$

This gives the familiar operational formula

$$
\widehat V_P=\frac{1}{4n\log 2}\sum_{i=1}^n
\left[\log\left(\frac{H_i}{L_i}\right)\right]^2.
$$

The statistic is a variance, not a standard deviation. Taking its square root gives a volatility estimate with a different sampling distribution and finite-sample bias. The paper's efficiency calculation below concerns estimation of $V$ or $D$.

The moment relation also yields the diagnostic

$$
\frac{E[R^2]}{\{E[R]\}^2}=\frac{\pi\log 2}{2}\approx1.08879.
$$

Parkinson rounds this to 1.09 and suggests comparing observed range moments with the relation. It is a model diagnostic, not a fully specified hypothesis test: the source supplies no critical values, power calculations, or correction for estimating both moments from the same dependent financial sample. A failure could reflect drift, changing volatility, noise, discrete observation, or other model departures rather than one uniquely identified mechanism.

## Why the estimator is more precise

For a zero-mean Gaussian endpoint return with variance $V$, $E[r^4]=3V^2$, so

$$
\operatorname{Var}\left(\frac1{N_x}\sum_{i=1}^{N_x}r_i^2\right)
=\frac{2V^2}{N_x}.
$$

If the mean is estimated and the sample variance uses $N_x-1$ degrees of freedom, the exact normal-model variance is $2V^2/(N_x-1)$. The paper's expression with $N_x$ is exact for the known-zero-mean second moment and is the corresponding large-sample comparison for an estimated mean.

The fourth range moment implied by the general moment formula on p. 62 is $E[R^4]=9\zeta(3)V^2$, where $\zeta$ is the Riemann zeta function. Therefore the squared-range estimator has

$$
\operatorname{Var}(\widehat V_P)
=\frac{V^2}{N_R}
\left[\frac{9\zeta(3)}{16(\log 2)^2}-1\right]
\approx\frac{0.4073V^2}{N_R}.
$$

The paper rounds the coefficient to .41. Equating this variance with the endpoint-return variance gives $N_x/N_R\approx2/.4073\approx4.91$, reported as about five. For the same number of intervals, the standard-error improvement is approximately $\sqrt{4.91}\approx2.22$. The variance improvement and standard-error improvement are different quantities; the introduction's broad “2½–5” description should not be treated as a single precise efficiency ratio.

The argument relies on independent, identically distributed ranges from constant-$D$ Brownian increments. In a time-varying-volatility setting, the average of interval estimates may still be informative, but the simple variance formula and the fivefold sample-size comparison do not automatically apply. In particular, reducing the window length by 80% can improve responsiveness only if the model remains locally appropriate; the paper does not optimize a bias-variance tradeoff for changing variance.

The analytical calculation supplies a model-based large-sample standard error $\widehat V_P\sqrt{.4073/n}$. A normal confidence interval built from it is a derived approximation, not an interval proposed or calibrated by the article. It may behave poorly for very small $n$ or under violations of Brownian independent increments.

## The simulation, including a change of estimator

Section IV generates 100 random walks, each containing 10,000 independent steps uniformly distributed on $(-1/2,+1/2)$. A step has variance $1/12$, so the variance over a complete walk is $10,000/12\approx833.33$. The paper treats a whole walk as one observation interval and records its terminal displacement $x_i$ and its maximum-minus-minimum range $R_i$.

This is a discrete uniform-increment approximation to Brownian motion, not exact continuous Brownian sampling. Finite-grid maxima and minima miss possible between-step extremes. The author uses a large number of small steps to approximate the continuous range model but does not provide a discretization-error study.

The reported summaries are:

| Quantity across 100 paths | Reported value |
|---|---:|
| Mean squared terminal displacement | 812.63 |
| Sample standard deviation of squared displacements | 1,164.60 |
| Mean range | 45.00 |
| Sample standard deviation of ranges | 14.3 |

Dividing the latter standard deviations by ten gives standard errors 116.46 for the mean squared displacement and 1.43 for the mean range. The article reports an endpoint estimate $813\pm116$ and a range estimate $795\pm51$, with the uncertainty interpreted as approximately one standard error, not as a 95% interval.

The range number here comes from $.393\bar R^2$, not from $.361\overline{R^2}$. For $\bar R=45$, the exact-constant first-moment plug-in is $(\pi/8)45^2\approx795.22$. Propagating the standard error of $\bar R$ through its square gives approximately $2(\pi/8)45(1.43)\approx50.54$. These derived calculations reproduce the reported rounded values.

The two range estimators should be kept separate. Squaring a sample average has positive finite-sample bias because $E[\bar R^2]=(E[R])^2+\operatorname{Var}(R)/n$. In contrast, the estimator based on the average squared range is exactly unbiased under the ideal model. The .41 analytical variance coefficient belongs to the latter. The numerical example confirms that range information can be substantially more precise, but does not directly report the .361-based estimator's realization or Monte Carlo coverage.

Footnote 5 gives unusual detail about the random-number generator because correlations could distort so many simulated increments. It uses the MacLaren–Marsaglia method: a table of 128 numbers from a congruential sequence with multiplier 65549 modulo $2^{31}$, with entries selected using another sequence with multiplier 65539 modulo $2^{31}$; each selected entry is replaced by the next number of the first sequence. The exact starting seeds, integer-to-uniform transformation, and complete code are not supplied. A modern independent-uniform generator can reproduce the experiment's design, but should not be expected to reproduce the four reported sample statistics exactly.

## Implementation boundaries and practical interpretation

To reconstruct the estimator, choose a fixed interval, collect positive highs and lows from that interval, verify $H_i\ge L_i>0$, calculate the log ratio, square it, and average with $1/(4\log2)$. Keep the number of intervals separate from their duration. For a comparison with closing returns, use the same sample and time coverage and state whether the mean is known zero or estimated.

The article motivates using published daily, weekly, or monthly highs and lows. It does not specify a stock universe, sample dates, adjustment for stock splits, handling of overnight moves, treatment of bad ticks, or transaction-price versus quote-price choice. There are no empirical return forecasts, portfolio constructions, trading costs, or out-of-sample performance tests to reproduce.

Several practical limitations follow from the assumptions. An intraday high-low range usually omits the price movement between the prior close and the next open, so it need not estimate the same variance as a close-to-close return. Sparse recording understates the continuous range, while an erroneous extreme print can greatly inflate it. Bid-ask effects and price discreteness are absent from the proof. Corporate actions need consistent adjustment of both extrema, and a range spanning a split should not be interpreted as an ordinary diffusion move. These are implementation implications, not problems empirically measured by Parkinson.

Nonzero log drift and price jumps also change the range distribution. The paper provides no drift correction, noise correction, or jump-robust estimator. Its financial claim that log prices approximately follow the assumed random walk is a modeling premise supported by cited literature, not a result established on new market data in this article.

The main takeaway is specific and reproducible: under a driftless constant-variance Brownian log-price, normalized squared high-low ranges use substantially more path information than endpoint returns and reduce estimator variance by about a factor of five. Applying that gain to real data requires matching the observed range, the target interval, and the model assumptions before interpreting a shorter estimation window as a more accurate risk measure.

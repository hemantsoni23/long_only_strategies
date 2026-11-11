# Realized range-based estimation of integrated variance

**Kim Christensen and Mark Podolskij (2007).** *Journal of Econometrics* 141, 323–349. DOI: 10.1016/j.jeconom.2006.06.012. Source: [RealizedVariance_ChristensenPodolskij_2007.pdf](../../Finance/RealizedVariance_ChristensenPodolskij_2007.pdf). All 27 PDF pages, including the proof appendix and empirical figures, were inspected. The earlier circulating title was *Asymptotic Theory for Range-Based Estimation of Integrated Variance of a Continuous Semi-Martingale*. References below use journal pages.

## Why this matters

A five-minute return uses two prices; a five-minute high–low range uses information from the entire path observed between those endpoints. Christensen and Podolskij show how to aggregate appropriately normalized intraday squared ranges into a consistent estimator of integrated variance, derive its mixed-normal limit, and correct the downward bias caused by observing the range on a finite grid. The theoretical variance can be about one fifth of the corresponding endpoint-return estimator’s variance when the full intrainterval path is available.

The gain has an important boundary. It is a comparison at the same number of coarse intervals, when one method also uses intermediate observations. It is not a claim that a range statistic dominates all uses of the same noise-free data. Nor is the proposed estimator intrinsically robust to microstructure noise or price jumps. The paper motivates moderate-frequency range aggregation because practical noise often prevents realized variance from using every available return, but its principal limit theory is for a continuous, noise-free semimartingale.

The novel components are a general time-varying-volatility framework for realized ranges, consistency and stable central limit theorems, feasible quarticity-based inference, and finite-grid normalization. The daily-range intuition alone does not deliver these results: intraday volatility varies, the range is a nonsmooth path functional, and the number of observations contributing to a high–low affects its scale.

## Model, target, and notation

Normalize the measurement horizon, usually one trading day, to $[0,1]$. The efficient log price is

$$
p_t=p_0+\int_0^t\mu_u\,du+\int_0^t\sigma_u\,dW_u.
$$

The drift is locally bounded and predictable; volatility is càdlàg. The price path is continuous. Quadratic variation therefore equals integrated variance,

$$
IV=\int_0^1\sigma_u^2\,du,
$$

and integrated quarticity is

$$
IQ=\int_0^1\sigma_u^4\,du.
$$

The target is realized ex-post variation over the observation horizon, not the conditional expectation of tomorrow’s variance and not necessarily a close-to-close quantity including overnight exposure. A forecasting model could subsequently use this measured series, but forecasting is not estimated in the article.

Divide the day into $n$ coarse intervals of length $\Delta=1/n$. The usual realized variance is $RV=\sum_{i=1}^n(p_{i/n}-p_{(i-1)/n})^2$. Under the standard regularity conditions, it converges to $IV$, and its asymptotic variance at rate $\sqrt n$ is $2IQ$. A corresponding quarticity estimator is $(n/3)\sum_i(\Delta p_i)^4$.

For the range, define

$$
R_i=\sup_{s,t\in[(i-1)/n,i/n]}(p_t-p_s)
=\max p-\min p
$$

within each interval. This is a range of **log prices**. The difference between the high and low in raw price units would have different scaling and is not the statistic in the theorem.

## Brownian range constants and the continuous-path estimator

Let $R_W=\max_{0\le t\le1}W_t-\min_{0\le t\le1}W_t$ and $\lambda_r=E(R_W^r)$. Brownian scaling implies that a constant-volatility, zero-drift process has $E(R_i^r)=\lambda_r\Delta^{r/2}\sigma^r$. In particular, $\lambda_2=4\log2$.

The continuous-path realized range-based variance is

$$
RRV=\frac1{\lambda_2}\sum_{i=1}^nR_i^2.
$$

For constant volatility, it is unbiased and

$$
\operatorname{Var}(RRV)=\frac{\Lambda\sigma^4}{n},
\qquad \Lambda=\frac{\lambda_4-\lambda_2^2}{\lambda_2^2}\approx0.4073.
$$

Compared with the coefficient two for realized variance, the variance ratio is approximately $0.4073/2=0.20365$. The standard-error ratio is its square root, about 0.451. Thus “five times greater precision” refers to an inverse-variance comparison; it does not mean that a confidence interval is five times narrower.

The range density, given on p. 328, can be represented by an alternating series of Gaussian densities. It is useful theoretically, but direct naive summation can be numerically unstable for some arguments. The paper’s implementable finite-grid method does not require fitting this density to market data: it uses simulated Brownian range moments for each grid size.

The first consistency theorem requires only the basic drift and càdlàg volatility conditions. It allows rich intraday variation, leverage through correlation with the price shock, and volatility paths with jumps, as long as the efficient price itself remains continuous. The drift contribution vanishes at the relevant law-of-large-numbers scale. This is a considerable extension of formulas that assume a constant daily diffusion coefficient.

## Central limit theorem and feasible inference

For the CLT, the article strengthens its assumptions. Volatility must not vanish and must itself admit the continuous semimartingale representation

$$
\sigma_t=\sigma_0+\int_0^t\mu'_u\,du+\int_0^t\sigma'_u\,dW_u+\int_0^t v'_u\,dB'_u,
$$

where $B'$ is independent of $W$, coefficient processes are càdlàg, and the drift meets the appropriate boundedness and predictability requirements. These are assumption V on p. 330. The broader consistency theorem should not be confused with this more restrictive CLT: the displayed volatility representation is continuous and does not itself include volatility jumps.

Theorem 2 establishes stable convergence,

$$
\sqrt n(RRV-IV)\ \Longrightarrow_{st}\ \sqrt\Lambda\int_0^1\sigma_u^2\,dB_u,
$$

where $B$ is independent of the original filtration. Conditional on the volatility path, the limit is Gaussian with variance $\Lambda IQ$; unconditionally it is mixed normal. The random mixing variance explains why the unconditional error distribution need not resemble a single Gaussian with fixed variance.

Stable convergence is stronger than ordinary convergence in distribution and permits joint use of a consistent quarticity estimator. Define

$$
RRQ=\frac n{\lambda_4}\sum_{i=1}^nR_i^4.
$$

Then $RRQ\to_p IQ$ and the feasible standardized error is

$$
\frac{\sqrt n(RRV-IV)}{\sqrt{\Lambda RRQ}}\Longrightarrow N(0,1).
$$

A first-order normal confidence interval is consequently $RRV\pm z_{1-\alpha/2}\sqrt{\Lambda RRQ/n}$. It can have a negative lower endpoint in small samples. The paper also develops log-based inference, which better matches its simulation distributions and preserves positive interval endpoints.

For unequal coarse interval lengths $\Delta_i$, the source introduces the limiting sampling-intensity function $H_u$, obtained from $n\sum_{t_i\le u}\Delta_i^2$. When its limit is differentiable, asymptotic variance becomes $\Lambda\int_0^1H'_u\sigma_u^4du$. Equidistant sampling gives $H_u=u$ and recovers the simple expression. This result should not be read as blanket permission for arbitrary endogenous observation times without the stated limiting conditions.

## Finite observation grids: the main practical correction

In real data, a high–low is observed at finitely many times. Suppose each coarse interval contains $m$ fine returns, so the whole day has $mn+1$ price observations. Within each interval, include both endpoints and all intermediate observations. The discrete range is

$$
R_{i,m}=\max_{0\le j\le m}p_{(i-1)/n+j/(mn)}
-\min_{0\le j\le m}p_{(i-1)/n+j/(mn)}.
$$

Define the analogous discrete Brownian range on $m+1$ equally spaced points, $R_{W,m}$, and constants $\lambda_{r,m}=E(R_{W,m}^r)$. Since intermediate continuous extrema are missed, $\lambda_{2,m}<\lambda_2$ for finite $m$. Dividing the observed squared range by $\lambda_2$ therefore produces downward bias even in an ideal Brownian experiment.

The proposed estimator uses the correct finite-grid normalization:

$$
RRV_m=\frac1{\lambda_{2,m}}\sum_{i=1}^nR_{i,m}^2.
$$

For $m=1$, the range is the absolute endpoint return, $\lambda_{2,1}=1$, and the estimator is exactly ordinary realized variance. As $m\to\infty$, the constants approach their continuous-range values. Theorem 3 establishes consistency uniformly in $m$ and a stable CLT when $m$ tends to a finite positive integer or infinity.

Set

$$
\Lambda_m=\frac{\lambda_{4,m}-\lambda_{2,m}^2}{\lambda_{2,m}^2},
\qquad RRQ_m=\frac n{\lambda_{4,m}}\sum_iR_{i,m}^4.
$$

Then the feasible standardized statistic uses $\sqrt{\Lambda_mRRQ_m}$ in the denominator. At $m=1$, $\Lambda_1=2$; at very large $m$ it tends to approximately 0.4073. Figure 3 gives about 0.7 for $m=10$, already a considerable improvement at a fixed coarse interval count.

These constants depend on the **number of increments**, not the number of price levels. A range from eleven prices has ten increments. Confusing those quantities gives an incorrect normalization, especially in sparse intervals. The initial price must be included when generating the Brownian range; using only cumulative increments without the zero starting point also changes the distribution.

The authors state that no explicit formula for the discrete constants is available to them and estimate them with 1,000,000 Monte Carlo repetitions. An implementation can draw $m$ independent $N(0,1/m)$ increments, prepend zero to their cumulative sum, compute the range, and average its second and fourth powers. The random seed is not reported. A reproducible implementation should store the simulated constant table and its numerical uncertainty, rather than recompute it with uncontrolled randomness for each day.

The correction solves finite-grid underobservation under the model. It does not remove bid–ask bounce, stale quotes, price rounding, or additive observation noise. In fact, spurious extremes can have a strong effect on a high–low. Calling the result a correction for non-trading effects must be distinguished from claiming full robustness to every market-data imperfection.

## How the proof works

The consistency proof freezes volatility at the beginning of each small interval. Its leading statistic is a sum of independent Brownian-range functionals conditional on the preceding information, with conditional means $\sigma_{(i-1)/n}^2/n$. The sum of those means converges to integrated variance. The sum of conditional variances is of order $1/n$ and vanishes.

The actual range differs from this frozen-volatility approximation because of drift and changing volatility. The range functional is controlled by suprema of the corresponding stochastic-integral errors. Burkholder and Cauchy–Schwarz inequalities, together with càdlàg paths and localization, make the aggregate remainder negligible. This is why time-varying volatility can be accommodated without assuming it is constant over a full trading day.

For the CLT, the centered frozen statistic is a martingale array. Its limiting conditional variance is $\Lambda IQ$. Symmetry of Brownian motion gives $E[W_1R_W^2]=0$, helping establish orthogonality to the original driving martingale and yielding an independent Brownian motion in the stable limit.

The nonsmooth maximum requires an additional argument. The appendix proves a directional derivative lemma: when a continuous function has a unique maximizer, a small perturbation changes its maximum to first order by the perturbing function evaluated at that maximizer. Brownian maxima and minima are almost surely unique. This allows the range’s first-order perturbation to be analyzed, and symmetry cancels the leading drift and volatility-variation terms.

The remaining Riemann-sum errors are controlled using the volatility semimartingale assumption. The discrete-range result follows through the same structure using finite-grid Brownian ranges and their moments. The proof therefore explains which assumptions are needed for consistency and which additional assumptions are needed for centered mixed-normal inference.

There is a typographical issue in Part II of the printed appendix, p. 345: the displayed centering identity contains a conditional second moment where a conditional first moment is required. For the defined difference $\zeta_i^n$, the centered sum must use $\zeta_i^n-E[\zeta_i^n\mid\mathcal F_{(i-1)/n}]$. The subsequent second-moment bound controls that centered sum’s variance. This correction preserves the proof mechanism and avoids propagating the printed identity into a derivation.

## Monte Carlo design and what it reports

Section 3 simulates a lognormal stochastic-volatility diffusion:

$$
dp_t=\sigma_t\,dW_t,
\qquad d\log\sigma_t^2=\theta(\omega-\log\sigma_t^2)dt+\eta\,dB_t,
$$

with independent Brownian motions. Parameters are $(\theta,\omega,\eta)=(0.032,-0.631,0.115)$, taken from an earlier empirical calibration. Initial conditions are $p_0=0$ and $\log\sigma_0^2=\omega$.

The experiment uses 1,000,000 daily replications, fixes $m=10$, and varies $n$ over 10, 50, and 100. Thus there are respectively 100, 500, and 1,000 fine increments per day. It compares the feasible standardized estimation error with a standard normal density. This is an estimator-distribution experiment, not a forecasting train/test design.

At $n=10$, the raw feasible statistic is visibly left-skewed and departs from normality in the center and tails. Larger $n$ improves the approximation; at $n=100$, tail agreement is much better. The paper presents kernel-density plots rather than a table of exact coverage percentages or empirical biases, so precise coverage improvements should not be invented from the figure.

The log delta method gives

$$
\sqrt n(\log RRV_m-\log IV)
\Longrightarrow MN\left(0,\frac{\Lambda_c IQ}{IV^2}\right).
$$

Its feasible standard error is $\sqrt{\Lambda_mRRQ_m/n}/RRV_m$. A positive interval for integrated variance is

$$
RRV_m\exp\left\{\pm z_{1-\alpha/2}\frac{\sqrt{\Lambda_mRRQ_m/n}}{RRV_m}\right\}.
$$

Figure 4 shows substantially better small-sample shape for the log-based statistic, with the $n=100$ density close to the normal reference. The square-root transformation also has a delta-method variance $\Lambda_cIQ/(4IV)$ at rate $\sqrt n$.

The PDF does not fully report the simulation time-discretization scheme for prices, numerical integration used to compute the latent $IV$, kernel bandwidth for plotted densities, or random seeds. A transparent reconstruction can exploit the exact Ornstein–Uhlenbeck transition for $X_t=\log\sigma_t^2$,

$$
X_{t+\delta}=\omega+e^{-\theta\delta}(X_t-\omega)
+\eta\sqrt{\frac{1-e^{-2\theta\delta}}{2\theta}}Z_t,
$$

and use a sufficiently fine scheme for the price integral and integrated variance. That transition is a mathematical implication of the specified model; the article does not state that its original code used this implementation. Discretization sensitivity should be reported if exact original code is unavailable.

### Finite-grid simulation details that determine the result

The Brownian constants and the estimator-distribution experiment are two distinct simulations. The first estimates universal normalization constants for a specified observation grid; the second generates prices under stochastic volatility and evaluates an estimator using those constants. Reusing a noisy constant estimate without tracking its error can introduce a small common scale error into every simulated or empirical day. With enough daily observations, that numerical bias can become more visible than daily sampling uncertainty.

For each chosen $m$, store estimates of $\lambda_{2,m}$ and $\lambda_{4,m}$ from the same simulated ranges. Their estimation errors are correlated, so uncertainty in $\Lambda_m=\lambda_{4,m}/\lambda_{2,m}^2-1$ should not be calculated by treating the two sample moments as independent. The article uses a million repetitions but does not tabulate Monte Carlo standard errors. For a modern reproduction, independent repeated batches or the empirical covariance of range powers provides a transparent diagnostic without altering the estimator's definition.

The lognormal diffusion experiment also depends on the time unit. The horizon is normalized to one day in the estimator theory; the quoted Ornstein–Uhlenbeck parameters should be used consistently with the source's daily replication convention. Changing the unit to years without transforming mean reversion and diffusion scale changes the intraday variation and therefore the finite-sample distribution being tested. The underlying exact transition provides a direct check that the variance of a log-volatility increment has the intended units.

For the feasible log statistic, the operational quantity is

$$
Z_{\log}=\frac{\sqrt n\,RRV_m(\log RRV_m-\log IV)}{\sqrt{\Lambda_mRRQ_m}}.
$$

The factor $RRV_m$ appears because the derivative of the logarithm is evaluated at the estimated variance. Omitting it would produce a statistic with the wrong scale. For the square-root statistic, the corresponding estimated derivative is $1/(2\sqrt{RRV_m})$. These transformations alter the approximation to sampling uncertainty, not the underlying daily point estimate.

A simulation should preserve the latent integrated variance separately from the observed-grid estimator. Using a very fine realized variance as though it were exact $IV$ adds a second approximation; using the same coarse grid for both target and estimator can conceal the error the experiment is meant to study. The article's reported density comparisons assume the true diffusion target can be evaluated in the Monte Carlo environment, but its numerical integration details are not supplied. Reporting a refinement check for the latent integral is therefore necessary for a transparent independent reconstruction.

## General Motors empirical experiment

The application uses General Motors TAQ data from 3 January 2000 through 31 December 2004, totaling 1,255 trading days. Only NYSE updates are retained, and reported results use the midpoint of bid and ask quotes. The authors also examine transaction data but do not report that parallel analysis in the article.

Raw records are filtered for irregularities including zero prices, timestamps outside the trading session, and negative spreads. A second procedure removes remaining price outliers. The exact thresholds and all quote-condition filters are not documented, leaving an important replication input. Since ranges are highly sensitive to isolated extremes, different plausible cleaning rules can materially change the comparison.

Table 1 reports average daily counts:

| Data type | All retained updates | After removing price repetitions | After additional reversal adjustment |
|---|---:|---:|---:|
| Trades | 2,220 | 960 | 558 |
| Quotes | 5,144 | 1,357 | 1,017 |

The paper labels the latter two columns using nonzero first differences and nonzero differences of returns after zero returns are removed. Its prose explains that simply counting nonzero changes overstates the effective number because of instantaneous reversals, and says repeated reversals are counted only once. The precise algorithm reconciling that prose with the count notation is not fully specified. A replicator should not assume that an arbitrary “remove bounce” filter recreates the authors’ effective $m$.

Both estimators are formed on 78 five-minute intervals over 9:30 a.m.–4 p.m., using previous-tick interpolation for endpoint returns in RV. The choice is guided by signature plots: sampling more frequently produced increasing evidence of microstructure contamination. The average effective quote count implies about $1,017/78\approx13$ increments per interval.

Counts vary across intervals. The source says to use each interval’s own $m$ rather than a daily average. For equal coarse interval lengths, the natural implementation is

$$
\widehat{IV}=\sum_i\frac{R_i^2}{\lambda_{2,m_i}}.
$$

A corresponding local variance estimate, obtained by applying the paper’s quarticity construction interval by interval, is

$$
\widehat V=\sum_i\frac{\Lambda_{m_i}}{\lambda_{4,m_i}}R_i^4.
$$

For constant $m$, this reduces to $\Lambda_mRRQ_m/n$. This intervalwise expression makes explicit an implementation implication of the varying-count discussion; the article’s main displayed theorem uses equal $m$. Handling an interval with no effective increments requires an explicit convention, which is not reported in the PDF.

Irregular tick arrival times create an additional approximation. Simulated constants for equally spaced Brownian observations depend only on $m$ under that design; for genuinely irregular within-interval times, the distribution of the sampled range can also depend on the spacing pattern. The empirical count correction should therefore not be described as a proven exact correction for arbitrary endogenous quote arrival schedules.

## Numerical findings and interpretation

Table 2 presents annualized percentage-variance statistics. The source values are:

| Statistic | RV | RRV |
|---|---:|---:|
| Mean | 7.276 | 6.212 |
| Time-series variance | 47.740 | 27.693 |
| Skewness | 3.624 | 3.056 |
| Non-excess kurtosis | 25.085 | 18.417 |
| Minimum | 0.472 | 0.496 |
| Maximum | 79.332 | 56.256 |

Their correlation is 0.982. The table’s annualized percentage convention is consistent with the plotted annualized decimal-variance series differing by a factor of 100, but the exact annualization day count is not explicitly documented. These are variances, not annualized standard deviations; taking a square root would be a further transformation.

RRV’s sample time-series variance is about 58% of RV’s. That is **not** an empirical estimate of the theoretical conditional estimation-error ratio $\Lambda_m/2$. The time-series variance combines variation in the latent target with measurement error, and both estimators are exposed to actual market departures from the diffusion model. The authors explicitly acknowledge this distinction.

Figure 5 shows a smoother but still volatile RRV path. Figure 6 restricts the display to 1 July–31 December 2002 and adds 95% log-based confidence intervals. Range intervals are visibly narrower and both estimators’ intervals widen in high-volatility periods. Without observed true integrated variance, narrower intervals and a smoother path do not directly establish empirical coverage or lower realized squared error.

Figure 7 gives the first 75 autocorrelations. Both measured-variance series are positively persistent, beginning around 0.60–0.70 and declining toward approximately 0.10–0.15. RRV’s ACF is generally higher and smoother, consistent with less independent measurement noise attenuating persistence. The authors suggest a possible forecasting application but do not run one.

The high 0.982 level correlation is offered as evidence that linear combinations may yield limited additional improvement. A rigorous optimal combination would require the covariance of **estimation errors**, rather than only the correlation of two series sharing the same latent target. The paper provides the joint asymptotic covariance structure involving $\operatorname{Cov}(W_1^2,R_{W,m}^2)/\lambda_{2,m}$ and reports exploratory simulations, but does not publish a fitted optimal combination or a forecast comparison.

## Implementation boundaries and practical conclusions

A faithful implementation needs two clocks: the coarse intervals over which variance is aggregated and the fine observations that determine each high–low. It also needs a consistent definition of effective increments, Brownian normalization constants matched to that definition, and quarticity terms matched to the same intervals. Merely summing squared five-minute ranges and dividing by $4\log2$ misses the paper’s principal finite-grid correction.

Useful numerical checks include the $m=1$ identity with RV, convergence of simulated constants toward $\lambda_2=4\log2$ and $\Lambda\approx0.4073$, and unbiasedness under simulated constant-volatility Brownian paths. Simulations should distinguish error from approximating the efficient path, error from estimating moment constants, and the actual finite-sample estimation error. These checks are direct implications of the model, not extra published experiments.

The theoretical gain should be interpreted relative to the available information. With no observation noise and all $mn$ returns usable, ordinary realized variance at the finest grid is a strong benchmark; under the constant-volatility Gaussian model it uses the full likelihood information. The range estimator’s appeal here is recovering intermediate-path information while retaining moderate coarse intervals, not proving universal dominance over that fine-grid benchmark.

Price jumps and microstructure noise are expressly left to further work. A single jump can determine an interval’s range; additive noise can create an extreme that is unrelated to efficient variation. Neither is repaired merely by increasing the Monte Carlo accuracy of $\lambda_{2,m}$. The source’s continuous-price assumptions and observed data cleaning must remain visible when the estimator is used in a risk system.

The paper establishes a concrete, implementable improvement over throwing away intrainterval extrema. It also supplies the variance estimator needed to attach uncertainty to measured daily variance. Its empirical evidence is encouraging for one liquid stock at five-minute aggregation, while exact numerical reproduction remains conditional on missing cleaning details, effective-count conventions, and original simulation code.

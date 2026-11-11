# Monitoring Active Portfolios Using Statistical Process Control

Emmanuel Yashchin, Thomas K. Philips, and David M. Stein. In H. Amman and coeditors, *Computational Approaches to Economic Problems*, Kluwer Academic Publishers, 1997, pp. 193–205. Source: [Sharpe_YashchinPhilipsStein_1997.pdf](../../Finance/Sharpe_YashchinPhilipsStein_1997.pdf), 13 pages. This is a standalone research chapter, not a summary of the containing book.

## Why this matters

A manager who performed well for years can deteriorate while still showing an attractive full-history information ratio. A fixed-window performance statistic either retains too much old success or discards useful data arbitrarily. Yashchin, Philips, and Stein propose a sequential monitoring rule that accumulates evidence of deterioration, discounts old favorable evidence through a reset mechanism, and raises an alarm when recent underperformance becomes sufficiently persistent.

The method adapts a one-sided cumulative-sum, or CUSUM, chart to active portfolio returns. Its design parameters have an operational interpretation: the satisfactory and unsatisfactory information ratios, the tolerated average time between false alarms, and the expected delay before detecting an unacceptable manager. The article's examples show that detecting modest changes in skill still takes years of monthly data. Sequential monitoring improves the use of evidence; it does not eliminate the low signal-to-noise ratio of active returns.

There are two models to distinguish. With known volatility and independent normal returns, the CUSUM has a direct likelihood-ratio derivation and a classical optimality basis. With the paper's adaptive volatility estimate, the standardized observations become dependent and the exact simple-model optimality result no longer transfers automatically. Threshold calibration must therefore match the full implemented recursion and its initialization.

## Return definition and the information ratio

Let $M_i$ and $B_i$ be the managed portfolio's and benchmark's simple returns in period $i$, with positive gross return factors. The active log return is

$$
\Delta_i=\log\left(\frac{1+M_i}{1+B_i}\right).
$$

The paper assumes $\Delta_i$ are independent normal variables with common mean $\mu$ and variance $\sigma^2$. Its per-period information ratio is $R=\mu/\sigma$. This uses log relative returns rather than the arithmetic difference $M_i-B_i$; those agree approximately for small returns but are not identical in volatile periods.

Over $N$ independent periods, cumulative active log return is normal with mean $N\mu$ and variance $N\sigma^2$. Therefore

$$
P\left(\prod_{i=1}^N\frac{1+M_i}{1+B_i}>1\right)
=\Phi(\sqrt N\,R).
$$

For monthly data an annualized information ratio is $\sqrt{12}R$ under these assumptions. The illustrative satisfactory monthly level $R_0=0.144$ corresponds to approximately 0.499 annualized. It implies only about an 80.6% chance of cumulative outperformance over three years and 86.8% over five years. A skilled manager can therefore experience an extended period of underperformance even in the idealized stationary model.

The monitoring problem specifies an acceptable boundary $R_0$ and an unacceptable boundary $R_1<R_0$. Values between them form an indifference region. The source's main example uses $R_0=0.144$ and $R_1=0$, equivalent approximately to annualized information ratios 0.5 and zero. These are policy inputs. They do not come from estimating an optimal firing threshold or a manager's economic replacement cost.

The word “net” in the source's simple-return definition should not be taken as a complete fee specification. A real implementation must explicitly identify management and performance fees, transaction costs, financing, taxes if relevant, and whether the benchmark is attainable on the same basis. The chart interprets whatever return series is supplied; it cannot repair inconsistent portfolio and benchmark accounting.

## Volatility adaptation and the standardized score

If volatility were known, one could monitor $X_i=\Delta_i/\sigma$. In practice the authors use a lagged estimate:

$$
X_i=\frac{\Delta_i}{\widehat\sigma_{i-1}}.
$$

The initial values satisfy $\widehat\sigma_0^2=\widehat\sigma_1^2=\sigma_0^2$, and for $i\ge2$ the variance estimate is

$$
\widehat\sigma_i^2
=\gamma\widehat\sigma_{i-1}^2
 +(1-\gamma)\frac{(\Delta_i-\Delta_{i-1})^2}{2}.
$$

The paper recommends values of $\gamma$ roughly between 0.8 and 0.95 and uses 0.9 in its main calibration. The typical memory scale is $1/(1-\gamma)$ observations, around ten months at 0.9; the exponential half-life is $\log(0.5)/\log(0.9)\approx6.58$ months. These are two different summaries of the same decay, not competing definitions of a rolling-window length.

For independent observations with constant mean and variance,

$$
E\left[\frac{(\Delta_i-\Delta_{i-1})^2}{2}\right]=\sigma^2.
$$

Using differences avoids estimating a slowly moving mean and then subtracting it from each observation. However, a one-time mean jump adds half the squared mean difference to the expectation of the squared difference. Serial dependence also matters: under stationarity this expectation is $\sigma^2-\operatorname{Cov}(\Delta_i,\Delta_{i-1})$. Positive first-order autocorrelation makes the difference-based estimate too low for the marginal variance.

The denominator is deliberately lagged. If the current negative return simultaneously raised its own volatility estimate, the adverse observation could partly hide itself through self-normalization. Using $\widehat\sigma_{i-1}$ evaluates the current outcome against previously available risk information. The variance update is then carried forward to the next observation.

This does not make $X_i$ a sample estimate of the manager's mean information ratio in the usual sense. It is one standardized return observation. Even with independent normal raw returns, the sequence of $X_i$ shares a random volatility state and is not independent normal. Moreover, $E[X_i]$ need not equal $R$ exactly, since the reciprocal estimated volatility is nonlinear. These distinctions matter in interpreting both plotted slopes and likelihood-based claims.

## Likelihood derivation of the CUSUM

First consider the idealized fixed-scale model $X_i\sim N(R,1)$. The log likelihood ratio favoring an unsatisfactory mean $R_1$ over a satisfactory mean $R_0$ is

$$
\ell_i=\log\frac{f_{R_1}(X_i)}{f_{R_0}(X_i)}
=(R_0-R_1)\left(\frac{R_0+R_1}{2}-X_i\right).
$$

A negative standardized return supplies positive evidence for deterioration. For a possible change after observation $j$, the accumulated log likelihood ratio is $\sum_{i=j+1}^n\ell_i$. Taking the maximum over possible change points, and including zero as the option of no accumulated evidence, leads to the recursive one-sided chart

$$
T_i=\max(0,T_{i-1}+\ell_i),\qquad T_0=0.
$$

Divide the statistic and threshold by $R_0-R_1>0$. The equivalent recursion used in the paper is

$$
P_i=\max(0,P_{i-1}-X_i+k),\qquad
k=\frac{R_0+R_1}{2},\qquad P_0=0.
$$

An alarm occurs at the first time $\tau=\inf\{i:P_i>h\}$. For the illustrative design, $k=0.072$. The strict threshold inequality should be specified even though equality has probability zero under a continuous return model; discretized or rounded operational data can create equality events.

The reset at zero explains why old good performance does not protect a manager forever. Favorable observations reduce the accumulated evidence until it vanishes. Subsequently, a run of adverse returns starts a fresh evidence accumulation. The statistic is not a rolling-window average with a fixed lookback, nor a cumulative loss measured in dollars.

A simple deterministic score example clarifies the mechanics. With $k=0.072$, $P_0=0$, and standardized observations $0.4,-0.5,-0.2,0.8,-0.4$, the successive $P_i$ values are $0,0.572,0.844,0.116,0.588$. The large favorable fourth observation reduces but does not quite erase the earlier evidence. Different observations could return the statistic to zero. This example illustrates only the recursion; it does not calibrate the probability of an alarm.

For known pre-change and post-change distributions and independent observations, the classical CUSUM has an optimal detection-delay interpretation at a given false-alarm run-length constraint. The source draws on that literature. The adaptive-scale version is motivated by it but introduces additional state and dependence. It should not be described as inheriting the exact optimality theorem without another proof.

## Average run length and the paper's calibration

An average run length is $E_R[\tau]$, the mean number of observations until the first alarm under a specified fixed information ratio and initialization. The in-control value, at $R_0$, measures the false-alarm waiting time. The out-of-control value, at $R_1$, measures the first-alarm delay when poor performance is present from the beginning of the run.

An ARL is not a fixed-horizon false-positive probability. An in-control ARL of 84 months does not mean an alarm occurs exactly once every seven years, nor that the chance of an alarm in the first year is $12/84$. The complete first-passage distribution and reset policy matter. It also does not by itself characterize worst-case delay after an unknown future change, because the chart's state when the change occurs affects detection.

For $\gamma=0.9$, $k=0.072$, and the satisfactory/unsatisfactory levels above, the paper reports:

| Threshold $h$ | ARL at $R_0=0.144$, months | ARL at $R_1=0$, months |
|---:|---:|---:|
| 6.81 | 84 | 41 |
| 6.29 | 72 | 37 |
| 5.72 | 60 | 32 |
| 5.08 | 48 | 27 |
| 4.33 | 36 | 22 |
| 3.41 | 24 | 16 |

At $h=6.81$, a manager with approximately −0.5 annualized information ratio is reported to trigger an alarm after about 25 months. This is the economic tradeoff: reducing false alarms from acceptable managers delays intervention against mediocre ones, while severely negative performance is detected faster.

A sentence in the source's calibration discussion reverses the comparison between the positive-information-ratio manager and the zero-information-ratio manager. The table has the correct economically expected ordering: the zero-information-ratio manager alarms in roughly half the time of the satisfactory manager, not the reverse. The note follows the table and the recursion.

## Independent numerical check and the replication gap

A separate simulation for this note implements the stated lagged-score recursion with 100,000 independent paths per mean, normal raw returns of unit standard deviation, $\sigma_0=1$, $\gamma=0.9$, $P_0=0$, no burn-in, $k=0.072$, and $h=6.81$. The random seed is 20261010. Variance is left at its initial value for the first observation; from observation two onward it is updated after calculating the current score and chart statistic.

| True monthly $R$ | Simulated mean time, months | Monte Carlo standard error, months | Median time, months | Probability of alarm by month 12 |
|---:|---:|---:|---:|---:|
| 0.144 | 87.758 | 0.240 | 65 | 3.371% |
| 0 | 42.504 | 0.101 | 33 | 8.628% |
| −0.144 | 25.760 | 0.052 | 21 | 18.350% |

Every simulated path reached the threshold before the 20,000-observation safety limit; no censored runs enter these means. These results reproduce the qualitative ordering and approximate scale, but they do **not** exactly reproduce the paper's 84, 41, and 25 months. The differences exceed Monte Carlo sampling error. The source does not provide code or enough detail on the numerical calibration's initialization and possible burn-in to resolve the discrepancy. It would be inappropriate to attribute it confidently to one cause or claim that the original table has been replicated.

This distinction is operationally significant. A production threshold should be calibrated using the same update order, initial variance, head start, reset policy, and return model that will be deployed. Reusing a printed threshold while changing those conventions gives a different false-alarm process even when the visible CUSUM equation is identical.

The simulation's small first-year alarm probability for the satisfactory manager also illustrates why reciprocal ARL is not a fixed-horizon probability. The process begins at zero, some distance from the threshold. Its first-passage distribution is strongly shaped by that initialization.

## Scale invariance, initialization, and state

Normalize raw returns by the true volatility: $Z_i=\Delta_i/\sigma$. Define $v_i=\widehat\sigma_i^2/\sigma^2$. Then the recursion becomes

$$
v_i=\gamma v_{i-1}+(1-\gamma)\frac{(Z_i-Z_{i-1})^2}{2},
\qquad X_i=\frac{Z_i}{\sqrt{v_{i-1}}}.
$$

Under the model, $Z_i\sim N(R,1)$. The initial normalized variance is

$$
v_0=v_1=\left(\frac{\sigma_0}{\sigma}\right)^2.
$$

This reveals the exact invariance condition: the chart's law depends on $R$, the initial volatility ratio, $\gamma$, $k$, $h$, and the chart head start. It is independent of the absolute volatility scale only when initialization is scaled consistently. The paper's normalized initialization notation can obscure the distinction between $\sigma_0^2$ in original units and $(\sigma_0/\sigma)^2$ in normalized units.

If the agreed initial risk estimate is too low, early adverse returns produce larger standardized scores; if it is too high, initial alarms can be delayed. This may be a deliberate policy feature when the manager has exceeded an agreed risk budget, but it changes the statistical calibration. It is not a free gain in detection speed with unchanged false-alarm properties.

The source also discusses a head start such as $P_0=h/2$, which makes the monitor more responsive to initially poor performance. A head start changes both the in-control and out-of-control first-passage distributions. It must be included in calibration rather than added after selecting a threshold from a zero-start table.

With a fixed known scale, $P_i$ is a one-dimensional Markov recursion. With adaptive scale, its future also depends on the current variance estimate and the previous raw return needed by the difference update. The augmented state $(P_i,\widehat\sigma_i^2,\Delta_i)$ is the relevant Markov state under independent raw returns. A one-dimensional integral-equation calculation that ignores those state variables is not automatically valid for the adaptive procedure.

## Empirical illustrations and their evidential limits

The authors discuss more than fifty funds observed over periods of roughly two to eight years as practical support for using the model. The article does not disclose a return panel or formal diagnostics sufficient to reproduce an independence and normality assessment. Those assumptions should therefore be treated as modeling choices, not established universal properties of active returns.

Two anonymized manager examples illustrate the monitor. An emerging-markets equity manager over 1988–1992 retains satisfactory relative performance while tracking error falls substantially, approximately halving. A fixed-income manager measured against the Lehman aggregate bond benchmark over 1985–1992 performs well early and poorly later. The cumulative full-history presentation can remain favorable even after the underlying performance has deteriorated; the CUSUM identifies the more recent adverse evidence.

The figures plot standardized cumulative performance and corresponding CUSUM behavior. Their geometry must be interpreted carefully: some visual presentations show adverse evidence downward, effectively plotting the negative of the nonnegative $P_i$ statistic. That sign convention does not change the alarm rule. Slopes in a cumulative standardized-return chart are also only approximate information-ratio diagnostics when volatility is estimated adaptively.

The source does not provide manager identities, complete monthly returns, precise original data adjustments, or enough numerical coordinates to reproduce the empirical charts exactly. The examples demonstrate use of the procedure rather than establish an out-of-sample manager-selection benefit. They do not compare realized replacement decisions, turnover costs, or the performance of managers selected by competing rules.

## A reproducible monitoring specification

A complete specification should first freeze the economic observation: portfolio and benchmark identifiers, return type, frequency, fee basis, currency, valuation policy, and treatment of missing periods. The model then requires $R_0$, $R_1$, the smoothing parameter, initial volatility, initial chart value, threshold, and an update-order convention. Keeping an audit trail of the raw return, lagged volatility, score, updated variance, and chart statistic allows every alarm to be reconstructed.

The minimal update order is: receive both returns; compute the active log return; divide by the previously available volatility estimate; update the CUSUM and test the threshold; update the variance using the current and preceding active return; store the current active return for the next iteration. The first observation needs its special initialization rule. Missing returns should not silently be replaced by zeros because that changes both the score and the variance dynamics.

After an alarm, the source advocates investigation rather than mechanical termination. The committee should distinguish a real deterioration in the manager's process from benchmark mismatch, a change in mandate, stale prices, a risk-estimation error, or an exceptional but plausible drawdown. Any reset, replacement of the benchmark, or re-estimation after that review should be recorded. Otherwise repeated informal restarts can make the published false-alarm characteristics meaningless.

Several extensions need new calibration. Monitoring many managers simultaneously increases the chance of at least one alert. Serially correlated or heavy-tailed returns change run lengths. Time-varying true volatility can interact with estimator lag. A changing target information ratio makes the fixed-boundary likelihood interpretation approximate. None of these issues is resolved by merely changing $h$ according to the original normal-iid table.

The economic value of a faster alarm also depends on the quality and cost of the available replacement manager. The paper does not optimize the tradeoff between firing a skilled manager too soon, retaining a weak manager too long, and paying transition costs. Its contribution is a disciplined evidence accumulation device that can enter that decision, with explicit statistical design parameters.

## Source and verification record

All thirteen source pages, including conclusions and references, were read. PDF pages 3–6 and 8–11 were visually checked for the return and variance definitions, likelihood derivation, normalization, calibration table, and empirical charts. The likelihood ratio, normalized initialization, and difference-based variance expectation were derived independently. The companion Monte Carlo is a documented numerical check with disclosed assumptions; its difference from the original table remains unresolved. No claim is made to reconstruct the anonymized manager return series.

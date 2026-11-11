# Spurious Regressions in Econometrics

C. W. J. Granger and P. Newbold (1974), *Journal of Econometrics* 2, 111–120. [Source PDF](../../Finance/SpuriousRegression_GrangerNewbold_1974.pdf). All ten PDF pages, including the references, were read; equations and Tables 1–2 were checked visually.

## Why this matters

Two unrelated but persistent series can produce a large regression coefficient, a high coefficient of determination, and an apparently overwhelming conventional significance test. The economic independence of the series does not protect the analyst: the test’s reference distribution assumes a residual process that the proposed null cannot have. Granger and Newbold demonstrate this with independent random walks and integrated moving-average series. With 50 observations, their nominal 5% regression test rejects the true no-relationship null in 76% of one-regressor random-walk simulations and 96% with five regressors.

For investment research, the immediate application is to regressions involving prices, cumulative wealth, slow-moving valuation quantities, or macroeconomic levels. A strong fit among these variables is not sufficient evidence of a forecasting signal. The paper’s contribution is a compact diagnostic argument and an unusually transparent simulation demonstration, rather than a general distribution theory or an estimator that cures all persistence problems. It also explains why adding regressors can make the illusion more convincing.

The numerical rejection rates are particular Monte Carlo outcomes, not universal correction factors. The paper does not say that every levels relationship is economically meaningless. It says that the usual regression inference is unreliable when the actual residual dynamics are inconsistent with its assumptions, and that the time-series specification must be examined before the coefficient is interpreted.

## Statistical setup and the incompatible null

Write the fitted levels regression as

$$
Y=X\beta+\varepsilon,
$$

where $Y$ is $T\times1$, $X$ is $T\times K$, its first column is a constant, and $K-1=m$ stochastic regressors are included. The textbook specification assumes regressors independent of the disturbance vector, $E[\varepsilon]=0$, and

$$
E[\varepsilon\varepsilon']=\sigma^2 I_T.
$$

With Gaussian disturbances, the conventional joint test of

$$
H_0:\beta_1=\cdots=\beta_m=0
$$

uses

$$
F=\frac{T-K}{K-1}\frac{R^2}{1-R^2}
\sim F_{K-1,T-K}.
$$

Here $R^2$ is the unadjusted coefficient of determination. The adjusted quantity used in Table 2 is

$$
\bar R^2=1-(1-R^2)\frac{T-1}{T-K}.
$$

It must not be substituted into the displayed $F$ formula without the appropriate conversion.

The key incompatibility appears under the no-relationship null. If no nonconstant regressor helps explain $Y_t$, the residual is $Y_t-\beta_0$. Its time-series dependence is therefore the dependence of $Y_t$ itself. If $Y_t$ is persistent or integrated, this error is not white noise. The classical $F$ reference distribution is consequently unavailable, even when the regressors are statistically independent of the dependent series.

There is no logical contradiction in a persistent dependent series having a well-specified regression with white-noise disturbances when meaningful explanatory variables are included. The conflict is between the joint claims that all those explanatory coefficients vanish and that the remaining error is white noise. This distinction is useful: a rejection of the textbook null may be exposing its error specification rather than a genuine relationship between the variables.

The usual consequences of autocorrelated regression disturbances are inefficient coefficient estimates, suboptimal forecasts, and invalid conventional coefficient tests. This paper concentrates on the last consequence. It does not establish that the OLS coefficient is biased in every model with serial correlation; that would require assumptions about the regressors and disturbance process beyond serial correlation alone.

## Persistence and the series models

Let $B$ be the lag operator and $\Delta=1-B$. The authors represent a stationary series $W_t$ through an ARMA model,

$$
\phi(B)W_t=\theta(B)a_t,
$$

where $a_t$ is white noise and the lag polynomials satisfy the stationarity and representation conditions. An integrated series is written

$$
\phi(B)\Delta^d X_t=\theta(B)a_t.
$$

Their practical starting point is that many economic levels are very smooth: either $d=1$ is appropriate or a stationary autoregressive root lies close to one. Two basic examples are the random walk,

$$
\Delta X_t=a_t,
$$

and an integrated moving-average process,

$$
\Delta X_t=a_t-\theta a_{t-1}.
$$

These are stochastic persistence models, not merely deterministic trends removed by an intercept or a linear time trend. A no-change forecast may work reasonably well because the series is persistent; that forecasting performance does not supply the missing justification for conventional levels-regression inference.

The paper gives a stationary analogue. Suppose independent series satisfy

$$
Y_t=\phi Y_{t-1}+a_t,
\qquad X_t=\phi^*X_{t-1}+u_t,
$$

with independent white-noise innovations. In a one-regressor regression with an intercept, $R^2$ is the squared sample correlation. The cited approximation is

$$
\operatorname{Var}(R)\approx\frac1T\frac{1+\phi\phi^*}{1-\phi\phi^*}.
$$

The paper prints this as an equality, but its large-sample/approximation status matters near the boundary: it cannot be a globally exact finite-sample variance because the right-hand side can exceed one while $R\in[-1,1]$. At $T=20$ and $\phi=\phi^*=0.9$, it gives $0.4763$, explaining the source’s rounded $E[R^2]\simeq0.47$. Persistence makes chance sample correlations much more dispersed than the familiar independent-observation calculation suggests.

The source further uses the bounded support of correlation to argue that a variance above $1/3$ is incompatible with a symmetric density that has a single mode at zero. Substituting the approximation gives

$$
\phi\phi^*>\frac{T-3}{T+3}.
$$

For equal positive autoregressive coefficients and $T=20$, the threshold is approximately $0.8597$, reported as 0.86. This is an illustrative approximation, not a formal finite-sample modality theorem for the estimated correlation near a unit root. Its relevance is that correlations near zero cease to dominate the sampling distribution even though population cross-series dependence is absent.

## Experiment 1: an absolute t statistic with the wrong scale

The first experiment regresses one independent random walk on another, includes an intercept, uses a series length of 50, and repeats the exercise 100 times. The reported statistic is

$$
S=\frac{|\hat\beta_1|}{\widehat{\operatorname{se}}(\hat\beta_1)}.
$$

The denominator is the conventional OLS standard error. It is precisely the use of this denominator under the wrong residual specification that is under investigation.

| Interval for $S$ | Count | Interval for $S$ | Count |
|---|---:|---|---:|
| 0–1 | 13 | 8–9 | 3 |
| 1–2 | 10 | 9–10 | 3 |
| 2–3 | 11 | 10–11 | 1 |
| 3–4 | 13 | 11–12 | 5 |
| 4–5 | 18 | 12–13 | 0 |
| 5–6 | 8 | 13–14 | 1 |
| 6–7 | 8 | 14–15 | 0 |
| 7–8 | 5 | 15–16 | 1 |

The bins sum to 100. Seventy-seven observations are in bins starting at 2, but the exact rejection count at the finite-sample two-sided 5% $t$ critical value cannot be recovered from those bins. The source reasonably describes the false rejection frequency as approximately three quarters.

The observed mean absolute statistic is 4.5. If the signed statistic were standard normal, its mean absolute value would be $\sqrt{2/\pi}\simeq0.798$. Dividing 4.5 by approximately 0.8 suggests a scale discrepancy of 5.6; squaring gives approximately 31.4 as a variance multiplier. The paper consequently suggests a critical magnitude near $2\times5.6=11.2$ in this example.

That last step is a heuristic, not a demonstrated 5% critical value. Matching one absolute moment does not establish that the entire nonstandard statistic distribution is a scaled normal distribution. The histogram alone cannot justify exact 5% size at 11.2; indeed, its coarse upper bins already show substantial mass around that level. An implementation should reproduce the empirical null distribution or use a justified time-series method, rather than adopt 11.2 as a universal persistence-adjusted threshold.

For context the paper cites a different autoregressive calculation with both persistence coefficients equal to 0.8 and $T=50$, producing a conventional coefficient-variance inflation factor of 5.8. This is a variance factor, whereas 5.6 in the random-walk discussion is a standard-deviation factor. Confusing them would understate the comparison by an order of magnitude. The stationary approximation is explicitly said to break down as both roots approach unity.

## Experiment 2: adding unrelated regressors

The second experiment uses $m=1,\ldots,5$ independent explanatory series and four types of regressions: random-walk levels, their changes, integrated moving-average levels, and their changes. Its construction is unusually reproducible. Starting at 100, generate mutually independent standard normal white noises and set

$$
Y_0=100,\qquad Y_t=Y_{t-1}+a_t,
\qquad Y_t'=Y_t+k b_t,
$$

$$
X_{j,0}=100,\qquad X_{j,t}=X_{j,t-1}+a_{j,t},
\qquad X_{j,t}'=X_{j,t}+k b_{j,t}.
$$

All innovations, dates, and series are independent. $k=0$ gives random walks; $k=1$ gives the sum of a random walk and independent white noise. The source calls the latter ARIMA$(0,1,1)$ because its first difference has an MA(1) covariance structure. This does not mean the source sets a scalar MA coefficient equal to one.

For example, directly from this construction,

$$
\Delta Y_t'=a_t+b_t-b_{t-1},
\quad \operatorname{Var}(\Delta Y_t')=3,
\quad \operatorname{Cov}(\Delta Y_t',\Delta Y_{t-1}')=-1.
$$

Thus its first autocorrelation is $-1/3$. An equivalent invertible scalar MA representation with the source’s minus-sign convention has $\theta=(3-\sqrt5)/2\simeq0.3820$ and innovation variance $(3+\sqrt5)/2\simeq2.6180$. This equivalence is derived here to clarify the simulation; the original independent-noise construction is sufficient for replication.

Each configuration has 100 replications and nominal series length 50. The joint significance test uses the unadjusted $R^2$ and a nominal 5% level. Table 2 reports the following outcomes; rejection rates and last-column frequencies are percentages, while $d$ and $\bar R^2$ are dimensionless.

| Series and transformation | $m$ | Reject $H_0$ | Mean $d$ | Mean $\bar R^2$ | Frequency $\bar R^2>0.7$ |
|---|---:|---:|---:|---:|---:|
| Random walk, levels | 1 | 76 | 0.32 | 0.26 | 5 |
| Random walk, levels | 2 | 78 | 0.46 | 0.34 | 8 |
| Random walk, levels | 3 | 93 | 0.55 | 0.46 | 25 |
| Random walk, levels | 4 | 95 | 0.74 | 0.55 | 34 |
| Random walk, levels | 5 | 96 | 0.88 | 0.59 | 37 |
| Random walk, changes | 1 | 8 | 2.00 | 0.004 | 0 |
| Random walk, changes | 2 | 4 | 1.99 | 0.001 | 0 |
| Random walk, changes | 3 | 2 | 1.91 | −0.007 | 0 |
| Random walk, changes | 4 | 10 | 2.01 | 0.006 | 0 |
| Random walk, changes | 5 | 6 | 1.99 | 0.012 | 0 |
| ARIMA$(0,1,1)$, levels | 1 | 64 | 0.73 | 0.20 | 3 |
| ARIMA$(0,1,1)$, levels | 2 | 81 | 0.96 | 0.30 | 7 |
| ARIMA$(0,1,1)$, levels | 3 | 82 | 1.09 | 0.37 | 11 |
| ARIMA$(0,1,1)$, levels | 4 | 90 | 1.14 | 0.44 | 9 |
| ARIMA$(0,1,1)$, levels | 5 | 90 | 1.26 | 0.45 | 19 |
| ARIMA$(0,1,1)$, changes | 1 | 8 | 2.58 | 0.003 | 0 |
| ARIMA$(0,1,1)$, changes | 2 | 12 | 2.57 | 0.010 | 0 |
| ARIMA$(0,1,1)$, changes | 3 | 7 | 2.53 | 0.005 | 0 |
| ARIMA$(0,1,1)$, changes | 4 | 9 | 2.53 | 0.025 | 0 |
| ARIMA$(0,1,1)$, changes | 5 | 13 | 2.54 | 0.027 | 0 |

The visually checked final heading is $\bar R^2>0.7$, not 0.1 as an imperfect text extraction can suggest. Table 1 and the $m=1$ row of Table 2 are separately reported experiments, so their approximately three-quarter rejection rates need not have identical counts.

Increasing the number of irrelevant regressors raises the mean adjusted fit in levels despite the usual degrees-of-freedom adjustment. It also raises average Durbin–Watson, so an improvement in that diagnostic alone does not establish a valid model. The random-walk differences are independent white noises, and their rejection percentages fluctuate around the nominal rate. The moving-average differences retain serial dependence; their five rejection percentages average 9.8%, nearly twice the nominal 5%.

With only 100 replications, a rejection proportion near 5% has Monte Carlo standard error about $\sqrt{0.05(0.95)/100}=2.18$ percentage points. The individual small deviations should therefore not be overinterpreted. The enormous levels-regression size distortions are far beyond this sampling uncertainty.

## A replication procedure and its limits

For each $k$ and $m$, generate the independent innovations, construct the level paths, and fit an intercept plus all $m$ regressors. Compute residuals $e_t$, the ordinary $R^2$, its adjusted version, and

$$
d=\frac{\sum_{t=2}^{T}(e_t-e_{t-1})^2}{\sum_{t=1}^{T}e_t^2}.
$$

Evaluate the joint $F$ statistic against the 95th percentile of $F_{m,T-m-1}$. Repeat on first differences, then accumulate rejection percentages, means of $d$ and $\bar R^2$, and the percentage of adjusted fits exceeding 0.7. To reproduce the first experiment, also store the absolute conventional slope $t$ statistic and its histogram.

The paper supplies the generating distributions, the starting level, the series lengths, the regressor counts, the replication count, and the summary statistics. It does not provide random seeds, realized draws, software, or a completely explicit endpoint convention for whether a nominal length of 50 refers to retained levels or retained differences. A modern reproduction must state that convention and use the resulting actual sample size in the degrees of freedom. Exact table matching is not possible from the source alone. Nor are these simulated units a return frequency: there is no daily-to-annual conversion in the experiments.

An implementation should retain separate innovations for every series. Sharing random shocks would introduce the very relationship that this experiment excludes. It should also include the intercept, avoid treating the common starting value of 100 as an explanatory signal, and keep the empirical rejection frequency separate from the nominal test level. Those choices are material to interpreting the exercise, not merely coding details.

## Remedies, qualifications, and the economic interpretation

The authors discuss adding a lagged dependent variable, taking first differences, and imposing an AR(1) residual model. Each can alleviate the problem, but none is asserted to be universally sufficient. Their own moving-average experiment demonstrates why differencing can leave conventional tests incorrectly sized. Conversely, differencing changes the object being studied; a relation in changes need not answer the same economic question as a long-run relation in levels.

They outline a possible approach based on first fitting each series from its own history and then investigating relationships among the remaining innovations. The economic intuition is incremental information: another variable is useful for forecasting only to the extent that it explains what the target’s own past has not already explained. The paper describes this proposal as preliminary. It does not provide a full prewhitening algorithm, a general multivariate inference theory, or finite-sample critical values for such a procedure.

The recommendation to inspect both levels and changes is illustrated by a cited UK consumption regression using autonomous expenditure and mid-year money stock over 1947–1962. The levels regression has adjusted $R^2=0.99$ and $d=0.59$; the changes regression has adjusted $R^2=-0.03$ and $d=2.21$. These are quoted historical results, not an empirical dataset reconstructed in this paper. They illustrate sensitivity to specification rather than prove that either regression identifies a structural causal mechanism.

Finally, economic theory may help choose variables but usually does not fully specify sampling lags, measurement error, or residual dynamics. A theoretically appealing list of regressors therefore cannot validate an inappropriate standard error. The source’s strong language about autocorrelated residuals should be understood as criticism of a specification claiming white-noise disturbances. Serial correlation does not by itself prove that the estimated economic relationship is absent, and white residuals are not sufficient evidence of structural identification. The implementable lesson is to align the null, the dynamics, and the test distribution before treating a high fit as investment evidence.

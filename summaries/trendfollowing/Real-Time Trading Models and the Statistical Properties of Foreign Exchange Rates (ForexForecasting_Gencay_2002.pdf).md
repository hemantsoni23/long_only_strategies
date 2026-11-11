# Real-Time Trading Models and the Statistical Properties of Foreign Exchange Rates

**Ramazan Gençay, Giuseppe Ballocchi, Michel Dacorogna, Richard Olsen, and Olivier Pictet. International Economic Review 43(2), May 2002, 463–491.**

**Source:** [ForexForecasting_Gencay_2002.pdf](../../Finance/ForexForecasting_Gencay_2002.pdf), thirty PDF pages including the JSTOR cover. The entire article, all nine tables, four kernel figures, and references were inspected. Printed journal pages are used below. The paper describes a commercial system but does not disclose all calibrated thresholds, execution rules, or software required to reproduce its exact trades.

## Why this matters

A price model can fit five-minute volatility reasonably well while generating completely unrealistic outcomes for a strategy that holds positions for days. This paper uses a fixed trading strategy as a diagnostic of the full temporal structure of exchange rates. The same trading system is run on historical quotes and simulated paths; differences in returns, drawdowns, and trading frequency reveal features of the data that conventional one-frequency fit measures miss.

There are two distinct contributions. First, the authors report seven years of performance for a real-time currency system whose parameters were not reoptimized over the evaluation period. Second, they use its performance distribution to test a random walk, GARCH, AR–GARCH, and a multihorizon HARCH process. Their proposed explanation for rejection is that the fitted models fail to reproduce the medium-horizon conditional mean structure used by the strategy, even when they capture some high-frequency dependence and volatility persistence.

This is a useful research design, but rejection of a collection of null models is not a universal proof of market inefficiency or future profitability. The findings are conditional on the trading implementation, the price-data treatment, and the simulated models. Several printed equations and diagnostics are incomplete or inconsistent, so a transparent reconstruction must separate the disclosed architecture from the unavailable commercial implementation.

## Data and evaluation chronology

The evaluation period is **January 1, 1990–December 31, 1996**, for USD–DEM, USD–CHF, USD–FRF, and DEM–JPY. The original live system processes tick-by-tick market-maker bid and ask quotes. To make 1,000 replications per process feasible, the paper evaluates five-minute data and simulations in a deseasonalized business-time clock. It reports **671,040 observations per currency**. A simulated year corresponding to 1989 is used to initialize return history and trading indicators before the scored period.

The authors state that the model was not reoptimized during 1989–1996. Thus the 1989 initialization year and the seven scored years have different roles. A fixed strategy reduces one form of in-period parameter search, but the paper does not provide the original optimization sample, all prior model-development decisions, or a complete audit of strategy selection. The volatility models used as simulation nulls are estimated on the historical evaluation data; they are fitted specification-test benchmarks, not necessarily ex ante forecasting competitors.

At quote time $t_j$, define log midpoint and log spread by

$$
x_j=\frac{\log P^{ask}_j+\log P^{bid}_j}{2},\qquad
s_j=\log P^{ask}_j-\log P^{bid}_j,
\qquad r_j=x_j-x_{j-1}.
$$

The midpoint is the logarithm of the geometric mean of bid and ask, rather than the log of their arithmetic midpoint. At ordinary FX spreads the difference is small, but the stated convention should be retained.

The time transformation, denoted $\theta$, follows the authors' earlier geographical seasonality model. Activity in East Asia, Europe, and North America determines the business-time clock from intraday/weekly volatility patterns. Recorded observation times and data gaps are preserved when generating synthetic bid/ask paths; only prices are replaced. The exact clock parameters, holiday calibration, quote filtering, and selected-tick algorithm are referred to other work or unavailable code.

The conclusion's description of hundreds of thousands of “independently sampled” observations should not be interpreted as statistical independence. The paper's premise is precisely that returns, volatility, trading signals, and overlapping performance intervals have dependence. Tick or five-minute sample size is not the number of independent medium-horizon trading opportunities.

## Robust moving averages and the signal

For elapsed lag $u\ge0$, the exponential kernel is

$$
w_{EMA}(u;\tau)=\frac1\tau e^{-u/\tau}.
$$

Repeated convolution produces an iterated EMA kernel,

$$
w_j(u;\tau)=\frac{e^{-u/\tau}}{\tau(j-1)!}
\left(\frac u\tau\right)^{j-1}.
$$

It integrates to one and has mean lag $j\tau$. The source's Figures 1–2 show how iteration moves weight away from the newest observation. This is a filter of historical log prices, not a distribution assumed for future prices.

The robust moving-average kernel averages $n$ such kernels using a rescaled elementary horizon:

$$
w_{MA}(u;\tau,n)=\frac1n\sum_{j=1}^{n}w_j(u;\tau'),
\qquad\tau'=\frac{2\tau}{n+1},
$$

$$
MA_p^n(\tau,t)=\int_0^\infty w_{MA}(u;\tau,n)p(t-u)\,du.
$$

The average mean lag is $\tau'(n+1)/2=\tau$, explaining why this rescaling keeps the effective range fixed as $n$ changes. The kernel has a relatively flat initial region and an exponentially declining tail. It avoids a simple moving average's abrupt loss of an observation at the window boundary while reducing the immediate emphasis of a single exponential filter.

A difference of two normalized filters has zero integral and acts as a momentum signal. For the reported system the central indicator is

$$
I_p(t)=p_t-MA_p^4(20,t),
$$

with $p_t$ a log price and the stated horizon twenty days. This is the four-component robust average, not simply a fourth power of a moving average. An implementation must specify whether the twenty days are measured in the business-time clock and exactly how the clock maps to market calendars; the paper does not provide the full operational mapping.

The continuous-time integrals can be evaluated numerically or through cascaded EMA states. On irregular observations, the result depends on interpolation and update conventions between quotes. Choosing a standard discrete EMA recursion is a reasonable reconstruction, but it is not proof of numerical identity with the commercial filter. Figures 3–4 provide kernel-shape checks, not a full discrete algorithm.

## Position sizing, thresholds, and state dependence

The allowed gearing is $g_t\in\{-1,-1/2,0,1/2,1\}$. Individual currency strategies are bounded by one unit of exposure. The schematic rule on p. 478 is

$$
g_t=\operatorname{sign}(I_p(t))\,f(|I_p(t)|)\,c_t,
$$

where

$$
f(z)=\begin{cases}
0,&z<a,\\
1/2,&a<z<b,\\
1,&z>b,
\end{cases}
\qquad b=2a,\qquad a<b<d.
$$

The source leaves equality cases unstated. Normally they are probability-zero under a continuous price model, but a deterministic implementation still needs a tie convention.

The contrarian multiplier is $+1$ for signals below the extreme threshold $d$. It becomes $-1$ when the signal exceeds $d$, the previous position is aligned with the trend, and the return associated with the last deal exceeds profit objective $P$. The paper describes this as taking profits from a successful trend position and then trading against an extreme move. It reports roughly two or three contrarian episodes per typical year, with an approximately 75% hit rate, against roughly sixty to seventy total deals. These descriptive counts are not the same as a separately tabulated, uncertainty-adjusted contrarian backtest.

The displayed branch definition does not state what happens when $|I_p|>d$ but the other reversal conditions fail. Nor does it fully define the return state used in that condition for an open versus completed deal. A reconstruction must make those transitions explicit and label them as choices; simply treating the formula as a complete stateless function would be wrong.

Thresholds depend on whether the strategy is already invested. The entry threshold is doubled when the previous gearing is zero, while the base threshold applies when there is an existing position. A second rule raises the threshold to ten times its base level if the absolute move from the last entry price is below $v$, generally less than 0.5%. This creates inertia: small moves do not trigger repeated switching. The paper does not unambiguously specify the precedence of all threshold adjustments or whether $b$ is recalculated from each adjusted $a$.

The usual profit objective is approximately **3%**. A gliding stop then protects accumulated gains; an independent stop-loss parameter $S$ closes an adverse position. The main parameters optimized before evaluation are $\tau,a,d,v$, followed by bounded optimization of $S$ and $P$. Actual currency-specific parameter values, optimization ranges, objective weights, and the complete trailing-stop algorithm are not disclosed. The article refers the optimization procedure to earlier work.

## Execution and trading constraints

The strategy is associated with the Zurich market's opening hours and holidays. The broader software supports several local markets, with typical office hours around 08:00–17:30 local time. Ordinary trades occur during market hours, while stops may execute outside them. Exact Zurich schedules, daylight-saving handling, and holiday lists are not published.

Recommendations are announced **three minutes before execution**, allowing a human dealer to respond. The execution price is based on a median of quotes over the last few minutes rather than a single quote. Bid/ask costs are included. These conventions are integral to the strategy: a simulation using the signal's instantaneous midpoint will not reproduce the stated implementation.

The claim that real-time quote selection eliminates slippage is too strong. It removes hindsight in choosing a quote but does not guarantee executable size, a firm quote, or a fill at that price. The paper itself notes potential stale-quote problems for DEM–JPY. It supplies no order-book model, market-impact function, rejected-fill rule, or capacity test. Its results should therefore be described as the system's recorded/model execution performance under its assumptions, not a guarantee of realizable returns at arbitrary scale.

Synthetic paths use a constant average spread. With log midpoint $x'_j$ and chosen average log spread $\bar s$, an explicit conversion is $P^{bid}_j=\exp(x'_j-\bar s/2)$ and $P^{ask}_j=\exp(x'_j+\bar s/2)$. The paper sometimes calls 0.00025 a spread and elsewhere a half-spread in its USD–DEM cost examples. One must resolve the per-deal convention rather than double or halve costs implicitly.

## Performance measures and units

The single-strategy total return sums deal returns against a fixed initial-capital/credit-limit convention:

$$
R_T=\sum_{j=1}^{n}r_j^{deal}.
$$

It is annualized linearly by elapsed calendar time. This differs from compounding a sequence of reinvested monthly returns, which is used later for the manager-index comparison. Maximum drawdown is the largest peak-to-subsequent-trough decline of this cumulative-return curve. It is not automatically the proportional drawdown of a compounded wealth process.

Risk-sensitive measures include open-position mark-to-market returns. For cumulative marked return $\widetilde R_t$, define $X_{\Delta,t}=\widetilde R_t-\widetilde R_{t-\Delta}$. Under Gaussian increments and CARA utility $u(x)=-e^{-\alpha x}$, the certainty equivalent is

$$
CE_\Delta=E[X_\Delta]-\frac\alpha2\operatorname{Var}(X_\Delta).
$$

The paper annualizes this expression and averages across horizons with weights $w_i$:

$$
X_{eff}=\frac{\sum_iw_i A_{\Delta_i}
\left(\bar X_{\Delta_i}-\frac\alpha2\widehat\sigma_{\Delta_i}^2\right)}
{\sum_iw_i}.
$$

It uses $\alpha=0.1$ when returns are expressed in percentage points, equivalent to 10 for decimal returns. Reported component horizons are **7, 29, 117, and 301 days**. The horizon weights and exact overlapping-observation sampling are not supplied. The annualization footnote is also ambiguous: to annualize an interval mean directly, $A_\Delta$ must be periods per year, whereas its printed ratio of interval counts in a year and in the full sample does not generally do that. Exact reproduction needs the original implementation.

The Gaussian assumption makes the quadratic certainty equivalent exact; with non-Gaussian empirical returns, the mean-minus-variance expression is a chosen score rather than the exact CARA certainty equivalent of the empirical distribution. It remains finite for a straight-line return curve and distinguishes different slopes when a Sharpe ratio with zero denominator would not.

The second score, $R_{eff}$, applies stronger risk aversion to losses: $\alpha_-=0.20$ and $\alpha_+=\alpha_-/4=0.05$ in percentage-point units. The article gives this principle but refers the complete functional construction to related work. A piecewise substitution into the variance formula should not be claimed to reproduce $R_{eff}$ without that derivation. Both scores reward a smoother marked-return path; neither is itself a traded return.

## Historical results

Table 2 reports the following for 1990–1996. Return and effective-return entries are percentages under the paper's conventions; drawdown is in percentage points of its cumulative-return measure.

| Measure | USD–DEM | USD–CHF | USD–FRF | DEM–JPY |
|---|---:|---:|---:|---:|
| Annual return | 9.63 | 3.66 | 8.20 | 6.43 |
| $X_{eff}$ | 3.78 | −1.68 | 4.80 | 3.81 |
| $R_{eff}$ | 4.43 | −4.23 | 4.95 | 3.45 |
| Maximum drawdown | 11.02 | 16.08 | 11.36 | 12.03 |
| Deals per week | 1.68 | 1.29 | 1.05 | 2.14 |

The authors describe these annual returns as unleveraged, net of trading costs, and above the risk-free return. Their exact funding/carry and deal-return bookkeeping are not fully printed. USD–CHF is the clear weak case: positive average return does not compensate for risk under either effective-return measure.

Performance varies with measurement horizon. USD–CHF's $R_{eff}$ is −4.81 at seven days, −8.97 at twenty-nine days, −1.77 at 117 days, and 1.71 at 301 days. USD–DEM's corresponding values are 1.80, 2.16, 5.10, and 6.83. Longer-horizon scores can look better because losses cluster at shorter horizons. The table also gives 2.14 deals per week for DEM–JPY, so prose claims that all systems trade fewer than twice weekly should be read as approximate.

For the Parker Systematic Index comparison, the four monthly strategy returns are equally weighted and multiplied by the **full-sample** ratio of index volatility to strategy-portfolio volatility. This retrospective risk matching is not an ex ante leverage policy. Equal standard deviation also does not make drawdown, skewness, or tail risk identical.

| 1990–1996 portfolio | Cumulative net gain | Annualized compounded return |
|---|---:|---:|
| Parker Systematic Index | 104.49% | 10.76% |
| Risk-matched RTT portfolio, before manager fees | 218.01% | 17.97% |
| After 2% management fee | 168.32% | 15.15% |
| After management and 20% performance fee | 130.24% | 12.65% |

The final annualized difference is **1.89 percentage points**. The cumulative-gain difference is 25.75 percentage points, but final wealth is only about $2.3024/2.0449-1=12.6\%$ larger, not the prose's approximately 25% larger capital. The printed management-fee recursion mixes monthly growth factors and prior capital; the text states monthly deduction of 2% annual management fees and annual 20% fees on net profits, without a fully specified high-water-mark or loss-carryforward convention. These are further barriers to exact fee-adjusted replication.

## Simulated null models

Each simulated path preserves the observation times, initializes from the real initial log price, generates returns, reconstructs quotes, runs the frozen trading system, and measures the same performance statistics. There are **1,000 replications**. A Gaussian innovation generator is the main implementation; the authors say resampling fitted residuals does not change their main findings, but do not show a complete parallel set of results.

The nulls are a Gaussian random walk with fitted drift and variance, GARCH(1,1), AR(4)–GARCH(1,1), and AR(4)–HARCH(9). Four AR lags are retained because adding more did not materially increase likelihood. The source writes the GARCH recursion as

$$
r_t=\gamma_0+\sum_{i=1}^{p}\gamma_i r_{t-i}+\epsilon_t,
\qquad\epsilon_t=\sqrt{h_t}z_t,
\qquad h_t=\alpha_0+\alpha_1h_{t-1}+\beta_1\epsilon_{t-1}^2,
$$

with $p=0$ or 4 and $z_t\sim N(0,1)$. This coefficient labeling places $\alpha_1$ on lagged variance, contrary to a common software convention. The tables have small $\alpha_1$ and large $\beta_1$; code is needed to determine whether the equation or table labels were interchanged. One should not silently infer implementation from customary notation.

The multihorizon recursion is

$$
r_t=\gamma_0+\sum_{i=1}^{4}\gamma_i r_{t-i}+\sigma_t\epsilon_t,
\qquad\sigma_t^2=c_0+\sum_{j=1}^{9}c_jv_{j,t},
$$

$$
v_{j,t}=\mu_jv_{j,t-1}+(1-\mu_j)
\left(\sum_{i=1}^{k_j}r_{t-i}\right)^2,
\qquad
\mu_j=\exp\left[-\frac{2}{k_{j+1}-k_j}\right].
$$

The printed grid is $k_1=1$ and $k_j=4^{j-2}+1$ for $j>1$. The source also describes horizons up to ten days, which is not the literal five-minute duration of the largest printed $k_j$; $\mu_9$ additionally requires the next grid point. Those details and the business-time conversion must be resolved explicitly. Table 8 reports impacts $I_j=k_jc_j$, not raw $c_j$, so dividing each tabulated impact by its horizon is necessary before applying this recursion.

For its USD–DEM HARCH estimates, impacts $I_1$ through $I_9$ are 0.1157, 0.1670, 0.1925, 0.1056, 0.0469, 0.0767, 0.1165, 0.0921, and 0.0421. The intercept is $2.252\times10^{-8}$, with standard error $5.241\times10^{-9}$. AR coefficients are −0.1957, −0.0373, −0.0064, and −0.0087. The GARCH-table intercept scales and some drift parameters are not comparably documented.

The irregular-time rescaling is another reproducibility qualification. The article multiplies an observed return by a positive square-root elapsed-time factor when describing normalization to a common interval, then uses the same direction when mapping simulated returns back. For driftless Brownian increments, normalizing a longer observed interval to a fixed interval requires the inverse square-root factor; mapping a standardized innovation to a longer interval uses the positive factor. A drift term scales linearly in elapsed time. The printed recipe should therefore be checked against original code, not treated as a complete coherent time-change specification.

## Null rejection results and interpretation

The reported p-value is the fraction of simulated statistics greater than the historical statistic. For return-based measures, small values put the historical outcome in the favorable upper tail. For drawdown and deal frequency, values near 100% instead mean almost all simulations have larger values. The tail direction must be considered separately; “100%” is not evidence that the historical drawdown is typical.

Annual-return p-values, in **percent**, are:

| Null model | USD–DEM | USD–CHF | USD–FRF | DEM–JPY |
|---|---:|---:|---:|---:|
| Random walk | 0.3 | 8.9 | 1.2 | 2.1 |
| GARCH(1,1) | 0.4 | 8.4 | 0.9 | 1.2 |
| AR(4)–GARCH(1,1) | 0.1 | 3.7 | 0.3 | 0.5 |

Thus ordinary return alone does not reject the first two nulls for USD–CHF at 5%. The full-period effective-return scores give stronger rejection: for example, random-walk $X_{eff}/R_{eff}$ p-values are 0.7%/0.6% for USD–CHF, and AR–GARCH gives 1.9%/2.3%. There are exceptions at individual horizons: the twenty-nine-day USD–CHF $R_{eff}$ p-value under AR–GARCH is **9.7%**. A statement that every score at every horizon rejects is incorrect.

With 1,000 replications, tabulated 0.0% means zero observed exceedances at that resolution, not an exactly zero population probability. Parameter-estimation uncertainty, multiplicity across currencies and scores, and model-selection uncertainty are not fully propagated. A p-value from an assumed price process is not the probability that future strategy returns will be favorable.

Random-walk mean simulated drawdowns are 53.79, 63.68, 47.68, and 53.49 percentage points, much larger than historical values. Mean simulated deal rates are 2.46, 1.98, 1.65, and 3.08 per week. GARCH produces similarly large drawdowns, 53.33, 60.58, 46.00, and 48.77, and deal rates 2.39, 1.87, 1.59, and 2.66. The nulls generate excessive switching and cost drag relative to the historical strategy path.

The USD–DEM random-walk example has 2.46 weekly deals, about 127.92 annually. Multiplying by the paper's per-deal cost 0.00025 gives approximately 3.20% annual costs, close to its simulated mean return of −3.44%. This is a useful accounting check. It does not validate every spread convention or the entire price model.

The HARCH presentation is internally mismatched: Table 8 is labeled USD–DEM, while Table 9 and its historical values are DEM–JPY. Table 9 reports annual-return, $X_{eff}$, and $R_{eff}$ p-values of 0.2%, 0.2%, and 0.1%, with drawdown 100% and deal frequency 88%. The latter is not an extreme 5% tail observation. The prose refers to USD–DEM and says other currencies are omitted. Do not connect the Table 8 parameter vector to Table 9 performance as a verified same-currency experiment.

Finally, the printed residual diagnostics contradict claims that serial correlation is absent. Table 4's $Q(12)$ values range from 3,089 to 4,810, Table 5's from 374 to 623, and Table 8's is 726; the stated 5% critical value is 21.03. These are strongly significant if the table labels and values are literal. Residual excess kurtosis is also large. The fitted nulls' inadequacy is therefore visible before applying the trading-system test, weakening any claim that rejection uniquely isolates missing medium-horizon mean predictability.

## What can be reimplemented

The filter family, restricted gearing architecture, state-dependent threshold logic, multihorizon scoring idea, and simulation-comparison design are disclosed well enough to build a transparent research reconstruction. The exact historical strategy is not reproducible from the PDF alone because calibrated thresholds, complete position-state transitions, execution/stop details, time-clock parameters, effective-return weights, and some statistical-model conventions are absent or contradictory.

A sound reconstruction should first validate filters and quote accounting, then freeze a fully specified strategy before scoring historical and simulated paths. Preserve the one-year initialization, calendar constraints, bid/ask construction, and common performance definitions. Report both gains and the frequency of trades, because an apparently successful price model may generate implausible strategy turnover. Treat additional sensitivity tests, alternative nulls, and modern execution assumptions as extensions rather than original findings.

The durable contribution is to assess financial time-series models through economically meaningful path functionals at the horizons where decisions occur. The paper's historical performance and null rejections support that approach. They do not identify a unique true price process, establish an executable modern alpha, or remove the need to test the undisclosed parts of the trading implementation.

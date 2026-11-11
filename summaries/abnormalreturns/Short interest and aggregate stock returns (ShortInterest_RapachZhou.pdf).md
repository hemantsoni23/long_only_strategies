# Short interest and aggregate stock returns

**David E. Rapach, Matthew C. Ringgenberg, and Guofu Zhou (2016).** *Journal of Financial Economics* 121, 46–65. DOI: 10.1016/j.jfineco.2016.03.004. Source: [library PDF](../../Finance/ShortInterest_RapachZhou.pdf), 20 pages, read in full. References below use printed journal pages and table numbers. The [separate robustness appendix](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2675298) is identified by the authors but could not be retrieved in this run; statements about its results below are limited to what the main paper reports. The author's [data page](https://sites.google.com/site/ringgenberghomepage/data) provides replication-data/code links and a later index update; this note describes the original 1973–2014 study, not an updated backtest.

## Why this matters and what is new

The paper constructs a market-level information signal from positions taken by short sellers. The innovation is to aggregate firm-level short interest, remove the large secular rise in the propensity and ability to short, and ask whether the remaining variation forecasts the equity premium. A negative stock-level relation between short interest and subsequent returns does not automatically imply a market-timing signal: cross-sectional designs usually remove common market movements. This study explicitly targets those common movements.

Its short interest index, or SII, forecasts lower aggregate returns when detrended short interest is high. It outperforms fourteen familiar macro-financial predictors in the reported sample, survives recursively estimated out-of-sample forecasts, and produces economically material certainty-equivalent gains in a constrained stock-versus-bills allocation. A return decomposition then attributes most of the predictive slope to cash-flow news relative to a specified market information set.

The result matters for two separate research programs. For forecasting, it supplies an implementable transformation of publicly released positions, with unusually strong performance around a major crisis. For information economics, it suggests that short sellers' information can concern aggregate cash flows rather than only firm-specific mispricing. Neither conclusion demonstrates that the signal remains profitable after publication or that the cash-flow interpretation is model-independent. The paper itself identifies those limitations.

## Constructing the short interest index

Section 2 uses January 1973 through December 2014, yielding 504 monthly observations and more than two million underlying asset-month observations. Compustat provides shares held short; CRSP provides shares outstanding. The historical Compustat series back to 1973 was added to the database only in 2014, although the original exchange releases were public at the time. A historical backtest therefore uses data that were theoretically observable but substantially more costly to assemble contemporaneously.

The universe includes common stocks, ADRs, ETFs, and REITs listed on U.S. exchanges. Exclude an asset if its price is below \$5 or its capitalization is below the fifth percentile of NYSE capitalization, using Kenneth French's breakpoints. Do not silently apply a common-stock-only filter: the authors deliberately include alternative security types because shorting sector and market ETFs can express aggregate negative information.

For each eligible asset $i$ in month $t$, define $s_{it}=SI_{it}/SO_{it}$, short shares divided by shares outstanding. Then form

$$
EWSI_t=\frac{1}{N_t}\sum_{i=1}^{N_t}s_{it},\qquad z_t=\log(EWSI_t).
$$

The logarithm is taken after averaging the ratios. Averaging log short ratios would be a different statistic and would create difficulties for zero observations. Nor is EWSI the ratio of all short shares to all outstanding shares, or a capitalization-weighted short ratio. Security splits and denominator alignment must be treated consistently in the raw join; the paper does not provide every database cleaning convention in its text.

Short positions are ordinarily compiled around the fifteenth and publicly reported four business days later, with financial-press publication the next day historically. After twice-monthly reporting begins in September 2007, the authors continue to use only the mid-month observations. This makes the information available for an end-of-month forecast without using the later report. Publication timing should be retained explicitly in any new implementation rather than assuming the measurement date equals the information date.

Estimate the deterministic trend

$$
z_t=a+bt+u_t,
$$

and standardize its fitted residual to unit standard deviation:

$$
SII_t=\frac{z_t-\widehat a-\widehat b t}{\widehat\sigma_u}.
$$

With an intercept the fitted residuals average zero. For in-sample analysis, trend and scaling parameters use the full sample. For forecasting, the trend is re-estimated recursively using only data available at the forecast origin. Scaling must likewise use information through that origin. A positive SII means unusually high short interest relative to the estimated secular trend, interpreted as greater pessimism; it does not mean that the raw short ratio exceeds a fixed percentage threshold.

EWSI averages 2.15% of shares outstanding in the asset-level ratio convention, with median 1.31% and standard deviation 1.98 percentage points. Its maximum is 8.93% in July 2008. Mean EWSI rises from 0.31% in 1973–1982 to 0.91% in 1983–1992, 1.82% in 1993–2002, and 4.98% in 2003–2014. These magnitudes motivate detrending: the same raw short ratio has a different interpretation at different stages of lending-market development.

Robust trend tests of Harvey, Leybourne, and Taylor reject a zero trend under persistent disturbances; Ng–Perron tests support stationarity around a linear trend. SII nevertheless has monthly autocorrelation 0.95. Stationarity around a fitted trend is not equivalent to low persistence or automatic validity of conventional predictive-regression inference. The paper uses specialized procedures for precisely this reason.

## Forecast target and competing predictors

The baseline target is the S&P 500 log return minus the log return on a one-month Treasury bill. For $h\in\{1,3,6,12\}$ define the average monthly excess return over the next $h$ months:

$$
r_{t:t+h}=\frac{1}{h}\sum_{j=1}^{h}r_{t+j}.
$$

It is an average of future monthly log excess returns, not the cumulative simple return. Multiplying a reported monthly-percentage-point slope by twelve gives its annualized effect. The predictive regression is

$$
r_{t:t+h}=\alpha_h+\beta_h x_t+\varepsilon_{t:t+h}.
$$

The fourteen comparison variables are the Goyal–Welch predictors: log dividend-price ratio, log dividend yield using lagged price, log earnings-price ratio, log dividend-payout ratio, return volatility, Dow Jones book-to-market, net equity expansion, three-month bill rate, long government yield, long government return, term spread, corporate default yield spread, corporate-minus-government default return spread, and CPI inflation. Dividend and earnings ratios use twelve-month moving sums; net equity expansion uses twelve-month net NYSE issuance relative to end-of-year NYSE market capitalization. The term spread is long yield minus bill rate; the default yield spread is Moody's BAA minus AAA.

One implementation difference from the familiar predictor dataset is important: return volatility is a twelve-month moving standard deviation of excess stock returns, rather than the sum of squared daily returns in a month. The authors make this change to avoid the extreme October 1987 observation. CPI release delay is respected. The predictor data and target come from Amit Goyal's updated series; a replication should record the exact historical file vintage because later revisions and extensions need not match it.

Each predictor is standardized to unit standard deviation for in-sample coefficient comparison. For the one-sided tests the signs of net equity expansion, bill rate, long yield, inflation, and SII are reversed so that the predicted coefficient is positive. Thus the positive 0.50 in the SII-minus row means a negative 0.50-percentage-point effect of a one-standard-deviation increase in actual SII. Sign normalization is a testing convention, not an economic reversal of the result.

Table 2 shows SII is only weakly related to the conventional variables. The largest absolute correlation is −0.28 with net equity expansion; correlations with dividend-price and earnings-price are −0.13 and −0.23. This motivates testing incremental information rather than treating SII as merely another valuation ratio. Weak contemporaneous correlation alone, however, does not establish incremental forecast value.

## In-sample estimation and inference

There are 503, 501, 498, and 492 usable observations at horizons one, three, six, and twelve months. Longer-horizon dependent variables overlap. The paper uses heteroskedasticity- and autocorrelation-robust $t$ statistics with wild-bootstrap significance, addressing both overlap and predictive-regression complications associated with persistent regressors. The article names these procedures but does not specify every bootstrap tuning choice, replication count, or covariance bandwidth. Those should be taken from verified replication code rather than fabricated from the tables.

The central Table 3 results are:

| Horizon in months | Slope for actual SII, percentage points per month | Robust absolute $t$ statistic | In-sample $R^2$ |
|---:|---:|---:|---:|
| 1 | −0.50 | 2.50 | 1.24% |
| 3 | −0.56 | 2.88 | 4.37% |
| 6 | −0.57 | 2.73 | 8.07% |
| 12 | −0.53 | 2.70 | 12.89% |

The slopes correspond to roughly six to seven percentage points lower annualized excess return per standard deviation higher SII. The annual-horizon $R^2$ does not mean that 12.89% of monthly return variance is forecastable. Longer-horizon averaging changes the signal-to-noise ratio, and overlapping observations provide much less independent information than their count suggests.

At the monthly horizon the default-return spread also reaches $R^2=1.24%$, so SII does not uniquely dominate every in-sample comparison at every horizon. At the annual horizon the term spread reaches 6.52%, the strongest conventional comparison, versus SII's 12.89%. The paper's claim is dominance over this named benchmark set and sample, not over every conceivable predictor.

To control for the conventional variables jointly, extract their first three principal components and estimate

$$
r_{t:t+h}=\alpha_h+\beta_{SII,h}SII_t+
\sum_{j=1}^{3}\beta_{j,h}\widehat f_{j,t}+\varepsilon_{t:t+h}.
$$

SII's slopes remain −0.51, −0.58, −0.59, and −0.55, with corresponding partial $R^2$ values 1.27%, 4.54%, 8.64%, and 13.69%. These are partial explanatory-power statistics for SII after the components, not the multiple regression's total $R^2$. The three-component specification compresses the competing information set; it does not prove that every nonlinear combination of the fourteen predictors is redundant.

## Recursive out-of-sample experiment

Forecast evaluation covers January 1990 through December 2014. The preceding January 1973–December 1989 history supplies a substantial initial estimation sample, especially valuable for fitting a time trend. At each origin $t$, estimate the detrending regression using observations through $t$, build SII on that information set, and estimate the horizon-specific return regression using completed outcomes only. For horizon $h$, an explanatory observation indexed $s$ is eligible only if $s+h\le t$. This restriction is essential: fitting on every origin through $t$ while inadvertently using its future $h$-month outcome introduces look-ahead bias.

The forecast is $\widehat r_{t:t+h}=\widehat\alpha_{h,t}+\widehat\beta_{h,t}x_t$. The benchmark is the prevailing historical average excess return, using only returns observed at the same origin. Re-estimating a historical detrended series at each origin is different from freezing today's full-sample residual history. The paper explicitly rules out full-sample detrending in the forecasting exercise; a replication should preserve this distinction even if the final plotted in-sample index looks similar.

Compute

$$
R^2_{OS}=1-
\frac{\sum_t(r_{t:t+h}-\widehat r_{t:t+h})^2}
{\sum_t(r_{t:t+h}-\overline r_t)^2}.
$$

Table 5 reports 1.94%, 6.54%, 11.70%, and 13.24% for SII at the four horizons. Positive values are proportional reductions in forecast mean squared error relative to the recursive mean, not in-sample regression fit. Clark–West tests reject the nested benchmark null at 1% for the first three horizons and 5% for twelve months. Serial dependence from overlapping forecasts is accounted for. An ordinary unadjusted Diebold–Mariano comparison is inappropriate for this nested-model setting.

All fourteen conventional predictors have negative out-of-sample $R^2$ at one and three months. At six months inflation reaches +1.95%; at twelve months the term spread reaches +3.35% and inflation +3.24%, although the latter is not statistically significant. These comparisons illustrate how very different in-sample and out-of-sample rankings can be.

Forecast-encompassing tests fit convex combinations

$$
\widehat r^*=(1-\lambda)\widehat r^{\,i}+\lambda\widehat r^{\,SII},
\qquad 0\le\lambda\le1.
$$

Estimated SII weights mostly equal one; remaining estimates are near one, with the annual term-spread comparison at 0.83. Harvey–Leybourne–Newbold tests reject zero SII weight for every comparison. Conversely, zero weight on the other forecast cannot be rejected. This supports SII's incremental information, but failure to reject a comparator's zero weight is not proof that its true contribution is exactly zero. The estimated combinations are evaluation devices, not a separately demonstrated real-time combination strategy.

## Asset allocation, constraints, and actual gains

Section 4 changes the forecasting target to **simple** excess returns for portfolio construction. An investor with relative risk aversion $\gamma=3$ sets

$$
w_t=\operatorname{clip}_{[-0.5,1.5]}
\left(\frac{\widehat\mu_{t+1}}{\gamma\widehat\sigma^2_{t+1}}\right).
$$

The conditional variance forecast comes from a trailing ten-year window. Both SII and prevailing-mean strategies use the same variance estimate, so weight differences arise from their expected-return forecasts. The bounds permit a 50% short equity position or a 150% long position; this is not a long-only allocation. The risk-free asset absorbs the residual weight.

For quarterly, semiannual, and annual experiments the forecast horizon matches rebalancing frequency. Forecasts used to implement those portfolios are nonoverlapping: weights are reset at the relevant period end and held over the next period. The article does not fully spell out every long-horizon variance aggregation and return-compounding convention. A reconstruction must put mean, variance, and realized holding-period return in matching units; simply pairing a twelve-month cumulative mean with a monthly variance would be incorrect.

Evaluate realized performance with

$$
CER=\overline R_p-\frac{\gamma}{2}\widehat{\operatorname{Var}}(R_p),
$$

and annualize the CER difference between the predictive strategy and the prevailing-mean strategy. This mean-variance criterion is an approximation to a utility comparison, not a general expected-utility identity for arbitrary nonnormal returns. The reported management-fee interpretation is a hypothetical willingness to pay under the stated criterion.

| Rebalancing horizon | Annualized CER gain, 1990–2014 | Annualized Sharpe ratio, SII | Sharpe ratio, prevailing mean |
|---|---:|---:|---:|
| Monthly | 4.17 percentage points | 0.66 | 0.39 |
| Quarterly | 4.65 percentage points | 0.60 | 0.31 |
| Semiannual | 5.44 percentage points | 0.72 | 0.37 |
| Annual | 3.43 percentage points | 0.53 | 0.35 |

These are the main Tables 6–7 economic findings. The reported baseline does not deduct an explicit transaction-cost schedule, borrowing fees, or differentiated funding spreads. A market-timing implementation also requires a tradable exposure proxy and execution timing. The evidence should therefore be described as allocation value before those implementation frictions, not a promised net performance record.

The subperiod split is central. During 1990–2006, SII's annualized CER gains are only 0.88, 0.73, 0.57, and −0.38 percentage points. During 2007–2014 they are 11.18, 13.08, 15.91, and 11.23 points. Before the crisis SII generally trails passive buy-and-hold on these comparisons; during the crisis interval it substantially exceeds it. Figure 2 shows the mechanism: the SII allocation becomes short early in the crisis, switches sharply toward an aggressive long position in late 2008, and remains strongly long through 2014. The large full-period gain is consequently concentrated in a small number of economically decisive episodes.

## Cash-flow versus discount-rate information

Section 5 uses total log stock returns, rather than excess returns, in a Campbell–Shiller log-linear decomposition. With $p_t=\log P_t$ and $d_t=\log D_t$,

$$
r_{t+1}\approx k+\rho p_{t+1}+(1-\rho)d_{t+1}-p_t,
\qquad \rho=\{1+\exp(\overline{d-p})\}^{-1}.
$$

Forward substitution under the stated no-bubble transversality condition implies an approximate innovation identity

$$
r_{t+1}-E_t r_{t+1}=\eta^{CF}_{t+1}-\eta^{DR}_{t+1}.
$$

Cash-flow news is the revision in expected discounted future dividend growth, with summation starting at the current next-period dividend; discount-rate news is the revision in expected future returns after that next period, with summation beginning one step later. The identity is derived from a log-linear approximation and an information set, not directly observed cash-flow surprises.

Estimate a first-order VAR with intercept,

$$
y_{t+1}=c+Ay_t+u_{t+1},\qquad y_t=(r_t,d_t-p_t,z_t')'.
$$

The paper suppresses the intercept in displayed notation, but not conceptually. Here $z_t$ contains either one conventional predictor or the first three principal components of all fourteen. The dividend-price ratio is always present; the dividend-price-only case has two variables rather than duplicating that ratio. SII is deliberately excluded from this market-information proxy.

Let $e_1$ select the return coordinate. After OLS estimation and calculation of $\widehat\rho$ from the sample dividend-price mean, construct

$$
\widehat\eta^r_{t+1}=e_1'\widehat u_{t+1},
\qquad
\widehat\eta^{DR}_{t+1}=e_1'\widehat\rho\widehat A
(I-\widehat\rho\widehat A)^{-1}\widehat u_{t+1},
$$

$$
\widehat\eta^{CF}_{t+1}=\widehat\eta^r_{t+1}+
\widehat\eta^{DR}_{t+1},\qquad
\widehat E_t r_{t+1}=e_1'(\widehat c+\widehat A y_t).
$$

A reproduction must check stability and the invertibility of $I-\widehat\rho\widehat A$. The cash-flow component is residually inferred after discount-rate news, so omitted predictive variables or VAR misspecification can be assigned to “cash-flow news.”

Regress each estimated component on SII, with an intercept for expected returns and zero intercepts for the mean-zero news series. The total-return predictive slope satisfies, apart from rounding,

$$
\widehat\beta=\widehat\beta_E+\widehat\beta_{CF}-\widehat\beta_{DR}.
$$

The total slope is −0.51 percentage points monthly, robust $t=-2.53$. In the return/dividend-price VAR the components are −0.07, −0.35, and +0.09. In the principal-component VAR they are −0.05, −0.31, and +0.15. Thus the cash-flow coefficient is the largest contribution in either specification, while discount-rate news also matters. Across Table 8 the cash-flow estimates range approximately from −0.27 to −0.40 and are significant at conventional levels. One cannot analogously divide the total $R^2$ into three independent shares because the components are correlated.

The interpretation is explicitly conditional. If SII enters the VAR information set, it becomes orthogonal to subsequent estimated news by construction. The competing explanation is then that SII proxies a time-varying equilibrium expected return. The paper cannot resolve that joint-hypothesis problem merely by labeling the residual cash-flow news. Its evidence favors an informed-trading reading relative to conventional predictor information, not a model-free rejection of rational time-varying risk premia.

## Robustness, limits, and a reconstruction sequence

Alternative in-sample detrending uses quadratic and cubic deterministic trends or a trailing sixty-month log-EWSI average. The stochastic-detrending sample begins in December 1977. Annual-horizon $R^2$ values are 15.51%, 8.35%, and 11.02%, respectively, versus 12.89% under linear detrending. The cubic annual coefficient has wild-bootstrap $p=0.11$, an exception to broad significance. Reported out-of-sample robustness is similar for quadratic and stochastic detrending and for cubic detrending at shorter horizons; exact supplementary cells are not supplied here.

The authors report significant IVX-Wald predictability tests robust to regressor persistence and no significant Elliott–Müller parameter-instability test. Yet the first and last decadal subsamples are significant while the two middle decades are not. This is compatible with crisis concentration; absence of a detected structural break does not establish uniform forecast strength. They also report predictive results for equal-weighted CRSP and S&P returns, common-stock-only or alternative-security-only universes, and weights proportional to log capitalization. The baseline broad equal-weighted index remains strongest. Ordinary capitalization weighting emphasizes large stocks, whose short ratios vary less, and is not the maintained baseline.

For replication, first reconcile asset-month counts and EWSI descriptive moments; then verify the log-after-aggregation transformation, trend residuals, and information-date joins. Reproduce in-sample coefficients with the target's monthly-average normalization. Build recursive forecasts with horizon-complete training labels and refitted trends. Only after matching forecast errors should the simple-return allocation and its constraints be implemented. Finally, reconstruct the VAR components and verify the slope-addition identity numerically. These separate checks localize mistakes that a single terminal-wealth comparison would obscure.

Unreported choices still include several raw-data cleaning rules, detailed bootstrap settings, and some long-horizon portfolio conventions. The linked replication materials are the natural next evidence source for those choices; their existence does not justify inventing their contents. Beyond replication, post-2014 testing, realistic trading costs, a precommitted trend-break rule, and tests of sensitivity to the crisis interval are required to evaluate present usefulness. The source provides a strong historical result whose economic interpretation and portability remain conditional on those design decisions.

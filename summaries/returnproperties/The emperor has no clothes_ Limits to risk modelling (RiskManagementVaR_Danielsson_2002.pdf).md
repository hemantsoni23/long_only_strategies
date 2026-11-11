# The emperor has no clothes: Limits to risk modelling

**Author:** Jón Daníelsson. **Publication:** Journal of Banking & Finance 26 (2002), 1273–1296. **Source:** [RiskManagementVaR_Danielsson_2002.pdf](../../Finance/RiskManagementVaR_Danielsson_2002.pdf), 24 PDF pages. Printed page numbers equal PDF page numbers plus 1272. The full paper, Appendix A, both numerical tables, and the illustrative figures were inspected. Statements about regulation describe the 1996 rules and 2001 Basel II proposals discussed by the author; this note does not present them as current requirements.

## Why this matters and what is new here

The paper asks whether a risk statistic remains useful when institutions act on it, particularly when many institutions face similar limits. It combines a rolling forecasting comparison with a critique of using a single loss quantile to set capital and trading constraints. The empirical contribution is evidence that forecast calibration and forecast stability vary considerably with asset, probability level, and estimation window. The conceptual contribution is to connect those instabilities to endogenous trading responses and to distinguish an internally useful forecasting tool from a reliable instrument for reducing systemic risk.

There is no newly estimated structural model of crises in this paper. The discussion of feedback draws on other theoretical studies and historical accounts of 1987 and 1998. The empirical exercise measures daily risk forecasts for individual asset series, not endogenous liquidation, aggregate leverage, or the causal effect of capital rules. Consequently, it supports a diagnosis of fragile model-dependent measurements more directly than the strong policy conclusions in the introduction. An implementation should preserve that distinction instead of treating a forecasting table as proof that a particular regulation caused a crisis.

The paper is also a useful warning about the objective of model validation. An unconditional violation frequency close to its target is not the same as accurate conditional forecasts, stable capital requirements, sensible rankings of portfolios, or calibrated probabilities of bank failure. These are different properties and require different data and tests. The author argues that reporting a single VaR number can conceal the distinctions.

## Definitions and an unambiguous sign convention

Let $r_{t+1}$ be a one-period portfolio return and let monetary or percentage loss be $L_{t+1}=-r_{t+1}$ in the corresponding units. At confidence level $c$, define positive-loss VaR by

$$
\operatorname{VaR}_{c,t}=F^{-1}_{L_{t+1}\mid\mathcal F_t}(c).
$$

Equivalently, write the lower-return quantile $q_{p,t}$ with $p=1-c$, so $\operatorname{VaR}_{c,t}=-q_{p,t}$ under compatible quantile conventions. A breach is $r_{t+1}<q_{p,t}$, or $L_{t+1}>\operatorname{VaR}_{c,t}$. The paper switches between negative return thresholds in Table 2 and positive loss magnitudes in its discussion and Figure 3; code should choose one convention and convert explicitly.

For $n$ forecasts, let $I_t$ be the breach indicator. The reported violation ratio is

$$
VR=\frac{\sum_{t=1}^n I_t}{np}.
$$

A value above one means more losses exceeded the threshold than expected: risk was underforecast at that quantile. A value below one means overforecasting. At 99% confidence and approximately 2,500 observations, the expected number of breaches is only 25. The author's proposed acceptable interval $0.8$–$1.2$ is a heuristic, not a reported hypothesis-test confidence interval.

For context, under independent correctly calibrated Bernoulli breaches the approximate standard deviation of this ratio is $\sqrt{(1-p)/(np)}$, about 0.20 for $p=0.01$ and $n=2500$. This calculation is an interpretation supplied here; it shows why a ±20% heuristic should not be confused with a 95% statistical acceptance region. Serial clustering changes the uncertainty further. The original study does not report conditional-coverage or independence tests for the table entries.

A coherent expected shortfall in a loss convention is the average of the upper quantiles,

$$
ES_c=\frac1{1-c}\int_c^1F_L^{-1}(u)\,du.
$$

For a continuous distribution this equals $E[L\mid L>\operatorname{VaR}_c]$. With atoms, the quantile integral allocates fractional mass at the threshold and is preferable to an unqualified conditional expectation. ES is total tail loss, not only the excess above VaR. The paper's informal ES discussion should be read with this distinction in mind, especially because its bond example has discrete payoffs.

## The empirical design that can actually be reconstructed

Section 3 and Appendix A describe daily observations obtained from Datastream, from each series' first available observation through the end of 1999. The listed universe includes the S&P 500, Hang Seng, Microsoft, Amazon, ringgit–pound and pound–dollar exchange rates, a clean US government bond price index, gold, and oil. The main tables present six series: S&P 500, US bond, oil, Hang Seng, Microsoft, and GBP/USD. Gold, Amazon, and ringgit–pound are not tabulated there.

The author describes the daily histories generally as at least 15 years long and the main forecasts as covering the 1990s, roughly 2,500 forecasts per series. That general description cannot literally apply to every listed asset, especially Amazon. Exact initial forecast dates and sample counts by series and window are not supplied. The S&P 500 discussion identifies 2,527 observations. Reproduction must not manufacture a common 1990 start for a series without the necessary prior history.

For each asset and each model, the window length is $W\in\{300,1000,2000\}$ daily observations. Estimate the model using the current window, forecast the next day's quantile, observe the next return, shift the window forward by one day, and reestimate. The procedure is rolling, not an expanding fit and not one fixed full-sample parameter estimate with recursive volatility updates. The original paper does not document parameter warm starts, optimization tolerances, or treatment of failed fits.

Four methods are compared: Gaussian GARCH, Student-$t$ GARCH, historical simulation, and an unconditional extreme-value approach. Section 3 calls the GARCH family variance–covariance models. It does not supply the precise GARCH order, mean equation, parameter constraints, likelihood initialization, or Student-$t$ degrees-of-freedom estimation rule. Calling the study an exact implementation of GARCH(1,1) would therefore overstate its disclosure.

A conventional implementation skeleton would write $r_t=\mu_t+\sigma_tz_t$, estimate a conditional variance recursion, and forecast $q_{p,t}=\mu_{t+1\mid t}+\sigma_{t+1\mid t}F_z^{-1}(p)$. Gaussian innovations use a normal quantile. Standardized Student-$t$ innovations require a variance-normalization factor when degrees of freedom exceed two. These equations explain the model family; the paper does not give enough information to select their precise fitted version. RiskMetrics is mentioned as a special case or related conditional-volatility method, not reported as a separate fifth model in the tables.

Historical simulation uses an empirical quantile of returns in the current window. The text does not state an interpolation or order-statistic convention, whether observations are demeaned, or how ties are handled. The unconditional EVT column likewise lacks a specified threshold, tail-index estimator, threshold-selection rule, or small-sample fallback. In many short-window rows EVT and HS are numerically identical. That fact is visible in the table but does not identify the undocumented implementation rule responsible for the equality.

Price adjustments, dividends, bond duration and index identifier, oil contract or spot-series identifier, FX quote orientation beyond the labels, log versus simple returns, holidays, stale observations, and missing-data handling are not specified. These omissions materially limit exact reproduction. A clean rerun can implement the disclosed rolling design and compare model families, but it would be a documented reconstruction rather than a byte-for-byte replication of the original results.

## Calibration results and their numerical meaning

Table 1, printed page 1280, reports the following 99% violation ratios. Each triplet is ordered by the 300-, 1,000-, and 2,000-day estimation windows.

| Asset | Gaussian GARCH | Student-$t$ GARCH | Historical simulation | EVT |
|---|---|---|---|---|
| S&P 500 | 1.46 / 1.27 / 0.91 | 1.07 / 0.83 / 0.67 | 0.79 / 0.95 / 1.07 | 0.79 / 0.99 / 1.07 |
| US bond | 0.94 / 0.53 / 0.37 | 0.66 / 0.57 / 0.49 | 0.49 / 0.66 / 0.67 | 0.49 / 0.41 / 0.37 |
| Oil | 1.76 / 1.67 / 1.64 | 1.38 / 1.30 / 1.04 | 1.17 / 0.92 / 0.35 | 1.17 / 1.00 / 0.35 |
| Hang Seng | 2.18 / 1.90 / 2.02 | 1.41 / 1.29 / 1.21 | 0.69 / 1.17 / 1.09 | 0.69 / 1.21 / 1.09 |
| Microsoft | 2.24 / 1.98 / 2.25 | 1.78 / 1.60 / 1.69 | 1.58 / 1.84 / 2.06 | 1.58 / 1.74 / 1.87 |
| GBP/USD | 2.13 / 1.85 / 1.62 | 1.42 / 1.18 / 1.14 | 0.79 / 0.63 / 0.47 | 0.79 / 0.63 / 0.47 |

The Gaussian GARCH column ranges from 0.37 to 2.25 in the actual table, although the surrounding prose reports an upper bound of 2.18. The Microsoft entries establish the higher maximum. All methods and windows overforecast the bond series and underforecast Microsoft. The Gaussian model strongly underforecasts Hang Seng and GBP/USD at 99%, while its S&P 500 calibration improves as the window lengthens. A different method or longer history does not fix every asset simultaneously.

Window sensitivity is substantial even within a single estimator. For oil, historical simulation changes from 1.17 to 0.92 to 0.35 as the window increases. For GBP/USD the corresponding ratios decline from 0.79 to 0.63 to 0.47, increasing conservatism. Conversely, Microsoft historical simulation moves from 1.58 to 2.06, becoming less conservative at the longest window. Longer histories therefore do not uniformly improve quantile calibration in this experiment.

The author reports, without an equivalent complete table in this paper, that Gaussian conditional models tend to perform best at 95% and EVT at 99.9%. Those statements are qualitative reports of the larger survey, not conclusions that can be independently recalculated from Table 1. The results show that model ranking depends on the probability level. They do not establish that any model is universally optimal at a named confidence level.

## Forecast variation is a separate diagnostic

The study also measures the sample dispersion and range of the sequence of VaR forecasts. Table 2 calls its dispersion measure “SE,” but the text defines it as the standard deviation of forecast levels over time, not a standard error of an estimated mean. Nor is it the standard deviation of day-to-day forecast changes. A slowly trending forecast can have a large level standard deviation without large daily jumps. The distinction matters when interpreting the author's claims about rebalancing costs.

For the S&P 500, daily return standard deviation is 0.89 percentage points, the worst daily return is minus 7.11%, and the best is 4.99%. At the 1% lower-return tail, the forecast statistics are:

| Window and model | Standard deviation of forecast, percentage points | Most negative threshold | Least negative threshold |
|---|---:|---:|---:|
| 300-day Gaussian GARCH | 0.66 | −7.52% | −1.05% |
| 300-day Student-$t$ GARCH | 0.68 | −6.68% | −1.09% |
| 300-day HS | 0.71 | −3.91% | −1.26% |
| 300-day EVT | 0.71 | −3.91% | −1.26% |
| 2,000-day Gaussian GARCH | 0.60 | −5.23% | −1.14% |
| 2,000-day Student-$t$ GARCH | 0.64 | −5.45% | −1.26% |
| 2,000-day HS | 0.29 | −2.72% | −1.90% |
| 2,000-day EVT | 0.33 | −2.84% | −1.90% |

At this confidence level, the long-window unconditional methods are much steadier. However, a blanket claim that they are always least volatile is contradicted by other rows. At the 0.1% lower tail and a 2,000-day window, forecast standard deviations are 0.80 for Gaussian GARCH, 1.06 for Student-$t$ GARCH, 2.10 for HS, and 1.42 for EVT. At a 300-day window, both HS and EVT have standard deviation 1.94 and a most negative threshold equal to the sample minimum, minus 7.11%. A 0.1% empirical tail with only 300 points contains fewer than one expected observation, so tail conventions and extremes dominate.

The paper argues that forecast instability can create unstable risk limits and capital allocations. It does not calculate realized trading costs, capital-raising costs, or a loss function that trades responsiveness against stability. A rapidly changing forecast can be appropriate when true conditional risk changes. Thus lower forecast variation is not independently sufficient evidence of a better model. The useful comparison is stability conditional on acceptable calibration and the intended decision problem.

Figures 2–3 show the Hang Seng around the 1997 Asian crisis. Daily moves include a fall of roughly 15% and a rebound of about 18%; Gaussian GARCH VaR rises to roughly 19–20% and decays over more than a month, while HS remains near 4–5%. The paper attributes much of the conditional-volatility increase to the large positive rebound because the symmetric variance model reacts to squared shocks. This is a mechanism demonstration, not a causal estimate of how much of the crisis was due to risk limits. The printed Figure 3 caption contains unrelated text about a sample economy; its plotted GARCH and HS lines and the surrounding discussion identify the intended comparison.

## Why the time horizon matters

The historical regulatory discussion concerns a 99% ten-day loss threshold. Direct estimation from nonoverlapping ten-day observations sharply reduces sample size: 250 daily observations give approximately 25 ten-day returns and only 0.25 expected observations in a 1% tail. Matching the number of nonoverlapping observations in a one-year daily study requires roughly ten years of daily history. The source's assertion that at least 3,000 days are required is a rule of thumb, not a theorem establishing sufficient accuracy.

For zero-mean independent Gaussian daily losses with common variance $\sigma^2$,

$$
\operatorname{VaR}_{c,T}=\sqrt T\,\sigma\Phi^{-1}(c).
$$

This justifies a square-root rule in that setting. With nonzero mean, the mean scales as $T$ and the centered standard deviation as $\sqrt T$; scaling the entire one-day VaR omits that distinction. Serial dependence, time-varying conditional variance, nonlinear portfolio exposure, and non-Gaussian tails can invalidate the simple rule. Gaussian iid assumptions are sufficient for exact normal-quantile scaling, not logically necessary for every distribution or approximation with a similar scaling relation.

The paper's strongest language says overlapping returns cannot be used and that multiperiod conditional forecasts are essentially impossible. Those statements are too absolute as mathematical claims. Overlapping observations create dependence that must be accounted for; they do not become unusable merely because they overlap. Conditional simulation or another explicitly specified dynamics model can generate multiperiod distributions, though their reliability remains model dependent. The defensible lesson is that multiplying a one-day estimate by $\sqrt{10}$ does not remove uncertainty about future dynamics.

Intraday scaling adds deterministic variation in trading activity and volatility across the day. A one-hour forecast near the open need not be interchangeable with one near midday. The source identifies this issue but gives no intraday estimator or experiment. Its numerical example in which a daily loss amount of one million could correspond to ten-day amounts around 1.5 or 6 million is illustrative, not a calibrated confidence interval.

## Dependence and the limits of the single-asset experiment

A portfolio model must specify more than marginal volatility. Nonelliptical joint distributions can produce downside dependence that a constant correlation matrix misses. The paper reproduces a selection of monthly correlation estimates from Erb, Harvey, and Viskanta: US–Germany correlation is 8.6% in jointly rising markets, 52% in jointly falling markets, minus 61% in mixed markets, and 35% overall. US–UK figures are 32%, 58%, minus 60%, and 50%. These are cited prior-study results, not new estimates from Appendix A.

Conditioning on market directions itself changes sample correlations. Such figures should not automatically be read as causal evidence that a correlation parameter changed or that all assets approach perfect correlation in every crisis. The author's claim that correlations reach almost 100% is rhetorical generalization, not an estimated universal law. The practical requirement is to evaluate the relevant joint tail distribution and the conditioning event, rather than infer portfolio tail risk from one unconditional covariance matrix.

Time zones create another measurement issue. A global shock can be reflected in US prices on one calendar date and in Asian or European prices over adjacent dates. Contemporaneous close-to-close correlations can then understate economic comovement or misidentify the location of the largest shock. The survey deliberately avoids portfolio aggregation and therefore cannot quantify this problem. Its single-asset design is a controlled simplification, not a demonstration that portfolio models must fail by a known larger amount.

## Quantile ranking, diversification, and manipulation

Example 1 gives an exact discrete illustration of VaR's failure of subadditivity. Each of 100 independent bonds has profit minus 100 with probability 0.01 and plus 2 otherwise. Compare holding one of each bond with holding 100 units of one bond. If $D\sim\operatorname{Binomial}(100,0.01)$, the diversified profit is $200-102D$, so diversified loss is $102D-200$. The concentrated loss is minus 200 with probability 0.99 and 10,000 with probability 0.01.

At 95% confidence, the concentrated VaR is minus 200: this quantile sees only the coupon outcome. Since $P(D\leq2)\approx0.9206$ and $P(D\leq3)\approx0.9816$, the diversified 95% VaR is $102(3)-200=106$. These numerical quantiles are derived here from the paper's example. Thus the diversified VaR exceeds the sum of individual VaRs, even though concentration creates the much larger rare loss. Flooring reported capital at zero changes the numerical concentrated charge but does not remove the misranking. The example is about a particular confidence level and discrete distribution, not proof that diversification always worsens VaR.

Figure 4 makes a related point by comparing a roughly normal series with a sparse sequence of large losses. The author reports standard deviations 1 and 0.7 and 99% VaRs approximately 2 and 7, respectively. The graph has 500 observations, and discrete quantile conventions at a 1% boundary matter. The source does not give the generating law or seed, so these are schematic illustrative numbers rather than a reproducible Monte Carlo result. Volatility remains a well-defined measure outside normality; the limitation is that it does not characterize the full downside distribution.

Example 2 proposes manipulating a VaR constraint with options and Figure 5 sketches a shifted profit CDF. The economic point is that improving one quantile can leave worse losses beyond it inadequately measured. The printed option description does not provide a complete self-financing trade: the underlying, premium, discounting, position sizes, and state-to-profit map are unspecified, and VaR symbols there represent negative profit thresholds. A unit long higher-strike put minus a unit lower-strike put is a bounded payoff spread; by itself its written strikes do not establish the claimed worsening of the extreme tail. Reproducing the proposed manipulation requires a complete payoff and financing specification rather than merely copying the two strikes.

Replacing a single quantile with expected shortfall measures more of the adverse tail and restores coherence under the usual definition. It does not eliminate estimation error, all model arbitrage, or all incentives to exploit unmeasured states. The paper recognizes greater tail-data demands, but its suggestion that ES makes manipulation impossible is stronger than the argument supplied.

## Endogenous risk and the scope of the policy argument

The proposed feedback mechanism is straightforward: measured risk rises; institutions sharing similar limits reduce risky holdings; simultaneous sales worsen prices and liquidity; realized volatility and measured risk rise further. Regulatory uniformity may synchronize the response, but private incentives can do so too. The author explicitly notes that the 1987 portfolio-insurance episode did not require the market-risk rules under discussion. The paper does not estimate a feedback coefficient, identify an exogenous regulatory shock, or compare otherwise similar constrained and unconstrained institutions.

A 99% daily quantile is expected to be breached about 2.5 times in 250 trading days even when perfectly calibrated. It therefore cannot be interpreted directly as a probability of insolvency or systemic collapse. Translating it into those events would require balance sheets, funding and liquidation dynamics, joint institutional exposures, and loss absorption. The paper's policy proposals—less model-sensitive capital, state-contingent requirements, and cross-insurance—are arguments for further design work, not evaluated counterfactual policies with reported welfare estimates.

The lasting research task is to test a model against the decision it supports. This source provides a replicable outer forecasting loop, substantial numerical evidence of sensitivity, and concrete reasons to model feedback and joint tails. It does not disclose enough estimation detail for exact reproduction of its four columns, prove that every risk model breaks down when regulated, or establish that forecast volatility alone is a defect. Keeping those limits explicit makes its warning more useful than adopting its most categorical rhetoric.

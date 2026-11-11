# Skulls, Financial Turbulence, and Risk Management

**Mark Kritzman and Yuanzhen Li (2010).** *Financial Analysts Journal* 66(5), September/October, 30–41. [Source PDF](../../Finance/TurbulenceDeleveraging_KritzmanLi_2010.pdf). All twelve pages were read, including the portfolio-construction appendix, figures, six tables, and endnotes. Printed page 30 corresponds to PDF page 1. This note separates retrospective diagnostics, a pre-crisis risk illustration, randomized portfolio tests, and a lagged currency-carry filter; they are different experiments with different information sets.

## Why this matters

A portfolio can experience unusual combinations of otherwise moderate returns when historically correlated assets decouple. Conversely, individually volatile assets can offset one another in a portfolio-level index and conceal a change in the joint environment. The turbulence index measures the unusualness of the complete return vector relative to a reference mean and covariance. It therefore detects cross-asset combinations that a single aggregate volatility series can miss.

The statistical measure is not new: it is the squared Mahalanobis distance, applied to financial returns in Chow and coauthors (1999). This paper’s contribution is to connect its empirical persistence and conditional return patterns to three applications: conditional risk assessment, portfolio construction emphasizing turbulent observations, and a rule for scaling currency-carry exposure. It does not establish that turbulence predicts the onset of a crisis. The proposed timing benefit comes from persistence after turbulence has begun.

## Exact statistic and interpretation

Use column-vector notation for $n$ asset returns $r_t$, with reference mean $\mu$ and invertible covariance $\Sigma$. The article’s equation (2) is

$$
d_t=(r_t-\mu)^T\Sigma^{-1}(r_t-\mu).
$$

There is no square root and no division by $n$ in this definition. The conventional Mahalanobis distance is $\sqrt{d_t}$; the paper’s second endnote explicitly distinguishes the two. For ordinal thresholding the transformation does not change rankings, but absolute levels and comparisons across dimensions are affected.

If $\Sigma=CC^T$, then $d_t=\|C^{-1}(r_t-\mu)\|^2$. This whitening interpretation explains why a move along a historically low-variance spread can be highly unusual even if each asset’s own return is moderate. The statistic is nondirectional: a large positive joint return can be turbulent just as a large loss can. The paper’s negative conditional returns are empirical observations, not consequences of the quadratic form alone.

The mean, covariance, sample frequency, asset set, and reference window are part of the definition. A full-sample estimate is appropriate for retrospective classification but uses future information if treated as a historical trading signal. Covariance inversion also requires adequate rank and numerical conditioning. The paper does not prescribe a general regularization rule for the turbulence metric; adding one changes the implementation and should be recorded.

The geometric diagrams use ellipsoids enclosing a chosen fraction of a Gaussian distribution. Actual turbulent observations are selected by empirical score thresholds. A known-parameter Gaussian squared distance has a chi-squared interpretation, but fitted means/covariances and non-Gaussian financial returns prevent treating that nominal distribution as a universally calibrated test in these applications.

## Descriptive samples and persistence evidence

Figure 4 uses monthly returns on six asset classes—U.S. and non-U.S. stocks, U.S. and non-U.S. bonds, commodities, and U.S. real estate—from January 1980 to January 2009. Its reference mean and covariance use the complete sample. The resulting spikes coincide with recognizable market disruptions, including 1987, the Russian default, and 2007–2008. This is historical event alignment, not an out-of-sample forecasting exercise.

Figure 5 compares returns during turbulent and quiet periods over January 1993–December 2008, using daily data from 4 January 1993 for equities, styles, and currencies, and monthly HFRI Fund of Funds Composite returns for hedge funds. The other return series are MSCI World, Russell 2000 minus S&P 500, Russell 1000 Growth minus Russell 1000 Value, and a naive currency carry strategy. Turbulence is based on the relevant global-allocation, U.S.-sector, or developed-currency universe. The figure uses full-sample covariance estimates and documents poor contemporaneous returns to risk; it does not itself show a tradeable forecast.

Table 1 examines average daily turbulence over the next 5, 10, and 20 days after a day in the most turbulent 10%, excluding that initial day. Scores are normalized to an average of one, and thresholds are estimated from full-sample returns. The source reports:

| Universe | Subsequent 5-day mean | 10-day mean | 20-day mean | Top-decile threshold |
|---|---:|---:|---:|---:|
| Global assets | 2.31 | 2.22 | 2.13 | 1.93 |
| U.S. assets | 2.98 | 2.90 | 2.79 | 1.95 |
| U.S. sectors | 3.12 | 3.04 | 2.87 | 2.03 |
| Currencies | 2.08 | 1.93 | 1.80 | 1.83 |
| U.S. fixed income | 4.05 | 3.85 | 3.60 | 2.12 |
| U.S. Treasury notes | 3.19 | 3.13 | 2.96 | 2.00 |
| U.S. credit | 4.17 | 4.09 | 3.69 | 1.61 |

The respective samples begin in January 1993, August 1989, January 1973, January 1975, December 2000, September 1998, and August 1998; all end in April 2009. The table labels its extreme threshold a “10th percentile,” using a high-turbulence tail convention. It should not be mistaken for the bottom 10% of an ordinary ascending score distribution.

The result is persistence in average subsequent unusualness. It does not imply every subsequent day remains extreme. Event windows can overlap, and the source gives no standard errors, event-thinning procedure, or test accounting for overlapping windows. The evidence motivates a lagged signal but is not a calibrated conditional probability of another crisis day.

## Stress-risk comparison before the financial crisis

The risk illustration estimates means and covariances using monthly data from January 1977 through December 2006. It identifies the top 25% of months by turbulence, using the 75th-percentile threshold and the full pre-crisis sample as the metric reference. The five-asset portfolio inputs are:

| Asset or input | Conservative | Moderate | Aggressive |
|---|---:|---:|---:|
| U.S. stocks, percent weight | 22.86 | 35.23 | 48.15 |
| Non-U.S. stocks | 16.59 | 24.22 | 32.19 |
| U.S. bonds | 49.95 | 32.81 | 14.89 |
| Real estate | 3.85 | 2.59 | 1.28 |
| Commodities | 6.75 | 5.16 | 3.49 |
| Assumed expected return, percent | 7.60 | 8.37 | 9.17 |
| Full-sample annual risk, percent | 7.77 | 10.12 | 12.86 |
| Turbulent-subsample annual risk, percent | 10.68 | 13.68 | 17.33 |

Conditional volatility is substantially larger for all three portfolios. Table 3 then compares a five-year terminal-loss VaR based on full-sample risk with a within-horizon VaR using turbulent risk. The tail probability is 1%, conventionally corresponding to 99% coverage:

| Portfolio | Terminal VaR, full sample | Within-horizon VaR, turbulent sample | Maximum loss from January 2007 inception through September 2009 | Maximum drawdown over that period |
|---|---:|---:|---:|---:|
| Conservative | 2.10% | 26.20% | 19.60% | 25.80% |
| Moderate | 9.90% | 35.10% | 29.42% | 35.50% |
| Aggressive | 18.70% | 45.00% | 38.96% | 45.30% |

The larger stress estimates are much closer to the subsequent crisis losses. This particular comparison does use data ending before the crisis. However, it changes two things simultaneously: the volatility estimate and whether risk is measured only at the horizon or anywhere before it. It does not isolate how much improvement comes from turbulence conditioning alone.

Within-horizon loss from initial wealth also differs from peak-to-trough drawdown. The two realized columns are useful comparisons, but neither is automatically the identical estimand as the modeled within-horizon VaR. The paper refers to first-passage probability calculations for continuous VaR but does not provide the complete process specification and numerical implementation in this article. One crisis episode cannot validate a 1% probability calibration or establish which event was expected to occur when.

## Randomized portfolio-construction experiment

Appendix A uses eight assets: U.S. equities, MSCI EAFE equities, U.S. Treasury bonds, U.S. corporate bonds, TIPS, commodities, REITs, and cash. The historical sample spans 1973–2009. TIPS before 1997 are backfilled using U.S. CPI returns and bond-index returns of similar duration; the source does not provide the exact backfill formula or underlying return file.

For each of 1,000 trials, half the observations are randomly selected for training and the other half for testing. A turbulent subset is identified within training, and an unconditional portfolio is compared with a turbulence-conditioned one. Both portfolios are evaluated over all test observations and over turbulent test observations.

There is a material threshold discrepancy. The main text says the highest quartile is selected, implying the 75th percentile. The appendix specifies the **70th percentile**, implying a 30% turbulent training subset. Its footnote says results are not especially sensitive to that threshold, but no sensitivity table resolves which setting produced the reported results. A replication should run and label both settings rather than silently select one.

The appendix says the training threshold is reused to classify testing observations. The metric’s mean/covariance reference for every testing calculation is not specified with the same precision. A clean implementation would freeze the reference moments estimated from training, but that is an explicit reconstruction choice. Randomly mixing historical dates between training and testing is a held-out observation test, not a chronological trading simulation: future regimes can inform portfolios tested on earlier dates.

## Modified mean–variance method

The unconditional expected returns are equilibrium returns using a market portfolio of 60% U.S. equities, 30% Treasury bonds, and 10% corporate bonds. The source does not give every reverse-optimization scaling parameter. For conditioned returns, both turbulent-subset and full-training sample means are shrunk toward a common scalar target and their difference is blended with equilibrium returns.

The appendix’s shrinkage equations can be transcribed completely. For sample mean $\widehat\mu$, sample covariance $\Sigma$, dimension $n$, observation count $T$, and all-ones vector $e$,

$$
\mu_m=\frac{e^T\Sigma^{-1}\widehat\mu}{e^T\Sigma^{-1}e},
$$

$$
w=\frac{n+2}{n+2+T(\widehat\mu-\mu_me)^T\Sigma^{-1}(\widehat\mu-\mu_me)},
$$

$$
\mu_s=w\mu_me+(1-w)\widehat\mu.
$$

The target is the estimated expected return of the global minimum-variance portfolio, replicated across assets. The same process is applied separately to the turbulent and full samples, using their corresponding sample sizes and estimates. It is not shrinkage of every asset toward its own historical mean.

Covariances are shrunk toward a one-factor market-model covariance using the cited Ledoit–Wolf approach. Conditioned covariances blend the shrunk turbulent estimate with the full-training estimate. Return adjustments and covariance blending use ratios proportional to sample sizes, but the article does not state a complete unambiguous algebraic weighting rule. Representing the conditioned mean as equilibrium returns plus a weighted difference of the two shrunk means captures its described structure; assigning an exact numerical weight requires a declared reconstruction or original code.

Both portfolios are optimized in a mean–variance framework, with risk aversion selected so training risk is approximately 10% annually for each. The feasible weight constraints, precise risk-aversion search, and solver are not fully specified. Those choices affect whether comparison portfolios have similar leverage and whether their solutions are stable, so they cannot be treated as irrelevant implementation details.

## Modified full-scale method

The full-scale experiment first adjusts training returns so asset means equal the same equilibrium-return estimates. It then increases turbulent observations’ representation through bootstrapping: the turbulent subset is sampled at three times the frequency used for the full training sample. The precise combined sample size and resampling mechanics are not given; sampling the subset three times as often is not the same as declaring all turbulent observations to constitute exactly 75% of the final sample.

The unconditional comparator is a mean–variance portfolio. The conditioned portfolio is selected by direct expected-utility optimization on the modified sample. Thus the comparison changes both scenario emphasis and the objective function; it does not isolate a pure effect of reweighting under one unchanged optimization criterion.

The utility function is

$$
U(x)=\begin{cases}
\log(1+x),&x\geq\theta,\\
\gamma(x-\theta)+\log(1+\theta),&x<\theta,
\end{cases}
\qquad \theta=-0.15,\quad\gamma=2.25.
$$

The article defines $x$ as annually compounded portfolio return. Utility is continuous at the threshold but has a derivative kink; it is not a jump in the level of utility. At $-15\%$, the slope above the threshold is $1/0.85$, while the lower-branch slope is 2.25, giving a larger marginal penalty for deeper losses.

For each candidate weight vector, utilities are summed across sample periods and the highest total is selected. The source describes searching many weight combinations but omits the exact search method, constraints, convergence tolerance, and mapping from input return frequency to the annual-return variable. Those omissions prevent exact numerical reproduction from the appendix alone.

## Portfolio-test results and their interpretation

Table 4 reports that the conditioned portfolio beats the unconditional comparator in turbulent held-out observations in **85%** of mean–variance trials and **86%** of full-scale trials. Across all market conditions, the corresponding frequencies are **45%** and **41%**. Figure 6 visually shows median annualized turbulent-period gains of roughly 3.6 and 4.5 percentage points, with full-sample median costs of approximately 0.3 and 0.4 percentage points. These figure values are approximate readings, not reported numerical table entries.

The result is a trade-off: materially better performance in selected turbulent observations with a small median return sacrifice across all observations. It is not general outperformance in most full-sample trials. The 1,000 trials repeatedly reuse the same historical dataset; their win frequencies are not independent Bernoulli observations or statistical confidence levels. The source gives no confidence intervals, independent final holdout, transaction-cost model, or turnover comparison.

## Carry exposure filter: timing, ranks, and numerical results

The underlying carry strategy estimates expected returns from currency forwards’ annualized monthly discounts or premiums, holds an equally weighted combination of long discount currencies and short premium currencies, and rebalances monthly. The risk filter computes a 30-day moving average of daily turbulence from the G–10 currency return set, assigns a quintile using a trailing three-year history, and applies the exposure with a **one-day implementation lag**.

Table 5 specifies exposures of 20%, 40%, 60%, 80%, and 100% for quintiles one through five. To implement the text’s stated policy of reducing exposure when turbulence is high, the ranking must run from most turbulent first to least turbulent fifth. The table does not explicitly spell out that ordering. Ordinary ascending quintile ranks would reverse the intended policy. This is a necessary interpretation to declare, not an innocuous coding convention. The rule is an ordinal step function, not literally exposure proportional to $1/d_t$.

The source’s endnote lists historical G–10 countries including Belgium, France, Germany, Italy, and the Netherlands alongside other currencies. It does not explain how the currency universe and euro transition are handled. It also does not clearly specify the moment-estimation window for the underlying daily turbulence calculation; the trailing three years are explicitly the ranking window. These should not be silently conflated.

Table 6 gives the following filtered performance:

| Statistic | Unfiltered | Turbulence | VIX | Five-year swap spread | TED spread | Yield spread |
|---|---:|---:|---:|---:|---:|---:|
| Annual return, percent | 2.81 | 3.02 | 1.98 | 2.67 | 2.21 | 2.10 |
| Annual volatility, percent | 5.55 | 3.29 | 3.95 | 4.04 | 3.51 | 3.07 |
| Reported information ratio | 0.51 | 0.92 | 0.50 | 0.66 | 0.63 | 0.68 |
| Skewness | −0.48 | −0.15 | −0.26 | −0.25 | −0.31 | −0.56 |

The swap spread is U.S.-dollar based relative to a comparable Treasury; the yield spread is ten-year minus two-year Treasury yield. The information ratios numerically resemble return divided by volatility. The article does not supply a separate tracking-error benchmark or financing adjustment that would justify substituting another definition.

The turbulence filter combines a slightly higher reported return with substantially lower volatility and less negative skewness. The comparison is not at equal average exposure or equal realized volatility, and no trading-cost deduction is documented. Figure 5 identifies the carry sample as January 1993–December 2008; Table 6 does not independently label its full estimation and evaluation dates. A replication needs the exact return series, start-up period for the rolling windows, daily exposure update convention, treatment of the unused capital, currency weights, and forward-roll costs.

## Reproduction priorities and practical limits

The central statistic is readily reconstructible; the complete reported performance is not, because data and several implementation conventions are missing or inconsistent. A source-faithful reproduction should keep four modules separate: retrospective event classification, the 1977–2006 risk calibration, randomized portfolio tests, and the daily lagged carry filter. Their thresholds, dates, frequencies, and information sets are different.

For a new implementable experiment, reference moments and score thresholds should be estimated only with information available before the exposure decision, and validation should respect chronology. Testing alternative regularization, turnover costs, rank direction, and the 70% versus 75% threshold would assess robustness. These are proposed replication controls, not tests reported in the paper.

The economic takeaway is conditional risk awareness: an asset’s average covariance contribution can differ sharply from its behavior during unusual joint moves. The evidence supports examining those conditional relationships and their persistence. It does not establish that a large turbulence score is inherently a loss forecast, that crisis timing is predictable, or that the reported carry improvement survives every reasonable implementation choice.

# Tail Risk Reduction Strategies

**Lerby M. Ergun and Philip A. Stork (2013).** Chapter 28 in *Rethinking Valuation and Pricing Models*, pp. 457–470. DOI: 10.1016/B978-0-12-415875-7.00028-2. Source: [TailRiskReduction_ErgunStork_2013.pdf](../../Finance/TailRiskReduction_ErgunStork_2013.pdf). This is an empirical research chapter, not a textbook-wide summary. Printed chapter pages are used below.

## Why this matters

A timing rule can reduce ordinary volatility yet leave investors exposed to abrupt crashes. This chapter evaluates a moving-average rule using extreme-value estimates of the *left tail*, alongside return, drawdown, and market-exposure statistics. Its contribution is the combination of a simple monthly timing rule with heavy-tail risk measurement across several assets. It neither invents moving-average investing nor identifies the economic cause of the reported timing advantage.

The reported historical result is substantial tail-loss reduction with roughly preserved compounded returns. The result is gross of trading frictions, and exact replication is limited by conflicting signal captions, an unspecified tail-estimation threshold, and incomplete data identifiers. Those limitations matter more than adding another interpretation of the rule's profitability.

## Data and strategy: the reproducible core

Section 28.2 describes daily CRSP data for a **value-weighted S&P 500 index**, July 1, 1926–December 31, 2010. It also examines a January 2, 1973–December 31, 2010 subsample. The chapter does not provide a CRSP series identifier or explain the construction of the early historical index. Table 28.1 instead calls the series equally weighted, while the figure calls it value weighted. These descriptions cannot all determine a unique input series; the main data-section description is the primary interpretation, with the weighting discrepancy retained as unresolved.

Additional daily Datastream total-return series cover the UK, Germany, Hong Kong, gold, REITs, and 10-year bonds, January 2, 1990–December 31, 2010. Exact index codes, the REIT and bond market, return currency, currency hedging, and international holiday alignment are not reported. The cash return comes from the one-month US Treasury-bill series on Kenneth French's data library. The conversion of that series to daily accruals is not specified.

Buy-and-hold stays fully invested in the relevant asset. The timing rule, as stated in the main text on p. 460, is fully invested when the **one-month moving average exceeds the ten-month moving average**, and otherwise holds short-term Treasury instruments. Decisions occur only on the last trading day of a calendar month. The authors emphasize actual calendar months rather than substituting 20 and 200 trading days.

For implementation, denote the two averages available at month-end $m$ by $M_{1,m}$ and $M_{10,m}$. The main-text interpretation is

$$
s_m=\mathbf{1}\{M_{1,m}>M_{10,m}\}.
$$

Given a specified execution lag, the subsequent daily strategy return is

$$
r^{T}_t=s_m r^{A}_t+(1-s_m)r^{f}_t,
$$

where $r^A_t$ is the asset return and $r^f_t$ is the cash return during the holding month. The lag must prevent the signal from earning a return already used to compute it. The chapter does not explicitly distinguish execution at the signal close from the next tradable price, specify equality handling, or say whether calendar-month averages use all daily levels or sampled monthly closes. These are implementation choices to disclose, not facts to fill in silently.

There is a serious source inconsistency: Figure 28.1 and the table captions repeatedly say to invest when the **long** average exceeds the short average, reversing the main-text rule. The results are discussed as trend following that exits prolonged bear markets, which supports the main-text direction, but no code is provided to resolve the contradiction conclusively. A faithful replication should implement the stated trend-following direction and report the reverse direction as a separate specification check.

There is no short position or leverage in the described rule. Switching moves the full allocation between the risky asset and cash. Taxes, commissions, and slippage are ignored. The authors expect modest costs for liquid S&P instruments, but provide no turnover counts, bid–ask costs, futures-roll conventions, ETF history, or cost-adjusted results. This is not evidence that costs are negligible in every asset or historical period.

## Tail model and estimation

To make the signs unambiguous, let $X=-r$ denote a positive loss. The chapter assumes a regularly varying right tail for losses:

$$
P(X>x)=A x^{-\alpha}\{1+B x^{-\beta}+o(x^{-\beta})\},
$$

with leading scale $A>0$ and tail exponent $\alpha>0$. The second-order terms describe approximation error; the reported quantile calculations keep only $A x^{-\alpha}$. A larger $\alpha$ means a thinner asymptotic loss tail. This is an assumption about sufficiently extreme losses, not a claim that the entire return distribution is Pareto.

The tail exponent is estimated with the Hill estimator. The source names the estimator but does not print its sample formula. A conventional reconstruction, ordering positive losses as $X_{(1)}\geq\cdots\geq X_{(n)}$, is

$$
\widehat\alpha^{-1}=\frac{1}{k}\sum_{i=1}^{k}\log\frac{X_{(i)}}{X_{(k+1)}}.
$$

Here $k$ is the number of exceedances, and $u=X_{(k+1)}$ is a threshold convention. The chapter uses notation $x_k$ for its threshold. Small order-statistic indexing differences must be resolved in code. In either convention, the leading-tail calibration is $\widehat A=(k/n)u^{\widehat\alpha}$.

For a loss exceedance probability $p$, the resulting approximation is

$$
\widehat{\operatorname{VaR}}_p=u\left(\frac{k}{np}\right)^{1/\widehat\alpha},\qquad
\widehat{\operatorname{ES}}_p=\frac{\widehat\alpha}{\widehat\alpha-1}\widehat{\operatorname{VaR}}_p.
$$

The second expression requires $\widehat\alpha>1$ for finite expected shortfall under the Pareto approximation. ES is an expected **loss** conditional on exceeding the loss threshold, not a guaranteed maximum loss. The chapter reports $p=2.5\%,1\%,0.5\%$, corresponding to confidence levels 97.5%, 99%, and 99.5%.

Crucially, the chapter does not disclose $k$, threshold-selection diagnostics, estimated exponents, uncertainty intervals, a bias correction, or treatment of serial dependence. Therefore its exact EVT numbers cannot be reproduced from the stated data and equations alone. Larger $k$ reduces sampling noise while potentially including observations outside the tail regime; smaller $k$ increases variance. In a timing strategy, clustering of exposure states and volatility further complicates nominal independent-observation inference. These are limitations of the evidence, not extra procedures claimed to have been performed by the authors.

## Main S&P results and units

Table 28.1 reports annualized compounded holding-period returns alongside **daily** volatility and daily tail-loss measures. Percentages below are in those respective units.

| Metric | 1926–2010 buy-and-hold | 1926–2010 timing | 1973–2010 buy-and-hold | 1973–2010 timing |
|---|---:|---:|---:|---:|
| Annualized holding-period return | 9.62 | 9.55 | 10.44 | 11.01 |
| Daily standard deviation | 1.07 | 0.77 | 1.06 | 0.76 |
| Daily skewness | −0.13 | −1.24 | −0.57 | −1.57 |
| Daily kurtosis | 19.92 | 38.93 | 18.91 | 38.68 |
| Reported Sharpe statistic | 3.54 | 6.39 | 4.02 | 7.62 |
| Maximum relative drawdown | 83.74 | 51.06 | 55.59 | 32.12 |
| Worst annual return | −43.18 | −20.63 | −38.63 | −13.11 |
| Daily VaR, 1% tail | 2.94 | 2.04 | 2.79 | 2.01 |
| Daily ES, 1% tail | 5.11 | 3.35 | 4.37 | 2.89 |
| Daily VaR, 0.5% tail | 3.95 | 2.67 | 3.59 | 2.48 |
| Daily ES, 0.5% tail | 6.86 | 4.39 | 5.61 | 3.57 |

The full-sample return difference is −0.07 percentage point annually; the later-period difference is +0.57 point. Full-sample daily volatility falls about 28%, measured relative to buy-and-hold. The text's 39% figure uses timing volatility as the denominator: buy-and-hold is 39% more volatile. These two comparisons are not interchangeable. The later-period volatility reduction is similarly about 28%, rather than 40% when expressed relative to buy-and-hold.

The 1% ES reduction is about 34% in both periods. At the 0.5% tail it is about 36% over the full sample. Nevertheless, timing retains a reported 51.06% maximum relative drawdown over the long sample. This is risk reduction, not downside insurance.

The authors' “Sharpe ratio” is the daily mean return divided by daily standard deviation **without subtracting the risk-free rate**. The table appears to scale this daily ratio by 100: values such as 3.54 should not be interpreted as a conventional annualized excess-return Sharpe of 3.54. Reproduction should report the stated statistic and a separately labeled conventional Sharpe, rather than conflate them.

The source distinguishes “absolute” and “relative” maximum drawdown, reporting 55.59% versus 21.25% for the former in both S&P periods. It gives only a verbal distinction between absolute-level differences and relative differences, without a complete normalization formula. The relative drawdown is the more interpretable reported comparison, but exact reconstruction of the nonstandard absolute measure remains unresolved.

Timing's more negative skewness and larger kurtosis are important qualifications to the claim that every measure of risk improves. Lower absolute tail losses can coexist with a more asymmetric and more peaked standardized distribution, including cash observations and occasional risky-asset shocks. The source does not estimate a mixture model to establish that explanation. Figure 28.1's caption describes a normalized natural logarithm, whereas the displayed axis is an index level reaching several thousand; the chart should not be used to infer exact log-wealth differences.

## Market exposure and conditional tails

Table 28.2 estimates monthly OLS regressions

$$
r^{T}_t-r^f_t=a+b(r^{BH}_t-r^f_t)+\varepsilon_t.
$$

For 1926–2010, reported monthly alpha is 0.0023 with a rounded $p$-value of 0.01, and beta is 0.4864. For 1973–2010, alpha is 0.0022 with table $p=0.06$, and beta is 0.5792. Multiplying the monthly alphas by 12 gives approximately 2.76% and 2.64% annually; this is an arithmetic annualization, not an independently estimated annual return. The prose calls the latter significance level 7%, differing from the table's 6%. The first table row also says 1925–2010 despite the stated July 1926 start.

Conditional betas split paired observations according to whether buy-and-hold returns are below or above their sample mean $\mu_{BH}$:

$$
b_-=\frac{\operatorname{Cov}(r^T,r^{BH}\mid r^{BH}<\mu_{BH})}{\operatorname{Var}(r^{BH}\mid r^{BH}<\mu_{BH})},\qquad
b_+=\frac{\operatorname{Cov}(r^T,r^{BH}\mid r^{BH}\geq\mu_{BH})}{\operatorname{Var}(r^{BH}\mid r^{BH}\geq\mu_{BH})}.
$$

Downside/upside betas are 0.4391/0.2391 for the long sample and 0.5059/0.4413 for the later sample. Timing loses considerable upside participation as well as reducing downside participation. These conditional regressions are descriptive; they are not coefficients of a complete nonlinear pricing model or proof of exploitable alpha after costs.

The “extreme beta” columns are different objects. The caption describes empirical copula counts of strategy-tail observations conditional on benchmark-tail observations, using 1% quantiles. A natural reconstruction is the joint-tail count divided by the number of benchmark-tail observations. This measures finite-threshold tail co-occurrence, not a regression slope and not automatically the asymptotic tail-dependence coefficient. The chapter does not fully specify observation frequency, rank/tie handling, or inference for these counts. Reported extreme downside/upside values are 0.4480/0.3122 for the long sample and 0.3298/0.2553 for the later sample.

No heteroskedasticity/autocorrelation adjustment, multiple-testing correction, or independent holdout is described for these comparisons. Rounded $p=0.00$ values mean below the display precision, not probabilities literally equal to zero.

## Moving-average sensitivity

Table 28.3 keeps the short average at one calendar month and changes the long average to 250, 200, 150, 100, or 50 trading days. Rebalancing remains monthly. This is a sensitivity exercise that deliberately differs from the main ten-calendar-month implementation.

| Long average | Annualized return, % | Daily volatility, % | Daily 1% ES, % | Relative drawdown, % | Monthly alpha | Beta |
|---|---:|---:|---:|---:|---:|---:|
| 250 days | 9.78 | 0.77 | 3.38 | 51.06 | 0.0025 | 0.4924 |
| 200 days | 8.98 | 0.76 | 3.30 | 55.65 | 0.0020 | 0.4727 |
| 150 days | 8.86 | 0.75 | 3.27 | 55.88 | 0.0020 | 0.4610 |
| 100 days | 8.56 | 0.74 | 3.26 | 62.24 | 0.0017 | 0.4686 |
| 50 days | 7.65 | 0.75 | 3.48 | 51.78 | 0.0007 | 0.5110 |

Buy-and-hold in this table returns 9.60%, with volatility 1.07%, 1% ES 5.12%, and relative drawdown 83.74%. The small difference from Table 28.1's 9.62% is not reconciled in the chapter. Returns decline as the long average becomes shorter, while daily volatility and EVT losses vary much less. Relative drawdown is **not monotone**: the 50-day value improves from the 100-day value. Thus the prose's broad statement that shorter windows increase drawdowns should not be interpreted as a universal ordering of every reported drawdown statistic. The authors report significant positive alphas at 5% except for the 50-day rule, but this table does not display their individual $p$-values.

## Other markets, 1990–2010

Tables 28.4 and its continuation report the following gross results. Return is annualized; ES is a daily percentage loss.

| Market | Return BH / timing, % | Volatility BH / timing, % | 0.5% ES BH / timing, % | Monthly alpha | Beta |
|---|---|---|---|---:|---:|
| UK | 9.24 / 8.39 | 1.14 / 0.75 | 6.24 / 3.85 | 0.0012 | 0.5438 |
| Germany | 8.11 / 10.85 | 1.44 / 0.92 | 7.43 / 4.46 | 0.0039 | 0.4907 |
| Hong Kong | 14.33 / 17.55 | 1.57 / 1.15 | 8.52 / 6.21 | 0.0062 | 0.5420 |
| 10-year bonds | 7.41 / 7.51 | 0.36 / 0.32 | 1.60 / 1.51 | 0.0004 | 0.8847 |
| REIT | 15.08 / 17.05 | 1.63 / 0.80 | 19.99 / 4.98 | 0.0066 | 0.4137 |
| Gold | 6.76 / 7.66 | 0.96 / 0.79 | 5.85 / 4.58 | 0.0016 | 0.6196 |

The strongest reported relative tail improvement is REIT ES, down about 75%; the bond improvement is only about 6%. Thus “risk reduction” is not a common magnitude across assets. UK timing gives up 0.85 percentage point of annualized return; Hong Kong gains 3.22 points. The source's six-of-seven return statement includes the S&P comparison in addition to these six markets.

Relative drawdowns fall from 72.68% to 31.30% for Germany, 63.80% to 45.28% for Hong Kong, and 74.58% to 23.53% for REITs. Even favorable examples can retain economically large losses. The other-market alpha table lacks $p$-values; the text states that some alphas are significant and others are not, so uniformly significant abnormal performance is unsupported.

## Replication boundary and interpretation

A reconstruction should first freeze the index identities and currency convention, implement both documented signal directions without look-ahead, distinguish calendar months from fixed trading-day windows, and state the cash-accrual and execution rules. It should then retain the daily return series for tail fitting and aggregate consistently to monthly observations for CAPM. The Hill threshold, estimated exponent, sample size, and tail diagnostics must be published for each strategy; these inputs are absent from the original.

That workflow clarifies the existing evidence rather than reproducing unavailable details by assertion. A new study would also need turnover and realistic costs, uncertainty on differences, chronological out-of-sample testing, and benchmarks with comparable average risky exposure or volatility. The chapter does not perform those extensions. Comparing a partly cash-invested rule to fully invested buy-and-hold mixes timing skill with reduced market exposure; low beta and lower loss magnitudes are therefore not by themselves proof of superior forecasting.

The authors explicitly leave the economic mechanism unresolved. Behavioral extrapolation, feedback trading, stop orders, margin constraints, and derivative hedging are possible explanations discussed in the literature, not separately identified causes in this sample. The supported takeaway is narrower: in the reported historical samples, a monthly moving-average switch produced lower absolute daily tail-loss estimates and lower drawdowns, often with similar or higher gross compounded returns. It did not eliminate crash exposure, prove cost-adjusted alpha, or establish that a particular future tail probability is known accurately.

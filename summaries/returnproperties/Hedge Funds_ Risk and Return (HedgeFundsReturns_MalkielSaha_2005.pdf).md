# Hedge Funds: Risk and Return

**Burton G. Malkiel and Atanu Saha. Financial Analysts Journal 61(6), November–December 2005, pp. 80–88.**

**Source:** [HedgeFundsReturns_MalkielSaha_2005.pdf](../../Finance/HedgeFundsReturns_MalkielSaha_2005.pdf), all nine pages, eight tables, endnotes, and references. Page pointers below use printed journal pages.

## Why this matters

A hedge-fund return database records both investment outcomes and managers' decisions about when to report those outcomes. A historical index assembled from currently reporting funds, with their retrospectively supplied histories, therefore need not describe an investor's attainable experience. Malkiel and Saha make this selection problem visible by separating contemporaneous from backfilled returns and continuing reporters from funds that disappear.

Their main contribution is a database audit combined with a manager-selection risk analysis. Removing backfilled observations and retaining discontinued reporters materially reduces average measured performance. The paper then shows why a low volatility for an aggregate hedge-fund series does not imply low risk for an investor choosing a particular manager: cross-sectional return dispersion and reporting attrition are substantial, while winner persistence is unstable.

This is not an estimated trading model or a structural explanation of hedge-fund alpha. It does not show that every fund lacks skill, nor that hedge funds have no diversification benefit. It shows that conclusions about average performance and persistence depend critically on database construction. The most useful implementation lessons are to preserve reporting timestamps, include discontinued reporters, distinguish different measures of selection bias, and avoid equating disappearance from a vendor with observed liquidation.

## Data universe and reporting-time design

The primary source is TASS, including both its live database and its graveyard records. The authors describe TASS as covering approximately one-third to one-half of the hedge-fund population. Coverage broadened after Tremont bought TASS in March 1999 and encouraged funds reporting elsewhere to join. Strategies are self-classified by managers. The data therefore cover many styles, but membership remains voluntary and is not a random sample of all hedge funds.

The relevant status cutoff is **April 2004**. A live fund continues to report at that point. A defunct fund has stopped reporting, whether because it closed or because it remained economically active but chose not to supply data. The source uses “defunct” for both cases. Any reconstructed outcome should retain that definition rather than relabel all stopped reporters as bankrupt.

The study uses several overlapping windows. Backfill comparisons cover 1994–2003; survivor comparisons, persistence, and cross-sectional dispersion principally cover 1996–2003; Table 1 descriptive moments cover 1995–2003. The authors exclude 1994–1995 from survivor comparisons because almost all recorded returns in those years are backfilled. The windows cannot be interchanged when reconciling their average returns.

TASS provides a date at which a manager began reporting. A return dated before that entry date is classified as backfilled; an observation supplied while the fund reports is contemporaneous. Backfill includes both incubation histories and selective historical submissions by funds that may previously have reported to another vendor. An exact replication needs the original entry-date field and its vintage. A current database with revised records may not reconstruct what TASS contained in April 2004.

The authors also fill missing months in partial calendar years with the contemporaneous average return of all reporting hedge funds (endnote 6, p. 88). For example, a fund observed only from March through December receives the cross-fund average in January and February. A natural compounding implementation is

$$
R_{iy}=\prod_{m=1}^{12}(1+\widetilde r_{iym})-1,
\qquad
\widetilde r_{iym}=\begin{cases}r_{iym},&\text{observed},\\ \bar r_{ym},&\text{missing partial-year month}.\end{cases}
$$

This formula reconstructs the stated procedure; the article does not provide code specifying all intermediate filters or the exact membership of the monthly imputation average. It is especially important to distinguish this imputation from a return actually earned by an investor before a fund existed or after it stopped reporting. Benchmark filling can attenuate extreme early or terminal outcomes.

Table 3 explicitly equal-weights funds. Asset-weighting is avoided because assets are missing for some funds, and the authors find that funds not reporting assets tend to underperform. Restricting an asset-weighted analysis to funds with available assets would introduce another selection condition. The mutual-fund comparison comes from Lipper's general-equity universe, with live status measured at December 2003; this status date differs from TASS's April 2004 cutoff.

## Backfill: distinguish a group gap from an index bias

For year $y$, let $B_y$ and $C_y$ be the sets of backfilled and contemporaneous annual observations. The direct comparison is

$$
D_y^{BF}=\bar R_{B,y}-\bar R_{C,y}.
$$

Table 2 reports annual means, medians, counts, and significance tests for this difference. The arithmetic average of the ten annual backfilled means is **14.65%**, versus **7.34%** for contemporaneous means, a gap of **7.31 percentage points**. Corresponding geometric averages of the annual series are **14.35%** and **6.81%**. The arithmetic averages of annual medians are **11.69%** and **5.95%**, a **5.74-point** gap. These are distinct statistics, not interchangeable estimates of a single average fund's internal rate of return.

Selected annual comparisons show the changing composition:

| Year | Backfilled mean | Backfilled count | Contemporaneous mean | Contemporaneous count | Reported mean gap |
|---|---:|---:|---:|---:|---:|
| 1994 | 0.42% | 1,076 | −11.53% | 22 | 11.96 points |
| 1996 | 19.44% | 1,299 | 12.37% | 331 | 7.08 points |
| 1998 | 9.62% | 1,352 | −2.04% | 751 | 11.65 points |
| 2000 | 14.69% | 1,463 | 2.08% | 1,030 | 12.62 points |
| 2003 | 19.49% | 936 | 17.20% | 2,065 | 2.29 points |

Small differences between subtraction of displayed rounded entries and the reported gaps reflect rounding. The 1994 contemporaneous sample is extremely small, making a simple equal-weight average across calendar years sensitive to an atypical early year. Only from 2002 onward do contemporaneous counts exceed backfilled counts in this table.

The reported mean-difference tests reject at 5% in all years except 1999 and 2003. Median-difference tests reject in all years except 2003. The signs of the printed $t$ statistics are negative although the displayed gap is backfilled minus contemporaneous; a reproduction should match the direction of the underlying test contrast rather than infer a negative economic gap from that sign.

The **7.31-point group gap is not the amount by which every full database index is overstated**. With common weighting and groups partitioning a given year's universe,

$$
\bar R_{all,y}-\bar R_{C,y}=w_{B,y}D_y^{BF},
$$

where $w_{B,y}$ is the backfilled fraction. Time-varying weights and alternative index construction alter this relationship. The two groups can also differ in age, strategy, and entry conditions. Thus the comparison documents economically large selection, but does not causally isolate the reporting decision while holding all fund characteristics fixed.

## Survivorship and the size of the omitted group

After excluding backfilled returns, the authors compare funds that will still report in April 2004 with those that will not. In notation,

$$
D_y^{LD}=\bar R_{live,y}-\bar R_{defunct,y},
\qquad
D_y^{surv}=\bar R_{live,y}-\bar R_{all,y}.
$$

The second is the relevant difference between a survivor-only equal-weight series and the contemporaneous full reporting universe. These two quantities should never be confused.

For 1996–2003, Table 3 reports arithmetic average annual returns of **13.74% for live funds**, **5.39% for defunct funds**, and **9.32% for all funds**. The live–defunct gap is **8.35 percentage points**, while the survivor-only overstatement relative to all funds is **4.42 points**, or **442 basis points per year**. Geometric averages are **13.31%, 4.91%, and 8.91%**, respectively. All eight annual live–defunct mean comparisons are significant at 5%.

The difference is particularly large in 2000: live funds return **9.39%**, defunct funds **−4.94%**, and all funds **2.08%**. The live–defunct gap is **14.33 points**, while the live–all gap is **7.32 points**. In 2003, the live–all gap is only **0.78 points**, partly because most funds observed near the cutoff are still in the live group. Fixed-endpoint survival classification mechanically allows longer exposure to attrition for earlier cohorts.

Among the 331 contemporaneous reporters represented in 1996, 58 are classified live at the 2004 cutoff. The paper says fewer than one-quarter remain; the displayed counts imply about **17.5%**. This is survival in the reporting dataset, not a direct estimate of investor capital lost or a liquidation probability over an invariant horizon.

The mutual-fund comparison gives an arithmetic live-only mean of **9.73%** and all-fund mean **8.49%** over 1996–2003, with a reported survivor gap of **1.23 points**. Rounding gives 1.24 from the displayed means. Hedge-fund survivor selection is much larger in this experiment, but the universes, status dates, and reporting obligations differ.

The authors attribute their larger estimates relative to some earlier papers to TASS's fuller graveyard coverage, use of contemporaneous data, a later sample, larger coverage, and deliberate collection of discontinued reporters. These are plausible explanations, not separately identified causal decompositions. In particular, the backfill and survival estimates concern related selection processes and cannot simply be added to subtract a fixed universal bias from an arbitrary index.

## Distributional risk and a printed kurtosis inconsistency

Table 1 excludes backfill and includes both live and defunct funds. The hedge-fund universe has annual mean **8.82%**, annual standard deviation **9.21%**, and annual Sharpe ratio **0.50**, compared with **12.38%, 21.69%, and 0.38** for the S&P 500. The T-bill annual mean is **4.20%**. The Sharpe calculation uses annual excess return divided by annual return standard deviation; for the universe, $(8.82-4.20)/9.21\approx0.50$.

The table separately gives monthly mean and standard deviation, **0.70% and 1.99%** for the universe. Annual and monthly statistics should be reproduced from their own aggregation rather than imposing a square-root-of-twelve identity on these historical summaries. The paper does not fully document every category-level averaging convention needed to reconcile all annual and monthly entries.

Several styles have substantial negative skew and large kurtosis. Event-driven returns have skewness **−1.50**, kurtosis **10.61**, and Jarque–Bera statistic **301.00**; fixed-income arbitrage has **−2.03**, **9.16**, and **244.98**. Global macro has skewness **0.09**, kurtosis **3.00**, and statistic **0.14**; managed futures has **0.09**, **2.87**, and **0.23**. At the reported 5% critical value of 5.99, the latter two categories do not reject normality, whereas the other displayed strategy categories do.

Endnote 5 defines the usual statistic

$$
JB=n\left[\frac{S^2}{6}+\frac{(K-3)^2}{24}\right],
$$

with $K$ raw kurtosis. There is a material table-label inconsistency: the strategy rows appear to report raw kurtosis, but the final aggregate/benchmark rows behave like **excess kurtosis**. For instance, the S&P 500 row prints $S=-0.64$, $K=0.28$, and $JB=7.69$. For 108 monthly observations, treating 0.28 as excess kurtosis yields approximately 7.73, consistent up to rounding; treating it as raw kurtosis yields a much larger value. The T-bill entry of **−0.80** cannot be raw kurtosis at all. The universe's printed 2.51 likewise yields roughly its reported 29.36 only when interpreted as excess kurtosis. This is a diagnostic reconstruction, not an explicit correction supplied by the authors. A replication should compute and label both raw and excess kurtosis to avoid propagating the ambiguity.

The normality rejection is not a complete tail-risk model. The paper does not estimate a conditional loss distribution, expected shortfall, liquidity-adjusted risk, or exposures to crash insurance. Its conclusion is narrower: variance and a Sharpe ratio do not exhaust the distributional features relevant to allocation.

## Persistence experiment and its changing selection rule

Each year, a winner earns more than the cross-sectional median hedge-fund return and a loser earns less. The experiment takes prior-year winners and asks what fraction remain winners in the next year. This is a rank-persistence design, not a factor-adjusted alpha sort, and it uses annual horizons.

Table 5 presents two treatments of disappearance. Panel A counts funds that stop reporting as losers. Panel B excludes dropped funds. Medians are independently recomputed for each panel's universe, so the winner-to-winner counts can change as well as the denominators. One cannot reproduce Panel B by merely deleting dropped losers from Panel A's original table.

With dropped funds counted as losers, the unweighted average of annual repeat-winner rates is **51.56%**. Annual values include **61.11% in 1996**, **42.03% in 1999**, **43.11% in 2000**, **61.41% in 2002**, and **39.59% in 2003**. The corresponding signed test statistics include **0.9, −3.0, −2.8, 5.1, and −5.8**. Persistence varies in sign rather than giving a stable selection rule.

Excluding dropped funds raises the average repeat-winner rate to **54.74%**. Nevertheless, the rate is only **43.96% in 2000** and **43.95% in 2003**, versus **65.63% in 2002**. Event-driven funds show the greatest category persistence in the source's untabulated breakdown, about **57%** repeating.

For a year's $n$ prior winners and $w$ repeat winners, the displayed signed values are consistent with the conventional binomial-normal calculation

$$
Z=\frac{w-n/2}{\sqrt{n/4}}.
$$

This is an implementation reconstruction. The table's note confusingly calls the reference a chi-squared distribution of 50%; a signed $Z$ statistic and a Bernoulli null probability of one-half are the coherent interpretation. Moreover, the displayed average $Z$ is not a valid pooled test obtained merely by averaging yearly test statistics. Serial dependence in fund performance and common strategy exposures also complicate independent Bernoulli inference. The defensible result is unstable historical rank persistence, not a proof that the exact probability of repeat success is one-half for every manager.

## Cross-sectional dispersion and reporting attrition

Table 6 calculates the cross-sectional standard deviation of monthly fund returns within each category, then averages those monthly standard deviations within years and across years. These are **monthly cross-sectional spreads**, not annual time-series volatilities. Over 1996–2003 the hedge-fund universe average is **5.56%**, versus **3.34%** for mutual funds. Emerging markets average **6.65%**, managed futures **6.36%**, long–short equity **5.88%**, and convertible arbitrage **2.08%**.

An aggregate index diversifies this dispersion mechanically. An allocator holding one or a few managers does not automatically obtain that diversification, particularly if managers share exposures or if access and minimum investments prevent broad allocation. The paper measures dispersion, not an optimal number of managers or a transaction-cost-adjusted fund-of-funds solution.

Table 7 defines annual attrition using funds exiting the reporting set relative to existing contemporaneous reporters. Hedge-fund rates include **20.24% in 1996**, **18.24% in 1998**, **20.49% in 2000**, and **14.29% in 2003**. Corresponding mutual-fund rates are **3.85%, 5.21%, 7.67%, and 8.22%**. The differences are significant in each reported year. The 1995 hedge-fund rate of 26.92% is based on only 52 contemporaneous funds and should not be treated as a precise estimate for the entire industry.

## Probit model of disappearance

The final experiment models a binary indicator $D_i$ equal to one for a defunct reporter and zero for a live reporter. A faithful functional-form reconstruction is

$$
P(D_i=1\mid x_i)=\Phi(x_i'\beta),
$$

estimated by the Bernoulli probit log likelihood. Inputs are four quarterly returns preceding the end of observed performance, standard deviation over the final twelve months, a peer-underperformance count, and fund assets. For a defunct fund, the endpoint precedes its reporting cessation; for surviving funds, it is the end of available performance. This is an endpoint classification exercise, not a documented rolling real-time hazard backtest.

The peer measure counts the final three months in which the fund's return falls below the monthly median of funds in its primary category. Assets are measured in **billions of dollars** in the final month; when missing, the first available value within the final four months is used. The source does not fully state the search ordering for that fallback or all missing-value exclusions.

Table 8 coefficients and reported standard errors are:

| Regressor | Coefficient | Standard error | $Z$ |
|---|---:|---:|---:|
| Most recent quarter, Q1 | −1.47 | 0.36 | −4.06 |
| Q2 | −4.93 | 0.32 | −15.54 |
| Q3 | −2.74 | 0.33 | −8.42 |
| Q4 | −3.71 | 0.35 | −10.72 |
| Final twelve-month standard deviation | 17.76 | 0.92 | 19.32 |
| Peer-underperformance count | 0.00 | 0.03 | −0.17 |
| Assets, billions | −1.30 | 0.17 | −7.76 |
| Constant | −0.37 | 0.07 | −5.49 |

Poor absolute recent performance, higher volatility, and smaller assets are associated with disappearance. Relative peer performance is not statistically distinguishable from zero conditional on these inputs. Probit coefficients are latent-index coefficients, not percentage-point probability effects; the marginal effect of a continuous regressor is $\phi(x_i'\beta)\beta_k$. The paper does not supply average marginal effects, a predictive validation sample, an ROC curve, the estimation sample count, or sufficient details to establish a calibrated default-probability model. Return scaling and standard-deviation frequency must also be matched before using the printed coefficients; they should not be inserted blindly into percentage-unit data.

## Reproduction limits and investment interpretation

The central reproducibility requirements are a historical TASS extract with entry dates and graveyard records, monthly return histories, contemporaneous strategy labels, asset observations, and the Lipper comparison universe. Preserve original status definitions, distinct sample windows, partial-year imputation, equal weighting, and separately recalculated persistence medians. Then reconcile annual counts before interpreting differences in average returns.

Important unmeasured biases remain. Funds that never report are absent. Funds may stop reporting before their worst terminal losses, creating an end-of-life bias that the authors cannot quantify. Stale or managed prices can understate beta and distort alpha. A graveyard improves measurement without recovering every missing final payoff, redemption delay, or gate.

The high-water-mark discussion provides an incentive mechanism for closure: after a large loss, a manager may be unable to earn further incentive fees until recovering the previous peak and may prefer opening a new fund. The paper does not separately estimate this mechanism in the probit. Similarly, its assertion that large successful funds are less likely to disappear is an average association, not evidence that no successful fund ever stops reporting for commercial reasons.

For a quantitative allocator, the result is to treat reporting history as part of the data-generating process. A database-cleaning decision can change measured annual performance by several percentage points, comparable to an attractive manager alpha. At the same time, manager selection introduces a dispersion and attrition problem that is not captured by the volatility of a diversified hedge-fund index. These findings justify an audit of coverage and terminal outcomes before optimizing an allocation; they do not themselves supply an investable manager-selection rule.

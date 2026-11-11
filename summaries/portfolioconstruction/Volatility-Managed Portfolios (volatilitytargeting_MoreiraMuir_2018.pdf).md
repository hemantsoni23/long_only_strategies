# Volatility-Managed Portfolios

**Alan Moreira and Tyler Muir.** *The Journal of Finance* 72(4), August 2017, pp. 1611–1644. DOI: 10.1111/jofi.12513. The library filename contains 2018, but the supplied PDF is the 2017 published article.

**Source:** [volatilitytargeting_MoreiraMuir_2018.pdf](../../Finance/volatilitytargeting_MoreiraMuir_2018.pdf). This note also uses the authors’ 21-page *Internet Appendix*, dated March 5, 2017, retrieved through [Tyler Muir’s research page](https://tylersmuir.com/) and its [appendix link](https://www.dropbox.com/scl/fi/y0iyrbfajedhfw82fc7da/JF_20160273_IA_MoreiraMuir.pdf?rlkey=ytiwy82cclbodixh7cmtis4cc&dl=0). Main-text page references use journal pagination; appendix references use its own pages.

## Why this matters

A volatility forecast can be economically valuable even without an expected-return forecast. If variance rises sharply while the expected excess return rises little, the reward per unit of variance falls. An investor who holds a fixed exposure then allocates disproportionately much risk to comparatively unattractive periods. This paper makes that argument testable using a particularly simple rule: scale next month’s factor return by the inverse of last month’s realized variance.

The contribution is broader than a smoother equity return series. The authors apply the same construction to several systematic factors, to static combinations of factors, and to currencies; examine recessions, leverage, costs, and longer holding periods; and connect the strategy’s unconditional alpha to variation in the price of risk. The resulting alpha is evidence against a proportional conditional risk–return relation. It does not, by itself, establish an exploitable mispricing relative to every possible conditional asset-pricing model.

Three distinctions are essential for replication. The rule uses **inverse variance**, not inverse standard deviation. Its scaling constant and static tangency portfolios use full-sample information, even though its monthly timing signal is lagged. Finally, a positive alpha relative to one original factor establishes an expanded investment opportunity set; it does not mathematically guarantee that the managed asset’s standalone Sharpe ratio exceeds the original asset’s Sharpe ratio.

## Data, returns, and the monthly trading rule

Section I uses daily observations to estimate monthly variance and monthly observations to evaluate strategy returns. The equity factor series come from Kenneth French, Hou–Xue–Zhang, and Frazzini–Pedersen; currency returns come from Lustig–Roussanov–Verdelhan, supplied by Adrien Verdelhan. The currency carry factor is the high-minus-low interest-rate or forward-discount portfolio. Daily exchange-rate changes of the high and low portfolios provide its volatility information; its investment return is the monthly carry factor, not simply the exchange-rate change.

The principal Table I samples are:

| Factors | Calendar coverage | Regression observations |
|---|---|---:|
| Market, SMB, HML | 1926–2015 | 1,065 each |
| Momentum | 1926–2015 | 1,060 |
| RMW, CMA | 1963–2015 | 621 each |
| ROE, IA | 1967–2015 | 575 each |
| Currency carry | 1983–2015 | 360 |
| Betting against beta | 1929–2012 | 996 |

These are the source’s table-specific counts, not an instruction to impose one common sample across every experiment. Later tables sometimes have slightly different counts because of available predictors or lag requirements. A reproducer should preserve the factor definitions and vintage, record missing dates, and match each table’s sample independently. The article does not provide a complete data-cleaning script or a vintage-locked list of all downloaded files.

Let $f_{t+1}$ be the excess return of a factor over month $t+1$. Define $v_t$ as month $t$’s realized variance, formed by summing squared demeaned daily factor returns:

$$
v_t=\sum_{d\in t}(f_d-\bar f_t)^2,
\qquad
\bar f_t=\frac{1}{n_t}\sum_{d\in t}f_d.
$$

Equation (2), p. 1616, writes a stylized 22-trading-day month. The important convention is a **sum** of daily squared deviations, producing a monthly variance measure; it is not the usual daily sample variance divided by $n_t-1$. The source does not spell out all calendar edge cases. An implementation should document how actual trading-day counts replace the displayed 22-day notation.

The strategy is

$$
w_t=\frac{c}{v_t},
\qquad
f_{t+1}^{\sigma}=w_t f_{t+1}.
$$

All of month $t$’s daily observations enter the signal, which determines exposure for month $t+1$. There is no contemporaneous scaling by the variance of the return being evaluated. The original factor is an excess-return investment, so the corresponding total return adds the risk-free return to $f_{t+1}^{\sigma}$; cash is not an additional alpha source.

For the main comparisons, $c$ is chosen to match the managed and original portfolios’ unconditional standard deviations over the sample. In implementable notation,

$$
c=\frac{\operatorname{sd}(f_{t+1})}
{\operatorname{sd}(f_{t+1}/v_t)}.
$$

A positive constant does not change a gross Sharpe ratio or the t-statistic on a proportionately rescaled alpha. It does change reported exposure, dollar P&L, alpha units, turnover, leverage, and the interaction with a cap. Consequently, the normalization makes the relative performance comparison transparent but is not a complete real-time capital-allocation prescription. A live replication needs an ex ante target or a training-period estimate of $c$.

The mean–variance motivation is $w_t^*=E_t[f_{t+1}]/(\gamma\operatorname{Var}_t[f_{t+1}])$. Replacing the conditional mean by a constant and the future variance by last month’s realized variance yields the rule. The paper is therefore exploiting predictable variation in the denominator rather than claiming to have identified the exact optimal portfolio under arbitrary preferences or return dynamics.

## Performance tests and their units

The basic spanning regression is

$$
f_{t+1}^{\sigma}=\alpha+\beta f_{t+1}+\varepsilon_{t+1}.
$$

The beta is an unconditional regression coefficient, not the average mechanical weight $E[w_t]$. A volatility-timed strategy puts larger weights on observations with smaller conditional second moments, so those quantities generally differ. Table I also includes the three Fama–French factors as controls. Standard errors adjust for heteroskedasticity; the caption does not specify a serial-correlation correction, a particular HC variant, or small-sample adjustment.

Table I expresses monthly returns as annual percentage rates by multiplying observations by 12. Thus an alpha of 4.86 means 4.86 percentage points per year. Its RMSE is also multiplied by 12, rather than annualized by $\sqrt{12}$. To obtain an annualized appraisal ratio from those table entries, use

$$
AR_{\mathrm{ann}}=\sqrt{12}\frac{\alpha_{\mathrm{table}}}{RMSE_{\mathrm{table}}}.
$$

For the market this is approximately $\sqrt{12}(4.86/51.39)=0.328$. Reading 51.39 as an annual residual volatility would produce the wrong result. Momentum’s analogous calculation is about 0.86 using rounded entries.

| Managed factor | Alpha, annual % | Heteroskedasticity-robust SE | Beta on original factor |
|---|---:|---:|---:|
| Market | 4.86 | 1.56 | 0.61 |
| SMB | −0.58 | 0.91 | 0.62 |
| HML | 1.97 | 1.02 | 0.57 |
| Momentum | 12.51 | 1.71 | 0.47 |
| RMW | 2.44 | 0.83 | 0.62 |
| CMA | 0.38 | 0.67 | 0.68 |
| Currency carry | 2.78 | 1.49 | 0.71 |
| ROE | 5.48 | 0.97 | 0.63 |
| IA | 1.55 | 0.67 | 0.68 |
| BAB | 5.67 | 0.98 | 0.57 |

The results are heterogeneous. SMB provides no positive-alpha evidence, and CMA’s estimate is small relative to its uncertainty. Momentum, profitability, ROE, and BAB show substantially stronger evidence than those two factors. The market result is economically sizable but should not be relabeled a universal anomaly independent of the benchmark.

The appendix makes this qualification especially clear. With market, SMB, HML, and momentum controls, managed-market alpha is 2.43% with SE 1.60% (Table IA. IV). With the six Fama–French–Carhart factors in the shorter 1963–2015 sample, it is only 0.18% with SE 1.87% (Table IA. V). In that six-factor regression, managed HML, momentum, and RMW retain alphas of 4.16%, 12.91%, and 3.21%, respectively. Both the benchmark and sample change; the disappearance of market alpha cannot be assigned solely to one added factor without a matched-sample comparison.

## Static factor combinations and the investment opportunity set

To ask whether timing helps an investor who already holds several factors, the authors construct a static mean–variance-efficient combination with weights proportional to $\widehat\Sigma^{-1}\widehat\mu$. Those relative factor weights remain fixed. They then time the **variance of the combined portfolio**, rather than independently changing the relative weights of all constituent factors.

Table II reports the following annualized Sharpe ratios:

| Static opportunity set | Static portfolio | Its volatility-managed version | Appraisal ratio |
|---|---:|---:|---:|
| Market | 0.42 | 0.51 | 0.33 |
| FF3 | 0.52 | 0.69 | 0.50 |
| FF3 plus momentum | 0.98 | 1.09 | 0.69 |
| FF5 | 1.19 | 1.20 | 0.56 |
| FF5 plus momentum | 1.34 | 1.42 | 0.77 |
| Hou–Xue–Zhang | 1.57 | 1.69 | 0.91 |
| Hou–Xue–Zhang plus momentum | 1.57 | 1.73 | 0.91 |

These static tangency weights are estimated over the full sample. The very high multifactor Sharpe ratios are therefore descriptions of an in-sample opportunity set, not out-of-sample forecasts of attainable performance from estimated factor means.

An orthogonal residual with nonzero alpha can improve the attainable frontier even when the standalone managed Sharpe ratio improves little. In the unconstrained mean–variance spanning calculation,

$$
SR_{\mathrm{expanded}}^2=SR_{\mathrm{original\ frontier}}^2+AR^2.
$$

The source’s large utility improvements refer to mean–variance utility after choosing exposures within the expanded opportunity set. With quadratic utility, the optimal risky-investment contribution is proportional to $SR^2/(2\gamma)$. A 65% increase in that contribution is not a 65% return, nor a 65% increase in total wealth or lifetime consumption utility.

The strategy also differs from conventional risk parity. Risk parity changes cross-sectional relative weights using risk estimates; this experiment times the overall scale of a static tangency portfolio. The authors examine inverse-volatility weighting based on three-year estimates as a control and argue that the two mechanisms are complementary.

## Costs, leverage, and implementation alternatives

Table IV applies proportional trading costs to the market timing strategy. The turnover statistic is average absolute monthly weight change, $E|w_t-w_{t-1}|$. It is not a round-trip measure divided by two. With a one-way cost $k$ in return units, the direct annual mean-return deduction is approximately $12kE|\Delta w_t|$. The reported alpha is recomputed after costs, and need not fall by precisely that amount because the regression beta may also change.

| Rule | Mean absolute monthly weight change | Gross alpha %/year | Alpha after 10 bp | Alpha after 14 bp | Break-even one-way cost |
|---|---:|---:|---:|---:|---:|
| Inverse realized variance | 0.73 | 4.86 | 3.98 | 3.63 | 56 bp |
| Inverse realized volatility | 0.38 | 3.85 | 3.39 | 3.21 | 84 bp |
| Inverse expected variance | 0.37 | 3.30 | 2.86 | 2.68 | 74 bp |
| Exposure capped at 1 | 0.16 | 2.12 | 1.93 | 1.85 | 110 bp |
| Exposure capped at 1.5 | 0.16 | 3.10 | 2.91 | 2.83 | 161 bp |

The expected-variance row is described here as an AR(1) forecast of log variance. The appendix’s broader expected-variance experiment uses **three** lags of log realized variance; it is a separate specification. Its Table IA. II reports market alpha 3.85% with SE 1.36%, and momentum alpha 12.54% with SE 1.67%. The forecast estimation window, recursive versus full-sample fitting, and log-to-level retransformation are not fully specified. A constant retransformation factor cancels under an unconstrained reestimated $c$, but can matter for capped exposures and a fixed capital target.

There is an unresolved source inconsistency: Table V assigns gross alphas 3.30% and 3.85% to inverse realized volatility and expected variance, respectively—the reverse of Table IV. Table IV’s own cost rows are reported above without silently exchanging their labels. The appendix’s three-lag expected-variance result does not by itself prove which main-table row is correct because its forecasting model differs. Exact reconciliation requires the underlying code.

The baseline median exposure is 0.93; the 75th, 90th, and 99th percentiles are 1.59, 2.64, and 6.39. This is a substantial quiet-period leverage tail. Inverse volatility reduces the corresponding upper percentiles to 1.61, 2.08, and 3.36, although its median is 1.23. A cap is therefore a substantive implementation change, not an innocuous display convention.

The 1 bp trading-cost assumption represents a liquid implementation; 10 bp is motivated by institutional estimates at about 1% of daily volume, while 14 bp incorporates an additional high-volatility cost allowance. These calculations do not constitute an endogenous market-impact model, a funding-spread model, or a test of liquidity during a margin call. The paper explicitly does not provide equivalent transaction-cost estimates for every long–short factor.

An options experiment, April 1986–January 2012, replaces required market leverage with an equal-weight combination of six in-the-money S&P 500 calls: maturities 60 and 90 days crossed with moneyness 90%, 92.5%, and 95%. The call portfolio’s beta is approximately seven, so its allocation is adjusted to supply the required market beta. Another version combines calls with short puts at matching moneyness. Table V reports Sharpe ratios 0.39 for buy-and-hold, 0.59 for direct volatility timing, 0.54 using calls, and 0.60 using calls plus puts. The corresponding timing alphas are 4.03%, 5.90%, and 6.67%, with SEs 1.81%, 3.01%, and 2.86%. These are empirical approximations using a particular option dataset, not an assertion that option leverage is costless or that short-put financing removes crash risk.

## Recessions, international evidence, and alternative performance measures

The recession test interacts factor returns with a recession indicator in the spanning regression. For the market, the expansion beta is 0.83 and the recession interaction is −0.51, implying recession beta approximately 0.32. The latter is a reduction in exposure, not a negative recession beta. This matters economically: the measured reward is not explained by a simple story in which the strategy deliberately takes more market risk during recessions. It does not exclude every state-dependent risk premium or every unobserved crisis exposure.

The appendix adds credit and term premia using monthly Asvanunt–Richardson series from 1926–2014. Because daily data are unavailable, variance is estimated from the preceding 18 monthly returns. Credit is corporate-bond exposure duration-matched against government bonds; term is long-minus-short government maturity exposure. Table IA. I reports credit alpha 1.48% with SE 0.40%, and term alpha 1.25% with SE 0.86%, both with 1,050 observations. The evidence for credit is stronger; the term result is not conventionally statistically significant.

The international exercise covers 20 OECD stock indices from Global Financial Data, converted to US dollars and evaluated over the US risk-free rate. Managed Sharpe ratios exceed original Sharpe ratios in 80% of the countries, with an average difference of 0.15. Many series lack dividends. Figure IA. 1 is therefore a comparison of these particular index return series, not a fully harmonized total-return international investability test; precise country-specific sample starts are not tabulated there.

The appendix also computes a manipulation-proof performance measure based on power utility with risk aversion three. It reports 2.48% for the market and 4.33% for the managed market, a difference of 1.85 percentage points annually. In a calibrated simulation with a constant price of risk, lognormal volatility, and conditionally lognormal returns, the managed measure exceeds the market measure only 0.2% of the time. This probability belongs to that null simulation, not a model-free bootstrap confidence level for future performance. The source does not supply all simulation settings needed for a bit-for-bit reproduction.

Risk checks include lower measured downside beta, controls for BAB, return-density plots, and the strategy’s behavior through the Great Depression and financial crisis. The appendix reports market downside beta 0.11, not significantly different from zero. Kernel densities use an Epanechnikov kernel with panel-specific bandwidths. Their absence of an obvious heavy left tail is informative sample evidence; it cannot rule out rare crashes after unusually quiet periods, precisely when inverse-variance leverage is large.

## Dynamics and holding horizon

A monthly VAR combines log realized variance, market returns, and Shiller’s CAPE. Variance is ordered first for shock identification, allowing a variance innovation to affect the other variables contemporaneously. The discussion says one lag, whereas Figure 5’s caption says two lags. This is a second explicit replication ambiguity: both specifications should be retained in a sensitivity check rather than guessing that one is the definitive published implementation.

The plotted response to a one-standard-deviation variance shock has a rapid increase and subsequent decline in variance, a much smaller immediate increase in expected return, and an initially roughly 50% reduction in the optimal mean–variance exposure. Exposure recovers as the variance shock dissipates, approximately over the subsequent year. The figure includes bootstrapped 95% confidence bands, but the number of bootstrap draws and all resampling details are not given in the main text.

A separate horizon experiment forms a position using initial inverse variance and holds it over nonoverlapping multi-month periods. The timing alpha generally weakens as the holding period lengthens, consistent with variance’s mean reversion. The market’s alpha remains statistically significant at the 10% level to about 18 months in the reported experiment. This is not an optimal long-horizon consumption–portfolio solution; it changes the evaluation and holding interval of a particular managed trade.

## What the alpha identifies theoretically

Section III obtains a clean expression in continuous time. Write the original excess-return increment as

$$
dR_t^e=\mu_t\,dt+\sqrt{v_t}\,dB_t,
\qquad
dR_t^{e,\sigma}=\frac{c}{v_t}dR_t^e.
$$

With finite required moments, $v_t>0$, and infinitesimal regression coefficients defined using quadratic covariation,

$$
\beta=\frac{c}{E[v_t]},
\qquad
\alpha=cE\!\left[\frac{\mu_t}{v_t}\right]
-\frac{cE[\mu_t]}{E[v_t]}
=-\frac{c}{E[v_t]}\operatorname{Cov}\!\left(\frac{\mu_t}{v_t},v_t\right).
$$

Conditional-mean covariance terms are order $dt^2$, which is why this is an instantaneous relation; it is not an exact identity obtained by mechanically replacing $dt$ with a month.

If $\mu_t=\gamma v_t$, timing alpha is zero. If expected returns are constant or mean-independent of variance, define

$$
J_v=E[v_t]E[v_t^{-1}]-1\ge0.
$$

Then $\alpha=cE[\mu_t]J_v/E[v_t]$. Nonconstant variance makes $J_v$ positive, assuming the inverse moment exists. Greater dispersion in variance can then create a larger timing opportunity without requiring an accurate forecast of the numerator.

More generally, the appendix writes $\mu_t=bv_t+\zeta_t$ with $E[\zeta_t\mid v_t]=E[\zeta_t]$. Setting $\gamma^u=E[\mu_t]/E[v_t]$ gives

$$
\alpha=cJ_v(\gamma^u-b),
\qquad
b=\gamma^u-\frac{\alpha}{cJ_v}.
$$

Thus alpha compares the conditional risk–return slope to the unconditional ratio. It is possible for expected returns to rise with variance and still generate positive timing alpha, provided that increase is insufficient relative to the unconditional trade-off.

For aggregate pricing implications, stronger spanning assumptions are required. Suppose systematic factors span the relevant conditional and unconditional mean–variance frontiers and, initially, their conditional covariance matrix is diagonal with entries $v_{i,t}$. The variance-information price of factor risk is

$$
\gamma_{i,t}^{v}=\gamma_i^u+
\frac{\alpha_i}{c_iJ_i}
\left(\frac{E[v_{i,t}]}{v_{i,t}}-1\right).
$$

This follows by substituting the alpha-identified slope into $b_i+E[\zeta_i]/v_{i,t}$. An SDF with diffusion exposure $\gamma_t^v$ prices factor strategies based on the volatility information under the stated spanning and integrability assumptions. The appendix explicitly uses mean independence of $\zeta$ from volatility; a main-text expression that leaves $\zeta_t$ unchanged inside its conditional expectation should not be read as the needed restriction. Some displayed covariance entries in the appendix omit variance squares. Using $v$ throughout avoids mixing variance with standard deviation in the reconstruction.

The theoretical interpretation is not justified merely by applying the rule to any individual stock. The appendix constructs an example with changing idiosyncratic variance in which timing a positive-beta stock can have alpha relative to that same stock while the CAPM remains valid. The aggregate conclusions require systematic factors and their spanning assumptions.

## Pricing distance and equilibrium-model experiments

The pricing interpretation is quantified using the variance of the difference between alternative SDF innovations, a Hansen–Jagannathan-style measure of potential pricing errors. In the single-factor construction, adding variance information moves the SDF by

$$
D^{u-v}=\left(\frac{\alpha}{c}\right)^2\frac{E[v_t]}{J_v}.
$$

The market calibration identifies this distance with approximately $0.33^2=0.11$, the squared appraisal ratio. The source combines it with an expected-return-predictability input of 0.06 to estimate a total distance of about 0.29. It assigns about 38% of that total to volatility information alone and 21% to expected-return information alone; their interaction accounts for much of the remainder. These are illustrative, model-dependent pricing-distance calculations. They are not fractions of realized market-return variance, and the expected-return component is imported from earlier predictability evidence rather than independently estimated as a new forecasting model here. The fuller decomposition also depends on assumptions about the residual expected-return component and its interaction with variance.

Section IV compares the observed timing alpha with simulations from Campbell–Cochrane habit formation, Bansal–Kiku–Yaron long-run risk, Wachter time-varying disasters, and He–Krishnamurthy intermediary models. Parameters come from the original calibrations. Each artificial history is subjected to the same inverse-variance construction, spanning regression, and conventional regression of future returns on lagged variance.

Figure 7 specifies 1,000 simulations of 100-year samples, while the surrounding text says samples of the same length as the roughly 90-year historical record. That discrepancy should be resolved before an exact simulation replication. Time discretization, seeds, initial-state treatment, and full model implementation are not supplied in this article. The main finding is a contrast in diagnostic power: these models frequently produce a weak estimated conventional risk–return slope, yet rarely match the observed managed alpha. The long-run-risk model matches the reported alpha in only about 0.2% of simulations; the others do worse. This challenges those calibrations and mechanisms, not all possible equilibrium explanations of volatility timing.

## Replication boundaries and takeaways

A faithful reproduction should preserve the monthly information lag, distinguish variance from volatility, match sample dates by table, keep excess returns separate from total returns, and maintain the table’s annualization conventions. It should estimate every reported regression on the actual aligned observations, compute static factor combinations separately from time-varying scale, and distinguish unconstrained ex post normalization from capped or funded implementation.

The main unresolved implementation inputs are calendar edge cases, data vintages, exact robust-SE conventions, forecasting estimation windows, the Table IV/V row inconsistency, and the VAR lag inconsistency. The appendix materially improves coverage but does not provide complete execution code, financing assumptions, or a modern market-impact model. Numerical results in this note are reported source estimates, not independently rerun backtests.

The strongest conclusion is that substantial forecastable variance variation is not matched by a proportional expected-return increase in these samples. That creates useful timing information, particularly for momentum and several profitability-related factors. The practical inference is to evaluate risk scaling as an additional portfolio decision, while testing funding, caps, parameter estimation, and broader factor benchmarks explicitly. A good volatility forecast and a positive single-factor alpha are insufficient on their own to establish a deployable, universally superior strategy.

# Expected Option Returns

Joshua D. Coval and Tyler Shumway. *The Journal of Finance* 56(3), June 2001, pp. 983–1009.

Source: [OptionReturns_Coval_2001.pdf](../../Finance/OptionReturns_Coval_2001.pdf). The supplied file includes a JSTOR cover and reference-link pages. Journal page 983 is PDF page 2; journal page numbers are used below. The full article, appendix material, and tables were inspected.

## Why this matters

Option pricing and option expected returns answer different questions. A formula can fit option prices while assigning the wrong compensation to risks that appear in option portfolios. Coval and Shumway ask whether observed returns are consistent first with weak asset-pricing restrictions and then with the much stronger Black–Scholes/CAPM combination. Their contribution is a return-based test that neutralizes the underlying market exposure and asks what risk premium remains.

The headline evidence is a large negative average return to buying approximately market-neutral index straddles. The result suggests that investors pay for a risk exposure associated with volatility, beyond ordinary stock-market beta. The paper also examines crash-neutral constructions, transaction-cost-inclusive selling strategies, other underlying markets, and the loading of equity portfolios on an option-return factor. These extensions distinguish a useful asset-pricing rejection from an immediately implementable claim of riskless option-selling profit.

There are two levels of inference. Simple restrictions on calls and puts broadly agree with the data. The stronger claim that a zero-beta option portfolio should earn only the risk-free rate does not. A negative straddle mean by itself neither proves mispricing nor uniquely identifies stochastic volatility: unmodeled tail exposure, state-dependent discounting, beta error, and quote problems are possible explanations, several of which the paper investigates.

## Weak pricing restrictions and their exact scope

Let $m>0$ be a stochastic discount factor over the option holding horizon. A payoff $X$ has price $E[mX]$, and its expected gross return is $E[X]/E[mX]$. The paper assumes that the underlying and discount factor are negatively related in the relevant conditional regions. This is stronger than knowing only that their unconditional covariance is negative.

For a European call at strike $K$, write $C(K)=E[m(S_T-K)^+]$. Its expected gross return is

$$
E[R_c(K)]=\frac{E[(S_T-K)^+]}{C(K)}.
$$

Differentiating with respect to strike, ignoring atoms at the strike or treating one-sided derivatives carefully, gives

$$
\frac{dE[R_c(K)]}{dK}
=-\frac{P(S_T>K)^2}{C(K)^2}\operatorname{Cov}(S_T-K,m\mid S_T>K).
$$

Thus the expected return rises with strike when the conditional covariance is negative. A call with zero strike is the underlying itself; increasing strike adds leverage to exposure that performs well when marginal valuation is low. The analogous put derivative is

$$
\frac{dE[R_p(K)]}{dK}
=\frac{P(S_T<K)^2}{P(K)^2}\operatorname{Cov}(K-S_T,m\mid S_T<K),
$$

which is positive under the corresponding condition. Put expected returns approach the risk-free return as strike becomes sufficiently large, so they lie below it in the relevant ordering. This does not require every put to have a negative net expected return. Similarly, positivity of a call's net expected return uses the baseline underlying-return assumptions, not covariance alone in an arbitrary negative-rate economy.

The propositions in Section I are attractive because they do not require a lognormal return distribution or a constant variance. They concern expected returns under a specified pricing-kernel relationship. Finite-sample means need not be strictly monotone, and a missing local monotonicity in one strike bin is not itself a decisive rejection without uncertainty estimates and the exact conditional assumptions.

## The stronger benchmark: beta-neutral straddles

Under Black–Scholes redundancy and the CAPM, an option's instantaneous market beta is its elasticity to the underlying multiplied by the underlying's beta. With underlying beta one,

$$
\beta_c=\frac{S\Delta_c}{C},\qquad \beta_p=\frac{S\Delta_p}{P}.
$$

The printed call-beta equation uses $\Delta_c=\Phi(d_1)$ while its $d_1$ includes a dividend yield. In a continuous-dividend Black–Scholes implementation the consistent delta is $e^{-q\tau}\Phi(d_1)$, where

$$
d_1=\frac{\log(S/K)+(r-q+\sigma^2/2)\tau}{\sigma\sqrt\tau}.
$$

This dividend adjustment should be specified rather than silently mixing conventions. The paper also uses put–call parity to relate the betas. With fixed cash dividends, the underlying asset net of their present value and the discounted strike must be treated consistently. A displayed rearrangement near equation (16) gives the bond term the wrong sign; the correct decomposition subtracts the riskless strike obligation. The beta relation survives because that bond term has zero market beta.

Given contemporaneous option values and estimated betas, the fraction of invested option value allocated to the call is

$$
\theta=-\frac{\beta_p}{\beta_c-\beta_p},\qquad
r_v=\theta r_c+(1-\theta)r_p.
$$

The construction uses dollar weights, not equal numbers of call and put contracts. For ordinary call and put deltas the weights are positive. The beta-neutrality is model based and local in time. A weekly or daily holding period is not continuous rebalancing, and nonlinear return exposure can remain over finite intervals. This motivates the paper's separate discrete-time stochastic-discount-factor test.

Volatility is proxied by the contemporaneous VIX available in the sample, then based on S&P 100 options, for both S&P 100 and S&P 500 calculations. It is not the later S&P 500 VIX methodology. The dividend input is an average annual yield derived from dividends realized during the option's life. Using future realized dividends can introduce information unavailable at formation; a strictly real-time replication should run a separately labeled version with an ex ante dividend estimate. The rate source and all yield-conversion details are not completely specified.

## Data, contract selection, and timing

Section II uses the Berkeley Options Database of CBOE quotes. The primary price is the midpoint of the first bid and ask after 9:00 a.m. Central time, paired with an early underlying index observation. Contracts expire in the following calendar month and have approximately 20–50 days remaining. Strikes are grouped into five bins defined by $K-S$: $[-15,-10)$, $[-10,-5)$, $[-5,0)$, $[0,5)$, and $[5,10)$. Selection uses the previous closing index level. These are absolute index-point bins, not constant moneyness percentages.

The S&P 500 options are European-style. The main weekly sample runs January 1990 through October 1995 and contains 305 observations. Weekly returns are normally Tuesday to Tuesday; the paper describes Wednesday substitutions for particular Tuesday holidays. Earlier contracts were less liquid, and November–December 1995 are excluded from this analysis because of missing out-of-the-money call quotes.

The S&P 100 options are American-style and are examined daily beginning in January 1986. The tables report 2,519 daily observations. The manuscript's date descriptions are not entirely consistent: October and December 1995 appear in different places, while separate monthly exercises explicitly use either 118 or 120 months. A reproduction should retain each table's stated window and verify the actual database dates rather than imposing one common endpoint. American exercise also means European parity and delta formulas are approximations for this sample, especially around dividends and deep in-the-money contracts.

The authors remove observations violating basic arbitrage conditions and deal with outliers, but do not give every numerical filter threshold. They report that assigning a return of −100% to contracts with a missing subsequent price does not materially change their conclusions. That is a sensitivity check, not evidence that missing observations are random. The asynchronous-quote robustness test later restricts the call–put timing gap to no more than 15 minutes.

All reported option holding-period returns should be implemented as simple net returns, $(V_{t+h}-V_t)/V_t$, with the specified investment weights. Log returns would be undefined for total losses and would not aggregate according to the portfolio formula. Weekly and daily results must not be mixed, and option values, dividend conventions, time-to-expiration fractions, and rate frequencies must use consistent units.

## Raw option results: what the weak restrictions explain

Tables I–II report the following means across the five strike bins in their stated order. Numbers are percentages per holding period, not annual rates.

| Sample and instrument | Bin 1 | Bin 2 | Bin 3 | Bin 4 | Bin 5 |
|---|---:|---:|---:|---:|---:|
| S&P 500 calls, weekly | 1.48 | 1.19 | 1.85 | 2.00 | 4.13 |
| S&P 500 puts, weekly | −14.56 | −12.78 | −9.50 | −7.71 | −6.16 |
| S&P 100 calls, daily | 0.62 | 0.55 | 0.67 | 0.80 | 0.85 |
| S&P 100 puts, daily | −2.30 | −2.02 | −1.79 | −1.42 | −1.22 |

The call means are positive and generally increase with strike, but the S&P 500 call mean t-statistics range only from 0.53 to 0.85. These are highly noisy means. Put losses are much more precisely estimated: the S&P 500 t-statistics are −4.22, −3.95, −3.05, −2.81, and −2.54. The pattern is economically consistent with expensive downside insurance and leverage differences; it is not yet a rejection of rational pricing.

Model call betas are very large: the S&P 500 estimates range from 21.14 in the first bin to 55.72 in the fifth. The corresponding put betas are −36.85, −37.53, −35.23, −31.11, and −26.53. The first two are not strictly monotone, despite a broad monotonicity description in the text. These betas explain why a large raw option return cannot be compared directly with the underlying's much smaller mean without adjustment.

The weekly S&P 500 index mean is about 0.181%, with minimum −5.39% and maximum 6.05%. The S&P 100 daily mean is about 0.04%, and its extreme daily return reaches −21.21% during the crash period. The difference in extreme realized states is important when comparing pre- and post-crash evidence and when considering whether a five-year post-1990 sample adequately reveals tail risks.

## The central result and beta sensitivity

Table III reports strongly negative beta-neutral straddle means:

| Sample | Bin 1 | Bin 2 | Bin 3 | Bin 4 | Bin 5 |
|---|---:|---:|---:|---:|---:|
| S&P 500 weekly mean, % | −4.49 | −4.28 | −3.15 | −3.15 | −2.89 |
| t-statistic | −5.44 | −4.75 | −2.89 | −2.72 | −2.38 |
| S&P 100 daily mean, % | −0.57 | −0.50 | −0.50 | −0.48 | −0.65 |
| t-statistic | −3.01 | −2.51 | −2.76 | −2.84 | −3.84 |

S&P 500 weekly medians are even lower, roughly −7.2% to −8.3%, and the maximum gains exceed 100% in every bin. The return distribution is strongly asymmetric: many losses to a long-volatility investor are offset occasionally by large gains. A negative average does not make the opposite position safe.

The paper varies the call-beta input by ±10% when forming the portfolios. All five S&P 500 means remain negative: approximately −2.49% to −3.23% under the 0.9 multiplier and −2.85% to −4.30% under the 1.1 multiplier. The S&P 100 results also remain negative. An alternative in-sample beta-neutral construction yields daily means from −0.32% to −0.51%, although not every bin remains individually significant at conventional levels. This establishes some robustness to modest beta mismeasurement; it cannot exhaust all state dependence or finite-horizon nonlinear exposure.

Restricting the call–put quote gap to 15 minutes produces S&P 100 daily means from −0.44% to −0.58%. Splitting the sample is more revealing. In 1986–1990, means are roughly −0.14% to −0.56% and are mostly imprecise. In 1991–1995, all five are around −0.69% to −0.86% and more strongly significant. The apparent premium varies with the period; the paper does not establish a stable daily rate that can simply be compounded indefinitely.

## A finite-horizon SDF test

To address the mismatch between instantaneous beta reasoning and discrete holding periods, the authors fit a one-parameter power pricing kernel. In a convenient normalized form,

$$
m_{t+1}=e^{-r_h}\frac{R_{m,t+1}^{-\gamma}}{E[R_{m,t+1}^{-\gamma}]},
$$

where $R_m$ is the market's gross holding-period return and $r_h$ is the corresponding continuously compounded risk-free return. Normalization prices the risk-free payoff. GMM then requires both the market and one straddle portfolio to satisfy $E[mR]=1$. There are two asset moments and one fitted parameter, giving a one-degree-of-freedom overidentification test under the reported setup.

Table IV's fitted $\gamma$ values are 5.41, 0.55, 5.68, −0.09, and −6.68 across the five portfolios. Their variability and economically awkward negative values reinforce the mismatch between a single market factor and the option returns. The J-statistics are 12.36, 12.38, 7.90, 5.39, and 3.91, with reported p-values 0.0004, 0.0004, 0.0049, 0.0202, and 0.0478. Every original straddle specification is rejected at 5%.

The authors repeat the test after removing the mean component of the straddle return. Rejections disappear: the reported J-statistics are 0.09, 0.45, 0.13, 0.04, and 0.10. This points to the mean premium rather than merely the shape of the centered return variation as a source of failure. One printed pairing is internally inconsistent: a one-degree-of-freedom J-statistic of 0.45 does not have the table's p-value 0.8314. It remains far from rejection, so the qualitative conclusion is unchanged. A reproduction should recompute p-values from the statistic rather than copy this entry.

The exact covariance estimator, bandwidth or lag selection, numerical optimizer, and all moment-normalization implementation details are not fully supplied. Those must be documented in new code. The exercise tests a particular market-return kernel; it does not test all admissible stochastic discount factors or identify a unique preference model.

## Removing a terminal crash exposure

Section III constructs a long call plus a put spread: buy a put at the call strike and sell an equal number of lower-strike puts. The lower strike must be at least 85% of the index level and is chosen from available contracts; its average is about 89%. The put spread stops increasing in payoff once the underlying falls below its lower strike. The dollar weight between the call and the put spread is chosen to offset estimated beta.

If $Q=P_1-P_2$, its beta is

$$
\beta_Q=\frac{S(\Delta_{p_1}-\Delta_{p_2})}{P_1-P_2},\qquad
\theta_Q=-\frac{\beta_Q}{\beta_c-\beta_Q}.
$$

The resulting portfolio buys the call with fraction $\theta_Q$ and the put spread with the rest. In the January 3, 1995 example, the index is 458.14, the high strike is 465, and the low strike is 400. A nominal 100-unit investment buys about 8.32 calls and 6.26 high-strike puts while selling 6.26 low-strike puts. The terminal crash payoff is capped near 400 units.

Table V reports a mean of −3.24% per week for the S&P 500 construction, t = −2.15, and −1.02% per day for the S&P 100 version, t = −4.09. This supports the argument that simple exposure to ever-larger terminal crash payouts is not the entire explanation of the original straddle means. It does not eliminate all disaster risk, volatility repricing before maturity, jump dependence in the hedge weights, or market illiquidity.

There is also a serious reproducibility qualification. The table reports minimum returns of −210.41% and −236.10%. Such losses do not fit a simple fully funded, nonnegative-payoff European long-call/long-put-spread position valued at arbitrage-free prices. Asynchronous quotes, approximate beta weights, American exercise conventions, or portfolio normalization may matter, but the paper does not resolve the discrepancy. These minima must be retained as reported findings and investigated, rather than silently interpreted as ordinary bounded-loss portfolio returns. Around October 1987, missing quotes additionally force the authors to use first transactions at different times, including 9:50 and 10:53 on the two crash-related days. Those observations deserve separate auditing.

## The transaction-cost selling exercise is a different strategy

The paper then evaluates selling a call and put at the money, buying an out-of-the-money put, and investing the premium with the remaining wealth in the underlying index. Trades use bid prices for sold options and ask prices for the protective put. Positions are initiated after the monthly expiration and held to the next expiration. This is an equal-contract, monthly strategy, not the same beta-neutral daily or weekly long-straddle test.

Table VI uses 118 months, January 1986–October 1995. Allocation is expressed as option premium relative to wealth. The results are:

| Premium allocation | Mean monthly return, % | Monthly SD, % | Worst month, % | Reported Sharpe ×100 |
|---|---:|---:|---:|---:|
| 0% | 0.99 | 3.99 | −21.53 | 14.47 |
| 5% | 1.94 | 5.48 | −27.22 | 27.91 |
| 10% | 2.89 | 8.04 | −35.00 | 30.82 |
| 15% | 3.84 | 10.96 | −47.45 | 31.29 |
| 20% | 4.79 | 14.01 | −59.90 | 31.27 |

These Sharpe numbers are monthly ratios multiplied by 100, consistent with subtracting roughly a monthly share of the assumed 5% annual risk-free rate. They are not annualized Sharpe ratios of 14 or 31. The reported test for a beneficial nonzero option allocation gives F = 8.76 and p = 0.0037. The worst month deteriorates markedly as premium exposure rises, making the tradeoff visible even in this favorable mean-return sample.

Premium allocation is not a margin budget or a maximum-loss limit. Bid–ask crossing is included, but the analysis does not establish feasibility under a complete brokerage-margin, collateral, financing, early-assignment, commission, tax, and position-capacity model. Midpoint return evidence and this bid/ask strategy should therefore be kept separate. The experiment suggests compensation for bearing an unpleasant exposure; it does not demonstrate a scalable arbitrage.

## Other markets and an equity volatility factor

The cross-market extension uses daily closing observations from Bridge/CRB on front-month options, generally October 1988–August 1999, with Nikkei coverage beginning September 1994. Implied volatility is estimated from at-the-money calls and puts rather than using equity VIX for every asset. The portfolios neutralize beta to their own underlying, which is different from neutralizing beta to the stock market.

Reported daily means are −0.69% for Treasury-bond options (t = −5.04, 1,783 observations), −0.33% for Eurodollar options (t = −1.68, 2,580), −0.29% for Nikkei options (t = −0.57, 1,075), and +0.01% for Deutsche-mark options (t = 0.03, 2,687). Their correlations with changes in VIX are approximately +0.12, −0.12, +0.08, and −0.16. The Treasury result supports broader insurance pricing, but the other estimates are not all statistically persuasive. The Eurodollar sign pattern especially cautions against explaining every premium with one common equity-volatility shock.

Table VIII asks whether the option return behaves like a priced equity factor. The authors construct a daily approximately at-the-money straddle return by interpolating adjacent strikes, cumulate it monthly, and regress ten CRSP NYSE/AMEX size-portfolio excess returns on both the value-weighted market and the straddle factor. The stated sample is 120 months, January 1986–December 1995. The exact interpolation and all inference implementation choices are not fully described.

The regression is

$$
r_{i,t}-r_{f,t}=\alpha_i+\beta_{im}(r_{m,t}-r_{f,t})+\beta_{iv}(r_{v,t}-r_{f,t})+\varepsilon_{i,t}.
$$

Volatility-factor loadings range from −0.0328 for the smallest stocks, t = −2.08, to +0.0059 for the largest, t = 4.81. Intermediate portfolios generally have progressively less negative loadings. The scale is tied to the large percentage fluctuations of the option portfolio, so the small coefficient magnitudes do not imply economically negligible covariance. Market betas are about 0.84–1.00, and adjusted R-squared values range roughly 0.33–0.99.

The joint-alpha GRS statistic is 2.31 with p = 0.0168. Thus the augmented factor specification is still rejected as a complete pricing model for these portfolios. The paper establishes an informative covariance pattern and a plausible volatility-risk interpretation, not a finished explanation of the cross-section of stock returns.

## Reimplementation sequence and limits of the inference

A reproducible implementation should first rebuild the contract-level panel, preserve quote timestamps, identify exercise style, and reconcile the sample endpoints for each table. It should next compute simple option returns and raw strike-bin moments before estimating any beta-neutral portfolio. Failure to match these primitives makes a later matching straddle mean hard to interpret.

The next layer is a fully specified option-beta calculation, including dividends, rate interpolation, maturity convention, and the original VIX definition. Dollar weights should be stored at formation, with both theoretical and realized regression betas reported. The ±10% and synchronization tests should be rerun without quietly changing the universe. Crash-neutral portfolios require contract-count and financing reconciliation, especially for observations below −100%. GMM should document its moments, normalization, weighting matrix, and p-value calculation. Finally, the monthly selling experiment and factor regressions should be implemented as separate designs with their own samples and transaction conventions.

The most defensible conclusion is that the sample contains a negative expected return to exposures that approximate buying index volatility while neutralizing linear index risk, inconsistent with the simple Black–Scholes/CAPM benchmark. The contribution lies in making option returns an asset-pricing diagnostic. It does not establish that all volatility premia are identical, that selling them has negligible drawdown risk, or that the observed mean can be forecast out of sample without a model of the underlying state and compensation for tail risk.

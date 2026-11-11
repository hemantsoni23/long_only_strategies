# Do Hedge Funds Hedge?

**Clifford Asness, Robert Krail and John Liew. May 2001 working-paper draft; first draft December 2000.** [Source PDF](../../Finance/HedgeFunds_Asness_2001.pdf). All 21 supplied pages were read, including Appendix A's strategy definitions and the references; Tables 1–6 were checked visually. The library's [HedgeFunds_Asness2001.pdf](../../Finance/HedgeFunds_Asness2001.pdf) is a byte-identical copy, not a second work. Page references below are PDF/printed page numbers.

## Why this matters

A low correlation between monthly reported hedge-fund returns and liquid equity returns need not imply low economic equity exposure. If some underlying positions are marked late, a market loss can enter the fund's reported return over several subsequent months. A contemporaneous regression then assigns part of the exposure to its residual. During a rising equity market, it can also label compensation for that omitted exposure as manager alpha.

The paper tests this problem using asset-weighted CSFB/Tremont hedge-fund indices over January 1994–September 2000. Adding three lagged market returns raises the aggregate estimated exposure from 0.37 to 0.84. The aggregate annualized regression intercept moves from 2.63% to −4.45%, but neither intercept is statistically distinguishable from zero. The stronger result concerns the measurement of market exposure; the sample is too short and the performance model too narrow to establish that hedge-fund managers generally destroy value.

The contribution is an application of established nonsynchronous-trading corrections to hedge-fund evaluation, reinforced by horizon comparisons, style differences, asymmetric responses and robustness checks. It is not a new beta estimator or a causal identification of deliberate return manipulation. The authors explicitly acknowledge genuine delayed economic responses as an alternative explanation and show that adding a size factor materially changes the alpha conclusion.

## Data, universe and observable returns

The core sample has 81 calendar months. There is one aggregate index and nine strategy indices: convertible arbitrage, event driven, equity market neutral, fixed-income arbitrage, long/short equity, emerging markets, global macro, managed futures and dedicated short bias. The indices are portfolios of managers, not observations on a representative individual fund. Cross-manager diversification and heterogeneous exposures affect their volatility.

The CSFB/Tremont universe starts with TASS+ funds having at least \$10 million of assets, audited financial statements and the provider's reporting qualifications. Funds of funds are excluded; funds closed to new investment are included. As of 15 November 2000, the eligible universe contains 656 funds. Within each strategy, the provider chooses a subset representing at least 85% of eligible assets. Index returns are asset-weighted and net of fund fees. Reconstructing the historical index requires the contemporaneous constituents and weights, not the November 2000 list applied retrospectively.

The paper distinguishes three selection problems. Dead funds are not perfectly retained, and TASS/HFR began collecting dead-fund data only in 1994. Reported industry performance can therefore contain survivorship bias. CSFB/Tremont includes newly admitted funds prospectively, avoiding the particular backfill mechanism in which their successful pre-entry histories are inserted into past index returns. Voluntary reporting still creates self-selection. The authors regard the latter bias as generally small, but supply no experiment that identifies its magnitude in this sample. Their acknowledgment that survival in a strong market may select high-beta funds matters: surviving index exposure is not automatically the exposure of the complete historical industry.

Let $r_{i,t}$ denote a net-of-fees index total return, $r_{f,t}$ the one-month Treasury-bill return, and $r_{M,t}$ the S&P 500 total return. Use decimal monthly returns and define

$$
R_{i,t}=r_{i,t}-r_{f,t},\qquad
R_{m,t}=r_{M,t}-r_{f,t}-c_m.
$$

For regressions, the text removes an annual 20-basis-point index-management fee from the market proxy, because the hedge-fund series is net of fees. Taking $c_m=0.002/12$ is an explicit implementation of that annual fee; the supplied PDF does not spell out the monthly conversion convention. Table captions emphasize the Treasury-bill subtraction but do not restate the fee adjustment. Preserve the text's net-versus-net comparison and record the fee convention when reproducing results.

Table 1's annualized mean is twelve times the average monthly excess return, its volatility uses monthly observations, and its Sharpe ratio is their quotient. The quoted 13.2% compound annual total return for the aggregate index is a different statistic from its 8.0% arithmetic annual excess return. Neither should be substituted for the other in an alpha calculation.

| Index | Annual mean excess return | Annualized monthly volatility | Monthly correlation with S&P 500 |
|---|---:|---:|---:|
| Aggregate | 8.0% | 10.0% | 0.52 |
| Convertible arbitrage | 5.4% | 5.1% | 0.13 |
| Event driven | 7.0% | 6.7% | 0.60 |
| Equity market neutral | 6.4% | 3.5% | 0.48 |
| Fixed-income arbitrage | 1.6% | 4.4% | 0.08 |
| Long/short equity | 11.8% | 12.6% | 0.62 |
| Emerging markets | 2.3% | 20.8% | 0.50 |
| Global macro | 7.7% | 14.4% | 0.36 |
| Managed futures | −1.2% | 11.1% | 0.01 |
| Dedicated short bias | −7.1% | 18.6% | −0.76 |
| S&P 500 | 14.6% | 14.2% | 1.00 |

These are rounded source values. Several styles' worst observations cluster in August or October 1998. For example, August 1998 excess returns are −8.0% for the aggregate, −12.2% for event driven and −23.4% for emerging markets, versus −14.9% for the S&P 500. Managed futures and dedicated short bias instead record their best months then, at 9.5% and 22.3% respectively.

## Contemporaneous exposure and why beta is not correlation

The initial model is ordinary linear regression with an intercept:

$$
R_{i,t}=\alpha_i+\beta_iR_{m,t}+\varepsilon_{i,t}.
$$

The reported annualized alpha is $12\hat\alpha_i$. Its interpretation is net performance beyond average exposure to this single market proxy. It does not remove size, value, momentum, international-equity, credit, liquidity or nonlinear exposures. A positive intercept is therefore not a model-free measure of skill.

In the simple regression,

$$
\hat\beta_i=\hat\rho_{im}\frac{\hat\sigma_i}{\hat\sigma_m}.
$$

Equity market neutral illustrates why a small beta is not itself evidence of economically negligible dependence: $0.48(3.5/14.2)=0.1183$, approximately the reported 0.12 beta. The category has low volatility, so even this beta explains a material share of its risk. Its beta $t$-statistic is 4.89. Comparing raw alpha magnitudes across categories with very different volatility is similarly misleading.

The aggregate simple-regression alpha is 2.63% with $t=0.76$, beta is 0.37 with $t=5.46$, and adjusted $R^2$ is 26.5%. Convertible-arbitrage alpha is 4.78% with $t=2.35$, while equity-market-neutral alpha is 4.69% with $t=3.84$. These two apparently strong results motivate checking whether timing mismatches have understated exposure.

The simple hedge $R_{i,t}-\hat\beta_iR_{m,t}$ has sample mean equal to the fitted intercept and sample covariance zero with the contemporaneous market regressor, provided it is evaluated on the regression's own sample. That is an algebraic in-sample property, not an implementable forecast or a guarantee of neutrality to future market moves.

## Delayed reporting and the summed-beta estimator

The extended regression is

$$
R_{i,t}=\alpha_i+\sum_{j=0}^{3}\beta_{ji}R_{m,t-j}+\varepsilon_{i,t},
\qquad B_i=\sum_{j=0}^{3}\beta_{ji},
\qquad L_i=\sum_{j=1}^{3}\beta_{ji}.
$$

$B_i$ is total summed exposure and $L_i$ is its lagged component. A positive market innovation can be recorded partly immediately and partly in later fund reports. Summing the coefficients collects those responses rather than treating the late part as unrelated return. The source uses three monthly lags; it does not estimate a data-selected lag length or claim that three months capture every illiquid position's repricing.

A useful explanatory reconstruction makes the identifying assumption explicit. Suppose the latent economic return is $R^*_{i,t}=a_i+b_iR_{m,t}+u_{i,t}$ and the reported return is a finite distributed average

$$
R_{i,t}=\sum_{j=0}^{K}\theta_jR^*_{i,t-j},
\qquad \sum_{j=0}^{K}\theta_j=1.
$$

If the lagged disturbances are orthogonal to the included market regressors, the regression coefficients are $b_i\theta_j$, and their sum is $b_i$. With an uncorrelated market series, a contemporaneous-only regression sees just $b_i\theta_0$. This stylized model explains the correction; it is not a smoothing model estimated in the paper. Time-varying exposures, omitted factors, a longer reporting lag or correlated disturbances can break the correspondence between summed coefficients and economic beta.

Implement inference on sums using their covariance matrix. If $\hat V$ is the estimated covariance of the four slopes and $a=(1,1,1,1)'$, then

$$
\operatorname{se}(\hat B_i)=\sqrt{a'\hat V a}.
$$

Use $a=(0,1,1,1)'$ for $L_i$. Table 4a's F-tests concern the scalar restrictions $B_i=0$ and $L_i=0$. The second is not the joint three-restriction hypothesis that every lagged coefficient is zero: offsetting lag coefficients can sum to zero without all being zero. A replication must not replace the reported test by that different null. The PDF reports $t$-statistics and F-test probabilities but does not specify a heteroskedasticity/autocorrelation-robust covariance implementation; an added HAC exercise should be labeled a robustness extension.

| Index | Simple beta | Summed beta | Simple annual alpha | Lag-model annual alpha | Lag-model alpha $t$ |
|---|---:|---:|---:|---:|---:|
| Aggregate | 0.37 | 0.84 | 2.63% | −4.45% | −1.16 |
| Convertible arbitrage | 0.04 | 0.43 | 4.78% | −0.98% | −0.46 |
| Event driven | 0.28 | 0.61 | 2.93% | −2.12% | −0.91 |
| Equity market neutral | 0.12 | 0.20 | 4.69% | 3.36% | 2.32 |
| Fixed-income arbitrage | 0.02 | 0.36 | 1.24% | −3.78% | −2.08 |
| Long/short equity | 0.55 | 0.99 | 3.82% | −2.83% | −0.61 |
| Emerging markets | 0.74 | 1.25 | −8.38% | −16.20% | −1.88 |
| Global macro | 0.37 | 0.98 | 2.41% | −6.64% | −1.08 |
| Managed futures | 0.01 | −0.19 | −1.30% | 1.72% | 0.32 |
| Dedicated short bias | −0.99 | −1.27 | 7.34% | 11.59% | 2.00 |

The aggregate distributed slopes are 0.40, 0.12, 0.22 and 0.10. Their respective $t$-statistics are 6.21, 1.85, 3.37 and 1.45; adjusted $R^2$ rises to 35.3%. The lagged sum is 0.44 with a reported F-test probability of 0.1%. Displayed 0.0% probabilities elsewhere are rounded, not exact zero probabilities. Since individual coefficients are rounded, the sum of printed components sometimes differs from the reported total by 0.01; use full-precision estimates in replication.

The lagged sum is significant at 5% for the aggregate, convertible arbitrage, event driven, fixed-income arbitrage, long/short equity and global macro. It is not significant for equity market neutral, emerging markets, managed futures or dedicated short bias. Total summed exposure is significant for every category except managed futures. Thus the economic point estimates and the evidence for delayed response must be distinguished category by category.

## Horizon aggregation and asymmetric exposure

Table 3 compares monthly observations with 27 nonoverlapping calendar quarters. Importantly, the authors **sum monthly excess returns** within a quarter; they do not compound them. Let $Q_{i,q}=R_{i,3q-2}+R_{i,3q-1}+R_{i,3q}$. Compare $\sqrt{12}\,s(R_i)$ with $\sqrt4\,s(Q_i)$ and calculate correlations with market returns aggregated in the same way.

For a stationary monthly series with autocovariances $\gamma_k$, the corresponding population identity is

$$
4\operatorname{Var}(Q_i)=12\gamma_0+16\gamma_1+8\gamma_2.
$$

This derived identity makes the diagnostic precise. Positive autocorrelation increases the annualized quarterly variance relative to $12\gamma_0$; the calculation alone cannot say whether that autocorrelation comes from valuation smoothing or genuine economic dynamics. The authors note that S&P 500 returns have mildly negative, insignificant autocorrelations at the first three lags, so rising fund-market correlation adds information beyond rising fund volatility.

Aggregate volatility changes little, from 10.0% to 10.1%, but its market correlation rises from 0.52 to 0.64. Convertible arbitrage changes from 5.1% to 7.2% volatility and 0.13 to 0.23 correlation; the reported volatility increase, computed before rounding, is 41.5%. Event-driven volatility rises from 6.7% to 8.6%; equity-market-neutral volatility rises from 3.5% to 4.2%. Long/short-equity correlation rises from 0.62 to 0.76. Not every category follows the pattern: emerging-market correlation falls from 0.50 to 0.44, and managed-futures volatility falls from 11.1% to 10.5% while its correlation becomes −0.29 from 0.01.

Table 5 separates up-market and down-market responses. A reproducible interpretation of its displayed current and lagged columns is the piecewise-linear model

$$
R_{i,t}=\alpha_i+\sum_{j=0}^{3}\left[
\beta_{ji}^{+}R_{m,t-j}\mathbf1\{R_{m,t-j}>0\}
+\beta_{ji}^{-}R_{m,t-j}\mathbf1\{R_{m,t-j}\le0\}
\right]+\varepsilon_{i,t}.
$$

This equation is a reconstruction of the table's specification, not a displayed source equation. The prose emphasizes doubling the three lagged terms, while the table also reports different contemporaneous coefficients. Exact replication requires confirming the original indicator construction and intercept treatment in the authors' code, which is not supplied. The intended comparison is current plus delayed exposure following positive versus negative market returns, not a predictive trading rule based on knowing a future market state.

For the aggregate, current/up exposure is 0.27 and the lagged/up sum is 0.17, producing total up exposure 0.44. Current/down exposure is 0.59 and the lagged/down sum is 0.79, producing total down exposure 1.38. The paper describes the down-market lag sum and its difference from the up-market sum as highly significant, but Table 5 does not print their standard errors or numerical probabilities. Fixed-income arbitrage has total up/down exposures 0.08/0.70; emerging markets 0.46/2.22; global macro 0.27/1.98. Equity market neutral goes the other way, at 0.31/0.06.

The authors interpret stronger delayed losses as circumstantial evidence of discretionary smoothing. It does not identify intent. Nonlinear economic exposures, state-dependent liquidity and valuation difficulty can also create asymmetry. The paper itself presents the interpretation as suggestive rather than conclusive, and its monthly index data cannot distinguish which managers deliberately altered marks.

## Hedged performance: three different return series

The paper compares the unhedged series with two contemporaneously market-hedged series:

$$
H^{(0)}_{i,t}=R_{i,t},\qquad
H^{(s)}_{i,t}=R_{i,t}-\hat\beta_iR_{m,t},\qquad
H^{(B)}_{i,t}=R_{i,t}-\hat B_iR_{m,t}.
$$

For each, calculate the reported annualized Sharpe convention as

$$
\widehat{SR}(H)=\frac{12\bar H}{\sqrt{12}\,s(H)}.
$$

The summed-beta hedge uses the whole estimated economic exposure against the current liquid-market return. It is not the distributed regression residual $R_{i,t}-\sum_j\hat\beta_{ji}R_{m,t-j}$. It also is not generally contemporaneously beta-zero. On an identical estimation sample, its simple-regression beta is $\hat\beta_i-\hat B_i$, approximately $0.37-0.84=-0.47$ for the aggregate. The source's description of both hedges as reducing “in-sample beta to zero” needs this distinction: the second offsets the summed response measure, rather than the simple contemporaneous regression coefficient.

Likewise, the extended regression intercept and the mean of $H^{(B)}$ need not coincide in finite samples:

$$
\bar H^{(B)}-\hat\alpha_i
=\sum_{j=0}^{3}\hat\beta_{ji}
\left(\bar R_{m,t-j}-\bar R_{m,t}\right).
$$

Equal population market means at different lags eliminate this difference in a stationary population, but sample boundaries and dropped observations need not. Do not force the −4.45% lag-regression alpha to equal twelve times the summed-hedge sample mean using rounded Table 1 inputs.

| Index | Unhedged Sharpe | Simple-beta hedge | Summed-beta hedge |
|---|---:|---:|---:|
| Aggregate | 0.80 | 0.31 | −0.40 |
| Convertible arbitrage | 1.07 | 0.95 | −0.11 |
| Event driven | 1.05 | 0.55 | −0.27 |
| Equity market neutral | 1.85 | 1.55 | 1.05 |
| Fixed-income arbitrage | 0.36 | 0.28 | −0.56 |
| Long/short equity | 0.94 | 0.39 | −0.23 |
| Emerging markets | 0.11 | −0.47 | −0.82 |
| Global macro | 0.54 | 0.18 | −0.40 |
| Managed futures | −0.10 | −0.12 | 0.14 |
| Dedicated short bias | −0.38 | 0.61 | 0.89 |

A larger exposure correction need not penalize every period. In January–September 2000, the aggregate earns 4.9% total and about 0.5% above cash. With the market falling, the simple-beta adjustment raises the reported excess performance to 2.7%, and the summed-beta adjustment raises it to 5.5%. These are results for that nine-month interval, not the full-sample annualized alpha. The corresponding convertible-arbitrage figures are 20% excess of cash and 22.5% after the summed-beta adjustment.

The authors warn that subtracting a current liquid-market hedge from a delayed reported fund return can exaggerate the measured hedge-series volatility. That pulls the Sharpe magnitude toward zero if the numerator is unchanged. More generally, square-root-of-time annualization is a reporting convention here, not a consistent estimate of an annual investment Sharpe under arbitrary serial dependence. Implementation should retain the paper's convention for comparison and separately report any long-horizon correction.

## Robustness, alternative explanations and scope

Excluding August–November 1998 reduces the aggregate summed beta from 0.84 to 0.69, compared with a contemporaneous beta of 0.41 on the reduced sample. The lagged component remains significant. Constraining the three lag coefficients to equal one another produces aggregate summed beta 0.80 instead of 0.84. These checks show that the result is not entirely the unrestricted fit of three slopes to the crisis observations; they do not remove all small-sample or specification uncertainty.

Using equally weighted HFR indices rather than asset-weighted CSFB/Tremont indices raises aggregate beta from 0.38 to 0.65 when delayed exposures are included. The unhedged Sharpe of 1.23 falls to 0.03 after the summed-beta hedge. The 1.20 reduction matches the magnitude of the CSFB/Tremont change from 0.80 to −0.40. HFR gives relatively more weight to smaller funds and has different reporting and investability issues. Its separate merger-arbitrage index retains strong significant positive risk-adjusted returns; CSFB/Tremont combines merger arbitrage with distressed debt, Regulation D and high yield in event driven.

The size-factor check in footnote 18 is consequential. Adding small-minus-large stock returns finds a small-cap tilt. Small stocks underperformed large stocks during this sample, and the extended model leaves the aggregate with approximately zero added or subtracted value. Thus the negative single-factor alpha is not robust evidence of negative skill. The authors say the understated-beta result remains. Their preliminary squared-market-return specification finds positive convexity for managed futures and negative convexity for most other categories; these nonlinear estimates are sensitive to the 1998 observations and do not materially overturn the lagged-beta result. Exact coefficients for these extensions are not supplied.

A genuine economic lead-lag relation is another explanation. For example, market conditions can change later merger-completion probabilities. Monthly data cannot distinguish that channel from delayed marking. Lockups and advance redemption notice may prevent an investor from exploiting the apparent predictability, leaving economically relevant market exposure either way. Conversely, asynchronous marks can overstate volatility for some genuinely hedged cross-time-zone portfolios; the paper explicitly rejects treating every stale-price effect as an automatic downward bias.

Average market exposure might itself result from successful long-horizon timing. The regressions subtract it regardless of whether it was a passive policy or an intentional tactical bet. They cannot measure timing skill separately. Performance fees also create asymmetry: even a linear gross payoff can have different net-of-fee upside and downside slopes. Dedicated short bias may look relatively skilled partly because a bull-market survival filter is severe and little incentive compensation was charged during its poor absolute performance.

## Replication requirements and practical use

An auditable reproduction should preserve dated index vintages, all ten monthly net series, S&P total returns, one-month Treasury-bill returns and the index-fee adjustment. Align month ends before subtraction. Construct a common sample for comparisons, explicitly record whether pre-1994 market observations supply the initial lags or whether the first three fund months are dropped, and retain at least full machine precision until reporting. The PDF's January 1994–September 2000 captions do not fully resolve that lag-boundary choice.

First reproduce Table 1 and the contemporaneous regressions, including intercepts, standard errors, adjusted $R^2$ and extreme months. Next reproduce nonoverlapping summed-quarter returns, the four-slope regressions, both scalar-sum restrictions and the asymmetric specification. Then construct the three hedge-return series directly; do not substitute regression residuals for the summed-beta hedge. Repeat the crisis deletion, equal-lag restriction and HFR comparison on explicitly documented samples. A further out-of-sample implementation would estimate exposures using only past returns and include hedge costs, but that is an extension, not a test performed here.

The underlying monthly observations, contemporaneous membership history, exact standard-error implementation, full-precision estimates, asymmetric-regression code and numerical multifactor results are not included. Consequently the note reconstructs the estimands and computational sequence and preserves the published targets, but cannot certify an exact numerical rerun from the PDF alone.

The useful decision rule is to inspect delayed market response before treating a smooth reported track record as diversifying alpha. The source establishes a material measurement risk in these historical index data. It leaves individual-manager selection, causal attribution of smoothing, full multifactor skill and investable out-of-sample performance unresolved.

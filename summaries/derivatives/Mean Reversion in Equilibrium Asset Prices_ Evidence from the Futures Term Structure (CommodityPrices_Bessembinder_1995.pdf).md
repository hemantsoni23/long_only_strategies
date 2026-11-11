# Mean Reversion in Equilibrium Asset Prices: Evidence from the Futures Term Structure

Hendrik Bessembinder, Jay F. Coughenour, Paul J. Seguin, and Margaret Monroe Smoller, *The Journal of Finance* 50(1), March 1995, pp. 361–375. [Source PDF](../../Finance/CommodityPrices_Bessembinder_1995.pdf). The supplied file has sixteen PDF pages: a JSTOR cover followed by the complete fifteen-page article. Page references below use journal pagination; PDF page 2 is p. 361.

## Why this matters

The paper asks whether a spot-price shock contains a component expected to reverse, using the contemporaneous futures curve rather than a regression of realized future spot returns. This matters for commodity exposure and long-dated valuation: a large nearby price move need not imply an equally large change in the value of delivery a year later. A curve whose distant contracts respond less than the nearby contract provides information about the persistence of shocks, subject to restrictions on risk premia and the interpretation of the nearby contract as a spot-price proxy.

The empirical contrast is sharp. In 1982–1991 daily data, agricultural commodities and crude oil display much smaller distant-price responses than nearby-price responses. Precious metals display weaker attenuation. Treasury-bond and stock-index futures provide little comparable evidence once the October 1987 crash is treated separately. The principal contribution is an equilibrium identification argument connecting these responses to implied cash-flow yields and interest rates. It is not an estimate of a profitable mean-reversion trading rule, and no transaction-cost-adjusted strategy is tested.

The title's term “mean reversion” needs a precise interpretation. Here it means an elasticity of the expected future spot level with respect to the current level below one. It does not establish stationarity, a constant unconditional price mean, an Ornstein–Uhlenbeck law, or negative autocorrelation of short-horizon returns. Even a price process with a permanent component can satisfy this elasticity condition over a particular horizon.

## Cost of carry, expected prices, and the identifying restriction

Let $P_t$ be the spot price, $F_t(m)$ the futures price for delivery $m$ periods ahead, $r_t$ the continuously compounded financing rate over that horizon, and $c_t$ the corresponding cash-flow yield accruing to the marginal holder of the asset. For equity this yield includes dividends; for bonds, coupons; for commodities it is the convenience yield net of storage costs. The maintained cost-of-carry relation is

$$
F_t(m)=P_t\exp[(r_t-c_t)m].
$$

The paper abstracts from differences between forward and futures prices arising from daily settlement, delivery options, and other impediments to exact carry arbitrage. These abstractions matter especially for interpreting financial futures, where deliverable-grade and timing options can affect the observed basis.

Define the long-futures risk premium by

$$
\pi_t=\frac{1}{m}\log\frac{E_t[P_{t+m}]}{F_t(m)}.
$$

This is a logarithm of a ratio involving the *expected future price level*. It is not $E_t[\log(P_{t+m}/F_t(m))]$, and it is not a return on the margin capital committed to a futures position. Combining these definitions gives

$$
P_t=E_t[P_{t+m}]\exp[-m(r_t+\pi_t-c_t)].
$$

For a fixed horizon, regard $r$, $c$, and $\pi$ as differentiable functions of the current price state $P$. Differentiation gives the paper's equation (4):

$$
\eta_E\equiv\frac{P}{E[P_{t+m}]}\frac{\partial E[P_{t+m}]}{\partial P}
=1+mP(r'+\pi'-c').
$$

The expected-price elasticity is below one exactly when $r'+\pi'-c'<0$. The directly observable futures-price elasticity is instead

$$
\eta_F\equiv\frac{P}{F(m)}\frac{\partial F(m)}{\partial P}
=1+mP(r'-c').
$$

Writing the log-curve slope as $s=r-c$, a negative response $s'<0$ implies $\eta_F<1$. It also implies $\eta_E<1$ **if the risk premium is nonincreasing in price**, $\pi'\leq0$. This additional assumption is consequential. Cost of carry alone does not identify the persistence of physical expected spot prices from the futures curve. A sufficiently positive $\pi'$ could offset a negative $s'$.

The authors motivate the risk-premium restriction by the familiar inverse relation between a price and its discount rate, holding expected cash flows fixed. In a multistate equilibrium, cash-flow news and risk-premium news can move together, so that motivation is not a general theorem about observed commodity prices. Footnote 2 reports supplemental regressions in which estimated risk-premium/price relations were negative in virtually all cases but none was statistically significant. Those results are not tabulated. They support neither a precise risk-premium correction nor a decisive test of the maintained sign restriction.

There are two observable equilibrium channels. A commodity price increase can raise its convenience yield because immediately available inventory becomes especially valuable; then $c'>0$ flattens or inverts the curve. Alternatively, higher prices can be associated with lower financing rates, $r'<0$. Both can lower the futures elasticity. A third channel, falling risk premia, can create expected-price mean reversion without a corresponding flattening of the observed curve. Failure to detect the first two channels therefore does not rule out the third. Nor does this method detect price correction associated with a temporary failure of cost of carry, since exact carry is a maintained equilibrium condition.

The equations apply to a particular maturity. Horizon-specific rates, yields, and risk premia need not have identical derivatives across tenors. The empirical maturity pattern supplies evidence about attenuation; it is not mechanically imposed by a single linear function of maturity.

## Data construction and estimands

The sample consists of daily settlement prices from Data Resources, Inc., primarily January 1982 through December 1991. There are eleven markets: wheat, live cattle, orange juice, world sugar, domestic sugar, crude oil, gold, silver, platinum, Treasury bonds, and the S&P 500. Stock-index futures begin in April 1982, crude oil in March 1983, and domestic sugar in September 1985. The article does not provide an observation-count table for every contract/rank combination.

The nearest eligible futures contract proxies for spot. This avoids mismatched cash/futures observation times and measurement problems in cash prices, at the cost of introducing a nonzero delivery horizon. Contracts in their delivery month are excluded. “Nearby 1” is the nearest remaining delivery; “Nearby 2” is the next; and so forth. Ranks with prices on fewer than 80 percent of sample trading dates are omitted. Metals use major delivery months, whose contracts are listed for a year or more, rather than short-lived minor months with low open interest. This is a retrospective data-availability screen, not an investable real-time universe rule.

The major delivery schedules are important for reconstruction: crude oil has monthly deliveries; gold, silver, and cattle use February, April, June, August, October, and December; platinum uses January, April, July, and October; wheat uses March, May, July, September, and December; orange juice uses January, March, May, July, September, and November; domestic sugar uses January, April, July, and October, while world sugar uses March, May, July, and October; and the financial contracts use March, June, September, and December. A given nearby rank therefore does not represent a common calendar horizon across assets.

For maturities $0<n<m$, the forward financing rate is extracted from Treasury-bill spot yields:

$$
r_{n,m,t}=\frac{m r_{m,t}-n r_{n,t}}{m-n}.
$$

The implied forward cash-flow yield and log futures-curve slope are

$$
c_{n,m,t}=r_{n,m,t}-\frac{\log[F_t(m)/F_t(n)]}{m-n},
$$

$$
s_{n,m,t}=\frac{\log[F_t(m)/F_t(n)]}{m-n}=r_{n,m,t}-c_{n,m,t}.
$$

The empirical pairs are adjacent deliveries: the row labeled Nearby 2 uses contracts 1 and 2, Nearby 3 uses contracts 2 and 3, and so on. These curve-slope regressions differ from the later return-elasticity regressions, in which every distant contract is compared with Nearby 1.

Tables I–III regress first differences in the term slope, implied yield, and financing rate on the contemporaneous change in the nearby price, with the price expressed relative to its own sample mean. The dependent variables are multiplied by 25,000, combining 250 trading days and 100 percentage points. The reported slopes thus describe changes in annualized percentage rates for a unit change in a price normalized by its mean. A one-percent-of-mean price move corresponds to multiplying a displayed coefficient by 0.01. These coefficients are not futures excess returns and should not be read as basis-point P&L without a further conversion.

A reconstruction should retain the actual contract identifiers when calculating daily changes and then assign maturity ranks. Changes caused by a shift in the nearby contract are a potential nuisance. The article specifies the delivery-month exclusion and rank screens, but does not supply a detailed roll-day return-splicing algorithm, missing-price rules, bill-yield interpolation, or all day-count conventions. These omissions should be treated as replication inputs to resolve from original data documentation, not filled in with an assumed modern continuous-futures series.

Inference uses a heteroskedasticity/autocorrelation-consistent covariance estimator. For pooled coefficient tests, observations are sorted by date and then delivery; with $K$ included maturities, the authors use $K+1$ lags to allow for cross-maturity dependence and first-order serial correlation. Wald statistics test restrictions such as all coefficients zero, all elasticities one, or all elasticities equal. In matrix notation the statistic is $(R\hat\beta-r)'[R\widehat{\operatorname{Var}}(\hat\beta)R']^{-1}(R\hat\beta-r)$, with asymptotic chi-square degrees of freedom equal to the number of restrictions. This particular stacked-data HAC construction should be replicated if reproducing the tables; it is not interchangeable with an unrestricted date-cluster covariance or a much longer serial-dependence adjustment.

## What the curve regressions show

The nearest-delivery term-slope coefficients illustrate the contrast across markets. Table I, p. 368, reports the following estimates and standard errors in the annualized-rate scaling just described:

| Market | Curve-slope response | Standard error |
|---|---:|---:|
| Crude oil | −148.76 | 11.82 |
| Wheat | −35.92 | 4.55 |
| Orange juice | −96.74 | 7.56 |
| Domestic sugar | −194.92 | 11.72 |
| World sugar | −37.36 | 3.63 |
| Cattle | −38.96 | 4.05 |
| Silver | −5.24 | 1.63 |
| Gold | −0.70 | 0.39 |
| Platinum | −3.82 | 0.42 |
| Treasury bonds | 0.28 | 0.60 |
| S&P 500, full sample | −0.19 | 0.82 |
| S&P 500, crash dates excluded | 1.78 | 0.81 |

The commodity coefficients generally become smaller in magnitude at more distant adjacent pairs. Oil declines to −16.32 (2.79) at Nearby 8. Domestic sugar declines to −15.21 (10.09) at Nearby 5 before becoming −27.59 (13.23) at Nearby 6. There is strong joint evidence, but not every individual commodity coefficient is significant at the same conventional threshold. Gold's nearest slope, for example, has an absolute estimate/standard-error ratio below two. The text's broad characterization of significant commodity responses should not replace row-specific inference.

The joint tests that all term-slope responses are zero have displayed $p$-values of 0.000 for each of the nine physical commodities. These are rounded small probabilities, not literally zero. Treasury bonds have a statistic of 6.73 and $p=0.457$. The full-sample stock-index statistic is 16.24, $p=0.001$, but becomes 4.64, $p=0.200$, after excluding October 15–31, 1987.

Table II, p. 369, shows that implied cash-flow yields account for nearly all of the physical-commodity curve response. At the nearest pair, oil's yield coefficient is 148.75 (11.83), orange juice's is 96.54 (7.56), domestic sugar's is 195.19 (11.07), and world sugar's is 37.49 (3.61). The positive relation is consistent with inventory scarcity raising the benefit of immediate possession. Domestic sugar's nearest yield sensitivity is about 5.21 times world sugar's. The authors connect this difference to the domestic import-quota regime, which limits access to lower-priced world supplies. It is an economically plausible comparison, not a controlled causal estimate of the effect of quotas.

Table III, p. 370, indicates little financing-rate response for most physical commodities. At the nearest pair, oil is approximately zero (0.22), wheat −0.03 (0.14), and orange juice −0.19 (0.25). Silver and gold have significant joint financing-rate relations, whereas platinum does not: their all-zero test $p$-values are 0.001, 0.000, and 0.526 respectively. Some distant gold and silver rate coefficients are positive, so a uniform negative-rate mechanism would overstate the table.

Treasury bonds provide the cleanest caution against interpreting one component alone. Their nearest financing-rate coefficient is −4.35 (0.42), while the implied coupon-yield coefficient is −4.63 (0.56). These nearly offset, leaving the positive, insignificant curve-slope coefficient 0.28. A bond's fixed coupon divided by a higher price falls; financing rates also fall when bond prices rise. The net effect relevant for the futures curve is small. On identical samples and specifications, the coefficient identity $\hat\beta_s=\hat\beta_r-\hat\beta_c$ follows directly from $s=r-c$. The three tables decompose the same response; they do not provide three independent causal tests.

## Distant-return elasticities and shock attenuation

Table IV, p. 374, directly regresses each distant contract's daily log-price change on the contemporaneous Nearby 1 log-price change. The population regression coefficient is $\operatorname{Cov}(\Delta\log F_m,\Delta\log F_1)/\operatorname{Var}(\Delta\log F_1)$. Calling it a structural price elasticity requires the model's interpretation of a common price-state disturbance. Additional factors, asynchronous prices, and measurement error can separate this regression slope from a derivative holding all other states fixed.

The following subset preserves the principal quantitative results. Parentheses contain reported standard errors.

| Market | Nearby 2 | Nearby 5 | Most distant included |
|---|---:|---:|---:|
| Oil | 0.808 (0.016) | 0.669 (0.023) | Nearby 8: 0.564 (0.028) |
| Silver | 0.985 (0.004) | 0.948 (0.005) | Nearby 7: 0.888 (0.010) |
| Gold | 0.998 (0.001) | 0.985 (0.004) | Nearby 8: 0.943 (0.009) |
| Platinum | 0.985 (0.002) | 0.942 (0.004) | Nearby 5: 0.942 (0.004) |
| Wheat | 0.874 (0.015) | 0.662 (0.022) | Nearby 5: 0.662 (0.022) |
| Orange juice | 0.743 (0.022) | 0.606 (0.028) | Nearby 7: 0.576 (0.031) |
| Domestic sugar | 0.456 (0.032) | 0.254 (0.038) | Nearby 6: 0.139 (0.044) |
| World sugar | 0.831 (0.016) | 0.600 (0.010) | Nearby 5: 0.600 (0.010) |
| Cattle | 0.858 (0.011) | 0.514 (0.018) | Nearby 6: 0.459 (0.019) |
| Treasury bonds | 1.000 (0.002) | 0.986 (0.010) | Nearby 8: 0.969 (0.016) |

Oil's intermediate slopes at ranks 3, 4, 6, and 7 are 0.742, 0.701, 0.632, and 0.617. The authors summarize the eighth-nearby result as roughly 44 percent expected reversal over about eight months. The exact complement of the reported slope is 43.6 percent. A simple normal approximation using its 0.028 standard error gives approximately 38.1–49.1 percent for this complement; that interval is a derived statistical illustration, not a reported confidence interval or an allowance for identification error.

The fifth-nearby agricultural responses of 0.514–0.662, excluding domestic sugar, imply substantial attenuation over the approximately annual horizons discussed by the authors. Delivery calendars differ, so these ranks must not be relabeled as exact common one-year contracts. Domestic sugar's fourth-nearby coefficient is 0.289 (0.033), versus world sugar's 0.650 (0.011). This is consistent with especially transitory domestic scarcity shocks but still depends on the same risk-premium and proxy assumptions.

The nearest-futures proxy can bias the inferred attenuation toward one under the paper's ordering argument. If both near and far contracts have positive spot elasticities below one, and the far elasticity is smaller, the observed ratio of far to near elasticities exceeds the far contract's elasticity relative to true spot. This is a conditional comparison, not a general statement about all measurement error: independent noise in the regressor can instead attenuate a regression slope. Footnote 7's economic proxy argument should not be conflated with classical errors-in-variables bias.

All physical commodities reject the joint hypothesis that the included coefficients equal one at displayed $p=0.000$. Treasury bonds do not: 5.89, $p=0.552$. For the stock index, full-sample slopes at ranks 2–4 are 1.001 (0.002), 0.995 (0.003), and 0.988 (0.004), with an all-one test of 12.16, $p=0.007$. After excluding the crash dates, the slopes are 1.010 (0.002), 1.011 (0.003), and 1.008 (0.004). They still reject equality to one, now in the direction of slight amplification; the hypothesis that these three coefficients equal each other is not rejected, $p=0.748$. Statistical rejection of unit elasticity by itself is therefore not evidence of mean reversion.

One printed Table IV entry is internally inconsistent. For orange juice the “all equal” statistic appears as 3.522 with $p=0.000$. Equality of six coefficients imposes five restrictions; a chi-square statistic of 3.522 on five degrees of freedom does not have a near-zero upper-tail probability. The scan confirms the displayed digits. Neither the intended statistic nor the intended probability can be recovered from the supplied table, so this note does not silently substitute 352.2 or another conjectured value. The separate all-one rejection, 596.7, and the individual declining slopes remain directly readable.

## Reimplementation and limits

A faithful implementation needs settlement prices by contract, delivery calendars, contemporaneous Treasury-bill yields, and the original eligibility rules. It should construct the adjacent-pair yields and the all-versus-nearest return regressions separately; reproduce the 25,000 scaling; retain contract identifiers across rolls; and perform the zero, one, and equality restrictions using the source's covariance construction. The October 1987 exclusion is a specified robustness check, not a general crash-filtering algorithm. Sensitivity to alternative nearby definitions, bill interpolation, fixed calendar maturities, roll-day treatment, and richer dependence corrections would be additional research rather than reported results.

There is no training/validation split, parameter tuning, forecasting competition, portfolio rebalancing rule, estimated trading turnover, transaction-cost model, or risk-adjusted investment performance. The regressions concern simultaneous responses and equilibrium expected-price interpretation. Turning the findings into a forecast of realized returns would require a physical risk-premium model, current inventory or convenience-yield information, contract-level execution assumptions, and an evaluation outside the estimation sample.

The lasting quantitative lesson is the distinction between nearby volatility and the exposure of distant delivery prices to the same shocks. Agricultural commodities and oil display large differences; precious metals display smaller differences; financial futures exhibit offsetting carry components or crash-sensitive effects. The data support that cross-market ordering more directly than they establish a universal stochastic law for commodity spot prices. Equations (1)–(5), pp. 363–365, carry the identification argument; equations (6)–(8), pp. 366–367, define the empirical carry decomposition; Tables I–III report its estimates; and Table IV supplies the shock-elasticity magnitudes.

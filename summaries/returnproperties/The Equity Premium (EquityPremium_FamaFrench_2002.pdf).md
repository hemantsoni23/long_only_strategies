# The Equity Premium

**Eugene F. Fama and Kenneth R. French.** *The Journal of Finance* 57(2), April 2002, 637–659. DOI: 10.1111/1540-6261.00437. Source: [EquityPremium_FamaFrench_2002.pdf](../../Finance/EquityPremium_FamaFrench_2002.pdf), the 23-page published article. Printed page 637 is PDF page 1. All pages, tables, and the valuation-ratio figure were inspected. The separately mentioned appendix was available on request and is absent from this PDF; a bounded search of the publisher and Kenneth French's research page did not locate it.

## Why this matters

A long period of high realized stock returns need not imply a high expected equity premium. Part of the realized return may be an unexpected increase in valuation multiples caused by a decline in the required return. Extrapolating that capital gain into a cost-of-capital estimate then counts the benefit of a lower discount rate as evidence for a higher future discount rate. The paper provides a simple way to diagnose this problem using the difference between growth in stock prices and growth in dividends or earnings.

The empirical question is historical: what was the average expected real return on the US equity market during 1872–2000, especially 1951–2000? It is not an estimate of today's conditional expected return, a tactical asset-allocation backtest, or an equilibrium explanation of why risk premia change. The contribution is to compare three estimators of the same broad historical object and evaluate them using precision, valuation, and profitability evidence. The authors emphasize the long pre-1951 comparison period because it shows that a gap between realized returns and fundamentals is not inevitable.

Their headline estimates for 1951–2000 are real equity premia of 2.55% from dividend growth, 4.32% from earnings growth, and 7.43% from realized stock returns. Those first two numbers are **unadjusted**. For the expected annual simple premium, the paper's variance corrections raise them to 3.83% and 4.78%. Omitting the correction would misstate the model's own qualification. Even after correction, the gap with the realized-return estimate remains economically large.

The paper is particularly useful as a reconstruction exercise because its basic estimators have few moving parts. Its most delicate issues are conceptual rather than computational: real versus nominal quantities, beginning- versus end-year denominators, arithmetic versus compounded returns, stationarity of valuation ratios, payout-policy changes, and how much one can infer about expectations from a single realized historical path.

## The three estimators and their assumptions

Let $P_t$, $D_t$, and $Y_t$ denote real year-end stock price, real dividends for year $t$, and real earnings for year $t$. Let $A(\cdot)$ denote a time-series arithmetic mean. Define simple growth rates

$$
GP_t=\frac{P_t-P_{t-1}}{P_{t-1}},\qquad
GD_t=\frac{D_t-D_{t-1}}{D_{t-1}},\qquad
GY_t=\frac{Y_t-Y_{t-1}}{Y_{t-1}}.
$$

Ignoring intrayear dividend reinvestment in the analytical identity, the annual stock return is dividend yield plus price appreciation:

$$
R_t=\frac{D_t}{P_{t-1}}+GP_t.
$$

The conventional expected-return estimate is $A(R)$. The alternative dividend and earnings estimates replace the capital-gain component:

$$
\widehat\mu_D=A\!\left(\frac{D_t}{P_{t-1}}\right)+A(GD),\qquad
\widehat\mu_Y=A\!\left(\frac{D_t}{P_{t-1}}\right)+A(GY).
$$

The earnings model still uses the **dividend yield**, not the earnings yield, for the cash-distribution component. Adding an earnings yield to earnings growth would double-count retained earnings' contribution and would not reproduce equation (3). The dividend yield here is $D_t/P_{t-1}$; the dividend–price ratio used to assess stationarity and forecast growth is $D_t/P_t$. The paper carefully distinguishes them, and the distinction matters when prices move substantially during a year.

The logic is a cointegration argument. Write $q_t=D_t/P_t$. The exact pathwise relation is

$$
\log(P_T/P_0)-\log(D_T/D_0)=\log q_0-\log q_T.
$$

If the log valuation ratio is stationary with suitable moments, its endpoint contribution divided by $T$ vanishes asymptotically. Long-run average log price growth and dividend growth then coincide. The same reasoning applies to earnings and the earnings–price ratio. This is stronger than simply asserting that dividends and prices trend upward together, but weaker than specifying a constant-growth Gordon model. Conditional expected returns and growth can vary; the principal target is their unconditional historical average.

The arithmetic estimators above inherit an approximation: equality of long-run log growth does not imply equality of expected one-period simple growth when variances differ. Section III addresses this explicitly. The accounting decomposition is exact in its stated convention; using dividend growth as the expected capital gain and the subsequent variance corrections require maintained statistical assumptions.

The authors permit structural shifts in expected growth or returns, provided valuation ratios mean-revert within regimes. A permanent shift in expected growth can be offset by a changed dividend yield, while a permanent discount-rate shift generates a one-time price jump that affects realized returns more than a fundamental-growth estimate. This is a useful robustness argument, not a general theorem that arbitrary nonstationary price/dividend processes leave the estimators unbiased. Continuous transitions in payout policy are one of the paper's own exceptions.

## Data reconstruction, dates, and units

Use annual data for the S&P 500 and its historical antecedents, 1872–2000 inclusive, 129 observations. The principal split is 1872–1950, 79 years, and 1951–2000, 50 years. The market is a broad US equity index rather than the theoretical portfolio of all investable wealth. The authors report similar results using the CRSP value-weighted NYSE/AMEX/Nasdaq index after 1925 but do not tabulate that alternative.

Dividends, prices, and returns before 1926 come from Shiller. An important historical convention is that the early annual price series averages daily January values; those returns are not identical to modern December-end-to-December-end returns. For 1926–2000, Ibbotson Associates supplies S&P dividend, price, and return data, with true annual returns. The historical deflator is the Producer Price Index through 1925, followed by the Consumer Price Index. The switch is part of the published data construction. Replacing the early price convention or the deflator with modern revised series is a legitimate robustness exercise but not an exact replication.

The risk-free proxy is the annual real return on six-month commercial paper rolled at midyear. For the year 2000 the tables use three-month commercial paper. This is a nominal short-term credit instrument, not an inflation-indexed riskless payoff; realized inflation makes its real return uncertain. The paper uses it as the risk-free benchmark conventionally. Replacing it with a one-month Treasury bill raises the 1951–2000 estimated annual equity premium by about one percentage point. Since the same benchmark is subtracted from all three expected-return estimates, this changes their levels but not their differences.

S&P earnings come from Shiller and are updated by Vuolteenaho and the authors. Early earnings data are considered unreliable, so the earnings-growth estimator is reported only for 1951–2000. Book-equity data start in 1925 and are constructed using the Davis–Fama–French files expanded to all NYSE firms. The article does not provide the full historical constituent mapping and aggregation procedure needed to reconstruct the S&P book-value series exactly. It also does not supply the underlying annual data file, adjustment history, or a documented archival source vintage for every series.

For replication, keep nominal lowercase series $p_t,d_t,y_t,b_t$ and the year-end price level $L_t$ separate from the real transformations. Table I specifies

$$
GD_t=\frac{d_t}{d_{t-1}}\frac{L_{t-1}}{L_t}-1,\quad
GY_t=\frac{y_t}{y_{t-1}}\frac{L_{t-1}}{L_t}-1,\quad
GP_t=\frac{p_t}{p_{t-1}}\frac{L_{t-1}}{L_t}-1,
$$

and the real dividend yield

$$
DY_t=\frac{d_t}{p_{t-1}}\frac{L_{t-1}}{L_t}.
$$

Construct $RD_t=DY_t+GD_t$ and $RY_t=DY_t+GY_t$. Subtract the same real commercial-paper return $F_t$ to form $RXD_t$, $RXY_t$, and $RX_t=R_t-F_t$. The subtraction is a difference between realized real rates, not division of two gross returns. Use decimals throughout calculations and multiply by 100 for the tables.

The real income return on book investment is defined differently from merely deflating the earnings numerator:

$$
ROI_t=\left(1+\frac{y_t}{b_{t-1}}\right)\frac{L_{t-1}}{L_t}-1.
$$

This adjusts the nominal gross accounting income return for inflation. The price-ratio variables $d_t/p_t$, $y_t/p_t$, and $b_t/p_t$ need no inflation correction because numerator and denominator have the same nominal units and date convention.

There is no training/validation split, machine-learning tuning, transaction-cost assumption, leverage rule, or portfolio rebalancing signal in the central estimator. All years in each designated subsample contribute to its mean. The later forecasting regressions test an interpretation of the endpoints; they are in-sample diagnostics, not a historical trading simulation.

## Main estimates and precision

Table I reports the following annual real quantities. All entries except ratios are percentage points or percent per year.

| Quantity | 1872–2000 | 1872–1950 | 1951–2000 |
|---|---:|---:|---:|
| Mean dividend yield | 4.70 | 5.34 | 3.70 |
| Mean dividend growth | 2.08 | 2.74 | 1.05 |
| Mean earnings growth | Not used | Not used | 2.82 |
| Mean capital gain | 4.11 | 2.96 | 5.92 |
| Dividend-based return | 6.78 | 8.07 | 4.74 |
| Earnings-based return | Not used | Not used | 6.51 |
| Realized stock return | 8.81 | 8.30 | 9.62 |
| Real commercial-paper return | 3.24 | 3.90 | 2.19 |
| Dividend-based premium | 3.54 | 4.17 | 2.55 |
| Earnings-based premium | Not used | Not used | 4.32 |
| Realized premium | 5.57 | 4.40 | 7.43 |

Minor discrepancies from adding displayed components reflect rounding. Up to 1950, average capital gains and dividend growth are similar, and the two return estimators almost coincide. After 1950, capital gains exceed dividend growth by nearly five annual percentage points. This is the central observed fact; it does not depend on which short-rate proxy is subtracted.

For 1951–2000, annual dividend growth has standard deviation 5.09%, versus 13.79% for earnings growth and 16.77% for capital gains. The resulting dividend-based annual return series has standard deviation 5.21%, earnings-based return 13.51%, and realized return 17.03%. The reported standard errors of their mean returns are 0.74%, 1.93%, and 2.43% respectively. These are errors for **mean returns**, not the standard deviations of investment returns and not the sampling errors of the excess-premium series. The article does not give a separate detailed long-run covariance estimator for these mean standard errors. Do not silently attribute a particular HAC lag convention to them.

The pre-1951 standard errors are much closer: 1.74% for the dividend-based estimate and 2.12% for the realized-return mean. Its annual dividend and capital-gain standard deviations are 15.28% and 18.48%. The precision advantage is therefore sample dependent, not an algebraic property ensuring dividend growth is always the best estimator.

The source compares three Sharpe-like ratios using a **common denominator**, the standard deviation of realized annual stock returns. It does not divide the dividend-based premium by the much smaller volatility of the synthetic $RD_t$ series. For 1872–1950 the dividend-based and realized ratios are 0.22 and 0.23. For 1951–2000 they are 0.15 and 0.44, while the earnings-based ratio is 0.25. The comparison asks whether the expected compensation per unit of the same actual equity risk changed markedly. It is not evidence of a tradable low-volatility dividend-growth portfolio.

The authors view stable fundamental-based ratios as more plausible than a near doubling of the realized-return ratio. Relating this to aggregate risk aversion requires an asset-pricing model and assumptions about the relevant risk exposures; a Sharpe ratio alone does not identify a structural preference parameter. The stability argument supports their interpretation but is not a statistical rejection of every explanation of changing risk premia.

## The profitability and valuation consistency check

During 1951–2000 the average book-to-market ratio is 0.66; it exceeds one in only six years and never exceeds 1.12. Market equity is usually valued above recorded book equity. The authors interpret this as evidence that typical investment earns more than its cost of capital. Under their simplifying constant-expected-earnings investment example, the accounting income return on book equity estimates the economic investment return without bias for an infinite-lived investment and with upward bias for finite life.

The average real accounting income return is 7.60%. It is above the dividend- and earnings-based return estimates, 4.74% and 6.51%, but below the realized stock-return mean, 9.62%. Taking 9.62% literally as the cost of equity would imply a typical investment return below the hurdle rate, which is difficult to reconcile with persistently high market-to-book valuations. This is a second diagnostic independent of simply observing low dividend yields.

The test rests on the relationship between accounting book capital, income recognition, economic capital, and investment duration. It is not a universal inequality for firms with intangible assets, nonconstant expected earnings, or arbitrary accounting conventions. The paper supplies a stylized valuation argument rather than estimating a full firm-level capital-budgeting model. Its force is comparative: the lower return estimates line up more comfortably with the observed aggregate valuations and profitability.

## Why the authors attribute the return gap to discount-rate news

Three mechanisms could produce unexpectedly high realized returns: unexpectedly high in-sample cash-flow growth, higher expected cash-flow growth after the endpoint, or lower expected future returns at the endpoint. Unexpected in-sample growth cannot by itself explain the gap between the three estimators, because it enters prices and the observed fundamental-growth estimators alike. If the starting and ending valuation ratios were identical, cumulative price and fundamental growth would be identical regardless of whether the growth had been anticipated.

This observation does not solve US-market survivorship bias. A country that survives wars, financial crises, and potential market destruction can have unusually high realized cash-flow growth; fundamental-growth estimators share that bias. The paper's narrower question is why price growth so substantially exceeded fundamental growth in the surviving US sample. It does not establish that its premium estimates apply unchanged to countries that suffered market closure or expropriation.

To investigate unusually high future growth, Table III estimates annual forecasting regressions. For one-year-ahead dividend growth, use lagged payout ratio $d_{t-1}/y_{t-1}$, lagged dividend–price ratio, three lags of dividend growth, three lags of real stock return, and an intercept. The earlier regression covers 1875–1950, 76 years; the later covers 1951–2000, 50 years. For a two-year-ahead forecast of the same one-year growth outcome $GD_t$, move the information set back to $t-2$: use payout and dividend–price ratios at $t-2$, growth at $t-2,t-3$, and returns at $t-2,t-3$. This is **not** a regression of cumulative two-year growth on current predictors.

The earlier one-year dividend regression has adjusted $R^2=0.38$, falling to 0.07 with two-year-old information. After 1950 the adjusted $R^2$ values are 0.01 and −0.05. The first lag of returns remains positive in the one-year postwar regression, coefficient 0.11 with $t=2.17$, but the remaining overall forecast power is negligible. Additional three-year-ahead results are described as showing no forecast power but are not tabulated. Thus the historical dividend-growth mean is the authors' preferred long-term forecast given these predictors; the tests do not prove no other information could forecast growth.

For one-year earnings growth, add lagged real accounting income return $Y_{t-1}/B_{t-2}$, payout ratio, earnings–price ratio, three earnings-growth lags, and three stock-return lags. The two-year version uses $t-2$ accounting information and ratios, plus growth and return lags $t-2,t-3$. All variables except payout ratio are in percent in Table III. The regressions have 50 annual observations and many coefficients; the article does not specify a holdout, pre-registration, shrinkage, or an alternative small-sample inference method.

Earnings are more predictable at short horizons: adjusted $R^2$ is 0.40 for one year and 0.23 for two years. But the patterns indicate reversal. Return lag one has coefficient 0.28 with $t=2.39$, while lag two is −0.25 with $t=-2.18$. Earnings-growth lag three is −0.31 with $t=-2.64$ in the one-year model. The earnings–price coefficient is −1.36 with $t=-1.91$ at one year and loses strength at two years. Therefore the high 1991–2000 mean earnings growth of 7.58% is not compelling evidence of permanently higher future growth. The preceding decade averaged only 0.37%, and ten-year mean earnings-growth standard errors are around five percentage points.

Figure 1 and Section II.C show the endpoint valuation changes. Dividend–price falls from 7.18% in 1950 to 1.22% in 2000; earnings–price falls from 13.39% to 3.46%. Consequently, the **gross growth factor** for price is 5.89 times the dividend growth factor and 3.87 times the earnings growth factor. These are ratios such as $(P_{2000}/P_{1950})/(D_{2000}/D_{1950})$, not ratios of net percentage gains after subtracting one. The earnings–price ratio was still 13.40% in 1979, so much of that repricing occurred in the last two decades.

Some valuation decline could have been anticipated from unusually high initial ratios. Using the historical average dividend–price ratio of 4.64% as a stylized 1950 forecast of its 2000 value, the final price is $4.64/1.22=3.80$ times the counterfactual price. The annualized log contribution is approximately $\log(3.80)/50=2.67%$. Using the average earnings–price ratio 7.14% gives $7.14/3.46=2.06$ and about 1.45% annually. These calculations are retrospective illustrations using realized full-sample means, not forecasts estimated with the actual 1950 information set. They support the size of the possible unexpected repricing component without identifying every discount-rate shock separately.

## Arithmetic-return correction and long-horizon caveats

Equal long-run log growth can coexist with unequal simple-growth means because volatility increases the arithmetic mean for a given geometric growth rate. To second order, the paper corrects a fundamental-based expected **annual simple** return by adding half the difference between capital-gain variance and fundamental-growth variance:

$$
\widehat\mu_D^{annual}\simeq\widehat\mu_D+\frac12(s_{GP}^2-s_{GD}^2),\qquad
\widehat\mu_Y^{annual}\simeq\widehat\mu_Y+\frac12(s_{GP}^2-s_{GY}^2).
$$

Use decimal standard deviations before squaring. For dividends, $\tfrac12(0.1677^2-0.0509^2)\approx0.0128$, or 1.28 percentage points per year. For earnings the correction is approximately 0.46 percentage points. These are approximations, not exact corrections for arbitrary non-Gaussian distributions; higher moments and the full joint process can matter.

Table IV also reports a different correction intended for long-horizon expected wealth. It treats unpredictable dividend growth as the more permanent component and subtracts half the excess variance of earnings growth or capital gains relative to dividends. The three columns must not be conflated:

| Premium estimator, 1951–2000 | Unadjusted | Annual simple-return adjustment | Published long-term adjustment |
|---|---:|---:|---:|
| Dividend growth | 2.55% | 3.83% | 2.55% |
| Earnings growth | 4.32% | 4.78% | 3.50% |
| Realized stock returns | 7.43% | 7.43% | 6.16% |

For earnings the long-term adjustment subtracts about 0.82 percentage points, half the variance difference between earnings and dividend growth. The authors argue that transitory price and earnings fluctuations make compounding their unconditional arithmetic means overstate long-term expected wealth. Estimation uncertainty adds a separate effect: compounding a noisy estimated mean is a convex transformation and creates upward bias relative to compounding the true mean.

The equalities printed as equations (5)–(7) require stronger assumptions than the brief exposition establishes. Zero pairwise serial correlation alone does not ensure $E[\prod_t(1+GD_t)]=[1+E(GD)]^T$; independence or a suitable constant conditional mean relative to the full past is sufficient. Nor does stationarity of $D/P$ imply exact equality of finite-horizon expected compounded price and dividend growth. The pathwise identity contains the random endpoint multiplier $q_0/q_T$, potentially correlated with dividend growth. Stationarity can make its contribution to average log growth vanish without making its effect on the expectation of terminal wealth vanish.

Reinvested dividends introduce another dependence: the exact total-wealth product includes the changing dividend yield, so equal growth rates of price and dividends do not by themselves establish equation (7). Accordingly, the note reports Table IV as the authors' approximate long-horizon adjustment, not a general proof of an unbiased terminal-wealth estimator. A rigorous extension would specify the joint process for growth, valuation ratios, and reinvestment and compute the relevant multi-period expectation. Expected terminal wealth, expected log wealth, and a typical compound growth rate are different objectives.

## Payout policy, uncertainty, and the implementable conclusion

Repurchases rise after 1983 and the fraction of dividend-paying firms declines after 1978. A sustained switch away from dividends can lower $D/P$ and observed dividend growth even without a lower expected return. The dividend model can then underestimate expected returns during the transition. Eventual stabilization and renewed mean reversion would improve its long-run justification, but the postwar sample may include a long transition. The earnings model avoids this particular payout substitution channel under stationary earnings–price ratios, at the cost of substantially greater sampling noise. The authors do not resolve the tradeoff by simply declaring one estimator uniformly superior.

The published text references an on-request appendix with regime-shift and repurchase examples. The inspected [author research page](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/working_papers.html) describes an earlier July 2000 draft with a different sample endpoint and does not expose that appendix. No claims about its uninspected derivations are made here. The final published article's assumptions and transition qualifications remain the evidentiary basis for this note.

A useful replication would first reconstruct annual nominal inputs and their original date conventions, verify all real transformations, reproduce Table I means and dispersion, then reproduce Table III's lag sets and Table IV's variance adjustments. The point is to obtain consistent answers to well-defined targets before experimenting with different deflators, risk-free rates, current data, or payout measures. In particular, a total-payout extension requires coherent treatment of issuance and repurchases rather than adding a repurchase yield to an unchanged per-share growth series.

The article's main conclusion is supported by several mutually reinforcing historical comparisons: fundamental growth was slower than price growth, fundamental-based estimates were more precise after 1950, profitability and book valuations fit those lower costs of equity more comfortably, and the chosen predictors gave little evidence of exceptional long-term cash-flow growth in 2000. None identifies a unique permanent equity premium. Their common implication is that a favorable realized repricing should be separated from the return investors could reasonably have expected before it occurred. That is the research contribution to carry into cost-of-capital estimation and long-horizon planning.

# Evaporating Liquidity

Stefan Nagel. December 2011 manuscript. Source: [Liquidity_Nagel_2012.pdf](../../Finance/Liquidity_Nagel_2012.pdf). The filename uses 2012, but the title page identifies the version summarized here as December 2011. The complete 56-page PDF includes Appendices A–C, five additional empirical tables, and references. Page numbers below are manuscript pages, one less than PDF page numbers.

## Why this matters and what the paper contributes

When liquidity disappears, prices can become harder to trade because adverse selection increases, because customers demand more immediacy, or because intermediaries reduce the capacity they supply. Conventional spreads and price-impact measures combine these forces. Nagel instead studies short-horizon reversal strategies as proxies for the compensation earned by liquidity providers. The distinction matters: a larger spread caused entirely by better-informed counterparties need not make liquidity provision more profitable.

The paper first derives a model linking reversal returns to inventory compensation. It then shows that returns from these strategies are strongly predictable using lagged VIX, especially during financial turmoil. The rise in expected return exceeds the rise in conditional volatility, so estimated conditional Sharpe ratios rise too. Even reversals across industry portfolios, weak on average, become profitable in high-VIX periods. These findings are consistent with a contraction in liquidity supply and a higher required reward for absorbing order imbalances.

The result is a measurement and prediction claim, not a randomized identification of intermediary funding constraints. VIX is a state proxy, and risk, funding, customer demand, and intermediary willingness to trade are correlated. Moreover, the reported returns assume favorable liquidity-provider execution conventions and omit major operating and trading costs. Their very high unconditional Sharpe ratios should not be interpreted as the performance available to an ordinary trader submitting market orders.

## The model: temporary inventory pressure versus information

There is one risky asset in zero net supply, a riskless asset with zero interest, and discrete trading dates. The terminal asset value accumulates public innovations $\xi_t$ and innovations $\delta_t$ that become public at time $t$ but are observed by informed traders one period earlier. Liquidity traders create exogenous demand $z_t$. These three innovations are jointly normal, mutually uncorrelated, and independent over time, with variances $\sigma_\xi^2$, $\sigma_\delta^2$, and $\sigma_z^2$.

Informed traders are competitive, myopic, and have CARA utility. Their orders cannot condition on the current execution price. If their signal is $s_t=\delta_{t+1}$, aggregate informed demand is $y_t=\beta s_t$. Total demand absorbed by market makers is $x_t=y_t+z_t$, and market-maker inventory is $-x_t$.

The representative market maker has linear asset demand

$$
m_t=\gamma\left(E[\delta_{t+1}\mid\mathcal M_t]+v_t-P_t\right).
$$

Here $\gamma$ is the aggressiveness of liquidity supply, not a risk-aversion coefficient: larger $\gamma$ means greater willingness to hold inventory. It summarizes risk-bearing capacity and potentially funding or risk-management constraints. Those constraints are not solved structurally in this model. The market maker infers information from order imbalance:

$$
E[\delta_{t+1}\mid\mathcal M_t]=\phi x_t,
\qquad
\phi=\frac{\beta\sigma_\delta^2}{\beta^2\sigma_\delta^2+\sigma_z^2}.
$$

Market clearing, $m_t+x_t=0$, produces

$$
P_t=v_t+(\gamma^{-1}+\phi)x_t.
$$

The appendix also characterizes informed demand through

$$
\beta=\frac{\widetilde\beta}{1+\widetilde\beta(\gamma^{-1}+\phi)},
$$

where $\widetilde\beta$ represents aggregate informed risk-bearing capacity relative to perceived payoff risk. This equation and the formula for $\phi$ must be solved jointly; treating both $\beta$ and $\phi$ as unrelated primitive parameters would miss the information-demand feedback.

Let $\eta_{t+1}=\delta_{t+1}-\phi x_t$ be the part of next period's informed news not inferred by market makers. Dollar price changes obey

$$
R_{t+1}=\xi_{t+1}+\eta_{t+1}+(\gamma^{-1}+\phi)x_{t+1}-\gamma^{-1}x_t.
$$

The first three terms are unpredictable using current market-maker information. The last term reverses inventory-related price pressure. Information incorporated in $\phi x_t$ is permanent once confirmed; it does not produce the same compensating reversal. If liquidity providers are holding positive inventory, $x_t<0$, expected next-period returns are positive.

The distinction depends on this model's short-lived information and stationary inventory structure. More persistent private information, delayed public-information diffusion, or different inventory dynamics can produce continuation as well as reversal. The empirical five-lag construction partly addresses such complications but does not prove that every observed reversal is an inventory premium.

## A return per unit of liquidity-provider capital

Extend the model to many securities with cross-sectionally independent informed and liquidity shocks. Public news has a common factor plus an idiosyncratic component, with identical factor loadings in the simplifying model. Normalize prices to one at the formation date and assume 50-percent margins on both long and short positions. Aggregate market-maker return per dollar of margin capital is

$$
L_t^{MM}=-\frac{\sum_i x_{i,t-1}R_{it}}{\tfrac12\sum_i|x_{i,t-1}|}.
$$

As the number of securities grows,

$$
L_t^{MM}\longrightarrow\sqrt{2\pi}\,\gamma^{-1}\sigma_x,
\qquad \sigma_x^2=\beta^2\sigma_\delta^2+\sigma_z^2.
$$

Appendix A obtains the denominator from the mean absolute value of a normal random variable and the numerator from inventory's covariance with the subsequent reversal. The expression rises when supply becomes less aggressive or order-imbalance dispersion increases. It therefore does not by itself identify whether a higher observed return comes from reduced supply or increased demand.

The large-cross-section return is constant only because the model assumes independent inventory shocks and identical common-factor exposures. Real market makers specialize, have heterogeneous factor exposures, and face common order-flow shocks. The paper acknowledges that those features leave nondiversifiable risk and could help endogenize the finite $\gamma$. A simulation reproducing the law-of-large-numbers result must retain its independence assumptions rather than interpret the constant as a general absence of liquidity-provider risk.

Inventories for all designated and de facto liquidity providers are unavailable. The empirical proxy therefore substitutes lagged market-adjusted returns. Define $q_{it}=R_{it}-\bar R_t$, with $\bar R_t$ the equally weighted return across the relevant assets. The one-lag reversal weights are

$$
w_{it}^{(1)}=-\frac{q_{i,t-1}}{\tfrac12\sum_j|q_{j,t-1}|}.
$$

Because the cross-sectional mean has been removed, weights sum to zero and absolute weights sum to two: the portfolio is \$1 long and \$1 short. Under the stated margin convention, that requires \$1 of capital. The strategy return is $L_t^R=\sum_iw_{it}^{(1)}R_{it}$.

Under the model assumptions,

$$
L_t^R\longrightarrow\rho\sqrt{2\pi}\,\gamma^{-1}\sigma_x,
\qquad
\rho=\frac{(\gamma^{-1}+\phi)\sigma_x}{\sigma_R},
$$

where $\sigma_R$ is cross-sectional return dispersion after the common component is removed. Lagged returns contain public-information noise in addition to inventory information. The proxy consequently uses capital on positions that do not track inventory perfectly; $\rho$ captures that attenuation. Time-varying $\rho$ is an important threat to interpreting changing reversal returns as changing market-maker compensation.

## Alternative normalizations and their purpose

The paper studies two alternatives to distinguish inventory compensation from changes in the noisiness or informativeness of returns. Weights $w_{it}=-q_{i,t-1}/N$ produce a payoff equal to the negative cross-sectional autocovariance, whose model value is $(\gamma^{-1}+\phi)\gamma^{-1}\sigma_x^2$. This does not depend on public-information variance through the capital denominator. It does not maintain the same fixed gross exposure as the main portfolio.

Weights $w_{it}=-q_{i,t-1}/\sum_jq_{j,t-1}^2$ instead produce a negative cross-sectional regression slope, or autocorrelation-like statistic. Its sensitivity to the information coefficient can differ from that of the fixed-exposure strategy. Holding the quantities specified in the comparative static fixed, the main strategy's elasticity with respect to $\phi$ is

$$
\frac{\phi}{\gamma^{-1}+\phi}(1-\rho^2),
$$

whereas the squared-return-normalized strategy has elasticity

$$
\frac{\phi}{\gamma^{-1}+\phi}(1-2\rho^2).
$$

The latter may fall when information becomes more important if $\rho^2>1/2$. Predictability that survives both alternatives is harder to explain solely by a changing public-news noise share or by changing information sensitivity. These are robustness diagnostics with different payoff units; their coefficients should not be compared as identical returns on a dollar of invested capital.

## Data, filters, and daily strategy construction

The main sample runs from January 1998 through December 2010. CRSP daily data cover NYSE, AMEX, and Nasdaq common shares with share codes 10 or 11. A stock must have a closing price of at least \$1 on the last trading day of the previous calendar month. The start date avoids Nasdaq's major 1997 order-handling transition; the analysis controls separately for the 2001 move to decimal pricing.

Two price definitions are used. Transaction returns use daily closing transactions, substituting a quote midpoint where no closing transaction price is available. Quote-midpoint returns use closing bid and ask quotes, adjusted for splits and dividends using CRSP information, and are available here for Nasdaq stocks only. Data-error screens require bid divided by midpoint to be at least 0.5, and midpoint return minus transaction return to lie between $-50$ and $100$ percent. These wide screens address occasional recording errors, not ordinary spread or volatility variation.

For each day $t$, construct five separate portfolios using market-adjusted returns on days $t-1$ through $t-5$. Normalize each subportfolio separately with the absolute-return denominator, compute each one's day-$t$ payoff, and average the five payoffs:

$$
L_t^R=\frac15\sum_{\ell=1}^5\sum_iw_{it}^{(\ell)}R_{it},
\qquad
w_{it}^{(\ell)}=-\frac{q_{i,t-\ell}}{\tfrac12\sum_j|q_{j,t-\ell}|}.
$$

This is not the same as forming one signal from the sum of five past returns and normalizing once. Offsetting subportfolio positions can also reduce the gross exposure of the combined overlay below the sum of their separate gross exposures. The paper reports the average-substrategy convention; a capital-efficient netted implementation is a different exercise.

Use the same price definition for formation and realization: midpoint signals forecast midpoint returns, transaction signals forecast transaction returns. Mixing them changes the bid–ask-bounce component. A separate version trades 48 industry portfolios, using the Fama–French industry classification and value weighting within industries. Reversal is then applied across those industry returns. This tests compensation for absorbing correlated sector-level imbalances rather than only individual-stock noise.

The source gives the principal screens but not executable treatment of every missing observation, delisting, classification update, or portfolio membership change across the five lags. A replication should document these details and verify that formation and payoff universes are aligned. Dropping securities using future availability would introduce a different experiment.

## Hedging the mechanically changing market exposure

A reversal portfolio tends to short high-beta stocks after a market rise and buy them after a decline. Its market beta therefore varies predictably even if its unconditional beta is small. Nagel estimates

$$
L_t^R=\beta_0+\beta_1f_t+\beta_2f_t\operatorname{sgn}(f_{t-1})+\epsilon_t,
$$

where $f_t$ is the CRSP value-weighted index return. Hedged returns subtract $[\widehat\beta_1+\widehat\beta_2\operatorname{sgn}(f_{t-1})]f_t$, retaining the intercept and the residual component. They do not simply remove the whole fitted regression or subtract an unconditional market beta.

Most subsequent results use these hedged returns. The paper does not prescribe a rolling real-time hedge-estimation window. Thus the hedge is a statistical exposure adjustment; exact replication of the historical tables should be distinguished from a deployable hedge estimated using only prior data. The later out-of-sample exercise concerns predictive-regression coefficients and is not a complete certification that every data-processing stage was estimated out of sample.

## Return levels and the execution interpretation

Table 1, p. 20, reports the following hedged statistics:

| Statistic | Individual stocks, transactions | Individual stocks, Nasdaq midpoints | Industry portfolios |
|---|---:|---:|---:|
| Mean, percent per day | 0.29 | 0.17 | 0.01 |
| Standard deviation, percent per day | 0.48 | 0.54 | 0.47 |
| Skewness | 2.45 | 2.26 | 0.88 |
| Worst day, percent | -2.26 | -3.92 | -3.12 |
| Worst three-month return, percent | 2.27 | -1.28 | -7.87 |
| Annualized Sharpe ratio | 9.58 | 4.91 | 0.44 |

The extreme Sharpe ratios are a warning about interpretation, not an invitation to assume a nearly riskless strategy. Transaction-price calculations represent a hypothetical liquidity supplier whose quotes or limit orders execute at the observed closing prices. An outside investor cannot automatically obtain those fills with those quantities. Midpoint execution is also not freely available, and the midpoint and transaction samples differ by exchange coverage. Their return gap consequently cannot be treated as a perfectly controlled estimate of spreads alone.

The paper argues that fixed technological and access costs restrict entry into liquidity provision. It does not estimate a full fee, borrow, queue-position, fill-probability, latency, or market-impact model. The positive historical skewness and positive worst three-month transaction return describe this sample before those costs; they do not establish an absence of tail risk outside the sample or for a leveraged executable implementation.

## The predictive regression and its numerical meaning

The main daily regression is

$$
L_t^R=a+b\,VIX^d_{t-5}+c^\top g_{t-5}+e_t,
\qquad VIX^d=VIX/\sqrt{250}.
$$

VIX is in percentage points, normalized to a daily volatility scale. The five-day lag places the predictor no later than the oldest formation return used in the overlay. Controls include an indicator for dates before April 9, 2001 and the preceding four-week return on the CRSP value-weighted index ending at $t-5$. Standard errors are Newey–West with twenty lags for daily regressions and three for monthly regressions.

Monthly dependent variables are **averages of daily strategy returns within the month**, not compounded monthly investment returns. Predictors are measured five trading days before the preceding month-end. Preserving this timing and dependent-variable scale is necessary to reproduce the similar daily and monthly slope magnitudes.

Table 2, p. 23, gives these VIX slopes:

| Regression | Transactions | Midpoints | Industries |
|---|---:|---:|---:|
| Daily, VIX alone | 0.22 (0.02) | 0.16 (0.02) | 0.07 (0.02) |
| Daily, with decimalization and market-return controls | 0.18 (0.02) | 0.13 (0.02) | 0.05 (0.02) |
| Monthly average, with controls | 0.15 (0.01) | 0.10 (0.03) | 0.04 (0.01) |

Parentheses contain standard errors. A one-point increase in normalized VIX corresponds to about 15.81 points of ordinary annualized VIX. In the first transaction specification, it predicts 0.22 percentage point more daily return. Equivalently, a ten-point increase in ordinary VIX corresponds to about 0.139 percentage point more daily return under that fitted specification; this conversion is arithmetic from the reported slope.

Daily adjusted $R^2$ is 0.07 for transaction returns with VIX alone and 0.11 with both controls. In the monthly regressions it is 0.56, 0.25, and 0.07 for transactions, midpoints, and industries respectively. The large monthly fit reflects persistent variation in average daily profitability; it should not be read as explaining 56 percent of individual daily return variance.

Figure 2 estimates the VIX-only predictive coefficients using observations through June 2007 and then holds those coefficients fixed. Conditional on the subsequently observed VIX path, the predictions track much of the crisis rise in reversal returns. Midpoint profits at the crisis peak are underpredicted, and industry predictions are visibly less accurate. These are useful out-of-sample coefficient checks, but the plotted three-month averages smooth daily errors and the experiment does not forecast the VIX path itself. No comprehensive out-of-sample forecasting loss table or cost-adjusted trading evaluation accompanies the figure.

## Conditional Sharpe ratios

To distinguish higher compensation from merely higher volatility, the paper writes the conditional mean as $E[L_t^R\mid VIX_{t-5}]=\sigma_t\theta_t$, and assumes both conditional standard deviation $\sigma_t$ and daily Sharpe ratio $\theta_t$ are linear in lagged normalized VIX and the decimalization dummy.

First regress returns on those predictors and obtain residuals $\widetilde L_t$. Define

$$
\kappa=\frac{\sqrt{T^{-1}\sum_t\widetilde L_t^2}}{T^{-1}\sum_t|\widetilde L_t|}.
$$

Regress $\kappa|\widetilde L_t|$ on VIX and the dummy; fitted values estimate $\sigma_t$. Then regress $L_t^R/\widehat\sigma_t$ on the same predictors. This is an absolute-residual scale model, not a GARCH fit to strategy returns. The empirical $\kappa$ calibrates unconditional RMS residuals to mean absolute residuals; under a zero-mean normal distribution its population counterpart is $\sqrt{\pi/2}$.

Table 3 reports VIX slopes of 0.13 with standard error 0.03 for both individual-stock versions, and 0.08 with standard error 0.02 for industries. The daily intercepts are 0.33, 0.10, and $-0.12$, respectively. Multiplying both daily Sharpe ratio and normalized VIX by $\sqrt{250}$ means the slope also measures the change in annualized Sharpe per percentage point of ordinary VIX. This equality depends on the stated scaling; multiplying the slope by $\sqrt{250}$ again would be an error.

The fitted conditional expected transaction return rises almost tenfold between precrisis conditions and late 2008, while its conditional Sharpe roughly doubles. Figure 3 sets the decimalization dummy to zero throughout to isolate VIX-related variation. The scale model is estimated from the sample and does not guarantee positive fitted standard deviations under arbitrary extrapolation. The source reports HAC inference but does not describe a bootstrap accounting for every generated-scale estimation step.

## What VIX may represent

Table 4 decomposes VIX into a physical-volatility forecast $\sigma_M$ and the difference $VIX-\sigma_M$. The forecast is obtained from a GARCH(1,1) estimated on daily S&P 500 returns over the full 1998–2010 sample and projected over 21 trading days, with matching volatility units. This is a **volatility difference**, not literally the variance premium $VIX^2-E[RV]$; the prose uses both volatility- and variance-premium language, but the implemented regression variable is the difference of standard deviations.

In the daily transaction specification with the decimalization control, coefficients are 0.18 (0.04) on the volatility difference and 0.21 (0.02) on expected volatility. For midpoints they are 0.07 (0.05) and 0.17 (0.03), indicating weaker evidence for the premium component there. Industries similarly load more clearly on expected volatility. An alternative uses monthly realized variance formed from squared five-minute S&P 500 returns, forecast by ARMA(1,1). That sample ends in February 2010. Both forecasting models are estimated in sample, and model forecast errors can contaminate the supposedly separate premium component.

Table 5 considers cross-sectional return dispersion, the three-month Eurodollar–Treasury spread, and thirteen-week primary-dealer repo growth. In separate transaction-return regressions, higher dispersion and a higher TED spread predict higher reversal returns, while repo growth predicts lower returns. Their reported coefficients are 8.80 (1.20), 12.08 (2.87), and $-0.71$ (0.27), respectively, using the source's predictor scales. Those magnitudes should not be converted into percentage-point effects without matching the underlying input units.

Jointly with the other variables, VIX remains significant for transactions at 0.12 (0.02). The midpoint coefficient is 0.05 (0.03), a much weaker result, and most other coefficients shrink. There is an unresolved construction discrepancy: the main text describes idiosyncratic volatility using the preceding month's cross-sectional dispersion, while Table 5's caption describes dispersion on day $t-5$. A reproducible implementation should report both variants or obtain the original code, rather than silently select one.

## Heterogeneity, appendix checks, and remaining limits

Monthly decile sorts use lagged capitalization, the previous month's average absolute-return/dollar-volume ratio, or previous-month daily return volatility. Illiquidity rankings are formed separately for Nasdaq and NYSE/AMEX because volume conventions differ. Within each subgroup, reversal returns are regressed on VIX and the decimalization indicator, and predictions are evaluated at the fifth and ninety-fifth VIX percentiles with the indicator set to zero.

Figure 4 shows particularly large high-VIX returns for small, illiquid, and volatile stocks. Yet even large, liquid, low-volatility groups earn around 0.1 percent per day under high VIX, while their low-VIX fitted returns are near zero. The figure's plotted legend identifies crosses as low VIX and circles as high VIX, contrary to a sentence in the narrative; the plotted values and legend make the intended comparison clear. Confidence intervals reflect the regression, not uncertainty about executable fills or causal attribution.

Appendix C finds negligible Stambaugh-style predictive bias because VIX innovations are almost uncorrelated with contemporaneous reversal-return innovations. This is specific to these return series; persistence alone does not determine bias. One-lag strategies preserve individual-stock predictability but weaken the industry result: Table A.1's industry VIX slope is 0.01 (0.05) without controls. The five-lag overlay is therefore substantively important for industry inference.

Alternative autocorrelation and autocovariance normalizations retain predictability. Capitalization-weighted signals also retain it: Table A.4 reports daily VIX-only slopes of 0.20 (0.03) for transactions and 0.25 (0.04) for midpoints. Its printed weighting expression multiplies market-adjusted returns by capitalization; an implementation must specify the market-centering convention because equal-weight centering no longer automatically guarantees dollar neutrality after capitalization weighting. The appendix does not fully resolve that convention.

Finally, splitting long and short sides and offsetting each with the equal-weight market gives broadly similar individual-stock results. Industry reversals are more concentrated on the long side: monthly VIX slopes are 0.04 for the long component and approximately zero for the short component in Table A.5. This is consistent with sector-level selling pressure, though it does not uniquely identify its source.

The paper's strongest conclusion is predictable time variation in a carefully defined proxy for liquidity-provision compensation. A faithful reconstruction should match the daily data filters, five separate lagged portfolios, execution-price conventions, conditional hedge, predictor timing, monthly averaging, and HAC settings before interpreting its regression slopes. A tradable extension additionally requires actual fill assumptions, financing and borrow costs, capacity, netting, and point-in-time parameter estimation. Those missing inputs are central to converting an economically informative liquidity measure into an investment result.

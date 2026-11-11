# What Do We Learn from the Price of Crude Oil Futures?

Ron Alquist and Lutz Kilian, *Journal of Applied Econometrics* 25 (2010), pp. 539–573, published online 24 February 2010, DOI: 10.1002/jae.1159. [Source PDF](../../Finance/futures/CrudeOilFutures_AlquistKillian.pdf). The supplied article is 35 pages; PDF page $j$ corresponds to printed page $538+j$. This note covers the complete article, its nine numbered tables and seven figures. There is no separate appendix in the supplied PDF.

## Why this matters

A traded futures quote is an observable market price, but using it as a statistical forecast of future spot requires additional assumptions. For oil, the value of having physical stocks available can change sharply even when the expected long-run supply level does not. The basis can therefore contain information about inventory insurance and market conditions that is different from information useful for minimizing spot-price forecast error.

The paper contributes a carefully constructed end-of-month WTI futures dataset, a real-time forecast comparison across five maturities, and a model linking uncertainty about future oil availability to convenience yields, inventories, spot prices, and futures spreads. Its empirical message is conditional and historically specific: over the reported 1991–2007 evaluation, a no-change forecast usually ranks better than futures-based forecasts, although the superiority over the raw futures quote is not statistically significant. Its economic message is that the negative futures spread can indicate precautionary demand under specific supply and convenience-yield assumptions. The indicator's divergence from an alternative measure after 2003 is part of the result, not a footnote to omit.

For quantitative work, this paper is useful both as a forecast-benchmark design and as a warning against assigning one economic meaning to every movement in the forward curve. It does not establish that futures prices are intrinsically inefficient, that the spot price is the true conditional expectation, or that the basis alone identifies a structural demand shock.

## Data and the maturity-matching rule

Daily NYMEX light sweet crude futures prices come from Price-Data.com, beginning 30 March 1983 and ending 28 February 2007. The physical delivery location is Cushing, Oklahoma. Daily WTI cash prices for Cushing come from Datastream. The analysis uses nominal end-of-month prices and horizons $h=1,3,6,9,12$ months.

The authors identify the $h$-month contract trading closest to the month's last trading day, using a backward-looking window of at most five days; for horizons through three months the maximum window is three days. This constructs a continuous monthly series at the desired contract maturity without replacing a missing maturity with another contract. It also limits, but does not eliminate, timestamp differences between spot and futures. The source describes the exchange's expiration convention as trading ending four days before the relevant 25th calendar day, with a business-day adjustment. Exact replication requires the historical contract calendar and the original daily files; one should not substitute a generic continuous front-month series.

Figure 1 shows spot and several maturities moving together in levels, with persistent differences during episodes of backwardation or contango. Figure 2 plots volume by maturity. Activity is heavily concentrated at short horizons, with much thinner long-dated contracts even after contracts beyond one year become available. The authors consequently stop the forecast exercise at twelve months. The volume plot supports a historical liquidity concern; it does not prove that a low-volume quote contains no information, and it is not evidence about today's oil market.

The forecast evaluation is labeled January 1991–February 2007. The initial recursive estimation window is April 1983–December 1990, except that six-month futures regressions begin in October 1983, nine-month regressions in December 1986, and twelve-month regressions in January 1989. The short initial history at the longest maturity is especially relevant to estimation variance. A real-time recreation must use only regression outcomes already realized by each forecast origin. The article does not supply code resolving every origin-versus-target endpoint convention or every historical quote gap, so those details must be recorded explicitly in a replication rather than inferred from the table label alone.

## Forecasts and objectives

Let $S_t$ denote the current spot price and $F_t^{(h)}$ the current quote for delivery $h$ periods ahead. Let $s_t=\log S_t$, $f_t^{(h)}=\log F_t^{(h)}$, and $x_t^{(h)}=f_t^{(h)}-s_t$. The benchmark is the random walk without drift,

$$
\widehat S_{t+h\mid t}=S_t.
$$

The raw futures forecast is $\widehat S_{t+h\mid t}=F_t^{(h)}$. Four spread forecasts use

$$
\widehat S_{t+h\mid t}=S_t[1+\widehat\alpha_h+\widehat\beta_h x_t^{(h)}],
$$

with both coefficients estimated recursively, only the intercept estimated and slope fixed at one, only the slope estimated and intercept fixed at zero, or both restrictions imposed. Their regression motivation is the relation between the future log spot change and the current log basis. The level reconstruction $1+\widehat{\Delta s}$ is a linear approximation. It differs from exponentiating a fitted log change and from a lognormal conditional-mean correction; silently replacing it would produce a different forecasting model.

Other candidates are a recursively estimated drift, rolling local drifts based on trailing windows of 1, 3, 6, 9, or 12 months, a Hotelling-style interest-rate forecast, and professional surveys. The printed rolling-drift forecast is $S_t[1+\overline{\Delta s}_t^{(l)}]$ for every horizon, with the trailing quantity described as a geometric average of monthly percentage changes. The accompanying endpoint wording and the absence of an explicit horizon multiplier leave an implementation ambiguity. The source formula should not be silently converted to an $h$-fold compounded trend. The Hotelling candidate is $S_t(1+i_{t,h})$ for $h=3,6,12$, using matching Treasury-bill maturities and compatible horizon-rate units.

Consensus Economics provides the arithmetic mean of private forecasts for WTI at three and twelve months. The available survey series runs October 1989–February 2007; the respondent pool changes from more than 100 firms initially to roughly 70. The paper also has survey minima, maxima, and standard deviations, but uses the mean for this test. Publication timing and the difference between survey collection and end-of-month futures timing would need to be checked in an exact recreation.

The primary objective is nominal-price mean squared prediction error. The authors also report average signed error, mean absolute prediction error, and directional accuracy. Here “MAPE” means **mean absolute prediction error**, not mean absolute percentage error. The benchmark MSPE is in squared dollars per barrel; benchmark absolute error and bias are in dollars per barrel. Other models' MSPE and MAPE columns are ratios to the no-change benchmark. Bias is actual minus forecast, so a positive value means average underprediction.

For forecasts without estimated parameters, comparisons use Diebold–Mariano tests. Nested estimated models use Clark–West procedures, with normal or bootstrap critical values as specified in Table I: rolling drift under squared loss uses normal critical values, while recursive squared-loss comparisons and absolute-loss comparisons use the stated bootstrap approach. Direction tests use Pesaran–Timmermann. Overlapping horizons require appropriate serial-dependence treatment; the source does not reproduce all bandwidth, bootstrap, and finite-sample implementation choices from the cited methods. The many horizon/model comparisons are not adjusted for the full extent of specification search.

## Forecast accuracy: numerical results and uncertainty

The first two rows of Tables I–V supply the central comparison.

| Horizon, months | No-change MSPE | Futures/no-change MSPE | No-change absolute error | Futures/no-change absolute error | Bias: no-change / futures |
|---|---:|---:|---:|---:|---:|
| 1 | 6.998 | 1.02 | 1.941 | 1.00 | 0.172 / 0.210 |
| 3 | 19.560 | 0.97 | 3.099 | 1.02 | 0.435 / 0.631 |
| 6 | 34.058 | 1.07 | 4.466 | 1.03 | 0.937 / 1.615 |
| 9 | 46.574 | 1.16 | 5.161 | 1.04 | 1.791 / 2.892 |
| 12 | 65.978 | 1.17 | 5.885 | 1.06 | 2.540 / 4.009 |

Only the three-month raw futures quote has a lower sample MSPE, by approximately 3%; its one-sided p-value for improved accuracy is 0.347. At twelve months futures have 17% higher MSPE, which is about 8.2% higher root MSPE, not 17% higher root error. The one-month absolute-error ratio rounds to 1.00, so the printed precision alone does not display the small ranking difference discussed in the text.

A crucial distinction is the direction of the alternative. Tables I–V test whether the candidate beats the no-change benchmark. Table VIII(C) reverses the alternative and asks whether no-change beats futures. Those p-values are 0.191, 0.653, 0.284, 0.114, and 0.102 at the five horizons. None rejects at 10%. The sample ranking supports using a simple benchmark; it does not demonstrate statistically established population dominance.

Raw futures directional success rates are 44.3%, 47.9%, 48.5%, 52.6%, and 53.6%. The nine- and twelve-month directional p-values are 0.080 and 0.021. These modest success rates are not a trading-strategy return, and the benchmark's zero predicted change has no comparable direction statistic. The Pesaran–Timmermann null incorporates marginal direction frequencies; a directional p-value is not merely a binomial comparison with a fair coin.

Estimating spread coefficients does not reliably improve forecasts. With both intercept and slope estimated, MSPE ratios are 1.00, 1.24, 1.52, 1.16, and 1.19. At six months this model loses 52% in MSPE relative to no-change. With just the slope estimated, the ratios are 1.00, 1.17, 1.38, 1.18, and 1.28. At twelve months the intercept-only model has MSPE ratio 1.16 and absolute-error ratio 1.04. Some longer-horizon spread models improve directional tests, but this does not offset their error magnitude under quadratic loss.

Survey forecasts are substantially worse in sample: MSPE ratios of 1.57 at three months and 1.64 at twelve months, absolute-error ratios 1.34 and 1.18, and biases of 1.905 and 4.808 dollars per barrel. Their directional success rates are 50.0% and 51.5%, without statistically compelling directional gains. The Hotelling candidate has MSPE ratios 1.01, 1.03, and 0.99 at three, six, and twelve months. Its bias is smaller than no-change, but its error ranking is not systematically better. Because a positive interest rate always predicts an increase, its direction forecast has no variation, preventing the standard direction test used for other models.

Drift models occasionally improve a table entry but do not establish a consistent winning specification. For example, the recursive-drift model has twelve-month MSPE ratio 0.98 but absolute-error ratio 1.18. At one month, the one-month rolling-drift model has MSPE ratio 1.99. The authors explicitly warn about specification mining and sensitivity to horizon and sample period. No portfolios, transaction costs, margin financing, or out-of-sample investment utility are evaluated.

## Forecast efficiency is a different question

The source also estimates full-sample log-change regressions,

$$
s_{t+h}-s_t=\alpha+\beta(f_t^{(h)}-s_t)+u_{t+h},
$$

and tests $(\alpha,\beta)=(0,1)$ with HAC standard errors. Table VI reports $(\widehat\alpha,\widehat\beta)$ of $(0.029,1.160)$ at three months, $(0.057,0.766)$ at six months, and $(0.111,0.731)$ at twelve months. Joint p-values are 0.247, 0.037, and 0.004. The first two samples are April 1989–February 2007; the twelve-month sample begins January 1990.

Failure to reject an in-sample restriction does not establish real-time forecast gains. Estimating coefficients can reduce misspecification bias while adding sampling variance. Log forecast efficiency also differs from unbiasedness of a price-level expectation because of Jensen effects and the forecaster's loss function.

Table VIII(A) reports average log futures-minus-realized-spot errors of −0.16%, −0.91%, −2.89%, −5.60%, and −7.77%, with HAC p-values 0.77, 0.59, 0.31, 0.10, and 0.05. These differ from the level-dollar bias column above. The separate log-level regressions in Table VIII(B) give slopes 0.987, 0.955, 0.941, 0.964, and 1.012; neither the separate zero-intercept nor unit-slope test rejects at 5%. A high level-regression slope near one is not the same test as the change-regression restriction. The source interprets these results as broadly consistent with risk neutrality, which is weaker than establishing it.

## Basis variation and the MSPE decomposition

Table VII characterizes $100(f_t^{(h)}-s_t)$. For the three-month spread its mean is −1.10, mean absolute deviation 2.73, maximum 12.3, minimum −10.1, and persistence 0.73. At twelve months the corresponding numbers are −4.21, 8.81, 30.1, −27.7, and 0.83. Persistence is the sum of autoregressive coefficients, with the AIC selecting an order from a maximum of 24 lags. It is not necessarily an AR(1) coefficient or a directly interpretable half-life. Both mean tests are reported as p=0.00 at printed precision, not literal zero probability.

The table note uses April 1983–February 2007 for the three-month spread and January 1989–February 2007 for twelve months. The preceding prose describes a common January 1989 start. A reproduction must resolve that discrepancy against the data or original code; the tabulated sample note is the explicit horizon-specific statement.

The paper argues that variation in the basis matters more than its modest mean. That interpretation can be sharpened with an exact derived identity. Set $b_t=F_t^{(h)}-S_t$ and $e_t=S_{t+h}-S_t$. Then

$$
E[(S_{t+h}-F_t^{(h)})^2]-E[(S_{t+h}-S_t)^2]
=E[b_t^2]-2E[e_tb_t].
$$

A volatile basis worsens forecasts only to the extent that its variation is not offset by covariance with the subsequent spot change. Basis variance alone does not prove poor forecasting. If $F_t^{(h)}=E_t[S_{t+h}]$ exactly, the conditional-mean projection property implies that futures must weakly beat any other time-$t$ measurable predictor in population MSPE. Convenience-yield variation cannot overturn that theorem. The sample rankings, sampling uncertainty, approximate pricing relation, and possible risk premia must therefore remain distinct.

The source illustrates its log-spread extremes using a spot price of \$65 and approximate dollar deviations of \$20 upward and \$18 downward. Exact conversion uses $F-S=S(e^{f-s}-1)$: at log spreads 0.301 and −0.277, the deviations are approximately \$22.83 and −\$15.73. These are derived conversions, not new observations. Multiplying a large log spread directly by the spot price is only a first-order approximation.

## Two-country model: quantities, prices, and assumptions

The model has an oil-exporting endowment economy, labeled Saudi Arabia, and an oil-importing producer of a final consumption good, labeled the United States. It abstracts from extraction decisions and oil underground. Each period the exporter receives a two-point oil endowment:

$$
\widetilde\omega_t=
\begin{cases}
\omega+\epsilon_t,&\text{probability }\theta,\\
\omega-\widehat\epsilon_t,&\text{probability }1-\theta,
\end{cases}
\qquad \widehat\epsilon_t=\frac{\theta\epsilon_t}{1-\theta}.
$$

The mean is $\omega$, and the derived variance is $v=\theta\epsilon_t^2/(1-\theta)$. Increasing the spread parameter $\epsilon_t$ at fixed $\theta$ is the mean-preserving uncertainty experiment. Positivity of the low endowment and feasible production must be maintained.

The importing economy produces the final good using oil $Z_t$ with production function $\mathcal F$. The source calls this function $F$; a different symbol here avoids confusion with the futures quote. It assumes $\mathcal F'>0$, $\mathcal F''<0$, $\mathcal F'''>0$, and an infinite marginal product as oil use approaches zero. With the final-good price $P_t$, the real oil price is $q_t=S_t/P_t$. Production and the oil resource constraint give

$$
q_t=\mathcal F'(Z_t),\qquad Z_t=\widetilde\omega_t-\Delta I_t,\qquad \Delta I_t=I_t-I_{t-1}.
$$

Diverting available oil into above-ground inventory raises the marginal product of the remaining oil and therefore its current real price. Both economies can hold a one-period risk-free bond and oil futures; the importing country also chooses production use and inventory. Risk neutrality is imposed for the main comparative statics. The article does not specify a full calibrated utility/budget system, solve a Bellman equation, or estimate structural parameters.

The convenience benefit is $g(I_t,v)$, with marginal benefit $g_1>0$, diminishing marginal benefit $g_{11}<0$, and uncertainty sensitivity $g_{12}>0$. An Inada condition $g_1\to\infty$ as inventories approach zero ensures positive inventory in the maintained solution. These properties are imposed. The paper connects the convenience yield to supply uncertainty, but does not derive a unique functional form from a detailed disruption technology.

Under real risk neutrality, the futures condition is

$$
E_t[F_t/P_{t+1}]=E_t[S_{t+1}/P_{t+1}].
$$

Since $F_t$ is known at $t$, this gives a price-level expectation weighted by inverse future goods prices. In particular,

$$
F_t=E_t[S_{t+1}]+
\frac{\operatorname{Cov}_t(S_{t+1},P_{t+1}^{-1})}{E_t[P_{t+1}^{-1}]}.
$$

The source uses a first-order approximation $F_t\approx E_tS_{t+1}$. The bond condition is $P_t^{-1}=\beta(1+r_t)E_t[P_{t+1}^{-1}]$. Its simplification to $r_t\approx\beta^{-1}-1$ presumes the stable-numeraire/price approximation used in the argument; a general nominal-rate equation also reflects expected inflation. With a constant final-good numeraire, these real-price distinctions simplify exactly.

The storage relation, after the source's approximation, is

$$
(1+r_t)q_t-\frac{F_t}{P_t}\approx(1+r_t)g_1(I_t,v),
$$

and hence

$$
\frac{F_t-S_t}{S_t}\approx r_t-(1+r_t)\frac{g_1(I_t,v)}{q_t}.
$$

The theoretical simple percentage spread differs from the empirical log spread; they coincide only to first order. Combining pricing conditions gives the inventory Euler equation used for comparative statics,

$$
\mathcal F'(\widetilde\omega_t-\Delta I_t)
=\beta E_t[\mathcal F'(\widetilde\omega_{t+1}-\Delta I_{t+1})]+g_1(I_t,v).
$$

## Uncertainty, inventory demand, and the spread condition

At fixed allocations, a mean-preserving spread raises expected future marginal product because $\mathcal F'$ is convex. It also raises current marginal convenience benefit through $g_{12}>0$. Both channels increase the incentive to hold inventory. Accumulating inventory reduces current production use and raises the current real price. The source depicts an initial price jump followed by partial reversal as inventories build and their marginal insurance value declines.

This is a conditional comparative-static mechanism, not a numerically solved global transition. Jensen's argument holds allocations fixed at the comparison point; a full dynamic proof must account for state-contingent future inventory policies. Figure 3 is schematic. Its higher long-run price is best read in the changed stochastic environment, not as an identity that a larger inventory stock raises $\mathcal F'(\omega)$ at unchanged current endowment and zero inventory change.

A rise in uncertainty does not unconditionally lower the basis. Holding the interest rate fixed to the approximation's order, differentiating the simple spread shows that it falls precisely when

$$
g_{12}\frac{dv}{d\epsilon}
+\left(g_{11}+g_1\frac{\mathcal F''}{\mathcal F'}\right)
\frac{d\Delta I_t}{d\epsilon}>0.
$$

Here current endowment and inherited inventory are held fixed for the uncertainty experiment. The direct insurance-value effect must exceed the offset from larger inventory holdings and the normalization by a higher real spot price. Equivalently, this is Eq. (15) in the source.

The source further expresses the condition as

$$
g_{12}>\frac{\lambda(1-\theta)B}{2\theta\epsilon(1-\lambda)},\qquad
\lambda=-\frac{g_{11}+g_1\mathcal F''/\mathcal F'}{A-g_{11}},
$$

where $A=-\mathcal F''(Z_t)-\beta E_t\mathcal F''(Z_{t+1})>0$. The endowment contribution to the derivative is

$$
B=\beta\theta\left[
\mathcal F''(\omega+\epsilon-\Delta I_{t+1})-
\mathcal F''(\omega-\widehat\epsilon-\Delta I_{t+1})
\right]>0.
$$

The low-state argument in printed p. 562 uses $\omega+\widehat\epsilon$; the minus sign above follows from the defined two-point distribution and is a derived correction. Since $\mathcal F'''>0$, the high-state second derivative exceeds the low-state one. The paper states $0<\lambda<1$ and interprets the threshold as sufficiently strong sensitivity of marginal inventory value to uncertainty. Under its positive-future-price Euler relation, $g_1<\mathcal F'$ helps bound that ratio. The article supplies no calibrated $g_{12}$ or empirical threshold test, and does not provide the full policy-derivative calculation needed to turn this local expression into a general dynamic theorem.

## Indicator evaluation and its historical breakdown

The proposed empirical indicator is $s_t-f_t^{(h)}$, the negative log spread. Positive spikes are interpreted as greater precautionary demand, conditional on the model. Figure 4 rises around the invasion of Kuwait and the buildup to the 2003 Iraq War, and declines around the Asian financial crisis and 9/11. Those events also affect expected supply or demand levels; the graph is a narrative consistency check, not a design isolating a mean-preserving variance shock.

The comparison measure comes from a monthly structural VAR with 24 lags, ordered as global crude-oil production growth, a detrended global real-activity index, and the real oil price. The identifying restrictions prevent supply from responding to demand innovations within the month and prevent oil-specific price shocks from affecting global activity contemporaneously. The residual oil-specific demand innovation is then interpreted as precautionary demand. That interpretation needs economic justification beyond the recursive matrix restriction; the residual could contain other oil-specific demand forces.

Historical decomposition gives a component of the real oil price associated with these innovations. Table IX reports contemporaneous correlations with the negative spreads:

| Horizon | January 1989–December 2006 | January 1989–December 2003 |
|---|---:|---:|
| 3 months | 0.388 | 0.587 |
| 6 months | 0.501 | 0.706 |
| 9 months | 0.572 | 0.770 |
| 12 months | 0.617 | 0.805 |

The increase with maturity is consistent with longer-horizon supply concerns, but correlation is not structural identification. Excluding the final three years materially strengthens the relationship. Figure 5 makes the breakdown visible: the VAR component remains relatively elevated after 2003 while the futures-based indicator declines. The negative twelve-month spread is rescaled by 1.5 for visual comparison, which does not change correlation or establish a calibrated conversion into the price component.

The authors suggest increased speculative participation as a possible cause of the divergence, citing CFTC patterns not displayed in the article. They explicitly leave causal verification for future work. The note therefore does not treat the 2003 break as proof that financial investors raised futures relative to spot.

Figure 6 reproduces a VAR response over roughly two years with one- and two-standard-error bands. Its initial increase and subsequent decline resemble the model's overshooting narrative. The article does not tabulate exact point estimates at each horizon, and the figure should not be used to invent precise response numbers. The VAR's full data construction and shock-estimation details reside partly in the cited Kilian study, so this paper alone is not a complete independent VAR replication package.

Inventory implications are supported by historical accounts of hoarding, not a formal estimated response. The authors explain that global inventory measurement, trends, and multiple inventory motives complicate such a test. This is an acknowledged gap between the proposed mechanism and direct measurement of its central state variable.

## Options comparison and implementation limits

Commodity Research Bureau data supply daily implied volatilities, computed as the arithmetic mean of put and call implied volatilities associated with a given futures maturity, beginning January 1989. Monthly series use the earlier quote-selection approach. Gaps prevent continuous longer-maturity series, so the main comparison uses one month. Correlations are 0.13 with the negative spread and 0.21 with the VAR component.

The concepts differ: the spread is intended to track a component of the real price level, whereas option volatility concerns uncertainty about a nominal price and includes other shocks. Figure 7's implied-volatility line takes signed values and its right axis is labeled “US Dollars”; the text does not fully explain the transformation behind that plotted series. The reported correlations can be recorded, but exact reconstruction of the graph requires clarification of its units and preprocessing rather than assuming it is raw positive implied volatility.

A faithful forecast replication needs original daily WTI and contract prices, historical maturity and expiration mapping, quote timestamps, survey release timing, horizon-specific observable regression outcomes, and the cited tests' dependence and bootstrap settings. A structural replication additionally needs functional forms, parameter values, a complete dynamic optimization and market-clearing solution, and the external VAR construction. None is supplied as runnable code here.

The durable empirical result is the value of a strong, parameter-free forecast benchmark and the difference between market pricing information and statistical forecasting performance. The proposed precautionary-demand interpretation is economically informative when its assumptions fit; the documented post-2003 divergence is a reason to test that fit over time. Neither the forecast ranking nor the convenience-yield model licenses treating every futures basis movement as a directly measured risk premium or a uniquely identified supply-uncertainty shock.

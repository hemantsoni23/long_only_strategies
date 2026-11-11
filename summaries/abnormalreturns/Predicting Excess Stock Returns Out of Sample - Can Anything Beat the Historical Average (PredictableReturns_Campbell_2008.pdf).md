# Predicting Excess Stock Returns Out of Sample: Can Anything Beat the Historical Average?

John Y. Campbell and Samuel B. Thompson. *The Review of Financial Studies* 21(4), 2008, 1509–1531. DOI: 10.1093/rfs/hhm055; advance publication November 20, 2007. Source: `Finance/PredictableReturns_Campbell_2008.pdf`, 23 pages. Page references below are journal pages; PDF page 1 corresponds to page 1509. The source evaluates data through 2005 and does not establish subsequent performance.

## The question and the paper's contribution

The historical average equity premium is a demanding forecasting benchmark because it estimates only one parameter from a very long sample. A predictive regression estimates an additional slope, often using a predictor available for fewer years. When monthly stock returns contain a great deal of noise, this estimation burden can outweigh genuine but modest predictability. Campbell and Thompson ask whether economically motivated restrictions can reverse the poor out-of-sample performance of unrestricted regressions documented by Goyal and Welch.

Their first contribution is deliberately simple. Require the regression slope to have the sign expected from economic theory, and prevent forecasts of the equity premium from becoming negative. Their second contribution is stronger: for valuation ratios, use steady-state accounting and valuation relationships to restrict coefficient magnitudes, potentially fixing the intercept at zero and slope at one. This replaces an unstable estimated relationship between noisy returns and valuations with a direct valuation-based expected-return calculation.

Their third contribution is to explain why a small forecasting $R^2$ can matter economically. The appropriate comparison is with the squared Sharpe ratio at the same horizon. Since the monthly equity Sharpe ratio is small, an improvement explaining less than one percent of monthly return variation may support material changes in a mean-variance investor's allocation and utility.

The central result is that simple restrictions often improve historical forecasts, and that fixed-coefficient valuation formulas perform particularly well at the monthly frequency. This does not mean every predictor succeeds, every restriction helps in every sample, or the resulting strategies have demonstrated positive net performance after costs. The paper gives a clear bias-variance argument for using theory in forecasting, supported by a historical real-time estimation exercise and a separate portfolio-choice calculation.

## Forecasting experiment and timing

The dependent variable is the simple excess return on the S&P 500. The authors forecast monthly returns and annual returns, with annual forecasts evaluated at monthly origins using overlapping twelve-month outcomes. They deliberately use simple returns rather than log returns. Earlier high-volatility decades depress log returns relative to arithmetic returns, so switching to logs changes the historical baseline and can induce systematic underprediction later in the sample.

High-quality monthly total returns from CRSP begin in January 1927. Earlier returns, assembled by Robert Shiller, rely partly on interpolated dividends and are used for initial estimation rather than the main forecast evaluation. Each predictor receives at least twenty years of initial estimation history. Evaluation begins at the later of January 1927 or twenty years after that predictor becomes available. The monthly evaluation ends in December 2005; annual forecasting tables use origins through December 2004 so the annual outcome can be observed by the end of 2005.

At each date, a predictive regression is reestimated using information through the preceding observation, and its next forecast is recorded. The benchmark is the historical average excess return available at that same point. The historical mean uses the entire return history back to 1871, even when the predictor has a shorter history. This gives it a real and intentional information-length advantage. Matching both methods to a short predictor sample would answer a different question.

For annual outcomes, a faithful implementation must respect their availability: an annual return associated with a recent forecast origin is not fully known until twelve months have elapsed. Overlapping outcomes also induce serial correlation in the in-sample regression errors. The paper reports adjusted inference for that overlap. A reproduction should make the origin-to-outcome calendar explicit rather than applying a generic monthly expanding-window routine to annual labels.

The forecasting score is

$$
R^2_{OS}=1-\frac{\sum_t(r_t-\widehat r_t)^2}{\sum_t(r_t-\overline r_t)^2},
$$

where $\widehat r_t$ is the model forecast formed without the current return and $\overline r_t$ is the contemporaneously available historical mean. Positive values mean lower realized mean squared error than the historical average. This is not the same statistic as the full-sample regression's adjusted $R^2$. It can be negative, and under a no-predictability null an estimated predictive regression can have negative expected out-of-sample performance simply because it estimates unnecessary parameters.

The authors deliberately focus on realized forecasting superiority rather than recasting every score into a formal test of true predictability. A zero out-of-sample score may be informative statistically because of the extra estimation burden, but it does not constitute an economic improvement over the benchmark. That distinction is maintained throughout the experiment.

## Predictors and construction choices

Table 1 begins with four valuation ratios, all expressed in levels rather than logarithms: dividend-price, earnings-price, smoothed earnings-price, and book-to-market. Smoothed earnings-price uses a ten-year moving average of real earnings divided by the current real stock price. Smoothing reduces the influence of cyclical earnings collapses that can make a current earnings yield misleading as a measure of valuation.

A separate predictor is ten-year-smoothed real return on equity. Real ROE is calculated from real earnings relative to lagged real book equity and the gross annual inflation rate. It measures the resources available for real payouts or growth in real book equity under clean-surplus accounting. It is included mainly because the later valuation formulas need a profitability input, not because the authors claim that standalone aggregate ROE is a strong timing signal.

Five macro-financial predictors are the Treasury bill rate, long-term bond yield, Treasury term spread, corporate default spread, and lagged inflation. The remaining variables are the equity share of new issuance and the consumption-wealth relation. For the latter, the authors enter consumption, labor income, and financial wealth directly into the return regression rather than first estimating a separate cointegrating combination. Consequently, that forecasting model estimates several coefficients and is particularly vulnerable to a short estimation history.

The long historical series differ in their start dates. Dividend-price and earnings-price begin in February 1872; smoothed earnings-price begins in February 1881. Book-to-market begins in June 1926, so its forecast evaluation starts in June 1946. Smoothed ROE starts in June 1936 and is first evaluated in June 1956. The bill rate and term spread begin in January 1920, with evaluation starting in January 1940. Default-spread evaluation begins in 1939, net-issuance evaluation in December 1947, and consumption-wealth evaluation in December 1971.

These differing windows mean rows are not a clean horse race on identical observations. A predictor with a good long-sample score may have benefited from periods unavailable to another predictor. Table 3's common historical divisions partly address stability, but they do not remove all differences in data availability. Interpretation should preserve each row's estimation and evaluation dates.

There is also a real-time data limitation. The consumption-wealth inputs use revised macroeconomic data, including changes to BEA definitions made in 2003. The authors explicitly do not solve the historical data-vintage problem. Their experiment is recursive in coefficient estimation, but that does not imply that every underlying historical observation was available in its final revised form at the forecast date.

## Sign constraints as economically motivated regularization

For a standard regression

$$
r_{t+1}=a+b x_t+u_{t+1},
$$

the slope restriction substitutes the historical-mean forecast whenever the estimated coefficient has the wrong sign. It does not retain a negative slope merely because that is what a short noisy sample suggests. The forecast restriction replaces a negative predicted equity premium with zero. The combined method first handles the slope and then applies the forecast floor.

For valuation ratios, the expected slope is positive. When prices are high relative to a fundamental numerator, the expected return should tend to be lower. The paper's empirical description refers to the theoretically expected sign as estimated over the full sample. A strict modern replication should record how the sign is fixed before evaluation; choosing a direction after inspecting forecast-period returns would introduce information beyond the recursive regression estimates. This caveat does not erase the economic rationale, but it matters for claims about a fully precommitted trading rule.

The zero floor encodes a view that an investor should not extrapolate a noisy linear relation into a strongly negative equity premium when valuations move far outside their historical range. It is a modeling restriction, not a theorem that the conditional premium can never be negative. Its purpose is to reduce forecast variance and the damage caused by extreme estimates.

Table 1 illustrates the effect at the monthly frequency. Dividend-price moves from an unrestricted $R^2_{OS}$ of $-0.65\%$ to $0.08\%$ under both restrictions. Earnings-price improves from $0.12\%$ to $0.18\%$, and smoothed earnings-price from $0.33\%$ to $0.43\%$. Book-to-market improves from $-0.43\%$ to approximately zero. The Treasury bill predictor already performs reasonably well, rising from $0.52\%$ to $0.55\%$; the term-spread score remains around $0.46\%$.

Not every variable is rescued. Default spread remains at $-0.19\%$, inflation remains negative at $-0.17\%$, and standalone smoothed ROE is still slightly negative. Consumption-wealth is a striking example of in-sample strength failing to translate into stable forecasts: its monthly in-sample adjusted $R^2$ is 2.60%, while unrestricted out-of-sample performance is $-1.36\%$. Flooring its forecasts raises the latter to $0.27\%$, but that should not be confused with reproducing the large in-sample fit.

The annual results are generally more favorable for valuations and yield-curve variables. With both sign restrictions, annual scores are 5.63% for dividend-price, 4.94% for earnings-price, 7.85% for smoothed earnings-price, and 1.39% for book-to-market. The bill-rate score is 7.47% and term spread 4.74%. Net issuance and consumption-wealth remain negative. The numerical table is more precise than a blanket statement that every valuation variable exceeds a two-percent score.

## Steady-state valuation model and fixed forecasts

The stronger restrictions begin with the Gordon relation

$$
\frac{D}{P}=R-G,
$$

where $R$ is the required return and $G$ is the growth rate. Under clean-surplus-style steady-state accounting, growth is retained earnings times accounting profitability:

$$
G=\left(1-\frac{D}{E}\right)ROE.
$$

Combining them yields the dividend-based return forecast

$$
\widehat R_{DP}=\frac{D}{P}+\left(1-\frac{D}{E}\right)ROE.
$$

Using $D/P=(D/E)(E/P)$ gives

$$
\widehat R_{EP}=\frac{D}{E}\frac{E}{P}+\left(1-\frac{D}{E}\right)ROE.
$$

The earnings-based forecast is therefore a payout-weighted average of current earnings yield and accounting profitability. If ROE equals the required return in long-run equilibrium, the relation reduces to an earnings-yield forecast. Since $E/P=(B/M)ROE$, the book-based version is

$$
\widehat R_{BM}=ROE\left[1+\frac{D}{E}\left(\frac{B}{M}-1\right)\right].
$$

These formulas combine several data inputs without estimating a separate unrestricted coefficient for each. Current valuation ratios provide the conditioning information. Payout ratios are averaged from the beginning of the available sample, while ROE uses a ten-year moving average. Before a ten-year ROE history is available in 1936, the authors use real earnings growth to estimate growth. One variant subtracts the historical average real interest rate, also computed from the beginning of the sample, to convert a real-return estimate into an excess-return estimate.

This use of a long-run real rate is deliberate. The valuation formula describes a steady-state long-run return; pairing it with a very volatile short-term realized real rate would be conceptually inconsistent and empirically noisy. The historical average real rate is stable, so the adjustment operates approximately like a slowly moving intercept shift.

The model assumes that valuation changes relative to historical cash flows correspond to permanent expected-return changes. If valuations instead move because expected profitability changes, the formulas can overstate expected-return variation. If discount-rate changes are temporary, the simple steady-state calculation can understate it. The authors view the restriction as a useful compromise, not a full dynamic asset-pricing model.

## Coefficient regimes and full-sample numerical results

Table 2 applies each valuation input in four ways: unrestricted regression; positive slope and nonnegative forecasts; positive intercept with slope bounded between zero and one; and fixed zero intercept with unit slope. In the last case, the valuation formula itself is the return forecast. No historical return-predictor covariance is needed to estimate its coefficients.

All eleven monthly fixed-coefficient specifications have positive out-of-sample scores, ranging from 0.24% to 0.97%. Unadjusted smoothed earnings-price has the largest score, 0.97%, versus 0.32% for its unrestricted regression. Unadjusted earnings-price scores 0.76%, while dividend-price scores 0.42%. Adding growth gives 0.63% for dividend-price, 0.57% for earnings-price, and 0.72% for smoothed earnings-price. Growth-adjusted book-to-market scores 0.33%.

Subtracting the historical real rate generally lowers the full-sample fixed-coefficient scores: the respective dividend, earnings, smoothed-earnings, and book-based variants score 0.41%, 0.39%, 0.52%, and 0.24%. A theoretically more complete-looking formula does not mechanically yield the best forecasting result. Data noise and the target being forecast matter alongside accounting consistency.

At the annual horizon, fixed-coefficient scores remain positive across the table, from 1.85% to 7.99%, but the stronger restriction can hurt relative to an estimated regression. The unadjusted dividend-price score falls from 5.53% unrestricted to 2.20% fixed. This particular zero-intercept restriction effectively assumes no real dividend growth and is less economically appealing than its growth-adjusted counterpart. The smoothed earnings-price fixed forecast achieves 7.99%, close to its unrestricted 7.89% score.

Thus the evidence supports a general variance-reduction mechanism but also shows a bias cost. Replacing estimated coefficients with theory works especially well where estimation error is large; imposing an incomplete economic identity can be too restrictive in another horizon or period. The paper does not claim a universal dominance theorem for fixed coefficients.

## Stability over historical regimes

Table 3 divides evaluation into 1927–1956, 1956–1980, and 1980–2005. These periods roughly separate the Depression and wartime era, postwar expansion and inflation shocks, and the later equity bull market. The first division also ensures that later growth adjustments can rely entirely on smoothed ROE rather than earlier earnings-growth substitutions.

Forecasting success is generally strongest in the first period and weakest in the last. The fixed unadjusted monthly smoothed-earnings score falls from 1.33% to 0.51% to 0.01%. Its growth-adjusted counterpart falls from 0.93% to 0.47% to 0.16%. The final figure is small but positive; a declining cumulative score does not by itself imply that the recent forecasts lose to the mean, only that they win less decisively.

Unadjusted dividend-price performs especially poorly after 1980. Its monthly fixed score is $-0.54\%$ and annual fixed score $-7.98\%$. Adding growth changes those to 0.14% and 0.28%. The authors connect the relative weakness of dividends to the increasing importance of repurchases in shareholder payouts, though they do not implement a full repurchase-adjusted payout series in these tables.

Growth-adjusted earnings and smoothed-earnings monthly fixed forecasts both score 0.16% after 1980. Annual fixed scores are 1.60% and 1.81%. Some real-rate-adjusted annual variants become negative, so even during the period most relevant to the paper's contemporary debate, success depends on the precise specification. Preserving these negative cases is essential to interpreting the result as empirical evidence rather than a guaranteed allocation recipe.

## Why small explanatory power can matter

The analytical example assumes

$$
r_{t+1}=\mu+x_t+\varepsilon_{t+1},
$$

with mean-zero predictor $x_t$, constant predictor variance $\sigma_x^2$, and constant innovation variance $\sigma_\varepsilon^2$. An investor maximizes expected portfolio return minus $\gamma/2$ times variance. Without observing the predictor, the optimal stock weight is

$$
\alpha=\frac{\mu}{\gamma(\sigma_x^2+\sigma_\varepsilon^2)}.
$$

With the predictor observed, it becomes

$$
\alpha_t=\frac{\mu+x_t}{\gamma\sigma_\varepsilon^2}.
$$

Predictable variation no longer counts as conditional uncertainty. Define the unconditional squared Sharpe ratio $S^2=\mu^2/(\sigma_x^2+\sigma_\varepsilon^2)$ and regression fit $R^2=\sigma_x^2/(\sigma_x^2+\sigma_\varepsilon^2)$. The increase in average excess portfolio return is

$$
\Delta E[r_p]=\frac{1}{\gamma}\frac{R^2}{1-R^2}(1+S^2).
$$

For short horizons with small $R^2$ and $S^2$, this is approximately $R^2/\gamma$, while the proportional return increase is approximately $R^2/S^2$. The observed monthly stock Sharpe ratio is 0.108, corresponding to about 0.374 annually, so its monthly square is roughly 1.2%. Comparing a 0.43% monthly forecasting score with 1.2% gives a proportional improvement near 36% in the stylized calculation.

For unit risk aversion, the example translates into about 43 basis points a month, or 5.2% annually; with risk aversion three, about 1.7% annually. These are model-based average-return implications, not reported net trading profits. The informed investor also changes risk exposure, so the return gain cannot be read directly as a welfare gain. The analytical result assumes known population relationships and unconstrained portfolio choice, unlike the subsequent historical exercise.

## Portfolio experiment, limitations, and practical interpretation

Table 4 separately computes utility gains for risk aversion $\gamma=3$. Stock weights are constrained between zero and 150%, preventing short equity positions and limiting leverage to 50%. Variance is estimated from a rolling five-year window of monthly returns. Each predictive strategy is compared with a strategy using the historical-mean premium and the same portfolio framework. Utility is measured as mean portfolio return minus half risk aversion times portfolio variance; monthly gains are multiplied by twelve to annualize them.

For 1980–2005, the fixed monthly earnings-price forecast produces a utility gain of 0.74% annually; smoothed earnings-price produces 0.46%. Their growth-adjusted versions produce 0.19% and 0.24%. The unadjusted dividend-price rule loses 1.32%, whereas its growth-adjusted version gains 0.34%. Annual fixed forecasts produce gains of 0.68% for earnings-price, 0.81% for smoothed earnings-price, and 0.50% for growth-adjusted smoothed earnings-price. These figures demonstrate that forecasting scores and allocation value are related but not identical.

The upper weight constraint can bind when estimated premiums are high, preventing additional forecasting variation from changing holdings. Conversely, a forecast improvement concentrated near allocation boundaries can have a disproportionate utility effect. Incorrect variance estimates also change realized utility, especially if the predictor contains information about volatility as well as mean returns. The paper acknowledges this issue but does not build a joint return-volatility model.

Transaction costs, taxes, borrowing spreads, and implementation frictions are not deducted. The utility differences can be interpreted as annual fees or extra costs an investor would tolerate under the stated preferences, but the study does not calculate actual turnover-dependent costs. The benchmark itself rebalances, so the relevant implementation question is incremental costs relative to that benchmark, not the total cost of the timing portfolio alone.

Reproducing the article requires preserving arithmetic-return targets, predictor levels, long-history benchmark estimation, the twenty-year initialization rule, annual-outcome availability, ten-year profitability smoothing, and the changing pre-1936 growth proxy. The paper supplies equations and tables but not a complete point-in-time database reconstruction or executable vintage-specific workflow. A modern extension should retain the original specification before considering revised payout measures, different floors, or alternative smoothing lengths; otherwise it becomes a new model-selection exercise.

The broader implication is a concrete forecasting principle: economic structure can be valuable even when it is only approximately true, because removing unstable coefficients can reduce forecast variance more than it adds bias. The article establishes that principle in historical aggregate-return prediction and quantifies its possible allocation value. Its strongest lesson is to compare restrained forecasts with a demanding simple benchmark, report unfavorable subperiods and predictors, and evaluate economic utility separately from statistical fit.

## Distinguishing the mechanisms behind the improvement

The restrictions operate on different sources of error and should be evaluated separately in replication. A sign restriction mainly protects against a slope estimated from an unrepresentative short history. A nonnegative forecast protects against extrapolation even when the slope has the expected sign. A bounded slope protects against excessively large sensitivity to valuation movements, and a fixed slope eliminates sensitivity-estimation error altogether. Their effects can coincide in a particular month, but they are not interchangeable statistical operations.

The paper's dividend-yield figure makes these distinctions concrete. In the early 1930s, estimated slopes could be negative, so high yields were perversely translated into low expected returns. Later, including in the 1960s and 1990s, the slope could have the sensible positive sign while unusually low yields generated extreme negative forecasts. The first episode is addressed by resetting the slope-based prediction to the historical mean; the second is addressed by the zero floor. Inspecting when each constraint binds is therefore an informative replication diagnostic beyond reproducing a single mean squared error.

The benefit of fixed valuation formulas also goes beyond shrinking the slope. Historical average returns are themselves difficult to estimate precisely because realized returns are volatile. A formula using cash-flow yields and relatively stable profitability inputs provides a different way to estimate the level of expected returns. It can avoid both the uncertain slope and the uncertain intercept of a regression fitted to a short return history. This helps explain why fixed coefficients can beat more permissive sign constraints even though the latter already exclude obviously implausible predictions.

There is an accounting subtlety in the smoothing choices. The current valuation denominator is allowed to respond immediately to market prices, while payout and profitability inputs adjust slowly. A sudden price change therefore produces an immediate expected-return response, whereas a new earnings observation is diluted in the smoothed series. That timing is part of the economic assumption that valuation changes chiefly reflect discount rates. Replacing the historical payout average with the latest payout, or ten-year ROE with quarterly profitability, would alter both the information weighting and the interpretation of the forecast.

The authors use arithmetic averages when converting accounting information into expected arithmetic stock returns. A geometric-growth approach would require an explicit volatility adjustment because stock returns are much more volatile than dividend growth or ROE. The article observes that an alternative geometric convention could imply higher arithmetic-return forecasts and perform better during the late-century bull market, but it does not conduct that full comparison. Consequently, a replication should not silently combine geometric growth estimates with the article's arithmetic return targets.

Finally, the conclusion that small $R^2$ values can be useful depends on horizon consistency. A monthly score must be compared with a monthly squared Sharpe ratio; annualizing only one side exaggerates or suppresses the apparent value. The same caution applies when comparing the article's annual overlapping forecasting results with a once-yearly trading strategy. Forecast frequency, holding period, and portfolio rebalancing schedule are separate design choices, and a production implementation must state all three explicitly.

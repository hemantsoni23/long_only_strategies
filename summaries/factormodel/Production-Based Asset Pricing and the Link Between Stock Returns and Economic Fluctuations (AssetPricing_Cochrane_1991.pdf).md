# Production-Based Asset Pricing and the Link Between Stock Returns and Economic Fluctuations

**Author:** John H. Cochrane. **Publication:** *Journal of Finance* 46(1), March 1991, pp. 209–237. **Source:** [AssetPricing_Cochrane_1991.pdf](../../Finance/AssetPricing_Cochrane_1991.pdf), 30 pages including an archive cover. The full image-only article and data appendix were read using local OCR, with equations, timing diagram and numerical tables checked against rendered pages. Printed page 209 is PDF page 2. This note describes the paper's original 1947–1987 aggregate implementation, not later cross-sectional investment-factor models.

## Why this matters

The paper obtains an asset-pricing restriction from optimal physical investment rather than from a consumer's marginal utility. A firm can divert goods from sales into capital today and reverse the capital change tomorrow, producing a state-contingent investment payoff. At an optimum, this marginal investment return must have the same price as its financial-market equivalent. Under the paper's special technology and capital-claim interpretation, the marginal physical return equals the firm's stock return state by state. This supplies a direct link between stock returns and investment activity without first solving the consumption side of the economy.

The empirical contribution is deliberately modest. A return inferred from aggregate investment tracks part of stock-return variation and much of the component forecast by business-cycle variables. It also forecasts subsequent activity in a way broadly similar to stock returns. Dividend-price ratios identify a stock-return component that the constant-productivity implementation misses. Timing and distributed-lag diagnostics expose further failures. The author explicitly does not claim that the exact model survives a formal specification test; literal equality of observed stock and constructed investment returns fails immediately.

For a quantitative researcher, the useful object is the map from a production technology and investment data to a marginal return. It separates a theoretically required payoff relation from an empirical calibration and from a statistical forecasting exercise. This distinction prevents interpreting an in-sample matching exercise as evidence for an implementable trading rule, or interpreting aggregate investment growth as itself a universal stochastic discount factor.

## State prices and the producer's optimization problem

The theoretical setup uses discrete dates, a finite state tree and one consumption good. A history $s^t$ identifies a date-$t$ state. Let $P(s^t)$ be its time-zero Arrow price and let $p(s^{t+1}\mid s^t)=P(s^{t+1})/P(s^t)$ be the one-step contingent price. A gross asset return obeys

$$
1=\sum_{s^{t+1}\succ s^t}p(s^{t+1}\mid s^t)R^A(s^{t+1}).
$$

Introducing conditional probabilities merely rewrites this as $1=E_t[m_{t+1}R^A_{t+1}]$, where $m$ is the contingent price divided by the corresponding probability. The firm's decision can be stated directly in state prices, without selecting a household utility function or attributing a particular subjective probability law to managers.

The firm maximizes the time-zero value of sales net of wages, given initial capital, contingent wages and prices. Its constraints are

$$
y_t=f(k_t,l_t,s_t),\qquad y_t=c_t+I_t,\qquad k_{t+1}=g(k_t,I_t).
$$

Here $c_t$ is output sold as consumption goods, $I_t$ is investment, $k_t$ capital and $l_t$ labor. The accumulation function contains adjustment costs. The first-order condition relevant for asset pricing is

$$
1=E_t[m_{t+1}R^I_{t+1}],\qquad
R^I_{t+1}=g_I(t)\left[f_k(t+1)+\frac{g_k(t+1)}{g_I(t+1)}\right].
$$

All derivatives are evaluated along the firm's optimal state-contingent plan. $R^I$ is a gross return measured in consumption goods; it is generally risky because marginal productivity and next-period decisions vary across states. The result requires an interior marginal adjustment with well-defined derivatives and a positive marginal conversion $g_I$. Binding irreversibility or financing restrictions would change the first-order condition.

The construction is worth reproducing rather than treating the equation as an asserted factor model. Reduce current sales by $dI_t$, raising next-period capital by $g_I(t)dI_t$. Next period, the extra capital produces $f_k(t+1)g_I(t)dI_t$ additional output. Reduce next-period investment by

$$
dI_{t+1}=-\frac{g_k(t+1)}{g_I(t+1)}g_I(t)dI_t
$$

so that capital at $t+2$ and every subsequent element of the plan remains unchanged. Both extra output and avoided investment can be sold at $t+1$. Their sum divided by the date-$t$ sacrifice is $R^I$. This two-date perturbation isolates a holding-period return without requiring an infinite discounted sum of future operating profits.

## What complete markets do and do not imply

In complete financial markets a portfolio can replicate the investment payoff across all next-period states. Optimal production eliminates an arbitrage between creating this payoff physically and buying it financially. The investment return therefore equals the return of its mimicking portfolio ex post, not just in expectation. This statement alone does not say that it equals an arbitrary stock index, the risk-free return, or the reciprocal of the stochastic discount factor.

The paper obtains equality with the firm's own stock return only after imposing a technology for which stock represents a claim to productive capital of a single technology, or a constant linear combination of such technologies. A claim at date $t$ to one unit of installed capital at $t+1$ costs $P_t^{k_{t+1}}=1/g_I(t)$. Holding that claim for one period produces marginal output $f_k(t+1)$ and $g_k(t+1)$ units of next-period capital, worth $P_{t+1}^{k_{t+2}}$ each. Thus

$$
R^{capital}_{t+1}
=\frac{f_k(t+1)+g_k(t+1)P_{t+1}^{k_{t+2}}}{P_t^{k_{t+1}}}
=R^I_{t+1}.
$$

An empirical mapping from this productive-capital claim to levered equity in a heterogeneous listed-firm portfolio is an additional approximation. The author acknowledges missing debt claims, private businesses, residential capital and taxes. This is the key distance between the clean arbitrage derivation and the aggregate empirical application.

The model is partial equilibrium. It says how investment, technological marginal returns and financial returns must relate given state prices. It does not explain why a term premium forecasts investment, whether shocks are monetary or technological, or how consumers choose consumption. It complements the consumption Euler equation rather than disproving it. A general-equilibrium model would need both sides to hold and would inherit additional restrictions and potential misspecification.

## Technology and an implementable investment-return formula

The chosen technology has linear contemporaneous production and a homogeneous nonlinear accumulation rule:

$$
y_t=mp_tk_t+mpl_tl_t,
$$

$$
k_{t+1}=(1-\delta)\left[k_t+I_t-\frac{\alpha}{2}\frac{I_t^3}{k_t^2}\right].
$$

$mp_t$ and $mpl_t$ are marginal products; $\delta$ is depreciation and $\alpha$ governs investment adjustment costs. Defining $x_t=I_t/k_t$ gives

$$
g_I(t)=(1-\delta)\left(1-\frac32\alpha x_t^2\right),\qquad
g_k(t)=(1-\delta)(1+\alpha x_t^3).
$$

Equation (15), checked against the rendered source, is therefore

$$
R^I(t\to t+1)
=(1-\delta)\left[mp_{t+1}+
\frac{1+\alpha x_{t+1}^3}{1-\frac32\alpha x_{t+1}^2}\right]
\left(1-\frac32\alpha x_t^2\right).
$$

A reproducing implementation should evaluate this expression directly and verify $1-\tfrac32\alpha x_t^2>0$ throughout its sample. It should also compare the result with the derivative-based general formula. The initial ratio reduces the return because current marginal capital formation is costly. A high next-period ratio raises the value of reducing next-period investment while returning to the original capital plan. These opposing effects make the return approximately a function of the change in the investment-capital ratio, and hence approximately of investment growth when capital changes slowly.

This is a local approximation, not an identity equating investment returns to investment growth. The exact expression is nonlinear and includes marginal productivity. In the implementation, productivity is held constant; much of the return's movement is therefore generated by changing adjustment costs. The author argues that parameter changes primarily rescale the series while leaving correlations and timing relatively stable. That is an empirical property of the relevant sample and parameter neighborhood, not a global invariance theorem for arbitrary technology or extreme ratios.

The capital price is

$$
P_t^{k_{t+1}}=\frac{1}{(1-\delta)(1-\frac32\alpha x_t^2)}.
$$

Solving this for $x_t$ recovers a version of Tobin's $q$ investment demand. The novelty is to use the return formulation and view production quantities as informative about asset returns. The author suggests that return changes can fit better than price levels when unobserved slow-moving technology shifts make a fixed long-run valuation relation unreliable, and that stock returns incorporate changing risk premia that interest-rate-only investment models can miss.

## Local sensitivities and the calibration diagnostic

The model's opposing endpoint effects can be verified analytically before touching stock data. Hold $mp$ fixed and define $a(x)=1-3\alpha x^2/2$ and $h(x)=(1+\alpha x^3)/a(x)$. Then

$$
R^I=(1-\delta)a(x_t)[mp+h(x_{t+1})],
$$

$$
\frac{\partial R^I}{\partial x_t}
=-3(1-\delta)\alpha x_t[mp+h(x_{t+1})],
$$

$$
\frac{\partial R^I}{\partial x_{t+1}}
=(1-\delta)a(x_t)
\frac{3\alpha x_{t+1}(1+x_{t+1}-\alpha x_{t+1}^3/2)}{a(x_{t+1})^2}.
$$

These derivatives are a reconstruction from equation (15), included to make the local approximation and Table IV gradients reproducible. They hold holding the other endpoint and marginal product fixed; they are not total derivatives through an endogenous investment policy. At admissible positive ratios, the initial derivative is negative and the final derivative is positive. Their magnitudes become unstable as marginal installation productivity $a(x)$ approaches zero. A linear approximation adequate near the sample mean can therefore fail badly near that boundary.

For an annual return, differentiate the product of four quarterly gross returns using the product rule. Intermediate ratios appear in two adjacent quarterly factors and much of their effect cancels; endpoints remain influential. This is why the theoretical annual distributed-lag pattern concentrates near the beginning and end of the holding interval. It is a property to verify numerically rather than a reason to delete all intermediate ratios by assumption.

The calibration comparison should use identical regression design matrices for observed stock returns and each candidate investment-return series. Compare their fitted components under the paper's lead/lag projection and solve for mean and fitted-volatility agreement, recalculating the capital path for every parameter trial. Because those two moments are targets, they should be reported as matched moments rather than counted among independent tests. Correlations, omitted-dividend-yield behavior, off-window coefficients, and forecasting of subsequent GNP supply the separate diagnostics.

## Data and construction of the state series

The sample is quarterly, 1947:Q1–1987:Q4. The data appendix names seasonally adjusted CITIBASE series GIF82 for investment; the main text calls the relevant quantity gross fixed private domestic investment, whereas the appendix uses gross private domestic investment. The explicit series identifier is therefore the safest starting point, followed by verification of its historical definition and units. Do not substitute a current revised BEA series without documenting the vintage and coverage difference.

Stock total and ex-dividend returns are CRSP's value-weighted NYSE series VWRET and VWRETX. Treasury-bill, government-bond and corporate-bond total returns and inflation come from the Ibbotson–Sinquefield series USTR, GBTR, CBTR and CPI. The government-bond series represents ten-year government bonds. These definitions matter because the paper's “term” and “corporate” variables are realized bond-return spreads, not the more familiar current yield spreads.

For each trial parameter set, capital is reconstructed consistently with the nonlinear accumulation equation. Appendix equation A1 can be written

$$
x_{t+1}=\frac{I_{t+1}}{I_t}
\frac{x_t}{(1-\delta)(1+x_t-\frac\alpha2x_t^3)}.
$$

Set $x_{1947:Q1}$ to a fixed point $x^*$ of this recursion with investment growth replaced by its sample mean. For a positive fixed point, the initialization solves

$$
\overline{I_{t+1}/I_t}
=(1-\delta)\left(1+x^*-\frac\alpha2(x^*)^3\right).
$$

A cubic can have multiple real roots; choose the economically relevant positive branch with positive marginal investment productivity and consistency with the reported ratio near 0.137. The paper does not describe a numerical root-selection algorithm or tolerance. Then iterate through observed investment growth, calculate quarterly $R^I$, and compound four successive gross returns for overlapping annual returns. Recalculation is required when $\alpha$ or $\delta$ changes because the capital series itself changes.

The flow-unit convention is especially important. The paper sets $\delta=0.10$ in the recurrence used with quarterly observations. This is a modeling normalization coupled to the source's investment scaling and calibrated marginal product; it should not casually be relabeled as a 10% annual physical depreciation rate. The article does not provide enough implementation code to resolve every annual-rate versus quarterly-flow convention independently. A replication must preserve the original GIF82 scaling and recover Table I before interpreting structural parameter magnitudes.

## Calibration and time alignment

Depreciation is fixed arbitrarily at 0.10. The marginal product and adjustment parameter are selected to match the mean stock return and the standard deviation of fitted returns from regressions on eight leads and lags of $I/k$. The fitted-value standard deviation is used because raw stock returns contain much more residual variation than constructed investment returns. Consequently, the calibration intentionally matches an investment-related component of stock-return volatility, not total equity volatility.

Reported parameters are $\alpha=13.04$, $mp=0.15$ for quarterly returns and $\alpha=13.22$, $mp=0.16$ for annual returns, in each case with $\delta=0.10$. These rounded values may not reproduce every table entry exactly. Matching uses future as well as past ratios and the entire sample. It is a descriptive calibration, not an out-of-sample forecasting design, and apparent agreement in matched moments is not independent validation.

The loss fraction of investment is $\alpha x_t^2/2$. The text illustrates this with $\alpha\approx13$ and $x\approx0.10$, obtaining roughly 7% of investment or about 1% of output. Table I's actual mean ratio is 0.137, at which the formula is about 12.2% of investment. The narrative calculation is therefore an order-of-magnitude example at a different ratio, not the exact sample-average loss. Neither number should be described as an independently measured adjustment cost.

Investment is a quarterly flow while stock returns are point-to-point. Figure 1 shifts outcome stock returns approximately from the center of the starting quarter to the center of the ending quarter. Its monthly grid uses a boundary near the end of the first month of the quarter—for example end-October to end-January for the depicted quarterly comparison—rather than conventional quarter-end returns. This is a crude time-aggregation correction, explicitly acknowledged as such. Regressor returns retain conventional beginning-to-end quarter dates; real variables are quarter aggregates. Outcome and regressor return timestamps therefore cannot be treated interchangeably.

Forecasts of $R(t-1\to t)$ use information labeled $t-2$, and forecasts of $R(t-4\to t)$ use information labeled $t-5$. Those extra lags avoid overlapping the predictor period with the shifted outcome period. They do not create a true real-time macroeconomic information set: original release dates, subsequent revisions and publication delays are not modeled.

## Forecast variables and inference

The regressors are $Term=GBTR-USTR$, $Corp=CBTR-USTR$, lagged real equity return, dividend-price ratio and $I/k$. Term and dividend yield are based on the year ending in the indicated predictor quarter; corporate spread and lagged equity return use that quarter. To form dividend yield, compound VWRET and VWRETX separately over the preceding year and compute

$$
d/p=\frac{R^{net}_{VW,annual}-R^{net}_{VW,exdiv,annual}}
{1+R^{net}_{VW,exdiv,annual}}.
$$

This convention carries dividends forward at the market return and divides by end-period price. A simple sum of unadjusted cash dividends divided by price is not identical. Real returns use the CPI transformation; preserve gross-return arithmetic before subtracting one or converting to percentage units.

The main comparisons estimate OLS for stock returns, investment returns and their difference using identical samples and regressors. Equal coefficients imply zero slopes for the difference regression. Individual two-sided tests and joint chi-square tests are reported as percentage $p$ values: a table value of 0.03 means 0.03%, not 3%. Annual overlapping-return inference uses a Hansen–Newey–West covariance correction with eight positive and negative lag covariances and damping to obtain a positive covariance estimate. The author chooses twice the overlap to give the first four lags adequate weight. Correlation standard errors also receive this correction. An implementation should document exact lag indexing and taper weights rather than silently using a software default bandwidth.

The theoretical statement is $R^{VW}=R^I$ at every observation, which is mechanically false for any reported calibration. Permitting unrestricted measurement errors, however, would make the statement unfalsifiable. Orthogonality restrictions on those errors are not automatic: aggregation mismatch, time aggregation, missing productivity and taxes need not be independent of forecasting variables. The author therefore interprets these regressions as measures of empirical correspondence and diagnostics, not a definitive structural specification test or a proof that model errors are innocuous.

## Numerical evidence: successes and failures

Table I reports a mean $I/k$ of 0.137, standard deviation 0.009 and strong persistence: first-order quarterly autocorrelation 0.90, falling to 0.28 at lag four and approximately zero at lag eight. Matched quarterly returns average 1.70%; the investment-return standard deviation is 3.42% versus 7.24% for stocks. Matched annual means are 7.33%, with standard deviations 9.37% and 15.53%. The large remaining equity variation is a substantive limitation, not a small residual ignored by the author.

Table II gives contemporaneous stock/investment-return correlation 0.241 quarterly, with standard error 0.069 and slope $t=3.163$. At the overlapping annual horizon it rises to 0.385, standard error 0.113 and $t=2.820$. Nonoverlapping annual correlations range from 0.306 to 0.449 depending on which quarter anchors the year. Investment growth itself has correlations 0.237 quarterly and 0.360 annually with stock returns; GNP growth has 0.294 and 0.404. The resemblance is therefore not a highly selective success of this exact adjustment-cost functional form.

Table III's single-regressor stock/investment slope pairs are 0.16/0.10 for the quarterly term variable, 0.35/0.16 for the corporate variable, 0.16/0.15 for lagged returns, and −1.53/−1.71 for $I/k$. Dividend yield is the exception: 1.32 for stock returns but 0.11 for investment returns. At the annual horizon its slope pair is 5.02/0.80. It forecasts stock-minus-investment returns with percentage $p$ values 1.22 quarterly and 0.02 annually. The interpretation is a dividend-yield component of predictable equity returns missing from the constant-productivity investment proxy.

With all five regressors, stock-return $R^2$ is 0.12 quarterly and 0.22 annually, versus 0.29 and 0.52 for investment returns. Joint stock-predictor percentage $p$ values are 0.03 and 0.01. The fitted stock and investment forecasts correlate 0.664 quarterly and 0.610 annually when dividend yield is included. Excluding it raises those correlations to 0.875, standard error 0.035, and 0.938, standard error 0.179. The latter uncertainty is large; these are in-sample forecast components, not correlations of independently validated predictions.

In regressions omitting dividend yield, the stock-minus-investment regression has $R^2=0.02$ quarterly and 0.03 annually, with joint percentage $p$ values 49.24 and 58.61. This supports a common component associated with business-cycle predictors. It does not establish equality with high precision at every horizon. In the full annual model, $I/k$ also predicts the difference individually at $p=3.94\%$, and the joint non-dividend-yield test is $p=7.09\%$. The paper's broad conclusion should therefore be read as approximate correspondence, with visible exceptions.

## Distributed-lag diagnostics and subsequent activity

Regressing returns on leading, contemporaneous and lagged investment-capital ratios is a diagnostic of the technology's timing, not an implementable forecast. For quarterly $R(t-1\to t)$ the formula directly uses only $x_{t-1}$ and $x_t$. Its local gradients at the reference ratio are −8.70 and 8.63, and the corresponding investment-return multiple-regression coefficients are −8.47 and 8.46 with $R^2=0.98$ (Table IV). A stock regression on just those two ratios gives −5.33 and 4.05, with $R^2=0.09$. The sign pattern fits; the magnitude and residual variation do not.

Including additional dates yields stock coefficients −6.14 at $t-1$, only 0.17 at $t$, 1.29 at $t+1$ and 2.49 at $t+2$. The positive association appears shifted forward relative to the physical-return formula. At the annual horizon the theoretical return depends mostly on the endpoints, whereas empirical stock coefficients are more spread across intervening quarters. Plausible explanations include gestation lags and uncertainty about when measured investment becomes productive, but these explanations are proposed extensions, not estimated fixes.

The difference regressions reject equality of all distributed-lag coefficients. Moreover, Table IV reports joint percentage $p$ values 2.06 for quarterly noncontemporaneous ratios and 3.51 for annual ratios outside $t-4,\ldots,t$. These are below 5%, despite nearby narrative emphasizing that most rejection is contemporaneous and that many individual lead/lag coefficients are insignificant. Reproduction should report the table's actual joint tests and avoid the stronger claim that every off-window restriction passes.

Persistence explains why an investment return that depends algebraically on current ratios can nevertheless correlate with future ratios in single regressions. This is not foresight or a contradiction. Once contemporaneous ratios are controlled for, the direct functional dependence is exhausted. The paper uses this observation to explain why stock returns can forecast future economic activity even though its proposed physical-return relation is contemporaneous. It distinguishes a common dynamic component from a claim that current prices are purely a delayed response to future output.

Table V reverses the regression direction and forecasts GNP growth using lagged returns. Four lagged quarterly stock returns give $R^2=0.16$; investment returns give 0.19; stock-minus-investment returns give 0.04 with joint $p=11.21\%$. Annual growth regressions have corresponding $R^2$ values 0.33, 0.47 and 0.06, with difference-regression joint $p=18.87\%$. These results suggest that much of the stock-market signal about subsequent activity is also present in the investment-derived series. Separate lag coefficients and timing are not identical, and failure to reject the difference does not establish equal economic forecasting loss.

## Reproducibility boundaries and practical use

To reproduce the article, first recover the original data definitions and units, construct the nonlinear ratio recursion, and match its descriptive moments. Then calibrate marginal product and adjustment costs under the stated fitted-volatility criterion, retaining separate quarterly and annual calibrations. Implement the shifted outcome-return convention and extra predictor lag explicitly. Reproduce Tables II–III before adding the lead/lag diagnostic and GNP forecasts. Retain gross-return compounding, source percentage units and the eight-lag covariance correction throughout. No machine-learning hyperparameters, portfolio rebalance rule, transaction-cost model or performance fee is part of this design.

Missing ingredients include the historical data files and vintages, exact capital-root solver, unrounded parameters, some monthly timing implementation details, and a statistical model for specification errors. The technology omits taxes, irreversibility, financing frictions, multiple capital types and measured productivity shocks. Aggregate NYSE equity is only an approximation to the claim on the capital corresponding to aggregate investment. None of the regressions is a rolling or expanding-window out-of-sample validation, and the paper reports no tradable excess-return strategy.

The durable takeaway is a method for building asset-pricing restrictions from the production margin. Its empirical demonstration links investment adjustment and business-cycle return predictability, while clearly leaving dividend-yield predictability, much equity volatility and exact timing unexplained. An extension should preserve the marginal-return derivation and improve the technology or data mapping, rather than merely add predictors until an in-sample regression fits. Cross-sectional technologies, observed productivity shocks and explicit installation lags are natural research directions identified by the author, but their success is not established by this paper.

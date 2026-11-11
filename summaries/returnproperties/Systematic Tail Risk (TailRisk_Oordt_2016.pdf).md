# Systematic Tail Risk

**Authors:** Maarten R. C. van Oordt and Chen Zhou. **Publication:** *Journal of Financial and Quantitative Analysis* 51(2), April 2016, 685-705. **DOI:** 10.1017/S0022109016000193. **Source:** `Finance/TailRisk_Oordt_2016.pdf`, 21 pages, including the appendix proof and references. Page references below use journal pagination. The study concerns nonfinancial U.S. equities, daily extreme-market losses, and the distinction between measuring crash exposure and finding a premium for that exposure.

## Main contribution and results

The paper constructs and tests a tail analogue of market beta. It measures the magnitude of an asset's response to an extreme market loss, not merely the probability that the asset also crashes and not its loading on innovations in an aggregate tail-risk index. The authors combine a locally linear model in the extreme market tail with an extreme-value estimator based on joint tail counts, marginal loss thresholds, and the market tail index. The resulting beta is additive across portfolio holdings under the model.

The empirical result has two parts that should remain separate. Historical tail betas predict which stocks lose more in subsequent severe market declines. But high estimated tail beta does not reliably command a positive unconditional return premium. During days on which the market excess return is below minus two percent, high-tail-beta stocks lose roughly two to three times as much as low-tail-beta stocks. This distinction persists after ordinary market risk and other characteristics are controlled. In contrast, unconditional high-minus-low returns are not significantly positive, and some size-controlled results are significantly negative.

This is useful negative evidence about a specific asset-pricing prediction, not evidence that all tail-risk measures are unpriced. In particular, Kelly-Jiang exposure to changes in aggregate tail conditions is a different economic object. A stock can react to news about future tail risk differently from how it co-moves with the market during a realized crash. Nor is the paper's measure identical to downside beta, which conditions on a much broader set of negative or below-average market returns.

The strongest applied contribution is a persistent, interpretable measure of systematic stress sensitivity. Its use for portfolio loss extrapolation requires additional heavy-tail and idiosyncratic-dependence assumptions. Its potential use as a low-tail-risk investment strategy requires costs, borrow availability, turnover, and realistic portfolio constraints, none of which are the focus of the reported tests.

## The linear tail model

Let $R_j^e=R_j-R_f$ and $R_m^e=R_m-R_f$ denote asset and market excess returns. Define $\operatorname{VaR}_m(\bar p)$ as the positive market loss exceeded with small probability $\bar p$. The maintained model, equation (1), is

$$
R_j^e=\beta_j^T R_m^e+\varepsilon_j,
\qquad R_m^e<-\operatorname{VaR}_m(\bar p).
$$

Within this extreme-market region, the idiosyncratic component is assumed independent of the market and to have mean zero. The coefficient $\beta_j^T$ describes the magnitude of market-tail exposure. For example, a beta of two corresponds to an expected asset movement of minus twenty percent when market excess return is minus ten percent, subject to the maintained tail model. This is an interpretation of conditional exposure, not a guarantee for an individual realized stock return.

The model makes no corresponding linearity claim for normal market conditions. Ordinary beta can therefore differ from tail beta without a contradiction. It also does not require estimating a global polynomial response with arbitrarily high co-moments, which can be problematic when heavy-tailed returns do not possess those moments. The price of that focus is reliance on a small number of tail observations and on approximate stability of the tail relation over the estimation window.

The zero intercept and conditional zero-mean idiosyncratic term are consequential. A finite-threshold regression with an intercept, a changing conditional residual mean, or dependence between residual and market shocks would not automatically share the same pricing interpretation. The paper's tail model should not be silently replaced by any regression fitted on a bad-market subsample and then treated as the same theoretical object.

## Why safety-first pricing predicts a tail-beta premium

The theoretical link uses the Arzac-Bawa safety-first equilibrium. Investors maximize expected return subject to a constraint on the probability of suffering a sufficiently large loss. Their equilibrium beta can be expressed as an asset's contribution to the market's loss quantile:

$$
\beta_j^{AB}=\frac{E[R_j^e\mid R_m^e=-\operatorname{VaR}_m(p)]}{-\operatorname{VaR}_m(p)}.
$$

The equilibrium expected excess return is $E[R_j^e]=\beta_j^{AB}E[R_m^e]$. If the admissible tail probability $p$ is below $\bar p$, the conditioning event lies inside the region where the linear tail model applies. Independence and zero residual mean then give $\beta_j^{AB}=\beta_j^T$. Higher tail beta should therefore be associated with higher expected return under these joint assumptions.

The appendix, pages 702-703, relates the derivative of a portfolio quantile to the conditional mean of an asset return at the portfolio quantile. Quantile homogeneity allows the relevant derivative to be evaluated at market portfolio weights. For a smooth joint distribution, the useful derivative identity is

$$
\frac{\partial q_p(w)}{\partial w_j}
=E[R_j\mid w^\top R=q_p(w)].
$$

The conditioning event has probability zero in a continuous model, so the expression is understood through a regular conditional density and suitable differentiability conditions. It is not an ordinary sample average over observations exactly equal to a loss threshold. An implementation or theoretical extension must retain those regularity conditions when applying quantile differentiation.

The empirical rejection is consequently a joint challenge to the safety-first extreme-loss focus, stable estimated exposures, and the relevant investment horizon. It does not identify which assumption fails. The authors suggest that investors may care more about ordinary downside states than rare extremes, may imperfectly perceive differences in tail exposure, or may face delegation incentives that weaken their attention to rare losses.

## Extreme-value estimator and exact construction

Write positive losses as $X_{m,t}=-R_{m,t}^e$ and $X_{j,t}=-R_{j,t}^e$. The heavy-tail approximation is

$$
\Pr(X_m>u)\sim A_m u^{-\alpha_m},\qquad
\Pr(X_j>u)\sim A_j u^{-\alpha_j},\quad u\to\infty.
$$

Smaller tail index means a heavier tail. The estimator combines the market index, a finite-threshold joint-tail probability, and relative marginal loss quantiles:

$$
\widehat\beta_j^T=
\widehat\tau_j(k/n)^{1/\widehat\alpha_m}
\frac{\widehat{\operatorname{VaR}}_j(k/n)}{\widehat{\operatorname{VaR}}_m(k/n)}.
$$

This is equation (5). It is not simply a regression coefficient from the $k$ worst market days. Its marginal asset threshold is based on the asset's own worst $k$ losses, which need not coincide with the market's worst $k$ losses. The intersection count links those two tail sets.

Sort market losses in ascending order, $X_{m,(1)}\leq\cdots\leq X_{m,(n)}$. Equation (6) estimates the reciprocal market tail index with the Hill statistic:

$$
\frac1{\widehat\alpha_m}=
\frac1k\sum_{i=1}^k\log\left(\frac{X_{m,(n-i+1)}}{X_{m,(n-k)}}\right).
$$

The threshold is the $(k+1)$th highest loss, not the $k$th highest. Use corresponding asset and market thresholds for the two VaRs. The tail-dependence estimate in equation (7) is

$$
\widehat\tau_j=
\frac1k\sum_{t=1}^n
\mathbf1\{X_{j,t}>X_{j,(n-k)},\ X_{m,t}>X_{m,(n-k)}\}.
$$

Dates must be aligned before computing this intersection. Ranking each series separately and then pairing its ordered tail observations would destroy the joint-event information. Strict exceedances match the displayed estimator; ties require an explicit convention, especially for thinly traded assets. The source's liquidity filter reduces but does not mathematically eliminate that issue.

The baseline chooses $k=50$ over the preceding 60 months, approximately 1,260 daily observations, so the tail fraction is roughly four percent. The authors also use $k=30$. Asymptotically, $k$ should increase while $k/n$ falls toward zero; with a finite sample there is a bias-variance tradeoff. Smaller $k$ gives noisier estimates, whereas larger $k$ includes states where the tail approximation may be less appropriate. The average estimated market tail index is 3.5.

The estimation theory cited by the paper requires $\alpha_j>\alpha_m/2$. With market tail indices around four, finite asset return variance is a useful sufficient condition in the intended setting. The companion methodology paper supplies the full estimator theory; this article does not repeat all its consistency and asymptotic-distribution arguments. The estimator is applied here principally to rank stocks and evaluate subsequent outcomes.

## Data, formation, and holding-period design

Daily nonfinancial common-stock data come from CRSP for NYSE, AMEX, and NASDAQ from July 1963 through December 2010. Risk-free rates, market excess returns, and benchmark factors come from Kenneth French's data library. The five-year initial history permits monthly portfolio formation from July 1968 through December 2010, giving 510 formation months. Subsequent daily portfolio returns total 10,704 observations in the main tables.

At the start of each month, estimate exposures using only the previous 60 months of daily observations. Exclude stocks reporting zero returns on more than 60 percent of trading days in that window, and exclude stocks priced below US\$5 at the end of the preceding month. The price restriction limits penny-stock effects; the zero-return restriction targets thin trading. The article says that including penny stocks does not qualitatively change its pricing conclusion, but their historical tail betas are less informative about future severe-market performance.

Sort eligible stocks into five equal-count groups. The first analysis sorts on tail beta itself. To isolate risk beyond ordinary market beta, further analyses sort on the tail-beta spread $\widehat\beta_j^T-\widehat\beta_j$. Estimate ordinary market beta from the same historical daily window. Hold the sorted portfolios through the next month and then reform them. Calculate both equal-weighted and value-weighted daily portfolio returns.

For benchmark-adjusted returns, first estimate each stock's factor exposures by historical regressions over the same preceding 60 months. Then subtract the product of these historical exposures and the next month's realized daily factors from the stock's excess return. Average those adjusted stock returns within each portfolio. This is the paper's equation (8), and differs from regressing the full realized portfolio series on factors after portfolio formation.

The zero-investment portfolio is long one unit of the highest-risk group and short one unit of the lowest-risk group. Thus a negative return during crashes is expected if the sorting variable measures crash exposure. Reversing the spread would provide protection, but the long-low/short-high reversal is not the sign used in the principal tables. Unit notional on each side does not mean zero market or factor exposure before adjustment.

The source does not fully document every modern CRSP implementation detail, such as the precise security-code screen, delisting-return integration, all missing-history requirements, or within-month weight drift. These choices should be recorded in an independent reproduction and reconciled against stock counts and reported portfolio moments. They should not be guessed and then attributed to the paper.

## Persistence and characteristics of the sorted portfolios

Table 1 shows why factor controls are necessary. High-tail-beta stocks have average ordinary beta 1.28, versus 0.42 for the low group. Their mean tail-beta spreads are 1.34 and 0.46, implying average tail betas around 2.62 and 0.88. The high group also has higher downside beta, volatility, idiosyncratic risk, and trading volume, and smaller average capitalization. Tail dependence itself differs less sharply, approximately 0.22 versus 0.15, because tail beta also incorporates the scale of marginal losses.

Persistence is evaluated over a 60-month interval, using estimated exposures from nonoverlapping five-year windows. For firms surviving to the later date, Table 2 reports transitions among risk quintiles. Of stocks initially in the highest EVT tail-beta quintile, 49 percent remain there five years later; for the lowest quintile, 61 percent remain lowest. Corresponding ordinary-beta persistence is 53 percent and 59 percent.

By contrast, tail betas obtained by a regression conditional on the 50 worst market days retain only 28 percent in each extreme quintile. This supports the use of the EVT estimator for stable ranking in this sample. It does not imply that every individual beta is estimated precisely or that survivorship in the transition calculation is innocuous. The persistence table conditions on a firm remaining observable and is therefore not a complete account of portfolio risk including exits.

The comparison also clarifies what persistence means. Similar quintile stability to market beta is evidence of cross-sectional structure, not proof that the true coefficient is constant for five years. Firms can change rank moderately while a group-level signal remains useful. The subsequent-loss tests provide a more direct test of whether the historical ranking retains economically relevant information.

## Out-of-sample crash losses and unconditional returns

The main stress event is a daily market excess return below minus two percent. There are 282 such days, approximately 2.5 percent of the return sample. Portfolio assignments were made using earlier data, so averaging their returns on these subsequent event days tests realized crash sensitivity without sorting retrospectively on the realized loss.

In Table 3, the high-tail-beta value-weighted portfolio loses 4.69 percent on an average event day, while the low group loses 1.81 percent. The high-minus-low difference is minus 2.88 percentage points with a reported t-statistic of minus 24.0. Equal-weighted losses are 3.96 percent and 1.49 percent, giving a difference of minus 2.47 percentage points. These are daily conditional averages, not annual returns or cumulative crisis drawdowns.

Unconditional high-minus-low excess returns are approximately zero for equal weights and minus 0.01 percent per day for value weights; neither is significantly positive. Removing observations from 2007 onward leaves the conclusion intact. In that precrisis sample, high- and low-tail-beta value-weighted portfolios lose 4.46 percent and 1.63 percent on adverse days, while the unconditional spread remains nonpositive and insignificant. The missing premium is therefore not solely an artifact of including the global financial crisis.

The tables use Newey-West corrections for unconditional averages but standard t-statistics for conditional adverse-day averages. Crash observations can cluster in time, so the very large conditional t-statistics should not be interpreted as the result of an explicitly crisis-cluster-robust inference procedure. The magnitudes are economically substantial, but an independent replication could assess block or event-level dependence as an additional robustness exercise.

## Incremental risk information after market, size, and characteristic controls

Sorting on tail-beta spreads and subtracting historical Fama-French three-factor exposures reduces the raw crash-return difference substantially, as expected if ordinary beta explains much of it. The residual difference remains meaningful: the equal-weighted high-minus-low adjusted return on adverse days is minus 0.39 percentage points, with t-statistic minus 8.0; the value-weighted difference is minus 0.47 percentage points, with t-statistic minus 4.9. Tail beta therefore contains crash information beyond ordinary factor exposure in the reported design.

The unconditional equal-weighted adjusted spread is positive and borderline significant at t-statistic 2.0, but the value-weighted spread is negative and insignificant. Presorting into five size cohorts resolves this mixed picture. Within each size cohort, sort again on tail-beta spread and evaluate value-weighted portfolios. The average high-minus-low adjusted return across size cohorts is negative, with t-statistic minus 3.2, while the average adverse-day difference is minus 0.44 percentage points, with t-statistic minus 9.0.

The strongest negative unconditional adjusted spreads occur among smaller and medium-sized firms. The largest firms show no meaningful positive premium. This prevents the isolated equal-weighted borderline result from being presented as robust evidence for safety-first pricing. At the same time, differences in crash losses remain present throughout size groups, so the absence of a premium is not simply absence of a measurable exposure.

Table 5 repeats characteristic presorts for downside beta and downside-beta spread, coskewness, cokurtosis, volatility, idiosyncratic volatility, skewness, kurtosis, trading volume, and past return intervals. The return intervals correspond to one month, months two through twelve, and months thirteen through sixty. Adjusted adverse-day high-minus-low differences remain negative, generally between about 0.37 and 0.56 percentage points in magnitude. These tests distinguish tail beta from several related risk and return characteristics.

Other reported robustness checks restrict the sample to the post-January-1973 period or to NYSE stocks; reduce $k$ to 30; replace EVT with conditional regression; estimate benchmark exposures from monthly rather than daily returns; and change the adverse-market cutoff to minus five percent or zero. The authors report qualitative stability. Not all numerical robustness results are tabulated, so one should not attach invented estimates or significance levels to those exercises.

## The downside-beta comparison is deliberately in sample

To compare with earlier downside-beta research, Table 6 estimates betas from the next twelve months and measures returns over those same twelve months. This uses realized future exposures and is not an implementable portfolio forecast. It is a comparison of contemporaneous risk-return associations. The text and table contain a start-date discrepancy, so the table's reported 559 months should be reconciled carefully in a reproduction rather than silently combined with the 510-month main design.

The tail estimator in this exercise uses $k=15$ with about 252 daily observations. The source footnote describes that fraction as approximately eight percent; arithmetically 15 divided by 252 is approximately six percent. The reproducible specification is the stated integer $k=15$, with actual sample size documented separately. This shorter window is acknowledged as less favorable for precise tail estimation.

Realized downside-beta-spread sorting gives an annual excess-return difference of 6.52 percent with t-statistic 5.53. Realized tail-beta-spread sorting gives minus 19.88 percent with t-statistic minus 8.42. The authors explicitly caution that high tail beta and low return can be mechanically related when both are measured over the same crash-containing interval. These numbers must not be advertised as forecast strategy returns. The earlier historical-estimate tests carry the out-of-sample content.

## Portfolio aggregation and the limits of the risk-management application

For nonnegative weights and tail betas, equation (9) implies

$$
\beta_P^T=\sum_jw_j\beta_j^T,\qquad
R_P^e=\beta_P^T R_m^e+\sum_jw_j\varepsilon_j
$$

in the market-tail region. This additivity makes exposure attribution simple: each holding contributes $w_j\beta_j^T$ to systematic tail loading. It does not by itself determine the portfolio's total tail distribution, because idiosyncratic risks remain and can be dependent across assets.

Under additional independence and common tail-index assumptions, heavy-tailed convolution gives the portfolio tail scale

$$
A_P=(\beta_P^T)^{\alpha_m}A_m+\sum_jw_j^{\alpha_m}A_{\varepsilon_j}.
$$

The idiosyncratic scale can be estimated as $\widehat A_j-(\widehat\beta_j^T)^{\widehat\alpha_m}\widehat A_m$, and the portfolio VaR at small probability $p$ is approximately $(A_P/p)^{1/\alpha_m}$. If an idiosyncratic component is thinner-tailed than the market, it vanishes from the leading asymptotic scale. If it is heavier-tailed, it can dominate the asymptotic loss distribution instead.

These conclusions need both the extended tail model and the stated idiosyncratic independence; market independence alone does not imply mutual residual independence. Sectoral shocks or common liquidity shocks can violate the aggregation formula even if the estimated market-tail beta remains informative. Negative estimated residual scales are also possible through sampling error; the article supplies no universal finite-sample repair rule, so any truncation or constrained estimator should be disclosed as an implementation choice.

The authors address the tension between unbounded heavy-tail approximations and simple equity returns bounded below by minus one hundred percent. In sufficiently diversified long-only portfolios, bounded idiosyncratic losses can diversify even when an untruncated asymptotic model would imply dominance by the heaviest individual tail. Systematic exposure cannot be diversified away simply by increasing the number of names. This argument does not extend automatically to short positions with unbounded losses or concentrated portfolios.

The final practical lesson is to use tail beta as a complementary stress-exposure measure. It provides a transparent linear map from an extreme market scenario to expected systematic portfolio response, and the historical evidence supports its cross-sectional ranking power. The evidence does not support assuming investors receive a reliable premium for holding that exposure. Neither does it establish a costless hedge in practice: that conclusion requires implementation costs and constraints absent from the paper. The appropriate distinction is between useful risk measurement, a conditional equilibrium pricing prediction, and a tradable investment strategy; the paper supports the first much more strongly than the latter two.

## Interpreting the estimator and preserving its horizon

The multiplicative form of equation (5) explains why tail beta can differ sharply from a pure crash-probability measure. The ratio of marginal VaRs captures how large an asset's tail losses are relative to the market. The factor $\widehat\tau^{1/\widehat\alpha_m}$ discounts that relative scale according to the frequency with which the asset and market enter their respective tails together. A stock with large standalone losses but little simultaneous market-tail exposure can have a much smaller systematic tail beta than its marginal loss quantile ratio suggests.

For illustration only, take a VaR ratio of three, an estimated joint-tail conditional frequency of 0.20, and a market tail index of 3.5. The tail beta is approximately $3\times0.20^{1/3.5}=1.89$. This calculation uses invented inputs to explain the estimator and is not a reported portfolio result. The power transformation means that a tail-dependence probability is not itself an elasticity or market-loss multiplier. Reading the table's tail-dependence values as direct betas would give the wrong magnitude and units.

With $k=50$, the empirical probability changes in increments of 0.02 when a joint event is added or removed. A zero intersection gives an estimated tail beta of zero through this formula, even though a finite sample cannot prove absence of true tail dependence. Changes in the marginal threshold and Hill index can also alter beta when the intersection count stays fixed. A diagnostic report should therefore save all four ingredients rather than only the final ranking. This makes unstable ranks traceable to co-exceedance counts, marginal tail scales, or the common market-tail estimate.

Investment horizon is a separate limitation from statistical precision. The study conditions on severe **daily** market declines. A severe monthly loss can arise from several modest daily declines without any day crossing the daily threshold. Conversely, a sharp daily crash can reverse within the month. There is no general identity equating a beta estimated on daily crash events with a beta appropriate to a monthly safety-first constraint. The authors explicitly identify this potential horizon mismatch as one reason their pricing results might differ at lower frequency, while recognizing that low-frequency tail estimation has very few observations.

For portfolio stress reporting, this means labeling the scenario and measurement horizon alongside the coefficient. A daily tail beta can support comparisons of daily market-crash sensitivity; using it to forecast annual drawdown, multiweek liquidation losses, or expected shortfall over a different horizon adds assumptions absent from the estimation exercise. The additive coefficient is a useful exposure summary, but it does not remove the need to model the path and horizon of the stress event.

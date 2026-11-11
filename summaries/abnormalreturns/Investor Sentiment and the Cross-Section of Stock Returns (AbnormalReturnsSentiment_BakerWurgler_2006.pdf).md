# Investor Sentiment and the Cross-Section of Stock Returns

Malcolm Baker and Jeffrey Wurgler. *The Journal of Finance* 61(4), August 2006, 1645–1680.

Source: [original PDF](../../Finance/AbnormalReturnsSentiment_BakerWurgler_2006.pdf). This note covers all 36 PDF pages, including the rotated tables and references. PDF page 1 corresponds to journal page 1645. The local article has no separate technical appendix. Unreported working-paper results and tables available from the authors are identified as such; they have not been reconstructed from invented data.

## Why this matters

An unconditional stock-return anomaly can conceal opposing relationships in different market environments. Baker and Wurgler ask whether investor sentiment changes which kinds of stocks subsequently outperform. Their contribution is a systematic conditional cross-sectional test, together with a composite sentiment measure. The main finding is that young, volatile, unprofitable, non-dividend-paying stocks perform relatively poorly after optimistic periods and relatively well after pessimistic periods. Extreme growth and distressed firms share this sensitivity, so a simple growth-versus-distress spread can cancel the phenomenon one wants to detect.

For replication, the broad goal is to distinguish a common market-return forecasting effect from variation in the *relative* returns of different firms. It is also necessary to distinguish these conditional effects from familiar unconditional size, value, and momentum effects. The paper is an empirical asset-pricing investigation, not a specified, costed trading system. Its equal-weighted portfolios emphasize precisely the smaller stocks where execution, shorting, and data problems may be most consequential.

## Economic mechanism and empirical hypothesis

The argument combines two channels. Some firms have unusually subjective valuations: a wide range of future earnings scenarios can plausibly support very different prices. Other firms are difficult to arbitrage because their returns are volatile, borrowing is difficult, or their prices can diverge further before converging. These categories overlap. A young firm without earnings or dividends, for example, may be both difficult to value and expensive to short. Changes in speculative demand therefore affect its price more strongly than the price of a stable dividend payer.

This is a qualitative mechanism, not an estimated structural equilibrium model. The article does not separately identify the strength of the demand and arbitrage channels. It tests their joint prediction using subsequent returns as evidence of correction of initial mispricing. A low subsequent return after high sentiment is consistent with initial overvaluation; it is not direct observation of fundamental value.

The organizing conditional-characteristics specification is equation (1), journal page 1652:

$$
E_{t-1}[R_{it}]=a+a_1T_{t-1}+b_1'x_{i,t-1}+b_2'T_{t-1}x_{i,t-1}.
$$

Here $i$ indexes firms, $T$ is a sentiment proxy, and $x$ contains characteristics. The $a_1$ term permits sentiment to forecast all stocks together. The $b_1$ terms capture unconditional characteristic effects. The interaction vector $b_2$ is the object of interest. A nonzero interaction establishes conditional predictability, but interpretation as mispricing additionally requires considering systematic-risk alternatives. The paper implements this idea mainly through sorts and portfolio forecasting regressions rather than estimating one universal firm-level panel equation.

The historical discussion motivates the chosen characteristics with episodes of speculative enthusiasm. Those examples are supporting context, not independent quantitative tests or a prespecified experimental protocol. The theoretically useful distinction is between stable firms and securities with uncertain valuation and limited arbitrage. It does not imply that every growth firm or every distressed firm is always overpriced.

## Data universe, timing, and characteristic construction

The source uses the merged CRSP–Compustat database and common stocks with CRSP share codes 10 or 11. Firm data extend from 1962 through 2001; the principal monthly-return tests cover 1963–2001. Table I contains 1,600,383 firm-month return observations, with fewer observations for characteristics requiring additional data. Accounting values for fiscal years ending in calendar year $t-1$ are assigned to monthly returns from July $t$ through June $t+1$. This six-month convention is essential: using contemporaneous financial statements would change the information set.

The characteristics are defined in Section III.B and Table I:

| Characteristic | Construction and timing |
|---|---|
| Market equity $ME$ | June price times shares outstanding from CRSP, used for July through the following June |
| Listing age | Years since first appearance on CRSP, measured to the nearest month; this is listing history, not incorporation age |
| Total return risk $\sigma$ | Standard deviation of monthly returns over the 12 months ending in June, requiring at least nine available monthly returns; used in the following July–June interval |
| Profitability | Positive earnings divided by book equity, plus a separate positive-earnings indicator; nonpositive observations form the comparison group |
| Dividends | Dividends divided by book equity, plus a positive-dividend indicator |
| Tangibility | Property, plant and equipment divided by assets, and R&D expense divided by assets |
| Book-to-market | Book equity divided by market equity |
| External finance | Change in assets minus change in retained earnings, divided by assets |
| Sales growth | Change in net sales divided by prior-year net sales; also expressed as a NYSE-based growth decile |

The historical Compustat item numbers matter for reproducing these definitions. Earnings are income before extraordinary items (18), plus income-statement deferred taxes (50), minus preferred dividends (19). Book equity is shareholders' equity (60) plus balance-sheet deferred taxes (35). Dividends are dividends per share at the ex date (26) times shares outstanding (25). PP&E is item 7, R&D is 46, assets are 6, retained earnings are 36, and net sales are 12. Table I adds a fallback omitted from the short prose definition: when the change in retained earnings is unavailable, use net income (172) less common dividends (21).

R&D is not used before 1972. Thereafter, Table I sets missing R&D to zero. This convention mixes genuinely zero expenditure with nonreporting and should be retained when reproducing the table, while being examined separately in robustness work. Less than half of firms report positive R&D even in recent years. The authors explicitly caution about its coverage.

Explanatory variables are winsorized annually at their 0.5th and 99.5th percentiles. The return observations themselves are not said to be winsorized: Table I reports a maximum monthly return of 2,400%. Momentum is the cumulative raw return over months $[-12,-2]$, an eleven-month period excluding the most recent month. It is a control, not one of the focal sentiment-sensitive characteristics.

NYSE breakpoints provide a stable reference for characteristic ranks. Consequently, a decile is not necessarily one tenth of all firms when Nasdaq and other covered stocks are included. A large group first enters CRSP in December 1972 when Nasdaq coverage begins. Excluding those observations from the age analysis reportedly leaves the conclusions unchanged.

There are small but material source-definition ambiguities. Table I's caption calls size and book-to-market logarithms, whereas the displayed summary rows report market equity in millions and a positive book-to-market ratio. Monotone logarithms preserve positive-valued ranks, but they do not preserve moments or linear regression coefficients. The same caption says dividends are scaled by assets, while Section III.B and the table row explicitly use $D/BE$. A faithful reconstruction should use the main-text ratio and report the caption conflict rather than silently treating these descriptions as identical. The article does not fully specify negative-book-equity treatment, all missing-field substitutions, delisting-return adjustments, security-link history, or exact historical database vintages. These are unresolved replication inputs.

## Constructing the annual sentiment indexes

Six proxies are measured annually. They are chosen because each plausibly contains a sentiment component, but each also contains other variation. The common component is meant to reduce proxy-specific noise.

1. **Closed-end fund discount, $CEFD$.** The year-end value-weighted discount of closed-end stock funds relative to net asset value. Larger discounts signify lower sentiment. Data come from Neal and Wheatley for 1962–1993, CDA/Wiesenberger for 1994–1998, and turn-of-year *Wall Street Journal* issues thereafter.
2. **NYSE turnover, $TURN$.** Reported share volume divided by average shares listed, from the NYSE Fact Book. Take its natural logarithm and remove a five-year moving average. Figure 1 describes the past five-year average. This removes part of a strong trend, but not necessarily the structural effect of the May 1975 commission deregulation.
3. **IPO count, $NIPO$.** Annual number of initial public offerings, from Jay Ritter's historical series.
4. **IPO first-day return, $RIPO$.** Annual average first-day IPO return from the same source.
5. **Equity share, $S$.** Gross equity issuance divided by gross equity plus gross long-term debt issuance, based on Federal Reserve data. This includes seasoned equity issues and measures financing composition rather than simply issuance volume.
6. **Dividend premium, $P^{D-ND}$.** The log difference between the value-weighted average market-to-book ratios of dividend payers and nonpayers. A high premium is associated with demand for stable dividend-paying firms and therefore enters the sentiment index negatively.

The timing-selection procedure is part of the estimator. First calculate a principal component using all six current proxies and their one-year lags, giving twelve inputs. Then compare the correlation of this first-stage index with each proxy's current and lagged value. Retain the timing with the stronger correlation for each proxy. Finally compute the first principal component of the correlation matrix of the six selected variables. Standardize the constituent variables and rescale the final index to unit variance, choosing the sign so that high values indicate optimism.

The resulting raw index, equation (2), is

$$
T_t=-0.241CEFD_t+0.242TURN_{t-1}+0.253NIPO_t
+0.257RIPO_{t-1}+0.112S_t-0.283P^{D-ND}_{t-1}.
$$

Every right-hand variable in this equation is standardized; these coefficients cannot be multiplied by raw percentage levels or raw IPO counts. The component explains 49% of the input variance. Its correlation with the twelve-input first-stage component is 0.95. The selected timing is economically plausible because issuance responds to demand with a delay, although closed-end discounts are an exception to the general timing pattern.

To reduce common business-cycle variation, the authors first regress each raw proxy on macroeconomic controls and use the residuals. Section III.C lists industrial-production growth, growth in consumption of durables, nondurables, and services, and an NBER recession dummy. Figure 1 and the table captions additionally list employment growth. This disagreement should be resolved against original code or data; it is not legitimate to assert that the article uniquely specifies the residualization regression.

The orthogonalized index, equation (3), is

$$
T_t^{\perp}=-0.198CEFD_t^{\perp}+0.225TURN_{t-1}^{\perp}
+0.234NIPO_t^{\perp}+0.263RIPO_{t-1}^{\perp}
+0.211S_t^{\perp}-0.243P_{t-1}^{D-ND,\perp}.
$$

It explains 53% of the residual-proxy variance; only the first eigenvalue exceeds one. Orthogonalization changes the historical picture relatively little. This is evidence of robustness to the chosen macro controls, not proof that the index is free of all rational information.

The text discusses proxy data through 2001, whereas Table II summarizes 1962–2000, the end-of-year predictor observations relevant to returns through 2001. The return-year matching is explicit: all monthly observations in calendar year $t$ use the sentiment observation from the end of year $t-1$. In contrast, accounting portfolios use the July–June convention. Both clocks must be implemented.

The PCA loadings, standardization, and timing selection are estimated with the historical sample. They are not described as a real-time recursively estimated signal. For a deployable forecast, one would also need publication dates, vintage data, expanding-window normalization and PCA, and a predetermined method for orienting the component. Such a variant is a new experiment, not the exact historical table reproduction.

## Portfolio sorts and the central numerical evidence

For each month, form equal-weighted characteristic portfolios using NYSE decile breakpoints. Separate nonpositive earnings, zero dividends, zero PP&E, and zero R&D observations where applicable. Classify the month by whether previous-year-end $T^{\perp}$ is positive or negative, then compute average portfolio returns within each regime. Table III reports monthly percentage returns; Figure 2 visualizes the same conditional pattern.

The following spreads use extreme deciles unless specified otherwise. They are not necessarily the same portfolios as the top-three-minus-bottom-three portfolios in the regression tables.

| Return comparison | After high sentiment | After low sentiment | Interpretation |
|---|---:|---:|---|
| Smallest minus largest size decile | −0.26% | 1.45% | The familiar small-stock premium is concentrated in pessimistic states |
| Oldest minus youngest listing-age decile | 0.85% | −0.54% | Age's conditional effect changes sign |
| Highest minus lowest volatility decile | −1.14% | 1.40% | The unconditional relationship obscures opposing regimes |
| Profitable minus unprofitable firms | 0.61% | −0.95% | Stable profitability protects relative performance after optimism |
| Dividend payers minus nonpayers | 0.75% | −0.89% | The same reversal appears for dividend status |

For scale, the smallest size decile earns 2.37% per month after low sentiment and 0.73% after high sentiment. The largest decile earns 0.92% and 0.98%, respectively. The highest-volatility decile earns 2.41% after low sentiment but only 0.30% after high sentiment; the lowest-volatility decile earns 1.01% and 1.44%. These are sample conditional averages, not guaranteed expected returns or net implementable profits.

Tangibility produces weaker evidence. Within positive PP&E observations, low tangibility appears more sentiment-sensitive, but R&D gives little consistent conditional pattern. The paper does not claim equally strong support for all proposed characteristics.

Growth and distress require a nonlinear comparison. Sales-growth deciles 1, 5, and 10 have high-minus-low-sentiment return differences of −1.79, −0.26, and −1.64 percentage points per month. Both tails are sensitive; the middle is relatively stable. Similar patterns appear in external finance and more weakly in book-to-market. A high-minus-low portfolio can obscure this because its two legs respond in the same direction. The economic classification is that very low growth or financing can represent distress, whereas very high values represent speculative growth opportunities.

## Continuous forecasting regressions and factor controls

The regression portfolios use High = top three NYSE deciles, Low = bottom three, and Medium = middle four. Profitability and dividend tests instead compare positive with nonpositive or zero groups. The size and value benchmark portfolios are the Fama–French SMB and HML series, so their construction should not be replaced by a homemade single-sort decile spread without disclosure.

For a characteristic spread $L_{m}$, the basic regression is

$$
L_m=c+dT_{y(m)-1}+u_m,
$$

where $y(m)$ is the calendar year containing month $m$. The controlled version is

$$
L_m=c+dT_{y(m)-1}+\beta RMRF_m+sSMB_m+hHML_m+qUMD_m+u_m.
$$

Omit SMB when SMB is the dependent variable, and HML when HML is the dependent variable. $RMRF$ is the excess value-weighted market return; $UMD$ is the momentum factor using the prior $[-12,-2]$ months. These are contemporaneous return controls used to assess conditional abnormal performance, not information available for a beginning-of-month forecast of realized factor returns.

Table V gives the following orthogonalized-index estimates. Coefficients are percentage points of monthly spread return per one-standard-deviation increase in sentiment. Brackets contain reported bootstrap $p$-values.

| Spread | Univariate $d$ [p] | With factors $d$ [p] |
|---|---:|---:|
| SMB | −0.4 [0.06] | −0.3 [0.15] |
| Old minus young | 0.5 [0.01] | 0.2 [0.04] |
| High minus low volatility | −0.9 [0.00] | −0.4 [0.01] |
| Profitable minus unprofitable | 0.8 [0.00] | 0.4 [0.02] |
| Payers minus nonpayers | 0.8 [0.00] | 0.4 [0.00] |
| High minus medium external finance | −0.4 [0.00] | −0.2 [0.00] |
| Medium minus low external finance | 0.2 [0.00] | 0.2 [0.00] |
| High minus medium sales growth | −0.4 [0.00] | −0.2 [0.00] |
| Medium minus low sales growth | 0.3 [0.01] | 0.2 [0.07] |

A printed 0.00 is a rounded probability, not an exact zero. The raw-index SMB estimate is −0.4 with $p=0.04$, falling to −0.3 with $p=0.08$ after factor controls. Thus the size result is less robust statistically than a blanket statement that every pattern survives adjustment would suggest. The controlled orthogonalized PP&E and R&D coefficients are both 0.1, with $p=0.53$ and $0.62$. The book-to-market tail comparisons are also not reliably significant. This selectivity is part of the result.

Inference is bootstrapped to address predictive-regression bias when persistent sentiment innovations correlate with return innovations, following the concern emphasized by Stambaugh. The article does not give the full resampling algorithm, number of draws, seed, or precise predictor-dynamics estimator. Ordinary independent-month standard errors would ignore both annual predictor repetition and persistence. Exact reproduction of the reported bootstrap probabilities therefore requires additional information; estimating the displayed OLS slopes alone does not reproduce inference.

The text compares residualized-proxy prediction to adding macro controls directly. The underlying linear-projection intuition is useful, but an index re-estimated through PCA and timing selection is not automatically algebraically identical to every regression using the raw index and macro controls. Replication should implement the stated residualization and PCA procedure rather than substitute a presumed equivalent model.

## Robustness, earlier history, and systematic risk

The reported main patterns survive a post-1982 indicator and become slightly stronger when January and December returns are excluded. The latter check argues against tax-related turn-of-year trading as the sole explanation. Using sentiment above or below one standard deviation strengthens the sorts. Defining high and low sentiment relative to a trailing ten-year average gives similar, somewhat weaker results while losing more than a quarter of the sample. Results for individual sentiment proxies are described as broadly consistent, but their detailed tables are in the working-paper version rather than this PDF.

For 1935–2001, the authors build a reduced sentiment index from closed-end discounts, the equity issuance share, and lagged turnover. Accounting-based characteristics are unavailable for the full early period, so tests focus on size, age, volatility, and dividend status. The early-sample orthogonalization uses consumption growth and recession indicators; the generic Table VI caption incorrectly repeats the six-proxy/industrial-production description from the later-sample setup. The main-text three-proxy design should govern this exercise.

Across 1935–2001, the factor-controlled orthogonalized coefficients are −0.2 for SMB ($p=0.07$), 0.1 for age ($p=0.26$), −0.4 for volatility ($p=0.00$), and 0.4 for payer status ($p=0.01$). The 1935–1961 evidence is less uniform. Raw-index volatility and dividend coefficients are −0.8 and 0.9, both with $p=0.01$, but orthogonalized versions are weaker. Early age results can have the opposite sign. Listing age is less informative about genuinely young firms before Nasdaq coverage.

The paper describes an additional past-data forecasting exercise comparing RMSE reductions with in-sample reductions. It says much of the predictability would have been knowable, except age and post-1980 SMB. The numerical table and complete estimation schedule are not supplied. This claim cannot be converted into a documented out-of-sample Sharpe ratio or quantified forecast improvement from the local source.

To test a conditional CAPM explanation, estimate the spread on sentiment, the market excess return, and their interaction. In directly estimable notation,

$$
L_m=c+dT_{y-1}+bRMRF_m+kT_{y-1}RMRF_m+u_m.
$$

The printed equation writes $b=\beta e$ and $k=\beta f$; only the products are identified by this regression. A beta-based explanation predicts a suitable alignment between $k$ and the earlier return-predictability coefficient. Most significant interactions have the wrong sign. There is an exception for high-minus-medium book-to-market, so the test does not reject every risk-related pattern. Table VII uses heteroskedasticity-robust probabilities. These checks challenge a simple conditional market-beta account; they cannot exhaust all rational multifactor models or prove that orthogonalized sentiment is causally exogenous.

## Earnings-announcement test

The final test asks whether sentiment forecasts corrections around earnings news. Quarterly announcement dates come from the merged CRSP–Compustat file. For each firm-quarter, calculate cumulative abnormal return relative to the value-weighted market over trading days $[-1,+1]$. Average these event returns within characteristic deciles by calendar quarter, then regress the quarterly series on previous-year-end sentiment.

The text says dates become available in January 1971; Table VIII is headed 1973–2001. This difference in availability versus reported estimation window needs checking in replication. Coverage is about 75% of the relevant firm observations. The article does not specify every treatment of multiple announcements, nontrading dates, or missing returns.

Most coefficients are negative. The smallest-size decile has a −0.18 percentage-point event-return coefficient ($p=0.03$); the highest-volatility decile has −0.30 ($p$ rounded to 0.00). The unprofitable group has −0.31 and nonpayers −0.18. Twelve of 104 coefficients are significant at 5%, with no stated multiple-testing adjustment. Six overlap the strongest conditional-return cells in Table III, with matching signs. These magnitudes apply to three-day announcement windows, not monthly returns.

The authors regard this as partial evidence for correction of earnings-expectation errors. The event study misses repricing of other firms when one firm's announcement changes beliefs about an entire sector. Its proposed “lower bound” interpretation is economic reasoning about omitted spillovers, not a formally identified bound that eliminates selection, confounding news, or measurement error.

## Reproduction priorities and limits

A useful implementation should preserve the two timing calendars, the selected sentiment lags, constituent standardization, and the distinction between decile sorts and three-decile regression portfolios. Verify the reported return counts and conditional averages before trying to match inference. Retain separate high-minus-medium and medium-minus-low portfolios; a single high-minus-low sort loses one of the central contributions. Check every coefficient in monthly percentage-point units.

The main unresolved inputs are historical source vintages, exact macro controls, PCA estimation endpoints, turnover moving-average endpoint convention, database linking and exclusions, and the bootstrap details. The article supplies no transaction costs, borrow fees, capacity constraints, turnover budget, leverage rule, or executable sentiment-timing allocation. Such additions are necessary for an investment application but should be labeled new design choices.

The durable finding is that sentiment interacts with firm characteristics in a structured, often nonlinear way. Several characteristics with modest unconditional explanatory power become informative conditional on sentiment. The evidence is strongest for volatility, profitability, dividend status, and the extreme-growth/distress comparisons, while tangibility and some adjusted size and book-to-market results are weak. The model-building implication is to allow conditional cross-sectional effects and overlapping demand/arbitrage channels; the implementation implication is to reproduce the information set and nonlinear portfolio comparisons before assigning economic meaning to apparent predictive performance.

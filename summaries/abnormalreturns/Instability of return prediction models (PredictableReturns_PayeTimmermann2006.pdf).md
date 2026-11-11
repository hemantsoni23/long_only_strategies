# Instability of return prediction models

Bradley S. Paye and Allan Timmermann. *Journal of Empirical Finance* 13 (2006), 274–315. DOI: 10.1016/j.jempfin.2005.11.001. Source: `Finance/PredictableReturns_PayeTimmermann2006.pdf`, 42 PDF pages. Journal page 274 is PDF page 1. The empirical samples end in December 2003; all stability statements in this note refer to those historical samples.

## Question, contribution, and scope

Return forecasting commonly assumes that the mapping from dividend yields, interest rates, term spreads, and credit spreads to expected stock returns is stable. Paye and Timmermann investigate that assumption directly across international markets. Their question is not simply whether a full-sample regression has a significant slope, but whether the slope vector changes, when those changes occur, and whether the predictable component becomes weaker afterward.

The paper's empirical contribution is a systematic international analysis of multiple structural breaks in conventional return-prediction models. It studies ten OECD markets over 1970–2003 and longer US and UK histories over 1952–2003. It estimates break dates and regime-specific coefficients instead of imposing an arbitrary early/late sample split. Most multivariate models display instability, and many have lower ex post explanatory power after the latest estimated break. The timing is heterogeneous, with some evidence of clusters rather than one universal global change.

Its methodological contribution is equally important. Persistent valuation ratios with innovations correlated with stock returns can make conventional break tests reject stability far too often. The authors simulate these finite-sample problems and compare several tests and model-selection procedures. The Elliott–Müller instability test behaves much better in the examined monthly settings, while ordinary supremum-F procedures can substantially overfit. The paper therefore does not treat every estimated breakpoint as equally credible.

The analysis is explicitly retrospective. Break dates use the full sample and cannot be presumed known at the time of the break. High regime-specific $R^2$ values describe an ex post partition, not the performance of an executable strategy. The study motivates better treatment of parameter instability in forecasting and allocation; it does not deliver a validated online break detector or a net-of-cost trading rule.

## Piecewise-linear conditional-return model

For a given market, let $r_t^e$ be its monthly excess return and let $x_{t-1}$ include a constant and predictors known one month earlier. With $K$ breaks, the model is

$$
r_t^e=\beta_k'x_{t-1}+\varepsilon_t,\qquad T_{k-1}<t\leq T_k,\quad k=1,\ldots,K+1.
$$

The coefficient vector is constant within each segment and changes at unknown dates. The multivariate specification contains local dividend yield, local short rate, local term spread, and the US default premium:

$$
r_t^e=\beta_{0k}+\beta_{1k}DY_{t-1}+\beta_{2k}TB_{t-1}+\beta_{3k}TS_{t-1}+\beta_{4k}DS^{US}_{t-1}+\varepsilon_t.
$$

All five coefficients may change at each break. The authors avoid imposing a prior distinction between stable and unstable predictors because they lack a strong economic basis for that restriction. Univariate models retain the constant and one predictor, permitting easier interpretation and potentially greater power when only a subset of the multivariate coefficients changes.

For a proposed set of break dates, ordinary least squares is fitted separately in every segment. The date estimates minimize total residual sum of squares:

$$
(\widehat T_1,\ldots,\widehat T_K)=\arg\min_{\{T_j\}}\sum_{k=1}^{K+1}\sum_{t=T_{k-1}+1}^{T_k}(r_t^e-\widehat\beta_k'x_{t-1})^2.
$$

Admissible partitions require each segment to contain at least a fraction $\pi$ of the full sample. The baseline trimming fraction is 15%. This corresponds to roughly seven years and eight months in the long sample and five years and one month in the shorter sample. The constraint prevents a handful of outliers from being fitted as a separate regime, but it also excludes genuine changes near sample boundaries or close to another break.

The step-function representation is an approximation. Monetary-policy changes, institutional reforms, or major shocks may produce discrete changes, but gradual parameter drift can also trigger a break test. A significant result therefore establishes instability relative to a constant-coefficient model, not proof that economic coefficients literally jumped once on the estimated calendar date.

## Break tests and selection of the number of regimes

The Bai–Perron supremum-F statistic tests no breaks against a specified number of breaks, maximizing over admissible locations. Related sequential tests compare $l$ with $l+1$ breaks. The sequential selection procedure starts with a stable model, adds a break when the corresponding test rejects, and stops when it does not reject or reaches the allowed maximum. The paper reports selection at both 10% and 5% significance levels.

A double-maximum statistic, UDMax, tests stability against an unknown number of breaks. This matters because some patterns are difficult to detect with a single break. For example, a coefficient that changes in the middle of the sample and then returns to its original value can appear nearly stable under a one-break approximation. The authors nevertheless initialize their main sequential procedure with the one-break test, a conservative choice that can miss such patterns.

The Hansen fixed-regressor bootstrap permits changes in the predictor distribution and heteroskedastic regression errors. That is valuable because a changing distribution of yields or rates can affect ordinary asymptotic break-test distributions. However, the implementation discussed permits only a single break and does not allow serial correlation in the regression disturbance. This limitation becomes serious when overlapping multi-month returns are used.

The Elliott–Müller J-test is a broad instability test with power against both rare large changes and many smaller changes. It uses standardized regression scores and auxiliary detrending regressions instead of repeatedly splitting the sample. It allows heteroskedasticity, serial correlation, and weakly endogenous regressors, but not regressors with stochastic trends. It is useful for corroborating instability rather than selecting a particular number and placement of breaks.

The article describes the J-test's construction at a conceptual level and refers to its original methodological source for the full algorithm. Reproducing that statistic therefore requires a faithful implementation of the cited method, including its covariance estimation and tuning conventions. Treating it as an ordinary CUSUM or as a supremum-F statistic with different critical values would not replicate the study.

## Why persistent predictors can produce spurious breaks

The size experiments use

$$
y_t=\alpha+\beta x_{t-1}+e_t,\qquad x_t=\theta+\phi x_{t-1}+v_t,
$$

with Gaussian innovations and contemporaneous correlation $\rho=\operatorname{Corr}(e_t,v_t)$. The simplest design sets the intercepts and predictive slope to zero and both innovation variances to one. Predictor persistence takes values 0, 0.9, 0.95, and 0.98, while innovation correlation is either zero or $-0.9$. Every experiment uses 500 observations and 2,000 Monte Carlo replications, with nominal test size 10%.

Persistence alone produces modest distortions, and strong innovation correlation without persistence is also relatively benign. Their combination is damaging. At $\phi=0.98$ and $\rho=-0.9$, SupF(1) rejects a truly stable model 41.2% of the time, SupF(2) 68.2%, and UDMax 63.7%. The Hansen bootstrap rejects 33.0%. The J-test rejects only 6.1%, slightly below its nominal level. Sequential model selection chooses no break only 58.9% of the time even though none exists.

The mechanism is related to predictive-regression bias. With a persistent endogenous predictor, the estimated return slope is biased and in-sample fit is inflated. Splitting the history into shorter segments increases that bias, making the fall in residual sum of squares look like evidence for a structural change. Searching across many split locations intensifies the problem. The J-test avoids this particular repeated-splitting mechanism.

The second calibration uses actual US estimates from July 1952 through December 2003. Dividend-yield persistence is 0.98846 and its innovation correlation with returns is $-0.92175$. Short-rate persistence is 0.97534, term-spread persistence 0.94091, and default-spread persistence 0.97213; their return-innovation correlations are much closer to zero. In the dividend-yield calibration, SupF(1) rejects 56.1% of stable samples and UDMax 81.0%, compared with 6.4% for the J-test. Even the other calibrated predictors produce notable supremum-F distortions, so near-zero correlation is not a guarantee of perfect finite-sample behavior.

BIC is conservative in these no-break experiments, choosing stability in about 96–99% of calibrated cases. That sounds attractive, but the power experiments reveal its cost. A procedure that rarely invents breaks may also fail to detect economically important ones in noisy returns.

## Power experiments and the cost of conservative selection

The power design introduces one break exactly at observation 250 of a 500-observation history:

$$
y_t=\begin{cases}(\beta^*-\delta/2)x_{t-1}+e_t,&t\leq250,\\
(\beta^*+\delta/2)x_{t-1}+e_t,&t>250.\end{cases}
$$

The predictor remains an AR(1), innovations have unit variance, and the two shocks are uncorrelated. The mean coefficient $\beta^*$ is selected to correspond to a full-sample signal level of 5% or 10% $R^2$. Break magnitudes range from 10% to 100% of that mean coefficient. The midpoint is favorable for detection because both regimes have substantial observations; breaks near the ends would be harder.

Tests are size-adjusted using empirical critical values from 5,000 no-break simulations, then evaluated over 2,000 break simulations. This adjustment is necessary: comparing raw rejection frequencies would otherwise reward an oversized test for falsely rejecting more often. At 5% signal and a break equal to only 10% of the mean coefficient, power is around the nominal 10% level for all procedures. Such a change is effectively undetectable in this design.

With a 100% break and 5% signal, SupF(1) power is 57.1% for a nonpersistent predictor and 41.8% at persistence 0.98. The J-test has corresponding power 56.8% and 45.4%. Its favorable size does not require a large sacrifice in size-adjusted power. At 10% signal and the largest break, SupF(1) power ranges from 70.3% to 87.3% across persistence cases; J-test power is similar.

BIC misses most breaks. With 5% signal and the largest break, it still chooses no break around 89–91% of the time. At 10% signal in the most favorable nonpersistent case, it selects the correct single break only 44.1% of the time, compared with about 82.6% for sequential selection. The authors therefore use the imperfect sequential procedure for dating and count selection, while relying on the J-test to assess whether its evidence is credible.

## International data and measurement

The broad dataset contains monthly local-currency equity total returns for Belgium, Canada, France, Germany, Italy, Japan, the Netherlands, Sweden, the UK, and the US from January 1970 through December 2003. Data are primarily from Global Financial Data. The long dataset covers the UK and US from July 1952 through December 2003. It trades geographic breadth for a longer span useful in detecting early changes.

Country indices include the Belgian CBB All-Share, Toronto SE-300, French SBF-250, German CDAX, Japanese Nikko Securities Composite, Italian BCI Global, Netherlands All-Share, Swedish Affarsvärlden Return Index, UK FTA All-Share, and US S&P 500. US robustness checks add CRSP value-weighted NYSE and NYSE/AMEX/NASDAQ portfolios. These are distinct market universes, not interchangeable labels for the same return series.

Dividend yield is the prior twelve months' distributions divided by current price, expressed as an annual rate. The short rate is a local three-month Treasury bill rate, and the term spread is the local long-government-bond yield minus that short rate. The default premium is Moody's US Baa yield minus Aaa yield for every country because comparable local series are unavailable. It therefore represents a common US credit condition, not country-specific default risk.

Excess returns subtract the relevant local short rate. The additional CRSP indices use a one-month risk-free series from the CRSP Risk Free Rates File, based on average prices. A replication must preserve this difference and convert annualized rate quotations to units consistent with monthly returns. Mixing annual rate units and monthly decimal returns would change slope magnitudes substantially even if some test statistics remained invariant to a consistent rescaling.

Table 4's stable-model benchmarks have weak explanatory power. Most univariate $R^2$ values are below 1%; the largest is 3.03% for UK dividend yield in the short sample. Multivariate fit improves, reaching 9.08% for the UK, 3.90% for the US, and only 0.37% for Italy in the shorter sample. These low signal levels explain why both false positives and low power require explicit simulation analysis.

## Evidence for instability and how strong it is

Multivariate instability is widespread. The break tests generally reject stability outside Italy, and the J-test corroborates instability for the country models except Sweden and Italy. Canada is supported at the weaker 10% level in the reported table. This corroboration is important because the multivariate model contains the problematic dividend-yield predictor but also other state variables.

At the 10% sequential-selection level, the long-sample NYSE and S&P 500 models have two breaks, the broader CRSP index one, and the UK two. In the ten-country sample, six markets receive one break, Germany, Sweden, and the US receive two, and Italy receives none. Most selections are similar at the 5% level, although the long US models can move from two breaks to one.

Univariate dividend-yield evidence is much weaker. Supremum-F tests often reject, but J-test confirmation is rare. The article explicitly cautions that these may be spurious break detections caused by the persistence/endogeneity problem. It is therefore inconsistent to summarize the paper as proving a dividend-yield breakdown in every market where the sequential algorithm places a breakpoint.

Evidence for short-rate, term-spread, and default-spread changes also differs across tests and samples. A long-sample US term-spread break is relatively well supported, while some short-rate breaks lack J-test corroboration. The default-premium results are mixed, with stronger agreement for the UK. No detected break is not affirmative proof of stability, given the weak power documented in the simulations.

## Timing and economic size of selected breaks

For long-sample US short-rate regressions, the algorithm identifies breaks in September 1962 and August 1974. In the NYSE specification the slope moves from $-16.79$ to $-11.76$ to $-0.94$, while segment $R^2$ values move from 11.6% to 13.8% to 0.3%. The S&P 500 shows a similar pattern: slopes $-17.82$, $-11.78$, and $-0.97$, with fit 12.1%, 14.8%, and 0.3%. The strong negative relation is concentrated before the mid-1970s.

The UK short-rate model has an estimated October 1974 break. Its slope changes from $-9.12$ to 1.25 and fit falls from 12.5% to 0.4%. For the US term spread, a May 1975 break divides a strong early relation from a weak later one: the S&P slope changes from 18.91 to 1.77 and fit from 8.7% to 0.2%. The date confidence intervals are broader than the point estimates, and they encompass the oil-shock period.

The long-sample multivariate S&P model differs from the univariate timing. Its breaks occur in July 1987 and March 1995, with segment fit 9.5%, 21.3%, and 9.9%. Dividend-yield slopes are 0.56, 9.75, and 4.16. Such large changes indicate that full-sample coefficients average very different conditional relations, but their standard errors are also substantial. The broad CRSP market has a single July 1987 break and fit declines from 9.6% to 7.3%.

European multivariate breaks cluster around the late 1970s and early 1980s: January 1978 in France, August 1981 in the Netherlands, October 1981 in Belgium, and December 1982 in Germany. France's fit falls from 18.2% to 2.4%, the Netherlands' from 22.4% to 5.4%, and Belgium's from 9.8% to 7.3%. Canada also has a January 1978 break, with fit falling from 14.9% to 8.2%.

Declining predictability is not universal. Japan's multivariate model has a May 1996 break and fit rises from 5.6% to 12.7%. Germany's fit rises from 9.2% to 11.9% after its second estimated break in July 1994. The long UK model retains 19.1% fit after its November 1974 break, lower than the preceding segment's 29.1% but still high. These exceptions matter for any claim of a worldwide disappearance of return predictability.

## Common-break tests and economic narratives

The authors suggest that the 1974–1975 changes may be related to the oil shock and that late-1970s European changes may relate to the founding of the European Monetary System in 1979. These are plausible interpretations of timing, not identified causal estimates. Other contemporaneous changes, overlapping confidence intervals, and the model's limited predictors prevent causal attribution.

A formal multivariate test using the Qu–Perron framework supports a common US–UK break in the long sample. The supremum likelihood-ratio statistic is 41.7, significant at 5%. The estimated date is November 1974, with a 90% interval from December 1973 to March 1975. This is stronger evidence for shared timing than merely noting two nearby separate estimates.

By contrast, the null of no joint break is not rejected for all ten markets or for the selected European group of Belgium, France, Germany, the Netherlands, and Sweden over 1970–2003. Thus visual clustering does not establish a single European structural event statistically. Increasing the number of countries increases the number of coefficients, and weak signal or changes in only a subset can dilute test power. The paper preserves this negative result rather than claiming all clustered dates are one common break.

## Robustness exercises

The payout extension constructs a US total-payout yield using annual Compustat repurchases plus dividends. Repurchases are purchases of common and preferred stock less reductions in preferred stock outstanding. Year-end repurchases are scaled by year-end market capitalization, and the denominator is updated during the following year using S&P 500 total returns as a proxy for market-value changes. Before the repurchase data begin in 1972, the payout yield equals dividend yield.

The total-payout regression still has an estimated break, in November 1994. Its slope moves from 0.61 to 4.70, compared with 0.40 to 7.46 in the short-sample dividend-yield regression. The extension suggests that substituting repurchases for dividends does not by itself remove the estimated instability. It remains subject to the earlier warning about inference with persistent endogenous yield measures and uses an approximate monthly repurchase series rather than directly observed monthly repurchases.

Changing the trimming fraction generally preserves the presence of breaks, though dates near admissible boundaries shift. The reported table compares 10%, 15%, and 20% trimming; the text discusses a broader range. At 20%, no more than three breaks are allowed, while other reported settings allow up to five. A 1994 break can become infeasible in a long history when the final segment must cover too large a fraction, forcing the estimated split earlier.

Adding squared or squared-and-cubed predictor terms, constrained to be stable, usually leaves instability in the linear terms intact. This addresses one form of omitted nonlinearity but does not exhaust possible nonlinear conditional-return models. The paper also studies overlapping two-, four-, and six-month cumulative returns. Many monthly breaks persist, but extra breaks appear and require caution because finite-sample distortions grow with horizon.

In the six-month simulation with persistence 0.98 and uncorrelated innovations, the Hansen bootstrap rejects stability 97.7% of the time and the J-test 21.4%, against a nominal 10%. Even robust procedures are imperfect once overlap becomes substantial. The authors accordingly stop at six months and avoid treating additional long-horizon breaks as unambiguous corroboration.

## Reproduction requirements and implications

A faithful implementation should first reproduce stable-model coefficients and predictor innovation properties, then run the simulated size and power designs before interpreting empirical break dates. It should retain local-currency returns, country-specific rates, the shared US credit spread, one-month predictor lags, HAC standard errors, trimming constraints, and the distinction between testing instability and selecting its representation. Dates should be reported with the 90% intervals, not as exact observed economic transition times.

Several implementation details must be obtained from the cited econometric procedures or associated code rather than inferred from the article: the complete J-statistic algorithm, exact covariance-estimator settings, bootstrap conventions, and numerical optimization details. The source mentions GAUSS simulations and use of Hansen's programs but does not supply a modern executable end-to-end data pipeline or a random seed. These omissions limit exact numerical reproducibility without invalidating the reported experimental design.

The paper's allocation implication is that the amount of history used to estimate expected returns is itself a modeling decision. Discarding all pre-break data reduces bias but can sharply increase estimation variance, especially after a recent change. Keeping some earlier data can be optimal when the break is modest and the new segment is short. The article discusses this trade-off but does not empirically choose an optimal live estimation window.

A complete investment model would also need a probability of future breaks and a distribution for coefficients after a break, making future returns a mixture over regimes. Those quantities are outside this retrospective study. The defensible conclusion is therefore narrower and useful: conventional conditional-return relations often change, conventional break tests can overstate that fact unless calibrated for financial predictors, and neither a stable full-sample fit nor a hindsight-selected regime fit should be treated as an automatically reliable forecast.

## Reading regime fit without turning hindsight into a strategy

There are two reasons a segment's reported $R^2$ can exceed the full-sample value. One is substantive: a stable regression averages different coefficient vectors, obscuring a relationship that is stronger within a regime. The other is mechanical: searching for breaks and fitting more coefficients reduces residual sum of squares. The article's test procedures attempt to assess whether that improvement is too large to attribute to noise, but the selected segment fit still benefits from the search. It is not an unbiased estimate of attainable forecast accuracy.

Comparing fit across segments also changes the denominator of $R^2$. A lower post-break value can reflect weaker predictable variation, greater unexplained volatility, or both. The paper therefore reports coefficients and standard errors alongside fit, allowing a reader to inspect whether slopes have weakened, reversed, or become imprecisely estimated. Large coefficient changes with wide intervals warrant a different interpretation from a precisely estimated collapse in a previously strong short-rate relation.

Finally, the same calendar year may be detectable in one sample and excluded in another. A 1974 break cannot be selected in a sample beginning in 1970 when the minimum initial regime exceeds five years. Failure to find it in that shorter dataset is therefore partly a design constraint, not independent evidence that other markets escaped the event. The long US–UK history is valuable precisely because it makes early-1970s changes admissible and leaves enough observations on each side to estimate their consequences.

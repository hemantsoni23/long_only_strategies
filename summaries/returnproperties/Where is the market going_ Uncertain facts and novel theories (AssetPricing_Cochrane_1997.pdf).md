# Where is the market going? Uncertain facts and novel theories

John H. Cochrane, *Economic Perspectives*, Federal Reserve Bank of Chicago, November/December 1997, pp. 3–37. Source: [AssetPricing_Cochrane_1997.pdf](../../Finance/AssetPricing_Cochrane_1997.pdf). The local PDF is the entire 40-page issue: this note covers Cochrane's article and its appendix, notes, and references, excluding issue front matter, the conference announcement, and annual index. Page pointers below use printed pages, which coincide with PDF pages.

## Why this matters and what the article contributes

The article connects three questions that are often analyzed separately: how precisely historical stock returns identify the equity premium, whether high valuation ratios imply low subsequent expected returns, and what economic models can simultaneously explain the premium, its variation, consumption, and interest rates. Its contribution is a quantitative synthesis and a set of diagnostic calculations rather than a new estimator or a fully specified trading strategy. The historical setting matters: observations end in 1996, forecasts are made in 1997, and assessments of which models work refer to research available then.

Cochrane argues that the postwar U.S. excess stock return of roughly 8% is an uncertain estimate of a long-run expectation. High price ratios provide evidence of unusually low conditional expected returns, but neither claim implies that everyone should sell. In equilibrium someone must hold outstanding equity; a portfolio recommendation requires understanding how an investor's risks and preferences differ from those of the marginal holder. Economic models are useful precisely because they make those differences explicit.

For replication, the article has two layers. Its historical moments and predictive regressions can be reconstructed with annual market, Treasury-bill, dividend, and inflation series. Its habit, incomplete-market, and production discussions are worked mechanisms and summaries of other papers. The article does not provide enough calibration and numerical-solution information to reproduce all of those underlying papers. Those omissions should not be filled by treating schematic examples as complete calibrated economies.

## Historical moments and uncertainty about the premium

Table 1 uses annual observations for 1947–1996. Real returns are CRSP nominal asset returns less consumer-price inflation. The value-weighted NYSE portfolio has mean 9.1% and standard deviation 16.7%; the S&P 500 has 9.5% and 16.8%; the equal-weighted portfolio has 11.0% and 22.2%. Long government bonds have mean 1.8% and volatility 11.1%; corporate bonds, 2.1% and 10.7%; Treasury bills, 0.8% and 2.6%. Reported standard errors of the means are respectively 2.4, 2.4, 3.0, 1.6, 1.5, and 0.4 percentage points.

The resulting stock–bill spread is approximately 8%, and its Sharpe ratio is near 0.5. This is an economically large reward relative to measured risk. It is not simply a story about Treasury bills having special liquidity services: attractive mean–variance opportunities also appear when comparing stocks with long bonds or considering stock portfolios alone. Levering a risky portfolio with a risk-free asset scales its excess mean and volatility together and therefore leaves its Sharpe ratio unchanged.

Under an independent, stationary sampling approximation, the standard error of a mean is

$$
\operatorname{se}(\bar r)=\frac{\sigma_r}{\sqrt T}.
$$

Taking annual volatility to be 17% gives standard errors of 7.6, 5.4, 3.8, and 2.4 percentage points for samples of 5, 10, 25, and 50 years. Even fifty years leave an approximate 95% interval of roughly 3%–13% around an 8% excess mean. This is frequentist sampling uncertainty conditional on the statistical assumptions, not a posterior probability that the true premium lies inside those endpoints.

Two additional uncertainties are outside that elementary calculation. First, the United States is a surviving, unusually successful national market; choosing it after observing success introduces selection. Second, a sample without rare disasters may understate both tail risk and uncertainty about expected returns. Investors may have required compensation for events that never occurred during the realized sample. An ex post average therefore need not equal the expected premium investors required at the beginning of the period.

Long investment horizons do not automatically solve these problems. With independent returns, an additive return's mean grows with horizon and its standard deviation with the square root of horizon. The variance of its annualized average falls, but uncertainty about total wealth does not disappear. Table 2 scales historical means by horizon and volatilities by the square root of horizon. For horizons of 1, 2, 3, and 5 years, the normalized means are 8.6%, 9.1%, 9.2%, and 10.5%, while normalized volatilities are 17.1%, 17.9%, 16.8%, and 21.9%. The corresponding normalized Sharpe ratios are 0.50, 0.51, 0.55, and 0.48. These results do not establish a dramatic horizon-based improvement in investment opportunities.

## Predictive regressions: inputs, timing, and results

The central experiment regresses a future holding-period stock return, in excess of the corresponding continuously reinvested Treasury-bill return, on the price/dividend ratio observed at the forecast date. For horizon $k$,

$$
R^e_{t\rightarrow t+k}=a_k+b_k(P_t/D_t)+\varepsilon_{t+k}.
$$

$P_t/D_t$ is the value-weighted NYSE price/dividend ratio. The return is the subsequent $k$-year holding-period return; it is not the contemporaneous return associated with the predictor. Table 4 also estimates dividend-growth regressions with the same predictor. The article uses annual postwar data, with the last completed observations in 1996. Its table reports heteroskedasticity- and serial-correlation-corrected GMM standard errors; it does not provide the exact covariance bandwidth, kernel, vintage of each series, or complete data-construction code.

| Horizon | Return slope | Standard error | Return $R^2$ | Dividend-growth slope | Standard error | Dividend-growth $R^2$ |
|---|---:|---:|---:|---:|---:|---:|
| 1 year | −1.04 | 0.33 | 0.17 | −0.39 | 0.18 | 0.07 |
| 2 years | −2.04 | 0.66 | 0.26 | −0.52 | 0.40 | 0.07 |
| 3 years | −2.84 | 0.88 | 0.38 | −0.53 | 0.43 | 0.07 |
| 5 years | −6.22 | 1.24 | 0.59 | −0.99 | 0.47 | 0.15 |

The slopes use the article's return and ratio scaling; a replication must match those units before comparing coefficients. A high price relative to dividends predicts a lower return, with larger cumulative effects at longer horizons. It predicts little dividend growth, and the estimated dividend-growth association has the opposite sign from the simple story that high valuations forecast strong dividends.

Long-horizon observations overlap and the predictor is persistent. A high five-year $R^2$ should therefore not be interpreted as many independent successful forecasts. Cochrane emphasizes that the sample contains only a few slow valuation episodes: low prices in the 1950s, high valuations before the 1970s, and low valuations before the subsequent boom. More sophisticated inference can weaken apparent significance substantially; the article characterizes predictability evidence as having about a 10% probability value before accounting for specification search. It does not reproduce that entire testing literature or claim its conventional table standard errors settle the issue.

Persistent expected returns explain why explanatory power rises with horizon. If one-period returns respond to a persistent state, many small predictable components accumulate. This does not create a high-frequency arbitrage. The article estimates that timing on these slow signals improves unconditional mean returns by only around one percentage point at comparable volatility in the examples discussed, rather than turning a 60% five-year $R^2$ into near-certain short-term profits.

Dividend repurchases and changing payout practices may alter $P/D$, but earnings, book values, and smoothed-price denominators provide related evidence. Figure 2 shows that $P/E$ and $P/D$ rise together near the sample end. That comparison weakens a purely dividend-policy explanation for high valuations; it does not prove constant long-run valuation means or eliminate all structural-change explanations.

## Reconstructing the 1997 forecast exercise

The forecast combines the return regression with an autoregression of the predictor:

$$
x_{t+1}=\mu+\rho x_t+u_{t+1},\qquad
E_t[R^e_{t+1}]=a+b x_t,\quad x_t=P_t/D_t.
$$

Iterating the state equation gives

$$
E_t[x_{t+h}]=\bar x+\rho^h(x_t-\bar x),\qquad \bar x=\mu/(1-\rho).
$$

One-period expected returns at later dates follow by substituting this conditional expectation into the return regression. These are forecasts of future one-year expected returns, not automatically annualized compounded returns earned from the initial date through that horizon.

The estimated predictor persistence is 0.90. Footnote 3 reports simulations illustrating downward finite-sample bias: a true coefficient of 0.90 produces an estimated median around 0.83 and standard deviation 0.09; a true coefficient of 0.98 produces a median estimate around 0.90. Cochrane therefore uses 0.98 for the out-of-sample forecast. The adjustment is an explicit modeling choice based on a simulation exercise, not a universally unbiased correction or an independently identified parameter.

At the end-1996 valuation, the linear forecast starts around −8% excess return for 1997. The forecast of the annual excess return remains about −5% ten years later, −1.75% after twenty-five years, and 2.35% after fifty years as it converges slowly toward an 8% long-run mean. These striking numbers illustrate the sensitivity of extrapolation to persistent state dynamics. They are not the article's claim of a reliable decades-long negative-return forecast.

The source gives several reasons for caution. The terminal price ratio is at the edge of or beyond the historical range; a nonlinear expected-return function flattening near zero can fit historical observations while generating much less extreme forecasts. The persistence estimate is highly uncertain. A true coefficient of 0.98 generates a very wide distribution of estimates, including a reported 95% range of roughly 0.66–1.00. Even a correct conditional mean is accompanied by large annual return noise. The article's measured conclusion is that expected returns are likely unusually low, not that a negative realization or immediate crash is guaranteed.

A faithful reconstruction should retain the full-sample fit and terminal forecast as the historical experiment. An expanding-window forecast evaluation, alternative predictor transformations, nonlinear constraints, and transaction-cost backtest would be useful extensions, but none is supplied here and their results must not be attributed to this paper.

## Present-value accounting disciplines the interpretation

The appendix starts with the exact gross-return identity $R_{t+1}=(P_{t+1}+D_{t+1})/P_t$. Iterating expresses price relative to dividends as discounted future dividend growth plus a terminal-price term. A log-linearized form, with constants suppressed, links the log price/dividend ratio to future dividend growth minus future returns:

$$
p_t-d_t\approx \text{constant}+
E_t\sum_{j\geq1}\varrho^{j-1}(\Delta d_{t+j}-r_{t+j}),
$$

provided the terminal term vanishes. Here $ϱ$ is the log-linearization weight, distinct from predictor persistence; the powers explicitly give the next dividend and return unit weight. Lower discount rates raise prices just as higher expected dividends do. Valuation variation therefore has to forecast dividend growth, discount rates, or a surviving terminal component. It cannot be dismissed as economically meaningless merely because short-horizon returns are noisy.

Multiplying this identity by the demeaned current valuation ratio and taking expectations yields a covariance decomposition of valuation variance. Table 5, using a fifteen-term truncation from earlier work, assigns real-dividend-growth covariation a contribution of −34% with standard error 10%, and real-return covariation 138% with standard error 32%. In nominal terms the corresponding entries are 30% with standard error 41% and 85% with standard error 19%. These are signed covariance contributions, can exceed 100% or be negative, and need not sum exactly to 100% under truncation and approximation. They are not nonnegative causal shares.

This accounting is consistent with discount-rate variation dominating much valuation movement, but it does not identify whether that variation reflects rational risk compensation or changing beliefs. Nor does it make the no-bubble terminal condition an empirical certainty. The article discusses the bubble possibility and relies on the broader literature rather than supplying a complete bubble test.

## Consumption pricing and the quantitative hurdle

For an investor maximizing expected discounted utility, the basic discrete-time pricing condition is

$$
1=E_t[M_{t+1}R_{t+1}],\qquad
M_{t+1}=e^{-\delta}\frac{u'(C_{t+1})}{u'(C_t)}.
$$

With power marginal utility $u'(C)=C^{-\gamma}$, consumption growth determines the discount factor. In a diffusion or local approximation, the excess expected return is proportional to consumption covariance:

$$
\frac{E_t[r]-r^f_t}{\sigma_t(r)}
=\gamma\,\sigma_t(dC/C)\operatorname{corr}_t(dC/C,r).
$$

A 0.5 Sharpe ratio is hard to reconcile with aggregate consumption-growth volatility near 1%, a generously measured stock–consumption correlation of 0.2, and risk aversion at most 10: their product is only 0.02. At 20% return volatility this implies a premium of 0.4%, not 8%. Even perfect correlation produces a Sharpe ratio of only 0.1 at $γ=10$.

The conditional problem is equally important. Low valuations predict much higher returns without proportionately higher return volatility. Therefore the conditional Sharpe ratio rises when valuations fall. A fixed-curvature consumption model needs substantial changes in consumption risk or its correlation with returns; the source argues the data do not supply changes of the required size.

Simply increasing curvature creates other tensions. With correlation 0.2, matching 0.5 requires curvature around 250; even correlation one requires about 50. Such parameters make consumers extremely unwilling to shift consumption across dates and imply implausible interest-rate behavior unless additional mechanisms offset those effects. The CAPM cannot resolve this aggregate premium puzzle because it takes the market premium as an input when pricing individual securities.

There are mathematical qualifications to the survey's simplified formulas. For a diffusion $dC/C=\mu_Cdt+\sigma_CdW$, exact power-utility pricing gives

$$
r^f=\delta+\gamma\mu_C-\tfrac12\gamma(\gamma+1)\sigma_C^2.
$$

In log-growth notation, this is $r^f=\delta+\gamma E[d\log C]/dt-\gamma^2\sigma_C^2/2$. The printed appendix's proportional-growth derivation suppresses the Itô precautionary term; footnote 7 restores a log-growth version. Thus its elementary interest-rate equation should not be implemented as exact at very high curvature. Likewise, the small symmetric-bet risk premium is approximately $\gamma y^2/(2C)$, not $\gamma y^2/C$ as one displayed approximation suggests; Table 6's numerical entries are consistent with the one-half factor. These qualifications preserve the economic argument while avoiding propagation of printed algebraic simplifications.

## Why simple risk-aversion calibrations can mislead

Table 6 compares certainty equivalents for a household consuming a constant amount $C=\$50{,}000$ per year. The hypothetical gamble permanently adds or subtracts $y$ from annual consumption with equal probability. Under power utility, the annual payment $x$ that makes avoiding the gamble equivalent is determined by

$$
u(C-x)=\tfrac12u(C+y)+\tfrac12u(C-y),
$$

or, for $\gamma\ne1$,

$$
x=C-\left[\tfrac12(C+y)^{1-\gamma}+\tfrac12(C-y)^{1-\gamma}\right]^{1/(1-\gamma)}.
$$

Discounting drops out because the same level comparison occurs every period. For a $\$10{,}000$ gamble, the reported willingness to pay is $\$2{,}000$ at curvature 2, $\$6{,}921$ at 10, and $\$9{,}889$ at 250. For a $\$10$ gamble, even curvature 250 implies only about 25 cents. These are illustrative calculations under one functional form, not survey estimates. They show why intuitions derived from small laboratory stakes need not tightly pin down behavior toward large permanent consumption risks. The limiting small-stake approximation must include the one-half factor stated above.

A second familiar calculation infers wealth risk aversion near 3 by dividing a 0.5 Sharpe ratio by 0.17 wealth volatility. That inference presumes that the marginal value of wealth depends only on wealth and that changes in wealth map directly into consumption. It quietly embeds a model in which consumption is much more volatile than the approximately 1% aggregate growth volatility actually observed. If investment opportunities, labor income, or habit are additional states, the value function is $V(W,z)$ and the covariance of returns with changes in $z$ also enters pricing through $V_{Wz}$. Ignoring it does not provide a clean independent estimate of risk aversion.

Cochrane consequently treats the consumption–interest-rate evidence as a stronger objection to extreme power curvature than casual gambling thought experiments. Raising curvature in a general model may be defensible; raising the single power-utility parameter changes both risk attitudes and willingness to shift consumption over time. The purpose of the next mechanisms is to separate those restrictions while preserving a coherent joint account of quantities and prices.

## Habit: a state variable that separates the problems

The Campbell–Cochrane mechanism uses external habit $X_t$ and utility proportional to $(C_t-X_t)^{1-\eta}/(1-\eta)$. The normalization ensures increasing utility when $η>1$. Define surplus consumption $S_t=(C_t-X_t)/C_t$. Local curvature with respect to consumption is $η/S_t$, so moderate power $η=2$ can coexist with high, time-varying aversion to consumption risk when surplus consumption is small.

Footnote 10 gives the state transition in logs:

$$
s_{t+1}-s_t=-(1-\phi)(s_t-\bar s)
+\left[\frac{\sqrt{1-2(s_t-\bar s)}}{\bar S}-1\right]
(\Delta c_{t+1}-g),\qquad s_t=\log S_t.
$$

Habit adjusts slowly to aggregate consumption, and a bad consumption shock brings consumption closer to habit, increasing effective risk aversion. Externality means an individual takes habit as given; personal consumption decisions do not internalize their contribution to the aggregate habit process.

The essential mechanism is a balance between intertemporal substitution and precautionary saving. In bad times, low consumption encourages borrowing against recovery, while increased risk aversion encourages saving against further deterioration. A carefully chosen sensitivity function balances those forces, allowing stable interest rates alongside a variable equity premium. The survey reports a steady surplus ratio around 0.05 and emphasizes that high risk aversion remains: the model is not a low-risk-aversion explanation of the premium.

The artificial economy produces a roughly 0.5 Sharpe ratio, valuation-based return predictability, and relatively low consumption–return correlation while preserving near-unpredictable consumption growth. Its consumption history does not explain the exceptionally high late-1990s valuations: measured consumption had grown too slowly relative to habit. Reproducing the full simulation requires parameters, state-domain treatment, pricing solution, and discretization from the underlying paper; these are not fully specified in the survey. In particular the square root requires a defined admissible state region or boundary rule, which should not be improvised silently.

## Incomplete markets: why dispersion rather than extra variance matters

Adding independent idiosyncratic noise to individual consumption does not automatically increase its covariance with a common market return. If $\Delta c_i=\Delta c_a+\epsilon_i$ and the idiosyncratic shock has zero conditional mean given aggregate returns, then $\operatorname{cov}(\Delta c_i,r)=\operatorname{cov}(\Delta c_a,r)$. Individual volatility rises while correlation falls, leaving the covariance unchanged in the local linear pricing calculation.

Constantinides–Duffie instead make the cross-sectional variance of permanent individual consumption shocks depend on aggregate conditions. In the general construction reviewed on pp. 24–26, write $C_{it}=\delta_{it}C_t$ and

$$
\delta_{it}=\delta_{i,t-1}
\exp(\eta_{it}y_t-y_t^2/2),\qquad \eta_{it}\sim N(0,1),
$$

conditionally independent across people. The normalization preserves mean individual shares. For a positive pricing kernel $m_t$, choose

$$
y_t^2=\frac{2}{\gamma(\gamma+1)}
\left[\log m_t+\delta+\gamma\log(C_t/C_{t-1})\right].
$$

Integrating individual power marginal utility across idiosyncratic shocks yields $m_t$ because the normal exponential moment contributes $\exp[\gamma(\gamma+1)y_t^2/2]$. Each household's Euler equation can therefore support the specified aggregate prices. The consumption ratio from $t-1$ to $t$ must be paired with return $R_t$; the printed display's $R_{t+1}$ is inconsistent with that timing and should not be carried into code.

Existence requires $y_t^2\geq0$, equivalently $\log m_t\geq-\delta-\gamma\log(C_t/C_{t-1})$, in every state. Mere positivity of $m_t$ is weaker. The simple illustration $m_t=1/R_t$ prices one return but need not satisfy the variance constraint or price a larger asset set. Permanent shocks prevent households from cheaply smoothing the risk away through borrowing against certain recovery. This is an existence mechanism, not evidence that empirically observed household risk has the required magnitude and cyclicality.

Cochrane stresses the empirical burden: low risk aversion requires very large dispersion and strong increases in that dispersion when the market falls. Figure 6 contrasts risk aversion from 1 through 25. With curvature around 2, a shift from a 5% gain to a 5% loss requires approximately a rise from 10% to 25% in the illustrated cross-sectional consumption-growth standard deviation. High risk aversion makes less extreme risks sufficient. The source's comparison of cohort dispersion levels with annual growth uncertainty is suggestive rather than a formally matched variance-growth estimator; one must compare increments of log-consumption variance, not simply increments of standard deviation, in an actual test.

## Production, equilibrium, and practical limits

The production discussion explains why price movements require adjustment frictions. With $Y=\theta K^\alpha L^{1-\alpha}$ and freely convertible investment, the marginal investment return is $1-\delta+\alpha Y_{t+1}/K_{t+1}$. Installed and uninstalled capital are perfect substitutes, making their relative price fixed. Plausible output fluctuations then generate far too little stock-return volatility.

Convex adjustment costs make installed capital valuable when investment is high. The article illustrates a quadratic cost $aI^2/(2K)$ and an investment-return approximation containing $a\Delta(I/K)$. Investment variation can now generate capital gains and losses. Figure 7 shows that the cyclical movements of investment/output and stock valuations align reasonably, whereas long-run valuation movements align less well. A rough illustration with $a=2$, $I/Y=0.15$, and $I/K=0.05$ implies adjustment costs of 0.75% of output. Some empirical estimates require much larger costs. The printed production formulas mix cost and accumulation conventions, so an implementation should derive the investment Euler equation from one explicit resource constraint rather than splice the displays together.

Technology alone does not generally determine the equity premium: it facilitates substitution across dates but may not span arbitrary state-contingent payoffs. Full equilibrium requires preferences, production, and market clearing. A model that matches equity returns while generating wildly volatile interest rates or predictable consumption has not solved the joint problem.

The most useful takeaway for a researcher is the joint diagnostic. Match historical means with appropriate uncertainty; distinguish persistent conditional expectations from realizations; require pricing kernels to satisfy economically plausible consumption and interest-rate implications; and assess household or technological mechanisms with their own data. A high expected premium need not warrant a larger equity allocation for someone whose background risk is highest in the same bad states. Conversely, an investor relatively insulated from those risks may rationally differ from the representative holder. The article provides that organizing logic, not a universally optimal allocation or a tested trading rule.

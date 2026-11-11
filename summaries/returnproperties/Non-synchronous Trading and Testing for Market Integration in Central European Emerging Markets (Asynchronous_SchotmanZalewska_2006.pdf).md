# Non-synchronous Trading and Testing for Market Integration in Central European Emerging Markets

**Peter C. Schotman and Anna Zalewska.** Working-paper version dated **15 March 2006**. Source: [original PDF](../../Finance/Asynchronous_SchotmanZalewska_2006.pdf). The full 48-page source, including six tables and all 21 figures, was inspected. The document has no separate technical appendix providing the complete likelihood implementation. Results below refer to this supplied version rather than an assumed later publication.

## Why this matters and the authors' contribution

The same calendar date does not imply the same information interval. In the 1990s a Central European exchange could finish fixing prices before the US stock market had even opened. Regressing its daily return on that day's US closing return consequently introduces information that was unavailable when the dependent price was set. A weak regression can then look like economic segmentation when it partly reflects incompatible clocks.

Schotman and Zalewska reconstruct developed-market return series using intraday index values selected to precede and approximate the closing time of each emerging market. The matching rules change when local trading systems and closing times change. They combine those series with time-varying regressions to trace return comovement and autocorrelation in Hungary, the Czech Republic, and Poland from April 1994 to February 2004.

Their principal findings are that clock alignment substantially improves explanatory power, weekly sampling does not fully remove the mismatch, and emerging-market comovement is highly variable rather than a smooth one-way progression toward integration. The Asian and Russian crises produce distinct episodes, especially for Hungary. Own-return autocorrelation declines over the sample and eventually becomes statistically indistinguishable from zero in all three markets.

The paper deliberately uses “integration” in the broad sense of return comovement. It does **not** test the full asset-pricing definition that equally risky assets have equal expected returns across countries. Its regressions are useful for measuring exposure and information overlap, but neither a high beta nor a low own-return coefficient proves unrestricted capital mobility or complete market efficiency.

## Markets, source data, and sample boundaries

The emerging-market indices are Budapest's BUX, Prague's PX50, and Warsaw's WIG. Developed comparators are Germany's DAX30, the UK's FTSE100, and the US S&P 500. DataStream supplies the time series. The common period is **7 April 1994–27 February 2004**, starting with the introduction of PX50 even though Budapest and Warsaw had operated earlier.

Table 2 lists 2,455 BUX observations, 2,403 PX50 observations, and 2,433 WIG observations. Developed-market totals are 2,491 DAX30, 2,499 FTSE100, and 2,492 S&P 500 observations. These are raw series counts, not a guarantee that every likelihood uses exactly that many matched observations after lags and exclusions.

The paper works with local-currency index returns. The section describing the data does not give a fully explicit formula distinguishing simple from log returns, nor a complete statement of price-index versus total-return adjustments for each series. These conventions must be recovered from the original data identifiers or author code for exact replication; they should not be guessed from the generic phrase “daily return.” Historical index composition also changes with listings, delistings, and index revisions.

Local market structure is important to interpreting the sample. Early Warsaw and Prague observations come from call systems in which prices were fixed once daily. Budapest initially had short sessions and very few trades. Prague's mass privatization created a large nominal listing universe, followed by extensive delistings during domestic financial distress. These institutions can generate autocorrelation through stale constituent prices and price-setting rules, without implying an easily exploitable forecasting strategy.

The authors discuss foreign ownership and domestic pension flows as possible explanations for differences between countries. Those institutional statistics motivate interpretations; they do not enter a causal identification strategy. Some descriptive statistics in the text and Table 1 differ, so the note does not use them as exact calibration targets for the return models.

## Calendar matching comes before clock matching

The observation calendar is tailored to the dependent emerging market. Developed-market returns with no corresponding emerging-market observation are removed. When the emerging exchange trades but the comparator is closed, the developed-market return is set to zero, interpreted as no new information from that market on that day. This is the published rule, not a claim that all economically relevant global information is absent on a national exchange holiday.

The calendars changed early in the sample. Warsaw traded Mondays, Tuesdays, and Thursdays through June 1994, added Wednesday sessions for July–September, and moved to five sessions a week on October 1. Prague moved from three sessions a week to five on September 19, 1994. Ignoring those changes would create fictitious daily observations or mismatched lagged returns.

A reproduction must also determine how returns spanning an emerging-market closure accumulate comparator information. The article says that unmatched developed returns are removed, but does not fully document whether every return is recomputed between retained price endpoints or whether precomputed daily returns are simply filtered. These constructions can differ around holidays. The same ambiguity affects the meaning of a “previous day” when the preceding calendar day was not a trading day. The supplied paper does not provide a complete calendar algorithm or a list of exceptional closures.

## Exact time-matching schedule

All clock times in the source are stated in GMT. DAX30 and FTSE100 are available at opening and at 10:00, 12:00, 14:00, 16:00, and closing. S&P 500 is available at opening, 16:00, and closing. The authors assume developed-market opening observations are sufficiently close to session opening because those markets are liquid. They report approximate openings of 08:00 for the European comparators and 14:30 for the US, and closes of 16:30 and 21:00 respectively.

These are the paper's conventions. Exact historical daylight-saving transitions and any vendor timestamp adjustments are not documented. A reproduction must preserve the underlying observation timestamps and verify the no-future-information condition instead of applying a modern opening-hours calendar blindly.

Table 3 supplies the operational matching rules:

| Dependent index | Period | DAX30 and FTSE100 selected level | S&P 500 selected level |
|---|---|---|---|
| BUX | 7 Apr 1994–16 May 1999 | Same-day 12:00 | Previous-day close |
| BUX | 17 May 1999–29 Jul 2001 | Same-day 16:00 | Same-day 16:00 |
| BUX | 30 Jul 2001–27 Feb 2004 | Same-day 14:00 | Same-day opening |
| PX50 | 7 Apr 1994–14 Mar 1996 | Same-day 10:00 | Previous-day close |
| PX50 | 15 Mar 1996–15 Mar 1998 | Same-day 12:00 | Previous-day close |
| PX50 | 16 Mar 1998–27 Feb 2004 | Same-day 14:00 | Same-day opening |
| WIG | 7 Apr 1994–15 Nov 2000 | Same-day 10:00 | Previous-day close |
| WIG | 16 Nov 2000–27 Feb 2004 | Same-day 14:00 | Same-day opening |

The authors construct matched **level series**, then returns from those levels. This is more specific than shifting an existing daily-close return by a fixed number of rows. At regime changes, the endpoints themselves change, so a transition return can span a different clock interval. The exact treatment of those boundary observations is not separately specified.

The schedule approximates synchrony rather than achieving it perfectly. For example, after July 2001 BUX closes at 15:30, while the selected European comparator is 14:00 and the US comparator is its opening value. Residual gaps remain. Earlier BUX closing times progress from noon to 12:15, 12:45, and 13:45 before the May 1999 extension to 16:00. These intermediate changes are grouped under the same noon comparator because finer observations are unavailable.

Prague's call-system prices were fixed and announced before the subsequent trading session. Continuous trading introduced in March 1996 initially covered only seven important issues. The authors assume the later index value adequately reflects the information incorporated by these liquid constituents. Warsaw's closing WIG value continued to reflect the fixed-price session even after some continuous trading began; the matching regime changes only with WARSET on November 16, 2000.

For each pair, two alternatives are retained as controls: same-calendar-day close-to-close developed returns and previous-day developed close-to-close returns. The matched series is expected to perform better than both because it uses a closer information interval without systematically incorporating future market moves.

## Regression system and interpretation of coefficients

The principal specification, Model 2, is

$$
r_{E,t}=\alpha_t+\beta_t r_{D,t}+\gamma_t r_{E,t-1}+e_t,
\qquad \operatorname{Var}(e_t)=\sigma_t^2.
$$

The dependent return is from the emerging market and the developed return is defined using one of the three alignment conventions. The impact coefficient $\beta_t$ measures contemporaneous comovement under that convention. The own-return coefficient $\gamma_t$ measures the residual first-order predictive relation. The intercept is included but is not interpreted as an asset-pricing alpha.

Model 1 removes the own-return lag. Model 3 adds current and lagged exchange-rate changes:

$$
r_{E,t}=\alpha_t+\beta_t r_{D,t}+\gamma_t r_{E,t-1}
+\delta_{0,t}s_t+\delta_{1,t}s_{t-1}+e_t.
$$

Here $s_t$ is the daily exchange-rate change relevant to the country pair. Rates are provided before midday by the emerging countries' national banks. The authors lack enough intraday currency data to align them exactly, so current and lagged changes are a second-best correction. The precise quote orientation and return formula for each currency series are not enumerated in the paper.

Separating currency changes avoids automatically introducing a common US-dollar component into both equity returns. For example, positively correlated European currencies against the dollar can induce correlation between dollar-denominated equity series even when local equity moves are unrelated. This motivates the design; it does not establish that currency risk is absent when its estimated coefficient is insignificant.

The complete design has three emerging markets, three developed comparators, three time alignments, and three regression specifications: **81 models**. These are pairwise comparisons, not a joint regression on all three developed indices. One should therefore not sum the three fitted developed-market variance shares or interpret their betas as mutually exclusive country exposures.

## Time-varying states and the limits of the estimation specification

Let $\theta_t$ collect the relevant coefficients. The state equation is

$$
\theta_t=\theta_{t-1}+\eta_t,
\qquad E[\eta_t]=0,
\qquad \operatorname{Var}(\eta_t)=\Omega,
$$

with diagonal $\Omega$. Setting $\Omega=0$ nests constant coefficients. The authors view the random walk primarily as a smoothing device: the estimated state-innovation variance determines how much neighboring data contribute to a local coefficient estimate. It is not a structural prediction that economic beta follows an unrestricted random walk forever.

Conditional variances of the emerging residual and developed-market return are modeled with asymmetric GARCH(1,1) processes, following Rockinger and Urga. The paper says alternative residual-variance specifications have little effect on coefficient paths. However, it does **not** print the exact asymmetric variance recursions, the estimated variance parameters, starting values, optimization algorithm, state initialization, or the complete filtering/smoothing equations. The keyword “Kalman filter” and the state-space equations identify the method family, but do not make the entire empirical implementation exactly reproducible from this document alone.

For clarity, a standard conditional Gaussian reconstruction of the stated regression would use design row $x_t^{\mathsf T}$, predicted state mean $m_{t|t-1}=m_{t-1|t-1}$, and predicted state covariance $P_{t|t-1}=P_{t-1|t-1}+\Omega$. Given a chosen residual variance sequence $\sigma_t^2$, it would calculate

$$
v_t=r_{E,t}-x_t^{\mathsf T}m_{t|t-1},
\qquad F_t=x_t^{\mathsf T}P_{t|t-1}x_t+\sigma_t^2,
$$

$$
K_t=P_{t|t-1}x_t/F_t,
\qquad m_{t|t}=m_{t|t-1}+K_tv_t,
$$

$$
P_{t|t}=P_{t|t-1}-K_tx_t^{\mathsf T}P_{t|t-1}.
$$

Its Gaussian innovation log likelihood is $-\tfrac12\sum_t[\log(2\pi)+\log F_t+v_t^2/F_t]$. These equations are an explicit reconstruction of the linear-Gaussian state-space machinery, **not a recovered statement of the authors' exact software**. In particular, when GARCH volatility depends on latent residuals, the choice between filtered errors, prediction innovations, and other approximations affects the recursion and must be documented. The publication does not settle that choice.

The discussion of observations “around” each date suggests a retrospective smoothing interpretation. A reproducing researcher must distinguish filtered estimates using information through $t$ from smoothed estimates using later data. The supplied version does not label every plotted path sufficiently to remove that ambiguity. The figures should not be treated as signals available to an investor at the plotted date without resolving it.

The source reports overwhelming likelihood-ratio rejection of constant parameters for all specifications, but omits the individual test statistics and reference-law details. Testing zero state variances places parameters on a boundary, so a routine interior-parameter chi-square approximation is not automatically justified. The note preserves the reported rejection as the authors' result rather than inventing a calibrated significance level.

## Conditional variance share: definition and a printed indexing error

Let $\omega_t^2$ be the developed-return variance and $\psi_t^2$ the emerging-return variance conditional on the coefficient path. Assuming developed returns are uncorrelated with lagged emerging returns and with $e_t$, Model 2 implies

$$
\psi_t^2=\beta_t^2\omega_t^2+\gamma_t^2\psi_{t-1}^2+\sigma_t^2.
$$

This is the paper's Eq. (2). It attributes emerging variance to current developed shocks, persistent earlier emerging variation, and local residual shocks. The exogeneity assumption is substantive: if the developed series responds to earlier emerging news or has relevant serial correlation, omitted cross terms enter the variance calculation.

An efficient way to implement the intended decomposition is to define $D_t$, the portion propagated from developed-market shocks, and $U_t$, the portion propagated from local shocks:

$$
D_t=\beta_t^2\omega_t^2+\gamma_t^2D_{t-1},
\qquad U_t=\sigma_t^2+\gamma_t^2U_{t-1}.
$$

With the stated zero initial variance, set $D_0=U_0=0$, obtain $\psi_t^2=D_t+U_t$, and calculate

$$
VR_t=\frac{D_t}{D_t+U_t}.
$$

These recursions are an algebraic implementation of Eq. (4). They avoid repeatedly summing the entire history and give a useful check: nonnegative component variances imply a ratio between zero and one, provided the denominator is positive.

The printed Eq. (3) has an indexing problem. It writes the current term $A_t^2$ separately and also starts its historical sum at $j=0$, which counts the current term again under the usual empty-product convention. The consistent expansion of Eq. (2) starts the historical sum at $j=1$:

$$
\psi_t^2=A_t^2+\sum_{j=1}^{t-1}
\left(\prod_{i=0}^{j-1}\gamma_{t-i}^2\right)A_{t-j}^2,
\qquad A_t^2=\beta_t^2\omega_t^2+\sigma_t^2.
$$

Equation (4) uses the corresponding developed component. This correction is derived from the displayed recursion and is stated explicitly rather than silently changing the source.

The first term in Eq. (4), $\beta_t^2\omega_t^2/\psi_t^2$, is the squared contemporaneous return correlation under the orthogonality assumptions. The source calls it a squared innovation correlation, but the emerging one-step innovation variance would instead exclude predictable lagged-return variance. Those quantities coincide when $\gamma_t=0$; otherwise the denominator distinction matters. The full ratio also includes developed shocks transmitted indirectly through past emerging returns.

This calculation conditions on coefficient paths and ignores their estimation uncertainty. It is not the full predictive variance after integrating over uncertain states, which would include terms such as $x_t^{\mathsf T}P_{t|t-1}x_t$. For Model 3 a complete variance attribution would additionally require currency variances and covariances. The paper presents the principal paths for Model 2 and does not give a separate general currency-inclusive decomposition.

## Model comparison and exact numerical results

The authors report a descriptive $R^2$ using residual and return sums of squares, while cautioning that ordinary regression interpretations are imperfect for time-varying maximum-likelihood models. Their formal comparison criterion is

$$
SC=2\log L-k\log T,
$$

where $k$ is the count of free parameters and $T$ the observations. **Higher is better**; this is the negative of the common minimization form of BIC. The paper does not print a parameter-count ledger for every state/GARCH specification, which limits exact reconstruction of the scores.

The most comparable numerical summary is Table 4's Model 2 $R^2$, in percent:

| Emerging index | Developed comparator | Previous day | Same day | Time adjusted |
|---|---|---:|---:|---:|
| BUX | DAX30 | 3.9 | 26.2 | 36.6 |
| BUX | FTSE100 | 3.6 | 19.1 | 34.5 |
| BUX | S&P 500 | 17.1 | 4.1 | 22.4 |
| PX50 | DAX30 | 8.6 | 23.8 | 31.3 |
| PX50 | FTSE100 | 8.6 | 24.1 | 28.3 |
| PX50 | S&P 500 | 11.0 | 10.8 | 14.2 |
| WIG | DAX30 | 6.2 | 11.9 | 21.9 |
| WIG | FTSE100 | 6.8 | 13.1 | 19.8 |
| WIG | S&P 500 | 16.8 | 5.1 | 18.2 |

Time adjustment wins each comparison. For BUX–DAX it improves same-day fit by 10.4 percentage points; for WIG–DAX by 10.0 points. For BUX–S&P 500 the same-day specification is particularly poor because much of the US return follows the Hungarian close. A previous-day return helps but still misses information that a changing intraday schedule can capture.

Daily Schwarz scores also favor time-adjusted returns in all 27 comparisons of the three timing choices within a fixed country pair and model. For BUX–DAX Model 2, the scores are 25,598 previous-day, 26,898 same-day, and 27,642 time-adjusted. The numerical gaps are large relative to the modest differences among some regression specifications. Comparison across unrelated dependent series or different return scalings should not be made merely by ranking raw likelihood levels.

Adding exchange rates changes the other coefficient paths little, and neither current nor lagged currency coefficients are reported individually significant at 5%. Nevertheless, the currency terms can improve likelihood fit through their time-varying state contribution. For example, time-adjusted BUX–DAX Model 3 has SC 27,696 versus 27,642 for Model 2. Conversely, the preferred DAX specification for PX50 is Model 1, and for WIG Model 2. There is no single regression specification that dominates all country pairs.

## Dynamic results by country

**Hungary.** The own-return coefficient starts around 0.4 and trends down; the authors date its loss of 5% significance to around early 1999. Figures 3–8 show sharply higher impact coefficients during the Asian crisis in 1997 and Russian crisis in 1998. The matched DAX peaks are roughly 1.2–1.3 from the graph; these are visual approximations, not tabulated parameter estimates. The comparable FTSE peak can be higher. Impact coefficients return toward precrisis levels over a few months, rise again around 1999–2001, and decline thereafter.

The source describes post-1999 impact coefficients of roughly 0.6–0.8 for nearly two years and middle-sample variance shares reaching 60–80%. Those shares fluctuate substantially with conditional volatility. They are not permanent estimates of the fraction of Hungary economically integrated with another country. The average reported standard error of recent impact estimates is about 0.17, and some late DAX values are not statistically distinguishable from zero.

**Czech Republic.** PX50 starts with stronger own-return persistence, around 0.6 in Figure 12, and becomes statistically insignificant around mid-1999 according to the text. A prominent comovement increase appears during the 1998 Russian crisis, but the 1997 Asian episode is much less visible than in Hungary. The authors associate this with severe domestic restructuring and financial distress around 1996–1997, while acknowledging that the paper does not identify the causal contribution of those events.

Early and middle-sample impact coefficients are generally higher against DAX and FTSE than against S&P 500. The US impact coefficient does not exceed about 0.25 during its 1998 rise, according to the text. After 2001 it becomes comparable with the European coefficients. Figure 13 shows a later European-impact plateau around 0.6–0.7 before declining; precise daily values cannot be recovered from the graph alone.

**Poland.** WIG begins with the lowest of the three own-return coefficients, around 0.3, but the authors date its loss of significance later, around 2000. That timing is consistent with the change from a fixed-price-session index to continuous-trading information in November 2000. It is not an isolated test proving that the trading-system change caused the decline.

Time-adjusted impacts against all three developed markets have broadly similar paths, with DAX generally lowest. The source reports significance from approximately 1996 for FTSE and S&P and 1997 for DAX, though graphical confidence intervals should be read as pointwise and approximate. Poland shows a rise around 2000 followed by an earlier decline than the other two countries. Domestic pension-fund inflows and reduced free float are proposed explanations, not estimated causal regressors.

The broad implication is that comovement changes with crisis periods, investor participation, local institutions, and observation alignment. A low average over a long sample can conceal temporary strong exposures. Conversely, a crisis peak should not be extrapolated as a permanent integration parameter.

## Weekly comparison and source inconsistencies

Weekly data are constructed Tuesday to Tuesday, chosen because Tuesday was a trading day even under the early three-day emerging-market calendars. Time-matched weekly returns use the same selected intraday levels as the daily matching schedule. The authors refit the models at weekly frequency; simply aggregating an estimated daily beta path would not reproduce that experiment.

Time adjustment has the highest Schwarz score in **22 of 27** within-model weekly timing comparisons. It therefore remains important even when the return interval is longer. For BUX–DAX Model 2, weekly SC is 1,954.48 for previous-day, 1,988.25 for same-day, and 2,025.69 for matched returns. Exceptions exist: WIG–DAX Model 3 prefers same-day returns, and several PX50–S&P specifications do as well.

Figure 20 shows smoother weekly impact paths. Figure 21 shows weekly standard errors usually around 0.25 and often appreciably above the daily errors, which commonly lie around 0.10–0.20. The paper argues that daily aligned observations better distinguish nearby crisis episodes. This is evidence about precision and temporal resolution in the fitted model, not a claim that increasing frequency always helps under arbitrary microstructure noise.

Several display problems deserve explicit caution. Figure 3's legend appears inconsistent with the text's ordering of same-day and previous-day DAX effects; the analogous FTSE figure and the numerical fit table support the text's interpretation, but the raw paths are unavailable to verify the labels. Tables 5–6 also contain repeated numerical rows across some different country/comparator combinations, which may be transcription artifacts. They should be reproduced as printed or checked against original estimation output, not silently “corrected.”

The article also suggests that the joint $R^2$ from previous-day and same-day regressors is generally below the sum of their separate $R^2$ values. That is not a universal regression identity: correlated regressors can generate suppression effects. The paper's central time-alignment finding is supported by its direct tables; the informal sum-of-fits comparison is not a substitute for estimating an explicitly combined-regressor benchmark.

## Reimplementation boundary and practical takeaway

A faithful reconstruction begins with a table of actual index timestamps and historical calendars, then creates three comparator-return variants per emerging market. It should preserve the exact matching schedule, identify every regime-boundary return, and document holiday and daylight-saving choices. It should fit all three regression specifications consistently and keep daily and weekly likelihoods separate.

The central statistical model is recoverable: random-walk coefficient states, pairwise emerging-on-developed regressions, own-return persistence, optional current/lagged currency changes, and conditional variance attribution. Exact numerical reproduction remains limited by missing return conventions, complete GARCH equations and estimates, state initialization, filtering versus smoothing details, optimizer settings, parameter counts, and the raw intraday data identifiers. No code or technical supplement in the supplied PDF fills those gaps.

No portfolio, rebalancing rule, cost model, or out-of-sample trading result is reported. The empirical aim is measurement of comovement and predictability. The note's implementation equations are therefore a transparent route to reconstructing the model family, not a claim that the historical figures have been independently replicated.

For subsequent research, the strongest lesson is to align information intervals before assigning economic meaning to low correlations, geographical differences, or disappearing autocorrelation. The paper shows that a data-construction decision can matter more than adding regression controls, and that lowering frequency can leave the mismatch while reducing the ability to detect short-lived changes.

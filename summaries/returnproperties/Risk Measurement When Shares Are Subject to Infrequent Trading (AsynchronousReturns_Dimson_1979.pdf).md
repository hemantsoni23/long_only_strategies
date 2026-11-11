# Risk Measurement When Shares Are Subject to Infrequent Trading

**Elroy Dimson (1979).** *Journal of Financial Economics* 7, 197–226. Source: [original PDF](../../Finance/AsynchronousReturns_Dimson_1979.pdf). This note covers the full article, model derivation, simulation, ten tables, and discussion of estimator evaluation. Equations with missing text-layer symbols and the principal numerical tables were checked against page images.

## Why this matters

A stock that trades infrequently can look less exposed to the market simply because its recorded price has not yet incorporated the market's latest movement. The same stale-price mechanism can make frequently traded stocks look unusually risky relative to an index whose constituents update slowly. A conventional regression beta therefore combines economic exposure with relative trading frequency.

Dimson proposes estimating beta by summing coefficients from a multiple regression on lagged, contemporaneous, and leading market returns. The method requires ordinary recorded return series rather than a complete history of transaction timestamps, and it allows the market index itself to contain stale prices. In the historical UK application, a severe cross-sectional gradient in conventional beta largely disappears: the least frequently traded decile's beta rises from 0.47 to 0.91, while the most frequently traded decile falls from 1.16 to 0.93.

The paper's second important contribution is an evaluation warning. A biased beta can appear stable and can predict future **recorded** returns better than a less biased economic beta if stale-price contamination persists in the evaluation period. Testing an estimator against the same distorted measurement system can reward the distortion. This matters for risk-model validation, small-stock anomalies, performance attribution, and any attempt to use beta stability as evidence of economic stability.

## Economic returns versus recorded returns

The latent market model is

$$
R_t=\alpha+\beta M_t+\varepsilon_t,
\qquad E[\varepsilon_t]=0,\qquad \operatorname{Cov}(\varepsilon_t,M_t)=0.
$$

Here $R_t$ is the stock's true chronological-period return and $M_t$ is the true market return. The source assumes true returns are serially and cross-serially uncorrelated, with stationary beta and a time-invariant intercept. In this model,

$$
\beta=\frac{\operatorname{Cov}(R_t,M_t)}{\operatorname{Var}(M_t)}.
$$

This is a market-model exposure, not a proof of the CAPM or an expected-return prediction. The model separates chronological time from transaction time: true values can change during intervals when no trade occurs.

Let $\theta_i$ be the probability that a stock's last recorded trade at time $t$ occurred in period $t-i$. Let $\phi_i$ be the corresponding fraction of the market portfolio last traded that many periods earlier. The paper assumes stationary, declining age weights, supported over a finite range, with

$$
\sum_{i=0}^{n}\theta_i=\sum_{i=0}^{n}\phi_i=1.
$$

The observed price is a stale realization of a true price, not generally the current latent price plus independent white noise. Averaging over the nontrading process produces a weighted average of past true prices, and an analogous relation for log returns. The ex-post representation used in the derivation is

$$
\widetilde R_t=\sum_{i=0}^{n}\theta_iR_{t-i}+u_{R,t},
\qquad
\widetilde M_t=\sum_{i=0}^{n}\phi_iM_{t-i}+u_{M,t}.
$$

Tildes distinguish measured returns from economic returns. The residual terms represent the difference between actual stale observations and their filtering representation. The source specifies zero-mean orthogonality conditions in discussing this approximation. Those conditions and the serial-independence assumptions matter to its consistency argument; arbitrary endogenous nontrading and arbitrary measurement errors are not covered merely by adding more regressors.

For a simple independent per-period trade probability $\theta_0$, the age weights follow the geometric pattern $\theta_i=\theta_0(1-\theta_0)^i$. Table 1 illustrates how quickly this decays. With trade probability 0.3, the first five weights are approximately 0.30, 0.21, 0.15, 0.10, and 0.07. At probability 0.9 they are approximately 0.90, 0.09, 0.01, 0, and 0. Thus a short lag window may be adequate for liquid stocks but inadequate for very sparse trading.

That illustration uses a geometric tail, whereas the theoretical exposition also invokes a finite maximum age. A finite regression is consequently a truncation in situations with unbounded waiting times. The paper's empirical success should not be restated as exact removal of every possible stale-price bias by a fixed finite number of coefficients.

## Aggregated coefficients: estimator and derivation

Estimate the multiple regression

$$
\widetilde R_t=a+\sum_{k=-L}^{H}b_k\widetilde M_{t+k}+w_t.
$$

Negative $k$ denotes a lagged market return, positive $k$ a leading market return, and zero the synchronous market return. The aggregated-coefficients estimator is

$$
\widehat\beta_{AC}=\sum_{k=-L}^{H}\widehat b_k.
$$

The article presents a symmetric theoretical window, then permits different practical numbers of lags and leads. Its main empirical regressions use five of each. The coefficients must come from **one joint multiple regression**. Summing slopes from separate univariate regressions is a different estimator when observed market returns are serially correlated.

The derivation in Eqs. (9)–(12) substitutes the latent market model into the stock's observed-return filter and substitutes the market filter into the right side of the multiple regression. Matching the coefficients of the underlying market returns gives convolution restrictions between $b_k$, $\theta_i$, and $\phi_i$. Summing those restrictions over all relevant dates cancels the temporal allocation because both age-weight sequences sum to one. The resulting aggregate exposure is $\beta$.

In filter language, each stale-price filter has unit response to a permanent accumulated market move. The individual regression coefficients redistribute the response in calendar time; their sum is intended to recover the total. This is a useful explanation of the article's algebra, not a claim that every finite empirical least-squares regression exactly inverts every market filter. Finite truncation, residual measurement-error correlations, changing beta, and genuine latent serial dependence can prevent the matching restrictions from holding exactly.

Leads are necessary because the benchmark can also be stale. A frequently traded stock may reflect today's true market news before much of the recorded index does; its current return then covaries with future **recorded** market returns. Including such a leading regressor does not assert that the stock forecasts tomorrow's economic shock. It corrects mismatched observation timing. In a live risk estimate, however, the leading returns must actually be available: with five leads, the latest five dependent-return months cannot yet be used in the same historical regression. This is an implementation implication of the design and prevents accidental look-ahead in a rolling backtest.

The expected sign pattern depends on relative trading frequency. For a stock trading more often than the index, the source predicts negative lagged coefficients, an upward-biased synchronous coefficient, and positive leading coefficients; the opposite relative-frequency case reverses the nonsynchronous signs. In an index of highly liquid large stocks, lagged terms generally dominate for thinly traded constituents. These are model-based population tendencies, not sign constraints to impose on every estimated coefficient.

## Choosing the window and quantifying uncertainty

Adding leads and lags trades reduced truncation bias against greater sampling variance. Dimson suggests examining whether cross-sectional variation in a given coefficient exceeds its estimated measurement-error variation. For coefficient position $k$,

$$
\widehat\tau_k^2=
\operatorname{Var}_{cross}(\widehat b_k)
-\operatorname{Mean}_{cross}\!\left[\widehat{\operatorname{Var}}(\widehat b_k)\right].
$$

This estimates the dispersion of true coefficients under independence between true exposures and estimation errors. If remote coefficients fluctuate around zero after allowing for estimation noise, their inclusion offers little additional bias reduction. A negative estimated difference can arise from sampling variation; it is not a literal negative population variance. The article does not provide a fully automated rule for resolving such estimates or selecting a window across changing samples.

In the principal UK experiment, five lags and five leads are fixed in advance to avoid selecting a favorable window from the results. The author explicitly says this is not a universal recommendation to use eleven market terms. A short sample with the same design would lose ten boundary observations and estimate twelve regression parameters including the intercept; its uncertainty can be substantial.

For implementation, the standard error of the aggregate should use the full slope covariance matrix:

$$
\widehat{\operatorname{Var}}(\widehat\beta_{AC})
=\mathbf1^{\mathsf T}\widehat V_b\mathbf1.
$$

This is the direct variance formula for a linear combination, stated here to make the procedure complete. Adding only the individual coefficient variances omits their covariances. The paper does not supply a modern heteroskedasticity-and-autocorrelation-robust implementation or a block-bootstrap design. Those would be extensions rather than reported empirical procedures.

## Practical reconstruction of the joint regression

For each security, build one row per dependent-return month with columns $1,\widetilde M_{t-5},\ldots,\widetilde M_t,\ldots,\widetilde M_{t+5}$. Estimate that entire design by least squares on the same usable calendar. Preserve the slope vector and its covariance matrix before summing the eleven slopes. Calculate the simple-regression comparator on those same rows, rather than comparing its longer available sample with the trimmed AC sample. Average security-level estimates within the published trading-frequency deciles; the tables are means of constituent betas, not regressions on ten separately constructed decile return series.

Two algebraic checks help catch implementation mistakes. With zero lags and leads, the method must reduce to the usual synchronous market-model regression. With the dependent return set equal to the same benchmark used in the regressors, a full-rank design should recover a synchronous coefficient of one, zero other slopes, and aggregate beta one, up to numerical precision. These are implementation checks implied by the regression, not new empirical validations of its economic assumptions.

A third check follows from the sample's equally weighted benchmark. When every security uses an identical design and sample, linearity of least squares implies that averaging its fitted slope vectors gives the slope vector from regressing the average security return on that design. The mean synchronous slope is therefore one and mean nonsynchronous slopes zero. If this identity fails substantially in a reproduction, inspect inconsistent missing-data masks, benchmark construction, or sample weights. Conversely, satisfying it does not establish unbiased individual exposures: the large conventional liquidity gradient can coexist with an exactly unit cross-sectional mean.

## Optional coefficient shrinkage

To reduce estimation noise, the paper adapts Vasicek-style shrinkage separately to each coefficient. The prior mean is one for the synchronous coefficient and zero for every lead or lag. For stock-specific estimation variance $v_{i,k}$ and estimated cross-sectional signal variance $\tau_k^2$, define

$$
w_{i,k}=\frac{\tau_k^2}{\tau_k^2+v_{i,k}}.
$$

Then the adjusted aggregate beta is

$$
\widehat\beta_{i,adj}
=1-w_{i,0}+\sum_{k=-L}^{H}w_{i,k}\widehat b_{i,k}.
$$

This is Eq. (15). The source conditions the componentwise argument on negligible interdependencies between coefficients. It is not a full multivariate Bayesian posterior accounting for their joint covariance. Nor are zero lead/lag priors neutral for thinly traded securities: shrinking a genuine delayed response toward zero can restore the very bias the AC method was introduced to remove.

The paper suggests using trading frequency, industry, international activity, or other company information for better priors. It does not estimate a final hierarchical model for these possibilities. In the empirical results, the most illiquid decile's adjusted beta is 0.67, versus its unadjusted AC estimate of 0.91. This is a material bias–variance tradeoff, not evidence that shrinkage always improves accuracy.

## Comparators and the simulation experiment

The article compares AC with conventional regression, trade-to-trade regression, and a Scholes–Williams procedure. Trade-to-trade returns align the stock return and market return over the same actual transaction interval. Residual heteroskedasticity motivates dividing the dependent return, market return, and intercept regressor by the square root of interval length. This requires transaction dates and a frequently recorded market index with little nontrading. Even perfect stock timing cannot fully solve a stale benchmark.

In the Scholes–Williams implementation described here, only returns between transactions in consecutive periods are used. Separate regressions on one lag, the matching market return, and one lead produce slopes that are summed and divided by $1+2\widehat\rho_M$, where $\widehat\rho_M$ is market autocorrelation. This is distinct from AC's joint regression. The observation filter is also costly: if trades occur independently with probability $\theta_0$, usable adjacent-period pairs occur with probability $\theta_0^2$, compared with trade-to-trade observations at rate $\theta_0$.

The simulation has 100 securities, 1,260 daily periods corresponding to sixty months, and ten replications. Every security has true beta one, making systematic estimator distortion directly visible. Prices have zero bid–ask spread. Monthly observed prices are generated from intermittent daily trading. Size and daily trading frequency are drawn jointly:

$$
\log C=\mu_C+\sigma_CN_1,
$$

$$
\log F=\mu_F+\sigma_F\left(\rho N_1+\sqrt{1-\rho^2}N_2\right),
$$

where $N_1,N_2$ are independent standard normals, capitalization $C$ is in millions of pounds, and $F$ is a daily trade probability. The reported calibration is $\mu_C=3.3$, $\sigma_C=1.7$, $\mu_F=-1.9$, $\sigma_F=1.2$, and $\rho=0.8$. Log capitalization is truncated at its first and ninety-ninth percentiles, and log frequency at zero to keep the implied probability no greater than one. The wording does not fully specify whether out-of-range draws are clipped or redrawn.

Market-model parameters are taken from referenced prior work and are not all reproduced in this article; neither random seeds nor complete simulation code are given. The earlier ten-thousand-period simulation validating the observed-return filter uses latent normal log-price innovations with standard deviation 0.1. That value should not be silently substituted for the separately calibrated daily-market simulation underlying Table 2.

Securities are sorted by capitalization into deciles, a proxy correlated with trading frequency. The AC comparator uses three lags and one lead. In the most liquid decile, conventional beta is 1.21, trade-to-trade beta 1.10, Scholes–Williams beta 0.99, and AC beta 1.00. In the least liquid decile the corresponding values are 0.54, 0.98, 0.93, and 0.88. The residual AC bias therefore remains concentrated at the severely nontraded end.

Across all securities the reported cross-sectional standard deviations are 0.35 for conventional regression, 0.17 for trade-to-trade, 0.48 for Scholes–Williams, and 0.36 for AC. AC removes much systematic bias without being the most statistically efficient procedure. The trade-to-trade average is 1.05, reflecting remaining benchmark effects. The prose on p. 210 refers to residual AC bias in “decile 1,” but Table 2 clearly places the substantial residual downward bias in decile 10; the table governs the numerical interpretation here.

## UK sample and return preprocessing

The London Share Price Database contains a one-in-three random sample of companies listed at or after January 1955, alongside overlapping large-company samples. The empirical period is January 1955–December 1974. Of 1,900 companies in the random sample, 421 have continuous listings throughout these twenty years. The final study sample is further restricted to essentially complete return histories.

Monthly returns are continuously compounded total returns,

$$
\widetilde R_{i,t}=\log(P_{i,t}+d_{i,t})-\log(P_{i,t-1}),
$$

using the last recorded transaction price and the month's dividend. Prices are adjusted for capital changes. Monthly log returns outside ±2 are classified as errors and treated as missing. At most two missing observations are allowed, almost always only one; a printing strike in February 1956 caused an important shared data gap. Missing returns are replaced by the corresponding Financial Times index movement. This increases the eligible sample to 314, after which fourteen companies with a majority of zero returns are excluded. The final analysis therefore uses **300 securities**.

These filters are consequential. The sample contains twenty-year survivors and drops some of the sparsest traders, so it understates the nontrading problem in the full historical market. The author acknowledges that surviving firms' trading frequency rises over time. The index substitution also mechanically imports a market return into a few dependent observations, although the paper judges the resulting bias small.

Stocks are ranked by the average age of their month-end transaction prices over the full sample and assigned to ten equal-sized deciles. Decile 1 has average price ages of approximately 0–0.1 days; decile 10 starts at 12.3 days. This sorting uses full-period information and is descriptive, not a formation rule for a real-time investment strategy. The broader database's age distribution is even more extreme: its least liquid decile has average ages above 20.1 days, and 33% of its observations are more than fifty days old.

## Benchmarks and regression samples

The equally weighted benchmark is the arithmetic mean of the sample's log returns. It contains exactly the stocks whose betas are estimated. Consequently, mean estimated beta is one by construction for common-sample conventional regressions, and the mean aggregate AC exposure also has that normalization. This accounting identity cannot by itself establish that individual betas are correct.

The alternative benchmark is the value-weighted Financial Times–Actuaries All Share Index, covering roughly 650 relatively large UK companies. Before its April 1962 introduction it is linked to the Financial Times Ordinary Share Index, an equally weighted geometric index of thirty large industrial stocks. The benchmark thus changes construction through history. The paper notes that mining, plantation, and overseas-oriented companies are not represented identically in the FTA and study sample.

The author recognizes that an arithmetic mean of log returns is not generally an attainable portfolio return. A robustness run using arithmetic simple total returns gives very similar results, but the detailed tables are not reported. The benchmark choice is therefore an explicit statistical construction, not a buy-and-hold portfolio recommendation.

The EW and FTA monthly returns correlate at 0.91, rising to 0.95 for quarterly or semiannual returns. Their first monthly autocorrelations are 0.25 and 0.07 respectively, consistent with more stale-price content in the equal-weighted benchmark. For the AC comparison, five leading and five lagged observations trim the regression window to June 1955–July 1974. Conventional comparison regressions in Table 7 use the matching trimmed window, whereas the interval-length comparisons in Table 6 use the complete January 1955–December 1974 period.

## Main results and what they do establish

Against the FTA, mean conventional monthly beta is 0.73 and mean $R^2$ is 21%. Using half-yearly changes raises them to 0.87 and 36%. Against the sample's EW index, mean beta remains one but mean $R^2$ rises from 23% monthly to 38% semiannually. This intervaling effect is evidence that return measurement changes the apparent relation; it is not unique proof that nontrading is the only cause.

Table 7 gives the cleanest same-sample comparison:

| Trading-frequency decile | Conventional beta | AC beta | Conventional $R^2$ (%) | AC $R^2$ (%) |
|---|---:|---:|---:|---:|
| 1, most frequent | 1.16 | 0.93 | 34.6 | 36.6 |
| 2 | 1.20 | 1.04 | 32.0 | 33.5 |
| 3 | 1.16 | 1.04 | 28.9 | 30.6 |
| 4 | 1.17 | 1.07 | 26.1 | 27.1 |
| 5 | 1.14 | 1.13 | 24.4 | 25.1 |
| 6 | 1.04 | 0.99 | 21.7 | 22.9 |
| 7 | 1.01 | 1.02 | 22.8 | 24.5 |
| 8 | 0.95 | 1.03 | 14.9 | 15.6 |
| 9 | 0.68 | 0.85 | 10.6 | 13.4 |
| 10, least frequent | 0.47 | 0.91 | 5.3 | 8.4 |
| All securities | 1.00 | 1.00 | 22.1 | 23.8 |

The dramatic change is the reduction in the liquidity-related spread of betas, not a large increase in explained variance. Observed stock returns remain noisy and stale even when the aggregate exposure estimate improves. Adding regressors mechanically increases unadjusted fit, so the $R^2$ increment is not independently decisive evidence of economic correctness.

The article estimates that 85% of cross-sectional variation in synchronous coefficients and 61% in first-lag coefficients reflects true coefficient differences rather than sampling error. Corresponding fractions at lags two, three, and four are 23%, 33%, and 21%, and at the first lead 21%. These support including several lags and at least one lead in this historical sample. The fifth lead's 28% is treated cautiously because unusual 1973–1974 market serial correlation may contribute.

Not every corrected decile beta equals one, nor should it. The thinly traded firms are small and often overseas-oriented: 23% of the least liquid decile consists of rubber and tea plantation companies, while the most liquid decile has different industrial composition. These differences offer an economic reason for residual beta differences. The assumption of equal true risk across trading-frequency deciles is a diagnostic prior, not an observed ground truth outside the simulation.

## Validation failure modes and research use

Suppose economic beta is one for two stocks, but one updates only intermittently. Conventional regression assigns it a lower beta because part of its response is recorded later. If its trading frequency remains stable, that low estimate will recur in the next sample. A beta-ranking stability test can then report persistence even if the true economic exposures themselves are unstable. Stability of a contaminated measurement is not consistency for the desired parameter.

Likewise, predicting next month's recorded stock return conditional on the recorded market can favor the biased coefficient. The stale stock's current print contains a mixture of current and previous market moves. A downward-biased synchronous beta may approximate that current recorded return better than an unbiased total economic exposure. An evaluation that ignores delayed responses can therefore reject the correction for doing exactly what it was designed to do.

Longer evaluation horizons reduce some timing distortion but sacrifice observations and increase sensitivity to outliers. Exact trade-to-trade evaluation requires transaction dates and a suitable daily benchmark, changing the information set and possibly the benchmark. The paper therefore does not claim to identify a universally best estimator solely from its empirical rankings.

A reproduction can implement the joint regression and aggregation from ordinary monthly data, but exact historical reproduction still requires the constituent list, capital-action and dividend adjustments, transaction-age records, original index series, and the missing-return substitutions. Complete simulation innovation parameters and code are not supplied in the paper. No trading costs or rebalancing rule are relevant to its reported risk-estimation exercise because it does not backtest an investment strategy.

The useful takeaway is to model timing mismatch at both the stock and benchmark level, distinguish total exposure from synchronous fit, and validate against a target that is not mechanically biased by the same nontrading process. AC is a practical estimator under a specified latent-return and observation model; its simplicity does not remove the need to diagnose lag truncation, benchmark composition, or genuine dynamics in economic returns.

# Does anything beat 5-minute RV? A comparison of realized measures across multiple asset classes

Lily Y. Liu, Andrew J. Patton and Kevin Sheppard. *Journal of Econometrics* 187 (2015), 293–311. DOI: 10.1016/j.jeconom.2015.02.008.

Source: [RealizedVariance_LiuPattonSheppard_2015.pdf](../../Finance/RealizedVariance_LiuPattonSheppard_2015.pdf). All 19 supplied pages were read, including the tables and figures. The authors’ 13-page August 19, 2014 supplemental appendix was also inspected. Page references below are journal pages unless specified otherwise.

## Why this matters

Estimating a day's volatility and forecasting a future day's volatility are different statistical tasks. An estimator that consistently recovers total quadratic variation from increasingly frequent observations need not provide the best finite-sample estimate on actual transaction data, and it need not be the most useful input to a forecasting model. This paper supplies a broad empirical comparison that makes those distinctions explicit.

The contribution is an evaluation design, rather than a new volatility estimator. It compares as many as 420 measures of daily quadratic variation on 31 assets, then extends the set to 648 measures for forecasting. It handles the fact that the true daily variance is latent, examines multiple-testing uncertainty, and separates choices about estimator family, sampling frequency, clock, price type and smoothing. The principal conclusion is qualified: five-minute realized variance is a difficult benchmark to reject, but benchmark-free selection does identify more accurate alternatives. For forecasting, removing jumps can matter more than choosing the theoretically most efficient estimator of total variation.

For a risk researcher, the paper provides a disciplined baseline and a warning about optimizing the wrong object. A sophisticated estimator may be worthwhile at one-second frequency on a liquid future and inappropriate on five-minute observations of a less active stock. Its reported average advantage can also shrink precisely in high-noise or high-volatility states. These are findings about the particular historical sample and evaluation design, not an assertion that five minutes is a universal optimal interval.

## Target, observations and the estimator grid

The efficient log price follows the general jump-diffusion representation in equation (1),

$$
dp(t)=\mu(t)dt+\sigma(t)dW(t)+\kappa(t)dN(t).
$$

The target for day $t+1$ is quadratic variation,

$$
QV_{t+1}=\int_t^{t+1}\sigma^2(s)ds+\sum_{t<s\le t+1}\kappa^2(s)
=IV_{t+1}+JV_{t+1}.
$$

Here $IV$ is integrated variance and $JV$ is the sum of squared jumps. With ideal observations, realized variance is the sum of squared intraday log returns and converges to $QV$ as the mesh shrinks. With observed prices contaminated by market frictions, using every available return can instead accumulate noise. The empirical comparison does not assume that all candidate estimators have correct noise models; that is part of what it tests.

For each price series, the main grid uses calendar-time intervals of 1 second, 5 seconds, 1 minute, 5 minutes and 15 minutes. Tick-time versions choose spacings that match those average calendar durations, and there is also an every-tick version. Thus there are 11 basic sampling configurations. Ten have subsampled counterparts; every-tick sampling cannot be further subsampled in this sense. Subsampling averages estimates on shifted grids at a fixed spacing, generally using at most ten partitions. It is distinct from averaging adjacent prices before calculating returns.

The baseline is ordinary five-minute RV computed from transaction prices in calendar time, without subsampling. It is a particular member of the RV family. Statements about this baseline should not be applied indiscriminately to all five-minute RV variants, especially where the paper pools tick-time and calendar-time results.

The eight main estimator classes and their implementation choices are as follows:

| Class | Construction and choices used in this study |
|---|---|
| RV | Sum of squared intraday log returns; sparse sampling reduces exposure to noise; shifted-grid averages produce RVss. |
| Bandi–Russell RV | Choose an estimated optimal spacing from noise variance and integrated quarticity; include bias-corrected and uncorrected versions. Quarticity uses 39 prices spaced uniformly in tick time. |
| RVac1 | Add a first-order return-autocovariance adjustment to RV to address serial dependence associated with noise. |
| TSRV/MSRV | Combine slower and faster time-scale estimates to remove noise bias; slower scales use the original methods' asymptotic-variance tuning. |
| Realized kernels | Flat-top Bartlett, cubic and modified Tukey–Hanning 2, plus non-flat-top Parzen; daily bandwidths follow the cited kernel implementation. |
| Pre-averaged RV | Form overlapping locally weighted returns; the window is $K=\lceil\sqrt n\rceil$, with $n$ the number of sampled intraday returns. |
| Realized range | Replace squared endpoint returns by appropriately normalized intrablock high–low ranges; use block lengths 5 and 10. |
| Maximum-likelihood RV | Fit the MA(1) observed-return structure implied by an efficient price plus independent noise, using Gaussian likelihood. |

Not every estimator receives every grid option. Kernels and pre-averaged RV are not additionally subsampled in the main count. The Bandi–Russell method chooses its own frequency, so it has eight versions per price series rather than 21. The exact count in footnote 5 is 136 nonsubsampled and 74 subsampled measures per price series, totaling 210; with transactions and quotes there are 420. Computed indices have no quote series, so their corresponding set is 210. The family labels conceal materially different tuning and sampling combinations; averaging all members is not a ranking of an optimally tuned family.

Some candidates are deliberately poorly matched to their sampling frequency, serving as checks that the comparison detects inferior procedures. Some widely used measures are not consistent for total $QV$ in the presence of jumps. The authors explicitly retain Bandi–Russell RV, range-based variance and MLRV despite that issue. Consequently, the experiment is a finite-sample empirical comparison of useful procedures, not a contest restricted to estimators of identical asymptotic scope.

The supplied article describes the method families and their selected settings, but does not reproduce the full defining formula and finite-sample edge treatment for each published estimator. Exact numerical reproduction of all 420 columns requires the referenced implementations. The calculations used code based on Kevin Sheppard's Oxford Realized/MFE toolbox. A replication should version that code and record bandwidth rounding, endpoints and treatment of days with too few observations, rather than substituting an arbitrary current implementation.

## Data and preprocessing

The data are intraday transactions and quotations from Thomson Reuters Tick History, principally January 2000–December 2010. There are five asset classes:

- Ten individual stocks: Coca-Cola, LSI, Microsoft, International Flavors & Fragrances and Sysco in the US; Diageo, Vodafone, SABMiller, Schroders and RSA Insurance in the UK.
- Six government-bond futures: US 2-, 5-, 10- and 30-year instruments and German short- and long-term government-bond futures.
- Five currency futures against USD: CAD, AUD, GBP, EUR and JPY.
- Five equity-index futures: EuroStoxx50, Nikkei225, DAX, FTSE100 and E-mini S&P500.
- The corresponding five computed equity indices, which are constructed price series rather than directly traded assets.

The stock series and most European/index series begin in early January 2000. US 5-, 10- and 30-year bond futures start January 2, 2001; the 2-year starts January 2, 2003. Currency futures start January 2, 2004. Most series end December 30 or 31, 2010, while several bond and index futures end October 29. Table 1 gives the individual dates and retained day counts. Its DAX computed-index row prints a 2006 start alongside 2,781 daily observations, which cannot both describe a sample ending in 2010; that start date must be checked against the underlying data rather than silently accepted. The table also uses “DAX 40” as a label; a replication should identify the historical contract and index from the actual data identifier.

Days with recorded prices covering less than 60% of regular operating hours are removed. The largest reported fraction removed is 1.7% for E-mini S&P500 futures. The mean retained series has 2,537 trading days; the shortest has 1,759 and the longest 2,782. Assets vary greatly in activity: average trade duration is about 0.5 seconds for E-mini futures but 52.4 seconds for Schroders. This heterogeneity is central to why a single frequency is not uniformly desirable.

For near-continuously traded futures, the liquid session is determined from local-time five-minute blocks. The selected contiguous region uses blocks whose fraction of trades exceeds 20% of the uniform daily fraction $1/288$. Local timestamps avoid mechanically shifting the session with daylight saving. The exact session boundaries need to be stored in a replication output because different exchange sessions change the daily object being measured.

The supplementary cleaning rules discard out-of-session observations, extreme one-tick reversals and crossed or abnormally wide quotes; common thresholds are 15 times the median spread. Duplicate timestamps are aggregated by median price. Trades and quotes are cross-checked within a one-minute neighborhood. Futures use volume-based selection with one irreversible roll date. Its QT1 upper buffer says “daily median standard deviation,” whereas the lower buffer uses spread; that ambiguity needs code verification. Manual cleaning affected under 0.1% of days. Estimators below 0.0001 for rates/FX or 0.001 otherwise on over 5% of days are excluded; isolated subthreshold values are replaced by the previous day's estimate. These thresholds require the authors' return units. See [supplement, sections S.A.1–S.A.2](https://public.econ.duke.edu/~ap172/Liu_Patton_Sheppard_19aug14_APPENDIX.pdf).

There is no overnight-return addition in the stated open-to-close target. Nor is this an investment-universe construction exercise with delisting or portfolio weights. The contract-roll convention and retrospective cleaning are appropriate to a measurement comparison but must not be treated automatically as information available to a live trading strategy.

## Evaluating a latent variance without declaring one candidate the truth

A naive evaluation against another high-frequency measure can reward an estimator merely because it shares that proxy's noise. The paper follows Patton's data-based ranking approach. The primary proxy is the squared open-to-close return, denoted $RV_{daily}$, and an adjacent day's proxy is used to break contemporaneous measurement-error dependence.

Write $M_{i,t}$ for candidate $i$, $\theta_t$ for true daily $QV$, and $Z_t$ for the proxy used in evaluation. The QLIKE loss is

$$
L(\theta,M)=\frac{\theta}{M}-\log\left(\frac{\theta}{M}\right)-1.
$$

For two positive candidate measures, the difference simplifies to

$$
L(Z_t,M_{i,t})-L(Z_t,M_{j,t})
=Z_t\left(M_{i,t}^{-1}-M_{j,t}^{-1}\right)
+\log M_{i,t}-\log M_{j,t}.
$$

This expression shows the identification requirement. The proxy error must be orthogonal to the inverse-measure difference in expectation. Unconditional equality of the proxy's mean and the target's mean alone is not sufficient. The one-day lead construction formally uses a random-walk approximation for daily $QV$, together with restrictions on measurement errors. High persistence makes the approximation plausible, but does not make it an identity for every stationary volatility process.

The article's estimated first- and second-order latent-QV autocorrelations average approximately 0.95 and 0.92. The correction uses the Hansen–Lunde instrumental-variables method, with demeaned lags 4–10 as instruments. Raw realized-measure autocorrelations are much lower because measurement error attenuates them. For Microsoft, five-minute RV's raw first-order autocorrelation is 0.72, whereas the latent-QV estimate is 0.96. These diagnostics support persistence but do not verify every orthogonality condition required by the ranking method.

The primary comparisons use $Z_t=RV_{daily,t+1}$. This is an ex-post evaluation instrument, not a feature permitted in a forecast at time $t$. Alternatives are leads of 15-minute RV, five-minute RV, one-minute MSRV and one-minute Tukey–Hanning2 kernels. The text generally identifies tick-time transaction proxies, while footnote 29 describes calendar-time proxies for the MCS robustness exercise; the exact comparison-specific setting should be retained. Proxies whose average differs significantly from daily squared returns are flagged in Table 5. A smaller proxy variance may improve power but introduces more risk of high-frequency bias.

The positivity requirement matters for QLIKE. Negative or essentially zero estimates cannot simply be passed to logarithms and inverses. The preprocessing rule above is part of the experimental design, not a cosmetic cleaning step. For loss differences, target-only logarithmic terms cancel; implementing that algebraic difference also avoids a spurious numerical issue when a squared-return proxy is zero.

## Two inferential questions, two different answers

The first question is whether any candidate significantly beats the specified five-minute RV baseline. Section 5.3 uses Romano–Wolf stepwise multiple testing, separately looking for better and worse candidates. The stationary bootstrap has 1,000 replications and expected block length ten days. Dependence must be preserved across candidates within a resampled day, since all are measured from the same asset's observations. The relevant persistence is that of loss differences, not the level of volatility. The authors report an average automatically selected block length of four for loss differences, compared with 97 for the realized measures themselves, supporting ten as a conservative practical choice.

The procedure controls the probability of at least one false rejection in the tested family. This does not equal the expected number of falsely rejected candidate measures. Footnote 25's informal conversion of familywise error into “0.05 of a measure” should not be used as a counting formula. There are also multiple asset-specific testing exercises, so control within an asset is not automatically simultaneous control over all assets and every robustness configuration.

Under the main daily proxy, Table 5 reports no significantly better estimator for any asset. Many estimators are significantly worse: Microsoft has 284, EuroStoxx50 futures 211 and German short-government-bond futures 372. The paper reports approximately 193 worse estimators per asset on average. Candidate counts differ because computed indices have only 210 measures and a few measures fail preprocessing. Thus the reported average should not be interpreted as 193 rejections out of 420 for every asset.

With more precise proxies, the notable valid exception is US 10-year Treasury futures. Depending on the proxy, 9, 24, 28 or 23 measures beat five-minute RV. These include high-frequency kernels, multiscale and range methods, and one-minute RV or RVac1. The S&P500 index row also contains numerical rejections under some proxies, but these are shaded as proxies with significantly different means; the paper's substantive conclusion excludes such unreliable proxy cases. Failure to beat the benchmark does not establish equal accuracy, and the ability to reject very poor estimators does not guarantee high power against small improvements.

The second question avoids a privileged benchmark: which candidates survive a model confidence set procedure? The authors construct 90% MCSs with the same primary proxy and stationary-bootstrap settings. Iterative elimination leaves a set intended to contain the best candidate among those considered; it does not identify a uniquely optimal estimator across all conceivable methods.

The MCS size ranges from 2 to 148 measures, averaging about 39. The most frequent survivor across the aggregate table is one-minute subsampled RV. Table 7 includes 31% of one-minute RVss variants compared with 15% of five-minute ordinary RV variants; one-second kernels have 29% inclusion. These are proportions of configurations within family/frequency cells across assets, not probabilities that a named estimator is correct. For individual equities, one-minute RVss reaches 53%, and one- and five-second kernels reach 58% and 55%. For index futures, one- and five-minute RV are very different choices: the table shows 25% inclusion at one minute and zero at five minutes. Very coarse sampling generally wastes the structure of noise-corrected estimators.

The apparent tension between the two tests is substantive. Benchmark-based testing is conservative about a large family of improvements over an acceptable reference. MCS elimination can narrow the candidate set through many relative comparisons. Neither result justifies saying that five-minute RV is definitively best; together they say that convincing, robust gains over it are harder to establish than raw rankings imply.

## Which design choices matter?

Table 4 compares matched estimators that differ only in price series, sampling clock, subsampling or pre-averaging. The entries are the percentage with significantly positive loss-difference statistics minus the percentage with significantly negative statistics. A negative entry favors the first named procedure, and the values are not percentage changes in variance-estimation error.

At relatively low frequencies, transaction prices generally perform better than midquotes. For ordinary RV the trade-minus-quote comparison is −54 at five minutes, while it is +73 at one second. Quote advantages at the highest frequency and trade advantages after sparse sampling are consistent with bid–ask bounce being more damaging before noise has been diluted. The best raw rankings differ across regions: US-stock top-ten configurations use trades and UK-stock configurations use midquotes.

Calendar-time sampling is often preferable at one and five seconds, while tick-time sampling becomes attractive at five and fifteen minutes. For ordinary RV, the corresponding entries are −84 at one second and +23 at five minutes. Subsampling tends to help sparse RV but is not a universal improvement: the not-subsampled-minus-subsampled comparison for RV is +29 at five minutes and +48 at fifteen minutes, whereas realized range has negative entries there. Pre-averaging ordinary RV is helpful at very high frequency and harmful at low frequency: the not-pre-averaged-minus-pre-averaged comparison is +77 at one second but −100 at five and fifteen minutes.

These findings identify a compatibility problem between data resolution and estimator design. Pre-averaging a series that is already sparsely sampled may remove useful variation; adding a noise correction to a coarse series may increase error when little removable noise remains. The results do not support mechanically stacking all available corrections.

## Conditional performance and its limits

Section 5.5 regresses the normalized loss advantage of each competing estimator over five-minute RV on lagged market conditions and asset/region indicators:

$$
L(Z^i_t,M^i_{0,t})-L(Z^i_t,M^i_{j,t})
=\beta_j'X^i_{t-1}+\gamma_j'Z^i+\varepsilon^i_{j,t}.
$$

Here $M_0$ is the five-minute baseline; positive left-hand values favor the competitor. Competitors are daily RV, one-minute RV, five-second MSRV, one-minute RVac1, five-second Tukey–Hanning2 RK and one-second MLRV, all using calendar-time transaction prices.

The covariates are average intertrade duration, local-currency trading volume, bid–ask spread, first-order correlation of five-second returns, jump share, relative noise and log volatility. Duration, volume and spread are divided by their own preceding 60-day means; 120- and 250-day versions give similar qualitative results. Jump share is $\max(RV-BPV,0)/RV$, with five-minute tick-time transactions. Log volatility uses subsampled five-minute RV. Covariates are winsorized at the 0.5% and 99.5% levels and demeaned; loss differences are divided by full-sample standard deviation.

The noise ratio is described as noise variance divided by per-observation efficient variance. Footnote 33 labels its numerator a return “autocorrelation,” although that would be dimensionless and can be negative, inconsistent with a variance ratio. A replication needs to verify the original routine's noise-variance estimator and sign convention. It should not substitute raw autocorrelation into that formula just because of the wording.

The principal panel excludes computed indices because they lack volume and spreads, leaving 26 assets and at most 2,860 dates in an unbalanced panel. Driscoll–Kraay standard errors allow heteroskedasticity, serial dependence and cross-sectional dependence; the implementation uses eight Newey–West lags. Asset-class dummies and UK/Europe/Asia indicators are included, with the US region omitted as reference. This is not a fully saturated individual-asset fixed-effects design.

Table 8's noise-ratio coefficients are negative for every sophisticated competitor. Their t-statistics include −8.84 for one-minute RV, −4.98 for MSRV and −13.11 for MLRV. Higher noise therefore reduces the relative benefit of these estimators. Log-volatility coefficients are negative and significant for one-minute RV, MSRV and RK, but not uniformly across all methods: RVac1 and MLRV have positive, insignificant coefficients in this specification. UK-region effects are negative for all five competitors, with t-statistics from −3.08 to −21.47. The interpretation is conditional association, not proof of a structural causal effect of geography.

The paper's closing sentence about high-volatility gains should be read with the pair being compared in mind. High volatility strengthens five-minute RV relative to daily squared returns; Table 8 often shows weaker gains from moving beyond five-minute RV to sophisticated alternatives. Those are different comparisons. The panel also does not by itself deliver an implementable switching rule: the relevant total conditional difference includes intercepts and all covariates, and uncertainty must be considered before changing estimators.

## Forecasting experiment

Forecasting adds 228 jump-robust measures, giving up to 648 inputs. These include bipower variation and its pre-averaged form, quantile RV, minimum/median neighboring-return estimators, and truncated RV. Quantile RV uses overlapping blocks around 100 returns and quantiles approximately 0.85, 0.90 and 0.96, with the original method's optimal weights. Truncated RV excludes returns larger than three local volatility estimates in magnitude. The local-volatility procedure may fail on illiquid days at one- or five-second spacing; those cases are treated as nonimplementable rather than assigned fabricated values.

Each measure enters a separate direct HAR regression, estimated separately for each horizon $h=1,\ldots,50$:

$$
\widetilde\theta_{t+h}=\beta_{0,j,h}+\beta_{1,j,h}M_{j,t}
+\beta_{2,j,h}\frac{1}{5}\sum_{k=0}^{4}M_{j,t-k}
+\beta_{3,j,h}\frac{1}{22}\sum_{k=0}^{21}M_{j,t-k}+\varepsilon_{j,t}.
$$

The response is the squared open-to-close return on the single future day $t+h$, not cumulative variation over the next $h$ days. Coefficients are re-estimated daily on a rolling 500-day window. When reconstructing the exercise, the training pairs must have target realizations available at the forecast origin; including targets from beyond that origin would introduce look-ahead. The supplied description does not specify every boundary convention or the treatment of negative linear HAR forecasts, which matters under QLIKE and should be checked in the code.

A HAR model using a jump-robust input can exploit persistence in the continuous component without making today's jump a predictor with identical persistence. This is a reduced-form strategy; it is not an explicit two-component jump/continuous forecasting model. Separate-component models and combinations of multiple realized measures are outside the comparison.

Table 9 summarizes 90% forecast MCS membership over horizons one through five. Across all assets, five-minute truncated RV has 61% inclusion and five-minute quantile RV 63%, compared with 35% for ordinary five-minute RV. At fifteen minutes, truncated RV reaches 63% versus 30% for RV. For rates, truncated RV reaches 88% at fifteen minutes. For currencies, quantile RV reaches 96% at five minutes. Individual equities differ: fifteen-minute subsampled RV, five-minute range variance and one-minute pre-averaged BPV each reach 58%, exceeding the corresponding short-horizon truncated-RV results.

Discrimination weakens at longer forecast horizons. At 50 days, about 43% of all candidates are still excluded on average, but MCS sizes approach the full set for several asset classes. Figure 2 shows the specific baseline five-minute RV in roughly 30% of short-horizon asset MCSs and around 60% at longer horizons. These are proportions across assets and should not be confused with Table 9's proportions across estimator configurations.

## Reproduction priorities and practical conclusion

An effective reconstruction should retain the full estimator-by-asset-by-day array, document every preprocessing exclusion, and reproduce the benchmark loss-difference series before attempting rankings. Preserve common bootstrap indices across candidate columns, distinguish the lead proxy used for measurement evaluation from lagged information used in forecasts, and report the family being controlled by each test. Results from the retrospective ranking exercise and the rolling forecast exercise should remain separate.

The main unresolved inputs are proprietary tick data and identifiers, ambiguous source wording in a few preprocessing/diagnostic definitions, precise historical toolbox settings and boundary handling. The article does not present executable code for every imported estimator, and its broader comparison excludes later estimators. It reports statistical forecasting gains rather than a portfolio backtest, transaction-cost-adjusted return improvement or a full economic utility calculation.

The reliable operational takeaway is to begin with a clearly defined sparse RV baseline, consider modest subsampling, and test whether a more elaborate procedure improves the actual task on the actual market. This source shows that theoretical noise robustness, empirical daily measurement accuracy and forecast usefulness cannot be treated as interchangeable claims.

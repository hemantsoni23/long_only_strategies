# How rating agencies achieve rating stability

Edward I. Altman and Herbert A. Rijken, *Journal of Banking & Finance* 28 (2004), 2679–2714. DOI: 10.1016/j.jbankfin.2004.06.006. Source: [CreditRating_AltmanRijken_2004.pdf](../../Finance/CreditRating_AltmanRijken_2004.pdf), 36 pages. Page references below are journal pages.

## Why this matters

Rating changes are often treated as observations of underlying credit-quality changes. This paper shows why that identification can fail: agencies both emphasize long-horizon information and deliberately smooth their decisions. A transition matrix estimated from published ratings can therefore understate the movement of a more responsive measure of credit quality, while serially correlated rating changes may reflect incomplete adjustment rather than predictable innovations in fundamentals.

The contribution is an empirical decomposition and a simple migration-policy model. The authors estimate the same six-variable financial-score system against three targets: one-year survival, longer-horizon survival, and the agency rating itself. They then compare the migration behavior of ratings implied by those scores with actual S&P ratings. Finally, they pass the agency-rating score through a threshold and partial-adjustment filter. A threshold around 1.25 notches and adjustment of roughly 75% of the gap reproduce important observed stability and drift patterns.

These are descriptive approximations to agency behavior. The paper does not derive an optimal stability policy from transaction costs, lender utility, or a social-welfare objective. It also does not establish an observable “true” credit-quality process. Its decomposition depends on treating its score models as credible point-in-time benchmarks and on attributing the residual dynamics principally to migration policy.

## Universe, calendar, and information availability

The rating source is the July 2002 S&P CREDITPRO database, with ratings beginning January 1981. It is matched to COMPUSTAT and market-equity data. The sample is restricted to publicly traded, nonfinancial US firms. Fewer than half of CREDITPRO records can be matched to COMPUSTAT; the resulting inference is not about the entire rated private-company universe.

The 1981–2001 panel includes 1,772 obligors, with histories from one to 21 years. There are 13,718 firm-year observations: 11,890 rated observations and 1,828 with nonrated status. Nonrated observations are included in the default-prediction model to increase sample size and are monitored for subsequent default, but cannot supply the dependent variable for the agency-rating regression.

Each observation is dated at the end of June. The rating and market equity use that date. Balance-sheet data come from the latest fiscal quarter ending in the previous calendar year; income-statement information uses the four fiscal quarters in that previous calendar year. Thus accounting data are lagged about six months. For firms with non-December fiscal years, the relevant quarterly records must be reconstructed rather than substituting their most recent annual filing indiscriminately.

A one-year survivor must have stock-price observations both at the June origin and at the following June. A default observation is a firm defaulting between those two dates. There are 13,447 survivors and 271 default observations over the full panel. Requiring a subsequent listing introduces selection among nondefaulting delistings; the authors report robustness but do not supply all underlying checks. The two-year 2000–2001 period contains 121 of the 271 default observations, an unusually large concentration that affects parameter stability.

## The six predictors and exact transformations

Let the predictor vector contain the following entries, with all quantities in consistent units:

$$
X=\left(\frac{WK}{TA},\; -\log\left[1-\frac{RE}{TA}\right],\; -\log\left[1-\frac{EBIT}{TA}\right],\; 1+\log\frac{ME}{BL},\; \log\frac{BL}{Mkt},\; Age\right).
$$

$WK$ is net working capital, $TA$ total assets, $RE$ retained earnings, $EBIT$ earnings before interest and tax, $ME$ market equity, $BL$ book total liabilities, and $Mkt$ total US equity-market value. The size variable is normalized liabilities, not raw dollar liabilities or log equity. Age is years since first agency rating, capped at ten; firms already rated at the 1981 sample start are assigned ten.

Working capital proxies liquidity, retained earnings cumulative profitability, EBIT current profitability, and market-equity-to-liabilities leverage and forward-looking prospects. Size and rating age capture additional cross-sectional default variation. The interpretation of size as too-big-to-fail protection is the authors' economic explanation, not a causally identified treatment effect.

Each variable's lowest and highest 0.5% values are replaced by the 0.5th and 99.5th percentiles. The paper reports this winsorization and the logarithmic transformations but does not provide a fully ordered cleaning algorithm or handling of invalid log domains. A reconstruction must check $ME/BL>0$, $RE/TA<1$, and $EBIT/TA<1$ before transformation, and document how missing or invalid records are treated. It must not feed percentages such as 20 into a ratio intended as 0.20.

The transforms reduce tail influence: for instance, changing $ME/BL$ from 0.5 to 1 carries more log-score information than an equal absolute increase at a very high valuation. These transformed quantities, not the raw ratios, multiply the reported regression coefficients.

## Survival logit: the source's outcome convention matters

The paper calls the first model a default-prediction, DP, model, but codes its binary response as one for survival and zero for default. Some introductory equations call the probability a default probability; the coding and positive coefficients show that the fitted logistic probability must be interpreted as survival. In unambiguous notation, let

$$
s_i=\alpha+\beta'X_i,\qquad P(Y_i=1\mid X_i)=\Lambda(s_i),\qquad PD_i=1-\Lambda(s_i)=\Lambda(-s_i),
$$

where $Y=1$ means survival and $\Lambda(z)=1/(1+e^{-z})$. Estimate by maximizing the Bernoulli log likelihood. A large DP-score denotes better credit quality, not greater default risk. No extra realized disturbance should be added to the linear predictor when generating fitted probabilities; the paper's notation with an error term is best read as latent-model shorthand.

The main DP parameters are estimated on 1981–1999. Table 2 gives

$$
s_{DP}=7.06+0.41X_1+0.20X_2+3.78X_3+1.28X_4+0.47X_5+0.20X_6.
$$

There are 11,990 observations and 150 subsequent defaults in this fit, with pseudo-$R^2=0.355$. The market-equity ratio coefficient has z-statistic 12.83; EBIT 3.79, size 6.40, and age 6.83. Working capital and retained earnings have much smaller z-statistics, 0.75 and 0.58. Correlation among fundamentals means these coefficients should not be interpreted as isolated structural effects.

Standard errors use a Huber–White sandwich generalized to clusters containing all observations of a firm. This permits heteroskedasticity and within-firm dependence. It does not by itself address dependence across firms caused by the same aggregate shock; that distinction is particularly relevant for longer-horizon overlapping outcomes.

## Ordered logit for the agency rating

The agency-rating, AR, model uses the same predictors with an ordered-logit likelihood. Rating numbers increase with quality: CCC/CC/C is 1, B− is 2, B is 3, B+ is 4, BB− is 5, BB is 6, BB+ is 7, BBB− is 8, BBB is 9, BBB+ is 10, A− is 11, A is 12, A+ is 13, AA− is 14, AA is 15, and AA+/AAA is 16. Lower grades and the top grades are combined to avoid very small cells.

Let $a_i=\beta_{AR}'X_i$ and $a_i+\epsilon_i$ be a latent credit-quality index with standard logistic error. For ordered cutpoints $B_0=-\infty<B_1<\cdots<B_{16}=\infty$,

$$
P(R_i=k\mid X_i)=\Lambda(B_k-a_i)-\Lambda(B_{k-1}-a_i).
$$

The likelihood is the product of the probability assigned to each observed class. A location normalization is necessary: an unrestricted intercept and all cutpoints cannot both be separately identified. The reported Table 2 implementation has no intercept in the AR column. Its main 1981–1999 slopes are

$$
a_i=-1.80X_1+3.33X_2+4.70X_3+0.85X_4+0.95X_5+0.082X_6.
$$

For reproduction of class probabilities, the finite lower boundaries listed in Table 2, in increasing quality order from B− through AAA/AA+, are −13.05, −11.65, −10.31, −8.56, −7.64, −7.01, −6.55, −5.99, −5.30, −4.73, −4.14, −3.06, −2.25, −1.61, and −0.24. These map to $B_1$ through $B_{15}$ in the interval formula; the displayed table lists the lower boundary alongside the higher class. The bottom class has lower boundary $-\infty$ and the top class has upper boundary $+\infty$.

The AR fit uses 10,345 observations and has pseudo-$R^2=0.214$. All six slopes are statistically significant; working capital has a negative sign, unlike the weak positive DP coefficient. An AR-score is a continuously updated statistical predictor of the agency's rating level. It is not the agency's published sticky rating, nor is it automatically a calibrated survival probability.

Later descriptive tables shift the AR-score's location to the lower boundary of the B rating. Such a common shift changes neither ranks nor increments. A replication should maintain one clear normalization and shift boundaries with scores whenever probabilities are evaluated.

## Inferring the effective horizon

To compare horizons fairly, all models in Table 3 are refitted using origins in 1981–1995, allowing six years of subsequent outcomes. Long-term DP models code survival beyond four or six years as one and default within that interval as zero. Observations without the required outcome horizon need a defined exclusion rule; the source describes the endpoint definitions but does not release the individual cohort masks.

The comparison normalizes coefficient magnitudes by predictor dispersion:

$$
RW_j=\frac{|\beta_j|\sigma(X_j)}{\sum_{l=1}^{6}|\beta_l|\sigma(X_l)}.
$$

This is a standardized absolute-coefficient share, not a variance decomposition; correlated predictors prevent that interpretation. The standard deviations use the common 1981–1995 panel.

| Predictor | One-year DP share | Four-year DP share | Six-year DP share | Agency-rating share |
|---|---:|---:|---:|---:|
| Working capital | 0.0% | 3.1% | 4.8% | 7.3% |
| Retained earnings | 5.2% | 6.9% | 11.8% | 24.7% |
| EBIT | 8.9% | 8.0% | 4.0% | 7.6% |
| Market equity/liabilities | 41.7% | 32.9% | 29.8% | 20.1% |
| Size | 25.7% | 31.5% | 33.9% | 34.7% |
| Age | 18.5% | 17.6% | 15.7% | 5.6% |

Longer-horizon prediction puts less relative weight on market valuation and more on accumulated profitability and size. The AR model lies closer to the six-year model than to the one-year model, but they remain materially different. Calling six years the exact agency horizon would overstate the evidence: it is the closest of the tested horizons, and the source explicitly notes that still longer horizons might reduce remaining differences.

The six-year model used in subsequent analysis has intercept 6.84 and slopes (0.82, 1.12, 1.57, 0.93, 0.66, 0.151), with 6,782 survivors and 400 default observations. The four-year counterpart has intercept 7.06 and slopes (0.56, 0.70, 3.31, 1.09, 0.64, 0.179). Their pseudo-$R^2$ values are 0.304 and 0.326. These different-horizon probabilities are cumulative endpoint probabilities, not annualized hazard rates.

## Converting scores into comparable rating histories

Every June, rank firms by each credit-model score. Allocate them to 16 discrete rating bins so that each bin contains exactly as many firms as the corresponding actual S&P category in that year. This matched-distribution mapping is crucial. It controls category population differences across models, and it means modeled rating migration depends on changing cross-sectional ranks and bin boundaries, not just individual absolute default probabilities.

The same firm can therefore experience a model-rating change despite an unchanged continuous score if peers or category counts change. This becomes important in the filtered-score experiment below. Ties, precise matched-universe masks, and handling of incomplete score histories are not specified in algorithmic detail.

The authors also estimate score units per notch, denoted $\gamma$ here. Within each year, regress category-average scores on rating numbers separately for grades 2–7 and 8–15. For the extreme categories, use the adjacent mean-score difference. Smooth each slope using the current and two preceding years; 1981 uses one year, 1982 two. Across the full sample, illustrative AR slopes are about 0.690 in the lower-grade range and 0.471 in the upper range; DP counterparts are 0.405 and 0.307. The local year/class conversion must be used in the threshold rule rather than treating one score unit as one notch.

The empirical benchmarking covers 1981–2001, while the principal model coefficients use 1981–1999 or 1981–1995. It is mainly an explanatory in-sample comparison with a final-period extension, not a rolling out-of-sample exercise. Reestimating every year would answer a related but different question.

## What changes, how often, and with what persistence

Table 6 reports 10,257 annual transitions including migrations to default. No-change probabilities are 76.6% for actual ratings, 51.0% for AR-model ratings, and 39.3% for one-year DP ratings. Thus annual change probabilities are 23.4%, 49.0%, and 60.7%. Both horizon choice and the absence of agency smoothing increase modeled migration.

The unconditional mean annual migration is −0.15 notch for agency ratings, −0.15 for AR ratings, and −0.13 for DP ratings. The panel's entry/exit accounting helps explain the downward drift: firms enter near BB+, exit near BB on average, and remain for an average uninterrupted 6.35 years. Around 80% of the overall downward movement is attributed to distressed firms approaching default. This background mean must be separated from conditional serial persistence.

After a previous downgrade, the next agency-rating change averages −0.47 notch. After no change it averages −0.14; after an upgrade it averages +0.08. Relative to the −0.15 unconditional mean, the upgrade and downgrade continuation effects are much more symmetric than their raw levels suggest. AR and DP rating changes exhibit little corresponding directional persistence in the authors' tests.

The mechanism proposed is partial adjustment. If a permanent deterioration requires a two-notch reduction, an agency can recognize most of it first and the rest later; published migrations then become serially correlated even if new fundamental innovations are not. Outlooks and watchlists can convey part of the information that is absent from the published rating level. The paper cites this possibility but does not incorporate those signals into its own score-filter estimation.

## Event-time evidence on delay and overshooting

For each June year $T$, group firms according to whether their rating rose, fell, or stayed unchanged over the preceding year. Calculate annual changes in actual and modeled ratings across the surrounding event window, accumulate from event time −5, and average over event years. Subtract the no-change group's cumulative path to reduce the common downward trend and changing-sample effects.

Because a regression of modeled rating on actual rating has slope below one, scale model event paths by the inverse of that slope. The reported slopes are 0.83 for AR ratings, 0.79 for six-year LDP ratings, and 0.74 for DP ratings. This scaling is distinct from the continuous-score-per-notch conversion $\gamma$ used in the filter.

In Figure 3, the cumulative agency path surrounding a downgrade ends near −2.2 notches. At event time −1, the AR path has already deteriorated about 0.9 notch while the agency path has moved only about 0.3. For upgrades, the endpoint is roughly +1.6 notches; the corresponding pre-event AR change is +0.7, versus approximately −0.1 for the agency path. One-year DP paths react most strongly and temporarily exceed the eventual cumulative movement, which the authors interpret as sensitivity to transitory credit-quality changes.

These are annual event-window averages, not exact timestamp estimates of how many days a specific agency waits. Firms disappear through default, delisting, mergers, and missing data. Subtracting the no-change path is a useful adjustment but not a proof that the changing event samples are exchangeable. Likewise, the long-horizon endpoint is a proxy for the permanent component, not a directly observed permanent shock.

## A reconstructable threshold and partial-adjustment filter

For each uninterrupted firm history, initialize the modified score $M_0=a_0$. Let $\theta$ be the threshold in notches and $f$ the fraction of the gap closed when action occurs. At annual date $t$ define $d_t=a_t-M_{t-1}$ and use the corresponding positive score-per-notch scale $\gamma_t$. Equations (5.1)–(5.2) are

$$
M_t=\begin{cases}
M_{t-1},& |d_t|/\gamma_t<\theta,\\
M_{t-1}+f d_t,& |d_t|/\gamma_t\geq\theta.
\end{cases}
$$

The threshold is symmetric in the implemented model. It suppresses small movements. Conditional on triggering, the adjustment fraction determines how much of a large movement remains unrecognized. With $f=1$, the score fully catches up; with $f<1$, it retains a gap that can produce continuation if sufficiently large or if subsequent fundamentals move in the same direction. Partial adjustment alone does not force another rating change: the remaining gap must again satisfy the threshold.

Next, convert modified scores to ratings using the same annual rank-and-count mapping. Then apply a necessary correction: whenever $M_t=M_{t-1}$, carry forward the previous modified rating rather than accepting a rating change induced only by shifting cross-sectional bin boundaries. This means exact matching of yearly class counts no longer holds after the correction; the source reports differences of at most 10% per class. Omitting this step would contaminate the estimate of a no-action region with artificial migrations.

The minimum triggered score jump is $\gamma_t f\theta$. The authors state that it is sufficient for nearly all triggered jumps to generate a rating change. “Nearly all” is important: discretization and changing rank cutoffs can still affect the correspondence, and the paper does not provide a complete tie-breaking rule.

Search over threshold and adjustment values to match migration distributions, conditional means, and migration-size dispersion. Defaults are excluded from this fitting experiment because a default designation is not a discretionary agency migration. The source reports a comparison grid rather than a formal objective function with weights, optimizer, confidence region, or statistical identification test for the two filter parameters.

## Estimated policy and transition-matrix implications

In Table 7's 8,416-observation nondefault experiment, actual ratings are unchanged 78.7% of the time. Unfiltered AR ratings are unchanged only 53.8%. A threshold of 1.25 with full adjustment gives 79.4% unchanged, showing that most of the frequency reduction comes from the threshold. Changing the fraction to 0.83 or 0.66 leaves no-change frequencies at 79.4% and 79.5%, respectively.

The fraction instead determines persistence and jump sizes. Following a previous downgrade exceeding one notch, actual subsequent migration averages −0.30. The filtered AR model gives −0.10 with full adjustment, −0.25 with fraction 0.83, −0.38 with 0.66, and −0.59 with 0.50. Following a previous upgrade exceeding one notch, the corresponding values are +0.18 actual, −0.01, +0.19, +0.33, and +0.50. Fractions 0.66–0.83 bracket important empirical drift patterns; 0.75 is an approximate descriptive midpoint rather than a precisely estimated universal coefficient.

Annual migration standard deviation is 0.82 notch for the actual ratings and 0.93 for unfiltered AR ratings in this subset. Filtered values are 0.78 at fractions 1 and 0.83, 0.68 at 0.66, and 0.60 at 0.50. The filter cannot perfectly match every statistic with a single pair of parameters. The source also calls the 1.25-notch threshold a minimum estimate because annual observation timing places the measured trigger on average roughly half a year before the actual within-year event.

Tables 8–9 aggregate to seven major categories. Excluding default migrations, the average major-category change probability is 9.5% for actual ratings, 20.0% for unfiltered AR ratings, 23.6% for six-year LDP ratings, and 33.0% for one-year DP ratings. These imply approximately 2.1, 2.5, and 3.5 times the actual frequency, respectively; the text describes the final comparison approximately as a factor of three. The filtered AR model with threshold 1.25 and fraction 0.66 gives 9.0%, close to actual.

Do not mix these frequencies with the earlier 23.4%, 49.0%, and 60.7% values: the latter use notch categories and include defaults. At the major BBB grade, no-change probability in Table 8 is 0.88 for actual ratings, 0.77 for AR, 0.74 for LDP, and 0.64 for DP. The major CCC group has large default probabilities—0.38 under actual classification and 0.51 under LDP/DP classification—showing that equal category counts do not imply identical constituent risk.

For a major rating $N$, equations (6.1)–(6.2) summarize movement as $\sum_{k=1}^{7}T(N,k)(k-N)$ and migration probability as $\sum_{k\ne N,\,k=1}^{7}T(N,k)$. Table 9 excludes default events. Its numbers show that the relevant transition probabilities are conditional on nondefault: the agency CCC row in Table 8 has about 15% nondefault movements and 38% defaults, whereas Table 9 reports 23.5% movement, close to $0.15/(1-0.38)$ after rounding. Simply dropping the default column of the all-event Table 8 matrix would not reproduce this result. Re-estimate or renormalize the nondefault rows using unrounded observations, and document this denominator choice; the equations do not explicitly state the change in conditioning, and printed rows are rounded.

## Limits and practical use

The most important identification assumption is that the AR model captures the agency's long-term assessment while its dynamic gap from actual ratings reflects migration policy. Private information, omitted variables, nonlinear effects, measurement error, changing standards, and cross-sectional re-ranking could also contribute. Comparable default-prediction performance helps justify the benchmark but does not prove that those alternatives are absent; detailed prediction-performance comparisons and several robustness tables are described as available on request rather than printed.

The late-period instability is substantive. In 2000–2001, the DP size coefficient changes from +0.47 to −0.24, while EBIT's coefficient rises from 3.78 to 8.36. Large firms were not uniformly protected in that episode. The authors exclude those years from the main coefficient estimation but include them in the behavioral comparison. Using the model as a contemporary default forecaster would require fresh estimation and validation, not copying its historical parameter vector.

The paper's useful implementation lesson is to keep three objects separate: a point-in-time probability score, a long-horizon credit assessment, and a published rating after decision smoothing. Transition matrices built from one are not automatically suitable for the others. A credit-risk engine can reproduce the threshold filter and test its implications, but should preserve its state variable and recent migration history rather than assume the rating alone is Markov. The work offers a parsimonious account of stability and drift; pricing, capital adequacy, and an optimal degree of smoothing remain additional research questions.

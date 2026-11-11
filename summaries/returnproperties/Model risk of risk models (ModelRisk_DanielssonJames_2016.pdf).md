# Model risk of risk models

**Authors:** Jon Danielsson, Kevin R. James, Marcela Valenzuela, and Ilknur Zer. **Publication:** Journal of Financial Stability 23 (2016), 79–91, DOI 10.1016/j.jfs.2016.02.002. **Source:** [ModelRisk_DanielssonJames_2016.pdf](../../Finance/ModelRisk_DanielssonJames_2016.pdf), 13 pages. Printed pages equal PDF page numbers plus 78. The full main paper, embedded Appendices A–B, tables, and critical figures were inspected. The separately advertised web appendix and individual forecast data at ModelsandRisk.org/modelrisk could not be recovered during preparation; implementation inputs absent from the PDF remain explicitly unresolved.

## Why this matters and the contribution

A bank's apparent risk can depend substantially on which accepted forecasting model it uses. The paper measures this disagreement by taking the ratio of the largest to the smallest forecast of the same risk quantity for the same asset and date. It applies the diagnostic to eleven models, to value at risk and expected shortfall, and then to two market-data-based systemic-risk measures. Disagreement becomes especially large during financial turmoil, precisely when decision makers may most want a single reliable risk number.

The contribution is measurement of model-choice sensitivity, not a new estimator that is proved closer to the unknown true risk. The authors deliberately avoid selecting a winning forecast model. They also distinguish disagreement among different systemic-risk concepts from disagreement within one concept when estimated using alternative statistical models. The latter is their target: hold the risk measure fixed and vary its estimator.

An important passage in Section 5 acknowledges that larger disagreement does not itself prove that forecast accuracy deteriorates in crises. A model can be accurate while its competitors are wrong; all models can agree and still be wrong. Risk ratios quantify a practically important source of uncertainty but are neither coverage tests nor confidence intervals for true risk. Their practical value is to expose sensitivity before a forecast is used for an expensive allocation or capital decision.

## The risk ratio and its mathematical limits

For asset $i$, forecast origin $t$, and positive risk forecasts $R_{i,t+1}^{(m)}$ from models $m=1,\ldots,M$, define

$$
RR_{i,t+1}=\frac{\max_mR_{i,t+1}^{(m)}}{\min_mR_{i,t+1}^{(m)}}.
$$

The baseline is one, and the ratio is unchanged if all forecasts are multiplied by the same positive portfolio value or unit conversion. Adding an extra model cannot reduce the ratio when the original forecasts are retained. This mathematical monotonicity does not mean candidate selection is innocuous: implausible models or numerical failures can inflate the statistic, and a narrow family of mutually similar models can suppress it.

The positivity condition matters. A near-zero denominator can generate a huge ratio without a correspondingly huge monetary spread. If forecasts cross zero, the simple ratio loses its interpretation as a factor of disagreement. The paper does not give a comprehensive zero-denominator or sign-crossing rule. A replication should store the minimum and maximum forecasts, their model identities, and their units alongside the ratio, and should make any excluded invalid cases explicit.

The statistic retains only the extremes. It does not say whether nine models cluster near the minimum or the maximum, nor does it separate parameter estimation error from differences in specification. The authors also compare standard deviation and absolute deviation of forecasts and report correlations above 80% among the three disagreement measures, with qualitatively similar results. Exact definitions and complete time series for these alternative diagnostics are not provided in the article.

Throughout this note, $\alpha$ denotes a small lower-return tail probability, such as 0.01. If $q_{\alpha,t}$ is a negative return quantile and portfolio value is $V$, then positive monetary VaR is $-Vq_{\alpha,t}$. Positive-loss expected shortfall is $-V E[r_{t+1}\mid r_{t+1}\leq q_{\alpha,t}]$ for a continuous law, or the corresponding quantile-integral definition with atoms. The source alternates between confidence probabilities such as 99% in its tables and lower-tail probabilities in formulas, and occasionally writes negative-return conditional expectations as “ES.” A consistent conversion is necessary before taking maxima and minima.

## Sample construction and forecast timing

The sample is built from the CRSP 1925 US Stock Database for January 1970–December 2012. It covers NYSE-, AMEX-, and NASDAQ-traded financial institutions with SIC codes 6000–6799: banking, insurance, real estate, and trading sectors. The authors collect daily prices, holding-period returns, and shares outstanding. A company must have more than 1,000 return observations, fewer than 30 consecutive days of missing returns, and belong to the largest 100 institutions by market capitalization at the beginning of a year. The resulting changing panel contains 439 institutions, not a fixed panel of 100 survivors.

Daily risk forecasts use a 1,000-day estimation window and a portfolio value of \$100. The reported forecast period begins in January 1974 after the initial history and ends in December 2012, subject to individual availability. Information through day $t$ is used to forecast day $t+1$. The source describes rolling estimates but does not fully document calendar treatment, return adjustments beyond CRSP holding-period returns, delisting-return incorporation, mergers, share-class aggregation, or the interpolation of missing observations. Those choices affect both membership and rare losses.

Illiquid histories caused fitting problems. The authors truncate the part of a stock's sample containing more than one week's worth of zero returns, rather than deleting individual zero observations or dropping the entire stock. The exact operational truncation boundary is not specified. They report similar qualitative results without truncation and when changing the weekly threshold, though untruncated histories produced more outlying forecasts. Rare nonlinear optimization failures or unstable estimates, often Student-$t$ GARCH, are omitted. The paper does not give a numerical rejection threshold or count of all excluded fits, preventing exact reproduction of this filter.

The highlighted institutions are JPMorgan, American Express, AIG, and Goldman Sachs. AIG is used rather than larger insurers with histories beginning only after 2000. System-level comparisons use the S&P 500, the Fama–French value-weighted financial-industry portfolio, and Fin100. Table 1 calls Fin100 a value-weighted portfolio of the largest 100 sample institutions with annual rebalancing. The surrounding prose confusingly calls its weights random while also tying them to beginning-of-year market capitalization. The later random-simplex bootstrap is a separate explicit experiment. A reconstruction should state whether it follows the Table 1 value-weighted definition rather than silently conflating these portfolios.

## Eleven candidate forecasting models

The five basic methods are historical simulation, EWMA, Gaussian GARCH, Student-$t$ GARCH, and unconditional EVT. Six hybrids apply either historical simulation or EVT to standardized residuals from Gaussian, Student-$t$, or skewed-$t$ GARCH fits. All should use the same asset, date, tail probability, horizon, and window when computing a given ratio.

Historical simulation takes a lower empirical return quantile. It retains observed nonnormality but gives equal weights to the window and does not explicitly model changing conditional scale. The empirical quantile interpolation convention and the fractional-tail convention for empirical ES are not specified. Such choices can matter when a 1,000-day window has only about ten observations in a 1% tail.

The EWMA recursion in Appendix A is

$$
\widehat\sigma_{t+1}^2=0.06r_t^2+0.94\widehat\sigma_t^2.
$$

Conditional normality then gives $\operatorname{VaR}_{1-\alpha,t+1}=-V\widehat\sigma_{t+1}\Phi^{-1}(\alpha)$ under a zero-mean convention. EWMA has no positive intercept and is the integrated-variance boundary of a GARCH(1,1) specification. The source does not state initialization within each rolling window. This can affect early fitted values and must be kept consistent across reruns.

The GARCH models use

$$
\widehat\sigma_{t+1}^2=\omega+a r_t^2+b\widehat\sigma_t^2.
$$

Gaussian or Student-$t$ likelihoods distinguish the two basic versions; the degrees of freedom are maximum-likelihood estimates. Positivity, persistence restrictions, mean treatment, starting values, and solver tolerances are not fully reported. If the Student-$t$ quantile is from a unit-scale $t_\nu$ law and $\sigma$ is intended to be conditional standard deviation, the standardized quantile is $\sqrt{(\nu-2)/\nu}\,t_\nu^{-1}(\alpha)$ for $\nu>2$. A reproduction must check its software parameterization instead of scaling twice or not at all.

The EVT method assumes a Pareto-type loss tail. For an explicit, consistent implementation notation, order positive adverse-tail magnitudes $x_{(1)}\geq\cdots\geq x_{(T)}$ and choose threshold $u=x_{(k+1)}$ below the largest $k$ losses. The Hill estimator and extrapolated loss quantile are

$$
\widehat\xi=\frac1k\sum_{j=1}^k\log\frac{x_{(j)}}u,
\qquad
\widehat v_\alpha=u\left(\frac{k}{T\alpha}\right)^{\widehat\xi}.
$$

The Pareto tail index is $\widehat\iota=1/\widehat\xi$, and the corresponding total tail expectation is

$$
\widehat{ES}_\alpha=\widehat v_\alpha\frac{\widehat\iota}{\widehat\iota-1},
\qquad\widehat\iota>1.
$$

These equations express the method in Appendix A with an unambiguous threshold convention. Its printed denominator is $x_{(q-1)}$ while summing $q$ ordered tail observations, an indexing convention that is not adequately defined and should not be copied mechanically. The article also omits the choice of tail count, threshold-selection method, and treatment of estimates with infinite tail mean. Those omissions are major replication gaps, particularly for ES. The Pareto formula is an approximation based on a fitted tail law, not an exact identity for all returns.

For hybrids, estimate a GARCH(1,1) filter, obtain standardized residuals, estimate their adverse quantile or tail expectation by HS or EVT, and restore the one-step location and scale. In return notation,

$$
q_{\alpha,t+1}^{r}=\widehat\mu+\widehat\sigma_{t+1}q_\alpha^{z},
\qquad\operatorname{VaR}_{1-\alpha,t+1}=-Vq_{\alpha,t+1}^{r}.
$$

The source's hybrid formula writes the location-scale expression as VaR without clarifying the sign. Treating it as a return quantile before converting to loss avoids that ambiguity. Fitting a Student or skewed-Student likelihood affects the estimated filter even when the final innovation quantile is subsequently empirical. The exact skewed-$t$ implementation, parameter restrictions, and residual resampling details are not fully stated in Appendix A.

## Daily VaR disagreement and the importance of aggregation

Table 1 reports episode maxima, while its last row reports full-period averages. Figure 1 is different again: each institution's maximum daily ratio within a year, summarized across institutions. These statistics should not be presented as interchangeable typical-day readings. The introduction reports an average maximum 99% VaR ratio of 9.23 and a single extreme of 55.32 during 1987. Section 3 also says average model risk is about four, but discusses it alongside the annual-maxima figure. Given that mismatch of prose and caption, the explicit Table 1 averages are the clearest basis for quantitative typical-day statements.

For the portfolios and four highlighted stocks, the main numerical results are:

| Series | Full-period mean 99% VaR ratio | Maximum during 1987 crash | Maximum during 2007–2009 episode |
|---|---:|---:|---:|
| S&P 500 | 1.71 | 10.39 | 5.22 |
| Fama–French financial portfolio | 1.78 | 10.10 | 5.26 |
| Fin100 | 1.82 | 10.10 | 6.39 |
| JPMorgan | 1.85 | 11.01 | 6.90 |
| American Express | 1.85 | 6.37 | 5.44 |
| AIG | 2.09 | 3.71 | 13.89 |
| Goldman Sachs | 2.16 | unavailable | 5.79 |

All figures are unit-free multiples, not percentages or loss amounts. A ratio of 10.39 means the largest forecast is 10.39 times the smallest on the date attaining the episode maximum. It does not mean the forecast error is 939% or that the largest model is wrong.

The event windows are May–October 1977, January–July 1980, July 1981–November 1982, October 1987–January 1988, July 1990–March 1991, August–November 1998, March–November 2001, and December 2007–June 2009. The paper labels the 1977 episode a crash and mixes these market-event windows with recession dates. Exact endpoint conventions matter for maxima and must follow the stated months.

Figure 2 plots only end-of-quarter extrema for JPMorgan to reduce clutter. It shows models exchanging places: Student-$t$ and EVT often give larger readings, Gaussian methods often smaller, but HS and hybrids can occupy either end. A quarterly plot cannot identify the dates or model identities of every daily maximum. The authors report that no one model consistently generates all extremes.

## Expected shortfall and overlapping observations

The study contrasts daily 99% VaR with 97.5% ES under two historical regulatory-proposal-inspired specifications. One uses ordinary nonoverlapping daily inputs; another uses overlapping ten-day observations, formed from days 1–10, 2–11, and so forth. This is a comparison of estimation designs, not a present-day statement of capital rules. The wording “daily ES with 10-day overlapping estimation windows” leaves some implementation details unclear, including whether a 1,000-day window denotes raw days or 1,000 aggregated observations and whether a scaling conversion follows fitting.

Full-period mean risk ratios are:

| Series | 99% daily VaR | 97.5% ES, overlapping inputs | 97.5% ES, nonoverlapping inputs |
|---|---:|---:|---:|
| S&P 500 | 1.71 | 2.78 | 1.76 |
| Financial portfolio | 1.78 | 3.00 | 1.83 |
| Fin100 | 1.82 | 2.93 | 1.87 |
| JPMorgan | 1.85 | 2.52 | 1.91 |
| American Express | 1.85 | 2.55 | 1.88 |
| AIG | 2.09 | 2.85 | 2.19 |
| Goldman Sachs | 2.16 | 2.79 | 2.14 |

Switching the measure alone does not eliminate disagreement. For example, nonoverlapping S&P 500 ES reaches 9.03 in 1987 versus VaR's 10.39. Overlapping-input Fin100 ES reaches 53.84 in the same episode versus 9.13 for nonoverlapping ES. During 2007–2009, overlapping-input JPMorgan ES reaches 24.12 versus 6.07 without overlap; AIG reaches 22.66 versus 9.59.

Overlapping aggregation repeats the contribution of a large daily shock in adjacent observations and induces serial dependence. Different fitting methods react differently to that dependence. This is the authors' explanation for increased dispersion, not an experimentally isolated causal decomposition. The table changes both distributional inputs and, relative to VaR, probability level and risk functional. It should not be described as proving that coherent ES is intrinsically more model-sensitive than VaR at matched settings.

## Robustness and the random-portfolio experiment

Table 2 removes one model at a time for the S&P 500. Full-period mean ratios range from 1.61 after excluding EWMA to 1.71 with the complete set. The 1987 maximum is 10.39 with all models, 9.62 without HS, and 10.08 without normal-filter EVT. The 2008 maximum is 5.22 with all models, 5.10 without HS, and 4.55 without Student-$t$ GARCH. Thus no single exclusion removes large crisis disagreement. This does not establish robustness to excluding an entire related family or applying a different admissibility screen. The source counts 2,035 model subsets of sizes two through ten but does not report all of them in the article.

To compare crisis with pre-crisis periods, Section 3.3 uses random portfolio weights rather than resampling time. At each year's beginning, select the largest 100 institutions. Draw weights from a unit simplex, form a portfolio return history, fit the eleven models with 1,000-day windows, and compute a daily ratio. Repeat the portfolio construction and forecast calculation 1,000 times. For each trial, average its daily ratios within an event and within the preceding twelve months. For the December 2007–June 2009 event, the comparison period is December 2006–November 2007.

The source says weights are drawn from a unit simplex but does not explicitly specify the probability law or random seed. Uniform simplex sampling is a possible choice, not a disclosed Dirichlet parameterization. The treatment of weights between annual reselections—constant target weights versus buy-and-hold drift—is also not fully explained. These details affect the generated portfolio paths and should be fixed in a reconstruction.

Figure 3 displays first and third quartiles of the trial results, with box-plot features, despite calling them confidence intervals. Interquartile ranges are not conventional 95% sampling confidence intervals for a population effect. The authors report higher ratios in every crisis window except the 1990 recession, and statistically significant differences for 1987, LTCM, and 2008. Exact test statistics, p-values, and the confidence-interval construction are not reported in the main paper. Randomizing weights assesses variation across portfolios on the observed historical path; it does not create independent crisis realizations or identify the causal effect of financial stress.

They also report qualitatively similar stationary/block-bootstrap results, without all block-length and dependence choices. The broader conclusion—that disagreement rises during the selected stress events—is supported across their specifications. Formal generalization to an unseen crisis needs more than the number of randomized portfolios.

## Systemic-risk quantities and conditional-event definitions

Let $r_i$ be an institution's return and $r_S$ the system return. The source classifies measures by whether they describe the institution conditional on the system, or the system conditional on the institution, and whether the statistic is a conditional mean or quantile. In consistent return notation,

$$
MES_i^{r}=E[r_i\mid r_S\leq q_{S,\alpha}],
$$

while a lower-tail CoVaR threshold $c_{S\mid i,\alpha}$ solves

$$
P(r_S\leq c_{S\mid i,\alpha}\mid r_i\leq q_{i,\alpha})=\alpha.
$$

Positive-loss MES and CoVaR negate these quantities and apply the required monetary scaling. CoVaR is a threshold, not a probability equal to $\alpha$; the source's Eq. (3) compresses that distinction. Conditioning on an institution's return being below its quantile is also a different event from conditioning on equality to that quantile, as in the original quantile-regression formulation. The article argues their empirical behavior is similar based on prior work; that is not a mathematical identity or a general “without loss of generality” substitution.

With a continuous institutional marginal, the tail-event version satisfies

$$
P(r_S\leq c,\ r_i\leq q_{i,\alpha})=\alpha^2.
$$

This follows by multiplying the conditional probability by $P(r_i\leq q_{i,\alpha})=\alpha$; it does not assume independence between institution and system. One numerically integrates a fitted bivariate density and solves for $c$. The sign of the threshold must remain negative in return space even when its reported loss magnitude is positive.

MES is evaluated at 95% confidence with the S&P 500 as the system and the eleven alternative models generating system-tail thresholds. Figure 4 shows end-of-quarter ratios generally closer to one than the 99% VaR ratios, with stress spikes. A less extreme 5% event contains more observations, but a smaller ratio is not itself proof of more accurate MES. The source does not give a complete model-by-model conditional-mean integration or dependence-estimation recipe for all eleven MES versions.

The CoVaR experiment uses the Fama–French value-weighted financial-industry portfolio as the system and a 99% level. It excludes historical-simulation-based methods because a 1% conditioning event followed by a 1% conditional quantile leaves approximately one expected joint-tail observation per 10,000 observations. That is a data-scarcity illustration, not a sufficient sample-size guarantee. Removing candidates mechanically weakens possible disagreement relative to the full set.

For the remaining joint models the authors use dynamic conditional correlation, and an extreme-value copula for the EVT specification, then solve the joint-tail equation numerically. The article does not name every copula family or give all DCC orders, parameter restrictions, innovation dependence conventions, numerical integration settings, and tail thresholds. Figure 5 lists seven candidate families, whereas the surrounding discussion also mentions a skewed-$t$ GARCH approach. The exact implemented set cannot be settled from that prose alone. CoVaR ratios are reported as larger on average than VaR/MES ratios and particularly elevated after 2008, but the graph does not provide a complete numerical daily series.

## The separate quantile-regression appendix

Appendix B studies a different CoVaR implementation using weekly growth in market-valued total assets. Daily market values are collapsed to weekly frequency and merged with quarterly CRSP/Compustat balance sheets. The system return is an average weighted by lagged market asset values. The authors filter leverage and book-to-market ratios using the stated zero and 100 bounds, but the wording does not fully resolve whether both variables receive both bounds. Release-date lags and the exact market-asset construction are not provided in the article.

At a fixed lower quantile, estimate

$$
Q_\alpha(r_{i,t}\mid M_{t-1})=a_i+\gamma_i'M_{t-1},
$$

$$
Q_\alpha(r_{S,t}\mid r_{i,t},M_{t-1})
=a_{S\mid i}+\beta_{S\mid i}r_{i,t}+\gamma_{S\mid i}'M_{t-1}.
$$

Quantile regression minimizes the sum of check losses $\rho_\alpha(u)=u(\alpha-\mathbf1_{u<0})$. Plug the institution's fitted quantile into the second equation to obtain CoVaR, and compare with the institution's median state:

$$
\Delta CoVaR_{i,t}^{r}
=\widehat\beta_{S\mid i}
\left[q_{i,t}(\alpha)-q_{i,t}(0.5)\right].
$$

The seven lagged state variables are VIX; three-month repo minus Treasury-bill spread; change in the three-month bill rate; change in the BAA corporate minus ten-year Treasury spread; change in the ten-year minus three-month Treasury slope; S&P 500 return; and the Fama–French real-estate-industry return. The repo series is available from Bloomberg only from 1991. The article does not specify the complete common-sample start or a pre-1991 substitute, so this appendix should not automatically inherit the 1974–2012 daily forecast sample.

The authors find time-series correlations between VaR and $\Delta CoVaR$ mostly above 99%. If the median quantile is near zero and $\beta$ is fixed, their near-proportional relation is partly algebraic. It does not prove that the two measures have the same cross-sectional ranking, since institutions have different slopes and conditional distributions.

For parameter uncertainty, they reshuffle regression residuals and refit 1,000 times, plotting 99% regions for the 2006Q4 point estimates of Goldman Sachs, MetLife, SunTrust, and American Express at a 1% tail level. Figure B.1 shows broad overlap. Goldman Sachs has the largest plotted systemic contribution at its point estimate, but the paper cautions against a confident ranking. Residual resampling dependence treatment, joint error resampling across equations, and the construction of the plotted ellipses are not fully documented. Overlapping individual regions are suggestive of uncertainty, not a substitute for a direct joint test of pairwise ranking differences.

## Interpretation and remaining replication work

The paper's evidence supports a narrow but consequential conclusion: plausible modeling choices can give sharply different readings of the same specified risk measure, and the difference is often largest in the observed stress episodes. A coherent measure such as ES does not solve estimator disagreement. Conditional systemic measures inherit marginal-tail uncertainty and add dependence and conditioning choices.

The proposed explanations—few crisis observations, structural change, and risk generated by interacting institutions—are plausible mechanisms discussed by the authors. The empirical design does not identify their separate causal contributions or prove that risk ratios predict the next crisis. Nor does it evaluate whether a high-ratio warning improves a particular portfolio or capital decision out of sample. That distinction is stated explicitly in Section 5 and should govern use of the results.

For a new implementation, retain all eleven forecast series and diagnostics, define the candidate admissibility rules before observing extremes, record failures, and separate model dispersion from parameter uncertainty. Exact matching to the article still requires the unavailable forecast archive and missing choices about tail thresholds, signs and scaling, return cleaning, overlap construction, joint density estimation, and bootstrap details. The main article is sufficient to reconstruct the comparison framework and its headline tables, but not every numerical estimator. Reporting that boundary is preferable to presenting an arbitrary software default as the authors' method.

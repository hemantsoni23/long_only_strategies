# Have Individual Stocks Become More Volatile? An Empirical Exploration of Idiosyncratic Risk

**Authors:** John Y. Campbell, Martin Lettau, Burton G. Malkiel, and Yexiao Xu. **Publication:** *The Journal of Finance* 56(1), February 2001, pp. 1–43. **Source:** [Volatility_CampbellLettauMalkielXu_2001.pdf](../../Finance/Volatility_CampbellLettauMalkielXu_2001.pdf). The local PDF has 44 pages, with the final page effectively blank; page references below are the printed article pages and coincide with PDF pages.

## Why this matters and what the paper contributes

A stable stock index can conceal a changing investment opportunity set. If individual stocks become riskier while their comovement declines, a diversified index need not become more volatile. Concentrated investors, stock selectors, and risk models calibrated to individual securities nevertheless face substantially different risks. Campbell and coauthors document this distinction in U.S. stocks from July 1962 through December 1997. Firm-specific return variance rises substantially, while neither market nor average industry variance has a comparably significant trend. Pairwise correlations and market-model explanatory power fall, and substantially more randomly chosen stocks are needed to attain a given diversification threshold.

The methodological contribution is a decomposition of the weighted average stock variance into market, industry, and firm components that does not require estimating thousands of individual betas. Covariances do not disappear security by security; they cancel after aggregation with consistent portfolio weights. This makes a long historical panel feasible despite entry, exit, and changing membership. A second contribution is to treat within-month sums of squared daily returns as observed volatility measures and study their trends, lead–lag relationships, and macroeconomic associations using conventional time-series methods.

The paper is primarily a statistical description, not an identified economic explanation of the increase or a trading-strategy backtest. Its causal discussion is explicitly tentative. The historical trend is a result for this sample; it is not an extrapolation that idiosyncratic volatility must keep increasing indefinitely. The decomposition and replication design remain useful independently of whether the trend persists in other periods.

## The decomposition and its exact scope

Let $R_{ji,t}$ denote the simple excess return of firm $j$ in industry $i$, $w_{ji,t}$ its within-industry weight, and $w_{i,t}$ the industry's market weight. Weights sum to one at each aggregation level. Use the same weights throughout:

$$
R_{i,t}=\sum_{j\in i}w_{ji,t}R_{ji,t},\qquad
R_{m,t}=\sum_iw_{i,t}R_{i,t}.
$$

Define industry and firm residual returns by subtraction, not regression:

$$
e_{i,t}=R_{i,t}-R_{m,t},\qquad
\eta_{ji,t}=R_{ji,t}-R_{i,t}.
$$

Then $\sum_iw_i e_i=0$ and $\sum_{j\in i}w_{ji}\eta_{ji}=0$. With weights treated as fixed over the measurement interval, expanding squared returns or variances and aggregating cancels all cross terms. Equations (9), (13), and (14) yield

$$
\sum_iw_i\sum_{j\in i}w_{ji}\operatorname{Var}(R_{ji})
=\operatorname{Var}(R_m)
+\sum_iw_i\operatorname{Var}(e_i)
+\sum_iw_i\sum_{j\in i}w_{ji}\operatorname{Var}(\eta_{ji}).
$$

Call these three right-hand components MKT, IND, and FIRM. Their sum is the variance of a typical stock when stocks are sampled with probabilities equal to their market-capitalization weights. It is **not** the variance of a portfolio holding all stocks: that portfolio's variance is MKT. Nor is FIRM an estimate of the risk of a particular stock after controlling for every relevant factor. Sector assignment and the imposed unit exposures matter.

For an individual industry, $\operatorname{Cov}(R_m,e_i)$ generally is nonzero, and for an individual firm $\operatorname{Cov}(R_i,\eta_{ji})$ generally is nonzero. Regressing each stock on a market factor and summing residual variances would produce a different statistic. The cancellation also fails if the market index, industry index, and firm averaging use inconsistent weights or universes. A useful numerical check is to reconstruct both sides of the weighted squared-return identity each day before monthly aggregation.

The authors compare their construction with a hierarchical CAPM-style representation $R_i=\beta_{im}R_m+\tilde e_i$ and $R_{ji}=\beta_{ji}R_i+\tilde\eta_{ji}$. Their Eq. (15) shows that IND includes the average orthogonal industry residual variance plus market variance multiplied by cross-sectional dispersion of industry betas. Thus the word “industry” does not imply complete separation from market volatility.

There is a mathematical qualification to the printed Eq. (16), which expresses FIRM using products of aggregate beta dispersions and aggregate variances. Under the stated hierarchical orthogonality assumptions, a direct expansion gives the more general expression

$$
\mathrm{FIRM}=\widetilde{\mathrm{FIRM}}
+\sum_iw_i C_i\left[\beta_{im}^{2}\operatorname{Var}(R_m)+\operatorname{Var}(\tilde e_i)\right],\qquad
C_i=\sum_{j\in i}w_{ji}(\beta_{ji}-1)^2.
$$

This expression is an algebraic clarification in this note. Replacing the last weighted sum by the product of average $C_i$ and average industry residual variance needs an additional restriction. Also, overall dispersion of firm market betas includes between-industry dispersion, which is already part of IND. The beta-free empirical decomposition does not rely on the printed shortcut; implement it directly rather than using Eq. (16) as a computational identity.

## Data, weights, and monthly measurement

The source panel is CRSP firms listed on NYSE, AMEX, and Nasdaq, July 1962–December 1997. The main text reports 2,047 firms initially and 8,927 at the end. Industries follow the 48-industry SIC classification of Fama and French (1997), plus a 49th category for unclassified firms. Exact SIC mappings are delegated to that source. The panel changes through time; it is not a balanced sample of firms surviving until 1997.

For month $t$, use firm market capitalizations from $t-1$, form within-industry and industry weights, and keep them fixed within month $t$. Build the market from the same firm panel instead of substituting the official CRSP market index. The correlation between the paper's constructed market and the CRSP value-weighted index is 0.997, but even that small difference would prevent exact algebraic cancellation. Convert the monthly 30-day Treasury-bill return into a daily risk-free return by dividing by the month's number of trading days; subtract this from each daily stock return.

Let $s$ index daily observations within month $t$, and let $\mu_m$ be the full-sample mean market excess return. The implemented measures in Eqs. (17)–(22) are

$$
\mathrm{MKT}_t=\sum_{s\in t}(R_{m,s}-\mu_m)^2,
$$

$$
\mathrm{IND}_t=\sum_iw_{i,t}\sum_{s\in t}(R_{i,s}-R_{m,s})^2,
$$

$$
\mathrm{FIRM}_t=\sum_iw_{i,t}\sum_{j\in i}w_{ji,t}\sum_{s\in t}(R_{ji,s}-R_{i,s})^2.
$$

There is no division by the number of daily observations: these are sums intended to estimate monthly variance. Annualize by multiplying by 12, not by taking a square root. The descriptive tables further multiply annualized variances and their time-series standard deviations by 100. Consequently, a table mean of 6.436 means annual variance 0.06436; it is not a stock volatility of 6.436%. Its square root is approximately 25.37% annual standard deviation for the firm-specific component.

Only the market return is explicitly demeaned in these formulas. Residual series use raw squared deviations from contemporaneous portfolios. The exact finite-sample squared-return identity therefore corresponds to centering each firm around the same market mean, not separately subtracting each stock's estimated expected return. Interpreting these sums as conditional variances uses the usual approximation that daily drift terms are small. The authors report that allowing a time-varying market mean barely changes the results.

Two-sided smoothing could improve variance estimation but would obscure lead–lag analysis. The paper therefore retains within-period realized measures for formal analysis; moving averages in some figures are visual aids. To study quarterly or annual relations, rebuild or aggregate the variance measures at the required frequency, with appropriate annualization, rather than using the final month's observation as the quarter's volatility.

Several low-level CRSP choices are not supplied: exact share-code filters, treatment of delisting returns, duplicate securities of the same issuer, missing or nontrading prices, changes in SIC assignment, and within-month entry or exit conventions. These are genuine replication inputs, not details that can be assumed from the exchange names. The correlation exercise has additional explicit filters described below; the paper does not clearly say to apply those same filters to every baseline variance series.

## Trend tests, crash treatment, and principal results

October 1987 is exceptional: annualized market variance reaches 0.672. The authors show raw results and a sensitivity version replacing the October observation by the second-largest observation in the corresponding series, separately for MKT, IND, and FIRM. This is neither removing October nor capping all large observations. It is an ex post robustness transformation and should not be used as a real-time filtering rule.

Table III reports these mean annual variances, converted here into decimal-return-squared units:

| Construction | MKT | IND | FIRM |
|---|---:|---:|---:|
| Daily returns, raw | 0.01542 | 0.01032 | 0.06436 |
| Daily returns, crash downweighted | 0.01409 | 0.01027 | 0.06383 |
| Weekly returns, raw | 0.01897 | 0.01218 | 0.05842 |
| Monthly returns, raw | Not reported | 0.01269 | 0.05039 |
| Daily returns, equal weighting, raw | 0.01211 | 0.01251 | 0.33903 |

The raw daily components sum to 0.09010. The square root, about 30.02%, is the standard deviation corresponding to average stock variance; it is not the average of the individual stock standard deviations. The difference between value-weighted and equal-weighted FIRM is large: 0.33903 is about 5.27 times 0.06436. Small listed firms have a disproportionate influence on equal-weighted risk.

Serial dependence requires care in trend inference. The authors apply augmented Dickey–Fuller tests with lag selection and reject unit roots in the three main volatility series. They then use Vogelsang's PS1 procedure, robust to serial correlation, to test a deterministic trend. Eq. (23) describes a volatility process with an intercept, linear time trend, lagged volatility, and serially dependent disturbances. The table distinguishes the simple OLS time-trend coefficient from the PS statistic and the confidence interval associated with the trend parameter in that testing framework. These are not interchangeable statistics.

The raw daily FIRM trend coefficient is 0.965 in the table's $10^5$ scaling; the crash-adjusted value is 0.939. The corresponding reported 90% intervals are [0.55, 1.47] and [0.49, 1.42]. Market and industry intervals include zero. The authors' fitted-trend interpretation is that firm-level variance more than doubles, while market and industry variance rise by only about one-third and without significant trends. FIRM's fitted share of total variance rises from about 65% to 76%; MKT falls from 20% to 14%, and IND from 15% to 10%.

The units of the printed trend rows need verification against original calculations. Means are explicitly annualized, but interpreting $0.939\times10^{-5}$ directly as an annual-variance increment per month would imply an increase of only about 0.004 over 426 months, inconsistent with the described doubling. Applying the factor of 12 to a monthly-variance slope gives about 0.048, which is compatible with the narrative. This suggests unannualized slope reporting, but the caption does not resolve it. Preserve the displayed coefficients and reported qualitative conclusion; do not silently convert the trend into an economic growth rate without checking this convention.

Daily serial correlation could mechanically affect sums of squared returns. Recomputing with weekly and monthly returns reduces average FIRM but leaves a significant positive trend. The printed raw FIRM trend slopes are 0.737 and 0.720, with reported 90% intervals [0.13, 0.69] and [0.28, 1.28] under the PS framework. The different levels are consistent with negatively autocorrelated firm-specific daily returns, while market and industry returns tend to be positively autocorrelated. Changing sampling frequency is a robustness test of the historical finding, not proof that the daily statistic is an unbiased integrated-variance estimator.

To address the expansion in listed firms, the authors repeat calculations on a fixed number of the largest firms each month. The main text says 2,047, while Table III's caption says 2,026; a faithful replication must resolve or test both. The large-firm FIRM raw mean is 0.05877 and its trend slope is 0.524 in displayed units, smaller than the full-sample slope. The raw 90% interval excludes zero, [0.03, 1.15], but the crash-adjusted interval [-0.02, 1.11] does not at that level. Thus the table supports a positive point estimate among large firms more strongly than an unconditional claim of significance under every variant. New listings and small firms contribute, but are not the entire explanation.

## Industry-level checks

The beta-free cancellation works after averaging across industries. For a particular industry, Section II.C instead estimates its market beta by OLS on full-sample monthly excess returns and uses $\tilde e_i=R_i-\beta_{im}R_m$. Firm residuals remain $R_{ji}-R_i$. The resulting industry-specific decomposition is

$$
\sum_{j\in i}w_{ji}\operatorname{Var}(R_{ji})
=\beta_{im}^{2}\operatorname{Var}(R_m)
+\operatorname{Var}(\tilde e_i)
+\sum_{j\in i}w_{ji}\operatorname{Var}(\eta_{ji}).
$$

This requires only industry betas, not individual firm betas, but assumes those estimated betas are constant over the sample. In a predictive application their full-sample estimation would be unavailable in real time.

Table IV lists the ten largest industries by average market capitalization. Petroleum/gas accounts for about 11.0%, financial services 7.8%, and utilities 7.4%. Utilities and telecommunications have comparatively low market betas, 0.66 and 0.70. Mean industry-specific variance differs markedly across industries, while firm variance is less dispersed. For computers, annual IND and FIRM means are 0.01654 and 0.06123; for utilities they are 0.00311 and 0.04032.

Six of the ten largest industries and 24 of all 49 have significant positive firm-variance trends; none has a significant negative firm trend. The largest increases among major sectors occur in telecommunications, computers, and retail. Industry-variance trends are less uniform: 14 positive and seven negative significant trends across all industries. These are multiple descriptive tests, and the paper does not provide a multiple-testing-adjusted discovery claim.

## Correlations and the number of stocks needed for diversification

Section III computes all pairwise stock correlations and averages them equally. At each month, daily correlations use the preceding 12 months of daily returns; monthly correlations use the preceding 60 months of monthly returns. The latter require a complete five-year history. The daily sample ranges roughly from 1,500 to 8,000 stocks and the monthly sample from 1,000 to 4,500. Stocks with a daily return above 200%, or zero returns on at least 75% of days in the last 12 months, are excluded to limit data errors and severe illiquidity. Figure 5's caption requires complete window histories, while the text allows shortened daily windows at the dataset's beginning; this initial-period convention should be recorded explicitly.

Average monthly-data correlations decline from approximately 0.28 in the early 1960s to 0.08 in 1997. Daily-data correlations fall from about 0.12 to roughly 0.02–0.04 during the 1990s. The horizons differ as well as the return frequencies: daily estimates give more weight to recent conditions. Market-model $R^2$, estimated stock by stock over the same windows using the NYSE/AMEX/Nasdaq composite market, exhibits a similar decline. Correlation and $R^2$ are not identical statistics in a heterogeneous market; the similar figures are an empirical pattern.

For Figure 6, randomly group eligible stocks into equal-weighted portfolios without replacement. Compute each portfolio's standard deviation from daily returns within each calendar year, annualize it, and take a simple average across portfolios. Subtract the annualized standard deviation of the equal-weighted all-stock index. This is a **difference of standard deviations**, not tracking-error volatility, variance in excess of the market, or a percentage reduction in risk.

The time-series panel uses portfolios of 2, 5, 20, and 50 stocks. A typical two-stock portfolio's excess annual standard deviation rises from about 25 percentage points in the early sample to a peak near 50 points in the early 1990s. The lower panel averages over 1963–1973, 1974–1985, and 1986–1997. In the first two periods, approximately 20 stocks reduce excess standard deviation to about five percentage points; in the last period, almost 50 are needed. This supports a historical change in random-stock diversification requirements, not a universal rule that every 50-stock portfolio is diversified. The source does not give a random seed, number of repeated random partitions, or a Monte Carlo uncertainty band.

## Comovement, forecasting, and macroeconomic timing

The three components move together strongly after the crash adjustment. Table V reports correlations MKT–IND 0.645, MKT–FIRM 0.708, and IND–FIRM 0.705; after linear detrending these become 0.641, 0.800, and 0.767. Although FIRM's level dominates typical-stock variance, MKT is highly variable relative to its own mean.

Table VI's actual subperiod mean shares should be distinguished from fitted trend endpoints: full-sample MKT/IND/FIRM shares are 0.160/0.116/0.724, July 1962–June 1971 shares are 0.162/0.126/0.712, and January 1988–December 1997 shares are 0.134/0.097/0.769. The adjacent prose calls these early and late observations “12 months,” but the table explicitly uses multiyear periods. Use the table dates for reconstruction.

The variance decomposition of the detrended *total variance series* is another level of analysis. Its six contributions are variances of MKT, IND, FIRM, and twice their three covariances, all divided by the variance of their sum. The values are 0.149, 0.027, 0.282, 0.081 for MKT–IND, 0.328 for MKT–FIRM, and 0.133 for IND–FIRM. They sum to one. A covariance entry already includes the factor of two; adding both symmetric entries would double count it. The paper also estimates conditional means by regressing each detrended component on four lags of all three, then decomposes the time variation of those fitted means.

Granger-causality regressions use detrended, crash-adjusted measures and AIC-selected lag lengths. In the trivariate system, lagged MKT predicts IND and FIRM with reported $p$-values 0.027 and 0.004. FIRM predicts MKT at 0.016 but not IND at conventional levels, 0.108; IND does not significantly predict the other two. These are predictive lead–lag findings conditional on the specified system, not causal effects of market risk on firms. Lag search and a single historical sample limit their stability.

All three measures are countercyclical. An expansion indicator has contemporaneous correlations -0.420, -0.472, and -0.508 with MKT, IND, and FIRM. Average market variance is roughly three times higher in recessions than expansions; industry and firm variance are roughly twice as high. Quarterly volatility also tends to lead lower GDP growth. The source studies both raw levels and innovations from fitted volatility dynamics; their correlations should not be conflated.

Table IX regresses quarterly GDP growth on one-quarter-lagged GDP growth, CRSP value-weighted return, and selected volatility components. Volatility is constructed at quarterly frequency, crash-adjusted, and linearly detrended. The baseline $R^2$ is 0.143; adding MKT, IND, or FIRM alone raises it to 0.190, 0.213, or 0.206. The respective volatility coefficients and robust $t$-statistics are -0.701 (-2.383), -1.841 (-2.432), and -0.477 (-2.999). With all three included, $R^2=0.222$ and their joint-significance $p$-value is 0.006, although no individual volatility coefficient is then significant. Strong comovement makes this loss of individual precision unsurprising.

These printed coefficients must be interpreted using the original GDP-growth and variance scaling; the table does not fully document every transformation needed for an independent economic-unit conversion. The paper uses Newey–West inference with automatic bandwidth selection. It does not report a rolling or expanding out-of-sample GDP forecast experiment. Full-sample detrending, crash replacement, and revised macroeconomic data mean these explanatory regressions are not deployable real-time forecast records.

Industry-output analysis uses annual BLS output for 1972–1997, with 47 industries because miscellaneous manufacturing and miscellaneous firms lack output data. It first residualizes industry output growth on aggregate industrial-output growth, then pools industries with common coefficients. Regressors include lagged output residuals, industry return, aggregate MKT/IND/FIRM, and the industry's own IND/FIRM. Industry-specific FIRM has coefficient -0.158 and $t=-2.345$, but explanatory power is only 1.2%. Residualizing on contemporaneous aggregate output is unavailable at the prior forecast date. A second pooled regression therefore uses raw industry growth, lagged industry and aggregate output growth, and the remaining lagged predictors. Own-industry FIRM has coefficient -0.190, $t=-2.559$, and $R^2=6.3%$. Details of dependence corrections for the stacked cross-section are not sufficient to reproduce every reported standard error from the PDF alone.

## Mechanisms, limits, and a disciplined replication

The paper discusses focused firms replacing conglomerates, earlier public listings, stock-option incentives, institutional ownership, and changing discount-rate shocks. These are possible explanations, not jointly estimated mechanisms. Breaking a conglomerate into separately listed firms can expose risks previously diversified inside one security. Earlier listings can raise measured firm risk, especially under equal weighting. Rising market-valued leverage is not a satisfactory explanation for the late-sample trend because the 1990s bull market reduced that leverage.

Faster information dissemination is also not automatically an explanation. With constant discount rates, earlier revelation of future cash flows can increase dispersion of price levels while reducing return volatility, because news arrives when distant cash flows are more heavily discounted. The authors therefore resist treating either technology or derivatives trading as an established cause. They do not identify cash-flow and discount-rate news separately in this paper.

A reproducible implementation should save the monthly firm universe, industry assignments, lagged capitalizations, daily portfolio returns, residuals, and all three unannualized measures before any smoothing or crash adjustment. Verify the daily weighted decomposition, annualization, and table scales. Reproduce value-weighted means before adding equal-weighted and fixed-count sensitivity samples. Implement the trend inference from the cited Vogelsang procedure rather than substituting ordinary OLS standard errors. Separately implement the rolling correlation windows, random-portfolio experiment, and quarterly macro regressions; each has different selection and timing conventions.

The main evidence is robust to return frequency, weighting, and some universe changes, but it remains exposed to historical data conventions, small-stock microstructure effects, industry classification, and retrospective transformations. The practical lesson is to monitor individual-security risk and comovement separately: stable aggregate volatility can coexist with materially greater concentration risk. The paper supplies a transparent diagnostic and a substantial historical finding; it does not supply an optimized covariance estimator, a causal model of rising idiosyncratic risk, or a validated trading rule.

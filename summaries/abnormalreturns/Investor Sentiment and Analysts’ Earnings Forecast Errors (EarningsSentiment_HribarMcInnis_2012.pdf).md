# Investor Sentiment and Analysts’ Earnings Forecast Errors

Paul Hribar and John McInnis, *Management Science* 58(2), February 2012, 293–307, doi:10.1287/mnsc.1110.1356. [Source PDF](../../Finance/EarningsSentiment_HribarMcInnis_2012.pdf). Printed-page references below correspond to PDF page plus 292. The complete 15-page supplied article, including all footnotes and references, was read. There is no separate appendix in the file.

## Why this matters

Sentiment can predict a return spread without revealing why the spread exists. It could proxy for changing required returns, for limits to arbitrage, or for mistaken expectations of future cash flows. Hribar and McInnis bring earnings expectations directly into the analysis. They find that high sentiment is associated with greater relative optimism in analysts' forecasts for firms that are harder to value. Ex post forecast errors then absorb part of the relationship between sentiment and subsequent returns on portfolios that buy uncertain firms and short more certain firms.

For investment research, the useful contribution is a diagnostic method: measure whether an apparent return anomaly aligns with later fundamental disappointments. The paper is not an earnings-forecasting strategy in which realized forecast errors are known at formation. Its central regressions use future earnings to explain contemporaneous return realizations over the year. Treating those errors as tradeable predictors would introduce look-ahead bias. The results instead inform how one might investigate sentiment-sensitive valuation assumptions and distinguish earnings-expectation errors from a purely price-based story.

The novelty lies in portfolio-level tests connecting aggregate sentiment, cross-sectional forecast-error differences, and characteristic-portfolio returns. Prior work had already documented analyst optimism and sentiment-dependent returns. The article adds a direct measurement bridge, considers both annual EPS and long-term growth expectations, and examines whether strategic analyst incentives could explain the association. It offers observational evidence for an expectations mechanism, not a structural proof of investor irrationality or a causal mediation estimate.

## Data universe and characteristic portfolios

The authors collect monthly I/B/E/S summary forecasts, actual earnings, and announcement dates. Accounting data come from Compustat and stock data from CRSP. The data section describes collection from August 1983 through December 2006; the main annual-EPS tests use August 1983–December 2005, giving 269 months. Long-term-growth analyses stop in December 2004 to allow future earnings to be observed. The final sample is described as 646,046 firm-months. Average monthly coverage rises from 839 firms in the first three years to 3,074 in the last three (pp. 295–296).

This is an analyst-covered sample, not the entire listed market. The article does not present a complete sequential attrition table, all CRSP share-code or exchange restrictions, or explicit delisting-return handling. It therefore cannot establish that the same results hold for companies without analyst coverage, including potentially extreme cases of valuation uncertainty. The changing coverage count also means that aggregate portfolio composition evolves substantially over time.

Each month firms are sorted using NYSE breakpoints on five characteristics. The ordering is set so decile ten contains the most uncertain firms and decile one the most certain. “Uncertainty” here is an operational label for small capitalization, young listing age, high return volatility, low profitability, and low or no dividends. These are correlated characteristics rather than five independent experiments or a directly observed latent belief variance.

Size is CRSP market equity measured each June. Age is months since first CRSP listing, updated monthly. Volatility is the standard deviation of returns over the preceding twelve months ending in June. Profitability is earnings divided by book equity, where earnings are income before extraordinary items plus deferred taxes less preferred dividends, Compustat items 18, 50, and 19. Book equity is item 60 plus balance-sheet deferred taxes, item 35. Dividend payments, items 25 times 26, are divided by the same book measure. Accounting data for fiscal years ending in calendar year $y-1$ govern monthly portfolios from July of $y$ through June of $y+1$.

These lags should be preserved when reproducing the design. Updating profitability with a statement released later in the return period would alter the experiment. The paper does not fully document treatment of negative book equity, missing items, or ties in characteristics such as zero dividends. A zero-dividend mass makes literal equal-count deciles difficult, so the operational interpretation of the “nonpayers minus payers” tail portfolio needs explicit coding rather than assuming an arbitrary tie-breaking rule.

For characteristic $k$, let $U_{k,t}$ and $C_{k,t}$ denote uncertain and certain tail memberships. The equal-weight return spread is

$$
H_{k,t}=\frac{1}{|U_{k,t}|}\sum_{i\in U_{k,t}}r_{i,t}-\frac{1}{|C_{k,t}|}\sum_{i\in C_{k,t}}r_{i,t}.
$$

The analogous difference in mean forecast errors is the empirical measure of relative expectation bias. Portfolio aggregation helps avoid treating thousands of correlated firm-level errors as independent observations. It does not eliminate common time shocks or persistence, which the authors address separately in their inference.

## Forecast errors, sentiment, and their signs

For an annual EPS forecast $f_{i,t}$ and subsequently realized I/B/E/S EPS $a_i$, the error is

$$
fe_{i,t}=\frac{a_i-f_{i,t}}{|f_{i,t}|}.
$$

Negative values mean optimistic forecasts: actual earnings fell short. Dividing by the absolute forecast avoids mechanically scaling by a market price that may itself reflect sentiment. This is a relative earnings-error unit, not a stock-return percentage. For example, −0.28 means an average shortfall equal to 28% of the absolute forecast, subject to aggregation across firms; it does not imply a 28% return loss.

Zero or near-zero forecasts are an obvious numerical issue. The main text does not specify how exact zeros are handled, or give a full winsorization policy. A sensitivity check excluding absolute forecasts below ten cents per share gives similar results. Scaling errors by stock price instead also produces similar inferences. Those checks reduce concern about denominator-driven effects without providing every preprocessing decision required to match the original sample exactly.

In the initial correlations, the annual consensus is updated each month. Compute the monthly cross-sectional mean error in each decile, then difference uncertain minus certain:

$$
FE_{k,t}=\overline{fe}_{U_{k,t}}-\overline{fe}_{C_{k,t}}.
$$

A negative $FE$ means analysts are relatively more optimistic about uncertain firms. It does not require analysts to be pessimistic about the certain firms. Indeed, the all-stock monthly average is negative in essentially every month of the sample, consistent with the established long-horizon optimism tendency.

Sentiment is the Baker–Wurgler index, obtained from the authors' data source. It is the first principal component of closed-end-fund discounts, the equity share of new issuance, NYSE share turnover, the number of IPOs, first-day IPO returns, and the dividend premium. This paper uses the existing index rather than reproducing all its preprocessing and component-lag choices. A replication needs the historical version of that series and its exact normalization, not merely a generic average of the six inputs.

For the correlation tests, the authors smooth sentiment by averaging the current, previous, and following month. The inclusion of the following month is appropriate to their retrospective association test but unavailable contemporaneously. It would have to be removed or lagged in any forecasting application. The return regressions instead use an indicator that beginning-of-year sentiment is positive. The article preserves that annual timing to match the earlier Baker–Wurgler specification, rather than aligning sentiment exactly with each analyst forecast date.

## Correlation evidence and serial dependence

Table 1 reports a mean all-stock forecast error of −0.28, with standard deviation 0.09 and first-order autocorrelation 0.91 across monthly portfolio observations. Mean uncertain-minus-certain differences are −0.57 for size, −0.25 for age, −0.48 for volatility, −0.54 for profitability, and −0.35 for dividends. Their first-order autocorrelations range from 0.56 to 0.83. The profitability row in Table 1 is labeled “profitable minus unprofitable,” opposite the uncertainty ordering and later table labels; the surrounding definitions and negative-error discussion imply the intended direction is unprofitable minus profitable. That source inconsistency should be tracked when checking signs.

Because analysts' aggregate optimism declines over time, the initial error series are detrended before correlation, except the young-minus-old series, which has no significant trend. The article says raw-series inferences are similar but does not supply the precise trend-fitting specification. Significance is obtained by regressing errors on sentiment and applying Newey–West with four lags, selected using the nearest integer to $T^{0.25}$. This is important: nominal iid correlations would exaggerate the information in persistent monthly series.

Table 2 provides a nuanced result. The all-stock correlation is −0.09, $p=0.310$, so annual-EPS optimism does not significantly co-move with sentiment for the market as a whole. Relative correlations are −0.19 for small minus big, $p=0.114$; −0.13 for young minus old, $p=0.085$; −0.15 for volatile minus smooth, $p=0.084$; −0.23 for unprofitable minus profitable, $p=0.012$; and −0.50 for nonpayers minus payers, $p<0.001$.

Thus the dividend and profitability partitions provide the strongest evidence. Age and volatility are marginal at 10%, and size is not significant at 10%. It would overstate the table to say that sentiment significantly increases annual-EPS optimism for every uncertainty characteristic. The common negative signs nevertheless fit the expected direction and motivate examining whether the errors line up with the return spreads.

## Aligning annual earnings news with returns

For the return tests, the error variable is constructed differently from the monthly-updated correlation variable. For each firm-year the authors take the first consensus annual forecast after announcement of the previous year's fourth-quarter EPS. They subtract it from eventual annual EPS and scale by the absolute forecast. This single error is assigned to each month in a twelve-month window beginning the month after the prior fourth-quarter announcement.

The convention treats annual earnings news as arriving throughout the year, through guidance, analyst revisions, quarterly results, conference calls, and other disclosures. It does not assume all correction occurs during a short earnings-announcement window. Forecast-error portfolios are recalculated across the characteristic memberships in each calendar month, but the underlying firm-year error is not refreshed with monthly revisions. This distinction is essential to reproducing Table 3 rather than accidentally reusing Table 2 inputs.

Let $S_t$ be the positive-beginning-of-year sentiment indicator. The source equation (1), page 298, is

$$
H_{k,t}=\alpha_k+\beta_{S,k}S_t+\beta_{M,k}MKT_t+\beta_{B,k}SMB_t+\beta_{V,k}HML_t+\beta_{E,k}FE_{k,t}+\epsilon_{k,t}.
$$

Returns are in percentage units. Three nested versions include sentiment alone, add the Fama–French factors, and finally add the error series. The uncertainty hypothesis predicts a negative sentiment coefficient and a positive forecast-error coefficient: less fundamental disappointment is associated with higher uncertain-firm returns. The central diagnostic is how much the sentiment coefficient moves toward zero after the error variable enters.

The printed small-minus-big regressions omit an SMB row, although the general equation contains it. This likely avoids mechanically controlling a size spread with another size factor, but the paper does not explicitly explain the omission; reproducing all panels with an identical factor matrix would not match the displayed design. The other four panels report market, SMB, and HML loadings.

## How much of the sentiment-return relation is absorbed?

Table 3 estimates the following sentiment coefficients before and after adding annual EPS errors, conditional on the reported factor controls:

| Uncertain-minus-certain portfolio | Before errors, monthly percentage points | After errors | Reported reduction | Test of reduction |
|---|---:|---:|---:|---:|
| Small minus big | −0.654 | −0.411 | 37% | $p=0.003$ |
| Young minus old | −0.679 | −0.204 | 70% | $p=0.027$ |
| Volatile minus smooth | −0.873 | −0.611 | 30% | $p=0.076$ |
| Unprofitable minus profitable | −0.559 | −0.395 | 29% | $p=0.028$ |
| Nonpayers minus payers | −0.530 | −0.210 | 60% | $p=0.029$ |

The nonpayer example is economically concrete: the estimated high-sentiment relative return deficit falls from about 53 to 21 basis points per month. None of the residual sentiment coefficients is significant at conventional 10% levels in this table, but the remaining magnitudes, especially volatility, are not negligible. Moreover, some pre-error coefficients were already weak: size has $p=0.150$ and profitability $p=0.149$ in the factor-controlled model. “Loses significance” therefore does not describe every panel.

The forecast-error coefficients are positive: 3.536 for size, 2.230 for age, 1.720 for volatility, 1.207 for profitability, and 0.955 for dividends. Their p-values are 0.003, 0.027, 0.076, 0.029, and 0.030. The volatility estimate is only marginal at 10%, despite the prose's broad statement that errors are significant throughout. A one-unit error difference is a 100-percentage-point difference relative to absolute forecast, so coefficient magnitudes should not be interpreted as the return effect of a one-cent EPS miss.

The authors use the Clogg–Petkova–Haritou test for changes in coefficients across nested models. A reduction is approximately $1-\widehat\beta_S^{with}/\widehat\beta_S^{without}$, but its significance depends on covariance between the estimates, not independent standard errors. The article references the method rather than printing its complete calculation. Monthly return regressions initially do not use autocorrelation corrections because residual persistence is low; a four-lag Newey–West sensitivity check reportedly preserves inferences, including for the size portfolio whose residual autocorrelation is significant.

This is evidence that realized fundamental news and sentiment-related returns overlap. It is not a fraction of causal mispricing identified without assumptions. Forecast errors incorporate future economic shocks, and both earnings news and stock returns respond to fundamentals. An ex post variable can absorb a sentiment coefficient even when the precise channel is not exclusively biased beliefs. The authors' design becomes more persuasive when combined with the direct forecast-error correlations and strategic-incentive checks, but it remains observational.

## Long-term earnings growth

Long-term-growth expectations are measured from I/B/E/S summary forecasts. Tables 4 and 5 explicitly use median consensus growth forecasts, unlike the mean annual EPS consensus. Actual growth is estimated from a log-linear trend over five annual earnings observations starting in the forecast year:

$$
\log(EPS_{i,y+j})=a_i+g_i j+u_{i,j},\qquad j\in\{0,1,2,3,4\}.
$$

The fitted slope $g_i$ is the actual growth measure; the error is $g_i$ minus the forecast, with units harmonized to the I/B/E/S growth convention. The paper does not specify whether the log slope is transformed by $\exp(g_i)-1$; its description says to use the slope. A faithful replication should not introduce a transformation without recording it.

Negative EPS observations are omitted, and at least three usable annual observations are required. The text calls these “nonnegative” observations, although logarithms of zero are undefined. An implementer needs a strictly positive criterion or an explicit zero treatment. This is a real missing input, not an invitation to set zero earnings to an arbitrary small constant. Omitting negative observations also creates selection toward firms with enough positive future earnings to estimate growth.

The profitability partition is dropped because unprofitable firms commonly have negative current and future EPS. Availability of positive earnings and growth forecasts reduces the sample by 278,347 observations relative to the annual-error sample. The growth tests end in 2004. Their realized outcome uses up to five years of future earnings, while the return model captures only the first twelve months after the forecast. The authors explicitly acknowledge this horizon mismatch.

Table 4 finds a market-wide sentiment correlation of −0.39, $p<0.001$, unlike the weak annual-EPS result. Relative correlations are −0.04 for size, $p=0.411$; −0.29 for age, $p=0.005$; −0.44 for volatility, $p<0.001$; and −0.65 for dividends, $p<0.001$. The growth-error series show no clear trend and are not detrended. Newey–West with four lags is again used, though five-year realized growth overlap raises a broader persistence issue worth examining in a replication.

For return attribution, the first growth forecast after the prior fourth-quarter announcement is paired with realized growth and assigned across the same twelve-month window. Table 5's sentiment slope falls by 71% for size, from −0.901 to −0.261 percentage points per month, $p=0.003$ for the change; and by 35% for age, from −1.077 to −0.705, $p=0.023$. Reductions are only 10% for volatility, $p=0.400$, and 16% for dividends, $p=0.276$. The correlation strongest in levels is therefore not necessarily the most effective return-attribution variable.

With both errors in Table 6, reductions are 49% for size, $p=0.0368$; 96% for age, $p=0.006$; 29% for volatility, $p=0.220$; and 41% for dividends, $p=0.083$. Residual sentiment slopes are −0.462, −0.041, −0.973, and −0.519, respectively, with p-values above 0.10. The volatility reduction is not statistically significant. The table caption describes median forecasts for annual EPS as well as growth, conflicting with the mean-EPS description in the main annual analysis. The consensus convention for this combined test is unresolved in the supplied source.

The reduction percentages are not additive or necessarily monotone as controls are added. Size provides a concrete example: long-term-growth errors alone reduce the sentiment slope by 71% in Table 5, while both errors reduce it by 49% in Table 6. Both error coefficients remain positive and significant in the combined size regression. Correlation among sentiment and the two error measures changes their conditional coefficients; adding a second error need not push the sentiment slope still closer to zero. These percentages therefore cannot be treated as disjoint shares of a causal return decomposition or summed into a fraction of mispricing explained.

The outcome is also a return spread conditional on a sentiment regime, not the portfolio's unconditional alpha. Table 1 reports average monthly uncertain-minus-certain returns of 0.41% for size, −0.01% for age, 0.03% for volatility, 0.16% for the profitability row, and 0.14% for dividends. Small unconditional averages can coexist with a substantial negative high-sentiment coefficient because performance changes across regimes. The intercept and regime coefficient jointly determine the fitted return at each sentiment state, and factor exposures must also be included. A researcher who compares only the high-sentiment coefficient with a transaction-cost estimate would be evaluating an incomplete trading rule.

The article also projects sentiment onto forecast errors and separates its fitted and residual components in untabulated checks. With annual errors, the fitted component predicts returns in all five partitions and the residual in none; with both errors, the same pattern holds in all four eligible partitions. This is another representation of the shared variation rather than an independent source of identification. Exact coefficients, projection details, and adjusted inference for generated regressors are not tabulated.

## Strategic incentives and alternative explanations

Analyst optimism could be deliberate catering rather than an unintended reflection of sentiment. The paper offers three checks. First, monthly I/B/E/S recommendation data run from November 1993 to December 2005, with one meaning strong buy and five strong sell. If analysts strategically become more bullish on uncertain firms in high-sentiment periods, uncertain-minus-certain recommendation differences should correlate negatively with sentiment. Instead, correlations are +0.63 for size, $p<0.001$; +0.05 for age, $p=0.780$; −0.03 for volatility, $p=0.399$; −0.36 for profitability, $p=0.001$; and +0.27 for dividends, $p=0.036$ (Table 7).

This rejects a uniform recommendation-catering pattern, not every strategic explanation. Recommendation levels can depend on valuation ratios that change differently from earnings estimates, and incentives for forecasts and recommendations need not be identical. Restricting forecast-error correlations to the shorter recommendation period reportedly makes the negative correlations stronger, so simple sample-date mismatch does not explain the contrast.

Second, the authors estimate firm-month regressions separately for forecasts 12, 11, and 10 months before annual announcement, versus forecasts three, two, and one month before it:

$$
fe_{i,t}=a+b_SS_t+b_XX_{i,t}+b_{XS}X_{i,t}S_t+u_{i,t},
$$

where $X$ is a rank increasing in uncertainty and $S$ now uses contemporaneous positive sentiment. Standard errors are clustered by firm–fiscal year. Strategic long-run optimism followed by beatable short-run forecasts would suggest attenuation or reversal of the uncertainty interaction. Instead, late-year interactions remain negative for all characteristics. For volatility they are −0.103 early and −0.061 late; profitability −0.111 and −0.077; dividends −0.124 and −0.088, all with $p<0.001$. The size interaction is −0.028 early, $p=0.249$, and −0.048 late, $p<0.001$. Thus the general optimism level falls as the announcement approaches, while relative high-sentiment optimism survives.

Third, an untabulated comparison finds no significant relation between sentiment and uncertain-minus-certain net insider selling for any characteristic. This weakens an explanation centered on analysts supporting managerial sales. Details of the insider-trading sample and estimator are not provided, so the null cannot be treated as a decisive test with known power.

Other sensitivity tests help bound the interpretation. Replacing signed errors with absolute errors yields little explanatory power for returns, supporting the relevance of directional disappointment rather than generic forecast difficulty. Market-wide Granger tests do not find that sentiment predicts errors or that errors predict sentiment conditional on their lags; the authors interpret the relationship as contemporaneous. Such nulls do not determine causal direction, especially because errors are realized only later and exact lag specifications are not tabulated.

Using Michigan consumer confidence produces similar negative error correlations but much weaker prediction of the characteristic return spreads. The Michigan and Baker–Wurgler indices correlate 0.46 over the sample. The return-attribution exercise is therefore not replicated with Michigan confidence because there is little return relationship to explain. This is partial robustness of the expectations association, not full robustness of the entire mechanism across sentiment measures.

## Practical interpretation and replication limits

The article supports a specific research hypothesis: optimism in earnings expectations varies with sentiment more strongly in some hard-to-value portfolios, and eventual disappointments help account for their relative returns. It does not show that all investors share sell-side forecasts, that analyst bias is necessarily unintended, or that limits to arbitrage are unimportant. Analysts may respond to prices, and arbitrage limits may influence those prices; the authors acknowledge that possibility while arguing that it is unlikely to explain the whole pattern.

A reconstruction should maintain separate datasets for monthly-updated forecasts and frozen first-of-year forecasts, preserve accounting lags, harmonize consensus and actual EPS definitions, and handle splits consistently. I/B/E/S split adjustment and penny rounding can distort individual forecast errors; the paper argues that averaging across firms mitigates bias and finds little sentiment-related variation in differential split incidence, apart from the age partition. That check is reassuring without eliminating every data-vintage issue.

No transaction costs, turnover, borrow fees, or capacity are analyzed. The long-short portfolios are explanatory research objects. A deployable model would need a forecast of future errors using only information available at the decision date, a sentiment series without future-month smoothing, and genuinely out-of-sample validation. The published contribution is the evidence connecting beliefs to subsequent fundamentals and returns; its most useful quantitative discipline is to keep that explanatory evidence separate from a claim that the realized errors themselves constitute a tradable signal.

# Active Share and Mutual Fund Performance

**Antti Petajisto (2013).** *Financial Analysts Journal* 69(4), July/August, 73–93. Source: [BestIdeas_Petajisto_2013.pdf](../../Finance/BestIdeas_Petajisto_2013.pdf). The complete 21-page article, including methodological endnotes and all eleven tables, is covered here. Journal page numbers are used below; PDF page 1 is journal page 73.

## Why this matters and what is new

The paper separates how much a fund differs from its benchmark from how volatile that difference is. A manager can own a distinctive, diversified collection of individual stocks without taking a large systematic factor bet. Conversely, a relatively small deviation in holdings can generate substantial tracking error if the deviations align with a sector or market factor. Looking only at tracking error conflates these approaches.

Using both holdings-based Active Share and return-based tracking error, Petajisto classifies U.S. equity mutual funds into diversified stock pickers, concentrated managers, factor bettors, moderately active funds, and closet indexers. The main performance sample is January 1990–December 2009. Diversified stock pickers earn an average 1.26% annual benchmark-adjusted return after fund fees and trading costs, versus −0.91% for closet indexers. The corresponding four-factor alpha spread is 2.45% annually, with $t=4.00$. High tracking error alone does not identify the successful funds.

This extends Cremers and Petajisto's earlier work by six years, changes several measurement choices, studies the financial crisis, separates concentrated from diversified stock selection, and investigates whether cross-sectional stock-return dispersion predicts the environment for stock pickers. It is an observational fund-selection study. It does not prove that mechanically increasing Active Share improves any given manager's skill, or that all systematic factor investing destroys value. The empirical “factor bets” category is a set of mutual funds identified by a return-risk measure, not an experiment on every possible factor strategy.

## Two measures with different information

For a fund and a chosen benchmark, let $w_i$ and $b_i$ be weights on the union of all assets held by either portfolio. Active Share is

$$
AS=\frac12\sum_i|w_i-b_i|.
$$

For fully invested long-only portfolios, $\sum_iw_i=\sum_ib_i=1$ and both vectors are nonnegative. Therefore

$$
AS=\sum_{i:w_i>b_i}(w_i-b_i)
=\sum_{i:w_i<b_i}(b_i-w_i)
=1-\sum_i\min(w_i,b_i).
$$

The identities show why the factor one-half appears: active long and active short deviations have equal notional. “Short” here usually means an underweight relative to the benchmark, not an actual short sale in the fund. Active Share is between zero and one under these assumptions. With shorts, leverage, cash treatment, derivatives, or unmatched holdings, the simple interpretation needs care. The article defines the measure over all assets but does not supply a complete coding specification for every non-equity or unmatched position in the holdings database.

Tracking error is

$$
TE=\operatorname{sd}(R_{fund}-R_{benchmark}).
$$

The study estimates it from daily returns over the six months before each holdings-report date, reporting annualized values. This is the standard deviation of the active return, not the residual standard deviation after fitting a free benchmark beta. The difference matters for cash timing: a fund that reduces equity exposure can have little regression residual but substantial active-return volatility. The paper does not state the precise annualization trading-day constant or minimum daily observation count.

As an illustration, consider 50 equally weighted industries with 20 equally weighted benchmark stocks each. Holding one stock per industry while matching every industry weight gives Active Share about 95%. Industry exposures can still cancel in the active portfolio, keeping tracking error modest if selected-stock residuals diversify. By contrast, overweighting the same sector across many names creates common risk. Neither measure, however, is an exact factor decomposition. Active Share does not know the covariance matrix, and tracking error also includes undiversified stock-specific risk.

The fee interpretation is useful: if a fund has Active Share one-third and charges 1.5% on all assets, its fee burden relative to its active notional is about 4.5%. This arithmetic does not imply that the passive and active pieces are separately traded or that costs scale linearly in practice. It shows why an expensive fund with small deviations needs a high return per unit of deviation to cover fees.

## Data assembly, benchmarks, and sources of look-ahead

The holdings source is Thomson Reuters, linked to CRSP mutual-fund data with MFLINKS and matched to CRSP securities. Benchmark holdings come directly from S&P, Russell, and Dow Jones/Wilshire. Nineteen indices cover common large-, mid-, and small-cap universes and their value/growth components. Fund monthly returns are net of expenses and brokerage commissions but before front/back-end sales loads. Daily fund returns use CRSP from September 1998 and the combined source used by Cremers and Petajisto before then. Index returns include dividends. The databases contain both surviving and dead funds.

The fund screens use four CRSP objective codes and one Thomson code, average CRSP stock allocation of at least 70%, and at least 60% matched U.S. stock holdings. Sector funds and funds with assets below \$10 million are excluded. For funds with multiple share classes, returns, fees, turnover, and other attributes are aggregated using value weights. The final historical universe contains 2,740 funds over 1980–2009. Performance comparisons begin in 1990 because almost all funds were highly active in the 1980s.

Benchmark assignment differs from the earlier study. The preferred benchmark is the fund's prospectus primary benchmark, obtained from Morningstar snapshots in January 2007 and March 2010, preferring the earlier snapshot. If unavailable, choose the index with the lowest average Active Share over the preceding three years. Indices enter only after their actual inception; backfilled histories are not treated as contemporaneously available benchmarks. The article argues that factor adjustments address misleading manager benchmarks, but this does not eliminate every issue caused by changing or retrospectively observed benchmark labels.

A replication should distinguish statistical description from a fully point-in-time fund-selection backtest. Two late-sample snapshots of prospectus benchmarks cannot by themselves establish which benchmark every fund publicly used in every earlier year. Similarly, the fund classification uses latest holdings values at month-end, but this article does not specify a two-month public-disclosure lag comparable to an explicit copycat strategy. It should not be assumed that an outside investor could observe every classification input immediately on its holdings date. Preserve these source conventions when reproducing the published result, then add contemporaneous benchmark and filing timestamps as an extension.

Manual corrections to MFLINKS and the change in CRSP's underlying data provider also affect sample comparability. The paper reports that Morningstar- and Lipper-based CRSP versions omit different funds despite both being intended as survivorship-free databases. Concentrated portfolios are particularly sensitive because the group is small and volatile. The article gives selection thresholds and sources but not all objective-code values, manual correction records, stale-holdings rules, or exact handling of delistings within hypothetical holdings returns.

## Reconstructing the fund categories

At the end of each month, eliminate index and enhanced-index funds from the active comparison. Sort remaining funds into quintiles of Active Share. **Within each Active Share quintile**, sort into tracking-error quintiles. The second sort is conditional, rather than based on one set of universal tracking-error breakpoints. Assign the 25 cells as follows:

| Active Share quintile | Tracking error 1–4 | Tracking error 5 |
|---|---|---|
| 5, highest | Stock pickers | Concentrated |
| 2–4 | Moderately active | Factor bets |
| 1, lowest | Closet indexers | Factor bets |

With equally populated cells, the stock-picker, factor-bet, and closet-indexer categories each contain about 16% of funds, concentrated funds 4%, and moderately active funds 48%. These are relative rankings. They are not the same as applying a fixed Active Share threshold of 60% to every fund every year; the paper also uses that threshold for descriptive discussion of closet indexing.

Table 4 shows approximately 1,124 funds in a typical month: 180 stock pickers, 45 concentrated funds, 179 factor bettors, 541 moderately active funds, and 180 closet indexers, with rounding. Mean Active Shares are respectively 97%, 98%, 79%, 83%, and 59%; tracking errors are 8.5%, 15.8%, 10.4%, 5.9%, and 3.5% annually. The stock-picker and concentrated groups own 66 and 59 stocks on average. Their distinction is therefore not simply the number of names.

Mean assets range from \$430 million for stock pickers to \$2.009 billion for closet indexers. Annual turnover is 83%, 122%, 104%, 84%, and 69%; expense ratios are 1.41%, 1.60%, 1.34%, 1.25%, and 1.05%. The concentrated group trades most and charges most, while the closet group remains costly relative to its small active component. Group returns are equal-weighted across funds to prevent one very large fund from dominating the result.

## Performance estimands and main results

“Gross return” means the hypothetical return on disclosed stock holdings without fees or transaction costs. “Net return” is the actual fund investor return after those costs, excluding sales loads. Thus the gross-minus-net difference is not a clean estimate of management fees alone: cash positions, unobserved interim trading, non-equity positions, and holdings measurement can contribute.

First subtract each fund's benchmark return. Then estimate a Carhart regression of the resulting active-return series on market, size, value, and momentum factors to remove residual exposures. A generic group-level representation is

$$
R^{active}_{g,t}=\alpha_g+\beta_g'F_t+u_{g,t}.
$$

The article's Table 5 presents annualized percentage returns and $t$-statistics using White heteroskedasticity-robust standard errors. The key estimates are:

| Fund group | Gross benchmark-adjusted | Gross four-factor alpha | Net benchmark-adjusted | Net four-factor alpha |
|---|---:|---:|---:|---:|
| Stock pickers | 2.61 | 2.10 | 1.26 | 1.39 |
| Concentrated | 1.64 | 0.52 | −0.25 | −0.89 |
| Factor bets | 0.06 | −1.02 | −1.28 | −2.19 |
| Moderately active | 0.82 | 0.20 | −0.52 | −0.78 |
| Closet indexers | 0.44 | 0.13 | −0.91 | −1.07 |
| All active funds | 0.96 | 0.31 | −0.41 | −0.71 |

The stock-picker net benchmark-adjusted estimate has $t=1.95$, whereas its four-factor alpha has $t=2.10$. The 2.17% stock-picker-minus-closet net return spread has $t=3.48$; its 2.45% alpha spread has $t=4.00$. Distinguish the stronger evidence for a difference between categories from the marginal significance of some absolute positive returns. The concentrated fund estimate is noisy and does not demonstrate average outperformance.

Reforming the entire grid separately within large-, mid-, and small-cap styles yields broadly similar patterns: stock pickers' gross benchmark-adjusted return is 2.54%, and net is 0.89%. Nine size/value style cells also give similar qualitative results, although detailed estimates are not tabulated. This reduces, without fully eliminating, the concern that Active Share merely selects small-cap benchmarks.

Sorting by fund size within each category produces no monotone performance-size pattern. The smallest stock pickers earn 1.84% net benchmark-adjusted return, while the largest earn 1.38%; their −0.46% high-minus-low difference has $t=-0.69$. The author interprets much of the overall size relation as operating across management types: large funds are disproportionately closet indexers. This is a descriptive decomposition, not proof that capacity is irrelevant within a strategy.

## Persistence and multivariate predictive tests

For persistence, sort funds within each category by prior-calendar-year benchmark-adjusted net return and examine subsequent performance. Concentrated prior winners beat prior losers by 10.04% annually, $t=2.28$, before the four-factor adjustment. The spread falls to 4.61%, $t=1.54$, after adjustment. That remaining magnitude is economically large but not conventionally significant at 5%. For diversified stock pickers, the spread falls from 3.20%, $t=1.68$, to 1.00%, $t=0.70$. Closet indexers have essentially no four-factor persistence: 0.01%, $t=0.01$.

The paper suggests that concentrated funds may have greater dispersion of skill, including both excellent managers and speculative, unskilled managers. That is an interpretation compatible with the evidence, not a directly observed distribution of true alpha. Momentum explains much of the observed persistence, and small group size increases uncertainty.

Table 8 estimates pooled annual panel regressions over 1992–2009, using year-$t$ benchmark-adjusted cumulative net returns or four-factor alpha as the dependent variable and characteristics measured at the end of $t-1$. Controls include turnover, expenses, base-10 log assets, assets squared, age, number of stocks, manager tenure, past one-to-three-year returns and flows, and year dummies. Standard errors cluster by year; there are 11,534 fund-year observations. To avoid survival selection, a fund-year is retained even when only one month of returns exists, which requires special care when interpreting partial-year cumulative outcomes.

The Active Share coefficient is 0.0739, $t=2.76$, for benchmark-adjusted return and 0.0609, $t=2.24$, for alpha. With fractions as inputs, a ten-percentage-point increase predicts approximately 0.739 percentage points higher annual return. Style interactions are positive: the benchmark-adjusted coefficients are 0.0867, 0.1023, and 0.1635 for large-, mid-, and small-cap funds. An alternative category specification estimates stock pickers outperforming closet indexers by 2.88% annually, $t=2.48$, or 2.11% alpha, $t=2.06$.

Expenses have coefficients below −1 in several specifications, suggesting that high fees correlate with worse gross quality as well as directly reducing net return. Fund age has a small negative coefficient. These regressions establish conditional predictive associations in the historical sample, not intervention effects. The article does not supply an independent post-selection holdout for choosing the category scheme or all controls.

## Predicting the opportunity set with cross-sectional dispersion

For market weights $b_{i,t}$ and stock and market returns $R_{i,t}$ and $R_{m,t}$, define monthly cross-sectional dispersion

$$
D_t=\sqrt{\sum_i b_{i,t}(R_{i,t}-R_{m,t})^2}.
$$

The author constructs this measure using Russell 3000 holdings because the vendor CrossVol history begins only in July 1996. Table captions sometimes describe vendor-computed values more broadly; the text establishes the reconstructed earlier series. Start/end-of-period weight conventions are not fully specified and matter for exact replication.

Regress the equal-weighted stock-picker benchmark-adjusted net return on current, leading, and lagged dispersion. In the univariate lag-one specification, the coefficient is 0.0846, $t=2.77$, with $R^2=7.6%$ across 240 months. If returns and dispersion are measured as fractions, a one-percentage-point rise in prior dispersion predicts roughly 8.46 basis points in the next month's active return. Contemporaneous dispersion alone has a small insignificant positive coefficient. A regression with multiple leads/lags reveals a negative contemporaneous effect and positive predictive lag effects.

The expected component is generated from an AR(3) of dispersion using its three most recent values; the innovation is actual minus predicted dispersion. In the joint model, expected dispersion has coefficient 0.1071, $t=3.18$, and its innovation −0.1582, $t=-3.08$, with $R^2=16.1%$. High initial dispersion followed by a fall is favorable to stock pickers, whereas a surprise increase is unfavorable. The article does not disclose the AR coefficient estimation window or whether these coefficients are recursively estimated. Calling this a strictly real-time trading forecast would therefore require additional documentation.

The proposed mechanism is convergence of stock-specific mispricing, with portfolio managers' risk-target responses potentially amplifying divergence and convergence. It remains a hypothesis: observed dispersion is not a direct measurement of mispricing. Results are similar after excluding dispersion above 15% and using Newey–West standard errors with two or twelve monthly lags. Replacing returns with benchmark-adjusted four-factor alphas roughly halves the coefficients. Effects weaken for all funds collectively, consistent with dispersion relating more closely to stock selection than closet indexing.

The comparison metric is average stock correlation with the market. For each month, the author estimates market-model betas and variances from daily observations, about 21 observations per stock, using S&P 500 stocks for liquidity. Under a single-factor orthogonality assumption,

$$
\rho_t=\sum_i b_{i,t}\frac{\beta_{i,t}\sigma_{m,t}}
{\sqrt{\beta_{i,t}^2\sigma_{m,t}^2+\sigma_{\varepsilon_i,t}^2}}.
$$

Average correlation predicts fund performance weakly: coefficient −0.0074, $t=-1.37$, $R^2=1.0%$. Idiosyncratic cross-sectional dispersion and beta dispersion have stronger predictive relations. Dispersion measures absolute differences in stock returns, whereas correlation normalizes by total volatility and can obscure their magnitude. The Russell 3000 dispersion and S&P 500 correlation constructions also differ in universe, an important replication qualification.

## Mathematical qualifications to the exposition

Two attractive statements in the article should not be promoted into general theorems.

First, pp. 78–79 motivate a 50% “theoretical minimum” Active Share by suggesting that approximately half of the index value must outperform its mean. A mean does not divide a weighted distribution into equal masses. A small benchmark-weighted subset can earn very large positive excess returns while most of the index earns slightly negative excess returns. Nor does Active Share directly measure the fraction of holdings expected to have negative alpha. A manager can make small, well-founded overweight and underweight adjustments while retaining all benchmark stocks. The 50% and 60% thresholds are economically motivated classification heuristics; optimal deviation also depends on risk, costs, constraints, estimation error, and fees.

Second, Equation 4 and endnote 9 present a dispersion decomposition with no beta-residual cross term. Given $R_i=\beta_iR_m+\varepsilon_i$ and a consistent fully invested market representation, the exact realized identity is

$$
D_t^2=R_{m,t}^2\sum_i b_{i,t}(\beta_i-1)^2
+\sum_i b_{i,t}\varepsilon_{i,t}^2
+2R_{m,t}\sum_i b_{i,t}(\beta_i-1)\varepsilon_{i,t}.
$$

The final term does not vanish at every date merely because each stock's time-series residual is orthogonal to the market. Cross-sectional covariance between beta and that month's realized residual is a different object. It may vanish under an additional cross-sectional condition or in a suitable expectation, but that is an extra assumption. For example, equal-weighted stocks with betas 0.5 and 1.5 and residuals $a$ and $-a$ have zero weighted residual and average beta one, yet their weighted beta-residual product is $-a/2$. Directly computing $D_t$ avoids relying on the shortened identity. This qualification does not by itself overturn the empirical regression using observed dispersion.

## Crisis evidence, limitations, and takeaways

Over January 2008–December 2009, stock pickers earn 0.97% annual benchmark-adjusted net return, concentrated funds −2.59%, factor bettors −1.72%, moderately active funds −0.32%, and closet indexers −0.83%. The stock-picker/closet spread is 1.79%, but $t=0.89$: a two-year stress episode is too short for strong inference. In 2009 alone, concentrated funds rebound 9.41% relative to benchmarks and stock pickers 6.09%, while closet indexers lose 0.66%. Strong recovery does not erase the earlier concentrated-fund drawdown.

The practical contribution is a disciplined separation of holdings deviation, active risk, and fees. A replication should first reproduce the sequential 5×5 sorts and category counts, then both actual net returns and hypothetical holdings returns, and finally benchmark-adjusted and factor-adjusted performance. It should separately audit benchmark vintage and holdings availability before describing the outcome as investable. A fund with high Active Share still requires evidence of skill, reasonable costs, and a suitable risk structure; a high value is neither sufficient for alpha nor a prescription to concentrate indiscriminately. The paper's strongest evidence favors historically distinctive but diversified stock selection over expensive benchmark-like portfolios, with useful qualifications about timing, category size, and source mathematics.

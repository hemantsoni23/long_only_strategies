# The Impact of Volatility Targeting

**Campbell R. Harvey, Edward Hoyle, Russell Korgaonkar, Sandy Rattray, Matthew Sargaison, and Otto Van Hemert.** *Journal of Portfolio Management* 45(1), Fall 2018, pp. 14–33; DOI 10.3905/jpm.2018.45.1.014. **Source:** [Finance/volatilitytargeting_Harvey_2018.pdf](../../Finance/volatilitytargeting_Harvey_2018.pdf), 21 PDF pages including the publisher cover. PDF page 2 is printed page 14. The separate online supplements referenced in the article were not included locally; the publisher supplement link could not be retrieved during preparation. Claims below distinguish the inspected article from supplementary results it only describes.

## Why this matters and what is new

Volatility targeting is often justified as a way to keep portfolio risk stable, then credited with improving returns as though the two benefits were equivalent. This paper separates those questions across more than 60 assets. Its principal empirical contribution is that inverse-volatility scaling improves historical Sharpe ratios mainly for equities, credit, and portfolios materially exposed to them. For currencies, commodities, and modern Treasury futures, the Sharpe effect is generally negligible. Risk stabilization is more widespread than return enhancement.

The paper also relates the differences across assets to a mechanism: equity and credit returns tend to be negatively associated with changes in volatility. After adverse returns, a volatility target reduces exposure; after favorable returns, it tends to raise exposure. This embeds a momentum-like position adjustment. Across the examined assets, the association of inverse volatility with recent returns explains a substantial share of the variation in Sharpe improvements. This is descriptive evidence about a channel, not a structural causal identification of the leverage effect or a theorem that volatility targeting must improve performance.

A replication must preserve three design choices that can easily be lost in a verbal summary. The strategy uses information through $t-2$ for return $t$, providing a full 24-hour gap. All comparisons are rescaled ex post to 10% full-sample realized volatility. And the reported balanced portfolio's 60/40 split is applied to volatility-normalized asset returns: it is a risk-unit allocation, not a conventional 60% equity and 40% bond capital allocation.

## Return data and sample construction

Exhibit 1 and the preliminary section provide the source map. Broad U.S. equities are the value-weighted NYSE, AMEX, and Nasdaq market series from Kenneth French, with daily observations beginning 1 July 1926. The ten French industry portfolios are also used. Equity performance is evaluated over 1927–2017 after initialization, with approximately three 30-year subperiods; Exhibit 1 labels 1928–1957, 1958–1987, and 1988–2017. The prose elsewhere describes the middle interval as 1957–1987. A replication should resolve this boundary against the original sample implementation rather than silently shift dates.

Historical U.S. Treasury returns are proxied from Federal Reserve daily ten-year yields starting in 1962. Treat the yield as the par yield of a semiannual-coupon bond. Reprice the par bond the following day using the new ten-year yield, moving every cash flow $1/261$ of a year closer. The one-day return is the repriced value minus par. This is a deliberately simplified constant-maturity return proxy, not observed total returns on an unchanged bond identifier. Historical monthly bond data from Global Financial Data extend the descriptive plots back to July 1926; they do not replace daily data in the volatility estimator. The bond-strategy performance sample begins in 1963.

S&P 500 and ten-year U.S. Treasury futures have daily and five-minute data from 1988, provided through Man AHL. The detailed performance tables use 1988–2017. Some rows in the source overview print 1988–2018, while exhibit captions state 1988–2017; the latter dates govern the numerical results quoted here. This inconsistency should be retained as a data-boundary uncertainty rather than resolved by invention.

The broader liquid futures/forward panel contains 50 instruments: six agricultural contracts, six energy contracts, seven metals, nine currency pairs against the U.S. dollar, ten equity-index contracts, nine bonds, and three interest-rate contracts. Credit is the Bank of America Merrill Lynch U.S. Corporate Master Total Return index hedged with Treasuries according to Cook et al. (2017). The intention is an exposure resembling synthetic investment-grade CDX. The article does not reproduce the complete hedge construction or identify every contract, roll date, forward maturity, vendor field, or price timestamp.

Work with excess or otherwise unfunded returns. For cash equity and proxy cash Treasury investments, deduct the T-bill financing return. Futures and forward returns are treated as already essentially unfunded, so a second risk-free subtraction is inappropriate. Treasury-hedged credit is also unfunded by construction. This convention is essential when leverage changes through time: scaling total returns without separately accounting for financing would create a spurious contribution from cash yield.

## Volatility estimator and exact information timing

Let $r_t$ be the relevant daily excess/unfunded return. For half-life $h$, an implementable representation of the paper's exponentially weighted zero-mean second moment is

$$
q_t=(1-\lambda_h)r_t^2+\lambda_h q_{t-1},\qquad
\lambda_h=2^{-1/h}.
$$

The annualized volatility estimate is $\widehat\sigma_t=\sqrt{Aq_t}$, with $A$ adjusted to the observation calendar. This recursion is a reconstruction of the described exponential weighting; initialization and finite-history renormalization are not specified. The source explicitly uses a stated zero mean rather than estimating a noisy short-window sample mean. It requires 270 trading days of input before scaled returns are formed, corresponding to three half-lives of the slowest 90-day estimator.

The position producing return $r_t$ uses $\widehat\sigma_{t-2}$:

$$
\ell_t=k_s\frac{0.10}{\widehat\sigma_{t-2}},\qquad
r_t^{s}=\ell_t r_t.
$$

Thus both the newest realized return and the newest volatility update available immediately before earning $r_t$ are deliberately excluded. A backtest using $\widehat\sigma_{t-1}$ implements a faster strategy than the article. The constant $k_s$, approximately one in the authors' description, is selected using the complete sample so the scaled series realizes 10% annualized volatility. The unscaled benchmark is $r_t^u=k_ur_t$, with $k_u$ likewise chosen to realize 10% over the comparison sample.

These constants make statistical comparisons easier but are not estimated solely from past information. For an individual strategy's gross Sharpe ratio, a fixed positive multiplier cancels. It does not make reported leverage, shortfalls, compounded wealth, or multiasset weights available ex ante. A live implementation requires a separately stated historical calibration or rolling rule. That modification should not be represented as an exact reproduction of the paper.

Daily-data half-lives are 10, 20, 40, 60, and 90 days; 20 days is the default for cross-asset figures. Equal-weight fixed windows and overlapping three- or five-day return estimators reportedly give similar results, but those robustness outputs are not shown. There is no described optimization over half-lives or out-of-sample model-selection criterion.

For broad U.S. equity data, calendar-day treatment accommodates Saturday exchange trading before 1952. Saturday squared returns are doubled before updating volatility because Saturdays were partial trading days. Other assets use weekday data. The article adjusts annualization for the number of observations but does not fully document zero filling on nontrading days or holiday-specific handling. Reproduction must not apply a uniform 252-day convention to every historical series without checking these choices.

For the two U.S. futures with high-frequency data, sum squared five-minute returns from 9:15 a.m. to 2:00 p.m. Chicago time to obtain each day's realized variance. Smooth these daily realized variances with exponentially decaying weights and take a square root. Intraday half-lives in the tables are 5, 15, 25, 40, and 60 days. The common restricted session is chosen for consistent liquidity across the history and the two securities. Adding the squared overnight return reportedly makes persistence slightly weaker, but that result is not tabulated. Intraday scaling still respects the same two-day information cutoff; it is not same-day intraday execution.

## Evaluation, shortfalls, and trading costs

Most statistics are evaluated on overlapping one-month returns: 30 calendar days for broad U.S. equities and 21 weekdays for the other assets. Mean exposure and turnover use daily observations. The source does not fully spell out the summation versus compounding convention used to assemble every rolling excess-return statistic; its cumulative performance plots explicitly display cumulative log returns. A faithful code implementation should document these separately rather than assume that adding daily excess returns is the same as a funded compound return.

The annualized Sharpe ratio is mean excess return divided by its standard deviation with the appropriate frequency conversion. Volatility of volatility is the standard deviation of rolling one-year realized volatility, itself computed from overlapping monthly returns. The left-tail measure at probability $p$ is the average realized return in the worst $p$ fraction of observations, reported as a negative return rather than a positive loss. It differs from the $p$-quantile VaR. The right-tail counterpart averages returns above the 95th or 99th percentile. These statistics describe realized sample tails, not a model-implied conditional forecast at each date.

For nonnegative exposure $\ell_t$, reported turnover is annual mean absolute exposure change divided by twice mean exposure:

$$
\tau=\frac{A\,\overline{|\ell_t-\ell_{t-1}|}}{2\bar\ell}.
$$

This counts annual roundtrips of the average notional position. If the one-way transaction cost per unit of notional is $c$, annual scaling cost is approximately $2c\bar\ell\tau$. The chosen estimates are 1.0 basis point for equities, 0.5 for bonds, 0.5 for credit, 1.0 for gold, 2.0 for oil, and 3.5 for copper. Tables show gross and net Sharpe ratios; figures are gross. Futures/forward rolling turnover and its costs are excluded. The unscaled single-asset position therefore has zero turnover under this definition.

The cost assumptions are intended to reflect the post-2008 trading environment and are applied over the historical sample. They are not estimates of executable 1930s costs. The credit assumption reflects a synthetic investment-grade index implementation, rather than the costs of physically trading every bond in the historical corporate index. Funding spreads above the risk-free rate, margin constraints, leverage caps, nonlinear impact, and forced deleveraging are not modeled.

For the ten-day U.S. equity rule, the paper illustrates annual cost as $2\times0.0001\times0.71\times4.66\approx0.00066$, or 6.6 basis points on the 10%-volatility strategy. Its unrounded gross and net Sharpe ratios are 0.4831 and 0.4766; both round to 0.48. Equal displayed Sharpe ratios therefore do not imply zero costs.

## U.S. equity results

Exhibit 4 sorts months by the preceding month's volatility. Next-month volatility rises strongly across quintiles, while expected excess returns do not show a comparably increasing pattern. The intuitive case for scaling is that persistent high variance does not come with a proportionate near-term mean-return reward. The exercise is descriptive and does not identify the full conditional distribution of returns or establish that expected returns are exactly constant.

Exhibit 5 reports the following for 1927–2017. Every strategy has 10% ex post full-sample volatility. Tail entries are monthly return averages in the indicated worst tail, and vol-of-vol entries are percentage points of annualized volatility.

| Rule | Gross Sharpe | Mean exposure | Roundtrips/year | Vol of vol | Worst 1% mean | Worst 5% mean |
|---|---:|---:|---:|---:|---:|---:|
| Unscaled | 0.40 | 52% | 0.00 | 4.6% | −11.4% | −6.9% |
| 10-day half-life | 0.48 | 71% | 4.66 | 1.7% | −8.3% | −6.1% |
| 20-day half-life | 0.49 | 70% | 2.39 | 1.8% | −9.0% | −6.4% |
| 40-day half-life | 0.50 | 69% | 1.22 | 1.9% | −9.6% | −6.5% |
| 60-day half-life | 0.51 | 68% | 0.82 | 2.1% | −9.9% | −6.6% |
| 90-day half-life | 0.51 | 67% | 0.56 | 2.2% | −10.1% | −6.7% |

The faster filter sacrifices slightly more gross Sharpe but delivers the strongest tail compression and risk stabilization, with more turnover. Slower filtering does not dominate simply because its rounded Sharpe is higher. The unscaled mean of the best 1% of monthly observations is 11.8%; the 20-day scaled version reduces it to 7.3%. Both tails are compressed, so this is not equivalent to a free put option protecting only losses.

For the default 20-day strategy, regression of scaled daily returns on unscaled returns gives a daily intercept of 0.64 basis point, Newey–West $t=3.05$ using 30 lags, and $R^2=0.73$ (footnote 14). This is the paper's reported inferential support for the equity improvement. It is a spanning-regression alpha test, not a direct independent-observation test of the difference between overlapping monthly Sharpe ratios. The repeated overlapping observations should not be counted as independent when constructing uncertainty measures.

Across the broad equity subperiods and ten industries, the reported Sharpe improvement is widespread, except for the middle historical subperiod. Volatility stability and shortfalls improve more consistently. The exact maximum-drawdown and higher-moment analyses are assigned to the unavailable supplements; the main article states the direction but does not provide all numerical values. There is no basis here for inventing them.

For 1988–2017 S&P 500 futures, Exhibit 8 gives an unscaled Sharpe of 0.50, vol of vol 3.8%, and 1% shortfall −11.2%. The default daily 20-day rule gives 0.59, 1.2%, and −8.4%, with 84% mean exposure and turnover 2.31. A 15-day intraday smoother gives Sharpe 0.62, vol of vol 1.4%, shortfall −8.3%, exposure 85%, and turnover 1.52. A 25-day intraday smoother gives Sharpe 0.63, volatility instability 1.5%, shortfall −8.7%, and turnover 0.97. Comparisons should match approximate turnover or response speed, rather than pair arbitrary half-life labels across daily and realized-variance estimators.

## Treasury and cross-asset evidence

The long historical Treasury sample is an important counterexample. Exhibit 11, 1963–2017, reports unscaled Sharpe 0.25. The default 20-day scaled version has Sharpe 0.06, mean exposure 179% versus 127%, and turnover 2.51. Vol of vol improves from 3.9% to 2.1%, but the worst-1% mean worsens from −8.4% to −8.9%, and the worst-5% mean from −5.9% to −6.3%.

The explanation is that the pre-1980 bond bear market combined low measured volatility with poor returns. Scaling increased exposure in that low-risk-looking regime. Across half-lives the scaled Sharpe ranges only from 0.05 to 0.09 before costs. This shows that lower volatility instability does not guarantee better Sharpe or better average tail returns. The article's broad statements about improving tail behavior must be read with this displayed exception in view.

The authors argue that pre-mid-1980s monetary regimes may be less representative of the later bond market, while acknowledging that the more recent sample itself largely contains declining rates. This is a regime qualification, not permission to discard an unfavorable historical period after seeing its performance. They also note that sovereign bonds can behave more like credit if creditworthiness becomes questionable; the cross-asset conclusion is not invariant to a country's risk regime.

For 1988–2017 ten-year Treasury futures, Exhibit 13 gives unscaled Sharpe 0.64 and vol of vol 2.5%. The daily 20-day rule gives 0.63 and 1.2%; the 1% shortfall is −7.5% versus −7.3% unscaled. Mean exposure rises from 171% to 182%, with turnover 2.19. Intraday filtering brings modest improvements: the five-day realized-variance version has gross/net Sharpe 0.66/0.65 and vol of vol 1.1%, but turnover 3.80. The result is primarily smoother risk, not a substantial reward enhancement.

Exhibit 15 extends the 20-day comparison to 50 futures/forward instruments plus hedged credit. Equity indices and credit show some Sharpe improvement; commodities, currencies, and fixed-income instruments show little systematic change. Volatility instability and left-tail measures improve for most instruments. Individual numerical observations are plotted rather than fully tabulated, so the source supports the category-level pattern more strongly than precise contract-specific estimates.

## Two-stage portfolio targeting

Construct each asset return at 10% full-sample volatility, then combine equity and Treasury futures with weights 0.60 and 0.40. Compare three versions: both asset and aggregate portfolio unscaled; individual assets dynamically scaled but aggregate portfolio unscaled; and dynamic scaling at both levels. Daily rebalancing to the target mix is assumed. The portfolio-level filter again uses a 20-day half-life.

If $u_{i,t}$ denotes the normalized component return, the first portfolio is $p_t=0.6u_{E,t}+0.4u_{B,t}$. In the second, replace each component by its dynamically scaled return before combining. In the third, multiply that combined return by a lagged inverse forecast of its own volatility. The second stage responds to changing aggregate risk, including correlations left uncontrolled by equalizing individual asset volatility. The article does not separately estimate a multivariate correlation model for this step.

Exhibit 16 gives gross Sharpe ratios 0.80, 0.87, and 0.91; corresponding net ratios are 0.80, 0.87, and 0.90. Vol of vol falls from 3.4% to 2.2% to 1.3%. Worst-1% average monthly returns improve from −9.7% to −8.0% to −7.3%, and worst-5% averages from −6.0% to −5.6% to −5.5%. Mean notional exposure rises from 153% to 179% to 183%; turnover is 0.00, 2.24, and 3.95. Best-1% averages fall from 9.7% to 8.7% to 8.0%.

The equal-volatility preparation explains why this is not a standard capital-weighted balanced portfolio. Its ex post normalizations also affect relative asset exposure. A practitioner testing a literal 60/40 capital allocation must construct and label that as a different experiment. A four-asset equity/bond/credit/commodity risk-parity portfolio is discussed, but its detailed results are in the separate supplement and cannot be reconstructed numerically from the main article alone.

## Mechanism, replication boundaries, and takeaways

Exhibit 18 compares monthly returns with the same month's variance and its change. Equity and credit show the negative association described as the leverage effect; other groups generally do not. These are contemporaneous relations, not causal estimates. Corporate leverage and volatility-feedback explanations are both discussed, and the article does not statistically distinguish them.

Exhibit 19 correlates inverse volatility with past 21-, 65-, 130-, and 260-day returns. With the 20-day filter, equity and credit exposure adjustments tend to align with momentum. For many other assets the correlation is negative, resembling mean reversion. Exhibit 20 then relates each asset's Sharpe improvement to the correlation between past 21-day returns and inverse volatility. The cross-sectional $R^2$ is 45% for the 20-day filter and 60% for a 90-day filter. These percentages describe fit across asset-level historical results; they are not the fraction of an individual strategy's return variance explained by a tradable momentum factor.

For replication, the necessary core pipeline is well specified: construct unfunded returns, align calendars, initialize a zero-mean EWMA, lag the scaling signal by two days, apply the chosen half-life, normalize compared series to equal sample risk, build overlapping evaluation returns, and compute tail averages, volatility instability, exposures, turnover, and stated cost deductions. Portfolio comparisons add daily mixing of normalized components and an optional second filter. The principal unresolved inputs are the exact contract data and rolls, credit hedge, finite-history EWMA treatment, holiday handling, and some return-aggregation conventions.

The inspected article does not supply executable code, a complete dataset, bootstrap confidence intervals for every Sharpe or tail comparison, or an out-of-sample optimization protocol. Its constant post-crisis cost assumptions and full-sample normalizations limit interpretation as a deployable historical simulation. The conclusions remain economically useful when stated narrowly: risk targeting can stabilize a portfolio even when it adds no mean-variance efficiency; equity and credit benefits are linked to their specific return-volatility relation; and reducing both tails is a change in payoff distribution that should be assessed alongside leverage, turnover, and regime exposure.

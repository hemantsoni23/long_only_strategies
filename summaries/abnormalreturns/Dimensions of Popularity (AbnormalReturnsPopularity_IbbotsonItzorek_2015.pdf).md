# Dimensions of Popularity

Roger G. Ibbotson and Thomas M. Idzorek, The Journal of Portfolio Management, special 40th anniversary issue, 40(5), 2014, pp. 68–74. Source: [AbnormalReturnsPopularity_IbbotsonItzorek_2015.pdf](../../Finance/AbnormalReturnsPopularity_IbbotsonItzorek_2015.pdf). The basename's 2015 refers to the stored/downloaded file; the article itself is dated 2014.

## Why this matters and the proposed contribution

The authors propose popularity as a broad organizing concept for asset prices and return premiums. Investors may pay for safety, liquidity, familiarity, favorable company narratives, transparency, or freedom from institutional inconvenience. An asset can then offer a lower expected financial return because it delivers desirable nonreturn attributes. Conversely, an investor unusually willing to bear unpopular attributes may obtain compensation. The proposal connects persistent equilibrium premiums with transitory behavioral overpricing without claiming that every premium must be compensation for volatility or market beta.

The article's distinctive empirical illustration is a stock-turnover sort and its cross-classification with beta and volatility. The low-turnover portfolios earn higher reported returns even within risk quartiles. This supports the usefulness of turnover as a descriptive characteristic in the sample. It does not separately identify popularity, liquidity compensation, mispricing, or a causal preference mechanism.

## Economic mechanism and distinctions

Holding expected future payoffs fixed, stronger demand for a desirable characteristic raises price and lowers prospective financial return. This is the logic behind the popularity–return relation. Risk is one undesirable characteristic, but the authors resist treating every dislike as conventional variance or beta risk. A taxable income stream can be unattractive to a taxable investor even without greater return volatility. An illiquid asset can be inconvenient to an investor who may need cash, while a patient investor may tolerate the same inconvenience.

The equilibrium interpretation allows these return differences to persist after discovery: investors continue to value liquidity, tax treatment, or convenience, so they need compensation to hold less desirable assets. Clienteles matter. A tax-exempt investor may not require the same compensation for taxable income; a long-horizon holder may assign little value to immediate saleability. Such a return advantage is not automatically an exploitable arbitrage for every investor.

The behavioral interpretation adds attention, overconfidence, herding, and temporary fads. A security may become expensive because investors like its story too much, with subsequent underperformance as enthusiasm corrects. A rise in popularity can also generate price appreciation for a current holder. Therefore the level of popularity and changes in popularity have different implications: buying an unpopular asset may offer a premium, while owning an asset that subsequently becomes more popular may add a revaluation gain.

The paper gives no formal utility function, market-clearing system, law of motion for popularity, or numerical equilibrium solution. The concept is intentionally broad. Its explanatory flexibility is also a limitation: identifying dislike from realized underperformance after the fact would make the story difficult to falsify. An implementable test needs a popularity definition fixed before observing subsequent returns.

## How the framework classifies familiar premiums

The equity premium mainly compensates for the unpopularity of risk. The liquidity premium compensates investors for giving up immediate tradability, potentially even when beta or volatility is not larger. Small-company premiums can combine risk, liquidity, and institutional search or capacity costs. A manager may undertake similar research effort for a small company while being unable to deploy as much capital as in a large company.

Value stocks can be unattractive because they are distressed, poorly managed, mature, or lacking compelling growth narratives. The authors stress that a good company is not necessarily a good investment at any price: expectations embedded in the price matter. Low-beta and low-volatility effects can arise if leverage-averse investors or benchmarked managers favor high-beta stocks as a substitute for borrowing. In that case investors like exposure to certain risks strongly enough to depress their expected returns.

Momentum receives a different treatment. The authors suggest that gradual migration in popularity may produce trends, interpreting momentum as a transition or shorter-term popularity wave rather than a stable premium for a permanently disliked attribute. This is a conjectural explanation, not a momentum model with estimated transition speeds or a new momentum backtest. The paper's cited literature supplies background; its own displayed results concern turnover and risk sorts.

## Observable proxy and sample construction

The authors propose share turnover as one measurable popularity proxy because scaling volume by shares outstanding separates activity from company size. A large stock can be easy to trade in dollar terms but have relatively low turnover. Analyst coverage, news presence, and brand familiarity are other suggested indicators, but are not separately tested in the article's exhibits.

The reported empirical universe is the largest 3,000 US stocks. Stocks are ranked using the previous year's turnover, with results covering 1972–2013. Exhibit 1 reports popularity quartiles. Exhibits 2 and 3 independently sort the universe into turnover quartiles and beta or volatility quartiles and then report the intersections. These results are credited to Ibbotson and Kim's 2014 working papers, rather than a fully documented data appendix in this article.

The source does not specify the database, exact volume normalization across exchanges, averaging window within the previous year, portfolio weights, rebalancing dates, size-universe refresh rule, delisting handling, beta-estimation benchmark and window, or volatility window. It also supplies no transaction-cost model, turnover of the strategy itself, or out-of-sample holdout. The one-year lag in the ranking input should not be silently replaced with contemporaneous trading activity.

A schematic turnover signal is shares traded divided by shares outstanding over a defined observation period. That expresses the concept only; the article does not provide the exact aggregation convention needed to reproduce every number. A reproduction must obtain those details from the cited working papers or disclose implementation choices as an extension.

## Numerical results

Exhibit 1, printed p. 72, reports the following annualized returns and standard deviations:

| Turnover/popularity quartile | Q1, least popular | Q2 | Q3 | Q4, most popular |
|---|---:|---:|---:|---:|
| Annualized return | 15.51% | 14.42% | 12.80% | 8.27% |
| Standard deviation, percent units | 20.18 | 20.66 | 22.74 | 28.35 |

The return spread between Q1 and Q4 is 7.24 percentage points annually, calculated from the exhibit. Lower popularity is associated with both higher reported return and lower volatility in this sort. The article does not report whether annualized return means compound growth or annualized arithmetic mean, nor a standard error for the spread. A difference between two long-only portfolio growth rates is not automatically the realized return of a self-financing long–short implementation.

Exhibit 2 cross-sorts by beta. Columns below run from least to most popular:

| Beta quartile | Q1 popularity | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| Lowest beta | 15.3% | 14.4% | 11.9% | 3.4% |
| Q2 beta | 16.3% | 15.0% | 13.8% | 10.5% |
| Q3 beta | 13.7% | 14.7% | 13.3% | 9.9% |
| Highest beta | 11.4% | 12.0% | 10.5% | 6.4% |

Within every beta row, the least-popular endpoint beats the most-popular endpoint. The corresponding endpoint spreads are 11.9, 5.8, 3.8, and 5.0 percentage points. Beta itself does not produce a uniform monotone ordering within each popularity column. The first and last columns, for example, do not both favor the lowest-beta row relative to the highest-beta row. These are descriptive interactions, not regression estimates adjusted for all competing characteristics.

Exhibit 3 repeats the exercise using volatility:

| Volatility quartile | Q1 popularity | Q2 | Q3 | Q4 |
|---|---:|---:|---:|---:|
| Lowest volatility | 14.1% | 14.0% | 12.7% | 10.9% |
| Q2 volatility | 15.6% | 14.4% | 13.9% | 12.1% |
| Q3 volatility | 16.1% | 15.4% | 13.5% | 10.4% |
| Highest volatility | 14.9% | 14.1% | 8.7% | 2.6% |

Returns decrease monotonically with popularity within each volatility row. The largest endpoint spread, 12.3 percentage points, occurs in the highest-volatility row. Within the lowest-popularity column, the highest-volatility portfolio returns 14.9%, compared with 14.1% for the lowest-volatility portfolio. Thus these displayed sorts cannot be reduced to a simple claim that low turnover wins only by selecting low volatility. They still do not establish independence from every other characteristic or a structural popularity factor.

## What can and cannot be inferred

There are no reported significance tests, confidence intervals, multiple-testing corrections, factor-regression alphas, subsample stability statistics, or trading-cost-adjusted returns for these exhibits. Equivalent size and valuation analyses are said to support the same story but are omitted. A reader cannot audit their magnitudes from this source. Results credited to related liquidity research should not be attributed as new estimates conducted in this article.

A useful replication would preserve the lagged turnover ranking, reproduce the single and independent double sorts, and then examine size, valuation, exchange conventions, liquidity costs, and sensitivity to portfolio weighting. That proposed sequence is a way to test the mechanism rather than a protocol fully reported by the authors. It should distinguish gross characteristic returns from net implementable returns and separate a durable inconvenience premium from a correction of temporary overvaluation.

The main takeaway is a research agenda: characterize what investors value beyond conventional risk, measure those attributes independently of future performance, and ask which investors can bear unpopular attributes cheaply. The numerical exhibits motivate that agenda; they do not prove that one universal popularity variable has replaced risk-based pricing or that every low-turnover portfolio will outperform.

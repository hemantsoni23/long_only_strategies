# How Active Is Your Fund Manager? A New Measure That Predicts Performance

K. J. Martijn Cremers and Antti Petajisto, *The Review of Financial Studies* 22(9), 2009, pp. 3329–3365, DOI 10.1093/rfs/hhp057. [Original PDF](../../Finance/PerformanceAttributionActiveShare_CremersPetajisto2009.PDF), 37 pages including the appendix and references. This is the original joint-author Active Share paper; Petajisto’s later 2013 study of Active Share and mutual-fund performance is a distinct extension.

## Why this matters

A fund can trade frequently yet remain close to its benchmark, or hold a very different set of stocks while maintaining low benchmark-relative volatility through diversification. Cremers and Petajisto introduce Active Share to measure how different the actual holdings are. They combine it with a return-based risk measure to distinguish diversified stock selection, concentrated stock selection, factor bets, and closet indexing.

Their 1990–2003 performance tests find a substantial difference between high- and low-Active-Share funds. The net annual benchmark-adjusted return spread is 2.55 percentage points, with a reported $t$-statistic of 3.47. A four-factor regression of those benchmark-adjusted returns increases the spread to 2.98 points, with $t=4.51$. Low-Active-Share nonindex funds consistently underperform after costs.

Two qualifications are essential. First, the high-Active-Share group’s standalone net outperformance is 1.13% annually with $t=1.60$, or 1.15% with $t=1.86$ after the additional factor adjustment. Those estimates are weaker than the highly significant high-minus-low spread and do not individually clear a conventional two-sided 5% threshold. Second, ordinary Carhart alphas calculated directly on fund returns over cash show no significant high-minus-low relation. The result is explicitly about performance relative to the holdings-matched benchmark, with important evidence on benchmark dependence rather than an invariant measure of manager skill.

## The measure and its exact interpretation

Let $w_i$ denote the fund’s weight in stock $i$ and $b_i$ the benchmark weight. Use the union of holdings: a stock missing from one portfolio has zero weight there. Active Share is

$$
AS(w,b)=\frac12\sum_{i=1}^{N}|w_i-b_i|.
$$

When both long-only weight vectors sum to one, this is also

$$
AS=1-\sum_i\min(w_i,b_i)
=\sum_{i:w_i>b_i}(w_i-b_i)
=\sum_{i:w_i<b_i}(b_i-w_i).
$$

These identities follow because active weights $a_i=w_i-b_i$ sum to zero, so total positive and negative deviations are equal. The fund can be written as the full benchmark plus a self-financing active portfolio whose long and short sides each have size $AS$. The factor one-half avoids counting both sides twice.

For example, take an equal-weighted 500-stock benchmark and a fund equally invested in 50 of those stocks. The retained stocks have benchmark mass 10%, and the overlap is 10%, so Active Share is 90%. With capitalization weights, the relevant quantity is weight overlap, not the fraction of stock names excluded. Fifty holdings need not imply 90% Active Share in a real index.

For fully invested, unlevered long-only portfolios, $AS$ lies between zero and one. Leverage and actual short positions can produce values above one. A nonzero value is necessary for a holdings-based return difference from the benchmark, but not sufficient for a positive expected difference. Large active positions can lose money just as readily as they can earn it.

The empirical application sums over stock positions, treating the selected funds as all-equity portfolios. The paper notes that a general multiasset application should include cash, bonds, and underlying exposures embedded in derivatives. Exact treatment of unmatched stocks, cash, and the denominator used to normalize the observed equity sleeve is not fully specified. The zero-sum identities above require equal total weight on the compared asset universe; omitting cash while retaining net-asset-value weights can break that premise. A replication should make the normalization explicit and test its consequences.

## Tracking error is modified in this study

The conventional definition is $\operatorname{SD}(R_p-R_b)$. The authors instead regress daily fund returns over cash on daily benchmark returns over cash:

$$
R_{p,d}-R_{f,d}=\alpha+\beta(R_{b,d}-R_{f,d})+\varepsilon_d,
\qquad TE=\operatorname{SD}(\varepsilon_d).
$$

They annualize this residual volatility. The lookback is the six months before the holdings report date, with at least 100 trading days required. The precise annualization day count and residual degrees-of-freedom convention are not printed.

This modified measure removes a stable benchmark beta different from one. A persistent cash allocation or low-beta tilt does not mechanically raise it in the way it raises conventional tracking error. Under regression orthogonality,

$$
\operatorname{Var}(R_p-R_b)
=(\beta-1)^2\operatorname{Var}(R_b-R_f)+\operatorname{Var}(\varepsilon).
$$

Thus reproducing the tables with the plain standard deviation of active returns would change the sorting variable.

Active Share measures absolute holding deviations without a covariance matrix. Tracking error depends on covariance and therefore emphasizes correlated bets. High Active Share with modest residual risk can describe diversified stock selection; high residual risk with lower Active Share can describe factor bets. These are economic proxies, not an exact identification theorem: residual risk still includes stock-specific risk, and holdings deviations can reflect systematic styles.

Industry-level Active Share replaces stock weights by weights in ten industry portfolios. The Industry Concentration Index instead squares industry active weights:

$$
AS_{\rm industry}=\frac12\sum_{g=1}^{10}|w_g-b_g|,
\qquad ICI=\sum_{g=1}^{10}(w_g-b_g)^2.
$$

Grouping cannot increase the absolute deviation, because the triangle inequality gives $AS_{\rm industry}\le AS_{\rm stock}$. This derived inequality formalizes why within-industry bets can produce high stock-level Active Share while industry exposure stays modest. The appendix relates tracking error to squared active weights under equal residual-volatility assumptions. To obtain $TE^2=\sum_i a_i^2\sigma_{\varepsilon i}^2$, residual cross-covariances must also be zero; otherwise the off-diagonal terms remain.

## Data construction and sample filters

Fund holdings come from Thomson Financial’s CDA/Spectrum database, based on mandatory filings and voluntary disclosures, beginning in 1980. Fund and index holdings are matched to CRSP stocks. Monthly fund returns come from CRSP and are net of expenses, fees, and brokerage commissions, but exclude front-end and back-end sales loads. Index total returns include dividends.

Daily fund data come primarily from S&P’s Micropal/Worths system. Because that source contains live funds, the authors supplement it with CRSP daily returns from January 2001 and the Wall Street Web data used by Goetzmann, Ivkovic, and Rouwenhorst for earlier dead funds. They prefer S&P when overlapping sources are available. A reconstruction therefore needs source-priority rules and identifier links as well as monthly returns.

The CRSP–Spectrum mapping combines two existing mappings and resolves conflicts manually. Share-class assets are summed to obtain fund assets. Expenses, loads, turnover, and stock percentages are asset-weighted across classes; other variables are taken from the largest class. The PDF does not give a separate fully explicit return aggregation algorithm for every share-class case, so a replication must verify rather than assume that all data fields use the same averaging rule.

The filters admit domestic equity objectives, including the source’s permitted unclassified or missing codes, and exclude balanced, allocation, international, precious-metal, and sector funds. The time-series average CRSP stock percentage must be at least 80% or missing. Matched Spectrum equity holdings must also meet the 67%-of-reported-assets threshold. This lower second threshold accommodates incomplete CRSP stock matching while removing portfolios insufficiently represented by domestic equities.

Holdings must be dated at month-end to align with index constituents. The 100-daily-return requirement reduces the sample by 5.4%, mostly in the 1980s. To reduce incubation bias, observations before the CRSP reported starting year and those with missing fund names are removed. Equity holdings must exceed \$10 million.

The final 1980–2003 sample contains 2,647 funds and 48,354 fund-report-date observations, about three holdings reports per fund per year. These are distinct counts: 2,647 is not the number simultaneously available each month. The 2002 cross-sectional table contains 1,678 funds; the time-series discussion reports 2,026 funds in 2003. The paper describes 2002 as its last complete year for the cross-sectional snapshot.

## Benchmark assignment and its consequences

The authors compare each fund’s holdings with nineteen indexes and select the one producing the smallest Active Share:

$$
b^*(p,t)=\arg\min_{b\in\mathcal B_t}AS(w_{p,t},b_t).
$$

The set comprises S&P 500, its Barra growth and value components, S&P 400, S&P 600; Russell 1000, 2000, 3000, and Midcap, each with growth and value versions; and Wilshire 5000 and 4500. It covers broad capitalization and style alternatives rather than forcing every fund to use the S&P 500.

S&P 500 constituents begin in January 1980; S&P 400 in July 1991; S&P 600 in December 1994; and the large-cap S&P/Barra styles in September 1992. Russell constituent data begin in December 1978 and Wilshire in January 1979. The authors use backdated constituent information where available, reconstruct Wilshire 4500 before 1983, and infer intermediate month-ends from backdated quarterly Russell constituents before 1987. They state that this affects the 1980s descriptive evidence but not the performance tests beginning in 1990.

The method is transparent and can update as a fund changes style. It does not necessarily recover the fund’s legally declared benchmark: it estimates an economically similar benchmark from the candidate set. Split benchmarks are not considered. Minimum-distance matching also builds a degree of benchmark fit into the measured Active Share. A different candidate set can change both the activity ranking and the return that is later subtracted.

For performance tests, a fund must have reported holdings within the preceding twelve months. The paper describes monthly sorting using the available holdings measure, but it does not fully specify a real-time filing-publication lag or the exact monthly treatment of holdings aging and benchmark changes. An executable strategy must distinguish the portfolio report date from the date investors could actually observe the filing.

## What the descriptive evidence establishes

In 2002, funds with 4%–6% annual residual tracking error have Active Share ranging from about 30% to 100%. Conversely, funds with Active Share of 70%–80% occupy tracking-error categories from 2% to above 14%. The measures are related but not interchangeable. Cells with fewer than five observations are suppressed; an empty table cell is not evidence of a zero count.

The paper treats values below roughly 20% as index-like, and discusses nonindex funds with 20%–60% as closet indexers. These are descriptive thresholds, distinct from the monthly quintile breakpoints in the return tests. Index funds are identified through Active Share sorting and names containing “index” or “idx”; the PDF does not provide a complete classification file or every exception rule.

Expenses offer a concrete economic motivation. The 2002 equal-weighted average expense ratio is 1.24%, versus 0.89% asset-weighted. The lowest Active Share/tracking-error group averages 0.47% equally weighted and 0.22% asset-weighted. Funds with 90%–100% Active Share charge 1.42%, while those with 30%–40% charge 1.08%. Closely tracking an index does not automatically bring an active fund’s fee near an index fund’s fee.

Average turnover is 94.8% annually. Its Pearson correlation with Active Share is only 18%, and rank correlation is 17%. Table 2 describes turnover as the maximum of purchases and sales divided by net assets; reproducing that printed definition should be distinguished from independently validating the underlying CRSP field convention. Trading frequency measures revisions to positions, whereas Active Share measures their size relative to the benchmark. The appendix contrasts a concentrated fund with 86% Active Share and 25% turnover with an index fund’s 30% turnover.

For nonindex large-cap funds, a Gaussian-kernel regression of Active Share on log assets, bandwidth 0.5, finds only a gradual decline up to approximately \$1 billion. Estimated marginal Active Share remains around 70% for much of that range, then falls toward 60% at \$10 billion and about 50% for the largest funds. This is a cross-sectional derivative, not a direct experiment observing how every fund invests its next dollar. The paper uses it to question a model in which all marginal inflows are indexed after the optimal active size is reached.

Table 3 explains Active Share using fund-year observations from 1992–2003, selecting the last holdings report of each year. Controls include tracking error, turnover, fees, size and squared size, holdings count, fund age, manager tenure, prior flows, and prior benchmark and active returns. Most specifications include year effects; standard errors cluster by fund. The broadest model explains about 32% of the variation. Tracking error is strongly related, turnover is not, and fees have a statistically detectable but modest economic association. The regressors are partly endogenous, so these are descriptive relationships rather than causal effects.

Over 1980–2003, assets in funds below 60% Active Share rise from 1.5% to 44.8%; assets above 80% fall from 42.8% to 23.3%. Index funds reach 15.3% of assets in 2003. For nonindex S&P 500-benchmarked funds, aggregate Active Share is only about 30% in later years versus a fund-level asset-weighted average near 55%–60%.

This difference is mathematically natural. If $\pi_f$ are fund asset shares and all funds share benchmark $b$,

$$
AS\left(\sum_f\pi_fw_f,b\right)
\le\sum_f\pi_fAS(w_f,b).
$$

Opposite active bets cancel within the aggregate. The evidence concerns the selected common-benchmark subgroup, not an unrestricted aggregation of all styles against one index.

Active Share is persistent: the top decile’s average rank is 9.67 after one year and 8.88 after five; the bottom decile moves from one to 1.27 and 2.08. This persistence describes portfolio style, not by itself persistence in abnormal returns.

## Performance design and estimands

The performance sample is 1990–2003 and excludes index funds. Every month, the authors sort first on Active Share and then within each quintile on tracking error, producing 25 portfolios. They compute equal-weighted returns after subtracting each fund’s assigned index. The principal portfolio return is therefore

$$
y_{g,t}=\frac1{n_{g,t}}\sum_{f\in g,t}\left(R_{f,t}-R_{b^*(f,t),t}\right).
$$

The four-factor adjustment regresses that active return on the market excess return, SMB, HML, and momentum:

$$
y_{g,t}=\alpha_g+\beta_{m,g}MKT_t+\beta_{s,g}SMB_t
+\beta_{h,g}HML_t+\beta_{u,g}UMD_t+e_{g,t}.
$$

There is no additional subtraction of the risk-free rate from $y$: it is already a difference between two fully invested returns. Tables report annualized returns and alphas, with $t$-statistics based on White heteroskedasticity-robust standard errors. They do not describe a Newey–West lag correction for these portfolio time series. Any arithmetic monthly-to-annual conversion and precise small-sample settings should be recorded in a reconstruction; the paper does not give implementation code.

Net returns are actual investor return series after recurring expenses and transaction costs, but before sales loads. Gross returns are hypothetical returns on disclosed stock holdings. They are not simply net returns plus the expense ratio: holdings-based returns omit interim trades, other assets, and unobserved actions. Exact holdings carry-forward and corporate-action rules are required to reproduce them. The paper discusses the resulting return gap and attributes part of the spread to unobserved actions, without supplying those actions individually.

## Main performance results

The marginal Active Share quintiles give the following annual percentages:

| Performance measure | Highest AS | Lowest AS | High minus low |
|---|---:|---:|---:|
| Net benchmark-adjusted mean | 1.13 ($t=1.60$) | −1.42 ($t=-3.53$) | 2.55 ($t=3.47$) |
| Net factor alpha after benchmark subtraction | 1.15 ($t=1.86$) | −1.83 ($t=-5.01$) | 2.98 ($t=4.51$) |
| Gross holdings benchmark-adjusted mean | 2.40 ($t=2.80$) | 0.11 ($t=0.29$) | 2.29 ($t=3.05$) |
| Gross holdings factor alpha after benchmark subtraction | 1.51 ($t=2.23$) | −0.63 ($t=-1.73$) | 2.13 ($t=3.29$) |

The last spread differs from subtraction of rounded cells by one basis point. These are portfolio-level statistics, not a claim that every high-Active-Share fund outperforms. The average fund has net benchmark-adjusted return −0.43% and benchmark-adjusted four-factor alpha −1.14%.

The spread is positive within all tracking-error quintiles. Reversing the sort order, using monthly rather than daily tracking error, and splitting 1990–1996 from 1997–2003 give qualitatively similar findings. Tracking error itself has little positive predictive power and sometimes a negative relation to performance. Still, Table 4 does not establish a monotonic benefit from tracking error even among high-Active-Share funds: the fourth tracking-error quintile has net alpha 2.72%, while the highest has only 0.29%.

Table 6 sorts first on size and then on Active Share. Median assets in the five size groups are \$28 million, \$77 million, \$184 million, \$455 million, and \$1.6 billion. The benchmark-adjusted net alpha spreads across Active Share are 3.78%, 3.20%, 3.05%, 1.83%, and 1.01%, with respective $t$-statistics 3.74, 3.22, 3.75, 2.51, and 1.43. The final spread is not statistically significant at conventional levels. For the largest size group, even the high-Active-Share portfolio has alpha −0.67%, emphasizing the difference between outperforming low-Active-Share peers and outperforming the benchmark.

## Persistence conditional on activity

Table 7 sorts first on Active Share and then on prior twelve-month benchmark-adjusted gross return, requiring at least nine months of that return history. Within the highest Active Share quintile, prior winners subsequently have net benchmark-adjusted return 5.10% annually, $t=3.67$, and four-factor alpha 3.50%, $t=3.29$. The winner-minus-loser spread is 6.81% before factor adjustment and 4.48% after it, the latter with $t=3.06$.

Within the lowest Active Share quintile, the factor-adjusted winner-minus-loser spread is only 0.47%, $t=0.70$. Momentum adjustment therefore eliminates the corresponding persistence evidence there, but not among the most active funds.

Restricting to below-median fund size raises the high-activity prior-winner return to 6.49%, $t=4.40$, and alpha to 4.84%, $t=4.04$. These figures come from increasingly selected historical portfolios. They should not be presented as the expected return of an arbitrary contemporary fund or as an independent out-of-sample validation. Sorting on gross holdings returns also requires that those holdings and returns be available at the decision date.

## Benchmark adjustment changes the answer

Table 8 runs the ordinary Carhart model on net fund returns minus the risk-free rate. The high-Active-Share group has alpha −0.25% and the low group −0.47%; the reported spread is 0.23%, $t=0.21$. Thus the simple sort does not demonstrate a significant relation under that estimand.

The corresponding benchmark portfolios have alphas −1.40% for high-Active-Share funds and +1.35% for low-Active-Share funds. Their spread is −2.75%, $t=-2.53$. For common regression observations and factors, linearity of OLS gives the exact decomposition

$$
\alpha(R_p-R_b)=\alpha(R_p-R_f)-\alpha(R_b-R_f).
$$

The reported spread therefore satisfies approximately $0.23-(-2.75)=2.98$ percentage points. Benchmark subtraction accounts algebraically for the difference between the two findings; it is not a minor adjustment that leaves the economic interpretation unchanged.

The authors favor the assigned passive benchmark because it represents an investor’s investment alternative and because their factor model assigns nonzero alphas to major passive indexes. They report S&P 500 alpha +1.08%, $t=2.72$, and Russell 2000 alpha −2.73%, $t=-2.58$. This motivates their model-misspecification concern. It does not prove that every matched benchmark is uniquely correct or that all benchmark-relative outperformance is pure security-selection skill. A robust use of Active Share should report both benchmark-relative and model-relative results.

## Multivariate predictive evidence

Table 9 predicts next calendar year’s performance using prior year-end characteristics. It uses 1992–2003, because some covariates are unavailable earlier, includes year effects, and clusters standard errors by year. Models using ordinary factor alpha or characteristic selectivity also include benchmark indicators. This clustering differs from the fund clustering in the descriptive Active Share regressions.

The benchmark-adjusted alpha coefficient on Active Share is 0.0722 with $t=2.53$ in column 1. A 0.30 increase in Active Share corresponds to $0.30\times0.0722=0.02166$, or 2.17 percentage points in next-year alpha. The prose below the table gives $t=2.42$ for this coefficient, whereas the visually checked table places 2.42 in column 2 and 2.53 in column 1; this note follows the table.

With a below-median-size interaction, the base coefficient is 0.0666 and the incremental coefficient 0.0139. Their sum times 0.30 gives 2.415 percentage points for small funds. Expense ratios have strongly negative coefficients, while turnover is insignificant. These associations control for many observed characteristics but do not constitute random assignment of a fund’s Active Share.

Under ordinary excess-return alpha with benchmark indicators, the Active Share coefficient is 0.0496, $t=1.89$, and the evidence weakens. Under characteristic selectivity, a gross holdings-based measure, the stronger result is again concentrated among smaller funds. The characteristic-benchmark matching procedure is delegated to Daniel and coauthors rather than fully specified in this paper.

Table 10 adds competing activity measures jointly. With the full controls, benchmark-adjusted alpha has Active Share coefficient 0.0612, $t=2.11$, plus a small-fund interaction 0.0141, $t=2.40$. Ordinary excess-return alpha, however, has base Active Share coefficient 0.0172, $t=0.73$, with a positive small-fund interaction. The evidence is consequently stronger for the benchmark-relative question and for smaller funds, not uniform across definitions and sizes. With only twelve calendar-year clusters in the 1992–2003 predictive tests, asymptotic clustered inference also deserves care; the PDF does not describe a small-cluster bootstrap.

## Replication priorities and limitations

A faithful implementation first reconstructs fund identifiers and share classes, applies the stated filters without imposing survival, and joins dated holdings to historical index constituents. It then computes every candidate Active Share, records the chosen index, estimates residual tracking error from the preceding six months, and maintains both report dates and actual availability dates. Unit tests should verify the overlap identity for normalized long-only weights, zero Active Share for identical portfolios, invariance to zero-weight union entries, and the industry aggregation inequality.

The monthly return pipeline should retain the 25 portfolio memberships, constituent benchmark returns, equal weights, and gross-versus-net distinction. Size and persistence sorts must use their stated sequential ordering and minimum histories. Annual regressions need separate code paths for fund-clustered descriptive models and year-clustered predictive models. Rounded table cells can check portfolio summaries, but cannot recover all classification and timing decisions.

Missing or insufficiently detailed inputs include the historical manual CRSP–Spectrum mapping, exact index-fund exceptions, security matching and delisting handling, cash and unmatched-weight normalization, daily-return cleaning, benchmark tie-breaking, reporting-delay treatment, gross holdings-return mechanics, and some factor/characteristic benchmark implementation details. These are material for exact numerical reproduction and for determining whether the portfolio sorts were executable using contemporaneously released information.

The metric records distance from an index, not research quality, information advantage, or expected alpha by definition. A benchmark-relative holding difference can reflect omitted risks or a persistent style. Report-date window dressing and changing holdings between reports are not fully observed; the paper argues that extreme window dressing would be costly but does not identify every such practice. The tests span many portfolios and specifications without an explicit multiple-testing adjustment, and their historical sample does not validate subsequent performance.

The paper’s central empirical contribution survives these distinctions: holdings-based distance adds information that turnover and residual tracking error do not contain. It exposes the cost of index-like portfolios charging active fees and identifies historical subsets with stronger benchmark-relative performance. Its use as a manager-selection signal requires the benchmark, observation timing, size, expenses, and performance definition to remain explicit.

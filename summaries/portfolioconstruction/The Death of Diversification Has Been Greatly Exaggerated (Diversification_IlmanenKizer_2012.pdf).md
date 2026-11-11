# The Death of Diversification Has Been Greatly Exaggerated

Antti Ilmanen and Jared Kizer. *The Journal of Portfolio Management*, Spring 2012, pp. 15–27. Source: [Diversification_IlmanenKizer_2012.pdf](../../Finance/Diversification_IlmanenKizer_2012.pdf), fourteen PDF pages including the final rights notice. All pages, the data appendix, endnotes, and Exhibits 1–10 were inspected. Page references below use the printed journal numbering.

## Why this matters

A portfolio spread across many asset classes can still obtain most of its risk from equity-market direction. Ilmanen and Kizer compare this familiar form of diversification with a portfolio combining equity exposure and four dynamic strategy styles. Their principal contribution is an empirical allocation comparison showing that the selected styles have much lower mutual correlations than conventional asset-class building blocks. The gross historical Sharpe ratio rises from 0.48 for their asset-diversified portfolio to 1.44 for their factor-diversified portfolio over 1973–2010.

That result has two sources: better standalone returns per unit of risk among the chosen factor strategies, and a stronger reduction in volatility when they are combined. The authors place greater confidence in the second source because trading costs, management fees, and future competition may substantially reduce the first. The paper does not discover new signals or estimate a new pricing model. It assembles previously studied premia into transparent monthly allocation rules and uses their joint behavior to challenge the claim that diversification failed during the financial crisis.

The distinction matters for implementation. The headline factor portfolio includes long-short stock selection and leveraged derivatives strategies. Replacing them with long-only stock tilts changes the exposures and lowers the benefit. Nor should its approximately 5% volatility and 17% maximum drawdown be compared with a 9% volatility traditional portfolio as if they had equal risk. The paper supplies a useful allocation experiment, but not a fully costed, capacity-constrained mandate.

## Two experiments with different data and purposes

The first experiment documents six US premia from January 1927 through December 2010: equity, size, value, momentum, term, and default. It establishes that economically distinct return streams can have low pairwise correlations over long histories. The second experiment, 1973–2010, compares implementable-style allocation building blocks: five conventional asset groups against equity plus four dynamic strategy composites. These experiments use different definitions and histories; the six long-history factors are not the five constituents of the headline factor portfolio.

All headline results are gross of trading costs and management fees. Endnote 1 says arithmetic means in every exhibit are based on annual returns, whereas other statistics use monthly data. This is essential: one cannot generally reproduce the reported arithmetic means by annualizing the sample monthly arithmetic mean, or recover the reported Sharpe ratio simply by dividing the printed annual arithmetic mean by volatility. The article's prose generally quotes geometric mean returns unless otherwise specified. Total returns and excess-return premia are also distinguished below.

No new hypothesis test or optimized allocation criterion is estimated. The core portfolio rule is equal nominal weighting and monthly rebalancing; a second rule rescales exposures using lagged realized volatility. The simplicity is intentional, avoiding a covariance optimizer that might exploit unstable sample correlations.

## Long-history premia and dependence

The equity premium is the US market return minus the one-month Treasury bill return, from Kenneth French's data library. Size is small minus large, equivalent to SMB; value is value minus growth, equivalent to HML. Momentum uses prior-year returns excluding the most recent month, equivalent to UMD. The term premium is long-term Treasury return minus the one-month bill return. Default is high-grade long-term corporate bond return minus long-term Treasury return, from Dimensional Returns 2.0 or the cited Morningstar history. The authors caution that this last series includes downgrade effects and significant measurement concerns; it is not a pure realized default compensation estimate.

Exhibit 1 gives these annualized percentages and reported risk statistics:

| Factor | Annual arithmetic mean | Geometric mean | Volatility | Sharpe | Maximum drawdown |
|---|---:|---:|---:|---:|---:|
| Equity | 8.0% | 5.8% | 19.0% | 0.39 | −85% |
| Size | 3.8% | 2.8% | 11.6% | 0.26 | −53% |
| Value | 4.9% | 3.9% | 12.4% | 0.38 | −46% |
| Momentum | 9.7% | 7.7% | 16.7% | 0.50 | −76% |
| Term | 2.2% | 1.8% | 8.3% | 0.26 | −59% |
| Default | 0.3% | 0.2% | 4.6% | 0.06 | −36% |

These standalone drawdowns show why a positive long-run premium is not sufficient for portfolio design. Momentum's reported skewness is −3.03 and kurtosis 26.54. The table does not clearly specify a universal kurtosis normalization across all presentations, so values should be identified as printed rather than re-labeled as Gaussian-adjusted measures without checking the underlying computation.

The average of the fifteen pairwise correlations is −0.03, with median 0.04. Notable values are equity–size 0.33, equity–momentum −0.34, value–momentum −0.40, and term–default −0.44. Rolling 60-month average pairwise correlation ranges from approximately −0.14 to +0.19, without an obvious trend. Conditional on the worst quartile of equity-return months, the average remains −0.03.

The lower feasible average correlation for six standardized variables is −1/5=−0.20, because the variance of their sum must be nonnegative. This explains the source's comment that correlations close to that boundary represent substantial diversification. It does not imply that every pair has low or negative dependence, or that average correlation summarizes tail co-losses. The reported worst-equity-quartile calculation is a conditional descriptive statistic, not a proof that correlations remain benign in all crises.

## The conventional allocation benchmark

The asset-diversified portfolio resets monthly to five 20% building blocks:

| Block | Definition in the source appendix |
|---|---|
| US large-cap equities | MSCI US total return; Bloomberg GDDUUS |
| Developed equities outside the US | MSCI World ex US; GDDUWXUS |
| Global government bonds | Citigroup World Government Bond Index, hedged to US dollars; SBWGC |
| Global nongovernment bonds | Barclays Global Aggregate excluding Treasuries and government-related bonds, hedged to US dollars |
| Other | Equal quarters in US small caps, emerging-market equities, commodity futures, and global listed property |

Thus, each component inside Other has 5% of the full portfolio. Small caps use the smallest quintile of the value-weighted equity market from French's library and also stand in for foreign small caps and private equity. Emerging equities use MSCI's free index, listed as GDUUEFG. Commodities use the S&P GSCI total-return index, SPGSCITR, and also proxy natural resources. Listed property uses the Global Property Research GGENGLOB index and also proxies unlisted real estate.

These proxies deliberately broaden the economic allocation but introduce mismatches. Listed property is not an appraisal-based private-real-estate series; US small caps are not actual private-equity investments. The portfolio is described as a reasonable broad market-cap proxy, but it does not follow changing market-cap weights. Its constant allocations and monthly rebalancing make it an explicit benchmark construction rather than the realized world market portfolio.

Histories require splicing. Before 1985 the government-bond evidence is US Treasury based; before 2001 the nongovernment-bond evidence is US credit based. Emerging-market data before 1988 use narrower S&P IFC histories, and property before 1984 uses US REITs. The source does not provide every exact transition month, splice factor, missing-data treatment, or index version. These differences are especially consequential when comparing “global” histories across the whole sample.

## The dynamic factor allocation

The factor portfolio resets monthly to 20% each in US large-cap equity and four style composites. Value and momentum are global long-short stock-selection series from the cited Asness–Moskowitz–Pedersen work. Value sorts by book-to-market; momentum sorts by the past year's return excluding the most recent month. Results are averaged across the US, Japan, UK, and Europe excluding the UK. Only US value data are available before 1981.

Carry combines four currency and fixed-income yield-seeking strategies described in Ilmanen's book, chapter 13.5. Trend combines long or short positions in almost sixty liquid equity-index futures, fixed-income futures, currency forwards, and commodity futures according to past-year returns, following the cited time-series momentum work. The carry and trend universes narrow progressively before the early 1990s. Those composites already contain substantial internal diversification; the study then diversifies across composites.

The article's appendix identifies the conceptual rules and external source series, but does not reproduce the full stock breakpoints, accounting publication lags, region weighting details, exact four carry rules, complete contract list, instrument-level volatility estimates, or futures roll calendars. It is therefore possible to reproduce the allocation layer from the original component return series, but not to regenerate every component from raw prices using this PDF alone. A replication should either obtain the exact historical source series or label newly reconstructed styles as approximations.

For a style excess return $s_{j,t}$ and one-month bill return $r_{f,t}$, the paper forms a cash-backed total return $r_{j,t}=r_{f,t}+s_{j,t}$. With equal nominal weights,

$$
r_{P,t}=\frac15\sum_{j=1}^{5}r_{j,t}.
$$

Adding cash to each return series and then averaging adds one cash return to the portfolio, not five. The comparison is between total-return portfolios with consistent cash treatment. A long-short style's gross long and short exposures need not sum to its allocated capital; nominal portfolio weights at this composite level do not disclose the total leverage of underlying positions.

## Main performance comparison

Exhibits 4 and 6 report:

| Quantity, 1973–2010 | Asset-diversified | Factor-diversified |
|---|---:|---:|
| Arithmetic annual mean | 10.47% | 13.45% |
| Geometric mean | 9.85% | 13.26% |
| Annualized volatility | 9.14% | 4.99% |
| Skewness | −0.62 | −1.20 |
| Printed kurtosis | 2.37 | 5.62 |
| Sharpe ratio | 0.48 | 1.44 |
| Maximum drawdown | −36% | −17% |
| Average constituent volatility | 11.88% | 10.90% |
| Average constituent Sharpe | 0.40 | 0.70 |
| Average pairwise correlation | 0.38 | −0.02 |

For the asset portfolio, volatility is $9.14/11.88\approx77\%$ of the average constituent volatility. For factors it is $4.99/10.90\approx46\%$. The absolute reductions are 2.74 and 5.91 annualized volatility percentage points. The source's 0.48 versus 1.44 Sharpe comparison is threefold, but the study does not report a confidence interval for that ratio or a formal test of its stability.

The factor constituents' printed Sharpes are 0.31 for equity, 0.61 for value, 0.52 for momentum, 0.82 for carry, and 1.22 for trend. Their volatilities are respectively 15.86%, 8.51%, 10.04%, 10.07%, and 10.01%. Thus the nominally equal-weighted factor portfolio is not equal risk, and the equity component is more volatile than the others. Carry has notably negative skewness, −2.81, and printed kurtosis 29.77. The combined portfolio's worse standardized higher moments coexist with its smaller absolute drawdown.

Among the ten factor pairs, value–momentum correlation is −0.53. Equity correlations with value, momentum, carry, and trend are −0.04, −0.11, +0.35, and 0.00. By contrast, the conventional portfolio contains highly related equity exposures and government/nongovernment bond correlation of +0.87. The asset portfolio correlates 0.87 with US stocks. Exhibit 7 gives 0.65 for the factor portfolio's equity correlation, while the nearby prose reports 0.64; this minor source discrepancy should not be concealed by selecting an extra decimal of invented precision.

The decomposition in endnote 5 is multiplicative:

$$
\frac{1.44}{0.48}
=\frac{0.70}{0.40}
\frac{1.44/0.70}{0.48/0.40}
\approx1.75\times1.71=3.00.
$$

The first term measures relative average constituent Sharpe; the second measures relative improvement on combination. It is an informative accounting decomposition, not causal identification. With heterogeneous volatilities, Sharpe ratios, and pairwise correlations, portfolio Sharpe is not generally average Sharpe times a universal breadth multiplier. The authors explicitly qualify the analogy to four independent bets.

For equal volatilities and common correlation $\rho$, an illustrative formula is

$$
\frac{\sigma_P}{\sigma}=\sqrt{\frac{1+(n-1)\rho}{n}}.
$$

At $n=5$, $\rho=0.38$ implies a ratio about 0.710, whereas $\rho=-0.02$ implies about 0.429. These derived illustrations capture the mechanism but are not exact predictions of the reported 0.77 and 0.46 ratios because the empirical constituent risks differ.

## Crisis behavior and what it establishes

Both portfolios reach their largest reported drawdown in February 2009: −36% for assets and −17% for factors. Before 2008 their next-worst drawdowns are approximately −20% and −7%. The lower factor drawdown mostly reflects lower overall volatility, not an unqualified improvement in tail shape. Its skewness and kurtosis are less favorable, largely because of carry.

In NBER recession months the asset portfolio earns an average 0.1% monthly return and the factor portfolio 0.7%. During expansions both average about 1.0–1.1% a month. Across the 46 worst US-equity months, approximately the worst decile of the sample, the asset portfolio loses 3.8% per month on average versus 0.9% for factors. In the remaining months both average 1.3%. These are ex post conditional comparisons; the allocation rule does not use knowledge of the recession classification or worst-month set to trade.

The average rolling pairwise factor correlation rises during the financial crisis but peaks around 0.18, remaining below the average asset-class correlation. Excluding the equity component, its peak is around 0.11. The evidence therefore supports relative resilience of this selected combination, not the assertion that factor dependence never increases in stress. Funding shocks can still link otherwise unrelated strategies, and the article discusses forced deleveraging as a serious limitation of leveraged diversification.

## Two changes to the allocation design

The first variant replaces long-short value and momentum with long-only portfolios containing the top 30% of stocks on the respective signals. Carry and trend still permit derivatives shorting and leverage. This is not a wholly unlevered or long-only implementation of every constituent. Value and momentum now correlate approximately 0.71–0.73 with US equity and 0.87–0.90 with global equity. Their mutual total-return correlation changes from negative to +0.73, although active-return correlation relative to an equity benchmark can remain negative.

The resulting factor portfolio has about 9.5% volatility, approximately 72% of average constituent volatility of 13.2%. Its Sharpe improves from an average constituent value of 0.68 to 0.86. It correlates 0.87 with US stocks and 0.92 with the conventional asset portfolio. A sizable benefit remains relative to 0.48, but it is much less than the original 1.44. The source attributes about one third of that remaining improvement to equity value/momentum tilts and about two thirds to replacing conventional complements with carry and trend.

The second variant scales each constituent by 15% divided by its past 36-month rolling annualized volatility. A causal formalization, using excess return and estimates available before month $t$, is

$$
\ell_{j,t}=\frac{0.15}{\widehat\sigma_{j,t-1}^{(36)}},\qquad
r_{j,t}^{\mathrm{scaled}}=r_{f,t}+\ell_{j,t}(r_{j,t}-r_{f,t}).
$$

The article states the exposure scaling rule but does not fully document financing, leverage caps, volatility floors, or exact cash implementation; the financed excess-return form above makes those accounting assumptions visible. This inverse-volatility rule equalizes estimated standalone risk, not covariance-inclusive Euler contributions, so it should not be described as an exact equal-risk-contribution optimization.

The common comparison window becomes 1976–2010 to permit the initial 36-month lookback. Over that matched period, asset Sharpe rises from 0.57 to 0.68 and factor Sharpe from 1.53 to 1.69. The long-only-style variant rises from 0.94 to 1.07. These matched-window baselines differ from the 1973–2010 headline figures. The paper reports average constituent Sharpe improvement of roughly 0.05 and somewhat stronger diversification, with portfolio volatility ratios falling to about 70% for assets and 44% for factors. The variant is described in prose rather than a full results table.

## Adding styles gradually

Exhibit 10 combines the conventional asset portfolio with an equal-weighted composite of the four styles alone. Equity is omitted from this style sleeve because it is already in the asset portfolio. Results are:

| Asset / style capital weight | Geometric return | Volatility | Sharpe | Max drawdown | Equity correlation | Asset sleeve risk share |
|---|---:|---:|---:|---:|---:|---:|
| 100 / 0 | 9.85% | 9.14% | 0.48 | −36% | 0.87 | 100% |
| 80 / 20 | 10.73% | 7.54% | 0.67 | −30% | 0.85 | 99% |
| 60 / 40 | 11.58% | 6.08% | 0.94 | −25% | 0.82 | 96% |
| 40 / 60 | 12.39% | 4.91% | 1.30 | −19% | 0.71 | 85% |
| 20 / 80 | 13.17% | 4.26% | 1.66 | −14% | 0.47 | 60% |
| 0 / 100 | 13.92% | 4.36% | 1.77 | −12% | 0.12 | 0% |

The 20% style allocation improves gross risk-adjusted performance, yet the asset sleeve still contributes 99% of total risk. This is a direct demonstration that capital diversification and risk diversification differ. A standard reconstruction of the reported risk share for asset weight $a$ is

$$
q_A=\frac{a\,\operatorname{Cov}(r_A,r_P)}{\operatorname{Var}(r_P)},\qquad
r_P=ar_A+(1-a)r_S.
$$

This covariance contribution, rather than the fraction of capital, is the relevant additive measure. The table alone does not provide the full-precision covariance inputs used by the authors.

## Reproducibility, costs, and interpretation

A faithful allocation-layer replication needs monthly component histories with the original vintage and splices, consistent bill returns, monthly 20% resets, the specified 36-month lookback for the scaling variant, and explicit handling of unavailable early observations. It should compute calendar-year compounded returns before taking the reported annual arithmetic mean, separately compute geometric growth, and reproduce monthly volatility, drawdowns, correlations, and conditional samples. The exact Sharpe estimator and some annualization details are not fully specified. Reproducing today's updated data-library series may differ from a 2012-vintage dataset.

The paper provides no net implementation backtest, source code, portfolio-level gross exposure history, instrument transaction ledger, security exclusions, or statistical uncertainty bands. Its appendix delegates important signal and weighting details to the source studies. It says results are similar for 1991–2010 when almost all series exist, but does not tabulate that robustness comparison. The evidence should therefore be treated as a gross historical design study with a clear allocation layer and partially external constituent construction.

The authors suggest then-current institutional trading costs might reduce dynamic macro-strategy Sharpe by at most about 0.1 units, with larger effects for equity momentum, and acknowledge that earlier historical costs were higher. These are judgments, not measured deductions in the exhibits. Their fee illustration assumes 10% volatility and 1.0 Sharpe after trading costs but before fees; a simplified 2-and-20 structure can reduce investor Sharpe to 0.6. Actual management contracts, high-water marks, cash treatment, and path dependence are not modeled in that illustration.

The largest unresolved economic risks are factor selection after seeing history, future premium decay, capacity, and maintaining leveraged exposures when financing conditions deteriorate. The authors emphasize that only the market portfolio can be held by everyone, so scaling a simulated long-short premium across all investors is not innocuous. The supported takeaway is narrower and useful: seek independently sourced return streams and evaluate their covariance contribution to the whole portfolio. The selected dynamic styles offered substantially more gross diversification than the selected asset labels, but realizing that advantage requires cost-effective exposure, credible signal construction, and financing that survives the same crises in which diversification is needed.

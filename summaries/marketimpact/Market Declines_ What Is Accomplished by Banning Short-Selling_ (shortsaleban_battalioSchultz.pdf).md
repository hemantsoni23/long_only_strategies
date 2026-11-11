# Market Declines: What Is Accomplished by Banning Short-Selling?

Robert Battalio, Hamid Mehran, and Paul Schultz. *Federal Reserve Bank of New York, Current Issues in Economics and Finance* 18(5), 2012. [Source PDF](../../Finance/shortsaleban_battalioSchultz.pdf). The complete seven-page article, including its references, three tables, two charts, and calculation footnotes, was read. Page numbers below refer to the PDF, which agrees with printed pagination.

## Why this matters

A restriction that reduces observed short selling can still make trading more expensive without preventing a market decline. This article separates those questions using the 2008 ban on U.S. financial stocks, the August 2011 sovereign-rating downgrade, and estimates of the costs borne by equity and option liquidity demanders. Its most useful contribution for a quant researcher is a compact set of implementable diagnostics, together with a transparent conversion from spread changes to dollar trading costs.

The results challenge a simple account in which unusually large short sales mechanically cause marketwide price declines. In the 2011 cross-section, larger increases in short interest are associated with higher, rather than lower, contemporaneous stock returns. Stocks subject to a short-sale price restriction on August 8 perform worse than unrestricted stocks. These are conditional and unconditional associations, however, not randomized experiments. The article is stronger as evidence against a simple descriptive prediction than as a complete estimate of the causal effect of a ban.

The source combines new calculations with estimates taken from other papers. Its three regression tables and its plot of 995 banned financial stocks are its own empirical presentation. The equity-spread input comes from Boehmer, Jones, and Zhang; the option-spread estimates come from Battalio and Schultz's separate 2011 study. A reproduction must retain those boundaries rather than treating all numbers as estimates from one common sample.

## Economic mechanisms and the relevant trading quantity

A short position begins with borrowing shares, selling them, and subsequently buying shares to return to the lender. The article describes U.S. equity collateral conventionally equal to 102% of the borrowed shares' value. The lender pays a negotiated rebate on cash collateral; for easy-to-borrow stocks, the cited rebate is roughly 8–25 basis points below the federal funds rate. Hard-to-borrow stocks can have much lower or negative rebates. These are historical institutional descriptions in this 2012 article, not current lending quotes or universal contract terms.

The distinction between short-sale volume and short interest is essential. Intraday market makers can sell short and cover repeatedly, contributing large transaction volume without building a persistent short position. Biweekly short interest measures shares remaining short at a reporting date. It is a stock of positions, not the sum of short-sale transactions. Changes in that stock combine openings and closings and miss positions created and covered between the two observations.

The paper's 2011 tests therefore focus on persistent net positioning, which the authors regard as more relevant to sustained price pressure. They cannot directly test whether transient intraday short-sale flows amplified a particular minute's decline. Nor do cash-equity short-interest data measure synthetic exposure obtained through options or other derivatives.

The proposed manipulation mechanism also requires more than selling pressure. If buying and selling have symmetric permanent price effects, an investor who pushes down the price by selling short must reverse that pressure while covering. A profitable manipulation needs some additional channel, such as inducing other investors to sell, exploiting nonlinear or transient effects, or damaging a firm's financing conditions. The article discusses these possibilities but does not specify or estimate a strategic manipulation model. Its argument is an economic obstacle to a naive bear-raid story, not a theorem ruling out every form of manipulation.

For financial institutions, price and funding can interact. Falling equity prices may reduce counterparty confidence, raise collateral requirements, or impair access to funding. That feedback can be efficient if prices reveal genuine weakness, or destructive if prices are artificially depressed. The empirical difficulty is distinguishing the two when the regulator imposes a ban precisely because the affected firms are under stress.

## The 2008 return comparison

The source examines 995 financial stocks subject to a short-selling ban during 2008. Daily holding-period returns come from CRSP. Chart 1, p. 4, displays equal-weighted cumulative returns for the banned financial-stock group and an equal-weighted portfolio of U.S. nonfinancial stocks not subject to the ban. The displayed period is August 1–October 31, 2008; both series are normalized to zero on September 14.

A literal reconstruction needs the date-specific restricted-security list, a stable security identifier crosswalk, CRSP daily returns including the chosen treatment of distributions and delistings, and the author's portfolio membership rules. Those constituent files are not supplied. The wording also does not fully distinguish averaging stock-level cumulative returns from compounding an equal-weighted portfolio's daily returns. Both are plausible interpretations of an equal-weighted cumulative-return plot, but they differ when individual returns disperse. The source's normalization date should be preserved rather than silently rebasing at the ban announcement.

The graph is descriptive. Financial and nonfinancial firms faced different credit exposures, leverage, funding stress, and policy interventions. The authors explicitly acknowledge the difficulty of finding an appropriate benchmark because nearly all financial stocks were targeted. An equal-weighted nonfinancial portfolio supplies context; it does not establish the financial stocks' untreated counterfactual.

The article emphasizes a large fall on September 15, when Lehman Brothers filed for Chapter 11 protection, and positive returns on September 18 and September 22 around the ban's initiation. It also notes the Treasury's September 20 request for authority to acquire troubled assets. Consequently, a positive abnormal return around the ban cannot be assigned uniquely to the prohibition.

The reported financial-stock decline exceeds 12% over the fourteen trading days of the ban. The authors describe subsequent stabilization, but Chart 1 still shows substantial variation afterward; “stabilization” should not be converted into a constant post-ban price or a formally estimated break. The ban was not sufficient to prevent falling prices. That observation alone does not determine whether prices would have fallen even more without it.

For international context, the article summarizes Beber and Pagano's study of thirty countries from January 2008 to June 2009. In countries where only some stocks were restricted, that study compares cumulative abnormal returns for restricted and unrestricted securities, with abnormal returns measured relative to an equal-weighted national index. The U.S. financial-stock response is unusually positive, potentially because of contemporaneous support measures such as TARP. The source reports no comparable support for a general price-protection effect outside the United States. This international evidence is cited research, not a thirty-country panel reconstructed in the present article.

## The 2011 event and short-interest normalization

S&P announced the U.S. sovereign downgrade from AAA to AA+ after the close on Friday, August 5, 2011. The S&P 500 fell 6.66% on Monday, August 8. There was no blanket U.S. short-sale ban analogous to the 2008 intervention, although individual stocks could be subject to short-sale price restrictions.

For the first test, define $S_{i,0}$ and $S_{i,1}$ as shares short on July 29 and August 15, respectively. The paper's explanatory variable is

$$
x_i=\frac{S_{i,1}-S_{i,0}}{(S_{i,1}+S_{i,0})/2}
=\frac{2(S_{i,1}-S_{i,0})}{S_{i,1}+S_{i,0}}.
$$

Require $S_{i,0}+S_{i,1}>0$. This excludes observations with zero short interest at both endpoints but permits zero at one endpoint. The variable is bounded in $[-2,2]$, with $-2$ representing complete closure from a positive initial position and $2$ representing a new position from zero. It is not the conventional percentage change with initial short interest in the denominator.

For positive initial short interest, let $g_i=S_{i,1}/S_{i,0}-1$. Then

$$
x_i=\frac{2g_i}{2+g_i},
\qquad
g_i=\frac{2x_i}{2-x_i}.
$$

This derived conversion helps interpret scale. A doubling of short interest gives $x_i=2/3$, not $1$; $x_i=0.1$ corresponds to approximately 10.53% growth. The symmetric denominator reduces the extreme leverage of observations with near-zero initial positions, but does not remove measurement errors or economic differences between stocks.

Table 1 identifies the short-interest universe as stocks listed on the NYSE and American Stock Exchange. The short-interest source is the NYSE; returns are CRSP data. The following entries are decimals, not percentages:

| Quantity | 10th percentile | 25th percentile | Median | 75th percentile | 90th percentile | Mean |
|---|---:|---:|---:|---:|---:|---:|
| Normalized short-interest change | −0.1714 | −0.0438 | 0.0493 | 0.1550 | 0.3063 | 0.0605 |
| Stock return | −0.2023 | −0.1440 | −0.0870 | −0.0377 | 0.0029 | −0.0939 |

Thus more than one-quarter of stocks experienced net short covering, while more than three-quarters experienced negative returns. The mean return is −9.39%, and the median is −8.70%. These stock-level event-window summaries should not be confused with the single-day, capitalization-weighted S&P 500 decline of 6.66%.

## Return regressions and their economic scale

The first cross-sectional specification is

$$
R_{i,[\mathrm{Jul}\,29,\mathrm{Aug}\,15]}
=\alpha+\beta x_i+\varepsilon_i.
$$

The source says returns are cumulated over July 29–August 15, 2011. A reproduction should document endpoint inclusion and arithmetic compounding. A compounded holding-period return is the natural implementation, but the article does not provide code confirming every convention. There are no reported sector, beta, size, leverage, or pre-event-return controls in this regression.

Table 2, p. 5, reports:

| Sample | Intercept | Intercept $t$ | $\beta$ | Slope $t$ | Adjusted $R^2$ | Stocks |
|---|---:|---:|---:|---:|---:|---:|
| All eligible stocks | −0.0957 | −43.03 | 0.0298 | 3.72 | 0.0069 | 1,843 |
| Price at least \$5 | −0.0927 | −41.77 | 0.0277 | 3.43 | 0.0066 | 1,611 |
| At least 1 million shares short at both dates | −0.1027 | −40.30 | 0.0624 | 4.79 | 0.0166 | 1,306 |

The positive slopes contradict the simple cross-sectional prediction that the largest increases in outstanding shorts should accompany the worst returns. They do not imply that increasing a stock's short interest raises its price. Shorts can respond to price changes, cover losing positions, provide liquidity after buying pressure, or share omitted determinants with returns.

For the full sample, a 0.1 increase in $x_i$ corresponds to a fitted return difference of $0.00298$, or 29.8 basis points. A doubling of shares short corresponds to a fitted difference of approximately 1.99 percentage points. These are coefficient-scale calculations, not counterfactual trading profits. The full-sample interquartile change in $x_i$ is $0.1550-(-0.0438)=0.1988$, giving a fitted return difference of approximately 59.24 basis points.

Explanatory power is modest: adjusted $R^2$ ranges from 0.66% to 1.66%. Statistical significance should not be mistaken for an explanation of most cross-sectional return variation. The article reports OLS $t$ statistics but does not give a complete variance-estimator specification. Reproducing the coefficients does not guarantee reproducing the reported significance without knowing whether standard errors were conventional, heteroskedasticity robust, or otherwise adjusted.

The price and minimum-short-position screens provide useful robustness checks, but they also change the sample. The higher 0.0624 coefficient in the large-short-position sample is not by itself evidence of a statistically significant interaction. A direct interaction test or common-sample comparison would be needed for that claim.

## The circuit-breaker comparison and a source-window inconsistency

The second test uses the individual-stock restriction triggered by a decline of at least 10%. As described on p. 5, restricted short sales must execute above the national best bid for the remainder of the triggering day and the next trading day. This is a price test, not a complete prohibition on every short sale. The conclusion's shorthand that affected stocks “could not be shorted” is too broad for the rule the body describes.

Let $D_i=1$ if stock $i$ triggered the restriction on Friday, August 5, before the sovereign downgrade was announced. Such stocks began August 8 under a restriction. The surrounding text specifies

$$
R_{i,\mathrm{Aug}\,8}
=a+bD_i+u_i,
$$

and then adds normalized volume,

$$
R_{i,\mathrm{Aug}\,8}
=a+bD_i+cV_i+u_i,
\qquad
V_i=\frac{\operatorname{Volume}_{i,\mathrm{Aug}\,8}}
{\sum_{d\in\mathrm{September}}\operatorname{Volume}_{i,d}}.
$$

The denominator is total September volume, not average daily September volume. It uses information after the event and is suitable only as an ex post normalization. This regression is not an implementable August 8 forecasting rule.

Table 3 gives the following estimates:

| Specification | Intercept | Intercept $t$ | Restriction coefficient | Restriction $t$ | Volume coefficient | Volume $t$ | Adjusted $R^2$ | Stocks |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Restriction indicator only | −0.0836 | −68.97 | −0.0216 | −5.12 | — | — | 0.0131 | 1,905 |
| With normalized volume | −0.0844 | −49.41 | −0.0217 | −5.14 | 0.0044 | 0.07 | 0.0128 | 1,611 |

Under the text's single-day specification, the unadjusted fitted return is −8.36% for unrestricted stocks and −10.52% for restricted stocks, a 2.16-percentage-point difference. The volume-adjusted gap is 2.17 percentage points. The volume coefficient is economically small in its stated units and statistically indistinguishable from zero by its reported $t=0.07$.

There is a material printed inconsistency. Table 3's note says returns are cumulated from July 29 through August 15, whereas both the surrounding design description and result interpretation repeatedly say August 8. The table's note appears to reuse the window in Table 2, but the PDF alone does not prove that this is a copy-editing error. An exact replication should estimate both windows, seek clarification or underlying code, and retain the distinction. The calculations above explicitly follow the prose; they do not silently overwrite the table note.

The sample falls from 1,905 to 1,611 when volume is included. The article does not clearly document whether this is entirely volume-data availability, an additional price screen, or another selection rule. It is not safe to attribute that count mechanically to the \$5 screen merely because Table 2 also contains 1,611 observations.

The main identification problem is selection into the restriction: a stock must already have fallen at least 10% to trigger it. Such stocks may be unusually exposed to the same shock that drives the next day's returns. The observed negative gap cannot establish that the price restriction itself caused an additional decline. The test shows that the restricted group was not visibly protected in this simple comparison; it does not supply a causal estimate under conditional exchangeability.

## From spread changes to dollar costs

The article's most directly reproducible numerical calculation concerns equity trading costs. It takes a 32-basis-point increase in relative effective spreads for banned stocks from Boehmer, Jones, and Zhang's multivariate analysis. A liquidity-demanding execution pays approximately one effective half-spread relative to the midpoint, so the relevant per-dollar cost increment is 16 basis points.

Using the inputs in footnote 10, p. 6,

$$
\Delta C_{\mathrm{equity}}
=\overline{\mathrm{DollarVolume}}\,
N\,T\,\frac{\Delta s}{2},
$$

with average daily dollar volume \$66,749,000, $N=404$ stocks restricted for the full period, $T=14$ trading days, and $\Delta s=0.0032$, gives

$$
\Delta C_{\mathrm{equity}}
=66{,}749{,}000\times404\times14\times0.0016
=604{,}051{,}750.40.
$$

The independent arithmetic therefore reproduces the article's “more than \$600 million” equity-cost estimate. Using the full spread instead of its half would double the estimate incorrectly. The 404 continuously restricted stocks are not the 995-stock group used in the earlier return plot; those are different sample definitions serving different calculations.

This calculation applies an estimated spread change to observed trading activity. It does not model how volumes would have changed without the ban, and it excludes gains from trades abandoned because liquidity became expensive. It is a trading-cost attribution, not a full welfare calculation. Dealer revenues, inventory losses, and informational rents are not separately decomposed.

The options analysis similarly combines observed daily volume with estimated daily incremental spreads from Battalio and Schultz's 2011 study:

$$
\Delta C_{\mathrm{options}}
=\sum_{t\in\mathcal B}
Q_t\,\frac{\Delta s_t^{\mathrm{option}}}{2},
$$

where $Q_t$ must be expressed in the units appropriate to the spread quote. For a standard option quoted per underlying share, a contract-count implementation needs the contract multiplier; adjusted contracts require their actual multipliers. This units requirement is a reconstruction detail, not a new parameter supplied by the article.

The cited options study finds that October-expiry puts and calls on banned stocks initially had quoted spreads more than \$0.96 wider than the control group's options. Spreads remained approximately 10% higher on average for the rest of the ban. These are different quantities: the former is a dollar spread difference for an expiry group, while the latter is a relative spread increase. They should not be interchanged in the cost formula.

Chart 2 reports more than \$110 million of incremental option trading costs on September 19 alone and more than \$505 million across the fourteen trading days, September 19–October 8. The September 19 bar is the largest; costs remain positive on subsequent days after the derivative-market-maker exemption is extended. The daily coefficients and exact volumes are not tabulated, so the chart is not a full numerical dataset. The source points to an appendix of the separate Battalio–Schultz article; that appendix is not included in this seven-page PDF.

The equity calculation plus the reported option total exceeds \$1.109 billion. This arithmetic supports the source's aggregate “more than \$1 billion” statement, conditional on the two studies' attribution assumptions. It does not provide a standard error for the sum or establish that all costs would disappear under an alternative policy.

## Why exemptions did not eliminate the options disruption

The ban began on a triple-witching Friday. Derivatives market makers initially had an exemption scheduled to expire at 11:59 p.m. on September 19. They could therefore face uncertainty about whether positions opened that day could be hedged by shorting stock afterward. The exemption was extended before the market opened on Monday, September 22, but further restrictions required clarification over subsequent trading days.

This chronology supplies an economic explanation for a sharp initial spread increase and continued costs after formal relief. A market maker prices the ability to manage the position over its life, not merely the legality of its next trade. Uncertainty about hedge availability can widen option quotes even if a later clarification ultimately permits hedging. The article interprets the persistence as regulatory uncertainty; it does not estimate a separate uncertainty process or isolate that channel from all crisis-related risk.

The same mechanism extends to convertible arbitrage. Investors commonly buy a convertible and short the issuer's common stock to reduce equity exposure. The source cites evidence that convertible arbitrageurs buy more than 75% of primary convertible issuance. Removing their hedge can reduce demand for new issues and impair financing access. That cited share is not a measured coefficient in the article's own regression tables, and the article does not derive an optimal hedge ratio or quantify issuer-level welfare losses.

## Reproduction boundaries and research use

A careful replication would keep four datasets separate: the 2008 daily equity-return panel; the 2011 short-interest and return cross-section; the August 5 restriction list and August 8 return/volume panel; and the equity/options spread-cost inputs. Security identifiers, corporate actions, observation exclusions, reporting dates, and publication dates must be explicit. The short-interest settlement observations used in the explanatory regressions should not be treated as information contemporaneously available to a live trader.

The original article supplies neither return files nor restricted-stock lists, regression code, exact standard-error conventions, a complete option-volume panel, or the external option-regression appendix. It also leaves the Table 3 return window unresolved. The documented formulas and printed tables make substantial reconstruction possible, but not a claim of exact data-level replication from the PDF alone.

For execution and portfolio research, the evidence supports treating shortability as part of the feasible trading and hedging set. It also warns against interpreting a short-interest change as pure informed selling pressure. A fall in outstanding shorts can coexist with deteriorating liquidity, and a policy aimed at cash-equity shorts can raise implementation costs in options and convertibles.

The defensible conclusion is narrower than a universal claim about short sellers. In these event comparisons, the simple prediction that more shorting accompanies worse returns is not supported, and the measured liquidity costs are large. The untreated price path and the systemwide effect of a possible confidence intervention remain unidentified. Those limits should accompany any use of the paper in a market-stress scenario or policy evaluation.

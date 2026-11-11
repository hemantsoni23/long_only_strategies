# Front-running of mutual fund fire-sales

**Teodor Dyakov and Marno Verbeek (2013).** *Journal of Banking & Finance* 37, 4931–4942. DOI: 10.1016/j.jbankfin.2013.08.013. Source: [BestIdeas_DyakovVerbeek_2013.pdf](../../Finance/BestIdeas_DyakovVerbeek_2013.pdf). This note covers the complete 12-page article, including Appendix A. Page references below are journal pages; subtract 4930 to obtain the PDF page.

## Why this matters

The paper asks whether publicly disclosed mutual-fund holdings, combined with forecasts of investor redemptions, identify stocks that will suffer temporary selling pressure. Its contribution is an attempt to make the information timing implementable: holdings enter with a two-month publication delay, and fund-flow forecasts use coefficients estimated before the forecast month. Earlier evidence that realized fund liquidations move prices need not establish a trading opportunity available beforehand.

The main finding is conditional. Among selected stocks below the contemporaneous **mean**, not median, NYSE market capitalization, the long portfolio of expected fire-sale stocks has a five-factor alpha of −0.50% per month, standard error 0.18%. Shorting reverses that alpha before implementation costs. The full stock selection has an insignificant −0.22% alpha, while the largest stocks have a positive 0.86% alpha: their prices appear to reverse before the delayed information can be exploited. Furthermore, the below-mean monthly alpha is only −0.08% in 2001–2010. Daily event returns suggest that the later opportunity ends roughly halfway through the month.

For a researcher, the useful object is a forecast of constrained demand coupled to its relaxation time. It is not simply a generic short signal based on poor fund performance. Fund distress, stock ownership, liquidity, information delay, and holding horizon jointly determine the return. The paper does not observe actual front-runners or establish that their trades causally worsen distressed funds' outcomes.

## Data, sample formation, and calendar

The authors combine CRSP mutual-fund returns and total net assets, Thomson Financial/CDA S12 fund equity holdings, CRSP monthly and daily stock files, Compustat accounting data, and I/B/E/S analyst forecasts. The two fund databases include dead funds and are linked with WRDS MFLINKS. Holdings are adjusted for splits and other share changes. The stated data window in Appendix A is January 1990 through June 2010, consistent with the reported 246 monthly portfolio opportunities; generic references to “1990–2010” should not be silently extended through December 2010.

The universe contains 2,639 distinct U.S. actively managed domestic equity funds. Index, balanced, bond, money-market, sector, international, and primarily non-common-stock funds are excluded. Appendix A specifies the following selection details:

- CRSP objectives must belong to the domestic-equity lists supplied by Lipper, Wiesenberger, or Strategic Insight. Lipper's list is EI, EIEI, EMN, FLX, G, GI, I, LCCE, LCGE, LCVE, LSE, MC, MCCE, MCGE, MCVE, MLCE, MLGE, MLVE, SCCE, SCGE, SCVE, SESE, SG. Strategic Insight's is SCG, GRO, AGG, ING, GRI, GMC. Wiesenberger's is SCG, AGG, G, G–S, S–G, GRO, LTG, I, I–S, IEQ, ING, GCI, G–I, G–I–S, G–S–I, I–G, I–G–S, I–S–G, S–G–I, S–I–G, GRI, MCG.
- Thomson objectives must be aggressive growth, growth, growth and income, or unclassified. Retain CRSP common-stock percentages from 80% through 105%; require at least ten stocks and at least \$5 million under management.
- Remove funds with names containing INDEX, INDE, INDX, S&P, or MSCI. Resolve overlapping report/file dates caused by mergers and name changes. The authors manually correct MFLINKS cases assigning different Thomson funds to one identity; these corrections are not supplied.
- Sum net assets over share classes. Use lagged-net-asset-weighted share-class attributes and returns, and the oldest share class for fund age.
- The cross-database asset check retains $1/1.3<TNA^{CRSP}/TNA^{CDA}<1.3$. An additional asset-change screen retains $-0.5<\Delta TNA_t/TNA_{t-1}<2.0$.

These screens matter because apparent redemptions caused by a merger, reporting discontinuity, or duplicated share class can otherwise become the strongest “distress” observations. The paper does not provide a downloadable correction list or specify every missing-data convention. Reproduction therefore requires documenting database vintage, matching rules, and observations dropped at each step.

Table 1 reports a full-sample median of 73 stocks, \$211 million in net assets, and 1.11% monthly net return. The median turnover and expense ratio in the table's full-period row are **66% annually and 1.23% annually**, respectively. The surrounding prose instead cites 63% and 1.17%; a faithful replication should use the table for this summary and retain the discrepancy as a source inconsistency. Mean net assets are \$928 million, considerably above the median. These are time-aggregated descriptive values, not inputs to the forecast.

## Step 1: infer flows and estimate separate tail classifiers

For fund $j$ and month $t$, the flow measure is

$$
f_{j,t}=\frac{TNA_{j,t}-TNA_{j,t-1}(1+R_{j,t})}{TNA_{j,t-1}},
$$

where $R_{j,t}$ is the fund's net return. This accounting residual assumes flows arrive at a convention compatible with monthly return adjustment; it is not a transaction-level observation of subscriptions and redemptions. Define two binary outcomes using each month's cross-sectional flow distribution: an outflow event is membership in its bottom decile; an inflow event is membership in its top decile.

Estimate two independent logistic regressions each month, with the same regressors but separate coefficients. Writing $s\in\{O,I\}$ for outflow and inflow, the model is

$$
\Pr(D^s_{j,t}=1\mid X_{j,t-1})=\Lambda(X_{j,t-1}'\theta^s_t),\qquad
\Lambda(z)=\frac{1}{1+e^{-z}},
$$

$$
X_{j,t-1}'\theta^s_t=a^s_t+\sum_{k=1}^{3}b^s_{k,t}f_{j,t-k}
+\sum_{k=1}^{3}c^s_{k,t}R_{j,t-k}
+d^s_{1,t}\log TNA_{j,t-1}+d^s_{2,t}(\log TNA_{j,t-1})^2.
$$

Each fit is a contemporaneous cross-sectional classification of month-$t$ outcomes using lagged characteristics. It is not a single full-sample logit or a rolling pooled regression. At the end of $t$, retain $\widehat\theta^s_t$, advance all explanatory variables one month, and compute $\widehat p^s_{j,t+1}=\Lambda(X_{j,t}'\widehat\theta^s_t)$. Select the highest 10% of predicted probabilities separately for each event type. A fund with the highest predicted outflow probability is selected as an outflow fund; the Table 4 caption's reference to the **lowest** decile of outflow probabilities is inconsistent with Section 3.1 and the classifier definition and should not be implemented.

Table 3's average outflow coefficients are −2.217 for the intercept, −10.144/−6.292/−4.484 for the three flow lags, −10.959/−3.027/−3.652 for return lags, and 0.041/−0.018 for log assets and its square. Inflow coefficients are −2.381, 12.095/8.913/5.925, 14.051/7.223/4.866, and −0.104/−0.010. These describe the fitted relation and cannot replace the sequence of monthly estimates without introducing look-ahead. The stronger effect of the most recent lag is consistent with persistent flows and return chasing. The paper averages coefficient estimates and estimates uncertainty from their time series, rather than reporting a pooled-logit covariance matrix.

The out-of-sample classification success rate is 30% for outflow funds and 48% for inflow funds, with time-series standard deviations of 8% and 10%. Because each predicted set contains a decile of funds, random classification would produce about 10% precision absent ties or unequal eligible samples. The corresponding OLS flow-prediction approach identifies 27% and 42%. This supports separate tail models but is not evidence of perfectly calibrated probabilities. Mean realized flows in selected outflow/inflow sets are −1.63%/+7.81%, and medians −2.16%/+7.15%. The average selected set contains 123 funds.

There is still an availability assumption: the implementation treats month-end returns and net assets needed for $f_{j,t}$ as available for next-month trading. The study carefully lags holdings but does not audit fund-by-fund publication timestamps for all monthly TNA data. A production backtest should impose the actual availability of those inputs as well.

## Step 2: translate predicted distress into stock-level demand

Let $N_{j,i,t}$ be the split-adjusted number of shares of stock $i$ in fund $j$'s latest eligible public holdings report at decision date $t$. Let $I_t$ and $O_t$ denote selected anticipated inflow and outflow funds. Equation 4 defines a signed pressure score:

$$
P_{i,t+1}=\frac{\sum_{j\in I_t}N_{j,i,t}-\sum_{j\in O_t}N_{j,i,t}}
{\operatorname{AvgVolume}_{i,t-12:t-6}}.
$$

Negative values imply more ownership by predicted redemption funds than by predicted inflow funds. The denominator is average trading volume over months $t-12$ through $t-6$. The article does not completely specify daily-versus-monthly volume aggregation or vendor adjustments; a common global scale would not change ranks, but heterogeneous volume conventions would. The lagged window helps avoid normalizing by volume already affected by current selling pressure.

This score is **not** expected dollar sales. It does not multiply each position by a predicted redemption fraction, apply the probability continuously, or estimate which individual securities a manager will liquidate. It first classifies funds into extreme sets and then nets their share holdings. Inflow ownership offsets redemption ownership because successful funds may use new money to expand existing positions. The economic asymmetry is that an outflow fund must raise cash, while an inflow fund can hold cash, add positions, or buy new securities.

Holdings receive a two-month reporting delay. A January-end snapshot becomes eligible at March-end and first informs the April portfolio. Quarterly reporters' April snapshots become usable at June-end. Semiannual reports remain eligible for at most six months **after publication eligibility**, so the underlying snapshot may be approximately two to eight months old. All intervening share adjustments must be applied. The authors repeat the exercise allowing only three months after the delay and find qualitatively similar results. Keeping six months preserves more continuous coverage of semiannual reporters.

At each formation date, select the bottom decile of the stock pressure distribution and equal-weight its constituents. The base pressure universe comprises stocks held by the selected flow funds, rather than necessarily every CRSP stock with an artificial zero score. The manuscript does not fully describe ties at zero, treatment of a fund selected by both logits, or missing/zero volume. These choices should be made explicit in a reconstruction. Holding the selected stocks for the next calendar month produces a **long** return series for expected fire sales; the hypothetical front-runner takes the opposite exposure. Rebalance monthly. Drop a portfolio-month with fewer than 25 eligible stocks.

There are on average 252 selected stocks: 194 below mean NYSE size and 58 above it. The full and below-mean groups have at least 25 names in 244 of 246 months; the above-mean group does so in only 156 months. Consequently, comparisons across size groups also involve different available calendars. Below-mean should not be equated with microcap: the selected below-mean stocks have 3.59%, 14.57%, 29.37%, 38.30%, and 14.16% representation across the five NYSE size quintiles. Most lie in the upper three quintiles, but the lower two still represent about 18% of this subgroup. The paper's “less than 15%” statement refers to the full selection, where the first two quintiles total 14.34%.

## Return attribution and central numerical results

For each portfolio, regress its monthly excess return on the market excess return, SMB, HML, momentum, and the traded Pastor–Stambaugh liquidity factor:

$$
R_{P,t}-R_{f,t}=\alpha+\beta_M MKT_t+\beta_S SMB_t+\beta_H HML_t+
\beta_U MOM_t+\beta_L LIQ_t+\varepsilon_t.
$$

The article also reports nested CAPM, three-factor, and four-factor specifications. Table 6 gives these five-factor results, in percentage points per month:

| Long expected-fire-sale portfolio | Alpha | Standard error | Market | SMB | HML | MOM | Liquidity |
|---|---:|---:|---:|---:|---:|---:|---:|
| All selected stocks | −0.22 | 0.17 | 1.09 | 0.45 | 0.29 | −0.22 | 0.05 |
| Below mean NYSE size | −0.50 | 0.18 | 1.08 | 0.56 | 0.31 | −0.31 | 0.04 |
| Above mean NYSE size | 0.86 | 0.28 | 1.06 | −0.04 | 0.07 | −0.05 | −0.09 |

The below-mean estimate has an approximate $t$-ratio of −2.78. Its CAPM, three-factor, and four-factor alphas are −0.49%, −0.74%, and −0.48%. A short book reverses both alpha and factor exposures; the result does not itself specify a market-neutral hedging portfolio, financing arrangement, or margin account. In particular, shorting an equity basket and earning its negative alpha are not the same as earning a standalone riskless 0.50% monthly return.

Event-time alphas in Table 7 strengthen the temporary-pressure interpretation. The below-mean stocks have alphas of −0.75%, −1.18%, and −1.43% in months −3, −2, and −1 relative to formation; −0.50% in the holding month; then +0.48%, +0.35%, and +0.22% in the next three months. Above-mean stocks show −1.02% immediately beforehand but +0.86% during the holding month. Large-stock pressure therefore appears to have been arbitraged away sooner. These before/after portfolios use ex post membership in the formation portfolio and are explanatory event studies, not additional investable signals known six months earlier.

The monthly short strategy turns over 71.78% of its portfolio. The authors report a 0.35% break-even transaction cost. This corresponds approximately to $0.50\%/(2\times0.7178)=0.348\%$ per one-way traded notional when entries and exits both incur costs. It is a stylized alpha budget. Borrow fees, recalls, failed locates, short-sale constraints, financing, impact, and the potential cost of factor hedges are not modeled explicitly. Being above microcap size is not proof that these costs or constraints are negligible.

## The holding horizon changes over time

The monthly effect is concentrated in the earlier period. Table 8's below-mean holding-month alpha is −0.62% with standard error 0.24% in 1990–2000, versus −0.08% with standard error 0.23% in 2001–2010. Above-mean alphas are +0.42% and +1.02%. The discussion attributes faster price restoration to potential improvements in liquidity, competition, and information dissemination; it does not identify one reform as the causal driver. Table 8's caption once says 2000–2010, but its panel label and the main split say 2001–2010.

For daily analysis, subtract the return on the CRSP value-weighted market from each selected stock's daily return, equal-weight, and accumulate across trading days within the month. These cumulative average abnormal returns are market-adjusted event statistics, not daily five-factor alphas. For below-mean stocks:

| Sample | Days 1–5 | Days 1–10 | Days 1–15 | Days 1–20 |
|---|---:|---:|---:|---:|
| 1990–2010 | −0.27% | −0.36% | −0.51% | −0.46% |
| 1990–2000 | −0.24% | −0.38% | −0.85% | −0.85% |
| 2001–2010 | −0.37% | −0.55% | −0.36% | −0.21% |

In the later period, the standard error at day 10 is 0.22%, rising to 0.64% at day 20. The initial decline followed by partial reversal explains why monthly alpha disappears. Choosing day 10 after examining this path is a new strategy choice. The paper does not report an independently trained, fully costed ten-day strategy with a preregistered exit rule. The later daily evidence is therefore suggestive of a shorter opportunity, rather than a complete validation of current profitability.

## Tests against news explanations and parameter sensitivity

The Fama–MacBeth test in Table 10 regresses individual stock returns on lagged size and book-to-market, prior 12-month return, a leverage measure, indicators for selected below/above-mean stocks, standardized unexpected earnings, and analyst forecast error. Accounting inputs use a four-month lag. SUE equals current quarterly EPS minus EPS four quarters earlier, divided by the standard deviation of EPS over the preceding eight quarters, requiring at least four. FER equals realized EPS minus the mean analyst forecast, divided by the previous year's book equity per share. These measures enter for announcements in months $t$, $t-1$, or $t-2$. Since contemporaneous announcement information is included, this regression tests an explanatory alternative; it is not an ex ante trading rule.

The selected-small-stock coefficient changes only from −0.32% to −0.33% with the two news variables, with standard error 0.15%. The selected-large-stock coefficient remains +1.35%, standard error 0.33%. SUE and FER have positive coefficients, 0.06 and 1.17. Standard errors use Newey–West with three lags. The leverage caption unusually defines a ratio of book assets to debt assets; its exact accounting field implementation is not given. Retain this uncertainty rather than silently substituting a familiar debt/assets measure.

These results make the two measured earnings channels inadequate explanations for the return pattern. They do not literally rule out every information-based explanation, as the article's prose sometimes suggests. Unobserved news, changing risk, measurement error, and joint selection on past performance can remain. Reversals are useful corroboration of temporary demand pressure, but they are not an instrument for a clean causal estimate of forced selling.

Robustness varies fund-tail selection and stock-pressure selection among 5%, 10%, and 15%. With a 10% fund-tail selection, below-mean holding-month alphas are −0.50%, −0.25%, and −0.51% for the 10%, 5%, and 15% stock selections; standard errors are 0.18%, 0.22%, and 0.17%. A narrower signal is not stronger here. The 5%-stock portfolio is often too small and sensitive to misclassification. Increasing the fund-tail selection to 15% gives a 5%-stock alpha of −0.40% with standard error 0.23%. Although the text calls this significant, its approximate two-sided $t$-ratio of 1.74 supports at most conventional 10% significance, not 5%. This qualification prevents overstating the robustness evidence.

## What a replication should deliver

An auditable implementation should produce monthly flow classifications using only previous estimates; timestamped eligible holdings; pressure-score distributions; selected names and weights; a count of exclusions; and separate long-basket and implementable-short-account returns. Reproduce the 246-month opportunity calendar, 244 full/below-mean valid months, and the thinner large-stock calendar before comparing alphas. Then reproduce the Table 6 coefficients and the Table 9 event paths under the source's cost-free assumptions.

The economically important extension is to measure publication lags and trading costs before selecting a shorter exit horizon. The paper's central contribution survives a cautious reading: fund-level capital constraints can forecast stock-level demand beyond simple momentum, and the time required for liquidity to arrive determines whether public information is useful. Its strongest implementation warning is equally concrete: an attractive full-sample alpha can disappear once the holding horizon becomes longer than the life of the pressure signal.

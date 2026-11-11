# Efficient Capital Markets: A Review of Theory and Empirical Work

**Author:** Eugene F. Fama. **Publication:** *The Journal of Finance* 25(2), May 1970, pp. 383–417. **Source:** [EfficientMarketHypothesis_Fama_1970.pdf](../../Finance/EfficientMarketHypothesis_Fama_1970.pdf). The supplied PDF contains the complete article, references, and a final rights notice. Page references below use the printed journal pagination. This is a review of evidence available in 1970, not a current survey or a single newly conducted experiment.

## Why this matters

Fama's contribution is to turn an informal claim about information in prices into a framework for designing tests. A researcher must specify an information set, a model of normal expected returns, and a feasible strategy or event response. Only then does an observed return pattern have an economic interpretation. The review organizes weak, semi-strong, and strong information tests and separates fair-game restrictions from the much stronger random-walk hypothesis. It also shows why small statistical dependencies, substantial announcement effects, and compensation for risk can coexist with informational efficiency.

For replication, the useful output is a set of test architectures: serial-dependence and trading-rule tests; residual-based event studies; and risk-adjusted manager performance comparisons. The paper does not supply a common database, code, or uniform estimation protocol for all studies it reviews. This note reconstructs the models and designs actually described, records the historical numerical findings, and identifies where reproducing a result requires its original underlying study. Its conclusions should not be read as evidence about later samples, present transaction costs, or modern market structure.

## The formal object: an equilibrium conditional expected return

Let $p_{jt}$ be security $j$'s price at date $t$, with the next-period payoff or reinvestment-adjusted price defined consistently with its return. Let $r_{j,t+1}$ denote the simple holding-period return, and let $\Phi_t$ be the information available at $t$. The expected-return formulation on pp. 384–386 writes

$$
E[p_{j,t+1}\mid\Phi_t]=p_{jt}\{1+E[r_{j,t+1}\mid\Phi_t]\}.
$$

To give this restriction empirical content, denote the expected return required by the maintained equilibrium model by $m_{jt}$. Define a price innovation and a return innovation by

$$
x_{j,t+1}=p_{j,t+1}-p_{jt}(1+m_{jt}),\qquad z_{j,t+1}=r_{j,t+1}-m_{jt}.
$$

The fair-game restriction is

$$
E[x_{j,t+1}\mid\Phi_t]=0,\qquad E[z_{j,t+1}\mid\Phi_t]=0.
$$

This is a condition on returns relative to their equilibrium expectation, not a requirement that expected raw returns vanish. It accommodates predictable movements in risk compensation. Defining $m_{jt}$ after the fact as the unrestricted true conditional expectation would make the innovation condition an identity. An operational test instead restricts $m_{jt}$ using a pricing model and estimates or otherwise specifies it before evaluating residual predictability. A rejection then challenges the joint package of informational efficiency and the return model. Fama makes the need for an equilibrium model explicit, including in the discussion of systematic risk and the footnote on p. 400.

Suppose $a_j(\Phi_t)$ is an investment chosen using the stated information set. The innovation component of a portfolio's payoff is

$$
V_{t+1}=\sum_j a_j(\Phi_t)z_{j,t+1}.
$$

Under measurability and integrability, $E[V_{t+1}\mid\Phi_t]=0$. Predictable portfolio weights therefore do not generate positive expected abnormal payoff against the maintained benchmark. This algebra does not license unlimited borrowing, doubling strategies, or comparisons between portfolios with different risk exposures. Trading costs and admissible financing must be added to an implementable strategy test. Nor does it establish that all investors have identical realized performance.

### Three hypotheses that must not be conflated

A fair game is a conditional-mean restriction on abnormal returns. A submartingale price restriction additionally requires expected future price to be at least current price. The latter supports comparisons between certain single-security trading rules and passive holding under the paper's setup, but is not implied for every security by all equilibrium models: an asset providing valuable hedging services could have a negative expected raw return. A negative excess return alone would not contradict the raw-price submartingale restriction.

A random walk imposes more: in the version studied here, successive price changes or returns have independent, identically distributed innovations. Independence concerns the entire conditional distribution; the fair-game model constrains its mean. Volatility may depend on past information even when the conditional mean is correctly priced. One must also specify whether the random-walk variable is an absolute price change, a log-price change, or a return; these are not interchangeable hypotheses.

Zero serial correlation is weaker still. With finite second moments, fair-game innovations have zero covariance with measurable past innovations. The converse fails. Fama's footnote example uses two independent variables taking $+1$ and $-1$ with equal probability and a third variable equal to their product. The three are pairwise uncorrelated, but the third is known after observing the first two. Thus a correlation test cannot establish absence of nonlinear forecasting opportunities. If variance is infinite, even the familiar covariance-based formulation requires reconsideration.

The paper describes frictionless trading, freely available information, and agreement about information's implications as sufficient conditions for efficiency, not as necessary facts about every efficient market. It does not model an endogenous costly-information industry. That omission matters when translating its framework into a model of research incentives.

## Information sets and the interpretation of tests

The weak form asks whether past price and return information supports abnormal prediction. The semi-strong form asks how prices respond to publicly available information, including reported earnings, splits, and issues. The strong form asks whether any group possesses information that enables abnormal profit, including private or monopolistic information. These are nested informational ambitions, but empirical implementations are not automatically nested statistical tests.

An announcement-related price jump is compatible with semi-strong efficiency: public news should move prices. The relevant question is whether information available before the trade continues to predict benchmark-adjusted returns afterward. Conversely, private information can move prices before an announcement while violating a strong-form claim. Measuring mutual-fund performance potentially tests investment ability, but does not reveal by itself whether a successful fund used public or private information.

All three categories inherit the normal-return problem. Apparent predictability can be a missing risk premium; an apparently flat event-study residual can result from an insensitive benchmark. Fama's organization makes those maintained assumptions visible rather than resolving them once for all applications.

## Weak-form evidence: dependence, trading rules, and execution

### Serial correlation and runs

Table 1 on p. 393 reports first-order serial correlations of log-price changes for 30 Dow Jones industrial stocks at differencing intervals of one, four, nine, and sixteen days. Samples contain roughly 1,200–1,700 daily observations, generally ending on 26 September 1962 and beginning around the end of 1957, with starting dates varying by stock. A faithful replication would retrieve the stock-specific original sample dates and corporate-action adjustments rather than impose a single common window. The review does not document every sampling or overlap convention.

At the daily interval, 11 of 30 coefficients exceed twice their estimated standard errors in absolute value, and 22 are positive. The average daily coefficient is .026, as noted in the accompanying discussion. Individual examples visible in the table include .118 for Alcoa, −.087 for American Can, and −.123 for Goodyear. At longer intervals the signs shift: 21 coefficients are negative at four days and 24 at nine days. The review finds no stable pattern from which economically useful longer-horizon forecasts follow.

The approximate standard error discussed is $1/\sqrt{N-1}$. With a long daily sample, a coefficient near .06 can be statistically noticeable yet explain only $.06^2=.0036$, or about 0.36%, of the next change's variance in a simple linear regression. Statistical detectability is not equivalent to executable profit. That variance interpretation assumes finite second moments and a suitable regression setting; the paper separately raises heavy-tail concerns. Correlated stocks also make the count of individual significant coefficients different from a test based on 30 independent experiments.

Runs tests examine strings of successive changes having the same sign. In the cited 30-stock evidence, 26 stocks have fewer runs than independence predicts and eight have departures exceeding twice their standard errors. The average shortfall in runs is approximately 3%. This supports some positive short-run dependence while indicating that its magnitude is small. Runs and correlations measure different features, and neither excludes all nonlinear or state-dependent forecasting rules.

### Filter strategies

The filter rule buys after price rises by a specified percentage $y$ from a preceding low; it holds until a decline of $y$ from a subsequent high, then sells and takes a short position. A later rise of $y$ from a low reverses the position again. Replication requires a precise running-extremum update, trigger convention, executable fill rule, dividend treatment, shorting and financing assumptions, and a matched buy-and-hold benchmark.

Alexander's index experiments cover 1897–1959 with filters from 1% to 50%. Fama and Blume study individual Dow stocks with the same general kind of rule. Very small filters—0.5%, 1%, and 1.5% in the discussion—can beat buy-and-hold before costs, but their advantage per trade is small and turnover is high. The review reports that even a roughly 0.1% round-trip clearing cost, equivalent to ten basis points, removes the relevant advantage for floor traders. This is a historical cost calculation, not a current estimate of implementation shortfall.

Execution at the threshold is a consequential assumption. A price can jump across the trigger, making a fill at the exact filter price impossible. The p. 401 footnote explains that correcting Alexander's earlier threshold-fill assumption materially weakens profitability. A reconstruction should execute at an observed feasible crossing price under a stated timing convention; it should not credit the strategy with a price the market never offered. Missing original details about spread, borrowing, and financing should remain missing inputs rather than be silently filled with favorable assumptions.

The economic conclusion is conditional: the small dependencies documented by these tests did not yield reliable excess returns after the costs considered. It is not a proof that every possible algorithm, security universe, or subsequent period lacks predictable returns.

### Transaction prices and market microstructure

The Niederhoffer–Osborne evidence finds reversals between successive nonzero transaction-price changes two to three times as often as continuations. Transaction prices also cluster at integers, halves, quarters, and other fractions under the historical one-eighth-dollar tick. Conditional patterns involving strings of changes are more complicated than a simple independent sequence.

These observations do not immediately imply exploitable information. Alternation between bid and ask and the discrete structure of resting limit orders can make recorded transaction changes reverse even when no trader can buy and sell at those alternating prices in the advantageous direction. A trading test must use the side of the market the strategy can actually access.

The specialist's private view of the order book is different. The review describes it as a source of monopolistic information and reports specialist participation in about 24% of trading volume, with 83% of specialist sales above the preceding purchase price and 81% of purchases below the preceding sale price in the cited evidence. These percentages are descriptive transaction comparisons, not estimates of risk-adjusted alpha or net profitability. They nevertheless make a universal strong-form claim difficult to maintain. The institutional setting is the historical NYSE and should not be projected unchanged onto later electronic markets.

### Distributional assumptions

Fama discusses nonnormal stable distributions as an explanation of heavy tails and challenges routine normal approximations. In some stable laws the second moment does not exist. That changes what a sample correlation, its nominal standard error, and a Gaussian significance test can mean. The review also acknowledges competing finite-variance mixture approaches. Its treatment records the state of this debate in 1970, not a definitive modern choice of return distribution.

For reconstruction, the distributional issue has two practical effects: inferential calculations may be fragile, and rare large price moves alter filter-rule crossings and realizable returns. A backtest with Gaussian simulation noise is not automatically a replication of a heavy-tailed empirical experiment.

## Testing an explicit expected-return model: Treasury bills

The Roll discussion is useful because it illustrates a test with a structured risk-premium alternative. Here $r_{jt}$ denotes a one-week forward interest rate for a future lending interval beginning at $t+j-1$, rather than the stock holding-period return used above. The previously observed $r_{j+1,t-1}$ refers to that same future interval. Define its liquidity premium by

$$
L_{jt}=r_{jt}-E[r_{1,t+j-1}\mid\Phi_t].
$$

The conditional expectation restriction gives

$$
E[r_{jt}\mid\Phi_{t-1}]=r_{j+1,t-1}+E[L_{jt}\mid\Phi_{t-1}]-L_{j+1,t-1}.
$$

Thus predictable movements in the relevant premium can make raw forward-rate changes predictable without creating a pricing error. Pure expectations, liquidity-preference, and market-segmentation models impose different restrictions on these premiums. The review reports that liquidity-preference and segmentation specifications perform better than pure expectations, with a modest advantage to the former; appropriately adjusted residuals display little remaining dependence.

The lesson is methodological: the test becomes more informative after a risk-premium model is specified. The review does not reproduce all estimation coefficients, sample dates, and exact construction details needed to regenerate Roll's regressions. Those must come from the original study. A newly chosen spline, yield-curve estimator, or instrument universe would be an extension, not an exact replication.

## Semi-strong tests: the stock-split event study

The Fama–Fisher–Jensen–Roll split study provides the most developed event-study design in the review, pp. 404–407 and Figure 1. Its sample has 940 NYSE splits between January 1927 and December 1959, with a split ratio of at least five for four. A security must remain listed for at least twelve months before and after the split. This future-listing requirement is part of the research sample and would be a selection restriction if used to design a historical trading universe.

Monthly returns are adjusted using a market model,

$$
r_{jt}=\alpha_j+\beta_j r_{Mt}+u_{jt}.
$$

Let event month $m=0$ be the month in which the split becomes effective. It is not uniformly the announcement month. If $u_{jm}$ is a stock's event-time residual, construct

$$
\bar u_m=\frac{1}{940}\sum_{j=1}^{940}u_{jm},\qquad U_m=\sum_{k=-29}^{m}\bar u_k.
$$

Figure 1 plots cumulative average residuals from month −29 through month +30. The review describes the market-model approach but does not give every security-specific estimation-window and exclusion rule or all raw-data cleaning details. Reproducing the chart precisely requires the underlying study's implementation. In particular, the event-window information must not silently enter a supposedly real-time estimate of expected returns.

The all-split curve rises strongly before month zero and is approximately flat afterward. The smooth pre-event rise is not evidence that a split announcement causes 29 months of returns: only about 10% of the cases have more than four months between announcement and effective split. Firms tend to split during unusually good periods, and the positive residual months differ across individual firms. Aggregating in event time can yield a smooth curve without making each firm's next return predictable by a trading rule.

The study then partitions stocks by subsequent dividend behavior. A dividend “increase” means the firm's percentage dividend increase in the year after the split exceeds the corresponding increase for all NYSE securities; it is a relative classification, not simply a positive dividend change. There are 672 such cases, approximately 71.5% of the 940 observations. This uses future outcomes and is an explanatory sorting device, not information available at event month zero.

After the split, the dividend-increase group has a small additional rise in cumulative residuals. The other group declines noticeably; within roughly a year its curve returns to a level comparable to about five months before the split. The interpretation is that a split is associated with expectations of improved dividends. The market prices the average expectation by the end of the effective-split month; subsequent failures to meet it lead to unfavorable revisions.

This design supports rapid average incorporation of the information measured at monthly frequency. It does not establish an instantaneous intraday response, and its future-dividend grouping cannot be used as a contemporaneous signal. It also does not prove the dividend channel uniquely: joint news and endogenous split timing complicate causal attribution. A reproducible extension should distinguish an announcement-time study from this effective-date alignment and should state which question it is testing.

## Other public-information evidence

The Ball–Brown earnings study, as described here, uses 261 major firms over 1946–1966. A regression of a firm's annual earnings change on an aggregate earnings change separates expected from unexpected earnings; the residual sign classifies good and bad earnings news. A separate market model produces monthly return residuals around the earnings-announcement month. Cumulative residuals rise before good-news announcements and fall before bad-news announcements. The review estimates that only about 10–15% of the information in annual earnings is unanticipated by the announcement month. This is a statement about the reported historical decomposition, not a universal numerical limit on earnings surprise effects.

Waud examines daily S&P 500 price changes around Federal Reserve discount-rate announcements, relative to an average-return benchmark. The reported first-next-trading-day effect is no more than roughly 0.5%. Some adjustment precedes the announcement, consistent with anticipation or earlier information. The review does not specify a complete modern identification strategy separating policy surprises from contemporaneous macroeconomic news. Such a strategy would change the design substantially.

Scholes studies secondary offerings of existing shares and reports negative average residual price changes around the offering, on the order of 1–2%. The lack of a simple proportional relationship with the block's size is interpreted as evidence for an information effect rather than a mechanical supply effect. Corporate-insider sellers have the largest unfavorable price responses, with investment-company sellers next. These are observational comparisons and do not alone exclude all liquidity or selection explanations.

Public reporting of the seller's identity can occur about six days after the sale under the historical arrangement discussed. By that later time, subsequent residual changes look approximately random. That is consistent with fast incorporation by the time the information is broadly reported while also leaving room for profitable private information. The same review describes preliminary evidence on 696 new issues in 1926–1966: favorable pre-issue residual performance and much less systematic behavior after the issue. Exact original datasets, filters, and standard-error methods are not fully reproduced in this survey.

## Risk adjustment and mutual-fund performance

The conditional Sharpe–Lintner expected-return relation discussed on pp. 402–403 and 410–411 is

$$
E[r_{j,t+1}\mid\Phi_t]=r_{f,t+1}+\beta_{jt}\{E[r_{M,t+1}\mid\Phi_t]-r_{f,t+1}\},
$$

$$
\beta_{jt}=\frac{\operatorname{Cov}(r_{j,t+1},r_{M,t+1}\mid\Phi_t)}{\operatorname{Var}(r_{M,t+1}\mid\Phi_t)}.
$$

The theoretical market portfolio includes all relevant investment assets. An S&P 500 index is an empirical proxy. A statistical market-model regression does not establish this pricing restriction merely because it explains substantial variance. For example, King's study of 60 NYSE stocks over 1926–1960 attributes about half of return variance to a common market factor and no more than about another tenth to industry factors. Those are comovement results, not direct proof that expected returns obey the CAPM.

Fama distinguishes the market model's intercept from the equilibrium restriction. Constant beta and a suitable risk-free-rate treatment are needed to interpret a regression intercept as abnormal performance; the theoretical relation would require $\alpha_j=r_f(1-\beta_j)$ in the corresponding simple specification. Replacing the unobservable expected market return with the realized market return additionally requires a residual with zero conditional mean given the realized market return. Footnote 31 on p. 411 states this extra assumption. It is not a consequence of the ex ante CAPM equation alone.

### Jensen's sample and measurement

The reviewed experiment evaluates 115 mutual funds over the ten years 1955–1964. Return is measured as the nominal continuously compounded ten-year return: the logarithm of terminal wealth divided by initial wealth. Historical nominal annual continuously compounded returns estimate risk, and the S&P 500 serves as the market proxy. The comparison is against a line formed from riskless and market-portfolio combinations with matching estimated beta.

The reported results are:

| Return treatment | Funds below the comparison line | Mean ten-year return deviation |
|---|---:|---:|
| Investor returns including loading charges and fund expenses | 89 of 115 | −14.6% |
| Loading charges excluded | 72 of 115 | −8.9% |
| Other reported expenses added back, before a brokerage correction | 58 of 115 | −2.5% |
| Estimated brokerage expenses also added back | Not separately reported here | +0.09% |

These deviations use the ten-year continuously compounded metric; they are not annual percentage-point alphas. For example, a log-wealth difference of −.146 corresponds to $\exp(-.146)-1$, approximately −13.6%, in a matched individual wealth ratio. Because the table reports an average log deviation across funds, this conversion should not be represented as the exact arithmetic average of their wealth shortfalls.

Brokerage expenses are not observed precisely for every individual fund. The correction uses average fund turnover information from 1953–1958. Thus the near-zero gross result is partly an estimated cost adjustment. One cannot reconstruct exact individual gross alphas from the review alone or interpret +0.09% as a precisely estimated economic surplus.

The paper also reports little persistence: superior performance in one subperiod generally does not predict superior performance in another. The number of very positive fund deviations is smaller than one would expect from chance variation among 115 funds under the stated no-skill premise. The review does not provide all test statistics and uncertainty estimates necessary to rebuild a modern multiple-testing or selection-adjusted analysis. Absence of clear average skill in this sample is weaker than proof that no fund ever has useful information. Fama explicitly recognizes the limited precision of such an inference.

## A disciplined reconstruction and the limits of the conclusions

To use the framework in a new study, first define exactly what an investor knows at each decision time. Specify the normal-return model separately, including estimated versus realized market returns, risk exposure, the risk-free asset, and whether parameters can vary. Then identify the observable implication: a zero conditional residual mean, a post-event return pattern, or net performance of a feasible rule. Implement timing, costs, and sample restrictions before calculating the statistic. A prediction based on an eventual dividend category or a future listing requirement is not a real-time forecast.

For direct replication of a historical result, retain the original sample, event definition, holding interval, and return convention. The monthly split-event cumulative residual, the daily filter-rule profit, and the ten-year fund log-return deviation answer different questions. Combining them into one “efficiency score” would erase their maintained assumptions. When the review omits original estimation windows, data exclusions, execution assumptions, or uncertainty calculations, consult the cited primary study rather than invent them.

Fama's historical assessment favors much of the weak- and semi-strong-form evidence, while accepting strong-form exceptions for groups such as corporate insiders and exchange specialists. The important research implication is not that a statistically significant return relation automatically disproves efficient pricing, nor that a failed strategy establishes it. Information, equilibrium compensation, measurement, and implementation must be specified together. That is the article's lasting contribution to reproducible testing, even where later data or different asset-pricing models could change its empirical verdicts.

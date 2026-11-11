# Speculation or hedging in the Irish stock exchange

Brian M. Lucey, Applied Financial Economics Letters 1(1), 2005, pp. 9–14; published online August 16, 2006. DOI 10.1080/1744654052000314653. Source: [Hedging_Lucey_2006.pdf](../../Finance/Hedging_Lucey_2006.pdf), seven PDF pages including publisher cover.

## Why this matters

The paper tests whether the volume-conditioned autocorrelation of stock returns identifies speculative rather than hedging motives in the Irish market. Its main contribution is a specification check: an apparently supportive simple regression changes materially when conditional volatility, heavy-tailed errors, and volume in the variance equation are introduced. The result is a warning against interpreting the sign of one reduced-form coefficient as an invariant label for investor motives.

The model mechanism comes from Llorente and coauthors, not a new equilibrium derived by Lucey. Hedging trades reallocate risk without changing fundamentals and may induce a temporary price concession followed by reversal. Informed speculation gradually impounds private information and may produce continuation. High volume distinguishes these trades from the model's normal-volume response to public news. The Irish application asks whether this interpretation travels to another market and survives alternative econometrics.

## Return and cross-sectional models

For stock $i$, let $R_{i,t}$ be its daily return and $V_{i,t}$ excess turnover. The simple regression, equation (1), is

$
R_{i,t}=a_i+b_{1i}R_{i,t-1}+b_{2i}V_{i,t-1}R_{i,t-1}+e_{i,t}.
$

The conditional autoregressive slope is $b_{1i}+b_{2i}V_{i,t-1}$. A positive $b_{2i}$ means higher prior turnover is associated with more continuation, interpreted as speculation under the maintained theory. A negative value means relatively more reversal, interpreted as hedging. A negative interaction coefficient does not imply negative autocorrelation at every turnover level, because the intercept slope $b_{1i}$ also matters.

Equation (3) adds a contemporaneous market-index return. The ISE-General or ISE-Financial index is selected according to whether the stock is nonfinancial or financial. This controls some common market variation but does not guarantee that residual cross-stock dependence vanishes. The source does not replace the original return interaction with an interaction based on fully residualized idiosyncratic returns.

A second-stage cross-sectional regression is

$
\widehat b_{2i}=c+g_1\operatorname{MEANMV}_i+g_2\operatorname{SOLO}_i+u_i.
$

MEANMV is the company's mean market capitalization over the sample. SOLO equals one if the company is listed only in Ireland and zero otherwise. Thirteen of the 52 companies have sole Irish listings; others are mostly also listed in London, with Iona Technologies on Nasdaq. The author predicts negative coefficients on both information-asymmetry proxies. The negative size prediction reflects lower asymmetry for large companies. The negative SOLO prediction is asserted in the source; it should not be silently reinterpreted as the opposite hypothesis on the basis of a generic intuition about cross-listing.

The dependent variable is itself estimated in a time-series regression. The paper discusses correlated shocks but does not report a complete generated-regressor covariance correction, precision weighting of individual estimates, or a joint panel model. Cross-sectional significance should be read within those limitations.

## Conditional-volatility extension and a damaged specification

Equation (4a) adds the square root of lagged conditional variance to the simple mean equation and uses Student-$t$ innovations. The variance equation is described as a leveraged GARCH model including lagged excess volume, intended to allow information-arrival activity to explain persistence otherwise assigned to volatility dynamics.

The printed equations on p. 11 are internally problematic. They equate $R_t$ with the innovation after separately specifying a nonzero conditional mean, repeat the same coefficient subscript on distinct variance terms, include contemporaneous squared error and squared lagged variance, and define the leverage indicator using $h_{t-1}\leq0$. If $h$ is a conditional variance, that last condition does not encode the usual negative-return or negative-shock asymmetry. These defects are visible in the PDF, not merely text-extraction errors.

Accordingly, the exact reported GARCH recursion cannot be reconstructed unambiguously. Replacing it with a standard GJR-GARCH or another familiar specification would be a proposed repair, not a verified reproduction. The paper omits code, parameter constraints, starting values, degrees-of-freedom estimates, optimization tolerances, and full per-stock diagnostics. It says poorly fitting models were retained for consistency. This is a material reproducibility limitation for the result most responsible for reversing the conclusions.

## Sample and volume construction

All 52 companies on the Irish Stock Exchange Official List are included. Daily price and volume data begin January 1, 2000 and are supplemented through December 2003 from the exchange website. XETRA trading began June 7, 2000; prior records measured volume by bargains. The article does not fully explain harmonization across this measurement change.

Turnover is the daily percentage of outstanding shares traded. Excess turnover subtracts a 50-day moving average. A reproduction must determine whether the current day is included in that average, how initial observations are handled, and whether volume includes trading on other listing venues. The source does not specify those choices. Return adjustment for dividends, splits, stale prices, holidays, and currency units also lacks an executable data recipe.

Table 1 identifies companies by numbers rather than names. It reports a cross-company average daily return of $-.012\%$, mean market value of 2,806.4 million euros, and unadjusted daily turnover .213% of shares outstanding. Some large firms have turnover rounded to .000%, which is relevant to possible venue coverage and scaling but does not establish the reason for those observations. The text says all data have unit roots and volume is autocorrelated at one lag; detailed tests are available on request, so which transformed series those statements concern cannot be fully audited.

## Results and internal count checks

The source reports 22 of 52 stocks with positive interaction coefficients under the simple model, about 42%, and 25 of 52 under the market model, about 48%. These are sign classifications, not 22 or 25 statistically significant positive coefficients. Table 2 separately marks significance, with many sign labels marked No.

The prose describes the GARCH model as having 10 of 52 speculative stocks, or 24%. That arithmetic is inconsistent: 10/52 is 19.2%. Reading the displayed GARCH classifications in Table 2 gives speculative labels for companies 2, 3, 7, 9, 20, 24, 43, 44, 45, and 47, confirming ten labels. Only companies 2, 20, and 45 have significant speculative labels in that column. The remainder of the ten do not demonstrate statistically distinguishable positive effects under the table's significance convention, which is not fully detailed.

The statement that only four stocks maintain their classification across all three models is also too broad if classification means only the printed speculation/hedging sign. Numerous rows, including 4, 5, 6, 8, 11, 12, and 14, remain hedging across all columns. The text may be referring to a narrower significance-based subset, but does not define it clearly. A reproduction should report sign stability and significance stability separately rather than adopt the ambiguous count.

Table 3 provides the main cross-sectional comparisons:

| Time-series specification | Intercept | Mean-market-value coefficient | SOLO coefficient | $R^2$ |
|---|---:|---:|---:|---:|
| Simple | 955.88 | negative, rounded -.00 | -1437.55 | .74 |
| Market adjusted | 963.04 | negative, rounded -.00 | -1272.20 | .81 |
| GARCH | -.06 | positive, rounded .00 | .04 | .16 |

The Sig. entries for SOLO are .03, .03, and .02. For mean market value they are .00, .00, and .10. Treating these as reported significance probabilities, .00 is rounded rather than exactly zero, and the GARCH size coefficient is at most borderline at 10%. The large scaling difference between simple-model and GARCH coefficients is not reconciled in the article. Full precision and dependent-variable scaling are needed to compare economic magnitudes.

The simple and market-adjusted results align with the paper's predicted negative proxy signs and have high cross-sectional fit. The GARCH results reverse signs and explain much less variation. That is the paper's key empirical finding. It does not establish that the GARCH labels reveal the true individual motives while the simpler labels are false; specification changes and estimation problems themselves may drive disagreement.

## Implications and replication priorities

A faithful replication first needs named securities, actual daily observations and venue coverage, the turnover normalization and 50-day convention, the market-index mapping, and unrounded first-stage coefficients and covariance estimates. Reproducing the conditional-volatility result additionally requires clarification or code correcting equation (4). A repaired model should be presented alongside the literal source limitations, with model diagnostics and sensitivity to thin trading, not passed off as the published equation.

The article proposes stock-specific time-series models and pooled cross-venue volume as future work, while acknowledging reduced comparability and sample size. Its durable result is the sensitivity of a motive interpretation to the econometric treatment of volatility and trading activity. There is no out-of-sample portfolio, transaction-cost analysis, direct trader-identification experiment, or verified causal separation of hedging and private-information trades.

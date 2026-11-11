# The Performance Persistence of Equity Long/Short Hedge Funds

**Markus M. Schmid and Samuel Manser. Working-paper version dated 31 October 2008.** [Source PDF](../../Finance/HedgeFunds_ShmidManser2008.pdf). The original filename misspells Schmid; the title and author identity here follow the document. All 26 pages, including the references, were read. The factor equation, data-selection passages, Tables 1–6 and Figures 1–3 were checked visually. Page references use the supplied PDF's printed numbering. The division slash in this note's filename substitutes for the title's filesystem-reserved slash only.

## Why this matters

A manager-selection process based on recent absolute returns can select factor exposure rather than persistent manager value added. This paper makes that distinction within equity long/short hedge funds, using annual portfolio formation rather than pooling unlike hedge-fund styles. It asks whether funds ranked on information available before the holding period subsequently earn different returns or different factor-model alphas.

Sorting on the previous year's raw return produces a monthly winner-minus-loser excess-return spread of 0.39%, but a four-factor alpha spread of −0.04%, neither statistically significant. The return spread is largely explained by the winners' exposure to stock momentum. Sorting instead on an alpha estimated over the preceding 24 months produces a significant monthly alpha spread of 0.79%, with the high-alpha decile itself earning 0.71% monthly alpha. That is the paper's central historical finding.

The evidence is conditional on the benchmark, database and implementation assumptions. It is not proof that investors could short the losing funds, obtain timely access to winners, or earn the full spread after fund-of-funds expenses and redemption costs. Nor does persistence in a fitted alpha establish that the underlying manager characteristic is skill: a persistently omitted exposure can also generate persistent estimated alpha. The authors explicitly raise that possibility.

## Research design and contribution

The method adapts the Hendricks–Patel–Zeckhauser portfolio-ranking design, also used by Carhart, to one relatively homogeneous hedge-fund strategy. It uses observed past characteristics to form portfolios, then evaluates the subsequent portfolio-return time series. Diversifying individual residual risk and using a long sequence of annual portfolio vintages can make portfolio-level exposure estimates more precise than short regressions on individual funds.

Restricting the universe to equity long/short funds is consequential. A common factor model fitted across unrelated hedge-fund strategies can classify an omitted strategy exposure as alpha and put one whole style in the winning portfolio. Within a single broad strategy, a small equity-factor set explains more of the return variation with fewer estimated parameters. The paper still recognizes that “equity long/short” contains heterogeneous dynamic strategies and that option-like exposures may remain.

The main comparisons are raw-return rankings, two-year alpha rankings and one-year Sharpe-ratio rankings. Additional, mostly unreported exercises use one- and three-year alpha windows, alpha $t$-statistics, market beta, option factors, market-timing factors, subsamples and stale-price adjustments. These are robustness and diagnostic comparisons, not independent preregistered tests. The PDF does not supply a multiple-testing adjustment across all the explored sorts.

## Database, filters and chronology

CISDM supplies monthly net-of-fee returns, assets, inception dates and self-reported strategy classifications. Coverage includes both surviving and defunct managers. The initial database description gives 4,390 non-fund-of-funds vehicles, of which 2,210 are inactive; equity long/short accounts for 1,693 funds, of which 901 are inactive. The study uses January 1994–December 2005, a 144-month calendar window, because the provider did not systematically retain defunct funds before 1994.

The reported filters remove duplicate records identified by matching fund name and company ID, restrict returns to U.S.-dollar funds, exclude funds without observations during the sample, delete each fund's first twelve observations to mitigate backfill, and require enough remaining history for the formation statistic. The selection bullets report 85 funds removed by the duplicate/currency step, 35 by the date restriction and 423 for insufficient history, leaving 1,150 funds. Those numbers reconcile from 1,693: $1693-85-35-423=1150$.

However, the preceding paragraph separately says that 1,649 funds are classified as equity long/short in the 1994–2005 period. Starting the same subtraction at 1,649 gives 1,106, not 1,150. The PDF does not provide a fund-level flow table that reconciles that intermediate count. The final reported universe is 1,150; a replication should preserve the discrepancy rather than silently invent an extra inclusion rule.

The first-twelve-observations deletion is a fixed proxy for backfill, not a deletion based on known reporting-entry dates. It may remove genuine live observations or retain more than twelve backfilled months. Including dead funds mitigates survivorship selection but cannot restore unreported terminal losses. Funds disappear from the portfolios when they stop reporting, with weights reassigned to the remaining members. Stopping to report and economically liquidating are not identical events.

Timing must also be explicit. Raw-return and Sharpe portfolios are formed each January from 1995 through 2005 and held during that January–December year, producing a reported 132-month evaluation series. Two-year alpha portfolios start in January 1996 and run through December 2005, giving 120 calendar months. The first-twelve-observations deletion must be tied to each fund's original reporting history; the source does not fully specify its order relative to the 1994 truncation or how early eligible funds are reconciled with that deletion. Deleting every fund's first twelve *post-January-1994* observations would prevent those observations from forming a complete 1994 ranking history. Exact code and dated fund records are needed to resolve this boundary condition.

## Constructing the ranking portfolios

For formation year $y$, estimate the ranking characteristic using observations strictly before January of $y$. Rank eligible funds from highest to lowest into ten portfolios. Portfolio 1 contains the top decile and portfolio 10 the bottom decile. Split each extreme decile into three further groups, called 1A, 1B, 1C and 10A, 10B, 10C, so that 1A and 10C are the most extreme winners and losers. The displayed spreads are portfolio 1 minus portfolio 10 and portfolio 1A minus portfolio 10C.

The paper says portfolios are equally weighted and weights are readjusted when a constituent disappears during the holding year. Under the standard monthly equal-weight interpretation, their excess return is

$$
x_{d,t}=\frac{1}{N_{d,t}}\sum_{i\in\mathcal P_{d,y}(t)}(r_{i,t}-r_{f,t}),
$$

where $\mathcal P_{d,y}(t)$ contains the still-reporting members of the January portfolio and $N_{d,t}$ is its size. This formula is an implementation of the equal-weight description. The PDF does not completely document within-year wealth drift versus rebalancing, how a missing intermediate month differs from a permanent exit, or the exact return assigned at exit. These choices must be fixed before reproducing the table cells. New entrants should not be inserted midyear simply because they later become eligible.

For a raw-return score, a natural construction is the prior calendar year's compounded total return, $\prod_{s\in y-1}(1+r_{i,s})-1$. The source calls the score a lagged one-year raw return without spelling out aggregation, so a compound-versus-arithmetic check is needed for exact replication. This ranking score is distinct from the mean monthly **excess** returns reported for the subsequent portfolios.

For the principal alpha score, regress each eligible fund's excess returns over the preceding 24 months on the four factors and rank the intercept estimate. The conventional one-year Sharpe score is the mean monthly excess return divided by its sample standard deviation over twelve months. Annualizing all such ratios by the same positive $\sqrt{12}$ does not change their ordering. A fund-specific choice of risk-free rate, treatment of missing observations or annualization under serial correlation could change the effective comparison; the original implementation is not supplied.

## Factor model and inference

The main reported benchmark is Carhart's four-factor model:

$$
x_{i,t}=\alpha_i+\beta_{i,M}RMRF_t+\beta_{i,S}SMB_t
+\beta_{i,H}HML_t+\beta_{i,U}MOM_t+\varepsilon_{i,t}.
$$

$RMRF$ is the value-weighted NYSE/AMEX/NASDAQ return less the one-month Treasury-bill rate. $SMB$ and $HML$ are the size and book-to-market factor-mimicking returns; $MOM$ is the one-year momentum factor. Use the same return units for the dependent series and all factors. In the printed tables, excess means and intercepts are monthly percentages, whereas slope coefficients are dimensionless. Thus alpha 0.71 means 0.71% per month, not 71% or 0.71% annually.

The extended specification adds out-of-the-money S&P 500 call and put return factors supplied by Agarwal and Naik. The authors say their loadings are generally insignificant, add little explanatory power and barely change the other estimates. Their available history ends in January 2005, eleven months before the main sample, so the option factors are omitted from the principal portfolio tables. The PDF does not reconstruct their strike selection, expiration roll or financing; exact option-factor replication requires those external series or their original construction.

At the CISDM median equity-long/short index level, Table 1 reports monthly alpha 0.33% with options and 0.34% without, both significant at 1%. Market slopes are 0.41 and 0.45, while $HML$, $SMB$ and $MOM$ are about 0.06, 0.20 and 0.07. Adjusted $R^2$ is 0.82 in both specifications. The option-coefficient columns are explicitly marked with $10^{-3}$ scaling. The option data's early endpoint means the broad 1994–2005 caption should not be read as proof that both specifications have identical effective dates. The uninvestable median index is descriptive context, not the same object as the strategy formed from individual funds.

Table stars denote Newey–West-corrected significance: one, two and three stars correspond to 10%, 5% and 1% tests. The kernel bandwidth/lag choice and any finite-sample adjustment are not specified. The reported tests concern the concatenated postformation portfolio series. They are not tests obtained by averaging individual funds' formation-window $t$-statistics. A long-minus-short alpha must be estimated from the spread series or with its full covariance; subtracting two separately computed standard errors is invalid.

## Raw-return winners: a factor-driven spread

Table 2's key monthly results are:

| Portfolio | Mean excess return | Four-factor alpha | Market beta | Size beta | Momentum beta | Adjusted $R^2$ |
|---|---:|---:|---:|---:|---:|---:|
| Highest-return decile 1 | 0.92% | 0.22% | 0.68 | 0.44 | 0.35 | 0.69 |
| Lowest-return decile 10 | 0.53% | 0.26% | 0.61 | 0.21 | −0.26 | 0.63 |
| 1 minus 10 | 0.39% | −0.04% | 0.07 | 0.23 | 0.60 | 0.48 |
| Extreme 1A minus 10C | 0.56% | −0.06% | 0.04 | 0.23 | 0.96 | 0.51 |

Neither displayed alpha spread is significant. The momentum slopes on the two spreads are significant at 1%. The decile-spread size slope is significant only at 10%. Given the paper's monthly momentum-factor mean of 0.84%, the rounded loading contribution $0.60\times0.84\%=0.504\%$ already exceeds the 0.39% raw spread. Other factor contributions and alpha offset part of it. This is an attribution using sample averages, not evidence that every winner manager intentionally pursues an identical momentum strategy.

The return ranks are not monotonically ordered out of sample: for example, decile 3 earns 0.99% per month against decile 1's 0.92%. Several middle deciles have significant alpha while the top raw-return decile does not. Portfolio diversification prevents inferring every constituent's volatility directly from its decile's volatility; the source itself makes this qualification.

The text calls the 0.39% monthly spread 4.78% annually. The printed monthly value gives $12\times0.39\%=4.68\%$ under arithmetic annualization, while $(1.0039)^{12}-1=4.7817\%$. The latter explains the reported figure as a compounded equivalent of a constant monthly spread. It is not the actual compounded return of the realized long-minus-short strategy, which requires the monthly path and a defined capital base.

### The parenthetical dispersion ambiguity

The return column is headed “exc. ret (std. dev)”; for portfolio 1 it shows 0.92 (0.46). Yet the source's printed probability calculation on page 13 uses

$$
P(X>0)=\Phi\left(\frac{0.92}{0.46\sqrt{132}}\right)\simeq0.5691.
$$

That calculation treats 0.46 as a standard error of the mean and recovers monthly volatility as $0.46\sqrt{132}\%=5.285\%$. If 0.46% were instead the monthly standard deviation, the same Gaussian calculation would give $\Phi(2)=97.7\%$, not 57%. The formula and table label therefore cannot both describe 0.46 as unscaled monthly volatility. This note preserves the table's means and significance statements but does not use those parenthetical entries as certified monthly volatilities or to manufacture Sharpe ratios. Moreover, because the mean column is excess return, the displayed calculation naturally concerns beating cash, rather than a positive total return, unless the authors switch return conventions without stating it.

## Alpha rankings: stronger next-year separation

Table 3 sorts on 24-month alpha and evaluates the subsequent annual portfolios. Selected results, all means and alphas in monthly percent, are:

| Portfolio | Mean excess return | Alpha | Alpha significance | Market beta | Adjusted $R^2$ |
|---|---:|---:|---|---:|---:|
| Highest-alpha decile 1 | 1.02% | 0.71% | 1% | 0.48 | 0.63 |
| Decile 2 | 0.82% | 0.40% | 1% | 0.44 | 0.71 |
| Decile 3 | 0.85% | 0.47% | 1% | 0.49 | 0.78 |
| Decile 8 | 0.79% | 0.42% | 1% | 0.51 | 0.75 |
| Decile 9 | 0.42% | −0.11% | Not significant | 0.60 | 0.81 |
| Lowest-alpha decile 10 | 0.51% | −0.08% | Not significant | 0.80 | 0.77 |
| 1 minus 10 | 0.52% | 0.79% | 1% | −0.32 | 0.23 |
| Most extreme winner 1A | 1.38% | 1.37% | 1% | 0.32 | 0.24 |
| Most extreme loser 10C | −0.19% | −0.95% | 1% | 1.18 | 0.69 |
| 1A minus 10C | 1.57% | 2.32% | 1% | −0.85 | 0.41 |

The decile spread is not simply a higher-beta winner portfolio. Its market slope is −0.32, significant at 1%, and its momentum slope is −0.07, significant at 5%. The high-alpha decile earns more raw return while loading less on the market than the lowest-alpha decile. Its 0.71% monthly alpha is 8.52% under arithmetic annualization; the 0.79% spread corresponds to 9.48%. These annualized translations are derived scale conversions, not separately reported realized annual returns.

The ordering is imperfect: decile 8 outperforms several higher-ranked groups, and extreme winner 1A has adjusted $R^2$ only 0.24. That weak fit makes the extreme 1.37% alpha particularly dependent on whether the factor set is adequate. The small number of managers in an extreme third of a decile also makes access, concentration and measurement error more consequential. The PDF does not report the annual constituent counts needed to quantify those issues.

A 36-month formation alpha yields a smaller, insignificant 0.44% alpha spread, while a 12-month estimate yields a significant 0.67% spread but a less orderly portfolio pattern. The authors offer two explanations for the three-year weakening: fewer qualifying funds reduce precision, and older alpha is less informative. These alternatives are not separated experimentally. A $t$-statistic ranking yields reported spreads of 0.84% in alpha and 0.58% in returns. The paper equates that ranking with an appraisal-ratio ranking; exact equivalence requires common regression design/sample length and standard-error scaling. It need not hold with arbitrary fund-specific HAC covariance corrections.

## What the transition figures do and do not show

For a formation decile $d$, estimate transition probabilities by counting whether its funds are in decile $k$ at the next annual ranking or no longer report. The “out” outcome should remain a separate category, rather than conditioning it away. Figure 2a shows substantial mobility under raw-return rankings: winners and losers can swap extremes, and poor performers are more likely to stop reporting. Figure 2b shows the initial return dispersion collapsing after formation; beyond the first holding year there is no evident raw-return persistence.

The alpha-ranking transition matrix in Figure 3a is more concentrated near the diagonal. The top alpha decile retains over 30% of its funds at the next ranking, and transitions directly between top and bottom alpha deciles are uncommon. This is descriptive rank persistence. Because successive two-year formation windows ordinarily share twelve months, part of diagonal stability can be mechanical. The subsequent-year portfolio-alpha test uses new holding-period returns and is more informative than the overlapping-score transition matrix about forward performance.

Figure 3b follows original alpha-ranked cohorts for several years. The source reports that the worst performers remain relatively poor for two years and that the second-year alpha spread reaches 0.97%, significant at 5%. It also states that winner and loser alphas individually are insignificant after the initial tracking year. Therefore a significant relative spread is not evidence that buying winners alone continues to deliver significant positive alpha in years two through four. The figure's axis is labeled alpha, although its caption's final sentence refers to monthly excess returns; the surrounding analysis and axis support interpreting it as alpha. The plotted curves are not a substitute for the unprovided monthly cohort series.

## Sharpe sorting and the distinction between a good portfolio and a significant spread

Table 4 ranks on the preceding year's Sharpe ratio. The highest-Sharpe decile has mean excess return 0.79%, alpha 0.45%, market beta 0.25 and adjusted $R^2$ 0.60. Its alpha is significant at 1%. The lowest-Sharpe decile has mean 0.48%, alpha 0.18% and market beta 0.47. Alphas for deciles 1–6 are positive and significant; decile 9 is also significant, so the ordering is not monotone.

The decisive qualification is that the top-minus-bottom alpha is only 0.26% and has no significance star. The extreme 1A-minus-10C alpha is 0.50%, also unstarred. Thus finding a significant alpha for the high-Sharpe portfolio is not the same as establishing significant alpha separation between high- and low-Sharpe portfolios. The four-factor alpha ranking supplies stronger direct spread evidence. Detailed Sharpe transition matrices and multiyear Sharpe paths are not printed; the authors offer them on request.

## Regime and smoothing checks

The alpha-sorted portfolios are split at March 2000. The relevant first evaluation subperiod is January 1996–March 2000, not January 1994, because the principal alpha sorts need two prior years. The second is April 2000–December 2005.

| Evaluation period | High-decile mean | High-decile alpha | Low-decile alpha | Spread alpha |
|---|---:|---:|---:|---:|
| Jan 1996–Mar 2000 | 1.87% | 1.15%, significant at 1% | 0.32%, insignificant | 0.83%, significant at 5% |
| Apr 2000–Dec 2005 | 0.40% | 0.26%, insignificant | −0.43%, significant at 10% | 0.69%, significant at 1% |

The later spread is supported materially by avoiding poor performers; the winner-only alpha is not significant. The first period's spread mean is 0.25%, compared with 0.72% later. Therefore “alpha persists in both periods” should be read as a statement about the relative portfolios, not uniformly significant standalone winners. An unreported exercise removes the first two years of the second regime so that formation windows also lie entirely after the breakpoint; the authors say results are qualitatively unchanged.

For stale prices, the paper estimates the Getmansky–Lo–Makarov MA(2) smoothing model for individual funds and reconstructs unsmoothed returns before repeating the alpha sort. A standard representation that clarifies the required operation is

$$
r^{obs}_{i,t}=\theta_{i,0}r^*_{i,t}
+\theta_{i,1}r^*_{i,t-1}+\theta_{i,2}r^*_{i,t-2},
\qquad \sum_{j=0}^{2}\theta_{i,j}=1.
$$

Given coefficients and starting values, inversion takes the recursive form

$$
\hat r^*_{i,t}=\frac{r^{obs}_{i,t}
-\hat\theta_{i,1}\hat r^*_{i,t-1}
-\hat\theta_{i,2}\hat r^*_{i,t-2}}{\hat\theta_{i,0}}.
$$

These equations reconstruct the cited method's basic operation; they are not equations printed or fully parameterized in this PDF. The source does not give the likelihood, coefficient constraints, invertibility treatment, initialization or whether smoothing parameters use only past observations at each formation date. A small $\theta_{i,0}$ can amplify noise. Consequently the reported robustness is not a certified, fully specified real-time trading implementation.

Table 6 nevertheless gives a useful numerical check: unsmoothing changes the top-decile alpha from 0.71% to 0.66%, the bottom from −0.08% to −0.13%, and the spread from 0.79% to 0.80%; top and spread remain significant at 1%. Extreme alphas become 1.33% and −0.99%, retaining their 2.32% spread. An alternative lagged-factor correction is said to leave the patterns intact, but its portfolio-level coefficient tables are not supplied. At the index level, a footnote reports that including lagged factors raises adjusted $R^2$ to 0.84 and reduces alpha from 0.33% to 0.28%, still significant.

## Reproduction boundary and interpretation

A complete rerun requires the historical CISDM fund panel with original identifiers, currencies, dates, classifications, dead-fund records and reporting-entry information; the exact monthly factor vintages; and code resolving eligibility, ties, percentile cutoffs, missing months, reweighting and terminal returns. It also requires the Newey–West bandwidth and the MA(2) estimation details. The printed tables alone cannot resolve the sample-count discrepancy, the dispersion-label ambiguity or the timing of smoothing-parameter estimation.

The selection and evaluation stages should be saved separately: a dated formation file containing each eligible fund's past-only score and decile; a holding-period membership file including exits; and the resulting monthly decile and spread returns. Regressions should then be run on those return series with a common declared date window. This separation exposes accidental use of later fund status, revised histories or future smoothing estimates. It also makes the 12-, 24- and 36-month comparisons attributable to both score design and changes in the eligible universe.

The practical result is narrower than a tradable long-short alpha opportunity. Underlying fund returns are already net of manager fees, but the tests do not charge the allocator's trading, administration, borrowing or additional fee layer. Shorting the loser portfolio is generally unavailable. Lockups, notice periods and closed funds can prevent annual switching even when the data make it appear possible. A winner-only strategy captures much of the full-sample alpha spread, but that conclusion weakens in the later subperiod.

The paper supports investigating past factor-adjusted performance rather than chasing absolute winners in this historical equity-long/short universe. It leaves the distinction between skill and benchmark misspecification, the true effect of reporting biases, and the net attainable performance of a constrained allocator unresolved.

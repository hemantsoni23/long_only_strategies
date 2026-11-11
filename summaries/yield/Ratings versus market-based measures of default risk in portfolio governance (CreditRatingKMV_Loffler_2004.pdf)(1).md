# Ratings versus market-based measures of default risk in portfolio governance

Gunter Löffler, *Journal of Banking & Finance* 28 (2004), 2715–2746. DOI: 10.1016/j.jbankfin.2004.06.007. Source: [CreditRatingKMV_Loffler_2004.pdf](../../Finance/CreditRatingKMV_Loffler_2004.pdf), 32 pages, including data corrections and portfolio-risk appendices. References below use journal pages and table numbers.

## Why this matters

A credit signal can be a better short-horizon default predictor yet a worse trigger for compulsory portfolio trading. The distinction is the paper's central contribution. It compares Moody's ratings with Moody's KMV expected default frequencies, EDFs, as inputs to purchase and sale restrictions. Rating stability can save turnover, while a market-based signal can react earlier. Which is preferable depends on eligibility thresholds, how long violations are tolerated, investment horizon, transaction costs, and whether performance means default losses, total returns, or downside risk.

This is an empirical simulation of governance rules using historical issuer information and actual default events. It is not a backtest using observed bond returns. The return extension assigns hypothetical bond prices from EDFs. That qualification matters because trading following a downgrade can crystallize a market loss before default; a default-count experiment alone treats a timely sale as escaping that loss without marking down the bond.

The results reject a simple claim of universal market-signal dominance. Tight EDF cutoffs reduce one-year buy-and-hold default losses, but investment-grade ratings perform better at five years. Immediate sale rules can favor ratings even before costs, and their lower turnover becomes valuable after costs. Adding a gap between the EDF purchase and sale thresholds substantially improves EDF governance. These are comparisons among specified rules, not a demonstration that the chosen ratings or EDF thresholds are optimal.

## Inputs and admissible universes

The matched monthly data contain a Moody's long-term rating and an EDF for every issuer-month. EDF is a commercial estimate of one-year physical default probability incorporating balance sheets, equity value, and equity volatility. US and non-US corporate issuers are included. Data extend from 1980 through 2002, but the experiment starts in 1983 to avoid artificial migrations when Moody's introduced rating modifiers in 1982.

There are 297,645 issuer-months in the analysis. The issuer count rises from 461 in 1983 to 1,960 in 2002. It is a changing universe, not a balanced panel. The paper defines five purchase universes:

| Rule | Meaning | Issuer-months | Mean EDF | Median EDF |
|---|---|---:|---:|---:|
| Rating better than Ba1 | Baa3 or better, investment grade | 175,318 | 0.41% | 0.17% |
| EDF at most 0.50% | Tight market-risk cutoff | 166,224 | 0.17% | 0.14% |
| EDF at most 0.75% | Larger low-risk universe | 190,839 | 0.23% | 0.17% |
| EDF at most 2% | Broader market-risk universe | 240,433 | 0.44% | 0.25% |
| Rating better than B1 | Ba3 or better | 239,857 | 0.76% | 0.26% |

Table 1 motivates comparisons without making them exact risk matches. The 0.50% cutoff is near the historical 0.49% Baa3 one-year default rate. The 0.75% rule has the same median EDF as investment grade, but a much lower mean. The 2% rule approximately matches the observation count of the better-than-B1 universe and approximately matches the average EDF of investment grade. Matching counts, medians, and means produces different comparisons; none simultaneously holds all exposures constant.

The low-risk results rely on few defaults. Table 1 records 22 issuers defaulting within one year after investment-grade inclusion, versus 25 following inclusion under EDF at most 0.50%. These counts cannot simply be divided by issuer-month counts to form annual default rates: the units and repeated inclusion windows differ.

## Data cleaning and information timing

Appendix A, pp. 2744–2745, supplies three important corrections. First, EDFs are floored consistently at 0.02%; the commercial minimum had been 0.01% until April 1997 and 0.02% thereafter. Second, missing EDFs are linearly interpolated only if the rating did not change across the gap, the issuer never defaulted after the gap, the gap spans at most three months, and the EDF percentage change across it is less than 25%. This adds 608 observations. Third, 411 suspicious observations with EDF exactly 20% are removed when followed by a decline of more than 18 percentage points and the rating is better than A3. Many occurred for highly rated firms before February 1988.

These corrections use future information. The interpolation criterion includes all subsequent default experience, and identifying a spurious 20% value uses its subsequent jump. They are retrospective database repairs, not rules executable at the historical month-end. A modern reconstruction should distinguish reproducing the published cleaned sample from a strictly point-in-time investment test; silently treating this cleaned panel as entirely contemporaneously available would overstate the design.

During simulation, an issuer with no observation in month $t+1$ is replaced in month $t$ without trading cost. The source tests whether such missingness predicts default using 22,059 non-overlapping December observations. The missingness coefficient alone is 0.131 with a t-statistic of 1.89. Controlling for investment-grade eligibility makes it −0.059, t-statistic −0.79; controlling for the tight EDF cutoff gives 0.047, t-statistic 0.63. This reduces concern about gross selection correlated with the particular eligibility cutoffs. It does not eliminate all selection or the use of next-month availability in the replacement rule.

The database itself, issuer identifiers, EDF production vintages, random seeds, and precise default-event timestamp conventions are not supplied. As a result, the paper provides a well-defined research design but not a fully reproducible public-data package.

## Portfolio simulation and trading rules

At each formation month-end, draw 50 distinct issuers uniformly without replacement from the eligible universe and assign equal weights. Evaluate horizons of one, three, and five years. One-year portfolios form January 1983–December 2001; five-year portfolios end formation in December 1997 so outcomes remain inside the data ending in 2002. The experiment uses all calendar formation months.

There are 996 simulation trials: 83 random trials for each of the 12 formation-month positions. A trial contains a sequence of portfolios formed in that calendar month in successive years, up to 19 one-year observations. It is not 996 independent realizations of the economic environment. Random portfolio draws reuse the same history of ratings, EDFs, and defaults.

In the buy-and-hold experiment, loss of eligibility alone does not trigger a sale. Defaulted issuers and firms whose records terminate or are interrupted are replaced. Replacements are drawn randomly from currently eligible issuers not already held. Consequently even this buy-and-hold label allows reinvestment after defaults and database exits.

The trading experiments require replacement after an eligibility violation persists for zero, six, or 12 months. If the issuer becomes eligible again during the tolerance period, the clock resets; the next violation starts a fresh period. For a one-year horizon, requiring sale only after 12 months effectively reproduces no eligibility-driven secondary-market transactions.

An additional market-based rule introduces hysteresis: buy at EDF at most 0.50%, but sell only when EDF exceeds 0.75%, subject to the chosen tolerance period. The interval between the thresholds limits repeated trading near a single boundary. A position at 0.60% remains eligible to hold but is not eligible for a new purchase. A faithful implementation must keep separate purchase and retention conditions.

The central cost is a 1% round-trip charge on replacements induced by governance rules. The price experiment also uses 0.5%. No transaction cost is charged for replacement caused by data disappearance. Costs are percentages of traded bond value, not a 1% deduction from the whole portfolio on each trade. With a 2% portfolio position, a full 1% round trip is approximately two basis points of portfolio wealth before price/weight changes. The paper does not publish a complete cash-accounting algorithm for equal-weight restoration, reinvestment at default, or how within-horizon transactions are rounded; these details should be fixed explicitly in replication code.

## Default-loss experiment

Initially, a surviving bond is assigned price one and a defaulted bond price 0.5. Recovery is fixed at 50%, independent of issuer, cycle, and default cause. Losses come from defaults and charged turnover. All multi-year loss rates in Tables 2–7 are cumulative, not annualized.

Table 2 gives the following whole-sample mean losses and 99.9th-percentile losses:

| Purchase rule | One-year mean | Three-year mean | Five-year mean | One-year 99.9% loss | Five-year 99.9% loss |
|---|---:|---:|---:|---:|---:|
| Investment grade | 0.052% | 0.297% | 0.609% | 2% | 5% |
| EDF at most 0.50% | 0.025% | 0.296% | 0.680% | 1% | 6% |
| EDF at most 0.75% | 0.038% | 0.333% | 0.781% | 2% | 7% |
| EDF at most 2% | 0.128% | 0.840% | 1.732% | 2% | 9% |
| Rating better than B1 | 0.234% | 1.157% | 2.007% | 3% | 10% |

The last block of printed Table 2 is labeled “better than Ba1,” but its values and the surrounding design correspond to the distinct better-than-B1 universe; investment grade already appears in the first block. The table above resolves that labeling inconsistency using the paper's defined five universes.

At one year, tight EDF selection saves only 1.4–2.7 basis points of mean default loss against investment grade. At five years, the rating rule saves 7.1 basis points versus the 0.50% rule and 17.2 versus the 0.75% rule. Thus ranking systems can change order as the horizon changes. The 2% EDF rule consistently loses more than investment grade but less than the roughly equally populated better-than-B1 universe.

## Economic uncertainty versus simulation uncertainty

The paper explicitly separates Monte Carlo error from statistical uncertainty about the historical advantage. More random portfolios can drive simulation noise toward zero without generating another business cycle or default episode. Tests based on the 996 simulation averages primarily diagnose whether random draws have stabilized, not whether the rule advantage generalizes.

For historical inference, the author first averages simulated losses across portfolios formed in each calendar year. This creates 19 annual observations for the one-year horizon and 15 for the five-year horizon. Differences between strategies are then analyzed using Newey–West standard errors with lag length equal to the holding period in years. The extra lag relative to the usual horizon-minus-one convention accommodates overlap between portfolios formed at different months within adjacent years.

A complementary recursive bootstrap fits an AR(1) to the annual difference series. Each of 10,000 bootstrap samples begins with an observed starting value, then uses estimated AR coefficients and residuals sampled with replacement. The reported fraction of positive bootstrap mean differences is a sign-frequency diagnostic, not automatically a conventional two-sided p-value.

Table 3 defines the difference as investment-grade loss minus EDF-rule loss. For EDF at most 0.50%, the one-, three-, and five-year differences are 0.026%, 0.001%, and −0.071%, with t-statistics 1.47, 0.01, and −0.38. The first mean difference differs slightly from subtraction of rounded Table 2 cells. For EDF at most 0.75%, the differences are 0.014%, −0.036%, and −0.172%, with t-statistics 1.05, −0.38, and −0.89. None establishes conventional significance.

Against EDF at most 2%, differences are −0.076%, −0.543%, and −1.123%, with t-statistics −3.10, −5.24, and −4.75. Bootstrap sign frequencies are zero in all three cases. These stronger results support the narrower comparison with the broad EDF rule. They do not establish that ratings dominate appropriately tightened or filtered EDF rules. A Table 3 caption refers to 1981–2001, inconsistent with the repeatedly specified 1983 start; the stated experimental calendar should govern replication.

## Sale timing, hysteresis, and costs

Table 4 exposes why prediction accuracy is insufficient. With immediate sales and zero costs, investment grade has one-year mean loss 0.005%, versus 0.018% for EDF at most 0.50%. Only one defaulting issuer in the sample was still investment grade at the immediately preceding month-end. That timing fact is compatible with ratings being slow in continuous time: Enron's downgrade just before the November 2001 month-end is counted as sufficiently early for a December default.

With a six-month tolerance period and zero costs, EDF at most 0.50% improves the one-year loss to 0.023%, versus 0.041% for investment grade. But at 1% transaction costs, those figures become 0.069% and 0.050%. Under immediate sale, the corresponding net loss figures are 0.280% and 0.029%; noisy boundary crossings overwhelm the small default-loss difference.

For three years and a six-month grace period, investment-grade loss is 0.155% before costs and 0.206% afterward. The tight EDF rule is 0.085% before costs and 0.312% afterward. The hysteresis EDF rule produces 0.084% before costs and 0.211% afterward, nearly matching ratings after costs. This isolates the benefit of a transaction filter without requiring a new credit model.

Table 6 solves for the transaction cost at which mean losses match. For the tight EDF rule with six-month tolerance, break-even round-trip costs are 0.48%, 0.40%, and 0.36% at one, three, and five years. For the hysteresis rule under the same tolerances they are 3.34%, 0.93%, and 0.64%. Blank cells signify no trading or that matching would require negative costs, not an estimated zero-cost threshold.

Tail losses remain discrete because a default on one of 50 equally sized positions with 50% recovery initially costs one percentage point. At five years, immediate-sale 99.9% losses including 1% costs are 2.12% for investment grade and 3.94% for the tight EDF rule. With six-month tolerance, three-year values are 3.06% and 2.46%, respectively. These examples show that mean-loss and tail-loss rankings need not coincide.

## Hypothetical pricing: intended model and a printed formula defect

The price extension is limited to one-year investments because the available EDFs are one-year probabilities. The first route maps physical EDFs into risk-neutral default probabilities with a structural barrier model. Recovery remains half of face value, paid through the terminal-payoff pricing convention.

There is a mathematical problem in printed equation (1), journal p. 2735. As printed, both normal arguments contain a positive $\log(A/L)$, and the exponential has a positive distance coefficient. For assets initially above the barrier, this expression can exceed one and cannot be a lower-barrier hitting probability. This is visible in the rendered PDF, not merely an extraction error.

For a coherent reconstruction, let $x=\log(A_0/L)>0$ and specify the log-distance process $X_t=x+m t+\sigma W_t$. Its first-passage probability by $T$ is

$$
p(T;x,m,\sigma)=\Phi\left(\frac{-x-mT}{\sigma\sqrt T}\right)+\exp\left(-\frac{2mx}{\sigma^2}\right)\Phi\left(\frac{-x+mT}{\sigma\sqrt T}\right).
$$

This corrected expression tends to zero as initial distance grows, is one at the barrier, and reduces to $2\Phi[-x/(\sigma\sqrt T)]$ for zero drift. Solve $p(1;x,m_P,\sigma)=\mathrm{EDF}$ for $x$ with a bracketed root finder. Then evaluate the same distance with a risk-neutral log drift and remaining maturity to obtain $p_Q$.

The source sets expected logarithmic asset return to 10%, asset volatility to 10%, and continuously compounded risk-free interest to 5%, describing an asset Sharpe ratio of 0.5. It instructs replacing drift by the risk-free rate. A further convention must therefore be resolved: under a no-payout geometric Brownian asset-price model, risk-neutral log drift is $r-\sigma^2/2$, not $r$. If the drift denotes the arithmetic asset-return drift, the physical log drift also requires the half-variance adjustment. These conventions and the printed sign error prevent exact recreation of the author's pricing code from the displayed formula alone. The correction here defines a valid model; it does not establish which implementation generated the published tables.

With a consistently chosen risk-neutral probability and continuous rate, the intended terminal-recovery price is

$$
P(T)=e^{-rT}[1-0.5p_Q(T)].
$$

The source writes discounting as $(1+i)^{-T}$, so consistency with $r=.05$ requires $i=e^{.05}-1$. Its physical expected one-year simple return is $[1-0.5\mathrm{EDF}]/P(1)-1$.

The second price route uses Bohn (2000), Exhibit 7, for maturities below two years. It maps EDF to an empirical spread and sets price to $[e^{.05}+s_T(\mathrm{EDF})]^{-T}$. Asset–market correlation is set to 0.5 and the time-scaling parameter to 0.5. The fitted spread coefficients themselves are not reproduced in this source; they remain an external dependency. These empirical prices generally imply higher spreads for safer bonds than the structural mapping. They are still fitted prices, not the issuers' observed historical bond transactions.

## Return results and the risk denominator

For each simulation trial, the paper calculates mean simple return, a Sharpe ratio using the simple risk-free rate, and a modified ratio using the square root of lower semivariance around the mean return. The last is not a downside ratio relative to zero or a target return. Ratios are computed from up to 19 annual returns within each trial and then averaged; the average of these ratios is not the ratio of pooled mean excess return to pooled standard deviation.

In Table 8's structural-price experiment, immediate-sale investment-grade return is 5.65% before costs and 5.62% at 1% costs; its Sharpe ratio changes from 1.86 to 1.78. The tight EDF rule has 5.30% before-cost return and 5.04% net return; its Sharpe ratio changes from 1.97 to −0.40. The negative net Sharpe is consistent with the simple risk-free return being approximately 5.127%.

Allowing six months reverses the tight-EDF comparison: its net Sharpe is 1.78 against 1.55 for ratings. Yet matching volatility by mixing the rating portfolio with the risk-free asset gives mean return 5.28%, versus the EDF portfolio's 5.30%. A noticeable ratio difference here corresponds to only about two basis points of matched-risk annual return.

The empirical-spread mapping produces much larger ratios. For EDF at most 0.50%, six-month tolerance, and 1% costs, Table 9 reports Sharpe 6.07 versus 3.00 for investment grade. These are not realistic stand-alone performance expectations. Default rates in the sample are below the EDFs used for pricing: for December cohorts under the tight cutoff, realized annual default rate averages 0.065%, whereas average EDF is 0.19%. In addition, the experiment excludes general interest-rate and spread shocks.

Table 10 reports lower-tail returns despite its “loss quantiles” heading. Under structural prices and 1% costs, the 0.1st-percentile immediate-sale return is 4.59% for investment grade and 3.73% for the tight EDF rule. With six-month tolerance it is 4.35% versus 4.15%. Higher is better in this table. The source finds the rating rule's lower-tail returns exceed those of the EDF alternatives across these comparisons.

Appendix B relates default-indicator covariances to portfolio risk. An explicit weighted version is

$$
\operatorname{Var}(L)=\sum_{i,j}w_iw_j\ell_i\ell_j\bigl[P(D_i=1,D_j=1)-p_ip_j\bigr],
$$

where $\ell_i$ is fractional LGD and $w_i$ is exposure weight. For bond-return variance, the default payoff decrement is scaled by purchase price as well. The source's expression omits explicit weights, so its LGD quantities must absorb exposures to represent a portfolio amount; using fractional LGD alone would give the variance of a sum rather than the equal-weight average. Also, a bivariate normal terminal-threshold default probability is not generally the joint first-passage probability of two correlated barrier processes. Its illustrative expected-Sharpe calculation should not be treated as an exact analytic solution of a multivariate first-passage model without additional assumptions.

## What the experiment establishes

The stable-rating advantage is conditional on implementation. It grows when compulsory adjustment is fast, turnover is expensive, and the user cares about lower tails rather than a single average ratio. It shrinks when an EDF rule uses hysteresis or grace periods. The historical experiment is therefore an argument for evaluating the entire decision rule, not for ignoring market information.

Several ingredients limit external validity: selected matched public issuers, few low-risk defaults, overlapping formation cohorts, retrospective repairs, fixed recovery and costs, hypothetical rather than actual prices, missing watchlists and outlooks, and unresolved pricing-formula conventions. There is no optimized allocation, liquidity-capacity model, tax treatment, or forecast of current corporate-bond execution costs. Combining ratings and EDFs can be useful—the source reports lower buy-and-hold losses from an investment-grade-and-EDF-below-2% intersection—but does not supply a complete return/cost analysis of that combination.

For implementation, the essential deliverable is a replayable month-end state machine with separate admission, retention, tolerance, missingness, default, and cost rules. Statistical signal quality should then be judged on the chosen horizon and feasible universe, and economic value on the resulting cash flows. The paper makes this evaluation distinction compelling even though its price extension requires explicit repairs and additional inputs before it can be reimplemented exactly.

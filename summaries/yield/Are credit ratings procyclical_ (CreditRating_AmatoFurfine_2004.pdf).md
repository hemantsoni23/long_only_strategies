# Are credit ratings procyclical?

Jeffery D. Amato and Craig H. Furfine, *Journal of Banking & Finance* 28 (2004), 2641–2677. DOI: 10.1016/j.jbankfin.2004.06.005. Source: [CreditRating_AmatoFurfine_2004.pdf](../../Finance/CreditRating_AmatoFurfine_2004.pdf), 37 PDF pages including the likelihood appendix. Page references below use journal pagination.

## Why this matters and the precise question

Ratings often worsen in recessions, but this observation alone cannot show that an agency changes its standards excessively with the cycle. Firms' underlying business and financial risks also worsen. The paper asks whether macroeconomic conditions have an additional effect on assigned S&P ratings after accounting for observable firm risk. This conditional question is more useful than simply comparing upgrade and downgrade counts across expansions and contractions.

The principal finding is sensitive to what counts as an observation. With annual observations of the broad rated universe, the paper finds little evidence of additional procyclicality. With only investment-grade firms, or only initial assignments and actual rating changes, evidence is stronger. For the latter sample, a controlled change in the output growth gap changes the predicted rating for about 27% of observations in the richer specification. That result concerns the selected decision-event sample; it is not a forecast that 27% of all rated firms will migrate in a recession.

The second contribution concerns historical claims that rating standards became progressively stricter. A positive time trend appears when common changes in financial variables are omitted. Adding their yearly cross-sectional averages removes or reverses the trend. The interpretation of a time dummy as a change in agency standards therefore depends on the controls for changing underlying risk.

The paper's test cannot conclusively identify “excess” cyclicality. Unobserved fundamentals may enter through the macro variable, while sufficiently broad aggregate controls may absorb economically meaningful cyclicality. The authors explicitly acknowledge both limitations. Their results are about conditional associations and alternative measurement choices, not a causal estimate of a business-cycle intervention on rating committees.

## Ratings, sample construction, and outcomes

S&P CreditPro supplies continuous issuer-rating histories from January 1, 1981 to December 27, 2001. Issuer ratings describe a firm's ability and willingness to meet obligations. Issue ratings also reflect claim-specific recovery and seniority, so they are deliberately excluded from the object modeled here.

Notches are collapsed into letter categories: AAA, AA, A, BBB, BB, B, CCC, and CC, coded 1 through 8. Larger numerical values mean worse credit quality. C and D observations are removed because their assignment is driven largely by specified bankruptcy/default conditions rather than discretionary assessment. Grouping notches reduces sparsity and the overweighting of firms receiving a rapid succession of small adjustments.

The baseline panel has 10,144 matched observations before removing 142 D observations, leaving 10,002 for the prediction tables. Effective annual coverage begins in 1984 because the financial variables require history. The sample includes financial firms, though finance, insurance, and real estate account for only 6.8% of baseline observations. US publicly traded firms with CRSP and COMPUSTAT coverage dominate; the matched sample is not every firm in the raw rating database.

The rating distribution is concentrated in A through B: 2,839 A, 2,636 BBB, 1,971 BB, and 1,236 B observations. There are 225 AAA, 1,024 AA, 70 CCC, and just one CC observation. This extreme sparsity matters for estimated cutpoints and lower-tail classifications. Baseline observations rise from 258 in 1984 to around 900 in the late 1990s. The 2001 count falls to 141 because the data stop before December 31, the fiscal year-end of many companies; it is not evidence of a collapse in the rated universe.

For the baseline, each firm's actual fiscal year-end is the reference date for its rating, macro conditions, market value, and return-based risk estimates. Firms appear at most once per calendar year. The narrative refers to fiscal-year-end information, while table captions sometimes call the reference the balance-sheet release date. The source does not provide a detailed filing-date lag convention to reconcile these descriptions. A replication must state which timestamp it uses; this is an explanatory historical model, not a demonstrated real-time forecast using verified publication dates.

The event sample instead uses the exact date of an initial rating or a change in a letter rating. Market variables end at that event date; annual accounting variables use the most recently available balance-sheet information. A firm may appear several times in a year. This yields 2,353 observations before excluded rating outcomes, and 2,268 in the reported event-sample prediction comparison.

## Business-risk variables

The source combines three measures of business risk with financial ratios. Firm size is the logarithm of real market equity, with a robustness specification using real total assets. Nominal values are deflated with the monthly CPI. CRSP provides market equity and returns; COMPUSTAT supplies assets and accounting items. Exact currency-unit and CPI-base normalizations mainly affect locations, but must be consistent with any published coefficient and cutpoint replication.

Market-model beta and the residual standard error distinguish systematic from idiosyncratic equity risk. Estimate the market model from 200 daily total-return observations ending at the reference date, using the CRSP value-weighted market index. Data need not cover 200 consecutive trading days, but 200 observations must be available within the preceding year. Results are reportedly robust to substituting the S&P 500.

The paper applies Dimson's correction for nonsynchronous trading. A general implementation regresses a firm's return on current and selected lagged/leading market returns and aggregates the market coefficients. However, the source does not report the lead/lag order or every detail of the corrected residual-standard-error calculation. These are missing replication inputs; inventing an order and presenting it as the original method would be unjustified.

Beta and residual standard error are divided by the corresponding mean across firms in the observation year. All business and financial predictors are then demeaned by their within-year cross-sectional averages. The first normalization removes common scale shifts in market-risk estimates; demeaning expresses a firm's relative position. Neither should be replaced with a pooled z-score using a full-sample standard deviation.

Yearly normalization uses the observations dated throughout that calendar year, so an early-year observation can depend on later-year peers. The authors note this timing issue and report similar qualitative results with quarterly standardization or no standardization. The historical normalization is not automatically available in a real-time application.

## Financial ratios and the nonlinear coverage function

Four underlying ratios proxy debt-service capacity, profitability, and leverage. They are averaged over three years, following the agency's emphasis on performance over a cycle. Market size, beta, and residual volatility are not three-year averaged.

Interest coverage is operating income after depreciation plus interest expense, divided by interest expense. Negative coverage observations are removed, because the ratio can give misleading marginal interpretations when earnings are negative. This exclusion can remove financially distressed firms and is therefore part of the sample definition, not a harmless numerical adjustment.

Let $C$ be the three-year average coverage ratio, capped at 100. Represent it by four bounded increments:

$$
C_1=\min(C,5),\quad C_2=\min(\max(C-5,0),5),
$$

$$
C_3=\min(\max(C-10,0),10),\quad C_4=\max(C-20,0).
$$

On the permitted interval $0\leq C\leq100$, these variables sum to $C$. Their coefficients are the marginal effects within successive coverage ranges, not four independent measures of total coverage. Increasing coverage from 4 to 6 changes $C_1$ by one and $C_2$ by one; increasing it from 25 to 26 changes only $C_4$.

Operating margin is operating income before depreciation divided by net sales. Long-term debt/assets and total debt/assets capture capital structure. Total debt includes debt in current liabilities plus long-term debt; average short-term borrowings are omitted because they are unavailable for most firms. The two debt ratios are strongly correlated.

The implementation order is to construct financial ratios, obtain three-year averages, transform averaged coverage into its four components, and then apply the described cross-sectional demeaning. The paper does not fully specify missing-year handling, averaging weights when accounting periods differ, or all COMPUSTAT filters. These choices can change the matched panel and must be documented rather than guessed.

## Three cycle measures and trend units

The NBER recession indicator equals −1 during a recession and zero otherwise. The source treats every day in a peak month and subsequent months before the trough month as recession dates. With this sign convention, a negative coefficient means recession raises the latent bad-credit index and worsens ratings. Reversing the sign to the more usual positive recession dummy without changing the coefficient would invert the conclusion.

The output growth gap is year-over-year real GDP growth minus year-over-year potential GDP growth, with potential growth from the Congressional Budget Office. It is a growth-rate gap, not the level gap between actual and potential GDP. Quarterly observations are assigned to all dates in the quarter. A value 0.015 means actual annual growth exceeds potential annual growth by 1.5 percentage points.

The discrete growth indicator is −1, zero, or +1 according to whether a quarter's year-over-year real GDP growth lies in the bottom, middle, or top third of the full-sample quarterly distribution. Its cutoffs therefore use the entire historical sample. It classifies expansions as well as contractions, unlike the recession dummy. GDP revisions, CBO data vintages, and exact tercile cutoffs are not supplied.

A linear time trend replaces unrestricted year effects when trend and cycle are estimated jointly. Table 4 coefficients near 0.019 per trend unit are described in the text as about 0.076 per year, implying quarter-scale increments. A replication should use four trend units per year to reproduce that numerical interpretation. Treating the printed coefficient as annual would understate the reported drift fourfold. The source reports similar qualitative cycle results with a quadratic trend.

## Ordered probit and the two conditional tests

Let $R_{it}\in\{1,\ldots,8\}$ be the observed category and define a latent bad-credit index

$$
Z_{it}=\eta_{it}+\epsilon_{it},\qquad \epsilon_{it}\sim N(0,1).
$$

With ordered cutpoints $\mu_0=-\infty<\mu_1<\cdots<\mu_7<\mu_8=\infty$, category $r$ occurs when $\mu_{r-1}\leq Z_{it}<\mu_r$. Thus

$$
p_{it,r}=\Phi(\mu_r-\eta_{it})-\Phi(\mu_{r-1}-\eta_{it}).
$$

Maximize $\sum_{it}\log p_{it,R_{it}}$ for the baseline panel. Unit normal variance fixes scale; omitting an intercept fixes location. With time dummies, one dummy is omitted. The source's tables appear to use a reference-year convention different from the prose description, but shifts in all cutpoints and time effects leave probabilities unchanged if treated consistently.

For the weak test, Baseline 1, let $x_{it}$ be demeaned firm-risk predictors, $c_t$ the chosen cycle measure, and $q_t$ the trend:

$$
\eta_{it}=\beta'x_{it}+\delta q_t+\theta c_t.
$$

The hypothesis of no additional cycle effect is $\theta=0$. The strong test, Baseline 2, additionally includes the yearly cross-sectional means of the business and financial predictors:

$$
\eta_{it}=\beta'x_{it}+\lambda'\bar x_t+\delta q_t+\theta c_t.
$$

Here $\bar x_t$ denotes the mean of the variables before demeaning, not the mean of already demeaned values, which would be zero. With a common sample this separates within-year firm variation from between-year aggregate variation. The text sometimes calls these financial averages, but Table 5 includes size and the market-model variables as well as the ratios.

An ordered-probit slope moves the latent index; it is not a constant number of rating notches. The category-probability derivative is

$$
\frac{\partial p_r}{\partial c}=\theta\left[\phi(\mu_{r-1}-\eta)-\phi(\mu_r-\eta)\right].
$$

Consequently the same index shift affects firms differently depending on their location relative to cutpoints. The source reports standard errors but does not establish firm-clustered, time-clustered, or common-shock-robust inference. Thousands of firms do not create thousands of independent business cycles; common time-series regressors are identified from a short macro history containing only two recessions in the effective 1984–2001 sample.

## A complete baseline coefficient example

For the output-gap version of Baseline 1, Table 4 gives the following coefficients on demeaned predictors:

| Predictor | Coefficient | Standard error |
|---|---:|---:|
| Coverage component 1 | −0.2926 | 0.0145 |
| Coverage component 2 | −0.0327 | 0.0097 |
| Coverage component 3 | −0.0451 | 0.0070 |
| Coverage component 4 | +0.0120 | 0.0017 |
| Operating margin | −1.2921 | 0.0943 |
| Long-term debt/assets | +3.2944 | 0.1559 |
| Total debt/assets | −1.4859 | 0.1593 |
| Log real market equity | −0.4237 | 0.0094 |
| Standardized beta | +0.3556 | 0.0189 |
| Standardized residual standard error | +1.1957 | 0.0372 |
| Trend | +0.0190 | 0.0006 |
| Output growth gap | −1.7879 | 0.8888 |

The large benefit of coverage below five and small effects beyond five fit diminishing informativeness. The positive coefficient above coverage 20 is statistically significant but economically small per coverage unit. The negative total-debt coefficient conditional on long-term debt is not evidence that more leverage improves credit quality. Shared variation between the debt measures changes the conditional interpretation; the robustness analysis dropping total debt leaves a positive long-term-debt coefficient near 2.1.

The paper does not publish the fitted cutpoints. Therefore these slopes cannot alone recreate numerical category probabilities or the confusion matrices. A reimplementation must refit them from the underlying data. This is an important boundary between reconstructing the model and reproducing the precise table outputs.

## Broad-panel results

Table 4's weak-test cycle coefficients are −0.0053 with standard error 0.0495 for the NBER indicator, −1.7879 with 0.8888 for the output growth gap, and −0.0163 with 0.0130 for the discrete indicator. Only the gap is significant at 5%. In latent-index units, changing the gap from +0.015 to −0.015 raises the fitted bad-credit index by about 0.0536 under this specification; that is a derived index shift, not a 0.0536-notch downgrade.

The richer test changes the result. Table 5 reports cycle coefficients +0.1727 (0.0805), +0.4216 (1.2000), and −0.0074 (0.0165). The NBER result is significant but countercyclical with the paper's coding; the other two are insignificant. Trend coefficients become −0.0034, −0.0072, and −0.0074, all insignificant. Thus the earlier positive trend and weak gap effect are not robust to the aggregate-risk controls.

The strong specification can also overcontrol. Yearly average ratios mix permanent secular changes and temporary cyclical changes, and the paper does not decompose them. If the empirical objective is to estimate total cyclical rating sensitivity, removing their effects is inappropriate; if it is to estimate cycle sensitivity unexplained by observed fundamentals, the controls are relevant. Those are distinct estimands.

Other checks add current ratios to the three-year averages, replace equity size with assets, or drop total debt. Most maintain the broad-panel conclusion. There is a minor source inconsistency: the discussion says the discrete-growth term becomes significant when current ratios are added, while printed Table 6 gives −0.0148 with standard error 0.0130, which is not significant at 5% under a conventional normal approximation. The note relies on the printed coefficient/standard-error pair rather than repeating that sentence as established evidence.

In-sample fit changes little. Table 7's diagonal counts imply approximately 53.00% exact-category matches for the time-dummy model, 53.15% for Baseline 1, and 52.92% for Baseline 2. These percentages are calculated from the published cells, not new out-of-sample results. Extreme categories are poorly represented: of 225 actual AAA observations, the time-dummy model predicts AAA only 45 times, AA 147 times, and A 33 times. Similar overall fit does not imply equivalent economic interpretation of trend and cycle parameters.

## Investment-grade restriction

The investment-grade-only model keeps AAA through BBB, 6,724 observations. Its weak-test cycle coefficients become −0.1206 (0.0634) for recession, −3.8543 (1.1598) for the output gap, and −0.0487 (0.0175) for discrete growth. The latter two are significant at 1%. Strong-test estimates are +0.0780 (0.1082), −2.3509 (1.5609), and −0.0445 (0.0220), leaving the discrete-growth result significant at 5%.

The scenario exercise holds all firm variables fixed and changes the gap from +1.5 to −1.5 percentage points. Under the weak model, 127 of 676 observations predicted AA in the upturn become A in the downturn, about 18.8%. Under the strong model, 64 of 657 move, about 9.7%. For predicted A observations, the corresponding moves to BBB are 273 of 3,613 and 154 of 3,584.

These are paired conditional predictions for the same observations, not observed recession transitions. Moreover, this restricted model cannot estimate BBB-to-BB downgrades: its lowest identified outcome is BBB and the speculative-grade cutpoint is missing. The apparent absence of that transition in its scenario table is a limitation of the support, not evidence that the investment-grade boundary is safe.

Selection on being investment grade can itself bias slope estimates. A firm whose realized rating is better than expected may enter the sample, while a counterpart with a worse-than-expected speculative rating is excluded. The source recognizes this concern. Different estimates can reflect heterogeneous rating behavior, outcome-based selection, or both.

## Event-sample likelihood: why ordinary probit is insufficient

For initial assignments, use the ordinary category probability $p_j(X)$. For observed changes, the new rating cannot equal the old rating. Appendix A modifies the likelihood to account for this selected support instead of treating changed ratings as an unselected random sample.

The source integrates over previous categories rather than simply conditioning on the recorded prior category. Define a second ordered-probit mapping with slopes $\tilde\beta$ and the same printed cutpoints,

$$
q_k(X)=\Phi(\mu_k-\tilde\beta'X)-\Phi(\mu_{k-1}-\tilde\beta'X).
$$

Its change-observation contribution for current category $j$ is

$$
g_j(X)=\sum_{k\ne j}q_k(X)\frac{p_j(X)}{1-p_k(X)}.
$$

The mixed log likelihood sums $\log p_j$ for initial ratings and $\log g_j$ for changes. The denominator renormalizes the current-rating distribution after excluding category $k$. Provided the probabilities span all eight categories, $\sum_jg_j=\sum_kq_k=1$. Numerically, evaluate normal-CDF differences and the complement $1-p_k$ stably, since extremely concentrated category probabilities can cause cancellation.

There are two qualifications. First, the derivation assumes the previous rating is independent of whether a current change occurs, conditional on covariates, and it removes prior-rating information from the current-category mapping beyond excluding a self-transition. The source motivates the former by limited rating-trigger effects, but rating persistence and differential monitoring can still challenge it. This mixture is a particular selection model, not a general correction for every form of event sampling.

Second, equation (A.3)'s printed statement $\mu_0\equiv0$ is inconsistent with the standard normal latent support. The lower endpoint must be $-\infty$, as implied by the baseline category definition; otherwise the category probabilities omit the lower tail and fail to sum to one. This is a source-confirmed typesetting/formula defect. The normalized version above uses the corrected endpoint. The paper does not report the ancillary $\tilde\beta$ estimates or the cutpoints, preventing exact reproduction of its event-sample fitted probabilities from tables alone.

A different valid design could condition directly on the observed old category and model $P(R_t=j\mid X,R_{t-1}=k,R_t\ne k)$, but that is not the same likelihood the authors estimated. One should not silently substitute it when claiming to reproduce their results.

## Event-sample findings and scope

Table 10 gives much stronger weak-test cycle coefficients: −0.5896 (0.0783), −14.7066 (1.6913), and −0.1386 (0.0307) for recession, output gap, and discrete growth. All are significant at 1%. With yearly means included, coefficients are −0.1414 (0.1164), −14.2007 (3.5485), and −0.1020 (0.0464). The gap remains significant at 1%, discrete growth at 5%, and recession is insignificant.

The event-sample trend is positive in weak specifications, around 0.0068–0.0084 per trend unit, but negative in the strong specifications, around −0.0086 to −0.0093. These negative terms suggest conditional easing of standards under the richer model rather than the broad claim of steadily increasing toughness.

For the strong output-gap specification, the +0.015 to −0.015 scenario shifts the latent index upward by about 0.4260, computed as $(-14.2007)(-0.03)$. The full probability/classification consequences additionally depend on the selection likelihood and fitted ancillary parameters. In Table 11, 16 of 20 predicted AA observations move to A, 213 of 489 A observations move to BBB, and 235 of 855 predicted BBB observations move to BB. Altogether 615 of 2,268 observations change predicted category, approximately 27.1%; all changes in the table are by one major category.

This is consequential near investment mandates that distinguish BBB from BB, but the selected sample represents occasions when the agency actively assigned or changed a rating. It excludes the many firms with unchanged ratings. The large conditional percentages cannot be multiplied across the whole universe without separately modeling the chance of a rating action. Nor does the paper estimate an actual spread response or capital-flow effect; those are plausible implications, not measured outcomes.

## Replication boundaries and research takeaway

A faithful reconstruction needs issuer-rating histories with event dates, a verified CRSP/COMPUSTAT linkage, the fiscal-year or release-date convention, three-year ratio histories, the 200-return estimation windows, a specified Dimson correction, CPI and GDP/potential-growth vintages, cross-sectional normalization populations, and the two ordered-probit likelihoods. The source makes the main construction transparent but leaves cutpoints, ancillary event-model slopes, some data filters, exact timing, and dependence-robust uncertainty unspecified.

Its most reusable lesson is to define the conditioning question before interpreting a cycle coefficient. Annual rating stocks, selected investment-grade observations, and active rating decisions answer different questions. A stable broad-panel rating distribution can coexist with strongly cycle-sensitive decisions when an agency acts. Similarly, an apparent secular tightening can disappear when common changes in measured risk are explicitly included. These findings warrant richer state and selection models rather than a blanket claim that ratings either do or do not react to the business cycle.

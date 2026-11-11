# Customer revolving credit – how the economic conditions make a difference

Natasa Sarlija, Mirta Bensic, and Zoran Bohacek. Research manuscript associated with the supplied 2005 filename. The document identifies the authors and affiliations but supplies no journal, DOI, or explicit publication date. Its empirical observations are from 2004.

Source: [original PDF](../../Finance/RevolvingCredit_SarlijaBensicBohacec2005.pdf). All 16 pages, including references, were read. The logistic and survival equations, data definitions, descriptive statistics, and coefficient tables were checked against the page images. Page references below are PDF page numbers, which match the manuscript’s printed numbering.

## Why this matters

Behavioral credit scoring uses an existing account’s payment and borrowing history to forecast future trouble. It can remain useful where a lender lacks a credit bureau, but the available predictors and their economic meanings can differ from those in a mature multi-lender information system. This paper examines that problem using Croatian current accounts with revolving overdraft facilities.

The authors fit a six-month logistic default model and a Cox time-to-default model to a single bank’s data. Both select employment status, second-job status, account age, client age, overdraft limits, and recent delinquency indicators. The logistic model also selects payment and usage variables. The study contributes a detailed local variable inventory and fitted coefficients. It does not develop a new estimator or identify a causal effect of Croatia’s macroeconomic environment.

Two implementation checks materially affect the interpretation. First, the paper’s total classification accuracy does not reconcile with its reported class-specific recall rates and validation class counts. Second, the monetary overdraft-excess variable has negative observed values. Its negative coefficient can therefore mean that a larger *absolute* excess predicts more risk, despite the authors’ verbal claim that larger excess is protective. Both issues should be resolved before using the fitted score operationally.

## Observation window, target, and sample

Data cover calendar 2004, with June 30 as the scoring date. The first six months form the feature window. The following six months form the outcome window. An account is “bad” if the customer exceeds the contracted overdraft for more than 35 days during that second half-year; otherwise it is “good.” This is the paper’s operational delinquency definition, not a legal-bankruptcy or charge-off definition.

The text does not say whether the 35 days must be consecutive or cumulative, how breaches spanning the observation date are handled, or whether default time in the Cox model is the first breach, the thirty-sixth breach day, or another event date. Those choices can alter both labels and survival durations. They should be recovered from the bank’s original event logic rather than guessed.

The initial randomly collected sample contains 50,000 accounts and falls to 44,089 after cleaning, an exclusion of 5,911 accounts, or 11.822%. Cleaning criteria are not disclosed. The development sample has 34,879 accounts: 1,134 bad and 33,745 good, a bad rate of 3.25%. The validation sample has 9,210 accounts: 278 bad and 8,932 good, a bad rate of 3.02%. The authors say the sample composition matches the bank’s full data set.

For survival analysis, account closure and surviving beyond the observation period produce right censoring. Closure may depend on credit quality, collection activity, or customer behavior. Cox interpretation therefore requires an appropriate noninformative-censoring assumption, conditional on modeled covariates, which is not tested here. Closure is not simply another default, and it is not the same as prepayment on a fixed-maturity loan.

The split is described as development and validation, with no separate later period. Both sets concern the same 2004 environment. There is no out-of-time validation, multi-bank comparison, or foreign-country control group. Customer identifiers, any multiple-account links, random seed, and split stratification are absent. An account-level split would also need scrutiny if one customer could contribute several accounts.

All information comes from the bank. The manuscript’s statements about the absence of a Croatian credit bureau concern this historical study setting. They are not claims about present-day institutions. The motivation cites GDP per capita of \$7,732, unemployment of 18%, and average net wages of 4,137 kuna, described as about EUR 600. These provide context, not covariates varying across observations in a fitted macroeconomic model.

## Variables and units

The authors start from 34 variables divided into demographics, socioeconomic characteristics, and behavior. Demographics are gender and age. Socioeconomic variables include working status, town/village residence, a second job, possession of credit cards, account age, and savings-account status. Working status distinguishes retired, employed, unemployed, and no answer; nearly half the good sample and more than half the bad sample give no answer. That missing-status category is a large part of the data, not a negligible nuisance.

Behavioral measures summarize the first six months. They include the contracted limit LIM; cash deposits CASH; transfers from other accounts PON; irregular receipts PNR; salary receipts SLR; interest paid to the client INT+; standing-order withdrawals STOR; cheque withdrawals CHE; card withdrawals CRE; cash withdrawals FCAS; and interest paid by the client INT−. Aggregate flows are TIN, total inflows, and TOUT, total outflows. Ratios compare flows with the limit or with each other. Balance measures include BAL, limit plus balance LBAL, and contracted limit divided by balance BALD.

Delinquency variables include USE, a three-category measure of whether the limit was unused, used, or exceeded; NEG, breach frequency; KN, the monetary excess; DAYS, breach days; CONT, continuous months with excess overdraft; and LAST, days since the most recent breach. The paper describes behavioral inputs as six-month averages, but the precise aggregation of counts, elapsed days, categorical usage, and money is not fully specified. A monthly average, daily average, end-month measure, and six-month total are not interchangeable units for the published coefficients.

Table 1 gives monetary quantities in Croatian kuna and supplies the approximate contemporary conversion EUR 1 ≈ 7.4 kuna. Coefficients on unscaled monetary variables must therefore be interpreted per kuna, not per euro or per thousand kuna. Age and account age appear to be in years from their values and descriptions, but a codebook should confirm account-age units. CONT is a month count; the descriptive table accidentally labels its mean and standard deviation in kuna.

Some illustrative good/bad development-sample averages are:

| Variable | Good | Bad | Units |
|---|---:|---:|---|
| Client age | 51.13 | 41.87 | Years |
| Account age | 9.98 | 7.69 | Apparent years |
| Contracted overdraft | 2,564.25 | 1,513.66 | Kuna |
| Salary receipts | 2,414.05 | 1,417.75 | Kuna, reported average |
| Total inflows | 3,187.49 | 2,240.29 | Kuna |
| Total outflows | 3,161.82 | 2,399.85 | Kuna |
| Net inflow | 25.66 | −159.57 | Kuna |
| Balance | 1,021.47 | −1,105.26 | Kuna |
| Overdraft excess KN | −26.49 | −371.93 | Kuna, signed |
| Breach days DAYS | 0.75 | 9.25 | Days |
| Continuous breach months CONT | 0.27 | 1.78 | Months |
| Days since breach LAST | 153.89 | 51.53 | Days |

The bad group is younger, has lower salary and limits, and has more recent and persistent overdraft breaches. These unconditional patterns motivate predictors but do not establish their conditional coefficients or causal effects. The second-job share, for example, is slightly higher among bads, 36.07% versus 33.19%, even though the fitted conditional coefficient is protective. Correlations with income, work status, and other behavior can explain why a marginal comparison and a conditional regression need not agree.

Several ratios are extremely dispersed. BALD has mean 15.56 and standard deviation 858.85 among goods; the inflow/outflow ratio RAT has mean 12.84 and standard deviation 86.07. Ratios with near-zero or sign-changing denominators can produce extreme values. Treatment of zero limits, zero withdrawals, negative balances, outliers, and missing entries is not reported, even though cleaning removes almost 12% of initial accounts.

The CITY percentages contain an explicit arithmetic inconsistency: goods in towns are 65.78% and goods in villages 42.22%, totaling 108%. Bad proportions total 100%. No correction is inferred here. The final models omit CITY, but the inconsistency limits reconstruction of the original descriptive data.

## Logistic model and estimable quantities

Let $Y_i=1$ if account $i$ breaches the six-month bad definition. With features available by June 30, logistic regression assumes

$$
p_i=P(Y_i=1\mid x_i)=\frac{\exp(\beta_0+x_i^\top\beta)}{1+\exp(\beta_0+x_i^\top\beta)}.
$$

Estimation maximizes

$$
\ell(\beta_0,\beta)=\sum_i\left[Y_i\log p_i+(1-Y_i)\log(1-p_i)\right].
$$

The authors use forward selection in SAS, reducing 34 candidates to 18 original variables. Working-status dummies make the number of coefficient rows larger than 18. Entry/removal criteria, interactions, transformations, collinearity controls, and any prior-probability or class-weight adjustments are not supplied.

Table 2 reports the following slopes:

| Variable or indicator | Coefficient | Reported $p$ |
|---|---:|---:|
| Working status: retired | −0.6806 | <.0001 |
| Working status: employed | −0.3056 | .0162 |
| Working status: no answer | −0.3043 | .0106 |
| Second job: yes | −0.1445 | .0398 |
| LIM | −0.00111 | <.0001 |
| PON | −0.00055 | .0212 |
| SLR | −0.00022 | <.0001 |
| INT+ | −0.3530 | <.0001 |
| CHE | 0.000729 | <.0001 |
| FCAS | −0.00005 | <.0001 |
| INT− | 0.0203 | <.0001 |
| INOUT | −0.00038 | <.0001 |
| BAL | −0.00081 | <.0001 |
| RAT | −0.00477 | .0019 |
| KN | −0.00019 | .0284 |
| DAYS | 0.0804 | <.0001 |
| CONT | 0.1250 | .0003 |
| LAST | −0.00818 | <.0001 |
| ACAGE | −0.0410 | <.0001 |
| AGE | −0.0113 | <.0001 |

Unemployed appears to be the omitted working-status category in this table; the full contrast coding is not stated. The intercept is not published. Consequently, even with all slope variables observed, the reader cannot calculate a numerical six-month PD or reproduce the reported cutoff from this table alone. Slopes permit relative odds comparisons under the specified coding, not an absolute scorecard.

For a continuous variable change $\Delta x_j$, the conditional odds multiplier is $\exp(\beta_j\Delta x_j)$. Derived examples help make the units visible: ten additional breach days multiply odds by $e^{.804}=2.234$; 30 additional days since the latest breach multiply odds by $e^{-.2454}=.782$; an additional 1,000 kuna of salary receipts multiplies odds by $e^{-.22}=.803$. A 1,000-kuna higher limit gives $e^{-1.11}=.330$, a large association whose magnitude particularly warrants checking coding, scaling, and bank selection policies.

These are conditional associations, not intervention effects. Banks may grant higher limits to safer borrowers; increasing an already risky account’s limit need not make it safer. The model also includes correlated flows and balances, so changing one coordinate while holding all others fixed can describe an economically uncommon counterfactual.

## Cox model and the missing baseline

Let $T_i$ be time from the observation date to the defined default event. The Cox model assumes

$$
h_i(t)=h_0(t)\exp(x_i^\top\gamma).
$$

Here $h_i(t)$ is an instantaneous event rate conditional on surviving to $t$, not a finite-interval default probability. For a short interval $dt$, the event probability is approximately $h_i(t)dt$. The proportional-hazards restriction makes the hazard ratio for two fixed covariate vectors independent of time.

With distinct event times, a conventional partial likelihood is

$$
L(\gamma)=\prod_{i:\delta_i=1}
\frac{\exp(x_i^\top\gamma)}{\sum_{j\in R(T_i)}\exp(x_j^\top\gamma)},
$$

where $\delta_i$ marks an observed default and $R(T_i)$ is the risk set immediately before it. This makes the estimation mechanism self-contained; the source names Cox estimation but does not give tie handling, precise duration units, risk-set construction, or proportional-hazards diagnostics. Daily or monthly event recording could create many ties, so the implementation choice matters.

Forward selection retains ten original variables, including two reported working-status terms. Table 3 gives:

| Variable or indicator | Coefficient | Printed hazard ratio | $p$ |
|---|---:|---:|---:|
| Female | 0.15769 | 1.171 | .0097 |
| Retired | −0.40249 | .669 | <.0001 |
| Unemployed | 0.53939 | 1.715 | <.0001 |
| No second job | 0.12424 | 1.132 | .0525 |
| LIM | −0.0000630 | 1.000 | .0001 |
| KN | −0.0003090 | 1.000 | <.0001 |
| DAYS | 0.05852 | 1.060 | <.0001 |
| CONT | 0.12961 | 1.138 | <.0001 |
| LAST | −0.01152 | .989 | <.0001 |
| ACAGE | −0.05925 | .942 | <.0001 |
| AGE | −0.00604 | .994 | .0320 |

The second-job term’s $p=.0525$ is above .05, despite its inclusion in the selected model and qualitative discussion. It should not be described as significant at 5%. The omitted working-status contrast is not fully explained, particularly the treatment of the large no-answer group.

Hazard ratios rounded to 1.000 for monetary variables do not mean no effect. Per 1,000 kuna, LIM implies $e^{-.063}=.939$. For ten additional breach days, the multiplier is $e^{.5852}=1.795$; for 30 additional days since a breach, it is $e^{-.3456}=.708$. These are derived rescalings of reported coefficients. Comparing their magnitudes directly with logistic odds ratios would conflate an instantaneous hazard with six-month odds.

To calculate an absolute six-month Cox default probability one also needs the baseline cumulative hazard $H_0(t)$:

$$
P(T\leq t\mid x)=1-\exp[-H_0(t)\exp(x^\top\gamma)].
$$

The authors explicitly say their focus is variable importance rather than the baseline-hazard shape, and they do not publish $H_0$. Thus the paper does not provide a fully deployable survival PD model either. Its promise of predicting default likelihood does not supply the numerical baseline required to do so from the note’s table.

## Signed overdraft excess changes the interpretation

KN is described as the amount by which an account exceeded its limit, but Table 1 reports negative averages: −26.49 kuna for goods and −371.93 for bads. Both fitted KN coefficients are negative. If excess magnitude $E\geq0$ is encoded as $KN=-E$, substitution yields

$$
\beta_{KN}KN=(-\beta_{KN})E.
$$

The coefficient on the positive magnitude is therefore positive. A further 1,000 kuna of excess, represented by a change $\Delta KN=-1000$, multiplies logistic odds by $e^{.19}=1.209$ and the Cox hazard by $e^{.309}=1.362$.

The authors instead describe greater excess as lowering risk and suggest that bank warnings may induce customers to improve. That behavioral story is not needed under the signed coding shown in their own descriptive table. The appropriate conclusion is conditional: if the regressions use the same signed KN definition, larger excess magnitude is associated with higher risk. The codebook and raw construction are needed to confirm that identity. The note does not silently alter the published coefficients or claim to know the original code.

This matters because a sign interpretation can reverse an account-management recommendation. A more negative balance-related variable is not a larger economic quantity simply because its label says “amount.” The separate protective association of a higher contractual limit should also not be confused with this signed excess variable.

## Classification performance and a numerical inconsistency

For the logistic model, the source reports a validation total hit rate of 81.16%, good recall of 82.4%, and bad recall of 74.46%. It also reports the complementary error rates, 17.6% of goods classified bad and 25.54% of bads classified good. Given 8,932 goods and 278 bads, the class-weighted accuracy implied by those recalls is

$$
\frac{8932(0.824)+278(0.7446)}{9210}=0.8216033,
$$

or approximately 82.16%, not 81.16%. Rounding the recalls cannot explain a one-percentage-point discrepancy. One of the values or its associated evaluation population must differ, but the source does not identify which. The note retains the reported total separately from the derived reconciliation and does not invent a corrected confusion matrix.

An always-good classifier would score $8932/9210=96.98\%$ on the stated validation set, above either total accuracy. That does not make the fitted classifier useless: identifying bad accounts can be economically valuable even at the price of rejecting many goods. It does mean that total accuracy alone is a misleading objective in this low-default sample.

Using the reported recalls and counts as approximate inputs, the model flags about 207 bads and 1,572 goods. Bad precision among flagged accounts is only about 11.64%. The roughly 1,572 false alarms prevent about 207 missed bads relative to always-good classification. With constant false-positive cost $C_G$ and false-negative cost $C_B$, that operating point has lower classification loss than always-good only if approximately

$$
\frac{C_B}{C_G}>\frac{8932(0.176)}{278(0.7446)}\approx7.59.
$$

This is a derived decision threshold, not a result or cost assumption of the paper. Real losses depend on exposure, recovery, customer margin, and the action taken after a flag. The paper supplies none of those components, nor the probability cutoff used to obtain its reported recalls.

The reported global score and Wald statistics are 8309.4855 and 2919.9757 for logit, and 8777.4851 and 3407.2117 for Cox, all with $p<.0001$. These test model association under the fitting assumptions. They do not compare out-of-sample discrimination, show calibrated probabilities, or validate the stepwise selection process. No Cox holdout hit rate, AUC, concordance index, integrated Brier score, or direct predictive comparison with logit is provided.

## Economic interpretation and replication boundary

The common selected predictors emphasize persistent and recent payment difficulty: DAYS, CONT, LAST, and KN, alongside employment and account tenure. Logistic regression adds salary, balance, flows, cheque use, and interest variables. CITY, cash deposits, and irregular receipts are not selected, despite being motivated by the authors’ expectations about rural poverty and supplementary income.

This is evidence about variable selection within one bank and one year. It does not identify the effect of national unemployment, war, transition, or institutional change. There are no cross-country controls, macro time series, counterfactual policy changes, or interaction tests. Permanent-job and second-job associations are consistent with the stated economic interpretation, but they may also appear in other countries and economic environments. Failure of imported models is asserted as motivation without a quantified comparator experiment in this paper.

The abstract mentions profitability, but the empirical models concern default and time to default. There is no profit function, interest-margin calculation, lifetime account valuation, or estimated optimal limit. Survival analysis can support such applications only after adding cash-flow and competing-event assumptions. Those extensions are not demonstrated here.

A reproduction requires the cleaning rules; the exact 35-day definition and event time; aggregation, sign, and denominator conventions; complete category contrasts; selection settings; logistic intercept; Cox baseline and tie handling; censoring details; and the classifier cutoff. A stronger test would preserve the June 30 information boundary, keep linked accounts together, and evaluate a subsequent year before attributing stability to the score. Within those limits, the study is a useful account of how bank transaction data can substitute for missing external information and how implementation details can dominate seemingly straightforward coefficient interpretations.

The source places its methods in the credit-scoring work of Hand–Henley, Banasik–Crook–Thomas, Stepanova–Thomas, and related survival-analysis studies. Their external results are background cited by the authors, not additional experiments reproduced in this note.

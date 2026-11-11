# Internal ratings systems, implied credit risk and the consistency of banks’ risk classification policies

Tor Jacobson, Jesper Lindé, and Kasper Roszbach. *Journal of Banking & Finance* 30 (2006), 1899–1926. DOI 10.1016/j.jbankfin.2005.07.011. [Source PDF](<../../Finance/Internal Rating Systems_Jacobson2006.pdf>). All 28 pages were read, including the sampling protocol, twelve tables, three figures, footnotes, discussion, and references. Printed page 1899 is PDF page 1. The paper evaluates historical Swedish bank data and the Basel II framework discussed in 2004; regulatory descriptions below are historical, not current capital guidance.

## Why this matters

A rating grade is a compression of information, not a portable unit of risk. Two banks may call the same borrower safe, disagree about the borrower, or concentrate very different borrowers in similarly named grades. Once grades are used to estimate portfolio losses and allocate capital, these differences become economically material. Jacobson, Lindé, and Roszbach show this with borrower-level records from two major Swedish banks, including firms that borrow simultaneously from both.

The paper's contribution is to connect rating-system design and implementation with estimated loss distributions. Its matched-borrower subset helps define comparable portfolio profiles despite one bank using fifteen grades and the other seven. A resampling experiment then shows how those profiles imply different expected and tail losses under the banks' own historical experience. Portfolio size, the mix of grades, and observed aggregate conditions also affect the difference.

This is especially useful for model governance: matching a distribution over rating buckets does not establish matching economic risk. It is less informative about absolute crisis capital. The observations cover roughly three predominantly favorable years, loss given default is assumed to be 100%, and large Monte Carlo samples do not create additional business-cycle histories. Several headline statements in the prose also disagree with the printed tables; the distinctions below preserve what can actually be reconstructed.

## Data and what constitutes a default

Bank A supplies 338,118 observations on 39,521 Swedish limited-liability companies over 1997Q1–2000Q1. Bank B supplies 183,392 observations on 20,966 companies over 1997Q1–2000Q2, with the common comparison period ending in 2000Q1. The banks jointly represented about 40% of the Swedish business-loan market. Records contain government firm identifiers, dates, internal and credit-bureau ratings, granted credit, actual exposure, credit type, payment information, and industry. Multiple facilities per borrower are common; the economic unit for default classification is the borrower.

The overlapping subset is described as 2,880 companies and 17,476 borrower-quarter observations, averaging slightly more than six shared quarters. Tables 2 and 3 instead show a total of 17,675. This difference is present in the supplied article and is not resolved by the text. A reproduction should retain the raw identifiers and document exactly which filtering produces each count rather than force them to agree. Table 1's descriptive samples are smaller again, at 323,671 and 176,985 observations.

Bank A's average full portfolio is SEK168.4 billion across 24,895 firms; B's is SEK143.7 billion across 12,642. Average credit is therefore about SEK6.76 million at A versus SEK11.37 million at B. Median facilities are much smaller: SEK250,000–500,000 at A and SEK1–2.5 million at B. The borrower counts are dominated by small businesses. About 65% of A's and 54–55% of B's Table 1 observations concern firms with no more than five employees. Exposure-weighted composition therefore differs sharply from borrower-count composition.

A uses classes 1–15, with 1 safest and 15 defaulted. B originally numbered grades in the opposite direction; the authors reverse them so 1 is safest and 7 defaulted. Both systems are intended to measure borrower default risk, not facility loss severity or expected loss. Their operational default definition requires payments at least 60 days overdue plus a bank official's judgment that payment is unlikely. That is distinct from legal bankruptcy and from the 90-day convention discussed in Basel II. Bank default flags generally precede recorded bankruptcy.

A borrower can default at one institution while remaining performing at the other. Consequently a shared identifier does not make the two bank-specific payment streams, contractual exposures, recovery prospects, or monitoring actions identical. This is a relevant alternative to interpreting every disagreement as a measurement error. The source does not establish which bank's label is universally correct.

## How ratings are produced and compared

The ratings combine loan-officer judgment, annual accounts, credit history, simple decision rules, external bureau information, and, for larger exposures, additional quantitative models. Credit committees review material deviations. Updates are required at least annually or when commitments change; central risk control runs checks around August, compares its results with branch ratings, and asks officers to explain stale or divergent assignments. The credit bureau's rating forecasts bankruptcy over eight quarters, so its target is not identical to a bank's payment-default event.

Formal granularity overstates effective granularity. Bank A places 20–40% of borrowers in grade 9, while B places 50–60% in grade 4. These are common entry grades for new lending, and rating inertia maintains the concentration. Roughly 95–99% of A's firms occupy nine grades; a similar share at B occupies only three. Grade definitions, entry policies, update behavior, and concentration all matter, even if both institutions describe their approach as through-the-cycle.

The overlapping borrowers provide a cross-tabulation. Only 21.82% of observations defaulted at A are simultaneously defaulted at B; conversely, 28.24% of B defaults are classed as defaults at A. These conditional proportions have different denominators. A substantial fraction of A-default observations is rated B3 or B4. Even A's safest borrowers are dispersed among B's early grades rather than being contained in B1.

Quarterly Spearman correlations between A and B ratings range approximately from 0.31 to 0.45. Ties mechanically depress such correlations when half the observations occupy one grade. The authors therefore also sort within one bank's grade using the other bank's ratings, with firm identifier as a further tie-breaker, to illustrate the information lost by discretization. This produces much larger adjusted correlations, but it imports the comparator's ordering and is not an independently validated estimate of a hidden continuous credit score. It is a sensitivity exercise showing that raw rank correlations alone cannot diagnose underwriting quality.

Tables 4–5 trace the grades of borrowers before default. At A, grades 11–14 contain about 15% of the portfolio but roughly 68% of next-quarter defaults; the share is broadly persistent at longer lags. At B, grades 5–6 account for about 60% of next-quarter defaults but only just over 20% at a twelve-quarter lookback. B4 accounts for 35–64% depending on horizon. These percentages condition on future defaults and on observed earlier membership; they are not grade-level probabilities of default.

The long-horizon cells are thin. The displayed number of A defaults with the relevant history falls from 879 at one quarter to 29 at twelve, and B falls from 570 to 43. The separate “Exits” row represents firms not yet in the portfolio at the earlier date, rather than an additional grade included in the displayed grade shares. Changes in these histories and survival in the panel limit comparisons across horizons. The data nonetheless show that an institution's practical ability to identify future problem loans is not summarized by how many grade labels it has.

## The resampling model

The procedure in Section 4.1, PDF pages 16–17, follows Carey's nonparametric Monte Carlo method. It does not fit a Gaussian latent-factor default model or posit a numerical default-correlation matrix. It does impose a sampling design. Drawing loans independently within a historical quarter does not preserve arbitrary pairwise dependence beyond the structure carried by that quarter, grade, exposure, and observed outcome; the finite set of quarters bounds the aggregate states the procedure can represent.

For implementation, index bank by $b$, borrower by $i$, initial quarter by $t$, and horizon by $h$. Let $E_{bit}$ be initial exposure, $g_{bit}$ the initial internal grade, $\tau_{bit}$ the first subsequent bank-defined default within the horizon, and $E_{bi\tau}$ exposure at default. Construct a horizon record before drawing portfolios:

1. Observe initial borrower identity, date, exposure, and grade.
2. Search every quarter through $t+h$ for default, exit, and re-entry; a terminal rating alone is insufficient.
3. A default that is followed by recovery and re-entry remains a default outcome. Retain its exposure at default rather than treating the later performing grade as a clean survival.
4. Nondefault exits and temporary disappearances are excluded or assigned zero entries in the data matrices, following the source's eligibility convention. The authors explicitly abstract from selection through exit because its cause cannot be identified.
5. Retain only starting dates with the full horizon observable, giving $T-h$ horizon matrices.

The paper's description of default handling and its final statement that absent borrowers receive zero entries should be implemented with care: zero must flag ineligibility, not a zero-loss loan to be sampled. Defaults observed before subsequent disappearance are explicitly supposed to remain loss events. The PDF provides no executable reconciliation code or counts by exit reason, so an exact reconstruction needs the original implementation.

The shared-borrower subset supplies bank-specific standard profiles. For each bank, calculate the average share of shared-portfolio credit assigned to each grade. Denote it $p_{bg}$, with $\sum_g p_{bg}=1$. These are exposure shares, not borrower frequencies. For A, the source reports 40.6% in grades 1–4, 34.7% in 5–8, and 24.7% in 9–14. For B, B2 and B3 account for 32.3% and 47.4%, with B4–B6 accounting for 19.7%; sparse B1 supplies the small remainder.

The simulated portfolios are then drawn from each bank's full eligible portfolio, not just from the matched borrowers. This distinction is central. The experiment standardizes a rating-exposure profile motivated by common borrowers; it does not repeatedly revalue an identical fixed set of facilities at the two banks. Grade-specific outcome distributions and exposure distributions from the full books drive the comparison.

For each simulated portfolio, choose a starting quarter at random, then draw borrower records within its grades until the desired exposure and grade proportions are reached. A single loan may contribute no more than 3% of total portfolio size, and a grade must have at least fifteen observations at that date to be eligible. The source's warning about repeated draws indicates sampling with replacement, but exact fill, overshoot, rounding, and sparse-grade reallocation rules are not printed. These rules should be documented rather than inferred from the final tables.

Let $m_i$ count repeated draws of record $i$. With the authors' fixed 100% LGD, a transparent reconstruction of simulated loss as a fraction of initial portfolio exposure is

$$
L^{(s)}_{b,h}=
\frac{\sum_i m_i E_{bi\tau_{bit}}1\{t<\tau_{bit}\le t+h\}}
{\sum_i m_i E_{bit}}.
$$

This notation makes explicit the source's exposure-at-default numerator. The denominator may differ slightly from the target if the sampling rule permits overshoot; the original rule is needed for exact matching. For a known constant LGD $\ell$, losses scale by $\ell$, but heterogeneous LGDs correlated with borrower risk or size would not generally preserve interbank ratios.

The benchmark is SEK54.5 billion, with 50,000 simulated portfolios. Conditional-quarter sampling prevents losses from good and bad quarters being averaged within every artificial portfolio. Averaging the resulting distributions over sampled quarters forms a historical mixture. The 3% cap excludes about 0.1% of A and 0.3% of B observations, representing roughly 5% and 8% of credit in the benchmark comparison. It is therefore not an innocuous numerical convenience.

Sort the 50,000 loss fractions to estimate quantiles. In notation, $\hat F(x)=50{,}000^{-1}\sum_s1\{L^{(s)}\le x\}$ and $\hat q_p=\inf\{x:\hat F(x)\ge p\}$. Expected loss is the simulated mean. Economic capital is the chosen loss quantile minus expected loss, presuming expected losses are separately provided for. Neither recovery estimation nor an optimized lending policy is part of this model.

## Benchmark losses and capital arithmetic

All loss and capital entries in the following tables are percentages of portfolio exposure, not decimal probabilities. Table 6 gives:

| Horizon | Bank | Mean loss | 90th | 95th | 99th | 99.9th | 99.99th |
|---|---|---:|---:|---:|---:|---:|---:|
| One quarter | A | 0.06 | 0.13 | 0.16 | 0.28 | 0.43 | 0.57 |
| One quarter | B | 0.03 | 0.06 | 0.09 | 0.16 | 0.30 | 0.42 |
| Four quarters | A | 0.27 | 0.43 | 0.49 | 0.63 | 0.80 | 0.92 |
| Four quarters | B | 0.16 | 0.29 | 0.35 | 0.46 | 0.60 | 0.75 |

A's expected one-quarter loss is twice B's, but the relative tail difference is smaller. Moving to a year does not multiply every quantile by four: A's 99.9th quantile grows from 0.43% to 0.80%, while its mean rises from 0.06% to 0.27%. Common temporal aggregation rules such as square-root scaling are not assumed; the horizon records are reconstructed separately.

At a one-year 99.9% confidence level, the economic capital calculations are

$$
EC_A=0.80\%-0.27\%=0.53\%,\qquad
EC_B=0.60\%-0.16\%=0.44\%.
$$

For SEK100 billion of exposure these are SEK530 million and SEK440 million. The difference is SEK90 million, and A's amount is 20.45% higher than B's. The nearby source statement that A must make a profit “more than a quarter higher” does not follow from these rounded capital figures alone; profitability also requires a target return and revenue/cost assumptions. At 99% confidence, capital is 0.36% and 0.30%.

The source's quantile explanation on PDF page 18 also confuses units: a 99.99th-percentile loss of 0.57% has approximately 0.01% exceedance probability, or 0.0001 in decimal form, not decimal probability 0.01. At 50,000 draws, the 99.9th quantile corresponds to sorted observation 49,950, while the 99.99th corresponds to 49,995. Only about fifty and five draws, respectively, lie above those locations. The paper reports convergence at 50,000 portfolios but provides no Monte Carlo intervals or historical-data uncertainty bands for these extreme quantiles.

## Diversification and composition experiments

Table 7 varies target portfolio size from SEK5 billion to SEK150 billion, preserving the standard rating profile and the cap rules. Selected one-quarter results show the scale of the effect:

| Size, SEK billion | A mean | A 99.9th | B mean | B 99.9th |
|---:|---:|---:|---:|---:|
| 5 | 0.09 | 1.78 | 0.04 | 1.41 |
| 10 | 0.08 | 1.21 | 0.04 | 0.76 |
| 25 | 0.07 | 0.63 | 0.03 | 0.36 |
| 50 | 0.06 | 0.45 | 0.03 | 0.34 |
| 100 | 0.06 | 0.32 | 0.03 | 0.19 |
| 150 | 0.06 | 0.27 | 0.03 | 0.18 |

For doubling from SEK50 billion to SEK100 billion, the rounded 99.9th loss falls 28.9% at A and 44.1% at B. Subtracting expected losses, the corresponding reductions in quarterly economic capital are 33.3% and 48.4%: A moves from 0.39% to 0.26%, B from 0.31% to 0.16%. These direct calculations distinguish quantile reduction from unexpected-loss reduction and explain why “up to 40%” in the headline is only a rough characterization of selected scenarios.

Changing size also changes the absolute eligibility threshold implied by the 3% cap. A loan excluded from a small simulated book may become eligible in a large one. The authors attribute changes in expected loss across sizes to this changing feasible set. The experiment therefore combines diversification with an exposure-selection effect; it is not simply replication of an invariant population at larger borrower count.

Tables 8–9 replace the standard low-grade share with 10%, 20%, through 100%, preserving relative shares in the rest of the book. A's lower group is grades 9–14, and B's is 4–6. Increasing this share from 10% to 100% raises A's mean loss from 0.04% to 0.17%, and its 99.9th loss from 0.48% to 0.62%. For B, mean loss rises from 0.02% to 0.19%, and the 99.9th from 0.24% to 0.95%. At 50% lower-grade exposure, A's and B's 99.9th losses are 0.44% and 0.60%. B's lower grades separate especially risky exposures more sharply in these simulated populations.

The extreme tail is not perfectly monotonic in every row: A's 99.99th losses are 0.58%, 0.57%, and 0.55% at 10%, 20%, and 50% lower-grade shares. The paper regards such small reversals as likely artifacts of rare defaults and larger firms in safer grades, but supplies no formal uncertainty test. The broader monotonic pattern should not be promoted into a theorem about every empirical quantile.

Table 10 shifts exposure toward supposedly safer groups. With all A exposure in grades 1–4, or all B exposure in grade 2, simulated losses are zero at every displayed quantile because no eligible historical defaults produce losses. This is a property of the empirical support, not a guarantee that a future portfolio cannot default. A's other “safe” group gives a more revealing result: the row labeled 100% in grades 6–8 has mean loss only 0.04%, below the 0.06% standard mean, but 99.9th loss 0.75%, above the standard 0.43%. Lower expected loss need not imply a smaller extreme-loss quantile when exposure concentration and sparse losses differ.

There is another transcription ambiguity in the source: the prose describes this A group as grades 5–8, whereas Table 10 explicitly labels 6–8. The numbers above follow the table; a replication must obtain the actual group definition. At B, 100% in grade 3 produces a reported mean rounded to 0.00%, with 99.9th and 99.99th losses 0.03% and 0.04%. Sparse grade B1 is excluded from these experiments.

## Aggregate-state sensitivity

The authors split eligible starting quarters into the six highest- and six lowest-default quarters separately for each bank. This intentionally creates the widest available contrast, not a common exogenous recession indicator. Numbering the quarters from the beginning of the common sample, A's bad set is 2, 1, 9, 4, 7, 5; its good set is 11, 8, 10, 6, 12, 3. B's corresponding sets are 7, 5, 1, 3, 9, 11 and 10, 4, 2, 8, 12, 6. Preserve those different bank-specific partitions when reproducing Table 11.

For A, rounded expected loss remains 0.06% in both groups, while 99.9th loss rises from 0.25% in good quarters to 0.49% in bad quarters. For B, expected loss rises from 0.03% to 0.05%, and 99.9th loss from 0.22% to 0.36%. The 99.99th comparison is 0.30% versus 0.61% at A and 0.27% versus 0.46% at B. Aggregate conditions affect different portions of the two distributions differently. But “bad” here means relatively bad among the observed 1997–2000 quarters, not a financial crisis or a full-cycle stress state.

## Regulatory comparison and the material source discrepancy

Table 12 computes historical regulatory capital using the Basel II corporate-exposure treatment for all borrowers and probabilities of default accumulated over the preceding four quarters. It does not distinguish retail, SME, and corporate treatment. The economic-capital rows are annual loss quantiles less annual mean loss, reproduced from Table 6. Thus the comparison is between one historical regulatory calculation and one empirical capital model, not between regulatory capital and observed true tail risk.

Regulatory percentages for A range from 3.42% to 4.85% across 1998Q1–2000Q1, and for B from 2.68% to 3.81%. At annual 99.9% confidence, subtracting the 0.53% and 0.44% economic-capital estimates gives gaps of 2.89–4.32 percentage points for A and 2.24–3.37 for B. The paper repeatedly states a 6–9 percentage-point excess in its introduction, discussion, and text accompanying Table 12. Those statements cannot be reproduced from the printed table. This is an independently identified arithmetic inconsistency, not an official erratum or a proposed replacement for the authors' unreported calculations.

The table still supports the qualitative statement that the historical regulatory charge exceeds this empirical capital estimate. It does not establish that the excess is economically unnecessary. The resampling support omits severe states, the overlap profile emphasizes larger and safer firms, and the modeled losses exclude estimation uncertainty and changing recoveries. The data can motivate a discussion about rating comparability and diversification; they cannot determine the appropriate prudential margin beyond the observed sample.

## Reproduction priorities and limits

A reproducible implementation requires the confidential borrower-quarter panels and the cross-bank identifier match. Before simulation, reconcile the 17,476 versus 17,675 overlap counts, aggregate multiple facilities consistently, distinguish granted credit from utilized exposure, and verify the timing and absorbing treatment of default. Then reconstruct each bank's exact exposure-weighted profile, the cap-filtered grade/date eligibility pools, and the horizon-specific exit rules. Fix random seeds and state whether quarter draws are uniform, how repeated draws are treated, how exact target exposure is filled, and how unavailable grades are handled. The source does not publish these low-level choices or the code.

Validation should compare the grade cross-tabs, observed quarterly defaults, standard losses, and composition experiments before interpreting extreme quantiles. Independently recomputing $q_p-E[L]$ from the published rounded rows checks the capital convention but cannot validate the underlying dependence model. Increasing Monte Carlo draws addresses simulation noise; uncertainty about the borrower population, default clustering, and economic regime mix requires additional data or a separate statistical procedure.

The study is about institutional measurement rather than a trading strategy, so it has no return backtest, transaction-cost assumption, or investment benchmark. Its comparator is the other bank's internal system and the historical regulatory mapping. The unresolved implementation details, short time span, homogeneous LGD, selective exits, and lack of uncertainty intervals constrain absolute-capital conclusions. Its robust practical lesson is narrower and valuable: test whether rating assignments, exposure concentration, and observed default experience imply compatible loss distributions before treating the same regulatory profile as the same economic risk.

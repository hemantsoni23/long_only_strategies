# Confidence intervals for probabilities of default

Samuel Hanson and Til Schuermann. *Journal of Banking & Finance* 30 (2006), pp. 2281–2301. DOI: 10.1016/j.jbankfin.2005.08.002; accepted August 1, 2005. Source: [ConfidenceIntervalDefault_Hanson2006.pdf](../../Finance/ConfidenceIntervalDefault_Hanson2006.pdf), 21 PDF pages. The full article, every table and figure, footnotes, and references were read. Printed page $p$ is PDF page $p-2280$.

## Why this matters

A default-probability estimate without uncertainty can create false precision, especially for high-quality borrowers with few observed defaults. Hanson and Schuermann compare confidence intervals for two estimators built from the same rating histories: a cohort estimator that counts beginning-to-end-year outcomes, and a duration estimator that uses every transition and time spent in each rating. The duration method often produces much tighter intervals. Even so, many neighboring investment-grade notches cannot be reliably distinguished using twenty-two years of data.

The sharper point is that precision and correctness are different. Duration estimation gains information by imposing a continuous-time Markov structure. Its point estimates can differ materially from cohort estimates because actual rating changes display downgrade momentum. A narrow bootstrap interval around a misspecified estimator does not measure that model bias. The paper is therefore useful both for selecting a rating granularity and for understanding why apparently precise PDs from different methodologies need not agree.

This is a study of historical physical one-year default probabilities for rated US corporate obligors. It does not estimate firm-observable default models, recovery distributions, credit-spread risk premiums, or a trading strategy. Its discussion of a 0.03% capital-floor rule concerns the Basel framework cited in 2004 and is historical, not a claim about current regulation.

## What the paper adds

Cohort and duration estimators, binomial intervals, and parametric simulation of rating histories are established methods. The contribution is a systematic comparison of analytic intervals and parametric/nonparametric bootstrap intervals on a common data set, followed by diagnostics of estimator disagreement, monotonicity, business-cycle conditioning, and sample-window effects.

The nonparametric bootstrap resamples actual issuer histories rather than generating all histories from the fitted Markov process. This preserves observed within-history features, including patterns inconsistent with a simple Markov chain, at the resampling stage. It does not remove the Markov assumption from the duration estimator applied to each resample. That separation is essential to reading the claimed efficiency gain correctly.

The authors also use bootstrap pairs of PD estimates to examine whether worse ratings reliably imply higher one-year PDs. This is more informative than reading rounded point estimates alone, though their probability-of-reversal calculation should not be confused with an automatically calibrated simultaneous test of the entire ordered rating system.

## Data, scope, and treatment of withdrawn ratings

The source uses Standard & Poor's rating histories from January 1, 1981 through December 31, 2002. There are 6,776 unique US-domiciled corporate obligors, mainly large institutions. Government entities, municipalities, sovereigns, and non-US firms are excluded. Ratings below CCC are pooled with CCC because of small sample sizes. Whole-grade and notch-level systems are estimated separately; aggregating an intensity model is not generally equivalent to simply averaging the published notch PDs.

The duration sample contains 50,611 firm-years and 842 rated defaults, for an overall annual default ratio of 1.66%. Exposure includes time spent rated before a withdrawal to Not Rated, or NR. Defaults following an NR transition are excluded from those rated-default counts.

The cohort sample has 46,814 firm-years and 855 defaults. Firms ending a year in NR are removed, while NR-to-default paths within a year can contribute default outcomes. Thirteen such additional defaults explain why the cohort default count exceeds the duration count despite its smaller denominator. Thus differences between estimators reflect both use of intermediate transitions and specific censoring/exposure conventions.

Withdrawal is treated as noninformative in the industry-standard adjustment described by the article: probability assigned to NR is effectively redistributed across other states by excluding withdrawn cases. This is an assumption, not an empirical demonstration that withdrawal contains no credit information. A replication should report the transition history through NR explicitly and test whether informative withdrawal changes conclusions.

## Cohort estimator and its likelihood interpretation

Let $N_i(t)$ be the number of firms starting year $t$ in rating $i$, and $N_{ij}(t)$ the number ending it in state $j$ under the cohort eligibility rules. The pooled estimator is

$$
\widehat P_{ij}^{coh}=\frac{\sum_{t=1}^T N_{ij}(t)}{\sum_{t=1}^T N_i(t)}.
$$

The one-year PD for rating $i$ is the default-column entry. Intermediate moves are discarded. A firm that moves A to BBB to B to default within the year supplies one A-to-default cohort observation, while its intermediate exposures and transitions matter in the duration approach.

Under a homogeneous discrete-time Markov model, the cohort proportions maximize the multinomial transition likelihood. For one rating's default/nondefault outcome, the marginal calculation is binomial. Denoting defaults by $d$ and eligible firm-years by $n$, $\widehat p=d/n$. Inference based on an iid binomial distribution additionally assumes stable default probability and independence across observations. Repeated issuers, macro shocks, industry clusters, and business links can violate those assumptions.

A pooled estimate is exposure weighted across calendar years, not an equal-weight average of annual PDs. Its interpretation is tied to the sample's composition of issuers and regimes. Extending the window increases observations while potentially mixing different rating practices and macroeconomic states.

## Duration estimator and its assumptions

For rating $i$, let $T_i$ be total observed time spent in the rating and $N_{ij}$ the count of all observed transitions from $i$ to $j$. A time-homogeneous continuous-time Markov chain has generator $Q$ with off-diagonal intensities $q_{ij}\ge0$ and diagonal $q_{ii}=-\sum_{j\ne i}q_{ij}$. Default is absorbing. The standard likelihood, expressed in transition counts and exposure times, is proportional to

$$
\ell(Q)=\sum_i\sum_{j\ne i}N_{ij}\log q_{ij}-\sum_iT_i\sum_{j\ne i}q_{ij}.
$$

Its unrestricted off-diagonal estimates are $\widehat q_{ij}=N_{ij}/T_i$, and the one-year transition matrix is

$$
\widehat P^{dur}(1)=\exp(\widehat Q),\qquad \widehat{PD}_i=\widehat P^{dur}_{iD}(1).
$$

These formulas make explicit the intensity procedure sketched in Section 2; the article refers readers elsewhere for the full derivation. A multi-step path can contribute to the one-year default probability even when no firm begins a year in that rating and directly defaults before year-end. This is why the duration method can produce positive AAA PDs with zero observed AAA cohort defaults.

The method assumes the current rating summarizes relevant history and that the generator is constant over the estimation window. If a recent downgrade raises the next downgrade/default hazard even after conditioning on current rating, the current grade is not a sufficient Markov state. Ignoring such momentum averages stable incumbents with rapidly deteriorating entrants and can underestimate chains of successive downgrades.

The article mentions nonhomogeneous duration methods in its background but its central comparisons use the homogeneous intensity estimator. A nonparametric bootstrap of that estimator is not the same thing as estimating a fully nonparametric nonhomogeneous transition process.

## Analytic cohort intervals

The Wald interval is

$$
\widehat p\pm z_{1-\alpha/2}\sqrt{\frac{\widehat p(1-\widehat p)}{n}}.
$$

It can extend outside $[0,1]$, and truncating it does not fix poor coverage. When $d=0$, its estimated standard error is zero, giving a degenerate interval. A large sample size alone is not sufficient to rescue the normal approximation if the expected event count remains small.

The Agresti–Coull construction uses $z=z_{1-\alpha/2}$,

$$
\widetilde n=n+z^2,\qquad
\widetilde d=d+\frac{z^2}{2},\qquad
\widetilde p=\frac{\widetilde d}{\widetilde n},
$$

and reports $\widetilde p\pm z\sqrt{\widetilde p(1-\widetilde p)/\widetilde n}$, truncated to the probability range when necessary. At 95%, replacing 1.96 by two motivates the familiar “add two successes and two failures” description. The adjusted center is an interval device; it is not the original maximum-likelihood PD.

Clopper–Pearson inverts binomial tails. For $0<d<n$, its endpoints can be written as beta quantiles,

$$
p_L=\operatorname{Beta}^{-1}(\alpha/2;d,n-d+1),\qquad
p_U=\operatorname{Beta}^{-1}(1-\alpha/2;d+1,n-d).
$$

For zero defaults, $p_L=0$ and $p_U=1-(\alpha/2)^{1/n}$ for a two-sided interval. This representation is a mathematically equivalent implementation of equation (6). “Exact” refers to binomial finite-sample coverage, which is generally conservative because outcomes are discrete. It does not make the interval exact when defaults are dependent or probabilities heterogeneous.

The source's confidence statement concerns repeated-sample coverage of a fixed unknown parameter. It is not a posterior statement assigning 95% probability to the realized interval under an unspecified prior. It is also not a 95% prediction interval for next year's realized portfolio loss or default count.

## Bootstrap design

The nonparametric bootstrap draws complete observed firm-rating histories with replacement, keeping the number of histories fixed. For each of 10,000 resamples, estimate the entire migration matrix and extract its default column. The empirical tails yield reported intervals. History lengths vary, so total firm-years vary slightly across resamples; the coefficient of variation in total exposure is just under 1%. Truncating a final history to force constant exposure would damage the natural observation unit and is not done.

Resampling a full history preserves that firm's observed sequence, rather than independently resampling rating transitions and destroying downgrade persistence. It still does not automatically preserve dependence between different issuers hit by the same shock. The authors acknowledge common factors, industry heterogeneity, and business-link default dependence. Restricting the universe to US corporates removes some heterogeneity; conditioning on recession/expansion removes some common variation; neither proves conditional independence.

The parametric bootstrap first estimates a generator, then simulates continuous-time Markov histories. Each synthetic history starts in the corresponding observed initial rating and is limited by the observed censoring horizon. Following the comparison study, NR, end of observation, and actual default can all delimit that horizon. The authors question treating actual default as a censoring bound for a counterfactual synthetic path but say the choice has little numerical effect here. Each synthetic data set is then analyzed with either the cohort or duration estimator.

This creates two distinct experiments. The nonparametric version asks how the estimator varies across resampled observed histories. The parametric version asks how it behaves if the fitted Markov model is the data-generating process. Agreement between the two for a given estimator is informative, but it cannot by itself validate all dependence or model assumptions.

With zero cohort defaults in every observed history, ordinary resampling cannot invent a default. The nonparametric cohort interval is therefore also zero-width. That is a support limitation of the empirical bootstrap, not evidence that the true PD is zero. Analytic small-event intervals or an explicit model are needed to express uncertainty beyond the observed support.

## Main numerical comparison

The following whole-grade values combine Tables 2 and 3. Every number is in basis points of annual probability; 100 basis points is 1%.

| Grade | Cohort PD | Cohort Agresti–Coull 95% interval | Duration PD | Duration nonparametric 95% interval |
|---|---:|---:|---:|---:|
| AAA | 0.00 | [0.00, 19.15] | 0.03 | [0.01, 0.07] |
| AA | 1.49 | [0.00, 9.37] | 0.54 | [0.11, 1.32] |
| A | 6.20 | [2.90, 12.46] | 0.86 | [0.55, 1.32] |
| BBB | 35.74 | [25.55, 49.81] | 10.43 | [6.09, 15.60] |
| BB | 140.70 | [114.98, 172.00] | 62.62 | [51.11, 75.44] |
| B | 651.80 | [598.20, 709.83] | 470.19 | [430.12, 511.30] |
| CCC and below | 2,853.54 | [2,549.81, 3,177.98] | 4,228.42 | [3,879.11, 4,597.62] |

AAA has 2,417 cohort observations and no defaults. Its Clopper–Pearson upper limit is 15.25 bp, consistent with the zero-event formula. AA has 6,690 observations and one default. Thus the wider AAA interval under the two nondegenerate analytic methods reflects less exposure, despite a smaller observed PD. Wald and nonparametric cohort intervals for AAA are both [0,0].

For A, the cohort point estimate is more than seven times the duration estimate. For BBB it is over three times as large. These differences are much larger than rounding or minor choices between analytic binomial intervals. CCC reverses the pattern: the duration estimate is about 42.3%, versus a 28.5% cohort estimate. Rapid entries into CCC followed by default make time-in-state information particularly important at the bottom of the rating scale.

Duration parametric and nonparametric intervals are almost identical for most grades. At CCC, however, the nonparametric interval has width 718.51 bp versus 534.65 bp for the parametric interval, about 34% wider. The authors connect this to mixtures of firms originally rated CCC and firms recently downgraded into it. That is consistent with a missing-history-state problem, not a fully identified causal explanation.

The text says Wald intervals are generally shortest, but exact table values contain exceptions beyond the one singled out in the prose: for example, the nonparametric cohort widths for BBB and B are slightly shorter than their Wald counterparts. The substantive distinction is zero-event failure and broad uncertainty, not a universal ordering of all reported interval lengths.

## Estimator disagreement as a Markov diagnostic

Table 4 applies both estimators to parametric Markov simulations. Their average PD estimates then move much closer. For A, duration averages 0.86 bp and cohort 0.88 bp, compared with actual-data estimates 0.86 and 6.20. For BBB, the simulated means are 10.43 and 10.75 bp, compared with actual estimates 10.43 and 35.74. For BB, they are 62.66 and 65.27 bp, compared with 62.62 and 140.70.

The simulation therefore shows that the empirical estimator gap is not an inevitable arithmetic consequence of the two definitions. It is consistent with rating-history features missing from a homogeneous Markov generator, especially downward momentum. Censoring and exposure differences still create some simulated gaps; for B the parametric means are 470.48 and 500.42 bp. The experiment is evidence about the fitted model's failure to reproduce the observed gap, not a formal unique attribution of all bias to momentum.

A printed caption under Table 4 reverses the panel descriptions. The panel headings and surrounding analysis establish that the top is nonparametric and the bottom parametric; those are the conventions used here. The text's broad statement that parametric intervals overlap at every grade also has a visible AAA qualification: the printed parametric cohort percentile interval is [0,0], despite a positive bootstrap mean of 0.03 bp, whereas duration is [0.01,0.07]. A tiny number of positive simulated cohort outcomes can raise the mean while leaving both central percentile endpoints zero. The broader middle-grade convergence remains clear.

## Rating granularity and monotonicity

Notch-level Table 1 is not perfectly ordered. Duration PDs are 0.05 bp for AA+, 0.93 for AA, 0.44 for AA−, 0.46 for A+, 0.84 for A, and 1.00 for A−. Sample noise and the different migration paths can produce apparent reversals. Whole-grade pooling reduces variance but discards distinctions a rating system may wish to maintain for other purposes.

The bootstrap diagnostic compares adjacent ratings jointly within each resample. For better grade $k$ and worse grade $j$, it reports the fraction with $\widehat{PD}_j^{(b)}<\widehat{PD}_k^{(b)}$. Small fractions support the intended ordering. In the full sample, the reversal fraction is 9.16% for AA+ versus AAA, 69.63% for AA− versus AA, 46.33% for A+ versus AA−, and 31.90% for BBB− versus BBB. Those results do not support fine one-year-PD distinctions among many investment-grade notches.

The speculative-grade evidence is stronger, especially for B+, B, B−, and CCC. But “all speculative notches are cleanly monotone” would overstate Table 5: the BB versus BB+ reversal fraction is 13.82% in the full sample and 25.84% during expansions. Other adjacent pairs are much more reliably ordered.

Overlap of separate 95% confidence intervals is not a formal test that two PDs are equal, because the estimates are correlated and overlap can coexist with a significant difference. The paired bootstrap is more directly relevant. Likewise, a reversal fraction exceeding 5% generally means the data do not establish the intended ordering at that threshold; it does not automatically mean monotonicity has been rejected in favor of the opposite order. The paper's occasional “reject monotonicity” wording should be read with that distinction.

The reported probabilities are empirical bootstrap tail fractions, labeled nominal $p$-values by the authors. They are not exact null-imposed $p$-values, and sixteen adjacent comparisons introduce multiplicity. No familywise simultaneous ordering guarantee is supplied. A production rating calibration might impose monotonicity or pool grades, but that would be an additional estimator and should be evaluated separately from these unconstrained estimates.

## Business-cycle conditioning

NBER recession dates partition the rating exposure and transitions. Because cycle dates are monthly while ratings change daily, the implementation places regime changes at midmonth. Only 1982 is a wholly recession year in the sample; 1981, 1990, 1991, and 2001 contain mixed regimes. Separate duration estimates use recession days and expansion days rather than assigning each mixed calendar year to one state.

Eight of sixteen adjacent-notch reversal fractions exceed 5% in both the pooled and expansion calculations. Only four exceed 5% during recessions. For A versus A+, the reversal fraction falls from 17.96% pooled and 19.35% in expansion to a reported 0.00% in recession. For A− versus A it falls from 33.99% to 0.19%. More defaults in stressed regimes can make some PD differences easier to detect despite fewer observations.

The improvement is not uniform. BBB+ versus A− has a 0.87% reversal fraction in expansion but 28.00% in recession; BBB− versus BBB reaches 65.68% in recession. Conditioning changes both the underlying probabilities and estimation uncertainty. It should not be sold as a mechanical cure for nonmonotonicity or correlated default risk.

Table 5 also prints a double significance star on a 2.34% reversal fraction despite defining double stars as 1% significance. The numerical value, rather than that marker, is the reliable object to carry into a replication.

## One-year windows versus the long-run estimate

Figure 3 estimates each grade's PD with rolling one-year windows and nonparametric intervals, then compares them with the full-sample estimate. Duration methods identify considerable conditional variation. B PD is above the estimated long-run level in five of twenty-two years and below it in nine. BB and B are elevated in 1990–1991; most grades other than AAA and AA are elevated in 2001; many are low in the mid-1990s.

The highest grades display an apparent change around 1989. Before then, their annual duration PDs are sometimes above the long-run level; afterward the intervals are mostly below it. The authors connect this to a decline in large multi-grade downgrades, which strongly influence low-PD multi-step paths. A shift toward more gradual rating adjustments is one explanation, but a change in underlying issuer shocks cannot be excluded.

The comparison treats the estimated unconditional PD as fixed, explicitly abstracting from its sampling error. Consequently, the count of years deemed different is not a full joint test that incorporates uncertainty in both estimates and their overlap in data. For a rigorous modern comparison, bootstrap the annual-minus-long-run difference jointly, and account for repeated window comparisons and shared macro shocks.

Cohort rolling estimates are much less informative in the high grades: no AAA starts lead to default within a year, and the single AA event occurs from AA− in 1999. The duration method extracts information from transitions throughout the rating network, but that information is valuable only to the extent that the assumed transition model is credible.

## Implications and a reproducible workflow

The historical Basel floor of 3 bp is above the upper duration interval for AAA, AA, and A, but lies inside the cohort interval for AA. This illustrates how a policy comparison depends on the estimator. It does not establish that a regulatory floor should equal a point estimate, that narrow model-based intervals capture all risk, or that the paper's one-year US corporate evidence transfers to other assets and horizons.

For internal rating design, the evidence favors caution about adding fine PD distinctions at the safest end. Splitting riskier grades can be statistically more defensible because events are more frequent. Ratings may still encode information about long-horizon credit quality, migration risk, or recovery that is not measured by this one-year-PD experiment; lack of precise one-year separation is not proof that every high-grade modifier is economically useless.

Replication begins with dated issuer histories, entry dates, withdrawals, default definitions, and whole-grade/notch maps. Reproduce 6,776 issuers, the two exposure totals, and the 842 versus 855 event counts before estimating matrices. Build cohort counts and duration transition/exposure arrays from the same cleaned histories but with their documented censoring conventions. Compute matrix exponentials, verify nonnegative entries and row sums, and reconcile the whole-grade tables independently from notch results.

Then reproduce analytic intervals and resample complete histories 10,000 times, retaining paired grade estimates. For parametric histories, reproduce initial states, censoring horizons, and the fitted generator. Save full bootstrap draws, not only rounded endpoints, so zero-event percentile behavior and ordering probabilities can be checked. The article does not supply its random seed, full transition matrices, exact quantile interpolation, or executable date-cleaning rules; exact numerical replication therefore requires data and implementation decisions beyond the PDF.

A stronger uncertainty analysis would add calendar-time or hierarchical resampling for common shocks and explicitly model history-dependent transitions. Those are proposed extensions, not results of this paper. The central conclusion remains conditional: using full rating paths substantially improves statistical precision, but neither bootstrap precision nor a long history removes the need to examine migration-model bias, event scarcity, and dependence.

## Source map

Hanson and Schuermann (2006), “Confidence intervals for probabilities of default.” Estimators and interval formulas: Section 2, pp. 2284–2287. Sample and main intervals: Tables 1–3, pp. 2288–2290. Notch and whole-grade comparisons: Figures 1–2, pp. 2291–2293. Markov diagnostic: Table 4 and pp. 2292–2295. Monotonicity and recession conditioning: Table 5 and pp. 2295–2297. Rolling windows: Figure 3 and pp. 2297–2299. Conclusions and references: pp. 2299–2301. No separate appendix appears in the supplied article.

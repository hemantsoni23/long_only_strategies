# Automatic modelling of credit risk through internal ratings: An application of advanced statistical models and Machine Learning techniques

Raquel Flórez-López. Presentation at Credit Scoring and Credit Control IX, University of Edinburgh Management School, September 7–9, 2005.

Source: [original presentation](../../Finance/ConsumerCreditScoring_FloresLopez2005.pdf). The supplied source is a 29-slide research presentation, not a full article. Page references below are PDF slide numbers. All slides were read, including the methodological equations and numerical comparisons. The filename suggests consumer credit, but the empirical subject is European non-life insurers’ financial-strength ratings.

## Why this matters

An institution lacking a long internal default history may try to infer rating grades from public financial statements and map those grades to external default experience. That creates two distinct estimation problems: reproducing an agency’s rating decision and estimating the default frequency associated with the reproduced grade. This presentation addresses the first. It does not estimate an insurer default model, validate a probability of default, or supply a capital calculation.

The practical contribution is a comparison of interpretable statistical and tree models after aggressive feature selection. A sample of 257 insurers is represented initially by 186 candidate accounting features. The procedure retains seven features related to size, liquidity, and profitability. An oblique CART tree has the highest reported classification accuracy: 74% on the classification matrix, falling to 59–61% under bootstrap error corrections. The fall is as informative as the ranking. It shows how much apparent accuracy can disappear after accounting for model fitting in a small sample.

The source proposes four stages: feature selection, multivariate analysis, model evaluation, and a Bayesian combination of models. Only the first three are implemented. Slide 19 explicitly describes the final Bayesian hybrid as work in progress and outside the presented results. A reader should not attribute the reported performance to Bayesian model averaging, an ensemble, or a completed hybrid architecture.

## Research setting and target

Slides 3–7 use the Basel II and contemporary Solvency II discussions as motivation. These are statements about the regulatory context in 2005. The presentation contrasts internal default experience, mapping internal grades to external ratings, and statistical default models. Mapping is described as an accessible response to incomplete historical records, but one whose credibility depends on comparable internal and external rating criteria.

The empirical target is an S&P public-information, or “pi,” financial-strength rating. According to slide 21, these ratings use published accounts and other public information, omit in-depth meetings with managers, follow a moderately conservative approach, and are normally updated annually or after important events. They therefore differ in information content from interactive ratings. The slide’s awkward wording that such ratings are “not applied for” is best understood as describing the rating process; it is not evidence that the sample lacks rated companies.

Each observation is a company’s latest available pi rating during January 1999–August 2000. There are 257 non-life insurers from 14 EU countries, all subject to the source’s stated 92/49/EEC framework. Inclusion requires four years of individual financial data before the rating. Each company appears once. The five modeled categories are AA, A, BBB, BB, and B; no finer plus/minus categories are reported.

This design avoids counting the same insurer repeatedly, but it remains a selected cross-section. It excludes firms without the required rating or accounting history and does not establish performance for unrated insurers, life insurers, other jurisdictions, or a later business cycle. The country-by-country counts, insurer identities, exclusions, and five class frequencies are absent. So are the original accounting database and precise statement publication dates. “Before rating” is a useful timing restriction, but cannot be audited into a point-in-time data set without those dates.

A rating category is an ordinal assessment, not a default event. To produce a PD from an estimated category distribution, an additional mapping would be required. For example, with grade-specific default rates $d_m$ and estimated class probabilities $\pi_m(x)$, one could form

$$
\widehat{PD}(x)=\sum_{m=1}^{5}\pi_m(x)d_m.
$$

This is a derived description of the missing second stage, not an estimator implemented in the presentation. It would require matching rating type, default definition, horizon, cohort, and economic regime, and accounting for uncertainty in both $\pi_m$ and $d_m$. No such $d_m$ values appear in the source.

## Candidate variables and feature selection

Slide 22 organizes 62 underlying ratios into eight groups:

| Group | Number | Economic content |
|---|---:|---|
| EXP | 8 | Capital adequacy and exposure |
| REA | 2 | Reinsurance usage, called “reassurance” in the slides |
| LIQ | 11 | Asset structure and solvency/liquidity |
| PROF | 21 | Profit and equity structure |
| RES | 7 | Technical provisions and reserves |
| DEB | 2 | Debt composition |
| DIM | 3 | Company size |
| IND | 8 | Country-specific insurance-industry characteristics |

The current-year value, two-year average, and three-year average of each ratio produce $62\times3=186$ candidate features. Four years of accounts are required for sample eligibility, but the presentation does not explain every underlying ratio or whether growth measures require the extra lag. One should not invent definitions from codes such as PROF19 or LIQ1.

The five-step procedure on slides 14–15 and 23 is as follows. First, parametric and nonparametric tests of equality of means and medians remove 42 features. Four relevance methods then operate on the remaining 144: Relief-F, WACSA, a Bayesian Gibbs approach, and neural-network-based measures. Each relevance indicator is normalized to $[0,1]$. A Final Relevance Measure, $FRM_i$, combines the indicators, and the ordered list is cut at a gap satisfying

$$
FRM_i\geq k\,FRM_{i+1}.
$$

Slide 15 suggests $k=2$ or $3$, whereas the implemented example on slide 23 uses $k=1.067$. This is a material difference in the selection rule, not a harmless rounding change. The source does not explain how the empirical value was chosen, whether several cutoffs were compared using downstream fit, or why the much smaller gap was appropriate.

The final features are DIM2, its two-year average, the two-year average of LIQ1, PROF8, the two-year average of PROF8, the three-year average of PROF10, and the three-year average of PROF19. Seven of 186 candidates survive, about 3.76%. No EXP, REA, RES, DEB, or IND variable survives. That result describes selection conditional on this candidate set and procedure. It does not establish that capital adequacy, reinsurance, reserves, or national institutions are economically irrelevant to insurer creditworthiness.

The selected variables are substantially correlated. Slide 23 reports correlations near 0.9 between DIM2 and its two-year average, near 0.9 between PROF8 and its two-year average, near 0.8 between PROF8 and three-year PROF19, and near 0.6 between three-year PROF10 and three-year PROF19. A small selected subset is therefore not necessarily a low-collinearity subset. Individual coefficient signs and significance can be unstable even when aggregate prediction is useful.

Several central replication inputs are missing: the initial test statistics and significance levels; treatment of multiple comparisons; Relief-F distance, neighbor count, and sampling scheme; the definition and tuning of WACSA; the Gibbs sampler’s likelihood, priors, chain length, and convergence checks; neural-network architectures and relevance calculations; and the aggregation formula for $FRM$. Normalizing four scores to the same interval does not define how they are combined. An equal-weight average, rank combination, and product would select different subsets. None should be presented as the author’s undisclosed formula.

The terminology “strongly relevant” is also not a proven conditional-independence statement. The procedure identifies a practically selected set; the slides give no theorem showing that the set is necessary and sufficient for the agency’s decision rule.

## Models and a coherent mathematical reconstruction

Let $x_i\in\mathbb R^7$ denote the selected accounting features, and let $y_i\in\{1,\ldots,5\}$ index the ordered rating categories. The presentation supplies model families and partial formulas but no fitted coefficient vectors or complete trees. The following notation makes those families implementable while separating conventional model definitions from unavailable fitted specifications.

For multiple discriminant analysis, slide 16 writes up to four linear discriminant scores,

$$
Z_{im}=\alpha_m+\beta_m^\top x_i,\qquad m=1,\ldots,4.
$$

Under the conventional common-covariance Gaussian implementation, class means $\mu_m$, common covariance $\Sigma$, and class priors $\rho_m$ imply class scores

$$
\delta_m(x)=x^\top\Sigma^{-1}\mu_m
-\frac12\mu_m^\top\Sigma^{-1}\mu_m+\log\rho_m.
$$

Prediction selects the largest score. This explicitly states the distributional and prior assumptions needed for that implementation; the slides do not give the covariance treatment, priors, standardization, or regularization actually used. With correlated ratios and small rating categories, these choices can affect results materially.

For multinomial logit, use category 1 as reference, $z_{i1}=0$, and for $m=2,\ldots,5$ let $z_{im}=\alpha_m+\beta_m^\top x_i$. Then

$$
\pi_{im}=\frac{e^{z_{im}}}{\sum_{h=1}^{5}e^{z_{ih}}},
\qquad
\ell=\sum_i\log\pi_{i,y_i}.
$$

There are four class-specific linear predictors; maximum likelihood maximizes $\ell$. This model does not impose ordinal structure. The usual maximum-probability rule minimizes estimated equal-cost classification error, but another rating loss matrix could give a different decision. No economic loss matrix is specified in the source.

For a conventional ordered logit, define a latent index $x_i^\top\beta+\varepsilon_i$, with logistic $\varepsilon_i$, and increasing thresholds $a_0=-\infty<a_1<\cdots<a_5=\infty$. Then

$$
\pi_{im}=\Lambda(a_m-x_i^\top\beta)
-\Lambda(a_{m-1}-x_i^\top\beta),
\qquad \Lambda(u)=\frac1{1+e^{-u}}.
$$

Maximize the same categorical log-likelihood subject to ordered cutoffs. Common slopes across cutoffs give the proportional-odds restriction. Slide 16 prints differences in the opposite order and includes an error term in the quantity fed into the CDF. Without a declared descending-threshold convention that expression is ambiguous. The formula above is a coherent ascending-threshold reconstruction, not a claim to have recovered the author’s exact coding. The category orientation must be fixed before interpreting a positive coefficient as better or worse credit quality.

The tree comparisons are C4.5, univariate CART with Gini splitting, and oblique CART with Gini splitting. If node $A$ contains empirical class shares $p_{m,A}$, its Gini impurity is

$$
G(A)=1-\sum_m p_{m,A}^2.
$$

A candidate split seeks a large reduction in impurity,

$$
G(A)-\frac{n_L}{n_A}G(A_L)-\frac{n_R}{n_A}G(A_R).
$$

A univariate split uses $x_j\leq t$; an oblique split uses $a^\top x\leq t$. The latter can express interactions among correlated financial measurements in a single branch, but requires more information to inspect or reproduce. C4.5 uses entropy-based gain or gain ratio, as described on slide 17. The source mentions pruning and stopping mechanisms but does not provide their empirical settings, minimum leaf size, class weights, oblique search algorithm, or final split coefficients. Therefore the reported nine-rule oblique tree cannot be implemented from the slides alone.

## Error estimation and what the numbers mean

Slides 18 and 24–26 distinguish the classification-matrix hit rate, a relaxed rating comparison, and bootstrap-corrected hit rates. The relaxed criterion is described on slide 18 as a direction-dependent one-notch adjustment: predicted rating minus one for AA/A or plus one for BBB/BB/B. The results slides abbreviate it as “+1 or −1 notch.” The exact loss matrix is absent. Consequently, these percentages should be called the source’s soft classification measure, rather than silently recast as a completely specified symmetric $|\widehat y-y|\leq1$ criterion.

Write $e_{\rm app}$ for resubstitution error and $e_{\rm oob}$ for the average error on observations excluded from each bootstrap training sample. The .632 estimator is

$$
\widehat e_{.632}=0.368e_{\rm app}+0.632e_{\rm oob}.
$$

The rationale is that sampling $N$ times with replacement includes a particular observation with probability $1-(1-1/N)^N\approx0.632$. The .632+ construction increases the weight on out-of-bag error when resubstitution is overly optimistic. In the source’s notation, with true-label shares $p_m$, predicted-label shares $q_m$, and no-information error $\gamma=\sum_m p_m(1-q_m)$,

$$
R=\frac{e_{\rm oob}-e_{\rm app}}{\gamma-e_{\rm app}},
\qquad w=\frac{0.632}{1-0.368R},
\qquad \widehat e_{.632+}=(1-w)e_{\rm app}+we_{\rm oob}.
$$

The slide does not document bounding of $R$, degenerate denominators, bootstrap count, random seed, or interval construction. Most importantly, it does not state whether the 186-to-seven feature search is repeated inside each bootstrap sample. If the subset was selected once using all outcomes, resampling only the final classifier fails to capture selection optimism. A faithful report must preserve that uncertainty.

The complete headline comparison is:

| Model | Apparent exact hit rate | Soft measure | Bootstrap hit rate | Printed parenthetical interval |
|---|---:|---:|---:|---:|
| MDA | 59% | 94% | 56% | 0.52–0.60 |
| Multinomial logit | 60% | 95% | 53–54% | 0.45–0.63 |
| Ordered logit | 58% | 91% | 55% | 0.44–0.65 |
| C4.5 | 66% | 98% | 53–55% | 0.50–0.61 |
| CART, univariate Gini | 68% | 92% | 56–58% | 0.48–0.68 |
| CART, oblique Gini | 74% | 96% | 59–61% | 0.49–0.66 |

The source does not identify the confidence level or exact meaning of the parenthetical intervals. Calling them 95% confidence intervals would supply missing information. Likewise, where a range is given for the two bootstrap methods, the slides do not assign each endpoint unambiguously to .632 versus .632+.

The oblique tree’s apparent advantage over univariate CART is six percentage points. Their corrected ranges differ by about one to five points, depending on which estimates are compared, and their printed intervals overlap substantially. There is no paired test or interval for the difference. The result supports the author’s ranking on the reported point estimates; it does not establish statistically decisive dominance. The highest soft score belongs to C4.5, further showing that “best” depends on the loss criterion.

## Interpretation, complexity, and limits

MDA identifies two-year LIQ1 with a negative sign, two-year DIM2 with a positive sign, and three-year PROF10/PROF19 with positive signs. Multinomial logit reports the two profitability measures positive across all functions, with the liquidity measure negative in functions 2–4. Ordered logit reports the same two profitability measures and the liquidity measure. Because the original ratio definitions, category coding, standard errors, and fitted equations are absent, these are reported signs, not a recoverable economic comparative-static model.

The logit pseudo-$R^2$ values are 60%, 64%, and 34% for multinomial logit under Cox–Snell, Nagelkerke, and McFadden definitions; ordered logit gives 54%, 58%, and 29%. They measure different likelihood comparisons and are not proportions of rating variance explained. They should not be compared directly with classification hit rates.

Tree size also matters. C4.5 has 11 rules and maximum depth six, with rule counts AA:0, A:3, BBB:6, BB:1, B:1. Univariate CART has 12 rules, depth six, counts 0/5/5/1/1, and uses six features excluding two-year LIQ1. Oblique CART has nine rules, depth five, counts 0/2/4/2/1, and uses all seven features. No tree has an AA terminal rule. If those terminal labels determine predictions, the trees never predict AA, regardless of their aggregate accuracy. That is an important limitation for a system intended to preserve the full rating scale.

The MDA comparison cites 31% accuracy “by chance.” Five equally likely categories would instead give 20%, so this is evidently a different baseline, plausibly related to unequal class frequencies. The source does not specify its calculation. Without class counts, neither majority-class accuracy nor a frequency-weighted random classifier can be independently reconstructed. The presentation notes that A and BBB are easier to predict than AA and BB, but does not publish the confusion matrices needed to assess the class tradeoffs.

For replication, the irreducible prerequisites are the insurer-level sample, ratio dictionary, point-in-time accounts, rating dates and labels, full selection implementation, all fitted-model settings, and bootstrap details. An extension should repeat feature selection inside resampling, reserve later rating dates for the out-of-time test requested by the author, and evaluate both exact-category and economically weighted errors. These are requirements for testing the proposed workflow, not results already supplied by the slides.

The source contains no loan portfolio, trading strategy, transaction costs, realized defaults, loss-given-default estimates, or profitability backtest. Its strongest supported conclusion is narrower: a compact, nonlinear rating reconstruction can fit this insurer sample better than the reported linear alternatives, but the accuracy advantage shrinks after bootstrap correction and the missing implementation details prevent exact reproduction. The proposed Bayesian combination and out-of-time validation remain future work.

## Source and intellectual context

The source’s literature discussion distinguishes rating-determinant studies of corporations and banks from the thinner insurer literature. It cites Pottier, Pottier–Sommer, Burton and coauthors, and Gaver–Pottier for insurance applications; Blume, Amato–Furfine, and Altman–Rijken provide adjacent corporate-rating context. CART, C4.5, and the Efron–Tibshirani bootstrap methods are methodological inputs, not inventions of this presentation. Those references were not independently read for this note. The original contribution documented here is their feature-selection and model-comparison application to the specified European pi-rated insurer cross-section.

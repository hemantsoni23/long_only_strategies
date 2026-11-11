# Subagging for credit scoring models

**Giuseppe Paleologo, André Elisseeff, and Gianluca Antonini. European Journal of Operational Research 201 (2010), 490–499. DOI: 10.1016/j.ejor.2009.03.008.** Source: [original PDF](../../Finance/CreditScoring_PaleologoElisseeffAntonini_2010.pdf), ten pages. The article was accepted in March 2009 and published in the 2010 volume. Page references below use journal pagination.

## Why this matters and the actual contribution

Credit scoring often starts with an unusually favorable historical sample: loans already accepted by an analyst, few observed bad outcomes, missing financial information, and multiple closely related requests from the same borrower. Applying a sophisticated classifier to such a sample does not remove the selection, imbalance, or dependence problems. A random request-level training/test split can even make a model appear successful by placing nearly identical requests from one company on both sides.

The paper develops a practical learning and validation procedure for that setting. Its central contributions are supervised minimum-or-maximum imputation, a class-balanced subsampling ensemble that retains every observed bad case in every training subsample, and company-grouped cross-validation with different training and evaluation definitions of a bad outcome. The empirical application is an IBM Global Financing Italian customer sample linked to Experian data.

Subagging is not introduced as a new general ensemble theorem. The innovation is its adaptation to rare adverse credit outcomes and its integration into a validation design that respects repeated borrower observations. The reported results favor ensembles over the corresponding single classifiers, with a decision-tree ensemble chosen for a combination of discrimination and inspectability. They do not establish that the model solves rejected-applicant selection, yields a calibrated bankruptcy probability directly, or outperforms all modern credit models.

## Outcome, score, and decision rule

Let $x_i\in\mathbb R^d$ describe a credit request and let $y_i\in\{0,1\}$ indicate a bad outcome during the following twelve months. The bad class is positive, so a larger risk score should indicate a more problematic request. The introductory formal objective is classification error,

$$
R(f)=E[|f(X)-Y|],\qquad f:\mathbb R^d\to\{0,1\}.
$$

For equal misclassification costs the Bayes rule predicts bad when $P(Y=1\mid X=x)>1/2$. This minimizes classification error, not realized delinquency in isolation or a lender's expected profit. If missing a bad borrower costs $C_{FN}$ and wrongly rejecting a good borrower costs $C_{FP}$, the corresponding probability threshold is $C_{FP}/(C_{FP}+C_{FN})$. That cost-sensitive expression is a direct decision-theoretic extension, not a loss function estimated in the article.

The experiment mainly evaluates real-valued scores using ROC area. For a threshold $b$, predict bad when $s(x)>b$. Sensitivity is the fraction of bad requests detected, specificity the fraction of good requests correctly left unflagged, and the false-positive rate is one minus specificity. An implementable empirical AUC is

$$
\widehat{AUC}=
\frac{1}{n_+n_-}
\sum_{i:y_i=1}\sum_{j:y_j=0}
\left[1\{s_i>s_j\}+\tfrac12 1\{s_i=s_j\}\right].
$$

The tie term is important for tree probabilities and finite voting ensembles. AUC measures ranking across the two classes; it neither supplies a deployment cutoff nor calibrates the numerical score as a probability. It also treats requests as equally weighted observations, whereas an expected-loss objective would distinguish exposures, recoveries, and collection costs.

The accepted-only sample explains why overall accuracy is unhelpful: predicting every request as good can be very accurate with only 5% bad outcomes. AUC and class-specific rates reveal discrimination that such an aggregate error conceals. Nevertheless they remain conditional on the population whose outcomes are observed. The paper argues that rejected requests would contain more bad cases, but those outcomes are not observed and are not recovered by balancing the accepted sample.

## Data and feature timing

IBM supplied 11,903 credit requests to Experian Italy; 10,059 were matched in the external database. After exclusions and cleaning, the analysis contains **9,730 requests from 5,153 companies**. Thus the mean is about 1.89 requests per company, but the grouping procedure must use the actual borrower identifiers, not this average. Calendar start and end dates are not reported, preventing an exact reconstruction of the economic period or of possible regime changes.

The original sample is approximately 80% industrial/commercial companies, 10% multi-year production companies, and 8.4% partnerships or individual companies. Banks, financial companies, fiduciaries, and insurers account for the remaining 1.6% and are excluded because their data and rating conventions differ and their representation is small. About 92% of the final sample are described as private companies, and 8.7% are involved in a legal-procedure event. These percentages describe different classifications and should not be forced into one mutually exclusive partition.

Table 1's activity shares include wholesale commerce 17%; metal manufacturing, mechanical manufacturing, and retail commerce 7% each; motor vehicles and informatics 6% each; business services 5%; food and drink and general manufacturing/furniture 4% each; and other activities 37%. Activity is encoded using the hierarchical Italian Ateco scheme, whose first two digits are listed in the table.

Raw inputs contain request identifiers and dates, location, business commencement dates, registry identifiers, subsidiaries, employee counts, information about the first three executives, company type and capital, legal negative events, balance sheets, accounts receivable, and Experian risk indices. The paper describes financial transformations including net worth, current assets and liabilities, total assets, revenue, net profit, liquid assets, cash flow, and several categories of ratios.

Accounts receivable are carefully split by time. Four quarters **before** the request produce, for each quarter, total outstanding debt at the snapshot, amounts due during the quarter that are not late, the ratio of debt overdue at least 90 days to total debt, and the analogous at-least-120-day ratio. Information up to one year **after** the request supplies target labels, not predictors. The distinction must be maintained when assembling a historical feature matrix; a variable named “legal event” or “accounts receivable” is not inherently safe without its observation date.

The final manually reduced feature set contains 39 variables. Because financial ratios were strongly correlated, the authors removed them and retained grouped financial quantities such as net worth, current assets, current liabilities, and total assets. They retained one Experian failure index rather than several differently scaled ordinal versions of similar information, while preserving company structure and activity variables. The complete ordered dictionary of 39 columns, cleaning thresholds, transformations, and categorical encodings is not supplied. Figure 5 labels some important retained features but is not a full schema.

## Two twelve-month definitions of bad

Table 2 distinguishes eight candidate indicators. BadGCS is a company placed on a special analyst watch list. BadAR_C is an internally defined conservative accounts-receivable outcome during the twelve months following the request; its operational threshold is not disclosed. BadWriteoff records a write-off within that year. BadAR_NC equals one when more than 10% of outstanding debt is overdue for at least 90 days during the following twelve months.

The four negative-event features differ in whose legal events count and whether a positive monetary cost is required:

| Indicator | Covered person or entity | Positive monetary cost required? |
|---|---|---|
| NEF1 | Company | Yes |
| NEF2 | Company or any of its first three executives | Yes |
| NEF3 | Company | No |
| NEF4 | Company or any of its first three executives | No |

All refer to events occurring up to one year after the request. The exact legal-event category mapping and cost measurement remain proprietary or unspecified. Such outcomes are broader than bankruptcy and need not all imply the same economic loss.

The training label is

$$
Y^{train}=NEF1\lor BadAR\_C\lor BadWriteoff,
$$

whereas evaluation uses

$$
Y^{test}=NEF4\lor BadAR\_NC.
$$

The article calls the first definition more conservative because it flags fewer bad cases, approximately 5%, while the broader evaluation definition flags approximately 11%. “Conservative” here means conservative about assigning the bad label; it does not mean a stricter loan-approval policy. Individual indicators are much rarer: BadGCS has frequency 0.49%, BadAR_C 0.53%, and BadWriteoff about 0.1%.

The training/evaluation mismatch is deliberate. The authors want to test whether a model trained on a relatively unambiguous small set of adverse cases can discriminate a broader set. It is not ordinary cross-validation under one fixed outcome definition. Nor does the logical expression guarantee perfect set inclusion without additional relationships between write-offs and the broader labels. A reproducer should calculate the actual cross-tabulation rather than assume that every training-positive event is necessarily positive under the second definition.

## Supervised extreme-value imputation

For each feature $j$, compute its minimum $m_j$ and maximum $M_j$ among observed **training** values. Create two candidate completed columns:

$$
x_{ij}^{min}=\begin{cases}x_{ij},&x_{ij}\text{ observed},\\m_j,&x_{ij}\text{ missing},\end{cases}
\qquad
x_{ij}^{max}=\begin{cases}x_{ij},&x_{ij}\text{ observed},\\M_j,&x_{ij}\text{ missing}.\end{cases}
$$

Treat each candidate column as a univariate score and compare its training AUC against the training label. Retain whichever candidate has the larger AUC. Store that choice and its training-derived endpoint; apply the same mapping to test observations. Normalization is learned afterward, also from training data only.

The rationale is that missing accounting data may itself identify a type of company, especially a small or private firm, rather than being an accidental missing-at-random measurement. Mean imputation would conceal this distinction. An extreme-value replacement makes missingness accessible to a downstream split or decision surface without introducing a separate missingness column.

This is a **supervised** preprocessing step: the choice between endpoints uses labels and therefore must be refitted inside each cross-validation training fold. Using the entire sample to choose endpoints would leak evaluation outcomes even if the final classifier were fitted only on training rows.

The paper does not specify how to handle a feature entirely missing within a fold, ties between the two AUCs, unseen categorical levels, or normalization of a zero-variance column. It also does not explain whether feature direction is reversed when lower values indicate higher risk. Literally maximizing the raw feature AUC differs from maximizing $\max(AUC,1-AUC)$. Those are reproducibility decisions that should be recorded, not silently interchanged.

Extreme imputation is not generally equivalent to observing the missing value. A genuinely observed endpoint and a missing value become indistinguishable, and outlying training values can strongly influence the replacement. The paper presents an application-motivated technique, not proof that it dominates mean imputation or explicit missingness indicators under all missingness mechanisms. It supplies no separate controlled ablation quantifying the imputation component's contribution.

## Class-balanced subagging

Partition a training fold into bad requests $S_+$ and good requests $S_-$, of sizes $n_+$ and $n_-$. For each ensemble member $t=1,\ldots,T$:

1. Keep all of $S_+$.
2. Draw $m=\alpha n_+$ distinct good requests uniformly without replacement from $S_-$. With $\alpha=1$, the subsample is class balanced.
3. Fit the selected base learner to the union of the bad cases and sampled good cases.
4. Save its score function $s_t(x)$ and average members for prediction:

$$
s_{ens}(x)=\frac1T\sum_{t=1}^{T}s_t(x).
$$

The sampling is without replacement **within** each member, but the same good request can occur in multiple members. All bad cases recur in every member. The members are therefore dependent; the procedure gains variation mainly by changing the majority-class observations, not by creating new independent bad outcomes. If $m$ is not an integer or exceeds $n_-$, rounding and feasibility rules are required; the source does not specify them.

The general exposition averages binary votes, whereas J48 returns positive-class probability estimates. Either can be averaged as a score, but averaging real-valued leaf estimates and averaging hard decisions are not identical algorithms. A replication should follow the actual base-learner outputs used in the reported experiment. For support vector machines, the paper does not fully specify whether margins, calibrated probabilities, or thresholded outputs were aggregated.

Ordinary bagging draws a bootstrap sample of approximately the original size and typically reproduces its class imbalance. This adaptation gives each base learner enough exposure to the rare class while using different subsets of the much larger good population across members. It reduces the tendency of a base classifier to devote almost all of its capacity to the majority class. It does not increase the information contained in the few bad companies or eliminate their potential outlier influence.

For an individual good request, its probability of never appearing in $T$ independently drawn subsamples is

$$
P(\text{never selected})=\left(1-\frac{\alpha n_+}{n_-}\right)^T.
$$

To make this probability at most $\delta$, take

$$
T\ge\left\lceil\frac{\log\delta}{\log(1-\alpha n_+/n_-)}\right\rceil.
$$

The paper uses $\delta=0.05$ as an order-of-magnitude guide and finds 20–50 members reasonable; its chosen J48 ensemble uses 30. This is a **per-observation** inclusion probability, not a guarantee that all good requests jointly appear. At an exactly 5% training bad rate and $\alpha=1$, the formula requires 56 members for 95% per-request inclusion; 30 gives approximately 80%. These are derived illustrations, not a contradiction of the authors' statement that the formula was only a heuristic and that imbalance varies with the outcome definition.

Balancing also changes class priors in the training subsamples. Even if a learner's numerical output were perfectly calibrated for the artificial balanced distribution, it would not automatically be calibrated for the accepted portfolio or the full applicant population. A ranking improvement and a probability calibration claim must therefore be evaluated separately.

## Validation procedure and hyperparameters

The experiment uses five repetitions of two-fold cross-validation. Each repetition partitions companies into two folds, and each fold in turn trains a model evaluated on the other. All requests from a company remain together. Positive cases are spread across folds to avoid an empty or severely deficient bad training set. Exact stratified-group allocation logic is not given, particularly for companies with requests carrying mixed labels.

Within each training fold, learn imputation, normalization, and the ensemble or single classifier. Train against the narrow bad definition, then evaluate the held-out scores against the broader definition. Record AUC for each split. The reported dispersion is an approximation based on variation across the two-fold splits; the ten results are not independent because repetitions reuse companies. They should not be interpreted as ten independent external validation cohorts.

The company grouping addresses borrower overlap. It does not create chronological validation: requests from later calendar periods may train models evaluated on earlier periods, and all periods can share macroeconomic conditions. Nor does it directly assess performance on previously rejected applications or under a different lender's acceptance policy. These are distinct generalization questions.

The models and search settings are specified as follows:

- Linear, polynomial, and radial-basis-function SVMs. The stated penalty grid is $C\in\{0.1,0.01,0.001,0.0001\}$, with RBF width candidates 1, 5, and 10. The text says degree-two polynomial kernels, but Table 3 reports degree three for the best single polynomial SVM and degree two for its subagged counterpart.
- Nearest neighbors with $k=1,\ldots,5$.
- J48 decision trees through Weka, using probability outputs.
- AdaBoost with decision stumps and a modified update designed for balanced error; the exact modified update is not printed.
- Subagged versions of each base method except AdaBoost, which the authors already adapted to imbalance.

The implementation uses the Spider MATLAB library interfaced with Weka. Historical software defaults, normalization formula, kernel-width convention, exact pruning test, and all random seeds are not documented fully. In particular, the discussion of a split-significance threshold should not be assumed identical to a current software package's default pruning-confidence option.

Feature reduction and model comparison were part of an iterative empirical process. The authors correctly keep preprocessing out of the outer test fold during training, but the article does not describe a nested loop isolating all hyperparameter choice and manual feature selection from the final evaluation. Its strong wording about unbiased AUC is therefore narrower than a guarantee of no model-selection optimism.

## Results and uncertainty

Table 3 reports:

| Base learner | Single-model AUC | Subagged AUC | Reported settings |
|---|---:|---:|---|
| Linear SVM | $0.50\pm0.003$ | $0.65\pm0.006$ | $C=0.001$ for both |
| Polynomial SVM | $0.51\pm0.008$ | $0.63\pm0.006$ | Single: degree 3, $C=0.0001$; ensemble: degree 2, $C=0.001$ |
| Nearest neighbors | $0.54\pm0.004$ | $0.62\pm0.007$ | $k=5$ |
| J48 | $0.53\pm0.010$ | $0.65\pm0.003$ | 30 ensemble members |
| RBF SVM | $0.60\pm0.006$ | $0.66\pm0.005$ | Single: width 1, $C=0.01$; ensemble: width 5, $C=0.1$ |
| AdaBoost | $0.59\pm0.003$ | Not reported | 100 stumps |

The largest displayed gain is 0.15 AUC for linear SVM; the J48 gain is 0.12, nearest-neighbor gain 0.08, and RBF gain 0.06. These are absolute AUC differences, not percentage reductions in default or expected loss. Some comparisons change hyperparameters along with resampling, so they do not isolate one intervention holding every other setting fixed.

The authors choose subagged J48 even though subagged RBF SVM has the highest numerical AUC, 0.66 rather than 0.65. The motivation is similar discrimination with simpler constituent rules. The reported variation does not supply a formal paired significance test proving equivalence or a material difference between those two ensembles. An AUC near 0.65 indicates useful but moderate ranking separation, not near-perfect identification of bad borrowers.

There is no logistic-regression result in Table 3 despite logistic regression motivating the introduction. Consequently the experiment does not demonstrate superiority to a carefully tuned logistic scorecard. It compares the listed learners under this particular data and labeling design.

## Inspecting the tree ensemble

The authors tighten the split/pruning significance threshold from $10^{-2}$ to $10^{-4}$ to $10^{-6}$. AUC remains around 0.65 while individual trees become much smaller. Figure 3 shows a three-leaf example at the strictest threshold and progressively more complex examples at looser thresholds. Figure 4 is labeled a distribution of tree sizes, while the adjacent prose refers to average depth; those are not identical quantities, so its bins should not be reported as exact depths without the original code.

Across five repetitions, two training directions, and 30 members per fitted ensemble, there are 300 fitted trees. Figure 5 counts feature use. Region and the Experian statistical index IVS are most prominent; CountryArea, net worth, total and deposited capital, Ateco activity, balance-sheet type, the failure index, and a prior-quarter accounts-receivable quantity also appear.

Some plotted counts exceed 300, so they cannot literally be the number of trees containing a variable once. They evidently allow repeated occurrences or use another counting convention. Treat them as split-use frequencies rather than normalized probabilities of inclusion until that convention is clarified. Such frequencies also do not measure causal importance or uniquely allocated predictive contribution: correlated predictors can substitute for one another, and categorical variables can offer many candidate splits.

The inspectability argument is therefore relative. Each component tree can be reviewed, and recurrent variables can be identified, but an average of thirty trees is still more complex than one decision rule. The article does not provide a complete exported ensemble or a global rule extraction proving that its decisions reduce to a small fixed scorecard.

## From score to adverse-outcome probability

The final exercise uses two-fold held-out predictions from the J48 ensemble, retaining the narrow training and broad evaluation definitions. Figure 6 estimates the score distributions separately for bad and good observations. Bad cases are relatively more prevalent at high scores; good cases concentrate toward lower values. The authors highlight separation below approximately 0.35 and above approximately 0.55, rather than identifying a universally optimal cutoff.

If $p_1(s)$ and $p_0(s)$ are the class-conditional score densities or same-bin probabilities and $\pi$ is the bad prevalence, Bayes' rule gives

$$
P(Y=1\mid s)=\frac{\pi p_1(s)}{\pi p_1(s)+(1-\pi)p_0(s)}.
$$

This supplies the explicit calculation underlying Figure 7. The text calls its priors “uniform” but says they equal the observed fractions of bad and nonbad cases; these are empirical class priors, not equal 50/50 priors. The score bins, smoothing rule, handling of empty bins, and precise averaging of the two folds are not specified.

The posterior curve is not identical to the ensemble score. Figure 7 stays near 0.05–0.10 at low scores and rises toward approximately 0.5 at the extreme high end; these are visual approximations, not tabulated estimates with confidence bands. Estimation is especially noisy where few held-out cases populate a bin. No Brier score, calibration slope, independent calibration set, or temporal calibration test is supplied.

The inferred probability concerns the broader **bad-event definition** within the observed accepted-customer population. Calling it a bankruptcy or contractual-default probability would change the event. Transporting it to all incoming applicants would additionally require assumptions or data about rejected borrowers, which the paper does not supply. Balancing training classes changes the learning problem; using empirical priors afterward does not remove selection on acceptance.

## Reimplementation boundary

The complete computational sequence can be reconstructed: define request-time predictors and twelve-month outcomes; group requests by company; generate repeated stratified company folds; learn endpoint imputation and normalization inside training; retain all bad requests and resample good requests for each member; average scores; evaluate against the broader label; and estimate score-conditioned adverse-event frequencies only from held-out predictions. Save the fold-company assignments, imputation choices, sampled indices, fitted models, and scores to make the experiment auditable.

Exact numerical reproduction is limited by proprietary customer data, missing calendar dates and data-cleaning rules, an incomplete 39-feature dictionary, undisclosed BadAR_C definition, software defaults, model-selection nesting, group-stratification details, and calibration-bin choices. No economic optimization of credit limits or approval thresholds is actually reported. The durable lesson is that rare-event learning, borrower dependence, informative missingness, and validation timing must be handled together; the best-performing classifier is only one part of that design.

# Comprehensible credit scoring models using rule extraction from support vector machines

**David Martens, Bart Baesens, Tony Van Gestel, and Jan Vanthienen.** Supplied article-in-press version, *European Journal of Operational Research* (2007), accepted April 2006. DOI 10.1016/j.ejor.2006.04.051. [Source PDF](../../Finance/SVMCreditScoring_Martens2007.pdf). All eleven pages, including references, were read; equations, rule diagrams, and Tables 2–3 were inspected visually. Page references refer to the supplied PDF, which has no final volume or journal pagination.

## Why this matters

A decision system may need a compact rule set that a credit officer can inspect, while its best predictive model is a nonlinear kernel classifier. This paper asks whether the nonlinear model can act as a teacher: label real or synthetic observations with its decisions, then train a simpler rule system to approximate those decisions. The teacher and the deployed rule system are distinct estimators. Accuracy against actual outcomes and fidelity to the teacher must therefore be assessed separately.

The authors extend two pedagogical techniques from neural-network interpretation to SVMs: Trepan, which queries the trained model for additional synthetic labels while growing a tree, and G-REX, which searches symbolic rules using genetic programming. They compare these with C4.5 trained on teacher-generated labels, conventional C4.5 on actual outcomes, logistic regression, and the original SVM. They also review two decompositional methods that use the teacher's internal geometry.

The result is heterogeneous. On the Australian credit dataset, Trepan retains 99.0% fidelity and loses only 0.6 percentage points of accuracy. On the corporate bankruptcy dataset, it loses 14.5 points, and its 82.0% accuracy is below the 87.0% logistic baseline. The paper's general language about a small loss of performance therefore requires dataset-specific qualification. The useful contribution is an experimentally evaluated route to simpler surrogates, together with clear metrics for the cost of simplification, not a universal claim that explanation is nearly free.

## Teacher model and the objects being approximated

For observations $(x_i,y_i)$ with binary labels $y_i\in\{-1,+1\}$, the SVM minimizes

$$
\frac12\|w\|^2+C\sum_i\xi_i,
\qquad y_i\{w'\phi(x_i)+b\}\ge1-\xi_i,
\quad \xi_i\ge0.
$$

The dual maximizes

$$
\sum_i\alpha_i-\frac12\sum_{i,j}\alpha_i\alpha_jy_iy_jK(x_i,x_j),
\qquad 0\le\alpha_i\le C,\quad\sum_i\alpha_i y_i=0.
$$

Its decision is $f(x)=\operatorname{sgn}[\sum_i\alpha_i y_iK(x_i,x)+b]$. The experiments use the RBF convention

$$
K(x,x_i)=\exp[-\|x-x_i\|^2/\sigma^2].
$$

This has no factor two in the denominator. Kernel bandwidths from an implementation using $\exp[-\|x-x_i\|^2/(2s^2)]$ must be translated as $\sigma^2=2s^2$. The paper uses grid search for bandwidth and regularization but does not publish the grid, chosen values, scaling rules, or exact internal validation procedure.

The SVM's convex objective protects its fitted coefficients from the neural-network type of local minima for fixed hyperparameters. It does not make bandwidth selection, tree growth, or genetic rule search convex. The margin loss is also not a default probability or expected-credit-loss objective. Since only class labels are queried during extraction, magnitude information in the SVM decision value is discarded. The source identifies margin-based confidence as future research; a raw margin would still need calibration before being interpreted as a probability.

Let $g$ denote an extracted rule classifier. On a held-out sample of size $n$, the principal metrics are

$$
\operatorname{Accuracy}(g)=\frac1n\sum_i1\{g(x_i)=y_i\},
\qquad
\operatorname{Fidelity}(g,f)=\frac1n\sum_i1\{g(x_i)=f(x_i)\}.
$$

The third reported metric is the number of rules. High fidelity can preserve the teacher's mistakes; high accuracy can coexist with imperfect fidelity if the surrogate corrects them. Conversely, good global fidelity need not preserve decisions for rare defaults or a small sensitive segment. The article reports global metrics and no segment-specific fidelity or error costs.

A useful derived bound is

$$
|\operatorname{Accuracy}(g)-\operatorname{Accuracy}(f)|
\le1-\operatorname{Fidelity}(g,f),
$$

because the two accuracy indicators can differ only where the classifiers disagree. This is a diagnostic relation, not a guarantee of acceptable performance. It holds without assuming the teacher is correct. No source theorem says that copying a fitted model necessarily removes noise rather than copying its bias.

## Decompositional methods: what the survey actually specifies

SVM+Prototype first clusters observations using vector quantization. Cluster prototypes define centers of ellipsoidal rule regions; support vectors determine their extents, with the furthest relevant support vector defining the long axis. An equation rule can use an ellipsoidal quadratic condition, while interval rules use coordinate-aligned regions. A partition test subdivides a proposed region when its prototype, vertices, or contained support vectors indicate conflicting classes. Iteration ends when no region requires division or a specified iteration limit is reached.

This procedure uses the SVM's internal support-vector information and is therefore decompositional. The source warns that complex data can generate many regions and hence many rules, defeating compactness; overlap also complicates clustering. It provides a conceptual diagram, not the complete numerical clustering and ellipsoid-construction settings needed for a fresh implementation. Its tabulated results are imported from other publications, not run under the paper's twenty-split experimental protocol.

The method reviewed from Fung and coauthors constructs nonoverlapping axis-aligned boxes for a **linear** SVM. A box corresponds to a conjunction $l_j\le x_j<u_j$ across coordinates. The source transforms a bounded domain to a unit box, reversing coordinates with negative coefficients. It then selects boxes by volume or data-point coverage, arranging a boundary vertex on the separating hyperplane. It does not directly apply to the nonlinear RBF teachers used in the main experiment.

There are two source-level implementation cautions. First, p. 5 calls the decision hyperplane $w'x+b=0$ and then writes its negative-side region as $w'x<b$. These conventions conflict: with the first convention the threshold is $-b$. One can avoid the mismatch by writing a separate threshold $h$ and consistently using $w'x<h$. The transformation's denominator is then $h-w'd$. Zero coefficients require separate handling because the printed diagonal transformation uses $\operatorname{sign}(w_j)$ and is singular when $w_j=0$.

Second, the displayed maximum-volume objective in equation (14) is

$$
\max_{0<x_j\le1}\ \sum_j\log x_j,
\qquad \sum_j\widetilde w_jx_j=1
$$

in normalized coordinates. It is a concave objective maximized over a convex feasible set, not an ordinary linear program despite the surrounding summary's reference to linear programs. The positive-domain restriction is implicit in the logarithm. If all transformed weights are positive, its interior KKT condition is $1/x_j=\lambda\widetilde w_j$, with upper bounds active when that solution exceeds one. This reconstruction describes the displayed subproblem; it is not a full recreation of the original cited extraction algorithm, whose partition management and coverage variant require further details.

## Pedagogical C4.5 and Trepan

The simplest extraction baseline relabels each training observation with $f(x_i)$ and grows C4.5 on those labels. Ordinary C4.5 in the benchmark instead uses $y_i$. This isolates whether fitting a tree to a smoother teacher decision surface improves on fitting a tree directly to realized outcomes.

C4.5 uses information gain adjusted for split information. For a binary-labeled node $S$, entropy is $H(S)=-p\log_2p-(1-p)\log_2(1-p)$. The gain for a partition is parent entropy minus the sample-size-weighted child entropies. Gain ratio divides this by the entropy of the split proportions, reducing the tendency to favor attributes with many distinct values. The source explains these criteria in equations (16)–(18), but does not report pruning parameters or how all continuous split candidates are generated in this implementation.

Trepan also begins with teacher-relabeled training data, but grows its tree using a best-first expansion queue and can use **M-of-N** tests: a branch is selected when at least $M$ of $N$ listed conditions hold. These are more expressive than a single univariate split. They can represent a complex condition in a small tree, which is why counting leaves alone does not measure the number of atomic conditions a person must process.

At a node with only $m<S_{\min}$ available cases, Trepan generates $S_{\min}-m$ extra inputs satisfying the path's existing constraints, queries the teacher for their labels, and uses the enriched sample to choose a split or leaf label. This addresses the thinning of real observations deep in a tree. The approach is model querying, not acquisition of new default outcomes; synthetic labels add information about the teacher's function, not new empirical information about borrowers.

The article models each input's local marginal distribution separately: empirical frequencies for discrete inputs and a Gaussian kernel density estimate for continuous ones. A normalized version of the intended density is

$$
\widehat p(x)=\frac1m\sum_{j=1}^m
\frac1{\sqrt{2\pi}\sigma}
\exp\left[-\frac{(x-x_j)^2}{2\sigma^2}\right].
$$

The source sets $\sigma=1/\sqrt m$. Equation (19), however, prints the exponent as $-[(x-x_j)/(2\sigma)]^2$ while retaining the standard Gaussian prefactor. Read literally, that density integrates to $\sqrt2$, not one. The normalized expression above is a derived correction to the displayed formula, not evidence that the authors' MATLAB implementation used the erroneous expression. The bandwidth rule also presupposes a meaningful feature scale, but normalization details are not supplied.

Sampling from separate marginal estimates can generate combinations unlike observed borrowers when features are dependent. Path constraints reduce the sampling domain but do not, by themselves, preserve the joint distribution of income, debt, profitability, and balance-sheet ratios. Fidelity measured on unrealistic queries may consume tree complexity without improving decisions on actual applicants. This is a design risk of the described query process, not an empirically measured failure in the paper.

The actual $S_{\min}$, node-priority criterion, M-of-N search bounds, stopping rules, query limits, pruning settings, and random seeds are not reported. Therefore one can reconstruct the extraction architecture and reproduce the metrics, but cannot claim an exact Trepan replication solely from this PDF.

## G-REX and the accuracy-complexity tradeoff

G-REX uses genetic programming to evolve symbolic classifiers. Candidate programs may encode Boolean rules, trees, M-of-N rules, or fuzzy rules. Fitness is described as incorporating fidelity, accuracy, and comprehensibility; roulette-wheel selection chooses programs for reproduction, and crossover and mutation produce new candidates. After a specified number of generations, the highest-fitness program is retained.

The concrete objective weights, complexity measure, program grammar, population size, probabilities of genetic operations, generation count, and stopping conditions are absent. These omissions are particularly consequential because a strong complexity penalty can explain low fidelity even when the teacher is easy to query. The source's illustrative program classifies a customer as Good when income exceeds 3,000 or both age is below 30 and amount below 10,000. This is a diagram explaining the rule language, not a documented estimated lending policy with identified units or out-of-sample performance.

For multiclass problems, the class variable is represented in the genetic program. As with pedagogical C4.5, the training data are relabeled with teacher predictions; unlike Trepan, the experiments do not describe extra synthetic queries for G-REX. Relabeling may simplify contradictory training outcomes but cannot reveal whether the teacher resolves those contradictions correctly. G-REX's flexibility in defining compactness is valuable, yet means its performance depends on an unreported outer objective as well as the quality of the original SVM.

## Experimental protocol and sample definitions

The main experiment repeats a random shuffle and two-thirds training/one-third test split twenty times for each dataset. An RBF SVM is fitted, rules are extracted using the training data and teacher, and the held-out original labels measure accuracy while held-out teacher labels measure fidelity. The same split structure permits paired comparisons among methods. The paper uses paired $t$ tests at 5% relative to the best result and formats nonsignificant alternatives in italics.

These are repeated random splits of the same observations, not twenty independent datasets. Overlap in training and test membership affects interpretation of naive $t$ tests. The article publishes no standard deviations, confidence intervals, exact test statistics, paired predictions, or multiplicity corrections. The hyperparameter tuning partition is insufficiently described to certify that grid selection is isolated from the outer test. These are limits to the precision of the claims; they do not prove test leakage occurred.

The datasets in Table 2 are Ripley, 1,250 observations and two continuous variables; Iris, 150 and four continuous variables; Wisconsin breast cancer, 699 and nine categorical/ordinal variables; Australian credit, 690 and fourteen variables; and Bene-C corporate bankruptcy, 422 and fifteen continuous variables. The Australian table allocates six variables to continuous and eight to categorical, an encoding description that should be verified against the exact file version. The breast-cancer discussion calls its dataset “Diagnostic,” but the tabulated 699 cases and nine attributes identify the particular variant operationally; a replicator should not substitute a differently dimensioned diagnostic file based only on that name.

The exception to the two-thirds split is Ripley: 250 training observations and 1,000 test observations are used for its synthetic overlapping-class problem. Iris has three balanced classes of fifty observations each; the paper does not specify its multiclass SVM construction. These noncredit cases assess extraction behavior, not the economics of credit underwriting.

Bene-C contains unlisted mid-cap companies in Belgium, the Netherlands, and Luxembourg from a major Benelux financial institution. The universe requires book assets exceeding EUR 10 million and turnover below EUR 0.25 billion. It is not a traded-equity or corporate-bond backtest. Exact observation dates, bankruptcy horizon, class balance, raw features, financial-report lags, missing-data exclusions, and repeated-firm identifiers are not supplied in this paper. The Australian feature names are anonymized. There is no chronological validation, default-probability calibration, or lending-loss measurement.

## Numerical results: separate the successful cases from the failures

Table 3 gives these average accuracies in percent. “C4.5 original” learns actual outcomes; “C4.5 extracted” learns the teacher's labels.

| Method | Ripley | Iris | Breast cancer | Australian credit | Bene-C |
|---|---:|---:|---:|---:|---:|
| Logistic regression | 88.0 | 96.4 | 96.1 | 85.7 | 87.0 |
| C4.5 original | 88.0 | 94.5 | 94.6 | 84.2 | 80.2 |
| SVM teacher | 90.3 | 97.0 | 96.3 | 85.7 | 96.5 |
| Trepan | 89.5 | 96.2 | 95.0 | 85.1 | 82.0 |
| C4.5 extracted | 89.1 | 95.1 | 94.4 | 85.1 | 80.2 |
| G-REX | 89.0 | 94.8 | 95.1 | 71.5 | 83.6 |

On Australia, Trepan and extracted C4.5 both reach 85.1%, compared with 85.7% for SVM and logistic regression. Their fidelities are 99.0% and 98.8%, with 2.6 and 2.9 average rules; original C4.5 uses 5.6 rules. This is the strongest credit-specific evidence for a compact approximation at little accuracy cost. G-REX instead produces 71.5% accuracy and 71.5% fidelity with 4.1 rules. Its large loss is not captured by a general statement that all extraction methods preserve performance.

On Bene-C, Trepan has 82.0% accuracy, 84.3% fidelity, and 6.1 rules. Extracted C4.5 has 80.2%, 84.4%, and 16.6 rules. G-REX has 83.6%, 85.1%, and 4.0 rules. G-REX is the best extracted method here, but loses 12.9 percentage points relative to SVM and is 3.4 points below logistic regression. Trepan loses 14.5 points and is 5.0 points below logistic regression. Thus the corporate case supports a substantial simplicity-accuracy tradeoff, not dominance over traditional interpretable models.

For binary Bene-C, the average accuracy and fidelity numbers permit a further approximate decomposition. Trepan's 15.7% disagreement with SVM combines new mistakes where SVM was correct and corrections where SVM was wrong. With error rates 18.0% and 3.5%, the identities imply about 15.1% new mistakes and 0.6% corrected mistakes, subject to the table's rounding. This derived calculation explains why high teacher accuracy makes a fidelity loss expensive. It does not identify which borrower types are harmed.

Ripley fidelities for Trepan, extracted C4.5, and G-REX are 97.5%, 96.5%, and 95.8%, with 7.3, 5.7, and 2.4 rules. Iris fidelities are 97.0%, 96.8%, and 97.2%, with 6.7, 4.3, and 4.0 rules. Breast-cancer fidelities are 97.2%, 96.4%, and 97.0%, with 5.4, 5.2, and 2.2 rules. These cases support useful compression but also illustrate that higher fidelity need not imply higher outcome accuracy and that a smaller rule count can accompany modest performance degradation.

The source's claim that relabeled C4.5 outperforms original C4.5 is not uniform: it is better on Ripley, Iris, and Australia, equal on Bene-C, and slightly worse on breast cancer, 94.4% versus 94.6%. Its claim that SVM performs best is a statement about these point estimates, including a tie with logistic regression on Australia, not a general theorem. Historical SVM+Prototype and Fung results are displayed in the same table but explicitly excluded from the authors' paired comparisons because they come from other experiments.

## What the rule diagrams establish

Figure 6 gives one corporate Trepan tree with 87.9% accuracy and 90.5% fidelity, materially above its twenty-run averages. It uses turnover, return on equity, financial debt payable after one year, solvency ratio, and total assets. Its first split is a one-of-two condition involving turnover at most 0.16 or ROE at most -10.6; later conditions include very small debt thresholds and a two-of-two solvency/assets test. The variable transformations and units are not sufficiently specified to treat these thresholds as usable economic cutoffs. This is one illustrative fitted tree, not the average performance in Table 3.

The Ripley example likewise shows one SVM at 91.4%, logistic at 88.6%, and Trepan at 90.2% with 97.6% fidelity; these are not the table averages. Its diagram makes clear that a sequence of axis-aligned tests approximates a curved SVM boundary by steps. The Iris examples show short petal-dimension rules, but their simplicity on a small botanical classification task does not establish interpretability for high-dimensional credit records.

Rule count is an incomplete proxy for comprehensibility. A single M-of-N rule may contain many comparisons; an ellipsoid rule uses an algebraic form that is harder to explain than a single threshold; long root-to-leaf paths require multiple conditions simultaneously. No user study, expert adjudication, cognitive-cost measurement, stability test across splits, or verification of individual explanations is reported. The source's historical legal motivation is background, not a present-day legal opinion or a demonstration that a surrogate explanation satisfies any regulatory requirement.

## Replication boundary and practical conclusion

To reproduce the architecture, one must train a fixed teacher on each training partition, construct surrogate training labels without using outer test outcomes, constrain synthetic queries to the intended borrower domain, and evaluate both truth accuracy and teacher fidelity on the same held-out observations. A replication should retain query budgets, tree grammar, atomic condition counts, pruning, fitness weights, stochastic seeds, and all selected hyperparameters. The PDF omits enough of these inputs that exact numerical reproduction requires the original software and data preparation beyond the paper.

The evidence does not distinguish whether corporate extraction failure comes from teacher geometry, unrepresentative queries, model-size limits, genetic search, or the credit-data distribution. Nor does it assess rare-event loss, monotone economic constraints, or how extraction performs after a distribution shift. Distilling a frozen model also produces a second object that must be revalidated when the teacher is updated; faithful approximation at one date does not establish future fidelity.

The paper's lasting lesson is to price interpretability empirically: measure the loss of outcome accuracy, agreement, and rule complexity on the actual task. Trepan is promising on the Australian example and several noncredit benchmarks. The corporate example is a clear warning that a compact surrogate can discard much of the teacher's apparent advantage and still be inferior to a direct logistic model.

## Source map and bibliography

Pages 2–3 provide the SVM and extraction taxonomy; pp. 4–6 review decompositional geometry and C4.5; pp. 6–7 specify Trepan and G-REX; pp. 7–9 give the data and illustrative rules; p. 10 contains Table 3 and the principal conclusions; pp. 10–11 give references. The direct antecedents include Craven and Shavlik on Trepan, Johansson and coauthors on genetic rule extraction, Núñez and coauthors on SVM+Prototype, Fung and coauthors on linear-SVM rules, Quinlan on C4.5, and Van Gestel and coauthors on the Bene-C setting. They were not independently read for this note. The fidelity bound, disagreement decomposition, Gaussian normalization correction, and optimization/sign checks above are derived audits of the supplied source.

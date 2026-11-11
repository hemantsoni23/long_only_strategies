# Credit scoring with a data mining approach based on support vector machines

**Cheng-Lung Huang, Mu-Chen Chen, and Chieh-Jen Wang.** *Expert Systems with Applications* 33 (2007), 847–856. DOI 10.1016/j.eswa.2006.07.007. [Source PDF](../../Finance/SVMCreditScoring_Huang2007.pdf). All ten pages, including references, were read; the mathematical specification, search procedures, five tables, and feature-importance figures were checked visually. References below use printed journal pages; PDF page 1 is p. 847.

## Why this matters and what is new

Feature selection and kernel tuning are coupled decisions. Removing an input changes pairwise distances, which changes the meaning of the RBF bandwidth; choosing a different bandwidth changes which feature combinations are useful. Huang, Chen, and Wang compare three ways of addressing this coupling: tune an SVM on all features, screen features with a univariate statistic and retune the SVM, or jointly search feature masks and SVM parameters using a genetic algorithm.

The empirical result is primarily about obtaining compact models without an established loss of accuracy. On two small public credit datasets, the joint genetic search selects about half the available features while remaining competitive with neural networks and genetic programming. It does not establish a statistically significant accuracy improvement over the other SVM strategies. The paper sometimes describes nonsignificant differences as “identical” performance; the evidence supports failure to detect a difference, not statistical equivalence.

The contribution is the comparative credit-scoring workflow and joint representation of features and hyperparameters, not a new SVM loss, kernel, genetic algorithm, or theoretical generalization bound. An individual SVM fit is a convex optimization problem; the outer feature-mask and hyperparameter search is discrete, nonconvex, and heuristic. No global-optimality guarantee for that outer search follows from the convexity of the inner fit.

## The model and its mathematical specification

For labeled observations $(x_i,y_i)$ with $y_i\in\{-1,+1\}$, the soft-margin classifier solves

$$
\min_{w,b,\xi\ge0}\ \frac12\|w\|^2+C\sum_{i=1}^n\xi_i,
\qquad y_i\{\langle w,\phi(x_i)\rangle+b\}\ge1-\xi_i.
$$

Here $C>0$ controls the tradeoff between margin size and hinge-loss violations. The objective does not literally minimize the number of mistakes, despite the source's informal description: a correctly signed observation inside the margin has positive slack, and a severely misclassified observation can incur more than one unit of loss. Equal penalties also mean that the objective does not encode an explicit lending-loss asymmetry.

The dual used by the nonlinear classifier is

$$
\max_{\alpha}\ \sum_i\alpha_i-
\frac12\sum_{i,j}\alpha_i\alpha_jy_iy_jK(x_i,x_j),
\qquad 0\le\alpha_i\le C,\quad \sum_i\alpha_i y_i=0.
$$

The equality follows from the free intercept. With the RBF kernel,

$$
K(x_i,x_j)=\exp[-\gamma\|x_i-x_j\|^2],\qquad \gamma>0,
$$

the fitted sign is

$$
\widehat y(x)=\operatorname{sgn}\left[\sum_i\alpha_i y_iK(x_i,x)+b\right].
$$

For a nonbound support vector, $b=y_i-\sum_j\alpha_jy_jK(x_j,x_i)$; averaging this quantity over nonbound support vectors is a standard implementation option, not an extra procedure specified in the article. Prediction cost depends on the number of retained support vectors as well as the number of selected features, but the paper reports feature counts rather than support-vector counts.

A typographical issue occurs in the hard-margin Lagrangian on p. 849, equation (2). The source writes the subtracted term as $\alpha_i y_i(\langle w,x_i\rangle+b)-1$ inside the summation. The constraint multiplier must instead multiply the whole residual, $\alpha_i[y_i(\langle w,x_i\rangle+b)-1]$, to generate the $\sum_i\alpha_i$ term in the printed dual (3). The displayed dual and subsequent soft-margin objective give the intended conventional formulation. This correction does not affect the reported LIBSVM implementation, whose source code was not supplied with the paper.

## Strategy 1: tune the full-feature SVM

The evaluation has an outer tenfold partition. For each held-out outer fold $k$, let $T_k$ contain the other nine folds. Hyperparameter selection occurs within $T_k$ using fivefold cross-validation. For every candidate $(C,\gamma)$, average the five validation error rates, choose the lowest, refit on all of $T_k$, and evaluate the untouched outer fold. The ten outer accuracies are then averaged.

The printed $\log_2 C$ grid is $\{-5,-4,\ldots,12\}$. The gamma grid is printed $\{-12,-13,\ldots,5\}$, an inconsistent progression: descending from $-12$ to $-13$ cannot continue by that step to $5$. A natural repair is $\{-12,-11,\ldots,5\}$, but it is an inference and should not silently replace the source when claiming exact replication. The paper also permits a finer search around a promising region without specifying its actual bounds or resolution.

Under the inferred 18-by-18 coarse grid, each outer fold entails $324\times5=1,620$ inner SVM fits, and ten folds entail 16,200 fits before final refits or refinement. These counts are derived, not reported timings. They explain why model-selection cost can dominate the cost of one small SVM. They also show why a fair comparison should account for search budgets rather than compare the terminal learner alone.

The outer folds provide test observations not used in each corresponding fit, but the ten fitted models share much of their training data. The fold accuracies are not ten independent samples from ten independent datasets. The paper correctly compares methods on common splits, although its statements about independent holdouts should not be taken to remove dependence induced by overlapping training samples.

## Strategy 2: F-score screening followed by SVM tuning

For feature $j$, define the overall mean $\bar x_j$, class means $\bar x_j^+$ and $\bar x_j^-$, and within-class sample variances $s_{j,+}^2$ and $s_{j,-}^2$. The source's statistic is

$$
F(j)=\frac{(\bar x_j^+-\bar x_j)^2+(\bar x_j^--\bar x_j)^2}
{s_{j,+}^2+s_{j,-}^2},
$$

where each class variance uses its own $n_\pm-1$ denominator. This is a univariate discrimination score, not a multivariate feature-selection objective or the usual ANOVA $F$ test with its associated reference distribution. Its numerator does not explicitly weight the two squared class-mean deviations by their sample counts. Constant features or zero within-class variance require a defined handling rule, which the paper does not give.

Within an outer training sample, the algorithm ranks the inputs and considers subsets containing the first $f=[d/2^i]$ features, for integer $i$ until the size reaches approximately one. It uses fivefold validation to select the number of retained features; inside each such training partition, it invokes the SVM tuning routine. Once the feature count is selected, it repeats training on the larger outer training set and measures accuracy on the outer test fold.

Two distinctions matter. First, the ranking is independent of the fitted SVM, but selection of the rank cutoff uses classifier performance. The article calls the overall procedure a filter; more precisely, it combines a univariate filter ordering with validation of model-dependent subset sizes. Second, a ranking based on marginal mean separation can discard a variable useful only through interaction. For example, two individually uninformative binary coordinates can jointly separate an exclusive-or pattern. RBF flexibility cannot recover an interaction after one of its necessary inputs has been deleted.

The placement of ranking within the nested validation deserves care. The written procedure computes F-scores on $T_k$ before splitting $T_k$ for the feature-count validation. This leaves the outer test protected, but lets inner validation labels influence the ranking used during inner evaluation. An implementation intended to estimate every selection stage without this reuse would recalculate the ranking inside each inner training fold. That is a stricter extension, not a procedure demonstrably used in the source.

The reported feature-count summaries cannot be fully reconstructed from the written coarse size schedule. For Australia, the natural integer sizes from 14 are 14, 7, 3, and 1, whereas the table reports a mean of 7.6 and standard deviation 1.2 over ten folds. Such tightly clustered counts are not explained by that coarse menu. The source does not document a finer feature-count search, alternative rounding, or aggregation convention that resolves this. The empirical table should be preserved as reported; the search specification should be marked incomplete rather than reverse-engineered into an invented protocol.

## Strategy 3: joint genetic search

Each chromosome concatenates binary encodings of $C$ and $\gamma$ with a binary mask $s\in\{0,1\}^d$. A one in the mask selects a feature. Parameter bit strings are decoded to numerical parameter values; the paper says their lengths may be chosen according to required precision but does not report the actual lengths, parameter mapping, or search ranges.

For each outer training sample, the genetic algorithm initializes a population of chromosomes. Each individual is evaluated by fitting the RBF SVM with its selected variables and parameter values across five inner folds. Mean validation accuracy is fitness. Selection, recombination, mutation, and replacement create a new population. The process repeats until a stopping criterion is met; the selected chromosome is then refitted on the full outer training set and tested on the held-out fold. Five independent genetic runs are averaged for each of the ten outer folds to reduce training randomness.

The article does not give the genetic search's population size, crossover/mutation probabilities, number of generations, elitism rule, tie-breaking convention, or exact stopping criterion. Nor does it specify how an empty feature mask is treated. The numerical genetic parameters reported later in the article apply to the separate **genetic programming benchmark**, not to the GA-SVM search. Transferring those settings would fabricate replication details.

The fitness is accuracy alone. No explicit penalty for feature count appears in the published objective. Smaller masks are an observed outcome, not a formally optimized minimum-cardinality solution or a guarantee of sparsity. The search can prefer a larger feature set whenever its estimated accuracy is better. A parsimonious tie-breaker would be a reasonable extension, but is not reported.

Because each fitness calculation is a noisy validation estimate, repeated genetic search can overfit that estimate. Outer evaluation is the relevant protection. Five repetitions do not turn a selected best inner result into an unbiased estimate, and they are not an additional ensemble unless outputs are combined at prediction time; the paper reports averaging performance, not constructing an ensemble classifier. The source also does not make clear whether the same inner folds are reused across chromosomes. Reusing fixed folds would reduce noise in pairwise fitness comparisons, while fresh folds would add randomness to selection.

## Datasets and availability of information

The Australian UCI dataset contains 690 cases, 14 attributes, and two outcomes. The source describes six nominal and eight numeric attributes, including missing values and anonymized category names. It reports 307 creditworthy and 383 noncreditworthy cases. The German numeric credit dataset contains 1,000 cases and 24 numeric inputs, with 700 creditworthy and 300 noncreditworthy applicants. Its fields describe credit history, balances, purpose, amount, employment, age, housing, and related characteristics.

These are static classification benchmarks. The paper supplies no observation dates, chronological train/test split, default performance window, historical release lags, loan balances, recoveries, funding costs, or time-varying approval policies. Its wording sometimes moves between accepted/rejected and good/bad credit. A replication must preserve the actual dataset target rather than assume that an acceptance label is a subsequently observed default event. There is no reject-inference exercise or identification of losses on applicants denied credit.

Preprocessing is materially underdocumented. The Australian file contains missing values and nominal codes, but no imputation rule, one-hot encoding policy, standardization transformation, or training-only preprocessing procedure is specified. Euclidean distances on integer-encoded categories can impose an artificial ordering. RBF bandwidths are inseparable from numerical feature units, so the published $C,\gamma$ strategy is insufficient to recreate a model without the exact transformation pipeline. The manuscript does not publish its final masks or fold-specific selected parameters.

## Results, uncertainty, and the size of the improvement

Tables 2 and 3 report mean hit rates and standard deviations across outer folds. These standard deviations are not confidence intervals for a population accuracy or standard errors of the mean.

| Dataset and strategy | Mean selected features | Feature-count SD | Accuracy, % | Accuracy SD, percentage points |
|---|---:|---:|---:|---:|
| Australian: grid | 14.0 | — | 85.51 | 3.78 |
| Australian: grid + F-score | 7.6 | 1.20 | 84.20 | 4.51 |
| Australian: GA-SVM | 7.3 | 1.65 | 86.90 | 4.22 |
| German: grid | 24.0 | — | 76.00 | 3.86 |
| German: grid + F-score | 20.4 | 5.50 | 77.50 | 4.03 |
| German: GA-SVM | 13.3 | 1.41 | 77.92 | 3.97 |

The genetic method's average reductions relative to the full-feature model are about 47.9% of Australian inputs and 44.6% of German inputs, derived from the reported means. Its accuracy gains over full-feature grid search are 1.39 and 1.92 percentage points. Whether those gains matter economically depends on which class changes and the costs of the changed decisions; no confusion matrices are supplied.

Friedman tests across the three SVM strategies give $p=0.349$ for Australia and $p=0.32$ for Germany. The article interprets this as the same accuracy; a more exact reading is that these comparisons do not reject equal performance. For feature counts, the paired Wilcoxon comparison between F-score and GA gives $p=0.567$ in Australia and $p=0.001$ in Germany. Thus the clearest statistically supported advantage is a smaller German feature subset than the particular F-score procedure, with comparable observed accuracy.

No per-fold prediction files, test statistics, confidence intervals for accuracy differences, or multiplicity adjustment are reported. Paired evaluation is sensible, but inferential precision remains limited because this is one collection of folds on each of two datasets. Common training data create dependence across folds, and repeated genetic runs within a fold should not be treated as new independent customer samples.

## Benchmarks and interpretation

The comparison includes backpropagation neural networks (BPN), genetic programming (GP), and C4.5 trees on the same tenfold splits. Stochastic BPN and GP results are averaged over five training repetitions per partition. Their outputs are thresholded at 0.5 to distinguish good from bad credit. This threshold is a classification convention rather than an estimated economically optimal lending cutoff.

For GP, population size is 250, reproduction probability 0.2, crossover 0.7, mutation 0.08, and the maximum generation count 2,000–3,000. These probabilities total 0.98; the remaining allocation and the reason for the generation range are not explained. The neural architectures selected are 14–32–1 for Australia and 24–43–1 for Germany, with learning rate 0.8 and momentum 0.2. C4.5 uses defaults. The network architecture search and stopping details are not nested explicitly in the reported outer procedure.

| Method | Australian accuracy, % (SD) | German accuracy, % (SD) |
|---|---:|---:|
| BPN | 86.83 (3.86) | 77.83 (3.21) |
| GP | 87.00 (4.03) | 78.10 (4.12) |
| C4.5 | 85.90 (3.47) | 73.60 (3.41) |
| GA-SVM | 86.90 (4.22) | 77.92 (3.97) |

Australian differences across these four methods are not significant in the reported Friedman test, $p=0.37$. For Germany, the authors report no detected difference among SVM, GP, and BPN, and weaker C4.5 performance in a Wilcoxon comparison, $p=0.04$. The description does not fully specify all pairwise tests or adjustments. GP, rather than GA-SVM, has the highest point estimate in both datasets. The absolute margins among the leading three are small.

The feature-size comparisons favor compact GP and SVM models: GP averages 8.2 Australian and 13.2 German features; C4.5 averages 12.2 and 20.3. Feature count alone is not a common measure of interpretability across a genetic program, a tree, a neural network, and an SVM with many support vectors. A seven-input nonlinear decision surface may remain difficult to explain to an applicant even though it uses fewer inputs.

Figures 3 and 4 compare normalized F-scores, neural Garson importance, and frequencies with which GP and GA-SVM select each feature. These quantities measure different things. Selection frequency measures stability across fitted models; a connection-weight diagnostic measures a fitted network's parameter structure; F-score measures marginal class separation. Their percentages are not interchangeable decompositions of predictive performance. Australian feature 8 is prominent under all four displays, especially F-score. Some features unselected by the F-score procedure still appear in the genetic or neural models. Because Australian names are anonymized, the source cannot turn this into an economic narrative about the customer characteristic.

Approximate per-fold Australian runtime is 19.3 minutes for GA-SVM, 15.4 for grid-plus-F-score, 9.5 for GP, and 6.3 for BPN, on a 1.6 GHz Pentium IV with 256 MB RAM. C4.5 is described as much faster. LIBSVM and the benchmark learners use C, grid/F-score routines use Python, and genetic evolution uses MATLAB. The authors explicitly decline a controlled speed comparison because software environments differ. These timings are historical implementation observations, not evidence of present-day hardware cost or algorithmic complexity dominance.

## Replication and limits of the conclusion

A transparent recreation should archive the exact dataset versions and row identifiers, freeze outer folds, and fit missing-value handling, category encoding, and scaling inside training partitions. It should record every inner grid or chromosome evaluation, selected mask, parameter setting, stopping rule, and stochastic seed. The entire selection process belongs inside the outer training sample. These are necessary operational choices where the source does not provide enough information, not claims about the original implementation.

Accuracy is the only optimized and broadly reported predictive criterion. There are no class-specific recalls, ROC curves, calibrated probabilities, expected-loss calculations, net profits, acceptance-rate constraints, or decision costs. A model improving accuracy by approving more of the majority class could worsen credit losses. Conversely, expensive data acquisition could make a smaller feature set valuable without changing classification. The paper measures neither channel, so “future savings” remains an application motivation rather than an observed financial result.

The practical lesson is to evaluate feature and kernel choices jointly, while preserving an outer assessment of the search procedure. The study supports GA-SVM as a competitive way to search a compact predictor set on these samples. It does not establish that genetic search is globally optimal, that SVMs are uniformly superior to simpler models, or that failure to reject an accuracy difference proves equivalence. The missing preprocessing and genetic configuration are the main obstacles to numerical replication; the small static datasets and accuracy-only objective are the main obstacles to a lending-performance conclusion.

## Source map and bibliography

Pages 849–851 contain the SVM, grid, F-score, and genetic procedures; p. 852 contains data descriptions and Tables 1–3; p. 853 contains benchmark settings, Tables 4–5, inference, and runtime; p. 854 contains the importance figures; pp. 855–856 contain references and concluding limitations. The source's direct methodological antecedents include Vapnik (1995), the LIBSVM work of Chang and Lin, Chen and Lin's feature-selection procedures, Goldberg on genetic algorithms, Koza on genetic programming, Quinlan on C4.5, and Garson on network weight interpretation. They were not separately read for this note. Search-cost calculations, normalization distinctions, and identified equation/grid inconsistencies are derived checks of the supplied source.

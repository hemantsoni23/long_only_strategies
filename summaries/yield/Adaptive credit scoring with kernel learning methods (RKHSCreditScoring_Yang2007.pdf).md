# Adaptive credit scoring with kernel learning methods

**Yingxu Yang.** Supplied article-in-press version, *European Journal of Operational Research* (2007), DOI 10.1016/j.ejor.2006.10.066; accepted October 2006. [Source PDF](../../Finance/RKHSCreditScoring_Yang2007.pdf). The source has 16 pages, including an attribute-ranking appendix and references; all were read. Page references below refer to this PDF's printed pages, which coincide with PDF pages. The supplied version does not give final volume or pagination.

## Why this matters

A creditor with few matured loans initially faces two different problems: how to learn a nonlinear decision boundary and how to incorporate later outcomes without rebuilding the optimization from a cold start. Yang proposes a kernel support vector machine whose dual solution is updated as observations arrive, while retaining previous observations that currently have zero multiplier. Retention matters because an observation outside today's margin can become a support vector after the boundary moves. Discarding all such observations would make future optimization depend on an incomplete history.

The paper supplies a useful optimization specification, an incremental control flow, two real lender datasets, and an interpretable class-cost tradeoff. Its principal implementation limitation is unusually explicit: the actual multiplier-update formula is company proprietary and is withheld on p. 5. The assertion that the algorithm always converges without numerical difficulty cannot be independently reproduced or established from the disclosed steps. A conventional convex optimizer can reproduce the stated final optimization problem, but that would be a replacement implementation, not replication of the proprietary algorithm.

The empirical contribution is also narrower than the word “adaptive” can suggest. Data are randomly shuffled before partitioning; online learning adds more observations from that shuffled development sample. There is no chronological experiment, documented population break, forgetting mechanism, or performance test under delayed default labels. The evidence demonstrates useful accumulation of labeled data and reported agreement with batch training, rather than tracking a changing conditional default process.

## Model, loss, and the role of the class penalties

Let $x_i\in\mathbb R^d$ describe applicant $i$, with $y_i=+1$ for Good and $y_i=-1$ for Bad. The paper uses a soft-margin SVM **without an intercept**. In feature space its objective is

$$
\min_{w,\xi\ge0}\ \frac12\|w\|^2+
C_-\sum_{i:y_i=-1}\xi_i+C_+\sum_{i:y_i=+1}\xi_i,
\qquad y_i\langle w,\phi(x_i)\rangle\ge1-\xi_i.
$$

The nonnegativity of the slack variables is required by the usual soft-margin formulation and the displayed dual. It is not explicitly included in the constraint line of the printed equation (3.1). Eliminating the slacks gives a regularized, class-weighted hinge loss. This minimizes a convex surrogate for errors, not the literal number of misclassified customers. An observation correctly classified but inside the margin still contributes to the hinge loss.

With $Q_{ij}=y_i y_jK(x_i,x_j)$, the paper minimizes the dual objective

$$
D(\alpha)=\frac12\alpha'Q\alpha-\mathbf1'\alpha,
\qquad 0\le\alpha_i\le C_{y_i}.
$$

There is no constraint $\sum_i\alpha_i y_i=0$: that constraint would arise from an unpenalized intercept, which this specification omits. Using an ordinary SVM library's default intercept without changing the model therefore need not reproduce the paper. The decision value and classifier are

$$
f(x)=\sum_{i=1}^n\alpha_i y_iK(x_i,x),\qquad \widehat y(x)=\operatorname{sgn}f(x).
$$

A positive-semidefinite kernel makes the dual convex. Strict positive definiteness can ensure uniqueness of the multiplier solution, but is stronger than needed for convexity; duplicate observations can make a Gram matrix singular without making the optimization ill-posed. Different optimal multipliers need not imply different fitted decision functions. The paper's statement about obtaining the same optimal solution should be interpreted with these distinctions in mind.

$C_-$ and $C_+$ govern the training penalty on Bad and Good applicants respectively. They are not estimated default probabilities or a calibrated loss-given-default model. Increasing $C_-/C_+$ can improve detection of bad loans while rejecting more good loans. Since the objective uses sums rather than class-average losses, both class counts and penalty ratios determine the aggregate influence of each class. The second experiment deliberately makes the rare Bad class expensive in the optimization.

## What the incremental procedure discloses

The gradient for coordinate $i$ is

$$
g_i=\frac{\partial D}{\partial\alpha_i}
=(Q\alpha)_i-1=y_if(x_i)-1.
$$

For this box-constrained convex quadratic program, the correct optimality cases are

$$
\alpha_i=0\Rightarrow g_i\ge0,\qquad
0<\alpha_i<C_{y_i}\Rightarrow g_i=0,\qquad
\alpha_i=C_{y_i}\Rightarrow g_i\le0.
$$

Together with feasibility these conditions are necessary and sufficient. The source prints them as biconditionals. That wording is too strong at equality: $g_i=0$ can occur at either endpoint as well as in the interior. An implementation must retain the weak endpoint inequalities and must not force a zero-gradient endpoint into the interior. This is a correction to the printed logical arrows, not a change to the SVM objective.

Initialize a newly appended observation with multiplier zero. If $y_u f_{\mathrm{old}}(x_u)\ge1$, its new-coordinate KKT condition already holds. Since existing multipliers and decision values have not changed, the enlarged solution remains optimal. The new observation is nevertheless stored in the pattern pool. If it violates this condition, its multiplier is increased and old multipliers must be revisited because all gradients can change.

The basic procedure on p. 5 repeatedly updates old and new multipliers until convergence. The faster version on p. 6 scans the full sample for KKT violations, forms a violation set $S_v$, updates its multipliers, concentrates further passes on nonbound observations, and returns to a full scan after those observations satisfy their conditions. The stopping objective is that every historical observation satisfies KKT, not merely the current support vectors. A chunk of new observations can replace a single arrival, although the source leaves chunk-update details unstated.

This is enough to reconstruct the bookkeeping and the optimization target, but not the numerical method. No explicit step length, projection formula, line search, tolerance, maximum iteration count, conditioning treatment, or convergence proof for the proprietary update is supplied. Convexity establishes that a feasible KKT point is globally optimal; it does not establish that an unspecified iterative rule reaches that point. Reported equality of classification results is useful evidence but is weaker than equality of objectives, gradients, and multipliers within a stated tolerance.

For orientation, an independently derived coordinate-descent replacement would update a single coordinate with positive diagonal $Q_{ii}$ as

$$
\alpha_i^{\mathrm{new}}
=\operatorname{clip}\left(\alpha_i-\frac{g_i}{Q_{ii}},0,C_{y_i}\right),
$$

and update cached gradients by the corresponding column of $Q$. This follows by exactly minimizing the one-dimensional quadratic with all other coordinates held fixed. It is not Yang's disclosed update. A complete replacement solver would still need a coordinate-selection policy, robust stopping criteria, memory management, and comparison with a batch reference. Retaining all patterns avoids information loss but causes the potential Gram matrix to grow quadratically with the number of loans; the paper reports no memory or timing benchmarks.

## Kernels, scores, and the attribute diagnostic

The first kernel is Gaussian,

$$
K_{\mathrm{RBF}}(x_i,x_j)=\exp\left[-\frac{\|x_i-x_j\|^2}{2\sigma^2}\right].
$$

The proposed alternative is the fat-tail KGPF kernel, equation (4.2):

$$
K_{\mathrm{KGPF}}(x_i,x_j)=
\frac{1}{a\left(1+\frac{k\|x_i-x_j\|^2}{a}\right)^{1+1/k}}.
$$

The experiment takes $a=16$ and $k=2.001$. The polynomial tail preserves influence over larger distances than the Gaussian. Kernel amplitude also changes: $K(x,x)=1/a$ rather than one. Consequently this is not only a comparison of tail shape with all other effective regularization held fixed. Penalties are retuned as well. A change in kernel scale changes the relation between the norm penalty and empirical loss.

The validity of the KGPF kernel can be checked separately from the proprietary solver. For $a>0$, $k>0$, and $r=1+1/k$, the identity

$$
(1+s)^{-r}=\frac1{\Gamma(r)}\int_0^\infty t^{r-1}e^{-t}e^{-ts}\,dt
$$

represents it as a positive mixture of Gaussian distance kernels with $s=k\|x_i-x_j\|^2/a$, multiplied by $1/a$. Such a mixture is positive semidefinite. This derived justification covers the positive parameters used in the experiment; it does not establish validity for arbitrary negative parameter settings. The term fat-tail refers here to how similarity decays with input distance. It does not mean that a default distribution or loan-loss tail has been estimated.

Kernel amplitude and the penalty are linked. If a kernel is multiplied by a positive constant $s$, the same function class can be written with a feature map multiplied by $\sqrt{s}$. Holding a decision function fixed then divides its squared feature-space norm by $s$. After multiplying the objective by $s$, the model is equivalent to the original kernel with class penalties multiplied by $s$. This is why the KGPF amplitude $1/16$ cannot be ignored when transferring the reported penalties to a normalized kernel implementation.

An additional scaling issue arises as training observations accumulate. With the paper's unnormalized loss sum and fixed $C_\pm$, increasing sample size increases the aggregate empirical-loss weight relative to the norm penalty. Rewriting the objective as a mean loss makes the effective regularization strength proportional to $1/n$ when the class mixture is held fixed. Thus the online trajectory combines information from more observations with a changing effective regularization level. Batch/incremental equivalence remains the correct comparison at a given sample size, but the learning-curve improvement is not an experiment that separately holds average-loss regularization fixed. The source keeps hyperparameters chosen on the initial batch rather than retuning at every expansion.

The interpretation device holds fitted multipliers fixed and removes attribute $h$ from the kernel calculation. If $K_{-h}$ is the resulting kernel, equation (3.8) defines

$$
R(h)=\frac12\sum_{i,j}\alpha_i\alpha_j y_i y_j
\left[K(x_i,x_j)-K_{-h}(x_i,x_j)\right].
$$

This is a change in the quadratic norm term, evaluated at the original multipliers. It is not the difference between two fully retrained optimum objectives, an out-of-sample performance ablation, or an applicant-specific explanation. Correlated variables can redistribute this diagnostic in ways unrelated to their standalone predictive value. Kernel deletion changes pairwise geometry, so the result is also conditional on scaling and bandwidth.

Only nonzero multipliers contribute, reducing calculation to support-vector pairs. Naive computation for $d$ variables and $s$ support vectors is of order $ds^2$ kernel contributions; the source emphasizes linear growth with the number of attributes, not linear total complexity. The appendix reports rankings for 102 anonymized attributes. The leading entries are variable 54 at 9.9947, variable 84 at 9.7024, variable 9 at 7.5284, and variables 100 and 99 at 7.0495, in the displayed $R\%$ column. The smallest is variable 69 at 0.071381. Attribute meanings and the precise percentage normalization are not supplied, so the rankings cannot be converted into economic explanations or reproduced from the paper alone.

The source also rescales decision values into scores and plots quantities called probabilities. Equation (2.3) is originally introduced for a logistic log-odds model, with a points-to-double-odds parameter $M$. A raw SVM margin is not a log odds merely because it is passed through a sigmoid or rescaled. The paper does not report an independently estimated calibration model, reliability curve, Brier score, or log loss. Its probability plots and claim that distance from 0.5 measures confidence should therefore be read as score transformations, not demonstrated probability calibration. The plotted monotone score distributions do not establish calibrated default frequencies.

## First lender: design and results

The first anonymous German lender supplies 5,921 observations, inferred exactly from the reported partition and logistic summary, with 102 attributes and approximately balanced Good/Bad outcomes. The article initially describes this as “about 6000.” Labels are $+1/-1$; all attributes are linearly scaled into $[0,1]$; no feature reduction is applied. The source does not provide lending dates, product definition, default horizon, attribute dictionary, missing-data rules, customer grouping, or the fitted scaling constants.

The dataset is “randomly shuffled 100 times” and divided into development and test samples. The reported matrices imply 4,000 development and 1,921 test observations, rather than an exact two-thirds/one-third split. It is unclear whether 100 shuffles mean repeated permutations before one split or a repeated experiment; the paper supplies one set of integer matrices and no dispersion across splits. Development starts with a 2,000-observation batch and adds the remaining 2,000 incrementally. Hyperparameters are selected by tenfold cross-validation on the initial batch and then fixed for the expanded training sample. The min-max scaling statement precedes splitting and does not establish training-only estimation of the extrema.

With RBF, $\sigma=5.66$ and $C_-=C_+=25$. The unusual confusion-matrix convention places correct cases in the **first column** for both outcome rows. Development is $\left[\begin{smallmatrix}1580&449\\1609&362\end{smallmatrix}\right]$; test is $\left[\begin{smallmatrix}745&208\\783&185\end{smallmatrix}\right]$. Thus the test has 953 Goods and 968 Bads. Define $\alpha$ error as a rejected Good and $\beta$ error as an accepted Bad. They are 21.83% and 19.11%, respectively. Overall test error, derived from the counts, is $393/1921=20.46\%$.

Table 1 reports the progression on the same test sample:

| Training observations | Good error, % | Bad error, % |
|---:|---:|---:|
| 2,000 | 26.15 | 22.46 |
| 2,500 | 25.02 | 21.25 |
| 3,000 | 24.50 | 20.86 |
| 3,500 | 22.39 | 19.45 |
| 4,000 | 21.83 | 19.11 |

This supports improvement as more labeled observations enter this experiment. It does not demonstrate a general monotonicity theorem. Nor is the sequence a time-based backtest: it repeatedly evaluates models trained on larger prefixes of shuffled data. Figures 1–4 show separation and transformed score distributions, but provide no numerical AUC or uncertainty interval.

The stepwise logistic benchmark uses supervised binning and tenfold cross-validation over all 5,921 observations, rather than the kernel model's fixed test split. Its correct counts are 2,238 Goods and 2,065 Bads; errors are 744 and 874. Total error is 27.33%, with class errors 24.95% and 29.74%. This is a materially worse reported result, but the distinct evaluation protocol and missing binning/selection details prevent a clean paired model comparison. Regularized logistic regression, matching class costs, and nonlinear feature construction are not separately benchmarked.

For KGPF, the penalties become $C_-=C_+=20$. Development correct/error counts are 1,641/388 for Goods and 1,588/383 for Bads; test counts are 760/193 and 771/197. Test class errors are approximately 20.25% and 20.35%. Overall error is $390/1921=20.30\%$: only three fewer mistakes than RBF, or about 0.16 percentage points. The class errors are more balanced, but there is no paired disagreement table or significance test. KGPF has about 20% more support vectors, and the ROC is described as almost unchanged. These results establish an operating-point tradeoff and a small aggregate change, not a strong general superiority of the new kernel.

## Second lender: rare defaults and economic loss

The second anonymous lender contributes 27,633 observations and 68 attributes, with about 96.7% Goods and 3.3% Bads. No credit-agency information is available. The same scaling, label coding, and shuffling description is used. Development contains 20,000 observations, initially 4,000 in batch; the holdout contains 7,633. Tenfold selection on the initial batch constrains $C_-/C_+=28$, yielding $\sigma=11.47$, $C_-=56$, and $C_+=2$.

The full-development correct/error counts are 13,455/5,884 for Goods and 493/168 for Bads. On the test sample they are 5,115/2,259 and 182/77. The test therefore contains 7,374 Goods and 259 Bads. Good error is 30.63%, Bad error 29.73%, and total error 30.60%. The relatively low 69.40% accuracy is a consequence of prioritizing rare bad-loan detection; accepting every loan would achieve approximately 96.61% accuracy in this holdout while detecting no Bads.

| Training observations | Good error, % | Bad error, % | Total error, % |
|---:|---:|---:|---:|
| 4,000 | 21.32 | 44.02 | 22.09 |
| 8,000 | 32.00 | 34.90 | 32.08 |
| 12,000 | 31.23 | 32.43 | 31.30 |
| 16,000 | 30.71 | 31.27 | 30.76 |
| 20,000 | 30.63 | 29.73 | 30.60 |

The first expansion improves rare-class detection while sharply worsening majority-class and total accuracy. This directly disproves an interpretation that online accumulation must monotonically reduce every error. It also shows why an economic objective must be stated before calling one result “better.”

Here the logistic benchmark does use the same-size separate test sample. Its Good correct/error counts are 6,672/702 and Bad counts 61/198. Total accuracy is 88.21%; Good recall is 90.48%, but Bad recall only 23.55%, versus 70.27% for the kernel model. The source does not report a logistic threshold or cost adjustment chosen to match the kernel operating point. Comparing different tradeoffs at their default thresholds cannot establish dominance of the whole ROC curve.

A simple loss calculation makes the issue concrete. Let $c_G$ be the cost of rejecting a Good and $c_B$ the cost of accepting a Bad, held constant within each class. Relative to logistic regression, the kernel model rejects 1,557 additional Goods and prevents 121 additional Bad acceptances. It has lower holdout loss precisely when

$$
121c_B>1557c_G,\qquad c_B/c_G>12.87.
$$

This threshold is derived from the reported counts, not estimated or advocated by the paper. Loan sizes, recoveries, interest margins, and application costs would alter the comparison. The training penalty ratio 28 is not automatically this economic cost ratio, because hinge loss and realized lending loss differ.

## Replication boundary and research implications

A faithful replication would preserve the no-intercept objective, exact kernel normalization, class-specific bounds, initial-batch tuning, retained observation pool, and unconventional confusion-matrix convention. It would log batch and incremental dual objectives, projected-gradient residuals, support-vector counts, and predictions under identical hyperparameters. Matching only accuracy would be insufficient evidence of exact optimization equivalence. New outcomes must be incorporated only after their contractual performance window matures; that timing is unspecified in these datasets.

The source withholds the raw data, economic attribute meanings, outcome windows, exact update, software, random seeds, hyperparameter search grids, and convergence tolerances. No test of concept drift, feature availability at application time, repeat borrowers, selection into approved loans, or external validation is reported. Loan-level outcomes among approved applicants do not automatically identify risk among historically rejected applicants; the paper provides no reject-inference design. These omissions prevent a production backtest or an exact algorithmic replication, even though the terminal convex program is clear.

The strongest reusable ideas are retaining inactive observations, checking optimality across the entire accumulated sample, and examining class-specific errors under explicit costs. The kernel and ranking proposals are testable extensions. The empirical results do not establish that linear models cannot be updated, that logistic regression requires linearly separable observations, or that kernel learning removes preprocessing and calibration requirements. Those stronger contrasts in the introductory discussion are motivations rather than mathematical limitations of logistic regression.

## Source map and bibliography

Pages 3–4 specify the objective, dual, and decision function; pp. 5–6 give the proprietary-method disclosure, KKT control flow, and attribute diagnostic. Pages 7–11 give the first lender, Table 1, RBF/KGPF comparison, and Figures 1–8. Pages 12–14 give the second lender, Table 2, logistic benchmark, and Figures 9–12. Page 15 contains the full 102-variable ranking appendix; pp. 15–16 contain references.

The direct antecedents identified by the source include Cortes and Vapnik, “Support-vector networks” (1995); Platt, “Sequential Minimal Optimization” (1998); Cauwenberghs and Poggio, incremental and decremental SVM learning (2000); Guyon and coauthors on kernel feature ranking; and Hosmer and Lemeshow on logistic regression. They supply background rather than new results of this paper and were not separately reviewed here. The coordinate update, weak-KKT correction, exact holdout error calculations, and economic cost threshold above are explicitly derived additions to the source account.

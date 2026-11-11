# Credit rating analysis with support vector machines and neural networks: a market comparative study

**Zan Huang, Hsinchun Chen, Chia-Jung Hsu, Wun-Hwa Chen, and Soushan Wu.** *Decision Support Systems* 37 (2004), 543–558; available online July 4, 2003. DOI 10.1016/S0167-9236(03)00086-1. [Source PDF](../../Finance/CreditScoring_Huang2006.pdf). The filename's 2006 is not the publication year. All sixteen pages, including the literature-review table, references, and author biographies, were read. Model equations, sample tables, confusion matrices, contribution formulas, and Figure 1 were checked visually. Printed page 543 is PDF page 1.

## Why this matters

The paper studies whether public financial statements can reproduce agency credit ratings and whether a fitted model can reveal which financial characteristics drive those ratings. It compares support vector machines with backpropagation neural networks and logistic regression for financial institutions in Taiwan and the United States, then uses neural-network connection weights to compare apparent variable importance across the markets.

Two conclusions must be kept separate. Prediction is approximately 80% accurate in the reported cross-validation exercises, with only modest differences between SVM and neural networks. Interpretation is a claim about a fitted network's weights, not direct evidence of analysts' causal reasoning. The paper's cross-market narratives are plausible descriptions of these particular samples, but the samples differ in institution types, dates, rating scales, class frequencies, and feature availability. The design does not identify a pure market effect.

The contribution is an early multiclass SVM application to bank ratings and a comparative use of connection-weight diagnostics. It does not introduce a new SVM formulation or a new importance measure. Nor does it predict realized default, estimate transition probabilities, or backtest bond trading. Reproducing a rating category is a different objective from identifying mispriced credit or estimating the probability and severity of loss.

## Samples, target labels, and information timing

The Taiwan sample uses Taiwan Ratings Corporation ratings and financial information from the Securities and Futures Institute. Because of availability, the target population is financial organizations. Ratings are matched to financial variables from two quarters before the rating release, taking fiscal-year information into account. The source explains that the rating process commonly takes three to six months and uses this lag as a way to obtain relevant prior financial information while preserving observations.

After removing cases with missing inputs, the sample contains 74 rating cases for 25 financial institutions during 1998–2002. It initially has 21 financial variables. The five categories and counts are twAAA 8, twAA 11, twA 31, twBBB 23, and twBB 1. These are repeated institution observations, not 74 independent banks. Public-release dates of each financial statement are not recorded in the paper, so a two-quarter accounting-period lag is a useful timing convention but not a complete point-in-time data audit.

The United States sample comes from Compustat, selecting commercial banks under the source's identifier DNUM 6021 and using S&P senior debt ratings. It covers 1991–2000 and contains 265 cases from 36 banks after missing-value exclusions. Rating release dates are unavailable, so first-quarter financial variables are matched with the rating results. That convention does not establish an unambiguous forecasting origin. It may be a contemporaneous reconstruction rather than a prospective prediction of an as-yet-unknown rating.

The US counts are AA 20, A 181, BBB 56, BB 7, and B 1. The majority category alone therefore gives $181/265=68.30\%$ exact accuracy; Taiwan's majority twA gives $31/74=41.89\%$. These derived benchmarks show why equal 80% hit rates do not mean equal task difficulty. The US target is highly concentrated in one class, while both markets contain a class represented by a single observation.

The Taiwanese national-scale labels and US S&P categories are not aligned numerically by this design. Taiwan spans twAAA through twBB and the US AA through B. Even aside from national versus broader rating-scale meaning, they have different support and class frequencies. The paper does not provide a common default-risk scale on which to interpret one category as economically equivalent across countries. It also does not supply issuer-versus-issue adjustments, seniority matching, or rating-outlook information sufficient to eliminate target differences.

## Financial inputs and screening

The 21 initial variables combine two balance measures with financial ratios. Table 3 lists total assets (X1), total liabilities (X2), long-term debt to total invested capital (X3), debt ratio (X4), current ratio (X5), EBIT to interest expense (X6), operating profit margin (X7), shareholders' equity plus long-term debt over fixed assets (X8), quick ratio (X9), return on assets (X10), return on equity (X11), operating income over received capital (X12), pretax income over received capital (X13), net profit margin (X14), earnings per share (X15), gross profit margin (X16), nonoperating income over sales (X17), and pretax income over sales (X18).

The cash-flow variables are operating cash flow over current liabilities (X19); a five-year measure of operating cash flow over capital expenditures, inventory increases, and cash dividends (X20); and operating cash flow less cash dividends over fixed assets, other assets, and working capital (X21). These definitions should be preserved as reported. The manuscript does not supply exact Compustat field mappings, currency conversions, accounting adjustments, or handling of zero and negative denominators.

An ANOVA screen on the Taiwan sample removes X5, X9, X17, X19, and X20, with displayed between-class $p$ values 0.36, 0.37, 0.81, 0.84, and 0.64. It retains X3 at 0.12 and X21 at 0.08, so the procedure is not a simple 5% significance rule. Other retained values include 0.01 for ROA, 0.04 for ROE, and 0.02 for gross margin. Entries printed 0.00 mean rounded small values, not probabilities known to be exactly zero.

This leaves 16 Taiwan inputs, including both balance measures. X6 and X21 are unavailable in the US sample, leaving 14 comparable inputs according to the prose. The four initial specifications are:

- TW I: X1, X2, X3, X4, X6, X7.
- TW II: X1, X2, X3, X4, X6, X7, X8, X10, X11, X12, X13, X14, X15, X16, X18, X21.
- US I: X1, X2, X3, X4, X7.
- US II: X1, X2, X3, X4, X7, X8, X10, X11, X12, X13, X14, X15, X16, **X17 as printed**.

The final US II entry conflicts with the earlier removal of X17 and the statement that it uses the Taiwan set minus X6 and X21; that construction would retain X18 instead. This is a visible source inconsistency, not an extraction ambiguity. Exact replication requires resolving which input was actually used; silently substituting X18 would invent a corrected experiment.

The source reports that adding the eliminated variables worsened predictions. That is evidence about selected models on these samples, not proof that those financial ratios contain no information in general. Screening appears before the cross-validation section and is not described as being repeated inside each training fold. If performed once using all cases and their ratings, it lets holdout labels influence the chosen feature list. The same issue applies to market comparison because the initial selection is driven by Taiwan rather than independently controlled in both markets.

## SVM objective, kernels, and multiclass construction

The paper reviews the binary SVM and then uses a multiclass formulation in the experiments. A consistent binary soft-margin specification is

$$
\min_{w,b,\xi\ge0}\ \frac12\|w\|^2+C\sum_i\xi_i,
\qquad y_i\{w'\phi(x_i)+b\}\ge1-\xi_i.
$$

Its dual maximizes $\sum_i\alpha_i-\tfrac12\sum_{i,j}\alpha_i\alpha_jy_iy_jK(x_i,x_j)$ subject to $0\le\alpha_i\le C$ and $\sum_i\alpha_i y_i=0$. The source's primal equations (1) and (3) omit the factor one-half while their corresponding duals retain this standard one-half coefficient. Read literally, those are not the same primal/dual pair. Restoring one-half in the primal makes the conventional normalization consistent; alternatively one must rescale dual variables and penalties. The distinction matters if reproducing a printed $C$ under a new solver.

The hard-margin dual also prints strict positivity for multipliers, whereas zero multipliers are allowed and essential to sparse support-vector representations. The final software-based results should not be interpreted as using an all-positive constraint merely because of that display. These are notation/normalization checks of the exposition, not evidence that the software optimization itself was wrong.

The authors try linear, polynomial, RBF, and sigmoid kernels and alternative multiclass constructions using BSVM. The final selection is described as Crammer–Singer multiclass classification with

$$
K(x_i,x_j)=\exp[-\gamma\|x_i-x_j\|^2],\qquad
\gamma=0.1,\quad C=1000.
$$

A polynomial kernel $(0.1\,x_i'x_j)^3$ is said to give comparable predictions for some specifications. The paper does not publish the search grid, exact model-selection sample, software version, feature normalization, or solver tolerance. Numerical scaling is especially important when total assets and liabilities coexist with ratios: without it, the fixed RBF parameter has no portable meaning.

One usual realization of the named multiclass family uses a score $F_k(x)=w_k'\phi(x)$ for each class and solves

$$
\min_{\{w_k\},\xi\ge0}\ \frac12\sum_k\|w_k\|^2+C\sum_i\xi_i,
\qquad F_{y_i}(x_i)-F_k(x_i)\ge1-\xi_i\quad(k\ne y_i),
$$

with prediction $\arg\max_kF_k(x)$. This is a self-contained reconstruction of the model family, not a displayed equation from the source or verification of the exact BSVM implementation's intercept and scaling conventions. It uses one shared slack per observation for the largest competing-class violation. A nominal multiclass loss treats adjacent and distant wrong categories alike unless an ordinal loss is added; the article does not fit such an ordinal SVM.

The SVM's convexity is conditional on a fixed kernel and hyperparameters. It does not remove sampling error, guarantee generalization, or establish that the selected $C$ is optimal out of time. Nor does a high-dimensional kernel eliminate the need to define feature availability, missingness, and repeated-bank dependence.

## Neural network and validation protocol

The neural benchmark is fully connected with one hidden layer. Inputs are the selected financial variables, and the five rating classes correspond to output nodes. The prescribed number of hidden nodes is $(\text{inputs}+\text{outputs})/2$. This yields half-integers for several specifications, but the rounding convention is not given. The source supplies only a general account of forward propagation, error backpropagation, and gradient-based weight updates.

A generic representation is $h_j(x)=\varphi(a_j+\sum_iw_{ji}x_i)$ and $o_k(x)=\psi(c_k+\sum_jv_{jk}h_j(x))$. The exact activation functions, output normalization, training loss, initialization, learning rate, momentum, epoch limit, stopping rule, and stochastic repetition count are not stated. Thus the architecture family is clear, but a unique numerical network training recipe is not recoverable from the PDF.

The authors report tenfold cross-validation and leave-one-out cross-validation, using 10% of the data as a neural validation set. It is not fully clear how that validation set is nested within each outer training partition. No chronological holdout or bank-grouped partition is described. Leaving one case out can leave other years for the same bank in training; this evaluates interpolation among recurring institutions more than generalization to an entirely unseen bank. Small rating categories also create folds with little or no training representation. In leave-one-out, a singleton class disappears entirely when its sole observation is held out.

The logistic benchmark is named but its ordinal/multinomial formulation, feature scaling, regularization, and convergence handling are unspecified. These omissions matter because conventional logistic regression does not generally require multivariate-normal inputs, contrary to the broad criticism of statistical methods in the literature review. An unfairly restricted or unstable logistic implementation cannot establish a general superiority of machine learning over statistical modeling.

## Exact prediction results

Table 4 gives the following accuracies, all in percent:

| Model | Tenfold logistic | Tenfold SVM | Tenfold NN | LOO logistic | LOO SVM | LOO NN |
|---|---:|---:|---:|---:|---:|---:|
| TW I | 72.97 | 79.73 | 75.68 | 75.68 | 79.73 | 74.32 |
| TW II | 70.27 | 77.03 | 75.68 | 70.27 | 75.68 | 74.32 |
| US I | 76.98 | 78.87 | 80.00 | 75.09 | 80.38 | 80.75 |
| US II | 75.47 | 80.00 | 79.25 | 75.47 | 80.00 | 75.68 |

SVM has the highest point estimate for three of the four feature specifications, but the best overall US number, 80.75%, belongs to the simpler neural model under leave-one-out. Taiwan's best is 79.73% from the simpler SVM specification. The larger feature sets are not systematically better; for Taiwan, they reduce SVM accuracy. US neural performance is also more sensitive to the richer feature set under leave-one-out.

There are no uncertainty intervals, paired significance tests, per-bank errors, macro-averaged recall, or repeated-partition standard deviations. Several differences correspond to very few cases: one Taiwan observation is 1.35 percentage points and one US observation about 0.38 points. The claim of a slight SVM improvement should therefore remain descriptive. Cross-validation accuracy near 80% does not imply that the omitted subjective component of agency judgment is unimportant; correlated public variables can approximate outcomes without identifying all information used to produce them.

## Within-one-class results and source arithmetic problems

Table 5 examines whether neural-network predictions fall within one adjacent rating category. It reports 91.89% for TW I, 93.24% for TW II, 97.74% for US I, and 98.44% for US II. These percentages are reported results, but the printed confusion matrices contain inconsistencies that prevent a clean reconstruction of every entry.

TW I's matrix sums to 74 and reproduces its stated 91.89% within-one-class result: six errors are at least two categories away. The sole twBB observation is predicted twBBB. TW II's displayed twA row sums to 30 rather than the 31 in Table 2, making its matrix total 73 rather than 74. Its printed percentage therefore cannot be treated as verified against the displayed counts.

US I's matrix totals 265 with row counts matching Table 2. Applying the stated adjacent-class criterion to the visible cells gives three errors more than one category away: two BB cases predicted A and the B case predicted BBB. That implies $262/265=98.87\%$, not the printed 97.74%. This is a derived table-arithmetic discrepancy; it does not identify which original entry or summary was mistyped. Its diagonal total is 211, which also does not exactly match the 80.00% tenfold NN figure in Table 4; the source does not clearly identify the exact fit behind each confusion matrix.

US II's last two rows sum to five BB and five B cases, rather than seven and one in Table 2, and the complete displayed matrix sums to 267. It cannot be taken as a confusion matrix for the reported 265-case sample without correction from original records. No guessed correction is imposed here. These issues were confirmed visually and are present in the PDF rather than caused by text extraction.

Even correct within-one-class performance needs a baseline. Always predicting US class A is within one category for AA, A, and BBB, or $257/265=96.98\%$ of this sample. Always predicting Taiwanese twA is within one category for twAA, twA, and twBBB, or $65/74=87.84\%$. These derived comparisons show how a concentrated class distribution can make a high adjacent-class hit rate easy to obtain. The metric also does not distinguish an error across the investment-grade boundary from another one-step error of different economic consequence.

## Refined networks and variable-contribution measures

Before interpretation, the authors perform a stepwise search beginning with TW I and US I: try adding or removing one input, retain changes that improve accuracy, and repeat until no improvement is observed. The resulting TW III uses X1, X2, X3, X4, X6, X7, X8; US III uses X1, X2, X3, X4, X7, X11. Reported tenfold neural accuracies are 77.52% and 81.32%. No independent holdout after this search or uncertainty on the selected model is given. These are optimized cross-validation results, not clean estimates after accounting for all model-search choices.

Let $w_{ji}$ connect input $i$ to hidden unit $j$, and $v_{jk}$ connect that hidden unit to output class $k$. The source uses Garson's nonnegative contribution measure. Define

$$
A_{ik}=\sum_j\frac{|w_{ji}|\,|v_{jk}|}{\sum_r|w_{jr}|},
\qquad G_{ik}=\frac{A_{ik}}{\sum_rA_{rk}}.
$$

For nondegenerate weights, this simplifies to

$$
G_{ik}=\frac{\sum_j|v_{jk}|\left(|w_{ji}|/\sum_r|w_{jr}|\right)}
{\sum_j|v_{jk}|}.
$$

Thus each hidden unit allocates its outgoing weight magnitude among inputs according to their relative incoming magnitudes; outputs then normalize the allocations to sum to one. The measure discards signs. It is not a partial derivative, an out-of-sample feature ablation, or a fraction of explained rating variance. The source does not specify handling for an all-zero incoming hidden-unit vector.

For comparison, the signed Yoon measure in equation (6) is

$$
Y_{ik}=\frac{\sum_jw_{ji}v_{jk}}
{\sum_r\left|\sum_jw_{jr}v_{jk}\right|}.
$$

Its class-dependent signs proved hard for the authors to summarize, so they focus on Garson. Discarding signs produces a simpler display but sacrifices information about whether an input raises or lowers a given class score. With five outputs, raising one class score does not automatically imply a monotone shift in credit quality.

The actual derivative of a one-hidden-layer output includes activation derivatives, schematically $\partial o_k/\partial x_i=\psi'(\cdot)\sum_jv_{jk}\varphi'(\cdot)w_{ji}$. Neither connection-product measure incorporates the input-dependent saturation terms or the empirical distribution of borrowers. Rescaling an input and compensating its incoming weights can leave the fitted function unchanged while changing its relative weight attribution. Correlated assets and liabilities also share information. These properties limit interpretation as an invariant economic decomposition or proof of an analyst's decision rule.

## Cross-market findings and what they can establish

Figure 1 shows different weight patterns for the refined networks. In the US, total assets, total liabilities, long-term debt to invested capital, and operating profit margin receive relatively large contributions; debt ratio and ROE receive less. In Taiwan, operating profit margin, debt ratio, and shareholders' equity plus long-term debt over fixed assets dominate; size measures, long-term debt ratio, and interest coverage are less prominent. The graph provides curves by output category, not a numerical table with standard errors, so exact importance percentages should not be invented from pixel positions.

The authors interpret US ratings as relying more on institution size and Taiwanese ratings more on profitability. They offer sample-distribution evidence: operating profit margins average roughly 30–35% across US rating groups other than B, while Taiwanese group averages range from 3.6% in BBB to 40% in AAA. Every US rating group has an average debt ratio above 90%, whereas no Taiwan group does; Taiwanese AAA averages about 37%. These are reported sample summaries, not adjusted cross-country estimates. Tiny low-rating groups make group statistics especially unstable.

This distributional explanation is important: a variable that scarcely varies across a sample's classes will naturally offer less discriminative information, even if analysts care about it economically. Different weight importance can arise from sample range, accounting definitions, collinearity, and class prevalence rather than different agency preferences. Taiwan includes financial institutions more broadly, while the US selection is commercial banks; national and US rating categories and observation years also differ. The study does not hold those factors fixed.

The authors acknowledge the need for field studies or expert surveys to validate the inferred rating behavior. That is the appropriate status of the interpretation. The result generates hypotheses about market-specific predictors but does not establish that US analysts causally overweight size, that Taiwanese firms generally follow a different leverage policy, or that a trading strategy can exploit those differences.

## Replication requirements and practical use

A faithful reproduction needs the original institution identifiers, dated rating histories, fiscal calendars, source statement vintages, missing-value exclusions, and exact numerical feature transformations. It also requires resolution of US II's X17/X18 conflict and Table 5's inconsistent counts, the precise multiclass BSVM options, neural hidden-size rounding and training controls, validation nesting, and the logistic specification. The paper gives no code or parameter files. Its reported datasets are small enough that such choices can move accuracy by several percentage points.

A prospective extension would split by date and, separately, hold out entire banks, while repeating ANOVA and stepwise selection within training samples. It would report exact and ordinal errors, class recalls, performance relative to majority and persistence baselines, and uncertainty clustered by institution. Such an exercise would answer a different and stronger question than random case-level cross-validation. These are needed design changes for the desired inference, not results attributed to the source.

The paper is useful as a demonstration that a short list of accounting variables can approximate historical bank ratings and that SVMs can be competitive with neural networks. Its strongest caution is methodological: attractive prediction accuracy and visually coherent importance curves do not by themselves reveal the economic rating mechanism. Without time alignment, independent institutions, stable preprocessing, and auditable counts, neither a default forecast nor a cross-market causal conclusion follows.

## Source map and bibliography

Printed pp. 543–548 introduce the target and survey antecedents; pp. 549–550 describe network and SVM families; p. 551 defines the two samples and Table 2; p. 552 gives variables, screening, model lists, and Table 4; p. 553 contains Table 5; p. 554 gives stepwise refinements and contribution equations; p. 555 gives Figure 1 and market comparisons; pp. 556–558 conclude and list references and biographies. Direct antecedents include Vapnik, Cortes and Vapnik, Hsu and Lin, Crammer and Singer, Garson, Yoon and coauthors, and prior rating studies by Kaplan and Urwitz, Moody and Utans, and Maher and Sen. They were not independently read for this note. The multiclass reconstruction, majority/adjacency baselines, formula-normalization checks, and confusion-table arithmetic above are explicit derived analyses of the supplied source.

# The Opportunity Cost of Mean–Variance Choice under Estimation Risk

**Yusif Simaan (2014).** *European Journal of Operational Research* 234, pp. 382–391. Available online 24 January 2013. DOI: 10.1016/j.ejor.2013.01.025.

**Source:** [EstimationError_Simaan_2014.pdf](../../Finance/EstimationError_Simaan_2014.pdf). All ten pages were read, including the tables and concluding limitations; the optimization and opportunity-cost equations and principal tables were checked visually. Printed page numbers are used below.

## Why this matters

If the true return distribution were known, directly maximizing expected utility could not underperform maximizing the same utility over a restricted set of mean–variance-efficient portfolios. With estimated inputs, that ordering need not survive evaluation on new observations. The flexibility that improves sample utility can also increase sensitivity to unusual sample outcomes.

Simaan turns this observation into a paired empirical experiment. For each random split of a historical stock-return panel, one portfolio maximizes sample average utility over the full feasible weight set. Its comparator maximizes the same sample utility over a dense estimated mean–variance frontier. Both portfolios are then evaluated on the unused months. The comparison is expressed as a utility-equivalent monetary opportunity cost rather than a raw utility difference.

The reported result is a reversal: direct utility optimization wins within the estimation sample by construction, while the frontier-restricted choice often wins on held-out months, particularly for highly risk-averse exponential utility and when short positions are permitted. The useful interpretation is regularization through a restricted portfolio menu. The study does not establish that mean–variance optimization dominates correctly specified expected-utility theory, nor does its random split constitute a chronological trading backtest.

## What is novel and what is the comparator

The paper extends earlier comparisons of mean–variance approximations with direct utility maximization in three ways: explicit in-sample versus held-out evaluation; a monetary opportunity-cost metric; and a second constraint regime allowing limited short positions. The comparator is carefully tailored to each utility function. It is not a single risk-aversion coefficient in a quadratic utility objective, a minimum-variance portfolio, or an equally weighted strategy.

For each utility and split, the best mean–variance alternative is selected by evaluating that same utility on each portfolio of the estimated frontier. Thus both procedures use sample utility; the distinction is the set of allowable portfolios searched. Treating the result as a contest between “utility” and “no utility” would miss the experimental design.

The source discusses known circumstances in which mean–variance and expected-utility rankings agree, such as suitable elliptical distributions or quadratic utility. It also observes nonnormality in the stock sample. Rejecting marginal normality does not itself reject all elliptical return models, and the paper acknowledges this distinction. The empirical question is about estimated decisions under the observed sample, not a universal characterization of admissible distributions.

## Data and sampling design

The asset set is the 30 Dow Jones Industrial Average constituents as of 1 March 2012. Table 1 lists AA, AXP, BA, BAC, CAT, CSCO, CVX, DD, DIS, GE, HD, HPQ, IBM, INTC, JNJ, JPM, KFT, KO, MCD, MMM, MRK, MSFT, PFE, PG, T, TRV, UTX, VZ, WMT, and XOM. Historical ticker identities must be preserved rather than replaced with current constituents.

The data are downloaded Yahoo Finance daily adjusted-close prices, converted into 120 monthly returns. There is a source date discrepancy: Section 2.1 says ten years ending in March 2012, while Section 3 and the Table 1 caption explicitly specify January 2002–December 2011. The latter is the more detailed documented window, but exact reproduction requires resolving it against the original data. The paper does not provide the downloaded panel, retrieval timestamp, month-end rule, missing-price treatment, or corporate-action adjustment audit.

Each replication uses 60 distinct months for estimation and the other 60 for evaluation. Footnote 3 supplies the randomization procedure: generate one independent standard-normal sorting key for each of the 120 rows, sort the complete monthly return vectors by those keys, and take the first 60 rows as the estimation set. The remaining rows form its complement. Repeat 1,000 times.

This is sampling without replacement within each split, preserving the contemporaneous dependence among all 30 assets. It is not an ordinary bootstrap with repeated months inside a training sample. Different replications reuse the same historical observations. The method assumes months can be treated as draws from a common time-invariant distribution, and it scrambles chronological order. The concluding section explicitly recognizes the stationarity assumption and notes that the sample includes both quiet periods and the 2008 crisis.

There is no rolling estimation window, forecast lag, live rebalancing schedule, transaction-cost deduction, financing spread, or borrow-cost model. Portfolios are evaluated by their fixed weights applied to individual monthly return vectors. A researcher implementing a chronological strategy would need a different evaluation design and should report it separately from this replication.

## Wealth, utilities, and feasible portfolios

Initial wealth is normalized to one. To remove a notation ambiguity in the source, let $a_t$ denote simple asset returns, $G_t=\mathbf1+a_t$ gross returns, and $w$ portfolio weights satisfying $\mathbf1'w=1$. Terminal wealth in month $t$ is

$$
W_t(w)=w'G_t=1+w'a_t.
$$

The source sometimes calls $R_t$ a return vector while inserting it directly into a utility of terminal wealth. Implementing log or power utility on simple returns would be wrong; the one-plus-return convention must be enforced consistently.

The 14 utilities are log utility $U(W)=\log W$; five power utilities $U(W)=W^c/c$ for $c\in\{0.1,0.3,0.5,0.7,0.9\}$; and eight exponential utilities $U(W)=-e^{-AW}/A$ for $A\in\{1,3,5,7,10,20,50,100\}$. Power utility’s relative risk aversion is $1-c$, while exponential utility’s absolute risk aversion is $A$ and relative risk aversion is $AW$.

The source’s power-utility grid therefore covers relative risk aversion only from 0.1 to 0.9, plus log utility at one. It does not support a conclusion that the entire CRRA class lacks flexibility. Negative power exponents, which would represent relative risk aversion above one, are not tested. The author includes large exponential coefficients as a stress test and discusses their strong emphasis on avoiding low-wealth outcomes.

Two feasible sets are used:

$$
\mathcal W_L=\{w:\mathbf1'w=1,\ 0\leq w_i\leq1\},
$$

$$
\mathcal W_S=\{w:\mathbf1'w=1,\ -0.2\leq w_i\leq0.2\}.
$$

The second allows shorting but also caps each long position at 20%, whereas the first allows a 100% long position. They are not nested feasible sets. Therefore describing the second as a pure expansion of the first, as some source prose does, is imprecise. Observed differences combine permission to short with changed concentration bounds.

Log and power utilities require positive terminal wealth. Under long-only weights and strictly positive gross asset returns this follows directly; with short positions it must be checked across both training and evaluation months. The paper does not state an explicit positivity constraint or how an invalid evaluation wealth observation is handled. Compact weight bounds alone do not resolve a utility-domain failure.

## The two optimization problems

For training rows $\mathcal I$ with $n=60$, direct sample utility maximization is

$$
w^*_{\mathcal I}=\arg\max_{w\in\mathcal W}
\frac1n\sum_{t\in\mathcal I}U(W_t(w)).
$$

For increasing concave utilities on their valid domains, this is a concave maximization problem with linear weight constraints. Numerical issues remain important for exponential utility at $A=100$: evaluating exponentials directly may cause extreme scaling. A stable equivalent minimizes a log-sum-exp expression for the negative exponential objective. This is an implementation recommendation, not an optimizer setting specified by the paper.

The frontier procedure estimates the sample mean vector and covariance from the same training rows. It spans 101 portfolios with equally spaced expected-return targets, from the global minimum-variance portfolio to the feasible maximum-mean endpoint. For target $\mu_j$, solve

$$
w_j=\arg\min_{w\in\mathcal W}w'\hat\Sigma w
\quad\text{subject to}\quad w'\hat\mu=\mu_j,
\qquad j=0,\ldots,100.
$$

The source describes a parametric quadratic program and equal mean spacing; the expression above makes that construction explicit. Each constraint regime gets its own frontier. Finally select

$$
\tilde w_{\mathcal I}=\arg\max_{j=0,\ldots,100}
\frac1n\sum_{t\in\mathcal I}U(W_t(w_j)).
$$

The same frontier can be reused across utilities within a split and constraint regime. The source says discretization causes negligible bias against the frontier strategy but supplies no grid-refinement check. A replication can compare 101 versus a finer grid as a robustness extension; it should not assume the approximation error is known to be negligible for every utility.

The exact utility optimum must weakly dominate every feasible grid portfolio in training utility. A violation is a useful solver or domain diagnostic. It says nothing about the evaluation sample, where the weights remain fixed and utility ordering can reverse.

## Opportunity cost and a consequential formula correction

For either a training or evaluation set $\mathcal E$, the opportunity cost $\theta_{\mathcal E}$ solves

$$
\frac1{|\mathcal E|}\sum_{t\in\mathcal E}U(W_t(w^*)-\theta_{\mathcal E})
=\frac1{|\mathcal E|}\sum_{t\in\mathcal E}U(W_t(\tilde w)).
$$

A positive value is the amount per unit of initial wealth the investor could pay from the direct-utility portfolio’s terminal wealth and still be indifferent to the frontier alternative. A negative value means the direct-utility choice needs compensation to match the alternative. This is an additive wealth adjustment, not a difference in expected returns or a Sharpe ratio.

For exponential utility, algebra gives the exact expression

$$
\theta_{\mathcal E}=\frac1A\log\left[
\frac{\sum_{t\in\mathcal E}e^{-AW_t(\tilde w)}}
{\sum_{t\in\mathcal E}e^{-AW_t(w^*)}}\right].
$$

The printed equation (3), p. 385, omits the factor $1/A$. That omission is visible in the original PDF, not an extraction artifact. The correct factor follows because shifting wealth by $\theta$ multiplies exponential utility by $e^{A\theta}$. The paper’s captions say it uses equation (3), while nearby prose refers to equation (2); the PDF alone does not establish whether the implementation contained the omission. Consequently, the reported cross-$A$ monetary magnitudes should be retained as published and flagged, not silently divided by $A$ or represented as independently reproduced values.

For log and power utilities, solve the scalar indifference equation numerically with a bracket preserving positive shifted wealth. Monotonicity gives a natural one-dimensional root search. The source does not report the solver, tolerances, or treatment of roots near the domain boundary.

## Principal reported results

Table 2 regresses the mean–variance alternative weights on the direct-utility weights, pooling 30 weights across 1,000 splits. Identical choices would give intercept zero, slope one, and $R^2=1$. For log utility, the long-only results are intercept 0.0002, slope 0.9937, and $R^2=0.9958$; under the short-permitted bounds they are 0.0019, 0.9434, and 0.9325. For exponential utility with $A=100$, the corresponding slopes are 0.6385 and 0.6705, with $R^2=0.5603$ and 0.5948. Thus portfolios differ most for the extreme exponential utility cases.

These pooled regressions are descriptive similarity measures. The 30 weights within a portfolio sum to one, and split portfolios share the same underlying data. They should not be treated as 30,000 independent market observations.

The following selections from Tables 3–4 retain reported opportunity costs and held-out p-values. Values are fractions of initial wealth; the source uses monthly utility evaluations, while later prose refers to per-annum magnitudes without documenting an annualization rule.

| Utility | Long-only training θ | Long-only held-out θ | Held-out p | Short-permitted training θ | Short-permitted held-out θ | Held-out p |
|---|---:|---:|---:|---:|---:|---:|
| Log | 0.000027 | −0.000040 | 0.8069 | 0.000670 | −0.000570 | 0.002963 |
| Power c=0.5 | 0.000032 | −0.000027 | 0.8675 | 0.000807 | −0.000511 | 0.007713 |
| Power c=0.9 | 0.000019 | 0.000005 | 0.9765 | 0.000939 | −0.000503 | 0.008695 |
| Exponential A=3 | 0.000006 | −0.000127 | 0.4392 | 0.000339 | −0.000571 | 0.002923 |
| Exponential A=7 | 0.000041 | −0.000343 | 0.0370 | 0.000176 | −0.000676 | 0.000419 |
| Exponential A=10 | 0.000093 | −0.000551 | 0.0008 | 0.000186 | −0.000861 | 0.000007 |
| Exponential A=20 | 0.000493 | −0.001661 | 0.0000 | 0.000563 | −0.002041 | 0.000000 |
| Exponential A=50 | 0.004337 | −0.007402 | 0.0000 | 0.004216 | −0.008181 | 0.000000 |
| Exponential A=100 | 0.011509 | −0.009689 | 0.0000 | 0.011088 | −0.011355 | 0.000000 |

Printed zero p-values denote rounding, not literally zero probability. Under long-only constraints, training opportunity costs are small and not statistically distinguishable from zero for log, tested power utilities, and exponential coefficients through ten. At $A=20,50,100$, training differences are larger and reported significant. Held-out costs are negative except for the tiny positive power-$0.9$ entry; held-out significance begins at $A=7$ for the exponential cases shown.

With shorting permitted, all held-out utility cases have negative reported opportunity costs and p-values below 1%. Training differences are generally larger, but not all are significant: exponential $A=5,7,10$ have training p-values approximately 0.0655, 0.1380, and 0.1166. This qualifies the broad introductory statement that every training case is significant.

For scale, the reported log-utility short-permitted held-out value −0.000570 equals −5.70 basis points of initial wealth under the experiment’s utility-equivalent shift. It should not be called an annual alpha. The extreme exponential values are particularly affected by the unresolved $1/A$ implementation issue.

## Frontier location and concentration

The source ranks the 101 frontier portfolios from zero at minimum variance to 100 at maximum aggressiveness. Table 5 and its accompanying text say the median selected log rank is 59 long-only and 91 with shorts permitted; power medians are around 60–62 and 91–92. Exponential utility covers lower ranks as $A$ increases, reaching reported medians 9 and 19 at $A=100$.

However, Table 5’s percentile ordering is internally impossible as printed. The long-only log row lists a median of 59 but a 75th percentile of 46; similar reversals occur throughout. The prose repeats some median entries, but does not repair the table. These rank values can be described as source claims, not a validated distribution of portfolio aggressiveness. A reproduction should regenerate the ordered percentiles rather than infer a column swap without evidence.

Concentration is measured by squared Euclidean distance from equal weights:

$$
D(w)=\sum_{i=1}^{30}(w_i-1/30)^2.
$$

Table 6 reports differences in this measure, rather than the distance between two portfolio vectors. For log utility, moving from the long-only regime to the short-permitted regime raises average concentration by 0.6169 for frontier portfolios and 0.7314 for direct-utility portfolios. The direct-minus-frontier concentration difference is 0.0060 long-only and 0.1204 with shorts. At $A=100$, the latter differences are 0.0658 and 0.1540. The reported pattern associates direct sample utility optimization with more concentrated choices, especially under the second constraints.

Because the feasible sets differ in both shorting and long-position caps, this comparison does not isolate a causal effect of short sales alone. Moreover, squared distance from equal weights is a weight-dispersion measure; it does not directly measure covariance-adjusted diversification, tail risk, turnover, or gross leverage.

## Mechanism, inference, and replication limits

The author argues that using estimated covariance information helps the frontier procedure extract information more effectively than direct sample utility maximization. A Gaussian example supports the intuition: for exponential utility and Gaussian returns, expected utility is a known function of the mean and variance, so a plug-in estimate can be more structured than the raw average of exponentials.

This explanation should not be read literally as saying empirical average utility ignores covariance information. The full panel of joint return observations contains that information. Restricting the portfolio menu changes how it is used and can reduce overfitting. Nor does using an empirical distribution eliminate every form of specification risk: it still assumes the historical sample is representative, and it imposes a stationarity model through random splitting.

The study reports t-statistics and p-values across resampled outcomes but does not give a complete variance-estimation formula, dependence adjustment, or multiple-comparison treatment. The 1,000 splits do not provide 1,000 independent ten-year histories. Conditional uncertainty from random splitting and uncertainty about the future return-generating process are different objects. The reported significance should therefore be attributed to the study’s procedure rather than treated as established forward-performance confidence.

A faithful replication requires the historical asset panel, a resolution of the sample-date discrepancy, precise return construction, a declared covariance denominator, the 1,000 random sorting seeds, both weight regimes, 101-point frontier construction, utility-domain checks, and verified optimizer solutions. Compute opportunity costs using the explicit indifference equation, and compare corrected CARA calculations with the published formula as a sensitivity analysis. Save per-split weights, training and held-out utilities, opportunity costs, and concentration measures so the aggregate tables can be audited.

Extensions such as chronological validation, block resampling, a changing constituent universe, stronger CRRA preferences, finer frontier grids, transaction costs, and borrowing fees would test robustness. They are not included in the reported experiment. The source also suggests a parametric nonelliptical model and jointly choosing estimation rules with portfolio decisions as future research.

The main finding is evidence that constraining portfolio choice to an estimated mean–variance frontier can help held-out utility when the unrestricted sample optimum is sensitive to estimation noise. Its strongest practical lesson concerns evaluation: in-sample optimality is a mathematical property of a fitted objective, while reliable portfolio choice depends on behavior outside that sample. The historical numerical claims remain conditional on the documented date, inference, table-ordering, and opportunity-cost formula ambiguities.

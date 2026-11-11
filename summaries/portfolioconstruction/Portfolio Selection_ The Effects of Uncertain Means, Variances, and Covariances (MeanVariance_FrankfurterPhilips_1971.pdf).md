# Portfolio Selection: The Effects of Uncertain Means, Variances, and Covariances

George M. Frankfurter, Herbert E. Phillips, and John P. Seagle, *Journal of Financial and Quantitative Analysis* 6(5), December 1971, 1251–1262. JSTOR stable identifier: 2329859.

Source: [MeanVariance_FrankfurterPhilips_1971.pdf](../../Finance/MeanVariance_FrankfurterPhilips_1971.pdf). The basename abbreviates Phillips differently from the printed author name. PDF page 1 is a JSTOR cover; printed page 1251 begins on PDF page 2. The complete paper, numerical tables, and Figure I were inspected.

## Why this matters

An efficient frontier computed from estimated inputs can contain portfolios that are substantially inefficient under the true return distribution. This paper demonstrates the problem in a deliberately favorable environment: only three assets, independent observations, constant parameters, a multivariate normal return distribution, and a small finite grid of feasible portfolios. Neither heavy tails nor changing market regimes are needed for estimation error to corrupt the apparent frontier.

The contribution is a Monte Carlo experiment in which the same simulated sample estimates both expected returns and the entire covariance matrix. The authors know the population parameters by construction, so they can distinguish a portfolio's true efficiency from how often it looks efficient in a finite sample. They also count cases in which a genuinely inferior portfolio appears to dominate a truly efficient one. This moves the question beyond whether individual parameter estimates are unbiased: selection based on those estimates can be unreliable even when the statistical model itself is correct.

The experiment is easy to reimplement because the three means and nine covariance entries are printed. Its most consequential lesson is about evaluation: assess a selected portfolio under the known population or independent validation distribution, rather than using the same estimated frontier as both the selection mechanism and the standard of success. The paper does not propose shrinkage, robust optimization, or a Bayesian replacement. Those would be extensions of the experiment, not methods tested here.

## Population model and portfolio definitions

Let $R_t\in\mathbb R^3$ be the vector of one-period asset returns. The simulation assumes

$$
R_t\overset{\mathrm{iid}}\sim N_3(\mu,\Sigma).
$$

Use column vectors throughout this reconstruction. For portfolio weights $w$, the population mean and variance are

$$
m(w)=w^\top\mu,\qquad v(w)=w^\top\Sigma w.
$$

The feasible set is long-only and fully invested:

$$
\mathcal W=\left\{(a,b,c)/10:\ a,b,c\in\{0,1,\ldots,10\},\ a+b+c=10\right\}.
$$

It contains $\binom{12}{2}=66$ portfolios. There is no risk-free asset, shorting, leverage, transaction cost, turnover constraint, or dynamic rebalancing decision. A weight of 10 in Table 2 means 100% of wealth, not ten times leverage. The grid spacing is ten percentage points of portfolio weight.

Portfolio $u$ dominates $w$ if $m(u)\ge m(w)$ and $v(u)\le v(w)$, with at least one strict inequality. A population-efficient portfolio is one not dominated by any other member of the 66-point grid. This is efficiency relative to the discrete opportunity set; it is not the continuous Markowitz frontier. A grid-efficient point could be dominated by a feasible weight combination omitted from the grid.

For a sample of $n$ return vectors, form $\hat\mu$ and $\hat\Sigma$. The corresponding estimated moments are

$$
\hat m(w)=w^\top\hat\mu,\qquad
\hat v(w)=w^\top\hat\Sigma w.
$$

Applying the same dominance rule to these estimated moments gives the sample-efficient set. The weights themselves are fixed candidates; the moments and the resulting efficient-set membership vary across simulations. This design cleanly isolates statistical errors in assessing a common opportunity set.

## Printed calibration and units

Table 1 on p. 1255 calibrates the artificial normal distribution to three actual securities: Chrysler, N.Y. Shipping, and Bulova, in that order. In percentage-return units,

$$
\mu=\begin{pmatrix}16.64\\6.64\\21.35\end{pmatrix},\qquad
\Sigma=\begin{pmatrix}
2102&-115&1115\\
-115&1664&-37\\
1115&-37&2223
\end{pmatrix}.
$$

The covariance entries are squared percentage-return units. A decimal-return implementation must divide the mean vector by 100 and the covariance matrix by 10,000. Dividing both by 100 would give the wrong risk scale. Table 2 reports portfolio variance multiplied by $10^{-2}$, so a displayed variance of 21.02 corresponds to 2,102 squared percentage points, or 0.2102 in decimal-return variance.

The implied individual standard deviations are approximately 45.85%, 40.79%, and 47.15% per accounting period. These are calculated from the printed covariance diagonal. The paper does not identify the dates, observation frequency, return construction, or number of observations used to obtain this original calibration. Its simulation periods are described as accounting periods. They should not silently be called months or years.

The three-asset covariance is positive definite. An independent check using the printed entries gives eigenvalues approximately 1,040.41, 1,662.52, and 3,286.07 in squared percentage-return units. This supports direct Cholesky simulation. The third covariance row is mislabeled as another row for security 2 in Table 1, but symmetry, its position, and the diagonal establish that it is the row for security 3.

There is a small numerical inconsistency between the tables: Table 1 gives Bulova variance 2,223, while Table 2's all-Bulova portfolio displays 22.22 rather than the 22.23 implied after scaling. A reproduction should choose and document an authoritative input table. The calculations in this note use Table 1 exactly. They recover the complete published list of 21 grid-efficient portfolio identifiers, so this discrepancy does not change that membership check.

The published efficient identifiers, after sorting all 66 candidates in decreasing true mean, are

$$
1,2,3,4,6,7,9,11,14,15,18,21,25,26,29,32,35,39,41,47,49.
$$

The maximum-mean candidate is portfolio 1, all Bulova, with mean 21.35%. Portfolio 49, weights $(0.3,0.5,0.2)$, is the minimum-variance grid portfolio: mean 12.582% and variance 786 squared percentage points, displayed as 12.58 and 7.86 in Table 2. Portfolio 23, all Chrysler, has mean 16.64% and variance 2,102. It is well inside the inefficient region. These provide useful unit and enumeration tests before any random draws are generated.

## Generating correlated return samples

Section II, pp. 1254–1255, constructs normal returns sequentially from conditional regression distributions. First draw

$$
R_1=\mu_1+\varepsilon_1,\qquad
\varepsilon_1\sim N(0,\Sigma_{11}).
$$

Conditional on $R_1$, draw

$$
R_2=\mu_2+\frac{\Sigma_{21}}{\Sigma_{11}}(R_1-\mu_1)+\varepsilon_{2\mid1},
$$

where the new independent innovation has variance

$$
\operatorname{Var}(\varepsilon_{2\mid1})
=\Sigma_{22}-\frac{\Sigma_{21}^2}{\Sigma_{11}}.
$$

Continue with asset 3 conditional on the first two. In general, if $A=\{1,\ldots,j-1\}$,

$$
R_j=\mu_j+\Sigma_{jA}\Sigma_{AA}^{-1}(R_A-\mu_A)+\varepsilon_{j\mid A},
$$

$$
\operatorname{Var}(\varepsilon_{j\mid A})
=\Sigma_{jj}-\Sigma_{jA}\Sigma_{AA}^{-1}\Sigma_{Aj}.
$$

This general conditional formula completes the paper's explicitly illustrated two-asset construction. Use independent innovations at each stage and independent return vectors across periods. The ordering of assets changes the regression representation but not the joint normal distribution.

An equivalent contemporary implementation factors $\Sigma=LL^\top$, draws $z_t\sim N_3(0,I)$, and sets $R_t=\mu+Lz_t$. Equivalence here is distributional, not a claim to recreate the authors' random-number stream. The paper supplies neither a seed nor a random-number generator specification.

The normal model can produce returns below $-100\%$ under this high-volatility calibration. The original experiment uses the untruncated normal distribution. Truncating, censoring, or replacing it by a lognormal distribution would change the population moments and the experiment. This is one reason the study should be understood as a controlled statistical exercise rather than a complete economic model of limited-liability equity returns.

## Simulation and evaluation protocol

The four sample sizes are $n\in\{5,10,25,50\}$. For each size, the authors generate 100 trial groups of $n$ independent three-asset observations. Each group represents all the information available to a hypothetical analyst. The same observations estimate the three means and the covariance matrix; the paper calls the estimation procedure standard correlation methods without providing exact code or a divisor convention.

A reproducible modern specification is the sample mean and covariance

$$
\hat\mu=\frac1n\sum_{t=1}^nR_t,\qquad
\hat\Sigma=\frac1{n-1}\sum_{t=1}^n(R_t-\hat\mu)(R_t-\hat\mu)^\top.
$$

The divisor $n-1$ is an explicit reconstruction choice. Replacing it by $n$ multiplies every candidate's variance within a trial by the same positive constant, so it does not change within-trial dominance or efficient-set membership. It would change the reported numerical estimated variances, but those are not the frequency endpoints here.

For each trial, calculate all 66 estimated moment pairs and determine which are nondominated. Record one indicator per candidate for membership in the sample frontier. Average those indicators over 100 trials. The denominator is trials, not the total number of points appearing on all frontiers. Several portfolios can be efficient in the same trial, so membership percentages across candidates need not sum to 100%.

Figure I, p. 1257, plots those membership frequencies at each candidate's *true* mean and variance, rounded to the figure's grid. This placement is deliberate: it shows how often portfolios at good or bad population locations are misclassified as efficient. It is not a plot of estimated frontiers averaged across simulations. Where several distinct portfolios round to one plot location, the figure displays the frequency that one or more of them is efficient. That union-event convention can produce a larger figure label than any one candidate's frequency and must be replicated when comparing individual plotted cells.

Table 3 adds a stricter pairwise endpoint for $n=5$. For each truly efficient column portfolio $B$ and row portfolio $A$, it counts trials in which $A$ lies on the sample frontier and also sample-dominates $B$:

$$
I_{A,B}=\mathbf1\{A\in\widehat{\mathcal F},\
\hat m(A)\ge\hat m(B),\ 
\hat v(A)\le\hat v(B),\ 
[\hat m(A)>\hat m(B)\ \text{or}\ \hat v(A)<\hat v(B)]\}.
$$

The sample-frontier condition for $A$ is part of the table definition. Counting all pairwise estimated dominance events, including dominance by a portfolio itself dominated by a third candidate, would not reproduce Table 3. Row and column events also overlap, so adding table entries does not give a probability that a selected investor loses.

## Principal findings and their interpretation

The authors divide true mean–variance space into three visual regions. Region I contains points close to or on the true efficient frontier, Region III contains markedly inferior portfolios, and Region II lies between them. These regions are descriptive partitions in Figure I, not a formal utility-loss classification or a universal statistical threshold.

The most visible example is all Chrysler, portfolio 23. The circled point has rounded true coordinates mean 17% and scaled variance 21. It appears efficient in 42 of 100 five-period samples. Figure I reports corresponding frequencies of 40%, 34%, and 25% for 10, 25, and 50 periods. More observations help, but even with 50 independent observations this substantially inefficient candidate frequently reaches the estimated frontier.

The maximum-mean portfolio, all Bulova, appears efficient in 42%, 46%, 57%, and 70% of the trials as sample size rises. Thus a genuinely efficient endpoint is often omitted in short samples while a genuinely inefficient concentrated position is included. These are two sides of the same estimation problem; reporting only erroneous inclusions would miss uncertainty about the supposedly reliable part of the frontier.

Table 3 shows that the damage is not confined to a particular investor's risk tolerance. In five-period samples, portfolio 23 appears on the estimated frontier and sample-dominates true-efficient portfolio 1 in 24% of trials, portfolio 2 in 23%, and portfolio 49 in 4%. The latter is the true minimum-variance grid portfolio. The different percentages reflect different true mean–variance separations and different estimation errors; they do not imply that one fixed investor would choose Chrysler at those exact rates.

The paper says that, for five-period samples, the average membership frequency of inferior Region III portfolios exceeds that of Region I portfolios. Because Figure I aggregates multiple candidates at some rounded locations, this statement cannot be checked by taking an unweighted mean of all printed labels in each region. The underlying portfolio indicators are the correct objects. The article does not publish a separate table of every individual membership rate and region assignment in machine-readable form.

The proposed mechanism is selection on noisy estimates. Concentrated, volatile positions have imprecisely estimated means and risks. Some samples give them unusually attractive estimated mean–variance combinations, so they enter the estimated frontier even though their population position is poor. For a fixed portfolio under this iid model,

$$
\operatorname{Var}[\hat m(w)]=\frac{v(w)}n.
$$

An independently derived illustration using the printed inputs gives the standard error of Chrysler's estimated mean as about 20.50 percentage points at $n=5$ and 6.48 percentage points at $n=50$. Those uncertainties are large relative to several of the population mean differences in Table 2. This helps explain why increasing sample length improves but does not immediately stabilize classification.

For the normal model, sample mean and sample covariance are statistically independent. Using the same sample does not overturn that normal-theory fact. The paper's joint treatment means that both sets of inputs are estimated and both contribute to the frontier error, rather than assuming one set known. Across portfolio candidates the estimation errors are strongly related because all candidates use the same three assets. A reconstruction should not generate an independent estimated mean and risk for each of the 66 portfolios; doing so would destroy those relationships.

## Monte Carlo uncertainty and an independent check

The published frequencies are based on 100 trials per sample size. For a single portfolio's membership event with probability $p$, the conventional Monte Carlo standard error of its frequency is approximately

$$
\sqrt{\frac{p(1-p)}{100}}.
$$

This is 3 percentage points at $p=0.1$ and 5 percentage points at $p=0.5$. Page 1259 states 3 and 10 percentage points, respectively, calling both standard deviations. The second number does not match the usual binomial standard-error formula for 100 independent trials; 10 percentage points is closer to a two-standard-error width near $p=0.5$. This discrepancy should not be propagated as an exact uncertainty calculation.

To check the mechanism independently, this note's preparation included a new simulation using the printed Table 1 inputs, the 66-weight grid, Cholesky normal draws, sample covariance divisor $n-1$, NumPy's PCG64 generator seeded with 1971, and 10,000 trials per sample size in the order 5, 10, 25, 50. These are newly calculated validation results, not the authors' original draws:

| Sample periods | Published Chrysler frontier frequency | Independent reconstruction |
|---|---:|---:|
| 5 | 42% | 35.13% |
| 10 | 40% | 31.81% |
| 25 | 34% | 28.04% |
| 50 | 25% | 21.76% |

The new run confirms frequent false inclusion and improvement with more data, but it does not exactly reproduce the printed percentages. The original random stream and any unreported input precision are unavailable. Differences of this scale must be considered against Monte Carlo variability from the original 100-trial experiment; the comparison is a mechanism check, not a certification that every original table entry has been recreated.

The same reconstruction recovers exactly the 21 true-efficient identifiers listed above. At $n=5$, the average membership frequency across those 21 portfolios is about 20.60%, compared with 20.52% across the other 45. At $n=50$, the averages are about 49.54% and 17.95%. These groups are true-frontier versus off-frontier, which differ from the source's broader visual Regions I and III. They should not be used as a numerical reproduction of its Region I/III comparison.

## What the experiment establishes, and what it leaves open

The clean result is that treating estimated moments as known can produce a very misleading efficient set, even in a small correctly specified stationary normal model. Because the population inputs are fixed and known to the experimenter, this conclusion does not depend on choosing an ex post market regime or disputing a realized return benchmark. It is a direct demonstration of finite-sample classification error.

The paper's broader conclusion is more tentative. It asks whether mean–variance-selected portfolios are any more likely to be truly efficient than randomly selected portfolios under realistic conditions and suggests a pessimistic answer. However, it does not specify a complete random-portfolio selection distribution, a risk-preference rule for selecting one point from each estimated frontier, and a common scalar welfare or return-risk loss for a head-to-head strategy comparison. Frontier-membership errors alone do not establish that every optimization procedure performs worse than every random allocation rule.

The experiment likewise does not quantify the benefits of a particular correction. There are no covariance-shrinkage baselines, return-shrinkage baselines, robust sets, Bayesian posterior allocation policies, or equal-weight performance comparisons. One can add them to the same known-population design, but any improvement would be a new finding. The source's contribution is diagnosis of a neglected problem rather than validation of a remedy.

The authors argue that time variation and judgmental forecasts would magnify estimation problems. That is a plausible concern, but a blanket monotonic deterioration is not established by their stationary simulation. Additional information can sometimes improve estimates, and different nonnormal or dependent processes affect different inputs differently. A careful application should test the intended departures explicitly rather than treating them as a proved extension.

Nor is the number 50 a universal minimum data requirement. It is one sample length in one three-asset calibration with large return variances. Changing mean separation, correlations, weight constraints, dimensionality, or loss function changes the difficulty. The experiment contains four observation counts but no broad sensitivity grid over those economic parameters.

## A reimplementation that preserves the question

Begin with deterministic checks: validate the covariance matrix, enumerate 66 fully invested long-only grid points, recover their means and variances, and identify the 21 true-efficient points. Only then generate independent samples for the four prescribed lengths. Within each trial estimate all moments from the same observations, compute sample efficiency without rounding, and accumulate individual frontier indicators and the Table 3 conditional dominance indicators.

Round coordinates only when constructing the Figure I display. Preserve individual event records so that overlapping cells can be combined as union events rather than by addition. Label variance in the table's scaled units and mean return in percent. Report the random generator, seed, number of trials, and covariance convention. Use the printed input precision if reconstructing this paper; retain a separate record if substituting higher-precision or newly estimated data.

For a replication of the published experiment, no estimation window rolls through real time, no portfolio is held for a subsequent observed period, and no rebalancing occurs. The true population moments evaluate candidate quality directly. A later out-of-sample investment study should be described as a distinct design with its own timing, costs, and validation sample.

The practical takeaway is to keep optimization error and input uncertainty visible together. A calculated frontier is conditional on estimates. In this paper's experiment, moving from that conditional object to the true opportunity set changes the status of many portfolios, including concentrated positions that appear attractive remarkably often. The printed inputs and finite grid make that warning reproducible without requiring a large modern backtest.

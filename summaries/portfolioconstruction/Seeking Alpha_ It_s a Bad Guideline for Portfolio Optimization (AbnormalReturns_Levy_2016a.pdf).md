# Seeking Alpha? It's a Bad Guideline for Portfolio Optimization

Moshe Levy and Richard Roll, The Journal of Portfolio Management 42(5), special issue 2016, pp. 107–112. Source: [AbnormalReturns_Levy_2016a.pdf](../../Finance/AbnormalReturns_Levy_2016a.pdf), six pages. This is a fixed-moment numerical portfolio exercise illustrating local versus finite optimization, not an out-of-sample stock-selection test.

## Why this matters and the innovative claim

An asset's alpha relative to the current portfolio is proportional to the derivative of that portfolio's Sharpe ratio with respect to its risky-asset weight. It therefore identifies a locally improving direction. The paper shows that taking a finite step along the original alpha vector can be substantially inferior to optimizing the complete portfolio at the same distance from the benchmark. Some assets with positive initial alpha optimally receive smaller weights, and vice versa.

The distinction is between using alpha as a gradient at a point and treating a fixed gradient as a whole optimization algorithm. This result does not invalidate alpha as every possible performance statistic or show that an optimizer should ignore expected returns. The exercise explicitly holds the estimated means and covariances fixed as if they were the true inputs so that estimation error does not obscure the geometric comparison.

## Notation and derivation

Let $x\in\mathbb R^N$ be risky weights, $\mu$ their expected returns, $\Sigma$ their covariance matrix, and $r_f$ a deterministic risk-free return over the same period. The residual risk-free weight is $1-\mathbf1^\top x$. Write $e=\mu-r_f\mathbf1$, portfolio excess mean $m=x^\top e$, and volatility $\sigma=(x^\top\Sigma x)^{1/2}$. The Sharpe ratio is

$
S(x)=\frac{x^\top e}{(x^\top\Sigma x)^{1/2}}.
$

Asset $i$ has beta to this portfolio and corresponding alpha

$
\beta_i(x)=\frac{(\Sigma x)_i}{\sigma^2},\qquad
\alpha_i(x)=e_i-\beta_i(x)m.
$

Equations (1)–(3), printed p. 108, yield

$
\frac{\partial S(x)}{\partial x_i}=\frac{e_i}{\sigma}-\frac{m(\Sigma x)_i}{\sigma^3}
=\frac{\alpha_i(x)}{\sigma}.
$

The quotient rule and derivative of quadratic variance produce this result. Increasing a risky weight is financed through the risk-free holding in this parametrization. The alpha vector is the steepest-ascent direction under an unconstrained Euclidean metric in risky-weight space. With additional binding constraints, the feasible local direction would instead require projection or constrained optimization; the unrestricted statement should not be transferred unchanged to every mandate.

For a displacement $h$, the first-order approximation is

$
S(x+h)=S(x)+\frac{\alpha(x)^\top h}{\sigma(x)}+O(\|h\|^2).
$

The remainder is the reason finite steps can behave differently. This Taylor expression is a concise reconstruction of the paper's local argument. After weights move, the portfolio mean, volatility, covariances to assets, betas, and alphas change even though $\mu$ and $\Sigma$ are held fixed. Maintaining the initial direction does not follow the changing gradient.

## Dataset and fixed-input experimental design

The benchmark is value weighted across the 100 largest US stocks as of December 31, 2014 that have return records over the preceding decade. Monthly observations from January 1, 2005 through December 31, 2014 supply sample means and covariances. The risk-free input is the period's average monthly Treasury-bill rate, 0.11%.

These estimates are treated as known population inputs for the comparison. The stock selection uses end-of-period size and a full-history requirement. Consequently this is not a historically investable universe selected at the beginning of 2005, and the exercise should not be presented as an unbiased forecast backtest. Its goal is to compare two mathematical transformations of the same inputs.

The source does not provide a stock-identifier list, return database, handling of distributions and corporate actions, exact sample-covariance convention, or benchmark market-cap weights. These omissions prevent bit-for-bit numerical replication from the article alone. Monthly means and covariances must retain consistent units; using annualized means with monthly covariance would change alpha magnitudes and the mapping from a step parameter to portfolio distance.

Let $x^B$ denote benchmark weights. The alpha-direction candidate before normalization is

$
x_i=x_i^B+a\alpha_i(x^B),\qquad a>0.
$

The paper defines distance by root mean square weight displacement:

$
D(x,x^B)=\sqrt{\frac{1}{N}\sum_{i=1}^N(x_i-x_i^B)^2}.
$

Thus $D=0.02$ is a two-percentage-point RMS displacement, not a maximum holding deviation, a two-percent relative change in each holding, or an average absolute deviation. With $N=100$, the corresponding Euclidean norm is $0.20$. That scale matters when judging the description of these adjustments as small.

Footnote 5 says the adjusted weights are normalized to sum to one because raw alphas need not sum to zero. Positive scaling of the risky portfolio leaves the Sharpe ratio unchanged when risk-free financing is accounted for consistently. However, scaling generally changes the distance from a fixed benchmark. Therefore a reproduction must compute the reported distance on the actual normalized candidate, rather than assume $D=a\|\alpha\|/\sqrt N$ without checking the normalization. The article does not provide the implementation code resolving this detail.

## Optimization comparator

For each allowed distance, the comparator directly maximizes the same Sharpe objective under a constraint on deviation from the benchmark. A natural mathematical reconstruction is

$
\max_x S(x)\quad\text{subject to}\quad D(x,x^B)\leq d,
$

with the same budget/normalization convention used for the candidate portfolios. The source reports numerical constrained optimization in Matlab, with the routine name printed as fmincom. It gives no solver tolerances, initialization protocol, convergence certificates, or complete list of position bounds. In particular, long-only or leverage limits should not be invented from the positive benchmark weights. Those details must be recovered from code or specified transparently in a reproduction.

An inequality distance constraint is the usual interpretation of an allowed deviation. The text also describes comparisons at the same distance, without a full mathematical constraint listing. If the solution is interior or normalization modifies the path, equality versus inequality can matter. The article's central geometric point survives, but exact plotted curves need the original numerical choices.

A defensible reconstruction would first verify the analytic gradient numerically at the benchmark, then generate the normalized fixed-alpha path and its actual distances, and solve the constrained problem at those distances with several starting points. Recomputing alpha after every small step would test a different algorithm. It should not be substituted for the published fixed-initial-alpha path while claiming to reproduce the same experiment.

## Reported results

Exhibit 1, p. 109, shows the two curves agreeing for very small displacements and separating noticeably beyond approximately $D=0.01$. At $D=0.02$, the authors report that the fixed-alpha portfolio's Sharpe ratio is about 30% below the optimized comparator. This is a relative difference between Sharpe-ratio levels, not a 30-percentage-point investment loss or a claim of 30% higher future return.

The alpha-path Sharpe ratio initially rises, peaks, and then declines as the step extends. In contrast, the optimized curve in the displayed range continues upward. The later alpha-path decline is consistent with the original direction becoming a poor direction after the portfolio changes. Values read approximately from a graph should not be treated as a numerical dataset; the article does not tabulate the complete frontier.

Exhibit 2 counts assets whose optimal change has the opposite sign to their initial alpha. At $D=0.02$ the text reports about 15% of assets. In formal terms this is the fraction with $\alpha_i(x^B)(x_i^*-x_i^B)<0$, excluding any exact-zero convention that would need code clarification. The fraction rises toward roughly one third at larger displayed distances. It measures disagreement with the globally chosen portfolio displacement, not the probability that an individual alpha estimate is statistically wrong.

Exhibit 3 at $D=0.04$ scatters initial alphas against optimal weight adjustments. The weak relationship illustrates that a component's best finite change depends on the joint covariance structure and all other holdings. Exhibit 4 compares initial alpha with alpha recalculated relative to portfolios on the alpha path. At $D=0.01$ the relation remains fairly close; at $D=0.02$ it is much weaker. No correlation coefficients, standard errors, or hypothesis-test statistics are provided for those visual statements.

The authors say similar patterns occur for other assets, sample periods, and universe sizes, but do not give full specifications or numerical robustness tables. The gradient's local nature is mathematical; the exact 1% threshold, 30% gap, and 15% disagreement are properties of the reported example, not universal constants proved by the derivative identity.

## Limits and practical use

No estimation uncertainty, transaction costs, market impact, turnover budget, forecast validation, or investor-specific utility is modeled. Direct sample optimization can be unstable out of sample even when it dominates a fixed-gradient path under the supplied moments. The paper deliberately separates that issue rather than resolving it. Neither curve establishes an attainable future Sharpe ratio.

The useful implementation lesson is to optimize the portfolio objective and actual constraints jointly. If alpha is used as an iterative signal, recognize that its reference portfolio and hence its gradient meaning change as holdings move. Under a binding mandate, covariance penalties, active-risk budgets, and feasibility also affect direction. This broader lesson follows from the demonstrated local-versus-finite distinction; it is not evidence that the authors tested every constrained optimizer or every definition of active management.

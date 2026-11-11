# Risk-Constrained Kelly Gambling

Enzo Busseti, Ernest K. Ryu, and Stephen Boyd, manuscript dated March 19, 2016. Source: [UniversalPortfolios_BussetiBoyd_1916.pdf](../../Finance/UniversalPortfolios_BussetiBoyd_1916.pdf). The historical filename contains a year typo and omits Ryu; this note concerns the supplied 28-page 2016 manuscript. The complete text, both appendices, and numerical figures were read. Page and equation references refer to that version.

## Why this matters

Kelly optimization maximizes long-run log wealth, but it does not directly control the chance of a large early loss. Fractional Kelly reduces all risky exposures by the same factor, preserving their relative proportions. Busseti, Ryu, and Boyd instead optimize the composition of the risky allocation subject to a tractable sufficient condition for limiting the probability that wealth ever falls below a specified fraction of its initial value.

The main contribution is the constraint $\mathbb E(r^Tb)^{-\lambda}\le1$. It is convex in portfolio weights and implies an infinite-horizon bound on the distribution of minimum wealth. The authors combine it with the usual concave Kelly objective, derive deterministic and stochastic solution methods, and relate a second-order approximation to mean–variance optimization. The guarantee belongs to the exact inverse-moment constraint under the assumed return law. It does not automatically carry over to the quadratic approximation, an estimated law, or a finite-sample numerical solution.

The term drawdown is narrower here than in many portfolio mandates. The reference is initial wealth, fixed at one. It is not the running high-water mark. A portfolio could grow from one to ten and then fall to two without violating an initial-wealth floor of 0.7, despite an 80% peak-to-trough decline. This distinction is fundamental when deciding whether the model matches a risk limit.

The numerical evidence is synthetic. In a finite-outcome example, changing composition delivers appreciably more growth than merely scaling Kelly exposure. In the mixture-of-lognormals example, risk-constrained and fractional Kelly perform essentially alike. The paper therefore supports the usefulness of a direct optimization framework, not a universal empirical dominance claim for every return distribution.

## Market model and growth objective

There are $n$ nonnegative gross-return assets or bets. Their vector is $r\in\mathbb R_+^n$, with $\mathbb Er_i<\infty$. The last asset is cash, $r_n=1$ almost surely. A constant portfolio fraction vector satisfies

$$
b\ge0,\qquad\mathbf1^Tb=1.
$$

The same fractions are restored before every independent identically distributed return realization. There is no leverage, short position, transaction cost, consumption, liability payment, or time-varying signal in the model. This is a constant-rebalanced allocation optimized under a known distribution, not a universal-portfolio learning rule that competes without knowing that distribution.

With $w_1=1$, the source indexes wealth as

$$
w_t=\prod_{j=1}^{t-1}r_j^Tb.
$$

Thus a path reported at dates $1,\ldots,100$ contains 99 returns under that convention. Its log wealth is a random walk with expected increment

$$
g(b)=\mathbb E\log(r^Tb).
$$

When the relevant moments are finite, expected log wealth is $(t-1)g(b)$ and log-wealth variance is $(t-1)\operatorname{Var}\log(r^Tb)$. A positive cash allocation guarantees $r^Tb\ge b_n>0$, avoiding a one-period zero-wealth event. Positive log growth describes asymptotic accumulation, not monotone paths or immunity to a severe initial loss.

The ordinary Kelly problem is

$$
\max_{b\ge0,\,\mathbf1^Tb=1}\mathbb E\log(r^Tb).
$$

It is a convex optimization problem in the standard sense of maximizing a concave objective over a convex feasible set. Cash is feasible and gives growth zero. Appendix A, Lemma 1 proves that all-cash is optimal if and only if every risky asset has $\mathbb Er_i\le1$. The sufficient direction follows from Jensen: $\mathbb E\log(r^Tb)\le\log\mathbb E(r^Tb)\le0$. If some $\mathbb Er_i>1$, a sufficiently small allocation from cash into asset $i$ has positive directional growth derivative $\mathbb Er_i-1$.

For one risky bet paying $P>1$ with probability $\pi$ and zero otherwise, the unconstrained risky fraction is

$$
b_1^*=\max\left\{0,\frac{\pi P-1}{P-1}\right\},\qquad b_2^*=1-b_1^*.
$$

The cash benchmark and the binary case are useful implementation checks. A solver should return no risky exposure when every available bet loses in arithmetic expectation and should match the analytical fraction in the binary case.

## What is constrained

Define the minimum wealth over all dates,

$$
W_{\min}=\inf_{t\ge1}w_t,
$$

and choose $\alpha,\beta\in(0,1)$. The desired probability constraint is

$$
\Pr(W_{\min}<\alpha)<\beta.
$$

For $\alpha=0.7$ and $\beta=0.1$, the event is a loss of more than 30% of initial wealth at any future observation date, with probability below 10%. The ideal problem maximizes $g(b)$ subject to this constraint and the simplex restrictions. Because the crossing probability depends on an entire multiplicative path, the authors do not claim to solve that ideal problem directly.

Set

$$
\lambda=\frac{\log\beta}{\log\alpha}>0.
$$

The central sufficient condition, equation (6), is

$$
\mathbb E(r^Tb)^{-\lambda}\le1
\quad\Longrightarrow\quad
\Pr(W_{\min}<\alpha)<\alpha^\lambda=\beta.
$$

For a fixed $\lambda$, the same allocation satisfies the family of bounds $\Pr(W_{\min}<u)<u^\lambda$ for every $u\in(0,1)$. With the example specification, $\lambda\approx6.456$ and the associated bound at half of initial wealth is $0.5^{6.456}\approx0.0114$. This is a tail envelope for minimum wealth, not just one pointwise numerical risk estimate.

A direct proof uses the nonnegative supermartingale $w_t^{-\lambda}$. Independence and a fixed allocation give

$$
\mathbb E[w_{t+1}^{-\lambda}\mid\mathcal F_t]
=w_t^{-\lambda}\mathbb E(r^Tb)^{-\lambda}\le w_t^{-\lambda}.
$$

Stop when wealth first falls below $\alpha$, truncate the stopping time, and apply the nonnegative-supermartingale stopping argument. On the crossing event, the stopped inverse wealth is strictly above $\alpha^{-\lambda}$. Passing to the limit with the appropriate nonnegative expectation inequality gives the claimed bound. For a zero-probability crossing event the conclusion is immediate. The source presents the equivalent exponentially tilted random-walk proof through Appendix A, Lemma 5: the stopped likelihood ratio has expectation at most one because it equals the tilted measure's probability of eventual stopping.

The one-period inverse moment is the key enforceable object. Independence makes its unconditional version sufficient. An extension to adapted allocations or dependent returns would need the corresponding conditional inequality at every date; merely reusing an unconditional estimate does not preserve the displayed proof. That extension is not the optimization problem solved in this paper.

## Exact convex restriction and risk parameter

The restricted risk-constrained Kelly problem, RCK, is

$$
\max_b\quad\mathbb E\log(r^Tb)
$$

$$
\text{subject to}\quad b\ge0,\quad\mathbf1^Tb=1,
\quad\mathbb E(r^Tb)^{-\lambda}\le1.
$$

For positive payoff, $x^{-\lambda}$ is convex. Composing it with the linear payoff and taking expectations preserves convexity. The log of the expectation is also convex here: it is a log-sum-exp or integral analogue of the convex functions $-\lambda\log(r^Tb)$. Cash remains feasible. A feasible RCK allocation satisfies the original crossing-risk constraint, but some allocations satisfying the original constraint may fail the inverse-moment test. The restriction can therefore be conservative.

Lemma 1 also proves that all-cash is optimal for RCK exactly when all risky expected gross returns are at most one. If a positive-growth Kelly allocation exists, mix a sufficiently small fraction of it into cash. The derivative of its inverse moment at zero exposure is negative, so this mixture is strictly feasible and has positive growth. Lemma 2 then obtains an optimal multiplier from strict feasibility; in the all-cash case a zero multiplier works. Risk aversion does not mechanically force cash for every finite $\lambda$ when an advantageous bet is available.

The parameter can be specified from $\alpha,\beta$ or used to trace a growth-risk tradeoff. At $\lambda=0$ the inverse-moment expression is identically one and the problem reduces to Kelly. As $\lambda$ grows without bound, a fixed feasible payoff must be at least one almost surely. This means no one-period loss; it need not mean a deterministic payoff, because a payoff can be random and still never fall below one.

Let $Z=\log(r^Tb)$. Under the moment and exponential-integrability conditions needed for the expansion,

$$
\frac1\lambda\log\mathbb E e^{-\lambda Z}
=-\mathbb EZ+\frac\lambda2\operatorname{Var}(Z)+O(\lambda^2).
$$

For small positive $\lambda$, the constraint therefore approximately limits log-return variance relative to mean log growth. This is a local expansion, not an exact mean–variance identity or a guarantee for a return distribution with uncontrolled tails.

## Solving finite-outcome instances

For outcomes $r^{(k)}$ with probabilities $\pi_k>0$, $k=1,\ldots,K$, solve

$$
\max_b\sum_{k=1}^K\pi_k\log((r^{(k)})^Tb)
$$

$$
\text{subject to}\quad b\ge0,\quad\mathbf1^Tb=1,
\quad\log\sum_{k=1}^K\exp\{\log\pi_k-\lambda\log((r^{(k)})^Tb)\}\le0.
$$

This is equation (11). The paper uses CVXPY and the ECOS solver with exponential-cone support. Appendix B provides the modeling specification; its return matrix stores outcomes as columns, whereas the surrounding numerical description indexes outcomes as rows. A reproduction must maintain one convention consistently rather than transpose the probability weighting inadvertently.

In the binary case, test the unconstrained Kelly fraction first. If it violates the inverse-moment condition, the optimal risky fraction is the positive risk-boundary root below Kelly:

$$
\pi[1+b_1(P-1)]^{-\lambda}+(1-\pi)(1-b_1)^{-\lambda}=1.
$$

The expression equals one at zero exposure, initially declines for a favorable bet, and is convex. It is not globally monotone on the entire feasible interval. Bisection can locate the nonzero boundary root by bracketing it on the increasing branch, or by maintaining a feasible lower and infeasible upper exposure away from the zero root. With only one risky asset, RCK is necessarily a fractional-Kelly allocation; there is no separate risky composition to optimize.

Two printed slips on pp. 9–10 matter for coding. Equation (10) omits the logarithm from the losing-state objective term; consistency with Kelly requires $(1-\pi)\log(1-b_1)$. The following root equation prints exponent $-\log\lambda$ for that state's inverse payoff; the correct exponent is $-\lambda$. These corrections follow directly from the general problem and are not attributed to an official erratum.

## General distributions, gradients, and optimality checks

If one can sample returns, the source proposes stochastic optimization. Introduce

$$
\Delta_\epsilon=\{b\ge0:\mathbf1^Tb=1,\ b_n\ge\epsilon\}
$$

and assume a solution exists with cash strictly above the chosen $\epsilon>0$. For Kelly, a sampled gradient is $r/(r^Tb)$. Projected ascent uses that gradient, a diminishing step $t_k$, and a step-weighted running average. The source suggests $t_k=C/\sqrt{k}$ and mini-batch averaging.

For RCK, the minimization-form Lagrangian is

$$
\mathcal L(b,\kappa)=-\mathbb E\log(r^Tb)
+\kappa[\mathbb E(r^Tb)^{-\lambda}-1],\qquad\kappa\ge0.
$$

Given sampled payoff $z=(r^{(k)})^T\bar b^{(k)}$, the primal-dual updates are

$$
\bar b^{(k+1)}=
\Pi_{\Delta_\epsilon}\left(\bar b^{(k)}+t_k\left[\frac1z+
\frac{\lambda\bar\kappa^{(k)}}{z^{\lambda+1}}\right]r^{(k)}\right),
$$

$$
\bar\kappa^{(k+1)}=
\Pi_{[0,M]}\left(\bar\kappa^{(k)}+t_k[z^{-\lambda}-1]\right).
$$

Average the primal and dual iterates with weights $t_k$. The assumed multiplier upper bound $M$ and cash floor must not bind the true solution. The paper recommends checking that the computed iterates stay away from those artificial bounds. In practice these checks, convergence diagnostics, and independent evaluation of expected constraints are necessary; a finite number of iterations is not itself an exact feasibility certificate. The manuscript cites stochastic-approximation theory rather than deriving a complete finite-sample convergence guarantee under all possible heavy-tailed return laws.

Appendix A, Lemma 3 gives the projection explicitly. For input $z$, find $\nu$ such that

$$
\sum_{i<n}\max(z_i-\nu,0)+\max(z_n-\nu,\epsilon)=1.
$$

The projected coordinates are those maxima. Bisection in $\nu$ over $[\max_i z_i-1,\max_i z_i]$ solves the scalar equation.

Equations (13) and Appendix A, Lemma 4 supply an independent optimality test. In addition to primal feasibility, $\kappa\ge0$, and complementary slackness, require

$$
a_i=\mathbb E\frac{r_i}{r^Tb}
+\kappa\lambda\mathbb E\frac{r_i}{(r^Tb)^{\lambda+1}}
\begin{cases}
=1+\kappa\lambda,&b_i>0,\\
\le1+\kappa\lambda,&b_i=0.
\end{cases}
$$

Multiplying the stationarity conditions by $b_i$ and summing explains the common value: the first expectation contributes one, and complementary slackness makes the inverse-moment contribution $\kappa\lambda$. These conditions assess the exact RCK problem, whereas the quadratic surrogate below solves a different objective and constraint.

## Quadratic approximation and the Markowitz connection

Write $\rho=r-\mathbf1$, $\mu=\mathbb E\rho$, and $S=\mathbb E\rho\rho^T=\Sigma+\mu\mu^T$. When portfolio net returns $\rho^Tb$ are small,

$$
\log(r^Tb)\approx\rho^Tb-\frac12(\rho^Tb)^2,
$$

$$
(r^Tb)^{-\lambda}\approx1-\lambda\rho^Tb+
\frac{\lambda(\lambda+1)}2(\rho^Tb)^2.
$$

The quadratic RCK problem, QRCK, maximizes $\mu^Tb-b^TSb/2$ on the simplex subject to

$$
-\lambda\mu^Tb+\frac{\lambda(\lambda+1)}2b^TSb\le0.
$$

The second moment is raw, not just covariance. Dropping $\mu\mu^T$ without further approximation changes the program. Large $\lambda$ amplifies higher-order sensitivity; a small-return approximation must be checked in the relevant tail as well as near the mean. QRCK does not inherit the exact crossing-risk guarantee.

The source proves that a QRCK solution is a Markowitz portfolio for some risk-aversion parameter, under its stated condition that every feasible positive-mean portfolio has positive variance. Dualize the quadratic risk constraint, dividing out $\lambda$ when positive, and let its normalized multiplier be $\nu\ge0$. The objective becomes, up to positive scale,

$$
\mu^Tb-\frac\eta2(\mu^Tb)^2-\frac\eta2b^T\Sigma b,
\qquad \eta=\frac{1+\nu(\lambda+1)}{1+\nu}>0.
$$

At the solution $b_q$, this objective has the same gradient as

$$
(1-\eta\mu^Tb_q)\mu^Tb-\frac\eta2b^T\Sigma b.
$$

If $1-\eta\mu^Tb_q$ were nonpositive, cash would outperform the positive-variance candidate in this concave problem, contradicting optimality. Therefore the factor is positive, and division gives the Markowitz parameter

$$
\gamma=\frac\eta{1-\eta\mu^Tb_q}.
$$

This is an exact optimizer correspondence for the approximate QRCK problem under that assumption. It does not make arbitrary mean–variance portfolios exactly drawdown-safe. The authors also use QRCK allocations and multipliers to initialize stochastic RCK optimization, a computational warm start rather than a new guarantee.

## Finite-outcome numerical experiment

Section 7.1 uses $n=20$ assets, comprising 19 risky bets and cash, and $K=100$ possible return vectors. Draw 100 independent uniform numbers on $[0,1]$ and normalize them to probabilities. Draw the 1,900 risky return entries uniformly on $[0.7,1.3]$, then set 30 selected entries to 0.2 and another 30 to 2. The cash column equals one. The printed approximate 0.45 probability of a row containing an extreme entry comes from an independent-entry calculation; exact probabilities depend on whether and how the selected entries are sampled without replacement and on the realized outcome weights. The article does not report a seed or the realized matrix/probability vector.

For each allocation the authors simulate 10,000 wealth paths through date 100. They use $\alpha=0.7$ and target $\beta=0.1$. Table 1 reports:

| Allocation | Mean log growth per period | $\alpha^\lambda$ bound | Simulated crossing frequency |
|---|---:|---:|---:|
| Kelly | 0.062 | not reported | 0.397 |
| RCK, $\lambda=6.456$ | 0.043 | 0.100 | 0.073 |
| RCK, $\lambda=5.500$ | 0.047 | 0.141 | 0.099 |

The first RCK allocation meets the target by the analytical inverse-moment certificate. The lower-$\lambda$ allocation is tuned until simulated risk is near 10%; its theoretical envelope is 14.1%, so it does not possess the same 10% certificate. The distinction matters when comparing the growth improvement from 0.043 to 0.047.

Table 2 reports QRCK growth/crossing-frequency pairs of 0.054/0.218 at $\lambda=0$, 0.027/0.025 at $\lambda=6.456$, and 0.044/0.100 at $\lambda=2.8$. Although the table includes values of $\alpha^\lambda$, these are not guaranteed bounds for QRCK allocations. The exact inverse-moment constraint would have to be checked separately.

Figures 1–3 show sample paths, empirical minimum-wealth distributions, and allocations. Kelly places most risky exposure in bet 4; RCK and QRCK diversify into additional bets. The text occasionally calls these positions outcomes, but Figure 3's horizontal axis is the 20 bets, not the 100 return scenarios. Figure 4 reports about 0.035 growth for fractional Kelly at approximately 10% risk, compared with about 0.047 for the tuned RCK portfolio. This advantage comes from changing the risky mix as well as total exposure.

## Mixture-of-lognormals experiment

Section 7.2 uses an equally weighted mixture of two multivariate lognormal return laws with $n=20$. The cash log mean and corresponding covariance entries enforce gross return one. A sample of one million return vectors is used for optimization. Kelly and RCK use batches of 100, giving 10,000 stochastic-gradient iterations with steps $C/\sqrt{k}$; QRCK uses first and second moments from the same sample and supplies warm starts. A separate sample generates 10,000 evaluation paths through date 100.

Table 3 gives:

| Allocation | Mean log growth per period | $\alpha^\lambda$ bound | Simulated crossing frequency |
|---|---:|---:|---:|
| Kelly | 0.077 | not reported | 0.569 |
| RCK, $\lambda=6.456$ | 0.039 | 0.100 | 0.080 |
| RCK, $\lambda=5.700$ | 0.043 | 0.131 | 0.101 |

The tuned second allocation has estimated risk 10.1%, not an established risk below 10%. Figures 5–6 show its paths and the certified allocation's empirical minimum-wealth distribution. Figure 7 is a material qualification to broad superiority language: fractional Kelly and RCK lie essentially on the same tradeoff curve in this example, while QRCK produces lower growth for comparable simulated risk.

The supplied article does not give the numerical lognormal means/covariances, random seed, step-size constant $C$, cash floor $\epsilon$, dual bound $M$, full parameter grids, or solver tolerances. Its model and algorithm can be reimplemented, but these omissions prevent exact reproduction of the printed instance from the paper alone. No historical estimation window or validation split exists here; the separate simulation sample evaluates a synthetic law already known to the optimizer.

## Uncertainty, certification, and implementation limits

The paper reports no confidence intervals. As a derived scale calculation, 10,000 independent paths with a crossing frequency near 0.10 have a binomial standard error about 0.003, or 0.3 percentage points; a rough 95% interval has half-width 0.006. Therefore 0.099 and 0.101 are both statistically compatible with risk above 0.10, before considering any tuning on those simulations. The finite evaluation horizon also misses crossings after date 100. A finite-horizon crossing frequency is not an unbiased estimate of the infinite-horizon probability in the theorem.

Accordingly, the source's proposed improvement of an ideal-problem growth lower bound to 0.047 based on simulated risk 0.099 is empirical evidence, not a rigorous infinite-horizon feasibility certificate. The analytically certified RCK solution provides the conservative feasible comparison, assuming its inverse moment is evaluated accurately under the true distribution. Monte Carlo checks of that expectation have their own uncertainty, especially when rare near-zero payoffs dominate the inverse moment.

The paper's guarantee is powerful because it reduces a path constraint to a convex one-period expectation. It is limited because that expectation is distribution-sensitive. Estimation error, changing regimes, dependence, and turnover costs require explicit modeling. The method does not by itself cap peak-to-trough drawdown, protect an account under arbitrary return laws, or make a quadratic approximation safe. Its useful implementation is a precisely specified constant-rebalanced model with an independently checked inverse-moment constraint, supplemented by simulation to understand how conservative the certificate is for the chosen return law.

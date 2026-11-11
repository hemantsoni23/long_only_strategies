# An Operational Measure of Riskiness

Dean P. Foster and Sergiu Hart. *Journal of Political Economy* 117(5), 2009, pp. 785–814. This is the original operational construction, distinct from the authors’ subsequent wealth-requirement axiomatization.

Source: [RiskManagement_FosterHart_2009.pdf](../../Finance/RiskManagement_FosterHart_2009.pdf), 30 PDF pages. PDF p. 1 is journal p. 785; the proofs and extensions occupy PDF pp. 20–29. All pages, including the appendix and references, were read. Page references below use PDF pagination.

## Why this matters

A favorable expected payoff does not make a repeated investment safe. If the position is large relative to available wealth, compounding losses can drive wealth toward zero even while its arithmetic expectation grows. Foster and Hart identify a monetary reserve threshold for each gamble. Their construction answers a precise operational question: how much expendable wealth is required before taking that gamble ceases to expose a scale-invariant strategy to eventual bankruptcy in a deliberately adverse sequence of investment opportunities?

The answer is the positive solution of a scalar expected-log equation. Logarithmic utility appears in that equation, but the argument does not begin by assuming that an investor has log utility. It begins with a requirement to avoid wealth converging to zero for every admissible process of offered gambles. That distinction is the contribution: the formula is justified as a minimal reserve constraint, rather than as a complete preference ordering or an optimal growth portfolio.

For quantitative work, this is a useful position-sizing benchmark when a payoff distribution and a credible maximum loss are available. It is especially informative for asymmetric gambles whose standard deviation confounds desirable upside with undesirable losses. It is not an empirically validated estimator of capital needs: the paper has no securities dataset, return backtest, parameter-estimation study, or transaction-cost analysis. Its numerical results are transparent binary-gamble illustrations and its principal evidence consists of theorems.

## Payoffs, wealth, and the admissible environment

A gamble $g$ has finitely many outcomes $x_i$ with probabilities $p_i>0$, summing to one. The domain requires both $E[g]>0$ and $P(g<0)>0$. Thus the paper considers favorable gambles that can lose money. Define

$$
L(g)=-\min_i x_i>0,\qquad M(g)=\max_i x_i>0,\qquad \|g\|_\infty=\max\{L(g),M(g)\}.
$$

All three quantities and the eventual riskiness measure have payoff units. A gamble is a net payoff, not a gross return or an asset price. Changing the currency or multiplying the position by a positive number multiplies the riskiness by that number.

At date $t$, wealth is $W_t>0$, and the decision maker observes the distribution of an offered gamble $g_t$. Acceptance gives $W_{t+1}=W_t+g_t$; rejection leaves wealth unchanged. Future offers can depend on all previous offers, decisions, and realizations. There is no probability distribution over the possible processes of offers and no assumption that future offers are independent of the past. The guarantees are uniform over the specified class of processes.

An important restriction is that the process is finitely generated: there is a finite set $G_0$ of gamble distributions and every offered gamble is a nonnegative multiple of a member of that set. The scale can depend on the history. This condition supplies uniform bounds on log-return increments and, in the shares results, uniform separation from zero drift. It cannot simply be dropped while retaining the proof. Dependence is therefore unrestricted within a structured collection of conditional gamble laws, not unrestricted over every imaginable changing distribution.

A simple strategy is described by a homogeneous threshold $Q(g)$, with $Q(cg)=cQ(g)$ for $c>0$. It rejects when $W<Q(g)$ and accepts when $W\ge Q(g)$. The basic model permits thresholds zero and infinity, including an always-reject strategy. Borrowing is disallowed, wealth must remain nonnegative, and bankruptcy means $W_t\to0$, including hitting zero and staying there. This is an asymptotic mathematical definition, not a legal insolvency event or a drawdown limit.

The universal guarantee quantifies over every positive initial wealth and every admissible process. It does not assert that one isolated acceptance below the threshold necessarily causes bankruptcy. Rather, if a homogeneous policy accepts some gamble below the threshold, there exists a process built from scaled copies of that gamble which makes the policy go bankrupt almost surely.

## Definition, uniqueness, and computation

The riskiness $R(g)$ is the unique finite number greater than $L(g)$ satisfying

$$
E\!\left[\log\left(1+\frac{g}{R(g)}\right)\right]
=\sum_i p_i\log\left(1+\frac{x_i}{R(g)}\right)=0.
$$

The zero at infinite wealth is not the desired solution. A numerically preferable parameterization is $\lambda=1/R$ and

$$
f(\lambda)=\sum_i p_i\log(1+\lambda x_i),\qquad 0\le\lambda<1/L(g).
$$

Here $f(0)=0$, $f'(0)=E[g]>0$, and

$$
f'(\lambda)=\sum_i\frac{p_i x_i}{1+\lambda x_i},\qquad
f''(\lambda)=-\sum_i\frac{p_i x_i^2}{(1+\lambda x_i)^2}<0.
$$

There is positive probability on the worst loss, so $f(\lambda)\to-\infty$ as $\lambda\uparrow1/L(g)$. Strict concavity implies exactly one strictly positive root $\lambda^*$; set $R(g)=1/\lambda^*$. This is the argument of appendix Lemma 1, illustrated by Figure A1 on p. 21.

The sign is operationally decisive. If $L(g)<W<R(g)$, expected log wealth change is negative. It is zero at $W=R(g)$ and positive above the threshold. A lower wealth at or below $L(g)$ additionally allows immediate ruin. The function expressed directly in wealth, $E[\log(1+g/W)]$, is not globally monotone: after crossing zero it eventually returns toward zero from above. Root-finding code should not assume otherwise.

A reproducible discrete-distribution implementation first checks the domain, including normalization of probabilities and the signs of mean and worst payoff. It then brackets the nonzero root of $f$ inside $(0,1/L)$. Use `log1p` for each $\lambda x_i$ and a safeguarded scalar solver. A small positive lower endpoint with positive $f$ and an upper endpoint near $1/L$ with negative $f$ isolate the intended root. Report the residual, the distance of the root from the insolvency boundary, and the sensitivity to the mean and extreme loss. When the mean is tiny, the nonzero root lies near zero and cancellation makes an unconstrained Newton iteration unreliable.

For equiprobable outcomes $+a$ and $-b$, with $a>b>0$, the equation becomes $(1+a/R)(1-b/R)=1$, giving

$$
R(g)=\frac{ab}{a-b}.
$$

Thus $+\$120/-\$100$ requires $\$600$, and $+\$105/-\$100$ requires $\$2{,}100$. The second gamble has only a slightly smaller upside but a much smaller expected surplus, so its reserve requirement is much larger. The mean and standard deviation of the first gamble are $\$10$ and $\$110$; neither alone identifies its reserve threshold.

## The no-bankruptcy theorem and its proof mechanism

Theorem 1, p. 6, states that a simple strategy guarantees no-bankruptcy if and only if $Q(g)\ge R(g)$ for every gamble. Equivalently, every gamble must be rejected at wealth below its riskiness. The condition does not require accepting anything above that threshold. An investor may impose additional preferences, liquidity constraints, or a larger reserve and still satisfy the guarantee.

The sufficiency proof is stronger than the stated simple-strategy theorem. It applies to any strategy that rejects when $W<R(g)$, even if that strategy has no homogeneous threshold. Every accepted gamble then has $W>L(g)$, preventing immediate ruin. Define the realized log increment

$$
Y_t=\log W_{t+1}-\log W_t.
$$

Conditionally on the observed history and the offered gamble, rejection gives $Y_t=0$, while acceptance gives nonnegative conditional expected log increment. The finite-generator assumption and homogeneity of $L$, $M$, and $R$ bound every accepted increment above and below. Consequently

$$
X_T=\sum_{t=1}^T\{Y_t-E[Y_t\mid\mathcal F_{t-1}]\}
$$

is a martingale with bounded increments, and $X_T\le\log W_{T+1}-\log W_1$. If wealth converged to zero, $X_T$ would tend to minus infinity. The martingale result cited in the appendix rules this out: a bounded-increment martingale either converges finitely or oscillates with arbitrarily large positive and negative values. Thus bankruptcy has probability zero. This proof does not claim that wealth stays above its starting value or that severe drawdowns cannot occur.

For necessity, suppose some gamble $g$ has threshold $q=Q(g)<R(g)$. If $q\le L(g)$, immediate ruin is already possible. Otherwise, offer at each date an independent copy of $g$ scaled by $W_t/q$. Homogeneity makes the strategy accept exactly at its threshold. Wealth then multiplies by $1+g_t/q$, and the strong law gives

$$
\frac{\log W_{T+1}-\log W_1}{T}
\longrightarrow E[\log(1+g/q)]<0.
$$

Wealth converges to zero almost surely. Independence enters this particular adverse construction; it is not imposed on all processes in the sufficiency theorem. This separation matters when translating the claim into a risk-control policy.

## Fractional positions and the critical boundary

The shares setup allows any nonnegative multiple of each offered gamble. A simple shares strategy takes $\alpha_t=W_t/Q(g_t)$ units, where the thresholds are finite and strictly positive. Thus the accepted position always uses exactly the prescribed wealth-to-gamble ratio, and

$$
W_{t+1}=W_t\left(1+\frac{g_t}{Q(g_t)}\right).
$$

Theorem 2 and appendix Proposition 8 distinguish strict inequalities from equality. For a finitely generated stream of active gambles, $Q(g)>R(g)$ for every generator implies $W_t\to\infty$ almost surely. If $Q(g)<R(g)$ throughout, wealth tends to zero. If thresholds are everywhere at least the riskiness, the upper limit of wealth is infinite; if everywhere at most the riskiness, the lower limit is zero. At exact equality for every generator,

$$
\limsup_t W_t=\infty,\qquad \liminf_t W_t=0
$$

almost surely. Equality avoids convergence to bankruptcy under the paper’s definition, but it does not ensure a positive wealth floor or eventual growth. The limiting oscillations are why a practical reader should distinguish the exact threshold from a strictly more conservative sizing rule.

The proof centers the log increments as before. The finite set of generators gives bounded increments, a positive lower bound on their conditional variances, and, under strict inequalities, a uniformly positive or negative log drift. The centered martingale divided by time vanishes, while at the boundary its accumulated conditional variance forces unbounded oscillations. These statements concern continued nondegenerate gambling; stopping forever instead preserves the wealth at stopping.

Several alternative long-run goals—no loss, a bounded loss, an assured gain, or unlimited gain—therefore produce the same critical boundary, with strictness qualifications at equality. They are not interchangeable finite-horizon risk guarantees. For example, positive long-run growth is compatible with a substantial probability of finishing a short evaluation window below initial wealth.

## Reproducing the binary illustration

For repeated independent $+120/-100$ gambles with equal probabilities, set $q=Q(g)$ and use the shares rule. If $K\sim\operatorname{Binomial}(t,1/2)$ counts wins, terminal relative wealth is

$$
\frac{W_{t+1}}{W_1}=(1+120/q)^K(1-100/q)^{t-K}.
$$

This binomial expression evaluates the finite-horizon probabilities without Monte Carlo simulation, although its exact values differ somewhat from the paper's rough numerical illustrations. At $t=100$, the probabilities of finishing above initial wealth are approximately 0.028444 for $Q=200$ and 0.617823 for $Q=1000$, compared with the source's approximately 0.027 and 0.64. At $t=1000$, they are approximately $6.88914\times10^{-10}$ and 0.879015, respectively. Median relative wealth for even $t$ is obtained at $K=t/2$: for $Q=1000,t=100$ it is 1.489452, while for $Q=200,t=1000$ it is approximately $3.50747\times10^{-49}$. These exact-binomial evaluations qualify the source's rounded examples; they are independent calculations, not revised numbers supplied by the authors.

At $q=200$, the multipliers are 1.6 and 0.5, with geometric mean $\sqrt{0.8}<1$. At $q=1{,}000$, they are 1.12 and 0.9, with geometric mean $\sqrt{1.008}>1$. At the critical $q=600$, their product is exactly one. Pages 8–9 report the following illustrative values:

| Threshold | Horizon | Probability of no terminal loss | Median wealth relative to initial wealth |
|---|---:|---:|---:|
| $\$200$ | 100 gambles | about 0.027 | about 0.000014 |
| $\$1{,}000$ | 100 gambles | about 0.64 | about 1.48 |
| $\$200$ | 1,000 gambles | about $10^{-9}$ | about $10^{-48}$ |
| $\$1{,}000$ | 1,000 gambles | about 0.87 | about 53.7 |

The paper also gives median wealth ratios of about 0.018 and 7.66 after 1,000 periods for thresholds 500 and 700. These calculations isolate compounding and position size. They contain no estimation error, trading frictions, changing opportunity set, or empirical inference. Treat them as demonstrations of the theorem rather than estimated investment performance.

## Diversification, dominance, and a printed proof error

The riskiness depends only on the payoff distribution, is positively homogeneous, exceeds maximum loss, and is subadditive and convex. For two admissible gambles on a common probability space,

$$
R(g+h)\le R(g)+R(h),\qquad
R(\theta g+(1-\theta)h)\le\theta R(g)+(1-\theta)R(h).
$$

The inequalities are strict unless the gambles are positive multiples of one another, subject to the stated domain. The mechanism is concavity of the log function applied to normalized payoffs. It makes the measure usable as a convex risk constraint when the payoff distribution is known, although this paper does not develop a numerical portfolio optimizer.

There is a sign error in the printed proof on p. 24, immediately after the log-concavity inequality: it concludes $r+r'\le R(g+h)$. The displayed expected logarithm is nonnegative at reserve $r+r'$, so Lemma 1 instead implies $R(g+h)\le r+r'$. The proposition itself has the correct direction. This correction follows directly from the preceding display and the lemma; it is a derived correction, not a cited official erratum.

Both strict first-order and the paper’s strict second-order stochastic dominance reduce riskiness. Higher gains, lower losses, and removal of mean-preserving spreads are thus rewarded. Standard deviation does not have this monotonicity: changing the initial binary gamble from $+120/-100$ to $+150/-90$ improves every outcome but increases standard deviation from 110 to 120. VaR also fails the paper’s strict sensitivity requirement when improvements occur away from its selected quantile; this should not be confused with saying that VaR fails ordinary weak monotonicity.

Dilution has no effect: replacing a gamble with zero with probability $1-\theta$ and otherwise playing the same gamble leaves $R$ unchanged. Its expected logarithm is merely multiplied by $\theta$. This result makes sense for an unlimited sequence, where dilution changes the waiting time to consequential events, but may be undesirable for a finite-horizon capital allocation problem.

For independent gambles, riskiness of their sum is strictly above the smaller individual riskiness and below their sum. For independent identically distributed $g_i$, the appendix strengthens this to

$$
\max\{R(g_1),nL(g_1)\}
<R\!\left(\sum_{i=1}^n g_i\right)
<R(g_1)+nL(g_1)+M(g_1).
$$

Hence riskiness of the average converges to $L(g_1)$, not zero. Even though the average converges in probability to a positive mean, the simultaneous worst-loss event remains possible for each finite sample. The measure retains that support-based constraint. A diversification engine built around it will therefore behave differently from one based on variance or a fixed tail quantile.

## Continuity, other risk measures, and implementation limits

Weak convergence alone does not ensure convergence of riskiness. With uniformly bounded gains and $g_n$ converging in distribution to $g$, if $L(g_n)\to L_0$, Proposition 10 gives

$$
R(g_n)\longrightarrow\max\{R(g),L_0\}.
$$

Ordinary continuity follows when the worst losses also converge to the worst loss of the limiting distribution. In the paper’s example, probabilities on outcomes 2 and $-1$ approach one half each, while a vanishing probability remains on $-3$. The limiting two-point gamble has riskiness 2, but riskiness along the sequence tends to 3. A tiny extreme-loss probability cannot be ignored merely because a sample fails to contain that outcome. This is a substantive obstacle to a plug-in empirical implementation, not a numerical nuisance.

The Aumann–Serrano index $R^{AS}$ instead solves $E[\exp(-g/R^{AS})]=1$. It is connected to a critical constant absolute risk aversion, while the operational measure identifies a wealth threshold. The functions $\log(1+x)$ and $1-e^{-x}$ agree through the quadratic term and differ from cubic order onward. Under the appendix’s uniform boundedness and nondegeneracy conditions, letting the gamble’s positive mean approach zero makes both measures diverge and their ratio approach one. Their common leading approximation is

$$
R(g)\approx R^{AS}(g)\approx\frac{E[g^2]}{2E[g]}.
$$

This is a limiting approximation, not a universally valid risk measure. The raw second moment, not just variance, appears, and the approximation need not preserve dominance. A separate bound is $-L(g)<R^{AS}(g)-R(g)<M(g)$.

The reserve threshold is also different from growth-optimal sizing. If $K(g)$ is the wealth denominator maximizing $E[\log(1+g/K)]$, its first-order condition is $E[g/(1+g/K)]=0$, and $K(g)>R(g)$. For equiprobable two-point gambles, $K(g)=2R(g)$. Thus the maximum nonnegative-log-growth exposure permitted by the reserve boundary is larger than the log-growth-maximizing exposure. A rule that always deploys the largest position allowed by $R$ is not the Kelly optimum.

The measure satisfies homogeneity, subadditivity, and monotonicity, but is not a coherent monetary risk measure because cash translation does not reduce it dollar for dollar. Adding enough cash to remove every loss should eliminate the gamble’s riskiness, which need not equal the original reserve less that cash. This distinction reflects different questions: a reserve supporting repeated favorable bets versus capital added to an arbitrary terminal position.

A protected wealth floor can be incorporated by applying the rule to wealth above that floor. Similarly, a fixed borrowing allowance shifts the relevant origin. Expected-utility agents with constant relative risk aversion at least one satisfy the no-bankruptcy condition; for more general utilities and nonhomogeneous policies, the small-wealth behavior is decisive. Appendix Proposition 11 provides a sufficient strict and necessary weak comparison between $R$ and $Q_1(g)=\lim_{c\downarrow0}Q(cg)/c$, assuming regularity and avoidance of immediate ruin. It does not remove all qualifications at equality.

Finally, unbounded losses imply infinite riskiness under this construction. Accurate implementation therefore requires credible loss bounds, not just estimates of a few moments. Unknown payoff probabilities, unstable means, leverage financing, default of counterparties, consumption, and forced liquidation are not estimated or modeled here. Applying the formula to empirical stock returns or options requires additional choices about horizon, net payoff, distribution estimation, rare-event support, and usable wealth. The paper establishes what follows when these inputs are known; it does not establish that their empirical estimates support the same universal guarantees.

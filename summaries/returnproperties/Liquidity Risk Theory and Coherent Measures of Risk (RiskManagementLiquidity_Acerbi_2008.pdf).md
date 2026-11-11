# Liquidity Risk Theory and Coherent Measures of Risk

**Authors:** Carlo Acerbi and Giacomo Scandolo. **Version inspected:** June 21, 2009 working paper, 25 pages; the local filename says 2008. **Source:** [RiskManagementLiquidity_Acerbi_2008.pdf](../../Finance/RiskManagementLiquidity_Acerbi_2008.pdf). Page references below are PDF/printed pages, which coincide. The full source, Appendix proofs, and Figure 1 were inspected. This is a theoretical framework with an illustrative Monte Carlo figure, not an empirically calibrated market-impact study.

## Why this matters

A portfolio that must raise cash tomorrow can have a different economic value from the same holdings with no funding obligation. Marking every position at a quoted unit price misses the cost of executing the necessary trades. Marking everything at full-liquidation proceeds goes too far when only a small cash amount must be raised. The paper inserts a third object: the highest attainable marked value after trading sufficiently to satisfy an explicit liquidity policy.

Its main contribution is a separation of two operations. First map holdings into a state-dependent, generally nonlinear value using market depth and funding constraints. Then apply a conventional coherent risk measure to that random value. The resulting measure of portfolio risk can fail positive homogeneity and exact cash translation even though the underlying risk measure remains coherent. The failure comes from the economics of converting positions into cash, rather than from a need to abandon coherence as a property of a functional on random monetary outcomes.

This distinction is useful for reproducing the model. A change in liquidity policy changes the valuation map; a change from expected shortfall to another coherent measure changes the distributional aggregation. Neither operation estimates the joint law of prices and liquidity. That law must be supplied separately. The framework addresses trading illiquidity and immediate cash needs. It does not solve a dynamic equilibrium model of market-wide liquidity or determine an optimal multiday execution schedule.

## The market primitives and their signs

There are $N$ noncash assets and one cash account. For each noncash asset, a marginal supply-demand curve $m_i(x)$ gives the price available for the marginal unit when executing a signed quantity $x$. Positive $x$ means selling into the bid side; negative $x$ means buying from the ask side. Each curve is decreasing, with the appropriate one-sided continuity, and is defined at all nonzero real quantities. The best quotes are

$$
m_i^+=m_i(0+),\qquad m_i^-=m_i(0-),\qquad m_i^-\geq m_i^+.
$$

Thus increasing a sale walks down the book, while increasing the size of a purchase walks up it. The formalism allows signed prices, which can matter for contracts that need not always have positive value. For ordinary securities one additionally wants positive prices. Cash has a constant curve $m_0(x)=1$.

Define signed execution proceeds

$$
P_i(s)=\int_0^s m_i(x)\,dx.
$$

For a positive-price asset, a sale gives positive proceeds and a purchase gives a negative cash flow. The average execution price is $P_i(s)/s$, for $s\ne0$; retaining the signed integral avoids confusing purchase costs with sale receipts. Decreasing marginal prices imply concavity of $P_i$.

A portfolio is $p=(p_0,p_1,\ldots,p_N)$, with cash $p_0$ and signed quantities $p_i$. Cash here means funds immediately available at the modeled liquidation instant. A negative cash position is an immediate funding shortfall; a debt instrument with future contractual cash flows need not be represented as negative immediately available cash. Holdings can be arbitrary real numbers, and the basic market permits opening or enlarging shorts. Position or trading restrictions are not implicit.

Two valuation operators appear throughout Sections 3–4:

$$
L(p)=p_0+\sum_{i=1}^N P_i(p_i),
$$

$$
U(p)=p_0+\sum_{i=1}^N
\left[m_i^+p_i\mathbf1_{\{p_i>0\}}+
 m_i^-p_i\mathbf1_{\{p_i<0\}}\right].
$$

$L$ is the cash obtained by full liquidation. $U$ marks long positions at the best bid and shorts at the best ask. It is not a midpoint mark. The depth cost is $C(p)=U(p)-L(p)\geq0$. Because $U$ already uses the appropriate side of the spread, $C$ measures deterioration relative to those best quotes; it is not the entire trading cost relative to a midpoint valuation.

Both $L$ and $U$ are concave, while $C$ is convex. $U$ is positively homogeneous and superadditive. It is additive for portfolios whose noncash positions have the same signs asset by asset. $L$ is subadditive for such concordant portfolios: combining two sales into a larger sale lowers proceeds. For discordant portfolios, with $p_iq_i\leq0$ for every noncash asset, internal netting instead makes $L$ superadditive. These distinctions explain why the later portfolio-risk results depend on sign patterns rather than a universal aggregation rule. For $\lambda\geq1$,

$$
L(\lambda p)\leq\lambda L(p),\qquad
U(\lambda p)=\lambda U(p),\qquad
C(\lambda p)\geq\lambda C(p).
$$

These are statewise valuation statements. They require no return distribution or tail-risk estimator.

## Attainable portfolios and liquidity policies

Trading a signed portfolio $r$ transforms $p$ into

$$
q=p-r+L(r)e_0,
$$

where $e_0$ is one unit of cash. Equivalently, $q_i=p_i-r_i$ for $i\geq1$ and $q_0=p_0+\sum_iP_i(r_i)$. The cash component of $r$ cancels, so an implementation can set $r_0=0$. A positive $r_i$ is a sale, but it need not be bounded above by the original holding. The authors' attainable set includes trades that buy new assets or establish shorts. Imposing liquidation-only trades is a possible extension with different feasible values.

A liquidity policy $\mathcal L$ is a closed convex subset of portfolios. It must allow extra cash: if $p\in\mathcal L$, then $p+ae_0\in\mathcal L$ for $a>0$. It must also allow simultaneous elimination of all noncash holdings while retaining the same cash: $(p_0,0,\ldots,0)\in\mathcal L$ whenever $p\in\mathcal L$. These conditions do not, by themselves, establish that reducing an arbitrary single position always preserves membership. Policies must be checked against the actual set definition.

The central example is a minimum-cash requirement

$$
\mathcal L(a)=\{p:p_0\geq a\}.
$$

The parameter $a$ is the amount of cash required at the modeled future instant. The constraint expresses preparedness for a funding event, not continuous compliance along an unspecified trading path. More elaborate convex policies can encode suitable exposure or margin restrictions. A nonconvex real-world rule need not inherit the paper's optimization and diversification results.

Policy-dependent value is

$$
V^{\mathcal L}(p)=\sup\{U(q):q\in\operatorname{Att}(p)\cap\mathcal L\}.
$$

If there is no feasible attainable portfolio, the value is $-\infty$. The optimization spends as little marked value as possible to achieve the policy. A basic lemma establishes $U(q)\leq U(p)$ for any attainable $q$, hence $V^{\mathcal L}(p)\leq U(p)$. The lower bound $L(p)\leq V^{\mathcal L}(p)$ requires full liquidation to satisfy the policy; it is not automatic when the required cash exceeds liquidation proceeds.

The two extreme policies clarify the interpretation. Requiring all noncash holdings to vanish gives $V=L$. Imposing no restriction gives $V=U$, because no trade is optimal. These are choices of policy, not competing estimates of one universal portfolio value. The distinction is especially consequential when a cash target remains fixed as position size grows.

## The convex valuation problem and its proof logic

Substituting the trade representation gives the implementable form on page 11:

$$
V^{\mathcal L}(p)=
\sup_r\left\{U(p-r)+L(r):
 p-r+L(r)e_0\in\mathcal L\right\}.
$$

The objective is concave. The feasible trade set is convex: concavity of $L$ means that trading a mixture of two feasible trade vectors produces at least the cash of the corresponding mixture of feasible resulting portfolios; the policy's closure under extra cash then preserves feasibility. Consequently maximizing this objective is a convex optimization problem in the standard sense. The source asserts attainment for a nonempty feasible set, although its short proof focuses on convexity; in numerical applications feasibility, finite values, and solver termination still need checking. Its reference to an attained “infimum” in this maximization discussion is a wording error.

Theorem 1 proves

$$
V^{\mathcal L}(\theta p+(1-\theta)q)
\geq\theta V^{\mathcal L}(p)+(1-\theta)V^{\mathcal L}(q),
\qquad0\leq\theta\leq1,
$$

and, for nonnegative added cash $e$,

$$
V^{\mathcal L}(p+ee_0)\geq V^{\mathcal L}(p)+e.
$$

For the first result, mix optimal or approximating liquidation trades for the two portfolios. The mixture is feasible by the preceding cash argument, while concavity of $U$ and $L$ bounds its objective below by the mixture of their original values. For the second, the original trade remains feasible after adding cash, and additional cash can also permit a less costly trade. Extra cash therefore contributes its face amount plus a possible liquidity benefit.

An optimal policy-adjusted portfolio $q^*$ satisfies $V^{\mathcal L}(q^*)=U(q^*)=V^{\mathcal L}(p)$. Once the required restructuring has been done, another execution against the same static book cannot improve the mark. This is not a statement that the original restructuring was costless, or that subsequent prices and liquidity cannot change.

A useful qualification concerns the paper's broad description of the infinitely deep-market limit. Flat bid and ask curves still have a spread. If a policy forces a new position across that spread, its value need not become $U$. For example, with zero initial holdings and cash, a flat bid of 1, ask of 2, and a cash target of 1, selling one unit short produces cash 1 and a short marked at minus 2: the optimal policy value is minus 1, whereas initial $U$ is zero. This counterexample uses the source's unrestricted attainable trades. The intuitive frictionless limit is safe for a zero-spread linear-price market with a feasible policy, or under additional conditions that avoid spread-crossing position changes. It should not be applied to every arbitrary liquidity policy merely because book depth is infinite.

## From random values to portfolio risk

At a fixed future horizon, the entire collection of supply-demand curves is random. For each state $\omega$, solve the valuation problem to obtain $V^{\mathcal L}_\omega(p)$. Apply a coherent risk measure $\rho$ to this random monetary value:

$$
\rho^{\mathcal L}(p)=\rho\big(V^{\mathcal L}(p)\big).
$$

The underlying measure is decreasing in its argument, cash translating as $\rho(X+c)=\rho(X)-c$, positively homogeneous, and subadditive. Larger terminal value means lower risk. The chosen random value must belong to the domain on which $\rho$ is defined; an infeasible policy can require infinite risk. This is not automatically a profit-and-loss measure relative to initial acquisition cost. If that benchmark is desired, define it explicitly and use cash translation consistently.

Theorem 2 combines statewise concavity of $V$ with monotonicity and convexity of $\rho$ to establish convexity of the portfolio functional:

$$
\rho^{\mathcal L}(\theta p+(1-\theta)q)
\leq\theta\rho^{\mathcal L}(p)+(1-\theta)\rho^{\mathcal L}(q).
$$

It also obtains

$$
\rho^{\mathcal L}(p+ee_0)\leq\rho^{\mathcal L}(p)-e,
\qquad e\geq0.
$$

The latter is an inequality because cash can relax forced execution. Exact translation remains an axiom of the risk measure on monetary random variables; it need not survive composition with nonlinear portfolio valuation.

The scaling results in Propositions 6–7, pages 16–18, distinguish three economically different experiments. Under mandatory full liquidation, $\rho^L(\lambda p)\geq\lambda\rho^L(p)$ for $\lambda\geq1$. Its subadditivity is guaranteed for discordant portfolios, where netting helps. Under unconstrained marking, $\rho^U$ remains positively homogeneous, subadditive, and exactly cash translating, even with a bid–ask spread.

Under a fixed cash policy $\mathcal L(b)$, if the original cash is nonnegative,

$$
\rho^{\mathcal L(b)}(\lambda p)\leq\lambda\rho^{\mathcal L(b)}(p),
\qquad\lambda\geq1.
$$

Subadditivity also holds when at least one component portfolio has nonnegative cash. The policy requirement is fixed while portfolio holdings and cash grow, so this result does not imply that market impact disappears for large traders. When the cash requirement is scaled along with the portfolio, the direction reverses:

$$
\rho^{\mathcal L(\lambda b)}(\lambda p)
\geq\lambda\rho^{\mathcal L(b)}(p).
$$

Appendix Lemmas 4–5 supply the corresponding valuation inequalities. Replicating these comparisons requires keeping track of whether $b$ is fixed or scaled; conflating the two experiments produces an apparent contradiction that is absent from the model.

## Explicit cash-policy solution

Section 5 restricts attention to continuous strictly decreasing curves, eliminating the quote discontinuity. Then $U(p)=p_0+\sum_im_i(0)p_i$ is linear. Suppose the required cash is $a$ and the shortfall is $b=a-p_0>0$. Minimizing the loss of marked value gives

$$
\min_r\quad\sum_i\left[m_i(0)r_i-P_i(r_i)\right]
\quad\text{subject to}\quad\sum_iP_i(r_i)\geq b.
$$

For an interior optimum with a binding constraint and multiplier $\lambda\geq0$, the first-order conditions are

$$
m_i(0)=(1+\lambda)m_i(r_i),\qquad
r_i=m_i^{-1}\left(\frac{m_i(0)}{1+\lambda}\right),
\qquad\sum_iP_i(r_i)=b.
$$

The multiplier equalizes proportional marginal price deterioration across assets. A practical algorithm brackets a nonnegative $\lambda$, evaluates the inverse curves, and solves the scalar cash equation, provided the inverse arguments lie in their ranges and the cash target is feasible. If $p_0\geq a$, no execution is necessary and $V=U$. With additional position constraints these interior conditions need complementary slackness and active-bound adjustments; they cannot simply be reused unchanged.

Because the source permits shorts, the optimal trade amounts here depend on the curves and cash shortfall, not directly on the amounts of each asset initially held. This is a potentially surprising consequence of the formal model. A sale-only implementation constrained by $0\leq r_i\leq p_i$ for long holdings is a different optimization problem and must be identified as such.

The worked family is

$$
m_i(x)=A_i e^{-k_ix},\qquad
P_i(r)=\frac{A_i}{k_i}(1-e^{-k_ir}),
$$

with positive $A_i,k_i$ for the nondegenerate strict-impact case. Define

$$
Q=\sum_i\frac{A_i}{k_i}.
$$

For $0<b<Q$,

$$
\lambda=\frac{b}{Q-b},\qquad
r_i=\frac1{k_i}\log\frac{Q}{Q-b}.
$$

The maximum cash obtainable by arbitrarily large sales approaches $Q$; a requirement $b\geq Q$ is not attained by any finite trade. A simulator must not evaluate the logarithm blindly in those states. Zero $k_i$ requires the frictionless limit rather than division by zero.

The execution cost and corrected policy value are

$$
C^*(b)=Q\log\frac{Q}{Q-b}-b,
$$

$$
V^{\mathcal L(a)}(p)=U(p)-C^*(b)
=p_0+\sum_iA_ip_i-Q\log\frac{Q}{Q-b}+b
=a+\sum_iA_i(p_i-r_i).
$$

The final displayed value formula on source page 20 instead prints $\sum_iA_i(p_i-r_i)+a-p_0$. That omits the initial-cash term. The corrected expression above follows both from $U-C^*$ and from the resulting portfolio's cash, which is exactly $a$. It is a correction to a printed algebraic expression, not an alternative economic specification.

Two further implications, derived here from the displayed solution, help verify code. For a small shortfall relative to depth,

$$
C^*(b)=\frac{b^2}{2Q}+\frac{b^3}{3Q^2}+O(b^4/Q^3).
$$

Thus cost is initially quadratic in the cash need and becomes unbounded as $b$ approaches $Q$. Also, while $p_0<a$,

$$
\frac{\partial V}{\partial p_0}=1+\lambda=\frac{Q}{Q-b}.
$$

The marginal value of cash exceeds one because it avoids impact. These statements are exact derivatives or stated series approximations of the analytic example; the paper supplies no estimated economic magnitudes for them.

## The illustrative simulation and what it cannot establish

Figure 1 compares distributions of the value of one portfolio under four price/depth specifications. The frictionless case has jointly normal price factors $A_i$ and $k_i=0$, giving a Gaussian linear marked value. A second case uses positive deterministic impact parameters. A third makes prices and depth parameters stochastic but independent. A fourth introduces negative dependence between $A_i$ and $k_i$, so lower prices accompany greater impact. The figure illustrates a leftward shift from execution costs and more adverse dispersion when price and liquidity deterioration coincide.

There are no empirical return data, calibration sample dates, fitted covariance matrices, or hypothesis tests. The paper does not report the number of assets, holdings, initial cash, cash target, simulation count, random seed, parameter means and variances, or the numerical correlation coefficients. The plotted axes do not substitute for those inputs. No exact change in VaR, expected shortfall, or crisis probability can therefore be recovered from this figure alone.

A second ambiguity matters for reproduction: the text describes joint normality of the price and impact factors while the exponential example assumes nonnegative parameters. An unrestricted Gaussian can generate negative $A_i$ or $k_i$, violating positive-security-price or decreasing-curve assumptions. The source does not specify truncation, transformations, or rejection of invalid draws. A positivity-preserving distribution is a reasonable extension, but presenting one as the authors' undisclosed implementation would fabricate a replication detail.

A faithful implementation should therefore separate the exact analytic model from a newly specified numerical experiment. Supply portfolio units, cash and horizon; specify a valid joint law for all curves; state the liquidity policy; solve each scenario's feasible valuation; retain an explicit infeasibility indicator; and aggregate with a named coherent risk measure and its probability level. Compare policies under the same scenarios to isolate policy effects. Compare dependence structures under controlled marginals if the goal is to isolate price–liquidity dependence. These are implementation requirements derived from the model, not an experimental protocol reported in the source.

## A finite-order-book implementation and the timing of liquidation

The continuous exponential example is not required for computation. A finite order book produces a decreasing step curve and a concave piecewise-linear proceeds function. Suppose the relevant trade interval for asset $i$ is partitioned into quoted segments and write its proceeds as the lower envelope of affine functions,

$$
P_i(r_i)=\min_k\{a_{ik}r_i+b_{ik}\}.
$$

The slopes are the marginal quotes and the intercepts enforce continuity of cumulative proceeds at segment boundaries. Include both purchase and sale sides with the signed-integral convention. An observed book has finite depth, so bounds on the supported trade interval must be added; extrapolating its last quote to arbitrary size would introduce an assumption absent from the observations.

The following linear-program construction is derived from the paper's valuation problem; the authors do not provide this explicit implementation. For a fixed initial portfolio, introduce trade quantities $r_i$, proceeds variables $z_i$, and marked noncash values $u_i$. Define $q_i=p_i-r_i$ and $q_0=p_0+\sum_i z_i$, and impose

$$
z_i\leq a_{ik}r_i+b_{ik}\quad\text{for every segment }k,
$$

$$
u_i\leq m_i^+q_i,\qquad u_i\leq m_i^-q_i.
$$

Maximize $q_0+\sum_i u_i$ subject to $q\in\mathcal L$ and the permitted trade bounds. The two inequalities for $u_i$ encode $U_i(q_i)=\min(m_i^+q_i,m_i^-q_i)$ without introducing a binary variable for position sign. The proceeds inequalities encode a hypograph of a concave function. With a polyhedral liquidity policy, every constraint and the objective are linear.

Why does allowing proceeds below their actual value not distort the answer? A feasible solution with $z_i<P_i(r_i)$ can be improved by replacing the proceeds with their actual values. This adds cash without changing noncash positions; the liquidity policy permits that change and the objective increases. Thus the relaxation recovers the correct attainable value at an optimum. The same monotonicity argument justifies the hypograph representation even for a convex policy requiring a more general convex solver. The construction also clarifies which assumptions matter: convexity and permission to add cash, rather than smooth prices or an exponential curve.

For a stochastic application, the initial holdings $p$ are fixed before the terminal market state is observed. The liquidation trade solving $V_\omega(p)$ is state contingent: it is chosen after the state-specific curves are known. This is a one-stage recourse valuation. Choosing a single trade today and applying it in every scenario is a different, more restrictive problem. Conversely, allowing the initial holdings themselves to depend on the future scenario would introduce perfect foresight and invalidate a portfolio comparison. The paper leaves the intrahorizon path and execution latency outside the model, so terminal recourse should not be confused with a realistically executable strategy through a rapidly changing order book.

When estimating a risk measure from scenarios, use the same probability law and horizon for each competing portfolio or policy. The execution optimizer is inside the scenario loop; tail aggregation is outside it. Evaluating impact at an average curve and then taking risk generally differs from taking risk of statewise optimized values because both optimization and valuation are nonlinear. Infeasible states must retain their economic meaning rather than being dropped from the Monte Carlo sample. In particular, discarding states with $b\geq Q$ in the exponential example would preferentially remove severe liquidity outcomes and bias the estimated risk downward. The source does not propose such a deletion rule.

## Scope and practical limits

The model is static and separable across assets. There is no cross-impact, order-book resilience, execution scheduling, endogenous response of other traders, or estimated transition law for liquidity. Infinite-domain curves simplify attainability but need not imply unlimited cash proceeds, as the exponential example demonstrates. A future margin call can be represented through a policy, but its stochastic dependence on market states must be modeled separately. The framework also takes the chosen horizon and the distributional risk functional as given.

Its strongest reusable result is structural: a concave policy-dependent valuation map, composed with a coherent monetary risk functional, gives a convex portfolio-risk measure and explains an extra marginal value of cash. Its analytic example makes that claim computable and exposes the need to distinguish fixed from scaled funding requirements. The source does not establish the empirical accuracy of any particular price-impact curve, estimate crisis dependence, or demonstrate production-scale performance. Those are separate research tasks after the mathematical specification has been implemented correctly.

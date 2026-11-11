# Dynamical models of market impact and algorithms for order execution

Jim Gatheral and Alexander Schied. Review article, version dated January 24, 2013; first version December 5, 2011. Source: [local PDF](../../Finance/MarketImpact_Gatheral_2013.pdf), 23 pages. Page and equation references below refer to this version.

## Why this matters

An execution optimizer can exploit defects in its own impact model. A fitted impact curve may look plausible for ordinary buy programs, yet imply that alternating purchases and sales creates expected profits or reduces execution costs without an economically plausible mechanism. More subtly, every round trip can have nonnegative expected cost while the optimizer still produces increasingly violent buy–sell oscillations as the trading grid becomes finer.

This review organizes execution models by these forms of regularity. It connects economic restrictions on trading costs to convexity, positive-definite kernels, integral equations and existence of optimal strategies. The central practical contribution is a hierarchy of tests for an impact model, extending beyond fitting average observed impact or checking only for profitable zero-net-position strategies.

The article is a synthesis of theoretical results, with two short proofs and an illustrative numerical experiment. It does not estimate impact from a proprietary execution dataset, report a backtested trading advantage, or provide a general empirical calibration pipeline. The numerical kernel experiment is fully specified at the mathematical level; several more elaborate models require cited papers for their proofs or optimizer formulas.

## Positions, trade signs, revenues and the benchmark

Let $X_t$ be the inventory still held at time $t\in[0,T]$. Positive initial inventory $X_0$ corresponds to a sell program, while negative inventory corresponds to a buy program that brings a short position to zero. Complete liquidation requires $X_{T+}=0$, allowing a final block trade. A sale has $dX_t<0$ and a purchase has $dX_t>0$. Pure liquidation is monotone; allowing arbitrary signed trades produces finite-variation inventory paths.

The unaffected price $S_t^0$ is an exogenously specified semimartingale. Strategies must be predictable relative to the model's filtration. Impact changes the execution price to $S_t^X$. For continuous finite-variation execution, revenue and cost are

$$
R_T(X)=-\int_0^T S_t^X\,dX_t,
\qquad
C_T(X)=X_0S_0^0-R_T(X).
$$

The reference value is initial inventory marked at the unaffected initial price. For a buy program the signed revenue is negative, while the same cost formula measures expenditure relative to that benchmark. Block trades need a within-block execution-price convention; the continuous integral alone must not be applied unchanged to jumps.

For the regularity analysis, $S^0$ is assumed to be a martingale. This removes expected gains from forecasting an exogenous drift and isolates gains created by the model's own impact mechanism. Admissibility also matters: the paper uses bounded strategies and the integrability needed for the relevant stochastic integrals to have zero expectation. One cannot invoke the martingale property while allowing arbitrary doubling strategies.

The execution objective can minimize expected costs, combine mean and variance, or maximize expected utility. Regularity is formulated risk-neutrally so that a model's basic validity is not made dependent on one investor's risk-aversion coefficient. A risk penalty can discourage a pathological strategy without repairing the underlying impact mechanism.

## Three distinct failures

A **price-manipulation strategy** is a round trip with $X_0=X_T=0$ and $E[R_T(X)]>0$, equivalently negative expected cost. This is an expected-profit statement, not a classical almost-sure arbitrage. Repeated and scaled manipulation can lead to quasi-arbitrage in particular settings, but the two concepts should not be conflated.

**Transaction-triggered price manipulation** occurs when a nonmonotone program produces higher expected revenue than every monotone program for the same initial position and horizon. A sell program then benefits from intermediate purchases, or a buy program from intermediate sales. The improvement need not make total expected cost negative.

**Negative expected liquidation costs** occur when a possibly nonzero-net-inventory program satisfies $E[C_T(X)]<0$. This is stronger than simply finding an efficient way to reduce a positive cost. A model can rule out negative-cost round trips while still allowing negative expected cost for a directional liquidation.

Proposition 1 gives the hierarchy. Absence of negative expected liquidation cost implies absence of ordinary manipulation, because round trips are included. If buys raise prices and sells lower them, absence of transaction-triggered manipulation implies absence of negative expected liquidation costs and hence ordinary manipulation. Reverse implications do not generally hold. The transient-kernel example below supplies an explicit model with no negative expected costs but unstable, nonmonotone optimal strategies.

The economic reason this matters is that an optimizer need not deliberately search for a named manipulation strategy. It can embed the same pattern inside a larger parent-order schedule. A numerical solution with unusually low cost may therefore be reporting a model defect rather than an execution innovation. See pp. 2–5.

## Temporary and permanent impact

### Additive Almgren–Chriss form

For an absolutely continuous inventory path, write $v_t=\dot X_t$. The additive model is

$$
S_t^X=S_t^0+\int_0^t g(v_s)\,ds+h(v_t),
$$

where $g$ and $h$ are nondecreasing and vanish at zero. The cumulative term is permanent impact; the rate-dependent term affects the currently executing trade. Define $f(v)=vh(v)$. Integration by parts gives

$$
R_T(X)=X_0S_0^0+\int_0^T X_t\,dS_t^0
-\int_0^T v_t\int_0^t g(v_s)\,ds\,dt
-\int_0^T f(v_t)\,dt.
$$

This separates exogenous price risk from impact costs. The usual unaffected-price illustration is $S_t^0=S_0+\sigma W_t$, with $\sigma$ in price units per square root of time. Additive impact and arithmetic Brownian motion can generate negative modeled prices; the review regards this as often negligible for realistic short-horizon calibrations, not as mathematically impossible.

Proposition 2 states that absence of manipulation **for every horizon** requires linear permanent rate impact, $g(v)=\gamma v$, $\gamma\ge0$. The proof is informative. A nonlinear permanent function admits a two-rate deterministic round trip with negative permanent-impact cost. Stretching time by $1/\epsilon$ and scaling inventory by $1/\epsilon$ keeps rates fixed. The favorable permanent contribution scales as $1/\epsilon^2$, while temporary cost scales only as $1/\epsilon$. For sufficiently small $\epsilon$, temporary costs cannot offset the gain. The conclusion relies on allowing this family of horizons and scales; it is not a numerical claim about a tightly constrained parent order at one fixed horizon.

With linear permanent impact,

$$
R_T(X)=X_0S_0^0+\int_0^T X_t\,dS_t^0
-\frac\gamma2X_0^2-\int_0^T f(v_t)\,dt.
$$

The permanent cost depends on net initial inventory, not the trading schedule. If $f$ is convex, Jensen's inequality and $\int_0^T v_tdt=-X_0$ imply

$$
E[C_T(X)]\ge\frac\gamma2X_0^2+T f(-X_0/T).
$$

A constant-rate path attains the bound:

$$
v_t^*=-X_0/T,\qquad X_t^*=X_0(1-t/T).
$$

Equation (7) on p. 7 prints $X_t^*=X_0/T$, which is a constant with rate-like units and fails the inventory boundary conditions. The expressions above reconstruct the strategy intended by the Jensen proof. Strict convexity is needed for a general uniqueness conclusion; convexity alone establishes optimality. In physical time this is a constant-rate schedule; it becomes VWAP when the time variable is cumulative market volume.

The cited empirical approximation $f(v)\propto|v|^{1+\beta}$ with $\beta\approx0.6$ is convex. This exponent belongs to temporary **cost**, so the corresponding signed temporary price displacement scales like $|v|^\beta$. It should not be confused with an exponent on total parent-order size or the decay exponent of a transient kernel.

### Adding risk

The review distinguishes deterministic mean–variance optimization from adaptive mean–variance control. For deterministic strategies in the arithmetic-Brownian setting, price-risk variance is $\sigma^2\int_0^T X_t^2dt$. For linear temporary impact $h(v)=\eta v$, the mean–variance problem therefore reduces to minimizing

$$
\int_0^T\left[\eta\dot X_t^2+\lambda\sigma^2X_t^2\right]dt
$$

plus the schedule-independent permanent term. A direct derivation gives $\ddot X_t=\kappa^2X_t$, $\kappa^2=\lambda\sigma^2/\eta$, and

$$
X_t=X_0\frac{\sinh(\kappa(T-t))}{\sinh(\kappa T)}.
$$

This explicit calculation is an implementation aid derived from the reviewed criterion, not a new numerical result reported by the article. Its zero-risk-aversion limit is constant-rate trading. The formula presumes $\eta>0$, deterministic parameters and strategies, and the displayed convention without a one-half multiplier on the variance penalty.

Adaptive mean–variance optimization is harder because variance is time inconsistent. Expected utility has a different dynamic structure. Under the cited arithmetic-Brownian/exponential-utility conditions, optimal adaptive execution reduces to a deterministic mean–variance problem. The review also describes time-averaged penalties $E[C_T+\int(\lambda X_tS_t^0+\nu X_t^2)dt]$, which may yield closed-form adaptive strategies with linear temporary impact but can generate negative inventories in extreme scenarios. Those are different risk criteria, not interchangeable calibrations of one formula.

### Multiplicative and supply-curve alternatives

A multiplicative Bertsimas–Lo variant sets

$$
S_t^X=S_t^0\exp\left(\int_0^t g(v_s)ds+h(v_t)\right).
$$

Positive unaffected prices then remain positive. With $g(v)=\gamma v$, the reviewed result excludes ordinary manipulation among bounded strategies. It does not provide the same general closed-form optimizer or establish every stronger monotonicity property. Dynamic programming or HJB methods are needed for the more detailed optimization problems cited.

Other models specify prices by inventory-dependent semimartingales or temporary supply curves. In some of these formulations, continuous finite-variation trades generate no liquidation cost, and general trades can be approximated by such paths. Impact can then be avoided asymptotically. The practical warning is that an appealing supply-curve interpretation is insufficient: the limiting execution-cost definition and admissible path class determine whether impact survives optimization at all. See §3, pp. 5–9.

## Linear transient impact: the kernel is the model

Transient impact from a trade decays with elapsed time. With kernel $G$, the pre-trade impacted price is

$$
S_t^X=S_t^0+\int_{[0,t)}G(t-s)\,dX_s.
$$

Equation (13), p. 10, has an extraneous differential on its left-hand side. The intended object is the price level shown above. The same page inconsistently calls $q$ both order-book density and price impact per share. Its equations use $q=G(0)$ as inverse depth: $\Delta S=q\Delta X$. A constant order density is therefore $1/q$, with units shares per price unit. Using $q$ as density would instead give $\Delta S=\Delta X/q$.

For finite continuous $G$, block execution includes the half-impact self-cost. The expected cost is the quadratic energy

$$
E[C_T(X)]=\frac12E\left[\int_{[0,T]}\int_{[0,T]}
G(|t-s|)\,dX_s\,dX_t\right].
$$

This formula includes initial and terminal block trades and the diagonal contribution. Omitting the diagonal is not an innocuous discretization: it changes the cost of blocks and can create artificial arbitrage.

Proposition 5 equates absence of negative expected liquidation costs with positive definiteness of the even kernel $G(|\cdot|)$ in the Bochner sense. Equivalently, that even function is the Fourier transform of a finite nonnegative measure. “Positive definite” here concerns nonnegative quadratic forms on finite signed trade measures; strict positive definiteness is a stronger property relevant to uniqueness and invertibility.

A nonnegative, nonincreasing, convex decay kernel satisfies the relevant Pólya criterion. The paragraph on p. 11 prints “nondecreasing”; this contradicts its decay setting, following example and Theorem 1. The operative sufficient condition is **nonincreasing**. Positive definiteness alone is weaker than the convex-decreasing regularity condition.

## Solving and reproducing the kernel experiment

For a deterministic trade measure supported on allowed times $\mathcal T$, optimality takes the Fredholm form

$$
\int_{\mathcal T}G(|t-s|)\,dX_s^*=\ell,
\qquad t\in\mathcal T,
$$

together with $\int dX^*=-X_0$. The Lagrange multiplier $\ell$ enforces net execution. In a positive-definite quadratic model, random adaptation cannot improve on the deterministic minimum when the unaffected price is a martingale and the same deterministic execution constraints apply.

On dates $t_0,\ldots,t_N$, let $z_i=\Delta X_{t_i}$ and $K_{ij}=G(|t_i-t_j|)$. Solve

$$
\min_z\frac12 z'Kz\quad\text{subject to}\quad\mathbf1'z=-X_0.
$$

When $K$ is positive definite, solve $Ka=\mathbf1$ and normalize

$$
z^*=\frac{-X_0}{\mathbf1'a}a.
$$

This is preferable numerically to forming an explicit inverse. Verify the residual $Kz^*-\ell\mathbf1$, the net-trade constraint and the energy. A monotone buy program additionally imposes $z_i\ge0$; comparing its quadratic-program value with the unconstrained value directly tests transaction-triggered manipulation on that grid.

Figure 2 specifies $X_0=-10$, $T=10$, equidistant dates $t_i=iT/N$, and $N=10,30,50,100$. Thus there are $N+1$ opportunities, including both endpoints, to buy a total of ten units. Compare

$$
G_1(t)=(1+t)^{-2},\qquad G_2(t)=(1+t^2)^{-1}.
$$

Both are positive definite; $G_2(|t|)$ is the Fourier transform of the measure with density $e^{-|x|}/2$. Yet $G_1$ is convex and decreasing, while $G_2$ is locally concave near zero. For $G_1$, the optimal strategy has positive trades, larger endpoint blocks, and a well-behaved interior as the grid is refined. For $G_2$, alternating signs emerge and the gross traded quantity grows dramatically. The model still has nonnegative expected costs, illustrating why that test alone is inadequate.

As a transparent mathematical reconstruction, solving the displayed matrices in double precision with the caption's net target of ten gives the following approximate values. These are calculations from the formulas, **not numerical tables reported by the authors**.

| $N$ | Kernel | Minimum trade | Maximum trade | Gross traded quantity | Expected impact cost |
|---:|---|---:|---:|---:|---:|
| 10 | $G_1$ | 0.822 | 1.176 | 10.000 | 8.315 |
| 30 | $G_1$ | 0.276 | 0.748 | 10.000 | 7.340 |
| 50 | $G_1$ | 0.166 | 0.661 | 10.000 | 7.248 |
| 10 | $G_2$ | 0.702 | 1.503 | 10.000 | 11.240 |
| 30 | $G_2$ | −2.160 | 2.492 | 22.777 | 11.107 |
| 50 | $G_2$ | −19.255 | 20.023 | 260.608 | 10.947 |

The figure's plotted trade amplitudes appear about twice those from the stated ten-unit normalization. That apparent plotting/caption discrepancy does not change the sign or stability comparison; an implementation should enforce its declared net quantity explicitly. Costs are in the model's normalized price-times-quantity units, not basis points or calibrated currency costs.

At $N=100$, the reconstructed $G_2$ matrix has condition number about $1.7\times10^{13}$, so detailed floating-point trade magnitudes should not be treated as precise economic estimates. High-precision arithmetic and convergence diagnostics are appropriate. A numerical ridge stabilizes a matrix but changes the execution model; it must be reported as a regularization or additional cost, not used to conceal nonexistence in the original continuous-time problem.

## Existence, monotonicity and nonlinear transient impact

Theorem 1 states that a nonconstant, nonincreasing, convex decay kernel has a unique optimal strategy for each initial position and horizon, and that the strategy is monotone. The continuous-time claim is obtained by extending discrete-time results through approximation. It also extends to weakly singular kernels satisfying

$$
G:(0,\infty)\to[0,\infty),\qquad
\int_0^1G(t)dt<\infty,
$$

with the same nonconstant, convex and nonincreasing conditions. In particular $G(t)=t^{-\gamma}$ is permitted for $0<\gamma<1$. Since $G(0)$ is infinite, a finite-kernel block-trade matrix cannot be used literally without choosing admissible finite-energy strategies or an appropriate integrated discretization.

A violation of convexity near zero satisfying $G(0)-G(s)<G(t)-G(t+s)$ for distinct positive $s,t$ produces transaction-triggered manipulation in the cited result. The review also states a nonexistence theorem for kernels whose Fourier measure has an exponential moment, under the conditions of the cited source. Mean–variance optimization can introduce sign changes even for convex-decreasing kernels, so the monotonicity guarantee belongs to the risk-neutral criterion; it is not a theorem about every risk preference.

For nonlinear transient rate impact, the Gatheral model is

$$
S_t^X=S_t^0+\int_0^t h(\dot X_s)G(t-s)ds.
$$

With $G(t)=t^{-\gamma}$, $0<\gamma<1$, and $h(v)=c|v|^\delta\operatorname{sign}(v)$, $c,\delta>0$, Theorem 3 establishes manipulation when $\gamma+\delta<1$. Therefore $\gamma+\delta\ge1$ is necessary within this family; the theorem does not assert it is sufficient. The commonly discussed square-root pair $\delta\approx\gamma\approx0.5$ lies near that boundary, consistent with impact depending roughly on the square root of order size and less on rate. This empirical rule of thumb is cited, not newly estimated here.

More severely, Proposition 6 says that a finite kernel continuous at zero combined with nonlinear $h$ admits manipulation in this model class. Exponential resilience with nonlinear instantaneous rate impact is therefore not generally repaired just by choosing a pleasant-looking half-life. This result concerns the stated convolution model and its execution-cost convention; it does not mean every nonlinear limit-order-book model with exponential recovery is invalid.

## Nonlinear order books and resilience conventions

A general book has shape density $f(x)>0$, cumulative volume $F(x)=\int_0^x f(y)dy$, and inverse $F^{-1}$. Under volume recovery,

$$
E_t=\int_{[0,t)}\exp\left(-\int_s^t\rho_rdr\right)dX_s,
\qquad D_t=F^{-1}(E_t),\qquad S_t^X=S_t^0+D_t.
$$

A block trade $z$ changes the volume displacement from $E_-$ to $E_-+z$. Its impact cash cost is consequently $\int_{E_-}^{E_-+z}F^{-1}(u)du$. Between trades the volume displacement decays exponentially. These equations provide a direct simulation and finite-grid optimization construction once the shape, resilience and time grid are specified.

Price recovery is a different model: while no trade occurs, $dD_t=-\rho_tD_tdt$, retaining $E_t=F(D_t)$. For a nonlinear shape, exponential decay in volume does not imply exponential decay in price. A calibration must choose which state recovers rather than mixing the two transition rules.

Theorem 2 gives sufficient discrete-grid conditions excluding both ordinary and transaction-triggered manipulation: $F(x)$ tends to both corresponding infinities and either the shape increases on the negative half-axis and decreases on the positive half-axis, or $f(x)=\lambda|x|^\alpha$ with positive parameters. The latter family vanishes at zero despite the introductory strict-positivity description; its cumulative function still permits the stated inverse construction. The review cites a corresponding price-recovery result but does not reproduce every condition or optimal-strategy formula.

Models that constrain strategies to buy-only or sell-only exclude round trips by admissibility. This can be an operationally useful parent-order restriction, but it is not a proof that unrestricted dynamics are free of manipulation. Likewise, varying book depth through time can create new irregularities even when fixed-depth exponential resilience is regular. A two-sided spread and distinct bid/ask impact can alter these conclusions; the associated exact parameter restrictions are left to cited sources.

## Dark pools and strategic competitors

In the dark-pool extension, an initial signed order $\widehat X$ may fill in random pieces $Y_i$ at times $\tau_i$, with cumulative executed quantity $Z_t=\sum_{i\le N_t}Y_i$. The unfilled order can be canceled at $\rho<T$. Lit trading rate $\xi_t$ must ensure

$$
X_0+\int_0^T\xi_tdt+Z_\rho=0
$$

almost surely. The exchange price is

$$
S_t=S_t^0+\gamma\left(\int_0^t\xi_sds+\alpha Z_{t-}^{\rho}\right)+h(\xi_t),
$$

and a dark fill executes at

$$
S_{\tau_i}^0+\gamma\left(\int_0^{\tau_i}\xi_sds+\alpha Z_{\tau_i-}+\beta Y_i\right)+g(\xi_{\tau_i}).
$$

The parameters have distinct roles: $\alpha\in[0,1]$ transmits permanent impact from dark fills to lit prices, $\beta\ge0$ creates quadratic dark-fill slippage $\beta\gamma Y_i^2$, and $g$ describes transmission of temporary lit impact into the dark execution price. Confusing these effects can create a strategy that shifts public prices and obtains favorable dark fills.

Under the stated convexity and regularity assumptions, plus arrival/fill conditions referred to the original dark-pool paper, Theorem 4 gives a uniform characterization: excluding manipulation for **every underlying Almgren–Chriss model and every horizon** requires and is achieved by $\alpha=1$, $\beta\ge1/2$, and $g=0$. The minimum slippage then equals the permanent-impact cost $\gamma Y_i^2/2$ of an equivalent lit execution. This is not a universal fee prescription for actual dark pools. Fixing the underlying lit model changes the quantifiers and can yield a subtler admissible region. Arrival intensity, fill-size distribution, cancellation and information leakage must also be modeled; this review supplies no calibrated values.

The multi-agent extension has one liquidating seller and $n$ competitors, all informed about one another's current positions. Price impact depends on aggregate positions and rates:

$$
S_t^X=S_t^0+\gamma\sum_{i=0}^n(X_t^i-X_0^i)
+\eta\sum_{i=0}^n\dot X_t^i.
$$

The seller must finish at $T_0$; competitors start at zero and must close at $T_1$. With common deadlines, the reviewed Nash equilibria feature predatory shorting followed by repurchase. If competitors have more time, temporary-impact-dominated markets can instead make it optimal to absorb the seller's inventory and liquidate later. Permanent-impact-dominated markets more readily sustain predation. For sufficiently many competitors, the cited model finds that adding competitors improves the seller's revenue regardless of the two impact parameters. Exact thresholds and equilibrium formulas are not reproduced here.

These conclusions depend on perfect position information, the specified deadlines and impact-sharing rules. They do not establish that observing order flow reveals all strategic inventories, or that any anticipatory trade has a particular legal status. The review's theoretical classification should remain separate from legal characterization.

## What can be implemented from this source

The additive expected-cost optimizer and the two-kernel experiment can be reconstructed directly from the equations and parameters above. A meaningful replication preserves signs, inventory constraints, diagonal block costs, and matrix conditioning, then compares unrestricted and monotone schedules across grids. The essential outcomes are existence, positivity of cost, monotonicity and stability, rather than a fabricated profit estimate.

The nonlinear-book, dark-pool and multi-agent sections specify mechanisms and key restrictions but delegate substantial proofs and computational details. They require further choices for shapes, resilience, fills, risk criteria and equilibrium solution. No source dataset, estimation window, statistical uncertainty, participation-rate constraint or transaction-fee calibration is supplied. The enduring result is methodological: impact models must be assessed over the strategies an optimizer can generate, and passing a round-trip test alone does not ensure a usable execution algorithm.

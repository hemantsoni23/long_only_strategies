# Portfolio Optimization with Spectral Measures of Risk

**Authors:** Carlo Acerbi and Prospero Simonetti. **Version:** Abaxbank working paper, March 27, 2002, 12 pages. **Source:** [MinimizationSpectralMeasures_AcerbiSimonetti_2002.pdf](../../Finance/MinimizationSpectralMeasures_AcerbiSimonetti_2002.pdf). Printed and PDF page numbers coincide. All sections, proofs, and references were inspected; the source contains no empirical tables, simulations, or separate appendix.

## Why this matters and the contribution

A portfolio's tail scenarios change when its holdings change. Directly minimizing a weighted average of its ordered scenario profits therefore inserts a sorting operation inside the optimization objective. The underlying risk measure can be convex while the implementation still appears awkward to a conventional smooth optimizer. Acerbi and Simonetti generalize the auxiliary-threshold formulation of expected shortfall to arbitrary spectral risk measures. Each downward change in the spectrum receives a threshold that separates an appropriate fraction of adverse scenarios. With affine scenario profits and linear portfolio constraints, the resulting problem is a linear program.

The exact contribution is a reformulation, not a new estimator of return distributions. It preserves the spectral objective while replacing repeated sorting by hinge losses and extra variables. A stepwise spectrum needs only one threshold per jump, allowing computational effort to be tied to the complexity of the investor's risk preferences rather than necessarily to every scenario rank. The second contribution connects mean-versus-spectral-risk optimization to a family of spectral objectives that interpolate between the original risk measure and negative expected profit.

The latter interpretation is useful but needs qualifications omitted from the source's broad statement. Portfolio constraints do not disappear; general nonconvex feasible sets can have unsupported efficient points; and endpoint scalarizations can retain dominated ties. Likewise, convexity alone does not ensure existence or uniqueness, despite the claim on page 2. These qualifications leave the core finite-scenario identity intact and are central when converting the paper into an optimizer.

## Sign, probabilities, and admissible preferences

Let $w\in\mathcal W\subseteq\mathbb R^d$ denote holdings or portfolio parameters, and let $X(w)$ be profit and loss over a fixed horizon. Larger $X$ is better. Risk is a monetary charge, so it carries a minus sign relative to profits. Define lower and upper quantiles by

$$
q_-(u)=\inf\{x:F_X(x)\geq u\},\qquad
q_+(u)=\inf\{x:F_X(x)>u\}.
$$

For a regular spectrum $\phi$, the risk measure is

$$
M_\phi(X)=-\int_0^1\phi(u)q_-(u)\,du.
$$

The spectrum must be nonnegative, nonincreasing, and normalized to integrate to one. It assigns more weight to worse profit quantiles. In a loss convention, the corresponding weight increases toward the upper tail; reversing the sign of profits without reversing this order is a substantive implementation error. The integral must be finite on the chosen domain. An integrable profit variable alone need not suffice for every unbounded spectrum concentrated near zero.

Definition 1.2 also allows a singular component $c\delta_0$, with $0\leq c\leq1$, and a regular component of mass $1-c$. The singular part contributes $-c\operatorname{ess\,inf}X$. The limiting case $c=1$ is worst-case loss. It is finite only for profit distributions bounded below; replacing a population with finitely many observed scenarios makes an empirical worst case finite without proving a finite population worst case.

Under the usual domain and regularity conditions, admissible spectra yield coherent measures: monotonicity, cash translation, positive homogeneity, and subadditivity. Cash translation follows directly from normalization:

$$
M_\phi(X+a)=M_\phi(X)-a.
$$

Thus a spectral objective rewards higher profit levels as well as penalizing adverse outcomes. Negative risk values are possible for uniformly favorable profits and are not computational failures. Law invariance means the risk measure depends on the profit distribution rather than the labels attached to scenarios. It does not, by itself, guarantee that limited data estimate extreme quantiles accurately.

The paper takes the scenario distribution and spectrum as inputs. It does not estimate investor preferences, choose a confidence level, select a forecast horizon, correct scenario probabilities, or supply a market model. Its coherence characterization draws on earlier spectral-risk results; the new proof concerns optimization of this already defined class.

## Expected shortfall as the single-threshold prototype

For lower-tail probability $\alpha\in(0,1]$, define

$$
ES_\alpha(X)=-\frac1\alpha\int_0^\alpha q_-(u)\,du.
$$

A 1% adverse-profit tail corresponds to $\alpha=0.01$, not $0.99$. This quantile-integral definition handles atoms by allocating only the necessary probability mass at a boundary. It need not equal the negative conditional mean given $X\leq q_-(\alpha)$ when that event has probability greater than $\alpha$.

The known Pflug–Rockafellar–Uryasev construction reviewed in Section 2 is

$$
\Gamma_\alpha(X,\psi)=-\psi+\frac1\alpha E[(\psi-X)_+],
\qquad (z)_+=\max(z,0).
$$

For fixed $X$, its minimum over $\psi$ equals $ES_\alpha(X)$. The threshold lies at an adverse-profit quantile. A careful nonsmooth first-order statement is

$$
F_X(\psi-)\leq\alpha\leq F_X(\psi).
$$

Equivalently, the minimizing thresholds fill the closed interval between lower and upper quantiles when these differ. At an atom one uses a subgradient, not an ordinary derivative of the hinge. For a continuous density with a unique quantile, this reduces to $F_X(\psi)=\alpha$. The threshold is not an extra risk preference or model parameter to be separately estimated; it is optimized jointly with the holdings.

For $N$ equally likely scenarios and $k=\lfloor N\alpha\rfloor\geq1$, the paper's empirical convention is

$$
ES^{(N)}_\alpha(X)=-\frac1k\sum_{i=1}^kX_{i:N},
\qquad
\Gamma^{(N)}_\alpha(X,\psi)=-\psi+\frac1k\sum_{i=1}^N(\psi-X_i)_+.
$$

Here $X_{1:N}\leq\cdots\leq X_{N:N}$ are sorted profits. This convention uses the worst $k$ observations and is exactly the empirical tail probability $k/N$. It differs from the empirical quantile-integral ES at an arbitrary nonintegral $N\alpha$, which gives fractional mass to one boundary observation and uses coefficient $1/(N\alpha)$ in the hinge formulation. It is undefined when $k=0$. These choices must not be silently mixed during verification.

When $k<N$, any $\psi\in[X_{k:N},X_{k+1:N}]$ minimizes the displayed objective. The paper sometimes writes a half-open interval, but the right endpoint also minimizes the continuous hinge objective. Ties collapse or extend flat regions without invalidating the identity. When $k=N$, every threshold at or above the sample maximum is optimal and ES becomes negative sample mean.

The interpretation explains the computational gain: one threshold separates the worst $k$ profits from the rest. The optimizer does not need a differentiable ordering of all scenarios. This does not mean sorting-based convex optimization is mathematically impossible; it means an explicit epigraph formulation avoids an awkward representation and allows established convex solvers to work directly.

## Exact finite-scenario generalization

For a general empirical spectrum, use weights

$$
\phi_1\geq\phi_2\geq\cdots\geq\phi_N\geq0,
\qquad\sum_{i=1}^N\phi_i=1,
$$

and define

$$
M^{(N)}_\phi(X)=-\sum_{i=1}^N\phi_iX_{i:N}.
$$

These $\phi_i$ are probability-rank weights whose sum is one, not pointwise continuous density values summing to $N$. A natural precise discretization of an integrable continuous spectrum is $\phi_i=\int_{(i-1)/N}^{i/N}\phi(u)du$. This bin-integral rule is an implementation specification derived from the definition; the paper only calls the weights a natural discretization.

Let $d_j=\phi_j-\phi_{j+1}\geq0$ for $j=1,\ldots,N-1$. The source uses the opposite sign $\Delta\phi_j=-d_j$. Proposition 3.1 can be written without negative hinge coefficients as

$$
\Gamma^{(N)}_\phi(X,\psi)
=\sum_{j=1}^{N-1}d_j\left[\sum_{i=1}^N(\psi_j-X_i)_+-j\psi_j\right]
-\phi_N\sum_{i=1}^NX_i.
$$

Its joint dependence on the scenario profits and thresholds is convex and piecewise linear. For every fixed scenario vector,

$$
\min_\psi\Gamma^{(N)}_\phi(X,\psi)=M^{(N)}_\phi(X).
$$

When $d_j>0$, an optimal threshold satisfies $\psi_j\in[X_{j:N},X_{j+1:N}]$. If $d_j=0$, its entire term vanishes and that variable should be omitted. Thresholds need not be explicitly sorted or constrained relative to each other: their independent minimizations place them at their associated ranks. A solver may return coincident or endpoint thresholds because the solution need not be unique.

The proof is constructive. At a valid rank-$j$ threshold,

$$
\sum_i(\psi_j-X_i)_+-j\psi_j=-\sum_{i=1}^jX_{i:N}.
$$

Substitute this into the objective and collect the coefficient of $X_{i:N}$. Its total adverse weight is $\sum_{j=i}^{N-1}d_j+\phi_N=\phi_i$, producing the original sorted statistic exactly. The $j=N$ auxiliary variable introduced temporarily in Eq. (16) is unnecessary because its contribution reduces to $-\phi_N\sum_iX_i$ whenever its threshold exceeds the maximum profit.

The constant-spectrum case is an important boundary: if every $\phi_i=1/N$, all $d_j$ vanish and the objective is simply $-N^{-1}\sum_iX_i$. No threshold is needed. Conversely, a strict decrease at every rank gives $N-1$ useful thresholds. More aggressive weighting of the worst scenarios changes the objective rather than making the solver estimate a different distribution.

As an algebra check, take four equally likely profits $(-4,-1,2,5)$ and rank weights $(0.4,0.3,0.2,0.1)$. This is an illustrative calculation, not an empirical experiment in the paper. The sorted formula gives risk $1.0$. The differences are all $0.1$; the threshold terms contribute $0.4$, $0.5$, and $0.3$, while the mean term contributes $-0.2$, again giving $1.0$. This check exercises the normalization and the sign of the final term, two common sources of incorrect implementations.

## An implementable linear program

Suppose scenario profits are affine in holdings,

$$
X_i(w)=a_i+b_i'w,
$$

and the permitted portfolio set is described by linear constraints such as $Aw\leq b$ and $Ew=f$. This includes fixed-budget and expected-profit constraints once returns, cash, and financing conventions are specified. The paper does not prescribe particular constraints or permit unbounded leverage by default.

Let $J=\{j:d_j>0\}$. Introduce one $u_{ij}$ for each scenario and active threshold, and solve

$$
\min_{w,\psi,u}\quad
\sum_{j\in J}d_j\left(\sum_{i=1}^Nu_{ij}-j\psi_j\right)
-\phi_N\sum_{i=1}^N(a_i+b_i'w)
$$

subject to

$$
u_{ij}\geq\psi_j-a_i-b_i'w,\qquad u_{ij}\geq0,
\qquad Aw\leq b,\quad Ew=f.
$$

Because every $d_j$ is positive on $J$, minimizing drives the slack $u_{ij}$ to the hinge value. No binary variables or sorting subroutine are needed. The formulation has $d+|J|+N|J|$ variables before optional simplification, and $2N|J|$ hinge inequalities plus portfolio constraints. A fully varying spectrum can therefore lead to quadratic growth in scenario count. The paper states that linear programming is possible but does not supply benchmark runtimes, solver tolerances, or a scalability experiment.

If a lower bound on expected profit is wanted, add $N^{-1}\sum_iX_i(w)\geq\mu_0$. For a risk budget, constrain the lifted objective to be at most $\rho_0$ and maximize expected profit: existence of some thresholds with lifted value below the budget is equivalent to spectral risk below that budget. An equality to a risk budget is more delicate and can force a portfolio onto an inefficient branch; the inequality is the natural convex feasible-set construction.

General nonlinear dependence $X_i(w)$ does not automatically preserve a linear program or joint convexity in $w$. The theorem is convex in the profit vector; affine mapping preserves that convexity. Concave profit maps can also permit convex formulations under suitable composition conditions, but that is not a license to feed arbitrary nonlinear prices, market impact, or discrete decisions into the same LP. Revalue instruments in each fixed scenario first when the scenario profit is linear in position size, and distinguish this from changing the scenario law as positions change.

After solving, independently evaluate the original sorted spectral objective at the returned holdings. Verify agreement with the optimized lifted value, portfolio feasibility, and cash-translation scaling. Report nonunique portfolios honestly rather than treating different threshold values as different risk estimates. With unbounded shorts or an arbitrage direction, the minimum may be negative infinity; bounded feasible sets or appropriate coercivity conditions are needed for existence. Convexity prevents spurious strict local minima but proves neither attainment nor uniqueness.

## General distributions and stepwise spectra

For a differentiable decreasing spectrum, Section 3.2 replaces discrete differences by derivatives:

$$
\Gamma_\phi[X,\psi]=
\int_0^1\phi'(u)\left[u\psi(u)-E(\psi(u)-X)_+\right]du
-\phi(1)E[X].
$$

Equivalently, let $\nu(du)=-d\phi(u)$ be the nonnegative Stieltjes measure generated by the decreasing spectrum. Then

$$
\Gamma_\phi[X,\psi]=
\int_{(0,1)}\left[E(\psi(u)-X)_+-u\psi(u)\right]\nu(du)
-\phi(1)E[X].
$$

This second form handles downward jumps transparently. Appropriate integrability and endpoint conditions are needed to interchange integration, expectation, and minimization. The paper's argument chooses $\psi(u)$ at the $u$-quantile, converts the hinge bracket to the integral of lower quantiles, and integrates by parts. The endpoint term $\phi(1)E[X]$ cancels, leaving $-\int\phi q$. It is not an extra funding adjustment.

For a spectrum with downward jump sizes $d_k=\phi(p_k-)-\phi(p_k+)\geq0$ at $p_k\in(0,1)$, the functional reduces to

$$
\Gamma_\phi(X,\psi)=
\sum_{k=1}^Jd_k\left[E(\psi_k-X)_+-p_k\psi_k\right]
-\phi(1)E[X].
$$

Only $J$ thresholds are needed, regardless of how many observations approximate the expectations. In a sample of $N$ equiprobable scenarios, replace each expectation by $N^{-1}\sum_i$. These continuous step heights $d_k$ should not be confused with the already normalized discrete rank-weight differences earlier; the factor $1/N$ belongs here.

A nonsingular spectrum can also be interpreted as a mixture of expected shortfalls and negative mean, because each bracket minimizes to $p_kES_{p_k}(X)$. For step spectra, normalization implies $\phi(1)+\sum_kp_kd_k=1$. This gives both an economic interpretation and a numerical check on a user-supplied risk-aversion curve.

Two qualifications matter. First, Proposition 3.2 calls the continuum functional piecewise linear. After expectation over a continuous distribution, hinge averages can be smooth nonlinear functions of the threshold; convexity survives, but finite-dimensional piecewise linearity belongs to a finite-scenario implementation. Second, the singular $c\delta_0$ admitted earlier is not automatically represented by an ordinary $\phi'$ integral on $(0,1)$. Add its worst-case term separately. In a finite scenario model this is implemented with $v\geq-X_i(w)$ for every scenario and objective coefficient $c$ on $v$, alongside the regular component. This preserves an LP but estimates only the sample worst case.

## Mean-risk frontiers and the scalarization result

The paper defines dominance in the plane $(M_\phi(X),E[X])$: another feasible portfolio dominates if it has no greater risk and no lower mean, with at least one strict improvement. It then proposes

$$
M_{\widehat\phi_\lambda}(X)
=(1-\lambda)M_\phi(X)-\lambda E[X],\qquad
\widehat\phi_\lambda(u)=(1-\lambda)\phi(u)+\lambda,
\quad0\leq\lambda\leq1.
$$

The new spectrum remains nonnegative, decreasing, and normalized. Increasing $\lambda$ shifts weight toward the uniform spectrum, hence toward mean profit. This explains why mean-risk preferences can themselves be written as a spectral objective. It does not mean that the investor's original spectrum or target return has been empirically identified.

For an interior value $0<\lambda<1$, every global minimizer over the same feasible set $\mathcal W$ is Pareto efficient: a dominating alternative would strictly lower a positive weighted sum of risk and negative return. The multiplier correspondence in the source is $\beta=\lambda/(1-\lambda)$ for minimizing risk minus $\beta$ times mean. A rigorous nonsmooth constrained statement uses subgradients and the normal cone of $\mathcal W$ rather than the paper's unrestricted differential equations.

Recovering every efficient point by weighted sums requires suitable convexity and closedness of the attainable upper objective set. Affine profits and convex portfolio constraints provide the natural setting. With lot sizes, cardinality limits, or other nonconvex restrictions, an efficient portfolio can be unsupported by any linear scalarization. The source does not state these restrictions when claiming full equivalence for an arbitrary feasible set.

At $\lambda=0$, a minimum-risk portfolio can be dominated by another portfolio with equal risk and higher mean. At $\lambda=1$, a maximum-mean portfolio can be dominated by another with equal mean and lower risk. Thus the statement in Remark 4.3 that all solutions automatically are efficient over the closed interval is too strong. Lexicographic tie-breaking at the endpoints restores the intended efficient choice. Moreover, “unconstrained” refers to removing a separate risk or return target; the original budget, exposure, and admissibility restrictions remain. Removing them changes the problem and can create an unbounded objective.

Example 4.4 specializes to ES:

$$
\widehat\phi_\lambda(u)=\lambda+\frac{1-\lambda}{\alpha}\mathbf1\{u\leq\alpha\}.
$$

There is one downward jump. Under the paper's signed convention $\Delta\phi=\phi(p+)-\phi(p-)$, its jump is $-(1-\lambda)/\alpha$, not the positive sign printed on page 11. The correct lifted objective is directly

$$
(1-\lambda)\left[-\psi+\frac1\alpha E(\psi-X)_+\right]-\lambda E[X].
$$

This formula is the safest implementation because it makes the positive hinge coefficient explicit. Using the printed positive signed jump in Eq. (31) would reverse the convexity and can make threshold minimization unbounded.

## What is and is not established

This is a theoretical optimization paper. It supplies no asset universe, return sample, dates, transaction costs, rebalancing rule, out-of-sample test, optimized portfolio performance, or Monte Carlo confidence intervals. Applications and computational experiments are deferred to a future publication listed as in preparation. No numerical evidence should be invented to fill those omissions.

The exact, reusable result is the finite-scenario threshold reformulation and its reduction for stepwise spectra. It gives a transparent way to implement distribution-sensitive risk preferences with linear constraints and to verify the answer against a sorted-scenario calculation. The frontier construction adds a useful preference interpretation once convexity, endpoint ties, and retained portfolio constraints are stated correctly. It does not solve distribution estimation, extreme-tail uncertainty, or the instability of optimized weights under changing scenarios. Those remain inputs and risks outside the theorem.

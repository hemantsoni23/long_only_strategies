# Simple Binomial Processes as Diffusion Approximations in Financial Models

Daniel B. Nelson and Krishna Ramaswamy, *The Review of Financial Studies* 3(3), 1990, 393–430. Source: [BinomialTrees_NelsonRamaswami_1990.pdf](../../Finance/BinomialTrees_NelsonRamaswami_1990.pdf). The supplied scan has a JSTOR cover followed by all 38 article pages: printed p. 393 is PDF p. 2. Every page, including the convergence appendix and numerical tables, was read visually. The source filename misspells the second author's surname; it is preserved in the link and note filename.

## Why this matters

A two-branch approximation is not necessarily a computationally useful tree. If each node uses its own state-dependent up and down distances, an up-then-down path need not reach the same state as a down-then-up path. The number of distinct terminal states can then double each period. Nelson and Ramaswamy construct recombining approximations to a broad class of one-dimensional diffusions by first transforming the state to constant local volatility. The transformed lattice has regular spacing; mapping its nodes back restores the intended state-dependent volatility without destroying recombination.

The difficult part is at boundaries where volatility vanishes. A square-root interest-rate process can have positive drift at zero, whereas a CEV stock can be absorbed there. A naive transform and nearest-neighbor walk can accidentally absorb the interest rate or distort its local drift. The paper allows odd multiples of the basic lattice jump near the boundary, preserving the lattice parity while moving far enough to support the required conditional mean. It then states conditions for weak convergence and separately proves convergence of European option values and discounted bond values.

This separation matters. Weak convergence of the state alone does not automatically establish convergence of every derivative price, especially for unbounded payoffs, early exercise, or path-dependent claims. The article proves selected pricing results and reports numerical evidence for American puts, while explicitly declining to claim a general American-option convergence theorem. Its numerical examples also show that asymptotic validity is not a guarantee of satisfactory accuracy at a chosen finite step count.

## General diffusion and the local matching conditions

The target is

$$
dy_t=\mu(y_t,t)\,dt+\sigma(y_t,t)\,dW_t,\qquad y_0\text{ fixed}.
$$

For horizon $T$, choose $n$ intervals of length $h=T/n$. At a node $(y,t)$, a Markov chain jumps to $Y_h^+(y,t)$ with probability $q_h(y,t)$ and $Y_h^-(y,t)$ with probability $1-q_h(y,t)$, then remains constant until the next grid time. Require ordered finite destinations and $0\le q_h\le1$. Its local conditional drift and uncentered second moment are

$$
\mu_h=\frac{q_h(Y_h^+-y)+(1-q_h)(Y_h^--y)}h,
$$

$$
a_h=\frac{q_h(Y_h^+-y)^2+(1-q_h)(Y_h^--y)^2}h.
$$

The second quantity is not exactly conditional variance per unit time: that variance is $a_h-h\mu_h^2$. Under locally bounded drift the distinction disappears as $h\to0$. Using the uncentered moment is deliberate and is called out in the source.

Theorem 1 requires continuous drift and nonnegative continuous volatility, existence and uniqueness in distribution of a nonexplosive solution, uniformly vanishing up/down jumps on every compact state-time set, and local-uniform convergence $\mu_h\to\mu$, $a_h\to\sigma^2$. With common initial value, the piecewise-constant processes then converge weakly to the diffusion in the Skorokhod path-space topology. This entails convergence of finite-dimensional distributions and suitably continuous path functionals; it is not a pathwise error estimate, a convergence rate, or an assertion that trajectories driven by the same random numbers stay close.

For an Ornstein–Uhlenbeck example, $dy=\beta(\alpha-y)dt+\sigma dW$, use destinations $y\pm\sigma\sqrt h$ and

$$
q_h=\operatorname{clip}_{[0,1]}\left(\frac12+\frac{\sqrt h\,\beta(\alpha-y)}{2\sigma}\right).
$$

The uncentered local second moment is exactly $\sigma^2$. The uncensored drift is exact, and on every compact state set clipping eventually becomes inactive. Thus clipped probabilities do not obstruct this particular weak limit even though they change the finite-grid model. This is different from claiming that arbitrary clipping is harmless in derivative pricing.

## Transforming to a recombining lattice

Where $\sigma$ is positive, define

$$
X(y,t)=\int^y\frac{dz}{\sigma(z,t)},\qquad y=Y(x,t).
$$

The integration constant can be chosen consistently. Itô's formula gives diffusion coefficient $X_y\sigma=1$ for the transformed process. The transformed drift contains $X_t+\mu/\sigma-\tfrac12\sigma_y$, but the algorithm need not approximate that drift directly. It places candidate states at $x\pm\sqrt h$ and maps them to the next calendar date:

$$
y^+=Y(x+\sqrt h,t+h),\qquad y^-=Y(x-\sqrt h,t+h).
$$

Choose the probability to match the drift in the original state:

$$
q_h=\frac{y+h\mu(y,t)-y^-}{y^+-y^-}.
$$

This produces exactly $E[y_{t+h}-y_t\mid y_t=y]=h\mu(y,t)$ whenever the probability is valid. Since $Y_x=\sigma$ and $Y_{xx}=\sigma\sigma_y$, local Taylor expansion yields $y^\pm-y=\pm\sigma(y,t)\sqrt h+O(h)$, and the second moment converges to $\sigma^2$. It is important to evaluate the inverse map at $t+h$ for a time-dependent volatility; using $t$ changes the drift calculation.

At date $kh$, all transformed states belong to $x_0+(2j-k)\sqrt h$. Without exceptional branches this gives $k+1$ nodes at that date. “Computationally simple” in the article means the number of nodes in a time slice grows at most linearly with the number of steps; total work over all slices is ordinarily quadratic. It does not mean an entire $n$-step tree contains only $O(n)$ node evaluations.

For geometric Brownian motion, $X(y)=\log(y)/\sigma$ and $Y(x)=e^{\sigma x}$, recovering the familiar multiplicative recombining construction. For a generic state-dependent volatility, applying $y\pm\sigma(y,t)\sqrt h$ directly in original coordinates lacks that recombination property. The transform supplies the missing geometric structure.

## Sufficient regularity and treatment of a zero boundary

Theorem 2 treats a nonsingular diffusion. Its sufficient assumptions include fixed transformed endpoint limits $x^L,x^U$; drift and variance continuity; volatility bounded away from zero on compact state-time sets; nonexplosion; and existence/local boundedness of the first and second partial derivatives of $\sigma$ and the inverse map used in the Taylor argument. The article permits transformed infinite-state endpoints and defines the inverse outside them formally, while assuming steps are small enough to avoid undefined transition probabilities. Probabilities are clipped into $[0,1]$ if necessary. Compact-set positivity of volatility ensures this clipping eventually becomes irrelevant there.

A usable nonexplosion criterion in the appendix is a nonnegative Lyapunov function $\varphi(y,t)$, once differentiable in time and twice in state, tending uniformly to infinity as $|y|\to\infty$ on bounded time intervals, such that

$$
\mu\varphi_y+\tfrac12\sigma^2\varphi_{yy}+\varphi_t\le\lambda(T)\varphi
$$

on $0\le t\le T$, for locally bounded positive $\lambda$. This converts a global path property into a generator inequality that can be checked for a proposed diffusion.

Theorem 3 allows $\sigma(0,t)=0$, $\mu(0,t)\ge0$, and positive volatility for $y>0$. The inverse map is set to zero for $x\le x^L=\lim_{y\downarrow0}X(y,t)$. The transformed endpoints are again assumed independent of time. A generalized modulus condition replaces ordinary Lipschitz continuity of volatility: for an increasing nonnegative $\rho$, positive away from zero,

$$
\int_{0+}^1\frac{du}{\rho(u)^2}=\infty,\qquad
|\sigma(y,t)-\sigma(z,t)|\le C\rho(|y-z|)
$$

locally, while drift is locally Lipschitz in state. This includes square-root volatility with $\rho(u)=\sqrt u$. Additional smoothness holds away from zero, $\sigma_y$ is positive near zero, and the inverse-map derivatives needed for the expansion remain bounded on compact sets. These are explicit sufficient conditions, not a theorem for every nonnegative diffusion with a square-root-looking coefficient.

Near zero, select odd positive integers $J_h^+,J_h^-$ and let

$$
y^+=Y(x+J_h^+\sqrt h,t+h),\qquad
y^-=Y(x-J_h^-\sqrt h,t+h).
$$

Choose the smallest odd upward step satisfying $y^+\ge y+h\mu(y,t)$ in a specified neighborhood $x<x^B$; away from it use one upward step. For the downward step, choose the smallest odd step satisfying $y^-\le y+h\mu(y,t)$, or reaching the zero boundary. Recompute the same mean-matching probability, with clipping where the construction calls for it. Odd step counts move from one time slice's parity to the next and therefore land on existing lattice locations. They do not insert irregular off-grid states. Restricting exceptional upward jumps to a fixed lower region preserves the linear growth of time-slice width.

Equation (44), printed p. 406, has the difference reversed in its downward test: it prints $Y(x,t)-Y(x-j\sqrt h,t+h)\le\mu h$. The condition stated here is the one obtained from $q_h\ge0$, namely $Y(x-j\sqrt h,t+h)-Y(x,t)\le\mu h$. It agrees with the appendix's inequalities (A12), (A17), and (A22), and with the explicit CIR rule (62). This is a derived correction to a printed sign; implementing the literal general formula can choose entirely wrong downward branches when drift is negative.

The boundary theorem guarantees nonnegativity of both the chain and limiting process, and weak convergence for a positive initial value under its assumptions. Zero need not be absorbing. When both drift and volatility vanish there, it can be absorbing; when drift is positive, the chain must retain a route out. The article also explains that an upper boundary with nonpositive drift can be handled symmetrically using exceptional downward branches.

## CEV stock and risk-neutral pricing

The stock example is

$$
ds_t=\mu s_t\,dt+\sigma s_t^\gamma\,dW_t,\qquad \tfrac12\le\gamma\le1.
$$

For $\gamma<1$, the transform and inverse are

$$
X(s)=\frac{s^{1-\gamma}}{\sigma(1-\gamma)},\qquad
S(x)=\begin{cases}[\sigma(1-\gamma)x]^{1/(1-\gamma)},&x>0,\\0,&x\le0.
\end{cases}
$$

The displayed power formula is singular at $\gamma=1$; that case uses the logarithmic transform above. At zero the stock is absorbed. The appendix extends volatility to $\sigma|s|^\gamma$ on the whole real line to invoke the existence/uniqueness machinery, then establishes that a nonnegative initial state remains nonnegative. The range $\gamma\ge1/2$ is part of the boundary regularity, not an arbitrary calibration convention.

Pricing uses a different transition probability from the physical drift-matching tree. With constant risk-free rate $r\ge0$, no dividends, and gross one-step return $R=e^{rh}$, exact one-step replication gives

$$
C(s,t)=e^{-rh}\{p_hC(s^+,t+h)+(1-p_h)C(s^-,t+h)\},\qquad
p_h=\frac{e^{rh}s-s^-}{s^+-s^-}.
$$

Here terminal call value is $(s-K)^+$ and put value $(K-s)^+$. Physical drift $\mu$ is absent. To keep $0\le p_h\le1$ throughout every finite tree, choose upward/downward odd steps so that $s^-\le e^{rh}s\le s^+$, rather than clipping a probability that fails this no-arbitrage bracket. Equations (70)–(72) permit the necessary upward jumps everywhere. This modification assures pricing probabilities but does not automatically guarantee computational simplicity for every imaginable coefficient specification; the source makes that qualification explicitly. It reports simplicity for conventional parameter choices in its CEV applications.

Under the theorem's conditions for the risk-neutral diffusion $dS=rSdt+\sigma(S,t)dW$, the pricing chain converges weakly. European puts have bounded terminal payoff, so convergence of expectations follows. Calls are handled using put–call parity rather than an unsupported inference about arbitrary unbounded payoffs. This is the logic of Theorem 4. Its source setting assumes the usual valid risk-neutral stock pricing relation; extending the argument to bubble/strict-local-martingale cases would require checking that relation separately.

For an American put, backward induction replaces continuation value by the maximum of continuation and intrinsic value. The paper gives a Taylor-expansion connection with the free-boundary PDE but states that it has not rigorously extended Theorem 4 to American options. Non-dividend-paying American calls have no early-exercise advantage in this setup, so the reported call values use the European benchmarks. Numerical agreement of selected American puts is evidence for those cases, not a proof for all optimal-stopping problems.

## CIR rates and the boundary branch rule

The rate process is

$$
dr_t=\kappa(\bar r-r_t)\,dt+\sigma\sqrt{r_t}\,dW_t,
\qquad X(r)=\frac{2\sqrt r}{\sigma},\qquad
R(x)=\frac{\sigma^2}{4}(x^+)^2.
$$

Parameters $\kappa,\bar r$ are nonnegative. When $\kappa\bar r>0$, zero has positive drift and must not become an absorbing lattice state. The paper's Figure 3 shows why this can fail with a single upward step: several transformed nodes below zero map to the same rate zero, and an adjacent upward node may still map to zero. An odd multi-step branch can reach the first sufficiently positive rate while preserving recombination.

In the positive-$x$ region, the mean target is $R(x)+h\kappa(\bar r-R(x))$. Dividing by $\sigma^2/4$ gives the quantity $A=4h\kappa\bar r/\sigma^2+x^2(1-\kappa h)$. Equations (61)–(62) choose the smallest odd positive upward $j$ with $(x+j\sqrt h)^2>A$, and the smallest odd positive downward $j$ with $(x-j\sqrt h)^2\le A$ or $x-j\sqrt h\le0$. Then compute the two mapped rates and the mean-matching probability, clipped into $[0,1]$ as specified. At mapped-zero nodes, the robust general construction uses $R(x)=0$ in the target and the piecewise inverse $R$ in both destinations. The printed squared-$x$ shortcut must not be mistaken for the inverse map on negative $x$.

For a default-free bond, the source introduces an instantaneous risk-premium adjustment $r^*=r[1+g(t,T-t)]$, where $g$ is bounded, continuous, and at least $-1$. With terminal payoff 1, the continuous price is

$$
P_0=E\left[\exp\left(-\int_0^T r_t[1+g(t,T-t)]\,dt\right)\right].
$$

This formulation specifies discounted expectations under the given rate process; an arbitrary maturity-dependent choice of $g$ should not be presumed to define an arbitrage-free system of all bond prices. The paper refers that economic restriction to the term-structure literature. Its numerical experiment takes $g=0$, the local expectations hypothesis.

Theorem 5 augments the rate state with accumulated discounting $y$. Use $y_0=1$ and update

$$
y_{k+1}=y_k\exp\{-h r_k[1+g(kh,T-kh)]\}.
$$

The joint chain converges to the rate diffusion and the finite-variation process $dy=-yr[1+g(t,T-t)]dt$. Since $0\le y_T\le1$, expectations converge. The added state is a proof device; practical tree valuation can discount the two successor values recursively without retaining all path-specific accumulated discount factors as extra lattice states.

There is a finite-step discounting inconsistency to retain when replicating the paper. Equation (74) uses $[qP^++(1-q)P^-]/(1+r^*h)$, while equations (75)–(81) and the proof use exponential discounting. These are not identical finite-grid formulas. Both have the same continuous-time limit under the stated regularity, but a numerical reconstruction must record which one it uses. The appendix also prints $1-g$ in (A26)–(A27), whereas the main definitions and (A28) use $1+g$; the latter is consistent with the stated $r^*$. Because the reported experiment fixes $g=0$, that sign discrepancy does not explain its numerical errors.

## Numerical option experiment

Table 1 fixes initial stock price at \$40, rate at 5% annually, strikes at \$35, \$40, and \$45, and maturities at one and four months. Elasticities are $\gamma=0.5$ and $0.875$. The volatility coefficient is selected so that the initial instantaneous return volatility is $\sigma'=0.2,0.3,$ or $0.4$ per square-root year:

$$
\sigma\,40^\gamma=40\sigma',\qquad \sigma=\sigma'40^{1-\gamma}.
$$

Thus setting the CEV coefficient itself to 0.2 would be a different experiment. The tree uses $n=5$ or $50$ intervals. Square-root-model calls use an analytic benchmark quoted from Cox and Rubinstein. The other call benchmarks and all American-put benchmarks use an implicit finite-difference PDE calculation with half-day time spacing and a \$0.20 stock-price mesh.

For $\gamma=0.5$, $\sigma'=0.2$, strike \$40, the one-month call is 1.049 with five steps, 0.999 with 50, and 1.00 in the analytic reference. At four months the values are 2.249, 2.152, and 2.17. With $\sigma'=0.4$ and strike \$40, the four-month American put is 3.635 at five steps, 3.367 at 50, versus PDE 3.374. For $\gamma=0.875$, $\sigma'=0.3$, strike \$45, the four-month call is 1.280 at five steps, 1.238 at 50, versus PDE 1.225. All values are option prices in dollars per unit share, not percentages or errors.

The source describes typical 50-step accuracy for these short maturities as about \$0.01–\$0.02, while five-step results are coarse. Rounding of the analytic benchmark limits how precisely the smallest differences can be interpreted. The finite-difference comparator is itself numerical and is not accompanied by an independent mesh-convergence table. There are no sampling standard errors because these are deterministic numerical calculations.

A footnote reports a GAUSS implementation on a personal computer for an at-the-money four-month American put with $\sigma'=0.4$, $\gamma=0.875$. Runtime was 0.20 seconds at five steps, 2.22 seconds at 50, and 66.57 seconds at 200. The PDE calculation took 93.6 seconds and agreed with the 50-step tree within 0.1 cent. The authors explicitly caution against treating these timings or accuracy as representative of all parameter choices. Hardware specifications, full source code, interpolation details and PDE boundary placement are absent; code was available on request at publication.

## Numerical bond experiment and a material limitation

Table 2 prices a \$100 face-value discount bond. The long-run mean rate is 8%; initial rates are 5% and 11%; maturities are 1, 6, 12 and 60 months. The listed parameter sets include $(\kappa,\sigma)=(0.01,0.1),(0.1,0.1),(0.1,0.5),(0.5,0.5)$. Step counts are 5, 50, 100 and 200. The final column contains the analytic CIR benchmark. The model is not calibrated to a yield-curve dataset, and several parameter choices intentionally extend beyond the empirical range discussed in the cited literature.

At $(\kappa,\sigma)=(0.01,0.1)$, initial rate 5%, and one month, the prices are 99.5843 at five steps and 99.5841 at 50–200, matching the benchmark 99.5841 to displayed precision. At 60 months, the corresponding row is 78.7935, 78.3999, 78.3771, and 78.3665, against 78.3451. The 200-step absolute error is still \$0.0214. At $(0.1,0.1)$, initial 11%, 60 months, the sequence 61.6259, 60.5878, 60.5255, 60.4942 approaches the benchmark 60.4628 with a remaining error of \$0.0314.

High-volatility cases are much less reassuring. For $(0.1,0.5)$, initial 5%, 60 months, prices are 84.2543, 87.1194, 87.3946, and 87.4445 versus 83.4832. For $(0.5,0.5)$ at the same initial rate and maturity, they are 76.6883, 76.0322, 83.2037, and 86.9128 versus 74.8289. The last error is \$12.0839 per \$100 face value, approximately 16.15% of the benchmark, calculated from the printed table. For initial 11% in that latter parameter set, the 200-step value is 77.4502 versus 68.6361, an error of \$8.8141.

These rows are nonmonotone in the step count, and some move farther from the benchmark over the displayed range. They should not be summarized as uniformly successful convergence at 200 steps. A weak-convergence theorem is an asymptotic statement; it neither supplies an error bound at these grids nor verifies that every implementation detail in the reported calculation satisfies the construction. The paper does not diagnose these large discrepancies, give the code needed to isolate them, or tabulate much finer grids. Boundary rules, finite discounting conventions, and a separate convergence study therefore remain necessary for a faithful numerical implementation. It would be speculation to assign the table errors to one particular cause.

## Proof structure and replication boundaries

The appendix frames the chains as probability measures on right-continuous paths with left limits. Theorem 1 is an application of established diffusion-approximation results. Theorem 2 proves the local moment requirements by expanding the inverse map and observing that nonsingular volatility overwhelms finite drift on compact sets as $h$ shrinks. Theorem 3 treats the boundary separately: a nonnegative test function of negative states proves the limiting diffusion cannot cross below zero; outside a shrinking boundary neighborhood, ordinary nearest-neighbor expansions apply; inside it, the selected odd jumps remain sufficiently small and their local second moments converge to the vanishing diffusion variance.

Some printed intermediate equalities in those expansions are less reliable than the underlying inequalities. For instance, near (A18) the text invokes $|\mu(y,t)|\le C y$, which need not hold when $\mu(0,t)>0$, as in CIR. The needed one-sided bound is $\mu(y,t)\ge-Cy$, obtained from local Lipschitz continuity and nonnegative boundary drift. Likewise a bound on squared increments should be used as a bound, not promoted to an exact leading coefficient. The results summarized here retain the proof's sufficient inequalities and the explicit model assumptions rather than treating these shorthand lines as additional model restrictions.

To reconstruct a working tree, specify the target measure and drift first, then derive the transform and its piecewise inverse. Generate each transformed time slice, map states at that date, choose the admissible odd destinations, and distinguish physical mean matching from exact risk-neutral mean matching. Store successor indices and probabilities, apply terminal payoff, and recurse with the selected discounting convention and exercise rule. Check nonnegative probabilities, exact finite-step mean brackets, boundary behavior, and pricing error as grids refine. The source provides the mathematical ingredients, but its generality does not remove these implementation choices.

No return signal, train/test split, transaction-cost assumption, or inference about investment performance appears in the paper. Its contribution is a constructive numerical approximation and carefully delimited convergence argument. Its strongest practical lesson is that recombination, boundary fidelity, and pricing convergence are separate requirements that must all be checked.

## Source map

Printed pp. 396–402 state local convergence conditions and the inverse-volatility transformation; pp. 403–408 give the nonsingular and zero-boundary theorems; pp. 408–412 construct CEV and CIR examples and Figures 1–3. European option convergence, risk-neutral branches and Table 1 occupy pp. 413–418. Bond discounting, Theorem 5 and Table 2 occupy pp. 418–421. The appendix on pp. 422–429 supplies the path-space setup, Lyapunov criterion and proofs; references finish on p. 430. Cited antecedents include Cox–Ross–Rubinstein (1979), Stroock and Varadhan (1979), and CIR (1985), but these notes do not claim a separate reading of those references for this task.

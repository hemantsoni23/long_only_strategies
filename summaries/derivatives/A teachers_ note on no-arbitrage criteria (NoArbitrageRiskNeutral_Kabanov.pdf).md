# A teachers' note on no-arbitrage criteria

Yuri Kabanov and Christophe Stricker, *Séminaire de Probabilités* XXXV (2001), 149–152. Source: [NoArbitrageRiskNeutral_Kabanov.pdf](../../Finance/NoArbitrageRiskNeutral_Kabanov.pdf), five PDF pages including the archive cover. The cover catalog uses “A teacher's note”; the article heading uses the plural “teachers'”. The article itself occupies PDF pages 2–5.

## Why this matters

The Dalang–Morton–Willinger theorem equates no arbitrage in finite discrete time with the existence of an equivalent martingale measure. The difficult part on an infinite state space is not the statement but closure: limits of gains dominated by trading payoffs must still be dominated by attainable gains. Finite-state cone geometry does not automatically establish that fact on a general probability space.

This paper offers a concise proof built around a measurable subsequence lemma and elimination of redundant trading directions. It avoids a general measurable-selection theorem by choosing subsequences with random indices through elementary constructions. Its novelty is the proof method and teaching presentation, rather than a new pricing criterion or an empirical result.

The main reconstruction task is to understand how divergent sequences of positions can be reduced without changing their payoffs. Once closure is established, a positive bounded separator gives the martingale density through standard functional analysis. The proof is finite-dimensional in the number of assets and finite in trading dates, even though the state space can be arbitrary.

## Objects and four equivalent conditions

Let $(\Omega,\mathcal F,P)$ carry a finite filtration $(\mathcal F_t)_{t=0}^{T}$ with $\mathcal F_T=\mathcal F$. Prices $S_t\in\mathbb R^d$ are adapted and are interpreted in units of a traded numeraire. A predictable holding $H_t$ is $\mathcal F_{t-1}$ measurable, so it is chosen before $\Delta S_t=S_t-S_{t-1}$ is observed.

Define the terminal-gain space and the dominated-gain cone by

$$
R_T=\left\{\sum_{t=1}^{T}H_t^\top\Delta S_t:H\text{ predictable}\right\},
\qquad A_T=R_T-L^0_+.
$$

The subtraction permits disposal of a nonnegative payoff. Thus $A_T$ includes terminal claims that can be dominated by a zero-cost trading gain. Its closure in probability is $\overline A_T$. All equalities and inequalities between random variables are understood almost surely.

Theorem 1 states equivalence of:

1. $A_T\cap L^0_+=\{0\}$, the no-arbitrage condition.
2. The same condition together with $A_T=\overline A_T$.
3. $\overline A_T\cap L^0_+=\{0\}$.
4. There is $\widetilde P\sim P$, with $d\widetilde P/dP\in L^\infty$, under which $S$ is a martingale.

The first condition can equivalently be stated as $R_T\cap L^0_+=\{0\}$. If a gain dominates a nonzero positive claim, the gain itself is nonnegative and positive somewhere. The reverse implication follows because $R_T\subset A_T$.

The equivalence of the first three conditions is special to this finite-time finite-asset setting. It is not a general rule that an arbitrage-free cone in an arbitrary infinite-dimensional market is closed. The source notes that without NA, even the one-period dominated-gain cone can fail to be closed on an infinite state space. The gain space itself has a stronger closure property, but subtracting the positive cone introduces the real difficulty.

A bounded density is bounded above and positive almost surely; it need not be bounded below by a positive constant. Equivalence preserves null events, not probabilities or physical expected returns. The martingale property also includes price integrability under the new measure, which the proof arranges through a preliminary change of probability.

## Measurable subsequences without a selection theorem

Lemma 2 considers measurable vectors $\eta^n\in L^0(\mathbb R^d)$ with $\liminf_n\|\eta^n\|<\infty$ almost surely. It constructs measurable vectors $\widetilde\eta^k$ which, for each state, form a convergent subsequence of the original sequence. The selected indices depend on the state; this is not generally a single deterministic subsequence converging everywhere.

The construction first selects indices whose norms approach the finite lower limit, making the selected vectors pointwise bounded. It then repeats the same operation coordinate by coordinate: choose a subsequence whose first coordinate converges, then one whose second converges, and so forth. There are only finitely many coordinates. The first index satisfying a measurable inequality is a measurable integer-valued variable, so every selected vector retains the information measurability of the original sequence.

These random indices are devices for selecting holdings known at the current date. They do not represent trading stopping times or an ability to inspect future returns. In the one-step closure argument, all holdings and selection events are $\mathcal F_0$ measurable.

## One-period closure: bounded positions and redundant directions

Suppose $H_1^n\cdot\Delta S_1-r^n\to\zeta$ almost surely, with $H_1^n$ measurable at time zero and $r^n\geq0$. Passing from convergence in probability to an almost-surely converging subsequence is enough because that is the closure being proved.

Split the state space according to whether $\liminf_n\|H_1^n\|$ is finite. On the finite part, Lemma 2 selects convergent holdings. Their gains converge to the payoff of the limiting holding, and the residual disposal amount has a nonnegative limit. This gives a representation of $\zeta$ in $A_1$ on that part.

On the part where the norms diverge, normalize:

$$
G_1^n=\frac{H_1^n}{\|H_1^n\|},
\qquad h_1^n=\frac{r^n}{\|H_1^n\|}.
$$

The normalized dominated payoff tends to zero. The unit vectors have a measurably selected convergent subsequence with limit $\widetilde G_1$. Since the normalized disposal terms are nonnegative, the limit satisfies $\widetilde G_1^\top\Delta S_1\geq0$. NA forces this payoff to be zero. Its holding vector is nevertheless nonzero: it is a unit limit.

This is the key economic observation. The divergent positions point along a redundant direction that generates no payoff. On a measurable partition where coordinate $i$ of $\widetilde G_1$ is nonzero, subtract a suitable multiple of that direction:

$$
\overline H_1^n=H_1^n-\beta^n\widetilde G_1,
\qquad \beta^n=H_{1,i}^n/\widetilde G_{1,i}.
$$

The gain is unchanged because $\widetilde G_1^\top\Delta S_1=0$, while coordinate $i$ of the new holding is exactly zero. Repeat the bounded/divergent split on the reduced holding. Each pass eliminates another nonzero coordinate on the relevant measurable piece. With only $d$ assets, the process terminates after finitely many eliminations. One eventually obtains convergent effective holdings and hence a limiting representation of the dominated claim.

This is not an argument that every original sequence of positions is bounded. Positions can diverge along payoff-null directions. It proves that equivalent positions with the same gains can be selected to converge. Imposing an invertible covariance matrix would avoid redundancy but would unnecessarily exclude models covered by the theorem.

## Extending closure to several dates

The proof proceeds by induction in $T$. Begin with an almost-surely convergent sequence of terminal dominated gains. Apply the same elimination logic to the first-date positions. Future terms form a residual market with one fewer date, to which the induction hypothesis applies. This allows replacement of first-date positions by an equivalent sequence that converges, while keeping the remaining terminal claim within the appropriate dominated-gain class.

After the first position converges, subtract its limiting first increment. The remaining problem has $T-1$ periods. Repeating the argument establishes $A_T=\overline A_T$ under NA. The text presents this induction compactly, relying on the reader to track the information sigma-algebras and the finite measurable partitions. It does not supply a numerical algorithm or a complexity bound for performing these eliminations on an arbitrary probability space.

The finite horizon and finite asset dimension are used at different places: finite dimension ends coordinate elimination, and finite horizon ends the time induction. Neither can be silently replaced by a countably infinite version.

## Kreps–Yan separation and the martingale density

Lemma 3 is a separation result for a closed convex cone $K\subset L^1$ containing $-L^1_+$ and satisfying $K\cap L^1_+=\{0\}$. It yields an equivalent probability measure with bounded density whose expectation is nonpositive on $K$.

For each nonzero positive $x$, Hahn–Banach produces a bounded nonnegative separator $z_x$ with $E[z_xx]>0$ and $E[z_x\xi]\leq0$ for every $\xi\in K$. Nonnegativity follows because $K$ contains all negative variables. A single separator can vanish on a positive-probability set, so it may not define an equivalent measure.

The Halmos–Savage exhaustion argument selects a countable subfamily with the same common null sets as the full family. Normalize the separators to lie below one and form $\rho=\sum_i2^{-i}z_{x_i}$. This sum is bounded. If its zero set had positive probability, separating that set's indicator would contradict the common-null-set property. Thus $\rho>0$ almost surely, and its normalized version is the required density. The article also sketches how to prove the exhaustion step directly rather than treating it as an external theorem.

To apply this result, first change to an equivalent measure under which every price is integrable. For a finite family of finite random variables, exponential damping gives such a density bounded relative to the original measure. NA and convergence in probability are invariant under equivalence. Intersect the closed dominated-gain cone with $L^1$ and apply separation there.

For every bounded predictable test holding at date $t$, both signs of $H_t^\top\Delta S_t$ lie in the integrable gain space. Hence its expectation under the separating measure is zero. Using indicator holdings for each coordinate and every event in $\mathcal F_{t-1}$ yields

$$
E_{\widetilde P}[\Delta S_t\mid\mathcal F_{t-1}]=0.
$$

Bounded density preserves the integrability achieved by the preliminary tilt. This proves the martingale-measure condition. Closure and the trivial positive intersection then give the remaining easy implications among the theorem's conditions.

## The reverse implication needs a careful integrability reading

The source finishes by conditioning the stochastic integral and asserting its expectation is zero. For bounded predictable holdings and integrable prices this is immediate. For arbitrary finite but unbounded random holdings, the total gain need not be integrable, so a blanket ordinary-expectation identity is not justified merely by the martingale property of $S$.

The no-arbitrage conclusion remains correct. It can be obtained with localized conditional arguments for a nonnegative terminal gain and finite backward induction. A reproducer should either provide that argument or state suitable integrability restrictions when using the expectation shortcut. This qualification limits a sentence in the proof, not the finite-time theorem itself. It also explains why unrestricted gain-space elements should not automatically be used inside risk-neutral expectation formulas.

## Scope and practical interpretation

There are no market datasets, estimated parameters, simulations, transaction costs, or empirical performance claims. The work is reproducible as a proof: establish measurable subsequence selection, reduce divergent holdings through payoff-null directions, close the dominated-gain cone by induction, and construct the strictly positive bounded separator.

For a finite-state market, one can instead search for positive state probabilities satisfying the martingale equations with linear programming. Such a computation is a useful special case, but it omits the infinite-state closure problem this paper resolves. The theorem gives existence of a pricing measure, not uniqueness, complete-market replication, or a unique price for every contingent claim.

The main takeaway is precise: in a frictionless market with finitely many assets and dates, NA supplies enough hidden compactness to close the dominated-gain cone. Random-index selection and finite coordinate elimination make that mechanism visible without a general measurable-selection theorem. Extensions involving infinitely many dates, constraints, transaction costs, or continuous-time admissibility require additional results rather than a direct reuse of this proof.

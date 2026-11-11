# A Hilbert Space Proof of the Fundamental Theorem of Asset Pricing in Finite Discrete Time

Walter Schachermayer, manuscript dated October 1992. Source: [NoArbitrageRiskNeutral_Schachermayer_1992.pdf](../../Finance/NoArbitrageRiskNeutral_Schachermayer_1992.pdf), fifteen pages including the auxiliary proofs and references. This note summarizes the supplied manuscript rather than reconstructing a later typeset version from external bibliographic information.

## Why this matters

In finite discrete time with finitely many assets, no arbitrage already implies an equivalent martingale measure, even when the state space is infinite and original prices need not be integrable. The hard step is the closure of the cone of claims dominated by trading gains. Without that closure, a separating density cannot simply be assumed to exist.

The paper's innovation is a proof based on orthogonality in a suitable Hilbert space, followed by extensions to measurable holdings. It replaces the original theorem's heavier measurable-selection machinery with a projection onto payoff-relevant directions, convex combinations, and a positive separating functional. It also provides a concrete counterexample showing why finitely many securities is essential.

This is a theoretical contribution. No empirical strategy, calibration, risk-premium estimate, or option-pricing performance test is presented. Reproduction means following the proof dependencies and checking the topology, information constraints, and integrability at each step.

## Market and theorem

Let $S_0,\ldots,S_N$ be an adapted $\mathbb R^d$-valued discounted price process on a filtered probability space, with finite $N$ and $d$. The source initially defines no arbitrage one step at a time: for each $t$ and every bounded $\mathcal F_{t-1}$-measurable vector $h$,

$$
h^\top(S_t-S_{t-1})\geq0\quad\Longrightarrow\quad h^\top(S_t-S_{t-1})=0
$$

almost surely. Boundedness causes no loss for this sign test because a finite measurable holding can be divided by a positive measurable function of its norm.

Lemma 1.2 shows equivalence to global terminal-gain NA. Define

$$
K=\left\{\sum_{t=1}^{N}h_t^\top\Delta S_t:h_t\text{ is }\mathcal F_{t-1}\text{ measurable}\right\}.
$$

Then the condition is $K\cap L^0_+=\{0\}$. The proof uses finite backward induction. If a nonnegative final gain has a previous accumulated gain negative on an event known before the last trade, that last trade would provide a one-step arbitrage on that event. Otherwise the preceding gain is itself nonnegative and the induction hypothesis applies.

Theorem 1.1 states equivalence between NA and an equivalent probability $Q$ under which $S$ is an integrable martingale. The density $dQ/dP$ can be chosen uniformly bounded. Its strict positivity is almost sure, not a uniform positive lower bound. The easy direction uses bounded one-step holdings, whose gains are integrable under $Q$, and then Lemma 1.2. This formulation avoids claiming that every stochastic integral with unbounded holdings necessarily has an ordinary zero expectation.

## Key closure lemma and its significance

In a one-period model with increment $Y$ and time-zero information $\mathcal F_0$, write $K_Y=\{h^\top Y:h\in L^0(\mathcal F_0;\mathbb R^d)\}$. Lemma 2.1 states

$$
K_Y\cap L^0_+=\{0\}\quad\Longrightarrow\quad K_Y-L^0_+\text{ is closed in probability}.
$$

Stricker's lemma says the gain space $K_Y$ itself is closed even without NA. The stronger assertion for dominated gains requires NA. Section 2.3 illustrates the difference on $[0,1]$ with trivial initial information and $Y(\omega)=\omega$: the constant payoff one is not dominated by any fixed multiple of $Y$, yet the dominated-gain cone is dense in all $L^0$. For instance, $\min(nY,1)$ is dominated by $nY$ and converges almost surely to one except at the null point zero. This market has a nonnegative nonzero gain, so NA fails.

Lemma 2.4 reduces the key closure proof to bounded $Y$. Multiplication by the strictly positive random factor $\varphi=\min(\|Y\|^{-1},1)$, with the natural value one at $Y=0$, is an order-preserving homeomorphism of $L^0$. Although the inverse multiplier need not be bounded, both multiplications preserve convergence in probability for finite random variables. Thus scaling payoffs preserves NA and the closure question. This is an auxiliary analytical transformation, not a claim that the multiplier is known at trading time or itself a traded return.

## Hilbert projection onto effective holdings

For bounded $Y$, define the payoff-null module

$$
\mathcal N=\{k\in L^0(\mathcal F_0;\mathbb R^d):k^\top Y=0\},
$$

and its pointwise orthogonal complement

$$
\mathcal N^\perp=\{h:k^\top h=0\text{ a.s. for every }k\in\mathcal N\}.
$$

The term module indicates closure under multiplication by scalar $\mathcal F_0$-measurable variables. It is stronger than merely a linear subspace under deterministic coefficients.

Lemma 2.5 first works in the Hilbert space $H=L^2(\mathcal F_0;\mathbb R^d)$. The intersections of the two modules with $H$ form an orthogonal decomposition. If a vector orthogonal in expectation to every square-integrable null holding were not pointwise orthogonal, localizing to an event where its inner product with a null holding is positive and normalizing that holding would contradict Hilbert orthogonality.

The ordinary $L^2$ orthogonal projection extends to a continuous projection $\pi$ on $L^0$, using measurable scalar normalization and the module property. Its kernel is $\mathcal N$, its range is $\mathcal N^\perp$, and

$$
h^\top Y=\pi(h)^\top Y.
$$

Thus redundant positions can be removed without changing payoffs. No invertibility of a covariance matrix is assumed. The proof's main compactness control applies to projected holdings, not to every original representation of a gain.

## Uniform positivity on an event

Let $\Omega_{\mathcal N}=\{E[\|Y\|\mid\mathcal F_0]=0\}$, the event where every payoff direction vanishes. On its complement, the projection of coordinate unit vectors supplies measurable effective directions of unit length. For a positive-probability time-zero event $A$ in that complement, Lemma 2.6 defines an infimum of expected positive gains over effective unit holdings on $A$ and proves that this infimum is strictly positive.

The proof is delicate because ordinary averaging can cancel unit vectors to zero. Suppose unit effective holdings had expected positive payoffs tending to zero. If negative payoffs did not also vanish, convex compactness would yield a nonzero one-sided gain, contradicting NA. If both signs vanish, a second lemma multiplies holdings by bounded measurable signs before taking convex averages, ensuring a nonzero limit. That limit would simultaneously lie in the payoff-null module and its orthogonal complement, which is impossible.

Lemma 3.3 supplies the nonzero-limit device. A bounded $L^2$ sequence staying away from zero in probability has some coordinate with nonvanishing expected absolute size. Multiply by the sign of that coordinate and select convex averages converging to a vector with positive expectation in that coordinate. This explains why a naive compactness argument without sign adjustment would be insufficient; ordinary Rademacher averages can converge to zero.

## Bounded effective holdings and closure

Lemma 2.7 shows that a pointwise upper bound on positive payoffs of effective holdings forces their norms to be pointwise bounded. If norms were unbounded on a positive-probability event, select holdings crossing successively larger thresholds and normalize to unit length. Their positive payoffs would tend to zero by the assumed envelope, contradicting the preceding strict-positivity result.

Now take a converging dominated-gain sequence $h_n^\top Y-k_n\to f$, with $k_n\geq0$. Pass to an almost-surely convergent subsequence and replace holdings by $\pi(h_n)$. The convergent dominated gains bound the **negative** parts of $h_n^\top Y$. Apply the boundedness lemma to $-h_n$, which is also an effective holding, to obtain a finite random bound on $\|h_n\|$.

Lemma 3.2 gives almost-surely convergent tail convex combinations of any pointwise bounded finite-dimensional random-vector sequence. Its proof normalizes by the random envelope, uses weak compactness in $L^2$, passes to norm-convergent convex averages, and selects an almost-surely convergent subsequence. Applying the same averages to the dominated payoffs preserves their limit $f$. The limiting holding $h$ therefore satisfies $h^\top Y\geq f$, establishing the key closure lemma.

The source's final closure paragraph references Lemma 2.6 where the immediate boundedness step is Lemma 2.7; the sign application is also compressed. Keeping the negative-part bound and the use of $-h_n$ explicit prevents a mistaken inference that $h_n^\top Y-k_n\to f$ controls the positive gain parts directly.

## Constructing the martingale measure

For original one-step prices, use the auxiliary bounded increment

$$
Y=\frac{S_1-S_0}{w},\qquad w=\max(\|S_0\|,\|S_1\|,1).
$$

After closure, intersect $K_Y-L^0_+$ with $L^1$. It is a norm-closed convex cone containing all negative integrable variables and no nonzero positive one. Yan's theorem yields a bounded strictly positive separator $g$ whose integral against the cone is nonpositive. Both signs of bounded-holding gains lie in the cone, so their integrals against $g$ are zero.

Define $dQ/dP=cg/w$ with normalizing constant $c$. The denominator makes $S_0$ and $S_1$ integrable because $\|S_t\|/w\leq1$; it also keeps the density bounded. Testing with bounded $\mathcal F_0$-measurable holdings proves $E_Q[S_1-S_0\mid\mathcal F_0]=0$.

Section 3.1 proves Yan's theorem through Hahn–Banach separation followed by exhaustion of supports. Individual nonnegative separators may vanish somewhere. Summable positive combinations attain a maximal support; a remaining positive-probability zero set could itself be separated, contradicting maximality. The resulting separator is positive almost surely, giving equivalence rather than only absolute continuity.

For multiple periods, first choose a bounded density making dates one through $N$ a martingale. Then tilt by a bounded $\mathcal F_1$-measurable density fixing the first step. Such an early-information tilt preserves later martingale conditional means. The finite product remains bounded, completing induction. Preservation of integrability uses the boundedness of these factors; a general unbounded early-information tilt would need an extra integrability check.

## Why finite asset dimension matters

Remark 2.8 constructs a one-period market with countably many securities on $\Omega=\mathbb N$, with $P(\{n\})=2^{-n}$ and trivial initial information. Security $j$ starts at zero and pays one in state $j$, minus one in state $j+1$, and zero elsewhere.

Every finite-support portfolio has no nonzero nonnegative payoff. Its state-payoff sequence telescopes; if all entries were nonnegative, the finite sum of entries being zero forces every entry to be zero. Thus there is no arbitrage among finite-support holdings.

A martingale measure would require $Q(\{j\})=Q(\{j+1\})$ for every $j$. Strictly positive equal masses cannot sum to one on the positive integers. Hence no equivalent martingale probability exists. The example cleanly separates ordinary NA from stronger asymptotic conditions needed in large markets. It is not a counterexample to the finite-dimensional theorem.

## Reproduction scope and interpretation

The full reconstruction consists of the effective-holding projection, the two convex-compactness lemmas, strict positivity on nondegenerate events, the dominated-gain closure, Yan separation, and finite-horizon measure tilting. The paper includes the necessary auxiliary proofs, so its principal methodological inputs are present rather than hidden in empirical defaults.

The result licenses an equivalent martingale representation under its assumptions. It does not establish uniqueness of that measure, market completeness, or a single risk-neutral value for every unreplicated payoff. Prices are already discounted, bounded density is only an upper bound, and the horizon and security dimension must remain finite. These qualifications explain both the strength of the theorem for unbounded original prices and the limits illustrated by the infinite-security counterexample.

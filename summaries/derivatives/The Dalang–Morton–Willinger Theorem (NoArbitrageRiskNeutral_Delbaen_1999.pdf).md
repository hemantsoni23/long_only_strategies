# The Dalang–Morton–Willinger Theorem

Freddy Delbaen, didactical note dated April 14, 1999. Source: [NoArbitrageRiskNeutral_Delbaen_1999.pdf](../../Finance/NoArbitrageRiskNeutral_Delbaen_1999.pdf), thirteen pages, including references. The author explicitly states that this is a teaching note rather than a journal submission.

## Why this matters

In a finite number of trading dates, absence of arbitrage is equivalent to the existence of an equivalent probability measure under which discounted security prices are martingales. The state space need not be finite, and prices need not be bounded under the original probability. This theorem provides a foundation for risk-neutral valuation while exposing the topological work hidden by elementary finite-state linear programming arguments.

Delbaen's contribution is pedagogical. He proves the measure-theoretic and closure results needed for two approaches to the theorem: a separation argument associated with Schachermayer and an exponential-minimization argument associated with Rogers. The theorem is not new here. The note's distinctive content is the chain of intermediate lemmas, including a measurable projection onto effective trading directions and an elementary convex-compactness construction.

The result concerns frictionless finite discrete time. It neither makes the martingale measure unique nor extends unchanged to infinitely many dates, continuous-time doubling strategies, transaction costs, or portfolio constraints. The same theorem appears in other works, but this note is a separate exposition with its own proof structure.

## Market, strategies, and exact statement

Work on $(\Omega,\mathcal F_T,P)$ with a finite filtration $\mathcal F_0\subset\cdots\subset\mathcal F_T$. The adapted price vector $S_t$ is finite-valued in $\mathbb R^d$ at each date. Financial interpretation takes prices in units of a traded numeraire; the numeraire has constant discounted price one.

A strategy chooses $\alpha_t\in\mathbb R^d$ using $\mathcal F_t$ information, before the increment $S_{t+1}-S_t$. Its zero-initial-cost trading gain is

$$
G_T(\alpha)=\sum_{t=0}^{T-1}\alpha_t^\top(S_{t+1}-S_t).
$$

Let $K$ be the vector space of all these gains in $L^0$, identifying variables equal almost surely. Holdings are finite random vectors but need not be uniformly bounded. The no-arbitrage condition is

$$
K\cap L^0_+=\{0\}.
$$

Thus a gain nonnegative almost surely must be zero almost surely. An arbitrage has no initial cost, never loses, and gains strictly with positive probability. This is not a statement about positive expected returns under the physical measure.

Theorem 2.2 states that NA holds if and only if there is $Q\sim P$ such that every $S_t$ is integrable under $Q$ and

$$
E_Q[S_{t+1}\mid\mathcal F_t]=S_t.
$$

Moreover, the density $dQ/dP$ may be chosen in $L^\infty$. Equivalence means the density is strictly positive almost surely, so $P$ and $Q$ agree on null events. Boundedness above does not mean bounded away from zero, and the inverse density need not be bounded. Integrability under $Q$ is part of the conclusion, not an unspoken assumption under $P$.

There is an integrability shortcut in the source's easy direction: it says $E_Qf=0$ for every $f\in K$. With unrestricted random holdings, some gains need not be integrable, so that sentence is too broad literally. For example, in one period take a known-at-time-zero heavy-tailed finite holding independent of a symmetric bounded price increment. Their product can fail to have an ordinary expectation even though the price is a martingale. The no-arbitrage implication remains valid; it uses localization/conditional arguments for a nonnegative terminal gain rather than a blanket expectation identity for every element of $K$. Bounded predictable test strategies, used in the converse proof, do have the required integrability.

## Reducing the horizon to one step

Section 3 proves that the one-step result implies the finite-horizon theorem by induction. Suppose an equivalent measure $Q_1$ with bounded density already makes $(S_1,\ldots,S_T)$ a martingale. Apply the one-step theorem to $(S_0,S_1)$ under $Q_1$ to obtain an additional bounded, strictly positive density factor that is $\mathcal F_1$ measurable.

Tilting by an $\mathcal F_1$-measurable factor preserves the martingale property for later dates: that factor is already measurable at every $\mathcal F_t$ for $t\geq1$ and cancels in conditional expectations. The new factor fixes the first increment. The product of the bounded density factors remains bounded because the horizon is finite.

For one step, write $X=S_1-S_0$. It suffices first to find an equivalent measure making $X$ integrable with conditional mean zero given $\mathcal F_0$. An additional $\mathcal F_0$-measurable tilt proportional to $e^{-\|S_0\|}$ makes $S_0$ integrable without changing that conditional zero mean. Then $S_1=S_0+X$ is also integrable. This separates the integrability of initial prices from the core martingale-increment problem.

## Effective directions and measurable projection

One-step gains have the form $\alpha^\top X$, with $\alpha$ measurable at time zero. Distinct holdings can generate exactly the same payoff when some directions of $X$ are redundant. Sequences of holdings may therefore diverge even when their gains converge. The projection construction removes those irrelevant directions.

After an equivalent probability change making $X$ square integrable, define

$$
B=E[XX^\top\mid\mathcal F_0].
$$

This random symmetric matrix is positive semidefinite. Positivity can be established simultaneously outside a single null set by checking rational vectors and using continuity. Let $\Pi$ be the orthogonal projection onto its range. Lemma 4.3 gives a measurable representation,

$$
\Pi=\int_0^\infty Be^{-\lambda B}\,d\lambda.
$$

For a scalar eigenvalue $b>0$, the integral is one; for $b=0$, it is zero. Hence the formula indeed projects onto the positive-eigenvalue subspace without requiring a measurably selected eigenbasis.

The resulting projection is unchanged by switching to another equivalent probability measure under which the relevant moments exist. Its range reflects possible payoff directions conditional on current information, not the particular probability weights assigned to them. Lemma 4.11 establishes

$$
\alpha^\top X=(\Pi\alpha)^\top X,
$$

and, for sequences of time-zero-measurable holdings,

$$
\alpha_n^\top X\xrightarrow{P}0
\quad\Longleftrightarrow\quad
\Pi\alpha_n\xrightarrow{P}0.
$$

This is the central finite-dimensional control. It converts convergence of payoffs into convergence of economically effective holdings. The proof uses subsequences and equivalent measures to make a dominating payoff bound square integrable, then applies the positive quadratic form of the conditional matrix. The matrix may be singular; replacing it by an assumed invertible covariance would miss the point.

A consequence is Stricker's lemma: the one-step gain space $K=\{\alpha^\top X\}$ is closed for convergence in probability. If gains form a Cauchy sequence, their projected holdings do too. The limit of projected holdings remains $\mathcal F_0$ measurable and generates the limit payoff. This closure of $K$ alone is not yet the closure of $K-L^0_+$ required for separation.

## Auxiliary probability and convexity tools

Lemma 4.10 constructs an equivalent measure with bounded density that gives every member of a countable family of finite nonnegative random variables all exponential moments. Choose small constants $\varepsilon_n$ so that $P(\varepsilon_nf_n\geq1)\leq2^{-n}$, set $h=\sup_n\varepsilon_nf_n$, and use density proportional to $e^{-h^2}$. Borel–Cantelli makes $h$ finite almost surely, and completing the square controls the desired exponential integrals. This is an integrability device, not a market calibration.

The next lemmas prevent positive mass from disappearing under convex averages. If each nonnegative $f_i$ exceeds $c$ with probability at least $\delta$, any convex combination exceeds $c\delta/2$ with probability at least $\delta/4$. A conditional-expectation version has the weaker constants $c\delta^2/16$ and $\delta/16$. The exact constants are sufficient bounds; they are not optimized financial risk parameters.

Lemma 4.18 gives a compactness substitute. If the convex hull of nonnegative variables $(f_n)$ is bounded in probability, there exist tail convex combinations $g_n\in\operatorname{conv}\{f_m:m\geq n\}$ converging in probability. The proof nearly maximizes $E[1-e^{-g}]$ over successive tail convex hulls. Strict concavity forces two near-maximizers to be close on sets where they are bounded; boundedness in probability controls the complement. Thus the selected combinations are Cauchy in probability.

Nonnegativity is essential to this version. The note uses independent Cauchy variables as a counterexample to dropping it: every convex average has the same Cauchy law, while a tail-measurable probability limit would be degenerate by the zero-one law. For a sequence dominated in absolute value by a finite random variable, one can add the bound to make it nonnegative and recover convergent convex combinations. The note also states stronger Komlós-type results, while explicitly saying they are not needed for the final proofs.

## From no arbitrage to closure of dominated gains

Theorem 5.1 is the topological expression of one-step NA:

$$
(\alpha_n^\top X)^-\xrightarrow{P}0
\quad\Longrightarrow\quad
(\alpha_n^\top X)^+\xrightarrow{P}0.
$$

An approximately vanishing loss cannot coexist with a persistently positive gain probability. The proof first projects the holdings into effective directions. On any event where holdings become unbounded, it normalizes a suitably selected sequence to unit size. Elsewhere, it leaves the bounded sequence intact. Negative payoffs still vanish, while the normalized holdings are bounded pointwise.

If positive payoffs remained bounded away from zero in probability, the convex mass lemma would preserve positive mass through tail averages. Convex compactness would then produce a limiting measurable holding with nonnegative payoff and a positive chance of strict gain, contradicting NA. This forces the normalized gains, and hence effective holdings, to vanish. Unit normalization on the alleged unbounded event gives a contradiction, completing the argument.

Theorem 5.8 derives a related boundedness statement: boundedness in probability of one sign of a family of gains implies boundedness of the other sign under NA. Applying Theorem 5.1 to negated and rescaled positions gives the result. Both signs and projected holdings are then controlled.

Theorem 5.9 finally proves that

$$
C=K-L^0_+
$$

is closed in probability under NA. For a sequence $f_n=\alpha_n^\top X-h_n\to f$ with $h_n\geq0$, pass to an almost-surely convergent subsequence. The negative parts of the gains are bounded by a finite random envelope derived from $f_n^-$. The preceding boundedness theorem controls the other side. Convex compactness produces converging gain averages; Stricker's lemma represents their limit as a gain. Applying the same averages to $h_n$ leaves a nonnegative limit, so $f$ still belongs to $K-L^0_+$. This is the closure needed to separate affordable dominated claims from positive claims.

## Separation proof

Yan's separation theorem, proved in Section 5, states that a closed convex cone $G\subset L^1$ containing $-L^1_+$ and satisfying $G\cap L^1_+=\{0\}$ has a strictly positive bounded separator $h$ with $E[hg]\leq0$ for all $g\in G$.

The proof separates $G$ from weakly compact sets of bounded nonnegative variables with expectation at least $1/n$. Each separator is nonnegative because $G$ contains all negative variables. Scaling their sup norms to a summable sequence and adding them produces a bounded separator that is positive almost surely. This exhaustion step upgrades nonnegative separating densities to an equivalent measure rather than merely an absolutely continuous one.

Section 6 first changes measure so that $X$ is integrable. Take $G=L^1\cap(K-L^0_+)$. Probability closure implies $L^1$ closure, and NA provides the required trivial intersection with the positive cone. The separator $\varphi$ has zero expectation against every integrable gain because gains form a vector space: both $f$ and $-f$ are admissible test elements. Normalize $\varphi$ into a probability density.

Testing the resulting measure with $1_AX_i$ for all $A\in\mathcal F_0$ gives $E_Q[X\mid\mathcal F_0]=0$. Bounded density preserves integrability through the successive measure changes. This finishes the one-step theorem and, by the earlier induction, the finite-horizon theorem.

## Rogers' exponential-minimization proof

Section 7 starts with a different preliminary measure, $dQ/dP$ proportional to $e^{-\|X\|^2}$, so $X$ has sufficiently strong exponential integrability. Minimize

$$
\phi(\alpha)=E_Q[e^{\alpha^\top X}]
$$

over $\mathcal F_0$-measurable holdings. Since $\phi(0)=1$, the infimum is finite. The hard step is showing attainment. The bound $x^+\leq e^x$ controls positive gain parts along near-minimizers; NA and the preceding lemmas control the negative parts and give convergent tail convex combinations. Stricker's lemma represents the limit by a holding $\delta$, and Fatou's lemma proves that it minimizes $\phi$.

Differentiate along bounded, localized perturbations $\delta+\varepsilon e_i1_{A\cap\{\|\delta\|<n\}}$. Integrability justifies differentiation and yields

$$
E_Q[e^{\delta^\top X}X_i1_{A\cap\{\|\delta\|<n\}}]=0.
$$

The exponential tilt alone need not produce the bounded density and integrable increments required by the theorem. The source therefore constructs a weighted sum over shells $n-1\leq\|\delta\|<n$, dividing by normalizers $k_n$ and adding damping $e^{-n^2/4}$. The result $\psi$ is strictly positive, makes $\psi X$ integrable, and preserves every localized zero-mean identity. Multiplication by the initial Gaussian-damping density is bounded because

$$
e^{n\|X\|-n^2/4-\|X\|^2}=e^{-(\|X\|-n/2)^2}\leq1.
$$

Normalizing the product gives the desired equivalent martingale measure with bounded density. Omitting the shell weights would turn the proof into an unjustified simple Esscher-transform claim.

## What can be reproduced and what is not claimed

This is a proof-based work with no datasets, empirical estimates, trading returns, or parameter selection. Reproduction means reconstructing its measurable projection, compactness, NA closure, and either density construction under the stated assumptions. A finite-state implementation could find a positive martingale probability by linear feasibility, but that computational shortcut does not reproduce the general-state-space proof.

The financial conclusion is existence of an equivalent martingale measure, not uniqueness or completeness. A replicated integrable claim has its price pinned down consistently by martingale valuation; unreplicated claims can admit multiple arbitrage-free valuations. Additional payoff integrability and strategy conditions must be stated before using unconditional expectations. The bounded-density conclusion also does not license infinite-horizon or continuous-time limits without new admissibility and closure arguments.

The note's main value is showing why the theorem survives unbounded prices and arbitrary state spaces at a finite horizon. It does so by controlling effective holdings, closing the cone of dominated gains, and constructing a strictly positive density with the necessary integrability, rather than assuming these analytic properties from the start.

# The Recovery Theorem

**Steve Ross.** *The Journal of Finance* 70(2), April 2015, pp. 615–648. DOI: 10.1111/jofi.12092. [Source PDF](../../Finance/StochasticDiscountRecovery_Ross_2015.pdf). This note covers all 34 supplied pages, including the proof arguments, numerical examples, and references; this version has no separate technical appendix. PDF page 1 is journal page 615.

## Why this matters

Option prices reveal how the market prices different outcomes, but a high price for crash insurance can reflect either a high perceived crash probability or a large compensation for bearing crash risk. Ross provides conditions under which those two components can be separated. With a finite Markov state space, a transition-independent pricing kernel, and a known matrix of conditional state prices, the natural probability transition matrix and the pricing kernel follow from a positive eigenvalue problem.

The result is an identification theorem, not an assumption-free extraction of objective probabilities from a current option smile. Its most important input is the entire matrix of prices conditional on every possible starting state. Ordinary options reveal distributions from today's state at various maturities. Recovering the unobserved conditional rows from those marginals is a separate and potentially unstable inverse problem. The paper's numerical application estimates those rows and illustrates both the potential and the fragility of the procedure.

For an investment researcher, the theorem offers a way to formulate forward-looking return distributions, risk premiums, and tail probabilities without first estimating historical return probabilities or imposing a specific risk-aversion coefficient. It also makes clear what must replace those inputs: strong restrictions on the state description and intertemporal kernel, a sufficiently informative transition-price system, and reliable recovery of that system from derivative prices. The paper's own unbounded lognormal example shows that the familiar inability to identify expected returns from options survives when those restrictions do not identify a unique positive eigenfunction.

## What is observed and what is to be recovered

Let $i$ denote the current state and $j$ next period's state. A state must include enough information to describe future evolution: the asset price may be one component, with volatility or other variables added when needed. The process is Markov and time homogeneous, so transition probabilities and prices depend on the state pair and time interval, not calendar time separately.

Write $p_{ij}$ for today's price in state $i$ of a claim paying one unit of currency next period only in state $j$. In a finite state space with $m$ states, collect these prices in $P\in\mathbb R^{m\times m}$. For a payoff vector $g$, its state-$i$ value is

$$
V_i(g)=\sum_{j=1}^m p_{ij}g_j.
$$

No arbitrage gives positive state prices on possible events; impossible transitions can have zero prices. In complete markets the state-price system is unique. In incomplete markets, choosing one compatible state-price system introduces an additional identification issue before recovery even begins.

The one-period riskless discount factor in state $i$ is

$$
b_i=\sum_j p_{ij}.
$$

Normalizing the row gives the risk-neutral transition probabilities $q_{ij}=p_{ij}/b_i$. The matrix $P$ itself is not a probability matrix, and its rows must not automatically be renormalized before applying the theorem. Differences in row sums carry information that becomes central to identification. In particular, a discount factor can exceed one when the corresponding interest rate is negative.

Let $f_{ij}$ be natural probabilities and $\phi_{ij}$ the pricing kernel, or stochastic discount factor, on the transition. The basic relation is

$$
p_{ij}=\phi_{ij}f_{ij},\qquad \sum_j f_{ij}=1.
$$

“Natural” in the paper means the actual distribution or the relevant subjective distribution. Recovering a distribution consistent with market prices and the maintained assumptions does not prove that market beliefs are objectively correct. The distinction is indispensable when interpreting a recovered crash probability as a forecast.

Without a restriction linking kernels across states, the factorization is underidentified. Any admissible positive row probability vector can be paired with an appropriate $p_{ij}/f_{ij}$. The theorem does not overturn this elementary nonuniqueness; it introduces a particular intertemporal structure that removes it in the finite irreducible setting.

## Transition independence and its economic content

The defining restriction is the existence of a positive state function $h$ and a positive scalar $\delta$ such that

$$
\phi_{ij}=\delta\frac{h_j}{h_i}.
$$

Ross calls this transition independence. The kernel depends on the destination state, with origin-state dependence only through the reciprocal normalization. It is a substantive condition on the stochastic discount factor, not a consequence of no arbitrage or Markov dynamics alone.

A motivating complete-markets representative-agent problem has increasing state-independent utility $U$, an intertemporally additive objective, a constant subjective discount factor $\delta$, state-dependent consumption $c_j$, and wealth $w$. Over the relevant pair of periods, the objective and budget are

$$
\max_{c_i,\{c_j\}}
\left[U(c_i)+\delta\sum_j f_{ij}U(c_j)\right],
\qquad
c_i+\sum_jp_{ij}c_j=w.
$$

The interior first-order conditions imply

$$
\phi_{ij}=\delta\frac{U'(c_j)}{U'(c_i)},
$$

so $h_j=U'(c_j)$. An economic interpretation in terms of marginal utility is useful, but the matrix proof only requires a positive $h$. It does not estimate a complete utility function or prove that a representative agent exists for arbitrary observed prices. The source also mentions recursive preferences as a possible motivation; a proposed preference model must still be checked against the exact kernel restriction rather than assumed to satisfy it by its name.

Over a realized path $i_0,i_1,\ldots,i_T$, the product of one-period kernels telescopes:

$$
\prod_{t=0}^{T-1}\phi_{i_ti_{t+1}}
=\delta^T\frac{h_{i_T}}{h_{i_0}}.
$$

Thus paths with the same endpoints and horizon have the same cumulative kernel. This is the mechanism behind the identifying power. In a more general discount-factor process, an additional path-dependent component could change valuation without being captured by a ratio of endpoint functions.

The source projects the kernel onto the filtration generated by the asset price. Such a projected object can be useful for claims measurable in that information set, but the required transition independence and Markov sufficiency still have to hold on the reduced state space. Merely omitting volatility from the state does not establish those properties. Nor must $h$ decline with the stock price: decreasing marginal utility in consumption only translates into decreasing $h$ in the asset price when the relationship between consumption and the asset state justifies it.

## The finite-state Recovery Theorem

Normalize $h$ at a reference state, for example $h_1=1$, and let $D=\operatorname{diag}(h_1,\ldots,h_m)$. The state-price equations become

$$
DP=\delta FD,
\qquad
F=\frac1\delta DPD^{-1}.
$$

Because $F$ must be stochastic, with $e$ the vector of ones,

$$
Fe=e.
$$

Substituting the previous relation and setting $z=D^{-1}e$ yields

$$
Pz=\delta z.
$$

The unknown inverse kernel is therefore a positive right eigenvector of the observable pricing matrix. Theorem 1 assumes no arbitrage, an irreducible nonnegative $P$, and generation by a transition-independent kernel. Irreducibility means that every state can be reached from every other state along some path with positive transition prices; it does not require every one-period entry to be positive. Aperiodicity is not needed to identify the positive Perron eigenvector.

Perron–Frobenius gives a positive eigenvalue $\lambda=\rho(P)$ and an associated strictly positive right eigenvector $z$, unique up to multiplication by a scalar. After fixing its normalization, the recovery is

$$
\delta=\lambda,\qquad h_i=\frac1{z_i},
$$

$$
f_{ij}=\frac{p_{ij}z_j}{\lambda z_i},
\qquad
\phi_{ij}=\lambda\frac{z_i}{z_j}.
$$

One can verify the probability constraint directly:

$$
\sum_j f_{ij}
=\frac{(Pz)_i}{\lambda z_i}=1.
$$

Nonnegativity is inherited from $P$, and the formula exactly reproduces $p_{ij}=\phi_{ij}f_{ij}$. A scalar rescaling of $z$ changes neither $F$ nor the transition kernel. The object recovered uniquely is the kernel ratio, not an absolute marginal-utility level.

The proof's existence argument uses the maintained data-generating representation. Its uniqueness comes from the unique positive eigenvector, not from counting equations alone. A singular matrix can satisfy this finite-state theorem: irreducibility, rather than full rank, is its relevant condition. This matters when comparing it with the separate multinomial theorem, whose local matrix construction needs invertibility.

An implementable exact-matrix algorithm is short: verify nonnegativity and communicating classes; compute the Perron eigenpair; choose a reference-state normalization; form the ratios above; verify row sums, reconstructed state prices, and positivity. Numerical stability is a separate issue. Entries close to zero, weakly connected state groups, or perturbations from option smoothing can change the recovered eigenvector even when an exact positive solution remains mathematically unique.

The eigenvalue is a discount *factor*, despite the paper sometimes calling it a discount rate. Positivity alone does not force it below one. An additional economic restriction that subjective discounting be less than one must be checked after estimation. Corollary 1 bounds $\delta$ above by the largest row sum of $P$, that is, the largest riskless discount factor. The usual Perron row-sum bounds also clarify that the scale of the fitted state prices affects the recovered discount factor.

## Constant interest rates and stochastic dominance

Theorem 2 produces an initially surprising implication. If the riskless discount factor is the same $b$ in every state, then

$$
Pe=be.
$$

By uniqueness of the positive eigenvector, $z$ is proportional to $e$. Consequently $h$ is constant, $\delta=b$, and

$$
F=\frac1bP=Q.
$$

Under these finite irreducible and transition-independent assumptions, natural and risk-neutral probabilities coincide. This is not a universal claim that constant interest rates eliminate risk premiums. It illustrates how strong the combined assumptions are, and why mechanically forcing all row sums to a common observed discount factor can force risk-neutral recovery. Infinite-state growth models avoid this conclusion precisely because positive-eigenfunction uniqueness need not hold there.

Theorem 3 concerns consumption rather than an arbitrary stock-price ranking. If marginal utility declines with consumption, then for a fixed starting state

$$
\frac{q_{ij}}{f_{ij}}=\frac{\phi_{ij}}{b_i}
=\frac{\delta}{b_i}\frac{U'(c_j)}{U'(c_i)}
$$

declines with $c_j$. Since both distributions integrate to one, their densities cross once: risk-neutral probability puts relatively more weight on low consumption. The natural consumption distribution first-order stochastically dominates the risk-neutral one under this ordering. In a one-period economy where terminal market wealth is consumed, that gives a positive expected market risk premium under the appropriate strictness conditions. It does not establish that every risky asset, or every multiperiod stock state, has a positive premium.

Bounded asset-price grids also require economically consistent carrying costs and dividends. A lowest or highest price node must not be interpreted as a free opportunity to exploit a sure one-sided price movement while ignoring the financing and payout terms. Ross notes that an equilibrium with positive state prices and exogenous consumption handles this accounting.

## Multinomial recovery: what additional information identifies the kernel?

Section III treats an unbounded tree without simply truncating its state space. An exogenous productive tree has height $H$ and pays consumed dividends $kH$. A discrete regime $i$ determines probabilities of next height $a_jH$. Consumption at the current height depends only on $H$, while the regime affects growth. The stock value is $S(i,H)$ and need not equal height or consumption.

At a fixed height, normalize current marginal utility and define $d_j=U'(ka_jH)/U'(kH)$. The local conditional pricing equations have the form

$$
p_{ij}(H)=\delta f_{ij}d_j,
\qquad P(H)=\delta FD,
$$

where $D=\operatorname{diag}(d_j)$. Unlike the finite-state formula, there is no left-hand $D$ here because the rows compare regimes at the same current consumption. Row normalization gives

$$
P(H)D^{-1}e=\delta e.
$$

When this local matrix is full rank,

$$
\frac1\delta D^{-1}e=P(H)^{-1}e.
$$

Writing $v=P(H)^{-1}e$, the products $\delta d_j=1/v_j$ and probabilities $f_{ij}=p_{ij}v_j$ are identified. Positivity of $v$ is needed for an economically valid solution and follows under the assumed generating model; full rank of an arbitrary observed matrix alone does not guarantee it. This step identifies the discounted kernel products, not yet $\delta$ and $d_j$ separately.

Recombination supplies extra information. In the illustrative binomial case, growth multipliers satisfy $ab=1$. An up move to $aH$ followed by a return to $H$ has the reverse marginal-utility ratio. If $p_{ab}(aH)$ and $f_{ab}$ are known, then

$$
p_{ab}(aH)=\delta\frac1{d_a}f_{ab}.
$$

Combining this with the recovered product $\delta d_a$ identifies $\delta^2$, after which positive $\delta$ and $d_a$ follow. The needed conditional price may come from contingent forward claims or appropriately identified path prices. Ordinary terminal claims need not distinguish all paths that recombine, so the availability of those extra prices is part of the identifying problem.

The paper also uses the two-step return price. Let $f_{aa}$ be the probability of staying in the up regime and $f_{bb}$ that of staying in the down regime. For the stated two-step structure, Eq. (41) is

$$
p_{a\cdot1}=\delta^2(1-f_{aa})(1+f_{aa}-f_{bb}).
$$

This is the extra equation allowing separation of discounting from the local kernel. The source discusses approximate returns to a starting height in a more general binomial before assuming exact two-step recombination. Reachability of a nearby node should not be confused with a proof that an arbitrary drifted binomial returns there almost surely; the clean worked algebra uses $ab=1$.

With identical rows, the local matrix is rank deficient. A state-independent binomial gives

$$
p_a=\delta d_a f,\qquad
p_b=\delta d_b(1-f),\qquad
p_{a\cdot1}=2\delta^2f(1-f).
$$

There are four unknowns and only three independent equations, leaving a family of positive solutions. Thus more maturities or recombination do not automatically solve identification when the economic transitions carry too little state dependence. The text's general statement about solution dimension being equal to the matrix rank should not be used as a general linear-algebra rule: nullity and the nonlinear additional restrictions determine the solution set; the explicit example establishes nonuniqueness without that general claim.

Theorem 4 summarizes recovery under the specified full-rank, kernel, and process conditions. Its full-rank requirement applies to this particular fixed-height regime construction; it is not a missing assumption in Theorem 1.

## CRRA specialization and the limits of parametric help

With constant relative risk aversion $\gamma$, the consumption-growth kernel is

$$
\phi(x,y)=\delta(y/x)^{-\gamma}.
$$

For a two-regime binomial, write $f_a=f_{aa}$ and $f_b=f_{bb}$. The four pricing equations are

$$
p_{aa}=\delta f_a a^{-\gamma},\qquad
p_{ab}=\delta(1-f_a)b^{-\gamma},
$$

$$
p_{ba}=\delta(1-f_b)a^{-\gamma},\qquad
p_{bb}=\delta f_b b^{-\gamma}.
$$

When the rows contain independent information, these identify $f_a,f_b,\gamma,\delta$. The paper gives the explicit probability solution in Eq. (60), followed by

$$
\gamma=
\frac{-\log[f_a/(1-f_a)]+\log[p_{aa}/p_{ab}]}{\log(b/a)},
\qquad
\delta=\frac{p_{aa}a^\gamma}{f_a}.
$$

A convenient reconstruction of the probability step is to first solve the two linear equations obtained after setting $A=\delta a^{-\gamma}$ and $B=\delta b^{-\gamma}$: $p_{aa}/A+p_{ab}/B=1$ and $p_{ba}/A+p_{bb}/B=1$. Once the reciprocal factors are determined, $f_a=p_{aa}/A$ and $f_b=p_{bb}/B$. This describes the same pricing restrictions while making the rank condition transparent.

If growth probabilities are state independent, $f_b=1-f_a$, the four equations collapse to two. Then a CRRA restriction still leaves three unknowns, $f,\gamma,\delta$, and two independent prices. Recombination supplies no new information because the CRRA growth ratios already impose the same relation along the return path. A parametric utility function can therefore reduce unknowns and simultaneously reduce independent restrictions without delivering recovery.

There are two clear source typographical issues on journal p. 629: the line introducing $f_b\ne1-f_a$ says “state independence,” although the condition and subsequent argument require meaningful state dependence, and Eq. (64) labels the down-state price $p_a$ instead of $p_b$. The equations above follow the state-dependent logic while identifying these corrections explicitly.

The tree valuation equations also distinguish stock prices from consumption. Under CRRA, $S(i,H)=v_iH$ for regime-dependent valuation constants $v_i$. Even if consumption height recombines with $ab=1$, the stock-price process need not return to the same value because the ending regime can differ. Recovery based on price nodes must respect that distinction. The paper further allows regime-dependent payout rates $k_a,k_b$, which enter cross-regime kernel ratios; these ratios need to be known or separately specified rather than absorbed invisibly into risk aversion.

## The constructive example and the unbounded counterexample

The first numerical exercise is a controlled one-period lognormal-payoff economy with CRRA coefficient $\gamma=3$, an assumed market return of 8%, standard deviation 20%, and subjective discount factor $e^{-0.02}=0.9802$. It uses eleven nodes from minus five to plus five standard deviations, with normalized payoff levels approximately 0.37, 0.45, 0.55, 0.67, 0.82, 1, 1.22, 1.49, 1.82, 2.23, and 2.72. Table I gives both the constructed pricing matrix and the natural matrix.

The natural payoff distribution is fixed across starting states, so its rows are identical. Nevertheless the price matrix has differing row scales because the current marginal utility differs. The recovered normalized kernel values are approximately 20.086, 11.023, 6.05, 3.32, 1.822, 1, 0.549, 0.301, 0.165, 0.091, and 0.05. Recovery reproduces the imposed distribution and discount factor. This is a consistency demonstration in data generated to fit the structure, not empirical evidence that the structure fits the market.

The paragraph below Table I says the positive eigenvector equals the displayed pricing kernel. Under the theorem's own $Pz=\delta z$ convention, it is the reciprocal of the normalized kernel. The numerical procedure must use $h_i=1/z_i$, not substitute the eigenvector directly for $h$. The table normalizes the kernel shape to one at the current node; the actual one-period stochastic discount factor also includes $\delta$.

The next example changes consumption to unbounded lognormal growth:

$$
S_T=S_0\exp\left[(\mu-\tfrac12\sigma^2)T+\sigma\sqrt T\,Z\right],
\qquad Z\sim N(0,1).
$$

To avoid the source's reuse of $\delta$ for both a discrete factor and a continuous discount rate, denote the latter by $\kappa$. The CRRA kernel is $e^{-\kappa T}(S_T/S_0)^{-\gamma}$. In log coordinates, state prices depend on a quadratic in the log growth increment. Even with known $\sigma$, its informative coefficients identify only the combinations

$$
\gamma-\frac{\mu-\sigma^2/2}{\sigma^2},
\qquad
\kappa+\frac{(\mu-\sigma^2/2)^2}{2\sigma^2},
$$

rather than the three parameters $\mu,\gamma,\kappa$ separately. This is the familiar diffusion-pricing indeterminacy in an explicit recovery setting.

The continuous pricing operator has many positive eigenfunctions. For every admissible exponential $v_\alpha(s)=e^{\alpha s}$, the paper obtains

$$
\lambda(\alpha)=
\exp\left[-\kappa T+(\alpha-\gamma)(\mu-\tfrac12\sigma^2)T
+\tfrac12\sigma^2T(\alpha-\gamma)^2\right].
$$

No unique positive eigenfunction selects the original natural drift. The finite Perron argument cannot simply be carried over to an unbounded continuous space without additional conditions.

Truncating tails can restore a finite matrix and a unique numerical answer, but it also imposes effective restrictions on the far-state kernel. A stable finite-grid answer is not by itself proof that the unbounded process has become identified. Ross suggests checking alternative truncations and considers bounded kernels, bounded processes, and richer state dependence as routes to recovery; the cited continuous-space extensions are separate results, not proved in this article. Tail aggregation can preserve particular cumulative probabilities in the constructed static example without making every dynamically truncated growth model exact.

## From an option surface to a transition matrix

Section V is explicitly an illustration on one date. The main reported state prices and recovered probabilities use April 27, 2011 S&P 500 options. Figure 1 shows a separate volatility surface labeled March 20, 2011, and the synthetic Table I discussion mentions March 15. These are different dated illustrations, not a time-series validation sample. The source data are a bank over-the-counter bid/offer sheet; Table II describes an offer sheet. The paper does not provide a fully reproducible quote archive or specify every choice of bid, ask, or midpoint.

For European call values at strike $K$ and maturity $T$,

$$
C(K,T)=\int_K^\infty(S-K)p(S,T)\,dS,
\qquad
p(K,T)=\frac{\partial^2C(K,T)}{\partial K^2}.
$$

The second derivative gives a state-price density, not an undiscounted probability density. Ross uses numerical second differences on an index-movement grid of 0.5%. Finite-difference differentiation amplifies quote and interpolation error; its output should be nonnegative and integrate to the maturity discount factor. The paper acknowledges deficiencies in precisely this step. It does not disclose a complete arbitrage-constrained smoothing method, tail extrapolation specification, dividend treatment, strike inclusion rule, or finite-difference boundary scheme.

The current option surface yields row vectors $p^{(t)}$ of prices for future state claims, all starting from today's state $c$. It directly determines only the current-state row of the one-period transition matrix. Time homogeneity supplies the forward equations

$$
p^{(t+1)}=p^{(t)}P,
\qquad p^{(0)}=e_c^{\mathsf T}.
$$

Stacking observed row vectors gives a linear system $XP=Y$, where successive rows of $X$ are $p^{(0)},p^{(1)},\ldots$ and those of $Y$ are the next maturities. This is a useful explicit reconstruction of the source's Eq. (86). In an exactly identified noiseless setting, $P=X^{-1}Y$ when $X$ is square and invertible. Counting $m^2$ equations for $m^2$ prices is not sufficient: those maturity vectors must span the state space. Nearly dependent rows make inversion ill conditioned.

The paper fits $P$ numerically to minimize squared deviations from the observed state-price vectors while requiring unimodal rows. An implementation of the stated forward-equation fit can minimize $\sum_t\|p^{(t+1)}-p^{(t)}P\|^2$ subject to nonnegative entries, the current-row constraint, and row unimodality. Alternatively, fitting $e_c^{\mathsf T}P^t$ directly to all observed marginal vectors yields a different nonlinear criterion in noisy data. The article's description does not resolve every detail of which residual construction, weighting, optimization algorithm, or mode-selection rule was used. Those choices cannot be invented and called an exact replication.

The fitted state grid has eleven nodes from minus five to plus five standard deviations, using 9% per quarter. The normalized index levels run from approximately 0.64 to 1.57, corresponding to representative returns −36%, −30%, −24%, −16%, −9%, 0%, 9%, 20%, 31%, 43%, and 57%. Observed maturity columns run quarterly from 0.25 to three years. The implementation deliberately treats the current index level as the entire state and omits implied volatility and past returns. Ross later acknowledges that price alone is not a sufficient state description in general.

Unimodality regularizes the matrix estimate but is not a theorem-implied property of every valid state-price transition matrix. Likewise, grid width, tail aggregation, and state omission are modeling choices. They sit between observed option premiums and the exact recovery theorem and can materially determine the result.

## Numerical recovered distributions and the source's inconsistencies

Table III's recovered normalized kernel declines from 1.86 at the lowest node to 0.22 at the highest, with values 1.24 at −9%, 1 at the current node, and 0.83 at +9%. As in Table I, these are normalized kernel-shape values. They do not on their own equal the full intertemporal kernel without its discount factor.

The reported quarterly Perron root is 1.0018. With monthly rather than quarterly data, the author reports 0.9977. The first value is mathematically compatible with a positive-eigenpair problem, but exceeds one and is uncomfortable under the conventional subjective-discounting interpretation. Ross presents the contrast as a warning about estimation sensitivity. It should not be repaired by silently clipping the eigenvalue or renormalizing every row.

Selected annualized statistics from Table IV are:

| Horizon | Recovered mean | Recovered volatility | Reported risk-free rate | Excess mean | Sharpe | ATM implied volatility |
|---|---:|---:|---:|---:|---:|---:|
| 0.25 years | 5.1% | 11.7% | 0.5% | 4.7% | 0.399 | 14.5% |
| 0.5 years | 5.5% | 14.0% | 0.2% | 5.3% | 0.376 | 16.7% |
| 1 year | 6.2% | 15.0% | 1.8% | 4.3% | 0.287 | 18.2% |
| 2 years | 6.2% | 15.4% | 4.8% | 1.5% | 0.096 | 19.3% |
| 3 years | 5.7% | 14.9% | 7.4% | −1.7% | −0.115 | 20.3% |

Rounding explains some small discrepancies between displayed mean minus rate and displayed excess mean. The historical comparison reports 10.3% annualized mean, 15.5% volatility, 5.5% risk-free rate, 4.9% excess mean, and Sharpe 0.316. It uses monthly S&P 500 returns from January 1, 1960 through November 30, 2010. The prose calls this “60 years,” whereas the table calls it a 50-year period; the explicit dates should govern replication.

The recovered mean is therefore lower than the historical mean, while recovered volatility is similar. Higher implied than recovered volatility is consistent with a volatility risk premium but is not sufficient evidence identifying such a premium. There is no forecast comparison against subsequent realized distributions over a holdout sample.

The estimated long-maturity interest rates are a recognized problem. The paper attributes the negative recovered risk premium after 2.5 years to biased state-price extraction, not to evidence that investors expected a negative equity premium. There is also a direct reporting inconsistency beyond that acknowledged bias: Table II's one- and three-year discount factors are 0.969 and 0.809. Using $r_T=-\log(B_T)/T$ gives approximately 3.15% and 7.06%, which do not reproduce the Table IV rates of 1.8% and 7.4%, or the prose's 1.85% and 7.93%. The supplied article does not provide enough implementation detail to reconcile those rate conventions and inputs. The table statistics should be reported as printed, with this limitation visible.

## Tail probabilities and what the historical comparison establishes

Table V compares six-month recovered probabilities with 5,000 bootstrap draws formed from independent monthly historical returns over the dates above. This bootstrap suppresses serial dependence and volatility-state conditioning by construction. It is a historical benchmark, not a competing option-based forecast fitted on the same current information set.

The probability of a six-month decline exceeding 32% is 0.0008, or 0.08%, in the bootstrap and 0.0120, or 1.20%, under recovery. The historical estimate is four occurrences in 5,000 draws. For a decline exceeding 26%, the cumulative probabilities are 0.0020 and 0.0223, or 0.20% and 2.23%; the historical count is ten. For the −19% cutoff they are 1.22% and 4.73%, and for −12% they are 5.70% and 9.12%.

These are natural probabilities under the recovered model, not the original risk-neutral tail probabilities. That separation is the paper's intended contribution to disaster-risk measurement. The two rarest comparisons are approximately fifteen-fold and eleven-fold differences, but their apparent precision should not disguise sensitivity to derivative tail extrapolation, finite-grid boundaries, and the very small historical event counts.

Table V uses range labels −32%, −26%, −19%, and so forth, whereas the earlier transition tables label representative state values −36%, −30%, −24%, and so forth. The reported tail cutoffs should therefore be taken from Table V's cumulative distribution rather than substituting the representative-node labels from Table III. A replication needs the underlying bin-boundary convention, not only the rounded node values.

The recovered distribution also has a thinner right tail than the historical bootstrap in this example. For instance, Table V's cumulative probability at the +14% range is 0.9951 under recovery versus 0.9578 historically. Thus the comparison is not merely a symmetric fattening of both tails. It reflects the whole fitted distribution from one day's surface and the chosen state dynamics.

No confidence intervals are supplied for the recovered means, kernel values, or tail probabilities. The application does not propagate quote uncertainty through smoothing, matrix estimation, and eigenvector recovery. Nor does it present systematic sensitivity grids, multiple-date forecast calibration, proper scoring rules, or transaction-cost-adjusted trading results. The author explicitly calls the exercise indicative and acknowledges that better estimation could alter its implications.

## The proposed efficiency tests

Section VI uses the recovered kernel to constrain the performance of trading strategies measurable within the relevant stock-market information set. For an excess return $x$, the pricing relation $E[\phi x]=0$ and Cauchy–Schwarz imply the Hansen–Jagannathan bound

$$
\frac{|E[x]|}{\sigma(x)}\le\frac{\sigma(\phi)}{E[\phi]}.
$$

With $E[\phi]=e^{-rT}$, this is

$$
\sigma(\phi)\ge e^{-rT}\frac{|E[x]|}{\sigma(x)}.
$$

The paper reports a one-year kernel variance of 0.1065 and standard deviation 0.3264. Ignoring the small discount adjustment, it interprets approximately 0.326 as the largest annual Sharpe ratio consistent with the recovered kernel. This is a model-consistency bound conditional on the kernel estimate, relevant asset span, and information set. It is not an unconditional empirical law that any strategy above a 0.33 Sharpe ratio proves markets inefficient.

The second proposed test decomposes returns as

$$
x_t=\mu(I_t)+\varepsilon_t,
\qquad E[\varepsilon_t\mid I_t]=0.
$$

The corresponding population regression fit is

$$
R^2=\frac{\operatorname{Var}[\mu(I_t)]}{\operatorname{Var}(x_t)}.
$$

Using the conditioning and pricing argument referenced to Ross (2005), the article states

$$
R^2\le
\frac{E[\mu(I_t)^2]}{\operatorname{Var}(x_t)}
\le e^{2rT}\operatorname{Var}(\phi).
$$

It therefore obtains an approximate 10% bound from the estimated kernel variance. The first inequality is the variance-versus-second-moment relation; the second requires the maintained pricing and information-set argument, not just that algebraic identity. The paper does not reproduce every conditioning step from the cited earlier work. An empirical test should match the population horizon and admissible information set rather than compare an arbitrary in-sample fitted $R^2$ with 10%.

The source emphasizes that adding noise orthogonal to traded payoffs can arbitrarily increase a candidate kernel's variance. The relevant object is consequently the projected kernel for claims in the stock-market filtration. A projection adequate for index-price-based strategies need not price strategies using additional state information that was omitted from the recovered model. The main conclusion's reference to “publicly available data” should therefore be read together with this narrower filtration qualification.

Similarly, unexplained return variation is residual uncertainty relative to $I_t$; it need not be idiosyncratic in the cross-sectional asset-pricing sense. A rejection could reflect failure of transition independence, state sufficiency, matrix estimation, or the maintained pricing structure rather than inefficiency alone. “Model-free” here means avoiding a particular parametric asset-pricing model within the recovery assumptions. Those assumptions remain joint maintained hypotheses. Ross also notes that an economically implementable violation must survive transaction costs; the paper does not perform that trading test.

## Assessment and source map

The theorem's durable contribution is the positive-eigenvector identification mechanism and its focus on conditional transition prices. The matrix algebra is exact under its assumptions. The numerical illustration is deliberately preliminary and has much weaker evidentiary status. The unbounded-growth counterexample is especially valuable because it makes the theorem's boundary explicit rather than suggesting that a dense option surface always identifies expected returns.

A serious empirical implementation would have to make state sufficiency, quote filtering, no-arbitrage smoothing, tail extrapolation, rank and conditioning of the forward equations, matrix constraints, and truncation sensitivity explicit. It would then need to propagate estimation uncertainty and compare recovered forecasts with realizations across dates. Those steps are not minor engineering additions to a verified strategy; they determine whether the theorem's informative input can be estimated well enough to support its proposed applications.

The basic framework and transition independence are on journal pp. 617–620, PDF pp. 3–6, Eqs. (1)–(14). The finite theorem and corollaries are on pp. 621–624, PDF pp. 7–10, Eqs. (15)–(30). Multinomial and CRRA recovery are on pp. 625–630, PDF pp. 11–16, Eqs. (31)–(69). The synthetic and unbounded examples are on pp. 630–633, PDF pp. 16–19, Table I and Eqs. (70)–(81). Option extraction and transition fitting are on pp. 634–639, PDF pp. 20–25, Eqs. (82)–(86) and Table II. Recovered distributions are Tables III–V, PDF pp. 26–29. Efficiency bounds are on pp. 643–645, PDF pp. 29–31, Eqs. (87)–(92). Conclusions and references occupy PDF pp. 31–34.

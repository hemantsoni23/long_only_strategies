# A Unified Beta Pricing Theory

**Gregory Connor (1984).** *Journal of Economic Theory* 34, 13–31. Source: [APTFundSeparation_Connor_1984.pdf](../../Finance/APTFundSeparation_Connor_1984.pdf). All nineteen PDF pages were inspected, including the final appendix page, whose extraction omits its equations and was read visually. References below are printed pages. This is a theoretical equilibrium paper without an empirical dataset or performance backtest.

## Why this matters

Two models can tell very different stories about diversification while making identical predictions for prices and investor portfolio returns. In one story, a finite set of assets contains combinations whose idiosyncratic risks cancel exactly. In the other, many individually small positions eliminate residual risk in the limit. Connor derives both stories from a common set of conditions and proves an equivalence between their competitive equilibria.

The novel organizing concept is **market insurance**: every distribution of expected payoff and factor exposure across investors can be implemented without anyone bearing idiosyncratic risk. Conditional mean-zero residuals make that insurance desirable to risk-averse investors. Feasibility and equilibrium then ensure that all investors use it. Their marginal indifference to residual risk forces *exact* linear factor pricing.

This is stronger than the usual asymptotic APT statement that the average squared pricing error vanishes. The strength comes from additional assumptions about supplies, spanning, preferences, and equilibrium. The paper is useful for diagnosing a factor model: uncorrelated residuals alone do not imply that investors can collectively eliminate them, and exact diversification is not a property of an arbitrary finite portfolio.

## Primitives of the finite and limit economies

Asset $i$ has a per-share terminal payoff. Collect risky payoffs in

$$
X=c+BF+\varepsilon,
$$

where $c=\mathbb E X$, $B$ is a loading matrix with $K$ columns, $\mathbb E F=0$, and $\mathbb E\varepsilon=0$. The paper assumes a riskless asset with payoff $x_0$, residual covariance $V=\mathbb E[\varepsilon\varepsilon']$, and factor second moments. Its key distributional condition is

$$
\mathbb E[\varepsilon\mid F]=0.
$$

This implies unconditional orthogonality to the factors when the moments exist, but is stronger than zero linear covariance. Residuals may have variances that depend on $F$, and they need not be independent of one another. Conditional mean independence is precisely what allows conditional Jensen inequalities and removes residual terms from marginal-utility pricing at insured allocations.

In a finite economy there are $v$ risky assets. The columns of $B$ are independent, and the covariance matrix of total risky payoffs is nonsingular, excluding redundant risky assets. Residual covariance $V$ may be singular. Investors have increasing, risk-averse expected-utility preferences, and a competitive equilibrium is assumed to exist. The proofs using strict improvement require strict risk aversion for genuinely nondegenerate conditional noise; indifferent linear-utility investors would not necessarily choose only insured positions.

In the limit economy, risky assets are countably infinite. For every sufficiently large finite prefix, $B_v$ has full column rank and $V_v$ is nonsingular. Investors may hold limits of finite portfolios in the norm

$$
\|(a_0,a)\|=\left(\mathbb E[(a_0x_0+a'X)^2]\right)^{1/2}.
$$

Portfolios giving the same payoff almost surely are identified. The admissible space includes its relevant mean-square limits, so a sequence of increasingly diversified holdings can define a portfolio even if it cannot be represented by a fixed, ordinary vector of share quantities. The construction is about payoff equivalence, not the physical delivery of infinitely many securities by a broker.

Let $(q_0,q)$ denote per-capita net supply and let there be $\mu$ investors. Allocations satisfy $\sum_\gamma(a_0^\gamma,a^\gamma)=\mu(q_0,q)$. Each investor's endowment is $(e_0^\gamma,e^\gamma)$. At prices $(p_0,p)$, competitive equilibrium requires budget feasibility and expected-utility optimality. No shorting, borrowing, or transaction-cost constraint restricts the marginal portfolio perturbations used in the pricing proof.

## Insurability: the two economically different requirements

A portfolio is well diversified if

$$
\mathbb E[(a'\varepsilon)^2]=a'Va=0.
$$

This means zero residual payoff almost surely, not merely a small estimated residual volatility. Two portfolios are factor equivalent when they have the same mean payoff and factor loading:

$$
a_0x_0+a'c=w_0x_0+w'c,\qquad a'B=w'B.
$$

An allocation is insured if every investor's portfolio is well diversified. An economy is insurable if every feasible allocation admits an insured factor-equivalent allocation. Theorem 1, pp. 19–20, gives necessary and sufficient conditions:

1. Aggregate net supply is already free of idiosyncratic risk: $\mathbb E[(q'\varepsilon)^2]=0$.
2. Every feasible factor exposure can be spanned by an idiosyncratic-risk-free portfolio: for every $b\in\mathbb R^K$, some $w$ satisfies $w'B=b'$ and $w'Vw=0$.

The first condition is a resource restriction. Investors cannot all insure away a risk that remains in aggregate supply. The second is a spanning restriction. Even if aggregate residual risk vanishes, investors still need to exchange arbitrary factor exposures without reintroducing it. Neither condition subsumes the other.

Necessity follows by summing insured holdings to recover the market portfolio and by considering allocations with any chosen factor position. For sufficiency, replace the first $\mu-1$ investors' portfolios by diversified factor-equivalent ones. Assign the last investor the residual aggregate supply. The market portfolio and all previously allocated portfolios have zero residual risk, so the last one does too. Adjust each investor's riskless position to match expected payoff; the total cash allocation remains feasible by the resource constraint. This construction is explicit and does not appeal to an unspecified representative investor.

Given a portfolio with payoff $m+b'F+a'\varepsilon$, conditional Jensen gives

$$
\mathbb E[u(m+b'F+a'\varepsilon)\mid F]
\le u(m+b'F).
$$

The insured factor-equivalent portfolio therefore weakly improves utility, strictly under the relevant nondegeneracy and strict-concavity conditions. If an equilibrium allocation were uninsured, the construction would produce a feasible Pareto improvement. Theorem 2 rules that out through competitive efficiency. It does not say that any ad hoc unilateral replacement at arbitrary prices is automatically budget feasible.

## Mutual funds and payoff-space dimension

Choose one diversified portfolio for each unit factor exposure and add the risk-free asset. Every insured payoff can be written as a combination of these $K+1$ payoffs. Corollary 2.1, p. 22, therefore implies that each equilibrium portfolio belongs to that mutual-fund span.

The risky factor-mimicking funds need not have the same expected payoff, price, or gross exposure, and the construction need not produce long-only funds. A useful normalization is to give each risky fund zero mean payoff by an offsetting cash holding; its remaining payoff is the corresponding factor. An investor with desired mean $m$ and factor vector $b$ then holds the claim $m+b'F$.

Because portfolios with equal payoffs are identified, the theorem's statement that investors “hold” the funds is stronger in wording than a conventional holdings-space separation theorem. Actual share holdings can differ through payoff-redundant positions without creating a distinct portfolio in Connor's space. Observing a different list of securities is not by itself a refutation of payoff separation.

## Exact price linearity and its proof

The paper normalizes prices so the gross risk-free return equals one, $p_0=x_0$. Under this normalization its exact pricing equation is

$$
p=c+Bm.
$$

The $K$-vector $m$ prices factor exposure in payoff units. Without normalization, divide payoffs or scale prices consistently by the gross risk-free return before applying this expression. It is not appropriate to insert a conventional return-regression premium without converting units and signs.

Lemma 1 constructs the deviation portfolio. In a finite universe, regress $p-c$ cross-sectionally on $B$ and write

$$
p-c=Bm+d,\qquad B'd=0.
$$

If $d\ne0$, hold risky quantities $h=-d$ and riskless quantity

$$
h_0=\frac{c'd+d'd}{x_0}.
$$

Then

$$
h_0p_0+h'p=0,\quad h'B=0,\quad
\mathbb E[h_0x_0+h'X]=d'd>0.
$$

This is not necessarily a risk-free arbitrage: it still contains $h'\varepsilon$. The lemma establishes a free positive expected payoff in exchange for residual risk whenever prices fail to be linear.

In the infinite economy, perform this calculation on a finite asset prefix with nonzero pricing residual and extend its holdings by zeros. If every sufficiently large prefix fits exactly, a common full-rank prefix uniquely identifies the factor-price vector and forces all subsequent fits to use the same vector. Thus either a finite deviation portfolio exists or prices are globally linear; no infinite cross-sectional least-squares sum is required.

At an insured equilibrium portfolio $W=a_0x_0+a'X$, wealth is a function only of $F$. Consider an infinitesimal zero-cost, zero-factor-risk perturbation $H=h_0x_0+h'X$. Optimality requires

$$
\left.\frac{d}{dt}\mathbb E[u(W+tH)]\right|_{t=0}
=\mathbb E[u'(W)H]=0.
$$

Conditional mean-zero residuals remove the covariance term, leaving

$$
\mathbb E[u'(W)](h_0x_0+h'c)=0.
$$

Since expected marginal utility is positive, the expected payoff of every such perturbation must be zero. This contradicts the deviation portfolio if $d\ne0$, proving Theorem 3. Economically, an investor with no existing residual exposure experiences its small addition only at second order but receives a positive expected payoff at first order.

Differentiation under expectation and interior admissibility are regularity requirements of this argument. The model is not a theorem about constrained agents who cannot make the proposed infinitesimal long-short perturbation. Nor does it identify the equilibrium vector $m$ without specifying the investors, endowments, and factor distribution.

## Implementable tests of the spanning condition

The appendix provides concrete matrix criteria. In a finite economy let $V^+$ be the Moore–Penrose inverse and define

$$
P_0=I-V^+V.
$$

For symmetric positive-semidefinite $V$, this is the orthogonal projector onto its null space. Lemma 2 says diversified factor spanning holds exactly when $P_0B$ has full column rank $K$. Aggregate insurance additionally requires $Vq=0$.

A constructive solution, derived from the lemma, is

$$
W=P_0B(B'P_0B)^{-1}.
$$

Its columns span unit factor exposures because $B'W=I_K$, and $VW=0$. For desired exposure $b$, set $w=Wb$ and add cash to obtain any chosen mean payoff. This formula makes the theorem directly checkable in a fully specified finite model.

For numerical work, use an eigendecomposition or SVD to determine the null space. An empirical covariance matrix is ordinarily noisy and full rank; declaring tiny eigenvalues exactly zero is an approximation that the theorem does not justify. Report the threshold used, the resulting residual variances, and the conditioning of $B'P_0B$. A nearly singular matrix may require extreme holdings even if a formal rank calculation passes.

For the infinite economy, Lemma 3 gives a sufficient condition:

$$
\left\|\left(B_v'V_v^{-1}B_v\right)^{-1}\right\|\longrightarrow0.
$$

For a fixed target $b$, construct

$$
w_v=V_v^{-1}B_v(B_v'V_v^{-1}B_v)^{-1}b.
$$

Then $B_v'w_v=b$, and its idiosyncratic variance is

$$
w_v'V_vw_v=b'(B_v'V_v^{-1}B_v)^{-1}b\longrightarrow0.
$$

This is the minimum-residual-variance portfolio for the specified factor exposure. To make the source's mean-square convergence argument fully explicit, fix the desired mean payoff $m_\star$ and choose the riskless holding

$$
h_{0,v}=\frac{m_\star-c_v'w_v}{x_0}.
$$

Total payoff is then $m_\star+b'F+w_v'\varepsilon$, which converges to $m_\star+b'F$ in $L^2$. Vanishing residual variance alone would not control a drifting mean. For example, with one factor, $B_v=\mathbf1$, $V_v=I$, target exposure one, and $c_i=i$, the risky weights are $1/v$. Residual variance is $1/v$ but the mean is $(v+1)/2$, which diverges. This is a constructed illustration of the missing mean control, not a numerical example in the paper. The riskless asset already present in the model supplies the required adjustment.

The limit criterion is stated as sufficient, whereas the finite null-space condition is necessary and sufficient. Both concern factor spanning; the aggregate-supply insurance condition still has to be checked independently.

## Equilibrium equivalence and what can be observed

A finite and a limit economy correspond when they have the same preferences, factor random variables, and factor-equivalent individual endowments. Their securities need not be identical. Theorem 4, pp. 26–27, states that any competitive equilibrium in one insurable economy has an isomorphic equilibrium in the other: the factor-price vector is the same, and each investor receives the same portfolio payoff.

The construction carries an insured allocation to its factor-equivalent insured counterpart and assigns prices $p^*=c^*+B^*m$. Under common $m$, the cost of any portfolio equals its mean payoff plus the value of its factor exposures. Corresponding endowments therefore have identical values and the transported allocation is budget feasible. If a better budget-feasible portfolio existed in the second economy, it could first be insured and then transported back, contradicting optimality in the first.

The reverse construction works identically. Equilibrium existence in the finite model can thus support an equilibrium in the corresponding limit model. Multiple equilibria are not excluded; the mapping is between equilibria, rather than a claim of a unique price or unique investor demand.

The observational implication is narrow but powerful. Prices and equilibrium portfolio returns alone do not distinguish the corresponding finite cancellation model from the infinite diversification model. The theorem does not say that security supplies, the joint law of individual payoffs, or other institutional information are uninformative. Nor does it equate every empirical multifactor model with every version of CAPM or APT.

## The CAPM case and the role of aggregate supply

For an externally specified finite factor model, exact aggregate cancellation requires supplies to lie in a special subspace. Small supply perturbations generally destroy it. The limit model instead obtains aggregate diversification from sufficiently small per-capita positions with controlled residual dependence. Connor regards the latter as the more plausible large-economy mechanism.

CAPM avoids imposing an externally fixed factor and then requiring supplies to cancel its residuals. It defines the factor from the market itself:

$$
F=q'X-\mathbb E[q'X],\qquad
B=\frac{\operatorname{Cov}(X,q'X)}{\operatorname{Var}(q'X)},\qquad
c=\mathbb E X.
$$

Consequently $q'B=1$ and $q'\varepsilon=0$ identically. Under joint normality, the regression residuals also have zero conditional mean given the market factor. The market supplies therefore satisfy aggregate insurance by construction, and the market provides the one risky exposure needed for spanning.

The price equation can be translated to the familiar expected-return relation. With normalized risk-free return one, asset return $R_i=X_i/p_i$ and risky-market return $R_M=q'X/(q'p)$ satisfy

$$
\mathbb E R_i-1=
\frac{\operatorname{Cov}(R_i,R_M)}{\operatorname{Var}(R_M)}
(\mathbb E R_M-1).
$$

This translation follows from $p_i=c_i+B_im$, $q'B=1$, and division by market values. It is not an empirical estimate in the paper. The market-based construction makes CAPM an “as if” representation of the larger diversification economy under the stated correspondence, not a demonstration that observed returns are normally distributed.

## Reproduction scope and practical limits

A finite synthetic reconstruction needs a joint law for $(F,\varepsilon)$, $B$, expected payoffs, supplies, a riskless payoff, preferences, and endowments. Verify conditional mean independence, the covariance/rank assumptions, $Vq=0$, and the null-space spanning test. Construct insured factor portfolios, solve the reduced $K+1$-payoff equilibrium, and map demands back to securities. Compare prices to $c+Bm$. The source supplies this theoretical recipe but no calibration, numerical optimizer, or simulated parameter set.

For an asymptotic reconstruction, document the nested asset universe and covariance matrices, keep desired mean payoff and factor exposure fixed, and show the maximum eigenvalue of $(B_v'V_v^{-1}B_v)^{-1}$ tending toward zero. A declining variance for one selected portfolio does not establish spanning for every factor direction.

The main limitations are economic as well as numerical. Real investors face incomplete insurance, institutional restrictions, nontraded income, heterogeneous beliefs, and financing costs. A finite covariance estimate rarely has the exact null space required by the finite theorem. Even where approximate spanning is possible, large gross exposure can make it costly. The paper provides no finite-sample error bound that converts approximate insurability into approximate linear pricing.

Its durable contribution is a clean separation of mechanisms: conditional mean-zero noise makes insurance desirable; supply and spanning make it feasible; equilibrium makes investors use it; and marginal optimality makes residual risk unpriced. Removing any one of those steps changes the conclusion. The empirical-equivalence result then explains why price regressions alone cannot identify which diversification mechanism generated the same observable factor-pricing relation.

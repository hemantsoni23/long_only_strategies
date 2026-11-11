# The Arbitrage Theory of Capital Asset Pricing

**Stephen A. Ross (1976).** *Journal of Economic Theory* 13, 341–360. Source: [APT_Ross_1976.pdf](../../Finance/APT_Ross_1976.pdf). The local PDF contains all 20 published pages, including both mathematical appendices and the references. Printed page 341 is PDF page 1. This note concerns the original theorem and its qualifications, rather than a later statistical factor-model formulation of arbitrage pricing theory.

## Why this matters

A factor model for realized returns is not, by itself, a theory of expected returns. Its common components describe how assets move together; a pricing theory must explain why expected returns should lie approximately in the span of their factor exposures. Ross supplies a large-market argument linking those statements without requiring that every investor have quadratic utility or that asset returns be jointly normal. The economic mechanism is the construction of diversified, zero-investment portfolios that eliminate common risks. If sufficiently large pricing discrepancies remained, these portfolios would offer attractive nearly riskless payoffs.

The important contribution is also a qualification of that intuition. Adding securities can increase aggregate wealth as well as diversification opportunities. If the relevant investors become increasingly averse to proportional wealth risk, vanishing portfolio variance need not remove the compensation required for that risk. Section I constructs an explicit counterexample. The subsequent theorem therefore uses bounded relative risk aversion, a nonnegligible investor, bounded expected returns, restrictions on aggregate positions, and a technical continuity condition on expected utility. It is more careful than the slogan that absence of arbitrage makes every asset exactly linearly priced.

The exact result is an approximation in a cross-sectional square-summability sense. There exist fixed coefficients such that the sum of squared expected-return discrepancies over an expanding asset universe is finite. Individual exceptional assets can retain nonzero discrepancies. Average discrepancy shrinks as the universe grows, but the theorem does not provide a practical finite-sample significance threshold or an algorithm for discovering the factors. Those distinctions matter when using the paper to motivate a factor model, evaluate an apparent anomaly, or design a neutral portfolio.

## Return system and the object to be explained

For asset $i$, write its random return as

$$
\widetilde x_i=E_i+\beta_i\widetilde\delta+\widetilde\varepsilon_i,
\qquad \beta_i=(\beta_{i1},\ldots,\beta_{ik}).
$$

Here $E_i$ is its subjective expected return, $\widetilde\delta$ is a fixed-dimensional vector of mean-zero common factors, and $\widetilde\varepsilon_i$ is its mean-zero idiosyncratic component. In the main theorem the idiosyncratic components are mutually uncorrelated and have uniformly bounded variances:

$$
E[\widetilde\delta_j]=E[\widetilde\varepsilon_i]=0,
\qquad E[\widetilde\varepsilon_i\widetilde\varepsilon_j]=0\quad(i\ne j),
\qquad \sigma_i^2=E[\widetilde\varepsilon_i^2]\le\bar\sigma^2<\infty.
$$

Equation (15), printed page 347, imposes no normality. The common factors need not be mutually independent, independent of the idiosyncratic terms, or even have finite variances. The mean-zero assumption still requires their expectations to be defined. The finite second-moment restriction belongs to the idiosyncratic components. This distinction is easily lost in the PDF's extracted text: the uncorrelated terms are the $\varepsilon_i$, not an additional assumption of independent common factors.

Let $E_n$ be the vector of the first $n$ expectations, $B_n$ the $n\times k$ loading matrix, and $e_n$ the vector of ones. A fully invested portfolio $\alpha$ satisfies $\alpha'e_n=1$. An incremental, zero-investment portfolio $\eta$ satisfies $\eta'e_n=0$; factor neutrality adds $\eta'B_n=0$. Its payoff is therefore

$$
\eta'\widetilde x=\eta'E_n+\eta'\widetilde\varepsilon,
\qquad \operatorname{Var}(\eta'\widetilde\varepsilon)=\eta'V_n\eta,
$$

where $V_n=\operatorname{diag}(\sigma_1^2,\ldots,\sigma_n^2)$. Eliminating the common factor is algebraic and does not require its variance to exist. Diversifying the remaining component uses the residual variance bound.

In the introductory heuristic, each weight is of order $1/n$, so $\eta'V_n\eta\le\bar\sigma^2\sum_i\eta_i^2=O(1/n)$. If every factor-neutral zero-investment portfolio had exactly zero expected payoff, elementary linear algebra would imply

$$
E_n=\rho e_n+B_n\gamma.
$$

The rigorous argument cannot simply set the small residual risk to zero. It must show that investors would exploit a sequence of such portfolios, with wealth and preferences evolving across the expanding markets. That is why the proof studies constrained minimum-variance portfolios and expected utility rather than relying only on the heuristic order calculation.

The paper uses terminal payoff per unit invested in its utility expressions. Subtracting one converts gross returns into net returns and changes the intercept correspondingly; factor premiums and pricing discrepancies are unchanged. The historical illustration quotes conventional net annual percentage returns. A reproduction should not insert a 5.1% net rate as the entire gross terminal payoff in a wealth-utility equation.

## Counterexample: diversification does not settle the economic argument

Section I, pages 344–346, considers independent normal risky returns and a single investor with constant absolute risk aversion:

$$
U(z)=-e^{-Az},\qquad A>0.
$$

With initial wealth $w$, riskless return $\rho$, and risky weights $\alpha_i$, maximizing expected utility is equivalent to maximizing the normal certainty equivalent. When return variances equal $\sigma^2$, first-order conditions are

$$
E_i-\rho=A w\sigma^2\alpha_i.
$$

There are two economically different ways to enlarge the market. First, add assets in positive supply. Let asset $i$ pay an independent normal amount $\widetilde c_i$ with mean $\bar c_i$ and payoff variance $c^2$, and let its price be $p_i$. If each is in unit supply, $p_i=w\alpha_i$. Since its return variance is $c^2/p_i^2$, the asset-specific version of the first-order condition gives

$$
p_i=\frac{\bar c_i-Ac^2}{\rho},\qquad
E_i=\frac{\bar c_i}{p_i}
=\rho\frac{\bar c_i}{\bar c_i-Ac^2}.
$$

This calculation switches from a normalized return variance to a payoff variance; they should not be held numerically equal after dividing by price. Assume positive prices, with payoff means sufficiently above $Ac^2$. Adding more independent assets does not change an existing asset's price or expected return in this example. Its premium can remain positive even though there is no common risk factor. Aggregate wealth $w=1+\sum_i p_i$ grows, and relative risk aversion $Aw$ grows with it. The diversification benefit is offset by investors' greater aversion to proportional risk.

Second, hold wealth fixed and add investment activities rather than endowed assets. For irreversible activities use nonnegative weights with $\sum_i\alpha_i\le1$. The same first-order relation now implies

$$
\sum_{i=1}^n|E_i-\rho|
=Aw\sigma^2\sum_{i=1}^n\alpha_i
\le Aw\sigma^2.
$$

Expected-return discrepancies are summable under this alternative interpretation. It does not follow that each fixed asset's premium falls with $n$; the claim concerns the cross-sectional sequence and its diminishing average. The contrast isolates the missing economic ingredient in a naive large-number-of-assets argument. The number of investment opportunities and the wealth generated by supplying those assets cannot be treated interchangeably.

This section is an analytical construction, not a fitted market example. The paper does not estimate $A$, calibrate payoff means, or simulate the utility-maximizing portfolios. Its role is to disprove an unconditional diversification claim and motivate the preference restriction used next.

## Preference restriction and the individual-investor theorem

A Type B investor has increasing, concave utility and uniformly bounded relative risk aversion on the relevant wealth domain:

$$
\sup_z\left[-\frac{zU''(z)}{U'(z)}\right]<R<\infty.
$$

The paper uses the comparison of risk aversion to represent $U$ as an increasing convex transformation $G$ of constant-relative-risk-aversion utility $U_R$. For $R\ne1$, $U_R(z)=z^{1-R}/(1-R)$; for $R=1$, $U_R(z)=\log z$. Thus $U=G\circ U_R$. Convexity of $G$ will transfer a strict utility improvement for the reference CRRA investor into one for the less risk-averse Type B investor.

Assumption 1 requires at least one limited-liability asset: its terminal payoff per unit invested is bounded below by $-t$ for some finite $t$. This supplies an outside investment with bounded downside. It does not impose long-only constraints on the arbitrage portfolios; their construction permits positive and negative positions.

Theorem I, pages 347–350, considers an optimal portfolio sequence $\alpha_n^0$ for a Type B investor in the growing markets. If its expected return is uniformly bounded above,

$$
(\alpha_n^0)'E_n\le m<\infty,
$$

then there exist a scalar $\rho$ and a fixed $k$-vector $\gamma$ such that

$$
\sum_{i=1}^{\infty}(E_i-\rho-\beta_i\gamma)^2<\infty.
$$

The result is intended to hold for arbitrary sequences of investor wealth, not only fixed wealth. Its proof also relies on the expected-utility convergence condition discussed in Appendix 2. That qualification is part of the substantive assumptions even though it is not numbered among Assumptions 1–5.

If a riskless asset exists, Corollary 1 permits $\rho$ to be its return. The proof uses excess returns $E_n-\rho e_n$ and finances positions with the riskless asset, eliminating the separate zero-investment constraint on risky holdings. Without a riskless asset, $\rho$ is an intercept associated with zero-factor-exposure diversified portfolios; exact equality of the returns on every finite zero-beta portfolio is stronger than the approximate theorem establishes.

## Constructing the portfolio and reconstructing the proof

Fix a target payoff $c>m+t$. Among zero-investment, factor-neutral portfolios with expected payoff $c$, solve

$$
\min_{\eta}\eta'V_n\eta
\quad\text{subject to}\quad
\eta'e_n=0,\quad \eta'B_n=0,\quad \eta'E_n=c.
$$

These are equation (19)'s constraints. They are feasible unless expectations already lie in the span of $e_n$ and $B_n$. Remove redundant factors and address zero residual variances separately; the displayed inverse formula assumes full column rank and positive residual variances. Define

$$
X_n=[E_n\ B_n\ e_n],\qquad b=(c,0,\ldots,0)' .
$$

The Lagrange equations and the unique minimum-variance portfolio are

$$
\eta_n=V_n^{-1}X_n(X_n'V_n^{-1}X_n)^{-1}b,
\qquad
v_n=b'(X_n'V_n^{-1}X_n)^{-1}b.
$$

These expressions give an immediately implementable version of the construction. Numerically, solve the linear systems rather than explicitly invert ill-conditioned matrices, and check all three constraints. The paper itself is proving existence, not prescribing a finite-data optimizer or regularization rule.

Suppose a subsequence has $v_n\to0$. Then the constructed payoff converges in mean square to $c$. Adding it to a unit investment in the limited-liability asset gives a payoff bounded below by the arbitrage payoff minus $t$, which converges to $c-t>m$. By the maintained utility-continuity condition, its reference-CRRA expected utility eventually exceeds $U_R(m)$. CRRA homogeneity factors out wealth; when $R=1$, logarithmic utility separates wealth additively. Jensen's inequality applied to the increasing convex function $G$ transfers this improvement to the actual investor. But concavity had bounded the utility of the alleged optimum by $U(w_nm)$. This contradicts optimality.

Therefore these target-payoff portfolios must have variance uniformly bounded away from zero: $v_n\ge a>0$. The remaining question is linear algebra: how does a lower bound on their variance force a bounded sum of pricing discrepancies? Appendix 1 supplies the required compactness argument.

Set $H_n=V_n^{-1}$. Because residual variances have an upper bound, the diagonal elements satisfy $H_{ii}\ge h=1/\bar\sigma^2>0$. The appendix lemma states that if

$$
b'(X_n'H_nX_n)^{-1}b\ge a>0,
$$

then a single vector $z^*$ exists with $b'z^*=1$ and $\sup_n\|X_nz^*\|_2^2<\infty$. To see the mechanism, minimize $z'X_n'H_nX_nz$ subject to $b'z=1$. The solution is

$$
z_n=\frac{(X_n'H_nX_n)^{-1}b}{b'(X_n'H_nX_n)^{-1}b},
\qquad
z_n'X_n'H_nX_nz_n\le\frac1a.
$$

Hence $\|X_nz_n\|^2\le1/(ha)$. Choose a fixed nonsingular row submatrix of $X_n$. Its fitted values are bounded, so its coefficient vectors have a convergent subsequence. Nested rows ensure that the limiting coefficient vector satisfies the same norm bound for every finite $n$. It also preserves $b'z^*=1$.

Since the first coordinate of $z^*$ is $1/c$, write $cz^*=(1,-\gamma',-\rho)'$. Multiplying the bound by $c^2$ yields the square-summability conclusion. The fixed limiting coefficients are essential: merely obtaining a different bounded-error regression for each finite universe would not yet prove the existence of one infinite-sequence pricing relation.

## Utility tails are not a dispensable technicality

Appendix 2, pages 358–359, explains why mean-square convergence alone is insufficient. A payoff can be almost constant with high probability yet have a sufficiently severe rare loss to dominate expected utility near a lower wealth boundary. Independent idiosyncratic shocks with uniformly bounded variances do not automatically eliminate this problem.

If utility is concave, bounded below on its domain, and evaluated on admissible wealths, Fatou's lemma supplies the lower bound on limiting expected utility; Jensen supplies the upper bound. For utilities unbounded below, the paper assumes uniform integrability of the transformed payoff sequence:

$$
\lim_{K\to\infty}\sup_n
E\left[|U(Z_n)|\mathbf1\{|U(Z_n)|\ge K\}\right]=0.
$$

A sufficient condition is $\sup_nE|U(Z_n)|^{1+\delta}<\infty$ for some $\delta>0$, together with convergence in probability to an interior admissible payoff. Suitable integrable lower bounds combined with concavity can also deliver the needed expected-utility convergence. The payoff sequence must stay within the utility's domain; convergence toward a positive constant does not itself ensure this for every finite $n$.

These requirements explain why the proof cannot be reduced to a variance calculation alone. In particular, a low-variance leveraged portfolio with a small probability of bankruptcy is not automatically equivalent to a safe increment for an investor with logarithmic or power utility. The article explicitly acknowledges this in its second appendix. Any claim that its theorem is preference-free should be qualified accordingly.

## From one investor to a market pricing relation

Theorem I assumes a bounded optimal expected return. Theorem II derives the required restriction from market-wide conditions. Beyond limited liability and the factor structure, the numbered assumptions are: at least one Type B investor remains nonnegligible; all investors share the expected-return vector and are risk averse; aggregate desired holdings in every asset are nonnegative; and $\sup_i|E_i|<\infty$.

Nonnegligibility means that the Type B investor's wealth share does not vanish along the relevant expanding-market sequence. In applying the proof, the share must remain material on the subsequence where the investor's optimal expected return would diverge. The article defines negligibility through convergence of the share to zero and invokes its complement in the proof; a uniform positive lower bound is the transparent sufficient operational interpretation and avoids pathological subsequence changes.

Let $\omega^0$ be that investor's wealth share and $\widehat\omega$ the rest of the market's share. Aggregate portfolio weights are $\xi_i=\omega^0\alpha_i^0+\widehat\omega\widehat\alpha_i$, with $\xi_i\ge0$ and $\sum_i\xi_i=1$. Bounded individual expectations imply that $\sum_i\xi_iE_i$ is bounded. If the Type B investor's expected portfolio return diverged upward with a nonvanishing weight, the remaining investors' wealth-weighted expected return would have to diverge downward. Common expected returns, risk aversion, and the limited-liability outside asset rule out optimal choices with such arbitrarily bad expected performance. Thus the hypothesized failure of approximate factor pricing cannot persist.

Aggregate nonnegative demand does not mean every investor is long-only or that the market is exactly clearing. Some assets may be in excess supply. This is why Ross interprets the conclusion as an arbitrage-based stability relation applicable beyond an exact equilibrium. The needed aggregate boundedness can also follow if gross aggregate exposure $\sum_i|\xi_i|$ is uniformly bounded, rather than every aggregate weight being nonnegative.

The proof is framed for a conventional population of agents. When extending it to a changing or infinite agent population, one must control the aggregation and subsequence arguments rather than assume an individual with divergent negative performance exists automatically. The source does not provide a full continuum-agent extension.

## Meaning, rates, and factor-portfolio normalization

Write $a_i=E_i-\rho-\beta_i\gamma$ and $C=\sum_i a_i^2<\infty$. Three precise consequences are

$$
a_i\to0\quad(i\to\infty),\qquad
\frac1n\sum_{i=1}^n a_i^2\le\frac Cn,
\qquad
\frac1n\sum_{i=1}^n|a_i|\le\sqrt{\frac Cn}.
$$

The last inequality is Cauchy–Schwarz. For any fixed tolerance $\epsilon>0$, at most $C/\epsilon^2$ assets can have $|a_i|>\epsilon$. These are useful interpretations of the exact theorem. They do not give the unknown constant $C$, nor show that a particular named asset's discrepancy disappears merely because more assets are listed. No uniform pointwise convergence rate is established.

If there are portfolios with unit exposure to one factor and zero exposure to the others, their approximate expected excess returns identify the corresponding $\gamma_j$. Under the appropriate normalization, equation (24) becomes

$$
E_i-\rho\approx\sum_{j=1}^k\beta_{ij}(E^j-\rho).
$$

The factor-mimicking portfolios must be well diversified enough for their pricing-error component to be negligible. For an arbitrary finite portfolio $w$, the exact relation includes $w'a$; unit factor exposure alone does not remove that error. The notation $E^j$ therefore should not be interpreted as an exact common return for every finite portfolio with that loading.

The factor basis is not uniquely identified. An invertible rotation of common factors and the inverse transformation of loadings leaves the return model unchanged; prices of factor risk transform correspondingly. The theorem restricts a span, not the labels of particular macroeconomic variables. It does not single out the market portfolio as the only priced factor, require it to be mean-variance efficient, or prescribe how many factors a researcher should estimate from data.

## The numerical illustration and what it does not estimate

Pages 353–354 derive a variance-weighted discrepancy bound,

$$
\sum_{i=1}^n\frac{a_i^2}{\sigma_i^2}\le\frac{c^2}{a},
$$

where $c$ is the target premium and $a$ is a lower bound on the variance of a portfolio attaining it under the relevant neutrality/financing constraints. This is more informative than a uniform unweighted bound because noisy assets can support larger pricing discrepancies.

Ross gives an illustrative calibration, not an empirical test. For January 1, 1962–December 31, 1971, the cited S&P Composite annual mean return is 7.4%, the mean yield on prime corporate securities with one year to maturity is 5.1%, and market volatility is 12.3%. Thus $c=0.023$. The corporate yield is the paper's risk-free proxy, not a modern default-free Treasury definition.

The key maintained assumption is that no relevant arbitrage portfolio earning the market premium can have less than half the market variance, giving $a=\tfrac12(0.123)^2$. The paper then substitutes average market-regression residual variance $2(0.123)^2$ for each $\sigma_i^2$. These are strong approximations: an average residual variance does not rigorously replace heterogeneous denominators, and the half-market-variance assumption is not demonstrated from return data.

With about 3,000 NYSE and Amex issues at December 31, 1971, the resulting illustrative average absolute discrepancy bound is

$$
\frac1n\sum_i|a_i|
\lesssim\frac{2(0.023)}{\sqrt{3000}}
=0.00084.
$$

That is approximately **8.4 basis points per year**, or 0.084 percentage points, about 1.1% of the 7.4% market return. It is not an 0.084% probability, a confidence interval, or a universal bound on each asset's alpha. The paper explicitly treats ex ante expectations as if observed ex post averages could proxy for them and calls the calculation crude. There are no standard errors, asset-level estimates, holdout periods, or reported tests of the assumed variance floor.

The cited market and residual statistics come from earlier studies by Friend and Myers. The article does not provide a constituent list, complete return file, missing-data or delisting treatment, covariance estimator, regression window details, or full-precision calibration. Exact data replication therefore cannot be completed from this PDF alone. Its arithmetic can be reproduced directly, while its empirical premises must be separately reconstructed and evaluated.

## Generalizations and the reproducible research boundary

Section III permits greater heterogeneity than the CAPM's usual common-distribution assumption. Other investors need not share the Type B investor's entire joint distribution. They can disagree about factor distributions and residual tails while sharing the expected-return vector required for the aggregation argument. This is weaker homogeneity of beliefs, but not arbitrary disagreement about expected returns. Opposing subjective means can support offsetting positions and undermine the boundedness argument.

The article also suggests weakening residual independence requirements. Mutual uncorrelatedness is already weaker than independence. If residual covariances vanish beyond a fixed cross-sectional separation, with uniformly bounded variances, covariance operator norms remain bounded and the diversification argument extends. More general laws of large numbers may support weaker approximation norms. The paper does not prove that any empirically correlated residual structure, or any slowly decaying common component, preserves its square-summability theorem.

For a computational reconstruction, one can specify $E_n,B_n,V_n$, solve the constrained portfolio problem, and verify that the variance equals the stated quadratic form. A useful equivalent calculation projects $E_n$ on $[e_n,B_n]$ in the $V_n^{-1}$ metric. If $a_n$ is that weighted residual, then the target-payoff neutral portfolio is $cV_n^{-1}a_n/(a_n'V_n^{-1}a_n)$ and its variance is $c^2/(a_n'V_n^{-1}a_n)$. This identity is derived from the same constraints and makes the relation between pricing dispersion and an increasingly attractive neutral trade explicit. It is a reconstruction aid, not a numerical experiment reported in the source.

Estimating the inputs from a finite return panel introduces a different problem: factor estimation, errors in loadings, noisy expected returns, joint-test inference, and model selection. The paper supplies no estimator or experimental protocol for those tasks. It also has no transaction costs, borrowing fees, short-sale limits, margin calls, turnover, or rebalancing rule. Such restrictions can prevent the theoretical portfolios from being implemented at the scale assumed by the argument.

The lasting contribution is the precise bridge from diversifiable residual risk to approximately linear expected returns, together with the counterexample and tail conditions that keep the bridge honest. A fitted factor model alone does not prove an alpha is arbitrage; a small residual variance alone does not prove investors regard the trade as safe. The theorem explains the economic and mathematical conditions under which cross-sectional pricing discrepancies become difficult to sustain, while leaving factor discovery and finite-sample empirical validation to subsequent work.

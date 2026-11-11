# The strategy approval decision: A Sharpe ratio indifference curve approach

David H. Bailey, Marcos López de Prado, and Eva del Pozo. *Algorithmic Finance* 2 (2013), pp. 99–109. DOI: 10.3233/AF-13018. Source: [SharpeRatio_BaileyLopezdepradoDelpozo_2013.pdf](../../Finance/SharpeRatio_BaileyLopezdepradoDelpozo_2013.pdf), 11 pages.

## Why this matters

A new strategy should not be approved solely because its standalone Sharpe ratio exceeds a fixed threshold. Its value depends on the portfolio it joins. A lower-Sharpe strategy can improve aggregate risk-adjusted performance through diversification, while an attractive standalone strategy can contribute little if it duplicates existing exposures. This paper turns that observation into a two-dimensional approval curve relating a candidate's Sharpe ratio to its average correlation with the approved strategies.

The result is an exact moment calculation for an equal-standalone-volatility benchmark. It is not a general solution of constrained portfolio optimization, an estimator that removes Sharpe-ratio uncertainty, or a proof that strategies below the curve have no economic value. Its principal advantage is organizational: it makes the diversification requirement explicit before strategy approval and gives research teams a common benchmark for comparing candidates.

The main approval formula is correct under its assumptions. Several printed appendix expressions contain consequential algebraic errors: covariance terms omit volatility factors, and two correlation derivatives have an incorrect power of the diversification denominator. A prose proposition also misstates the direction of the effect of adding strategies. This note derives the correct formulas rather than reproducing those errors.

## Model and exposure convention

There are $S$ strategies with excess-return means $\mu_s$, strictly positive volatilities $\sigma_s$, and pairwise correlations $\rho_{st}$. All moments must refer to the same return interval and consistent financing and fee conventions. The paper assumes jointly normal returns, although its portfolio mean, variance, and Sharpe identities require only finite second moments.

Define the standalone Sharpe ratio of strategy $s$ as $q_s=\mu_s/\sigma_s$, the arithmetic average Sharpe ratio as

$$
\bar q=\frac1S\sum_{s=1}^S q_s,
$$

and the average off-diagonal correlation as

$$
\bar\rho=\frac{2}{S(S-1)}\sum_{s<t}\rho_{st}.
$$

The benchmark uses exposures $w_s=1/(S\sigma_s)$. Thus each standalone strategy contributes the same dollar-volatility scale before accounting for correlations. These are not generally weights summing to one. A common positive rescaling can normalize the total exposure without changing its Sharpe ratio under linear excess-return financing, but constraints, borrowing spreads, fees, and position limits can make such rescaling economically nontrivial.

Equal standalone volatility also does not generally mean equal contributions to portfolio risk. Strategy $s$ has a risk contribution proportional to the sum of row $s$ of the correlation matrix under these exposures. Those row sums need not be equal. Calling the construction equal-risk-contribution without an additional symmetry condition would be incorrect.

An especially transparent derivation standardizes the strategy returns: $z_s=r_s/\sigma_s$. Then $E[z_s]=q_s$ and $\operatorname{Var}(z_s)=1$. A portfolio proportional to $\sum_s z_s$ has mean $S\bar q$ and variance

$$
V=S+S(S-1)\bar\rho.
$$

Its Sharpe ratio is therefore

$$
B(S,\bar q,\bar\rho)
=\frac{S\bar q}{\sqrt{S+S(S-1)\bar\rho}}
=\bar q\sqrt{\frac{S}{1+(S-1)\bar\rho}}.
$$

The denominator must be positive. A zero-variance standardized aggregate is a singular case, not a finite Sharpe ratio to which the formula can be applied mechanically. For $S>1$, positive semidefiniteness implies $\bar\rho\ge-1/(S-1)$, but that scalar inequality alone does not validate a proposed full correlation matrix.

## Diversification comparative statics

Let $\alpha=1+(S-1)\bar\rho$. For a positive average Sharpe ratio,

$$
\frac{\partial B}{\partial\bar q}=\frac{\sqrt S}{\sqrt\alpha},
\qquad
\frac{\partial B}{\partial\bar\rho}
=-\frac{\bar q\sqrt S(S-1)}{2\alpha^{3/2}}.
$$

The effect of correlation becomes larger in magnitude as the diversification denominator gets small. The second derivative is

$$
\frac{\partial^2B}{\partial\bar\rho^2}
=\frac{3\bar q\sqrt S(S-1)^2}{4\alpha^{5/2}}>0.
$$

Thus Sharpe decreases with correlation but is convex in it when $\bar q>0$. Lowering correlation by a fixed amount has greater value when starting at a lower feasible correlation. The cross derivative is

$$
\frac{\partial^2B}{\partial\bar q\,\partial\bar\rho}
=-\frac{\sqrt S(S-1)}{2\alpha^{3/2}}.
$$

Treating $S$ temporarily as continuous while keeping $\bar q$ and $\bar\rho$ fixed gives

$$
\frac{\partial B}{\partial S}
=\frac{\bar q(1-\bar\rho)}{2\sqrt S\,\alpha^{3/2}}.
$$

For $\bar q>0$ and $0\le\bar\rho<1$, this is positive and decreases as $S$ grows: the benchmark Sharpe rises with diminishing marginal gains. The paper's Proposition 2 says “decreasing” in describing the number-of-strategies dependence, while its figure and the correct appendix derivative indicate increasing behavior. The relevant economically usual result is increasing and concave over this nonnegative-correlation range. One should not extend concavity unqualified to every feasible negative correlation.

For fixed positive $\bar\rho$, the limiting Sharpe is $\bar q/\sqrt{\bar\rho}$. If average correlation is zero, it grows as $\bar q\sqrt S$. A fixed negative average correlation cannot be held constant while taking $S$ to infinity because it eventually violates the positive-semidefinite lower bound. The large-$S$ limit is therefore conditional on an admissible sequence of portfolios, not a license to extrapolate a finite negative-correlation example indefinitely.

The paper illustrates these relationships with $S=16$. At $\bar q=0.75$ and $\bar\rho=0.20$, $B=1.50$. Reducing average Sharpe to 0.50 gives $B=1.00$; retaining 0.50 but increasing correlation to 0.30 gives approximately 0.8528. These are arithmetic examples with assumed known moments, not empirical estimates of achievable fund performance.

## Adding a candidate and deriving the indifference curve

Let the candidate have standalone Sharpe ratio $q$ and correlations $a_s$ with the $S$ existing strategies. Write its average correlation as $c=S^{-1}\sum_s a_s$. After adding it with the same standalone-volatility allocation convention, the portfolio Sharpe is

$$
B_{\mathrm{new}}(q,c)
=\frac{S\bar q+q}{\sqrt{V+1+2Sc}}.
$$

This expression is exact: the candidate adds its standardized mean, one unit of standardized variance, and twice its aggregate covariance with the old standardized sum. The complete correlation vector affects feasibility and optimized weighting, but for this particular benchmark its average alone determines the aggregate variance increment.

Equivalently, the enlarged set has

$$
\bar q_{\mathrm{new}}=\frac{S\bar q+q}{S+1},\qquad
\bar\rho_{\mathrm{new}}
=\frac{S(S-1)\bar\rho+2Sc}{S(S+1)}.
$$

Substitution in the portfolio formula gives the same result. This identity is useful as a coding check: computing the augmented full covariance matrix and computing the three scalar aggregates must agree.

For a desired positive target Sharpe $B_*$, assume $S\bar q+q>0$ and $V+1+2Sc>0$. Squaring $B_{\mathrm{new}}\ge B_*$ and rearranging gives

$$
c\le c_{\max}(q;B_*)
=\frac12\left[
\frac{(S\bar q+q)^2}{S B_*^2}
-\frac{S+1}{S}-(S-1)\bar\rho
\right].
$$

The equality is the Sharpe-ratio indifference curve. A candidate below the curve has sufficiently low correlation to attain at least the target under the specified allocation. The equivalent minimum-Sharpe requirement is

$$
q\ge B_*\sqrt{V+1+2Sc}-S\bar q.
$$

The sign condition on the numerator matters. Squaring an inequality without it can admit candidates with a large negative aggregate mean whose squared Sharpe happens to equal the target's square. Those candidates do not attain a positive target Sharpe. The variance condition also excludes the singular boundary where the ratio is undefined.

Setting $B_*$ equal to the current benchmark Sharpe answers whether the candidate preserves or improves the existing benchmark. Setting it higher answers a different question: whether the candidate matches a preferred alternative or a new policy hurdle. The paper's central three-strategy example uses the latter comparison; confusing its target with the original two-strategy Sharpe changes the approval decision.

## Worked approval example

Start with two strategies whose average Sharpe is 1 and whose correlation is 0.10. Then $V=2.2$ and the existing benchmark Sharpe is $2/\sqrt{2.2}=1.348400$. A third strategy with $q=1$ and $c=0.10$ yields

$$
B_{\mathrm{new}}=\frac3{\sqrt{3.6}}=1.581139.
$$

Use 1.581139 as the comparison target. The indifference curve then permits a candidate with $q=1.5$ to have average correlation 0.425. A much weaker candidate with $q=-0.1$ must have average correlation −0.439 to attain the same target. Direct substitution gives 1.581139 in both cases. The negative standalone Sharpe is compensated by enough negative covariance with the existing portfolio.

A candidate with $q=0.7$ and $c=0.10$ produces 1.423025. It improves the old 1.348400 benchmark but fails to match the preferred 1.581139 alternative. Raising its correlation to 0.20 produces 1.350000, only slightly above the original benchmark. These are different approval questions, so a statement that a candidate “fails” must identify its hurdle.

This negative-Sharpe example should not be described as guaranteed downside insurance. The model is linear and based on unconditional covariance. Negative average correlation does not establish a convex payoff in a crash, robust hedging under regime change, or reliable liquidity when other positions lose money. Under jointly normal returns the diversification arithmetic is particularly transparent, but tail protection is a separate economic claim.

## Correlation feasibility is an additional constraint

An indifference curve drawn over $-1\le c\le1$ includes points that may not correspond to any valid joint distribution with the existing strategies. Let $C$ be the existing correlation matrix and $a$ the vector of candidate correlations. When $C$ is positive definite, the augmented matrix is positive semidefinite exactly when

$$
\begin{pmatrix}C&a\\a^\top&1\end{pmatrix}\succeq0
\quad\Longleftrightarrow\quad
1-a^\top C^{-1}a\ge0.
$$

This is the Schur-complement condition. If $C$ is singular, a corresponding range condition and generalized inverse are needed; a naive inverse is not valid.

Even without the full vector, Cauchy–Schwarz supplies a scalar necessary bound. The candidate has covariance $Sc$ with the old standardized sum, whose variance is $V$. Therefore

$$
|c|\le\frac{\sqrt V}{S}
=\sqrt{\frac{1+(S-1)\bar\rho}{S}}.
$$

For the two-strategy example, this bound is $\sqrt{0.55}\approx0.74162$. Both 0.425 and −0.439 are feasible when each correlation with the old strategies equals the stated average. More generally, a feasible average does not validate an arbitrary proposed correlation vector. A candidate may satisfy the scalar approval formula yet fail the actual correlation-matrix check.

The distinction becomes particularly important when many nearly collinear strategies are already present. Estimation noise can produce an indefinite sample matrix after separately estimated pairwise correlations are combined. Regularizing that matrix changes the average correlation and the approval frontier. The note's feasibility check is an implementation requirement derived from the model, not an empirical procedure supplied by the article.

## Exact formulas versus printed appendix errors

The ordinary portfolio variance is

$$
\sigma_P^2=\sum_s w_s^2\sigma_s^2
+2\sum_{s<t}w_sw_t\sigma_s\sigma_t\rho_{st}.
$$

The source's Appendix equations (3) and (4), on PDF page 10, omit $\sigma_s\sigma_t$ in cross terms while defining $\rho_{st}$ as correlation. The omission is dimensionally incorrect: a correlation alone has no return-squared scale. Substitution of inverse-volatility exposures works correctly only when these volatility factors are present, at which point they cancel as expected. The paper's resulting benchmark formula, equation (7), is consistent with the corrected variance expression.

The same page's equations (9) and (10) display a square-root expression with the wrong power of $\alpha$ in derivatives involving correlation. Differentiating $\bar q\sqrt S\alpha^{-1/2}$ requires $\alpha^{-3/2}$, as shown above, not multiplication by $\alpha^{1/2}$. A derivative used in sensitivity analysis would be materially wrong if copied literally.

The central approval equations (13) and (14) are consistent with the correctly derived aggregate mean and variance. These local errors therefore do not invalidate the indifference curve. They do mean that an implementation should derive from the standardized-return portfolio rather than translate every printed appendix equation line by line. The distinction between a valid central result and invalid ancillary formulas is essential to a fair assessment of the paper.

## Relation to optimization and strategy selection

The benchmark is a screening device with a prescribed allocation rule. It is not the maximum-Sharpe portfolio. If a new strategy can receive zero weight, enlarging the feasible set of a true portfolio optimization cannot reduce its maximum objective: the old portfolio remains feasible. By contrast, forcing the new strategy to receive the same standalone-volatility allocation as every existing strategy can reduce the benchmark Sharpe. Rejection under this rule means rejection under that allocation convention, not proof that no beneficial allocation exists.

Likewise, saying that optimization will necessarily improve strictly on the benchmark is too strong. The benchmark may already be optimal, or constraints may prevent a different solution. A weak inequality is justified when the benchmark belongs to the optimization's feasible set and the same population moments and objective are used. Out of sample, estimation error can reverse the comparison between a highly optimized portfolio and a stable benchmark.

Sequential approval is also path dependent. The value of candidate A is assessed against whichever strategies have already been approved. Two candidates rejected separately may work well together, while two individually attractive candidates may duplicate each other. The paper's scalar frontier evaluates one candidate at a time; it does not solve combinatorial subset selection or account for research-development costs.

The conclusion is especially sensitive to the meaning of “strategy.” Splitting one economic exposure into several labels changes the count $S$ and can change its total weight under equal standalone volatility. A robust organizational implementation should define strategy units consistently and inspect common underlying exposures. Correlation provides some protection against duplication but does not itself fix arbitrary changes in the allocation rule caused by relabeling.

## Estimation, implementation, and incentives

To reproduce the paper's numerical figures one needs only the stated population inputs and the equations above. To use the method in an investment business, the required inputs are considerably richer: synchronized net return histories, a common financing convention, stable estimates of means and volatilities, the full correlation matrix, trading costs, capacity constraints, and an allocation policy that can actually be implemented. The article does not estimate these from a disclosed empirical dataset.

Means are generally much less precisely estimated than volatilities, and candidate strategies are often selected after extensive backtesting. The approval frontier takes $q$ and $c$ as given; it contains no sampling distribution, confidence region, selection-bias correction, or holdout requirement. A point just inside the curve is not statistically distinguishable from one just outside it without an uncertainty analysis. A faithful implementation should display both the population-style decision and its sensitivity to plausible moment estimates.

Correlation estimates should use returns at a frequency appropriate to the economic exposures. Illiquid marks, asynchronous prices, overlapping positions, and dynamic leverage can distort apparent diversification. A low unconditional correlation can disappear in stressed markets. Joint normality rules out some tail asymmetries but does not make a noisy estimate of correlation reliable.

The paper connects strategy approval to compensation and team incentives. Its organizational argument is that researchers and portfolio managers should be rewarded for the contribution of their strategies to the combined portfolio, rather than standalone performance alone. That implication follows naturally from the diversification examples. More specific claims about bargaining power, replaceability, and the cost of obtaining low-Sharpe diversifiers are economic conjectures in the discussion, not results of a formal agency model or empirical compensation study.

A defensible operational sequence is to define the current benchmark exposures; compute its full-matrix moments and the scalar summary; estimate each candidate using the same conventions; verify augmented-matrix feasibility; evaluate the candidate against an explicit target; and separately run constrained portfolio optimization and stress scenarios. The first five steps reproduce the article's question. The final optimization and stress work address questions the article deliberately leaves open.

The resulting report should distinguish three outcomes: improvement over the current equal-volatility benchmark, attainment of a preferred higher target, and improvement in a constrained implementable portfolio. Those outcomes can differ, as the $q=0.7$ example demonstrates. A single green/red approval label can hide that difference.

## Source and verification record

All eleven PDF pages, including the mathematical appendix and references, were read. PDF pages 4–8 and 10–11 were visually checked for comparative-static plots, approval examples, equations, and appendix details. The principal example values and both indifference points were independently calculated. Covariance normalization, derivatives, numerator-sign restrictions, and correlation feasibility were checked algebraically. The paper supplies illustrative arithmetic rather than an empirical return panel, so no out-of-sample performance replication is claimed.

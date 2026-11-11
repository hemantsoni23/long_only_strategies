# Coherent measures of risk in everyday market practice

**Carlo Acerbi.** Abaxbank article dated April 24, 2008; an earlier version was presented in Dublin on June 8, 2006. **Source:** [RiskManagement_Acerbi_2008.pdf](../../Finance/RiskManagement_Acerbi_2008.pdf), 11 pages, inspected in full, including Figures 1–3 and the optimization formulations. This is a practical review of previously developed results, not a new empirical test. Page references below are PDF pages, which coincide with the printed pages.

For the numerical inputs underlying Figures 1–2, the cited local chapter [RiskManagement_Acerbi_2003.pdf](../../Finance/RiskManagement_Acerbi_2003.pdf) was consulted specifically at Example 2.15, pp. 22–23, and Examples 4.3–4.4, pp. 54–55. Those passages supplement missing inputs in the short article; the entire chapter is not represented as having been summarized here.

## Why this matters

Most work in a portfolio risk engine occurs before the final risk statistic is calculated: constructing joint scenarios, modeling risk factors, and repricing instruments. Replacing a quantile statistic with a coherent tail statistic can preserve that expensive infrastructure. The article asks which coherent measures fit such a distribution-based workflow and how to estimate and optimize them without losing the main computational advantage of coherence.

The proposed practical filter adds law invariance and comonotonic additivity to the four coherence axioms. Under the relevant representation assumptions, this identifies spectral measures: decreasing probability-rank-weighted averages of portfolio profits. The article then gives exact finite-scenario estimators and linear-program formulations for ES and general spectral measures.

Its value is the connection between preference specification, a scenario engine, and an optimizer. Several statements in the discussion are stronger than the mathematics justifies. A faithful implementation should preserve convexity and the scenario formulas while distinguishing them from claims of unique optima, automatic statistical consistency, or unrestricted computational tractability.

## Coherence and the diversification benefit

Let $X$ and $Y$ be profits and losses over one chosen horizon, with low values adverse and positive $\rho$ denoting required capital. Define

$$
H(X,Y;\rho)=\rho(X)+\rho(Y)-\rho(X+Y).
$$

Subadditivity requires $H\ge0$. Together with cash translation, positive homogeneity, and monotonicity, it defines coherence. The article interprets $H$ as the capital relief from combining positions. A negative value means that separately capitalizing the components can cost less than capitalizing their aggregate, inviting organizational rather than economic risk reduction.

For a portfolio $Y_w=\sum_kw_kX^{(k)}$, coherence implies convexity in the **holding weights**:

$$
\rho(Y_{\lambda w+(1-\lambda)v})
\le\lambda\rho(Y_w)+(1-\lambda)\rho(Y_v),\quad0\le\lambda\le1.
$$

This result assumes an affine payoff mapping in the decision variables. Derivatives can be highly nonlinear in market factors while remaining linear in the number of contracts held, so nonlinear option valuation does not by itself invalidate it. Market impact depending nonlinearly on the chosen holdings, integer lots, or cardinality constraints can change the optimization problem.

Convexity rules out strictly inferior local minima on a convex feasible set. It does not imply a unique minimizer or strict convexity. Flat optimal faces are normal in the linear programs described later. The article's language about a single global minimum should therefore be read as a claim about particular illustrated examples, not a general theorem for every coherent measure.

## A counterexample with normal marginals

Section 2 warns that Gaussian marginal distributions do not ensure VaR subadditivity. Its equation (3) writes a singular dependence construction using Dirac deltas. This is a formal copula **density/measure** representation, not an ordinary copula cumulative distribution function.

A direct simulation-free construction makes the model precise. Let $U$ be uniform on $(0,1)$, choose tail probability $p=0.01$, and put $q=p+\epsilon=0.0101$. Define

$$
V=\begin{cases}q-U,&0<U<q,\\U,&q<U<1.\end{cases}
\qquad X=\Phi^{-1}(U),\quad Y=\Phi^{-1}(V).
$$

The mapping preserves the uniform distribution, so both $X$ and $Y$ are standard normal. The worst 1.01% of ranks are paired in reverse order; the remaining ranks are paired identically. The joint distribution is singular and not bivariate normal.

The article gives the rough figures $2.4+2.4-5.2\approx-0.4$ for the VaR hedging benefit. Recomputing the stated construction more precisely yields individual 1% profit-left-tail VaR about 2.32635 and aggregate VaR about 5.14480, hence $H\approx-0.49211$. The aggregate threshold follows from the two tail intervals each of probability $p/2$:

$$
\operatorname{VaR}_p(X+Y)
=-\Phi^{-1}(p/2)-\Phi^{-1}(q-p/2).
$$

These recalculated values clarify the article's approximate arithmetic; the direction of the result is unchanged. All numbers are in units of the marginal standard deviation, not dollars. The example is a deliberately specified dependence model, not a fitted currency or equity distribution.

The familiar Gaussian subadditivity argument requires jointly Gaussian portfolio returns and a sufficiently adverse quantile, not just normal-looking individual histograms. This is the central practical warning: a marginal diagnostic cannot validate a portfolio aggregation rule.

## Recovering the inputs to the two diversification figures

Figure 1 compares 5% VaR and ES for a long-only mixture of two otherwise identical bonds whose defaults are mutually exclusive. The referenced chapter specifies a price of \$104.60 for each bond, a nondefault payoff of \$108, a 2% soft-default probability with payoff \$100, and a 3% hard-default probability with payoff zero. There are five joint states: hard default of A, soft default of A, hard default of B, soft default of B, and no default, with probabilities 3%, 2%, 3%, 2%, and 90%.

For $Y_\lambda=\lambda X_A+(1-\lambda)X_B$ and $0\le\lambda\le1$, use profits relative to the fixed initial budget \$104.60. An individual bond has profits $-104.6,-4.6,3.4$ in its hard-default, soft-default, and survival states. ES at tail probability 0.05 is $(0.03\times104.6+0.02\times4.6)/0.05=64.6$. At equal weights, both hard-default states have portfolio loss 50.6 and together occupy 6% probability; atom-corrected 5% ES is therefore 50.6.

To reproduce the VaR curve, preserve the chapter's threshold convention at exact cumulative masses: its reported individual 5% VaR is 4.6, corresponding to the lower profit quantile. Switching to the upper quantile can change boundary values. Also, the chapter's no-default A+B table entry says 6.4, while the two component profits sum to 6.8; use the component payoff arithmetic. Neither issue changes the ES comparison.

Figure 2 varies the number of equal-sized independent defaultable bonds rather than weights in a fixed-dimensional portfolio. The chapter specifies price 97, survival payoff 100 with probability 97%, and default payoff zero with probability 3%. For fixed initial budget $B$, let $K\sim\operatorname{Binomial}(N,0.03)$. Portfolio profit is

$$
X_N(K)=\frac{B}{97N}(3N-100K).
$$

Enumerating the $N+1$ binomial states gives VaR, naïve TCE, and atom-corrected ES exactly; simulation is unnecessary. Divide risk values by $B$ to obtain the normalized scale plotted in Figure 2. The threshold jumps in a discrete default-count distribution generate the sawtooth behavior of VaR and TCE as $N$ changes. ES averages fractional mass at the cutoff and behaves much more smoothly.

As the caption correctly notes, this curve against $N$ is not the risk surface against holding weights, so it need not itself be convex. The example supports a qualitative diversification comparison. It supplies no estimate of real default dependence and should not be used to infer that adding correlated issuers always produces the independent-binomial reduction.

## The distribution-first workflow and law invariance

Sections 3–4 contrast a general robust representation,

$$
\rho(X)=\sup_{P\in\mathcal F}E_P[-X],
$$

with a workflow that first specifies one portfolio distribution and then computes a statistic of it. The author calls the latter an objectivist paradigm. The philosophical terminology is not needed to implement the distinction: the former allows a family of probability models, whereas the latter takes a fixed fitted law as the input to the risk functional.

Law invariance means $F_X=F_Y\Rightarrow\rho(X)=\rho(Y)$. It is necessary if the only available input is an iid sample from the marginal law and the estimator is expected to identify a unique risk number. Two positions with the same distribution give statistically indistinguishable samples, so a sample-only procedure cannot consistently identify different target values for them.

Theorem 4.1 informally asserts equivalence between law invariance and estimability. Its forward direction proposes the plug-in estimator $\rho(\widehat F_N)$ but does not establish its convergence for an arbitrary functional, domain, and sampling process. A distributional functional can be evaluated on an empirical law without a consistency theorem following merely from that definition. For the bounded spectral weights and integrable iid profits used in the associated spectral results, consistency has explicit supporting assumptions. Serial dependence, infinite tail moments, or singular/unbounded weights require additional analysis.

Thus the defensible practical statement is that law invariance makes marginal-distribution-based estimation conceptually possible; stability and consistency still need a domain and regularity argument. The review supplies no finite-sample confidence intervals, mixing assumptions for time-series scenarios, or statistical comparison of competing estimators.

Equation (12) illustrates a coherent one-sided-moment measure,

$$
\rho_{p,a}(X)=-E[X]+a\|(X-E[X])^-\|_p,
\quad0\le a\le1,\quad p\ge1.
$$

At $p=2$ the second term is a lower semideviation, the square root of a second lower partial moment. Calling it a semivariance literally would be dimensionally misleading: the norm and the mean both have monetary units, whereas a variance has squared units. This example is used to show that law-invariant coherent measures need not be comonotonic additive.

## Why add comonotonic additivity?

If $X=f(Z)$ and $Y=g(Z)$ for nondecreasing functions $f,g$, both positions rank all states in the same direction. They are comonotonic. The proposed additional requirement is

$$
\rho(X+Y)=\rho(X)+\rho(Y)
$$

for such pairs. They need not be linearly proportional, and comonotonicity should not be confused with a linear correlation of exactly one.

The author views zero hedging benefit for comonotonic positions as part of a complete diversification principle. Coherence alone imposes only nonnegative hedging benefit; it does not force equality in this case. The article describes capital reduction from merging comonotonic books as a second form of regulatory arbitrage. That interpretation is a normative preference for this additional axiom, not a logical consequence of the original four.

Under the probability-space and continuity assumptions of the cited representation theory, law-invariant, comonotonic-additive coherent measures are spectral measures. General representations also need to accommodate a possible worst-case component at probability zero. The short review suppresses those domain and endpoint qualifications, which matter when taking its formulas beyond bounded, finite-scenario applications.

## Spectra and exact empirical weights

A regular spectral functional is

$$
\rho_\phi(X)=-\int_0^1\phi(p)q_X(p)dp,
\quad\phi\ge0,\quad\int_0^1\phi=1,
\quad\phi\text{ nonincreasing}.
$$

Equivalently it is a positive **normalized** mixture of ES levels. Equation (14)'s phrase “any measure” must include total mass one if cash translation is to hold. An arbitrary unnormalized measure would assign the wrong capital reduction to an added unit of cash.

ES has a rectangular spectrum $\alpha^{-1}1_{p\le\alpha}$. Figure 3 uses $\alpha=0.1$, giving height ten on the worst tenth of outcomes. VaR is represented formally by a Dirac mass at the threshold, which fails the decreasing-weight condition because worse outcomes receive no weight.

For equally likely scenarios, sort $y_{1:N}\le\cdots\le y_{N:N}$ and compute the bin-integrated weights

$$
\bar\phi_i=\int_{(i-1)/N}^{i/N}\phi(p)dp,
\qquad \widehat\rho_\phi=-\sum_{i=1}^N\bar\phi_i y_{i:N}.
$$

These are the exact weights of the empirical-CDF plug-in functional, not a point-sampling approximation. They are nonnegative, decreasing, and sum to one. They therefore define a coherent measure on the finite scenario space even before any asymptotic argument is invoked.

For $k=\lfloor N\alpha\rfloor$, ES becomes

$$
\widehat{\operatorname{ES}}_\alpha
=-\frac{\sum_{i=1}^{k}y_{i:N}+(N\alpha-k)y_{k+1:N}}{N\alpha}.
$$

Omit the next term if its weight is zero. For $N\alpha<1$, this is the worst observation, not an undefined empty-tail average. Coherence of the scenario statistic does not imply accurate estimation of an extreme population tail from so little data.

## ES optimization: what the positive-part formulation accomplishes

Let $y_i(w)=\sum_kw_kx_i^{(k)}$, with a fixed common scenario matrix and feasible holdings $w\in\mathcal W$. Equations (21)–(22) introduce

$$
\Gamma_\alpha(w,\psi)=-\psi+
\frac1{N\alpha}\sum_{i=1}^N(\psi-y_i(w))^+.
$$

For fixed $w$, minimizing over $\psi$ returns empirical ES; a minimizing threshold lies in the corresponding empirical quantile interval. Minimizing jointly over $w$ and $\psi$ gives the ES-optimal holdings.

Contrary to one sentence in the source, this objective is not analytic: positive parts have kinks. Its advantage is joint convexity and removal of sorting from the optimization expression. Introducing $z_i\ge0$ and $z_i\ge\psi-y_i(w)$ yields the linear objective $-\psi+(N\alpha)^{-1}\sum_i z_i$. With linear constraints on $w$, the full problem is a linear program.

One should also not interpret the review's warning about naïve sorted optimization as a theorem that every nonsmooth method must fail. The sorted risk is continuous and convex, although its active scenarios change; appropriate nonsmooth algorithms can handle it. The lifted formulation is useful because it exposes a standard optimization structure and avoids requiring a differentiable sorting routine.

The exact LP needs $N$ auxiliary slack variables, one threshold, and the holding variables. It has two inequalities per scenario in addition to the portfolio constraints. The paper does not report runtimes, tolerances, scaling limits, or a solver benchmark. Feasibility, conditioning, and memory remain practical constraints despite the favorable convex structure.

## General spectral optimization and the rank-index issue

Put $d_j=\bar\phi_j-\bar\phi_{j+1}\ge0$ for $j=1,\ldots,N-1$. Equation (23) can be written in a sign-transparent form:

$$
\Gamma_\phi(w,\psi)=
\sum_{j=1}^{N-1}d_j\left\{\sum_{i=1}^N(\psi_j-y_i(w))^+-j\psi_j\right\}
-\bar\phi_N\sum_{i=1}^Ny_i(w).
$$

For a fixed portfolio, the $j$th bracket is minimized for a threshold between the $j$th and $(j+1)$th ordered profits, with value $-\sum_{i=1}^jy_{i:N}$. Telescoping the coefficients gives exactly $-\sum_i\bar\phi_i y_{i:N}$. This derivation establishes both the sign and the integer multiplying each threshold.

Only ranks with $d_j>0$ need a threshold variable. Let their actual indices be $k_1,\ldots,k_J$. The compressed LP must use $k_j\psi_j$, not simply $j\psi_j$. Equation (24) abbreviates the active steps using $j=1,\ldots,J$; preserving the original rank index is essential when the spectrum jumps at, say, the fifth rather than the first order statistic.

For each active rank introduce $z_{ij}\ge0$, $z_{ij}\ge\psi_j-y_i(w)$ and minimize

$$
\sum_{j=1}^{J}d_{k_j}\left(\sum_i z_{ij}-k_j\psi_j\right)
-\bar\phi_N\sum_i y_i(w),\qquad w\in\mathcal W.
$$

The coefficients of all slacks are nonnegative. This is a useful sign check: reversing the spectral difference can make the objective unbounded as a slack is increased. A spectrum with many distinct levels can require up to $N(N-1)$ slacks in this direct representation; the article's broad claims of virtually unrestricted size should not be read as a complexity bound.

## Implementation boundary

A reproducing researcher can independently check the empirical sorted formula and LP on a small fixed scenario matrix, including ties, noninteger tail counts, cash shifts, and a spectrum with jumps at nonconsecutive ranks. The two objective values should agree; the optimizer's threshold vector need not be unique. A held-out scenario set would be needed to evaluate the selected portfolio's risk beyond the optimized sample, but the review does not perform that experiment.

The source supplies no trading universe, sample dates, costs, rebalancing schedule, or market-data calibration. Its numerical figures are stylized illustrations and its computational results are reductions, not measured portfolio performance. The most useful operational conclusion is that one can retain a joint scenario engine while replacing the final quantile computation and portfolio objective with explicit coherent alternatives. That change repairs the aggregation structure; it does not validate the scenario distribution or eliminate estimation and execution risk.

# The 1-N investment strategy is optimal under high model ambiguity

Georg Ch. Pflug, Alois Pichler, and David Wozabal, *Journal of Banking & Finance* 36 (2012), 410–417. DOI: 10.1016/j.jbankfin.2011.07.018. Source: [MVOrobust_Pflug_2012.pdf](../../Finance/MVOrobust_Pflug_2012.pdf), eight PDF pages, including Appendix A. The source title writes the investment rule as 1/N; the slash is replaced in this filename and heading for filesystem compatibility.

## Why this matters

Equal weighting is often a difficult benchmark for optimized portfolios to beat. This paper provides a specific rational-choice explanation: when the distribution of future asset losses is uncertain within an increasingly large Wasserstein ball, minimizing worst-case risk becomes equivalent to minimizing nominal risk plus a norm penalty on portfolio weights. That penalty ultimately favors equal weights.

The contribution is stronger than a loose diversification intuition. Under specified dual-representation assumptions, the authors derive an exact robust counterpart, prove convergence to equal weighting as the ambiguity radius grows, and illustrate the result for CVaR and a mean-plus-standard-deviation objective. It is also narrower than the title can suggest. The conclusion depends on the geometry and symmetry of the ambiguity set, the risk functional, and the chosen asset coordinates. It is not a theorem that equal weighting is optimal for every uncertain investment problem or every finite radius.

The numerical study illustrates how optimized allocations change with radius on a fixed historical scenario distribution. It is not an out-of-sample horse race showing that a calibrated robust strategy earns superior risk-adjusted returns after costs.

## Portfolio problem and ambiguity geometry

Let $X^P\in\mathbb R^N$ be the vector of one-period asset losses with reference law $P$. Portfolio weights $w\in\mathbb R^N$ may be negative, but satisfy $\mathbf1^\top w=1$. Portfolio loss is $w^\top X^P$. The nominal problem is

$$
\inf_{\mathbf1^\top w=1}\mathcal R(w^\top X^P).
$$

The paper assumes this problem is well posed, in particular bounded below. This assumption is important when shorting and leverage are unrestricted. A risk functional that permits arbitrarily attractive long-short directions can otherwise invalidate existence or convergence arguments.

The reference distribution is not assumed to be the true law. For $1\leq p<\infty$, the Wasserstein distance is

$$
d_p(P,Q)=\left[\inf_{\pi\in\Pi(P,Q)}\int\|x-y\|_p^p\,d\pi(x,y)\right]^{1/p},
$$

where $\Pi(P,Q)$ contains joint distributions with marginals $P$ and $Q$. Both the transportation exponent and the ground norm use $p$. The radius-$\kappa$ ambiguity set is $B_\kappa(P)=\{Q:d_p(P,Q)\leq\kappa\}$. The robust portfolio solves

$$
\inf_{\mathbf1^\top w=1}\sup_{Q\in B_\kappa(P)}\mathcal R(w^\top X^Q).
$$

The radius has the units of the asset losses; it is not directly a confidence level or a volatility target. The ambiguity set is nonparametric and imposes no separate support, covariance, or economic-factor restrictions on alternative distributions. Moving probability outside the empirical support is allowed. Adding bounded returns, a factor structure, asset-specific transportation costs, or restrictions on admissible scenarios changes the robust problem.

Wasserstein geometry is useful because empirical distributions converge in this metric when the appropriate moments exist. Thus more data can reduce distributional uncertainty in a statistically meaningful topology. The paper discusses possible confidence-set interpretations but does not calibrate the numerical radius to a specified finite-sample coverage probability. It also explicitly cautions that the equal-weight conclusion is not established for a different ambiguity construction such as relative entropy.

## Risk functionals and dual assumptions

The principal examples are the Markowitz functional

$$
M_c(Y)=E[Y]+c\sqrt{\operatorname{Var}(Y)},\qquad c>0,
$$

and upper-tail loss CVaR,

$$
\operatorname{CVaR}_\alpha(Y)=\frac1{1-\alpha}\int_\alpha^1 F_Y^{-1}(u)\,du,
\qquad 0<\alpha<1.
$$

The first objective penalizes **standard deviation**, rather than the usual quadratic variance penalty. Calling it mean-variance optimization without this qualification would change both its homogeneity and its robust counterpart. Loss signs must also be consistent: with return mean $\mu_r$, its nominal term is $-\mu_r^\top w+c\sqrt{w^\top\Sigma_rw}$.

The theory works with convex, law-invariant risk functionals on $L^p$ that admit a dual representation

$$
\mathcal R(Y)=\max_Z\{E[YZ]-\mathcal A(Z)\},
\qquad \frac1p+\frac1q=1.
$$

Law invariance means dependence on the distribution of loss rather than its particular realization on the underlying probability space. Proposition 1 assumes that the relevant maximizing dual variables all have the same finite $L^q$ norm $C$. The endpoint case $p=1$, $q=\infty$ uses an additional special structure: maximizing dual variables take absolute values zero or $C$. These are substantive attainability conditions. Convexity alone is not enough to infer the exact equality below.

For CVaR the dual variables obey $EZ=1$ and $0\leq Z\leq1/(1-\alpha)$. On a sufficiently rich atomless representation, a maximizing tail variable can be chosen as $Z=1_A/(1-\alpha)$ with probability of $A$ equal to $1-\alpha$. This includes splitting an atom at the quantile if necessary. It yields $C=1/(1-\alpha)$ in the $p=1$ construction.

For nonconstant $Y$, the Markowitz objective has maximizing variable

$$
Z=1+c\frac{Y-EY}{\sqrt{\operatorname{Var}(Y)}},
\qquad \|Z\|_{L^2}=\sqrt{1+c^2}.
$$

Constant losses need a limiting or nonunique dual-maximizer treatment rather than division by zero. The final robust formula remains meaningful, but an implementation that explicitly constructs $Z$ must handle that case.

## From a stability bound to an exact regularizer

Lemma 1 couples two loss distributions with an optimal transport plan, applies the dual representation of risk, and uses Hölder's inequality twice. One application controls the scalar random loss difference by $\|Z\|_{L^q}$; the other controls the asset-space inner product by $\|w\|_q$. The result is

$$
|\mathcal R(w^\top X^{P_1})-\mathcal R(w^\top X^{P_2})|
\leq C\|w\|_q d_p(P_1,P_2),
$$

when the relevant dual norm bound is finite. This gives a worst-case upper bound. It does not yet show that nominal risk plus the bound is the actual robust objective.

Propositions 1 and 2 construct adverse transports that align the change in loss with the portfolio weights and a maximizing dual variable so that both Hölder inequalities are tight. For $1<p<\infty$, shifts are proportional to $\operatorname{sign}(w_n)|w_n|^{q/p}$ across assets and to $\operatorname{sign}(Z)|Z|^{q/p}$ across states, with scaling chosen to exhaust the transportation radius. For $p=1$, adverse shifts are concentrated on coordinates whose absolute weights attain $\|w\|_\infty$. The dual conditions make these shifts attain the stability bound.

Consequently, Equation 17 is the exact robust counterpart for this class:

$$
\sup_{Q\in B_\kappa(P)}\mathcal R(w^\top X^Q)
=\mathcal R(w^\top X^P)+C\kappa\|w\|_q.
$$

This is the implementable core of the paper. It converts a minimax problem over distributions into an ordinary convex portfolio objective with an explicit norm regularizer. The correspondence between norms is crucial: a Wasserstein-1 ball with $\ell_1$ ground cost produces an $\ell_\infty$ portfolio penalty, whereas the Wasserstein-2/$\ell_2$ construction produces an $\ell_2$ penalty. These are not interchangeable conventions.

The proof uses a common atomless probability space on which arbitrary Borel loss distributions can be realized. Appendix A establishes this using intervals for atoms and a measure-preserving representation for the non-atomic remainder. This technical construction permits the coupling and tail splitting used above. It is not an extra empirical assumption that market data themselves are continuously distributed.

## Why equal weights emerge

Let $w^u=(1/N,\ldots,1/N)$. Under the budget constraint, this vector minimizes $\|w\|_q$ for the dual norms relevant to finite $p$. For $1<q<\infty$ strict convexity makes it the unique norm minimizer; for $q=\infty$, the budget and the minimum possible maximum absolute weight also force equal weighting. A statement about arbitrary $q=1$ would require care: many long-only portfolios have unit $\ell_1$ norm. That endpoint is not the dual of finite $p$ in the paper's main convergence claim.

As $\kappa$ grows, the norm penalty eventually dominates the nominal-risk advantage of more concentrated portfolios. The proof compares nominal-risk differences using a Lipschitz bound and controls the ratio between distance from $w^u$ and excess norm. Under the stated well-posedness assumptions, Proposition 3 gives convergence of optimal portfolios to $w^u$.

There are useful distinctions between the two worked cases. For $p=1$, the maximum-weight norm has corners and equal weighting becomes exactly optimal above a finite sufficient threshold. For $p=2$, the norm is smooth around the equal-weight point within the budget hyperplane. The optimum generally approaches equal weighting continuously, without necessarily reaching it at any finite radius. Exact equality at a finite radius and asymptotic convergence are different conclusions.

For the $p=1$ case, the paper gives a sufficient threshold of the form

$$
\kappa^*=(N-1)E[\|X^P\|_1\,1_{\{Z\ne0\}}],
$$

with the dual-tail event and notation used in Proposition 3. It is a conservative analytic bound, not an estimated optimal radius. For $p=2$, a sufficient condition for $\|w^*-w^u\|_2\leq D$ is

$$
\kappa\geq\left(\sqrt{1+\frac1{ND^2}}+\frac1{\sqrt N D}\right)
\left(E[\|X^P\|_2^2\,1_{\{Z\ne0\}}]\right)^{1/2}.
$$

The qualitative mechanism is that imposing a common transportation geometry makes exposure concentration expensive under worst-case distributional changes. Asset rescaling or an asymmetric ground cost changes which exposures are expensive. Equal dollars across the selected instruments is therefore a conclusion of that modeling geometry; it is not invariant to replacing a fund by multiple near-duplicate share classes or changing the definition of an investment opportunity.

## Robust CVaR: a reproducible linear program

With empirical loss scenarios $x_s$, probabilities $p_s$, and $S$ scenarios, the exact robust objective is

$$
\operatorname{CVaR}_\alpha(w^\top X^P)+\frac{\kappa}{1-\alpha}\|w\|_\infty.
$$

One transparent LP implementation uses variables $w,a,z_s,m$:

$$
\min\ a+\frac1{1-\alpha}\sum_{s=1}^{S}p_sz_s+\frac{\kappa}{1-\alpha}m,
$$

$$
z_s\geq w^\top x_s-a,\quad z_s\geq0,\quad -m\leq w_n\leq m,\quad \mathbf1^\top w=1.
$$

Here $a$ is the CVaR threshold and $m$ bounds absolute positions. This form follows directly from Equation 17 and avoids confusing the CVaR threshold with the ambiguity penalty. An equivalent implementation shifts the penalty inside every scenario loss and redefines the threshold.

The printed LP on page 415 gives only a positive-side inequality for the auxiliary maximum. Since short weights are explicitly allowed, that does not generally enforce the maximum **absolute** weight. A faithful implementation of the preceding norm formula needs both signs as displayed here. Restricting to long-only portfolios would remove this issue but would change the feasible set of the paper's numerical experiment. The source's displayed LP should therefore be checked against the exact robust objective rather than copied mechanically.

For a worst-case CVaR transport, choose a tail event with probability $1-\alpha$. If $k$ coordinates attain the maximum absolute weight, move those coordinates in their adverse signed directions by magnitude $\kappa/[(1-\alpha)k]$ on that event. The expected $\ell_1$ movement is $\kappa$, and the resulting tail loss increase is $\kappa\|w\|_\infty/(1-\alpha)$. Finite empirical scenarios may require splitting probability at the cutoff to realize the correct tail mass.

## Robust mean plus standard deviation

For $p=2$, the robust Markowitz objective becomes

$$
E[w^\top X^P]+c\sqrt{\operatorname{Var}(w^\top X^P)}
+\kappa\sqrt{1+c^2}\|w\|_2.
$$

Given a loss mean vector $\mu$ and covariance $\Sigma$, solve

$$
\min_{\mathbf1^\top w=1}\mu^\top w+c\sqrt{w^\top\Sigma w}
+\kappa\sqrt{1+c^2}\|w\|_2.
$$

A second-order-cone formulation uses auxiliary variables $s,t$ with $\|\Sigma^{1/2}w\|_2\leq s$ and $\|w\|_2\leq t$, minimizing $\mu^\top w+cs+\kappa\sqrt{1+c^2}t$. This is a standard computational reformulation of the reported objective, not a new empirical specification. It keeps the robust problem in the same broad convex computational class as the nominal one.

This penalty is linear in the Euclidean norm. It is not equivalent to adding $\lambda I$ to a covariance matrix inside a quadratic objective, and it is not a squared ridge penalty. Substituting either changes the solution path and the finite-radius behavior.

## Numerical design and reported results

Section 4 uses seven instruments or indices: the Dow Jones Industrial Index, Dow Jones CBOT Treasury Index, SPDR Gold Shares, Dow Jones Composite All REIT Index, Euro Stoxx 50, Nikkei 225, and Shanghai Stock Exchange Composite. All are expressed in US dollars; foreign-currency index values are converted using the relevant exchange rates. The source states weekly historical returns from January 1, 2007 to October 31, 2010 and an empirical distribution of 151 equally weighted observations.

That observation count is materially smaller than the number of calendar weeks in the stated interval. The paper does not explain the filtering, common-date intersection, missing values, or other sampling choices producing 151 records. Reproducing only the stated dates with a default weekly download need not reproduce the reference distribution. It also does not specify whether quoted index histories include dividends, the weekday used, simple versus logarithmic return conventions, or the exact FX timestamp.

CVaR uses the scenarios directly; the Markowitz example uses their estimated mean and covariance. The figures display portfolio compositions as ambiguity radius varies, together with normalized Herfindahl–Hirschman concentration

$$
H(w)=\frac{\sum_nw_n^2-1/N}{1-1/N}.
$$

This equals zero at equal weighting and one at a single fully invested asset. With unrestricted shorting or leverage, it can exceed one; it is not universally confined to the unit interval. The figures show rapid concentration reduction, initially including short positions, as radius increases.

For CVaR, the smallest radius at which the numerical optimum becomes equal weight is reported as 0.026. The analytic sufficient bound is 0.0734, approximately 2.82 times larger. This illustrates conservatism of the bound for that particular empirical distribution and objective. It is not a universal ambiguity threshold. Figure 1 plots radius up to about 0.03, with allocation becoming equal near the reported threshold.

For the Markowitz example, Figure 2 plots radius up to 0.3 and shows rapid approach to equal weighting without apparent exact finite-radius equality. Figure 3 compares actual Euclidean distance with the theoretical bound; the observed distance is much smaller. The source does not tabulate exact weights or concentration at every radius. Values read approximately from curves should not be reported as exact solutions.

Important numerical parameters are not fully disclosed: the CVaR confidence level and Markowitz risk-aversion coefficient are not stated in the numerical-study text or figure captions, and a complete radius grid, solver tolerances, and covariance normalization are absent. They are required to replicate the plotted paths exactly. No rebalancing schedule, estimation/validation split, transaction costs, turnover comparison, confidence interval, or out-of-sample return series is supplied for this study.

## Interpretation and limits

The theorem establishes a structural connection between distributional robustness and norm regularization. It supplies a principled reason why increasing uncertainty can push a rational optimizer toward equal weighting under the chosen symmetric loss-space metric. The mechanism is exact for the worked objectives, not an ad hoc shrinkage rule.

Several extrapolations would be unwarranted. A weak nominal model does not logically imply that equal weighting will dominate every alternative in realized performance. Neither the theoretical radius limit nor the historical allocation figures calibrate how much ambiguity a particular investor should use. The results do not show that robustification removes tail risk, and the ambiguity ball can include economically implausible loss distributions if no support or factor restrictions are added.

For reimplementation, reproduce the exact nominal objective, the loss sign convention, and the Wasserstein/dual-norm pairing first. Check the unrestricted-short LP with both absolute-value constraints, verify the empirical scenario count and return conventions, and distinguish an illustrative radius sweep from a statistically calibrated decision rule. The paper's durable contribution is the exact robust counterpart and the convergence mechanism; its numerical figures illustrate those claims while leaving several calibration inputs unresolved.

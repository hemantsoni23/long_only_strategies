# Assessing Specification Errors in Stochastic Discount Factor Models

**Lars Peter Hansen and Ravi Jagannathan · 1997 · Journal of Finance 52(2), 557–590 · DOI: 10.1111/j.1540-6261.1997.tb04813.x.** Source: [StochasticDiscount_HansenJagannathan_1997.pdf](<../../Finance/StochasticDiscount_HansenJagannathan_1997.pdf>). Several page objects in the library copy are damaged or missing. The same published article was recovered from a [University of Houston hosted copy](https://www.bauer.uh.edu/rsusmel/phd/hansen-jaganathan_1997JF.pdf); all article pages and Appendices A–B were inspected. Page references below use the journal pagination.

## Why this matters

An asset-pricing model can be statistically rejected yet remain a useful approximation. Conversely, a model can obtain a relatively small rejection statistic by producing noisy pricing errors rather than economically small errors. Hansen and Jagannathan construct a common economic yardstick for comparing misspecified stochastic discount factors: the smallest root-mean-square alteration that makes a candidate discount factor price a specified payoff space correctly. Its dual interpretation is the largest pricing error over portfolios normalized by their payoff second moment.

The distinction from a specification test is substantive. A conventional GMM statistic weights errors by their own sampling covariance, which depends on the candidate model. Increasing discount-factor variability can reduce the statistic without improving pricing. The proposed distance instead uses a weighting matrix determined by asset payoffs. Models are compared against the same geometric standard. This does not replace statistical inference: an economically defined distance still has estimation uncertainty, and the paper develops inference for a strictly positive population distance.

A second contribution imposes nonnegativity on the corrected discount factor. This matters if a model will price derivatives outside the test-asset span. A signed discount factor can price every tested security correctly yet assign a negative price to a nonnegative contingent claim. The positivity-constrained distance accounts for that failure. The two criteria answer related but different questions, and their near equality in the empirical illustration is a finding about that dataset rather than a theorem that positivity never matters.

## Payoffs, information, and admissible discount factors

Work in $L^2$, the space of square-integrable random variables measurable at the payoff date, with inner product $\langle a,b\rangle=E[ab]$ and norm $\|a\|_2=\sqrt{E[a^2]}$. Let $P$ be a closed linear subspace containing the portfolio payoffs under examination. The pricing functional $\pi:P\to\mathbb R$ is continuous and linear, and at least one payoff has price one. These are Assumptions 1.1–1.2, pp. 560–562. They express the law of one price and the regularity needed for Hilbert-space projection.

For the finite-dimensional implementation, let $x\in\mathbb R^n$ be the next-period payoff vector and $q\in\mathbb R^n$ its current price vector. Prices may vary over time. Set

$$
G=E[xx'],\qquad \bar q=E[q],\qquad P=\{c'x:c\in\mathbb R^n\}.
$$

Assume $G$ is nonsingular and $q$ has finite first moments. Then $\pi(c'x)=c'\bar q$. Gross returns have prices one, so $q=\mathbf1$ in the empirical illustration. Do not substitute excess returns without changing their prices: an excess-return payoff has price zero. The distinction determines the moment restrictions and the level of the discount factor.

The admissible family is

$$
\mathcal M=\{m\in L^2:E[mx]=\bar q\}.
$$

More generally, $E[mp]=\pi(p)$ for every $p\in P$. The Riesz representation theorem gives a unique admissible discount factor lying within $P$, namely $m_P=x'G^{-1}\bar q$. All other admissible factors are $m_P+v$, where $v$ is orthogonal to $P$. Thus finitely many correctly priced assets ordinarily leave infinitely many admissible discount factors. Correct pricing of the test assets alone does not identify preferences or prices for every derivative.

Conditioning information can enter through managed payoffs. If a trading-date instrument is $z_t$ and the primitive gross return is $R_{t+1}$, the payoff $z_tR_{t+1}$ has price $z_t$, hence unconditional expected price $E[z_t]$. Alternatively, combine two unit-price returns with weights summing to one; the managed portfolio then retains unit price. The paper also permits random portfolio weights measurable with respect to trading-date information. A sufficient integrability condition is $E[q'E[xx'\mid\mathcal I]^{-1}q]<\infty$, with the conditional second-moment matrix nonsingular almost surely. Appendix A establishes boundedness of the induced expected-price functional by conditional factorization and Cauchy–Schwarz.

For derivative pricing, define $\mathcal M^{++}$ as the strictly positive members of $\mathcal M$ and assume this set is nonempty. Strict positivity makes every nonzero nonnegative $L^2$ claim have a strictly positive price. Optimization uses its closed extension

$$
\mathcal M^+=\{m\in\mathcal M:m\geq0\text{ almost surely}\}.
$$

The distinction is necessary: the nearest strictly positive factor need not exist, whereas the nearest nonnegative factor does. A boundary solution can assign zero price to a positive claim on a zero-discount-factor event. It is a limit of strictly arbitrage-free extensions, not necessarily a strictly arbitrage-free pricing rule on every possible claim.

## The two distances and their exact economic meaning

Let $y\in L^2$ be a proposed discount factor, perhaps $a+bR_M$ or $\beta(C_{t+1}/C_t)^{-\gamma}$. The paper defines

$$
\delta(y)=\min_{m\in\mathcal M}\|y-m\|_2,
\qquad
\delta^+(y)=\min_{m\in\mathcal M^+}\|y-m\|_2.
$$

Both minimizing random variables are unique because projection onto a closed convex set in a Hilbert space is unique. The second feasible set is smaller, so $\delta^+\geq\delta$. These are distances between random variables, not percentages of expected asset returns and not standard errors.

Write the pricing-error vector and its correcting portfolio as

$$
e=E[xy]-\bar q,\qquad \lambda=G^{-1}e,\qquad p_e=\lambda'x.
$$

The unrestricted nearest admissible factor is $m^*=y-p_e$. Indeed, $E[xm^*]=E[xy]-G\lambda=\bar q$. For every other admissible $m$, the component of $y-m$ projected onto $P$ is also $p_e$; its remaining orthogonal component can only increase the squared norm. Therefore

$$
\delta^2=e'G^{-1}e=E[p_e^2].
$$

Proposition 2.1 and equation (29), pp. 565–570, show that

$$
\delta=\max_{p\in P,\ E[p^2]=1}|E[yp]-\pi(p)|.
$$

When $\delta>0$, the maximizing payoff can be chosen as $p_e/\delta$, up to sign. This is an explicit diagnostic portfolio, not just a scalar rejection measure. Its weights show which linear combination of tested payoffs exposes the model most strongly.

Normalization is by second moment, not variance. A portfolio with a large deterministic payoff uses part of its norm budget even if its volatility is small. Nor are there budget, leverage, turnover, or short-sale constraints in the maximization. A distance of 0.30 means a pricing error of 0.30 for some unit-$L^2$-norm payoff; it does not mean a readily tradable 30% monthly alpha.

The metric is invariant to nonsingular changes of basis in the tested payoff space. Replacing $x$ by $Ax$ and $q$ by $Aq$ changes $e$ to $Ae$ and $G$ to $AGA'$, leaving $e'G^{-1}e$ unchanged. Adding genuinely new payoff directions can increase the distance. Thus fair comparisons must hold the test space fixed; enlarging the universe changes the economic question.

For the positive family, Proposition 2.2 gives a minimax interpretation:

$$
\delta^+=\min_{m\in\mathcal M^+}\ \max_{h\in L^2,\ E[h^2]=1}|E[mh]-E[yh]|.
$$

Here $h$ ranges beyond the observed asset span. The minimization selects the admissible nonnegative extension that makes the worst discrepancy with the proxy as small as possible. It is not a claim that unobserved derivative market prices are known; the possible arbitrage-consistent extensions are exactly what is being optimized over.

## Computing the positive distance through a finite dual

The primal positive problem imposes $E[mx]=\bar q$ and $m\geq0$. Use multipliers $2\lambda$ for the pricing constraints. Completing the square yields a pointwise minimization with solution

$$
m_\lambda=(y-\lambda'x)_+,\qquad a_+=\max(a,0).
$$

Substitution gives the concave, finite-dimensional dual, pp. 568–571:

$$
(\delta^+)^2=\max_{\lambda\in\mathbb R^n}
E\left[y^2-(y-\lambda'x)_+^2-2\lambda'q\right].
$$

The derivative is $2E[x(y-\lambda'x)_+-q]$. At an optimum, it enforces the pricing restrictions for the clipped factor. Away from observations exactly at the clipping threshold, the Hessian is

$$
-2E[xx'\mathbf1\{y-\lambda'x>0\}],
$$

which is negative semidefinite. These derivatives are direct algebraic implementation aids. They make clear why one must optimize after introducing clipping: clipping the unrestricted $m^*$ at zero generally destroys its correct pricing of the original assets.

The corrected random variable is unique even if the multiplier is not. The source gives nonsingularity of $E[xx'\mathbf1\{y-\lambda'x>0\}]$ as a sufficient condition for multiplier uniqueness. Appendix A uses the existence of a strictly positive admissible factor to place the expected price vector in the interior of the feasible pricing cone and justify the duality step. A sample with an apparent arbitrage or deficient payoff rank may fail these regularity conditions. An optimizer reporting a result is not itself evidence that the sample satisfies them.

Without positivity, replace the positive-part square by $(y-\lambda'x)^2$. The objective is quadratic and the optimizer is $G^{-1}e$. If the resulting corrected factor is already nonnegative almost surely, the two distances coincide. Otherwise the positive correction changes both the active states and the multiplier. This supplies a simple internal check on an implementation.

## Fitting linear factor proxies and interpreting expected-return errors

Suppose $y=f'\theta+\gamma_0$, where the factors are observed and the coefficients are to be fitted. Let $z=(1,f')'$ and $D=E[xz']$. Minimizing the unrestricted distance becomes weighted least squares in moment space:

$$
\widehat\theta_{\mathrm{pop}}
=\arg\min_a(Da-\bar q)'G^{-1}(Da-\bar q).
$$

Here $a$ includes the intercept; the hat is only a label for an optimized coefficient, not yet a sample estimate. If $D'G^{-1}D$ is nonsingular, the solution is $(D'G^{-1}D)^{-1}D'G^{-1}\bar q$. If it is singular, coefficients need not be identified even though fitted prices or the best distance may be. This expression follows directly from the paper's projection characterization in Section IV.B.

Equivalently, project the factor payoffs and the constant payoff onto $P$, then approximate the minimum-norm admissible factor using those projected factors. The first-order conditions mean that the chosen proxy prices its factor-mimicking payoffs correctly. Factors with no projection onto the tested asset space cannot improve this criterion merely by adding unrelated variation.

Expected-return error has a related but distinct normalization. For an admissible $m$ with positive mean,

$$
E[p]=\frac{\pi(p)-\operatorname{Cov}(m,p)}{E[m]}.
$$

To substitute $y$ into this relation while interpreting the discrepancy as a return error, the means of $m$ and $y$ must agree. The paper therefore studies a further constrained projection and obtains a sharp maximum expected-payoff error, normalized by payoff standard deviation, equal to the constrained distance divided by $E[y]$. The agreement of means is automatic at an interior optimum over a free additive constant: differentiation of $E[(y-m)^2]$ with respect to that constant gives $E[y-m]=0$. It is not automatic for every utility-based proxy.

This qualification prevents a common overinterpretation of HJ distance as a universal return-error bound. Pricing-error and expected-return-error comparisons align for suitably optimized linear models with the constant term included. They need not align for a fixed proxy that also misprices the unit payoff. The paper treats the latter discrepancy as part of model misspecification rather than silently forcing it away.

## Sample estimation and uncertainty

Use a common aligned sample of $(x_{t+1},q_t,y_{t+1})$, $t=1,\ldots,T$. Compute $\widehat G=T^{-1}\sum x_{t+1}x_{t+1}'$ and $\widehat e=T^{-1}\sum(x_{t+1}y_{t+1}-q_t)$. Then $d_T=\sqrt{\widehat e'\widehat G^{-1}\widehat e}$. For unknown proxy parameters, minimize this quantity over the stated parameter family. The positive estimator instead maximizes the sample dual for each parameter vector and, if appropriate, minimizes its optimized value over proxy parameters.

Section V assumes stationarity at least asymptotically, laws of large numbers for sample moments, and suitable central limit behavior. For a positive population distance, define the dual criterion contribution at the population optimizer as

$$
u_t=y_{t+1}^2-(y_{t+1}-\lambda'x_{t+1})^2-2\lambda'q_t.
$$

Its mean is $\delta^2$. If the centered sample average has long-run variance $\sigma_u^2$, the delta method gives

$$
\sqrt T(d_T-\delta)\Rightarrow
N\left(0,\frac{\sigma_u^2}{4\delta^2}\right).
$$

The same structure applies with the positive-part criterion for $\delta^+$. Estimation of the optimizing parameters does not add a first-order term under the required regularity, because the population criterion is stationary there. This envelope argument does not imply that arbitrary, nonoptimal nuisance estimates can be ignored.

For reproduction, evaluate the scalar criterion sequence at fitted parameters, center it by its sample mean, and estimate its long-run variance. The empirical tables use Newey–West with truncation parameter 15; the source reports similar results for 9 and 12. A standard-error reconstruction is $\widehat\sigma_u/(2d_T\sqrt T)$. The paper's printed central-limit summation in equation (43) omits an explicit sample-average normalization; its coherent reading is $T^{-1/2}\sum(u_t-\delta^2)$, consistent with equation (42).

This normal approximation is not valid at $\delta=0$. Correct specification is a boundary case with different asymptotics and may be tested using the original pricing moments and a suitable GMM test. A small nonzero estimate should not be converted mechanically into a symmetric normal confidence interval with division by an almost-zero distance. The study gives asymptotic theory, not a finite-sample guarantee or an out-of-sample pricing exercise.

## Empirical construction: six monthly real returns

Section VI.A and Appendix B use January 1959–December 1990, 384 monthly observations. The first three gross returns are equally weighted NYSE largest-size-decile stocks, equally weighted smallest-size-decile stocks, and long-term government bonds. Size is measured by common equity market capitalization in June. Appendix B explicitly says the resulting portfolios supply returns for the twelve months of the subsequent calendar year; a replication should preserve that convention or reconcile it against source code rather than assume the more familiar July–June formation cycle.

The other three assets are managed portfolios combining the large-stock return with a one-month Treasury bill:

$$
R^{(j)}_{t+1}=(1-z^{(j)}_t)R^{TB}_{t+1}+z^{(j)}_tR^{Large}_{t+1},
\qquad j=4,5,6.
$$

The instruments are previous-period annual yield differences: Aaa versus Baa corporate bonds; Baa bonds versus one-month Treasury bills; and one-year versus one-month Treasury bills. They are known at investment time. The text does not fully specify yield units or a within-month observation convention. This is consequential because multiplying a yield spread by 100 changes managed exposures sharply. Appendix B's moments should therefore be used as reconciliation targets, not treated as optional descriptive statistics.

Stock returns and market indices come from CRSP. Government-bond and bill returns come from Ibbotson's 1991 yearbook. Yields come from Federal Reserve Bulletins. Nominal returns are deflated by the CITIBASE nondurables-consumption price deflator. Per-capita nondurables consumption is also constructed from CITIBASE. The market proxies used in candidate discount factors are CRSP equally weighted and value-weighted NYSE/AMEX indices.

Table B.1 gives mean gross returns $(1.008,1.013,1.005,1.006,1.021,1.001)$ and standard deviations $(0.044,0.071,0.029,0.056,0.167,0.056)$. The fifth managed return is especially volatile, and several series have kurtosis around 9–14. These moments identify the scale of the exercise and warn against assuming nearly Gaussian pricing-error samples. The six assets are not independent: correlations among the three managed returns are 0.93, 0.80, and 0.81.

No trading-cost or portfolio-capacity model is imposed. The managed portfolios operationalize conditioning information for model evaluation; they are not presented as deployable allocations. The universe, sample, real-return convention, and managed payoff definitions stay fixed while the candidate stochastic discount factor changes.

## What the empirical comparisons establish

The best constant discount factor has estimated mean 0.998 and distance 0.329, standard error 0.054. Optimizing over constants is equivalent to finding the least-volatile admissible factor; the distance is its standard deviation. Positivity changes neither distance at three decimals. The minimum GMM statistic is 41.6 with five degrees of freedom, strongly rejecting risk-neutral pricing.

For power utility, $y_{t+1}=\beta(C_{t+1}/C_t)^{-\gamma}$, Table I considers $\beta=0.95$ and 1 with $\gamma=0,1,5,10,15$, then optimizes the criteria. The unrestricted minimum distance is 0.327, standard error 0.053, at $\beta=1.03$, $\gamma=33.3$. The positive minimum is also 0.327 at $\beta=1.03$, $\gamma=28.6$. Thus even freely fitted, economically unusual preference parameters barely improve on the constant-factor benchmark. In contrast, minimizing the GMM statistic chooses $\beta=1.608$, $\gamma=249.5$ and still yields 35.2. Extreme powers make a few recessionary observations dominate moments, undermining comfortable reliance on asymptotic approximations.

The external-habit-style example modifies marginal utility so that

$$
y_{t+1}=\beta(C_{t+1}/C_t)^{-\gamma}(C_t/C_{t-1})^{\gamma-1}.
$$

This is the paper's consumption externality specification, not a general internal-habit model. Table III minimizes distance at 0.328, with $(\beta,\gamma)=(0.998,7.3)$ for the unrestricted criterion and $(0.999,4.8)$ for the positive one. Again, the economic improvement is negligible. The GMM optimum uses $(21.1,237.6)$ and gives 27.5, illustrating the gap between lowering a rejection statistic and improving economic approximation.

A reciprocal-market-return proxy produces distance 0.311, standard error 0.055, for both criteria. Its GMM statistic is 128. Ranking it below the power-utility proxy solely because 128 exceeds 35.2 reverses the message of the economic distance. These are different questions, not inconsistent arithmetic.

Table IV is the sharpest demonstration:

| Variable factor, with intercept | Distance minimized | Standard error | GMM statistic at distance optimum | Distance at GMM optimum | Minimized GMM statistic |
|---|---:|---:|---:|---:|---:|
| Equally weighted market return | 0.286 | 0.054 | 30.1 | 0.286 | 29.3 |
| Value-weighted market return | 0.289 | 0.052 | 33.5 | 0.290 | 31.5 |
| Consumption growth | 0.325 | 0.052 | 38.9 | 1.57 | 12.0 |

The consumption model's GMM-optimal factor is more than thirty times as variable as its distance-optimal counterpart. Its small rejection statistic accompanies a dramatically worse pricing distance. The table reports 30.1 for the first market specification; nearby prose says 30.2. The table value is retained here, with the discrepancy made explicit.

The correction portfolios also locate the failure. In Table II, at $\beta=1$ and $\gamma=0$, the multipliers are approximately $(8.60,1.81,4.74,-13.46,3.76,-5.56)$. The last three, attached to managed payoffs, are large relative to their standard errors and remain similar as risk aversion changes. Across power-utility proxies, correction-payoff correlations exceed 0.999. Across the constant and linear-factor models, Table VI reports correlations from 0.87 to 0.99. This suggests common omitted pricing directions, although the authors caution that shared sampling artifacts could also produce this pattern.

## A concrete numerical reconstruction of the estimator

The following implementation details are consequences of the objectives above, rather than additional empirical procedures claimed by the authors. Store the aligned observations in a $T\times n$ payoff matrix $X$, with rows $x_t'$, and a $T$-vector $y$. The unrestricted sample correction solves

$$
(X'X/T)\lambda=X'y/T-\bar q.
$$

Solve this linear system rather than explicitly constructing a matrix inverse. The corrected sample discount-factor vector is $m=y-X\lambda$. Check $X'm/T=\bar q$ and verify that the squared distance computed as $\|X\lambda\|^2/T$ agrees with the moment quadratic form. These are independent numerical expressions for the same estimate and reveal orientation or normalization errors immediately.

The worst-error portfolio has weights $\lambda/d_T$ when $d_T>0$. Its sample payoff second moment should equal one, and its sample pricing error should equal $d_T$. The vector $\lambda$ alone is the unnormalized correction portfolio; confusing it with the normalized diagnostic portfolio would change every reported weight. Neither portfolio is required to have price one, because the maximization constrains payoff norm rather than initial expenditure. If budget-normalized holdings are desired for interpretation, that is an additional transformation and no longer preserves the exact unit-norm error statement without corresponding rescaling.

For the positive problem, define the active observation set $A(\lambda)=\{t:y_t-x_t'\lambda>0\}$. On a region with this set fixed, the dual is a concave quadratic with curvature $-2X_A'X_A/T$. A Newton step can solve the local linear system when it is nonsingular, but a line search is needed when the step crosses active-set boundaries. Alternatively a generic concave maximizer can use the explicit objective and gradient. A nearly singular active-set matrix signals weak multiplier identification; a stable corrected factor does not imply that every individual correcting weight is well determined.

At convergence, use $m_t=\max(y_t-x_t'\lambda,0)$ and check nonnegativity, pricing-moment residuals, and agreement between the primal mean square correction and the maximized dual objective. Simply replacing negative entries of the unconstrained solution with zero fails the moment check except in special cases. If moment residuals cannot be reduced while the objective continues to move, investigate sample feasibility and rank before interpreting the difference as economic misspecification.

Scaling also deserves an explicit diagnostic. Multiplying one payoff and its price by the same nonzero constant should leave the unrestricted distance unchanged. Corresponding multiplier coordinates rescale inversely. Replacing the second-moment matrix by a covariance matrix generally fails this invariance calculation for the intended pricing problem because it removes payoff means; it also changes the admissible moment geometry. Mean-centering returns without preserving their prices is therefore not an innocent numerical preprocessing step.

For parameterized proxies, separate the optimization over economic parameters from the correction step. At each trial parameter, construct the full $y$ vector, solve its pricing correction, and record distance, corrected mean, moments, and active fraction. Compare several starting values for a nonlinear utility family, especially when large curvature parameters create extreme observations. The paper's very large GMM-optimal consumption parameters make this an economically relevant numerical issue, not merely a software preference. No parameter bounds or optimizer tolerance beyond what the source reports should be represented as part of its historical method.

Finally, estimate uncertainty from the fitted scalar dual-criterion sequence using the same return sample. A standard deviation of individual pricing errors is not the required long-run variance, and the dispersion of the fitted discount factor is not the standard error of distance. Keeping these three objects separate makes the reported sampling uncertainty interpretable and preserves the paper's central distinction between noisy errors and large economic errors.

## Limits and practical use

A faithful reimplementation needs archived data definitions, exact instrument units, portfolio membership rules, missing-return handling, optimizer tolerances and starting values, and a precise GMM weighting update. Not all are supplied. The theory supplies the objective and restrictions; it does not justify inventing these inputs. Direct reproduction should first match Table B.1, then validate moment constraints, primal/dual objective agreement, and the reported distances before interpreting fitted preference parameters.

The metric intentionally depends on the tested payoff space. Six securities cannot establish that a discount factor prices every economically relevant risk. Adding derivatives or richer managed strategies can increase the required correction. The positive distance handles arbitrage-consistent extensions, but it cannot select actual unobserved option prices without further evidence. Similarly, high correlation among omitted factors is diagnostic, not structural identification.

The paper's lasting contribution is to separate economic misspecification from statistical rejection. Use a common payoff geometry to compare candidate models, inspect the portfolio exposing the largest error, and retain the distinction between unrestricted correction and positive derivative-pricing correction. Report sampling uncertainty and implementation limitations alongside the distance. In this application, neither nonlinear consumption preferences nor linear market exposure eliminates the missing pricing component, and changing the fitting criterion can materially change which model appears preferable.

# Optimal credit limit management under different information regimes

Markus Leippold, Paolo Vanini, and Silvan Ebnoether. *Journal of Banking & Finance* 30 (2006), 463–487. DOI: 10.1016/j.jbankfin.2005.04.018; available online 27 June 2005. Source: [original PDF](../../Finance/Credit%20Limit%20Management_Leippold2006.pdf). All 25 PDF pages were read, including Appendix A's proofs and coefficient formulas. References below use journal pagination, with PDF page 1 corresponding to p. 463.

## Why this matters

The paper treats a credit limit as an active short-horizon control. A company chooses borrowing to improve its surplus; the bank chooses how much credit to make available and pays for that commitment even when some is unused. The two choices interact. More borrowing changes both expected surplus growth and its volatility, while the bank's limit constrains the company's feasible investment. The authors formulate a continuous-time noncooperative game, then change the bank's information from full observation of surplus to a noisy signal and finally add incentives for disclosure effort.

The principal insight is that information quality can change the shape of the bank's desired limit schedule and the alignment of borrower and bank objectives. Under the proposed partial-information approximation, a borrower with relatively weak investment opportunities may benefit from a noisier surplus signal because the bank supplies more credit. A disclosure contract may reduce this distortion, but its design depends on the distribution assumed for borrower types or effort. The paper therefore connects limit policy, filtering, and screening rather than treating a credit score as an exogenous sufficient input to a static limit rule.

The model deliberately abstracts from an explicit default event. The per-unit credit price is said to include funding, operating, regulatory, and rating-related costs. There is no default intensity, recovery model, liquidity-triggered failure, endogenous bank capital constraint, or portfolio loss distribution. Accordingly, the results concern a stylized bilateral control problem, not a calibrated optimal exposure policy under default risk. The numerical material consists of illustrative parameter choices and simulated or schematic figures, without an empirical sample or a forecasting test.

For reimplementation, the article requires unusual care. Several printed formulas are internally inconsistent with their stated differential equations, and finite-horizon conditions are not fully resolved. The notes distinguish what the paper reports from mathematical checks derived here. None of those checks is presented as an official erratum or as a fully repaired version of the game.

## State dynamics and the two objectives

Let $S_t$ be company surplus, assets less liabilities. The company chooses $c_t\ge0$, borrowing expressed as a fraction of surplus, so the absolute draw is $c_tS_t$. The bank supplies a nonnegative limit $\ell_t$ with $c_tS_t\le\ell_t$. Without borrowing, surplus has drift $\mu_0$ and diffusion coefficient $\sigma_0$. With borrowing, the assumed process is

$$
dS_t=[\mu_0+(\mu_1-p)c_t]dt+[\sigma_0+\sigma_1c_t]dW_t.
$$

Here $\mu_1$ describes incremental investment return, $p>0$ is the loan price, and $\sigma_1$ describes incremental risk. This is an additive surplus SDE driven by the borrowing fraction, not the usual geometric diffusion in which drift and volatility are multiplied by $S_t$. It must be implemented as written if reproducing the paper. Economic units and the interpretation of a “fraction” should be normalized consistently before numerical work.

The initial company problem maximizes discounted expected surplus over the entire interval, subject to a bound on integrated conditional variance and the credit constraints. With discount rate $\delta>0$, the preference tradeoff can be written schematically as

$$
\max_c\int_t^T\left\{E_t[e^{-\delta(s-t)}S_s]
-\omega\operatorname{Var}_t[e^{-\delta(s-t)}S_s]\right\}ds.
$$

The variance penalty is nonseparable for ordinary dynamic programming. The authors embed it in a family of separable linear-quadratic problems, labelled $(C1)$,

$$
J^C(S,t;\omega,\lambda)=\max_{c\in\mathcal C}
E_t\!\int_t^T e^{-\delta(s-t)}[\lambda_sS_s-\omega S_s^2]ds.
$$

$\omega$ controls the mean–variance tradeoff and $\lambda$ is an embedding parameter or process. Proposition 1 invokes a relation between the solution of the original problem and a suitable member of this family. The printed statement uses $\lambda_t^*=1+2\omega c_t^*$ while its surrounding text refers to the associated surplus trajectory; the notation is not sufficient to independently reconstruct the embedding fixed point. Thus optimizing an arbitrary chosen quadratic utility is not automatically equivalent to solving the original variance-constrained problem.

The bank receives $pc_tS_t$ and pays $\kappa\ell_t$, where $\kappa$ is the cost of committing a unit of limit. Its printed objective $(B1)$ is

$$
J^B(S,t)=\max_{\ell\ge0}E_t\!\int_t^T
 e^{-\delta(T-s)}[pc_sS_s-\kappa\ell_s]ds.
$$

Notice that the bank's printed discount kernel differs from the company's $e^{-\delta(s-t)}$. Later HJB and value-function expressions use the former convention for both in places. A reproduction should explicitly select the printed-formulation variant or a conventional present-value formulation; silently replacing every discount factor would obscure a material source ambiguity.

Commitment cost on the limit is crucial. If cost were only on actual usage and $p>\kappa$, the paper argues that the bank would simply meet credit demand. With a positive cost on unused commitment, slack is costly: holding actual usage fixed, reducing an unused portion $\varepsilon$ saves $\kappa\varepsilon$ per unit time. This motivates a binding credit relation at the candidate equilibrium, $c_t^*S_t=\ell_t^*$. It does not imply that a borrower always wants to draw an arbitrarily high offered line; the binding statement belongs to the jointly optimized candidate.

The equilibrium concept is subgame-perfect Nash: neither player benefits from a unilateral feasible change given the other's policy. The derivation uses quadratic value-function ansätze, HJB first-order conditions, and a multiplier on the credit constraint. Verification requires admissibility, appropriate curvature, and horizon or transversality conditions in addition to solving those algebraic equations.

## Reported full-information limit schedule

Define $q=\mu_1-p$. Proposition 2 reports

$$
\ell^*(S)=\gamma_1S+\gamma_2S^2,\qquad
c^*(S)=\gamma_1+\gamma_2S,
$$

$$
\gamma_1=\frac{\sqrt\delta}{\sigma_1},\qquad
\gamma_2=\frac{\mu_0q-\delta\sigma_0\sigma_1}
{\sqrt\delta\,\sigma_1(q+\sqrt\delta\,\sigma_1)}.
$$

For the parameter region $q>0$ and $\sigma_1>0$, the denominator is positive. The numerator determines convexity. If $\mu_0q>\delta\sigma_0\sigma_1$, the line is convex and the borrowing fraction rises with surplus. At equality it is linear. If the inequality reverses, the line is concave, with a positive zero at $S_{\rm stop}=-\gamma_1/\gamma_2$. Beyond that zero the algebraic policy is negative and violates the nonnegative-limit constraint. The paper interprets the positive zero as ending the credit relation; a numerical implementation must define the relevant state domain or solve the constrained boundary problem.

The maximum of a concave limit curve occurs at $S_{\rm peak}=-\gamma_1/(2\gamma_2)$, halfway to its positive zero. These two thresholds answer different questions: the point after which the line starts to decrease and the point at which it disappears. They should not be conflated with the maxima of the bank's or firm's value functions, which the article calls satiation levels.

Proposition 3 gives

$$
J^B(S,t)=e^{-\delta(T-t)}(p-\kappa)
\left(b_0+b_1S+\frac12b_2S^2\right),
\qquad
J^C(S,t)=e^{-\delta(T-t)}
\left(k_0+k_1S+\frac12k_2S^2\right).
$$

For completeness, Appendix A reports, with $D=q+\sqrt\delta\sigma_1$,

$$
b_0=\frac{-q(\delta\sigma_0^2-\mu_0^2)(q+2\sqrt\delta\sigma_1)
-2\delta\mu_0\sigma_1^2(\mu_0+\sqrt\delta\sigma_0)}{2\delta^2D^3},
\quad
b_1=\frac{\sigma_1(\mu_0+\sqrt\delta\sigma_0)}{\sqrt\delta D^2},
\quad b_2=-\frac1{2D}.
$$

Its company coefficients, evaluated after substituting the reported policy, are

$$
k_2=\frac{2\omega}{\delta+\gamma_2(2q+\gamma_2\sigma_1^2)},
$$

$$
k_1=-\frac{\lambda+k_2[\mu_0+\gamma_2\sigma_0\sigma_1+
\gamma_1(q+\gamma_2\sigma_1^2)]}{\delta+\gamma_2q},
\qquad
k_0=-\frac{2k_1(\gamma_1q+\mu_0)+k_2(\sigma_0+\gamma_1\sigma_1)^2}{2\delta}.
$$

These transcriptions preserve the supplied formulas. They should be tested against the selected HJB and terminal conditions before they are used as verified value functions. For finite $T$ and no terminal payoff, an integral objective must have value zero at $t=T$. The printed expressions generally do not. Their time-independent coefficients also do not depend on remaining horizon. This suggests that an additional stationary or infinite-horizon interpretation, or missing boundary treatment, is needed; the paper does not give a complete resolution.

The nominal limit rule also omits both $\omega$ and $\kappa$, although they enter preferences or the value-function level. That is a feature of the reported algebra under the binding relation, not a general economic statement that risk aversion and commitment cost do not affect limits. The derivation presumes a useful positive lending margin; if $p\le\kappa$, or if unconstrained surplus becomes nonpositive, its interpretation must be revisited.

## Full-information figures and internal checks

Figures 1 and 2 use $\mu_0=2\%$, $\sigma_0=10\%$, $\sigma_1=30\%$, $\delta=5\%$, and $p=1\%$. The incremental return $\mu_1$ varies between zero and 12%; the highlighted cases are 5% and 10%. Figure 2 adds $\kappa=0.8\%$ and displays a ten-year simulated trajectory of surplus, borrowing fraction, absolute limit, and cumulative bank earnings.

At those parameters, the convexity boundary derived from the reported coefficients is $\mu_1=8.5\%$. For $\mu_1=5\%$, $\gamma_1\approx0.74536$ and $\gamma_2\approx-0.09745$; for $\mu_1=10\%$, $\gamma_2\approx0.02847$. These numbers are calculations from Proposition 2, not a numerical table in the article. They explain why the two chosen returns fall on opposite sides of the convexity boundary. The source does not specify a random seed, time step, initial state in the captions, path-generation algorithm, or confidence intervals. Its earnings graph is therefore illustrative, not exactly reproducible from a complete simulation recipe.

Substituting the policy into the state equation produces the affine diffusion

$$
dS=[\mu_0+q\gamma_1+q\gamma_2S]dt
+[\sigma_0+\sigma_1\gamma_1+\sigma_1\gamma_2S]dW.
$$

The source states on p. 469 that stationarity holds if and only if $q\gamma_2>0$. For a stationary distribution with a finite stable mean, the mean dynamics instead require a negative linear drift coefficient, $q\gamma_2<0$. Finite second-moment stability additionally involves $2q\gamma_2+(\sigma_1\gamma_2)^2<0$. These are direct moment-equation checks; they are not a claim to have established every possible stationary-distribution condition or an official correction. They show that the printed criterion cannot be used uncritically.

There is a related price-comparative-static inconsistency in Section 5.1. The paper states that $\gamma_2$ decreases with $p$, but then gives a small-versus-large-firm interpretation with the opposite implication for the sign condition. Under the positive parameter region used in the figures, increasing $p$ reduces $q$ and makes a positive numerator less likely. The formula is the reproducible object; the verbal inference should be checked against it for the intended pricing comparison.

## Partial observation and the filter approximation

The bank observes a signal $\zeta_t$,

$$
d\zeta_t=(A_0+A_1S_t)dt+B\,dZ_t,
$$

with $W$ and $Z$ assumed independent. It observes the absolute draw $c_tS_t$, but neither the true surplus nor the fraction separately. The bank forms an estimate $\widehat S_t$ and an inferred fraction $\widehat c_t$ satisfying $\widehat c_t\widehat S_t=c_tS_t$. Its decision problem replaces true surplus by the estimate.

The source calls $\widehat S_t$ a mean-square-optimal filter and gives Proposition 4:

$$
d\widehat S_t=\left[\mu_0+q\widehat c_t+\rho_t\frac{A_1^2}{B^2}(S_t-\widehat S_t)\right]dt
+\rho_t\frac{A_1}{B}dZ_t,
$$

$$
\dot\rho_t=(\sigma_0+\sigma_1\widehat c_t)^2-\frac{A_1^2}{B^2}\rho_t^2,
\qquad\rho_0=E[(S_0-\widehat S_0)^2].
$$

The same mean equation can be written operationally in innovations form,

$$
d\widehat S_t=(\mu_0+q\widehat c_t)dt+
\rho_t\frac{A_1}{B^2}
[d\zeta_t-(A_0+A_1\widehat S_t)dt].
$$

This expression uses the observed signal increment, whereas the first display expands that increment in terms of the unobserved state and observation noise. A coder should not feed true $S_t$ to the bank's estimator except when simulating an experiment in which it is used solely to generate observations.

There are two substantive qualifications. First, the information set should be generated by the observations and available controls. The text instead describes it as generated by $Z_t$; observation noise alone is not the signal information set. Equation (7) also prints an infimum of $E|\widehat S_t-Y|^2$ rather than $E|S_t-Y|^2$, making the right side trivially zero for $Y=\widehat S_t$. The intended conditional-mean definition is apparent, but these are genuine notation problems in the displayed source.

Second, Gaussian filtering with a closed deterministic Riccati equation is not generally exact when the hidden state has state-dependent volatility and the control itself is unobserved. The true borrowing fraction enters both drift and diffusion. The identity $\widehat c=cS/\widehat S$ is not generally the same as $E[c\mid\mathcal G_t]$. Thus a filter using $\widehat c$ as if it were the known control is a modeling closure requiring justification. The article recognizes a nonlinear filtering problem, but asserts Gaussian conditional distributions without establishing the needed restrictions. For empirical implementation it is safer to treat the proposed filter as an approximation and compare it with a nonlinear filtering benchmark.

The authors proceed with two small quantities: relative state-estimation error and $\widehat c\sigma_1$. They linearize the variance coefficient as $\rho_t\approx r_0(t)+r_1(t)\widehat c_t$ and ignore the state-estimation error in the HJB to leading order. Their key statement is that the complete-information coefficients can be reused after the substitutions

$$
\sigma_0\longmapsto \widetilde\sigma_0(t)=r_0(t)A_1/B,
\qquad
\sigma_1\longmapsto \widetilde\sigma_1(t)=r_1(t)A_1/B.
$$

This gives an approximate quadratic line in estimated surplus,

$$
\ell^{(1)*}_t=\widehat\gamma_1(t)\widehat S_t+
\widehat\gamma_2(t)\widehat S_t^2,
\qquad c^{(1)*}_t=\ell^{(1)*}_t/S_t.
$$

The operative coefficients can be defined unambiguously by substituting $\widetilde\sigma_0,\widetilde\sigma_1$ into Proposition 2. The direct displayed expression for $\widehat\gamma_2$ in Proposition 5 contains a denominator term with $\delta$ and $A_1^2/B$, which does not match that substitution. Its surrounding text and Appendix A both emphasize the substitution route. A replication should document which variant it uses rather than combine them.

Appendix A's printed solution for $\rho_t$ also fails a simple steady-state check against its stated Riccati ODE. Let $h=A_1/B>0$ and freeze $a=\sigma_0+\sigma_1\widehat c>0$. Then $\dot\rho=a^2-h^2\rho^2$ has equilibrium $a/h$, whereas the printed prefactor implies $a/h^2$. A solution derived directly from the stated ODE is

$$
\rho(t;a)=\frac{a}{h}\,
\frac{h\rho_0+a\tanh(aht)}{a+h\rho_0\tanh(aht)}.
$$

It satisfies both the initial condition and the differential equation. To derive a first-order approximation consistently from that ODE with control frozen during the expansion, one can integrate

$$
\dot r_0=\sigma_0^2-h^2r_0^2,\quad r_0(0)=\rho_0,
\qquad
\dot r_1=2\sigma_0\sigma_1-2h^2r_0r_1,\quad r_1(0)=0.
$$

These are analyst-derived diagnostic alternatives to the printed Appendix formula. If $\widehat c_t$ varies over time, simply inserting its current value into a frozen-control Riccati solution does not capture the history of the control. Direct numerical integration of the chosen filtering equations is then preferable. The note does not claim that repairing this ODE alone verifies the broader nonlinear filter or game equilibrium.

## Incentive distortion illustrated by partial information

Figure 4 returns to $\mu_1=5\%$ and the same baseline parameters. In the complete-information panel, the authors compare company risk aversions $\omega=1.2$ and $\omega=1.125$. Value-function maxima define separate company and bank satiation levels. Depending on the ordering, one participant's preferred surplus is reached before the other's. The partial-information panel uses $A_1/B=10$ and $\omega=1.125$.

In the illustrated configuration, partial information shifts the bank's satiation level to the right and makes its quadratic limit curve less concave, permitting the company to reach its preferred surplus before the bank reaches its own. The company is better off, while the bank supplies a larger potential exposure and pays more commitment cost. The proposed manipulation channel is a reduction in signal quality, either by increasing $B$ or reducing $A_1$.

This is a comparative-static mechanism under the stated approximations. The figure does not estimate manipulation in borrower disclosures, quantify average loss from opacity, or provide a universally optimal information policy. In particular, the approximation assumes small relative estimation error; drawing a conclusion about arbitrarily poor signals or negative signal coefficients would move beyond its local domain. The initial variance, observation sampling frequency, signal construction, and mapping from disclosure behavior to $A_1/B$ are not calibrated.

## Contracting with hidden effort or type

The last model adds effort $e$ on a compact interval $[\underline e,\overline e]$ and a payment $K(e)$ from the bank to the company. Effort is costly: the modified surplus drift uses $\mu_1-(p+e)$ in place of $q$. The contract adds $K(e)$ to company utility and subtracts it from bank earnings. The bank assumes a prior distribution $F(e)$ with positive density $f(e)$ and smooth quasi-linear preferences.

Two constraints are central. Incentive compatibility requires the company to prefer its assigned allocation to reporting a different effort or type; individual rationality requires utility at least as high as an outside option $\bar u$. Writing $y(e)=(c(e),K(e))$, the source's compatibility condition is

$$
u(y(e),S(e))\ge u(y(\widetilde e),S(e))
\quad\text{for every }e,\widetilde e\in[\underline e,\overline e].
$$

The article alternates between unobservable chosen effort and a privately known type distributed according to $F$. A full structural implementation must make that distinction explicit. A distribution over types and a moral-hazard effort choice are not interchangeable without additional assumptions. In addition, no function $A_1(e)$ or $B(e)$ is supplied to quantify how costly effort improves the signal. The drift cost is specified, but the technological benefit of effort to information remains incomplete.

The six-step solution route is: filter surplus; impose equality of actual and inferred draws and eliminate the separate limit control; define feasible compatible allocations; replace true surplus by its estimate for the bank's optimization; eliminate transfers with the envelope theorem; then characterize the credit policy by an optimality condition. The “$\widehat S$-optimal” policy explicitly treats the estimate as the true state. It is a restricted solution concept, not a proof of optimality over all policies under the full posterior distribution.

Proposition 6 uses a monotonicity or single-crossing condition,

$$
\frac{\partial\widehat c(e)}{\partial e}\,
\frac{\partial^2u}{\partial e\,\partial c}\ge0,
$$

as a sufficient implementability condition under the assumed smoothness and structure. Appendix A derives local first- and second-order conditions by differentiating the truthful-report condition. Applying a local condition as a global implementability guarantee requires the maintained single-crossing and shape restrictions; numerical implementations should still test deviations across the report grid.

Let $u_1$ and $v_1$ denote company and bank utility after removing the transfer. The envelope calculation, with the lowest type's participation rent normalized to zero, gives the present value of the transfer as

$$
\int_t^T e^{-\delta(T-s)}K(e)ds
=\int_{\underline e}^{e}\partial_{\widetilde e}u_1(c(\widetilde e),S(\widetilde e))\,d\widetilde e
-u_1(c(e),S(e)).
$$

For a nonzero outside option, the corresponding participation constant must be retained. This integrated expression is more directly implementable than the source's time-derivative representation of $K^*$. Substituting into bank utility and integrating by parts gives the virtual-surplus objective

$$
\max_{\widehat c}\ E\!\int_{\underline e}^{\overline e}
\left[v_1+u_1-\frac{1-F(e)}{f(e)}\partial_eu_1\right]f(e)de,
$$

subject to the state dynamics, feasibility, and compatibility requirements. The coefficient $(1-F)/f$ is the inverse hazard rate of the type distribution. It measures the information-rent adjustment, not a default intensity.

The final optimality condition is organized into four contributions: marginal joint surplus; the dynamic generator associated with the noisy state; the information-rent term; and a generator correction due to effort. The paper does not solve this system numerically or deliver a closed-form implementable contract for a calibrated borrower. Its uniform-versus-Student-$t$ comparison illustrates how the assumed prior can change the desired allocation of credit and the types the bank attracts. The discussion's log-concavity claims should be read as conditions supporting a monotone hazard argument, not as a universally valid equivalence between increasing hazard and log-concave density.

## What a credible reproduction would require

A first implementation should isolate the paper's analytic full-information rule and verify the algebra at the figure parameters. Record the admissible state interval, lending-margin assumption, and treatment of negative surplus or a negative algebraic limit. Plot both the limit and the borrowing fraction, since their curvature and economic interpretation differ. Simulate the affine state equation with a declared step, seed, and initial state, and report sensitivity to time-step refinement. The source's example is a single path, so it supplies no evidence about expected profit distributions or downside quantiles.

Next, specify a coherent finite-horizon or stationary objective and derive its boundary conditions. Substituting the reported value functions into that objective's HJB will determine whether the printed formulas apply. For a finite-horizon problem with no terminal payment, solve the resulting time-dependent coefficient or numerical HJB system with zero terminal value. This would be a model reconstruction beyond a literal transcription, and it should be labelled accordingly.

For partial information, simulate the hidden state and observation jointly while updating the bank only with observed increments and draw amounts. Compare the proposed Gaussian closure with a nonlinear filter, especially when state-dependent borrowing materially changes volatility. Estimate the initial uncertainty, signal-loading parameters, and noise variance from a specified observation series rather than selecting a signal-to-noise ratio solely to reproduce the diagram. Separately test the small-error and small-$\widehat c\sigma_1$ approximations.

For the contract stage, specify whether $e$ is a fixed private type, a chosen effort, or both; define its effect on information quality, its cost, the outside option, transfer timing, and the bank's prior. Discretize both the state and type domains if needed, impose all incentive constraints, and evaluate the chosen policy under the true simulated state rather than only under the estimate. Without these inputs the final mechanism is an economic characterization, not a complete numerical contract algorithm.

There is no source dataset, bank-account sample, estimation period, return window, transaction-cost schedule, realized profit table, statistical significance test, or out-of-sample exercise. The figures are comparative statics for a stylized model. The paper's substantive value is the warning that noisy information and incentives interact with exposure control. Its exact formulas are useful hypotheses and benchmarks, but the documented internal inconsistencies and missing implementation choices prevent treating the supplied expressions as a turnkey optimal credit-limit engine.

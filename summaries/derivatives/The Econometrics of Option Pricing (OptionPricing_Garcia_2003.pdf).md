# The Econometrics of Option Pricing

René Garcia, Eric Ghysels, and Éric Renault. First draft November 2001; supplied version August 1, 2003.

Source: [OptionPricing_Garcia_2003.pdf](../../Finance/OptionPricing_Garcia_2003.pdf). The file has 79 PDF pages, with manuscript page 1 on PDF page 2. Page references below use manuscript pagination. This note covers the complete survey, including the references. Several displayed formulas in the draft require corrections, distinguished below from the authors' substantive arguments.

## Why this matters and the survey's contribution

Option econometrics must connect three different objects: a physical process estimated from asset returns, a pricing process inferred from options, and an observation scheme in which volatility and other states are latent. Treating a calibrated volatility surface as if it were a directly observed physical process can produce incorrect inference even when fitted prices look excellent.

The survey's distinctive contribution is to organize continuous-time, discrete-time, parametric, and nonparametric methods around the stochastic discount factor and the statistical information available to investors and econometricians. It explains when a pricing formula can avoid explicit preference parameters, why that property does not require complete markets, and how latent-state inversion changes estimation. It then contrasts model-based dynamics with methods that estimate the option-pricing function or risk-neutral distribution directly.

This is not one new empirical specification with a common dataset and a single best-performing estimator. Numerical findings come from the surveyed studies and use different samples and assumptions. The reader can reconstruct the principal model and estimation architectures from this note, but exact reproductions of the individual cited studies require their data definitions, algorithms, and original parameter tables.

## Prices, projected discount factors, and risk-neutral valuation

For a payoff $h(S_T)$, let the stochastic discount factor be $m_{t,T}>0$. Its time-$t$ price is

$$
\pi_t(h)=E_t[m_{t,T}h(S_T)].
$$

The discount-bond price is $B(t,T)=E_t[m_{t,T}]$. Projection onto the payoff-relevant state gives $m^*_{t,T}(S_T)=E_t[m_{t,T}\mid S_T]$. This projected kernel prices every payoff measurable with respect to $S_T$, even if the full economy has other risks and incomplete markets. Its uniqueness on the priced payoff space is different from completeness of all contingent claims.

The normalized density change $m^*/B$ defines the risk-neutral terminal distribution. Thus

$$
\pi_t(h)=B(t,T)E_t^Q[h(S_T)].
$$

Risk-neutral valuation as a change of probability measure is general. A risk-neutral valuation relationship, or RNVR in the survey's narrower terminology, is stronger: a simple transformation of the physical distribution makes valuation independent of otherwise unknown preference parameters. These two uses of “risk neutral” must not be conflated.

In a two-state binomial model, the risk-neutral up probability is $q=(S_t/B-S_d)/(S_u-S_d)$, assuming no intervening dividends. This is a consequence of spanning the two-state payoff space with stock and bond. In a model with many or continuously many terminal states, a finite number of option quotes usually leaves the distribution underidentified. Choosing exactly enough states to match the number of traded securities is an additional modeling restriction, not proof that the actual market is complete.

## Conditional lognormality and the preference-free case

Suppose $(\log m,\log S_T)$ is conditionally jointly Gaussian. Exponential tilting by $m$ shifts the mean of $\log S_T$ by $\operatorname{Cov}_t(\log m,\log S_T)$ while leaving its conditional variance unchanged. Hence

$$
E_t[mh(S_T)]=E_t[m]E_t\left[h\left(S_Te^{\operatorname{Cov}_t(\log m,\log S_T)}\right)\right].
$$

The stock-pricing equation identifies the required scale factor from the observed stock and bond prices. The transformed terminal stock is

$$
S_T^*=S_T\frac{S_t}{B(t,T)E_t[S_T]},
$$

so that $B E_t[S_T^*]=S_t$. Options can then be priced without separately identifying a risk-aversion parameter. This is a statistical restriction on the joint distribution, not a general theorem that all incomplete-market option prices are preference free.

The implication is useful for modeling: one can obtain a Black–Scholes-like valuation relationship without deriving a continuously rebalanced hedge. But the distributional assumption is doing real economic work. If the conditional covariance or higher-order structure varies with unobserved states, the rescaling need not eliminate preference dependence.

## Mixtures: how smiles and risk premia enter together

Sections 2.4–2.7 introduce a mixing variable $U$ such that the joint distribution of log stock and log discount factor is Gaussian conditional on $U$. Crucially, this variable is not necessarily observed by the investor at time $t$. Mixing over a fictitious conditional economy is different from conditioning the actual investor's decisions on an observed volatility state.

A self-contained form of the mixture call price is obtained by defining

$$
B_U=E_t[m\mid U],\quad X_U=E_t[mS_T\mid U],\quad
v_U=\operatorname{Var}_t(\log S_T\mid U).
$$

Then

$$
C_t=E_t[X_U\Phi(d_{1,U})-KB_U\Phi(d_{2,U})],
$$

$$
d_{1,U}=\frac{\log(X_U/(KB_U))+v_U/2}{\sqrt{v_U}},
\qquad d_{2,U}=d_{1,U}-\sqrt{v_U}.
$$

The stock and bond restrictions imply $E_t[X_U]=S_t$ and $E_t[B_U]=B(t,T)$. Conditional prices look Black–Scholes, but their effective spot, discount factor, and variance can all vary across mixture states. Dependence among these components carries economically meaningful information about the discount factor.

A pure variance mixture with fixed effective spot and bond produces a symmetric implied-volatility smile in log-forward moneyness, with its minimum at the money under the conditions discussed in the survey. Allowing the effective stock component to co-vary with variance creates asymmetry and permits smirks or other shapes. The word “price” in the draft's symmetry discussion should not be read as saying calls at reciprocal strikes have identical monetary prices; the relevant symmetry is in implied volatility after the appropriate normalization.

The unconditional identity $E[X_U]=S_t$ does not permit replacing $X_U$ with its mean inside a nonlinear mixture price when $X_U$ and $v_U$ are dependent. Such dependence is precisely one route by which leverage and risk premia affect the smile. Jensen-type comparisons require the proper conditional mean restrictions, not merely an unconditional normalization.

Multiperiod versions multiply one-period discount factors. The state process must summarize both measurement relationships and transition dynamics, and the survey imposes conditional independence or no-feedback restrictions where needed. Summing conditional variances across periods is valid only under the corresponding conditional independence structure. The resulting generalized Black–Scholes expressions average over future state paths rather than assuming that a single current variance estimate stays fixed.

## Continuous-time leverage and an unspanned price of risk

The survey links the mixture perspective to continuous-time stochastic-volatility models. A convenient representation is

$$
\frac{dS_t}{S_t}=(r_t+\mathcal P_t^S)dt+\sigma_t\left(\rho\,dW_t^X+\sqrt{1-\rho^2}\,dW_t^\perp\right),
$$

with a state $X_t$ driven by $W^X$. Write

$$
d\log m_t=\left[-r_t-\tfrac12(a_t^2+b_t^2)\right]dt+a_t\,dW_t^X+b_t\,dW_t^\perp.
$$

Pricing the stock requires

$$
\mathcal P_t^S+\sigma_t\left(\rho a_t+\sqrt{1-\rho^2}b_t\right)=0.
$$

This is one restriction on two risk-price components. The part loading on the volatility state is not generally identified from stock and bond alone. It is the economic source of an extra volatility risk premium in an incomplete market.

Under the survey's exogeneity and martingale conditions, let $U$ denote the future state path and define the stochastic exponential

$$
\mathcal E_t^T(g)=\exp\left\{\int_t^Tg_u\,dW_u^X-\frac12\int_t^Tg_u^2\,du\right\}.
$$

Equations (2.27)–(2.29) then give the inputs for the preceding mixture formula:

$$
B_U=e^{-\int_t^Tr_u\,du}\mathcal E_t^T(a),\qquad
X_U=S_t\mathcal E_t^T(a+\rho\sigma),\qquad
v_U=(1-\rho^2)\int_t^T\sigma_u^2\,du.
$$

The outer expectation is under the historical law of the state paths. Thus a numerical implementation can simulate those paths under the physical specification, accumulate the integrated variance and stochastic-exponential factors, compute each conditional Gaussian call value, and average. The same draws must be used for the correlated effective spot and variance; independently resampling those components changes the model. The stochastic exponentials require the integrability conditions that make the stock and bond normalization valid. This explains how leverage and the volatility price of risk can alter both the mixture's location and its scale. It is not a formula for an arbitrary correlated stochastic-volatility process without those conditions.

In the no-leverage case, the smile's symmetry may survive even though physical and risk-neutral variance distributions differ. Therefore a symmetric smile does not imply zero volatility risk premium. To identify that premium one needs information about the historical process as well as option prices. This is an example of the survey's repeated distinction between a surface's shape and the joint economics of $P$ and $Q$.

## Parametric dynamics: which features each family contributes

Section 3 reviews diffusion and jump models. The standard square-root variance system has

$$
d\log S_t=\mu_tdt+\sqrt{V_t}\,dW_t^1,
$$

$$
dV_t=\kappa(\theta-V_t)dt+\sigma_v\sqrt{V_t}\left(\rho\,dW_t^1+\sqrt{1-\rho^2}\,dW_t^2\right),
$$

before adding jumps and making the drift convention explicit. The $\log S$ drift already includes the appropriate diffusion adjustment if derived from a level-price process. Nonnegative variance, boundary behavior, and admissible jump specifications must be checked separately; writing a square root is not an entire existence argument.

Return jumps with approximately Gaussian sizes address short-horizon tails. Independent variance jumps add abrupt volatility changes. Common return/variance jumps allow negative returns to coincide with upward variance shocks. In a common-jump specification surveyed here, variance jump size is exponential with mean $\mu_v$, while the return jump conditional on it is Gaussian with mean $\mu_y+\rho_J\xi_v$ and variance $\sigma_y^2$. Affine intensities may be constant or depend linearly on a state. The distinctions matter for what the underlying history can identify and what option prices add.

Some cited physical estimates put volatility persistence and leverage around familiar values, including a mean-reversion coefficient near 0.02 in the study's sampling units and return–variance correlation near −0.4. These should not be transplanted without their time units. The surveyed Eraker sample for 1980–1999 suggests roughly 1.5 jumps per year, a mean price jump near −2.6%, and jump standard deviation just above 4%; another study on 1953–1996 imposes zero jump mean and estimates a jump standard deviation below 2%. Different restrictions, samples, and estimators yield different answers.

The survey reports spot volatility values of 15.10%, 14.32%, 15.18%, and 15.51% for illustrative SV, return-jump SV, common-jump, and independent-jump specifications. It considers option maturities of two weeks, two months, six months, and one year. Jumps particularly steepen short-maturity smiles. However, setting jump risk premia to zero in those illustrations is an assumption; the shapes do not demonstrate that jump risks are unpriced.

Nonaffine models relax the linear-transform structure. A two-factor exponential volatility model can combine fast and slow factors, producing richer short- and long-run volatility behavior. Its empirical success in cited work comes at the cost of less convenient likelihoods and pricing transforms. A choice between affine and nonaffine models is therefore partly computational, but a model should be selected for restrictions the data can test rather than transform convenience alone.

The Lévy-driven OU family uses a positive subordinator to drive variance. In consistent notation,

$$
dv_t=-\delta v_tdt+dZ_{\delta t},\qquad
v_t=e^{-\delta t}v_0+\int_0^t e^{-\delta(t-s)}dZ_{\delta s}.
$$

Returns can contain both $\sqrt{v_t}dW_t$ and a correlated jump component $\rho dZ_{\delta t}$, with negative $\rho$ generating downward price jumps when variance jumps upward. Gamma or inverse-Gaussian stationary variance distributions are among the possibilities. The draft's equations around (3.9)–(3.10) have inconsistent variance notation and an incorrect-looking decay kernel; the expression above is the solution of the stated OU equation. A pricing measure still must be specified.

Long-memory constructions fractionally integrate a centered variance factor. For fractional order $0<d<1/2$, the covariance decays like a power, roughly $k^{2d-1}$, rather than exponentially. This changes how fast uncertainty in average future variance disappears with maturity. The paper's illustrative comparison is that increasing maturity by a factor of 100 reduces a relevant variance measure by about ten when $d=0.25$, versus about 100 in the short-memory benchmark. Exact constants depend on the stated process normalization. Positivity is an extra concern when fractionally integrating a centered factor.

A subtle distributional point is that short-horizon conditional Gaussianity does not imply unconditional Gaussian returns. With random current variance and no relevant dependence, the limiting unconditional kurtosis is $3[1+\operatorname{Var}(v)/(Ev)^2]$, above three. Long-horizon kurtosis can tend toward three slowly under long memory. The conditioning set and horizon must therefore accompany claims that an option smile should flatten.

## Latent-state inversion changes the likelihood

Section 4 is central for implementation. Suppose $K$ latent factors $X_t$ generate $n$ observed option prices or transformations of prices. If all observations are deterministic functions of only $K<n$ factors, their joint distribution is singular. To write an ordinary likelihood, the model must explain the extra dimensions, often with pricing or measurement errors.

One construction selects $K$ observations or combinations $Z_t=h(X_t;\theta)$ that are treated as exact, and writes the rest as $V_t=e(X_t;\theta)+u_t$. The inverse $X_t=h^{-1}(Z_t;\theta)$ depends on the trial parameters. Choosing the “error-free” quotes is a modeling decision. It does not establish that actual bid–ask midpoints are observed without noise, and the inversion may be ill conditioned.

A latent criterion can combine a transition density and cross-sectional residuals:

$$
L(\theta;X)=\sum_t\log p_{\theta_P}(X_t\mid X_{t-1})
-\frac12\sum_t[V_t-e(X_t;\theta)]'\Omega^{-1}[V_t-e(X_t;\theta)],
$$

with the determinant terms included where the covariance is estimated. Backfitting alternates between recovering $X_t$ under the current parameter vector and optimizing the criterion while holding that state path fixed. Fixed-point convergence requires identification and appropriate regularity; it is not guaranteed merely by repeating the two steps.

A direct likelihood for the observed data must also include the Jacobian of the parameter-dependent transformation from observed prices to latent variables. Dropping it changes the objective. Similarly, a Gaussian quasi-likelihood valid for a latent transition does not automatically remain valid after a nonlinear inversion. The transformed moment restrictions must be checked, and an extended Kalman approximation can introduce further error when the pricing function is nonlinear.

Inference must account for the fact that the recovered state changes when parameters change. Treating inferred states as fixed observations can give incorrect standard errors and misleading efficiency claims. The paper distinguishes the efficiency of an estimator with genuinely observed states from that of the feasible estimator obtained by inversion. They need not coincide.

## GMM, simulation, and the information in option panels

Implied-state GMM evaluates moment functions of the recovered states, schematically $\psi(h^{-1}(Z_t;\theta),\theta)$. Its derivative includes both the direct parameter effect and the derivative through the inversion. Optimal instruments depend on the conditional expected derivative and conditional variance of the moments. Ignoring the state channel can lose efficiency and distort reported uncertainty; in some constructions it does not destroy consistency, but that must be established from the moments rather than assumed.

Risk-premium parameters may be identified mainly through the option-price inversion, while physical transition parameters govern the latent process. A backfitting criterion that holds the states fixed can become uninformative about parameters that enter only through the inversion. Adding cross-sectional pricing residuals or using an appropriately formulated direct estimator helps address this identification issue. Merely combining “historical data plus options” is not an identification proof.

The survey also describes efficient method of moments and indirect inference. Fit an auxiliary model, such as a flexible density approximation, to actual data; simulate the structural model under trial parameters; and match auxiliary scores or estimates. A Black–Scholes implied-volatility series can serve as a useful proxy even when Black–Scholes is false, provided simulation reproduces the proxy transformation and corrects the induced bias. Treating the proxy as the true latent variance omits that correction.

Bayesian MCMC integrates over latent volatility and jumps jointly with parameters, subject to the prior and discretization choices. Reprojection techniques approximate filters for latent states after structural estimation. High-frequency realized variation can supply another measurement, followed by a second estimation stage. Each route trades analytical tractability for simulation, approximation, or filtering error.

The survey does not prescribe one common simulation length, burn-in, random-number seed, convergence tolerance, auxiliary-polynomial order, optimizer, or GMM bandwidth. These are essential reproducibility inputs for a new experiment and must be supplied from the particular method being reproduced. An asymptotic efficiency label cannot replace a check of finite-sample behavior, numerical stability, and dependence among option quotes on the same day.

## Nonparametric pricing functions and risk-neutral densities

Section 5 first considers estimating the option-pricing function directly. A semiparametric approach smooths implied volatility over forward price, strike, and maturity using product kernels and then inserts the fitted volatility into Black–Scholes. Bandwidth selection controls the bias–variance tradeoff. Pooling many dates assumes an adequately stable conditional relationship; fitting each day's surface separately makes a different bias–variance tradeoff.

Derivatives of the fitted function are economically important. If $C=C_{BS}(S,K,\tau,\widehat\sigma(S,K,\tau))$, the hedge delta is

$$
\frac{\partial C}{\partial S}=\Delta_{BS}+\operatorname{Vega}_{BS}\frac{\partial\widehat\sigma}{\partial S}.
$$

Ignoring the derivative of the estimated surface yields the Black–Scholes partial delta rather than the model's total delta. The risk-neutral CDF and density are

$$
F_Q(K)=1+\frac{1}{B}C_K(K),\qquad f_Q(K)=\frac{1}{B}C_{KK}(K).
$$

The discount factor matters: the second derivative itself is a state-price density, while division by $B$ yields a probability density. Equation (2.30) in the draft gives an incorrect second-line chain rule involving delta and omits the direct strike derivative. With an implied-volatility surface the consistent formula is $F_Q(K)=\Phi(-d_2)+(\operatorname{Vega}_{BS}/B)\widehat\sigma_K$ under the usual Black–Scholes conventions.

A smooth fit need not be arbitrage free. Calls must decrease with strike, have slope between $-B$ and zero, and be convex in strike. Correct boundary behavior is needed to normalize the recovered density. A shape-constrained method first fits prices subject to monotonicity and convexity and then smooths in a way that preserves those properties. Unconstrained local polynomials can produce negative densities even when their price errors are small.

The survey cites an S&P 500 application covering January 4–December 31, 1993 and simulated Black–Scholes checks with small estimation errors, as well as later shape-constrained examples. These are demonstrations from the underlying papers, not a fully specified benchmark here. It reports that daily implied-tree fits can outperform pooled kernel fits at short horizons of about five days, while the latter can perform better beyond roughly ten days. The ordering depends on the cited experiment, not a universal superiority result.

## Entropy calibration and implied trees

Canonical valuation starts with historical terminal scenarios $S_h=S_tR_h$ and empirical probabilities $p_h$, often equal weights over overlapping $T$-period gross returns. It then changes probabilities to satisfy traded-asset pricing restrictions while staying close to the physical empirical distribution.

For exponential tilting, the consistent optimization is

$$
\min_{q_h\geq0}\sum_hq_h\log(q_h/p_h)
\quad\text{subject to}\quad \sum_hq_h=1,\quad\sum_hq_hg(S_h)=\bar g.
$$

The solution has $q_h\propto p_h\exp(\gamma'g(S_h))$, with multipliers determined by the pricing constraints. The dual minimizes a log-sum-exp function minus the target moment term. Feasibility requires the target payoff vector to lie in the convex hull of the scenario payoffs. If a historical sample contains no sufficiently adverse scenario, reweighting cannot create that missing support.

The draft's equation (5.7) prints the prior weights outside the logarithm and minimizes the wrong signed/oriented expression. That expression does not produce the exponential-tilting solution in equation (5.9). The forward-KL formulation above is the consistent method. Also, the $r^T$ notation in that subsection denotes accumulation from a gross risk-free return; it should not be confused with a continuously compounded rate raised to a power.

Implied-tree methods instead start with a lattice or a prior terminal distribution and find probabilities matching observed stock, bond, and option prices, perhaps within bid–ask ranges. A squared-distance objective or smoothing penalty selects among the many feasible distributions. The choice of prior and distance matters, especially in tails where quotes are sparse. A probability-vector Euclidean distance differs from a Hansen–Jagannathan-type distance that weights by inverse physical probabilities, placing more emphasis on rare states. No choice eliminates the need to distinguish statistical beliefs from pricing probabilities.

## Neural networks and recovered preferences

Neural networks approximate prices as nonlinear functions of observables. Homogeneity of degree one can reduce the representation to $C/K=f(S/K,\tau)$ under the relevant return-distribution assumptions. This helps use price-level information efficiently, but does not automatically enforce all no-arbitrage restrictions. Hidden-unit count and regularization require validation; excellent in-sample price fits can coexist with poor deltas, negative densities, or worse hedge performance.

The survey discusses positive-curvature constructions using the softplus $\xi(z)=\log(1+e^z)$. Its derivative is the increasing logistic $1/(1+e^{-z})$, and its second derivative is positive. The draft uses inconsistent signs for a logistic defined as $1/(1+e^z)$, whose first derivative is negative. An implementation should choose one convention and differentiate it correctly. Appropriate weights and strike-loadings can produce monotone, convex call functions, but density normalization and limiting slopes still require boundary restrictions. Positivity of one basis function's curvature alone does not prove that an arbitrary fitted network is a normalized pricing density.

Finally, comparing risk-neutral and physical densities can recover a projected pricing kernel:

$$
m(s)=B\frac{f_Q(s)}{f_P(s)}.
$$

If terminal underlying value can legitimately be treated as the relevant wealth state, local relative risk aversion is

$$
\operatorname{RRA}(s)=-s\frac{d\log m(s)}{ds}
=s\left[\frac{f_P'(s)}{f_P(s)}-\frac{f_Q'(s)}{f_Q(s)}\right].
$$

The interpretation is conditional on the mapping from underlying returns to wealth or consumption and on the absence of omitted priced state variables. A projected kernel need not coincide with primitive marginal utility. State mixing, continuation values under recursive utility, conditioning differences, and unstable density derivatives can create apparently implausible risk-aversion shapes. The survey discusses estimated negative local risk aversion over parts of a return range; that does not by itself prove that actual investors prefer risk locally.

## What a complete empirical implementation must specify

The survey suggests a disciplined order of operations. First define the traded payoffs, observation times, exercise features, dividends, and discounting conventions. Then state the physical dynamics and exactly which restrictions distinguish the pricing measure. Specify what investors observe and what the econometrician observes. If latent states are inverted from options, declare the selected quotes, measurement-error model, Jacobian, and parameter dependence.

Next identify the estimation target: prices, implied volatilities, transition densities, auxiliary scores, or conditional moments. State the weights and loss used both in fitting and evaluation. Document every numerical approximation and validate derivatives or hedges separately from price levels. For density methods, verify positivity, normalization, boundary conditions, and robustness to the tail support or prior. For risk-premium inference, show which information comes from $P$, which from $Q$, and why the joint parameters are identified.

The manuscript is most valuable as a map of these dependencies. Its central lesson is that fitting options, estimating physical volatility, and learning investor preferences are connected but distinct statistical problems. A reproducible model must make those connections explicit and retain the restrictions and numerical uncertainty that give the resulting inference meaning.

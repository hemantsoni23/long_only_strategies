# An Explicit Bound on Individual Assets’ Deviations from APT Pricing in a Finite Economy

**Philip H. Dybvig (1983).** *Journal of Financial Economics* 12, 483–496. Source: [APT_Dybvig_1983.pdf](../../Finance/APT_Dybvig_1983.pdf). All fourteen pages, including the technical footnotes, aggregation lemma, and numerical illustrations, were inspected. References below use printed pages. This is an equilibrium theorem with illustrative calibrations, not a historical backtest or an estimated anomaly study.

## Why this matters and what is new

An asymptotic APT theorem can say that most assets approximately obey a factor-pricing equation while leaving a few individual assets substantially mispriced. It also may not tell a researcher whether a real, finite market is large enough for the approximation to be useful. Dybvig addresses both questions by deriving a separate, explicit pricing-error bound for each asset in a finite economy.

The bound combines four economically interpretable quantities: the asset's supply per investor, its idiosyncratic payoff variance, a bound on investor absolute risk aversion, and an implicit discount factor. The proof first handles one investor, then aggregates heterogeneous investors through optimal risk sharing. The effective risk-aversion bound is a harmonic mean. Larger aggregate populations reduce the representative investor's exposure to each security's residual risk.

This is not a proof that factor-model errors observed in data are always tiny. The theorem requires a particular payoff decomposition, independent residual risks, sufficiently bounded preferences, positive net supplies, and an efficient allocation for aggregation. The paper's cents-per-share and basis-point calculations are rough economic illustrations under those assumptions. Their value is that every ingredient of the approximation is visible, so the conditions can be challenged directly.

## Payoffs, units, and the single-investor problem

There are $I$ assets and $J$ factors. Asset $i$ pays, per share,

$$
X_i=c_i+\sum_{j=1}^J\beta_{ij}F_j+\varepsilon_i.
$$

The constants $c_i$ are expected payoffs because factors and residuals have zero means. Each $\varepsilon_i$ is independent of the entire factor vector and of the other residuals. The factors need not be mutually independent. The idiosyncratic variance must be finite for the bound to be finite.

Asset prices are $p_i$, portfolio quantities are $\alpha_i$, and terminal wealth is $W=\sum_i\alpha_iX_i$. An investor with initial wealth $W_0$ solves

$$
\max_{\alpha}\mathbb E[u(W)]
\quad\text{subject to}\quad
\sum_i\alpha_ip_i=W_0.
$$

The pricing derivation uses the unconstrained first-order conditions

$$
\mathbb E[X_i u'(W)]=\mu p_i,
$$

where $\mu$ is the marginal utility of initial wealth. There are no trading costs or binding portfolio constraints. In the single-agent equilibrium, the investor holds the positive net supply of every asset. Positive *net supply* is the restriction used in the theorem; it is not a claim that heterogeneous investors are individually forbidden to short.

Substitution of the payoff equation gives an exact decomposition:

$$
p_i=\rho c_i+\sum_{j=1}^J\beta_{ij}\lambda_j+\delta_i,
$$

where

$$
\rho=\frac{\mathbb E[u'(W)]}{\mu},\qquad
\lambda_j=\frac{\mathbb E[F_j u'(W)]}{\mu},\qquad
\delta_i=\frac{\mathbb E[\varepsilon_i u'(W)]}{\mu}.
$$

The APT approximation drops $\delta_i$. The factor coefficients $\lambda_j$ here are prices of exposure in a *payoff-price* equation, not immediately the positive expected-return premia of a conventional return regression. If a traded unit risk-free payoff is available, $\rho$ is its price. Otherwise it is an implicit discount factor obtained from the investor's marginal utility. No restriction in the theorem itself forces $\rho\le1$; that follows from nonnegative interest rates or a suitable storage opportunity.

The payoff residual is normalized to satisfy $\varepsilon_i\ge-1$ almost surely. Dybvig explains that a bounded-below residual can be brought into this form by redefining a share. A researcher must make that normalization before using the numerical bound: changing share units changes supply and variance together. With an unnormalized lower bound $-L_i$, the corresponding derivation places $\bar A\alpha_iL_i$ in the exponential. This generalized expression is a unit-preserving deduction from the proof, not a separately numbered theorem in the source.

## The finite-economy bound and its assumptions

Theorem 1, pp. 486–488, assumes an increasing, strictly concave, three-times continuously differentiable utility. Absolute risk aversion is

$$
A(w)=-\frac{u''(w)}{u'(w)}\le\bar A
$$

uniformly over the relevant wealth domain, and $u'''(w)\ge0$, so marginal utility is convex. Together with independent, mean-zero, bounded-below residuals and positive supplies, the theorem gives

$$
|\delta_i|\le
\rho\exp(\bar A\alpha_i)
\operatorname{Var}(\varepsilon_i)\bar A\alpha_i.
$$

The bound is individual and explicit: no limit in the number of assets is taken. It becomes small when the investor's quantity exposure to a security, measured against risk tolerance, is small and residual variance is controlled. The exponential is close to one only if $\bar A\alpha_i$ is small in the source's residual normalization; that approximation should not be assumed outside that regime.

Uniformly bounded absolute risk aversion is more restrictive than concavity. Constant-relative-risk-aversion utility has absolute risk aversion proportional to reciprocal wealth and is unbounded near zero. Quoting a plausible relative-risk-aversion coefficient at one wealth level does not establish the theorem's global bound. The numerical exercise later uses such a local economic judgment as a calibration, not as a proof of admissibility for every wealth state.

The convex-marginal-utility requirement is weaker than decreasing absolute risk aversion. The multi-agent theorem adopts decreasing absolute risk aversion because it also helps preserve the relevant property under aggregation. The theorem does not require normally distributed residuals; indeed an ordinary nondegenerate Gaussian residual has no finite lower bound and cannot satisfy the stated normalization literally.

## Proof: isolating the marginal utility of one residual

Remove asset $i$'s residual contribution from wealth:

$$
W=W_i^*+\alpha_i\varepsilon_i.
$$

Independence makes $W_i^*$ independent of $\varepsilon_i$. Conditional on $W_i^*$, a Taylor expansion of $u'$ around $W_i^*$ gives

$$
\left|\mathbb E[\varepsilon_i u'(W_i^*+\alpha_i\varepsilon_i)\mid W_i^*]\right|
\le\alpha_i\operatorname{Var}(\varepsilon_i)
\sup_{w\ge W_i^*-\alpha_i}|u''(w)|.
$$

The zero-order term vanishes because the residual has mean zero. The lower-bound assumption controls the entire interval through which the Taylor remainder can move; the formula is an exact Taylor-remainder bound, not an uncontrolled second-order approximation.

Bounded absolute risk aversion implies

$$
|u''(w)|\le\bar A u'(w)
$$

and, by integrating the logarithmic derivative of marginal utility,

$$
u'(W_i^*-\alpha_i)
\le u'(W_i^*)e^{\bar A\alpha_i}.
$$

Since $u'$ decreases with wealth, these relations bound the preceding supremum by $\bar A u'(W_i^*)e^{\bar A\alpha_i}$. Convexity of $u'$ and conditional Jensen give

$$
\mathbb E[u'(W_i^*+\alpha_i\varepsilon_i)]
\ge\mathbb E[u'(W_i^*)].
$$

Finally write $\delta_i=\rho\mathbb E[\varepsilon_i u'(W)]/\mathbb E[u'(W)]$. The remaining expectation of $u'(W_i^*)$ cancels between the upper bound on the numerator and the lower bound on the denominator. That cancellation produces the stated bound. It is the reason a variance term becomes sufficient here despite the familiar failure of variance alone to control arbitrary expected-utility losses.

Under the same independence and positive-supply assumptions, the residual pricing adjustment is nonpositive: $u'(W_i^*+\alpha_i\varepsilon_i)$ decreases with $\varepsilon_i$, so its conditional covariance with the mean-zero residual is nonpositive. This sign is a deduction from the setup. The paper emphasizes the absolute magnitude because its objective is proximity to a linear factor-price equation.

Footnote 7, pp. 488–489, removes the $u'''\ge0$ condition at the expense of a looser bound:

$$
|\delta_i|\le
2\rho e^{2\bar A\alpha_i}
\operatorname{Var}(\varepsilon_i)\bar A\alpha_i.
$$

The argument uses the mean-zero residual and lower bound $-1$ to obtain at least one-half probability below $1$, then bounds expected marginal utility below by $\tfrac12e^{-\bar A\alpha_i}\mathbb E[u'(W_i^*)]$. This alternative preserves the linear small-exposure order but worsens both the leading constant and exponent.

## Converting the result to expected returns

For positive asset price $p_i$, the gross return is $R_i=X_i/p_i$. Divide the exact price equation by $\rho p_i$ and rearrange:

$$
\mathbb E R_i=
\rho^{-1}-\sum_j\frac{\beta_{ij}}{p_i}\frac{\lambda_j}{\rho}
-\frac{\delta_i}{\rho p_i}.
$$

Thus the expected-return loading is $\beta_{ij}/p_i$, while the associated factor premium in this convention is $-\lambda_j/\rho$. The residual expected-return error is $-\delta_i/(\rho p_i)$, with magnitude bounded by Corollary 1:

$$
\left|\frac{\delta_i}{\rho p_i}\right|
\le e^{\bar A\alpha_i}
\operatorname{Var}(\varepsilon_i/p_i)\bar A\alpha_ip_i.
$$

The variance now has return units, and the linear exposure term is position *value*. The exponent still uses the payoff normalization and quantity exposure. Converting every $\alpha_i$ to a market value without changing the residual normalization would produce an incorrect formula.

This is a population expected-return statement. Its residual is not an estimated alpha with a standard error. The paper supplies neither a factor-estimation routine nor a statistical test for deviations from the bound. Such a test would need uncertainty about means, loadings, residual variances, supplies, and preference bounds.

## Heterogeneous investors and the harmonic mean

Section 3 begins by assuming an **unconstrained Pareto-optimal allocation**. This premise is essential even though it is not repeated as a separate lettered condition in Theorem 2. One interpretation is that the traded asset set already supports optimal risk sharing. Another is that additional zero-net-supply financial claims complete the market, while the fundamental positive-supply assets retain the assumed factor structure.

Let there be $K$ investors with utilities $u_k$ and positive social welfare weights $\omega_k$. Define a representative utility as the optimal value of

$$
v(w)=\max_{w_1,\ldots,w_K}
\sum_{k=1}^K\omega_k u_k(w_k)
\quad\text{subject to}\quad
\frac1K\sum_{k=1}^K w_k=w.
$$

The argument $w$ is **per-capita wealth**. Optimal allocations $h_k(w)$ equalize weighted marginal utilities up to a common multiplier. Log differentiation yields

$$
A_k(h_k(w))h_k'(w)=A_v(w).
$$

Differentiating the average-resource constraint then gives

$$
A_v(w)=\left[\frac1K\sum_{k=1}^K
\frac{1}{A_k(h_k(w))}\right]^{-1}.
$$

If $A_k\le\bar A_k$, the representative bound is

$$
\widehat A=\left[\frac1K\sum_{k=1}^K\bar A_k^{-1}\right]^{-1}.
$$

Low-risk-aversion investors receive greater weight through their risk tolerances. This is not an arithmetic average of risk aversion or a market-capitalization-weighted average.

A normalization detail is worth making explicit. With $v$ defined as the unscaled welfare sum above, its derivative is $K$ times a suitably normalized common marginal utility in equation (10). Multiplying the value function by $1/K$ fixes the source's envelope shorthand and leaves $-v''/v'$ unchanged. The harmonic-mean result depends on the per-capita resource constraint, not on that irrelevant scaling of utility.

If individual absolute risk aversion is nonincreasing, each $h_k$ is increasing and the harmonic-mean expression makes representative absolute risk aversion nonincreasing as well. That implies convex marginal utility and allows the single-agent bound to be applied to per-capita asset supplies.

For aggregate net supply $\alpha_i$, Theorem 2 and Corollary 2 give

$$
|\delta_i|\le
\rho e^{\widehat A\alpha_i/K}
\operatorname{Var}(\varepsilon_i)\widehat A\frac{\alpha_i}{K},
$$

and

$$
\left|\frac{\delta_i}{\rho p_i}\right|
\le e^{\widehat A\alpha_i/K}
\operatorname{Var}(\varepsilon_i/p_i)\widehat A\frac{\alpha_ip_i}{K}.
$$

One can instead formulate the representative investor using aggregate wealth, in which case absolute risk aversion becomes $\widehat A/K$ and supply remains $\alpha_i$. Mixing aggregate wealth with the per-capita risk-aversion coefficient would exaggerate the bound by a factor that also enters the exponent.

## Reproducing the numerical illustrations

Section 5 uses deliberately coarse inputs. The assumed upper absolute risk aversion is $5/100{,}000=0.00005$ per dollar, obtained from relative risk aversion 5 and wealth of \$100,000. For the price bound it uses residual payoff standard deviation \$20 per share, supply five shares per capita, and $\rho\le1$. Substitution gives

$$
e^{0.00005\times5}\times20^2\times0.00005\times5
=0.100025\ldots.
$$

The reported approximation is ten cents per share. This is an upper-bound illustration, not a measured mispricing. The author argues that the inputs combine adverse cases that are unlikely to occur jointly, but provides no cross-sectional calibration dataset or uncertainty interval.

The expected-return illustration instead uses annual residual return standard deviation 20% and per-capita market value \$200, retaining the small exponent above:

$$
e^{0.00025}\times0.20^2\times0.00005\times200
=0.00040010\ldots.
$$

That is approximately **0.04 percentage points, or four basis points annually**. It is not 4%, and it is not a four-basis-point upper bound on empirically estimated alphas after arbitrary factor selection.

The source motivates annualization by treating residual variance and expected excess returns as proportional to the observation interval. This is a diffusion or aggregation intuition, not a general theorem for serially dependent or heavy-tailed returns. The monthly payoff-volatility illustration and annual return-volatility illustration use different coarse inputs; they should not be combined into one internally calibrated security.

## Limits, replication inputs, and the sequence-economy connection

To implement the bound for an actual security, specify the time horizon, payoff currency, share normalization, positive price, aggregate share supply, and relevant investor population. Identify a factor decomposition with the required residual independence, estimate residual variance in matching units, and justify an absolute-risk-aversion bound over the wealth domain used in the proof. The efficient-risk-sharing premise must be justified separately. Merely fitting a linear regression does not verify independence or Pareto efficiency.

The paper gives no preferred factor count, observation frequency, lookback window, method for estimating risk aversion, investor-population definition, or inference correction for estimated inputs. These are missing implementation inputs rather than values to be silently filled in. The result can guide sensitivity analysis by varying supply, residual variance, and risk tolerance; it cannot choose those quantities for the researcher.

Section 4 illustrates how the finite bound yields a stronger asymptotic conclusion. Let both assets and investors grow with $n$, keep aggregate individual-asset supplies uniformly bounded, and keep discount factors and harmonic-mean risk-aversion bounds finite. To bound the maximum error over all assets, residual variances also need uniform control. The displayed inequality on p. 494 uses a uniform variance constant without spelling out that additional requirement in the surrounding prose. Under those conditions the maximal bound is of order $e^{C/n}/n$ and tends to zero. Without uniform variance control, the displayed step does not follow merely from each asset having finite variance.

The dependence on asset supply is substantive. If a particular asset's aggregate supply grows as fast as the investor population, its per-capita residual exposure need not shrink. Adding many tiny securities elsewhere then does not force its error to vanish. This is precisely the economic issue that a count of assets alone cannot settle.

The finite bound therefore contributes a disciplined bridge between preferences, residual risk, and pricing accuracy. Its strongest practical use is diagnostic: it identifies what must be small for a specific asset's idiosyncratic risk to have little pricing effect. The attractive numerical illustrations remain conditional on a demanding economic structure, and the paper explicitly leaves correlated residuals, asymmetric information, factor identification, and time-varying loadings for further work.

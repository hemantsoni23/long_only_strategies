# Stochastic optimal hedge ratio: theory and evidence

Abdulnasser Hatemi-J and Youssef El-Khatib, *Applied Economics Letters* 19(8), 699–703 (2012), published online September 9, 2011. DOI: 10.1080/13504851.2011.572841. Source: [hedging_Hatemi_2011.pdf](../../Finance/hedging_Hatemi_2011.pdf), six PDF pages including the publisher cover and mathematical/filter appendix.

## Why this matters

A hedge ratio estimated once can differ from the ratio appropriate as spot–futures relationships change. This paper contrasts a constant minimum-variance hedge with a stochastic coefficient process, gives a Brownian-motion illustration, and plots a Kalman-filter coefficient estimate for US equity and futures indices. Its central message is that equal expected ratios do not imply identical paths of hedge positions.

That message is valid but weaker than proof of improved hedging performance. The theoretical example assumes a time-varying ratio; it does not derive that process as the conditional variance-minimizing hedge for a joint spot/futures model. The empirical section shows different coefficient paths without reporting realized hedged variance, out-of-sample performance, transaction costs, uncertainty bands, or a formal constancy test. Several mathematical and Kalman-filter expressions also require correction for implementation.

The useful reconstruction is therefore a clean separation of the established constant-ratio optimum, an illustrative stochastic coefficient, and the actual state-space estimation needed to investigate dynamic hedging.

## Constant minimum-variance hedge

Suppose an investor will sell $N_A$ units of an asset and hedges with a short futures position on $N_F$ comparable units. Define the unit hedge ratio $h=N_F/N_A$. With spot and futures price changes $\Delta S$ and $\Delta F$, terminal proceeds can be written as

$$
Y=S_1N_A+(\Delta S-h\Delta F)N_A.
$$

Given known initial spot price and exposure size, minimize the variance of $\Delta S-h\Delta F$:

$$
V(h)=\sigma_S^2+h^2\sigma_F^2-2h\rho\sigma_S\sigma_F.
$$

For $\sigma_F^2>0$, differentiation yields

$$
h^*=\frac{\operatorname{Cov}(\Delta S,\Delta F)}{\operatorname{Var}(\Delta F)}
=\rho\frac{\sigma_S}{\sigma_F},
\qquad V''(h)=2\sigma_F^2>0.
$$

The printed first-order derivative omits a square on the futures standard deviation in one term; the resulting displayed ratio is the standard correct expression. An OLS regression $\Delta S_t=c+h\Delta F_t+e_t$ estimates that unconditional projection slope under the appropriate sampling assumptions.

This unit ratio is not necessarily a contract-count ratio. Actual futures positions also require the contract multiplier, index units, and exposure notional. The paper does not provide a complete mapping from its index-level coefficient to traded contract quantities.

A genuinely conditional minimum-variance hedge is

$$
h_t^*=\frac{\operatorname{Cov}_t(\Delta S_{t+1},\Delta F_{t+1})}
{\operatorname{Var}_t(\Delta F_{t+1})}.
$$

The ratio can vary if conditional moments vary. Merely writing down a stochastic $h_t$ does not show that it equals this expression. The spot/futures joint law is needed to establish that claim.

## Brownian coefficient illustration

The paper proposes $h_t=a+B_t$ on $[0,T]$, where $B$ is standard Brownian motion and $a$ equals the constant OLS-style optimum. Since $EB_t=0$, Proposition 1 gives $Eh_t=a$. Brownian dispersion is $\operatorname{Var}(h_t)=t$, so the process is not stationary or mean reverting. A coefficient process with a realistic time unit would normally specify a diffusion scale as well; the example implicitly sets it to one.

Proposition 2 considers the pathwise discrepancy

$$
e=\int_0^T|h_t-a|dt=\int_0^T|B_t|dt.
$$

For $T>0$, this is positive almost surely. A continuous Brownian path would have zero area only if it were identically zero, an event of probability zero. Thus equal means do not imply the same realized ratio path.

An independent calculation gives a useful scale for the illustration:

$$
Ee=\int_0^TE|B_t|dt
=\int_0^T\sqrt{2t/\pi}\,dt
=\frac23\sqrt{\frac2\pi}T^{3/2}.
$$

This expectation is not tabulated in the paper. It quantifies deviation of positions, not monetary hedge loss, return variance, tracking error, or utility. No futures-price process appears in $e$, so it cannot by itself rank hedging strategies.

Indeed, adding independent zero-mean noise to a truly optimal constant hedge can make hedging worse. If $h=a+B$ is independent of the one-period price changes and $a$ already minimizes their variance, the random hedge introduces an additional variance term involving $E[B^2]E[(\Delta F)^2]$. This counterpoint is a mathematical qualification, not an empirical result from the source. Dynamic hedging helps only when the estimated variation captures relevant changes in the conditional optimum well enough to outweigh estimation and trading costs.

## The finite-zero-crossing proposition is not a Brownian proof

Proposition 3 assumes Brownian motion has only finitely many zeros on the interval, alternates sign between successive zeros, and ends with an even number of crossings. It then integrates by parts to express the absolute area as a finite alternating sum of stochastic integrals.

Standard Brownian motion started at zero does not have a finite list of zero crossings near its starting point. Its zero set has infinitely many points almost surely, and it is not correct to assume a finite positive first interval beginning at zero without changing the process or working with a discrete sampled approximation. Therefore the proposition's assumptions do not describe a typical Brownian path, and its finite-sum calculation does not establish the stated identity as a general result for that model.

A correct continuous-time route uses Tanaka's formula. With symmetric Brownian local time $L_t^0$ under the convention

$$
|B_t|=\int_0^t\operatorname{sgn}(B_s)dB_s+L_t^0,
$$

integration over time gives

$$
\int_0^T|B_t|dt
=\int_0^T(T-s)\operatorname{sgn}(B_s)dB_s
+\int_0^T(T-s)dL_s^0.
$$

The local-time contribution is the feature absent from a naive finite-crossing argument. This corrected identity is supplied here to delimit the source's proof, not attributed to the authors. Numerical integration of a discretely sampled absolute path remains straightforward, but it should not be mistaken for the proposed finite-crossing theorem.

Figure 1 depicts one C-language simulation over approximately ten thousand displayed steps, with a constant reference near one and a stochastic path ranging from slightly negative to around 1.8. The figure demonstrates possible path variation and sign changes. The paper supplies no seed, Brownian step size, total modeled horizon, diffusion rescaling, number of independent simulations, or Monte Carlo confidence interval. It is an illustration rather than a reproducible sampling-distribution study.

## Empirical application

The application uses weekly data over 1999–2009 for an MSCI US equity price index and a US futures-market share-price index, sourced from Reuters, misspelled in the text. The exact futures index/contract, vendor identifiers, observation weekday, sample endpoints, number of observations, and continuous-contract roll method are not specified.

The authors report unit roots in both price indices and cointegration between them. Test statistics, lag choices, deterministic terms, significance levels, and residual diagnostics are not shown and are said to be available on request. They discuss levels regressions as a way to preserve long-run information, while the earlier OHR derivation and Equation 6 concern price changes. A cointegrating levels slope is not automatically the minimum-variance hedge for weekly price changes. The actual empirical regression transformation should therefore be verified before claiming replication of the figure.

The constant OLS line in Figure 2 is approximately 0.960. The dynamic estimate begins around 0.966–0.969, crosses the constant line around 2000–2001, and gradually declines toward approximately 0.946 by 2007–2008. These are approximate readings of the plot, not tabulated parameter estimates. No fitted series is supplied, so reporting more decimal precision would be unwarranted.

The empirical dynamic path's average is not asserted to equal the constant estimate. Thus the application is not a controlled test of the theoretical equal-mean comparison. A visibly changing filtered coefficient alone also does not demonstrate statistically significant parameter variation; its estimated state-noise variance, uncertainty, and a constant-parameter comparison would be needed.

## State-space model and corrected Kalman recursion

The intended linear Gaussian model in the appendix is

$$
y_t=x_t^\top\beta_t+\epsilon_t,
\qquad \beta_t=A\beta_{t-1}+v_t,
\qquad \epsilon_t\sim N(0,\sigma),\quad v_t\sim N(0,Q),
$$

with independent disturbances over time and across equations. The printed state equation is missing an addition sign before $v_t$. The measurement variance is denoted $\sigma$ in the source, rather than $\sigma^2$; preserving that distinction avoids squaring it twice.

For a random-walk ratio the relevant transition would have $A=I$, possibly with a state vector containing an intercept and slope, but the application does not fully state which coefficients vary or its estimated transition. The theoretical Brownian example corresponds to a particular random-walk discretization, not every unrestricted state transition.

The dimensionally correct filter is

$$
\beta_t^-=A\beta_{t-1}^+,\qquad P_t^-=AP_{t-1}^+A^\top+Q,
$$

$$
e_t=y_t-x_t^\top\beta_t^-,\qquad f_t=x_t^\top P_t^-x_t+\sigma,
\qquad K_t=P_t^-x_t/f_t,
$$

$$
\beta_t^+=\beta_t^-+K_te_t,
\qquad P_t^+=P_t^--P_t^-x_tx_t^\top P_t^-/f_t.
$$

The printed mean update instead contains a scalar quadratic form where the vector gain should appear, and its indexing does not consistently use the predicted mean. Copying it literally fails for a multi-parameter coefficient vector. The corrected equations above reconstruct the intended standard filter.

Gaussian innovation likelihood can estimate the declared unknown parameters through $-\tfrac12\sum_t[\log(2\pi)+\log f_t+e_t^2/f_t]$. Initialization, diffuse-state treatment, parameter constraints, estimated $A,Q,\sigma$, optimizer, and whether Figure 2 shows filtering or full-sample smoothing are not given. These omissions prevent exact numerical reproduction and obscure what coefficient would have been available for a contemporaneous hedge.

## Evidence and practical interpretation

The paper establishes that a stochastic ratio with the same mean as a constant ratio can differ along almost every path. It illustrates a varying coefficient on historical US index data. It does not show that the stochastic specification minimizes realized or prospective hedging variance, that the particular state dynamics are preferred by a formal test, or that extra rebalancing earns a net benefit.

A proper replication should reproduce the static price-change hedge first, identify the precise index data and empirical transformation, implement the corrected state-space equations, and distinguish predicted, filtered, and smoothed coefficients. For an operational hedge, use the coefficient available before the next return interval, translate it into actual contracts, and evaluate held-out hedged variance and turnover with costs. Those are necessary extensions to test the investment implication, not reported achievements of this source.

The main limitations are the unproved optimality of the assumed Brownian ratio, the invalid finite-zero-crossing premise, the levels-versus-changes ambiguity, and incomplete empirical/filter settings. The practical takeaway is to investigate conditional hedge variation carefully; it is not that any time-varying coefficient or any visible departure from a constant estimate improves risk management.

# Market timing, investment, and risk management

Patrick Bolton, Hui Chen, and Neng Wang. *Journal of Financial Economics* 109 (2013), 40–62. DOI: 10.1016/j.jfineco.2013.02.006. [Source PDF](../../Finance/MarkettiminginvestmentriskmanagementBoltonChenWang_2013.pdf). All 23 PDF pages were read, including Appendices A–D and references. Page references below use printed journal pages; PDF page 1 is p. 40. The equations, calibration tables, policy figures, hedging diagram, and appendix comparisons were checked against rendered pages.

## Why this matters

A firm can issue equity while it still has cash because cheap financing may disappear. Its cash reserve consequently reflects both protection against future distress and an option to exploit current financing conditions. Bolton, Chen, and Wang put these motives into one dynamic optimization problem. The resulting investment policy need not increase with cash, and the optimal derivative position can change abruptly from hedging to speculation. Neither result requires irrational managers or equity mispricing.

The quantitative implication is equally useful: a small investment decline when financing conditions deteriorate does not establish that financing frictions are unimportant. Firms expecting deterioration have already accumulated cash, reduced investment, and sometimes raised equity. Event-time investment changes miss these earlier costs. The paper provides a disciplined counterexample to interpreting investment–cash sensitivities or crisis-date investment changes as direct measures of financial constraints.

The contribution is a regime-switching extension of the authors’ earlier unified investment, financing, and cash-management framework. The new ingredient is changing access to external finance, particularly state-dependent fixed issuance costs. The results are model implications under a plausible calibration, not estimates identifying a causal effect of a real financing shock. The paper has no trading backtest, portfolio-performance claim, or transaction-cost-adjusted investment strategy.

## State variables, financing technology, and objective

Capital $K_t$ and cash $W_t$ evolve continuously between financing and payout interventions. The observable state $s_t\in\{G,B\}$ is a continuous-time Markov chain. State $G$ has relatively favorable financing; $B$ has unfavorable financing. Its physical transition intensity out of state $s$ is $\zeta_s$. Capital obeys

$$
dK_t=(I_t-\delta K_t)\,dt,
$$

where $I_t$ is gross investment and $\delta$ depreciation. Operating revenue is $K_t\,dA_t$, with $dA_t=\mu_s\,dt+\sigma_s\,dZ_t^A$. Investment can be negative, representing asset sales. Installation costs are homogeneous:

$$
\Gamma(I,K,s)=K g_s(i),\qquad g_s(i)=\frac{\theta_s}{2}(i-\nu_s)^2,\qquad i=I/K.
$$

The parameter $\nu_s$ is the investment rate at which adjustment costs vanish. Cash earns $r_s-\lambda$, where $\lambda>0$ is a carrying cost. Let $H$ be cumulative cash raised from investors and $U$ cumulative payouts. Raising cash requires a fixed cost $\phi_sK$ at each issue and proportional cost $\gamma_s$ per unit raised. These shareholder costs are collected in a separate cumulative process $X$. The cash equation is

$$
dW_t=K_t\,dA_t-[I_t+\Gamma(I_t,K_t,s_t)]\,dt+(r_{s_t}-\lambda)W_t\,dt+dH_t-dU_t.
$$

Thus $dH$ is the cash actually delivered to the firm; shareholders pay $dH+dX$. Confusing net proceeds with gross issuance would change the boundary conditions. There is no debt choice or freely available line of credit. The firm can liquidate at time $\tau$ for $l_sK+W$. It chooses investment, financing, payouts, and liquidation to maximize discounted shareholder value under the risk-neutral measure:

$$
P(K,W,s)=\sup E^{\mathbb Q}\left[\int_0^\tau e^{-\int_0^t r_{s_u}\,du}(dU_t-dH_t-dX_t)+e^{-\int_0^\tau r_{s_u}\,du}(l_{s_\tau}K_\tau+W_\tau)\right].
$$

Productivity shocks have correlation $\rho_s$ with the aggregate Brownian factor. If its price of risk is $\eta_s$, risk-neutral productivity is $\widehat\mu_s=\mu_s-\rho_s\sigma_s\eta_s$. Financing jumps also command a risk premium:

$$
\widehat\zeta_s=e^{\kappa_s}\zeta_s.
$$

The baseline sets $\kappa_G=\log3=-\kappa_B$: adverse financing changes arrive more often and favorable changes less often under valuation probabilities. Physical intensities govern simulated occurrence frequencies and stationary distributions; risk-neutral intensities enter the valuation equations. Switching them is a substantive implementation error.

## Reduced dynamic program and free boundaries

Homogeneity gives $P(K,W,s)=Kp_s(w)$ with $w=W/K$. The enterprise-value ratio is $q_s(w)=p_s(w)-w$, and the net marginal value of cash is $q_s'(w)=p_s'(w)-1$. In the continuation region, the coupled HJB equations are

$$
r_sp_s=\max_i\left\{[(r_s-\lambda)w+\widehat\mu_s-i-g_s(i)]p_s'+\frac{\sigma_s^2}{2}p_s''+(i-\delta)(p_s-wp_s')+\widehat\zeta_s[p_{s^-}-p_s]\right\}.
$$

The state argument $w$ is unchanged by the financing-state jump itself. The other state may immediately trigger an issuance or payout, so $p_{s^-}(w)$ must include its action-region extension. Solving two ODEs only on their separate continuation intervals without those extensions misses part of the coupling.

The investment first-order condition is

$$
i_s(w)=\nu_s+\frac{1}{\theta_s}\left[\frac{p_s(w)}{p_s'(w)}-w-1\right].
$$

The economically relevant marginal value of capital is scaled by the marginal value of cash. Average enterprise $q$ alone therefore does not determine investment as in a frictionless model. At the payout boundary $\overline w_s$, smooth pasting and super-contact give

$$
p_s'(\overline w_s)=1,\qquad p_s''(\overline w_s)=0,
$$

with $p_s(w)=p_s(\overline w_s)+w-\overline w_s$ above it. At the financing boundary $\underline w_s$, an issue raises cash to target $m_s$:

$$
p_s(\underline w_s)=p_s(m_s)-\phi_s-(1+\gamma_s)(m_s-\underline w_s),\qquad p_s'(m_s)=1+\gamma_s.
$$

For an interior issuance boundary $\underline w_s>0$, also impose $p_s'(\underline w_s)=1+\gamma_s$. If the interior solution is not admissible, set the boundary to zero and do not impose that extra free-boundary condition. Compare the issuance continuation value there with liquidation value $l_s$. The calibrated solution issues rather than liquidates when cash reaches zero; this is a result of its parameters, not a universal boundary assumption.

Differentiating the investment rule yields the central local result:

$$
i_s'(w)=-\frac{p_s(w)p_s''(w)}{\theta_s[p_s'(w)]^2}.
$$

Where value is concave, investment rises with cash. Where value is convex, investment falls with cash. Equal marginal values at the pre-issue boundary and post-issue target, combined with a fixed issuance cost, permit a locally convex segment. A numerical method that enforces concavity everywhere would eliminate the paper’s main mechanism. Combining the investment rule and issuance value matching also gives

$$
i_s(m_s)-i_s(\underline w_s)=\frac{\phi_s}{\theta_s(1+\gamma_s)}.
$$

For baseline $G$ parameters this is $0.0026205$, or about 0.262 percentage points of annual investment divided by capital. Raising substantial cash consequently changes investment only slightly at that instant.

## Calibration, data construction, and numerical reconstruction

Table 1 sets annual $r=0.05$, $\delta=0.15$, $\mu=0.227$, $\sigma=0.12$, $\theta=1.8$, $\nu=0.15$, $\lambda=0.015$, $\gamma=0.06$, $\rho=0.4$, and $\eta=0.4$ in both states. Consequently $\widehat\mu=0.2078$. State-specific inputs are

| Parameter | $G$ | $B$ |
|---|---:|---:|
| Physical transition intensity $\zeta_s$ | 0.10 | 0.50 |
| Risk-neutral intensity $\widehat\zeta_s$ | 0.30 | 0.166667 |
| Liquidation value per capital $l_s$ | 1.0 | 0.3 |
| Fixed issuance cost per capital $\phi_s$ | 0.005 | 0.50 |

An intensity of 0.10 means an expected holding time of ten years, not exactly a 10% probability of leaving within one year. The latter is $1-e^{-0.1}=9.516%$. The paper sometimes uses the probability shorthand. The crisis-state fixed cost of 50% is an educated assumption designed to make finance very expensive; it is not a crisis issuance-cost estimate.

Appendix B uses annual Compustat data for 1981–2010. Firms must be incorporated in the United States and have positive total assets and net property, plant, and equipment. Utilities, SIC 4900–4999, and financial firms, SIC 6000–6999, are excluded. Firm-years are removed when assets or sales grow by more than 100%, or investment exceeds 50% of previous-year capital. Capital is PPENT, investment is CAPX, and cash is CHE minus BAST, average short-term borrowing. The ratios are $(CHE_t-BAST_t)/PPENT_t$ and $CAPX_t/PPENT_{t-1}$. The authors first compute firm-level moments and then take the median across firms. They choose $\mu$ and $\theta$ to match cash/capital 0.29 and investment/capital 0.17. Replacing these targets with pooled firm-year medians changes the calibration.

A reconstruction can discretize $w$, evaluate action operators, and solve the coupled nonlinear HJB system by policy iteration with boundary searches. Given $p,p'$, update $i$ using the explicit first-order condition. Update issuance targets by maximizing $p_s(m)-(1+\gamma_s)m$ and compare issuance, payout, continuation, and liquidation values. Refine the grid around financing thresholds and changes in curvature. Verify residuals, value matching, derivative conditions, and the absence of an unexploited intervention elsewhere. These are implementation suggestions derived from the stated control problem; the paper does not provide code, grid spacing, tolerances, or convergence diagnostics.

For stationary results, use the optimal policy and physical state transitions. Between actions the cash ratio obeys

$$
dw_t=\left[(r_s-\lambda+\delta-i_s(w_t))w_t+\mu_s-i_s(w_t)-g_s(i_s(w_t))\right]dt+\sigma_s\,dZ_t^A.
$$

Payout reflects cash at the upper boundary; an issuance resets it to $m_s$. State jumps can immediately activate a different boundary. One may simulate this process or solve its forward equation with reset flows. The source does not specify a simulation seed, horizon, discretization, or stationary-density solver, so its reported quantiles are numerical targets rather than exactly reproducible software output from the PDF alone. The independent checks in this note are algebraic and scalar numerical checks, not a new solution of the full free-boundary problem.

## Baseline policy and stationary outcomes

In $G$, the issuance boundary is approximately 0.027, issue size is 0.128 per unit capital, and the payout boundary is about 0.370–0.371. Thus the target cash ratio is about 0.155. Different passages round the financing boundary as 0.0268 or 0.027; a passage prints 0.0277. In $B$, issuance occurs only at zero, the target is about 0.219, and the payout boundary is 0.408. Favorable financing therefore induces issuance before cash exhaustion, while expensive financing induces waiting until cash runs out.

Figures 1–2 show a convex portion of $p_G$ below roughly $w=0.061$. Investment decreases with cash there. In $B$, value is concave and the low-cash marginal value becomes very large: near zero, the total marginal value of cash is about 24, and investment approaches approximately $-0.40$ per year. This is asset liquidation within the operating firm, not necessarily liquidation of the entire firm.

The stationary distribution explains why those dramatic conditional policies are not typical experiences. Table 2 reports:

| Conditional statistic | $G$ | $B$ |
|---|---:|---:|
| Mean cash/capital | 0.283 | 0.312 |
| First percentile cash/capital | 0.088 | 0.114 |
| Median cash/capital | 0.300 | 0.325 |
| Mean investment/capital | 0.170 | 0.161 |
| First percentile investment/capital | 0.112 | 0.003 |
| Median investment/capital | 0.176 | 0.173 |
| Mean net marginal value of cash | 0.015 | 0.031 |
| 99th percentile net marginal value of cash | 0.111 | 0.351 |

Cash management keeps most firms away from the region where financing constraints are extreme. The mean total marginal value of cash is only 1.015 or 1.031. The authors’ nearby statement that values 1.35 and 1.11 differ by 22 cents is a small arithmetic inconsistency; the rounded values differ by 24 cents.

A change from $B$ to $G$ can produce both an issuance wave and a repurchase wave. Firms with cash between the two payout boundaries distribute the excess because their precautionary need falls. Firms with very low cash raise equity because favorable financing becomes available. These are different firms at different cash positions responding to the same aggregate improvement. The explanation does not require repurchases to reveal undervaluation.

The duration and cost experiments identify the mechanism. With $\zeta_G=0.01$, cheap finance lasts 100 years on average and the firm issues only at zero; value is concave and investment monotone. With $\zeta_G=0.50$, the issuance boundary rises to about 0.071 and the payout boundary to 0.400. Increasing the fixed issuance cost has the opposite effect on issuance timing: Table 3 moves the boundary from 0.092 at zero fixed cost to 0.027 at $\phi_G=0.005$, 0.013 at 0.01, and zero by 0.02. At zero fixed cost, financing is continuous and global concavity returns despite changing financing opportunities.

Table 3’s average issuance costs are $\gamma+\phi_G/(m_G-\underline w_G)$. At the baseline, $0.06+0.005/0.128=0.0990625$, agreeing with 0.099. For fixed costs 0.01, 0.02, 0.05, and 0.10, issue sizes are 0.153, 0.176, 0.189, and 0.199 and reported average costs are 0.126, 0.174, 0.324, and 0.563. Positive fixed costs can retain local convexity even after the optimal issuance boundary reaches zero; interior issuance is sufficient for the boundary argument, not a necessary condition for every convex segment.

## Anticipation, investment shocks, and expected returns

Table 4 compares a low anticipated financing-shock intensity, $\zeta_G=0.01$, with the baseline 0.10, holding $\zeta_B=0.50$. Average pre-shock cash rises from 0.224 to 0.283. Evaluating the investment-policy jump at those respective means gives declines of 4.03 versus 0.96 percentage points of investment/capital. Averaging the jump across each conditional stationary cash distribution gives 6.59 versus 1.78 percentage points. These are changes in the investment/capital rate, not proportional declines relative to its approximately 17% level.

The distribution matters: at the first cash percentile, the investment-rate decline is 43.17 points in the low-hazard case and 18.11 in the baseline; at the fifth percentile it is 23.66 versus 6.49; at the median it is 3.66 versus 0.76. Higher anticipated risk changes both the policy at a given cash level and the distribution of cash before the event. Comparing only the realized average decline omits this selection into better-prepared balance sheets.

The productivity-shock comparison holds financing costs equal across states at $\phi=0.005$, $\gamma=0.06$, and changes productivity from 0.227 to 0.1925. The latter is selected to match the 6.59-point mean investment drop under low anticipation. Under the higher hazard, the mean productivity-driven drop is 3.15 points, compared with 1.78 for financing. Productivity effects are also nearly uniform across cash percentiles, whereas financing effects are concentrated among cash-poor firms. This is a model-based diagnostic, not a universal empirical exclusion restriction: richer models can make productivity and financing exposures correlated.

The conditional equity risk premium separates Brownian operating risk and financing-regime risk:

$$
\mu_s^R(w)=\eta_s\rho_s\sigma_s\frac{p_s'(w)}{p_s(w)}-(e^{\kappa_s}-1)\zeta_s\frac{p_{s^-}(w)-p_s(w)}{p_s(w)}.
$$

Both components can be positive: deteriorating finance lowers value while the stochastic discount factor rises; improving finance raises value while it falls. The physical expectation calculation should evaluate the valuation-optimal investment policy, rather than independently optimizing a physical-measure HJB. The state-dependent value difference supplies exposure to an aggregate risk not captured by the diffusion factor alone.

Near zero cash in $B$, conditional annual productivity premia can exceed 80% and financing premia 30%. They should not be reported as typical required returns, because the stationary distribution places little mass there. High cash reduces both exposure amplification and the share of value represented by risky productive assets. In the frictionless constant-parameter benchmark, the diffusion premium is $\eta\rho\sigma/q^{FB}$.

Appendix C rewrites the premium in a two-factor beta form. For a technology factor with volatility $\sigma_s^T$, $\beta_s^T=(\rho_s\sigma_s/\sigma_s^T)p_s'/p_s$. For a financing factor whose jump is $e^{\kappa_s^F}-1$, $\beta_s^F=(p_{s^-}-p_s)/[p_s(e^{\kappa_s^F}-1)]$. There is a sign conflict in the printed appendix: with its positive-jump stochastic-discount-factor convention and compensated-jump return equation, the factor premium must be $-\zeta_s(e^{\kappa_s^F}-1)(e^{\kappa_s}-1)$ to reproduce the main equation above. Printed equation (46) uses a plus sign. This correction follows from the negative return–discount-factor covariance condition and equation (27); it is a derived diagnosis, not an official erratum.

## Hedging, speculation, and source-equation cautions

Section 7 introduces futures with risk-neutral dynamics $dF/F=\sigma_m\,dZ^M$. The contract is constructed to hedge the market’s financing-jump exposure already, so the firm uses it against continuous productivity risk rather than directly trading its own regime jump. Let futures notional be $\psi W$. A margin account holding fraction $a$ of cash permits $|\psi|\leq\pi_sa$. The numerical example sets the margin-account carry penalty to zero, allowing $a=1$ without tracking a separate cash-allocation state.

The cash variance per unit capital becomes

$$
V_s(\psi,w)=\sigma_s^2+\psi^2w^2\sigma_m^2+2\rho_s\sigma_s\sigma_m\psi w.
$$

Its contribution to the HJB is $V_sp_s''/2$. For $p_s''<0$ and positive correlation, the optimizer minimizes this variance:

$$
\psi_s^*(w)=\max\left\{-\frac{\rho_s\sigma_s}{w\sigma_m},-\pi_s\right\}.
$$

When $p_s''>0$, maximizing variance over the symmetric bounded interval gives $\psi_s^*=+\pi_s$. At zero curvature the local variance term is indifferent. The policy discontinuity arises from a change in the sign of the value of cash volatility. It is not a reversal in the sign of the physical correlation. The margin bound is essential: without it, locally convex value would encourage unbounded variance within this simplified control formulation.

The illustration uses $\sigma_m=0.20$, $\rho=0.4$, $\pi_G=5$, and $\pi_B=2$. The unconstrained hedge is $-0.24/w$; it reaches the $B$ margin constraint for $w\leq0.12$. In $G$, the speculative region extends from the issuance boundary 0.0219 to the curvature threshold 0.0593, where the position is $+5$. At larger cash values the firm hedges. With hedging available, payout boundaries fall from about 0.371 to 0.355 in $G$ and from 0.408 to 0.385 in $B$, because hedging substitutes for precautionary cash.

Two source issues matter for implementation. Equation (32), printed on p. 57, gives the $G$ transition term proportional to $P_G-P_B$. A Markov generator instead requires $\widehat\zeta_G(P_B-P_G)$, consistent with equations (10)–(11). Its drift and intensity notation also drops the risk-neutral hats; a valuation implementation should retain $\widehat\mu_G$ and $\widehat\zeta_G$. Separately, the text describing concavity in state $B$ prints a $G$ state index in the second derivative. These are derived transcription corrections checked against the main model, not assumptions that the published numerics necessarily used the erroneous formulas.

Figure 6’s caption says $B$ is absorbing, while its parameter sentence and nearby prose refer back to Table 1, where $\zeta_B=0.50$. The PDF does not resolve which specification produced that figure. Exact reproduction of its plotted boundaries should therefore test both cases or obtain author code. Quoting its numbers as an unambiguous recalculation of the baseline would overstate what the source establishes.

## Extensions, scope, and use in research

Appendix A allows $n$ financing/productivity states with generator terms $\sum_{j\ne s}\widehat\zeta_{sj}(p_j-p_s)$. Its stochastic discount factor has Brownian loading $-\eta_s$ and compensated transition jumps $e^{\kappa_{sj}}-1$, implying $\widehat\zeta_{sj}=e^{\kappa_{sj}}\zeta_{sj}$. Only transitions out of the current state are active. The first-best benchmark replaces cash management with algebraic equations for $q_s^{FB}$ and $i_s^{FB}$, satisfying $q_s^{FB}=1+\theta_s(i_s^{FB}-\nu_s)$.

Appendix D makes investment and financing opportunities correlated. One firm has productivity 0.227 in $G$ and 0.197 in $B$; the other reverses them. Both have the baseline financing costs and symmetric risk-neutral intensities 0.10. Figures D1–D2 show that positive correlation does not rank financing constraints uniformly: at low cash it can lower the marginal value of cash, while at higher cash the ranking reverses, sometimes in both states. Survival through poor conditions preserves the opportunity to exploit a particularly valuable good state. A single unconditional correlation therefore cannot replace the full state-dependent continuation value.

The framework is most useful as a structural mechanism and a disciplined generator of conditional predictions. Its cost parameters are partly judgmental; its two calibration targets cannot identify every financing friction; cash is observed and frictionless to reallocate; and taxes, debt maturity, credit commitments, asymmetric information, and agency conflicts are absent. Allowing negative investment assumes assets can be sold through the same adjustment-cost technology. Those restrictions should be preserved when reproducing the exercise and deliberately relaxed when applying it to a particular issuer.

A useful replication reports HJB residuals, intervention-value inequalities, stationary moments, sensitivity to grids and physical versus pricing intensities, and the convexity regions before interpreting investment or hedging policies. The paper’s central lesson survives without treating its point calibrations as estimates: financing conditions alter behavior before the financing shock, and endogenous cash policy determines how much of the shock appears in observed investment and returns.

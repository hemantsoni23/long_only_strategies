# Drawdown Control with a Risk Floor

Joe Zhou and James Shang. *The Journal of Alternative Investments*, 17(4), Spring 2015, pp. 79–94. The supplied PDF includes the 16-page article and an issue contents/abstract page.

Source: [Drawdown_ZhouShang_2015.pdf](<../../Finance/Drawdown_ZhouShang_2015.pdf>). Page references below use printed journal pages. This note covers both appendices, which contain the policy solution and the transaction-cost argument.

## Why this matters

A drawdown rule can reduce exposure so aggressively near its limit that trading to maintain the rule consumes the expected investment return. Zhou and Shang examine this failure for the Grossman–Zhou policy with a decaying high-water mark. They propose maintaining a positive minimum volatility, even after the nominal drawdown trigger has been reached. The resulting portfolio retains a chance of recovering instead of following the declining reference level with negligible investment risk.

The tradeoff is substantive: a positive risk floor relinquishes the original hard drawdown guarantee. The paper's solution is a modified **frictionless** control policy; transaction costs motivate the modification and enter simulations, but the authors do not solve an optimal control problem with transaction costs. Their discussion of a possible no-trade region is a conjecture about a fuller solution. A fixed positive portfolio volatility still requires some trading, so it is not literally a no-trade rule.

The useful contribution is the connection among the state dependence of exposure, the frequency needed to track that exposure, transaction costs, and recovery from a drawdown. Its numerical illustrations should be read as experiments under a specified diffusion, not evidence from historical hedge-fund returns.

## Market, state, and objective

There is a riskless asset with constant rate $r$ and a risky asset with constant excess drift $\mu$ and volatility $\sigma$. Write $S=\mu/\sigma$ for its instantaneous annual Sharpe ratio, $X_t$ for dollars invested in it, and $\eta_t=X_t/\mathcal W_t$ for the risky fraction. Nominal wealth obeys

$$
\frac{d\mathcal W_t}{\mathcal W_t}=r\,dt+\sigma\eta_t(S\,dt+dZ_t).
$$

Leverage is possible in this idealized model. The portfolio volatility is $v_t=\sigma\eta_t$, with positive exposure in the examples. All time units must agree: an annual Sharpe ratio cannot be combined directly with a daily volatility and an annual time increment.

The decayed high-water mark is

$$
\mathcal M_t=\max\left\{\mathcal M_0e^{\bar\lambda t},\sup_{0\le s\le t}\mathcal W_s e^{\bar\lambda(t-s)}\right\}.
$$

The usual fixed historical maximum is the case $\bar\lambda=0$. A negative $\bar\lambda$ lets old peaks decay, whereas a positive value raises the reference level. Discounting both wealth and mark by $e^{\bar\lambda t}$ produces $W_t$ and $M_t$, where $M_t$ is the running maximum of transformed wealth. The transformed cash rate is

$$
\lambda=r-\bar\lambda\ge0.
$$

The normalized state is $u=W/M=\mathcal W/\mathcal M$. Decayed drawdown is $1-u$. In the original Grossman–Zhou problem, $u\ge\alpha$, with $0<\alpha<1$, is a hard constraint. When $r=0$ and the mark decays 12% per year, $\bar\lambda=\log(0.88)$ and $\lambda\approx0.1278$. Thus the apparently large positive $\lambda$ is mainly reference-level decay, not a cash yield.

The objective is long-run certainty-equivalent growth for constant relative risk aversion $A$, using power utility. In transformed units it is expressed through

$$
\xi=\sup_\eta\liminf_{T\to\infty}\frac{1}{(1-A)T}\log E[W_T^{1-A}].
$$

The nominal growth rate is $\bar\xi=\xi+\bar\lambda$, so the growth premium above cash satisfies $\bar\xi-r=\xi-\lambda$. This is neither the expected arithmetic return nor a finite-horizon return quantile. The derivation assumes the same continuous, frictionless diffusion setting as the underlying Grossman–Zhou framework.

The proposed modification requires portfolio volatility $v(u)=q>0$ when $u\le\alpha$. Above the trigger, volatility is chosen using the modified boundary condition. The path can therefore pass below $\alpha$. A portfolio subject to a contractual absolute drawdown limit cannot substitute this policy without changing the mandate.

## Frictionless risk-floor policy: a reconstructible solution

Appendix A, pp. 89–91, exploits wealth homogeneity. In the active region $\alpha\le u\le1$, the optimality equation can be written for portfolio volatility rather than dollar exposure. Define

$$
\phi=\frac{2[(1-A)\xi+S^2/2-\lambda]}{S}.
$$

The differential equation and boundary conditions are

$$
(u v'(u)+v(u))v(u)=\phi v(u)+2\lambda,
\qquad v(\alpha)=q,
\qquad v(1)=\frac{2(\xi-\lambda)}{S}.
$$

The final condition comes from the running-maximum boundary of the value function, not from arbitrarily fixing exposure at a new high. Once $v$ is obtained, the risky fraction is $\eta(u)=v(u)/\sigma$. The solution is governed by $S,A,\lambda,\alpha,q$; underlying volatility is additionally needed to convert target portfolio volatility into dollars of the traded asset.

For $\lambda=0$, the equation becomes $d(uv)/du=\phi$. Consequently,

$$
 v(u)=\phi+\frac{\alpha}{u}(q-\phi),
\qquad
\phi=\frac{S-\alpha(A-1)q}{(1-\alpha)A+\alpha}.
$$

Together with $v(1)=2\xi/S$, this gives the growth rate. Setting $q=0$ recovers the original Grossman–Zhou solution. For implementation, the increasing-exposure branch requires $\phi\ge q$, equivalently $q\le S/A$. This condition follows directly from the displayed solution: an imposed floor above the unconstrained Merton volatility is a different regime from the monotone increasing policy illustrated in the article. The paper does not supply a comprehensive parameter-domain treatment of such extreme floors.

For $\lambda>0$, let

$$
\nu_1=\frac{-\phi-\sqrt{\phi^2+8\lambda}}2<0,
\qquad
\nu_2=\frac{-\phi+\sqrt{\phi^2+8\lambda}}2>0,
\qquad
\delta=-\frac{\phi}{\sqrt{\phi^2+8\lambda}}.
$$

Integration yields the implicit curve

$$
 u^2|v(u)+\nu_1|^{1-\delta}|v(u)+\nu_2|^{1+\delta}=c,
$$

where

$$
 c=\alpha^2|q+\nu_1|^{1-\delta}|q+\nu_2|^{1+\delta}.
$$

There are two nested scalar problems. First, for a trial $\xi$, calculate $\phi,\nu_1,\nu_2,\delta$, evaluate the expression at $u=1$ and $v=2(\xi-\lambda)/S$, and match it to $c$. Second, with that $\xi$, solve the implicit equation at each desired $u$. Use logarithms of the product away from a zero factor, and select the continuous economic branch attached to $v(\alpha)=q$. A generic root finder without branch tracking can return an irrelevant solution because the formula contains absolute values.

An implementation should verify the two boundary residuals and the ODE residual on an interior grid, inspect monotonicity, and refine the grid near $\alpha$. Below $\alpha$, use the prescribed floor $q$, not an extrapolation of the upper-region equation. Numerical brackets, tolerances, and code are not supplied by the authors. These checks and the log-domain implementation are reconstruction guidance, not claims about their original program.

For the main example, the upper-region policy resembles an original Grossman–Zhou policy with a looser implied hard threshold: the paper reports an implied drawdown limit of 20.44% instead of the 20% trigger. That is a way to describe the upper curve. The actual risk-floor portfolio is clamped to positive risk below its trigger; the implied 20.44% level is not a second guaranteed loss barrier.

The appendix obtains the boundary-value solution by adapting the Grossman–Zhou Bellman argument. It does not provide a separate exhaustive verification theorem for every floor, all excursions below the trigger, and every admissibility condition. This matters when extending the rule outside the illustrated parameter range. The formulas reconstruct the policy presented in the article; they should not be treated as a general transaction-cost optimality theorem.

## How familiar sizing rules fit the framework

The unconstrained Merton risk level is $S/A$. With logarithmic utility, $A=1$, it is $S$, the continuous-time Kelly risk level. If $S=0.5$, Kelly volatility is 50% annually; scaling risk down to 1% daily, or approximately 15.87% annually, corresponds to risk aversion around 3.15. This is an illustration of risk scaling, not a forecast of an attainable trading Sharpe ratio.

For a fixed cash floor $K$, constant proportion portfolio insurance has risky dollars

$$
X=\frac{S}{\sigma A}(W-K).
$$

For the Grossman–Zhou case $\lambda=0$ and zero risk floor,

$$
X=\frac{S}{\sigma A^*}(W-\alpha M),
\qquad A^*=(1-\alpha)A+\alpha.
$$

The distinction is the moving reference level and adjusted effective risk aversion. Replacing $K$ by $\alpha M$ in the fixed-floor formula while retaining the same multiplier would not reproduce the optimum. When $\lambda>0$, the risk curve is nonlinear and cannot generally be represented by one constant insurance multiplier.

## Transaction costs: what is being traded

Appendix B, pp. 91–93, starts from the original zero-floor Grossman–Zhou target. Trading is the difference between desired risky dollars at the next rebalance and the value of the risky holding carried from the previous rebalance. It is not simply the change in target exposure fraction. Locally, the risky trade divided by current wealth is

$$
\frac{\Delta X-X\Delta P/P}{W}=\mu_T\Delta t+\sigma_T\Delta Z+o(\Delta t).
$$

The signed diffusion coefficient is

$$
\sigma_T=\big[u\eta'(u)+\eta(u)-1\big]\sigma\eta(u).
$$

Using the optimality equation gives the convenient expression

$$
\sigma_T=(\phi-\sigma)\eta(u)+\frac{2\lambda}{\sigma}.
$$

Expected absolute trading volume uses $|\sigma_T|$. The illustrations use a branch where the reported coefficient is positive. With proportional cost $T_c$ per unit of traded notional, the leading cost rate is

$$
\frac{E[\mathrm{cost}]}{W\Delta t}
\approx T_c\sqrt{\frac2\pi}\frac{|\sigma_T|}{\sqrt{\Delta t}}.
$$

This follows from the leading absolute moment of a centered normal increment. The general folded-normal formula printed on p. 92 has the wrong prefactor in its first term: for $X\sim N(a,b^2)$, that prefactor must be $b\sqrt{2/\pi}$, not $a\sqrt{2/\pi}$. The subsequent leading-order trading-volume expression uses the appropriate volatility scaling.

The authors use a Leland-style small-time approximation with $k=T_c/\sqrt{\Delta t}$. Their adaptive tracking rule keeps the expected relative target deviation approximately constant:

$$
\frac{|\sigma_T(u)|}{\eta(u)}\sqrt{\Delta t(u)}=\text{constant}.
$$

Thus the time between trades decreases when target sensitivity rises relative to target exposure. Equivalently, $k(u)=k_0|\sigma_T(u)|/\eta(u)$ for a calibration constant $k_0$. The nominal expected wealth drift becomes approximately

$$
\mu_{\mathcal W}(u)=r+S\sigma\eta(u)
-\sqrt{\frac2\pi}\,k_0\frac{\sigma_T(u)^2}{\eta(u)}.
$$

The approximation treats the leading random cost fluctuation as negligible in its scaling limit. It is not an exact finite-step self-financing accounting identity with a fixed positive transaction fee.

For $\lambda=0$, relative sensitivity is constant, so the calibrated interval is constant and costs act like a reduction in the effective Sharpe ratio. For $\lambda>0$, as $u\downarrow\alpha$, target risk tends to zero while $\sigma_T$ approaches $2\lambda/\sigma$. Rebalancing more frequently to track a vanishing position then makes the cost term diverge negatively. The source obtains

$$
 v(u)\sim2\sqrt{\lambda/\alpha}\sqrt{u-\alpha},
\qquad
\mu_{\mathcal W}(u)\to-\infty.
$$

The claim concerns this particular adaptive implementation and local asymptotic model. A fixed daily rebalance has a different limiting cost rate; one should not infer infinite losses for every possible discrete implementation of a drawdown rule. Likewise, the diffusion approximation becomes delicate exactly where required trading intervals approach zero.

Using scale and speed calculations for the approximating state diffusion, the paper classifies the lower boundary as attracting, attainable, and absorbing when $\lambda>0$ and costs are present. This explains the simulated trapping phenomenon, but the classification is attached to the approximate cost-adjusted process. It is not a proof that all realistic market implementations have an absorbing loss state.

## Numerical design and reported results

The main calibration on pp. 80–84 uses $S=1$, underlying volatility 1% per trading day, $r=0$, $\alpha=0.8$, and a mark that decays 12% per year. Risk aversion is $A=6.129$, chosen so that the original policy holds 100% exposure, or 1% daily portfolio volatility, at a new high. The transaction cost is 0.10% of traded notional. The adaptive interval is anchored at one day when decayed drawdown is 18%.

Under that calibration, expected return becomes negative at a decayed drawdown of 19.60%, before the nominal 20% limit. Exposure there is 28.83% of its value at zero drawdown. The required trading interval is 0.1042 day, about 50 minutes using an eight-hour trading day. The last conversion follows the article's convention; it is not a universal exchange session length.

The principal Monte Carlo comparison introduces a floor equal to 30% of the initial risk: 0.30% daily volatility, approximately 4.762% annually. It starts at a decayed drawdown of 19%, uses 100,000 runs, a minimum step of 0.01 day, and rebalances when the relative exposure deviation exceeds 5%. Other parameters, including proportional costs, remain as above. The article examines return distributions over three, six, and twelve months.

Exhibit 3 shows a concentration of original-policy one-year outcomes near a loss of 12%, consistent with following the decaying mark after risk has collapsed. The floor spreads outcomes more broadly and leaves more recovery potential. Exhibit 4 reports the **20th percentile**, not the expected shortfall or the mean of the worst fifth of observations:

| Horizon | Original policy | 30% risk floor | Improvement |
|---|---:|---:|---:|
| 3 months | −1.10% | −0.76% | 0.34 percentage point |
| 6 months | −3.74% | −1.94% | 1.80 percentage points |
| 12 months | −12.40% | −2.47% | 9.93 percentage points |

These are conditional simulation outcomes from an already distressed starting state. They do not estimate unconditional annual performance for a fund starting at a fresh high. Nor do they establish that the risk floor improves every lower quantile, worst-case loss, or tail expectation. Maintaining positive risk permits deeper drawdowns, even when this particular 20th percentile improves.

The sensitivity illustrations vary $S$ across 0.5, 1, 1.5, and 2, holding other parameters fixed. Higher skill supports more risk away from the floor. Other exhibits vary $\lambda$ through 0%, 2%, 5%, 10%, 15%, and 30%; faster reference-level decay delays exposure reduction and makes the final reduction toward the trigger steeper. The growth comparison is a certainty-equivalent growth calculation, not a table of realized returns. Graphs should not be turned into spurious high-precision estimates.

## Replication details that remain unspecified

No historical return sample, security universe, or estimation window is used. The inputs are fixed model parameters, so there is no train/test split or fitted signal. The PDF supplies equations, parameter choices, selected simulation controls, and figures, but no source code, random seed, confidence intervals, or standard errors for the reported quantiles.

A replicator must specify how risky prices and cash evolve within each 0.01-day step; whether the high-water mark is monitored continuously or only at grid points; whether the cost deduction can itself trigger another trade; and whether the 5% deviation is measured against desired or current exposure. The minimum step also prevents arbitrarily rapid trading, whereas the analytical cost argument studies a shrinking-interval limit. These are distinct experiments and should be documented separately.

For a transparent reconstruction, solve both target curves first, use common Brownian paths for the paired portfolios, update holdings and cash before deciding a trade, deduct costs on the actual risky notional traded, and update the decaying mark consistently with net wealth. Report both the stated trigger and realized drawdowns. Refine the simulation step and examine threshold sensitivity before treating the reported percentile differences as numerically stable. These are suggested implementation choices and diagnostics; the source does not state that it followed this exact event order.

A second practical issue is capacity. Appendix B assumes the market can absorb $L\sqrt{\Delta t}$ dollars over an interval, leading near the original limit to the bound

$$
\lambda<\sqrt{\frac\pi2}\frac{\sigma}{2\alpha}\frac{L}{M_t}.
$$

This bound is derived from the preceding volume inequality $u|\sigma_T|<\sqrt{\pi/2}L/M_t$ and $\sigma_T\to2\lambda/\sigma$. The final printed bound on p. 93 instead has coefficient $\sqrt{2\pi}$ multiplying $(\sigma/\alpha)(L/M_t)$, four times too large. The article's example reports an annual cap of about 15% for $L/M_t\approx30\%$, $\sigma=1\%$ daily, and $\alpha=0.8$. Using 15.87% annual volatility and the stated 30% liquidity ratio in the same annual time units, the preceding inequality implies about 3.73%, rather than 15%. Because $L$ has units of dollars per square-root time, its time convention must also be recorded when converting the example. This is a stylized liquidity scaling, not an estimated market-impact function. Its reliable implication is that allowed reference decay depends on capacity relative to portfolio size. The printed numerical cap should not be used without correcting the algebra and fixing the time units.

## Limits and practical interpretation

The risky opportunity has constant skill and volatility. There are no jumps, financing spreads, bid–ask nonlinearities, time-varying liquidity, leverage caps, taxes, or endogenous alpha decay. Even the original hard floor relies on continuous paths and trading. A risk floor adds deliberate exposure beyond the trigger and therefore makes the mandate tradeoff more explicit.

The paper supports designing the exposure curve jointly with a feasible tracking rule. It also suggests evaluating recovery distributions from distressed states, rather than judging a drawdown controller solely by its attractive curve near new highs. Its results do not justify retaining positive risk after evidence that the underlying strategy has lost its edge: the simulation assumes a positive, unchanged $S$ throughout. Finally, the article cites later qualifications to the original Grossman–Zhou framework; its adapted Bellman construction should be used with its admissibility and asymptotic qualifications, not as a universal optimality claim.

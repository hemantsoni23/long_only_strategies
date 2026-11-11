# A Model of Returns and Trading in Futures Markets

**Harrison Hong, 2000.** *Journal of Finance* 55(2), 959–988. [Source PDF](../../Finance/CommodityPrices_Hong_2000.pdf). The supplied 31-page scan contains a JSTOR cover and the complete 30-page article, including six figures, the mathematical appendix, the numerical procedure, and references. All pages were read; the model equations, numerical captions, and appendix were checked against rendered pages. Printed page 959 corresponds to PDF page 2.

## Why this matters

Why does futures price volatility sometimes fail to rise monotonically as delivery approaches? The usual Samuelson argument says a transitory fundamental shock has little effect on distant delivery but a larger effect on nearby delivery. Hong adds endogenous information revelation: futures prices contain both information about fundamentals and noise from investors' hedging needs, and their relative sensitivities change with maturity. A contract can become less informative near delivery even while its direct sensitivity to a fundamental shock increases. The information effect can outweigh the ordinary maturity effect and create a hump in volatility.

The paper's distinctive contribution is a dynamic competitive rational-expectations model in which spot prices, futures prices, learning, hedging, and speculative positions are determined together. Earlier static noisy-information futures models could not describe a contract's life cycle. Models with an exogenous spot process or a representative fully informed investor generally omit the particular feedback between maturity, informative prices, and adverse selection emphasized here.

Hong also connects this mechanism to open interest and to the effect of introducing a futures market on spot volatility. The model can generate declining or hump-shaped open interest and lower spot volatility when futures improve risk sharing. These are theoretical possibilities and numerical comparative statics. The paper does not estimate its model on a new dataset, report sample regression coefficients, test a tradable signal, or measure returns after costs. Its review of commodity-market evidence motivates the model rather than constituting independent empirical validation of its parameterization.

The relevant market is one where spot and futures are not redundant through a simple cash-and-carry trade. The spot pays a stochastic convenience yield, and investors bear nonmarketed risks and possess different information. A weak Samuelson effect in a financial or precious-metal market close to cost of carry is not automatically evidence for this mechanism; Hong explicitly makes that qualification. Equally, the model does not include physical stockouts, endogenous production, or inventory nonnegativity, all of which can affect actual commodity curves.

## Assets, timing, and endowments

Time is discrete and infinite. A riskless asset has perfectly elastic supply at constant gross return $R=1+r$, with $r>0$. One unit of the risky spot asset pays

$$
D_t=Z_t+\varepsilon_{D,t},\qquad
Z_t=a_ZZ_{t-1}+\varepsilon_{Z,t},\quad 0\le a_Z\le1.
$$

The persistent component $Z_t$ determines expected future convenience yields. The spot can be interpreted as a claim on services from commodity inventories; it is modeled as a divisible financial claim paying an exogenous dividend. The innovation $\varepsilon_D$ is temporary payoff noise. Treating this as an endogenous physical-storage model would add structure the paper deliberately omits.

At most one futures contract trades at a time. Contract $k$ is introduced at $t_k$, expires after $M$ periods at $m_k=t_k+M$, and the next contract begins at $t_{k+1}=m_k+N$. The cycle has length $M+N$. When $N=0$, a new contract begins exactly as the old one expires. When $N>0$, there is a period without futures trading. Figure 1 depicts the zero-gap case. This structure is a tractability device; it is not the simultaneous ladder of delivery months observed on commodity exchanges.

Let $S_t$ be spot price and $H_t$ the currently outstanding futures price. At delivery, $H_{m_k}=S_{m_k}$. Futures positions are chosen through $m_k-1$; the terminal price difference settles at $m_k$. There is no ambiguity about prices at a date when the next contract is introduced, because the expiring contract's price is pinned to spot. A simulation must nevertheless keep contract identities separate and must not treat the switch to a new maturity as an ordinary daily return on the old contract.

There are two classes of investors, $a$ and $b$, with population weights $\omega$ and $1-\omega$. Each initially owns one spot share. Aggregate spot supply per investor is therefore one, while futures have zero net supply. Investors within a class are identical. Class $a$ additionally receives nonmarketed income

$$
q_{t+1}=Y_t+Y_t\varepsilon_{q,t+1},
\qquad Y_t=1+Y_{1,t}+Y_{2,t},
$$

$$
Y_{j,t}=a_{Y_j}Y_{j,t-1}+\varepsilon_{Y_j,t},
\qquad 0\le a_{Y_j}<1,\quad j=1,2.
$$

The same $Y_t$ scales the conditional mean and shock exposure of this income. Thus conditional income variance is $Y_t^2\sigma_q^2$, and its covariance with next period's spot dividend is $Y_t\kappa_{Dq}\sigma_D\sigma_q$. The scaling is not an additive independent endowment shock. Gaussian states can make $Y_t$ negative; the formulation is a tractable risk-exposure model rather than a literal nonnegative production-income process.

All primitive innovations are jointly Gaussian and independent over time. Their only nonzero cross-correlation is $\operatorname{Corr}(\varepsilon_{D,t},\varepsilon_{q,t})=\kappa_{Dq}>0$. The sign ensures that class $a$ wants to hedge its endowment exposure through marketed assets. Hong notes that reversing the sign would change position directions rather than the basic mechanism. The two separate persistent $Y$ factors also help prevent the two observed market prices from revealing all private information exactly.

## Information and preferences

Both investor classes observe the histories of dividends, spot prices, and futures prices. Class $a$ also observes the true fundamental $Z$, its nonmarketed income, and both endowment-state variables. Class $b$ sees only public information and rationally filters the hidden state. Its ignorance is therefore endogenous: prices are signals, but their movements reflect hedging demand as well as private information about future dividends.

Investors maximize expected discounted CARA utility of consumption,

$$
E_{i,t}\left[-\sum_{s=t}^{\infty}\rho^{s-t}e^{-\gamma c_{i,s}}\right],
\qquad i\in\{a,b\}.
$$

They can trade spot and futures competitively at no cost. Define the next-period per-share spot excess payoff and futures payoff as

$$
Q^S_{t+1}=S_{t+1}+D_{t+1}-RS_t,
\qquad Q^H_{t+1}=H_{t+1}-H_t.
$$

Wealth evolves according to

$$
W_{i,t+1}=R(W_{i,t}-c_{i,t})+
\theta^S_{i,t}Q^S_{t+1}+\theta^H_{i,t}Q^H_{t+1}
+\mathbf1_{\{i=a\}}q_{t+1}.
$$

These are dollar or consumption-unit payoffs per share or contract, not returns divided by a spot price or by futures margin. In particular, a futures contract has zero initial value, so $\Delta H$ is a payoff convention rather than an ordinary investment-rate return. Hong calls the variance of this payoff “return volatility.” Replacing it with percentage price volatility changes the reported object and can alter maturity patterns through the denominator.

CARA preferences and a constant riskless rate make risky positions independent of wealth. This supports linear equilibrium prices even though agents differ in wealth histories. It also eliminates wealth effects, leverage constraints, margin liquidity, default, bid-ask spreads, and transaction costs from the model. Risk sharing is frictionless conditional on information and the available securities. Adverse selection here arises through rational inference and equilibrium compensation, not through an explicit dealer spread or order-book model.

## Linear periodic equilibrium

Let

$$
G_t=(Z_t,Y_{1,t},Y_{2,t})',\qquad
\widehat G_t=E[G_t\mid\mathcal N_t],\qquad
\Delta_t=G_t-\widehat G_t.
$$

Hong conjectures prices linear in the true states and estimation errors:

$$
S_t=\lambda_{S,Z}(t)Z_t-\lambda_{S,X}(t)X_t,
\qquad
H_t=\lambda_{H,Z}(t)Z_t-\lambda_{H,X}(t)X_t,
$$

$$
X_t=(1,Y_{1,t},Y_{2,t},\Delta_t')'.
$$

All coefficient functions repeat every $M+N$ periods. Realized prices do not repeat: the state changes even when the calendar-phase coefficients are identical. At expiration the spot and futures coefficient vectors coincide. Equilibrium requires optimal consumption and portfolios, the information filter implied by those prices, and coefficient-by-coefficient market clearing:

$$
\omega\theta^S_{a,t}+(1-\omega)\theta^S_{b,t}=1,
\qquad
\omega\theta^H_{a,t}+(1-\omega)\theta^H_{b,t}=0.
$$

This is a fixed point among prices, beliefs, and demands. Estimating a Kalman filter from arbitrary price loadings and then applying a standard mean-variance hedge does not solve it. The chosen price loadings must make the resulting optimal portfolios clear both markets at every state and every phase of the contract cycle.

## The learning problem in implementable notation

The hidden state follows $G_t=AG_{t-1}+\eta_t$, with $A=\operatorname{diag}(a_Z,a_{Y_1},a_{Y_2})$ and diagonal innovation covariance $Q_G=\operatorname{diag}(\sigma_Z^2,\sigma_{Y_1}^2,\sigma_{Y_2}^2)$. Known intercepts and known functions of the uninformed estimate can be subtracted from observed prices to obtain effective linear signals. Write them as

$$
n_t=C_tG_t+\nu_t.
$$

The two effective price signals are noiseless linear combinations conditional on the full hidden state; their “noise” economically is the unobserved hedging factors. The dividend signal is $Z_t+\varepsilon_{D,t}$. Hence the signal-noise covariance has zeros for the price rows and $\sigma_D^2$ for the dividend row. The relevant state innovations are uncorrelated with dividend noise. The correlation between dividend and nonmarketed-income shocks affects portfolio choice, not this particular state-observation covariance.

Given posterior covariance $P_{t-1}$, the filter is

$$
P_t^-=AP_{t-1}A'+Q_G,
\qquad
K_t=P_t^-C_t'(C_tP_t^-C_t'+R_n)^{-1},
$$

$$
\widehat G_t=A\widehat G_{t-1}
+K_t(n_t-C_tA\widehat G_{t-1}),
\qquad
P_t=(I-K_tC_t)P_t^-.
$$

The source calls the covariance $o(t)$. It is deterministic once the periodic price coefficients are fixed. The information-asymmetry measure used in the figures is

$$
\delta(t)=\sqrt{P_t(1,1)},
$$

the posterior standard deviation of the fundamental error. This is an uncertainty measure conditional on public information, not the unconditional volatility of $Z$ and not a direct estimate of a bid-ask spread.

There are numerical details at expiration. Since spot and the expiring futures have identical payoffs and prices, their signal rows become redundant. A robust implementation should remove redundant rows or use an appropriate rank-aware covariance solve rather than blindly invert a singular signal matrix. During the $N$ periods with no futures market, the futures signal and trading control must be removed. The appendix writes the proof for $N=0$ and says the extension is straightforward; it does not provide code for either case.

Equation (A3) prints the forecast innovation as an observed signal minus its conditional expectation at time $t$. Taken literally with that signal in the time-$t$ information set, the innovation would vanish. The intended Kalman prediction is the expectation before the new signal, as written above. The appendix also switches between primitive shocks with stated standard deviations and matrices that multiply standard deviations. An implementation must choose either unit-variance standardized shocks with volatility loadings or shocks already carrying those variances, avoiding double scaling.

## Dynamic portfolio choice and computation

The conditional state for class $a$ includes the six entries of $X_t$. Class $b$ needs only $(1,\widehat Y_{1,t},\widehat Y_{2,t})$ after conditional expectation, since it sets the estimation errors' conditional means to zero. The underlying innovation representation for class $b$ incorporates its previous state-estimation error as well as the new primitive shocks. This is why its uncertainty cannot be represented by the informed investor's covariance matrix with a single extra scalar variance.

The value-function form is exponential-quadratic:

$$
J_{i,t}=-\rho^t\exp\left[-\alpha W_{i,t}
-\frac12X_{i,t}'V_i(t)X_{i,t}\right],
\qquad \alpha=\frac{r\gamma}{R}.
$$

The factor $\rho^t$ is an inconsequential time normalization relative to utility discounted from the current date. The optimal risky positions are linear, $\theta_{i,t}=h_i(t)X_{i,t}$. The matrices $V_i$ satisfy backward nonlinear recursions derived by substituting the value function into the Bellman equation and integrating Gaussian innovations. The filter runs forward, whereas continuation values and pricing conditions link adjacent phases in the opposite direction. Periodicity closes the system as a boundary-value problem.

A convenient way to reproduce the appendix's integration is to express the next conditional state and returns as $X'=AX+B\epsilon$ and $Q'=CX+D\epsilon$, where $\epsilon$ has conditional covariance $\Sigma$. These matrices are investor-specific here, so they should not be confused with the hidden-state matrices in the preceding section. Let $V$ be the next-period value matrix. For class $a$, write income as $eX+(eX)b_q\epsilon$, with $e$ selecting $1+Y_1+Y_2$; set its income indicator $d_i$ to one, and set it to zero for class $b$.

Completing the Gaussian square gives

$$
\Omega=(\Sigma^{-1}+B'VB)^{-1},
\qquad
J_{X\epsilon}=A'VB+\alpha d_ie'b_q,
$$

$$
g=C-D\Omega J_{X\epsilon}',
\qquad
h_i=\frac1\alpha(D\Omega D')^{-1}g.
$$

This notation reconstructs the appendix's portfolio first-order condition. The $A'VB$ term captures changes in future investment opportunities; the $e'b_q$ term captures endowment hedging. A static covariance-to-variance hedge would omit the first term. Gaussian integration also contributes the determinant factor $|I+\Sigma B'VB|^{-1/2}$ to the continuation value, which affects the consumption rule and constant term in the value recursion. The inverse and expectation require the relevant covariance and exponential-integrability conditions; a numerical root that violates them is not an admissible solution.

The remaining recursion can be implemented by substituting this portfolio rule and the optimal consumption rule back into the original Bellman equation and matching the constant, linear, and quadratic coefficients in $X$. This is preferable to guessing missing constants from an OCR transcription. The source gives the full matrix construction in (A8)–(A16), including investor-specific dimensions and state transition loadings. The mean endowment term is linear in the state and must be represented through the constant state coordinate when matching quadratic forms.

Hong solves the full system using Newton–Kantorovich iteration: linearize the nonlinear equations and periodic boundary conditions around a trial solution, solve for an update, and repeat. He obtains starting values from the economy with $\omega=1$, then reduces $\omega$ gradually to remain on a solution branch. He also checks solutions by starting from zero endowment-state innovation variances, where a closed-form solution exists. Additional limits such as $\sigma_Z\to0$ are used as checks. The article gives no executable code, convergence tolerance, step-size schedule, or numerical residual table.

The existence theorem is local and generic. It proves a linear periodic equilibrium when $\omega$ is sufficiently close to one or when $\sigma_{Y_1}$ and $\sigma_{Y_2}$ are sufficiently close to zero. It does not quantify the required neighborhoods or prove global uniqueness. The proof combines bounded periodic filtering, Riccati-style control bounds, fixed-point arguments, and an implicit-function continuation. The numerical examples farther from these limits show computed solutions, not a theorem covering all admissible parameters. Hong explicitly says he does not know uniqueness.

## Symmetric-information benchmark

When both classes observe $G_t$, no filtering error remains. Spot and futures have the forms

$$
S_t=\lambda_{S,Z}Z_t-\lambda_{S,0}(t)
-\lambda_{S,1}(t)Y_{1,t}-\lambda_{S,2}(t)Y_{2,t},
$$

$$
H_t=\lambda_{H,Z}(t)Z_t-\lambda_{H,0}(t)
-\lambda_{H,1}(t)Y_{1,t}-\lambda_{H,2}(t)Y_{2,t},
$$

with $\lambda_{S,Z}=a_Z/(R-a_Z)$ and $\lambda_{H,Z}(t)=\lambda_{S,Z}a_Z^{m_k-t}$. For $0<a_Z<1$, the fundamental loading increases as calendar time advances toward expiration, or equivalently decreases with remaining maturity. This is the price-sensitivity channel behind Samuelson's effect. The $Y$ terms are risk discounts induced by equilibrium hedging demand, even though they do not change the spot's future convenience-yield process directly.

Proposition 1 treats iid nonmarketed income by setting **innovation standard deviations** $\sigma_{Y_1}=\sigma_{Y_2}=0$. It does not merely set their persistence coefficients to zero. In the stationary version of that special case, $Y=1$ and the nonmarketed-income exposure is constant. The proposition proves the Samuelson effect and monotonically declining open interest as the contract expires. A fixed spot risk requires a larger futures position when a distant contract has a smaller fundamental loading.

In this special case, the one-step conditional futures innovation variance is $\lambda_{H,Z}(t)^2\sigma_Z^2$. For the spot, direct substitution in $Q_t^S=S_t+D_t-RS_{t-1}$ gives innovation $\varepsilon_{D,t}+(1+\lambda_{S,Z})\varepsilon_{Z,t}$ and hence variance $\sigma_D^2+(1+\lambda_{S,Z})^2\sigma_Z^2$. Appendix A18 and the preceding variance definition print a term involving $1+\lambda_{S,Z}^2$ instead. That differs by the cross term $2\lambda_{S,Z}\sigma_Z^2$ and appears inconsistent with the stated payoff equation. The direct return identity should be used to check a numerical replication rather than copying that expression without reconciliation.

For persistent hedging states, Hong illustrates the same qualitative symmetric-information pattern numerically; the paper does not prove it for every possible parameter vector. In Figure 2, futures loadings on both endowment factors increase near expiration, with the less persistent factor's loading especially small at long maturity. Futures volatility rises while open interest declines. The plotted volatility runs roughly from 0.007 to 0.012 and open interest from about 0.6 to 0.37 in model units. These are approximate visual readings, not tabulated estimates or market percentages.

## Asymmetric information and the numerical experiments

With private information, the futures price can be written in the reduced form

$$
H_t=\lambda_{H,Z}Z_t-\lambda_{H,0}
-\lambda_{H,1}Y_{1,t}-\lambda_{H,2}Y_{2,t}
+\lambda_{H,\widehat Z}(Z_t-\widehat Z_t),
$$

with positive speculative loading in the reported solutions. If uninformed investors underestimate the fundamental, informed investors buy futures and push its price upward. The uninformed side supplies risk bearing because a trade may reflect hedging needs rather than superior information. Price movements therefore reflect both information and the compensation needed to absorb a different exposure.

The numerical time unit is roughly a week. The reported interest rate is 0.05% per period, so $r=0.0005$, and $M=30$ periods is described as approximately a six-month contract. The informed population weight is $\omega=0.05$. Figure 2 uses $N=0$; later exercises use $N=30$ to separate expiration from the introduction of another futures contract. The recurring baseline parameters are

$$
\kappa_{Dq}=0.5,\quad \sigma_D=0.2,\quad \sigma_q=0.025,
\quad a_Z=0.98,\quad \sigma_Z=0.025,
$$

$$
a_{Y_1}=0.97,\quad \sigma_{Y_1}=0.075,
\quad a_{Y_2}=0.8,\quad \sigma_{Y_2}=0.05.
$$

These are illustrative model choices, not estimates from a named commodity sample. The figure captions and numerical discussion do not give an unambiguous complete value for every preference parameter used in every figure. The appendix's separate parameter vector with risk aversion 100 is used to demonstrate a nonzero determinant in the existence argument; it should not silently be treated as the figure calibration.

In Figure 3, the fundamental is more persistent than either hedging factor. A distant contract is relatively insensitive to transitory hedging noise, so its price reveals $Z$ quite well. As delivery approaches, the hedging-factor loadings rise, making prices noisier signals; posterior uncertainty $\delta(t)$ rises sharply. The figure shows $\delta$ increasing from roughly 0.003 to 0.05. Futures volatility first rises and then falls near expiration, while open interest declines. The key mechanism is the *change in informativeness over maturity*, not simply the presence of some private information.

The intuition is comparative and conditional. Holding other equilibrium effects fixed, more posterior uncertainty means less private information is incorporated into price movements and higher adverse-selection costs for uninformed risk bearers. Yet changing a primitive parameter also changes price loadings, demands, and filtering. It would be too strong to infer that increasing information asymmetry must lower every asset's volatility under every parameterization.

Figure 4 reverses the persistence ordering. The text sets $a_Z=0.95$, $a_{Y_1}=0.98$, and $a_{Y_2}=0.97$. The caption instead lists $a_{Y_2}=0.95$. This is a material discrepancy: the caption makes one hedging factor equally persistent as the fundamental rather than more persistent. An exact numerical reproduction needs the original computation or a sensitivity run for both values. The plotted result is falling information asymmetry as expiration approaches, monotonically increasing futures volatility, and hump-shaped open interest. Greater short-maturity informativeness reinforces the ordinary Samuelson effect, while improving risk sharing initially offsets the declining number of contracts needed for a hedge.

Figure 5 varies dividend-noise volatility $\sigma_D$ across 0.1, 0.15, and 0.2. Larger dividend noise makes the public payoff signal less informative about $Z$, increases posterior uncertainty, and strengthens its rise near expiration. The displayed futures-volatility curve becomes more clearly hump-shaped as that uncertainty increases. These are comparative-static solutions of different economies; they are not realized conditional-volatility forecasts from one fitted time series.

Figure 6 varies the less persistent endowment factor's autoregression coefficient $a_{Y_2}$ across 0.9, 0.8, and 0.6, holding $a_{Y_1}=0.97$. Lower persistence lets a sequence of prices reveal the persistent fundamental more clearly at distant maturities, while information asymmetry can still rise rapidly near expiration. The volatility curve can therefore turn down near delivery even when the overall level of information asymmetry is lower. The relevant slope and persistence contrast matter as well as its absolute level.

## Open interest, spot volatility, and empirical interpretation

The paper measures open interest using the average position of class $a$ scaled by its population weight. Because the two classes' futures positions clear, they hold opposite aggregate sides. For an implementation with state-dependent positions that can change sign, actual outstanding contracts are $\omega|\theta_a^H|=(1-\omega)|\theta_b^H|$ at each state, and average open interest involves the expectation of that absolute value. This differs from taking the absolute value of an average signed position. Hong's plotted convention should be reproduced explicitly before comparison with exchange statistics.

There are two forces on maturity-specific open interest. A distant contract is less sensitive to fundamental shocks, requiring more contracts to hedge a given spot position. Information asymmetry can simultaneously make uninformed counterparties less willing to absorb positions. If adverse selection increases with remaining maturity, these forces can offset and produce a hump. If it rises toward expiration, both forces can make open interest decline as delivery approaches. The mechanism applies to liquid intermediate maturities, while Hong notes that very near and very distant contracts can have low actual open interest for liquidity reasons absent from the model.

Expected futures payoffs and investor positions both depend on the endowment states. This gives a connection between hedging pressure, open interest, and expected returns. It does not establish that aggregate unsigned open interest alone identifies the sign or magnitude of a premium: the direction of hedgers' positions and the relevant state matter. The paper cites evidence that net-short hedging demand is associated with positive futures returns and net-long demand with negative returns, but does not provide a new predictive regression, estimation window, or portfolio test.

New futures can also reduce spot volatility by improving hedging. In the numerical argument, investors absorb more nonmarketed-risk shocks in their spot holdings, so spot price loadings on $Y_1$ and $Y_2$ fall. This is an equilibrium risk-sharing effect. The paper omits the corresponding comparative-static figures for brevity and supplies no estimated percentage reduction or causal event study of listings. It cites prior literature on commodity futures introductions and inventories. A claim that every new futures listing must reduce volatility would go beyond the theoretical and numerical evidence presented.

## Reproduction and research use

A computational reconstruction should begin with the exact contract calendar, payoff units, information sets, innovation covariance, and investor endowment exposure. Solve the symmetric-information or zero-endowment-state-volatility limit first. Verify delivery equality, market clearing, posterior covariance positivity, exponential integrability, and the Bellman residual. Continue parameters gradually to the asymmetric-information cases and track the solution branch. A low nonlinear solver residual alone is insufficient if the filter uses the wrong information date or if the expiring futures and spot signals are duplicated in a singular matrix.

Once a valid periodic solution exists, calculate return moments using the full state transition and the phase-specific price functions. The paper speaks of unconditional payoff variance. That includes variation in conditional expected payoffs across states as appropriate; it should not automatically be replaced by the conditional innovation variance used in the simple benchmark. For stationary calculations require $a_Z<1$ or handle the random-walk endpoint separately. Conditional filtering errors can remain bounded even when the level of a fundamental is nonstationary, but that does not make every unconditional level moment finite.

Exact figure reproduction remains limited by the missing code, unspecified tolerances, incomplete calibration details, caption discrepancy, and several appendix notation or printing issues. The article's structure is nevertheless sufficiently explicit to build the equilibrium from the primitive Bellman and filtering equations. A defensible replication should document corrections and distinguish a reconstructed solution from a verbatim reproduction of the original unpublished program.

An empirical test inspired by the paper would compare maturity-volatility and maturity-open-interest profiles across markets while controlling for seasonal information flow, contract rolls, liquidity, and physical inventory conditions. It would need independent measures or instruments for the persistence of fundamentals and hedging noise. Those are proposed research designs, not tests conducted here. Real trading applications would additionally need forecasts of the state, risk-premium mapping, contract sizing, margin funding, execution costs, and performance evaluated with forward information timing.

The durable result is that maturity changes what a futures price reveals as well as what payoff it represents. This creates a coherent joint explanation for nonmonotonic volatility and open-interest profiles. The theorem establishes local equilibrium existence and a transparent special case; the general maturity patterns are illustrated numerically. The paper is most useful as a model of those competing channels and as a source of testable restrictions, rather than as direct evidence of an exploitable futures return strategy.

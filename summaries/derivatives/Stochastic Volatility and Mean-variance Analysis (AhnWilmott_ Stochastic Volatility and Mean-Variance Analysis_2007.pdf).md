# Stochastic Volatility and Mean-variance Analysis

Hyungsok Ahn and Paul Wilmott. *Wilmott magazine*, technical article, pp. 84–90. The library filename supplies the year 2007; the supplied seven pages do not independently establish the issue date. Source: [AhnWilmott_ Stochastic Volatility and Mean-Variance Analysis_2007.pdf](../../Finance/AhnWilmott_%20Stochastic%20Volatility%20and%20Mean-Variance%20Analysis_2007.pdf). All seven pages, equations, figures, and numerical tables were read and visually checked. Page references below use printed pagination.

## Why this matters

A model that fits today's option quotes does not necessarily explain tomorrow's hedging profit and loss. Recalibrating a stochastic-volatility model can move its parameters even when the implementation treats them as fixed, while a hedge against the model's volatility state need not equal a hedge against changes in quoted implied volatilities. Ahn and Wilmott respond by treating the cash flow from an option position and its dynamic stock hedge as a risky object with a conditional mean and variance.

The useful contribution is an implementable sequence: specify physical dynamics; derive a stock hedge that minimizes the instantaneous residual variance; solve for the mean and remaining variance of discounted cash flows; and use traded options as static positions to improve a chosen reward-for-risk criterion. The result is a reservation value that depends on the remaining risk and the user's risk allowance. It is not a unique riskless replication price for every claim.

The worked barrier-option example illustrates why hedge selection and valuation should be solved together. A static vanilla-option portfolio reduces the reported residual variance by approximately 84%, and lowers the stated required premium for the short barrier claim. However, the PDF is a methodological article with a hypothetical example. It contains no fitted dataset, historical hedging experiment, or statistical validation of the quoted profitability probabilities. Several implementation conventions are missing or internally inconsistent, including the sign of the displayed static hedge. These qualifications are central to reconstructing the example faithfully.

## Physical dynamics and the cash-flow object

There is one non-dividend-paying tradable asset with price $S_t$ and one volatility-related state $Z_t$. Under the physical probability measure,

$$
dS_t=\mu(S_t,Z_t,t)S_t\,dt+\sigma(S_t,Z_t,t)S_t\,dW_{1,t},
$$

$$
dZ_t=p(S_t,Z_t,t)\,dt+q(S_t,Z_t,t)\,dW_{2,t},
\qquad d\langle W_1,W_2\rangle_t=\rho(S_t,Z_t,t)\,dt.
$$

The usual interpretation $Z=\sigma$ is a special case. The funding rate $r$ is constant for exposition. Dynamic trading is allowed in the stock and cash account, but other options are not dynamically traded. The calculation assumes frictionless continuous stock rebalancing; transaction costs are introduced only for the static option portfolio in the example. Suitable regularity, integrability, and boundary conditions are needed to give the stochastic integrals and PDE solutions meaning, although the article does not provide a formal existence theorem.

Let $P_i$ be a signed claim cash flow at date or stopping time $\tau_i$. With the paper's hedge convention, the stock holding is $-\Delta$. A consistent transcription of the future cash-flow object, correcting dummy integration-variable notation, is

$$
\Pi(t,T)=\sum_i e^{-r(\tau_i-t)}P_i(S_{\tau_i},\tau_i)
-\int_t^T e^{-r(u-t)}\Delta_u\,[dS_u-rS_u\,du].
$$

Positive $P_i$ denotes money received by the position. For the seller of a terminal call, the signed terminal payoff is negative. The initial option premium is excluded from $\Pi$ and can subsequently be added as a deterministic amount. This convention explains why the example has a negative unhedged mean even though the call's selling premium is positive.

Conditional on the current state, define

$$
m(S,Z,t)=E_t[\Pi(t,T)],\qquad
v(S,Z,t)=\operatorname{Var}_t[\Pi(t,T)].
$$

Both quantities are expressed in money discounted back to $t$. Thus $v$ has squared-money units, and $\sqrt v$ has the same units as $m$. The valuation criterion later called “mean-variance” actually combines the mean with the **standard deviation**, not with the variance itself.

The physical generator is

$$
\mathcal L=\tfrac12\sigma^2S^2\partial_{SS}
+\rho\sigma Sq\,\partial_{SZ}
+\tfrac12q^2\partial_{ZZ}+\mu S\partial_S+p\partial_Z.
$$

At dates without a claim payment, the one-step cash-flow recursion gives equation (2),

$$
m_t+\mathcal Lm-rm=(\mu-r)S\Delta.
$$

The right-hand side is the stock's expected excess gain removed by the hedge. Dropping it while leaving the physical drift $\mu$ in the generator would not reproduce the specified mean. For a single terminal payoff $P$, the terminal condition is $m(S,Z,T)=P(S,Z)$. For known intermediate payments, the mean jumps by the signed payment when moving backward across that date. The associated variance treatment must preserve the conditional cash-flow convention.

## Residual risk and the locally variance-minimizing hedge

The random part of a small change in the hedged mean is

$$
\sigma S(m_S-\Delta)\,dW_1+q m_Z\,dW_2.
$$

Its instantaneous variance rate is

$$
G(\Delta)=\sigma^2S^2(m_S-\Delta)^2
+2\rho\sigma Sq(m_S-\Delta)m_Z+q^2m_Z^2.
$$

The conditional-variance recursion in Section 5 therefore produces

$$
v_t+\mathcal Lv-2rv+G(\Delta)=0.
$$

The discount term is $2r$ because the discounted cash flow is squared. The source derives this equation by splitting future uncertainty into the next-step mean innovation and a conditionally mean-zero continuation residual. Their covariance vanishes by conditional expectation. It is not an assumption that all future cash-flow increments are unconditionally independent.

Holding the local derivatives of $m$ fixed, minimizing the quadratic $G$ yields equation (4):

$$
\Delta^*=m_S+\frac{\rho q}{\sigma S}m_Z,
\qquad G(\Delta^*)=q^2(1-\rho^2)m_Z^2.
$$

The second term uses the stock to hedge the part of volatility-state risk correlated with stock returns. Ordinary delta $m_S$ is sufficient when $\rho=0$, but then the orthogonal volatility risk remains. For $|\rho|=1$, the two Brownian risks collapse to one direction and the residual source term vanishes, subject to the regularity and replication assumptions. For $q=0$, there is no stochastic volatility-state innovation.

A necessary qualification concerns the word “optimal.” The paper explicitly selects the stock hedge by minimizing the instantaneous variance contribution. The mean function itself depends on the strategy through its PDE. The article does not prove that this local choice solves every possible global terminal-variance or expected-utility problem, especially when a nonzero stock risk premium creates intertemporal investment opportunities. A faithful implementation should use the displayed local criterion and should not silently reinterpret it as a universal optimal-control theorem.

The source says perfect hedging requires either $q=0$ or $|\rho|=1$. Its equation permits an additional claim-specific degeneracy: $m_Z=0$ along the relevant states also eliminates this source of risk. For example, a claim insensitive to the volatility state need not inherit its unspanned variance. A generic option with nonzero volatility sensitivity has residual risk when $q\ne0$ and $|\rho|<1$.

## The coupled PDEs and their interpretation

Define $\mathcal L^*$ by replacing the stock drift $\mu S\partial_S$ in $\mathcal L$ with $rS\partial_S$, while initially leaving $p\partial_Z$ unchanged. Substituting the selected hedge gives equations (5)–(6):

$$
m_t+\mathcal L^*m-rm
=\frac{\mu-r}{\sigma}\rho q m_Z,
$$

$$
v_t+\mathcal Lv-2rv
+q^2(1-\rho^2)m_Z^2=0.
$$

Equivalently, the mean PDE uses the effective volatility-state drift

$$
p^*=p-\rho q\frac{\mu-r}{\sigma}.
$$

The mean equation resembles an incomplete-market pricing PDE under a particular volatility-risk adjustment, but the authors arrive at it from physical cash-flow moments and their hedge criterion. The variance equation still uses the **physical** generator $\mathcal L$. Reusing $\mathcal L^*$ for both solves a different problem.

The computational ordering is simple. First solve the linear backward equation for $m$. Then compute its $Z$ derivative and use the nonnegative squared derivative as the source in the linear backward equation for $v$. Although the pair is coupled nonlinearly through $m_Z^2$, there is no need for a simultaneous nonlinear solve once the coefficients and payoff are specified. For a terminal-only payoff, $v(S,Z,T)=0$ because no future uncertainty remains after the state and payoff at expiry are known.

A useful derived representation, under the same regularity conditions, is

$$
v(S,Z,t)=E_{S,Z,t}^{\mathbb P}
\left[\int_t^T e^{-2r(u-t)}q_u^2(1-\rho_u^2)
m_Z(S_u,Z_u,u)^2\,du\right].
$$

For a knocked-out claim, the integration or state representation must respect the knock-out event. This expression supplies an implementation diagnostic: computed variance should be nonnegative, should vanish when the source vanishes, and should reflect the entire future volatility-sensitivity path. A single current vega is not a substitute for solving that path-dependent risk accumulation.

The model state must also be available to the trader. The article notes that a volatility index used by a model need not be directly observable, yet does not supply a filtering or estimation procedure for $Z_t$. Treating a noisy estimate as the true state adds estimation risk outside the displayed variance equation.

## Reservation values and probability claims

For a signed position the authors consider $m-\xi\sqrt v$, where $\xi$ is a selected risk allowance. For a short claim with no initial hedge cost, the premium needed to offset this criterion is $-m+\xi\sqrt v$. The example fixes $\xi=1$ to keep the illustration simple. For a long claim, the corresponding bid-style amount is the mean less the risk allowance.

If the discounted outcome were Gaussian, a one-sided 95% allowance would use $\xi=1.644853$. A one-standard-deviation allowance would imply approximately 84.13% probability of a favorable outcome relative to the relevant break-even threshold. These are distributional calculations, not probabilities established by the two PDEs alone. The source acknowledges that an option portfolio's outcome generally need not be normal.

Its appeal to the central limit theorem does not justify a one-trade Gaussian tail probability. Aggregation needs appropriate dependence, variance, and concentration conditions, and may be poor for barrier discontinuities or a portfolio dominated by a few risks. The final claim that the example makes money 84% of the time should therefore be read as a normal-approximation interpretation of the chosen buffer, not as a measured simulation frequency or distribution-free guarantee.

Figures 2–4 show a qualitative tradeoff: a higher risk allowance raises per-trade margin but may reduce the number of counterparties willing to trade. The curves are schematic. No demand function, arrival-intensity calibration, or optimization yielding an empirically optimal $\xi$ is reported. Selecting $\xi$ is consequently an additional decision input, not a parameter estimated by this paper.

## Barrier-option experiment

The claim is a short up-and-out call with strike 100, upper barrier 110, and expiry in 30 days. Initial stock price is 100 and initial annualized spot volatility is 20%. The authors set $Z=\sigma$, $\rho=0$, and physical volatility dynamics

$$
d\sigma_t=0.8(\sigma_t^{-1}-0.2)\,dt+0.5\,dW_{2,t}.
$$

The singular inverse-volatility drift should be transcribed as printed, not replaced by a familiar mean-reverting linear drift. The source does not specify its numerical treatment close to zero. Neither the stock drift $\mu$ nor funding rate $r$ is explicitly provided for the numerical example. The day-count convention converting 30 days to model time is also not stated.

Before knock-out, the terminal payoff is $-(S_T-100)^+$. At the barrier, the unhedged short claim has $m(110,\sigma,t)=v(110,\sigma,t)=0$, corresponding to no rebate. Expiry variance is zero. An implementation also needs lower-stock and volatility-domain boundary conditions and truncation levels, which are not supplied. The isolated symbol $X$ in the source's terminal domain is not defined there; the barrier-domain interpretation is $0<S<110$ before knock-out.

The reported unhedged results are $m=-1.1101$ and $v=0.3290$. They imply

$$
-m+\sqrt v=1.1101+\sqrt{0.3290}\approx1.683685.
$$

The table reports a selling value of 1.6836. The small difference is compatible with using unrounded numerical inputs. The variance peaks near the barrier in Figure 6 because the magnitude of $m_\sigma$ becomes large; that derivative drives the variance PDE even though the selected hedge is ordinary delta when $\rho=0$.

The six available hedge instruments are 30-day vanilla calls. Their hypothetical prices are generated with the alternative volatility drift $1/\sigma-0.2$ under a risk-neutral construction, then a stated 0.5% bid-ask adjustment. The quote table is the reproducible input; “0.5% spread” alone is ambiguous about full versus half spread.

| Strike | Bid | Ask | Printed hedge quantity |
|---:|---:|---:|---:|
| 96.62 | 4.6186 | 4.6650 | 0.0000 |
| 100.00 | 2.6774 | 2.7043 | −1.1688 |
| 104.17 | 1.1895 | 1.2014 | 1.0207 |
| 108.70 | 0.4302 | 0.4345 | 3.1674 |
| 112.36 | 0.1770 | 0.1788 | −3.6186 |
| 116.96 | 0.0557 | 0.0562 | 0.8035 |

These are model-generated quotes, not observed market data. There is no empirical universe, sample period, train/test split, cost calibration, or hypothesis test behind this table.

## Static hedge, coupled barrier states, and the sign inconsistency

Let $h_i$ denote actual signed call holdings, positive for purchases, with transaction cost

$$
C(h)=\sum_i\begin{cases}a_i h_i,&h_i\ge0,\\b_i h_i,&h_i<0,\end{cases}
$$

where $a_i$ and $b_i$ are ask and bid quotes. Negative terms represent cash received on sales. The physically meaningful optimization corresponding to the text is

$$
\max_h\left\{m^{(1)}(S,\sigma,0;h)
-\sqrt{v^{(1)}(S,\sigma,0;h)}-C(h)\right\}.
$$

State 1 means the barrier claim is alive; state 0 means it has knocked out while static vanillas remain. At the barrier, $m^{(1)}=m^{(0)}$ and $v^{(1)}=v^{(0)}$. The post-knock-out position does not generally have zero value or variance, because the static calls continue to expiry. Its terminal payoff is $\sum_i h_i(S-E_i)^+$; the alive state's terminal payoff subtracts $(S-100)^+$. Both terminal variances are zero. Solve the state-0 PDE first and use it to provide the alive state's barrier boundary.

Section 10.1(b) prints the post-knock-out mean equal to the terminal call-payoff sum at general time $t$. That cannot literally be the continuation value at every pre-expiry time. Interpreting it as the terminal condition at $T$, followed by PDE evolution, is the consistent reconstruction. It is a clarification of the boundary specification, not a quoted complete numerical algorithm.

There is also a material sign inconsistency in the displayed quantities. Using the printed quantity vector as actual holdings in the quote table gives

$$
C(h_{\rm printed})=-1.12217634,
$$

a net cash inflow, whereas the source reports a cost of \$1.1863. Reversing every quantity gives

$$
C(-h_{\rm printed})=1.18629844,
$$

which matches that reported cost. This arithmetic strongly suggests an opposite quantity convention, but the displayed positive payoff sum and the objective's subtraction of cost do not resolve the convention explicitly. A reproduction must test and document the sign convention; the note does not assert that reversing the table alone reproduces the reported PDE moments.

The reported post-hedge mean and variance are 0.0398 and 0.0522. Combining them with the **reported** cost gives

$$
1.1863-0.0398+\sqrt{0.0522}\approx1.374973,
$$

versus the printed value 1.3752. This smaller discrepancy concerns rounded moment inputs; it does not explain the quantity-sign problem. Residual variance falls by $1-0.0522/0.3290\approx84.13\%$. The reported alternative risk-neutral barrier value is 1.1256; the residual standard deviation is approximately 0.2285. These are different valuation constructions, so the gap is not an empirical arbitrage profit.

## Reconstructing the numerical method

The article gives governing equations but no PDE grid, time step, solver, optimization tolerance, boundary truncation, or convergence study. A concrete reconstruction should record the missing drift/rate and time-unit choices, solve the mean equations with a stable backward scheme, compute volatility derivatives consistently, and solve variance equations using the physical generator. Mesh refinement should be concentrated near the barrier and payoff kink. Negative variances or sensitivity to arbitrary volatility boundaries are numerical warnings.

A useful derived acceleration follows from linearity. Solve means for the barrier claim and each vanilla basis position, then form their linear combination for any candidate $h$. Residual variance is a quadratic form in those holdings. Its cross terms can be obtained from PDEs with source $q^2(1-\rho^2)m_{i,Z}m_{j,Z}$, or from paired linear combinations. Keeping the cross terms is essential: adding standalone variances would lose the benefit of hedging.

At the initial state this gives a mean affine in $h$ and a variance quadratic in $(1,h)$. If the covariance matrix is positive semidefinite and bid prices do not exceed asks, the standard-deviation penalty is convex and transaction cost is convex. The stated maximization then has a concave objective. This is an implementation interpretation of the source equations, not an optimization theorem supplied in the article. A finite optimum still requires checking for directions in which model-implied reward exceeds the risk penalty and trading cost without bound. The source does not report position bounds or an existence analysis.

A simulation check should use the same physical dynamics, evolve the live/knocked-out state, trade the stock according to the computed hedge, and include funding and static transaction costs with consistent signs. It should compare simulated discounted cash-flow moments with the PDE outputs before assessing tail probabilities. Finite rebalancing intervals, volatility filtering error, and stock transaction costs are useful extensions, but they change the idealized experiment. Their results must not be presented as quantities reported by this paper.

The transferable lesson is to make the residual risk of a hedged claim part of the valuation and static-hedge decision. The two moment equations provide a precise route to doing so. The limits are equally concrete: local hedge optimality, physical-dynamics uncertainty, observation of volatility, missing numerical conventions, the static-quantity sign ambiguity, and an unvalidated Gaussian interpretation of profitability. Addressing those points is necessary before using the worked example as a pricing or risk-control implementation.

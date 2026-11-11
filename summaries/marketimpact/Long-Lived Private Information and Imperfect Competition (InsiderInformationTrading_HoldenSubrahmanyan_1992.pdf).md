# Long-Lived Private Information and Imperfect Competition

Craig W. Holden and Avanidhar Subrahmanyam. *The Journal of Finance* 47(1), March 1992, 247–270. [Supplied PDF](../../Finance/InsiderInformationTrading_HoldenSubrahmanyan_1992.pdf), 25 pages including the archive cover. The entire article and Appendix were read; journal page 247 is PDF page 2. Equilibrium equations, numerical figures, limiting proofs, and the information-acquisition proposition were checked visually against the scanned source.

## Why this matters

A trader with exclusive information has an incentive to release it gradually through trades: revealing too much today destroys tomorrow's informational rent. Holden and Subrahmanyam show how sharply that conclusion changes when several traders possess the same information and compete. Each trader would prefer the others to wait, but each also wants to trade before the others reveal the information. Even two noncooperating informed traders can therefore cause prices to become informative very quickly.

The new contribution is the finite-horizon, sequential-auction equilibrium with multiple strategic informed traders, together with a tractable backward/forward numerical solution and limiting results. The benchmark is Kyle's monopolistic informed trader. The paper does not introduce heterogeneous noisy signals, successive news arrivals, risk-averse market makers, or inventory-constrained liquidity provision. Its strong information-revelation result depends on common exact information, risk neutrality, and noncooperative competition.

The practical distinction is between the lifetime of information and the lifetime of its trading value. The liquidation value is fixed and known throughout the trading horizon, yet the private advantage can be competed away early. The model also separates initially poor liquidity from subsequently deep trading: aggressive early information release increases adverse selection at the opening but leaves little hidden information later. Thus the presence of more informed competitors does not uniformly improve depth at every auction.

## Environment and information structure

One risky security is traded in $N$ auctions during calendar time $[0,1]$. Let $t_n$ be auction times and $\Delta t_n=t_n-t_{n-1}>0$. The terminal value is

$$
v\sim N(p_0,\Sigma_0),\qquad \Sigma_0>0.
$$

There are $M\ge1$ informed traders. Every one observes the same realization of $v$ before trading begins. Trader $i$ submits signed order $\Delta x_{in}$ at auction $n$, and total informed flow is $\Delta X_n=\sum_{i=1}^M\Delta x_{in}$. Orders are strategic because informed traders understand their impact on the execution price and the future information inferred from that price.

Noise flow is independent Gaussian demand with mean zero and variance proportional to the time interval:

$$
\Delta u_n\sim N(0,\sigma_u^2\Delta t_n),
\qquad \sigma_u^2>0.
$$

Noise orders are serially independent and provide camouflage for informed trading. Scaling their variance by $\Delta t_n$ is essential when comparing economies with different auction counts: the total noise variance over the fixed horizon remains $\sigma_u^2$. Keeping per-auction noise variance fixed while increasing $N$ would change the economy rather than merely refine its trading grid.

Competitive, risk-neutral market makers observe aggregate order flow $y_n=\Delta X_n+\Delta u_n$, not its decomposition. They execute at the conditional expected liquidation value:

$$
p_n=E[v\mid y_1,\ldots,y_n].
$$

An informed trader maximizes expected terminal trading profit from current and subsequent orders, conditional on the known $v$, observed past prices, and correct conjectures about the other informed traders' strategies. There are no position limits, capital constraints, funding charges, spreads added to the clearing price, fixed trading costs, or risk penalties. The paper's trading objective is informational profit, not mean–variance portfolio allocation.

All informed traders have the same information, but they do not collude. They cannot infer other traders' realized past orders perfectly from prices because unobserved noise demand also moves prices. The source discusses backward induction in this setting and rules out future rewards or punishments sustaining collusive behavior in the finite game. This is materially different from treating the group as one trader who internalizes the effect of every informed order on aggregate future profits.

## Linear equilibrium and dynamic optimization

Proposition 1 states a unique linear equilibrium. In a symmetric equilibrium, each informed trader uses the same coefficient $\beta_n$:

$$
\Delta x_{in}=\beta_n(v-p_{n-1})\Delta t_n,
\qquad
\Delta X_n=M\beta_n(v-p_{n-1})\Delta t_n.
$$

The price update and posterior error variance are

$$
p_n-p_{n-1}=\lambda_n y_n,
\qquad
\Sigma_n=\operatorname{Var}(v\mid y_1,\ldots,y_n).
$$

The impact coefficient $\lambda_n$ is the marginal price response to a unit of aggregate signed order flow. Its reciprocal is market depth in the model. It is not a quoted bid–ask spread or an empirical coefficient estimated from a trade database. $\Sigma_n$ measures remaining uncertainty about the common terminal value, rather than realized price volatility.

The expected future profit of an individual informed trader before auction $n$ has quadratic form

$$
E[\pi_{in}\mid v,p_1,\ldots,p_{n-1}]
=\alpha_{n-1}(v-p_{n-1})^2+\delta_{n-1}.
$$

To understand the recursion, suppose continuation profit after the current auction is $\alpha_n(v-p_n)^2+\delta_n$. The current trader chooses $z=\Delta x_{in}$ to maximize

$$
E\left[(v-p_n)z+\alpha_n(v-p_n)^2+\delta_n
\mid v,p_1,\ldots,p_{n-1}\right],
$$

holding the other traders' conjectured orders fixed when taking the best response. The trader internalizes both current price impact and the effect of today's revelation on future rent. Imposing symmetry after optimizing gives equation (19), and the public-information martingale property of prices eliminates an additional predictable drift term in the candidate pricing rule.

With $q_n=\alpha_n\lambda_n$ and $D_n=M(1-2q_n)+1$, the resulting first-order and continuation relations are

$$
\beta_n\Delta t_n=\frac{1-2q_n}{\lambda_nD_n},
\qquad
\alpha_{n-1}=\frac{1-q_n}{\lambda_nD_n^2},
$$

$$
\delta_{n-1}=\delta_n+\alpha_n\lambda_n^2\sigma_u^2\Delta t_n.
$$

The second-order condition is $\lambda_n(1-q_n)>0$. The economically relevant solution has positive impact and $0\le q_n<1/2$, so informed demand has the sign of $v-p_{n-1}$. At the last auction, $\alpha_N=\delta_N=0$ because no future trading opportunities remain. Then $\beta_N\Delta t_N=1/[\lambda_N(M+1)]$.

Normality makes the market maker's conditional expectation linear. The regression formulas in equations (20)–(21) give

$$
\lambda_n=
\frac{M\beta_n\Sigma_{n-1}}
{M^2\beta_n^2\Sigma_{n-1}\Delta t_n+\sigma_u^2},
$$

$$
\Sigma_n=
\frac{\sigma_u^2\Sigma_{n-1}}
{M^2\beta_n^2\Sigma_{n-1}\Delta t_n+\sigma_u^2}.
$$

Useful equivalent identities are $\lambda_n=M\beta_n\Sigma_n/\sigma_u^2$ and $\Sigma_n=(1-M\beta_n\lambda_n\Delta t_n)\Sigma_{n-1}$. These connect optimal demand, inference, and impact. A numerical solution should satisfy all of them, rather than rely on one isolated formula.

The proof constructs the equilibrium through backward induction and Gaussian updating. The article refers the uniqueness argument to the analogous proof in Kyle rather than reproducing it fully. Its proposition concerns the linear equilibrium class; it does not prove uniqueness over every nonlinear or path-dependent strategy space.

## The best-response calculation and a one-auction diagnostic

The strategic first-order condition can be reconstructed without treating informed flow as exogenous. Set $e=v-p_{n-1}$, $b=\beta_n\Delta t_n$, $q=\alpha_n\lambda_n$, and let one trader deviate to order $z$. The other $M-1$ traders submit $(M-1)be$. The residual value after execution is $e'=e-\lambda_n[z+(M-1)be+\Delta u_n]$. Up to constants independent of $z$, expected current-plus-continuation profit is

$$
z\{[1-\lambda_n(M-1)b]e-\lambda_n z\}
+\alpha_n\{[1-\lambda_n(M-1)b]e-\lambda_n z\}^2.
$$

Noise adds the constant $\alpha_n\lambda_n^2\sigma_u^2\Delta t_n$. Differentiating the remaining expression gives

$$
(1-2q)[1-\lambda_n(M-1)b]e
-2\lambda_n(1-q)z=0.
$$

Only after obtaining that best response should symmetry be imposed by setting $z=be$. Rearrangement yields

$$
\lambda_n b\{(M-1)(1-2q)+2(1-q)\}=1-2q.
$$

The bracket equals $M(1-2q)+1$, recovering the equilibrium expression for $b$. This ordering of optimization and symmetry matters: differentiating as though every competitor changed its order when the focal trader deviated would internalize the entire group's price impact and solve a different strategic problem. The curvature is $-2\lambda_n(1-q)$, giving the stated second-order condition. The calculation also shows why the noise-generated continuation constant survives in expected profit even though noise demand has zero mean.

A useful closed-form diagnostic is a single auction with interval length $\Delta t$. There is no continuation value, so $q=0$ and the consistent formulas reduce to

$$
\Sigma_1=\frac{\Sigma_0}{M+1},\qquad
\lambda_1=\frac{\sqrt{M\Sigma_0}}{(M+1)\sigma_u\sqrt{\Delta t}},\qquad
\beta_1=\frac{\sigma_u}{\sqrt{M\Sigma_0\Delta t}}.
$$

These expressions provide a particularly simple way to expose the factor-of-$M$ inconsistency discussed below. They satisfy Gaussian regression, the informed best response, and positive demand for positive mispricing simultaneously. With one informed trader they return the familiar equal split of original uncertainty after one auction, $\Sigma_1=\Sigma_0/2$. With more traders a larger fraction is revealed in that auction, but a finite $M$ still leaves strictly positive error variance.

An additional algebraic implication, not a separate numerical result reported by the authors, is that one informed trader's ex ante gross profit in this one-auction economy is

$$
E[\pi_i]=\beta_1\Delta t\,\Sigma_1
=\frac{\sigma_u\sqrt{\Delta t}\sqrt{\Sigma_0}}{\sqrt M(M+1)}.
$$

To derive it, condition on $e$, note that expected residual mispricing is $e/(M+1)$, multiply by that trader's order $\beta_1\Delta t e$, and average $e^2=\Sigma_0$. Total informed profit is $M$ times this expression, or $\sigma_u\sqrt{\Delta t}\sqrt{\Sigma_0}\sqrt M/(M+1)$. It falls toward zero as the number of informed competitors grows, despite the divergence of their total conditional order magnitude. Competition can therefore dissipate aggregate informational rent while increasing the gross amount they try to trade. Large quantity and large aggregate profit are not interchangeable in the perfect-competition limit.

The market makers' conditional-pricing rule also supplies a profit-accounting check. Aggregate order $y$ is observable when the price is set, so $E[(v-p)y]=0$. Summed trading profits of informed and noise traders therefore have zero expectation under the model; positive informed expected profit is offset by noise-trader expected losses, while competitive market makers earn zero expected profit. This is an accounting implication of the specified terminal-value payoff and information sets, not a welfare analysis. Noise trading is exogenous, and the paper does not model the consumption, hedging, or liquidity motives that might make it beneficial for those traders despite their adverse-selection loss.

## A reproducible numerical solution

Proposition 2 transforms the coupled recursions into a scalar backward problem followed by a forward variance calculation. Start with $q_N=0$. For $n=N,N-1,\ldots,2$, define

$$
k_n=\frac{(1-q_n)^2}
{(1-2q_n)[M(1-2q_n)+1]^2},
\qquad d_n=\frac{\Delta t_{n-1}}{\Delta t_n}.
$$

Then choose the unique economically admissible root $q_{n-1}\in(0,1/2)$ of

$$
2Md_nq_{n-1}^3-(M+1)d_nq_{n-1}^2
-2k_nq_{n-1}+k_n=0.
$$

A bracketed scalar root solver is sufficient. Selecting an arbitrary root returned by a polynomial routine is unsafe because the economic restriction is part of the solution. At zero the polynomial is positive; at one half it is negative. The Appendix establishes the relevant root's uniqueness and derives the cubic by combining two expressions for the ratio of successive price-impact coefficients.

After the backward pass, start at the exogenous $\Sigma_0$ and move forward for $n=1,\ldots,N$:

$$
\Sigma_n=\frac{\Sigma_{n-1}}{D_n},
\qquad
\lambda_n=
\sqrt{\frac{M\Sigma_n(1-2q_n)}
{\Delta t_n\sigma_u^2D_n}}.
$$

Recover trading intensity using the equilibrium identity

$$
\beta_n=\frac{\lambda_n\sigma_u^2}{M\Sigma_n}
=\sqrt{\frac{(1-2q_n)\sigma_u^2}
{M\Sigma_n\Delta t_nD_n}}.
$$

Finally obtain $\alpha_{n-1}$ and $\delta_{n-1}$ from the continuation recursions, starting with the terminal conditions. This procedure works for the unequal positive auction intervals allowed in Proposition 2. The numerical figures and asymptotic propositions specialize to equally spaced auctions.

There is a material printed inconsistency in equation (26). The scanned page gives $\beta_n$ with $M(1-2q_n)\sigma_u^2$ in the numerator and $\Sigma_n\Delta t_nM D_n$ in the denominator. Those two factors of $M$ cancel, leaving a coefficient $\sqrt M$ larger than the expression implied by equations (6), (7), and (25). The formula above is a **derived reconciliation using those equilibrium identities**, not a literal transcription of equation (26). The Appendix's later substitution $\beta_1=\lambda_1\sigma_u^2/(M\Sigma_1)$ also supports the reconciled expression. The source alone does not establish what formula the authors' numerical code used.

For numerical stability, very small posterior variances can be accumulated in logs. The recursion is deterministic; it does not require Monte Carlo to produce the paper's curves. Prices and profits can subsequently be simulated by drawing $v$ and independent noise increments, but that is a separate exercise from the reported numerical equilibrium comparisons. Neither random seeds nor simulation standard errors are relevant to a direct solution of the displayed system.

The recursion also isolates which inputs affect the shape of the result. The dimensionless sequence $q_n$ depends only on the informed-trader count and ratios of auction intervals. It does not depend on the overall price-uncertainty scale or noise-flow scale. Consequently, for a fixed grid and $M$, multiplying the initial standard deviation of value by $a>0$ and the noise-flow standard deviation by $b>0$ multiplies every posterior variance by $a^2$, every impact coefficient by $a/b$, and every trading-intensity coefficient by $b/a$. If the conditional initial mispricing is scaled by $a$ as well, expected order quantities scale by $b$. Expected profits scale by $ab$.

These are derived homogeneity checks on the equilibrium system. They explain why the normalized figures can represent a family of differently sized theoretical markets without re-solving the scalar backward problem. They also show what normalization cannot establish: the speed of information decay as a fraction of initial uncertainty is unchanged by those two scales, whereas currency profits and absolute market depth are not. In a calibrated use, the researcher would still need a value-uncertainty estimate and a noise-demand estimate with compatible units. A return variance alone is not automatically the variance of the terminal fundamental value, and total observed volume is not automatically noise-flow variance. The article does not provide estimators for those objects.

## Numerical design and magnitude of the effect

The paper sets $\Sigma_0=1$, $\sigma_u^2=1$, and $\Delta t_n=1/N$ in every numerical example. Figures 1–3 keep $M=2$ and compare $N=4,20,100$. Figures 4–6 keep $N=20$ and compare $M=1,2,4,20$. The quantity figures additionally condition on $v=21$ and $p_0=20$, so the initial mispricing is one unit. These are normalized theoretical economies, not fits to securities, trading days, or observed informed-trader counts.

The paper emphasizes that with two informed traders and 100 auctions, less than 5% of the original uncertainty remains after the fifth auction. With 20 auctions, its text describes the fifth-auction error variance as approximately 0.05 for $M=2$, versus approximately 0.8 for a monopolist. The difference is economically large despite a very small change in the number of competitors.

An independent calculation of the stated cubic and consistent equilibrium identities gives the following diagnostic values. They are newly computed checks, not numbers transcribed from an author table:

| Informed traders $M$ | Auctions $N$ | First-auction impact $\lambda_1$ | Fifth-auction variance $\Sigma_5$ |
|---:|---:|---:|---:|
| 1 | 20 | 0.91519 | 0.78004 |
| 2 | 20 | 2.23194 | 0.04195 |
| 4 | 20 | 1.91177 | 0.000807 |
| 20 | 20 | 0.96165 | $2.71\times10^{-7}$ |
| 2 | 100 | 4.99077 | 0.04196 |

These values recover the figures' main patterns. The impact coefficient at the first auction is not monotonic in the number of informed traders across this grid. Two traders generate greater initial adverse selection than one, while many competitors force rapid revelation and eventually reduce the marginal informational content of additional flow. Later in the horizon, impact becomes very small with multiple informed traders.

The fifth-auction variances for two traders are nearly identical for $N=20$ and $N=100$, but they occur at very different calendar times: 0.25 and 0.05. This is exactly why auction index and clock time must not be confused. More frequent auctions accelerate revelation in calendar time even if a given small number of early auctions removes a similar fraction of uncertainty.

For reconstructing Figures 3 and 6, the conditional expected residual mispricing is

$$
E[v-p_{n-1}\mid v]
=\frac{\Sigma_{n-1}}{\Sigma_0}(v-p_0),
$$

so total expected informed order is

$$
E[\Delta X_n\mid v]
=M\beta_n\Delta t_n
\frac{\Sigma_{n-1}}{\Sigma_0}(v-p_0).
$$

Using the figure calibration, first-auction expected total order is approximately 0.49948 for $M=2,N=4$, 0.21042 for $M=2,N=20$, and 0.09410 for $M=2,N=100$. The increasing trading intensity does not imply increasing quantity per auction: each auction spans less time and contains less noise flow. In contrast, holding $N=20$ fixed while increasing $M$ raises first-auction total expected informed flow across the displayed cases.

No confidence intervals accompany these comparative statics because they are model outputs. The paper includes no real-data estimate, statistical test, transaction-cost-adjusted strategy return, calibration window, or out-of-sample experiment. Analyst coverage is mentioned as a possible indirect proxy for the number of informed traders, but it is not used to estimate $M$ or test the model.

## Three distinct limits

Proposition 3 assumes equally spaced auctions. Its first limit holds $M\ge2$ fixed and sends $N$ to infinity over the unchanged interval $[0,1]$. For any fixed calendar time $\tau>0$, let $n'=\lfloor\tau N\rfloor$ denote the most recent auction. Then

$$
\Sigma_{n'}\longrightarrow0,
\qquad
\lambda_{n'}\longrightarrow0.
$$

Thus at every strictly positive time the limiting price is fully informative and depth becomes unbounded. This is the source's precise sense of almost immediate revelation. It is not a statement that the first finite auction always reveals everything.

The second limit examines that first auction while increasing $N$:

$$
\lambda_1\longrightarrow\infty,
\qquad
E[\Delta X_1\mid v]\longrightarrow0,
\qquad
\beta_1\longrightarrow\infty.
$$

Initial depth therefore tends to zero, whereas depth at any fixed positive calendar time tends to infinity. There is no contradiction: a shrinking initial boundary layer has intense adverse selection. In that layer informed traders submit smaller absolute orders into even smaller noise demand while trading at a rising rate per unit time.

The third limit keeps the number of auctions fixed and increases $M$. At the first auction, $\Sigma_1\to0$, $\lambda_1\to0$, and $p_1\to v$. The magnitude of total conditional informed order diverges for nonzero initial mispricing. The printed proposition writes $E[\Delta X_1\mid v]\to\infty$ without a sign qualification; for $v<p_0$ the signed order instead tends toward negative infinity, and for $v=p_0$ its conditional expectation is zero. The positive statement matches the figures' assumption $v-p_0=1$.

This perfect-competition limit is not a realistic forecast of unlimited turnover. It follows from unlimited risk-neutral orders and unbounded capacity within the model. Its purpose is to show the direction of information revelation as competition increases.

## How the Appendix proves rapid revelation

The proof tracks $q_n^N=\alpha_n\lambda_n$ as auction count changes. Under equal spacing, the backward recursion depends on the number of auctions remaining, not the physical interval length. Consequently coefficients at the same distance from the terminal auction coincide across different horizons. The Appendix establishes monotonicity and boundedness of the backward sequence, then shows that fixed-auction-index coefficients converge to a common limit $q$.

The limiting value satisfies equation (39):

$$
(1-2q)\left[
4M^3q^4-2M^2(2M+3)q^3
+M(M^2+3M+3)q^2-1
\right]=0.
$$

For a monopolist the relevant limiting value is $q=1/2$. For $M=2$, the relevant root is approximately 0.27862654; for larger $M$ it is smaller and positive. That strict separation from one half is the mathematical source of the sharp economic contrast.

Since $\Sigma_n/\Sigma_{n-1}=1/[M(1-2q_n)+1]$, the competitive case has a uniform per-auction contraction bounded away from one. For $M=2$ the limiting bound is about 0.530365, and the proof uses the looser common bound $2/3$ for $M\ge2$. Applying the contraction through $\lfloor\tau N\rfloor$ auctions makes remaining uncertainty decay geometrically. A factor growing only like $\sqrt N$ in the impact expression cannot offset that decay, yielding the positive-time impact limit.

The scanned proof replaces the floor index by $\tau N$ inside one geometric upper bound with the inequality in the wrong direction: for a base below one, $a^{\lfloor\tau N\rfloor}\ge a^{\tau N}$. Keeping the floor, or using $\lfloor\tau N\rfloor\ge\tau N-1$, gives the same zero limit correctly. This is a local bound-writing issue, not a change in the limiting mechanism. Likewise, a sentence in the conclusion says the interval between auctions becomes “large,” although the propositions, proof, and preceding discussion concern intervals becoming small.

## Continuous-time equilibrium and information acquisition

The limit of finite-auction equilibria does not automatically define an equilibrium in a continuous-time strategy space. Section II.C explicitly presents informal arguments against continuous linear trading strategies under the maintained multiple-insider structure: instantaneous revelation and unbounded initial trading intensity leave no ordinary first-instant optimum. It then discusses discrete initial orders, which have no contemporaneous noise camouflage and would reveal information immediately. With risk-neutral agents, no risk-sharing motive, and an unbounded normal value distribution, the authors argue that a discrete-strategy equilibrium also fails.

The source explicitly stops short of a general nonexistence theorem, particularly for nonlinear equilibria. A note or implementation should preserve that distinction. The well-defined result is the sequence of finite-auction linear equilibria and its limits; the broader continuous-time claim is a reasoned discussion.

Section II.D lets becoming informed cost $C>0$. An individual trader's ex ante gross profit with $M$ informed traders is

$$
\Pi(M)=\alpha_0(M)\Sigma_0+\delta_0(M).
$$

Proposition 4 writes $\Pi(M^*)=C$ while requiring $M^*$ to be a nonnegative integer. Exact equality generally need not hold for an arbitrary cost when entry is discrete. The usual entry interpretation is that incumbent profit covers the cost while one additional entrant would not: $\Pi(M^*)\ge C$ and $\Pi(M^*+1)\le C$, with a separate no-entry case. These inequalities are an explicit interpretation of the economic argument, not the printed proposition. The article supplies no cost calibration, integer search results, or empirical information-acquisition estimates.

The endogenous-entry section also exposes a limit of the fixed-$M$ comparison. Rapid erosion of informational rents can discourage acquiring information in the first place. One cannot conclude from the two-insider trading equilibrium alone that any market will sustain two perfectly informed agents at a positive information cost.

## Scope of the economic conclusion

The model suggests a concentration of informational trading near the opening if common long-lived information arrives while markets are closed. It also gives a reason for adverse selection to decline after that information is revealed. These are proposed interpretations of intraday patterns, not tests performed in this paper. There is no fresh news later in the model; adding repeated information shocks, heterogeneous signal quality, risk aversion, inventory limits, or collusion could change both the speed and location of price discovery.

The source's claims about tightness, depth, and resiliency refer to this idealized auction market. Almost full information revelation removes the modeled adverse-selection friction, but it does not remove real-world matching delays, operational costs, funding constraints, or order-book discreteness. The central result is precise within its domain: even a small number of strategic traders with the same exact information can dissipate its private value far faster than an informed monopolist. The explicit recursion makes that result reproducible, provided the printed trading-intensity inconsistency is reconciled openly and the singular limits are kept separate from claims about continuous-time equilibrium existence.

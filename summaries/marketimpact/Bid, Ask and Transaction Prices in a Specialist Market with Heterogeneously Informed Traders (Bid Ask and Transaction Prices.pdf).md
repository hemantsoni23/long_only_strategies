# Bid, Ask and Transaction Prices in a Specialist Market with Heterogeneously Informed Traders

Lawrence R. Glosten and Paul R. Milgrom, 1985, *Journal of Financial Economics* 14, pp. 71–100. [Local source PDF](<../../Finance/Bid Ask and Transaction Prices.pdf>). The supplied copy is a 30-page Columbia Business School scan of the article, with its own page numbers 1–30. It records receipt in August 1983 and a final version in September 1984. References below use those PDF page numbers. The complete source, including the proof appendix on pages 28–29 and references on pages 29–30, was read visually; extracted text contains mainly the added institutional branding.

## Why this matters

A positive bid–ask spread can arise even when a dealer is risk neutral, has no processing or inventory cost, and earns zero expected profit on every trade. Buying and selling are informative decisions. A dealer selling to a customer must value the security conditional on that customer's willingness to buy, and a dealer buying must condition on the willingness to sell. Those conditional values differ when some customers know more than the dealer.

The paper goes beyond that static explanation. It shows how transactions reveal information, how a spread can coexist with martingale transaction prices, why the history of trade changes future spreads, and how sufficiently elastic uninformed demand can lead to a market shutdown. It also distinguishes returns measured from transaction prices from returns available to an investor who must buy at an ask and sell at a bid.

For a quant, this is a foundational model for permanent price impact, order-flow inference, and execution-cost measurement. Its greatest practical value is a set of conditional-pricing identities and explicit assumptions. It is not a calibrated execution algorithm, a claim that all spreads reflect information, or evidence that inventory constraints are negligible in real markets. The general theoretical statements and the transparent two-value example also need to be distinguished: some strong learning claims require more identifying structure than balanced order flow alone supplies.

## Trading protocol, preferences, and information

The basic model on pages 6–10 is a sequential dealership market. The specialist posts a bid $B_t$ and ask $A_t$ for one unit. An investor arrives anonymously, observes the quotes, and buys one unit, sells one unit, or leaves. The specialist can revise quotes after this decision and before the next arrival. All active orders are market orders. Limit-order submission, queue position, and strategic choice of order size are outside the model.

At a future informational date $T_0$, uncertainty about the relevant security value is resolved. Let $V\geq0$ have finite variance. There is initially no discounting. The dealer is risk neutral, has unlimited access to cash and securities, and faces zero holding and transaction costs. Competition is represented by a zero-expected-profit condition on each side of each transaction; a full strategic competition game is not solved. Free entry by itself would not generally imply that stronger per-transaction condition, a distinction the conclusion acknowledges.

Investor utility from stock quantity $x$ and current consumption $c$ is $\rho xV+c$. The personal parameter $\rho$ captures liquidity or time-preference motives. A high value makes future ownership attractive; a low value favors current consumption. The specialist's parameter is normalized to one. Investor parameters are independent of the payoff and information about it, and independent across traders; informed and uninformed traders may have different distributions. Noninformational preference heterogeneity is what allows mutually beneficial trade despite common probabilistic beliefs and risk neutrality.

Let $H_t$ denote public information, $S_t$ the specialist's information, and $F_t$ the arriving trader's information after seeing quotes. An informed trader additionally observes a private signal; an uninformed trader observes public information and quotes. The trader's reservation value is

$$
Z_t=\rho_t\mathbb E[V\mid F_t].
$$

The optimal one-unit decision is to buy if $Z_t>A_t$, sell if $Z_t<B_t$, and otherwise abstain. The paper uses strict inequalities and does not develop an economically consequential tie-breaking rule. An implementation with discrete preferences or payoff states must specify ties explicitly.

Arrivals occur one at a time. Their probability law can depend on the trading history and information, and the dealer knows that law. The general model does not require a constant Poisson intensity, independent trade signs, or a fixed informed fraction. An informed investor can submit multiple unit orders, but the paper does not solve a strategic dynamic concealment problem for a monopolistic insider. Correct Bayesian inference by the specialist is assumed.

## Competitive quotes are conditional expectations

For posted quotes, the expected dealer profit from an arrival is

$$
\mathbb E[(A_t-V)\mathbf1_{\{Z_t>A_t\}}+(V-B_t)\mathbf1_{\{Z_t<B_t\}}\mid S_t].
$$

The side-specific break-even conditions are

$$
A_t=\mathbb E[V\mid S_t,Z_t>A_t],
\qquad
B_t=\mathbb E[V\mid S_t,Z_t<B_t].
$$

These are fixed-point equations: changing the quote changes the set of customers willing to trade. Conditioning only on the pretrade public mean would miss the adverse-selection cost. Where the specialist has only public information, the paper selects the lowest ask with nonnegative expected selling profit and the highest bid with nonnegative expected buying profit. This selection matters when a nonlinear equation has multiple roots. At zero-probability trade events, a conditional expectation is not a usable numerical formula; shutdown must be handled as a boundary outcome.

Proposition 1 puts the quotes on opposite sides of the common-information expectation $m_t$: $B_t\leq m_t\leq A_t$. The proof uses the fact that buying selects the upper tail of the trader's valuation, together with the preference-independence conditions. Strict separation requires economically informative selection into the relevant trade side. Merely labeling a trader informed does not ensure that her private information affects her action when a strong liquidity motive dominates it.

A quote is therefore a contingent posterior. Before the next trade, the ask states the dealer's valuation if the next customer buys; the bid states the valuation if that customer sells. There is no inconsistency in the eventual transaction price reflecting information the dealer lacked before the order arrived. The order itself supplies that information.

Let $T_k$ be the time of the $k$th completed trade and $S_k$ the dealer's information just after it. In the zero-cost model,

$$
p_k=\mathbb E[V\mid S_k].
$$

The tower property gives $\mathbb E[p_{k+1}\mid S_k]=p_k$. Because the transaction price is public, the price sequence is also a martingale relative to the public post-trade information filtration. Finite payoff variance makes its increments square integrable and uncorrelated across nonoverlapping trade intervals. This is Proposition 2, pages 11–13.

The result directly warns against interpreting every alternation between bid and ask as mechanical bid–ask bounce. With purely informational spreads, the efficient conditional value moves with the trade. A buy occurs at a higher price because it raises the posterior value; the next sell need not return to the old bid. The result does not say that transaction returns in a market with processing costs, inventory pressure, stale quotes, or price discreteness are uncorrelated.

## Separating information from a per-trade processing cost

Pages 13–14 add a fixed dealer cost $c$ per transaction. Quotes become conditional values plus or minus $c$, and transaction prices satisfy $p_k=m_k+cQ_k$, where $Q_k=+1$ when the customer buys and $-1$ when the customer sells. Under the source's additional symmetric-direction and public-information assumptions, let $\Psi$ be the difference between the two conditional values. The total spread is $\Psi+2c$.

The adjacent price-change covariance and variance are

$$
\operatorname{Cov}(\Delta p_k,\Delta p_{k+1})=-\frac{c\Psi}{2}-c^2,
$$

$$
\operatorname{Var}(\Delta p_k)=\theta^2+\frac{\Psi^2}{4}+c\Psi+2c^2,
$$

where $\theta^2$ is the variance of public-information innovations between trades. Define the processing-cost fraction $\beta=2c/(\Psi+2c)$ and $\delta=1+[2\theta/(\Psi+2c)]^2$. Their first-order correlation is

$$
R=-\frac{\beta}{\delta+\beta^2}.
$$

When $c=0$, correlation is zero despite a positive informational spread. When information risk vanishes and there is no intervening public news, the familiar pure-cost result is $R=-1/2$. For admissible $R<0$, the economically relevant inverse is

$$
\beta=\frac{-1+\sqrt{1-4\delta R^2}}{2R}.
$$

This is not a standalone estimator of the adverse-selection share: $\delta$ is unknown, and the symmetric flow assumptions may fail. The source explicitly notes this identification obstacle. Independent arithmetic checks of the covariance, variance, and correlation identities agree for several cost/information combinations. They validate the algebra, not the model's empirical applicability.

## Spread–volume bounds, learning, and their scope

Returning to zero processing costs, Proposition 3 considers the quotes immediately before each trade. Write $s_k=A_k-B_k$ and $\bar s_N=N^{-1}\sum_{k=1}^Ns_k$. The paper defines $1/\gamma_k$ as the product of the pretrade buy and sell probabilities and $\gamma^*=(N+1)^{-1}\sum_{k=1}^{N+1}\gamma_k$, using a terminal convention when the extra trade does not occur. Its bound is

$$
\mathbb E\left[\frac{N}{N+1}\frac{N\bar s_N^2}{\gamma^*}\right]\leq\operatorname{Var}(V).
$$

If $\gamma^*\leq\gamma$ almost surely and $N\geq1$, this yields

$$
\mathbb E[N\bar s_N^2]\leq2\gamma\operatorname{Var}(V).
$$

Balanced positive probabilities on both sides prevent $\gamma$ from exploding. The result is an expectation bound on squared average spread times trade count, not an exact inverse-square-root regression law and not a pointwise forecast for every path. It concerns learning about a fixed finite-variance payoff; continual introduction of new private information can replenish uncertainty and is not captured by applying the bound indefinitely to an unchanged initial variance.

The proof uses the martingale variance budget: the expected sum of squared price innovations cannot exceed $\operatorname{Var}(V)$. Conditional innovation variance is bounded below by $s_k^2/\gamma_k$, and Cauchy–Schwarz connects individual spreads to their average. The scan's page 16 intermediate line prints $\sum_k\sqrt{e_k\gamma_k}\geq\sum_ks_k^2$. From the preceding $e_k\geq s_k^2/\gamma_k$, the correct immediate step is $\sqrt{e_k\gamma_k}\geq s_k$, without squaring the right side. This derived typographical repair has the correct units and leads to the displayed final bound; it is not an official erratum.

Proposition 4 states that the specialist's and arriving traders' payoff expectations converge in probability when trading remains balanced. This should not be used as a general theorem for arbitrary preference distributions allowed earlier in the paper. Balanced order directions need not identify private information. A counterexample, constructed here, makes the limitation explicit. Let $V$ equal 1 or 2 with equal prior probabilities; let a positive fraction of arrivals know $V$ exactly; and independently let every arrival have $\rho=1/4$ or $4$, equally likely. Set $A=B=1.5$. Every low-$\rho$ trader sells and every high-$\rho$ trader buys, regardless of the payoff. Both directions have probability one-half in both states, the dealer breaks even on each side, and no transaction reveals the state. An informed trader's payoff expectation remains 1 or 2 while the dealer's remains 1.5.

This example satisfies balanced flow and the basic preference independence conditions, but private information never changes the trade decision. It shows why a learning application needs an additional assumption ensuring that informed beliefs affect action probabilities. It does not undermine the source's explicit binary example below, where informed traders have $\rho=1$ and their actions identify the state statistically. The proof's broad convergence conclusion should be kept separate from that verified special case.

The inventory corollary additionally relies on the normalization that the preference distribution has equal probability mass above and below one. Even when learning holds, vanishing inventory drift is not bounded inventory, and the model supplies no capital constraint or risk penalty preventing large holdings along a path.

## Comparative statics are conditional on the same history

For Proposition 5, pages 19–21 explicitly specialize to informed traders with $\rho=1$ and a dealer possessing only public information. Let $G$ be the uninformed preference distribution, with density $g$, and let $m=\mathbb E[V\mid H]$. Uninformed demand at ask $A$ is $1-G(A/m)$ and supply at bid $B$ is $G(B/m)$. Their positive elasticity magnitudes are

$$
e_D=\frac{Ag(A/m)}{m[1-G(A/m)]},
\qquad
e_S=\frac{Bg(B/m)}{mG(B/m)}.
$$

Holding the current information and trading history fixed, more precise insider information, a larger informed-to-uninformed arrival ratio, or more elastic uninformed supply and demand widens the spread. Informed customers impose expected losses; less elastic liquidity demand lets the dealer recover those losses from a smaller change in quote. The proof compares expected side-specific profits and uses a conditional-expectation refinement argument for better information.

The qualification about fixed history is central. Raising the informed fraction initially widens spreads but can accelerate learning, leaving smaller spreads later. Proposition 5 therefore does not imply that a market with more informed participation has a larger time-average spread over every horizon. Nor does the spread–volume bound imply that unexpectedly high volume must narrow today's spread. If high volume signals a higher informed-arrival probability, current spreads can rise. The two statements condition on different information.

With completely inelastic uninformed buy and sell demands, sufficiently wide quotes can compensate the dealer without extinguishing liquidity trade. With elastic demand, raising the ask may drive away the uninformed buyers needed to subsidize losses to informed buyers. No active break-even ask may remain. If neither side trades and no external news arrives, the missing trades also prevent information revelation, so the shutdown can persist. This is an informational externality argument, not a quantified welfare theorem or a policy prescription establishing an optimal exchange design.

## The two-value example: a fully implementable benchmark

Section 3 uses $V_L=1$ and $V_H=11$, with current probability $\pi$ of the high value and public expectation $m=1+10\pi$. A fraction $\alpha$ of arrivals is perfectly informed and has $\rho=1$. Arrivals' informed status is independent of the payoff realization. No exogenous public information arrives during trading. The remaining arrivals are liquidity traders.

First take perfectly inelastic liquidity demand: an uninformed arrival buys or sells with equal probability, represented in the paper by limiting preferences 0 and infinity. For $0<\alpha<1$ and $0<\pi<1$, the break-even equations are

$$
\alpha\pi(11-A)=\frac{1-\alpha}{2}(A-m),
$$

$$
\alpha(1-\pi)(B-1)=\frac{1-\alpha}{2}(m-B).
$$

Solving gives

$$
A=\frac{11\alpha\pi+\frac{1-\alpha}{2}m}{\alpha\pi+\frac{1-\alpha}{2}},
\qquad
B=\frac{\alpha(1-\pi)+\frac{1-\alpha}{2}m}{\alpha(1-\pi)+\frac{1-\alpha}{2}}.
$$

The unconditional probability of a buy is $p_+=\alpha\pi+(1-\alpha)/2$. Bayes updating after a buy or sell yields

$$
\pi^+=\frac{\pi(1+\alpha)}{1-\alpha+2\alpha\pi},
\qquad
\pi^-=\frac{\pi(1-\alpha)}{1+\alpha-2\alpha\pi}.
$$

The posterior price identities are $A=1+10\pi^+$ and $B=1+10\pi^-$. Also $p_+A+(1-p_+)B=m$, directly verifying the martingale property at each state. At $\pi=1/2$, the quotes reduce to $A=6+5\alpha$ and $B=6-5\alpha$. Independently calculated examples give bids/asks 5.5/6.5 for $\alpha=0.1$, and 5/7 for $\alpha=0.2$. The spread doubles from one to two payoff units, while the public mean stays six. These are model calculations, not observed dollar spreads or source calibration estimates.

A minimal simulation draws the payoff once per path, then draws each arrival's informed status. An informed arrival buys in the high state and sells in the low state; an uninformed arrival uses a fair coin. Calculate quotes from the pretrade posterior, execute at the relevant quote, update the posterior, and carry it into the next arrival. Record dealer inventory as minus the cumulative customer direction, dealer cash with the opposite sign, spreads, posterior entropy, and transaction prices. Do not redraw the terminal payoff on every trade: that would replace learning about one value with a different model.

For a unit sold by the dealer, record terminal profit $A-V$; for a unit bought, $V-B$. Conditional expected profits should vanish, even though informed trades lose money and uninformed trades compensate for those losses. Numerical checks over several $(\alpha,\pi)$ combinations reproduce the posterior-price and martingale identities to floating-point precision. Such state-by-state identities are more informative implementation checks than a noisy Monte Carlo average alone.

## Information speed and a printed first-passage formula

In the inelastic example, log posterior odds change by a constant amount:

$$
\ell_k=\log\frac{\pi_k}{1-\pi_k},
\qquad
\ell_{k+1}=\ell_k+Q_{k+1}\kappa,
\qquad
\kappa=\log\frac{1+\alpha}{1-\alpha}.
$$

Conditional on the high state, $\mathbb E[Q]=\alpha$; conditional on the low state, it is $-\alpha$. Thus the log-odds random walk drifts toward the true state, and the posterior converges correctly with indefinitely many informative trades. For small $\alpha$, $\kappa\approx2\alpha$, so the information drift is approximately $2\alpha^2$. The characteristic learning time therefore scales as $1/\alpha^2$, while the initial spread is approximately linear in $\alpha$.

The source defines near-revelation by posterior odds exceeding a chosen threshold $\Omega$ in the true high state or falling below $1/\Omega$ in the true low state. This is a stopping criterion conditional on the true state, not an observer's first exit through either boundary. Let $L=\log\Omega$ and $\ell_0=\log[\pi_0/(1-\pi_0)]$, initially between the boundaries. Ignoring lattice overshoot, the conditional mean times are $(L-\ell_0)/(\alpha\kappa)$ in the high state and $(L+\ell_0)/(\alpha\kappa)$ in the low state. Weighting by the prior gives

$$
\mathbb E[T]\approx\frac{L+(1-2\pi_0)\ell_0}{\alpha\kappa}.
$$

Printed equation (12), page 23, instead uses $(1-\pi_0)\ell_0$. The coefficient $1-2\pi_0$ above follows directly from prior-weighting the two conditional first-passage expressions and is a derived repair, not an official erratum. At $\pi_0=1/2$ both formulas agree because $\ell_0=0$, which can conceal the discrepancy in symmetric examples.

For a concrete independent check, take $\alpha=0.2$, $\pi_0=0.2$, and $\Omega=100$. The printed expression is 43.1126 trades, while the corrected continuous-boundary expression is 46.5317. The required integer displacements are 15 steps upward in the high state and 8 downward in the low state. The exact lattice mean for reaching the corresponding correct boundary is $(0.2\times15+0.8\times8)/0.2=47$ trades. This difference is not explained solely by rounding the boundary. An implementation stopping at the first exit through either boundary must instead solve a two-boundary hitting-time problem and allow wrong-boundary exits.

The paper argues that raising a small informed fraction from 0.1 to 0.2 roughly doubles initial spreads but quarters learning time. Over a sufficiently long fixed trading horizon, faster learning can more than offset the higher initial spread in the average. That is a special-case dynamic comparison, not a universal relationship between informed participation and total execution costs.

## Elastic liquidity demand and one-sided shutdown

The second example takes uninformed preferences uniformly distributed on $(0,2)$. Their probability of buying is $1-A/(2m)$ when $A\leq2m$, and selling probability is $B/(2m)$ within the relevant range. Break-even conditions become

$$
\alpha\pi(11-A)=(1-\alpha)\left(1-\frac{A}{2m}\right)(A-m),
$$

$$
\alpha(1-\pi)(B-1)=(1-\alpha)\frac{B}{2m}(m-B).
$$

Choose the lowest feasible ask root and highest feasible bid root. The ask polynomial is

$$
(1-\alpha)A^2-[3m(1-\alpha)+2m\alpha\pi]A
+2m[(1-\alpha)m+11\alpha\pi]=0.
$$

The bid polynomial is

$$
(1-\alpha)B^2+[2m\alpha(1-\pi)-(1-\alpha)m]B
-2m\alpha(1-\pi)=0.
$$

A real algebraic root is insufficient: verify its location, the probability bounds, and the assumed informed trading decisions. A negative ask discriminant or absence of a feasible active root means the buy side cannot operate at a competitive break-even quote under that state. A no-trade quote can then exclude buyers, while the sell side may remain active. Abstention and the surviving trade direction must still enter Bayesian updating; do not treat one-sided shutdown as permanent absence of all information.

Page 24 states that the example has no active ask when $\alpha=0.3$, but that statement is not true for every prior. Independently solving the printed equations illustrates the required conditioning. At $\pi=0.1$, $m=2$, the ask discriminant is −0.7136 and the active ask is absent; the bid is approximately 1.491545. At $\pi=0.5$, $m=6$, the ask discriminant is 10.8, the feasible ask is approximately 7.938332, and the bid is 4.061668. The other ask root, 12.633097, violates the active-trade region. Thus the source's example should be interpreted as a state-dependent possibility, not a universal threshold at an informed fraction of 30%.

For the active uniform-preference case, an implementer can use conditional action likelihoods directly. A buy has probability $\alpha+(1-\alpha)d$ in the high state and $(1-\alpha)d$ in the low state, where $d=1-A/(2m)$. A sell has probability $(1-\alpha)s$ in the high state and $\alpha+(1-\alpha)s$ in the low state, where $s=B/(2m)$. An abstention's probability is the remaining mass. Multiply prior odds by the likelihood ratio of the observed action. Recompute $m$, roots, and feasible regions after every arrival; a stale quote or stale posterior changes the model.

## Discounting and the difference between measured and attainable returns

Section 4 and Proposition 6 add a common discount normalization. Write $D_t=\exp[-r_t(T_0-t)]$ and consistently scale reservation values and quotes as $Z_t^*=D_tZ_t$, $A_t^*=D_tA_t$, and $B_t^*=D_tB_t$. The first line on page 25 prints a positive exponent for $Z_t^*$, whereas its quote equations and asserted invariance use negative exponents. To preserve the same trade decisions, all three must use the same positive scaling factor; the negative-exponent convention here is the one consistent with equation (13) and the subsequent derivation.

The model imposes a normal attainable return $i$ for an uninformed investor who buys now and sells after a normal holding interval $\tau$:

$$
\mathbb E_t\left[\frac{B_{t+\tau}^*}{A_t^*}\right]=e^{i\tau}.
$$

This condition determines the discount normalization rather than emerging from a complete consumption equilibrium. In recursive form,

$$
D_t=e^{-i\tau}\frac{\mathbb E_t[D_{t+\tau}B_{t+\tau}]}{A_t}.
$$

After the informational date, value is known and the terminal normalization uses the normal rate $i$. Iterate this recursion backward. For an integer $n$ such that $t+n\tau\in[T_0-\tau,T_0)$, define

$$
\frac1{k_t}=\left\{\mathbb E_t\left[\prod_{j=0}^{n}\frac{B_{t+(j+1)\tau}}{A_{t+j\tau}}\right]\right\}^{1/(n+1)}.
$$

Then Proposition 6 gives

$$
r_t=i+\frac{n+1}{T_0-t}\log k_t.
$$

The expectation of the sequential round-trip product is at most one under the zero-cost martingale model, so $k_t\geq1$ and the extra term is nonnegative, provided the positive-price and integrability conditions needed for the ratios and logarithms hold. The root is taken after expectation; it is not the expected geometric mean obtained by interchanging the root and expectation. The appendix establishes the product recursion by the tower property and backward induction.

There are two additional visible algebraic slips in the appendix. The base-case expression on page 28 prints a power $T_0-t$ where solving the preceding equation requires $1/(T_0-t)$. On page 29, the final conditional-expectation inequality uses a future conditioning subscript in its first term; the martingale step requires conditioning at the beginning of that holding interval. The reconstruction above uses the recursive return condition directly, so neither typographical step is needed as an implementation rule.

For positive prices, transaction-price returns overstate the return attainable by crossing quotes at the same endpoints:

$$
\frac{p_{t+\tau}^*}{p_t^*}\geq\frac{B_{t+\tau}^*}{A_t^*}.
$$

The reason is mechanical: the observed ending price is at least the bid available to a seller, and the observed starting price is at most the ask paid by a buyer. If the discount normalization changes slowly over the interval, the observed expected gross return is approximately $e^{r_t\tau}$, whereas the imposed attainable return is $e^{i\tau}$. The spread-related difference can be amortized over a longer investment horizon; it is not a free short-horizon premium an uninformed trader can collect.

The discussion relates this distinction to small-firm and neglected-firm return patterns and suggests a possible connection with information around fiscal-year announcements. Those are theoretical interpretations, not empirical tests in this article. There is no estimated asset-pricing regression, historical portfolio sample, or calibrated January-effect magnitude here.

## Reimplementation priorities and limits

The article contains analytical propositions and illustrative numerical mechanisms rather than a documented empirical experiment. It supplies no raw trading dataset, fitted parameter estimates, Monte Carlo replication count, random seed, confidence interval, or complete simulation output table. The binary state values 1 and 11 and the illustrative informed fractions are modeling choices. The independent numerical examples in this note are explicitly reconstructed from the source equations.

A robust implementation should first verify side-specific expected profits, posterior-price identities, and martingale averaging in the inelastic case. Then add elastic demand with root feasibility and abstention likelihoods. Keep arrival count distinct from completed-trade count when abstention is possible, and distinguish a correct-state learning boundary from an observable two-sided stopping rule. Finally, introduce transaction costs or discount normalization as separate extensions instead of mixing their assumptions into the zero-cost theorem.

The source's main mechanism survives these qualifications: informed order flow changes conditional values, and competitive liquidity suppliers charge different prices depending on which side the customer chooses. The model does not determine modern queue dynamics, impact of variable trade sizes, capital-constrained dealer behavior, strategic informed execution, or equilibrium routing across venues. Its clean conditional-expectation structure is a useful component for those richer models, while the scanned formula repairs and the general-learning counterexample mark places where direct transcription would be unsafe.

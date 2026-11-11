# Proof That Properly Anticipated Prices Fluctuate Randomly

**Paul A. Samuelson (1965).** *Industrial Management Review* 6(2), Spring, 41–49. Source: [EfficientMarketHypothesis_Samuelson_1965.pdf](../../Finance/EfficientMarketHypothesis_Samuelson_1965.pdf). The complete nine-page scan, including both panels of Figure 1 and the concluding qualifications, was read visually. Page references below are printed pages. This is a theoretical paper; it contains illustrative stochastic processes, not an estimated financial dataset or trading backtest.

## Why this matters and what the paper establishes

The claim that anticipated news is already in prices is often used to assert that prices must follow independent random walks. Samuelson gives a precise theorem with a narrower conclusion. If the price of a fixed-maturity claim equals the conditional expectation of its terminal payoff under a consistent probability law, subsequent price changes have zero conditional mean. This remains true when the underlying spot price is predictable, seasonal, or mean reverting.

The contribution is the conditional-expectation argument and the separation of its assumptions from its consequences. The theorem does not derive the pricing rule from competitive equilibrium, prove that actual markets satisfy it, or establish statistical independence of price changes. It also provides a mechanism for greater futures-price volatility near delivery, even when the spot-price process has a constant innovation variance.

For a quantitative researcher, the first implementation decision is therefore the object being predicted. A forecast of a future spot price, a change in a fixed-delivery futures quotation, a rolled constant-maturity futures series, and a risk-adjusted asset return are different objects. The proof concerns the second under an explicit pricing axiom. Confusing these objects can make a valid theorem appear contradicted by an irrelevant empirical result.

## Probability model, information, and contract identity

The source starts with spot prices $X_t$ and a conditional distribution for $X_{t+T}$ given the observed history $X_t,X_{t-1},\ldots$. It writes this distribution as $P(X,X_t,X_{t-1},\ldots;T)$. The one-period and multi-period probabilities must be mutually consistent through iterated integration. Equations (1)–(2), pp. 42–43, express that consistency; the result is a version of the law of iterated expectations.

The stochastic process need not be Markov, Gaussian, independent over time, or ergodic. Samuelson initially uses a time-homogeneous conditional law, which he calls stationary in a qualified sense, but the central argument only needs consistent conditional distributions and an integrable terminal payoff. Time homogeneity is not what makes the tower property hold. This last observation is a mathematical clarification of the proof's scope.

Use modern notation $\mathcal F_t$ for the information available at time $t$, with $\mathcal F_t\subseteq\mathcal F_{t+1}$. Fix a delivery date $M$ once and for all. Define $F_t^M$ as the quotation at time $t$ for that same contract. In the source's notation this is $Y(T,t)$ with $T=M-t$. As calendar time advances, the remaining maturity decreases: the next quotation is $Y(T-1,t+1)$, not $Y(T,t+1)$.

This distinction matters for empirical construction. Comparing today's three-month contract with tomorrow's three-month contract changes the terminal payoff. It is not the sequence to which the fixed-maturity martingale proof directly applies. A researcher constructing a rolled series must model roll decisions and changes of delivery month separately.

At delivery the source imposes convergence to the delivered spot price, ignoring commissions:

$$
F_M^M=X_M.
$$

If several grades are deliverable, the terminal payoff can instead be a function of the relevant commodity-price vector, such as the cheaper deliverable grade. The extension remains valid when the correct terminal claim is identified before taking expectations.

## Pricing axiom and martingale proof

The axiom of mathematically expected price formation, equation (6), sets

$$
F_t^M=\mathbb E[X_M\mid\mathcal F_t].
$$

Interest, risk aversion, and transaction costs are initially ignored. The expectation uses the postulated probability law; the paper does not identify it empirically or prove it equals every trader's subjective belief. In particular, replacing this expectation with a risk-neutral expectation and then claiming zero expected gains under actual probabilities would change the theorem's economic content.

Assume $\mathbb E|X_M|<\infty$. Then

$$
\mathbb E[F_{t+1}^M\mid\mathcal F_t]
=\mathbb E[\mathbb E[X_M\mid\mathcal F_{t+1}]\mid\mathcal F_t]
=\mathbb E[X_M\mid\mathcal F_t]
=F_t^M.
$$

Thus $F_t^M$ is a martingale under that law and information filtration. Samuelson's equation (10), p. 45, proves the same identity by interchanging nested probability integrals. Integrability supplies the modern regularity needed for the interchange and conditional expectations.

Define the one-period price innovation $\Delta F_{t+1}^M=F_{t+1}^M-F_t^M$. The immediate consequence is

$$
\mathbb E[\Delta F_{t+1}^M\mid\mathcal F_t]=0.
$$

Under square integrability, this innovation is orthogonal to any square-integrable variable measurable at time $t$. In particular, nonoverlapping price innovations are uncorrelated. Square integrability is needed before discussing Pearson correlations; the first-moment martingale statement alone does not ensure finite variances.

The result does not require independent increments, constant conditional variance, a normal distribution, or a continuous path. Conditional volatility can be highly predictable. A sequence of surprises can therefore be a martingale-difference sequence while displaying volatility clustering or predictable higher moments.

For a finite horizon and bounded predictable holdings $H_t$, the gross trading gain $\sum_t H_t\Delta F_{t+1}^M$ has expectation zero under the same law, by conditioning each term. This is a direct extension of the proof, not a full admissibility theorem in the article. Unlimited doubling strategies, undefined expected payoffs, financing constraints, and execution costs require additional conditions. The paper's informal statements about chart-based profits should be read within its model and regularity assumptions.

## Processes that illustrate the theorem

Samuelson gives several examples to show that random quotation changes do not require an unpredictable spot level.

For a spot process with zero-mean independent increments, $X_{t+1}=X_t+u_{t+1}$, the conditional terminal mean is simply $F_t^M=X_t$. The futures quotation coincides with spot and inherits its zero-mean increments. A Brownian-motion example is a continuous-time analogue, not a necessary distributional assumption.

If increments instead have constant mean $\mu$, the quotation is

$$
F_t^M=X_t+\mu(M-t).
$$

Its next change equals $u_{t+1}-\mu$, with conditional mean zero. Predictable spot appreciation is offset by the shrinking amount of future appreciation still embedded in the quotation. The market's forecast can be correct without the spot process itself being a martingale.

For the autoregressive example, write

$$
X_{t+1}=aX_t+u_{t+1},\qquad
\mathbb E[u_{t+1}\mid\mathcal F_t]=\mu.
$$

The initial autoregressive example uses independent innovations; the later p. 45 discussion says they are uncorrelated. Uncorrelatedness and an unconditional mean alone would be insufficient for the conditional forecast below. The displayed conditional-mean assumption makes the needed restriction explicit. With $|a|<1$, the consistent $h$-period conditional mean is

$$
F_t^{t+h}=a^hX_t+\mu\sum_{j=0}^{h-1}a^j
=\bar x+a^h(X_t-\bar x),\qquad
\bar x=\frac{\mu}{1-a}.
$$

The printed example (c), p. 45, uses $a^hX_t+\mu h$. For the stated autoregression with constant innovation mean, that term should be the geometric sum above. Its subsequent cancellation also omits the corresponding power of $a$. The printed expression is valid in the special zero-mean case used by the figure, or in the unit-root limit, but not for a general nonzero $\mu$ with $a\ne1$. This correction follows by iterating the stated recurrence and preserves the central theorem.

For a finite-state Markov model, let states have spot prices $q_1,\ldots,q_m$ and let the row-stochastic matrix $P$ satisfy $P_{ij}=\Pr(X_{t+1}=q_j\mid X_t=q_i)$. Then

$$
F_t^{t+h}=(P^h q)_i\quad\text{when }X_t=q_i.
$$

The martingale identity becomes $P(P^{h-1}q)=P^h q$. This gives a direct numerical reconstruction without simulating investors or an order book. Use a single transition matrix and terminal payoff vector; independently fitting inconsistent horizon-specific forecasts can violate the very tower property on which the proof relies.

The paper also describes a positive multiplicative process that doubles with probability $1/3$ and halves with probability $2/3$. Its one-period conditional mean is unchanged because $2/3+(1/2)(2/3)=1$. It is a martingale even though a decline is more likely than an increase. This example helps separate conditional mean, median, and typical realized path.

## The maturity-volatility mechanism

Figure 1, pp. 46–47, uses a mean-zero autoregression with $a=1/2$ and current spot $X_t=80$. Expected spot levels one, two, and three periods ahead are 40, 20, and 10. The quotation of the contract delivering in three periods is therefore 10. Future quotations for that *same* delivery date retain conditional mean 10, although their conditional distributions widen as previously unknown innovations arrive.

Write the centered innovation as $\eta_{t+1}=u_{t+1}-\mu$ and suppose its conditional variance is the constant $\sigma_\eta^2$. For a fixed delivery date with current remaining maturity $h$, the corrected autoregressive formula gives

$$
F_{t+1}^{t+h}-F_t^{t+h}=a^{h-1}\eta_{t+1},
$$

and consequently

$$
\operatorname{Var}(F_{t+1}^{t+h}-F_t^{t+h}\mid\mathcal F_t)
=a^{2(h-1)}\sigma_\eta^2.
$$

With $|a|<1$, the one-period quotation-change variance rises as delivery approaches. With $a=1/2$, the multipliers at remaining maturities three, two, and one are $1/16$, $1/4$, and $1$. These numerical variance ratios are derived here from the source's example; the paper does not estimate an innovation variance from commodity data.

The mechanism is mean reversion of spot shocks. An innovation today has little effect on a distant delivery payoff because much of it is expected to dissipate. Close to delivery, less dissipation remains. No change in spot innovation variance is needed. The source's power of $a$ in its accompanying proportionality statement differs by a fixed factor depending on the horizon indexing; the explicit one-step formula above fixes the timing convention.

Increasing one-period volatility toward maturity is different from uncertainty about the terminal price viewed from a fixed current date. The latter accumulates future shocks. Keeping both the conditioning date and the delivery date explicit avoids interpreting the figure's widening forecast distributions as a failure of the zero-drift theorem.

## Discounted expectations and a nonzero expected return

Samuelson next replaces the initial pricing axiom with present-discounted expected value. With a constant gross required return $\lambda>1$ and remaining maturity $h$,

$$
F_t^{t+h}=\lambda^{-h}\mathbb E[X_{t+h}\mid\mathcal F_t].
$$

For that fixed contract, the tower property now gives $\mathbb E[F_{t+1}^M\mid\mathcal F_t]=\lambda F_t^M$. The quotation has a predictable percentage drift of $\lambda-1$, while $\lambda^{-t}F_t^M$ is a martingale up to an irrelevant constant time-origin normalization.

The source allows deterministic horizon-dependent required returns. Set $D_h=\prod_{j=1}^{h}\lambda_j$ and $F_t^M=D_{M-t}^{-1}\mathbb E[X_M\mid\mathcal F_t]$. Its one-step expected growth factor is then $\lambda_{M-t}$. A larger required return close to maturity can express the paper's normal-backwardation intuition when nearer contracts are riskier.

These required-return factors are additional assumptions. The theorem does not estimate them or derive them from a utility-maximizing equilibrium. Interest and a risk premium are discussed as motivations, but a stochastic discount factor correlated with the payoff cannot generally be replaced by an arbitrary deterministic scalar without justification. Likewise, a modern daily-settled futures contract and a prepaid claim have different funding cash flows. The article's quotation model does not implement daily variation margin or settle the forward–futures distinction under stochastic interest rates.

## Extensions, reconstruction, and limits

The terminal payoff may be any integrable $G$ measurable at delivery, including a function of several commodity prices and other observable state variables. Defining $F_t=\mathbb E[G\mid\mathcal F_t]$ preserves the proof. Expanding information to rainfall or quantities is permissible if forecasts remain conditional expectations under one coherent joint law. It does not follow that past spot prices alone are sufficient statistics for every economically relevant forecast.

A reproducible numerical demonstration can specify an AR coefficient, innovation distribution, starting value, delivery date, and number of paths, calculate the analytic quotations above, and compare simulated conditional changes with zero. Alternatively, specify a finite-state transition matrix and verify the matrix identity exactly. The article supplies no Monte Carlo sample size, random seed, estimation window, inference procedure, or measured strategy return. Any numerical calibration beyond its stated $a=1/2$ and starting-value example is a new illustration and should be labeled accordingly.

A statistical test on observed contracts would additionally need synchronized quotation times, fixed delivery identifiers, roll treatment, bid-ask and stale-price controls, collateral returns, a specified information set, and an economically justified expected-return adjustment. Those inputs are absent because the paper proves a conditional proposition rather than proposing an empirical test.

Replacing the expectation by a conditional median does not preserve the tower identity. Nor does zero conditional mean imply an equal chance of gains and losses: the doubling/halving example has a two-thirds chance of a decline. Serially unpredictable means also do not prohibit predictable volatility or nonnormal tails.

Samuelson closes by declining several stronger interpretations. The theorem does not prove actual competitive markets work well, establish that speculation improves welfare, or show that speculative gains are deserved. It leaves unresolved whose probabilities enter prices and how disparate beliefs aggregate. Its lasting contribution is the exact chain of reasoning: a coherent information structure plus the conditional-expectation pricing axiom yields martingale innovations; empirical market efficiency remains a separate claim about whether the assumptions describe observed prices.

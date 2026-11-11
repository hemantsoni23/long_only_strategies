# Forces That Shape the Yield Curve

**Mark Fisher (2001).** *Federal Reserve Bank of Atlanta Economic Review*, First Quarter, pp. 1–15. This is the accessible journal exposition, including its notation appendix; the separate working paper containing Parts 1 and 2 is cited by the author but is not part of this source.

**Source:** [YieldCurveBonds_Fisher_2001.pdf](../../Finance/YieldCurveBonds_Fisher_2001.pdf). Page references below are both PDF and printed page numbers. This is a theoretical teaching article with algebraic illustrations, not a fitted term-structure model or an empirical trading study.

## Why this matters

A yield curve does not directly reveal investors’ forecasts of future short rates. Expectations, compensation for bearing risk, and the nonlinear transformation from bond prices to yields all affect its shape. Fisher develops a deliberately small economy in which these channels can be separated without stochastic calculus. Its usefulness is diagnostic: it shows which conclusions follow from no arbitrage and which require additional assumptions about probabilities, preferences, or the evolution of interest rates.

The central modeling device is a single fair coin flip that determines tomorrow’s entire discount curve. After the flip there is no remaining uncertainty. This is enough to derive a common price of risk across bonds and to show that even when the expected future yield curve is flat, today’s yield curve need not be flat. The mechanism is convexity, which operates even when investors demand no risk premium.

For implementation, the relevant output is a consistent set of current zero-coupon prices given two possible future discount curves, a current short rate, and a common risk-price parameter. This is not a recipe for forecasting real bond returns: those inputs have to be supplied. The article’s contribution is a transparent derivation of the restrictions connecting them.

## Instruments, timing, and conventions

Let $p(t,n)$ be the time-$t$ price of a default-free zero-coupon claim paying one unit at time $t+n$. A coupon bond is a portfolio of such claims, so its price can be obtained by adding each promised cash flow multiplied by the corresponding discount factor. The source deliberately abstracts from liquidity, taxation, embedded options, and credit differences. Its discussion of Treasury securities and STRIPS describes the institutional setting at publication.

The boundary condition is $p(t,0)=1$. The article also uses discount functions tending to zero at long maturities in a positive-rate environment. That long-horizon condition is an additional economic restriction, not the definition of no arbitrage. Likewise, the source’s assertion that nominal rates cannot be negative reflects its frictionless currency argument; the algebra below needs positive gross accumulation $1+r(t)$, not a blanket prohibition on negative quoted rates.

An investor purchasing an $n$-period bond now and selling it one period later receives $p(t+1,n-1)$. The simple holding-period return is

$$
R_{t,t+1}^{(n)}=\frac{p(t+1,n-1)}{p(t,n)}-1.
$$

The denominator is today’s price; tomorrow’s maturity is $n-1$, not $n$. Confusing the maturity date with the remaining tenor changes both the risk calculation and the convexity example.

For the one-period bond, tomorrow’s payoff is certain, so equation (1) on p. 6 defines

$$
1=[1+r(t)]p(t,1),\qquad r(t)=\frac{1}{p(t,1)}-1.
$$

Here $r(t)$ is a simple one-period rate. Later continuously compounded yields use a different convention. Both describe the same prices, but they should not be inserted interchangeably into the discounting equations.

## Deterministic benchmark and the expectations hypothesis

First suppose tomorrow’s bond price is known. Buy the $n$-period bond and borrow its full price for one period. The initial net expenditure is zero and the terminal net payoff is

$$
p(t+1,n-1)-[1+r(t)]p(t,n).
$$

If this known payoff were positive, the trade would be an arbitrage. If negative, reversing the trade would be an arbitrage. Therefore it must be zero, giving equations (2)–(3):

$$
p(t,n)=\frac{p(t+1,n-1)}{1+r(t)}=p(t,1)p(t+1,n-1).
$$

Iterating this recursion until maturity gives the product of the one-period discount factors, equation (18):

$$
p(t,n)=\prod_{j=0}^{n-1}p(t+j,1).
$$

Define the continuously compounded zero-coupon yield by $y(t,n)=-\log p(t,n)/n$. Taking logarithms converts the product into a sum:

$$
y(t,n)=\frac{1}{n}\sum_{j=0}^{n-1}y(t+j,1).
$$

This is the deterministic expectations hypothesis in equation (15). It is exact because future short rates are known. Under uncertainty, replacing those rates by physical expectations does not preserve the equality automatically. The remainder of the article identifies two separate reasons: risk premia in prices and convexity in translating prices into yields.

The proof also clarifies the role of financing. No arbitrage equates a known bond payoff with its financing cost. It does not require the physical expected payoff of every risky bond to equal that cost. An expected payoff can exceed financing cost while the position loses money in one state.

## Binary uncertainty and the first no-arbitrage restriction

Suppress the initial time index. Write $p_n$ for the current price, $r$ for the current simple short rate, and $p^H_{n-1}$ and $p^T_{n-1}$ for the two possible resale prices after the fair coin flip. Physical probabilities are each one half. Define

$$
\bar p_{n-1}=\frac{p^H_{n-1}+p^T_{n-1}}{2},\qquad
\delta^p_{n-1}=\frac{p^H_{n-1}-p^T_{n-1}}{2}.
$$

Then the state-contingent future bond prices are $\bar p_{n-1}\pm\delta^p_{n-1}$. The variance of tomorrow’s price is $(\delta^p_{n-1})^2$ and its standard deviation is $|\delta^p_{n-1}|$. Fisher calls the signed quantity volatility because its sign identifies whether the payoff rises or falls in the chosen state. In most statistical usage volatility is nonnegative, so retaining that sign convention explicitly is important.

For a nondegenerate bond with $p^H_{n-1}>p^T_{n-1}$, no arbitrage in the bond-plus-financing trade requires

$$
p^T_{n-1}<(1+r)p_n<p^H_{n-1}.
$$

The inequalities are strict: equality at one boundary produces a zero payoff in one state and a strictly positive payoff in the other after choosing the appropriate trade direction. Such a free contingent gain also qualifies as arbitrage. If both future prices coincide, this interval collapses and deterministic discounting applies.

Introduce an adjustment $a_{n-1}$ to the physical mean payoff, following equation (5):

$$
p_n=\frac{\bar p_{n-1}-a_{n-1}}{1+r}.
$$

Rearranging gives the expected simple holding return, equation (6):

$$
E[R^{(n)}]=r+\frac{a_{n-1}}{p_n}.
$$

The adjustment is measured in units of next-period price, whereas the excess expected return is the adjustment divided by today’s price. The adjustment can be negative when the bond provides valuable insurance. Nothing in this individual-bond calculation makes compensation necessarily positive or proportional to maturity.

## Cross-maturity hedging and the common price of risk

The decisive step uses two maturities driven by the same coin. Hold one $n$-period bond and $b$ units of an $m$-period bond. Their combined future payoffs are

$$
\pi^H=p^H_{n-1}+bp^H_{m-1},\qquad
\pi^T=p^T_{n-1}+bp^T_{m-1}.
$$

For a nonzero exposure $\delta^p_{m-1}$, equation (8) gives the hedge ratio

$$
b^*=-\frac{p^H_{n-1}-p^T_{n-1}}{p^H_{m-1}-p^T_{m-1}}
=-\frac{\delta^p_{n-1}}{\delta^p_{m-1}}.
$$

This makes the state-contingent payoffs identical. When both exposures have the same sign, the hedge requires shorting the second bond. The known payoff is $\pi^*=\bar p_{n-1}+b^*\bar p_{m-1}$, while its initial price is $p_n+b^*p_m$. Financing this portfolio requires

$$
\pi^*=(1+r)(p_n+b^*p_m).
$$

Substituting the adjusted-mean pricing equations and cancelling the mean payoffs yields $a_{n-1}+b^*a_{m-1}=0$. Consequently,

$$
\frac{a_{n-1}}{\delta^p_{n-1}}=\frac{a_{m-1}}{\delta^p_{m-1}}=\lambda.
$$

This is equation (12), the common price of risk. It is a cross-sectional restriction: given this single source of risk, the compensation per unit of signed exposure must agree across maturities. No arbitrage does not estimate $\lambda$ or establish its sign. Preferences and the economic meaning of the states must supply that information.

Equations (13)–(14) then become

$$
a_{n-1}=\lambda\delta^p_{n-1},\qquad
E[R^{(n)}]=r+\lambda\frac{\delta^p_{n-1}}{p_n}.
$$

The relative exposure $\delta^p_{n-1}/p_n$ is the signed standard-deviation analogue for holding returns. The risk premium disappears if either exposure or its price is zero. A longer maturity is not itself the primitive risk quantity; the relevant quantity is how much its resale price differs between the two states.

A useful implementation consequence, derived from these equations, is the equivalent probability representation:

$$
p_n=\frac{q_Hp^H_{n-1}+q_Tp^T_{n-1}}{1+r},\qquad
q_H=\frac{1-\lambda}{2},\quad q_T=\frac{1+\lambda}{2}.
$$

For a genuinely risky bond the strict interval condition implies $-1<\lambda<1$, giving strictly positive pricing probabilities. These are pricing weights, not the physical probabilities, which remain one half. Interchanging the labels of the states reverses both the exposure and $\lambda$, leaving prices unchanged.

This representation also shows the model’s limits. Risk-free discounting plus one nondegenerate binary risky payoff spans two states. With several independent shocks, two bonds generally cannot remove all uncertainty and a single scalar price of risk is insufficient. The exact hedge is a property of this binary economy, not a claim that any two real government bonds perfectly hedge each other.

## Yields, compounding, and the convexity channel

For an $n$-period unit-payoff bond, the gross return from purchase to maturity is $1/p_n$. With $i$ compounding intervals per period, the quoted yield satisfies

$$
\left(1+\frac{y_i}{i}\right)^i=p_n^{-1/n},\qquad
y_i=i\left[p_n^{-1/(ni)}-1\right].
$$

Simple compounding uses $i=1$; continuous compounding gives $y_n=-\log p_n/n$. The current one-period relation is $y_1=\log(1+r)$. These formulas, on p. 11, matter when comparing rates or reproducing figures.

The mapping from a future price $P$ to its remaining-tenor yield is $-\log(P)/(n-1)$. It is decreasing and convex. Jensen’s inequality therefore gives

$$
-\frac{\log E[P]}{n-1}\leq E\left[-\frac{\log P}{n-1}\right].
$$

The yield computed from the mean price is below the mean yield. Charts 4–5 illustrate this geometrically. This comparison holds the remaining maturity fixed; it should not be confused with simply comparing the level of ten- and twenty-year yields at one arbitrary price.

To isolate this effect, Fisher sets the current short continuously compounded yield and the mean post-flip yield equal to $\bar y$, and assumes a constant signed yield displacement $d=\delta^y$ across all remaining maturities. The two future yields are $\bar y+d$ and $\bar y-d$. Their corresponding prices are exponentials of minus remaining maturity times yield. A positive yield displacement means a negative price displacement, so the sign convention for yield risk differs from that for price risk.

With zero risk-price adjustment, the exact price and current yield implied by the article’s setup are

$$
p_n=e^{-n\bar y}\cosh((n-1)d),\qquad
y_n=\bar y-\frac{1}{n}\log\cosh((n-1)d).
$$

These equations are a reconstruction from the preceding pricing relations; the source prints an approximation and points to its companion working paper for the exact formula. They make the timing explicit: there are $n-1$ periods after tomorrow’s coin flip and one initial period discounted at $\bar y$.

Using $\log\cosh z=z^2/2+O(z^4)$ gives the local approximation

$$
y_n\approx\bar y-\frac{(n-1)^2}{2n}d^2.
$$

For maturities large enough that $(n-1)^2/n\approx n$, but small enough that $|(n-1)d|$ remains modest, this becomes the source’s p. 13 expression $y_n\approx\bar y-nd^2/2$. The two approximation requirements should not be conflated. In particular, substituting $n=1$ into the simplified formula spuriously creates a convexity correction; the exact one-period correction is zero.

## Numerical illustration and a reproducible calculation

Chart 6 uses $\bar y=0.10$ and $d=0.05$: the two future yield curves are flat at 15% and 5%, with physical mean 10%. These are illustrative parameter choices, not estimates or fitted market forecasts. A direct implementation can evaluate the exact formula for integer maturities from one to thirty years.

Derived values, rounded, are about 10.000% at one year, 9.603% at five, 9.020% at ten, 8.019% at twenty, and 7.299% at thirty. They show how today’s curve can slope down even though mean future yields do not. For numerical stability at large arguments, evaluate $\log\cosh z$ as $|z|+\log(1+e^{-2|z|})-\log2$.

A complete reproduction of the theoretical exercise proceeds as follows:

1. Choose maturity units, the current simple rate, and two arrays of positive future discount factors with unit payoff at remaining tenor zero. Keep the physical probabilities at one half to match the source.
2. Compute each mean price and signed price displacement. Supply a common $\lambda$ strictly between minus one and one, or infer it from one observed risky price and test consistency of the others.
3. Price all maturities using the adjusted mean formula. Check both state inequalities and confirm the one-period price is $1/(1+r)$.
4. For any two nondegenerate maturities, compute $b^*$ and verify equal state payoffs and correct discounting of the hedged portfolio. A discrepancy identifies inconsistent prices or a coding error.
5. Transform prices into yields using one declared compounding convention. Compare the physical mean future yield with the yield of the mean future price separately from the current yield.
6. Set $\lambda=0$ and the chart parameters above to reproduce the convexity example. Then vary risk pricing while holding the two future curves fixed to isolate compensation for risk.

This procedure does not require Monte Carlo simulation: there are only two outcomes and expectations are exact finite sums. Introducing a random-number generator would add sampling noise without supplying new economic content.

## What the article establishes, and what remains unspecified

The source establishes a common compensation-to-exposure ratio in its one-factor binary setting, deterministic averaging of short yields when rates are certain, and a downward yield adjustment from convexity when averaging uncertain prices. Its introductory discussion connects these mechanisms to upward slopes and long-end humps, but the final section explicitly defers a fully rigorous treatment of risk premia in yield space to the companion working paper. The present article is therefore not a complete calibrated explanation of observed curve shapes.

There is no security panel, sample period, curve-fitting algorithm, estimation objective, standard-error calculation, forecast evaluation, transaction-cost model, or out-of-sample trading test. Charts 1–5 are explanatory diagrams; source coordinates sufficient to reproduce their exact plotted curves are not supplied. Chart 6 supplies the parameters needed for its theoretical example. The historical discussion of curve behavior should not be promoted to a statistical estimate.

A practical application must supply a physical distribution of future curves, a specification of risk pricing, and suitable instruments. It would also need to accommodate recurrent uncertainty, multiple factors, financing constraints, bid–ask spreads, and market segmentation. The article’s short-sale and borrowing arguments assume trades can be reversed freely; constraints can obstruct the exact arbitrage constructions.

The lasting takeaway is a discipline for interpretation. Price expectations, expected holding returns, and expected yields are different objects. A yield curve mixes them through discounting, risk compensation, and a nonlinear transformation. Reconstructing those operations explicitly is the prerequisite for using its shape as evidence about future interest rates.

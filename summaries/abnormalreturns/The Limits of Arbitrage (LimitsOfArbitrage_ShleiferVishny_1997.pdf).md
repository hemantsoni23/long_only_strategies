# The Limits of Arbitrage

Andrei Shleifer and Robert W. Vishny, *The Journal of Finance* 52(1), March 1997, pp. 35–55. Source: [LimitsOfArbitrage_ShleiferVishny_1997.pdf](../../Finance/LimitsOfArbitrage_ShleiferVishny_1997.pdf). The supplied file contains the complete twenty-one-page article and three additional pages of linked references. Page references below use the journal pagination; PDF page numbers are journal pages minus 34.

## Why this matters

A trade can converge to a known terminal payoff and still be impossible to finance through its intermediate losses. This paper makes that distinction economically consequential by separating the specialists who understand a mispricing from the investors who supply their capital. Investors observe performance much more readily than they observe the trade's quality. Consequently, a widening mispricing can lower both the specialist's marked wealth and the amount outsiders are willing to entrust to that specialist. The opportunity improves while the ability to exploit it deteriorates.

The innovative component is a model of performance-based arbitrage: delegated capital responds to realized returns, and that response feeds back into prices. The central result is particularly sharp when specialists entered the trade fully invested. Further pessimism forces them to sell an asset whose terminal value they know, rather than buy more of it. Their selling amplifies the price effect of the original shock. Initial caution also becomes rational: maintaining cash protects the option to invest after a worsening of the opportunity.

For a quantitative researcher, the useful object is the joint system linking prices, marked portfolio returns, investor flows, and subsequent positions. Forecasting convergence alone leaves out an endogenous funding state. The paper is a theoretical mechanism with a small numerical illustration, not an estimated trading strategy, a causal empirical test, or a calibrated fund-redemption model. Its discussion of anomalies and market specialization extends the formal model's logic without providing new portfolio backtests.

## Economic environment and information

There are three dates, $t=1,2,3$, one risky asset in unit supply, and cash. The asset's fundamental value is the constant $V$. Arbitrageurs know $V$ from the start. Their investors do not understand the detailed pricing model or the arbitrage strategy. Noise traders may be pessimistic at dates 1 and 2; everyone recognizes the value at date 3, so $p_3=V$ with certainty. There is no long-run fundamental payoff risk in the formal model. The risk is that the price moves farther from $V$ before the trade can be completed.

The three participant classes are noise traders, specialized arbitrageurs, and investors allocating capital across arbitrageurs. A specialist operates in one narrow market or strategy segment. Many price-taking specialists compete within that segment, and there are many segments. The model does not give an individual specialist market power. It does allow their common strategy and common investor response to have an aggregate effect on market clearing.

Let $S_t$ denote pessimistic noise-trader demand displacement. Their aggregate quantity demand is equation (1), p. 38:

$$
Q_N(t)=\frac{V-S_t}{p_t}.
$$

The initial displacement $S_1$ is known. At date 2, either the error disappears, with probability $1-q$, or it worsens to a fixed $S>S_1$, with probability $q$. The recovery state has $S_2=0$ and $p_2=V$. The adverse state's price will be denoted $p_2^-$ below when distinguishing states helps. This notation is explanatory; the article generally writes $p_2$ for that adverse-state price.

Initial arbitrage capital $F_1$ is given and includes available borrowing capacity. Let $D_1\in[0,F_1]$ be dollars invested in the asset at date 1. Holdings are $D_1/p_1$, while $F_1-D_1$ remains in cash. Market clearing gives equation (3):

$$
p_1=V-S_1+D_1.
$$

The article focuses on parameters with $F_1<S_1$, so even fully invested specialists cannot restore the initial price to $V$. In the adverse date-2 state, they invest all available resources $F_2^-$: the terminal price is certain and exceeds the current price. Their holdings then equal $F_2^-/p_2^-$. Equation (2) becomes

$$
p_2^-=V-S+F_2^-.
$$

The intended region has positive prices and remaining capital, with $F_2^-<S$. In the recovery state the specialists liquidate their risky positions and hold cash. Cash has zero net return in this setup; inserting an interest rate would change the equations and is not part of the reported model.

## Capital supply and the agency assumption

The article motivates delegation with heterogeneous investor beliefs about manager ability and competition in investment services. Investors allocate funds to the manager they believe offers the best expected return net of fees. Competition makes service prices equal to constant marginal cost. Different beliefs prevent every investor from choosing the same manager. Investors cannot reliably infer the changing structural model of each narrow arbitrage market, so their updating is summarized by the manager's realized performance.

This story motivates, rather than fully estimates or uniquely derives, the following capital-supply function. A specialist's gross portfolio return from date 1 to date 2 is

$$
R_A=\frac{D_1}{F_1}\frac{p_2}{p_1}+\frac{F_1-D_1}{F_1}
=1+\frac{D_1}{F_1}\left(\frac{p_2}{p_1}-1\right).
$$

Equation (4), p. 40, specifies

$$
F_2=F_1G(R_A),\qquad G(1)=1,\quad G'\geq1,\quad G''\leq0.
$$

The normalization makes zero benchmark-relative performance leave capital unchanged. The derivative includes the mechanical effect of returns on wealth. Therefore $G'=1$ is already a meaningful limited-capital case: lost money is not replenished. A derivative above one adds net investor withdrawals after losses and inflows after gains. It should not be interpreted as merely the slope of external net flows.

The main analysis uses the linear specialization

$$
G(x)=ax+1-a,\qquad a\geq1.
$$

Equation (6), p. 41, then reads

$$
F_2=F_1+aD_1\left(\frac{p_2}{p_1}-1\right).
$$

Marked portfolio wealth before external flows is $F_1+D_1(p_2/p_1-1)$. External net flows are consequently $(a-1)D_1(p_2/p_1-1)$. This decomposition explains why $a=1$ involves no extra withdrawals, whereas $a>1$ makes a negative return shrink investable resources by more than the trading loss itself.

The model's interpretation requires caution. An investor could rationally infer from poor performance that a manager is weak, even when the manager knows that the opportunity has improved. But the paper does not solve a complete Bayesian learning system for an estimated $a$, nor an optimal contracting problem that proves all other financing arrangements impossible. It discusses why limited liability, information secrecy, uncertain ability, and outside options may prevent contracts from eliminating the agency problem. Those arguments support the assumed flow rule; they are not additional solved states in the model.

## The portfolio decision and competitive equilibrium

The specialist maximizes expected date-3 funds under management, which the paper treats as equivalent to the relevant profit objective under its fee structure. After early recovery, terminal managed funds are

$$
W^+=F_1+aD_1\left(\frac{V}{p_1}-1\right).
$$

After adverse sentiment at date 2, every remaining dollar is invested until the terminal convergence:

$$
W^-=\frac{V}{p_2^-}
\left[F_1+aD_1\left(\frac{p_2^-}{p_1}-1\right)\right].
$$

Equation (7) maximizes $(1-q)W^++qW^-$. Crucially, each individual specialist takes prices as given when differentiating. Substituting aggregate market-clearing prices into this objective and taking their total derivative would instead give a different problem in which a representative trader internalizes price impact.

After dividing the price-taking marginal payoff by $a$, equation (8), p. 43, is

$$
g(D_1)=(1-q)\left(\frac{V}{p_1}-1\right)
+q\left(\frac{p_2^-}{p_1}-1\right)\frac{V}{p_2^-}.
$$

For the parameter region studied, an interior allocation satisfies $g(D_1)=0$ after equilibrium prices are imposed. At the fully invested corner, $D_1=F_1$ and $g(D_1)\geq0$. Equality can also hold at the boundary between regimes; the source's strict-inequality wording should not exclude this knife-edge case. A complete numerical solver should additionally check the lower boundary and all feasibility restrictions rather than presuppose that every arbitrary input lies in the paper's interior or upper-corner region.

The first term is the benefit from buying earlier if convergence occurs immediately. The second is negative when the adverse price is below $p_1$: an early dollar loses value and is subject to the capital response before it can exploit the improved opportunity. Holding cash is valuable even though the asset is initially underpriced and the specialist is risk neutral. This cash option, rather than conventional variance aversion, generates the interior choice.

Proposition 1 says that for fixed $V,S_1,S,F_1,a$, a cutoff $q^*$ separates full investment at sufficiently small worsening probability from retained cash at larger probability. The threshold is a property of equilibrium prices and incentives, not an externally specified risk limit. The parameter $a$ cancels from the marginal condition directly but still affects that condition through adverse-state equilibrium prices.

## A reproducible solution procedure

The following reduction is algebra from the paper's equations, provided here to make implementation explicit. For any trial aggregate $D\in[0,F_1]$, calculate

$$
p_1(D)=V-S_1+D,
$$

$$
p_2^-(D)=\frac{V-S+F_1-aD}{1-aD/p_1(D)},
\qquad F_2^-(D)=p_2^-(D)-V+S.
$$

Also calculate $F_2^+(D)=F_1+aD(V/p_1(D)-1)$. The rational expression for $p_2^-$ results from combining market clearing with capital supply. It is valid only while its branch is economically admissible. Check that prices are positive, the denominator is nonzero, managed capital is nonnegative, and the assumed mispricing and investment regime apply. Negative capital is not a legitimate trading position; the linear flow formula is not a global model of bankruptcy.

First evaluate $g(F_1)$. If it is nonnegative and the full-investment state is feasible, use the upper corner. Otherwise solve $g(D)=0$ on a feasible interval, for example by bisection when signs bracket a root. Record the residuals in both market-clearing equations and the capital equation, and verify the complementarity condition at the chosen boundary or interior point. This implements a competitive equilibrium, preserving price taking in the first-order condition while imposing aggregate consistency afterward.

For the upper corner, write $A=V/p_1-1$ and $B=(p_2^-/p_1-1)V/p_2^-$. If $A>0>B$, its cutoff is

$$
q^*=\frac{A}{A-B}.
$$

This formula also provides a useful test of a numerical implementation. A second test is the $a=1$ case: a fully invested manager retains the same number of shares after a price fall, although marked dollars decline. A third is the artificial constant-capital benchmark $a=0$: resources are restored to $F_1$ regardless of trading losses. That comparison lies outside the assumed $a\geq1$ flow family but is expressly used by the authors as a benchmark.

## Numerical example and an identifiable discrepancy

The illustration on pp. 44–46 sets $V=1$, $F_1=0.2$, $a=1.2$, $S_1=0.3$, and $S=0.4$. No empirical units or fitted parameters are attached to these values. They normalize fundamental value to one and illustrate economically possible regimes.

| Quantity | Fully invested case | Interior case with $q=0.5$ |
|---|---:|---:|
| Initial investment $D_1$ | 0.200000 | 0.174282 |
| Initial price $p_1$ | 0.900000 | 0.874282 |
| Adverse-state price $p_2^-$ | 0.763636 | 0.776644 |
| Adverse-state capital $F_2^-$ | 0.163636 | 0.176644 |
| Recovery-state capital $F_2^+$ | 0.226667 | 0.230073 |

These are recomputed values from the equations; they reproduce the article's displayed values to its stated decimal precision. Greater willingness to wait makes the initial price lower because less specialist money supports it. It leaves more capital for the bad state, making the subsequent adverse price higher than under full initial investment.

The article prints $q^*=0.35$. Substitution of its parameters into equations (2), (3), (6), and (8) gives $q^*=0.358974\ldots$. This small discrepancy should be retained in a replication log rather than forcing a solver to return 0.35. Both values convey the same regime comparison, but they are not numerically identical. For liquidation, the reconstructed boundary is approximately $q=0.387755$, consistent with the article's rounded statement that liquidation occurs below about 0.39.

At full investment, initial holdings are $0.2/0.9=0.222222$ units. After the adverse state, holdings are $0.163636/0.763636=0.214286$ units. Specialists therefore sell units, not merely report a lower dollar valuation of unchanged positions. In the $q=0.5$ interior solution, holdings rise from approximately 0.199343 to 0.227445 units. A sufficiently large cash reserve reverses the liquidation outcome even though the same fundamental value and sentiment shocks apply.

## Why falling prices can cause selling

Proposition 3, p. 45, concerns full initial investment, a worsening displacement, and $a>1$. Under these conditions $F_2^-<D_1$ and $F_2^-/p_2^-<D_1/p_1$. The difference between final and initial quantities can be written particularly transparently as

$$
\frac{F_2^-}{p_2^-}-\frac{F_1}{p_1}
=(a-1)F_1\left(\frac1{p_1}-\frac1{p_2^-}\right)<0.
$$

The expression is zero for $a=1$. Thus losses without replenishment reduce purchasing power but do not themselves require a fully invested manager to sell existing units; investor withdrawals create that additional liquidation. Full investment is sufficient, not necessary. A small cash buffer can still be overwhelmed by withdrawals, as the numerical liquidation threshold demonstrates.

For full investment, equation (9) is

$$
p_2^-=\frac{V-S-(a-1)F_1}{1-aF_1/p_1}.
$$

On the stable positive-capital branch $aF_1<p_1$, keeping the initial state fixed yields

$$
\frac{\partial p_2^-}{\partial S}
=-\frac1{1-aF_1/p_1}<-1,
$$

$$
\frac{\partial^2p_2^-}{\partial a\,\partial S}
=-\frac{F_1/p_1}{(1-aF_1/p_1)^2}<0.
$$

These are Proposition 4's amplification results. A one-unit deterioration in noise demand lowers the price by more than one unit because it also removes specialist capital. Increasing performance sensitivity strengthens the amplification. For the illustration, the adverse-price slope is about $-1.363636$, compared with $-1$ when capital is automatically replenished and zero under unconstrained arbitrage that keeps price at fundamental value.

The stability denominator is not a license to extrapolate to arbitrarily large shocks. Even with a positive denominator, the numerator or resulting capital can cross an economic boundary. The paper discusses complete exit when the stable equilibrium fails, at a price supported only by noise traders, $V-S$. Implementations must handle this as a regime change. Continuing the rational expression into negative capital would misrepresent the model.

## Comparative statics and the limits of the conclusions

Proposition 2 reports that larger initial or later pessimism worsens the corresponding prices. When specialists initially retain cash, anticipating a larger adverse date-2 shock also depresses date-1 price: they preserve more liquidity. At the fully invested corner, changing the later shock does not affect the initial price while the same regime persists.

The authors deliberately avoid a universal claim that performance-sensitive capital always lowers ex ante market efficiency. In their two-state example, date-2 sentiment either vanishes or worsens. Stronger performance feedback then lowers the adverse price and weakly lowers the initial price. With gradual partial recovery, however, gains can attract funding before all mispricing disappears. The feedback can accelerate convergence. The distribution and timing of sentiment shocks therefore matter for an unconditional volatility or efficiency comparison.

The article's section III identifies mechanisms that could attenuate or reinforce the problem. Redemption delays can allow a position to converge before withdrawals. Diversification can prevent every position losing simultaneously. Long lockups and closed-end structures protect capital, but expose investors to being trapped with an ineffective manager. Creditors can demand cash when collateral falls even if equity investors cannot redeem. Internal capital allocators can also impose liquidation on a trader whose apparent performance deteriorates. These are institutional interpretations; their relative magnitude is not estimated here.

The formal arbitrageur is risk neutral and knows terminal value. The paper separately suggests that risk aversion, uncertain skill, or learning about an unstable strategy may cause voluntary selling before a mandatory cash shortage occurs. It also recognizes that outsiders with performance-independent funding could absorb distressed positions and undo the mechanism. Its defense is specialization: outside capital may lack the knowledge or reputation to enter precisely the distressed strategy. Neither perfect segmentation nor universal funding fragility should be assumed in an empirical application without evidence.

## Empirical implications and what a replication would require

Section IV discusses risky real-world arbitrage, extending beyond the formal model's certain terminal convergence. Specialized investors care about total trade risk, including idiosyncratic components that a market-wide factor model might classify as diversifiable. A security can remain overpriced and have low expected returns despite high idiosyncratic volatility, because shorting it is hazardous. This differs from a segmented rational-pricing explanation in which bearing additional unhedgeable risk necessarily demands a higher expected return.

The relevant comparison is expected alpha relative to risk over the funding horizon. Doubling both noise-driven alpha and volatility need not deter arbitrage: halving position size preserves both. High volatility becomes unattractive when alpha does not rise proportionally, when fundamental uncertainty dominates, or when convergence occurs much later than performance evaluation. The article's discussion of value versus glamour uses prior evidence, including an approximate 60% one-year probability of outperforming the S&P 500; it explicitly notes that this probability depends on the sample and universe. It is not a newly estimated universal win rate.

No dataset, estimation window, transaction-cost model, investor-level flow panel, or statistical inference procedure is supplied for fitting the theoretical system. An empirical implementation would need observations separating marked returns from external flows, measures of capital commitment and redemption terms, a defensible proxy for mispricing, and identification of common strategy exposure. It would also need to distinguish manager withdrawals caused by losses from withdrawals anticipating genuinely worse fundamentals. Those are proposed requirements for testing the mechanism, not methods claimed by this paper.

The practical conclusion is conditional and specific. A large pricing discrepancy can coexist with weak corrective demand when those best equipped to exploit it have already committed their capital and face return-sensitive financing. Sizing, cash reserves, investor terms, collateral rules, and convergence horizon then enter the research problem alongside expected return. The model explains why an apparently superior opportunity may be hardest to hold; it does not identify which observed discrepancies are genuine or guarantee that waiting for convergence will pay.

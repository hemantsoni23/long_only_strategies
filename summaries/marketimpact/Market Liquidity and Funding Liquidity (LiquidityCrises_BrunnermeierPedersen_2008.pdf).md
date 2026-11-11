# Market Liquidity and Funding Liquidity

Markus K. Brunnermeier and Lasse Heje Pedersen. *Review of Financial Studies* 22(6), 2009, 2201–2238; advance publication November 26, 2008. DOI: 10.1093/rfs/hhn098. Source: [LiquidityCrises_BrunnermeierPedersen_2008.pdf](../../Finance/LiquidityCrises_BrunnermeierPedersen_2008.pdf). The filename's 2008 date refers to advance publication, while the article's volume is 2009. This note covers the complete article, institutional Appendix A, and mathematical Appendix B. Page references are printed journal pages.

## Why this matters and the contribution

A liquidity provider may recognize that a security is cheap and still be unable to buy it. Buying requires financing, financing requires a margin contribution, and the provider's usable capital may decline at exactly the time that margins rise. Brunnermeier and Pedersen turn this balance-sheet mechanism into a competitive equilibrium model. Their distinctive contribution is to make margin requirements responsive to price movements and information, allowing funding conditions and market liquidity to reinforce each other.

The paper separates a **loss spiral**, in which price changes reduce the capital supporting existing positions, from a **margin spiral**, in which those changes increase the required capital per position. Either can amplify shocks; together they can be more powerful than the sum of their isolated effects. The analysis also derives a common shadow price of financing across assets, explaining why otherwise unrelated securities can become illiquid together and why high-margin securities can suffer disproportionately.

This is primarily a theory paper with numerical illustrations and institutional evidence. It does not estimate a structural model on a specified stock universe, run a portfolio backtest, or report confidence intervals for a causal effect of margins. Its contribution to empirical work is a set of conditional predictions and mechanisms. Replicating its figures means solving an equilibrium, not fitting an ordinary return regression.

## Agents, dates, shocks, and state variables

There are $J$ risky assets, trading dates $t=0,1,2$, and final payoffs $v^j$ at $t=3$. Net asset supply and the aggregate customer endowment shock are zero, and the risk-free interest rate is zero. Fundamental value is the conditional expected payoff $v_t^j=E_t[v^j]$. Its innovations satisfy

$$
v_{t+1}^j=v_t^j+\sigma_{t+1}^j\epsilon_{t+1}^j,
\qquad
\sigma_{t+1}^j=\sigma^j+\theta^j|\Delta v_t^j|,
$$

where the $\epsilon$ innovations are independent standard normal across dates and assets, and $\sigma^j,\theta^j\geq0$. This is a conditional **standard-deviation** rule, not the conventional squared-return GARCH variance recursion. Large fundamental shocks increase subsequent fundamental volatility when $\theta^j>0$.

There are three customer groups indexed by arrival date $k=0,1,2$. Each has exponential utility with risk aversion $\gamma$ and an anticipated terminal endowment $z^{j,k}$ of each security, with $\sum_k z^{j,k}=0$. Trading offsets the endowment risk. With probability $1-a$, all customers arrive at time zero, so their demands can offset immediately. With probability $a$, they arrive sequentially. Before arrival a customer's market position is zero. The aggregate endowment of customers already present at time $t$ is $Z_t=\sum_{k=0}^t z^k$.

Speculators are risk neutral, intermediate the temporary order imbalance, and maximize terminal wealth. Their capital evolves as

$$
W_t=W_{t-1}+(p_t-p_{t-1})^\top x_{t-1}+\eta_t,
$$

where $x$ is their position and $\eta_t$ is an independent wealth shock from other activities. Funding is constrained by

$$
\sum_j\left(m_t^{j,+}x_t^{j,+}+m_t^{j,-}x_t^{j,-}\right)\leq W_t,
\qquad x_t^j=x_t^{j,+}-x_t^{j,-}.
$$

Both long and short positions consume capital. A short sale does not release unrestricted cash: its proceeds collateralize the borrowing and an additional margin protects against price increases. The $m$ variables are dollar margins per unit, not necessarily fixed percentages of notional. A margin percentage must be converted to the appropriate dollar requirement before using this equation.

Speculators cannot replenish capital instantaneously. The model would allow capital raised only at time two without changing its central intermediation problem. When wealth becomes nonpositive, further risky positions are prohibited. Bankruptcy utility assumptions matter for time-zero risk-taking; the paper specifies them rather than relying entirely on limited liability.

Financiers set margins so a position's one-period loss exceeds the nonnegative margin with probability at most $\pi$, usually a small number such as one percent. For a long position,

$$
\Pr(-\Delta p_{t+1}^j>m_t^{j,+}\mid\mathcal F_t)\leq\pi,
$$

with equality when the unconstrained loss quantile is positive, and the analogous upper-tail condition for a short position. If the loss quantile is negative, flooring the required margin at zero makes the inequality strict. Informed financiers observe fundamental values, customer shocks, prices, and relevant wealth shocks. Uninformed financiers observe prices and must infer how much of a move is fundamental. The information set is central to the model: the same apparent price decline can justify opposite margin responses under different information.

## Solving backward and defining liquidity

Market illiquidity is the absolute deviation of price from fundamental value. Define signed deviation $\Lambda_t^j=p_t^j-v_t^j$; then illiquidity is $|\Lambda_t^j|$. It is not directly a bid–ask spread, turnover measure, or price-impact regression coefficient. An empirical test needs a defensible mapping from observable liquidity proxies to this theoretical wedge.

At time two every customer is present. Because total endowment exposure is zero, customers can offset their risks without speculator capital, and the unique equilibrium has $p_2=v_2$. If all customers arrive at time zero, the same argument gives fundamental pricing at every date. Temporary imbalance under sequential arrival creates the economically interesting case.

At time one, customers 0 and 1 each choose

$$
y_1^{j,k}=\frac{v_1^j-p_1^j}{\gamma(\sigma_2^j)^2}-z^{j,k}.
$$

Market clearing therefore requires, for a given asset,

$$
x_1^j=Z_1^j+\frac{2(p_1^j-v_1^j)}{\gamma(\sigma_2^j)^2}.
$$

For positive $Z_1^j$, customers want to sell at fundamental value, speculators absorb positive inventory, and any funding-induced discount reduces the amount customers sell. The factor two comes from two customers being present. Omitting it changes the equilibrium slope and the spiral multiplier.

Risk-neutral speculators allocate scarce financing to positions with the highest expected convergence profit per margin dollar. For positive wealth, their marginal value of capital is

$$
\phi_1=1+\max_j\left\{\frac{v_1^j-p_1^j}{m_1^{j,+}},\frac{p_1^j-v_1^j}{m_1^{j,-}}\right\}.
$$

For every asset they actually hold, Proposition 1 gives

$$
|\Lambda_1^j|=m_1^j(\phi_1-1).
$$

Use the margin for the appropriate position direction. For assets with zero speculative positions, equality becomes an inequality. The relation is a complementary-slackness condition: an unheld opportunity cannot offer a strictly higher profit per financing dollar than held opportunities. If capital is abundant, $\phi_1=1$ and prices equal fundamentals. When capital is scarce, a common financing shadow value links the pricing wedges across assets.

## Why informed margins can stabilize prices

Let $z_\pi=\Phi^{-1}(1-\pi)$. At time one, informed financiers know both current fundamental value and that price equals fundamental value next period. The exact margins are

$$
m_1^{j,+}=\max\{z_\pi\sigma_2^j+\Lambda_1^j,0\},
\qquad
m_1^{j,-}=\max\{z_\pi\sigma_2^j-\Lambda_1^j,0\}.
$$

A speculator buying below fundamental value expects a favorable convergence move. That expected gain cushions possible fundamental losses, reducing the required long margin. A speculator shorting above fundamentals receives the symmetric protection. In this benchmark, greater mispricing can ease the funding needed to arbitrage it.

This conclusion requires knowledge of the fundamental value and of near-term convergence. It does not say that real financiers always lower margins in a crisis. It also applies specifically to the time-one problem; before time one, even informed financiers face uncertainty about future market liquidity. The paper later shows that time-zero margins can rise with illiquidity because funding-induced price risk remains unresolved.

## Why uninformed margins can destabilize prices

When financiers observe only prices and the prior probability $a$ of sequential arrival approaches zero, they attribute most observed price variation to fundamentals. Proposition 3 obtains the limiting common long and short margin

$$
m_1^j=z_\pi\left(\sigma^j+\theta^j|\Delta p_1^j|\right)
=z_\pi\left(\sigma^j+\theta^j|\Delta v_1^j+\Delta\Lambda_1^j|\right).
$$

A price move caused partly by liquidity pressure is then interpreted as information about future volatility. The resulting higher margin reduces the capacity to absorb that pressure. Positive volatility persistence and imperfect inference together generate the feedback.

The result is conditional. A liquidity move that offsets fundamental news can reduce the absolute price move and lower the margin. Destabilizing means that margins **can** rise as illiquidity worsens, not that margins are globally increasing in every liquidity shock. At positive $a$, a sufficiently extreme drop can make a liquidity event likely even to an uninformed lender. Anticipated convergence then reintroduces the cushioning effect and changes the shape of demand.

The limiting $a\to0$ expression is therefore useful for transparent calculations, but it is not an exact substitute for the finite-$a$ Bayesian filtering problem. Since lenders' beliefs depend on equilibrium prices, choosing an equilibrium branch also changes their inference and hence the margin function.

## Fragility: existence of discontinuous price responses

For one security under selling pressure, let $b_0=W_0-p_0x_0$ denote the initial cash component. At a constrained time-one equilibrium,

$$
m_1^+(p_1)\left[Z_1+\frac{2(p_1-v_1)}{\gamma\sigma_2^2}\right]=b_0+p_1x_0+\eta_1.
$$

Define the left-hand funding need net of marked inventory and initial cash as

$$
G(p)=m_1^+(p)\left[Z_1+\frac{2(p-v_1)}{\gamma\sigma_2^2}\right]-px_0-b_0.
$$

Constrained prices solve $G(p)=\eta_1$, subject to position direction, capital feasibility, and the relevant price range. With slack financing, first check whether $p=v_1$ can be supported. Appendix B proves fragility by showing that $G$ can have a decreasing segment. A continuously varying wealth shock then cannot always be matched by a continuous choice of equilibrium price.

Two mechanisms can create that nonmonotonicity. Large preexisting long inventory causes falling prices to reduce wealth, represented by $-px_0$. Alternatively, a sufficiently strong destabilizing margin response can make required funding rise as prices fall, even when $x_0=0$. Proposition 4 establishes existence conditions with sufficiently large prior inventory or, for uninformed lenders, sufficiently strong volatility persistence and small sequential-arrival probability. It does not provide a universal numerical threshold applying to all assets.

The paper focuses on locally stable equilibria: a small downward price perturbation generates excess demand and a small upward perturbation generates excess supply. Finding an algebraic root is insufficient; an implementation must identify its stability. Multiple stable equilibria may coexist, separated by an unstable branch. The result concerns unavoidable jumps somewhere in the equilibrium correspondence as conditions vary, not a unique forecasting rule selecting exactly when a market jumps between branches.

## Numerical example and what can be reproduced directly

The single-security example uses baseline fundamental standard deviation 10, persistence coefficient $\theta=0.3$, prior price 130, customer endowment pressure $Z_1=30$, customer risk aversion $\gamma=0.05$, initial speculative inventory $x_0=0$, and capital 900 before the illustrated wealth shock. Financiers use $\pi=1$ percent, and the sequential-arrival probability is $a=1$ percent. Figure 3 sets current fundamental value to 120 and compares wealth shocks zero and $-150$.

With zero wealth shock, the finite-$a$ example has two stable equilibria: fundamental pricing at 120 and an illiquid price around 94. An unstable equilibrium lies just below 120. After the negative wealth shock, the liquid equilibrium disappears and only a highly illiquid equilibrium remains. The price near 94 is an illustrative graph-level result, not an empirical estimated fair value or an exact machine-precision number supplied by the authors.

A transparent reconstruction of the limiting case proceeds as follows. Fix $v_1$, compute $\sigma_2=10+0.3|v_1-v_0|$, and evaluate customer supply $30+2(p-v_1)/(0.05\sigma_2^2)$. Set $m(p)=2.326(10+0.3|p-130|)$, then compare feasible speculative demand to that supply. For prices below fundamental value, speculators optimally buy up to available wealth divided by margin; above fundamentals they short up to the corresponding bound. Search all admissible price intervals, including the kink at 130 and the indifference point at $v_1$, and classify the crossings by local excess-demand slopes.

This is an implementation procedure for the stated limiting model, not a claim to reproduce the finite-one-percent figures exactly. At $v_1=120$, the limiting margin is approximately 30.238, so financing all 30 shares requires about 907.14. Capital of 900 alone is slightly insufficient under that limiting formula. The source's finite-$a$ lender inference changes margins enough that its liquid equilibrium can exist. Conflating those two calculations would create an apparent contradiction.

Exact finite-$a$ figure replication additionally requires the full prior distributions relevant to lenders' inference, a consistent equilibrium-selection convention, numerical integration and root-search details, and tolerances. The article describes the economics and selected parameter values but does not provide source code or a complete numerical specification of all these choices. The time-zero informed-margin simulations are explicitly described as available from the authors rather than displayed in the article.

## The local multiplier and interacting spirals

For a stable, constrained equilibrium with customer selling pressure, Proposition 5 differentiates the funding equation:

$$
\frac{\partial p_1}{\partial\eta_1}=\frac{1}{\dfrac{2m_1^+}{\gamma\sigma_2^2}+\dfrac{\partial m_1^+}{\partial p_1}x_1-x_0}.
$$

The denominator is positive on the relevant stable branch. With constant margins and no initial inventory, the sensitivity is $\gamma\sigma_2^2/(2m_1^+)$. A negative dollar wealth shock reduces the number of shares that can be financed by $1/m_1^+$, and the two customer demand slopes translate that inventory reduction into a price change.

A negative margin derivative makes the second denominator term negative: falling prices increase margins on long positions. Positive initial inventory makes the final term negative: falling prices generate losses on positions already held. Both lower the denominator and magnify the effect of wealth shocks. Near a stability boundary the denominator can become small, so local responses become large before a discontinuity occurs.

The short-side formula differs in signs because greater capital lets speculators absorb customer buying by selling more:

$$
\frac{\partial p_1}{\partial\eta_1}=-\frac{1}{\dfrac{2m_1^-}{\gamma\sigma_2^2}+\dfrac{\partial m_1^-}{\partial p_1}x_1+x_0},\qquad x_1<0.
$$

A rising short margin with price can then destabilize the market. The economically relevant loss condition is inventory aligned with the endowment pressure, $x_0Z_1>0$: long inventory loses under customer selling, and short inventory loses under customer buying. “Opposite to demand pressure” in the prose refers to customers' desired trade direction, not the sign of $Z_1$.

The interaction is nonlinear because the total multiplier is the reciprocal of a denominator reduced by both mechanisms. The geometric-series interpretation in the paper treats successive feedback rounds as terms of that reciprocal expansion. It is a local equilibrium comparative static, not a literal claim that a discretely simulated adjustment path converges at a particular speed.

## Multiple assets, commonality, and flight to quality

In a multi-asset solution, the same $\phi_1$ prices scarce financing across all active positions. For positive customer selling pressure, Appendix B gives

$$
|\Lambda_1^j|=\min\left\{(\phi_1-1)m_1^{j,+},\;\frac{\gamma(\sigma_2^j)^2Z_1^j}{2}\right\}.
$$

The second term is the discount when speculators provide no intermediation and customers absorb the imbalance themselves. There is a symmetric expression using $-Z_1^j$ and short margins for buying pressure. Positions follow from market clearing, and the sum of their margin requirements must equal available capital when constrained. These equations yield a scalar-shadow-price approach to solving the multi-asset problem, with inner price–margin fixed points when margins depend on prices.

Proposition 6 proves commonality and flight-to-quality results under sufficiently small volatility-persistence parameters and, in the uninformed case, sufficiently small $a$. The proof begins with constant margins or the informed cushioning expression, where each asset's illiquidity is monotone in the common shadow value, and extends by continuity. These parameter qualifications matter; the theorem is not unrestricted for arbitrary nonlinear margin rules.

Jumps in the funding shadow value induce simultaneous illiquidity jumps for assets on which speculators are marginal. Higher-fundamental-volatility assets generally have larger margins, so they require larger pricing wedges per common unit of financing scarcity. The comparison requires either an active speculative position in the riskier asset or sufficiently large customer pressure in that asset, as specified in the proposition. An asset with negligible demand for intermediation need not become especially illiquid merely because its volatility is high.

The two-asset illustration changes baseline volatilities to 7.5 and 10 and doubles capital to 1,800, using the uninformed limiting case. Both assets have fundamental value 120. As financing deteriorates, both prices fall, but the higher-volatility asset falls farther on the illiquid branch. At very low financing, a position corner can arise in which remaining capital goes to the riskier asset because its customers offer a sufficiently large discount. This qualifies the shorthand that constrained dealers always allocate only to the safest asset: they maximize compensation per margin dollar, not minimize standalone volatility.

## Funding risk before the constraint binds

At time zero, a speculator anticipates that capital will be especially valuable at time one when financing is scarce. Under the paper's bankruptcy-cost treatment and with a currently slack constraint, the first-order condition is

$$
E_0[\phi_1(p_1^j-p_0^j)]=0.
$$

Thus

$$
p_0^j=E_0[p_1^j]+\frac{\operatorname{Cov}_0(\phi_1,p_1^j)}{E_0[\phi_1]}.
$$

The normalized future marginal value of capital is a pricing kernel. A position that loses money when capital becomes most valuable commands a discount today. Current spare financing therefore does not imply unlimited liquidity provision: the trader values preserving capacity for adverse future states. Appendix B extends the argument to a binding time-zero constraint by ranking funding-adjusted expected profits per margin dollar.

Figures 6 and 7 illustrate this precautionary effect. Current price is below both fundamental value 130 and the expected time-one price for the displayed unconstrained wealth levels. Under customer selling pressure, downside shocks trigger amplification while favorable shocks do not, giving negative conditional price skewness. The skewness is not monotone in initial wealth; Figure 7 approaches zero when funding is ample and is strongly negative in an intermediate region. Under customer buying, price skewness reverses sign, but speculative returns can remain negatively skewed because the positions are short. The distinction between price and trader-return skewness is necessary.

## Evidence, institutional interpretation, and research use

Figure 1 displays historical S&P 500 futures margin changes during several crises. Appendix A explains how repos, prime brokerage, derivatives margins, and regulatory capital can create constraints of the model's general form. It also explains important exceptions: cross-margining, multiple counterparties and legal entities, unsecured funding, committed versus revocable credit, and differing access to customer collateral. These are historical institutional descriptions in a 2008–2009 paper, not current regulatory guidance.

The historical examples support plausibility but do not identify the mechanism causally. A proper empirical test would seek shocks to intermediary capital unrelated to the affected asset's fundamentals, measure margin changes and market-liquidity responses, and test whether effects are nonlinear near funding constraints. It would also compare high- and low-margin assets and common intermediaries. The paper explicitly suggests such designs rather than claiming to have completed them.

For simulation, the most important checks are capital feasibility, market clearing, correct signs for long and short margins, classification of stable branches, and distinction between finite-$a$ inference and its limit. For risk management, the implication is that a static execution-cost estimate and a fixed leverage limit may omit a shared state variable: the cost of usable financing. The model supplies an economically coherent stress mechanism, but a production implementation needs independently calibrated margin dynamics, customer demand, funding availability, and equilibrium-selection assumptions. Its analytical conclusions do not determine those inputs for a particular portfolio.

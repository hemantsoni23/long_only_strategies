# Equilibrium Forward Curves for Commodities

Bryan R. Routledge, Duane J. Seppi, and Chester S. Spatt, *The Journal of Finance* 55(3), June 2000, pp. 1297–1338. [Source PDF](../../Finance/CommodityPrices_Routledge_2000.pdf). The supplied forty-two-page article includes the complete appendix and references. Journal page numbers equal PDF page numbers plus 1296.

## Why this matters

A physical commodity can be consumed now or stored for later. A forward contract conveys the right to receive it later and lacks the intervening consumption opportunity. When aggregate discretionary inventory is exhausted, that difference becomes valuable: physical ownership can command a high spot price even when expected future prices are lower. This paper derives forward curves from that storage option rather than specifying an independent convenience-yield process.

The main practical result is that the state of inventory changes the relationship among spot prices, forward curves, volatility, and hedge ratios. One exogenous demand shock plus endogenous inventory already creates two state variables and a stochastic convenience yield. A second, permanent multiplicative shock can move the entire curve without requiring a higher-dimensional storage optimization. This provides an economic account of temporary scarcity and persistent price-level shifts.

The paper combines equilibrium theory, a small numerical example, and a calibration to 1992–1996 oil futures. It explicitly presents calibration rather than a formal statistical test. The broad storage mechanism is useful, but several printed claims require qualification: eventual convergence of conditional forward-price variance does not by itself imply eventual monotonicity, and an explicit counterexample below falls within the stated assumptions. The numerical demonstration of inventory-related violations of the Samuelson effect remains a distinct, valid mechanism.

## Economic primitives and equilibrium

At each discrete date, immediate consumption $c_t(P_t)$, current production $g_t(P_t)$, and inventory traders clear a homogeneous commodity market. Let $Q_{t-1}$ be inventory entering the storage interval and $\delta$ the proportional physical loss per period. Current inventory change net of surviving stock is

$$
\Delta Q_t=Q_t-(1-\delta)Q_{t-1}.
$$

Market clearing is $c_t(P_t)-g_t(P_t)=-\Delta Q_t$. The resulting inverse net-demand function is

$$
P_t=f(a_t,\Delta Q_t).
$$

For every demand state, $f$ is positive, continuous, increasing in inventory accumulation, and unbounded above over its feasible domain. Accumulation withdraws the good from immediate use and raises its current marginal value. If production capacity is bounded, unbounded price can arise as accumulation approaches that capacity; the quantity domain need not itself be unbounded.

The transitory demand state $a_t$ follows an exogenous finite-state irreducible Markov chain with transition matrix $\Pi$, independent of inventory decisions. Some propositions additionally require every transition probability to be strictly positive, or an aperiodic finite-step analogue. Irreducibility alone does not eliminate periodicity. Seasonality can be represented by cyclic seasonal subsets, but then the limiting distribution and forward-price limit can depend on the season rather than being globally constant.

Inventory traders are competitive and risk neutral, face a constant risk-free rate $r\geq0$, and cannot hold negative aggregate discretionary stocks. The source allows $\delta\in(0,1]$; formulas dividing by $1-\delta$ require the interior case $\delta<1$. Define

$$
\theta=\frac{1-\delta}{1+r}.
$$

For $0<\delta<1$, $0<\theta<1$. Equilibrium conditions are

$$
Q_t\geq0,\qquad P_t\geq\theta E_t[P_{t+1}],\qquad Q_t\{P_t-\theta E_t[P_{t+1}]\}=0.
$$

The expectation is physical here because the inventory traders are risk neutral. A risk-averse extension would require a pricing-measure specification; the calibrated model does not estimate a commodity risk premium. The relevant inventory is discretionary stock available to traders, not all recorded physical inventories, some of which are committed to production or transit.

Write $J(a,q)$ for outgoing inventory and $P(a,q)$ for spot price given current shock $a$ and incoming inventory $q$. The equilibrium satisfies

$$
P(a,q)=f(a,J(a,q)-(1-\delta)q),
$$

with the complementarity condition above and next state $(a',J(a,q))$. The pair $(a_t,Q_{t-1})$ is Markov. Spot price alone generally is not a sufficient state: different combinations of scarcity and inventory can generate the same spot price but different forward curves.

## Existence, inventory monotonicity, and renewal

The appendix constructs the equilibrium as a limit of finite-horizon economies. At the terminal date inventory is zero because stored goods have no continuation value. Given the next-date policy, current positive inventory solves

$$
f(a,q^*-(1-\delta)q)=\theta\sum_{a'}\Pi_{aa'}f(a',J_{\mathrm{next}}(a',q^*)-(1-\delta)q^*).
$$

The left side increases with $q^*$, whereas the right side decreases under the inductively established inventory slope bound. A unique root, if positive, determines current inventory; otherwise the constraint selects zero. The construction establishes continuity and, in the interior depreciation case,

$$
0\leq J(a,q+\varepsilon)-J(a,q)<(1-\delta)\varepsilon.
$$

Extending the terminal horizon weakly increases inventory policies. A finite upper bound follows from the maximum price attainable without incoming inventory and the fact that holding costs prevent buying above the highest possible future sale price. Monotone limits yield the stationary policy. Proposition 1 states existence and policy properties; its reference to a unique upper bound should not be expanded into an unqualified global uniqueness theorem for every conceivable equilibrium outside the constructed class.

For each demand state, solve $\widehat Q_a=J(a,\widehat Q_a)$; the slope bound gives a unique crossing of the 45-degree line when inventory at zero is positive. The maximum of these crossings is an invariant upper inventory bound $Q_{\max}$. Spot prices are positive, finite, continuous, and decreasing in incoming inventory on the relevant compact state domain.

The source identifies sell states and proves recurrent stockouts. If positive inventory could persist without any chance of a stockout, repeatedly substituting the equality condition would make a positive bounded spot price equal to $\theta^n$ times a bounded expected future price for arbitrarily large $n$, a contradiction. With the finite-state/recurrent structure, stockouts reset the inventory component, removing dependence on ancient inventory history. Under the stronger mixing assumption on $\Pi$, there is an invariant joint distribution independent of the initial state.

An inventory perturbation has a particularly useful pathwise interpretation. Couple two economies to exactly the same demand-shock sequence and add $x>0$ to one economy's initial inventory. Then

$$
0\leq Q_t^x-Q_t<(1-\delta)^t x.
$$

The perturbed economy has weakly lower spot and forward prices. When the higher-inventory path stocks out, both paths have zero inventory and thereafter coincide. The appendix states the latter condition correctly; it is the stockout of the higher path that guarantees coupling, not merely a stockout of the lower path. Prices of increasing European payoffs also decrease with initial inventory under this coupling. No corresponding claim is made for arbitrary nonmonotone derivatives.

## Forward pricing, ordering, and curve shape

With risk neutrality and deterministic rates,

$$
F_t(t+n)=E[P_{t+n}\mid a_t,Q_{t-1}].
$$

This is a delivery price paid at maturity, so it is not discounted at inception. Financing and wastage affect it through equilibrium storage and future spot prices. Once $J$ is known, define a transition operator

$$
(\mathcal K h)(a,q)=\sum_{a'}\Pi_{aa'}h(a',J(a,q)).
$$

Then $F_n=\mathcal K^n P$. This supplies a direct computational route from the inventory policy to every forward tenor and, after discounting the appropriate payoff, to European derivatives.

Under mixing, forward prices converge to the invariant mean spot price $F_\infty$, independent of current inventory and demand. The paper gives upper and lower bounds that tighten with maturity. The limiting mean need not move monotonically with storage cost: more wastage reduces available consumption, but high wastage also discourages inventory and can reduce total lost stock. Even linear inverse demand does not remove that tradeoff.

To order prices across demand states, the paper adds two assumptions: inverse net-demand curves are ordered at every inventory change, and transitions from higher demand states first-order stochastically dominate those from lower states. Proposition 4 then states that spot and forward curves preserve that ordering. Ordering current demand alone is insufficient in a multistate model, since a currently low state might strongly predict very high future demand and trigger storage demand. In a symmetric two-state chain, persistence probabilities above one half deliver the stochastic ordering used in the example. More generally, the two-state condition is $p_{HH}+p_{LL}>1$, not necessarily that each probability separately exceeds one half.

For a binomial conditional shock process, a bond and a one-period forward span the two next-period outcomes if their spot payoffs differ. The proof uses ordered next-state spot prices to make the payoff matrix invertible. This gives dynamic completeness despite the inability to short physical inventory at a stockout. It does not automatically extend to a general multistate chain, where path-dependent inventory makes spanning across all reachable states a substantive condition.

Define the scaled adjacent-tenor slope and implied one-period convenience yield by

$$
s_{t,n}=\frac{F_t(t+n+1)-F_t(t+n)}{F_t(t+n)},\qquad y_{t,n}=1-\theta\frac{F_t(t+n+1)}{F_t(t+n)}.
$$

The carry inequality implies $s_{t,n}\leq\theta^{-1}-1=(r+\delta)/(1-\delta)$ and $0\leq y_{t,n}<1$. If inventory is strictly positive throughout the relevant future interval in every reachable state, repeated carry equalities give $F_t(t+n)=\theta^{-n}P_t$. Otherwise anticipated scarcity reduces the curve below this maximum-carry path. Under the stationary mixing conditions, the long-tenor slope tends to zero and the convenience yield tends to $1-\theta=(r+\delta)/(1+r)$.

A precise formulation avoids overstating the source's “if and only if stockout” language. Let $L_s=P_s-\theta E_s[P_{s+1}]\geq0$ denote carry slack. Then

$$
y_{t,n}=\frac{E_t[L_{t+n}]}{E_t[P_{t+n}]}.
$$

Convenience yield is positive exactly when positive carry slack has positive conditional probability. Positive slack requires zero inventory, but zero inventory at an indifference boundary can coexist with zero slack. The source's equivalence between positive stockout probability and positive yield is therefore naturally read for strict, value-bearing stockouts, excluding ties. In particular, backwardation here refers to the contemporaneous delivery-price curve, not Keynesian compensation for bearing a futures risk premium.

## Numerical illustration and the conditional Samuelson effect

The baseline example has two demand states $a_H=1$, $a_L=0$, symmetric staying probability .75, linear inverse net demand $f(a,\Delta Q)=a+\Delta Q$, $r=0$, and $\delta=.1$. The linear example is interpreted on its relevant equilibrium domain; a linear function with zero intercept is not globally positive over all hypothetical inventory changes. The calculated equilibrium nonetheless has positive prices and nonnegative inventory. Inventory accumulates in the low state and is consumed in the high state.

The authors approximate $J$ by piecewise-linear interpolation on 1,000 equally spaced inventory points. Fixed-point iterations typically require 20–50 updates to the stated numerical tolerance, whose value is not supplied. They later use a third-order polynomial approximation to accelerate calibration. A full shock tree is nonrecombining because the order of high and low shocks affects inventory. A sparse transition matrix over demand states and inventory grid avoids exponential enumeration. Figure 2 uses 100 specially chosen inventory points and plots sixty common forward curves; the precise grid-selection rule is not supplied.

The figures show upward curves in low-demand states, downward curves after severe high-demand stockouts, and hump-shaped curves with high demand but enough inherited inventory to postpone a shortage. Runs of low demand move the hump farther out. In the two-state example all stockouts occur in the high state and have identical outgoing inventory, so forward prices after a stockout coincide even though current spot prices differ with incoming inventory. This creates the visible fan between the different spot prices and the common next-delivery price.

For a binary next shock with probability $p$, the conditional level-price variance at a given tenor is

$$
p(1-p)\{F_n(a_H,q)-F_n(a_L,q)\}^2.
$$

Thus the high-minus-low dispersion plotted in Figure 5 ranks conditional variances in this example. At low inventory, short-horizon dispersion is greatest. At high inventory, storage buffers spot consumption value, while more distant prices scale up at the carry rate until stockout risk becomes relevant. If both next-date states remain in the no-stockout region for the pertinent horizon, $F_n=\theta^{-n}P$ implies larger *level* variance at longer nearby tenors. This is not a statement that percentage-return volatility rises by the same factor.

Figure 5 shows the four-period dispersion overtaking the one-period dispersion when inventory exceeds roughly half the endogenous maximum, while the eight-period dispersion remains lower. Figure 7 shows the corresponding four-period hedge ratio exceeding one above inventory approximately .99. These are numerical results of the baseline example. The mechanism requires enough inventory and a horizon over which storage equalities apply in the relevant states; it does not exist in every economy with prohibitively costly storage.

## A limit to the general volatility proposition

Proposition 8(a), p. 1316, claims that conditional forward-price variance eventually decreases monotonically with maturity for every strictly positive transition matrix. Its appendix proof on p. 1336 appeals to shrinking forward-price bounds and convergence to $F_\infty$. Those facts imply variance converges to zero, but do not imply it becomes monotone.

The distinction is material, and an explicit counterexample can be constructed within the stated primitive assumptions. Set $r=0$, $\delta=.95$, demand-state values $(1,2,10)$, and $f(a,\Delta Q)=a\exp(\Delta Q)$. This function is positive, increasing, continuous, and unbounded. Let

$$
\Pi=\begin{pmatrix}.01&.98&.01\\.01&.01&.98\\.98&.01&.01\end{pmatrix}=.01\mathbf1\mathbf1'+.97C,
$$

where $C$ cyclically permutes the three states. Every transition probability is positive. Starting with zero inventory, no storage is optimal: the maximum possible discounted surviving-unit sale value is at most $.05\times10=.5$, below the minimum current spot price 1. Thus spot prices are $p=(1,2,10)'$ and $n$-period forward prices are $\Pi^np$.

Conditional on the current first state, the variance of the next-date $n$-period forward is $\operatorname{Var}_{\Pi_{1,\cdot}}[(\Pi^np)_{a_{t+1}}]$. For $n=0,1,2,3,4,5$ the values are approximately .645100, 1.337113, .717087, .537350, 1.113778, and .597314. Since the nonconstant component rotates by $C$ and contracts by .97 at each step, the variance sequence repeats its three-tenor pattern scaled by $.97^6$. It rises from $n=3k$ to $n=3k+1$ for every $k$, while still tending to zero. No finite maturity makes it permanently decreasing.

This is a derived counterexample to the general eventual-monotonicity assertion, not a reported experiment in the article. It uses an interior depreciation rate and does not require the singular $\delta=1$ boundary. It does not satisfy the additional demand-state stochastic-order restriction, but Proposition 8 states only strict positivity of $\Pi$, not that extra restriction. The paper's persistent symmetric two-state example and its inventory-induced local reversal mechanism remain separately interpretable. A robust implementation should compute the entire conditional variance curve rather than enforce a universal monotone tail solely from mixing.

## State-dependent forward hedges

Suppose a long-dated forward delivering at $T$ is hedged using a shorter forward delivering at $\tau<T$ and a bond. Across two next-date states, let $\Delta F_T$ and $\Delta F_\tau$ denote the high-minus-low forward-price changes. Matching marked-to-market values gives the number of short contracts per long exposure as

$$
h=\frac{\Delta F_T}{\Delta F_\tau}(1+r)^{\tau-T}.
$$

The discount factor accounts for distinct delivery cash-flow dates. It should not be dropped except when rates are zero or a deliberately different settlement convention is modeled. Under the ordering conditions the ratio is positive, but its size depends on inventory and current demand. It can exceed one for intermediate horizons with high inventory and becomes small for sufficiently remote maturities in the basic stationary model as far-forward state dependence vanishes.

The model demonstrates a source of hedge-ratio variation, not an empirical backtest of a rolling hedge. Margin calls, liquidity, transaction costs, financing constraints, bid–ask spreads, and discrete contract replacement are not included. Dynamic completeness in an ideal binomial model does not remove these implementation risks.

## Oil calibration: exact target construction

The empirical exercise uses daily NYMEX light sweet crude-oil futures prices over 1992–1996, after the Gulf War. Contracts are sorted by delivery rank: “one month” is the nearest delivery and “ten months” the tenth, chosen for liquidity and availability. These are nearby ranks, not exact constant-calendar-maturity interpolated contracts. Spot prices are not available. The article does not list exact start/end trading dates, sample counts, roll filters, quote times, or contract-level missing-data exclusions.

Conditional moments at date $t$ use the curve shape twenty trading days earlier. Backwardation is determined by the sixth-nearby minus first-nearby price being negative; contango uses a positive difference. Thus current prices are conditioned on a lagged classification, avoiding the different estimand produced by conditioning on today's slope. Means and standard deviations are computed for price *levels*, in dollars, not log returns or annualized return volatility.

The one-factor calibration uses $f(a,\Delta Q)=(a+\Delta Q)^\alpha$. A two-state Markov chain approximates a Gaussian AR(1) demand process using Tauchen–Hussey discretization. The intended parameters are unconditional mean $\mu_A$, standard deviation $\sigma_A$, and autocorrelation $\rho_A$. Equation (13) prints innovation scale $\sqrt{1-\rho_A}\sigma_A$, while the next sentence calls $\sigma_A^2$ the unconditional variance. Those two statements are inconsistent: the printed recursion has variance $\sigma_A^2/(1+\rho_A)$. To implement the stated unconditional-variance parameterization, the innovation scale must instead be $\sqrt{1-\rho_A^2}\sigma_A$. The supplied article does not establish which convention the original code used; the table should not be silently reinterpreted as proof of either implementation.

The objective gives equal numerical weight to sixty moment discrepancies:

$$
\min_{\mu_A,\sigma_A^2,\rho_A,\alpha}\sum_{v\in\{U,B,C\}}\sum_{n=1}^{10}\left[(\widehat m_n(v)-m_n(v))^2+(\widehat s_n(v)-s_n(v))^2\right].
$$

Here $U$ is unconditional, and $B,C$ refer to the lagged curve classification. Model moments come from the invariant distribution and its one-period transitions. A transparent calculation of a conditional expectation is $E[g(X_{t+1})1_{B(X_t)}]/\Pr(B(X_t))$ under that distribution. This uses the same lag as the empirical twenty-day classification, with one model period interpreted as a month.

The rate is fixed at $.04/12$ monthly and physical storage loss at .0025 monthly. The authors choose the latter after preliminary exploration, partly to avoid numerical difficulty at extremely low storage costs; it is not an independently measured oil-storage expense. They temporarily replace the exponent by one if candidate nonequilibrium policies produce a nonpositive power base, and report that this safeguard does not bind in the final equilibrium. No standard errors, optimal moment-weighting matrix, parameter-confidence intervals, or holdout performance are reported.

## Permanent augmentation and normalized calibration

To preserve the solved storage policy while permitting persistent level changes, multiply inverse demand by $b_t>0$:

$$
f^*(a_t,b_t,\Delta Q_t)=b_tf(a_t,\Delta Q_t).
$$

The source states a factorization condition on conditional expected future values. Its concrete calibration uses independent multiplicative innovations

$$
\log(b_{t+1}/b_t)\sim N(-\tfrac12\sigma_b^2,\sigma_b^2),
$$

so $E_t[b_{t+1}]=b_t$. Independence from the transitory shock process makes the pricing factorization valid for the state-dependent equilibrium continuation payoff, yielding $J^*=J$, $P_t^*=b_tP_t$, and $F_t^*(t+n)=b_tF_t(t+n)$. A condition checked only for a fixed deterministic inventory change would not by itself justify factorization for every state-dependent policy payoff; the independent-factor specification is sufficient and is the one used here.

All scaled curve slopes and implied convenience yields are preserved, while raw price levels become nonstationary. The model's forward-price ratios eliminate $b_t$ exactly. The authors therefore normalize both model and empirical curves by the contemporaneous tenth-nearby price and rescale by its sample mean:

$$
\widetilde F_t(t+n)=\frac{F_t(t+n)}{F_t(t+10)}\operatorname{mean}[F_t(t+10)].
$$

They fit the same sixty-moment objective to these normalized prices. In a second step they choose permanent-factor volatility to match the unconditional volatility of raw tenth-nearby log returns, and choose the initial factor level to match price levels. The tenth contract is used as a proxy for the far-forward level, not established to be an exact permanent factor. Normalized tenth-contract variance is mechanically zero, so convergence of fitted normalized volatilities at tenor ten is partly a normalization identity. The article does not report numerical $\sigma_b$ or $b_0$, preventing a complete reconstruction of the raw augmented price process.

A separate additive augmentation is discussed in footnote 26. A nonnegative factor with $E_t[b'_{t+1}]=\theta^{-1}b'_t$ preserves inventory and adds $\theta^{-n}b'_t$ to each forward. Its positive expected growth differs from the multiplicative martingale construction. The two can be combined, but that three-factor extension is not calibrated in this paper.

## Numerical results, diagnostics, and remaining gaps

Table I gives basic-model parameters $\mu_A=16.1992$, $\sigma_A=6.9988$, $\rho_A=.6370$, and $\alpha=1.0092$. The augmented model's transitory component uses 17.7732, 9.8742, .2462, and 1.0172. Both retain the same fixed financing and storage rates. The fitted curvature is nearly linear; adding a permanent level factor sharply reduces required transitory persistence.

The raw basic model fits unconditional level-volatility decay well in Figure 8, but fails the conditional comparison: backwardation-conditioned model standard deviations are much too low and ordered incorrectly relative to contango. Figures 9–10 compare normalized augmented and basic results. The augmented model substantially improves unconditional and contango volatility fits and improves backwardation volatility, though it still misses portions of the curve. Exact means and standard deviations by maturity are plotted rather than tabulated, so a full numerical target vector cannot be recovered to machine precision from the article.

The diagnostics not included in the calibration objective are revealing:

| Diagnostic | Data | Basic model | Augmented model |
|---|---:|---:|---:|
| Backwardation frequency | 59.81% | 32.00% | 30.75% |
| Hump starting at first forward | 19.03% | 3.02% | 8.31% |
| Normalized first-forward skewness | .773 | .784 | .868 |
| Normalized first-forward excess kurtosis | .566 | −1.253 | .025 |
| Unconditional model inventory mean | Not observed | 21.981 | 18.855 |
| Inventory mean after backwardation | Not observed | .969 | 4.224 |
| Inventory standard deviation after backwardation | Not observed | 1.753 | 3.744 |

A hump starting at the first forward means $F_1<F_2$ and $F_2>F_3$; it is not the same as a hump between spot and the first two forwards. The latter frequencies are 4.44 percent and 13.34 percent for the two models, with no empirical spot comparison available. Inventory units are model demand units, not observed barrels. With a linear unit slope, dumping one additional unit reduces price by one dollar; near-linear fitted curvature makes that only an approximate local interpretation for the calibrated specifications.

Unconditional inventory standard deviations are 17.102 in the basic model and 12.457 in the augmented model. Conditional inventory means after contango are 31.870 and 25.350, with standard deviations 11.096 and 8.979. These are implied latent quantities, not validation against measured physical stocks. The augmented model still produces backwardation only about half as often as the data, helping explain its understated unconditional mean curve despite improved conditional fits. Its two-point transitory shock distribution also limits tail flexibility.

One raw-data pair in Table I is internally suspect. The unscaled empirical skewness is printed as 6.199 and kurtosis as 1.792. Since negative entries elsewhere make clear that the kurtosis row uses excess kurtosis, conventional standardized moments must satisfy excess kurtosis at least skewness squared minus two. Here that lower bound is 36.427601, far above 1.792. The supplied printing therefore cannot be treated as a consistent pair of conventional third/fourth standardized moments. No corrected digit is inferred; the normalized diagnostics and other reported values are recorded separately.

The economic contribution survives these qualifications: inventory endogenizes temporary scarcity, convenience yield, and maturity-dependent hedge exposure; a separable permanent factor explains why long-forward levels can remain volatile. Reimplementation requires contract data, an explicit discretization convention for the AR process, inventory-grid or polynomial details, numerical tolerances, the missing permanent-factor calibration, and care with the distinction between conditional level dispersion and return volatility. The supplied evidence does not establish out-of-sample derivative-pricing accuracy, executable hedging profits, or a universally monotone volatility term structure.

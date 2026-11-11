# Speculation and the Carryover

John Burr Williams, *The Quarterly Journal of Economics* 50(3), May 1936, 436–455. JSTOR stable identifier: 1882611.

Source: [MeanVariance_Williams_1936.pdf](../../Finance/MeanVariance_Williams_1936.pdf). Despite the filename, the article primarily develops a commodity storage and intertemporal price model. The final probability discussion concerns geometric growth under repeated reinvestment. The PDF has a JSTOR cover followed by the twenty article pages; references below use printed pages.

## Why this matters

A bumper crop need not be consumed entirely before the next harvest. When the commodity can be stored, speculators can buy part of today's surplus and sell it against future production. Their purchases raise the current price; their later sales lower future prices and discourage future production. The equilibrium carryover must account for all three responses: current consumption, future consumption, and future supply. Looking only at the current demand curve or at an unchanged expected future price misses the market feedback from storage itself.

Williams's contribution is an explicit system of equations tying inventories, supply, demand, and carrying charges across years. He describes how to solve for both the amount stored and the duration of liquidation, then extends the mechanism to anticipated shifts in demand. The concluding note adds uncertainty about harvests and argues for a geometric-mean representative price when traders repeatedly reinvest their entire capital.

The paper is theoretical and diagrammatic. Its cotton quantities, price examples, and 10% carrying rate are illustrations, not fitted structural estimates or results from a documented backtest. A useful modern reproduction therefore reconstructs the equilibrium equations and numerical solution procedure while distinguishing Williams's assumptions about risk and expectations from conclusions that actually follow from the accounting identities.

## The market, timing, and objects

The opening example begins in December of a crop year with enough cotton to satisfy demand until the next harvest but no speculative stock intended for the following crop year. Dealers and mills may still hold working stocks to avoid delivery delays and production stoppages. Williams explicitly separates those operational stocks from carryover held because of an anticipated price increase.

Traders may already deal in a new-crop October futures contract ten months ahead. The prospective price influences planting acreage and fertilizer use before harvest. Weather then determines the realized yield. Thus the quantity supplied at a planting price is a distribution, not a known point. Expected demand is described by quantities consumers would purchase at different prices, conditional on the business conditions traders anticipate.

Use the following notation, simplifying the article's primes and subscripts. Let $f(c)$ be inverse demand: the price that clears consumption quantity $c$. Let $\phi(q)$ be inverse expected supply: the planting or supply price associated with expected production $q$. Where inverses exist, write

$$
D(p)=f^{-1}(p),\qquad S(p)=\phi^{-1}(p).
$$

Demand is decreasing and supply increasing in the diagrams. The paper does not specify functional forms, slopes, or estimated elasticities for numerical application. Let $q_0$ be the realized current bumper crop, and let $i>0$ be the proportional annual carrying charge. It includes interest, taxes, storage, insurance, and spoilage in one effective rate. The illustrative rate is 10% of purchase price per year.

For a constant carrying rate, moving one unit of commodity from a date with price $p_t$ to the next year requires a gross sale price $(1+i)p_t$ to cover cost. Two years require multiplication by $(1+i)^2$, not addition of just $2i$ to the original price. This proportional-cost representation is the source's simplification; it is not a separate explicit physical decay equation, warehouse-capacity constraint, or convenience-yield model.

The stable no-carryover benchmark is the intersection

$$
D(p_u)=S(p_u),
$$

where $p_u$ is the eventual price once the original surplus has been liquidated and future supply and demand conditions have returned to their assumed stationary pattern.

## Uncertain supply and the meaning of the supply curve

Charts 1 and 2, pp. 439–440, describe a family of crop distributions indexed by the planting price. If $Q\mid s$ is the future crop given supply price $s$, the density can be written $\varphi(q\mid s)$. The expected-supply schedule is

$$
S(s)=\int q\,\varphi(q\mid s)\,dq.
$$

The supply curve therefore passes through conditional means, not necessarily modes. In the cotton illustration, ordinary weather gives a modal crop around 15 million bales, while unfavorable weather is assumed to reduce yields more than favorable weather can increase them. The resulting distribution has a left tail and a mean below its mode. A quantity of 14.5 million bales appears as an expected-crop illustration.

This is an assumed asymmetry in the example, not an empirically estimated probability law. The article does not give a normalized density, a support, a variance, or a time series from which to estimate it. Each new crop is described as information that could improve the trader's rough understanding of the distribution. Nor is the location of the mode above the mean sufficient by itself to determine the probability of exceeding a particular stockout or storage threshold.

If a short crop occurs when speculative carryover is zero, inventories cannot be released to cushion consumption. Williams's example has realized production of 13 million bales against 14.5 million expected. The price must rise along the demand curve until consumption falls to the available quantity. A bumper crop has a different response because storage can absorb part of the excess. This asymmetry between stockouts and positive inventory is central to the model.

## One-year carryover equilibrium

Let $I\ge0$ be the quantity taken from the current crop for sale next year. Current consumption is $q_0-I$, next year's production is $q_1$, and next year's consumption is $q_1+I$. For an interior one-year storage episode, pp. 443–444 give four equations for four unknowns:

$$
p_0=f(q_0-I),
$$

$$
p_1=f(q_1+I),
$$

$$
p_1=\phi(q_1),
$$

$$
p_1=(1+i)p_0.
$$

The unknowns are $p_0,p_1,q_1,I$; current crop $q_0$, carrying rate, and the curves are inputs. The third equation is the production response. It prevents a solver from treating next year's crop as unchanged when the future price falls because of inventory liquidation.

Competition supplies the fourth equation. Adding more inventory raises the current purchase price and lowers the future sale price. The net gain per unit, after carry, is $p_1-(1+i)p_0$. Entry and expansion of storage eliminate that residual in the interior equilibrium. The price spread still covers carrying expenses; zero residual profit does not mean zero gross price increase or free warehousing.

A single scalar equation makes the system readily implementable. For a trial current price $p$,

$$
I=q_0-D(p),\qquad
q_1=S((1+i)p).
$$

Clear next year's market by solving

$$
F(p)=D((1+i)p)-S((1+i)p)-q_0+D(p)=0.
$$

With strictly decreasing demand and increasing supply, this residual is decreasing where the curves are defined, providing a natural bracketed root-finding problem. After solving, verify $I\ge0$, all quantities are in their domains, and no additional year of storage would improve the outcome. The article advocates successive approximation and a graphical equivalent rather than specifying a particular numerical root solver or tolerance.

Williams illustrates why equalizing consumption across years can store too much. If the current crop is 16.5 million bales and the next crop is provisionally 14.5 million, carrying 1 million bales would give 15.5 million available for consumption in both years. Under unchanged demand curves, prices would be equal, leaving no spread to pay storage. Carrying only 0.5 million would instead leave 16 million for current consumption and 15 million next year, allowing a positive price difference. These quantities explain the direction of adjustment; they do not solve the full four-equation model because next year's production must respond too.

## Several years of liquidation

A sufficiently large bumper crop can require sales over multiple later harvests. Let the active episode include dates $0,1,\ldots,n-1$. Let $I_0$ be accumulation at date zero and $\ell_t\ge0$ the release from the original stock at later date $t$. For the stationary expected-curve case, Williams's equations on pp. 446–447 become

$$
p_0=f(q_0-I_0),
$$

$$
p_t=f(q_t+\ell_t),\qquad p_t=\phi(q_t),
\quad t=1,\ldots,n-1,
$$

$$
p_t=(1+i)p_{t-1},\quad t=1,\ldots,n-1,
$$

$$
I_0=\sum_{t=1}^{n-1}\ell_t.
$$

There are $3n-1$ unknowns: $n$ prices, $n-1$ future production quantities, and $n$ accumulation or liquidation amounts. There are equally many equations. In this indexing, a one-year hold from date zero to date one corresponds to $n=2$ active dates, a distinction worth preserving when interpreting “years” in the prose.

For fixed $n$, eliminate the intermediate variables:

$$
p_t=p_0(1+i)^t,\qquad
\ell_t=D(p_t)-S(p_t),
$$

$$
q_0-D(p_0)=\sum_{t=1}^{n-1}
\left[D(p_0(1+i)^t)-S(p_0(1+i)^t)\right].
$$

This is the scalar balance equation behind the graphical procedure of shifting a band of horizontal price lines. The lines are equally spaced proportionally, because the carrying charge is a percentage, rather than equally spaced in price units. Their horizontal intercepts between demand and supply curves give annual releases. Initial accumulation must equal the sum of those releases.

A solver should also reconstruct remaining inventory after every release and verify that it never becomes negative. In this particular single-accumulation episode, nonnegative releases and the total balance ensure that property. In a model allowing later accumulation as well, cumulative stock constraints must be checked explicitly; total purchases equaling total sales is not enough.

## Determining the terminal date and checking the boundary

The last liquidation price must be close enough to the ultimate equilibrium price that extending storage one further year is not profitable. The source discusses the condition that $p_{n-1}$ lie between $p_u/(1+i)$ and $p_u$. Below the lower endpoint, another year at the ultimate price covers carry and leaves a gain. Above the upper endpoint, the proposed liquidation price is inconsistent with the stationary demand–supply clearing benchmark and nonnegative release.

Using $p_{n-1}=p_0(1+i)^{n-1}$ yields a logarithmic interval of length one for the admissible integer $n$. Page 449 is inconsistent about strict and weak inequalities and prints both final bounds as strict while claiming a unique integer always lies between them. At an integer boundary, an open interval of length one contains no integer. A reconstruction should therefore use the economic no-profitable-extension and nonnegative-release conditions directly, allowing endpoint indifference and choosing a documented minimal active horizon when an extra zero-release year would merely relabel the same solution.

For example, under a convention that omits a terminal date with zero release, impose

$$
\frac{p_u}{1+i}\le p_{n-1}<p_u.
$$

If $a=\log(p_u/p_0)/\log(1+i)$, this corresponds to $a\le n<a+1$. A different convention can include an indifferent zero-release endpoint without changing economic flows. The initial price is endogenous and changes with the candidate horizon, so computing $n$ once from an arbitrary guessed $p_0$ is not a complete solution.

A practical algorithm enumerates candidate horizons, solves the scalar stock-balance equation for each, and retains one satisfying all positivity, inventory, and terminal conditions. The source provides neither convergence tolerances nor a proof of global numerical convergence for arbitrary supply and demand curves. Monotonic curves and a feasible bracket make the scalar formulation much easier to control than solving all $3n-1$ equations blindly.

## An explicit numerical reconstruction

The following example is constructed for this note to test the equations; it is not Williams's cotton calibration. Use quantities in millions of units, prices in consistent arbitrary units, $D(p)=20-p$, $S(p)=p$, $q_0=14$, and $i=0.10$. The stationary price is $p_u=10$.

Trying only one year of storage gives $p_0=8.125$ and $p_1=8.9375$. Although the two-date stock balance holds, $p_1<10/1.1\approx9.0909$, so the terminal condition fails: holding part of the stock another year is worthwhile.

With active dates 0, 1, and 2, the balance is

$$
p_0-6=(20-2.2p_0)+(20-2.42p_0),
$$

so $p_0=46/5.62\approx8.185053$, $p_1\approx9.003559$, and $p_2\approx9.903915$. Initial accumulation is approximately 2.185053 million units. Releases are approximately 1.992883 and 0.192171 million, whose sum matches accumulation to rounding. Production in the two later dates is $q_1=p_1$ and $q_2=p_2$ under the chosen supply curve. The last price lies between 9.0909 and 10, so the terminal condition is satisfied.

This example tests an important implementation distinction: solving the accounting equations for a proposed horizon is necessary but not sufficient. One must also test whether that horizon is consistent with the opportunity to extend storage. It also shows why future production belongs inside the equilibrium calculation: it changes at each price on the liquidation path.

## Seasonal prices and anticipated demand changes

Chart 5 on p. 448 depicts rising prices during liquidation and a seasonal sawtooth once the original surplus has disappeared. Within a normal crop year, a stored unit must earn its intra-year carrying charge. At the next harvest, newly available output has not yet incurred those storage costs, producing a downward seasonal reset in the diagram. Larger carrying costs imply a larger intra-year rise, other assumptions held fixed.

This is a conditional theoretical price path, not a forecast that commodity futures always rise smoothly with maturity. Williams himself notes a July 1935 configuration in which near cotton contracts traded above distant ones despite a large carryover, attributing it to government loans supporting spot cotton at 12 cents per pound. The example signals that policy can break the unconstrained competitive-storage mechanism. The article does not estimate the policy effect or provide a term-structure dataset.

Part II, pp. 450–452, considers improving business conditions and thus outward-moving demand curves. Traders accumulate in early low-demand years and release in later high-demand years. Chart 6 uses 1935–1936 for accumulation and 1937–1938 for liquidation. Storage raises early prices, reducing early consumption and inducing more early production; later releases lower prices, increase consumption, and reduce later production relative to the no-storage counterfactual.

With time-varying demand, one can write a transparent accounting reconstruction using $D_t(p)$ and supply $S_t(p)$. Net inventory acquisition at date $t$ is $S_t(p_t)-D_t(p_t)$. During an interior episode with positive carried stocks, successive prices cover carrying charges, while initial and terminal inventories and all intermediate nonnegativity conditions determine feasibility. Total net acquisitions over a closed episode sum to zero. This notation extends the paper's diagram into a reproducible system; the source does not formulate a general stochastic dynamic program with state-contingent policies.

The article interprets this movement of goods through time as beneficial smoothing. It does not calculate a formal welfare surplus, specify heterogeneous consumer preferences, or prove a general welfare theorem allowing market power, constraints, externalities, and uncertain beliefs. Its welfare language should be read in the context of the competitive diagrams and correct anticipated conditions.

## The probability note and geometric reinvestment

Pages 452–455 revisit uncertain harvests. Williams separates potentially valuable information about current crops or future demand from attempts to predict weather assumed to be pure chance. His representative-price argument then assumes a trader repeatedly commits capital plus accumulated gains or losses to successive trades.

If every purchase is made at price $P$ and successive resale prices are $P_1,\ldots,P_N$, ignoring carrying expenses for this algebraic step, capital evolves as

$$
C_N=C_0\prod_{j=1}^{N}\frac{P_j}{P}.
$$

Setting final capital equal to initial capital gives the pathwise break-even purchase price

$$
P=\left(\prod_{j=1}^{N}P_j\right)^{1/N}.
$$

The article therefore uses a geometric representative resale price for a trader who reinvests sequentially. In a probability formulation with positive resale price and integrable logarithm, the corresponding population quantity is

$$
P_G=\exp(E[\log P_1]).
$$

Under additional frequency or ergodic assumptions, average log returns converge to $E[\log P_1]-\log P$. These assumptions make explicit the bridge from Williams's finite product to a probabilistic long-run statement. They are not a guarantee that a finite sequence of trades ends with unchanged capital, nor do they remove drawdown or ruin risk.

The geometric criterion is also not the same as zero expected arithmetic profit. For nonconstant positive prices, Jensen's inequality gives $P_G\le E[P_1]$. A purchase at the geometric mean can have positive expected arithmetic gain while having zero long-run log-growth rate before carry. Treating the two means as interchangeable would erase the central distinction in the appendix.

The paper does not optimize a fraction of capital allocated to the trade, add a cash asset, or solve a modern leverage-constrained growth-optimal portfolio problem. Full sequential reinvestment is an assumption of the illustrative argument. Calling this a complete Kelly allocation rule would add a decision variable and optimization problem absent from the source.

## Reconstructing the uncertain one-year equilibrium

Williams gives six steps for the uncertain one-year case. Let $I$ be current accumulation and $p_0=f(q_0-I)$. Set the next-period supply price $s_1=(1+i)p_0$. That supply price selects the crop distribution $Q_1\mid s_1$ from the family of conditional yield laws. Consumption next year is $A_1=Q_1+I$, so the random demand-clearing price is $P_1=f(A_1)$. The geometric representative of that price must equal the supply price:

$$
\exp\left(E\left[\log f(Q_1+I)\mid s_1\right]\right)=s_1,
\qquad s_1=(1+i)f(q_0-I).
$$

In terms of a supplied conditional density, the root condition is

$$
\int\log f(q+I)\,\varphi(q\mid s_1)\,dq-\log s_1=0.
$$

This is a direct computational rendering of pp. 454–455. It makes the feedback explicit: changing inventory changes today's price, which changes next year's supply price, which changes the distribution of next year's crop, which changes the distribution of consumption and resale prices. Holding that conditional crop distribution fixed while solving for inventory would omit part of the source's mechanism.

A numerical implementation would bracket feasible $I\in[0,q_0]$, evaluate the induced supply price, integrate the log-price over the corresponding crop law, and solve for a zero residual. It must check positive prices, log integrability, and the applicability of one-year liquidation. The source supplies no conditional density parameters, integration nodes, convergence tolerance, or calibrated curves, so an exact numerical cotton equilibrium cannot be reproduced from this article alone.

For constant-elasticity inverse demand,

$$
\log p=\eta\log a+c,
$$

where $\eta<0$ for decreasing demand, taking expectations gives

$$
\exp(E[\log P_1])=e^c\left(\exp(E[\log A_1])\right)^\eta.
$$

Thus the geometric mean of price equals the inverse-demand function evaluated at the geometric mean of quantity. The source calls this an equality between expected price and the price of the expected amount; its precise mathematical meaning here uses geometric, not arithmetic, means. Constant elasticity makes the relationship linear in logs, not linear in price and quantity levels. In general $E[f(A_1)]\ne f(E[A_1])$.

Similarly, the text's suggestion that a geometric mean makes average percentage error zero needs qualification. The geometric mean centers logarithmic deviations. It does not generally make an arithmetic average of percentage forecast errors vanish. A reproduction should state exactly which error or growth criterion is being centered.

## Limitations, source claims, and practical takeaways

The core deterministic storage equations are the most directly reusable part of the paper. Their accounting is explicit, the competitive carrying relation has a clear interior interpretation, and the scalar reduction makes numerical solution straightforward once curves are supplied. At a zero-stock boundary, however, the equality need not hold: an inequality indicating that storage is not worthwhile replaces the interior relation. Enforcing a full-carry equality in every year would incorrectly eliminate the stockout regime that motivates the paper's asymmetry.

The article asserts that competitive speculators receive no risk premium because chances of gain and loss balance. That is a modeling position in the text, not a general implication of competition or probability theory. Equal probabilities do not ensure equal gain and loss magnitudes, and neither condition establishes that bearing risk requires no compensation. The paper does not derive an equilibrium pricing kernel or model risk-averse balance-sheet capacity. Its later geometric-growth criterion should likewise not be silently substituted for a risk-neutral expectation.

Several broad corollaries are conditional. Storage can damp the cobweb response of future production to past prices, but the paper's diagrams do not prove that every storable commodity system is free of oscillations under arbitrary expectations, delays, or constraints. A left-skewed crop law may encourage recurrent carryover, but its mean–mode ordering alone does not quantify how often storage is optimal. The claim that storability prevents a commodity price from reaching zero presumes sufficiently valuable future demand and feasible carrying; it does not incorporate finite storage capacity or all costs that could make surplus disposal optimal.

There is also no empirical estimation or experimental protocol hidden behind the historical examples. The paper gives no complete cotton dataset, sample dates for fitting curves, standard errors, likelihood, validation period, transaction-cost estimation, or futures portfolio returns. The figures are mechanism diagrams. They should be replicated as solutions under stated illustrative inputs, with any new calibrated exercise labeled separately.

For a researcher implementing the ideas, the essential choices are the demand and supply schedules, their timing, the mapping from planting prices to crop distributions, carrying costs, initial stocks, inventory constraints, and the terminal condition. Those determine the endogenous price path and storage policy. If using the appendix's uncertainty treatment, specify why the geometric criterion fits the decision maker and what repeated-trading assumptions justify it.

The lasting contribution is the feedback loop between storage and both sides of the market. Inventory purchases do more than exploit a given spread: they alter the spread and the next crop. The correct equilibrium balances intertemporal consumption and production against carrying costs, and the correct reproduction verifies quantity conservation, feasible inventories, and the stopping condition together.

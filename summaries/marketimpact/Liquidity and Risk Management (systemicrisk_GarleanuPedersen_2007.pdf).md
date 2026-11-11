# Liquidity and Risk Management

**Nicolae Gârleanu and Lasse Heje Pedersen (2007).** *American Economic Review*, Papers and Proceedings, 97(2), 193–197. DOI: 10.1257/aer.97.2.193. [Source PDF](../../Finance/systemicrisk_GarleanuPedersen_2007.pdf). The local file contains the five-page article, a citation page, and a reproduction notice. The publisher’s [four-page appendix](https://www.aeaweb.org/articles/materials/240) was also read and its equations inspected visually. The note distinguishes the published comparative statics from a numerical reconstruction and several inconsistencies in the appendix and figure calibration.

## Why this matters

A position limit can be individually prudent and collectively destabilizing. If every institution reduces its position when volatility rises, the market can lose buyers with unused capacity. Sellers then wait longer, receive lower prices, and face more risk before completing a sale. A limit that accounts for this longer liquidation horizon requires another reduction in positions. The contribution is to make this feedback an equilibrium calculation rather than assume a fixed holding period or an externally imposed liquidity discount.

The mechanism operates even with risk-neutral agents. Falling prices are compensation for impaired trading opportunities and costly unwanted holdings; the result does not require an increase in conventional risk aversion. The paper extends the Duffie–Gârleanu–Pedersen search market by making the maximum position endogenous to risk controls. It is a theoretical contribution with an illustrative calibration. The discussion of the 1998 crisis is motivating evidence, not a formal empirical test, estimated causal effect, or investment backtest.

## Assets, agents, constraints, and meetings

There is a liquid account earning a constant continuously compounded rate $r>0$, and an illiquid risky asset paying a dividend flow $X_t$. Dividend changes follow a zero-drift Lévy process with finite variance:

$$
E_t[X_{t+T}-X_t]=0,\qquad
\operatorname{Var}_t(X_{t+T}-X_t)=\sigma_X^2T.
$$

Brownian and compound-Poisson dividends are admissible examples. The distinction matters: a variance constraint is equivalent to a fixed-confidence Gaussian VaR limit under Brownian increments, but variance alone does not determine a Lévy distribution’s quantiles. The model primarily analyzes the former risk-control representation, not an exact quantile formula for every admitted dividend process.

Agents are infinitely lived, risk neutral, discount at $r$, and keep wealth bounded below. Each agent independently switches between a high-capacity state $h$ and a low-capacity state $l$. The transition intensity from $l$ to $h$ is $\lambda_u$ and from $h$ to $l$ is $\lambda_d$. The risk capacities are $\bar\sigma$ and zero, respectively. Low capacity can stand for redemptions, funding pressure, or a need to stabilize earnings; these explanations are interpretations, not separately modeled shocks.

For position $\theta_t$, the constraint is

$$
\operatorname{Var}_t\!\left(\theta_t[P(X_{t+\tau})-P(X_t)]\right)
\leq \sigma_i^2.
$$

A holding that breaches the constraint incurs a flow cost $\delta>0$ per share. This is a soft implementation of the limit: a low-capacity owner cannot necessarily sell immediately and bears the cost while searching. Calling the setup an instantaneous hard constraint would eliminate precisely the constrained sellers whose presence produces illiquidity.

The analysis restricts equilibrium holdings to zero or $\bar\theta$, the largest position satisfying the high-state limit. Total asset supply per agent is $\Theta>0$. Four population masses describe type and ownership: $\mu_{ho},\mu_{hn},\mu_{lo},\mu_{ln}$, where $o$ denotes owner and $n$ nonowner. They satisfy

$$
\mu_{ho}+\mu_{hn}+\mu_{lo}+\mu_{ln}=1,\qquad
\bar\theta(\mu_{ho}+\mu_{lo})=\Theta.
$$

An agent contacts randomly selected counterparties at intensity $\lambda$. The paper’s aggregate meeting convention counts either party initiating contact; effective matching between low-state owners and high-state nonowners is $2\lambda\mu_{lo}\mu_{hn}$. Keeping this factor of two consistent is essential. A distressed owner’s rate of finding an eligible buyer is $2\lambda\mu_{hn}$, giving expected sale time

$$
T_s=\frac{1}{2\lambda\mu_{hn}}.
$$

Matched parties bargain, with seller bargaining weight $q\in[0,1]$. Search is most directly suited to OTC markets. The paper also interprets delays in gathering information, making decisions, and mobilizing capital as sources of effective trading delay in other venues; it does not model a limit-order book.

## Reconstructing the steady-state masses

Equation (5) balances the flows into and out of constrained ownership:

$$
0=-2\lambda\mu_{hn}\mu_{lo}-\lambda_u\mu_{lo}
+\lambda_d\mu_{ho}.
$$

The three terms represent selling, recovery of risk-bearing capacity, and a high-capacity owner becoming constrained. The stationary fraction of high types is $h=\lambda_u/(\lambda_u+\lambda_d)$. Define the ownership fraction $s=\Theta/\bar\theta$ and eligible-buyer mass $y=\mu_{hn}$. Conservation then gives

$$
\mu_{ho}=h-y,\qquad
\mu_{lo}=y-h+s,\qquad
\mu_{ln}=1-s-y.
$$

Substituting into the displayed flow balance yields a scalar quadratic:

$$
2\lambda y^2+
\left[2\lambda(s-h)+\lambda_u+\lambda_d\right]y
-\lambda_u(1-s)=0.
$$

This reduction follows directly from the article’s market-clearing and flow equations and supplies a convenient implementation. Let $b=2\lambda(s-h)+\lambda_u+\lambda_d$. The admissible root is

$$
y=\frac{-b+\sqrt{b^2+8\lambda\lambda_u(1-s)}}{4\lambda}.
$$

Check that all four recovered masses are nonnegative and sum to one; $\bar\theta\geq\Theta$ is necessary under the stipulated ownership structure. A zero buyer mass implies an infinite sale time and is unsuitable as a finite-liquidation equilibrium. Computing only a formal positive root without checking the population constraints can produce a spurious numerical solution.

For fixed positions, increasing position capacity leaves the outstanding supply concentrated among fewer owners and frees more high-state nonowners to buy. It therefore raises $y$ and reduces the constrained-owner mass in the relevant interior solution. This direction is also apparent numerically and from the mass identities; it is important for the risk-liquidity feedback.

## Position limits with fixed and endogenous horizons

The conjectured equilibrium price has the form $P(X)=X/r+p$, where $p$ is constant in a given stationary economy. Hence the price-change variance over a fixed horizon is $\sigma_X^2\tau/r^2$. Binding the high-state limit gives the simple-risk-management position

$$
\bar\theta_{\mathrm{simple}}=
\frac{r\bar\sigma}{\sigma_X\sqrt{\tau}}.
$$

With liquidity adjustment, the horizon is the random waiting time to meet an eligible buyer. Under the model’s independence and zero-drift assumptions, total variance reduces to the dividend variance rate multiplied by expected waiting time. Thus equation (10) is

$$
\bar\theta_{\mathrm{liq}}=
\frac{r\bar\sigma}{\sigma_X}
\sqrt{2\lambda\mu_{hn}(\bar\theta_{\mathrm{liq}})}.
$$

This is a fixed point because the position limit changes the population of buyers, which changes the liquidation horizon used to determine the limit. It does not say that every individual liquidation time is known in advance or that positions can be reduced instantly. The liquidity-adjusted constraint evaluates risk over the distribution of search times.

Write $S=r\bar\sigma/\sigma_X$ and $g(u)=u-S\sqrt{2\lambda y(u)}$. Solving $g(u)=0$ over admissible $u>\Theta$ gives candidate equilibria. Multiple roots can occur. The paper selects stable equilibria and identifies the largest-position equilibrium as stable and welfare superior among its equilibrium set. Locally, the relevant stability condition can be implemented as

$$
g'(u)=1-\frac{u\,y'(u)}{2y(u)}>0
$$

at a root. This is a derived expression for the paper’s condition that a marginal increase in holdings violates the constraint after quantities adjust. Blind fixed-point iteration can converge to the wrong branch or fail near a turning point; bracket all admissible roots and assess stability rather than accept the first solver output.

## Bargaining and the liquidity discount

An agent’s value is linear in liquid wealth and in the dividend present value. The ownership-dependent component is $\bar\theta X/r$; type-dependent continuation values incorporate future switches, trading opportunities, and holding penalties. The traded price divides the bilateral surplus according to $q$.

The article’s equation (11) gives the per-share price:

$$
P(X)=\frac{X}{r}
-\frac{\delta}{r}
\frac{r(1-q)+\lambda_d+2\lambda\mu_{lo}(1-q)}
{r+\lambda_d+2\lambda\mu_{lo}(1-q)+\lambda_u+2\lambda\mu_{hn}q}.
$$

The subtraction is crucial. The first term is fundamental dividend value; the second is an illiquidity discount. More buyers improve a seller’s outside option and reduce the discount, while more sellers weaken that option. The penalty, bargaining, meeting, and type-transition parameters affect the discount; no independent stochastic discount factor or risk-aversion calibration is needed.

When trading is immediate, the paper’s footnote distinguishes whether high-capacity agents can absorb all supply. If $\Theta/\bar\theta<h$, the Walrasian benchmark is $X/r$. If high-capacity demand cannot absorb supply, the benchmark becomes $(X-\delta)/r$. Comparing a constrained search equilibrium to an unconstrained fundamental value without checking this capacity condition can conflate two different scarcity effects.

## What the comparative statics establish

Proposition 2 starts from a stable liquidity-adjusted equilibrium and chooses the fixed horizon to equal that equilibrium’s expected sale time. The two regimes then have identical starting allocations and prices. Relative to this common baseline, higher dividend volatility, a lower risk limit, slower meetings, slower recovery into high capacity, or faster loss of capacity lengthen sale times and lower prices. Liquidity adjustment amplifies the effects.

The mechanisms differ across shocks. Higher $\sigma_X$ or lower $\bar\sigma$ directly reduces the simple-rule position. More agents must then hold the outstanding supply, reducing unused buying capacity and lengthening search. Under the liquidity-adjusted rule, longer search creates another tightening of allowable positions. By contrast, changes in meeting or type-switching intensities do not change the simple-rule position when $r,\bar\sigma,\sigma_X,\tau$ are fixed; they affect the mass distribution and prices. Liquidity adjustment makes those same shocks affect positions as well.

These are comparative statics across steady-state economies. The paper argues that adding stochastic changes in parameters could turn them into crisis dynamics, but it does not estimate or simulate a fully specified transition path after a shock. It also does not quantify the probability of a sudden liquidity collapse in real data.

## Numerical design and a replication discrepancy

The published example uses $\lambda=100$, $r=0.1$, $X_0=1$, $\lambda_d=0.2$, $\lambda_u=2$, $\delta=3$, $q=0.5$, $\Theta=1$, and $\bar\sigma=1$. Figure 1 varies $\sigma_X$ and compares the endogenous horizon with fixed $\tau=0.0086$ years. It says the regimes coincide at $\sigma_X=0.3$. There is no dataset, stochastic seed, estimation window, standard error, or transaction-cost backtest: the figure is a deterministic equilibrium calculation.

The following numbers are **derived by implementing the printed mass balance, constraints, and price formula**, not values tabulated by the authors. All admissible roots were bracketed on a logarithmic grid over $(1,1000)$ and refined by bisection; the largest root was selected. The fixed-horizon rule uses the published $0.0086$.

| Dividend volatility | Rule | Position | Expected sale time, years | Price |
|---|---|---:|---:|---:|
| 0.20 | Fixed horizon | 5.39164 | 0.0069073 | 9.88948 |
| 0.20 | Liquidity adjusted | 6.10540 | 0.0067067 | 9.89399 |
| 0.30 | Fixed horizon | 3.59443 | 0.0079200 | 9.86561 |
| 0.30 | Liquidity adjusted | 3.78726 | 0.0077465 | 9.86983 |
| 0.40 | Fixed horizon | 2.69582 | 0.0092795 | 9.83068 |
| 0.40 | Liquidity adjusted | 2.54004 | 0.0096872 | 9.81958 |

At volatility $0.3$, the endogenous expected horizon is approximately $0.0077465$, rather than $0.0086$. Therefore the printed equations and stated parameter values do not reproduce the claimed exact crossing. Setting the fixed horizon to the reconstructed endogenous value restores a matched baseline, but that is a correction to the numerical comparison, not the stated calibration. The reported figure’s qualitative amplification is consistent with the mechanism, while its exact plotted levels should not be treated as independently reproduced.

The endogenous calculation also returns a smaller root: approximately 1.09777, 1.16243, and 1.27428 at the three volatility settings. These are additional algebraic solutions; the stable-branch selection matters economically and computationally. Recording only the largest root without documenting the other candidates would obscure this sensitivity.

## Appendix checks and implementation limits

The appendix contains transcription inconsistencies. Its buyer HJB uses an owner mass where the matching counterparty is a constrained seller; its price-adjustment expression has the opposite sign to the main article’s discount; and its random-horizon calculation omits the main text’s factor of two. Its stated position derivatives for buyer and seller masses reverse the directions used later in its own proof. These issues were checked visually. The reconstruction above follows the main article’s mass balance, matching convention, and price formula, with conservation identities used as consistency checks.

A reproducible implementation should therefore enforce the same meeting convention in every equation; verify nonnegative masses, supply clearing, and stationarity; solve all candidate position roots; test the selected branch; and match the starting fixed horizon to the reconstructed expected sale time before comparing sensitivities. The numerical table isolates those checks and does not claim an empirical validation.

Several economic limits remain. Dividend risk is exogenous, while price changes caused by moving between stationary equilibria are not included as a fully modeled additional source of transition risk. Risk capacity switches are independent across agents; common funding shocks are represented through parameter changes rather than an estimated correlated default process. Positions are binary, there is one illiquid asset, meetings and bargaining are stylized, and the direct benefits of risk control are not endogenously optimized. The largest-position equilibrium’s welfare ranking is internal to that model, not a general argument for relaxing institutional limits.

The practical research implication is specific: a liquidation horizon can depend on how much buying capacity remains after other institutions react to the same risk signal. Treating that horizon as exogenous can miss a multiplier. The article supplies a parsimonious equilibrium mechanism and a reconstructible fixed-point problem; it does not provide calibrated portfolio limits or a demonstrated crisis-prediction strategy.

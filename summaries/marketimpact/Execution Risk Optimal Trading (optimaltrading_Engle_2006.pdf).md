# Execution Risk — Engle & Ferstenberg (2006) — Detailed Quantitative Research Notes

**Authors:** Robert Engle (NYU Stern, NBER), Robert Ferstenberg (Morgan Stanley) | **Year:** 2006 | **Venue:** NBER Working Paper 12165 (April 2006), JEL G2 | **Source file:** `Finance/optimaltrading_Engle_2006.pdf` (the filename says "optimal trading"; the paper is *Execution Risk*)

Theory paper, no empirical calibration; illustrations come from a 20-period Excel model with undisclosed "rather typical" parameters.

---

## Question

The paper puts portfolio choice (Markowitz: expected gain vs. variance of holdings) and optimal execution (Almgren–Chriss, Grinold–Kahn, Bertsimas–Lo, Obizhaeva–Wang: $\min E(TC)+\lambda^* V(TC)$) into one problem. It then asks four questions: (i) should $\lambda^*$ equal the investment $\lambda$? (ii) does execution risk average out across names and over time? (iii) should the schedule depend on the rest of the book? (iv) should execution risk be hedged with assets that are not in the order?

Answers: (i) yes, it is one problem with one $\lambda$. (ii) no, it is priced through the variance of the whole P&L. (iii) no, under specific conditions (Prop. 4). (iv) yes, by temporarily trading correlated, cheap assets such as futures.

## Setup and the key identity

Holdings are $x_t$ (shares), mid/fair price is $p_t$, execution price is $\tilde p_t$ and arrival price is $p_0$. Implementation shortfall (Perold 1988):
$$TC=\sum_{t=1}^T \Delta x_t'(\tilde p_t-p_0)=\sum_t \Delta x_t'(\tilde p_t-p_t)+\sum_t (x_T-x_{t-1})'\Delta p_t .$$
Portfolio value is $y_t=x_t'p_t+c_t$ with self-financing cash $\Delta c_t=-\Delta x_t'\tilde p_t$ (zero rates, no dividends), so $\Delta y_t=x_{t-1}'\Delta p_t-\Delta x_t'(\tilde p_t-p_t)$ and
$$y_T-y_0=x_T'(p_T-p_0)-TC. \tag{13}$$

**Proposition 1.** The optimal trajectory solves $\max_{\{x_t\}} E[x_T'(p_T-p_0)-TC]-\lambda V[x_T'(p_T-p_0)-TC]$. The risk is the variance of a *difference*, so $\mathrm{Cov}(\text{gain},TC)$ matters, not just $V(TC)$. For a liquidation ($x_T=0$), long and short positions give the same problem.

**Two-step separation.** Optimize over $(0,T_2)$ with $T_2\gg T$, assuming no return covariance between $(0,T)$ and $(T,T_2)$. The problem then splits approximately into (18) choosing $x_T$ by the usual mean-variance rule and (19) choosing $x_1,\dots,x_{T-1}$ given $x_T$. This matches the PM-to-trader workflow. High-turnover funds cannot separate the two, and then targets depend on costs. That is the link to liquidity asset pricing (Amihud–Mendelson 1986; Acharya–Pedersen 2005).

## Sharpe ratio and mis-specified frontiers

$$SR=\frac{E[x_T'(p_T-p_0)]-E[TC]-r_f y_0T}{\sqrt{T\,[V(\text{gain})+V(TC)-2\,\mathrm{Cov}(\text{gain},TC)]}}$$
In a single asset, buys have $\mathrm{Cov}>0$: TC is high when prices rise, and so are gains, which lowers net risk. Sells have the opposite sign. The paper compares three objectives: Pure Markowitz (ignores TC), Cost-Adjusted Markowitz (subtracts $E[TC]$ and ignores its risk) and the True objective. Their frontiers are ordered Pure $\ge$ Cost-Adjusted $\ge$ True. Portfolios chosen under the first two lie inside the true frontier, so this is a planning error, not only an ex-post disappointment.

## General assumptions and Propositions 2–3

- **A.1** $V_0(\tilde p_t-p_t\mid\{x\})=0$ and $E_0(\tilde p_t-p_t\mid\{x\})=\tau_t$. The instantaneous cost is deterministic given the path.
- **A.2** $V_0(\Delta p_t\mid\{x\})=\Omega$ and $E_0(\Delta p_t\mid\{x\})=\mu+\pi_t$. Trades shift the mean of price changes but leave the covariance unchanged.

With these, $V(\text{gain})=T\,x_T'\Omega x_T$, $V(TC)=\sum_t(x_T-x_{t-1})'\Omega(x_T-x_{t-1})$ and $\mathrm{Cov}=\sum_t x_T'\Omega(x_T-x_{t-1})$. Combined:
$$V\big(x_T'(p_T-p_0)-TC\big)=\sum_{t=1}^T x_{t-1}'\Omega x_{t-1}. \tag{28}$$
So risk is just the running variance of the holdings actually carried.

**Prop. 2:** $\max_{\{x_t\}}\sum_t\big[x_{t-1}'(\mu+\pi_t)-\Delta x_t'\tau_t\big]-\lambda\sum_t x_{t-1}'\Omega x_{t-1}$. This is generally nonlinear because $\tau_t,\pi_t$ depend on the path.

**A.3 (optimal target):** $x_T=\tfrac{1}{2\lambda}\Omega^{-1}\mu$. Substituting $\mu=2\lambda\Omega x_T$ and completing the square gives

**Prop. 3:** $\max_{\{x_t\}}\sum_t\big[x_{t-1}'\pi_t-\Delta x_t'\tau_t+\lambda x_T'\Omega x_T-\lambda(x_T-x_{t-1})'\Omega(x_T-x_{t-1})\big]$.

Here $\mu$ drops out and only the target matters. The relevant risk is $V(TC)$, i.e. the "tracking error to target" of the unfinished trade. Under A.3, **buys and sells have the same risk as liquidations regardless of other holdings**. The buy/sell asymmetry from the Sharpe-ratio section only applies when the target is *not* mean-variance optimal. This also justifies the Almgren–Chriss objective, and it pins $\lambda^*=\lambda$.

## Almgren–Chriss dynamics (Section V)

- **A.1.a** $\tilde p_t-p_t=\mathrm{T}\Delta x_t$ (temporary impact matrix $\mathrm{T}$).
- **A.2.a** $\Delta p_t=\Pi\Delta x_t+\mu+\varepsilon_t$ with $\varepsilon_t\sim D(0,\Omega)$ (permanent impact $\Pi$).

Huberman–Stanzl (2004) is cited: no-arbitrage forces permanent impact to be linear and time-invariant, while temporary impact is unrestricted. Then
$$E(TC)=\sum_t\{\Delta x_t'\mathrm{T}\Delta x_t+(x_T-x_{t-1})'(\mu+\Pi\Delta x_t)\},\qquad V(TC)=\sum_t (x_T-x_{t-1})'\Omega(x_T-x_{t-1}).$$
The problem is linear-quadratic, so trajectories have a closed form. Without A.3 the solution needs the full holdings vector and $\mu$.

**Prop. 4.** Assume A.1.a, A.2.a and A.3, and that traded assets have zero permanent impact on non-traded ones. Then holdings that stay fixed during the trade do not affect optimal execution. The only surviving interaction term is $x_{t-1}'\Pi\Delta x_t$. The covariance with the rest of the book, which lowers risk for buys and raises it for sells in positively correlated books, is exactly offset by the expected-return term when the target is optimal.

**Three-period closed form** (times $0,t,T$; symmetric matrices):
$$x_t=\tfrac12(\Pi+2\mathrm{T}+\lambda\Omega)^{-1}\big[(\Pi+2\mathrm{T})x_0+(\Pi+2\mathrm{T}+2\lambda\Omega)x_T\big]. \tag{40}$$
- With $\lambda=0$ the midpoint holding is $(x_0+x_T)/2$, i.e. an even pace.
- With $\lambda>0$ (scalar case) the midpoint moves toward $x_T$, so trading is front-loaded. This holds for any terminal position, not only liquidations.
- $\Pi$ and $\mathrm{T}$ enter only as $\Pi+2\mathrm{T}$. In discrete time, summing $(X-x_{t-1})\Delta x_t$ gives $X^2/2+\tfrac12\sum\Delta x_t^2$, so permanent impact acts like extra temporary impact of size $\Pi/2$ on top of a schedule-independent cost.

**Hedge trades.** Take block-diagonal impacts, $x_{2,0}=x_{2,T}$ and a non-block-diagonal $\Omega$:
$$x_{2,t}=x_{2,T}-(\Pi_{22}+2\mathrm{T}_{22}+\lambda\Omega_{22})^{-1}\lambda\Omega_{12}(x_{1,t}-x_{1,T}). \tag{41}$$
With positive correlation, a buy program in asset 1 also buys asset 2 and later sells it back, so the unfinished book is long asset 2 and short the remaining asset-1 purchase. When $\lambda$ is large or asset 2's impact is negligible, the hedge ratio tends to $-\Omega_{22}^{-1}\Omega_{12}$. The paper calls this "the beta of asset 2 on asset 1". Strictly, the minimum-variance hedge ratio is the regression coefficient of asset-1 returns on asset-2 returns ($\mathrm{Cov}_{12}/\mathrm{Var}_2$). The paper's phrasing reverses the regression. Futures are the natural hedge instrument.

**Simulations (20 periods, buy order; Figs. 1–2).** Risk-neutral trading is flat. Risk-averse trading is front-loaded. Adding the hedge asset makes the primary trade *less* aggressive, and more so at higher covariance (0.5 vs 0.8). Hedge positions are bought early, resold gradually, and larger when covariance is higher.

## Reversals and continuations (Section VI)

The model adds lags: $\tilde p_t=p_t+\mathrm{T}(L)\Delta x_t$ and $\Delta p_t=\Pi(L)\Delta x_t+\mu+\varepsilon_t$. The text labels these A.2.b/A.3.b and Prop. 5 calls them A.1.b/A.2.b, an inconsistency in the paper. Trades before $T$ affect prices after $T$, so the objective runs to $T_1\ge T+q$. **Prop. 5**: the problem is still linear-quadratic with a closed form, and still uses the same $\lambda$. Figure 3 results:
- A one-period permanent reversal makes trading less aggressive. Buying into a rise that later reverts is especially costly.
- A transitory continuation also makes trading less aggressive.
- A transitory reversal leads to *more* early trading, even when combined with a permanent reversal.

The authors note that these offsetting effects depend on coefficient magnitudes.

## Liquidity risk (Section VII)

Liquidation value $y_T=c_T$ (with $x_T=0$) is a random variable, in fact a family of them indexed by strategy. Choose the strategy by expected utility, then measure its tail:
- 1% quantile of cash after *optimal* liquidation over, say, 10 days, parallel to 10-day market VaR;
- or preferably expected shortfall: the expected liquidation cost given that it exceeds its 99% quantile.

Liquidity risk can be larger or smaller than market risk. Exposure falls as the position is sold, but the directional impact cost may dominate. Because optimal liquidation is front-loaded, the measure is fairly insensitive to the allowed horizon except for large positions. Impact parameters rise with volatility, so liquidity risk can vary *more than proportionally* to volatility. For crises, the paper suggests inflating the impact coefficients and recomputing, a possible model of Persaud's "liquidity black holes".

## Critical assessment

- **Convincing.** Identity (13) and Prop. 1 are clean accounting, and the one-$\lambda$ argument follows directly from them. Prop. 3 is the substantive insight. Under an optimal target, execution risk is the utility loss from being away from target, $\lambda(x_T-x_{t-1})'\Omega(x_T-x_{t-1})$. This anticipates later "aim portfolio" and tracking-to-target formulations.
- **Fragile.**
  - Prop. 4 and the buy/sell symmetry rest on A.3 holding exactly with a constant $\mu$ over the trading window. In practice, targets come from cost-aware optimizers with constraints, and short-horizon alpha (decay, momentum in the traded names) differs from the $\mu$ that set $x_T$. Both break the independence result.
  - A.1–A.2 exclude random instantaneous costs and trade-induced volatility.
  - Linear permanent and temporary impact conflicts with the square-root law for large metaorders.
  - Units matter for "same $\lambda$". It is per-period dollar variance, so a PM's $\lambda$ calibrated at an annual horizon must be rescaled to the execution clock before it can be reused.
  - The figures cannot be reproduced, because the parameters are not reported.
- **Practical relevance.**
  - Set algo urgency from the fund's own risk aversion rather than an arbitrary broker setting.
  - Evaluate TCA on $E[TC]+\lambda V(TC)$, not on mean shortfall.
  - Overlay index or sector futures during large programs, sized near the minimum-variance hedge of the unfinished trade and unwound as it completes.
  - Report liquidation ES next to VaR, with stressed impact parameters.

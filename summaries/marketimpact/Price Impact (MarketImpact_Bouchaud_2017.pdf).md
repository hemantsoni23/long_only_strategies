# Price Impact

**Authors:** Jean-Philippe Bouchaud (Capital Fund Management)  
**Publication:** Encyclopedia-style entry "Price Impact" (cross-references "Execution Costs", "Adverse Selection", "Limit Order Markets" indicate an encyclopedia of quantitative finance); this PDF version dated August 24, 2017, 11 pp. Fuller treatment: Bouchaud, Farmer and Lillo, "How markets slowly digest changes in supply and demand", *Handbook of Financial Markets: Dynamics and Evolution* (2009).  
**Source file:** `Finance/MarketImpact_Bouchaud_2017.pdf`

---

## 1. Question and framing

Price impact is the correlation between an incoming order's sign and the subsequent price change. The two operational questions are its **volume dependence** and its **temporal structure** (immediate/permanent vs lag-dependent). Bouchaud separates three mechanisms that all yield positive flow-return correlation:

1. **Forecasting:** traders anticipate moves; trades need not move prices at all, and pure noise trades should have zero impact.
2. **Information revelation** (Glosten-Milgrom, Kyle): with anonymous flow, every trade may carry private information, so all trades impact. Impact is both a friction and the channel through which information enters prices.
3. **Mechanical/statistical:** even a purely random order flow in an order-book model (Farmer, Patelli, Zovko 2005) produces a well-defined impact conditional on an extra buy. "Information revelation" can then be self-fulfilling with zero informed traders.

For (1)-(2), in Hasbrouck's (2007) phrase, "orders do not impact prices... orders forecast prices." The chapter's thesis is that volume dependence and time dependence are where these pictures can be discriminated.

## 2. Kyle benchmark: linear and permanent

The market maker clears every $\Delta t$ with $\Delta p = \lambda\,\epsilon v$ ($\epsilon=\pm1$ the sign of net volume, $v=|v_b-v_s|$), and impact is permanent:
$$p_T = p_0 + \lambda\sum_{n=0}^{N-1}\epsilon_n v_n,\qquad T=N\Delta t.$$
Huberman-Stanzl (2004) and Farmer (2002): if impact is permanent, linearity is the only specification that excludes price manipulation. Prices are a martingale only if $\epsilon_n v_n$ are serially uncorrelated, which the Kyle insider's schedule guarantees but real order flow violates.

## 3. Measures

- **Response function** (drift neglected): $R(T)=E[(p_T-p_0)\epsilon_0]$; in Kyle, $R(T)=\lambda E[v]$, independent of lag. Volume-conditioned $R(T,v)=E[(p_T-p_0)\epsilon_0\mid v_0=v]=\lambda v$ in Kyle. Both depend implicitly on the aggregation scale $\Delta t$.
- **Flow-return correlation** $\rho(T)=\mathrm{corr}\big(p_T-p_0,\ \sum_n\epsilon_n v_n\big)$: equal to 1 in Kyle; below 1 with time-varying $\lambda$ or trade-unrelated quote revisions, $p_T=p_0+\lambda\sum\epsilon_n v_n+\sum\eta_n$. Replacing $v_n$ by $v_n^\psi$ with $\psi<1$ raises the measured correlation.

## 4. Empirical facts

Two time scales must be specified: aggregation $\Delta t$ and measurement horizon $T$.

**Concavity.** $R(\Delta t,v)\propto v^{\psi(\Delta t)}$, $\psi\le1$, with $\psi\simeq0.1$-$0.3$ for individual trades, rising toward 1 when $\Delta t$ spans thousands of trades (residual concavity at large volumes; Hasbrouck-Seppi 2001, Plerou et al. 2002). $\rho(\Delta t)$ also rises with $\Delta t$, exceeding 0.5 for daily returns of stocks, futures and FX (Evans-Lyons 2002). Small trade-level $\psi$ is consistent with price changes correlating more with the number of trades than with volume (Jones, Kaul, Lipson), and is usually attributed to **discretionary trading**: large market orders are sent only when large volume sits at the best quote.

**Own-trade (metaorder) impact.** Brokers' own-execution data give $\psi\approx1/2$ (Almgren et al. 2005). BARRA (1997):
$$R(\Delta t,v)=A\,\sigma\sqrt{v/V},\qquad A=O(1),$$
with $\sigma$ volatility and $V$ volume per unit time, $\Delta t$ the time needed to complete the trade. Justifications: BARRA, Grinold-Kahn (1999), Gabaix et al. (2006).

**Cap scaling** (single trades; Lillo, Farmer, Mantegna 2003): $R(\Delta t,v)\approx M^{-0.3}F\big(M^{0.3}v/\bar v\big)$, $\bar v$ the stock's average trade size, $F$ a power law with exponent $\psi$.

**Long memory of order flow.** Trade-sign autocorrelation $C(\ell)=E[\epsilon_n\epsilon_{n+\ell}]$ decays extremely slowly, over at least several days (thousands of trades), $C(\ell)\sim\ell^{-\gamma}$ with $\gamma\approx0.5$ for stocks. Cause: displayed liquidity is tiny relative to desired size, so orders are split over hours to weeks. This also means private information is incorporated only slowly. Combined with permanent impact, it would generate strongly autocorrelated returns, which are not observed. **Impact therefore cannot be permanent.**

## 5. Transient, non-linear (propagator) model

$$p_T=p_{-\infty}+\lambda\sum_{n=-\infty}^{N-1}G(N-n)\,\epsilon_n v_n^{\psi}.$$
With equal volumes and $C(\ell)\sim\ell^{-\gamma}$, $\gamma<1$, returns are uncorrelated if $G(\ell)\sim\ell^{-\beta}$ with
$$\beta=\frac{1-\gamma}{2}\quad(\text{Bouchaud, Gefen, Potters, Wyart 2004}).$$
A permanent component $G(\infty)>0$ is compatible with diffusive prices only if $\gamma>1$. Observed response and bare kernel are related by
$$R(\ell\Delta t)=\lambda v^\psi\Big[G(\ell)+\sum_{0<j<\ell}G(\ell-j)C(j)+\sum_{j>0}\big(G(\ell+j)-G(j)\big)C(j)\Big]:$$
the second term is the impact of subsequent same-sign trades, the third the evolving impact of earlier trades correlated with $\epsilon_0$. So $R\neq G$; even though $G(\ell)\to0$, both $R(T)$ and $\rho(T)$ tend to **non-zero limits** as $T\to\infty$ when $\beta=(1-\gamma)/2$ holds.

**No manipulation.** With permanent impact ($\beta=0$) only $\psi=1$ is admissible. With transient impact, Gatheral (2008, SSRN) shows $\beta+\psi\ge1$ rules out manipulation.

## 6. Surprise formulation and asymmetric impact

If prices are required to be a strict random walk, only the unpredictable part of flow moves them:
$$\Delta p_n=\lambda v^\psi\big(\epsilon_n-E[\epsilon_n\mid I_{n-1}]\big).$$
Uncorrelated signs recover Kyle. With correlated signs, the more likely outcome ($\epsilon_n=\operatorname{sign}E[\epsilon_n\mid I_{n-1}]$) has the smaller impact (Gerig 2007): a buy after a buy moves the price less than a sell after a buy. With a linear predictor $E[\epsilon_n\mid I_{n-1}]=\sum_{j\ge1}a_j\epsilon_{n-j}$ (Hasbrouck 1991 VAR; $a_j$ obtained from $C(\ell)$ by standard filtering), the surprise model coincides with the propagator model under
$$G(\ell)=1-\sum_{j=1}^{\ell-1}a_j.$$

## 7. Spread and impact

Market makers who cannot predict the surprise quote
$$a_n=p_{n-1}+\lambda v^\psi\big(1-E[\epsilon_n\mid I_{n-1}]\big),\quad b_n=p_{n-1}+\lambda v^\psi\big(-1-E[\epsilon_n\mid I_{n-1}]\big),$$
which gives no ex-post regret (Madhavan, Richardson, Roomans 1997) and $S=a_n-b_n=2\lambda v^\psi$. Spread and impact are the same quantity: liquidity providers are compensated for adverse selection. Consequently volatility per trade $\sigma_1\propto S$, supported empirically by Wyart et al. (2008); clock-time volatility is $\sigma=\sigma_1\sqrt f$ with $f$ the trading frequency.

## 8. Conclusions of the chapter

Signed flow and returns are strongly correlated, but impact is concave in volume and transient in time; transience is forced by long-memory order flow. An effective linear-permanent model makes sense only after averaging over days. Because electronic markets are anonymous, informed and uninformed trades executed the same way must have the same statistical impact: impact lets private information into prices, and by the same token noise-trader flow contributes to volatility.

## 9. Assessment

- **Nature of the piece.** A short survey with no new data; all exponents ($\psi$, $\gamma$, $\beta$, the $M^{-0.3}$ scaling) are quoted from the cited literature and are era- and venue-dependent. It does not discriminate empirically among the three mechanisms of Section 1; it only says where to look.
- **Tension in the stylized numbers.** With $\gamma\approx0.5$ the diffusivity condition gives $\beta\approx0.25$; combined with trade-level $\psi\approx0.1$-$0.3$, $\beta+\psi<1$, i.e. outside the region where Gatheral's criterion guarantees no manipulation. The chapter does not comment on this; in practice the propagator is calibrated at the trade level while the $\psi\approx1/2$ square-root law refers to metaorders, and the two should not be mixed in one execution model without checking the no-arbitrage condition.
- **Equal-volume simplification.** The $\beta=(1-\gamma)/2$ result and the $R$-$G$-$C$ identity are derived with constant volumes; volume and liquidity fluctuations are acknowledged but not treated.
- **Practical relevance.** (i) Fitting "permanent impact" to observed $R(T)$ confounds bare impact with predictable future same-sign flow and overstates permanence; deconvolve with $C$ or use the VAR route. (ii) For one's own parent orders the sign is highly predictable, so incremental impact of later child orders is not the unconditional impact. (iii) The square-root law $R/\sigma=A\sqrt{v/V}$ is the natural metaorder cost model; linear permanent impact is acceptable only for coarse, daily-or-longer attribution. (iv) $S/\sigma_1$ is a usable cross-venue sanity check for the spread-impact relation.

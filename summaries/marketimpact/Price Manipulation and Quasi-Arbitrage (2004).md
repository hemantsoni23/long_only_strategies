# Price Manipulation and Quasi-Arbitrage

**Authors:** Gur Huberman, Werner Stanzl  
**Year:** 2004  
**Journal/Venue:** *Econometrica*, Vol. 72, No. 4 (July 2004), pp. 1247--1275  
**Source file:** `Finance/MarketImpact_HubermanStanzl_2004.pdf`

## Question

A trader with no view on value but perfect knowledge of how prices respond to trades tries to profit from round trips. Which price-response functions rule this out? The answer: with time-independent impact, the **permanent** component must be linear in trade size; the temporary component can be much more general. With time-varying linear impact, no-manipulation is a positive-semidefiniteness condition that limits how fast liquidity may improve over time.

## Model

One asset, $N$ auctions on $(0,1]$, $\Delta_N=1/N$. The trader submits $q_{n}$; the crowd's net order $\eta_n$ (i.i.d., mean zero, unknown to the trader when he trades) and public news $\varepsilon_n$ (i.i.d., mean zero) are independent:
$$\tilde p_n=\tilde p_{n-1}+U_{n-1}(q_{n-1}+\eta_{n-1})+\varepsilon_n,\qquad p_n=\tilde p_n+P_n(q_n+\eta_n).$$
$\tilde p_n$ is the quote, $p_n$ the transaction price; the **price-impact function** $P$ is the total immediate effect, the **price-update function** $U$ the permanent effect, $P-U$ the temporary effect. Both are deterministic functions of total flow set by competitive liquidity providers; their origin (information or inventory) is not modeled. Examples: a bid-ask spread $s$ with depth $S$ and a midquote moving halfway to the last trade gives $P(q)=\pm s/2$ on $0<|q|\le S$ and $U=P/2$; the family $\tilde p_n=\alpha\tilde p_{n-1}+(1-\alpha)p_{n-1}+\varepsilon_n$ gives $U=(1-\alpha)P$; $\alpha=0$ with linear $U$ and $\varepsilon=0$ is Kyle (1985). Suggested interpretation of $\eta$ given autocorrelated real order flow: the *unexpected* part of crowd demand.

Round trip: $\sum_n q_n=0$, profit $\pi=-\sum_n p_nq_n-c(T)$ with fixed cost $c(k)\propto k^e$, $e<2$, for $k$ trades.

**Definitions.** Price manipulation (PM): round trip with $E[\pi]>0$. Unbounded PM (UM): sequence with $E[\pi_m]\to\infty$. Quasi-arbitrage (QA): UM with $E[\pi_m]/\mathrm{Std}[\pi_m]\to\infty$ (if divisible, its risk can be scaled away, as in Huberman's 1982 asymptotic arbitrage; weaker than Ledoit's $\delta$-arbitrage). A market is **weakly viable** if a Sharpe-ratio maximizer's optimal demand exists, **strongly viable** if it is uniquely zero; weak viability rules out QA.

**Markets.** $\mathcal M$: expected functions $\hat P(q)=E[P(q+\eta)]$, $\hat U$ exist and are sign-preserving (buys raise, sells lower expected prices); the trader may choose $\Delta_N$. $\mathcal M_1$: additionally $\hat U(q)\ge-\hat U(-q)$ for $q\ge0$ (buys update at least as much as sells). $\mathcal M_2$: $\mathcal M_1$ plus variances of $P$, $U$, $\varepsilon$ exist and per-period variances grow at most linearly in $N$ (the standard assumption has $\sigma_\varepsilon^2\propto1/N$; constant or growing per-period variance is allowed).

## Results: time-independent impact ($P_n=P$, $U_n=U$)

Proof strategy for necessity, each step a constructed round trip whose expected profit is $O(m^2)$ in the number of trades $m$ while its standard deviation grows more slowly, so letting $\Delta_N\to0$ yields QA:
1. **Symmetry**, $\hat U(q)=-\hat U(-q)$: otherwise buy $q$ for $m$ periods, sell $q$ for $m$ periods (or the reverse).
2. **Continuity** except possibly at 0: exploit a jump by buying just above it and selling at it.
3. **Linearity on rationals**, $\hat U(q)=\hat U(1)q$: otherwise buy $q$ for $m$ periods and sell one share in each of $mq$ periods (or reverse).
4. **$U$ itself linear**: $E[R_U(q+\eta)]=0$ for all $q$ with Gaussian $\eta$ forces the residual $R_U=0$ a.e.

**Proposition 1.** With unrestricted trade size and either $\eta\equiv0$ or Gaussian $\eta$: NoPM in $\mathcal M$ requires $U$ linear with nonnegative slope (a.e.); so do NoUM in $\mathcal M_1$ and NoQA in $\mathcal M_2$.

**Theorem 1** (general symmetric domains, non-Gaussian crowd). Each of NoPM, NoUM, NoQA implies $U$ is **quasi-linear**: $U(y)=\lambda y+R_U(y)$, $\lambda\ge0$, with $E_n[R_U(\tilde q_n+\eta_n)]=0$ for every trader-measurable $\tilde q_n$, i.e. the trader always expects linear updating. $P$ may include per-share commissions, so the results hold with proportional costs.

**Proposition 2** (necessary, if $c(k)\propto k^a$, $a<1$). (i) $\hat P(q)-\hat P(-q)\ge\hat U(q)$ for $q\ge0$: the expected spread at any size must exceed the expected permanent update; (ii) $\hat P\ne0$ whenever $\hat U\ne0$. QA-absence alone does not imply these.

**Proposition 3** (sufficient). $U$ linear with slope $\lambda\ge0$, Gaussian crowd, $P$ odd and $P(q)\ge U(q)/2$ for $q\ge0$ $\Rightarrow$ NoPM, NoUM, NoQA. The key fact: with $P=U/2=\lambda x/2$, $q\equiv0$ uniquely maximizes expected round-trip profit. Hence **nonlinear, even complicated, temporary impact is admissible** as long as it is odd and dominates half the permanent impact.

**Proposition 4 / Corollary 1.** Under Prop. 3's condition on $P$ and Gaussian crowd: linear $U$ $\Leftrightarrow$ NoPM in $\mathcal M$ $\Leftrightarrow$ NoUM in $\mathcal M_1$ $\Leftrightarrow$ NoQA in $\mathcal M_2$; NoQA in $\mathcal M_2$ $\Leftrightarrow$ strong viability of $\mathcal M_2$ (risk-neutral: NoUM $\Leftrightarrow$ strong viability of $\mathcal M_1$). This justifies the linear-impact assumptions in insider-trading models and in Bertsimas-Lo (1998) and Huberman-Stanzl (2002) optimal execution.

## Results: time-dependent linear impact

$U_n(q)=\lambda_n q$, $P_n(q)=\mu_n q$, $\lambda_1=\mu_1\ge0$; later slopes may be of either sign.

**Theorem 2.** For fixed $\Delta_N$ and sufficiently large initial price, NoPM $\Leftrightarrow$
$$\Lambda_N=\begin{bmatrix}2\mu_2&\lambda_2&\lambda_2&\cdots&\lambda_2\\ \lambda_2&2\mu_3&\lambda_3&\cdots&\lambda_3\\ \lambda_2&\lambda_3&2\mu_4&\cdots&\lambda_4\\ \vdots&&&\ddots&\vdots\\ \lambda_2&\lambda_3&\lambda_4&\cdots&2\mu_N\end{bmatrix}\succeq0.$$
Expected round-trip profit is $-\tfrac12\,q^\top\Lambda_N q-c$, which is where the matrix comes from ($N=3$ worked explicitly: requires $\mu_2,\mu_3\ge0$ and $\mu_2\mu_3\ge\lambda_2^2/4$). Positive definiteness can be checked in $O(N)$ via leading minors,
$$\det\Lambda_j=2(\mu_j+\mu_{j-1}-\lambda_{j-1})\det\Lambda_{j-1}-(2\mu_{j-1}-\lambda_{j-1})^2\det\Lambda_{j-2},$$
with $\det\Lambda_1=2\mu_2$, $\det\Lambda_2=4\mu_2\mu_3-\lambda_2^2$.

Implications: all $\mu_n\ge0$, but $\lambda_n$ may be negative (a purchase that lowers future prices undermines manipulation). For any update sequence, sufficiently large $\mu_n$ restore NoPM. With purely permanent impact ($\lambda_n=\mu_n$), PSD means **liquidity may not increase too fast**: otherwise buy in illiquid early periods and sell into later liquid ones; decreasing liquidity is harmless. There is no comparably clean criterion for UM or QA. Example: $\tilde p_0=10$, $\lambda=(1,1,0)$; buying $q$ in periods 1 and 2 and selling $2q$ in period 3 gives $E[\pi]=q^2$, $\mathrm{Std}[\pi]=q\sqrt{3\sigma_\eta^2+5\sigma_\varepsilon^2}$, a quasi-arbitrage.

**Kyle.** Black (1995) conjectured Kyle's model admits manipulation by uninformed traders posing as informed. False: Kyle's equilibrium is a special case (no temporary impact, $\varepsilon=0$) with nearly constant $\lambda_n$, so $\Lambda_N\succeq0$ and the equilibrium is strongly viable. **Proposition 5:** with symmetric update functions that become less sensitive over time ($U_n(x)\le U_{n-1}(x)$, $x\ge0$) and Gaussian crowd, NoUM forces $\hat U_n$ to converge pointwise to a linear function on any $(\tau,1-\tau)$ as $N\to\infty$: only approximately linear equilibria survive frequent trading.

## Extensions

- **Multiple assets.** With $U=P$ (no temporary impact) as sufficient condition, NoPM $\Leftrightarrow$ impact linear with a PSD matrix; in particular **cross-impacts must be linear and symmetric** (impact of $i$ on $j$ equals impact of $j$ on $i$). Table I example: buying A moves B by $0.5$, buying B does not move A; a 22-trade round trip earns \$1 in expectation. This is stronger than Black's additivity requirement. UM/QA are less meaningful here because unbounded trading can drive other prices negative.
- **Gain-loss ratio** (Bernardo-Ledoit 2000). Replacing "infinite Sharpe ratio" by "infinite GLR" ("great deals"), with growth conditions on expected negative parts instead of variances, leaves all results unchanged.

## Empirical implications stated by the authors

Empirical models that impose time independence and identify $P$ with $U$ while finding nonlinear updates (Hasbrouck 1991; Hausman-Lo-MacKinlay 1992; Kempf-Korn 1999), or asymmetric buy/sell block impact (Chan-Lakonishok 1995; Holthausen-Leftwich-Mayers; Gemmill 1996; Keim-Madhavan 1996), taken literally imply manipulation opportunities. Either those opportunities are unexploited or the specification is wrong, most plausibly time independence or the conflation of permanent and temporary impact. Models where past trades change the current impact function (Breen-Hodrick-Korajczyk 2002; Hasbrouck 1991) fall outside Theorems 1-2, but estimated parameters can be checked directly for manipulation.

## Assessment

- **What is robust:** the linearity of *permanent, time-independent* impact is a clean and strong result, and the separation of permanent from temporary impact is the paper's lasting contribution: concave temporary costs (square-root-type) are not ruled out, and much of later execution theory rests on "linear permanent + general temporary". The $\Lambda_N\succeq0$ criterion is a practical consistency check for any fitted time-varying linear impact schedule (e.g. intraday liquidity profiles).
- **What is restrictive:** impact is a deterministic function of current flow only; temporary impact vanishes by the next auction, so decaying (transient) impact is not covered. Later work (Gatheral 2010; Bouchaud and coauthors' propagator models) shows that once impact decays over time, concave instantaneous impact can be manipulation-free, which weakens the practical force of "nonlinear permanent impact implies arbitrage". Market orders only; limit orders are the named open extension. The strongest statements need Gaussian crowd trades; otherwise only quasi-linearity. Sharpe-ratio (or risk-neutral) preferences only.
- **Practical relevance:** when calibrating impact for execution or TCA, keep the permanent component linear (and symmetric across assets in a cross-impact matrix), put nonlinearity into the temporary or decaying part, and verify that the temporary cost satisfies $P\ge U/2$ at relevant sizes and that liquidity schedules do not violate the PSD condition.

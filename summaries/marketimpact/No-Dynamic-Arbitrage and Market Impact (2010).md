# No-Dynamic-Arbitrage and Market Impact

**Authors:** Jim Gatheral (Bank of America Merrill Lynch; Courant Institute, NYU)  
**Year:** 2010  
**Journal/Venue:** *Quantitative Finance*, Vol. 10, No. 7, pp. 749--759 (received Oct 2008; DOI 10.1080/14697680903373692)  
**Source file:** `Finance/MarketImpact_gatheral_2010.pdf`

## Question

A transient-impact model needs two ingredients: an instantaneous impact function $f(v)$ and a decay kernel $G(\tau)$. The literature picks each independently: linear, power or log impact, combined with exponential or power-law decay. The paper asks which pairs are *consistent*, meaning that no round trip has negative expected cost. The answer rules out the popular combination of exponential decay with concave impact. It also ties the exponents of the square-root law to the decay of impact and to the long memory of order signs.

## Model

$$S_t=S_0+\int_0^t f(\dot x_s)\,G(t-s)\,ds+\int_0^t\sigma\,dZ_s, \tag{1}$$
- $\dot x_s$ is the dollar trading rate, and time is business (volume) time.
- $f$ and $G$ are *unconditional* averages. They mimic how pre-trade cost models are fitted: bucket all VWAP executions and ignore book state or flow history. They do not apply to state-conditioned (liquidity-seeking) strategies.
- (1) is the continuous-time limit of the propagator $S_t=\sum_{i<t}f(\delta x_i)G(t-i)+\text{noise}$, which is the Bouchaud–Gefen–Potters–Wyart (BGPW) picture. Via Bouchaud–Farmer–Lillo (2008), it is also the Lillo–Farmer picture of permanent but state-dependent impact, provided agents forecast flow with a linear ARFIMA model.
- Gerig (2007) finds that LSE hidden-order data reject this form.

Special cases:
- Almgren et al. (2005): $G=\delta$, $f(v)=\eta\sigma v^{0.6}$ with $v=\dot x/V$. Cost is $\int \dot x_t^{1+\beta}dt$.
- Obizhaeva–Wang: $G=e^{-\rho\tau}$, $f\propto v$. Alfonsi–Fruth–Schied (2010) use the same exponential decay but with nonlinear $f$.
- Bouchaud et al. (2004): $f\propto\log v$, $G\propto(l_0+\tau)^{-\gamma}$.

Expected cost, which equals expected implementation shortfall, ignores slippage (spread and other frictions):
$$C[\Pi]=\int_0^T\dot x_t\,dt\int_0^t f(\dot x_s)G(t-s)\,ds .$$

**No-dynamic-arbitrage.** Every round trip ($\int_0^T\dot x_t dt=0$) must have $C[\Pi]\ge 0$. This is a condition on expected P&L only: it is not scalable and says nothing about Sharpe ratio. It is *weaker* than Huberman–Stanzl quasi-arbitrage or Bernardo–Ledoit approximate arbitrage, and closer to statistical arbitrage.

## Results

**Permanent impact ($G\equiv1$).** Buying at $+v$ and then selling at $-v$ costs $\propto vT^2\{-f(-v)-f(v)\}$, which forces $f$ to be odd (Huberman–Stanzl). If $f=\eta v$, then $C=\tfrac{\eta}{2}(x_T-x_0)^2$, which is zero for any round trip. A linear permanent component can therefore be added to any model without changing the results below.

**Test strategy.** Buy at rate $v_1$ for $\theta T$, then sell at $v_2$ for $(1-\theta)T$, with $\theta=v_2/(v_1+v_2)$. The cost is $C_{11}+C_{22}-C_{12}$. The cross term $C_{12}$ is the cost of the sales caused by the impact of the earlier purchases. Manipulation needs $C_{12}$ to dominate, so it requires $G$ to have memory. If $G$ is strictly decreasing, trading in and out at the *same* rate is never profitable, so any manipulation must use different rates.

**Exponential decay.** The integrals have closed forms. The paper's example uses $f=\sqrt v$, $v_1=0.2$, $v_2=1$ and $\rho T=1$, and gets $C=-0.001705<0$. Expanding in $\rho T$ gives
$$\frac{v_1v_2\,[v_1f(v_2)-v_2f(v_1)]}{2(v_1+v_2)^2}(\rho T)^2+O((\rho T)^3)\ge0 \;\;\forall v_1,v_2 \;\Rightarrow\; f(v)\propto v .$$
- **Lemma 4.1:** exponential decay is arbitrage-free only with linear $f$.
- **Corollary 4.2** ($\rho\to0$): nonlinear permanent impact is inconsistent.
- Empirically $f$ is concave for moderate $v$ and convex for very large $v$, when a trade exhausts the book. Exponential decay is therefore rejected as a realistic assumption.
- A footnote cites Friz et al.: linear $f$ is consistent with *any* convex non-increasing $G$. Schied et al. were working on a full characterization.

**Power-law decay** $G(\tau)=\tau^{-\gamma}$, $0<\gamma<1$. With $\theta=v_2/(v_1+v_2)$ the master inequality is
$$f(v_1)\{v_1v_2^{1-\gamma}-(v_1+v_2)^{2-\gamma}+v_1^{2-\gamma}+v_2^{2-\gamma}\}+f(v_2)\,v_1^{2-\gamma}\ge0. \tag{8}$$
Limiting cases: $\gamma=0$ requires $f\propto v$, and $\gamma=1$ imposes no constraint when $f\ge 0$.

- **Slow build, fast exit** ($v_1=\epsilon v$, $\epsilon\to0$): $\dfrac{f(\epsilon v)}{f(v)}\le\dfrac{\epsilon^{1-\gamma}}{1-\gamma}$. With $f\propto v^\delta$ this gives **Lemma 5.1: $\gamma+\delta\ge1$**.
- **Log impact** $f=\log(v/v_0)$, the $\delta\to0$ limit. Take $v_0=0.001$, which corresponds to one average-size print per trade for a stock trading 10M shares/day in 10,000 trades. Then $v_1=0.15$, $v_2=1$, $\gamma=1/2$ give $C=-0.0028$. For any $\gamma<1$, manipulation exists once $v_0$ is small enough, so the BGPW log specification is internally inconsistent.
- **Pump and dump** (fast build, slow exit; $v=v_2/v_1<1$): $f(v_1)h(v,\gamma)+f(v_2)\ge0$ with $h=v^{1-\gamma}-(1+v)^{2-\gamma}+1+v^{2-\gamma}$. Appendix A shows that $h<0$ for some $v\in(0,1)$ iff $\gamma<\gamma^*=2-\log 3/\log 2\approx0.415$, with the worst case near $v\to1$. Trading speed is bounded by $v_{\max}$ (exhausting the book). If $f(v)\sim(v_{\max}-v)^{-\nu}$ as $v\to v_{\max}$, taking $v_1=1-\epsilon^2$ and $v_2=1-\epsilon$ yields **Lemma 5.2: $\gamma\ge\gamma^*$** for any $\nu>0$.

## Stylized facts

1. **Diffusivity.** BGPW argue as follows. Suppose trade signs have autocorrelation $\propto|i-j|^{-\alpha}$ with $\alpha<1$ and impact is permanent. Then $\mathrm{Var}[\Delta P]\sim N^{2-\alpha}$, which is superdiffusive and would make trend-following profitable. Diffusion therefore requires transient impact with $\gamma=(1-\alpha)/2$. France Télécom has $\alpha\approx0.2$, so $\gamma\approx0.4$. Long memory ($\alpha>0$) implies $\gamma<1/2$.
2. **Square-root law.** Cost $=$ spread $+\,c\,\sigma\sqrt{n/V}$. This matches the Grinold–Kahn rule of thumb (one day's volatility to trade one day's volume), the Barra handbook fits, and the weak duration dependence in Engle–Ferstenberg–Russell (2008), for participation of roughly 1–25%. In model (1), a VWAP execution over duration $T$ costs in total $\propto v f(v)T^{2-\gamma}$. Per share, that is $\propto (n/V)^{\delta}\,T^{1-\gamma-\delta}$. Independence from duration forces **$\gamma+\delta=1$**, exactly the no-arbitrage boundary. $\gamma=\delta=1/2$ gives the square root. The empirical pair $\gamma\approx0.4$ (BGPW) and $\delta\approx0.6$ (Almgren et al.) also sums to 1. The paper's point is that these inequalities are "typically close to being equalities".
3. **Book tail.** The Bouchaud–Mézard–Potters (2002) average book with limit-order placement exponent $\mu=0.6$ gives a virtual impact $\Delta P\sim(n_{\max}-n)^{-1/\mu}$. This is convex for large size, which validates the premise of Lemma 5.2, so $\gamma\ge\gamma^*$. At very high rates $\delta$ can leave the boundary; for example $1/\mu\approx1.67$.

**Constraint on sign memory.** Combining $\gamma=(1-\alpha)/2$ with $\gamma\ge\gamma^*$ gives
$$\alpha\le1-2\gamma^*\approx0.17 .$$
This is roughly consistent with BGPW's $\alpha\approx0.2$. It is inconsistent with Bouchaud et al. (2006), where $\alpha$ ranges from 0.125 to 0.69, with Lillo–Farmer ($\alpha\approx0.6$), and with Lillo–Mike–Farmer's order-splitting explanation. The paper offers three readings: (a) pump-and-dump at high participation is impractical or illegal; (b) manipulation actually exists; or, most interesting, (c) model (1) is too simple. In particular, the separable product of a volume factor and a time factor may fail if decay depends on size, or if agents condition on more than linear flow forecasts (Gerig; Bouchaud–Farmer–Lillo). The paper's Fig. 3 shows the admissible region $\{\gamma+\delta\ge1,\ \gamma\ge\gamma^*,\ \gamma\le1/2\}$.

## Caveats stated by the author

- All conditions are **necessary only**. They come from two-rate, piecewise-constant strategies. Richer or discrete strategies could tighten them, and sufficiency is not proven.
- Ignoring slippage makes every inequality conservative. With spread costs, the admissible region is larger.
- Unconditional manipulation implies conditional manipulation, but not the converse.

## Assessment

- **Convincing.** The exponential-decay result is exact and robust. For a quant, the clean takeaway is that **a concave (e.g. square-root) impact function combined with exponentially decaying impact is not arbitrage-free**. A multi-period optimizer built on that combination can find spurious round trips that "earn" negative impact cost. Either keep $f$ linear with an exponential kernel, as in Obizhaeva–Wang, or use power-law decay with $\gamma+\delta\ge1$.
- **Useful calibration heuristic.** If the cost per share of your VWAP executions is flat in duration at fixed size, then $\gamma\approx1-\delta$.
- **Fragile.** The $\gamma^*$ bound depends on a singular, factorized kernel and on extrapolating to trading rates near book exhaustion. The empirical point $(\gamma,\delta)\approx(0.4,0.6)$ actually sits just below $\gamma^*\approx0.415$. The $\alpha\le0.17$ prediction contradicts most sign-memory estimates, which points to misspecification of (1), not a market anomaly. Later work (Gatheral–Schied–Slynko, Alfonsi–Schied–Slynko) moved to linear-transient models, where the relevant condition is positive definiteness of $G$ and where transaction-triggered manipulation is also studied. That work supersedes the two-rate test used here.
- The PDF's keyword list (stochastic/local volatility terms) is a publisher error unrelated to the content.

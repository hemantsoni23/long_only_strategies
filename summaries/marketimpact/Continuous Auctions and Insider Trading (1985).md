# Continuous Auctions and Insider Trading

**Authors:** Albert S. Kyle  
**Year:** 1985  
**Journal/Venue:** *Econometrica*, Vol. 53, No. 6, pp. 1315--1335  
**Source file:** Finance/MarketImpact_Kyle_1985.pdf

## Question

How fast is private information impounded into prices, what determines market depth, and what is private information worth, when a single insider trades strategically against competitive market makers who see only aggregate order flow? The answers (depth, informativeness, insider profit) are derived from optimization rather than assumed.

## Setup

- One risky asset, liquidation value $\tilde v \sim N(p_0, \Sigma_0)$.
- Noise-trader cumulative order $\tilde u(t)$: Brownian motion with instantaneous variance $\sigma_u^2$, independent of $\tilde v$.
- A risk-neutral insider knows $v$ and past prices (hence past own trades); submits market orders; cannot condition on the current price. No commitment: each trade must be optimal given current information (sequential-equilibrium flavor, Kreps--Wilson).
- Competitive risk-neutral market makers see only total order flow and set $p = E[\tilde v \mid \text{order-flow history}]$ (semi-strong efficiency; zero expected profit, interpretable as the outcome of Bertrand competition).
- All results are for **linear** equilibria. Kyle states he suspects, but cannot prove, that nonlinear equilibria do not exist.

## Single auction (Theorem 1)

With $P(y)=\mu+\lambda y$, the insider solves $\max_x (v-\mu-\lambda x)x$, giving $x = (v-\mu)/(2\lambda)$, i.e. $\beta = 1/(2\lambda)$. The projection theorem gives $\lambda = \beta\Sigma_0/(\beta^2\Sigma_0+\sigma_u^2)$. Solving:

$$X(v)=\beta(v-p_0),\quad P(y)=p_0+\lambda y,\qquad \beta=\Big(\frac{\sigma_u^2}{\Sigma_0}\Big)^{1/2},\quad \lambda=\frac{1}{2}\Big(\frac{\Sigma_0}{\sigma_u^2}\Big)^{1/2}.$$

(The printed statement of Theorem 1 gives $\lambda$ as $2(\sigma_u^2/\Sigma_0)^{-1/2}$; this is inconsistent with the paper's own FOC $1/\beta = 2\lambda$ -- the correct factor is $1/2$.)

- $\Sigma_1=\operatorname{var}(v\mid p)=\Sigma_0/2$: half of the information is revealed; price variability is independent of $\sigma_u$.
- Depth $1/\lambda = 2\sigma_u/\Sigma_0^{1/2}$: proportional to noise, inversely proportional to information (Bagehot's adverse-selection story made rigorous).
- Conditional profit $(v-p_0)^2/(4\lambda)$; unconditional $E\pi = \tfrac12(\Sigma_0\sigma_u^2)^{1/2}$ -- borne entirely by noise traders.
- More noise trading draws proportionally more informed trading, so it does not destabilize prices (this would fail with a risk-averse insider).

## Sequential auctions (Theorem 2)

$N$ auctions at $0=t_0<\dots<t_N=1$, noise trade $\Delta u_n \sim N(0,\sigma_u^2\Delta t_n)$. The unique linear equilibrium is recursive:

$$\Delta x_n=\beta_n(v-p_{n-1})\Delta t_n,\qquad \Delta p_n=\lambda_n(\Delta x_n+\Delta u_n),$$

with value function $E[\pi_n\mid\cdot]=\alpha_{n-1}(v-p_{n-1})^2+\delta_{n-1}$ and

$$\alpha_{n-1}=\frac{1}{4\lambda_n(1-\alpha_n\lambda_n)},\quad \delta_{n-1}=\delta_n+\alpha_n\lambda_n^2\sigma_u^2\Delta t_n,\quad \beta_n\Delta t_n=\frac{1-2\alpha_n\lambda_n}{2\lambda_n(1-\alpha_n\lambda_n)},$$
$$\lambda_n=\beta_n\Sigma_n/\sigma_u^2,\qquad \Sigma_n=(1-\beta_n\lambda_n\Delta t_n)\Sigma_{n-1},$$

$\alpha_N=\delta_N=0$, second-order condition $\lambda_n(1-\alpha_n\lambda_n)>0$.

Proof logic: (1) backward induction shows the continuation value is quadratic, so linear strategies are optimal even among nonlinear ones; an extra linear term $h$ in the price rule must vanish by market efficiency, so the equilibrium is recursive. (2) Projection gives $\lambda_n,\Sigma_n$ from $\beta_n,\Sigma_{n-1}$. (3) Combining yields a cubic in $\lambda_n$, $(1-\lambda_n^2\sigma_u^2\Delta t_n/\Sigma_n)(1-\alpha_n\lambda_n)=\tfrac12$, whose middle root is the only one satisfying the SOC; a scaling argument ($\Sigma_N\mapsto\zeta^2\Sigma_N$) pins the unique terminal $\Sigma_N$ matching $\Sigma_0$.

Interpretation of the SOC: it bounds $\lambda_n$ above as a decreasing function of $\alpha_n$, ruling out schemes where the insider loses money to push the price away from $v$ and then recoups more later. Intuition for the dynamics: if future depth exceeds current depth the insider "saves" information; if it declines he trades harder now.

Properties: $\Sigma_n$ decreasing but $\Sigma_N>0$ (not all information revealed with finite $N$). Doubling $\sigma_u$ halves $\lambda_n$, doubles $\beta_n,\alpha_n,\delta_n$, leaves $\Sigma_n$ unchanged. Ex ante profit $\propto(\Sigma_0\sigma_u^2)^{1/2}$.

## Continuous auctions (Theorem 3, heuristic)

$$dx=\beta(t)(v-p)\,dt,\qquad dp=\lambda(t)(dx+du),\qquad d\pi=(v-p)\,dx.$$

Trades are priced at the **end** of the instant. For the smooth insider the $dp\,dx$ term is $O(dt^{3/2})$ and immaterial, but $du\,dp=\lambda\sigma_u^2dt$ is first order: noise traders pay for moving the price against themselves, which is exactly what makes market makers break even. Beginning-of-instant pricing would invite unbounded insider trades.

With $\Sigma^*(t)=E(v-p)^2$ and $d\Sigma^*/dt=-2\lambda\beta\Sigma^*+\lambda^2\sigma_u^2$, eliminating the control $\beta$ gives

$$E\pi(0)=\tfrac12\int_0^1\lambda(t)\sigma_u^2\,dt+\tfrac12\int_0^1\lambda(t)^{-1}\,d(-\Sigma^*(t)),$$

a problem in the state $\Sigma^*\ge0$ alone. Then:

- Optimality requires $\Sigma^*(1)=0$.
- If $\lambda$ ever **decreases** (depth rises), the insider can raise $\Sigma^*$ by a large amount before and lower it after -- unbounded profit. So $\lambda$ is nondecreasing. (Intuition: accumulating a position in small parcels along a linear supply curve and unwinding on a flatter curve.)
- If $\lambda$ ever **increases**, the insider drives $\Sigma^*$ to zero where $\lambda$ is minimal, i.e. before $t=1$, after which prices stop moving -- inconsistent with nondecreasing $\lambda$.
- Hence $\lambda$ is constant; with constant $\lambda$ any attainable path with $\Sigma^*(1)=0$ is optimal, and market efficiency selects the equilibrium one. Since $\operatorname{var}(dp)=\lambda^2\sigma_u^2dt$ must integrate to $\Sigma_0$:

$$\lambda=\Big(\frac{\Sigma_0}{\sigma_u^2}\Big)^{1/2},\quad \Sigma(t)=(1-t)\Sigma_0,\quad \beta(t)=\frac{\sigma_u^2\lambda}{\Sigma(t)}=\frac{\sigma_u\Sigma_0^{-1/2}}{1-t},$$
$$\alpha(t)=\tfrac12(\sigma_u^2/\Sigma_0)^{1/2}\ (t<1),\qquad \delta(t)=\tfrac12(\sigma_u^2\Sigma_0)^{1/2}(1-t).$$

($\lambda=\beta\Sigma/\sigma_u^2$ is the Kalman-filter regression coefficient.)

Consequences:
- Prices are, to market makers, a driftless Brownian motion with variance $\Sigma_0$ per unit time; information enters at a constant rate and is fully revealed at $t=1$ ($p(t)\to v$ in mean square).
- Volatility is generated by noise trading; the insider's volume is small, but his trades are serially correlated, so he determines the terminal price.
- Ex ante insider profit $=\Sigma_0^{1/2}\sigma_u$, exactly double the one-shot value.
- Liquidity in Black's sense: **tightness** infinite in continuous time (round trips are costless because the insider walks along the supply curve like a discriminating monopsonist; not so with discrete auctions); **depth** $1/\lambda$ constant (time-varying in the discrete model); **resiliency**, driven entirely by the insider through $\beta(t)$, increases in $t$ and becomes infinite as $t\to1$.

## Convergence (Theorem 4)

As the mesh $\to0$, the discrete equilibrium converges to Theorem 3: uniformly on $[0,1]$ for $\Sigma,\delta$; uniformly on closed sets excluding $t=1$ for $\lambda,\beta,\alpha$ (the boundary $\alpha_N=0$ versus $\alpha(t)\to\tfrac12\sigma_u\Sigma_0^{-1/2}$ creates a discontinuity at $t=1$ that defeats standard ODE convergence theorems). The system is reduced to a scalar recursion in $\phi_n=4\alpha_n^2\Sigma_n/\sigma_u^2$ with $\phi_N=0$, solved backward via a cubic; the economic root satisfies $-5/4<(\phi_n-\phi_{n-1})/\Delta t_n<-1$ and $\to-1$, so $\phi(t)\to1-t$; then $\Sigma'/\Sigma=-1/(1-t)$ gives $\Sigma(t)=(1-t)\Sigma_0$. This also gives a practical algorithm: iterate $\phi$ backward, $\Sigma$ forward, then recover $\alpha,\beta,\lambda$. Figure 1 ($\Sigma_0=\sigma_u^2=1$, equally spaced, $N=4,20,100$) shows $\lambda_n$ and $\Sigma_n$ approaching the continuous values $\lambda=1$, $\Sigma=1-t$.

## Assessment

**Convincing / durable.** The central insight -- price impact per unit of order flow is an adverse-selection object, $\lambda=\sigma_v/\sigma_u$ (the ratio of information to noise, in square-root units), and efficient prices are compatible with a monopolist insider -- is clean and robust across the one-shot, discrete and continuous versions. Linear permanent impact is the equilibrium, not an assumption; the no-arbitrage argument for constant depth (time-varying $\lambda$ invites manipulation) prefigures the no-dynamic-arbitrage conditions later used in the execution literature (Huberman--Stanzl, Gatheral).

**Fragile.**
- Linearity: uniqueness is within linear equilibria only; Theorem 3 is explicitly heuristic, and its rigor comes from Theorem 4.
- Gaussian, risk-neutral, single insider, market orders only, one asset, exogenous price-insensitive noise trading, known terminal date (hence the $\beta(t)\to\infty$ singularity as $t\to1$).
- No inventory, spreads, tick size, or market-maker compensation; the model says nothing about temporary impact, which dominates practical execution costs.
- Constant depth is a property of this stylized economy; empirically, intraday depth and impact vary strongly.

**Practical relevance for a quant PM.** Kyle's $\lambda$ is the canonical permanent-impact coefficient and the origin of the square-root-of-variance-over-volume scaling intuition ($\lambda\propto\sigma/\sqrt{\text{noise volume}}$) used in impact models; regressions of returns on signed order flow estimate it. The insider's strategy -- trade linearly in the mispricing, intensity rising as the horizon shortens, hidden inside noise flow -- is a useful template for alpha-driven trading, but a real PM is not a monopolist with a known deadline and faces temporary costs, so the model is a benchmark rather than an execution rule. Extensions: multiple insiders (Holden--Subrahmanyam; Back--Cao--Willard), limit orders (Kyle's companion "Equilibrium in a Speculative Market with Strategic Informed Trading"), and the Glosten--Milgrom sequential-trade alternative.

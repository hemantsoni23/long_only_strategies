# The Volatility Surface: A Practitioner's Guide — Detailed Quantitative Research Notes

**Author:** Jim Gatheral · **Foreword:** Nassim Nicholas Taleb · **Year:** 2006 · **Publisher:** John Wiley & Sons (Wiley Finance), ISBN 978-0-471-79251-2 · **Origin:** Courant Institute (NYU) lecture notes  
**Source file:** `Finance/(Wiley Finance) Jim Gatheral, Nassim Nicholas Taleb - The Volatility Surface_ A Practitioner's Guide (Wiley Finance)-Wiley (2006).pdf` (Drive text extraction covers front matter and Ch. 1–4 only; Ch. 5–11 details below are retained from earlier notes and checked only against the table of contents and figure/table captions.)

---

## Programme

Black–Scholes implied volatility $\sigma_{BS}(K,T)$ is a *quoting convention*; the surface it spans encodes the risk-neutral marginals but not the dynamics. Gatheral's agenda:

1. Connect implied, local and instantaneous variance exactly (Ch. 1, 3).
2. Show which model classes can reproduce the SPX surface — stochastic volatility (SV) alone fits the back but not the front; adding jumps (SVJ) fixes the front (Ch. 2–5).
3. Characterize the surface via asymptotics — short, long and small vol-of-vol expansions and extreme strikes (Ch. 7).
4. Show that models agreeing on all vanillas can disagree sharply on forward-skew-dependent exotics: digital cliquets, barriers, Mediobanca cliquets, Napoleons (Ch. 8–10).
5. Isolate what *is* model-independent: variance swaps via the log strip (Ch. 11).

Taleb's foreword sets the epistemology: models are tools for consistent *relative* pricing across instruments, not statistical descriptions of reality.

Empirical anchors:
- SPX daily log returns 31 Dec 1984 – 31 Dec 2004, and 77 years of daily returns vs. the normal distribution, both featuring the −22.9% return of 19 Oct 1987.
- The SPX surface at the close of **15 Sep 2005** (day before triple witching), SPX = 1227.73.

---

## Chapter 1 — Stochastic Volatility and Local Volatility

**SV valuation.** Take the model
$$dS_t=\mu_tS_t\,dt+\sqrt{v_t}S_t\,dZ_1,\qquad dv_t=\alpha(S,v,t)dt+\eta\beta(S,v,t)\sqrt{v_t}\,dZ_2,\qquad \langle dZ_1dZ_2\rangle=\rho\,dt.$$
Hedging with stock and a second option gives a PDE in which the drift of $v$ appears as $\alpha-\phi\beta\sqrt v$. Here $\phi$ is the market price of volatility risk, and it is absorbed into a risk-neutral drift. A delta-hedged but not vega-hedged position earns $\beta\sqrt v\,\partial_vV(\phi\,dt+dZ_2)$, a CAPM-like interpretation of $\phi$. Thereafter all models are written risk-neutrally and fitted to option prices.

**Local volatility.**
- Breeden–Litzenberger: $\partial_{KK}C=\varphi(K,T)$.
- Dupire (1994) / Derman–Kani give the unique diffusion consistent with all Europeans:
$$\partial_TC=\tfrac12\sigma^2(K,T)K^2\partial_{KK}C+(r-D)(C-K\partial_KC).$$
- In terms of total implied variance $w=\sigma_{BS}^2T$ and $y=\log(K/F_T)$:
$$v_L=\frac{\partial_Tw}{1-\dfrac{y}{w}\partial_yw+\dfrac14\Big(-\dfrac14-\dfrac1w+\dfrac{y^2}{w^2}\Big)(\partial_yw)^2+\dfrac12\partial_{yy}w}.$$
  With no skew, $v_L=\partial_Tw$ (forward variance). A negative denominator signals butterfly arbitrage in the input surface.
- **Key identity** (Dupire 1996; Derman–Kani 1998), obtained by applying Itô/Tanaka to $(S_T-K)^+$:
$$\sigma_L^2(K,T)=\mathbb E[v_T\mid S_T=K].$$
  Local variance is the risk-neutral expectation of instantaneous variance conditional on the final spot equal to the strike. This is the workhorse of the whole book.
- Local vol is an *effective* theory: Dumas–Fleming–Whaley reject it as a model of surface dynamics.

## Chapter 2 — The Heston Model

**Model.**
$$dv=-\lambda(v-\bar v)dt+\eta\sqrt v\,dZ_2.$$
The forward-value call is $C=K[e^xP_1-P_0]$ with $x=\log(F/K)$. The $P_j$ solve a PDE with coefficients $a=\lambda\bar v$, $b_j=\lambda-j\rho\eta$. The affine ansatz $\tilde P_j=\frac1{iu}\exp\{C(u,\tau)\bar v+D(u,\tau)v\}$ reduces it to a Riccati equation:
$$D=r_-\frac{1-e^{-d\tau}}{1-ge^{-d\tau}},\qquad C=\lambda\Big[r_-\tau-\frac2{\eta^2}\log\frac{1-ge^{-d\tau}}{1-g}\Big],$$
where $r_\pm=(\beta\pm d)/\eta^2$, $d=\sqrt{\beta^2-4\alpha\gamma}$, $g=r_-/r_+$.

**Complex-log digression.** Written this way, the logarithm in $C$ stays on the principal branch and avoids the discontinuities that plague the original Heston form of the integrand (2.13).

**Simulation.**
- Euler discretization gives negative variances.
- The **Milstein** scheme costs the same and largely alleviates this, so it is "always to be preferred". Gatheral notes a condition in terms of $\bar v/\eta^2$ (the Feller-type ratio) for when it works well.
- Exact sampling (Broadie–Kaya 2004) uses the non-central $\chi^2$ transition of $v_t$, then $\int v\,ds$, then $S_t$; Andersen–Brotherton-Ratcliffe offer a moment-matched shortcut.

**Why Heston is popular.** Its quasi-closed-form Europeans make calibration feasible. With suitable parameters, *all* SV models give roughly the same surface shape and similar exotic implications, so the cheap one wins despite unrealistic dynamics.

## Chapter 3 — The Implied Volatility Surface

**Implied variance as a path average.** Applying Itô to $C_{BS}(S_t,\sigma(t))$ and requiring zero expected hedging P&L gives
$$\sigma_{BS}^2(K,T)\,T=\int_0^T\mathbb E^{\mathbb G_t}[v_t]\,dt.$$
This is a **gamma-weighted** average of instantaneous variance ($\mathbb G_t$ weights paths by $S_t^2\Gamma_{BS}$). Equivalently, it is local variance integrated against a Brownian-bridge-like density concentrated near the most probable path from spot to strike (Fig. 3.1).

Approximation: $\sigma_{BS}^2(K,T)\approx\frac1T\int_0^Tv_L(\tilde x_t,t)dt$ along that path. Two consequences:
- For short expiries, implied variance ≈ the average of local variance at spot and at strike.
- Hence the **implied skew ≈ ½ the local skew**.

**Heston local and implied vol.** Using $\sigma_L^2=\mathbb E[v_T|x_T]$ and the ansatz $\mathbb E[x_s|x_T]\approx x_T\hat w_s/\hat w_T$ gives approximate closed forms. With $\lambda'=\lambda-\rho\eta/2$:
$$\sigma_{BS}^2\big|_{ATM}\approx(v-\bar v')\frac{1-e^{-\lambda'T}}{\lambda'T}+\bar v',\qquad \partial_k\sigma_{BS}^2\big|_{k=0}\approx\frac{\rho\eta}{\lambda'T}\Big\{1-\frac{1-e^{-\lambda'T}}{\lambda'T}\Big\}.$$
The skew decays like $1/T$ at long maturities and tends to a constant as $T\to0$.

**SVI.** Gatheral (2004), "stochastic volatility inspired":
$$\sigma_{BS}^2(k)\,T=a+b\{\rho(k-m)+\sqrt{(k-m)^2+\sigma^2}\}$$
with parameters per expiry. In the book it is fitted **to all expirations simultaneously subject to no calendar-spread arbitrage**, then total variance is interpolated between slices with Stineman monotone splines (Fig. 3.2 surface; Fig. 3.3 fits to bid/offer vols for eight expiries).

**Table 3.1 — SPX ATM variance and ATM variance skew $\partial_k\sigma_{BS}^2$, 15 Sep 2005:**

| Expiry | T | ATM var | ATM skew |
|---|---|---|---|
| Sep-05 | 1 day | 0.0109 | −0.0955 |
| Oct-05 | 1m | 0.0123 | −0.1601 |
| Nov-05 | 2m | 0.0149 | −0.1372 |
| Dec-05 | 3m | 0.0161 | −0.1221 |
| Mar-06 | 6m | 0.0183 | −0.0945 |
| Jun-06 | 9m | 0.0195 | −0.0815 |
| Dec-06 | 15m | 0.0209 | −0.0679 |
| Jun-07 | 21m | 0.0220 | −0.0594 |

The ATM variance term structure is fitted well by the Heston formula. The skew term structure is not: fitting (3.21) with or without the first three points shows the formula is "too stiff". Observed skew grows much faster as $T\to0$ than any time-homogeneous SV model allows, so **jumps are needed** — and this is one reason practitioners prefer local vol.

**Table 3.2 — Heston fit (15 Sep 2005):**

| $v_0$ | $\bar v$ | $\eta$ | $\rho$ | $\lambda$ |
|---|---|---|---|---|
| 0.0174 | 0.0354 | 0.3877 | −0.7165 | 1.3253 |

Implied values: spot vol ≈13.2%, long-run ≈18.8%, variance half-life ≈0.52y. Fig. 3.6 shows the fit is good for long expiries and poor for short ones (the Heston surface is plotted shifted down 5 vol points for visibility).

## Chapter 4 — The Heston–Nandi Model

**Setup.** With $\rho=-1$ there is one Brownian driver: the preference-free continuous-time limit of Heston–Nandi GARCH, with no volatility risk premium. The model is one-factor but not Markov in $S$. Rewriting $dv$ in terms of $dx$ gives $\lambda'=\lambda+\eta/2$, $\bar v'=\bar v\lambda/\lambda'$, and approximate local variance
$$v_L(x_T,T)\approx(v_0-\bar v')e^{-\lambda'T}+\bar v'-\eta x_T\,\frac{1-e^{-\lambda'T}}{\lambda'T},$$
floored at zero: the density has a hard right cutoff, so very high strikes are unattainable.

**Book-wide laboratory parameters:** $v_0=\bar v=0.04$, $\lambda=10$, $\eta=1$, $\rho=-1$. Local vols from the Dupire ratio agree closely with the formula, and European implied vols from Heston and from the local-vol model (a PDE with these local vols) coincide (Figs. 4.2–4.3).

**Moral:** fitting all Europeans does not determine prices; one must assume dynamics. In local vol, future volatilities are known in advance; in SV they are uncertain. This pair is used in Ch. 9–10 to isolate the effect of dynamics on exotics.

## Chapter 5 — Adding Jumps

**Why jumps.** Table 5.1 lists Sep-05 (one-day) SPX option quotes on 15 Sep 2005. Far-OTM overnight options have firm bids: e.g., the 1160 put bid 0.05/0.25 and the 1250 call bid 0.05/0.10. The earlier notes record these as ≈13.7σ and ≈4.7σ moves under a diffusion calibrated to the ATM level. No diffusion can justify them, and the one-day smile (Fig. 5.1) is far steeper than the Heston skew.

**Jump-diffusion.** $dS/S=\mu\,dt+\sigma\,dZ+(J-1)dq$. The risk-neutral PIDE carries the compensator $\mu_J=-\lambda\mathbb E[J-1]$. With an uncertain jump size, perfect replication is impossible.

**Characteristic-function toolkit.**
- Lévy–Khintchine representation.
- Merton characteristic function: $\phi_T(u)=\exp\{iu\omega T-\tfrac12u^2\sigma^2T+\lambda T(e^{iu\alpha-u^2\delta^2/2}-1)\}$.
- Lewis's formula:
$$C=S-\sqrt{SK}\frac1\pi\int_0^\infty\frac{du}{u^2+1/4}\mathrm{Re}\big[e^{-iuk}\phi_T(u-i/2)\big].$$
- A matching closed-form integral for the ATM skew.

**Short-maturity jump skew:** $\partial_k\sigma_{BS}^2|_{k=0}\approx-2\mu_J$. Jump skew decays over a characteristic time $T^*$ at which the jump size is comparable to one diffusion standard deviation. Beyond that the CLT restores normality: $T^*\approx0.67$ for the Table 5.2 parameters ($\sigma=0.2$; $(\lambda,\alpha,\delta)=(0.5,-0.15,0.05),(1,-0.07,0),(1,-0.07,0.05)$).

**SVJ vs. SVJJ.**
- SVJ is Heston plus lognormal jumps in $S$; SVJJ adds simultaneous jumps in $v$ (Bakshi–Cao–Chen and Duffie–Pan–Singleton-type parameterizations).
- The ATM skew of SVJ ≈ Heston skew + jump skew (additive).
- SVJJ adds little at the short end, because a jump in $v$ does not immediately affect the smile.
- The SVJ fit to 15 Sep 2005 (Fig. 5.9) reproduces the major features of the surface. **SVJ wins:** it is parsimonious and fits both ends.

## Chapter 6 — Modeling Default Risk

**Merton jump-to-ruin.** The stock jumps to zero at hazard $\lambda$, which is roughly the credit spread. This lifts low-strike vols (Fig. 6.1: 3m vols with 20% diffusion vol and spreads of 100/200/300 bp).

**Capital-structure arbitrage.** Put-call parity with default and a 1×2 put spread (long 1.0-strike put, short two 0.5-strike puts) produce arbitrage bounds on deep-OTM put vols given a CDS spread (Table 6.1). Table 6.2 compares Goodyear (GT = 9.40, 20 Oct 2004, Jan-05 options) market vols with a Merton jump-to-ruin fit.

**CreditGrades.** An industry structural model with an uncertain default barrier, covering survival probability, the link between equity vol and leverage, and calibration to CDS and equity options.

## Chapter 7 — Volatility Surface Asymptotics

- **Short expiries (Medvedev–Scaillet).** For SV, the ATM skew tends to $\rho\,b(\sigma)/(2\sigma)$ as $T\to0$, where $b$ is the diffusion coefficient of $\sigma$. This is *time-homogeneous*, unlike local vol, whose forward skews decay.
- **SABR** (short expiries; no mean reversion):
  - model: $dS=\sigma S^\beta dZ_1$, $d\sigma=\chi\sigma\,dZ_2$;
  - Hagan et al. formula for $\beta=1$: $\sigma_{BS}(k)\approx\sigma_0\frac{y}{f(y)}\{1+[\tfrac14\rho\chi\sigma_0+\tfrac{2-3\rho^2}{24}\chi^2]\tau\}$, with $y=-\chi k/\sigma_0$;
  - ATM skew $\rho\chi/2$, consistent with Medvedev–Scaillet.
- **With jumps.** The short-end variance skew is $\rho\,b-2\mu_J$ (per the earlier notes): SV and jump contributions add exactly at $\tau=0$.
- **Long expiries (Fouque–Papanicolaou–Sircar).** Skew ∝ $1/T$. Gatheral's interpolation between the short and long limits:
$$\partial_k\sigma_{BS}^2\approx\frac{\rho\eta\beta(v)}{\lambda'T}\Big\{1-\frac{1-e^{-\lambda'T}}{\lambda'T}\Big\},\quad\lambda'=\lambda-\tfrac12\rho\eta\beta(v).$$
- **Small vol-of-vol (Lewis 2000).** A power-series expansion in $\eta$ of implied variance in $k$, which agrees with the formula above to $O(\eta)$.
- **Extreme strikes (Lee 2004 moment formula).** The wing slope $\limsup\sigma_{BS}^2T/|k|\in[0,2]$ is tied to the moment explosion: left wing via $q^*=\sup\{q:\mathbb E[S_T^{-q}]<\infty\}$, $\beta^*=2-4(\sqrt{q^{*2}+q^*}-q^*)$; right wing analogous. Benaim–Friz give conditions under which limsup becomes lim. Heston has asymptotically linear wings in $k$.
- **Conclusion:** the *shape* of the surface is generic across SV(J) models; dynamics distinguish them.

## Chapter 8 — Dynamics of the Volatility Surface

**Empirical rule.** The volatility skew $\partial_k\sigma_{BS}$ is roughly **independent of the vol level**. So the variance skew $\partial_k\sigma^2$ scales like $\sqrt v$. Since the short-end variance skew scales like $\beta(v)/\sqrt v$, this requires $\beta(v)\propto v$ — i.e., **lognormal** variance dynamics, not Heston's square root. Heston's vol skew flattens as vol rises (∝ $1/\sqrt v$), so it under-hedges skew in high-vol regimes.

**Local vol.** Local skews decay with calendar time, so LV **forward skews are much flatter than today's**. SV forward skews are roughly stationary.

**Digitals.** A digital equals $-\partial_KC=-\partial_KC_{BS}-\text{vega}\cdot\partial_K\sigma_{BS}$. For a 1y ATM digital with 25% vol and a skew of 3 vol points per 10% of strike, the skew term ≈ 0.4 × 0.3 ≈ **12% of notional**.

**Digital cliquets.** A digital cliquet is a strip of *forward-starting* digitals, whose value depends on *forward* skew. LV underprices them relative to SV, so an LV-marking seller is adversely selected. The earlier notes record an error ≈5.76% of notional for a 5y, 6%-coupon example; the exact arithmetic could not be re-verified.

**Stochastic implied volatility models.** Schönbucher and others: the martingale constraint ties surface dynamics tightly, but these models' continuity assumptions conflict with the need for jumps.

## Chapter 9 — Barrier Options

**Limiting cases with model-free hedges.**
- A knock-out call with barrier = strike below spot (a limit order) is worth $S-K$ and is hedged with one share when $r=q=0$.
- European capped calls.
- The reflection principle, the lookback hedging argument and put-call symmetry give quasi-static hedges.

**Model dependence.** European binaries agree under LV and SV (same vanillas), but **one-touches differ** (Figs. 9.2–9.4). Out-of-the-money barriers, live-outs and lookbacks are compared under the Heston–Nandi vs. LV pair.

**Discrete monitoring (Broadie–Glasserman–Kou).** Shift the barrier by $e^{\pm\beta\sigma\sqrt{\Delta t}}$ with $\beta=-\zeta(1/2)/\sqrt{2\pi}\approx0.5826$. Example: 32% vol with daily monitoring gives a shift of about 1.2% of the barrier.

**Variants.** Parisian options (reduce manipulation and Greek blow-ups at the barrier), ladders (discretized lookbacks), and ranges (double one-touches).

## Chapter 10 — Exotic Cliquets (Mediobanca case studies, priced under Heston–Nandi vs. its LV twin)

- **Locally capped, globally floored cliquet** (Mediobanca Bond Protection 2002–2005, on Euro Stoxx 50).
  - Annual coupon: $\max\{\sum_{t=1}^{12}\min(\max(r_t,-1\%),+1\%),\ 2\%\}$.
  - Expected coupon at a 2% floor: **Heston 3.53% vs. LV 2.55%**, ≈3% upfront over three years — more than the structuring margin.
  - The LV/SV gap depends on the floor level; the investor is effectively long forward skew.
  - Realized/estimated coupons 3.91%, 3.55%, 4.14% vs. a 3y EUR swap of 3.59% (per the earlier notes).
- **Reverse cliquet** (Mediobanca 2000–2005 Telecommunicazioni).
  - Payoff: $\max[0,\,100\%+\sum_{i=1}^{10}\min(0,r_i)]$ on semiannual returns, ≈ a short strip of ATM puts plus a global floor.
  - Expected redemption **43.9% (Heston) vs. 42.0% (LV)**: a small gap, with the sign set by the floor.
- **Napoleon** (Mediobanca World Indices Euro Note Serie 46; SPX, SX5E, NKY).
  - Coupon: $\max[0,\,10\%+\text{worst monthly return}]$.
  - Intuition says a steeper forward skew makes it cheaper, yet the expected coupon is ≈**1.74% under both** models: volatility convexity offsets forward skew.
  - Pricing with independent increments (correct monthly marginals, deterministic forward vol) underprices vol convexity. Dealers who did so won deals and lost money.
- **Moral:** stress the *model class*, not only the parameters.

## Chapter 11 — Volatility Derivatives

**Spanning (Carr–Madan).**
$$g(S_T)=g(F)+g'(F)(S_T-F)+\int_0^Fg''(K)(K-S_T)^+dK+\int_F^\infty g''(K)(S_T-K)^+dK.$$
One example is an amortizing call.

**Log contract and variance swap.** Itô gives $\int_0^T\sigma_t^2dt=2\int dS/S-2\log(S_T/S_0)$. Hence, for any diffusion,
$$\mathbb E\Big[\int_0^T\sigma_t^2dt\Big]=2\Big\{\int_{-\infty}^0p(k)\,dk+\int_0^\infty c(k)\,dk\Big\},$$
with OTM options in log-strike weighted by $1/K^2$ in strike space. Equivalently, $\mathbb E[W_T]=\int N'(z)\,\sigma_{BS}^2(z)\,T\,dz$ with $z=d_2$: fair variance is an average of implied variance across strikes, so it depends on skew and curvature.

In Heston, $\mathbb E[W_T]=\bar vT+(v_0-\bar v)(1-e^{-\lambda T})/\lambda$, which is independent of $\eta$ and $\rho$.

**Market context.** After 1998, hedge funds sold variance at high implied levels.

**Jumps.** Jumps break exact replication: the log strip and realized quadratic variation differ by a jump term.

**Volatility swaps.** These need a convexity adjustment because $\mathbb E\sqrt W\le\sqrt{\mathbb EW}$. Heston convexity curves are shown for the Heston–Nandi and BCC parameters. Tools: zero-correlation Laplace-transform results, a lognormal approximation to quadratic variation (good for 1y variance calls), and options on volatility, where model independence is only partial.

**Listed contracts.** The VIX (a 30-day log-strip fair variance) and VXB futures, whose convexity was measured on 8 Dec 2004 (Table 11.1).

**Postscript.** Reiterates that consistency across instruments, not realism, is the criterion.

---

## Critical assessment

- **Durable contributions:**
  - $\sigma_L^2=\mathbb E[v_T|S_T=K]$ and the gamma-weighted path representation of implied variance, which together explain most smile heuristics (implied skew ≈ ½ local skew; Heston skew ~ $1/T$).
  - A clear empirical demonstration (Table 3.1, Fig. 3.6) that time-homogeneous SV cannot fit the short-end skew.
  - Using a matched SV/LV pair to *measure* model risk in exotics.
- **Fragile or dated:**
  - One calm-day SPX surface (Sep 2005) carries most of the empirical argument.
  - $r=q=0$ throughout.
  - Jump fits to the one-day expiry are sensitive to triple-witching microstructure.
  - The Heston–Nandi laboratory ($\rho=-1$, $\eta=1$) is extreme.
  - The later literature offers alternatives to jumps for the short-end skew explosion: rough volatility (Gatheral–Jaisson–Rosenbaum), Bergomi forward-variance models, stochastic-local vol hybrids, and arbitrage-free SVI (Gatheral–Jacquier).
- **Practical use for a quant PM/researcher:**
  - Treat the surface as a no-arbitrage constraint; quote fair variance off the log strip, with Lee-consistent wing extrapolation and an explicit jump/discretization allowance.
  - Price any product that depends on forward skew or vol-of-vol (cliquets, one-touches, Napoleons, forward digitals) under at least two model classes, and reserve the gap.
  - Size short-dated crash exposure from the observed wings, not from an SV fit.
  - Remember that Heston understates skew persistence in high-vol regimes.

## Related

- Bergomi, *Stochastic Volatility Modeling*; Lewis, *Option Valuation under Stochastic Volatility*; Demeterfi–Derman–Kamal–Zou on variance swaps; Gatheral–Jacquier arbitrage-free SVI.

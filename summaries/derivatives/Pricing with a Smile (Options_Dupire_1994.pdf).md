# Pricing with a Smile

**Author:** Bruno Dupire (Bloomberg)  
**Publication:** Risk, 1994; this PDF is the 10-page reprint in *Derivatives Pricing: The Classic Collection* (chapter 11, production stamp 10/08/04). Conference version: Dupire (1993b), "Pricing and Hedging with Smiles", AFFI La Baule / IAFE New York.  
**Source file:** `Finance/Options_Dupire_1994.pdf`

---

## Question

Black–Scholes implied vols vary with maturity and strike. The maturity dimension is easy: Merton's deterministic $\sigma(t)$ reconciles, e.g., Nikkei ATM vols of 20% (6M) and 18% (1Y), since implied variance is the time average of instantaneous variance. (Implied forward vol for 6M→1Y: $\sqrt{(0.18^2\cdot 1-0.20^2\cdot 0.5)/0.5}\approx 15.7\%$.) The strike dimension (smile) had been addressed with jumps, stochastic volatility or transaction costs, all of which add a non-traded risk and destroy completeness. Dupire asks: given arbitrage-free call prices $C(K,T)$ for all $K,T$, is there a risk-neutral one-factor diffusion

$$\frac{dS}{S}=r(t)\,dt+\sigma(S,t)\,dW$$

with deterministic $\sigma(S,t)$ that reproduces every European price, so that the model stays complete and can price and hedge American, barrier, compound and other path-dependent claims consistently with the vanillas?

## Key idea: marginals plus the martingale constraint pin down the diffusion

- Path-dependent prices are equivalent to knowing the full risk-neutral process; European prices only give the marginal densities of $S_T$ given $S_0$.
- In general marginals do not identify a diffusion (a mean-reverting Gaussian process and a Gaussian process with decreasing vol can share marginals). But restricting to **risk-neutral** diffusions (drift fixed by the numeraire) removes the ambiguity: under technical conditions there is a unique diffusion compatible with the smile (Figure 1).
- With $r=0$, Breeden–Litzenberger gives the density: $C(K,T)=\int (S-K)^+\varphi_T(S)\,dS \Rightarrow \varphi_T(K)=\partial_{KK}C(K,T)$. In practice $C$ must be smoothly interpolated "from a few points".

## The Dupire equation

For the driftless diffusion $dx=b(x,t)\,dW$, Fokker–Planck (derivation deferred to Dupire 1993b) yields

$$\frac{b^2(K,T)}{2}\,\frac{\partial^2 C}{\partial K^2}=\frac{\partial C}{\partial T}\qquad\text{(E)}$$

so $b^2(K,T)=2\,\partial_T C/\partial_{KK}C$ and $\sigma(S,t)=b(S,t)/S$. Both derivatives are positive by no-arbitrage (butterfly for convexity, conversion for maturity), so $b^2>0$ on an arbitrage-free surface. The local vol at spot $K$ and time $T$ is read off options with strikes and maturities near $(K,T)$.

**Duality with Black–Scholes.** The BS PDE $\partial_t C=-\tfrac12 b^2(S,t)\partial_{SS}C$ holds for a fixed claim $(K,T)$ as a function of current $(S,t)$ and applies to any payoff; (E) holds for fixed today $(S_0,0)$ as a function of $(K,T)$, and only because the call payoff is the second integral of a Dirac mass ("very fortunate that the market trades this particular payoff"). Consequence: a **forward** tree rooted at $(K_0,T_0)$, fed today with intrinsic values of immediately expiring options, prices a whole strip of calls in one forward sweep; each node carries today's price of the call whose strike/maturity equals that node (Figure 2).

## Discrete construction (implied trinomial tree)

Rather than discretising (E) with Nelson–Ramaswamy binomial or Hull–White trinomial schemes, Dupire uses forward induction (Jamshidian 1991; Hull–White 1992):

- Equal time steps; the price-step/time-step ratio ("opening") must be large enough to accommodate local variance, the analogue of explicit-PDE stability. Equal log-spot steps work if smiles are mild; widen the opening if the procedure fails.
- Matching Europeans alone leaves superabundant degrees of freedom; imposing the martingale condition at every node, with a trinomial structure, gives existence and uniqueness (a simplistic discretisation need not).
- At step $n$, all continuous piecewise-linear payoffs with kinks at inner nodes (a $(2n+1)$-dimensional space containing cash, the asset, and calls/puts struck at nodes) must be priced correctly. Arrow–Debreu prices $A(n,i)$ are obtained from portfolios of market calls, spot and cash.
- Generic step for node $(n,i)$, sweeping from the bottom: compute $w(n,i,i-1)$ from the forward relation $A(n+1,i-1)=\sum_k A(n,k)\,w(n,k,i-1)$, using $A(n,i),A(n,i-1),A(n,i-2)$ and the already-known $w(n,i-1,i-1),w(n,i-2,i-1)$; then fix $w(n,i,i)$ and $w(n,i,i+1)$ from the one-step backward pricing of a unit of cash and a unit of spot. Top Arrow–Debreu profiles need not be imposed separately: they are spanned by those already fitted plus cash and spot (Figure 3).

## Hedging

1. **Delta.** With the full process, path-dependents are priced by Monte Carlo and Americans by dynamic programming; delta comes from shifting $S_0$ and re-inferring the process. This works only if spot actually follows the inferred diffusion, which "it probably will not."
2. **Robust vanilla hedge.** Perturb the volatility surface locally around $(K_0,T_0)$, obtain the new diffusion and the new value of claim $X$, and convert that sensitivity into an equivalent position in the $(K_0,T_0)$ call. Repeating over all $(K,T)$ gives a vega spectrum $\text{Vega}(K,T)$ and a continuous portfolio of calls, a projection of $X$ onto the calls, that matches $X$ to first order even if the market violates the forward volatilities implied today. It must be rebalanced periodically. This is the origin of bucketed-vega risk for exotics, letting them sit in the same book as vanillas.

## Conclusion as stated

It would be "excessive to pretend that the spot will follow this diffusion"; the claim is only that the market prices Europeans as if it did. Practical payoff: consistent pricing of path-dependent and American options and strike-by-maturity risk analysis.

## Critical assessment

- **Convincing:** The identification result is exact and elegant. Given the full marginals and the drift, the diffusion coefficient is determined, and the formula is model-free apart from the one-factor diffusion assumption. The forward-equation view (price all strikes at once) and the vega-projection hedge were both lasting contributions.
- **Thin in this paper:** It is a 10-page sketch. The Fokker–Planck derivation, the technical conditions for uniqueness, and the treatment of rates and dividends are omitted or deferred to Dupire (1993b); everything is shown for $r=0$. (Standard extension, not in the paper: $\partial_T C=\tfrac12\sigma^2K^2\partial_{KK}C-(r-q)K\partial_K C-qC$.) There are no numerical examples or empirical tests.
- **Fragile in practice:** Extracting $\partial_{KK}C$ and $\partial_T C$ from sparse, noisy quotes is an ill-posed inverse problem. Local vol is really an output of the surface-fitting and arbitrage-cleaning step (often done in implied/total-variance space), and wings and short expiries are unstable.
- **Model risk:** Local vol matches today's marginals, not smile dynamics. Its deterministic forward smiles tend to flatten, and later work (e.g., Hagan et al. 2002) showed it predicts smile moves against spot that contradict observed behaviour, so deltas and forward-start/cliquet prices can be biased. Barrier and forward-smile-sensitive products are where local vol and stochastic-vol models calibrated to the same vanillas disagree most. The first-order vanilla hedge only partly mitigates this, and the paper does not quantify the residual.
- **Relevance for a quant PM:** Local vol is the canonical baseline for exotics and the basis of local-stochastic-vol hybrids. Breeden–Litzenberger/Dupire is the right lens for reading risk-neutral densities from option surfaces. Treat local vol as a calibration and interpolation device, not a forecast of realised volatility.

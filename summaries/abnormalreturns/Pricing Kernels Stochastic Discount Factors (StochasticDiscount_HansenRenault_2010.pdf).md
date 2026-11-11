# Pricing Kernels (Stochastic Discount Factors)

**Authors:** Lars Peter Hansen & Eric Renault
**Publication:** "Pricing Kernels," entry in *Encyclopedia of Quantitative Finance* (Wiley), c. 2010; 10 pages. Companion entry: Stochastic Discount Factors.
**Source file:** Finance/StochasticDiscount_HansenRenault_2010.pdf (Drive id `0B-6kBz0I0dMsOWZtNE9UdWhzZlk`)

## Scope

This is a compact reference entry. It covers:
1. how no-arbitrage delivers a kernel representation of dynamic valuation operators;
2. the factorization into riskless discounting times an equivalent martingale measure;
3. a catalogue of SDFs implied by preferences and frictions;
4. long-horizon (Markov/eigenfunction) factorizations;
5. econometrics of SDFs from a finite asset menu and coarser-than-investor information.

It is a map, not a new result, and it contains no empirical estimates.

## 1. Representation

The law of one price is weaker than no-arbitrage (NA): if $b$ and $c$ have the same payoff but $b$ is cheaper, go long $b$, short $c$, and use the proceeds to buy a positive payoff $a$, which is an arbitrage. For the date-$t$ valuation operator on date-$t+1$ payoffs,

$$\pi_{t,t+1}(p_{t+1}) = E(s_{t+1}p_{t+1}\mid\mathcal F_t),\qquad s_{t+1}>0 \text{ a.s.} \tag{1}$$

A positive kernel implies NA. There are two existence routes, both with complete markets (indicators of $\mathcal F_{t+1}$ events are traded):
- a conditional Riesz theorem on $\mathcal F_{t+1}$-measurable payoffs with finite conditional second moments, with $\pi$ conditionally linear and continuous, plus NA (Hansen-Richard);
- Radon-Nikodym on bounded payoffs, with $E\pi$ absolutely continuous, plus NA.

With a thinner payoff space, Riesz still gives a representer $q_{t+1}\in P_{t+1}$, but $q$ need not be positive even under NA. A positive kernel exists if $P$ can be extended to include event indicators while preserving NA, and it is then generally **not unique**.

Multiperiod: $S_{t+1}=\prod_{j\le t+1}s_j$ (compounding follows from the law of iterated values with interim trading). Then $\pi_{\tau,t+1}(p)=E[(S_{t+1}/S_\tau)\,p\mid\mathcal F_\tau]$, and the discount-bond price is $E(S_{t+1}\mid\mathcal F_0)$.

## 2. Risk-neutral measure

$$\pi_{t,t+1}(p)=E(s_{t+1}\mid\mathcal F_t)\,\tilde E(p\mid\mathcal F_t),\qquad \tilde E(p\mid\mathcal F_t)=E\!\Big[\tfrac{s_{t+1}}{E(s_{t+1}\mid\mathcal F_t)}\,p\,\Big|\,\mathcal F_t\Big].$$

Factor $S_{t+1}=\bar S_{t+1}M_{t+1}$, where $\bar S$ compounds the one-period riskless discounts $E(s_j\mid\mathcal F_{j-1})$ and $M_{t+1}=\prod_j s_j/E(s_j\mid\mathcal F_{j-1})$ is a positive unit-mean martingale. The martingale property makes the implied probability assignments consistent across dates: "the law of iterated expectations enforces the law of iterated values." Prices become $\tilde E(\bar S_{t+1}p_{t+1}\mid\mathcal F_\tau)$.

This is the Harrison-Kreps/Ross content, and it is a mild modification of the efficient-markets claim that discounted prices are martingales: they are, under an *equivalent* distortion that encodes risk compensation (reconciling Rubinstein and Lucas). In Brownian filtrations, Girsanov turns the measure change into drift adjustments. The priced risks are the undiversifiable ones, typically macro shocks, so the risk prices embedded in engineering risk-neutral measures are the same objects that structural models try to explain.

## 3. SDFs implied by preferences and frictions

All are written with subjective discount rate $\delta$ and $\rho$ = inverse EIS.

| Model | $S_{t+1}/S_t$ | Notes |
|---|---|---|
| Power utility (Rubinstein, Lucas) | $e^{-\delta}(C_{t+1}/C_t)^{-\rho}$ | Complete markets, representative agent |
| Recursive (Epstein-Zin, Kreps-Porteus, Weil) | $e^{-\delta}(C_{t+1}/C_t)^{-\rho}\,[U_{t+1}/R_t(U_{t+1})]^{\rho-\gamma}$, with $R_t(U)=(E[U^{1-\gamma}\mid\mathcal F_t])^{1/(1-\gamma)}$ | $\gamma$ is risk aversion, separated from EIS. With $\rho=1$ it is observationally linked to robustness (Anderson-Hansen-Sargent) |
| External habit / catching up (Abel, Campbell-Cochrane, Menzly-Santos-Veronesi) | $e^{-\delta}(C_{t+1}/C_t)^{-\rho}\,\phi(H_{t+1})/\phi(H_t)$ | $H$ is the consumption-to-social-stock ratio; a preference-shock wedge driven by equilibrium aggregate consumption |
| Reference level (Garcia-Renault-Semenov) | $e^{-\delta}(C_{t+1}/C_t)^{-\rho}(H_{t+1}/H_t)^{\eta}$ | $H$ is the consumption-to-reference-level ratio. Internal habits (Constantinides, Heaton) and relative wealth (Bakshi-Chen) are also mentioned |
| Incomplete markets (e.g. Constantinides-Duffie) | $e^{-\delta}(C^a_{t+1}/C^a_t)^{-\rho}\,\dfrac{E[(C^j_{t+1}/C^a_{t+1})^{-\rho}\mid\mathcal F_{t+1}]}{E[(C^j_t/C^a_t)^{-\rho}\mid\mathcal F_t]}$ | Contracts only on aggregate shocks; the SDF loads on the **$-\rho$-th** cross-sectional moment |
| Private information (Kocherlakota-Pistaferri, from Rogerson's inverse Euler) | Same form with **$+\rho$-th** moments | Pareto optimal under private productivity; implies "savings constraints" |
| Solvency / limited commitment (Luttmer; He-Modest; Cochrane-Hansen; Alvarez-Jermann) | $e^{-\delta}\big[\min_j C^j_{t+1}/C^j_t\big]^{-\rho}$ | $S_{t+1}/S_t \ge e^{-\delta}(C^j_{t+1}/C^j_t)^{-\rho}$ for every $j$. The agent with the lowest consumption growth is unconstrained and prices assets; the others' constraints bind (Chien-Lustig vary the punishment) |

The sign flip between the incomplete-markets and private-information kernels is the sharpest testable contrast in the catalogue. It says which moment of the cross-sectional consumption distribution should price aggregate risk.

## 4. Long-term risk

With a Markov state $X$ (Alvarez-Jermann 2005; Hansen-Scheinkman 2009; Hansen 2008):

$$S_t=e^{-\eta t}\,M_t\,\frac{\hat f(X_0)}{\hat f(X_t)},\qquad \pi_{0,t}(p_t)=e^{-\eta t}\,\hat E\!\Big[\frac{p_t}{\hat f(X_t)}\,\Big|\,X_0\Big]\hat f(X_0),$$

where $\eta$ is a long-run discount rate, $\hat f$ is a positive (principal) eigenfunction, and $M$ is a multiplicative martingale. Here $M$ defines a change of measure *different* from the risk-neutral one, under which long-horizon pricing is constant discounting plus Markov expectations. Hansen-Scheinkman give conditions for the $M$-measure to have stable dynamics.

Transient model components enter as $S^*_{t+1}/S^*_t=(S_{t+1}/S_t)\,f(X_{t+1})/f(X_t)$. Habit models take this form (Bansal-Lehmann), as does a limiting case of recursive utility. They change $\hat f$ to $f^*=\hat f/f$ but leave $\eta$ and $M$ unchanged. Practical implication: models that differ only in transient components agree on long-horizon risk prices. Alvarez-Jermann use the factorization to measure the persistence of marginal utility from bond prices; Hansen-Scheinkman use it to value stochastically growing cash flows.

## 5. Econometrics with a finite menu

The econometrician sees $n$ payoffs $Y_{t+1}$ and prices $Q_t$, with information $\mathcal G_t\subset\mathcal F_t$: $E(s_{t+1}Y_{t+1}\mid\mathcal G_t)=Q_t$.

- **Minimal representer.** $p^*_{t+1}=Y_{t+1}'[E(Y_{t+1}Y_{t+1}'\mid\mathcal G_t)]^{-1}Q_t$ prices $Y$ and is the conditional least-squares projection of any admissible $s$ onto the payoff span. It need not be positive, so using it to price nonlinear claims on $Y$ can create arbitrage. If a riskless payoff is included, $E(s\mid\mathcal G)=E(p^*\mid\mathcal G)$ and $\mathrm{vol}(s)\ge\mathrm{vol}(p^*)$. This is the Hansen-Jagannathan volatility-bound family (also Bansal-Lehmann, Snow; conditional version in Gallant-Hansen-Tauchen).
- **Derivative-rich span.** If all Borel functions $\phi(Y_{t+1})$ are tradable, the Riesz representer $h^*$ on that space is positive and is the projection of $s$ onto it. It equals $s$ if that space is the full investor payoff set. Aït-Sahalia-Lo and Rosenberg-Engle state-price-density estimators can be read as estimating $h^*$.
- **Linear factor models as SDFs.** $Q_t=E[(\lambda_t\cdot z_{t+1}+\alpha_t)Y_{t+1}\mid\mathcal G_t]$ implies $E(Y\mid\mathcal G)=\alpha^*_tQ_t+\lambda^*_t\cdot\mathrm{cov}(Y,z\mid\mathcal G)$, where $\alpha^*_t=1/(\alpha_t+\lambda_t\cdot E(z\mid\mathcal G))$ and $\lambda^*_t=-\lambda_t\alpha^*_t$. Standardized factors make $\lambda^*$ the betas. With $z$ the market return this gives the CAPM; adding size and B/M factors gives a conditional FF3. If the factors are traded and a riskless payoff is included, $p^*=\lambda\cdot z+\alpha$.
  - Unconditional, excess returns, i.i.d. normal: ML and likelihood-ratio tests (Gibbons-Ross-Shanken).
  - GMM (Hansen 1982) relaxes normality, heteroskedasticity and dependence, as MacKinlay-Richardson stress, and unifies tests of conditional beta models.
- **Misspecification: HJ distance.** Choose $(\lambda,\alpha)$ to minimize the maximum pricing error over payoffs with unit second moment. Equivalently, minimize $E[(\lambda\cdot z+\alpha-v)^2]$ over true kernels $v$ that price $Y$, i.e. the quadratic form $e'[E(YY')]^{-1}e$ in the pricing errors $e$. The objective is zero under correct specification and a distance otherwise.
- **Parametric SDFs** $s_{t+1}=\phi_{t+1}(\theta)$ (the preference models above). The problem is semiparametric: the law of motion of payoffs is not specified. Conditioning information enters "through the back door" by scaling payoffs and prices by $\mathcal G_t$-measurable instruments, which turns conditional into unconditional moments for Hansen-Singleton GMM.
  - Alternatively, minimize the HJ criterion $\bar g(\theta)'[\tfrac1N\sum YY']^{-1}\bar g(\theta)$. Because its weighting matrix does not depend on the model, it is inefficient under correct specification but makes pricing errors comparable across models.
  - A variant requires the fitted SDF to be close to the set of *positive* kernels, so derivative payoffs are also priced well (Hansen-Heaton-Luttmer).
- **Conditional moments directly.** Ai-Chen sieve methods, and Antoine-Bonnal-Renault's conditional continuously-updated GMM (related to empirical likelihood and minimum entropy), avoid ad hoc instrument choice and can be combined with the HJ misspecification approach.

## Assessment

- **Value:** a tight, correct taxonomy linking three dialects (risk-neutral, beta/factor, consumption/structural) through one object. For a quant researcher the practical points are:
  1. A linear factor SDF is only a local pricing device. Check how often the fitted $s_t=a-b'f_t$ is negative before using it to value options or any nonlinear payoff.
  2. The HJ distance, with a model-independent weighting matrix, is the right metric for ranking misspecified factor models. Efficient GMM $J$-statistics are not comparable across models.
  3. The econometrician's $\mathcal G_t$ is coarser than investors' information, so tests are of implications, not of the full model.
  4. The long-run factorization isolates what matters for long-horizon valuation ($\eta$ and $M$) from transient model features.
- **Limits:**
  - An encyclopedia entry: no derivations beyond the sketches, no empirical calibration, and no discussion of which kernels fit the data.
  - Continuous time is covered only by a Girsanov pointer.
  - Some formulas (the habit and long-run factorizations) are stated schematically, so the cited originals are needed for implementation.

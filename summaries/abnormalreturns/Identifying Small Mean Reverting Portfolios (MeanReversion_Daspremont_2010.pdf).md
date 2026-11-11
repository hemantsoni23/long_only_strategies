# Identifying Small Mean Reverting Portfolios — d'Aspremont (2008/2011)

| Field | Detail |
|------|--------|
| **Author** | Alexandre d'Aspremont (ORFE, Princeton) |
| **Date** | Working paper February 26, 2008; published *Quantitative Finance* 11(3), 351–364, 2011 (arXiv 0708.3048) |
| **JEL** | C61, C82 |
| **Keywords** | Mean reversion; sparse estimation; convergence trading; momentum trading; covariance selection |
| **Source file** | `Finance/MeanReversion_Daspremont_2010.pdf` (Drive id `0B-6kBz0I0dMseDVNZ0N5M1p3b2c`; 2008 working-paper version) |

---

## Question

Classical tools for extracting mean-reverting baskets — cointegration (Engle–Granger, Johansen) and Box–Tiao canonical analysis — return **dense** portfolios. Dense baskets have three problems:
- they are costly to trade;
- they are hard to interpret;
- the most mean-reverting of them often behave like noise that moves inside the bid–ask spread.

The paper asks how to find the most mean-reverting portfolio subject to a **cardinality** constraint, and how to estimate its inputs stably. Everything applies symmetrically to momentum: maximize rather than minimize predictability, with identical numerics.

## Setup

The target is a portfolio $P_t=\sum_i x_i S^i_t$ that follows an Ornstein–Uhlenbeck process, $dP_t=\lambda(\bar P-P_t)\,dt+\sigma\,dZ_t$. We want to maximize $\lambda$ subject to $\|x\|=1$ and $\mathrm{Card}(x)\le k$.

The proxy for $\lambda$ is Box–Tiao predictability. Prices follow a stationary, demeaned VAR(1), $S_t=S_{t-1}A+Z_t$ with $Z_t\sim N(0,\Sigma)$. Let $\Gamma=\mathrm{Cov}(S_t)$. Then

$$
\nu(x)=\frac{x^\top A^\top\Gamma A\,x}{x^\top\Gamma x},
$$

the share of the portfolio's variance explained by its lag. Small $\nu$ means the portfolio is noise-dominated and mean-reverts fast; large $\nu$ means it is close to a unit root, i.e. momentum. Minimizing $\nu$ is the generalized eigenproblem $\det(\lambda\Gamma-A^\top\Gamma A)=0$. For $\Gamma\succ0$ the solution is $x=\Gamma^{-1/2}z$, where $z$ is the bottom eigenvector of $\Gamma^{-1/2}A^\top\Gamma A\,\Gamma^{-1/2}$.

In practice $A$ is estimated by OLS, $\hat A=(S_{t-1}^\top S_{t-1})^{-1}S_{t-1}^\top S_t$. Following Bewley et al. (1994), Johansen's ML cointegration is the same kind of canonical problem, run on $\Delta S_t$ versus $S_{t-1}$ with $Q=A-I$. So both methods reduce to

$$
\max_x \frac{x^\top A x}{x^\top B x}\quad\text{s.t. }\ \mathrm{Card}(x)\le k,\ \|x\|=1 \qquad (A,B\in\mathbb S^n).
$$

This sparse generalized eigenproblem is equivalent to subset selection, which is NP-hard (Natarajan 1995).

## Algorithms

**Greedy forward selection.**
- Start with $I_1=\arg\max_i A_{ii}/B_{ii}$.
- Given the current support $I_k$, try each remaining index: solve the dense GEP of size $k+1$ and keep the index that gives the best objective.
- Each step costs $O(k^2(n-k))$, so the full path $k=1,\dots,n$ costs $O(n^4)$.
- The supports are nested by construction, although optimal supports need not be. Forward–backward passes can repair this.
- Greedy provides no optimality bound.

**Semidefinite relaxation.** This extends the d'Aspremont–El Ghaoui–Jordan–Lanckriet (2007) sparse-PCA relaxation.
- Lift the vector to a matrix, $X=xx^\top$.
- Replace $\mathrm{Card}(X)\le k^2$ with the convex constraint $\mathbf 1^\top|X|\mathbf 1\le k$. This is valid because $\|x\|_1\le\sqrt{k}\,\|x\|_2$ and $\|X\|_F=1$.
- Drop the rank constraint.
- Homogenize with $Y=X/\mathrm{Tr}(BX)$ and $z=1/\mathrm{Tr}(BX)$, which gives the SDP

$$
\max\ \mathrm{Tr}(AY)\quad\text{s.t. } \mathbf 1^\top|Y|\mathbf 1\le kz,\ \mathrm{Tr}(Y)=z,\ \mathrm{Tr}(BY)=1,\ Y\succeq0 .
$$

The optimal value is an upper bound on the value of the sparse problem, and the relaxation is tight if $\mathrm{rank}(Y)=1$. Otherwise, take the leading eigenvector of $Y$ as the portfolio. The SDP costs much more than greedy, but it does not force nested supports.

## Penalized estimation as preprocessing

**Covariance selection.** Estimate a sparse precision matrix:

$$
\max_X\ \log\det X-\mathrm{Tr}(\Sigma X)-\rho\sum_{ij}|X_{ij}| .
$$

Zeros in $X$ mean conditional independence of the idiosyncratic components. On U.S. swaps with $\rho=0.1$, the graph links each tenor to its neighbors: the curve appears as a chain.

**Sparse VAR.**
- *Endogenous case,* $Z_t\sim N(0,\sigma I)$. The paper derives $A^\top A=I-\sigma\Gamma^{-1}$, so $A$ can be taken as a Cholesky factor. If the graph of $\Gamma$ is chordal, $A$ inherits $\Gamma$'s zero pattern (Wermuth 1980). By Gilbert (1994), a disconnected graph of $\Gamma$ implies $A$ is block-diagonal on the same clusters.
- *General case.* Estimate $A$ column by column with the LASSO: $\min_x\|S^i_t-S_{t-1}x\|_2^2+\gamma\|x\|_1$.

**Cluster restriction (Gilbert 1994, Thm 6.1).** Suppose the penalized $\Gamma$ and $A^\top\Gamma A$ share the same block-diagonal structure. Then every generalized eigenvector lies inside a single cluster. Practical recipe:
1. Choose $\rho$ large enough to break the graph into small components.
2. Check that the graph is chordal, or that the LASSO $\hat A$ shares its clusters.
3. Run the sparse search within each component only.

**Trading layer (appendix).**
- Estimate the OU parameters by an AR(1) regression of $P_t$ on $P_{t-1}$: $\hat\lambda=-\Delta t^{-1}\log\hat\rho_1$, with half-life $\tau=\log 2/\lambda$.
- Optimal log-utility holding (Jurek–Yang 2006): $N_t=W_t\,[\lambda(\bar P-P_t)-rP_t]/\sigma^2$.
- With proportional fund flows $dF=f\,d\Pi+\sigma_f dZ^{(2)}$, the denominator becomes $\sigma^2(1+f)$.
- In steady state with $\bar P=0$, $P\sim N(0,\sigma^2/2\lambda)$, so leverage is Gaussian and stays below $M=\alpha(\lambda+r)/\big((1+f)\sigma\sqrt{2\lambda}\big)$ with probability $N(\alpha)$. This bound is an alternative way to set $f$.

## Empirical results

**Data.**
- U.S. swap rates at 1Y, 2Y, 3Y, 4Y, 5Y, 7Y, 10Y and 30Y, 1998–2005, in percent.
- 44 USD exchange rates, April 2002–April 2007 (pip size $10^{-4}$, bid–ask about 0.0005 for key rates).

**Dense Box–Tiao on 100 days of swaps (Table 1).** The eight canonical portfolios have $\lambda$ = 0.58, 8.61, 16.48, 38.59, 84.55, 174.82, 184.83, 238.11 and volatilities 0.21, 0.28, 0.34, 0.14, 0.10, 0.09, 0.07, 0.07. All are significant at 99% except the last ($p=0.51$). Its $\lambda\approx238$ implies a half-life of about one day, which daily data cannot identify. The 1–8 axis indexes the canonical portfolios; each one uses all eight swaps. Figure 1, on the same data, labels the plots with somewhat different $\lambda$ values (ending at 252), so Table 1 and Figure 1 do not agree exactly.

**Sparse greedy on the same window (Figure 6).** $\lambda$ for $k=1,\dots,8$ is roughly 0, 35, 128, 178, 213, 247, 252, 252. About 85% of the attainable mean reversion is reached with 5 of 8 tenors, and essentially all of it with 6.

**Greedy vs SDP (Figure 5).** The SDP is sometimes better, but greedy is more reliable on this data. Both coincide at $k=1$ and $k=n$. The full greedy path for $n=100$ takes 1 min 40 s.

**Rolling out-of-sample test on swaps (Figure 7).** Portfolios are estimated on 200-day windows, rolled every 50 days, and $\lambda$ is re-measured on the next 200 days. Figure 7 plots in-sample and out-of-sample average $\lambda$ against $k$ and shows the out-of-sample price range in bp (roughly the 10–40 bp scale). The paper's point is that sparse baskets move over a wider range, so they are more tradable against the spread.

**Portfolio weights (Table 2).** Weights by maturity × $k$:

| Maturity | $k=1$ | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| 1Y | 0 | 0 | 0 | −0.041 | −0.037 | 0.036 | −0.013 | 0.001 |
| 2Y | 0 | 0 | 0 | 0 | 0 | 0 | −0.102 | 0.117 |
| 3Y | 0 | 0 | −0.288 | 0.433 | 0.419 | −0.437 | 0.547 | −0.495 |
| 4Y | 0 | −0.714 | 0.806 | −0.803 | −0.802 | 0.809 | −0.767 | 0.702 |
| 5Y | 1.000 | 0.700 | −0.517 | 0.408 | 0.424 | −0.389 | 0.317 | −0.427 |
| 7Y | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0.219 |
| 10Y | 0 | 0 | 0 | 0 | 0 | −0.031 | 0.025 | −0.130 |
| 30Y | 0 | 0 | 0 | 0 | −0.007 | 0.016 | −0.008 | 0.014 |

All the action is in the 3Y–5Y belly:
- $k=2$ is a 4s5s spread;
- $k=3$ is a 3s4s5s butterfly;
- higher $k$ adds only tiny wing weights.

**FX (Figures 8–9).** Covariance selection isolates a connected cluster of 14 rates. Within it, the sparse decomposition is run on unpenalized estimates and on penalized ones: $\Gamma$ with $\rho=0.01$, and LASSO $A$ with $\gamma$ set to zero out 20% of the coefficients. Findings:
- Sparse portfolios have **higher out-of-sample $\lambda$** than dense ones.
- Penalized estimates beat unpenalized ones out of sample.
- Sparse portfolios have a significantly broader price range (in percent).

This is the paper's main evidence that sparsity is a statistical regularizer as well as a cost control.

**Convergence trading on swaps (Figure 10).** Parameters are estimated on 100 days and the Jurek–Yang rule is traded on the next 50 days. Average out-of-sample Sharpe ratios look attractive without frictions, but a 1 bp bid–ask spread completely eliminates them in this very liquid market.

**Open issues the author acknowledges.**
- There is no consistency result for support recovery; Amini–Wainwright (2008) on sparse PCA is only suggestive.
- There is no suboptimality bound for the greedy algorithm.

## Assessment

**What holds up.**
- The reduction of cointegration and Box–Tiao to a (sparse) generalized eigenproblem is clean.
- The greedy and SDP pair is a practical toolkit.
- The cluster-restriction result is a useful dimension-reduction device for large universes.
- The FX evidence that penalization and sparsity *raise* out-of-sample mean reversion is the most useful empirical finding.
- The Table 2 weights show that the method recovers familiar curve trades — spreads and butterflies — rather than arbitrary combinations.

**What is fragile.**
- *Selection bias.* In-sample $\lambda$ comes from an AR(1) fit on 100–200 observations of a portfolio *chosen* to minimize predictability. It is biased upward twice: by the usual small-sample bias of mean-reversion estimates and by optimization over $x$. Only the out-of-sample figures are informative, and they are shown as plots rather than tables.
- *Modelling assumptions.* Box–Tiao assumes a stationary VAR(1), while swap rates are close to unit roots. The $\|x\|_2=1$ normalization is in rate units, not DV01 or risk units, so $\lambda$ and "range" across $k$ are not risk-comparable.
- *Endogenous-VAR derivation.* The step from $\Gamma=A^\top\Gamma A+\sigma I$ to $A^\top A=I-\sigma\Gamma^{-1}$ does not hold for general $A$ (it needs $A$ to commute with $\Gamma$). Treat the chordal/Cholesky shortcut as a heuristic.
- *Thin empirics.* The work is illustrative: one short swap sample, one FX cluster, no transaction-cost-aware optimization, no significance tests on out-of-sample differences, and a trading test that fails at 1 bp.

**Practical relevance.** Use this as a basket-construction and feature-discovery layer for rates or FX relative value, or on factor-model residuals in equities, not as a source of free Sharpe. A sensible pipeline:
1. Cluster with the graphical lasso.
2. Run a greedy sparse Box–Tiao path within each cluster.
3. Pick $k$ at the elbow.
4. Screen on out-of-sample half-life and on range relative to round-trip cost.
5. Size with an OU/Jurek–Yang rule under a leverage cap.

Pairs trading (Gatev–Goetzmann–Rouwenhorst) is the $k=2$ special case. The paper's advantage is a principled way to go beyond pairs without dense-basket overfitting.

## Relation to literature

- **Box–Tiao (1977); Johansen (1988, 1991); Bewley et al. (1994):** the dense canonical baselines.
- **d'Aspremont et al. (2007) sparse PCA; Banerjee–El Ghaoui–d'Aspremont covariance selection; Friedman–Hastie–Tibshirani graphical lasso; Tibshirani LASSO:** the sparse machinery the paper builds on.
- **Kim–Omberg, Campbell–Viceira, Wachter, Liu–Longstaff, Jurek–Yang:** optimal trading of mean-reverting spreads.
- **Grossman–Vila, Xiong:** leverage and fund-flow constraints (the LTCM motivation).

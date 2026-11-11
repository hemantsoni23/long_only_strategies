# A New Approach to Modeling and Estimation for Pairs Trading — Do, Faff & Hamza (2006) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Authors** | Binh Do, Robert Faff, Kais Hamza (Monash University) |
| **Date / venue** | May 29, 2006, working paper |
| **Source file** | `Finance/InvestmentsPairs_DoFaffHamza_2006.pdf` |
| **Contribution** | A critique of the distance, cointegration and Elliott et al. stochastic-spread methods; a "stochastic residual spread" state-space model anchored in APT/CAPM relative pricing; an EM algorithm for a linear Gaussian state-space model with an exogenous input in the measurement equation; a three-pair illustration |

## Motivation and positioning
The published pairs-trading literature at the time consisted of Gatev–Goetzmann–Rouwenhorst (1999; distance rule, profitable after costs), Vidyamurthy (2004; cointegration playbook, no empirics) and Elliott–van der Hoek–Malcolm (2005; Kalman-filtered OU spread). The authors argue that all three are ad hoc or impose **return parity**: in the long run the two legs must earn the same return. A pairs rule that forces a wrong equilibrium leads to "non-tradeability" at best and non-convergence at worst. They distinguish pairs trading (relative mispricing between two names; statistical arbitrage or merger arbitrage; not necessarily market neutral) from market-neutral portfolio optimization in the Jacobs–Levy sense.

## Critique of existing methods
- **Distance (GGR; Nath 2003).** Uses the SSD of normalized prices. GGR trigger at 2 formation-period standard deviations; Nath enters at the 15th percentile of the empirical distance distribution, stops out at the 5th, and uses a forced close at period end. The method is model-free, so it carries no misspecification risk, but it gives no forecast of convergence time. It assumes a static price-level distance, i.e. return parity, which is valid only for near-identical twins.
- **Cointegration (Vidyamurthy).** Engle–Granger regression $\log p^A_t-\gamma\log p^B_t=\mu+\epsilon_t$, ADF on residuals. Problems:
  - Results depend on which variable is the regressand (fix: Engle–Yoo critical values, or a Johansen VECM cross-check).
  - The regression is spurious if the prices are not cointegrated (Lim–Martin 1995), so one should not trade in that case.
  - Vidyamurthy's favored "zero-crossing rate" diagnostic has no clear trigger.
  - Vidyamurthy's APT justification (A's loadings are $\gamma$ times B's, therefore cointegration) is wrong. Under APT, $R^A=R_f+\gamma(\sum_i b_i r_i)+R^{s,A}$ and $R^B=R_f+\sum_i b_i r_i+R^{s,B}$, so $R^A\ne\gamma R^B+\text{noise}$ unless $\gamma=1$: the risk-free term does not scale.
- **Stochastic spread (Elliott et al.).** A latent OU state $dx_t=\kappa(\theta-x_t)dt+\sigma dB_t$ observed as $y_t=x_t+H\omega_t$. It has three advantages: explicit mean reversion, first-passage-time forecasts of holding period and expected return, and exact Kalman MLE via
$$x_k=\theta(1-e^{-\kappa\Delta})+e^{-\kappa\Delta}x_{k-1}+\epsilon_k,\qquad \mathrm{Var}(\epsilon)=\tfrac{\sigma^2}{2\kappa}(1-e^{-2\kappa\Delta}).$$
  The spread should be in log prices, not price levels (a level spread widens as prices rise). Even in logs, a mean-reverting log spread forces return parity. The authors see this as appropriate only for dual-listed companies (Unilever NV/PLC, Royal Dutch/Shell before July 2005, BHP Billiton Ltd/PLC, Rio Tinto Ltd/PLC) and cross-listings/ADRs.

## Proposed model: stochastic residual spread
A "relative APT": $R^A_t=R^B_t+\Gamma r^m_t+e_t$, where $\Gamma=\beta^A-\beta^B$ is the vector of factor-loading differences and $r^m$ the factor excess returns. The residual spread $G_t=R^A_t-R^B_t-\Gamma r^m_t$ is modeled as a noisy observation of an OU state. Because $\Gamma$ is unknown, the observation is redefined as the raw return differential, which lets $\Gamma$ and the state be estimated jointly and avoids stacking the errors of a two-step procedure:
$$x_k=\theta(1-e^{-\kappa\Delta})+e^{-\kappa\Delta}x_{k-1}+\epsilon_k,\qquad y_k\equiv R^A_k-R^B_k=x_k+\Gamma' r^m_k+H\omega_k.$$
- The model nests Elliott et al. when $\Gamma=0$.
- The measurement noise is justified as uncertainty in the equilibrium relation, not bid-ask noise.
- A nonzero $\theta$ is read as a firm-specific relative premium (for example management quality). Rather than adding a separate constant $\mu$, it is absorbed into $\theta$.
- The paper does not require APT to hold exactly; the factor structure is a flexible way to encode the trader's priors. The simulation and empirics use single-factor CAPM.

**Trading logic at the return level.** Mispricing here is in returns, not prices. The rule is to enter when the accumulated filtered residual $\delta_k=\sum_{i=k-l}^{k}E[x_i\mid Y_i]$ exceeds $\theta$ by a threshold, and to exit when the accumulated spread is neutralized, which can mean the per-period residual overshoots to the other side of $\theta$. Example: twins, A +5% and B +3%; convergence requires a subsequent residual of about −2%. The expected holding period is the first passage of $\delta$ through 0, to be computed by Monte Carlo (analytic results are left for future work). No rule is actually specified or tested.

## Estimation
- **Kalman MLE.** Prediction-error decomposition $\log L=-\tfrac N2\log2\pi-\tfrac12\sum_i(\log|F_i|+e_i'F_i^{-1}e_i)$ over $\Psi=\{\theta,\kappa,\sigma,\Gamma,H\}$.
- **EM (Shumway–Stoffer 1982).** Treats $x$ as missing data, increases the likelihood monotonically, and yields RTS-smoothed states as a by-product. The technical contribution is the EM derivation (in an appendix) for
$$x_k=Ax_{k-1}+B+Gv_{k-1},\qquad y_k=x_k+DU_k+H\omega_k,$$
  where $U_k$ is a time-varying exogenous input with unknown coefficient $D$ ($=\Gamma$). Elliott et al. had no $U_k$. The mapping is $A=e^{-\kappa\Delta}$ and $B=\theta(1-A)$. $\log A$ is estimated to keep $A>0$.
- **Alternatives discussed.**
  - MCMC is sound but computationally expensive.
  - Joint filtering (Kitagawa's self-organizing state space) treats parameters as slowly varying states. It could track a time-varying $\Gamma$ but may be unstable (Liu–West).
  - EKF and UKF are unsuitable because of the unknown noise variances.
  - Particle filters (Pitt–Shephard auxiliary PF) are not tied to linearity or Gaussianity but need a correctly specified noise law, so they are less robust than Kalman MLE.
  - The suggested hybrid is EM, then numerical MLE, then PF initialized at the MLE.
- **Simulation.** True values $A=0.9$, $B=0.005$, $D=0.1$, $G=0.0529$, $H=0.05$ (i.e. $\theta=0.05$, $\kappa=5$, $\sigma=0.4$, $\Gamma=0.1$), $N=100$, market simulated as GBM, starting values far from the truth. EM converges quickly, and further MLE or PF steps add little. The methods differed little in estimation error, and no error statistics are reported.

## Empirical illustration
Three industry pairs, each using **two years of weekly returns**:
- BHP vs Rio Tinto: S&P/ASX 200 as market.
- Target vs Walmart: S&P 500.
- Shell vs BP: FTSE All-Share.

Local Treasury yields are the risk-free rate. Estimation is by EM.

**Table 1 (z-statistics in parentheses):**

| | BHP–RIO | Target–Walmart | Shell–BP |
|---|---|---|---|
| $\log A$ | −6.3665 (−3.53) | −6.1471 (−6.90) | −6.5089 (−6.07) |
| $B$ | −0.0009 (−5.48) | 0.0048 (18.29) | −0.0000 (−0.01) |
| $D=\Gamma$ | 0.4420 (34.14) | −0.0251 (−1.33) | −0.0518 (−7.12) |
| $G$ | 0.0121 (16.38) | 0.0155 (7.58) | 0.0132 (15.79) |
| $H$ | 0.0110 (13.44) | 0.0226 (15.91) | 0.0117 (12.60) |
| $\theta$ | −0.0009 | 0.0048 | −0.0000 |
| $\kappa$ | 6.3665 | 6.1471 | 6.5089 |
| $\sigma$ | 0.0433 | 0.0545 | 0.0475 |

(The OCR of the table columns is jumbled. This assignment is consistent with the reported identities $\kappa=-\log A$, $\theta\approx B$ and $\sigma=G\sqrt{2\kappa}$.)

**Authors' reading:**
1. Coefficients are significant, which they take as support for OU mean reversion. Target–Walmart's $\Gamma$ and Shell–BP's $B$ are not significant, however.
2. $\kappa\approx6$–6.5 for all three pairs: strong reversion, so little non-convergence risk but opportunities vanish quickly.
3. $\theta\ne0$. BHP–RIO: about 5% per year in favor of Rio ($-0.0009\times52$). Target–Walmart: about 25% per year ($0.0048\times52$), reflecting divergent two-year trends (Target up, Walmart down); this is flagged as a pair to avoid because it co-moves short-term but trends apart. Shell–BP: $\theta\approx0$.
4. The joint $\hat\Gamma=0.442$ for BHP–RIO matches separate market-model betas, 1.7827 − 1.3377 = 0.445. The authors attribute this to BHP's oil exposure.

## Critical assessment
- **The persistence result says the opposite of "strong mean reversion."** The reported $\kappa$ is numerically $-\log A$. With weekly data, $A=e^{-6.4}\approx0.002$, so the latent residual has essentially no week-to-week autocorrelation. (Either $\kappa$ is quoted per week, or it has not been annualized; $\kappa$ per year would be about 330.) The filtered "mispricing" is then i.i.d. noise around $\theta$ in return space. Two consequences:
  - With $A\approx0$, the state noise ($G$) and the measurement noise ($H$) are two white-noise components with nearly equal estimated scales. They are not separately identified in any meaningful sense, so the significant z-stats on $G$ and $H$ carry little information.
  - For the proposed trading rule, the object that matters is the accumulated residual $\delta_k$. If per-period residuals are i.i.d., $\delta_k$ is a random walk with drift $\theta$, the opposite of convergence. The evidence therefore does not support tradeable mean reversion in these pairs. What it does show is that the market-adjusted return differential has a small, possibly nonzero mean. The simulation used $A=0.9$, i.e. real persistence, which the data do not exhibit.
- **The return-level framing is the conceptual crux.** Mean reversion in return residuals is not the same as mean reversion in cumulative (price-level) residuals, which is what pays in a pairs trade. The model would be more coherent if the OU state described the cumulative residual $\sum(R^A-R^B-\Gamma r^m)$, i.e. an OU process on the idiosyncratic log-price spread, as in Avellaneda–Lee (2010). That formulation also sidesteps the return-parity objection through the $\Gamma$ hedge.
- **What is useful:**
  - The critique of the cointegration–APT argument (the risk-free term) and of return parity.
  - Hedging the market-beta differential inside the spread; joint estimation of $\Gamma$ recovers the OLS beta difference.
  - The EM derivation with an exogenous input.
  - The practical warning that a large $|\theta|$ signals trend divergence rather than a tradeable pair.
- **Missing:** a cross-section of pairs, any backtest, entry and exit thresholds, transaction costs, short-sale constraints, multi-factor $\Gamma$, and any test of time variation in $\Gamma$. There are about 104 observations per pair and the paper does not report the simulation's estimation errors. The authors defer profitability to future work.
- **For a PM:** Take away the factor-hedged residual spread and joint beta estimation. Re-express the state as a cumulative idiosyncratic spread and check its half-life before trusting any "κ".

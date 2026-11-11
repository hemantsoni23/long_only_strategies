# Where Do Alphas Come From?: A New Measure of the Value of Active Investment Management — Lo (2007) — Detailed Quantitative Research Notes

## Bibliographic Header

| Field | Detail |
|------|--------|
| **Title** | Where Do Alphas Come From?: A New Measure of the Value of Active Investment Management |
| **Author** | Andrew W. Lo (MIT Sloan; AlphaSimplex Group) |
| **Dates** | First draft March 5, 2007; latest revision May 15, 2007 (working paper) |
| **Source file** | `Finance/HedgeFundsAlpha_Lo_2007b.pdf` |
| **Drive file_id** | `0B-6kBz0I0dMsbi1GTG56RU8xYlE` |
| **Keywords** | Active management; AP decomposition; active ratio; factor timing; alpha vs beta; sampling interval |

---

## Question

Alpha, beta, tracking error and the Sharpe and information ratios are functions of *single-date* moments (means, variances, contemporaneous covariances), and are usually estimated under i.i.d. assumptions. Active management, however, is about forecasting, a multi-date property. Lo proposes a benchmark-free decomposition of expected return that isolates the contribution of forecast power. It is aimed especially at hedge funds, where investors worry they "pay for alpha and get beta".

## The AP decomposition

**Assumptions.** (A1) Asset returns are stationary and ergodic with finite fourth moments. (A2) Weights $\omega_{it}$ are stationary, ergodic functions of $X_{t-1}$ only, which rules out look-ahead (otherwise $\omega_{it}\propto\max[0,R_{it}]$ would be an arbitrage).

**Proposition 1.** With $R_{pt}=\sum_i\omega_{it}R_{it}$,

$$
E[R_{pt}]=\underbrace{\sum_i \mathrm{Cov}[\omega_{it},R_{it}]}_{\delta_p\ \text{(active)}}+\underbrace{\sum_i E[\omega_{it}]E[R_{it}]}_{\nu_p\ \text{(passive)}},\qquad \theta_p\equiv\frac{\delta_p}{\delta_p+\nu_p}\ \text{(active ratio)}.
$$

Equivalently, $\delta_p=\sum_i\sigma(\omega_{it})\sigma(R_{it})\mathrm{Corr}[\omega_{it},R_{it}]$. Value is added by making weights more volatile where their correlation with returns is positive, and less volatile where it is negative. $\theta_p$ is unit-free, so it does not scale with the horizon the way an IR does. It is dynamic and requires no benchmark (it can be applied to excess-of-benchmark returns if desired).

**Passive, redefined (Definition 1).** A portfolio is passive if its weights are uncorrelated with the corresponding returns. Two consequences:
- A cap-weighted index has time-varying weights, $\omega_{it}\propto P_{i,t-1}S_{i,t-1}$, yet is passive if returns are serially independent. With serial correlation, even buy-and-hold acquires an active component.
- An S&P-futures portfolio plus a static commodity basket shows traditional "alpha" but is fully passive under AP.

**Sample identity.** The decomposition holds exactly for sample moments (with $1/T$ normalization), so it is an exhaustive ex-post attribution. More usefully,

$$
\hat\delta_p=\bar R_p-\sum_i\bar\omega_i\bar R_i,
$$

so only **average weights and average asset returns** are needed. Position-level transparency is not required, which lowers the disclosure cost for secretive managers. Lo's remark: a manager whose average weights barely move should not be earning hedge-fund fees anyway.

## Factor version (Proposition 2)

Under (A3), $R_{it}=\alpha_i+\sum_k\beta_{ik}F_{kt}+\epsilon_{it}$ with $E[\epsilon_{it}\mid F]=0$, and portfolio betas $\beta_{pk,t}=\sum_i\omega_{it}\beta_{ik}$:

$$
E[R_{pt}]=\underbrace{\sum_i\alpha_iE[\omega_{it}]}_{\text{security selection}}+\underbrace{\sum_k\mathrm{Cov}[\beta_{pk,t},F_{kt}]}_{\text{factor timing}}+\underbrace{\sum_k E[\beta_{pk,t}]E[F_{kt}]}_{\text{risk premia}},
$$

with $\mathrm{Cov}[\beta_{pk,t},F_{kt}]=\sum_i\beta_{ik}\mathrm{Cov}[\omega_{it},F_{kt}]$. The first two terms are active, the third passive (Definition 2: passive exposure to factor $k$ means $\beta_{pk,t}$ is uncorrelated with $F_{kt}$). Implications drawn:
1. Excess return over a benchmark can be purely passive exposure to non-market factors (e.g. a static credit beta of 0.5).
2. **Long-only constraints limit factor timing**, since a long-only manager cannot take negative betas when premia turn negative. This offers a structural explanation of the long-only vs hedge-fund performance gap that does not rely on talent migration.
3. On "paying for alpha, getting beta": timed beta (allocation alpha) is legitimate active value, while static beta can be bought cheaply (Leibowitz's "beta grazers", futures-based hedge-fund replication). Passive exotic betas (credit, liquidity, volatility) may justify higher management fees, but never incentive fees.
4. Even if all $\alpha_i=0$, time-varying premia leave room for active value.

## Analytical examples

**Two-asset toy (Figs. 1–3, 5).** Asset 1 alternates between 1% and 2% monthly; Asset 2 pays 0.15%. The average weights are 75/25, so the passive component is 1.16%/month in all of A1–A3:

| Portfolio | Weight dynamics | $E[R_p]$ | $\delta_p$ | $\theta_p$ |
|---|---|---:|---:|---:|
| A1 | constant 75% | 1.16% | 0 | 0% |
| A2 | 50% when $R_1=1\%$, 100% when $R_1=2\%$ | 1.29% | +0.13% | 9.71% |
| A3 | the reverse | 1.04% | −0.13% | −12.05% |
| A4 | 50% for 7 months, then 100% (one decision, sampled monthly) | 1.13% | +0.02% | 1.85% |

A4 illustrates that sampling more finely than the decision interval introduces no bias: an unchanged weight is a deliberate "let it ride" decision.

**AR(1) timing (Section 4.2).** For $R_t=\mu+\rho(R_{t-1}-\mu)+\epsilon_t$ and $\omega_t=\gamma_1+\gamma_2R_{t-1}$:

$$
E[R_{pt}]=\gamma_2\rho\,\mathrm{Var}[R_t]+(\gamma_1+\gamma_2\mu)\mu+(1-\gamma_1-\gamma_2\mu)R_f .
$$

The active term is positive iff $\mathrm{sign}(\gamma_2)=\mathrm{sign}(\rho)$ (momentum trading on momentum, reversal trading on reversal), and it scales with the return variance.

**Stop-loss (Section 4.3, Table 1).** The rule is: go to cash at $t$ if $R_{t-1}\le\zeta$, with Gaussian AR(1) returns. Then

$$
\delta_p=\rho\,\sigma\,\phi\!\left(\tfrac{\zeta-\mu}{\sigma}\right).
$$

The sign is that of $\rho$. With $R_f=5\%$, $E[R]=10\%$, $\sigma=20\%$ (annual; monthly process) and annualized thresholds from −1% to +1%:
- $\rho=-25\%$: active component ≈ −6.6% to −6.9% per year, so the stop destroys value.
- $\rho=0$: zero.
- $\rho=+25\%$: +6.6% to +6.9% (active share of return ~45–48%).
- $\rho=+50\%$: +13.1% to +13.8% (~62–65%).

Stops therefore add value only in the presence of momentum (see Kaminski–Lo).

## Implementation

- **Inference (Proposition 3, Appendix A.1).** GMM on the $2n$ moment conditions for the means of weights and returns ($H=-I$), delta method for $\theta$, Newey–West HAC. The empirical section uses 6 lags for daily data and 3 for monthly.
- **Sampling interval (Section 5.3).** Aggregating over $q$ periods, $E[R_{p\tau}(q)]=q\,\delta_p+q\,\nu_p$. However, the only $q$-period weights that reproduce the $q$-period portfolio return are *return-weighted* averages, $\omega_{i\tau}(q)=\sum_t\omega_{it}R_{it}/R_{i\tau}(q)$. The decomposition computed on coarse data is therefore not a scaled version of the fine one: it mixes within-period cross-moments. The rule is that data must be sampled at least as finely as the finest decision interval. Lo's illustration: monthly data are adequate for Buffett but not for Steve Cohen.

## Empirical application: Lo–MacKinlay contrarian on NASDAQ size deciles

Weights are $\omega_{it}=-\frac1n(R_{i,t-1}-\bar R_{t-1})$ on the five smallest CRSP-NASDAQ size deciles, daily, Jan 2, 1990 – Dec 29, 1995 (a period chosen for the rise of day trading). The exercise is illustrative, not an implementable strategy.

- **Lead–lag (Table 2).** First-order cross-autocorrelations are 15–27%. Larger deciles lead smaller ones (e.g. $\mathrm{corr}(R_{5,t},R_{1,t+1})=25.4\%$ vs $\mathrm{corr}(R_{1,t},R_{5,t+1})=16.7\%$). Own autocorrelations are 10–19%.
- **Performance (Table 3).** Annualized mean 31.4%, volatility 7.9%, Sharpe 3.95, versus decile Sharpes of 1.35–2.25. The daily strategy's own $\rho_1$ is 4.7%.
- **AP (Table 4, daily).**

| | Estimate (ann.) | SE | $t$ |
|---|---:|---:|---:|
| Mean | 31.4% | 0.3% | 91.0 |
| Risk premia $\nu_p$ | −0.6% | 3.5% | −0.17 |
| Active $\delta_p$ | 32.0% | 3.5% | 9.24 |
| $\theta_p$ | 101.9% | 0.3% | 354.4 |

  The passive component is slightly negative because the strategy is on average long low-mean losers and short high-mean winners (Lo–MacKinlay 1990, Section 5.3.1). Timing more than covers it.
- **Monthly transparency (Tables 4–5).** Using only month-end weights and monthly decile returns gives an apparent mean of **−4.0%** (t = −3.98), Sharpe −0.45, and an "active component" of −4.1%. Daily bets are invisible at month end, so both the sign of the return and the attribution are wrong. The monthly $\theta=102.6\%$ is numerically close to the daily value, but it is a ratio of two wrong numbers.

## Limitations

- **Covariance is not skill.** $\delta_p>0$ says weights co-move with subsequent returns. With small NASDAQ decile portfolios in 1990–95, much of that covariance is stale-price and nonsynchronous-trading lead–lag, which is not tradable at the stated magnitudes. The example has no costs.
- **$\theta_p$ is a ratio.** It is unstable when $E[R_p]$ is near zero and can exceed 1 or go negative. Reporting $\delta_p$ and $\nu_p$ with their standard errors is more informative.
- **The passive term is estimated imprecisely.** In Table 4 its standard error (3.5%) is ten times that of the mean (0.3%), because it depends on mean-return estimates. The split can therefore be much noisier than the total.
- **Proposition 2 as stated drops a term.** The general identity also contains $\sum_i\mathrm{Cov}[\omega_{it},\epsilon_{it}]$, i.e. timing of idiosyncratic returns. This is exactly what stat-arb and short-horizon strategies harvest, so it should be carried as a separate "residual timing" term (or assumed zero explicitly). The "security selection" term, as written, captures only static tilts toward high-$\alpha_i$ names.
- **Stationarity and ergodicity (A1–A2)** exclude strategy changes, capacity-driven decay and regime shifts, which are central to real hedge-fund track records.
- **The attribution depends on the factor model.** An omitted factor that is timed will show up as selection or residual timing.

## Assessment

- **What holds up:** the identity itself, and its two practical corollaries. First, active value lives in $\mathrm{Cov}(\omega,R)$, which can be computed from average weights and returns alone. Second, observation frequency must match decision frequency. The NASDAQ example makes the second point vividly (+31% becomes −4%). The long-only-as-a-timing-constraint argument is a clean mandate-design insight.
- **Practical use for a PM or allocator:**
  1. Split a manager's return into $\sum\bar\omega_i\bar R_i$ and the remainder. The passive piece is replicable, and fees, especially incentive fees, should attach to the remainder. A natural implementation is a hurdle equal to a static clone built from the manager's average weights.
  2. In a factor setting, estimate $\mathrm{Cov}(\beta_{p,t},F_t)$ per factor to separate timed from static exposure to value, momentum, carry and similar factors, and keep a separate residual-timing term.
  3. Demand holdings at the strategy's decision frequency, or accept that neither returns nor attribution can be verified from coarser reports. Comparing AP at native frequency with AP at the reporting frequency is a cheap test of whether reporting is adequate.
  4. For overlays such as stops and vol-targeting, the AR(1) and stop-loss formulas give the sign test directly: the overlay adds value only if its trigger variable predicts returns with the right sign.

---

*Scholar summary 2026-09-22. Source Drive `HedgeFundsAlpha_Lo_2007b.pdf` (id `0B-6kBz0I0dMsbi1GTG56RU8xYlE`).*

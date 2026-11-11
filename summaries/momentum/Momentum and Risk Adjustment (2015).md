# Momentum and Risk Adjustment

**Martin Dudler, Bruno Gmür (Quantica Capital), Semyon Malamud (EPFL/SFI) · 2015 · *Journal of Alternative Investments* (Fall 2015), 91–103 · Source file `Finance/MomentumVolAdj_Malamud_2015.pdf` · 64 liquid futures (15 equity index, 25 commodity, 13 bond, 5 interest-rate, 6 FX), daily data Jan 1984–Jan 2014**

## Claim / contribution
Time-series momentum (Moskowitz–Ooi–Pedersen 2012, "TSMOM") forms its *signal* from raw past returns. Because returns are heteroskedastic, that signal is a noisy estimate of the drift. **RAMOM** instead takes the sign of an average of *volatility-normalized* returns, with the same inverse-vol position sizing as TSMOM. The paper reports that RAMOM:
- beats TSMOM for most lookback/holding pairs;
- is less "straddle-like", with outperformance negatively related to volatility;
- has **~40% lower dollar turnover** (30–50% depending on horizon);
- after costs, has **~40% smaller maximum drawdown** and about **half the average time in drawdown**.
The paper is purely empirical and takes no stance on why momentum exists.

## Setup
- Log returns $r_{it}=\log(p_{it}/p_{i,t-1})$, $h$-day returns $r_{i,t,h}=\log(p_{it}/p_{i,t-h})$.
- EWMA variance $\sigma^2_{it}(\lambda)=\lambda\sigma^2_{i,t-1}(\lambda)+(1-\lambda)r_{it}^2$, with $\lambda=0.94/0.87/0.5$ ≈ 30/15/5-day windows.
- **Signal:** 12-day returns scaled by the lagged fast vol, averaged over the lookback:
$$R^{RA}_{i,t,h}(\lambda)=\frac1h\sum_{l=t-h}^{t}\frac{r_{i,l,12}}{\sigma_{i,l-1}(\lambda)},\qquad \lambda=0.5 \text{ by default}.$$
As $\lambda\to1$, RAMOM converges to TSMOM. The very fast $\lambda=0.5$ is chosen deliberately so that the normalization has bite. The window is shortened by 11 days so the effective lookback matches TSMOM.
- **Positions:** "months" are 25 trading days; $k_1$ (lookback) and $k_2$ (holding) run from 1 to 24. The book is the sum of the $k_2$ overlapping monthly-staggered signs, rebalanced **daily**, sized by $1/\sigma_{i,t-1}(0.94)$:
$$r^{RAMOM}_{it}(k_1,k_2,\lambda)=\Big(\sum_{l=0}^{k_2-1}\operatorname{sign}R^{RA}_{i,\,t-1-25l,\;25k_1-11}\Big)\frac{e^{r_{it}}-1}{\sigma_{i,t-1}(0.94)},\qquad R_t=\frac1{k_2N_{t-1}}\sum_i r_{it}.$$
TSMOM is identical except that it uses the sign of the raw $25k_1$-day return.
- **Benchmark:** long-only risk parity, $r^{RP}_{it}=(e^{r_{it}}-1)/\sigma_{i,t-1}(0.94)$. Full-sample Sharpe **1.1** and Calmar **0.2** (monthly rebalancing: 1.1/0.25 gross, **0.95/0.2 net** of costs).
- **Incremental test:** $R^{RAMOM}_t=\alpha+\beta R^{TSMOM}_t+\varepsilon_t$, reported as the annualized Sharpe of the zero-TSMOM-beta portfolio $R^{RAMOM}-\beta R^{TSMOM}$. A volatility-hedged version adds $\beta_2\Delta VIX_t$, which is tradable via VIX futures.

## Main results
(Exhibit tables are images; only numbers stated in the text are available.)
| Result | Number |
|---|---|
| RAMOM vs TSMOM Sharpe, grid of $(k_1,k_2)$ | ~10% higher for most pairs, up to 20% for some |
| Calmar, MOP (12,1) | +30% |
| Calmar, 3-month lookback | ×2 |
| RAMOM vs long-only RP | Sharpe +30–40%, Calmar ×2 |
| Zero-TSMOM-beta portfolio | positive for **all** pairs; (12,1) Sharpe **0.5**; $\lambda=0.5$ and $0.87$ similar |
| VIX-hedged zero-beta portfolio | $\beta_2$ on ΔVIX highly significant and **negative**; many Sharpes > 0.6 |
| Averaged strategy (all $k_1,k_2\in\{1,3,6,9,12\}$) | Sharpe only **~5%** higher, Calmar **30%** higher |
| Daily vs monthly rebalancing (gross) | 1m/1m: Sharpe 1.1 vs 0.7; 12m/1m: 1.4 vs 1.1 |
| After costs, TSMOM (12,1) | Sharpe 1.1 at either rebalancing frequency (daily gains eaten by costs) |
| After costs, RAMOM (12,1) daily | Sharpe ~20% higher than TSMOM; Calmar +40% (×2 for short horizons) |
| Turnover | RAMOM 30–50% lower (≈40% on average) |

**Mechanism** (regression of position changes on instrument volatility):
- $\Delta I^{RAMOM}-\Delta I^{TSMOM}$ on $\sigma_{it}$: no directional bias ($\beta_1$ insignificant, unstable sign).
- $|\Delta I^{RAMOM}-\Delta I^{TSMOM}|$ on $\sigma_{it}$: strongly negative. In high vol RAMOM behaves like TSMOM. In low vol it reacts much faster, so TSMOM's trades driven by volatility swings are filtered out.
- TSMOM drawdowns cluster in *low-vol* regimes, where RAMOM recovers faster.

**Subperiods.**
- Zero-beta Sharpe is higher in low-vol 1984–98 than in high-vol 2008–13, but the RAMOM/TSMOM Sharpe *ratio* is higher in 2008–13.
- The authors explain the paradox: if $R=\alpha+\beta F$ with $\operatorname{cov}(\alpha,F)=0$, then $SR_R/SR_F=\dfrac{E\alpha/EF+\beta}{\sqrt{\operatorname{Var}\alpha/\operatorname{Var}F+\beta^2}}$. This ratio blows up when $E[F]$ collapses, as TSMOM's did post-2008.
- Their lesson: evaluate by Jensen alpha or the benchmark-neutral Sharpe, not by Sharpe ratios.

## Critical assessment
- **Useful and credible as a signal-engineering idea.** Normalizing returns before aggregating is a t-stat-like, SNR-weighted trend estimate. It is closely related to averaging $r/\sigma$ (the "Sharpe of the lookback"), and the turnover reduction is mechanically plausible.
- **Weaknesses:**
  - Most evidence is in exhibits whose values are not in the text: grids of Sharpe/Calmar ratios, with no t-stats for the Sharpe differences despite the claim of "statistically significant" differences.
  - The 64×(24×24) grid invites data mining.
  - $\lambda=0.5$ is chosen ex post, and the headline averaged improvement is only ~5% in Sharpe.
  - Practitioner authors (Quantica) with a proprietary interest.
  - The cost model per asset class (Exhibit A2) is not given in the text.
  - Futures series are back-adjusted nearest contracts (5th expiry for short-rate futures), and a JPM bond index is used before bond futures existed.
- RAMOM's **negative vega** (loads negatively on ΔVIX) partly offsets TSMOM's well-known long-straddle property (Hurst–Ooi–Pedersen 2013). RAMOM is therefore a worse crisis hedge; this is a trade-off, not a free lunch.
- **Typos in the paper:**
  - "average time in drawdown for RAMOM is two times shorter than that for RAMOM" should say *TSMOM*.
  - The turnover comparison is cited as Exhibit 7 but is Exhibit 9.
  - Moskowitz is spelled "Moscowitz" throughout.
  - The index range in Eq. (4) (sum from $t-h$ to $t$ divided by $h$) is loose.
- An earlier version of this summary said RAMOM "outperforms particularly in calmer regimes" without noting that its *relative* Sharpe is higher in 2008–13, or that its averaged Sharpe gain is only ~5%. Both are corrected here.

## Practical relevance for a quant PM
- A cheap upgrade for any trend signal: aggregate $r_{t}/\hat\sigma_{t-1}$ (fast vol) rather than raw returns. Expect lower turnover and shallower drawdowns rather than a large Sharpe gain.
- The volatility estimator used for the signal (fast, λ≈0.5) should be separate from the one used for sizing (λ≈0.94).
- Daily rebalancing of trend signals only pays if the signal is turnover-efficient. Here TSMOM's daily edge disappears after costs; RAMOM's does not.
- Check the vega profile of the book: moving from TSMOM to RAMOM reduces the convex, crisis-alpha profile that many allocators pay CTAs for.

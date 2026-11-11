# Momentum Is Not an Anomaly

**Robert F. Dittmar, Gautam Kaul, Qin Lei · Oct 2007 · working paper (Michigan / SMU) · Source file `Finance/AbnormalReturnsMomentum_DittmarKaulLei_2007.pdf` · all NYSE/AMEX stocks, 1926–2006 (profits stamped Jul 1926–Jun 2006), 6-month ranking / 1-month gap / 6-month holding**

## Claim
The received view (Jegadeesh–Titman 1993/2001/2002, Grundy–Martin, Chen–Hong) is that momentum comes from positive serial covariance in the **firm-specific** return component, i.e. delayed reaction or continued overreaction. The authors propose a test that needs **no model of expected returns and no estimated decomposition**: run momentum on *base portfolios* of $n$ stocks and see how profits scale with $n$. Profits do not fall with $n$ when stocks are grouped by past-return rank, and they fall like $1/n$ when stocks are grouped at random. The authors conclude that "there is no momentum in the idiosyncratic components of security returns" and that momentum is driven entirely by cross-sectional differences in expected returns and risks.

## Setup
**Strategy (WRSS, Lo–MacKinlay type):** $w_{it}=\frac1N(r_{i,t-1}-r_{m,t-1})$, where $r_m$ is the equal-weighted market. Profit is $\pi_t=\sum_i w_{it}r_{it}$, and investment long is $I_t=\frac1{2N}\sum_i|r_{i,t-1}-r_{m,t-1}|$ (a measure of cross-sectional dispersion). Scaled profit is $\pi/I$. The authors warn that scaled profits can rise just because $I$ falls.

**Returns:** $r_{it}=\mu_i+\beta_if_t+\varepsilon_{it}$, with $E f=0$, $E(\varepsilon_{it}\varepsilon_{j,t-k})=0$ for $i\neq j$ and all $k$, and $E(f_t\varepsilon_{i,t-k})=0$. Own autocovariance of $\varepsilon$ is allowed. Then
$$E\pi_t=\tfrac1N\sum_iE(r_{it}r_{i,t-1})-E(r_{mt}r_{m,t-1})\quad\text{(own-products minus market own-product)}$$
$$=\sigma^2_\mu+\sigma^2_\beta\,\mathrm{Cov}(f_t,f_{t-1})+\text{(N-scaled terms)}+\tfrac{N-1}{N^2}\sum_i\mathrm{Cov}(\varepsilon_{it},\varepsilon_{i,t-1})\quad(10)$$
The first two terms are "rational" (cross-sectional); only the last is "irrational". Identification problem: separating them normally requires estimating $\mu_i,\beta_i$.

**Portfolio version:** $N/n$ equal-weighted base portfolios with $w_{pt}=\frac{n}{N}(r_{p,t-1}-r_{m,t-1})$. For large $N$ (Appendix A4):
$$E(\pi_{pt}|n)=\Big[\tfrac1n\overline{\mu_i^2}+\tfrac{n-1}{n}\overline{\mu_i\mu_j}^{PORT}-\overline{\mu_i\mu_j}^{ALL}\Big]+\Big[\tfrac1n\overline{\beta_i^2}+\tfrac{n-1}{n}\overline{\beta_i\beta_j}^{PORT}-\overline{\beta_i\beta_j}^{ALL}\Big]\mathrm{Cov}(f_t,f_{t-1})+\tfrac1n\overline{\mathrm{Cov}(\varepsilon_{it},\varepsilon_{i,t-1})}\quad(14)$$
Here PORT denotes the average over pairs within the same base portfolio and ALL the average over all pairs.
- **Random grouping:** $\overline{\cdot}^{PORT}\to\overline{\cdot}^{ALL}$, so $E(\pi|n)=\frac1nE(\pi|1)$ (eq. 15). This is not diagnostic; it serves as a placebo.
- **Rank grouping** (adjacent-ranked winners with winners, losers with losers): if rank proxies for $(\mu,\beta)$, then $\overline{\mu_i\mu_j}^{PORT}\approx\overline{\mu_i^2}$, so the systematic part is invariant to $n$ (eq. 16) while the idiosyncratic part still shrinks as $1/n$.
- **Sharpest test, $n=2$:** a pure idiosyncratic story predicts profits halve; a pure cross-sectional story predicts no change.

## Results
**Table 1: single-stock strategies (profit ×100 per 6-month holding period; Newey–West t)**
| | 1926–2006 | 26–46 | 46–66 | 66–86 | 86–06 |
|---|---|---|---|---|---|
| EW $\pi$ | 0.417 (6.51) | 0.371 (2.02) | 0.284 (6.00) | 0.463 (4.67) | 0.549 (3.96) |
| EW $\pi/I$ (%) | 4.38 (≈9% p.a.) | 2.82 | 4.56 | 4.66 | 5.48 |
| VW $\pi$ | 0.192 (4.84) | 0.277 (2.77) | 0.170 (4.99) | 0.163 (2.30) | 0.157 (1.67) |

Value-weighting ($w_i=v_{i,t-1}(r_{i,t-1}-r^{VW}_{m,t-1})$) cuts profits by more than half. VW profits are only 35% of EW in 1966–86 and under 30% in 1986–2006, where they are insignificant. Size therefore matters, which is consistent with either smaller-firm risk dispersion or Hong–Lim–Stein slow diffusion.

**Table 2: EW rank-portfolio strategies, full-sample $\pi(n)$ ×100**
| $n$ | 1 | 2 | 3 | 5 | 10 | 20 | 50 |
|---|---|---|---|---|---|---|---|
| Rank-grouped | 0.417 | **0.436** | 0.444 | 0.439 | 0.431 | 0.422 | 0.413 |
| Random (Table 5) | 0.417 | 0.222 | 0.145 | 0.076 | 0.037 | 0.017 | 0.008 |

- $I$ is identical across $n$ for rank grouping (0.094), because winners are never pooled with losers.
- Rank-grouped profits are flat in every 20-year subperiod. The one exception is a mild decline for $n>20$ in 1926–46 (0.371 → 0.289), still statistically indistinguishable from $n=1$.
- The $n=2$ point estimate exceeds $n=1$ in every subperiod except 1926–46.
- Scaled profit at $n=50$ is still more than 75% of $n=1$, versus the 2% the idiosyncratic hypothesis predicts.
- VW rank portfolios (Table 3) are also flat: 0.192 → 0.199 at $n=50$.
- Random grouping falls roughly as $1/n$ in every subperiod.

**Table 4: own- and cross-products (EW rank portfolios, full sample, ×100)**
- $n=1$: own-products 1.239 − market own-product 0.810 ≈ profit 0.417 (the small gap comes from stocks delisting during the holding period).
- $n=2$: own-products halve to 0.620, but weighted cross-products of 0.653 fully offset them. **Unweighted within-portfolio cross-products of 1.306** are about equal to own-products (1.239) and far above the all-pairs level of 0.810.
- $n=50$: weighted and unweighted cross-products are 1.222 and 1.247, still close to 1.239.
- Random portfolios (Table 6): unweighted cross-products at $n=2$ are 0.867 ≈ 0.810 (statistically indistinguishable), so profits vanish.
- The market own-product of 0.810 per 6 months implies a positive factor autocovariance unless the annual market mean exceeded ~18%. The authors argue that earlier negative autocorrelation estimates (JT93, MG99) are small-sample biased (Dixon 1944).

**Robustness:** results are qualitatively the same without the skip month (unlike MG's industry momentum), when all base portfolios are required to hold exactly $n$ stocks in both the ranking and holding periods, and when stocks are required to have all 6 ranking months of returns.

## Critical assessment
- **Elegant idea.** Momentum profit is a cross-sectional covariance, and grouping by the sorting variable versus at random is a model-free diagnostic in principle. The random-grouping placebo behaves exactly as predicted.
- **Main weakness (my assessment, not the authors').** The derivation of (14)/(16) treats portfolio membership as independent of the $\varepsilon$'s. But rank-based base portfolios are formed *on the same ranking-period returns* that enter the weights. Conditioning on adjacent ranks makes within-portfolio cross-products $E(\varepsilon_{i,t-1}\varepsilon_{j,t}\mid i,j\text{ adjacent})$ non-zero whenever there is own-autocorrelation: $j$ was selected for a large $\varepsilon_{j,t-1}$ and so has a high expected $\varepsilon_{j,t}$.
  - More directly, WRSS profits are linear in holding returns. When $n$ adjacent stocks have nearly equal ranking returns, $\sum_p n\,w_p\bar r_p\approx\sum_iw_ir_i$ *mechanically*, whatever the source of continuation.
  - Flat profits for $n\le50$ out of thousands of stocks, with identical investment $I$ across $n$, are therefore what one would expect under **either** hypothesis. The unweighted cross-product (1.306) ≈ own-product (1.239) is the same mechanical fact. The test appears to lack power against idiosyncratic continuation.
- The "irrational" term is defined under the strong assumption of zero cross-serial $\varepsilon$ correlation. Lead–lag effects (Lewellen) and industry effects are assigned to the rational side by construction.
- **No positive evidence on what the risks are.** No pricing model is estimated; the authors concede that behavioural biases could also generate cross-sectional patterns. Long-run reversals (JT01, Griffin–Ji–Martin) and January seasonality are explicitly left unaddressed; both are hard for a constant-$\mu_i$ story.
- The EW-vs-VW drop (Table 1) is informative, but the authors themselves acknowledge it is consistent with Hong–Lim–Stein underreaction.
- Units: profits are per 6-month holding period ×100 on a zero-investment WRSS, and only scaled profits ($\pi/I$) are comparable to returns. The paper is an unrefereed working paper (typos include "Korajzyck").

## Practical relevance for a quant PM
- The reliable empirical content: (i) EW WRSS momentum on NYSE/AMEX is about 4.4% per 6 months per dollar long, stable across 1926–2006 subperiods; (ii) VW momentum is less than half as large and insignificant post-1986 in this construction; (iii) aggregating adjacent-ranked names into small baskets costs nothing in expected profit and reduces name-level noise.
- Do not rely on the paper to conclude that momentum is a risk premium. Treat the "no idiosyncratic momentum" claim as unproven, given the mechanical-invariance issue above. Residual/idiosyncratic momentum (e.g. Blitz–Huij–Martens, Grundy–Martin) remains empirically strong in later work.
- The own/cross-product decomposition is a useful, estimation-free diagnostic when attributing a sort-based signal's P&L to within-group co-movement versus name-specific persistence.

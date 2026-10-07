# Do Industries Explain Momentum? — Moskowitz & Grinblatt (1999) — Detailed Quantitative Research Notes

| Field | Detail |
|------|--------|
| **Authors** | Tobias J. Moskowitz (Chicago GSB); Mark Grinblatt (UCLA Anderson) |
| **Venue** | *Journal of Finance* 54(4), August 1999 (Papers and Proceedings), pp. 1249–1290 |
| **Sample** | CRSP/COMPUSTAT, NYSE/AMEX/Nasdaq, July 1963 – July 1995 (characteristic- and DGTW-adjusted results: Jan 1973 – Jul 1995) |
| **Industries** | 20 value-weighted portfolios from two-digit CRSP SIC codes (time-varying), avg. ~230 stocks each |
| **Source file** | `Finance/AbnormalReturnsIndustryMomentum_MoskowitzGrinblatt_1999.pdf` (JSTOR scan; OCR renders Table II/III as "Table 11/111", some tables unreadable) |

## Question

Is intermediate-horizon (6–12 month) stock momentum driven by firm-specific return persistence, by cross-sectional dispersion in unconditional means (Conrad–Kaul 1998), by serial correlation in priced factors, or by persistence in the *industry* component of returns? Answer: mostly industry. A second, underappreciated point: because winners and losers cluster by industry, momentum portfolios are poorly diversified, so momentum is "a good deal but far from an arbitrage."

## Model and decomposition

Returns follow a factor + industry + idiosyncratic structure (constant $r_f$):

$$
r_{jt} = \mu_j + \sum_{k=1}^{K} \beta_{jk} R_{kt} + \sum_{m=1}^{M} \theta_{jm} \delta_{mt} + \varepsilon_{jt},
$$

where $R_k$ are zero-cost factor-mimicking portfolios (think Fama–French or Daniel–Titman characteristic matches) carrying the unconditional premia, $\delta_m$ are industry components orthogonal to the factors with zero unconditional mean (and, per Table I, no detectable premium), and $\varepsilon_j$ is firm-specific. Own-autocorrelations are allowed, cross-autocorrelations are not. For the linear momentum portfolio with weights $(r_{j,t-1}-\bar r_{t-1})$ funded by the equal-weighted index, expected profits averaged over stocks decompose into four terms:

$$
\sigma^2_\mu \;+\; \sum_k \sigma^2_{\beta_k}\,\mathrm{Cov}(R_{kt},R_{k,t-1}) \;+\; \sum_m \sigma^2_{\theta_m}\,\mathrm{Cov}(\delta_{mt},\delta_{m,t-1}) \;+\; \overline{\mathrm{Cov}(\varepsilon_{jt},\varepsilon_{j,t-1})}.
$$

(1) Conrad–Kaul mean dispersion; (2) factor serial correlation; (3) industry serial correlation; (4) firm-specific serial correlation (Jegadeesh–Titman underreaction). The empirical strategy is to kill terms one at a time. The linear portfolio correlates 0.95 with their 30%-breakpoint strategy and 0.93 with JT deciles, justifying the mapping.

## Design

- **Stock momentum (6,6):** rank on $t-6$ to $t-1$ returns; value-weight top 30% minus bottom 30%; hold 6 months; JT overlapping-cohort averaging (each month's return is 1/6 from each of six cohorts, so the adjacent month contributes little bid-ask/lead-lag contamination).
- **Industry momentum IM(L,H):** long the 3 best, short the 3 worst of 20 VW industries on past $L$-month return, hold $H$ months, rebalanced monthly.
- **Adjustments:** Daniel–Titman size×BE/ME (25 portfolios) matched returns; DGTW 125 size×BE/ME×12-month-return benchmarks; contemporaneous industry-return subtraction.
- **Placebo "random industries":** each stock replaced by the average of the stocks ranked just above and below it on past 6-month return, so the pseudo-industry has the same momentum profile but not the same industry membership.
- **Industry-neutral / excess-industry / cross strategies** (Table II Panel C).

## Results (6,6 unless stated)

**Factors and mean dispersion are not the source.**
- Six-month serial covariance of the EW index $\approx -0.0001$; of Mkt–rf, SMB, HML: $-0.00008$, $0.00007$, $0.00004$ (autocorrelations $-0.038$, $0.102$, $0.061$), all insignificant. Momentum across the three FF factors: $-0.05\%$/mo ($t=-0.42$).
- Cross-sectional variance of ex-post mean industry monthly returns 0.00083 vs 0.011 for stocks; F-test of equal industry means not rejected; no industry has a significant size/BE/ME-adjusted alpha after Bonferroni.

**Baseline magnitudes.**
- Stock momentum (VW, 30% breakpoints): about 0.43%/mo, ~6%/yr per dollar long. EW within 30% legs: ~9.3%/yr. JT (EW, deciles) ~12%/yr.
- Industry momentum IM(6,6), VW industries: **0.43%/mo** — identical to stock momentum. EW industries: **0.81%/mo, ~10.2%/yr ($t=7.71$)**, ~90 bp/yr above the EW stock strategy. This directly contradicts Conrad–Kaul: industries have far less mean dispersion but equal or larger momentum.
- Size/BE/ME-adjusted stock momentum: 0.29%/mo ($t=3.34$), not significantly different from raw (difference 13 bp, $t=1.40$; the gap is concentrated pre-1980 when the size effect was alive).
- DGTW-adjusted industry momentum: **0.20%/mo ($t=2.27$)**, not significantly below raw 0.43%. DGTW explains ~85% of cross-sectional variation in industry means and ~56% / ~38% of the time-series variance of the stock / industry strategies. Subtracting each stock's full-sample mean before forming the industry strategy yields *larger* profits.

**Industry control kills stock momentum.**

| Strategy (Table II) | Mean monthly profit | t-stat |
|---|---|---|
| Stock momentum, industry-adjusted returns | 0.13% | 2.04 (attributed to early-sample size effect) |
| Stock momentum, size/BE/ME- and industry-adjusted | negligible | – |
| Stock momentum, random-industry-adjusted | virtually unchanged from unadjusted | – |
| Random-industry momentum | nonexistent | – |
| Industry-neutral (30/30 within each industry, VW) | 0.11% | 1.01 |
| Excess-industry (rank on return minus industry return) | −0.07% | −0.83 |
| Long losers in 3 best industries, short winners in 3 worst | **+0.30%** | significant |

The last row is the sharpest test: it bets *against* stock momentum and *with* industry momentum, and it earns positive, significant profits.

**Horizons (Table III).** Industry momentum is strongest at IM(1,1) — the opposite sign of the Jegadeesh (1990) one-month reversal in stocks — strong at 3–12 months, fades after a year, weakly reverses at (24,36) (reversals stronger with fewer industries per leg). Skipping a month in the (6,6) strategy: 0.40% vs 0.43%/mo. Skipping a month eliminates IM(1,1) profits, which the authors attribute to decaying autocorrelation, not microstructure. Industry partial autocorrelations (Table IV) mirror this: average lag-1 ~0.087, near zero at 6, 12 and 36 lags. No industry dominates IM(1,1) legs (max 80 of 347 months in the winner leg; max 5 consecutive months; average ranks 10.0–11.0; month-to-month rank correlation ~0.02), again against a mean-dispersion story.

**Long vs short.** For IM(6,6), winners minus middle 3 industries earns 0.36%/mo, middle minus losers 0.07%/mo: profits come from the long side (contrast with stock momentum, where shorting illiquid losers dominates; Hong–Lim–Stein). IM(1,1) profits are split evenly. Buy-side profits decay within 12 months and reverse at 24–36; sell-side profits decay slower and do not reverse, consistent with short-sale frictions slowing arbitrage of bad news.

**Lead-lag and liquidity (Table V).** Restricting IM(1,1) to the largest size quintile within each industry: 0.99%/mo ($t=5.89$; DGTW 0.43%, $t=3.54$); largest dollar-volume quintile: 1.56%/mo ($t=9.27$). Small-stock quintiles earn more on a rebalanced basis (1.78%/mo), evidence of a genuine within-industry large-to-small lead-lag, but with VW industries the largest size quintile contributes 75% of raw and 77% of DGTW-adjusted profits, the smallest under 1%. Random industries show no IM(1,1) effect either. The response to Grundy–Martin is that if momentum does not exist intra-industry, industry momentum is by definition some within-industry lead-lag; the point is it is not size/liquidity/microstructure.

**Trading costs.** IM(6,6) turnover ~200%/yr, breakeven ~75 bp per one-way dollar traded; holding 6 extra months does not reduce average returns, so turnover can fall to ~100%/yr and breakeven rises to ~150 bp — above institutional cost estimates for mid/large caps, though the authors leave net profitability as open. IM(1,1) is described as unlikely to survive costs.

**Fama–MacBeth (Table VI, 1973–1995, size/BE/ME-adjusted returns).** Industry past returns subsume stock past returns at (6,1) and (6,6) horizons; the one-month industry return in turn absorbs much of the six-month industry effect. The exception is **12-month stock momentum (12,1)**, which remains significant alongside industry variables; results are unchanged when skipping a month ((7,2), (12,2) etc.). Industry momentum is never subsumed by stock momentum. The authors suggest the surviving 12-month stock effect may be largely tax-loss seasonality (Grinblatt–Moskowitz 1999).

## Interpretation offered

Hot/cold sector herding; DHS overconfidence concentrated in hard-to-value new industries; BSV conservatism/representativeness at the industry level; Hong–Stein slow diffusion from industry leaders to followers; rational growth-option (Berk–Green–Naik) or irreversible-investment (Kogan) channels with industry-correlated risk. None is tested — explicitly left as conjecture.

## Assessment

- **Convincing:** the decomposition-plus-placebo design (random industries, cross strategy, excess-industry sort) is cleaner than most momentum papers; the size-quintile contribution analysis defuses the "it's all small-cap lead-lag" objection for VW industries.
- **Fragile:** only 20 coarse SIC industries and a 3-vs-3 long/short, so the industry strategy is highly concentrated; several comparisons (raw 0.43 vs DGTW 0.20; industry 0.43 vs stock 0.43) rest on differences that are statistically insignificant. The claim that industry "explains" stock momentum is weakest at 12-month formation, which is the horizon most practitioners actually use (12-1). Subsequent literature (e.g., Grundy–Martin; later work with finer industries) finds substantial residual/intra-industry momentum at 12-1, so "industry-neutral stock momentum is dead" should not be taken at face value outside this sample and construction.
- **Much of the headline industry effect is the one-month industry continuation**, which is costly to trade and decays fast.
- **Practical relevance:** (i) stock momentum books carry large, concentrated industry bets — decide explicitly whether to neutralize or harvest them; (ii) industry momentum is long-side driven and works in the largest, most liquid names, making it amenable to long-only tilts and sector ETF/futures implementations; (iii) combine 1-month industry, 6-month industry and 12-month stock signals rather than treating them as one factor; (iv) evaluate on the Wi–Mid / Mid–Lo split, not only Wi–Lo, since leg asymmetry differs sharply between stock and industry momentum.

# Searching the Factor Zoo

**Authors:** Soosung Hwang and Alexandre Rubesam  
**Version:** March 2018 working paper (SSRN: https://ssrn.com/abstract=3100811)  
**Note on filename:** Drive file is named `AbnormalReturnsReview_Hwang_2018.pdf` but the paper title is *Searching the Factor Zoo*.  
**Source file:** Finance/AbnormalReturnsReview_Hwang_2018.pdf  
**Summary prepared:** 2026-09-24 (Scholar batch_2026-09-24_1)  
**OCR:** Not required; clean extract (~18,770 words of source)

---

## Question and claims

With hundreds of published factors, which *combinations* actually describe returns? Instead of testing factors one at a time against a baseline model (FF5, HXZ), the authors search the space of linear factor models with Bayesian variable selection, using thousands of individual stocks as test assets to avoid the characteristic-sorted-portfolio problem (Lo-MacKinlay, Berk, Lewellen-Nagel-Shanken). Claims:
1. Only a handful of factors are selected for individual stocks in any period.
2. The market excess return is the only factor selected consistently over time.
3. The other selected factors rotate and are not FF3/FF5/Chen-Zhang/HXZ factors. They include short-term reversal (`mom1m`), change in 6-month momentum (`chmom`), earnings-announcement return and volume (`ear`, `aeavol`), change in analyst coverage (`chanalyst`), industry concentration (`herf`), `sue`, and industry-adjusted size (`mve_ia`).
4. On characteristic-sorted portfolios, the method selects factors built from the sorting characteristic.

## Method

For $N$ assets with common regressors $X$ ($T\times K$, including an intercept column), the model is a SUR:
$$r_i = X\beta_i + e_i,\qquad \tilde e \sim N(0,\Sigma\otimes I_T),$$
with contemporaneously correlated but serially uncorrelated errors. Priors: $\beta \sim N(b_0,B_0)$ and $\Sigma \sim IW(\nu_0,\Lambda_0)$ with $\nu_0 = N$, $\Lambda_0 = I$.

**Selection.** This extends Kuo-Mallick (1998) to SUR: a single inclusion vector $\gamma\in\{0,1\}^K$ is *common to all $N$ equations*, with the regressors replaced by $X_\gamma$ and $\gamma_j \sim \text{Bernoulli}(\pi_j)$ independent of $\beta$ (non-hierarchical, so no spike-and-slab tuning). The Gibbs update is
$$P(\gamma_j=1\mid\cdot)=\Big[1+\tfrac{1-\pi_j}{\pi_j}\exp\{-\tfrac12\mathrm{Tr}(\Sigma^{-1}(S_1-S_0))\}\Big]^{-1},$$
where $S_1, S_0$ are residual cross-product matrices with factor $j$ in and out. The computational contribution is sampling each $\beta_i$ conditionally on the others, which needs only $K\times K$ and $N\times N$ objects rather than $NT\times NT$. This makes $N\approx 1{,}000$ stocks feasible.

**Defaults.** Empirical-Bayes prior $\beta_i \sim N(\hat\beta_i^{OLS}, c\,(X'X)^{-1})$ with $c=1$; $\pi_j=0.5$, so all $2^K$ models are equally likely a priori; 10,000 MCMC iterations for stocks and 50,000 for portfolios. The intercept is one of the candidate "factors"; its selection is read as evidence that the model leaves alpha.

## Data

- **Factors:** 82 characteristics from Green, Hand and Zhang (2017) (12 GHZ characteristics dropped for missing data or degenerate deciles), each turned into a VW top-minus-bottom decile return (unsigned), plus the market excess return from French's library. Monthly, 1980-2016 (444 months), with coverage varying by factor (`herf` from 2000, `nanalyst` from 2007).
- **Factor zoo statistics (Table 1):** 27 factors have $|t|>2$, but only 6 survive Benjamini-Yekutieli FDR at 5%: `acc`, `chcsho`, `chinv`, `invest`, `nanalyst`, `sfe`. Pairwise absolute correlations (July 2007-2016, 3,403 pairs) have median 0.179, 90% below 0.498, and 4 above 0.90.
- **Test assets:** NYSE/AMEX/NASDAQ common stocks excluding financials, microcaps (below the NYSE 20th percentile) and sub-$1 stocks, with survivorship bias limited by using sub-periods. Microcaps are run separately. Portfolios: 20 French-library sets (13 univariate sorts, 6 bivariate sorts, 49 industries; over 300 portfolios), 1980-2016.

## Results

**Three 12-13-year windows, all available factors (Table 3):**

| Window | $N$ / $K$ | Top models (posterior) | Marginal > 0.5 |
|---|---|---|---|
| 1980-1991 | 807 / 75 | mkt+chmom 0.24; mkt+mom1m 0.16; mkt+mom1m+ms 0.16 | mkt, chmom |
| 1992-2003 | 893 / 81 | mkt 0.64; mkt+aeavol 0.32 | mkt |
| 2004-2016 | 967 / 83 | int+mkt+herf+mom1m 0.24; mkt+chanalyst+herf+mom1m 0.20 | mkt, herf, (intercept), mom1m in every top model |

Twelve factors plus the intercept are ever selected. Models with ≤5 factors dominate, although the top-13 list in 2004-16 reaches 7. The intercept enters in 2004-16, which the authors read as model inadequacy in that window.

**Five ~7.5-year windows, 44-49 factors (the GHZ-significant set), 1,014-1,296 stocks (Table 4):**
- 1980-Jun 1987: mkt+chmom, posterior 1.0.
- Jul 1987-1994: mkt+chmom+ear+mom1m 0.8; without mom1m 0.2.
- 1995-Jun 2002: mkt alone 0.44; mkt+pctacc 0.16; mkt+mom1m 0.12.
- Jul 2002-2009: mkt+sue 0.44; mkt+bm 0.16; mkt+bm+sue 0.16.
- 2010-2016: mkt+mom1m+mve_ia 0.36; mkt+mve_ia 0.28; mkt+mom1m+mve_ia+sue 0.24.

At most 4 factors are selected, 10 factors in total. Six ever have marginal > 0.5 (mkt, chmom, ear, mom1m, mve_ia, sue). The intercept is never selected, so shorter windows reduce apparent misspecification, consistent with time-varying true models.

**Microcaps (Table 5):** 6 factors ever selected. In 1995-Jun 2002 the top two models omit the market: `aeavol` alone 0.48, `aeavol`+`chanalyst` 0.40. The authors attribute this to tech-bubble microcaps trading on news more than on the market. In 2010-16 the market alone gets posterior 1.0.

**Portfolios, full 1980-2016 (Table 6):** the selected factors mirror the sort variable. Size portfolios select `mve_ia`, B/M portfolios `bm`, OP portfolios `roic`, and the FF25 select `mve_ia`+`lev`, where `lev` has ~0.70 correlation with `bm`. Best-model posteriors range from 0.10 (long-term reversal sorts) to 0.57 (OP), and are ~0.2 for double sorts. The intercept is never selected even with $T=444$, which the authors treat as "incorrectly promising". The market is the only factor with average posterior > 0.5 across portfolio sets. The 49 industries select mkt, beta, illiquidity, leverage and organizational capital.

**Robustness:** with $c=5$ (a more diffuse prior), results for stocks are virtually identical. For portfolios, fewer factors are selected with higher posterior mass, and the sort-mirroring pattern persists.

**Comparisons:** GHZ (2017) find 12 characteristics significant in FM regressions (9 for non-microcaps), overlapping here only on `ear` and `mom1m`. Barillas-Shanken (2017) favor a six-factor model, but they search only 10 factors and use portfolios related to those factors. Harvey-Liu (2016, "lucky factors") also find the market dominant for individual stocks.

## Assessment

- **What the method actually measures.** Selection is driven by $\mathrm{Tr}(\Sigma^{-1}(S_1-S_0))$, i.e. how much a factor reduces time-series residual covariance across stocks. That is a covariance-explaining criterion, not a test of whether a factor carries a premium or prices the cross-section of expected returns. This explains why the winners are high-comovement, often premium-less factors. `mom1m` has $t=-1.06$, `herf` $t=-0.38$ and `aeavol` $t=0.00$, while none of the six FDR-significant premia (`acc`, `invest`, `chinv`, …) is ever selected. The headline "FF5 factors are not selected" therefore says FF5 factors add little *time-series explanatory power* for individual stocks beyond the market and a few others. It does not say they lack premia. Relative to FF5 as a pricing model, this is a different question.
- **Intercept inference is weak.** A single common $\gamma$ for the intercept across ~1,000 noisy single-stock equations has low power, so "no intercept ⇒ the model prices stocks" is not comparable to a GRS-type rejection. Conversely, selecting the intercept only in the 144-156-month windows may reflect nonstationarity rather than a missing factor.
- **Numerical coarseness.** Every reported posterior is a multiple of 0.04 (e.g., 0.24, 0.64, 0.44), which is consistent with only ~25 effectively retained draws. Model probabilities therefore carry large Monte Carlo error, and "posterior 1.0" means 25 of 25 draws. With $N > T$ and $\nu_0 = N$, $\Lambda_0 = I$, the $\Sigma$ posterior leans heavily on the prior; residual cross-sectional structure beyond the selected factors is effectively regularized away.
- **Other design limits:** unsigned decile spreads, VW deciles over the full CRSP universe, a common factor set for all stocks (no stock-specific selection), static betas within each window, and survivorship within windows.
- **Convincing:** the portfolio exercise is a clean demonstration that sorted test assets pre-determine which factors get selected. The individual-stock results support a strongly market-dominated, sparse and unstable time-series factor structure once dozens of correlated long-short factors compete jointly.
- **For a quant PM:** relevant to *risk-model* factor selection more than to alpha. For stock-level covariance, the market plus a few short-horizon, event-driven and industry-level factors capture most of what 80 anomaly spreads add, and the membership of that set rotates. It does not justify dropping value/profitability/investment as return sources. Separate "explains covariance" from "earns a premium" when reading the headline. When validating a factor, avoid test portfolios sorted on the same characteristic.

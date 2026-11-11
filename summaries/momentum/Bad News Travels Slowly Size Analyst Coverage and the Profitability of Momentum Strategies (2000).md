# Bad News Travels Slowly: Size, Analyst Coverage, and the Profitability of Momentum Strategies

**Harrison Hong, Terence Lim, Jeremy C. Stein · 2000 · *Journal of Finance* 55(1), 265–295 · Source: `Finance/AbnormalReturnsMomentum_HongLimStein_2000.pdf` · CRSP NYSE/AMEX/Nasdaq common stocks (share codes 10/11), I/B/E/S analyst counts, 1980–1996 (returns)**

## Claim
A direct test of an auxiliary prediction of the Hong–Stein (1999) gradual-information-diffusion model: momentum should be stronger where firm-specific information spreads slowly. Three results: (1) past the very smallest stocks, momentum profits **decline sharply with size**; (2) **holding size fixed, momentum is stronger for low residual analyst coverage** (≈60% larger in the lowest vs highest coverage tercile); (3) the coverage effect comes **almost entirely from past losers** — bad news diffuses slowly (managers push good news out themselves; analysts matter for bad news).

## Setup
- **Momentum measure:** 6-month ranking / 6-month holding (Jegadeesh–Titman), equal-weighted, but terciles rather than deciles: P1 = worst 30%, P2 = middle 40%, P3 = best 30%; momentum = **P3 − P1** (better signal-to-noise when splitting into up to 12 subsamples; P10−P1 gives larger point differences but lower t-stats).
- **Coverage:** number of I/B/E/S analysts with FY1 estimates that month; unmatched CUSIPs = 0 (measurement error biases toward null). Uncovered share: 77.3% (1976), 58.2% (1980), 36.9% (1996); hence sample starts 1980. Below the 20th NYSE/AMEX size percentile (~\$30m mid-sample, ~\$60m in 1996) 82% of firms have no analyst (1988) → all coverage tests exclude these stocks.
- **Residual coverage:** monthly cross-sectional OLS
$$\log(1+\text{Analysts}_{it})=a_t+b_t\log(\text{Size}_{it})+c_t\,\text{NASD}_{it}+\varepsilon_{it}$$
  (Model 1, $R^2=0.61$ in Dec 1988, size coefficient 0.54, $t=52.7$). Adding 15 industry dummies: $R^2=0.63$; B/M, Scholes–Williams beta, $1/P$, variance, lagged returns, turnover, option-listing dummy raise $R^2$ to at most 0.65 — size dominates. Beta (+0.38, $t=11.5$), B/M, turnover and options enter positively.
- **Timing:** residual coverage measured 6 months *before* the ranking period (stale, to avoid endogeneity: analysts initiate on optimism, recommendation drift lasts ~6 months); results similar with 0, 12, 18-month lags. Coverage and past-return sorts are independent; coverage terciles Sub1 (low) / Sub2 / Sub3 (high).

## Main results (monthly returns, t-stats in parentheses)

**Table III — P3 − P1 by NYSE/AMEX size decile (all stocks):**

| All | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 | D10 |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.53% (2.61) | −0.37% (−1.77) | 0.85 (3.60) | **1.43 (6.66)** | 1.38 (6.10) | 1.19 (5.32) | 1.04 (4.80) | 0.89 (3.72) | 0.43 (1.90) | 0.44 (1.73) | 0.02 (0.08) |

Inverted U: negative in the tiniest stocks (mean cap \$7m; thin market-making/reversal, or price discreteness), peak in decile 3 (mean \$44m, mean 1.1 analysts), ~0 in the largest (mean \$7.3bn, 21 analysts). Losers dominate: (P2−P1)/(P3−P1) ≈ 0.73–0.90 in deciles 2–8 (1.09 in D9); in D3, 1.05 of the 1.43% comes from P2−P1. The 0.53% is below JT's 0.95% because of terciles and inclusion of tiny Nasdaq stocks, not the period (NYSE/AMEX P10−P1 replicates JT).

**Table IV — sort on Model-1 residual coverage (stocks > 20th pct):**

| | All | Sub1 (low) | Sub2 | Sub3 (high) | Sub1 − Sub3 |
|---|---|---|---|---|---|
| P1 | 0.62% | 0.27 | 0.67 | 0.97 | **−0.70 (−5.16)** |
| P3 | 1.56 | 1.40 | 1.58 | 1.69 | −0.29 (−2.80) |
| P3 − P1 | 0.94 (4.89) | **1.13 (5.46)** | 0.92 (4.64) | 0.72 (3.74) | **0.42 (3.50)** |
| Median analysts | | 0.1 | 3.5 | 7.6 | |
| Median size (\$m) | | 103 | 200 | 180 | |

- The difference is entirely on the loser side. **LAST ("loser-analyst-spread trade")** = long P1/Sub3, short P1/Sub1: **0.70%/month (t = 5.16)**, size- and momentum-neutral. Low-coverage winners do slightly *worse* than high-coverage winners (fragile; vanishes beta-adjusted — median beta 0.75 in Sub1 vs 0.95 in Sub3).
- Size matching is imperfect (mean size Sub1 \$962m vs Sub3 \$455m because coverage saturates for mega-caps, which land in Sub1) → Table V.

**Table V — double sort (coverage residuals estimated within each size class):** P3 − P1

| Size class (NYSE/AMEX pct) | Sub1 | Sub2 | Sub3 | Sub1 − Sub3 |
|---|---|---|---|---|
| 20–40 (mean \$63m; median analysts 0.0/0.9/3.1) | 1.51 (6.46) | 1.39 | 1.15 (5.10) | **0.36 (2.13)** |
| 40–60 (~\$200m) | 1.06 (4.49) | 0.98 | 0.73 (3.60) | 0.33 (1.95) |
| 60–80 (~\$650m) | 0.61 (3.11) | 0.32 | 0.42 (2.02) | 0.18 (1.18) |
| 80–100 | 0.09 (0.49) | 0.01 | 0.07 (0.33) | 0.02 (0.14) |

Sizes are now almost perfectly matched within class; the coverage effect decays with size, as predicted. Holding size fixed understates total diffusion effects (even Sub3 in class 1 has only ~3 analysts).

## Robustness
| Variant | Sub1−Sub3 (P3−P1) | LAST |
|---|---|---|
| Beta-adjusted returns (market model, rank and hold) — Table VI | 0.49% (4.04); overall P3−P1 1.20% (5.99) | 0.50% (3.64) |
| Residuals with industry dummies (Model 2) | 0.33% (3.06) | 0.60% (5.03) |
| Residuals incl. turnover (Model 8), 1984–96, loses ~12% of firms — Table VII | 0.31% (2.23) | 0.56% (3.58) |
| + options-listing dummy (Model 9) | ≈ Table VII | ≈ Table VII |
| Skip one month | ≈ Table IV | |
| Excluding January | 0.46% (3.75) | |

- **B/M:** median B/M 0.57 (Sub1) vs 0.69 (Sub3) ⇒ ≈0.10%/month by Fama–French (1992) — too small to explain LAST.
- **Subperiods (Table VIII):** Sub1−Sub3 = 0.65% (2.90) 1980–84, 0.31% (1.62) 1985–90, 0.33% (1.60) 1991–96; LAST = 0.93% (3.48), 0.54% (2.21), 0.68% (3.34) — significant in all three. Overall momentum nearly disappears in 1991–96 (P3−P1 0.33%, t = 0.97, vs 1.14% and 1.38% earlier).
- **Event time (Fig. 2, beta-adjusted):** high-coverage momentum stops after ~10 months; low-coverage keeps accruing to ~24 months. 24-month cumulative P3−P1: **19.63% (Sub1) vs 8.90% (Sub3)**, difference 10.73%; cumulative LAST 9.32% — i.e. low-coverage stocks underreact by ~20% vs ~9% and take ~2 years vs <1 year to adjust.
- **Regression approach (Table IX, 1979–92):** for each stock, RHO = slope of 6-month excess returns on lagged 6-month returns (49 overlapping obs over 5 years); cross-sectional regressions on $\log(1+\text{Analysts})$, log size, Nasdaq dummy. Coverage coefficient negative in 13/14 years; Fama–MacBeth **−0.0125 (t = −3.80)**, pooled −0.0127 (−5.09); size insignificant. With interaction: coverage −0.0630 (FM t −1.89; pooled −5.05), size −0.0094 (−2.37), coverage×size +0.0041 (FM 1.54; pooled 4.45) — coverage matters less for large firms. Implied magnitude: Δρ = 0.0125·(ln 8.6 − ln 1.1) = 0.026 × ~60% P3–P1 formation spread ⇒ 1.56% per 6 months ≈ 0.25%/month (vs 0.42% in Table IV); for the smallest class, ≈0.60%/month (vs 0.36%). Adding beta does not change results; Kendall small-sample bias $-(1+3\rho)/T$ only rescales RHO.

## Critical assessment
- **Convincing:** clean design (stale, size-residualized coverage; double sorts with matched size; loser-only, momentum-neutral LAST spread); consistent across beta adjustment, industries, turnover/options controls, subperiods, event time and a parametric regression.
- **Caveats:** coverage may proxy for unmeasured trading frictions — especially short-sale costs, which would also produce loser-side sluggishness (Diamond–Verrecchia); turnover and option listing are crude proxies, as the authors concede. Turnover control is ambiguous (coverage may cause volume). Equal-weighted, no transaction costs; the loser leg in low-coverage small caps is exactly the hardest/most expensive to short. Momentum itself fades in 1991–96. The size result is hump-shaped, not monotone, and coverage tests exclude the bottom 20% (NYSE breakpoints) by construction. Minor text slip: the 40–60 class differential is described as "Sub3 − Sub1" but is Sub1 − Sub3.

## Practical relevance for a quant PM
- Condition momentum on information environment: the loser leg in low-residual-coverage small/mid caps carries most of the continuation; the effect is near zero in the top NYSE size quintile — where most capacity is.
- LAST-type spreads (short low-coverage losers vs long high-coverage losers) are a momentum-neutral way to harvest slow diffusion of bad news, but borrow cost/availability must be modelled explicitly since it is the leading alternative explanation.
- Residualize coverage on log size (and exchange) cross-sectionally each month; use $\log(1+N)$ and lagged coverage. The longer decay (≈2 years) in low-coverage names argues for longer holding periods/slower signal decay in those buckets.

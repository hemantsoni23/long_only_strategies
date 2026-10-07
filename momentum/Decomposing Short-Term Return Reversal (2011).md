# Decomposing Short-Term Return Reversal

**Zhi Da, Qianqiu Liu, Ernst Schaumburg · 2011 · Federal Reserve Bank of New York Staff Report no. 513 (Sept. 2011; later published as "A Closer Look at the Short-Term Return Reversal", *Management Science* 2014) · Source: `Finance/AbnormalReturnsMomentumMeanReversionDecomposition_DaLiuSchaumburg_2011.pdf` · Sample: I/B/E/S-covered US stocks, price ≥ \$5, Jan 1982–Mar 2009 (≈2,355 stocks/month, ≈74% of CRSP market cap, mean cap \$2.5bn, ~8 analysts)**

## Claim
The profit of the standard 1-month reversal strategy decomposes exactly into (1) across-industry momentum (negative), (2) within-industry expected-return dispersion (≈0), (3) reaction to within-industry cash-flow news (**negative: underreaction / earnings momentum**), and (4) a residual "discount-rate" (non-cash-flow) component — the **only positive term, ≈2.5× the total profit**. A within-industry reversal on this residual (DR) earns a 3-factor alpha of **1.34%/month (t = 9.28)** vs 0.33% (t = 1.37) for the standard strategy (the abstract says "three times", the conclusion correctly "four times"). The long leg (buying DR losers) is liquidity provision; the short leg (selling DR winners) is sentiment-driven overpricing with short-sale constraints.

## Decomposition
Lehmann / Lo–MacKinlay weights $w_{i,t}=-\frac1N(r_{i,t-1}-r^M_{t-1})$, profit $\pi_t=-\frac1N\sum_i(r_{i,t-1}-r^M_{t-1})r_{i,t}$. With industry $j$ ($N^j$ stocks, mean return $r^j$):
$$\pi_t=\underbrace{-\frac1N\sum_jN^j(r^j_{t-1}-r^M_{t-1})r^j_t}_{\Omega_{m,t}\ \text{(across-industry)}}+\frac1N\sum_jN^j\pi^j_t .$$
Campbell–Shiller: $r_{i,t+1}=\mu_{i,t}+CF_{i,t+1}+DR_{i,t+1}$, $CF=(E_{t+1}-E_t)\sum_{j\ge0}\rho^j\Delta d$, $DR=-(E_{t+1}-E_t)\sum_{j\ge1}\rho^jr$. With industry-demeaned tildes,
$$\pi^j_t=\underbrace{-\tfrac{1}{N^j}\textstyle\sum_i(\mu_{i,t-2}-\mu^j_{t-2})r_{i,t}}_{\Omega^j_\mu}\ \underbrace{-\tfrac{1}{N^j}\textstyle\sum_i\widetilde{CF}_{i,t-1}r_{i,t}}_{\Omega^j_{CF}}\ \underbrace{-\tfrac{1}{N^j}\textstyle\sum_i\widetilde{DR}_{i,t-1}r_{i,t}}_{\Omega^j_{DR}},$$
so $\pi_t=\Omega_{m,t}+\Omega_{\mu,t}+\Omega_{CF,t}+\Omega_{DR,t}$ — an identity period by period; each term is a zero-investment strategy. Weights are rescaled by $M_t=\frac12\sum_i|w_{i,t}|$ so each leg is \$1 and profits are returns.

## Measurement
- **Expected return $\mu$:** FF3 with betas from rolling 60-month windows (min. 36); factor premia = full-sample average factor returns (CAPM/5-factor give similar results).
- **Cash-flow news** (Da–Warachka 2009, from I/B/E/S unadjusted consensus, $A1$, $A2$, $LTG$): expected earnings $X_{t,t+1}=A1$, $X_{t,t+2}=A2$, then grow at $LTG$ to year 5; linear fade from $LTG$ to $g_t$ (cross-sectional mean $LTG$) over years 6–10; clean-surplus book value with payout $\psi=5\%$ of book; expected log accounting return $e_{t,t+j+1}=\log(1+X_{t,t+j+1}/B_{t,t+j})$ for $j\le9$, $\log(1+g_t/(1-\psi))$ thereafter; $\rho=0.95$:
$$CF_{t+1}=E_{t+1}\sum_{j\ge0}\rho^je_{t+j+1}-E_t\sum_{j\ge0}\rho^je_{t+j+1},\qquad E_t\sum\rho^je=\sum_{j=0}^{9}\rho^je_{t,t+j+1}+\frac{\rho^{10}}{1-\rho}\log\Big(1+\frac{g_t}{1-\psi}\Big).$$
  Revisions measured over the **I/B/E/S month** (third Thursday to third Thursday). Simple proxy: $FREV=(A1_{t+1}-A1_t)/B_t$ (earnings surprise $(E1-A1)/B$ in announcement months).
- **DR = r − μ − CF** (residual): "return innovation not explained by cash-flow news" — includes liquidity shocks, sentiment mispricing and CF measurement error (with opposite sign).
- Industries: 11 I/B/E/S sectors (FF17/FF48 give the same results).

## Main results

**Table 2 — decomposition (%/month, t-stats):**

| | $\pi$ | within-ind. $\pi^j$ | $\Omega_m$ | $\Omega_\mu$ | $\Omega_{CF}$ | $\Omega_{DR}$ |
|---|---|---|---|---|---|---|
| All months 1982–2009 | 0.53 (2.66) | 0.82 (5.49) | −0.30 (−4.15) | 0.00 (−0.34) | **−0.47 (−8.22)** | **1.29 (9.32)** |
| Non-January | 0.37 (1.79) | 0.67 (4.36) | −0.30 | 0.00 | −0.52 | 1.19 (8.29) |
| 1982–89 | 1.18 (4.74) | 1.32 | −0.14 | 0.00 | −0.58 | 1.90 (9.64) |
| 1990–99 | 0.12 (0.42) | 0.58 | −0.47 | 0.01 | −0.61 | 1.19 (6.10) |
| 2000–09 | 0.40 (0.90) | 0.65 (1.92) | −0.25 | −0.02 | −0.22 | 0.88 (2.94) |

**Table 3 — subsamples (top vs bottom 30%):** $\Omega_{DR}$ is positive and significant everywhere; larger in small (1.88) vs large (0.67, t 4.83), illiquid (2.22) vs liquid (0.63), value (1.54) vs growth (1.09), low (1.64) vs high coverage (0.81). The standard $\pi$ is significant only among small, illiquid, low-coverage (and value/growth) groups, e.g. large 0.29 (1.35), liquid 0.19 (0.80). The Jegadeesh–Titman (1995) decomposition confirms delayed reaction to common factors is not the driver.

**Table 4 — decile long-short portfolios (%/month):**

| Strategy | Raw | FF3 α | FF3+MOM+ST-reversal α |
|---|---|---|---|
| Standard (prior-month return deciles) | 0.67 (2.53) | 0.33 (1.37) | −0.19 (−0.85) |
| Within-industry return deciles | 1.20 (5.87) | 0.92 (5.11) | 0.46 (2.77) |
| **Within-industry DR deciles** | **1.57 (9.48)** | **1.34 (9.28)** | **0.91 (6.02)** |

Monthly Sharpe ratio (raw): 0.52 (DR) vs 0.14 (standard); FF3-adjusted 0.53 vs 0.08.

**Robustness (Table 5):** profit is 1.57% in month +1, 0.40% (t 2.51) in month +2, ≈0 afterwards; calendar-month returns: raw 1.74% (10.57), FF3 α 1.63% (10.29), 5-factor α 1.47% (12.96); mid-quote returns: raw 2.11%, FF3 α 1.97% (8.72), 5-factor 1.79%. **Non-parametric version:** 3×3 within-industry double sort on prior return and forecast revision, long losers with upward revisions / short winners with downward revisions: raw 1.86% (12.05), FF3 α 1.72% (12.24), 5-factor 1.11% (7.22); correlation 0.76 with the DR strategy and 0.80 with $\Omega_{DR}$. DR strategy significant in each of the 11 industries (t 3.81–6.45).

**Portfolio characteristics (Table 6):** decile 1: DR −18.07%, formation return −11.32%, **CF +5.51%**, next-month return 1.90%, FF3 α 0.66%; decile 10: DR +24.57%, return +16.75%, **CF −8.99%**, next-month 0.34%, α −0.67%. Expected-return spread tiny (1.24 vs 1.17). Extremes are smaller (≈\$1.6bn vs ≈\$3.5bn mid-deciles), less covered, higher IVOL and Amihud illiquidity. Portfolio turnover ≈90%/month; quoted spreads 46/43 bp ⇒ cost ≈ 46×0.902 + 43×0.908 = **80.5 bp/month**; cost-adjusted α ≈ **0.54%/month (t 3.9)**.

**Fama–MacBeth (Table 7, NW 12 lags):** industry-demeaned DR is the strongest predictor of next-month returns (negative, |t| > 7 in all specifications); once DR is included, prior return, industry-demeaned return and CF revision are insignificant. Industry-demeaned CF revision alone predicts positively (earnings momentum).

## Liquidity vs sentiment (Tables 8–9; FF3 + lagged state variables, NW 12 lags)
- **Long leg (buy DR losers):** loads positively on lagged detrended Amihud illiquidity (0.389, t 5.18) and lagged S&P 500 realized volatility (0.030, t 2.51); not on sentiment ⇒ compensation for liquidity provision (easier to provide liquidity as buyer). Correlation of smoothed long α with Amihud/RV: 0.24/0.23; with sentiment −0.10/−0.03.
- **Short leg (sell DR winners):** loads on lagged number of IPOs (t 3.02) and equity share in new issues $s$ (0.032, t 4.01) — Baker–Wurgler sentiment components; correlations 0.43/0.57 ⇒ overpricing that persists due to short-sale constraints (Miller 1977; Stambaugh–Yu–Yuan).
- Whole DR strategy also loads on lagged Amihud (t 3.28) and RV (t 2.02); FF ST-reversal factor only on Amihud (t 3.52). Pattern holds in all 10 characteristic subsamples; liquidity variables matter most for small, illiquid, high-dispersion stocks.

## Critical assessment
- **Convincing:** exact algebraic decomposition, strong and uniform $t$-stats across periods, industries, classifications, size/liquidity groups; the effect lives in large, analyst-covered stocks; a simple non-parametric double sort replicates it, so it does not hinge on the Da–Warachka model; the long/short asymmetry is a neat mechanism test.
- **Caveats:** (i) DR = return − μ − CF, so sorting on DR is mechanically **reversal plus CF momentum**: decile 1 combines negative returns *and* positive CF news; $\Omega_{DR}\approx\pi^j-\Omega_{CF}-\Omega_\mu$. Part of the "residual" alpha is earnings-revision momentum repackaged — the paper's own Table 5D (losers with up-revisions) makes this explicit. (ii) Factor premia use full-sample averages (mild look-ahead in μ, though $\Omega_\mu\approx0$). (iii) ≈90% monthly turnover; cost estimate uses quoted half-spreads only, no price impact — the cost-adjusted α of 0.54% is fragile for size. (iv) Standard reversal is insignificant after the 1980s and DR profits also shrink (0.88% in 2000–09 decomposition). (v) Sentiment/liquidity attribution rests on time-series loadings of lagged aggregates, with a modest sample (327 months). (vi) "Three times" vs "four times" inconsistency between abstract and text.

## Practical relevance for a quant PM
- Never trade raw 1-month reversal cross-industry: industry momentum (−0.30%/month) eats it. Run reversal **within industry** and **condition on fundamental news**: fade price moves unaccompanied by (or opposite to) analyst revisions; ride moves confirmed by revisions.
- Cheap implementation: residualize last month's return on industry and on the contemporaneous revision/surprise signal (or use the 3×3 return × FREV double sort); rebalance monthly, 1-month horizon only (month-2 profit ≈ 0.4%, then zero).
- Expect higher payoff when lagged illiquidity/volatility is high (long leg) and after IPO/issuance booms (short leg) — natural conditioning variables for leg sizing; costs and capacity must be modelled with realistic impact given ~90% turnover.

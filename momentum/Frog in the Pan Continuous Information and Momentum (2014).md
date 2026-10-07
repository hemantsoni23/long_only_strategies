# Frog in the Pan: Continuous Information and Momentum

**Zhi Da, Umit G. Gurun, Mitch Warachka · 2014 · Review of Financial Studies 27(7) (advance access Feb 2014, doi:10.1093/rfs/hhu003) · Source file `Finance/AbnormalReturnsMomentum_Da_2014.pdf` · Data: CRSP/Compustat US stocks with $5 price filter, 1927–2007 (subsamples from 1980/1982/1992 for characteristics, IBES, media); Dow Jones Newswire (Factiva), PR Newswire (2000–2007), 13F, TAQ order flow (1983–2004)**

## Claim
Investors, and analysts, underreact to information that arrives **continuously in small amounts** more than to the same cumulative news arriving in a few salient jumps. The "frog-in-the-pan" (FIP) mechanism is a *lower* attention threshold. Holding the 12-month formation return fixed, momentum is much stronger and more persistent when the return was built from many small same-signed days. It does not reverse in the long run, consistent with underreaction rather than overreaction.

## Model (Appendix A)
- $N$ i.i.d. signals $s^i\sim U[-L,L]$ arrive in period 1, and $P_2=s_1+s_2$ with $s_1=\sum_i s^i$.
- A fraction $m$ of CARA investors ignores signals with $|s^i|<k$ until period 2, which gives
$$P_1=s_1-m\sum_{i=1}^N s^i\,\mathbf 1\{|s^i|<k\}.$$
- Momentum comes from truncated small signals with the same sign as the formation return. Conditional on $s_1$, it rises with the frequency (and size) of small same-signed signals and with $k$ (less attention).
- In a simulation with $N=250$, corr(ID, continuation) is −0.65 for winners and −0.67 for losers, and ≈0 when PRET ≈ 0.

## Measures
- **Formation return:** $PRET$ = 12-month cumulative return skipping the most recent month (months $t-12$ to $t-2$).
- **Information discreteness:** with %pos and %neg the shares of positive and negative daily returns in the formation window,
$$ID=\text{sgn}(PRET)\times(\%neg-\%pos)\in[-1,1].$$
  Low (negative) ID means continuous information; high ID means discrete. ID = −1 if every day has the sign of PRET.
- **Variants:**
  - $ID_Z=\text{sgn}(PRET)(\%neg-\%pos)/(\%neg+\%pos)$ removes zero-return days (illiquidity).
  - $ID_{MAG}=-\frac1N\text{sgn}(PRET)\sum_i\text{sgn}(r_i)\,w_i$, with weights 5/15, 4/15, …, 1/15 on firm-specific |return| quintiles, so small days count more.
  - Market-adjusted ID gives similar results.
  - $ID_f=\text{sgn}(CUMREV)(\%down-\%up)$ uses monthly analyst EPS revisions.
- **Properties:** mean −0.035, SD 0.054. Annual autocorrelation is only **0.033**, vs IVOL 0.843, UCG 0.668, CGO 0.681, so ID is a time-varying flow rather than a firm trait. Correlations: ID with PRET 0.167, with |PRET| −0.332, with RC −0.307. Firm characteristics explain only 14.1% of its cross-sectional variance.
- **Salience check (2000–2007 FM regression of ID):** high ID goes with rising turnover (0.31, t = 4.8), more media articles (t = 2.9), more press releases (t = 3.1) and larger |SUE| (t = 8.5). Change in analyst coverage is insignificant.

## Main results: 6-month winner−loser returns (Table 2, post-1927)
Sequential sort: PRET quintiles first, then ID quintiles within each.

| ID quintile | Discrete | 2 | 3 | 4 | Continuous | Cont.−Disc. |
|---|---|---|---|---|---|---|
| Raw 6-month WML | −2.07% | 0.64% | 3.12% | 4.36% | **5.94%** | **8.01% (t = 8.54)** |
| FF3 α | −2.01% | 3.53% | 5.05% | 6.71% | 8.77% | 10.78% (t = 10.55) |

**Robustness of the continuous − discrete spread:**

| Variant | Spread | t |
|---|---|---|
| Post-1980, sequential | 6.74% | 5.41 |
| Independent double sort (post-1927) | 6.35% (discrete −0.63% → continuous 5.72%) | 4.48 |
| $ID_Z$ | 4.75% (FF3 5.66%) | 4.11 (FF3 5.85) |
| $ID_{MAG}$ | 9.62% | 6.02 |
| $ID_{MAG}$ with steeper weights | 11.05% | – |
| **3-year horizon** | continuous +5.39% (t = 2.23) vs discrete −8.48% (t = −2.08); spread 13.88% | 2.49 |

- The 3-year result is the no-reversal finding: continuous-information momentum does not revert.
- **Monthly decay** (FF3, non-cumulative): continuous momentum lasts about 8 months (month 8: 0.46%, t = 2.08; month 9: 0.21%, t = 0.97). Discrete momentum is insignificant by month 3 (0.31%, t = 1.30).

## Attention tests (Table 3: continuous − discrete gap by subset)

| Split (bottom/top 30%, or median) | Low-attention subset | High-attention subset | Difference (t) |
|---|---|---|---|
| Institutional ownership | 8.79% | 5.48% | 3.31% (2.41) |
| IO concentration (dispersed vs concentrated) | 11.23% | 5.44% | 5.79% (2.41) |
| Size (small vs large) | 7.17% | 4.92% | 2.25% (2.18) |
| Analyst coverage | 6.83% | 3.41% | 3.42% (2.24) |
| Media coverage (≤3 vs ≥4 articles/quarter) | 5.89% | 3.75% | FF3: 5.94% vs 1.96%, diff 3.98% (2.09) |

**Time series, 1992–2007.** FF3-adjusted returns of the continuous-information momentum strategy load positively on log(number of listed stocks), coefficient 22.5 (t = 3.86), and negatively on log(media coverage), −5.17 (t = −2.66). Aggregate UCG, aggregate RC, the market return and a time trend are insignificant; there is no decay over the sample.

## Distinguishing from alternatives
- **Disposition effect (Grinblatt–Moskowitz return consistency RC; UCG; Frazzini CGO):**
  - Signed PosID and NegID predict continuation for both winners and losers (post-1927: 0.063, t = 2.01; −0.130, t = −9.60). RC fails for losers.
  - The FIP effect survives within the RC = 1 subset (17% of observations).
  - Order-flow imbalances after continuous information are positive for winners and negative for losers, the opposite of disposition selling.
  - Analysts, who have no reference prices, also underreact.
- **Conservatism:** momentum after *confirming* continuous information (8.02%) exceeds that after disconfirming (5.14%). This is the opposite of what conservatism predicts.
- **IVOL (Zhang 2006):** after orthogonalising IVOL to |PRET|, the high−low residual-IVOL momentum spread is 0.02% (t = 0.25). IVOL's apparent effect is mechanical.
- **Fama–MacBeth of 6-month returns** on PRET, ID, PRET×ID plus 13 controls and their PRET interactions (RC, UCG, CGO, SUE, BM, SIZE, TURN, IVOL, COV, Amihud, price delay D, MAX, CSKEW):
  - PRET×ID coefficient: −0.063 (t = −3.17) post-1927 and −0.212 (t = −4.65) post-1980.
  - With all controls and interactions: −0.270 (t = −8.39).
  - For winners, the economic effect of a 1-SD ID move exceeds the effects of RC (18% of ID's), UCG (41%), size, turnover, IVOL and coverage. BM is larger for losers.
  - Using $ID_{MAG}$: −0.112 (t = −7.27) and −0.265 (t = −5.94).
- **Residual ID** (ID orthogonalised to |PRET|, RC, BM, size, turnover, IVOL, coverage, IO; adj. R² 0.141): momentum rises from 0.98% to 6.73%, spread 5.75% (t = 4.86). The 3-year spread is 16.30% (t = 2.08).
- **Analysts:** in regressions of SURP on ID×PRET the interaction is −0.0028 (t = −2.19), so forecast errors are larger after continuous information. Sorting on $ID_f$ gives a continuous − discrete gap of **10.93%** (t = 11.02; FF3 10.13%), and momentum after discrete revisions is insignificant.

## Critical assessment
- **Convincing:**
  - Large, monotone and robust conditional effect: sequential and independent sorts, many controls, residual ID, a revision-based ID independent of daily-return noise, and no long-run reversal.
  - ID's low persistence argues against it being a proxy for a static firm trait.
- **Caveats:**
  - ID ignores magnitudes. Paths such as {2,2,2,2,2,2} and {1,1,1,1,1,7} share ID = −1. $ID_{MAG}$ helps only marginally.
  - Low ID is mechanically associated with lower realized path volatility for a given PRET. It overlaps with "smooth"/low-vol momentum and residual-momentum ideas, which the paper controls for only via IVOL and MAX.
  - The media and attention proxies are endogenous, and the salience regressions have R² ≈ 0.5–0.8%.
  - Most attention-split differences are only marginally significant (t ≈ 2.1–2.4).
  - Returns are 6-month buy-and-hold on quintile-within-quintile portfolios (thin corners), and sample ends 2007. There are no transaction costs, no value-weighted results in the main table, and no evidence on the 2009 momentum crash.
  - The sequential-sort spread (8.01%) is partly driven by the *discrete* winners−losers leg being negative (−2.07%). Losers with discrete information outperform winners.

## Practical relevance for a quant PM
- **Cheap, orthogonal momentum conditioner:** needs only daily return signs over the 12-2 window.
  - Implement as a double sort (PRET then ID), or add $-\text{PRET}\times ID$ (or $ID_{MAG}$) to a momentum score.
  - Prefer smooth winners and smooth losers; avoid jump-driven winners.
  - Continuous-information momentum lasts about 8 months, which permits slower rebalancing and lower turnover.
- **Where the effect is largest:** neglected names (low/dispersed IO, small, low analyst and media coverage). Check capacity and costs there.
- **Analyst revisions:** the $ID_f$ version works on analyst revision paths too. It suggests conditioning earnings-revision momentum on revision smoothness.
- **Relation to other signals:** closely related to later "smooth momentum", path-dependent momentum and residual momentum. Test for overlap before stacking them.

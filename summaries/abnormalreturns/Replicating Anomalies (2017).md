# Replicating Anomalies
**Authors:** Kewei Hou, Chen Xue, Lu Zhang
**Year:** 2017
**Journal/Venue:** Review of Financial Studies (working paper 2017; published 2020. The PDF is the accepted version, editorial decision Oct 2018)
**Source file:** Finance/AbnormalReturnsReview_HouXueZhang_2017.pdf

## Question and setup

This is a large-scale "scientific replication" (in Hamermesh's sense: same population, similar but not identical methods) of 452 published anomalies, split into momentum 57, value-vs-growth 69, investment 38, profitability 79, intangibles 103 and trading frictions 106. The authors follow the original variable definitions and apply one common protocol. Monthly-sorted signals are evaluated at 1-, 6- and 12-month holding horizons (overlapping Jegadeesh-Titman subportfolios), which is why the count reaches 452.

- **Data:** CRSP/Compustat, Jan 1967-Dec 2016. Financials and negative-book-equity firms are excluded, and there is no price screen, so microcaps stay in the sample. Annual sorts use end-of-June formation with fiscal year $t-1$ data. Quarterly earnings are used after the announcement date (RDQ); other quarterly items get a 4-month lag. Delisting returns are handled per Beaver-McNichols-Price.
- **Procedures:** decile sorts with {NYSE, All (NYSE-Amex-NASDAQ)} breakpoints × {VW, EW} returns; univariate Fama-MacBeth regressions by OLS and by WLS with market-equity weights. Regressors are winsorized 1-99%, demeaned and scaled by their cross-sectional s.d. Newey-West t-stats throughout.
- **Replication success:** $|t| \ge 1.96$ for the high-minus-low decile under **NYSE-VW** (or the FM-WLS slope). Multiple-testing hurdles are 2.78 and 3.39, Harvey-Liu-Zhu's BHY cutoffs at 5% and 1% FDR. The authors call these heuristic and conservative: applying BHY directly to their 452 tests gives 3.47 and 4.27.

**Regression slope as a portfolio.** With $X_t = [\mathbf 1, C_t]$ and $M_t = \mathrm{diag}(ME_{it})$,

$$B_t = (X_t' M_t X_t)^{-1} X_t' M_t R_{t+1}, \qquad W_t = M_t X_t (X_t' M_t X_t)^{-1},$$

so $W_t' X_t = I$. The slope is the return on a zero-investment portfolio with unit characteristic spread and zero net exposure to the intercept. Its legs do not sum to ±1, so slope magnitudes are not comparable to decile spreads. OLS ($M_t = I$) acts like an All-EW sort, but it overweights microcaps even more because the least-squares fit leans on extreme-characteristic, volatile-return outliers. Univariate specifications are chosen deliberately, to avoid specification search over regressor sets (Leamer).

## Why microcaps matter (Tables 1-2)

Microcaps (below the NYSE 20th ME percentile) average 2,365 of 3,896 firms (60.7%) but 3.21% of market cap. They have the highest EW return (1.27%/mo vs. 1.01% for big stocks) and the largest cross-sectional return dispersion (19.3% vs. 8.8% for big). They also have the widest dispersion in most anomaly variables. The microcap share peaked at 71.6% of firms in 1987 and fell to 50.1% (1.6% of cap) by 2016; at the end of 2016 the NYSE 20th percentile was $724M.

Weights and **investment capacity**, $\min_i ME_i/|w_i|$ (EW: $n \cdot \min_i ME_i$; VW: $\sum_i ME_i$):
- Momentum low decile: 8% microcap weight under NYSE-VW vs. 63.9% under All-EW. Capacity is 5.95% of market cap (~$1.2T at end-2016) vs. 0.02% (~$1.19B).
- Value high decile: 7.4% vs. 64.2% microcap weight; capacity $900B vs. $1.19B.
- Regressions: the investment short leg has 3.6% microcap weight under WLS vs. 62.1% under OLS, with capacity 9.03% vs. 0.02% of market cap.

## Headline results (Figure 2, extended sample)

| Procedure | $\lvert t\rvert\ge1.96$ | $\lvert t\rvert\ge2.78$ |
|---|---|---|
| NYSE-VW | 35.0% (158/452) | 17.9% |
| NYSE-EW | 56.4% | 46.7% |
| All-VW | 40.7% | 22.1% |
| All-EW | 58.6% | 48.0% |
| FM-WLS | 33.6% | 13.3% |
| FM-OLS | 58.2% | 48.5% |

- The failure rate is 65% under NYSE-VW and 82% at 2.78. Equal-weighting, not the choice of breakpoints, is the main channel for microcap inflation (All-VW 40.7% vs. NYSE-EW 56.4%).
- Even with maximal microcap weight, the multiple-testing failure rate is about 52%, so the "replication crisis" is not only a microcap story.
- Dropping microcaps entirely from VW returns (after NYSE breakpoints) cuts the success rate to 30.5% for sorts and 27.2% for regressions.
- **Not a post-sample decay effect:** on each anomaly's original sample the NYSE-VW rate is 34.7% (65.3% failure). All-EW fails 43.1% at 1.96 and 56.2% at 2.78. Between samples, 22 anomalies lose significance and 33 gain it.

**By category (NYSE-VW, single / multiple test):** momentum 63.2% / 49.1%; value-growth 42% / 10.1%; investment 73.7% / 50%; profitability 44.3% / 17.7%; intangibles 25.2% / 10.7%; trading frictions 3.8% / 1.9% (102 of 106 fail). Under All-EW, frictions still replicate at only 39.6%, and at 41.5% even in a microcap-only universe. Microcaps revive short-term reversal, turnover, dollar volume, Amihud and zero-trading-days, but not PIN, the Pástor-Stambaugh or Acharya-Pedersen liquidity betas, idiosyncratic volatility, the high-low spread or the intermediary leverage beta.

## Selected individual anomalies (NYSE-VW, monthly spreads)

- **Momentum:** R6 with 6-month holding 0.82% (t=3.5) vs. 1.1% in JT (1993). JT's number is reproduced with All-EW in their sample (1.18%), but that estimate falls to 0.70% in the extended sample. Sue1/6/12: 0.46% (t=3.48), 0.16%, 0.08%, versus CJL's ~1.13%/mo at 6 months. Customer momentum 0.78% vs. 1.58% originally; the gap comes mostly from the original $5 price screen.
- **Value:** Bm 0.54% (t=2.61), vs. 1.41% in Rosenberg-Reid-Lanstein's short sample. Monthly-updated ratios are stronger (Epq 0.93%, t=4.94), consistent with Asness-Frazzini. Five-year sales growth fails (-0.19%, t=-1.08), as does La Porta's Ltg (0.13%). IBES back-revisions may matter for the latter.
- **Investment/accruals:** I/A -0.44% (t=-2.89) vs. CGS's -1.05% (VW) and -1.73% (EW). Operating accruals -0.27% vs. Sloan's -0.87%. Total accruals fail (-0.22%). The original size-adjusted EW returns mixed VW size benchmarks, an internal inconsistency.
- **Profitability:** Roe 0.68% at 1 month (t=3.12), fading by 12 months. Gross profits-to-lagged-assets 0.16% (t=1.04) vs. GP/current assets 0.38%. Because $Gpa = Gla/(\text{asset growth})$, the gross-profitability premium is argued to be largely the investment premium. FF (2015) operating profitability Ope fails (0.27%, t=1.34). Piotroski F fails (0.29%). Distress fails: failure probability -0.39% (t=-1.35), and it was positive in 1976-80 before CHS's sample. O- and Z-scores are null.
- **Intangibles:** G-index 0.02% over 1990-2006; GIM's result is reproduced in-sample and reverses in 2000-06. Accrual quality and most Francis et al. earnings attributes are null, but earnings predictability (-0.53%) and timeliness (0.34%) survive. Analyst dispersion is null under VW; it is -0.69% under All-EW, so the effect is driven by microcaps.
- **Frictions:** 15 of 16 volatility measures are insignificant, and All-EW is even weaker, so microcaps do not rescue low-vol. Ivff 1-month -0.52% (t=-1.71) vs. Ang et al.'s -1.06%; the All-VW procedure does reproduce ~-1.2%, which shows the effect hinges on NASDAQ-inclusive breakpoints. Short-term reversal -0.27% (t=-1.4) vs. -2.57% under All-EW. Max daily return, PIN, Amihud (except at 12 months in WLS) and the intermediary leverage beta all fail.

**Commonality (Table 4).** Among the 158 survivors, within-category correlations are high (value: 0.44 rank, 0.60 return) and cross-category correlations low. PC1 explains 25.9% of variance across all 158 long-short returns, and 4/6/8 PCs explain 56%/64%/68%. Intangibles are diffuse: PC1 explains 21% within the category.

## Assessment

- **Convincing:** a uniform, documented protocol across 452 signals. Showing that replication rates are nearly identical on the original samples rules out "anomalies decayed after publication" as the main explanation, and points instead to construction and weighting. The capacity calculation turns "microcaps" from a rhetorical point into a quantitative one.
- **Contestable:** NYSE-VW decile spreads are low-power for signals whose premium sits in small/mid caps. Value-weighting deciles concentrates the portfolio in a few megacaps, so failing to reject is not the same as a zero premium; Jensen-Kelly-Pedersen later argue Bayesian shrinkage recovers much higher replication rates. The 452 count includes 1/6/12-month variants of the same signal, which are highly dependent, so both the "65%" and the FDR cutoffs should be read loosely. Univariate tests ignore that weak signals can matter in combination. Some failures stem from judgment calls, e.g. the 4-month lag vs. 3 in Thomas-Zhang, or no $5 screen. The authors also co-authored the q-factor model, and the conclusion that fundamentals (investment, profitability) matter more than frictions aligns with that model.
- **Practical use:** a default hygiene standard for signal research. Report NYSE-breakpoint VW spreads and ME-weighted FM slopes alongside EW. Compute capacity. Treat $|t|<3$ on a published univariate anomaly with suspicion. Expect realized spreads roughly half of the originally reported ones (I/A, accruals, Sue, momentum). Friction and volatility signals are the least robust category in large-cap, investable form.

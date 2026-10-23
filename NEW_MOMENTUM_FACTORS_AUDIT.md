# Audit of `NEW_MOMENTUM_FACTORS_AND_IDEAS.md` — research before implementation

**Date:** 2026-10-20 · **Gates fixed beforehand:** `factor_research/NEW_MOMENTUM_AUDIT_PREREG.md` · **Code:** `factor_research/stage24_new_factor_audit.py`, `stage24b_quiet_placebo.py` · **Outputs:** `factor_research/results/stage24_*.csv`
Nothing in `Old_live_strategies/` was touched. No strategy was built. Same proxy book as stages 2/3 (top-15, monthly, equal weight, 0.3%/side, no stops), so book numbers are *relative* evidence only.

## 1. Verdict in one paragraph
**Do not implement any of the seven blueprints as written.** Five of seven had already been tested and cut in earlier work (several on your real engines). The two that were not (Quiet Momentum, Asymmetric Beta) fail or add nothing once compared with the proper controls. The headline IC / ICIR / t numbers are *reproducible* (they match the old 111-factor catalog) but they do not translate into books, and the "improved" versions do not beat their plain controls. The document's literature claims are also partly wrong (two cited papers are not in `momentum/`; two papers say the opposite of what is attributed to them). Nothing here is certain: this is one survivorship-biased 2003-2026 panel with ~125 factor variants examined.

## 2. Was it already tested? (map to the prior record)
| Blueprint | Prior record | Status |
|---|---|---|
| 1 Quiet momentum | `volume surge`, `vol-confirmation` rejected (FINDINGS §2, §4); inverse-volume framing **not** previously isolated | new, tested here → §4.1 |
| 2 Asymmetric beta | `high_beta`, `up_capture`, `down_resilience`, `low_beta` scanned (reversed / weak / book Sharpe ≈ 0); Δβ itself new | new, tested here → §4.2 |
| 3 Intraday vs overnight | in catalog since 2026-10-05 (`intra_over_*`, t≈5.4); I4 book cut (ΔSharpe +0.02); **real engines: Elendel/Zenith −0.22 to +0.03 Sharpe, only Quad 301-1000 +0.19** (MASTER_RANKING §C) | already cut |
| 4 SUE / PEAD | stage15 / `csm_pead`: IC real, top-15 book no better; PEAD book = market beta, "not recommended". Option B (OHLCV jump proxy): `event_ret_63` reversed; re-tested here → negative sign | already cut |
| 5 Factor momentum | stage17: IC 0.05-0.07 but book Sharpe 0.48-0.72 vs 0.80 plain Elendel | already cut |
| 6 Ulcer momentum | low-ulcer add-on cut on real engines (Elendel −0.26 Sharpe, −6.3 pt CAGR, P=0.00); I3/I4 optional/cut | already cut |
| 7 Convexity / acceleration | `mom_accel` IC −0.010 (t −1.4); bake-off "rejected"; re-tested with a true quadratic fit → ~0 | already cut |

## 3. Is the evaluation harness trustworthy?
* **Mislabelled baseline (H2).** The runner's `corr_elendel` / `inc_ic` use `q5_126` alone, not Elendel (A3+Q5). Against the true Elendel/Zenith the numbers move (e.g. `intra_over_252` corr 0.17 → 0.20/0.32; incremental IC 0.036 → 0.031/0.023). The guide's own hurdle "incremental NW-t > 2" is never computed by the runner; I computed it.
* **Long-horizon t-stats are unreliable.** Calibration with a persistent placebo factor (200 draws, rank-AR(1) 0.9): NW-t has SD ≈ 1.17 (not 1); P(|t|≥3) ≈ 1-2% instead of 0.3%. Worse for fast-moving factors: runner reports `trend_accel_63` 12m **t = 6.04** (U1); on non-overlapping samples it is **1.38**. Use 3m t-stats, treat 6-12m NW-t as an upper bound.
* **IC ≠ book, again.** Same-IC factors give very different books: `intra_over_252` IC₃ 0.060 → U2 top-15 holdout Sharpe 0.41 vs `mom_12_1` 0.49; top-quintile excess 0.5%/3m vs 1.9% for Q5. The low-vol/ulcer/tight family has *negative* top-quintile excess at 6-12m while IC is positive: the IC lives in avoiding junk, not picking winners.
* **Document's own "expected correlation" column is a guess, not a measurement** (e.g. convexity 0.60-0.70 stated; measured −0.02 to 0.38). Ulcer stated 0.55-0.65, measured 0.58 (ok). Δβ stated 0.50-0.60, measured 0.15/0.07. "`low_ulcer_252` t = 5.5 at 12m" is the *3m* t; the 12m NW-t is 3.1 (U2) / 3.5 (U1). The "−36.9% vs −66.8% drawdown" comes from stripped proxy books that FINDINGS §6 says are not comparable with live engines (not re-verified).
* Survivorship (98 of 5,205 files end before mid-2026) flatters smooth/low-risk screens most.

## 4. Per-blueprint findings (U2 = the pool the live books rank; gates from the pre-registration)
Gate key: G1 signal (3m NW-t ≥ 3, both halves +, holdout t ≥ 2) · G2 increment vs TRUE Elendel and Zenith (t ≥ 2) · G3 beats plain control (|t| ≥ 2) · G4 top-decile excess >0, t ≥ 2, both halves · G5 add-on book beats un-tilted base in discovery AND holdout at both weights.

| Factor | IC₃ (t) | hold t | G1 | G2 (Elen / Zen t) | G3 vs control (t) | G4 | G5 | Verdict |
|---|---|---|---|---|---|---|---|---|
| quiet_mom_12_1 | 0.033 (3.1) | 2.1 | pass (barely) | 0.2 / −0.3 **fail** | +0.002 (0.95) **fail** | pass | w=0.5 pass, w=1.0 fail → **fail** | no |
| delta_beta_252 | 0.006 (0.8) | 0.1 | **fail** | fail | blend vs mom_12_1: **−0.013 (t −2.1)** | fail | fail | no |
| intra_over_252 | 0.047 (4.4) | 2.4 | pass | 3.1 / 2.5 pass | +0.014 (0.85) **fail** | **fail** (hold −0.8%) | **fail** (hold Sharpe −0.34 on Elendel) | no |
| intra_over_126 | 0.037 (4.0) | 2.3 | pass | 2.1 / 1.6 fail | fail | fail | fail | no |
| ulcer_mom_252 | 0.053 (4.8) | 2.8 | pass | 1.8 / 0.5 **fail** | +0.018 (3.7) pass | fail | fail | no (≈ vol-scaled momentum, already live) |
| low_ulcer_252 | 0.072 (5.1) | 2.9 | pass | 3.7 / 2.9 pass | – | fail | fail | no (already cut on real engines) |
| trend_accel_63 / quad_gamma_126 | 0.001 / −0.003 | – | **fail** | fail | – | fail | fail | no |
| convex_mom (β·R² + γ) | 0.020 (2.3) | 0.3 | fail | fail | −0.009 (−1.1) | pass | fail | no (= velocity momentum) |
| jump_react_126 (PEAD proxy) | **−0.039 (−2.9)** | −2.5 | wrong sign | negative | – | negative | fail | no (reversed) |

### 4.1 Quiet momentum — the closest call, and why it still fails
* Rank correlation with plain 12-1 momentum is **0.96**; with the true Elendel 0.48. It is momentum with a mild volume tilt, not a new signal. IC gain over plain momentum: +0.002 (t 0.95).
* **Literature mismatch.** Lee-Swaminathan's volume variable is *formation-window turnover* (shares traded / shares outstanding), not a 21d/252d volume surge. In their own Table II the first-year volume effect among *winners* is −0.12%/mo (t −0.67), insignificant; the large effect is on the *loser* side (high-volume losers keep losing), which a long-only book cannot use; the benefit for low-volume winners shows up in years 2-3. My 12-1 × volume-tercile sort (H6) agrees: among winners, low-volume minus high-volume is ≈ 0 for both surge definitions in U1 and U2 (3m: −0.15%, t −0.35 and +0.16%, t 0.22). The only volume variable with a spread is the dollar-volume *level* (low-liquidity winners better, U1 3m +1.7%, t 2.1): that is the known "ranks 301-1000 beat the megacaps" liquidity-tier effect, not a life-cycle effect. True turnover needs shares outstanding, which the OHLCV files lack.
* **Book.** As a 0.5-weight add-on it lifts proxy Sharpe on both bases (Elendel 0.81 → 0.96; Zenith 0.77 → 0.91), better than plain 12-1 momentum — but at w=1.0 holdout turns negative on Elendel (−0.05), and **vs a placebo (volume term randomly permuted within month, 60 draws) the gain is significant in the discovery period only (p≈0.00) and not in the holdout (p = 0.2-0.5)**. Standalone, it is no better than `mom_12_1_sharpe` (already in csm_batch): Sharpe 0.70/0.49 hold vs 0.72/0.59.
* Conclusion: a re-parameterised momentum signal whose volume information fades after 2014. Not worth a build.

### 4.2 Asymmetric beta — the cited papers point the other way
* Ang-Chen-Xing (in `momentum/`): stocks with **high** downside beta earn **higher** returns (≈6%/yr, contemporaneous); high β⁺−β⁻ earns **less** (Q5−Q1 −7.8%/yr). The investable version is weak: sort on past β⁻ gives +0.11%/mo (t 0.6) unless the top-volatility quintile is dropped; relative β⁻ has 12-month persistence of only **0.08**. Chabi-Yo-Ruenzi-Weigert and Ruenzi-Weigert (also in the folder) find crash sensitivity is *compensated*. "Lu & Murray (2018)" is not in the folder.
* Data: U2 IC₃ 0.006 (t 0.8); a signal only appears in U1/U3 (0.03-0.04), where it is partly a trend/market-state proxy and vanishes inside the SMA200 pool. The doc's own blend (12-1 + λ·Δβ) is **worse** than plain 12-1 (IC −0.013, t −2.1).

### 4.3 Intraday vs overnight — a possible data artefact, not an institutional-flow signal
* The doc credits Lou-Polk-Skouras (2019); that paper is **not in `momentum/`** (my search of the folder: no file mentions "overnight"). Its abstract (web) says momentum profits accrue *overnight* and intraday is the offsetting leg, with components that persist for years and reverse across periods. Our factor bets on the *opposite* tilt (fade overnight, own intraday).
* H5 cross-persistence (3m): past overnight → future overnight **+0.40** (t 42) and → future intraday −0.31; past intraday → future intraday +0.29 and → future overnight −0.32. ICs this large are not ordinary return predictability. Sanity check on the data: the average stock shows **+50% (top-300) to +130% (illiquid) annualised overnight return and −25% to −120% intraday**, with a cross-stock correlation of **−0.8** between the two. That is a persistent stock-specific offset between open and close prints. **Follow-up (confirmed, 2026-10-20): the `open` field is not a usable opening price.** NIFTYBEES (a Nifty tracker) shows **+174%/yr "overnight" and −163%/yr "intraday"** (total +10.5%, which is right); BANKBEES +81/−71, JUNIORBEES +215/−202. Its open sits at 76% of the day's range on average, is above the prior close on 79% of days (mean gap +1.16%), and same-day overnight vs intraday correlate at −0.93. The offset is present in every era (top-300 stocks: +100/−90 in 2005-09, ≈+50/−50 since 2010) and open is almost never outside [L,H] (5e-7). So the overnight/intraday split measures a data-construction offset, not investor behaviour, and Blueprint 3 (plus the earlier `intra_over_*`, `overnight_*`, `event_gap_*`, `gapup_freq_*` catalog results and the I4 sleeve) should be treated as untrustworthy. Cause not identified (my guess: vendor candle construction or the NSE closing-VWAP convention). **Open question for you: do any backtests fill at the next day's OPEN?** If so that fill price is affected too.
* Net payoff is modest and defensive: corr with low-vol 0.34, low-beta 0.33, low-ulcer 0.35, down-resilience 0.33, momentum 0.11. IC is similar to undecomposed total return (G3 fail). Pre/post NSE pre-open auction (Oct 2010) IC is stable (U2 0.058 → 0.043), but 2019-26 U2 is 0.034 (t 1.8). Book: adding it to Elendel/Zenith cuts holdout Sharpe by 0.07-0.39.

### 4.4 Convexity / acceleration
The cited "Unpacking Price Momentum: The Need for Speed" is a Nomura note on **rebalance timing** (quarterly vs monthly vs mid-month), not on curvature; there is no source for the idea in the folder. Implementation in the runner is a slope-difference, not the quadratic fit the doc describes; I tested both. True OLS γ: IC −0.003, positive in only 42% of years, fails every gate; the lone positive 12m result in the runner is a Newey-West artefact (§3).

## 5. Literature claims vs sources
| Doc claim | Source check |
|---|---|
| LS2000: momentum "pronounced and persistent among low-volume winners" | partly: the paper's early-stage effect is real but is mostly years 2-3 and the short side; yr-1 winner V1−V3 −0.12%/mo, t −0.67; volume = turnover, not surge |
| Novy-Marx: SUE\|r₂,₁₂ vol 5.1%, skew +0.46 | accurate, but long-short US factor stats; our stage15 found no top-15 book gain |
| Ang et al.: "want β⁺>1, β⁻<0.5" | opposite sign in the paper (downside beta is rewarded; β⁺−β⁻ earns less) |
| Lu & Murray 2018, Lou-Polk-Skouras 2019, Chen-Jegadeesh-Wermers, Heston-Sadka, Barroso-Santa-Clara, Arnott et al., Chordia-Shivakumar | not stand-alone files in `momentum/` (the folder has 61 files incl. duplicates). Real papers exist for some, but they were not read here |
| "Need for Speed (2009)" supports curvature | it is about rebalance timing |
| Ehsani-Linnainmaa factor Sharpe >1.3 | one column of their table shows 1.33; our market-specific test (stage17) did not reproduce a book gain |

## 6. What this does and does not tell you
* Does: reproduces the runner's numbers, shows why each fails a book-level or control test, and corrects the sources.
* Does not: test on real engines (only proxy books); correct survivorship; verify the open-price hypothesis; test SUE with a fresh fundamentals feed (still the gating dependency per MASTER_RANKING).
* ~125 variants have now been examined on this panel; the pre-registered gates were met by none of the seven.

## 7. If you want to keep researching (not building)
1. ~~Open-price integrity check~~ **done, see §4.3 follow-up (open field unusable).** Still worth finding the cause (second-source comparison of ~20 symbols, needs external data).
2. **True Lee-Swaminathan turnover**: feasible (`shares_out` in `pit_harness/cache/facts_quarterly.parquet`, 98% populated, 2018-2026, plausible 0.07-0.5%/day for large caps) but 728 share-count jumps (splits/bonuses) vs volume adjustment must be handled, ~70 monthly signals only, and the paper's own long-only gain sits in years 2-3. Not run: low power, high unit-mismatch risk (cf. the E/P share-unit bug in MASTER_RANKING).
3. ~~Fix the runner~~ **done**: `evaluate_new_momentum_factors.py` now uses the true Elendel (A3+Q5-126) as baseline and carries the caveats at the top; results CSVs regenerated. Incremental NW-t and non-overlapping t remain in `stage24_new_factor_audit.py`.
4. Items MASTER_RANKING already ranks higher: residual-momentum tilt (built), cash sweep, Zenith 301-1000 universe, refreshed quarterly-results feed.

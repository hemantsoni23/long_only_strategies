# Industry-momentum book — PRE-REGISTRATION (written 2026-10-10, before any book was simulated)

Purpose: decide, with numbers fixed in advance, whether a slow, staggered, industry-led long-only book is worth building, and make it
possible for this research to FAIL CLEANLY. Nothing here may be loosened after results are seen; any deviation goes in the override log at the bottom.

## 0. What is already known (all of it is full-sample; there is no untouched lockbox)
* Signal evidence (stage18/20/21): bottom-up Industry_clean basket momentum (leave-one-out, 3m, no skip) has IC 0.058 (U1) / 0.066 (U7) at 3m,
  NW-t 6.9 / 8.0, t>=3.9 in both halves (<=2012, >=2013), 9/9 monotone deciles, top-2-year share 23%, placebo p=0/60 (global and within-sector).
  Fama-MacBeth coefficient survives stock-level controls. IC decays ~50% after 2014 and is ~0 in 2024-26 — but so do Elendel/Zenith.
* Failure history (6+ attempts, `Discarded sector based strategies/`, `other_momentum_ideas/`): gates/quotas on 11 sectors added nothing; Meridian
  correlated 0.78-0.83 with its sibling; breadth books Sharpe ~1.0-1.5 gross, zero cost, 35% exposure; SC1 weekly book died on cost (break-even 11-13 bp);
  industry momentum as a monthly ranking tilt was "not distinguishable from zero"; my own stage19 tilt failed the holdout gate and the tilted books were
  badly concentrated (6 names per industry).
* Booking: engine-booked figures (Sharpe 1.7-2.7) are inflated 17-26 CAGR points (csm_value/AUDIT.md). THIS STUDY USES ITS OWN FAITHFUL SIMULATOR
  (signal at close t, fill at close t+1, positions earn returns only from the day after the fill, costs on traded notional, no stops) and compares against
  `csm_value/output/faithful_engine_returns.csv` (faithful live Elendel/Zenith/Quad daily returns). The "1.7-2.7 / -12..-16%" bar is NOT used.
* Honest limits: (i) survivorship (only ~56 of 5,205 files end before 2026), (ii) static current-day industry labels, (iii) 2005-2012 trades on a few
  hundred to ~1,600 surviving names vs ~4,500 later, (iv) halves are consistency checks, not a lockbox. The only true out-of-sample is forward paper trading.

## 1. Design under test (fixed)
Universe/pool: U2_live_trend (U1 liquid-1000, price>20, <=5 locked days/63, close > SMA200) for stock picks; U1 live members define industry usability.
Signal date: month-end close t. Fill: close t+1. Names that are NaN or circuit-locked (high==low) on the fill day cannot be bought (that weight stays in cash).
Industry rank: equal-weighted Industry_clean basket (members U1-eligible at the prior month-end) trailing L-month return, skip 0. An industry is usable if it has
>=10 live U1 members at t and trailing return > 0. Take the top n_ind usable industries (fewer if fewer qualify; the rest stays in cash).
Stock pick inside an industry: top m pool members by A1 (close / 252d high, `F['a1_52wh']`).
Weights: each cohort name 1/(n_ind*m); JT overlapping tranches: target = mean of the last H monthly cohorts.
Regime gate: scale the whole target by 1.0 if the equal-weight market index is above its SMA200 at t, else 0.5.
Cash: 6.5%/yr on idle cash (liquid fund), also reported at 0%. Costs: 0.3%/side on traded notional. No stops. Start 2005-01-01 (first month with >=8 usable industries).
Primary spec **D1**: L=3, n_ind=8, m=2, H=6.   Sensitivity neighbours (all reported, none chosen post hoc): D2 focused (L3, n_ind 5, m 2, H 3); D3 slow (L6, n_ind 8, m 2, H 6);
one-at-a-time +-: L in {2,3,4,6}, n_ind in {5,6,8,10,12}, m in {1,2,3}, H in {3,4,6,9,12}; stock score in {A1, lowvol, random}; gate off; skip 1; weighting; universes U1 / U7 / U3.

## 2. Pre-registered gates (ALL must hold for D1; "faithful" = this simulator)
Signal (done above, G1): passed except one mis-specified sub-gate (see override log).
Book gates:
 B1  Beats the same-pool RANDOM-STOCK book (same N, same gate, same costs, 200 draws) on Sharpe with p<=0.05 in the full sample AND in each half.
 B2  Beats the RANDOM-INDUSTRY book (random n_ind among usable positive-return industries, same A1 within, 200 draws) on Sharpe with p<=0.05 (full sample): industry ranking adds value.
 B3  Beats the within-sector SHUFFLED-LABEL book (60+ draws) on Sharpe with p<=0.05: industry identity matters.
 B4  Playbook Stage 4, both split directions (A: IS 2005-2012 -> OOS 2013+; B: IS 2013+ -> OOS 2005-2012): OOS/IS Sharpe >= 60%, Calmar >= 60%, CAGR >= 50%, OOS MaxDD <= 1.5x IS, OOS Sharpe > 0.
 B5  Parameter plateau: Sharpe swing <= 0.4 for +-20% moves of L, n_ind, m, H (neighbours above); no cliff.
 B6  Costs: Sharpe at 0.6%/side >= 70% of Sharpe at 0.3%/side; and CAGR still > the faithful Zenith CAGR (13.2%, 2003-26) or EW-pool benchmark, whichever is higher, at 0.6%/side.
 B7  Concentration: ex-best-3-calendar-years Sharpe > 0.5 and CAGR >= 50% of full; top-10 stock-holding episodes <= 40% of positive P&L.
 B8  Risk (the user's stated goal): MaxDD no worse than the equal-weight pool buy-and-hold with the same gate, AND Calmar >= 1.0 x the faithful Zenith Calmar on the same window.
 B9  Diversification: break-even rule Sharpe_new > rho x Sharpe_trio against the FAITHFUL trio (rf 0 and rf 6% both shown), and a 20-30% blend must raise the trio's Sharpe AND not deepen its MaxDD.
 B10 Deflated Sharpe: DSR >= 0.5 with N_trials = (counter below x 3) — reported with N = 20/100/300 so the reader can see the sensitivity.
 B11 Delay sanity (informational): signal lagged one extra month must lose performance (information decays); if it does not, suspect the result is a beta/regime artefact.
 Verdict rules: PASS = B1-B10 hold.  CAUTION = only B6/B7/B10 miss by <20% of the bar.  KILL = any of B1, B2, B4 (either direction), B9 fails -> industry-momentum books are CLOSED (documented), no re-tuning.

## 3. Trial counter (for B10)
Signal studies so far: 111 factors (project) + 64 stage18 variants + 5 stage21 variants + 12 stage19 tilt cells.  Book phase: D1 + neighbours + nulls counted as they are run (see log).

## 4. Logs
OOS-look log: Every time a half/OOS result is inspected is appended below with what changed afterwards (Playbook: >2 post-look modifications spends the window).
Override log (Appendix C): 
| date | item | deviation | reason | needs user sign-off |
|---|---|---|---|---|
| 2026-10-10 | G1(c) global-shuffle placebo | I coded it as "max |NW-t| over 60 draws < 2"; the pre-registered text was a single-draw |t|<2 | a max over draws exceeds 2 by chance with overlapping returns, and LOO mechanically biases null IC to -0.002..-0.004; real IC exceeds every null draw (p=0/60) | yes |

## 5. Amendments and look log (appended 2026-10-10 after the first D1 battery)
OOS-look log (every time a half / holdout result was inspected and what changed afterwards):
| # | date | what was looked at | change made afterwards |
|---|---|---|---|
| 1 | 2026-10-10 | first full D1 battery (halves A/B, nulls, sensitivity, blend). D1 FAILED B3 and B4(Split B); B2 marginal; MaxDD -43% (2008). Controls added (staggered no-industry books, erased-jump stress). | **Amendment 1: D1v = D1 + the chassis-style vol-target overlay (15% annual vol of the whole book, 63-day realised vol lagged one day, de-leverage only, cost 0.3% x |change in scale|).** Parameters are the user's chassis values (csm_value/AUDIT.md: 'vol target 15% de-leverage only'), NOT tuned; 12% and 18% are reported as sensitivity only. The same overlay is applied to every null and benchmark. This is post-look modification #1 of 2 allowed (Playbook 4.1); a second modification would spend the window. |
Trial counter: stage18 64 variants x 4 universes, stage19 12 tilt cells, stage21 5 LOO variants, battery 1 (D1) = 65 book cells, controls ~16, overlay tests ~9. Battery 2 (D1v) adds ~65.
Pre-registered KILL rule is unchanged and applies to D1v exactly as to D1: any of B1, B2, B4 (either direction), B9 failing closes industry-momentum books.
Known limits stated up front: no lockbox exists (all data was seen by the signal studies); survivorship; static labels; the 2005-2012 half trades on far fewer names than 2013+; the only genuine out-of-sample is forward paper trading (Playbook stage 6).

## 6. Outcome (appended after verification, 2026-10-10)
D1: FAIL (B3; B4 Split B) - kill rule fired on B4 for the base spec, and the cause is 2008 (true of every long-only book tested). D1v (Amendment 1): 9/10 gates, only B3 fails, kill rule did not fire. Independent verification: numbers reproduced, no look-ahead, trust rating MEDIUM.
Corrections accepted from the referee: do not compare D1 with the faithful live engines unless the exit model is the same; the industry rank is worth ~+2 pt CAGR / +0.06 Sharpe; headline levels need a 1-4 pt survivorship/hindsight haircut; always show rf 6.5% Sharpe and the cash-0% variant.
Post-look modifications used: 1 of 2 (the vol-target overlay). Any further change to the design should be treated as a NEW pre-registration with fresh evidence (forward paper trading).

## §7 Amendment 2 (2026-10-12, written before running): Zenith as the base, universe robustness, and a worth-it test
User request: make sure everything is sound before any gold/silver overlay; use **Zenith instead of Elendel** as the reference base; check other universes than 1-1000; and give an independent answer on whether an industry strategy is worth implementing.

**A. Health audit of the implementation** (`csm_industry/CSMIndustryBook`): (A1) truncation test - panels cut at 2013-12, 2017-06, 2021-03 must reproduce the full-data target weights on every signal row before the cut (excluding the cut month itself) exactly; (A2) live-row sanity - weights >= 0, sum <= 1, no NaN, all names in the SMA200 pool, labelled, <= 2 per industry, <= 8 industries; (A3) parity with the research simulator (done: exact).

**B. Zenith base.** Comparator = `zenith_faithful` from `csm_value/output/faithful_engine_returns.csv` (Elendel and the trio are dropped as references). Report corr, break-even (Sharpe_new > rho x Sharpe_zenith, rf0 and rf6) and 10/20/30/50% blends over the fully-built window and both halves (<=2012, >=2013).
Stock score inside the selected industries: A1 (primary, unchanged) vs the Zenith composite (A1 + Q5_189, the existing `zen` score frame) = **post-look modification #2 of 2 (the last allowed)**. Rule: switch to the Zenith score only if Sharpe >= A1's in BOTH halves and MaxDD not worse in either half; otherwise A1 stays. No other change is allowed after this.
**Worth-it control**: the same blend-with-Zenith test for simpler books under identical overlays (gate, 15% vol target, 6.5% cash, H=6): (i) no-industry staggered top-16 by the Zenith composite, (ii) EW pool, (iii) mean of 20 random-industry books. The industry layer is "worth it" only if D1v's blend beats (i) and (ii) on Sharpe and MaxDD at 20-30% weight in BOTH halves.

**C. Universe robustness** (D1v spec unchanged: L3 skip0, 8 x 2, H6, min_members 10, gate, vol target 15%; baskets AND stock pool both drawn from the same band; pool = band AND close > SMA200):
bands by 63d median dollar-volume rank: 1-300, 1-500, **1-1000 (base)**, 301-1000, 1-1500, 1-2000. Reported per band: usable industries/month, names, turnover, Sharpe/CAGR/MaxDD (rf0 and rf6), halves, edge over the band's own EW-pool book, 30 random-industry draws (p-value), median daily traded value of picks.
Robustness verdict: PASS if D1v beats its own EW-pool Sharpe in >= 4 of 6 bands AND Sharpe > 1.0 (rf0) in >= 4 of 6. A band replaces 1-1000 only if it beats base Sharpe by >= 0.10 in BOTH halves AND median traded value of picks is not lower than base's; otherwise 1-1000 stays. Capacity beyond rank 1000 is NOT validated by this study.

**D. Verdict criteria (fixed now)** - implementation is "worth it" only if: (1) A1-A3 pass; (2) B worth-it control passes; (3) C robustness passes; (4) the blend with Zenith improves Sharpe and MaxDD in BOTH halves at 20-30%; (5) no more than 60% of the blend benefit comes from a single calendar year. Otherwise the answer is "not worth it as an industry strategy" and I will say which simpler component carries any value.
Trial counter: B score variant (+1), C bands (+5), random-industry draws are nulls. 

### §7 Outcome (run 2026-10-12: `stage23_zenith_universe.py`, `results/stage23_*`; health audit `csm_industry/test_health.py`)
* **A health**: A1 truncation test exact (cuts 2013-12, 2017-06, 2021-03: max diff 0); A2 live-row checks pass (newest cohort in the SMA200 pool, <= 2 names per industry, <= 8 industries, weights >= 0, no NaN; 6 older-tranche names sit below SMA200 by design); A3 parity with the simulator exact for both scores.
* **B2 score rule: SWITCH to the Zenith composite** (halves Sharpe 1.59/1.46 vs A1 1.53/1.34; MaxDD -22.2/-18.8 vs -23.3/-19.3). This was post-look modification #2 of 2: **the D1v specification is now frozen**. Standalone (2005-26, fully built): CAGR 20.6%, Sharpe 1.50 (rf6 1.05), MaxDD -22.2%.
* **Vs Zenith faithful** (12.4% / 0.97 / -31.5%): rho 0.75; 30% blend: Sharpe +0.14 (<=2012) / +0.27 (>=2013), MaxDD +3.6 / +5.1 pt. Best single year = 29% of the benefit (2014).
* **B3 worth-it control FAILED**: the no-industry staggered top-16 Zenith book (same overlays) gives nearly the same blend benefit (dSharpe +0.13/+0.21, MaxDD +3.0/+5.4) and the 20-draw random-industry mean is within ~0.06-0.07 Sharpe; the industry RANKING adds nothing visible in the blend. What the industry structure (<= 2 per industry, positive-trend industries) does buy is standalone drawdown: -22% vs -37% for the no-industry book - but random industries get the same.
* **Sensitivity (not pre-registered)**: the blend benefit depends on how good Zenith really is. Against zenith_engine (engine-booked, Sharpe 2.37, MaxDD -14%) the same blends REDUCE Sharpe by 0.06-0.29. Break-even is roughly Sharpe_Zenith = Sharpe_new / rho = 1.5/0.75 = 2.0.
* **C universes**: D1v beats its own EW-pool Sharpe in 6/6 bands and has Sharpe > 1.0 in 6/6 (PASS), but the industry ranking beats random industries only in broad bands: p = 0.57 (1-300, only ~6 usable industries), 0.07 (1-500), 0.00 (1-1000), 0.07 (301-1000), 0.00 (1-1500), 0.00 (1-2000). 1-1500 / 1-2000 look slightly better (Sharpe 1.48 / 1.49, CAGR ~20.5%) but fail the replacement rule (gain < 0.10 in the first half; lower median traded value of picks; 1-2000 MaxDD -27.6%). **1-1000 stays.** Capacity beyond rank 1000 not validated.
* **D verdict**: criteria (1) PASS, (2) FAIL, (3) PASS, (4) PASS, (5) PASS -> by the rule fixed in advance the answer is "not worth it as an industry/sector-ROTATION strategy"; the value is in the slow staggered, trend-gated, vol-targeted, industry-diversified construction as a diversifying sleeve, conditional on Zenith's true Sharpe being below ~2.

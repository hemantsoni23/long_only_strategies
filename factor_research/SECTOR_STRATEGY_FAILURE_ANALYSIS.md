# Why the sector/industry strategies failed — consolidated findings (2026-10-10)

Scope: every sector/industry strategy in `Discarded sector based strategies/` (six families, ~20 versions), the two earlier
factor-research stages (`stage7_sector.py`, `stage10_sector_stock.py`), and the new bottom-up industry work (FINDINGS §7–8).
Sources: six parallel code audits (each re-ran or re-derived the strategy's numbers), my own re-runs, and the breadth/concentration
measurement in §3. Claims are tagged **[CONFIRMED]** (reproduced from code/data), **[RE-RUN]** (I re-ran the strategy), or
**[INFERRED]** (follows from the code/data layout but not directly tested). Anything untagged is a reported number.

---

## 0. One-paragraph answer

Sector rotation on this data failed for **seven stacked reasons, and the signal itself was only one of them**. (A) The sector layer has
only **11 buckets that behave like one factor** (89% of their variance is a single market component) and are wildly unequal in size —
so a "sector pick" is really a 90–170-stock pool in which all the real selection happens somewhere else. (B) The sector index was built
from ~5,000 untradable, bug-ridden tickers. (C) Gates and quotas stacked on a thin pool left the books **35–55% invested with idle cash at 0%**,
so Sharpe/Calmar/MaxDD looked good merely from sitting in cash. (D) Every variant sat on the same live chassis, which pins
return-correlation to the live engines at **0.78–0.83 regardless of the signal**. (E) The evaluation was wrong: engine-booking, no costs,
rf = 0, one tuning window, reused "OOS". (F) Data bugs (zero prices, unadjusted splits, bad ticks, static labels, survivorship).
(G) A real-but-small signal was asked to carry the whole strategy, and IC never converted into book P&L. Fixing A–F honestly leaves
a **real but modest, front-loaded industry effect (~+2 pt CAGR / +0.06 Sharpe over random industries)**, not a high-alpha rotation.

---

## 1. The attempts, side by side

"Reported" = the author's headline. "Honest" = after the audit's corrections. Every strategy below is a **long-only, top-N-sector × k-stock** design on
`Sector_clean` (11 buckets) unless noted.

| # | Family (folder) | Idea | Reported | What the audit found |
|---|---|---|---|---|
| 1 | `csm_sector_rotation_*` (v1) | AND-gate: stock rankable only if its sector is in top-4 of 11 by 12m+6m momentum | CAGR 13.2%, Sharpe 1.01, MaxDD −31.6% (2003–25) | **Gate is a no-op: +0.07 pt CAGR vs no gate**; worse in IS (15.0 vs 19.1). The sector index was **poisoned by 28 inf cells** (4 of 11 indices dead from 2003/2013). Avg exposure 0.55, ~25% of days flat, cash 0%, 48/276 months with zero names. 2014 alone +110%. |
| 2 | `csm_quad_sector_rotation_*` | Quota: top-3 sectors × 6 stocks, sector cascade exit | IS 32.6% / Sharpe 1.75 / DD −20.7% (2003–14); "tuned" 14.9% / **2.29** / −9.0% | "Tuned" CAGR **fell 54%** while Sharpe rose 31% — pure cash effect (mean exposure 0.56, 21% of days empty). Baseline run contains the Bosch (+861%/−90%) and TIL (−98%/+5131%) phantom days. Knob-selection picked **worse-than-baseline "winners"**. Buffer ladder degenerate (only 2 distinct outcomes). Sector IC 0.13 (t≈5) but P&L no better than the flat-rank baseline; the live baseline beat it. |
| 3 | `csm_meridian_*` | Z-score Zenith's two legs within Industry_clean (fallback Sector) + sector top-8-of-11 gate | 23.8% / 2.01 / −17.3% (2003–13, pre-fix) | **Thin-group z-score bug**: ~3,570 phantom rankable names/month vs ~170 live (20:1). Honest 23.2% / 1.95 / **−24.1%**, and **dominated on every metric by both siblings** (Elendel 29.0%/2.24, Zenith 28.2%/2.28 same window). Top-8-of-11 gate passes 73% of the market. Largest single sector = 36% of holdings (p90 50%, max 100%). Return corr to live stayed 0.78–0.83. |
| 4 | `sector_rotation/v4,v5,v6` (colleague's factor book) | Sector rank = 126d sector return + 21d dispersion; top-3/4 sectors × 2 stocks, weekly | v6: 25.3% / 1.32 / −21.0% (2015–24) | **Not reproducible**: same code, current data → 21.1% / 1.11 / −32.7%. Rebalance weekday alone moves CAGR 6–9 pts. Return-timing bug (entry gap credited, exit gap never charged). **No costs** (turnover ~39× NAV/yr; break-even ≈ 0.5% one-way). 2015+2020+2021 = 70% of log return; the other 7 years compound at 10.3%. Sector indices built from all ~5,000 names (EW benchmark 27% vs tradable top-1000 18%). |
| 5 | `breadth_rotation` v1–v5 (Sector_clean, and an Industry_clean variant) | Rank sectors by breadth (% above SMA200 etc.) orthogonalised to #4; top-4 × 2 | v1 25.4% / 1.42 / **−49.2%**; v5 15.9% / 1.17 / −23.2% (IS 2003–12 only) | Every number is the tuning window. OOS re-run (gross) 16.1% / 1.08 / −28.8%; **at 25 bp/side 12.4%, at 50 bp 8.9%**. Avg 3.1 open positions, 39% zero-position days, gross exposure 0.39. The stock ranker saturates (65% of slots have tied names, broken by CSV row order). Industry_clean variant (v1): 14.2% / 0.90 / −51.1% — the finer level was *worse* here (pools ~6 names). |
| 6 | `breadth_rotation` v6–v9 | Same sector signal; only chassis/stock-rank/stop tweaks | v9: 17.1% / 1.33 / −19.9% (IS) | Total Sharpe gain v6→v9 = 0.149 vs a Sharpe standard error ≈ 0.43 — **noise**. 34.8% average allocation, 45% of days all-cash, no costs at ~459% turnover. Top-5 trades 38% of P&L; ex-2007 CAGR 12.5%, ex-2007/2009 8.9%. ADANIENT unadjusted split books −85.5% in one trade. |
| — | `stage7_sector.py` (earlier research) | Trade the ~19 NSE sector indices directly | standalone Sharpe ~0.3–0.5, MaxDD −50%+ | Too few "assets". |
| — | `stage10_sector_stock.py` (earlier research) | 6/12-month sector momentum as a stock factor | ICIR 0.05–0.2, t mostly < 2 | Wrong horizon; residual variant passed IC but ran 0.6–0.68 correlated with Elendel. |

Pattern: **the more a version was tuned, the lower the CAGR and the higher the Sharpe/Calmar** (#2, #5→#6). That is the signature of
de-risking by sitting in cash, not of a better signal.

---

## 2. Root causes (the taxonomy)

### A. Too few, too-correlated, too-unequal buckets — see §3 for the numbers
11 `Sector_clean` buckets. Measured: 89% of their monthly variance is one component; effective independent *relative* bets ≈ 7; the three biggest
sectors hold 57% of all names while four sectors hold 11%; in the SMA200 trend pool 5–6 of 11 sectors have < 30 names and some go to **zero**.
A sector pick therefore selects a pool of 90–170 stocks (or ~8 for Utilities/Energy), and the book's alpha has to come from the *stock* ranker.
Evidence the sector layer carried no edge: gate vs no gate +0.07 pt (#1); Meridian's sector gate "adds no IC" post-fix and passes 73% of the
market (#3); breadth v1–v5 "alpha is sector selection + trend filter with near-random name choice among tied names" (#5).

### B. The sector signal was measured on an untradable index
Every version built the sector index as the equal-weight mean of **all ~5,000 mapped tickers** — penny stocks, illiquid names, bad ticks — then traded only
the top-1000 liquid subset. The EW all-name benchmark returns 27% CAGR / Sharpe 1.96 vs 18% / 0.95 for the tradable EW top-1000 **[RE-RUN]**. The signal
is therefore partly a micro-cap/illiquidity effect that the book cannot capture. Fix applied in the new work: baskets from `U1_liquid1000` members only,
prior-month eligibility (no look-ahead).

### C. Gates and quotas stacked on a thin pool → a mostly-cash book
Stacked filters (price > 20, top-1000 liquidity, ≤5 circuit days, SMA200, prev-month ≥ −15%, absolute momentum > 0, sector gate, hard bear gate) left
**133 names/month for 30 slots** (#1) and 20.5% of top-4-sector slots with zero candidates (#5). Add a 5% cap × few names and gross never exceeds ~35–90%.
Idle cash earned **0%** and Sharpe used **rf = 0** everywhere. Consequences: headline Sharpe/Calmar/MaxDD are flattered by cash; "smaller books win" (#2:
top-k = 1 caps gross at ~30% and halves CAGR, 16.7% vs 32.6%, yet Sharpe rises 1.97 vs 1.75); and quotas force weak names into top sectors (#2 held up to 35 positions vs 18 nominal).

### D. The shared chassis pins correlation to the live engines
#2, #3, #5, #6 reuse the live Quad/Batch chassis (15 names, 5% cap, −15%/−20% stops, Crash Guard, regime leverage, 15% vol target). On that chassis a
**random ranking already correlates 0.77–0.79** with the live engines, so any signal inherits ~0.78–0.83 daily return correlation — Meridian's factor-rank
"decorrelation" to < 0.77 never reached the return level **[CONFIRMED]**. A sector strategy built on this chassis cannot diversify the live book, which was the
whole point.

### E. Evaluation errors (these inflate every number above)
* **Engine-booking**: the chassis books executed weight × same-day close-to-close, crediting the never-held entry gap and never charging the stop-fill gap
  — inflates CAGR 17–26 pts (Zenith 28.2% → 12.5%; Elendel 32.4 → 10.9; Quad 26.1 → 6.3 over 2003–26) **[CONFIRMED, csm_value/AUDIT.md]**. #4/#5/#6 have the same
  timing flaw in their own simulators.
* **No transaction costs** in #4, #5, #6 (break-even 0.5% one-way; at 25–50 bp OOS CAGR drops 16 → 12.4 → 8.9%).
* **rf = 0** and cash at 0%: Sharpe is not excess return; with India cash at 6–8% the Sharpe of a half-invested book is overstated by ~0.4–0.5.
* **One tuning window**: #5/#6 tuned ~40 choices on 2003–12; #2 ran a 9-knob joint selection on 2003–14; Sharpe SE over 10 years ≈ 0.43 so gains of 0.1–0.15 are noise.
* **"Untouched OOS" that was not**: #2's ablation docstring claims 2015+ is a holdout but a prior script had already evaluated 2013–25 for 5 sector combos; the IS
  window overlaps the OOS window by two years. Stage-4 "PASS" compared the strategy with itself, not with the baseline (which beat it).
* **Phase fragility**: weekly/20-day rebalance counted from backtest start — weekday/start date moves CAGR 6–9 pts (#4 **[RE-RUN]**).
* **Report-window mismatch**: curves start 2001 (two flat years) but are labelled 2003 (#1); window silently shortened from 2025 to 2024 to drop a −12% / −20% year (#4).
* **Selection rule flaws**: "winner = best Calmar among guardrail survivors" accepted worse-than-baseline settings and a 54% CAGR cut (#2).

### F. Data bugs that flowed straight into P&L
* **Zero prices → inf returns** poisoned 4 of 11 sector indices permanently (#1), and the same unclipped code exists in the Quad fork **[INFERRED for the fork]**.
* **Bad ticks and unadjusted corporate actions**: BOSCHLTD 2004 (+861%/−90%), TIL 2018 (−98%/+5131%; +94.9% one-day portfolio gain), ADANIENT 2004-07-29 10:1 split
  (−85.5% booked, −18% in one day at 20% weight), INDIANVSH, GAYATRI, NYSSACORP and others. These guards were applied to the sector *index* only, never to P&L.
* **Static current-day labels** (`instruments_clean.csv` is a 2026 snapshot) and **survivorship** (5,149 of 5,205 files run to 2026; ~56 ended earlier) — flatters early-year breadth
  and returns; only 288 files exist at 2003 and ~1,600 by 2008, so early sector cross-sections are tiny (Technology 6 trades, Real Estate 2 in #6).
* **Industry_clean covers only ~2,749 of ~5,205 tickers** (46% untagged), so any Industry-level design can only ever hold a subset of the market.

### G. Real but small signal; IC never became a book; wrong construction
* A genuine sector effect exists (Quad sector IC 0.13, t≈5; breadth IC 0.25 raw; my LOO industry IC 0.058–0.066, t 7–8), but **P&L was no better than the flat-rank baseline** (#2).
  Top-15/16 books live in the cross-sectional tail; IC rewards the whole cross-section (FINDINGS §3).
* **Horizon mismatch**: IC measured at 21–252d, book re-ranked weekly and held 7–12 days (#4); the composite flips ~0.56 of top-3 sectors per week.
* **Residualising instead of adding**: `stock − sector` kills most of the effect (Moskowitz–Grinblatt) and stayed 0.6–0.68 correlated with Elendel (stage10).
* **Statistical power**: an 11-name cross-section gives IC std 0.32–0.41 per month; sector-dispersion's long-horizon IC vanished after 2015 (126d ICIR 0.465 → 0.025) **[RE-RUN]**.
* **Concentration in time and trades**: top 20 trades = 26% of P&L (#1), 2014 = +110% (#1), 2007/2009 = 59% of P&L (#6), stops net-negative in every version while rank-decline exits carry profit.

---

## 3. The concentration / breadth problem (the user's point), measured

User's observation: only 11 sectors, so each sector holds ~90–100 stocks in a 1–1000 universe. **Confirmed on the average, and the distribution is worse than the average.**
Measured on `U1_liquid1000` (month-end, ex-ante eligible names), `Sector_clean`:

| Sector | avg names 2005–26 | min–max | avg names 2023–26 | share of universe |
|---|---:|---:|---:|---:|
| Industrials | 170.8 | 62–218 | 207 | 21% |
| Consumer Cyclical | 144.3 | 69–184 | 157 | 18% |
| Basic Materials | 136.4 | 55–189 | 159 | 17% |
| Financial Services | 84.4 | 30–136 | 125 | 10% |
| Healthcare | 62.5 | 32–96 | 84 | 8% |
| Consumer Defensive | 57.3 | 28–73 | 62 | 7% |
| Technology | 52.8 | 22–87 | 74 | 7% |
| Communication Services | 28.4 | 14–39 | 24 | 4% |
| Real Estate | 26.3 | 3–40 | 27 | 3% |
| Energy | 18.5 | 9–27 | 23 | 2% |
| Utilities | 16.2 | 6–27 | 23 | 2% |
| **Universe** | **798** (891 in 2013+, 965 in 2023+) | | | 99% labelled |

* **Average ≈ 73–88 per sector** (≈ the 90–100 you estimated, since the real universe is 800–970 names), but the spread is 16 → 207. **Three sectors = 57% of all names**; the four smallest = 11%.
* Effective number of sectors (1/HHI) = **7.2 of 11**; 3.1 sectors (3.7 in 2023–26) have < 30 names.
* In the **SMA200 trend pool** (`U2_live_trend`, what a long-only rotation actually draws from; avg 439 names): **6.1 of 11 sectors have < 30 names** (5.1 in 2023–26) and the minimum is **zero** for
  Industrials, Consumer Cyclical, Basic Materials, Communication, Real Estate, Energy and Utilities in some months — a bear market empties most sectors at once, exactly when rotation is supposed to help.
* **The 11 baskets are one factor**: mean pairwise monthly correlation **0.87**, PC1 = **89%** of variance (PC1–3 = 94%, 2 PCs explain 90%). Raw effective independent bets = **1.3**. Relative to the market
  average (what rotation actually trades) ≈ **7.1** bets, PC1 25%. With 11 buckets and ~7 bets, a top-4 pick is nearly a coin flip about *which* mega-bet to hold.
* **Finer level (Industry_clean) helps, but not as much as the count (205) suggests**: only **23.8** industries have ≥ 10 live members on average (2005+), 26.9 in 2013+, 30.1 in 2023+;
  median usable industry = 17–19 names; 2,417 of 5,242 instruments carry no Industry tag. 19 baskets survive a ≥ 80%-of-months coverage rule; mean correlation 0.80, PC1 82%, relative
  effective bets ≈ **10.5**. Breadth v1 on Industry_clean saw "7.5 usable buckets in 2003", median 10–15 names, ~6 tradable names per pick, 37.8%/week slot churn.

Why this breaks rotation specifically:
1. **The sector layer cannot be selective.** Top-8-of-11 passes 73% of the market; top-4 of 11 still leaves 100–300 stocks. The edge must then come from stock-picking inside a huge pool, i.e. the strategy is a trend-filtered stock picker with a sector label.
2. **Sector index ≈ market.** An equal-weight index of 100–170 heterogeneous businesses (Industrials = capital goods + EPC + defence + logistics + …) is dominated by market beta; sector-vs-market differences are small and noisy.
3. **Sizes differ 13×**, so equal "2 stocks per sector" or "top-k sectors" treats a 16-name sector (Utilities) and a 207-name sector alike; z-scores within groups of different size are not comparable (Meridian: a 5-member group caps at |z| = 1.79 per leg while large groups reach 3+, biasing picks toward big industries).
4. **Whichever sector wins drives book concentration**: Consumer Cyclical = 41% of trades (#1), Meridian single-sector share avg 36% / p90 50% / max 100%, Consumer Defensive 33% + Energy 28% of P&L (#6).
5. **Thin tradable pools in the small sectors**: when Energy/Utilities/Real Estate lead, SMA200 + liquidity + circuit filters leave ~8–14 names, so slots stay empty and the book is in cash.
6. **Statistical**: 11 cross-sectional points per month → IC std 0.32–0.41, impossible to separate skill from noise on 10 years of history.

---

## 4. What the new bottom-up industry work fixed, and what it did not

| Failure cause | Status in the new work (FINDINGS §7–8) |
|---|---|
| A. 11 buckets / one factor | **Partly fixed**: Industry_clean with ≥ 10 live members (≈ 24–30 usable) → ~10.5 relative bets; Sector fallback when thin; ≤ 2 stocks per industry caps concentration. *Not fixed*: still only ~30 industries, 46% of tickers unlabelled, static 2026 labels. |
| B. Untradable index | **Fixed**: baskets from `U1_liquid1000` members only, prior-month eligibility; leave-one-out so a stock's own return is not in its basket. |
| C. Cash-drag / thin pool | **Fixed in accounting, not in nature**: 8 industries × 2 stocks × 6 staggered tranches ≈ 57 names; cash credited 6.5% and Sharpe shown at rf 0 and 6.5%; ~28% of capital still sits in cash (worth +2.1 pt, disclosed). |
| D. Chassis pins correlation | **Not fixed, only measured**: rho 0.82 vs the faithful trio (diversification limited), though break-even test (Sharpe 1.41 > ρ·0.85) and 20–30% blend lift trio Sharpe 0.85 → 1.0–1.07. |
| E. Evaluation errors | **Fixed**: faithful accounting (signal t, fill t+1, earn t+2, 0.3%/side), pre-registered gates, placebo/null books, both split directions, cost/delay stress, blind re-implementation, truncation tests, ≤ 2 post-look changes (1 used). *Not fixed*: no lockbox exists; only forward paper-trading is real OOS. |
| F. Data bugs | **Mostly fixed**: ≥ 40% daily-loss cells erased and tested (603 cells, negligible), locked/NaN names not buyable. *Not fixed*: survivorship (−0.5..−3 pt), static labels (~−0.6 pt). |
| G. Small signal / IC ≠ book | **Faced honestly**: signal real (LOO IC 0.058/0.066, t 6.9–8.0, both halves, placebo p = 0/60) but worth only ~+2.4 pt CAGR / +0.06 Sharpe over random industries, front-loaded (+4.3 pt in 2005–13, −1.4 in 2020–26). The shuffled-label placebo (B3) **fails** (p ≈ 0.15–0.20). Most of D1/D1v is construction (staggering, breadth, gate, vol target, cash). |

Net result, D1v (faithful): CAGR 19.1%, Sharpe 1.41 (0.96 at rf 6.5%), MaxDD −23.3%; plan on ~14–17% after survivorship/hindsight haircuts; parity — not superiority — with live Zenith under identical exits;
recent 2024–26 CAGR 4.8%. This is a sound diversified construction, **not evidence that sector rotation is a high-alpha source**.

---

## 5. Design checklist for any future sector/industry strategy

1. **Never rank 11 sectors.** Use Industry_clean (≥ 10 live members, fall back to sector), report usable-bucket count per month, and treat ~7–10 relative bets as the ceiling.
2. **Build baskets from tradable, ex-ante-eligible, leave-one-out members** — never from the full ~5,000-name mapped list; clip/mask zero prices and ≥ 40% bad ticks before baskets *and* P&L.
3. **Cap per-bucket and per-sector exposure** (≤ 2 names per industry, ≤ ~25–30% per sector) and size by pool depth; do not give small sectors the same quota as Industrials.
4. **No stacked hard gates on thin pools**: measure realised exposure, % empty slots, % zero-position days; evaluate with cash at the actual yield and report Sharpe at rf 0 and rf ≈ 6.5%.
5. **Judge on faithful accounting only** (fill t+1, earn t+2, costs ≥ 0.3%/side, stress to 0.6%); never compare to engine-booked "Sharpe 1.7–2.7 / MaxDD −12..−16%".
6. **Pre-register** gates and the kill rule; use random-stock, random-industry and shuffled-label nulls; test both split directions; allow ≤ 2 post-look changes; count trials and deflate.
7. **Test against the live baseline under identical exits** and measure *return* correlation (not factor-rank correlation); a version that is dominated by its sibling on every metric is dead on arrival.
8. **Stress the nuisance parameters first**: rebalance phase/weekday, start date, window end, cost, delay; if CAGR moves > 3 pts, the headline is a draw from a distribution, not an estimate.
9. **Look for time/trade concentration** (top-3 years, top-20 trades, per-sector P&L share); require the result to survive ex-best-3-years.
10. **Disclose** survivorship, static labels, thin early universe (288 files at 2003), and the fact that unlabelled names (46%) cannot be bought.
11. **Treat IC as a gate, not a verdict**: require IC → top-N book conversion with the same universe and horizon, and check that the best-IC universe is the one actually traded.

---

## 6. Provenance and caveats

* Source scripts: `Discarded sector based strategies/` (`csm_sector_rotation_*`, `csm_quad_sector_rotation_*`, `csm_meridian_*`, `sector_rotation/{v4,v5,v6,breadth_rotation}`), `factor_research/stage7_sector.py`,
  `stage10_sector_stock.py`; new work `industry_lib.py`, `industry_book.py`, `stage18/19/21/22*.py`, `INDUSTRY_BOOK_PREREG.md`, FINDINGS §7–8.
* Several of the discarded scripts no longer run as-is (moved `instruments_clean.csv`, missing `hr_breakout_v2`, deleted `*_work` modules); the audits used patched copies and the moved file.
  The per-claim audit text lives in the session transcript, not the repo.
* §3 measurements: month-end `U1_liquid1000` / `U2_live_trend` membership from `industry_book.load_book_data()`, `Sector_clean`/`Industry_clean` from `instruments_clean.csv`;
  correlation/PCA on monthly basket returns since 2008 (baskets with ≥ 80% coverage). Basket PCA = equal-weight, prior-month eligibility, same construction as `industry_lib.basket_returns`.
* Numbers marked **[INFERRED]** in the audits (survivorship effects, Quad-fork poisoning, some phantom-gain sizes) were not tested directly.
* Nothing here changes `Old_live_strategies/`; no strategy class has been built and nothing has been committed.

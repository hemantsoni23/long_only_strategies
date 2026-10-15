# Improving the Momentum and Breakout Books Beyond the Signal

**Date:** 2026-10-01; extended 2026-10-05 to every book in the repo.
**Scope:** universe filtering, entry timing, portfolio construction, risk management, stop-loss management, validation and live operations for **all** the books: the three CSM books (Elendel / Zenith / Meridian, §§1–4), the HR and VCP breakout books (§I, §J), the older csm_quad / csm_absolute / residual books (§H, §K) and how they combine (§L). Signal ideas are covered in `SHORT_TERM_MOMENTUM_SIGNALS.md` and `LONG_TERM_MOMENTUM_SIGNALS.md`.

**Evidence used. Every claim below is tagged with one of these:**

| Tag | Meaning |
|---|---|
| **[M]** | Measured on this repo's data |
| **[L]** | Literature |
| **[R]** | Measured here **after re-booking the backtest to its own fills** (see §0b). Use these, not [M], for any stop-driven book |
| **[H]** | Hypothesis, not yet tested here |

Where [M] results come from:
- The books' own backtest logs in `output/csm_{elendel_a3q5,zenith,meridian}_{daily,trade}_log.csv` (window 2003-01 → 2013-12).
- The one-change-at-a-time ablation of Zenith in `output/zenith_full_ablation.csv`: 71 configs, same window, `run_zenith_full_ablation.py`.
- The signal screens in this folder.

> **⚠ Correction, 2026-10-05: the backtest engines overstate stop-driven books, and several [M] conclusions below rest on that.**
> The runners compute the curve as `executed_weights × close-to-close returns`. A name that exits today has weight 0 today, so the move from the previous close to its exit fill is **never booked**; a name entered today is credited the whole close-to-close move, including the overnight gap it never held. Re-booking each run from its own trade log changes the headline a lot (§0b).
> What this invalidates: every figure marked **[M]** that depends on how many stops fire, namely the stop-variant table (F2), the "tighter stops help" reading (F1/F2), the Zenith `next_open` result in A4 (the −7.1 pp was an accounting difference, not a fill effect) and the chandelier result. What it leaves standing: cash yield (D1), the signal studies, and the direction of the regime / cooldown / bear-leverage changes, which still help on re-booked numbers (smaller).
> Nothing in the engines was changed (the booking decision is still open, see `IDEAS_BACKLOG.md` C0/C1); the re-booking is a diagnostic in `nextopen_estimator.py`.

---

## 0. Short answer

**Yes.** The signals are not the weak link. The A1/A3/Q5 family is the strongest predictor in every horizon test run here. The bigger gaps are around the signal:

| # | Area | Problem (evidence) | Idea | Expected effect | Evidence |
|---|---|---|---|---|---|
| 1 | Cash | Books are only 59–68% invested on average, and idle cash earns **0%** in the backtests | Park idle cash in a liquid fund (`use_liquid_mf=True`) | **CAGR +3.0 pp; MaxDD −20.8% → −17.7%; Calmar 1.36 → 1.76** | [M] |
| 0 | **Backtest booking** | Stop/exit-day moves and entry-day gaps are mis-booked; stop-heavy books look far better than they are | Re-book every run to its own fills; decide whether to fix the engines | Zenith 28.2% → **12.5%**, csm_quad 31% → **10%**, HR 43.6% → **12.2%**, VCP 34.2% → **12.3%** (IS/full windows, §0b) | [R] |
| 2 | Stop execution | Zenith/Meridian assume resting intraday stop orders; Elendel checks stops on the close | Make backtest fills match how stops are actually placed live | ~~CAGR −7.1 pp~~ **superseded:** the −7.1 pp was an accounting difference; on re-booked numbers "breach, sell next open" is *better* than resting stops (Zenith 22% vs 12.5%, A4) | [M]→[R] |
| 3 | Validation | The books' backtests stop at 2013-12, and settings were picked from 71 in-sample configs | One combined, one-shot holdout test on 2014–2026 | An honest performance estimate; expect some shrinkage | [M]/[L] |
| 4 | Stops | 50–64% of trades exit on stops at −2.6% to −4.6%, after averaging **+20–22% at their peak** | Tighter entry stop, ATR chandelier, or a tighter peak stop | ~~Sharpe 2.28 → 2.43–2.69~~ **engine-booked, biased toward more stops.** Re-booked: entry −10% adds ~0.1 pp CAGR and trims MaxDD −31.5% → −28.1%; chandelier **collapses** (15.1% → 0.7% CAGR) | [M]→[R] |
| 5 | Entry timing | 14–17% of trades hit the −15% entry stop; last week's biggest winners lose −19%/yr the next week | Exclude or delay names that just spiked | Fewer early stop-outs | [M] signal, [H] book effect |
| 6 | Concentration | The largest single sector is 32–36% of holdings on average, 43–50% at the 90th percentile, up to 76–100% | Sector cap of about 35–40% | Lower tail risk; small return cost possible | [M]/[H] |
| 7 | Cross-book | Daily return correlation between the books is **0.77–0.85**; an equal-weight combo adds little | Treat them as one sleeve; cap single-name exposure across books; diversify with different strategies | Real diversification only comes from new information | [M] |
| 8 | Crash risk | All three books' worst drawdowns were in early 2009, the classic momentum crash | Scale exposure by the book's own realised volatility | Smaller rebound-crash losses | [L]/[H] |
| 9 | Holding period | Signal IC keeps rising out to 6–12 months, but `quarterly_entries` *hurt* (cash drag) | Staggered tranches | About 40% less turnover at the same edge; less rebalance-date luck | [M]/[L] |
| 10 | HR breakout | 94% of trades exit on a stop; 15–20% of capital idle at 0% | Cash yield; **do not** tighten stops | Re-booked in-sample CAGR 17.5% → 19.1% from cash; tighter stops *lower* it to 15–16% (§I) | [R] |
| 11 | VCP | Only 27–33% invested in 2003–13 (2.4 names); sized off a ~8% ATR distance but exits on a flat 15% stop | Cash yield (+4.7 pp), 12% hard stop, 40-day stale exit | Re-booked in-sample CAGR 9.2% → 13.9% (cash) → 15.4–16.7% with stops; **holdout pending** (§J) | [R] |
| 12 | csm_quad / other old books | Same chassis as Zenith, same booking issue; csm_absolute already flagged (C0) | Port the Zenith package; fix booking first | quad re-booked CAGR 10.0% → 13.2% in-sample, 7.1% → 8.3% since 2014 (§K) | [R] |
| 13 | Combining books | HR/VCP correlate 0.62 / 0.46 with Zenith vs 0.77 for quad | Zenith + VCP is the only combination that helped on re-booked numbers | Sharpe 0.97 → 1.05, Calmar 0.39 → 0.43 (§L) | [R] |


### 0b. What the books really earn once the booking is consistent [R]

Same cleaned 2001–2026 panel for every book, 0.3% per side, each book run as its own runner configures it. "Re-booked" adds the exit-day move to the fill and strips the never-held entry gap (`nextopen_estimator.rebook`, applied to the engine's own executed weights; the engines are untouched). Sanity check: Zenith's `next_open` engine, which already holds names through the breach day, moves only 21.1% → 22.2%.

| Book | Window | Engine CAGR / Sharpe | **Re-booked CAGR / Sharpe / MaxDD** | Avg exposure | Stop share of exits |
|---|---|---|---|---|---|
| Zenith, old defaults | 2005–13 | 29.1% / 2.22 | **11.6% / 0.91 / −35.0%** | 70% | 55% |
| | 2014–26 | 24.3% / 1.76 | **8.0% / 0.61 / −35.7%** | 78% | |
| Zenith, new defaults | 2005–13 | 32.7% / 2.71 | **15.9% / 1.32 / −25.9%** | 62% | 63% |
| | 2014–26 | 28.1% / 2.14 | **9.7% / 0.75 / −31.7%** | 72% | |
| csm_quad (repo version) | 2005–13 | 30.7% / 2.20 | **7.8% / 0.61 / −36.8%** | 65% | 65% |
| | 2014–26 | 29.6% / 1.98 | **7.1% / 0.53 / −47.0%** | 69% | |
| HR breakout | 2005–13 | 41.6% / 1.97 | **11.4% / 0.63 / −38.6%** | 74% | 94% |
| | 2014–26 | 45.0% / 1.82 | **12.8% / 0.63 / −51.0%** | 87% | |
| VCP (rank 500–1000) | 2005–13 | 25.5% / 2.13 | **11.4% / 0.94 / −31.4%** | 33% | 83% |
| | 2014–26 | 47.5% / 2.36 | **15.0% / 0.84 / −40.0%** | 69% | |

- **How to read it:** the engines say 25–48% a year; booked consistently, every book is **7–16%**. The gap grows with the stop share, which is why HR (94% stops) loses the most.
- **Independent evidence that the engine is the problem, not the re-booking:** the trade logs (real entry and exit fills) are the same in both views. For old Zenith 2003–13 at zero cost, the trade log's own rupee P&L takes ₹1 to about ₹10 (a rough figure, since it assumes fixed quantities), between the engine's ₹20 and the re-booked ₹4.75, and Zenith's per-trade averages follow the re-booked ordering (A4). The check that the re-booking is not simply too harsh is the `next_open` engine, which it leaves almost unchanged.
- **Not yet re-booked:** Elendel, Meridian, Equinox (same engine, expect a similar gap; their stop shares are 50–64%), csm_absolute (already shown at +38% → −16%, `TIDE_BACKTEST_RESULTS.md` §3) and residual momentum (its exits are sold at the next open, so its booking should already be consistent; unverified).
- **What survives:** rank-ordered relative comparisons *within a book that change few stops* (cash yield, signal, universe) and trade-level statistics. What does not: absolute CAGR/Sharpe/drawdown, and any comparison that changes how many stops fire.
- **Decision still open:** fix the exit-day / entry-day booking in the engines (every number in this repo shifts), or keep the engines and report both. See `IDEAS_BACKLOG.md` C0.

---

## 1. What the books actually do today

All figures are measured from the 2003–2013 backtest logs. **They are engine-booked: CAGR, Sharpe and drawdown in this section (and the stop-exit averages that exclude the unbooked stop-day move) are overstated for stop-heavy books, see §0b.**

| | Elendel | Zenith | Meridian |
|---|---|---|---|
| CAGR / MaxDD (worst date) | 29.0% / −19.9% (2009-03-25) | 28.2% / −20.8% (2009-01-07) | 23.8% / −17.3% (2009-03-24) |
| Average exposure (median) | **59%** (64%) | **63%** (70%) | **68%** (75%) |
| Days less than 50% invested | 33% | 31% | 21% |
| Average positions / maximum | 14.2 / 26 | 14.8 / 27 | 16.6 / 30 |
| Regime mix | Bull 67%, Bear 24%, High-vol 8%, Panic 2% (all three) | | |
| Trades | 1,005 | 909 | 1,010 |
| Exits by stop | **64%**, avg −2.6%, win 26% | **58%**, avg −2.6%, win 28% | **50%**, avg −4.6%, win 25% |
| Average peak gain (MFE) of stopped trades | **+22.4%** | **+22.1%** | **+19.6%** |
| Stopped trades that had been +15% or more | 43% | 42% | 43% |
| Exits by rank decay (rebalance) | 34%, avg **+15.9%**, win 76%, ~80d hold | 38%, avg **+16.0%**, win 81% | 48%, avg **+13.3%**, win 66% |
| Entry-floor stops (−15% from entry) | 173 (17%) | 143 (16%) | 128 (13%) |
| Gap-down exits (filled below the stop) | 145 | 104 | 128 |
| Largest single-sector share of holdings: mean / p90 / max | 34% / 50% / 76% | 32% / 43% / 82% | 36% / 50% / 100% |
| Re-entry after a stop: avg PnL vs fresh entry | 2.4% vs 4.6% | 4.2% vs 5.2% | 4.5% vs 3.8% |

Daily net-return correlation (2003–13): Elendel–Zenith **0.85**, Elendel–Meridian **0.77**, Zenith–Meridian **0.82**.

| Portfolio | Sharpe | MaxDD |
|---|---|---|
| Elendel / Zenith / Meridian, each alone | 2.24 / 2.28 / 2.01 | −19.9% / −20.8% / −17.3% |
| Equal-weight combination of all three | 2.33 | −19.0% |

**Settings that differ between the books for no stated reason:**
- Elendel has **no Low-MAX exclusion**; Zenith and Meridian do.
- Stop fills: Elendel `stop_fill_mode='close_next_open'`; Zenith and Meridian `'stop'`. **But see A4: the Elendel backtest never applies `close_next_open`**, so all three backtests actually run resting-stop fills.
- Q5 lookback: Zenith 189 days vs Elendel 126.

**Settings all three share:**
- 15 names at up to 5% each, so the gross cap is about 75% plus buffer carry-over.
- Hard stops at −15% from entry and −20% from peak; the chandelier is off.
- Crash guard on, 15% volatility target, regime leverage 1.0 / 0.8 / 0.5.
- Backtest assumptions: transaction cost 0.3% flat, risk-free 0%, idle cash earns 0%, ₹1 lakh starting capital, no liquidity cap.

---

## 2. Ideas by area

Each idea gives the problem, the change, what to expect and how to test it.

The baseline for **[M] ablation numbers** is Zenith 2003–13: **CAGR 28.2%, volatility 11.3%, Sharpe 2.28, Sortino 3.50, MaxDD −20.8%, Calmar 1.36, turnover 8.1×/yr**.

### A. Validation and backtest realism (do these first; they decide whether anything else is real)

**A1. Use 2014–2026 as a one-shot holdout.**
- **Problem [M]:** every book's runner stops at 2013-12-31. Zenith's settings were chosen by looking at 71 in-sample configs over the same window. Nothing since 2014 has been used to *choose* chassis settings. That is 12+ years of clean holdout.
- **Change:** freeze one candidate configuration per book, combining the changes from steps 1–2 of §3. Run it **once** on 2014-01 → 2026-09, using full-history indicators (no cold start). Report it beside the unchanged baseline.
- **Expect:** lower numbers than in-sample. The bake-off showed signal ICs fell 25–38% after 2018. This is the most valuable single run, because it tells you which of the ideas below are real.

**A2. Correct for having picked winners from 71 configs.**
- **Problem [L]:** over 11 years, the standard error of a single Sharpe ratio is about 0.57 (Lo 2002: √((1+SR²/2)/years) with SR ≈ 2.3). Most ablation gains are +0.05 to +0.4 Sharpe. Picking the best of 70 guarantees some of that gain is luck.
- **Change:** only adopt changes with an economic reason, apply a Deflated Sharpe check, and confirm on the A1 holdout.
- **Expect:** some in-sample winners will not survive. That is the point.

**A3. Make costs and slippage realistic.**
- **Problem [M]:**
  - Costs are a flat 0.3% per side regardless of liquidity.
  - In this repo's VCP study, the "better" rank 500–1000 band went from Calmar 1.67 at 0.3% cost to 0.69 at 1.5%; the liquid band held up far better.
- **Changes:**
  - Rerun each book at 0.3%, 0.6% and 1.0%.
  - Add slippage that grows with position size ÷ 20-day average daily value traded (ADV).
  - Cap each position at about 5–10% of ADV.
  - Rerun at the capital you actually intend to deploy, not ₹1 lakh.
- **Expect:** a lower but honest return figure, and a real capacity limit. It also decides whether the universe changes in B4 are safe.

**A4. Align the stop-fill model with how stops are actually executed live.**
- **Problem [M]:**
  - Zenith and Meridian assume a resting intraday stop that fills at the stop level.
  - Elendel assumes the stop is checked on the close and sold at the next open.
  - In the Zenith ablation, switching to "breach intraday, sell next open" (`stop_fill_mode='next_open'`) gave **CAGR 21.1% (−7.1 pp), Sharpe 1.69, MaxDD −29.1%, Calmar 0.73**.
- **Change:**
  - Decide how stops are placed live: broker stop-loss orders every day, or an end-of-day check.
  - Make all three books use that model.
  - If stops are end-of-day, rerun Zenith and Meridian with `close_next_open`.
- **Expect:** if live stops aren't resting broker orders, Zenith and Meridian's current backtests are **optimistic by several points of CAGR**. This is the biggest realism risk found.
- **Correction (2026-10-02, code reading):** Elendel's backtest does *not* model close-checked stops either.
  - `run_csm_elendel_backtest.py` only branches on `stop_fill_mode == 'next_open'` (lines 760 and 840).
  - It calls `_check_stop_exit` without `close_only` (line 826).
  - So with the default `'close_next_open'`, the backtest triggers on the intraday low and fills at the stop the same day, exactly like `'stop'`.
  - Only Elendel's live `get_exit_signals` uses the close-only check (`csm_elendel_strategy.py:746`).
  - **All three books' 2003–13 numbers therefore assume resting stops.** If Elendel's live stops really are end-of-day checks, its backtest is optimistic in the same way as Zenith's `next_open` row above. Implementing the mode in the runner is a prerequisite for the A1 holdout.

- **Correction (2026-10-05, re-booking [R]):** the "−7.1 pp" is an accounting difference, not a fill effect.
  - In `next_open` mode the position is still held at the close of the breach day, so that day's loss *is* booked; in resting-stop mode the exit-day weight is 0, so the loss to the stop price is *not*. The two modes therefore book different amounts for the same economics.
  - Re-booked to each mode's own fills (Zenith, 2003–13): resting stops **12.5%** CAGR (engine said 28.2%); next-open **22.2%** (engine 21.1%, almost unchanged because it was nearly consistent already). 2014–26: resting 8.0% vs next-open 11.4%.
  - Per trade, the same ordering: the average stopped trade earns **+1.3%** with next-open exits and **−2.6%** with resting fills, because the next open is on average 4% above the stop price (wick lows recover, gap-downs mean-revert).
  - So the live question reverses: on this data, "check, then sell next open" beats resting broker stops. Caveat: the engine's next-open mode still *triggers* on the intraday low; a live end-of-day check would trigger on the close, which is not measured.
  - Open item stays C1, but the framing is now "which booking is true", not "how much do we lose without resting orders".

**A5. Check the entry-price assumption.**
- **Problem [M]:** the short-term research found that measuring returns from the next day's opening print inflated some signals by about 60%. Opening prices carry a per-stock bias.
- **Change:** re-score book entries at a VWAP proxy ((O+H+L+C)/4) or at the next close, and compare.
- **Expect:** probably a small effect for these slow signals (SC1-type signals barely moved), but it should be measured once.

**A6. Survivorship bias.**
- **Problem [M]:** the folder has no delisting calendar, so dead stocks are under-represented. Every CAGR and Sharpe here is an upper bound.
- **Change:** get NSE's list of delisted and suspended stocks, and treat a disappearance as an exit at the last price, or at a haircut for compulsory delistings.
- **Expect:** lower numbers, mostly in the small and mid-cap tail.

### B. Universe filtering

**B1. Add Low-MAX exclusion to Elendel.**
- **Evidence [M]:** the stocks with the biggest one-day spike in the last month (the top Low-MAX quintile) lose **−15.1%/yr** over the next week and −5.5%/yr over a month. Zenith and Meridian already exclude the worst 20%.
- **Caveat:** in `zenith_param_ablation.csv`, Zenith's composite IC was *higher* without the exclusion (0.086 vs 0.077). IC isn't the right test for a filter, because removing names reduces the cross-section being ranked.
- **Expect [H]:** fewer blow-ups among Elendel's entries. Needs a book backtest with the parameter on vs off.

**B2. Entry-spike filters (new).**
- **Evidence [M], from the short-term screen, entry at the next close:**
  - Last week's top-fifth gainers: **−19.2%/yr** the next week.
  - Stocks whose recent gains came on ≥2× volume days: **−12.1%/yr**.
  - Volume-spike stocks: **−14.1%/yr**.
- **Change:** at each rebalance, skip or postpone new entries that are in the top fifth of the 5-day return, or whose 21-day gain came mostly on heavy-volume days.
- **Expect [H]:** fewer entry-floor stops (13–17% of trades today) and fewer gap-down exits, with a small loss of the best runners. The breakout lab found that waiting 2 days after a breakout added +0.71%.

**B3. High-volatility exclusion.**
- **Evidence [M]:** 12-month low volatility has IC 0.07–0.09 at 6–12 months, but all of it comes from avoiding the most volatile names. The most volatile fifth is the problem.
- **Change:** exclude the top-volatility quintile, like Low-MAX.
- **Expect [H]:** lower drawdowns, with a small return cost in speculative rallies.
- **Caveat [M] (2026-10-02, `LONG_TERM_MOMENTUM_SIGNALS.md` §7.3):** measured on the cleaned panel with entry at the next close, 63d volatility deciles are hump-shaped.
  - The most volatile decile earns only −1.5%/yr against the universe; the *least* volatile earns −3.3%/yr.
  - So the exclusion removes names whose mean return is only slightly below average. Expect a mostly risk-side effect (drawdown, dispersion), not a return gain.
  - Judge it on a book ablation, not on IC.

**B4. Price floor and universe size.**
- **Evidence [M] (Zenith ablation):**

| Change | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| `min_price=10` | 30.2% | 2.39 | −20.1% | **1.50** |
| `universe_top_n_max=1500` | 29.1% | 2.33 | −20.3% | 1.43 |
| `universe_top_n_max=500` | 26.5% | 2.15 | −21.1% | 1.26 (worse) |
| `max_circuit_days=3` | 28.3% | 2.28 | −19.6% | 1.44 |

- **Caution:** cheaper and less liquid names flatter results at a flat 0.3% cost, which is exactly the VCP band lesson.
- **Change:** only adopt after A3's liquidity-aware costs.
- **Expect:** +1 to 2 pp CAGR in-sample, possibly zero after realistic costs.

**B5. Liquidity cap per position [H]:** at most about 5–10% of 20-day ADV. It protects live capacity, and nothing in the books enforces it today.

**B6. Corporate-action detection [M]:** the mask only catches one-day moves below −40% or above +300%. An unadjusted 1:2 bonus (−33%) slips through and can trigger a false stop. It is rare (about 0.2% of events in the breakout lab), so it is low priority, but cheap to fix with a list of standard split/bonus ratios.

### C. Entry timing and execution

**C1. Don't buy at the top of a short-term spike.** This is B2 used as *delay* rather than *exclude*. Enter at the next weekly check once the 5-day spike has cooled.
- **Expect [H]:** better entry prices for the 20–30% of new entries that arrive just after a spike.

**C2. Staggered tranches instead of one month-end rebalance.**
- **Evidence:**
  - [M] IC rises from 0.055 (1 month) to 0.12 (6 months) for the books' signals.
  - [M] But `quarterly_entries=True` gave **CAGR 17.2%, Calmar 0.93**: stops still fire monthly, so stopped capital sat idle for up to a quarter.
  - [L] Hoffstein et al. measured up to **348 bp/yr** CAGR spread between rebalance dates for US momentum; tranching reduces that spread roughly by 1/N.
- **Change:** split each book into 3 tranches, each rebalanced every 3 months on staggered month-ends. Stops still exit at any time, and freed capital is re-deployed at that tranche's next rebalance or in the next tranche's.
- **Expect:**
  - About 40% less turnover at the same gross edge. Top-quintile proxy, net of 30 bp: Elendel +0.9 pp/yr, Meridian +1.4 pp, Zenith +0.2 pp.
  - Smoother results that depend less on which day the rebalance falls.
  - Must be backtested, because the `quarterly_entries` failure shows implementation details dominate.

**C3. Execution style [H]:** use limit or VWAP-style execution over market-on-open for rebalances. The opening print is noisy in this data (A5).

### D. Portfolio construction

**D1. Earn yield on idle cash (largest measured gain, lowest risk).**
- **Evidence [M]:** average exposure is 59–68%, so 32–41% of capital is idle.
  - Zenith with `use_liquid_mf=True` (6.5% on idle cash): **CAGR 31.2% (+3.0 pp), Sharpe 2.49, MaxDD −17.7%, Calmar 1.76**.
  - Rough check: 0.32–0.41 idle × 6.5% ≈ +2.1 to +2.7 pp/yr.
- **Change:**
  - Turn the flag on in all three books.
  - Live, sweep idle cash into a liquid fund or a liquid ETF (e.g. LIQUIDBEES), keeping 1–2 days of settlement buffer.
- **Expect:** about +2–3 pp CAGR and shallower drawdowns.
- **Caveat:** the 6.5% assumption is constant; real liquid-fund yields varied with the policy rate (about 4% to 9%).

**D2. Holding period.** See C2. Don't use `quarterly_entries`.

**D3. Exposure and cash drag: more beta is not more edge.**
- **Evidence [M]:**

| Change | CAGR | Sharpe | Vol | MaxDD | Calmar |
|---|---|---|---|---|---|
| `top_n=20` | 29.8% | 2.27 | — | **−24.5%** | 1.21 |
| `max_weight_per_stock` 0.07 | — | 2.06 | — | −23.6% | — |
| `max_weight_per_stock` 0.10 | — | 2.10 | — | −23.9% | — |
| `leverage_bull=1.2` | 34.2% | 2.17 | 14.2% | — | 1.53 |

This repo's earlier risk-budget sizing A/B test also made Sharpe, MaxDD and Calmar worse.

**Structural cap [M, code]:** each weight is capped at min(`risk_pct_per_trade` / `hard_stop_from_entry`, `max_weight_per_stock`) = min(6.7%, 5%) = 5%, and the clip-and-renormalise loop ends with a final clip (`csm_elendel_strategy.py:555-561`).
- With `top_n=15`, the books are at most **75%** invested (up to 90% only while buffered names push holdings to 18), before the overlay scales anything down.
- So the 59–68% average exposure in §1 is mostly this sizing rule, not the regime overlay.
- csm_quad has the same cap. csm_absolute (12% cap, 25 names) and residual momentum (renormalised to 100%) do not.
- **Recommendation:** treat exposure as a deliberate risk dial, not something to maximise. Fix cash yield (D1) first, then decide whether you want more market risk.
- **Expect:** higher exposure raises CAGR and drawdown together; risk-adjusted return stays flat or gets worse.

**D4. Sector concentration cap.**
- **Evidence [M]:** the largest sector is 32–36% of the book on average, 43–50% at the 90th percentile, and reached 76% (Elendel), 82% (Zenith) and **100%** (Meridian). Meridian's sector gate selects the top 8 sectors; it does not cap concentration within them.
- **[L]:** industry momentum is part of momentum's return (Moskowitz-Grinblatt), so capping can cost some upside.
- **Change:** cap any sector at 35–40% of the book, and test with and without it.
- **Expect [H]:** smaller losses in sector-specific busts (e.g. 2008 realty/infra), possibly 0.5–1 pp/yr less CAGR in strong sector runs. Judge it on Calmar and worst-month loss, not CAGR.

**D5. Manage the three books as one sleeve.**
- **Evidence [M]:** daily correlation is 0.77–0.85. The equal-weight combo improves Sharpe only to 2.33 and MaxDD to −19.0%. Trade-log overlap (aligned windows) is 15–34%. **Update 2026-10-05 [R]:** HR and VCP correlate 0.62 and 0.46 with Zenith, so they are the better diversifiers; only Zenith + VCP improved every metric on re-booked numbers (§L).
- **Changes:**
  - Cap combined single-name exposure across books, e.g. 8–10% of total capital.
  - Allocate capital across *different* strategies (HR, VCP, the short-term SC1 candidate) rather than across these three.
- **Expect:** a lower combined drawdown only if the added sleeves are genuinely different. SC1's correlation with the books' signals is −0.09 to −0.22.

**D6. Weighting within a book [H]:** test inverse-volatility weights, or weights tilted by signal strength, against today's near-equal weights. Not measured yet.

### E. Risk management (portfolio level)

**E1. Momentum-crash protection.**
- **Evidence:**
  - [M] Every book's worst drawdown came in Jan–Mar 2009, when last year's losers rallied hardest.
  - [M] The crash guard helps: turning it off gave MaxDD −24.4% and Calmar 1.12.
  - [M] The current volatility scaler uses *benchmark* volatility and rarely binds (mean `Vol_Scale` 0.96–0.98).
  - [L] Scaling momentum exposure by the strategy's *own* recent volatility (Barroso & Santa-Clara 2015) largely removes the worst crashes and roughly doubles the Sharpe of US long-short momentum. Daniel & Moskowitz (2016) cut exposure in "bear market + high volatility" states.
- **Change:** add a scaler based on the book's own 6-month realised volatility, or the realised volatility of a long-short spread of the books' signal, targeting about 15%.
- **Expect [H]:** smaller drawdowns in rebound crashes (2009, 2020). The gain for a long-only top-15 book is smaller than the literature's long-short result.

**E2. Regime settings (measured in-sample, need holdout confirmation).**

| Change | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| `leverage_bear=0.6` | 27.4% | — | **−17.9%** | **1.54** |
| `use_cg_quality_gate=True` | 28.7% | — | −17.4% | **1.65** |
| `abs_momentum_lag_months=2` | 27.8% | — | −18.0% | 1.55 |
| `abs_momentum_lookback_months=18` | — | — | — | 1.45 |

- **Expect:** each lifts Calmar by about 0.1–0.3 in-sample. They overlap, so don't add the effects together; test them as one package on A1.

**E3. The correlation guard never fires [M].** `Corr_Scale` averages 0.99–1.00, and thresholds of 0.6, 0.8 and 1.0 give near-identical results. Either remove it for simplicity, or redesign it to measure the book's real crowding (average pairwise correlation or sector share).

**E4. Book-level drawdown brake [H, low priority].** For example, halve exposure after a −15% book drawdown. Evidence for this is mixed: it often delays recovery after V-shaped rebounds, which is exactly when momentum books recover. Only consider it after E1.

**E5. Live monitoring [L].**
- Rolling 12-month IC of each book's live signal (ICs fell 25–38% after 2018).
- Live vs backtest fill slippage.
- Exposure and sector dashboards.
- Pre-agreed rules for cutting size when the live IC or tracking error breaks below set bands.

### F. Stop-loss management

**F1. Where the giveback comes from [M].**
- Stops close 50–64% of all trades, at an average of −2.6% to −4.6%. Those same trades had peaked at **+20–22%** on average, and 42–43% had been +15% or more.
- So the current 20%-from-peak stop gives back most of the gain.
- The money is made in rank-decay exits: **+13% to +16%** average, 66–81% win rate, about 80-day holds.

**F2. Stop variants already measured (Zenith, in-sample).**

| Variant | CAGR | Vol | Sharpe | MaxDD | Calmar | Turnover/yr |
|---|---|---|---|---|---|---|
| Baseline (entry −15%, peak −20%) | 28.2% | 11.3% | 2.28 | −20.8% | 1.36 | 8.1× |
| Entry stop −10% | 29.1% | 10.9% | 2.43 | **−17.9%** | **1.63** | 8.8× |
| Peak stop −15% | 29.0% | 10.5% | 2.51 | −19.5% | 1.48 | 10.4× |
| ATR chandelier (default) | 27.8% | **9.4%** | **2.69** | −18.0% | 1.55 | **15.8×** |
| ATR chandelier + ATR cap | 27.7% | 9.0% | **2.78** | −18.6% | 1.48 | 17.1× |
| Flat (not loss-scaled) cooldown | 29.7% | 11.1% | 2.41 | −17.9% | **1.66** | 7.7× |
| Stop cooldown 40 days | 28.6% | 11.2% | 2.33 | −19.5% | 1.47 | 7.7× |
| Entry stop −20% | 27.8% | 11.5% | 2.21 | −22.7% | 1.23 | 7.9× |
| Peak stop −25% | 27.3% | 11.6% | 2.17 | −23.0% | 1.19 | 7.2× |

- **Correction (2026-10-05):** the table above is engine-booked and favours any change that fires more stops, so its ranking is biased. Re-booked [R], Zenith 2003–13, each change on top of cash yield (D1: 15.1% CAGR, Calmar 0.48):

| Variant | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| D1 (liquid-fund cash) | 15.1% | 1.20 | −31.5% | 0.48 |
| + entry stop −10% | 15.2% | 1.25 | −28.1% | 0.54 |
| + flat cooldown | 16.8% | 1.34 | −30.0% | 0.56 |
| + crash-guard quality gate | 15.8% | 1.26 | −29.2% | 0.54 |
| + bear leverage 0.6 | 15.7% | 1.28 | −26.9% | 0.58 |
| + ATR initial stop 2.5× | 15.5% | 1.26 | −28.6% | 0.54 |
| + chandelier | **0.7%** | 0.12 | −40.1% | 0.02 |
| Package (D1 + stop 10% + flat + gate + bear 0.6), **adopted as Zenith's default** | **17.1%** | 1.48 | −25.9% | 0.66 |

- The package still wins on the one-shot 2014–26 holdout on re-booked numbers: old Zenith 8.0% CAGR / Sharpe 0.61 / MaxDD −35.7%, package 9.7% / 0.75 / −31.7% (resting stops); 11.4% vs 13.9% with next-open exits. The gain is real but modest; most of it is cash yield and flat cooldown. The tight-stop and chandelier gains in the engine-booked table were mostly the artefact.
- **[L]:** Han, Zhou & Zhu (2016) found a simple 10% stop-loss on momentum cut the worst monthly loss from −49.8% to −11.4% and more than doubled Sharpe (US long-short, 1926–2013).
- ~~**Reading:** tighter stops consistently improve risk-adjusted returns here~~ **Withdrawn (2026-10-05):** on re-booked numbers a tighter entry stop mainly trims drawdown and the chandelier destroys the book (it fires twice as many stops, each one an unbooked loss in the engine).
- **Recommendation (revised):** keep entry −10% + flat cooldown for the drawdown benefit, **drop the chandelier**. The A1 holdout has been run for Zenith (`ZENITH_IMPROVEMENT_RESULTS.md`).

**F3. Volatility-scaled initial stops [H].** Today every stock gets a flat 15% entry stop. That is noise for a high-volatility small-cap and generous for a quiet large-cap. Test an initial stop of about 2.5–3 × ATR, clamped to 8–20%. The chandelier results in F2 are indirect support.

**F4. Gap risk [M]/[H].**
- 104–145 exits per book filled below the stop on a gap-down. Resting stops can't prevent that.
- Options:
  - Smaller weights for names with high historical overnight-gap volatility.
  - Avoid holding through results dates. That needs an earnings calendar, which is not in this data.
- The short-term research also found that big overnight *gains* tend to reverse.

**F5. Tested and rejected [M]. Do not use** (note: the "next-open fills" row is withdrawn, see A4; the other rows are not stop-count-driven or were rejected on trade-level evidence):

| Change | Result |
|---|---|
| Partial profit-taking (`use_crystallisation`) | CAGR 14.9%, Calmar 0.59 |
| Time stop | Calmar 1.23 |
| "Breach intraday, sell next open" fills | Calmar 0.73 |

Layering a partial profit-take on HR also hurt, in this session's test.

**F6. Re-entry after a stop [M].** Results are mixed: worse for Elendel (avg 2.4% vs 4.6% for fresh entries), better for Meridian. No change recommended beyond testing the flat cooldown in F2.

### G. Diversification (beyond the three books; HR, VCP and the older books are covered in §§I–L)

- **G1.** Add a short-term sleeve built on **SC1** (industry 1-month momentum + within-industry reversal; see `SHORT_TERM_MOMENTUM_SIGNALS.md`). Its correlation with the books' signals is −0.09 to −0.22, which no A1/A3/Q5 variant can offer. It still needs its own cost-aware backtest.
- **G2.** Keep HR and VCP as separate sleeves and measure their overlap with the books on **aligned date windows**. A truncated window makes strategies look more diversified than they are.

### H. Lessons from the older live books (`Old_momentum_strategies/`, reviewed 2026-10-02)

The three older books still trade live. Code facts below are from these files. Results marked **[ext]** come from their own docs in `/Users/hemantsoni/Documents/final_momentum_strategies/`, measured on their own windows, not re-run here.

| | csm_quad | csm_absolute | residual momentum |
|---|---|---|---|
| Signal | Average of raw 6m and 12m return/vol, skip 1m (the 3/6/9/12 "quad" version was retired) | Average of raw 9m and 4m return/vol, skip 1m; entry needs factor > 0.6 and 9m return > 0 | z(168-day CAPM residual t-stat vs the equal-weight top-500 market) + z(52-week-high ratio) |
| Universe | Liquidity **band 500–1000** in the live runner | Top 1,000, ≤ 8 circuit days | Top 500, price ≥ ₹20, ≥ ₹1 cr/day |
| Book | 15 names, 5% cap (75% gross), monthly | 25 names, 12% cap, **quarterly** re-rank | 40 names, enter ≤ 30 / hold ≤ 80, about 100% gross, monthly |
| Stops | −15% entry / −20% peak | **−8% entry / −12% peak** + 2×ATR chandelier | −25% from peak, sold next open |
| Regime | Vol-panic crash guard; bear ×0.8 | **Sells everything whenever the EW benchmark is below its SMA-200** | Flat when the EW index is below its 150-day SMA |

**H1. The Elendel/Zenith/Meridian chassis is the csm_quad chassis.** The defaults are identical; only the signal and the universe band changed. That is why the books' return correlation has a structural floor. [M] In the 2026-10-01 Zenith–Elendel tests, two *random*-ranking 15-name books on this chassis already correlated 0.77–0.79 in daily returns. Changing the signal can't push a new book below that unless the chassis changes too.

**H2. Settings that earlier tests rejected are still on.**
- [ext] The quad V3 tests rejected 0.8 bear leverage (blueprint §10). It is still the default in quad and in all three CSM books (E2 above measures `leverage_bear=0.6` as better).
- Combining raw Sharpe legs by simple averaging (quad, absolute) lets the longer leg dominate, because its returns aren't annualised. Elendel and residual sum z-scores instead.

**H3. Measured wins worth carrying into new books [ext]:**
- re-entry after *profitable* stops (cooldown 0, or the loss-scaled cooldown);
- the rebalance exit buffer and the swap gap;
- removing the chandelier: median hold 9 → 28 days, win rate +8 points, turnover halved;
- liquid-MF cash parking (about +5 points in quad V3);
- `min_periods=21` on the liquidity window: IC t 1.03 → 3.87;
- residual momentum's **bad-data guard**: a > 150% daily move that doesn't revert within 5 days excludes the name. It is a stronger version of B6.
- Dropping residual's illiquidity/low-price tilts: 93% of that config's return came from one data glitch.

**H4. Live-parity gaps in csm_absolute (code):**
- Its live `get_exit_signals` defaults to 15%/20% stops, but production backtests use 8%/12%.
- The re-entry cooldown isn't mirrored live.
- It imports a limit-order module that is not in this repo.
- Its wishlist/monitor helpers compute the signal with a different formula (8-month window, vol not annualised, 1.5 bull leverage).

**H5. csm_quad's live universe choice may rest on bad data [ext].** The 500–1000 band shows 37.3% CAGR and −18.9% MaxDD over 10 years, but a Sharpe of only 0.70. That combination usually means an unadjusted price jump inflated volatility. Re-check the band on a cleaned panel (`sc1_strategy.session_keep_mask` + the bad-data guard) before trusting it.

**H6. Holding period vs signal horizon.**
- Residual momentum's IC is still rising at 12 months (0.053 / 0.095 / 0.132 / 0.147 at 1 / 3 / 6 / 12 months [ext]), yet it rebalances monthly. Its holds are already long (about 4 months), so it is the natural book to test the C2 tranche idea on.
- csm_absolute re-ranks quarterly because its IC peaks at 3 months, but its 8%/12% stops cut the average hold to about 10 days. In practice it is a short-horizon book (see `SHORT_TERM_MOMENTUM_SIGNALS.md` §9).
- csm_quad: IS 2003–12 Sharpe 2.36 → OOS 2013–25 Sharpe 1.84 (78% of IS, docstring). That is the only out-of-sample record in this family, and a fair prior for how much the CSM books will shrink on the A1 holdout.


### I. HR breakout (`hr_breakout_v2.py`, `run_hr_breakout_v2.py`)

**What it does today [code, M].** Horizontal-resistance breakout (cluster of ≥3 local highs within 1.5%, close 0.5% above), top-500 liquidity, EMA 50/150/200 stack, relative strength in the top 25%, benchmark-trend gate. Up to 10 names, 1% risk-based sizing capped at 15%, stops at −15% from entry and −15% from peak plus a 1.5–2.5× ATR chandelier (clamped 12–30% from peak), 45-day time stop, 20-day cooldown.

| 2005–2026, 0.3% cost | Engine | Re-booked [R] |
|---|---|---|
| CAGR / Sharpe / MaxDD | 43.6% / 1.87 / −28.1% | **12.2% / 0.63 / −51.0%** |
| 2005–15 (the book's own in-sample window) | 51.1% | 17.5% |
| 2014–26 | 45.0% | 12.8% |

- 1,237 of 1,320 trades (94%) exit on a stop at an average +4.1% (engine view); those trades had peaked at **+19.9%** on average and 41% had been +15% or more. Time stops: 72 trades at −5.9%.
- Exposure 78% in-sample, 85% since: about 8 names. Idle cash earns **0%** (the runner passes `risk_free_rate=0`).
- The top 10 trades make 26% of gross profit, so the book is not one-trade dependent.
- **Config drift:** 7 parameters differ between the class defaults and what the runner actually uses (universe 1000 vs 500, RS top 30% vs 25%, position cap 20% vs 15%, chandelier 3.0 vs 2.5, entry/peak stops 10% vs 15% each, slippage 0.3% vs 0). Decide which set is live.

**I1. Cash yield (adopt).** `cash_yield` option added to the backtest (default = old behaviour). Re-booked in-sample CAGR 17.5% → 19.1%, MaxDD −38.6% → −36.0%.

**I2. Tighter stops do not help (reverses the engine result).** One change at a time on top of I1, re-booked, 2005–15:

| Change | Engine CAGR / Calmar | Re-booked CAGR / Sharpe / Calmar |
|---|---|---|
| I1 only | 53.1% / 2.76 | 19.1% / 0.89 / 0.53 |
| Peak stop 10% | 54.8% / 3.13 | 14.9% / 0.73 / 0.41 |
| Entry stop 10% | 58.3% / 3.66 | 15.7% / 0.77 / 0.51 |
| Chandelier clamp-min 8% | 43.1% / 1.81 | 4.4% / 0.31 / 0.08 |
| Max positions 12 / 15 | 48.8% / 47.0% | 15.5% / 15.3% |
| Risk 0.75% per trade | 51.5% / 3.32 | 19.2% / **0.96** / 0.62 |
| Risk 1.25% per trade | 53.2% / 2.62 | 18.9% / 0.86 / 0.50 |
| Cooldown 40 days | 53.8% | 19.9% / 0.92 / 0.55 |
| Min-hold 10 / time stop 30d | 56.5% / 51.3% | 17.2% / 17.1% |
| Universe top-1000 | 56.9% / 2.42 | 16.5% / 0.78 / 0.36 |

The engine would have had us tighten stops (+7 pp CAGR). Booked consistently the same change *loses* 3–4 pp. Only I1, a lower risk setting and a longer cooldown are at or above I1, and they are within noise of it.

**I3. Ideas not yet tested [H].**
- **Wider** stops (entry/peak 20%) and no chandelier, since tighter ones now look harmful: needs the same re-booked sweep.
- A real `stop_fill_mode` (breach → next open) in the HR loop. 94% of exits are stops, so the fill model *is* this book's result.
- Re-booked cost sweep (engine view: 43.6% → 37.9% → 30.8% at 0.3 / 0.6 / 1.0%; turnover 7×).
- Make the HR runner and class defaults agree, then freeze.

### J. VCP breakout (`vcp_v4.py`, `run_vcp_v4.py`)

**What it does today [code, M].** Minervini trend template + 4 volatility-contraction criteria, **liquidity rank 500–1000** (the runner; class default is 1–1000), 1-year RS ≥ 75th percentile, 10 names, risk-based sizing 2–20% with a 10%-of-ADV cap, hard stop −15%, ATR trail activated at +10%, stale exit after 60 days below +5%, 30-day lockout.

| 2003–2026, 0.3% cost | Engine | Re-booked [R] |
|---|---|---|
| 2003–13 | 20.4% / Sharpe 1.92 / MaxDD −16.7% | **9.2% / 0.85 / −31.4%** |
| 2005–13 / 2014–26 | 25.5% / 47.5% | 11.4% / 15.0% |
| Whole period | 34.2% / 2.13 | **12.3% / 0.82 / −40.0%** |

- Exits (engine view): TRAIL_STOP 55% at +15.8% (97% win), HARD_STOP 28% at −15.3%, STALE 17% at −2.3%. Trail-stopped trades peaked at +22.5%, i.e. the trail gives back about a third.
- **Barely invested early on:** 27% exposure and 2.4 names in 2003–13 (the 500–1000 band yields few signals), 69% and 6.2 names since 2014. Idle cash earns 0%, so cash yield matters most here.
- **Sizing and exit disagree [code]:** the position is sized off the tighter of the 15% hard stop and a 7–10% ATR distance, but the actual exit is the flat 15% hard stop. A stopped-out trade costs weight × 15.3% ≈ **1.7% of NAV**, not the intended 1%. Sizing off the real worst case (15%) would cut position sizes to about 6.7%; tightening the hard stop to the sizing distance is the other fix.

**J1. In-sample sweep, re-booked [R], 2003–13, one change on top of cash yield** (holdout under honest booking **not yet run**):

| Change | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| Base (no cash yield) | 9.2% | 0.85 | −31.4% | 0.30 |
| + cash yield (6.5%) | 13.9% | 1.25 | −27.8% | 0.50 |
| + hard stop 12% | 15.4% | 1.46 | −19.6% | 0.79 |
| + hard stop 10% / 8% | 13.9% / 13.2% | 1.36 / 1.31 | −18.6% / −16.6% | 0.75 / 0.80 |
| + stale exit 40 days | **16.7%** | **1.51** | −19.1% | **0.88** |
| + risk 0.75% per trade | 15.2% | 1.48 | −20.0% | 0.76 |
| + max positions 15 | 15.1% | 1.38 | −28.4% | 0.53 |
| + trail activation 7% / 15% | 14.4% / 12.7% | 1.29 / 1.15 | −26.9% / −30.2% | 0.53 / 0.42 |
| + universe rank 1–1000 | 13.0% | 0.81 | −28.1% | 0.46 |
| + universe rank 250–1000 | 20.0% | 1.35 | −28.2% | 0.71 |

- Unlike HR, VCP's tighter hard stop genuinely helps (it removes the sizing/exit mismatch above), so J2 is not an engine artefact.
- **Universe widening is the cost trap** (A3, B4): the 250–1000 band's 20% CAGR is the sort of gain that disappears at higher costs; rank 1–1000 is worse than the band the runner uses.
- Candidate package to freeze for a one-shot 2014–26 holdout: cash yield + hard stop 12% + stale exit 40 days. Not adopted in code yet.

**J2. Other ideas [H].** Cap the weight at the 15%-stop risk budget (6.7%); make the 10%-of-ADV cap bind by testing at the capital actually deployed (at ₹1 lakh it never binds, A3/B5); re-booked cost sweep; align runner and class defaults (8 parameters differ: hard stop 8% vs 15%, trail 7% vs 5%, stale 20d vs 60d, min-hold 5 vs 15, RS 70 vs 75, band 1 vs 500, ATR trail mult 3.0 vs 2.5, stale return 0% vs 5%).

### K. csm_quad and the other older books (`Old_momentum_strategies/`)

**K1. csm_quad is the Zenith chassis with a plain 6m/12m raw-return signal [code]**, so the Zenith results transfer directly. Re-booked [R]:

| csm_quad (repo version, top-1000) | 2003–13 | 2014–26 |
|---|---|---|
| Engine CAGR / Sharpe | 31.2% / 2.31 | 29.6% / 1.98 |
| Re-booked CAGR / Sharpe / MaxDD | **10.0% / 0.77 / −36.8%** | **7.1% / 0.53 / −47.0%** |
| + Zenith package (cash, stop 10%, flat cooldown, gate, bear 0.6) | 13.2% / 1.08 / −27.2% | 8.3% / 0.64 / −36.3% |
| Breach → next-open exits instead (re-booked) | 20.0% / 1.51 | 9.7% / 0.73 |

- The package helps quad about as it helped Zenith: a few points of CAGR, a lot of drawdown. Port it, but the weakest piece is still the signal: 7% a year since 2014 is not a book to scale (live csm_quad uses the 500–1000 band; H5 says re-check that band on a cleaned panel).
- Stop share 65% and 2,489 trades in 23 years: the same stop-driven profile as Zenith.

**K2. csm_absolute [code, ext].** Quarterly re-rank, 25 names, 12% cap, stops −8% / −12% plus a 2×ATR chandelier, sells everything when the benchmark is below its SMA-200. Not re-run here: `csm_absolute_backtest.py` needs `limit_ordder_manager`, which is not in the repo, and its booking problem is already documented (+38% → −16%, C0). Everything in §H4 still applies. Cash yield is the one change not in doubt: the runner already sets `use_liquid_mf=True` with a **0%** rate, i.e. it is switched on but earns nothing.

**K3. Residual momentum [code, ext].** −25% from peak, sold next open, so exit booking is consistent by construction (not re-verified here). It is the natural book for the staggered-tranche test (C2, H6) and the only older book that is not stop-driven. Not re-run.

### L. Putting the books together [R]

Re-booked daily returns, 2005-01 → 2026-09, each book at its own 0.3% cost, combined with fixed weights and daily rebalancing (no extra cost for the rebalancing):

| Correlation | Zenith (new) | csm_quad | HR | VCP |
|---|---|---|---|---|
| Zenith (new) | 1.00 | 0.77 | 0.62 | 0.46 |
| csm_quad | | 1.00 | 0.60 | 0.46 |
| HR | | | 1.00 | 0.42 |

| Combination (equal weight) | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| Zenith alone | 12.2% | 0.97 | −31.7% | 0.39 |
| Zenith + VCP | **13.2%** | **1.05** | **−30.9%** | **0.43** |
| Zenith + HR | 12.7% | 0.82 | −35.6% | 0.36 |
| Zenith + HR + VCP | 13.3% | 0.95 | −34.5% | 0.39 |
| Zenith + quad + HR + VCP | 11.9% | 0.90 | −37.4% | 0.32 |

- HR and VCP are materially less correlated with Zenith (0.62, 0.46) than csm_quad is (0.77). This is the diversification the CSM books could not offer each other (D5, H1).
- **Only Zenith + VCP improves every metric.** HR's −51% drawdown drags any mix, and adding the correlated csm_quad dilutes it.
- These are small gains from small, unconfirmed books; treat as direction, not as an allocation. The honest portfolio to build is the one after the booking is fixed and HR/VCP have their holdouts.

---

## 3. Prioritised roadmap

Revised 2026-10-05 after the re-booking finding (§0b) and the extension to HR, VCP and the older books.

| Step | What | Expected result | Effort |
|---|---|---|---|
| 0. Settle the booking | Decide whether the engines get fixed to book exit-day and entry-day moves at the real fills (`IDEAS_BACKLOG.md` C0/C1). Until then report engine and re-booked numbers side by side (`nextopen_estimator.py`). | Every absolute number shifts: books that read 25–48% a year read **7–16%**. Rankings of changes that alter the stop count change too. | Low to run, high impact |
| 1. Mechanical fixes | D1 cash yield in **every** book (done for Zenith's default and as an option in HR/VCP); A3 cost sensitivity and liquidity cap; A6 survivorship note | Cash yield alone: Zenith +2.6 pp, HR +1.6 pp, VCP **+4.7 pp** (re-booked, in-sample) | Low |
| 2. Package that survived honest booking | **Zenith (done):** cash, stop −10%, flat cooldown, gate, bear 0.6. 2003–13 re-booked 12.5% → 17.1% CAGR; 2014–26 holdout 8.0% → 9.7% (resting) / 11.4% → 13.9% (next-open). Next: port to csm_quad (+3 pp in-sample, +1 pp holdout) and Meridian/Elendel with their own holdouts | Modest and real; **do not** expect the engine-booked 28% → 33% | Medium |
| 3. Book-specific candidates, one-shot holdout each | VCP: hard stop 12% + stale exit 40d (+ cash). HR: **no stop changes**; test wider stops and a next-open fill model first. csm_absolute / residual: not before C0 | VCP re-booked in-sample 9.2% → 16.7% CAGR (candidate only) | Medium |
| 4. Test the remaining new ideas | Entry-spike filters (B2/C1, already closed for momentum books), high-volatility exclusion (B3, **rejected on Zenith**), staggered tranches (C2, untested), sector cap (D4, **rejected on Zenith**), own-volatility scaler (E1, **already in the code**) | C2 is the one open idea with a clear mechanism | Medium-high |
| 5. Run them as a portfolio | Zenith + VCP is the only mix that improved every metric on re-booked numbers (§L); cap single-name exposure across books (D5); SC1 (G1); live monitoring (E5) | Small, unconfirmed gains; build after steps 0–3 | Medium |

## 4. Things measured to make results worse (avoid)

*Engine-booked, 2026-10-01. The `stop_fill_mode='next_open'` row is withdrawn (A4); `use_crash_guard=False` and the looser-stop rows should be re-read on re-booked numbers before relying on them.*

| Change | Measured result (Zenith, 2003–13) |
|---|---|
| `quarterly_entries=True` | CAGR 28.2 → **17.2%**, Calmar 0.93 (idle cash after stops) |
| `use_crystallisation=True` (partial profit-take) | CAGR **14.9%**, MaxDD −25.0%, Calmar 0.59 |
| `stop_fill_mode='next_open'` | CAGR **21.1%**, MaxDD **−29.1%**, Calmar 0.73 |
| `rebalance_exit_buffer_months=0` | CAGR 21.5%, Sharpe 2.03 |
| `use_crash_guard=False` | MaxDD −24.4%, Calmar 1.12 |
| `top_n=20` / `top_n=10` | MaxDD −24.5% / CAGR 20.2% |
| `max_weight_per_stock` 0.07–0.10, risk-budget sizing | Sharpe 2.06–2.10, MaxDD about −24% |
| `use_time_stop=True` | Calmar 1.23 |
| Looser stops (entry −20%, peak −25%) | Calmar 1.19–1.23 |

## 5. Caveats

- **All ablation numbers in §§1–4 are Zenith, 2003–2013, in-sample and engine-booked.** Elendel and Meridian share the chassis, so directions may carry over, but magnitudes need re-running per book, on re-booked numbers.
- **The re-booking is a first-order diagnostic [R].** It uses the engine's own executed weights (constant-weight, daily-rebalanced), so it does not model path-dependent re-entry changes; its main check is that it leaves the already-consistent `next_open` engine nearly unchanged. HR/VCP holdouts under honest booking and a re-booked cost sweep for them are still to do.
- **Selection history.** Zenith's package was chosen from engine-booked in-sample numbers and then confirmed on a one-shot holdout; its re-booked in-sample and holdout results agree on direction. The HR/VCP sweeps in §I–§J were run on re-booked numbers but have not had a holdout; treat them as candidates.
- **Sharpe differences below about 0.3 are within noise** for one 11-year path, and 70 alternatives were tried. Hence A1/A2.
- **Effects interact.** Tighter stops plus a higher price floor plus bear-leverage cuts are not additive. Test packages, not sums.
- **Survivorship and flat costs** make every absolute number an upper bound.
- **Cash yield** assumes a constant 6.5%; real liquid-fund yields varied with the policy rate.

## Sources

- [Han, Zhou & Zhu 2016, stop-loss momentum](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2407199)
- [Barroso & Santa-Clara 2015; Daniel & Moskowitz 2016](https://www.researchgate.net/publication/256017573_Momentum_Has_Its_Moments)
- [Rebalance timing luck / tranching](https://quantpedia.com/the-tranching-dilemma/)
- [Moskowitz & Grinblatt 1999](http://www-stat.wharton.upenn.edu/~steele/Courses/956/Resource/Momentum/MoskowitzGrinblatt99.pdf)
- [Sullivan, Timmermann & White 1999, data snooping](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00163)
- [Nifty200 Momentum 30 methodology](https://www.niftyindices.com/docs/default-source/indices/nifty200-momentum-30/nifty200_momentum_30_index_whitepaper_sep_20.pdf)

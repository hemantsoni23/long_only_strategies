# CSM Aegis — Independent Review and Improvement Plan

> Historical review note: this document predates the two-file consolidation and the decision to exclude idle-cash yield from strategy results. The current production configuration and workflow are in `README.md`.

**Review date:** 2026-10-23
**Scope:** `csm_aegis/` strategy, backtest engine, runner, parity test, outputs, cached data.
**Status of the book:** research output, paper-trade candidate, not live-validated.
**Code changes made:** none. This is a review + plan.

---

## 1. Bottom line

CSM Aegis is a genuinely good piece of research. The core idea is sound, the faithful-booking engine is a real improvement over the older research scripts, the pre-registration discipline is unusually good, and the parity test actually passes. The headline backtest is **26.9% CAGR / 1.85 Sharpe / -28% MaxDD** (live preset `v1.2_liquid`, 2005-01 to 2026-07).

But the number you should **plan** with is lower:

| Basis | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| Headline `v1.2_liquid` (backtest, cash 6.5%) | 26.9% | 1.85 | -28% |
| Conservative `v1.2` (cash 0%) | 24.2% | 1.69 | -29% |
| **Own out-of-sample split (select 2005-12, test 2013-26)** | **19.6%** | **1.40** | **-29%** |
| Random picks through identical wrapper (placebo) | 14.9% | 0.96 | — |
| Nifty 500 price | 12.6% | 0.69 | -64% |
| Live preset at Rs 1cr / 5cr / 25cr capacity | 19.6% / 15.2% / 10.8% | — | — |

**Realistic planning range: 15-20% CAGR, Sharpe ~1.3-1.5, MaxDD -30% to -35%, at Rs 1-5 crore, before tax.** Anything above that is the backtest, not the forward expectation.

The two things that must be fixed before paper trading are **not signal ideas** — they are **data integrity** and **live order-sheet safety**:

1. Corporate actions and bad prints are handled by silently zeroing two days of returns and leaving price levels unadjusted. This contaminates trade stats, several level-based filters, and the risk picture.
2. The live workflow prints 6.67% per name for 20 names (~133% gross), while the backtest actually fills ~5% per name. Following the README literally would create unintended leverage.

Fix those, add concentration caps, and the book is a credible paper-trade candidate. Chasing more signal work before those fixes is premature.

---

## 2. What the strategy actually does

| Block | Rule | Comment |
|---|---|---|
| Universe | price ≥ 20; 63d rupee-volume rank 1-1000; ≤5 circuit-locked sessions in 63d; close > SMA200; remove worst 20% by M3 (largest 1-day spike in last month) | ~200-600 names pass; only 82 in the 2008 crash. Sensible. |
| Signal | `score = z(R1) + z(-Ulcer252)` | R1 = residual momentum (daily return minus lagged 252d beta × equal-weight market, summed t-252..t-21, divided by vol). Ulcer = RMS drawdown from rolling 252d closing high. |
| Selection | top 20 at month-end; hold until rank > 40 or out of pool | Hysteresis is doing real work; 522 of 1,336 exits are rank exits. |
| Entry filters | skip if >25% above SMA50; no entries while 63d market vol > expanding 85th pct | Extension filter rejects only 89 candidates; vol-state gate rejects 50. Both are marginal. |
| Market gate | equal-weight market ≤ 120d average → exit all, no entries until recovery | The single most valuable wrapper component. Kept 2008 at -10.6% vs -57%. |
| Exits | -15% from entry, -20% from peak close, time stop (45d and < -5%), rank/pool, market gate; close fills next close | Stops buy return, not safety (removing them: 15.6% CAGR, same Sharpe, -18% DD). |
| Sizing | `1% risk / 15% stop` → 6.67%, clamp 3-8%, gross ≤ 100% | Degenerate: flat 15% stop means every name gets the same 6.67%. Not actually risk-based. |
| Execution | decide close, fill next close, 0.3%/leg, optional 5%-ADV cap, idle cash at 6.5% | Close fills justified by the broken `open` field. |

**Key structural read:** most of the return comes from the **pool + market gate + stops + cash yield**, not from stock selection. Random picks through the same wrapper earn 14.9%; the selector adds ~9 points; the wrapper adds the rest. The selector's top-20 excess over the pool is small and only significant at 3 months.

---

## 3. Performance decomposition

### 3.1 What is verified

| Metric | Value | Note |
|---|---|---|
| Period | 2005-01-03 → 2026-07-17 | 2026 is a partial month in the data |
| CAGR | 26.9% | live preset, cash 6.5% |
| Sharpe | 1.85 | per README (mean-based); CAGR/vol ≈ 2.0 |
| MaxDD | -28.0% | worst intra-year -28.0% in 2016 |
| Trades | 1,336 | 51.6% win rate, payoff 2.76, profit factor 3.00 |
| Avg hold | ~75 days | turnover 6.1x/yr |
| Avg gross exposure | 65% over all days; 94% on invested days | fully in cash 31% of days (2005+; the raw daily log starts in 2003 warmup, where the cash share is higher) |
| Positions | median 18, max 20 | rarely fully invested even when "invested" |

### 3.2 Where the return comes from

- **Cash yield is not a rounding error.** Idle cash at 6.5% contributes roughly 2.7 points of CAGR and ~0.16 Sharpe. It also creates the repeated exactly-`+0.5%` months in 2025-26. Report the equity sleeve separately from the cash sleeve.
- **The first half is much stronger than the second.** 2005-2012: 35.2% CAGR, -18% DD. 2013-2026: 22.2% CAGR, -28% DD. Be careful comparing Sharpe across halves (convention-dependent), but the CAGR/DD gap is real.
- **Beat rate is good, not overwhelming.** 16 of 22 calendar years beat Nifty 500; average excess +13.0 points, median +13.6. Losses vs benchmark in 2006, 2009, 2016, 2019, 2022, 2025.
- **The recent regime is flat.** 2025: +0.1% (index +6.7%); 2026 YTD: +1.0% (index -2.2%). 2026 is ~90% fully in cash. Almost all of the recent positive return is cash yield, not equity.
- **Beta is low.** ~0.34-0.38 vs Nifty 500, correlation ~0.49-0.59. Simple CAPM alpha ~18-19%/yr vs Nifty 500 and Smallcap 250. The book is not a high-beta index proxy; it is a low-exposure, timing-heavy book.

### 3.3 Signal evidence

| Horizon | IC | ICIR | NW-t | Top-20 excess over pool | NW-t |
|---|---|---|---|---|---|
| 1m | +0.051 | 0.350 | 5.60 | +0.3% | 1.53 |
| 3m | +0.060 | 0.389 | 4.37 | +1.1% | 2.06 |
| 6m | +0.064 | 0.411 | 3.44 | +1.3% | 1.24 |
| 12m | +0.059 | 0.375 | 2.32 | +1.4% | 0.64 |

3m IC by 36-month chunk: 2005-08 +0.082 (t 3.0); 2008-11 +0.043 (0.9); 2011-14 +0.097 (2.2); 2014-17 +0.066 (1.8); 2017-20 +0.092 (2.6); **2020-23 -0.008 (-0.27)**; 2023-26 +0.051 (2.6).

**Reading:** the composite is a real, positive, 6-12 month signal in six of seven chunks, but the selector's *marginal* contribution is modest and not significant at 12m. One chunk is flat. The strategy has not shown a structural step-down, but it also has not shown that selection alone is robust enough to carry the book. Treat the wrapper and the timing gate as first-class contributors, not as decoration.

### 3.4 Is it capacity-constrained?

Yes, materially. With each position capped at 5% of 63-day rupee volume:

| Capital | `v1.2` CAGR | Live preset CAGR |
|---|---|---|
| Rs 1 crore | 17.0% | 19.6% |
| Rs 5 crore | 12.7% | 15.2% |
| Rs 25 crore | 7.6% | 10.8% |

The account compounds, so the cap binds harder over time. **Plan for Rs 1-5 crore.** At Rs 25 crore, the capacity cap eats most of the edge.

---

## 4. Findings

Severity: **P0** = fix before any paper trade; **P1** = fix before scaling / needed for honest evaluation; **P2** = engineering hygiene.

### P0-1. Corporate actions are handled by silently deleting returns

**What the code does** (`csm_aegis_strategy.py`, `load_data`): if a close-to-close move is outside `[-40%, +300%]`, the loader sets **all of O/H/L/C for that day to NaN**. Then `RET = ret.fillna(0.0)`.

**Why it matters:**

- A masked day's return becomes **0**.
- Because the masked close is NaN, the **next day's return is also NaN → 0**.
- So a genuine -45% crash is recorded as two flat days. Risk is understated. A genuine +350% squeeze is also flattened.
- Unadjusted splits/bonuses are "implicitly adjusted" by zeroing the jump. The *return* is often economically right, but **price levels remain unadjusted for up to 252 days**.
- Any level-based or level-derived signal then compares prices across the split: `SMA200`, `SMA50` extension, `Ulcer252` (drawdown from rolling high), 52-week-high proximity (A1 in `v1.2_high_return`), and the `price >= 20` floor. A 1:10 split can make a post-split winner look like a sub-Rs-20 penny stock or a broken-down chart.
- A raw scan finds **~900 masked close-to-close events since 2005 across ~550 symbols (~10% of the file set)**, with roughly 3:1 down vs up. Some are bad prints, some are splits, some are genuine crashes. The code cannot tell them apart.

**Concrete example:** `FELDVR`, entry 2016-05-02 at 129.15, exit 2016-05-13 at 13.75. The trade log records **-89.4%**. The per-name equity path records **+7.3%**, because 13.75 × 10 ≈ 137.5 — a 10:1 split. The equity is right; the trade log is wrong.

**Fix:**

1. Build a proper **adjusted-close panel** from split/bonus factors (or detect ratio-like jumps and back-adjust all prior prices).
2. Keep a separate **bad-print flag** for non-ratio anomalies; do not conflate a 1:10 split with a -90% crash.
3. Never `fillna(0)` a masked return silently. Either impute from an adjusted series, or drop the name for the affected window and log it.
4. Emit a **data audit table** (date, symbol, raw move, classified as split/bonus/bad print/crash, action taken). Review it once, then version it.

**Acceptance:** zero level-series discontinuities across known splits; every masked event classified; trade PnL and equity PnL reconcile.

### P0-2. Trade log and equity path disagree

25 trades differ by more than 5 percentage points between `PnL_Pct` in the trade log and the return implied by the per-name return series the equity engine uses. `FELDVR` is the extreme case (see above: -89.4% in the trade log vs **+7.3%** on the per-name equity path). The net NAV effect is small relative to gross PnL, but:

- win rate, payoff, average win, average loss, and tail statistics are contaminated;
- "average win +25.4%, average loss -9.2%, profit factor 3.00" should not be trusted until recomputed from the same series used for equity;
- any per-trade risk analysis (MAE/MFE, stop effectiveness) inherits the error.

**Fix:** compute trade PnL from the same masked/adjusted return series the equity uses (or from adjusted prices), and add a reconciliation assertion: `sum(weight_i × trade_return_i) ≈ equity contribution` within tolerance. Add this to the parity test.

**Acceptance:** no trade differs by >0.5 points from its equity-implied return; reconciliation residual <0.1% of NAV per trade.

### P0-3. The live order sheet creates unintended leverage

The latest-picks table prints `weight = 0.067` for all 20 names. That is the **pre-gross-cap, pre-capacity** target. In the actual backtest:

- median filled weight is **4.98%**;
- ~63% of entries fill below 5%, ~20% below 4.5%, 5.5% below 4% (min 1.8%);
- only **1.1%** of entries get the full 6.67%.

Twenty names at the printed 6.67% = **133% gross**. Following the README's "buy the top 20" workflow literally would lever the book. Separately, `GROSS_CAP_SCALED` logs **1,321 entries as "rejects"** even though many were partially bought, so the reject log misleads you about what the engine did. And `w_lo = 3%` is not enforced after the gross-cap scale-down, which is how you get 1.8% positions.

**Fix:**

1. Print **post-cap weights that sum to ≤ 100%** (plus a cash line). Keep a separate `target_weight` column for transparency.
2. Separate **full reject** from **partial fill** in the reject log.
3. Enforce `w_lo` after scaling, or explicitly allow dust and label it.
4. Add an assertion before order generation: `sum(weights) ≤ max_gross + epsilon`, and a hard fail if not.
5. Document the cash buffer (e.g., 2-5%) so fills/slippage don't force leverage.

**Acceptance:** printed weights sum ≤ 100%; a simulated order sheet produces no leverage; reject log distinguishes reject vs scale.

### P0-4. No stale-price / delisting exit

`check_stop_exit` returns `None` when close is non-finite. A suspended, delisted, or data-missing name can therefore **freeze at its last mark indefinitely**. In the backtest this is partly hidden by the survivorship-biased universe; in live trading it is a real capital trap.

**Fix:**

1. Staleness rule: if no valid close for N sessions (e.g., 10), force an exit at the last valid close with a haircut, or write the position down and flag it.
2. Add a delisting/suspension calendar if one can be sourced; otherwise treat missing data as a risk event, not a flat price.
3. Add a live reconciliation that flags any holding with no fresh price.

**Acceptance:** no position can remain marked at an unchanged stale price for >10 sessions without an explicit flag/exit.

### P1-1. No sector, industry, or cap limits

The latest top-20 is concentrated:

| Sector | Count | Industry detail |
|---|---|---|
| Healthcare | 5 | all 5 in "Drug Manufacturers - Specialty & Generic" |
| Industrials | 5 | 4 in "Specialty Industrial Machinery" |
| Financials | 3 | 2 regional banks |
| Consumer Cyclical | 3 | 3 auto parts |
| Consumer Defensive | 2 | household products |
| Technology | 1 | electronic components |
| Basic Materials | 1 | aluminum |

**50% of the book sits in two sectors; 25% in a single industry.** Cap mix is 8 Large / 8 Mid / 4 Small. This is a single-factor shock waiting to happen, and it is not tested anywhere in the report. `instruments_clean.csv` already has `Cap`, `Sector_clean`, `Industry_clean` — the data is there.

**Fix:** add configurable caps (e.g., max 25% sector, max 15% industry, max 40% small-cap, max 10% single name) as a first-class selection constraint, then pre-register the test. Expect a small CAGR give-up for a lower DD and better robustness. Do **not** adopt on the strength of the latest book alone — test it across the full history.

### P1-2. Benchmark is wrong for the book

The benchmark is **Nifty 500 price only**. The book is small/mid-cap, holds cash 31-37% of the time, and has beta ~0.35. That comparison flatters the strategy in falling markets and penalizes it in cash-heavy periods.

**Fix:** report a benchmark suite:

- Nifty 500 **Total Return**;
- Nifty Smallcap 250 TR;
- a **blended** benchmark (e.g., 65% Nifty 500 TR + 35% cash at the actual cash yield);
- beta-adjusted alpha, up-capture, down-capture, and information ratio.

### P1-3. Capacity model is too crude for the stated AUM

The 5%-of-ADV cap plus 0.3%/leg is a reasonable first pass, but it ignores:

- market impact (square-root or Almgren-style);
- participation-rate limits and multi-day execution;
- circuit-locked sessions (the universe already screens them, but exits can still be trapped);
- the fact that the cap binds harder as the account compounds.

At Rs 5 crore the CAGR is already 12.7% (`v1.2`) / 15.2% (live preset). That is the real planning constraint, not the 26.9% headline.

**Fix:** add a square-root impact model calibrated to Indian small/mid-caps, a participation cap, circuit-aware fill assumptions, and a capacity report by liquidity bucket. Re-run the stress table and publish the AUM where Sharpe falls below ~1.0.

### P1-4. Cash-yield assumption and the equity/cash split

6.5% flat idle-cash yield is applied across 2005-2026. Actual liquid-fund yields were ~3.5% in 2020-21 and 7-9% in 2007-08/2011-13. Taxes on the income are ignored. More importantly, **the recent "flat" performance is mostly cash yield** — the equity sleeve may be flat-to-negative since Jan 2025.

**Fix:** use a time-varying cash-yield series; report the equity sleeve and cash sleeve separately; show pre- and after-tax returns. Do not let cash yield mask a weak equity signal in monitoring.

### P1-5. The market gate is binary and whipsaw-prone

Exit-all at month-end when the equal-weight market ≤ 120d average; re-enter when it recovers. This is the most valuable component, but 0/100 de-risking creates:

- whipsaw risk around the threshold (exit, then re-enter a month later);
- cash drag in choppy markets;
- a single-parameter dependence (120d). The report says 100-120 is flat and 150+ is worse, which is reassuring, but the gate is still a timing bet.

**Fix (test, don't assume):**

- hysteresis: exit at 120d, re-enter at a faster average (e.g., 60d) or with a buffer;
- partial de-risking (e.g., scale gross to 50%) instead of 0/100;
- a second, slower trend filter on the index for confirmation.

### P1-6. Non-earning components are still switched on

The report's own ablations say:

- removing the **vol-state gate**: 25.1% CAGR / 1.73 Sharpe (vs 24.2/1.69) — it does not earn its place, and 2025-26 improves to +4.8%;
- the **time stop** is neutral;
- **ATR stops** lower MaxDD to -26.5% with the same Sharpe.

Keeping these "because they might help" is a form of optionality that costs turnover and complexity. Either pre-register a test that shows a benefit, or remove them and simplify.

### P1-7. Multiple-testing / walk-forward accounting

The report tests many variants (presets, gate windows, stops, universe bands, filters, ablations). The noise floor is documented (±0.05 Sharpe, ±0.07 Calmar, ±2 points MaxDD), which is good. But there is no **deflated Sharpe ratio** or explicit trial count. With this many looks, the headline Sharpe is optimistic by an unknown amount.

**Fix:** record every variant tested; compute a deflated Sharpe (or at least a haircut) using the trial count; run a purged/embargoed walk-forward with the design choices frozen at each step.

### P2. Engineering and reproducibility

| Issue | Location | Fix |
|---|---|---|
| Hardcoded absolute `DATA_FOLDER` | `run_csm_aegis_backtest.py:30` | env var / config file with a documented default |
| `--set` uses `eval` | `run_csm_aegis_backtest.py` `_parse_set` | parse with `ast.literal_eval`, whitelist keys/types |
| `save_outputs` reads global `ARGS` | runner | pass `tag`/config explicitly |
| No `requirements.txt` / `pyproject.toml`, no CI | repo | pin pandas/numpy/pyarrow/matplotlib; add a smoke test |
| Parity test depends on `../decay_check` + 154MB pickles | `test_parity.py` | vendor small fixtures or generate them; make the test hermetic |
| `output/` and `.cache/` not ignored | `.gitignore` | add them; commit code + docs |
| `csm_aegis/` entirely untracked | git | commit it; otherwise the review/plan is not reproducible |
| No tests for corporate actions, stale prices, gross cap, weight sum | tests | add focused unit tests; these are the P0s |
| Data cut at 2026-07-17 due to `min_names=2000` | loader | make the endpoint explicit; warn on partial month |
| 20 weekend rows in the calendar; 2.34% interior NaNs | data | add a calendar/NaN audit |

---

## 5. Improvement plan

Order matters. Do not start Phase 3 before Phase 0-1.

### Phase 0 — Truth in the numbers (1-3 days)

**Goal:** make the backtest and the order sheet describe the same book.

1. Build an adjusted-price panel; classify every masked event.
2. Recompute trade PnL from the equity return series; add reconciliation assertions.
3. Fix the order sheet: post-cap weights summing ≤100%; target vs filled; reject vs scale.
4. Add a stale-price exit and a missing-price flag.
5. Add a data audit report (masked events, splits, bad prints, NaNs, calendar).

**Exit criteria:** zero trade/equity mismatches >0.5pt; printed weights sum ≤100%; every masked event classified; no frozen positions.

### Phase 1 — Paper-trading harness (1 week)

**Goal:** prove the live path, not the backtest.

1. Generate a daily order sheet from the same code path used by the backtest.
2. Paper-trade 20-40 sessions; record intended vs filled price, weight, slippage, rejects.
3. Reconcile daily: holdings, cash, gross, NAV.
4. Compare paper NAV to a shadow backtest run on the same dates.

**Exit criteria:** tracking error <1 point over 6 months; no unintended leverage; slippage within the 0.3%/leg assumption or explicitly re-estimated.

### Phase 2 — Portfolio construction (1-2 weeks)

**Goal:** reduce concentration and fragility without destroying the edge.

1. Add sector/industry/cap caps as parameters.
2. Pre-register the test (see §6) and evaluate on the full history, both halves, and the last two chunks.
3. Test gate hysteresis / partial de-risking.
4. Add the benchmark suite (TR, smallcap, blended, beta-adjusted).
5. Test staggered rebalancing (e.g., 4 weekly tranches per month) to reduce timing and impact.

**Expected trade-off:** modest CAGR give-up (0-2 points) for lower DD and better tail behavior. Reject if Sharpe/Calmar regress beyond the noise floor.

### Phase 3 — Robustness and honest evaluation (2-4 weeks)

1. Purged/embargoed walk-forward with frozen design choices.
2. Deflated Sharpe / trial-count haircut.
3. Factor attribution (market, size, value, momentum, quality, cash).
4. Square-root impact + participation cap + circuit-aware fills.
5. After-tax returns (STCG/LTCG) and time-varying cash yield.
6. Decide the fate of the vol-state gate and time stop.

### Phase 4 — Optional alpha research (only after 0-3)

Ideas worth testing, in order of prior belief:

1. **Industry-neutral residual momentum** — rank within industry, then cap; addresses the concentration and the 2020-23 flat chunk.
2. **Quality/earnings overlay** — avoid the value-trap tail; test with strict pre-registration.
3. **Volatility-scaled score** — size the signal by residual vol, not just rank it.
4. **Alternate universes** — e.g., top 500 only for capacity, or a smallcap-only variant.

Do not add factors just because they improve the full-sample CAGR. Require out-of-sample and chunk stability.

---

## 6. Pre-registration and acceptance criteria

Use this template for every change (copy into `decay_check/PREREG.md` as a new addendum):

```
Addendum N — <change>
Hypothesis: <one sentence>
Implementation: <exact parameter/code change>
Evaluation window: full history 2005-01..2026-07, plus 2013-2026 OOS
Baseline: v1.2_liquid (26.9 / 1.85 / -28) and v1.2 (24.2 / 1.69 / -29)
Adopt only if ALL of:
  - CAGR gain >= +1.0pt OR MaxDD improvement >= 2pt with CAGR give-up <= 0.5pt
  - Sharpe change >= +0.05 and Calmar not worse than baseline - 0.07
  - positive in both halves (2005-12, 2013-26)
  - positive in the latest two 36m chunks
  - survives 0.6%/leg costs
  - capacity at Rs 5cr not worse than baseline - 1pt
  - no sector/industry/cap breach
Reject if any stability criterion fails, even if full-sample CAGR improves.
```

Add a **trial counter** so the deflated Sharpe can be computed later.

---

## 7. Monitoring and kill rules

Adopt these before paper trading (the README has a draft; make it explicit and dated):

| Trigger | Action |
|---|---|
| Latest 36m chunk IC NW-t < 1 on **two consecutive** quarterly checks | Reduce risk / review |
| Rolling 36m CAGR < 10th percentile of its own history (~13.6%) | Reduce risk / review |
| Live vs paper parity gap > 3 points over 6 months | Stop and reconcile |
| Drawdown > -35% (or >1.5× backtest MaxDD) | De-risk |
| Sector/industry cap breach in the live book | Rebalance |
| Any data-integrity incident (stale price, unclassified split) | Halt new entries until resolved |
| Signal IC negative for 2 consecutive quarters | Cut exposure |

Also monitor: turnover, slippage vs 0.3%/leg, cash yield vs assumption, gross exposure vs target, number of names, and the equity-sleeve return separately from total return.

---

## 8. Realistic expectations

| Scenario | CAGR | Sharpe | MaxDD | Notes |
|---|---|---|---|---|
| Headline backtest | 26.9% | 1.85 | -28% | not a forward estimate |
| OOS split | 19.6% | 1.40 | -29% | best single anchor |
| Rs 1-5cr, after costs, pre-tax | 15-20% | 1.3-1.5 | -30 to -35% | planning range |
| Rs 25cr | ~8-11% | ~1.0 | -17% | capacity-bound |
| After tax (STCG ~20%) | subtract ~2-4 pts | — | — | depends on holding period mix |

Do not underwrite the 27%. The honest pitch is: **a low-beta, cash-aware, small/mid momentum book that historically compounded high-teens to low-20s at Rs 1-5 crore, with ~-30% drawdowns and long flat stretches.** That is still a good strategy — it just isn't a 27% machine.

---

## 9. Quick-win checklist

- [ ] Build adjusted-price panel; classify all masked events (P0-1)
- [ ] Reconcile trade log to equity; fix `PnL_Pct` (P0-2)
- [ ] Print post-cap weights summing ≤100%; add cash line (P0-3)
- [ ] Split reject vs partial-fill in the reject log; enforce `w_lo` post-scale (P0-3)
- [ ] Add stale-price / missing-data exit (P0-4)
- [ ] Add sector/industry/cap caps and pre-register the test (P1-1)
- [ ] Add TR/smallcap/blended benchmarks and beta-adjusted alpha (P1-2)
- [ ] Add impact model + participation cap; publish capacity curve (P1-3)
- [ ] Use time-varying cash yield; report equity vs cash sleeve (P1-4)
- [ ] Test gate hysteresis / partial de-risking (P1-5)
- [ ] Retire or justify the vol-state gate and time stop (P1-6)
- [ ] Add deflated Sharpe / trial count (P1-7)
- [ ] Fix `eval`, hardcoded path, global `ARGS`; add requirements + CI (P2)
- [ ] Commit `csm_aegis/`; ignore `output/` and `.cache/` (P2)

---

## 10. How this review was checked

- Read `README.md`, `CSM_AEGIS_REPORT.md` (all 706 lines), `csm_aegis_strategy.py`, `csm_aegis_backtest.py`, `run_csm_aegis_backtest.py`, `test_parity.py`.
- Inspected `output/` logs, `trade_log_v1_2_liquid.csv`, `daily_log_v1_2_liquid.csv`, `yearly_returns_v1_2_liquid.csv`, `latest_picks_v1_2_liquid.csv`.
- Recomputed: trade stats, weights, exposure, position counts, exit breakdown, yearly beat rate, halves, concentration, sector/cap mix.
- Scanned raw `upstox_data_folder/ohlcv_data/` for masked corporate-action events.
- Ran `test_parity.py`: all 12 configurations `max|diff| 0.00e+00`, live exit parity 0 mismatches, `ALL PARITY TESTS PASSED`.
- Verified the `FELDVR` split example (129.15 → 13.75 ≈ 10:1).

**Caveat:** some figures above come from the repo's own outputs and are not independently recomputed (e.g., Sharpe convention, factor attribution). Where I recomputed, the numbers match the README within rounding. The data is survivorship-biased and absolute return levels are upper bounds.

---

*Research output, not investment advice. Paper-trade before risking capital.*

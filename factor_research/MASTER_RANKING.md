# Master ranking — what to do, in what order, and what to expect

Written 2026-10-06. This replaces the ranking in `IDEA_ROADMAP.md` (built on simplified proxy books) and folds in the momentum-literature work
(`MOMENTUM_LITERATURE_PLAYBOOK.md`), the gold work (`momentum_gold/`) and the new real-engine tests below. `Old_live_strategies/` was not touched.

## 0. Evidence base and how to read the tables

* **Real-engine tests** (`momentum_value/run_improvement_variants.py`, `report_improvements.py`, `blend_check.py`): your actual Elendel / Zenith / Quad classes, unmodified, with only the monthly score
  (or the liquidity-rank band) changed; stops, regimes, vol target, Crash Guard, hysteresis, 0.3% cost as live. Two windows: **2005+** (all data) and **2015+** (the less flattering period).
  "P" = block-bootstrap probability that the variant's daily return beats the same engine without it.
* Variants were scored against the engine **as it is today** (live universe) and against the same universe without the change. Where the two differ, both are shown.
* **Selection caution:** about 39 engine/universe/variant comparisons were run. The ideas ranked at the top were a-priori candidates from earlier stages (residual momentum from the stage 3–4 proxy study,
  the universe effect from stage 17, E/P from the literature) and agree in sign across **both** windows; ones that only worked in one window are marked. Even so, treat the size of each gain as an upper estimate.
* "Planning expectation" = roughly **half of the 2015+ gain** (judgement, not a measurement). Survivorship (only currently listed names) flatters everything, mostly the cheap/small end.

## 1. The ranking

### A. Upgrades to the strategies you already run (best evidence, lowest effort)

| Rank | Change | Real-engine result: 2005+ / 2015+ (Sharpe, CAGR, vs same engine today) | P (2005+ / 2015+) | Planning expectation | Effort / catch |
|---|---|---|---|---|---|
| **1** | **Zenith: add 0.5 × residual-momentum to the score** | Sharpe 1.87 → 2.21 (+0.33), CAGR +6.1 pt / Sharpe 1.48 → 1.98 (+0.50), CAGR +8.8 pt; MaxDD −14.0 → −14.5 / −11.9 → −13.0 | 1.00 / 1.00 | Sharpe +0.2 to +0.25, CAGR +4 to +5 pt, drawdown ~ +1 pt worse | One extra z-term (residual-momentum code already exists in `residual_momentum_strategy.py`). Zenith's A1 leg looks like the weak part: dropping A1 for Q5 alone gives +0.33 / +0.36 Sharpe (P 1.00 / 0.99) — same direction, overlaps with this |
| **2** | **Elendel: add 0.5 × residual-momentum** | Sharpe 1.81 → 2.03 (+0.22), CAGR +4.5 pt / 1.66 → 1.91 (+0.25), +5.1 pt; MaxDD −19.9 → −20.4 / −18.5 → −16.3 | 0.97 / 0.93 | Sharpe +0.10 to +0.13, CAGR +2 to +3 pt | Same one-term change; confirms the proxy-book finding on the real engine |
| **3** | **Idle cash → liquid fund** (Elendel and Quad; check what live does) | Measured earlier on real engines: +2.8 to +3.1 pt CAGR, +0.16 to +0.17 Sharpe, 2.5–2.7 pt shallower max DD (their backtests assume 0%; Zenith already does it) | – (deterministic) | Same, if live is not already sweeping | Zero signal risk. **Open question: do the live Elendel/Quad actually park idle cash in a liquid fund?** |
| **4** | **Zenith: move the universe to liquidity ranks 301–1000** (drop the top-300 megacaps) | Sharpe 1.87 → 2.54 (+0.66), CAGR +9.0 pt / 1.48 → 2.15 (+0.66), +10.5 pt; MaxDD −14.0 → −12.6 | – (universe change; same sign both windows) | Sharpe +0.3 to +0.35, CAGR +4 to +5 pt | Parameter change only. Costs capacity (~₹5–15 cr book at ≤5% of daily value today vs more in the live universe). **Zenith only:** Elendel +0.27 / only +0.08 since 2015; Quad +0.22 / −0.02 |
| 5 | **Value tilt: add 0.5 × earnings yield (E/P)** to Zenith / Quad | Zenith +0.46 Sharpe, +9.5 pt; Quad +0.23 to +0.40, +4 to +7 pt (2019-06→2025-06 only); Elendel ≈ 0 | 0.98–1.00 / 0.91–0.99 | Zenith +3 to +5 pt, Quad +2 to +4 pt | Needs a refreshed quarterly-results feed (current file ends 2024Q4). **Overlaps with #4:** inside the 301–1000 universe E/P adds only +0.13 to +0.23 Sharpe (P 0.84–0.86) |
| 6 | **Quad: tight-range term** (`tight_close_15` replaces/ joins the score) | Swap, live universe: Sharpe 1.67 → 1.90 (+0.23, P 0.79) / 1.42 → 1.62 (+0.20, P 0.73). In 301–1000: +0.34 (P 0.92) / +0.40 (P 0.93), MaxDD −18.5 → −13.9 | 0.79–0.92 | Sharpe +0.1 to +0.15, shallower drawdown | Moderate evidence; the tightness idea is the old "I1". Not helpful for Elendel since 2015 or for Zenith in 301–1000 |
| 7 | **Elendel: tight-range blend, universe 301–1000** | vs same-universe base: +0.20 (P 0.86) / +0.13 (P 0.65); vs Elendel today +0.47 / +0.21 Sharpe | 0.86 / 0.65 | Sharpe +0.05 to +0.10 | Weakest of the "keep" items — half of it is the universe change |

**Do not stack blindly.** Zenith's improvements (Q5-only, residual tilt, tight swap, 301–1000, E/P) all push the same way and overlap. Measured stacking for Zenith: 301–1000 + residual tilt adds a further +0.16 Sharpe / +3.7 pt (P 0.99 / 0.92); 301–1000 + E/P adds +0.13 to +0.23. So do #1, then #4, re-measure, then decide on #5.

**Portfolio view** (equal-weight blend of the three engines, daily returns; idle cash as each engine assumes):

| Blend | CAGR / Sharpe / MaxDD 2005+ | CAGR / Sharpe / MaxDD 2015+ |
|---|---|---|
| Live trio today | 31.5% / 2.01 / −15.9% | 28.6% / 1.69 / −13.6% |
| A: residual tilt on Elendel + Zenith, Quad tight swap | 35.5% / 2.29 / −13.4% | 33.9% / 2.02 / −11.6% |
| D: only Zenith → 301–1000 + residual tilt | 35.6% / 2.28 / −15.4% | 33.3% / 1.96 / −13.1% |
| C: all three on 301–1000, plus the A changes | 39.9% / 2.50 / −13.5% | 35.3% / 2.09 / −12.4% |

Daily-return correlation of every upgraded variant with the live engines is 0.64–0.87 (the live engines are 0.64–0.81 among themselves): **these are upgrades, not new diversifiers**.

### B. New strategies / sleeves (build only after A; none is a free lunch)

| Rank | Idea | Evidence | Planning expectation | Effort / catch |
|---|---|---|---|---|
| **8** | **Post-earnings-drift event sleeve** (surprise AND announcement-return top 30%) | Event study: +3.1% excess per 60 days, t 2.8, positive in both halves; bad-news set −2.6% (t −4.8). Win rate 49% (skew strategy) | Unknown until backtested; its value is a **different return stream** (event-timed). Also gives a bad-news veto for the books | Needs the fundamentals feed + a full event backtest with stops, ≤5% ADV, costs. The only candidate that may really diversify |
| 9 | **Breakout v3** (52-week-high, RS-ranked, Stage-2 template) | Proxy prototype only: 2015+ Sharpe ties the Elendel control; win rate 39%, payoff 5.8× | Sharpe 0.37–0.59 on proxy | You already run HR/VCP breakouts; marginal value probably small. Keep as a candidate after #8 |
| 10 | **Gold: capped idle-cash overlay** (`momentum_gold/`) | +0.6 pt CAGR, +0.03 Sharpe, drawdown unchanged; ≈ 0 if gold's drift disappears | +0.4 pt, +0.015 Sharpe | Built and parity-tested; low value — only worthwhile if you want a non-equity leg for its own sake |

### C. Cut — tested and rejected (so we stop revisiting them)

| Idea | Why it is cut |
|---|---|
| **Low-risk add-on** (low vol / ulcer) to Elendel or Zenith | Real engines: Elendel (live universe) Sharpe **−0.26**, CAGR **−6.3 pt** (P 0.00); Zenith −0.24 / −5.8 pt (live) and −0.25 / −6.4 pt (301–1000), P 0.00. Elendel in 301–1000 ≈ 0; Quad slightly positive (+0.03 live, +0.14 in 301–1000, P 0.75) |
| **Intraday-drift term** | Elendel and Zenith: −0.22 to +0.03 Sharpe (negative in 301–1000, P ≤ 0.05 on 2015+); only Quad 301–1000 +0.19 (P 0.96) / +0.13 (P 0.82) |
| Q5-only for Elendel | −0.06 / −0.28 Sharpe (P 0.18 / 0.03). (It helps Zenith, see #1) |
| Earnings-surprise / margin terms added to the score | IC is real but the top-15 book does not improve (stage 15) — use only as the event trigger |
| Crash-state / vol / dispersion / illiquidity exposure scaling | Engines already absorb it; Sharpe flat to lower (stage 16–17) |
| Factor momentum; long-run reversal; time-series momentum on stocks | Worse than plain Elendel / no signal (stage 16–17) |
| Universes below rank 1000 | Look excellent in backtests (Zenith Sharpe 3.0+ since 2015) but trade ~₹1 cr/day at rank 1500, and survivorship is worst there |
| Asset rotation, sector rotation, VIX-spike re-entry, index timing, seasonality, standalone gold sleeve | Cut in `IDEA_ROADMAP.md` (no portfolio gain; gold sleeve superseded) |

## 2. Recommended order of work

1. **Residual-momentum term in Zenith and Elendel** (#1, #2) — one change, strongest and most consistent evidence. Backtest the exact live code path, paper-trade a month.
2. **Confirm the idle-cash sweep** in live Elendel/Quad (#3) — free return if it is missing.
3. **Zenith universe 301–1000** (#4) — decide after checking capital per strategy (below). Re-measure on top of step 1.
4. **Refresh the quarterly results feed**, then (**E/P tilt**, #5) and the (**PEAD event sleeve**, #8) — both depend on it. The feed is the single gating dependency.
5. Quad tight-range term (#6) as a small, separable experiment.
6. Everything else only if steps 1–5 leave you wanting more.

**Kill/review rules** (for each shipped change): over any rolling 12 months the changed engine trailing the unchanged one by more than 5 CAGR points, or a max drawdown more than 3 points worse than the unchanged engine over the same period, → revert and investigate. Residual-momentum tilt: also check that the picks' overlap with the live residual-momentum strategy does not push the combined book's correlation above ~0.9.

## 3. Open items and caveats

* **Capital per strategy** is still unknown. It decides #4 and the sleeves: at ≤5% of average daily value, a 15-name book is capped at roughly the daily traded value of its least-liquid holding — today about ₹5 cr at rank 1000, ₹17 cr at rank 600, ₹60 cr at rank 300.
* Volume history before ~2020 is much thinner than today in these files (rank-300 daily value ₹3 cr in Dec 2019 vs ₹39 cr in Dec 2023), so historical liquidity ranks and capacity figures are distorted; ranks remain usable, absolute rupee capacity from history is not.
* One window per fundamentals idea (2019-06→2025-06); E/P and PEAD results are one cyclical-value regime and one set of results.
* The changes were tested at pre-set weights (0.5; 1.0 for E/P) without tuning; no further parameter search has been done and none is recommended before live paper-trading.
* Survivorship: only 98 of 5,205 price files end before mid-2026.

## 4. Implementation status

| Rank | Item | Status |
|---|---|---|
| 1 | Zenith + 0.5 × residual momentum | **Built** — `csm_resid_tilt/` (`CSMZenithResid`); native backtest confirms: 2005+ Sharpe 1.87 → 2.23, 2015+ 1.48 → 1.99 (P 1.00), 21 of 24 years better; look-ahead and parity tests pass |
| 2 | Elendel + 0.5 × residual momentum | **Built** (`CSMElendelResid`); native result weaker than the research variant: 2015+ Sharpe 1.66 → 1.84, P 0.86, interval includes zero — paper-trade longer than Zenith |
| 3–10 | everything else | not started |

**Update (same day) — standalone strategies built with their own backtest modules, because the tilts above raise correlation between the engines:**

| Strategy | Folder | Result (own window) | Correlation with live engines | Verdict |
|---|---|---|---|---|
| CSM Earnings-Yield (monthly, ranks 301–1000, E/P + rising profit) | `csm_value/` | 2019-08→2025-06: CAGR 49.6%, Sharpe 1.67, MaxDD −30.8% | daily 0.62–0.70 (beta ~1.0); **market-residual corr 0.20–0.26** | Modest return-adding diversifier; blend Sharpe +0.03 at 10%, drawdown +2 pt worse |
| PEAD Confirmed-Drift (event-driven) | `csm_pead/` | 2020-09→2025-06: CAGR 31.6%, Sharpe 1.20, MaxDD −25.5% | daily 0.69–0.73 | Not recommended: lowers the trio's Sharpe; signal is real (+2.6% / 60d causal) but the book is market beta |

**Update 2 — Elendel-style reporting.** `csm_value/` was rebuilt on the Elendel chassis (same engine, overlays, logs, IC sections): 2019-06→2025-06 CAGR 44.7%, Sharpe(rf0) 2.70, MaxDD −12.6% vs Elendel 43.2% / 2.61 / −12.8% in the same window; market-residual correlation with the live engines 0.36–0.42; adding it to the live trio at 30% lifts Sharpe 2.01 → 2.24 with no drawdown cost. `csm_pead/` prints the same Elendel report format (event-driven loop; own regime scaling absent): CAGR 30.8%, Sharpe(rf0) 1.50, MaxDD −25.5% — still not recommended as a standalone book.

# Strategy Validation Playbook

A strategy-agnostic checklist for taking any momentum strategy in this repo from development to live capital — pre-agreed pass/caution/kill numbers, so the same result gets the same verdict every time.

**Applies to**: `csm_absolute.py`, `momentum_strategy.py`, `csm_batch_strategy.py`, `csm_stock_strategy.py`, and future variants. `csm_absolute` is used as the worked example (marked **Ex:**) — the flow and thresholds are the generic part. Every number is a *default*: overridable per strategy with a written reason (Appendix C).

**Not in scope**: strategy design, code style, ops. This is the gate-keeping layer on top of whatever's already built.

---

## Quick map — 8 stages at a glance

| # | Stage | Core question | Pass bar (one line) |
|---|---|---|---|
| 1 | Data integrity & universe | Is the panel/universe clean? | ≥8 names/month, `min_periods` set, survivorship checked |
| 2 | Core signal diagnostics | Does the raw signal have edge? | L0 & L3 IC NW-t ≥ 2.0 |
| 3 | Universe/param robustness + ablation | Overfit to one universe / knob / component? | Core-band Sharpe range ≤ 0.35, no parameter cliffs, ablation scorecard clean |
| 4 | IS/OOS validation | Survives untouched data? | OOS Sharpe ≥ 60% of IS in **both** split directions, sign positive; full-sample (2002–2025) reported, not gated |
| 5 | Exit-quality diagnostics | Are exits doing their job? | Per-reason post-exit verdict computed, ≥30 trades/bucket |
| 6 | Paper / shadow | Does live plumbing match backtest? | Weight parity ≥99%, slippage ≤1.5× model |
| 7 | Live deployment | Only the vetted file goes live? | Two-person sign-off, Tier-1/2 diff clean |
| 8 | Monitoring & kill | Still working? | Rolling scorecard green, kill-switch armed |

**Flow**: 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8. Stages 2–5 can loop (tweak → re-check), but the moment OOS (stage 4) is *looked at* to decide a change, log it (§4's "not a slot machine" rule) — the one anti-p-hacking rule everything else protects. Stage 8 feeds back to Stage 1/3, never a silent prod hotfix. Post-exit analysis (§5) and the ablation scorecard (§3) are **diagnostics, not gates** — they force a conversation, they don't block on their own.

Full numeric lookup table: **Appendix B**.

---

## Vocabulary

| Term | Definition |
|---|---|
| IS / OOS windows | 2001-01-01→2012-12-31 and 2013-01-01→present — the two halves of the time split. Which half plays IS vs. OOS is **interchanged** (both directions run, §4.1) |
| Full window | 2002-01-01 → 2025-12-31 (or latest complete year) — entire usable history, no split. Stage 4 reporting only (§4.2), never a promotion gate on its own |
| Split type | Single **time-based** split per direction. Not walk-forward. Never re-drawn within a direction. |
| Universe | Tradeable cross-section after `filter_universe()` (price floor, liquidity rank, circuit/listing-age exclusions) |
| Band | Contiguous liquidity-rank slice, e.g. `500–1000` (vs. a top-N universe, `0–1000`) |
| Cell | One fully-specified run: one version × one config × one window |
| IC | Cross-sectional Spearman correlation, factor(t) vs. forward return(t→t+k) |
| ICIR | IC mean ÷ IC std ("IC Sharpe") |
| NW-t | Newey-West HAC t-stat on mean IC, lag ≥ horizon. **Use this**, not plain t-stat, beyond 1-month horizons |
| Base strategy file | The one file eligible for live capital (**Ex:** `csm_absolute.py`) |

---

## Stage 1 — Data integrity & universe definition

| Check | Verify | Threshold | If it fails |
|---|---|---|---|
| Survivorship | % tickers delisted >6mo before panel end | flag if < 2% | Downstream IC is an upper bound only — say so in every report |
| Split/dividend adjustment | No unadjusted return jumps | spot-check | Fix data before proceeding |
| Min listing history | Trading days before eligibility | ≥ 252 days | Exclude name until met |
| `min_periods` on liquidity rolling window | Set explicitly, verified by per-month row count | must be set | See real bug below |
| Breadth floor | Names per cross-sectional month | ≥ 8 | Exclude month from IC, report exclusion % |

> **This already happened once**: an unset `min_periods` on a `rolling(63)` dollar-volume window emptied the tradeable universe in ~60% of months and silently collapsed NW-t from ~3.7 to ~0.5. Not hypothetical — treat it as a mandatory line item.

**Output**: a one-paragraph "universe card" (definition + pass-rate stats) pinned atop every downstream report. Stage 2 is meaningless if this stage is buggy.

---

## Stage 2 — Core signal diagnostics

| # | Check | Method | Gate | Note |
|---|---|---|---|---|
| 2.1 | Filter ladder | IC/ICIR/NW-t at rungs L0(raw)→L1(price)→L2(liquidity)→L3(tradeable)→L4(gates)→L5(ranked pool) | **L0 & L3 NW-t ≥ 2.0** | If L0 has no edge, filters are manufacturing it — kill here. **Ex:** L0 IC ≈ +0.02–0.025, NW-t ≈ 3.7–4.2 |
| 2.2 | Horizon decay | IC at 1/3/6/12m forward | Flag rebalance/horizon mismatch | Not auto-kill — reason about it. **Ex:** IC peaks at 3m on a monthly-rebalanced strategy |
| 2.3 | Quantile monotonicity | 5–10 quantile spread of forward return | ≥80% monotonic adjacent pairs; spread NW-t ≥ 2.0 on L3 | Checked independently of 2.1 |
| 2.4 | Breadth | % months excluded for <8 names | ≤ 15% | >15% → revisit Stage 1 |
| 2.5 | Equal- vs. value-weighted IC | Compute both | Flag large divergence | Edge lives in illiquid names → capacity concern, carry to Stage 6 |
| 2.6 | Year/regime concentration | Top-2-year share of cumulative signed IC | ≤ 50% | >50% → label "concentration-fragile," carry caveat forward |
| 2.7 | Lookahead assert | raw-forward IC vs. ffill-across-delisting IC | divergence ≈ 0 | Large gap = survivorship leak |

**Gate to Stage 3:**
- [ ] L0 NW-t ≥ 2.0
- [ ] L3 NW-t ≥ 2.0
- [ ] Breadth-exclusion ≤ 15% of months
- [ ] No unresolved lookahead-assert failures

---

## Stage 3 — Universe/parameter robustness & ablation harness

### 3.1 Universe band sweep

Standard set — **top-N**: {100, 250, 500, 750, 1000, 1500} · **bands**: {0–500, 500–1000, 1000–1500, 1000–2000}. Dispersion computed on the **core set {250, 500, 750, 1000, 1500}** — the 100-name band is a "does it break" stress probe, not a robustness input (breadth rule, §2.4).

| Metric (core-band range) | Acceptable | Caution | Major divergence |
|---|---|---|---|
| Sharpe | ≤ 0.35 | 0.35–0.60 | > 0.60 |
| Calmar | ≤ 0.50 | 0.50–0.90 | > 0.90 |
| CAGR | ≤ 8 pp | 8–15 pp | > 15 pp |
| Max Drawdown | ≤ 10 pp | 10–18 pp | > 18 pp |
| Any core-band Sharpe | > 0 | — | ≤ 0 → **auto major divergence**, overrides row above |

Apply the **same bands + thresholds to signal IC**, independently of backtest P&L — separates sizing/cost artifacts from genuine signal overfitting.

> A *better* number in a wide/illiquid band (e.g. 1000–2000) is a red flag, not reassurance — usually under-modeled cost, not real edge. Don't bank it without re-modeling cost for that band.

### 3.2 Parameter sensitivity

| Knob | Sweep | Gate |
|---|---|---|
| Lookback window(s) | ±20%, ±40%, ≥5 points incl. current | Sharpe swing ≤ 0.4 across ±20% move |
| Rebalance frequency | same | same |
| Top-N capacity | same | same |
| Stop-loss % | same | same |
| Regime-filter thresholds | same | same |

A knob that swings Sharpe >0.4 on a 20% nudge is a "cliff" — overfit to that exact value. Prefer a flat plateau over a sharp peak, even if the peak's raw number is higher.

### 3.3 Ablation harness — the single-metric pitfall

Optimizing on one scalar (commonly Calmar) hides degradation elsewhere. **Every ablation cell reports all 5, always:**

| Metric | Max allowed regression vs. baseline (to disqualify a "winner") |
|---|---|
| Sharpe | 15% relative |
| Calmar | 15% relative |
| Return stability (std of trailing-12m returns) | 20% relative |
| Avg drawdown depth (mean of all >2% episodes, not just max) | 20% relative |
| Turnover (or cost-adjusted return) | 25% relative |

**Selection rule**: if the nominal best-on-primary-metric cell trips any row above, use the next-best cell that clears all five. If none clear it, the ablation is inconclusive — keep baseline, don't force a "winner" through.

Report as one row per cell × all 5 metrics + delta vs. baseline (never a single-column "winner" table). Run leave-one-out (n+1 cells) minimum; full factorial (2ⁿ) only if n ≤ 4–5.

**Gate to Stage 4:**
- [ ] All Stage 3 tuning done on IS window only — nothing here touches OOS

---

## Stage 4 — Train/test (IS/OOS) validation

All Stage 3 tuning is IS-only. OOS touched only after the config is frozen. Single split — no re-drawing the boundary within a direction.

### 4.1 Bidirectional split (interchange IS ↔ OOS)

Run the split **both ways**, not just one fixed direction — each half of history serves once as the tuning set and once as the holdout:

| Pass | IS (tune on) | OOS (validate on) |
|---|---|---|
| **Split A** | 2001-01-01 → 2012-12-31 | 2013-01-01 → present |
| **Split B** | 2013-01-01 → present | 2001-01-01 → 2012-12-31 |

Both passes go through the identical gate table below, **independently** — Stage 3 is re-run per direction (a config frozen from Split A's IS tuning is not automatically valid as Split B's IS tuning). A strategy that passes one direction and fails the other is **not validated** — it's found a regime-specific edge, not a general one. Treat a single-direction pass as incomplete, not a soft pass.

| Metric | Acceptable | Caution | Kill |
|---|---|---|---|
| Sharpe (OOS ÷ IS) | ≥ 60% | 40–60% | < 40% |
| Calmar (OOS ÷ IS) | ≥ 60% | 40–60% | < 40% |
| CAGR (OOS ÷ IS) | ≥ 50% | — | < 50% |
| Max Drawdown (OOS vs IS) | ≤ 1.5× | — | > 1.5× |
| OOS Sharpe sign | > 0 | — | ≤ 0 → **auto-kill**, overrides ratios |
| OOS IC NW-t (L0 & L3) | ≥ 1.5 | — | < 1.5 |

- **Regime coverage**: confirm OOS spans ≥1 real stress regime (2018 vol / 2020 COVID / 2022 selloff). If dodged entirely → flag as untested-tail-risk, not full validation.
- **"OOS is not a slot machine"**: log every time OOS is looked at (date / what / what changed after). If OOS has been viewed and the strategy is modified **more than twice** afterward, the window is spent — extend with new data or re-run Stage 4 on a fresh slice. This applies **per direction** — looking at Split A's OOS doesn't spend Split B's, but modifying the shared core signal because of what Split A's OOS showed does taint Split B, since Split B's "IS" now includes knowledge derived from Split A's holdout. Log which direction triggered any change.

### 4.2 Full-sample report (2002–2025) — reporting only, never a gate

Once both split directions clear the gate above, generate one more report: the full scorecard (Appendix A.2) computed over the **entire** usable history, 2002-01-01 → 2025-12-31 (or latest complete year), with no IS/OOS split at all.

**Why run it**: each split half carries roughly half the sample — noisier Sharpe/Calmar confidence intervals, and each half only guarantees partial regime coverage on its own. The full-sample run gives the tightest-available estimate of headline metrics and the only single number guaranteed to reflect every stress regime in the dataset (2008 GFC, 2018 vol, 2020 COVID, 2022 selloff) at once. It's the number to actually communicate as "what this strategy has done over its full history."

**Why it can't replace §4.1**: by the time this runs, the config has already been shaped by looking at data from both halves (across the two split directions) — so full-sample numbers are structurally optimistic in the same way any in-sample number is, and blind to overfitting. It answers *"what has this strategy actually done,"* not *"does it generalize."* **Never promote or kill on this number alone** — it deliberately has no pass/caution/kill row of its own in Appendix B.

**Gate to Stage 5:**
- [ ] Both split directions (A and B) independently clear the OOS gate above
- [ ] OOS Sharpe > 0 in both directions
- [ ] OOS IC NW-t ≥ 1.5 (L0 and L3) in both directions
- [ ] Regime-coverage caveat documented either way, per direction
- [ ] Full-sample report (§4.2) generated and attached to the record — informational, not scored

---

## Stage 5 — Exit-quality diagnostics (incl. post-exit continuation)

| Check | Threshold | If it fails |
|---|---|---|
| `END_OF_PERIOD` share of exits | < 5% (outside final months) | Backtest close-out is contaminating live-relevant stats |
| Trades per exit-reason bucket | ≥ 30 | Report as directional only, not a hard number |

### Post-exit continuation — scoped correctly

**Wrong use**: comparing raw post-exit return *across strategies* ("Strategy A's exited names rose more than B's, so B's exits are worse"). Meaningless — a risk-averse strategy that exits pre-emptively will *always* look worse on this than one that holds until a visible drop, simply because avoiding that upside is its job.

**Right use**: within one strategy, per exit reason, ask *"did this rule do its own job?"* — never "did the stock keep rising."

| Exit reason | Purpose | Right question | Verdict |
|---|---|---|---|
| `STOP_HIT` | Avoid further downside | Did the name keep underperforming after the stop? | Benchmark-relative avg(+20d,+60d): ≤ −1.0% → **working**. ≥ +1.0% → **too tight** (widen, or add re-entry rule). Between → neutral |
| `REBALANCE` | Rotate to something better-ranked — not loss-avoidance | Did the name rotated *into* outperform the one rotated *out of*? | **Paired** comparison (exited vs. entered, same window) — not the single-name return |
| `SIGNAL_DROP` | Rank fell same-period, no full rebalance | Was the rank drop real signal or noise? | Same verdict shape as `STOP_HIT`, but fix differs: rank-buffer/hysteresis, not stop-distance |
| `CRASH_GUARD` | Avoid a broad regime downturn | Firing frequency vs. whipsaw cost vs. drawdown avoided? | Judged on that tradeoff, not post-exit sign alone — a quick reversal is expected false-positive cost |
| `END_OF_PERIOD` | None — backtest artifact | N/A | Excluded entirely |

**Reference implementation**: [csm_batch_post_exit_analysis.py](csm_batch_post_exit_analysis.py) — forward returns at [1,3,5,10,20,40,60]d, raw + benchmark-relative (net of equal-weight universe), grouped by `Exit_Reason`, printed verdict per reason. Reusable as-is on any strategy's trade log.

**Status**: diagnostic, same tier as IC/ICIR — not a standalone gate. A verdict that stays contradicted across re-runs (e.g. a stop repeatedly firing at local bottoms) escalates to a redesign conversation.

**Gate to Stage 6:**
- [ ] Exit breakdown table produced, <30-trade buckets flagged
- [ ] Per-reason verdicts computed and documented (contradictions → redesign note, not silently passed)

---

## Stage 6 — Paper / shadow validation

The point here is proving **plumbing matches backtest assumptions** — not re-proving alpha (that was Stages 2–4).

| Check | What | Threshold | If it fails |
|---|---|---|---|
| Duration | Rebalance cycles observed | ≥ 3 (≥ 6 if regime-sensitive exits like `CRASH_GUARD`) | Extend paper period |
| Weight parity | Shadow vs. backtest-simulated weight vectors, same date | ≥ 99% similarity | Hard blocker — find the plumbing bug (off-by-one date, stale universe snapshot, timezone) |
| Slippage — core universe | Realized vs. modeled cost (e.g. 0.3%) | ≤ 1.5× modeled | Recalibrate cost model, regenerate Stage 4/5 numbers |
| Slippage — any band | same | ≤ 3× modeled | same |
| Execution timing | Signal-to-fill lag | Matches or more conservative than backtest | Fix assumption or fix pipeline (a common silent alpha-destroyer) |

**Gate to Stage 7:**
- [ ] Parity confirmed
- [ ] Slippage within bar (or cost model updated + re-verified)
- [ ] No unresolved plumbing blockers
- [ ] Minimum duration met

---

## Stage 7 — Live deployment: the two-tier file model

| Tier | Deploys live? | Contains | Example |
|---|---|---|---|
| 1 | **Yes — only this** | Signal, universe filter, position/exit logic | `csm_absolute.py` |
| 2 | Never | Backtest engine, thin runner, all diagnostics/research scripts | `csm_absolute_backtest.py`, `run_csm_absolute.py`, `csm_absolute_core_signal_diagnostics.py` |

The runner *feels* production-adjacent (it wires the strategy end-to-end) but it wires historical data + reporting, not a live order path — it stays Tier 2.

**Pre-deployment checklist:**
- [ ] Live Tier-1 file diffed against the exact version that cleared Stages 2–6 (no silent post-OOS tweaks)
- [ ] Live entry point uses the identical validated code path — no parallel/forked live-only branch
- [ ] Two-person sign-off recorded (researcher + reviewer) — caution-tier items re-affirmed explicitly, not silently inherited
- [ ] Initial capital-at-risk ramp agreed — not full size on day one

---

## Stage 8 — Post-live monitoring & kill/decay

| Watch | Cadence | Caution | Kill / escalate |
|---|---|---|---|
| Trailing IC NW-t (24–36m) | quarterly | < 1.0 for 2 qtrs → formal review | negative for 2 consec. qtrs → kill decision |
| Live Sharpe ÷ OOS Sharpe | rolling | 40–60% | < 40% or ≤ 0 for 2 rebalance cycles → kill-switch |
| Live MaxDD vs. OOS MaxDD | continuous | — | > 1.5× → mechanical de-risk, no discretion |
| Exit-reason verdict drift (§5, rerun on live log) | quarterly | — | "working" → "contradicts" for 2 consec. qtrs → escalate |
| Tracking error vs. backtest | quarterly | — | ≥ 5% ann., 2 consec. qtrs unexplained → retire |

**Decommission triggers** (any one):
- [ ] Sustained kill-switch trigger (any row above)
- [ ] Universe/market-structure shift invalidates original `filter_universe` assumptions
- [ ] Unexplained tracking error persists 2 quarters

→ Mandatory retirement or full re-entry to Stage 3. Never a silent prod hotfix. This is where the loop closes back to the top.

---

## Appendix A — Scorecard templates

**A.1 Ablation scorecard (lean, Stage 3)** — one row per cell + delta vs. baseline:

| Cell | Sharpe | Calmar | Return stability | Avg DD depth | Turnover |
|---|---|---|---|---|---|

**A.2 Full report scorecard (Stages 4/6/8):**

| Sharpe | Sortino | Calmar | CAGR | Max DD | Beta | Alpha (ann.) | Win rate | Profit factor (%) | Profit factor ($) | Payoff ratio | Avg hold (days) |
|---|---|---|---|---|---|---|---|---|---|---|---|

Don't mix them — lean table for scanning many ablation cells, full table for one config under formal review.

## Appendix B — Every threshold in one place

| Stage | Metric | Acceptable | Caution | Kill / Major divergence |
|---|---|---|---|---|
| 1 | Breadth (names/month) | ≥ 8 | — | < 8 (month excluded) |
| 2 | L0/L1 IC NW-t | ≥ 2.0 | — | < 2.0 |
| 2 | L3 (tradeable) IC NW-t | ≥ 2.0 | — | < 2.0 |
| 2 | Monotonic quantile pairs | ≥ 80% | — | < 80% |
| 2 | Breadth-excluded months | ≤ 15% | — | > 15% |
| 2 | Top-2-year share of signed IC | ≤ 50% | > 50% flagged | — |
| 3 | Universe Sharpe range (core bands) | ≤ 0.35 | 0.35–0.60 | > 0.60 |
| 3 | Universe Calmar range (core bands) | ≤ 0.50 | 0.50–0.90 | > 0.90 |
| 3 | Universe CAGR range (core bands) | ≤ 8 pp | 8–15 pp | > 15 pp |
| 3 | Universe MaxDD range (core bands) | ≤ 10 pp | 10–18 pp | > 18 pp |
| 3 | Any core-band Sharpe | > 0 | — | ≤ 0 (auto major divergence) |
| 3 | Parameter Sharpe swing @ ±20% | ≤ 0.4 | — | > 0.4 (cliff) |
| 3 | Ablation regression — Sharpe/Calmar | ≤ 15% rel. | — | > 15% (disqualified) |
| 3 | Ablation regression — stability/avg-DD-depth | ≤ 20% rel. | — | > 20% |
| 3 | Ablation regression — turnover | ≤ 25% rel. | — | > 25% |
| 4 | OOS/IS Sharpe | ≥ 60% | 40–60% | < 40% |
| 4 | OOS/IS Calmar | ≥ 60% | 40–60% | < 40% |
| 4 | OOS/IS CAGR | ≥ 50% | — | < 50% |
| 4 | OOS vs IS MaxDD | ≤ 1.5× | — | > 1.5× |
| 4 | OOS Sharpe sign | > 0 | — | ≤ 0 |
| 4 | OOS IC NW-t (L0, L3) | ≥ 1.5 | — | < 1.5 |
| 4 | Post-OOS-look modifications before re-validation | ≤ 2 | — | > 2 (window spent) |
| 4 | Split directions independently passing (A and B) | 2 of 2 | — | < 2 (incomplete, not a soft pass) |
| 4 | Full-sample report (2002–2025) generated | attached to record | — | — (informational only, never scored) |
| 5 | Trades per exit-reason bucket | ≥ 30 | — | < 30 (directional only) |
| 5 | `END_OF_PERIOD` share of exits | < 5% | — | ≥ 5% |
| 5 | Post-exit verdict, benchmark-rel. avg(20d,60d) | ≤ −1.0% working | −1.0%–+1.0% neutral | ≥ +1.0% too early |
| 6 | Weight-vector parity | ≥ 99% | — | < 99% (hard blocker) |
| 6 | Slippage vs. modeled — core universe | ≤ 1.5× | — | > 1.5× |
| 6 | Slippage vs. modeled — any band | ≤ 3× | — | > 3× |
| 8 | Trailing 24–36m IC NW-t | ≥ 1.0 | 2 qtrs < 1.0 → review | sustained negative → kill review |
| 8 | Live ÷ OOS Sharpe (rolling) | ≥ 60% | 40–60% | < 40% or ≤ 0, 2 cycles → kill |
| 8 | Live MaxDD vs. OOS MaxDD | ≤ 1.5× | — | > 1.5× (kill-switch) |
| 8 | Unexplained tracking error (ann.) | < 5% | — | ≥ 5%, 2 consec. qtrs → retire |

## Appendix C — Per-strategy override log

| Strategy | Threshold overridden | Deviation | Reason | Reviewer sign-off | Date |
|---|---|---|---|---|---|
| | | | | | |

## Appendix D — Worked-example index (`csm_absolute`)

| Section | Example |
|---|---|
| Stage 1 | `min_price=20`, `max_circuit_days=8`; the real `min_periods` universe bug |
| Stage 2 | L0 IC ≈ +0.021–0.025, NW-t ≈ 3.7–4.2; IC peaking at 3m vs. monthly rebalance |
| Stage 3 | `universe_top_n=1000` production default; band sweep set matches what's already been run |
| Stage 5 | Exit taxonomy `STOP_HIT`/`CRASH_GUARD`/`REBALANCE`/`SIGNAL_DROP`/`END_OF_PERIOD`; post-exit template built for sibling `csm_batch`, directly reusable here |
| Stage 7 | Tier 1: `csm_absolute.py`. Tier 2: `csm_absolute_backtest.py`, `run_csm_absolute.py`, `csm_absolute_core_signal_diagnostics.py` |

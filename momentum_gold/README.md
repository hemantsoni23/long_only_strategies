# Momentum books + gold: idle cash → capped gold in weak markets

Idea (yours): the momentum books sit in cash when the market is weak; gold has a low correlation with equities, so put that idle cash in gold instead.
This folder tests that idea on your **actual live engines (unmodified)** and ships the version the evidence supports.

## Bottom line

| | What the evidence says |
|---|---|
| **All idle cash → gold in weak markets (the idea as stated)** | **Hurts.** Sharpe −0.09 to −0.17, max drawdown 5–11 pts deeper, in all three strategies. In stress the books are 64–100% idle, so the portfolio becomes mostly gold. CAGR rises ~3.3 pts, but that is gold's own 2007–2026 drift. |
| **Capped gold (10% of portfolio) in weak markets** — shipped as `GoldIdleCashOverlay` | **Small, consistent gain; no drawdown protection.** CAGR +0.6 pt, Sharpe +0.025 to +0.03 (bootstrap P = 0.96–0.98), max drawdown ≈ unchanged (−0.2 to +0.4 pt). With gold's excess drift set to zero it is neutral (Sharpe +0.001 to +0.003). Better in 10 of 16 calendar years in every strategy. |
| **Biggest lever (not gold)** | Elendel and Quad backtests leave idle cash at **0%**. Putting idle cash in a 6.5% liquid fund adds **+2.8 to +3.1 pts CAGR, +0.16 to +0.17 Sharpe and 2.5–2.7 pts shallower max drawdown** (zero-risk; Zenith already does this). |

**Why gold does not protect these books:** their worst drawdowns (2018, 2008, 2016, 2025–26…) happen when they are *already* holding about 40% cash on average (range 18–68% across the 12 worst episodes); gold rose in 11 of the 12 worst episodes, but the drawdown is dominated by the equity part, so the max-drawdown line barely moves. And a low-correlation asset only improves a Sharpe 1.7–1.9 book if it also earns above cash. With gold's drift neutralised, a static 10% sleeve changes Sharpe by −0.01 to −0.02 versus the proper control (10% in the liquid fund); with its sample drift (15.8% vs 6.5% a year) it adds +0.07 to +0.08 — i.e. the gain is gold's return in this sample, not diversification.

## The overlay

```
gold weight = min(idle cash weight, 10%)   if the engine's regime in {BEAR, PANIC, HIGH_VOL}   else 0
rest of idle cash → liquid fund (LIQUIDBEES)
```

Gold is held on ~32% of days, averaging 3.2% of the portfolio. Stock decisions are untouched.

## Results (15 usable years; `python3 run_momentum_gold_report.py`)

Baseline = idle cash in a 6.5% liquid fund. Overlay = cap 10%, weak regimes.

| Strategy | Baseline CAGR / Sharpe / MaxDD | Overlay (sample gold) | Overlay (half drift) | Overlay (zero drift) |
|---|---|---|---|---|
| Elendel | 34.0% / 1.80 / −17.1% | +0.6 pt / +0.026 / −0.1 pt | +0.4 / +0.014 / −0.3 | +0.1 / +0.001 / −0.5 |
| Zenith | 29.3% / 1.73 / −11.9% | +0.6 / +0.030 / −0.2 | +0.4 / +0.016 / −0.3 | +0.1 / +0.003 / −0.3 |
| Quad momentum | 34.5% / 1.86 / −15.3% | +0.6 / +0.025 / +0.4 | +0.4 / +0.013 / +0.4 | +0.1 / +0.001 / +0.3 |

(Engine-default versions with idle cash at the engine's own rate: Elendel 31.2% / 1.64 / −19.9%; Zenith unchanged; Quad 31.5% / 1.68 / −17.8%.)

Cap and mode sensitivity (all vs the liquid-fund baseline; real gold): cap 5/10/15/20% always-on adds Sharpe +0.03/+0.04/+0.05/+0.055 for Elendel but turns **negative** (−0.01/−0.02/−0.04/−0.06) when gold's drift is removed; the two settings that stay ≥ 0 under zero drift in all three strategies are the 10% cap in weak markets (shipped) and its BEAR/PANIC-only variant (smaller: Sharpe +0.017/+0.018/+0.018 with sample drift). 0.30% gold trading costs lower the gain only slightly (Sharpe +0.020–0.023).

## What to expect

* **Planning case** (half of gold's sample drift): about **+0.4 pt CAGR and +0.015 Sharpe**, drawdown unchanged. Zero-drift case: ≈ 0. Treat it as a low-risk, low-reward add-on, not as the improvement you are looking for.
* It will **not** make drawdowns shallower. If drawdown reduction is the goal, the levers that matter in these tests were the liquid-fund sweep and the regime/vol scaling already in the engines.

## Using it

* Live: each day (or at each rebalance) compute the book's idle-cash weight and read the engine's regime label; `GoldIdleCashOverlay().live_instruction(idle_weight, regime)` returns the gold and liquid-fund weights and raises if the GOLDBEES price is stale (> 5 days).
* Backtest: `GoldIdleCashOverlay().apply(executed_weights, net_returns, regime, daily_cash_rate)` on any engine run (post-processing is exact because the engine's stock decisions never depend on cash).
* Regime labels come from each engine's own `_regime_daily` (BULL / BEAR / HIGH_VOL / PANIC, built from lagged inputs).

## Files

| File | Purpose |
|---|---|
| `gold_idle_cash.py` | `GoldIdleCashOverlay` (live rule, backtest `apply`, stale guard, gap-safe) |
| `run_live_engines.py` | runs the **unmodified** Elendel / Zenith / Quad engines from `Old_live_strategies` (their own defaults, 0.3% cost, 2001 → 2026-07-16) and stores daily outputs in `.cache/` |
| `run_momentum_gold_report.py` | the report above → `output/momentum_gold_report.txt` |
| `test_overlay_parity.py` | overlay reproduces the analysis exactly; cap / idle / gap / regime constraints verified |
| `gold_overlay.py`, `analyze_gold_idle.py`, `analyze_gold_caps.py`, `final_gold_idle.py`, `static_sleeve_check.py` | the research: variants, caps, drift scenarios, controls |
| `results_*.csv` | all numbers |

## Caveats

* **15 usable years, one gold bull market.** GOLDBEES data are missing 2011-01 → 2014-12; the overlay and the evaluation exclude those years (idle cash stays in the liquid fund there). Gold's sample excess return over a liquid fund was ~+9 pts a year; nothing in the data says that persists.
* **Candidate set was declared before the final run** (uncapped, cap 10/20% weak markets, cap 10% always, BEAR/PANIC-only), but the cap/regime choice was made after seeing exploratory results across several caps; treat the +0.6 pt as an upper-middle estimate.
* The engines' regime labels, costs and idle-cash accounting are used as-is; taxes on gold ETF rebalancing are not modelled; daily rebalancing of the gold weight is assumed (cost charged on weight changes).
* **Not tested:** csm_absolute and the residual-momentum strategy (they use different simulators); gold in the stock *ranking* itself; silver.
* The earlier research documents (`factor_research/IDEA_ROADMAP.md`, `gold_sleeve/README.md`) showed larger gold gains on weaker proxy books (Sharpe ~0.7); on your real engines (Sharpe 1.7–1.9) the marginal value of gold is much smaller, as above.

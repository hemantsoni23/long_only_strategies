> **Update 2026-10-06 — read `../momentum_gold/README.md` first.** The portfolio numbers below use a weak proxy bucket (Sharpe ~0.6–0.7). Tested on the real Elendel/Zenith/Quad engines (Sharpe 1.7–1.9) a gold sleeve adds far less: the static-sleeve gain is gold's sample return (it vanishes if gold's drift is neutralised) and drawdowns do not improve. The recommended gold integration is the capped, weak-market idle-cash overlay in `momentum_gold/`.

# Gold sleeve — Persistence × Volatility (`GoldSleevePV`)

A time-series momentum sleeve on one liquid gold ETF (GOLDBEES), sized by trend persistence and volatility. It is built as a **risk tool for a momentum equity book**, not as a return source — read "What this is and is not" before using it.

## Core logic

Decided on the last trading day of each month, executed at the next day's close:

```
persistence  Q = share of the last 126 trading days on which gold closed above its 50-day SMA
volatility   s = 63-day realised daily-return std, annualised
exposure     E = Q × min(1, 12% / s)          →  E in gold, (1 − E) in cash / liquid fund
```

The persistence leg is the same idea as `q5_126` in the stock books (how *consistently* is it trending, not how far did it move), applied in time series to a single asset. The volatility leg keeps the sleeve's risk contribution stable.

## What this is and is not

* **No gold-timing return edge exists in the data.** Over ~13–15 usable years the best own-trend or cross-asset signal (12-month momentum) has a t-stat of 1.1; classic TSMOM-12-1 and SMA200 rules did not beat holding gold as a sleeve (`factor_research/results/gold_eda_signals.csv`, `gold_rules_scorecard.csv`).
* **What the rule does do** (at an equal risk budget to a 10% buy-and-hold gold sleeve, i.e. ≈19% weight; `gold_riskmatched.csv`, `gold_g5_neighbourhood.csv`, `gold_g5_placebo.csv`):
  * blended max drawdown shallower in **81 of 81** neighbouring parameter sets (+1.4 to +3.5 pts) with unchanged Sharpe (−0.01 to +0.02);
  * the real exposure path beat **86–90%** of circularly time-shifted placebo exposure paths on drawdown (so the *alignment* carries some information, but only about drawdown);
  * blended Sharpe equal to buy-and-hold gold within noise (+0.01), blended CAGR −0.8 pt.
* **Expect:** a smoother ride and shallower drawdowns. **Do not expect** extra return. If you only want the diversification, `mode="buy_hold"` (static 10%) gives nearly the same Sharpe with less machinery — it is built in for an A/B.

## Results (`python3 run_gold_sleeve_backtest.py`, 174 usable months, 2007-10 → 2026-05)

| | CAGR | Vol | Sharpe | Max DD |
|---|---|---|---|---|
| Persistence × Vol sleeve | 11.5% | 8.4% | 0.64 | −6.9% |
| Buy & hold GOLDBEES | 16.3% | 15.9% | 0.66 | −17.3% |
| Sleeve, 2015+ only | 10.7% | 8.1% | 0.59 | −6.9% |
| Buy & hold, 2015+ only | 14.1% | 14.8% | 0.57 | −17.3% |

* Average gold exposure 52%; ~11 exposure changes a year (7 with a 5% deadband, not part of the validated rule).
* Costs: Sharpe 0.64 / 0.63 / 0.60 at 0.15% / 0.30% / 0.50% one-way.
* Alongside a proxy of your momentum books (4 stripped books): correlation of the sleeve with the bucket −0.24; bucket Sharpe 0.58 → 0.66 and max DD −36.6% → −28.7% with a 19% sleeve (vs −31.8% for 10% buy-and-hold).
* Latest signal (2026-07-31): gold exposure 24% (persistence 0.43, volatility 21.8% after the January 2026 shock). It de-risked from 96% in Aug 2025.
* **Planning expectation** (judgmental haircut: 50–80% of 2015+ Sharpe, drawdown × 1.25–1.5): CAGR ≈ 8–9%, max DD −9% to −10% standalone — treat the drawdown as a **floor** (see data gap, gaps in price).

## Data gap — important

All gold ETF files here (and JUNIORBEES, LIQUIDBEES) are **missing 2011-01 → 2014-12**. The strategy never forward-fills across a gap: windows touching missing data stay NaN, and months whose entry/exit price is missing — or not within 7 days of the decision date — are skipped. This also exposed a flaw in the earlier research roadmap (gold was forward-filled; corrected 2026-10-06). The backtest therefore has two usable segments (2007-10 → 2010, 2015 → 2026) and the drawdown figures cannot include whatever happened in the missing four years.

## Files

| File | Purpose |
|---|---|
| `gold_sleeve_strategy.py` | `GoldSleevePV`: `calculate_signals()`, `backtest()`, `latest_signal()` (stale-data guard), `metrics()`; `mode='pv'` or `'buy_hold'` |
| `run_gold_sleeve_backtest.py` | loader, backtest vs buy-and-hold, segments, cost/deadband sensitivity, yearly table, portfolio view, latest signal, plots → `output/` |
| `test_parity.py` | proves the class reproduces the research series exactly (and standalone to corr 1.0000), and never uses a month inside the data gap |
| `output/` | `gold_sleeve_monthly_log.csv`, `gold_sleeve_daily_signals.csv`, `gold_sleeve_performance.png`, `gold_sleeve_report.txt` |

Research that led here: `factor_research/gold_data.py`, `gold_eda.py`, `gold_rules.py`, `gold_riskmatched.py`, `gold_robustness.py`.

## Using it live

* Run on the last trading day of the month; trade GOLDBEES at the next close; park the rest in LIQUIDBEES / a liquid fund (the backtest assumes 6%).
* `GoldSleevePV.latest_signal()` raises if the last price is more than 5 days old or if too little contiguous history exists — do not bypass it.
* Sleeve weight inside the total portfolio is a portfolio decision: the evidence above uses ≈19% for equal risk to a 10% buy-and-hold sleeve.

## Kill / review criteria

* Drop the timing logic and hold gold statically if, over a full gold drawdown, the live sleeve's drawdown is not clearly shallower than buy-and-hold.
* Re-size to 5% if the rolling 3-year correlation of gold with the equity bucket rises above +0.3.
* Re-examine if realised average exposure drifts far from ~50% or exposure changes exceed ~15 a year.

## Caveats

* One instrument, ~19 years, one major gold bull market (INR gold also benefited from rupee depreciation); 2011–14 is missing.
* Parameters (126 / 50 / 63 / 12%) were set from standard values and checked in a 81-point neighbourhood, but the *choice* of this rule among 8 pre-registered candidates was made on the sleeve's drawdown contribution, which is a selection step.
* Monthly decisions only: no intra-month stop (gold fell 10.5% in one day on 2026-01-30).
* Backtest cash leg is a constant 6%; taxes on short-term ETF gains from rebalancing are not modelled.

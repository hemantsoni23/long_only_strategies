# csm_value — CSM Earnings-Yield

**Two implementations live here.**
* **`csm_value_strategy.py` + `run_csm_value_backtest.py` — the main one: the Elendel chassis** (derived from `csm_elendel_strategy.py` / `run_csm_elendel_backtest.py` by `_generate_elendel_chassis.py`, the way Zenith/Quad were derived). Only the ranking signal and the universe differ; sizing (inverse-vol, 5% cap), hysteresis + swap gap, three-layer hard stops, Crash Guard, correlation guard, 15% vol target, BULL/BEAR/HIGH_VOL/PANIC leverage, loss-scaled cooldown, T+1 fills, 0.3% cost, trade/reject/daily logs, IC/ICIR and realised-IC sections are Elendel's, so the report is the same as your other strategies'.
* `value_strategy.py` + `run_value_backtest.py` — the earlier lightweight version (simple stops, no regime overlays); kept for reference (results in the second half of this file).

## Elendel-chassis version
Signal: E/P = TTM net profit / (month-end price × shares) from point-in-time quarterly results (usable from the filing date, expires after 140 days), among names with positive TTM profit, rising latest-quarter profit and E/P ≤ 50%; z-scored. Universe: liquidity ranks **301–1000** (the 300 largest excluded), price > ₹20, circuit/falling-knife filters as Elendel, **no SMA-200 trend filter and no absolute-momentum gate**. Top 15, buffer 0.2, swap gap 10, all other Elendel defaults (idle cash earns 0%, as in the Elendel runner).

Result (`python3 run_csm_value_backtest.py`; 2019-06-03 → 2025-06-30; Elendel report conventions, Sharpe/Sortino with rf = 0):

| | CAGR | Vol | Max DD | Sharpe | Sortino | Calmar |
|---|---|---|---|---|---|---|
| **CSM Value** | **44.7%** | 14.3% | **−12.6%** | **2.70** | 4.04 | 3.56 |
| Elendel (same window) | 43.2% | 14.4% | −12.8% | 2.61 | 3.82 | 3.39 |
| Zenith | 35.1% | 13.0% | −11.9% | 2.42 | 3.54 | 2.94 |
| Quad | 25.0% | 13.8% | −15.9% | 1.72 | 2.46 | 1.57 |

535 trades, trade win rate 47%, payoff 2.8, profit factor 2.55, median trade −1.3% (a skew book), average MAE −7.7% / MFE +29.6%; exits: rebalance 141, hard stop 378 (PEAK_HARD 240, ENTRY_HARD 97, GAP_DOWN_OPEN 41), Crash Guard 1. Yearly returns: 2020 +69%, 2021 +107%, 2022 +7%, 2023 +73%, 2024 +38%, 2025 H1 +3% (year max drawdowns −7% to −13%).
IC/ICIR of the E/P factor (filtered universe): 1m +0.032 (ICIR 0.27, hit 66%), 3m +0.053, 6m +0.071, 12m +0.097 (ICIR 0.93, NW-t 3.6; the slow, 12-month horizon is typical of value).

**Correlation and portfolio effect (same window; `daily log`s):** raw daily correlation with Elendel / Zenith / Quad **0.67 / 0.64 / 0.71** (live engines among themselves 0.82 / 0.72 / 0.66). With the equal-weight market removed: **0.36 / 0.37 / 0.42** (live engines 0.42–0.70 among themselves). Beta to the market 0.61 (engines 0.46–0.56).
Blend with the equal-weight live trio: value 10% / 20% / 30% / 50% → Sharpe(rf6) 2.10 / 2.18 / 2.24 / 2.32 (trio alone 2.01), CAGR +1.1 / +2.2 / +3.2 / +5.3 pt, max drawdown unchanged at −12.6%. On the Elendel chassis it is a genuine addition to the trio, unlike the lightweight version below (which was a full-beta book).

Tests (`python3 test_csm_value.py`, all pass): E/P re-derived independently from raw results for 400 random stock-months; truncating the data at 2023-06 leaves factor rows and target positions identical; scored names are all inside ranks 301–1000 with positive E/P ≤ 50%; no absolute-momentum gate (26% of held name-months have negative trailing-12m return); weights ≤ 5%, total ≤ 1; `get_exit_signals` keeps Elendel's interface.

Caveats: fundamentals cover 2019-02→2025-06 only — one cheap-cyclical/PSU/commodity regime, 6 years, survivorship in the cheap end; the chassis parameters were not tuned, but the design choices (ranks 301–1000, growth filter) came from earlier look-ups in the same short window. Capacity: ranks 301–1000 hold ~₹5–17 cr/day per name. Needs the quarterly-results feed refreshed for live use (ends 2024Q4 results, filed ≤ 2025-04). Kill/review: pause if trailing-12-month return trails the equal-weight market by > 25 points or the median pick P/E stays < ~4.

---
## Earlier lightweight version (`value_strategy.py`, `run_value_backtest.py`) — for reference

A standalone strategy + backtest module in the same two-file layout as the live ones (`value_strategy.py` ↔ `csm_*_strategy.py`, `run_value_backtest.py` ↔ `run_csm_*_backtest.py`), plus `value_fundamentals.py` (point-in-time results) and `test_value.py`.
Nothing in `Old_live_strategies` is modified; data loading, corporate-action masking and the equal-weight benchmark are imported from the live Elendel runner.

## Rules
Month-end signal, trade at the next close. **Eligible:** liquidity rank 301–1000 (63-day median traded value; the 300 largest excluded), price > ₹20, ≤ 5 circuit-locked days in 63, latest quarterly result filed ≤ 140 days ago,
TTM net profit > 0, latest quarter's yoy net-profit growth > 0, E/P ≤ 50%. **Rank** by E/P = TTM net profit / (price × shares). **Hold** the top 20; a name stays until rank > 30 or it stops being eligible; equal weight 1/20 at entry, survivors not rebalanced.
**Risk:** −20% hard stop from entry (close-based, sell next open less 0.3% slippage, 20-day cooldown); new entries at 70% size when the equal-weight benchmark is below its SMA200; idle cash earns 6.5%; 0.3% cost per side. No price-trend condition anywhere.

## Result (2019-08 → 2025-06, 5.8 years; defaults fixed before running, nothing tuned)
CAGR **49.6%**, vol 22.2%, Sharpe (rf 6%) **1.67**, max drawdown **−30.8%**, 382 trades, win rate 57%, payoff 3.0, ~27% monthly turnover. Years: 2019 +8, 2020 +52, 2021 +151, 2022 +6, 2023 +96, 2024 +42, 2025 H1 −14 (equal-weight market: +5, +56, +138, +29, +62, +53, −6).
Sensitivity (`--sensitivity`, one-at-a-time; every row reported): Sharpe 1.49–1.78 and CAGR 42–56% across top-15/30, no growth filter, no bear scaling, stop 12%/none, universe variants, 2× costs, 0% cash yield — the result is not fragile to the design.

## Correlation — the point of building it (`output/value_report.txt`)
| | corr with Elendel / Zenith / Quad (daily) | monthly |
|---|---|---|
| Earnings-Yield | 0.67 / 0.62 / 0.70 | 0.71 / 0.58 / 0.72 |
| for comparison, live engines among themselves | 0.82 / 0.72 / 0.66 | |

**The raw correlation is mostly market beta**: EY's beta to the equal-weight market is ~1.0 while the live engines run ~0.55 (they hold ~40% cash and cut exposure in weak regimes). With the equal-weight market removed from every stream, EY's residual correlation with Elendel/Zenith/Quad is **0.20 / 0.20 / 0.26**, versus 0.34–0.64 among the live engines themselves — the stock-selection stream is genuinely different, the market exposure is not.
Blend with the live trio (equal weight, 2020-09→2025-06): +10% EY: Sharpe 2.08 → 2.11, CAGR +1.9 pt, max DD −12.6% → −14.6%; +20% EY: Sharpe 2.11, CAGR +3.9 pt, DD −16.5%. The Sharpe break-even rule (new Sharpe > corr × portfolio Sharpe) is met only narrowly (1.67 vs 1.56). **So it is a modest, return-adding diversifier, not a drawdown reducer.**
Lowering the correlation further would need the market component taken out (an index-futures hedge; not long-only) — untested.

## Checks (`python3 test_value.py`, all pass)
E/P re-derived independently from raw results for 400 random (stock, month) pairs; truncating the data at 2023-06 leaves E/P rows and equity identical; `get_exit_signals` agrees with all 66 simulated stops; `get_target_portfolio` reproduces the simulated rebalance sells exactly and buys as a subset across 69 rebalances; position/weight/universe accounting.

## Use
```
python3 run_value_backtest.py               # report, plots, trade/daily logs -> ./output
python3 run_value_backtest.py --sensitivity
```
Live: at each month-end after the close call `get_target_portfolio(as_of, current_holdings)` → keep/sell/buy lists and the new-position weight; each day call `get_exit_signals(portfolio, live_data)` for the stop. Needs the quarterly-results feed refreshed (the file ends with 2024Q4 results, filed ≤ 2025-04).

## Caveats — read before sizing
Fundamentals cover 2019-02→2025-06 only; this is one cheap-cyclical/PSU/commodity-value regime (median picks have P/E ≈ 5). Survivorship: cheap stocks that later died are missing. Ranks 301–1000 hold ~₹5–17 cr of daily value per name today, so capacity is a few crore per strategy.
Quarterly results can contain one-offs (other income, exceptional gains) that inflate E/P; the 50% cap and the growth filter only partly guard against it. 2025 H1 was −14%: the strategy has no history in a value-hostile regime.
Kill/review: pause if trailing-12-month return is below the equal-weight market by more than 25 points, or if the median pick P/E stays under ~4 (peak-earnings crowding).

# CSM Value — look-ahead / inflation audit (2026-10-08)

Everything below is reproducible: `python3 audit_lookahead.py fills replay filings truncation splitters holdings benchmark delay placebo 40`, `python3 audit_engine_accounting.py`, `python3 test_csm_value.py`, `python3 ablation_versions.py`, `python3 train_test_protocol.py`. Raw output: `output/audit_report.txt`, `output/audit_engine_accounting.txt`.

## 1. The one thing that WAS inflating the results (now fixed in this strategy's runner)

**The Elendel engine books `executed_weight[day] × close-to-close return[day]` for the same day.** Executed weights are end-of-decision weights, but fills happen at the open (entries) and at the stop level / open (exits):
* a position bought at the open of day *i* is credited the whole close-to-close return of day *i*, i.e. the overnight gap it never owned (mean +0.63% per entry here);
* a position stopped out or sold on day *j* has weight 0 on day *j*, so the move from the previous close to the actual exit fill is never charged. For the 385 stop exits that move averages **−5.1%** (the backtest uses intraday resting-stop semantics: it triggers on the low and fills at stop × (1−0.3%), or at the open on a gap-down). The "stop-return capping" block in the engine was written to charge exactly this, but it only works if the weight on the exit day is non-zero, which it never is — it is dead code.
Effect, measured three independent ways:
* closed trades booked by the engine contribute +2.085 of equity; buy-and-hold at the same trades' own fills gives +1.396 (1.49×); the corrected booking gives +1.231 (0.88×, difference = daily constant-weight positions vs buy-and-hold);
* an execution-faithful replay (only the entry-day and exit-day returns change, fills taken from the trade log) cuts CSM Value from **38.5% to 20.0% CAGR** (Sharpe 2.36 → 1.26, max DD −12.6% → −23.0%); the runner now books this way by default (`EXECUTION_FAITHFUL_ACCOUNTING = True` in `run_csm_value_backtest.py`; the replay `execution_replay.py` and the runner agree to 5 decimals);
* the same replay on the **live** engines (read-only, `audit_engine_accounting.py`, 2003-2026): Elendel 32.4% → 10.9%, Zenith 30.5% → 13.2%, Quad 26.1% → 6.3% CAGR; 2019-06→2025-06: Elendel 43.2% → 17.6%, Zenith 35.0% → 14.1%, Quad 25.0% → 1.7%. These engines are the user's; nothing in `Old_live_strategies` was changed. Note the live exit rule (`get_exit_signals`, stop on the close, exit next open) differs again from the backtest's intraday-stop assumption; compare against actual live P&L before trusting either.

## 2. Look-ahead checks — all clean
| Check | Result |
|---|---|
| Full-engine truncation: run on data cut at 2021-06 / 2022-12 / 2024-03 vs the full run | equity path **identical to 1e-10** up to the cut (signals, regimes, thresholds, vol scaling, stops, fills use no future data) |
| Entries strictly after the signal month-end; priced at that day's raw open; no NaN-open/stale fills; none on circuit-locked days | 544 / 544 trades pass (min gap 1 day, median 3); entry-open vs previous close +0.63% avg, open→close −0.11% (no favourable-gap selection) |
| Filing dates | lag after quarter end p5/median/p95 = 21 / 41 / 73 days; none before quarter end; 1.2% within 15 days; results used only from `filed_date`, trade next close |
| Delay / advance sensitivity of the information time (can the test see a leak?) | filings shifted +90 / +60 / +30 / 0 / −30 / −60 days: CAGR 11.5 / 13.7 / 18.6 / 20.2 / 27.2 / 29.0% — monotone; a 60-day look-ahead would be worth +8.8 points, the unshifted result sits where an honest one should |
| Residual unit leak: are held stocks over-represented among companies that split/bonus within the next 12 months? | held **2.3%** vs eligible universe 6.7% (under-represented) |
| Split-adjusted prices × filed share counts (the earlier leak) | restored to today's units; jumps >2× in market cap between filings fall 610 → 235; worth +5.0 CAGR points in the full window (+16 in train, −2 in test) |
| Corporate-action mask | 3,900 stock-months excluded; independently re-derived in tests #8a/#8b; negligible effect on returns |
| Net-profit definition | consistent reported net profit in every quarter (owners-attributable is reported for only 80% of consolidated / 10% of standalone filings and mixes definitions across quarters) |
| Price series | split/bonus-adjusted, spot checks (TCS 13-Sep-2019 close ₹2,142, ITC ₹240, COALINDIA ₹183, HUL ₹1,806) are in line with actual levels as I remember them, i.e. NOT dividend-adjusted (not independently verified: a web search did not return the historical closes) |

## 3. Is there an edge? (the honest part)
* **Permutation placebo** (E/P shuffled across stocks inside each month, same universe/eligibility/chassis/costs, 40 runs): random picks earn **13.8% CAGR / Sharpe 0.92**; the real strategy 20.0% / 1.26 — **+6.2 points, p = 0.07 (CAGR), p = 0.10 (Sharpe)**: suggestive, not significant at 5%. Most of the return is the universe/eligibility filters + the chassis, not the ranking.
* **Against its own universe**: the equal-weight eligible universe (no costs) earned 38.9% CAGR / Sharpe 1.62 / max DD −44.7%; CSM Value 20.0% / 1.26 / −23.0%. The strategy gives up return for half the drawdown; it does not beat the pool it picks from on return.
* Holdings are extreme: median purchase E/P 23.4% (P/E 4.3) vs 5.2% for the eligible universe (4.5× cheaper), 4% of purchases near the 50% cap. Top 5 trades = 21% of summed trade returns; mean trade 8.1% → 3.2% without the best 5%.
* Capacity is thin: median purchase has ₹3.5 cr daily traded value; a ₹5 cr book makes a 5% position 7% of daily value (39% of purchases above 10% of ADV); ₹10 cr: 60% above 10%.
* One six-year window, one cheap-cyclical regime, survivorship in the cheap end; residual unit mismatch for splits after the last filing (Dec-2024) cannot be removed from the data.

## 4. Corrected headline numbers (execution-faithful, Sharpe rf 0)
| | CAGR | Vol | Max DD | Sharpe |
|---|---|---|---|---|
| CSM Value FULL 2019-06→2025-06 | 20.0% | 15.7% | −23.0% | 1.26 |
| CSM Value TRAIN 2019-06→2021-12 (selection) | 28.7% | 15.4% | −19.8% | 1.74 |
| **CSM Value TEST 2022-01→2025-06 (scored once)** | **14.0%** | 15.9% | −23.0% | **0.92** |
| Elendel / Zenith / Quad, same full window (faithful replay) | 17.6 / 14.1 / 1.7% | | −33.0 / −25.1 / −35.6% | 1.08 / 0.97 / 0.19 |
| Elendel / Zenith / Quad, test window (faithful replay) | 4.0 / 2.6 / −8.7% | | −33.0 / −25.1 / −35.3% | 0.32 / 0.25 / −0.53 |
Correlation with the engines (faithful, daily): 0.68 / 0.65 / 0.71; market-residual 0.36 / 0.35 / 0.39; beta 0.69. Blend with their equal-weight trio (Sharpe rf 6%): value 0 / 10 / 20 / 30 / 50% → 0.42 / 0.48 / 0.54 / 0.60 / 0.71, max DD −30.4% → −21.2%.

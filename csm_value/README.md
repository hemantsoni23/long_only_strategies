# csm_value — CSM Earnings-Yield (Elendel chassis)

Long-only value strategy: buy cheap companies whose profits are still rising, no price-trend condition. Same engine and report as `csm_elendel_strategy.py` (inverse-vol sizing, hysteresis + swap gap, 3-layer stops, Crash Guard, vol target, regime leverage, T+1 fills, 0.3% cost, logs, IC/ICIR).

## Files (everything needed is in this folder + two data folders)
| File | Role |
|---|---|
| `csm_value_strategy.py` | the strategy class `CSMValue` (derived from the Elendel file by `_generate_elendel_chassis.py`; only the signal and universe differ) |
| `run_csm_value_backtest.py` | backtest runner / report (Elendel's, renamed) |
| `fundamentals_loader.py` | reads the raw NSE XBRL JSON directly and builds the point-in-time results table — **no cache, no other project** |
| `train_test_protocol.py` | design choices on TRAIN only, test scored once |
| `train_test_item5_7.py` | Items 5 and 7 (one-off filter, profit definition, idle cash) with train/test selection |
| `ablation_versions.py` | v1 / v2 / v3 data-handling ablation (table below) |
| `test_csm_value.py` | 18 checks (causality, independent E/P and mask re-derivation, unit consistency, accounting reconciliation, full-engine truncation, self-containment) |
| `audit_lookahead.py`, `audit_engine_accounting.py`, `execution_replay.py`, `AUDIT.md` | the adversarial audit and the execution-faithful replay |

Data: OHLCV CSVs `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data` and raw fundamentals `/Users/hemantsoni/Documents/stocks_fundamentals/fundamentals/*.json` (override with env `CSM_FUNDAMENTALS_DIR`). Parsing all 2,019 JSON files takes ~4 s per run, so nothing is cached.
Not used any more: `upstox_data_folder/pit_harness/cache/facts_quarterly.parquet`. (That folder exists — created 2026-09-08/09 — it is a separate "point-in-time harness" project whose `io_fundamentals.py` flattened these same JSON files into parquet caches. The earlier version of this strategy read its parquet; this version reads the JSON itself.)

## The signal and where each number comes from
E/P = **TTM net profit ÷ market cap**, where market cap = **month-end close (OHLCV) × shares outstanding (fundamentals)**:
* price — `close` from the OHLCV CSV, as in every other strategy;
* TTM net profit — sum of the last four consecutive quarterly results (reported net-profit line, same definition everywhere) from the JSON, each usable only from its `filed_date`;
* shares — `paid_up_equity_share_capital ÷ face_value_per_share` from the same filing (face value must be 0.5/1/2/5/10/100), restored to today's units (below).
So this is **not an OHLCV-only strategy**: it needs the fundamentals JSON. Eligible: liquidity ranks 301–1000, TTM profit > 0, latest-quarter profit rising year on year, E/P ≤ 50%, result no older than 140 days, no corporate-action cliff since that result. Rank by E/P, top 15, Elendel hysteresis/sizing/stops. No SMA-200 filter and no absolute-momentum gate.

## Headline numbers under both bookings (default configuration; Sharpe rf 0; `python3 report_both_bookings.py`)
Default = reported net profit, no one-off filter, **idle cash swept into a 6.5% liquid fund** (`use_liquid_mf=True`, as in Zenith; this was the only change adopted from Items 5/7).
| Window | Engine booking (headline; same convention as Elendel/Zenith/Quad backtests) | Execution-faithful booking |
|---|---|---|
| FULL 2019-06→2025-06 | **42.0% CAGR, vol 14.5%, Sharpe 2.53, max DD −11.8%** | 23.1%, 15.7%, 1.42, −21.3% |
| TRAIN 2019-06→2021-12 | 53.3%, 14.2%, 3.13, −11.5% | 32.6%, 15.4%, 1.93, −18.8% |
| TEST 2022-01→2025-06 | 34.3%, 14.7%, 2.11, −11.8% | 16.6%, 15.9%, 1.06, −21.3% |
(Before the idle-cash sweep: 38.5% / 2.36 / −12.6% engine and 20.0% / 1.26 / −23.0% faithful over the full window.) Use the left column when comparing with your other backtests (they share that booking); the right column is what the fills would have earned. The return booking code was not changed.

### Items 5 and 7 (earnings quality, profit definition, idle cash) — `train_test_item5_7.py`
Pre-declared grid, idle cash swept in every cell: profit definition {total, owners_consistent, core} × one-off filter {off, 50%, 25% of trailing pre-tax profit from other income + exceptional gains; banks exempt}. Selection = train (2019-06→2021-12) engine-booking Sharpe; test (2022-01→2025-06) scored once.
| Cell (engine booking: CAGR / Sharpe / max DD) | TRAIN | TEST | FULL |
|---|---|---|---|
| committed version (idle cash 0%) | 48.9% / 2.92 / −12.6% | 31.4% / 1.96 / −12.4% | 38.5% / 2.36 / −12.6% |
| **idle-cash sweep only = total profit, no filter (chosen on train)** | **53.3% / 3.13 / −11.5%** | **34.3% / 2.11 / −11.8%** | **42.0% / 2.53 / −11.8%** |
| total profit, one-off filter 50% | 51.5% / 3.03 / −11.6% | 32.5% / 2.03 / −13.3% | 40.2% / 2.45 / −13.3% |
| total profit, one-off filter 25% | 48.4% / 2.91 / −10.9% | 31.7% / 1.99 / −14.3% | 38.5% / 2.37 / −14.3% |
| core profit (less other income & exceptionals), no filter | 49.2% / 2.94 / −11.4% | 34.0% / 2.12 / −12.6% | 40.2% / 2.46 / −12.6% |
| core profit, one-off filter 50% / 25% | 49.1% / 2.94 ; 48.1% / 2.87 | 31.6% / 1.99 ; 31.5% / 2.00 | 38.7% ; 38.2% |
| owners_consistent, filter off / 50% / 25% | 44.7% ; 42.9% ; 45.4% | 27.0% ; 28.9% ; 26.1% | 34.2% ; 34.6% ; 33.9% |
Reading: the idle-cash sweep adds ~3.5 CAGR points (engine) / ~3.1 (faithful) mechanically. **None of the earnings-quality variants beat the plain reported net profit on train or test**: the one-off filter and the core-profit definition are neutral to negative, and owners-attributable profit (consistent version) is worse by ~8 points. The earlier observation that purchases with other income above 30% of profit earn less (4.9% vs 8.7% per trade) did not turn into a portfolio improvement once those names were removed. All the differences are within the placebo noise (sd ≈ 4 CAGR points), so they are not evidence either way. The options stay in the code (`profit_basis`, `max_oneoff_share`), off by default. Two Item-7 points were left as they are: standalone→consolidated switching (the switch is causal and consolidated is the right base for a group's market cap) and the 13 days of executed weight above 100% (engine behaviour).

## Look-ahead / data audit (what was found and fixed)
1. **Split-adjusted prices × unadjusted share counts — a real leak, fixed.** The OHLCV prices are retroactively split/bonus-adjusted (HDFCBANK shows ~₹550 in 2019; it traded above ₹1,100 after its 2019 split). A 2019 filing's share count is in 2019 units, so adjusted-price × filed-shares understates market cap by every later split/bonus — stocks that later split look 2–10× cheaper in the past (future information). `fundamentals_loader.py` multiplies each filing's share count by the clean split/bonus ratios (1.5, 2, 2.5, 3, 4, 5, 10 or reciprocals, ±3%) visible in later filings, restoring the units the prices are already in; genuine issuance/mergers are left alone. Check: for 458 companies with detected splits, jumps >2× in market cap between consecutive filings fall from 610 to 235 (`test_csm_value.py` #6).
2. **Corporate-action mask (new, in the spirit of the runner's `mask_corporate_actions`).** A *cliff* is a one-day price move that matches a clean split/bonus (−33%, −50%, −60%, −67%, −75%, −80%, −90%, or a clean reverse-split jump, ±3 points) or a day the runner already NaN'd (move outside [−40%, +300%]). It is used twice: (a) a split seen in the filings is restored **only if the price series was adjusted** for it (no cliff around it) — if the vendor left it unadjusted, prices and filings already agree and nothing is restored; (b) a stock-month is **excluded** when a cliff occurred after the latest filing it uses (the filed share count is then stale): 3,900 stock-months. Independently re-derived in tests #8a/#8b.
3. **Net-profit definition must be the same in every quarter.** Profit "attributable to owners" is reported in only 80% of consolidated and 10% of standalone filings, and 1,053 of ~1,600 consolidated companies mix both across quarters, so "owners, else total" corrupts trailing sums and year-on-year growth. The default is now the reported net-profit line (`profit_basis='total'`, same definition everywhere); its limitation is that minority interests are included. (A rewrite of the loader on 2026-10-08 briefly used the inconsistent "owners" form; that is what produced the interim 30.0% / 1.93 figure.)
4. **No cache, no other project.** The loader reads the raw JSON directly; `test_csm_value.py` #7 fails if any file here touches `pit_harness`, parquet/pickle caches or another project's code.
5. Timing: a result counts only from its filing date and the trade is the next close; out-of-order and >120-day-late filings are dropped; truncating the data at any date reproduces identical signals/positions up to it (test #2).
6. **Residual that cannot be fixed from the data:** a split/bonus *after* the last filing (results end Dec-2024) that the vendor *did* adjust leaves historical share counts in old units for that stock; no cliff and no filing reveals it (volume is adjusted too, so it carries no information; I tested this). Upstox corporate actions are not available, so this stays as a known, small bias (it makes some historical E/P too high). Also shared with the live strategies: survivorship and split-adjusted `min_price`.

### Ablation — what each data fix is worth (same chassis and configuration, execution-faithful accounting, Sharpe rf 0)
| | FULL 2019-06→2025-06 | TRAIN 2019-06→2021-12 | TEST 2022-01→2025-06 |
|---|---|---|---|
| v1 leaky (raw filed shares) | 25.2% / 1.54 / −26.2% | 44.3% / 2.61 / −16.7% | 12.8% / 0.83 / −24.1% |
| v2 units restored | 20.2% / 1.27 / −23.0% | 28.1% / 1.71 / −19.9% | 14.8% / 0.95 / −23.0% |
| **v3 + corporate-action mask (default)** | **20.0% / 1.26 / −23.0%** | 28.7% / 1.74 / −19.8% | **14.0% / 0.92 / −23.0%** |

## 7. Engine accounting (the largest correction) — see `AUDIT.md`
The Elendel engine books executed weight × same-day close-to-close return, which credits entry gaps the buyer never owned and never charges the move from the previous close to a stop fill (−5.1% on average, 385 stops; I re-checked this independently: stop-exit trades average +7.8% as booked by the engine vs +1.5% at their actual fills). **Both bookings are always computed and printed** (`Accounting cross-check` block of the report, `report_both_bookings.py`); `EXECUTION_FAITHFUL_ACCOUNTING` in `run_csm_value_backtest.py` only chooses the headline, and is **False** so the headline is directly comparable with the Elendel / Zenith / Quad backtests (same booking). The tables below that say 'faithful' use the other booking.

## Train / test
Requested: train 2002–2013, test 2014–2025. **Not possible for this signal** — the fundamentals start with FY2018-19 results, so TTM earnings exist only from 2019 (the code runs unchanged if you obtain older results). Instead (`train_test_protocol.py`): **TRAIN 2019-06-03 → 2021-12-31** chooses among 8 pre-declared configurations (net-profit definition × liquidity-rank floor {1, 301} × rising-profit filter on/off) by train Sharpe; **TEST 2022-01-03 → 2025-06-30** is scored for the winner only.
Train winner (unchanged by the accounting fix): total profit, ranks 301–1000, growth on — train CAGR 28.7%, Sharpe 1.74. **Test: CAGR 14.0%, vol 15.9%, Sharpe 0.92, max DD −23.0%, Calmar 0.61.** The other seven configurations on test (not used for any choice): CAGR 6.1%–18.2%. Limits: the E/P idea and the candidate list came from earlier looks at 2019–2025; the train window is 31 months.

## Final result (defaults = train winner; Elendel report layout; execution-faithful; Sharpe rf 0)
| | CAGR | Vol | Max DD | Sharpe | Calmar |
|---|---|---|---|---|---|
| **CSM Value, FULL 2019-06→2025-06** | **20.0%** | 15.7% | **−23.0%** | **1.26** | 0.87 |
| **CSM Value, TEST 2022-01→2025-06** | **14.0%** | 15.9% | −23.0% | 0.92 | 0.61 |
| Elendel / Zenith / Quad, full window, same faithful booking | 17.6 / 14.1 / 1.7% | | −33.0 / −25.1 / −35.6% | 1.08 / 0.97 / 0.19 | |
| Elendel / Zenith / Quad, test window, same faithful booking | 4.0 / 2.6 / −8.7% | | −33.0 / −25.1 / −35.3% | 0.32 / 0.25 / −0.53 | |
544 trades, win rate 50%, median trade −0.1%, payoff 2.5, avg MAE −7.5% / MFE +28.8%; factor IC (1m) +0.018 (t 1.0), 12m +0.071 (NW-t 2.8): a slow signal.
Correlation with the engines (daily, faithful): 0.68 / 0.65 / 0.71; market-residual 0.36 / 0.35 / 0.39; beta to the market 0.69. Blend with their equal-weight trio (Sharpe rf 6%): value 0 / 10 / 20 / 30 / 50% → 0.42 / 0.48 / 0.54 / 0.60 / 0.71, max DD −30.4% → −21.2%.

## Is there an edge? (permutation placebo, `AUDIT.md`)
Shuffling E/P across stocks inside each month (same universe, eligibility, chassis, costs; 40 runs) gives 13.8% CAGR / Sharpe 0.92 for random picks; the real strategy is +6.2 CAGR points above that, **p = 0.07 (CAGR) / 0.10 (Sharpe) — suggestive, not significant at 5%**. It also earns less than the equal-weight pool it picks from (38.9% CAGR before costs, but with a −44.7% drawdown vs −23.0%).

## Verdict
Implemented, self-contained and leak-audited (14 unit tests + the adversarial audit pass; the full engine is identical when the future is cut off). After the accounting correction it is a modest strategy: 20% CAGR / Sharpe 1.26 over the window, 14% / 0.92 on the held-out 2022-25 test, better than the live engines on the same faithful booking, but its ranking edge over random picks is not statistically established and capacity is thin (a ₹5 cr book makes a 5% position 7% of typical daily value). Treat as a paper-trading candidate, not a proven edge.

## Run
```
python3 run_csm_value_backtest.py       # Elendel-style report + logs/plots in ./output (git-ignored)
python3 train_test_protocol.py          # train/test table -> output/train_test_report.txt
python3 ablation_versions.py            # what each data fix is worth
python3 test_csm_value.py
```

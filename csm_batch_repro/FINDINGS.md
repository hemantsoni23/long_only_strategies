# CSM Batch: why the old v2.4 report (24.11% CAGR) doesn't reproduce

Nothing in `Old_live_strategies/` was edited. All patched copies live here (`bt_x.py`, `strat_x.py`).
Data: `upstox_data_folder/ohlcv_data`, 5,205 symbols. Window: load 2003-01-01, report 2004-01-01 to 2012-12-31. txn 0.3%.

## 1. The pasted report is not the current config
Pasted "CSM BATCH v2.4" = `csm_stock_strategy.py` + `run_csm_stock_backtest.py` (final_momentum_strategies/):
top_n=15, min_hold_days=5, vol_target=0.15, monthly rebalance, trailing ATR stops always on, report 2003-2012, data folder `output_stocks` (no longer on disk).
The current runner is a different strategy: top_n=30, `use_trailing_stop=False`, quarterly rebalance, rank-exit on, report 2013-2025.
Its trade count / win rate / profit factor (1467 / 44.65% / 1.085) match the "BATCH v2.4 (ref)" row in `csm_quad/run_*.py`, where CAGR is 19.41% at rfr=0.
So 24.11% = the same trade set with idle cash earning ~8% (+4.7 pts; original engine here: +5.1 pts for 8%).
Sharpe 1.515 only reconciles with an excess return over a ~7-8% rfr, not 0 and not clearly 6%.

## 2. Engine regression test (same data, same window, v2.4 parameters, rfr=0)
Factors and target positions are bit-identical between the original and modular code (max abs diff 0.0, 107/107 rows).
All divergence is in the daily engine / booking.

| Variant | CAGR | MDD | Vol | Trades |
|---|---|---|---|---|
| Original v2.4 engine | 20.17 | -25.9 | 10.04 | 1394 |
| Modular `csm_batch_backtest.py` as-is | 11.35 | -29.2 | 9.23 | 1418 |
| Modular `csm_batch_backtest1.py` (decide close, fill next open) | 11.74 | -34.0 | 11.46 | 1190 |
| ... entry-gap credit restored | 12.71 | -32.7 | | |
| ... exit-gap charge removed | 15.38 | -21.3 | | |
| ... both booking changes undone | 16.79 | -25.2 | | |
| ... + ATR not lagged (original) | 19.93 | -25.0 | 9.15 | 1388 |

Three causes, in order of size:
1. **Exit-gap not charged (about +4 pts).** Original exit-day weight is 0, so the prev-close to open move on a stop/rebalance/crash exit is never booked. Modular charges it.
2. **ATR same-day (about +3 pts).** Original `self.atr` has no `.shift(1)`, so the stop uses today's true range (lookahead). Modular lags it one day.
3. **Entry-gap credit (about +1.4 pts).** Original books entry day close-to-close from prev close, though the fill is the open. Modular books close/open.

Residual vs original: 0.2 pt CAGR, 6 trades, 0.9 pt vol (unexplained; not chased).

## 3. What this means
The modular files are the honest version, not a broken one. Honest v2.4 on this data: about 11-12% at rfr=0, about 16-17% with 8% cash yield.
Max drawdown differs a lot (-14.4% pasted vs -25% here) and the 2007/2008 years differ too (pasted 16.2 / +3.6 vs 16.2 / -16.5 here).
The `output_stocks` dataset is gone, so that part can't be traced.

## 4. Current runner as written (top_n=30, no trailing, quarterly, rfr=0, txn 0.3%)
2013-2025: CAGR 9.19%, MDD -41.6%, Sharpe 0.73, 1780 trades. 2004-2013: CAGR 21.1%, MDD -35.1%. Not investigated further.

Reproduce: `python3 decomp.py`, `decomp2.py`, `decomp3.py`, `mimic.py` (first run builds `data.pkl`, ~20 s).

## 5. Why the current runner gives 9.2% / -41.6% on 2013-2025 (top_n=30, no trailing, quarterly, rfr=0, txn 0.3%)
Engine: `csm_batch_backtest1.py`. All variants below are in-sample explorations, not selected configs.

**Ruled out**
- *Unadjusted splits / bad ticks.* Raw data has unadjusted corporate actions (BCP 5:1, AURUM, FORBESCO, CRSL, RANDER, STAR demerger) and one-day bad-tick spikes (TIL x50). A generic symmetric adjuster (`generic_adjust.py`, 762 events) only moves CAGR 9.19 -> 9.61 and leaves MDD about -42%. Standard-ratio detectors: 9.15-9.17.
- *Warm-up.* Crash-guard threshold is an expanding 95th pct learned from the load window; with `start_load=2012` it trips 46-58 days/yr in 2014-2016 and 0 days in 2018/2019/2021/2023. Loading from 2003 fixes that, but CAGR stays 8.4-9.4% and MDD -40..-42% for every load start (`warm.py`).

**What the loss actually is**
- Drawdown is a grind, peak 2018-01-11 to trough 2020-05-18: Sep-2018 -14%, Jul-2019 -9%, Mar-2020 -16.6%. Years: 2018 -22.9, 2019 +3.1, 2022 -19.6, 2025 -22.6; good years 2014 +39, 2017 +53, 2021 +56, 2023 +43.
- Costs: turnover ~923%/yr x 0.3% one-way = ~3.1 pts/yr (CAGR 12.3% at zero cost).
- Exits over the window: STOP_HIT 548 trades, avg -16.1%, contribution -228; REBALANCE 808 trades, avg +14.9%, contribution +348. Stops fill at next open (close-triggered), so the "15%" stop averages -16%.
- Idle cash: avg allocation ~66% earning 0 at rfr=0; at ~7% that adds roughly 2-2.5 pts.
- A real illiquidity case is in the drawdown: PREMSYN entered 2018-09, then 108 lower-circuit days (1-share volume), exited -93% at 4% weight (-3.7 pts of equity).

**Lever sweep, 2013-2025 (baseline 9.19 / -41.6)**
| Change | CAGR | MDD |
|---|---|---|
| trailing stop ON | 4.26 | -44.5 |
| v2.4 params | 3.04 | -48.1 |
| monthly rebalance | 7.88 | -38.5 |
| rank exit off | 8.77 | -43.4 |
| crash guard off | 11.34 | -39.5 |
| vol target off | 10.51 | -48.0 |
| hard stop 10% / 25% | 8.89 / 9.25 | -42.4 / -43.1 |
| top_n 15 | 8.26 | -40.1 |
| universe_top_n 500 / 300 | 9.04 / 10.15 | -40.2 / -35.0 |
| old same-day-stop engine (flattering booking) | 15.76 | -31.2 |

No single lever gets drawdown under -35%. `top_n=50` shows 24% CAGR / 59.6% vol only because of two TIL bad ticks (+168%, +124% days): ignore it.

**Read**: no bug here. The config is a small/mid-cap momentum book that gets caught by the 2018-19 and Mar-2020 reversals, pays ~3 pts/yr in costs, and its stops lose more than they save. The old same-day-stop engine would show 15.8% for the same config, which is the booking inflation from section 2.

## 6. Exit-day booking: do the other engines differ from batch, and does it explain the weak result?
**Other engines** (read, not edited): Zenith (`run_csm_zenith_backtest.py` ~1274) fixes the entry day (close/entry_fill - 1) and states "Exit days are unchanged (weight 0 on the exit day)". Elendel and Quad only have the stop-return cap (a no-op when exit-day weight is 0) and no entry fix. `csm_absolute_backtest.py` patches the exit-day return but its exit-day weight is also 0, so nothing is booked.
**Batch** (`csm_batch_backtest1.py` ~503-575): same entry fix as Zenith, plus one extra line that adds `prev_weight * (open_exit / prev_close - 1)` on every exit day. That line is the only difference in exit-day treatment.

Current runner config, `bt1_x.py` (copy with switches), rfr=0, txn 0.3%:
| Booking | 2013-25 CAGR | MDD | 2004-13 CAGR | MDD |
|---|---|---|---|---|
| as written (entry fix + exit gap charged) | 9.19 | -41.6 | 21.10 | -35.1 |
| Zenith-style (entry fix, exit day = 0) | 8.88 | -37.4 | 20.58 | -32.1 |
| raw, no fixes (Elendel/Quad-style) | 10.47 | -33.5 | 21.36 | -32.6 |

Exit-day gap (open / prev close - 1) by exit reason, 2013-25, per trade: REBALANCE 808 trades mean +0.55% (rebalance exits tend to gap up); CRASH_GUARD 396 mean -0.62%; STOP_HIT 548 mean -0.21%. Weighted sum over the window about +4 pts of equity in total (+0.3 pt/yr): net a small gain, not a drag.

**Read**: the exit-day charge is not what makes the batch result weak. Setting the exit day to 0 lowers CAGR by 0.3 pt (rebalance gaps are favourable) and trims MDD by about 4 pts (it deletes the crash-guard gap losses, mostly Mar-2020). The biggest single booking item on this config is the entry fix (about 1.6 pts). Even with no booking fixes at all the result is 10.5% / -33.5%. Weight 0 on the exit day is equivalent to assuming the exit filled at the previous close, which contradicts the batch rule "decide at close, fill next open"; so it improves drawdown optics rather than reflecting data that is missing.

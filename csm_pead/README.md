# csm_pead — PEAD Confirmed-Drift (event-driven, long-only)

Standalone strategy + backtest module (`pead_strategy.py`, `pead_fundamentals.py`, `run_pead_backtest.py`, `test_pead.py`), same layout as the live strategies; `Old_live_strategies` untouched.

## Rules
Event = a quarterly result (point-in-time `filed_date`). Signal day S = 2nd trading day after the filing. **Buy** when standardised unexpected EPS (SUE) and the announcement return (stock minus equal-weight benchmark, close d−1 → d+2) are **both** in the top 30% of liquid events filed in the previous 120 days
(thresholds trailing, pool ≥ 150). Enter at the close of S+1 (up to 5 days later if no slot), best score first; 20 slots at 1/20; liquid universe (rank ≤ 1000, price > ₹20, circuit-checked); hold 60 trading days; −15% hard stop (next open, 0.3% slippage); idle cash 6.5%; 0.3% per side.

## Results (2020-09 → 2025-06, 4.8 years, defaults fixed in advance)
Signal quality (causal, no portfolio constraints): 1,637 BUY signals earn **+2.6% excess over 60 days vs the equal-weight liquid universe (t 2.6)**, positive in 2020–2024 (+5.3, +3.1, +2.0, +3.4, +1.8; 2025 −0.3), win rate 47% (a skew signal).
As a portfolio: CAGR 31.6%, vol 19.6%, **Sharpe 1.20**, max DD −25.5%, 415 trades, win rate 57%, avg trade +7.0%, ~90% invested. Sensitivity (all reported): Sharpe 1.07–1.56 (30 slots 1.51, no stop 1.40, hold 90d 1.42, top-20% signal 1.56; 40d hold 1.23, 10 slots 1.09; 2× costs 1.07). The better variants were found after looking and are not the defaults.
**Correlation and blend (`output/pead_report.txt`):** daily correlation with Elendel/Zenith/Quad **0.73 / 0.71 / 0.69** (monthly 0.72–0.78); beta to the liquid equal-weight market 0.87 (corr 0.86). It does **not** meet the break-even rule (1.20 vs 0.73 × 2.14) and **lowers** the live trio's Sharpe at every weight (2.08 → 2.00 at 10%).
**Verdict: built and tested, but not recommended as a new strategy** — the drift signal is real but the portfolio is an undiversified, fully invested market-beta book with a lower Sharpe than the live engines. Use cases that remain: the bad-news veto for the momentum books, or a beta-hedged/more selective version (not tested).

## Elendel-style report (`run_csm_pead_backtest.py`)
PEAD is event-driven, so it keeps its own event loop (like your HR/VCP breakouts) instead of the monthly Elendel engine, but everything you read is Elendel's: `elendel_style_report.py` is generated from `run_csm_elendel_backtest.py` (`_generate_report_style.py`) — portfolio metrics (CAGR, avg drawdown, Sharpe/Sortino/Calmar with rf = 0), three win-rate views, trade statistics with MAE/MFE, exit/entry-reason/regime breakdowns, turnover, yearly returns with yearly max/avg drawdown, 5-panel chart + monthly heatmap, daily log, Elendel-column trade log, plus an event-level IC/ICIR table (signal vs forward 20/40/60-day return inside each filing month).
`python3 run_csm_pead_backtest.py` (2020-09-01 → 2025-06-30): CAGR 30.8%, vol 19.6%, max DD −25.5%, Sharpe 1.50 / Sortino 2.01 / Calmar 1.21 (rf 0), 395 trades, win rate 58%, payoff 1.8, profit factor 2.4, avg MAE −10.2% / MFE +22.7%; exits: hold expiry 300 (avg +14.9%), stop 95 (avg −17%); PANIC-regime entries average −0.5%.
Event IC: SUE+EAR 60d +0.077 (ICIR 0.91, hit 88%, NW-t 6.0); EAR alone 40d +0.076 (ICIR 0.93); SUE alone is slower (20d +0.014, 60d +0.063).
Same-window comparison (rf 0): Elendel 48.0% / 2.74 / −12.8%, Zenith 38.0% / 2.45 / −11.9%, Quad 25.2% / 1.67 / −15.9%, CSM Value 48.4% / 2.77 / −12.6%, **PEAD 31.1% / 1.50 / −25.5%** — PEAD lacks the Elendel chassis' regime scaling, vol target and Crash Guard, which is the main reason its drawdown is twice as deep.

## Checks (`python3 test_pead.py`, all pass)
Filing precedes signal and entry follows signal; truncating data at 2023-06 reproduces the same BUY signals/thresholds and identical equity; `get_exit_signals` matches the simulation on all 415 trades (hold the day before, exit on the decision day, same reason); ≤ 20 positions, weights ≤ 1, no double entry, universe test at entry, trailing pool ≥ 150.

## Use
```
python3 run_pead_backtest.py [--sensitivity]
python3 diag_event_alpha.py        # causal per-signal alpha;   python3 diag_correlation.py   # where the correlation comes from
```
Live: `get_entry_candidates(as_of)` (eligible signals, best first) and `get_exit_signals(portfolio, live_data, today)`. Needs a refreshed quarterly-results feed (data ends with results filed 2025-04).

## Data caveat (added 2026-10-08)
SUE is built from per-share EPS differences; around a split or bonus a quarter's EPS is in different units from the year-ago quarter, which creates spurious surprises. This has not been audited or corrected (the market-cap unit fix in `csm_value/fundamentals_loader.py` does not apply here). Treat the PEAD numbers as unaudited for that effect.

Note (2026-10-08): PEAD's own event loop books entries at the close, stops at the next open and cash/shares explicitly, so it does not share the Elendel engine's same-day booking issue (see `csm_value/AUDIT.md`).

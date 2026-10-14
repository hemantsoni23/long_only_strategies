# Crestline v2.6 - Zenith's exit convention inside Crestline (2026-10-13)

Request (user): make Crestline exit like Zenith (the live engines' convention), accepting that exit-day P&L cannot be resolved with daily OHLCV. v2.5 and every other Crestline file are untouched; v2.6 is generated from v2.5 by `make_v26.py` (asserted patches). Tests: `test_v2_6.py` (9 checks, all pass). Raw: `results_v26.csv`, `v26_headline.csv`, `v26_report_out.txt`.

## What EXIT_MODE does
| mode | trigger | execution | booked |
|---|---|---|---|
| **zenith (default, as requested)** | today's LOW vs the stop in force (state through the previous bar; Crestline's own hard 20% / peak 15% / vol-scaled levels) | closed today at stop level x (1 - 0.3%), or at the open if the day gaps through it; locked (high == low) days defer; a position is first tested the day after entry | **at the PREVIOUS CLOSE** - exit-day weight is 0, so the move from the previous close to the fill is never charged. Rebalance exits are booked the same way. |
| honest (= v2.5) | close vs the stop, flagged at the close | next open | at the next open, gap booked |
| resting | as zenith | as zenith | at the fill (gap charged) - the bridge |
Each run prints/stores **"Exit P&L NOT booked %/yr"** (sum of shares x (logged fill - booked price) / average equity / years). Change mode with `CL_OVR='{"EXIT_MODE":"honest"}'`.

## Tests (all pass)
honest == v2.5 bit-exact (2 anchors); zenith stop exits booked at the previous close while the logged fill is lower (1,563 stops, mean fill -4.84% vs previous close); fills never above the stop level (87% at level x 0.997, 13% gap-through opens); no stop on the entry day; resting books at the fill; hidden P&L: zenith -13.3%/yr, resting 0, honest 0; no look-ahead (truncation at 2019-12-31 leaves earlier equity unchanged).

## Results (gold sleeve 25% at the 8%/yr planning case, idle cash 0%, 6 anchors, 2006-25, Sharpe rf = 0)
| book | convention | CAGR | Sharpe | MaxDD | Calmar | stock exposure | P&L not booked |
|---|---|---|---|---|---|---|---|
| 1 lakh | **zenith** | **24.0%** | **2.68** | **-12.8%** | 1.87 | 40% | -13.4%/yr |
| | resting (gap charged) | 8.5% | 0.92 | -25.0% | 0.34 | 41% | 0 |
| | honest next-open (v2.5) | 16.8% | 1.51 | -27.2% | 0.62 | 52% | 0 |
| 1 cr | zenith | 16.6% | 2.31 | -10.2% | 1.62 | 30% | -10.7% |
| | resting / honest | 6.3% / 11.6% | 0.77 / 1.25 | -23.1% / -21.4% | | | |
| 5 cr | zenith | 12.3% | 2.02 | -8.6% | 1.43 | 23% | -8.1% |
| | resting / honest | 5.1% / 8.6% | 0.72 / 1.10 | -19.2% / -16.1% | | | |
| 20 cr | zenith | 9.0% | 1.75 | -6.6% | 1.36 | 17% | -5.7% |
| | resting / honest | 4.0% / 6.2% | 0.68 / 0.97 | -14.5% / -12.8% | | | |
No gold, 1 lakh: zenith 22.6% / 2.72 / -13.3%; resting 7.2% / 0.82 / -25.8%; honest 15.4% / 1.45 / -29.4%.
Stock exposure is lower and holds shorter under the intraday trigger (mean hold 51.5 vs 71.1 calendar days, 1,636 vs 1,488 exits at anchor 0): intraday lows breach 10-15% trailing stops far more often than closes do.

## How to read it
* The zenith number now looks like the live engines (Sharpe 2+, MaxDD -13%) - that is the convention, not an improvement: with the SAME trigger and fills but the gap charged, the strategy earns 8.5%; the honest next-open execution earns 16.8%. About 13 CAGR points at a lakh-scale book (5.7 at 20 cr, because less capital is in stocks) are never booked.
* The convention also changes behaviour (intraday trigger -> more, earlier exits), not just accounting.
* Quote zenith-mode figures only with the honest line beside them. The gold-sleeve results from the previous round were measured under the honest mode and are unaffected.

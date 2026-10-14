# Gold / silver ETFs for Crestline's idle capital - pre-registration (written 2026-10-13, BEFORE any gold number was computed)

Idea (user): the core logic cannot raise exposure (avg ~51% at tiny size, 20-40% at realistic size), so give the idle capital a second, low-correlation asset class - gold/silver ETFs.
Approach 1: gold/silver as extra candidates in the SAME core ranking. Approach 2: a separate simple trend/momentum sleeve for gold/silver funded by idle cash, with more gold in bad regimes (bear / panic).
Base B = `crestline_v2_4.py` (25 names, 2006-25, CA_ADJUST, idle cash at 6.5% liquid fund). 6 schedule anchors. Gating metric Sharpe vs 6.5% (Sh65).

## Data facts established before design (gold_silver_ohlcv_data)
* Every gold/silver ETF file has ZERO rows in 2011-2014 (4-year gap, also found by the earlier gold study). GOLDBEES: 2007-03..2010-12 and 2015-01..; no value is ever forward-filled across the gap.
* Silver ETFs start 2022-02 (SILVERBEES, ~Rs 56 cr/day; SILVERIETF 10, SBISILVER 6): ~3.9 years inside the strategy window. Silver is reported DESCRIPTIVELY only and can never carry an adoption.
* Instruments: GOLDBEES (Rs ~65 cr/day since 2023), SILVERBEES. One ETF per metal (the other gold ETFs are near-identical and would only duplicate positions; they matter only for sleeve capacity, noted).
* GOLDBEES close 22.8 (2015) -> 110.1 (2025): a strong INR gold bull (+72% in 2025). Sample drift is the main danger to honest evaluation.
* GOLDBEES traded below Rs 20 (the strategy's price floor) until ~end-2010, and post-gap price windows would be stale: for Approach 1 an ETF is eligible only after 240 genuine (non-filled) observations in the last 252 bars.

## Part 0 - descriptive: is the correlation really low, and when?
Daily-return correlation of GOLDBEES with (a) the equal-weight stock index, (b) each v2.4 book (6 anchors), overall and by engine regime (bear / panic / other), by period (2007-10, 2015-25), plus rolling 1-year; gold return in the worst 10 equal-weight-index drawdown episodes. No gate; it tests the premise (user: ~0.19).

## Part A - the sleeve (Approach 2), exact post-processing of the stock engine
Valid because the stock decisions never depend on cash (stops, entries, overlay use the equity book only; the engine only needs cash to settle entries, and a sleeve sale at the open funds them). Per run the engine writes daily equity, invested fraction and the bear/panic flags.
Gold weight a_t (fraction of equity) is decided at the close of t-1 and held through t: a_t = idle_{t-1} x m_t, where idle_{t-1} = 1 - invested fraction at the close of t-1 and m_t is the variant's multiplier. The rest of idle cash stays in the 6.5% liquid fund. Trades only when |target - current| > 2% of equity (deadband); cost 0.15% one-way on traded notional (stress 0.30%). Gold is forced down immediately if idle_{t-1} falls below the held weight. In the gap and for 200 valid days after it, m_t = 0.
Signals (data to the close of t-1 only): S_sma = GOLDBEES close > its 200-day SMA; S_per = share of the last 126 valid days with close > its 50-day SMA is >= 0.5. Windows touching missing data are invalid (-> 0).
| id | multiplier m_t |
|---|---|
| G1 | 0.5 always (static half of idle cash; the no-timing control) |
| G2 | S_sma |
| G3 | S_per |
| G4 | S_sma x (1.0 if engine regime is BEAR or PANIC, else 0.5) |
| G5 | S_sma x 1[BEAR or PANIC] |
| G6 | min(idle x S_sma, 10% of equity) |
Book sizes: INITIAL_CAPITAL 1 lakh, 1 cr, 5 cr, 20 cr (idle share rises with size: ~49 / 61 / 71 / 79%). Each variant is compared with G0 (all idle in the liquid fund) at the SAME size and the SAME anchors.
DRIFT CONTROL (the part that decides honesty): each variant is also run with gold's excess return over the liquid fund scaled down - lambda = 0.5 (half drift) and 1.0 (zero drift): r'_g = r_g - lambda x (mean(r_g) - cash_d), mean over all usable gold days. A variant earns its place only if it is not just owning gold's bull market.
### Adoption (per book size; all must hold vs G0)
* A1: real-drift dSh65 >= +0.08 on the full 2006-25 window (gap years equal G0 by construction)
* A2: dSh65 > 0 in BOTH P_A (2006-14; effect exists only in 2007-10) and P_B (2015-25)
* A3: dSh65 > 0 in >= 5 of 6 anchors
* A4: mean MaxDD no more than 3 pts worse than G0
* A5 (drift): half-drift dSh65 >= +0.03 AND zero-drift dSh65 >= -0.01
* A6 (cost): at 0.30% one-way, dSh65 still > 0
Silver sleeve (descriptive only, 2022-02..2025-12): S1 = same as G2 on SILVERBEES; reported next to gold over the same window.

## Part B - gold/silver inside the core ranking (Approach 1)
Engine change: GOLDBEES (and SILVERBEES) enter the price/volume panel as ordinary columns and are scored, ranked and traded exactly like stocks (same universe filters; eligibility rule above; excluded from the equal-weight benchmark so the regime flags do not move). Variants: R1 = GOLDBEES + SILVERBEES, R2 = GOLDBEES only. Book sizes 1 lakh and 1 cr. Same drift control: lambda 1.0 rebuilds each ETF's price path with zero excess drift before the engine sees it.
Adoption vs B at the same size: N1 dSh65 >= +0.08, N2 both periods positive (P_A will have no ETF trades: the price floor and the eligibility rule exclude them - reported), N3 >= 5/6 anchors, N4 MaxDD within 3 pts, plus zero-drift dSh65 >= -0.01. Mechanism check: share of days with an ETF position and its share of P&L.

## Combination (only if both parts pass something): the passing sleeve variant on top of the passing ranking variant, judged vs each alone with N1-N4.

## Caveats stated in advance
One gold bull market in the usable sample (2015-25 CAGR ~17% in INR); 2011-14 unobserved; January 2026-type -10% gap days exist; the earlier study found no gold timing edge (best signal t 1.1) and a small drift-driven gain on near-fully-invested engines - Crestline has far more idle cash, so the room is larger but the risk of mistaking drift for skill is the same. Taxes on ETF churn are not modelled. Sleeve capacity: GOLDBEES alone supports a few crore a day at 5% of its volume; larger books need to split across GOLDIETF / SETFGOLD / HDFCGOLD (~Rs 12 cr/day each). ~20 comparisons: expect ~1 spurious pass. In-sample, no lockbox.

## Post-look change log
* Engine definition fix found by test 3 BEFORE any gold result: ETF columns are joined on the existing stock calendar (left join) - an outer join added ETF-only dates and shifted every bar.
* Extra descriptive diagnostic (no decision attached): gold's excess return on G5's own days by period, to explain the G5 result.
* Outcome vs the pre-registered gates: Part A passes in exactly one cell (G6 at the 20 cr book); Part B passes nothing; no combination test (needs both parts).

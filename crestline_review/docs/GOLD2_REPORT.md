# Gold sleeve under conservative accounting (idle cash at 0%) - v2.5 (2026-10-13)

Instruction followed: no 6.5% on idle cash while developing the strategy; Sharpe measured at rf = 0; gold/silver ETFs are how idle capital is put to work.
Protocol `PREREG_GOLD2.md` (fixed before the numbers; one openly labelled post-look). Code: `gold_study2.py` (post-processing study), `gold_sizing_study.py`, `make_v25.py` -> `crestline_v2_5.py` (native sleeve), `test_v2_5.py` (11 checks, all pass), `experiments_v25.py`, `v25_report.py`. Raw: `gold2_*.csv`, `results_v25.csv`, `v25_headline.csv`, `*_out.txt`.

## 1. The honest baseline (v2.4, idle cash at 0%, 6 anchors, 2006-25)
| book size | CAGR | Sharpe rf=0 | MaxDD | Calmar | stock exposure |
|---|---|---|---|---|---|
| 1 lakh | 15.4% | 1.45 | -29.4% | 0.52 | 52% |
| 1 cr | 10.4% | 1.18 | -23.0% | 0.45 | 41% |
| 5 cr | 7.4% | 1.03 | -17.2% | 0.43 | 32% |
| 20 cr | 5.0% | 0.89 | -14.3% | 0.35 | 24% |
The 18.8% quoted earlier contained ~3.5 points of cash interest. (Information item: TOP_N 25 vs 15 at 0% cash: Sh0 1.45 vs 1.24 - the breadth gain survives the accounting change.) At 5-20 cr the stock side is 24-32% invested and earns less than a fixed deposit: the idle capital is the problem to solve.

## 2. Gold-return honesty
Gold's usable sample (2007-10 + 2015-25) returned 16.6%/yr (arithmetic, vol 14.9%); point-to-point over 2007-03..2025-12 including the unobserved 2011-14 it was 13.9%; silver 2022-25 returned 35-38% (vol 24%). Against a 0% baseline almost any gold holding looks good, so every result is shown under gold re-centred to 8%/yr (the planning case, ~half of the sample), 4%, and real. Gates use 8%.

## 3. Pre-registered 7-rule round: nothing passed
H1 all idle in gold, H2 half of idle, H3 trend (SMA200), H4 persistence, H5 trend x bear/panic tilt, H6 gold+silver trend, H7 trend capped at 10%. Gates (8% scenario): Sh0 +0.08, both periods positive, >= 5/6 anchors, MaxDD within 3 pts, positive at 4%, >= +0.05 at double gold cost.
Large weights (20-54% of equity) added +2.0 to +3.8 CAGR but LOWERED Sh0 by 0.07-0.20 and deepened MaxDD (gold at 8% has Sharpe 0.54, below the book's 0.9-1.45; 100% of idle cash in gold is far past the Sharpe-optimal weight). Trend gating (H3/H4/H6) was worse than not timing; bear/panic tilt (H5) worse still; silver (H6) worst. H2 and H7 were positive (+0.03..+0.06) but under +0.08. Gates were not loosened.

## 4. Post-look sizing study (weight is the decision; rule fixed before running)
Untimed gold = min(idle cash, w x equity), 4 book sizes, gold at 8% / 4% / real. Sh0 and Calmar improve up to w ~ 20-25% and fall beyond; 100% of idle is negative:
| w (share of equity) | dSh0 @8% (1 lakh .. 20 cr) | dCAGR @8% | dMaxDD @8% (+ = shallower) | dSh0 @4% |
|---|---|---|---|---|
| 10% | +.04 .. +.07 | +0.55 | +1.0 .. +1.4 | +.015 .. +.022 |
| 15% | +.05 .. +.09 | +0.83 | +1.1 .. +1.8 | +.014 .. +.018 |
| 20% | +.06 .. +.09 | +1.1 | +1.1 .. +1.9 | +.004 .. +.014 |
| **25%** | **+.06 .. +.09** | **+1.3** | **+0.9 .. +2.0** | -.017 .. +.007 |
| 30% | +.06 .. +.08 | +1.6 | +0.5 .. +1.9 | -.043 .. -.004 |
| 40% | +.04 .. +.05 | +2.0 | -0.5 .. +1.6 | -.099 .. -.031 |
| 100% | -.08 .. -.11 | +3.2 .. +3.8 | -2.7 .. -9.7 | -.18 .. -.28 |
Selection rule (largest w with Sh0 >= 0, Calmar >= 0, MaxDD within 3 pts, both periods positive at every book size at 8%, and Sh0 >= -0.03 at 4%): **w* = 25%**. This is a documented rule output, not a pass of the original gates. My own recommendation, made after seeing the table, is 20%: it keeps ~90% of the benefit, stays positive at 4% gold at every size, and is further from the cliff.
At w*: trend-gating = -0.01 Sh0 and worse Calmar vs untimed; bear-tilt (2x in bear/panic, 0.5x otherwise) = -0.04..-0.07; gold+silver 50/50 = -0.02..-0.03. **Neither of your two timing ideas beats a plain capped holding;** weight is the lever.

## 5. Native strategy: `crestline_v2_5.py`
Gold ETF (GOLDBEES) held inside the engine with idle cash, <= GOLD_CAP of equity (default 25%), sold to fund stock entries, 2% dead band, 0.15% one-way cost, closed in the 2011-14 data gap and never bought on a stale price. Idle cash earns 0%.
Tests (11): GOLD_CAP=0 + 6.5% cash == v2.4 bit-exact; native vs post-processing daily correlation 0.9993-0.9995 and CAGR within -0.06..+0.18 pt (pre-registered bars 0.999 / 0.30); frozen gold + zero cost == no-gold book exactly; no gold in the gap; no look-ahead (truncation).
**Data-quality finding caught on the way:** the vendor's ETF OPENING prints are not tradable-quality. GOLDBEES's average overnight (prev close -> open) return is +109%/yr and its intraday (open -> close) return -87%/yr (2020-25: +221% / -189%), with overnight volatility ~2x close-to-close; the same pattern holds for every gold/silver ETF. My first native version filled the ETF at the open and showed +0.4..+0.6 CAGR that did not exist (it sold at inflated opening prints). The sleeve now fills at the PREVIOUS close; a test asserts close-fills are not more flattering than open-fills (18.32% vs 18.87%). The stock pool shows the same overnight/intraday asymmetry on average (+87% / -61% per year); stock opening prices are auction prices and the engine already pays the average +0.35% gap on entries, but whether stop-exit fills at the open are fully achievable is an OPEN caveat for the whole study.

## 6. Headline: v2.5 (gold 25%) vs no gold, 6 anchors, 2006-25, idle cash 0%
| book | case | CAGR | Sh0 | MaxDD | Calmar | dSh0 | anchors + | P_A / P_B |
|---|---|---|---|---|---|---|---|---|
| 1 lakh | no gold | 15.4 | 1.45 | -29.4 | 0.52 | | | 1.74 / 1.21 |
| | gold 25% @ 8% | **16.8** | 1.51 | -27.2 | 0.62 | +.07 | 6/6 | 1.78 / 1.29 |
| | @ 4% | 16.1 | 1.46 | -27.8 | 0.58 | +.01 | 5/6 | |
| | real gold | 18.4 | 1.64 | -25.9 | 0.71 | +.20 | 6/6 | |
| 1 cr | no gold | 10.4 | 1.18 | -23.0 | 0.45 | | | 1.28 / 1.12 |
| | gold 25% @ 8% | **11.6** | 1.25 | -21.4 | 0.54 | +.07 | 6/6 | 1.33 / 1.19 |
| | @ 4% | 11.0 | 1.18 | -22.2 | 0.49 | .00 | 2/6 | |
| | real gold | 13.1 | 1.41 | -19.7 | 0.67 | +.23 | 6/6 | |
| 5 cr | no gold | 7.4 | 1.03 | -17.2 | 0.43 | | | 1.02 / 1.05 |
| | gold 25% @ 8% | **8.6** | 1.10 | -16.1 | 0.53 | +.07 | 6/6 | 1.09 / 1.12 |
| | @ 4% | 8.0 | 1.02 | -17.6 | 0.45 | -.01 | 2/6 | |
| | real gold | 10.1 | 1.30 | -14.0 | 0.72 | +.27 | 6/6 | |
| 20 cr | no gold | 5.0 | 0.89 | -14.3 | 0.35 | | | 0.85 / 0.92 |
| | gold 25% @ 8% | **6.2** | 0.97 | -12.8 | 0.48 | +.08 | 6/6 | 0.93 / 1.00 |
| | @ 4% | 5.6 | 0.87 | -14.3 | 0.39 | -.01 | 1/6 | |
| | real gold | 7.6 | 1.21 | -10.5 | 0.73 | +.33 | 6/6 | |
Cap 20% at 8%: 16.5 / 11.3 / 8.4 / 6.0% CAGR (dSh0 +.06 / +.06 / +.07 / +.09). Double costs (stock 0.6% + gold 0.3%): dSh0 still +0.054 / +0.060 / +0.075 / +0.092 at 8%, 6/6 anchors. 2015-25 alone (gold 8%): 14.0 vs 12.6 (1 lakh), 11.6 vs 10.4 (1 cr), 9.5 vs 8.3 (5 cr), 7.0 vs 5.8 (20 cr) CAGR with Sh0 and MaxDD also better. Six-anchor staggered blend: Calmar 0.51 -> 0.61, 0.44 -> 0.53, 0.45 -> 0.58, 0.39 -> 0.53.

## 7. What this does and does not solve
* Gold adds ~+1.2 to +1.4 CAGR points at a 8%/yr gold return (+2.7 to +3.0 at the real sample return), improves Calmar by ~0.10-0.13 and makes drawdowns ~1-2 pts shallower. At a 4%/yr gold return it is neutral to slightly negative on Sharpe: the sleeve is not free.
* It does NOT fix capacity. A 25% cap leaves most idle capital still idle at big book sizes (at 20 cr, 76% is idle, 25% goes to gold). Higher weights raise CAGR (cap 40%: +2.0, 100% of idle: +3.8 at 8% gold) but lower Sharpe and deepen drawdowns - a risk-appetite choice, not an efficiency gain.
* Realistic expectation after all conservative haircuts: ~16-17% (1 lakh), ~11-12% (1 cr), ~8-9% (5 cr), ~6% (20 cr) CAGR with MaxDD -13..-27%.
* Silver: no evidence of value (0.71 correlation with gold, 3.9 years of data; the split version is worse). Kept out of v2.5.

## 8. Limits
One gold bull market (2015-25), 2011-14 unobserved, January-2026-type -10% gap days; planning scenarios are judgement, not forecasts; taxes on ETF churn not modelled; ETF capacity: 25% of a 20 cr book is ~Rs 5 cr (GOLDBEES trades ~Rs 65 cr/day; split across 2-3 gold ETFs if larger); the open-print issue for stock fills is unresolved; in-sample, no lockbox.

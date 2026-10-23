# CSM Aegis: a new momentum strategy built from the signal files and the breakout lessons

> **Current state of the strategy is in `README.md`** (production preset, results, decay status, how to run). This file is the chronological research log: sections 0-10 quote v1.0 numbers (open fills, no market gate); later sections update to v1.1, v1.2, and the Addendum 7-8 tests. Cash-yield variants in this historical log are not part of the current production result.


Date 2026-10-19. Data: Upstox OHLCV, 5,205 symbols, 2003 to 2026-07-17 (last complete month June 2026). All numbers are faithful-booked (positions drift, exit day charged, 0.3% per leg, idle cash 0%) and unlimited-capacity unless a row says otherwise.
Pre-registration (written before the numbers): `decay_check/PREREG.md`, Addendum 4. Code: this folder (strategy, runner, parity test) and `decay_check/` (research scripts, results CSVs).
Inputs you pointed me to: `MOMENTUM_SIGNALS_EXPLAINED.md`, `MOMENTUM_FAMILY_BAKEOFF_REPORT.md`, `decay_check/LESSONS_BREAKOUTS_FOR_MOMENTUM.md`. No sector-rotation signal was used. `Old_live_strategies/` was not touched.

> **Update 2026-10-21: v1.2.** The module now defaults to v1.2 (R1 + Ulcer selector, 120-day market gate, close fills). Sections 0 to 11 describe v1.0/v1.1 and used next-open fills, which the data audit says are biased; section 12 explains why, re-tests your upgrade list, and gives the out-of-sample view.

> **Update 2026-10-19: v1.1.** Sections 0 to 10 describe v1.0. Section 11 adds the Residual strategy's market trend gate (the only momentum-book overlay that passed the pre-registered tests): max drawdown -57% to -37%, Sharpe 1.30 to 1.41, CAGR 24.4% to 22.9%. The module now defaults to v1.1.

## 0. Short answer

1. **Signal battery.** I measured every non-sector signal in the file (IC, ICIR, hit rate, NW-t, plain t, horizon profile, top-quintile excess, accuracy, monotonicity, incremental information, decay ladder). My numbers reproduce the file's (for example BASE 3m IC 0.078 vs 0.074 there, A1 0.099 vs 0.095, Q5 0.088 vs 0.085).
2. **Decay status depends on the horizon.** At 3 months the ladder calls A1, A3, Q4, Q3 DECAYING. At their own peak horizon (6 to 12 months) **A1, A2, A3, Q5, Q4 and R1 are all HEALTHY**. V2 (volatility contraction) is DECAYED at 6m and 12m. This also suggests my earlier "Elendel/Zenith decaying" calls, which used the 3m IC inside the live pool, deserve a second look (section 8).
3. **No new selector exists in the file.** Under the pre-registered qualification rule only **M3 (low MAX, as an exclusion filter)** qualified as a building block. A1 and A3 are the signals Elendel and Zenith already trade and they fail the rule on 3m decay; Q5, Q4, A2 and BASE add no information beyond those two books; V2 (the coil) is decayed.
4. **Fallback applied, logged, and labelled "not distinct at the signal level".** The healthiest remaining signal is **R1 (residual momentum)**, so the book is R1 + M3 exclusion + the breakout-lessons wrapper. Its top-20 holdings overlap the live books little (0.09 to 0.26 Jaccard), so it is a different portfolio even though the signal family is shared with your Residual strategy.
5. **Result.** Full-history 24.4% CAGR, Sharpe 1.30, max drawdown -57%, beating 100 of 100 random-pick placebos run through the same wrapper (placebo mean 11.3%, Sharpe 0.68). It passed Stage 2, Stage 3 and Stage 4 in both split directions on the Playbook's numeric gates.
6. **Honest weaknesses.** It is a high-volatility small/mid-cap book. It lost **24% since January 2025** (index +4%), and is 25% below its January 2025 peak. Random picks through the same wrapper lost 19.5% over that window, so most of it is the market and the pool, but selection added nothing there (about -4.5 points). Capacity is limited (5% of volume cap at Rs 1 crore: 16%; at Rs 25 crore: 6.6%). Survivorship bias is not removable with this data.
7. **Verdict under the pre-registered accept rule: worth paper-trading, not live-ready.** Stages 6 to 8 (paper, deployment, monitoring) are outstanding.

## 1. The signal battery

Universe and method: top-1000 by 63d dollar volume (prior day), price >= 10, <= 5 circuit days; signal at month-end; forward return month-end to month-end; Newey-West lag h-1; 36-month chunks anchored on 2026-05. "Incr. t" = t-stat of the IC left after removing (by rank regression) everything shared with the Elendel (A3+Q5) and Zenith (A1+Q5) scores together.

| Signal | IC 3m | ICIR | Hit | NW-t | Peak horizon (IC) | Top-quintile excess/3m (NW-t) | Accuracy top quintile | Corr BASE | Incr. t vs Elendel+Zenith info | Decay 3m | Decay 6m | Decay 12m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A1 52w-high proximity | +0.099 | 0.60 | 77% | 6.9 | 12m (+0.128) | +1.6% (3.0) | 56% | 0.57 | 2.7 | DECAYING | HEALTHY | HEALTHY |
| A2 52w range position | +0.085 | 0.62 | 76% | 7.0 | 6m (+0.106) | +1.8% (4.0) | 55% | 0.70 | -1.4 | HEALTHY | HEALTHY | HEALTHY |
| A3 RS line at 52w high | +0.095 | 0.63 | 77% | 7.2 | 6m (+0.118) | +2.1% (4.4) | 55% | 0.76 | 2.8 | DECAYING | HEALTHY | HEALTHY |
| A4 New-high recency | +0.053 | 0.50 | 71% | 5.6 | 6m (+0.062) | +1.7% (4.9) | 54% | 0.60 | -2.4 | WEAK / REGIME | - | - |
| Q5 Trend persistence | +0.088 | 0.77 | 79% | 8.9 | 6m (+0.109) | +1.9% (4.5) | 55% | 0.77 | -2.3 | INCONCLUSIVE | HEALTHY | HEALTHY |
| Q4 Signed trend R2 | +0.077 | 0.69 | 75% | 8.0 | 6m (+0.101) | +1.8% (4.6) | 55% | 0.75 | -2.6 | DECAYING | HEALTHY | HEALTHY |
| Q3 Clenow slope x R2 | +0.061 | 0.52 | 71% | 6.2 | 6m (+0.083) | +1.8% (4.9) | 53% | 0.61 | -1.9 | DECAYING | - | - |
| R1 Residual momentum | +0.069 | 0.52 | 73% | 5.6 | 6m (+0.073) | +1.6% (3.6) | 54% | 0.87 | 1.6 | HEALTHY | HEALTHY | HEALTHY |
| M3 Low MAX (lottery) | +0.038 | 0.35 | 62% | 4.3 | 1m (+0.046) | -0.5% (-1.8) | 52% | -0.01 | 5.5 | WEAK / REGIME | WEAK / REGIME | WEAK / REGIME |
| V2 Volatility contraction | +0.021 | 0.30 | 64% | 4.2 | 3m (+0.021) | +0.2% (1.4) | 50% | 0.00 | 5.0 | INCONCLUSIVE | DECAYED | DECAYED |
| V1 Up/down volume | +0.018 | 0.24 | 64% | 2.8 | 12m (+0.048) | +0.9% (4.3) | 50% | 0.23 | -2.5 | DECAYING | - | - |
| M1 Acceleration | -0.002 | -0.02 | 52% | -0.3 | 12m (+0.025) | +0.6% (2.1) | 50% | -0.13 | -0.6 | INCONCLUSIVE | - | - |
| M2 1m reversal | -0.019 | -0.17 | 40% | -2.4 | 1m (+0.012) | -1.1% (-4.3) | 47% | -0.04 | 2.5 | WEAK / REGIME | - | - |
| Q1 Frog-in-the-pan | -0.008 | -0.07 | 46% | -0.8 | 12m (+0.003) | -0.6% (-1.9) | 48% | -0.23 | 0.2 | WEAK / REGIME | - | - |
| Q2 FIP x momentum | +0.016 | 0.19 | 52% | 2.0 | 6m (+0.016) | +0.4% (1.6) | 50% | 0.21 | -0.0 | WEAK / REGIME | - | - |
| T1 Seasonality | +0.011 | 0.13 | 58% | 1.9 | 1m (+0.034) | -0.0% (-0.1) | 50% | 0.08 | 1.5 | WEAK / REGIME | - | - |
| BASE BASE dual Sharpe 12/6 (reference) | +0.078 | 0.61 | 78% | 6.8 | 6m (+0.087) | +2.0% (4.1) | 54% | 1.00 | 0.4 | HEALTHY | HEALTHY | WEAK / REGIME |
| CTRL CTRL 12-1m return (reference) | +0.066 | 0.47 | 75% | 5.3 | 6m (+0.066) | +1.3% (2.6) | 52% | 0.91 | 0.9 | HEALTHY | - | - |

Reading it:
- **Accuracy** (share of top-quintile names beating the cross-sectional median over 3 months) is 53% to 56% for every working signal. Small per-name edge, spread over many names.
- **Long-side vs IC.** M3, V2 and V1 have decent IC but their top quintile does not beat the universe (M3 -0.5%, V2 +0.2%): their IC comes from identifying losers, so they are filters, not selectors, as the file says.
- **Horizon.** Anchors (A1, A2, A3), trend quality (Q5, Q4) and BASE peak at 6 to 12 months. R1 peaks at 6m. M3 is a 1m signal.
- **Incremental information** (last column of the first table): only M3 (5.5), V2 (5.0) and the "1m reversal" M2 (2.5, but its own IC is negative) add information beyond Elendel+Zenith with t above 2. R1 adds 1.6.

![signal decay](charts/fig1_signal_decay.png)

| Signal | 2008-11 | 2011-14 | 2014-17 | 2017-20 | 2020-23 | 2023-26 |
|---|---|---|---|---|---|---|
| A1 | +0.106 (1.9) | +0.113 (2.7) | +0.088 (3.1) | +0.144 (3.5) | +0.059 (2.4) | +0.059 (1.8) |
| A2 | +0.086 (2.0) | +0.092 (3.0) | +0.086 (3.1) | +0.103 (3.3) | +0.056 (2.4) | +0.051 (2.0) |
| A3 | +0.100 (2.0) | +0.112 (2.9) | +0.090 (3.5) | +0.114 (3.1) | +0.059 (2.5) | +0.053 (1.8) |
| Q5 | +0.097 (2.7) | +0.094 (3.5) | +0.076 (3.3) | +0.106 (4.8) | +0.052 (2.6) | +0.051 (2.5) |
| R1 | +0.069 (1.6) | +0.087 (2.2) | +0.074 (2.7) | +0.077 (2.9) | +0.016 (0.5) | +0.067 (4.2) |
| BASE | +0.075 (1.8) | +0.088 (2.7) | +0.075 (3.2) | +0.088 (3.2) | +0.047 (1.7) | +0.057 (2.7) |
| M3 | +0.066 (3.4) | +0.045 (1.8) | +0.028 (1.3) | +0.098 (4.6) | +0.012 (0.7) | +0.038 (1.4) |
| V2 | +0.037 (3.6) | +0.020 (1.5) | +0.029 (2.7) | +0.025 (1.8) | +0.023 (1.7) | +0.003 (0.2) |

![horizon profile](charts/fig2_horizon.png)

Decay rules as in the pre-registration: HEALTHY / WEAK / DECAYING / DECAYED from the latest-chunk NW-t, the full-history trend, the percentile of the latest window within the signal's own history, and a market-regime control. The 3m ladder was the pre-registered primary; the 6m and 12m columns are supplementary and were added to answer "horizon period".

## 2. Qualification rule and what it selected

Rule (fixed before the run): a building block needs (Q1) full-history 3m NW-t of at least 3, (Q2) not DECAYING/DECAYED and latest-chunk NW-t of at least 1, (Q3) incremental t versus Elendel+Zenith of at least 2 with positive incremental IC in the latest 6 years. Selector if the top-quintile excess NW-t is at least 2 and the quintiles are monotonic, otherwise filter.

| Signal | Q1 | Q2 | Q3 | Outcome |
|---|---|---|---|---|
| A1, A3 | pass | DECAYING at 3m | pass | rejected (decay) |
| A2, A4, Q5, Q4, Q3 | pass | mixed | fail (no new information) | rejected |
| BASE, CTRL | pass | pass | fail | rejected |
| R1 | pass | pass | fail (1.6 vs 2.0) | not a qualifying block |
| **M3** | pass | pass | **pass** | **FILTER (exclude worst 20% by recent spike)** |
| V2 | pass | fail (latest-chunk NW-t 0.2) | pass | rejected: decayed. Coil component C2 dropped. |
| the rest | fail | | | rejected |

Sensitivity (not used, because the rule was pre-registered at 3m): evaluated at 6m, A1 and A3 would pass Q2 as well, and they carry incremental information versus the Elendel+Zenith pair (t 2.7 and 2.8). They would be selectors, but they are exactly what Zenith (A1) and Elendel (A3) already trade, so a book built on them would be a re-skin of those two.

No selector qualified under the pre-registered rule, so the fallback applied. The fallback sentence was silent on "best", so I clarified it before any strategy run (post-look change #1 in `PREREG.md`): highest latest-chunk IC NW-t among signals that pass Q1 and Q2. **R1 wins (4.2)**, ahead of BASE (2.7), CTRL (2.6) and Q5 (2.5). R1 is labelled NOT DISTINCT at the signal level (rank correlation 0.87 with BASE; the Residual strategy uses a composite of the same family). The distinctness check on holdings:

| Live book | Top-20 overlap, all months | Latest 3y |
|---|---|---|
| absolute | 0.19 | 0.17 |
| batch | 0.26 | 0.24 |
| elendel | 0.12 | 0.09 |
| quad | 0.09 | 0.14 |
| residual | 0.20 | 0.19 |
| zenith | 0.16 | 0.15 |

Overlap is at or below the pre-registered 0.35 limit for every live book.

## 3. The strategy

| Block | Rule | Source |
|---|---|---|
| Pool | top-1000 by 63d dollar volume (prior day), price >= 20, <= 5 circuit-locked days in 63, close above SMA-200 | momentum books + breakout trend gate |
| Selector | R1 residual momentum, 12m window skipping the last month, vol-scaled, beta from 252d lagged one day | signals file, family R |
| Exclusion | drop the worst 20% of the pool by M3 (biggest one-month spike) | signals file, M3 |
| Selection | month-end close; top 20 by R1; held until rank > 40 or it leaves the pool | |
| Entry | next trading day open; skip if it gaps up more than 3%; skip names more than 25% above SMA-50 (C1); no new entries when benchmark 63d vol is above its expanding 85th percentile (C3) | lessons T2, T3 |
| Exits | all close-based, filled at the next open: -15% from entry, -20% from peak close, time stop (45+ days and below -5%) (C4), rank exit | lessons T4, breakout chandelier philosophy |
| Sizing | weight = 1% / 15% = 6.7%, clamped to 3% to 8%, gross at most 100% (C5) | lessons T5 |
| Costs | 0.3% per leg; idle cash 0% (6.5% shown separately) | |

Nothing was tuned: every parameter is a textbook or lessons-file value fixed in the pre-registration.

## 4. Validation

### 4.1 Stage 2: does the signal have edge at each filter rung (R1)

| Rung | IC 3m | NW-t | ICIR | Names/month | Quintile means (%/3m) | Monotonic pairs | NW-t 2005-12 | NW-t 2013-26 | Top-2-year IC share |
|---|---|---|---|---|---|---|---|---|---|
| L0 raw | +0.064 | 5.9 | 0.54 | 1496 | [np.float64(3.42), np.float64(4.46), np.float64(5.18), np.float64(6.52), np.float64(28.54)] | 100% | 3.9 | 4.5 | 18% |
| L1 price>=10 | +0.065 | 5.8 | 0.53 | 1306 | [np.float64(3.05), np.float64(4.06), np.float64(4.83), np.float64(5.85), np.float64(6.72)] | 100% | 4.0 | 4.3 | 18% |
| L2 +liquidity top1000 | +0.067 | 5.6 | 0.52 | 789 | [np.float64(3.07), np.float64(3.63), np.float64(4.66), np.float64(5.61), np.float64(6.45)] | 100% | 4.0 | 4.1 | 17% |
| L3 tradeable (px>=20, circuit) | +0.070 | 5.7 | 0.53 | 721 | [np.float64(3.1), np.float64(3.56), np.float64(4.62), np.float64(5.59), np.float64(6.25)] | 100% | 4.1 | 4.2 | 18% |
| L4 strategy pool (SMA200 + M3 excl.) | +0.044 | 3.6 | 0.34 | 335 | [np.float64(4.21), np.float64(4.7), np.float64(5.76), np.float64(6.18), np.float64(6.73)] | 100% | 2.2 | 2.8 | 19% |

Playbook gates: L0 and L3 NW-t at least 2.0 (pass: 5.9 and 5.7); monotonic pairs at least 80% (100% on the time-averaged quintile means); months with fewer than 8 names at most 15% (under 2%); top-2-year share of signed IC at most 50% (about 18%); OOS NW-t at least 1.5 in both periods (pass at every rung). The strategy pool (L4: SMA-200 gate plus M3 exclusion) halves the IC (0.044) but it stays significant (NW-t 3.6). The small-cap versus large-cap IC split is equal (0.065 vs 0.066), so the edge is not concentrated in the least liquid half.

### 4.2 Does the selector matter? Placebo and wrapper bake-off

| Run | CAGR | Sharpe | MaxDD | Calmar |
|---|---|---|---|---|
| wrapper[R1] | 24.4% | 1.30 | -57% | 0.43 |
| wrapper[ELEN] | 21.9% | 1.21 | -52% | 0.42 |
| wrapper[ZEN] | 19.3% | 1.15 | -52% | 0.37 |
| wrapper[BASE] | 24.4% | 1.24 | -56% | 0.43 |
| placebo mean (100 random draws) | 11.3% | 0.68 | -56% | 0.20 |
| placebo 95th pct | 14.5% | 0.84 | -52% | 0.28 |

- **R1 beats every one of 100 random-pick draws** through the identical wrapper, on Sharpe and on CAGR. The wrapper alone (random picks) earns about market return, so the edge is the selection.
- The same wrapper on the existing selectors (Elendel's A3+Q5, Zenith's A1+Q5, BASE) earns 19% to 24% faithful CAGR against 7% to 10% for the live books' faithful numbers over the same window. That gap is **not** a clean test of wrapper versus chassis: pools, top-N, vol targeting, crash guard and stop logic all differ. It is, however, a strong reason to look at the live books' execution layer (section 8).

| Chunk | Aegis CAGR | Placebo mean | Placebo 95th | Placebo draws beaten |
|---|---|---|---|---|
| 2008-11 | 31.4% | 10.8% | 16.9% | 100% |
| 2011-14 | 34.4% | 14.3% | 21.9% | 100% |
| 2014-17 | 27.6% | 17.7% | 28.3% | 93% |
| 2017-20 | -2.2% | -12.2% | -6.2% | 99% |
| 2020-23 | 50.9% | 30.5% | 41.6% | 100% |
| 2023-26 | 16.1% | 3.9% | 12.1% | 99% |
| All | 24.1% | 9.1% | 12.6% | 100% |

Aegis beats 99% to 100% of the placebo draws in five of the six 3-year chunks and 93% in 2014 to 2017.

### 4.3 Stage 3: robustness and ablation (all five Playbook metrics per cell)

| Test | CAGR | Sharpe | Calmar | MaxDD | Avg DD depth | Return stability (std 12m) |
|---|---|---|---|---|---|---|
| BASELINE | 24.4% | 1.30 | 0.43 | -57% | -8.2% | 0.39 |
| band (1, 500) | 19.9% | 1.12 | 0.35 | -58% | -7.7% | 0.35 |
| band (1, 1000) | 24.4% | 1.30 | 0.43 | -57% | -8.2% | 0.39 |
| band (250, 1000) | 27.0% | 1.43 | 0.50 | -54% | -8.7% | 0.44 |
| band (500, 1500) | 26.2% | 1.39 | 0.58 | -45% | -8.9% | 0.45 |
| param top_n=16 | 24.2% | 1.29 | 0.48 | -51% | -7.8% | 0.41 |
| param top_n=24 | 22.8% | 1.24 | 0.40 | -58% | -8.5% | 0.39 |
| param stop=0.12 | 24.9% | 1.34 | 0.45 | -55% | -8.0% | 0.39 |
| param stop=0.18 | 24.4% | 1.30 | 0.43 | -56% | -8.0% | 0.39 |
| param trail=0.16 | 22.5% | 1.25 | 0.41 | -55% | -8.4% | 0.39 |
| param trail=0.24 | 24.0% | 1.27 | 0.40 | -59% | -8.3% | 0.40 |
| param hold_rank=32 | 22.7% | 1.22 | 0.40 | -56% | -8.1% | 0.39 |
| param hold_rank=48 | 23.2% | 1.26 | 0.40 | -57% | -8.1% | 0.39 |
| without: no extension filter (C1) | 24.0% | 1.29 | 0.42 | -57% | -8.0% | 0.38 |
| without: no vol-state gate (C3) | 25.6% | 1.34 | 0.45 | -57% | -8.1% | 0.39 |
| without: no time stop (C4) | 24.8% | 1.30 | 0.42 | -59% | -8.1% | 0.40 |
| without: equal sizing (C5) | 23.4% | 1.30 | 0.42 | -56% | -7.9% | 0.37 |
| without: no trend gate (C6) | 22.1% | 1.18 | 0.34 | -65% | -8.6% | 0.41 |
| without: no M3 exclusion | 23.6% | 1.21 | 0.44 | -53% | -8.0% | 0.40 |
| without: no hard/trail stops | 15.6% | 1.26 | 0.33 | -48% | -6.9% | 0.23 |
| without: no stops, no time stop | 15.0% | 1.11 | 0.25 | -59% | -7.4% | 0.24 |

Playbook gates:
- **Universe bands** (1-500, 1-1000, 250-1000, 500-1500): Sharpe range 0.31 (limit 0.35, pass), CAGR range 7.1 points (limit 8, pass), Calmar range 0.24 (limit 0.50, pass), max drawdown range 12.7 points (caution band 10 to 18), every band Sharpe above 0 (pass).
- **Parameter swings** at +-20% (top_n, stop, trail, hold rank): largest Sharpe swing 0.10 (limit 0.4, pass).
- **What each lessons component earned** (baseline minus ablated): hard/trail stops +8.8 points CAGR (Sharpe +0.05, but max drawdown -57% vs -48% without); trend gate +2.3 points (max drawdown -65% without it); risk-based sizing +1.0; M3 exclusion +0.8; extension filter C1 +0.4 (negligible); time stop C4 -0.4 (negligible); **vol-state gate C3 -1.2 points and Sharpe -0.04, it does not earn its place** (consistent with VCP's regime filter in the earlier ablation). Removing C3 would clear all five Playbook metrics, so it is the natural v1.1 simplification; I kept the frozen v1.0 as pre-registered and did not use a post-look change on it.

### 4.4 Stage 4: bidirectional split

| Split | IS Sharpe | OOS Sharpe | OOS/IS Sharpe | OOS/IS Calmar | OOS/IS CAGR | MaxDD OOS vs IS |
|---|---|---|---|---|---|---|
| Split A | 1.32 | 1.29 | 98% | 133% | 94% | 0.71x |
| Split B | 1.29 | 1.32 | 102% | 75% | 107% | 1.42x |

All ratios are inside the acceptable bands in both directions (the max-drawdown ratio in Split B is 1.42x against a 1.5x limit, close to the edge). OOS Sharpe is positive in both. Because nothing was tuned, "IS" is descriptive; the split mostly confirms the result is not a one-era artifact. The OOS window in Split A (2013 onward) contains the 2018, 2020 and 2022 stress periods.

### 4.5 Stage 5: exits

| Exit reason | Trades | Share | Avg trade | Win rate | Post-exit vs market 20d / 60d | Verdict |
|---|---|---|---|---|---|---|
| RANK_EXIT | 991 | 47% | +19.9% | 82% | -0.4% / -1.1% | neutral |
| STOP_ENTRY | 405 | 19% | -18.4% | 0% | +0.1% / +0.5% | neutral |
| STOP_TRAIL | 296 | 14% | +8.8% | 50% | -0.8% / -5.0% | working |
| TIME_STOP | 383 | 18% | -7.1% | 0% | -0.5% / -1.7% | working |

Trades per bucket are all above 30; END_OF_PERIOD is 0.8% of exits (limit 5%). Trail stops are "working" (the stock keeps lagging after the exit, post-exit -2.9% vs market), time stops marginally so, entry stops and rank exits are neutral. Entry stops average -18.4%, not -15%, because they exit at the next open after a close-based trigger (gaps).

### 4.6 Stress (all faithful)

| Stress | CAGR | Sharpe | MaxDD |
|---|---|---|---|
| cost 0.6%/leg | 20.8% | 1.14 | -59% |
| cost 1.0%/leg | 16.2% | 0.92 | -61% |
| resting stop fills | 16.3% | 0.95 | -53% |
| cash earns 6.5% | 25.3% | 1.35 | -57% |
| ADV cap 5%, start Rs1cr | 16.4% | 1.07 | -49% |
| ADV cap 5%, start Rs5cr | 11.7% | 0.98 | -36% |
| ADV cap 5%, start Rs25cr | 6.6% | 0.77 | -24% |
| entry gap cancel off | 24.5% | 1.31 | -54% |

- Costs: at 1% per leg CAGR falls to 16% and Sharpe to 0.92; it survives.
- **Resting-stop fills lower the result** (16.3%): intraday wicks stop out names that recover, so the close-based, next-open rule used here is both executable and better.
- **Capacity is the main limit.** With each position capped at 5% of 63-day rupee volume, 16.4% from Rs 1 crore, 11.7% from Rs 5 crore, 6.6% from Rs 25 crore (the account compounds, so the cap binds more later).
- One or two extra days of execution delay (ad hoc check, not in the table) cost 0.5 and 1.8 points of CAGR.
- Trade concentration is moderate: the top 10 trades are 15% of summed contribution, the top 50 are 48%. Seven trades had a single-day move above 25% while held (possible data glitches); together they were -1.6% of total contribution, so they do not flatter the result.

### 4.7 Performance by 3-year chunk (CAGR, Sharpe in brackets)

| Strategy | 2008-11 | 2011-14 | 2014-17 | 2017-20 | 2020-23 | 2023-26 | All |
|---|---|---|---|---|---|---|---|
| AEGIS(R1) | 31.4% (1.69) | 34.4% (2.21) | 27.6% (1.33) | -2.2% (-0.05) | 50.9% (2.23) | 16.1% (0.97) | 24.1% (1.33) |
| wrapper[ELEN] | 25.0% (1.38) | 38.2% (2.55) | 21.9% (1.16) | -4.8% (-0.26) | 34.1% (1.62) | 13.0% (0.76) | 19.4% (1.13) |
| wrapper[ZEN] | 20.3% (1.26) | 30.8% (2.21) | 16.5% (1.00) | -7.9% (-0.54) | 33.9% (1.67) | 17.5% (1.07) | 16.9% (1.08) |
| wrapper[BASE] | 30.6% (1.56) | 41.9% (2.62) | 20.0% (0.96) | 0.2% (0.10) | 39.7% (1.79) | 16.0% (0.87) | 22.8% (1.21) |
| live Elendel | 0.0% (0.06) | 16.0% (1.31) | 15.5% (0.97) | -7.5% (-0.55) | 38.7% (2.08) | -0.3% (0.07) | 9.0% (0.66) |
| live Zenith | 13.5% (1.21) | 11.7% (1.27) | 6.5% (0.51) | 0.7% (0.12) | 25.4% (1.56) | 5.4% (0.42) | 10.0% (0.82) |
| live Quad | 9.2% (0.74) | 19.0% (1.55) | 23.9% (1.35) | -9.9% (-0.81) | 12.5% (0.83) | -4.8% (-0.26) | 7.3% (0.57) |
| Nifty 500 (price) | 12.4% | 10.9% | 10.8% | 0.6% | 25.0% | 12.1% | 10.4% |

![chunks](charts/fig4_chunks.png)

![equity](charts/fig3_equity.png)

Yearly returns:

| Year | Aegis | Nifty 500 (price) |
|---|---|---|
| 2005 | +74.6% | +34.9% |
| 2006 | +19.1% | +30.7% |
| 2007 | +88.7% | +62.5% |
| 2008 | -55.8% | -57.1% |
| 2009 | +68.4% | +88.6% |
| 2010 | +47.6% | +14.1% |
| 2011 | -15.9% | -27.2% |
| 2012 | +60.7% | +31.4% |
| 2013 | +23.2% | +3.4% |
| 2014 | +103.7% | +37.8% |
| 2015 | +17.9% | -0.7% |
| 2016 | +4.2% | +3.8% |
| 2017 | +64.7% | +35.9% |
| 2018 | -15.2% | -3.4% |
| 2019 | -8.0% | +7.7% |
| 2020 | +32.9% | +16.7% |
| 2021 | +108.8% | +30.2% |
| 2022 | -12.9% | +3.0% |
| 2023 | +78.8% | +25.8% |
| 2024 | +31.1% | +15.2% |
| 2025 | -16.5% | +6.7% |
| 2026 | -8.9% | -2.2% |

## 5. Decay status of the strategy itself

- **Rolling 36-month CAGR:** latest 14.2%, at the 22nd percentile of its own history (minimum -4.3%). Rolling Sharpe latest 0.87 (minimum -0.13). Inside its own normal range, not yet unusual.
- **Latest chunk:** +16.1% against the index's +12.1%, positive, but the weakest positive chunk and much lower than 2011 to 2014 (34%) and 2020 to 2023 (51%).
- **Since January 2025: -24.0% (index +4.3%)**, currently 25% below the January 2025 peak. Random picks through the same wrapper lost 19.5% (5th to 95th percentile -29% to -6%), so the pool (small and mid caps with a trend gate) fell with the market. Selection added about -4.5 points in that window.
- **R1 signal in the same period:** 3m excess over the universe +0.3% in 2025 and -2.8% in 2026 to date; 1m excess positive (+1.0% in 2025, +2.0% in 2026). So the signal's short-horizon edge is intact; the 3m edge went flat.
- Not biased by recent years: the verdict above uses all chunks, the rolling percentile and the placebo; the last 18 months are reported separately as a caution, not used to reject.

## 6. What the breakout lessons did here

| Lesson | Result in this strategy |
|---|---|
| T1 price-location / residual selector | Strong: R1 is +13 CAGR points over placebo; healthy at every horizon |
| T2 extension filter | Negligible (+0.4 points) |
| T3 market-vol gate | Did not help (-1.2 points); drop in v1.1 |
| T4 time stop | Negligible (-0.4 points); marginally "working" on exit diagnostics |
| T5 risk-based sizing | Small (+1.0 point) |
| Close-based hard and trailing stops | Largest wrapper contributor (+8.8 points) but raises max drawdown |
| Trend gate | +2.3 points and avoids a -65% drawdown |
| M3 exclusion | +0.8 points |
| Capacity realism (breakout lesson) | Applied in stress; it is the binding constraint |
| Faithful booking (lesson T6) | Used throughout; independent replay from the trade log matches the engine (24.35% vs 24.37%) |

![ablation](charts/fig5_ablation.png)

## 7. Caveats

- **Survivorship.** The data has no delisting calendar; absolute levels are upper bounds. The placebo and chunk comparisons share the same bias.
- **High risk.** Max drawdown -57% (2008), volatility 18%, concentrated in small and mid caps. Position sizes and the 100% gross cap mean there is no leverage, but the book is not Nifty-like.
- **Capacity** (section 4.6). Real slippage in rank 500 to 1000 names is not modelled beyond 0.3% per leg.
- **Not distinct at the signal level.** It shares a signal family with the Residual strategy; it is different as a portfolio (holdings overlap 0.2) and as an execution design.
- **In-sample.** Every number is historical; the only true out-of-sample is forward paper trading (Stage 6).
- **The wrapper values (stops 15%/20%, 45 days, 1% risk) were not tuned** but they are not independent of the breakout books, whose results I had seen.
- **Stages 6 to 8 are not run:** paper/shadow parity, deployment sign-off, post-live monitoring and kill rules.

## 8. A correction to earlier decay calls, and a lead worth following

The decay ladder was run at 3 months. At the anchors' own 6m and 12m horizons on the full tradeable universe, A1, A2, A3, Q5 and Q4 are healthy (percentile of the latest window within their own history 35% to 72%). The earlier "Elendel DECAYING / Zenith signal healthy" calls were made on 3m IC inside the live pool (price above SMA-200, falling-knife gate, universe band), where the IC is much lower (the BASE factor, as used by Batch and Quad, has 3m IC 0.017 in the live pool and 0.057 on the full universe in the latest chunk). The same wrapper on those selectors earned 13% to 17.5% in the latest 3 years while the live books earned -0.3% and 5.4%. That points at the **live books' execution layer and pool gates**, not only at signal decay. I have not decomposed it; it is the highest-value follow-up (run the live books with this wrapper's exits and sizing one component at a time).

## 9. How to run it

```bash
cd csm_aegis
python3 test_parity.py                 # module == research engine bit-for-bit; live exit rules == backtest exits; signals match
python3 csm_aegis_backtest.py                   # faithful backtest, yearly table, exit breakdown, latest picks -> output/
python3 make_charts.py && python3 build_report.py
```
Monthly paper routine (Stage 6 design): on the last trading day of the month run `CSMAegis.latest_picks()`; place next-open entries for ranks up to 20 not blocked by the extension filter or vol gate (weight 6.7%, never above 100% gross); every day after the close call `get_exit_signals(holdings, today)` and sell the names it returns at the next open; at month-end also run it for rank exits.

Files: `csm_aegis_strategy.py` (strategy), `csm_aegis_backtest.py` (booking and runner), `test_parity.py`, `output/` (trade log, daily returns, exit breakdown, yearly returns, latest picks), `charts/`. Research: `decay_check/signals_lib.py`, `signal_battery.py`, `strategy_engine.py`, `aegis_validation.py`, `aegis_checks.py`, `results/battery_*.csv`, `results/aegis_*.csv`.

## 10. Next steps I would take
1. Forward paper-trade v1.0 for at least two quarters (Stage 6), with weight parity and slippage logging.
2. v1.1 candidate: drop the vol-state gate (C3) and re-run Stages 3 and 4.
3. Test the live books with this wrapper's exits and sizing one component at a time (section 8).
4. Add a capacity-aware sizing rule (5% of volume cap) as a first-class parameter rather than a stress test.

---
## 11. Update v1.1: adding logic from the momentum books (2026-10-19)

You asked to add things from the momentum strategies in `Old_live_strategies` that can improve results. I read the overlay code in the batch, zenith, quad, residual and absolute books, listed every distinct piece, fixed the list and the adoption rule in `PREREG.md` (Addendum 5) before running anything, ported each one with the books' own default parameters (no tuning), and tested them add-one on v1.0 with forward selection.

**Outcome: one piece was adopted, the Residual strategy's market trend gate.** At each month-end, if the equal-weight market index is at or below its 150-day average, exit everything at the next open and take no entries. Nothing else passed on top of it.

![v1.1 vs v1.0](charts/fig6_v11.png)

### 11.1 What v1.1 changes (faithful, 0.3% per leg, unlimited capacity)

| Run | CAGR | Sharpe | Calmar | MaxDD | Avg DD depth | Stability | Turnover/yr |
|---|---|---|---|---|---|---|---|
| v1.0 | 24.4% | 1.30 | 0.43 | -57% | -8.2% | 0.39 | 9.8x |
| v1.1 (adopted) | 22.9% | 1.41 | 0.62 | -37% | -7.6% | 0.37 | 7.8x |
| K4 gate window 120d (sensitivity) | 26.2% | 1.62 | 0.81 | -32% | -6.8% | 0.35 | 7.7x |
| K4 gate window 180d (sensitivity) | 22.3% | 1.38 | 0.60 | -37% | -7.7% | 0.37 | 7.8x |
| v1.1 + K1 crash guard (near miss) | 24.5% | 1.51 | 0.66 | -37% | -7.3% | 0.36 | 7.7x |
| v1.1 + K2 vol target (near miss) | 20.0% | 1.47 | 0.71 | -28% | -7.1% | 0.30 | 9.9x |
| v1.1 + 6.5% cash yield (separate) | 25.6% | 1.55 | 0.73 | -35% | -7.1% | 0.36 | 7.8x |


- **Max drawdown -57% to -37%, Calmar 0.43 to 0.62, Sharpe 1.30 to 1.41; CAGR 24.4% to 22.9%.** It trades a little return for a lot of drawdown.
- **2008: -29% instead of -56%** (the gate was out of the market for much of the crash). Since January 2025: **-14.9% instead of -24.0%**, and 16% below peak instead of 25%. Still negative in 2025 and 2026 to date (-10.1% and -5.3%).
- The gate is not a knife-edge: a 120-day window gives Sharpe 1.63 and a 180-day window 1.38, so v1.1 is not sitting on a lucky parameter. I did not switch to 120 days because that would be tuning after the fact.
- Gate exits: 154 times, average trade +5.3%, win rate 52%; average gross exposure 0.91. A gated month means the book sits in cash with 0% yield, unless you park it in a liquid fund (+1.2 points of CAGR in the "v1.1 + 6.5% cash" row).

### 11.2 Everything tested (add-one on v1.0, round 1)

![overlay results](charts/fig7_overlays.png)

| Candidate | CAGR | Sharpe | Calmar | MaxDD | Passed? | Why not (pre-registered criteria) |
|---|---|---|---|---|---|---|
| v1.0 baseline | 24.4% | 1.30 | 0.43 | -57% | - | - |
| Crash Guard (batch/zenith/quad) | 26.1% | 1.38 | 0.50 | -52% | no | d: latest 2 chunks Sharpe lower |
| Vol targeting 15% (residual/quad) | 21.1% | 1.35 | 0.50 | -42% | no | b: turnover +25% |
| Regime leverage 0.6 bear / 0.5 panic (zenith) | 26.5% | 1.45 | 0.53 | -50% | **YES** | - |
| Market trend gate, EW index vs SMA-150 (residual) | 22.9% | 1.41 | 0.62 | -37% | **YES** | - |
| Corr guard (batch) | 24.4% | 1.30 | 0.43 | -57% | no | a: gain too small |
| Loss-scaled re-entry cooldown (zenith/quad) | 24.9% | 1.33 | 0.44 | -56% | no | a: gain too small |
| Absolute-momentum gate (batch family) | 22.0% | 1.22 | 0.38 | -58% | no | a: gain too small; c: a half regresses >5%; d: latest 2 chunks Sharpe lower; e: worse at 0.6% cost |
| Falling-knife gate (batch family) | 24.3% | 1.30 | 0.44 | -55% | no | a: gain too small; d: latest 2 chunks Sharpe lower; e: worse at 0.6% cost |
| Inverse-vol sizing (batch/residual) | 22.7% | 1.35 | 0.42 | -55% | no | a: gain too small |
| ATR chandelier (elendel/zenith) | 21.6% | 1.22 | 0.40 | -54% | no | a: gain too small; c: a half regresses >5%; d: latest 2 chunks Sharpe lower; e: worse at 0.6% cost |
| Min-hold 5 days (batch family) | 24.4% | 1.29 | 0.43 | -56% | no | a: gain too small; d: latest 2 chunks Sharpe lower; e: worse at 0.6% cost |
| Quarterly entries (quad V5) | 11.3% | 0.88 | 0.28 | -40% | no | a: gain too small; b: Sharpe/Calmar regress >15%; c: a half regresses >5%; d: latest 2 chunks Sharpe lower; e: worse at 0.6% cost |


Criteria (all pre-registered): Calmar +10% or Sharpe +5% relative; no regression above 15% in Sharpe/Calmar, 20% in stability or average drawdown depth, 25% in turnover; each half (2005-12, 2013-26) not more than 5% below on Sharpe; latest two chunks' Sharpe not lower; Sharpe at 0.6% cost not lower.
- **Passed in round 1:** regime leverage (K3) and the market trend gate (K4). K4 scored higher (mean of Sharpe and Calmar gains) and was adopted. In round 2, with K4 in place, nothing passed (K3 no longer adds enough).
- **Near misses (not adopted, because each fails one criterion):** Crash Guard on top of v1.1 gives Sharpe 1.51, Calmar 0.66, drawdown -37% but its latest-two-chunk Sharpe is lower than v1.1's. Vol targeting 15% on top of v1.1 gives Sharpe 1.47, Calmar 0.71, drawdown -28% but turnover is up 26% (limit 25%). These two are the natural v1.2 candidates; they would need a fresh pre-registration or a paper-trading result to adopt honestly.
- **Failed clearly:** absolute-momentum gate, falling-knife gate, ATR chandelier, min-hold and quarterly entries all lower the latest-period Sharpe or the cost-stressed result; quarterly entries halve the CAGR (11.3%). Corr guard, loss-scaled cooldown and inverse-vol sizing change little. This matches the Quad blueprint's own graveyard notes for several of these.
- Take-profit / crystallisation was not re-tested: the Quad blueprint measured it at -14 points of CAGR.

### 11.3 Re-validation of v1.1

**Stage 3 (bands, parameters).** v1.1's universe-band sweep is wider than v1.0's: Sharpe range 0.38 across the four bands (limit 0.35, so the caution band), CAGR range 8.2 points (caution), Calmar range 0.26 and max-drawdown range 6.5 points (both fine). The 1 to 500 band is the weak one (Sharpe 1.19). Parameter swings at +-20% stay small (largest Sharpe swing 0.08).

| Run | CAGR | Sharpe | Calmar | MaxDD | Avg DD depth | Stability | Turnover/yr |
|---|---|---|---|---|---|---|---|
| band (1, 500) | 18.4% | 1.19 | 0.53 | -35% | -6.9% | 0.31 | 7.5x |
| band (1, 1000) | 22.9% | 1.41 | 0.62 | -37% | -7.6% | 0.37 | 7.8x |
| band (250, 1000) | 26.2% | 1.57 | 0.64 | -41% | -7.7% | 0.41 | 8.0x |
| band (500, 1500) | 26.6% | 1.56 | 0.79 | -34% | -7.7% | 0.46 | 7.3x |
| param top_n=16 | 22.8% | 1.41 | 0.60 | -38% | -7.0% | 0.38 | 7.4x |
| param top_n=24 | 22.0% | 1.36 | 0.59 | -37% | -7.9% | 0.37 | 8.1x |
| param stop=0.12 | 23.0% | 1.43 | 0.61 | -38% | -7.5% | 0.37 | 7.9x |
| param stop=0.18 | 22.7% | 1.40 | 0.62 | -37% | -7.4% | 0.36 | 7.6x |
| param trail=0.16 | 21.0% | 1.34 | 0.58 | -36% | -7.6% | 0.37 | 8.2x |
| param trail=0.24 | 22.9% | 1.38 | 0.66 | -35% | -7.6% | 0.38 | 7.6x |
| param hold_rank=32 | 22.4% | 1.37 | 0.61 | -36% | -7.2% | 0.36 | 8.4x |
| param hold_rank=48 | 22.2% | 1.38 | 0.61 | -37% | -7.3% | 0.36 | 7.4x |


**Ablation of the rest of the wrapper, now with the gate in place:**

| Run | CAGR | Sharpe | Calmar | MaxDD | Avg DD depth | Stability | Turnover/yr |
|---|---|---|---|---|---|---|---|
| ablation without K4 (=v1.0) | 24.4% | 1.30 | 0.43 | -57% | -8.2% | 0.39 | 9.8x |
| ablation no extension C1 | 23.2% | 1.42 | 0.61 | -38% | -7.3% | 0.36 | 7.7x |
| ablation no vol-state gate C3 | 24.0% | 1.45 | 0.68 | -35% | -7.5% | 0.37 | 7.9x |
| ablation no time stop C4 | 23.4% | 1.42 | 0.63 | -37% | -7.5% | 0.37 | 7.4x |
| ablation equal sizing C5 | 21.9% | 1.42 | 0.61 | -36% | -7.5% | 0.35 | 7.5x |
| ablation no trend gate C6 | 21.9% | 1.36 | 0.50 | -44% | -7.9% | 0.38 | 8.0x |
| ablation no M3 | 21.6% | 1.28 | 0.55 | -40% | -7.4% | 0.36 | 6.4x |
| ablation no hard/trail stops | 14.7% | 1.39 | 0.59 | -25% | -5.8% | 0.21 | 4.3x |


- The hard and trailing stops no longer improve Sharpe (1.39 without vs 1.41 with) and they cost drawdown (-25% without vs -37% with); what they still buy is about 8 points of CAGR. With the market gate present, they are a return-versus-risk choice, not a clear win.
- The vol-state gate C3 again does not earn its place (Sharpe 1.455 and Calmar 0.69 without it); it is the obvious v1.2 simplification.

**Stage 4, both split directions** (all inside the acceptable bands):

| Split | IS Sharpe | OOS Sharpe | OOS/IS Sharpe | OOS/IS Calmar | OOS/IS CAGR | MaxDD OOS vs IS |
|---|---|---|---|---|---|---|
| Split A | 1.43 | 1.39 | 97% | 90% | 94% | 1.05x |
| Split B | 1.39 | 1.43 | 103% | 111% | 106% | 0.96x |


**Placebo with the same gate:** random picks earn 13.5% / Sharpe 0.88 (the gate lifts the placebo too, from 11.3% / 0.68). v1.1 beats all 100 draws on CAGR, Sharpe and Calmar.

**Chunks, CAGR (Sharpe, max drawdown):** v1.1 gives up the best chunks but fixes the worst ones.

| Version | 2008-11 | 2011-14 | 2014-17 | 2017-20 | 2020-23 | 2023-26 | All |
|---|---|---|---|---|---|---|---|
| v1.0 | 31.4% (1.69, DD -26%) | 34.4% (2.21, DD -23%) | 27.6% (1.33, DD -26%) | -2.2% (-0.05, DD -40%) | 50.9% (2.23, DD -31%) | 16.1% (0.97, DD -30%) | 24.1% (1.33, DD -40%) |
| v1.1 | 28.5% (1.93, DD -19%) | 21.5% (1.92, DD -13%) | 23.0% (1.17, DD -27%) | 6.3% (0.64, DD -25%) | 39.6% (1.87, DD -37%) | 20.9% (1.48, DD -14%) | 22.8% (1.47, DD -37%) |


**Stress (v1.1):**

| Run | CAGR | Sharpe | Calmar | MaxDD | Avg DD depth | Stability | Turnover/yr |
|---|---|---|---|---|---|---|---|
| stress cost 0.6% | 20.1% | 1.26 | 0.51 | -40% | -7.8% | 0.36 | 7.8x |
| stress cost 1.0% | 16.5% | 1.05 | 0.38 | -44% | -8.2% | 0.34 | 7.8x |
| stress resting stop | 16.5% | 1.08 | 0.42 | -39% | -8.1% | 0.34 | 8.2x |
| stress delay 1d | 21.7% | 1.33 | 0.57 | -38% | -7.4% | 0.34 | 7.8x |
| stress delay 2d | 22.8% | 1.35 | 0.60 | -38% | -7.7% | 0.36 | 7.8x |
| stress cash 6.5% | 25.6% | 1.55 | 0.73 | -35% | -7.1% | 0.36 | 7.8x |
| stress ADV cap Rs1cr | 15.4% | 1.16 | 0.51 | -30% | -7.1% | 0.25 | 5.8x |
| stress ADV cap Rs5cr | 11.1% | 1.06 | 0.50 | -22% | -6.5% | 0.18 | 4.1x |
| stress ADV cap Rs25cr | 6.3% | 0.86 | 0.39 | -16% | -5.8% | 0.11 | 2.5x |


Capacity is still the binding constraint: from Rs 25 crore with a 5%-of-volume cap, 6.3% CAGR.

### 11.4 What I did not do
- No parameter of the adopted gate was tuned; 150 days is the Residual strategy's own setting.
- Vol-target and crash-guard stacking were not adopted (above).
- The overlays' history is the same history that was used to pick them; 13 candidates were tested, which is why the rule requires both halves, the latest chunks and a cost stress, and why the final config was re-validated. It is still in-sample. The forward paper test remains the only real out-of-sample.

### 11.5 Files
`csm_aegis_strategy.py` now defaults to v1.1 (`mkt_gate=True`; `mkt_gate=False` reproduces v1.0 exactly). `test_parity.py` checks both versions against the research engine bit-for-bit and the exit rules, including the market-gate exits. Research: `decay_check/strategy_engine2.py` (all candidate overlays), `overlay_tests.py`, `v11_validation.py`, `results/overlay_addone.csv`, `results/v11_*.csv`.

---
## 12. Update v1.2 (2026-10-21): the user's "recommended upgrades" list, tested

You pasted nine proposed changes. Several came from sensitivity tables I had printed, so I treated them as post-look picks. I wrote the tests, the adoption rule and the "post-look" accounting into `PREREG.md` (Addendum 6) before running anything.

### 12.0 An important data problem found first
Another session's audit (`NEW_MOMENTUM_FACTORS_AUDIT.md`) says the `open` field in the Upstox data is not a tradable price. I checked: across the top-500 liquid stocks the open sits on average **+0.31% above the previous close every day (about +87% a year overnight)** while the whole close-to-close return is about +14% a year, and intraday (open to close) averages -0.20% a day. So every fill I modelled at the next open used a biased price.
- **I re-ran Aegis with fills that never use the open field:** orders decided at one close, filled at the next close. v1.0: 24.4% to 23.6% CAGR, Sharpe 1.30 to 1.25. v1.1: 22.9% to 21.6%, Sharpe 1.41 to 1.33. So the strategy survives, at about 1 to 1.5 points less CAGR, and **all new numbers below use close fills**.
- **Not re-checked:** the breakout and Quad faithful re-bookings and the csm_value faithful series also used opens. Aegis shows the effect is modest (about 1 to 1.5 points), but I have not re-run them.

### 12.1 Your claims, one by one

| Your proposal | What the evidence says |
|---|---|
| Upgrade A: z(R1) + z(52w-high) | The cited evidence is R3b on the Absolute/Batch/Elendel pools, not Aegis's R1. Tested on Aegis: signal IC 3m 0.044 to 0.074, IC 6m 0.035 to 0.078, top-20 excess 1.68% to 1.80% per 3 months, so it is a better ranking, but the strategy gains little (Sharpe 1.33 to 1.36). It **fails** the pre-registered rule (gain too small, one half regresses more than 5%, latest-two-chunk Sharpe lower). **Not adopted.** |
| Upgrade B: z(R1) + z(-Ulcer) | The cited IC 0.086 is for `blend_intra_ulcer`, which is intraday drift (built from the unusable open) plus low-Ulcer. It is not R1 + Ulcer, so I tested R1 + Ulcer directly. IC improves (0.044 to 0.059 in the strategy pool), but the top-20 basket excess falls from 1.68% to 1.03% per 3 months (Ulcer alone: -0.16%), so it improves the ranking of the bad names, not the picks. At strategy level it **passes**: Sharpe 1.33 to 1.46, Calmar 0.58 to 0.73, drawdown -37% to -29%, with CAGR flat. **Adopted** (a risk improvement, not a return improvement). |
| Drop the market-vol gate (volgate off) | Passed round 1 on v1.1 (Sharpe 1.37), but after the window change it adds too little, and the choice made on 2013-2026 did not transfer to 2005-2012. **Not adopted**; harmless to drop. |
| Gate window 120 instead of 150 | **Adopted.** Not an isolated spike: window 100 gives Sharpe 1.68 and 120 gives 1.69 (on v1.2), against 1.46 at 150, 1.38 at 180 and 200. |
| Remove the 45-day time stop | "383 exits, 0% win rate" is mechanical: it only exits positions already below -5%. Removing it gains 0.4 points of CAGR and 0.03 Sharpe. **Fails** (gain too small). |
| Stop 12% instead of 15% | Gain too small (Sharpe 1.33 to 1.35). **Not adopted.** |
| Cash yield 6.5% | Historical sensitivity only: v1.2 CAGR 24.2% to 26.9%, Sharpe 1.69 to 1.85 (4% yield: 25.8%, 1.79). It is not part of the current strategy result and `cash_rate` has been removed from the production implementation. |
| Vol targeting 15% | In-sample it passed round 3 (Sharpe 1.69 to 1.72, drawdown -29% to -24%, CAGR 24.2% to 22.4%; the CAGR cost was not in your summary). **Neither half chose it** in the out-of-sample test. Kept as an optional risk dial; implemented only in the research engine, not in the module. |
| Band (200, 1000) | Round 1: fails (latest-two-chunk Sharpe lower). Later rounds: stability worse by more than 20%. **Not adopted.** |
| All of it together | CAGR 30% to 31%, Sharpe 2.15 to 2.17, but 2005-2012 Sharpe 2.97 vs 1.70 to 1.72 in 2013-2026. That is the signature of over-fitting to the history; I would not expect it. |

### 12.2 Signal tests for the two selector upgrades

| Pool | Signal | IC 3m (NW-t) | IC 6m (NW-t) | Top-20 excess / 3m | Top-quintile accuracy | Overlap with R1 top-20 | Decay 3m / 6m |
|---|---|---|---|---|---|---|---|
| L3 tradeable | R1 (current) | +0.070 (5.7) | +0.075 (4.3) | +2.26% | 54.2% | 1.00 | HEALTHY / HEALTHY |
| L3 tradeable | A1 alone | +0.101 (6.8) | +0.123 (6.2) | +1.48% | 56.1% | 0.04 | DECAYING / HEALTHY |
| L3 tradeable | Ulcer alone (-UI) | +0.084 (5.4) | +0.097 (4.5) | +0.91% | 55.5% | 0.09 | HEALTHY / HEALTHY |
| L3 tradeable | S1 = R1 + A1 | +0.099 (6.6) | +0.114 (5.6) | +2.57% | 56.5% | 0.42 | HEALTHY / HEALTHY |
| L3 tradeable | S2 = R1 + (-Ulcer) | +0.087 (5.8) | +0.096 (4.6) | +1.95% | 55.6% | 0.45 | HEALTHY / HEALTHY |
| L4 strategy pool | R1 (current) | +0.044 (3.6) | +0.035 (1.8) | +1.68% | 53.1% | 1.00 | HEALTHY / WEAK / REGIME |
| L4 strategy pool | A1 alone | +0.071 (5.7) | +0.086 (5.4) | +0.45% | 54.0% | 0.07 | WEAK / REGIME / HEALTHY |
| L4 strategy pool | Ulcer alone (-UI) | +0.059 (4.0) | +0.069 (3.5) | -0.16% | 54.2% | 0.14 | WEAK / REGIME / HEALTHY |
| L4 strategy pool | S1 = R1 + A1 | +0.074 (5.5) | +0.078 (4.4) | +1.80% | 54.9% | 0.41 | HEALTHY / HEALTHY |
| L4 strategy pool | S2 = R1 + (-Ulcer) | +0.059 (4.2) | +0.058 (3.0) | +1.03% | 54.5% | 0.50 | HEALTHY / HEALTHY |


R1 + A1 also moves the holdings closer to the live books (top-20 overlap with Zenith 0.33 and Residual 0.29, against 0.17 and 0.20 for R1 alone); R1 + Ulcer stays at 0.21 and 0.21.

### 12.3 Add-one results on v1.1 (close fills), round 1 of the pre-registered selection

| Candidate | CAGR | Sharpe | Calmar | MaxDD | Passed? | Why not |
|---|---|---|---|---|---|---|
| v1.1, close fills (baseline) | 21.6% | 1.33 | 0.58 | -37% | - | - |
| S1 selector R1+A1 | 21.2% | 1.36 | 0.58 | -37% | no | a: gain too small; c: a half regresses >5%; d: latest 2 chunks Sharpe lower |
| S2 selector R1+Ulcer | 21.3% | 1.46 | 0.73 | -29% | **YES** | - |
| F1 volgate off | 22.7% | 1.37 | 0.69 | -33% | **YES** | - |
| F2 gate window 120 | 24.6% | 1.53 | 0.76 | -32% | **YES** | - |
| F3 time stop off | 22.5% | 1.36 | 0.61 | -37% | no | a: gain too small |
| F4 stop 12% | 21.6% | 1.35 | 0.59 | -36% | no | a: gain too small |
| P2 vol target 15% | 19.2% | 1.42 | 0.68 | -28% | no | b: turnover +25% |
| P3 band (200,1000) | 23.9% | 1.46 | 0.63 | -38% | no | d: latest 2 chunks Sharpe lower |


Forward selection (same rule as Addendum 5, at most 3 additions, at most 2 post-look): round 1 adopted the 120-day window, round 2 the R1 + Ulcer selector, round 3 vol targeting. Full table: `decay_check/results/overlay2_addone.csv`.

### 12.4 The test that matters: does the selection procedure survive out of sample?

I ran the same selection procedure using only one half of the history, then judged its choices on the half it never saw.

| Selection run | Chosen | In-sample Sharpe v1.1 to new | Unseen half Sharpe | Unseen Calmar | Unseen CAGR | Unseen MaxDD |
|---|---|---|---|---|---|---|
| select on 2005-2012, test on 2013-2026 | F2,S2 | 1.33 to 2.18 | 1.32 to 1.40 | 0.57 to 0.68 | 21.2% to 19.6% | -37% to -29% |
| select on 2013-2026, test on 2005-2012 | F1,F4 | 1.32 to 1.46 | 1.33 to 1.33 | 0.68 to 0.66 | 22.3% to 21.8% | -33% to -33% |


- Chosen on 2005-2012 (the 120-day window and R1 + Ulcer): on the unseen 2013-2026, Sharpe 1.32 to 1.40, Calmar 0.57 to 0.68, drawdown -37.5% to -29%, but **CAGR fell from 21.2% to 19.6%**.
- Chosen on 2013-2026 (volgate off, stop 12%): on the unseen 2005-2012 there is **no gain** (Sharpe 1.328 to 1.329).
- So the real, transferable gain is **lower drawdown and a bit better Sharpe, not more return**. The in-sample Sharpe near 1.7 overstates what to expect. I therefore adopt only the two changes that transfer (post-look change #1: vol targeting stays optional).

### 12.5 v1.2 = v1.1 + 120-day gate + R1 + Ulcer selector + close fills

![v1.2](charts/fig8_v12.png)

| Run | CAGR | Sharpe | Calmar | MaxDD | Sharpe 2005-12 / 2013-26 | Since Jan 2025 | Turnover/yr |
|---|---|---|---|---|---|---|---|
| v1.1 close fills | 21.6% | 1.33 | 0.58 | -37% | 1.33 / 1.32 | -18.4% | 7.8x |
| v1.2 (window120 + R1+Ulcer) | 24.2% | 1.69 | 0.83 | -29% | 2.18 / 1.40 | -4.6% | 6.1x |
| v1.1 open fills (as first reported) | 22.9% | 1.41 | 0.62 | -37% | 1.43 / 1.39 | -14.9% | 7.8x |
| v1.2 OPEN fills | 23.5% | 1.66 | 0.87 | -27% | 2.19 / 1.35 | -4.8% | 6.1x |
| v1.2 without window120 (150) | 21.3% | 1.46 | 0.73 | -29% | 1.62 / 1.36 | -7.0% | 6.2x |
| v1.2 without Ulcer (R1) | 24.6% | 1.53 | 0.76 | -32% | 1.79 / 1.37 | -16.6% | 7.7x |
| v1.2 + vol target 15% (optional, in-sample only) | 22.4% | 1.72 | 0.95 | -24% | 2.20 / 1.46 | -7.2% | 7.4x |
| v1.2 + 6.5% cash yield | 26.9% | 1.85 | 0.96 | -28% | 2.35 / 1.56 | +1.1% | 6.1x |
| v1.2 + 4% cash yield | 25.8% | 1.79 | 0.91 | -28% | 2.28 / 1.50 | -1.1% | 6.1x |


- **Removing either adopted piece hurts** (Sharpe 1.69 falls to 1.46 without the Ulcer term and to 1.46 without the 120-day window).
- **Both halves improve independently:** Sharpe 1.33 to 2.18 in 2005-2012 and 1.32 to 1.40 in 2013-2026; most of the gain is in the first half.
- **Placebo with the same overlays:** random picks earn 14.9% and Sharpe 0.96; v1.2 beats all 100 draws on CAGR, Sharpe and Calmar.
- **Open vs close fills no longer matters for v1.2** (23.5% / 1.66 with opens vs 24.2% / 1.69 with closes).
- **Since January 2025:** -4.6% instead of -18.4% for v1.1 on the same fills (index +4.3%).
- **Not uniformly better:** 2014-2017 is weaker (CAGR 13.4% vs 18.8%; 2016 -21.8% vs -10.1%), and the last two 3-year chunks have similar CAGR with a shallower drawdown.

**By 3-year chunk, CAGR (Sharpe, max drawdown):**

| Version | 2008-11 | 2011-14 | 2014-17 | 2017-20 | 2020-23 | 2023-26 | All |
|---|---|---|---|---|---|---|---|
| v1.1 | 21.8% (1.47, DD -20%) | 19.6% (1.84, DD -13%) | 18.8% (0.97, DD -30%) | 8.6% (0.86, DD -19%) | 37.5% (1.82, DD -37%) | 20.6% (1.41, DD -18%) | 20.8% (1.35, DD -37%) |
| v1.2 | 36.6% (2.97, DD -12%) | 28.3% (2.62, DD -8%) | 13.4% (0.85, DD -29%) | 7.8% (0.87, DD -15%) | 36.1% (1.96, DD -24%) | 20.4% (1.58, DD -12%) | 23.2% (1.70, DD -29%) |


**Robustness (v1.2):** universe-band Sharpe range 0.21 (limit 0.35, pass), CAGR range 4.8 points, max-drawdown range 2.6 points; parameter swings at +-20% at most 0.11 Sharpe.

| Run | CAGR | Sharpe | Calmar | MaxDD | Sharpe 2005-12 / 2013-26 | Since Jan 2025 | Turnover/yr |
|---|---|---|---|---|---|---|---|
| v1.2 gate window 100 | 24.2% | 1.68 | 0.83 | -29% | 2.23 / 1.36 | -4.6% | 6.1x |
| v1.2 gate window 120 | 24.2% | 1.69 | 0.83 | -29% | 2.18 / 1.40 | -4.6% | 6.1x |
| v1.2 gate window 150 | 21.3% | 1.46 | 0.73 | -29% | 1.62 / 1.36 | -7.0% | 6.2x |
| v1.2 gate window 180 | 19.9% | 1.38 | 0.69 | -29% | 1.56 / 1.27 | -24.4% | 6.2x |
| v1.2 gate window 200 | 20.3% | 1.38 | 0.51 | -40% | 1.55 / 1.28 | -30.4% | 6.1x |
| v1.2 band (1, 500) | 22.4% | 1.60 | 0.80 | -28% | 1.98 / 1.37 | -2.9% | 6.1x |
| v1.2 band (1, 1000) | 24.2% | 1.69 | 0.83 | -29% | 2.18 / 1.40 | -4.6% | 6.1x |
| v1.2 band (250, 1000) | 27.2% | 1.81 | 0.89 | -31% | 2.47 / 1.46 | -6.9% | 6.8x |
| v1.2 band (500, 1500) | 27.1% | 1.72 | 0.95 | -28% | 2.30 / 1.50 | -4.0% | 6.6x |
| v1.2 param top_n=16 | 23.2% | 1.57 | 0.70 | -33% | 2.02 / 1.31 | -4.7% | 6.0x |
| v1.2 param top_n=24 | 22.7% | 1.60 | 0.74 | -31% | 2.08 / 1.31 | -4.0% | 6.4x |
| v1.2 param stop=0.12 | 24.2% | 1.71 | 0.89 | -27% | 2.22 / 1.41 | -4.3% | 6.2x |
| v1.2 param stop=0.18 | 24.7% | 1.71 | 0.88 | -28% | 2.16 / 1.45 | -4.4% | 6.1x |
| v1.2 param trail=0.16 | 22.6% | 1.63 | 0.73 | -31% | 2.12 / 1.35 | -4.2% | 6.5x |
| v1.2 param trail=0.24 | 24.1% | 1.67 | 0.83 | -29% | 2.15 / 1.40 | -6.0% | 6.0x |
| v1.2 param hold_rank=32 | 23.6% | 1.64 | 0.72 | -33% | 2.14 / 1.36 | -4.8% | 6.6x |
| v1.2 param hold_rank=48 | 24.2% | 1.69 | 0.80 | -30% | 2.18 / 1.40 | -4.4% | 5.9x |


**Stress and ablation (v1.2):**

| Run | CAGR | Sharpe | Calmar | MaxDD | Sharpe 2005-12 / 2013-26 | Since Jan 2025 | Turnover/yr |
|---|---|---|---|---|---|---|---|
| stress cost 0.6% | 22.0% | 1.55 | 0.72 | -30% | 2.07 / 1.25 | -6.8% | 6.1x |
| stress cost 1.0% | 19.1% | 1.36 | 0.58 | -33% | 1.91 / 1.05 | -9.7% | 6.1x |
| stress delay 1d | 23.5% | 1.62 | 0.90 | -26% | 2.04 / 1.38 | -4.8% | 6.1x |
| stress delay 2d | 22.9% | 1.57 | 0.89 | -26% | 1.89 / 1.38 | -4.5% | 6.1x |
| stress ADV cap Rs1cr | 17.0% | 1.34 | 0.76 | -22% | 1.36 / 1.33 | -2.0% | 4.7x |
| stress ADV cap Rs5cr | 12.7% | 1.20 | 0.67 | -19% | 0.98 / 1.34 | -2.6% | 3.5x |
| stress ADV cap Rs25cr | 7.6% | 0.97 | 0.46 | -17% | 0.63 / 1.17 | -4.8% | 2.4x |
| v1.2 no vol-state gate C3 | 25.1% | 1.73 | 0.86 | -29% | 2.18 / 1.47 | +4.8% | 6.2x |
| v1.2 no time stop | 24.1% | 1.66 | 0.85 | -28% | 2.10 / 1.40 | -4.5% | 5.7x |
| v1.2 no M3 | 24.5% | 1.62 | 0.85 | -29% | 2.02 / 1.39 | -7.0% | 5.1x |
| v1.2 no trend gate C6 | 22.6% | 1.60 | 0.74 | -30% | 2.16 / 1.27 | -3.9% | 6.4x |
| v1.2 no hard/trail stops | 15.6% | 1.68 | 0.87 | -18% | 2.10 / 1.45 | -3.9% | 3.7x |


Capacity remains the binding limit (7.6% CAGR from Rs 25 crore with a 5%-of-volume cap).

### 12.6 What changed in the module
`csm_aegis_strategy.py` now defaults to v1.2: `selector='R1_ULCER'`, `mkt_gate_window=120`, `fill='close'`. `selector='R1'`, `mkt_gate_window=150`, `fill='open'` reproduce v1.1, and `mkt_gate=False` on top reproduces v1.0. `test_parity.py` checks all three configurations against the research engine bit-for-bit, plus the new Ulcer signal, the stop/time exits and the market-gate exits. Vol targeting is not in the module.

### 12.7 Caveats and next steps
- It is still in-sample selection on one history; the procedure test above is the best evidence I can give, and it says to expect a smaller gain than the headline.
- The optional pieces (vol targeting, cash yield, dropping the vol-state gate) are risk/return dials, not validated improvements.
- Next: forward paper trading of v1.2, and re-running the older faithful numbers (HR, VCP, Quad, csm_value) with close fills.


## 13. Rebuild (2026-10-21): structure of the strategy, and the R3b-composite x band (200, 1000) hypothesis

### 13.1 What was wrong with the previous layout
The logic existed (pool filters, stops, sizing, gates) but sat inside one long function in one file, with no logs and no diagnostics, so from outside it read like a bare ranker. The strategy is now laid out like the breakout books in `Old_live_strategies`: a strategy core, a backtest engine with logs, and a thin runner. Numbers are unchanged by the rebuild: `test_parity.py` matches the research engine to 0.0 on all 12 configurations (trades, returns, exits), plus the signal values and the live exit rules.

### 13.2 What each file now holds
| Layer | Where | What it does |
|---|---|---|
| Universe | `filter_universe`, `universe_card` | price >= 20, 63-day turnover rank band (default 1-1000; `v1.2_high_return` 200-1000), circuit-day cap (<= 5 in 21 days), close > SMA200, M3 exclusion. The card prints the average names surviving each filter by year. |
| Signal | `calculate_factors`, `score_pool` | R1 residual momentum, plus Ulcer (default) or 52-week-high z. Placebo mode for random picks. |
| Selection | `select_entries` | top 20, kept until rank 40 (hysteresis); extension filter (> 25% above SMA50 blocked), optional vol-state and absolute-momentum / falling-knife gates, cooldown after a stop. Every rejection is logged with its reason. |
| Portfolio | `entry_weight`, engine loop | 1% risk per trade / 15% stop distance, weight clamped to 3-8%, gross cap, ADV capacity cap, cash yield option, execution delay. |
| Exits and stops | `check_stop_exit` (one implementation used by backtest and live) | -15% from entry, -20% from peak (close based), time stop (45 days and below -5%), 120-day market trend gate (exit all and block entries below the SMA of the equal-weight index). |
| Risk overlays (off by default) | `exposure_target` | vol target, crash guard, regime leverage, correlation guard, ATR chandelier, min-hold. |
| Live use | `latest_picks`, `get_exit_signals` | month-end picks table with weights and entry stops; exit signals for current holdings. |
| Logs and diagnostics | `csm_aegis_backtest.py` | trade log, reject log, daily log, yearly returns, exit breakdown, trade stats, IC at 1/3/6/12m inside the pool with Newey-West t and 36-month chunk decay, performance plot. |

Run: `python3 csm_aegis_backtest.py` (v1.2), `--preset v1.2_high_return`, `--compare`, `--stress`, `--set key=value`. Outputs land in `output/`. See `README.md`.

### 13.3 Your hypothesis: R3b composite in band (200, 1000) raises CAGR and lowers max drawdown
Pre-registered as Addendum 7 before any run. Baseline v1.2: CAGR 24.2%, Sharpe 1.69, Calmar 0.83, MaxDD -29.0%. Close fills, faithful booking, 0.3% per leg.

| Run | CAGR | Sharpe | Calmar | MaxDD | Sharpe 2005-12 / 2013-26 | Since Jan 2025 |
|---|---|---|---|---|---|---|
| v1.2 baseline (R1+Ulcer, 1-1000) | 24.2% | 1.69 | 0.83 | -29.0% | 2.18 / 1.40 | -4.6% |
| R1+Ulcer, band 200-1000 (band only) | 28.0% | 1.88 | 0.94 | -29.9% | 2.65 / 1.46 | -9.9% |
| R1+52wH (pasted R3b), band 1-1000 | 24.7% | 1.60 | 0.77 | -32.0% | 2.04 / 1.33 | -13.3% |
| R1+52wH (pasted R3b), band 200-1000 | 29.5% | 1.91 | 1.00 | -29.5% | 2.75 / 1.47 | -6.4% |
| Residual book's own R3b, band 1-1000 | 22.1% | 1.35 | 0.68 | -32.4% | 1.57 / 1.20 | -2.6% |
| Residual book's own R3b, band 200-1000 | 20.2% | 1.38 | 0.75 | -26.9% | 1.18 / 1.45 | -4.9% |

What it says:
- **CAGR: yes, by about 5 points, and it is the band doing it.** R1+Ulcer in 200-1000 already gets 28.0%; swapping in the composite adds 1.5 points on top. Dropping the 200 most liquid names helps because the top of the liquidity ranking has the weakest residual-momentum signal, which is consistent with the Quad finding.
- **Max drawdown: no.** -29.0% becomes -29.5% (composite) or -29.9% (band only). Nothing lowers it; the one run with a lower drawdown (-26.9%) is the residual book's own composite, which loses CAGR and Sharpe.
- **Pre-registered criteria: not met.** The composite in 200-1000 fails stability (worse by more than 20%) and the latest-two-chunks Sharpe check; band-only fails stability. Band neighbours 150 and 250 do hold up (Sharpe 1.84 and 1.94, so there is a plateau), and both halves improve on Sharpe, so the band is not a spike. The 2005-12 half carries most of the gain (CAGR 32% -> 40%) against 20% -> 22% in 2013-26.
- **The composite as the Residual book computes it (its own R3b) is worse than R1+Ulcer** in either band. So "R3b composite" only helps in the pasted form z(R1)+z(close/252d high), and there the gain over R1+Ulcer is small.
- **Cost of the extra CAGR:** turnover 6.1x -> 7.5x per year, and the since-2025 drawdown gets worse (-4.6% -> -6.4% to -9.9%). More capacity-hungry too, since the cheaper-to-trade top 200 names are removed.

Decision: not adopted as the default (post-look change budget untouched). `v1.2_high_return` (R1 + 52-week-high, band 200-1000) is shipped as an opt-in preset: higher return, same drawdown, higher turnover, weaker recent months. Sources: `decay_check/results/addendum7_runs.csv`, `addendum7_judged.csv`.

### 13.4 Still open
Forward paper trading of v1.2; re-running the older faithful numbers (HR, VCP, Quad, csm_value) with close fills; the survivorship and capacity caveats of section 7 are unchanged.


## 14. Update (2026-10-21): second improvement list and six OHLCV universe filters, tested

Pre-registered as Addendum 8. Baseline = v1.2 (24.2% CAGR, Sharpe 1.69, Calmar 0.83, MaxDD -29.0%, 0.3% per leg, close fills). Every item was run through the product module; the new switches (`atr_stops`, `liq_mode`) are research options, off by default, and the default configuration still matches the research engine bit-for-bit.

### 14.1 The quoted yearly figures check out
2008 -15.6% (worst DD -18.3%), 2020 worst DD -12.9%, 2021 +82.4%, 2025 worst DD -11.7% all match `output/yearly_returns_v1_2.csv`.

### 14.2 Part 1 improvements
| Run | CAGR | Sharpe | Calmar | MaxDD | Turnover/yr | Since Jan 2025 | Verdict (Addendum 5 criteria) |
|---|---|---|---|---|---|---|---|
| baseline v1.2 | 24.2% | 1.69 | 0.83 | -29.0% | 6.1x | -4.6% | |
| 1. cash 6.5% on idle cash | 26.9% | 1.85 | 0.96 | -28.0% | 6.1x | +1.1% | passes (mechanical) |
| 2. vol gate off | 25.1% | 1.73 | 0.87 | -29.0% | 6.2x | +4.8% | gain too small |
| 3. ATR stops + risk sizing | 24.0% | 1.70 | 0.91 | -26.5% | 6.1x | -3.7% | gain too small; latest chunks Sharpe lower |
| 4. hold_rank 50 | 24.4% | 1.70 | 0.85 | -28.7% | 5.8x | -4.5% | gain too small; latest chunks lower |
| 4. hold_rank 60 | 24.9% | 1.73 | 0.89 | -28.0% | 5.6x | -2.7% | gain too small |

- **Cash yield is real money, but external to the strategy.** This historical sensitivity measured a 2.7-point CAGR uplift from a 6.5% sweep. It is no longer modeled in the production implementation; the strategy reports zero return on uninvested cash and the account layer must report any cash-product return separately.
- **Vol gate off** is the same result as Addendum 6 (F1): +0.9 points of CAGR (your text says +1.2), +0.04 Sharpe, and a better 2025-26 (+4.8% vs -4.6%). It does not clear the pre-registered gain threshold, so it stays a documented dial, not a default.
- **ATR stops and sizing** cut max drawdown from -29.0% to -26.5% but not Sharpe or CAGR. One arithmetic correction: with 1% risk and the stop clipped to 8-18% the position size is 5.6%-8%, never the 3-4% described, so quiet and volatile names differ less in size than the text implies. I did not separately measure gap-down slippage on stops.
- **hold_rank 50** cuts turnover by 5% (60 by 8%), not 15-20%, and the since-2025 result is flat. The 48 setting in the Stage-3 table already showed this.

### 14.3 Part 2: the six OHLCV liquidity filters (all shifted one day, same as the default)
| Filter | CAGR | Sharpe | Calmar | MaxDD | Pool (names) | Baseline pool kept | CAGR at Rs 5cr, 5% ADV cap | Verdict |
|---|---|---|---|---|---|---|---|---|
| default (63d mean rupee volume rank) | 24.2% | 1.69 | 0.83 | -29.0% | 359 | 100% | 12.7% | |
| U1 20th-percentile turnover, top 1000 | 24.3% | 1.70 | 0.87 | -27.9% | 356 | 97% | 12.7% | gain too small |
| U1b 20th-pct turnover >= Rs 25 lakh | 20.3% | 1.43 | 0.66 | -31.1% | 266 | 70% | 13.8% | regresses |
| U2 Amihud capacity, top 1000 | 24.2% | 1.69 | 0.83 | -29.1% | 355 | 96% | 13.0% | no change |
| U3 continuity >= 0.95 (126d) | 23.4% | 1.63 | 0.78 | -30.1% | 350 | 97% | 12.7% | worse at 0.6% cost |
| U4 volume CV <= 1.8 | 23.0% | 1.58 | 0.76 | -30.4% | 300 | 83% | 13.2% | half regresses |
| U5 Corwin-Schultz, drop worst 15% | 23.5% | 1.68 | 0.78 | -30.1% | 301 | 84% | 13.1% | worse at 0.6% cost |
| U6 composite as pasted (raw floor z) | 23.5% | 1.65 | 0.76 | -31.0% | 356 | 96% | 12.7% | worse at 0.6% cost |
| U6b composite with log floor | 24.7% | 1.72 | 0.93 | -26.6% | 356 | 97% | 12.8% | passes the judge, see below |

What this says:
- **The default liquidity rank is already close to the pasted composite.** 96-97% of the names are the same; the measures differ only at the margin. No filter lifts CAGR or Sharpe by more than the noise below.
- **U6b is not a real improvement.** U6 and U6b differ only by a log transform of one input (about 4% of the pool changes) yet go from fail (-31.0% drawdown) to pass (-26.6%). To measure how much a small change of the pool moves the result by chance, I dropped a random 4% of the baseline pool every month, 12 times: Sharpe ranges 1.55-1.71 (standard deviation 0.05), Calmar 0.70-0.95 (0.07), MaxDD -31.4% to -26.0% (1.6 points). U6b (1.72, 0.93, -26.6%) sits inside that envelope. The same noise explains why hold_rank, ATR stops and similar items move MaxDD by two to three points.
- **What it tells you about the earlier ideas:** differences of ±0.05 in Sharpe or ±2 points in MaxDD between close variants of this strategy cannot be distinguished from chance. Only the cash yield (a mechanical +2.7 points) and the band effect (Section 13: +4 points of CAGR, tested at 150 and 250) are larger than the noise.
- **Capacity:** none of the filters changes the Rs 5 crore result materially (12.7%-13.8%); the binding limit is still the 5%-of-volume cap, not which illiquid names are in the pool. The hard Rs 25 lakh floor (U1b) shrinks the pool by 30% and costs 4 points of CAGR.
- Your three structural arguments (pump-and-dump entry, circuit lock volume, turnover clumping) are sound in principle, but the pool already requires price >= 20, at most 5 circuit days and a 200-day trend filter, and the measured effect of adding those same ideas is within noise.

### 14.4 Decision
No change to the v1.2 default. Cash-yield results are historical sensitivities only and are excluded from the production implementation. The ATR-stop and OHLCV-liquidity options are kept in the module as research switches (`atr_stops`, `liq_mode`), off by default. Post-look change budget for Addendum 8: unused. Files: `decay_check/addendum8.py`, `addendum8_noise.py`, `results/addendum8_runs.csv`, `results/addendum8_noise.csv`.

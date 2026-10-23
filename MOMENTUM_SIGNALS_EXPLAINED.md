# Momentum Signals Explained — What Each One Measures, How It Is Built, and How It Performed

**Date:** 2026-09-22
**Code:** `momentum_family_bakeoff.py` (every formula below is copied from `build_signals()` in that file)
**Outputs:** `momentum_family_bakeoff_results.csv` (single signals), `momentum_family_bakeoff_blends.csv`
(blends), `momentum_family_bakeoff_yearly_ic.csv` (IC per calendar year)
**Supersedes the numbers in** `MOMENTUM_FAMILY_BAKEOFF_REPORT.md` (that run used only 2010-2025).

---

## 0. Data window — read this first

Requested window: **2000-2025**. Source: `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data`
(5,205 CSVs). The script loads everything from 2000-01-01, but the folder does not actually have
usable history that early:

| year | tickers with a price | in top-1000 universe |
|---|---|---|
| 2000-2002 | **3** | **2** |
| 2003 | 445 | 235 |
| 2005 | 520 | 445 |
| 2008 | 1,512 | 810 |
| 2015 | 1,882 | 926 |
| 2025 | 4,267 | 986 |

A month is only scored if at least 30 stocks have both a signal and a forward return, and most
signals need 12 months of history first. So **the effective IC window is 2003 → 2025-12**
(first scored month 2003-01 to 2004-08 depending on the signal; seasonality from 2006-02 because it
needs 3+ years of same-month history). That is 239-274 scored months per signal. 2000-2002 cannot
be tested with this data folder — it would need a different source.

Early years (2003-2007) have a much smaller universe (235-630 names), so the "top-1000" filter is
effectively "every liquid stock" there.

---

## 1. How to read the metrics

Every month-end, each stock gets a signal value. We then check whether stocks with higher values
went on to earn higher returns.

| metric | what it means | good value |
|---|---|---|
| **IC** (Information Coefficient) | Rank correlation (Spearman) between the signal and the next 63 trading days' return, across all stocks in the universe that month. Averaged over all months. +1 = perfect ranking, 0 = useless, negative = backwards. | > 0.03 is useful for stock selection; > 0.08 is strong |
| **IC_21 / IC_63** | Same, for a 21-day (1 month) and 63-day (3 month) forward return. | |
| **NW-t** | t-statistic of the average IC, corrected (Newey-West) for the fact that 63-day returns measured every month overlap. Tells you whether the IC could be luck. | > 2 = significant, > 3 = robust |
| **ICIR** | Average IC ÷ standard deviation of monthly IC. How *consistent* the signal is month to month. | > 0.5 is good for a monthly signal |
| **Hit rate** | % of months with IC > 0. | > 60% |
| **Sub-period IC** | IC averaged within 2003-10, 2011-17, 2018-25 separately. A real signal should be positive in all three. | same sign in all 3 |
| **Corr with BASE** | Average cross-sectional rank correlation with the signal your live books use today. 1.0 = same information; 0 = completely different. | lower = more *new* information |
| **Incremental IC / t** | IC of the signal *after* removing everything it shares with BASE (each month: regress the signal's ranks on BASE's ranks, keep the residual, correlate with forward return). This is the key column: does it add anything to what you already have? | t > 2 |
| **Top-quintile excess %/yr** | Average 1-month return of the top 20% of stocks by the signal, minus the universe average, ×12. What a long-only book buying the top fifth would have earned above the market. (Returns winsorised 1/99% per month.) | higher is better |
| **Q5−Q1 %/yr** | Top fifth minus bottom fifth, ×12. The full long-short spread. | |
| **Mono** | Rank correlation between quintile number (1-5) and quintile return. 1.0 = returns rise steadily from worst to best quintile. | ≥ 0.9 |

**Test mechanics (same for every signal):**
- Universe each day: top 1,000 stocks by 63-day average rupee volume, price ≥ ₹10, ≤ 5 circuit-locked
  days in the last 63, all measured on the previous day (`sr_panel.compute_universe_mask`).
- Corporate-action days (1-day move < −40% or > +300%) have their close masked to NaN (`sr_panel.mask_corporate_actions`).
- The signal is read at the **previous** day's close (one extra day of lag — conservative).
- Forward return = buy at the **next day's open**, sell at the close 21 or 63 trading days later.
- Scored at every month-end (your momentum books rebalance monthly).

---

## 2. The reference: what your live strategies already use

### BASE — Dual-lookback Sharpe momentum (12m + 6m, skip 1 month)

**In plain words:** How much did the stock rise over the last year and the last half-year, measured
per unit of volatility, ignoring the most recent month. This is the csm_batch / csm_quad signal.

**Formula (daily approximation of the monthly version in `csm_batch_strategy.calculate_factors`):**
```
leg(L)   = [ P(t−21) / P(t−21−L) − 1 ]  /  [ stdev(daily returns over L days, lagged 21) × √252 ]
leg is clipped to [−5, +5]
BASE     = ( leg(231) + leg(105) ) / 2          # ≈ 12m-skip-1m and 6m-skip-1m
```
**Example:** a stock that rose 60% from 12 months ago to 1 month ago with 30% annual volatility has a
12m leg of 2.0; if it rose 25% over 6m-to-1m with 28% vol its 6m leg is 0.9; BASE = 1.45.

**Result:** IC_63 **0.074**, NW-t 6.09, ICIR 0.57, positive in all three sub-periods (0.079 / 0.086 /
0.059), top-quintile excess **+8.3 %/yr**, mono 1.0. A genuinely good signal — the problem is not
that it is weak, it is that every variant you have built is the *same* signal.

### CTRL — Plain 12-month return, skip 1 month
```
CTRL = P(t−21) / P(t−252) − 1
```
Included to prove the point in the brief: correlation with BASE **0.91**, incremental IC **−0.017**
(t −1.66). Changing the lookback, or the risk-adjustment, gives the same information. Adding a
4th, 5th or 6th window will not help.

---

## 3. The signals, family by family

Each entry: **what it measures → exact formula → how to read it → why it could work → result → verdict.**

---

### Family A — Anchor momentum ("where is the price relative to its extreme?")

These do not ask "how much did it go up?" They ask "how close is it to its best level?" Two stocks
can have the same 12-month return but one is at its high and the other has fallen 25% from it.
BASE cannot tell them apart; these signals can.

#### A1 — 52-week-high proximity  ⭐ rank 1
**Measures:** How close today's close is to the highest price of the last year.
```
A1 = Close(t) / max( High over last 252 days )        # needs ≥ 200 days of history
```
**Read it:** 1.00 = at the 52-week high today. 0.80 = 20% below it. Higher is better. Range (0, 1].
**Example:** high of the year ₹500, close ₹480 → 0.96. Another stock with high ₹500, close ₹350 → 0.70.
**Why it could work:** George & Hwang (2004). Traders anchor on the 52-week high as a reference
price and are reluctant to buy above it, so good news near the high is absorbed slowly; when the
stock breaks through, it keeps drifting. This is the same information your breakout books trade on
as an *event*; here it is used as a continuous *ranking*.
**Result (2003-2025):** IC_63 **0.095** (NW-t 6.16) — higher than BASE. Positive in every sub-period
(0.087 / 0.108 / 0.089) and **held up best after 2018**. Corr with BASE only **0.57**; incremental
IC **0.074, t 5.93** — nearly all of its predictive power is new information. 20 of 23 years positive.
**But:** top-quintile excess is only **+4.6 %/yr** (below BASE's 8.3). Its IC comes disproportionately
from correctly identifying the *losers* (stocks far below their high keep falling). On its own it
is a better filter than selector; combined with a trend signal it becomes a strong selector (§4).
**Verdict:** best new information in the test. Use it inside a blend.

#### A2 — 52-week range position ("RangePos")
**Measures:** Where today's close sits between the year's low and the year's high.
```
A2 = ( Close − min(Close, 252d) ) / ( max(Close, 252d) − min(Close, 252d) )
```
**Read it:** 0 = at the 52-week low, 1 = at the 52-week high, 0.5 = halfway.
**Example:** low ₹200, high ₹500, close ₹440 → (440−200)/(500−200) = 0.80.
**Difference from A1:** uses the low as well, so a stock that has only moved within a narrow range
can still score high. Uses closes, not intraday highs.
**Result:** IC_63 0.081 (NW-t 6.35), all 3 sub-periods positive, corr with BASE 0.70, incremental
t 5.74, top-quintile excess +7.1 %/yr, mono 1.0.
**Verdict:** strong, but 0.87 correlated with A1 — they carry the same idea. Pick one of A1/A2/A3.

#### A3 — Relative-strength line at its 52-week high  ⭐ rank 1 (alternative to A1)
**Measures:** Is the stock's *outperformance vs the market* at its best level of the year?
```
RS_line(t) = Close(t) / Benchmark(t)                   # benchmark = equal-weight universe index
A3         = RS_line(t) / max( RS_line over last 252 days )
```
**Read it:** 1.00 = the stock is outperforming the market by more than at any point in the last
year. 0.90 = its relative performance is 10% off its best.
**Example:** a stock that is flat while the market falls 10% has a *rising* RS line and can score
1.00 even though its own price is not at a high.
**Why it could work:** the O'Neil / IBD "RS line new high" idea — leadership shows up in relative
strength before price. It also strips out market moves, so it is less distorted in crashes.
**Result:** IC_63 **0.094**, NW-t **6.90** (the strongest t in the anchor family), ICIR 0.64,
sub-periods 0.092 / 0.107 / 0.085, corr with BASE 0.72, incremental IC 0.059 (t 5.88),
top-quintile excess **+8.4 %/yr**, mono 1.0. 20 of 23 years positive.
**Verdict:** the best *single* anchor signal for a long-only book (better top-quintile returns than
A1, nearly the same IC). Recommended.

#### A4 — New-high recency
**Measures:** How many trading days since the stock last made a 52-week closing high.
```
A4 = −( trading days since Close(t) ≥ max(Close, 252d) )
```
**Read it:** 0 = made a new high today; −30 = last high was 30 days ago; higher is better.
**Result:** IC_63 0.044 (t 4.24), but 2003-10 IC only 0.027, incremental t **1.42** (not significant).
**Verdict:** a blunter version of A1 — reject in favour of A1/A3.

---

### Family Q — Trend quality ("how *clean* was the move, not how *big*?")

Two stocks both up 40%: one climbed steadily, the other sat still for 10 months then jumped in 3
days on news. BASE scores them almost identically. These signals separate them.

#### Q5 — Trend persistence  ⭐ rank 2
**Measures:** The share of the last 6 months the stock spent above its own 50-day moving average.
```
above(t) = 1 if Close(t) > SMA50(t) else 0
Q5       = mean( above ) over the last 126 days            # needs ≥ 100 days
```
**Read it:** 0.90 = above its 50-day average on 90% of the last 126 days (a steady uptrend).
0.30 = mostly below it. Range [0, 1].
**Example:** a stock that spent 113 of the last 126 days above its SMA50 → 0.90.
**Why it could work:** persistence captures trends driven by steady institutional accumulation,
which tend to continue, rather than one-off jumps, which tend to fade. It is also naturally robust
to single outlier days, which a return-based signal is not.
**Result:** IC_63 0.085 with **NW-t 8.07 — the highest t-stat of every signal tested**, and the
best **ICIR (0.74)** and hit rate (78%). Positive in all sub-periods (0.098 / 0.089 / 0.069) and in
**21 of 23 years**. Corr with BASE 0.77, incremental IC 0.042 (**t 6.62**). Top-quintile excess
+8.4 %/yr, mono 1.0.
**Verdict:** the most *reliable* signal found. Recommended.

#### Q4 — Trend R² (126 days), signed
**Measures:** How closely the log-price followed a straight line over 6 months, with the sign of the move.
```
R²   = R-squared of an OLS fit  log(Close) ~ time  over the last 126 days
Q4   = R² × sign( 126-day return )
```
**Read it:** +0.9 = a very straight uptrend; −0.9 = a very straight downtrend; ~0 = choppy.
**Result:** IC_63 0.074 (t 7.30), sub-periods all positive, corr with BASE 0.75, incremental t 3.60.
**Verdict:** good, but a weaker cousin of Q5 (lower incremental IC). Use Q5.

#### Q3 — Clenow adjusted slope (90 days)
**Measures:** The annualised growth rate of the best-fit exponential trend, multiplied by how well it fits.
```
slope = OLS slope of log(Close) on time over 90 days
Q3    = ( exp(slope × 252) − 1 ) × R²
```
**Read it:** a stock trending at 50%/yr with R² 0.8 → 0.40.
**Result:** IC_63 0.056 (t 5.38), corr with BASE 0.61, but incremental t only **1.38**.
**Verdict:** its magnitude part is already in BASE; its quality part is already in Q5. Reject.

#### Q1 — Frog-in-the-pan smoothness (Da, Gurun & Warachka 2014)
**Measures:** Whether the 12-month move came from many small up days (continuous) or a few big days (discrete).
```
pos = share of days with a positive return, over [t−252, t−21]
neg = share of days with a negative return, same window
ID  = sign(12-1m return) × (neg − pos)          # "information discreteness"
Q1  = −ID                                        # higher = smoother
Q2  = z(12-1m return) + z(−ID)                  # the paper's combined version
```
**Read it:** a winner with 60% up days has ID = −0.2 → Q1 = +0.2 (smooth, good).
**Why it should work (US evidence):** investors under-react to information that arrives in small
pieces, so smooth winners keep winning.
**Result:** IC_63 **−0.006 (t −0.60)**; Q2 IC 0.005 (t 0.59) and incremental t −1.99.
**Verdict:** does not work on Indian data in any sub-period. Reject. (Q5 captures the "smoothness"
idea in a way that does work.)

---

### Family R — Residual momentum

#### R1 — Residual (beta-stripped) momentum (Blitz, Huij & Martens 2011)
**Measures:** Momentum in the part of the stock's return that is *not* explained by the market.
```
beta(t)   = cov(stock ret, market ret) / var(market ret)   over 252 days, lagged 1 day
resid(t)  = stock ret(t) − beta(t) × market ret(t)
R1        = sum(resid over [t−252, t−21]) / stdev(resid over the same window)
```
**Read it:** a stock that outperformed what its beta implied, consistently, scores high.
**Why it could work:** strips out the market-timing component, which is what makes classic
momentum crash in sharp rebounds.
**Result:** IC_63 0.071 (t 5.83), positive in every sub-period — but corr with BASE **0.90**,
incremental IC 0.006 (t **0.76**).
**Verdict:** on this data it is your current signal with the beta taken out; it adds almost nothing
new. Low priority (possibly useful only as a crash-robust *replacement* for BASE, not an addition).

---

### Family I — Cross-asset momentum

#### I1 — Sector (industry) momentum (Moskowitz & Grinblatt 1999)
**Measures:** How strongly the stock's *sector* has trended; every stock inherits its sector's score.
```
sector index = equal-weight average of member stocks' daily returns (11 sectors, instruments_clean.csv)
I1           = SectorIndex(t−21) / SectorIndex(t−147) − 1        # sector 6m return, skip 1m
```
**Read it:** every stock in a sector that rose 25% over 6-to-1 months ago gets 0.25.
**Result (full history):** IC_63 0.028 (t 2.71), corr with BASE only 0.23 — but the IC **decays
to near zero**: 0.050 (2003-10) → 0.024 (2011-17) → 0.011 (2018-25); only 14 of 23 years positive;
incremental t **1.31**.
**Verdict:** looked useful on 2010-2025 alone; the full history shows the edge fading. Demoted —
only worth using with a finer industry classification than 11 sectors (not tested).

---

### Family V — Volume and volatility

#### V1 — Up-day vs down-day volume
**Measures:** Is more volume traded on up days than down days (accumulation vs distribution)?
```
V1 = log( (Σ volume on up days over 63d + 1) / (Σ volume on down days over 63d + 1) )
```
**Result:** IC_63 0.019 (t 2.86) but **−0.004 in 2018-25**; incremental t −0.30.
**Verdict:** dead in the recent era, no new information. Reject.

#### V2 — Volatility contraction (the "coil")
**Measures:** Is the stock's current volatility low compared with its own recent history?
```
ATR%(t) = ATR14(t) / Close(t)                       # Wilder ATR
V2      = −( ATR%(t) / median(ATR% over 126 days) )
```
**Read it:** −0.6 = volatility is 40% below its 6-month norm (tightly coiled); −1.5 = 50% above it.
**Why it could work:** the Minervini VCP idea behind your VCP breakout strategy — volatility
compresses before a directional move; buying in a quiet phase also means a tighter stop.
**Result:** IC_63 0.023 (t 4.26), all sub-periods positive, corr with BASE **0.00**, incremental t
**4.14** — genuinely different information. But top-quintile excess only **+2.7 %/yr**.
**Verdict:** not a stock *selector*. Use it as an **entry-timing filter** on names BASE/A3/Q5 have
already chosen — this is exactly "Fix 3" in `POSITION_SIZING_BREAKOUT_VS_MOMENTUM.md`.

---

### Family M — Short-term shape of the move

#### M3 — Low maximum daily return ("lottery" filter, Bali, Cakici & Whitelaw 2011)
**Measures:** The biggest single-day gain in the last month, inverted.
```
M3 = −max( daily return over the last 21 days )
```
**Read it:** a stock whose best day last month was +2% scores −0.02; one that had a +18% spike
scores −0.18 (worse).
**Why it could work:** investors overpay for lottery-like stocks with big one-day spikes, which
subsequently underperform.
**Result:** IC_63 0.039 (t 4.15), IC_21 0.045 (t 7.10), corr with BASE **−0.01**, incremental t
**4.54**, and — unusually — *stronger* in 2018-25 (0.057) than earlier. **But top-quintile excess
is −0.3 %/yr** and mono only 0.3: all of the IC comes from the bottom of the ranking (the spike
stocks that crash), none from picking winners.
**Verdict:** an excellent **exclusion filter** (drop names with a big recent spike), useless as a
selector.

#### M1 — Momentum acceleration
```
M1 = (3-month return) − (return from 6 months ago to 3 months ago)
```
**Result:** IC_63 −0.006 (t −0.70). **Reject** — whether momentum is speeding up or slowing down
has no predictive value here.

#### M2 — 1-month reversal
```
M2 = −(21-day return)
```
**Result:** IC_63 **−0.024 (t −2.93)**, incremental t −2.90. The sign is negative, which means the
opposite of reversal: **last month's winners keep winning** over the next 3 months.
**Side finding:** BASE deliberately *skips* the last month (standard in US research because of
1-month reversal). On this data that month carries positive information. A cheap test for the live
books is `lag_months = 0`.

---

### Family T — Calendar

#### T1 — Seasonality (Heston & Sadka 2008)
**Measures:** How the stock performed in the *same calendar month* in each of the last 5 years.
```
T1(month m) = average of the stock's return in month m+1 of years −1…−5   # needs ≥ 3 of 5
```
**Result:** IC_63 **−0.016 (t −2.69)** — significantly *negative*, driven by 2003-10 (−0.044).
**Verdict:** reject. Not a usable momentum signal on Indian data.

---

## 4. Blends — putting the pieces together

Each blend = equal-weight sum of the components' cross-sectional z-scores each month.

| blend | IC_63 | NW-t | ICIR | 2003-10 | 2011-17 | 2018-25 | corr w/ BASE | **top-decile excess %/yr** |
|---|---|---|---|---|---|---|---|---|
| BASE (live today) | 0.074 | 6.09 | 0.57 | 0.079 | 0.086 | 0.059 | 1.00 | **7.0** |
| 52w-high alone | 0.095 | 6.16 | 0.57 | 0.087 | 0.108 | 0.089 | 0.57 | 5.0 |
| BASE + 52w-high | 0.096 | 6.55 | 0.61 | 0.100 | 0.107 | 0.084 | 0.89 | 9.0 |
| **RS line + Trend persistence** | 0.096 | **7.39** | **0.69** | 0.102 | 0.107 | 0.083 | 0.81 | **10.1** |
| 52w-high + RS line + Persistence | **0.101** | 7.13 | 0.66 | 0.105 | 0.112 | 0.089 | 0.76 | 9.8 |
| 52w-high + Persistence + Low-MAX | **0.110** | **8.02** | **0.73** | 0.116 | 0.111 | **0.105** | 0.67 | 7.2 |
| … + Sector | 0.111 | 7.73 | 0.71 | 0.127 | 0.106 | 0.100 | 0.66 | 8.5 |

How to read this:
- **For a long-only top-N book (what you trade), top-decile excess is the column that matters.**
  RS line + Trend persistence earns **+10.1 %/yr** above the universe vs **+7.0 %/yr** for BASE —
  about 45% more, with a higher t-stat and ICIR.
- Adding Low-MAX gives the **highest IC and the best 2018-25 stability**, but *lowers* top-decile
  excess (7.2) — it improves the ranking of the bad names, not the good ones. That is why Low-MAX
  belongs as a filter (exclude spike stocks) rather than inside the ranking score.

## 5. Year-by-year IC (63-day horizon)

| year | BASE | 52w high | RS line | Persistence | Low-MAX | Vol contr. | Sector | Blend 52wH+RS+Persist |
|---|---|---|---|---|---|---|---|---|
| 2003* | .350 | .096 | .070 | .156 | .047 | .023 | .074 | .155 |
| 2004 | .028 | −.056 | −.011 | −.007 | −.011 | .056 | −.072 | −.022 |
| 2005 | .178 | .107 | .161 | .155 | .005 | .040 | .134 | .176 |
| 2006 | .097 | .130 | .106 | .115 | .044 | −.018 | .009 | .128 |
| 2007 | .132 | .147 | .152 | .156 | −.034 | −.008 | .134 | .165 |
| 2008 | .002 | .141 | .117 | .045 | .078 | .032 | .046 | .113 |
| 2009 | −.062 | −.094 | −.080 | −.019 | −.010 | −.000 | −.085 | −.072 |
| 2010 | .148 | .207 | .189 | .187 | .080 | .062 | .140 | .214 |
| 2011 | .120 | .147 | .143 | .115 | .054 | .004 | .037 | .142 |
| 2012 | .119 | .170 | .158 | .113 | .084 | .033 | −.007 | .161 |
| 2013 | .101 | .127 | .118 | .091 | .036 | .017 | .049 | .122 |
| 2014 | .120 | .122 | .134 | .160 | −.023 | .062 | .023 | .165 |
| 2015 | .038 | .043 | .048 | .041 | .039 | .020 | .101 | .047 |
| 2016 | .024 | .033 | .045 | .018 | .038 | .022 | −.028 | .037 |
| 2017 | .080 | .116 | .105 | .085 | .001 | .045 | −.006 | .109 |
| 2018 | .073 | .208 | .157 | .105 | .149 | .005 | −.004 | .172 |
| 2019 | .151 | .213 | .190 | .153 | .110 | .028 | .065 | .200 |
| 2020 | −.058 | −.072 | −.050 | .013 | .022 | .046 | −.061 | −.043 |
| 2021 | .131 | .056 | .109 | .082 | −.018 | .064 | .038 | .097 |
| 2022 | −.000 | .109 | .083 | .031 | .059 | −.018 | −.003 | .078 |
| 2023 | .118 | .052 | .100 | .103 | −.055 | −.008 | .054 | .100 |
| 2024 | .015 | .069 | .026 | .023 | .097 | .003 | −.011 | .039 |
| 2025 | .045 | .080 | .063 | .044 | .090 | .013 | .012 | .066 |
| **years > 0** | 20/23 | 20/23 | 20/23 | **21/23** | 17/23 | 18/23 | 14/23 | 20/23 |

\*2003 = a few months on ~235 stocks; treat as noise.

What the yearly view shows:
- **Momentum crashes hit everything in the same years** (2009, 2020 — sharp V-shaped rebounds after
  a crash, when last year's losers rally hardest). Only **Trend persistence** stayed positive in
  2020 (+0.013) and lost least in 2009 (−0.019 vs −0.062 for BASE).
- **2008 and 2022:** BASE had zero IC; 52w-high/RS line had 0.08-0.14. Anchor signals help most in
  falling markets — the stocks holding near their highs are the true leaders.
- **2021 and 2023:** BASE beat the anchor signals (broad, fast rallies where magnitude mattered
  more than proximity to the high) — which is why blending BASE-like trend information with an
  anchor signal is more robust than replacing one with the other.

## 6. Final ranking

| rank | signal | role | why |
|---|---|---|---|
| 1 | **RS line at 52w high (A3)** / 52w-high proximity (A1) | selector | IC ≥ BASE, only 0.57-0.72 shared with BASE, incremental t ≈ 5.9, strongest in bear years |
| 2 | **Trend persistence (Q5)** | selector | highest t (8.07), highest ICIR, 21/23 years positive, least hurt in momentum crashes |
| 3 | **Blend A3 + Q5** (± A1) | the recommended new ranking score | top-decile excess 10.1 %/yr vs 7.0 for BASE |
| 4 | **Low-MAX (M3)** | exclusion filter | zero overlap with BASE, IC rising in 2018-25, but only identifies losers |
| 5 | **Volatility contraction (V2)** | entry timing | zero overlap, incremental t 4.1; pairs with the breakout-style entry idea |
| 6 | Residual momentum (R1) | possible crash-robust replacement for BASE | 0.90 corr with BASE — not an addition |
| 7 | Sector momentum (I1) | — | edge decays to ~0 after 2011 |
| ✗ | Frog-in-the-pan, acceleration, seasonality, up/down volume, new-high recency, Clenow slope | reject | no IC, negative IC, dead after 2018, or redundant |

## 7. Caveats
- **IC is not P&L.** A signal still has to go through a real backtest engine with costs, stops and
  sizing before it can replace BASE.
- **Survivorship bias:** the folder has no delisting calendar, so dead stocks are under-represented;
  absolute IC levels are upper bounds. The *relative* ranking between signals is the robust output.
- **Early years are thin:** 2003-2007 has 235-630 stocks; 2000-2002 is untestable (3 tickers).
- **Holdout status:** this run uses the full 2003-2025 history, so no part of it is a clean
  out-of-sample test for these particular signals any more. The three sub-periods are the stability
  evidence.
- Windows (252, 126, 50, 21 days) were set to textbook values up front and not tuned.

## 8. Suggested next step
One-variable test in the csm_quad chassis: keep universe, sizing, stops and overlays identical and
swap only the ranking signal — BASE vs A3 vs (A3 + Q5) — with Low-MAX as an optional exclusion
filter, transaction costs on.

# New strategy ideas — factors, accuracy, pros & cons

_Generated 2026-10-05 from `factor_research/` (all tables are produced by `gen_report.py` from `results/*.csv`; re-run the stage scripts to refresh)._

**Purpose.** Shortlist single factors / pairs of factors that can anchor *new* strategies, with measured predictive accuracy. Following your note, overlap with the existing momentum books is **not** treated as disqualifying — it can be reduced through universe, sizing, stops and overlays — but it is reported for every idea so you know what you are buying.

## Bottom line

* **Best factor pairs to build new strategies on** (all positive in both the ≤2014 and ≥2015 halves): (1) `tight_close_15 + q5_126` — best book Sharpe, mid/small caps; (2) `mom_resid_12_1 + q5_126` — best upgrade of existing books, ~⅓ less turnover; (3) `lowvol_126 + low_ulcer_252` — lowest drawdown, works in bear markets, low CAGR; (4) `intra_over_252 + low_ulcer_252` — most distinct signal, large caps only.
* **Event/breakout idea**: 52-week-high or Donchian breakouts only pay when gated by top-quartile relative strength + trend template; volume confirmation did not help.
* **"Volatile / high-CAGR" ideas**: selecting *for* volatility has negative IC. What moved drawdowns most was an overlay — SMA200 gate + 20% volatility target cut max drawdown from −58…−74% to −37…−41% in the stripped books at a 0-4 point CAGR cost.
* **Honest limitation**: no factor-based stock idea is uncorrelated with your momentum books (book correlation 0.6-0.9). The only genuinely decorrelated building blocks found are **asset-class rotation with gold (0.26-0.49)** and gold itself (≈ −0.15). Index timing, sector rotation and seasonality did not hold up as stand-alone strategies.

## 0. How to read the numbers

* **IC** = monthly cross-sectional Spearman rank correlation of the signal (taken at month-end close) with the forward return from the **next day's close** over *h* months (same convention as `calculate_ic` in your runners, plus a 1-day execution lag). **ICIR** = mean(IC)/std(IC) over months. **Hit** = % of months with IC>0. **t (NW)** = Newey-West t-stat (lag h−1; monthly samples of multi-month returns overlap). **Peak h** = horizon with the highest IC (the "horizon period" / factor-decay peak).
* Rule of thumb used here: |t|≥3 and the same sign in both halves (**≤2014 discovery**, **≥2015 holdout**). ~120 factors were tested, so |t|<3 is treated as noise.
* **Books** = simplified long-only top-15, equal weight, monthly rebalance, 0.3% one-way cost, **no stops / regime scaling / Crash Guard**. They exist only to compare ideas against each other and against the Elendel signal run through the *same* engine — their absolute drawdowns (−55% to −70%) are far worse than your live books because the live risk machinery is deliberately absent. "SMA200 gate" = 50% exposure (rest in 6% cash) when the equal-weight market index is below its 200-day average.
* **Universes**: Liquid-1000 = price>₹20, top-1000 by 63d median traded value, circuit ≤5/63d (~700 names avg); Top-250 = csm_absolute's universe size; Mid/small = rank 301-1000; vol terciles are within Liquid-1000.
* **Data limits**: only ~2% of stock files are delisted names (**survivorship bias** flatters long-only price signals, low-vol and smooth-trend screens in particular); index data are price indices (no dividends); ETF/index results are monthly and use ≤19 years of history, so t-stats are lower than for the ~700-stock cross-section.

## 1. Ranked summary

| Idea | Factors | ICIR 3m (best universe) | Top-15 book Sharpe plain / gated | corr→Elendel book | Verdict |
|---|---|---|---|---|---|
| **I1** Tight-range trend | tight_close_15 + q5_126 | 0.92 (mid/small) | 1.12 / 1.26 | 0.88 | **A** – best new risk-adjusted book, highest turnover |
| **I2** Residual momentum + persistence | mom_resid_12_1 + q5_126 | 0.70 (liquid) | 0.84 / 0.94 | 0.88 | **A** as an upgrade of existing books; high overlap |
| **I3** Low-risk sleeve | lowvol_126 + low_ulcer_252 | 0.47 (liquid) | 0.67 / 0.77 | 0.67 | **A** for drawdown control / diversification, low CAGR |
| **I4** Quality-intraday trend (large-cap) | intra_over_252 + low_ulcer_252 | 0.42 (top-250) | 0.74 / 0.87 | 0.84 | **B+** – most distinct signal; large-cap only |
| **I5** csm_absolute-style Sharpe momentum + overlays | csm_abs_dual_sharpe (+ gate + vol-target) | 0.69 (liquid) | 0.49 / 0.57 | 0.86 | **B** – signal is good, edge of live book is in its overlays |
| **I6** RS-gated breakout v3 | 52w-high / Donchian + RS top-25% + trend template | (event study) | – | – | **B+** – edge is the filter, not the breakout |
| **I7** Anchor-aware long high | hi_3y + low_pain_126 | 0.54 (liquid) | 0.63 / 0.73 | 0.82 | **C** – high IC, weak book (IC/return disconnect) |
| **X1** Asset-class dual momentum | Nifty/Midcap/Smallcap/Gold/cash, 3m momentum or 252d-high | N=4 → IC t≤1.8 (1-3m) | see §4.1 | see §6 | **A** for diversification (gold sleeve) |
| **X2** Factor-index regime switch | Low-Vol index vs Momentum index by market state | hit-rate based | see §4.3 | – | **B** overlay |
| **X3** VIX-spike contrarian re-entry | India VIX 2y percentile | ts-IC +0.14 (1m) | see §3.2 | – | **B** (39 spike months only) |
| **X4** Sector rotation | 19 sector indices, q5/52w-high/Sharpe | ICIR ≈0.2 | see §4.2 | ~0.7 | **C** – weak standalone |
| **X5** Breadth/trend index timing | % stocks >SMA200, SMA200, VIX, vol | bal. acc. 0.50–0.57 | see §4.4 | – | **C** as strategy / **B** as overlay |
| **S1** 1-month seasonality tilt | same-month 5y mean | IC 1m 0.024 (t 4.6) | – | – | **D** – tiny, 80% turnover |

_Priority key: A = build next; B = worthwhile with design work; C = weak/overlay only; D = skip. Sharpe is net of 0.3% one-way costs vs 6% cash._

## 2. Stock-selection ideas (single factors and factor pairs)

### I1. Tight-range trend  —  `tight_close_15` + `q5_126`

**Idea.** Buy names that trend persistently (share of last 126d above SMA50) *and* whose last 15 closes are unusually tight — a quantified "base tightness" in the spirit of VCP/Minervini, but ranked cross-sectionally rather than as a pattern-match.

* `tight_close_15` = −(std of last 15 closes / their mean). `q5_126` = fraction of last 126 days with close > SMA50 (live Elendel leg).

**Single factor `tight_close_15` (alone):**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.043 | 0.042 | 0.042 | 0.047 | 0.32 | 60.6% | 4.2 | 0.046 | 0.037 | 12 |
| Top-250 (csm_absolute universe) | 0.027 | 0.031 | 0.037 | 0.057 | 0.19 | 59.9% | 2.6 | 0.046 | 0.015 | 12 |
| Mid/small (rank 301-1000) | 0.052 | 0.044 | 0.046 | 0.037 | 0.32 | 64.5% | 4.0 | 0.048 | 0.041 | 1 |
| Top-300 | 0.028 | 0.033 | 0.037 | 0.053 | 0.21 | 60.6% | 2.8 | 0.045 | 0.019 | 12 |

Note the signal is *fast* (month-to-month rank autocorrelation only 0.26) and near-orthogonal to Elendel (corr ≈ 0.00, incremental IC +0.045): its information is short-horizon — IC 1m ≈ IC 3m ≈ 0.04 — so it works as an entry-timing/ranking add-on to a persistent trend signal rather than as a stand-alone hold.

**Pair (z-score sum):**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.071 | 0.097 | 0.115 | 0.106 | 0.71 | 79.5% | 8.4 | 0.116 | 0.077 | 6 | 0.71 | 0.044 |
| Top-250 (csm_absolute universe) | 0.051 | 0.075 | 0.097 | 0.098 | 0.41 | 71.4% | 5.0 | 0.093 | 0.056 | 12 | 0.71 | 0.033 |
| Mid/small (rank 301-1000) | 0.085 | 0.111 | 0.129 | 0.118 | 0.92 | 83.1% | 11.2 | 0.140 | 0.081 | 6 | 0.69 | 0.055 |
| Top-300 | 0.052 | 0.077 | 0.098 | 0.097 | 0.44 | 74.0% | 5.4 | 0.094 | 0.060 | 6 | 0.71 | 0.034 |

**Top-15 book vs the Elendel signal in the same engine:**

| Universe | Signal | Overlay | CAGR | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Turnover/mo | corr→Elendel book |
|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | Elendel signal (reference) | plain | 26.2% | 0.74 | -66.8% | 0.39 | 0.77 | 0.56 | 1.00 |
| Liquid-1000 | Elendel signal (reference) | SMA200 gate (50% in bear) | 26.9% | 0.80 | -55.0% | 0.49 | 0.81 | 0.56 | 1.00 |
| Liquid-1000 | this idea | plain | 29.8% | 0.95 | -57.6% | 0.52 | 0.80 | 0.68 | 0.83 |
| Liquid-1000 | this idea | SMA200 gate (50% in bear) | 29.9% | 1.04 | -44.1% | 0.68 | 0.85 | 0.68 | 0.80 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | plain | 21.9% | 0.65 | -71.5% | 0.31 | 0.66 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | SMA200 gate (50% in bear) | 22.4% | 0.70 | -60.6% | 0.37 | 0.68 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | this idea | plain | 19.4% | 0.62 | -64.1% | 0.30 | 0.41 | 0.60 | 0.89 |
| Top-250 (csm_absolute universe) | this idea | SMA200 gate (50% in bear) | 19.7% | 0.68 | -50.3% | 0.39 | 0.42 | 0.60 | 0.87 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | plain | 34.0% | 0.94 | -66.3% | 0.51 | 0.76 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | SMA200 gate (50% in bear) | 35.2% | 1.05 | -52.1% | 0.67 | 0.86 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | this idea | plain | 36.8% | 1.12 | -60.0% | 0.61 | 0.84 | 0.65 | 0.88 |
| Mid/small (rank 301-1000) | this idea | SMA200 gate (50% in bear) | 37.0% | 1.26 | -45.2% | 0.82 | 0.93 | 0.65 | 0.84 |

**Pros**

* Best risk-adjusted book of the new packs: ties persistence-alone in Liquid-1000 (Sharpe 0.95) and beats it in mid/small (1.12 vs 1.00; gated 1.26). In Liquid-1000 and mid/small it also holds up in the ≥2015 holdout (Sharpe 0.80–0.93 vs Elendel 0.76–0.86); **in the Top-250 it does not** (holdout Sharpe 0.41–0.42 vs Elendel 0.66–0.68).
* The tightness leg is genuinely distinct information (corr≈0 with Elendel) and has a natural stop location (below the base).
* Strongest IC in the mid/small universe (ICIR 0.92, t 11); 1-month IC is strong, so it also helps entry timing.

**Cons / risks**

* **Turnover 0.6–0.7 of the book per month** (vs 0.4–0.5 for persistence alone): the edge is partly eaten by costs/slippage in small names — the book numbers already include 0.3% one-way.
* Book return correlation with Elendel is still 0.83–0.89 (the persistence leg dominates). Needs universe/stop/sizing differences to be a different strategy.
* In the Top-250 universe it does *not* beat persistence alone (IC 3m 0.075 vs 0.074; Sharpe 0.62 vs 0.64) — mid/small is where it adds value.
* Tight closes in illiquid names can be an artefact of thin trading.

**Implementation notes.** Mid/small universe (rank 301-1000), monthly rank + weekly re-check of tightness; initial stop just under the 15-day low; consider requiring tightness to *persist* (two consecutive month-ends) to cut turnover.

### I2. Residual momentum + persistence  —  `mom_resid_12_1` + `q5_126`

**Idea.** Rank on the stock-specific part of 12-1 momentum (daily return minus beta × equal-weight market, summed over t−12…t−1) together with trend persistence. Strips out market-beta-driven winners.

**Single factor `mom_resid_12_1`:**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.051 | 0.073 | 0.081 | 0.065 | 0.58 | 75.7% | 6.5 | 0.091 | 0.057 | 6 |
| Top-250 (csm_absolute universe) | 0.047 | 0.066 | 0.075 | 0.067 | 0.37 | 67.2% | 4.1 | 0.084 | 0.050 | 6 |
| Mid/small (rank 301-1000) | 0.054 | 0.076 | 0.082 | 0.063 | 0.68 | 78.8% | 7.8 | 0.099 | 0.056 | 6 |
| Top-300 | 0.047 | 0.067 | 0.078 | 0.071 | 0.39 | 68.3% | 4.4 | 0.082 | 0.052 | 6 |

**Pair:**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.059 | 0.089 | 0.107 | 0.095 | 0.70 | 81.9% | 7.8 | 0.115 | 0.065 | 6 | 0.91 | 0.024 |
| Top-250 (csm_absolute universe) | 0.049 | 0.079 | 0.097 | 0.087 | 0.44 | 70.7% | 5.0 | 0.097 | 0.061 | 6 | 0.90 | 0.030 |
| Mid/small (rank 301-1000) | 0.062 | 0.095 | 0.112 | 0.100 | 0.84 | 82.6% | 9.5 | 0.128 | 0.065 | 6 | 0.90 | 0.026 |
| Top-300 | 0.050 | 0.079 | 0.099 | 0.090 | 0.47 | 72.2% | 5.2 | 0.098 | 0.062 | 6 | 0.90 | 0.028 |

**Top-15 book vs the Elendel signal in the same engine:**

| Universe | Signal | Overlay | CAGR | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Turnover/mo | corr→Elendel book |
|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | Elendel signal (reference) | plain | 26.2% | 0.74 | -66.8% | 0.39 | 0.77 | 0.56 | 1.00 |
| Liquid-1000 | Elendel signal (reference) | SMA200 gate (50% in bear) | 26.9% | 0.80 | -55.0% | 0.49 | 0.81 | 0.56 | 1.00 |
| Liquid-1000 | this idea | plain | 31.5% | 0.84 | -68.6% | 0.46 | 0.77 | 0.37 | 0.88 |
| Liquid-1000 | this idea | SMA200 gate (50% in bear) | 32.5% | 0.94 | -55.3% | 0.59 | 0.80 | 0.37 | 0.85 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | plain | 21.9% | 0.65 | -71.5% | 0.31 | 0.66 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | SMA200 gate (50% in bear) | 22.4% | 0.70 | -60.6% | 0.37 | 0.68 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | this idea | plain | 27.9% | 0.79 | -66.3% | 0.42 | 0.75 | 0.33 | 0.91 |
| Top-250 (csm_absolute universe) | this idea | SMA200 gate (50% in bear) | 27.7% | 0.87 | -53.1% | 0.52 | 0.76 | 0.33 | 0.89 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | plain | 34.0% | 0.94 | -66.3% | 0.51 | 0.76 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | SMA200 gate (50% in bear) | 35.2% | 1.05 | -52.1% | 0.67 | 0.86 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | this idea | plain | 33.4% | 0.89 | -62.1% | 0.54 | 0.67 | 0.41 | 0.90 |
| Mid/small (rank 301-1000) | this idea | SMA200 gate (50% in bear) | 34.4% | 1.00 | -48.6% | 0.71 | 0.75 | 0.41 | 0.87 |

**Pros**

* Improves on Elendel in book terms in Liquid-1000 (CAGR 31.5% vs 26.2%, Sharpe 0.84 vs 0.74) and Top-250 (27.9% vs 21.9%, Sharpe 0.80 vs 0.65), with **~34% lower turnover** (0.37 vs 0.56 in Liquid-1000); in mid/small it is roughly level (CAGR 33.4% vs 34.0%, Sharpe 0.89 vs 0.94) but has the second-best ICIR among pairs there (0.84, t 9.5) and lower turnover.
* Hit rate of IC>0 ≈ 80-83% across universes (among the highest of the candidates).

**Cons / risks**

* Correlation with the Elendel book ≈ 0.86–0.90: this is an *upgrade* to existing momentum books more than a new return stream. Residual momentum is already one of your live strategies.
* ≥2015 holdout Sharpe (0.77 liquid-1000) is no better than Elendel's (0.77): the in-sample improvement is mostly in ≤2014.
* Needs a stable beta estimate (252d); beta uses an equal-weight market proxy, not Nifty.

### I3. Low-risk sleeve  —  `lowvol_126` + `low_ulcer_252`

**Idea.** Own the calmest uptrending names: lowest 126d volatility and lowest ulcer index (RMS drawdown from trailing 252d peak). A defensive stock sleeve with very low turnover.

**Single factors:**

`lowvol_126`

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.053 | 0.062 | 0.065 | 0.077 | 0.35 | 66.2% | 4.1 | 0.062 | 0.061 | 12 |
| Top-250 (csm_absolute universe) | 0.043 | 0.061 | 0.075 | 0.104 | 0.27 | 62.2% | 3.2 | 0.075 | 0.046 | 12 |
| Mid/small (rank 301-1000) | 0.057 | 0.058 | 0.058 | 0.062 | 0.33 | 67.4% | 3.9 | 0.054 | 0.063 | 12 |
| Top-300 | 0.045 | 0.059 | 0.072 | 0.097 | 0.28 | 61.8% | 3.2 | 0.071 | 0.047 | 12 |

`low_ulcer_252`

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.064 | 0.084 | 0.096 | 0.100 | 0.48 | 77.2% | 5.5 | 0.103 | 0.066 | 12 |
| Top-250 (csm_absolute universe) | 0.057 | 0.080 | 0.097 | 0.114 | 0.35 | 69.1% | 4.0 | 0.113 | 0.050 | 12 |
| Mid/small (rank 301-1000) | 0.059 | 0.079 | 0.089 | 0.089 | 0.51 | 73.7% | 5.9 | 0.091 | 0.068 | 6 |
| Top-300 | 0.060 | 0.082 | 0.100 | 0.116 | 0.38 | 68.7% | 4.3 | 0.113 | 0.053 | 12 |

**Pair:**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.072 | 0.089 | 0.102 | 0.112 | 0.47 | 73.0% | 5.3 | 0.105 | 0.075 | 12 | 0.33 | 0.066 |
| Top-250 (csm_absolute universe) | 0.058 | 0.080 | 0.101 | 0.129 | 0.32 | 66.4% | 3.7 | 0.109 | 0.054 | 12 | 0.31 | 0.065 |
| Mid/small (rank 301-1000) | 0.071 | 0.088 | 0.097 | 0.102 | 0.52 | 71.0% | 6.0 | 0.098 | 0.080 | 12 | 0.29 | 0.067 |
| Top-300 | 0.061 | 0.082 | 0.102 | 0.130 | 0.34 | 67.2% | 3.9 | 0.109 | 0.057 | 12 | 0.30 | 0.066 |

**Top-15 book vs the Elendel signal in the same engine:**

| Universe | Signal | Overlay | CAGR | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Turnover/mo | corr→Elendel book |
|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | Elendel signal (reference) | plain | 26.2% | 0.74 | -66.8% | 0.39 | 0.77 | 0.56 | 1.00 |
| Liquid-1000 | Elendel signal (reference) | SMA200 gate (50% in bear) | 26.9% | 0.80 | -55.0% | 0.49 | 0.81 | 0.56 | 1.00 |
| Liquid-1000 | this idea | plain | 16.1% | 0.67 | -36.9% | 0.44 | 0.39 | 0.19 | 0.67 |
| Liquid-1000 | this idea | SMA200 gate (50% in bear) | 16.3% | 0.77 | -25.9% | 0.63 | 0.46 | 0.19 | 0.64 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | plain | 21.9% | 0.65 | -71.5% | 0.31 | 0.66 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | SMA200 gate (50% in bear) | 22.4% | 0.70 | -60.6% | 0.37 | 0.68 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | this idea | plain | 19.1% | 0.76 | -46.6% | 0.41 | 0.53 | 0.16 | 0.75 |
| Top-250 (csm_absolute universe) | this idea | SMA200 gate (50% in bear) | 18.9% | 0.85 | -34.7% | 0.54 | 0.60 | 0.16 | 0.73 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | plain | 34.0% | 0.94 | -66.3% | 0.51 | 0.76 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | SMA200 gate (50% in bear) | 35.2% | 1.05 | -52.1% | 0.67 | 0.86 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | this idea | plain | 16.1% | 0.61 | -52.6% | 0.31 | 0.53 | 0.24 | 0.75 |
| Mid/small (rank 301-1000) | this idea | SMA200 gate (50% in bear) | 17.2% | 0.77 | -38.2% | 0.45 | 0.68 | 0.24 | 0.71 |

**Pros**

* **Lowest drawdown of any stock idea**: Liquid-1000 plain −37% (vs −67% Elendel); with the SMA200 gate −26%; max DD since 2015 only −16% to −23% in Liquid-1000/Top-250/Top-300 (−33% plain, −16% gated in mid/small).
* Turnover 0.16-0.24 of the book per month (rank autocorrelation 0.95-0.99) → cheap to run.
* Works in every universe and keeps positive IC in bear months (IC 3m ≈ +0.07 to +0.08 in market-below-SMA200 months). Orthogonal to Elendel at factor level (lowvol corr −0.02, incremental IC +0.065).
* Low-vol factor *index* beats the Nifty 500 by ~1.6%/month in drawdowns >10% (§4.3), corroborating the regime behaviour.

**Cons / risks**

* **CAGR only 16-19%** and Sharpe ≈0.6–0.9: rank IC is high but the top-quintile *mean* excess is negative (the edge is win-rate/risk, not return) — IC overstates its value for a return-seeking book.
* Weakest holdout (Sharpe ≥2015 0.39–0.68): low-vol lagged during the 2015-2024 small/mid-cap momentum run.
* Book correlation to Elendel still 0.64–0.75; to Nifty 500 0.76 (it is long equity).
* Survivorship bias flatters low-vol screens the most (delisted names were usually volatile).

### I4. Quality-intraday trend (large caps)  —  `intra_over_252` + `low_ulcer_252`

**Idea.** `intra_over_252` = Σ(log close/open) − Σ(log open/prev close) over 252d, daily legs clipped ±15%: stocks whose trend is built **during the session** rather than by overnight gaps. Overnight drift is a *negative* predictor (t −3.2 to −5.1), intraday drift positive. Paired with low ulcer index for smoothness.

**Single factor `intra_over_252`:**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.044 | 0.060 | 0.068 | 0.071 | 0.48 | 73.0% | 5.4 | 0.066 | 0.054 | 12 |
| Top-250 (csm_absolute universe) | 0.051 | 0.080 | 0.094 | 0.105 | 0.48 | 71.1% | 5.5 | 0.091 | 0.070 | 12 |
| Mid/small (rank 301-1000) | 0.040 | 0.056 | 0.065 | 0.069 | 0.55 | 71.4% | 6.5 | 0.062 | 0.050 | 12 |
| Top-300 | 0.050 | 0.074 | 0.090 | 0.101 | 0.46 | 70.0% | 5.4 | 0.081 | 0.068 | 12 |

**Pair:**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.065 | 0.086 | 0.099 | 0.105 | 0.52 | 75.7% | 5.8 | 0.104 | 0.069 | 12 | 0.48 | 0.054 |
| Top-250 (csm_absolute universe) | 0.063 | 0.092 | 0.112 | 0.129 | 0.42 | 71.0% | 4.8 | 0.119 | 0.068 | 12 | 0.50 | 0.070 |
| Mid/small (rank 301-1000) | 0.061 | 0.083 | 0.095 | 0.098 | 0.60 | 74.9% | 6.9 | 0.096 | 0.071 | 12 | 0.46 | 0.049 |
| Top-300 | 0.064 | 0.090 | 0.111 | 0.128 | 0.43 | 73.4% | 4.9 | 0.114 | 0.068 | 12 | 0.50 | 0.067 |

**Top-15 book vs the Elendel signal in the same engine:**

| Universe | Signal | Overlay | CAGR | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Turnover/mo | corr→Elendel book |
|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | Elendel signal (reference) | plain | 26.2% | 0.74 | -66.8% | 0.39 | 0.77 | 0.56 | 1.00 |
| Liquid-1000 | Elendel signal (reference) | SMA200 gate (50% in bear) | 26.9% | 0.80 | -55.0% | 0.49 | 0.81 | 0.56 | 1.00 |
| Liquid-1000 | this idea | plain | 15.7% | 0.48 | -68.2% | 0.23 | 0.25 | 0.22 | 0.77 |
| Liquid-1000 | this idea | SMA200 gate (50% in bear) | 17.5% | 0.61 | -52.9% | 0.33 | 0.35 | 0.22 | 0.77 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | plain | 21.9% | 0.65 | -71.5% | 0.31 | 0.66 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | SMA200 gate (50% in bear) | 22.4% | 0.70 | -60.6% | 0.37 | 0.68 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | this idea | plain | 21.7% | 0.74 | -57.8% | 0.38 | 0.60 | 0.21 | 0.84 |
| Top-250 (csm_absolute universe) | this idea | SMA200 gate (50% in bear) | 22.6% | 0.87 | -41.8% | 0.54 | 0.68 | 0.21 | 0.82 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | plain | 34.0% | 0.94 | -66.3% | 0.51 | 0.76 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | SMA200 gate (50% in bear) | 35.2% | 1.05 | -52.1% | 0.67 | 0.86 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | this idea | plain | 15.8% | 0.47 | -69.9% | 0.23 | 0.18 | 0.26 | 0.78 |
| Mid/small (rank 301-1000) | this idea | SMA200 gate (50% in bear) | 18.1% | 0.61 | -54.9% | 0.33 | 0.31 | 0.26 | 0.77 |

**Pros**

* The most *distinct* positive-IC signal found (corr→Elendel 0.31 single / 0.46–0.50 pair) and **strongest in large caps** (IC 3m 0.080 in Top-250, t 5.4 in Top-300) where plain momentum is weakest (IC 3m 0.044 for 12-1 in Top-250).
* Low turnover (0.22) and decent Top-250/Top-300 books: Sharpe 0.74-0.75 plain, 0.86-0.87 gated, max DD gated −42%.

**Cons / risks**

* **Weak in mid/small caps** (Sharpe 0.47-0.61; IC 3m 0.083 but poor book) — keep to the top ~300.
* Depends on the quality of the **open** print (NSE call-auction opening, un-adjusted corporate actions). Daily legs are clipped at ±15%, but the signal should be re-validated on a second data source before going live.
* Mechanism is a behavioural/microstructure story (gap-chasing reverses); less proven than momentum and may be crowded/decay with regime.

### I5. csm_absolute-style Sharpe momentum with risk overlays  —  `csm_abs_dual_sharpe` (+ SMA200 gate + volatility target)

**Idea.** Your live `csm_absolute` ranks on a dual-window (9m & 4m, lag 1m) return / monthly-volatility score from the top-250 liquid names, 15 positions. This section measures (a) how accurate that score is, and (b) what the "volatile but low-drawdown" behaviour is actually built from.

**Signal accuracy (exact csm_absolute formula, clipped ±5):**

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h (m) |
|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.052 | 0.080 | 0.096 | 0.079 | 0.69 | 76.6% | 8.0 | 0.101 | 0.059 | 6 |
| Top-250 (csm_absolute universe) | 0.039 | 0.067 | 0.081 | 0.069 | 0.42 | 67.3% | 4.9 | 0.086 | 0.049 | 6 |
| Mid/small (rank 301-1000) | 0.056 | 0.087 | 0.104 | 0.088 | 0.81 | 79.6% | 9.8 | 0.113 | 0.060 | 6 |
| Top-300 | 0.040 | 0.068 | 0.084 | 0.073 | 0.44 | 70.6% | 5.2 | 0.085 | 0.052 | 6 |

**Where it works** (IC 3m by universe, for context):

| Factor (IC 3m) | Top-250 | Liquid-1000 | Mid/small | High-vol tercile | Low-vol tercile |
|---|---|---|---|---|---|
| csm_abs_dual_sharpe | 0.067 | 0.080 | 0.087 | 0.073 | 0.088 |
| q5_126 | 0.074 | 0.085 | 0.098 | 0.078 | 0.098 |
| LIVE_elendel(A3+Q5_126) | 0.080 | 0.095 | 0.101 | 0.081 | 0.103 |
| mom_12_1 | 0.044 | 0.065 | 0.079 | 0.059 | 0.084 |
| low_pain_126 | 0.092 | 0.096 | 0.094 | 0.075 | 0.078 |
| hi_3y | 0.083 | 0.093 | 0.094 | 0.074 | 0.079 |
| intra_over_252 | 0.080 | 0.060 | 0.056 | 0.053 | 0.046 |

**Finding 1 — the *signal* is accurate but not special:** ICIR 0.69 (t 8.0, hit 77%) is among the highest of any single stock factor (only `q5_126` is marginally higher at 0.70), yet its stripped top-15 book (CAGR 17%, Sharpe 0.49 in Liquid-1000; 21%/0.63 in Top-250, roughly level with Elendel there) is clearly behind the Elendel signal in Liquid-1000 and mid/small. I cannot reproduce the live engine here, so I cannot attribute its high-CAGR / low-DD profile; what the tests do show is that the ranking alone does not produce it and that the drawdown profile moves a lot with overlays (Finding 2).

**Finding 2 — risk overlays do the heavy lifting.** Same top-15 books, Liquid-1000, with an SMA200 market gate (50% in bear), a 20% volatility target (exposure = min(1, 20%/trailing-6m book vol)), and both:

| Signal (top-15) | Overlay | CAGR | Vol | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Max DD ≥2015 |
|---|---|---|---|---|---|---|---|---|
| Elendel signal | plain | 26.2% | 30.3% | 0.74 | -66.8% | 0.39 | 0.77 | -40.4% |
| Elendel signal | sma200_gate50 | 26.9% | 27.4% | 0.80 | -55.0% | 0.49 | 0.81 | -36.8% |
| Elendel signal | voltarget20 | 21.6% | 24.2% | 0.70 | -44.4% | 0.49 | 0.65 | -37.4% |
| Elendel signal | gate+voltarget | 22.9% | 22.6% | 0.78 | -41.4% | 0.55 | 0.76 | -30.9% |
| P4 residual+persistence | plain | 31.5% | 32.2% | 0.84 | -68.6% | 0.46 | 0.77 | -47.9% |
| P4 residual+persistence | sma200_gate50 | 32.5% | 28.3% | 0.94 | -55.3% | 0.59 | 0.80 | -36.0% |
| P4 residual+persistence | voltarget20 | 27.2% | 24.3% | 0.88 | -44.6% | 0.61 | 0.71 | -44.6% |
| P4 residual+persistence | gate+voltarget | 28.0% | 22.2% | 0.97 | -36.7% | 0.76 | 0.83 | -25.8% |
| P6 tight-range trend | plain | 29.8% | 24.8% | 0.95 | -57.6% | 0.52 | 0.80 | -25.3% |
| P6 tight-range trend | sma200_gate50 | 29.9% | 22.2% | 1.04 | -44.1% | 0.68 | 0.85 | -24.2% |
| P6 tight-range trend | voltarget20 | 26.9% | 21.4% | 0.96 | -40.7% | 0.66 | 0.76 | -21.9% |
| P6 tight-range trend | gate+voltarget | 26.6% | 19.8% | 1.01 | -37.4% | 0.71 | 0.81 | -23.2% |
| csm_absolute score | plain | 17.1% | 30.0% | 0.49 | -73.7% | 0.23 | 0.25 | -49.2% |
| csm_absolute score | sma200_gate50 | 19.1% | 26.9% | 0.57 | -59.9% | 0.32 | 0.28 | -32.2% |
| csm_absolute score | voltarget20 | 15.7% | 23.1% | 0.50 | -40.8% | 0.39 | 0.21 | -40.8% |
| csm_absolute score | gate+voltarget | 16.4% | 21.8% | 0.54 | -40.1% | 0.41 | 0.28 | -26.8% |
| P2 low-risk sleeve | plain | 16.1% | 15.6% | 0.67 | -36.9% | 0.44 | 0.39 | -22.9% |
| P2 low-risk sleeve | sma200_gate50 | 16.3% | 13.3% | 0.77 | -25.9% | 0.63 | 0.46 | -16.6% |
| P2 low-risk sleeve | voltarget20 | 16.3% | 14.9% | 0.70 | -28.7% | 0.57 | 0.38 | -22.9% |
| P2 low-risk sleeve | gate+voltarget | 16.3% | 13.2% | 0.77 | -24.1% | 0.67 | 0.44 | -16.4% |

Gate + vol-target takes max drawdown for the four momentum-type books from −58%…−74% **down to −37%…−41%** (low-risk sleeve −37% → −24%), always with higher Sharpe and a 0-4 point CAGR give-up (P4: 31.5% → 28.0% CAGR, Sharpe 0.84 → 0.97, DD −69% → −37%).

**Finding 3 — concentration is not where the return is:** (CAGR / Max DD / Sharpe, Liquid-1000, P4 signal)

| Overlay | Top-8 | Top-10 | Top-15 | Top-25 |
|---|---|---|---|---|
| plain | 29.9% / -66% / 0.75 | 28.4% / -70% / 0.73 | 31.5% / -69% / 0.84 | 31.3% / -64% / 0.87 |
| gate+voltarget | 25.8% / -31% / 0.87 | 24.6% / -34% / 0.83 | 28.0% / -37% / 0.97 | 28.2% / -30% / 1.01 |

Top-8 to top-25 produce similar CAGR (≈28-32%); top-25 has the best Sharpe. Going to 8-10 names adds variance, not return, for these signals.

**Finding 4 — "volatility-seeking" is the *wrong* direction:** the high-volatility factor has **negative** IC (`hvol_126` IC 3m −0.062, t −4.1, hit 34%); momentum inside the high-vol tercile still works (IC 3m ≈0.055-0.08) but sorting *for* volatility loses. ATR-expansion (IC 0.005), up-range-expansion days (0.003), jump frequency (−0.013) and a regime-switched beta (long high-beta in bull, low-beta in bear: IC −0.021) carry no usable signal.

**Pros** — exact live-signal accuracy is now measured; overlays are portable to every book; shows what to keep (gate + vol-target) when building volatile, high-CAGR books.

**Cons** — the stripped books cannot reproduce the live engine; a proper test needs the full event-driven loop (stops, crash guard, take-profit). Gate/vol-target parameters (SMA200, 50%, 20%, 6m) were fixed in advance, not tuned, but are only one choice.

### I6. RS-gated breakout v3  —  52-week-high / Donchian breakout + RS rank + trend template

**Idea.** Event-driven entry on daily breakouts, but only for names that already have top-quartile 6-month relative strength and pass the Stage-2 trend template (C>SMA50>SMA150>SMA200, SMA200 rising, within 25% of 52w high, >30% above 52w low). Entry T+1 close; excess = forward return minus the same-day liquid-universe mean.

| Event | N | Excess 20d | Excess 60d | t 20d | t 60d | % beating universe 20d | % beating universe 60d | Excess 60d ≤2014 | Excess 60d ≥2015 |
|---|---|---|---|---|---|---|---|---|---|
| 52w closing-high breakout (all) | 33289 | 0.6% | 1.8% | 3.9 | 4.9 | 45.9% | 47.0% | 2.2% | 1.5% |
| … + RS top-25% | 13536 | 1.1% | 2.9% | 4.8 | 5.6 | 47.8% | 49.2% | 4.1% | 2.0% |
| … + trend template + vol≥1.5x + RS top-25% | 7694 | 1.0% | 2.6% | 4.1 | 4.6 | 46.2% | 48.4% | 4.4% | 1.6% |
| … + compressed base (VCP-like) | 3266 | 0.8% | 2.5% | 2.6 | 5.1 | 47.7% | 48.6% | 2.9% | 2.1% |
| Donchian-55 breakout (all) | 50763 | -0.2% | 0.6% | -0.1 | 1.6 | 42.9% | 44.1% | 0.4% | 0.7% |
| … + RS top-25% | 14446 | 0.9% | 2.6% | 3.7 | 4.4 | 46.9% | 48.5% | 3.3% | 2.1% |
| … + trend template + vol≥1.5x + RS top-25% | 8400 | 1.0% | 2.7% | 3.8 | 4.4 | 46.5% | 48.2% | 4.3% | 1.8% |

**Pros**

* The filter turns a flat signal into a significant one: Donchian-55 alone is +0.6% at 60d (t 1.6); with RS top-25% it is +2.6% (t 4.4); 52w-high with RS top-25%: +2.9% (t 5.6). Positive in both halves.
* Clean, rule-based entries with natural stop levels; fits the existing HR/VCP event-driven chassis.

**Cons / risks**

* **Hit rate vs universe is under 50% (43-49%)** and median 20d excess is negative: the average comes from a fat right tail, so a breakout book needs payoff asymmetry (tight stops, let winners run) and tolerance for many small losses.
* The edge is momentum/RS in disguise, so correlation to momentum books will be high unless exits/sizing differ.
* **Volume confirmation did not help** (52w-high on <1.5× volume: 20d +0.9% vs +0.45% on ≥1.5×; Donchian-55 on ≥1.5× volume is negative at 20d) — contrary to the usual rule; consider dropping the volume gate in HR/VCP.
* Holdout (≥2015) edge is roughly one-half to two-thirds of the ≤2014 edge.

### I7. Anchor-aware long high  —  `hi_3y` + `low_pain_126`

**Idea.** Proximity to the 756-day high (long-horizon anchoring) combined with low average drawdown pain. Highest IC among the pairs, but a **cautionary example**:

| Universe | IC 1m | IC 3m | IC 6m | IC 12m | ICIR 3m | Hit 3m | t (NW) | IC ≤2014 | IC ≥2015 | Peak h | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | 0.071 | 0.103 | 0.123 | 0.120 | 0.54 | 77.6% | 6.0 | 0.135 | 0.076 | 6 | 0.79 | 0.068 |
| Top-250 (csm_absolute universe) | 0.060 | 0.093 | 0.119 | 0.128 | 0.39 | 70.4% | 4.3 | 0.136 | 0.056 | 12 | 0.79 | 0.067 |
| Mid/small (rank 301-1000) | 0.071 | 0.107 | 0.126 | 0.119 | 0.65 | 81.2% | 7.3 | 0.135 | 0.083 | 6 | 0.78 | 0.071 |
| Top-300 | 0.062 | 0.095 | 0.122 | 0.130 | 0.41 | 73.2% | 4.6 | 0.136 | 0.060 | 12 | 0.79 | 0.068 |

**Top-15 book vs the Elendel signal in the same engine:**

| Universe | Signal | Overlay | CAGR | Sharpe | Max DD | Calmar | Sharpe ≥2015 | Turnover/mo | corr→Elendel book |
|---|---|---|---|---|---|---|---|---|---|
| Liquid-1000 | Elendel signal (reference) | plain | 26.2% | 0.74 | -66.8% | 0.39 | 0.77 | 0.56 | 1.00 |
| Liquid-1000 | Elendel signal (reference) | SMA200 gate (50% in bear) | 26.9% | 0.80 | -55.0% | 0.49 | 0.81 | 0.56 | 1.00 |
| Liquid-1000 | this idea | plain | 17.8% | 0.63 | -51.1% | 0.35 | 0.26 | 0.49 | 0.82 |
| Liquid-1000 | this idea | SMA200 gate (50% in bear) | 18.6% | 0.73 | -39.7% | 0.47 | 0.32 | 0.49 | 0.80 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | plain | 21.9% | 0.65 | -71.5% | 0.31 | 0.66 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | Elendel signal (reference) | SMA200 gate (50% in bear) | 22.4% | 0.70 | -60.6% | 0.37 | 0.68 | 0.44 | 1.00 |
| Top-250 (csm_absolute universe) | this idea | plain | 13.4% | 0.43 | -58.4% | 0.23 | 0.21 | 0.42 | 0.87 |
| Top-250 (csm_absolute universe) | this idea | SMA200 gate (50% in bear) | 14.2% | 0.50 | -47.3% | 0.30 | 0.25 | 0.42 | 0.86 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | plain | 34.0% | 0.94 | -66.3% | 0.51 | 0.76 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | Elendel signal (reference) | SMA200 gate (50% in bear) | 35.2% | 1.05 | -52.1% | 0.67 | 0.86 | 0.51 | 1.00 |
| Mid/small (rank 301-1000) | this idea | plain | 21.9% | 0.74 | -60.9% | 0.36 | 0.48 | 0.47 | 0.86 |
| Mid/small (rank 301-1000) | this idea | SMA200 gate (50% in bear) | 23.6% | 0.89 | -46.3% | 0.51 | 0.61 | 0.47 | 0.83 |

**Pros** — high IC (ICIR 0.39-0.65, hit 70-81%, IC 12m 0.12-0.13), moderate drawdowns (gated −40% to −47%). **Cons** — **the IC does not translate into returns**: CAGR 13-24% and Sharpe 0.43-0.89. The signal ranks the whole cross-section well by selecting low-risk names, whose absolute returns are modest. Treat as a risk/quality filter on other ideas, not a standalone book.

### S1. One-month seasonality tilt (rejected as a strategy)

`season_same_month_5y` (mean return of the upcoming calendar month over the previous 5 years): IC 1m = 0.024, ICIR 0.30, hit 61%, t 4.6 — real but **dies after one month** (IC 3m 0.005, t 0.9), has ~0 correlation with everything else, and composites containing it ran at 75-85% monthly turnover. Adding it to Elendel/Zenith (weight 0.5) lowered book Sharpe. Quarterly (earnings-cycle) and 3y/8y variants are weaker (IC 1m 0.022-0.025, IC 3m ≤0.014). Skip, or use only as a tie-breaker.

## 3. Volatility- and regime-based ideas (risk management as strategy)

### 3.1 Trend gate + volatility target (see I5, Finding 2)

Both overlays use only month-end information. Combined, they reduced max drawdown by 20-34 points in the four momentum-type books (13 points in the low-risk sleeve) and are the most robust "improvement per unit of complexity" found in this study. Caveat: they were evaluated on stripped books — the live books already contain some of this (regime leverage, Crash Guard), so the *marginal* benefit has to be re-measured in the live engine.

### 3.2 India VIX spike as a contrarian re-entry / risk-on signal

When India VIX is in the **top 20% of its trailing 2-year range**, the next 1-3 months have been unusually good for Indian equities (2010-2026, 39 month-ends in the top quintile):

| Index | Horizon | Time-series IC (rank) | Mean fwd return, VIX top-20% | Mean fwd return, rest | P(up), VIX top-20% | P(up), rest |
|---|---|---|---|---|---|---|
| Nifty 50 | 1m | 0.140 | 2.6% | 0.5% | 71.8% | 54.2% |
| Nifty 50 | 3m | 0.068 | 5.0% | 2.1% | 71.8% | 63.4% |
| Nifty 500 | 1m | 0.140 | 2.9% | 0.5% | 76.9% | 56.8% |
| Nifty 500 | 3m | 0.075 | 5.5% | 2.3% | 74.4% | 62.1% |
| Midcap 100 | 1m | 0.116 | 3.4% | 0.7% | 82.0% | 60.7% |
| Midcap 100 | 3m | 0.068 | 6.5% | 3.1% | 71.8% | 60.8% |
| Smallcap 100 | 1m | 0.157 | 4.3% | 0.4% | 76.9% | 56.1% |
| Smallcap 100 | 3m | 0.122 | 8.4% | 2.2% | 69.2% | 58.2% |

**Pros** — simple, uses a data series you already hold, opposite in sign to a naive "low VIX = safe" rule (the *low-VIX* gate has negative IC −0.12 and loses money as a timer); P(up) is 18-22 points higher at 1m in every index (8-14 points at 3m). Natural fit for **post-Crash-Guard re-entry** and for leaning into drawdowns.

**Cons** — only 39 high-VIX months (clustered around 2011, 2013, 2015-16, 2020, 2022); monthly-IC t-stat is ≈2; VIX is available from 2009 only; the 3m IC is small (0.07-0.12) so the value is in the *tail* months, not in a continuous signal.

## 4. Index & ETF ideas

Data: 208 index series (broad, sector, factor, G-Sec, VIX, 2× leveraged/inverse) back to 2000-2005; ~140 ETFs with >1,000 days (NIFTYBEES 2002, LIQUIDBEES/GOLDBEES 2007, silver 2022+, Nasdaq/Hang Seng/sector ETFs 2010-2022+). Monthly signal, T+1 fill, 0.1% one-way cost, cash = LIQUIDBEES (6% before 2007).

### 4.1 X1 Asset-class dual momentum (Nifty 50 / Midcap 100 / Smallcap 100 / Gold / cash)

Rank the four assets monthly on a momentum/trend score, hold the top 1 or 2; optional absolute filter (12m return must beat cash, otherwise LIQUIDBEES). Window 2008-04 → 2026-07 (limited by GOLDBEES).

| Score | Top-k | Abs. filter | CAGR | Vol | Sharpe | Max DD | Calmar | Sharpe ≤2014 | Sharpe ≥2015 | Turnover | % months > cash |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hi_252 | 1 | none | 16.1% | 17.1% | 0.62 | -20.4% | 0.79 | 0.37 | 0.82 | 0.83 | 59.7% |
| mom_3_0 | 1 | none | 18.8% | 21.0% | 0.65 | -25.3% | 0.74 | 0.56 | 0.73 | 0.73 | 58.4% |
| mom_6_1 | 1 | abs>cash | 14.3% | 19.7% | 0.49 | -46.2% | 0.31 | 0.48 | 0.49 | 0.53 | 54.8% |
| mom_12_1 | 2 | none | 14.1% | 17.7% | 0.51 | -29.0% | 0.49 | 0.48 | 0.54 | 0.27 | 60.2% |
| q5_126 | 2 | none | 15.6% | 18.4% | 0.56 | -26.5% | 0.59 | 0.56 | 0.58 | 0.29 | 58.8% |
| q5_126 | 1 | none | 14.7% | 18.7% | 0.52 | -30.9% | 0.47 | 0.56 | 0.49 | 0.38 | 56.6% |

Reference (same window, buy & hold): Nifty 50 CAGR 9.2% / DD −49%; Midcap 100 13.5% / −56%; Smallcap 100 9.6% / −66%; **Gold 13.3% / −17% (Sharpe 0.53)**; equal-weight of the four 12.6% / −43%.

**Cross-asset IC (N=4 assets per month, ~160 months):**

| Factor | IC 1m | Hit 1m | t 1m | IC 3m | Hit 3m | t 3m | IC 6m | Hit 6m | t 6m |
|---|---|---|---|---|---|---|---|---|---|
| dist_sma200 | 0.068 | 51.8% | 1.3 | 0.129 | 56.1% | 1.8 | 0.195 | 62.7% | 1.9 |
| hi_252 | 0.009 | 47.6% | 0.2 | 0.122 | 58.6% | 1.8 | 0.158 | 60.4% | 1.8 |
| mom_3_0 | 0.019 | 48.8% | 0.4 | 0.113 | 56.0% | 1.7 | 0.170 | 61.2% | 2.0 |
| mom_6_1 | 0.075 | 52.4% | 1.4 | 0.086 | 53.0% | 1.2 | 0.203 | 60.7% | 2.1 |
| sharpe_6_1 | 0.073 | 55.4% | 1.4 | 0.082 | 53.0% | 1.2 | 0.220 | 62.6% | 2.4 |
| mom_6_0 | 0.047 | 49.1% | 0.9 | 0.078 | 53.3% | 1.1 | 0.174 | 59.9% | 1.7 |

**Pros** — **genuinely different return stream**: monthly return correlation with the stock books is only 0.26-0.49 for the 252d-high / 3m-momentum rotations and **−0.12 to −0.19 for gold** (§6); best configurations reach 16-19% CAGR with max DD ≈ −20% to −25% (Calmar 0.7-0.8); ETF-implementable (NIFTYBEES/JUNIORBEES/GOLDBEES/LIQUIDBEES + mid/small ETFs from 2019/2023).

**Cons** — **those two were the best of 24 configurations tried (6 scores × top-1/2 × with/without absolute filter); the median configuration returned 13.1% CAGR, Sharpe 0.46, max DD −29%** (equal-weight 4 assets: 12.6%, 0.42, −43%), so most of the value is diversification, not selection skill. **Cross-asset IC is weak statistically** (|t| ≤ 1.8 at 1-3m; up to 2.4 at 6m, with N=4 assets and overlapping returns); hit rates are only 50-58%; results are flattered by gold's 2019-2026 run and by a short window (18 years) with few regime changes; Smallcap/Midcap index ETFs with real liquidity only exist since 2019-2024 (index returns are not what you would have captured earlier); price indices omit dividends.

### 4.2 X4 Sector-index rotation (19 sectors/themes, 2004-2026)

| Factor | IC 1m | ICIR 1m | Hit 1m | IC 3m | ICIR 3m | Hit 3m | t 3m | IC 6m | t 6m | IC ≤2014 | IC ≥2015 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| rs_near_high | 0.078 | 0.21 | 59.5% | 0.084 | 0.23 | 61.2% | 2.8 | 0.118 | 2.8 | 0.122 | 0.051 |
| sharpe_6_1 | 0.061 | 0.18 | 57.7% | 0.076 | 0.23 | 59.3% | 3.0 | 0.115 | 3.2 | 0.104 | 0.051 |
| low_ulcer_126 | 0.062 | 0.16 | 59.5% | 0.087 | 0.23 | 58.9% | 2.7 | 0.127 | 2.8 | 0.132 | 0.046 |
| q5_126 | 0.072 | 0.21 | 61.9% | 0.075 | 0.22 | 58.2% | 2.6 | 0.121 | 3.2 | 0.106 | 0.046 |
| hi_252 | 0.062 | 0.15 | 62.6% | 0.070 | 0.19 | 60.4% | 2.3 | 0.110 | 2.6 | 0.130 | 0.015 |
| dist_sma200 | 0.088 | 0.22 | 61.4% | 0.071 | 0.18 | 57.6% | 2.3 | 0.097 | 2.5 | 0.100 | 0.044 |

Top-3 sector books (EW sectors: CAGR 12.9%, DD −58%; Nifty 500: 12.7%, −62%):

| Score | CAGR | Vol | Sharpe | Max DD | Sharpe ≥2015 | Turnover |
|---|---|---|---|---|---|---|
| lowvol_126 | 14.4% | 17.9% | 0.52 | -41.0% | 0.28 | 0.27 |
| low_ulcer_126 | 14.9% | 20.1% | 0.51 | -52.0% | 0.26 | 0.40 |
| q5_126 | 14.8% | 22.4% | 0.47 | -53.9% | 0.23 | 0.51 |
| mom_3_0 | 14.2% | 24.8% | 0.43 | -52.7% | 0.40 | 0.95 |

**Pros** — consistent sign: trend-persistence/52w-high/Sharpe scores have positive IC at every horizon, strongest at 6m (IC ≈ 0.11-0.13, hit 63-65%); low-ulcer top-3 gives CAGR 14.9% at DD −52%. **Cons** — **ICIR ≈ 0.2, holdout IC halves (≥2015 ≈ 0.05)**; books barely beat the Nifty 500 and still draw down ~50%; sectors overlap (Bank / Pvt Bank / Fin Services); sector ETFs exist only from 2020-2022 for most themes. Better as a conditioning input (the stock-level sector factors in §5 add little) than as its own strategy. **Verdict: C.**

### 4.3 X2 Factor-index regime switch (Low-Vol vs Momentum/Alpha indices)

Mean monthly excess return vs Nifty 500 (and % of months beating it), by regime known at month-end:

| Factor index | All | Bull (>SMA200) | Bear | VIX>median | Mkt DD>10% |
|---|---|---|---|---|---|
| LowVol30(N100) | +0.23% (53%) | +0.04% (53%) | +0.72% (51%) | +0.36% (50%) | +1.61% (59%) |
| Momentum30(N200) | +0.37% (57%) | +0.48% (59%) | +0.09% (53%) | +0.05% (53%) | -0.33% (52%) |
| Alpha50 | +0.63% (60%) | +0.79% (61%) | +0.23% (57%) | +0.53% (58%) | -0.23% (55%) |
| Midcap150Mom50 | +0.69% (60%) | +1.02% (64%) | -0.15% (51%) | +0.46% (54%) | -0.45% (48%) |
| Quality30(N200) | +0.12% (51%) | +0.14% (50%) | +0.09% (53%) | -0.04% (54%) | +0.07% (53%) |
| Value20(N50) | +0.06% (50%) | +0.19% (53%) | -0.26% (45%) | -0.10% (49%) | -0.78% (42%) |

**Pros** — the Low-Vol index is the only factor index that **gains** when the market is in drawdown (+1.6%/month, 59% hit when the Nifty 500 is >10% off its 1y high; +0.7%/month in bear regimes) while Momentum/Alpha indices lose in those states (−0.2% to −0.5%/month) → a simple state-dependent switch between the momentum books and a low-vol sleeve (I3). **Cons** — differences are small per month (≤1.6%), hit rates only 51-59%, factor indices start 2003-2009 (NIFTY100 Quality 2009, Value 20 2009) and several factor ETFs/indices are very recent (HighBeta/LowVol 50 from 2024); not significant as standalone strategies.

### 4.4 X5 Equity-index timing (trend, breadth, VIX, volatility)

| Asset | Signal (ON = invested, else cash) | % months ON | Balanced accuracy | CAGR | Buy&hold CAGR | Max DD | B&H Max DD | Sharpe | B&H Sharpe | Sharpe ≥2015 |
|---|---|---|---|---|---|---|---|---|---|---|
| Nifty 500 | sma200 | 69.4% | 0.50 | 11.0% | 13.3% | -29.2% | -62.0% | 0.35 | 0.40 | 0.04 |
| Nifty 500 | breadth200_gt50 | 54.4% | 0.54 | 9.5% | 13.3% | -26.5% | -62.0% | 0.30 | 0.40 | 0.04 |
| Nifty 500 | vote_sma200_breadth | 52.4% | 0.54 | 9.4% | 13.3% | -26.5% | -62.0% | 0.29 | 0.40 | 0.08 |
| Midcap 100 | sma200 | 71.9% | 0.54 | 13.2% | 19.2% | -41.5% | -66.9% | 0.44 | 0.58 | 0.16 |
| Midcap 100 | breadth200_gt50 | 56.6% | 0.54 | 12.7% | 19.2% | -26.4% | -66.9% | 0.45 | 0.58 | 0.27 |
| Midcap 100 | vote_sma200_breadth | 56.3% | 0.54 | 13.0% | 19.2% | -26.4% | -66.9% | 0.46 | 0.58 | 0.31 |
| Smallcap 100 | sma200 | 65.0% | 0.51 | 12.3% | 13.2% | -39.6% | -75.9% | 0.39 | 0.37 | 0.21 |
| Smallcap 100 | breadth200_gt50 | 59.2% | 0.53 | 11.9% | 13.2% | -31.8% | -75.9% | 0.38 | 0.37 | 0.19 |
| Smallcap 100 | vote_sma200_breadth | 56.1% | 0.53 | 12.8% | 13.2% | -30.8% | -75.9% | 0.43 | 0.37 | 0.29 |

Breadth = % of liquid stocks above their own SMA200 (computed from the stock panel). Balanced accuracy = mean of P(ON → asset beats cash) and P(OFF → asset loses to cash).

**Pros** — halves the index drawdown (−56%→−23% for Nifty 50 with breadth; Midcap −67%→−26%); breadth200 (alone or combined with SMA200) gave the largest drawdown cut for the smallest CAGR loss among the nine signals tried. **Cons** — accuracy is **barely above a coin flip (0.50-0.57)**, time-series ICs are ≈0, and timed CAGR is **below buy-and-hold** (e.g. Nifty 500 9.5% vs 13.3%; Midcap 12.7% vs 19.2%) because cash earns 6% and misses sharp recoveries. Valid only as a **drawdown overlay** for the stock books (§3.1), not as a strategy. A 2× leveraged Nifty TR index with the same gates did not help either (best: CAGR 9.2% vs 13.2% buy-and-hold, DD −35% vs −58%).

## 5. Sector information as a *stock-level* factor (tested, low value)

No sector map exists in the data, so each stock was assigned (point-in-time) to the sector index with the highest trailing-252d correlation of market-residual returns (only ~24% of stock-months clear a 0.10 correlation bar). On the **same assigned subset**:

| Universe | Factor | IC 3m | ICIR 3m | Hit 3m | t | corr→Elendel | incr. IC 3m |
|---|---|---|---|---|---|---|---|
| Liquid-1000 (assigned stocks) | mom_6_1 | 0.061 | 0.42 | 71.5% | 5.0 | 0.80 | -0.016 |
| Liquid-1000 (assigned stocks) | mom_12_1 | 0.064 | 0.40 | 72.7% | 4.6 | 0.74 | 0.005 |
| Liquid-1000 (assigned stocks) | q5_126 | 0.087 | 0.65 | 78.1% | 7.4 | 0.92 | 0.001 |
| Liquid-1000 (assigned stocks) | stock_vs_sector_6_1 | 0.054 | 0.56 | 75.9% | 6.7 | 0.68 | -0.011 |
| Liquid-1000 (assigned stocks) | stock_vs_sector_12_1 | 0.056 | 0.52 | 72.7% | 6.0 | 0.62 | 0.003 |
| Liquid-1000 (assigned stocks) | sector_q5_126 | 0.029 | 0.24 | 64.1% | 2.9 | 0.20 | 0.013 |
| Liquid-1000 (assigned stocks) | sector_hi_252 | 0.027 | 0.17 | 58.1% | 2.1 | 0.18 | 0.014 |
| Liquid-1000 (assigned stocks) | mom_6_1+sector_q5(z) | 0.053 | 0.36 | 70.0% | 4.2 | 0.59 | 0.004 |
| Liquid-1000 (assigned stocks) | q5_126+stock_vs_sector_6_1(z) | 0.079 | 0.64 | 77.8% | 7.3 | 0.88 | -0.008 |
| Mid/small (rank 301-1000) (assigned stocks) | mom_6_1 | 0.077 | 0.56 | 77.1% | 6.8 | 0.79 | -0.015 |
| Mid/small (rank 301-1000) (assigned stocks) | mom_12_1 | 0.090 | 0.60 | 76.7% | 7.0 | 0.74 | 0.016 |
| Mid/small (rank 301-1000) (assigned stocks) | q5_126 | 0.105 | 0.84 | 82.8% | 9.5 | 0.91 | -0.002 |
| Mid/small (rank 301-1000) (assigned stocks) | stock_vs_sector_6_1 | 0.068 | 0.66 | 74.0% | 8.0 | 0.67 | -0.012 |
| Mid/small (rank 301-1000) (assigned stocks) | stock_vs_sector_12_1 | 0.075 | 0.62 | 74.4% | 7.1 | 0.61 | 0.009 |
| Mid/small (rank 301-1000) (assigned stocks) | sector_q5_126 | 0.026 | 0.24 | 60.7% | 3.1 | 0.12 | 0.016 |
| Mid/small (rank 301-1000) (assigned stocks) | sector_hi_252 | 0.017 | 0.12 | 53.8% | 1.4 | 0.12 | 0.007 |
| Mid/small (rank 301-1000) (assigned stocks) | mom_6_1+sector_q5(z) | 0.060 | 0.47 | 70.6% | 5.8 | 0.55 | 0.003 |
| Mid/small (rank 301-1000) (assigned stocks) | q5_126+stock_vs_sector_6_1(z) | 0.098 | 0.79 | 82.1% | 9.0 | 0.88 | -0.011 |

Sector momentum *level* has no signal (IC 3m ≤0.02, |t|<1.5 when evaluated across all assigned stocks); sector *trend quality* (q5, 52w-high) is weak but orthogonal (corr 0.12-0.32, IC 3m 0.017-0.044, t≈1.4-3.3, incremental IC +0.01 to +0.05); stock-minus-sector momentum is a slightly smoother momentum (higher ICIR, lower correlation) but **not more predictive** and has ~zero incremental IC. **Verdict: skip as a standalone factor.**

## 6. Where each factor works (universe guide) and cross-strategy correlation

| Factor (IC 3m) | Top-250 | Liquid-1000 | Mid/small | High-vol tercile | Low-vol tercile |
|---|---|---|---|---|---|
| q5_126 | 0.074 | 0.085 | 0.098 | 0.078 | 0.098 |
| a1_52wh | 0.080 | 0.094 | 0.096 | 0.076 | 0.071 |
| hi_3y | 0.083 | 0.093 | 0.094 | 0.074 | 0.079 |
| mom_12_1 | 0.044 | 0.065 | 0.079 | 0.059 | 0.084 |
| mom_resid_12_1 | 0.066 | 0.073 | 0.076 | 0.062 | 0.086 |
| csm_abs_dual_sharpe | 0.067 | 0.080 | 0.087 | 0.073 | 0.088 |
| low_pain_126 | 0.092 | 0.096 | 0.094 | 0.075 | 0.078 |
| low_ulcer_252 | 0.080 | 0.084 | 0.079 | 0.068 | 0.069 |
| lowvol_126 | 0.061 | 0.062 | 0.058 | 0.066 | 0.011 |
| low_beta_252 | 0.065 | 0.050 | 0.033 | 0.018 | 0.021 |
| intra_over_252 | 0.080 | 0.060 | 0.056 | 0.053 | 0.046 |
| tight_close_15 | 0.031 | 0.042 | 0.044 | 0.051 | -0.004 |
| neg_overnight_126_clip | 0.045 | 0.031 | 0.029 | 0.020 | 0.018 |
| hvol_126 | -0.061 | -0.062 | -0.058 | -0.066 | -0.011 |

Reading: persistence/anchor factors work everywhere and are strongest in mid/small and low-vol names; **momentum weakens in large caps** (Top-250 IC of 12-1 is half that of mid/small) while **risk-aware and intraday factors strengthen there** (low_pain 0.092, hi_3y 0.082, intra_over_252 0.080 in Top-250). Low-beta only works in large caps (0.065 vs 0.033 mid/small). Raw volatility-seeking is negative everywhere.

**Monthly-return correlation across the candidate strategies** (2008-04 → 2026-07, net of costs; stock books = top-15 in Liquid-1000 unless noted):

|  | Elendel | I2 resid | I1 tight | I3 low-risk | I4 intraday | X1 hi252 | X1 mom3m | X4 sector | Gold | Nifty500 |
|---|---|---|---|---|---|---|---|---|---|---|
| Elendel | 1.00 | 0.86 | 0.82 | 0.64 | 0.74 | 0.30 | 0.44 | 0.69 | -0.16 | 0.72 |
| I2 resid | 0.86 | 1.00 | 0.78 | 0.63 | 0.76 | 0.26 | 0.42 | 0.69 | -0.14 | 0.71 |
| I1 tight | 0.82 | 0.78 | 1.00 | 0.72 | 0.76 | 0.37 | 0.49 | 0.74 | -0.12 | 0.74 |
| I3 low-risk | 0.64 | 0.63 | 0.72 | 1.00 | 0.77 | 0.27 | 0.41 | 0.80 | -0.07 | 0.76 |
| I4 intraday | 0.74 | 0.76 | 0.76 | 0.77 | 1.00 | 0.31 | 0.46 | 0.81 | -0.14 | 0.86 |
| X1 hi252 | 0.30 | 0.26 | 0.37 | 0.27 | 0.31 | 1.00 | 0.74 | 0.29 | 0.31 | 0.36 |
| X1 mom3m | 0.44 | 0.42 | 0.49 | 0.41 | 0.46 | 0.74 | 1.00 | 0.45 | 0.30 | 0.50 |
| X4 sector | 0.69 | 0.69 | 0.74 | 0.80 | 0.81 | 0.29 | 0.45 | 1.00 | -0.09 | 0.88 |
| Gold | -0.16 | -0.14 | -0.12 | -0.07 | -0.14 | 0.31 | 0.30 | -0.09 | 1.00 | -0.12 |
| Nifty500 | 0.72 | 0.71 | 0.74 | 0.76 | 0.86 | 0.36 | 0.50 | 0.88 | -0.12 | 1.00 |

The factor-based stock ideas are 0.6-0.9 correlated with the Elendel book (as you expected). The only low-correlation building blocks are **asset-class rotation (0.26-0.49) and gold (≈ −0.15)**; the low-risk sleeve is the lowest of the stock ideas (0.63).

### ETF proxies available for the index ideas (recent median daily traded value)

| ETF | Name | History from | Median value / day |
|---|---|---|---|
| NIFTYBEES | NIP IND ETF NIFTY BEES | 2002-01-08 | ₹168.7 cr |
| JUNIORBEES | NIP IND ETF JUNIOR BEES | 2007-01-02 | ₹26.0 cr |
| BANKBEES | NIP IND ETF BANK BEES | 2004-06-04 | ₹57.4 cr |
| MID150BEES | NIP IND ETF MIDCAP 150 | 2019-02-04 | ₹14.0 cr |
| HDFCSML250 | HDFCAMC - HDFCSML250 | 2023-02-21 | ₹28.3 cr |
| GOLDBEES | NIP IND ETF GOLD BEES | 2007-03-19 | ₹237.9 cr |
| SILVERBEES | NIPPONAMC - NETFSILVER | 2022-02-07 | ₹500.4 cr |
| LIQUIDBEES | NIP IND ETF LIQUID BEES | 2007-01-02 | ₹295.2 cr |
| LIQUIDCASE | ZERODHAAMC - LIQUIDCASE | 2024-01-24 | ₹180.3 cr |
| MON100 | MOTILAL OS NASDAQ100 ETF | 2015-01-01 | ₹13.6 cr |
| HNGSNGBEES | NIP IND ETF HANGSENG BEES | 2010-03-18 | ₹5.3 cr |
| ITBEES | NIP IND ETF IT | 2020-07-01 | ₹54.9 cr |
| PHARMABEES | NIPPONAMC - NETFPHARMA | 2021-07-07 | ₹15.9 cr |
| PSUBNKBEES | NIP IND ETF PSU BANK BEES | 2007-11-01 | ₹20.0 cr |
| LTGILTBEES | NIP IND ETF LONGTERM GILT | 2016-07-14 | ₹3.6 cr |
| SMALLCAP | MIRAEAMC - SMALLCAP | 2024-02-29 | ₹8.0 cr |
| MIDCAPETF | MIRAEAMC - MAM150ETF | 2022-03-15 | ₹4.6 cr |

Full list: `results/etf_liquid_list.csv`. Note mid/small-cap ETFs with meaningful liquidity only exist from 2019-2024, so back-tests on those sleeves rely on index data that you could not have fully captured earlier.

## 7. Rejected / low-value signals (so they are not re-tested)

| Factor | IC 1m | IC 3m | ICIR 3m | Hit 3m | t | IC ≤2014 | IC ≥2015 | Note |
|---|---|---|---|---|---|---|---|---|
| rev_1m | 0.004 | -0.024 | -0.20 | 38.0% | -3.0 | -0.030 | -0.018 | continuation, not reversal |
| rev_1w | 0.011 | -0.011 | -0.11 | 42.7% | -1.8 | -0.015 | -0.007 | continuation, not reversal |
| overnight_126 | -0.028 | -0.030 | -0.28 | 37.5% | -3.2 | -0.035 | -0.024 |  |
| overnight_minus_intraday_126 | -0.038 | -0.051 | -0.45 | 29.1% | -5.1 | -0.058 | -0.045 | sign-flipped = I4 (intraday-led trend) |
| gapup_freq_63 | -0.032 | -0.032 | -0.23 | 37.5% | -2.7 | -0.029 | -0.036 |  |
| event_ret_63 | -0.026 | -0.020 | -0.19 | 42.6% | -2.3 | -0.012 | -0.028 |  |
| illiq_amihud_63 | -0.027 | -0.023 | -0.15 | 41.5% | -1.7 | -0.013 | -0.034 | no illiquidity premium |
| small_dvol_63 | -0.024 | -0.019 | -0.13 | 41.4% | -1.5 | -0.011 | -0.027 | no small-size premium |
| vol_surge_21_252 | -0.010 | 0.002 | 0.02 | 49.3% | 0.3 | 0.004 | -0.000 |  |
| up_capture_252 | -0.027 | -0.033 | -0.18 | 41.1% | -2.1 | -0.033 | -0.032 |  |
| high_beta_252 | -0.038 | -0.050 | -0.25 | 37.4% | -2.8 | -0.058 | -0.042 |  |
| hvol_126 | -0.053 | -0.062 | -0.35 | 33.8% | -4.1 | -0.062 | -0.061 | volatility-seeking loses |
| beta_regime | -0.020 | -0.021 | -0.10 | 44.8% | -1.1 | -0.029 | -0.012 |  |
| atr_expansion_14_63 | -0.012 | 0.005 | 0.05 | 54.5% | 0.8 | 0.006 | 0.003 |  |
| range_expansion_up | -0.013 | 0.003 | 0.04 | 54.0% | 0.6 | 0.013 | -0.007 |  |
| mom_accel | -0.002 | -0.010 | -0.11 | 44.7% | -1.4 | -0.007 | -0.013 |  |
| nr7_count_21 | 0.001 | -0.009 | -0.18 | 45.5% | -3.0 | -0.015 | -0.003 |  |
| vr_5_252 | -0.014 | -0.020 | -0.22 | 36.7% | -2.5 | -0.023 | -0.016 |  |
| autocorr1_126 | -0.016 | -0.020 | -0.24 | 40.0% | -2.8 | -0.022 | -0.018 |  |
| jump_up_freq_126 | -0.021 | -0.013 | -0.21 | 40.7% | -2.7 | -0.004 | -0.022 |  |

## 8. Suggested build order

1. **I1 + I2 as new books in the mid/small universe** (rank 301-1000) using the existing chassis; keep the top-15 / hysteresis / inverse-vol machinery but add the **SMA200 gate + volatility-target overlay** (§3.1) and re-measure in the full engine. These have the best evidence and the best book Sharpe, but expect 0.8-0.9 correlation with the current momentum books — differentiate via universe, stops and sizing.
2. **I3 low-risk sleeve** as the drawdown-control / diversification book (low turnover, works in bear regimes); combine with the **factor-index regime evidence** (§4.3) to scale it up when the market is >10% off its high.
3. **X1 asset-class rotation** (Nifty/Midcap/Smallcap/Gold/LIQUIDBEES) as the genuinely decorrelated sleeve — treat the gold leg skeptically (2019-26 bull) and cap its weight.
4. **I6 breakout v3** — add RS-top-quartile + trend-template gate to HR/VCP, drop the volume requirement, and evaluate with the stop/exit logic (event study shows no raw edge without the gate).
5. **I4** only for a large-cap (top-300) variant, after validating open-price quality on a second data source.
6. **Add the India-VIX spike rule** as a re-entry/leverage signal to the Crash Guard logic of existing books and test it in the live engine (39 events — treat as supporting evidence only).

## 9. Caveats that matter

* **Survivorship bias** (only ~2% of symbols are delisted) inflates absolute CAGRs, most for low-vol and smooth-trend selection; relative comparisons are more trustworthy than levels.
* **Stripped books**: equal weight, monthly, no stops/Crash Guard/take-profit/regime leverage. Use them to *rank ideas*, not to forecast live CAGR/drawdown.
* **Holdout decay**: nearly every price-based signal has ~30-40% lower IC in 2015-2026 than in 2004-2014 (still t>5 for the main factors). Idea ranks were not tuned on the holdout, but the pack definitions were chosen after seeing single-factor results on the full sample.
* **Multiple testing**: ~120 factors, ~10 packs, many universes. Packs/overlay parameters (weights 0.5/1.0, SMA200, 50%, 20% vol target) were fixed in advance, but an idea that wins in one universe only (e.g. I1 in mid/small, I4 in large-cap) deserves out-of-sample paper trading before capital.
* **Index/ETF history is short and regime-poor** (≤19y with gold), cross-asset N is tiny, and index ≠ tradable ETF before 2010-2024.
* Equal-weight market index is used as the beta/regime proxy (as in the live runners); benchmark index files in `benchmark_data/` cover 2026 only, but `index_data/` has the full history if you want to switch to Nifty-based regime flags.

## 10. Appendix — definitions and files

| Factor | Definition (signal at close of t; higher = better) |
|---|---|
| `q5_126 / q5_189` | share of last 126/189 days with close > SMA50 (live Elendel / Zenith leg) |
| `a1_52wh, a3_rs_high` | close / 252d high; RS-line (stock/equal-weight market) / its 252d max (live) |
| `tight_close_15` | −std(close, 15d)/mean(close, 15d) |
| `mom_resid_12_1` | Σ over t−252…t−21 of [daily return − beta₍t−1₎ × equal-weight market return], beta from 252d rolling covariance |
| `lowvol_126` | −std of daily returns over 126d |
| `low_ulcer_252` | −sqrt(mean( (close / trailing-252d max − 1)² )) over 252d |
| `low_pain_126` | mean over 126d of (close / trailing-126d max − 1)  (negative; closer to 0 is better) |
| `intra_over_252` | Σ log(close/open) − Σ log(open/prev close) over 252d, each daily leg clipped to ±15% |
| `hi_3y` | close / 756d high |
| `csm_abs_dual_sharpe` | ½[(P₍t−1₎/P₍t−10₎ −1)/σ₉ₘ + (P₍t−1₎/P₍t−5₎ −1)/σ₄ₘ], σ = monthly-return std × √12, clipped ±5 (csm_absolute.py) |
| `hvol_126, beta_regime, …` | see `factors.py` (all ~120 definitions with docstrings) |

Files: `data.py`, `assets.py` (loaders) · `factors.py` (factor library) · `evaluate.py` (IC/ICIR/hit/t engine) · `portfolio_lab.py`, `index_lab.py` (books) · `run_scan.py` + `stage2…13_*.py` (studies) · `results/*.csv` (all numbers) · `FINDINGS.md` (first-pass study) · `gen_report.py` (this document).

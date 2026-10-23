# Momentum Beyond Lookback Windows — Signal Bake-off

> **Superseded:** full 2000-2025 rerun with detailed signal explanations is in `MOMENTUM_SIGNALS_EXPLAINED.md`.

**Date:** 2026-09-21 · **Script:** `momentum_family_bakeoff.py` → `momentum_family_bakeoff_results.csv`
**Setup:** upstox OHLCV via `sr_panel` (CA-masked), top-1000 by 63d dVol, signal read at T-1 close,
fill T+1 open → close T+h, sampled at 191 month-ends 2010-01 → 2025-11. Cross-sectional Spearman IC,
Newey-West t (lag = h/21). **Incremental IC** = IC of the signal's rank after regressing out the rank
of the current live signal (BASE = dual 12m/6m Sharpe, skip 1m) → "does it know something new?"

## The problem, stated precisely
Every live book (csm_batch / csm_quad / csm_absolute) ranks on *how much the price rose over N months*.
Changing N or averaging several N's is the same information: 12-1m raw return has corr **0.92** with
BASE and adds nothing (incremental t −0.72). Note: almost every price signal uses *some* window — the
point is **what** it measures. Low correlation with BASE is the proof that the information is different.

## Results (h = 63d, the relevant holding horizon)

| signal | family | IC | NW-t | IC 2010-17 | IC 2018-25 | corr w/ BASE | incr IC | incr t | top-quintile excess %/yr |
|---|---|---|---|---|---|---|---|---|---|
| **BASE dual Sharpe 12/6** | lookback return | .076 | 6.07 | .094 | .058 | 1.00 | — | — | 9.5 |
| 52w-high proximity | anchor | **.104** | 6.45 | .121 | **.088** | **0.58** | **.079** | **5.83** | 6.9 |
| RS line at 52w high | anchor | .100 | 7.15 | .117 | .083 | 0.71 | .065 | 6.27 | 9.0 |
| 52w range position | anchor | .087 | 6.61 | .107 | .066 | 0.71 | .050 | 5.78 | 8.8 |
| Trend persistence (% days > SMA50, 126d) | trend quality | .085 | **7.74** | .101 | .068 | 0.79 | .040 | 5.75 | 9.4 |
| Trend R² × sign (126d) | trend quality | .072 | 6.69 | .090 | .054 | 0.76 | .022 | 2.71 | 8.1 |
| Clenow slope × R² (90d) | trend quality | .056 | 5.11 | .070 | .042 | 0.62 | .012 | 1.30 | 7.0 |
| New-high recency | anchor/event | .054 | 5.00 | .071 | .037 | 0.62 | .016 | 2.57 | 6.6 |
| Residual (beta-stripped) momentum | lookback, de-beta'd | .074 | 5.71 | .095 | .052 | **0.91** | .009 | 1.03 | 8.4 |
| Sector / industry momentum | cross-asset | .035 | 3.82 | .049 | .022 | **0.20** | .024 | 2.69 | 6.0 |
| Low MAX daily return (lottery) | risk/path | .047 | 4.48 | .039 | .056 | **−0.03** | .046 | 4.49 | 0.7 |
| Volatility contraction (ATR% vs own median) | coil / timing | .025 | 4.22 | .033 | .017 | **0.00** | .024 | 4.11 | 0.8 |
| Up/down volume ratio | volume | .018 | 2.38 | .039 | **−.003** | 0.25 | −.002 | −0.22 | 2.9 |
| Frog-in-the-pan smoothness | path | −.010 | −0.92 | −.008 | −.011 | −0.23 | −.001 | −0.18 | −3.1 |
| FIP × momentum | path | .011 | 1.31 | .016 | .007 | 0.14 | −.006 | −1.11 | 1.4 |
| Acceleration (3m − prior 3m) | 2nd derivative | −.007 | −0.87 | −.007 | −.007 | −0.13 | .004 | 0.48 | −0.1 |
| Seasonality (same month, 5y) | calendar | −.006 | −0.92 | .005 | −.016 | 0.03 | −.008 | −1.29 | −1.9 |
| 1m reversal | short-term | −.028 | −3.27 | −.041 | −.015 | −0.04 | −.024 | −3.03 | −2.2 |

## Blends (equal-weight cross-sectional z-scores)

| blend | IC | NW-t | ICIR | 2010-17 | 2018-25 | top-decile excess %/yr | corr w/ BASE |
|---|---|---|---|---|---|---|---|
| BASE (today) | .076 | 6.07 | .65 | .094 | .058 | 8.2 | 1.00 |
| RS line + Trend persistence | .100 | 7.52 | .79 | .118 | .081 | 11.4 | 0.81 |
| **52w high + RS line + Trend persistence** | **.106** | 7.27 | .77 | .125 | .087 | **11.6** | 0.77 |
| 52w high + Persistence + Low-MAX | .115 | 7.76 | .82 | .126 | .103 | 8.6 | 0.67 |
| 52w high + Persistence + Low-MAX + Sector | **.117** | **8.74** | **.90** | .128 | **.105** | 9.4 | 0.66 |

Pairwise: the three anchor signals are 0.86-0.87 correlated with each other (pick one or two);
Low-MAX / vol-contraction are ~0 correlated with everything (true diversifiers, but see rank 4).

## Ranking

1. **Anchor momentum (52-week-high proximity / RS line at its high).** Beats BASE outright (IC .104 vs
   .076), shares only 0.58 of its information, incremental t 5.8-6.3, and decays the *least* in
   2018-25 (.088 vs BASE .058). Behavioural anchoring: investors under-react to good news near a
   known high. Use RS-line-high or 52w-high (RS line has better top-quintile returns). Also the most
   natural bridge to your breakout books — the same "near the high" information they trade on events.
2. **Trend persistence / trend quality.** Highest t-stat of any single signal (7.74, ICIR .83) —
   measures how *consistently* a stock stayed in trend, not how far it moved. Incremental t 5.75.
3. **Composite of 1 + 2** — the actual recommendation for a new selector: top-decile excess
   **11.6 %/yr vs 8.2 %/yr for BASE**, IC .106, and it holds up better in 2018-25.
4. **Low-MAX and volatility contraction — use as filters/timing, not selectors.** ~0 correlation,
   incremental t 4.1-4.5, lift blend IC and late-period stability — but top-quintile excess is only
   ~0.7-0.8 %/yr and monotonicity is weak: their edge comes from *avoiding* lottery blow-ups, not
   picking winners. Vol-contraction is the VCP "coil" — this is Fix 3 from the sizing report
   (breakout-style entry timing) with evidence behind it.
5. **Sector momentum as a tilt.** Low correlation (0.20), modest standalone (t 3.8); improves blend
   ICIR (.82 → .90). Pairs with the existing sector_rotation work.
6. **Residual momentum — deprioritise.** Works (t 5.7) but corr 0.91 with BASE: on this data it is
   essentially your current signal with the beta taken out.
7. **Rejected:** frog-in-the-pan (works in US literature, fails here both halves), acceleration,
   seasonality, up/down volume (dead after 2018), Clenow slope×R² (redundant with trend persistence).

**Side finding:** 1m "reversal" is *negative* (t −3.3; incremental −3.0) — last month's winners keep
winning. BASE's skip-month may be discarding information. Cheap test: drop `lag_months` to 0.

## Caveats
- IC ≠ backtest P&L; a signal swap must still be run through a real engine with costs.
- Survivorship-biased data (no delisting calendar) → IC levels are upper bounds; *relative* ranking
  is the robust output.
- The 2018-25 half was used here as a stability check, so it is no longer a clean holdout for these
  specific signals (per the stage-gate playbook).
- Every signal decays after 2018 (BASE −38 %); the anchor family retains the most (−27 %).

## Next step
Swap the selector in the csm_quad chassis only (keep universe, sizing, stops, overlays fixed):
BASE vs 52w-high vs (52w-high + RS line + persistence), same backtest, costs on — a clean one-variable test.

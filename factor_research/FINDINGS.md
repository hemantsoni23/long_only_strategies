# Factor research for new long-only strategies — findings (2026-10-05)

Scope: OHLCV-only signals on the Upstox NSE/BSE universe (5,205 symbols, 2003 → 16 Jul 2026), evaluated with the
same conventions as the live runners (monthly Spearman rank IC, ICIR = mean/std, hit rate = % months IC>0), plus
Newey-West t-stats, horizons 1/2/3/6/12 m, a discovery (≤2014) / holdout (≥2015) split, and top-15 book tests.
Nothing in `Old_live_strategies/` was touched.

## How to reproduce
```
python3 data.py                 # build/cached parquet panels (≈20 s)
python3 run_scan.py --rebuild   # 111 factors x 3 universes -> results/scan_*.csv
python3 stage2_composites.py    # add-ons to Elendel / Zenith composites
python3 stage3_standalone.py    # standalone top-15 book per factor + correlation to live books
python3 stage4_regime.py        # bull / bear split
python3 stage5_breakout.py      # daily breakout event study
```
Outputs: `results/factor_catalog.csv` (every factor, tiered), `scan_*.csv`, `stage2..5_*.csv`.

Method notes: signal at close of month-end t, entry at close t+1 (live T+1 lag). Forward returns use cleaned daily
returns (jump days outside −40%/+300% counted as 0, delisted names stay flat). Universes: U1 = price>₹20, top-1000
63d-median traded value, circuit ≤5/63d (≈700 names avg); U2 = U1 ∩ above SMA200 (what the live pipeline ranks);
U3 = top-300 liquid. Factor direction ("higher = better") was fixed before looking at results.

## 1. The live signals are already near the top of what OHLCV offers
| signal (U1, 3m) | IC | ICIR | hit | t(NW) | IC disc / hold |
|---|---|---|---|---|---|
| Q5-126 (trend persistence) | 0.085 | 0.70 | 78% | 8.0 | 0.104 / 0.066 |
| Zenith A1+Q5-189 | 0.104 | 0.66 | 79% | 7.5 | 0.121 / 0.087 |
| Elendel A3+Q5-126 | 0.095 | 0.65 | 77% | 7.4 | 0.115 / 0.076 |
| A3 / A1 alone | 0.092 / 0.094 | 0.60 / 0.55 | 76% / 75% | 6.9 / 6.4 | |

Horizon: peak IC at 6 m (12 m for pure 52w-high family) — consistent with the monthly/hysteresis design.
Holdout IC is ~35–40% lower than discovery for every price-based signal (all still t>5): edge is real but fading.

## 2. Factor tiers (111 factors; see factor_catalog.csv)
* **B — significant but redundant with live (40)**: corr 0.6–0.9 with Elendel (trend t-stat/R², Clenow, KER,
  weekly consistency, 504/756-day highs, low-ulcer, residual momentum, RS-line trend...). Same bet, not new.
* **C — significant, both halves same sign, also holds in top-300 (29), corr<0.6 with Elendel**. The ones worth a look:
  * *Low-risk family* — lowvol_63/126/252, low_ivol, low_downvol, low_atrp, low_max_21/63 (live Zenith M3),
    low_ulcer/shallow_dd: IC3 0.05–0.08, corr ≈ 0, incremental IC after removing Elendel +0.05–0.07,
    t 3.9–5.5, positive in bear months (IC3 0.07–0.08).
  * *Intraday vs overnight drift* — intraday_126 / intra_over_63/126/252: IC3 0.05–0.07, t 5.2–6.0, **stronger in
    the top-300 (t≈5.4) than in U2**; corr with Elendel 0.3–0.58. Mirror image: overnight drift is *negative*
    (t −3.2 → −5.1 for overnight-minus-intraday): gap-driven moves fade, intraday-built trends persist.
  * *Smoothness / tight price action* — tight_close_15, low_volvol_126, up_days_net_231, mom_consistency.
  * *Seasonality* (same calendar month, 5y): IC1 0.024, t 4.6 — **1-month only**, dies by 3 m; turnover 75–85%.
* **D — rejected**: 1w/1m reversal (continuation, not reversal: IC3 −0.024), illiquidity/small-size (negative: no
  small-cap premium in this universe), abnormal-volume-day returns, gap-up frequency, up-capture, high beta,
  volume surge, momentum acceleration, NR7 counts, ATR contraction.

## 3. Why IC alone is not enough — the top-15 book test
Rank IC rewards the whole cross-section; a 15-name book lives in the extreme tail.
* Low-risk add-ons raise IC (Elendel 0.077 → 0.098 with lowvol) and cut turnover, but **reduce top-15 book CAGR and
  holdout Sharpe** (U2: Sharpe 0.81 → 0.74, hold 0.76 → 0.54). Their top-quintile *mean* excess is negative; the
  edge is in win-rate vs median / risk, not in return.
* **Residual momentum (CAPM, 12-1) is the only add-on that improved everything**: U2 CAGR 28.6% → 35.2% (w=0.5) /
  36.9% (w=1.0), Sharpe 0.81 → 0.94 / 0.97, maxDD −58% → −52%, turnover 0.58 → 0.42–0.46, and on Zenith holdout
  Sharpe 0.40 → 0.58–0.68. (Caveat: residual momentum is already a live strategy; the finding is that it
  complements Elendel/Zenith.)
* **Q5-126 alone beats the A3+Q5 composite in the simple book** (U1 Sharpe 0.95 vs 0.74, CAGR 32.5% vs 26.2%; holdout
  0.745 vs 0.772 — i.e. equal out-of-sample, better in-sample). Lead for improving Elendel; must be re-tested in the
  full live engine before acting.
* Every momentum-family standalone book is 0.75–0.9 correlated with the live books; even low-risk books are ≈0.65–0.72.
  OHLCV price/volume factors do not give a genuinely uncorrelated return stream.

## 4. Breakout event study (daily signals, entry t+1 close, excess vs same-day liquid universe)
* Raw breakouts are weak: Donchian-55 20d excess −0.2%, 60d +0.6% (t 1.6); 52w-closing-high 20d +0.6% (t 3.9),
  60d +1.75% (t 4.9). **Hit rate vs universe is only 43–48%**; positive mean comes from a fat right tail
  (median 20d excess −1.0% to −1.7%). Any breakout strategy needs payoff skew + tight loss control, not accuracy.
* The edge is in the *filter*, not the breakout: Donchian-55 + RS top-quartile + Stage-2 trend template + 1.5x volume:
  60d excess +2.7% (t 4.4, disc +4.4% / hold +1.8%); the same breakout without RS/trend: −0.2% (t −0.2).
  52w-high with RS top-25%: 60d +2.9% vs +1.0% otherwise.
* **Volume confirmation does not help** (52w-high: <1.5x vol 20d +0.9% vs ≥1.5x +0.45%; Donchian-55 with ≥1.5x vol
  is negative). Consistent with `event_ret_63` / `nh_volconfirm` factor results. Gap-up breakouts: no worse.
* Compressed (VCP-like) bases add a little at 60d (+2.5% vs +1.75%) but with only ~3k events and t 5.1.

## 5. Candidate directions for new strategies (ranked by evidence, none yet backtested in the full engine)
1. **Residual-momentum overlay on Elendel/Zenith** (weight ~0.5): best evidence of improving a live book.
2. **Q5-only / Q5-weighted Elendel variant**: improvement lead for an existing live strategy.
3. **Low-risk-trend sleeve** (low_ulcer_252 + lowvol, rank autocorr 0.98, book turnover 0.19–0.3, maxDD ≈ −45% vs −67%):
   a lower-vol, lower-turnover sleeve; return correlation to live ≈ 0.7; weak holdout Sharpe (0.4–0.5).
4. **Intraday-drift trend strategy** (intra_over_126/252 + trend filter): most distinct signal that is also robust in
   large caps; needs open-price data-quality check (clipped ±15%/day already) before trusting.
5. **Breakout v3**: RS-top-quartile + trend-template gate on 52w-high/Donchian breakouts, drop volume gate; evaluate with
   stops/exits in an event-driven backtest.
6. Seasonality as a small tilt only (1-month horizon; costly turnover).

## 6. Caveats (read before trusting any number)
* **Survivorship bias**: only 98 of 5,205 symbol files end before mid-2026 — the dataset is overwhelmingly
  currently-listed names. This flatters long-only price signals, low-vol and "smooth trend" screens most.
  Small/illiquid factors came out negative, which is mildly reassuring, but the absolute levels are optimistic.
* Books here are deliberately stripped (equal weight, monthly, no stops/regime/crash guard); their drawdowns
  (−45% to −70%) are not comparable with the live strategies. Use them only for *relative* comparisons.
* ~111 factors were tested; with t-stat ≥3 plus same-sign discovery/holdout the false-positive risk for tier C is low
  but not zero. The weight choices in `stage2_composites.py` (0.5, 1.0) were fixed in advance, not tuned.
* The equal-weight market index is the benchmark/beta proxy (as in the live runners); Nifty index files cover 2026 only.
* No fundamentals/delivery/sector data were used. `upstox_data_folder/pit_harness` (point-in-time fundamentals) is the
  most promising route to a *truly* orthogonal signal (quality, value, earnings revisions) — worth a dedicated pass.

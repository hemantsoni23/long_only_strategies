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

## 7. Industry/sector momentum, bottom-up construction (2026-10-09)

Three prior unlogged attempts at a sector/industry strategy (all via `instruments_clean.csv`) had failed. Diagnosis from
`stage7_sector.py`/`stage10_sector_stock.py` plus the full `momentum/` literature (Moskowitz-Grinblatt 1999, Lewellen 2002,
Da-Liu-Schaumburg 2014, Grundy-Martin via the JT 2011 survey, Swinkels 2004 survey): too few independent "assets" (only 19
NSE sector indices / 11 `Sector_clean` buckets), the wrong horizon tested (6/12m only, not the 1-3m band the literature
flags, and no skip-month variant), and a residualizing (subtractive) construction that fights the literature's own additive
mechanism. Rebuilt in `stage18_industry_momentum.py`: industry/sector baskets built **bottom-up from member stocks**
(`instruments_clean.csv`'s 205-category `Industry_clean`, falling back to the 11-bucket `Sector_clean` in any month an
industry has <10 live `U1_liquid1000` members — avg. 20-31 usable industries/month since 2008), not from any external
index/ETF series — this sidesteps the sector-ETF history problem entirely (most sector ETFs only start 2021+) and is
refreshable indefinitely (pure OHLCV + a static classification file, no fundamentals dependency). 64 variants swept
(formation 1/3/6/12m × skip 0/1 × level/residual construction × `Industry_clean`/`Sector_clean` × equal/dollar-volume
weight), each evaluated at every forward horizon.

**Stage 1 (IC/ICIR) — clean, decisive win.** Winner `indmom_level_ind_eq_L3_skip0` (3-month formation, no skip,
`Industry_clean` with fallback, equal-weighted, **additive** "level" construction — the construction the literature
predicts, not the residual one that failed before): t₃/t₆ = 3.5–8.3 across all 4 universes, same-sign discovery/holdout IC
everywhere, and — the key number — **`corr_elendel` only 0.21–0.30**, against 0.6–0.68 for every sector factor tried
before, with `inc_ic` clearly positive everywhere. Sanity check: the bottom-up `Sector_clean` baskets correlate 0.5–0.94
(monthly returns) with the matching real NSE sector index, confirming the construction behaves like a real sector, not an
artifact. All top factors in the sweep were **additive**, not residual — confirms Moskowitz-Grinblatt's finding that
industry-adjusting (subtracting) kills the effect. All top factors were **no-skip** — sides with Moskowitz-Grinblatt over
Grundy-Martin on the skip question, at least in this market. The effect was strongest in **`U7_midsmall_301_1000`**
(t=8.3) rather than the large-cap universes (`U1` t=6.9, `U3_top300` t=4.0) — sides with Nijman-Swinkels-Verbeek's
small/mid-cap finding over Moskowitz-Grinblatt's US large-cap concentration; this market doesn't replicate the literature's
cap-concentration finding either way, which is exactly why the plan tested both ends rather than assuming one.

**Stage 2 (additive tilt on the live ELEN/ZEN composites, proxy top-15 book) — fails the gate.** `stage19_industry_tilt_proxy.py`
blended `z(base) + w·z(indmom_level_ind_eq_L3_skip0)` at w∈{0.3,0.5,1.0} into the Elendel and Zenith composites on `U1_liquid1000`
and `U2_live_trend` (the universes those composites actually trade — not `U7`, where the factor is strongest). Result: the
ELEN tilt **raises** discovery-period Sharpe sharply (0.70→0.85–0.99 on U1) but **lowers** holdout Sharpe (0.77→0.51–0.68) at
every weight — the opposite of what's wanted. The ZEN tilt is closer to neutral (U1, w=0.5: disc 1.00→0.97, hold 0.38→0.45)
but never clears "beat the base in both periods" at any preset weight. **Verdict: cut at Stage 2** — the gate
("tilted must beat the un-tilted base on Sharpe in both discovery and holdout") was set in advance and is not met, despite
Stage 1's unusually clean IC. This is exactly the IC-vs-book gap this project has seen before (§3): rank IC rewards the
whole cross-section, a top-15 book lives in the tail, and here the factor's best universe (`U7_midsmall_301_1000`) isn't
even the one being tilted. **Not pursued further under this plan** — Stage 3 (real-engine tilt) was gated on Stage 2 and was
not run. A **documented, not-yet-tested** follow-on for a future pass: a standalone top-15 book built directly on
`indmom_level_ind_eq_L3_skip0` in `U7_midsmall_301_1000` (where Stage 1's signal is strongest) rather than as a tilt on
large-cap-weighted ELEN/ZEN — this would be a new candidate requiring its own Stage-1→2→3 gating, not an extension of this
result.

Reproduce: `python3 stage18_industry_momentum.py` then `python3 stage19_industry_tilt_proxy.py` (needs `.cache/state.pkl` /
`.cache/extra_universes.pkl` from `run_scan.py`/`stage6_universes.py`, already built). Caveat carried over from the plan:
`instruments_clean.csv` is a static, current-day snapshot (no point-in-time reclassification history) — bounded, not fixed.


## 8. Industry-led staggered book: faithful-accounting study (2026-10-10)  [independently verified - see 8.7; read 8.6-8.7 before any number]

Pre-registration: `INDUSTRY_BOOK_PREREG.md` (written before any book was simulated). Code: `industry_lib.py` (vectorised baskets, leave-one-out), `industry_book.py`
(faithful simulator), `stage21_industry_loo_signal.py` (signal gate), `stage22_book_battery.py` (book gates; `VT=0.15 python3 stage22_book_battery.py` for D1v).
Results: `results/stage21_*.csv`, `results/stage22_*.csv`, `results/stage22_book_battery*.txt`.

### 8.1 Why a new simulator
`csm_value/AUDIT.md` shows the Elendel-family engine booking (executed weight x same-day close-to-close return) credits the never-held entry gap and never charges the
stop-fill gap, inflating live-engine CAGR by 17-26 points (Elendel 32.4 -> 10.9, Zenith 30.5 -> 13.2, Quad 26.1 -> 6.3 over 2003-26). The "Sharpe 1.7-2.7, MaxDD -12..-16%" figures every
discarded sector strategy was compared against are engine-booked. `industry_book.py` books honestly: signal at close t, fill at close t+1, positions earn from t+2, 0.3%/side on
traded notional, no stops, cash at 6.5%, locked/NaN names cannot be bought. All comparators in this section use that accounting or the faithful replay `csm_value/output/faithful_engine_returns.csv`.

### 8.2 Signal (stage21): leave-one-out industry momentum is real
LOO removes the stock's own return from its basket (self-inclusion was ~8% of the IC: 0.062 -> 0.058 on U1, 0.072 -> 0.066 on U7). LOO L3 skip0: IC 0.058 (U1) / 0.066 (U7) at 3m,
NW-t 6.9 / 8.0; t >= 3.9 in BOTH halves (<=2012, >=2013) and >= 4.2 in 2015+ holdout; deciles 9/9 monotone (top-bottom 3.5% / 4.6% per 3m); top-2-year share of IC 23%;
placebos: global shuffle IC -0.003..+0.006 vs real 0.058-0.069 (p=0/60); within-sector shuffle 0.040-0.048 vs real (p=0/60) - industry labels add ~30% of the IC beyond the 11 sectors.
Gate G1 literal verdict FAIL only on sub-gate (c), which I mis-specified ("max |t| over 60 null draws < 2" - impossible with overlapping returns, and LOO biases null IC to -0.003); logged in the
override table of the pre-registration (needs user sign-off). Factor-level correlation with Elendel 0.21-0.30; Fama-MacBeth coefficient +4.9 (t 6.5) with all stock-level controls.

### 8.3 Book D1 (pre-registered primary): industry-led, staggered, no stops
L3 skip0 basket momentum; top 8 usable positive-return Industry_clean (>=10 live U1 members); 2 stocks each by A1 (52w-high proximity) from the U2 trend pool; Jegadeesh-Titman tranches H=6;
gate 0.5x when the EW index < SMA200; ~57 names; ~167%/yr one-way turnover. 2005-08 -> 2026-07, faithful: CAGR 21.1%, vol 16.5%, Sharpe 1.24 (rf6 0.89), **MaxDD -43.0% (Jan-Mar 2008)**, Calmar 0.49.
Same-accounting comparators: EW pool + gate 18.5% / 1.03 / -55%; faithful live Zenith 12.4% / 0.97 / -31.5%; Elendel 10.6% / 0.76 / -38.6%; Quad 7.2% / 0.58 / -43.8%; faithful trio 10.2% / 0.85 / -37.1%.
Pre-registered gates for D1: B1 PASS (random-stock p=0.005), B2 PASS but thin (random-industry p=0.025 full, 0.189 in half B), **B3 FAIL (shuffled-label p=0.17)**, **B4 FAIL in Split B (MaxDD 1.86x, Calmar 0.46)** because 2008 sits in
the out-of-sample half - every long-only book fails that direction (EW pool 1.47x/0.47, TOPN-zen 2.18x/0.50); only the faithful engines pass it, and only because they got WORSE after 2013 (Zenith Sharpe 1.41 -> 0.75). D1 verdict: FAIL, kill rule fired on B4.

### 8.4 What drives the performance (controls, same accounting; Sharpe / CAGR / MaxDD)
equal-weight pool+gate 1.03 / 18.5% / -55%;  random stocks (same N, H, gate) 1.04 / 18.7% / -54%;  real industries + random stocks 1.12 / 19.9% / -45%;  random industries + A1 1.17 / 18.4% / -41.5%;  D1 1.24 / 21.1% / -43%;
no-industry staggered top-16: A1 1.16 / 19.3% / -53%, Zenith composite 1.27 / 22.3% / -54%, Elendel composite 1.31 / 25.8% / -55%, Q5 1.35 / 25.3% / -50%; industry-led with Zenith score 1.34 / 23.0% / -41.5%.
Same signals re-ranked monthly (H=1): A1 0.69, Zenith 1.12. **Conclusions: (i) most of the edge is portfolio construction - staggering (turnover 167% vs ~720%), breadth (~57 names), pool, gate, cash yield; (ii) the industry layer adds a
~10-12 point MaxDD reduction, but a random-industry book gets the same reduction, so that comes from the one-name-pair-per-industry cap and the positive-return filter, not from ranking hot industries; (iii) ranking adds ~+0.08..0.10 Sharpe
(dose-response flat for n_ind 4-12, premium 0.06-0.14). Erased >=40% daily losses (603 cells) matter little for D1 (21.1 -> 21.0% CAGR).**

### 8.5 D1v: add the chassis-style vol target (post-look modification #1, logged)
15% annual vol target of the whole book, 63-day realised vol lagged a day, de-leverage only, 0.3% x |dscale| (the user's chassis parameters; NOT tuned; 12% / 18% shown as sensitivity). Applied identically to every null and benchmark.
**D1v: CAGR 19.1%, vol 13.1%, Sharpe 1.41 (rf6 0.96), MaxDD -23.3%, Calmar 0.82; half A (2005-12) Sharpe 1.53 / DD -23.3%, half B (2013+) Sharpe 1.34 / DD -19.3%.** 12% target: -19.2% DD / Calmar 0.93; 18%: -26.9% / 0.75 (smooth plateau).
Gates: B1 PASS (p=0.005 all windows), B2 PASS (p=0.010 full; 0.124 in half B), **B3 FAIL (p=0.149)**, B4 PASS both directions (OOS/IS Sharpe 0.87 / 1.14, MaxDD 0.83x / 1.21x), B5 PASS (Sharpe swing <= 0.05), B6 PASS (0.6%/side: Sharpe 1.31, CAGR 17.7% vs EW-pool 13.7%),
B7 PASS (ex-best-3-years Sharpe 1.01, CAGR 12.9%; top-10 episodes 13% of positive P&L), B8 PASS (-23.3% vs EW-pool -38.6%; Calmar 0.82 vs Zenith 0.39), B9 PASS (rho 0.82 vs faithful trio; break-even 1.41 > 0.69; 20-30% blend lifts trio Sharpe 0.85 -> 1.00-1.07 and MaxDD -37% -> -30..-32%),
B10 PASS (DSR ~1.0; weak test because trial cells are highly correlated). Delay test: Sharpe 1.41 / 1.42 / 1.37 / 1.30 / 1.17 / 0.85 / 0.69 for 0 / 1 / 2 / 3 / 6 / 9 / 12 months late - monotone decay, the signal is slow.
Verdict by the pre-registered rules: 9/10 gates, only B3 failing; kill rule (B1, B2, B4, B9) did NOT fire. Not a clean PASS.

### 8.6 Honest limits (read before using any number)
* The industry-specific part of the edge is small (+0.08..0.10 Sharpe; B3 fails). The headline is mostly construction + risk overlay. Do not describe this as "sector rotation works".
* No lockbox: every month was seen by the signal studies; halves are consistency checks. D1v's overlay was chosen after seeing D1's -43% (1 of 2 allowed post-look changes used). Only forward paper trading is real out-of-sample.
* Survivorship (only ~56 of 5,205 files end before 2026), static current-day industry labels, 2005-12 trades on far fewer names (288 files by 2003, ~1,600 by 2008, ~4,500 later) and thin historical volume: at Rs 10 cr AUM the median monthly trade is 6.8% of ADV in 2005-12 but 0.3% in 2023-26; only 2.7% of 2023-26 trades exceed 5% of ADV (10% at Rs 25 cr).
* Recent record is weak: 2024 +17.3%, 2025 -4.9%, 2026 YTD +0.7% (2024-26 CAGR 4.8%, Sharpe 0.42), though the faithful trio lost 9.3%/yr over the same span. Ex-best-3-years (2014, 2007, 2023) CAGR 12.9%. It lags the broad EW index in violent bull years (2009, 2021).
* Typical drawdowns of 20-25% still occur every few years (2006, 2008, 2011). Under faithful accounting nothing here reaches the engine-booked "-12..-16%".

### 8.7 Independent verification (4 agents + referee) and corrections - TRUST RATING: MEDIUM
Blind re-implementation from the spec, a holdings-based re-simulation, a look-ahead/accounting audit and a bridge test against the faithful engine replay. Outcome:
* **Numbers confirmed**: blind CAGR 20.65% (calendar-year basis; 21.05% on the 252-day convention), Sharpe 1.243, MaxDD -43.02%; daily-return correlation with the repo simulator 0.99995; terminal NAV within 0.4%. End-to-end truncation tests
  (rebuild factors, universes and book from panels cut at 2009-11, 2012-06, 2016-03, 2019-12, 2023-06) give a difference of exactly 0.0; deliberate future-information controls explode the result (CAGR 27-113%), so the harness would catch leakage. No accounting or look-ahead bug.
  One fix applied: monthly returns now use the last traded price (a stale name no longer gets a phantom 0% month; 2 of 258 cohorts, +0.4% NAV; all stage21/22 results re-run, conclusions unchanged).
* **CORRECTION - D1 is NOT shown to beat the live engines like-for-like.** The faithful Zenith 12.4% depends on the engine backtest's resting-stop fill (trigger on the intraday low, fill at stop x 0.997). Imposing that same stop convention on D1 gives 13.2% / Sharpe 1.20 / MaxDD -25.0%
  (parity with Zenith); with close-breach / next-open exits D1 gives 19.1% / 1.49 / -27.7% against the engine's 18.2-19.2% / 1.40 / -28..-31% (also parity). csm_value/AUDIT.md itself notes the live rule is close-based with next-open exit, so the '7-12% live engines' reference is uncertain by ~6 points.
  Earlier statements in this file/session that D1 'beats the live engines by 2x' should be read as 'D1 without stops vs engines with resting stops'.
* **Attribution**: ~18.5-19% of the 21% is the harness baseline (even an equal-weight U2 book earns 18.5%; random-stock books 19.0%; random-industry books 18.1-18.6%). The industry rank is worth ~+2.4 pt CAGR / +0.06 Sharpe over random industries (D1 beats 20/20 placebos),
  but the gain over the EW pool is not firm in CAGR (paired block-bootstrap P(diff<=0) = 12%; Sharpe diff P = 0.2%) and is FRONT-LOADED: +4.3 pt CAGR in 2005-2013, +1.1 in 2014-26, +0.3 in 2016-26, -1.4 in 2020-26; 2014/2007/2017 supply 43% of total log return.
  The MaxDD cut vs EW (-43% vs -55%) comes from the positive-trend-industry filter and cash (random-industry books also show -41%), not from ranking.
* **Level haircuts** (referee estimates, not measured): survivors-only panel (named failures such as Satyam, DHFL, Jet, Educomp, Gitanjali are absent) -0.5..-3 pt; static 2026 labels and label-availability hindsight (D1 can only buy the 2,749 labelled names; unlabelled U2 names earned 5.5% EW) ~-0.6 pt;
  cash credited at 6.5% on ~28% of capital is worth +2.1 pt (cash 0%: 19.0% / Sharpe 1.14; Sharpe at rf 6.5% is 0.86-0.88); 252-day vs ~248 trading-day convention -0.4 pt; flat 0.3% costs with no impact (0.6%/side: 19.8% / 1.18). Reasonable planning range for D1: CAGR ~14-17%.
  Reference points from real indices over the same window (price only): Nifty 500 12.3%, Midcap150 15.2%, Nifty200 Momentum30 16.9%, Midcap150 Momentum50 20.8% (MaxDD -73%).
* The simulator books ~4-5 pt more than the faithful replay on identical monthly weights of a 15-name book (only ~1.3 pt explained by constant-weight booking, 0.4-1.1 pt by locked-circuit exits); D1's exposure to that is inferred <= 1-1.5 pt (4.3x lower turnover). D1 has NOT been run through the actual replay executor (`csm_value/execution_replay.py`) - open item.

### 8.8 Verdict and what is open
* Pre-registered verdict: D1 FAIL (B3 shuffled-label p=0.20; B4 Split-B fails because of 2008 - true of every long-only book here). D1v (D1 + chassis vol-target, post-look modification #1) passes 9 of 10 gates, fails B3 (p=0.158), kill rule did not fire.
* Plain-language conclusion: **industry momentum is a real but modest, front-loaded effect (~2 pt/yr); a slow, staggered, industry-capped, vol-targeted book is a sound, diversified construction that matches (not beats) the live engines under identical exits, with MaxDD ~-23..-28% in the simulator.
  It is not evidence that 'sector rotation' is a high-alpha source.** Certainty is not achievable: no lockbox exists; forward paper trading (Playbook stage 6, >= 6 monthly cohorts) is the only real out-of-sample.
* Needs user decision/sign-off: (1) the Appendix-C override for G1(c); (2) which stop-fill model matches live fills (moves every engine benchmark by ~6 pt); (3) run D1/D1v weights through `execution_replay.py`; (4) whether to build a strategy class (JT-tranche chassis) and paper-trade it.

## 9. Why the earlier sector/industry strategies failed (2026-10-10)
Consolidated in `SECTOR_STRATEGY_FAILURE_ANALYSIS.md`: six discarded families audited (gate/quota/breadth/Meridian/colleague factor book), seven stacked causes - (A) 11 sector buckets that behave like one factor
(PC1 = 89% of variance, mean corr 0.87, ~7 relative bets) and are very unequal in size (Industrials/Consumer Cyclical/Basic Materials = 57% of U1 names; Utilities/Energy/Real Estate/Communication 16-28 names each; 5-6 of 11
sectors have < 30 names in the SMA200 trend pool), (B) sector index built from ~5,000 untradable tickers, (C) gates/quotas on thin pools -> 35-55% invested with cash at 0%, (D) shared chassis pins return correlation to the
live engines at 0.78-0.83, (E) engine-booked / cost-free / rf=0 / single-window evaluation, (F) data bugs and static labels, (G) a real but small signal that never converted IC into book P&L. Includes a design checklist.

### 9.1 Industry name-cap inside the live engines - cut (2026-10-12)
Pre-registered (`INDUSTRY_CAP_PREREG.md`), run natively in `csm_industry_cap/` with the live Zenith/Elendel classes unmodified (parity exact at cap off). At most 2 names per Industry_clean: binds in ~50% of months but
return correlation to base is 0.98, dSharpe -0.02..-0.08 (Elendel 2015+ +0.03), Elendel MaxDD 3-4 pts WORSE, and shuffled-label placebos do as well. Cut. The standalone book's drawdown profile is its construction, not a cap.

### 9.2 D1v implemented as a strategy class (2026-10-12)
`csm_industry/industry_book_strategy.py::CSMIndustryBook` - self-contained, parity-tested against the research simulator (identical cohorts and daily returns). Next: gold/silver ETF overlay sub-version (pre-registered), paper trading.

### 9.3 Zenith base, universe robustness, worth-it control (2026-10-12) - `INDUSTRY_BOOK_PREREG.md` section 7, `stage23_zenith_universe.py`
D1v with the Zenith composite as in-industry score (post-look #2, spec now frozen): 20.6% / Sharpe 1.50 / MaxDD -22.2% standalone; rho 0.75 with faithful Zenith; 30% blend with Zenith: Sharpe +0.14/+0.27, MaxDD +3.6/+5.1 pt (halves).
Worth-it control FAILED: a no-industry staggered Zenith-score book gives about the same blend benefit; industry ranking beats random industries only in broad universes (>= 1000 names; p=0.00) and not in top-300 (p=0.57). Universes 1-300..1-2000 all beat their EW pool; 1-1000 kept.
Blend benefit flips sign if Zenith's engine-booked Sharpe (2.37) were true; break-even Zenith Sharpe ~2.0. Conclusion: not worth it as sector rotation; the staggered/trend-gated/industry-diversified construction is the useful part.

# Gold / silver ETFs for Crestline's idle capital (2026-10-13)

Protocol `PREREG_GOLD.md` (fixed before any gold number). Code: `make_gold_lab.py` -> `crestline_gold_lab.py` (defaults == v2.4 bit-exact; `test_gold_lab.py` 7/7 pass: parity, daily dump, regime flags unchanged by ETFs, no ETF trade in the data gap or before eligibility, drift placebo brings GOLDBEES to the 6.5% liquid-fund rate, truncation/no-look-ahead), `gold_common.py`, `gold_part0.py`, `gold_sleeve_study.py`, `experiments_gold.py`. Raw: `gold_sleeve_raw.csv`, `gold_sleeve_gates.csv`, `results_gold_engine.csv`, `gold_*_out.txt`.
Base = v2.4, 6 anchors, 2006-25, idle cash in a 6.5% liquid fund (G0). Book sizes 1 lakh (c0) / 1 cr / 5 cr / 20 cr. Data caveats: every gold/silver ETF file is empty for 2011-2014 (sleeve is out then; no forward-fill), silver starts 2022-02, GOLDBEES was below the Rs 20 floor until ~2010.

## Part 0 - the premise: gold really is decorrelated (and more so than you quoted)
* Daily correlation of GOLDBEES with the equal-weight stock index -0.05 (2007-10 -0.04; 2015-25 -0.06; 2020-25 0.00); weekly -0.06; monthly -0.14; with the Crestline book -0.01 daily / -0.12 monthly. Rolling 1-year daily correlation: min -0.30, median -0.06, max +0.21, never above +0.3.
* By engine regime: bear days corr -0.17 (gold +19.5%/yr while the market fell -8%), other days -0.01, panic days +0.17 (103 days; gold +35%/yr, vol 27%, market -52%/yr).
* Worst stock-index drawdowns (peak -> trough): 2008-01..2009-03 market -72%, gold +32%, book -27%; 2018-02..2020-03 market -60%, gold +34%, book +1%; 2016-01..02 market -18%, gold +12%, book -2%; 2022-02..06 market -17%, gold +4%, book -10%.
* Silver (2022-02..2025 only): correlation 0.07 with stocks but 0.71 with gold; +35%/yr, vol 24%. Not independent evidence.
So the diversification premise is TRUE. The question is whether it converts into a better portfolio.

## Part A - sleeve funded by idle cash (post-processing of the engine's daily output)
Gold weight = idle fraction (previous close) x multiplier, 2% dead band, 0.15% cost one way. G0 baseline by book size: CAGR 18.8 / 13.9 / 11.2 / 9.3%, Sh65 1.13 / 0.86 / 0.70 / 0.57.
Sh65 change vs G0 (real drift | half drift | ZERO drift), MaxDD change in pts, average gold weight:
| variant | 1 lakh | 1 cr | 5 cr | 20 cr | MaxDD effect | avg gold wt (1 lakh -> 20 cr) |
|---|---|---|---|---|---|---|
| G1 static half of idle | +.10 / +.02 / -.06 | +.14 / +.03 / -.09 | +.18 / +.02 / -.14 | +.21 / +.01 / -.19 | ~0 (+0.2 .. -1.8) | 18% -> 29% |
| G2 idle x gold above SMA200 | +.04 / -.07 / -.18 | +.07 / -.07 / -.21 | +.09 / -.08 / -.25 | +.12 / -.08 / -.27 | **-6 .. -15 pts worse** | 27% -> 42% |
| G3 idle x persistence >= 0.5 | +.04 / -.06 / -.16 | +.08 / -.05 / -.18 | +.10 / -.06 / -.22 | +.14 / -.05 / -.23 | -6 .. -15 worse | 26% -> 39% |
| G4 trend x (1.0 bear/panic, 0.5 else) | +.02 / -.07 / -.16 | +.04 / -.07 / -.18 | +.05 / -.08 / -.21 | +.08 / -.08 / -.24 | -7 .. -15 worse | 21% -> 30% |
| G5 trend, bear/panic only | **-.03** / -.09 / -.15 | -.03 / -.10 / -.17 | -.03 / -.12 / -.20 | -.03 / -.13 / -.23 | -9 .. -15 worse | 14% -> 18% |
| **G6 trend, capped 10% of equity** | +.05 / +.02 / -.00 | +.06 / +.03 / -.01 | +.08 / +.04 / -.01 | **+.10 / +.05 / -.01** | ~0 | 5.0% -> 5.4% |
Pre-registered adoption (real-drift dSh >= +0.08, both periods positive, >= 5/6 anchors, MaxDD within 3 pts, half-drift >= +0.03, zero-drift >= -0.01, still positive at 0.30% cost): **exactly one cell passes: G6 at the 20 cr book** (+0.10; periods +0.07 / +0.13; 6/6; MaxDD +0.1; half +0.05; zero -0.006; cost 0.30% +0.09). G6 at 5 cr just misses the first bar (+0.076), at 1 cr and 1 lakh it is +0.06 / +0.05. CAGR effect of G6: +0.65 pts at every size.
What the table says:
1. **Every large-gold variant is a bet on gold beating the liquid fund, not a diversifier.** With gold's excess drift set to zero all of G1-G5 LOSE Sharpe (-0.06 to -0.27): swapping a riskless 6.5% asset for a risky asset with the same expected return adds variance with nothing to pay for it. Under the real 2015-25 drift (gold ~17%/yr in INR vs 6.5%) they look good (+0.04 to +0.21).
2. **Nothing reduces the drawdown, and the trend/regime versions make it worse** (6-15 pts): the book's drawdowns are dominated by its stock holdings; gold's own drawdowns and whipsaws add to them. This replicates the earlier momentum_gold study on the old engines.
3. **Your regime intuition is partly supported but not stable.** Gold's excess return over cash on bear/panic days was +15-17%/yr in 2015-25 vs +6-9% on other days - and +2% (with 25% volatility and -8% days) in 2007-10 vs +17-21% otherwise. G5 (gold only in bear/panic) therefore helps in 2015-25 (+0.15..+0.21 real drift) but hurts in 2007-10 (-0.27..-0.32), so it fails across periods and also under the placebo. The regime flag (benchmark < SMA200) flags 28% of days and 64% of the book's worst-10% drawdown days, but it is a lagging flag and gold's behaviour on those days is not consistent.
4. Capacity: G6 at 20 cr holds ~5% of equity (~Rs 1 cr) in GOLDBEES, trivial against Rs 65 cr/day; G1-type 25-30% weights at 20 cr (Rs 6 cr) would need splitting across GOLDBEES / GOLDIETF / SETFGOLD / HDFCGOLD.
Silver (2022-02..2025, descriptive): the book was weak (Sh65 0.37-0.47). A silver sleeve shows the same pattern as gold - large real-drift gains (G2 +0.56..+0.64 Sh65, +11.7..+14.3 CAGR), zero-drift -0.08..-0.26; capped G6 is the only version that is neutral at zero drift (+0.01..+0.02). Silver adds no information beyond gold (0.71 correlation, 3.9 years).

## Part B - gold/silver in the core ranking (same z-score, ranks, stops)
Added GOLDBEES (+ SILVERBEES) as ordinary columns (eligible only after 240 genuine observations in 252 bars; excluded from the benchmark). They almost never rank in the stock top-25: 14-18 ETF trades in 20 years across six anchors, first in Feb 2020 (the price floor and the data gap exclude 2007-2015). Sharpe change -0.005 to -0.007 (real drift) and +0.002 (zero drift), CAGR -0.1 .. +0.02, MaxDD 0.0, at 1 lakh and 1 cr. **No effect and nothing passes.** The ranking is built from stocks' 52-week-high proximity and trend persistence; an ETF competes with ~700 stocks and rarely wins a slot, so this route does not use idle capital at all.

## Verdict
* Approach 1 (gold in the ranking): cut - no effect.
* Approach 2 (sleeve): only the capped trend sleeve (G6: gold = min(idle cash x [gold above SMA200], 10% of equity), rest in the liquid fund) passes, and only at a ~20 cr book; it is neutral if gold's drift disappears (-0.006) and +0.05..+0.10 Sharpe with the 2015-25 drift. Its realistic planning value is about +0.65 CAGR points and +0.03..+0.05 Sharpe (half-drift), with no change in drawdown. Larger or more regime-driven gold weights are cut: they only pay if gold keeps beating cash by ~9 points a year, and they deepen drawdowns.
* What gold does NOT do here: reduce the book's drawdown. The idle cash is already earning 6.5% at no risk; gold must out-earn that to add value, and the data cannot say it will.

## Limits
One gold bull market in the usable sample (2015-25), 2011-14 unobserved, January-2026-type gap days; the 20 cr pass is one cell of 24 (expect ~1 spurious pass; it sits on a monotone size gradient: +0.05 / +0.06 / +0.08 / +0.10); post-processing assumes a same-day sleeve sale funds stock entries and uses close-to-close gold returns; taxes on ETF churn not modelled; in-sample, no lockbox.

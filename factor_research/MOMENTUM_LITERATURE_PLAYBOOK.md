# Momentum-literature playbook: what the 61 papers in `momentum/` give us for new strategies

Written 2026-10-06. Everything below was tested on your data; nothing in `Old_live_strategies/` was touched.
Scripts: `factor_research/stage15*.py`, `stage16_literature_quick.py`, and `momentum_value/` (real-engine runs).

## 1. Short answer

The literature's most useful message for *your* situation is not another price-momentum variant (you already own the best ones).
It is: **momentum is weakly related to fundamentals-based signals, and mixing them improves both** (Asness 1997, Griffin–Ji–Martin 2005, Novy-Marx 2012,
Sadka 2006). Your OHLCV-only research could never test that. You also have point-in-time quarterly results with `filed_date`
(`upstox_data_folder/pit_harness/cache/facts_quarterly.parquet`, ~2,000 symbols, results for 2018Q1–2024Q4), which can.

| # | Idea (source) | Verdict on your data | Use |
|---|---|---|---|
| 1 | **Value × momentum**: add earnings yield (E/P) to the momentum score (Asness 1997; Asness–Moskowitz–Pedersen) | **Works in Zenith and Quad, not in Elendel.** Real engines, 2019-06→2025-06: Zenith +9.5 pt CAGR / Sharpe +0.46; Quad +4 to +7 pt / +0.23 to +0.40; Elendel −0.5 to +0.9 pt / ≈0 | **Lead idea — build as Zenith-V and Quad-V** |
| 2 | **Post-earnings-announcement drift as an event strategy** (Sadka 2006; CJL 1996) | Good news *confirmed by price* earns **+3.0% excess over 60 days (t 2.8, both sub-periods positive)**; bad news −2.6% (t −4.8). Win-rate only 49% — a skew strategy | **Second idea — new, structurally different sleeve** |
| 3 | Earnings-surprise / margin-change as extra *ranking* terms (Novy-Marx fundamental momentum) | Real IC (0.04–0.06, t 3–4), only 0.27–0.34 correlated with Elendel — but **no improvement in the top-15 book** | Do not add to the score; use as the PEAD trigger or an exclusion screen |
| 4 | Momentum-crash / vol scaling of exposure (Daniel–Moskowitz; Barroso–Santa-Clara; HMM turbulence) | **No increment** on the real engines (Sharpe 1.80 vs 1.81 etc.). Your engines already carry regime scaling, a 20% vol target and Crash Guard | Skip |
| 5 | Long-run (3–5 y) reversal combined with momentum (Balvers–Wu) | **Nothing**: IC3 ≈ 0 (t < 1) in this market | Skip |
| 6 | Information discreteness / "frog in the pan", vol-normalised momentum, intermediate (12-7) momentum, residual momentum, volume-conditioned momentum, industry momentum | Already covered by earlier stages (`FINDINGS.md`: tiers B–D). Smooth-path and residual variants are in the live family; volume confirmation was rejected | No new strategy |
| 7 | Within-industry residual reversal, analyst-revision momentum, liquidity-risk beta, 13F crowding, factor momentum on fundamentals | **Not testable**: no sector map, no I/B/E/S, no intraday data, no holdings data | Needs data first |

## 2. Idea 1 — value × momentum (the lead)

**Why the literature predicts it.** Value and momentum are negatively correlated across stocks, so each hides the other (Asness 1997); adding value to a
momentum rank buys the cheap end of the winners. Novy-Marx and Griffin et al. show the earnings side of this is distinct from price.

**Signal (point-in-time).** E/P = TTM net profit / (price × latest shares outstanding). A quarter becomes usable on its `filed_date`, expires after
140 days, loss-makers get negative E/P (ranked last). Variants — EPS/price, sales/market-cap, EBIT/market-cap, book/market-cap — all behave the same way.

**Signal quality (liquid-1000 universe, 61 monthly signals 2020-06→2025-03):**

| | IC 3m | ICIR | hit | IC 6m | IC 12m | corr. with Elendel |
|---|---|---|---|---|---|---|
| E/P (EPS) | 0.046 | 0.53 | 72% | 0.063 | 0.083 (hit 93%) | 0.02 |
| E/P (net profit/mcap) | 0.047 | – | 72% | 0.067 | 0.089 (hit 95%) | – |
| Sales/price | 0.066 | – | 79% | 0.096 | 0.130 | – |
| Elendel base (same dates) | 0.059 | 0.53 | 70% | 0.091 | – | – |

E/P is the only signal tested in this whole project that is both significant and ~uncorrelated with the live books.

**Proxy top-15 books (same names, same dates; z(base) + w·z(E/P)):** Sharpe 1.00 → 1.65 (w 0.5, paired t 3.0) in U1; the combined book beat the base book
in every calendar year 2020–2025 (+16, +15, +12, +34, +26, +4 pts). Block-bootstrap of the monthly paired difference: P(>0) = 1.00.

**Real engines (unmodified engines; only the monthly score replaced by z(base) + w·z(E/P); stops, regimes, vol target, 0.3% cost as live):**

| 2019-06 → 2025-06 | Base CAGR / Sharpe / MaxDD | w = 0.5 | w = 1.0 | EPS-based, w = 0.5 |
|---|---|---|---|---|
| **Zenith** | 35.6% / 1.97 / −11.9% | +9.5 pt / +0.46 / −0.7 pt | +9.1 / +0.46 / −0.9 | +12.8 / +0.61 / −1.1 |
| **Quad** | 25.4% / 1.29 / −15.9% | +4.1 / +0.23 / 0.0 | +7.3 / +0.40 / +0.8 | +4.3 / +0.23 / 0.0 |
| **Elendel** | 44.0% / 2.20 / −12.8% | −0.5 / −0.01 / −1.5 | +0.9 / +0.09 / −1.5 | +3.2 / +0.18 / −0.2 |

Bootstrap on daily differences: Zenith P(excess > 0) 0.98–1.00 (5th percentile of annual excess +1.2 to +4.3 pts); Quad 0.91–0.99; Elendel 0.44–0.74 (no evidence).
Zenith was better in all 7 calendar years at w = 0.5; Quad in 6 of 7; Elendel lost 20 pts in 2021.

**Where it works.** By liquidity rank (proxy book, w 0.5): ranks 1–300 — no effect (Sharpe 1.39 → 1.23, t −0.7); ranks 301–600 — strongest (1.29 → 1.67, t 2.7);
ranks 601–1000 — 1.02 → 1.28 (t 1.6). That matches why Quad (rank 500–1000) benefits and why a top-300 version is pointless.

**Why I do not trust the absolute size yet — read this before building:**
* **Six years, one regime.** 2020–23 was a cyclical/PSU/commodity-value rally in India. The picks' median E/P was 21.7% (P/E ≈ 4.6) against 3.8% for the base book — extremely cheap names. A regime that punishes cheap cyclicals would hurt; nothing here tests that.
* **Survivorship.** Only currently listed companies have both prices and fundamentals. Cheap stocks that died are missing; a cheap-stock effect is flattered more than a momentum one.
* **Coverage and freshness.** The fundamentals file ends with 2024Q4 results (filed ~Feb 2025); E/P coverage falls to 826 names in 2025 and is gone afterwards. **A live version needs a refreshed quarterly results feed first** (`fetch_fundamentals_and_fo_samples.py` is the starting point).
* Elendel gets nothing, which is itself informative: its RS-line + Q5 score already holds most of what E/P adds in the large-liquid names.
* Four variants per engine were run; weights 0.5/1.0 were pre-declared, but the choice to carry the net-profit version forward was made after seeing both.

**Planning expectation (judgemental haircut, not a measurement):** keep roughly a third to a half of the measured gain —
**Zenith ≈ +3 to +5 pts CAGR, Sharpe +0.15 to +0.25; Quad ≈ +2 to +4 pts, Sharpe +0.10 to +0.20; drawdown ≈ unchanged.** Treat Elendel as +0.

## 3. Idea 2 — post-earnings drift event sleeve (new, different return stream)

Entries are triggered by each company's own filing date rather than a month-end ranking, so the book is spread across the calendar.

Test: every liquid-universe filing (16,856 events, 2020-06→2025-03); entry at the close of the 3rd trading day after the filing (the announcement reaction
is already known); excess = stock minus equal-weight liquid universe; t-stats clustered by filing month.

| Event set (ranked within filing month) | Events | Excess 20d | Excess 60d | t (60d) | Win 60d | 2020-22 / 2023+ (60d) |
|---|---|---|---|---|---|---|
| All filings | 16,856 | −0.0% | +0.1% | −0.2 | 42% | +0.1 / +0.1 |
| Earnings surprise top 30% | 3,945 | +0.4 | +1.7 | 1.3 | 46% | +2.0 / +1.4 |
| Announcement return top 30% | 5,083 | +0.8 | +1.7 | 0.9 | 46% | +2.3 / +1.0 |
| **Surprise AND announcement return top 30%** | 1,681 | **+1.5** | **+3.1** | **2.8** | 49% | **+3.6 / +2.6** |
| …plus EBIT-margin change top 40% | 1,955 | +1.1 | +3.3 | 3.1 | 48% | +4.1 / +2.6 |
| Surprise top 30% but price did not confirm | 1,472 | −0.8 | +0.6 | −0.7 | 43% | +0.4 / +0.7 |
| **Bad news: both bottom 30%** | 1,559 | −0.4 | −2.6 | −4.8 | 35% | −2.8 / −2.4 |

* The edge needs **both** conditions; an earnings beat that the market ignored earns nothing — the same "filter, not signal" pattern as the breakout study.
* Median excess is negative even for the good set (−0.5% at 60d): it is a skew strategy that wins by size, ~49% of the time. Expect streaky months.
* The bad-news result is a **screen**: use it to veto names in the momentum books around results, since the book is long-only.
* This is an event study, not a strategy backtest — no position limits, stops, costs beyond the entry day, or capacity yet. About 29 qualifying events a month.
* Same survivorship and 5-year-window caveats as above.

## 4. What did not work, and why that is still useful

* **Fundamental momentum as extra score terms** (SUE, margin change, growth, announcement return): IC is genuine, but IC rewards the whole cross-section; a 15-name book lives in the tail. Paired differences in the top-15 book: −0.5 to +0.2 pts/month, |t| ≤ 1.2. Same lesson as the low-risk family in `FINDINGS.md`: *rank IC ≠ book improvement*.
* **Own-vol targeting and Daniel–Moskowitz crash state** on engine returns (2005+): Elendel Sharpe 1.81 → 1.77–1.81, Zenith 1.87 → 1.86–1.87, Quad 1.67 → 1.65–1.67, with MaxDD moves of at most 1.4 pts (Elendel). The live engines already absorb this.
* **Long-run reversal / "cheap in price"**: 60-12m and 36-12m reversal have IC3 ≈ 0; far-from-3-year-high is simply the opposite of the 52-week-high factor (IC −0.09, corr −0.72 with Elendel).
* **Gold overlay**: see `momentum_gold/README.md` — a ~+0.4 pt, drawdown-neutral add-on. The value tilt above is a larger lever than anything found there.

## 5. Implementation plan

1. **Data (prerequisite, 1–2 days).** Refresh quarterly results to the latest quarter with `filed_date`; keep the point-in-time rule (usable from filing date; expire after 140 days; missing = neutral z of 0). Without this nothing below can go live.
2. **Zenith-V / Quad-V (first build).** One new term in `calculate_factors`: `z(base) + 0.5 · z(E/P)`. No other engine change. Reproduce the `momentum_value/` runs in the live codebase, then paper-trade. Run Quad-V first-class (rank 500–1000 is where it works). Skip Elendel.
   * Kill/review: drop the tilt if over any rolling 12 months Zenith-V trails Zenith by more than 5 pts, or if the picks' median P/E stays under ~6 for a year (cyclical-peak crowding).
3. **PEAD event sleeve (second build, after 1).** Full event-driven backtest on the existing chassis: liquid universe, surprise ∩ announcement-return filter, 40–60 day hold, ATR stop, ≤ 5% per name, costs both sides, capacity at ≤ 5% ADV. Decide only after seeing drawdown and win-streak behaviour, not the mean.
4. **Veto screen** for existing books: skip entries when the latest result is in the "bad news" set. Cheap, low-risk; measure separately.
5. **Needs new data to try**: sector map (within-industry reversal, industry momentum), analyst revisions, intraday liquidity.

## 6. Second pass (same day): what else the folder offered

Scripts: `stage17_more_literature.py` (price-only, 2003–2026), `momentum_value/run_universe_engines.py` (real engines, unmodified).

| Idea (source) | Result | Verdict |
|---|---|---|
| **Liquidity-tier / size effect** (Hong–Lim–Stein 2000; Griffin et al. 2005) | Elendel-score IC3 by liquidity rank: 1–300 **0.081**, 301–600 **0.107** (ICIR 0.72), 601–1000 0.092, 1001–1500 0.060, 1501–2000 0.045. Real engines with the top-300 megacaps excluded (universe 301–1000), 2005+ Sharpe: Elendel 1.81 → **2.08**, Zenith 1.87 → **2.53**, Quad 1.67 → **1.88**. 2015+: Elendel 1.66 → 1.74, Zenith 1.48 → **2.15** (CAGR 25.8% → 36.3%), Quad 1.42 → 1.40 | **Real, and a universe change only — no new signal.** Biggest effect in Zenith |
| Universe below rank 1000 (1001–2000) | Engine Sharpe 2015+ of 2.2–3.2 (Zenith 3.0–3.2) | **Do not use.** Median daily traded value is ~₹5 cr at rank 1000 and ~₹1 cr at rank 1500 (2026-06); a 5%-weight book is limited to roughly ₹1–5 cr, and survivorship (dead small caps missing) is worst here |
| Aggregate-illiquidity state (Avramov–Cheng–Hameed 2016) | Direction matches the paper in the proxy book (high-illiquidity months: Sharpe 0.24 vs 0.78, IC3 0.054 vs 0.094; only 39 months). But halving exposure in that state on the real engines changes Sharpe by 0 to −0.04 (MaxDD ±1 pt) | Skip: engines already absorb it |
| Dispersion state (du Plessis 2013) | High-dispersion months were the **best** for the book; halving exposure then costs 0.05–0.13 Sharpe | Skip |
| Factor momentum (Ehsani–Linnainmaa 2017): follow the factors that worked over 12 months, 122 factors | IC3 0.05–0.07 (t 3.7–5.0), but top-15 book Sharpe 0.48–0.72 vs 0.80 for plain Elendel (paired t −0.2 to −2.0). It mostly re-picks the momentum factors | Skip |
| Inverse-vol weighting, robust optimisation (Vol-weighting 2017; Robust Optimization 2009) | Already in the live engines (inverse-vol weights, caps, hysteresis) | Nothing to add |
| HMM turbulence filter (Daniel–Jagannathan–Kim 2012) | `hmmlearn` not installed; the simpler crash-state rule (stage16) gave nothing and the engines have PANIC/HIGH_VOL regimes | Low expected value; not run |
| Rebalance timing / mid-month (Nomura 2009) | Needs an engine change (offset or tranche rebalance); cannot be tested on month-end factor frames | Untested, cheap to try in the engine if you want it |
| Industry momentum, within-industry reversal, lead-lag, crowding, analyst revisions | Need a sector map, analyst data or holdings data you do not have | Needs data |
| Time-series momentum on indices/ETFs, carry (currencies), country rotation | Earlier stages covered index/ETF timing; currency carry does not apply to a long-only NSE book | Nothing new |

**What to take from it:** excluding the top-300 names is a no-new-code lever worth a proper test on Zenith (and Elendel), and it fits the earlier finding that
E/P works best at liquidity ranks 301–600. The two together (Zenith, universe 301–1000, + 0.5·E/P) is the natural next experiment; I have not run it. Capacity falls
from roughly ₹6–11 cr (median) in the live universe to under ₹1 cr per the history-averaged measure, but that measure is distorted: volume in the data before ~2020 looks
far thinner than today (rank-300 daily value ₹3 cr in 2019-12 vs ₹39 cr in 2023-12), so use the 2026 figures above for sizing.

## 7. Caveats that apply to every number here

* One window (2019/2020 → 2025), one regime; 58–61 monthly signals. Bootstrap CIs are sampling statements about that window, not about other markets.
* Survivorship (98 of 5,205 price files end before mid-2026; fundamentals only for current names).
* Selection: ~15 fundamental signals and 4 engine variants were looked at; the headline (E/P) was one of three pre-declared signal families, but weights and the variant carried forward were chosen with the results visible.
* The proxy books are equal-weight, no stops; the engine runs are the realistic ones.
* Engine idle cash earns 0% in the Elendel/Quad backtests (as in the live runners), so absolute CAGRs are conservative; the deltas are unaffected.

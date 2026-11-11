# CSM Aegis validation summary

**Overall verdict: performance gates pass; validation remains incomplete.** The independent IS/OOS comparison passes in both directions, the 2015–2025 core universe dispersion checks pass, and the 3-month equity signal clears its stated IC gate. Exit diagnostics support the market gate, rank rotation, trailing stop, and time stop, but flag the entry stop as potentially too early or tight. The data survivorship check fails, value-weighted IC is weak, and the wider liquidity band performs slightly better without a cost stress run. These findings need resolution before treating the backtest as a deployment result.

The runs use the `v1.4_low_dd` preset, `R1_ULCER` selector, GOLDBEES idle-cash sleeve, and **0.30% transaction cost per leg**. Signal diagnostics and the universe sweep evaluate **2015–2025**. IS/OOS runs **2005–2014** and **2015–2025** as separate, flat-start backtests. Earlier loaded dates warm up indicators and are excluded from reported performance.

## Universe sweep: 2015–2025

| Liquidity universe | CAGR | Sharpe | Max drawdown | Calmar | 3m IC NW-t | Median equity pool | Months with pool <30 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Top 100 | 17.36% | 1.28 | −15.96% | 1.09 | 1.13 | 49 | 4.55% |
| Top 250 | 19.27% | 1.43 | −16.42% | 1.17 | 2.03 | 118 | 0.76% |
| Top 500 | 20.04% | 1.43 | −20.35% | 0.98 | 2.38 | 227 | 0% |
| Top 750 | 22.28% | 1.54 | −19.95% | 1.12 | 2.21 | 323 | 0% |
| Top 1000 | 23.44% | 1.62 | −19.43% | 1.21 | 2.40 | 408 | 0% |
| Top 1500 | 24.47% | 1.69 | −18.92% | 1.29 | 2.34 | 523 | 0% |
| Ranks 501–1000 | 21.39% | 1.51 | −16.90% | 1.27 | 2.94 | 180 | 0.76% |
| Ranks 1001–1500 | 24.70% | 1.69 | −19.54% | 1.26 | 2.05 | 115 | 10.61% |

The **top 250–1500 core set passes all four dispersion limits**: Sharpe range 0.27 (limit 0.35), Calmar range 0.31 (limit 0.50), CAGR range 5.20 percentage points (limit 8), and max-drawdown range 3.93 points (limit 10). The lowest core 3-month IC NW-t is 2.03. This supports breadth across the tested bands at the modeled cost.

The ranks 1001–1500 band returns **24.70% CAGR and 1.69 Sharpe**, slightly above the top-1000 result (**23.44%, 1.62**), while its 3-month IC is lower (**0.0298 vs 0.0408**) and its pool falls below 30 names in **10.61%** of months. The script's 25% Sharpe red-flag threshold does not trigger, but the result still warrants capacity and higher-cost testing. **Only the base 0.30% cost was run; cost-stress robustness has not been established.** [Sweep report](output/validation/universe_sweep_summary.md) · [raw results](output/validation/universe_sweep_results.csv) · [dispersion](output/validation/universe_sweep_dispersion.csv)

## Independent IS/OOS comparison

| Metric | IS, 2005–2014 | OOS, 2015–2025 |
|---|---:|---:|
| CAGR | 26.34% | 23.44% |
| Sharpe | 1.73 | 1.62 |
| Calmar | 1.49 | 1.21 |
| Max drawdown | −17.70% | −19.43% |
| 3m L0 IC NW-t | 4.47 | 4.62 |
| 3m tradeable-pool IC NW-t | 3.17 | 2.40 |
| Stock win rate | 60.92% | 50.70% |
| Stock profit factor | 5.05 | 2.89 |
| One-way turnover | 3.9×/year | 6.4×/year |

**Split A passes every stated gate:** OOS/IS Sharpe 94% (minimum 60%), Calmar 81% (minimum 60%), CAGR 89% (minimum 50%), max-drawdown ratio 1.10× (maximum 1.50×), positive OOS Sharpe, and both OOS IC NW-t values above 1.5. The reverse-period Split B also passes. OOS includes five benchmark stress years: **2016, 2018, 2019, 2020, and 2025**. Stock trade win rate and profit factor fall in OOS, while turnover rises, so the passing aggregate gate does not imply unchanged trade quality. [IS/OOS report](output/validation/stage4_is_oos.md) · [window metrics](output/validation/stage4_window_metrics.csv) · [scorecard](output/validation/stage4_scorecard.csv)

The GOLDBEES sleeve first permits an IS trade on **2007-03-19**, so IS portfolio performance does not cover 2005–2006. The two backtests start flat and the OOS run uses 2013–2014 for indicator warmup; positions and expanding indicator history from IS are not carried across the split. The reported ratios therefore compare **independent runs**, rather than two slices of one continuous portfolio.

## Signal and data checks: 2015–2025

The **formal Stage 2 gate passes** at the primary 3-month horizon: L0 and L3 Newey–West IC t-statistics exceed 2.0, and no signal month is excluded for having fewer than eight names. IC measures the rank relationship between the equity signal and forward stock returns; these figures do not include GOLDBEES performance.

### Filter ladder, 3-month forward returns

| Signal rung | Mean IC | IC NW-t | Positive-IC months | Average names |
|---|---:|---:|---:|---:|
| L0 R1 alone, all eligible price histories | 0.0500 | 3.94 | 69.0% | 1,910 |
| L0 composite, before universe filters | 0.0684 | 4.62 | 79.1% | 1,910 |
| L1, plus price floor | 0.0604 | 4.05 | 77.5% | 1,528 |
| L2, plus circuit and liquidity band | 0.0649 | 3.78 | 77.5% | 844 |
| L3, final tradeable pool | 0.0408 | 2.40 | 70.5% | 401 |
| L3 R1 component | 0.0301 | 2.20 | 66.7% | 401 |
| L3 Ulcer component | 0.0425 | 2.17 | 65.9% | 403 |

All rows use **129 signal months**. The composite is strongest before the final pool filters; L3 retains a positive IC but its NW-t falls from **4.62 to 2.40**. The two L3 components are both positive on their own. [Full ladder results](output/validation/stage2_ladder.csv)

### Horizon decay and quantiles in the L3 pool

| Forward horizon | Mean IC | IC NW-t | Positive-IC months |
|---|---:|---:|---:|
| 1 month | 0.0353 | 2.91 | 63.4% |
| 3 months | 0.0408 | 2.40 | 70.5% |
| 6 months | 0.0377 | 1.68 | 61.1% |
| 12 months | 0.0180 | 0.55 | 56.7% |

Mean IC peaks at **3 months**. Statistical strength fades at 6 and 12 months. The mean forward-return quantiles rise from **Q1 5.06% to Q5 5.90%** at 3 months, with all four adjacent pairs increasing. Their **0.84-point Q5–Q1 spread has NW-t 0.92**, below the diagnostic target of 2.0. At 1 month, Q1 is **1.43%**, Q5 **1.90%**, three of four adjacent pairs increase, and spread NW-t is **1.27**. Thus the rank pattern is orderly at 3 months, but its extreme-quantile spread is not statistically strong. [Quantile results](output/validation/stage2_quantiles.csv)

### Gate and data-quality checks

| Check | Result | Assessment |
|---|---:|---|
| L0 3m IC NW-t, minimum 2.0 | 4.62 | Pass |
| L3 3m IC NW-t, minimum 2.0 | 2.40 | Pass |
| Months excluded for breadth, maximum 15% | 0% | Pass |
| 3m Q5–Q1 spread NW-t, target 2.0 | 0.92 | Below target |
| Top-two-year share of signed L3 IC, target ≤50% | 62.4% | Concentrated |
| Dead-name forward-fill IC difference | −0.0002 | Small |
| Rupee-volume-weighted IC vs equal-weight IC | 0.0176 vs 0.0408 | Weaker in liquid names |
| Rupee-volume-weighted IC NW-t | 0.63 | Weak |
| Names ending >6 months before panel end, minimum 2% | 60 / 4,978 = 1.2% | Survivorship check fails |

The final-pool funnel averages **403 names in 2015**, peaks at **618 in 2021**, and averages **326 in 2025**. The low fraction of names whose histories end early raises a **survivorship-bias concern**; backtest returns and IC may be optimistic if delisted names are missing. The much lower volume-weighted IC raises a separate **capacity concern**. These are unresolved even though the formal IC gate passes. [Signal report](output/validation/stage2_signal_diagnostics.md) · [gate data](output/validation/stage2_gate.csv) · [universe card](output/validation/stage1_universe_card.csv)

## Exit diagnostics: 2015–2025

The real-data run contains **284 stock exits**, matching the OOS scorecard. Every exit-reason bucket has at least **30 trades**. There are **no `END_OF_PERIOD` exits** (0%, below the 5% threshold). All 284 exits have a 20-trading-day follow-up; 274 have a 60-day follow-up. GOLDBEES sleeve trades are outside this stock-exit analysis.

| Exit rule | Exits | Rule-specific post-exit measure | Diagnostic verdict |
|---|---:|---|---|
| Market gate | 51 | Equal-weight index averaged **−3.32%** over 20 and 60 days after **10 distinct gate events** | Working |
| Rank exit | 96 | Same-date entrants beat exited names by **6.36%** on average across 20 and 60 days, over **48 paired rotations** | Rotation adds value |
| Entry stop | 30 | Exited names beat the equal-weight index by **2.86%** on average across 20 and 60 days | **Too early / too tight** |
| Trailing stop | 34 | Exited names lagged the index by **4.14%** on the same measure | Working |
| Time stop | 73 | Exited names lagged the index by **4.05%** on the same measure | Working |

The entry-stop finding is the clear contradiction: names exited at an average trade loss of **16.06%** subsequently returned **+4.27%** over 20 days and **+10.41%** over 60 days; their benchmark-relative returns were **+3.90%** and **+1.81%**, respectively. That pattern suggests rebound or an overly tight stop, but this is a **diagnostic**, not proof that widening the stop would improve portfolio results. It should be checked with a controlled stop or re-entry test and fresh OOS evidence before changing the rule. [Exit report](output/validation/stage5_exit_diagnostics.md) · [exit data](output/validation/stage5_exit_diagnostics.csv)

**Next validation work:** audit historical delistings and panel coverage, test the entry-stop/re-entry question without tuning to the inspected OOS period, then rerun the universe sweep at higher trading costs and with capacity assumptions. The current reports do not establish those results.

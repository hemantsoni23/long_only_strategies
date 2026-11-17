# CSM Value: live-strategy signals and fundamental combinations

> **Benchmark correction:** A first pass used fewer stocks in the market
> benchmark and a shorter warm-up than the normal runner. Its outputs are
> preserved in `prior_smaller_benchmark_universe/`. Both comparisons below
> use the corrected runner-aligned setup; its baseline has been reconciled
> exactly with the normal runner's saved daily returns.

## Decision

No tested blend has demonstrated a reliable improvement on an unexamined period. One blend improved both historical return and drawdown, but it was identified after inspecting the previously examined comparison period. It is available as the explicit `value_growth_pullback` experimental ranking; the default value ranking remains unchanged. These results are development research: 2019–2024, the position count, the value idea, and related OHLCV factors have all been examined previously. Repeated searches increase selection bias.

## Signals inspected

- **Elendel A3:** the stock's price divided by an equal-weight market benchmark, divided by the 252-session maximum of that ratio (minimum 200 observations). Its Q5 is the fraction of the last 126 sessions for which the close exceeds its 50-session moving average (minimum 100 valid observations). These are derived from `Old_live_strategies/csm_elendel_strategy.py`.
- **Zenith:** close divided by the rolling 252-session high, and Q5 measured over 189 sessions. Its original liquidity-rank and other universe filters were not imported.
- **Quad:** the mean of six- and 12-month momentum returns divided by their lagged historical volatility, each with a one-month lag. Its original liquidity-rank cutoff was not imported.
- **Other live strategies:** residual momentum subtracts a lagged beta-adjusted market return; VCP uses moving-average stacks and price strength; the breakout code uses price breakouts, volume and market regime. These ideas are candidates for future work, not claims that their original historical results transfer to this smaller common universe.

Elendel and Zenith forward-fill daily price series in their signal construction. This research reproduces that behaviour; long suspensions or stale prices can therefore distort signals and need a separate data-quality and executable-fill audit.

## Method

All facts supplied to the research were filed and related to a period by 31 December 2024. The existing loader admits a filing only after its filing date. OHLCV and NSE month-end valuation prices were truncated to that date; the benchmark and indicator history begins in 2001, as in the normal runner. The benchmark includes all 2,300 OHLCV symbols with a fundamentals file, even before a company has an eligible quarterly result; current-file membership can create survivorship bias. Both periods use the same files, universe mapping, 10-position cap, 5% per-name weight cap, costs, chassis, stop rules, risk overlays and next-session order model. No top-1,000 price × volume filter is used. The user's zero exit-day weight convention is unchanged. Idle cash earns the model's assumed 6.5% per year; weight changes cost 0.30% each way. Turnover here is total absolute buys plus sells, annualized.

To retain fundamentals as the main factor, the first experiment uses 75% cross-sectional earnings-yield percentile and 25% percentile of the tested live-strategy signal. For composites, the OHLCV quarter is split equally between the two live legs. Missing secondary values receive a neutral rank; an invalid fundamental rank remains ineligible. The earnings-quality-filter candidate retains plain value rank and excludes cases where the available trailing measure of other income plus positive exceptional items divided by pre-tax profit exceeds 50%; this measure is not a pure one-time-profit measure.

Two Elendel-inspired OHLCV benchmarks use A3 and Q5 z-scores and the live strategy's positive 12-month lagged absolute-momentum gate. One is restricted to the value-eligible stock-months; the second uses the available fundamentals/OHLCV stock intersection with the common price, circuit and falling-knife gates, without requiring positive or growing earnings. Both use the CSM Value execution and portfolio chassis rather than Elendel's original top-1,000 universe and position settings. Thus they are controlled *adaptations*, not reproductions of the live strategy's headline results.

The `study.py` development period was 3 June 2019–31 December 2021. Before scoring the previously examined 2022–2024 window it saved the highest development Calmar candidate, with Sharpe and the original value signal as tiebreakers. Baselines were reported separately and were not eligible for fundamental-blend selection.

| Candidate | 2019–2021 CAGR | Max DD | 2022–2024 CAGR | Max DD |
|---|---:|---:|---:|---:|
| Existing value ranking | 24.50% | -13.86% | 24.53% | -11.26% |
| Value + Elendel A3/Q5, selected on development | 32.70% | -13.97% | 18.53% | -16.42% |
| OHLCV Elendel on value-eligible stock-months | 37.62% | -10.77% | 20.55% | -12.19% |
| OHLCV Elendel on available common stock universe | 31.95% | -11.31% | 18.64% | -13.03% |

The pure-OHLCV benchmarks have an absolute-momentum gate; the value candidates do not. They are useful reference points, not a perfect isolation of one factor. The stronger OHLCV development results do not demonstrate that fundamental information necessarily hurts in every setting, and the value baseline's stronger 2022–2024 result does not establish persistent fundamental alpha.

## Second, explicitly exploratory mix

After seeing the first experiment and earlier 2024 research, `explore_fundamental_mix.py` investigated an extra fundamental dimension. Growth is the loader's point-in-time latest-quarter profit-growth score. Quality uses the negative of the other-income/exceptional-items proxy described above; it is not an independently verified measure of recurring earnings. The candidates used the same monthly percentile ranking, costs and mechanics. In growth + live-signal variants, 55% of score came from earnings yield, 20% from the fundamental growth or quality percentile and 25% from OHLCV. All results below are exploratory; showing all candidates is not independent validation.

| Candidate | 2019–2021 CAGR / DD | 2022–2024 CAGR / DD |
|---|---:|---:|
| Existing value | 24.50% / -13.86% | 24.53% / -11.26% |
| Value + growth + Elendel | 33.63% / -14.35% | 20.40% / -16.40% |
| Value + growth + Q5 (development winner) | 35.41% / -14.14% | 15.80% / -19.85% |
| Value + quality + Elendel | 29.41% / -12.97% | 14.26% / -15.86% |
| Value + growth + inverse Elendel | 25.89% / -13.46% | 29.07% / -10.39% |
| Value + inverse Q5 | 23.90% / -12.50% | 22.38% / -11.44% |
| Value + profit growth | 28.82% / -14.52% | 29.67% / -14.24% |

The development winner, growth + Q5, performed worse in the later comparison. Value + growth + inverse Elendel improved both metrics in both historical windows but was identified after inspecting the later results and was not the development winner. It is an exploratory candidate, not an independently validated improvement. Its formula is 55% earnings-yield percentile + 20% profit-growth percentile + 25% inverse A3/Q5 percentile. Inverse A3/Q5 gives more weight to weaker price strength inside the fundamentally eligible value universe; it should not be interpreted as a signal to buy all falling stocks. Run it with `python3 csm_value/run_csm_value_backtest.py --ranking value_growth_pullback`. Its output files have their own prefix. Evaluating new variants after inspecting these windows cannot turn them into a fresh holdout.

## Limits and next work

The 2018–2024 source still has documented scaling and revision-history errors, incomplete SME support and no complete point-in-time security master. Past prices/volumes are vendor-adjusted and may have stale cells. Monthly NSE as-traded closes and a conservative corporate-action mask reduce, but do not eliminate, split and bonus risk. The zero exit-day weight convention can differ materially from realized fill-to-fill P&L. Opening auction access, circuit-limit fills, bid/ask spread and market impact are not modeled. These limitations matter before comparing live strategies or expecting a specific CAGR.

Future work should first improve the known input errors and then evaluate return, drawdown, turnover and concentration using a new unexamined period and sensitivity analyses. Full results, annual return breakdowns and reproducible scripts are alongside this report; no live strategy or default ranking was replaced. [Harvey, Liu and Zhu](https://www.nber.org/papers/w20592) discuss why repeated factor searches need stronger validation.

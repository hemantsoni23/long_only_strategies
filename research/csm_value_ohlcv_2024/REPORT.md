# OHLCV research for CSM Value — data through 2024

> **Comparability update, 12 November 2026:** This first-pass study used a
> smaller equal-weight market-benchmark universe and a 2017 warm-up, while the
> normal CSM Value runner uses all matched JSON/OHLCV files and history from
> 2001. Its results therefore do not reproduce the normal runner's baseline.
> See the newer live-signal study for comparisons reconciled to the runner.

## Conclusion

Price momentum, 52-week-high proximity, volatility and price trends are plausible secondary signals for a fundamentals-led value strategy. This first controlled study does **not** justify adding one to the default strategy. The 6-to-1-month momentum blend won on the 2019–2021 development period, then had both lower CAGR and a deeper drawdown than the value baseline in 2022–2024. That latter period has been researched before and is not a clean blind holdout.

## Scope and data

- Every financial block supplied to this study had a reporting period ending by 31 December 2024 and a public filing date by that date. A filing is usable only on a later calendar day, as enforced by the existing loader. The OHLCV and NSE price panels are truncated at 31 December 2024; prices beginning in 2017 warm up indicators.
- The source is the current `fundamentals/` folder plus `/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data/` and NSE monthly as-traded closes in `csm_value/data/nse_monthly_prices.csv`. The research had 2,029 symbols with some pre-2025 fundamental blocks and 2,015 OHLCV symbols in those staged files. This is not the number eligible in each month, nor a historical security master. No liquidity-rank universe cutoff was applied.
- The primary signal remains point-in-time trailing net profit divided by market capitalization, with the existing positive-profit and profit-growth requirements. The comparison keeps the current 10-position cap, 5% maximum weight per stock, price, falling-knife and circuit gates, buffers, stops, risk overlays and timing. The strategy forms monthly signals after the last trading-session close and the engine uses its existing next-session open order mechanics.
- The user's Elendel accounting convention remains: the exited position has zero weight on exit day. Portfolio returns are weight-based estimates, not a cash/share ledger. The strategy charges 0.30% per unit of absolute weight change; the model assumes idle cash earns 6.5% annually. Turnover below is total absolute weight change, including buys and sells, annualized—not one-way round trips. Capacity, impact, auction liquidity and circuit execution are not fully modeled.
- Current files have survivor/security-identity, historical revision, scale and corporate-action limitations. The retroactively adjusted OHLCV series must not be presumed to reproduce every as-traded historical price or volume. As-traded NSE closes are used to value filed shares, with the existing conservative corporate-action mask. Earlier data also contains known errors. These limitations can change signals and returns.

## Research hypotheses

1. **Intermediate stock momentum, with value still primary.** Measure stock return from 252 to 21 sessions ago, or 126 to 21 sessions ago, and use it as a secondary cross-sectional score. A cheap stock with improving price action may avoid some value traps. Evidence that value and momentum behave differently across several markets is documented by [Asness, Moskowitz and Pedersen (2013)](https://w4.stern.nyu.edu/facdir/lpederse/papers/ValMomEverywhere.pdf); Indian value and momentum evidence is discussed by [Agarwalla, Jacob and Varma (2017)](https://journals.sagepub.com/doi/10.1177/0256090917733848). Neither paper establishes that this particular long-only Indian stock portfolio benefits after costs.
2. **Proximity to a 52-week high.** The test uses current close divided by the highest close in the last 252 sessions, requiring 200 observations. It measures price strength in a different way from a cumulative return. The [George–Hwang 52-week-high paper](https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.2004.00695.x) motivates the hypothesis; this implementation is a secondary rank, not a replication of that paper.
3. **Lower historical volatility or downside risk.** A 63-session daily-return standard deviation serves as a secondary rank favoring lower volatility. This can overlap with the existing inverse-volatility position sizing, so incremental benefit must be measured. The [Ang et al. research](https://www.ruf.rice.edu/~yxing/AHXZ_011906.pdf) studies idiosyncratic volatility; total 63-day volatility here is a different, simpler measure. Future research could separately test downside semi-volatility or drawdown from a rolling high.
4. **Trend gate.** A candidate admits a stock only when its close exceeds its own trailing 200-session mean, requiring at least 180 observations; value still ranks stocks that pass. This can exclude falling value traps but can also miss recoveries. [Time-series momentum research](https://w4.stern.nyu.edu/facdir/lpederse/papers/TimeSeriesMomentum.pdf) motivates trend persistence but examines futures, not this stock-level rule.
5. **Trading activity and capacity.** Median daily traded value, days with no trades, absolute-return-per-traded-value and gap frequency can identify implementation risk. [Amihud (2002)](https://www.sciencedirect.com/science/article/pii/S1386418101000246) motivates an illiquidity proxy, while [NSE's 2012 momentum research](https://nsearchives.nseindia.com/research/content/RP_2_Feb2012.pdf) discusses liquidity and costs in India. Use these first to estimate fills and capacity at explicit account sizes—not to impose the unwanted top-1,000 price-times-volume universe. OHLCV cannot reveal the spread, order-book depth, queue priority or an executable circuit-limit order. Price and volume must use compatible adjustment units before multiplying them.
6. **Market-adjusted and sector-relative momentum.** A future candidate can calculate a stock's trailing return less a lagged beta times a market return, or compare its momentum with point-in-time sector peers. This asks whether it is stronger than its market or industry, not merely participating in a broad rally. It was **not tested** here; sector history and benchmark membership would need point-in-time sources.
7. **Price reaction to earnings.** Compare the return and traded volume around the first session after a public result; a delayed positive reaction might corroborate the value thesis. This was **not tested**. The filing timestamp/date must be reliable, the filing itself is unavailable on its publication date under the user's rule, and a close-observed reaction cannot be traded at that earlier close. Revised or late filings require separate history.
8. **Market breadth and existing risk overlays.** The share of eligible stocks above a trailing trend can describe a broad or narrow market. Test it only as a separate market-risk experiment because this chassis already uses benchmark trend, crash guard, volatility and correlation scaling; an extra filter could duplicate them and reduce exposure. Do not optimize several thresholds on the same short history.

## Fixed experiment and results

Development period: 3 June 2019–31 December 2021. Candidate definitions were fixed before running the study. In each blended candidate, value percentile rank receives 75% weight and the OHLCV percentile receives 25%, ranked across that month's fundamentally eligible stocks. If the secondary score is missing, it is assigned a neutral 50th percentile; the trend-gate candidate instead requires an observed close above its mean. Baseline ranks only earnings yield. Highest development-period Calmar selects the candidate; ties go to Sharpe, then baseline. These are experimental design choices, not optimized truths.

| Candidate | Development CAGR | Development max drawdown | Calmar | Annual turnover |
|---|---:|---:|---:|---:|
| Value baseline | 24.96% | -13.14% | 1.90 | 452% |
| Value + 12–1 momentum | 27.73% | -12.22% | 2.27 | 438% |
| Value + 6–1 momentum | 29.91% | -12.53% | 2.39 | 452% |
| Value + 52-week-high proximity | 25.52% | -12.27% | 2.08 | 465% |
| Value + lower 63-day volatility | 23.53% | -11.61% | 2.03 | 379% |
| Value with 200-day trend gate | 23.74% | -12.83% | 1.85 | 453% |

The frozen development winner was **6–1 momentum**. Only that candidate and the baseline were then scored in the previously examined comparison period, 3 January 2022–31 December 2024:

| Candidate | CAGR | Max drawdown | Calmar | Annual turnover | Mean exposure |
|---|---:|---:|---:|---:|
| Value baseline | 18.03% | -13.87% | 1.30 | 472% | 43.70% |
| Value + 6–1 momentum | 12.93% | -19.61% | 0.66 | 588% | 42.23% |

The baseline versus momentum returns by calendar year were 3.61% versus 2.05% in 2022, 38.85% versus 35.59% in 2023, and 14.16% versus 3.98% in 2024. These are portfolio returns under the requested booking, not proof of a single cause. Higher turnover increased modeled trading costs, but the results do not establish that turnover explains the full gap. The 2019–2021 selection result is not evidence that the momentum addition will generalize.

The other four candidates were not scored in the comparison period, to avoid choosing a new winner after seeing that period. Their development scores alone do not establish that they would improve the strategy.

## Follow-up research

1. Repair and independently validate filing versions, units and corporate actions; explicitly identify symbols and dates omitted because the evidence is insufficient.
2. Investigate candidate behavior by entry, exit, holding period, regime, profitability and liquidity using time-aligned diagnostics, without using a backtested winner as proof. Consider benchmark- and sector-adjusted momentum, downside risk, and earnings-reaction timing as distinct hypotheses.
3. Predeclare a small new experiment and cost/capacity assumptions. Report annual returns, rolling drawdowns, turnover, exposure, position counts and the same-universe baseline. Use chronological walk-forward selection and block-bootstrap or randomization checks for selection risk. A period already used to guide changes is development data, not a new holdout.
4. Once 2025–2026 fundamentals are repaired, set aside a future period that has not been used to tune the resulting rule. Do not use the poor-data period as a clean test until its inputs and availability are verified.

`study.py` is the reproducible selection and frozen comparison; `diagnostics.py` produces the year-by-year results. `results.json`, `frozen_selection.json` and `yearly_diagnostics.json` store the numbers. `test_study.py` tests causal feature calculations and missing-signal handling. No OHLCV overlay from this experiment was added to the production strategy.

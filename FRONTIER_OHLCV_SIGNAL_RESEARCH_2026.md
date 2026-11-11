# Frontier OHLCV Signal Research for New Indian Long-Only Strategies

**Research date:** 26 October 2026  
**Data tested:** daily Indian-stock OHLCV, usable panel 1 January 2003–4 September 2026; monthly signal dates 31 January 2003–17 July 2026  
**Decision:** no newly tested signal is ready to become a standalone live strategy. One weak-but-repeatable soft tilt (`low_kurt_252`) merits a controlled engine test; two other findings merit pre-registered follow-up designs.

## 1. Executive conclusion

The repository is already much further along than the two older momentum reports imply. In addition to the strategies in `Old_live_strategies/`, the later `factor_research/` work has tested 122 factors and several dedicated extensions. It already covers most obvious OHLCV ideas: conventional and residual momentum, 52-week anchors, trend quality, low volatility/MAX/skew, volume and money flow, intraday/overnight returns, reversal, breakout/compression, relative strength, and seasonality.

I therefore tested ten genuinely additional specifications rather than renaming an existing factor:

1. 36–13 and 60–13 month long-run reversal;
2. low 252-day realized kurtosis;
3. negative market coskewness;
4. resilience on the market's worst rolling-quintile days;
5. stock-level Amihud illiquidity shock;
6. five-day reversal conditional on an illiquidity shock;
7. stable dollar-volume participation;
8. low stale-price frequency; and
9. Hou–Moskowitz weekly price delay.

The honest outcome is:

- **Do not build a new standalone factor strategy from this batch.** Concentrated top-15 books do not confirm the strongest IC readings.
- **Research `low_kurt_252` as a small safety/quality tilt only.** It is positive in the 2015+ and 2019+ holdouts and across universes, but its incremental t-stat is weak and its portfolio improvement is negligible.
- **Treat tail resilience as a risk descriptor, not an alpha rank.** It has the largest IC, but the highest-resilience quintile does not earn the return; middle quintiles do. Adding it to Elendel/Zenith damages holdout Sharpe.
- **Pre-register an “avoid acute illiquidity shock” test.** The literature-motivated positive illiquidity-premium direction failed. The opposite pattern—severe recent liquidity deterioration followed by underperformance—is strong in the broad universe, but reversing the sign now would be post-selection and needs a fresh test.
- **Keep price delay and liquidity-shock reversal on the watchlist.** Price delay is marginal and fades in holdout. Liquidity-shock reversal is a one-month event effect with very high turnover, not a monthly long-horizon selection factor.

The best unimplemented ideas already present in the repository remain ahead of these new signals: tight-range trend, residual-momentum plus persistence, the low-risk sleeve, and large-cap intraday trend. See `factor_research/NEW_STRATEGY_IDEAS.md` and `factor_research/MASTER_RANKING.md` before commissioning another strategy.

## 2. What the existing live strategies already cover

| Existing strategy | Main selection logic | What a new signal must add |
|---|---|---|
| CSM Batch / Quad / Absolute | dual-window, volatility-scaled 6/12-month momentum; positive absolute-momentum gate | not another return/lookback/Sharpe variation |
| Elendel | relative-strength line near its own 52-week high + 126-day trend persistence | must be incremental to a very strong anchor/quality composite |
| Zenith | price near 52-week high + 189-day persistence; high-MAX exclusion | must survive after anchor, persistence and lottery filters |
| Residual Momentum | beta-stripped momentum + 52-week-high tilt | not simple market-residual return |
| HR Breakout | clustered horizontal-resistance break plus trend template and relative strength | not a generic Donchian/new-high rule |
| VCP | volatility-contraction pattern plus trend template and relative strength | not a range/ATR compression clone |

The old momentum explanations additionally cover range position, new-high recency, signed trend R², Clenow slope, frog-in-the-pan consistency, industry momentum, up/down volume, volatility contraction, low MAX, acceleration, one-month reversal, and seasonality. The later factor catalog expands this to 122 factors. This is why a superficially attractive idea such as “low volatility momentum,” “volume-confirmed breakout,” or “intraday momentum” is not new here.

## 3. Research basis for the frontier signals

- **Price delay.** Hou and Moskowitz measure how slowly a stock incorporates common market information and report a return premium among the most delayed firms. The implementation here uses their D1 idea: one minus the contemporaneous-market regression R² divided by the R² with four weekly market lags, estimated over 52 weeks. [Hou & Moskowitz, *Market Frictions, Price Delay, and the Cross-Section of Expected Returns*](https://doi.org/10.1093/rfs/hhi023)
- **Systematic skewness.** Harvey and Siddique show that systematic skewness can matter for expected returns and report a link to momentum. I test a rolling daily coskewness rank, not merely the stock's standalone skewness already in the catalog. [Harvey & Siddique, *Conditional Skewness in Asset Pricing Tests*](https://onlinelibrary.wiley.com/doi/10.1111/0022-1082.00247)
- **India-specific higher moments.** An Indian NSE-100 study finds conditional co-moments can be priced, which makes a local test reasonable but does not guarantee a tradable cross-sectional rank. [Chaudhary, Misra & Bakhshi, 2020](https://doi.org/10.21511/imfi.17%282%29.2020.24)
- **Long-run reversal.** De Bondt and Thaler's classic overreaction design motivates old-winner/old-loser reversal. [De Bondt & Thaler, 1985](https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6261.1985.tb05004.x). India-specific evidence reports raw reversal but says it disappears after simultaneous beta, size, value and liquidity controls. [Maheshwari & Dhankar, Indian re-examination](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2785516)
- **Liquidity shocks and short-term reversal.** Nagel interprets short-term reversal as compensation for supplying liquidity, with a strongly time-varying opportunity set. [Nagel, *Evaporating Liquidity*](https://www.nber.org/system/files/working_papers/w17653/w17653.pdf). The present test asks whether an individual-stock Amihud shock, or a five-day reversal weighted by that shock, works in the Indian panel.
- **Statistical hurdle.** Because overlapping 3/6/12-month returns induce serial dependence, reported t-statistics use Newey–West lags of `horizon - 1`. [Newey & West, 1987](https://ideas.repec.org/a/ecm/emetrp/v55y1987i3p703-08.html). A conventional `|t| > 2` is not enough after a large factor search; Harvey, Liu and Zhu argue that a newly mined factor should clear a much higher hurdle near 3.0. [Harvey, Liu & Zhu, 2016](https://www.aea.ru/data/pdf/campbell.pdf)

## 4. Test protocol

### 4.1 Universes

- **U1 Liquid-1000:** price above ₹20, trailing 63-day median rupee-volume rank at most 1,000, and no more than five circuit-like days in the last 63 sessions.
- **U2 Live-trend:** U1 plus close above SMA-200. This is the closest diagnostic universe to the live momentum books and is the primary table below.
- **U3 Top-300:** price/circuit filters plus trailing rupee-volume rank at most 300, without the SMA-200 gate. This tests whether a result survives in more executable large caps.

The average U2 cross-section is about 281–416 names depending on signal history. The average U3 cross-section is about 182–271.

### 4.2 Timing and metrics

- Signal observed at monthly date `t`; entry is delayed one trading day.
- Forward returns are 1, 3, 6 and 12 months.
- **IC:** monthly cross-sectional Spearman rank correlation between signal and forward return.
- **ICIR:** mean monthly IC divided by its time-series standard deviation; it is not annualized.
- **Accuracy:** fraction of monthly IC observations above zero.
- **NW t-stat:** Newey–West t-statistic with lags `0/2/5/11` at 1/3/6/12 months.
- **Non-overlap t-stat:** average t-stat across the `h` nonoverlapping monthly offsets; reported in the CSV as a robustness check.
- **Holdout:** discovery through December 2014; holdout from January 2015 onward. A second recent check starts January 2019.
- **Incremental IC:** residualize the candidate's cross-sectional percentile rank on the live Elendel composite, then measure residual IC.
- **Portfolio translation:** equal-weight top 15, monthly rebalance, 30 bps one-way charged on replaced weight. This is a stripped signal test, not the full production engine.

Signal orientation was frozen before results were inspected. Failed signs were not flipped into discoveries.

## 5. Primary results — U2 live-trend universe

All IC and excess-return values are decimals. `Top Q excess` is the mean three-month return of the highest factor quintile minus the winsorized cross-sectional average.

| Signal | IC 1m | IC 3m | ICIR 3m | Accuracy | NW t(3m) | IC 6m | IC 12m | Holdout IC / t | Incremental IC / t | Top Q excess | Peak | Verdict |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| `low_kurt_252` | 0.0128 | 0.0154 | 0.180 | 62.8% | 2.16 | 0.0149 | 0.0061 | 0.0188 / 2.37 | 0.0096 / 1.37 | +0.0017 | 3m | weak soft tilt |
| `tail_resilience_252` | 0.0455 | 0.0548 | 0.286 | 62.1% | 3.06 | 0.0588 | 0.0516 | 0.0537 / 2.18 | 0.0439 / 2.54 | **−0.0039** | 6m | risk descriptor, not rank |
| `price_delay_52w` | 0.0108 | 0.0183 | 0.158 | 56.7% | 1.81 | 0.0182 | 0.0078 | 0.0106 / 0.79 | 0.0122 / 1.26 | −0.0046 | 3m | watch/reject standalone |
| `liqshock_reversal_5` | 0.0129 | 0.0076 | 0.115 | 56.4% | 1.70 | 0.0046 | 0.0003 | 0.0097 / 2.01 | 0.0026 / 0.42 | −0.0064 | 1m | daily-event research only |
| `stable_dvol_63` | 0.0219 | 0.0140 | 0.119 | 57.1% | 1.42 | 0.0105 | −0.0023 | 0.0208 / 1.58 | 0.0116 / 1.21 | −0.0154 | 1m | non-monotonic; reject |
| `neg_coskew_252` | 0.0100 | 0.0092 | 0.088 | 56.8% | 1.05 | 0.0071 | 0.0061 | 0.0109 / 0.86 | 0.0097 / 1.15 | +0.0008 | 2m | reject |
| `illiq_shock_21_252` | −0.0063 | −0.0064 | −0.062 | 45.9% | −0.79 | −0.0060 | −0.0052 | 0.0044 / 0.42 | 0.0113 / 1.43 | **−0.0111** | 12m | expected sign fails; avoidance lead |
| `longrev_36_13` | −0.0169 | −0.0165 | −0.134 | 45.1% | −1.47 | −0.0136 | −0.0070 | 0.0099 / 0.92 | −0.0148 / −1.35 | −0.0003 | 12m | reject |
| `longrev_60_13` | −0.0086 | −0.0116 | −0.090 | 48.3% | −0.91 | −0.0063 | −0.0032 | 0.0094 / 0.73 | −0.0107 / −0.87 | +0.0015 | 12m | reject |
| `low_stale_63` | 0.0018 | −0.0089 | −0.104 | 45.9% | −1.28 | −0.0167 | −0.0212 | −0.0260 / −2.75 | −0.0247 / −4.25 | −0.0563 | 1m | reject / data warning |

### 5.1 Large-cap robustness

In U3 Top-300:

- `low_kurt_252`: IC3 **0.0314**, ICIR **0.359**, NW t **4.36**, accuracy **63.7%**, holdout IC **0.0275**. It clears the statistical hurdle, but the highest decile excess is negative and the top-15 holdout Sharpe is only **0.24**.
- `tail_resilience_252`: IC3 **0.0700**, NW t **2.97**, holdout IC **0.0697**, and IC12 **0.0941**. Yet the highest quintile excess is again slightly negative and top-15 holdout Sharpe is only **0.04**.
- `price_delay_52w`: IC3 **0.0278**, NW t **1.90**, but holdout IC falls to **0.0133** with t **0.75**.

This is the central warning of the exercise: **a good rank correlation across all names is not sufficient evidence for a concentrated long-only strategy.** Tail resilience mostly separates fragile losers from the middle, not exceptional winners from the middle.

## 6. Portfolio translation and why no factor is promoted

### 6.1 Standalone top-15 books in U2

| Signal | CAGR | Sharpe all | Sharpe 2015+ | Max drawdown | Monthly turnover |
|---|---:|---:|---:|---:|---:|
| Elendel reference | 28.6% | 0.81 | 0.76 | −57.8% | 0.58 |
| `low_kurt_252` | 19.4% | 0.54 | 0.51 | −64.9% | 0.41 |
| `tail_resilience_252` | 8.7% | 0.22 | −0.23 | −46.0% | 0.38 |
| `price_delay_52w` | 12.8% | 0.38 | 0.21 | −54.2% | 0.44 |

`tail_resilience_252` lowers drawdown but does not earn enough return and deteriorates after 2014. That is a defensive characteristic, not a standalone alpha.

### 6.2 Add-on tests

Adding a candidate z-score to the live composite gives the following representative results:

| Base + add-on | Weight | Sharpe all | Sharpe pre-2015 | Sharpe 2015+ | Max DD | Decision |
|---|---:|---:|---:|---:|---:|---|
| Elendel only | 0 | 0.808 | 0.855 | 0.760 | −57.8% | reference |
| Elendel + low kurtosis | 0.25 | 0.816 | 0.830 | 0.801 | −58.9% | tiny, unstable improvement |
| Elendel + tail resilience | 0.50 | 0.791 | 1.155 | 0.458 | −47.7% | discovery/holdout failure |
| Elendel + price delay | 0.25 | 0.807 | 0.860 | 0.758 | −51.9% | essentially no Sharpe gain |
| Zenith only | 0 | 0.768 | 1.133 | 0.398 | −51.0% | reference |
| Zenith + low kurtosis | 0.50 | 0.779 | 1.111 | 0.434 | −53.9% | tiny, drawdown worse |
| Zenith + tail resilience | 0.50 | 0.535 | 1.064 | 0.018 | −48.7% | reject |
| Zenith + price delay | 0.50 | 0.624 | 0.988 | 0.273 | −47.0% | reject |

Simple bottom-decile/quintile exclusion filters also fail to improve both discovery and holdout. Therefore even `low_kurt_252` should not be merged into live code on this evidence.

## 7. Signal definitions and implementable strategy ideas

### 7.1 Kurtosis-aware momentum — only candidate for a controlled engine test

For stock `i` at date `t`:

`low_kurt_252(i,t) = - excess_kurtosis(daily_return[i, t-251:t])`

Proposed experiment, not a live rule:

`score = z(Elendel) + 0.25 × z(low_kurt_252)`

Why it may help: it penalizes trends dominated by fat-tailed jumps without duplicating MAX, volatility, drawdown or trend persistence exactly. It remains positive after 2015 and after 2019 and works better in Top-300 stocks.

Why it is not approved: U2 t=2.16 is below a factor-zoo threshold, incremental t=1.37, the top bucket is not economically strong, and the add-on improves Sharpe by only 0.007 overall. The next test must be the full Elendel engine with unchanged stops, costs and sizing, plus placebo weights and an untouched forward paper window.

### 7.2 Tail-resilient momentum — use as a portfolio constraint, not the alpha score

Let `I_d` mark days in the bottom 20% of market returns over the trailing year:

`tail_resilience = sum(r_i,d × I_d) / sum(abs(r_m,d) × I_d)`

Higher values mean the stock historically fell less—or rose more—on market-tail days.

The IC is strong and incremental, but returns are hump-shaped: the middle quintiles outperform while the highest-resilience quintile does not. Possible future use is a **portfolio-level tail-beta constraint** or tie-breaker among otherwise equal momentum candidates. Do not rank the book primarily on this factor. Any middle-bucket rule would be post-hoc and must be pre-registered and tested on a later sample or alternate data source.

### 7.3 Illiquidity-shock avoidance — promising negative screen, but discovered post-look

`illiq_shock = log(mean_21(|r| / rupee_volume) / mean_252(|r| / rupee_volume))`

The a-priori high-score direction fails. In U1, IC3 is −0.0297 with NW t −3.81; in U2, the highest quintile underperforms the cross-section by **1.11% over three months** with t −4.07. This suggests recent deterioration in tradability is not compensated—it is a warning.

A useful next hypothesis is: **block new entries in the worst 10–20% of illiquidity shocks, while leaving the base score unchanged.** Because that rule is chosen after seeing the negative result, it is not verified here. Freeze the cutoff and test it in a rolling expanding-window design and in the event-driven engine, including market-impact costs.

### 7.4 Price-delay × momentum — literature-consistent interaction, not yet verified

Price delay alone is too weak. Hou–Moskowitz report stronger drift in delayed firms, so the better hypothesis is an interaction:

`score = z(existing momentum) + λ × z(momentum × price_delay)`

This must be pre-registered before testing. Use only Top-300/Top-500 stocks, because weekly nonsynchronous trading can mechanically create apparent delay in illiquid names. Require at least 48 valid weekly observations, as in the present implementation.

### 7.5 Liquidity-provision event sleeve — separate daily research project

`liqshock_reversal_5 = - five_day_return × max(log(illiq_shock), 0)`

It has a one-month IC of 0.0129 with t=2.94 in U2 and remains positive after 2015, but decay is fast, the highest bucket is poor, and monthly turnover is about 0.86. If pursued, it needs a daily/weekly event backtest with next-open fills, bid/ask or slippage stress, circuit-day handling, and holding periods of 1/2/5/10/20 sessions. It does not belong in the monthly momentum engine yet.

## 8. Rejected ideas — avoid retesting without new data or a new mechanism

- **Long-run reversal:** wrong sign in the discovery sample, negligible holdout evidence, and weak concentrated books. The trend-gated long-only universe is structurally hostile to a deep-loser strategy.
- **Negative coskewness:** small positive IC but no statistical or economic strength; it does not improve Elendel materially.
- **Stable dollar volume:** only a short-horizon average relation; the top quintile is the worst. Non-monotonicity makes a simple rank invalid.
- **Low stale-price frequency:** deteriorates sharply after 2014 and is contaminated by ties and data-quality effects.
- **Tail resilience as top-rank alpha:** strong IC but poor extreme bucket and poor holdout portfolio.
- **Price delay standalone:** does not survive the holdout strongly enough and provides little portfolio improvement.

## 9. Recommended build order

1. **Do not create a new production strategy from stage 25.** Preserve the negative result.
2. **Prioritize the already-tested candidates in `factor_research/MASTER_RANKING.md`** before any stage-25 idea.
3. **Run one controlled full-engine test of Elendel + 0.25 low-kurtosis**, with no other parameter changes. Treat it as a tie-break/soft tilt, not a new book.
4. **Pre-register an illiquidity-shock entry veto** and test 10%, 20% and one placebo cutoff only; the final decision must be based on holdout/walk-forward results, not the in-sample negative IC.
5. **Build a daily event harness** only if a genuinely distinct short-horizon sleeve is desired; test liquidity-shock reversal there rather than forcing it into a monthly framework.
6. **Use tail resilience for portfolio risk diagnostics**: exposure reporting, candidate tie-breaks, and perhaps a maximum aggregate crash-beta constraint. Do not allocate directly to its top-ranked names.

Promotion gates for any follow-up:

- positive IC at the intended horizon in U1 and U3;
- NW `t >= 3` in at least one primary universe and `t >= 2` in the untouched holdout;
- positive incremental IC with `t >= 2` versus Elendel/Zenith;
- monotone or at least economically coherent quintiles, with a positive top bucket;
- full-engine improvement in both discovery and holdout Sharpe without materially worse drawdown;
- robustness to 15/30/50 bps one-way cost, universe bands, and alternate corporate-action cleaning;
- paper trading before live capital.

## 10. Data and inference limitations

These results are **research verification, not production certification**.

1. The cached usable panel starts in 2003, not 2000, because broad cross-sectional coverage and warm-up requirements remove the earliest raw rows.
2. The stock files are not proven to be a point-in-time, survivorship-free security master. Missing delisted firms can materially flatter low-risk and low-kurtosis signals.
3. Prices are not a verified total-return, split/dividend-adjusted series. The loader masks close-to-close moves below −40% or above +300% as probable corporate actions/bad prints.
4. Forward-return construction keeps a disappeared price flat rather than booking a delisting loss. This is conservative for some gaps but optimistic for bankruptcies/delistings.
5. The benchmark used for factor construction is an equal-weight return across available stocks, not a point-in-time investable index.
6. The stripped top-15 book does not reproduce stops, hysteresis, capacity limits, next-open gaps or all live-engine overlays.
7. Ten new signals were tested after an earlier 122-factor search. The nominal t-stat must be interpreted in that multiple-testing context; a t around 2 is a research lead, not proof.
8. IC measures ranking across all eligible stocks. Concentrated long-only performance depends on the extreme right tail, which is why quintile and top-15 checks overrule attractive ICs here.

## 11. Reproduction files

- `factor_research/stage25_frontier_signals.py` — factor construction and main evaluation.
- `factor_research/stage25b_frontier_robustness.py` — nonoverlap t-stats, holdout/recent splits, quintiles, add-on and filter tests.
- `factor_research/results/stage25_frontier_summary.csv` — compact IC/ICIR/accuracy/horizon/book table.
- `factor_research/results/stage25_robustness.csv` — NW and nonoverlap inference, incremental tests, year consistency.
- `factor_research/results/stage25_quintiles.csv` — monotonicity and economic-tail diagnostics.
- `factor_research/results/stage25_addon_books.csv` — Elendel/Zenith add-on tests.
- `factor_research/results/stage25_filter_books.csv` — one-sided exclusion tests.

Re-run from the repository root:

```bash
python3 factor_research/stage25_frontier_signals.py
python3 factor_research/stage25b_frontier_robustness.py
```

The scripts only write stage-25 cache/result files and do not modify any live strategy.


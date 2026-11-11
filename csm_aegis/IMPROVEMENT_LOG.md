# CSM Aegis improvement log

This is a sequential research log. `v1.2` is frozen: close fills, 0.3% per
leg, zero return on idle cash, and data through 2026-07-17. Every candidate
below is one isolated change from that baseline unless explicitly stated.

> **Execution-integrity correction (2026-10-26):** Results recorded below the
> next section used forward-filled close prices as executable fills. That allowed
> fills on missing-volume and circuit-locked bars, including a fictitious exit
> during NARMADA's 2017–18 suspension. They are retained as research history,
> not valid decision evidence. Corrected raw-OHLCV execution cancels unfillable
> entries and defers exits until a tradable bar: **v1.2: 23.51% CAGR, 1.64
> Sharpe, -32.90% max DD; v1.3: 24.08%, 1.70, -34.10%**. Re-run all candidate
> comparisons under this model before promoting any configuration.

> **ETF calendar-date correction (2026-10-28):** ETF CSV timestamps are local
> exchange midnight values (for example `+05:30`). The ETF loader previously
> converted them to UTC before taking the calendar date, shifting ETF closes by
> one session. It now preserves the exchange calendar date. All ETF-sleeve
> figures below this notice use the corrected alignment: unrestricted v1.3 +
> GOLDBEES is **27.99% CAGR, 1.54 Sharpe, -30.6% DD**; v1.4_low_dd is
> **24.11%, 1.51, -24.4%**. Earlier ETF figures are superseded.

## v1.4 low-drawdown promotion — daily ADX/DMI gate plus GOLDBEES sleeve

**Rule.** Retain v1.3's selector, five-day fresh-entry spike filter, and
two-name industry cap. A fresh top-20 candidate must additionally have daily
ADX(14) >= 25 and `+DI > -DI` at the signal close. Rejected top-20 candidates
do not backfill from below rank 20, which preserves the isolated experiment's
breadth. Sweep all idle cash into GOLDBEES at raw tradable ETF closes, using the
same raw positive-volume/non-circuit validation as stock fills. The existing
bear/panic regime-leverage sales release capital into the sleeve; risk-on
rebalance buys are funded only by a valid ETF sale. No RFR/cash yield is used.

| Common GOLDBEES window: 2007-03-19 to 2026-07-17 | CAGR | Sharpe | Max DD | Calmar |
|---|---:|---:|---:|---:|
| v1.3 equity-only control | 23.09% | 1.66 | -33.8% | 0.68 |
| v1.3 + unrestricted GOLDBEES sleeve | 27.99% | 1.54 | -30.6% | 0.91 |
| **v1.4_low_dd: ADX/DMI + GOLDBEES** | **24.11%** | **1.51** | **-24.4%** | **0.99** |

**Decision.** Promote `v1.4_low_dd` as the drawdown-focused live/paper-trade
preset; retain v1.3 as the higher-return comparator. Supertrend exit and daily
pivot variants were rejected: each reduced CAGR materially without a comparable
improvement in risk-adjusted return. The next validation requirement is a
pre-declared ADX 20/25/30 sensitivity and split-period/cost/delay stress before
increasing capital allocation.

## Rejected experiment — long-only gold/silver ratio sleeve rotation

**Rule.** On each month-end, compute the 63-session rolling z-score of
`log(GOLDBEES / SILVERBEES)` and execute at the next valid close. At z >= +1,
hold SILVERBEES (gold expensive relative to silver); at z <= -1, hold GOLDBEES;
otherwise retain the prior metal. A switch pays both ETF legs at 0.3% each.
This is long-only tactical rotation, not arbitrage: a true ratio arbitrage
requires a simultaneous long/short spread, borrow/margin, and a separate
execution model.

| Common SILVERBEES window: 2022-02-07 to 2026-07-31 | CAGR | Sharpe | Max DD | Calmar | Rotations |
|---|---:|---:|---:|---:|---:|
| Always GOLDBEES | 26.35% | 1.35 | -24.4% | 1.08 | 0 |
| Always SILVERBEES | 31.40% | 0.98 | -45.0% | 0.70 | 0 |
| Ratio rotation, 0.3%/leg | 28.33% | 1.19 | -24.4% | 1.16 | 22 |
| Ratio rotation, 0.6%/leg | 26.34% | 1.13 | -24.4% | 1.08 | 22 |
| Ratio rotation, 1.0%/leg | 23.73% | 1.03 | -24.8% | 0.96 | 22 |

**Decision.** Reject from production. It does not improve max drawdown, its
apparent return advantage is erased at a modest cost increase, and SILVERBEES
provides only 4.5 years of common executable history. The isolated files
`csm_aegis_metal_ratio_experiment.py` and
`run_metal_ratio_experiment.py` retain the reproducible experiment.

## Acceptance rule

We want a material drawdown improvement without sacrificing the strategy:

- full-sample CAGR must remain at least 23.7% (preferably improve on 24.17%);
- max drawdown must improve by more than normal research noise (about 2–3
  percentage points is not automatically persuasive here);
- the direction should survive the 2005–2015 / 2016–2026 split, the latest 36
  months, and higher-cost/delayed-fill stress tests;
- no idle-cash yield, open-fill assumption, or unrecorded parameter search.

| Variant | CAGR | Sharpe | Max DD | Calmar | Trades | Decision |
|---|---:|---:|---:|---:|---:|---|
| Frozen v1.2 | 24.17% | 1.69 | -29.02% | 0.83 | 1,336 | Baseline |
| Fresh-entry 5d spike filter | 24.35% | 1.73 | -26.67% | 0.91 | 1,287 | Continue validation |
| 10% entry stop | 23.45% | 1.67 | -27.00% | 0.87 | 1,403 | Reject |
| 10% entry stop + 20d fixed cooldown | 24.23% | 1.73 | -29.07% | 0.83 | 1,384 | Reject |
| 5% maximum entry weight | 23.86% | 1.68 | -28.88% | 0.83 | 1,336 | Reject |
| Discrete-path filter (FIP) | 22.86% | 1.61 | -29.55% | 0.77 | 1,335 | Reject |
| At most 2 names / industry | 24.90% | 1.72 | -28.84% | 0.86 | 1,268 | Continue validation |

## Candidate 1 — fresh-entry five-day spike filter

**Rule.** At every signal month-end, calculate each eligible stock's raw-close
five-day return. Do not open a new position when it exceeds the 80th percentile
of the eligible universe. Existing holdings are unaffected. This is the exact
fresh-entry convention used in the prior residual-momentum research; the
parameter values were chosen there, not fitted in this run.

The economic rationale is short-term reversal after salient price jumps. It is
also deliberately narrower than a generic volatility screen, which Aegis has
already tested.

| Period / stress | v1.2: CAGR / Sharpe / DD | Spike filter: CAGR / Sharpe / DD |
|---|---|---|
| 2005–2015 | 31.79% / 2.13 / -18.59% | 32.97% / 2.24 / -18.64% |
| 2016–end | 16.75% / 1.22 / -27.52% | 16.02% / 1.20 / -25.90% |
| Latest 36 months | 19.18% / 1.49 / -11.68% | 17.74% / 1.40 / -11.68% |
| Cost 0.6%/leg | 21.96% / 1.55 / -30.42% | 22.17% / 1.59 / -28.16% |
| One-day extra fill delay | 23.49% / 1.62 / -25.99% | 24.72% / 1.72 / -24.50% |
| Two-day extra fill delay | 22.85% / 1.57 / -25.81% | 23.79% / 1.65 / -24.00% |

There were 316 `ENTRY_SPIKE` rejections. The full-sample and stress direction
is favourable, but the lower latest-36-month CAGR and the modest size of the DD
gain remain a caution. It is promoted as part of user-selected `v1.3`; its
standalone switch remains available for comparison and monitoring.

## Candidate 2 — tighter stop and fixed stop cooldown

**Rule.** `stop_from_entry=0.10` and `stop_cooldown_days=20`. The cooldown is a
calendar-day, ticker-specific ban after every `STOP_ENTRY` or `STOP_TRAIL`,
matching the Zenith/Batch convention. It is independent of Aegis's older
loss-scaled cooldown experiment.

The 10% stop itself improved drawdown but failed the return floor. Adding the
fixed cooldown generated 115 rejections and restored return, but also restored
the baseline drawdown. It fails the objective and is not carried forward.

## Candidate 3 — maximum 5% entry weight

**Rule.** `w_hi=0.05`, keeping the existing 100% gross cap and all other sizing
unchanged. This is a real entry cap, not an after-the-fact portfolio rescale.

It lowered average exposure to 0.644 and slightly reduced both CAGR and DD. The
DD effect is far too small to justify a production change.

## Candidate 4 — gradual-path (Frog-in-the-Pan) entry filter

**Rule.** Over the same 12-month, one-month-skip formation period as R1,
compute `ID = sign(formation return) * (negative-day share - positive-day
share)`. Reject fresh candidates above the 80th eligible-universe percentile:
the most jump-driven price paths. The source is Da, Gurun and Warachka (2014),
summarized in `momentum/Frog in the Pan Continuous Information and Momentum
(2014).md`.

It produced 85 rejections and materially worsened all headline metrics. This
is useful negative evidence: Aegis's existing Ulcer and M3 controls already
capture enough of this idea, or the result does not transport to this universe.

## Candidate 5 — two names per industry

**Rule.** At month-end, permit at most two holdings/new entries sharing an
`Industry_clean` label from `instruments_clean.csv`. The limit applies only to
new entries; it does not force liquidation of a pre-existing over-cap book.
Unknown labels are intentionally assigned a unique one-name group rather than
being falsely pooled. There were 504 cap rejections; 52.8% of all panel symbols
had an industry label.

| Period | v1.2: CAGR / Sharpe / DD | Industry cap: CAGR / Sharpe / DD |
|---|---|---|
| 2005–2015 | 31.79% / 2.13 / -18.59% | 32.50% / 2.18 / -17.79% |
| 2016–end | 16.75% / 1.22 / -27.52% | 17.49% / 1.26 / -27.32% |
| Latest 36 months | 19.18% / 1.49 / -11.68% | 18.28% / 1.39 / -11.32% |

The full sample improves return and risk modestly, but the DD benefit is below
the materiality threshold and recent CAGR is lower. It is promoted as part of
user-selected `v1.3`, with the following controls outstanding: improve/reconcile
label coverage and run label-placebo tests.

## Candidate 6 — abnormal turnover entry filter

**Rule.** At each month-end, calculate 21-day mean rupee turnover divided by
the stock's 252-day median rupee turnover. Reject a fresh top-20 candidate above
the 80th percentile of the eligible universe. This is distinct from the
universe's absolute-liquidity screen: it measures unusual attention in a stock
relative to itself. The source is Lee and Swaminathan (2000), summarized in
`momentum/Price Momentum and Trading Volume (2000).md`.

The result is a clear rejection: **22.38% CAGR, 1.61 Sharpe, -29.19% max DD**
with 601 `ENTRY_TURNOVER` rejections. The 2016–end and latest-36-month CAGRs
were only 13.20% and 11.11%. Keep `entry_turnover_filter=False`.

## Candidate 7 — risk-adjusted residual momentum (RAMOM-style)

**Rule.** Replace R1's raw residual-return aggregation with the average of
12-day residual returns divided by their one-day-lagged fast EWMA volatility
(alpha 0.50), over the same 12-month/one-month-skip formation span. Ranking,
Ulcer, sizing, execution, and gates are unchanged. The source is Dudler, Gmür,
and Malamud (2015), summarized in `momentum/Momentum and Risk Adjustment
(2015).md`.

It raised return quality but fails the target drawdown: **24.37% CAGR, 1.74
Sharpe, -31.65% max DD**. Its earlier and recent split results were also mixed
(2005–2015: 30.34% / 2.09 / -21.85%; 2016–end: 18.47% / 1.38 / -25.79%; latest
36 months: 20.68% / 1.69 / -15.25%). Keep `risk_adjusted_signal=False`.

## Combined configuration — v1.3

**Rule.** Frozen v1.2 plus Candidate 1 and Candidate 5:
`entry_spike_filter=True`, `entry_spike_window=5`,
`entry_spike_quantile=0.80`, and `industry_cap=2`.

| Period | v1.2: CAGR / Sharpe / DD | v1.3: CAGR / Sharpe / DD |
|---|---|---|
| Full sample | 24.17% / 1.69 / -29.02% | 24.54% / 1.74 / -29.28% |
| 2005–2015 | 31.79% / 2.13 / -18.59% | 31.84% / 2.21 / -19.17% |
| 2016–end | 16.75% / 1.22 / -27.52% | 17.40% / 1.27 / -26.95% |
| Latest 36 months | 19.18% / 1.49 / -11.68% | 18.90% / 1.45 / -11.40% |

The rules interact: although each isolated test was promising, their combination
does **not** improve full-sample maximum drawdown (−29.28% versus −29.02%). The
user chose to promote this explicit combined configuration as `v1.3`; retain
v1.2 as the audit comparator and treat further drawdown claims as unproven until
walk-forward and industry-label placebo checks are complete.

### Validation addendum

The requested post-integration validation does **not** establish that v1.3
improves drawdown alongside CAGR. Its full-sample maximum drawdown occurs over
the same 2015-08-05 to 2016-05-24 episode as v1.2, but is worse: -29.28% versus
-29.01%. The spike filter alone reached -26.67% in that episode; the industry
cap changes the holdings enough to remove that benefit.

| Independent slice | v1.2: CAGR / Sharpe / DD | v1.3: CAGR / Sharpe / DD |
|---|---|---|
| 2005–2009 | 33.07% / 2.01 / -18.59% | 32.65% / 2.06 / -19.17% |
| 2010–2014 | 33.19% / 2.72 / -12.14% | 33.63% / 2.78 / -12.66% |
| 2015–2019 | 6.52% / 0.54 / -29.01% | 7.08% / 0.60 / -29.28% |
| 2020–2024 | 36.01% / 2.07 / -24.31% | 36.68% / 2.07 / -22.76% |
| 2025–end | -3.08% / -0.33 / -11.68% | -2.39% / -0.27 / -11.40% |

Execution stress is also mixed. At 0.6% per leg, v1.3 is 22.35% CAGR / 1.60
Sharpe / -30.67% DD versus v1.2's 21.96% / 1.55 / -30.42%. Under a one-day
extra delay it is 25.42% / 1.77 / -24.96% versus 23.49% / 1.62 / -25.99%; under
a two-day delay it is 24.29% / 1.68 / -25.78% versus 22.85% / 1.57 / -25.81%.
Thus the return/Sharpe improvement is robust to these stresses, but the desired
base/cost drawdown improvement is not.

For the industry-cap falsification check, true `Industry_clean` labels produced
24.90% CAGR / 1.72 Sharpe / -28.84% DD in isolation. Three label permutations
(seeds 1, 7, 19) produced CAGRs of 23.79%, 23.88%, and 23.26%, respectively;
their DDs were -29.27%, -28.30%, and -29.97%. Real labels appear useful for
return quality, but the small sample does not prove a robust drawdown effect.

**Validation conclusion:** retain the implementations and v1.2 comparator, but
do not claim v1.3 has solved maximum drawdown. A production-default decision
should favour v1.2 until a configuration improves both measures without relying
on the interaction that failed above.

## Reproduction

```bash
cd csm_aegis
python3 csm_aegis_backtest.py --preset v1.2 --set entry_spike_filter=True
python3 csm_aegis_backtest.py --preset v1.2 --set stop_from_entry=0.10 --set stop_cooldown_days=20
python3 csm_aegis_backtest.py --preset v1.2 --set w_hi=0.05
python3 csm_aegis_backtest.py --preset v1.2 --set entry_path_filter=True
python3 csm_aegis_backtest.py --preset v1.2 --set industry_cap=2
python3 csm_aegis_backtest.py --preset v1.2 --set industry_cap=2 --set industry_label_seed=1
python3 csm_aegis_backtest.py --preset v1.3
```

Parameterized runs receive their own output-file tag and cannot overwrite the
frozen v1.2 result files.

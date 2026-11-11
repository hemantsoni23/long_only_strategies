# residual_momentum_v2 — standalone residual momentum research strategy

**What it is.** A self-contained target-weight generator and event-driven backtest. It
contains its strategy engine in `residual_momentum_v2_strategy.py`; it does not
import the old strategy directory or any other project file. V2 adds the 50–1000
liquidity rank band, the entry-spike filter and a simulated ETF cash sweep.

**Live deployment status: not an automated live-trading system.** This package does not
connect to a broker, reconcile holdings, submit or monitor orders, persist stop state, or
execute a gold sweep. The backtest uses whole shares and ETF units, but does not model
settlement delays. Its drawdown and ATR exits only run inside the simulator. A broker-specific execution and reconciliation layer, market calendar and
operational testing are required before using real money. `get_positions()` returns
historical target weights, not executable orders. It treats the last available date of
each month as a month end, including a partial final month, so a live scheduler must
explicitly verify that the session is the actual final exchange session before using a
monthly signal.

**Historical results below are obsolete research records.** They predate fixes for ETF
funding, transaction costs, stale fills, cash interest, first-day returns and CAGR. They
also predate correction of an ETF timestamp shift. Re-run the current code; do not use
the tables below as current estimates.

**Cost and income model.** Stock and ETF orders both use the same assumed 15 bps
per-side fixed charge plus participation-based impact, subject to a 25%-of-ADV daily
cap on rebalance and ETF trades. Stop exits use a 75 bps charge and a 5%-of-ADV
daily cap. This fixed charge is an aggregate assumption for costs, not an itemized or verified
brokerage, tax and exchange fee schedule. ETF costs and stock costs are reported
separately. ETF ADV uses previous-session close and volume. Idle cash earns 0%, and the
runner reports a zero-interest cash comparison over the same period. Dividends are not
credited; corporate actions need independent verification. Integer fills on adjusted
historical prices are an approximation of historical share counts. Immediate conversion
and the absence of settlement delays remain approximations.

## Files and setup

- `residual_momentum_v2_strategy.py`: data loading, signal and target weights; this file
  can be copied alone into an existing compatible live integration.
- `residual_momentum_v2_backtest.py`: simulation and reporting.
- `run_residual_momentum_v2.py`: backtest runner.
- `requirements.txt`: runtime dependencies; research validation additionally needs
  `statsmodels`, and optional plotting needs `matplotlib`.

Copy the full directory and install `python3 -m pip install -r requirements.txt`.
Stock data consists of per-symbol CSVs with `datetime,open,high,low,close,volume`;
set `RESIDUAL_MOM_DATA_DIR` or pass `--data-dir`. ETF CSVs use
`timestamp,open,close,volume`; set `RESIDUAL_MOM_ETF_DATA_DIR`. Timestamps are interpreted
in Asia/Kolkata. Both environment variables must be set before starting Python.
Without overrides the legacy paths point to the original development machine.
With no arguments the sweep runner limits its end date to the last ETF bar and selects
the latest continuous period of ETF data for the default report start. The supplied
GOLDBEES CSV has no data from 2011 through 2014 and ends on 2026-07-31; with these files
the default sweep therefore starts in 2015 and ends in July 2026. Individual missing
ETF sessions are valued at the previous close and no ETF trades are executed on those
sessions; the runner reports the affected count. Stock orders require a valid same-day
open; a missing bar cannot trigger a fill. Gaps longer than seven calendar days are rejected, as is extrapolation beyond ETF coverage.
Explicit `--report-start` and `--data-end` requests are not silently shortened. Use
`--cash-sweep-etf none` for a stock-only backtest across the available stock history.

Run tests with `python3 -m unittest -v test_standalone` from this directory.

V2 defaults are rank 50–1000, the 5-day 80th-percentile entry-spike filter and
GOLDBEES sweep. The simulation now differs from the original engine because it enforces
funding and execution constraints.

## 1. Universe band: why it changed

Reading every sibling book's own live-runner config in `Old_live_strategies` (not guessed):

| Book | Live universe band (rank by liquidity) |
|---|---|
| Zenith / Elendel / csm_absolute | 1–1000 |
| **HR breakout** | **1–500 — identical to residual momentum's old band** |
| csm_quad / VCP | 500–1000 |
| Residual momentum (old) | 1–500 |

Residual momentum's old pool was a strict subset of 3 books' pools and bit-identical to a
4th's — structurally the most crowded band in the repo.

**What the liquidity floor allows:** candidates were screened under the SAME `min_price=20` /
`min_adv=1e7` tradability floor (not relaxed — that's a live-execution constraint, not an
overlap dial):

| Band | Avg names/month | Min names/month | Months with <80 names (of 297) |
|---|---|---|---|
| current (1-500) | 324 | 2 | 29 |
| widen only (1-1000) | 435 | 2 | 29 |
| shift+widen (300-1200) | 222 | 0 | 153 |
| shift+widen (400-1500) | 188 | 0 | 195 |
| disjoint-from-HR (500-1500) | 149 | 0 | 213 |
| **trim top 50 (50-1000) — adopted** | 389 | 0 | 43 |
| trim top 100 (100-1000) | 344 | 0 | 61 |

**Finding: full non-overlap with Zenith/Elendel/csm_absolute's 1-1000 pool is not achievable**
— the actually-tradable (≥₹20, ≥₹1cr/day) universe in this data often doesn't reach
1000-1500 names, especially pre-2010, so shifting the lower bound past ~500 breaks the
enter/exit-rank(30/80) hysteresis for a large share of history. **rank 50-1000** is the
best-evidenced compromise: trims only the ~50 most extreme-liquidity names (the tier every
book in the repo would include first if it screens well — the highest crowding-risk slice),
nearly doubles breadth, and real thin-month cost is modest (43 vs 29 months, concentrated
pre-2010).

**Measured overlap reduction** (holdings-level, not just band arithmetic): the average share
of residual momentum's own monthly holdings that also sit inside HR breakout's exact rank≤500
band drops from **99.8% → 88.8%**. About 1 in 9 of v2's holdings each month are now names HR
breakout cannot hold at all under its current config — real, if modest, diversification.

## 2. Entry-spike filter + universe band combined: results

Full history, 2002–2026, AUM=Rs50cr (the project's earlier backtest default — see §4 for why
the real AUM changes the exposure/CAGR picture a lot):

| Variant | CAGR | Sharpe | MaxDD | Calmar | post-2020 CAGR | post-2020 Sharpe | Win rate |
|---|---|---|---|---|---|---|---|
| Baseline (live, 1-500) | 15.90% | 1.15 | −15.6% | 1.02 | 18.70% | 1.37 | 56.1% |
| Universe-only (50-1000) | 14.17% | **1.23** | **−13.4%** | **1.06** | 16.05% | 1.39 | 56.8% |
| Spike-filter-only (1-500) | **16.16%** | 1.19 | −15.7% | 1.03 | 18.31% | 1.38 | **58.5%** |
| **V2 combined (50-1000 + spike)** | 13.64% | 1.14 | −13.8% | 0.99 | 16.74% | **1.43** | 56.8% |

**Honest finding: the two changes do not combine additively.** Each alone improves a
different axis (universe → risk-adjusted/drawdown; spike filter → return/win-rate); combined,
full-sample CAGR and Calmar sit slightly *below* either individual change — likely because the
spike filter's 80th-percentile threshold is computed within whatever universe is active, and
the wider, more volatile 50-1000 pool has a more extreme 5-day-return distribution than the
calmer top-500, so the *same* cutoff blocks a different, more aggressive set of candidates
once the universe changes. **Not re-tuned** for the new universe — that would be an
unregistered extra round of fitting. The combination still wins outright on **post-2020**
Sharpe/MaxDD (the regime where the 1m/3m signal was found to have decayed), which is why it
shipped as the default anyway.

## 3. Entry-spike-filter "fast damage" check

Trades losing ≥10% within 45 holding days ("false starts"): baseline 7.7% → spike-filtered
6.7%. STOP_HIT exit share also drops modestly as a side effect.

## 4. Exposure / cash deep-dive → why AUM matters enormously here

Instrumenting the live day-loop (byte-for-byte duplicate, cross-checked to match the real
engine's `net` to float precision) to recover daily cash/invested state the public engine
doesn't expose:

- At **Rs50cr** (the backtest default used in §2 above and throughout most of this project),
  average exposure is only ~22-29%, mostly because the 25%-of-21-day-ADV per-trade cap limits
  same-day fills to a 59-65% average fill rate with **no multi-day catch-up mechanism** — a
  capacity artifact of testing at a scale this strategy's universe can't support efficiently,
  not a real finding for a small account.
- At the **real intended AUM (Rs1 lakh)**, the ADV cap never binds (fill rate ~100-103%).
  Average exposure is a healthy ~50%, and the only material remaining driver is the trend gate
  (binary: ~69% exposure when on, ~10% when off, off ~33% of all days).
- **Practical caveat not modeled by this backtest**: 40 positions × ~2.5% weight ≈ Rs2,500
  each at Rs1 lakh AUM — NSE whole-share constraints mean higher-priced names get 1-2 shares,
  so realized weights will deviate from target more than this continuous-share backtest
  shows; these historical results used fractional units. Fixed per-trade costs
  (brokerage, STT) can also matter at this size.

This is why every result from here on is reported at **AUM=Rs1 lakh**, not Rs50cr.

## 5. Gold cash-sweep (adopted)

**What it is.** Every rupee of idle cash is swept into GOLDBEES instead of sitting idle:
every stock-side cash inflow (a sale, a stop-out) buys GOLDBEES units at that moment's price,
every outflow (a purchase) sells GOLDBEES units to fund it. No separate un-invested currency
exists in this mode (a deliberate simplification — real settlement needs a small T+1/T+2
buffer, not modeled). Data: GOLDBEES OHLCV from
`/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data/GOLDBEES.csv`, available
from 2007-03-19 onward — so a v2+gold backtest window is restricted to 2007-04-01 onward, ~5
years shorter than the pure-equity v2's 2002-2026 range.

**Results** (2007-04-01 → 2026-09-04, AUM=Rs1 lakh):

| | CAGR | Sharpe (rf=0%) | Sharpe (rf=6.5%) | Sortino (rf=0%) | Calmar | MaxDD |
|---|---|---|---|---|---|---|
| V2 equity-only (cash @ 0%) | +24.37% | 1.88 | 1.34 | 1.80 | 1.15 | −21.10% |
| **V2 + GOLDBEES sweep** | **+33.03%** | 1.82 | **1.43** | **2.06** | **1.56** | −21.18% |

Both rf conventions shown per this project's research standard (never quote one risk-free
assumption alone). At rf=0% the two are a near-wash on Sharpe with gold far ahead on
CAGR/Sortino/Calmar for essentially no extra drawdown; at the more conservative rf=6.5%
convention gold's much higher return pulls it **ahead** on Sharpe too (1.43 vs 1.34).

**What was tested and rejected before adopting this version:**
- **NIFTYBEES sweep** (broad equity ETF): catastrophic — MaxDD −18.7% → **−61.6%**.
  Reintroduces full market risk exactly during the periods the trend gate exists to avoid.
- **Conditional gold sweep** (GOLDBEES only while the trend gate is off, plain cash
  otherwise): intuitively the "smarter" design, targeting gold specifically at the de-risked
  regime — but **worse than the always-on sweep on every risk metric** (Sharpe 1.34, MaxDD
  −34.9%, Calmar 0.84 at rf=6.5%; 2022 alone cost it −24.0% vs the always-on version's −7.6%).
  Concentrating gold exposure into gate-off windows concentrates gold's *own* volatility
  there too, instead of diversifying it away — the crash-hedge hypothesis did not hold up.
- **LIQUIDBEES sweep** (the real money-market alternative): its OHLC price series is
  essentially flat (liquid funds distribute yield via unit accrual/dividends, not NAV
  appreciation), so this data can't measure its true yield — the original 6% assumption is a
  better proxy for "if a real liquid-fund sweep is already available to you." The choice
  between gold and a real liquid-fund sweep is then a genuine preference (gold: more return,
  more volatility); gold is the clear win specifically if idle cash is truly earning ~0% today.
- **Silver (SILVERBEES)**: only 4.5 years of data (2022+) — too short to trust. Offered as a
  configurable option (`cash_sweep_etf="SILVERBEES"`), not recommended as a default.

## 6. Deliberately NOT changed (tested and rejected)
- **Tighter breaker** (0.15-0.20 vs the live default 0.25): trades CAGR/Sharpe for lower
  MaxDD — a risk preference, not a strict win.
- **Slower single-book rebalance** (2-3 months): strictly worse on every metric.
- **True staggered 3-tranche rebalancing**: roughly flat-to-worse on Sharpe/Calmar, turnover
  saving far below the literature's estimate.
- **Graded trend gate** (replacing the binary 150-day-SMA switch with a continuous logistic
  scaler, slope pre-registered at 2.0 per `STRATEGY_IMPROVEMENT_IDEAS.md` E1): a clean loss on
  every metric (CAGR +23.70%→+19.26%, Sharpe 1.49→1.34, MaxDD −18.7%→−20.6%, Calmar 1.27→0.94,
  win rate 57.1%→50.3%). It also did the opposite of what was intended — average exposure fell
  (42.7%→38.4%), not rose, because the logistic curve shaves exposure during ordinary bull
  markets (common) more than it adds during bear markets (rarer), and changing the exposure
  multiplier every month rather than only at regime flips roughly tripled stop-outs
  (223→602). Not adopted.

## Usage

```sh
export RESIDUAL_MOM_DATA_DIR=/path/to/stock_csvs
export RESIDUAL_MOM_ETF_DATA_DIR=/path/to/etf_csvs
python3 run_residual_momentum_v2.py --data-end 2026-07-31
python3 run_residual_momentum_v2.py --cash-sweep-etf none
python3 run_residual_momentum_v2.py --cash-sweep-etf SILVERBEES --data-end 2026-07-31
```

Specify an end date covered by **your** data. Gold and silver ETF data may have
different coverage. Sweep trade statistics use its own stock sale fills, with partial
sales recorded separately; end-of-period holdings are marked to market. ETF order counts
and aggregate costs are displayed, and the strategy object exposes `cash_sweep_trades`
with each simulated ETF order. Cash-only trade statistics remain approximate for partial
trims and do not incorporate all trading costs.

## Caveats
- Parameters (5-day spike lookback, 0.80 quantile, rank 50-1000) are each independently
  evidenced but not jointly optimized (see §2's interaction finding).
- All numbers are in-sample on the same panel used throughout this project; there is no
  separate lockbox. Only forward paper-trading is true out-of-sample.
- Survivorship: only currently-listed-name history, same caveat as the rest of this repo.
- The gold-sweep backtest window (2007-2026) is shorter than the pure-equity v2's (2002-2026)
  because GOLDBEES data starts in 2007; §2's table and §5's table are NOT over identical
  windows or AUM — each section's own table is internally consistent, the two sections are not
  directly comparable to each other.
- Gold's recent historic bull run (2019-2021, 2024-2025) contributes real return to these
  numbers; some of the edge over cash is genuine diversification, some is this specific
  sample period's commodity cycle — not separable with the data available here.
- Backtested trade logs and win rates depend on how partial exits are counted; the
  cash-only trade log is approximate. Dividends are not credited.

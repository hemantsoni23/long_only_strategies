# Crestline

Cross-sectional trend-leadership strategy for Indian equities, plus a capped gold-ETF sleeve for idle capital. One strategy file, one test file, one evaluation tool.

## Files
| file | purpose |
|---|---|
| `crestline_v2_6.py` | the strategy + backtest + report (read the docstring first) |
| `test_crestline.py` | behaviour tests; `--parity` also proves identity with the frozen reference `research_archive/crestline_v2_6_precleanup.py` |
| `anchor_report.py` | (caches runs in the disposable `.anchor_cache/`) runs the 6 schedule anchors in parallel and prints the per-anchor table, the mean and the staggered blend: **the way to quote results** |
| `docs/` | the research record: reports + pre-registrations (`LINEAGE.md` first) |
| `research_archive/` | research scripts, generators, intermediate versions and result tables (not needed to run the strategy) |
| `../Crestine/crestline_v2_2.py` | the colleague's original, never edited |

## Run (from the repo root, `long_only_strategies/`)
```bash
python3 crestline_review/crestline_v2_6.py                                        # default: EXIT_MODE=zenith, TOP_N=25, gold sleeve 25%, idle cash 0%
CL_OVR='{"EXIT_MODE":"honest"}' python3 crestline_review/crestline_v2_6.py        # honest next-open booking
CL_OVR='{"GOLD_TARGET_RET":0.08}' python3 crestline_review/crestline_v2_6.py      # gold re-centred to 8%/yr (planning scenario)
python3 crestline_review/anchor_report.py '{"EXIT_MODE":"honest"}'           # 6 anchors + staggered blend for any config
python3 crestline_review/test_crestline.py                                   # ~3 min;  add --parity for the bit-exact check (~10 min)
```
Environment: `CL_OVR` (JSON config overrides; unknown keys are rejected), `CL_OUT` (output folder), `CRESTLINE_OFFSET` (schedule anchor in bars). Outputs per run: `equity_curves.csv`, `daily.csv` (equity, stock exposure, gold weight, bear/panic flags), `trade_log_full.csv`, `yearly_returns.csv`, `icir_report.csv`, `exit_reason_summary.csv`, `summary.json`.

## Key parameters (`CL_OVR` keys)
`TOP_N` (25) | `REBALANCE_FREQ_DAYS` (60) | `EXIT_RANK_MULT` (2) | `PEAK_STOP_PCT` (.15) | `VOLSTOP_K / _MIN_PCT / _MAX_PCT` (2.5 / .10 / .25) | `EXIT_MODE` | `BEAR_SCALE`, `PANIC_SCALE` (.6, .3) | `GOLD_CAP` (.25; 0 = off) | `GOLD_TARGET_RET` | `INITIAL_CAPITAL` (1e5; **set it to the real book size - the 5% ADV cap never binds at 1 lakh**) | `COST_ONE_WAY` (.003) | `CASH_RATE_ANNUAL` (0) | `MIN_PRICE`, `UNIVERSE_TOP_N_MIN/MAX` | `HP_WINDOW`, `TP_LOOKBACK`, `TP_SMA_WINDOW` | `START_DATE`, `END_DATE`.

## Conventions you must keep when quoting a number
1. Idle cash earns 0%; Sharpe at rf = 0.
2. Quote the mean over the 6 schedule anchors (and the range), not anchor 0 alone; use 2006-2025, not 2015-2025 alone.
3. `EXIT_MODE=zenith` hides P&L (`Exit P&L NOT booked %/yr` is printed on every run): always show the `honest` result beside it.
4. Gold results depend on gold's sample return (~17%/yr INR in the usable 2007-10 + 2015-25 data): show them under `GOLD_TARGET_RET=0.08` as well as real.
5. Results at 1 lakh are small-book numbers; report the book size you mean (1 cr / 5 cr / 20 cr change CAGR from ~17% to ~6%).

## Known limitations (not modelled or not fixable with this data)
Gold/silver ETF files are empty for 2011-2014 (sleeve is off then); silver has only 2022-25 and is not used. Vendor opening prints (stocks and ETFs) are used as fills; whether stop-exit fills at stock opens are achievable is unverified. No market impact beyond the flat 0.3% per side, no taxes, locked circuits at the open are not modelled for entries. Survivorship (almost only currently listed names), thin pre-2020 volume (ADV caps/liquidity ranks distorted early), a single gold bull market, and everything is in-sample (no lockbox): only forward paper trading is out-of-sample.

# CSM ESR (Earnings Surprise & Reaction)

Previously named `csm_pead`. This event-driven research strategy looks for a
quarterly earnings surprise that is accompanied by a strong share-price
reaction. It uses company results as its starting signal and price data as a
second selection condition, as well as for trading and risk management.
The price reaction is measured from the last close on or before the filing
date through the close of the second trading session strictly after it. The
result is never used on its filing date.

Read [STRATEGY_LOGIC.md](STRATEGY_LOGIC.md) for the full step-by-step rules,
formulas, timing, examples, portfolio management, exits and limitations.
See [IMPROVEMENT_REVIEW.md](IMPROVEMENT_REVIEW.md) for the prioritized review
of confirmed problems, research gaps and ideas to test.

## Run

From the repository root:

```bash
python3 csm_esr/run_tests.py
python3 csm_esr/run_csm_esr_backtest.py
```

The runner defaults to reporting 1 September 2020 through 31 December 2024.
An earlier start and/or end can be specified with `--start YYYY-MM-DD` and
`--end YYYY-MM-DD`; the end cannot exceed 2024-12-31. The daily and trade logs,
transactions and charts are written to `output/`. Set `CSM_ESR_OUTPUT_DIR`
to change the output directory. Set `CSM_FUNDAMENTALS_DIR` to use another
compatible fundamentals directory.

The trade log includes `Filed`, `Reaction_Base_Date`, `Available_Date`,
`Signal_Date` and `Entry_Date` so the timing of each completed trade can be
checked directly.

## Folder guide

| File or folder | Purpose |
| --- | --- |
| `STRATEGY_LOGIC.md` | Complete description of the implemented default rules. |
| `IMPROVEMENT_REVIEW.md` | Evidence-based problems and possible improvements. |
| `esr_strategy.py` | Signals, selection, portfolio, execution and exits. |
| `esr_fundamentals.py` | Point-in-time quarterly earnings events. |
| `run_csm_esr_backtest.py` | Main runnable backtest and performance report. |
| `backtest_data.py` | Loads prices and builds the market comparison series using the shared CSM Value loader. |
| `backtest_report.py` | Report and chart formatting. |
| `run_tests.py` and `tests/` | Regression checks for filing dates, execution and accounting. |
| `output/` | Results from the renamed strategy's latest backtest. |

Older outputs, diagnostics and scripts that use historical assumptions were
preserved in `research/csm_pead_legacy_20261117/`. They are an archive, not the
active strategy. Earlier documents may still refer to the former `csm_pead/`
path. This strategy is research; its past results are not independent proof of
future performance.

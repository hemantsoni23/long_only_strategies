# CSM Aegis v1.4 low-drawdown — testing handoff

The production implementation is contained in:

- `csm_aegis_strategy.py` — deterministic signals, universe, selection, ADX/DMI gate, stops, and execution eligibility.
- `csm_aegis_backtest.py` — event-driven booking, GOLDBEES sleeve, regime leverage, reports, and command-line runner.

The `*_experiment.py` files are research artifacts and are not required to execute v1.4.

## Install

```bash
python3 -m pip install -r requirements.txt
```

## Required data

Daily per-symbol OHLCV files must be CSVs with these columns:

```text
datetime,open,high,low,close,volume
```

The v1.4 sleeve also requires `GOLDBEES.csv` with:

```text
timestamp,open,high,low,close,volume
```

The v1.4 industry cap requires an instruments CSV with `trading_symbol` and
`Industry_clean` columns. Give all locations explicitly when testing:

```bash
python3 csm_aegis_backtest.py \
  --preset v1.4_low_dd \
  --data-folder /path/to/daily_ohlcv \
  --etf-data-folder /path/to/gold_silver_ohlcv \
  --industry-labels-file /path/to/instruments_clean.csv \
  --output-dir /path/to/csm_aegis_output \
  --no-cache \
  --no-plot
```

Equivalent environment variables are `CSM_AEGIS_DATA_FOLDER`,
`CSM_AEGIS_ETF_DATA_FOLDER`, and `CSM_AEGIS_INSTRUMENTS_FILE`.

## Expected characteristics

With the supplied research panel through 2026-07-17 and 0.3% cost per leg,
v1.4 starts when GOLDBEES data begins (2007-03-19). Its reference result is
about 24.11% CAGR, 1.51 Sharpe, and -24.4% max drawdown. Small differences can
occur only if the source OHLCV or instrument labels differ.

Every run writes a `run_manifest_*.json` that records parameters, input paths,
panel coverage, dependency versions, and headline metrics. Preserve this file
with reported results.

## Required checks

```bash
python3 test_execution_integrity.py
python3 test_secondary_etf.py
```

The first verifies raw-bar stock entries/exits. The second verifies v1.4 stock
and ETF transactions, cash accounting, regime leverage, and deferred ETF fills.

## Execution rules to verify

- A stock/ETF fill needs positive raw close, positive volume, valid high/low,
  and `high != low`; forward-filled prices are marks only.
- Unfillable stock exits remain pending until a valid later bar.
- GOLDBEES cash-sweep and ETF funding orders are deferred on unusable ETF bars.
- Idle cash does not receive a risk-free return.
- ADX/DMI affects fresh entries only; it never forces an existing holding out.

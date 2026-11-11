#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v3/validation_2026_11_06/evidence
python3 -u "$D/replay.py" early universe > "$D/early_universe.log" 2>&1
for w in early late; do
 python3 -u "$D/replay.py" "$w" sweep > "$D/${w}_sweep.log" 2>&1
 python3 -u "$D/signal_diagnostics.py" "$w" > "$D/signal_${w}.log" 2>&1
done
for w in playbook_early playbook_late full; do
 python3 -u "$D/replay.py" "$w" baseline > "$D/${w}.log" 2>&1
done
for w in playbook_early playbook_late; do
 python3 -u "$D/signal_diagnostics.py" "$w" > "$D/signal_${w}.log" 2>&1
done
python3 -u "$D/causality.py" > "$D/causality.log" 2>&1
python3 -u "$D/exit_diagnostics.py" > "$D/exit.log" 2>&1
python3 -u "$D/verify_strategy_parity.py" > "$D/parity.log" 2>&1
CELL_ONLY=band_500_1000,positions_36,positions_42 python3 -u "$D/replay.py" late probe > "$D/raw_probe.log" 2>&1
CELL_ONLY=band_500_1000,positions_36,positions_42 EXCLUDE_TICKERS=TIL python3 -u "$D/replay.py" late probe > "$D/no_TIL_probe.log" 2>&1
for w in playbook_early playbook_late; do
 python3 -u "$D/replay.py" "$w" sweep > "$D/${w}_sweep.log" 2>&1
done
python3 -u "$D/etf_coverage.py" > "$D/etf_coverage.log" 2>&1
python3 -u "$D/postprocess.py" > "$D/postprocess.log" 2>&1
python3 -u "$D/verify_snapshot.py" > "$D/snapshot_verification.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1
python3 -u "$D/native_main_comparison.py" > "$D/native_main.log" 2>&1
python3 -u "$D/replay.py" parity baseline > "$D/parity_window.log" 2>&1
NATIVE_START=2005-01-01 NATIVE_END=2015-12-31 NATIVE_TAG=default python3 -u "$D/native_main_comparison.py" > "$D/native_default.log" 2>&1

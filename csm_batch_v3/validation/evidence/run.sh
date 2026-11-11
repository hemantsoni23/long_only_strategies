#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export IC_DATA_FOLDER=/private/tmp/csm_batch_v3_validation_snapshot/ohlcv
D=csm_batch_v3/validation/evidence
for w in late early; do
 python3 -u "$D/replay.py" "$w" universe > "$D/${w}_universe.log" 2>&1
 python3 -u "$D/replay.py" "$w" sweep > "$D/${w}_sweep.log" 2>&1
 python3 -u "$D/signal_diagnostics.py" "$w" > "$D/signal_${w}.log" 2>&1
done
for w in playbook_early playbook_late full; do
 python3 -u "$D/replay.py" "$w" baseline > "$D/${w}.log" 2>&1
done
for w in playbook_early playbook_late; do
 python3 -u "$D/signal_diagnostics.py" "$w" > "$D/signal_${w}.log" 2>&1
done
python3 -u "$D/prefix_parity.py" > "$D/prefix.log" 2>&1
python3 -u "$D/exit_diagnostics.py" > "$D/exit.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1

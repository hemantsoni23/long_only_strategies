#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
export IC_DATA_FOLDER=/private/tmp/csm_batch_v3_validation_snapshot/ohlcv
D=csm_batch_v3/validation/evidence
for w in playbook_early playbook_late; do
 python3 -u "$D/replay.py" "$w" sweep > "$D/${w}_sweep.log" 2>&1
done
for w in early late; do
 python3 -u "$D/replay.py" "$w" adx > "$D/${w}_adx.log" 2>&1
done
python3 -u "$D/native_main_comparison.py" > "$D/native_main.log" 2>&1
python3 -u "$D/mask_signal_sensitivity.py" > "$D/mask_signal.log" 2>&1

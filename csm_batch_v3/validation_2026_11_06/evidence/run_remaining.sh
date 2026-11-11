#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v3/validation_2026_11_06/evidence
python3 -u "$D/native_main_comparison.py" > "$D/native_main.log" 2>&1
python3 -u "$D/replay.py" parity baseline > "$D/parity_window.log" 2>&1
NATIVE_START=2005-01-01 NATIVE_END=2015-12-31 NATIVE_TAG=default python3 -u "$D/native_main_comparison.py" > "$D/native_default.log" 2>&1
python3 -u "$D/verify_snapshot.py" > "$D/snapshot_verification.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1

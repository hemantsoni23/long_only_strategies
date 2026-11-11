#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v2/validation_v3/evidence
printf 'Original data: band 501–1000 and 36/42 stocks\n'
CELL_ONLY=band_500_1000,positions_36,positions_42 python3 -u "$D/replay.py" late probe > "$D/raw_probe.log" 2>&1
printf 'TIL excluded in memory: same settings\n'
CELL_ONLY=band_500_1000,positions_36,positions_42 EXCLUDE_TICKERS=TIL python3 -u "$D/replay.py" late probe > "$D/no_TIL_probe.log" 2>&1
python3 -u "$D/outliers.py" > "$D/outliers.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1
printf 'Extra probes complete\n'

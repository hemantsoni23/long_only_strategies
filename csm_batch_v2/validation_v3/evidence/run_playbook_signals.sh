#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v2/validation_v3/evidence
printf 'Playbook early signal\n'
python3 -u "$D/signal_diagnostics.py" playbook_early > "$D/signal_playbook_early.log" 2>&1
printf 'Playbook late signal\n'
python3 -u "$D/signal_diagnostics.py" playbook_late > "$D/signal_playbook_late.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1
printf 'Supplemental signal tests complete\n'

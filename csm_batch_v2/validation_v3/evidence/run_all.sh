#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v2/validation_v3/evidence
printf 'Universe sweep: 2015–2025\n'
python3 -u "$D/replay.py" late universe > "$D/universe.log" 2>&1
printf 'Parameter and ablation sweep: 2005–2014\n'
python3 -u "$D/replay.py" early sweep > "$D/early_sweep.log" 2>&1
printf 'Parameter and ablation sweep: 2015–2025\n'
python3 -u "$D/replay.py" late sweep > "$D/late_sweep.log" 2>&1
printf 'Playbook split baselines\n'
python3 -u "$D/replay.py" playbook_early baseline > "$D/playbook_early.log" 2>&1
python3 -u "$D/replay.py" playbook_late baseline > "$D/playbook_late.log" 2>&1
printf 'Full-sample baseline\n'
python3 -u "$D/replay.py" full baseline > "$D/full.log" 2>&1
printf 'Suspicious ticker tests\n'
CELL_ONLY=band_500_1000,positions_36 python3 -u "$D/replay.py" late probe > "$D/raw_probe.log" 2>&1
CELL_ONLY=band_500_1000,positions_36 EXCLUDE_TICKERS=TIL python3 -u "$D/replay.py" late probe > "$D/no_TIL_probe.log" 2>&1
python3 -u "$D/outliers.py" > "$D/outliers.log" 2>&1
printf 'Signal and decay: 2005–2014\n'
python3 -u "$D/signal_diagnostics.py" early > "$D/signal_early.log" 2>&1
printf 'Signal and decay: 2015–2025\n'
python3 -u "$D/signal_diagnostics.py" late > "$D/signal_late.log" 2>&1
printf 'Signal and regime prefix invariance\n'
python3 -u "$D/causality.py" > "$D/causality.log" 2>&1
printf 'Exit diagnostics\n'
python3 -u "$D/exit_diagnostics.py" > "$D/exit.log" 2>&1
printf 'Year and cost sensitivity\n'
python3 -u "$D/postprocess.py" > "$D/postprocess.log" 2>&1
printf 'Data audit and fingerprint\n'
python3 -u "$D/data_audit.py" > "$D/data_audit.log" 2>&1
python3 -u "$D/fingerprint.py" after > "$D/fingerprint.log" 2>&1
printf 'All runs complete\n'

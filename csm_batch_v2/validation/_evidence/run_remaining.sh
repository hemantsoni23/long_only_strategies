#!/bin/sh
set -eu
export PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1
D=csm_batch_v2/validation/_evidence
printf 'Parity replay\n'
python3 -u "$D/backtest.py" parity baseline > "$D/parity.log" 2>&1
printf 'Original runner replay\n'
PYTHONPATH="$PWD/csm_batch_v2" python3 -u "$D/runner_snapshot.py" > "$D/reference_runner.log" 2>&1
python3 "$D/check_parity.py" > "$D/parity_check.log" 2>&1
printf 'Late-period sweeps\n'
python3 -u "$D/backtest.py" late sweep > "$D/late.log" 2>&1
printf 'Full-sample baseline\n'
python3 -u "$D/backtest.py" full baseline > "$D/full.log" 2>&1
printf 'Suspicious-price sensitivity\n'
CELL_ONLY=band_500_1000,positions_36 python3 -u "$D/backtest.py" late probe > "$D/probe.log" 2>&1
python3 -u "$D/outliers.py" > "$D/outliers.log" 2>&1
printf 'Early signal tests\n'
python3 -u "$D/signal_checks.py" early > "$D/early_signal.log" 2>&1
printf 'Late signal tests\n'
python3 -u "$D/signal_checks.py" late > "$D/late_signal.log" 2>&1
printf 'Exit tests\n'
python3 -u "$D/exit.py" > "$D/exit.log" 2>&1
python3 "$D/check_version.py" > "$D/version_check.log" 2>&1
python3 "$D/check_data_unchanged.py" > "$D/data_unchanged.log" 2>&1
printf 'Runs complete\n'

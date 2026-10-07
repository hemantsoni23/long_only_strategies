"""
Runs the live Zenith / Elendel runner end-to-end (its own data loading, logging, plots, metrics) with the residual-momentum-tilted class swapped in.
Nothing in Old_live_strategies is modified or written to: the runner module's output directory and version tag are redirected here.

    python3 run_resid_tilt_backtest.py zenith            # or elendel;  --weight 0.5  --mode event_driven|live
"""
import argparse
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from resid_tilt_strategies import CSMZenithResid, CSMElendelResid, LIVE   # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument('which', choices=['zenith', 'elendel'])
ap.add_argument('--weight', type=float, default=0.5)
ap.add_argument('--mode', default=None)
ap.add_argument('--start', default='2001-01-01'); ap.add_argument('--end', default='2026-07-16'); ap.add_argument('--report', default='2003-01-01')
a = ap.parse_args()

mod = importlib.import_module(f'run_csm_{a.which}_backtest')
out = os.path.join(HERE, 'output'); os.makedirs(out, exist_ok=True)
mod.OUTPUT_DIR = out                                   # keep every file out of Old_live_strategies/output
mod.VERSION_TAG = f'{a.which}_resid{a.weight:g}'
cls = {'zenith': CSMZenithResid, 'elendel': CSMElendelResid}[a.which]
setattr(mod, 'CSMZenith' if a.which == 'zenith' else 'CSMElendel',
        lambda **kw: cls(resid_weight=a.weight, **kw))
mod.main(load_start=a.start, load_end=a.end, start_report=a.report, mode=a.mode)

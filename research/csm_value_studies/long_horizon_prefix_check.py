"""Compare chosen long-horizon signals and returns with a 2023 data prefix."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('live_study', ROOT / 'research/csm_value_live_signals/study.py')
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
import run_csm_value_backtest as rb

END = pd.Timestamp('2023-12-29')
PROFILE = {'top_n': 20, 'buffer_ratio': 1., 'max_weight_per_stock': .05,
           'risk_pct_per_trade': .0075, 'hard_stop_from_peak': .20,
           'fill_weight_caps': False}
MODES = {'value': {'ranking_mode': 'value', 'leverage_bear': .8,
                   'rebalance_exit_buffer_months': 2, 'vol_target': .20},
         'experimental': {'ranking_mode': 'value_growth_pullback', 'leverage_bear': .5,
                          'rebalance_exit_buffer_months': 3, 'vol_target': .22}}


def run(data, results, end, mode):
    st = live.core.make_strategy(data, results, end)
    for key, val in {**PROFILE, **MODES[mode]}.items():
        setattr(st, key, val)
    if mode == 'experimental':
        st.components = ('EP', 'PROFIT_GROWTH', 'PULLBACK')
        st.calculate_factors()
    st.get_positions()
    res = rb.backtest_event_driven(st, transaction_cost=.003, risk_free_rate=0.)
    return st.factors.copy(), st.positions.copy(), res['executed_weights'].copy(), res['net_returns'].copy()


def max_difference(a, b):
    if not a.index.equals(b.index) or (isinstance(a, pd.DataFrame) and not a.columns.equals(b.columns)):
        raise AssertionError('Prefix index or columns differ')
    if not np.array_equal(pd.isna(a), pd.isna(b)):
        raise AssertionError('Prefix missing-value patterns differ')
    diff = np.abs(a.to_numpy(dtype=float) - b.to_numpy(dtype=float))
    return float(np.nanmax(diff)) if np.isfinite(diff).any() else 0.


def main():
    tmp, results, data = live.make_inputs()
    out = {'prefix': str(END.date()), 'tolerance': 1e-10, 'modes': {}}
    try:
        for mode in MODES:
            full = run(data, results, live.core.CUTOFF, mode)
            prefix = run(data, results, END, mode)
            diffs = {}
            for label, f, p in zip(('factors', 'positions', 'executed_weights', 'net_returns'), full, prefix):
                # Monthly factor labels use calendar month-end, including the
                # label after the final actual December trading session.
                aligned = f.reindex(index=p.index)
                if isinstance(p, pd.DataFrame):
                    extra = aligned.columns.difference(p.columns)
                    if len(extra):
                        earlier = aligned[extra]
                        if label == 'factors':
                            if earlier.notna().any().any():
                                raise AssertionError(f'{mode}: future-only symbols have earlier factor values')
                        elif earlier.fillna(0).abs().to_numpy().max() > 1e-10:
                            raise AssertionError(f'{mode}: future-only symbols have earlier positions')
                    aligned = aligned.reindex(columns=p.columns)
                diffs[label] = max_difference(aligned, p)
                if diffs[label] > 1e-10:
                    raise AssertionError(f'{mode}: {label} differs by {diffs[label]}')
            out['modes'][mode] = diffs
            print('PREFIX', mode, json.dumps(diffs), flush=True)
        Path(__file__).with_name('long_horizon_prefix_checks.json').write_text(json.dumps(out, indent=2) + '\n')
    finally:
        tmp.cleanup()


if __name__ == '__main__':
    main()

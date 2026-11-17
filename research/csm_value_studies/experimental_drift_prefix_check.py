"""Check the drift-aware experimental runner against a 2023 data prefix."""
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'csm_value'))
import csm_value_experimental_strategy as exp
import run_csm_value_experimental_backtest as rb

spec = importlib.util.spec_from_file_location('live_study', ROOT / 'research/csm_value_live_signals/study.py')
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
END = pd.Timestamp('2023-12-29')


def run(data, results, end):
    prices, volumes, highs, lows, opens, valuations = [p.loc[:end] for p in data]
    prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens)
    strategy = exp.CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs,
                            lows_df=lows, opens_df=opens, benchmark_series=rb.build_benchmark(prices),
                            valuation_prices_df=valuations, results_df=results[results.filed <= end].copy())
    strategy.calculate_factors()
    strategy.get_positions()
    res = rb.backtest_event_driven(strategy, initial_capital=100000,
                                   transaction_cost=.003, risk_free_rate=0.)
    return (strategy.factors, strategy.positions, res['executed_weights'], res['net_returns'],
            res['turnover'], res['execution_book_value'])


def max_diff(full, prefix, name):
    full = full.reindex(prefix.index)
    if isinstance(prefix, pd.DataFrame):
        extra = full.columns.difference(prefix.columns)
        if len(extra):
            if name == 'factors' and full[extra].notna().any().any():
                raise AssertionError('future-only securities have earlier factor values')
            if name != 'factors' and full[extra].fillna(0).abs().to_numpy().max() > 1e-10:
                raise AssertionError('future-only securities have earlier holdings')
        full = full.reindex(columns=prefix.columns)
    if not full.index.equals(prefix.index) or not np.array_equal(pd.isna(full), pd.isna(prefix)):
        raise AssertionError(f'{name} index or missing-value pattern differs')
    differences = np.abs(full.to_numpy(dtype=float) - prefix.to_numpy(dtype=float))
    return float(np.nanmax(differences)) if np.isfinite(differences).any() else 0.


def main():
    tmp, results, data = live.make_inputs()
    try:
        full = run(data, results, live.core.CUTOFF)
        prefix = run(data, results, END)
        # Book NAV is in rupees; allow absolute floating-point tolerance in
        # addition to a strict relative tolerance because it grows over time.
        out = {}
        for label, a, b in zip(('factors', 'positions', 'executed_weights', 'net_returns',
                                'turnover', 'execution_book_value'), full, prefix):
            out[label] = max_diff(a, b, label)
            tolerance = 1e-6 if label == 'execution_book_value' else 1e-10
            if out[label] > tolerance:
                raise AssertionError(f'{label} prefix differs by {out[label]}')
        path = Path(__file__).with_name('experimental_drift_prefix_checks.json')
        path.write_text(json.dumps({'prefix_end': str(END.date()), 'max_absolute_differences': out}, indent=2) + '\n')
        print('PREFIX_CHECK', json.dumps(out), flush=True)
    finally:
        tmp.cleanup()


if __name__ == '__main__':
    main()

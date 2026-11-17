"""Explore longer holdings and equity exposure using only data through 2024.

The dataset has already influenced strategy selection; these are not holdout
results. The user's zero-exit-day-weight convention is retained. No minimum
holding period is imposed on protective exits.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('long_horizon_exposure_results.json')
spec = importlib.util.spec_from_file_location('live_study', ROOT / 'research/csm_value_live_signals/study.py')
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
import run_csm_value_backtest as rb

WINDOWS = {'full': ('2019-06-03', '2024-12-31'),
           'development': ('2019-06-03', '2021-12-31'),
           'previously_examined': ('2022-01-03', '2024-12-31'),
           'year_2024': ('2024-01-01', '2024-12-31')}

# Same scenario set for each ranking. Explicitly set both ceilings so that
# weight caps above 6.67% are not silently limited by the risk budget.
CASES = {
    'current': {},
    'cap10': {'top_n': 10, 'max_weight_per_stock': .10, 'risk_pct_per_trade': .015},
    'cap15': {'top_n': 15, 'max_weight_per_stock': .07, 'risk_pct_per_trade': .0105},
    'cap20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075},
    'buffer2': {'rebalance_exit_buffer_months': 2},
    'buffer3': {'rebalance_exit_buffer_months': 3},
    'rank_buffer_100pct': {'buffer_ratio': 1.0},
    'trail25': {'hard_stop_from_peak': .25},
    'trail30': {'hard_stop_from_peak': .30},
    'long10': {'top_n': 10, 'max_weight_per_stock': .10, 'risk_pct_per_trade': .015,
               'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1., 'hard_stop_from_peak': .25},
    'long15': {'top_n': 15, 'max_weight_per_stock': .07, 'risk_pct_per_trade': .0105,
               'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1., 'hard_stop_from_peak': .25},
    'long20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
               'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1., 'hard_stop_from_peak': .25},
    'long15_vol25': {'top_n': 15, 'max_weight_per_stock': .07, 'risk_pct_per_trade': .0105,
                     'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                     'hard_stop_from_peak': .25, 'vol_target': .25},
    'long20_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                     'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                     'hard_stop_from_peak': .25, 'vol_target': .25},
    # Capacity-filling weights leave less idle cash when enough eligible
    # securities exist, without violating per-stock caps or using leverage.
    'filled_long10': {'top_n': 10, 'max_weight_per_stock': .10, 'risk_pct_per_trade': .015,
                      'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                      'hard_stop_from_peak': .25, 'fill_weight_caps': True},
    'filled_long15': {'top_n': 15, 'max_weight_per_stock': .07, 'risk_pct_per_trade': .0105,
                      'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                      'hard_stop_from_peak': .25, 'fill_weight_caps': True},
    'filled_long20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                      'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                      'hard_stop_from_peak': .25, 'fill_weight_caps': True},
    'filled_long15_vol25': {'top_n': 15, 'max_weight_per_stock': .07, 'risk_pct_per_trade': .0105,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .25, 'fill_weight_caps': True, 'vol_target': .25},
    'filled_long20_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .25, 'fill_weight_caps': True, 'vol_target': .25},
    'filled_long20_vol25_corr95': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .25, 'fill_weight_caps': True, 'vol_target': .25,
                            'corr_guard_threshold': .95},
    'filled_long20_trail18_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .18, 'fill_weight_caps': True, 'vol_target': .25},
    'filled_long20_trail20_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'fill_weight_caps': True, 'vol_target': .25},
    'filled_long20_trail22_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .22, 'fill_weight_caps': True, 'vol_target': .25},
    'filled_long20_trail20_buffer3_vol25': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 3, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'fill_weight_caps': True, 'vol_target': .25},
    # Calibrate volatility limits and stops without the capacity-filling option.
    'long20_cal_t20_v20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'vol_target': .20},
    'long20_cal_t20_v22': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'vol_target': .22},
    'long20_cal_t20_b3_v20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 3, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'vol_target': .20},
    'long20_cal_t20_b3_v22': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 3, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .20, 'vol_target': .22},
    'long20_cal_t25_v20': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .25, 'vol_target': .20},
    'long20_cal_t25_v22': {'top_n': 20, 'max_weight_per_stock': .05, 'risk_pct_per_trade': .0075,
                            'rebalance_exit_buffer_months': 2, 'buffer_ratio': 1.,
                            'hard_stop_from_peak': .25, 'vol_target': .22},
}

MODES = {'value': {}, 'experimental': {'ranking_mode': 'value_growth_pullback',
         'components': ('EP', 'PROFIT_GROWTH', 'PULLBACK'),
         'max_weight_per_stock': .10, 'risk_pct_per_trade': .015,
         'hard_stop_from_peak': .12, 'leverage_bear': .5}}


def summary(res, trades, start, end):
    m = rb.window_metrics(res['net_returns'], start, end)
    w = res['executed_weights'].loc[start:end]
    exp = w.sum(axis=1)
    bull = res['regime'].loc[start:end].eq('BULL')
    # Exclude end-of-period marks: these are censored, not completed trades.
    exit_dates = pd.to_datetime(trades['Exit_Date'])
    closed = trades[exit_dates.between(start, end) & trades['Exit_Reason'].ne('END_OF_PERIOD')]
    hold = closed['Holding_Days']
    years = (m['end'] - m['start']).days / 365.25
    stressed = rb.window_metrics(res['net_returns'] - .003 * res['turnover'], start, end)
    return {'cagr': float(m['cagr']), 'max_drawdown': float(m['max_drawdown']),
            'sharpe': float(m['sharpe']), 'avg_exposure': float(exp.mean()),
            'median_exposure': float(exp.median()),
            'avg_bull_exposure': float(exp[bull].mean()) if bull.any() else None,
            'bull_sessions': int(bull.sum()),
            'max_exposure': float(exp.max()), 'avg_positions': float((w > 1e-6).sum(axis=1).mean()),
            'max_positions': int((w > 1e-6).sum(axis=1).max()),
            'annual_turnover': float(res['turnover'].loc[start:end].sum() / years),
            'completed_trades': len(closed),
            'mean_holding_days': float(hold.mean()) if len(hold) else None,
            'median_holding_days': float(hold.median()) if len(hold) else None,
            'fraction_90_days': float((hold >= 90).mean()) if len(hold) else None,
            'fraction_180_days': float((hold >= 180).mean()) if len(hold) else None,
            'exit_counts': {str(k): int(v) for k, v in closed['Exit_Reason'].value_counts().items()},
            'double_cost_cagr': float(stressed['cagr']),
            'double_cost_drawdown': float(stressed['max_drawdown'])}


def main():
    requested = set(sys.argv[1:])
    if requested - CASES.keys():
        raise ValueError(f'Unknown case names: {sorted(requested - CASES.keys())}')
    output_path = OUT.with_name('long_horizon_exposure_calibration_results.json' if any('_cal_' in c for c in requested)
                                else 'long_horizon_exposure_stops_results.json' if any('_trail' in c for c in requested)
                                else 'long_horizon_exposure_selected_results.json') if requested else OUT
    output = {'warning': 'Previously examined history, not independent validation.',
              'windows': WINDOWS, 'cases': CASES, 'results': []}
    tmp, results, data = live.make_inputs()
    try:
        st = live.core.make_strategy(data, results, live.core.CUTOFF)
        all_keys = {k for cfg in (*CASES.values(), *MODES.values()) for k in cfg}
        defaults = {k: getattr(st, k) for k in all_keys}
        for mode, mode_params in MODES.items():
            for key, val in defaults.items():
                setattr(st, key, val)
            for key, val in mode_params.items():
                setattr(st, key, val)
            if mode != 'value':
                st.calculate_factors()
            mode_defaults = {k: getattr(st, k) for k in all_keys}
            for name, params in CASES.items():
                if requested and name not in requested:
                    continue
                for key, val in mode_defaults.items():
                    setattr(st, key, val)
                for key, val in params.items():
                    setattr(st, key, val)
                print('START', mode, name, flush=True)
                st.get_positions()
                result = rb.backtest_event_driven(st, initial_capital=100000,
                                                   transaction_cost=.003, risk_free_rate=0.)
                trades = rb.get_trade_log(st).reset_index(drop=True)
                row = {'mode': mode, 'case': name,
                       'windows': {key: summary(result, trades, *dates) for key, dates in WINDOWS.items()}}
                output['results'].append(row)
                output_path.write_text(json.dumps(output, indent=2) + '\n')
                print('RESULT', json.dumps(row), flush=True)
    finally:
        tmp.cleanup()


if __name__ == '__main__':
    main()

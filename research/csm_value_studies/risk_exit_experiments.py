"""Controlled pre-2025 CSM Value sizing, risk, and exit experiments.

Research only: no configuration is promoted based on these historical tests.
The entire history has already influenced prior research. The requested
zero-exit-day-weight accounting and normal next-open engine are unchanged.
"""
import importlib.util
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('risk_exit_results.json')
spec = importlib.util.spec_from_file_location('live_study', ROOT / 'research/csm_value_live_signals/study.py')
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)
import run_csm_value_backtest as rb

WINDOWS = {
    'full': ('2019-06-03', '2024-12-31'),
    'development': ('2019-06-03', '2021-12-31'),
    'previously_examined': ('2022-01-03', '2024-12-31'),
    'year_2024': ('2024-01-01', '2024-12-31'),
}
# Each case differs from baseline in one dimension. Raising the cap requires
# increasing the risk-budget parameter as well; otherwise 6.67% still binds.
CASES = {
    'baseline': {},
    'weight_8pct': {'max_weight_per_stock': .08, 'risk_pct_per_trade': .012},
    'weight_10pct': {'max_weight_per_stock': .10, 'risk_pct_per_trade': .015},
    'trailing_12pct': {'hard_stop_from_peak': .12},
    'trailing_16pct': {'hard_stop_from_peak': .16},
    'short_cooldown': {'stop_cooldown_days': 5, 'cooldown_floor_days': 2, 'cooldown_cap_days': 15},
    'bear_full_exposure': {'leverage_bear': 1.0},
    'bear_half_exposure': {'leverage_bear': .5},
    'no_rebalance_delay': {'rebalance_exit_buffer_months': 0},
    'monthly_sma50_gate': {'_monthly_sma50_gate': True},
    # Exploratory combinations added after inspecting the individual results.
    'combined_8_12_bear50': {'max_weight_per_stock': .08, 'risk_pct_per_trade': .012,
                             'hard_stop_from_peak': .12, 'leverage_bear': .5},
    'combined_10_12_bear50': {'max_weight_per_stock': .10, 'risk_pct_per_trade': .015,
                              'hard_stop_from_peak': .12, 'leverage_bear': .5},
    'combined_10_16_bear50': {'max_weight_per_stock': .10, 'risk_pct_per_trade': .015,
                              'hard_stop_from_peak': .16, 'leverage_bear': .5},
}


def monthly_sma50_gate(strategy):
    """Month-end close > SMA50, sampled only at actual trading sessions."""
    p = strategy.prices
    sma = p.rolling(50, min_periods=50).mean()
    labels = strategy.factors.index
    sessions = pd.Series(p.index, index=p.index).resample('ME').last().reindex(labels)
    valid = sessions.notna()
    dates = pd.DatetimeIndex(sessions[valid].values)
    result = (p > sma).where(p.notna() & sma.notna()).reindex(dates)
    result.index = labels[valid]
    return result.reindex(index=labels, columns=strategy.factors.columns).astype('boolean').fillna(False).astype(bool)


def summary(res, trades, start, end):
    metrics = rb.window_metrics(res['net_returns'], start, end)
    weights = res['executed_weights'].loc[start:end]
    years = (metrics['end'] - metrics['start']).days / 365.25
    selected = trades[pd.to_datetime(trades['Entry_Date']).between(start, end)]
    # Trading-cost stress preserves decisions because the strategy's risk
    # buffers are based on gross returns, not net-of-cost portfolio equity.
    stressed = res['net_returns'] - .003 * res['turnover']
    stress = rb.window_metrics(stressed, start, end)
    return {
        'cagr': float(metrics['cagr']), 'max_drawdown': float(metrics['max_drawdown']),
        'sharpe': float(metrics['sharpe']),
        'calmar': float(metrics['cagr'] / abs(metrics['max_drawdown'])),
        'avg_exposure': float(weights.sum(axis=1).mean()),
        'max_actual_positions': int((weights > 1e-6).sum(axis=1).max()),
        'max_actual_weight': float(weights.max().max()),
        'turnover_per_year': float(res['turnover'].loc[start:end].sum() / years),
        'trades_entered': len(selected),
        'median_holding_days': float(selected['Holding_Days'].median()) if len(selected) else None,
        'exit_counts_by_entry_cohort': {str(k): int(v) for k, v in selected['Exit_Reason'].value_counts().items()},
        'double_cost_cagr': float(stress['cagr']),
        'double_cost_max_drawdown': float(stress['max_drawdown']),
    }


def main():
    selected = set(sys.argv[1:])
    unknown = selected.difference(CASES)
    if unknown:
        raise ValueError(f'Unknown cases: {sorted(unknown)}')
    output_path = OUT.with_name('risk_exit_selected_results.json') if selected else OUT
    tmp, results, data = live.make_inputs()
    output = {'warning': 'All pre-2025 data has been examined; these are exploratory historical comparisons, not independent validation.',
              'cases': CASES, 'windows': WINDOWS, 'results': []}
    try:
        strategy = live.core.make_strategy(data, results, live.core.CUTOFF)
        for mode in ('value', 'value_growth_pullback'):
            if mode != 'value':
                strategy.ranking_mode = mode
                strategy.components = ('EP', 'PROFIT_GROWTH', 'PULLBACK')
                strategy.calculate_factors()
            base_momentum = strategy.momentum_returns.copy()
            gate = monthly_sma50_gate(strategy)
            original = {key: getattr(strategy, key) for cfg in CASES.values() for key in cfg if not key.startswith('_')}
            for name, config in CASES.items():
                if selected and name not in selected:
                    continue
                for key, value in original.items():
                    setattr(strategy, key, value)
                for key, value in config.items():
                    if not key.startswith('_'):
                        setattr(strategy, key, value)
                strategy.momentum_returns = base_momentum.where(gate) if config.get('_monthly_sma50_gate') else base_momentum.copy()
                print('START', mode, name, flush=True)
                strategy.get_positions()
                res = rb.backtest_event_driven(strategy, initial_capital=100000, transaction_cost=.003, risk_free_rate=0.)
                trades = rb.get_trade_log(strategy).reset_index(drop=True)
                row = {'ranking': mode, 'case': name,
                       'windows': {key: summary(res, trades, *dates) for key, dates in WINDOWS.items()}}
                output['results'].append(row)
                output_path.write_text(json.dumps(output, indent=2) + '\n')
                print('RESULT', json.dumps(row), flush=True)
            for key, value in original.items():
                setattr(strategy, key, value)
    finally:
        tmp.cleanup()


if __name__ == '__main__':
    main()

"""Evaluate CSM Value's hard position limit without liquidity-rank filtering.

The candidate set and selection rule are fixed here: select the highest IS
Calmar (CAGR / |MaxDD|), breaking ties by Sharpe and then fewer positions.
The 2022-onward comparison is historical and previously examined, not a blind
holdout. The existing 5% position weight limit and all other defaults stay
fixed; low position counts therefore may deliberately leave cash uninvested.
"""
import gc
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'csm_value'))
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue

IS_START = '2019-06-03'
IS_END = '2021-12-31'
OOS_START = '2022-01-03'
CANDIDATES = (10, 15, 20, 25, 30, 40)
BASELINE = 15
OUT = Path(__file__).resolve().parent / 'output'


def make_strategy(end=None):
    prices, volumes, highs, lows, opens = rb.load_data(rb.data_folder_path)
    valuations = rb.load_nse_monthly_prices(symbols=set(prices.columns))
    last = min(prices.index.max(), valuations.index.max(), rb.RESEARCH_END_DATE)
    if end is not None:
        last = min(last, pd.Timestamp(end))
    sl = lambda frame: frame.loc['2001-01-01':last]
    prices, volumes, highs, lows, opens, valuations = map(sl, (prices, volumes, highs, lows, opens, valuations))
    prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens)
    bench = rb.build_benchmark(prices)
    strategy = CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs,
                        lows_df=lows, opens_df=opens, benchmark_series=bench,
                        valuation_prices_df=valuations, top_n=BASELINE,
                        buffer_ratio=.2, risk_pct_per_trade=.01, max_weight_per_stock=.05,
                        hard_stop_from_peak=.20, leverage_bear=.8, vol_target=.15,
                        rebalance_exit_buffer_months=1, fill_weight_caps=False)
    strategy.calculate_factors()
    return strategy, last


def evaluate(strategy, n, start, end):
    strategy.top_n = n
    strategy.get_positions()
    res = rb.backtest_event_driven(strategy, initial_capital=100_000,
                                   transaction_cost=0.003, risk_free_rate=0.)
    metrics = rb.window_metrics(res['net_returns'], start, end)
    if metrics is None or metrics['max_drawdown'] >= 0:
        raise ValueError(f'Not enough observations to evaluate {n} positions')
    weights = res['executed_weights'].loc[start:end]
    counts = (weights > 1e-6).sum(axis=1)
    max_count = int(counts.max())
    if max_count > n:
        raise AssertionError(f'{max_count} actual holdings exceeded limit {n}')
    duration = (metrics['end'] - metrics['start']).days / 365.25
    turnover = float(res['turnover'].loc[start:end].sum() / duration)
    return dict(n=n, cagr=float(metrics['cagr']), drawdown=float(metrics['max_drawdown']),
                sharpe=float(metrics['sharpe']), calmar=float(metrics['cagr'] / abs(metrics['max_drawdown'])),
                exposure=float(weights.sum(axis=1).mean()), annual_turnover=turnover,
                max_positions=max_count, start=str(metrics['start'].date()), end=str(metrics['end'].date()))


def row(m):
    return (f"| {m['n']} | {m['cagr']:.2%} | {m['drawdown']:.2%} | {m['calmar']:.2f} | "
            f"{m['sharpe']:.2f} | {m['exposure']:.1%} | {m['annual_turnover']:.1%} | {m['max_positions']} |")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    print('IS selection: max Calmar; tie-break Sharpe, then fewer positions. Candidates:', CANDIDATES, flush=True)
    train, last = make_strategy(IS_END)
    if last < pd.Timestamp(IS_END):
        raise ValueError(f'IS data ends early: {last.date()}')
    train_results = []
    for n in CANDIDATES:
        print(f'\\n[IS] Testing maximum {n} positions', flush=True)
        train_results.append(evaluate(train, n, IS_START, IS_END))
        print('[IS result]', json.dumps(train_results[-1]), flush=True)
    winner = max(train_results, key=lambda x: (x['calmar'], x['sharpe'], -x['n']))['n']
    frozen = {'selection_rule': 'IS max Calmar, then IS Sharpe, then fewer positions',
              'candidates': list(CANDIDATES), 'selected': winner, 'results': train_results,
              'warning': '2022 onward has been previously examined and is not a blind holdout.'}
    (OUT / 'position_count_is_selection.json').write_text(json.dumps(frozen, indent=2) + '\n')
    print(f'\\nFrozen IS selection: {winner} positions', flush=True)
    del train
    gc.collect()

    full, last = make_strategy()
    candidates = [winner] + ([] if winner == BASELINE else [BASELINE])
    oos = []
    for n in candidates:
        print(f'\\n[Previously examined OOS] Evaluating {n} positions', flush=True)
        oos.append(evaluate(full, n, OOS_START, str(last.date())))
        print('[OOS result]', json.dumps(oos[-1]), flush=True)
    header = '| Max positions | CAGR | Max DD | Calmar | Sharpe | Avg exposure | Annual turnover | Max actual |'
    sep = '|---:|---:|---:|---:|---:|---:|---:|---:|'
    lines = ['# CSM Value position-count study', '',
             f'IS: {IS_START} to {IS_END}. Selected {winner} using IS Calmar only, '
             'then IS Sharpe and fewer positions as tie-breaks.',
             'The 2022-onward period has already been examined and is not a blind OOS holdout.',
             'No price × volume ranking cutoff. The ₹20 price floor, circuit-day and falling-knife gates remain.',
             'Elendel return booking: zero weight on the exit day. Costs: 0.30% one-way; cash assumes 6.5% p.a.',
             'The 5% maximum weight per stock is unchanged, so 10 or 15 positions can leave cash uninvested.',
             '', '## In-sample candidates', '', header, sep, *[row(x) for x in train_results],
             '', '## Previously examined OOS: selected limit and 15-position baseline', '', header, sep,
             *[row(x) for x in oos], '',
             'All runs use the same universe and current implementation. Position-count selection is based on a short IS period; '
             'neither the accounting convention nor this selection establishes realized P&L or a robust edge.']
    report = '\n'.join(lines) + '\n'
    (OUT / 'position_count_study.md').write_text(report)
    print('\n' + report, flush=True)


if __name__ == '__main__':
    main()

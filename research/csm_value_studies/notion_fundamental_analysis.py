"""Historical fundamentals-vs-OHLCV comparisons for the Notion analysis.

Controls are prespecified: Elendel-inspired A3/Q5 pullback and trend ranks.
The common-universe control retains point-in-time fundamental eligibility;
the broad control removes quarterly-result screening, while retaining the
requested fundamentals-file/OHLCV symbol intersection and price filters.
Normal and experimental engines are compared only within themselves.
"""
import gc
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'research/csm_value_studies/notion_analysis'
OUT.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(ROOT / 'csm_value'))
import csm_value_strategy as normal
import csm_value_experimental_strategy as experimental
import run_csm_value_backtest as nr
import run_csm_value_experimental_backtest as er

spec = importlib.util.spec_from_file_location('live_study', ROOT / 'research/csm_value_live_signals/study.py')
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)

START = '2019-06-03'
END = '2024-12-31'
WINDOWS = {'full': (START, END), 'development': (START, '2021-12-31'),
           'previously_examined_2022_2024': ('2022-01-03', END),
           'year_2024': ('2024-01-01', END)}
CASES = ('fundamental', 'pullback_common', 'pullback_price_only', 'trend_price_only')


def technical_panels(strategy):
    prices = strategy.prices.ffill()
    benchmark = strategy.benchmark.reindex(prices.index).ffill()
    rs = prices.div(benchmark, axis=0)
    a3 = rs / rs.rolling(252, min_periods=200).max()
    sma = prices.rolling(50, min_periods=40).mean()
    above = (prices > sma).where(prices.notna() & sma.notna()).astype(float)
    q5 = above.rolling(126, min_periods=100).mean()
    labels = strategy.factors.index
    sess = pd.Series(prices.index, index=prices.index).resample('ME').last().reindex(labels)
    valid = sess.notna()
    dates = pd.DatetimeIndex(sess[valid].values)
    def sample(df):
        return df.reindex(dates).set_axis(labels[valid]).reindex(labels)
    return sample(a3), sample(q5)


def technical_score(a3, q5, eligible, direction):
    """A3/Q5 percentile average; missing components get neutral .5."""
    rank_a3 = a3.where(eligible).rank(axis=1, pct=True, method='average').fillna(.5)
    rank_q5 = q5.where(eligible).rank(axis=1, pct=True, method='average').fillna(.5)
    strength = (rank_a3 + rank_q5) / 2
    return (1.0 - strength if direction == 'pullback' else strength).where(eligible)


def metrics(res, trades, start, end, engine):
    m = engine.window_metrics(res['net_returns'], start, end)
    w = res['executed_weights'].loc[start:end]
    duration = (m['end'] - m['start']).days / 365.25
    d = trades.copy()
    d['Entry_Date'] = pd.to_datetime(d['Entry_Date'])
    d['Exit_Date'] = pd.to_datetime(d['Exit_Date'])
    closed = d[d.Entry_Date.ge(pd.Timestamp(start)) & d.Exit_Date.le(pd.Timestamp(end))
               & d.Exit_Date.ge(pd.Timestamp(start)) & d.Exit_Reason.ne('END_OF_PERIOD')].copy()
    pnl = pd.to_numeric(closed.PnL_Pct, errors='coerce').dropna()
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    return {'cagr': float(m['cagr']), 'max_drawdown': float(m['max_drawdown']),
            'sharpe': float(m['sharpe']), 'exposure': float(w.sum(axis=1).mean()),
            'annual_turnover': float(res['turnover'].loc[start:end].sum() / duration),
            'max_positions': int((w > 1e-6).sum(axis=1).max()),
            'closed': int(len(pnl)), 'winners': int(len(wins)), 'losers': int(len(losses)),
            'flat': int((pnl == 0).sum()), 'win_rate': float((pnl > 0).mean()) if len(pnl) else None,
            'loss_rate': float((pnl < 0).mean()) if len(pnl) else None,
            'mean_win_pct': float(wins.mean()) if len(wins) else None,
            'mean_loss_pct': float(losses.mean()) if len(losses) else None,
            'median_pnl_pct': float(pnl.median()) if len(pnl) else None,
            'mean_holding_days': float(closed.Holding_Days.mean()) if len(closed) else None,
            'median_holding_days': float(closed.Holding_Days.median()) if len(closed) else None,
            'exit_counts': {str(k): int(v) for k, v in closed.Exit_Reason.value_counts().items()}}


def yearly(res):
    r = res['net_returns'].loc[START:END]
    return {str(year): float((1 + group).prod() - 1) for year, group in r.groupby(r.index.year)}


def trade_aggregates(trades):
    d = trades.copy()
    d.Entry_Date = pd.to_datetime(d.Entry_Date)
    d.Exit_Date = pd.to_datetime(d.Exit_Date)
    d = d[(d.Entry_Date >= START) & (d.Exit_Date <= END) & (d.Exit_Reason != 'END_OF_PERIOD')]
    out = {}
    for column in ('Exit_Reason', 'Exit_Detail', 'Regime_At_Entry'):
        groups = []
        for name, g in d.groupby(column, dropna=False):
            p = pd.to_numeric(g.PnL_Pct, errors='coerce').dropna()
            if not len(p): continue
            groups.append({'group': str(name), 'n': len(p), 'win_rate': float((p > 0).mean()),
                           'mean_pnl_pct': float(p.mean()), 'median_pnl_pct': float(p.median()),
                           'mean_days': float(g.Holding_Days.mean())})
        out[column] = sorted(groups, key=lambda x: -x['n'])
    d = d.assign(_holding_band=pd.cut(d.Holding_Days, [0, 30, 90, 180, 365, np.inf],
                                       labels=['1–30', '31–90', '91–180', '181–365', '>365']))
    out['holding_bands'] = []
    for name, g in d.groupby('_holding_band', observed=True):
        p = pd.to_numeric(g.PnL_Pct, errors='coerce').dropna()
        if len(p):out['holding_bands'].append({'group': str(name), 'n': len(p),
              'win_rate': float((p > 0).mean()), 'mean_pnl_pct': float(p.mean())})
    cols = ['Ticker', 'Entry_Date', 'Exit_Date', 'PnL_Pct', 'Holding_Days', 'Exit_Reason']
    out['best'] = json.loads(d.nlargest(8, 'PnL_Pct')[cols].to_json(orient='records', date_format='iso'))
    out['worst'] = json.loads(d.nsmallest(8, 'PnL_Pct')[cols].to_json(orient='records', date_format='iso'))
    return out


def main():
    tmp, fundamentals, data = live.make_inputs()
    all_rows, all_trades, all_returns = [], {}, {}
    try:
        prices, volumes, highs, lows, opens, valuations = data
        prices, highs, lows, opens = nr.mask_corporate_actions(prices, highs, lows, opens)
        bench = nr.build_benchmark(prices)
        for name, module, engine in [('normal', normal, nr), ('experimental', experimental, er)]:
            print('BUILD', name, flush=True)
            s = module.CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs,
                                lows_df=lows, opens_df=opens, benchmark_series=bench,
                                valuation_prices_df=valuations, results_df=fundamentals)
            s.calculate_factors()
            base, momentum = s.factors.copy(), s.momentum_returns.copy()
            components, legs = s.components, s.factor_legs.copy()
            a3, q5 = technical_panels(s)
            first = base.loc['2019-06-01':].dropna(how='all').index.min()
            print('FIRST_ELIGIBLE_SIGNAL', name, str(first), flush=True)
            common = base.notna()
            price_only = momentum.reindex(index=base.index, columns=base.columns).notna()
            price_only.loc[price_only.index < first] = False
            price_only = price_only.where(price_only.sum(axis=1) >= s.min_eligible, False)
            for case in CASES:
                print('START', name, case, flush=True)
                s.momentum_returns = momentum.copy()
                if case == 'fundamental':
                    s.factors, s.components, s.factor_legs = base.copy(), components, legs.copy()
                else:
                    elig = common if case == 'pullback_common' else price_only
                    direction = 'trend' if case == 'trend_price_only' else 'pullback'
                    s.factors = technical_score(a3, q5, elig, direction)
                    s.components = ('TECHNICAL',)
                    s.factor_legs = {'TECHNICAL': s.factors.copy()}
                s.get_positions()
                result = engine.backtest_event_driven(s, initial_capital=200000,
                                                       transaction_cost=.003, risk_free_rate=0.)
                trades = engine.get_trade_log(s).reset_index(drop=True)
                metrics_by_window = {k: metrics(result, trades, *dates, engine) for k, dates in WINDOWS.items()}
                row = {'version': name, 'case': case, 'first_signal': str(first.date()),
                       'windows': metrics_by_window, 'annual_returns': yearly(result),
                       'trade_groups': trade_aggregates(trades)}
                all_rows.append(row)
                trades.to_csv(OUT / f'{name}_{case}_trades.csv', index=False)
                all_returns[f'{name}:{case}'] = result['net_returns'].loc[START:END].copy()
                all_trades[f'{name}:{case}'] = trades
                (OUT / 'metrics.json').write_text(json.dumps({'results': all_rows}, indent=2, allow_nan=False) + '\n')
                print('RESULT', json.dumps({'version': name, 'case': case, **metrics_by_window['full']}), flush=True)
            del s, base, momentum, a3, q5
            gc.collect()
        pd.concat(all_returns, axis=1).to_csv(OUT / 'daily_returns.csv', index_label='date')
        print('COMPLETE', flush=True)
    finally:
        tmp.cleanup()


if __name__ == '__main__':
    main()

"""Research-only crash-guard comparison; does not alter the live strategy.

Run: MPLCONFIGDIR=/tmp/mpl-csm python3 research/csm_absolute_crash_guard/compare.py
"""
from pathlib import Path
import contextlib
import os
import sys
import time

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'Old_live_strategies'))
from csm_absolute import IndividualMomentumStrategy, load_data
import csm_absolute_backtest as bt
import run_csm_absolute as config


def guards(bench):
    """Values are known before the execution day, matching the existing engine."""
    sma = bench.rolling(200, min_periods=180).mean().shift(1)
    trend = (bench < sma).shift(1).fillna(False)
    vol = bench.pct_change(fill_method=None).rolling(21).std().shift(1)
    result = {'sma200': trend, 'none': trend & False}
    for q in (0.90, 0.95, 0.975):
        threshold = vol.expanding(min_periods=126).quantile(q)
        result[f'vol{q:g}'] = (vol > threshold).fillna(False)
        if q == 0.95:
            result['vol0.95_floor2.6pct'] = (vol > threshold.clip(lower=.026)).fillna(False)
    return result


def research_engine():
    """Inject only the guard series and fix missing P&L of fully exited names.

    Remaining engine assumptions are intentionally preserved. In particular this
    is not a full replacement for a cash-and-shares order execution simulator.
    """
    import inspect
    source = inspect.getsource(bt._run_event_backtest)
    old = '    # 0-E ── Monthly target weights → daily (shifted 1 trading day)'
    assert source.count(old) == 1
    source = source.replace(old, '    is_bearish = self._research_guard.reindex(self.prices.index).fillna(False)\n\n' + old)
    old = '    _eq_ret     = (executed_weights * _daily_ret).sum(axis=1)'
    assert source.count(old) == 1
    new = '''    _pnl_weights = executed_weights.copy()
    _prior_weights = executed_weights.shift(1).fillna(0.0)
    for _ev in self._trade_events:
        if _ev['type'] == 'EXIT' and _ev['reason'] != 'END_OF_PERIOD':
            _d, _s = _ev['date'], _ev['ticker']
            if executed_weights.at[_d, _s] < 1e-6:
                _pnl_weights.at[_d, _s] = _prior_weights.at[_d, _s]
    _eq_ret = (_pnl_weights * _daily_ret).sum(axis=1)'''
    source = source.replace(old, new)
    scope = dict(vars(bt))
    exec(compile(source, 'research_engine', 'exec'), scope)
    return scope['_run_event_backtest']


def metrics(ret, turn, weights, guard, events, start, end):
    ret = ret.loc[start:end]
    turn = turn.reindex(ret.index)
    eq = (1 + ret).cumprod()
    years = (ret.index[-1] - ret.index[0]).days / 365.25
    dd = eq / eq.cummax() - 1
    return dict(start=str(ret.index[0].date()), end=str(ret.index[-1].date()),
        cagr=eq.iloc[-1] ** (1 / years) - 1,
        max_drawdown=dd.min(), volatility=ret.std() * np.sqrt(252),
        sharpe=np.sqrt(252) * ret.mean() / ret.std(),
        calmar=(eq.iloc[-1] ** (1 / years) - 1) / abs(dd.min()),
        worst_day=ret.min(), annual_turnover=turn.sum() / years,
        mean_exposure=weights.sum(axis=1).reindex(ret.index).mean(),
        guard_days=int(guard.reindex(ret.index).sum()),
        crash_exits=sum(e['type']=='EXIT' and e['reason']=='CRASH_GUARD' and ret.index[0] <= e['date'] <= ret.index[-1] for e in events))


def main():
    started = time.time()
    print('Loading', flush=True)
    frames = load_data(os.environ.get('CSM_DATA_FOLDER', config.DATA_FOLDER))
    frames = [x.loc['2019-01-01':'2025-12-31'].sort_index() for x in frames]
    prices, volumes, highs, lows, opens = frames
    benchmark = (1 + prices.pct_change().clip(-.5, .5).mean(axis=1)).cumprod()
    print('Data shape', prices.shape, 'date range', prices.index.min(), prices.index.max(), flush=True)
    s = IndividualMomentumStrategy(prices, volumes, highs_df=highs, lows_df=lows, opens_df=opens,
        benchmark_series=benchmark, lookback_months=config.LOOKBACK_MONTHS,
        lookback_short_months=config.LOOKBACK_SHORT_MONTHS, atr_period=config.ATR_PERIOD,
        atr_multiplier=config.ATR_MULTIPLIER, lag_months=config.LAG_MONTHS,
        sharpe_threshold=config.SHARPE_THRESHOLD, capacity_limit=config.CAPACITY_LIMIT,
        universe_top_n=config.UNIVERSE_TOP_N, leverage_bull=config.LEVERAGE_BULL,
        leverage_bear=config.LEVERAGE_BEAR, leverage_panic=config.LEVERAGE_PANIC,
        min_price=config.MIN_PRICE, max_circuit_days=config.MAX_CIRCUIT_DAYS,
        max_weight_per_stock=config.MAX_WEIGHT_PER_STOCK, stop_std_devs=config.STOP_STD_DEVS,
        use_rebalance=config.USE_REBALANCE, rebalance_months=config.REBALANCE_MONTH,
        use_trailing=config.USE_TRAILING, reentry_cooldown_days=config.REENTRY_COOLDOWN_DAYS,
        rank_buffer=config.RANK_BUFFER, cooldown_losers_only=config.COOLDOWN_LOSERS_ONLY,
        use_take_profit=config.USE_TAKE_PROFIT)
    s.calculate_factors()
    s.get_positions()
    print('Positions ready', round(time.time()-started), 'seconds', flush=True)
    engine = research_engine()
    results, daily, years = [], {}, []
    series = guards(benchmark)
    for name, signal in series.items():
        print('Running', name, round(time.time()-started), 'seconds', flush=True)
        s._research_guard = signal
        result = engine(s, **config.BT_KWARGS)
        events = list(s._trade_events)
        daily[name] = result['net_returns']
        for label, start, end in [('full','2020-01-01','2025-12-31'),
                                  ('early','2020-01-01','2022-12-31'),
                                  ('late','2023-01-01','2025-12-31')]:
            m = metrics(result['net_returns'], result['turnover'], result['executed_weights'], signal, events, start, end)
            results.append(dict(variant=name, period=label, **m))
        for year in range(2020, 2026):
            m = metrics(result['net_returns'], result['turnover'], result['executed_weights'], signal, events, f'{year}-01-01', f'{year}-12-31')
            years.append(dict(variant=name, year=year, **m))
        pd.DataFrame(results).to_csv(OUT / 'metrics.csv', index=False)
        pd.DataFrame(years).to_csv(OUT / 'yearly.csv', index=False)
        pd.DataFrame(daily).to_csv(OUT / 'daily_returns.csv', index_label='date')
        pd.DataFrame(series).to_csv(OUT / 'guard_signals.csv', index_label='date')
        print('Finished', name, round(time.time()-started), 'seconds', flush=True)


if __name__ == '__main__':
    main()

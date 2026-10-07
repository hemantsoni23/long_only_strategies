"""
run_value_backtest.py -- backtest runner for EarningsYieldStrategy (same conventions as the live runners; shared helpers come from csm_pead/run_pead_backtest.py).

    python3 run_value_backtest.py                  # main backtest + reports -> ./output
    python3 run_value_backtest.py --sensitivity    # one-at-a-time sensitivity grid around the pre-declared defaults
Fundamentals exist for results filed 2018-05..2025-04 => default window 2019-03 .. 2025-06 (~6.3 yrs).
"""
import argparse, os, sys
import numpy as np, pandas as pd
HERE = os.path.dirname(os.path.abspath(__file__)); PEAD = os.path.join(os.path.dirname(HERE), 'csm_pead')
sys.path.insert(0, HERE); sys.path.insert(0, PEAD)
import run_pead_backtest as rp                                                  # noqa: E402  (data loading, perf, trade_stats, correlation_report, plotting)
from value_strategy import EarningsYieldStrategy                                # noqa: E402

OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
_out = lambda n: os.path.join(OUT, n)


def backtest_event_driven(strategy, start=None, end=None):
    res = strategy.simulate(start=start, end=end)
    res['perf'] = rp.perf(res['net_returns']); res['trade_stats'] = rp.trade_stats(res['trades'])
    return res


def report(res, strategy, bench_ret, start, end):
    lines = []
    r = res['net_returns'].loc[start:end]; p = rp.perf(r); ts = res['trade_stats']
    lines += ['=' * 100, f" CSM Earnings-Yield   {r.index[0].date()} .. {r.index[-1].date()}  ({p['years']:.1f} yrs)   cost {strategy.transaction_cost:.2%}/side, idle cash {strategy.cash_annual_rate:.1%}", '=' * 100]
    lines.append(f"  CAGR {p['cagr']*100:.1f}%   vol {p['vol']*100:.1f}%   Sharpe(rf6%) {p['sharpe']:.2f}   Sortino {p['sortino']:.2f}   MaxDD {p['max_drawdown']*100:.1f}%   Calmar {p['calmar']:.2f}")
    lines.append(f"  worst month {p['worst_month']*100:.1f}%   best month {p['best_month']*100:.1f}%   positive months {p['pct_pos_months']:.0%}")
    b = bench_ret.loc[r.index[0]:r.index[-1]]; pb = rp.perf(b)
    lines.append(f"  Equal-weight market (all stocks, same days): CAGR {pb['cagr']*100:.1f}%  vol {pb['vol']*100:.1f}%  Sharpe {pb['sharpe']:.2f}  MaxDD {pb['max_drawdown']*100:.1f}%")
    d = res['daily'].loc[r.index[0]:r.index[-1]]
    lines.append(f"  average invested {d['invested'].mean():.0%}; positions median {d['n_positions'].median():.0f}")
    if ts:
        lines.append(f"  trades {ts['trades']}   win rate {ts['win_rate']:.0%}   avg win {ts['avg_win']*100:.1f}%   avg loss {ts['avg_loss']*100:.1f}%   payoff {ts['payoff']:.2f}   avg trade {ts['avg_ret']*100:.2f}%   median {ts['median_ret']*100:.2f}%")
        tr = res['trades']; lines.append(f"  avg holding {ts['avg_days']:.0f} trading days; exits: rebalance {int((tr.Reason=='REBAL_EXIT').sum())}  stop {int((tr.Reason=='STOP_HIT').sum())}; monthly turnover (names replaced) ~{len(tr)/ (p['years']*12) / strategy.top_n:.0%}")
    y = rp.yearly(r); yb = rp.yearly(b)
    lines.append('  yearly returns %: ' + '  '.join(f"{k}: {v*100:+.1f} (mkt {yb.get(k, np.nan)*100:+.1f})" for k, v in y.items()))
    rp.correlation_report(r, bench_ret, lines, label='EY')
    txt = '\n'.join(lines); print(txt)
    open(_out('value_report.txt'), 'w').write(txt + '\n')
    res['trades'].to_csv(_out('value_trade_log.csv'), index=False); res['daily'].to_csv(_out('value_daily_log.csv'))
    res['net_returns'].rename('net_return').to_csv(_out('value_daily_returns.csv'))
    rp.plot_performance(res, bench_ret, _out('value_performance.png'))
    return p


def sensitivity(prices, volumes, highs, lows, opens, bench, start, end):
    rows = []
    def run(label, **kw):
        s = EarningsYieldStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, **kw)
        s.calculate_factors(); res = s.simulate(); r = res['net_returns'].loc[start:end]; p = rp.perf(r); ts = rp.trade_stats(res['trades'])
        rows.append(dict(variant=label, cagr=p['cagr'] * 100, sharpe=p['sharpe'], maxdd=p['max_drawdown'] * 100, trades=ts.get('trades'), win=ts.get('win_rate'), invested=res['daily'].loc[r.index[0]:r.index[-1], 'invested'].mean()))
        print(rows[-1], flush=True)
    run('DEFAULT')
    run('top 15', top_n=15, exit_rank=23); run('top 30', top_n=30, exit_rank=45)
    run('no profit-growth filter', require_profit_growth=False)
    run('no bear scaling', exposure_bear=1.0); run('stop 12%', hard_stop=0.12); run('no stop', hard_stop=0.99)
    run('include top-300 (rank 1-1000)', universe_min_n=1); run('ranks 301-1500', universe_top_n=1500); run('ranks 100-1000', universe_min_n=100)
    run('cost 0.6%/side', transaction_cost=0.006); run('cash earns 0%', cash_annual_rate=0.0)
    df = pd.DataFrame(rows); df.to_csv(_out('value_sensitivity.csv'), index=False, float_format='%.4f'); print('\n', df.round(3).to_string(index=False))


def main(start='2019-03-01', end='2025-06-30', do_sens=False):
    prices, volumes, highs, lows, opens, bench = rp.load_all()
    bench_ret = bench.pct_change().fillna(0.0)
    st = EarningsYieldStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)
    st.calculate_factors(); st.get_positions()
    res = backtest_event_driven(st)
    report(res, st, bench_ret, start, end)
    if do_sens:
        sensitivity(prices, volumes, highs, lows, opens, bench, start, end)
    return st, res


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--start', default='2019-03-01'); ap.add_argument('--end', default='2025-06-30'); ap.add_argument('--sensitivity', action='store_true')
    a = ap.parse_args(); main(a.start, a.end, a.sensitivity)

"""
run_pead_backtest.py -- backtest runner for PEADStrategy (same conventions as the Old_live_strategies runners).

    python3 run_pead_backtest.py                     # main backtest + reports -> ./output
    python3 run_pead_backtest.py --sensitivity       # pre-declared one-at-a-time sensitivity grid
    python3 run_pead_backtest.py --start 2020-09-01 --end 2025-06-30

Data loading, corporate-action masking and the equal-weight benchmark are imported from the live Elendel runner (read-only) so every strategy sees identical data.
Fundamentals exist only for results filed 2018-05 .. 2025-04, hence the default reporting window 2020-09 .. 2025-06 (~4.8 years).  See README.md before reading any number.
"""
import argparse
import importlib
import os
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
sys.path.insert(0, HERE); sys.path.insert(0, LIVE)
from pead_strategy import PEADStrategy                                         # noqa: E402

OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
LIVE_CACHE = '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache'
VERSION_TAG = 'pead'


def _out(name):
    return os.path.join(OUT, name)


# ───────────────────────────── data (identical to the live runners) ─────────────────────────────
def load_all(load_start='2001-01-01', load_end='2026-07-16'):
    ele = importlib.import_module('run_csm_elendel_backtest')
    prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
    sl = lambda d: d.loc[load_start:load_end] if not d.empty else d
    prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
    prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
    bench = ele.build_benchmark(prices)                      # exactly the live definition (loaded from 2001)
    return prices, volumes, highs, lows, opens, bench


# ───────────────────────────── metrics ─────────────────────────────
def perf(r, rf=0.06):
    r = r.dropna()
    if len(r) < 30:
        return {}
    eq = (1 + r).cumprod(); yrs = len(r) / 252
    rfd = (1 + rf) ** (1 / 252) - 1
    dd = eq / eq.cummax() - 1
    mth = (1 + r).groupby([r.index.year, r.index.month]).prod() - 1
    return dict(cagr=eq.iloc[-1] ** (1 / yrs) - 1, vol=r.std() * np.sqrt(252), sharpe=(r - rfd).mean() / r.std() * np.sqrt(252),
                sortino=(r - rfd).mean() / r[r < rfd].std() * np.sqrt(252) if (r < rfd).sum() > 5 else np.nan,
                max_drawdown=dd.min(), calmar=(eq.iloc[-1] ** (1 / yrs) - 1) / abs(dd.min()) if dd.min() < 0 else np.nan,
                worst_month=mth.min(), best_month=mth.max(), pct_pos_months=(mth > 0).mean(), years=yrs)


def trade_stats(tr):
    if tr is None or len(tr) == 0:
        return {}
    w = tr[tr.Return > 0]; l = tr[tr.Return <= 0]
    return dict(trades=len(tr), win_rate=len(w) / len(tr), avg_win=w.Return.mean() if len(w) else np.nan, avg_loss=l.Return.mean() if len(l) else np.nan,
                payoff=(w.Return.mean() / abs(l.Return.mean())) if len(w) and len(l) else np.nan, avg_ret=tr.Return.mean(), median_ret=tr.Return.median(),
                avg_days=tr.Days_Held.mean(), stop_hits=int((tr.Reason == 'STOP_HIT').sum()), time_exits=int((tr.Reason == 'TIME_STOP').sum()))


def backtest_event_driven(strategy, start=None, end=None):
    """Runs the strategy's single event loop and returns results plus summary metrics (net of costs, idle cash at the liquid-fund rate)."""
    res = strategy.simulate(start=start, end=end)
    res['perf'] = perf(res['net_returns']); res['trade_stats'] = trade_stats(res['trades'])
    return res


def yearly(r):
    y = (1 + r).groupby(r.index.year).prod() - 1
    return y


def correlation_report(r, bench_ret, lines, label='PEAD'):
    """Daily-return correlation with the unmodified live Elendel / Zenith / Quad engines and the 3-engine blend with and without this strategy."""
    live = {}
    for n in ('elendel', 'zenith', 'quad'):
        p = os.path.join(LIVE_CACHE, f'engine_{n}.pkl')
        if os.path.exists(p):
            import pickle
            live[n] = pickle.load(open(p, 'rb'))['net_returns']
    if not live:
        lines.append('(live-engine cache not found: run momentum_gold/run_live_engines.py to enable the correlation report)'); return
    df = pd.concat({**live, 'new': r}, axis=1).dropna()
    df = df.loc[r.index[0]:]
    lines.append(f"\n--- Correlation with the unmodified live engines (daily, {df.index[0].date()}..{df.index[-1].date()}, n={len(df)})")
    for n in live:
        lines.append(f"  corr({label}, {n:<8}) = {df['new'].corr(df[n]):+.2f}   (beta of {label} on {n}: {df['new'].cov(df[n]) / df[n].var():.2f})")
    lines.append('  live engines among themselves: ' + ', '.join(f"{a}-{b} {df[a].corr(df[b]):.2f}" for a, b in (('elendel', 'zenith'), ('elendel', 'quad'), ('zenith', 'quad')) if a in df and b in df))
    m = (1 + df).resample('ME').prod() - 1
    lines.append('  monthly-return correlation: ' + ', '.join(f"{n} {m['new'].corr(m[n]):+.2f}" for n in live))
    trio = df[list(live)].mean(axis=1)
    pt = perf(trio); pn = perf(df['new']); rho = df['new'].corr(trio)
    lines.append(f"--- Does it help the live trio? Break-even rule: a new stream raises the blend's Sharpe only if its Sharpe ({pn['sharpe']:.2f}) > corr x trio Sharpe ({rho:.2f} x {pt['sharpe']:.2f} = {rho*pt['sharpe']:.2f}) -> {'YES' if pn['sharpe'] > rho*pt['sharpe'] else 'NO'}")
    for w in (0.0, 0.10, 0.20, 0.30):
        b = (1 - w) * trio + w * df['new']; p = perf(b)
        lines.append(f"  {label} weight {w:>4.0%}: CAGR {p['cagr']*100:5.1f}%  vol {p['vol']*100:4.1f}%  Sharpe {p['sharpe']:5.2f}  MaxDD {p['max_drawdown']*100:6.1f}%")


def plot_performance(res, bench_ret, fname):
    eq = res['equity']; r = res['net_returns']; dd = eq / eq.cummax() - 1
    fig, ax = plt.subplots(3, 1, figsize=(14, 12), gridspec_kw={'height_ratios': [3, 1.5, 1.5]})
    be = (1 + bench_ret.reindex(eq.index).fillna(0)).cumprod()
    ax[0].plot(eq.index, eq / eq.iloc[0], label='PEAD Confirmed-Drift'); ax[0].plot(be.index, be / be.iloc[0], '--', color='gray', label='Equal-weight market')
    ax[0].set_yscale('log'); ax[0].legend(); ax[0].grid(alpha=.3); ax[0].set_title('Growth of 1 (log)')
    ax[1].fill_between(dd.index, dd * 100, 0, color='crimson', alpha=.4); ax[1].set_title('Drawdown %'); ax[1].grid(alpha=.3)
    d = res['daily']; ax[2].plot(d.index, d['invested'] * 100, color='navy'); ax[2].set_title('Invested % of equity'); ax[2].grid(alpha=.3)
    plt.tight_layout(); plt.savefig(fname, dpi=130); plt.close()


def report(res, strategy, bench_ret, report_start, report_end):
    lines = []
    r = res['net_returns'].loc[report_start:report_end]
    p = perf(r); ts = res['trade_stats']
    lines.append('=' * 100); lines.append(f" PEAD Confirmed-Drift   {r.index[0].date()} .. {r.index[-1].date()}  ({p['years']:.1f} yrs)   cost {strategy.transaction_cost:.2%}/side, idle cash {strategy.cash_annual_rate:.1%}"); lines.append('=' * 100)
    lines.append(f"  CAGR {p['cagr']*100:.1f}%   vol {p['vol']*100:.1f}%   Sharpe(rf6%) {p['sharpe']:.2f}   Sortino {p['sortino']:.2f}   MaxDD {p['max_drawdown']*100:.1f}%   Calmar {p['calmar']:.2f}")
    lines.append(f"  worst month {p['worst_month']*100:.1f}%   best month {p['best_month']*100:.1f}%   positive months {p['pct_pos_months']:.0%}")
    b = bench_ret.loc[r.index[0]:r.index[-1]]; pb = perf(b)
    lines.append(f"  Equal-weight market (all stocks, same days): CAGR {pb['cagr']*100:.1f}%  vol {pb['vol']*100:.1f}%  Sharpe {pb['sharpe']:.2f}  MaxDD {pb['max_drawdown']*100:.1f}%")
    d = res['daily'].loc[r.index[0]:r.index[-1]]
    lines.append(f"  average invested {d['invested'].mean():.0%} (median positions {d['n_positions'].median():.0f}, max {d['n_positions'].max()}); days with 0 positions {int((d['n_positions']==0).sum())}")
    if ts:
        lines.append(f"  trades {ts['trades']}   win rate {ts['win_rate']:.0%}   avg win {ts['avg_win']*100:.1f}%   avg loss {ts['avg_loss']*100:.1f}%   payoff {ts['payoff']:.2f}   avg trade {ts['avg_ret']*100:.2f}%   median {ts['median_ret']*100:.2f}%")
        lines.append(f"  avg holding {ts['avg_days']:.0f} trading days   exits: time {ts['time_exits']}  stop {ts['stop_hits']}")
    y = yearly(r); yb = yearly(b)
    lines.append('  yearly returns %: ' + '  '.join(f"{k}: {v*100:+.1f} (mkt {yb.get(k, np.nan)*100:+.1f})" for k, v in y.items()))
    correlation_report(r, bench_ret, lines)
    txt = '\n'.join(lines); print(txt)
    open(_out('pead_report.txt'), 'w').write(txt + '\n')
    res['trades'].to_csv(_out('pead_trade_log.csv'), index=False)
    res['daily'].to_csv(_out('pead_daily_log.csv'))
    res['net_returns'].rename('net_return').to_csv(_out('pead_daily_returns.csv'))
    plot_performance(res, bench_ret, _out('pead_performance.png'))
    return p


def sensitivity(strategy, bench_ret, report_start, report_end):
    """One-at-a-time grid around the pre-declared defaults. Every row is reported; none was used to choose the defaults."""
    rows = []
    base = dict(hold_days=strategy.hold_days, max_positions=strategy.max_positions, hard_stop=strategy.hard_stop, use_market_gate=strategy.use_market_gate,
                entry_window=strategy.entry_window, transaction_cost=strategy.transaction_cost)
    def run(label, **kw):
        for k, v in {**base, **kw}.items():
            setattr(strategy, k, v)
        res = strategy.simulate(); r = res['net_returns'].loc[report_start:report_end]; p = perf(r); ts = trade_stats(res['trades'])
        rows.append(dict(variant=label, cagr=p['cagr'] * 100, sharpe=p['sharpe'], maxdd=p['max_drawdown'] * 100, trades=ts.get('trades'), win=ts.get('win_rate'), avg_trade=ts.get('avg_ret', np.nan) * 100,
                         invested=res['daily'].loc[r.index[0]:r.index[-1], 'invested'].mean()))
        strategy.results = None
        print(rows[-1], flush=True)
    run('DEFAULT')
    for h in (40, 90): run(f'hold {h}d', hold_days=h)
    for m in (10, 30): run(f'{m} slots', max_positions=m)
    for s in (0.10, 0.99): run('stop 10%' if s == 0.10 else 'no stop', hard_stop=s)
    run('market gate ON', use_market_gate=True)
    run('entry window 1d', entry_window=1); run('entry window 10d', entry_window=10)
    run('cost 0.6%/side', transaction_cost=0.006)
    for k, v in base.items(): setattr(strategy, k, v)
    df = pd.DataFrame(rows); df.to_csv(_out('pead_sensitivity.csv'), index=False, float_format='%.4f')
    print('\n', df.round(3).to_string(index=False))
    return df


def main(start='2020-09-01', end='2025-06-30', do_sens=False, top_pct=0.30):
    prices, volumes, highs, lows, opens, bench = load_all()
    bench_ret = bench.pct_change().fillna(0.0)
    st = PEADStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, top_pct=top_pct)
    st.calculate_factors(); st.get_positions()
    res = backtest_event_driven(st)
    report(res, st, bench_ret, start, end)
    if do_sens:
        sensitivity(st, bench_ret, start, end)
        if abs(top_pct - 0.30) < 1e-9:
            rows = []
            for tp, mm in ((0.20, False), (0.40, False), (0.30, True)):
                s2 = PEADStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, top_pct=tp, require_margin_up=mm)
                s2.calculate_factors(); rr = s2.simulate(); r = rr['net_returns'].loc[start:end]; p = perf(r)
                rows.append(dict(variant=f'top {tp:.0%}{" + margin up" if mm else ""}', cagr=p['cagr'] * 100, sharpe=p['sharpe'], maxdd=p['max_drawdown'] * 100, trades=len(rr['trades'])))
            d2 = pd.DataFrame(rows); d2.to_csv(_out('pead_sensitivity_signal.csv'), index=False, float_format='%.4f'); print('\n', d2.round(3).to_string(index=False))
    return st, res


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--start', default='2020-09-01'); ap.add_argument('--end', default='2025-06-30'); ap.add_argument('--sensitivity', action='store_true'); ap.add_argument('--top-pct', type=float, default=0.30)
    a = ap.parse_args()
    main(a.start, a.end, a.sensitivity, a.top_pct)

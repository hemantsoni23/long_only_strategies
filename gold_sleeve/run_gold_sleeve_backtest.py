"""
run_gold_sleeve_backtest.py -- backtest + report for GoldSleevePV (persistence x volatility gold sleeve).

    python3 run_gold_sleeve_backtest.py

Outputs (./output): gold_sleeve_monthly_log.csv, gold_sleeve_daily_signals.csv, gold_sleeve_performance.png, gold_sleeve_report.txt
"""
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from gold_sleeve_strategy import GoldSleevePV, load_etf_close

ETF_FOLDER = '/Users/hemantsoni/Documents/upstox_data_folder/etf_ohlcv_data'
GOLD_SYMBOL = 'GOLDBEES'
BUCKET_CSV = os.path.join(_HERE, '..', 'factor_research', 'results', 'stage14_monthly_returns.csv')
BUCKET_COLS = ['Elendel (control)', 'Zenith', 'csm_absolute score', 'Residual mom (live-like)']
OUTPUT_DIR = os.path.join(_HERE, 'output')
HOLDOUT_START = pd.Timestamp('2015-01-01')
os.makedirs(OUTPUT_DIR, exist_ok=True)
_report = []


def say(*a):
    line = ' '.join(str(x) for x in a)
    print(line)
    _report.append(line)


def fmt(m):
    return (f"CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  "
            f"MaxDD {m['max_drawdown']*100:6.1f}%  Calmar {m['calmar']:5.2f}  months {m['months']}")


def main():
    gold = load_etf_close(os.path.join(ETF_FOLDER, GOLD_SYMBOL + '.csv'))
    gaps = gold.index.to_series().diff().dt.days
    big = gaps[gaps > 10]
    say('=' * 78)
    say(f' GOLD SLEEVE  |  {GOLD_SYMBOL}  {gold.index[0].date()} -> {gold.index[-1].date()}  ({len(gold)} obs)')
    for d, n in big.items():
        say(f'   DATA GAP: {int(n)} calendar days ending {d.date()}  (treated as MISSING; never forward-filled)')
    say('=' * 78)

    pv = GoldSleevePV(gold, mode='pv')
    bh = GoldSleevePV(gold, mode='buy_hold')
    r_pv, r_bh = pv.backtest(), bh.backtest()
    common = r_pv.index.intersection(r_bh.index)
    r_pv, r_bh = r_pv.loc[common], r_bh.loc[common]
    # re-chain equity on the common window
    for r in (r_pv, r_bh):
        r['equity'] = (1 + r.net_return).cumprod()

    say(f'\nEvaluation window: {common[0].date()} -> {common[-1].date()}  ({len(common)} usable months; months touching the data gap are excluded)')
    say('\n--- Standalone (capital not in gold earns 6% cash; 0.15% one-way cost on exposure changes)')
    say(f"  Persistence x Vol sleeve : {fmt(GoldSleevePV.metrics(r_pv.net_return))}")
    say(f"  Buy & hold gold          : {fmt(GoldSleevePV.metrics(r_bh.net_return))}")
    say(f"  average gold exposure {r_pv.exposure.mean()*100:.0f}% | exposure changes per year {r_pv.turnover.sum()/(len(r_pv)/12):.2f} (sum of |dE|) | "
        f"months fully out {int((r_pv.exposure < 0.05).sum())} | months >=90% in {int((r_pv.exposure >= 0.9).sum())}")

    say('\n--- Two usable segments (the 2011-2014 data gap separates them; segment A is short -> low statistical weight)')
    for lab, mask in (('A  2008-2010', r_pv.index < pd.Timestamp('2011-06-01')), ('B  2015-2026', r_pv.index >= HOLDOUT_START)):
        say(f"  {lab}: sleeve {fmt(GoldSleevePV.metrics(r_pv.net_return[mask]))}")
        say(f"  {' ' * len(lab)}  hold   {fmt(GoldSleevePV.metrics(r_bh.net_return[mask]))}")

    say('\n--- Cost sensitivity (one-way, on |exposure change|)')
    for c in (0.0015, 0.003, 0.005):
        m = GoldSleevePV.metrics(GoldSleevePV(gold, cost_one_way=c).backtest().loc[common].net_return)
        say(f"  cost {c*100:.2f}%: CAGR {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:.2f}  MaxDD {m['max_drawdown']*100:.1f}%")
    say('  (early GOLDBEES liquidity was thin: ~Rs 0.5-8 cr/day in 2007-10 -> use the 0.30-0.50% rows for that era)')

    say('\n--- Rebalance deadband (NOT part of the validated rule; shown for information)')
    for db in (0.0, 0.05, 0.10):
        rr = GoldSleevePV(gold, deadband=db).backtest().loc[common]
        m = GoldSleevePV.metrics(rr.net_return)
        say(f"  deadband {db:.0%}: CAGR {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:.2f}  MaxDD {m['max_drawdown']*100:.1f}%  trades/yr {(rr.turnover > 1e-9).sum()/(len(rr)/12):.1f}")

    # ---------------- yearly table
    say('\n--- Calendar-year returns (months in the gap are absent, so 2011-2014 are not shown)')
    yr = pd.DataFrame({'sleeve': r_pv.net_return, 'hold': r_bh.net_return}).groupby(common.year).apply(lambda x: (1 + x).prod() - 1)
    cnt = pd.Series(common.year).value_counts().sort_index()
    say(f"  {'Year':<6}{'sleeve':>9}{'hold':>9}{'months':>8}")
    for y, row in yr.iterrows():
        say(f"  {y:<6}{row.sleeve*100:8.1f}%{row.hold*100:8.1f}%{cnt[y]:>8}")

    # ---------------- portfolio view (needs factor_research results)
    if os.path.exists(BUCKET_CSV):
        S = pd.read_csv(BUCKET_CSV, index_col=0, parse_dates=True)
        B = S[BUCKET_COLS].mean(axis=1)
        B.index = B.index.to_period('M')
        sl = r_pv.net_return.copy(); sl.index = sl.index.to_period('M')
        hd = r_bh.net_return.copy(); hd.index = hd.index.to_period('M')
        idx = sl.index.intersection(B.dropna().index)
        b, s_, h_ = B[idx], sl[idx], hd[idx]
        w_bh = 0.10
        w_pv = min(0.35, w_bh * h_.std() / s_.std())     # equal risk budget to a 10% buy&hold sleeve
        mb = GoldSleevePV.metrics(b)
        m_h = GoldSleevePV.metrics((1 - w_bh) * b + w_bh * h_)
        m_p = GoldSleevePV.metrics((1 - w_pv) * b + w_pv * s_)
        say(f'\n--- Portfolio view: live-like momentum bucket (4 stripped books, proxy only) + gold sleeve  [{len(idx)} common months]')
        say(f"  bucket alone                         : {fmt(mb)}")
        say(f"  + {w_bh:.0%} buy&hold gold                  : {fmt(m_h)}")
        say(f"  + {w_pv:.0%} persistence x vol sleeve (equal risk): {fmt(m_p)}")
        say(f"  correlation of sleeve with bucket: {np.corrcoef(s_, b)[0, 1]:+.2f}   (buy&hold gold: {np.corrcoef(h_, b)[0, 1]:+.2f})")
        say(f"  -> vs buy&hold gold at equal risk: blended Sharpe {m_p['sharpe']-m_h['sharpe']:+.2f}, blended max drawdown {(m_p['max_drawdown']-m_h['max_drawdown'])*100:+.1f} pts, blended CAGR {(m_p['cagr']-m_h['cagr'])*100:+.1f} pts. A risk tool, not a return source.")
    else:
        say('\n(portfolio view skipped: factor_research results not found)')

    # ---------------- latest signal
    say('\n--- Latest signal')
    last_obs = gold.dropna().index[-1]
    try:
        sig = pv.latest_signal(today=last_obs)         # evaluated as of the last data date (data here end in the past)
        for k, v in sig.items():
            say(f'  {k}: {v}')
    except RuntimeError as e:
        say(f'  not available: {e}')
    say('\n  last 12 month-end targets:')
    tail = pv.month_end_exposure.dropna().tail(12)
    for d, e in tail.items():
        say(f'    {d.date()}  gold {e*100:5.1f}%  cash {(1-e)*100:5.1f}%')

    # ---------------- outputs
    log = r_pv.copy()
    log['buyhold_net_return'] = r_bh.net_return
    log['equity_buyhold'] = r_bh.equity
    log.to_csv(os.path.join(OUTPUT_DIR, 'gold_sleeve_monthly_log.csv'), float_format='%.6f')
    pv.daily.to_csv(os.path.join(OUTPUT_DIR, 'gold_sleeve_daily_signals.csv'), float_format='%.5f')

    fig, ax = plt.subplots(3, 1, figsize=(13, 11), sharex=True, gridspec_kw={'height_ratios': [2.2, 1.2, 1.2]})
    ax[0].plot(r_pv.index, r_pv.equity, label='Persistence x Vol sleeve', color='#1f77b4', lw=1.6)
    ax[0].plot(r_bh.index, r_bh.equity, label='Buy & hold gold', color='gray', ls='--', lw=1.2)
    ax[0].set_yscale('log'); ax[0].legend(); ax[0].grid(alpha=.3)
    ax[0].set_title('Gold sleeve: equity (months touching the 2011-14 data gap removed, so lines are spliced there)')
    ax[1].fill_between(r_pv.index, r_pv.exposure, step='post', color='#9467bd', alpha=.5); ax[1].set_ylabel('gold exposure'); ax[1].grid(alpha=.3)
    for r, c, l in ((r_pv, '#d62728', 'sleeve'), (r_bh, 'gray', 'hold')):
        ax[2].plot(r.index, r.equity / r.equity.cummax() - 1, color=c, label=l)
    ax[2].set_ylabel('drawdown'); ax[2].legend(); ax[2].grid(alpha=.3)
    plt.tight_layout(); plt.savefig(os.path.join(OUTPUT_DIR, 'gold_sleeve_performance.png'), dpi=140); plt.close(fig)
    with open(os.path.join(OUTPUT_DIR, 'gold_sleeve_report.txt'), 'w') as f:
        f.write('\n'.join(_report) + '\n')
    say(f'\nSaved to {OUTPUT_DIR}')


if __name__ == '__main__':
    main()

"""
run_momentum_gold_report.py -- before/after report for GoldIdleCashOverlay on the live-chassis momentum strategies.

    python3 run_live_engines.py elendel zenith quad     # once: runs the UNMODIFIED live engines, stores daily outputs in .cache/
    python3 run_momentum_gold_report.py

Compares, on identical days (only days where gold data are valid, 2007-03..2026-07 excluding the 2011-2014 hole):
  engine default idle cash | idle cash in 6.5% liquid fund (fair baseline) | capped gold in weak markets (the overlay)
under three assumptions for gold's future drift (sample drift / half / zero), plus segments, years and the uncapped version.
"""
import os
import sys
import pickle

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)
from gold_idle_cash import GoldIdleCashOverlay

OUT = os.path.join(_HERE, 'output'); os.makedirs(OUT, exist_ok=True)
STRATS = ('elendel', 'zenith', 'quad')
_lines = []


def say(*a):
    s = ' '.join(str(x) for x in a); print(s); _lines.append(s)


def row(lab, m, base=None):
    s = f"  {lab:<52} CAGR {m['cagr']*100:5.1f}%  vol {m['vol']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['max_drawdown']*100:6.1f}%  Calmar {m['calmar']:5.2f}"
    if base is not None:
        s += f"   | d: CAGR {100*(m['cagr']-base['cagr']):+4.1f}pt  Sharpe {m['sharpe']-base['sharpe']:+.3f}  MaxDD {100*(m['max_drawdown']-base['max_drawdown']):+4.1f}pt"
    say(s)


def main():
    M = GoldIdleCashOverlay.metrics
    for name in STRATS:
        path = os.path.join(_HERE, '.cache', f'engine_{name}.pkl')
        if not os.path.exists(path):
            say(f'[{name}] engine output missing -> run run_live_engines.py first'); continue
        p = pickle.load(open(path, 'rb'))
        w, net, reg, cr = p['executed_weights'], p['net_returns'], p['regime'], p['daily_cash_rate']
        base_ov = GoldIdleCashOverlay(mode='off')
        base = base_ov.apply(w, net, reg, cr)
        win = base.gold_valid & (base.index >= '2003-01-01')
        lf_daily = base_ov.lf_daily
        # engine default: idle cash at engine rate; fair baseline: idle in liquid fund
        default_r = net.reindex(w.index)
        fair_r = base.net_return
        say('\n' + '=' * 110)
        say(f' {name.upper()}   ({win.sum()} usable days = {win.sum()/252:.1f} yrs;  idle cash: mean {base.idle_cash_weight[win].mean():.0%}; '
            f"in weak regimes {base.idle_cash_weight[win & base.regime.isin(GoldIdleCashOverlay().regimes)].mean():.0%}; weak-regime days {base.regime[win].isin(GoldIdleCashOverlay().regimes).mean():.0%})")
        say('=' * 110)
        m_def, m_fair = M(default_r[win]), M(fair_r[win])
        row('engine default (idle cash at engine rate)', m_def)
        row('BASELINE: idle cash in 6.5% liquid fund', m_fair, m_def)
        say('  -- the overlay (cap 10% of portfolio, weak markets only), gold drift scenarios; all deltas vs the liquid-fund baseline')
        for mult, lab in ((1.0, 'actual gold returns (sample drift)'), (0.5, 'half of gold\'s excess drift'), (0.0, 'gold with zero excess drift (pure diversification)')):
            r = GoldIdleCashOverlay(cap=0.10, mode='weak', drift_multiplier=mult).apply(w, net, reg, cr)
            row(f'overlay cap10% weak | {lab}', M(r.net_return[win]), m_fair)
        r1 = GoldIdleCashOverlay(cap=0.10, mode='weak').apply(w, net, reg, cr)
        say(f"  gold used on {(r1.gold_weight[win] > 0.005).mean():.0%} of days; average gold weight {r1.gold_weight[win].mean():.1%} of the portfolio (max {r1.gold_weight[win].max():.0%})")
        say('  -- for context: the UNCAPPED version of the same idea (all idle cash -> gold in weak markets)')
        ru = GoldIdleCashOverlay(cap=1.0, mode='weak').apply(w, net, reg, cr)
        row('uncapped: all idle cash -> gold in weak markets', M(ru.net_return[win]), m_fair)
        say(f"     (gold would be {ru.gold_weight[win & base.regime.isin(['PANIC'])].mean():.0%} of the portfolio on PANIC days, {ru.gold_weight[win & (base.regime == 'BEAR')].mean():.0%} on BEAR days)")
        say('  -- segments (the 2011-14 hole separates them), overlay vs baseline')
        for lab, mask in (('2007-2010', win & (base.index < '2011-06-01')), ('2015-2026', win & (base.index >= '2015-01-01'))):
            a, b = M(r1.net_return[mask]), M(fair_r[mask])
            say(f"    {lab}: Sharpe {b['sharpe']:.2f} -> {a['sharpe']:.2f}   MaxDD {b['max_drawdown']*100:.1f}% -> {a['max_drawdown']*100:.1f}%   CAGR {b['cagr']*100:.1f}% -> {a['cagr']*100:.1f}%")
        yr_o = (1 + r1.net_return[win]).groupby(r1.index[win].year).prod() - 1
        yr_b = (1 + fair_r[win]).groupby(fair_r.index[win].year).prod() - 1
        d = (yr_o - yr_b) * 100
        say('    year-by-year difference (pts): ' + '  '.join(f'{y}:{v:+.1f}' for y, v in d.items() if abs(v) > 0.005 or True))
        say(f'    years better/equal: {(d >= -0.005).sum()} of {len(d)}')

    with open(os.path.join(OUT, 'momentum_gold_report.txt'), 'w') as f:
        f.write('\n'.join(_lines) + '\n')
    say(f'\nSaved {os.path.join(OUT, "momentum_gold_report.txt")}')


if __name__ == '__main__':
    main()

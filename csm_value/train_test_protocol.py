"""
train_test_protocol.py -- design choices are made on the TRAIN window only; the TEST window is scored once, for the chosen configuration.

WINDOWS.  The requested split (train 2002-2013, test 2014-2025) is impossible for this signal: the fundamentals in stocks_fundamentals start with FY2018-19 results (NSE XBRL), so trailing-12-month
earnings exist only from 2019.  The split used here is therefore chronological inside the data that exists:
        TRAIN  2019-06-03 .. 2021-12-31   (choose between the pre-declared configurations)
        TEST   2022-01-03 .. 2025-06-30   (never used for any choice)
Configurations (everything else is Elendel's default chassis; top_n = 15 fixed):
        net-profit definition {total, owners-with-fallback} x universe liquidity-rank floor {1, 301} x require rising quarterly profit {yes, no}  (8 configurations)
Selection rule (fixed before running): highest TRAIN Sharpe (rf 0); ties broken by Calmar.
Caveat that no protocol can remove: earlier looks at 2019-2025 (while building the idea) informed the choice of THESE four candidates and of the E/P signal itself.

    python3 train_test_protocol.py        -> output/train_test_report.txt
"""
import os, sys, itertools
import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue

TRAIN = ('2019-06-03', '2021-12-31'); TEST = ('2022-01-03', '2025-06-30')
GRID = [dict(universe_top_n_min=u, require_profit_growth=g, profit_basis=pb) for pb, u, g in itertools.product(('total', 'owners'), (1, 301), (True, False))]
lines = []
def say(s=''):
    print(s); lines.append(s)

def metrics(r):
    r = r.dropna(); eq = (1 + r).cumprod(); y = (r.index[-1] - r.index[0]).days / 365.25; dd = eq / eq.cummax() - 1
    cagr = eq.iloc[-1] ** (1 / y) - 1
    return dict(cagr=cagr * 100, vol=r.std() * np.sqrt(252) * 100, sharpe=r.mean() / r.std() * np.sqrt(252), maxdd=dd.min() * 100, calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan, days=len(r))

def run(cfg, data):
    prices, volumes, highs, lows, opens, bench = data
    csm = CSMValue(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench, universe_top_n_max=1000, **cfg)
    csm.calculate_factors(); csm.get_positions()
    res = rb.backtest_event_driven(csm, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    return res['net_returns']

def main():
    prices, volumes, highs, lows, opens = rb.load_data(rb.data_folder_path)
    prices = prices.loc['2001-01-01':TEST[1]]; volumes = volumes.loc['2001-01-01':TEST[1]]
    highs = highs.loc['2001-01-01':TEST[1]]; lows = lows.loc['2001-01-01':TEST[1]]; opens = opens.loc['2001-01-01':TEST[1]]
    prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens)
    bench = rb.build_benchmark(prices); data = (prices, volumes, highs, lows, opens, bench)
    rets = {}
    for cfg in GRID:
        key = f"profit={cfg['profit_basis']}, rank>={cfg['universe_top_n_min']}, growth {'on' if cfg['require_profit_growth'] else 'off'}"
        rets[key] = run(cfg, data)
    say('=' * 100); say(f' TRAIN {TRAIN[0]} .. {TRAIN[1]}   (selection uses ONLY this table)'); say('=' * 100)
    tr = {k: metrics(r.loc[TRAIN[0]:TRAIN[1]]) for k, r in rets.items()}
    for k, m in tr.items():
        say(f"  {k:<40} CAGR {m['cagr']:6.1f}%  vol {m['vol']:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['maxdd']:6.1f}%  Calmar {m['calmar']:5.2f}")
    best = max(tr, key=lambda k: (round(tr[k]['sharpe'], 6), tr[k]['calmar']))
    say(f'\n  SELECTED on train: {best}')
    say(''); say('=' * 100); say(f' TEST {TEST[0]} .. {TEST[1]}   (scored once, for the selected configuration)'); say('=' * 100)
    m = metrics(rets[best].loc[TEST[0]:TEST[1]])
    say(f"  {best:<40} CAGR {m['cagr']:6.1f}%  vol {m['vol']:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['maxdd']:6.1f}%  Calmar {m['calmar']:5.2f}   ({m['days']} days)")
    say('\n  For transparency only (NOT used for any choice) -- the other configurations on the test window:')
    for k, r in rets.items():
        if k == best: continue
        mm = metrics(r.loc[TEST[0]:TEST[1]]); say(f"  {k:<40} CAGR {mm['cagr']:6.1f}%  vol {mm['vol']:5.1f}%  Sharpe {mm['sharpe']:5.2f}  MaxDD {mm['maxdd']:6.1f}%  Calmar {mm['calmar']:5.2f}")
    open(os.path.join(rb.OUTPUT_DIR if hasattr(rb, 'OUTPUT_DIR') else HERE, 'train_test_report.txt'), 'w').write('\n'.join(lines) + '\n')

if __name__ == '__main__':
    main()

"""Checks for EarningsYieldStrategy (python3 test_value.py)
 1. point-in-time inputs: E/P for random (symbol, month) re-derived independently from raw results filed on/before the date
 2. no look-ahead: data truncated at 2023-06-30 -> identical E/P rows and identical simulated equity up to 2023-03-31
 3. stop parity: get_exit_signals agrees with every simulated STOP_HIT (hold before, exit_next_open on the decision day)
 4. rebalance parity: get_target_portfolio(signal day, actual holdings) reproduces the rebalance the simulation executed (sells equal, buys superset of entries)
 5. accounting: <= top_n positions, weights sum <= 1, no double entry, entries pass the universe test, only positive-E/P names bought"""
import os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); PEAD = os.path.join(os.path.dirname(HERE), 'csm_pead'); sys.path.insert(0, HERE); sys.path.insert(0, PEAD)
import run_pead_backtest as rp
from value_strategy import EarningsYieldStrategy
from value_fundamentals import build_results
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else '')); (None if ok else fails.append(name))
prices, volumes, highs, lows, opens, bench = rp.load_all()
mk = lambda p, v, h, l, o, b: EarningsYieldStrategy(prices_df=p, volumes_df=v, highs_df=h, lows_df=l, opens_df=o, benchmark_series=b)
st = mk(prices, volumes, highs, lows, opens, bench); st.calculate_factors(); res = st.simulate(); tr = res['trades']; dates = st._dates
# 1
raw = build_results(symbols=list(prices.columns)); rng = np.random.default_rng(3); bad = 0; n = 0
ep = st.ep.dropna(how='all')
for _ in range(400):
    d = ep.index[rng.integers(0, len(ep))]; row = ep.loc[d].dropna()
    if row.empty: continue
    s = row.index[rng.integers(0, len(row))]
    g = raw[(raw.symbol == s) & (raw.filed <= d)].sort_values('filed')
    last = g.iloc[-1]; px = st._C[int(dates.get_loc(d)), st._cols[s]]
    exp = last.np_ttm / (px * last.shares); n += 1
    if (d - last.filed).days > st.max_age or not np.isclose(exp, row[s], rtol=1e-9):
        bad += 1
check('1. E/P re-derived independently from results filed on/before the date', bad == 0, f'{n} samples, {bad} mismatches')
# 2
cut = pd.Timestamp('2023-06-30'); p2, v2, h2, l2, o2 = [d.loc[:cut] for d in (prices, volumes, highs, lows, opens)]
s2 = mk(p2, v2, h2, l2, o2, bench.loc[:cut]); s2.calculate_factors(); r2 = s2.simulate()
common = st.ep.index.intersection(s2.ep.index); common = common[common <= '2023-03-31']
check('2a. E/P rows identical on truncated data', all(st.ep.loc[d].fillna(-9).equals(s2.ep.loc[d].fillna(-9)) or np.allclose(st.ep.loc[d].fillna(-9).values, s2.ep.loc[d].fillna(-9).values) for d in common), f'{len(common)} months')
e1 = res['equity'].loc[:'2023-03-31']; e2 = r2['equity'].loc[:'2023-03-31']; j = e1.index.intersection(e2.index)
check('2b. simulated equity identical on truncated data', len(j) > 800 and np.allclose(e1[j], e2[j], rtol=1e-9), f'{len(j)} days, max rel diff {np.max(np.abs(e1[j]/e2[j]-1)):.2e}')
# 3
bad = 0; n = 0
for t in tr[tr.Reason == 'STOP_HIT'].itertuples():
    j = st._cols[t.Ticker]; ei = int(dates.get_loc(t.Entry_Date)); xi = int(dates.get_loc(t.Exit_Date)); dd = xi - 1
    port = {t.Ticker: dict(entry_price=t.Entry_Price)}
    for d, want in ((dd - 1, False), (dd, True)):
        if d <= ei: continue
        g = st.get_exit_signals(port, {t.Ticker: dict(close=float(st._C[d, j]))}); got = t.Ticker in g['exits']; n += 1
        bad += (got != want)
check('3. get_exit_signals agrees with every simulated STOP_HIT', bad == 0, f'{n} checks, {bad} mismatches ({int((tr.Reason=="STOP_HIT").sum())} stops)')
# 4
exec_days = sorted(set(tr[tr.Reason == 'REBAL_EXIT'].Exit_Date) | set(tr.Entry_Date)); bad_s = 0; bad_b = 0; k = 0
sig_of = {int(i) + 1: int(i) for i in st._sig_idx}
for d in exec_days:
    xi = int(dates.get_loc(d))
    if xi not in sig_of: continue
    nxt = dates[xi + 1] if xi + 1 < len(dates) else None
    held = tr[(tr.Entry_Date < d) & ((tr.Exit_Date > d) | ((tr.Exit_Date == d) & (tr.Reason == 'REBAL_EXIT'))) & ~((tr.Reason == 'STOP_HIT') & (tr.Exit_Date == nxt))].Ticker.tolist()   # a stop flagged on the rebalance day's own close exits at the next open and is not part of the rebalance
    adv = st.get_target_portfolio(dates[sig_of[xi]], held)
    sold = set(tr[(tr.Exit_Date == d) & (tr.Reason == 'REBAL_EXIT')].Ticker); bought = set(tr[tr.Entry_Date == d].Ticker)
    k += 1
    bad_s += (sold != set(adv['sell'])); bad_b += (not bought <= {b for b, _ in adv['buy']})
check('4. get_target_portfolio reproduces executed sells (exact) and buys (subset)', bad_s == 0 and bad_b == 0, f'{k} rebalances, sell mismatches {bad_s}, buy mismatches {bad_b}')
# 5
W = res['executed_weights']; d = res['daily']
check('5a. never above top_n positions', int(d.n_positions.max()) <= st.top_n, f'max {int(d.n_positions.max())}')
check('5b. weights sum <= 1', bool((W.sum(axis=1) <= 1.0001).all()), f'max {W.sum(axis=1).max():.3f}')
ov = tr.sort_values(['Ticker', 'Entry_Date']); ov['pe'] = ov.groupby('Ticker').Exit_Date.shift(1)
check('5c. no double entry', bool((ov.Entry_Date >= ov.pe.fillna(pd.Timestamp('1900-01-01'))).all()))
check('5d. entries pass the universe test and have positive E/P', all(st._universe_ok(int(dates.get_loc(t.Entry_Date)), st._cols[t.Ticker]) and t.EP > 0 for t in tr.itertuples()), f'{len(tr)} trades')
print('\nALL PASS' if not fails else f'\nFAILED: {fails}'); sys.exit(1 if fails else 0)

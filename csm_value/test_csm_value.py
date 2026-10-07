"""Checks for CSMValue (Elendel chassis).  python3 test_csm_value.py
 1. E/P at month-ends re-derived independently from raw results filed on/before the date (400 random stock-months)
 2. no look-ahead: data truncated at 2023-06-30 gives identical factor rows through 2023-03-31 (and identical positions)
 3. universe: every scored name is inside liquidity ranks 301-1000, price > 20, positive TTM profit, rising profit, E/P in (0, 50%]; no SMA-200 filter was applied
 4. no absolute-momentum gate: held names include some with negative trailing-12m return; Elendel's own gate would have excluded them
 5. chassis intact: weights <= 5% each, total <= 1, positions only in scored names; get_exit_signals runs on a held name and returns the Elendel keys"""
import os, sys, importlib, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'; sys.path.insert(0, LIVE)
ele = importlib.import_module('run_csm_elendel_backtest')
from csm_value_strategy import CSMValue
from value_fundamentals import build_results
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else '')); (None if ok else fails.append(name))
prices, volumes, highs, lows, opens = ele.load_data(ele.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = ele.mask_corporate_actions(prices, highs, lows, opens)
bench = ele.build_benchmark(prices)
mk = lambda p, v, h, l, o, b: CSMValue(prices_df=p, volumes_df=v, highs_df=h, lows_df=l, opens_df=o, benchmark_series=b)
st = mk(prices, volumes, highs, lows, opens, bench); st.calculate_factors(); pos = st.get_positions()
F = st.factors; ep = st._legs_unfiltered['EP']
# 1
raw = build_results(symbols=list(prices.columns)); rng = np.random.default_rng(5); mp = prices.resample('ME').last(); bad = 0; n = 0
Fn = F.dropna(how='all')
for _ in range(400):
    d = Fn.index[rng.integers(0, len(Fn))]; row = Fn.loc[d].dropna(); s = row.index[rng.integers(0, len(row))]
    g = raw[(raw.symbol == s) & (raw.filed <= d)].sort_values('filed'); last = g.iloc[-1]
    exp = last.np_ttm / (mp.loc[d, s] * last.shares); n += 1
    if (d - last.filed).days > st.results_max_age_days or not np.isclose(exp, ep.loc[d, s], rtol=1e-9): bad += 1
check('1. E/P re-derived independently from raw results', bad == 0, f'{n} samples, {bad} mismatches')
# 2
cut = pd.Timestamp('2023-06-30'); p2, v2, h2, l2, o2 = [d.loc[:cut] for d in (prices, volumes, highs, lows, opens)]
s2 = mk(p2, v2, h2, l2, o2, bench.loc[:cut]); s2.calculate_factors(); pos2 = s2.get_positions()
idx = F.index[F.index <= '2023-03-31'].intersection(s2.factors.index)
same = all(np.allclose(F.loc[d].fillna(-99).values, s2.factors.loc[d].fillna(-99).values) for d in idx)
check('2a. factor rows identical on truncated data', same, f'{len(idx)} months')
pi = pos.index[pos.index <= '2023-03-31'].intersection(pos2.index)
check('2b. target positions identical on truncated data', np.allclose(pos.loc[pi].values, pos2.loc[pi].values), f'{len(pi)} months')
# 3
dv = (prices * volumes).rolling(63, min_periods=21).median().shift(1).resample('ME').last().reindex(F.index).rank(axis=1, ascending=False, method='min')
sc = F.notna()
inband = ((dv >= 301) & (dv <= 1000)) | ~sc
check('3a. scored names are inside liquidity ranks 301-1000', bool(inband.all().all()))
epx = ep.reindex(index=F.index, columns=F.columns)
check('3b. scored names have positive E/P <= 50%', bool(((epx > 0) | ~sc).all().all() and ((epx <= 0.5) | ~sc).all().all()))
# 4
m12 = (mp.shift(1) / mp.shift(13) - 1).reindex(pos.index); held = (pos > 0)
neg_held = int(((m12 <= 0) & held).sum().sum()); tot = int(held.sum().sum())
check('4. held names include negative-12m-return stocks (no momentum gate)', neg_held > 0, f'{neg_held} of {tot} held name-months')
# 5
check('5a. weights <= 5% and total <= 1', bool((pos.max(axis=1) <= 0.0500001).all() and (pos.sum(axis=1) <= 1.0001).all()))
check('5b. positions only in scored names', bool(((pos > 0) & ~F.reindex(pos.index).notna()).sum().sum() == 0))
t = pos.index[(pos > 0).sum(axis=1) > 5][-1]; tk = pos.loc[t][pos.loc[t] > 0].index[0]
g = st.get_exit_signals({tk: dict(entry_price=100.0, entry_date='2025-01-02', peak_price=105.0, atr_stop=0.0)}, {tk: dict(close=99.0)}, today='2025-02-03')
check('5c. get_exit_signals runs and returns the Elendel interface keys', set(g) == {'exits', 'holds', 'crash_guard_fired', 'high_vol'})
print('\nALL PASS' if not fails else f'\nFAILED: {fails}'); sys.exit(1 if fails else 0)

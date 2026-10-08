"""Checks for CSMValue.  python3 test_csm_value.py     (needs only this folder, the OHLCV folder and the raw fundamentals JSON folder)
 1. E/P at month-ends re-derived independently from the loader's results table (400 random stock-months)
 2. no look-ahead: data truncated at 2023-06-30 gives identical factor rows through 2023-03-31 (and identical target positions)
 3. universe: every scored name is inside liquidity ranks 301-1000 with positive E/P <= 50%, positive TTM profit and rising quarterly profit
 4. no absolute-momentum gate: held names include some with negative trailing-12m return
 5. chassis intact: weights <= 5%, total <= 1, positions only in scored names; get_exit_signals keeps the Elendel interface
 6. units: restoring today's share units cuts the number of >2x market-cap jumps between consecutive filings of split/bonus companies (vs raw share counts)
 9. engine accounting reconciles with the trade log; 10. full-engine truncation invariance
 7. self-contained: no source file in this folder reads pit_harness, a parquet/pickle cache, or another project's code"""
import glob, os, re, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import run_csm_value_backtest as rb
from csm_value_strategy import CSMValue
import fundamentals_loader as fl
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else '')); (None if ok else fails.append(name))
prices, volumes, highs, lows, opens = rb.load_data(rb.data_folder_path)
sl = lambda d: d.loc['2001-01-01':'2025-06-30']
prices, volumes, highs, lows, opens = map(sl, (prices, volumes, highs, lows, opens))
prices, highs, lows, opens = rb.mask_corporate_actions(prices, highs, lows, opens)
bench = rb.build_benchmark(prices)
mk = lambda p, v, h, l, o, b: CSMValue(prices_df=p, volumes_df=v, highs_df=h, lows_df=l, opens_df=o, benchmark_series=b)
st = mk(prices, volumes, highs, lows, opens, bench); st.calculate_factors(); pos = st.get_positions()
F = st.factors; ep = st._legs_unfiltered['EP']
# 1
raw = fl.load_results(symbols=list(prices.columns)); rng = np.random.default_rng(5); mp = prices.resample('ME').last(); bad = 0; n = 0
Fn = F.dropna(how='all')
for _ in range(400):
    d = Fn.index[rng.integers(0, len(Fn))]; row = Fn.loc[d].dropna(); s = row.index[rng.integers(0, len(row))]
    g = raw[(raw.symbol == s) & (raw.filed <= d)].sort_values('filed'); last = g.iloc[-1]
    exp = last.np_ttm / (mp.loc[d, s] * last.shares_adj); n += 1
    if (d - last.filed).days > st.results_max_age_days or not np.isclose(exp, ep.loc[d, s], rtol=1e-9): bad += 1
check('1. E/P re-derived independently from the results table', bad == 0, f'{n} samples, {bad} mismatches')
# 2
cut = pd.Timestamp('2023-06-30'); p2, v2, h2, l2, o2 = [d.loc[:cut] for d in (prices, volumes, highs, lows, opens)]
s2 = mk(p2, v2, h2, l2, o2, bench.loc[:cut]); s2.calculate_factors(); pos2 = s2.get_positions()
idx = F.index[F.index <= '2023-03-31'].intersection(s2.factors.index)
check('2a. factor rows identical on truncated data', all(np.allclose(F.loc[d].fillna(-99).values, s2.factors.loc[d].fillna(-99).values) for d in idx), f'{len(idx)} months')
pi = pos.index[pos.index <= '2023-03-31'].intersection(pos2.index)
check('2b. target positions identical on truncated data', np.allclose(pos.loc[pi].values, pos2.loc[pi].values), f'{len(pi)} months')
# 3
dv = (prices * volumes).rolling(63, min_periods=21).median().shift(1).resample('ME').last().reindex(F.index).rank(axis=1, ascending=False, method='min')
sc = F.notna(); epx = ep.reindex(index=F.index, columns=F.columns)
check('3a. scored names are inside liquidity ranks 301-1000', bool((((dv >= 301) & (dv <= 1000)) | ~sc).all().all()))
check('3b. scored names have positive E/P <= 50%', bool(((epx > 0) | ~sc).all().all() and ((epx <= 0.5) | ~sc).all().all()))
gr = fl.monthly_frame(raw, 'sg_np', F.index, F.columns, st.results_max_age_days); ttm = fl.monthly_frame(raw, 'np_ttm', F.index, F.columns, st.results_max_age_days)
check('3c. scored names have positive TTM profit and rising quarterly profit', bool(((ttm > 0) & (gr > 0) | ~sc).all().all()))
# 4
m12 = (mp.shift(1) / mp.shift(13) - 1).reindex(pos.index); held = (pos > 0)
neg_held = int(((m12 <= 0) & held).sum().sum()); tot = int(held.sum().sum())
check('4. held names include negative-12m-return stocks (no momentum gate)', neg_held > 0, f'{neg_held} of {tot} held name-months')
# 5
check('5a. weights <= 5% and total <= 1', bool((pos.max(axis=1) <= 0.0500001).all() and (pos.sum(axis=1) <= 1.0001).all()))
check('5b. positions only in scored names', bool(((pos > 0) & ~F.reindex(pos.index).notna()).sum().sum() == 0))
t = pos.index[(pos > 0).sum(axis=1) > 5][-1]; tk = pos.loc[t][pos.loc[t] > 0].index[0]
g = st.get_exit_signals({tk: dict(entry_price=100.0, entry_date='2025-01-02', peak_price=105.0, atr_stop=0.0)}, {tk: dict(close=99.0)}, today='2025-02-03')
check('5c. get_exit_signals returns the Elendel interface keys', set(g) == {'exits', 'holds', 'crash_guard_fired', 'high_vol'})
# 6
rows = []
for p in sorted(glob.glob(fl.FUNDAMENTALS_DIR + '/*.json')): rows.extend(fl._read_symbol(p))
df = pd.DataFrame(rows); big_raw = big_adj = pairs = 0
for sym, g in df.groupby('symbol'):
    sh = g.groupby('period_end').shares.median().sort_index().dropna()
    if len(sh) < 2 or sym not in prices.columns: continue
    f = fl._split_factor_per_period(sh)
    if f.isna().any() or not (np.abs(f - 1) > 1e-9).any(): continue
    px = prices[sym].dropna(); filed = g.groupby('period_end').filed.max().reindex(sh.index); ix = pd.DatetimeIndex(filed.values)
    p = px.reindex(px.index.union(ix.unique())).ffill().loc[ix].values
    for series, which in ((sh.values, 'raw'), ((sh * f).values, 'adj')):
        d = np.abs(np.diff(np.log(p * series))); d = d[np.isfinite(d)]
        if which == 'raw': big_raw += int((d > 0.69).sum())
        else: big_adj += int((d > 0.69).sum())
    pairs += len(sh) - 1
check('6. restoring share units removes spurious >2x market-cap jumps', big_adj < 0.7 * big_raw, f'{pairs} filing pairs of split/bonus companies: {big_raw} jumps with raw shares -> {big_adj} with restored units')

# 8. corporate-action mask, re-derived independently from raw prices and the results table
r1 = prices.pct_change(fill_method=None); mday = prices.isna() & prices.shift(1).notna() & prices.shift(-1).notna()
cl = mday.copy()
for c_ in (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0):
    cl |= (r1 - (1 / c_ - 1)).abs() <= st.ca_tol; cl |= (r1 - (c_ - 1)).abs() <= st.ca_tol * c_
stale = st.ca_stale_mask; sm = stale[stale.any(axis=1)]
rng = np.random.default_rng(11); bad_s = 0; n_s = 0
pairs = [(d, c) for d in sm.index for c in sm.columns[sm.loc[d].values]]
for k in rng.choice(len(pairs), size=min(300, len(pairs)), replace=False):
    d, s_ = pairs[k]; g = raw[(raw.symbol == s_) & (raw.filed <= d)].sort_values('filed'); L = g.filed.iloc[-1]
    seg = cl.loc[(cl.index > L) & (cl.index <= d), s_]; n_s += 1
    bad_s += (not bool(seg.any()))
check('8a. every sampled stale-mask month really has a corporate-action cliff after its latest filing', bad_s == 0, f'{n_s} samples, {bad_s} wrong')
bad_f = 0; n_f = 0
scored = F.notna()
for _ in range(400):
    d = F.index[scored.any(axis=1).values][rng.integers(0, int(scored.any(axis=1).sum()))]; row = scored.loc[d]; s_ = row.index[row.values][rng.integers(0, int(row.sum()))]
    L = raw[(raw.symbol == s_) & (raw.filed <= d)].sort_values('filed').filed.iloc[-1]
    n_f += 1; bad_f += bool(cl.loc[(cl.index > L) & (cl.index <= d), s_].any())
check('8b. no scored stock-month has a cliff after the filing it uses', bad_f == 0, f'{n_f} samples, {bad_f} violations')
tot_steps = skipped = 0
for sym, g in df.groupby('symbol'):
    sh = g.groupby('period_end').shares.median().sort_index().dropna()
    f_noc = fl._split_factor_per_period(sh)
    if f_noc.isna().any(): continue
    steps_all = (f_noc / f_noc.shift(-1)).iloc[:-1] if len(f_noc) > 1 else pd.Series(dtype=float)
    tot_steps += int((np.abs(steps_all - 1) > 1e-9).sum())
res_masked = fl.load_results(symbols=list(prices.columns))
print(f'   info: clean split/bonus steps seen in filings: {tot_steps}')

# 9. engine accounting: booked P&L of the closed trades must agree with the trade log's own fills (this is what exposed the original Elendel booking)
import execution_replay as er
rb_res = rb.backtest_event_driven(st, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
Wx = rb_res['executed_weights']; ix = Wx.index; cx = {x: k for k, x in enumerate(Wx.columns)}
DRx = prices.pct_change(fill_method=None).fillna(0).reindex(index=ix, columns=Wx.columns).values
metax = pd.DataFrame(st.position_metadata); metax = metax[(metax.Entry_Date >= pd.Timestamp('2019-06-03')) & (metax.Exit_Reason != 'END_OF_PERIOD') & (metax.Exit_Date <= pd.Timestamp('2025-06-30'))]
orig = sum((Wx.values[ix.get_loc(t.Entry_Date):ix.get_loc(t.Exit_Date), cx[t.Ticker]] * DRx[ix.get_loc(t.Entry_Date):ix.get_loc(t.Exit_Date), cx[t.Ticker]]).sum() for t in metax.itertuples())
fills = sum(Wx.values[ix.get_loc(t.Entry_Date):ix.get_loc(t.Exit_Date), cx[t.Ticker]].mean() * (t.Exit_Price / t.Entry_Price - 1) for t in metax.itertuples())
net_f, _ = er.faithful_net_returns(st, rb_res, daily_cash_rate=((1 + st.liquid_mf_annual_rate) ** (1 / 252) - 1) if st.use_liquid_mf else 0.0)   # the replay must earn the same idle-cash rate as the runner
cg_ = lambda x: (1 + x.loc['2019-06-03':'2025-06-30']).prod() ** (365.25 / (pd.Timestamp('2025-06-30') - pd.Timestamp('2019-06-03')).days) - 1
check('9a. the runner\'s execution-faithful booking equals the independent replay (CAGR within 0.1 pt)', abs(cg_(st._net_by_booking['faithful']) - cg_(net_f)) < 0.001)
say_ratio = orig / fills
print(f'   info: the ORIGINAL Elendel booking would credit {orig:+.3f} of equity for these trades vs {fills:+.3f} implied by buy-and-hold at their fills ({say_ratio:.2f}x); the runner prints both bookings')
check('9b. the original booking overstates trade P&L by > 1.3x (documents why the faithful booking is always reported next to the headline)', say_ratio > 1.3)
check('9c. headline = engine booking (flag False, comparable with Elendel/Zenith/Quad) and both bookings are exposed', rb.EXECUTION_FAITHFUL_ACCOUNTING is False and set(st._net_by_booking) == {'engine', 'faithful'} and np.allclose(rb_res['net_returns'].values, st._net_by_booking['engine'].values))
# 10. full-engine truncation invariance (signals, regimes, vol scaling, stops, fills all causal)
cut = pd.Timestamp('2023-03-31'); p2, v2, h2, l2, o2 = [d.loc[:cut] for d in (prices, volumes, highs, lows, opens)]
s3 = mk(p2, v2, h2, l2, o2, bench.loc[:cut]); s3.calculate_factors(); s3.get_positions()
r3 = rb.backtest_event_driven(s3, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)['net_returns']
jj = r3.index.intersection(rb_res['net_returns'].index); jj = jj[jj <= cut - pd.Timedelta(days=10)]
check('10. the FULL engine path is identical when the data is cut at 2023-03-31 (nothing uses the future)', np.abs(r3[jj] - rb_res['net_returns'][jj]).max() < 1e-10, f'{len(jj)} days, max diff {np.abs(r3[jj] - rb_res["net_returns"][jj]).max():.1e}')

# 11. Item 5 / 7 fields, re-derived independently from the raw JSON
import json as _json
rr = fl.load_results(symbols=list(prices.columns), profit_basis='core'); rt = fl.load_results(symbols=list(prices.columns), profit_basis='total')
rng2 = np.random.default_rng(21); samp = rr[rr.period_end >= '2020-12-31'].sample(60, random_state=3); bad_o = bad_c = n_o = 0
cache_ = {}
for r_ in samp.itertuples():
    d_ = cache_.setdefault(r_.symbol, _json.load(open(f'{fl.FUNDAMENTALS_DIR}/{r_.symbol}.json')))
    qs = {}
    for fy_, nd in d_['fiscal_years'].items():
        for qq_, qn in nd['quarters'].items():
            b_ = qn.get(r_.basis)
            if not b_: continue
            inc = b_.get('income_statement') or {}; per = b_.get('period') or {}
            if per.get('end'): qs[pd.Timestamp(per['end'][:10])] = inc
    ends = pd.date_range(end=r_.period_end, periods=4, freq='QE')
    if not all(e in qs for e in ends): continue
    isb = any((qs[e].get('revenue_from_operations') is None and (qs[e].get('other_facts') or {}).get('InterestEarned') is not None) for e in ends)
    g = lambda e, k: (qs[e].get(k) if qs[e].get(k) is not None else 0.0)
    pbt_ = sum(g(e, 'profit_before_tax') for e in ends); oi_ = sum(g(e, 'other_income') for e in ends)
    exc_ = sum(max(g(e, 'profit_before_tax') - g(e, 'profit_before_exceptional_and_tax'), 0.0) for e in ends)
    exp_oo = 0.0 if isb else ((oi_ + exc_) / pbt_ if pbt_ > 0 else np.nan)
    n_o += 1
    if not (np.isclose(exp_oo, r_.oneoff_share, rtol=1e-6, equal_nan=True)): bad_o += 1
check('11a. one-off share (other income + exceptional gains over TTM pre-tax profit) re-derived from the raw JSON', bad_o == 0, f'{n_o} samples, {bad_o} mismatches')
mm = rt.merge(rr, on=['symbol', 'period_end'], suffixes=('_t', '_c'))
check('11b. core profit differs from reported profit only through other income / exceptional items (banks identical)', bool(np.isfinite(mm.np_ttm_c).all()) and len(mm) == len(rt) and (mm.np_ttm_c / mm.np_ttm_t).median() < 1.0)
check('11c. the idle-cash sweep into a liquid fund is on (use_liquid_mf) and the default profit definition is the reported net profit with no one-off filter', st.use_liquid_mf is True and st.profit_basis == 'total' and st.max_oneoff_share is None)

# 12. Item 6 / Item 3 options
sc_ = mk(prices, volumes, highs, lows, opens, bench); sc_.min_cooldown_days = 42; sc_.book_size_cr = 5.0; sc_.max_adv_participation = 0.10
sc_.calculate_factors(); pos_c = sc_.get_positions()
check('12a. min_cooldown_days puts a floor under every stop cooldown (profitable stops included) and leaves longer cooldowns alone', sc_._cooldown_days_for(+8.0) == 42 and sc_._cooldown_days_for(-30.0) >= 42 and st._cooldown_days_for(+8.0) == 0)
adv_ = sc_._adv_monthly.reindex(index=pos_c.index, columns=pos_c.columns)
lim_ = (0.10 * adv_ / (5.0 * 1e7)).fillna(0.0)
check('12b. capacity cap: every target weight <= 10% of the name\'s median daily traded value for a Rs 5 cr book', bool(((pos_c - lim_) <= 1e-12).all().all()), f'max target weight {pos_c.max().max():.3%}; tightest cap hit in {(abs(pos_c - lim_) < 1e-12).sum().sum() if False else int(((pos_c > 0) & ((pos_c - lim_).abs() < 1e-12)).sum().sum())} name-months')
check('12c. the cap is off by default and the default cooldown floor is 0', st.book_size_cr is None and st.min_cooldown_days == 0)
# 7
bad_refs = []
for f in glob.glob(os.path.join(HERE, '*.py')):
    if os.path.basename(f) in ('test_csm_value.py', '_generate_elendel_chassis.py'): continue
    src = open(f).read()
    for pat in ('pit_harness', 'read_parquet', 'to_parquet', 'pickle.load', 'factor_research', 'momentum_gold', 'momentum_value', 'csm_pead'):
        if pat in src: bad_refs.append((os.path.basename(f), pat))
check('7. strategy, loader and runner do not touch pit_harness / caches / other projects', not bad_refs, str(bad_refs) if bad_refs else 'clean')
print('\nALL PASS' if not fails else f'\nFAILED: {fails}'); sys.exit(1 if fails else 0)

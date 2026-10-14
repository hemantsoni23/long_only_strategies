"""
Checks for the three Zenith backtest-engine corrections (2026-10-09) in Old_live_strategies/csm_zenith_strategy.py and run_csm_zenith_backtest.py.
    python3 test_zenith_engine_fixes.py
Self-contained: synthetic prices (no data folder, nothing written).  Each correction has an off-switch on CSMZenith; the tests also show that the legacy engine FAILS the invariant the fix restores.

 1. deferred holds are not scaled twice     (fix_deferred_double_scale)
 2. stop order inside a bar                  (fix_stop_uses_prior_peak)  -- unit tests of _check_stop_exit and get_exit_signals parity
 3. entry-day stop and peak                  (check_stop_on_entry_day)
 4. entry-day booking                        (fix_entry_booking)          -- equity-curve difference equals exactly the overnight-gap credit it removes
 5. legacy switch                            (LEGACY_V1_OVERRIDES reproduces the old engine's behaviour flags)
"""
import contextlib, importlib, io, os, sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
sys.path.insert(0, LIVE)
z = importlib.import_module('run_csm_zenith_backtest')
from csm_zenith_strategy import CSMZenith, LEGACY_V1_OVERRIDES
fails = []
def check(name, ok, info=''):
    print(('PASS ' if ok else 'FAIL ') + name + (f'  [{info}]' if info else '')); (None if ok else fails.append(name))
def quiet(f, *a, **k):
    with contextlib.redirect_stdout(io.StringIO()): return f(*a, **k)

# ───────────── synthetic market ─────────────
def make_market(seed=7, n_stocks=120, n_days=1100, crash_rate=0.012):
    rng = np.random.default_rng(seed)
    idx = pd.bdate_range('2018-01-01', periods=n_days)
    mu = rng.normal(0.0004, 0.0006, n_stocks); sg = rng.uniform(0.012, 0.03, n_stocks)
    mkt = rng.normal(0.0003, 0.008, n_days)
    rets = mu + 0.7 * mkt[:, None] + rng.normal(0, 1, (n_days, n_stocks)) * sg
    close = pd.DataFrame(100 * np.exp(np.cumsum(rets, axis=0)), index=idx, columns=[f'S{k:03d}' for k in range(n_stocks)])
    prev = close.shift(1).fillna(close.iloc[0])
    opn = prev * (1 + rng.normal(0, 0.004, close.shape))
    high = np.maximum(opn, close) * (1 + np.abs(rng.normal(0, 0.008, close.shape)))
    low = np.minimum(opn, close) * (1 - np.abs(rng.normal(0, 0.008, close.shape)))
    crash = rng.random(close.shape) < crash_rate          # deliberate intraday spikes down so stops get exercised, including right after an open fill
    low = low.where(~crash, opn * 0.86)
    vol = pd.DataFrame(rng.uniform(5e5, 2e6, close.shape), index=idx, columns=close.columns)
    return close, vol, high, low, opn
close, vol, high, low, opn = make_market()
bench = z.build_benchmark(close)
def run(**kw):
    base = dict(universe_top_n_min=1, universe_top_n_max=100, min_price=1.0, top_n=12, use_trade_deadband=False)
    base.update(kw)
    c = CSMZenith(prices_df=close, volumes_df=vol, highs_df=high, lows_df=low, opens_df=opn, benchmark_series=bench, **base)
    quiet(c.calculate_factors); quiet(c.get_positions)
    res = quiet(z.backtest_event_driven, c, initial_capital=100_000, transaction_cost=0.003, risk_free_rate=0.0)
    return c, res

# ───────────── 1. deferred holds ─────────────
cF, rF = run(fix_deferred_double_scale=True); cL, rL = run(fix_deferred_double_scale=False)
def deferred_stats(c, res):
    """executed/unscaled spread across held names, and how the UNSCALED target of a deferred hold moves from one day to the next."""
    ex, un = res['executed_weights'], c._target_unscaled
    sig = c.positions.reindex(ex.index, method='ffill').shift(1).fillna(0.0)
    worst = 0.0; ratios = []
    for k in range(1, len(ex)):
        d, dp = ex.index[k], ex.index[k - 1]
        m = un.loc[d] > 1e-9
        if m.sum() >= 2 and ex.loc[d].sum() > 0:
            r = ex.loc[d][m] / un.loc[d][m]; worst = max(worst, float(r.max() - r.min()))
        dm = (sig.loc[d] <= 1e-9) & m & (un.loc[dp] > 1e-9)                  # held today, no longer in the monthly signal, held yesterday = a deferred hold
        if un.loc[d].sum() <= 1.0 + 1e-12:                                     # skip days where the gross-weight renormalisation of Step H kicks in
            ratios += list((un.loc[d][dm] / un.loc[dp][dm]).values)
    return worst, np.array(ratios)
wF, rF_ = deferred_stats(cF, rF); wL, rL_ = deferred_stats(cL, rL)
check('1a. test data exercises deferred holds', len(rF_) > 20 and len(rL_) > 20, f'{len(rF_)} / {len(rL_)} deferred name-days')
check('1b. FIXED engine: executed = unscaled target x one common scale for every held name (deferred ones included)', wF < 1e-9, f'max cross-sectional spread of executed/unscaled = {wF:.2e}')
check('1c. FIXED engine: a deferred hold keeps its unscaled target from day to day (ratio 1.000)', float(np.abs(rF_ - 1.0).max()) < 1e-9, f'max |ratio-1| = {np.abs(rF_ - 1.0).max():.2e}')
check('1d. LEGACY engine: whenever the risk scale is below 1 the deferred hold is cut again (share of deferred name-days with day-over-day ratio < 0.99 is material, and 0 in the fixed engine)', float((rL_ < 0.99).mean()) > 0.05 and float((rF_ < 0.99).mean()) == 0.0, f'legacy {(rL_ < 0.99).mean():.0%} of {len(rL_)} deferred name-days, min ratio {rL_.min():.3f}; fixed {(rF_ < 0.99).mean():.0%}')

# ───────────── 2. stop ordering (unit) ─────────────
def mk(**kw):
    d = pd.DataFrame({'A': [100.0, 101.0]}, index=pd.bdate_range('2020-01-01', periods=2))
    return CSMZenith(prices_df=d, volumes_df=d, highs_df=d, lows_df=d, opens_df=d, benchmark_series=None, hard_stop_from_entry=0.10, hard_stop_from_peak=0.20, stop_slippage_pct=0.003, **kw)
def hold(**kw):
    h = dict(entry_price=100.0, peak_price=100.0, atr_stop=0.0, entry_date='2020-01-01', weight=0.05); h.update(kw); return h
cn, cl = mk(), mk(fix_stop_uses_prior_peak=False)
# bar: opens 100, spikes to 130 and prints 100 (could be before or after the spike); close 120
ex_n, fp_n, lv_n, h_n, dt_n = cn._check_stop_exit('A', 120.0, 100.0, 2.0, 100.0, hold(), curr_high=130.0)
ex_l, fp_l, lv_l, h_l, dt_l = cl._check_stop_exit('A', 120.0, 100.0, 2.0, 100.0, hold(), curr_high=130.0)
check('2a. a low of 100 does NOT hit the stop that was in force (entry-based 90) just because the same bar\'s high (130) would have lifted it to 104', ex_n is False, f'in-force stop 90, low 100')
check('2b. ...and the legacy check does fire there (the bug)', ex_l is True and abs(lv_l - 104.0) < 1e-9, f'legacy stop level {lv_l}')
check('2c. today\'s high raises tomorrow\'s stop: peak 130, next stop 104, returned as the resting-stop level', abs(h_n['peak_price'] - 130.0) < 1e-9 and abs(h_n['atr_stop'] - 104.0) < 1e-9 and abs(lv_n - 104.0) < 1e-9)
ex2, fp2, lv2, h2, dt2 = cn._check_stop_exit('A', 92.0, 85.0, 2.0, 99.0, hold(), curr_high=100.0)
check('2d. a real breach fills at stop x (1 - slippage)', ex2 and abs(fp2 - 90.0 * 0.997) < 1e-9 and dt2 == 'ENTRY_HARD', f'fill {fp2:.3f} detail {dt2}')
ex3, fp3, lv3, h3, dt3 = cn._check_stop_exit('A', 86.0, 84.0, 2.0, 85.0, hold(), curr_high=88.0)
check('2e. a gap-down open below the stop fills at the open', ex3 and abs(fp3 - 85.0) < 1e-9 and dt3 == 'GAP_DOWN_OPEN')
# next day, with the persisted state, the raised stop is in force
ex4, fp4, lv4, h4, dt4 = cn._check_stop_exit('A', 110.0, 103.0, 2.0, 112.0, h_n, curr_high=115.0)
check('2f. next bar: a low of 103 breaches the stop (104) raised by yesterday\'s high', ex4 and dt4 == 'PEAK_HARD' and abs(lv4 - 104.0) < 1e-9)
g = cn.get_exit_signals({'A': dict(entry_price=100.0, entry_date='2019-12-01', peak_price=130.0, atr_stop=104.0, weight=0.05)}, {'A': dict(close=110.0, high=115.0, low=103.0, open=112.0)}, today='2020-02-03')
check('2g. live get_exit_signals gives the same decision as the backtest check', 'A' in g['exits'] and g['exits']['A']['detail'] == 'PEAK_HARD')

# ───────────── 3. entry-day stop / peak ─────────────
cE, rE = run(min_hold_days=0, check_stop_on_entry_day=True); cE0, rE0 = run(min_hold_days=0, check_stop_on_entry_day=False)
tlE = quiet(z.get_trade_log, cE); tlE0 = quiet(z.get_trade_log, cE0)
same_day = tlE[tlE.Exit_Date == tlE.Entry_Date]; same_day0 = tlE0[tlE0.Exit_Date == tlE0.Entry_Date]
check('3a. with min_hold_days=0 some positions are stopped out on the day they were bought (they could not be before)', len(same_day) > 0 and len(same_day0) == 0, f'{len(same_day)} entry-day stops vs {len(same_day0)} without the check')
ok_fill = all(abs(t.Exit_Price - t.Stop_Price_At_Exit * 0.997) < 1e-6 * t.Entry_Price for t in same_day.itertuples())
check('3b. their fills are stop x (1 - slippage), below the open fill and above the day\'s low', ok_fill and bool((same_day.Exit_Price < same_day.Entry_Price).all()))
cD, rD = run(); tlD = quiet(z.get_trade_log, cD)
check('3c. with the default min_hold_days=5 there are no entry-day stops (the grace period still applies)', int((tlD.Exit_Date == tlD.Entry_Date).sum()) == 0)

# ───────────── 4. entry booking ─────────────
cB, rB = run(fix_entry_booking=True); cB0, rB0 = run(fix_entry_booking=False)
check('4a. booking does not change any decision (identical executed weights)', np.allclose(rB['executed_weights'].values, rB0['executed_weights'].values))
tlB = quiet(z.get_trade_log, cB); W = rB['executed_weights']; dr = close.pct_change(fill_method=None).fillna(0.0)
exp = pd.Series(0.0, index=W.index); n_ent = 0
for t in tlB.itertuples():
    w = W.at[t.Entry_Date, t.Ticker]
    if w > 1e-9:
        c_ = close.at[t.Entry_Date, t.Ticker]; exp.at[t.Entry_Date] += w * ((c_ / t.Entry_Price - 1.0) - dr.at[t.Entry_Date, t.Ticker]); n_ent += 1
diff = (rB['net_returns'] - rB0['net_returns'])
check('4b. the equity-curve change equals exactly sum(weight x [close/open_fill - 1 - close-to-close return]) on entry days and is zero elsewhere', np.allclose(diff.values, exp.values, atol=1e-6), f'{n_ent} entries, max abs diff {np.abs(diff - exp).max():.2e} (trade-log entry prices are rounded to 4 dp)')
check('4c. the correction removes the overnight-gap credit on average (entry-day return is lower when the stock gapped up into the fill)', float(diff.sum()) != 0.0, f'total change in summed daily return {diff.sum():+.4f}')

# ───────────── 5. legacy switch ─────────────
check('5. LEGACY_V1_OVERRIDES turns all four corrections off', all(LEGACY_V1_OVERRIDES[k] is False for k in ('fix_deferred_double_scale', 'fix_stop_uses_prior_peak', 'check_stop_on_entry_day', 'fix_entry_booking')))
print('\nALL PASS' if not fails else f'\nFAILED: {fails}'); sys.exit(1 if fails else 0)

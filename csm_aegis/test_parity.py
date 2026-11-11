"""Parity tests. (1) the module reproduces the pre-execution-integrity research engine (decay_check/strategy_engine*.py) bit-for-bit for v1.0, v1.1, v1.2 and for every
optional overlay; (2) the live exit rules (get_exit_signals) reproduce every stop / time / market-gate exit the backtest booked, one close earlier, and never fire
early; (3) the signals equal the research signal file."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); RES = os.path.join(os.path.dirname(HERE), 'decay_check')
sys.path.insert(0, HERE); sys.path.insert(0, RES)
import common as C, strategy_engine as SE, strategy_engine2 as SE2
from csm_aegis_strategy import CSMAegis
from csm_aegis_backtest import backtest_event_driven
P = C.load_panels()
# The reference engines predate raw-bar execution validation. Keep this file as
# a factor/legacy-booking parity test; test_execution_integrity.py validates the
# production fill model separately.
def mk(**kw):
    kw.setdefault('require_tradable_fill', False)
    return CSMAegis.from_panels(P, **kw).calculate_factors()
def cmp(name, S, **ref_kw):
    res = backtest_event_driven(S, log_rejects=False); ref = SE2.run(**ref_kw)
    d = float((res['ret'] - ref['ret']).abs().max()); print(f'{name:58s} max|diff| {d:.2e}  trades {len(res["trades"])} vs {len(ref["trades"])}'); assert d < 1e-12 and len(res['trades']) == len(ref['trades']); return res
A = mk()                                                              # legacy booking reproduction of v1.2
# the research file signals_all.pkl built r121 with ffill(limit=5); the module uses limit=10 everywhere. Give the research engine the module's r121 so the abs-momentum test compares like with like.
SE2.extras()['r121'] = A.r121_me
# likewise the research signal file stores R1/M3/A1/Ulcer as float32; feed the engine the module's float64 values so rank ties at filter boundaries cannot flip.
_D = SE.data()
for _n, _a in (('R1', A.R1), ('M3', A.M3), ('ULC', A.ULC), ('A1', A.A1)): _D['S'][_n] = pd.DataFrame(_a, index=A.per, columns=A.cols)
res = cmp('v1.2 default (R1+Ulcer, gate 120, close fills)', A, sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close')
cmp('v1.1 (R1, gate 150, open fills)', mk(selector='R1', mkt_gate_window=150, fill='open'), sel='R1', mkt_gate=True, mkt_win=150, fill='open')
r10 = backtest_event_driven(mk(selector='R1', mkt_gate=False, fill='open'), log_rejects=False); e10 = SE.run(sel='R1'); d = float((r10['ret'] - e10['ret']).abs().max()); print(f'{"v1.0 vs ORIGINAL v1.0 engine":58s} max|diff| {d:.2e}'); assert d < 1e-12
cmp('R1+A1 selector, band 200-1000 (high-return preset)', mk(selector='R1_A1', universe_min_rank=200), sel='R1A1', mkt_gate=True, mkt_win=120, fill='close', band=(200, 1000))
cmp('vol target 15%', mk(vol_target=0.15), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', vol_target=0.15)
cmp('crash guard', mk(crash_guard=True), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', crash_guard=True)
cmp('regime leverage + corr guard', mk(regime_leverage=True, corr_guard=True), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', regime_lev=True, corr_guard=True)
cmp('loss cooldown + min-hold + chandelier', mk(loss_cooldown=True, min_hold_stops=True, chandelier=True), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', loss_cooldown=True, minhold=True, chandelier=True)
cmp('abs-mom + falling-knife + quarterly + inverse-vol', mk(abs_momentum_gate=True, falling_knife_gate=True, quarterly_entries=True, inverse_vol_sizing=True), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', abs_mom=True, falling_knife=True, quarterly=True, invvol=True)
cmp('capacity cap + delay + no vol gate/time stop', mk(adv_fraction=0.05, initial_capital=1e7, execution_delay=1, vol_gate=False, time_stop=False), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='close', adv_frac=0.05, C0=1e7, delay=1, volgate=False, timestop=False)
cmp('resting-stop research variant', mk(resting_stop=True, fill='open'), sel='R1ULC', mkt_gate=True, mkt_win=120, fill='open', resting_stop=True)
Ap = mk(placebo_seed=3); rp = backtest_event_driven(Ap, log_rejects=False); ep = SE2.run(sel='random', seed=3, mkt_gate=True, mkt_win=120, fill='close'); dp = float((rp['ret'] - ep['ret']).abs().max()); print(f'{"placebo (random picks, seed 3)":58s} max|diff| {dp:.2e}'); assert dp < 1e-12
# signals
S_ = pickle.load(open(f'{C.CACHE}/signals_all.pkl', 'rb')); per = A.per   # original float32 research file, loaded fresh
for nm, arr in (('R1', A.R1), ('M3', A.M3), ('ULC', A.ULC), ('A1', A.A1)):
    ref = S_[nm].reindex(per).values.astype('float64'); d = float(np.nanmax(np.abs(ref - arr))); print(f'signal {nm}: max|diff| {d:.2e}'); assert d < 1e-5
# live exit rules vs booked exits
tl = res['trades']; dates = A.dates; bad = early = checked = 0
for t in tl[tl.Exit_Reason.isin(['STOP_ENTRY', 'STOP_TRAIL', 'TIME_STOP'])].sample(150, random_state=1).itertuples():
    ix = dates.get_loc(pd.Timestamp(t.Exit_Date)); ie = dates.get_loc(pd.Timestamp(t.Entry_Date)); h = {t.Ticker: dict(entry_date=t.Entry_Date, entry_price=t.Entry_Price)}
    checked += 1; bad += A.get_exit_signals(h, dates[ix - 1]).get(t.Ticker) != t.Exit_Reason
    for d_ in range(ie + 1, ix - 1):
        if t.Ticker in A.get_exit_signals(h, dates[d_]): early += 1; break
print(f'exit-signal parity on {checked} sampled stop/time exits: mismatches {bad}, early-fire cases {early}'); assert bad == 0 and early == 0
gt = tl[tl.Exit_Reason == 'MKT_GATE'].sample(40, random_state=2); bad2 = 0
for t_ in gt.itertuples():
    ix = dates.get_loc(pd.Timestamp(t_.Exit_Date)); h = {t_.Ticker: dict(entry_date=t_.Entry_Date, entry_price=t_.Entry_Price)}
    bad2 += A.get_exit_signals(h, dates[ix - 1]).get(t_.Ticker) not in ('MKT_GATE', 'STOP_ENTRY', 'STOP_TRAIL', 'TIME_STOP')
print(f'market-gate exit parity on {len(gt)} sampled gate exits: mismatches {bad2}'); assert bad2 == 0
# research switches: no crash, sane pools, sane stops/weights; presets; live helpers
for m in ('floor20', 'floor20_abs', 'amihud', 'continuity', 'cvvol', 'cs_spread', 'tradability', 'tradability_log'):
    Sx = mk(liq_mode=m); pools = [Sx.filter_universe(k).sum() for k in range(len(Sx.me)) if Sx.me[k] >= pd.Timestamp('2012-01-01')]
    assert min(pools) > 30 and max(pools) < 1000, (m, min(pools), max(pools))
print('liq_mode variants: pools sane for all 8 modes')
Sa = mk(atr_stops=True); sp = np.array([Sa.stop_pct(Sa.me_idx[k], j) for k in (100, 150, 200, 250) for j in range(0, len(Sa.cols), 40)]); wt = np.clip(0.01 / sp, 0.03, 0.08)
assert sp.min() >= 0.08 - 1e-12 and sp.max() <= 0.18 + 1e-12 and wt.min() >= 0.0555 and wt.max() <= 0.08 + 1e-12; print(f'atr_stops: stop {sp.min():.3f}-{sp.max():.3f}, weight {wt.min():.3f}-{wt.max():.3f}')
from csm_aegis_strategy import PRESETS
pv = CSMAegis.from_panels(P, **PRESETS['v1.2'], require_tradable_fill=False).calculate_factors()
rv = backtest_event_driven(pv, log_rejects=False)
assert float((rv['ret'] - res['ret']).abs().max()) < 1e-12
print('v1.2 preset reproduces legacy booking with zero idle-cash return')
assert A.get_positions(A.me[-1]).equals(A.latest_picks(A.me[-1])); print('get_positions == latest_picks')
print('ALL PARITY TESTS PASSED')

"""Event-study decay analysis for HR breakout and VCP (binary entry signals; no IC).  usage: python analyze_events.py hr|vcp"""
import sys, os, io, contextlib, time
import numpy as np, pandas as pd
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

which = sys.argv[1]
HZ = (5, 10, 20, 40, 60)
P = C.load_panels()
px, vol, hi, lo, op = P['close'], P['volume'], P['high'], P['low'], P['open']
quiet = io.StringIO()

with contextlib.redirect_stdout(quiet):
    if which == 'hr':
        from hr_breakout_v2 import HRBreakoutStrategy
        S = HRBreakoutStrategy(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op,
            universe_top_n=500, universe_min_n=1, min_price=10.0, max_circuit_days=5, prior_month_min_ret=-0.15,
            benchmark_sma_period=50, benchmark_streak_max=5, ema_fast=50, ema_mid=150, ema_slow=200, ema_slope_window=20,
            high_band_pct=0.75, rs_lookback=126, rs_top_pct=0.25, peak_wing=2, cluster_lookback=60, cluster_min_peaks=3,
            cluster_spread_pct=0.015, breakout_buffer=0.005, entry_gap_cancel_pct=0.03, momentum_rank_window=30,
            max_positions=10, warmup_days=252)
    else:
        from vcp_v4 import VCPBreakoutStrategy
        S = VCPBreakoutStrategy(prices_df=px, volumes_df=vol, highs_df=hi, lows_df=lo, opens_df=op,
            universe_top_n=1000, universe_min_n=500, min_price=10.0, max_circuit_days=5, ca_drop_thresh=0.40, ca_gain_thresh=3.00,
            bench_sma_period=50, bench_consec_days=5, sma_fast=50, sma_mid=150, sma_slow=200, sma_slope_lookback=20,
            high_52w_period=252, within_52w_high_pct=0.25, rs_period=252, rs_min_percentile=75, vcp_base_window=15,
            vcp_base_tight_pct=0.15, vcp_vol_contract_pct=0.80, vcp_vol_base_window=30, vcp_breakout_window=20,
            vcp_near_high_pct=0.10, max_positions=10, entry_gap_cancel_pct=0.03, warmup_days=252)
    S.calculate_factors()
    regime = S._compute_regime_flags()

prices = S._prices_ff
dates, cols = prices.index, prices.columns
n, m = prices.shape
opens_ff = S._opens_ff
prev_close = prices.shift(1)
entry_px = opens_ff.where(opens_ff.notna() & (opens_ff > 0), prev_close).values      # entry at bar-i open (prev-close fallback, runner convention)
gap = (opens_ff / prev_close - 1).values
close_v = prices.values
FW = {h: np.full((n, m), np.nan) for h in HZ}
for h in HZ:
    FW[h][:n - h] = close_v[h:] / entry_px[:n - h] - 1
for h in HZ:
    FW[h][~np.isfinite(FW[h])] = np.nan
    FW[h][np.abs(FW[h]) > 3.0] = np.nan                                             # bad-print guard

t0 = time.time()
ev_i, ev_j = [], []
elig_rows, univ_rows, sig_rows = {}, {}, {}
if which == 'hr':
    for i in range(S.warmup_days, n):
        if not bool(regime.iloc[i]):
            continue
        um = S._universe_mask_df.iloc[i]
        tm = S._trend_gate(i, um)
        el = (um & tm).values
        idx = np.flatnonzero(el)
        hits = []
        for j in idx:
            if gap[i, j] > S.entry_gap_cancel_pct:
                continue
            sig, _ = S._find_hr_signal(cols[j], i)
            if sig:
                hits.append(j)
        if hits:
            ev_i += [i] * len(hits); ev_j += hits
            elig_rows[i] = el; univ_rows[i] = um.values; sig_rows[i] = np.zeros(m, bool); sig_rows[i][hits] = True
        if i % 1000 == 0:
            print(which, i, n, round(time.time() - t0), 's', flush=True)
else:
    UM, TM, SG = S._universe_mask_matrix.values, S._trend_mask_matrix.values, S._vcp_signal_matrix.values
    reg = regime.values.astype(bool)
    for i in range(max(S.warmup_days, 1), n):
        if not reg[i]:
            continue
        el = UM[i - 1] & TM[i - 1]
        sg = el & SG[i - 1]
        sg = sg & ~(gap[i] > S.entry_gap_cancel_pct)
        if sg.any():
            hits = np.flatnonzero(sg)
            ev_i += [i] * len(hits); ev_j += list(hits)
            elig_rows[i] = el; univ_rows[i] = UM[i - 1]; sig_rows[i] = sg

ev = pd.DataFrame({'i': ev_i, 'j': ev_j}).sort_values(['j', 'i'])
# de-duplicate: one event per stock per 20 trading days
keep, last = [], {}
for i, j in zip(ev.i.values, ev.j.values):
    if j in last and i - last[j] < 20:
        keep.append(False)
    else:
        keep.append(True); last[j] = i
ev = ev[np.array(keep)].sort_values(['i', 'j']).reset_index(drop=True)
print(which, 'raw events', len(ev_i), 'dedup', len(ev), 'time', round(time.time() - t0), flush=True)

rows = []
cache = {}
for i, g in ev.groupby('i'):
    el, um, sg = elig_rows[i], univ_rows[i], sig_rows[i]
    peers = el & ~sg
    for h in HZ:
        cache[(i, h)] = (np.nanmean(np.where(um, FW[h][i], np.nan)) if um.any() else np.nan,
                         np.nanmean(np.where(peers, FW[h][i], np.nan)) if peers.any() else np.nan)
for i, j in zip(ev.i.values, ev.j.values):
    r = dict(date=dates[i], stock=cols[j], month=pd.Period(dates[i], 'M'))
    for h in HZ:
        f = FW[h][i, j]
        bm, bt = cache[(i, h)]
        r[f'raw{h}'] = f; r[f'xm{h}'] = f - bm; r[f'xt{h}'] = f - bt
    rows.append(r)
E = pd.DataFrame(rows)
E.to_pickle(f'{C.CACHE}/events_{which}.pkl')
print(which, 'events', len(E), E.date.min().date(), E.date.max().date())

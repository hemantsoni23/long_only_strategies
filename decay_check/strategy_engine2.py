"""strategy_engine2: v1.0 engine + the momentum-book overlays of Addendum 5 (all default OFF; with every flag off it equals strategy_engine.run bit-for-bit)."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C, strategy_engine as SE
_X = None
def extras():
    global _X
    if _X is None:
        D = SE.data(); P = C.load_panels(); close = P['close']; cf = close.ffill(limit=10); dates = D['dates']; me = D['me']
        bench = P['bench']; br = P['bench_ret']
        bvol21 = br.rolling(21).std().shift(1); thr = bvol21.expanding(min_periods=126).quantile(0.95)
        hi, lo = P['high'], P['low']; pc = cf.shift(1); tr = pd.concat([(hi - lo), (hi - pc).abs(), (lo - pc).abs()]).groupby(level=0).max()
        atr = tr.ewm(com=13, adjust=False, min_periods=14).mean().shift(1)
        ret = close.pct_change(fill_method=None)
        me_i = D['me_idx']; cm = D['close_me'].values.astype(float)
        prev_ret = np.full_like(cm, np.nan); prev_ret[2:] = cm[1:-1] / cm[:-2] - 1
        _X = dict(bench=bench.values, sma150=bench.rolling(150).mean().values, sma200=bench.rolling(200).mean().values, panic=(bvol21 > thr).fillna(False).values,
                  atr=atr.values, r121=D['S']['_r121'].reindex(D['per']).values.astype(float), prev_ret=prev_ret, vol21_me=ret.rolling(21, min_periods=15).std().loc[me].values)
    return _X
NEW = dict(crash_guard=False, cg_n=10, vol_target=None, regime_lev=False, lev_bear=0.6, lev_panic=0.5, mkt_gate=False, corr_guard=False, loss_cooldown=False, abs_mom=False, falling_knife=False,
           invvol=False, chandelier=False, minhold=False, quarterly=False, fill='open', mkt_win=150)
def _zs(x, m):
    v = np.where(m, x, np.nan); return (v - np.nanmean(v)) / (np.nanstd(v) + 1e-12)
def _sel(D, k, sel, elig, rng):
    if sel in ('R1A1', 'R1ULC'):
        per = D['per'][k]; S = D['S']; a = S['R1'].loc[per].values.astype(float); b = S['A1' if sel == 'R1A1' else 'ULC'].loc[per].values.astype(float)
        return np.where(elig, _zs(a, elig & np.isfinite(a)) + _zs(b, elig & np.isfinite(b)), np.nan)
    if sel == 'R3B':
        global _R3B
        if _R3B is None: _R3B = pickle.load(open(f'{C.CACHE}/r3b1000.pkl', 'rb'))['R3b']
        v = _R3B.reindex(D['per']).values.astype(float)[k]; return np.where(elig & np.isfinite(v), v, np.nan)
    return SE.selector_scores(D, k, sel, elig, rng)
_R3B = None
_SMA = {}
def _bench_sma(X, w):
    if w == 150: return X['sma150']
    if w not in _SMA: _SMA[w] = pd.Series(X['bench']).rolling(w).mean().values
    return _SMA[w]
def run(**kw):
    p = dict(SE.DEFAULT); p.update(NEW); p.update(kw); D = SE.data(); X = extras(); n = len(D['dates']); rng = np.random.default_rng(p['seed'])
    O, H, L, CL, RET, ADV = D['open'], D['high'], D['low'], D['close'], D['ret'], D['adv']; dates = D['dates']; cols = D['cols']
    sig_day = {i: k for k, i in enumerate(D['me_idx'])}; per = D['per']
    E = 1.0 if p['C0'] is None else float(p['C0']); pos = {}; pend_exit = {}; exit_due = {}; pend_entry = []; trades = []; rets = np.zeros(n); expo = np.zeros(n); turnover = 0.0
    start_i = dates.get_indexer([pd.Timestamp(p['start'])], method='bfill')[0]; dcash = (1 + p['cash_rate']) ** (1 / 252) - 1
    m = 1.0; last_upd = -99; cg_cool = 0; cg_pending = False; target_set = []; blocked = {}; overlays = any([p['vol_target'], p['regime_lev'], p['corr_guard']])
    mhist = np.ones(n)
    for i in range(1, n):
        e0 = E; pnl = 0.0; exited = []; mm = m
        for j, why in [(jj, w_) for jj, w_ in list(pend_exit.items()) if jj in pos and exit_due.get(jj, 0) <= i]:
            v, epx, ei, pk, edate, wrel = pos[j]
            fill = (CL[i, j] if p['fill'] == 'close' else (O[i, j] if np.isfinite(O[i, j]) and O[i, j] > 0 else CL[i - 1, j]))
            if not np.isfinite(fill): fill = CL[i - 1, j]
            r = fill / CL[i - 1, j] - 1 if ei != i else 0.0; r = float(np.clip(np.nan_to_num(r), -0.99, 5.0))
            pnl += mm * v * r; v2 = v * (1 + r); pnl -= mm * v2 * p['cost']; turnover += mm * v2 / e0
            pnlp = (fill / epx - 1) * 100
            trades.append(dict(j=j, entry=edate, entry_px=epx, exit=dates[i], exit_px=fill, reason=why, pnl_pct=pnlp, w_rel=wrel * mm)); exited.append(j)
            if p['loss_cooldown'] and why in ('STOP_ENTRY', 'STOP_TRAIL') and pnlp < 0:
                blocked[j] = dates[i] + pd.Timedelta(days=int(np.clip(20 * abs(pnlp) / 10.0, 10, 60)))
        for j in exited: del pos[j]; pend_exit.pop(j, None); exit_due.pop(j, None)
        panic_prev = bool(X['panic'][i - 1]) if p['crash_guard'] else False
        due_now = [x for x in pend_entry if x[2] <= i]; pend_entry = [x for x in pend_entry if x[2] > i]
        if due_now and not (p['crash_guard'] and (panic_prev or cg_cool > 0)):
            gross = sum(a[0] for a in pos.values()); want = []
            for j, w, _d in due_now:
                if j in pos: continue
                if p['loss_cooldown'] and blocked.get(j, pd.Timestamp(0)) > dates[i]: continue
                o = CL[i, j] if p['fill'] == 'close' else O[i, j]; pc = CL[i - 1, j]
                if not (np.isfinite(o) and o > 0 and np.isfinite(pc) and pc > 0): continue
                if p['fill'] != 'close' and o > pc * (1 + p['gap_cancel']): continue
                v = w * e0
                if p['adv_frac'] is not None and np.isfinite(ADV[i, j]): v = min(v, p['adv_frac'] * ADV[i, j] / max(mm, 1e-9))
                want.append((j, v, o))
            tot = sum(x[1] for x in want); room = max(0.0, e0 / max(mm, 1e-9) - gross); sc_ = min(1.0, room / tot) if tot > 0 else 0.0
            for j, v, o in want:
                v *= sc_
                if v <= 0: continue
                pos[j] = [v, o, i, o, dates[i], v / e0]; pnl -= mm * v * p['cost']; turnover += mm * v / e0
        gross = 0.0; stop_hits = []
        for j, a in pos.items():
            v, epx, ei, pk, ed, wrel = a
            r = CL[i, j] / epx - 1 if ei == i else RET[i, j]; r = float(np.clip(np.nan_to_num(r), -0.99, 5.0))
            if p['resting_stop'] and ei != i:
                lvl = max(epx * (1 - p['stop']), pk * (1 - p['trail']))
                if np.isfinite(L[i, j]) and L[i, j] <= lvl:
                    fill = O[i, j] if (np.isfinite(O[i, j]) and O[i, j] <= lvl) else lvl
                    r = float(np.clip(fill / CL[i - 1, j] - 1, -0.99, 5.0)); pnl += mm * v * r; v2 = v * (1 + r); pnl -= mm * v2 * p['cost']; turnover += mm * v2 / e0
                    trades.append(dict(j=j, entry=ed, entry_px=epx, exit=dates[i], exit_px=fill, reason='STOP_RESTING', pnl_pct=(fill / epx - 1) * 100, w_rel=wrel * mm)); stop_hits.append(j); continue
            pnl += mm * v * r; a[0] = v * (1 + r); gross += a[0]
            if np.isfinite(CL[i, j]): a[3] = max(a[3], CL[i, j])
        for j in stop_hits: del pos[j]
        pnl += max(0.0, e0 - mm * gross) * dcash; E = e0 + pnl; rets[i] = pnl / e0 if e0 else 0.0; expo[i] = mm * gross / E if E else 0.0; mhist[i] = mm
        # ---- after close
        for j, a in pos.items():
            if j in pend_exit: continue
            v, epx, ei, pk, ed, wrel = a; c = CL[i, j]
            if not np.isfinite(c): continue
            why = None; hold_ok = (not p['minhold']) or (i - ei >= 5)
            if not p['resting_stop'] and hold_ok:
                if c <= epx * (1 - p['stop']): why = 'STOP_ENTRY'
                else:
                    if p['chandelier']:
                        a14 = X['atr'][i, j]; d = np.clip(3.0 * a14 / a[3], 0.12, 0.30) if np.isfinite(a14) else 0.20
                        if c <= a[3] * (1 - d): why = 'STOP_TRAIL'
                    elif c <= a[3] * (1 - p['trail']): why = 'STOP_TRAIL'
            if why is None and p['timestop'] and (dates[i] - ed).days >= p['time_days'] and c / epx - 1 < p['time_loss']: why = 'TIME_STOP'
            if why: pend_exit[j] = why; exit_due[j] = i + 1 + p['delay']
        panic_i = bool(X['panic'][i])
        if p['crash_guard']:
            if panic_i:
                for j in pos:
                    if j not in pend_exit or pend_exit[j] != 'CRASH_GUARD': pend_exit[j] = 'CRASH_GUARD'; exit_due[j] = i + 1
                if pos: cg_pending = True
                cg_cool = p['cg_n']
            elif cg_cool > 0: cg_cool -= 1
            if cg_pending and not panic_i and cg_cool == 0 and i >= start_i:
                slots = p['top_n'] - len([j for j in pos if j not in pend_exit]); w0 = float(np.clip(0.01 / p['stop'], p['w_lo'], p['w_hi'])) if p['risk_size'] else p['w_eq']
                for j in target_set:
                    if slots <= 0: break
                    if j not in pos: pend_entry.append((int(j), w0, i + 1)); slots -= 1
                cg_pending = False
        # exposure multiplier for tomorrow
        if overlays and pos:
            lev = 1.0
            if p['regime_lev']:
                if p['crash_guard'] is False and False: pass
                lev = p['lev_panic'] if panic_i else (p['lev_bear'] if (np.isfinite(X['sma200'][i]) and X['bench'][i] < X['sma200'][i]) else 1.0)
                lev = min(lev, p['lev_panic'] if panic_i else 1.0)
            vs = 1.0; cs = 1.0
            if (p['vol_target'] or p['corr_guard']) and i >= 63:
                js = list(pos.keys()); wt = np.array([pos[j][0] for j in js]) / E
                if p['vol_target']:
                    pr = (RET[i - 62:i + 1][:, js] * wt).sum(axis=1); rv = pr.std() * np.sqrt(252)
                    if rv > 0: vs = min(1.0, p['vol_target'] / rv)
                if p['corr_guard']:
                    R21 = RET[i - 20:i + 1][:, js]; pv = (R21 * wt).sum(axis=1).std(); sv = (R21.std(axis=0) * wt).sum() / wt.sum()
                    if sv > 0 and pv / sv > 0.8: cs = 0.5
            tgt = lev * vs * cs
            if (i - last_upd >= 5) or abs(tgt - m) / max(m, 1e-9) > 0.05:
                if abs(tgt - m) > 1e-9:
                    gv = sum(a[0] for a in pos.values()); E -= p['cost'] * abs(tgt - m) * gv; turnover += abs(tgt - m) * gv / e0
                m = tgt; last_upd = i
        elif overlays and not pos: m = m  # keep
        # ---- month-end signal
        if i in sig_day and i >= start_i:
            k = sig_day[i]; elig, sc = (None, None)
            px = CL[i]; elig = np.isfinite(px) & (px >= p['min_price']) & (D['circ_me'].iloc[k].values <= 5)
            rk = D['dv_me'].iloc[k].rank(ascending=False, method='min').values; elig &= (rk >= p['band'][0]) & (rk <= p['band'][1])
            if p['trend_gate']: elig &= px > D['sma200_me'].iloc[k].values
            if p['abs_mom']: elig &= np.nan_to_num(X['r121'][k], nan=-1.0) > 0
            if p['falling_knife']: elig &= np.nan_to_num(X['prev_ret'][k], nan=0.0) >= -0.15
            if p['m3_excl']:
                m3 = D['S']['M3'].loc[per[k]].values.astype(float); ok = elig & np.isfinite(m3)
                if ok.sum() > 50: thr_ = np.nanquantile(m3[ok], p['m3_q']); elig &= ~(np.isfinite(m3) & (m3 < thr_))
            sc = _sel(D, k, p['sel'], elig, rng); sc = np.where(np.isfinite(sc) & elig, sc, np.nan); nvalid = int(np.isfinite(sc).sum())
            _sm = _bench_sma(X, p['mkt_win']); mkt_off = p['mkt_gate'] and np.isfinite(_sm[i]) and X['bench'][i] <= _sm[i]
            if mkt_off:
                for j in pos:
                    if j not in pend_exit: pend_exit[j] = 'MKT_GATE'; exit_due[j] = i + 1 + p['delay']
                target_set = []
            elif nvalid >= 30:
                order = np.argsort(-np.where(np.isfinite(sc), sc, -np.inf)); rank = np.full(len(cols), 10 ** 6); rank[order[:nvalid]] = np.arange(1, nvalid + 1)
                for j in list(pos.keys()):
                    if j not in pend_exit and (not np.isfinite(sc[j]) or rank[j] > p['hold_rank']): pend_exit[j] = 'RANK_EXIT'; exit_due[j] = i + 1 + p['delay']
                gate_block = p['volgate'] and bool(D['gate_me'].iloc[k]); slots = p['top_n'] - len([j for j in pos if j not in pend_exit])
                entries_ok = (not p['quarterly']) or (per[k].month in (1, 4, 7, 10))
                keep = [j for j in pos if j not in pend_exit]; new_sel = []
                if slots > 0 and not gate_block and entries_ok:
                    sma50 = D['sma50_me'].iloc[k].values
                    if p['invvol']:
                        v21 = X['vol21_me'][k]; medv = np.nanmedian(np.where(elig, v21, np.nan))
                    for j in order[:nvalid]:
                        if rank[j] > p['top_n']: break
                        if j in pos or slots <= 0: continue
                        if p['ext'] and np.isfinite(sma50[j]) and px[j] / sma50[j] - 1 > p['ext_x']: continue
                        if p['loss_cooldown'] and blocked.get(j, pd.Timestamp(0)) > dates[min(i + 1, n - 1)]: continue
                        if p['invvol']: w = float(np.clip(0.05 * medv / v21[j], p['w_lo'], p['w_hi'])) if np.isfinite(v21[j]) and v21[j] > 0 else 0.05
                        else: w = float(np.clip(0.01 / p['stop'], p['w_lo'], p['w_hi'])) if p['risk_size'] else p['w_eq']
                        pend_entry.append((int(j), w, i + 1 + p['delay'])); new_sel.append(int(j)); slots -= 1
                target_set = keep + new_sel
    for j, a in pos.items():
        trades.append(dict(j=j, entry=a[4], entry_px=a[1], exit=dates[-1], exit_px=CL[-1, j], reason='END_OF_PERIOD', pnl_pct=(CL[-1, j] / a[1] - 1) * 100, w_rel=a[5] * m))
    tl = pd.DataFrame(trades)
    if len(tl): tl['ticker'] = [cols[j] for j in tl.j]
    return dict(ret=pd.Series(rets, index=dates), expo=pd.Series(expo, index=dates), trades=tl, params=p, turnover=turnover, mult=pd.Series(mhist, index=dates))

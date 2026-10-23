"""Faithful daily engine for the new 'wrapper' strategy (signals from MOMENTUM_SIGNALS_EXPLAINED.md + lessons from breakouts).
Signal at month-end close -> trade next open. Close-based stops -> exit next open (executable). Positions drift. Entry day open->close, exit day prev-close->fill charged."""
import os, sys, pickle
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C
_D = None
def data():
    global _D
    if _D is None:
        P = C.load_panels(); S = pickle.load(open(f'{C.CACHE}/signals_all.pkl', 'rb'))
        close = P['close']; cf = close.ffill(limit=10)
        me = C.month_end_days(close.index); me = me[me >= pd.Timestamp('2004-06-01')]
        sma200 = cf.rolling(200, min_periods=150).mean(); sma50 = cf.rolling(50, min_periods=40).mean()
        circ = (P['high'] == P['low']).rolling(63, min_periods=1).sum()
        dv = (close * P['volume']).rolling(63, min_periods=45).mean(); adv = (close * P['volume']).rolling(63, min_periods=21).median()
        bvol = P['bench_ret'].rolling(63).std(); thr = bvol.expanding(min_periods=1260).quantile(0.85)
        def at(df): x = df.loc[me]; return x
        _D = dict(dates=close.index, cols=list(close.columns), open=P['open'].values, high=P['high'].values, low=P['low'].values, close=cf.values,
                  ret=close.pct_change(fill_method=None).fillna(0.0).values, adv=adv.shift(1).values, me=me,
                  me_idx=[close.index.get_loc(d) for d in me], sma200_me=at(sma200), sma50_me=at(sma50), close_me=at(cf), circ_me=at(circ), dv_me=at(dv.shift(1)),
                  gate_me=(bvol > thr).loc[me], S=S, bench_ret=P['bench_ret'])
        # monthly signals indexed by Period -> map to me dates
        D = _D; per = pd.PeriodIndex(me, freq='M'); D['per'] = per
    return _D
def zs(x):
    return (x - np.nanmean(x)) / (np.nanstd(x) + 1e-12)
def selector_scores(D, k, sel, mask, rng=None):
    """mask: boolean array of eligible names. returns score array (NaN outside)."""
    per = D['per'][k]; S = D['S']
    def g(n): return S[n].loc[per].values.astype(float)
    if sel == 'R1': sc = g('R1')
    elif sel == 'BASE': sc = g('BASE')
    elif sel == 'ELEN': sc = None
    if sel in ('ELEN', 'ZEN'):
        parts = [g('A3'), g('Q5')] if sel == 'ELEN' else [g('A1'), g('Q5')]
        sc = sum(zs(np.where(mask, p, np.nan)) for p in parts)
    if sel == 'random': sc = rng.random(len(mask))
    return np.where(mask, sc, np.nan)
DEFAULT = dict(sel='R1', top_n=20, hold_rank=40, stop=0.15, trail=0.20, time_days=45, time_loss=-0.05, ext=True, ext_x=0.25, volgate=True, timestop=True,
               risk_size=True, w_lo=0.03, w_hi=0.08, w_eq=0.05, trend_gate=True, m3_excl=True, m3_q=0.20, cost=0.003, resting_stop=False, min_price=20.0,
               band=(1, 1000), adv_frac=None, C0=None, cash_rate=0.0, gap_cancel=0.03, start='2005-01-01', seed=0, delay=0)
def run(**kw):
    p = dict(DEFAULT); p.update(kw); D = data(); n = len(D['dates']); rng = np.random.default_rng(p['seed'])
    O, H, L, CL, RET, ADV = D['open'], D['high'], D['low'], D['close'], D['ret'], D['adv']; dates = D['dates']
    sig_day = {i: k for k, i in enumerate(D['me_idx'])}
    E = 1.0 if p['C0'] is None else float(p['C0']); pos = {}; pend_exit = {}; exit_due = {}; pend_entry = []; trades = []; rets = np.zeros(n); expo = np.zeros(n); turnover = 0.0; picks = {}
    start_i = dates.get_indexer([pd.Timestamp(p['start'])], method='bfill')[0]
    dcash = (1 + p['cash_rate']) ** (1 / 252) - 1
    for i in range(1, n):
        e0 = E; pnl = 0.0
        # 1) open: exits then entries
        exited = []
        for j, why in [(jj, w_) for jj, w_ in list(pend_exit.items()) if (jj in pos and pos[jj][2] + 0 <= i and exit_due.get(jj, 0) <= i)]:
            if j not in pos: continue
            v, epx, ei, pk, edate, wrel = pos[j]
            fill = O[i, j] if np.isfinite(O[i, j]) and O[i, j] > 0 else CL[i - 1, j]
            r = fill / CL[i - 1, j] - 1 if ei != i else 0.0
            r = float(np.clip(np.nan_to_num(r), -0.99, 5.0)); pnl += v * r; v2 = v * (1 + r); pnl -= v2 * p['cost']; turnover += v2 / e0
            trades.append(dict(j=j, entry=edate, entry_px=epx, exit=dates[i], exit_px=fill, reason=why, pnl_pct=(fill / epx - 1) * 100, w_rel=wrel)); exited.append(j)
        for j in exited: del pos[j]; pend_exit.pop(j, None); exit_due.pop(j, None)
        due_now = [x for x in pend_entry if x[2] <= i]; pend_entry = [x for x in pend_entry if x[2] > i]
        if due_now:
            gross = sum(a[0] for a in pos.values()); want = []
            for j, w, _d in due_now:
                if j in pos: continue
                o = O[i, j]; pc = CL[i - 1, j]
                if not (np.isfinite(o) and o > 0 and np.isfinite(pc) and pc > 0): continue
                if o > pc * (1 + p['gap_cancel']): continue
                v = w * e0
                if p['adv_frac'] is not None and np.isfinite(ADV[i, j]): v = min(v, p['adv_frac'] * ADV[i, j])
                want.append((j, v, o))
            tot = sum(x[1] for x in want); room = max(0.0, e0 - gross); sc = min(1.0, room / tot) if tot > 0 else 0.0
            for j, v, o in want:
                v *= sc
                if v <= 0: continue
                pos[j] = [v, o, i, o, dates[i], v / e0]; pnl -= v * p['cost']; turnover += v / e0
        # 2) daily P&L (positions that survived open) and cash
        gross = 0.0; stop_hits = []
        for j, a in pos.items():
            v, epx, ei, pk, ed, wrel = a
            if ei == i: r = CL[i, j] / epx - 1
            else: r = RET[i, j]
            r = float(np.clip(np.nan_to_num(r), -0.99, 5.0))
            if p['resting_stop'] and ei != i:
                lvl = max(epx * (1 - p['stop']), pk * (1 - p['trail']))
                if np.isfinite(L[i, j]) and L[i, j] <= lvl:
                    fill = O[i, j] if (np.isfinite(O[i, j]) and O[i, j] <= lvl) else lvl
                    r = fill / CL[i - 1, j] - 1; r = float(np.clip(r, -0.99, 5.0)); pnl += v * r; v2 = v * (1 + r); pnl -= v2 * p['cost']; turnover += v2 / e0
                    trades.append(dict(j=j, entry=ed, entry_px=epx, exit=dates[i], exit_px=fill, reason='STOP_RESTING', pnl_pct=(fill / epx - 1) * 100, w_rel=wrel)); stop_hits.append(j); continue
            pnl += v * r; a[0] = v * (1 + r); gross += a[0]
            if np.isfinite(CL[i, j]): a[3] = max(a[3], CL[i, j])
        for j in stop_hits: del pos[j]
        cash_w = max(0.0, e0 - gross); pnl += cash_w * dcash
        E = e0 + pnl; rets[i] = pnl / e0 if e0 else 0.0; expo[i] = gross / E if E else 0.0
        # 3) after close: stop checks -> pending exits (next open)
        if not p['resting_stop']:
            for j, a in pos.items():
                if j in pend_exit: continue
                v, epx, ei, pk, ed, wrel = a; c = CL[i, j]
                if not np.isfinite(c): continue
                if c <= epx * (1 - p['stop']): pend_exit[j] = 'STOP_ENTRY'; exit_due[j] = i + 1 + p['delay']
                elif c <= a[3] * (1 - p['trail']): pend_exit[j] = 'STOP_TRAIL'; exit_due[j] = i + 1 + p['delay']
                elif p['timestop'] and (dates[i] - ed).days >= p['time_days'] and c / epx - 1 < p['time_loss']: pend_exit[j] = 'TIME_STOP'; exit_due[j] = i + 1 + p['delay']
        else:
            for j, a in pos.items():
                if j in pend_exit: continue
                if p['timestop'] and (dates[i] - a[4]).days >= p['time_days'] and CL[i, j] / a[1] - 1 < p['time_loss']: pend_exit[j] = 'TIME_STOP'; exit_due[j] = i + 1 + p['delay']
        # 4) month-end signal
        if i in sig_day and i >= start_i:
            k = sig_day[i]; cols = len(D['cols'])
            c = D['close_me'].iloc[k].values if 'close_me' in D else CL[i]
            px = CL[i]; elig = np.isfinite(px) & (px >= p['min_price']) & (D['circ_me'].iloc[k].values <= 5)
            dvr = D['dv_me'].iloc[k]; rk = dvr.rank(ascending=False, method='min').values
            elig &= (rk >= p['band'][0]) & (rk <= p['band'][1])
            if p['trend_gate']: elig &= px > D['sma200_me'].iloc[k].values
            if p['m3_excl']:
                m3 = D['S']['M3'].loc[D['per'][k]].values.astype(float); ok = elig & np.isfinite(m3)
                if ok.sum() > 50: thr = np.nanquantile(m3[ok], p['m3_q']); elig &= ~(np.isfinite(m3) & (m3 < thr))
            sc = selector_scores(D, k, p['sel'], elig, rng)
            nvalid = np.isfinite(sc).sum()
            if nvalid >= 30:
                order = np.argsort(-np.where(np.isfinite(sc), sc, -np.inf)); rank = np.full(cols, 10 ** 6); rank[order[:nvalid]] = np.arange(1, nvalid + 1); picks[D['per'][k]] = [D['cols'][jj] for jj in order[:20]]
                for j in list(pos.keys()):
                    if j not in pend_exit and (not np.isfinite(sc[j]) or rank[j] > p['hold_rank']): pend_exit[j] = 'RANK_EXIT'; exit_due[j] = i + 1 + p['delay']
                gate_block = p['volgate'] and bool(D['gate_me'].iloc[k])
                held_after = [j for j in pos if j not in pend_exit]; slots = p['top_n'] - len(held_after)
                if slots > 0 and not gate_block:
                    sma50 = D['sma50_me'].iloc[k].values
                    for j in order[:nvalid]:
                        if rank[j] > p['top_n']: break
                        if j in pos or slots <= 0: continue
                        if p['ext'] and np.isfinite(sma50[j]) and px[j] / sma50[j] - 1 > p['ext_x']: continue
                        w = float(np.clip(0.01 / p['stop'], p['w_lo'], p['w_hi'])) if p['risk_size'] else p['w_eq']
                        pend_entry.append((int(j), w, i + 1 + p['delay'])); slots -= 1
    # close all at end
    for j, a in pos.items():
        trades.append(dict(j=j, entry=a[4], entry_px=a[1], exit=dates[-1], exit_px=CL[-1, j], reason='END_OF_PERIOD', pnl_pct=(CL[-1, j] / a[1] - 1) * 100, w_rel=a[5]))
    r = pd.Series(rets, index=dates); tl = pd.DataFrame(trades)
    if len(tl): tl['ticker'] = [D['cols'][j] for j in tl.j]
    return dict(ret=r, expo=pd.Series(expo, index=dates), trades=tl, params=p, turnover=turnover, picks=picks)

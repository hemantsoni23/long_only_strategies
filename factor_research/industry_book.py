"""
industry_book.py -- FAITHFUL simulator for a slow, staggered, industry-led long-only book (see INDUSTRY_BOOK_PREREG.md).

Accounting (deliberately not the Elendel engine's booking, which csm_value/AUDIT.md shows inflates CAGR by 17-26 points):
  * signal at the CLOSE of month-end t (information <= t), orders filled at the CLOSE of the next trading day b = t+1
  * a position earns returns only from the day AFTER its fill (b+1 ...) -- no overnight-gap credit
  * costs = side_cost x sum|target - drifted weight| charged on the fill day; no stops (primary spec)
  * names that are NaN or circuit-locked (high == low) on the fill day cannot be bought (that weight stays in cash)
  * idle cash earns `cash_rate` per year (daily compounded, 252); set cash_rate=0 for the engine-comparable convention
  * daily returns use the project's cleaned-return convention (evaluate.forward_returns): closes ffilled, daily moves outside
    (-40%, +300%) counted as 0, delisted names stay flat at the last price

Selection (per month-end t): rank usable Industry_clean baskets (>=10 live U1 members, trailing L-month EW return > 0) by return,
take the top n_ind, buy the top m pool members of each by a stock score (A1 by default). Overlapping tranches: the target is the
mean of the last H monthly cohorts (Jegadeesh-Titman), scaled by a market-regime gate (EW index above its SMA200 -> 1.0, else gate_low).
"""
import os
import pickle
import sys
from dataclasses import dataclass, replace

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from industry_lib import IndustryEngine, basket_returns, onehot, trailing, permute_within  # noqa: E402


@dataclass(frozen=True)
class Spec:
    L: int = 3
    skip: int = 0
    n_ind: int = 8
    m: int = 2
    H: int = 6
    min_members: int = 10
    require_pos: bool = True
    score: str = 'a1'              # 'a1' | 'lowvol' | 'rand'
    pool: str = 'U2_live_trend'    # key in U / extra universes
    gate: bool = True
    gate_low: float = 0.5
    weighting: str = 'eq'          # basket weighting for the industry rank
    side_cost: float = 0.003
    cash_rate: float = 0.065
    start: str = '2005-01-01'
    mode: str = 'real'             # 'real' | 'rand_ind' | 'rand_stock' | 'ew_pool' | 'topn'
    vol_target: float = 0.0        # 0 = off; else annual vol target of the WHOLE book (de-leverage only), chassis-style overlay
    vol_win: int = 63              # trailing window (days) for the overlay's realised vol, lagged one day


class BookData:
    def __init__(self, X, sig, U, UN, F):
        self.X, self.sig, self.F = X, sig, F
        self.cols = X.C.columns
        self.dates = X.C.index
        Cff = X.C.ffill()
        r = Cff.pct_change(fill_method=None)
        self.R = r.where((r > -0.40) & (r < 3.00), 0.0).fillna(0.0).values.astype(np.float32)
        pos = self.dates.get_indexer(sig)
        ok = (pos >= 0) & (pos + 1 < len(self.dates))
        self.pos = pos
        self.b = np.where(ok, pos + 1, -1)
        Cv, Hv, Lv = X.C.values, X.H.values, X.L.values
        T, N = len(sig), len(self.cols)
        self.tradable = np.zeros((T, N), dtype=bool)
        for k in range(T):
            if self.b[k] >= 0:
                bb = self.b[k]
                self.tradable[k] = np.isfinite(Cv[bb]) & ~((Hv[bb] == Lv[bb]) & np.isfinite(Hv[bb]))
        bench = X.bench
        sma = bench.rolling(200, min_periods=150).mean()
        up = (bench > sma).reindex(self.dates).values
        self.gate_up = np.array([bool(up[p]) if p >= 0 and np.isfinite(sma.values[p]) else True for p in pos])
        self.U1 = U['U1_liquid1000']
        self.pools = {**{k: v for k, v in U.items()}, **UN}
        self.eng = IndustryEngine(X, sig, self.U1)
        e = self.eng
        self.n_ind, self.n_sec = e.n_ind, e.n_sec
        self.cnt_now = self.U1.reindex(sig).fillna(False).values.astype('float64') @ onehot(e.ind_code, e.n_ind)
        from evaluate import composite
        pool_u = U['U2_live_trend']
        self.score_frames = {'a1': F['a1_52wh'].reindex(sig).values, 'lowvol': F['lowvol_126'].reindex(sig).values,
                             'q5': F['q5_126'].reindex(sig).values,
                             'zen': composite(F, ['a1_52wh', 'q5_189'], pool_u).reindex(sig).values,
                             'elen': composite(F, ['a3_rs_high', 'q5_126'], pool_u).reindex(sig).values}
        self.G_cache = {}

    def group_trailing(self, L, skip, weighting='eq', ind_code=None):
        key = (L, skip, weighting, None if ind_code is None else hash(ind_code.tobytes()))
        if key not in self.G_cache:
            e = self.eng
            code = e.ind_code if ind_code is None else ind_code
            w = e.dv if weighting == 'dv' else None
            ret, cnt = basket_returns(code, e.n_ind, e.mret, e.elig_prev, w)
            self.G_cache[key] = (trailing(ret, L, skip), cnt)
        return self.G_cache[key]


def build_cohorts(bd, sp, rng=None, ind_code=None):
    """-> C (T x N) nominal weights per monthly cohort, and a log of selected industries per month."""
    e = bd.eng
    code = e.ind_code if ind_code is None else ind_code
    T, N = len(bd.sig), len(bd.cols)
    G, _ = bd.group_trailing(sp.L, sp.skip, sp.weighting, ind_code)
    cnt_now = bd.cnt_now if ind_code is None else bd.U1.reindex(bd.sig).fillna(False).values.astype('float64') @ onehot(code, bd.n_ind)
    ok = cnt_now >= sp.min_members
    pool = bd.pools[sp.pool].reindex(bd.sig).fillna(False).values
    C = np.zeros((T, N), dtype=np.float32)
    sel_log = [None] * T
    start_ts = pd.Timestamp(sp.start)
    rng = rng if rng is not None else np.random.default_rng(0)
    sc = bd.score_frames.get(sp.score)
    members_by_g = {g: np.where(code == g)[0] for g in range(bd.n_ind)}
    for k in range(T):
        if bd.b[k] < 0 or bd.sig[k] < start_ts:
            continue
        pool_k = pool[k] & bd.tradable[k]
        if sp.mode == 'ew_pool':
            idx = np.where(pool_k)[0]
            if len(idx):
                C[k, idx] = 1.0 / len(idx)
            continue
        if sp.mode == 'topn':
            idx = np.where(pool_k)[0]
            n_take = sp.n_ind * sp.m
            v = np.nan_to_num(sc[k, idx], nan=-np.inf)
            if len(idx) >= n_take:
                C[k, idx[np.argsort(-v, kind='stable')[:n_take]]] = 1.0 / n_take
            continue
        if sp.mode == 'rand_stock':
            idx = np.where(pool_k & (code >= 0))[0]
            n_take = sp.n_ind * sp.m
            if len(idx) >= n_take:
                C[k, rng.choice(idx, n_take, replace=False)] = 1.0 / n_take
            continue
        Gk = G[k, :bd.n_ind]
        usable = ok[k] & np.isfinite(Gk)
        if sp.require_pos:
            usable &= Gk > 0
        cand = np.where(usable)[0]
        if len(cand) == 0:
            continue
        if sp.mode == 'rand_ind':
            sel = rng.choice(cand, min(sp.n_ind, len(cand)), replace=False)
        else:
            sel = cand[np.argsort(-Gk[cand], kind='stable')[:sp.n_ind]]
        sel_log[k] = sel
        w = 1.0 / (sp.n_ind * sp.m)
        for g in sel:
            mem = members_by_g[g]
            mem = mem[pool_k[mem]]
            if len(mem) == 0:
                continue
            if sp.score == 'rand':
                pick = rng.permutation(mem)[:sp.m]
            else:
                s = np.nan_to_num(sc[k, mem], nan=-np.inf)
                pick = mem[np.argsort(-s, kind='stable')[:sp.m]]
            C[k, pick] += w
    return C, sel_log


def simulate(bd, C, sp, track_episodes=False):
    """Faithful daily simulation. Returns dict(ret=Series of daily net returns, turnover, exposure, episodes)."""
    T, N = C.shape
    H = 1 if sp.mode == 'ew_pool' else sp.H
    cum = np.cumsum(C.astype('float64'), axis=0)
    prev = np.vstack([np.zeros((H, N)), cum[:T - H]]) if H < T else np.zeros_like(cum)
    target = (cum - prev) / H
    gate = np.where(bd.gate_up, 1.0, sp.gate_low) if sp.gate else np.ones(T)
    target = target * gate[:, None]
    nd = len(bd.dates)
    rf_d = (1 + sp.cash_rate) ** (1 / 252) - 1
    has = np.where((target > 0).any(axis=1) & (bd.b >= 0))[0]
    if len(has) == 0:
        return None
    k_first = int(has[0])
    daily = np.zeros(nd)
    w = np.zeros(N)
    cash = 1.0
    E = 1.0
    turn_log, expo_log, names_log, dates_log = [], [], [], []
    episodes = []
    active_ep = {}
    for idx, k in enumerate(range(k_first, T)):
        b0 = bd.b[k]
        if b0 < 0:
            break
        tgt = target[k]
        d = np.abs(tgt - w)
        turnover = d.sum()
        cost = sp.side_cost * turnover
        daily[b0] = (1.0 + daily[b0]) * (1.0 - cost) - 1.0 if daily[b0] != 0 else -cost
        E_start = E * (1.0 - cost)
        if track_episodes:
            for i in np.where((tgt > 0) & (w <= 0))[0]:
                active_ep[i] = [bd.dates[b0], 0.0]
            for i in np.where((tgt <= 0) & (w > 0))[0]:
                if i in active_ep:
                    s, c = active_ep.pop(i)
                    episodes.append((bd.cols[i], s, bd.dates[b0], c))
        w = tgt.copy()
        cash = 1.0 - w.sum()
        nxt = bd.b[k + 1] if k + 1 < T and bd.b[k + 1] >= 0 else nd - 1
        a = np.where(w > 0)[0]
        days = np.arange(b0 + 1, nxt + 1)
        if len(days) > 0:
            Rseg = bd.R[b0 + 1:nxt + 1][:, a].astype('float64')
            growth = np.cumprod(1.0 + Rseg, axis=0)
            vals = growth * w[a]
            cashv = cash * (1 + rf_d) ** np.arange(1, len(days) + 1)
            total = vals.sum(axis=1) + cashv
            prev_tot = np.concatenate([[1.0], total[:-1]])
            daily[days] = total / prev_tot - 1.0
            if track_episodes:
                dv = np.diff(np.vstack([w[a], vals]), axis=0)
                for j, i in enumerate(a):
                    if i in active_ep:
                        active_ep[i][1] += float(dv[:, j].sum()) * E_start
            w_new = np.zeros(N)
            w_new[a] = vals[-1] / total[-1]
            cash = cashv[-1] / total[-1]
            w = w_new
            E = E_start * total[-1]
        else:
            E = E_start
        turn_log.append(turnover / 2.0)
        expo_log.append(w.sum())
        names_log.append(int((w > 1e-9).sum()))
        dates_log.append(bd.dates[b0])
    if track_episodes:
        for i, (s, c) in active_ep.items():
            episodes.append((bd.cols[i], s, bd.dates[-1], c))
    first_day = bd.b[k_first]
    ret = pd.Series(daily[first_day:], index=bd.dates[first_day:])
    info = pd.DataFrame({'turnover_oneway': turn_log, 'exposure': expo_log, 'names': names_log}, index=pd.DatetimeIndex(dates_log))
    return dict(ret=ret, info=info, episodes=episodes, k_first=k_first)


def metrics(r, rf=0.0, periods=252):
    r = r.dropna()
    if len(r) < 60:
        return {}
    eq = (1 + r).cumprod()
    yrs = len(r) / periods
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = r.std() * np.sqrt(periods)
    rfd = (1 + rf) ** (1 / periods) - 1
    sharpe = (r - rfd).mean() / r.std() * np.sqrt(periods) if r.std() > 0 else np.nan
    dn = r[r < rfd]
    sortino = (r - rfd).mean() / dn.std() * np.sqrt(periods) if len(dn) > 5 and dn.std() > 0 else np.nan
    dd = eq / eq.cummax() - 1
    return dict(cagr=cagr, vol=vol, sharpe=sharpe, sortino=sortino, maxdd=dd.min(), calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan, years=yrs)


def window(r, a=None, b=None):
    out = r
    if a is not None:
        out = out[out.index >= pd.Timestamp(a)]
    if b is not None:
        out = out[out.index <= pd.Timestamp(b)]
    return out


def vol_overlay(r, sp):
    """Pre-set chassis-style overlay: scale the whole book by min(1, target / trailing realised vol), vol lagged one day; the
    remainder sits in cash at sp.cash_rate; cost = side_cost x |change in scale| (proportional whole-book trade)."""
    vol = r.rolling(sp.vol_win, min_periods=40).std().shift(1) * np.sqrt(252)
    s = (sp.vol_target / vol).clip(upper=1.0).fillna(1.0)
    rf = (1 + sp.cash_rate) ** (1 / 252) - 1
    return s * r + (1 - s) * rf - sp.side_cost * s.diff().abs().fillna(0), s


def run(bd, sp, rng=None, ind_code=None, track_episodes=False):
    C, sel = build_cohorts(bd, sp, rng=rng, ind_code=ind_code)
    res = simulate(bd, C, sp, track_episodes)
    if res is not None:
        res['sel'] = sel
        res['C'] = C
        if sp.vol_target > 0:
            res['ret_raw'] = res['ret']
            res['ret'], res['scale'] = vol_overlay(res['ret'], sp)
    return res


def load_book_data():
    from data import load_panels
    from factors import Ctx
    st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
    UN = pickle.load(open(os.path.join(HERE, '.cache', 'extra_universes.pkl'), 'rb'))
    X = Ctx(load_panels())
    return BookData(X, st['sig'], st['U'], UN, st['F'])


if __name__ == '__main__':
    import time
    t0 = time.time()
    bd = load_book_data()
    print('data ready %.1fs' % (time.time() - t0))
    sp = Spec()
    t1 = time.time()
    res = run(bd, sp)
    print('D1 run %.1fs' % (time.time() - t1))
    r = res['ret']
    full_start = r.index[0] + pd.DateOffset(months=sp.H)
    for lbl, rr in (('all', r), ('fully built', window(r, full_start))):
        m0, m6 = metrics(rr, 0.0), metrics(rr, 0.06)
        print(f"{lbl:<12} {rr.index[0].date()}..{rr.index[-1].date()}  CAGR {m0['cagr']*100:5.1f}%  vol {m0['vol']*100:4.1f}%  Sharpe(rf0) {m0['sharpe']:.2f}  Sharpe(rf6) {m6['sharpe']:.2f}  "
              f"MaxDD {m0['maxdd']*100:6.1f}%  Calmar {m0['calmar']:.2f}")
    info = res['info']
    print('avg exposure %.2f | avg names %.0f | avg one-way turnover/month %.1f%% (%.0f%%/yr)' % (info.exposure.mean(), info.names.mean(), info.turnover_oneway.mean() * 100, info.turnover_oneway.mean() * 1200))

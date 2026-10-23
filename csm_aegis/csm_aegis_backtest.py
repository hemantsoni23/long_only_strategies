"""
csm_aegis_backtest.py
=====================
Event-driven FAITHFUL backtest engine and command-line runner for CSM Aegis.
All decisions are taken by the strategy object (csm_aegis_strategy.CSMAegis); this file books the P&L, produces diagnostics and exposes the runnable interface.

Execution model (identical for every version; see decay_check/PREREG.md Addenda 4-7)
  * Signals are computed at a month-end close; stop / time-stop triggers at any close.
  * fill='close' (default): the order is filled at the NEXT close. fill='open': at the next open (the data's open is biased; kept only to reproduce v1.0/v1.1).
  * Faithful booking: positions drift after entry; the entry-day return is fill->close; the exit-day return is prev-close->fill and IS charged.
  * Cost: transaction_cost on the notional of every entry and every exit. Idle cash earns zero. Gross exposure is capped at max_gross of equity.
  * Optional exposure multiplier (vol targeting / regime leverage / corr guard) scales all positions; changes are charged at the same cost.
"""
import argparse
import ast
import os
import sys
import warnings
import numpy as np
import pandas as pd

from csm_aegis_strategy import CSMAegis, Holding, PRESETS, load_data

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")


# ══════════════════════════════════════════════════════════════════════════════
# ENGINE
# ══════════════════════════════════════════════════════════════════════════════
def backtest_event_driven(S, log_rejects=True):
    """Run the strategy over its whole history. Returns a results dict and attaches logs to S:
    S.position_metadata (closed trades), S.reject_log, S.daily_log, S.picks_by_month."""
    if not S._ready:
        S.calculate_factors()
    dates, cols, O, CL, RET, ADV = S.dates, S.cols, S.O, S.CL, S.RET, S.ADV
    n = len(dates)
    rng = np.random.default_rng(S.placebo_seed) if S.placebo_seed is not None else None
    sig_day = {i: k for k, i in enumerate(S.me_idx)}
    start_i = dates.get_indexer([pd.Timestamp(S.start)], method="bfill")[0]
    cost, dcash, delay = S.transaction_cost, 0.0, S.execution_delay
    E = float(S.initial_capital)
    pos, pend_exit, exit_due, pend_entry = {}, {}, {}, []          # j -> Holding ; j -> reason ; j -> due idx ; [(j, weight, due, meta)]
    blocked, target_set = {}, []
    trades, rejects, daily, picks = [], [], [], {}
    rets, expo, mhist = np.zeros(n), np.zeros(n), np.ones(n)
    turnover, m, last_upd, cg_cool, cg_pending = 0.0, 1.0, -99, 0, False
    close_fill = S.fill == "close"

    def reject(date, reason, j):
        if log_rejects:
            rejects.append(dict(Date=date, Ticker=cols[j], Reason=reason))

    def record(j, h, i, fill, why, mm):
        pnl_pct = (fill / h.entry_px - 1) * 100
        trades.append(dict(
            j=j, Ticker=cols[j], Entry_Date=h.entry_date, Entry_Price=h.entry_px, Exit_Date=dates[i], Exit_Price=fill, Exit_Reason=why, PnL_Pct=pnl_pct,
            Holding_Days=(dates[i] - h.entry_date).days, Weight_At_Entry=h.w_rel * mm, Signal_Date=h.signal_date, Rank_At_Entry=h.rank_at_entry,
            Score_At_Entry=h.score_at_entry, Regime_At_Entry=h.regime, MAE_Pct=(h.min_close / h.entry_px - 1) * 100, MFE_Pct=(h.max_close / h.entry_px - 1) * 100))
        if S.loss_cooldown and why in ("STOP_ENTRY", "STOP_TRAIL") and pnl_pct < 0:
            blocked[j] = dates[i] + pd.Timedelta(days=int(np.clip(20 * abs(pnl_pct) / 10.0, 10, 60)))

    for i in range(1, n):
        e0, pnl, mm = E, 0.0, m
        # ── 1. exits that fall due at today's fill ───────────────────────────────
        done = []
        for j, why in [(jj, w_) for jj, w_ in list(pend_exit.items()) if jj in pos and exit_due.get(jj, 0) <= i]:
            h = pos[j]
            fill = CL[i, j] if close_fill else (O[i, j] if np.isfinite(O[i, j]) and O[i, j] > 0 else CL[i - 1, j])
            if not np.isfinite(fill):
                fill = CL[i - 1, j]
            r = float(np.clip(np.nan_to_num(fill / CL[i - 1, j] - 1 if h.entry_idx != i else 0.0), -0.99, 5.0))
            pnl += mm * h.v * r
            v2 = h.v * (1 + r)
            pnl -= mm * v2 * cost
            turnover += mm * v2 / e0
            record(j, h, i, fill, why, mm)
            done.append(j)
        for j in done:
            del pos[j]; pend_exit.pop(j, None); exit_due.pop(j, None)

        # ── 2. entries that fall due ──────────────────────────────────────────────
        panic_prev = bool(S.panic[i - 1]) if S.crash_guard else False
        due_now = [x for x in pend_entry if x[2] <= i]
        pend_entry = [x for x in pend_entry if x[2] > i]
        if due_now and S.crash_guard and (panic_prev or cg_cool > 0):
            for j, w, _d, meta in due_now:
                reject(dates[i], "CRASH_GUARD", j)
        elif due_now:
            gross, want = sum(h.v for h in pos.values()), []
            for j, w, _d, meta in due_now:
                if j in pos:
                    continue
                if S.loss_cooldown and blocked.get(j, pd.Timestamp(0)) > dates[i]:
                    reject(dates[i], "COOLDOWN", j); continue
                o = CL[i, j] if close_fill else O[i, j]
                pc = CL[i - 1, j]
                if not (np.isfinite(o) and o > 0 and np.isfinite(pc) and pc > 0):
                    reject(dates[i], "NO_PRICE", j); continue
                if not close_fill and o > pc * (1 + S.gap_cancel):
                    reject(dates[i], "GAP_CANCEL", j); continue
                v = w * e0
                if S.adv_fraction is not None and np.isfinite(ADV[i, j]):
                    v = min(v, S.adv_fraction * ADV[i, j] / max(mm, 1e-9))
                want.append((j, v, o, meta))
            tot = sum(x[1] for x in want)
            room = max(0.0, S.max_gross * e0 / max(mm, 1e-9) - gross)
            sc_ = min(1.0, room / tot) if tot > 0 else 0.0
            for j, v, o, meta in want:
                if sc_ < 1.0:
                    reject(dates[i], "GROSS_CAP_SCALED", j)
                v *= sc_
                if v <= 0:
                    continue
                pos[j] = Holding(v, o, i, dates[i], v / e0, *meta)
                pnl -= mm * v * cost
                turnover += mm * v / e0

        # ── 3. daily P&L of everything held ──────────────────────────────────────
        gross, stop_hits = 0.0, []
        for j, h in pos.items():
            r = float(np.clip(np.nan_to_num(CL[i, j] / h.entry_px - 1 if h.entry_idx == i else RET[i, j]), -0.99, 5.0))
            if S.resting_stop and h.entry_idx != i:                      # research variant: intraday stop fills
                lvl = max(h.entry_px * (1 - S.stop_from_entry), h.peak * (1 - S.trail_from_peak))
                if np.isfinite(S.L[i, j]) and S.L[i, j] <= lvl:
                    fill = O[i, j] if (np.isfinite(O[i, j]) and O[i, j] <= lvl) else lvl
                    r = float(np.clip(fill / CL[i - 1, j] - 1, -0.99, 5.0))
                    pnl += mm * h.v * r
                    v2 = h.v * (1 + r)
                    pnl -= mm * v2 * cost
                    turnover += mm * v2 / e0
                    record(j, h, i, fill, "STOP_RESTING", mm); stop_hits.append(j)
                    continue
            pnl += mm * h.v * r
            h.v *= (1 + r)
            gross += h.v
            c = CL[i, j]
            if np.isfinite(c):
                h.peak, h.min_close, h.max_close = max(h.peak, c), min(h.min_close, c), max(h.max_close, c)
        for j in stop_hits:
            del pos[j]
        pnl += max(0.0, e0 - mm * gross) * dcash
        E = e0 + pnl
        rets[i] = pnl / e0 if e0 else 0.0
        expo[i] = mm * gross / E if E else 0.0
        mhist[i] = mm

        # ── 4. after the close: stop rules ───────────────────────────────────────
        for j, h in pos.items():
            if j in pend_exit:
                continue
            why = S.check_stop_exit(h.entry_px, h.peak, h.entry_idx, h.entry_date, i, j)
            if why:
                pend_exit[j] = why; exit_due[j] = i + 1 + delay

        # ── 5. crash guard (optional) ────────────────────────────────────────────
        panic_i = bool(S.panic[i])
        if S.crash_guard:
            if panic_i:
                for j in pos:
                    if pend_exit.get(j) != "CRASH_GUARD":
                        pend_exit[j] = "CRASH_GUARD"; exit_due[j] = i + 1
                if pos:
                    cg_pending = True
                cg_cool = S.crash_guard_cooldown
            elif cg_cool > 0:
                cg_cool -= 1
            if cg_pending and not panic_i and cg_cool == 0 and i >= start_i:
                slots = S.top_n - len([j for j in pos if j not in pend_exit])
                w0 = S.entry_weight(0, 0, np.ones(len(cols), bool)) if not S.inverse_vol_sizing else 0.05
                for j in target_set:
                    if slots <= 0:
                        break
                    if j not in pos:
                        pend_entry.append((int(j), w0, i + 1, (np.nan, np.nan, dates[i], "CG_REENTRY"))); slots -= 1
                cg_pending = False

        # ── 6. exposure multiplier for tomorrow (optional overlays) ──────────────
        if S.uses_exposure_overlay and pos:
            tgt = S.exposure_target(i, pos, E)
            if (i - last_upd >= 5) or abs(tgt - m) / max(m, 1e-9) > 0.05:
                if abs(tgt - m) > 1e-9:
                    gv = sum(h.v for h in pos.values())
                    E -= cost * abs(tgt - m) * gv
                    turnover += abs(tgt - m) * gv / e0
                m, last_upd = tgt, i

        # ── 7. month-end: rank, exits, entries ───────────────────────────────────
        if i in sig_day and i >= start_i:
            k = sig_day[i]
            elig, sc = S.score_pool(k, rng)
            nvalid = int(np.isfinite(sc).sum())
            if S.market_gate_off(i):
                for j in pos:
                    if j not in pend_exit:
                        pend_exit[j] = "MKT_GATE"; exit_due[j] = i + 1 + delay
                target_set = []
                if log_rejects and nvalid >= 30:
                    order, rank, nv = S.rank_pool(sc)
                    for j, _w in S.select_entries(k, i, order, rank, nv, S.top_n, set(), elig):
                        reject(dates[i], "MKT_GATE", j)
            elif nvalid >= 30:
                order, rank, nv = S.rank_pool(sc)
                picks[S.per[k]] = [cols[jj] for jj in order[:20]]
                for j in list(pos.keys()):
                    if j not in pend_exit and (not np.isfinite(sc[j]) or rank[j] > S.hold_rank):
                        pend_exit[j] = "RANK_EXIT"; exit_due[j] = i + 1 + delay
                gate_block = S.vol_gate and bool(S.vol_gate_me[k])
                slots = S.top_n - len([j for j in pos if j not in pend_exit])
                keep = [j for j in pos if j not in pend_exit]
                new_sel = []
                nxt = dates[min(i + 1, n - 1)]
                cand = S.select_entries(k, i, order, rank, nv, slots, set(pos.keys()), elig, reject=lambda r_, j_: reject(dates[i], r_, j_), blocked=blocked, next_date=nxt) if slots > 0 else []
                for j, w in cand:
                    if gate_block:
                        reject(dates[i], "VOL_GATE", j); continue
                    reg = "VOL_STATE_HIGH" if S.vol_gate_me[k] else "NORMAL"
                    pend_entry.append((int(j), w, i + 1 + delay, (int(rank[j]), float(sc[j]), dates[i], reg)))
                    new_sel.append(int(j))
                target_set = keep + new_sel
        daily.append((dates[i], E, rets[i], expo[i], mm, len(pos)))

    for j, h in pos.items():                                  # mark open positions at the last close (no exit cost)
        trades.append(dict(j=j, Ticker=cols[j], Entry_Date=h.entry_date, Entry_Price=h.entry_px, Exit_Date=dates[-1], Exit_Price=CL[-1, j], Exit_Reason="END_OF_PERIOD",
                           PnL_Pct=(CL[-1, j] / h.entry_px - 1) * 100, Holding_Days=(dates[-1] - h.entry_date).days, Weight_At_Entry=h.w_rel * m, Signal_Date=h.signal_date,
                           Rank_At_Entry=h.rank_at_entry, Score_At_Entry=h.score_at_entry, Regime_At_Entry=h.regime,
                           MAE_Pct=(h.min_close / h.entry_px - 1) * 100, MFE_Pct=(h.max_close / h.entry_px - 1) * 100))
    S.position_metadata = trades
    S.reject_log = pd.DataFrame(rejects)
    S.daily_log = pd.DataFrame(daily, columns=["Date", "Equity", "Return", "Gross_Exposure", "Multiplier", "Positions"]).set_index("Date")
    S.picks_by_month = picks
    ret = pd.Series(rets, index=dates)
    res = dict(ret=ret, expo=pd.Series(expo, index=dates), mult=pd.Series(mhist, index=dates), turnover=turnover, picks=picks,
               equity_curve=(1 + ret[ret.index >= S.start]).cumprod(), trades=get_trade_log(S))
    res.update(compute_metrics(ret, S.start))
    res["ann_turnover"] = turnover / (len(ret[ret.index >= S.start]) / 252)
    S.results = res
    return res


# ══════════════════════════════════════════════════════════════════════════════
# LOGS
# ══════════════════════════════════════════════════════════════════════════════
def get_trade_log(S):
    tl = pd.DataFrame(S.position_metadata)
    if len(tl):
        tl["PnL_Contrib_Pct"] = tl.Weight_At_Entry * tl.PnL_Pct
        tl = tl.drop(columns=["j"]).sort_values(["Entry_Date", "Ticker"]).reset_index(drop=True)
    return tl


def get_reject_log(S):
    return S.reject_log


# ══════════════════════════════════════════════════════════════════════════════
# METRICS / REPORTS
# ══════════════════════════════════════════════════════════════════════════════
def compute_metrics(ret, start="2005-01-01", end=None):
    r = ret.loc[start:end] if end else ret.loc[start:]
    r = r[r.index >= r[r != 0].index.min()]
    yrs = len(r) / 252
    eq = (1 + r).cumprod()
    dd = eq / eq.cummax() - 1
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    ep, cur = [], 0.0
    for v in dd.values:
        if v < 0:
            cur = min(cur, v)
        else:
            if cur < -0.02: ep.append(cur)
            cur = 0.0
    if cur < -0.02: ep.append(cur)
    return dict(cagr=cagr, vol=r.std() * np.sqrt(252), sharpe=r.mean() / r.std() * np.sqrt(252), sortino=r.mean() / np.sqrt((r.clip(upper=0) ** 2).mean()) * np.sqrt(252),
                maxdd=dd.min(), calmar=cagr / abs(dd.min()) if dd.min() else np.nan, avg_dd_depth=float(np.mean(ep)) if ep else 0.0, current_dd=float(dd.iloc[-1]),
                best_month=float(((1 + r).resample("ME").prod() - 1).max()), worst_month=float(((1 + r).resample("ME").prod() - 1).min()))


def trade_stats(tl):
    w, l = tl[tl.PnL_Pct > 0], tl[tl.PnL_Pct < 0]
    return dict(trades=len(tl), win_rate=(tl.PnL_Pct > 0).mean(), avg_trade=tl.PnL_Pct.mean(), median_trade=tl.PnL_Pct.median(), avg_hold_days=tl.Holding_Days.mean(),
                avg_win=w.PnL_Pct.mean(), avg_loss=l.PnL_Pct.mean(), payoff=w.PnL_Pct.mean() / -l.PnL_Pct.mean(), best=tl.PnL_Pct.max(), worst=tl.PnL_Pct.min(),
                avg_mae=tl.MAE_Pct.mean(), avg_mfe=tl.MFE_Pct.mean(),
                profit_factor=(tl.PnL_Contrib_Pct.clip(lower=0).sum() / -tl.PnL_Contrib_Pct.clip(upper=0).sum()))


def print_report(res, S, benchmark_ret=None):
    m = {k: res[k] for k in ("cagr", "vol", "sharpe", "sortino", "maxdd", "calmar", "avg_dd_depth", "current_dd", "best_month", "worst_month")}
    print("\n" + "=" * 78 + f"\nCSM AEGIS  selector={S.selector}  band={S.universe_min_rank}-{S.universe_max_rank}  gate={S.mkt_gate_window}d  fill={S.fill}  cost={S.transaction_cost:.2%}/leg\n" + "=" * 78)
    print(f"  CAGR {m['cagr']*100:6.2f}%   Vol {m['vol']*100:5.1f}%   Sharpe {m['sharpe']:.2f}   Sortino {m['sortino']:.2f}   Calmar {m['calmar']:.2f}")
    print(f"  MaxDD {m['maxdd']*100:6.1f}%   AvgDD depth {m['avg_dd_depth']*100:5.1f}%   Current DD {m['current_dd']*100:5.1f}%   Best/Worst month {m['best_month']*100:+.1f}% / {m['worst_month']*100:+.1f}%")
    ex = res["expo"][res["expo"].index >= S.start]
    tail = "open fills are NOT used" if S.fill == "close" else "WARNING: fill='open' uses the biased open field"
    print(f"  Exposure: {ex[ex > 0].mean():.2f} on invested days, {ex.mean():.2f} over all days ({(ex == 0).mean() * 100:.0f}% of days fully in cash)   one-way turnover/yr {res['ann_turnover']:.1f}x   {tail}")
    if benchmark_ret is not None:
        b = benchmark_ret.reindex(res["ret"].index).fillna(0)
        bm = compute_metrics(b, S.start)
        print(f"  Benchmark (Nifty 500 price): CAGR {bm['cagr']*100:.1f}%  Sharpe {bm['sharpe']:.2f}  MaxDD {bm['maxdd']*100:.0f}%")
    ts = trade_stats(res["trades"])
    print(f"\nTRADES  n={ts['trades']}  win rate {ts['win_rate']*100:.1f}%  avg {ts['avg_trade']:+.2f}%  median {ts['median_trade']:+.2f}%  payoff {ts['payoff']:.2f}  profit factor {ts['profit_factor']:.2f}")
    print(f"        avg win {ts['avg_win']:+.1f}%  avg loss {ts['avg_loss']:+.1f}%  best {ts['best']:+.0f}%  worst {ts['worst']:+.0f}%  avg hold {ts['avg_hold_days']:.0f}d  avg MAE {ts['avg_mae']:.1f}%  avg MFE {ts['avg_mfe']:.1f}%")


def print_exit_breakdown(tl):
    g = tl.groupby("Exit_Reason").agg(n=("PnL_Pct", "size"), avg_pnl_pct=("PnL_Pct", "mean"), win_rate=("PnL_Pct", lambda s: (s > 0).mean()), avg_hold_days=("Holding_Days", "mean"),
                                      avg_mae=("MAE_Pct", "mean"), avg_mfe=("MFE_Pct", "mean"))
    g["share_%"] = g.n / g.n.sum() * 100
    print("\nEXIT BREAKDOWN"); print(g.round(2).to_string())
    return g


def yearly_table(ret, benchmark_ret=None, start="2005-01-01"):
    r = ret[ret.index >= start]
    y = (1 + r).groupby(r.index.year).prod() - 1
    eq = (1 + r).cumprod(); dd = (eq / eq.cummax() - 1).groupby(r.index.year).min()
    df = pd.DataFrame({"return_%": y * 100, "worst_dd_%": dd * 100})
    if benchmark_ret is not None:
        b = benchmark_ret.reindex(r.index).fillna(0); df["benchmark_%"] = ((1 + b).groupby(b.index.year).prod() - 1) * 100
    return df


def print_yearly_returns(ret, benchmark_ret=None, start="2005-01-01"):
    r = ret[ret.index >= start]
    y = (1 + r).groupby(r.index.year).prod() - 1
    eq = (1 + r).cumprod(); dd = (eq / eq.cummax() - 1).groupby(r.index.year).min()
    df = pd.DataFrame({"return_%": y * 100, "worst_dd_%": dd * 100})
    if benchmark_ret is not None:
        b = benchmark_ret.reindex(r.index).fillna(0); df["benchmark_%"] = ((1 + b).groupby(b.index.year).prod() - 1) * 100
    print("\nYEARLY RETURNS"); print(df.round(1).to_string())
    return df


def print_reject_summary(S):
    if S.reject_log is None or not len(S.reject_log):
        return
    g = S.reject_log.groupby("Reason").size().sort_values(ascending=False)
    print("\nENTRY REJECTS (candidates inside top_n that were NOT bought)"); print(g.to_string())


# ══════════════════════════════════════════════════════════════════════════════
# IC DIAGNOSTICS
# ══════════════════════════════════════════════════════════════════════════════
def _nw_t(x, lag):
    x = np.asarray(pd.Series(x).dropna(), dtype=float)
    n = len(x)
    if n < 8: return np.nan
    e = x - x.mean(); lrv = e @ e / n
    for k in range(1, min(lag, n - 1) + 1):
        lrv += 2 * (1 - k / (lag + 1)) * (e[k:] @ e[:-k]) / n
    return x.mean() / np.sqrt(lrv / n) if lrv > 0 else np.nan


def calculate_ic(S, horizons=(1, 3, 6, 12), chunk_months=36):
    """Rank IC of the selector INSIDE the strategy pool: mean, ICIR, hit rate, Newey-West t (lag h-1), top-N basket excess, 36-month chunk decay."""
    F = S.factors if S.factors is not None else S.build_factor_frame()
    mp = S.prices.ffill().resample("ME").last(); mp.index = pd.PeriodIndex(mp.index, freq="M"); mp = mp[~mp.index.duplicated(keep="last")]
    out, ic3 = {}, None
    for h in horizons:
        R = (mp.shift(-h) / mp - 1)
        ics, exc = {}, {}
        for p in F.index.intersection(R.index):
            f, r = F.loc[p], R.loc[p]; ok = f.notna() & r.notna()
            if ok.sum() < 20: continue
            ics[p] = f[ok].rank().corr(r[ok].rank())
            top = f[ok].rank(ascending=False) <= S.top_n; exc[p] = r[ok][top].mean() - r[ok].mean()
        ic, ex = pd.Series(ics), pd.Series(exc); ic, ex = ic[ic.index >= pd.Period(S.start, "M")], ex[ex.index >= pd.Period(S.start, "M")]
        out[h] = dict(ic=ic.mean(), icir=ic.mean() / ic.std(), hit=(ic > 0).mean(), nw_t=_nw_t(ic, max(h - 1, 0)), top_n_excess=ex.mean(), top_n_nw_t=_nw_t(ex, max(h - 1, 0)), n=len(ic))
        if h == 3: ic3 = ic
    chunks = []
    if ic3 is not None:
        end = ic3.index.max()
        while True:
            start = end - (chunk_months - 1); seg = ic3.loc[start:end]
            if len(seg) < 24: break
            chunks.append(dict(chunk=f"{start}->{end}", ic=seg.mean(), nw_t=_nw_t(seg, 2), n=len(seg))); end = start - 1
        chunks = chunks[::-1]
    return dict(by_horizon=pd.DataFrame(out).T, chunks=pd.DataFrame(chunks), ic_series_3m=ic3)


def print_ic_report(ic):
    print("\nSELECTOR IC INSIDE THE POOL (Spearman, month-end -> month-end)"); print(ic["by_horizon"].round(3).to_string())
    if len(ic["chunks"]):
        print("\n3m IC by 36-month chunk (decay check)"); print(ic["chunks"].round(3).to_string(index=False))


# ══════════════════════════════════════════════════════════════════════════════
# PLOTS
# ══════════════════════════════════════════════════════════════════════════════
def plot_performance(res, S, benchmark_ret=None, filename="csm_aegis_performance.png"):
    import matplotlib; matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(OUT_DIR, exist_ok=True)
    r = res["ret"][res["ret"].index >= S.start]; eq = (1 + r).cumprod(); dd = eq / eq.cummax() - 1
    fig, axs = plt.subplots(3, 1, figsize=(11, 10), gridspec_kw={"height_ratios": [2.4, 1, 1]})
    axs[0].plot(eq.index, eq, lw=2, label="CSM Aegis")
    if benchmark_ret is not None:
        b = benchmark_ret.reindex(r.index).fillna(0); axs[0].plot(b.index, (1 + b).cumprod(), color="black", lw=1.1, label="Nifty 500 (price)")
    axs[0].set_yscale("log"); axs[0].legend(); axs[0].set_title("CSM Aegis (faithful booking)")
    axs[1].fill_between(dd.index, dd * 100, 0, color="#eb6834", alpha=.6); axs[1].set_ylabel("drawdown %")
    y = (1 + r).groupby(r.index.year).prod() - 1; axs[2].bar(y.index, y * 100, color=["#1baf7a" if v > 0 else "#e34948" for v in y]); axs[2].set_ylabel("calendar-year return %")
    fig.tight_layout(); fig.savefig(os.path.join(OUT_DIR, filename), dpi=140); plt.close(fig)


# ══════════════════════════════════════════════════════════════════════════════
# COMMAND-LINE RUNNER
# ══════════════════════════════════════════════════════════════════════════════
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.environ.get("CSM_AEGIS_DATA_FOLDER", "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")
PANEL_CACHE = os.path.join(HERE, ".cache")
INDEX_FILE = os.path.join(HERE, "data", "nifty500_price_index.parquet")
REPORT_START = "2005-01-01"
DEFAULT_PRESET = "v1.2"


def _benchmark():
    if os.path.exists(INDEX_FILE):
        return pd.read_parquet(INDEX_FILE)["Nifty_500"].dropna().pct_change()
    return None


def _parse_set(items):
    """Parse --set key=value overrides without evaluating arbitrary Python."""
    overrides = {}
    for item in items or []:
        key, value = item.split("=", 1)
        try:
            overrides[key] = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            overrides[key] = value
    return overrides


class _Tee:
    def __init__(self, path):
        self.file, self.stdout = open(path, "w"), sys.stdout

    def write(self, text):
        self.stdout.write(text)
        self.file.write(text)

    def flush(self):
        self.stdout.flush()
        self.file.flush()


def build(preset, data, **overrides):
    prices, volumes, highs, lows, opens = data
    return CSMAegis.from_preset(
        preset, prices, volumes, highs, lows, opens, start=REPORT_START, **overrides
    ).calculate_factors()


def run_one(preset, data, benchmark, verbose=True, **overrides):
    strategy = build(preset, data, **overrides)
    results = backtest_event_driven(strategy)
    if verbose:
        print_report(results, strategy, benchmark)
        print_exit_breakdown(results["trades"])
        print_yearly_returns(results["ret"], benchmark, REPORT_START)
        print_reject_summary(strategy)
        print("\nUNIVERSE CARD (average names surviving each filter, by year)")
        print(strategy.universe_card().to_string())
        print_ic_report(calculate_ic(strategy))
    return strategy, results


def save_outputs(strategy, results, preset, asof=None):
    os.makedirs(OUT_DIR, exist_ok=True)
    tag = preset.replace(".", "_")
    results["trades"].to_csv(os.path.join(OUT_DIR, f"trade_log_{tag}.csv"), index=False)
    if strategy.reject_log is not None and len(strategy.reject_log):
        strategy.reject_log.to_csv(os.path.join(OUT_DIR, f"reject_log_{tag}.csv"), index=False)
    strategy.daily_log.to_csv(os.path.join(OUT_DIR, f"daily_log_{tag}.csv"))
    results["ret"].to_csv(os.path.join(OUT_DIR, f"daily_returns_{tag}.csv"), header=["ret"])
    yearly_table(results["ret"], _benchmark(), REPORT_START).round(2).to_csv(
        os.path.join(OUT_DIR, f"yearly_returns_{tag}.csv")
    )
    picks = strategy.latest_picks(asof)
    picks.to_csv(os.path.join(OUT_DIR, f"latest_picks_{tag}.csv"), index=False)
    print(
        f"\nLATEST SELECTION  signal date {picks.attrs['signal_date']}  pool {picks.attrs['pool_size']} names  "
        f"market gate OFF: {picks.attrs['market_gate_off']}  "
        f"vol-state blocks new entries: {picks.attrs['vol_gate_blocks_new_entries']}"
    )
    print(picks.head(25)[["rank", "ticker", "score", "r1", "ulcer_neg", "close", "ext_vs_sma50", "blocked_extension", "weight", "entry_stop"]].round(3).to_string(index=False))
    print("\nNOTE: price coverage of the broad universe ends mid-July 2026, so the latest month-end can be partial. Research output, not advice.")


def compare(data, benchmark):
    rows = []
    for preset in ("v1.0", "v1.1", "v1.2", "v1.2_high_return"):
        strategy, results = run_one(preset, data, benchmark, verbose=False)
        trades = results["trades"]
        rows.append(dict(
            preset=preset, CAGR=f"{results['cagr'] * 100:.1f}%", Sharpe=f"{results['sharpe']:.2f}",
            MaxDD=f"{results['maxdd'] * 100:.0f}%", Calmar=f"{results['calmar']:.2f}", trades=len(trades),
            win=f"{(trades.PnL_Pct > 0).mean() * 100:.0f}%", fill=strategy.fill,
            turnover=f"{results['ann_turnover']:.1f}x",
        ))
    print("\nPRESET COMPARISON (faithful, 0.3%/leg, uninvested cash return 0%)\n" + pd.DataFrame(rows).to_string(index=False))


def live(preset, data, overrides, holdings_csv, asof):
    """Print the live exit signals and next-fill candidates for a holdings CSV."""
    strategy = build(preset, data, **overrides)
    holdings_frame = pd.read_csv(holdings_csv)
    required = {"ticker", "entry_date", "entry_price"}
    missing = required - set(holdings_frame.columns)
    if missing:
        raise ValueError(f"holdings CSV is missing columns: {', '.join(sorted(missing))}")
    holdings = {
        row.ticker: dict(entry_date=row.entry_date, entry_price=float(row.entry_price))
        for row in holdings_frame.itertuples()
    }
    asof = pd.Timestamp(asof) if asof else strategy.dates[-1]
    exits = strategy.get_exit_signals(holdings, asof)
    signal_text = ", ".join(f"{ticker}: {reason}" for ticker, reason in exits.items()) if exits else "none"
    print(f"\nEXIT SIGNALS as of {asof.date()} (place at the next close): {signal_text}")
    print("Month-end rank/pool/market-gate exits are evaluated only when asof is a month-end close.")
    picks = strategy.latest_picks(asof)
    print(f"\nPICKS  signal date {picks.attrs['signal_date']}  pool {picks.attrs['pool_size']}  market gate OFF: {picks.attrs['market_gate_off']}  vol-state blocks entries: {picks.attrs['vol_gate_blocks_new_entries']}")
    print(picks.head(strategy.top_n + 5)[["rank", "ticker", "score", "close", "ext_vs_sma50", "blocked_extension", "weight", "entry_stop", "in_hold_zone"]].round(3).to_string(index=False))


def stress(preset, data, overrides):
    rows = []
    scenarios = (
        ("base", {}),
        ("cost 0.6%/leg", dict(transaction_cost=0.006)),
        ("cost 1.0%/leg", dict(transaction_cost=0.010)),
        ("delay +1 day", dict(execution_delay=1)),
        ("delay +2 days", dict(execution_delay=2)),
        ("capacity 5% ADV, Rs1cr", dict(adv_fraction=0.05, initial_capital=1e7)),
        ("capacity 5% ADV, Rs5cr", dict(adv_fraction=0.05, initial_capital=5e7)),
        ("capacity 5% ADV, Rs25cr", dict(adv_fraction=0.05, initial_capital=2.5e8)),
    )
    for name, scenario in scenarios:
        strategy = build(preset, data, **{**overrides, **scenario})
        results = backtest_event_driven(strategy, log_rejects=False)
        rows.append(dict(stress=name, CAGR=f"{results['cagr'] * 100:.1f}%", Sharpe=f"{results['sharpe']:.2f}", MaxDD=f"{results['maxdd'] * 100:.0f}%", Calmar=f"{results['calmar']:.2f}"))
    print("\nSTRESS TESTS\n" + pd.DataFrame(rows).to_string(index=False))


def main(argv=None):
    warnings.filterwarnings("ignore")
    parser = argparse.ArgumentParser(description="Run or backtest CSM Aegis.")
    parser.add_argument("--preset", default=DEFAULT_PRESET, choices=list(PRESETS))
    parser.add_argument("--set", action="append", help="strategy override, e.g. --set top_n=15")
    parser.add_argument("--compare", action="store_true", help="compare all presets")
    parser.add_argument("--stress", action="store_true", help="run cost, delay and capacity stress tests")
    parser.add_argument("--asof", default=None, help="signal date for selection output (YYYY-MM-DD)")
    parser.add_argument("--no-plot", action="store_true")
    parser.add_argument("--holdings", help="CSV with ticker,entry_date,entry_price; prints exits and picks only")
    args = parser.parse_args(argv)
    overrides = _parse_set(args.set)
    if not args.holdings:
        os.makedirs(OUT_DIR, exist_ok=True)
        sys.stdout = _Tee(os.path.join(OUT_DIR, f"run_log_{args.preset.replace('.', '_')}.txt"))
    print("Loading data ...")
    data = load_data(DATA_FOLDER, cache_dir=PANEL_CACHE)
    print(f"Panels {data[0].shape}  {data[0].index.min().date()} -> {data[0].index.max().date()}")
    if args.holdings:
        live(args.preset, data, overrides, args.holdings, args.asof)
        return
    benchmark = _benchmark()
    if args.compare:
        compare(data, benchmark)
    strategy, results = run_one(args.preset, data, benchmark, **overrides)
    save_outputs(strategy, results, args.preset, args.asof)
    if not args.no_plot:
        plot_performance(results, strategy, benchmark, filename=f"csm_aegis_performance_{args.preset.replace('.', '_')}.png")
    if args.stress:
        stress(args.preset, data, overrides)


if __name__ == "__main__":
    main()

"""
residual_momentum_backtest.py
==============================
Residual Momentum — backtest engine + metrics: plain functions, no class, taking the
strategy object as the first argument.

Event-driven day loop (_simulate) with per-trade recording, a yearly-performance table, a
Portfolio-Metrics-and-Win-Rate report, and equity/drawdown/histogram/heatmap plots.

Execution/cost-model assumptions (aum, fixed_bps, impact_k, capadv, slc, rf,
breaker_adv_cap, breaker_cost_bps) live on backtest_event_driven()'s signature. The
drawdown-stop threshold (strat.breaker) and optional ATR-exit threshold (strat.atr_k) are
read from the strategy object, since they're risk rules, not execution mechanics.
"""
import numpy as np
import pandas as pd


# ══════════════════════════════════════════════════════════════════════════════
# METRICS
# ══════════════════════════════════════════════════════════════════════════════

def metrics(net, bench, rf_annual=0.06, trading_days=252):
    rf_daily = rf_annual / trading_days
    eq   = (1 + net).cumprod()
    yrs  = len(net) / trading_days
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    sd   = net.std()
    vol  = sd * np.sqrt(trading_days)
    sharpe  = (net.mean() - rf_daily) / sd * np.sqrt(trading_days) if sd > 0 else np.nan
    # Sortino: std of the negative-return subsample (mean-centered on that subsample itself),
    # not the textbook fixed-target downside deviation -- a common simplification, but it will
    # read a bit higher than a strict-definition Sortino computed elsewhere.
    dn      = net[net < 0].std()
    sortino = (net.mean() - rf_daily) / dn * np.sqrt(trading_days) if dn > 0 else np.nan
    dd  = eq / eq.cummax() - 1
    mdd = dd.min()
    calmar = cagr / abs(mdd) if mdd < 0 else np.nan
    b  = bench.reindex(net.index).fillna(0)
    ex = net - b
    te = ex.std() * np.sqrt(trading_days)
    ir   = ex.mean() * trading_days / te if te > 0 else np.nan
    # ddof=1 on both sides (np.cov defaults to sample covariance) so beta isn't biased by the
    # N/(N-1) mismatch that np.var's default ddof=0 would otherwise introduce.
    beta = np.cov(net, b)[0, 1] / np.var(b, ddof=1) if np.var(b, ddof=1) > 0 else np.nan
    return dict(CAGR=cagr, Vol=vol, Sharpe=sharpe, Sortino=sortino,
                MaxDD=mdd, Calmar=calmar, IR_vs_mkt=ir, beta=beta)


# ══════════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN BACKTEST ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _simulate(strat, WT, aum, fixed_bps, impact_k, capadv, slc, rf, breaker_adv_cap, breaker_cost_bps):
    """Event-driven day loop with sliced circuit-breaker exits. Reads
    strat.days/close/opn/tv/atr/low/high/breaker/atr_k/drift_band/trading_days.

    Exit taxonomy: STOP_HIT (sub-typed BREAKER = sliced drawdown-from-peak stop, ATR =
    optional same-day ATR stop), REBALANCE (dropped from the target book at a monthly
    rebalance), END_OF_PERIOD (still open at the last simulated day, force-closed for
    reporting). Regime de-risking only affects the NEXT month's target weight -- it never
    forces an instant same-day flatten."""
    days, close, opn, tv, atr = strat.days, strat.close, strat.opn, strat.tv, strat.atr
    low, high = strat.low, strat.high
    cff  = close.ffill()
    adv  = tv.rolling(21, min_periods=10).median()
    pos  = days.searchsorted(WT.index, side="right")
    fills = {days[p]: t for t, p in zip(WT.index, pos) if p < len(days)}
    start = min(fills)
    idx   = days[days >= start]
    cols  = close.columns
    band  = strat.drift_band
    brk   = strat.breaker
    atrk  = strat.atr_k
    rf_d  = rf / strat.trading_days

    shares        = pd.Series(0.0, cols)
    peak          = pd.Series(np.nan, cols)
    pending_exit  = pd.Series(0.0, cols)
    cash          = float(aum)
    tot           = 0.0
    eq            = pd.Series(index=idx, dtype=float)

    # trade-log bookkeeping (observational only)
    strat.position_metadata = []
    entry_price, entry_date, entry_weight, entry_shares = {}, {}, {}, {}
    min_price, max_price = {}, {}
    exit_accum_val, exit_accum_shares, exit_kind = {}, {}, {}

    # turnover-by-liquidity-tier bookkeeping (observational only; tier defs near `tval` below)
    strat.turnover_by_adv_tier = {}

    def _close_trade(tkr, exit_date, exit_price, reason, stop_type=""):
        strat.position_metadata.append(dict(
            Ticker=tkr, Entry_Date=entry_date[tkr], Entry_Price=entry_price[tkr],
            Exit_Date=exit_date, Exit_Price=float(exit_price),
            Weight=entry_weight[tkr], Quantity=entry_shares[tkr],
            Exit_Reason=reason, Stop_Type=stop_type,
            Min_Price=min_price.get(tkr, entry_price[tkr]),
            Max_Price=max_price.get(tkr, entry_price[tkr]),
        ))
        for store in (entry_price, entry_date, entry_weight, entry_shares, min_price,
                     max_price, exit_accum_val, exit_accum_shares, exit_kind):
            store.pop(tkr, None)

    for d in idx:
        c = cff.loc[d]
        o = opn.loc[d].where(opn.loc[d] > 0).fillna(c)   # today's open, falling back to close
        prev_shares = shares.copy()   # pre-today snapshot, for entry/exit detection

        # MAE/MFE tracking, updated before today's closures so a same-day exit reflects
        # today's price extremes too.
        if entry_price:
            day_low  = low.loc[d]  if not low.empty  else c
            day_high = high.loc[d] if not high.empty else c
            for tkr in entry_price:
                lo, hi = day_low.get(tkr), day_high.get(tkr)
                if pd.isna(lo) or lo <= 0:
                    lo = c.get(tkr, min_price[tkr])
                if pd.isna(hi) or hi <= 0:
                    hi = c.get(tkr, max_price[tkr])
                min_price[tkr] = min(min_price[tkr], float(lo))
                max_price[tkr] = max(max_price[tkr], float(hi))

        if pending_exit.any():
            # Fills at today's open (same basis as REBALANCE fills below), not close --
            # a stop triggered on a prior close should exit ASAP the next session, not wait
            # for that session's own close.
            max_sell  = (breaker_adv_cap * adv.loc[d] / o).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            sell      = pending_exit.clip(upper=max_sell)
            sell_val  = sell * o
            cost_brk  = float((sell_val * breaker_cost_bps / 1e4).sum())
            cash     += float(sell_val.sum()) - cost_brk
            tot      += float(sell_val.sum())
            shares   -= sell
            pending_exit = (pending_exit - sell).clip(lower=0.0)

            # accumulate this day's slice toward the BREAKER trade record; close out once
            # a position has fully liquidated (non-rebalance days)
            for tkr, amt in sell[sell > 0].items():
                if tkr not in entry_price:
                    continue
                exit_accum_val[tkr]    = exit_accum_val.get(tkr, 0.0) + float(sell_val[tkr])
                exit_accum_shares[tkr] = exit_accum_shares.get(tkr, 0.0) + float(amt)
                exit_kind[tkr] = "BREAKER"
            for tkr in [t for t in exit_kind if exit_kind[t] == "BREAKER"]:
                if abs(shares[tkr]) < 1e-9 and exit_accum_shares.get(tkr, 0.0) > 0:
                    avg_px = exit_accum_val[tkr] / exit_accum_shares[tkr]
                    _close_trade(tkr, d, avg_px, "STOP_HIT", "BREAKER")

        if d in fills:
            t  = fills[d]
            w  = WT.loc[t]
            mk = o

            # If a BREAKER liquidation is still mid-flight (bounded by breaker_adv_cap, it can
            # take several sessions to fully unwind), force-complete whatever's left at today's
            # rebalance open before applying new target weights. Otherwise a name that
            # re-qualifies for selection while its stop-out is still in progress would have its
            # rebalance buy blended into the stale, partially-sold share count, and the
            # eventual trade record would mix the old trade's entry info with the new
            # rebalance-driven share changes.
            still_pending = pending_exit[pending_exit > 0]
            if len(still_pending):
                px_now   = mk.loc[still_pending.index]
                val      = still_pending * px_now
                cost_fin = val * breaker_cost_bps / 1e4
                cash    += float(val.sum()) - float(cost_fin.sum())
                tot     += float(val.sum())
                shares.loc[still_pending.index]       -= still_pending
                pending_exit.loc[still_pending.index]  = 0.0
                for tkr, v in val.items():
                    if tkr not in entry_price:
                        continue
                    exit_accum_val[tkr]    = exit_accum_val.get(tkr, 0.0) + float(v)
                    exit_accum_shares[tkr] = exit_accum_shares.get(tkr, 0.0) + float(still_pending[tkr])
                    exit_kind[tkr] = "BREAKER"
                    if abs(shares[tkr]) < 1e-9:
                        avg_px = exit_accum_val[tkr] / exit_accum_shares[tkr]
                        _close_trade(tkr, d, avg_px, "STOP_HIT", "BREAKER")

            pre_reb_shares = shares.copy()   # post-forced-completion snapshot, used below to
                                              # decide which of today's buys are genuinely fresh
            V  = cash + float((shares * mk).sum())
            cur_w = (shares * mk) / V
            tgt   = w.copy()
            if band > 0:
                hr  = (cur_w > 1e-9) & (tgt > 1e-9) & ((tgt - cur_w).abs() <= band)
                tgt = tgt.where(~hr, cur_w)
            tgt_sh = ((tgt * V) / mk).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            dsh    = tgt_sh - shares
            csh    = (capadv * adv.loc[t] / mk).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            dsh    = dsh.clip(lower=-csh, upper=csh)
            tval   = dsh.abs() * mk

            # Buckets this rebalance's traded $ value by the traded name's ADV tier within
            # that day's top-N universe (1=most liquid fifth .. 5=least liquid fifth;
            # 0=name had already dropped out of the tracked universe).
            traded = tval[tval > 0]
            if len(traded):
                u_names = strat.univ.loc[t]
                adv_u = adv.loc[t, u_names[u_names].index].dropna()
                adv_u = adv_u[adv_u > 0]
                if len(adv_u) >= 5:
                    bin_idx = pd.qcut(adv_u, 5, labels=False, duplicates="drop")
                    tier = bin_idx.max() - bin_idx + 1
                    for tkr, val in traded.items():
                        lvl = tier.get(tkr)
                        key = int(lvl) if pd.notna(lvl) else 0
                        strat.turnover_by_adv_tier[key] = (
                            strat.turnover_by_adv_tier.get(key, 0.0) + float(val))

            cost   = float((tval * (fixed_bps / 1e4
                            + impact_k / 1e4
                            * (tval / adv.loc[t]).replace([np.inf, -np.inf], np.nan).fillna(0.0)
                            / slc)).sum())
            cash   -= float((dsh * mk).sum()) + cost
            shares  = shares + dsh
            tot    += float(tval.sum())

            # fresh entries: previously flat as of just before this rebalance (i.e. after any
            # forced BREAKER completion above), now bought
            fresh = dsh[(pre_reb_shares.reindex(dsh.index).fillna(0.0).abs() < 1e-9) & (dsh > 0)]

            # peak: only reset the high-water mark for genuinely fresh entries. A name that
            # was already held and simply gets topped up this month keeps its existing peak
            # (bumped up only if today's fill price is itself a new high) -- otherwise the
            # breaker stop "forgets" prior gains every time a held name's target weight rises.
            fresh_mask = pd.Series(False, index=peak.index)
            if len(fresh):
                fresh_mask.loc[fresh.index] = True
            peak = peak.mask(fresh_mask, mk)
            topped_up = ~fresh_mask & (dsh > 0)
            peak = peak.mask(topped_up & ((mk > peak) | peak.isna()), mk)

            for tkr, qty in fresh.items():
                entry_price[tkr]  = float(mk[tkr])
                entry_date[tkr]   = d
                entry_weight[tkr] = float(w.get(tkr, 0.0))
                entry_shares[tkr] = float(qty)
                min_price[tkr] = max_price[tkr] = float(mk[tkr])

            # Keep the running cost basis honest for names that stay open across multiple
            # rebalances: top-ups blend into a volume-weighted average entry price (so
            # PnL_Abs/Position_Size reflect the shares actually bought, not just the original
            # entry-day quantity); trims shrink the tracked share count to match what's still
            # held, keeping the existing avg cost basis on the remainder. Realized P&L on
            # shares sold in a trim isn't separately booked, so PnL_Abs at eventual close is
            # still an approximation for a ticker trimmed before its final exit -- just a much
            # closer one than only ever using the entry-day quantity.
            for tkr, delta in dsh.items():
                if tkr in fresh.index or abs(delta) < 1e-9 or tkr not in entry_price:
                    continue
                if abs(shares[tkr]) < 1e-9:
                    continue   # fully closed this rebalance -- handled by the closure loop below
                if delta > 0:
                    old_qty = entry_shares[tkr]
                    new_qty = old_qty + delta
                    entry_price[tkr]  = (entry_price[tkr] * old_qty + float(mk[tkr]) * delta) / new_qty
                    entry_shares[tkr] = new_qty
                    entry_weight[tkr] = float(w.get(tkr, entry_weight[tkr]))
                else:
                    entry_shares[tkr] = float(shares[tkr])

            # catch-all closure for rebalance days: a plain REBALANCE exit, or a BREAKER
            # slice that happens to finish on the same day a rebalance runs (already-closed
            # tickers are no longer in entry_price, so this never double-counts).
            for tkr in list(entry_price.keys()):
                if abs(prev_shares.get(tkr, 0.0)) > 1e-9 and abs(shares[tkr]) < 1e-9:
                    if exit_kind.get(tkr) == "BREAKER" and exit_accum_shares.get(tkr, 0.0) > 0:
                        avg_px = exit_accum_val[tkr] / exit_accum_shares[tkr]
                        _close_trade(tkr, d, avg_px, "STOP_HIT", "BREAKER")
                    else:
                        _close_trade(tkr, d, float(mk[tkr]), "REBALANCE")

        held = shares != 0
        peak = peak.mask(held & ((c > peak) | peak.isna()), c)

        if brk is not None:
            triggered = held & (c < peak * (1 - brk)) & (pending_exit == 0)
            if triggered.any():
                pending_exit += shares.where(triggered, 0.0)
                for tkr in triggered[triggered].index:   # tag as BREAKER-in-progress
                    if tkr in entry_price:
                        exit_kind.setdefault(tkr, "BREAKER")
        if atrk is not None:
            ex = held & (c < peak - atrk * atr.loc[d])
            if ex.any():
                liq  = float((shares * c)[ex].sum())
                tot += abs(liq)
                cash += liq - abs(liq) * (fixed_bps / 1e4)
                shares = shares.mask(ex, 0.0)
                # immediate full ATR exit -- same-day, no slicing
                for tkr in ex[ex].index:
                    if tkr in entry_price:
                        _close_trade(tkr, d, float(c[tkr]), "STOP_HIT", "ATR")

        cash *= (1 + rf_d)
        eq.loc[d] = cash + float((shares * c).sum())

    # force-close anything still open at the end of the backtest (mark-to-market)
    last_c = cff.loc[idx[-1]]
    for tkr in list(entry_price.keys()):
        _close_trade(tkr, idx[-1], float(last_c[tkr]), "END_OF_PERIOD")

    net = eq.pct_change().dropna()
    yrs = len(net) / strat.trading_days
    return net, tot / eq.mean() / yrs


def backtest_event_driven(strat, aum=5e8, fixed_bps=15, impact_k=500, capadv=0.25, slc=10,
                          rf=0.06, breaker_adv_cap=0.05, breaker_cost_bps=75, stagger=False):
    """Requires strat.positions already set (strat.get_positions(start) called first).
    capadv=0.25 caps any single rebalance order at 25% of a name's 21-day median $-volume
    (was 1.0/100% -- unrealistic order-size assumption for anything outside the most liquid
    names). stagger=True runs 3 offset-and-average simulations instead of one (not used by
    the validated config). Returns (net_returns, turnover)."""
    WT = strat.positions
    if not stagger:
        return _simulate(strat, WT, aum, fixed_bps, impact_k, capadv, slc, rf,
                         breaker_adv_cap, breaker_cost_bps)

    dd = strat.days
    base_pos = dd.searchsorted(WT.index)
    nets = []
    for off in (0, 7, 14):
        np_ = np.clip(base_pos + off, 0, len(dd) - 1)
        WT2 = WT.copy()
        WT2.index = dd[np_]
        WT2 = WT2[~WT2.index.duplicated(keep="first")]
        n2, _ = _simulate(strat, WT2, aum, fixed_bps, impact_k, capadv, slc, rf,
                          breaker_adv_cap, breaker_cost_bps)
        nets.append(n2)
    return pd.concat(nets, axis=1).mean(axis=1).dropna(), np.nan


# ══════════════════════════════════════════════════════════════════════════════
# TRADE LOG
# ══════════════════════════════════════════════════════════════════════════════

def get_trade_log(strat):
    """Build a trade-log DataFrame from strat.position_metadata, populated as a side effect
    of backtest_event_driven() — call this after running the backtest."""
    if not strat.position_metadata:
        print("Warning: No trade metadata. Run backtest_event_driven() first.")
        return pd.DataFrame()

    rows = []
    for m in strat.position_metadata:
        entry_price, exit_price = m["Entry_Price"], m["Exit_Price"]
        entry_date, exit_date   = m["Entry_Date"], m["Exit_Date"]
        qty = m["Quantity"]

        pnl_pct = ((exit_price / entry_price) - 1) * 100 \
                  if (entry_price and entry_price > 0 and exit_price and exit_price > 0) else np.nan
        pnl_abs = qty * (exit_price - entry_price) if pd.notna(pnl_pct) else np.nan
        holding_days = max((exit_date - entry_date).days, 1)

        win = pd.notna(pnl_pct) and pnl_pct > 0
        exit_detail = f"{m['Exit_Reason']}_{'WIN' if win else 'LOSS'}"

        entry_p = entry_price if entry_price and entry_price > 0 else np.nan
        mae_pct = ((m["Min_Price"] / entry_p) - 1) * 100 if pd.notna(entry_p) else np.nan
        mfe_pct = ((m["Max_Price"] / entry_p) - 1) * 100 if pd.notna(entry_p) else np.nan

        rows.append({
            "Ticker": m["Ticker"], "Entry_Date": entry_date, "Entry_Price": round(entry_price, 4),
            "Exit_Date": exit_date, "Exit_Price": round(exit_price, 4),
            "Exit_Reason": m["Exit_Reason"], "Stop_Type": m["Stop_Type"], "Exit_Detail": exit_detail,
            "Weight": round(m["Weight"], 6), "Quantity": round(qty, 4),
            "Position_Size": round(entry_price * qty, 2),
            "PnL_Pct": round(pnl_pct, 4) if pd.notna(pnl_pct) else np.nan,
            "PnL_Abs": round(pnl_abs, 2) if pd.notna(pnl_abs) else np.nan,
            "Holding_Days": holding_days,
            "MAE_Pct": round(mae_pct, 2) if pd.notna(mae_pct) else np.nan,
            "MFE_Pct": round(mfe_pct, 2) if pd.notna(mfe_pct) else np.nan,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("Entry_Date").reset_index(drop=True)
        df.index += 1
        df.index.name = "Trade_ID"

        wins, total = (df["PnL_Pct"] > 0).sum(), len(df)
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {(df['PnL_Pct'] < 0).sum()}"
              f" | Win Rate: {wins / total * 100:.1f}%")
        print(f"[Trade Log] Worst trade: {df['PnL_Pct'].min():.2f}%  Best trade: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
    return df


def populate_trade_stats(results, detailed_log):
    if detailed_log is None or detailed_log.empty:
        return results

    dl = detailed_log
    wins, losses, total_t = (dl["PnL_Pct"] > 0).sum(), (dl["PnL_Pct"] < 0).sum(), len(dl)

    results["trade_win_rate"]      = wins / total_t if total_t > 0 else 0.0
    results["total_trades_count"]  = total_t
    results["avg_trade_return"]    = dl["PnL_Pct"].mean()
    results["median_trade_return"] = dl["PnL_Pct"].median()
    results["avg_holding_days"]    = dl["Holding_Days"].mean()
    results["best_trade"]          = dl["PnL_Pct"].max()
    results["worst_trade"]         = dl["PnL_Pct"].min()
    results["avg_mae"]             = dl["MAE_Pct"].mean()
    results["avg_mfe"]             = dl["MFE_Pct"].mean()

    avg_win  = dl.loc[dl["PnL_Pct"] > 0, "PnL_Pct"].mean() if wins > 0 else 0.0
    avg_loss = dl.loc[dl["PnL_Pct"] < 0, "PnL_Pct"].abs().mean() if losses > 0 else 0.0
    results["avg_win_pct"]  = avg_win
    results["avg_loss_pct"] = avg_loss
    results["payoff_ratio"] = avg_win / avg_loss if avg_loss > 0 else float("inf")

    gw_pct = dl.loc[dl["PnL_Pct"] > 0, "PnL_Pct"].sum()
    gl_pct = dl.loc[dl["PnL_Pct"] < 0, "PnL_Pct"].abs().sum()
    results["profit_factor"] = gw_pct / gl_pct if gl_pct > 0 else float("inf")

    gw_abs = dl.loc[dl["PnL_Abs"] > 0, "PnL_Abs"].sum()
    gl_abs = dl.loc[dl["PnL_Abs"] < 0, "PnL_Abs"].abs().sum()
    results["profit_factor_dollar"] = gw_abs / gl_abs if gl_abs > 0 else float("inf")

    reason_counts = dl["Exit_Reason"].value_counts()
    results["pct_stops"]      = reason_counts.get("STOP_HIT", 0) / total_t * 100
    results["pct_rebalance"]  = reason_counts.get("REBALANCE", 0) / total_t * 100
    results["pct_end_period"] = reason_counts.get("END_OF_PERIOD", 0) / total_t * 100

    return results


def print_exit_breakdown(trade_log):
    """Per top-level reason: n / win% / avg PnL% / median PnL% / % of total P&L contribution
    (Sigma weight*PnL%), then Stop_Type sub-buckets (BREAKER/ATR) under STOP_HIT only.

    Median is shown alongside the mean deliberately: a handful of extreme trades can drag a
    bucket's mean PnL positive even when most trades in it lose money -- mean-only reporting
    would hide that."""
    if trade_log is None or trade_log.empty:
        print("\n-- Exit Breakdown -- no trades --")
        return

    df = trade_log.copy()
    df["_c"] = df["Weight"] * df["PnL_Pct"]
    tot = df["_c"].sum() or 1.0

    def _row(label, sub, indent=""):
        print(f"  {indent}{label:<20}{len(sub):>5}{(sub['PnL_Pct'] > 0).mean() * 100:>7.1f}%"
              f"{sub['PnL_Pct'].mean():>9.2f}%{sub['PnL_Pct'].median():>9.2f}%"
              f"{(sub['PnL_Pct'] < 0).mean() * 100:>7.1f}%{sub['_c'].sum() / tot * 100:>8.1f}%")

    print("\n-- Exit Breakdown -- by reason & outcome --")
    print(f"  {'bucket':<22}{'n':>5}{'win%':>8}{'avgPnL':>9}{'medPnL':>9}{'neg%':>8}{'%ofPnL':>9}")
    print(f"  {'-' * 66}")
    fam_order = ["STOP_HIT", "REBALANCE", "END_OF_PERIOD"]
    fams = fam_order + [r for r in df["Exit_Reason"].unique() if r not in fam_order]
    for fam in fams:
        sub = df[df["Exit_Reason"] == fam]
        if sub.empty:
            continue
        _row(fam, sub)
        if fam == "STOP_HIT":
            for st in ("BREAKER", "ATR"):
                s = sub[sub["Stop_Type"] == st]
                if s.empty:
                    continue
                _row(st, s, indent="L ")
    print(f"  {'-' * 66}")


def print_turnover_attribution(strat):
    """% of total traded $ value by ADV tier of that day's top-N universe (1=most liquid
    fifth .. 5=least liquid fifth; 0=name had dropped out of the tracked universe)."""
    d = getattr(strat, "turnover_by_adv_tier", None)
    if not d:
        print("\n-- Turnover by Liquidity Tier -- no data --")
        return
    tot = sum(d.values()) or 1.0
    print("\n-- Turnover by Liquidity Tier -- (share of total traded $ value) --")
    for k in (1, 2, 3, 4, 5, 0):
        if k not in d:
            continue
        label = f"Tier {k}" if k else "Untracked (out of universe)"
        print(f"  {label:<28}{d[k] / tot * 100:>7.1f}%")


# ══════════════════════════════════════════════════════════════════════════════
# YEARLY RETURNS + YEARLY DRAWDOWN
# ══════════════════════════════════════════════════════════════════════════════

def compute_yearly_table(net):
    """Per-calendar-year Return + intra-year Max_DD, using the prior year-end level as each
    year's opening base for the running peak."""
    eq = (1 + net).cumprod()
    rows, prev_val = [], 1.0
    for y in sorted(eq.index.year.unique()):
        g = eq[eq.index.year == y]
        yearly_ret = g.iloc[-1] / prev_val - 1
        base = pd.concat([pd.Series([prev_val]), g])
        cm = base.cummax()
        max_dd = float((base / cm - 1).min())
        rows.append((y, float(yearly_ret), max_dd))
        prev_val = g.iloc[-1]
    return pd.DataFrame(rows, columns=["Year", "Return", "Max_DD"]).set_index("Year")


def print_yearly_performance(net):
    table = compute_yearly_table(net)
    print("=" * 40)
    print("YEARLY PERFORMANCE")
    print("=" * 40)
    print(f"{'Year':<6}{'Return':>10}{'Max DD':>10}")
    for y, row in table.iterrows():
        print(f"{y:<6}{row['Return']:>+10.1%}{row['Max_DD']:>10.1%}")
    print(f"{'Avg':<6}{table['Return'].mean():>+10.1%}{table['Max_DD'].mean():>10.1%}")
    print("=" * 40)
    return table


# ══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE REPORT
# ══════════════════════════════════════════════════════════════════════════════

def print_report(net, turn, bench, rf_annual=0.06, trading_days=252, label="RESULT"):
    """Portfolio Metrics + Win Rate. Trade Statistics / Exit Breakdown are printed
    separately (see run_residual_momentum_strategy.py) since they need the trade log."""
    m = metrics(net, bench, rf_annual, trading_days)
    eq = (1 + net).cumprod()
    dd = eq / eq.cummax() - 1
    avg_dd = float(dd.mean())

    b = bench.reindex(net.index).fillna(0)
    alpha = float((net.mean() - m["beta"] * b.mean()) * trading_days) if pd.notna(m["beta"]) else np.nan

    daily_win_rate = float((net > 0).mean())
    monthly_ret = (1 + net).resample("ME").apply(lambda x: x.prod() - 1)
    monthly_win_rate = float((monthly_ret > 0).mean())

    print("=" * 78)
    print(f"PERFORMANCE REPORT — {label}")
    print("=" * 78)
    print("Portfolio Metrics")
    print(f"  CAGR                : {m['CAGR']:+.2%}")
    print(f"  Volatility (ann.)   : {m['Vol']:.2%}")
    print(f"  Sharpe              : {m['Sharpe']:.2f}")
    print(f"  Sortino             : {m['Sortino']:.2f}")
    print(f"  Calmar              : {m['Calmar']:.2f}")
    print(f"  Max Drawdown        : {m['MaxDD']:.2%}")
    print(f"  Avg Drawdown        : {avg_dd:.2%}")
    print(f"  Beta (vs mkt)       : {m['beta']:.2f}")
    print(f"  Alpha (ann., realized) : {alpha:+.2%}")
    print(f"  Information Ratio   : {m['IR_vs_mkt']:.2f}")
    print(f"  Annual Turnover     : {turn:.0%}")
    print()
    print("Win Rate")
    print(f"  Daily               : {daily_win_rate:.1%}")
    print(f"  Monthly             : {monthly_win_rate:.1%}")
    print("=" * 78)
    return m


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════

def plot_performance(net, bench, strat=None, filename="residual_momentum_performance.png"):
    """Equity curve (log scale) vs benchmark, drawdown profile, and a monthly-return
    histogram. If `strat` is passed (with strat.positions set), adds an active-position-count
    panel sampled at rebalance dates (not daily). Also saves a Year x Month returns heatmap."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    eq = (1 + net).cumprod()
    b = bench.reindex(net.index).fillna(0)
    bench_eq = (1 + b).cumprod()
    dd = eq / eq.cummax() - 1
    avg_dd = float(dd.mean())
    monthly_ret = (1 + net).resample("ME").apply(lambda x: x.prod() - 1)

    n_panels = 4 if strat is not None and strat.positions is not None else 3
    fig, axes = plt.subplots(n_panels, 1, figsize=(14, 4 * n_panels))

    ax = axes[0]
    ax.plot(eq.index, eq.values, label="Strategy", linewidth=1.3)
    ax.plot(bench_eq.index, bench_eq.values, label="Benchmark (EW universe)", alpha=0.7, linewidth=1.0)
    ax.set_yscale("log")
    ax.set_title("Equity Curve (log scale)")
    ax.legend()

    ax = axes[1]
    ax.fill_between(dd.index, dd.values * 100, 0, color="firebrick", alpha=0.5)
    ax.axhline(avg_dd * 100, color="black", linestyle="--", linewidth=1, label=f"Avg DD {avg_dd:.1%}")
    ax.set_title("Drawdown (%)")
    ax.legend()

    panel_i = 2
    if n_panels == 4:
        ax = axes[2]
        active = (strat.positions > 0).sum(axis=1)
        ax.step(active.index, active.values, where="post")
        ax.set_title("Active Positions at Each Rebalance (not daily)")
        panel_i = 3

    ax = axes[panel_i]
    ax.hist(monthly_ret.values * 100, bins=30, color="steelblue", edgecolor="white")
    ax.axvline(monthly_ret.mean() * 100, color="red", linestyle="--", linewidth=1,
              label=f"Mean {monthly_ret.mean():.1%}")
    ax.set_title("Monthly Return Distribution (%)")
    ax.legend()

    fig.tight_layout()
    fig.savefig(filename, dpi=120)
    plt.close(fig)
    print(f"[plot] saved {filename}")

    heatmap_filename = filename.rsplit(".", 1)[0] + "_heatmap.png"
    try:
        import seaborn as sns
        pct = monthly_ret * 100
        table = pct.groupby([pct.index.year, pct.index.month]).first().unstack()
        table.columns = [pd.Timestamp(2000, m, 1).strftime("%b") for m in table.columns]
        fig2, ax2 = plt.subplots(figsize=(10, max(3, 0.4 * table.shape[0])))
        sns.heatmap(table, annot=True, fmt=".1f", cmap="RdYlGn", center=0, ax=ax2, cbar_kws={"label": "%"})
        ax2.set_title("Monthly Returns Heatmap (%)")
        fig2.tight_layout()
        fig2.savefig(heatmap_filename, dpi=120)
        plt.close(fig2)
        print(f"[plot] saved {heatmap_filename}")
    except Exception as e:
        print(f"[plot] heatmap skipped: {e}")

    return filename, heatmap_filename
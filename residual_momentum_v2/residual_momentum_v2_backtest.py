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

def metrics(net, bench, rf_annual=0.0, trading_days=252):
    rf_daily = rf_annual / trading_days
    eq   = (1 + net).cumprod()
    elapsed_days = (net.index[-1] - net.index[0]).total_seconds() / 86400
    yrs = elapsed_days / 365.2425
    cagr = eq.iloc[-1] ** (1 / yrs) - 1 if yrs > 0 else np.nan
    sd   = net.std()
    vol  = sd * np.sqrt(trading_days)
    sharpe  = (net.mean() - rf_daily) / sd * np.sqrt(trading_days) if sd > 0 else np.nan
    excess = net - rf_daily
    downside = np.sqrt(np.square(excess.clip(upper=0)).mean())
    sortino = excess.mean() / downside * np.sqrt(trading_days) if downside > 0 else np.nan
    dd  = eq / eq.cummax().clip(lower=1.0) - 1
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

def _transaction_cost(value, adv, fixed_bps, impact_k, slc):
    """Same fixed plus participation-impact model for stocks and ETFs."""
    if not np.isfinite(adv) or adv <= 0:
        return float("inf") if value > 0 else 0.0
    return value * (fixed_bps / 1e4 + impact_k / 1e4 * (value / adv) / slc)


def _stock_trade_cost(dsh, price, adv, fixed_bps, impact_k, slc):
    values = (dsh.abs() * price).fillna(0.0)
    participation = (values / adv).replace([np.inf, -np.inf], np.nan).fillna(0.0)
    return float((values * (fixed_bps / 1e4 + impact_k / 1e4 * participation / slc)).sum())


def _scale_stock_buys_to_budget(dsh, price, adv, available_cash, fixed_bps, impact_k, slc):
    """Scale only purchases; sales and their costs are included in the budget."""
    sells = dsh.clip(upper=0)
    buys = dsh.clip(lower=0)
    sell_proceeds = float((-sells * price).sum())
    budget = max(0.0, available_cash + sell_proceeds)
    def needed(fraction):
        trades = sells + buys * fraction
        return float((buys * fraction * price).sum()) + _stock_trade_cost(trades, price, adv, fixed_bps, impact_k, slc)
    if needed(1.0) <= budget:
        return sells + np.floor(buys)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if needed(mid) <= budget:
            lo = mid
        else:
            hi = mid
    return sells + np.floor(buys * lo)


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
    adv_previous = adv.shift(1)
    previous_close = cff.shift(1)
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
        valid_open = opn.loc[d].notna() & (opn.loc[d] > 0) & close.loc[d].notna()
        o = opn.loc[d].where(valid_open).fillna(previous_close.loc[d])
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
            max_sell  = (breaker_adv_cap * adv_previous.loc[d] / o).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            sell      = np.floor(pending_exit.clip(upper=max_sell).where(valid_open, 0.0))
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

            # Pending stop exits remain queued and are not repurchased while pending.
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
            dsh    = np.trunc(dsh.clip(lower=-csh, upper=csh).where(valid_open & (pending_exit <= 0), 0.0))
            # Sell first, then scale buys to available cash, including trading costs.
            dsh = _scale_stock_buys_to_budget(dsh, mk, adv.loc[t], cash,
                                               fixed_bps, impact_k, slc)
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
            ex = held & (c < peak - atrk * atr.loc[d]) & (pending_exit == 0)
            if ex.any():
                pending_exit += shares.where(ex, 0.0)
                for tkr in ex[ex].index:
                    if tkr in entry_price:
                        exit_kind.setdefault(tkr, "BREAKER")

        cash *= (1 + rf_d)
        eq.loc[d] = cash + float((shares * c).sum())

    # force-close anything still open at the end of the backtest (mark-to-market)
    last_c = cff.loc[idx[-1]]
    for tkr in list(entry_price.keys()):
        _close_trade(tkr, idx[-1], float(last_c[tkr]), "END_OF_PERIOD")

    net = eq.pct_change()
    net.iloc[0] = eq.iloc[0] / aum - 1.0
    yrs = max((idx[-1] - idx[0]).days / 365.2425, 1 / strat.trading_days)
    return net, tot / eq.mean() / yrs


def _cash_backtest_event_driven(strat, aum=5e8, fixed_bps=15, impact_k=500, capadv=0.25, slc=10,
                          rf=0.0, breaker_adv_cap=0.05, breaker_cost_bps=75, stagger=False):
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

def print_report(net, turn, bench, rf_annual=0.0, trading_days=252, label="RESULT"):
    """Portfolio Metrics + Win Rate. Trade Statistics / Exit Breakdown are printed
    separately (see run_residual_momentum_strategy.py) since they need the trade log."""
    m = metrics(net, bench, rf_annual, trading_days)
    eq = (1 + net).cumprod()
    dd = eq / eq.cummax().clip(lower=1.0) - 1
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
    dd = eq / eq.cummax().clip(lower=1.0) - 1
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

# V2 ETF cash-sweep simulation
import os



DATA_DIR = os.environ.get("RESIDUAL_MOM_ETF_DATA_DIR",
                          "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data")
ETF_START_DATE = {
    "GOLDBEES": pd.Timestamp("2007-03-19"),
    "SILVERBEES": pd.Timestamp("2022-02-07"),
}


def load_etf_data(etf_name):
    """Load ETF prices and volume, needed for the shared transaction-cost model."""
    path = os.path.join(DATA_DIR, f"{etf_name}.csv")
    df = pd.read_csv(path, usecols=["timestamp", "open", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=True).dt.tz_convert("Asia/Kolkata").dt.tz_localize(None).dt.normalize()
    df = df.drop_duplicates("timestamp").set_index("timestamp").sort_index()
    if df.empty or df[["open", "close", "volume"]].isna().any().any() or (df[["open", "close", "volume"]] <= 0).any().any():
        raise ValueError(f"ETF data has missing or non-positive prices/volume: {path}")
    return df


def load_etf_prices(etf_name):
    df = load_etf_data(etf_name)
    return df["open"], df["close"]


def backtest_event_driven(strat, aum=5e8, fixed_bps=15, impact_k=500, capadv=0.25, slc=10,
                          rf=0.0, breaker_adv_cap=0.05, breaker_cost_bps=75, stagger=False):
    """Drop-in replacement for the live engine's backtest_event_driven(). Requires
    strat.positions already set. Returns (net_returns, turnover) exactly like the live
    engine; when a sweep is active, strat.cash_sweep_frac (the swept ETF's daily fraction
    of total equity) is also stashed on `strat` for inspection, mirroring how the live
    engine stashes strat.turnover_by_adv_tier."""
    etf_name = getattr(strat, "cash_sweep_etf", None)
    if etf_name is None:
        return _cash_backtest_event_driven(strat, aum=aum, fixed_bps=fixed_bps, impact_k=impact_k,
                                           capadv=capadv, slc=slc, rf=rf,
                                           breaker_adv_cap=breaker_adv_cap,
                                           breaker_cost_bps=breaker_cost_bps, stagger=stagger)

    if stagger:
        raise ValueError("stagger=True is not implemented for ETF sweep backtests")
    etf = load_etf_data(etf_name)
    WT = strat.positions
    if WT.index.min() < ETF_START_DATE[etf_name]:
        raise ValueError(
            f"cash_sweep_etf={etf_name!r} needs positions starting no earlier than "
            f"{ETF_START_DATE[etf_name].date()} (that ETF's own data start); got positions "
            f"from {WT.index.min().date()}. Call strat.get_positions(start=...) with a later "
            f"date, or set cash_sweep_etf=None.")

    net, turnover, etf_frac = _simulate_with_sweep(
        strat, WT, aum, fixed_bps, impact_k, capadv, slc, breaker_adv_cap, breaker_cost_bps,
        etf["open"], etf["close"], etf["volume"])
    strat.cash_sweep_frac = etf_frac
    return net, turnover


def _align_etf_prices(etf_open, etf_close, days, max_gap_days=7):
    """Use the previous close as a proxy for isolated missing ETF sessions.

    Never extrapolate beyond the last observation or bridge a long data outage.
    Using a proxy for an ETF conversion is an approximation, reported to the user.
    """
    missing = days.difference(etf_close.index)
    if len(days) == 0:
        raise ValueError("No simulated trading days")
    if days[0] < etf_close.index.min() or days[-1] > etf_close.index.max():
        raise ValueError("ETF data missing at the edge of the simulation; restrict the "
                         "dates to the ETF CSV's coverage")
    previous = etf_close.index.searchsorted(missing, side="right") - 1
    age = missing - etf_close.index[previous]
    if (previous < 0).any() or (age > pd.Timedelta(days=max_gap_days)).any():
        bad = missing[(previous < 0) | (age > pd.Timedelta(days=max_gap_days))]
        raise ValueError(f"ETF data missing for an extended period, starting {bad[0].date()}; "
                         "obtain the missing prices or use a contiguous report period")
    eo, ec = etf_open.reindex(days), etf_close.reindex(days)
    if len(missing):
        proxy = pd.Series(etf_close.reindex(missing, method="ffill").values, index=missing)
        eo.loc[missing] = proxy
        ec.loc[missing] = proxy
        print(f"[ETF data] {len(missing)} stock session(s) lack an ETF bar "
              f"(first {missing[0].date()}); prior ETF close used as an approximate "
              "valuation only; ETF trading is skipped on those sessions.")
    return eo, ec, missing


def _simulate_with_sweep(strat, WT, aum, fixed_bps, impact_k, capadv, slc,
                         breaker_adv_cap, breaker_cost_bps, etf_open, etf_close, etf_volume):
    """Long-only cash and ETF ledger; no trade executes without its own price bar.

    ETF purchases and sales use the same fixed/impact formula and daily ADV cap
    as stocks. Missing ETF sessions are valued at the previous close, but no ETF
    trade is executed on those sessions. Orders use whole stock and ETF units.
    """
    days, close, opn, tv, atr = strat.days, strat.close, strat.opn, strat.tv, strat.atr
    cff = close.ffill()
    prev_close = cff.shift(1)
    adv = tv.rolling(21, min_periods=10).median()
    prior_adv = adv.shift(1)
    etf_adv = (etf_close * etf_volume).rolling(21, min_periods=10).median().shift(1)
    positions = days.searchsorted(WT.index, side="right")
    fills = {days[p]: t for t, p in zip(WT.index, positions) if p < len(days)}
    if not fills:
        raise ValueError("No rebalance has a following trading session")
    idx = days[days >= min(fills)]
    etf_o, etf_c, missing = _align_etf_prices(etf_open, etf_close, idx)
    strat.cash_sweep_proxy_dates = missing
    etf_tradable = idx.isin(etf_open.index) & idx.isin(etf_volume.index)
    etf_adv_on_days = etf_adv.reindex(idx, method="ffill")

    shares = pd.Series(0.0, index=close.columns)
    peak = pd.Series(np.nan, index=close.columns)
    pending = pd.Series(0.0, index=close.columns)
    cash = float(aum)
    etf_shares = 0.0
    equity = pd.Series(index=idx, dtype=float)
    etf_value = pd.Series(index=idx, dtype=float)
    cash_values = pd.Series(index=idx, dtype=float)
    stock_turnover = etf_turnover = etf_costs = stock_costs = 0.0
    etf_buys = etf_sells = skipped_stock_fills = 0
    etf_trades = []
    strat.position_metadata = []
    entries = {}

    def stock_sale(symbol, qty, price, cost, day, reason):
        item = entries.get(symbol)
        if item is None or qty <= 0:
            return
        strat.position_metadata.append(dict(
            Ticker=symbol, Entry_Date=item["date"], Entry_Price=item["basis"],
            Exit_Date=day, Exit_Price=max(0.0, price - cost / qty),
            Weight=item["weight"], Quantity=qty, Exit_Reason=reason,
            Stop_Type="BREAKER" if reason == "STOP_HIT" else "",
            Min_Price=item["low"], Max_Price=item["high"]))

    for i, d in enumerate(idx):
        c = cff.loc[d]
        valid = opn.loc[d].notna() & (opn.loc[d] > 0) & close.loc[d].notna()
        mark = opn.loc[d].where(valid).fillna(prev_close.loc[d])
        eo, ec = float(etf_o.loc[d]), float(etf_c.loc[d])
        eadv = float(etf_adv_on_days.loc[d])
        can_trade_etf = bool(etf_tradable[i]) and np.isfinite(eadv) and eadv > 0
        etf_daily_remaining = capadv * eadv if can_trade_etf else 0.0

        def etf_trade(direction, desired):
            nonlocal cash, etf_shares, etf_daily_remaining, etf_turnover, etf_costs, etf_buys, etf_sells
            if desired <= 0 or etf_daily_remaining <= 0:
                return
            limit = min(etf_daily_remaining, etf_shares * eo) if direction == "sell" else etf_daily_remaining
            if limit <= 0:
                return
            def cost(value):
                return _transaction_cost(value, eadv, fixed_bps, impact_k, slc)
            # Solve for the gross order value given desired cash proceeds or budget.
            lo, hi = 0.0, limit
            for _ in range(45):
                mid = (lo + hi) / 2
                total = mid - cost(mid) if direction == "sell" else mid + cost(mid)
                if total <= desired:
                    lo = mid
                else:
                    hi = mid
            # Exchange orders use whole ETF units. Round purchases down and
            # sales up when possible so a sale can fund the intended stock buy.
            max_units = int(np.floor(limit / eo + 1e-10))
            if direction == "buy":
                units = min(max_units, int(np.floor(lo / eo + 1e-10)))
            else:
                units = min(max_units, int(np.ceil(lo / eo - 1e-10)))
            value = units * eo
            fee = cost(value)
            if value <= 1e-9 or (direction == "sell" and fee >= value):
                return
            if direction == "buy":
                cash -= value + fee
                etf_shares += value / eo
                etf_buys += 1
            else:
                cash += value - fee
                etf_shares -= value / eo
                etf_sells += 1
            etf_daily_remaining -= value
            etf_turnover += value
            etf_costs += fee
            etf_trades.append(dict(date=d, side=direction, value=value, cost=fee, price=eo))

        # The portfolio begins in cash; the first ETF purchase incurs its own cost.
        if i == 0:
            etf_trade("buy", cash)

        if pending.any():
            limit = (breaker_adv_cap * prior_adv.loc[d] / mark).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            sell = np.floor(pending.clip(upper=limit).where(valid, 0.0))
            sell_values = sell * mark
            fees = sell_values * (breaker_cost_bps / 1e4)
            for symbol, qty in sell[sell > 1e-12].items():
                stock_sale(symbol, float(qty), float(mark[symbol]), float(fees[symbol]), d, "STOP_HIT")
            cash += float(sell_values.sum() - fees.sum())
            stock_costs += float(fees.sum())
            stock_turnover += float(sell_values.sum())
            shares -= sell
            pending = (pending - sell).clip(lower=0.0)
            for symbol in sell[sell > 1e-12].index:
                if shares[symbol] <= 1e-9:
                    entries.pop(symbol, None)

        if d in fills:
            t = fills[d]
            target = WT.loc[t].copy()
            portfolio = cash + etf_shares * eo + float((shares * mark).sum())
            cur_weight = (shares * mark) / portfolio
            if strat.drift_band > 0:
                hold = (cur_weight > 1e-9) & (target > 1e-9) & ((target - cur_weight).abs() <= strat.drift_band)
                target = target.where(~hold, cur_weight)
            target_shares = ((target * portfolio) / mark).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            delta = target_shares - shares
            limit = (capadv * adv.loc[t] / mark).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            delta = np.trunc(delta.clip(lower=-limit, upper=limit))
            skipped_stock_fills += int(((delta.abs() > 1e-9) & ~valid).sum())
            delta = delta.where(valid & (pending <= 0), 0.0)
            sells = delta.clip(upper=0)
            sell_values = (-sells * mark).fillna(0.0)
            sell_part = (sell_values / adv.loc[t]).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            sell_fees = sell_values * (fixed_bps / 1e4 + impact_k / 1e4 * sell_part / slc)
            for symbol, qty in (-sells[sells < -1e-12]).items():
                stock_sale(symbol, float(qty), float(mark[symbol]), float(sell_fees[symbol]), d, "REBALANCE")
            cash += float(sell_values.sum() - sell_fees.sum())
            stock_costs += float(sell_fees.sum())
            stock_turnover += float(sell_values.sum())
            shares += sells
            for symbol in sells[sells < -1e-12].index:
                if shares[symbol] <= 1e-9:
                    entries.pop(symbol, None)

            buys = delta.clip(lower=0)
            buy_need = float((buys * mark).sum()) + _stock_trade_cost(buys, mark, adv.loc[t], fixed_bps, impact_k, slc)
            etf_trade("sell", max(0.0, buy_need - cash))
            buys = _scale_stock_buys_to_budget(buys, mark, adv.loc[t], cash, fixed_bps, impact_k, slc)
            buy_values = (buys * mark).fillna(0.0)
            buy_part = (buy_values / adv.loc[t]).replace([np.inf, -np.inf], np.nan).fillna(0.0)
            buy_fees = buy_values * (fixed_bps / 1e4 + impact_k / 1e4 * buy_part / slc)
            for symbol, qty in buys[buys > 1e-12].items():
                old_qty = float(shares[symbol])
                price = float(mark[symbol])
                basis = price + float(buy_fees[symbol]) / float(qty)
                if symbol in entries and old_qty > 1e-9:
                    item = entries[symbol]
                    item["basis"] = (item["basis"] * old_qty + basis * qty) / (old_qty + qty)
                else:
                    entries[symbol] = dict(date=d, basis=basis, weight=float(target[symbol]), low=price, high=price)
                    peak[symbol] = price
            cash -= float(buy_values.sum() + buy_fees.sum())
            stock_costs += float(buy_fees.sum())
            stock_turnover += float(buy_values.sum())
            shares += buys

        # Sweep any residual cash only at a real ETF open, once stock orders finish.
        etf_trade("buy", max(0.0, cash))
        for symbol, item in entries.items():
            lo = strat.low.loc[d, symbol] if not strat.low.empty else c[symbol]
            hi = strat.high.loc[d, symbol] if not strat.high.empty else c[symbol]
            if pd.notna(lo) and lo > 0:
                item["low"] = min(item["low"], float(lo))
            if pd.notna(hi) and hi > 0:
                item["high"] = max(item["high"], float(hi))
        held = shares > 1e-9
        peak = peak.mask(held & ((c > peak) | peak.isna()), c)
        triggered = pd.Series(False, index=close.columns)
        if strat.breaker is not None:
            triggered |= held & (c < peak * (1 - strat.breaker)) & (pending <= 0)
        if strat.atr_k is not None:
            triggered |= held & (c < peak - strat.atr_k * atr.loc[d]) & (pending <= 0)
        pending += shares.where(triggered, 0.0)
        if cash < -1e-6 or etf_shares < -1e-8:
            raise RuntimeError(f"Negative cash or ETF position on {d.date()}")
        cash = max(cash, 0.0)
        etf_shares = max(etf_shares, 0.0)
        etf_value.loc[d] = etf_shares * ec
        cash_values.loc[d] = cash
        equity.loc[d] = cash + etf_value.loc[d] + float((shares * c).sum())

    for symbol, item in entries.items():
        stock_sale(symbol, float(shares[symbol]), float(cff.loc[idx[-1], symbol]), 0.0, idx[-1], "END_OF_PERIOD")
    net = equity.pct_change()
    net.iloc[0] = equity.iloc[0] / aum - 1.0
    strat.cash_sweep_cash = cash_values
    strat.cash_sweep_trades = pd.DataFrame(etf_trades, columns=["date", "side", "value", "cost", "price"])
    strat.cash_sweep_costs = dict(etf=etf_costs, stock=stock_costs, etf_buy_orders=etf_buys,
                                  etf_sell_orders=etf_sells, etf_turnover=etf_turnover,
                                  skipped_stock_fills=skipped_stock_fills)
    yrs = max((idx[-1] - idx[0]).days / 365.2425, 1 / strat.trading_days)
    return net, (stock_turnover + etf_turnover) / equity.mean() / yrs, etf_value / equity

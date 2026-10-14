"""
csm_sector_rotation_backtest.py
================================
Backtest engine, metrics, reporting and trade log for CSMSectorRotation.

Everything that operates ON a strategy object but is not part of the strategy
CORE (which lives in csm_sector_rotation_strategy.py) — same Tier-1/Tier-2
split as csm_batch_strategy.py / csm_batch_backtest.py. The daily event loop
(STEP C/E/F/G/H/I) is a verbatim port of csm_batch_backtest.py's
_run_backtest_core — same proven mechanics (Crash Guard, per-stock stops,
rebalance/rank-decay exits, in-loop Corr Guard + Vol Targeting, entry/exit-day
return patching for equity-curve/trade-log consistency). Only the class being
driven is different.

All functions take the strategy object as the first argument `strat`.
"""

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
# TRADE RECORDING
# ══════════════════════════════════════════════════════════════════════════════

def _record_closed_trade(strat, ticker, holding, exit_date,
                          exit_price, fill_price, exit_reason,
                          stop_price_at_exit):
    """Append one trade record to strat.position_metadata."""
    self = strat
    entry_price  = holding['entry_price']
    entry_date   = holding['entry_date']
    peak_price   = holding['peak_price']
    stop_pct     = holding.get('stop_pct',     np.nan)
    atr_at_entry = holding.get('atr_at_entry', np.nan)
    weight       = holding.get('weight',        0.0)
    min_price    = holding.get('min_price',     entry_price)
    max_price    = holding.get('max_price',     entry_price)

    _stop_reasons = {'STOP_HIT', 'CRASH_GUARD'}
    actual_fill = fill_price if exit_reason in _stop_reasons else exit_price

    mae_pct = ((min_price / entry_price) - 1) * 100 if (entry_price and entry_price > 0) else np.nan
    mfe_pct = ((max_price / entry_price) - 1) * 100 if (entry_price and entry_price > 0) else np.nan

    self.position_metadata.append({
        'Ticker'            : ticker,
        'Entry_Date'        : entry_date,
        'Entry_Price'       : round(entry_price,       4) if pd.notna(entry_price)       else np.nan,
        'Exit_Date'         : exit_date,
        'Exit_Price'        : round(actual_fill,       4) if pd.notna(actual_fill)       else np.nan,
        'Close_At_Exit'     : round(exit_price,        4) if pd.notna(exit_price)        else np.nan,
        'Peak_Price'        : round(peak_price,        4) if pd.notna(peak_price)        else np.nan,
        'Stop_Price_At_Exit': round(stop_price_at_exit,4) if pd.notna(stop_price_at_exit) else np.nan,
        'Stop_Pct'          : round(stop_pct * 100,    2) if pd.notna(stop_pct)          else np.nan,
        'ATR_At_Entry'      : round(atr_at_entry,      4) if pd.notna(atr_at_entry)      else np.nan,
        'Exit_Reason'       : exit_reason,
        'Weight'            : round(weight,             6),
        'MAE_Pct'           : round(mae_pct,            2) if pd.notna(mae_pct)           else np.nan,
        'MFE_Pct'           : round(mfe_pct,            2) if pd.notna(mfe_pct)           else np.nan,
    })


# ══════════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN BACKTEST ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def _run_backtest_core(
    strat,
    initial_capital:   float,
    transaction_cost:  float,
    risk_free_rate:    float,
    label:             str   = "Event-Driven",
) -> dict:
    """Core event-driven daily loop. Vol Targeting and Correlation Guard run
    inside the loop using rolling windows over past data only."""
    self = strat
    if self.positions is None:
        raise ValueError("Call get_positions() first.")

    print("\n" + "=" * 65)
    print(f"[CSM Sector Rotation]  {label} Backtest starting")
    print("=" * 65)
    print(f"  Capital        : Rs {initial_capital:,.0f}")
    print(f"  Txn cost       : {transaction_cost*100:.3f}% one-way")
    print(f"  RFR            : {risk_free_rate*100:.1f}% p.a.")
    print(f"  Stop (entry)   : -{self.hard_stop_from_entry*100:.0f}%  [Layer 2]")
    print(f"  Stop (peak)    : -{self.hard_stop_from_peak*100:.0f}%  [Layer 3]"
          f"  (trailing={'ON' if self.use_trailing_stop else 'OFF'})")
    print(f"  Crash Guard    : {'ON' if self.use_crash_guard else 'OFF'}"
          f"  cooldown={self.crash_guard_cooldown} days")
    print(f"  Corr Guard     : threshold={self.corr_guard_threshold}")
    print(f"  Stop cooldown  : {self.stop_cooldown_days} days per ticker after STOP_HIT")
    print(f"  Min hold       : {self.min_hold_days} days before stop can fire")
    print(f"  Vol target     : {self.vol_target*100:.0f}%  (de-leverage only)")
    print("=" * 65)

    prices_ff  = self._prices_ff
    opens_ff   = self._opens_ff
    open_proxy = self._open_proxy
    highs_ff   = self.highs.ffill() if not self.highs.empty else prices_ff.copy()
    lows_ff    = self.lows.ffill()  if not self.lows.empty  else prices_ff.copy()

    if not self.highs.empty and not self.lows.empty:
        is_circuit_ff = (highs_ff == lows_ff)
    else:
        is_circuit_ff = pd.DataFrame(False, index=prices_ff.index, columns=prices_ff.columns)

    _dr_all = self.prices.pct_change(fill_method=None).fillna(0.0)

    if self.benchmark is not None and self.use_crash_guard:
        if self._panic_threshold_series is not None:
            bvol_daily  = self._bvol_daily.reindex(self.prices.index).ffill()
            _expand_thr = self._panic_threshold_series.reindex(self.prices.index).ffill()
            is_panic    = (bvol_daily > _expand_thr).fillna(False)
        else:
            is_panic = pd.Series(False, index=self.prices.index)
    else:
        is_panic = pd.Series(False, index=self.prices.index)

    if self.benchmark is not None and self._panic_threshold_series is not None:
        _bench_vol_75 = self._bvol_daily.reindex(self.prices.index).ffill()
        _expand_75 = (
            _bench_vol_75.expanding(min_periods=63).quantile(0.75).shift(1).ffill()
        )
        is_high_vol = (_bench_vol_75 > _expand_75).fillna(False)
    else:
        is_high_vol = pd.Series(False, index=self.prices.index)

    monthly_signal = (
        self.positions
        .reindex(self.prices.index, method='ffill')
        .shift(1)
        .fillna(0.0)
    )

    rank_exit_daily = None
    _rxm = getattr(self, 'rank_exit_mask', None)
    if _rxm is not None and not _rxm.empty:
        rank_exit_daily = (_rxm.reindex(self.prices.index, method='ffill')
                           .shift(1).fillna(False))

    active_holdings:        dict = {}
    stop_cooldown_tickers:  dict = {}
    executed_weights_list        = []
    self.position_metadata       = []
    self._backtest_initial_capital = initial_capital

    atr_daily = (
        self.atr.reindex(self.prices.index) if self.atr is not None else None
    )

    n_stop, n_crash, n_rebalance, n_rank_exit = 0, 0, 0, 0
    cg_cooldown_remaining: int   = 0
    daily_rfr = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0

    _port_ret_buf:  list = []
    _stock_ret_buf: list = []
    _weight_buf:    list = []
    VOL_WIN  = 21
    CORR_WIN = 21

    for i, date in enumerate(self.prices.index):

        if i == 0:
            _zero_w = pd.Series(0.0, index=self.prices.columns)
            executed_weights_list.append(_zero_w)
            _port_ret_buf.append(0.0)
            _weight_buf.append(_zero_w)
            _stock_ret_buf.append(_dr_all.iloc[0])
            continue

        prev_weights   = executed_weights_list[i - 1]
        prev_held      = set(prev_weights.index[prev_weights > 1e-6])
        target_weights = monthly_signal.iloc[i].copy()
        exited_today: set = set()

        # ── STEP C: Crash Guard ───────────────────────────────────────────
        in_panic = is_panic.iloc[i]
        if self.use_crash_guard and in_panic:
            for stock in prev_held:
                _close = float(prices_ff.at[date, stock])
                _fill  = float(opens_ff.at[date, stock])
                if pd.isna(_fill) or _fill <= 0:
                    _fill = _close
                _h = active_holdings.get(stock, {})
                _record_closed_trade(
                    self, ticker=stock, holding=_h, exit_date=date,
                    exit_price=_close, fill_price=_fill,
                    exit_reason='CRASH_GUARD', stop_price_at_exit=_h.get('atr_stop', np.nan),
                )
                exited_today.add(stock)
                n_crash += 1
            active_holdings.clear()
            target_weights[:] = 0.0
            cg_cooldown_remaining = self.crash_guard_cooldown
            stop_cooldown_tickers.clear()
            for _cg_stock in exited_today:
                stop_cooldown_tickers[_cg_stock] = date
            _zero_w = target_weights.copy()
            executed_weights_list.append(_zero_w)
            _port_ret_buf.append(0.0)
            _weight_buf.append(_zero_w)
            _stock_ret_buf.append(_dr_all.loc[date])
            continue

        if cg_cooldown_remaining > 0:
            cg_cooldown_remaining -= 1
            for stock in list(target_weights.index):
                if stock not in prev_held and target_weights[stock] > 1e-6:
                    target_weights[stock] = 0.0

        # ── STEP E: Daily stop check ──────────────────────────────────────
        for stock in prev_held:
            if stock in exited_today or stock not in active_holdings:
                continue

            today_close = float(prices_ff.at[date, stock])
            today_low   = float(lows_ff.at[date, stock])
            today_high  = float(highs_ff.at[date, stock])
            today_open  = float(opens_ff.at[date, stock])
            if pd.isna(today_open) or today_open <= 0:
                today_open = float(open_proxy.at[date, stock])

            if pd.isna(today_close) or today_close <= 0:
                continue

            curr_atr = np.nan
            if atr_daily is not None and stock in atr_daily.columns:
                curr_atr = float(atr_daily.at[date, stock])
            if pd.isna(curr_atr) or curr_atr <= 0:
                curr_atr = today_close * 0.02

            _entry_date = active_holdings[stock].get('entry_date', date)
            _days_held  = (date - _entry_date).days

            should_exit, fill_px, stop_lvl, updated_h = self._check_stop_exit(
                stock, today_close, today_low, curr_atr, today_open,
                active_holdings[stock], curr_high=today_high,
                high_vol=bool(is_high_vol.iloc[i]),
            )
            if _days_held < self.min_hold_days:
                should_exit = False

            if should_exit and stock in is_circuit_ff.columns \
                    and bool(is_circuit_ff.at[date, stock]):
                should_exit = False

            if should_exit:
                _record_closed_trade(
                    self, ticker=stock, holding=active_holdings[stock], exit_date=date,
                    exit_price=today_close, fill_price=fill_px,
                    exit_reason='STOP_HIT', stop_price_at_exit=stop_lvl,
                )
                del active_holdings[stock]
                target_weights[stock] = 0.0
                exited_today.add(stock)
                n_stop += 1
                stop_cooldown_tickers[stock] = date
            else:
                _low  = today_low  if (not pd.isna(today_low)  and today_low  > 0) else today_close
                _high = today_high if (not pd.isna(today_high) and today_high > 0) else today_close
                updated_h['min_price'] = min(updated_h.get('min_price', today_close), _low)
                updated_h['max_price'] = max(updated_h.get('max_price', today_close), _high)
                active_holdings[stock] = updated_h

        # ── STEP F: Rebalance exits ───────────────────────────────────────
        current_held = set(target_weights.index[target_weights > 1e-6])
        for stock in prev_held:
            if stock in current_held or stock in exited_today:
                continue
            if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                target_weights[stock] = float(prev_weights.get(stock, 0.0))
                continue
            _close = float(prices_ff.at[date, stock])
            _fill  = float(opens_ff.at[date, stock])
            if pd.isna(_fill) or _fill <= 0:
                _fill = _close
            _h    = active_holdings.pop(stock, {})
            _is_rank = (rank_exit_daily is not None and stock in rank_exit_daily.columns
                        and bool(rank_exit_daily.at[date, stock]))
            _reason = 'RANK_EXIT' if _is_rank else 'REBALANCE'
            _record_closed_trade(
                self, ticker=stock, holding=_h, exit_date=date,
                exit_price=_close, fill_price=_fill,
                exit_reason=_reason, stop_price_at_exit=_h.get('atr_stop', np.nan),
            )
            exited_today.add(stock)
            if _is_rank:
                n_rank_exit += 1
            else:
                n_rebalance += 1

        # ── STEP G: New entries ───────────────────────────────────────────
        for stock in list(current_held):
            if stock not in prev_held:
                if stock in exited_today:
                    target_weights[stock] = 0.0
                    continue
                if stock in stop_cooldown_tickers:
                    _gap = (date - stop_cooldown_tickers[stock]).days
                    if _gap < self.stop_cooldown_days:
                        target_weights[stock] = 0.0
                        continue
                    else:
                        del stop_cooldown_tickers[stock]
                if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                    target_weights[stock] = 0.0
                    continue

                _ep_open  = float(opens_ff.at[date, stock])
                _ep_close = float(prices_ff.at[date, stock])
                _ep = _ep_open if (_ep_open > 0 and not pd.isna(_ep_open)) else _ep_close

                _atr_entry = np.nan
                if atr_daily is not None and stock in atr_daily.columns:
                    _atr_entry = float(atr_daily.at[date, stock])
                if self.use_trailing_stop and not pd.isna(_atr_entry) and _atr_entry > 0:
                    raw_dist  = self.atr_multiplier * _atr_entry
                    stop_dist = float(np.clip(raw_dist, 0.03 * _ep, 0.30 * _ep))
                else:
                    stop_dist = self.hard_stop_from_entry * _ep
                initial_atr_stop = max(
                    _ep - stop_dist,
                    _ep * (1.0 - self.hard_stop_from_entry),
                    _ep * (1.0 - self.hard_stop_from_peak),
                )
                active_holdings[stock] = {
                    'entry_date'  : date,
                    'entry_price' : _ep,
                    'peak_price'  : _ep,
                    'atr_stop'    : initial_atr_stop,
                    'stop_pct'    : stop_dist / _ep,
                    'atr_at_entry': _atr_entry,
                    'weight'      : float(target_weights.get(stock, 0.0)),
                    'min_price'   : _ep,
                    'max_price'   : _ep,
                }

        # ── STEP H: Sync weight into active_holdings ──────────────────────
        current_held = set(target_weights.index[target_weights > 1e-6])
        for stock in current_held:
            if stock in active_holdings:
                active_holdings[stock]['weight'] = float(target_weights.get(stock, 0.0))
        for _stk in list(active_holdings.keys()):
            if _stk not in current_held:
                del active_holdings[_stk]

        # ── STEP I: In-loop Vol Targeting & Corr Guard ────────────────────
        raw_weights = target_weights.copy()

        _gross = float(raw_weights.sum())
        if _gross > 1.0:
            raw_weights = raw_weights / _gross

        corr_scale = 1.0
        if len(_port_ret_buf) >= CORR_WIN:
            _pbuf   = np.array(_port_ret_buf[-CORR_WIN:])
            _p_vol  = float(_pbuf.std())
            _pw     = _weight_buf[-1]
            _w_sum  = float(_pw.sum())
            if _w_sum > 0 and _p_vol > 0:
                _hist_start = max(0, i - CORR_WIN)
                _s_std = _dr_all.iloc[_hist_start:i].std()
                _avg_s_vol = float((_s_std * _pw).sum() / _w_sum)
                if _avg_s_vol > 0 and (_p_vol / _avg_s_vol) > self.corr_guard_threshold:
                    corr_scale = 0.5

        vol_scale = 1.0
        if len(_port_ret_buf) >= VOL_WIN:
            _win = _port_ret_buf[-63:] if len(_port_ret_buf) >= 63 else _port_ret_buf[-VOL_WIN:]
            _rv  = float(np.std(_win)) * np.sqrt(252)
            if _rv > 0:
                vol_scale = min(1.0, self.vol_target / _rv)

        scaled_weights = raw_weights * (corr_scale * vol_scale)
        executed_weights_list.append(scaled_weights.copy())

        _dr_today = _dr_all.loc[date]
        _gross_pos_ret = float((raw_weights * _dr_today).sum())
        _port_ret_buf.append(_gross_pos_ret)
        _weight_buf.append(scaled_weights.copy())
        _stock_ret_buf.append(_dr_today)

    # ── Close positions still open at end of period ───────────────────────
    _last_date = self.prices.index[-1]
    for stock, _h in active_holdings.items():
        _close = float(prices_ff.at[_last_date, stock])
        _fill  = float(opens_ff.at[_last_date, stock])
        if pd.isna(_fill) or _fill <= 0:
            _fill = _close
        _record_closed_trade(
            self, ticker=stock, holding=_h, exit_date=_last_date,
            exit_price=_close, fill_price=_fill,
            exit_reason='END_OF_PERIOD', stop_price_at_exit=_h.get('atr_stop', np.nan),
        )
    active_holdings.clear()
    self._prices_ff_backtest = prices_ff

    print(f"\n[{label}] Stop exits    : {n_stop}")
    print(f"[{label}] Crash Guard   : {n_crash}")
    print(f"[{label}] Rebal exits   : {n_rebalance}")
    print(f"[{label}] Rank exits    : {n_rank_exit}")

    executed_weights = pd.DataFrame(
        executed_weights_list, index=self.prices.index
    ).fillna(0.0)

    # ── Entry/exit-day return patching so equity curve matches trade log ───
    _dr          = _dr_all.copy()
    _prev_close  = prices_ff.shift(1)
    _prev_exec_w = executed_weights.shift(1).fillna(0.0)
    for meta in self.position_metadata:
        ticker     = meta['Ticker']
        entry_date = meta['Entry_Date']
        entry_open = meta['Entry_Price']
        if (ticker not in _dr.columns or entry_date not in _dr.index
                or pd.isna(entry_open) or entry_open <= 0):
            continue
        close_e = float(prices_ff.at[entry_date, ticker])
        if pd.isna(close_e) or close_e <= 0:
            continue
        _dr.at[entry_date, ticker] = close_e / entry_open - 1.0

    _exit_adj = pd.Series(0.0, index=self.prices.index)
    for meta in self.position_metadata:
        ticker    = meta['Ticker']
        exit_date = meta['Exit_Date']
        exit_fill = meta['Exit_Price']
        if ticker not in self.prices.columns or exit_date not in self.prices.index:
            continue
        if pd.isna(exit_fill) or exit_fill <= 0:
            continue
        pc = float(_prev_close.at[exit_date, ticker])
        if pd.isna(pc) or pc <= 0:
            continue
        prev_w = float(_prev_exec_w.at[exit_date, ticker])
        if prev_w <= 1e-9:
            continue
        _exit_adj.at[exit_date] += prev_w * (exit_fill / pc - 1.0)

    gross_eq_ret    = (executed_weights * _dr).sum(axis=1) + _exit_adj
    total_w         = executed_weights.sum(axis=1)
    cash_w          = (1.0 - total_w).clip(lower=0.0)
    cash_ret        = cash_w * daily_rfr
    w_chg           = executed_weights.diff().abs().sum(axis=1)
    txn_cost        = w_chg * transaction_cost
    net_returns     = gross_eq_ret + cash_ret - txn_cost

    equity_curve    = (1.0 + net_returns).cumprod()
    portfolio_value = equity_curve * initial_capital

    n_years  = (equity_curve.index[-1] - equity_curve.index[0]).days / 365.25
    cagr     = (equity_curve.iloc[-1]) ** (1.0 / n_years) - 1.0 if n_years > 0 else 0.0
    ann_vol  = net_returns.std() * np.sqrt(252)

    _excess  = net_returns - daily_rfr
    sharpe   = (np.sqrt(252) * _excess.mean() / net_returns.std()
                if net_returns.std() > 0 else 0.0)
    _dn      = net_returns.clip(upper=0.0)
    _dndev   = np.sqrt((_dn ** 2).mean())
    sortino  = (np.sqrt(252) * net_returns.mean() / _dndev if _dndev > 0 else 0.0)

    _rmax    = equity_curve.cummax()
    _dd      = (equity_curve / _rmax) - 1.0
    max_dd   = _dd.min()
    avg_dd   = _dd.mean()
    calmar   = cagr / abs(max_dd) if max_dd != 0 else 0.0

    _mret    = portfolio_value.resample('ME').last().pct_change().dropna()
    win_rate = (_mret > 0).mean()
    ann_turn = w_chg.sum() / n_years if n_years > 0 else 0.0
    _pos_diff_events = (self.positions.diff().abs() > 1e-4).sum(axis=1).sum()
    sig_turn = (_pos_diff_events / 2.0) / n_years if n_years > 0 else 0.0

    self.results = {
        'equity_curve'       : equity_curve,
        'portfolio_value'    : portfolio_value,
        'net_returns'        : net_returns,
        'executed_weights'   : executed_weights,
        'turnover'           : w_chg,
        'total_return'       : float(equity_curve.iloc[-1] - 1.0),
        'cagr'               : cagr,
        'sharpe'             : sharpe,
        'sortino'            : sortino,
        'calmar'             : calmar,
        'max_drawdown'       : max_dd,
        'avg_drawdown'       : avg_dd,
        'ann_volatility'     : ann_vol,
        'win_rate'           : win_rate,
        'ann_turnover'       : ann_turn,
        'ann_signal_turnover': sig_turn,
        'n_stop'             : n_stop,
        'n_crash'            : n_crash,
        'n_rebalance'        : n_rebalance,
        'n_rank_exit'        : n_rank_exit,
    }

    print(f"\n[{label}] CAGR={cagr*100:.2f}%  Sharpe={sharpe:.2f}  "
          f"MaxDD={max_dd*100:.2f}%  AvgDD={avg_dd*100:.2f}%  Calmar={calmar:.2f}")
    return self.results


def backtest_event_driven(
    strat,
    initial_capital  = 100_000.0,
    transaction_cost = 0.001,
    risk_free_rate   = 0.06,
):
    """Event-driven backtest — all overlays applied inside the loop using
    past data only. No post-loop vectorised pass."""
    return _run_backtest_core(
        strat,
        initial_capital   = initial_capital,
        transaction_cost  = transaction_cost,
        risk_free_rate    = risk_free_rate,
        label             = "Event-Driven",
    )


# ══════════════════════════════════════════════════════════════════════════════
# TRADE LOG
# ══════════════════════════════════════════════════════════════════════════════

def get_trade_log(strat):
    """Build a trade-log DataFrame from strat.position_metadata. Must be
    called after backtest_event_driven()."""
    self = strat
    if not self.position_metadata:
        print("Warning: No trade metadata. Run backtest_event_driven() first.")
        return pd.DataFrame()

    equity_curve     = self.results['equity_curve']     if self.results else None
    executed_weights = self.results['executed_weights'] if self.results else None
    prices_ffill     = self.prices.ffill()

    rows = []
    for meta in self.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        exit_date   = meta['Exit_Date']
        entry_price = meta['Entry_Price']
        exit_price  = meta['Exit_Price']

        if pd.isna(exit_price) and ticker in prices_ffill.columns:
            exit_price = (prices_ffill.at[exit_date, ticker]
                          if exit_date in prices_ffill.index
                          else prices_ffill[ticker].iloc[-1])

        weight = meta['Weight']
        if executed_weights is not None and ticker in executed_weights.columns:
            ew_col  = executed_weights[ticker]
            window  = ew_col.loc[(ew_col.index > entry_date) & (ew_col.index <= exit_date)]
            nonzero = window[window > 1e-9]
            if not nonzero.empty:
                weight = float(nonzero.iloc[0])

        port_val = np.nan
        if equity_curve is not None:
            future_idx = equity_curve.index[equity_curve.index > entry_date]
            if len(future_idx) > 0:
                port_val = float(equity_curve.loc[future_idx[0]])

        qty = np.nan
        if pd.notna(entry_price) and entry_price > 0 and pd.notna(port_val) and weight > 0:
            qty = (weight * port_val) / entry_price

        pnl_pct = ((exit_price / entry_price) - 1) * 100 \
                  if (pd.notna(entry_price) and entry_price > 0
                      and pd.notna(exit_price) and exit_price > 0) else np.nan

        pnl_abs = qty * (exit_price - entry_price) \
                  if (pd.notna(qty) and pd.notna(entry_price)
                      and pd.notna(exit_price)) else np.nan

        holding_days = max((exit_date - entry_date).days, 1)

        _win = (pd.notna(pnl_pct) and pnl_pct > 0)
        if meta['Exit_Reason'] == 'STOP_HIT':
            _sp  = meta.get('Stop_Price_At_Exit', np.nan)
            _eh  = (entry_price * (1.0 - self.hard_stop_from_entry)
                    if (pd.notna(entry_price) and entry_price > 0) else np.nan)
            _above_hard = (pd.notna(_sp) and pd.notna(_eh) and _sp > _eh + 1e-6)
            if _above_hard and self.use_trailing_stop:
                _stop_type, _exit_detail = 'TRAILING', ('TRAILING_WIN' if _win else 'TRAILING_LOSS')
            else:
                _stop_type, _exit_detail = 'STOP_LOSS', 'STOP_LOSS'
        else:
            _stop_type   = ''
            _exit_detail = meta['Exit_Reason'] + ('_WIN' if _win else '_LOSS')

        rows.append({
            'Ticker'            : ticker,
            'Entry_Date'        : entry_date,
            'Entry_Price'       : entry_price,
            'Exit_Date'         : exit_date,
            'Exit_Price'        : round(exit_price,              4) if pd.notna(exit_price)              else np.nan,
            'Close_At_Exit'     : meta.get('Close_At_Exit',      np.nan),
            'Peak_Price'        : meta.get('Peak_Price',         np.nan),
            'Stop_Price_At_Exit': meta.get('Stop_Price_At_Exit', np.nan),
            'Stop_Pct'          : meta.get('Stop_Pct',           np.nan),
            'ATR_At_Entry'      : meta.get('ATR_At_Entry',       np.nan),
            'Exit_Reason'       : meta['Exit_Reason'],
            'Stop_Type'         : _stop_type,
            'Exit_Detail'       : _exit_detail,
            'Weight'            : round(weight,                   6),
            'Quantity'          : round(qty,                      4) if pd.notna(qty)     else np.nan,
            'Position_Size'     : round(weight * port_val,        2) if (pd.notna(port_val) and weight > 0) else 0.0,
            'Portfolio Value'   : round(port_val, 2) if pd.notna(port_val) else np.nan,
            'PnL_Pct'           : round(pnl_pct,                  4) if pd.notna(pnl_pct) else np.nan,
            'PnL_Abs'           : round(pnl_abs,                  2) if pd.notna(pnl_abs) else np.nan,
            'Holding_Days'      : holding_days,
            'MAE_Pct'           : meta.get('MAE_Pct',             np.nan),
            'MFE_Pct'           : meta.get('MFE_Pct',             np.nan),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values('Entry_Date').reset_index(drop=True)
        df.index += 1
        df.index.name = 'Trade_ID'

        wins   = (df['PnL_Pct'] > 0).sum()
        losses = (df['PnL_Pct'] < 0).sum()
        total  = len(df)
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {losses}"
              f" | Win Rate: {wins/total*100:.1f}%")
        print(f"[Trade Log] Worst trade: {df['PnL_Pct'].min():.2f}%"
              f"  Best trade: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Avg holding days: {df['Holding_Days'].mean():.1f}"
              f"  (median {df['Holding_Days'].median():.0f})")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
    return df


def print_exit_breakdown(trade_log):
    """Per-exit-reason WIN/LOSS breakdown with within-reason win rate,
    average trade P&L, and equity-contribution share."""
    if trade_log is None or trade_log.empty:
        print("\n-- Exit Breakdown -- no trades --")
        return

    df = trade_log.copy()
    if 'Exit_Detail' not in df.columns:
        df['Exit_Detail'] = df['Exit_Reason'] + np.where(df['PnL_Pct'] > 0, '_WIN', '_LOSS')
    df['_c'] = df['Weight'] * df['PnL_Pct']
    tot = df['_c'].sum() or 1.0

    print(f"\n-- Exit Breakdown -- by reason & outcome --")
    print(f"  {'bucket':<22}{'n':>6}{'win%':>8}{'avgP&L':>9}{'%ofP&L':>9}")
    print(f"  {'-' * 55}")
    fam_order = ['STOP_HIT', 'REBALANCE', 'RANK_EXIT', 'CRASH_GUARD', 'END_OF_PERIOD']
    sub_order = {
        'STOP_HIT'     : ['TRAILING_WIN', 'TRAILING_LOSS', 'STOP_LOSS'],
        'REBALANCE'    : ['REBALANCE_WIN', 'REBALANCE_LOSS'],
        'RANK_EXIT'    : ['RANK_EXIT_WIN', 'RANK_EXIT_LOSS'],
        'CRASH_GUARD'  : ['CRASH_GUARD_WIN', 'CRASH_GUARD_LOSS'],
        'END_OF_PERIOD': ['END_OF_PERIOD_WIN', 'END_OF_PERIOD_LOSS'],
    }
    fams = fam_order + [r for r in df['Exit_Reason'].unique() if r not in fam_order]
    for fam in fams:
        sub = df[df['Exit_Reason'] == fam]
        if sub.empty:
            continue
        label = 'STOP_HIT (all stops)' if fam == 'STOP_HIT' else fam
        print(f"  {label:<22}{len(sub):>6}{(sub['PnL_Pct'] > 0).mean() * 100:>7.1f}%"
              f"{sub['PnL_Pct'].mean():>8.2f}%{sub['_c'].sum() / tot * 100:>8.1f}%")
        details = sub_order.get(fam, sorted(sub['Exit_Detail'].dropna().unique()))
        for d in details:
            s = sub[sub['Exit_Detail'] == d]
            if s.empty:
                continue
            print(f"    L {d:<18}{len(s):>6}{(s['PnL_Pct'] > 0).mean() * 100:>7.1f}%"
                  f"{s['PnL_Pct'].mean():>8.2f}%{s['_c'].sum() / tot * 100:>8.1f}%")
    print(f"  {'-' * 55}")


# ══════════════════════════════════════════════════════════════════════════════
# REPORT
# ══════════════════════════════════════════════════════════════════════════════

def print_report(strat):
    """Print a compact headline performance report from strat.results."""
    r = strat.results
    if not r:
        print("No results — run backtest_event_driven() first.")
        return
    print("\n" + "=" * 65)
    print("PERFORMANCE REPORT — CSM Sector Rotation")
    print("=" * 65)
    print(f"  Total Return     : {r['total_return']*100:.2f}%")
    print(f"  CAGR             : {r['cagr']*100:.2f}%")
    print(f"  Ann. Volatility  : {r['ann_volatility']*100:.2f}%")
    print(f"  Sharpe           : {r['sharpe']:.2f}")
    print(f"  Sortino          : {r['sortino']:.2f}")
    print(f"  Calmar           : {r['calmar']:.2f}")
    print(f"  Max Drawdown     : {r['max_drawdown']*100:.2f}%")
    print(f"  Avg Drawdown     : {r['avg_drawdown']*100:.2f}%")
    print(f"  Win Rate (mo.)   : {r['win_rate']*100:.1f}%")
    print(f"  Ann. Turnover    : {r['ann_turnover']*100:.1f}%")
    print(f"  Exit mix         : stop={r['n_stop']}  rebal={r['n_rebalance']}"
          f"  rank_exit={r['n_rank_exit']}  crash={r['n_crash']}")
    print("=" * 65)

"""
csm_batch_backtest.py
=====================
Backtest engine, metrics, reporting, IC analytics and plots for the
Cross-Sectional Momentum Batch Strategy (CrossSectionalMomentum).

This module holds everything that operates ON a strategy object but is not part
of the strategy CORE (which lives in csm_batch_strategy.py):

  • Event-driven backtest engine   — _run_backtest_core(strat, ...)
  • Public wrapper                 — backtest_event_driven
  • Trade recording + trade log    — _record_closed_trade, get_trade_log
  • Metrics + reporting            — slice_results, populate_trade_stats, print_report
  • Drawdown / yearly diagnostics  — compute_yearly_table, print_yearly_performance
  • Information Coefficient         — calculate_ic, calculate_realized_ic, plot_ic
  • Performance plots              — plot_performance

All functions take the strategy object as the first argument `strat`; moved
class methods alias `self = strat` at the top so their bodies are preserved
verbatim. The strategy must already have had calculate_factors() and
get_positions() called on it before the engine is invoked.

NEW (vs csm_stock_strategy report): the performance report now includes the
Average / Mean Drawdown, and a yearly table that pairs each calendar year's
return with that year's worst (intra-year) drawdown.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# ══════════════════════════════════════════════════════════════════════════════
# TRADE RECORDING
# ══════════════════════════════════════════════════════════════════════════════

def _record_closed_trade(strat, ticker, holding, exit_date,
                          exit_price, fill_price, exit_reason,
                          stop_price_at_exit):
    """Append one trade record to strat.position_metadata.
    Called for every exit: STOP_HIT, REBALANCE, CRASH_GUARD, END_OF_PERIOD.
    """
    self = strat
    entry_price  = holding['entry_price']
    entry_date   = holding['entry_date']
    peak_price   = holding['peak_price']
    stop_pct     = holding.get('stop_pct',     np.nan)
    atr_at_entry = holding.get('atr_at_entry', np.nan)
    weight       = holding.get('weight',        0.0)
    min_price    = holding.get('min_price',     entry_price)
    max_price    = holding.get('max_price',     entry_price)

    # Actual fill: for stop exits use fill_price; for others use exit_price
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
    accounting_mode:   str   = "modern",
    label:             str   = "Event-Driven",
) -> dict:
    """
    Core event-driven daily loop. Vol Targeting and Correlation Guard run inside the
    loop using rolling windows over past data only — no post-loop vectorised pass.
    """
    self = strat
    if self.positions is None:
        raise ValueError("Call get_positions() first.")
    if accounting_mode not in {"modern", "historical"}:
        raise ValueError("accounting_mode must be 'modern' or 'historical'")

    print("\n" + "=" * 65)
    print(f"[CSM Batch]  {label} Backtest starting")
    print("=" * 65)
    print(f"  Capital        : ₹{initial_capital:,.0f}")
    print(f"  Txn cost       : {transaction_cost*100:.3f}% one-way")
    print(f"  RFR            : {risk_free_rate*100:.1f}% p.a.")
    print(f"  Stop (entry)   : −{self.hard_stop_from_entry*100:.0f}%  [Layer 2]")
    print(f"  Stop (peak)    : −{self.hard_stop_from_peak*100:.0f}%  [Layer 3]")
    print(f"  Chandelier     : peak − {self.atr_multiplier}×ATR [Layer 1]")
    print(f"  Crash Guard    : {'ON' if self.use_crash_guard else 'OFF'}"
          f"  cooldown={self.crash_guard_cooldown} days")
    print(f"  Corr Guard     : threshold={self.corr_guard_threshold}")
    print(f"  Stop cooldown  : {self.stop_cooldown_days} days per ticker after STOP_HIT")
    print(f"  Min hold       : {self.min_hold_days} days before stop can fire")
    print(f"  ATR mult       : {self.atr_multiplier} normal / {self.atr_multiplier_high_vol} high-vol")
    print(f"  Vol target     : {self.vol_target*100:.0f}%  (de-leverage only)")
    if accounting_mode == "historical":
        print("  Accounting     : historical CSM Batch parity")
    print("=" * 65)

    # ── Pre-compute static arrays ─────────────────────────────────────────
    prices_ff  = self._prices_ff
    opens_ff   = self._opens_ff
    open_proxy = self._open_proxy          # prev-close; used for LTP gap check
    highs_ff   = self.highs.ffill() if not self.highs.empty else prices_ff.copy()
    lows_ff    = self.lows.ffill()  if not self.lows.empty  else prices_ff.copy()

    # Circuit breaker: True on bars where high == low (stock locked at price limit)
    # On these days no fills are possible — stops, rebalances, and entries are deferred.
    if not self.highs.empty and not self.lows.empty:
        is_circuit_ff = (highs_ff == lows_ff)
    else:
        is_circuit_ff = pd.DataFrame(False, index=prices_ff.index, columns=prices_ff.columns)

    # All daily returns (needed for rolling vol/corr computations)
    _dr_all = self.prices.pct_change(fill_method=None).fillna(0.0)

    # ── Panic / high-vol regime flags ─────────────────────────────────────
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

    # Monthly signal → daily (shifted 1 trading day so T signal trades T+1)
    monthly_signal = (
        self.positions
        .reindex(self.prices.index, method='ffill')
        .shift(1)
        .fillna(0.0)
    )

    # Rank-decay exits: align the month-end mask to daily (ffill) + shift(1) — the
    # same timing as the signal — so STEP F can label those drops RANK_EXIT.
    rank_exit_daily = None
    _rxm = getattr(self, 'rank_exit_mask', None)
    if _rxm is not None and not _rxm.empty:
        rank_exit_daily = (_rxm.reindex(self.prices.index, method='ffill')
                           .shift(1).fillna(False))

    # ── Mutable state ─────────────────────────────────────────────────────
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

    # Rolling buffers for in-loop Vol Targeting and Corr Guard.
    # We track UNSCALED portfolio position returns (gross, no vol scaling)
    # so the vol estimate is not distorted by our own scaling decisions.
    _port_ret_buf:  list = []   # past gross portfolio returns (position legs only)
    _stock_ret_buf: list = []   # list of pd.Series (all stocks, past day returns)
    _weight_buf:    list = []   # list of pd.Series (executed weights, past bars)
    VOL_WIN  = 21               # rolling window for vol estimate (annualised)
    CORR_WIN = 21               # rolling window for corr guard ratio

    # ── Main daily loop ───────────────────────────────────────────────────
    for i, date in enumerate(self.prices.index):

        # First bar: seed buffers with zeros, nothing to do
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
                    self,
                    ticker             = stock,
                    holding            = _h,
                    exit_date          = date,
                    exit_price         = _close,
                    fill_price         = _fill,
                    exit_reason        = 'CRASH_GUARD',
                    stop_price_at_exit = _h.get('atr_stop', np.nan),
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

        # ── Crash Guard cooldown ──────────────────────────────────────────
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

            # Circuit day: price locked at limit — no fills possible, defer to next bar
            if should_exit and stock in is_circuit_ff.columns \
                    and bool(is_circuit_ff.at[date, stock]):
                should_exit = False

            if should_exit:
                _record_closed_trade(
                    self,
                    ticker             = stock,
                    holding            = active_holdings[stock],
                    exit_date          = date,
                    exit_price         = today_close,
                    fill_price         = fill_px,
                    exit_reason        = 'STOP_HIT',
                    stop_price_at_exit = stop_lvl,
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
            # Circuit day: can't sell — restore previous weight and defer to next bar
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
                self,
                ticker             = stock,
                holding            = _h,
                exit_date          = date,
                exit_price         = _close,
                fill_price         = _fill,
                exit_reason        = _reason,
                stop_price_at_exit = _h.get('atr_stop', np.nan),
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

                # Per-ticker stop cooldown
                if stock in stop_cooldown_tickers:
                    _gap = (date - stop_cooldown_tickers[stock]).days
                    if _gap < self.stop_cooldown_days:
                        target_weights[stock] = 0.0
                        continue
                    else:
                        del stop_cooldown_tickers[stock]

                # Circuit day: price locked, can't enter
                if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                    target_weights[stock] = 0.0
                    continue

                _ep_open  = float(opens_ff.at[date, stock])
                _ep_close = float(prices_ff.at[date, stock])
                _ep = _ep_open if (_ep_open > 0 and not pd.isna(_ep_open)) else _ep_close

                # Initial stop sizing
                _atr_entry = np.nan
                if atr_daily is not None and stock in atr_daily.columns:
                    _atr_entry = float(atr_daily.at[date, stock])
                if not pd.isna(_atr_entry) and _atr_entry > 0:
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
        # Both use PAST data from the rolling buffers — strictly no lookahead.

        raw_weights = target_weights.copy()

        # No-leverage guard: keep gross exposure ≤ 100%. A circuit-day weight
        # restoration (STEP F retains a locked name's prior weight on top of the new
        # signal) can push the target sum above 1.0 — scale the whole book back so
        # allocation never exceeds full investment.
        _gross = float(raw_weights.sum())
        if _gross > 1.0:
            raw_weights = raw_weights / _gross

        # Correlation Guard: ratio of portfolio vol to avg-stock vol over
        # the past CORR_WIN days.  If ratio > threshold → scale to 50%.
        corr_scale = 1.0
        if len(_port_ret_buf) >= CORR_WIN:
            _pbuf   = np.array(_port_ret_buf[-CORR_WIN:])
            _p_vol  = float(_pbuf.std())         # portfolio std (daily)
            _pw     = _weight_buf[-1]             # previous day's weights (past)
            _w_sum  = float(_pw.sum())
            if _w_sum > 0 and _p_vol > 0:
                # Past CORR_WIN days of stock returns for stocks in prev portfolio
                _hist_start = max(0, i - CORR_WIN)
                _s_std = _dr_all.iloc[_hist_start:i].std()   # per-stock std
                _avg_s_vol = float((_s_std * _pw).sum() / _w_sum)
                if _avg_s_vol > 0 and (_p_vol / _avg_s_vol) > self.corr_guard_threshold:
                    corr_scale = 0.5

        # Vol Targeting (de-lever only): rolling 21-day portfolio vol (annualised).
        # Uses a longer 63-day buffer when available for a smoother estimate.
        vol_scale = 1.0
        if len(_port_ret_buf) >= VOL_WIN:
            _win = _port_ret_buf[-63:] if len(_port_ret_buf) >= 63 else _port_ret_buf[-VOL_WIN:]
            _rv  = float(np.std(_win)) * np.sqrt(252)
            if _rv > 0:
                vol_scale = min(1.0, self.vol_target / _rv)

        scaled_weights = raw_weights * (corr_scale * vol_scale)
        executed_weights_list.append(scaled_weights.copy())

        # Update rolling buffers (AFTER recording scaled_weights)
        # Gross position return = unscaled weights × today's returns
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
            self,
            ticker             = stock,
            holding            = _h,
            exit_date          = _last_date,
            exit_price         = _close,
            fill_price         = _fill,
            exit_reason        = 'END_OF_PERIOD',
            stop_price_at_exit = _h.get('atr_stop', np.nan),
        )
    active_holdings.clear()
    self._prices_ff_backtest = prices_ff

    print(f"\n[{label}] Stop exits    : {n_stop}")
    print(f"[{label}] Crash Guard   : {n_crash}")
    print(f"[{label}] Rebal exits   : {n_rebalance}")
    print(f"[{label}] Rank exits    : {n_rank_exit}")

    # ── Build executed-weights DataFrame ──────────────────────────────────
    executed_weights = pd.DataFrame(
        executed_weights_list, index=self.prices.index
    ).fillna(0.0)

    # ── Portfolio returns & equity curve ──────────────────────────────────
    # ``historical`` replicates the booking convention used by the recovered
    # 2003–2012 CSM Batch report.  It intentionally does not credit entry-day
    # open-to-close movement or separately charge the exit-day overnight gap.
    # Keep this explicit rather than hiding it in the strategy core: it is an
    # accounting choice, not a live signal or risk-management rule.
    _dr = _dr_all.copy()
    if accounting_mode == "historical":
        # The original engine only capped adverse stop/crash returns at the
        # recorded fill.  This is the exact historical convention needed for
        # parity with the recovered report.
        for meta in self.position_metadata:
            if meta['Exit_Reason'] not in {'STOP_HIT', 'CRASH_GUARD'}:
                continue
            ticker     = meta['Ticker']
            exit_date  = meta['Exit_Date']
            exit_price = meta['Exit_Price']
            if ticker not in _dr.columns or pd.isna(exit_price) or exit_price <= 0:
                continue
            if exit_date not in _dr.index:
                continue
            exit_loc = _dr.index.get_loc(exit_date)
            if exit_loc == 0:
                continue
            prev_close = self.prices.iloc[exit_loc - 1].get(ticker, np.nan)
            if pd.isna(prev_close) or prev_close <= 0:
                continue
            capped_ret = (exit_price / prev_close) - 1.0
            raw_ret    = _dr.at[exit_date, ticker]
            if not pd.isna(raw_ret) and raw_ret < capped_ret:
                _dr.at[exit_date, ticker] = capped_ret
        gross_eq_ret = (executed_weights * _dr).sum(axis=1)
    else:
        _opens_ff    = self._opens_ff
        _prev_close  = prices_ff.shift(1)
        _prev_exec_w = executed_weights.shift(1).fillna(0.0)
        # Modern booking: credit the entry-day close/open move, then account
        # for the position held through an exit-day open fill.
        for meta in self.position_metadata:
            ticker     = meta['Ticker']
            entry_date = meta['Entry_Date']
            entry_open = meta['Entry_Price']
            if (ticker not in _dr.columns
                    or entry_date not in _dr.index
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
            if ticker not in _opens_ff.columns or exit_date not in _opens_ff.index:
                continue
            open_exit = float(_opens_ff.at[exit_date, ticker])
            if pd.isna(open_exit) or open_exit <= 0:
                continue
            pc = float(_prev_close.at[exit_date, ticker])
            if pd.isna(pc) or pc <= 0:
                continue
            prev_w = float(_prev_exec_w.at[exit_date, ticker])
            if prev_w <= 1e-9:
                continue
            _exit_adj.at[exit_date] += prev_w * (open_exit / pc - 1.0)
        gross_eq_ret = (executed_weights * _dr).sum(axis=1) + _exit_adj
    total_w         = executed_weights.sum(axis=1)
    cash_w          = (1.0 - total_w).clip(lower=0.0)
    cash_ret        = cash_w * daily_rfr
    w_chg           = executed_weights.diff().abs().sum(axis=1)
    txn_cost        = w_chg * transaction_cost
    net_returns     = gross_eq_ret + cash_ret - txn_cost

    equity_curve    = (1.0 + net_returns).cumprod()
    portfolio_value = equity_curve * initial_capital

    # ── Performance metrics ───────────────────────────────────────────────
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
    avg_dd   = _dd.mean()                       # NEW: mean (time-average) drawdown
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
        'avg_drawdown'       : avg_dd,            # NEW
        'ann_volatility'     : ann_vol,
        'win_rate'           : win_rate,
        'ann_turnover'       : ann_turn,
        'ann_signal_turnover': sig_turn,
        'benchmark_ret'      : (self.benchmark.pct_change(fill_method=None)
                                .reindex(self.prices.index)
                                if self.benchmark is not None else None),
    }

    print(f"\n[{label}] CAGR={cagr*100:.2f}%  "
          f"Sharpe={sharpe:.2f}  MaxDD={max_dd*100:.2f}%  AvgDD={avg_dd*100:.2f}%")
    return self.results


def backtest_event_driven(
    strat,
    initial_capital  = 100_000.0,
    transaction_cost = 0.001,
    risk_free_rate   = 0.06,
    accounting_mode  = "modern",
):
    """Event-driven backtest — all overlays applied inside the loop
    using past data only. No post-loop vectorised pass.

    ``accounting_mode='historical'`` reproduces the return-booking convention
    used by the recovered 2003–2012 CSM Batch report.  ``'modern'`` keeps the
    corrected entry/exit-day accounting used by the newer harness.
    """
    self = strat
    return _run_backtest_core(
        self,
        initial_capital   = initial_capital,
        transaction_cost  = transaction_cost,
        risk_free_rate    = risk_free_rate,
        accounting_mode   = accounting_mode,
        label             = "Event-Driven",
    )


# ══════════════════════════════════════════════════════════════════════════════
# TRADE LOG  (v3-style: built from position_metadata, no matrix reverse-eng)
# ══════════════════════════════════════════════════════════════════════════════

def get_trade_log(strat):
    """
    Build a trade-log DataFrame from strat.position_metadata.
    Must be called after backtest_event_driven().

    Columns: Ticker, Entry_Date, Entry_Price, Exit_Date, Exit_Price
      (actual fill — open/stop for stops, close for rebalance),
      Close_At_Exit, Peak_Price, Stop_Price_At_Exit, Stop_Pct,
      ATR_At_Entry, Exit_Reason, Weight, Quantity, Position_Size,
      PnL_Pct, PnL_Abs, Holding_Days, MAE_Pct, MFE_Pct.
    """
    self = strat
    if not self.position_metadata:
        print("Warning: No trade metadata. Run backtest() first.")
        return pd.DataFrame()

    equity_curve     = self.results['equity_curve']     if self.results else None
    executed_weights = self.results['executed_weights'] if self.results else None
    prices_ffill     = self.prices.ffill()

    # Build a fast date→portfolio-value lookup from the equity curve.
    # .ffill() ensures weekend / holiday entry dates still get a valid value.
    _equity_lookup = None
    if equity_curve is not None and not equity_curve.empty:
        _equity_lookup = equity_curve.ffill()

    rows = []
    for meta in self.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        exit_date   = meta['Exit_Date']
        entry_price = meta['Entry_Price']
        exit_price  = meta['Exit_Price']   # fill price (stop or close)

        # Recover NaN exit via forward-fill
        if pd.isna(exit_price) and ticker in prices_ffill.columns:
            exit_price = (prices_ffill.at[exit_date, ticker]
                          if exit_date in prices_ffill.index
                          else prices_ffill[ticker].iloc[-1])

        # Read actual executed weight (first non-zero after entry_date)
        weight = meta['Weight']
        if executed_weights is not None and ticker in executed_weights.columns:
            ew_col  = executed_weights[ticker]
            window  = ew_col.loc[(ew_col.index > entry_date) & (ew_col.index <= exit_date)]
            nonzero = window[window > 1e-9]
            if not nonzero.empty:
                weight = float(nonzero.iloc[0])

        # Portfolio value on first execution day (T+1)
        port_val = np.nan
        if equity_curve is not None:
            future_idx = equity_curve.index[equity_curve.index > entry_date]
            if len(future_idx) > 0:
                port_val = float(equity_curve.loc[future_idx[0]])

        # Quantity and dollar P&L
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

        # Classify stop exits, aware of use_trailing_stop and the profit-lock:
        #   • stop at/below entry-hard (−15%)      → STOP_LOSS (fixed/gap catastrophe)
        #   • above entry-hard & trailing ON       → TRAILING (ATR chandelier / peak-hard)
        #   • above entry-hard & trailing OFF      → STOP_LOSS (initial fixed ATR stop)
        _stop_type = ''
        _win = (pd.notna(pnl_pct) and pnl_pct > 0)
        if meta['Exit_Reason'] == 'STOP_HIT':
            _sp  = meta.get('Stop_Price_At_Exit', np.nan)
            _eh  = (entry_price * (1.0 - self.hard_stop_from_entry)
                    if (pd.notna(entry_price) and entry_price > 0) else np.nan)
            _above_hard = (pd.notna(_sp) and pd.notna(_eh) and _sp > _eh + 1e-6)
            if _above_hard and self.use_trailing_stop:
                _stop_type   = 'TRAILING'
                _exit_detail = 'TRAILING_WIN' if _win else 'TRAILING_LOSS'
            else:
                _stop_type, _exit_detail = 'STOP_LOSS', 'STOP_LOSS'
        else:
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
            'Portfolio Value'   : round(port_val, 2),
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
    if total > 0:
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {losses}"
              f" | Win Rate: {wins/total*100:.1f}%")
        print(f"[Trade Log] Worst trade: {df['PnL_Pct'].min():.2f}%"
              f"  Best trade: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
    return df


def print_exit_breakdown(trade_log):
    """Granular exit breakdown: each exit reason split into WIN / LOSS, with the
    within-reason win rate, average trade P&L, and that bucket's share of total
    equity contribution (Σ weight × PnL%). STOP_HIT is shown as TRAILING — the
    dominant stop is the ATR chandelier trail.

    Reads the column added in get_trade_log; safe to call on any trade-log frame.
    """
    if trade_log is None or trade_log.empty:
        print("\n── Exit Breakdown — no trades ────────────────────────────────")
        return

    df = trade_log.copy()
    if 'Exit_Detail' not in df.columns:   # older trade-log frame: derive coarse detail
        df['Exit_Detail'] = df['Exit_Reason'] + np.where(df['PnL_Pct'] > 0, '_WIN', '_LOSS')
    df['_c'] = df['Weight'] * df['PnL_Pct']            # ≈ equity contribution
    tot = df['_c'].sum() or 1.0

    print(f"\n── Exit Breakdown — by reason & outcome ──────────────────────")
    print(f"  {'bucket':<22}{'n':>6}{'win%':>8}{'avgP&L':>9}{'%ofP&L':>9}")
    print(f"  {'-' * 55}")
    fam_order = ['STOP_HIT', 'REBALANCE', 'RANK_EXIT', 'CRASH_GUARD', 'END_OF_PERIOD']
    sub_order = {
        'STOP_HIT'     : ['TRAILING_WIN', 'TRAILING_LOSS',
                          'BREAKEVEN_WIN', 'BREAKEVEN_LOSS', 'STOP_LOSS'],
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
            print(f"    └ {d:<18}{len(s):>6}{(s['PnL_Pct'] > 0).mean() * 100:>7.1f}%"
                  f"{s['PnL_Pct'].mean():>8.2f}%{s['_c'].sum() / tot * 100:>8.1f}%")
    print(f"  {'-' * 55}")


# ══════════════════════════════════════════════════════════════════════════════
# SLICE & REBASE + METRICS  (recompute on the reporting window)
# ══════════════════════════════════════════════════════════════════════════════

def slice_results(res, start_date, risk_free_rate=0.06):
    """
    Trim results to the reporting window and recompute all metrics on
    the sliced data so the report reflects only the declared period.

    NEW: also computes res['avg_drawdown'] (mean of the daily underwater
    series) and stores res['dd_series'] for the yearly-drawdown table.
    """
    eq = res['equity_curve']

    # Find first available index >= start_date
    if start_date not in eq.index:
        idx = eq.index.searchsorted(start_date)
        if idx >= len(eq):
            print(f"WARNING: start_date {start_date} is after data end — not slicing.")
            return res
        start_date = eq.index[idx]

    res['equity_curve']     = eq.loc[start_date:]
    # Rebase to initial capital
    res['equity_curve']     = res['equity_curve'] / res['equity_curve'].iloc[0] * 100_000
    res['portfolio_value']  = res['equity_curve']
    res['net_returns']      = res['net_returns'].loc[start_date:]
    res['executed_weights'] = res['executed_weights'].loc[start_date:]
    if 'turnover' in res:
        res['turnover']     = res['turnover'].loc[start_date:]

    eq  = res['equity_curve']
    ret = res['net_returns']

    n_years     = (eq.index[-1] - eq.index[0]).days / 365.25
    daily_rfr   = (1 + risk_free_rate) ** (1 / 252) - 1

    res['cagr']         = (eq.iloc[-1] / eq.iloc[0]) ** (1 / n_years) - 1 if n_years > 0 else 0
    res['total_return'] = eq.iloc[-1] / eq.iloc[0] - 1
    res['ann_volatility']= ret.std() * np.sqrt(252)

    excess              = ret - daily_rfr
    res['sharpe']       = (np.sqrt(252) * excess.mean() / ret.std()
                           if ret.std() != 0 else 0)

    # Sortino: daily downside deviation (no extra sqrt(252) in denominator)
    _dn                 = ret.clip(upper=0.0)
    _dndev              = np.sqrt((_dn ** 2).mean())
    res['sortino']      = (np.sqrt(252) * ret.mean() / _dndev if _dndev > 0 else 0)

    running_max         = eq.cummax()
    dd_series           = (eq / running_max) - 1
    res['dd_series']    = dd_series                 # NEW: stored for yearly table
    res['max_drawdown'] = dd_series.min()
    res['avg_drawdown'] = dd_series.mean()          # NEW: mean (time-average) drawdown
    res['calmar']       = (res['cagr'] / abs(res['max_drawdown'])
                           if res['max_drawdown'] != 0 else 0)
    
    _gross_alloc          = res['executed_weights'].sum(axis=1)
    res['avg_allocation'] = float(_gross_alloc.mean())
    res['max_allocation'] = float(_gross_alloc.max())
    res['min_allocation'] = float(_gross_alloc.min())

    # ── Portfolio beta / alpha vs benchmark over the report window (NEW) ──
    # Realized beta of the actual strategy return stream — captures the net market
    # exposure left after all rebalancing, stops, crash-guard and other exit logic.
    res['beta'], res['alpha'] = np.nan, np.nan
    _bret = res.get('benchmark_ret', None)
    if _bret is not None:
        _b    = _bret.loc[start_date:].reindex(ret.index)
        _pair = pd.concat([ret, _b], axis=1).dropna()
        if len(_pair) > 20 and float(_pair.iloc[:, 1].var()) > 0:
            _c = np.cov(_pair.iloc[:, 0].values, _pair.iloc[:, 1].values)
            res['beta']  = float(_c[0, 1] / _c[1, 1])
            res['alpha'] = float((_pair.iloc[:, 0].mean()
                                  - res['beta'] * _pair.iloc[:, 1].mean()) * 252)

    monthly_res         = res['portfolio_value'].resample('ME').last().pct_change()
    res['win_rate']     = (monthly_res.dropna() > 0).mean()

    if 'turnover' in res and n_years > 0:
        res['ann_turnover'] = res['turnover'].sum() / n_years

    # Daily win rate
    res['daily_win_rate'] = (ret > 0).mean()

    # Trade-basis metric placeholders (populated by populate_trade_stats())
    res['trade_win_rate']     = 0.0
    res['total_trades_count'] = 0
    res['avg_trade_return']   = 0.0
    res['avg_win_pct']        = 0.0
    res['avg_loss_pct']       = 0.0
    res['payoff_ratio']       = 0.0
    res['avg_holding_days']   = 0.0
    res['best_trade']         = 0.0
    res['worst_trade']        = 0.0
    res['profit_factor']      = 0.0
    res['profit_factor_dollar'] = 0.0
    res['median_trade_return']  = 0.0
    res['pct_stops']            = 0.0
    res['pct_rebalance']        = 0.0
    res['pct_rank_exit']        = 0.0
    res['pct_crash_guard']      = 0.0
    res['pct_end_period']       = 0.0
    res['avg_stop_pct']          = 0.0
    res['avg_mae']               = 0.0
    res['avg_mfe']               = 0.0

    # Save backtest log CSV
    log = pd.DataFrame(index=eq.index)
    log['Portfolio_Value'] = res['portfolio_value']
    log['Net_Return']      = ret
    w = res['executed_weights']
    log['Positions']       = (w > 1e-6).sum(axis=1)
    log['Exposure']        = w.sum(axis=1)
    log['Drawdown']        = dd_series
    log.to_csv('backtest_logs_batch.csv')
    print(f"[Logs] backtest_logs_batch.csv  ({len(log)} rows)")

    return res


def populate_trade_stats(results, detailed_log):
    """Populate trade-basis metrics on `results` from a filtered trade log.
    Mirrors the trade-stats block of the original runner verbatim."""
    if detailed_log is None or detailed_log.empty:
        return results

    dl      = detailed_log
    wins    = (dl['PnL_Pct'] > 0).sum()
    losses  = (dl['PnL_Pct'] < 0).sum()
    total_t = len(dl)

    results['trade_win_rate']     = wins / total_t if total_t > 0 else 0.0
    results['total_trades_count'] = total_t
    results['avg_trade_return']   = dl['PnL_Pct'].mean()
    results['median_trade_return']= dl['PnL_Pct'].median()
    results['avg_holding_days']   = dl['Holding_Days'].mean()
    results['best_trade']         = dl['PnL_Pct'].max()
    results['worst_trade']        = dl['PnL_Pct'].min()
    results['avg_stop_pct']       = dl['Stop_Pct'].mean()
    results['avg_mae']            = dl['MAE_Pct'].mean()
    results['avg_mfe']            = dl['MFE_Pct'].mean()

    avg_win  = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].mean() if wins   > 0 else 0.0
    avg_loss = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().mean() if losses > 0 else 0.0
    results['avg_win_pct']  = avg_win
    results['avg_loss_pct'] = avg_loss
    results['payoff_ratio'] = avg_win / avg_loss if avg_loss > 0 else float('inf')

    gw_pct = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].sum()
    gl_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().sum()
    results['profit_factor'] = gw_pct / gl_pct if gl_pct > 0 else float('inf')

    gw_abs = dl.loc[dl['PnL_Abs'] > 0, 'PnL_Abs'].sum()
    gl_abs = dl.loc[dl['PnL_Abs'] < 0, 'PnL_Abs'].abs().sum()
    results['profit_factor_dollar'] = gw_abs / gl_abs if gl_abs > 0 else float('inf')

    reason_counts = dl['Exit_Reason'].value_counts()
    results['pct_stops']       = reason_counts.get('STOP_HIT',     0) / total_t * 100
    results['pct_rebalance']   = reason_counts.get('REBALANCE',    0) / total_t * 100
    results['pct_rank_exit']   = reason_counts.get('RANK_EXIT',    0) / total_t * 100
    results['pct_crash_guard'] = reason_counts.get('CRASH_GUARD',  0) / total_t * 100
    results['pct_end_period']  = reason_counts.get('END_OF_PERIOD',0) / total_t * 100

    return results


# ══════════════════════════════════════════════════════════════════════════════
# YEARLY RETURNS + YEARLY DRAWDOWN  (NEW)
# ══════════════════════════════════════════════════════════════════════════════

def compute_yearly_table(portfolio_value):
    """
    Build a per-calendar-year DataFrame indexed by Year with columns:
      • Return  — full-year return of the equity curve.
                  Year 1 is measured from inception to that year's end.
      • Max_DD  — worst INTRA-year drawdown (peak resets at each year start),
                  i.e. min over the year of (equity / running-max-within-year − 1).

    Returns an empty DataFrame if portfolio_value has no usable points.
    """
    pv = portfolio_value.dropna()
    if pv.empty:
        return pd.DataFrame(columns=['Return', 'Max_DD'])

    # ── Yearly returns (chained year-end-to-year-end; year 1 from inception) ──
    year_end   = pv.resample('YE').last()
    yearly_ret = year_end.pct_change()
    if len(year_end) > 0:
        yearly_ret.iloc[0] = year_end.iloc[0] / pv.iloc[0] - 1

    # ── Yearly intra-year max drawdown ───────────────────────────────────────
    def _intra_year_max_dd(year_slice):
        rmax = year_slice.cummax()
        return ((year_slice / rmax) - 1).min()

    yearly_dd = pv.groupby(pv.index.year).apply(_intra_year_max_dd)

    table = pd.DataFrame({
        'Return': yearly_ret.set_axis(yearly_ret.index.year),
        'Max_DD': yearly_dd,
    })
    table.index.name = 'Year'
    return table


def print_yearly_performance(portfolio_value):
    """Print a yearly table pairing each calendar year's return with that
    year's worst intra-year drawdown, plus the averages across years."""
    table = compute_yearly_table(portfolio_value)

    print("\n" + "=" * 34)
    print("  Yearly Returns & Drawdown")
    print("=" * 34)
    print(f"{'Year':<6} | {'Return':>9} | {'Max DD':>9}")
    print("-" * 32)
    for year, row in table.iterrows():
        ret_str = f"{row['Return']*100:>8.2f}%" if pd.notna(row['Return']) else f"{'N/A':>9}"
        dd_str  = f"{row['Max_DD']*100:>8.2f}%" if pd.notna(row['Max_DD']) else f"{'N/A':>9}"
        print(f"{year:<6} | {ret_str} | {dd_str}")
    print("-" * 32)

    avg_ret = table['Return'].mean()
    avg_dd  = table['Max_DD'].mean()
    avg_ret_str = f"{avg_ret*100:>8.2f}%" if pd.notna(avg_ret) else f"{'N/A':>9}"
    avg_dd_str  = f"{avg_dd*100:>8.2f}%"  if pd.notna(avg_dd)  else f"{'N/A':>9}"
    print(f"{'Avg':<6} | {avg_ret_str} | {avg_dd_str}")
    print("=" * 34)
    return table


# ══════════════════════════════════════════════════════════════════════════════
# PERFORMANCE REPORT
# ══════════════════════════════════════════════════════════════════════════════

def print_report(results, historical_style=False):
    """Formatted performance report. Mirrors the original runner's report and
    adds an Avg / Mean Drawdown line to the Portfolio Metrics block.

    ``historical_style=True`` emits the recovered 2003–2012 report layout.
    It intentionally suppresses diagnostics that did not exist in that report
    (beta/alpha/allocation and rank-exit share), making visual parity useful
    without removing those diagnostics from modern runs.
    """
    W = 38   # column width for alignment
    SEP = "=" * W

    print(f"\n{SEP}")
    print(f"  CSM BATCH  —  PERFORMANCE REPORT")
    print(SEP)

    print(f"\n── Portfolio Metrics ─────────────────")
    print(f"  CAGR              : {results['cagr']*100:>8.2f}%")
    print(f"  Total Return      : {results['total_return']*100:>8.2f}%")
    print(f"  Ann Volatility    : {results['ann_volatility']*100:>8.2f}%")
    print(f"  Max Drawdown      : {results['max_drawdown']*100:>8.2f}%")
    print(f"  Avg / Mean DD     : {results.get('avg_drawdown', 0)*100:>8.2f}%  (time-average underwater)")
    print(f"  Sharpe Ratio      : {results['sharpe']:>9.3f}")
    print(f"  Sortino Ratio     : {results['sortino']:>9.3f}")
    print(f"  Calmar Ratio      : {results['calmar']:>9.3f}")
    if not historical_style:
        print(f"  Beta (vs bench)   : {results.get('beta', float('nan')):>9.3f}  (realized market exposure)")
        print(f"  Alpha (ann.)      : {results.get('alpha', 0)*100:>8.2f}%  (return beyond beta×benchmark)")
        print(f"  Avg Allocation    : {results.get('avg_allocation', 0)*100:>8.2f}%  (gross exposure; rest in cash)")
        print(f"  Max Allocation    : {results.get('max_allocation', 0)*100:>8.2f}%")
        print(f"  Min Allocation    : {results.get('min_allocation', 0)*100:>8.2f}%")
    print(f"  Final Portfolio   : ₹{results['portfolio_value'].iloc[-1]:>12,.2f}")

    print(f"\n── Win Rate (3 views) ────────────────")
    print(f"  Daily Win Rate    : {results['daily_win_rate']*100:>8.2f}%")
    print(f"  Monthly Win Rate  : {results['win_rate']*100:>8.2f}%")
    if results['total_trades_count'] > 0:
        print(f"  Trade Win Rate    : {results['trade_win_rate']*100:>8.2f}%"
              f"  ({results['total_trades_count']} trades)")
    else:
        print(f"  Trade Win Rate    : {'N/A':>8}")

    print(f"\n── Trade Statistics ──────────────────")
    if results['total_trades_count'] > 0:
        print(f"  Total Trades      : {results['total_trades_count']:>8}")
        print(f"  Avg Trade Return  : {results['avg_trade_return']:>8.2f}%")
        print(f"  Median Trade Ret  : {results['median_trade_return']:>8.2f}%")
        print(f"  Best Trade        : {results['best_trade']:>8.2f}%")
        print(f"  Worst Trade       : {results['worst_trade']:>8.2f}%")
        print(f"  Avg Win  (trade)  : {results['avg_win_pct']:>8.2f}%")
        print(f"  Avg Loss (trade)  : -{results['avg_loss_pct']:>7.2f}%")
        print(f"  Payoff Ratio      : {results['payoff_ratio']:>9.3f}  (avg win / avg loss)")
        print(f"  Profit Factor (%) : {results['profit_factor']:>9.3f}  (equal-weighted)")
        print(f"  Profit Factor : {results['profit_factor_dollar']:>9.3f}  (rupees-weighted)")
        print(f"  Avg Holding Days  : {results['avg_holding_days']:>8.1f}")
        print(f"  Avg Stop Pct      : {results.get('avg_stop_pct', 0):>8.2f}%  (initial ATR stop at entry)")
        print(f"  Avg MAE           : {results.get('avg_mae', 0):>8.2f}%  (max adverse excursion)")
        print(f"  Avg MFE           : {results.get('avg_mfe', 0):>8.2f}%  (max favorable excursion)")
    else:
        print("  No completed trades in reporting period.")

    print(f"\n── Exit Breakdown ────────────────────")
    if results['total_trades_count'] > 0:
        print(f"  Stop Hit          : {results['pct_stops']:>8.1f}%")
        print(f"  Rebalance         : {results['pct_rebalance']:>8.1f}%")
        if not historical_style:
            print(f"  Rank Exit         : {results.get('pct_rank_exit', 0):>8.1f}%")
        print(f"  Crash Guard       : {results['pct_crash_guard']:>8.1f}%")
        print(f"  End of Period     : {results.get('pct_end_period', 0):>8.1f}%")

    print(f"\n── Turnover ──────────────────────────")
    if 'ann_turnover' in results:
        print(f"  Ann Turnover      : {results['ann_turnover']*100:>8.2f}%  (daily weight changes × txn cost)")
    if 'ann_signal_turnover' in results:
        print(f"  Signal Turnover   : {results['ann_signal_turnover']:>8.1f}  round-trips/year (monthly rebal only)")


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════

def plot_performance(results, benchmark_series=None):
    equity           = results['equity_curve']
    dd               = (equity / equity.cummax()) - 1
    executed_weights = results.get('executed_weights', None)

    fig = plt.figure(figsize=(16, 20))
    gs  = fig.add_gridspec(4, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='CSM Batch', color='#1f77b4', linewidth=1.5)
    ax1.set_yscale('log')
    if benchmark_series is not None:
        bench_rb = benchmark_series / benchmark_series.iloc[0]
        ax1.plot(bench_rb.index, bench_rb, label='Benchmark', color='gray',
                 linestyle='--', alpha=0.7)
    ax1.set_title('1. Cumulative Growth (Log Scale)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', linestyle='--', alpha=0.3)
    ax1.set_ylabel('Portfolio Value')

    # Panel 2: Relative Strength
    ax2 = fig.add_subplot(gs[1, 0])
    if benchmark_series is not None:
        ba = benchmark_series.reindex(equity.index).ffill()
        rs = (equity / equity.iloc[0]) / (ba / ba.iloc[0])
        ax2.plot(rs.index, rs, color='purple', linewidth=1.2)
        ax2.set_title('2. Relative Strength vs Benchmark', fontsize=12, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.set_ylabel('Ratio')
    else:
        ax2.text(0.5, 0.5, 'No Benchmark', ha='center', va='center')

    # Panel 3: Active Positions
    ax3 = fig.add_subplot(gs[1, 1])
    if executed_weights is not None:
        pos_count = (executed_weights > 1e-6).sum(axis=1)
    else:
        pos_count = pd.Series(0, index=equity.index)
    ax3.fill_between(pos_count.index, pos_count, step='post', color='#9467bd', alpha=0.5)
    ax3.plot(pos_count.index, pos_count, color='#9467bd', linewidth=0.8, drawstyle='steps-post')
    ax3.set_title('3. Active Positions (Daily Count)', fontsize=12, fontweight='bold')
    ax3.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax3.set_ylabel('Count')

    # Panel 4: Drawdown
    ax4 = fig.add_subplot(gs[2, :])
    ax4.fill_between(dd.index, dd, 0, color='#d62728', alpha=0.3)
    ax4.plot(dd.index, dd, color='#d62728', linewidth=1)
    # Overlay the mean (average) drawdown line — NEW
    avg_dd_line = results.get('avg_drawdown', dd.mean())
    ax4.axhline(avg_dd_line, color='black', linestyle=':', linewidth=1,
                label=f'Avg DD: {avg_dd_line*100:.2f}%')
    ax4.set_title('4. Drawdown Profile', fontsize=12, fontweight='bold')
    ax4.legend(fontsize=9)
    ax4.grid(True, linestyle='--', alpha=0.3)
    ax4.set_ylabel('Drawdown')

    # Panel 5: Monthly Return Distribution
    ax5 = fig.add_subplot(gs[3, :])
    monthly_ret = equity.resample('ME').last().pct_change().dropna()
    ax5.hist(monthly_ret * 100, bins=50, color='teal', edgecolor='black', alpha=0.7)
    ax5.axvline(0, color='black', linestyle='--', linewidth=1)
    mean_ret = monthly_ret.mean() * 100
    ax5.axvline(mean_ret, color='blue', linestyle=':', label=f'Mean: {mean_ret:.2f}%')
    ax5.set_title('5. Monthly Return Distribution', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Monthly Return (%)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('strategy_performance_batch.png', dpi=150)
    print("[Graphics] Saved  →  strategy_performance_batch.png")

    # Heatmap
    try:
        hm_df              = pd.DataFrame({'Return': monthly_ret})
        hm_df['Year']      = hm_df.index.year
        hm_df['Month']     = hm_df.index.month
        heatmap_data       = hm_df.pivot(index='Year', columns='Month', values='Return')
        plt.figure(figsize=(14, max(6, len(heatmap_data) * 0.55)))
        sns.heatmap(heatmap_data * 100, annot=True, fmt='.1f',
                    cmap='RdYlGn', center=0, cbar=False)
        plt.title('Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('strategy_heatmap_batch.png', dpi=150)
        print("[Graphics] Saved  →  strategy_heatmap_batch.png")
    except Exception as e:
        print(f"[Graphics] Heatmap failed: {e}")


# ══════════════════════════════════════════════════════════════════════════════
# IC / ICIR  —  Information Coefficient Analysis
# ══════════════════════════════════════════════════════════════════════════════

def calculate_ic(strat, forward_periods: int = 1, method: str = 'spearman',
                 report_start: str = None,
                 per_component: bool = True) -> dict:
    """
    Filtered-universe IC / ICIR for the dual-lookback Sharpe factor.

    WHAT IC MEASURES HERE
    ─────────────────────
    IC_t = cross-sectional Spearman rank correlation between the composite
    factor score (at month-end t) and the actual forward return from t to
    t+k, computed ONLY on stocks that passed the universe filter (SMA-200,
    liquidity, circuit-breaker, price floor, falling-knife) at time t.

    WHY THIS IS MEANINGFUL FOR A PURE TOP-N STRATEGY
    ─────────────────────────────────────────────────
    Unlike gated strategies that reject 90%+ of candidates via hard entry
    conditions, this strategy IS a pure factor strategy: it holds the top
    `top_n` (=15) ranked stocks from the ~30-80 monthly eligible universe.
    Universe IC directly measures "does the factor correctly rank the
    eligible pool?" — which IS the strategy's core mechanism.

    IMPORTANT CAVEATS
    ─────────────────
    1. Bear-market months: when most stocks fall below SMA-200, the eligible
       universe collapses to < 5 stocks → those months are excluded from IC
       computation. This is correct (strategy is also idle then), but means
       IC is measured only in active / bull-market months.
    2. The absolute momentum gate in get_positions() (positive 12m return
       required) further restricts actual holdings beyond the universe filter.
       IC here includes negative-momentum stocks that ARE in the universe but
       would be gate-rejected. To measure IC on gate-passed stocks only, use
       calculate_realized_ic().
    3. top_n=15 is VERY concentrated. Standard IC thresholds (> 0.05, ICIR
       > 0.5) were calibrated for 100+ stock portfolios. For a 15-stock book,
       meaningful IC thresholds are lower (IC > 0.03, ICIR > 0.2 useful).

    Parameters
    ----------
    forward_periods : int   — holding horizon in months (default 1)
    method          : str   — 'spearman' (default) or 'pearson'
    report_start    : str   — ISO date; only IC from this date in summary
    per_component   : bool  — also compute IC for 12m and 6m Sharpe separately

    Returns
    -------
    dict: ic_series, ic_mean, ic_std, icir, ic_positive_pct,
          t_stat, factor_decay, component_ic
    """
    self = strat
    from scipy import stats as _scipy_stats

    if self.factors is None:
        raise ValueError("Call calculate_factors() first.")

    monthly_prices = self.prices.ffill().resample('ME').last()
    fwd_ret = (monthly_prices
               .pct_change(forward_periods, fill_method=None)
               .shift(-forward_periods))

    corr_fn = (
        lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation
        if method == 'spearman'
        else _scipy_stats.pearsonr(x, y)[0]
    )

    # ── (A) Combined factor IC — universe-filtered cross-section ──────────
    ic_records = []
    for date in self.factors.index:
        if date not in fwd_ret.index:
            continue
        f      = self.factors.loc[date].dropna()   # universe-filtered only
        r      = fwd_ret.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) < 5:
            continue
        ic_records.append({
            'Date'     : date,
            'IC'       : corr_fn(f[common].values, r[common].values),
            'N_stocks' : len(common),
        })

    ic_series = pd.DataFrame(ic_records).set_index('Date')['IC'].dropna()
    ic_rep    = ic_series.loc[report_start:] if report_start else ic_series
    n         = len(ic_rep)

    ic_mean = ic_rep.mean()
    ic_std  = ic_rep.std()
    icir    = ic_mean / ic_std if ic_std > 0 else 0.0
    pos_pct = (ic_rep > 0).mean()
    t_stat  = ic_mean / (ic_std / np.sqrt(n)) if (n > 0 and ic_std > 0) else 0.0

    # ── (B) Factor decay across multiple horizons ─────────────────────────
    decay = {}
    for h in [1, 3, 6, 12]:
        fwd_h     = monthly_prices.pct_change(h, fill_method=None).shift(-h)
        ic_h_list = []
        for date in self.factors.index:
            if date not in fwd_h.index:
                continue
            f      = self.factors.loc[date].dropna()
            r      = fwd_h.loc[date].dropna()
            common = f.index.intersection(r.index)
            if len(common) < 5:
                continue
            ic_h_list.append(corr_fn(f[common].values, r[common].values))
        _arr = np.array(ic_h_list)
        _m, _s = float(np.nanmean(_arr)), float(np.nanstd(_arr))
        decay[h] = {'ic_mean': _m, 'icir': _m / _s if _s > 0 else 0.0}

    # ── (C) Per-component IC (12m Sharpe + 6m Sharpe) ────────────────────
    # UNIVERSE FILTER FIX: restrict components to the same eligible universe
    # as the combined factor (self.factors.notna() mask). Without this, all
    # 250 stocks are included, contaminating IC with below-SMA200 stocks that
    # exhibit short-term mean reversion → artificially negative component IC.
    component_ic = {}
    if per_component:
        prices_ff = self.prices.ffill()
        monthly_ret = prices_ff.resample('ME').last().pct_change(fill_method=None)
        idx       = self.factors.index
        _uni_mask = self.factors.notna()   # True for universe-eligible stocks

        L, S, lag = self.lookback_months, self.lookback_short_months, self.lag_months

        # 12m Sharpe component
        _mp = prices_ff.resample('ME').last()
        ret_L  = (_mp.shift(lag) / _mp.shift(lag + L)) - 1
        vol_L  = (monthly_ret.rolling(L).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        comp_12m = (ret_L / vol_L).clip(-5, 5).reindex(idx)

        # 6m Sharpe component
        ret_S  = (_mp.shift(lag) / _mp.shift(lag + S)) - 1
        vol_S  = (monthly_ret.rolling(S).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        comp_6m  = (ret_S / vol_S).clip(-5, 5).reindex(idx)

        for comp_name, comp_df in [('12m_Sharpe', comp_12m), ('6m_Sharpe', comp_6m)]:
            _ic_c = []
            for date in idx:
                if date not in fwd_ret.index:
                    continue
                # KEY: restrict to universe-eligible stocks only
                uni_stocks = _uni_mask.loc[date]
                uni_stocks = uni_stocks[uni_stocks].index
                f = comp_df.loc[date].reindex(uni_stocks).dropna()
                r = fwd_ret.loc[date].dropna()
                common = f.index.intersection(r.index)
                if len(common) < 5:
                    continue
                _ic_c.append(corr_fn(f[common].values, r[common].values))
            _arr = np.array(_ic_c)
            _m, _s = float(np.nanmean(_arr)), float(np.nanstd(_arr))
            component_ic[comp_name] = {
                'ic_mean': _m,
                'ic_std' : _s,
                'icir'   : _m / _s if _s > 0 else 0.0,
                'pos_pct': float((_arr > 0).mean()),
            }

    # ── Print report ─────────────────────────────────────────────────────
    total_factor_months = len(self.factors.index)
    print("\n" + "=" * 68)
    print(f" FILTERED-UNIVERSE IC / ICIR  —  CSM Batch  "
          f"({method.upper()}, {forward_periods}m forward)")
    print("=" * 68)
    print(f"  Strategy: pure top-{self.top_n} factor ranking — universe IC IS the")
    print(f"  right primary measure. Bear-market months excluded when < 5")
    print(f"  stocks pass SMA-200/liquidity/circuit filter.")
    print(f"  Thresholds: top_n={self.top_n} (concentrated) → IC>0.03, ICIR>0.2 meaningful.")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  Total factor months  : {total_factor_months}")
    print(f"  IC-computable months : {n}  (>= 5 stocks eligible)")
    print(f"  Excluded months      : {total_factor_months - n}  (bear market / warmup)")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  IC Mean (factor)     : {ic_mean:+.4f}")
    print(f"  IC Std               : {ic_std:.4f}")
    print(f"  ICIR                 : {icir:+.3f}   (> 0.2 useful for top-{self.top_n} book)")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic          : {t_stat:+.2f}   (> 2.0 = statistically significant)")
    if abs(t_stat) >= 2.0:
        print(f"  ✓ t-stat >= 2.0: factor predictive power is statistically significant")
    print(f"\n  Factor Decay (IC across forward horizons):")
    print(f"  {'Horizon':>8}  {'IC Mean':>10}  {'ICIR':>8}")
    peak_h = max(decay, key=lambda h: decay[h]['ic_mean'])
    for h, d in decay.items():
        tag = " ← peak (sweet spot)" if h == peak_h else ""
        print(f"  {h:>6}m  {d['ic_mean']:>+10.4f}  {d['icir']:>8.3f}{tag}")
    if component_ic:
        print(f"\n  Per-Component IC (universe-filtered, {method}, {forward_periods}m):")
        print(f"  {'Component':<14}  {'IC Mean':>10}  {'ICIR':>8}  {'Hit%':>7}")
        for cname, d in component_ic.items():
            print(f"  {cname:<14}  {d['ic_mean']:>+10.4f}  "
                  f"{d['icir']:>8.3f}  {d['pos_pct']*100:>6.1f}%")
    print("=" * 68)

    return {
        'ic_series'       : ic_series,
        'ic_mean'         : ic_mean,
        'ic_std'          : ic_std,
        'icir'            : icir,
        'ic_positive_pct' : pos_pct,
        't_stat'          : t_stat,
        'factor_decay'    : decay,
        'component_ic'    : component_ic,
    }


def calculate_realized_ic(strat, method: str = 'spearman',
                           report_start: str = None) -> dict:
    """
    Realized IC — correlation between factor score at entry and trade PnL.

    WHAT IT MEASURES
    ─────────────────
    For each entry month, compute the Spearman rank correlation between:
      • Composite factor score at the month-end BEFORE entry
      • Actual realized PnL % from the trade (entry → exit fill price)

    This measures whether the factor's RANKING within the held portfolio is
    correct: did the highest-ranked of the 15 held stocks actually perform
    best? For a top-N strategy, this is the intra-portfolio ranking quality.

    NOTE ON SAMPLE SIZE
    ───────────────────
    With top_n=15 and monthly rebalancing, each month has at most ~5 new
    entries (hysteresis means most of the 15 stocks were already held). The
    min_trades threshold is set to 2 to maximize coverage. Interpret t-stat
    cautiously — small-sample months will dominate.

    Returns
    -------
    dict: realized_ic_series, ic_mean, ic_std, icir, ic_positive_pct,
          t_stat, n_months, n_trades
    """
    self = strat
    from scipy import stats as _scipy_stats

    if not self.position_metadata:
        raise ValueError("No position_metadata — run backtest first.")
    if self.factors is None:
        raise ValueError("Call calculate_factors() first.")

    corr_fn = (
        lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation
        if method == 'spearman'
        else _scipy_stats.pearsonr(x, y)[0]
    )

    # Build trade DataFrame from position_metadata
    rows = []
    for meta in self.position_metadata:
        ep  = meta.get('Entry_Price', np.nan)
        xp  = meta.get('Exit_Price',  np.nan)
        if pd.isna(ep) or ep <= 0 or pd.isna(xp) or xp <= 0:
            continue
        rows.append({
            'Ticker'    : meta['Ticker'],
            'Entry_Date': pd.Timestamp(meta['Entry_Date']),
            'PnL_Pct'   : (xp / ep - 1) * 100.0,
        })
    if not rows:
        print("[Realized IC] No usable trades in position_metadata.")
        return {}

    trades = pd.DataFrame(rows)

    if report_start:
        trades = trades[trades['Entry_Date'] >= pd.Timestamp(report_start)]

    # Map each entry date to the last month-end on or before it
    factor_idx = self.factors.index
    def _last_me(d):
        valid = factor_idx[factor_idx <= d]
        return valid[-1] if len(valid) > 0 else pd.NaT

    trades['Entry_Month'] = trades['Entry_Date'].apply(_last_me)
    trades = trades.dropna(subset=['Entry_Month'])

    # Per-month realized IC
    ic_records = []
    min_trades = 2   # lowered from 3: top_n=15 has very few entries per month

    for month, grp in trades.groupby('Entry_Month'):
        if len(grp) < min_trades:
            continue
        if month not in factor_idx:
            continue
        factor_row = self.factors.loc[month]
        scores, returns = [], []
        for _, row in grp.iterrows():
            ticker = row['Ticker']
            if ticker in factor_row.index and not pd.isna(factor_row[ticker]):
                scores.append(factor_row[ticker])
                returns.append(row['PnL_Pct'])
        if len(scores) < min_trades:
            continue
        ic_records.append({
            'Date'    : month,
            'IC'      : corr_fn(np.array(scores), np.array(returns)),
            'N_trades': len(scores),
        })

    if not ic_records:
        print("[Realized IC] Not enough monthly groups (need >= 2 entries with factor scores).")
        return {}

    ric_df     = pd.DataFrame(ic_records).set_index('Date')
    ric_series = ric_df['IC'].dropna()
    n          = len(ric_series)
    n_trades   = int(ric_df['N_trades'].sum())

    ric_mean = ric_series.mean()
    ric_std  = ric_series.std()
    ricir    = ric_mean / ric_std if ric_std > 0 else 0.0
    pos_pct  = (ric_series > 0).mean()
    t_stat   = ric_mean / (ric_std / np.sqrt(n)) if (n > 0 and ric_std > 0) else 0.0

    print("\n" + "=" * 68)
    print(f" REALIZED IC / ICIR  —  CSM Batch ({method.upper()})")
    print("=" * 68)
    print(f"  Context: IC on HELD positions — factor score vs actual trade")
    print(f"  PnL% grouped by entry month. Measures intra-portfolio ranking")
    print(f"  quality: did highest-ranked of the 15 stocks perform best?")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  Months with >= {min_trades} entries : {n}")
    print(f"  Total trades used    : {n_trades}")
    print(f"  Avg trades / month   : {n_trades/n:.1f}")
    print(f"  IC Mean (Realized)   : {ric_mean:+.4f}   (> 0.05 meaningful)")
    print(f"  IC Std               : {ric_std:.4f}")
    print(f"  ICIR (Realized)      : {ricir:+.3f}   (> 0.2 usable for top-{self.top_n})")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic          : {t_stat:+.2f}   (> 2.0 = significant)")
    if ric_mean > 0.0:
        print(f"\n  ✓ Positive realized IC: within the held portfolio, higher-")
        print(f"    ranked stocks DO deliver better trade outcomes on average.")
    else:
        print(f"\n  ✗ Negative/zero realized IC: factor ranking does not correctly")
        print(f"    order the 15 held stocks by trade outcome.")
    print(f"\n  Note: top_n={self.top_n} is concentrated. Each month has ~ {min_trades}-5 new")
    print(f"  entries. Small sample per month → wide IC distribution is normal.")
    print("=" * 68)

    return {
        'realized_ic_series' : ric_series,
        'ic_mean'            : ric_mean,
        'ic_std'             : ric_std,
        'icir'               : ricir,
        'ic_positive_pct'    : pos_pct,
        't_stat'             : t_stat,
        'n_months'           : n,
        'n_trades'           : n_trades,
    }


def plot_ic(strat, ic_results: dict, filename: str = 'factor_ic_batch.png'):
    """
    Three-panel IC chart:
      Panel 1: Monthly IC bars + 12m rolling mean
      Panel 2: Cumulative IC (persistent positive slope = genuine edge)
      Panel 3: Factor decay bar chart (IC Mean + ICIR at 1/3/6/12m horizons)

    Parameters
    ----------
    ic_results : dict   — output of calculate_ic()
    filename   : str    — PNG filename to save
    """
    self = strat
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    ic_s     = ic_results.get('ic_series', pd.Series(dtype=float))
    ic_roll  = ic_s.rolling(12).mean()
    decay    = ic_results.get('factor_decay', {})
    comp_ic  = ic_results.get('component_ic', {})

    n_panels = 3 + (1 if comp_ic else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=(13, 5 * n_panels))
    if n_panels == 1:
        axes = [axes]

    # Panel 1: Monthly IC bars + rolling mean
    ax = axes[0]
    colors = ['#2ca02c' if v > 0 else '#d62728' for v in ic_s]
    ax.bar(ic_s.index, ic_s, color=colors, width=20, alpha=0.7)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axhline(ic_results.get('ic_mean', 0), color='blue', linestyle='--',
               label=f"Mean IC = {ic_results.get('ic_mean', 0):+.4f}")
    ax.plot(ic_roll.index, ic_roll, color='navy', linewidth=1.5,
            label='12m Rolling IC')
    ax.set_title(
        f"Monthly IC (Spearman | ICIR = {ic_results.get('icir', 0):.3f} | "
        f"t = {ic_results.get('t_stat', 0):+.2f})",
        fontsize=12, fontweight='bold'
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('IC')

    # Panel 2: Cumulative IC
    ax2 = axes[1]
    cumIC = ic_s.cumsum()
    ax2.plot(cumIC.index, cumIC, color='#1f77b4', linewidth=1.5)
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_title('Cumulative IC  (positive slope = persistent predictive edge)',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Cumulative IC')

    # Panel 3: Factor decay
    ax3 = axes[2]
    if decay:
        horizons  = list(decay.keys())
        ic_means  = [decay[h]['ic_mean'] for h in horizons]
        icirs     = [decay[h]['icir']    for h in horizons]
        x = np.arange(len(horizons))
        w = 0.35
        ax3.bar(x - w/2, ic_means, w, label='IC Mean', color='steelblue',  alpha=0.8)
        ax3.bar(x + w/2, icirs,    w, label='ICIR',    color='darkorange', alpha=0.8)
        ax3.axhline(0, color='black', linewidth=0.8)
        ax3.set_xticks(x)
        ax3.set_xticklabels([f'{h}m' for h in horizons])
        ax3.set_title('Factor Decay: IC Mean and ICIR at Multiple Forward Horizons',
                      fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3, axis='y')

    # Panel 4 (optional): Per-component IC
    if comp_ic and n_panels == 4:
        ax4 = axes[3]
        names   = list(comp_ic.keys())
        c_means = [comp_ic[c]['ic_mean'] for c in names]
        c_icirs = [comp_ic[c]['icir']    for c in names]
        x = np.arange(len(names))
        w = 0.35
        ax4.bar(x - w/2, c_means, w, label='IC Mean', color='mediumseagreen', alpha=0.8)
        ax4.bar(x + w/2, c_icirs, w, label='ICIR',    color='coral',          alpha=0.8)
        ax4.axhline(0, color='black', linewidth=0.8)
        ax4.set_xticks(x)
        ax4.set_xticklabels(names)
        ax4.set_title('Per-Component IC (universe-filtered, 12m vs 6m Sharpe)',
                      fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"[IC] Saved IC analysis to '{filename}'")

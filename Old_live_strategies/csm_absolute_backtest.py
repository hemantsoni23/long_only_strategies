"""
csm_backtest — backtest engine, metrics, reporting, IC, and plots for the
Cross-Sectional Individual Momentum (CSM v2.2) strategy.

This module holds everything that operates ON a strategy object but is not part
of the strategy CORE (which lives in csm_v2.py):

  • Event-driven backtest engine          — _run_event_backtest(strat, ...)
  • Public wrappers                        — backtest_event_driven / run_backtest / live_backtest
  • Trade logs                             — get_trade_log, generate_detailed_trade_log
  • Metrics + report                       — compute_metrics, print_report
  • Break / yearly diagnostics             — detect_strategy_breaks, print_yearly_returns,
                                             calculate_trade_stats, plot_performance
  • Information Coefficient analytics       — calculate_ic, calculate_realized_ic, plot_ic
  • Performance plots                      — plot_summary, plot_diagnostics

All functions take the strategy object as the first argument `strat`; moved
class methods alias `self = strat` at the top so their bodies are preserved
verbatim. The strategy must already have had calculate_factors() and
get_positions() called on it before the engine is invoked.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from limit_ordder_manager import LimitOrderManager  

# Correlation backend for the IC functions: use scipy.stats when available, else a
# tiny no-scipy shim (Spearman = Pearson-on-ranks, the same correlation value).
try:
    from scipy import stats as _STATS
except ModuleNotFoundError:
    import types as _types

    def _spearmanr(x, y, nan_policy="omit"):
        s = pd.DataFrame({"x": np.asarray(x, float), "y": np.asarray(y, float)}).dropna()
        c = s["x"].rank().corr(s["y"].rank()) if len(s) > 1 else np.nan
        return _types.SimpleNamespace(correlation=c)

    def _pearsonr(x, y):
        s = pd.DataFrame({"x": np.asarray(x, float), "y": np.asarray(y, float)}).dropna()
        c = s["x"].corr(s["y"]) if len(s) > 1 else np.nan
        return (c, np.nan)

    _STATS = _types.SimpleNamespace(spearmanr=_spearmanr, pearsonr=_pearsonr)


# ════════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN BACKTEST ENGINE
# ════════════════════════════════════════════════════════════════════════════

def _run_event_backtest(
    strat,
    initial_capital: float        = 100_000.0,
    transaction_cost: float       = 0.001,
    risk_free_rate: float         = 0.06,
    # ── Stop-Loss Layers ────────────────────────────────────────────────
    hard_stop_from_entry_pct: float = 0.15,
    hard_stop_from_peak_pct:  float = 0.20,
    atr_cap_percentile:       float = 0.75,
    atr_cap_window:           int   = 63,
    stop_slippage_pct:        float = 0.003,
    # ── Crash-Guard ─────────────────────────────────────────────────────
    bear_sma_window:          int   = 200,
    bear_sma_min_periods:     int   = 180,
    crash_guard_cooldown:     int   = 10,
    # ── Limit Order Manager ─────────────────────────────────────────────
    use_limit_orders:         bool  = False,
    stop_approach_pct:        float = 0.02,
    trail_approach_pct:       float = 0.03,
    order_ttl_days:           int   = 4,
    order_fill_assumption:    str   = 'limit_price',
    # ── Liquid MF Parking ───────────────────────────────────────────────
    use_liquid_mf:            bool  = False,
    liquid_mf_annual_rate:    float = 0.065,
    # ── Event-Driven Extensions ─────────────────────────────────────────
    use_ltp_filter:           bool  = False,   # live_backtest: skip gap-up new entries
    max_entry_gap_pct:        float = 0.02,    # skip entry if open > prev_close × (1+pct)
    label:                    str   = "Event-Driven",
) -> dict:
    """
    Shared engine for backtest_event_driven() and live_backtest().

    Three-layer stop formula (effective_stop = tightest / highest):
      Layer 1 — Chandelier    : peak_high − atr_mult × ATR(capped, D-1)
      Layer 2 — Entry Hard    : entry_price × (1 − hard_stop_from_entry_pct)
      Layer 3 — Peak Hard     : peak_high  × (1 − hard_stop_from_peak_pct)
      effective_stop = max(Layer1, Layer2, Layer3)

    All decisions use only data available at the START of day D (up to and
    including the close of day D-1). The Correlation Guard is evaluated in-loop
    using rolling buffers so it cannot see future volatility.

    Returns
    -------
    dict (stored in self.results):
      equity_curve, portfolio_value, net_returns, executed_weights, turnover,
      cagr, sharpe, sortino, calmar, max_drawdown, ann_volatility,
      win_rate, ann_turnover, ann_signal_turnover
    """
    self = strat

    # ════════════════════════════════════════════════════════════════════
    # GUARD
    # ════════════════════════════════════════════════════════════════════
    if self.positions is None:
        raise ValueError("[Backtest] self.positions is None — call get_positions() first.")

    print("\n" + "=" * 70)
    print(f"[Backtest — {label}]  IndividualMomentum · Corr Guard In-Loop")
    print("=" * 70)
    print(f"  Capital          : ₹{initial_capital:,.0f}")
    print(f"  Transaction Cost : {transaction_cost*100:.3f}% one-way")
    print(f"  Risk-Free Rate   : {risk_free_rate*100:.1f}% p.a.")
    print(f"  Stop (Entry)     : −{hard_stop_from_entry_pct*100:.0f}% from entry price  [Layer 2]")
    print(f"  Stop (Peak)      : −{hard_stop_from_peak_pct*100:.0f}% from peak price   [Layer 3]")
    print(f"  Chandelier       : peak − {self.atr_multiplier}×ATR(capped@{atr_cap_percentile*100:.0f}th/{atr_cap_window}d)  [Layer 1]")
    print(f"  Stop Slippage    : {stop_slippage_pct*100:.2f}%")
    print(f"  Crash Guard      : SMA{bear_sma_window} only  "
          f"| cooldown={crash_guard_cooldown}d")
    print(f"  Limit Orders     : {'ENABLED  stop_approach='+str(stop_approach_pct*100)+'%  TTL='+str(order_ttl_days)+'d' if use_limit_orders else 'DISABLED'}")
    print(f"  Liquid MF Park   : {'ENABLED  @ '+str(liquid_mf_annual_rate*100)+'% p.a.' if use_liquid_mf else 'DISABLED (cash earns RFR)'}")
    print(f"  LTP Gap Filter   : {'ENABLED  max_gap='+str(round(max_entry_gap_pct*100,1))+'%' if use_ltp_filter else 'DISABLED'}")
    print("=" * 70)

    # ════════════════════════════════════════════════════════════════════
    # SECTION 0 — PRE-COMPUTE ALL STATIC DAILY ARRAYS
    # ════════════════════════════════════════════════════════════════════

    # 0-A ── Forward-filled price / high / low ───────────────────────────
    prices_ffill = self.prices.ffill()

    has_highs = self.highs is not None and not self.highs.empty
    has_lows  = self.lows  is not None and not self.lows.empty

    highs_ffill = self.highs.ffill() if has_highs else prices_ffill.copy()
    lows_ffill  = self.lows.ffill()  if has_lows  else prices_ffill.copy()

    # 0-B ── Open proxy (prev_close shifted 1 day, or real opens) ────────
    has_opens  = (hasattr(self, 'opens') and self.opens is not None
                  and not self.opens.empty)
    if has_opens:
        open_proxy = (
            self.opens
            .reindex(index=prices_ffill.index, columns=prices_ffill.columns)
            .ffill()
        )
    else:
        open_proxy = prices_ffill.shift(1)      # prev close, shifted — no lookahead

    # 0-C ── ATR (capped, shifted by 1 day) ──────────────────────────────
    if has_highs and has_lows:
        _prev_c = prices_ffill.shift(1)
        _hl     = highs_ffill - lows_ffill
        _hc     = (highs_ffill - _prev_c).abs()
        _lc     = (lows_ffill  - _prev_c).abs()
        _tr     = _hl.combine(_hc, np.maximum).combine(_lc, np.maximum)
        _atr_raw = _tr.rolling(
            window      = self.atr_period,
            min_periods = max(1, self.atr_period // 2),
        ).mean()
        _atr_cap = _atr_raw.rolling(
            window      = atr_cap_window,
            min_periods = max(1, atr_cap_window // 2),
        ).quantile(atr_cap_percentile)
        atr_for_stops = _atr_raw.clip(upper=_atr_cap).shift(1)   # ← shift here
    else:
        atr_for_stops = prices_ffill.multiply(0.02).shift(1)     # 2% fallback

    # 0-D ── Crash-guard regime filter — SMA200 ONLY (no fast ROC) ────────
    if self.benchmark is not None:
        _bench    = self.benchmark.reindex(self.prices.index).ffill()
        _sma_slow = _bench.rolling(
            window      = bear_sma_window,
            min_periods = bear_sma_min_periods,
        ).mean().shift(1)          # shift → day i uses SMA computed up to day i-1
        is_bearish = (_bench < _sma_slow).shift(1).fillna(False)
    else:
        is_bearish = pd.Series(False, index=self.prices.index)

    # 0-E ── Monthly target weights → daily (shifted 1 trading day) ──────
    monthly_signal = (
        self.positions
        .reindex(self.prices.index, method='ffill')
        .shift(1)
        .fillna(0.0)
    )

    # 0-F ── Pre-compute daily returns (for in-loop Correlation Guard) ────
    _dr_all = prices_ffill.pct_change(fill_method=None).fillna(0.0)

    # 0-G ── Limit Order Manager ─────────────────────────────────────────
    # Gated by use_trailing: the LOM is a chandelier-based advance-order layer,
    # so when trailing is disabled it is bypassed and STEP E hard stops apply.
    order_manager = None
    if use_limit_orders and self.use_trailing:
        try:
            from limit_ordder_manager import LimitOrderManager
            order_manager = LimitOrderManager(
                stop_approach_pct  = stop_approach_pct,
                trail_approach_pct = trail_approach_pct,
                ttl_days           = order_ttl_days,
                fill_assumption    = order_fill_assumption,
                verbose            = False,
            )
            print(f"[Backtest] LimitOrderManager ready  "
                  f"approach={stop_approach_pct*100:.1f}%  "
                  f"trail={trail_approach_pct*100:.1f}%  "
                  f"TTL={order_ttl_days}d  fill={order_fill_assumption}")
        except ImportError:
            print("[Backtest] WARNING: limit_ordder_manager not importable — "
                  "continuing without limit orders.")

    # ════════════════════════════════════════════════════════════════════
    # SECTION 1 — MUTABLE STATE (persist across loop iterations)
    # ════════════════════════════════════════════════════════════════════
    # entry_prices[stock]  Price on the FIRST day held in current trade (Layer-2).
    # peak_highs[stock]    Running max of daily highs since entry (Layers 1 & 3),
    #                      updated AFTER exit checks using the previous day's high.
    # Both dicts are cleared on crash-guard events and pruned on exit.
    entry_prices: dict = {}
    peak_highs:   dict = {}

    executed_weights_list: list = []
    self._trade_events            = []
    self._backtest_initial_capital = initial_capital

    # Exit counters (for summary report)
    n_stop_fallback = 0   # fired by our own stop check
    n_stop_lom      = 0   # fired by LimitOrderManager
    n_crash         = 0
    n_rebalance     = 0
    n_signal_drop   = 0

    # Buy-once (use_rebalance=False) no-re-entry guard: once a name exits (any
    # reason) it is never re-bought. Inert when use_rebalance=True (default).
    _perm_exited: set = set()

    # Post-STOP_HIT re-entry cooldown: ticker -> trading-day index until which
    # re-entry is blocked. Inert when reentry_cooldown_days == 0 (default).
    _stop_cooldown_until: dict = {}
    _reentry_cd = int(getattr(self, 'reentry_cooldown_days', 0) or 0)
    _cd_losers  = bool(getattr(self, 'cooldown_losers_only', False))  # cooldown only after losing stops

    # Crash-guard cooldown counter — suppresses new entries after a CG fire.
    cg_cooldown_remaining: int = 0

    # Pre-compute prev_day_high ONCE outside the loop (O(N) not O(N²)).
    prev_day_high = highs_ffill.shift(1)

    # ── In-loop Correlation Guard rolling buffers ─────────────────────────
    # _port_ret_buf stores UNSCALED gross daily portfolio returns (last CORR_WIN).
    # _pre_scale_w_buf stores pre-CG-scale executed weight Series (last CORR_WIN).
    # Appended at the END of each iteration so day D+1's guard reads prior data.
    CORR_WIN       = 21
    CORR_THRESHOLD = 0.8        # ratio: port_vol / avg_stock_vol  > threshold → scale 0.5
    _port_ret_buf:    list = []  # unscaled gross daily portfolio returns
    _pre_scale_w_buf: list = []  # pre-CG-scale executed weight Series
    n_corr_fired:     int  = 0   # days where CG scaled exposure down to 50%

    # ════════════════════════════════════════════════════════════════════
    # SECTION 2 — MAIN DAILY LOOP
    # ════════════════════════════════════════════════════════════════════
    for i, date in enumerate(self.prices.index):

        # ── Day 0: no history — initialise with zero weights and skip ────
        if i == 0:
            _zero_w0 = pd.Series(0.0, index=self.prices.columns)
            executed_weights_list.append(_zero_w0)
            _pre_scale_w_buf.append(_zero_w0)
            _port_ret_buf.append(0.0)
            continue

        prev_weights = executed_weights_list[i - 1]
        prev_held    = set(prev_weights.index[prev_weights > 1e-6])

        # Today's monthly-signal target (shifted — no lookahead)
        target_weights = monthly_signal.iloc[i].copy()

        # First trading day of a new calendar month? (REBALANCE vs SIGNAL_DROP)
        is_new_month = (
            self.prices.index[i].month != self.prices.index[i - 1].month
        )

        # exited_today: tickers already given an EXIT event this iteration.
        exited_today: set = set()

        # ── STEP C ── CRASH GUARD ────────────────────────────────────────
        # On bearish days: exit all positions at today's close, go to cash,
        # cancel all pending LOM orders, clear tracking dicts. The STOP-FLOOR
        # FIX applies the same gap-down / intraday-touch logic as Step E, then
        # takes the stop fill (never optimistic vs the close).
        if is_bearish.iloc[i]:
            for stock in prev_held:
                _cg_close = float(prices_ffill.at[date, stock])
                _cg_fill  = _cg_close   # default: exit at market close

                if stock in entry_prices and stock in peak_highs:
                    try:
                        _atr_cg = float(atr_for_stops.at[date, stock])
                        if pd.isna(_atr_cg) or _atr_cg <= 0:
                            _atr_cg = _cg_close * 0.02
                        _peak_cg     = peak_highs[stock]
                        _chand_cg    = (_peak_cg - (self.atr_multiplier * _atr_cg)) if self.use_trailing else -np.inf
                        _entry_stop  = entry_prices[stock] * (1.0 - hard_stop_from_entry_pct)
                        _peak_stop   = _peak_cg * (1.0 - hard_stop_from_peak_pct)
                        _eff_stop_cg = max(_chand_cg, _entry_stop, _peak_stop)

                        _low_cg  = float(lows_ffill.at[date, stock])
                        _open_cg = float(open_proxy.at[date, stock])
                        if pd.isna(_low_cg)  or _low_cg  <= 0: _low_cg  = _cg_close
                        if pd.isna(_open_cg) or _open_cg <= 0: _open_cg = _cg_close

                        if _low_cg <= _eff_stop_cg:
                            # Stop was breached intraday — compute stop fill
                            if _open_cg <= _eff_stop_cg:
                                _stop_fill = _open_cg   # gap-down: fill at open
                            else:
                                _stop_fill = _eff_stop_cg * (1.0 - stop_slippage_pct)
                            # Only improve fill vs close (stop fill is BETTER = higher price)
                            _cg_fill = _stop_fill
                    except Exception:
                        pass  # data missing — fall back to close

                self._trade_events.append({
                    'type'  : 'EXIT',
                    'ticker': stock,
                    'date'  : date,
                    'price' : _cg_fill,
                    'weight': 0.0,
                    'reason': 'CRASH_GUARD',
                })
                exited_today.add(stock)
                n_crash += 1

            target_weights[:] = 0.0
            entry_prices.clear()
            peak_highs.clear()

            if order_manager is not None:
                order_manager.cancel_all(reason='CRASH_GUARD', date=date)

            # Reset cooldown on every CG fire.
            cg_cooldown_remaining = crash_guard_cooldown

            # Append zero entries to rolling buffers BEFORE the continue so the
            # buffers stay date-aligned and the corr guard sees zero exposure.
            _cg_zero_w = pd.Series(0.0, index=self.prices.columns)
            _pre_scale_w_buf.append(_cg_zero_w)
            if len(_pre_scale_w_buf) > CORR_WIN + 5:
                _pre_scale_w_buf.pop(0)
            _port_ret_buf.append(0.0)
            if len(_port_ret_buf) > CORR_WIN + 5:
                _port_ret_buf.pop(0)

            executed_weights_list.append(target_weights.copy())
            continue     # skip all remaining steps on crash days

        # ── STEP C2 ── COOLDOWN (suppress new entries after CG) ───────────
        # Existing positions are kept; only NEW entries (not in prev_held) blocked.
        if cg_cooldown_remaining > 0:
            cg_cooldown_remaining -= 1
            for stock in list(target_weights.index):
                if stock not in prev_held and target_weights[stock] > 1e-6:
                    target_weights[stock] = 0.0

        # ── STEP C3 ── POST-STOP_HIT RE-ENTRY COOLDOWN ────────────────────
        # Zero the weight of any would-be re-entry (not currently held) whose
        # ticker is still inside its post-STOP_HIT cooldown window. This MUST
        # zero target_weights (not merely skip the entry-log event) so the
        # capital is genuinely freed and the executed book / turnover / equity
        # reflect the cooldown. Mirrors the STEP C2 crash-cooldown pattern.
        if _reentry_cd > 0 and _stop_cooldown_until:
            for stock in list(target_weights.index):
                if (stock not in prev_held
                        and target_weights[stock] > 1e-6
                        and i < _stop_cooldown_until.get(stock, 0)):
                    target_weights[stock] = 0.0

        # ── STEP D ── LIMIT ORDER MANAGER ────────────────────────────────
        # Runs BEFORE the fallback stop check. Places advance stop/trailing
        # orders and fills pending ones; fills are zeroed + logged + marked so
        # the fallback stop check skips them.
        lom_handled: set = set()   # tickers filled by LOM this day

        if order_manager is not None:
            _t_open  = open_proxy.iloc[i]
            _t_high  = highs_ffill.iloc[i]
            _t_low   = lows_ffill.iloc[i]
            _t_close = prices_ffill.iloc[i]
            _p_close = prices_ffill.iloc[i - 1]
            _atr_dict = atr_for_stops.iloc[i].dropna().to_dict()

            # Cancel LOM orders for stocks the monthly signal is dropping
            for _stk in list(order_manager._pending_orders.keys()):
                if (_stk not in prev_held
                        and target_weights.get(_stk, 0.0) < 1e-6):
                    order_manager.cancel_order(
                        _stk, reason='SIGNAL_DROPPED', date=date
                    )

            target_weights, day_meta = order_manager.process_day(
                date            = date,
                current_weights = target_weights,
                entry_prices    = entry_prices,
                peak_highs      = peak_highs,
                atr_values      = _atr_dict,
                atr_multiplier  = self.atr_multiplier,
                today_open      = _t_open,
                today_high      = _t_high,
                today_low       = _t_low,
                today_close     = _t_close,
                prev_close      = _p_close,
            )

            # Process LOM fills
            for fill in day_meta.get('fills', []):
                _stk = fill.ticker
                if _stk in exited_today:
                    continue    # crash guard already logged exit

                _fill_px = (getattr(fill, 'fill_price', None)
                            or float(prices_ffill.at[date, _stk]))

                self._trade_events.append({
                    'type'    : 'EXIT',
                    'ticker'  : _stk,
                    'date'    : date,
                    'price'   : float(_fill_px),
                    'weight'  : 0.0,
                    'reason'  : 'STOP_HIT',
                    'stop_type': fill.order_type,   # 'STOP_LOSS' | 'TRAILING_STOP'
                })
                exited_today.add(_stk)
                lom_handled.add(_stk)
                n_stop_lom += 1
                _entry_cd = entry_prices.pop(_stk, None)
                peak_highs.pop(_stk,   None)
                if _reentry_cd > 0 and (not _cd_losers or (_entry_cd and _fill_px < _entry_cd)):
                    _stop_cooldown_until[_stk] = i + _reentry_cd

        # ── STEP E ── FALLBACK STOP CHECK ────────────────────────────────
        # For every stock held yesterday, still wanted today, not already exited.
        # Peak highs used here = running max up to yesterday (updated in Step H).
        # FILL PRICE: gap-down (open <= stop) → open; intraday touch → stop×(1−slip).
        for stock in prev_held:
            if stock in exited_today or stock in lom_handled:
                continue

            # Skip if monthly signal is dropping this stock (Step F handles it)
            if target_weights.get(stock, 0.0) < 1e-6:
                continue

            today_close = float(prices_ffill.at[date, stock])
            today_low   = float(lows_ffill.at[date, stock])
            today_open  = float(open_proxy.at[date, stock])

            if today_close <= 0 or pd.isna(today_close):
                continue
            if today_low <= 0 or pd.isna(today_low):
                today_low = today_close
            if today_open <= 0 or pd.isna(today_open):
                today_open = today_close

            _atr = float(atr_for_stops.at[date, stock])
            if pd.isna(_atr) or _atr <= 0:
                _atr = today_close * 0.02    # 2% fallback

            if stock not in entry_prices:
                entry_prices[stock] = today_close
            if stock not in peak_highs:
                peak_highs[stock]   = today_close

            # ── Three-layer stop ─────────────────────────────────────────
            # peak_highs[stock] here is the max-high up to yesterday
            # Use high-vol multiplier when appropriate:
            is_hv       = bool(is_high_vol.iloc[i]) if hasattr(self, '_is_high_vol') else False
            _atr_mult   = self.atr_multiplier_high_vol if is_hv else self.atr_multiplier
            _peak   = peak_highs[stock]
            chandelier_stop = (_peak - (_atr_mult * _atr)) if self.use_trailing else -np.inf

            entry_hard_stop = entry_prices[stock] * (1.0 - hard_stop_from_entry_pct)
            peak_hard_stop  = _peak * (1.0 - hard_stop_from_peak_pct)
            effective_stop  = max(chandelier_stop, entry_hard_stop, peak_hard_stop)

            if today_low > effective_stop:
                continue    # Stop not touched — keep holding

            # ── STOP TRIGGERED — determine realistic fill price ──────────
            if today_open <= effective_stop:
                fill_px = today_open                       # gap-down: fill at open
            else:
                fill_px = effective_stop * (1.0 - stop_slippage_pct)   # intraday touch

            # Sub-classify the stop: entry-hard binding = classic stop-loss;
            # chandelier/peak-anchored binding = trailing (win/loss split later).
            _stop_type = ('STOP_LOSS'
                          if entry_hard_stop >= max(chandelier_stop, peak_hard_stop)
                          else 'TRAILING_STOP')

            self._trade_events.append({
                'type'    : 'EXIT',
                'ticker'  : stock,
                'date'    : date,
                'price'   : float(fill_px),
                'weight'  : 0.0,
                'reason'  : 'STOP_HIT',
                'stop_type': _stop_type,
            })
            exited_today.add(stock)
            n_stop_fallback += 1

            target_weights[stock] = 0.0
            _entry_cd = entry_prices.pop(stock, None)
            peak_highs.pop(stock,   None)
            if _reentry_cd > 0 and (not _cd_losers or (_entry_cd and fill_px < _entry_cd)):
                _stop_cooldown_until[stock] = i + _reentry_cd

        # ── LTP GAP FILTER (live_backtest only) ───────────────────────────
        # Applied to NEW entries only (not in prev_held). Skip when today's open
        # has gapped up more than max_entry_gap_pct above the previous close.
        if use_ltp_filter and max_entry_gap_pct > 0:
            for _stk_ltp in list(target_weights.index):
                if _stk_ltp in prev_held:
                    continue          # continuation position — N/A
                if target_weights[_stk_ltp] < 1e-6:
                    continue          # already zero
                _open_ltp  = float(open_proxy.at[date, _stk_ltp])
                _pclose_ltp = float(prices_ffill.iloc[i - 1][_stk_ltp])
                if (not pd.isna(_open_ltp)  and _open_ltp  > 0
                        and not pd.isna(_pclose_ltp) and _pclose_ltp > 0):
                    if _open_ltp / _pclose_ltp - 1.0 > max_entry_gap_pct:
                        target_weights[_stk_ltp] = 0.0

        # ── STEP F ── REBALANCE / SIGNAL-DROP EXITS ──────────────────────
        # Stocks held yesterday but not in today's target, not yet logged.
        current_held = set(target_weights.index[target_weights > 1e-6])

        for stock in prev_held:
            if stock in current_held:
                continue    # still held — not an exit
            if stock in exited_today:
                continue    # already logged

            _ep_open = float(open_proxy.at[date, stock])
            _ep_close = float(prices_ffill.at[date, stock])
            _ep = _ep_open if (not pd.isna(_ep_open) and _ep_open > 0) else _ep_close
            _reason = 'REBALANCE' if is_new_month else 'SIGNAL_DROP'
            self._trade_events.append({
                'type'  : 'EXIT',
                'ticker': stock,
                'date'  : date,
                'price' : _ep,
                'weight': 0.0,
                'reason': _reason,
            })
            exited_today.add(stock)
            n_rebalance   += (1 if _reason == 'REBALANCE'   else 0)
            n_signal_drop += (1 if _reason == 'SIGNAL_DROP' else 0)
            entry_prices.pop(stock, None)
            peak_highs.pop(stock,   None)

        # ── IN-LOOP CORRELATION GUARD ─────────────────────────────────────
        # Uses ONLY prior-day data in the rolling buffers — zero lookahead.
        #   port_vol  = std of last CORR_WIN unscaled gross daily returns
        #   avg_s_vol = weighted avg of each stock's CORR_WIN daily vol
        #   if port_vol / avg_s_vol > CORR_THRESHOLD → scale all weights 50%
        corr_scale = 1.0
        if len(_port_ret_buf) >= CORR_WIN:
            _pbuf  = np.array(_port_ret_buf[-CORR_WIN:])
            _p_vol = float(_pbuf.std())
            if _p_vol > 0 and _pre_scale_w_buf:
                _prev_psw = _pre_scale_w_buf[-1]   # yesterday's pre-scale weights
                _w_sum    = float(_prev_psw.sum())
                if _w_sum > 0:
                    _hist_start = max(0, i - CORR_WIN)
                    _s_std      = _dr_all.iloc[_hist_start:i].std()
                    _avg_s_vol  = float((_s_std * _prev_psw).sum() / _w_sum)
                    if _avg_s_vol > 0 and _p_vol / _avg_s_vol > CORR_THRESHOLD:
                        corr_scale = 0.5

        # Snapshot pre-scale weights (used by tomorrow's corr guard and buffer)
        _pre_scale_w = target_weights.copy()

        if corr_scale < 1.0:
            target_weights = target_weights * corr_scale   # new Series, same index
            n_corr_fired  += 1

        # ── STEP G ── NEW ENTRY LOGGING ───────────────────────────────────
        # Stocks in today's target that were NOT held yesterday.
        for stock in current_held:
            if stock in prev_held:
                continue    # continuation — not a new entry
            if (not self.use_rebalance) and stock in _perm_exited:
                continue    # buy-once mode: never re-enter a stopped name
            # NOTE: post-STOP_HIT cooldown is enforced in STEP C3 by zeroing the
            # weight (so a blocked name is never in current_held here). No check needed.

            _ep = float(open_proxy.at[date, stock])
            if pd.isna(_ep) or _ep <= 0:
                _ep = float(prices_ffill.at[date, stock])
            self._trade_events.append({
                'type'  : 'ENTRY',
                'ticker': stock,
                'date'  : date,
                'price' : _ep,
                'weight': float(target_weights.get(stock, 0.0)),
                'reason': '',
            })
            entry_prices[stock] = _ep
            peak_highs[stock]   = _ep

        # ── STEP H ── UPDATE PEAK HIGHS (after all exits resolved) ────────
        # For continuation stocks: update peak with YESTERDAY's high.
        for stock in current_held:
            if stock not in entry_prices:
                # Defensive: initialise if somehow missing
                entry_prices[stock] = float(prices_ffill.at[date, stock])
                peak_highs[stock]   = float(prices_ffill.at[date, stock])
                continue

            if stock in prev_held:
                _yday_high = float(prev_day_high.at[date, stock])
                if not pd.isna(_yday_high) and _yday_high > 0:
                    peak_highs[stock] = max(peak_highs[stock], _yday_high)
            # New entries (NOT in prev_held): peak stays at entry price (set in G)

        # Prune tracking for any stock that is no longer in the portfolio
        for _stk in list(entry_prices.keys()):
            if _stk not in current_held:
                entry_prices.pop(_stk)
                peak_highs.pop(_stk, None)

        # ── STEP I ── SAVE WEIGHTS + UPDATE ROLLING BUFFERS ─────────────────
        executed_weights_list.append(target_weights.copy())

        # Append pre-scale weights for tomorrow's corr guard.
        _pre_scale_w_buf.append(_pre_scale_w)
        if len(_pre_scale_w_buf) > CORR_WIN + 5:
            _pre_scale_w_buf.pop(0)

        # Today's unscaled gross portfolio return using pre-scale weights.
        _dr_today   = _dr_all.iloc[i]
        _today_pret = float((_pre_scale_w * _dr_today).sum())
        _port_ret_buf.append(_today_pret)
        if len(_port_ret_buf) > CORR_WIN + 5:
            _port_ret_buf.pop(0)

        # Buy-once mode (use_rebalance=False): remember names exited today so
        # STEP G never re-buys them from the frozen target.
        if not self.use_rebalance:
            _perm_exited.update(exited_today)

    # ════════════════════════════════════════════════════════════════════
    # SECTION 3 — CLOSE OPEN POSITIONS AT END OF BACKTEST
    # ════════════════════════════════════════════════════════════════════
    _last_date = self.prices.index[-1]
    _last_w    = executed_weights_list[-1]

    _already_closed = {
        e['ticker'] for e in self._trade_events
        if e['date'] == _last_date and e['type'] == 'EXIT'
    }
    for stock in _last_w.index[_last_w > 1e-6]:
        if stock not in _already_closed:
            self._trade_events.append({
                'type'  : 'EXIT',
                'ticker': stock,
                'date'  : _last_date,
                'price' : float(prices_ffill.at[_last_date, stock]),
                'weight': 0.0,
                'reason': 'END_OF_PERIOD',
            })

    # Expose forward-filled prices for generate_detailed_trade_log()
    self._prices_ffill = prices_ffill

    # ════════════════════════════════════════════════════════════════════
    # SECTION 4 — BUILD EXECUTED-WEIGHTS DATAFRAME
    # ════════════════════════════════════════════════════════════════════
    executed_weights = pd.DataFrame(
        executed_weights_list, index=self.prices.index
    ).fillna(0.0)

    # ════════════════════════════════════════════════════════════════════
    # SECTION 5 — PORTFOLIO RETURN CALCULATION
    # ════════════════════════════════════════════════════════════════════
    # FILL-PRICE EQUITY-CURVE CORRECTION: the base series uses plain
    # pct_change() (correct for every CONTINUATION day). On the two boundary
    # days of every trade it is patched:
    #   ENTRY DAY : close_T / entry_fill_price − 1
    #   EXIT DAY  : exit_fill_price / close_{T-1} − 1   (close_{T-1}, NOT open_proxy)
    # Same-day entry+exit composes both legs into exit_fill / entry_fill − 1.
    # _prev_close_for_ret is always prices_ffill.shift(1), independent of opens.
    _daily_ret = self.prices.pct_change(fill_method=None).fillna(0.0)
    _prev_close_for_ret = prices_ffill.shift(1)   # always yesterday's close —
                                                    # independent of open_proxy

    for _ev in self._trade_events:
        _d_ev = _ev['date']
        _s_ev = _ev['ticker']
        _fp_ev = _ev['price']

        if not (_d_ev in _daily_ret.index and _s_ev in _daily_ret.columns
                and _fp_ev and _fp_ev > 0):
            continue

        if _ev['type'] == 'ENTRY':
            # close_T / entry_fill_price − 1
            _close_ev = float(prices_ffill.at[_d_ev, _s_ev])
            if _close_ev > 0 and not pd.isna(_close_ev):
                _daily_ret.at[_d_ev, _s_ev] = _close_ev / _fp_ev - 1.0

        elif _ev['type'] == 'EXIT':
            # exit_fill_price / close_{T-1} − 1   (close_{T-1}, NOT open_proxy)
            _pc_ev = float(_prev_close_for_ret.at[_d_ev, _s_ev])
            if _pc_ev > 0 and not pd.isna(_pc_ev):
                _exit_leg = _fp_ev / _pc_ev - 1.0
                # Same-day entry+exit: compose into a single round-trip return.
                _same_day_entry = any(
                    e['type'] == 'ENTRY' and e['date'] == _d_ev
                    and e['ticker'] == _s_ev and e['price'] and e['price'] > 0
                    for e in self._trade_events
                )
                if _same_day_entry:
                    _entry_fp = next(
                        e['price'] for e in self._trade_events
                        if e['type'] == 'ENTRY' and e['date'] == _d_ev
                        and e['ticker'] == _s_ev
                    )
                    _daily_ret.at[_d_ev, _s_ev] = _fp_ev / _entry_fp - 1.0
                else:
                    _daily_ret.at[_d_ev, _s_ev] = _exit_leg

    _eq_ret     = (executed_weights * _daily_ret).sum(axis=1)

    _total_w    = executed_weights.sum(axis=1)
    _cash_w     = (1.0 - _total_w).clip(lower=0.0)
    _daily_rfr  = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0

    # Liquid MF parking: when fully idle, cash earns liquid MF rate
    if use_liquid_mf:
        _daily_lmf = (1.0 + liquid_mf_annual_rate) ** (1.0 / 252) - 1.0
        _is_idle   = _total_w < 1e-6
        _cash_rate = pd.Series(_daily_rfr, index=self.prices.index)
        _cash_rate[_is_idle] = _daily_lmf
        _cash_ret  = _cash_w * _cash_rate
    else:
        _cash_ret  = _cash_w * _daily_rfr

    _w_chg      = executed_weights.diff().abs().sum(axis=1)
    _txn_cost   = _w_chg * transaction_cost

    net_ret     = _eq_ret + _cash_ret - _txn_cost
    eq_curve    = (1.0 + net_ret).cumprod()
    port_value  = eq_curve * initial_capital

    # ════════════════════════════════════════════════════════════════════
    # SECTION 6 — PERFORMANCE METRICS
    # ════════════════════════════════════════════════════════════════════
    _nyears  = (eq_curve.index[-1] - eq_curve.index[0]).days / 365.25
    cagr     = (eq_curve.iloc[-1]) ** (1.0 / _nyears) - 1.0 if _nyears > 0 else 0.0
    ann_vol  = net_ret.std() * np.sqrt(252)

    _excess  = net_ret - _daily_rfr
    sharpe   = (np.sqrt(252) * _excess.mean() / net_ret.std()
                if net_ret.std() > 0 else 0.0)

    _dn      = net_ret.clip(upper=0.0)
    _dndev   = np.sqrt((_dn ** 2).mean())                      # daily only
    sortino  = (np.sqrt(252) * net_ret.mean() / _dndev if _dndev > 0 else 0.0)

    _rmax    = eq_curve.cummax()
    _dd      = (eq_curve / _rmax) - 1.0
    max_dd   = _dd.min()
    calmar   = cagr / abs(max_dd) if max_dd != 0 else 0.0

    _mret    = port_value.resample('ME').last().pct_change().dropna()
    win_rate = (_mret > 0).mean()
    ann_turn = _w_chg.sum() / _nyears if _nyears > 0 else 0.0
    sig_turn = (self.positions.diff().abs().sum(axis=1).sum()
                / _nyears if _nyears > 0 else 0.0)

    # ════════════════════════════════════════════════════════════════════
    # SECTION 7 — STORE RESULTS & PRINT SUMMARY
    # ════════════════════════════════════════════════════════════════════
    self.results = {
        # Time-series
        'equity_curve'        : eq_curve,
        'portfolio_value'     : port_value,
        'net_returns'         : net_ret,
        'executed_weights'    : executed_weights,
        'turnover'            : _w_chg,          # trading ACTIVITY (sum |Δweight|/day) — not a cost
        'txn_cost_daily'      : _txn_cost,        # actual cost drag PAID each day (= turnover × cost rate)
        # Scalars
        'total_return'        : float(eq_curve.iloc[-1] - 1.0),
        'cagr'                : cagr,
        'sharpe'              : sharpe,
        'sortino'             : sortino,
        'calmar'              : calmar,
        'max_drawdown'        : max_dd,
        'ann_volatility'      : ann_vol,
        'win_rate'            : win_rate,
        'ann_turnover'        : ann_turn,
        'ann_signal_turnover' : sig_turn,
        'ann_txn_cost_pct'    : (_txn_cost.sum() / _nyears if _nyears > 0 else 0.0),  # real TC drag, annualized
        # Config actually used — stored so downstream slicing/reporting (compute_metrics,
        # print_report) recompute against the SAME rates the backtest ran with, instead
        # of falling back to hardcoded constants.
        'risk_free_rate'       : risk_free_rate,
        'transaction_cost_rate': transaction_cost,
        # Liquid MF config (for downstream reporting)
        'use_liquid_mf'       : use_liquid_mf,
        'liquid_mf_annual_rate': liquid_mf_annual_rate if use_liquid_mf else 0.0,
    }

    if order_manager is not None:
        self._order_manager = order_manager
        order_manager.print_backtest_impact()

    # ── Final summary ─────────────────────────────────────────────────
    _tot = max(n_stop_fallback + n_stop_lom + n_crash + n_rebalance + n_signal_drop, 1)
    _n_days = len(self.prices.index)
    print("\n" + "=" * 70)
    print(f"[Backtest — {label}]  COMPLETED")
    print("=" * 70)
    print(f"  Exit Breakdown:")
    print(f"    STOP_HIT  (fallback stop check) : {n_stop_fallback:>5}  ({n_stop_fallback/_tot*100:.1f}%)")
    print(f"    STOP_HIT  (limit order manager) : {n_stop_lom:>5}  ({n_stop_lom/_tot*100:.1f}%)")
    print(f"    CRASH_GUARD                     : {n_crash:>5}  ({n_crash/_tot*100:.1f}%)")
    print(f"    REBALANCE                       : {n_rebalance:>5}  ({n_rebalance/_tot*100:.1f}%)")
    print(f"    SIGNAL_DROP                     : {n_signal_drop:>5}  ({n_signal_drop/_tot*100:.1f}%)")
    print(f"    ─────────────────────────────────────────────────────")
    print(f"    TOTAL                           : {_tot:>5}")
    print(f"  Corr Guard (in-loop, scaled 50%) : {n_corr_fired:>5} days "
          f"({n_corr_fired / _n_days * 100:.1f}% of trading days)")
    print(f"  ─────────────────────────────────────────────────────")
    print(f"  CAGR           : {cagr*100:>8.2f}%")
    print(f"  Max Drawdown   : {max_dd*100:>8.2f}%")
    print(f"  Sharpe Ratio   : {sharpe:>8.3f}")
    print(f"  Sortino Ratio  : {sortino:>8.3f}")
    print(f"  Calmar Ratio   : {calmar:>8.3f}")
    print(f"  Ann Volatility : {ann_vol*100:>8.2f}%")
    print(f"  Win Rate (Mo)  : {win_rate*100:>8.1f}%")
    print(f"  Ann Turnover   : {ann_turn:>8.2f}×   (trading ACTIVITY — sum |Δweight|, not a cost)")
    print(f"  Ann TC Drag    : {(_txn_cost.sum()/_nyears if _nyears>0 else 0.0)*100:>7.2f}%   (= turnover × {transaction_cost*100:.3f}% cost rate; already deducted daily above)")
    print("=" * 70)

    return self.results


# ════════════════════════════════════════════════════════════════════════════
# PUBLIC WRAPPERS
# ════════════════════════════════════════════════════════════════════════════

def backtest_event_driven(
    strat,
    initial_capital: float          = 100_000.0,
    transaction_cost: float         = 0.001,
    risk_free_rate: float           = 0.06,
    hard_stop_from_entry_pct: float = 0.15,
    hard_stop_from_peak_pct:  float = 0.20,
    atr_cap_percentile:       float = 0.75,
    atr_cap_window:           int   = 63,
    stop_slippage_pct:        float = 0.003,
    bear_sma_window:          int   = 200,
    bear_sma_min_periods:     int   = 180,
    crash_guard_cooldown:     int   = 10,
    use_limit_orders:         bool  = False,
    stop_approach_pct:        float = 0.02,
    trail_approach_pct:       float = 0.03,
    order_ttl_days:           int   = 4,
    order_fill_assumption:    str   = 'limit_price',
    use_liquid_mf:            bool  = False,
    liquid_mf_annual_rate:    float = 0.065,
) -> dict:
    """
    Fully event-driven backtest with in-loop Correlation Guard.

    Every decision uses only data available at the START of day D (data up to
    and including the close of day D-1). Use this as the primary backtest for
    research and strategy development.
    """
    self = strat
    return _run_event_backtest(
        strat,
        initial_capital          = initial_capital,
        transaction_cost         = transaction_cost,
        risk_free_rate           = risk_free_rate,
        hard_stop_from_entry_pct = hard_stop_from_entry_pct,
        hard_stop_from_peak_pct  = hard_stop_from_peak_pct,
        atr_cap_percentile       = atr_cap_percentile,
        atr_cap_window           = atr_cap_window,
        stop_slippage_pct        = stop_slippage_pct,
        bear_sma_window          = bear_sma_window,
        bear_sma_min_periods     = bear_sma_min_periods,
        crash_guard_cooldown     = crash_guard_cooldown,
        use_limit_orders         = use_limit_orders,
        stop_approach_pct        = stop_approach_pct,
        trail_approach_pct       = trail_approach_pct,
        order_ttl_days           = order_ttl_days,
        order_fill_assumption    = order_fill_assumption,
        use_liquid_mf            = use_liquid_mf,
        liquid_mf_annual_rate    = liquid_mf_annual_rate,
        use_ltp_filter           = False,
        max_entry_gap_pct        = 0.0,
        label                    = "Event-Driven",
    )


# Alias to mirror momentum_backtest.run_backtest(strat, ...)
run_backtest = backtest_event_driven


def live_backtest(
    strat,
    initial_capital: float          = 100_000.0,
    transaction_cost: float         = 0.001,
    risk_free_rate: float           = 0.06,
    hard_stop_from_entry_pct: float = 0.15,
    hard_stop_from_peak_pct:  float = 0.20,
    atr_cap_percentile:       float = 0.75,
    atr_cap_window:           int   = 63,
    stop_slippage_pct:        float = 0.003,
    bear_sma_window:          int   = 200,
    bear_sma_min_periods:     int   = 180,
    crash_guard_cooldown:     int   = 10,
    use_limit_orders:         bool  = False,
    stop_approach_pct:        float = 0.02,
    trail_approach_pct:       float = 0.03,
    order_ttl_days:           int   = 4,
    order_fill_assumption:    str   = 'limit_price',
    use_liquid_mf:            bool  = False,
    liquid_mf_annual_rate:    float = 0.065,
    max_entry_gap_pct:        float = 0.02,
) -> dict:
    """
    Live-simulation backtest: event-driven + LTP gap filter on new entries.

    Identical to backtest_event_driven() except new entries are skipped when
    today's market open has already gapped up more than max_entry_gap_pct
    (default 2 %) above the previous close. With the default open proxy
    (prev_close) the gap is always 0 and behaves identically; supply self.opens
    (real opens aligned to self.prices) to activate meaningful gap filtering.
    """
    self = strat
    return _run_event_backtest(
        strat,
        initial_capital          = initial_capital,
        transaction_cost         = transaction_cost,
        risk_free_rate           = risk_free_rate,
        hard_stop_from_entry_pct = hard_stop_from_entry_pct,
        hard_stop_from_peak_pct  = hard_stop_from_peak_pct,
        atr_cap_percentile       = atr_cap_percentile,
        atr_cap_window           = atr_cap_window,
        stop_slippage_pct        = stop_slippage_pct,
        bear_sma_window          = bear_sma_window,
        bear_sma_min_periods     = bear_sma_min_periods,
        crash_guard_cooldown     = crash_guard_cooldown,
        use_limit_orders         = use_limit_orders,
        stop_approach_pct        = stop_approach_pct,
        trail_approach_pct       = trail_approach_pct,
        order_ttl_days           = order_ttl_days,
        order_fill_assumption    = order_fill_assumption,
        use_liquid_mf            = use_liquid_mf,
        liquid_mf_annual_rate    = liquid_mf_annual_rate,
        use_ltp_filter           = True,
        max_entry_gap_pct        = max_entry_gap_pct,
        label                    = "Live",
    )


# ════════════════════════════════════════════════════════════════════════════
# TRADE LOGS
# ════════════════════════════════════════════════════════════════════════════

def get_trade_log(strat):
    """
    Generate a comprehensive Trade Log from position changes.
    Returns:
        pd.DataFrame: Date, Ticker, Action, Weight_Change, Price
    """
    self = strat
    if self.positions is None:
        raise ValueError("Positions not generated.")

    print("Generating Trade Log...")

    weight_diff = self.positions.diff().fillna(0.0)

    # Filter for non-zero changes
    changes = weight_diff.unstack()
    trades = changes[changes.abs() > 1e-4]

    if trades.empty:
        return pd.DataFrame()

    # Format as DataFrame
    trade_log = trades.reset_index()
    trade_log.columns = ['Ticker', 'Date', 'Weight_Change']

    # Add Action Label
    trade_log['Action'] = trade_log['Weight_Change'].apply(lambda x: 'BUY' if x > 0 else 'SELL')

    # Add Price
    prices_stack = self.prices.reindex(self.positions.index, method='ffill').stack().reset_index()
    prices_stack.columns = ['Date', 'Ticker', 'Price']

    trade_log = pd.merge(trade_log, prices_stack, on=['Date', 'Ticker'], how='left')

    # Sort
    trade_log = trade_log.sort_values(by=['Date', 'Ticker'])

    return trade_log


def generate_detailed_trade_log(strat, initial_capital=None, equity_curve=None):
    """
    Generate a detailed per-trade log from the events recorded during backtest().

    Returns a DataFrame with columns:
        Trade_ID, Ticker, Entry_Date, Entry_Price, Exit_Date, Exit_Price,
        Holding_Days, Weight_At_Entry, Portfolio_Value_At_Entry,
        Quantity, PnL_Pct, PnL_Abs, Exit_Reason

    Args:
        initial_capital (float): Starting capital. Used as fallback when
            equity_curve is not provided or entry falls before curve start.
        equity_curve (pd.Series): The compounding equity curve produced by
            backtest() — when supplied, Quantity and PnL_Abs are computed using
            the ACTUAL portfolio value on the entry date so they correctly
            reflect compounded (growing) capital throughout the run.
    """
    self = strat
    if not hasattr(self, '_trade_events') or not self._trade_events:
        raise ValueError(
            "No trade events found. "
            "Run backtest_event_driven() (or live_backtest()) first."
        )

    if initial_capital is None:
        initial_capital = getattr(self, '_backtest_initial_capital', 100_000.0)

    # Build a fast date→portfolio-value lookup from the equity curve.
    _equity_lookup = None
    if equity_curve is not None and not equity_curve.empty:
        _equity_lookup = equity_curve.ffill()

    print("\n[Trade Log] Pairing entry/exit events...")

    # Separate entries and exits per ticker
    open_entries = {}   # ticker -> list of entry event dicts (FIFO)
    completed_trades = []

    for event in self._trade_events:
        ticker = event['ticker']
        if event['type'] == 'ENTRY':
            if ticker not in open_entries:
                open_entries[ticker] = []
            open_entries[ticker].append(event)

        elif event['type'] == 'EXIT':
            if ticker in open_entries and open_entries[ticker]:
                entry        = open_entries[ticker].pop(0)  # FIFO
                entry_date   = pd.Timestamp(entry['date'])   # coerce; survives JSON→str
                entry_price  = entry['price']
                entry_weight = entry['weight']
                exit_date    = pd.Timestamp(event['date'])   # coerce
                exit_price   = event['price']
                exit_reason  = event['reason']
                exit_stop_type = event.get('stop_type', '')   # '' for non-STOP_HIT exits

                holding_days = (exit_date - entry_date).days

                # ── Portfolio value on entry date ─────────────────────────
                if _equity_lookup is not None:
                    try:
                        port_val_at_entry = float(_equity_lookup.asof(entry_date))
                        if np.isnan(port_val_at_entry) or port_val_at_entry <= 0:
                            port_val_at_entry = initial_capital
                    except Exception:
                        port_val_at_entry = initial_capital
                else:
                    port_val_at_entry = initial_capital

                # Quantity: estimated shares = (portfolio_value * weight) / entry_price
                if entry_price and entry_price > 0:
                    quantity = (port_val_at_entry * entry_weight) / entry_price
                else:
                    quantity = float('nan')

                # P&L
                if entry_price and entry_price > 0 and exit_price and exit_price > 0:
                    pnl_pct = (exit_price / entry_price - 1) * 100
                    pnl_abs = quantity * (exit_price - entry_price) if not np.isnan(quantity) else float('nan')
                else:
                    pnl_pct = float('nan')
                    pnl_abs = float('nan')

                completed_trades.append({
                    'Ticker':                   ticker,
                    'Entry_Date':               entry_date,
                    'Entry_Price':              round(entry_price, 4) if entry_price else float('nan'),
                    'Exit_Date':                exit_date,
                    'Exit_Price':               round(exit_price, 4) if exit_price else float('nan'),
                    'Holding_Days':             holding_days,
                    'Weight_At_Entry':          round(entry_weight, 6),
                    'Portfolio_Value_At_Entry': round(port_val_at_entry, 2),
                    'Quantity':                 round(quantity, 2) if not np.isnan(quantity) else float('nan'),
                    'PnL_Pct':                  round(pnl_pct, 4) if not np.isnan(pnl_pct) else float('nan'),
                    'PnL_Abs':                  round(pnl_abs, 2) if not np.isnan(pnl_abs) else float('nan'),
                    'Exit_Reason':              exit_reason,
                    'Stop_Type':                exit_stop_type,
                })
            # else: exit with no matching entry (e.g. pre-warmup) — skip

    if not completed_trades:
        print("[Trade Log] No completed trades found.")
        return pd.DataFrame()

    df = pd.DataFrame(completed_trades)
    df.sort_values(['Entry_Date', 'Ticker'], inplace=True)
    df.reset_index(drop=True, inplace=True)
    df.index += 1
    df.index.name = 'Trade_ID'
    df.reset_index(inplace=True)

    # Summary
    wins   = (df['PnL_Pct'] > 0).sum()
    losses = (df['PnL_Pct'] < 0).sum()
    total  = len(df)
    if total > 0:
        print(f"[Trade Log] Total Trades: {total} | Wins: {wins} | Losses: {losses} "
              f"| Win Rate: {wins/total*100:.1f}%")
    else:
        print("[Trade Log] No trades.")
    print(f"[Trade Log] Exit Reasons: {df['Exit_Reason'].value_counts().to_dict()}")

    return df


# ════════════════════════════════════════════════════════════════════════════
# METRICS + REPORT
# ════════════════════════════════════════════════════════════════════════════

def _longest_underwater_days(drawdown_series):
    """
    Longest consecutive underwater (drawdown < 0) stretch, measured in CALENDAR days.
    Returns 0 if the curve is never underwater.
    """
    underwater = (drawdown_series < -1e-9).values
    idx = drawdown_series.index
    longest = 0
    run_start = None
    for i, uw in enumerate(underwater):
        if uw and run_start is None:
            run_start = idx[i]
        elif (not uw) and run_start is not None:
            longest = max(longest, (idx[i - 1] - run_start).days)
            run_start = None
    if run_start is not None:
        longest = max(longest, (idx[-1] - run_start).days)
    return longest


def compute_metrics(res, start_date, risk_free_rate=None):
    """
    Slice results to the report start, rebase equity to 100k, and recompute all
    metrics (CAGR/Sharpe/Sortino/Calmar/MaxDD/turnover/win-rate/etc.). Seeds
    placeholder trade-basis keys (overwritten by the caller from the detailed
    trade log). Writes backtest_logs.csv. Returns the augmented res dict.

    risk_free_rate : the ANNUAL risk-free rate used for the Sharpe ratio's excess
        return. Must match the rate the backtest was actually run with (BT_KWARGS
        / config), not an arbitrary constant — otherwise Sharpe is computed against
        a hurdle the strategy was never benchmarked to. If not passed explicitly,
        falls back to res['risk_free_rate'] (stored by the engine) and finally to 0.0.
    """
    if risk_free_rate is None:
        risk_free_rate = res.get('risk_free_rate', 0.0)
    eq = res['equity_curve']
    if start_date not in eq.index:
        # If start_date (Jan 1) is holiday, finding first valid index
        idx = eq.index.searchsorted(start_date)
        if idx < len(eq):
            start_date = eq.index[idx]

    # Slice
    res['equity_curve'] = eq.loc[start_date:]
    # Rebase Equity
    res['equity_curve'] = res['equity_curve'] / res['equity_curve'].iloc[0] * 100_000

    res['portfolio_value'] = res['equity_curve'] # Same magnitude
    res['net_returns'] = res['net_returns'].loc[start_date:]
    res['executed_weights'] = res['executed_weights'].loc[start_date:]
    # Slice Turnover (Series) if it exists and align
    if 'turnover' in res:
         res['turnover'] = res['turnover'].loc[start_date:]
    # Slice the actual daily transaction-cost-paid series (distinct from turnover activity)
    if 'txn_cost_daily' in res:
         res['txn_cost_daily'] = res['txn_cost_daily'].loc[start_date:]

    # Re-calc Metrics on sliced data
    eq = res['equity_curve']
    ret = res['net_returns']

    total_ret = eq.iloc[-1] / eq.iloc[0] - 1
    n_years = (eq.index[-1] - eq.index[0]).days / 365.25
    res['cagr'] = (eq.iloc[-1]/eq.iloc[0]) ** (1 / n_years) - 1 if n_years > 0 else 0

    # Annualized Volatility
    res['ann_volatility'] = ret.std() * np.sqrt(252)

    # Sharpe Ratio — uses the ACTUAL configured RFR (matches the backtest engine),
    # not a hardcoded constant.
    daily_rfr = (1 + risk_free_rate)**(1/252) - 1
    excess_ret = ret - daily_rfr
    res['sharpe'] = (np.sqrt(252) * excess_ret.mean() / ret.std()) if ret.std() != 0 else 0

    # Sortino Ratio — downside_dev is DAILY (no sqrt(252)); sqrt(252) in numerator annualises.
    downside_ret = ret.copy()
    downside_ret[downside_ret > 0] = 0.0
    downside_dev = np.sqrt((downside_ret**2).mean())   # daily only
    res['sortino'] = (np.sqrt(252) * ret.mean() / downside_dev) if downside_dev != 0 else 0

    # Max Drawdown
    running_max = eq.cummax()
    drawdown_series = (eq / running_max) - 1
    res['max_drawdown'] = drawdown_series.min()
    res['drawdown_series'] = drawdown_series

    # Drawdown depth & duration (NEW)
    _uw = drawdown_series[drawdown_series < 0]
    res['avg_drawdown']        = drawdown_series.mean()            # mean of full series (<= 0)
    res['avg_drawdown_uw']     = _uw.mean() if len(_uw) else 0.0   # mean while underwater
    res['pct_time_underwater'] = (drawdown_series < -1e-9).mean()
    res['longest_dd_days']     = _longest_underwater_days(drawdown_series)

    # Allocation / exposure stats — gross deployed = sum of position weights (NEW)
    _w = res['executed_weights']
    _exposure = _w.sum(axis=1)
    res['min_exposure']     = _exposure.min()
    res['avg_exposure']     = _exposure.mean()
    res['max_exposure']     = _exposure.max()
    res['avg_positions']    = (_w > 1e-6).sum(axis=1).mean()
    res['pct_time_in_cash'] = (_exposure < 1e-6).mean()

    # Calmar Ratio
    res['calmar'] = res['cagr'] / abs(res['max_drawdown']) if res['max_drawdown'] != 0 else 0

    # Win Rate (Monthly)
    monthly_res = res['portfolio_value'].resample('ME').last().pct_change()
    res['win_rate'] = (monthly_res.dropna() > 0).mean()

    # Annualized Turnover (Sliced) — trading ACTIVITY, sum of |Δweight|/year. This is
    # NOT the cost paid; it's how much the book churned.
    if 'turnover' in res:
        res['ann_turnover'] = res['turnover'].sum() / n_years if n_years > 0 else 0

    # Real transaction-cost drag (Sliced) — turnover × actual cost rate, i.e. what was
    # actually deducted from returns. Uses the SAME cost rate the backtest ran with
    # (stored by the engine), not an assumed/guessed number.
    _cost_rate = res.get('transaction_cost_rate', None)
    if 'txn_cost_daily' in res:
        res['ann_txn_cost_pct'] = res['txn_cost_daily'].sum() / n_years if n_years > 0 else 0
    elif 'turnover' in res and _cost_rate is not None:
        # Fallback if the daily series wasn't carried through: derive it from turnover.
        res['ann_txn_cost_pct'] = res['ann_turnover'] * _cost_rate

    res['total_return'] = total_ret

    # 1. Daily Win Rate
    res['daily_win_rate'] = (ret > 0).mean()

    # 2. Trade Basis Metrics — populated later from detailed_log after date filter
    # (Placeholder zeros; overwritten in main() after generate_detailed_trade_log)
    res['trade_win_rate'] = 0
    res['total_trades_count'] = 0
    res['avg_trade_return'] = 0
    res['avg_holding_days'] = 0
    res['best_trade'] = 0
    res['worst_trade'] = 0
    res['profit_factor'] = 0

    # --- Generate Custom Logs CSV (DISABLED — keep the folder clean; re-enable if needed) ---
    # log_df = pd.DataFrame(index=eq.index)
    # log_df['Portfolio Value'] = res['portfolio_value']
    # log_df['Net Return'] = ret
    # w = res['executed_weights']
    # log_df['Positions'] = (w > 1e-6).sum(axis=1)
    # log_df['Exposure'] = w.sum(axis=1)
    # log_df['Drawdown'] = drawdown_series
    # log_df['Monthly Return'] = monthly_res
    # log_df.to_csv('backtest_logs.csv')
    # print(f"\n[Logs] Saved detailed logs to 'backtest_logs.csv' ({len(log_df)} rows)")

    return res


def compute_benchmark_metrics(results, benchmark_price, rfr_annual=0.0):
    """
    Compute CAPM beta and annualized Jensen's alpha of the strategy vs a benchmark.

    Aligns the benchmark's daily returns to the (already-sliced) strategy return
    series and stores:
        results['beta']  : cov(rp, rb) / var(rb)            on daily returns
        results['alpha'] : annualized Jensen's alpha        (rf default 0%)

    Benchmark is the synthetic equal-weight universe index built in the runner
    (same series passed to the plots). rfr_annual defaults to 0 because the
    strategy's idle cash earns 0% (liquid-MF @ 0.0) and the benchmark is gross.
    """
    eq = results['equity_curve']
    rp = results['net_returns'].reindex(eq.index).fillna(0.0)            # strategy daily returns
    rb = benchmark_price.reindex(eq.index).pct_change().fillna(0.0)      # benchmark daily returns

    var_b = np.var(rb, ddof=1)   # ddof=1 to match np.cov's default
    beta = (np.cov(rp, rb)[0, 1] / var_b) if var_b > 0 else float('nan')

    d_rf = (1 + rfr_annual) ** (1 / 252) - 1
    alpha_daily = (rp - d_rf).mean() - beta * (rb - d_rf).mean()
    alpha_ann = (1 + alpha_daily) ** 252 - 1 if np.isfinite(alpha_daily) else float('nan')

    results['beta'] = beta
    results['alpha'] = alpha_ann
    return results


def print_report(results):
    """
    Print the PERFORMANCE REPORT block (CAGR, Sharpe, Sortino, Calmar, MaxDD,
    win rates, trade stats, profit factors, turnover, final value).
    """
    eq = results['equity_curve']
    y0, y1 = eq.index[0].year, eq.index[-1].year

    W = 52
    print("\n" + "=" * W)
    print(f" PERFORMANCE REPORT ({y0}-{y1})".center(W))
    print("=" * W)

    print("-- Returns --")
    print(f"  CAGR:              {results['cagr']*100:.2f}%")
    print(f"  Total Return:      {results['total_return']*100:.2f}%")
    print(f"  Final Portfolio:   {results['portfolio_value'].iloc[-1]:,.2f}")

    print("\n-- Risk & Drawdown --")
    print(f"  Sharpe Ratio:      {results['sharpe']:.2f}")
    print(f"  Sortino Ratio:     {results['sortino']:.2f}")
    print(f"  Calmar Ratio:      {results['calmar']:.2f}")
    print(f"  Ann Volatility:    {results['ann_volatility']*100:.2f}%")
    print(f"  Max Drawdown:      {results['max_drawdown']*100:.2f}%")
    print(f"  Avg Drawdown:      {results.get('avg_drawdown', 0)*100:.2f}%  (mean of full series)")
    print(f"  Avg DD (underwtr): {results.get('avg_drawdown_uw', 0)*100:.2f}%  (mean while below peak)")
    print(f"  Time Underwater:   {results.get('pct_time_underwater', 0)*100:.2f}%")
    print(f"  Longest DD:        {results.get('longest_dd_days', 0)} days")

    print("\n-- Benchmark (vs synthetic EW index) --")
    print(f"  Beta:              {results.get('beta', float('nan')):.2f}")
    print(f"  Alpha (ann.):      {results.get('alpha', float('nan'))*100:.2f}%")

    print("\n-- Allocation --")
    print(f"  Gross Exposure:    min {results.get('min_exposure', 0)*100:.1f}% | "
          f"avg {results.get('avg_exposure', 0)*100:.1f}% | "
          f"max {results.get('max_exposure', 0)*100:.1f}%")
    print(f"  Avg # Positions:   {results.get('avg_positions', 0):.1f}")
    print(f"  Time in Cash:      {results.get('pct_time_in_cash', 0)*100:.2f}%")

    print("\n-- Trade Stats --")
    print(f"  Daily Win Rate:    {results['daily_win_rate']*100:.2f}%")
    print(f"  Win Rate (M):      {results['win_rate']*100:.2f}%")
    print(f"  Win Rate (Trade):  {results['trade_win_rate']*100:.2f}% ({results['total_trades_count']} trades)")
    print(f"  Avg Trade Return:  {results['avg_trade_return']:.2f}%")
    print(f"  Avg Win  (Trade):  {results.get('avg_win_pct', 0):.2f}%")
    print(f"  Avg Loss (Trade):  -{results.get('avg_loss_pct', 0):.2f}%")
    print(f"  Payoff Ratio:      {results.get('payoff_ratio', 0):.2f}  (Avg Win % / Avg Loss %)")
    print(f"  Avg Holding Days:  {results['avg_holding_days']:.1f} days")
    print(f"  Best Trade:        {results['best_trade']:.2f}%")
    print(f"  Worst Trade:       {results['worst_trade']:.2f}%")
    print(f"  Profit Factor (%): {results['profit_factor']:.2f}  (equal-weighted % returns)")
    print(f"  Profit Factor ($): {results.get('profit_factor_dollar', 0):.2f}  (dollar-weighted, compounded)")

    if ('ann_turnover' in results) or ('ann_signal_turnover' in results) or ('ann_txn_cost_pct' in results):
        print("\n-- Turnover & Costs --")
        if 'ann_turnover' in results:
            print(f"  Total Turnover:    {results['ann_turnover']*100:.2f}% (Includes Vol Scaling)  "
                  f"[ACTIVITY — sum of |Δweight|, NOT a cost]")
        if 'ann_signal_turnover' in results:
            print(f"  Signal Turnover:   {results['ann_signal_turnover']*100:.2f}% (Stocks Only)")
        if 'ann_txn_cost_pct' in results:
            _rate = results.get('transaction_cost_rate', None)
            _rate_str = f" @ {_rate*100:.3f}% per one-way trade" if _rate is not None else ""
            print(f"  Txn Cost Drag:     {results['ann_txn_cost_pct']*100:.2f}% p.a. (ACTUAL cost paid = "
                  f"Turnover × cost rate{_rate_str}; already deducted daily in net returns above)")

    print("=" * W)


# ════════════════════════════════════════════════════════════════════════════
# TRADE / BREAK / YEARLY DIAGNOSTICS
# ════════════════════════════════════════════════════════════════════════════

def print_exit_breakdown(detailed_log):
    """
    Nested exit breakdown of the detailed trade log (the user's "exit breakdown by
    reason AND outcome"). STOP_HIT is split into three sub-categories:
        stop_loss      — the hard −15%-from-entry stop bound (classic stop-out)
        trailing_win   — the ATR chandelier / peak-anchored trailing stop, PnL > 0
        trailing_loss  — the trailing stop, PnL < 0
    (derived from the Stop_Type recorded by the engine + the trade PnL sign.)
    The other reasons — CRASH_GUARD, REBALANCE, SIGNAL_DROP, END_OF_PERIOD — keep
    their name. Every MIXED category is then shown with Win and Loss sub-rows.

    Columns: N, %Trd, Win%, AvgPnL%, SumPnL%, %ofPnL, AvgHold.
    Contribution (SumPnL%, %ofPnL) uses the EQUAL-WEIGHTED %-return basis (consistent
    with the report's Profit Factor (%)); %ofPnL is a share of the grand total
    (TOTAL = 100). Pure read of detailed_log; writes no file.
    """
    if detailed_log is None or detailed_log.empty:
        print("\n[Exit Breakdown] No trades to summarize.")
        return None

    df = detailed_log.copy()
    n_total   = len(df)
    total_pct = df['PnL_Pct'].sum()

    # ── Derive the fine-grained exit category ─────────────────────────────────
    def _cat(row):
        if row['Exit_Reason'] == 'STOP_HIT':
            if str(row.get('Stop_Type', '')) == 'STOP_LOSS':
                return 'stop_loss'
            return 'trailing_win' if row['PnL_Pct'] > 0 else 'trailing_loss'
        return row['Exit_Reason']
    df['_cat'] = df.apply(_cat, axis=1)

    order = ['stop_loss', 'trailing_win', 'trailing_loss',
             'CRASH_GUARD', 'REBALANCE', 'SIGNAL_DROP', 'END_OF_PERIOD']
    present = set(df['_cat'])
    cats = [c for c in order if c in present] + [c for c in present if c not in order]

    def _stats(g):
        n = len(g)
        s = g['PnL_Pct'].sum()
        return dict(
            N=n,
            pct_tr=n / n_total * 100 if n_total else 0.0,
            winpct=(g['PnL_Pct'] > 0).mean() * 100 if n else 0.0,
            avg=g['PnL_Pct'].mean() if n else 0.0,
            sumpct=s,
            ofpnl=(s / total_pct * 100) if total_pct else float('nan'),
            hold=g['Holding_Days'].mean() if n else 0.0,
        )

    # rows: list of (category_label, outcome_label, stats_dict)
    rows = []
    for cat in cats:
        g  = df[df['_cat'] == cat]
        gw = g[g['PnL_Pct'] > 0]
        gl = g[g['PnL_Pct'] < 0]
        rows.append((cat, 'all', _stats(g)))
        if len(gw) and len(gl):                    # mixed → show win/loss split
            rows.append(('', '├─ win',  _stats(gw)))
            rows.append(('', '└─ loss', _stats(gl)))
    rows.append(('TOTAL', 'all', _stats(df)))
    rows.append(('', '├─ win',  _stats(df[df['PnL_Pct'] > 0])))
    rows.append(('', '└─ loss', _stats(df[df['PnL_Pct'] < 0])))

    # ── Render an aligned text table ──────────────────────────────────────────
    headers = ['Exit Category', 'Outcome', 'N', '%Trd', 'Win%',
               'AvgPnL%', 'SumPnL%', '%ofPnL', 'AvgHold']

    def _cells(cat, outcome, s):
        return [
            cat, outcome,
            f"{s['N']:.0f}",
            f"{s['pct_tr']:.1f}",
            f"{s['winpct']:.0f}" if outcome == 'all' else '',
            f"{s['avg']:+.2f}",
            f"{s['sumpct']:+,.0f}",
            f"{s['ofpnl']:+.1f}",
            f"{s['hold']:.1f}",
        ]

    body = [_cells(*r) for r in rows]
    widths = [max(len(headers[c]), *(len(b[c]) for b in body)) for c in range(len(headers))]

    def _render(cells):
        return '  '.join(
            (cells[c].ljust(widths[c]) if c < 2 else cells[c].rjust(widths[c]))
            for c in range(len(cells))
        )

    line_w = sum(widths) + 2 * (len(headers) - 1)
    print("\n" + "=" * line_w)
    print(" EXIT BREAKDOWN  (reason → outcome)")
    print(" STOP_HIT split into stop_loss / trailing_win / trailing_loss; mixed reasons show win/loss rows.")
    print(" SumPnL%/%ofPnL = equal-weighted %-return contribution (TOTAL = 100).")
    print("=" * line_w)
    print(_render(headers))
    print("-" * line_w)
    for (cat, _outcome, _s), cells in zip(rows, body):
        if cat == 'TOTAL':
            print("-" * line_w)
        print(_render(cells))
    print("=" * line_w)
    return rows


def calculate_trade_stats(weights, prices):
    """
    Calculate per-trade statistics based on holding periods.
    Trade = Contiguous period of non-zero weight.
    Returns DataFrame with ['Return', 'Days']
    """
    trades_data = [] # List of dicts
    # Ensure aligned
    common_idx = weights.index.intersection(prices.index)
    weights = weights.loc[common_idx]
    prices = prices.loc[common_idx]

    daily_rets = prices.pct_change(fill_method=None).fillna(0)

    for col in weights.columns:
        if col not in prices.columns: continue

        w_col = weights[col]
        # Boolean series
        is_held = (w_col > 1e-6)

        if not is_held.any(): continue

        # Identify state changes: 1 = Start of trade, -1 = End of trade
        diff = is_held.astype(int).diff().fillna(0)

        # If starts with held, manually handle the first day.
        if is_held.iloc[0]:
            diff.iloc[0] = 1

        starts = diff[diff == 1].index
        ends = diff[diff == -1].index

        # If currently held at the end, close the trade for stats
        if is_held.iloc[-1]:
             ends = ends.insert(len(ends), weights.index[-1])

        # Robust zip
        for s, e in zip(starts, ends):
            if e < s: continue # Should not happen

            # Holding period: [s, e] (inclusive of return days)
            period_rets = daily_rets.loc[s:e, col]

            # Compounded Return
            trade_ret = (1 + period_rets).prod() - 1

            # Duration
            days = (e - s).days
            if days == 0: days = 1 # Intraday or 1 day

            trades_data.append({'Return': trade_ret, 'Days': days})

    return pd.DataFrame(trades_data) if trades_data else pd.DataFrame(columns=['Return', 'Days'])


def detect_strategy_breaks(executed_weights, equity_curve, min_break_days=14,
                           use_liquid_mf=False, liquid_mf_annual_rate=0.0):
    """
    Detect periods where the strategy holds zero positions (taking a break).

    A break is a contiguous stretch of trading days with 0 active positions.
    Breaks <= min_break_days (default 14, ~2 weeks) are ignored.

    Returns a DataFrame with columns:
        Break_Start, Break_End, Duration_Days, Trading_Days,
        Capital_Start, Capital_End, Break_Return_Pct, Parking_Mode
    Also prints a summary table.
    """
    pos_count = (executed_weights > 1e-6).sum(axis=1)
    is_idle = (pos_count == 0)

    if not is_idle.any():
        print("\n[Breaks] Strategy was always invested — no idle breaks detected.")
        return pd.DataFrame()

    # Identify contiguous idle stretches using diff on the boolean
    state_change = is_idle.astype(int).diff().fillna(0)
    if is_idle.iloc[0]:
        state_change.iloc[0] = 1  # starts idle

    starts = state_change[state_change == 1].index   # idle begins
    ends   = state_change[state_change == -1].index   # idle ends (first active day)

    # If still idle at the very end, close the last break at the last date
    if is_idle.iloc[-1]:
        ends = ends.insert(len(ends), executed_weights.index[-1])

    breaks = []
    for s, e in zip(starts, ends):
        if is_idle.iloc[-1] and e == executed_weights.index[-1]:
            last_idle = e
        else:
            idx_pos = executed_weights.index.get_loc(e)
            if idx_pos > 0:
                last_idle = executed_weights.index[idx_pos - 1]
            else:
                last_idle = s

        trading_days = is_idle.loc[s:last_idle].sum()
        calendar_days = (last_idle - s).days
        if calendar_days == 0:
            calendar_days = 1

        # Capital at break start and end
        cap_start = float(equity_curve.loc[s]) if s in equity_curve.index else np.nan
        cap_end   = float(equity_curve.loc[last_idle]) if last_idle in equity_curve.index else np.nan
        break_ret = ((cap_end / cap_start) - 1) * 100 if cap_start > 0 else 0.0

        breaks.append({
            'Break_Start': s,
            'Break_End': last_idle,
            'Duration_Days': calendar_days,
            'Trading_Days': int(trading_days),
            'Capital_Start': round(cap_start, 2),
            'Capital_End': round(cap_end, 2),
            'Break_Return_Pct': round(break_ret, 2),
        })

    breaks_df = pd.DataFrame(breaks)

    if breaks_df.empty:
        print("\n[Breaks] No idle breaks detected.")
        return breaks_df

    # Filter: only show breaks longer than min_break_days calendar days
    significant = breaks_df[breaks_df['Duration_Days'] > min_break_days].copy()

    if significant.empty:
        print(f"\n[Breaks] All {len(breaks_df)} idle stretches were <= {min_break_days} calendar days. None significant.")
        return significant

    significant = significant.reset_index(drop=True)
    parking_label = f"Liquid MF @ {liquid_mf_annual_rate*100:.1f}%" if use_liquid_mf else "Cash (RFR)"

    print(f"\n{'='*100}")
    print(f" STRATEGY BREAK REPORT  (idle > {min_break_days} calendar days)  |  Parking: {parking_label}")
    print(f"{'='*100}")
    print(f"{'#':<4} {'Start':<13} {'End':<13} {'Cal Days':<10} {'Trd Days':<10} "
          f"{'Capital In':>12} {'Capital Out':>12} {'Return':>8}")
    print(f"{'-'*100}")

    total_cal = 0
    total_trd = 0
    for i, row in significant.iterrows():
        print(f"{i+1:<4} {str(row['Break_Start'].date()):<13} {str(row['Break_End'].date()):<13} "
              f"{row['Duration_Days']:<10} {row['Trading_Days']:<10} "
              f"{row['Capital_Start']:>12,.2f} {row['Capital_End']:>12,.2f} "
              f"{row['Break_Return_Pct']:>7.2f}%")
        total_cal += row['Duration_Days']
        total_trd += row['Trading_Days']

    print(f"{'-'*100}")
    print(f"{'Tot':<4} {'':<13} {'':<13} {total_cal:<10} {total_trd:<10}")
    print(f"{'='*100}")
    print(f"  {len(significant)} significant break(s) out of {len(breaks_df)} total idle stretches.")
    print(f"  Parking mode: {parking_label}")

    # Save to CSV (DISABLED — keep the folder clean; re-enable if needed)
    significant['Parking_Mode'] = parking_label
    # significant.to_csv('strategy_breaks.csv', index=False)
    # print(f"  Saved to 'strategy_breaks.csv'")

    return significant


def plot_performance(results, benchmark_series=None):
    """
    Enhanced Plotting Dashboard:
    File 1: strategy_performance.png (Dashboard)
    File 2: strategy_heatmap.png (Monthly Returns)

    Note: alternate dashboard plotter, kept as an orphan helper.
    """
    equity = results['equity_curve']
    dd = (equity / equity.cummax()) - 1
    returns = results['net_returns']
    executed_weights = results.get('executed_weights', None)

    fig = plt.figure(figsize=(16, 20))
    gs = fig.add_gridspec(4, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='CSM Strategy', color='#1f77b4', linewidth=1.5)
    ax1.set_yscale('log')
    if benchmark_series is not None:
        bench_rebased = benchmark_series / benchmark_series.iloc[0]
        ax1.plot(bench_rebased.index, bench_rebased, label='Benchmark', color='gray', linestyle='--', alpha=0.7)
    ax1.set_title('1. Cumulative Growth (Log Scale)', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, which="both", linestyle='--', alpha=0.3)
    ax1.set_ylabel('Portfolio Value ($)')

    # Panel 2: Relative Strength
    ax2 = fig.add_subplot(gs[1, 0])
    if benchmark_series is not None:
        bench_aligned = benchmark_series.reindex(equity.index).ffill()
        rs = (equity/equity.iloc[0]) / (bench_aligned/bench_aligned.iloc[0])
        ax2.plot(rs.index, rs, color='purple', linewidth=1.2)
        ax2.set_title('2. Relative Strength (vs Benchmark)', fontsize=12, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.set_ylabel('Ratio')
    else:
        ax2.text(0.5, 0.5, "No Benchmark", ha='center')

    # Panel 3: Active Positions (Invested)
    ax3 = fig.add_subplot(gs[1, 1])
    if executed_weights is not None:
        pos_count = (executed_weights > 1e-6).sum(axis=1)
    else:
        pos_count = pd.Series(0, index=equity.index)

    ax3.fill_between(pos_count.index, pos_count, step='post', color='#9467bd', alpha=0.5)
    ax3.plot(pos_count.index, pos_count, color='#9467bd', linewidth=0.8, drawstyle='steps-post')
    ax3.set_title('3. Active Positions (Invested Count)', fontsize=12, fontweight='bold')
    ax3.set_ylim(0, 60)
    ax3.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax3.set_ylabel('Count')

    # Panel 4: Drawdown
    ax4 = fig.add_subplot(gs[2, :])
    ax4.fill_between(dd.index, dd, 0, color='#d62728', alpha=0.3)
    ax4.plot(dd.index, dd, color='#d62728', linewidth=1)
    ax4.set_title('4. Drawdown Profile (%)', fontsize=12, fontweight='bold')
    ax4.grid(True, linestyle='--', alpha=0.3)
    ax4.set_ylabel('Drawdown')

    # Panel 5: Return Distribution
    ax5 = fig.add_subplot(gs[3, :])
    monthly_ret = equity.resample('ME').last().pct_change().dropna()
    ax5.hist(monthly_ret*100, bins=50, color='teal', edgecolor='black', alpha=0.7)
    ax5.axvline(0, color='black', linestyle='--', linewidth=1)
    mean_ret = monthly_ret.mean() * 100
    ax5.axvline(mean_ret, color='blue', linestyle=':', label=f'Mean: {mean_ret:.2f}%')
    ax5.set_title('5. Monthly Return Distribution', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Monthly Return (%)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('strategy_performance.png', dpi=150)
    print("\n[Graphics] Saved Main Dashboard to 'strategy_performance.png'")

    # --- 2. Heatmap (Separate File) ---
    try:
        monthly_ret_df = pd.DataFrame({'Return': monthly_ret})
        monthly_ret_df['Year'] = monthly_ret_df.index.year
        monthly_ret_df['Month'] = monthly_ret_df.index.month
        heatmap_data = monthly_ret_df.pivot(index='Year', columns='Month', values='Return')

        plt.figure(figsize=(10, 12)) # Tall aspect ratio for years
        import seaborn as sns
        sns.heatmap(heatmap_data*100, annot=True, fmt=".1f", cmap="RdYlGn", center=0, cbar=False)
        plt.title('Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig('strategy_heatmap.png', dpi=150)
        print("[Graphics] Saved Heatmap to 'strategy_heatmap.png'")
    except Exception as e:
        print(f"Heatmap generation failed: {e}")


def print_yearly_returns(portfolio_value):
    """
    Print Yearly Returns Table with per-year intra-year Max Drawdown.
    Max DD resets the peak each calendar year (worst peak-to-trough WITHIN the year),
    so it answers "what was the deepest dip that year" rather than vs the all-time high.
    """
    yearly_res = portfolio_value.resample('YE').last()
    yearly_ret = yearly_res.pct_change()

    # Intra-year max drawdown (peak resets each Jan)
    yearly_dd = {}
    for year, eq_y in portfolio_value.groupby(portfolio_value.index.year):
        yearly_dd[year] = (eq_y / eq_y.cummax() - 1).min()

    print("\n" + "="*34)
    print(" Yearly Returns")
    print("="*34)
    print(f"{'Year':<6} | {'Return':>8} | {'Max DD':>8}")
    print("-" * 34)

    for date, ret in yearly_ret.items():
        if pd.notna(ret):
            dd = yearly_dd.get(date.year, float('nan'))
            print(f"{date.year:<6} | {ret*100:7.2f}% | {dd*100:7.2f}%")
    print("="*34)


# ════════════════════════════════════════════════════════════════════════════
# INFORMATION COEFFICIENT (IC) ANALYTICS
# ════════════════════════════════════════════════════════════════════════════

def calculate_ic(strat, forward_periods: int = 1, method: str = 'spearman',
                 report_start: str = None) -> dict:
    """
    Compute per-period Information Coefficient (IC) and ICIR.

    IC_t = cross-sectional rank correlation between the combined factor scores
    at time t and the actual forward returns from t to t+k. A positive IC means
    the factor correctly ranks stocks.

    Returns
    -------
    dict with keys: ic_series, ic_mean, ic_std, icir, ic_positive_pct, t_stat,
                    factor_decay (IC at 1m, 3m, 6m, 12m forward horizons).
    """
    self = strat
    _scipy_stats = _STATS

    if self.factors is None:
        raise ValueError("Call calculate_factors() first.")

    monthly_prices = self.prices.resample('ME').last()
    fwd_ret = monthly_prices.pct_change(forward_periods, fill_method=None).shift(-forward_periods)

    corr_fn = lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation \
              if method == 'spearman' \
              else _scipy_stats.pearsonr(x, y)[0]

    ic_records = []
    for date in self.factors.index:
        if date not in fwd_ret.index:
            continue
        f = self.factors.loc[date].dropna()
        r = fwd_ret.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) < 5:
            continue
        ic_val = corr_fn(f[common].values, r[common].values)
        ic_records.append({'Date': date, 'IC': ic_val, 'N_stocks': len(common)})

    ic_df = pd.DataFrame(ic_records).set_index('Date')
    ic_series = ic_df['IC'].dropna()

    if report_start:
        ic_series_rep = ic_series.loc[report_start:]
    else:
        ic_series_rep = ic_series

    ic_mean  = ic_series_rep.mean()
    ic_std   = ic_series_rep.std()
    icir     = ic_mean / ic_std if ic_std > 0 else 0.0
    pos_pct  = (ic_series_rep > 0).mean()
    n        = len(ic_series_rep)
    t_stat   = ic_mean / (ic_std / np.sqrt(n)) if (n > 0 and ic_std > 0) else 0.0

    # Factor decay: IC at multiple forward horizons
    decay = {}
    for h in [1, 3, 6, 12]:
        fwd_h = monthly_prices.pct_change(h, fill_method=None).shift(-h)
        ic_h_list = []
        for date in self.factors.index:
            if date not in fwd_h.index:
                continue
            f = self.factors.loc[date].dropna()
            r = fwd_h.loc[date].dropna()
            common = f.index.intersection(r.index)
            if len(common) < 5:
                continue
            ic_h_list.append(corr_fn(f[common].values, r[common].values))
        ic_h = np.array(ic_h_list)
        decay[h] = {
            'ic_mean': float(np.nanmean(ic_h)),
            'icir':    float(np.nanmean(ic_h) / np.nanstd(ic_h)) if np.nanstd(ic_h) > 0 else 0.0,
        }

    # ── Print report ────────────────────────────────────────────────────
    total_factor_months = len(self.factors.index)
    print("\n" + "=" * 68)
    print(f" FILTERED-UNIVERSE IC / ICIR  —  v2_2  "
          f"({method.upper()}, {forward_periods}m forward)")
    print("=" * 68)
    print(f"  Context: IC computed only on months where >= 5 stocks pass")
    print(f"  the SMA-200/liquidity/circuit/price universe filter. Bear-")
    print(f"  market months (2008 crash, 2011-12 bear) are excluded because")
    print(f"  most stocks fall below SMA-200 → universe collapses → skipped.")
    print(f"  See Realized IC for trade-log-based edge measurement.")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  Total factor months  : {total_factor_months}  "
          f"(all months with any eligible stock)")
    print(f"  IC-computable months : {n}  "
          f"(>= 5 stocks cross-sectional overlap with fwd return)")
    print(f"  Excluded months      : {total_factor_months - n}  "
          f"(too few eligible stocks — mostly bear market)")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  IC Mean (factor)     : {ic_mean:+.4f}")
    print(f"  IC Std               : {ic_std:.4f}")
    print(f"  ICIR                 : {icir:+.3f}   (> 0.3 useful for ranking)")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic          : {t_stat:+.2f}   (> 2.0 = statistically significant)")
    if abs(t_stat) >= 2.0:
        print(f"  ✓ t-stat >= 2.0: factor predictive power is statistically significant")
    print(f"\n  Factor Decay (hump at 6m = textbook momentum ✓):")
    print(f"  {'Horizon':>8}  {'IC Mean':>10}  {'ICIR':>8}")
    for h, d in decay.items():
        tag = " ← peak (sweet spot)"  if d['ic_mean'] == max(dd['ic_mean'] for dd in decay.values()) else ""
        print(f"  {h:>6}m  {d['ic_mean']:>+10.4f}  {d['icir']:>8.3f}{tag}")
    print("=" * 68)

    return {
        'ic_series'       : ic_series,
        'ic_mean'         : ic_mean,
        'ic_std'          : ic_std,
        'icir'            : icir,
        'ic_positive_pct' : pos_pct,
        't_stat'          : t_stat,
        'factor_decay'    : decay,
    }


def plot_ic(strat, ic_results: dict, filename: str = 'factor_ic.png'):
    """
    Plot IC time-series, rolling IC, cumulative IC, and factor decay.

    Parameters
    ----------
    ic_results : dict   — output of calculate_ic()
    filename   : str    — PNG filename to save
    """
    self = strat
    ic_s = ic_results['ic_series']
    ic_roll = ic_s.rolling(12).mean()

    fig, axes = plt.subplots(3, 1, figsize=(13, 14))

    # 1. Bar chart of monthly IC
    ax = axes[0]
    colors = ['#2ca02c' if v > 0 else '#d62728' for v in ic_s]
    ax.bar(ic_s.index, ic_s, color=colors, width=20, alpha=0.7)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axhline(ic_results['ic_mean'], color='blue', linestyle='--',
               label=f"Mean IC = {ic_results['ic_mean']:+.4f}")
    ax.plot(ic_roll.index, ic_roll, color='navy', linewidth=1.5,
            label='12m Rolling IC')
    ax.set_title(f"Monthly IC (Spearman rank correlation | ICIR = {ic_results['icir']:.3f})",
                 fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('IC')

    # 2. Cumulative IC (shows consistent positive edge)
    ax2 = axes[1]
    cumIC = ic_s.cumsum()
    ax2.plot(cumIC.index, cumIC, color='#1f77b4', linewidth=1.5)
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_title('Cumulative IC (positive slope = persistent predictive edge)',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Cumulative IC')

    # 3. Factor decay bar chart
    ax3 = axes[2]
    horizons = list(ic_results['factor_decay'].keys())
    ic_means = [ic_results['factor_decay'][h]['ic_mean'] for h in horizons]
    icirs    = [ic_results['factor_decay'][h]['icir']    for h in horizons]
    x = np.arange(len(horizons))
    w = 0.35
    ax3.bar(x - w/2, ic_means, w, label='IC Mean', color='steelblue', alpha=0.8)
    ax3.bar(x + w/2, icirs,    w, label='ICIR',    color='darkorange', alpha=0.8)
    ax3.axhline(0, color='black', linewidth=0.8)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'{h}m' for h in horizons])
    ax3.set_title('Factor Decay: IC Mean and ICIR at Multiple Forward Horizons',
                  fontsize=12, fontweight='bold')
    ax3.legend(fontsize=9)
    ax3.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"[IC] Saved IC analysis to '{filename}'")


def calculate_realized_ic(strat, trade_log_df: 'pd.DataFrame',
                          method: str = 'spearman',
                          report_start: str = None) -> dict:
    """
    Realized IC — the correct IC for this gated threshold strategy.

    For each entry month, compute the Spearman rank correlation between the
    dual-window Sharpe factor score at the month-end BEFORE entry (the score
    that caused the shortlist) and the actual realized PnL % from the detailed
    trade log. Directly measures: among the stocks we actually entered, did
    higher Sharpe score → better trade outcome?

    Parameters
    ----------
    trade_log_df : pd.DataFrame
        Output of generate_detailed_trade_log() — needs columns:
        Ticker, Entry_Date, PnL_Pct.
    method : str        'spearman' (default) or 'pearson'.
    report_start : str  ISO date string — only trades from this date onward.

    Returns
    -------
    dict: realized_ic_series, ic_mean, ic_std, icir, ic_positive_pct, t_stat,
          n_months, n_trades, min_trades_per_month
    """
    self = strat
    _scipy_stats = _STATS

    if self.factors is None:
        raise ValueError("Call calculate_factors() first.")
    if trade_log_df is None or trade_log_df.empty:
        print("[Realized IC] No trade log provided or log is empty.")
        return {}

    corr_fn = (
        lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation
        if method == 'spearman'
        else _scipy_stats.pearsonr(x, y)[0]
    )

    # ── Prepare trades ───────────────────────────────────────────────────
    needed_cols = {'Ticker', 'Entry_Date', 'PnL_Pct'}
    if not needed_cols.issubset(trade_log_df.columns):
        print(f"[Realized IC] Missing columns: {needed_cols - set(trade_log_df.columns)}")
        return {}

    trades = trade_log_df[['Ticker', 'Entry_Date', 'PnL_Pct']].copy()
    trades['Entry_Date'] = pd.to_datetime(trades['Entry_Date'])

    if report_start:
        trades = trades[trades['Entry_Date'] >= pd.Timestamp(report_start)]

    # Map each entry date to the last month-end on or before entry date
    factor_index = self.factors.index  # monthly (ME) timestamps
    def _last_month_end(d):
        valid = factor_index[factor_index <= d]
        return valid[-1] if len(valid) > 0 else pd.NaT

    trades['Entry_Month'] = trades['Entry_Date'].apply(_last_month_end)
    trades = trades.dropna(subset=['Entry_Month'])

    # ── Per-month realized IC ─────────────────────────────────────────────
    ic_records = []
    min_trades = 3

    for month, grp in trades.groupby('Entry_Month'):
        if len(grp) < min_trades:
            continue
        if month not in factor_index:
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
        ic_val = corr_fn(np.array(scores), np.array(returns))
        ic_records.append({
            'Date'    : month,
            'IC'      : ic_val,
            'N_trades': len(scores),
        })

    if not ic_records:
        print("[Realized IC] Not enough monthly groups to compute IC "
              "(need >= 3 trades with factor scores per month).")
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
    print(f" REALIZED IC / ICIR  —  v2_2  ({method.upper()})")
    print("=" * 68)
    print(f"  Context: IC computed on ENTERED stocks only (passed Sharpe")
    print(f"  threshold). Dual-window Sharpe score at entry month vs actual")
    print(f"  realized trade PnL%. This is the true factor ranking edge.")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  Months with >= {min_trades} entries : {n}")
    print(f"  Total trades used    : {n_trades}")
    print(f"  Avg trades / month   : {n_trades/n:.1f}")
    print(f"  IC Mean (Realized)   : {ric_mean:+.4f}   (> 0.05 meaningful)")
    print(f"  IC Std               : {ric_std:.4f}")
    print(f"  ICIR (Realized)      : {ricir:+.3f}   (> 0.3 usable)")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic          : {t_stat:+.2f}   (> 2.0 = significant)")
    if ric_mean > 0:
        print(f"\n  ✓ Positive realized IC: factor correctly ranks better trades")
        print(f"    among threshold-passed entries (higher Sharpe → better PnL).")
    else:
        print(f"\n  ✗ Negative realized IC: factor ranking does NOT improve")
        print(f"    trade outcomes among threshold-passed entries.")
    print(f"\n  Note: avg holding = 9.2 days. Monthly IC measures next-month")
    print(f"  return (~20 days) — realized IC uses actual exit PnL, matching")
    print(f"  the true holding period regardless of length.")
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
        'min_trades_per_month': min_trades,
    }


# ════════════════════════════════════════════════════════════════════════════
# PERFORMANCE PLOTS
# ════════════════════════════════════════════════════════════════════════════

def plot_summary(strat, benchmark_series=None, filename='strategy_summary.png',
                 heatmap_filename='strategy_heatmap.png'):
    """
    Generate Performance Dashboard (6 panels) and Monthly-Returns Heatmap.
    """
    self = strat
    if self.results is None:
        print("No results to plot. Run backtest() first.")
        return

    print(f"Generating Summary Plots to {filename}...")

    equity = self.results['equity_curve']
    dd = (equity / equity.cummax()) - 1
    executed_weights = self.results.get('executed_weights', None)

    # --- 1. Main Dashboard (6 Panels) ---
    fig = plt.figure(figsize=(16, 25))
    gs = fig.add_gridspec(5, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='Strategy', color='#1f77b4', linewidth=1.5)
    ax1.set_yscale('log')
    if benchmark_series is not None:
        # Rebase bench to strategy start
        start_dt = equity.index[0]
        if start_dt in benchmark_series.index:
            bench_slice = benchmark_series.loc[start_dt:]
            bench_rebased = bench_slice / bench_slice.iloc[0] * equity.iloc[0]
            ax1.plot(bench_rebased.index, bench_rebased, label='Benchmark', color='gray', linestyle='--', alpha=0.7)
    ax1.set_title('1. Cumulative Growth (Log Scale)', fontsize=14, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, which="both", linestyle='--', alpha=0.3)
    ax1.set_ylabel('Portfolio Value ($)')

    # Panel 2: Relative Strength
    ax2 = fig.add_subplot(gs[1, 0])
    if benchmark_series is not None:
        bench_aligned = benchmark_series.reindex(equity.index).ffill()
        if not bench_aligned.empty:
            strat_norm = equity / equity.iloc[0]
            bench_norm = bench_aligned / bench_aligned.iloc[0]
            rs = strat_norm / bench_norm
            ax2.plot(rs.index, rs, color='purple', linewidth=1.2)
            ax2.set_title('2. Relative Strength (vs Benchmark)', fontsize=12, fontweight='bold')
            ax2.grid(True, linestyle='--', alpha=0.3)
            ax2.set_ylabel('Ratio')
    else:
        ax2.text(0.5, 0.5, "No Benchmark Provided", ha='center')

    # Panel 3: Active Positions
    ax3 = fig.add_subplot(gs[1, 1])
    if executed_weights is not None:
        pos_count = (executed_weights > 1e-6).sum(axis=1)
        ax3.fill_between(pos_count.index, pos_count, step='post', color='#9467bd', alpha=0.5)
        ax3.plot(pos_count.index, pos_count, color='#9467bd', linewidth=0.8, drawstyle='steps-post')
        ax3.set_title(f'3. Active Positions (Max cap: {self.capacity_limit})', fontsize=12, fontweight='bold')
        ax3.grid(True, axis='y', linestyle='--', alpha=0.3)
        ax3.set_ylabel('Count')

    # Panel 4: Drawdown
    ax4 = fig.add_subplot(gs[2, :])
    ax4.fill_between(dd.index, dd, 0, color='#d62728', alpha=0.3)
    ax4.plot(dd.index, dd, color='#d62728', linewidth=1)
    ax4.set_title('4. Drawdown Profile (%)', fontsize=12, fontweight='bold')
    ax4.grid(True, linestyle='--', alpha=0.3)
    ax4.set_ylabel('Drawdown')

    # Panel 5: Running CAGR
    ax5 = fig.add_subplot(gs[3, :])
    days_running = (equity.index - equity.index[0]).days
    years_running = days_running / 365.25
    with np.errstate(divide='ignore', invalid='ignore'):
        running_cagr = (equity / equity.iloc[0]) ** (1 / years_running) - 1
    running_cagr.replace([np.inf, -np.inf], np.nan, inplace=True)
    # Smooth start noise
    mask_date = equity.index[0] + pd.Timedelta(days=180)
    running_cagr_plot = running_cagr.loc[mask_date:]
    ax5.plot(running_cagr_plot.index, running_cagr_plot * 100, color='darkgreen', linewidth=1.5)
    # Annotation
    if not running_cagr.dropna().empty:
        final_cagr = running_cagr.dropna().iloc[-1]
        ax5.axhline(final_cagr * 100, color='green', linestyle=':', label=f'Final: {final_cagr*100:.2f}%')
    ax5.set_title('5. Running CAGR Evolution (%)', fontsize=12, fontweight='bold')
    ax5.grid(True, linestyle='--', alpha=0.3)
    ax5.legend()
    ax5.set_ylabel('CAGR (%)')

    # Panel 6: Return Distribution
    ax6 = fig.add_subplot(gs[4, :])
    monthly_ret = equity.resample('ME').last().pct_change().dropna()
    if not monthly_ret.empty:
        ax6.hist(monthly_ret*100, bins=50, color='teal', edgecolor='black', alpha=0.7)
        ax6.axvline(0, color='black', linestyle='--', linewidth=1)
        mean_ret = monthly_ret.mean() * 100
        ax6.axvline(mean_ret, color='blue', linestyle=':', label=f'Mean: {mean_ret:.2f}%')
        ax6.set_title('6. Monthly Return Distribution', fontsize=12, fontweight='bold')
        ax6.set_xlabel('Monthly Return (%)')
        ax6.legend()
        ax6.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)

    # --- 2. Heatmap ---
    try:
        if not monthly_ret.empty:
            monthly_ret_df = pd.DataFrame({'Return': monthly_ret})
            monthly_ret_df['Year'] = monthly_ret_df.index.year
            monthly_ret_df['Month'] = monthly_ret_df.index.month
            heatmap_data = monthly_ret_df.pivot(index='Year', columns='Month', values='Return')

            plt.figure(figsize=(10, 12))
            sns.heatmap(heatmap_data*100, annot=True, fmt=".1f", cmap="RdYlGn", center=0, cbar=False)
            plt.title('Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
            plt.tight_layout()
            plt.savefig(heatmap_filename, dpi=150)
            plt.close()
            print(f"[Graphics] Saved Heatmap to '{heatmap_filename}'")
    except Exception as e:
        print(f"Heatmap generation failed: {e}")


def plot_diagnostics(strat, filename='strategy_diagnostics.png'):
    """
    Generate Diagnostic Plots: Signal Strength, Volatility, Turnover.
    """
    self = strat
    if self.results is None or self.factors is None:
        return

    print(f"Generating Diagnostics to {filename}...")

    fig, axes = plt.subplots(3, 1, figsize=(12, 18))

    # 1. Average Signal Strength
    avg_sharpe = []
    dates = []

    for date, pos_row in self.positions.iterrows():
        held = pos_row[pos_row > 1e-6]
        if len(held) > 0 and date in self.factors.index:
            factor_scores = self.factors.loc[date, held.index]
            avg_sharpe.append(factor_scores.mean())
            dates.append(date)

    if avg_sharpe:
        axes[0].plot(dates, avg_sharpe, color='darkblue', linewidth=1.5)
        axes[0].set_title('Average Signal Strength (Sharpe of Held Stocks)', fontsize=12, fontweight='bold')
        axes[0].grid(True, alpha=0.3)
        axes[0].set_ylabel('Avg Sharpe')

    # 2. Portfolio Volatility
    if 'net_returns' in self.results:
        vol_21d = self.results['net_returns'].rolling(21).std() * np.sqrt(252)
        axes[1].plot(vol_21d.index, vol_21d * 100, color='orange', linewidth=1.2)
        axes[1].set_title('Rolling 21-Day Volatility (Annualized)', fontsize=12, fontweight='bold')
        axes[1].grid(True, alpha=0.3)
        axes[1].set_ylabel('Volatility (%)')

    # 3. Turnover
    if 'turnover' in self.results:
        turnover = self.results['turnover']
        # Plot cumulative
        cum_turnover = turnover.cumsum()
        axes[2].plot(cum_turnover.index, cum_turnover, color='red', linewidth=1.2)
        axes[2].set_title('Cumulative Turnover', fontsize=12, fontweight='bold')
        axes[2].grid(True, alpha=0.3)
        axes[2].set_ylabel('Turnover')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close()
    print(f"[Graphics] Saved Diagnostics to '{filename}'")
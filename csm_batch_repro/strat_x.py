"""
csm_batch_strategy.py
=====================
Cross-Sectional Momentum — Batch Strategy  (strategy CORE only).

CLEAN production version: contains only the logic that is currently in use. The
previous kitchen-sink version (with every experimental overlay) is preserved as
csm_batch_strategy_raw.py. Disabled overlays removed here: NAV kill switch, 200-SMA
trend exit, signal-reversal exit, vol-spike trim, calm-regime leverage, breakeven
profit-lock, weight-buffer, ERC / rank weighting, and the live get_exit_signals
evaluator. The ATR trailing stop is KEPT behind its use_trailing_stop switch.

Signal   : dual-lookback Sharpe (12m + 6m), absolute-momentum gate, hysteresis buffer
Universe : top-N liquidity, price floor, circuit-breaker, SMA-200, falling-knife
Exits    : entry hard stop (+ optional ATR chandelier/peak trail), dynamic rank-decay,
           crash guard; rebalance diffs. Sizing: inverse-vol, vol-target, corr-guard.
"""

import pandas as pd
import numpy as np
import os
import glob


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADER
# ══════════════════════════════════════════════════════════════════════════════

def load_data(folder_path):
    """Load all CSV files from folder_path.
    Returns: prices_df, volumes_df, highs_df, lows_df, opens_df (all DataFrames).
    Entries/exits fill at next-day open; falls back to prev-close if open missing.
    """
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))
    if not all_files:
        raise ValueError(f"No CSV files found in {folder_path}")

    price_list, volume_list, high_list, low_list, open_list = [], [], [], [], []
    print(f"Loading {len(all_files)} files from {folder_path}...")

    for filename in all_files:
        try:
            symbol = os.path.basename(filename).replace('.csv', '')
            df = pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')

            def _clean(s):
                return s[~s.index.duplicated(keep='last')]

            if 'close' in df.columns:
                price_list.append(_clean(df['close'].rename(symbol)))
            else:
                print(f"Warning: 'close' missing in {filename}")

            if 'volume' in df.columns:
                volume_list.append(_clean(df['volume'].rename(symbol)))
            if 'high' in df.columns:
                high_list.append(_clean(df['high'].rename(symbol)))
            if 'low' in df.columns:
                low_list.append(_clean(df['low'].rename(symbol)))
            if 'open' in df.columns:
                open_list.append(_clean(df['open'].rename(symbol)))

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not price_list:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    def _build(lst):
        if not lst:
            return pd.DataFrame()
        df = pd.concat(lst, axis=1)
        df.sort_index(inplace=True)
        return df

    prices_df  = _build(price_list)
    volumes_df = _build(volume_list)
    highs_df   = _build(high_list)
    lows_df    = _build(low_list)
    opens_df   = _build(open_list)

    print(f"Loaded  Prices:{prices_df.shape}  Volumes:{volumes_df.shape}  "
          f"Highs:{highs_df.shape}  Lows:{lows_df.shape}  Opens:{opens_df.shape}")
    if opens_df.empty:
        print("  Warning: No 'open' column found in CSV files. "
              "Entry/exit fills will fall back to close prices.")
    return prices_df, volumes_df, highs_df, lows_df, opens_df


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class CrossSectionalMomentum:
    """
    Batch cross-sectional momentum with daily stop management.

    Per-position state lives in active_holdings[ticker]:
        entry_date, entry_price, peak_price, atr_stop (ratchets up only),
        stop_pct, atr_at_entry, weight, min_price, max_price

    This class holds the strategy CORE only. The event-driven backtest engine,
    trade log, metrics, IC analytics and plots live in csm_batch_backtest.py as
    free functions that take an instance of this class as their first argument.

    Live callers use get_positions() for target weights and get_exit_signals()
    for daily stop/crash-guard monitoring — but neither alone reproduces the
    backtested risk management. Also call, every trading day:
        apply_risk_overlays()        — Corr Guard + Vol Targeting de-lever
        apply_crash_guard_cooldown() — post-panic new-entry freeze
        check_stop_cooldown()        — per-ticker post-stop re-entry ban
    These are the exact methods csm_batch_backtest.py's event-driven loop calls,
    so live and backtested behaviour can't silently diverge on these rules.
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        # Factor
        lookback_months     = 12,
        lag_months          = 1,
        # Universe
        top_n               = 30,
        min_price           = 20.0,
        universe_top_n      = 1000,
        max_circuit_days    = 5,
        buffer_ratio        = 0.2,
        # Stops
        atr_period          = 14,
        atr_multiplier      = 3.0,
        atr_multiplier_high_vol = 2.0,  # tighter chandelier when benchmark vol is elevated
        hard_stop_from_entry    = 0.15,
        hard_stop_from_peak     = 0.20,
        stop_slippage_pct       = 0.003,
        use_trailing_stop       = False,  # True = add the ATR chandelier + peak-hard trail
        stop_cooldown_days      = 20,     # block re-entry N days after a stop on the same ticker
        min_hold_days           = 0,      # stop cannot fire within first N days of entry
        # Risk overlays
        use_crash_guard         = True,
        crash_guard_cooldown    = 10,
        corr_guard_threshold    = 0.8,
        vol_target              = 0.13,
        # Position sizing
        max_weight_per_stock    = 0.05,
        rebalance_months        = 3,      # rebalance cadence: 1=monthly, 3=quarterly, …
        rebalance_min_fill_frac = 0.5,     # skip a scheduled rebalance (keep the prior
                                           # book instead) if it selects fewer than this
                                           # fraction of top_n names — guards against a
                                           # single corrupted reference day (e.g. an
                                           # exchange-holiday row left in the price data)
                                           # emptying the book for the whole cadence
        # Dynamic rank-decay exit (anti-overfit: thresholds are FRACTIONS of top_n)
        rank_exit_dynamic       = True,
        rank_exit_drop_frac     = 0.33,   # cut if rank slid ≥ this × top_n from its best (≈10 at top_n=30)
        rank_exit_floor_frac    = 0.67,   # … AND rank now past this × top_n (≈20 at top_n=30)
        **kwargs,
    ):
        self.prices               = prices_df
        self.volumes              = volumes_df
        self.highs                = highs_df  if highs_df  is not None else pd.DataFrame()
        self.lows                 = lows_df   if lows_df   is not None else pd.DataFrame()
        self.opens                = opens_df  if opens_df  is not None else pd.DataFrame()
        self.benchmark            = benchmark_series

        self.lookback_months      = lookback_months
        self.lag_months           = lag_months
        self.lookback_short_months= max(1, lookback_months // 2)
        self.top_n                = top_n
        self.min_price            = min_price
        self.universe_top_n       = universe_top_n
        self.max_circuit_days     = max_circuit_days
        self.buffer_ratio         = buffer_ratio

        self.atr_period           = atr_period
        self.atr_multiplier       = atr_multiplier
        self.atr_multiplier_high_vol = atr_multiplier_high_vol
        self.hard_stop_from_entry = hard_stop_from_entry
        self.hard_stop_from_peak  = hard_stop_from_peak
        self.stop_slippage_pct    = stop_slippage_pct
        self.use_trailing_stop    = use_trailing_stop
        self.stop_cooldown_days   = stop_cooldown_days
        self.min_hold_days        = min_hold_days

        self.use_crash_guard      = use_crash_guard
        self.crash_guard_cooldown = crash_guard_cooldown
        self.corr_guard_threshold = corr_guard_threshold
        self.vol_target           = vol_target

        self.max_weight_per_stock = max_weight_per_stock
        self.rebalance_months     = rebalance_months
        self.rebalance_min_fill_frac = rebalance_min_fill_frac
        self.rank_exit_dynamic    = rank_exit_dynamic
        self.rank_exit_drop_frac  = rank_exit_drop_frac
        self.rank_exit_floor_frac = rank_exit_floor_frac

        self.factors              = None
        self.momentum_returns     = None
        self.positions            = None
        self.results              = None
        self.position_metadata    = []
        self.atr                  = None

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty
        print(f"CSM Batch initialised  |  top_n={top_n}  buffer={buffer_ratio}"
              f"  lookback={lookback_months}m/{self.lookback_short_months}m"
              f"  ATR-stops={'YES' if has_h and has_l else 'FALLBACK-2%'}"
              f"  opens={'YES' if has_o else 'FALLBACK-close'}"
              f"  crash_guard={'ON' if use_crash_guard else 'OFF'}"
              f"  trailing_stop={'ON' if use_trailing_stop else 'OFF'}"
              f"  rank_decay={'ON' if rank_exit_dynamic else 'OFF'}"
              f"  vol_target={vol_target}  universe_top_n={universe_top_n}")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, daily_prices):
        """
        Boolean mask for stocks eligible to enter the ranked universe.
        Filters (all lookahead-safe via .shift):
          1. Price > min_price (prev month)
          2. 63d rolling median dollar-vol rank ≤ universe_top_n
          3. Circuit days (high==low) in last 63d ≤ max_circuit_days
          4. Price > SMA-200 at month-end
          5. Previous month's return ≥ -15% (falling-knife gate)
        """
        # 1. Price floor (prev month's close to avoid lookahead)
        price_mask = monthly_prices.shift(1) > self.min_price

        # 2. Dynamic liquidity: 63d median dollar-vol rank, shifted before resample
        daily_dvol        = self.prices * self.volumes
        median_dvol_daily = daily_dvol.rolling(window=63, min_periods=21).median().shift(1)
        monthly_dvol      = median_dvol_daily.resample('ME').last().reindex(monthly_prices.index)
        dvol_rank         = monthly_dvol.rank(axis=1, ascending=False, method='min')
        liquidity_mask    = dvol_rank <= self.universe_top_n

        # 3. Circuit-breaker: exclude stocks locked at price limit too often
        circuit_mask = pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)
        if not self.highs.empty and not self.lows.empty:
            is_circuit   = (self.highs == self.lows).shift(1)
            circuit_cnt  = is_circuit.rolling(window=63, min_periods=1).sum()
            monthly_circ = circuit_cnt.resample('ME').last().reindex(monthly_prices.index).fillna(0)
            circuit_mask = monthly_circ <= self.max_circuit_days

        # 4. SMA-200 trend filter (double-shifted to avoid lookahead on boolean)
        sma200_daily = daily_prices.ffill().rolling(window=200, min_periods=150).mean().shift(1)
        is_above_sma = (daily_prices > sma200_daily).shift(1)
        trend_mask   = is_above_sma.resample('ME').last().astype(bool)
        trend_mask   = trend_mask.reindex(monthly_prices.index, fill_value=False)

        # 5. Falling-knife: use prior month's return only
        monthly_ret = monthly_prices.pct_change(fill_method=None)
        crash_mask  = monthly_ret.shift(1) >= -0.15

        return price_mask & liquidity_mask & circuit_mask & trend_mask & crash_mask

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """
        Composite Sharpe momentum factor = (12m Sharpe + 6m Sharpe) / 2, lagged 1m.
        Both legs must agree → reduces false signals from decelerating stocks.
        Stores self.momentum_returns (12m raw return) for the abs-momentum gate.
        """
        print("Calculating Dual-Lookback Factors...")

        monthly_prices = self.prices.resample('ME').last()
        monthly_ret    = monthly_prices.pct_change(fill_method=None)

        L  = self.lookback_months        # e.g. 12
        S  = self.lookback_short_months  # e.g.  6
        lag= self.lag_months             # e.g.  1

        # Long factor: 12m Sharpe; Short factor: 6m Sharpe
        ret_long  = (monthly_prices.shift(lag) / monthly_prices.shift(lag + L)) - 1
        vol_long  = (monthly_ret.rolling(window=L).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_long = (ret_long / vol_long).clip(upper=5.0, lower=-5.0)

        ret_short  = (monthly_prices.shift(lag) / monthly_prices.shift(lag + S)) - 1
        vol_short  = (monthly_ret.rolling(window=S).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_short = (ret_short / vol_short).clip(upper=5.0, lower=-5.0)

        self.factors          = (factor_long + factor_short) / 2.0
        self.momentum_returns = ret_long   # used for abs-momentum gate in get_positions()

        valid_universe        = self.filter_universe(monthly_prices, self.prices)
        self.factors          = self.factors.where(valid_universe)
        self.momentum_returns = self.momentum_returns.where(valid_universe)

        self._prepare_stop_indicators(monthly_prices)
        self.factors.dropna(how='all', inplace=True)
        self.momentum_returns.dropna(how='all', inplace=True)

        # ATR (Wilder EWM): True Range = max(H-L, |H-PrevC|, |L-PrevC|)
        close_p = self.prices
        if not self.highs.empty and not self.lows.empty:
            _h, _l, _pc = self.highs.ffill(), self.lows.ffill(), close_p.shift(1)
            _tr = (_h - _l).abs().combine((_h - _pc).abs(), np.maximum).combine((_l - _pc).abs(), np.maximum)
        else:
            _tr = close_p.diff().abs() * np.sqrt(np.pi / 2)
        self.atr = _tr.ewm(com=self.atr_period - 1, adjust=False).mean()

        # Crash-guard regime inputs: 21d benchmark-return vol + its expanding 95th-pct panic
        # threshold, and a parallel 75th-pct/63d "elevated vol" threshold that gates the
        # tighter high-vol ATR multiplier (both no-lookahead). Computed ONCE here so the
        # backtest loop (STEP C/STEP I) and get_exit_signals() (live) read the identical
        # series — this is the single source of truth for both call sites.
        if self.benchmark is not None:
            bench_ret  = self.benchmark.pct_change(fill_method=None)
            bvol_daily = bench_ret.rolling(window=21).std().shift(1)
            self._panic_threshold_series = bvol_daily.expanding(min_periods=126).quantile(0.95)
            self._panic_threshold        = float(bvol_daily.quantile(0.95))
            self._bvol_daily             = bvol_daily

            # High-vol threshold: identical construction to what the backtest computed
            # inline before this refactor (reindex to the price panel, then expanding
            # 75th-pct/63d, shifted 1 to avoid lookahead).
            _bvol_reidx = bvol_daily.reindex(self.prices.index).ffill()
            self._high_vol_threshold_series = (
                _bvol_reidx.expanding(min_periods=63).quantile(0.75).shift(1).ffill()
            )

            # Live scalars: latest point-in-time (causal) value of each series — the
            # fallback get_exit_signals() uses when `today` can't be matched in the series.
            _p95 = self._panic_threshold_series.dropna()
            self._live_panic_threshold = float(_p95.iloc[-1]) if not _p95.empty else self._panic_threshold
            _p75 = self._high_vol_threshold_series.dropna()
            self._high_vol_threshold   = float(_p75.iloc[-1]) if not _p75.empty else self._panic_threshold
        else:
            self._panic_threshold            = 1.0
            self._live_panic_threshold       = 1.0
            self._high_vol_threshold         = 1.0
            self._panic_threshold_series     = None
            self._high_vol_threshold_series  = None
            self._bvol_daily                 = None

        print(f"Factors shape: {self.factors.shape}  "
              f"Non-NaN per month (avg): {self.factors.notna().sum(axis=1).mean():.0f}")
        return self.factors

    def _prepare_stop_indicators(self, monthly_prices):
        """Pre-compute forward-filled price arrays used by the daily backtest loop."""
        prices_ff = self.prices.ffill()
        # Primary entry/exit fill price; falls back to prev-close if no opens loaded
        self._opens_ff   = self.opens.ffill() if not self.opens.empty else prices_ff.shift(1)
        self._open_proxy = prices_ff.shift(1)   # prev-close: gap-down fallback only
        self._prices_ff  = prices_ff

    # ──────────────────────────────────────────────────────────────────────────
    # SHARED LIVE/BACKTEST RISK-OVERLAY HELPERS
    #
    # Single source of truth for Corr Guard, Vol Targeting, and the two cooldown
    # gates (crash-guard re-entry freeze, per-ticker post-stop ban) plus the
    # panic/high-vol threshold lookup. csm_batch_backtest._run_backtest_core()
    # calls these exact methods instead of re-deriving the math inline, and any
    # live caller uses the same methods on top of get_positions()/get_exit_signals()
    # output — so live and backtest can no longer silently diverge on these rules.
    # ──────────────────────────────────────────────────────────────────────────

    def resolve_regime_threshold(self, series, fallback_scalar, as_of_date):
        """Point-in-time lookup of a causal regime-threshold series (panic or
        high-vol) for a given date. Falls back to the pre-computed scalar (the
        latest value as of the last calculate_factors() call) if the series is
        unavailable or has no observation at/before as_of_date.
        """
        if series is None or series.empty:
            return fallback_scalar
        ts  = pd.Timestamp(as_of_date)
        idx = series.index[series.index <= ts]
        if len(idx) == 0:
            return fallback_scalar
        val = series.loc[idx[-1]]
        return float(val) if pd.notna(val) else fallback_scalar

    def check_stop_cooldown(self, stock, date, stop_cooldown_tickers):
        """Per-ticker post-stop/crash-exit re-entry ban (`stop_cooldown_days`).
        Mirrors the backtest's STEP G cooldown gate exactly.

        `stop_cooldown_tickers` is a caller-owned dict of ticker -> last-exit-date,
        mutated in place (expired entries are removed, matching backtest behaviour).
        Returns True if `stock` may NOT be (re-)entered on `date`.
        """
        if stock not in stop_cooldown_tickers:
            return False
        gap = (pd.Timestamp(date) - pd.Timestamp(stop_cooldown_tickers[stock])).days
        if gap < self.stop_cooldown_days:
            return True
        del stop_cooldown_tickers[stock]
        return False

    def apply_crash_guard_cooldown(self, target_weights, prev_held, cg_cooldown_remaining):
        """Blocks NEW entries (tickers not already held) for `crash_guard_cooldown`
        trading days after a Crash Guard exit. Mirrors the backtest's post-STEP-C
        cooldown gate exactly. Returns (gated_weights, updated_cg_cooldown_remaining).
        """
        if cg_cooldown_remaining <= 0:
            return target_weights, cg_cooldown_remaining
        cg_cooldown_remaining -= 1
        gated = target_weights.copy()
        for stock in list(gated.index):
            if stock not in prev_held and gated[stock] > 1e-6:
                gated[stock] = 0.0
        return gated, cg_cooldown_remaining

    def apply_risk_overlays(self, raw_weights, port_ret_history, prev_weights, stock_ret_window):
        """
        Corr Guard + Vol Targeting (STEP I) — the shared scaling step applied to
        target weights every trading day, in the backtest loop and, identically,
        by any live daily position-sizing job. This is the single implementation;
        do not re-derive this math elsewhere.

        Parameters
        ----------
        raw_weights : pd.Series
            Target weights before overlay scaling (ticker -> weight).
        port_ret_history : sequence of float
            Trailing daily UNSCALED gross portfolio returns (raw weights dotted with
            that day's stock returns), oldest first, most recent last, NOT including
            today. Both overlays are a no-op (scale=1.0) below 21 entries — matching
            the backtest's cold-start behaviour.
        prev_weights : pd.Series
            Yesterday's SCALED executed weights (used to weight per-stock vol in
            Corr Guard).
        stock_ret_window : pd.DataFrame
            Trailing daily per-stock returns (>= 21 rows to activate), NOT including
            today; columns must align with raw_weights/prev_weights (extra columns
            with zero weight are harmless — they contribute nothing to the dot product).

        Returns
        -------
        (scaled_weights, corr_scale, vol_scale)
        """
        CORR_WIN = 21
        VOL_WIN  = 21

        weights = raw_weights.copy()
        gross = float(weights.sum())
        if gross > 1.0:
            weights = weights / gross

        corr_scale = 1.0
        if len(port_ret_history) >= CORR_WIN:
            _pbuf  = np.array(port_ret_history[-CORR_WIN:])
            _p_vol = float(_pbuf.std())
            _w_sum = float(prev_weights.sum())
            if _w_sum > 0 and _p_vol > 0:
                _s_std     = stock_ret_window.iloc[-CORR_WIN:].std()
                _avg_s_vol = float((_s_std * prev_weights).sum() / _w_sum)
                if _avg_s_vol > 0 and (_p_vol / _avg_s_vol) > self.corr_guard_threshold:
                    corr_scale = 0.5

        vol_scale = 1.0
        if len(port_ret_history) >= VOL_WIN:
            _win = port_ret_history[-63:] if len(port_ret_history) >= 63 else port_ret_history[-VOL_WIN:]
            _rv  = float(np.std(_win)) * np.sqrt(252)
            if _rv > 0:
                vol_scale = min(1.0, self.vol_target / _rv)

        scaled_weights = weights * (corr_scale * vol_scale)
        return scaled_weights, corr_scale, vol_scale

    # ──────────────────────────────────────────────────────────────────────────
    # STOP STATE MANAGER
    # ──────────────────────────────────────────────────────────────────────────

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False):
        """
        Stop evaluation for one stock on one bar. atr_stop persists and only ratchets UP.

        effective_stop = max(chandelier, entry_hard, peak_hard)
          L1 Chandelier : new_peak − atr_mult × ATR  (clamped [3%, 30%] below peak)  [trailing only]
          L2 Entry hard : entry_price × (1 − hard_stop_from_entry)
          L3 Peak hard  : new_peak    × (1 − hard_stop_from_peak)                    [trailing only]

        The chandelier (L1) and peak-hard (L3) are the TRAILING component, gated by
        use_trailing_stop. Trigger: intraday LOW (or close). Fill: gap-down (open ≤ stop)
        → open; intraday → stop × (1−slip). Returns (should_exit, fill, stop, holding).
        """
        if pd.isna(curr_close) or curr_close <= 0:
            return False, np.nan, holding.get('atr_stop', np.nan), holding

        entry_price = holding['entry_price']
        peak_price  = holding['peak_price']
        atr_stop    = holding['atr_stop']

        # Force-exit on extreme loss (>60% from entry) — treats as data anomaly
        if not pd.isna(entry_price) and entry_price > 0:
            if (curr_close / entry_price) - 1 < -0.60:
                synthetic_stop = entry_price * 0.40
                fill = curr_open if (not pd.isna(curr_open) and curr_open > 0
                                     and curr_open <= synthetic_stop) \
                       else synthetic_stop * (1.0 - self.stop_slippage_pct)
                return True, float(fill), float(synthetic_stop), holding

        # Seed effective stop using old peak before updating it.
        _trail = self.use_trailing_stop
        peak_hard      = peak_price * (1.0 - self.hard_stop_from_peak) if _trail else -np.inf
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop}

        # Update peak using intraday high (Chandelier anchors to true daily high)
        bar_high = curr_high if (not pd.isna(curr_high) and curr_high > 0) else curr_close
        new_peak = max(peak_price, bar_high)
        if new_peak > peak_price:
            holding['peak_price'] = new_peak

        # L1: chandelier — tighter ATR multiplier in high-vol regime (trailing only)
        _atr_mult = self.atr_multiplier_high_vol if high_vol else self.atr_multiplier
        if _trail and not pd.isna(curr_atr) and curr_atr > 0:
            chandelier = float(np.clip(
                new_peak - _atr_mult * curr_atr,
                new_peak * 0.70,   # max 30% below peak
                new_peak * 0.97,   # min 3% below peak
            ))
            atr_stop = max(atr_stop, chandelier)   # ratchet UP only

        # L2 + L3 recalculated with updated peak
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        peak_hard      = new_peak * (1.0 - self.hard_stop_from_peak) if _trail else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop, 'peak_price': new_peak}

        # Trigger check via intraday low
        check_price = curr_low if (not pd.isna(curr_low) and curr_low > 0) else curr_close
        if check_price > effective_stop:
            return False, np.nan, effective_stop, holding

        # Fill: gap-down → fill at open; intraday breach → stop × (1−slippage)
        _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
        fill  = _open if _open <= effective_stop else effective_stop * (1.0 - self.stop_slippage_pct)
        return True, float(fill), float(effective_stop), holding

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION  (absolute momentum gate; hysteresis; dynamic rank-decay)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self, live_holdings=None):
        """
        Monthly cross-sectional ranking with a hysteresis buffer.

        `live_holdings` is accepted for the uniform engine contract; CSM's target
        is still a stateless weight matrix computed purely from data (its exits —
        RANK_EXIT / genuine top-N REBALANCE — come from the target diff, which is
        already correct), so this is used for exactly one thing: telling the
        final row's circuit-day guard below which names are already held, so it
        never zeroes an existing holding's weight.

        - Absolute-momentum gate: stocks with non-positive 12m return are ineligible.
        - Hysteresis: a held stock stays until its rank drops beyond top_n × (1+buffer_ratio).
        - Dynamic rank-decay exit: cut a held stock whose rank has slid ≥ (drop_frac×top_n)
          from its own best AND is now past (floor_frac×top_n) — flagged RANK_EXIT.
        - Weights: inverse-vol, then a two-pass clip+renorm at max_weight_per_stock.
        - Rebalance cadence guard: when rebalance_months > 1, a scheduled rebalance
          selecting fewer than rebalance_min_fill_frac × top_n names is treated as a
          corrupted reference day and skipped (prior book carried forward) instead of
          being locked in for the whole cadence window.
        """
        if self.factors is None:
            raise ValueError("Call calculate_factors() first.")

        print(f"Generating Positions  top_n={self.top_n}  buffer={self.buffer_ratio}  "
              f"abs_momentum_gate=ON  max_wt={self.max_weight_per_stock:.0%}")

        # Volatility for inverse-vol weighting (shift 1 before resample)
        daily_ret   = self.prices.pct_change(fill_method=None)
        monthly_vol = (daily_ret.rolling(21).std().shift(1)
                       .resample('ME').last()
                       .reindex(self.factors.index))

        all_ranks  = self.factors.rank(axis=1, ascending=False, method='first')

        position_list = []
        prev_held     = set()
        held_best_rank: dict = {}      # ticker → best (lowest) rank seen while held
        rank_exit_records: list = []   # (date, ticker) cut by the rank-decay rule

        entry_threshold = self.top_n
        exit_threshold  = int(self.top_n * (1 + self.buffer_ratio))

        # Dynamic rank-decay thresholds: fractions of top_n (scale-free, anti-overfit).
        if self.rank_exit_dynamic:
            _rk_drop  = max(1, int(round(self.rank_exit_drop_frac  * self.top_n)))
            _rk_floor = max(1, int(round(self.rank_exit_floor_frac * self.top_n)))
            _rk_on    = self.rank_exit_drop_frac > 0
        else:
            _rk_drop, _rk_floor, _rk_on = 0, 0, False

        for date, row_ranks in all_ranks.iterrows():
            valid_ranks = row_ranks.dropna()

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # ── Absolute momentum gate: remove any stock whose 12m raw return ≤ 0 ──
            if date in self.momentum_returns.index:
                pos_ret_stocks = set(
                    self.momentum_returns.loc[date].dropna().loc[lambda s: s > 0].index
                )
                valid_ranks = valid_ranks[valid_ranks.index.isin(pos_ret_stocks)]

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # ── Hysteresis selection + dynamic rank-decay exit ──
            current_selection = []
            for stock, rank in valid_ranks.items():
                if stock in prev_held:
                    # Track the best (lowest) rank achieved while held.
                    best = min(held_best_rank.get(stock, rank), rank)
                    held_best_rank[stock] = best
                    # RANK_EXIT: rank slid ≥ drop from its best AND is now past the floor.
                    if (_rk_on and (rank - best) >= _rk_drop and rank > _rk_floor):
                        rank_exit_records.append((date, stock))
                        continue
                    if rank <= exit_threshold:
                        current_selection.append(stock)
                else:
                    if rank <= entry_threshold:
                        current_selection.append(stock)
                        held_best_rank[stock] = rank

            prev_held = set(current_selection)
            held_best_rank = {k: v for k, v in held_best_rank.items() if k in prev_held}

            if not current_selection:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                continue

            # ── Inverse-vol weights, then two-pass clip+renorm at max_weight_per_stock ──
            sel_vols = monthly_vol.loc[date, current_selection].fillna(0.02).replace(0, 0.02)
            inv_vol  = 1.0 / sel_vols
            raw_w    = inv_vol / inv_vol.sum()

            cap = self.max_weight_per_stock
            for _ in range(2):
                raw_w = raw_w.clip(upper=cap)
                total = raw_w.sum()
                if total > 0:
                    raw_w = raw_w / total   # renormalize
            raw_w = raw_w.clip(upper=cap)   # final safety clip

            full_w = pd.Series(0.0, index=self.factors.columns, name=date)
            full_w.update(raw_w)
            position_list.append(full_w)

        self.positions = pd.concat(position_list, axis=1).T
        self.positions.index = all_ranks.index

        # Rank-decay exit mask (month-end × ticker) — the backtest reads this to label
        # those drops RANK_EXIT instead of REBALANCE.
        self.rank_exit_mask = pd.DataFrame(False, index=all_ranks.index,
                                           columns=self.factors.columns)
        for _d, _s in rank_exit_records:
            if _s in self.rank_exit_mask.columns:
                self.rank_exit_mask.at[_d, _s] = True

        # Configurable rebalance cadence: hold the book N months between rebalances.
        # A scheduled rebalance row that selects suspiciously few names (below
        # rebalance_min_fill_frac × top_n) is more likely a corrupted reference day
        # (e.g. an exchange-holiday row left in the price data, which distorts that
        # month's SMA/momentum calc for the whole universe at once) than a genuine
        # "nothing is eligible" reading — skip it and keep the prior book rather than
        # locking in a near-empty portfolio for the whole rebalance_months window on
        # the strength of one bad day.
        skipped_rebalances = []
        if self.rebalance_months and int(self.rebalance_months) > 1:
            _n = int(self.rebalance_months)
            _real_rows = self.positions.iloc[::_n].copy()

            _min_names      = max(1, int(round(self.rebalance_min_fill_frac * self.top_n)))
            _nonzero_counts = (_real_rows > 1e-6).sum(axis=1)
            _degenerate     = _nonzero_counts < _min_names
            if _degenerate.any():
                skipped_rebalances = list(zip(_real_rows.index[_degenerate],
                                              _nonzero_counts[_degenerate].astype(int)))
                _real_rows.loc[_degenerate] = np.nan
                _real_rows = _real_rows.ffill()

            _sn = self.positions.copy()
            _sn.iloc[:] = np.nan
            _sn.iloc[::_n] = _real_rows
            self.positions = _sn.ffill().fillna(0.0)

        if _rk_on:
            print(f"Rank-decay exit ON [dynamic top_n-frac]: drop≥{_rk_drop} ranks & rank>{_rk_floor}"
                  f"  →  {len(rank_exit_records)} cuts flagged")
        if skipped_rebalances:
            print(f"Rebalance guard: {len(skipped_rebalances)} scheduled rebalance(s) selected "
                  f"fewer than {_min_names} names (likely a corrupted reference day) — "
                  f"kept the prior book instead: {skipped_rebalances}")

        # ── Signal timing (ISSUES.md G2) ──────────────────────────────────────
        # Research activates a month-end row the day AFTER its label. The in-progress
        # month's row carries a FUTURE label and the engine trades iloc[-1], so live
        # acted on a half-formed month. Keep only rows labelled on/before the latest
        # bar, and trim rank_exit_mask to the same rows so the engine's
        # mask.iloc[-1] (RANK_EXIT label) still describes the row it trades. Only
        # the live engine / simulator pass live_holdings; research drivers call
        # get_positions() bare and are unchanged.
        if live_holdings is not None:
            _done = self.positions.index <= self.prices.index[-1]
            if _done.any():
                self.positions = self.positions.loc[_done]
                self.rank_exit_mask = self.rank_exit_mask.loc[self.positions.index]

        # ── Circuit-day guard (today's entry decision only) ───────────────────
        # A stock locked at its circuit limit cannot actually be bought — block
        # only a NEW entry into it on the final (today's live) row; an existing
        # holding is left alone, since a circuit lock is transient and zeroing a
        # held name's weight here would look like a REBALANCE exit the engine
        # can't place either (mirrors hr_breakout_v2/vcp's own same-day circuit
        # guard). This is a monthly weight matrix with no per-day loop to hook
        # into, so it's checked once against the latest daily bar actually
        # available, applied only to the last row.
        if not self.highs.empty and not self.lows.empty and len(self.positions) > 0:
            last_date = self.positions.index[-1]
            locked = (self.highs.iloc[-1] == self.lows.iloc[-1]).reindex(
                self.positions.columns).fillna(False)
            held_now = pd.Index(list((live_holdings or {}).keys()))
            new_entry_locked = (self.positions.loc[last_date] > 1e-6) & locked \
                & ~self.positions.columns.isin(held_now)
            blocked = self.positions.columns[new_entry_locked]
            if len(blocked):
                self.positions.loc[last_date, blocked] = 0.0
                print(f"[Circuit] blocking new entry — locked on latest bar: {list(blocked)}")

        return self.positions


    def get_exit_signals(self,
                         portfolio:      dict,
                         live_data:      dict,
                         benchmark_vol:  float = None,
                         today          = None) -> dict:
        """
        Evaluate all exit rules for currently held positions on one live bar.

        Mirrors csm_batch_backtest._run_backtest_core() STEP C and STEP E exactly:
          • STEP C — Crash Guard : if benchmark rolling-vol > panic threshold,
                                   exit every held position immediately.
          • STEP E — Per-stock   : circuit-day guard → min-hold guard →
                                   three-layer ATR stop via _check_stop_exit().

        NOT covered here — call these shared methods separately (the same ones the
        backtest engine calls, so behaviour can't silently diverge):
          • Rebalance exits      — diff get_positions() output between rebalance dates.
          • Correlation Guard /
            Vol Targeting        — scale-only, do not trigger exits; call
                                    apply_risk_overlays() on target weights every
                                    trading day (not just rebalance days).
          • Crash Guard cooldown — blocks NEW entries for `crash_guard_cooldown` days
                                    after a panic; call apply_crash_guard_cooldown()
                                    alongside get_positions().
          • Stop cooldown        — blocks re-entry into a just-stopped/crash-exited
                                    ticker for `stop_cooldown_days` days; call
                                    check_stop_cooldown() per candidate ticker before
                                    treating a get_positions() name as a fresh entry.

        Parameters
        ----------
        portfolio : dict
            ticker → {
                'entry_price' : float,           # price at which position was entered
                'entry_date'  : date | str,      # ISO-8601 entry date
                'peak_price'  : float,           # highest close/high seen since entry
                'atr_stop'    : float,           # current chandelier stop level
                                                 # (MUST be persisted by caller and
                                                 #  passed back each bar — it only
                                                 #  ratchets UP, never resets)
                'weight'      : float,           # portfolio weight (informational)
            }
        live_data : dict
            ticker → {
                'close' : float,                 # required
                'high'  : float,                 # optional; defaults to close
                'low'   : float,                 # optional; defaults to close
                'open'  : float,                 # optional; defaults to close
                'atr'   : float,                 # optional; defaults to close × 0.02
            }
        benchmark_vol : float, optional
            Today's benchmark rolling-21d daily return std-dev.
            Must use the same scale as the training series (raw daily std, not
            annualised).  If None, Crash Guard and high-vol detection are skipped.
        today : date-like, optional
            Today's date for min-hold-days computation.
            Defaults to datetime.date.today().

        Returns
        -------
        dict with four keys:
            'exits' : dict
                ticker → {
                    'reason'      : str,   # 'CRASH_GUARD' | 'STOP_HIT'
                    'fill_price'  : float, # estimated fill (open or stop × (1−slip))
                    'stop_level'  : float, # effective stop level that was breached
                }
            'holds' : dict
                ticker → {
                    'updated_peak'     : float, # new peak after today's high
                    'updated_atr_stop' : float, # ratcheted chandelier stop — persist this!
                    'stop_level'       : float, # current effective stop level
                }
            'crash_guard_fired' : bool
            'high_vol'          : bool   # True → tighter ATR multiplier active
        """
        import datetime as _dt

        if today is None:
            today = _dt.date.today()
        elif not isinstance(today, _dt.date):
            today = pd.Timestamp(today).date()

        exits: dict = {}
        holds: dict = {}
        crash_guard_fired = False
        high_vol          = False

        # ── Derive regime flags from benchmark_vol ────────────────────────────
        # Point-in-time lookup against the causal series computed in
        # calculate_factors() — NOT the non-causal full-sample scalars — so this
        # matches what the backtest actually validated at this date.
        if benchmark_vol is not None and self.use_crash_guard:
            panic_thr = self.resolve_regime_threshold(
                getattr(self, '_panic_threshold_series', None),
                getattr(self, '_live_panic_threshold', self._panic_threshold),
                today,
            )
            hv_thr = self.resolve_regime_threshold(
                getattr(self, '_high_vol_threshold_series', None),
                getattr(self, '_high_vol_threshold', self._panic_threshold),
                today,
            )
            crash_guard_fired = bool(benchmark_vol > panic_thr)
            high_vol          = bool(benchmark_vol > hv_thr)

        # ── STEP C: Crash Guard — exit ALL positions ──────────────────────────
        if crash_guard_fired:
            for ticker, pos in portfolio.items():
                bar = live_data.get(ticker, {})
                _close = float(bar.get('close', np.nan))
                _open  = float(bar.get('open',  bar.get('close', np.nan)))
                if pd.isna(_open) or _open <= 0:
                    _open = _close
                _atr_stop = float(pos.get('atr_stop', np.nan))
                fill_px   = _open if (not pd.isna(_open) and _open > 0) else _close
                exits[ticker] = {
                    'reason'     : 'CRASH_GUARD',
                    'fill_price' : float(fill_px) if pd.notna(fill_px) else np.nan,
                    'stop_level' : float(_atr_stop),
                }
            return {
                'exits'             : exits,
                'holds'             : {},
                'crash_guard_fired' : True,
                'high_vol'          : high_vol,
            }

        # ── STEP E: Per-stock stop check ──────────────────────────────────────
        for ticker, pos in portfolio.items():
            bar = live_data.get(ticker, {})

            # Pull OHLC — fall back to close for any missing field
            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
                # No usable price — skip; holding state unchanged
                continue

            _high  = float(bar.get('high',  _close))
            _low   = float(bar.get('low',   _close))
            _open  = float(bar.get('open',  _close))
            if pd.isna(_high) or _high <= 0:
                _high = _close
            if pd.isna(_low)  or _low  <= 0:
                _low  = _close
            if pd.isna(_open) or _open <= 0:
                _open = _close

            # ATR fallback: 2% of close (matches backtest default)
            _atr = float(bar.get('atr', np.nan))
            if pd.isna(_atr) or _atr <= 0:
                _atr = _close * 0.02

            # ── Circuit day guard: high == low → price locked, no fills ──────
            # IMPORTANT: only apply this guard when real intraday H/L data was
            # explicitly provided by the caller.  When the caller passes only
            # {'close': ltp}, both _high and _low default to _close, making
            # _high == _low always True and silently suppressing the stop on
            # EVERY tick.  Skip the guard unless real H/L keys are present.
            _has_real_hl = ('high' in bar) and ('low' in bar)
            if _has_real_hl and _high == _low:
                # Defer: return current stop level but do not fire exit
                _atr_stop = float(pos.get('atr_stop', np.nan))
                holds[ticker] = {
                    'updated_peak'     : float(pos.get('peak_price', _close)),
                    'updated_atr_stop' : _atr_stop,
                    'stop_level'       : _atr_stop,
                }
                continue

            # ── Min-hold-days guard ───────────────────────────────────────────
            entry_date_raw = pos.get('entry_date', '')
            try:
                _entry_dt  = pd.Timestamp(str(entry_date_raw)[:10]).date()
                _days_held = (today - _entry_dt).days
            except Exception:
                _days_held = 999   # unknown → treat as past grace period

            # Build the holding dict expected by _check_stop_exit
            holding_state = {
                'entry_price' : float(pos.get('entry_price', np.nan)),
                'entry_date'  : entry_date_raw,
                'peak_price'  : float(pos.get('peak_price',  _close)),
                'atr_stop'    : float(pos.get('atr_stop',    np.nan)),
                'weight'      : float(pos.get('weight',       0.0)),
            }
            # Seed nan atr_stop so the chandelier is computed fresh on first bar
            if pd.isna(holding_state['atr_stop']) or holding_state['atr_stop'] <= 0:
                holding_state['atr_stop'] = 0.0

            should_exit, fill_px, stop_lvl, updated_h = self._check_stop_exit(
                stock      = ticker,
                curr_close = _close,
                curr_low   = _low,
                curr_atr   = _atr,
                curr_open  = _open,
                holding    = holding_state,
                curr_high  = _high,
                high_vol   = high_vol,
            )

            # Override: min-hold-days grace period suppresses stop
            if _days_held < self.min_hold_days:
                should_exit = False

            if should_exit:
                exits[ticker] = {
                    'reason'     : 'STOP_HIT',
                    'fill_price' : float(fill_px)  if pd.notna(fill_px)  else np.nan,
                    'stop_level' : float(stop_lvl) if pd.notna(stop_lvl) else np.nan,
                }
            else:
                holds[ticker] = {
                    'updated_peak'     : float(updated_h.get('peak_price',  _close)),
                    'updated_atr_stop' : float(updated_h.get('atr_stop',    0.0)),
                    'stop_level'       : float(stop_lvl) if pd.notna(stop_lvl) else np.nan,
                }

        return {
            'exits'             : exits,
            'holds'             : holds,
            'crash_guard_fired' : crash_guard_fired,
            'high_vol'          : high_vol,
        }

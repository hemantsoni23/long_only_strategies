"""
csm_batch_strategy.py
=====================
Cross-Sectional Momentum — Batch Strategy  (strategy CORE only).

Strategy logic only: the data loader plus the CrossSectionalMomentum class
(universe / factor / position / live-exit methods). No backtest engine, metrics,
IC, or plotting code lives here — see csm_batch_backtest.py for that, and
run_csm_batch_strategy.py for the thin orchestration runner.

Mirrors the csm_absolute.py / momentum_strategy.py organization. Verbatim port of
the strategy-core pieces of csm_stock_strategy.py; behavior is unchanged.

Signal  : dual-lookback Sharpe (12m + 6m), absolute-momentum gate, hysteresis buffer
Universe: top-N liquidity, price floor, circuit-breaker, SMA-200, falling-knife
Stops   : three-layer ATR chandelier + entry hard stop + peak hard stop (daily loop)
Overlays: Crash Guard, Correlation Guard, vol targeting (all in-loop, no lookahead)
"""

import pandas as pd
import numpy as np
import os
import glob


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADER  (v2: also loads High & Low)
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
# EQUAL-RISK-CONTRIBUTION SOLVER  (Lever 2 — correlation-aware weighting)
# ══════════════════════════════════════════════════════════════════════════════

def _erc_weights(cov, max_iter=250, tol=1e-9):
    """
    Equal-Risk-Contribution weights from a covariance matrix — each name
    contributes the same share of portfolio variance (down-weights correlated
    clusters vs plain inverse-vol). Damped multiplicative fixed-point seeded from
    inverse-vol. Returns a numpy array, or None on degenerate input so the caller
    can fall back to inverse-vol.
    """
    cov = np.asarray(cov, dtype=float)
    n = cov.shape[0]
    if n == 0 or not np.all(np.isfinite(cov)):
        return None
    d = np.diag(cov).astype(float).copy()
    pos = d[d > 0]
    if pos.size == 0:
        return None
    floor = np.median(pos)
    d = np.where(np.isfinite(d) & (d > 0), d, floor)          # floor degenerate variances
    vol = np.sqrt(d)
    w = 1.0 / vol
    if not np.isfinite(w).all() or w.sum() <= 0:
        return None
    w = w / w.sum()
    cov = cov + np.eye(n) * (floor * 1e-8)                    # ridge for PSD stability
    for _ in range(max_iter):
        mrc = cov @ w                                        # marginal risk contribution
        rc = w * mrc                                         # risk contribution per name
        s = rc.sum()
        if not np.isfinite(s) or s <= 0:
            return None
        upd = np.sqrt((s / n) / np.maximum(rc, 1e-16))       # nudge each rc toward the mean
        w_new = np.maximum(w * upd, 0.0)
        if w_new.sum() <= 0:
            return None
        w_new = w_new / w_new.sum()
        if np.max(np.abs(w_new - w)) < tol:
            w = w_new
            break
        w = w_new
    return w


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
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        lookback_months     = 12,
        lag_months          = 1,
        top_n               = 100,
        min_price           = 20.0,
        universe_top_n      = 2000,
        max_circuit_days    = 5,
        buffer_ratio        = 0.2,
        atr_period          = 14,
        atr_multiplier      = 3.0,
        atr_cap_percentile  = 0.75,
        atr_cap_window      = 63,
        hard_stop_from_entry    = 0.15,
        hard_stop_from_peak     = 0.20,
        stop_slippage_pct       = 0.003,
        use_crash_guard         = True,
        crash_guard_cooldown    = 10,
        corr_guard_threshold    = 0.8,
        stop_cooldown_days      = 20,   # block re-entry N days after stop on same ticker
        min_hold_days           = 5,    # stop cannot fire within first N days of entry
        atr_multiplier_high_vol = 2.0,  # tighter chandelier when benchmark vol is elevated
        max_weight_per_stock    = 0.05,
        vol_target              = 0.15,
        breakeven_arm_pct       = 0.0,   # arm a profit-lock once peak gain ≥ this (0 = off)
        breakeven_lock_pct      = 0.0,   # locked stop = entry × (1 + this) once armed
        use_trailing_stop       = True,  # False = drop the ATR chandelier + peak-hard trail
        rebalance_months        = 1,     # rebalance cadence: 1=monthly, 3=quarterly, …
        rank_exit_drop          = 0,     # RANK_EXIT: cut if rank slid ≥ this from its best (0 = off)
        rank_exit_floor         = 20,    # … AND current rank is past this floor
        weighting_scheme        = 'inv_vol',  # 'inv_vol' (default) | 'rank' | 'erc'
        weight_buffer           = 0.0,   # Lever 4: no-trade band on a held name's weight (0 = off)
        erc_cov_window          = 126,   # Lever 2: trailing days for the ERC covariance estimate
        use_trend_exit          = False, # NEW EXIT: drop a held name on a daily close below its 200-SMA
        trend_exit_buffer       = 0.0,   # … require close < SMA200×(1−buffer); 0 = exact cross
        trend_exit_min_hold     = 0,     # … but never within the first N days of the trade (whipsaw guard)
        use_reversal_exit       = False, # NEW EXIT: drop a held name whose factor rank collapses to bottom quintile
        reversal_exit_pct       = 0.20,  # … "bottom quintile" = worst this fraction of the ranked universe
        use_vol_spike_trim      = False, # NEW SIZING: trim a held name whose realised vol spikes vs entry
        vol_spike_mult          = 2.0,   # … trigger when Nd vol > mult × the name's vol at entry
        vol_spike_window        = 5,     # … realised-vol lookback in days
        use_nav_kill_switch     = False, # NEW RISK: cut gross on the strategy's OWN NAV drawdown
        kill_dd_warn            = -0.10, # … −10% from peak → scale gross to kill_reduce_scale
        kill_dd_flat            = -0.15, # … −15% from peak → flatten (gross 0)
        kill_reduce_scale       = 0.5,   # … gross multiplier while in the warn band
        # ── DYNAMIC (anti-overfit) variants: thresholds self-scale to the strategy's own regime ──
        kill_dynamic            = False, # kill-switch DD thresholds = K_sigma × EXPANDING annualised vol
        kill_warn_sigma         = 0.7,   # … warn band  (≈ −10% at the baseline ~13% vol; auto-scales)
        kill_flat_sigma         = 1.1,   # … flat band  (≈ −15% at the baseline ~13% vol; auto-scales)
        kill_vol_window         = 63,    # … MIN days of history before the expanding-vol estimate is used
        rank_exit_dynamic       = False, # rank-decay thresholds as FRACTIONS of top_n (scale-free)
        rank_exit_drop_frac     = 0.33,  # … cut if rank slid ≥ this × top_n from its best (≈10 at top_n=30)
        rank_exit_floor_frac    = 0.67,  # … … AND rank now past this × top_n (≈20 at top_n=30)
        lev_max                 = 1.0,   # Calmar lever: max gross when calm (>1.0 ⇒ lever up in low-vol)
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
        self.atr_cap_percentile   = atr_cap_percentile
        self.atr_cap_window       = atr_cap_window
        self.hard_stop_from_entry = hard_stop_from_entry
        self.hard_stop_from_peak  = hard_stop_from_peak
        self.stop_slippage_pct    = stop_slippage_pct

        self.use_crash_guard          = use_crash_guard
        self.crash_guard_cooldown     = crash_guard_cooldown
        self.corr_guard_threshold     = corr_guard_threshold
        self.stop_cooldown_days       = stop_cooldown_days
        self.min_hold_days            = min_hold_days
        self.atr_multiplier_high_vol  = atr_multiplier_high_vol
        self.max_weight_per_stock     = max_weight_per_stock
        self.vol_target               = vol_target
        self.breakeven_arm_pct        = breakeven_arm_pct
        self.breakeven_lock_pct       = breakeven_lock_pct
        self.use_trailing_stop        = use_trailing_stop
        self.rebalance_months         = rebalance_months
        self.rank_exit_drop           = rank_exit_drop
        self.rank_exit_floor          = rank_exit_floor
        self.weighting_scheme         = weighting_scheme
        self.weight_buffer            = weight_buffer
        self.erc_cov_window           = erc_cov_window
        self.use_trend_exit           = use_trend_exit
        self.trend_exit_buffer        = trend_exit_buffer
        self.trend_exit_min_hold      = trend_exit_min_hold
        self.use_reversal_exit        = use_reversal_exit
        self.reversal_exit_pct        = reversal_exit_pct
        self.use_vol_spike_trim       = use_vol_spike_trim
        self.vol_spike_mult           = vol_spike_mult
        self.vol_spike_window         = vol_spike_window
        self.use_nav_kill_switch      = use_nav_kill_switch
        self.kill_dd_warn             = kill_dd_warn
        self.kill_dd_flat             = kill_dd_flat
        self.kill_reduce_scale        = kill_reduce_scale
        self.kill_dynamic             = kill_dynamic
        self.kill_warn_sigma          = kill_warn_sigma
        self.kill_flat_sigma          = kill_flat_sigma
        self.kill_vol_window          = kill_vol_window
        self.rank_exit_dynamic        = rank_exit_dynamic
        self.rank_exit_drop_frac      = rank_exit_drop_frac
        self.rank_exit_floor_frac     = rank_exit_floor_frac
        self.lev_max                  = lev_max
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
              f"  stop_cooldown={stop_cooldown_days}d  min_hold={min_hold_days}d"
              f"  atr_mult={atr_multiplier}/{atr_multiplier_high_vol}(hv)"
              f"  universe_top_n={universe_top_n}  state=active_holdings")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, monthly_avg_dvol, daily_prices):
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

        # Month-end prices / volumes
        monthly_prices   = self.prices.resample('ME').last()
        monthly_volumes  = self.volumes.resample('ME').mean() if not self.volumes.empty else None

        # Dollar-volume for the universe filter
        daily_dvol       = self.prices * self.volumes
        monthly_avg_dvol = daily_dvol.resample('ME').mean()

        monthly_ret = monthly_prices.pct_change(fill_method=None)

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

        self.factors       = (factor_long + factor_short) / 2.0
        self.momentum_returns = ret_long   # used for abs-momentum gate in get_positions()

        valid_universe        = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)
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
        self.atr = _tr.ewm(com=self.atr_period - 1, adjust=False).mean().shift(1)

        # Daily SMA-200 panel for the optional TREND_EXIT overlay. Stored RAW (unshifted);
        # the engine compares the PREVIOUS day's close to the PREVIOUS day's SMA and fills at
        # today's open, so the exit is lookahead-safe without shifting here.
        self._sma200_daily = self.prices.ffill().rolling(window=200, min_periods=150).mean()

        # Daily realised-vol panel (close-to-close std) for the optional VOL-SPIKE TRIM. The
        # engine compares the PREVIOUS day's vol to the name's vol AT ENTRY (lookahead-safe).
        _vw = max(2, int(self.vol_spike_window))
        self._vol_daily = (self.prices.pct_change(fill_method=None)
                           .rolling(window=_vw, min_periods=max(2, _vw // 2)).std())
        # NOTE: the SIGNAL_REVERSAL mask is built in get_positions() (not here) so it tracks the
        # current reversal_exit_pct each run — calculate_factors is computed only once and reused.

        # Panic threshold: expanding 95th-pct of 21d benchmark vol (no lookahead)
        if self.benchmark is not None:
            bench_ret  = self.benchmark.pct_change(fill_method=None)
            bvol_daily = bench_ret.rolling(window=21).std().shift(1)
            self._panic_threshold_series = bvol_daily.expanding(min_periods=126).quantile(0.95)
            self._panic_threshold        = float(bvol_daily.quantile(0.95))
            # Live thresholds: final expanding value (no lookahead; used by get_exit_signals)
            _expand_95_final             = self._panic_threshold_series.dropna()
            self._live_panic_threshold   = float(_expand_95_final.iloc[-1]) if not _expand_95_final.empty else self._panic_threshold
            _expand_75                   = bvol_daily.expanding(min_periods=63).quantile(0.75)
            _expand_75_final             = _expand_75.dropna()
            self._high_vol_threshold     = float(_expand_75_final.iloc[-1]) if not _expand_75_final.empty else float(bvol_daily.quantile(0.75))
            self._bench_vol_monthly      = bvol_daily.resample('ME').last()
            self._bvol_daily             = bvol_daily
        else:
            self._panic_threshold        = 1.0
            self._live_panic_threshold   = 1.0
            self._high_vol_threshold     = 1.0
            self._panic_threshold_series = None
            self._bench_vol_monthly      = None
            self._bvol_daily             = None

        print(f"Factors shape: {self.factors.shape}  "
              f"Non-NaN per month (avg): {self.factors.notna().sum(axis=1).mean():.0f}")
        return self.factors

    def _prepare_stop_indicators(self, monthly_prices):
        """Pre-compute forward-filled price arrays used by the daily backtest loop."""
        has_hl    = not self.highs.empty and not self.lows.empty
        prices_ff = self.prices.ffill()

        if has_hl:
            highs_ff = self.highs.ffill()
            lows_ff  = self.lows.ffill()
            self._monthly_highs = highs_ff.resample('ME').max().reindex(monthly_prices.index)
            self._monthly_lows  = lows_ff.resample('ME').min().reindex(monthly_prices.index)
        else:
            self._monthly_highs = monthly_prices.copy()
            self._monthly_lows  = monthly_prices.copy()

        # Primary entry/exit fill price; falls back to prev-close if no opens loaded
        self._opens_ff   = self.opens.ffill() if not self.opens.empty else prices_ff.shift(1)
        self._open_proxy = prices_ff.shift(1)   # prev-close: gap-down fallback only
        self._prices_ff  = prices_ff

    # ──────────────────────────────────────────────────────────────────────────
    # STOP STATE MANAGER  (ported from IndividualMomentumStrategy v3)
    # ──────────────────────────────────────────────────────────────────────────

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False):
        """
        Three-layer stop evaluation for one stock on one bar.
        atr_stop persists across calls and only ratchets UP.

        Layers: effective_stop = max(chandelier, entry_hard, peak_hard)
          L1 Chandelier : new_peak − atr_mult × ATR  (clamped [3%, 30%] below peak)
          L2 Entry hard : entry_price × (1 − hard_stop_from_entry)
          L3 Peak hard  : new_peak    × (1 − hard_stop_from_peak)

        Trigger: checked via intraday LOW (or close if low unavailable).
        Fill   : gap-down (open ≤ stop) → fill at open; intraday → stop × (1−slip).
        Returns: (should_exit, fill_price, stop_level, updated_holding)

        Shared by the live exit evaluator (get_exit_signals) and the backtest
        engine (csm_batch_backtest._run_backtest_core), so it lives in the core.
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

        # Seed effective stop using old peak before updating it. The chandelier (L1)
        # and peak-hard (L3) are the TRAILING component — gated by use_trailing_stop.
        _trail = getattr(self, 'use_trailing_stop', True)
        peak_hard      = peak_price * (1.0 - self.hard_stop_from_peak) if _trail else -np.inf
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop}

        # Update peak using intraday high (Chandelier Exit anchors to true daily high)
        bar_high = curr_high if (not pd.isna(curr_high) and curr_high > 0) else curr_close
        new_peak = max(peak_price, bar_high)
        if new_peak > peak_price:
            holding['peak_price'] = new_peak

        # L1: chandelier — tighter ATR multiplier in high-vol regime
        _atr_mult = self.atr_multiplier_high_vol if high_vol else self.atr_multiplier
        if _trail and not pd.isna(curr_atr) and curr_atr > 0:
            chandelier = float(np.clip(
                new_peak - _atr_mult * curr_atr,
                new_peak * 0.70,   # max 30% below peak
                new_peak * 0.97,   # min 3% below peak
            ))
            atr_stop = max(atr_stop, chandelier)   # ratchet UP only

        # L1b: profit-lock — once peak gain ≥ breakeven_arm_pct, never let the stop
        # sit below the locked level (entry × (1 + breakeven_lock_pct)). Converts
        # "rose then reversed to a loss" trades into ~break-even exits. (0 = off.)
        if getattr(self, 'breakeven_arm_pct', 0.0) > 0 and not pd.isna(entry_price) and entry_price > 0:
            if (new_peak / entry_price - 1.0) >= self.breakeven_arm_pct:
                be_floor = entry_price * (1.0 + getattr(self, 'breakeven_lock_pct', 0.0))
                atr_stop = max(atr_stop, be_floor)   # ratchet UP only

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
    # POSITION GENERATION  (v2: absolute momentum gate; hysteresis preserved)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self):
        """
        Monthly cross-sectional ranking with hysteresis buffer.

        NEW: Stocks with non-positive 12m return (self.momentum_returns ≤ 0)
        are ineligible regardless of their cross-sectional Sharpe rank.
        This prevents holding the "least-bad" names in a broad bear market.

        PRESERVED: Hysteresis buffer — a held stock stays in the portfolio
        until its rank drops beyond top_n × (1 + buffer_ratio), reducing churn.
        """
        if self.factors is None:
            raise ValueError("Call calculate_factors() first.")

        print(f"Generating Positions  "
              f"top_n={self.top_n}  buffer={self.buffer_ratio}  "
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

        # Rank-decay thresholds: fixed absolute ranks, OR (anti-overfit) fractions of top_n so
        # they scale with the portfolio's concentration instead of being pinned to magic numbers.
        if getattr(self, 'rank_exit_dynamic', False):
            _rk_drop  = max(1, int(round(self.rank_exit_drop_frac  * self.top_n)))
            _rk_floor = max(1, int(round(self.rank_exit_floor_frac * self.top_n)))
        else:
            _rk_drop, _rk_floor = self.rank_exit_drop, self.rank_exit_floor
        _rk_on = (self.rank_exit_drop > 0) or (getattr(self, 'rank_exit_dynamic', False)
                                               and self.rank_exit_drop_frac > 0)

        for date, row_ranks in all_ranks.iterrows():
            valid_ranks = row_ranks.dropna()

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # ── Absolute momentum gate ────────────────────────────────────────
            # Remove any stock whose 12m raw return is non-positive.
            if date in self.momentum_returns.index:
                pos_ret_stocks = set(
                    self.momentum_returns.loc[date].dropna()
                    .loc[lambda s: s > 0].index
                )
                valid_ranks = valid_ranks[valid_ranks.index.isin(pos_ret_stocks)]

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # ── Hysteresis selection + rank-decay exit ────────────────────────
            current_selection = []
            for stock, rank in valid_ranks.items():
                if stock in prev_held:
                    # Track the best (lowest) rank achieved while held.
                    best = min(held_best_rank.get(stock, rank), rank)
                    held_best_rank[stock] = best
                    # RANK_EXIT: rank slid ≥ drop from its best AND is now past the floor →
                    # cut it earlier than the hysteresis would. Thresholds fixed or top_n-relative.
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

            # ── Base weights: inverse-vol (default) or rank-based linear decay ──
            # Then a two-pass clip+renorm at max_weight_per_stock so the book stays
            # fully invested even when several names hit the cap.
            _scheme = getattr(self, 'weighting_scheme', 'inv_vol')
            if _scheme == 'rank':
                # Rank decay: best-ranked (rank 1) gets the largest share; weights
                # fall off linearly down the selection. Concentrates on top names.
                sel_ranks = valid_ranks.reindex(current_selection)
                sel_ranks = sel_ranks.fillna(sel_ranks.max())
                score     = (sel_ranks.max() + 1.0) - sel_ranks
                raw_w     = score / score.sum()
            elif _scheme == 'erc' and len(current_selection) >= 2:
                # Lever 2: equal-risk-contribution from a trailing covariance of the
                # selected names (point-in-time: strictly before this month-end).
                # Down-weights correlated clusters; falls back to inverse-vol if the
                # covariance estimate is too short or degenerate.
                _win  = int(getattr(self, 'erc_cov_window', 126))
                _rets = (daily_ret[current_selection]
                         .loc[daily_ret.index < date].iloc[-_win:].fillna(0.0))
                _erc  = _erc_weights(_rets.cov().values) if len(_rets) >= 21 else None
                if _erc is not None and np.isfinite(_erc).all() and _erc.sum() > 0:
                    raw_w = pd.Series(_erc, index=current_selection)
                else:
                    sel_vols = monthly_vol.loc[date, current_selection].fillna(0.02).replace(0, 0.02)
                    raw_w    = (1.0 / sel_vols); raw_w = raw_w / raw_w.sum()
            else:
                sel_vols = monthly_vol.loc[date, current_selection].fillna(0.02).replace(0, 0.02)
                inv_vol  = 1.0 / sel_vols
                raw_w    = inv_vol / inv_vol.sum()

            # Two-pass clip-and-renorm
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

        # ── Rank-decay exit mask (month-end × ticker) — the backtest reads this
        #    to label those drops RANK_EXIT instead of REBALANCE. ───────────────
        self.rank_exit_mask = pd.DataFrame(False, index=all_ranks.index,
                                           columns=self.factors.columns)
        for _d, _s in rank_exit_records:
            if _s in self.rank_exit_mask.columns:
                self.rank_exit_mask.at[_d, _s] = True

        # ── Signal-reversal mask (month-end × ticker): True where a name's factor rank sits in
        #    the bottom `reversal_exit_pct` of that month's ranked universe. Built HERE so it
        #    tracks the current reversal_exit_pct on every get_positions() (calculate_factors is
        #    computed once and reused across configs). rank 1 = best → percentile ≈ 1 = worst.
        _nk  = self.factors.notna().sum(axis=1).replace(0, np.nan)
        _pct = all_ranks.div(_nk, axis=0)
        self.reversal_exit_mask = (_pct > (1.0 - self.reversal_exit_pct)).fillna(False)

        # ── Configurable rebalance cadence: hold the book N months between
        #    rebalances (1 = monthly default → no change). ──────────────────────
        if self.rebalance_months and int(self.rebalance_months) > 1:
            _n  = int(self.rebalance_months)
            _sn = self.positions.copy()
            _sn.iloc[:] = np.nan
            _sn.iloc[::_n] = self.positions.iloc[::_n]
            self.positions = _sn.ffill().fillna(0.0)

        # ── Weight buffer zone (Lever 4): hold a continuing name's weight unless it
        #    drifts > weight_buffer from its prior value — cuts rebalancing churn.
        #    Entries (0→w) and exits (w→0) always trade. ────────────────────────
        _wb = getattr(self, 'weight_buffer', 0.0)
        if _wb and _wb > 0 and len(self.positions) > 1:
            _rows, _prev = [], None
            for _dt, _row in self.positions.iterrows():
                _cur = _row.copy()
                if _prev is not None:
                    _keep = (_cur > 1e-9) & (_prev > 1e-9) & ((_cur - _prev).abs() < _wb)
                    _cur[_keep] = _prev[_keep]
                _rows.append(_cur)
                _prev = _cur
            self.positions = pd.DataFrame(_rows, index=self.positions.index)

        if _rk_on:
            _mode = "dynamic(top_n-frac)" if getattr(self, 'rank_exit_dynamic', False) else "fixed"
            print(f"Rank-decay exit ON [{_mode}]: drop≥{_rk_drop} ranks & rank>{_rk_floor}"
                  f"  →  {len(rank_exit_records)} cuts flagged")
        return self.positions

    # ──────────────────────────────────────────────────────────────────────────
    # LIVE EXIT SIGNAL EVALUATOR
    # ──────────────────────────────────────────────────────────────────────────

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

        NOT covered here (caller is responsible):
          • Rebalance exits   — diff get_positions() output between rebalance dates.
          • Correlation Guard — scale-only; does not trigger exits.
          • Vol Targeting     — scale-only; does not trigger exits.

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
        if benchmark_vol is not None and self.use_crash_guard:
            panic_thr    = getattr(self, '_live_panic_threshold', self._panic_threshold)
            hv_thr       = getattr(self, '_high_vol_threshold',   self._panic_threshold)
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

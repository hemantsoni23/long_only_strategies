"""
hr_breakout_strategy.py
=======================
Horizontal Resistance (HR) Breakout Strategy — Event-Driven Backtest

Signal  : HR breakout — cluster of local-peak highs breached above resistance
Universe: top-500 by dollar volume | price ≥ ₹10 | circuit ≤5/63d | prior month ≥-15%
Regime  : benchmark SMA-50 streak < 5d (bench_ok only)
Trend   : EMA 50/150/200 aligned | EMA-200 slope | 52w high band | RS top 25%
Stops   : chandelier [1.5–3×ATR, clamped 12–30%] | entry floor | peak floor
Exits   : STOP_HIT | TIME_STOP (≥45d, profit<-5%) | CIRCUIT_TIMEOUT | END_OF_DATA
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
        print("  Warning: No 'open' column found. Entry/exit fills fall back to close prices.")

    return prices_df, volumes_df, highs_df, lows_df, opens_df


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class HRBreakoutStrategy:
    """
    Event-driven Horizontal Resistance Breakout strategy.

    Per-position state lives in active_holdings[ticker]:
        entry_date, entry_price, peak_price, atr_stop (ratchets up only),
        stop_pct, atr_at_entry, weight, min_price, max_price
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df              = None,
        lows_df               = None,
        opens_df              = None,
        # Universe
        universe_top_n        = 1000,       # top-N stocks by median dollar volume (upper bound)
        universe_min_n        = 1,          # bottom rank bound — stocks ranked below this excluded
        min_price             = 10.0,       # minimum prior-day close (₹)
        max_circuit_days      = 5,          # max locked days in 63-day window
        prior_month_min_ret   = -0.15,      # prior 22d return floor
        # Regime
        benchmark_sma_period  = 50,         # SMA period for benchmark trend
        benchmark_streak_max  = 5,          # max consecutive days below SMA-50
        # Trend gate
        ema_fast              = 50,
        ema_mid               = 150,
        ema_slow              = 200,
        ema_slope_window      = 20,         # bars to look back for EMA-200 slope
        high_band_pct         = 0.75,       # close >= 75% of 52w high
        rs_lookback           = 126,        # 6-month RS lookback (trading days)
        rs_top_pct            = 0.30,       # top 30% by RS excess return
        # HR Signal
        peak_wing             = 2,          # bars each side for local peak detection
        cluster_lookback      = 60,         # bars to look back for peak cluster
        cluster_min_peaks     = 3,          # minimum peaks to form a cluster
        cluster_spread_pct    = 0.015,      # max (high-low)/low spread in cluster
        breakout_buffer       = 0.005,      # close must exceed cluster_top by 0.5%
        entry_gap_cancel_pct  = 0.03,       # skip entry if open gaps >3% above prior close
        momentum_rank_window  = 30,         # candidate ranking: N-day momentum window
        max_positions         = 10,         # max concurrent open positions
        # Position sizing
        risk_pct_per_trade    = 0.01,       # fraction of portfolio risked per trade (1%)
        position_ceil         = 0.20,       # max weight any single position can reach
        position_floor        = 0.02,       # min weight any single position can reach
        # Stops
        atr_period            = 14,         # ATR lookback (Wilder EWM, com=13)
        atr_multiplier_max    = 3.0,        # chandelier mult for calm (low ATR%) names
        atr_multiplier_min    = 1.5,        # chandelier mult for volatile (high ATR%) names
        atr_pct_calm          = 0.020,      # ATR/price <= this -> full atr_multiplier_max
        atr_pct_volatile      = 0.045,      # ATR/price >= this -> full atr_multiplier_min
        chandelier_clamp_min  = 0.12,       # chandelier never closer than 12% to peak
        chandelier_clamp_max  = 0.30,       # chandelier never farther than 30% from peak
        hard_stop_from_entry  = 0.10,       # entry floor = entry × (1 − 10%)
        hard_stop_from_peak   = 0.10,       # peak floor  = peak  × (1 − 10%)
        stop_slippage_pct     = 0.003,      # fill slippage on intraday stop breach
        # Lockout
        stop_cooldown_days    = 20,         # re-entry block after STOP_HIT
        # Time stop
        min_hold_days         = 20,         # chandelier suppressed for first N days (only entry floor active)
        time_stop_min_days    = 45,         # time stop evaluated after N days
        time_stop_min_profit  = -0.05,      # exit if profit < -5% after time_stop_min_days (only genuinely broken trades)
        # Warmup
        warmup_days           = 252,        # trading days before first trade allowed
    ):
        self.prices               = prices_df
        self.volumes              = volumes_df
        self.highs                = highs_df  if highs_df  is not None else pd.DataFrame()
        self.lows                 = lows_df   if lows_df   is not None else pd.DataFrame()
        self.opens                = opens_df  if opens_df  is not None else pd.DataFrame()

        # Universe
        self.universe_top_n       = universe_top_n
        self.universe_min_n       = universe_min_n
        self.min_price            = min_price
        self.max_circuit_days     = max_circuit_days
        self.prior_month_min_ret  = prior_month_min_ret

        # Regime
        self.benchmark_sma_period = benchmark_sma_period
        self.benchmark_streak_max = benchmark_streak_max

        # Trend gate
        self.ema_fast             = ema_fast
        self.ema_mid              = ema_mid
        self.ema_slow             = ema_slow
        self.ema_slope_window     = ema_slope_window
        self.high_band_pct        = high_band_pct
        self.rs_lookback          = rs_lookback
        self.rs_top_pct           = rs_top_pct

        # HR signal
        self.peak_wing            = peak_wing
        self.cluster_lookback     = cluster_lookback
        self.cluster_min_peaks    = cluster_min_peaks
        self.cluster_spread_pct   = cluster_spread_pct
        self.breakout_buffer      = breakout_buffer
        self.entry_gap_cancel_pct = entry_gap_cancel_pct
        self.momentum_rank_window = momentum_rank_window
        self.max_positions        = max_positions

        # Sizing
        self.risk_pct_per_trade   = risk_pct_per_trade
        self.position_ceil        = position_ceil
        self.position_floor       = position_floor

        # Stops
        self.atr_period           = atr_period
        self.atr_multiplier_max   = atr_multiplier_max
        self.atr_multiplier_min   = atr_multiplier_min
        self.atr_pct_calm         = atr_pct_calm
        self.atr_pct_volatile     = atr_pct_volatile
        self.chandelier_clamp_min = chandelier_clamp_min
        self.chandelier_clamp_max = chandelier_clamp_max
        self.hard_stop_from_entry = hard_stop_from_entry
        self.hard_stop_from_peak  = hard_stop_from_peak
        self.stop_slippage_pct    = stop_slippage_pct

        # Lockout / time stop
        self.stop_cooldown_days   = stop_cooldown_days
        self.min_hold_days        = min_hold_days
        self.time_stop_min_days   = time_stop_min_days
        self.time_stop_min_profit = time_stop_min_profit
        self.warmup_days          = warmup_days

        # State
        self.atr              = None
        self.results          = None
        self.position_metadata = []

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty

        print(
            f"HR Breakout Strategy initialised\n"
            f"  Universe     : rank {universe_min_n}–{universe_top_n} by dVol | min_price=₹{min_price}"
            f"  | circuit≤{max_circuit_days}/63d | prior_month≥{prior_month_min_ret*100:.0f}%\n"
            f"  Regime       : benchmark SMA-{benchmark_sma_period} streak<{benchmark_streak_max}d\n"
            f"  Trend gate   : EMA {ema_fast}/{ema_mid}/{ema_slow} aligned | slope-{ema_slope_window}d"
            f"  | 52w high band | RS top {rs_top_pct*100:.0f}%\n"
            f"  HR Signal    : wing={peak_wing} | lookback={cluster_lookback}bars"
            f"  | ≥{cluster_min_peaks} peaks | spread≤{cluster_spread_pct*100:.1f}%"
            f"  | breakout buffer={breakout_buffer*100:.1f}%\n"
            f"  Stops        : chandelier peak−[{atr_multiplier_min},{atr_multiplier_max}]×ATR14 (dynamic by ATR%%)"
            f" clamped [{chandelier_clamp_min*100:.0f}%-{chandelier_clamp_max*100:.0f}%] | entry−{hard_stop_from_entry*100:.0f}%"
            f"  | peak−{hard_stop_from_peak*100:.0f}%\n"
            f"  Time stop    : after {time_stop_min_days}d | profit<{time_stop_min_profit*100:.0f}%\n"
            f"  Max positions: {max_positions} | risk={risk_pct_per_trade*100:.1f}%/trade | ceil={position_ceil*100:.0f}% | floor={position_floor*100:.0f}%\n"
            f"  OHLCV data   : H={'YES' if has_h else 'NO'}  L={'YES' if has_l else 'NO'}"
            f"  O={'YES' if has_o else 'FALLBACK-close'}"
        )

    # ──────────────────────────────────────────────────────────────────────────
    # PRE-COMPUTE INDICATORS
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """
        Pre-compute all daily indicator arrays required by the event loop.
        Strictly uses .shift(1) throughout — no lookahead.
        """
        print("\nPre-computing indicators...")
        prices = self.prices.ffill()
        highs  = self.highs.ffill()  if not self.highs.empty  else prices.copy()
        lows   = self.lows.ffill()   if not self.lows.empty   else prices.copy()

        # ── ATR-14 (Wilder EWM, com=13) ──────────────────────────────────────
        prev_close = prices.shift(1)
        if not self.highs.empty and not self.lows.empty:
            tr = (highs - lows).abs() \
                 .combine((highs - prev_close).abs(), np.maximum) \
                 .combine((lows  - prev_close).abs(), np.maximum)
        else:
            tr = prices.diff().abs() * np.sqrt(np.pi / 2)
        self.atr = tr.ewm(com=self.atr_period - 1, adjust=False).mean()

        # ── EMA family ───────────────────────────────────────────────────────
        self._ema_fast = prices.ewm(span=self.ema_fast, adjust=False).mean()
        self._ema_mid  = prices.ewm(span=self.ema_mid,  adjust=False).mean()
        self._ema_slow = prices.ewm(span=self.ema_slow, adjust=False).mean()

        # ── 52-week rolling high / low (252 trading days) ─────────────────
        # Uses prior-day close (apples-to-apples with trend gate close comparison)
        self._high_52w = prev_close.rolling(252, min_periods=200).max()
        # ── Dollar volume & 63-day median dVol ───────────────────────────────
        # Use raw self.volumes (not forward-filled) so suspended days with
        # zero/NaN volume are not inflated by ffill on prices.
        dvol = prices * self.volumes
        self._median_dvol = dvol.rolling(63, min_periods=21).median()

        # ── 63-day circuit-breaker count ──────────────────────────────────────
        # Fix 2: detect locked days on RAW highs/lows (self.highs, self.lows)
        # before forward-fill. A forward-filled high==low comparison carries a
        # single locked day into subsequent bars and inflates the rolling count.
        if not self.highs.empty and not self.lows.empty:
            is_locked = (self.highs == self.lows)   # raw, no ffill
            self._circuit_count = is_locked.rolling(63, min_periods=1).sum()
        else:
            self._circuit_count = pd.DataFrame(
                0.0, index=prices.index, columns=prices.columns
            )

        # ── 22-day prior return ──────────────────────────────────────────────
        self._prior_month_ret = prices.pct_change(22, fill_method=None)


        # ── Universe mask (pre-computed for benchmark & breadth) ─────────────
        # Fix 3: build _universe_mask_df from the SAME intermediate arrays
        # (_median_dvol, _circuit_count) that filter_universe() reads in the
        # event loop, so both paths produce identical eligibility on every bar.
        # Shift by 1 here to represent T-1 data (same as filter_universe()).
        dvol_med_full  = self._median_dvol.shift(1)
        dvol_rank_full = dvol_med_full.rank(axis=1, ascending=False, method='min')
        mask_dvol      = (dvol_rank_full <= self.universe_top_n) & (dvol_rank_full >= self.universe_min_n)
        mask_px        = prev_close >= self.min_price
        mask_circ      = self._circuit_count.shift(1) <= self.max_circuit_days
        prev_ret_full  = prev_close / prev_close.shift(22) - 1
        mask_ret       = prev_ret_full >= self.prior_month_min_ret
        self._universe_mask_df = (mask_dvol & mask_px & mask_circ & mask_ret).fillna(False)
        # Raw universe: price floor only — no liquidity, circuit, or momentum filter.
        # Used exclusively for regime signals (breadth + benchmark) so they act as
        # independent macro reads, not contaminated by the entry-eligibility logic.
        self._raw_universe_df  = mask_px.fillna(False)

        # ── Raw-universe benchmark (equal-weight, price-floor stocks only) ─────
        # Built from _raw_universe_df so the benchmark trend check (bench_ok) is
        # a genuine whole-market signal, decoupled from the entry universe size.
        # RS excess return uses this same benchmark for consistency.
        raw_univ_ret       = prices.pct_change(fill_method=None).where(self._raw_universe_df)
        bench_daily        = raw_univ_ret.mean(axis=1, skipna=True).fillna(0)
        self._bench_series = (1 + bench_daily).cumprod()

        # ── 6-month RS: stock return − universe-filtered benchmark return ─────
        self._stock_ret_6m = prices.pct_change(self.rs_lookback, fill_method=None)
        bench_ret_6m       = self._bench_series.pct_change(self.rs_lookback, fill_method=None)
        self._rs_excess    = self._stock_ret_6m.subtract(bench_ret_6m, axis=0)

        # ── 30-day momentum for candidate ranking ────────────────────────────
        self._mom_30d = prices.pct_change(self.momentum_rank_window, fill_method=None)

        # ── Benchmark SMA (for regime filter) — uses universe-filtered bench ──
        self._bench_sma50 = self._bench_series.rolling(
            self.benchmark_sma_period, min_periods=30
        ).mean()

        # ── Cache forward-filled price/open arrays for the event loop ────────
        self._prices_ff  = prices
        self._opens_ff   = self.opens.ffill() if not self.opens.empty else prev_close
        self._open_proxy = prev_close          # prev-close fallback
        self._highs_ff   = highs
        self._lows_ff    = lows

        # ── Numpy array caches for hot-path performance ───────────────────────
        # Pre-extracting .values once avoids repeated pandas indexing overhead
        # inside the per-stock, per-bar event loop. Integer column indices
        # allow O(1) numpy array slicing instead of pandas label lookups.
        self._highs_np      = highs.values                   # (n_bars, n_stocks)
        self._prices_np     = prices.values                  # (n_bars, n_stocks)
        self._ema_fast_np   = self._ema_fast.values          # (n_bars, n_stocks)
        self._ema_mid_np    = self._ema_mid.values           # (n_bars, n_stocks)
        self._ema_slow_np   = self._ema_slow.values          # (n_bars, n_stocks)
        self._high_52w_np   = self._high_52w.values         # (n_bars, n_stocks)
        self._rs_excess_np  = self._rs_excess.values        # (n_bars, n_stocks)
        # Stock → column index mapping for O(1) numpy column lookup
        self._stock_col_idx = {s: j for j, s in enumerate(prices.columns)}

        print("  Indicators ready.")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE MASK (daily)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, i, date):
        """
        Returns a boolean Series of eligible stocks for bar i.
        All conditions use T-1 data (shifted by 1 bar before this call).
        """
        # 1. Minimum price
        prev_close = self._prices_ff.iloc[i - 1]
        price_ok = prev_close >= self.min_price

        # 2. Top-N by median dVol
        dvol_today = self._median_dvol.iloc[i - 1]
        dvol_rank  = dvol_today.rank(ascending=False, method='min')
        dvol_max   = dvol_rank <= self.universe_top_n
        dvol_min   = dvol_rank >= self.universe_min_n
        dvol_ok    = dvol_max & dvol_min

        # 3. Circuit breaker
        circuit_ok = self._circuit_count.iloc[i - 1] <= self.max_circuit_days

        # 4. Prior 22d return
        ret22 = self._prior_month_ret.iloc[i - 1]
        ret_ok = ret22 >= self.prior_month_min_ret

        return price_ok & dvol_ok & circuit_ok & ret_ok

    # ──────────────────────────────────────────────────────────────────────────
    # REGIME FILTER (daily, market-wide)
    # ──────────────────────────────────────────────────────────────────────────

    def _compute_regime_flags(self):

        prices = self._prices_ff

        # ── Benchmark trend: rolling-window consecutive-days check (T-1) ─────
        # bench_series is also built from the raw universe in calculate_factors.
        # Block entries only when the benchmark was below SMA on ALL N of the
        # last N days; a single recovery day resets the block immediately.
        bench_below = (
            (self._bench_series < self._bench_sma50)
            .shift(1)
            .fillna(False)
            .infer_objects(copy=False)
            .astype(int)
        )
        rolling_sum = bench_below.rolling(
            self.benchmark_streak_max,
            min_periods=self.benchmark_streak_max,
        ).sum()
        bench_ok = (rolling_sum < self.benchmark_streak_max).fillna(True)
        bench_ok = bench_ok.reindex(prices.index).fillna(True)

        return bench_ok


    # ──────────────────────────────────────────────────────────────────────────
    # TREND GATE (per stock, using T-1 data)
    # ──────────────────────────────────────────────────────────────────────────

    def _trend_gate(self, i, universe_mask=None):
        """
        Returns a boolean Series of stocks that pass all 4 trend conditions.
        Uses row i-1 (T-1 data). Reads from pre-extracted numpy arrays
        to avoid pandas .iloc row extraction overhead in the hot path.
        """
        idx   = i - 1
        cols  = self._prices_ff.columns

        # Pull rows from numpy arrays — single O(n_stocks) slice, no pandas overhead
        close  = self._prices_np[idx]
        ema_f  = self._ema_fast_np[idx]
        ema_m  = self._ema_mid_np[idx]
        ema_s  = self._ema_slow_np[idx]
        hi52   = self._high_52w_np[idx]

        # 3.1 EMA alignment: EMA-50 > EMA-150 > EMA-200
        ema_align = (ema_f > ema_m) & (ema_m > ema_s)

        # 3.2 Price above EMA-200
        above_ema200 = close > ema_s

        # 3.3 EMA-200 slope: higher than 20 bars ago
        if idx >= self.ema_slope_window:
            ema_s_old = self._ema_slow_np[idx - self.ema_slope_window]
            ema_slope = ema_s > ema_s_old
        else:
            ema_slope = np.zeros(len(cols), dtype=bool)

        # 3.4 52-week high band: close >= 75% of 52w high
        hi_band = close >= (hi52 * self.high_band_pct)

        # 3.5 Relative strength: top 25% by RS excess return
        # Use pandas Series for RS to support universe_mask boolean indexing
        rs_today = pd.Series(self._rs_excess_np[idx], index=cols)
        if universe_mask is not None:
            rs_pool = rs_today[universe_mask & rs_today.notna()]
        else:
            rs_pool = rs_today[self._universe_mask_df.iloc[idx] & rs_today.notna()]
        if len(rs_pool) > 0:
            threshold = rs_pool.quantile(1.0 - self.rs_top_pct)
            rs_ok     = rs_today >= threshold
        else:
            rs_ok = pd.Series(False, index=cols)

        # Combine: all numpy arrays except rs_ok which stays as pandas Series
        combined_np = ema_align & above_ema200 & ema_slope & hi_band
        return pd.Series(combined_np, index=cols) & rs_ok

    # ──────────────────────────────────────────────────────────────────────────
    # HR SIGNAL: LOCAL PEAKS + CLUSTER + BREAKOUT
    # ──────────────────────────────────────────────────────────────────────────


    def _find_hr_signal(self, stock, i):
        """
        Evaluates the HR breakout signal for one stock at bar i (T-1 data).

        Step 1: Detect local peaks using vectorized numpy comparisons.
                Peak at bar k confirmed at k+wing — T-1 discipline preserved.
        Step 2: Find tightest cluster of ≥3 peaks (spread ≤ cluster_spread_pct).
        Step 3: Price breakout check (T-1 bar).

        Returns (signal: bool, cluster_top: float)
        """
        col_idx = self._stock_col_idx.get(stock, -1)
        if col_idx == -1:
            return False, np.nan

        wing     = self.peak_wing
        lookback = self.cluster_lookback

        # Slice the pre-extracted numpy array — O(1) integer indexing, no pandas
        start_idx  = max(0, i - lookback - wing)
        high_slice = self._highs_np[start_idx:i, col_idx]   # bars up to i-1 inclusive
        n          = len(high_slice)

        if n < 2 * wing + self.cluster_min_peaks:
            return False, np.nan

        # ── Step 1: vectorized peak detection ────────────────────────────────────
        # mid[k] = high_slice[wing + k] for k in 0 .. n-2*wing-1
        # A peak is confirmed at k+wing, so we restrict to k+wing <= n-1
        # i.e. k <= n-1-wing, which is already enforced by the slice bounds below.
        mid = high_slice[wing : n - wing]          # candidate peaks
        is_peak = np.ones(len(mid), dtype=bool)
        for j in range(1, wing + 1):
            is_peak &= mid > high_slice[wing - j : n - wing - j]   # left wing
            is_peak &= mid > high_slice[wing + j : n - wing + j]   # right wing
        peaks = mid[is_peak]

        if len(peaks) < self.cluster_min_peaks:
            return False, np.nan

        # ── Step 2: tightest cluster of ≥3 peaks ────────────────────────────────
        peaks_sorted     = np.sort(peaks)
        best_cluster_top = np.nan
        best_spread      = np.inf

        for a in range(len(peaks_sorted)):
            lo = peaks_sorted[a]
            if lo <= 0:
                continue
            for b in range(a + self.cluster_min_peaks - 1, len(peaks_sorted)):
                hi     = peaks_sorted[b]
                spread = (hi - lo) / lo
                if spread > self.cluster_spread_pct:
                    break   # sorted: further b only widens spread
                count = b - a + 1
                if count >= self.cluster_min_peaks and spread < best_spread:
                    best_spread      = spread
                    best_cluster_top = hi

        if np.isnan(best_cluster_top):
            return False, np.nan

        # ── Step 3: price breakout (T-1 bar, numpy lookup) ───────────────────────
        prev_close = self._prices_np[i - 1, col_idx]
        if np.isnan(prev_close) or prev_close <= 0:
            return False, np.nan

        price_breakout = prev_close > best_cluster_top * (1.0 + self.breakout_buffer)
        return price_breakout, best_cluster_top
    # ──────────────────────────────────────────────────────────────────────────
    # DYNAMIC ATR MULTIPLIER
    # ──────────────────────────────────────────────────────────────────────────

    def _dynamic_atr_multiplier(self, atr_pct):
        """
        Map a stock's entry-time ATR% (ATR / entry_price) to a chandelier
        multiplier, interpolating linearly between atr_multiplier_max
        (calm names, low ATR%) and atr_multiplier_min (volatile/gappy
        names, high ATR%). Fixed once at entry and stored on the holding.
        """
        if pd.isna(atr_pct) or atr_pct <= self.atr_pct_calm:
            return self.atr_multiplier_max
        if atr_pct >= self.atr_pct_volatile:
            return self.atr_multiplier_min
        frac = (atr_pct - self.atr_pct_calm) / (self.atr_pct_volatile - self.atr_pct_calm)
        return self.atr_multiplier_max - frac * (self.atr_multiplier_max - self.atr_multiplier_min)

    # ──────────────────────────────────────────────────────────────────────────
    # STOP EVALUATION (per bar, per position)
    # ──────────────────────────────────────────────────────────────────────────

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan):
        """
        Three-layer stop for one stock on one bar.
        atr_stop ratchets UP only (chandelier trailing stop).

        Layers:
          L1 Chandelier : peak_close − atr_multiplier × ATR14 (ratchets up,
                          clamped to [chandelier_clamp_min, chandelier_clamp_max]
                          of peak; atr_multiplier is fixed per-position at
                          entry based on entry-time ATR%)
          L2 Entry floor: entry_price × (1 − 10%)
          L3 Peak floor : peak_close  × (1 − 10%)

        During min_hold_days (first 20 bars), only L2 (entry floor) is active.
        This gives the trade room to consolidate after entry before the trailing
        chandelier begins ratcheting — aligned with IC decay showing edge builds from 30d.

        Trigger : today's low < effective_stop
        Fill    : min(open, effective_stop) — handles both gap-down and
                  intraday breach with a single rule, no slippage parameter.

        Returns: (should_exit, fill_price, stop_level, updated_holding)
        """
        if pd.isna(curr_close) or curr_close <= 0:
            return False, np.nan, holding.get('atr_stop', np.nan), holding

        entry_price = holding['entry_price']
        peak_price  = holding['peak_price']
        atr_stop    = holding['atr_stop']
        days_held   = holding.get('days_held', 999)

        # Force exit on anomalous loss (>60% from entry) — data anomaly guard
        if not pd.isna(entry_price) and entry_price > 0:
            if (curr_close / entry_price) - 1 < -0.60:
                synthetic_stop = entry_price * 0.40
                _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
                fill  = min(_open, synthetic_stop)
                return True, float(fill), float(synthetic_stop), holding

        # Update peak using prior close (conservative; anchors to prices actually
        # sustained at close rather than intraday spikes that were never held)
        new_peak = max(peak_price, curr_close)
        holding  = {**holding, 'peak_price': new_peak}

        # ── Min-hold-days: only entry floor active during grace period ────────
        entry_hard = entry_price * (1.0 - self.hard_stop_from_entry) \
                     if not pd.isna(entry_price) else -np.inf

        if days_held < self.min_hold_days:
            effective_stop = entry_hard
            holding = {**holding, 'atr_stop': effective_stop}
            check_price = curr_low if (not pd.isna(curr_low) and curr_low > 0) else curr_close
            if check_price > effective_stop:
                return False, np.nan, effective_stop, holding
            _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
            fill  = min(_open, effective_stop)
            return True, float(fill), float(effective_stop), holding

        # ── Full three-layer stop ─────────────────────────────────────────────
        # L1: chandelier (ratchets up only) — multiplier fixed at entry based
        # on entry-time ATR%, distance clamped to [clamp_min, clamp_max] of peak
        if not pd.isna(curr_atr) and curr_atr > 0:
            mult = holding.get('atr_multiplier', self.atr_multiplier_max)
            chandelier = float(np.clip(
                new_peak - mult * curr_atr,
                new_peak * (1.0 - self.chandelier_clamp_max),
                new_peak * (1.0 - self.chandelier_clamp_min),
            ))
            atr_stop   = max(atr_stop, chandelier)   # never falls

        # L2 + L3
        peak_hard  = new_peak * (1.0 - self.hard_stop_from_peak)
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding = {**holding, 'atr_stop': effective_stop, 'peak_price': new_peak}

        # Trigger check via intraday low
        check_price = curr_low if (not pd.isna(curr_low) and curr_low > 0) else curr_close
        if check_price > effective_stop:
            return False, np.nan, effective_stop, holding

        _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
        fill  = min(_open, effective_stop)
        return True, float(fill), float(effective_stop), holding

    # ──────────────────────────────────────────────────────────────────────────
    # TRADE RECORD
    # ──────────────────────────────────────────────────────────────────────────

    def _record_closed_trade(self, ticker, holding, exit_date,
                              exit_price, fill_price, exit_reason,
                              stop_price_at_exit):
        """Append one completed trade to self.position_metadata."""
        entry_price  = holding['entry_price']
        entry_date   = holding['entry_date']
        peak_price   = holding['peak_price']
        stop_pct     = holding.get('stop_pct',     np.nan)
        atr_at_entry = holding.get('atr_at_entry', np.nan)
        atr_mult     = holding.get('atr_multiplier', np.nan)
        weight          = holding.get('weight',          0.0)
        intended_weight = holding.get('intended_weight', weight)   # pre-normalisation weight
        min_price    = holding.get('min_price',     entry_price)
        max_price    = holding.get('max_price',     entry_price)

        _stop_reasons = {'STOP_HIT', 'TIME_STOP'}
        actual_fill   = fill_price if exit_reason in _stop_reasons else exit_price

        mae_pct = ((min_price / entry_price) - 1) * 100 \
                  if (entry_price and entry_price > 0) else np.nan
        mfe_pct = ((max_price / entry_price) - 1) * 100 \
                  if (entry_price and entry_price > 0) else np.nan

        self.position_metadata.append({
            'Ticker'             : ticker,
            'Entry_Date'         : entry_date,
            'Entry_Price'        : round(entry_price,        4) if pd.notna(entry_price)        else np.nan,
            'Exit_Date'          : exit_date,
            'Exit_Price'         : round(actual_fill,        4) if pd.notna(actual_fill)        else np.nan,
            'Close_At_Exit'      : round(exit_price,         4) if pd.notna(exit_price)         else np.nan,
            'Peak_Price'         : round(peak_price,         4) if pd.notna(peak_price)         else np.nan,
            'Stop_Price_At_Exit' : round(stop_price_at_exit, 4) if pd.notna(stop_price_at_exit) else np.nan,
            'Stop_Pct'           : round(stop_pct * 100,     2) if pd.notna(stop_pct)           else np.nan,
            'ATR_At_Entry'       : round(atr_at_entry,       4) if pd.notna(atr_at_entry)       else np.nan,
            'ATR_Multiplier'     : round(atr_mult,           3) if pd.notna(atr_mult)           else np.nan,
            'Exit_Reason'        : exit_reason,
            'Weight'             : round(weight,              6),
            'Intended_Weight'    : round(intended_weight,     6),
            'MAE_Pct'            : round(mae_pct, 2)             if pd.notna(mae_pct)           else np.nan,
            'MFE_Pct'            : round(mfe_pct, 2)             if pd.notna(mfe_pct)           else np.nan,
        })

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self):
        """
        Build the daily positions DataFrame for all bars.

        Loops over every bar (same as the backtest entry loop — STEP B),
        applying regime filter, filter_universe(), _trend_gate(), and
        _find_hr_signal() using only T-1 data (no lookahead).

        For each bar, stocks that pass all filters and fire the HR signal
        are assigned self.position_ceil weight. Result is stored in
        self.positions (shape: dates × stocks) and returned.

        Called by the live system and the runner after calculate_factors().
        """
        if self.atr is None:
            raise ValueError("Call calculate_factors() first.")

        print(f"Generating Positions  "
              f"max_positions={self.max_positions}  weight={self.position_ceil:.0%}  "
              f"universe_top_n={self.universe_top_n}  warmup={self.warmup_days}d")

        prices_ff  = self._prices_ff
        opens_ff   = self._opens_ff
        open_proxy = self._open_proxy
        highs_ff   = self._highs_ff
        lows_ff    = self._lows_ff
        all_stocks = list(prices_ff.columns)
        dates      = prices_ff.index
        n_dates    = len(dates)

        # Circuit-breaker mask
        if not self.highs.empty and not self.lows.empty:
            is_circuit = (highs_ff == lows_ff)
        else:
            is_circuit = pd.DataFrame(False, index=dates, columns=prices_ff.columns)

        # Regime flags — pre-computed once for all bars (no lookahead, uses .shift(1))
        bench_ok = self._compute_regime_flags()

        position_list          = []
        active_holdings        = set()   # tickers currently held
        stop_cooldown_tickers  = {}      # ticker → date of stop hit (calendar-day comparison)

        for i, date in enumerate(dates):

            if i == 0:
                position_list.append(pd.Series(0.0, index=all_stocks, name=date))
                continue

            # Carry forward weights of currently held stocks
            curr_weights = pd.Series(
                {s: self.position_ceil for s in active_holdings},
                dtype=float
            ).reindex(all_stocks, fill_value=0.0)
            curr_weights.name = date

            # Skip new entries during warmup
            if i < self.warmup_days:
                position_list.append(curr_weights)
                continue

            # Regime gate
            regime_pass = bool(bench_ok.iloc[i])

            if regime_pass and len(active_holdings) < self.max_positions:
                universe_mask = self.filter_universe(i, date)
                trend_mask    = self._trend_gate(i)
                eligible      = universe_mask & trend_mask

                candidates = []
                for stock in all_stocks:
                    if not eligible.get(stock, False):
                        continue
                    if stock in active_holdings:
                        continue

                    # Stop cooldown
                    if stock in stop_cooldown_tickers:
                        if (date - stop_cooldown_tickers[stock]).days < self.stop_cooldown_days:
                            continue
                        else:
                            del stop_cooldown_tickers[stock]

                    # Circuit day
                    if stock in is_circuit.columns and bool(is_circuit.at[date, stock]):
                        continue

                    # HR breakout signal
                    signal, _ = self._find_hr_signal(stock, i)
                    if not signal:
                        continue

                    # Gap cancel
                    today_open     = float(opens_ff.at[date, stock]) if stock in opens_ff.columns else np.nan
                    prev_close_val = float(open_proxy.at[date, stock]) if stock in open_proxy.columns else np.nan
                    if not pd.isna(today_open) and not pd.isna(prev_close_val) and prev_close_val > 0:
                        prev_atr = float(self.atr.iloc[i - 1][stock]) if stock in self.atr.columns else np.nan
                        if not pd.isna(prev_atr) and prev_atr > 0:
                            if abs(today_open - prev_close_val) > prev_atr:
                                continue

                    # 30-day momentum for ranking
                    mom = float(self._mom_30d.iloc[i - 1][stock]) if stock in self._mom_30d.columns else -np.inf
                    if pd.isna(mom):
                        mom = -np.inf
                    candidates.append((stock, mom))

                # Rank by momentum, fill available slots
                candidates.sort(key=lambda x: x[1], reverse=True)
                slots = self.max_positions - len(active_holdings)
                for stock, _ in candidates[:slots]:
                    active_holdings.add(stock)

                    # Risk-based sizing — mirrors backtest logic exactly
                    entry_px   = float(opens_ff.at[date, stock])                                  if stock in opens_ff.columns else np.nan
                    if pd.isna(entry_px) or entry_px <= 0:
                        entry_px = float(open_proxy.at[date, stock])                                    if stock in open_proxy.columns else np.nan
                    curr_atr_e = float(self.atr.iloc[i - 1][stock])                                  if stock in self.atr.columns else np.nan
                    if pd.isna(curr_atr_e) or curr_atr_e <= 0:
                        curr_atr_e = entry_px * 0.02 if pd.notna(entry_px) and entry_px > 0 else np.nan

                    if pd.notna(entry_px) and entry_px > 0 and pd.notna(curr_atr_e):
                        atr_pct_e  = curr_atr_e / entry_px
                        mult_e     = self._dynamic_atr_multiplier(atr_pct_e)
                        init_stop  = max(
                            entry_px * (1.0 - self.hard_stop_from_entry),
                            entry_px - mult_e * curr_atr_e,
                        )
                        stop_pct_e = (entry_px - init_stop) / entry_px
                        if stop_pct_e > 0:
                            w = float(np.clip(
                                self.risk_pct_per_trade / stop_pct_e,
                                self.position_floor,
                                self.position_ceil,
                            ))
                        else:
                            w = self.position_floor
                    else:
                        w = self.position_floor

                    curr_weights[stock] = w

            # Normalise if total > 100%
            total_w = curr_weights.sum()
            if total_w > 1.0:
                curr_weights = curr_weights / total_w

            position_list.append(curr_weights)

        self.positions = pd.DataFrame(position_list, index=dates).fillna(0.0)
        print(f"Positions shape: {self.positions.shape}  "
              f"Avg daily holdings: {(self.positions > 0).sum(axis=1).mean():.1f}")
        return self.positions


    # ──────────────────────────────────────────────────────────────────────────
    # LIVE EXIT SIGNAL EVALUATOR
    # ──────────────────────────────────────────────────────────────────────────
 
    def get_exit_signals(self,
                         portfolio:      dict,
                         live_data:      dict,
                         benchmark_vol:  float = None,
                         today                 = None) -> dict:
        """
        Evaluate all exit rules for currently held positions on one live bar.
 
        Implements every exit condition used in the backtest exactly:
          • Anomaly guard    : loss > 60% from entry_price → immediate exit.
          • Circuit day      : high == low (price locked) → defer, no fill.
          • Min-hold grace   : first min_hold_days bars (20) → only entry floor active.
                             Chandelier does not activate until this period expires.
          • L1 Chandelier    : peak − atr_multiplier × ATR, clamped to
                               [chandelier_clamp_min, chandelier_clamp_max] of
                               peak (ratchets up only). atr_multiplier is the
                               per-position value fixed at entry from ATR%.
          • L2 Entry floor   : entry_price × (1 − hard_stop_from_entry).
          • L3 Peak floor    : peak_price  × (1 − hard_stop_from_peak).
          • Trigger          : low < effective_stop → fill at min(open, stop).
          • Time stop        : after time_stop_min_days, exit if profit < threshold.
 
        benchmark_vol is accepted for interface compatibility but is not used —
        the HR strategy has no crash-guard or vol-regime exit rule.
 
        Parameters
        ----------
        portfolio : dict
            ticker → {
                'entry_price' : float,   # price at which position was entered
                'entry_date'  : date | str,
                'peak_price'  : float,   # highest close seen since entry
                'atr_stop'    : float,   # current chandelier stop (persist and
                                         # pass back each bar — ratchets up only)
                'weight'      : float,   # informational only
                'atr_multiplier': float, # per-position chandelier multiplier
                                         # fixed at entry from ATR% (defaults
                                         # to atr_multiplier_max if absent)
            }
        live_data : dict
            ticker → {
                'close' : float,         # required (T-1 settled close)
                'high'  : float,         # optional; defaults to close
                'low'   : float,         # optional; defaults to close
                'open'  : float,         # optional; defaults to close
                'atr'   : float,         # optional; defaults to close × 0.02
            }
        benchmark_vol : float, optional
            Not used by this strategy. Accepted for interface compatibility.
        today : date-like, optional
            Today's date for calendar-day calculations.
            Defaults to datetime.date.today().
 
        Returns
        -------
        dict with four keys:
            'exits' : dict
                ticker → {
                    'reason'      : str,   # 'STOP_HIT' | 'TIME_STOP' | 'ANOMALY'
                    'fill_price'  : float, # min(open, effective_stop)
                    'stop_level'  : float, # stop level that was breached
                }
            'holds' : dict
                ticker → {
                    'updated_peak'     : float, # new peak after this bar's close
                    'updated_atr_stop' : float, # ratcheted chandelier — persist this!
                    'stop_level'       : float, # current effective stop level
                }
            'crash_guard_fired' : bool   # always False — HR has no crash guard
            'high_vol'          : bool   # always False — HR has no vol-regime rule
        """
        import datetime as _dt
 
        if today is None:
            today = _dt.date.today()
        elif not isinstance(today, _dt.date):
            today = pd.Timestamp(today).date()
 
        exits: dict = {}
        holds: dict = {}
 
        for ticker, pos in portfolio.items():
            bar = live_data.get(ticker, {})
 
            # ── Pull OHLC — fall back to close for any missing field ──────────
            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
                # No usable price — skip; holding state unchanged
                continue
 
            _high = float(bar.get('high', _close))
            _low  = float(bar.get('low',  _close))
            _open = float(bar.get('open', _close))
            if pd.isna(_high) or _high <= 0: _high = _close
            if pd.isna(_low)  or _low  <= 0: _low  = _close
            if pd.isna(_open) or _open <= 0: _open = _close
 
            # ATR fallback: 2% of close (matches backtest default)
            _atr = float(bar.get('atr', np.nan))
            if pd.isna(_atr) or _atr <= 0:
                _atr = _close * 0.02
 
            # ── Circuit day guard: high == low → price locked, no fills ──────
            # Only apply when real intraday H/L were explicitly provided.
            # When only 'close' is passed, _high and _low both equal _close,
            # so the guard would silently suppress every stop — skip it.
            _has_real_hl = ('high' in bar) and ('low' in bar)
            if _has_real_hl and _high == _low:
                _atr_stop = float(pos.get('atr_stop', np.nan))
                holds[ticker] = {
                    'updated_peak'     : float(pos.get('peak_price', _close)),
                    'updated_atr_stop' : _atr_stop,
                    'stop_level'       : _atr_stop,
                }
                continue
 
            # ── Unpack position state ─────────────────────────────────────────
            entry_price = float(pos.get('entry_price', np.nan))
            peak_price  = float(pos.get('peak_price',  _close))
            atr_stop    = float(pos.get('atr_stop',    0.0))
            if pd.isna(atr_stop) or atr_stop <= 0:
                atr_stop = 0.0
 
            # ── Calendar days held ────────────────────────────────────────────
            entry_date_raw = pos.get('entry_date', '')
            try:
                _entry_dt  = pd.Timestamp(str(entry_date_raw)[:10]).date()
                _days_held = (today - _entry_dt).days
            except Exception:
                _days_held = 999   # unknown → treat as past every grace period
 
            # ── Anomaly guard: >60% loss from entry → force exit ──────────────
            if not pd.isna(entry_price) and entry_price > 0:
                if (_close / entry_price) - 1.0 < -0.60:
                    synthetic_stop = entry_price * 0.40
                    fill = min(_open, synthetic_stop)
                    exits[ticker] = {
                        'reason'     : 'ANOMALY',
                        'fill_price' : float(fill),
                        'stop_level' : float(synthetic_stop),
                    }
                    continue
 
            # ── Update peak (close only — conservative, matches backtest) ─────
            new_peak = max(peak_price, _close)
 
            # ── Entry floor (always computed, used in both grace and full stop) ─
            entry_hard = (entry_price * (1.0 - self.hard_stop_from_entry)
                          if not pd.isna(entry_price) else -np.inf)
 
            # ── Time stop: profit check against settled close ─────────────────
            # Evaluated before the chandelier so a stale position that hasn't
            # reached the stop level but has also not delivered enough profit
            # is still exited — mirrors backtest order: time stop checked first.
            if _days_held >= self.time_stop_min_days:
                open_profit = ((_close / entry_price) - 1.0
                               if (not pd.isna(entry_price) and entry_price > 0)
                               else 0.0)
                if open_profit < self.time_stop_min_profit:
                    exits[ticker] = {
                        'reason'     : 'TIME_STOP',
                        'fill_price' : float(_open),
                        'stop_level' : float(atr_stop),
                    }
                    continue
 
            # ── Min-hold grace: only entry floor active ───────────────────────
            if _days_held < self.min_hold_days:
                effective_stop     = entry_hard
                updated_atr_stop   = effective_stop
                check_price        = _low
                if check_price > effective_stop:
                    holds[ticker] = {
                        'updated_peak'     : float(new_peak),
                        'updated_atr_stop' : float(updated_atr_stop),
                        'stop_level'       : float(effective_stop),
                    }
                else:
                    fill = min(_open, effective_stop)
                    exits[ticker] = {
                        'reason'     : 'STOP_HIT',
                        'fill_price' : float(fill),
                        'stop_level' : float(effective_stop),
                    }
                continue
 
            # ── Full three-layer stop ─────────────────────────────────────────
            # L1: chandelier — ratchets up, never falls. Multiplier fixed at
            # entry (passed via portfolio[ticker]['atr_multiplier']) based on
            # entry-time ATR%; distance clamped to [clamp_min, clamp_max] of peak.
            if not pd.isna(_atr) and _atr > 0:
                mult = pos.get('atr_multiplier', self.atr_multiplier_max)
                chandelier = float(np.clip(
                    new_peak - mult * _atr,
                    new_peak * (1.0 - self.chandelier_clamp_max),
                    new_peak * (1.0 - self.chandelier_clamp_min),
                ))
                atr_stop   = max(atr_stop, chandelier)
 
            # L2 + L3
            peak_hard      = new_peak * (1.0 - self.hard_stop_from_peak)
            effective_stop = max(atr_stop, entry_hard, peak_hard)
 
            # Trigger: intraday low breaches the stop
            if _low > effective_stop:
                holds[ticker] = {
                    'updated_peak'     : float(new_peak),
                    'updated_atr_stop' : float(atr_stop),
                    'stop_level'       : float(effective_stop),
                }
            else:
                fill = min(_open, effective_stop)
                exits[ticker] = {
                    'reason'     : 'STOP_HIT',
                    'fill_price' : float(fill),
                    'stop_level' : float(effective_stop),
                }
 
        return {
            'exits'             : exits,
            'holds'             : holds,
            'crash_guard_fired' : False,   # HR strategy has no crash guard
            'high_vol'          : False,   # HR strategy has no vol-regime rule
        }
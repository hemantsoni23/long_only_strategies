"""
vcp_breakout.py
===============
Minervini SEPA / VCP Breakout Strategy
Indian Equities | Flat Allocation | No Pyramid

Universe : top-N dVol (63d avg) | min price ₹10 | circuit ≤5/63d
           corporate-action filter (single-day drop >40% or gain >300%)
Regime   : benchmark not below SMA-50 for 5+ consecutive days
           (raw universe — independent macro read)
Entry    : All 7 Trend Template (Stage 2) criteria + all 4 VCP criteria
           Ranked by 1-year RS percentile; filled at T+1 open
Sizing   : risk-based | risk 1%/trade via ATR stop distance | clamp 2%-20%
           liquidity cap: 10% of stock 63d avg dVol | tracked on running equity
Exits    : Hard stop −8% | Trailing stop (activates at +10%, trails 7% from peak)
           Stale trade (≥60 days AND <5% return) | End of data
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

class VCPBreakoutStrategy:
    """
    Event-driven Minervini SEPA / VCP Breakout strategy.

    Per-position state lives in active_holdings[ticker]:
        entry_date, entry_price, hard_stop, trail_stop, trail_active,
        peak_price, weight, min_price, max_price, obs
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df               = None,
        lows_df                = None,
        opens_df               = None,
        # Universe
        universe_top_n         = 1000,      # top-N stocks by 63d avg dollar volume
        universe_min_n         = 1,         # bottom rank bound (set >1 to slice a band)
        min_price              = 10.0,      # minimum prior-day close (₹)
        max_circuit_days       = 5,         # max locked days in 63d window
        ca_drop_thresh         = 0.40,      # single-day drop >40% → corporate action
        ca_gain_thresh         = 3.00,      # single-day gain >300% → corporate action
        # Regime
        bench_sma_period       = 50,        # benchmark SMA period
        bench_consec_days      = 5,         # block if bench below SMA for N+ consecutive days
        # Trend Template
        sma_fast               = 50,        # TT4/5: fast SMA
        sma_mid                = 150,       # TT1/2/4: mid SMA
        sma_slow               = 200,       # TT1/2/3/4: slow SMA
        sma_slope_lookback     = 20,        # TT3: SMA-200 must be above N days ago
        high_52w_period        = 252,       # TT7/VCP5: 52-week high lookback
        within_52w_high_pct    = 0.25,      # TT7: price within 25% of 52w high
        rs_period              = 252,       # TT8: 1-year RS lookback
        rs_min_percentile      = 70,        # TT8: >= 70th percentile rank
        # VCP Signal
        vcp_base_window        = 15,        # VCP1/2: base lookback days
        vcp_base_tight_pct     = 0.15,      # VCP1: max base range (hi-lo)/hi <= 15%
        vcp_vol_contract_pct   = 0.80,      # VCP2: base vol <= 80% of prior 30d avg
        vcp_vol_base_window    = 30,        # VCP2: prior volume average window
        vcp_breakout_window    = 20,        # VCP3: close > highest close of prior N days
        vcp_near_high_pct      = 0.10,      # VCP5: within 10% of 52w high
        # Entry execution
        max_positions          = 10,        # max concurrent open positions
        entry_gap_cancel_pct   = 0.03,      # skip entry if open gaps >3% above prior close
        # Position sizing (risk-based)
        risk_pct_per_trade    = 0.01,       # portfolio fraction risked per trade
        weight_min            = 0.02,       # position weight floor
        weight_max            = 0.20,       # position weight ceiling
        liquidity_cap_pct      = 0.10,      # cap at 10% of stock's 63d avg dVol
        # Exits
        hard_stop_pct          = 0.08,      # hard stop = entry × (1 − 8%)
        trail_activate_pct     = 0.10,      # trailing stop activates at +10% gain
        trail_pct              = 0.07,      # trail = peak × (1 − 7%)
        trail_floor_pct        = 0.001,     # trail >= entry × (1 + 0.1%) once active
        # ATR-based trail — same logic as HR chandelier (fixed at entry)
        trail_atr_mult_max     = 3.0,       # multiplier for calm stocks (low ATR%)
        trail_atr_mult_min     = 1.5,       # multiplier for volatile stocks (high ATR%)
        trail_atr_pct_calm     = 0.020,     # ATR/price <= this → full trail_atr_mult_max
        trail_atr_pct_volatile = 0.045,     # ATR/price >= this → full trail_atr_mult_min
        min_hold_days          = 5,         # only hard stop active for first N days
        stale_days             = 20,        # stale: held >= N calendar days
        stale_ret_pct          = 0.0,      # stale: return < 5%
        lockout_days           = 30,        # re-entry lockout after stop exit (calendar days)
        # Warmup
        warmup_days            = 252,       # trading days before first trade allowed
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
        self.ca_drop_thresh       = ca_drop_thresh
        self.ca_gain_thresh       = ca_gain_thresh

        # Regime
        self.bench_sma_period     = bench_sma_period
        self.bench_consec_days    = bench_consec_days

        # Trend Template
        self.sma_fast             = sma_fast
        self.sma_mid              = sma_mid
        self.sma_slow             = sma_slow
        self.sma_slope_lookback   = sma_slope_lookback
        self.high_52w_period      = high_52w_period
        self.within_52w_high_pct  = within_52w_high_pct
        self.rs_period            = rs_period
        self.rs_min_percentile    = rs_min_percentile

        # VCP
        self.vcp_base_window      = vcp_base_window
        self.vcp_base_tight_pct   = vcp_base_tight_pct
        self.vcp_vol_contract_pct = vcp_vol_contract_pct
        self.vcp_vol_base_window  = vcp_vol_base_window
        self.vcp_breakout_window  = vcp_breakout_window
        self.vcp_near_high_pct    = vcp_near_high_pct

        # Execution
        self.max_positions        = max_positions
        self.entry_gap_cancel_pct = entry_gap_cancel_pct
        self.risk_pct_per_trade   = risk_pct_per_trade
        self.weight_min           = weight_min
        self.weight_max           = weight_max
        self.liquidity_cap_pct    = liquidity_cap_pct

        # Exits
        self.hard_stop_pct        = hard_stop_pct
        self.trail_activate_pct   = trail_activate_pct
        self.trail_pct            = trail_pct
        self.trail_floor_pct      = trail_floor_pct
        self.trail_atr_mult_max     = trail_atr_mult_max
        self.trail_atr_mult_min     = trail_atr_mult_min
        self.trail_atr_pct_calm     = trail_atr_pct_calm
        self.trail_atr_pct_volatile = trail_atr_pct_volatile
        self.min_hold_days        = min_hold_days
        self.stale_days           = stale_days
        self.stale_ret_pct        = stale_ret_pct
        self.lockout_days         = lockout_days
        self.warmup_days          = warmup_days

        # State
        self.results           = None
        self.position_metadata = []

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty

        print(
            f"VCP Breakout Strategy initialised\n"
            f"  Universe  : rank {universe_min_n}–{universe_top_n} by dVol"
            f" | min_price ₹{min_price} | circuit ≤{max_circuit_days}/63d"
            f" | CA filter drop>{ca_drop_thresh*100:.0f}% gain>{ca_gain_thresh*100:.0f}%\n"
            f"  Regime    : bench SMA-{bench_sma_period} streak<{bench_consec_days}d\n"
            f"  TT        : SMA {sma_fast}/{sma_mid}/{sma_slow} | slope-{sma_slope_lookback}d"
            f" | 52w high band | RS≥{rs_min_percentile}th pct\n"
            f"  VCP       : base {vcp_base_window}d ≤{vcp_base_tight_pct*100:.0f}%"
            f" | vol contract ≤{vcp_vol_contract_pct*100:.0f}%"
            f" | breakout>{vcp_breakout_window}d high"
            f" | within {vcp_near_high_pct*100:.0f}% of 52w high\n"
            f"  Exits     : hard stop −{hard_stop_pct*100:.0f}%"
            f" | trail (activate +{trail_activate_pct*100:.0f}%,"
            f" ATR-based [{trail_atr_mult_min}×-{trail_atr_mult_max}×]ATR"
            f" (calm≤{trail_atr_pct_calm*100:.1f}% vol≥{trail_atr_pct_volatile*100:.1f}%))"
            f" | stale {stale_days}d/<{stale_ret_pct*100:.0f}%\n"
            f"  Max pos   : {max_positions} × risk {risk_pct_per_trade*100:.1f}%/trade"
            f" (clamp {weight_min*100:.0f}-{weight_max*100:.0f}%)"
            f" | liq cap {liquidity_cap_pct*100:.0f}% dVol"
            f" | OHLCV H={'YES' if has_h else 'NO'}"
            f" L={'YES' if has_l else 'NO'}"
            f" O={'YES' if has_o else 'FALLBACK-close'}"
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
        highs  = self.highs if not self.highs.empty else prices.copy()
        lows   = self.lows  if not self.lows.empty  else prices.copy()

        prev_close = prices.shift(1)   # T-1 closes — base for all indicators

        # ── Corporate action mask ─────────────────────────────────────────────
        # Flag bars with single-day drop >40% or gain >300%, plus the bar after.
        # These represent splits, bonuses, demergers — data artefacts, not trades.
        daily_ret     = prices.pct_change(fill_method=None)
        ca_flag       = (daily_ret < -self.ca_drop_thresh) | (daily_ret > self.ca_gain_thresh)
        self._ca_mask = (ca_flag | ca_flag.shift(1).fillna(False)).fillna(False)

        # ── Dollar volume (63-day rolling mean) ───────────────────────────────
        dvol               = prices * self.volumes
        self._dvol_avg63   = dvol.rolling(63, min_periods=21).mean()

        # ── Circuit breaker count (63-day rolling) ────────────────────────────
        # Uses raw H/L before ffill so suspended days aren't inflated by carry.
        if not self.highs.empty and not self.lows.empty:
            is_locked           = (self.highs == self.lows)
            self._circuit_count = is_locked.rolling(63, min_periods=1).sum()
        else:
            self._circuit_count = pd.DataFrame(
                0.0, index=prices.index, columns=prices.columns
            )

        # ── Universe mask (precomputed — used for regime benchmark) ──────────
        # Raw universe: price floor only, no liquidity/circuit/momentum filter.
        # Keeps regime signals independent of the entry-eligibility logic.
        mask_px              = prev_close >= self.min_price
        self._raw_universe_df = mask_px.fillna(False)

        # Full entry universe mask (for filter_universe() consistency check)
        dvol_med_shifted = self._dvol_avg63.shift(1)
        dvol_rank_full   = dvol_med_shifted.rank(axis=1, ascending=False, method='min')
        mask_dvol        = (dvol_rank_full <= self.universe_top_n) & \
                           (dvol_rank_full >= self.universe_min_n)
        mask_circ        = self._circuit_count.shift(1) <= self.max_circuit_days
        mask_ca          = ~self._ca_mask.shift(1).fillna(False)
        self._universe_mask_df = (mask_dvol & mask_px & mask_circ & mask_ca).fillna(False)
        self._raw_universe_df = (mask_px).fillna(False)

        # ── Raw-universe benchmark (price-floor stocks only) ──────────────────
        # Built from _raw_universe_df so regime is decoupled from universe_top_n.
        raw_univ_ret       = prices.pct_change(fill_method=None).where(self._raw_universe_df)
        bench_daily        = raw_univ_ret.mean(axis=1, skipna=True).fillna(0)
        self._bench_series = (1 + bench_daily).cumprod()
        self._bench_sma    = self._bench_series.rolling(
            self.bench_sma_period, min_periods=30
        ).mean()

        # ── Trend Template SMAs (T-1 shifted) ────────────────────────────────
        self._sma_fast     = prev_close.rolling(self.sma_fast,  min_periods=40).mean()
        self._sma_mid      = prev_close.rolling(self.sma_mid,   min_periods=100).mean()
        self._sma_slow     = prev_close.rolling(self.sma_slow,  min_periods=150).mean()
        self._sma_slow_lag = self._sma_slow.shift(self.sma_slope_lookback)  # TT3

        # ── 52-week high (T-1 shifted H) ──────────────────────────────────────
        hp             = highs.shift(1)
        lp             = lows.shift(1)
        self._high_52w = hp.rolling(self.high_52w_period, min_periods=200).max()

        # ── 1-year relative strength return (TT8 / candidate ranking) ────────
        self._ret_1y = prices.pct_change(self.rs_period, fill_method=None)

        # ── VCP indicators ────────────────────────────────────────────────────

        # VCP1: 15-day base range = (15d high − 15d low) / 15d high
        # Uses T-1 shifted H/L so event loop reading row i-1 is T-1 safe.
        base_high = hp.rolling(self.vcp_base_window,
                               min_periods=self.vcp_base_window // 2).max()
        base_low  = lp.rolling(self.vcp_base_window,
                                min_periods=self.vcp_base_window // 2).min()
        self._vcp_base_range = (base_high - base_low) / base_high.replace(0, np.nan)

        # VCP2: volume contraction — 15d base avg vs prior 30d avg (non-overlapping)
        # Volume shifted to T-1 before rolling; prior window starts after the base.
        vp = self.volumes.shift(1)
        vol_base_avg        = vp.rolling(self.vcp_base_window,
                                         min_periods=self.vcp_base_window // 2).mean()
        vol_prior_avg       = vp.shift(self.vcp_base_window).rolling(
                                self.vcp_vol_base_window,
                                min_periods=self.vcp_vol_base_window // 2).mean()
        self._vcp_vol_ratio = vol_base_avg / vol_prior_avg.replace(0, np.nan)

        # VCP3: T-1 close > highest close of prior vcp_breakout_window days
        # Double shift: prev_close already at T-1; shift(1) again gives T-2..T-N.
        self._vcp_high_n = prev_close.shift(1).rolling(
            self.vcp_breakout_window,
            min_periods=self.vcp_breakout_window // 2
        ).max()

        # ── ATR-14 (Wilder EWM) — observational enrichment at entry ──────────
        if not self.highs.empty and not self.lows.empty:
            tr = (highs - lows).abs() \
                 .combine((highs - prev_close).abs(), np.maximum) \
                 .combine((lows  - prev_close).abs(), np.maximum)
        else:
            tr = prices.diff().abs() * np.sqrt(np.pi / 2)
        self._atr14 = tr.ewm(com=13, adjust=False).mean()

        # ── Cache for event loop ──────────────────────────────────────────────
        self._prices_ff  = prices
        self._highs_ff   = highs
        self._lows_ff    = lows
        self._opens_ff   = self.opens.ffill() if not self.opens.empty \
                           else prev_close
        self._open_proxy = prev_close   # prev-close fallback for open

        print("  Indicators ready.")
        self._precompute_signal_matrices()

    # ──────────────────────────────────────────────────────────────────────────
    # VECTORISED SIGNAL MATRICES (whole-history, computed once)
    # ──────────────────────────────────────────────────────────────────────────

    def _precompute_signal_matrices(self):
        """
        Whole-history, fully-vectorised versions of filter_universe(),
        _trend_gate(), and _find_vcp_signal(). These three were previously
        recomputed per-day (universe/trend) or per-stock-per-day (VCP) inside
        the event loop via scalar .iloc[idx].get(stock) lookups — the main
        cost of the old backtest loop. Every input here depends only on T-1
        market data (never portfolio state), so the whole date × stock result
        is identical whichever positions happen to be open — safe to compute
        once, in full, up front.

        Each matrix is built from the exact same underlying factor frames the
        scalar methods already read from (self._high_52w, self._sma_fast, ...),
        with no extra shifting applied — row k of each matrix here equals
        exactly what filter_universe(k+1)/_trend_gate(k+1)/_find_vcp_signal(
        stock, k+1) would have returned (since those methods themselves read
        row idx = i-1 of these same frames). The event loop reads row (i-1)
        from these matrices exactly as it used to call the row-(i-1) methods.
        """
        print("  Vectorising signal matrices...")

        c    = self._prices_ff
        sf   = self._sma_fast
        sm   = self._sma_mid
        ss   = self._sma_slow
        ss_n = self._sma_slow_lag
        hi52 = self._high_52w

        # ── Universe mask (vectorised filter_universe) ────────────────────────
        price_ok   = c >= self.min_price
        dvol_rank  = self._dvol_avg63.rank(axis=1, ascending=False, method='min')
        dvol_ok    = (dvol_rank <= self.universe_top_n) & (dvol_rank >= self.universe_min_n)
        circuit_ok = self._circuit_count <= self.max_circuit_days
        ca_ok      = ~self._ca_mask.fillna(False)

        self._universe_mask_matrix = (price_ok & dvol_ok & circuit_ok & ca_ok).fillna(False)

        # ── Trend Template (vectorised _trend_gate) ────────────────────────────
        tt1 = (c > sm) & (c > ss)
        tt2 = sm > ss
        tt3 = ss > ss_n
        tt4 = (sf > sm) & (sm > ss)
        tt5 = c > sf
        tt7 = c >= hi52 * (1.0 - self.within_52w_high_pct)

        # TT8: cross-sectional RS percentile rank, restricted to universe —
        # DataFrame.rank(axis=1, pct=True) ranks within each row independently
        # (identical algorithm/tie-method to the old per-day Series.rank call),
        # ignoring NaN in both numerator and denominator automatically.
        ret_masked = self._ret_1y.where(self._universe_mask_matrix)
        tt8 = (ret_masked.rank(axis=1, pct=True) * 100).fillna(0) >= self.rs_min_percentile

        self._trend_mask_matrix = (tt1 & tt2 & tt3 & tt4 & tt5 & tt7 & tt8).fillna(False)

        # ── VCP signal (vectorised _find_vcp_signal) ───────────────────────────
        vcp1 = self._vcp_base_range <= self.vcp_base_tight_pct
        vcp2 = self._vcp_vol_ratio  <= self.vcp_vol_contract_pct
        vcp3 = c > self._vcp_high_n
        vcp4 = (hi52 > 0) & (c >= hi52 * (1.0 - self.vcp_near_high_pct))

        self._vcp_signal_matrix = (vcp1 & vcp2 & vcp3 & vcp4).fillna(False)

        print("  Signal matrices ready.")

    # ──────────────────────────────────────────────────────────────────────────
    # REGIME FLAGS (precomputed, vectorised)
    # ──────────────────────────────────────────────────────────────────────────

    def _compute_regime_flags(self):
        """
        Returns a single boolean Series indexed to prices.index.
        True  → condition met → new entries permitted.
        False → entries blocked.

        Condition (bench): raw-universe benchmark has NOT been below its
                            SMA for ALL bench_consec_days of the last N days.

        Raw universe (_raw_universe_df = price-floor only) keeps the
        benchmark independent of universe_top_n — changing the entry pool
        doesn't change the macro read.
        All data is T-1 shifted — no lookahead.
        """
        prices = self._prices_ff

        # ── Benchmark consecutive-days check ──────────────────────────────────
        # Block only when benchmark was below SMA on ALL N of the last N days.
        bench_below = (
            (self._bench_series < self._bench_sma)
            .shift(1)
            .infer_objects(copy=False)
            .fillna(False)
            .astype(int)
        )
        rolling_sum = bench_below.rolling(
            self.bench_consec_days,
            min_periods=self.bench_consec_days,
        ).sum()
        bench_ok = (rolling_sum < self.bench_consec_days).fillna(True)
        bench_ok = bench_ok.reindex(prices.index).fillna(True)

        return bench_ok

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER (per bar, T-1 data)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, i, date):
        """
        Returns a boolean Series of eligible stocks for bar i.
        Conditions: price floor, dVol rank band, circuit breaker, CA filter.
        All use T-1 data (row i-1).
        """
        prev_close = self._prices_ff.iloc[i - 1]
        price_ok   = prev_close >= self.min_price

        dvol_row   = self._dvol_avg63.iloc[i - 1]
        dvol_rank  = dvol_row.rank(ascending=False, method='min')
        dvol_ok    = (dvol_rank <= self.universe_top_n) & \
                     (dvol_rank >= self.universe_min_n)

        circuit_ok = self._circuit_count.iloc[i - 1] <= self.max_circuit_days
        ca_ok      = ~self._ca_mask.iloc[i - 1].fillna(False)

        return price_ok & dvol_ok & circuit_ok & ca_ok

    # ──────────────────────────────────────────────────────────────────────────
    # TREND TEMPLATE (per stock, T-1 data)
    # ──────────────────────────────────────────────────────────────────────────

    def _trend_gate(self, i, universe_mask=None):
        """
        Returns a boolean Series — True if the stock passes all 7 Trend
        Template criteria at bar i (using T-1 data, row i-1).

        TT1: Price > SMA-mid AND Price > SMA-slow
        TT2: SMA-mid > SMA-slow
        TT3: SMA-slow > SMA-slow N days ago (upward slope)
        TT4: SMA-fast > SMA-mid > SMA-slow (full bullish stack)
        TT5: Price > SMA-fast
        TT7: Price within within_52w_high_pct of 52w high
        TT8: 1-year RS return rank >= rs_min_percentile
        """
        idx  = i - 1
        c    = self._prices_ff.iloc[idx]

        sf   = self._sma_fast.iloc[idx]
        sm   = self._sma_mid.iloc[idx]
        ss   = self._sma_slow.iloc[idx]
        ss_n = self._sma_slow_lag.iloc[idx]
        hi52 = self._high_52w.iloc[idx]

        tt1 = (c > sm) & (c > ss)
        tt2 = sm > ss
        tt3 = ss > ss_n
        tt4 = (sf > sm) & (sm > ss)
        tt5 = c > sf
        tt7 = c >= hi52 * (1.0 - self.within_52w_high_pct)

        # TT8: cross-sectional RS percentile rank
        ret_row = self._ret_1y.iloc[idx]
        if universe_mask is not None:
            ret_row = ret_row[universe_mask]   # restrict to universe-eligible only
        ret_row = ret_row.dropna()
        if len(ret_row) > 0:
            rs_ranks = ret_row.rank(pct=True) * 100
            tt8 = rs_ranks.reindex(c.index).fillna(0) >= self.rs_min_percentile
        else:
            tt8 = pd.Series(False, index=c.index)

        return tt1 & tt2 & tt3 & tt4 & tt5 & tt7 & tt8

    # ──────────────────────────────────────────────────────────────────────────
    # VCP SIGNAL (per stock, T-1 data)
    # ──────────────────────────────────────────────────────────────────────────

    def _find_vcp_signal(self, stock, i):
        """
        Evaluates all 4 VCP criteria for one stock at bar i (T-1 data).

        VCP1: 15-day base range (hi-lo)/hi <= vcp_base_tight_pct
        VCP2: 15-day avg volume <= vcp_vol_contract_pct × prior 30d avg
        VCP3: T-1 close > highest close of prior vcp_breakout_window days
        VCP4: T-1 close within vcp_near_high_pct of 52-week high

        Returns True if all 4 pass, False otherwise.
        """
        idx = i - 1

        # VCP1: base tightness
        base_rng = float(self._vcp_base_range.iloc[idx].get(stock, np.nan)) \
                   if stock in self._vcp_base_range.columns else np.nan
        if pd.isna(base_rng) or base_rng > self.vcp_base_tight_pct:
            return False

        # VCP2: volume contraction
        vol_ratio = float(self._vcp_vol_ratio.iloc[idx].get(stock, np.nan)) \
                    if stock in self._vcp_vol_ratio.columns else np.nan
        if pd.isna(vol_ratio) or vol_ratio > self.vcp_vol_contract_pct:
            return False

        # VCP3: price breakout above N-day high
        prev_close = float(self._prices_ff.iloc[idx].get(stock, np.nan)) \
                     if stock in self._prices_ff.columns else np.nan
        high_n = float(self._vcp_high_n.iloc[idx].get(stock, np.nan)) \
                 if stock in self._vcp_high_n.columns else np.nan
        if pd.isna(prev_close) or pd.isna(high_n) or prev_close <= high_n:
            return False

        # VCP4: near 52-week high
        hi52 = float(self._high_52w.iloc[idx].get(stock, np.nan)) \
               if stock in self._high_52w.columns else np.nan
        if pd.isna(hi52) or hi52 <= 0:
            return False
        if prev_close < hi52 * (1.0 - self.vcp_near_high_pct):
            return False

        return True


    # ──────────────────────────────────────────────────────────────────────────
    # DYNAMIC ATR MULTIPLIER (same logic as HR chandelier)
    # ──────────────────────────────────────────────────────────────────────────

    def _dynamic_atr_multiplier(self, atr_pct):
        """
        Map entry-time ATR% to a trail multiplier, interpolating linearly
        between trail_atr_mult_max (calm, low ATR%) and trail_atr_mult_min
        (volatile, high ATR%). Fixed once at entry, stored on the holding.

        Volatile stocks get a LOWER multiplier — their ATR is already large
        in absolute terms so a smaller multiplier keeps the distance sensible.
        Calm stocks get a HIGHER multiplier to compensate for their small ATR.
        """
        if pd.isna(atr_pct) or atr_pct <= self.trail_atr_pct_calm:
            return self.trail_atr_mult_max
        if atr_pct >= self.trail_atr_pct_volatile:
            return self.trail_atr_mult_min
        frac = ((atr_pct - self.trail_atr_pct_calm) /
                (self.trail_atr_pct_volatile - self.trail_atr_pct_calm))
        return self.trail_atr_mult_max - frac * (self.trail_atr_mult_max - self.trail_atr_mult_min)

    # ──────────────────────────────────────────────────────────────────────────
    # EXIT STOP EVALUATION (per position, per bar)
    # ──────────────────────────────────────────────────────────────────────────

    def _effective_stop(self, h, prev_close, days_held):
        """
        Compute effective stop level for a holding, updating trail state in place.

        Peak is updated via prev_close (T-1 settled close) — conservative,
        avoids locking in stops on intraday wicks.

        hard_stop  = entry × (1 − hard_stop_pct)  — fixed, never moves down
        trail_stop = peak × (1 − trail_pct)        — ratchets up only
                     floored at entry × (1 + trail_floor_pct)

        Min-hold grace (first min_hold_days days): only hard_stop active.
        Trail activates once position gains >= trail_activate_pct from entry.
        Effective stop = max(hard_stop, trail_stop if active).

        Modifies h in place. Returns the effective stop level.
        """
        entry_price = h['entry_price']
        hard_stop   = h['hard_stop']

        # Update peak using T-1 settled close
        if not pd.isna(prev_close) and prev_close > 0:
            h['peak_price'] = max(h.get('peak_price', entry_price), prev_close)

        # Min-hold grace: only hard stop active
        if days_held < self.min_hold_days:
            return hard_stop

        peak = h['peak_price']

        # Check trail activation
        if not h.get('trail_active', False):
            if peak >= entry_price * (1.0 + self.trail_activate_pct):
                h['trail_active'] = True

        if h.get('trail_active', False):
            trail_floor = entry_price * (1.0 + self.trail_floor_pct)
            # ATR-based trail: use fixed distance computed at entry.
            # Falls back to percentage trail if trail_atr_distance not on holding.
            trail_dist = h.get('trail_atr_distance', None)
            if trail_dist is not None and trail_dist > 0:
                new_trail = max(hard_stop, trail_floor, peak - trail_dist)
            else:
                new_trail = max(hard_stop, trail_floor, peak * (1.0 - self.trail_pct))
            h['trail_stop'] = max(h.get('trail_stop', hard_stop), new_trail)
            return max(hard_stop, h['trail_stop'])

        return hard_stop

    # ──────────────────────────────────────────────────────────────────────────
    # OBSERVATIONAL ENRICHMENT (recorded at entry for post-trade analysis)
    # ──────────────────────────────────────────────────────────────────────────

    def _obs_enrichment(self, stock, i, entry_price):
        """Compute context metrics at entry time. Uses T-1 data (row i-1)."""
        idx    = i - 1
        close  = float(self._prices_ff.iloc[idx].get(stock, np.nan)) \
                 if stock in self._prices_ff.columns else np.nan
        atr    = float(self._atr14.iloc[idx].get(stock, np.nan)) \
                 if stock in self._atr14.columns else np.nan
        hi52   = float(self._high_52w.iloc[idx].get(stock, np.nan)) \
                 if stock in self._high_52w.columns else np.nan
        sf     = float(self._sma_fast.iloc[idx].get(stock, np.nan)) \
                 if stock in self._sma_fast.columns else np.nan
        ss     = float(self._sma_slow.iloc[idx].get(stock, np.nan)) \
                 if stock in self._sma_slow.columns else np.nan

        def _r(x): return round(x, 4) if pd.notna(x) else np.nan

        return {
            'ATR_Ratio'    : _r(atr / close if close and close > 0 and pd.notna(atr) else np.nan),
            'Dist_52w_High': _r((close / hi52 - 1) * 100 if hi52 and hi52 > 0 else np.nan),
            'Dist_SMA50'   : _r((close / sf - 1) * 100 if sf and sf > 0 else np.nan),
            'Dist_SMA200'  : _r((close / ss - 1) * 100 if ss and ss > 0 else np.nan),
        }

    # ──────────────────────────────────────────────────────────────────────────
    # TRADE RECORD
    # ──────────────────────────────────────────────────────────────────────────

    def _record_closed_trade(self, ticker, holding, exit_date,
                             exit_price, fill_price, exit_reason,
                             hard_stop=np.nan):
        """Append one completed trade to self.position_metadata."""
        entry_price      = holding['entry_price']
        entry_date       = holding['entry_date']
        weight           = holding.get('weight', 0.0)
        intended_weight  = holding.get('intended_weight', weight)
        min_price        = holding.get('min_price', entry_price)
        max_price        = holding.get('max_price', entry_price)

        mae_pct = ((min_price / entry_price) - 1) * 100 \
                  if (pd.notna(entry_price) and entry_price > 0) else np.nan
        mfe_pct = ((max_price / entry_price) - 1) * 100 \
                  if (pd.notna(entry_price) and entry_price > 0) else np.nan

        record = {
            'Ticker'          : ticker,
            'Entry_Date'      : entry_date,
            'Entry_Price'     : round(entry_price, 4) if pd.notna(entry_price) else np.nan,
            'Exit_Date'       : exit_date,
            'Exit_Price'      : round(fill_price,  4) if pd.notna(fill_price)  else np.nan,
            'Close_At_Exit'   : round(exit_price,  4) if pd.notna(exit_price)  else np.nan,
            'Hard_Stop'       : round(hard_stop,   4) if pd.notna(hard_stop)   else np.nan,
            'Trail_Stop'      : round(holding.get('trail_stop', np.nan), 4)
                                if pd.notna(holding.get('trail_stop', np.nan)) else np.nan,
            'Trail_Active'    : holding.get('trail_active', False),
            'Exit_Reason'     : exit_reason,
            'Weight'          : round(weight, 6),
            'Intended_Weight' : round(intended_weight, 6),
            'MAE_Pct'         : round(mae_pct, 2) if pd.notna(mae_pct) else np.nan,
            'MFE_Pct'         : round(mfe_pct, 2) if pd.notna(mfe_pct) else np.nan,
        }
        record.update(holding.get('obs', {}))
        self.position_metadata.append(record)

    # ──────────────────────────────────────────────────────────────────────────
    # LIVE EXIT SIGNALS  (called daily by external live-trading system)
    # ──────────────────────────────────────────────────────────────────────────

    def get_exit_signals(self, portfolio: dict, live_data: dict,
                         today=None) -> dict:
        """
        Evaluate exit conditions for all currently-held positions using
        today's live OHLC bar data.

        Parameters
        ----------
        portfolio : dict
            ticker → position dict with keys:
                entry_date, entry_price, hard_stop, trail_stop,
                trail_active, peak_price, weight
        live_data : dict
            ticker → bar dict with keys: open, high, low, close
        today : date-like, optional

        Returns
        -------
        dict with keys:
            'exits' : ticker → {'reason', 'fill_price', 'stop_level'}
            'holds' : ticker → {'updated_peak', 'updated_trail_stop',
                                 'trail_active', 'stop_level'}
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

            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
                continue

            _high  = float(bar.get('high',  _close))
            _low   = float(bar.get('low',   _close))
            _open  = float(bar.get('open',  _close))
            if pd.isna(_high) or _high <= 0: _high = _close
            if pd.isna(_low)  or _low  <= 0: _low  = _close
            if pd.isna(_open) or _open <= 0: _open = _close

            # Circuit day guard
            _has_real_hl = ('high' in bar) and ('low' in bar)
            if _has_real_hl and _high == _low:
                holds[ticker] = {
                    'updated_peak'       : float(pos.get('peak_price', _close)),
                    'updated_trail_stop' : float(pos.get('trail_stop', 0.0)),
                    'trail_active'       : pos.get('trail_active', False),
                    'stop_level'         : float(pos.get('hard_stop', 0.0)),
                }
                continue

            entry_price  = float(pos.get('entry_price', np.nan))
            entry_date_r = pos.get('entry_date', '')
            hard_stop    = float(pos.get('hard_stop', 0.0))
            trail_stop   = float(pos.get('trail_stop', hard_stop))
            trail_active = bool(pos.get('trail_active', False))
            peak_price   = float(pos.get('peak_price', entry_price))

            try:
                _entry_dt  = pd.Timestamp(str(entry_date_r)[:10]).date()
                _days_held = (today - _entry_dt).days
            except Exception:
                _days_held = 999

            # Build a temporary holding dict to reuse _effective_stop logic
            h = {
                'entry_price' : entry_price,
                'hard_stop'   : hard_stop,
                'trail_stop'  : trail_stop,
                'trail_active': trail_active,
                'peak_price'  : peak_price,
            }
            eff_stop = self._effective_stop(h, _close, _days_held)

            # Stale exit check (uses live close as proxy for settled price)
            if _days_held >= self.stale_days:
                ret = (_close / entry_price) - 1.0 \
                      if (not pd.isna(entry_price) and entry_price > 0) else 0.0
                if ret < self.stale_ret_pct:
                    exits[ticker] = {
                        'reason'     : 'STALE',
                        'fill_price' : float(_open),
                        'stop_level' : float(eff_stop),
                    }
                    continue

            # Stop exit
            if _low <= eff_stop:
                fill = _open if _open <= eff_stop else eff_stop
                reason = 'TRAIL_STOP' if h.get('trail_active', False) else 'HARD_STOP'
                exits[ticker] = {
                    'reason'     : reason,
                    'fill_price' : float(fill),
                    'stop_level' : float(eff_stop),
                }
            else:
                holds[ticker] = {
                    'updated_peak'       : float(h['peak_price']),
                    'updated_trail_stop' : float(h.get('trail_stop', hard_stop)),
                    'trail_active'       : bool(h.get('trail_active', False)),
                    'stop_level'         : float(eff_stop),
                }

        return {'exits': exits, 'holds': holds}
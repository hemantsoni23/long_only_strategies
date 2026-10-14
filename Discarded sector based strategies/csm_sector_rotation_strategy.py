"""
csm_sector_rotation_strategy.py
================================
Cross-Sectional Momentum — Sector Rotation (strategy CORE only).

Different EDGE from csm_absolute / csm_quad / csm_batch, not another reparametrization
of the same one: those three all flat-rank every stock in one pool by dual-lookback
Sharpe momentum. This one adds a SECTOR-TIMING layer on top -- a stock is only
tradeable at all if its sector itself has positive, top-ranked momentum that month.
The stock-level ranking/universe/stop/overlay machinery underneath is the SAME proven
chassis as csm_batch_strategy.py (verbatim reuse -- see calculate_factors() for the
one part that's actually new).

Two-stage mechanism:
  1. SECTOR momentum: build a synthetic equal-weight daily return index per sector
     (from Sector_clean-mapped member tickers), compute the identical dual-lookback
     (12m+6m Sharpe) momentum factor on that sector index, rank the ~11 sectors each
     month. A sector is "eligible" if it ranks in the top sector_top_k AND its own
     raw 12m return is positive (mirrors the stock-level absolute-momentum gate).
  2. STOCK selection: exactly the csm_batch chassis (5-filter universe, dual-lookback
     Sharpe ranking, hysteresis, inverse-vol sizing, 3-layer stop, Crash/Corr Guard,
     Vol Targeting) -- but restricted to only the stocks whose sector is eligible
     that month. A stock in a sector that drops out of the top-K becomes ineligible
     and exits at that month's rebalance, same code path as any other rank-based exit.

Sector mapping caveat (documented, not hidden): New_momentum_strategy/instruments_clean.csv
has NO date dimension -- Sector_clean is today's classification applied retroactively
across the whole backtest history. This is a smaller risk than it would be for a
cap-tier signal (a company's sector rarely changes, unlike market cap, which drifts
mechanically with the same price history being backtested), but it is not zero --
genuine sector reclassifications and business-model pivots do happen. Report this
caveat alongside any backtest result from this strategy.

Sector-level concentration cap is NOT built into v1 (documented limitation, not an
oversight) -- per-stock max_weight_per_stock and sector_top_k already bound
concentration indirectly; add an explicit sector weight cap only if a real backtest
shows it's needed.
"""

import pandas as pd
import numpy as np
import os
import glob


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADERS
# ══════════════════════════════════════════════════════════════════════════════

def load_data(folder_path):
    """Load all CSV files from folder_path.
    Returns: prices_df, volumes_df, highs_df, lows_df, opens_df (all DataFrames).
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


def load_sector_map(csv_path):
    """
    Loads New_momentum_strategy/instruments_clean.csv and returns a ticker -> sector
    pd.Series (using the Sector_clean column -- 11 broad sectors, vs Industry_clean's
    204 categories which are too thin for reliable sector-level momentum).

    Ambiguous trading_symbols (same symbol appears more than once in the file, e.g.
    an NSE/BSE collision) are dropped entirely rather than guessed at -- same
    "exclude, don't guess" discipline as the ticker-collision handling documented
    elsewhere in this repo's data-quality notes.
    """
    df = pd.read_csv(csv_path)
    n_before = len(df)
    df = df[~df['trading_symbol'].duplicated(keep=False)]
    n_dropped = n_before - len(df)
    if n_dropped:
        print(f"[Sector map] Dropped {n_dropped} rows with ambiguous (duplicated) "
              f"trading_symbol values.")
    sector_map = df.set_index('trading_symbol')['Sector_clean']
    print(f"[Sector map] Loaded {len(sector_map)} ticker->sector mappings, "
          f"{sector_map.nunique()} distinct sectors.")
    return sector_map


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class CSMSectorRotation:
    """
    Sector-timed cross-sectional momentum.

    Per-position state lives in active_holdings[ticker]:
        entry_date, entry_price, peak_price, atr_stop (ratchets up only),
        stop_pct, atr_at_entry, weight, min_price, max_price

    This class holds the strategy CORE only. The event-driven backtest engine,
    trade log, metrics and plots live in csm_sector_rotation_backtest.py as free
    functions taking an instance of this class as their first argument -- same
    Tier-1/Tier-2 split as csm_batch_strategy.py.

    Live callers use get_positions() for target weights and get_exit_signals() for
    daily stop/crash-guard monitoring, and must also call every trading day:
        apply_risk_overlays()        — Corr Guard + Vol Targeting de-lever
        apply_crash_guard_cooldown() — post-panic new-entry freeze
        check_stop_cooldown()        — per-ticker post-stop re-entry ban
    identical contract to csm_batch_strategy.py.
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        sector_map          = None,   # REQUIRED: pd.Series, ticker -> sector (see
                                       # load_sector_map()). This is the new edge.
        # Sector-timing layer
        sector_lookback_months = 12,
        sector_lookback_short_months = 6,
        sector_lag_months       = 1,
        sector_top_k            = 4,   # eligible sectors per month, out of ~11
        # Factor (stock level -- identical formula/params to csm_batch_strategy.py)
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
        atr_multiplier_high_vol = 2.0,
        hard_stop_from_entry    = 0.15,
        hard_stop_from_peak     = 0.20,
        stop_slippage_pct       = 0.003,
        use_trailing_stop       = False,
        stop_cooldown_days      = 20,
        min_hold_days           = 0,
        # Risk overlays
        use_crash_guard         = True,
        crash_guard_cooldown    = 10,
        corr_guard_threshold    = 0.8,
        vol_target              = 0.13,
        leverage_bull            = 1.0,   # exposure multiplier, benchmark > trend SMA
        leverage_bear             = 0.0,   # HARD gate (zero, not partial) when
                                            # benchmark < trend SMA -- csm_batch's
                                            # chassis has no proactive regime gate,
                                            # only Crash Guard (reacts to a vol
                                            # SPIKE, after the fact). Validated on
                                            # the sibling csm_residual build: a soft
                                            # 0.8x scalar barely moved MaxDD, a hard
                                            # zero-exposure gate did (-45%->-34% in
                                            # that build's 2008 window). This
                                            # strategy's own worst drawdown is a
                                            # DIFFERENT episode (2018-19 NBFC/midcap
                                            # crash, not 2008) but the same missing
                                            # mechanism applies.
        trend_gate_window        = 150,    # SMA window (trading days)
        leverage_panic            = 0.0,   # same hard gate for a vol-spike panic
                                            # regime that hasn't yet dropped below trend
        # Position sizing
        max_weight_per_stock    = 0.05,
        rebalance_months        = 1,
        rebalance_min_fill_frac = 0.5,
        # Dynamic rank-decay exit (fractions of top_n, anti-overfit)
        rank_exit_dynamic       = True,
        rank_exit_drop_frac     = 0.33,
        rank_exit_floor_frac    = 0.67,
        **kwargs,
    ):
        if sector_map is None:
            raise ValueError(
                "CSMSectorRotation requires sector_map -- a ticker->sector pd.Series "
                "(see load_sector_map()). This is the strategy's core edge, not an "
                "optional overlay."
            )

        self.prices               = prices_df
        self.volumes              = volumes_df
        self.highs                = highs_df  if highs_df  is not None else pd.DataFrame()
        self.lows                 = lows_df   if lows_df   is not None else pd.DataFrame()
        self.opens                = opens_df  if opens_df  is not None else pd.DataFrame()
        self.benchmark            = benchmark_series
        self.sector_map           = sector_map.reindex(prices_df.columns)

        self.sector_lookback_months       = sector_lookback_months
        self.sector_lookback_short_months = sector_lookback_short_months
        self.sector_lag_months            = sector_lag_months
        self.sector_top_k                 = sector_top_k

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
        self.leverage_bull        = leverage_bull
        self.leverage_bear        = leverage_bear
        self.trend_gate_window    = trend_gate_window
        self.leverage_panic       = leverage_panic

        self.max_weight_per_stock = max_weight_per_stock
        self.rebalance_months     = rebalance_months
        self.rebalance_min_fill_frac = rebalance_min_fill_frac
        self.rank_exit_dynamic    = rank_exit_dynamic
        self.rank_exit_drop_frac  = rank_exit_drop_frac
        self.rank_exit_floor_frac = rank_exit_floor_frac

        self.factors               = None
        self.momentum_returns      = None
        self.sector_factors        = None
        self.sector_eligible_mask  = None
        self.positions              = None
        self.results                = None
        self.position_metadata      = []
        self.atr                    = None

        n_mapped = int(self.sector_map.notna().sum())
        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty
        print(f"CSM Sector Rotation initialised  |  top_n={top_n}  buffer={buffer_ratio}"
              f"  sector_top_k={sector_top_k}  sector_lookback={sector_lookback_months}m/"
              f"{sector_lookback_short_months}m  mapped_tickers={n_mapped}/{len(self.sector_map)}"
              f"  ATR-stops={'YES' if has_h and has_l else 'FALLBACK-2%'}"
              f"  opens={'YES' if has_o else 'FALLBACK-close'}"
              f"  crash_guard={'ON' if use_crash_guard else 'OFF'}"
              f"  trailing_stop={'ON' if use_trailing_stop else 'OFF'}"
              f"  universe_top_n={universe_top_n}")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER  (identical to csm_batch_strategy.py -- proven, reused as-is)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, daily_prices):
        """
        Boolean mask for stocks eligible to enter the ranked universe.
        Filters (all lookahead-safe via .shift):
          1. Price > min_price (prev month)
          2. 63d rolling median dollar-vol rank <= universe_top_n
          3. Circuit days (high==low) in last 63d <= max_circuit_days
          4. Price > SMA-200 at month-end
          5. Previous month's return >= -15% (falling-knife gate)
        """
        price_mask = monthly_prices.shift(1) > self.min_price

        daily_dvol        = self.prices * self.volumes
        median_dvol_daily = daily_dvol.rolling(window=63, min_periods=21).median().shift(1)
        monthly_dvol      = median_dvol_daily.resample('ME').last().reindex(monthly_prices.index)
        dvol_rank         = monthly_dvol.rank(axis=1, ascending=False, method='min')
        liquidity_mask    = dvol_rank <= self.universe_top_n

        circuit_mask = pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)
        if not self.highs.empty and not self.lows.empty:
            is_circuit   = (self.highs == self.lows).shift(1)
            circuit_cnt  = is_circuit.rolling(window=63, min_periods=1).sum()
            monthly_circ = circuit_cnt.resample('ME').last().reindex(monthly_prices.index).fillna(0)
            circuit_mask = monthly_circ <= self.max_circuit_days

        sma200_daily = daily_prices.ffill().rolling(window=200, min_periods=150).mean().shift(1)
        is_above_sma = (daily_prices > sma200_daily).shift(1)
        trend_mask   = is_above_sma.resample('ME').last().astype(bool)
        trend_mask   = trend_mask.reindex(monthly_prices.index, fill_value=False)

        monthly_ret = monthly_prices.pct_change(fill_method=None)
        crash_mask  = monthly_ret.shift(1) >= -0.15

        return price_mask & liquidity_mask & circuit_mask & trend_mask & crash_mask

    # ──────────────────────────────────────────────────────────────────────────
    # SECTOR-LEVEL MOMENTUM  (the new part)
    # ──────────────────────────────────────────────────────────────────────────

    def _compute_sector_eligibility(self, monthly_prices):
        """
        Builds a synthetic equal-weight daily index per sector, computes the same
        dual-lookback (long/short Sharpe) momentum factor used at the stock level,
        ranks sectors each month, and returns a per-stock monthly boolean mask:
        True where that stock's sector ranked in the top sector_top_k AND has
        positive raw long-window return that month (mirrors the stock-level
        absolute-momentum gate). Unmapped tickers (no known sector) are always
        False -- excluded, not guessed at.
        """
        sectors = sorted(self.sector_map.dropna().unique())
        daily_ret = self.prices.pct_change(fill_method=None)

        sector_daily_ret = pd.DataFrame(index=self.prices.index, columns=sectors, dtype=float)
        for s in sectors:
            members = self.sector_map.index[self.sector_map == s]
            members = [m for m in members if m in daily_ret.columns]
            sector_daily_ret[s] = daily_ret[members].mean(axis=1, skipna=True)

        sector_idx     = (1.0 + sector_daily_ret.fillna(0.0)).cumprod()
        sector_monthly = sector_idx.resample('ME').last()
        sector_ret     = sector_monthly.pct_change(fill_method=None)

        L, S, lag = (self.sector_lookback_months, self.sector_lookback_short_months,
                     self.sector_lag_months)

        ret_long_sec  = (sector_monthly.shift(lag) / sector_monthly.shift(lag + L)) - 1
        vol_long_sec  = (sector_ret.rolling(window=L).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_long_sec = (ret_long_sec / vol_long_sec).clip(upper=5.0, lower=-5.0)

        ret_short_sec  = (sector_monthly.shift(lag) / sector_monthly.shift(lag + S)) - 1
        vol_short_sec  = (sector_ret.rolling(window=S).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_short_sec = (ret_short_sec / vol_short_sec).clip(upper=5.0, lower=-5.0)

        self.sector_factors = (factor_long_sec + factor_short_sec) / 2.0
        self.sector_factors = self.sector_factors.reindex(monthly_prices.index)
        ret_long_sec         = ret_long_sec.reindex(monthly_prices.index)

        sector_rank = self.sector_factors.rank(axis=1, ascending=False, method='first')
        sector_ok   = (sector_rank <= self.sector_top_k) & (ret_long_sec > 0)

        # Broadcast sector eligibility to a per-stock mask
        stock_sector_ok = pd.DataFrame(False, index=monthly_prices.index, columns=self.prices.columns)
        for s in sectors:
            members = self.sector_map.index[self.sector_map == s]
            members = [m for m in members if m in stock_sector_ok.columns]
            if not members or s not in sector_ok.columns:
                continue
            stock_sector_ok[members] = np.broadcast_to(
                sector_ok[[s]].values, (len(sector_ok), len(members))
            )

        n_eligible_sectors = sector_ok.sum(axis=1)
        print(f"Sector eligibility: avg {n_eligible_sectors.mean():.1f} of {len(sectors)} "
              f"sectors eligible/month  (top_k={self.sector_top_k})")
        return stock_sector_ok

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """
        Stock-level factor is the identical dual-lookback (12m+6m) Sharpe momentum
        used by csm_batch_strategy.py. The only difference from that chassis: a
        stock only enters self.factors at all if BOTH (a) it passes the standard
        5-filter universe, AND (b) its sector is currently eligible (top-K sector
        momentum, positive absolute sector return) -- see _compute_sector_eligibility().
        """
        print("Calculating Sector-Rotation Factors...")

        monthly_prices = self.prices.resample('ME').last()
        monthly_ret    = monthly_prices.pct_change(fill_method=None)

        L  = self.lookback_months
        S  = self.lookback_short_months
        lag= self.lag_months

        ret_long  = (monthly_prices.shift(lag) / monthly_prices.shift(lag + L)) - 1
        vol_long  = (monthly_ret.rolling(window=L).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_long = (ret_long / vol_long).clip(upper=5.0, lower=-5.0)

        ret_short  = (monthly_prices.shift(lag) / monthly_prices.shift(lag + S)) - 1
        vol_short  = (monthly_ret.rolling(window=S).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_short = (ret_short / vol_short).clip(upper=5.0, lower=-5.0)

        self.factors          = (factor_long + factor_short) / 2.0
        self.momentum_returns = ret_long

        valid_universe          = self.filter_universe(monthly_prices, self.prices)
        self.sector_eligible_mask = self._compute_sector_eligibility(monthly_prices)

        combined_mask          = valid_universe & self.sector_eligible_mask
        self.factors           = self.factors.where(combined_mask)
        self.momentum_returns  = self.momentum_returns.where(combined_mask)

        self._prepare_stop_indicators(monthly_prices)
        self.factors.dropna(how='all', inplace=True)
        self.momentum_returns.dropna(how='all', inplace=True)

        close_p = self.prices
        if not self.highs.empty and not self.lows.empty:
            _h, _l, _pc = self.highs.ffill(), self.lows.ffill(), close_p.shift(1)
            _tr = (_h - _l).abs().combine((_h - _pc).abs(), np.maximum).combine((_l - _pc).abs(), np.maximum)
        else:
            _tr = close_p.diff().abs() * np.sqrt(np.pi / 2)
        self.atr = _tr.ewm(com=self.atr_period - 1, adjust=False).mean().shift(1)

        if self.benchmark is not None:
            bench_ret  = self.benchmark.pct_change(fill_method=None)
            bvol_daily = bench_ret.rolling(window=21).std().shift(1)
            self._panic_threshold_series = bvol_daily.expanding(min_periods=126).quantile(0.95)
            self._panic_threshold        = float(bvol_daily.quantile(0.95))
            self._bvol_daily             = bvol_daily

            _bvol_reidx = bvol_daily.reindex(self.prices.index).ffill()
            self._high_vol_threshold_series = (
                _bvol_reidx.expanding(min_periods=63).quantile(0.75).shift(1).ffill()
            )

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

        # ── Monthly regime trend gate (hard, not a partial scalar) ────────────
        # PROACTIVE, book-level exposure gate applied in get_positions() -- distinct
        # from Crash Guard (reacts to a vol SPIKE, daily, after the fact). See the
        # leverage_bear docstring in __init__ for why this is a hard 0.0 gate, not
        # a soft scalar.
        if self.benchmark is not None:
            _tw = self.trend_gate_window
            bench_sma_daily = self.benchmark.rolling(_tw, min_periods=int(_tw * 0.75)).mean().shift(1)
            bench_below_sma = (self.benchmark < bench_sma_daily).shift(1)
            self._regime_bear_monthly = (bench_below_sma.resample('ME').last()
                                          .astype(bool).reindex(monthly_prices.index, fill_value=False))
            panic_daily = (self._bvol_daily > self._panic_threshold_series).fillna(False)
            self._regime_panic_monthly = (panic_daily.resample('ME').last()
                                           .astype(bool).reindex(monthly_prices.index, fill_value=False))
        else:
            self._regime_bear_monthly  = pd.Series(False, index=monthly_prices.index)
            self._regime_panic_monthly = pd.Series(False, index=monthly_prices.index)

        print(f"Factors shape: {self.factors.shape}  "
              f"Non-NaN per month (avg): {self.factors.notna().sum(axis=1).mean():.0f}")
        return self.factors

    def _prepare_stop_indicators(self, monthly_prices):
        """Pre-compute forward-filled price arrays used by the daily backtest loop."""
        prices_ff = self.prices.ffill()
        self._opens_ff   = self.opens.ffill() if not self.opens.empty else prices_ff.shift(1)
        self._open_proxy = prices_ff.shift(1)
        self._prices_ff  = prices_ff

    # ──────────────────────────────────────────────────────────────────────────
    # SHARED LIVE/BACKTEST RISK-OVERLAY HELPERS  (identical to csm_batch_strategy.py)
    # ──────────────────────────────────────────────────────────────────────────

    def resolve_regime_threshold(self, series, fallback_scalar, as_of_date):
        if series is None or series.empty:
            return fallback_scalar
        ts  = pd.Timestamp(as_of_date)
        idx = series.index[series.index <= ts]
        if len(idx) == 0:
            return fallback_scalar
        val = series.loc[idx[-1]]
        return float(val) if pd.notna(val) else fallback_scalar

    def check_stop_cooldown(self, stock, date, stop_cooldown_tickers):
        if stock not in stop_cooldown_tickers:
            return False
        gap = (pd.Timestamp(date) - pd.Timestamp(stop_cooldown_tickers[stock])).days
        if gap < self.stop_cooldown_days:
            return True
        del stop_cooldown_tickers[stock]
        return False

    def apply_crash_guard_cooldown(self, target_weights, prev_held, cg_cooldown_remaining):
        if cg_cooldown_remaining <= 0:
            return target_weights, cg_cooldown_remaining
        cg_cooldown_remaining -= 1
        gated = target_weights.copy()
        for stock in list(gated.index):
            if stock not in prev_held and gated[stock] > 1e-6:
                gated[stock] = 0.0
        return gated, cg_cooldown_remaining

    def apply_risk_overlays(self, raw_weights, port_ret_history, prev_weights, stock_ret_window):
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
    # STOP STATE MANAGER  (identical to csm_batch_strategy.py)
    # ──────────────────────────────────────────────────────────────────────────

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False):
        if pd.isna(curr_close) or curr_close <= 0:
            return False, np.nan, holding.get('atr_stop', np.nan), holding

        entry_price = holding['entry_price']
        peak_price  = holding['peak_price']
        atr_stop    = holding['atr_stop']

        if not pd.isna(entry_price) and entry_price > 0:
            if (curr_close / entry_price) - 1 < -0.60:
                synthetic_stop = entry_price * 0.40
                fill = synthetic_stop * (1.0 - self.stop_slippage_pct)
                return True, float(fill), float(synthetic_stop), holding

        _trail = self.use_trailing_stop
        peak_hard      = peak_price * (1.0 - self.hard_stop_from_peak) if _trail else -np.inf
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop}

        bar_high = curr_high if (not pd.isna(curr_high) and curr_high > 0) else curr_close
        new_peak = max(peak_price, bar_high)
        if new_peak > peak_price:
            holding['peak_price'] = new_peak

        _atr_mult = self.atr_multiplier_high_vol if high_vol else self.atr_multiplier
        if _trail and not pd.isna(curr_atr) and curr_atr > 0:
            chandelier = float(np.clip(
                new_peak - _atr_mult * curr_atr,
                new_peak * 0.70,
                new_peak * 0.97,
            ))
            atr_stop = max(atr_stop, chandelier)

        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        peak_hard      = new_peak * (1.0 - self.hard_stop_from_peak) if _trail else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop, 'peak_price': new_peak}

        check_price = curr_low if (not pd.isna(curr_low) and curr_low > 0) else curr_close
        if check_price > effective_stop:
            return False, np.nan, effective_stop, holding

        _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
        fill  = _open if _open <= effective_stop else effective_stop * (1.0 - self.stop_slippage_pct)
        return True, float(fill), float(effective_stop), holding

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION  (identical to csm_batch_strategy.py -- eligibility is
    # already baked into self.factors being NaN for ineligible stocks, so this
    # loop needs no sector-specific logic at all)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self, live_holdings=None):
        if self.factors is None:
            raise ValueError("Call calculate_factors() first.")

        print(f"Generating Positions  top_n={self.top_n}  buffer={self.buffer_ratio}  "
              f"abs_momentum_gate=ON  max_wt={self.max_weight_per_stock:.0%}")

        daily_ret   = self.prices.pct_change(fill_method=None)
        monthly_vol = (daily_ret.rolling(21).std().shift(1)
                       .resample('ME').last()
                       .reindex(self.factors.index))

        all_ranks  = self.factors.rank(axis=1, ascending=False, method='first')

        position_list = []
        prev_held     = set()
        held_best_rank: dict = {}
        rank_exit_records: list = []

        entry_threshold = self.top_n
        exit_threshold  = int(self.top_n * (1 + self.buffer_ratio))

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

            if date in self.momentum_returns.index:
                pos_ret_stocks = set(
                    self.momentum_returns.loc[date].dropna().loc[lambda s: s > 0].index
                )
                valid_ranks = valid_ranks[valid_ranks.index.isin(pos_ret_stocks)]

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            current_selection = []
            for stock, rank in valid_ranks.items():
                if stock in prev_held:
                    best = min(held_best_rank.get(stock, rank), rank)
                    held_best_rank[stock] = best
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

            sel_vols = monthly_vol.loc[date, current_selection].fillna(0.02).replace(0, 0.02)
            inv_vol  = 1.0 / sel_vols
            raw_w    = inv_vol / inv_vol.sum()

            cap = self.max_weight_per_stock
            for _ in range(2):
                raw_w = raw_w.clip(upper=cap)
                total = raw_w.sum()
                if total > 0:
                    raw_w = raw_w / total
            raw_w = raw_w.clip(upper=cap)

            full_w = pd.Series(0.0, index=self.factors.columns, name=date)
            full_w.update(raw_w)

            # ── Regime trend gate (bull/bear/panic) ────────────────────────
            current_lev = self.leverage_bull
            if date in self._regime_panic_monthly.index and bool(self._regime_panic_monthly.loc[date]):
                current_lev = self.leverage_panic
            if date in self._regime_bear_monthly.index and bool(self._regime_bear_monthly.loc[date]):
                current_lev = min(current_lev, self.leverage_bear)
            full_w = full_w * current_lev

            position_list.append(full_w)

        self.positions = pd.concat(position_list, axis=1).T
        self.positions.index = all_ranks.index

        self.rank_exit_mask = pd.DataFrame(False, index=all_ranks.index,
                                           columns=self.factors.columns)
        for _d, _s in rank_exit_records:
            if _s in self.rank_exit_mask.columns:
                self.rank_exit_mask.at[_d, _s] = True

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
            print(f"Rank-decay exit ON [dynamic top_n-frac]: drop>={_rk_drop} ranks & rank>{_rk_floor}"
                  f"  ->  {len(rank_exit_records)} cuts flagged")
        if skipped_rebalances:
            print(f"Rebalance guard: {len(skipped_rebalances)} scheduled rebalance(s) skipped "
                  f"(kept prior book): {skipped_rebalances}")
        return self.positions

    # ──────────────────────────────────────────────────────────────────────────
    # LIVE EXIT SIGNAL EVALUATOR  (identical to csm_batch_strategy.py)
    # ──────────────────────────────────────────────────────────────────────────

    def get_exit_signals(self,
                         portfolio:      dict,
                         live_data:      dict,
                         benchmark_vol:  float = None,
                         today          = None) -> dict:
        import datetime as _dt

        if today is None:
            today = _dt.date.today()
        elif not isinstance(today, _dt.date):
            today = pd.Timestamp(today).date()

        exits: dict = {}
        holds: dict = {}
        crash_guard_fired = False
        high_vol          = False

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

        for ticker, pos in portfolio.items():
            bar = live_data.get(ticker, {})

            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
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

            _atr = float(bar.get('atr', np.nan))
            if pd.isna(_atr) or _atr <= 0:
                _atr = _close * 0.02

            _has_real_hl = ('high' in bar) and ('low' in bar)
            if _has_real_hl and _high == _low:
                _atr_stop = float(pos.get('atr_stop', np.nan))
                holds[ticker] = {
                    'updated_peak'     : float(pos.get('peak_price', _close)),
                    'updated_atr_stop' : _atr_stop,
                    'stop_level'       : _atr_stop,
                }
                continue

            entry_date_raw = pos.get('entry_date', '')
            try:
                _entry_dt  = pd.Timestamp(str(entry_date_raw)[:10]).date()
                _days_held = (today - _entry_dt).days
            except Exception:
                _days_held = 999

            holding_state = {
                'entry_price' : float(pos.get('entry_price', np.nan)),
                'entry_date'  : entry_date_raw,
                'peak_price'  : float(pos.get('peak_price',  _close)),
                'atr_stop'    : float(pos.get('atr_stop',    np.nan)),
                'weight'      : float(pos.get('weight',       0.0)),
            }
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

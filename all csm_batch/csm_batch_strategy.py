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
        self.atr = _tr.ewm(com=self.atr_period - 1, adjust=False).mean().shift(1)

        # Crash-guard regime inputs: 21d benchmark-return vol + its expanding 95th-pct panic
        # threshold (no lookahead). The engine reads _bvol_daily and _panic_threshold_series.
        if self.benchmark is not None:
            bench_ret  = self.benchmark.pct_change(fill_method=None)
            bvol_daily = bench_ret.rolling(window=21).std().shift(1)
            self._panic_threshold_series = bvol_daily.expanding(min_periods=126).quantile(0.95)
            self._panic_threshold        = float(bvol_daily.quantile(0.95))
            self._bvol_daily             = bvol_daily
        else:
            self._panic_threshold        = 1.0
            self._panic_threshold_series = None
            self._bvol_daily             = None

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

    def get_positions(self):
        """
        Monthly cross-sectional ranking with a hysteresis buffer.

        - Absolute-momentum gate: stocks with non-positive 12m return are ineligible.
        - Hysteresis: a held stock stays until its rank drops beyond top_n × (1+buffer_ratio).
        - Dynamic rank-decay exit: cut a held stock whose rank has slid ≥ (drop_frac×top_n)
          from its own best AND is now past (floor_frac×top_n) — flagged RANK_EXIT.
        - Weights: inverse-vol, then a two-pass clip+renorm at max_weight_per_stock.
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
        if self.rebalance_months and int(self.rebalance_months) > 1:
            _n  = int(self.rebalance_months)
            _sn = self.positions.copy()
            _sn.iloc[:] = np.nan
            _sn.iloc[::_n] = self.positions.iloc[::_n]
            self.positions = _sn.ffill().fillna(0.0)

        if _rk_on:
            print(f"Rank-decay exit ON [dynamic top_n-frac]: drop≥{_rk_drop} ranks & rank>{_rk_floor}"
                  f"  →  {len(rank_exit_records)} cuts flagged")
        return self.positions

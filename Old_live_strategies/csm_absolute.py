"""
csm_absolute — Individual-stock momentum strategy CORE.

Strategy logic only: data loader, the IndividualMomentumStrategy class
(signal/universe/factor/position/exit methods), and standalone live tools
(wishlist + entry-signal monitors). No backtest engine, metrics, IC, or
plotting code lives here — see csm_absolute_backtest.py for that, and run_csm_v2.py
for the thin orchestration runner.

Mirrors the momentum_strategy.py organization. Verbatim port of the core
pieces of csm_v2 with dead code and verbose narration
trimmed; strategy/backtest behavior is unchanged.
"""

import pandas as pd
import numpy as np
import os
import glob
import logging

_log = logging.getLogger(__name__)


def load_data(folder_path):
    """
    Loads all CSV files from the specified folder.
    Returns:
        prices_df (pd.DataFrame): Index=Datetime, Columns=Tickers, Values=Close
        volumes_df (pd.DataFrame): Index=Datetime, Columns=Tickers, Values=Volume
        highs_df (pd.DataFrame): Index=Datetime, Columns=Tickers, Values=High
        lows_df (pd.DataFrame): Index=Datetime, Columns=Tickers, Values=Low
        opens_df (pd.DataFrame): Index=Datetime, Columns=Tickers, Values=Open
    """
    all_files = glob.glob(os.path.join(folder_path, "*.csv"))

    if not all_files:
        raise ValueError(f"No CSV files found in {folder_path}")

    price_list = []
    volume_list = []
    high_list = []
    low_list = []
    open_list = []

    print(f"Loading {len(all_files)} files from {folder_path}...")

    for filename in all_files:
        try:
            # Extract symbol from filename (e.g., 'RELIANCE.csv' -> 'RELIANCE')
            symbol = os.path.basename(filename).replace('.csv', '')

            # Read CSV
            df = pd.read_csv(filename, parse_dates=['datetime'], index_col='datetime')

            # Select Close price
            if 'close' in df.columns:
                series = df['close'].rename(symbol)
                # Remove duplicate indices
                series = series[~series.index.duplicated(keep='last')]
                price_list.append(series)
            else:
                print(f"Warning: 'close' column not found in {filename}")

            # Select High
            if 'high' in df.columns:
                h_series = df['high'].rename(symbol)
                h_series = h_series[~h_series.index.duplicated(keep='last')]
                high_list.append(h_series)

            # Select Low
            if 'low' in df.columns:
                l_series = df['low'].rename(symbol)
                l_series = l_series[~l_series.index.duplicated(keep='last')]
                low_list.append(l_series)

            # Select Open
            if 'open' in df.columns:
                o_series = df['open'].rename(symbol)
                o_series = o_series[~o_series.index.duplicated(keep='last')]
                open_list.append(o_series)
            else:
                print(f"Warning: 'open' column not found in {filename}")

            # Select Volume
            if 'volume' in df.columns:
                v_series = df['volume'].rename(symbol)
                v_series = v_series[~v_series.index.duplicated(keep='last')]
                volume_list.append(v_series)

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not price_list:
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

    # Create Wide DataFrames
    prices_df = pd.concat(price_list, axis=1)
    volumes_df = pd.concat(volume_list, axis=1) if volume_list else pd.DataFrame()

    # Sort index
    prices_df.sort_index(inplace=True)
    if not volumes_df.empty:
        volumes_df.sort_index(inplace=True)

    highs_df = pd.concat(high_list, axis=1) if high_list else pd.DataFrame()
    lows_df = pd.concat(low_list, axis=1) if low_list else pd.DataFrame()
    opens_df = pd.concat(open_list, axis=1) if open_list else pd.DataFrame()

    if not highs_df.empty: highs_df.sort_index(inplace=True)
    if not lows_df.empty: lows_df.sort_index(inplace=True)
    if not opens_df.empty: opens_df.sort_index(inplace=True)

    print(f"Loaded Prices: {prices_df.shape}, Volumes: {volumes_df.shape}, Highs: {highs_df.shape}, Opens: {opens_df.shape}")
    return prices_df, volumes_df, highs_df, lows_df, opens_df

class IndividualMomentumStrategy:
    def __init__(self, prices_df, volumes_df, highs_df=None, lows_df=None, opens_df=None, benchmark_series=None,
                 lookback_months=12, lag_months=1,
                 lookback_short_months=None,
                 sharpe_threshold=0.5,
                 universe_top_n=250,
                 capacity_limit=15,
                 leverage_bull=1.0,
                 leverage_bear=0.8,
                 leverage_panic=0.0,
                 max_weight_per_stock=0.15,
                 min_price=20.0,
                 max_circuit_days=5,
                 stop_std_devs=3.0,
                 atr_period=14, atr_multiplier=3.0,
                 use_rebalance=True, rebalance_months=1, use_trailing=True,
                 reentry_cooldown_days=0, rank_buffer=1.0,
                 cooldown_losers_only=False, rank_signal='default',
                 use_take_profit=True, take_profit_gain=0.25, take_profit_size=0.5, **kwargs):

        self.prices = prices_df
        self.volumes = volumes_df
        self.highs = highs_df
        self.lows = lows_df
        self.opens = opens_df
        self.benchmark = benchmark_series

        # Momentum Settings
        self.lookback_months = lookback_months
        self.lag_months = lag_months
        self.sharpe_threshold = sharpe_threshold

        if lookback_short_months is None:
            self.lookback_short_months = max(1, lookback_months // 2)
        else:
            self.lookback_short_months = lookback_short_months

        # Portfolio Constraints
        self.universe_top_n = universe_top_n
        self.capacity_limit = capacity_limit

        self.leverage_bull = leverage_bull
        self.leverage_bear = leverage_bear
        self.leverage_panic = leverage_panic
        self.max_weight_per_stock = max_weight_per_stock

        # Filters
        self.min_price = min_price
        self.max_circuit_days = max_circuit_days

        # Stops
        self.stop_std_devs = stop_std_devs
        self.atr_period = atr_period
        self.atr_multiplier = atr_multiplier

        self.use_rebalance = use_rebalance
        self.rebalance_months = max(1, int(rebalance_months))
        self.use_trailing = use_trailing
        self.reentry_cooldown_days = max(0, int(reentry_cooldown_days))
        self.rank_buffer = max(1.0, float(rank_buffer))
        self.cooldown_losers_only = bool(cooldown_losers_only)
        self.rank_signal = str(rank_signal)
        self._rank_score = None   
        self.use_take_profit  = bool(use_take_profit)
        self.take_profit_gain = float(take_profit_gain)
        self.take_profit_size = float(take_profit_size)

        # Placeholders
        self.factors = None
        self.momentum_returns = None
        self.positions = None
        self.results = None

        print(f"Strategy Initialized: Top {self.capacity_limit} stocks  |  "
              f"Universe: top-{self.universe_top_n} by 63d median dollar-vol  |  "
              f"min_price={self.min_price}")
        print(f"Momentum Windows: Long={self.lookback_months}m, Short={self.lookback_short_months}m, Lag={self.lag_months}m")
        print(f"Toggles: use_rebalance={self.use_rebalance} (every {self.rebalance_months}m)  |  "
              f"use_trailing={self.use_trailing}  |  reentry_cooldown={self.reentry_cooldown_days}d  |  "
              f"rank_buffer={self.rank_buffer}")

    def filter_universe(self, monthly_prices, monthly_volumes, daily_prices):
        """
        DYNAMIC UNIVERSE FILTER - FIXED FOR LOOKAHEAD BIAS
        Instead of a fixed $1M cutoff, we select the Top N stocks by Dollar Volume.
        This adapts automatically to 2005 (lower liquidity) vs 2024 (higher liquidity).

        CRITICAL FIX: All rolling calculations now use .shift(1) to avoid lookahead bias
        """
        # 1. Price Filter (Cheap stocks often have weird liquidity)
        price_mask = monthly_prices.shift(1) > self.min_price

        # 2. Dynamic Liquidity Filter (Top N by Median Dollar Vol) - FIXED
        if self.prices is not None and self.volumes is not None:
             daily_dvol = self.prices * self.volumes

             median_dvol = daily_dvol.rolling(window=63, min_periods=21).median().shift(1)
             monthly_dvol = median_dvol.resample('ME').last()

             # Align
             monthly_dvol = monthly_dvol.reindex(monthly_prices.index)

             # RANKING: Rank descending (1 is highest liquidity)
             # method='min' means ties share the lower rank
             dvol_rank = monthly_dvol.rank(axis=1, ascending=False, method='min')

             # Mask: Keep only Top N (e.g., 2000)
             liquidity_mask = dvol_rank <= self.universe_top_n
        else:
             # Fallback if no daily data
             dollar_vol = monthly_prices * monthly_volumes
             dvol_rank = dollar_vol.rank(axis=1, ascending=False)
             liquidity_mask = dvol_rank <= self.universe_top_n

        # 3. Circuit Breaker Filter (Critical for India) - FIXED
        circuit_mask = pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)
        if self.highs is not None and self.lows is not None:
            # CRITICAL FIX: Shift by 1 day to avoid using current day's circuit data
            is_circuit = (self.highs == self.lows).shift(1)
            circuit_count = is_circuit.rolling(window=63).sum().resample('ME').last()
            circuit_count = circuit_count.reindex(monthly_prices.index).fillna(0)
            circuit_mask = circuit_count <= self.max_circuit_days

        # 4. Trend Filter (SMA 200) - FIXED
        # CRITICAL FIX: Shift SMA by 1 day to avoid using today's price in the average
        sma200_daily = daily_prices.ffill().rolling(window=200, min_periods=150).mean().shift(1)
        is_above_sma = (daily_prices > sma200_daily).shift(1)   # ← extra shift on boolean
        trend_mask   = is_above_sma.resample('ME').last().astype(bool)
        trend_mask   = trend_mask.reindex(monthly_prices.index, fill_value=False)

        # 5. Falling Knife Filter — use PREVIOUS month's return (LOOKAHEAD FIX)
        # monthly_prices.pct_change() at row T = return OF month T (current month).
        # We cannot use the current month's return to decide whether to include a
        # stock in the current month's portfolio — that is lookahead bias.
        # A -15% crash during month T is only known at end of month T, which is
        # exactly when we're computing the signal. The stock would already be held
        # and stopped out by the daily backtest stop logic.
        # Fix: compare against the PREVIOUS month's return (.shift(1)).
        monthly_ret = monthly_prices.pct_change(fill_method=None)
        crash_mask = monthly_ret.shift(1) >= -0.15  # FIXED: prev month's return only

        return price_mask & liquidity_mask & circuit_mask & trend_mask & crash_mask

    def get_positions(self):
        """
        STRICT TOP-N CONCENTRATION
        1. Ranking: Strict Sharpe Ratio.
        2. Size: Hard Cap (e.g., 15 stocks). No buffer/hysteresis.
        3. Weighting: Normalized Inverse Volatility (Risk Parity).
        """
        if self.factors is None: self.calculate_factors()

        print(f"Generating Concentrated Positions (Top {self.capacity_limit})...")

        # Volatility for Sizing - FIXED: Shift before resampling
        daily_ret = self.prices.pct_change(fill_method=None)
        monthly_vol = daily_ret.rolling(21).std().shift(1).resample('ME').last().reindex(self.factors.index)

        # Benchmark Regime (timing handled in backtest)
        bench_monthly = None
        bench_sma = None
        if self.benchmark is not None:
            bench_monthly = self.benchmark.resample('ME').last()
            bench_sma = self.benchmark.rolling(200).mean().shift(1).resample('ME').last()

        position_list = []
        held_peak_prices = {} # For trailing stops
        entry_prices = {} # Track entry prices for take-profit
        take_profit_triggered = {} # Track if take-profit has been triggered
        prev_held = set()

        for date, row_factors in self.factors.iterrows():
            # --- 1. Regime Check (Dynamic Leverage) ---
            current_lev = self.leverage_bull # Default 1.0

            if self.benchmark is not None and date in bench_monthly.index:
                # Panic — use expanding quantile (no lookahead)
                if self.bench_vol_monthly is not None and self._panic_threshold_series is not None:
                    if date in self._panic_threshold_series.index:
                        threshold = self._panic_threshold_series.loc[date]
                    else:
                        threshold = np.inf   # safe fallback: don't trigger
                    if self.bench_vol_monthly.loc[date] > threshold:
                        current_lev = self.leverage_panic

                # Trend
                if bench_monthly.loc[date] < bench_sma.loc[date]:
                    current_lev = min(current_lev, self.leverage_bear)

            # --- 2. Candidate Selection ---
            valid_factors = row_factors.dropna()

            # Absolute Momentum Check (Positive Return)
            if date in self.momentum_returns.index:
                 valid_rets = self.momentum_returns.loc[date]
                 valid_factors = valid_factors[valid_factors.index.isin(valid_rets[valid_rets > 0].index)]

            # Filter by Sharpe Threshold
            candidates = valid_factors[valid_factors > self.sharpe_threshold]

            # --- 3. Strict Ranking (The "No Buffer" Logic) ---
            # Order the gated candidates by the chosen ranking score (default = the
            # dual-Sharpe factor; 'sharpe6' = the IC-validated 6-month Sharpe). The
            # GATE above is unchanged, so only the top-N pick order changes.
            if self._rank_score is not None and date in self._rank_score.index:
                ranked_candidates = (self._rank_score.loc[date, candidates.index]
                                     .fillna(-np.inf).sort_values(ascending=False))
            else:
                ranked_candidates = candidates.sort_values(ascending=False)

            # Take Top N (e.g. 15)
            # We iterate to fill 15 slots, checking Stops on the fly
            final_selection = []

            # --- 3b. Selection hysteresis / buffering ---
            # rank_buffer == 1.0 -> strict top-N (iterate by pure rank, current behavior).
            # rank_buffer  > 1.0 -> a currently-HELD name keeps priority for its slot as
            #   long as it still ranks within capacity_limit * rank_buffer; only then do
            #   new names fill the remaining slots. This avoids swapping a holding out for
            #   a marginally-better newcomer every month -> lower signal turnover.
            if self.rank_buffer > 1.0 and prev_held:
                _ranks = {s: r for r, s in enumerate(ranked_candidates.index, start=1)}
                _exit_rank = int(round(self.capacity_limit * self.rank_buffer))
                _held_keep = [s for s in ranked_candidates.index
                              if s in prev_held and _ranks[s] <= _exit_rank]
                _new_names = [s for s in ranked_candidates.index if s not in prev_held]
                iteration_order = _held_keep + _new_names
            else:
                iteration_order = list(ranked_candidates.index)

            for stock in iteration_order:
                if len(final_selection) >= self.capacity_limit:
                    break

                # --- Trailing Stop Check ---
                # Even if it's Rank #1, if it hit a stop this month, we skip it.
                # (This is a "simulated" intra-month stop)
                try:
                    price_curr = self.prices.at[date, stock] # Current price (approx month end)

                    if stock in prev_held:
                         peak = held_peak_prices.get(stock, price_curr)

                         # Use PREVIOUS month's data to avoid lookahead
                         date_idx = self.monthly_highs.index.get_loc(date)
                         if date_idx > 0:
                             prev_date = self.monthly_highs.index[date_idx - 1]

                             # Update Peak with PREVIOUS month's high
                             if hasattr(self, 'monthly_highs'):
                                 high_prev = self.monthly_highs.at[prev_date, stock]
                                 peak = max(peak, high_prev)
                             else:
                                 peak = max(peak, price_curr)

                             held_peak_prices[stock] = peak

                             # Chandelier Stop Calc using PREVIOUS month's ATR
                             atr = self.monthly_atr.at[prev_date, stock] if hasattr(self, 'monthly_atr') else (price_curr * 0.02)

                             # If take-profit triggered, use breakeven stop instead of chandelier
                             if take_profit_triggered.get(stock, False):
                                 stop_price = entry_prices.get(stock, price_curr)  # Breakeven stop
                             else:
                                 stop_price = peak - (self.atr_multiplier * atr)  # Chandelier stop

                             # Check PREVIOUS month's low against stop
                             if hasattr(self, 'monthly_lows'):
                                 low_prev = self.monthly_lows.at[prev_date, stock]
                                 if low_prev < stop_price and self.use_trailing:
                                     # STOP HIT (trailing): skip this candidate this month.
                                     # Gated by use_trailing so the selection-time
                                     # trailing stop can be turned off for A/B testing.
                                     continue
                         else:
                             # First month, no previous data - skip stop check
                             pass
                    else:
                         # New Entry
                         held_peak_prices[stock] = price_curr
                         entry_prices[stock] = price_curr
                         take_profit_triggered[stock] = False
                except:
                    pass # Data missing, skip check

                final_selection.append(stock)

            # --- 4. Check Take-Profit (25% gain) ---
            for stock in final_selection:
                if stock in entry_prices and stock in prev_held:
                    try:
                        entry_price = entry_prices[stock]
                        current_price = self.prices.at[date, stock]
                        gain = (current_price / entry_price) - 1

                        # Trigger take-profit at the configured gain (if enabled)
                        if (self.use_take_profit and gain >= self.take_profit_gain
                                and not take_profit_triggered.get(stock, False)):
                            take_profit_triggered[stock] = True
                    except:
                        pass

            # --- 5. Smart Weighting (Normalized Risk Parity) ---
            if not final_selection:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # Get Vols for selected stocks
            sel_vols = monthly_vol.loc[date, final_selection].fillna(0.02)
            sel_vols = sel_vols.replace(0, 0.02)

            # Inverse Volatility
            inv_vols = 1.0 / sel_vols

            # Normalize to 1.0 (100% Equity)
            # Weights = (1/Vol_i) / Sum(1/Vol_all)
            raw_weights = inv_vols / inv_vols.sum()

            # Apply Take-Profit size reduction
            for stock in final_selection:
                if take_profit_triggered.get(stock, False):
                    raw_weights[stock] *= self.take_profit_size

            # Apply Leverage & Caps
            final_w = raw_weights * current_lev

            # Cap individual stocks (e.g., max 15% or 20%) to prevent single stock concentration
            final_w = final_w.clip(upper=self.max_weight_per_stock)

            # Re-normalize if clipping reduced exposure?
            # Usually safer to just leave it (implies slight cash buffer if one stock was huge)

            # Save
            full_weights = pd.Series(0.0, index=self.factors.columns, name=date)
            full_weights.update(final_w)
            position_list.append(full_weights)

            prev_held = set(final_selection)
            # Clean up tracking dicts for stocks we no longer hold
            held_peak_prices = {k: v for k, v in held_peak_prices.items() if k in prev_held}
            entry_prices = {k: v for k, v in entry_prices.items() if k in prev_held}
            take_profit_triggered = {k: v for k, v in take_profit_triggered.items() if k in prev_held}

        self.positions = pd.concat(position_list, axis=1).T
        self.positions.index = self.factors.index

        # ── Rebalance cadence control (defaults are a no-op) ──────────────
        # use_rebalance=False : freeze to the FIRST non-empty basket. The engine
        #   forward-fills it forever, so no re-rank ever fires REBALANCE/SIGNAL_DROP
        #   exits; combined with the engine's no-re-entry guard each name is held
        #   until a stop/crash-guard exits it, then dropped (capital -> cash).
        # rebalance_months=N>1 : keep only every Nth month-end target; the engine
        #   forward-fills monthly->daily so the basket holds for N months.
        if not self.use_rebalance:
            _nonempty = self.positions.index[self.positions.abs().sum(axis=1) > 0]
            if len(_nonempty) > 0:
                self.positions = self.positions.loc[[_nonempty[0]]]
            print(f"[Rebalance] use_rebalance=False -> frozen first basket "
                  f"({self.positions.index[0].date() if len(self.positions) else 'n/a'}), hold-until-stop")
        elif self.rebalance_months > 1:
            self.positions = self.positions.iloc[::self.rebalance_months]
            print(f"[Rebalance] rebalance_months={self.rebalance_months} -> "
                  f"{len(self.positions)} rebalance dates (every {self.rebalance_months}m)")

        return self.positions

    def apply_regime_bias(self, ticker, current_regime):
        """
        Placeholder for Regime Bias.
        Adjusts thresholds based on market regime.
        """
        # Example logic (Placeholder):
        # If in Bear regime, tighten entry thresholds
        if current_regime == 'BEAR':
            return 1.2 * self.sharpe_threshold # Require stronger signal
        return self.sharpe_threshold

    def calculate_factors(self):
        """
        CORRECTED VERSION - NO LOOKAHEAD BIAS

        Calculate momentum factors using a 12-month lookback with 1-month lag.
        Ranking metric: Sharpe Ratio = Return / Volatility

        CRITICAL FIXES:
        1. Monthly prices are shifted by 1 period before calculations
        2. All rolling indicators use .shift(1) before resampling
        3. Benchmark SMA uses .shift(1)
        """
        print("Calculating Momentum Factors (TIMING FIXED)...")

        # Get month-end prices (signals will be executed NEXT trading day)
        monthly_prices = self.prices.resample('ME').last()

        # For volume, use mean
        if not self.volumes.empty:
            monthly_volumes = self.volumes.resample('ME').mean()
            # Calculate dollar volume for filtering
            monthly_avg_dvol = monthly_prices * monthly_volumes
        else:
            monthly_volumes = None
            monthly_avg_dvol = None

        # Shared base: monthly returns for volatility calculations
        monthly_ret = monthly_prices.pct_change(fill_method=None)

        # ── 1. LONG Momentum Factor (e.g. 9-month) ──────────────────────────
        # Return window: P(t-lag) / P(t-lag-lookback) - 1
        num_long = monthly_prices.shift(self.lag_months)
        den_long = monthly_prices.shift(self.lag_months + self.lookback_months)
        ret_long = (num_long / den_long) - 1

        # Volatility over long window, shifted by lag to avoid lookahead
        vol_long = monthly_ret.rolling(window=self.lookback_months).std().shift(self.lag_months)
        annualized_vol_long = vol_long * np.sqrt(12)

        factor_long = ret_long / annualized_vol_long.replace(0, np.nan)

        # ── 2. SHORT Momentum Factor (e.g. 4-month) ──────────────────────────
        # Captures recent acceleration; uses same lag for consistency
        num_short = monthly_prices.shift(self.lag_months)
        den_short = monthly_prices.shift(self.lag_months + self.lookback_short_months)
        ret_short = (num_short / den_short) - 1

        # Volatility over short window, shifted by lag
        vol_short = monthly_ret.rolling(window=self.lookback_short_months).std().shift(self.lag_months)
        annualized_vol_short = vol_short * np.sqrt(12)

        factor_short = ret_short / annualized_vol_short.replace(0, np.nan)

        # ── 3. Combined Factor: Equal-weight average of long + short ─────────
        # Both legs must agree to score highly. A stock with strong long-term
        # momentum but recent deceleration will rank lower than in v2_1 alone.
        self.factors = (factor_long + factor_short) / 2.0

        # Absolute momentum check uses LONG-term return (trend definition)
        self.momentum_returns = ret_long

        # ── 4. Clip Factors (Safety) ─────────────────────────────────────────
        self.factors = self.factors.clip(upper=5.0, lower=-5.0)

        # 5. Apply Universe Filter
        valid_universe = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)
        self.factors = self.factors.where(valid_universe)
        self.momentum_returns = self.momentum_returns.where(valid_universe)

        # Drop rows where everything is NaN
        self.factors.dropna(how='all', inplace=True)
        self.momentum_returns.dropna(how='all', inplace=True)

        # ── Alternative ranking score (orders the gated pool; gate stays dual-Sharpe) ──
        # IC-validated on the gated pool (see csm_absolute_signal_bakeoff.py).
        if self.rank_signal == 'sharpe6':
            ret_6 = (monthly_prices.shift(self.lag_months)
                     / monthly_prices.shift(self.lag_months + 6)) - 1
            vol_6 = monthly_ret.rolling(window=6).std().shift(self.lag_months)
            s6 = ret_6 / (vol_6 * np.sqrt(12)).replace(0, np.nan)
            self._rank_score = s6.where(valid_universe).reindex(self.factors.index)
        else:
            self._rank_score = None

        # --- Benchmark / Regime Prep - FIXED ---
        if self.benchmark is not None:
            bench_ret = self.benchmark.pct_change(fill_method=None)
            # CRITICAL FIX: Shift volatility to avoid using today's crash data
            bench_vol_daily = bench_ret.rolling(window=21).std().shift(1)
            self._bench_vol_daily = bench_vol_daily
            self.panic_threshold = bench_vol_daily.quantile(0.95)   # kept for legacy reference only
            self._panic_threshold_series = bench_vol_daily.expanding(min_periods=126).quantile(0.95)
            self.bench_vol_monthly = bench_vol_daily.resample('ME').last()
        else:
            self.bench_vol_monthly = None
            self.panic_threshold = 1.0
            self._bench_vol_daily = None
            self._panic_threshold_series = None

        # --- Pre-Calculate Indicators for Exits ---
        if self.highs is not None and self.lows is not None:
            self.monthly_highs = self.highs.resample('ME').max()
            self.monthly_lows = self.lows.resample('ME').min()
            self.monthly_closes = monthly_prices

            # ATR Calculation
            prev_close = self.prices.shift(1)
            tr = np.maximum(self.highs - self.lows,
                   np.maximum((self.highs - prev_close).abs(), (self.lows - prev_close).abs()))
            self.atr_daily = tr.rolling(window=self.atr_period).mean()
            self.monthly_atr = self.atr_daily.resample('ME').last()

            # Reindex to match
            self.monthly_highs = self.monthly_highs.reindex(monthly_prices.index)
            self.monthly_lows = self.monthly_lows.reindex(monthly_prices.index)
            self.monthly_atr = self.monthly_atr.reindex(monthly_prices.index)

        # CRITICAL FIX: Shift SMA200 by 1 day before resampling
        sma200_daily = self.prices.ffill().rolling(window=200).mean().shift(1)
        self.monthly_sma200 = sma200_daily.resample('ME').last()
        self.monthly_sma200 = self.monthly_sma200.reindex(monthly_prices.index)

        return self.factors

    def get_exit_signals(self,
                         portfolio:              dict,
                         live_data:              dict,
                         benchmark_close:        float = None,
                         benchmark_sma200:       float = None,
                         hard_stop_from_entry_pct: float = 0.15,
                         hard_stop_from_peak_pct:  float = 0.20,
                         stop_slippage_pct:        float = 0.003) -> dict:
        """
        Evaluate all exit rules for currently held positions on one live bar.

        Mirrors _run_event_backtest() STEP C and STEP E exactly:
          • STEP C — Crash Guard  : if benchmark_close < benchmark_sma200,
                                    exit every held position immediately.
                                    Fill applies the stop-floor improvement:
                                    if the low has already breached the stop
                                    level, use the better stop fill rather
                                    than the raw close.
          • STEP E — Per-stock   : three-layer stop check (chandelier + entry
                                    hard + peak hard) triggered via intraday low.

        NOT covered here (caller is responsible):
          • Rebalance / Signal-Drop exits — diff get_positions() output.
          • Correlation Guard             — scale-only; does not trigger exits.
          • Limit Order Manager           — advanced approach orders (separate class).

        Parameters
        ----------
        portfolio : dict
            ticker → {
                'entry_price' : float,    # price at which position was entered
                'peak_price'  : float,    # highest daily HIGH seen since entry
                                          # (MUST be persisted by caller and
                                          #  updated each bar — see 'holds' below)
                'weight'      : float,    # current portfolio weight (informational)
            }
        live_data : dict
            ticker → {
                'close' : float,          # required
                'high'  : float,          # optional; used for peak update
                'low'   : float,          # optional; stop trigger price
                'open'  : float,          # optional; determines gap-down fill
                'atr'   : float,          # optional; defaults to close × 0.02
                                          # caller should pre-cap ATR at its
                                          # rolling 75th-pct to match backtest
            }
        benchmark_close  : float, optional
            Today's benchmark index close.  If None, Crash Guard is skipped.
        benchmark_sma200 : float, optional
            Today's 200-day SMA of the benchmark.  Crash Guard fires when
            benchmark_close < benchmark_sma200.
        hard_stop_from_entry_pct : float
            Layer-2 hard stop: exit when close < entry_price × (1 − pct).
            Default 0.15 (−15%) — matches _run_event_backtest default.
        hard_stop_from_peak_pct : float
            Layer-3 hard stop: exit when close < peak_high × (1 − pct).
            Default 0.20 (−20%) — matches _run_event_backtest default.
        stop_slippage_pct : float
            Slippage applied on intraday stop fills (not gap-down fills).
            Default 0.003 (0.3%) — matches _run_event_backtest default.

        Returns
        -------
        dict with three keys:
            'exits' : dict
                ticker → {
                    'reason'      : str,   # 'CRASH_GUARD' | 'STOP_HIT'
                    'fill_price'  : float, # estimated fill (open or stop × (1−slip))
                    'stop_level'  : float, # effective stop at time of exit
                }
            'holds' : dict
                ticker → {
                    'updated_peak' : float, # new peak after today's high — PERSIST THIS
                    'stop_level'   : float, # current effective stop (for monitoring)
                }
            'crash_guard_fired' : bool
            'high_vol'          : bool   # always False (csm_v2 has no vol-regime detection)

        Usage notes
        -----------
        • Persist `result['holds'][ticker]['updated_peak']` back into
          `portfolio[ticker]['peak_price']` on every bar — the chandelier stop
          anchors to the running peak high, which must accumulate correctly.
        • Pass a real pre-capped ATR value in live_data[ticker]['atr'] where
          possible.  The default close × 2% fallback widens the chandelier
          significantly in low-vol stocks.
        • The crash guard uses YESTERDAY's SMA200 (caller should shift before
          passing) to match the backtest's pre-shifted is_bearish series.
        """
        exits: dict = {}
        holds: dict = {}
        crash_guard_fired = False

        # ── STEP C: Crash Guard — SMA-200 regime ──────────────────────────────
        if (benchmark_close is not None and benchmark_sma200 is not None
                and benchmark_close < benchmark_sma200):
            crash_guard_fired = True

            for ticker, pos in portfolio.items():
                bar        = live_data.get(ticker, {})
                _close     = float(bar.get('close', np.nan))
                _low       = float(bar.get('low',   _close if pd.notna(_close) else np.nan))
                _open      = float(bar.get('open',  _close if pd.notna(_close) else np.nan))
                _atr       = float(bar.get('atr',   np.nan))

                # BUG-3 FIX: skip positions with missing price data instead of
                # cascading _close = 0.0 through _low/_open/_peak → fill_price=0.
                # A ₹0 exit is an impossible broker fill and creates ghost positions
                # (system marks exit while broker rejects the order).
                # Mirrors STEP E line ~794: "if pd.isna(_close) or _close <= 0: continue"
                if pd.isna(_close) or _close <= 0:
                    _log.warning(
                        "get_exit_signals [CRASH_GUARD]: %s has no usable price "
                        "in live_data — position NOT added to exits; "
                        "exit it MANUALLY via the broker UI",
                        ticker,
                    )
                    continue    # no usable price — skip; position stays held
                if pd.isna(_low)  or _low  <= 0: _low  = _close
                if pd.isna(_open) or _open <= 0: _open = _close
                if pd.isna(_atr)  or _atr  <= 0: _atr  = _close * 0.02

                _entry = float(pos.get('entry_price', np.nan))
                _peak  = float(pos.get('peak_price',  _close))   # 'peak_high' was wrong key

                # Stop-floor improvement: if low already breached stop, use
                # the better stop fill rather than the worse raw close
                # (mirrors the STOP-FLOOR FIX in _run_event_backtest STEP C)
                cg_fill     = _close    # default: exit at close
                eff_stop_cg = np.nan
                if pd.notna(_entry) and _entry > 0 and _peak > 0:
                    _chand      = _peak - (self.atr_multiplier * _atr)
                    _entry_stop = _entry * (1.0 - hard_stop_from_entry_pct)
                    _peak_stop  = _peak  * (1.0 - hard_stop_from_peak_pct)
                    eff_stop_cg = max(_chand, _entry_stop, _peak_stop)
                    if _low <= eff_stop_cg:
                        # Stop was breached intraday — compute stop fill
                        if _open <= eff_stop_cg:
                            _stop_fill = _open    # gap-down
                        else:
                            _stop_fill = eff_stop_cg * (1.0 - stop_slippage_pct)
                        # Take the BETTER of stop fill and close (never worse than close)
                        cg_fill = max(_stop_fill, _close)

                exits[ticker] = {
                    'reason'     : 'CRASH_GUARD',
                    'fill_price' : float(cg_fill) if pd.notna(cg_fill) else np.nan,
                    'stop_level' : float(eff_stop_cg) if pd.notna(eff_stop_cg) else np.nan,
                }

            return {
                'exits'             : exits,
                'holds'             : {},
                'crash_guard_fired' : True,
                'high_vol'          : False,
            }

        # ── STEP E: Per-stock three-layer stop check ───────────────────────────
        for ticker, pos in portfolio.items():
            bar = live_data.get(ticker, {})

            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
                continue    # no usable price — skip

            _high  = float(bar.get('high', _close))
            _low   = float(bar.get('low',  _close))
            _open  = float(bar.get('open', _close))
            _atr   = float(bar.get('atr',  np.nan))

            if pd.isna(_high) or _high <= 0: _high = _close
            if pd.isna(_low)  or _low  <= 0: _low  = _close
            if pd.isna(_open) or _open <= 0: _open = _close
            if pd.isna(_atr)  or _atr  <= 0: _atr  = _close * 0.02   # 2% fallback

            _entry = float(pos.get('entry_price', np.nan))
            _peak  = float(pos.get('peak_price',  _close))

            if pd.isna(_entry) or _entry <= 0:
                # BUG-2 FIX: warn and fall back to close instead of silently
                # holding with stop_level=NaN.  Without this, a position whose
                # avg_buy_price was never persisted in portfolio.json bypasses
                # ALL three stop layers indefinitely — the "ghost position" bug.
                #
                # Mirrors _run_event_backtest STEP E defensive init (lines ~1457-1460):
                #   if stock not in entry_prices:
                #       entry_prices[stock] = today_close    ← same fallback
                _log.warning(
                    "get_exit_signals: %s has entry_price=%.2f — "
                    "falling back to current close ₹%.2f; "
                    "fix avg_buy_price in portfolio.json to restore correct stops",
                    ticker, float(_entry) if pd.notna(_entry) else 0.0, _close,
                )
                _entry = _close   # conservative proxy; stop layers will compute from here

            # ── Three-layer effective stop ────────────────────────────────────
            # L1 Chandelier : peak_high - atr_multiplier × ATR
            # L2 Entry hard : entry_price × (1 - hard_stop_from_entry_pct)
            # L3 Peak hard  : peak_high  × (1 - hard_stop_from_peak_pct)
            # effective_stop = max(L1, L2, L3)   [highest price = tightest stop]
            chandelier_stop  = _peak - (self.atr_multiplier * _atr)
            entry_hard_stop  = _entry * (1.0 - hard_stop_from_entry_pct)
            peak_hard_stop   = _peak  * (1.0 - hard_stop_from_peak_pct)
            effective_stop   = max(chandelier_stop, entry_hard_stop, peak_hard_stop)

            # ── Trigger: checked via intraday LOW ─────────────────────────────
            if _low > effective_stop:
                # Stop not touched — hold, update peak with today's high
                _new_peak = max(_peak, _high)
                holds[ticker] = {
                    'updated_peak' : _new_peak,
                    'stop_level'   : float(effective_stop),
                }
                continue

            # ── Stop triggered ────────────────────────────────────────────────
            # Fill: gap-down (open ≤ stop) → fill at open
            #       intraday breach        → fill at stop × (1 − slippage)
            if _open <= effective_stop:
                fill_px = _open                                           # gap-down
            else:
                fill_px = effective_stop * (1.0 - stop_slippage_pct)    # intraday

            exits[ticker] = {
                'reason'     : 'STOP_HIT',
                'fill_price' : float(fill_px),
                'stop_level' : float(effective_stop),
            }

        return {
            'exits'             : exits,
            'holds'             : holds,
            'crash_guard_fired' : crash_guard_fired,
            'high_vol'          : False,   # csm_v2 has no vol-regime detection
        }


# ──────────────────────────────────────────────────────────────────────────
# LIVE TOOLS — wishlist generation + entry-signal monitoring
# ──────────────────────────────────────────────────────────────────────────

def generate_momentum_wishlist(prices_df, volumes_df, benchmark_series=None,
                                lookback_months=9, lag_months=1,
                                sharpe_threshold=0.3, min_return_threshold=0.05,
                                wishlist_size=250, min_price=20.0, min_dollar_vol=1e7):
    """
    Generate a ranked wishlist of stocks currently showing momentum signals.
    This function can be called independently to get real-time momentum candidates.

    Args:
        prices_df (pd.DataFrame): Daily OHLCV prices (Close column)
        volumes_df (pd.DataFrame): Daily volumes
        benchmark_series (pd.Series): Benchmark for trend filter (optional)
        lookback_months (int): Momentum lookback period (default: 9)
        lag_months (int): Momentum lag period (default: 1)
        sharpe_threshold (float): Minimum Sharpe ratio for inclusion (default: 0.3)
        min_return_threshold (float): Minimum return requirement (default: 5%)
        wishlist_size (int): Target number of stocks in wishlist (default: 250)
        min_price (float): Minimum stock price filter (default: 20)
        min_dollar_vol (float): Minimum daily dollar volume (default: 10M)

    Returns:
        pd.DataFrame: Ranked wishlist with columns:
            - Ticker: Stock symbol
            - Momentum_Score: Risk-adjusted momentum (Sharpe Ratio)
            - Raw_Return: 12m return
            - Volatility: 12m rolling volatility
            - Current_Price: Latest available price
            - Avg_Dollar_Volume: Average daily dollar volume
            - Days_Since_Peak: Days from 52-week high
            - Rank: Final rank (1 = best)
    """
    import pandas as pd
    import numpy as np

    print(f"\n{'='*50}")
    print("MOMENTUM WISHLIST GENERATOR")
    print(f"{'='*50}")
    print(f"Universe Size: {len(prices_df.columns)} stocks")
    print(f"Target Wishlist: {wishlist_size} stocks")
    print(f"Date Range: {prices_df.index.min()} to {prices_df.index.max()}")

    # Get the most recent date with data
    latest_date = prices_df.index[-1]
    print(f"Analysis Date: {latest_date}")

    # 1. Resample to Monthly for momentum calculation
    monthly_prices = prices_df.resample('ME').last()
    monthly_volumes = volumes_df.resample('ME').sum()

    # Fix last date mismatch (same as in calculate_factors)
    if not prices_df.empty and not monthly_prices.empty:
        last_real_date = prices_df.index[-1]
        last_resampled_date = monthly_prices.index[-1]

        if last_resampled_date > last_real_date:
            new_index = list(monthly_prices.index)
            new_index[-1] = last_real_date
            monthly_prices.index = pd.Index(new_index)

            if len(monthly_volumes) == len(monthly_prices):
                monthly_volumes.index = monthly_prices.index

    # 2. Calculate Momentum Metrics
    # Return: (P(t-lag) / P(t-lookback)) - 1
    numerator = monthly_prices.shift(lag_months)
    denominator = monthly_prices.shift(lookback_months)
    momentum_returns = (numerator / denominator) - 1

    # Volatility: 12-month rolling std of monthly returns
    monthly_ret = monthly_prices.pct_change(fill_method=None)
    rolling_vol = monthly_ret.rolling(window=lookback_months).std()

    # Sharpe Ratio (Risk-Adjusted Momentum)
    momentum_sharpe = momentum_returns / rolling_vol.replace(0, np.nan)
    momentum_sharpe = momentum_sharpe.clip(upper=5.0, lower=-5.0)

    # 3. Apply Universe Filters
    # Get latest row of metrics
    latest_sharpe = momentum_sharpe.iloc[-1]
    latest_return = momentum_returns.iloc[-1]
    latest_vol = rolling_vol.iloc[-1]
    latest_price = prices_df.iloc[-1]

    # Calculate average dollar volume (last 21 days)
    recent_prices = prices_df.iloc[-21:]
    recent_volumes = volumes_df.iloc[-21:]
    avg_dollar_vol = (recent_prices * recent_volumes).mean()

    # Price Filter
    price_mask = latest_price > min_price

    # Liquidity Filter
    liquidity_mask = avg_dollar_vol > min_dollar_vol

    # Trend Filter: Price > 200-day SMA
    sma200 = prices_df.ffill().rolling(window=200, min_periods=180).mean().iloc[-1]
    trend_mask = latest_price > sma200

    # Monthly Stop-Loss: Last month return > -15%
    last_month_ret = monthly_ret.iloc[-1]
    stop_loss_mask = (last_month_ret >= -0.15) | (last_month_ret.isna())

    # Combine all filters
    valid_universe = price_mask & liquidity_mask & trend_mask & stop_loss_mask

    print(f"\nFiltering Universe:")
    print(f"  Price > {min_price}: {price_mask.sum()} stocks")
    print(f"  Liquidity > {min_dollar_vol/1e6:.1f}M: {liquidity_mask.sum()} stocks")
    print(f"  Above 200-day SMA: {trend_mask.sum()} stocks")
    print(f"  No Stop-Loss Hit: {stop_loss_mask.sum()} stocks")
    print(f"  Combined Valid Universe: {valid_universe.sum()} stocks")

    # 4. Signal Filters (Momentum Quality)
    # Positive return requirement
    positive_return = latest_return > min_return_threshold

    # Sharpe threshold
    strong_sharpe = latest_sharpe > sharpe_threshold

    # Combined momentum signal
    momentum_signal = valid_universe & positive_return & strong_sharpe

    print(f"\nMomentum Signals:")
    print(f"  Return > {min_return_threshold*100:.0f}%: {positive_return.sum()} stocks")
    print(f"  Sharpe > {sharpe_threshold}: {strong_sharpe.sum()} stocks")
    print(f"  Combined Momentum Signal: {momentum_signal.sum()} stocks")

    # 5. Build Wishlist DataFrame
    candidates = momentum_signal[momentum_signal].index.tolist()

    if len(candidates) == 0:
        print("\n⚠️  WARNING: No stocks meet momentum criteria!")
        return pd.DataFrame()

    wishlist_data = []

    for ticker in candidates:
        # Calculate additional metrics
        # Days since 52-week high
        high_52w = prices_df[ticker].iloc[-252:].max() if len(prices_df) >= 252 else prices_df[ticker].max()
        current_price = latest_price[ticker]
        days_since_peak = 0

        # Find last occurrence of 52w high
        high_dates = prices_df[ticker].iloc[-252:][prices_df[ticker].iloc[-252:] == high_52w].index
        if len(high_dates) > 0:
            days_since_peak = (latest_date - high_dates[-1]).days

        wishlist_data.append({
            'Ticker': ticker,
            'Momentum_Score': latest_sharpe[ticker],
            'Raw_Return': latest_return[ticker],
            'Volatility': latest_vol[ticker],
            'Current_Price': current_price,
            'Avg_Dollar_Volume': avg_dollar_vol[ticker],
            'Days_Since_Peak': days_since_peak,
            'Distance_From_Peak': (current_price / high_52w - 1) if high_52w > 0 else 0
        })

    wishlist_df = pd.DataFrame(wishlist_data)

    # 6. Rank by Momentum Score (Sharpe Ratio)
    wishlist_df = wishlist_df.sort_values('Momentum_Score', ascending=False)
    wishlist_df['Rank'] = range(1, len(wishlist_df) + 1)

    # 7. Trim to target size
    if len(wishlist_df) > wishlist_size:
        print(f"\n✂️  Trimming wishlist from {len(wishlist_df)} to {wishlist_size} stocks")
        wishlist_df = wishlist_df.head(wishlist_size)

    # 8. Summary Statistics
    print(f"\n{'='*50}")
    print("WISHLIST SUMMARY")
    print(f"{'='*50}")
    print(f"Total Stocks: {len(wishlist_df)}")
    print(f"\nMomentum Score (Sharpe):")
    print(f"  Mean: {wishlist_df['Momentum_Score'].mean():.2f}")
    print(f"  Median: {wishlist_df['Momentum_Score'].median():.2f}")
    print(f"  Min: {wishlist_df['Momentum_Score'].min():.2f}")
    print(f"  Max: {wishlist_df['Momentum_Score'].max():.2f}")
    print(f"\nRaw Returns:")
    print(f"  Mean: {wishlist_df['Raw_Return'].mean()*100:.2f}%")
    print(f"  Median: {wishlist_df['Raw_Return'].median()*100:.2f}%")
    print(f"  Min: {wishlist_df['Raw_Return'].min()*100:.2f}%")
    print(f"  Max: {wishlist_df['Raw_Return'].max()*100:.2f}%")
    print(f"\nPrice Range:")
    print(f"  Min: ₹{wishlist_df['Current_Price'].min():.2f}")
    print(f"  Max: ₹{wishlist_df['Current_Price'].max():.2f}")
    print(f"  Median: ₹{wishlist_df['Current_Price'].median():.2f}")

    # 9. Display Top 10
    print(f"\n{'='*50}")
    print("TOP 10 MOMENTUM STOCKS")
    print(f"{'='*50}")
    print(wishlist_df.head(10)[['Rank', 'Ticker', 'Momentum_Score', 'Raw_Return', 'Current_Price']].to_string(index=False))

    return wishlist_df


def save_wishlist_to_csv(wishlist_df, filename='momentum_wishlist.csv'):
    """
    Save wishlist to CSV file for external use.

    Args:
        wishlist_df (pd.DataFrame): Wishlist from generate_momentum_wishlist()
        filename (str): Output CSV filename
    """
    if wishlist_df.empty:
        print("⚠️  Wishlist is empty, nothing to save.")
        return

    wishlist_df.to_csv(filename, index=False)
    print(f"\n✅ Wishlist saved to '{filename}'")
    print(f"   {len(wishlist_df)} stocks ready for live trading")


def monitor_entry_signals(stock_list, prices_df, volumes_df, benchmark_series=None,
                          lookback_months=9, lag_months=1,
                          sharpe_threshold=0.5, min_return_threshold=0.0,
                          min_price=20.0, min_dollar_vol=1e7,
                          target_daily_risk=0.01, max_weight_per_stock=0.12,
                          leverage_bull=1.5, leverage_bear=0.8, leverage_panic=0.5):
    """
    Monitor specific stocks for ENTRY signals based on momentum strategy criteria.

    This function evaluates each stock in your watchlist and tells you:
    - Whether to ENTER NOW or WAIT
    - What price to enter at
    - How much allocation (% of portfolio)
    - Why the signal is triggered (or why not)

    Args:
        stock_list (list): List of ticker symbols to monitor (e.g., ['RELIANCE', 'TCS', 'INFY'])
        prices_df (pd.DataFrame): Full universe daily prices
        volumes_df (pd.DataFrame): Full universe daily volumes
        benchmark_series (pd.Series): Benchmark for regime detection
        lookback_months (int): Momentum lookback (default: 9)
        lag_months (int): Momentum lag (default: 1)
        sharpe_threshold (float): Entry threshold (default: 0.5)
        min_return_threshold (float): Minimum return filter (default: 0%)
        min_price (float): Price filter (default: 20)
        min_dollar_vol (float): Liquidity filter (default: 10M)
        target_daily_risk (float): Risk per stock for sizing (default: 1%)
        max_weight_per_stock (float): Max allocation per stock (default: 12%)
        leverage_bull/bear/panic (float): Regime-based leverage limits

    Returns:
        pd.DataFrame: Entry signals with columns:
            - Ticker: Stock symbol
            - Signal: ENTER NOW | WAIT | NOT READY
            - Entry_Price: Current/recommended entry price
            - Recommended_Allocation: % of portfolio to allocate
            - Sharpe_Ratio: Current momentum score
            - Raw_Return: 9-month return
            - Volatility: Daily volatility
            - Regime: Bull/Bear/Panic market state
            - Checks: Detailed pass/fail for each criterion
            - Reason: Human-readable explanation
    """
    import pandas as pd
    import numpy as np
    from datetime import datetime

    print(f"\n{'='*60}")
    print(f"ENTRY SIGNAL MONITOR - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}")
    print(f"Monitoring {len(stock_list)} stocks for entry signals")
    print(f"Strategy: {lookback_months}m momentum, Sharpe > {sharpe_threshold}")

    # Validate stocks exist in data
    available_stocks = [s for s in stock_list if s in prices_df.columns]
    missing_stocks = [s for s in stock_list if s not in prices_df.columns]

    if missing_stocks:
        print(f"\nWARNING: {len(missing_stocks)} stocks not found in data:")
        print(f"   {', '.join(missing_stocks)}")

    if not available_stocks:
        print("\nERROR: No valid stocks to monitor!")
        return pd.DataFrame()

    print(f"Found {len(available_stocks)} stocks in dataset")

    # Get latest date
    latest_date = prices_df.index[-1]
    print(f"Analysis Date: {latest_date.strftime('%Y-%m-%d')}")

    # ========== STEP 1: Calculate Momentum Metrics ==========

    # Filter prices and volumes to available stocks only
    prices_subset = prices_df[available_stocks].copy()
    volumes_subset = volumes_df[available_stocks].copy()

    sma200_full = prices_subset.ffill().rolling(window=200, min_periods=180).mean()

    # Resample to monthly
    monthly_prices = prices_subset.resample('ME').last()
    monthly_volumes = volumes_subset.resample('ME').sum()

    # Fix date mismatch
    if not monthly_prices.empty:
        last_real_date = prices_subset.index[-1]
        last_resampled_date = monthly_prices.index[-1]

        if last_resampled_date > last_real_date:
            new_index = list(monthly_prices.index)
            new_index[-1] = last_real_date
            monthly_prices.index = pd.Index(new_index)
            monthly_volumes.index = monthly_prices.index

    # Momentum Return: (P(t-lag) / P(t-lookback)) - 1
    numerator = monthly_prices.shift(lag_months)
    denominator = monthly_prices.shift(lookback_months)
    momentum_returns = (numerator / denominator) - 1

    # Volatility: Rolling std of monthly returns
    monthly_ret = monthly_prices.pct_change(fill_method=None)
    rolling_vol = monthly_ret.rolling(window=lookback_months).std()

    # Sharpe Ratio (Risk-Adjusted Momentum)
    momentum_sharpe = momentum_returns / rolling_vol.replace(0, np.nan)
    momentum_sharpe = momentum_sharpe.clip(upper=5.0, lower=-5.0)

    # Get latest metrics
    latest_sharpe = momentum_sharpe.iloc[-1]
    latest_return = momentum_returns.iloc[-1]
    latest_vol_monthly = rolling_vol.iloc[-1]
    latest_price = prices_subset.iloc[-1]

    # Calculate daily volatility for position sizing (FIXED: Use proper window)
    daily_returns = prices_subset.pct_change(fill_method=None)
    # Make sure we have enough data for 21-day rolling
    if len(daily_returns) >= 21:
        daily_vol = daily_returns.rolling(window=21).std().iloc[-1]
    else:
        # Fallback if not enough data
        daily_vol = daily_returns.std()

    # Replace NaN/0 with reasonable default (2% daily vol)
    daily_vol = daily_vol.fillna(0.02)
    daily_vol = daily_vol.replace(0, 0.02)

    # Calculate average dollar volume (last 21 days)
    recent_window = min(21, len(prices_subset))
    recent_prices = prices_subset.iloc[-recent_window:]
    recent_volumes = volumes_subset.iloc[-recent_window:]
    avg_dollar_vol = (recent_prices * recent_volumes).mean()

    # ========== STEP 2: Market Regime Detection ==========

    regime_label = "NEUTRAL"
    regime_leverage = 1.0

    if benchmark_series is not None and len(benchmark_series) > 0:
        # Benchmark metrics
        bench_latest = benchmark_series.iloc[-1]

        # Calculate SMA200 (make sure we have enough data)
        if len(benchmark_series) >= 200:
            bench_sma200 = benchmark_series.rolling(window=200).mean().iloc[-1]
        else:
            bench_sma200 = benchmark_series.mean()

        # Volatility for panic detection
        bench_ret = benchmark_series.pct_change(fill_method=None)

        if len(bench_ret) >= 21:
            bench_vol_21d = bench_ret.rolling(window=21).std().iloc[-1]
            panic_threshold = bench_ret.rolling(window=21).std().quantile(0.95)
        else:
            bench_vol_21d = bench_ret.std()
            panic_threshold = bench_vol_21d * 2  # Fallback

        # Determine regime
        is_panic = bench_vol_21d > panic_threshold
        is_bull = bench_latest > bench_sma200

        if is_panic:
            regime_label = "PANIC"
            regime_leverage = leverage_panic
        elif is_bull:
            regime_label = "BULL"
            regime_leverage = leverage_bull
        else:
            regime_label = "BEAR"
            regime_leverage = leverage_bear

        print(f"\nMarket Regime: {regime_label}")
        print(f"   Benchmark: ₹{bench_latest:.2f} (SMA200: ₹{bench_sma200:.2f})")
        print(f"   Volatility: {bench_vol_21d*100:.2f}% (Panic: {panic_threshold*100:.2f}%)")
        print(f"   Max Leverage: {regime_leverage:.1f}x")

    # ========== STEP 3: Evaluate Each Stock ==========

    signals = []

    for ticker in available_stocks:
        # Current metrics
        sharpe = latest_sharpe[ticker]
        ret_9m = latest_return[ticker]
        vol = daily_vol[ticker]
        price = latest_price[ticker]
        dvol = avg_dollar_vol[ticker]

        # SMA200 for trend (FIXED: Use pre-calculated full history SMA)
        sma200 = sma200_full[ticker].iloc[-1]

        # Last month return for stop-loss check
        if len(monthly_ret[ticker]) > 0:
            last_month_ret = monthly_ret[ticker].iloc[-1]
        else:
            last_month_ret = 0.0

        # ===== ENTRY CRITERIA CHECKS =====

        checks = {}

        # 1. Price Filter
        checks['Price_OK'] = price > min_price

        # 2. Liquidity Filter
        checks['Liquidity_OK'] = dvol > min_dollar_vol

        # 3. Trend Filter (Above 200-day SMA) - FIXED
        if not pd.isna(sma200) and sma200 > 0:
            checks['Trend_OK'] = price > sma200
        else:
            checks['Trend_OK'] = False

        # 4. Stop-Loss Check (No recent crash)
        if not pd.isna(last_month_ret):
            checks['No_Crash'] = last_month_ret >= -0.15
        else:
            checks['No_Crash'] = True

        # 5. Positive Momentum
        if not pd.isna(ret_9m):
            checks['Positive_Return'] = ret_9m > min_return_threshold
        else:
            checks['Positive_Return'] = False

        # 6. Strong Sharpe Ratio
        if not pd.isna(sharpe):
            checks['Strong_Sharpe'] = sharpe > sharpe_threshold
        else:
            checks['Strong_Sharpe'] = False

        # 7. Valid Volatility (for sizing) - FIXED
        checks['Valid_Vol'] = not pd.isna(vol) and vol > 0.001  # At least 0.1% daily vol

        # Count passed checks
        passed = sum(checks.values())
        total = len(checks)

        # ===== POSITION SIZING =====

        allocation = 0.0

        if all(checks.values()):
            # Calculate weight based on volatility
            safe_vol = vol if vol > 0.001 and not pd.isna(vol) else 0.02
            raw_weight = target_daily_risk / safe_vol

            # Cap individual weight
            capped_weight = min(raw_weight, max_weight_per_stock)

            # Adjust for regime
            allocation = capped_weight * regime_leverage

            # Final cap at max_weight
            allocation = min(allocation, max_weight_per_stock)

        # ===== SIGNAL DETERMINATION =====

        if all(checks.values()):
            signal = "ENTER NOW"
            reason = f"All checks passed. Strong momentum (Sharpe: {sharpe:.2f})"
        elif passed >= 5:  # Most checks pass
            signal = "WAIT"
            failed = [k.replace('_', ' ') for k, v in checks.items() if not v]
            reason = f"Close but waiting on: {', '.join(failed)}"
        else:
            signal = "NOT READY"
            failed = [k.replace('_', ' ') for k, v in checks.items() if not v]
            reason = f"Multiple issues: {', '.join(failed[:2])}"

        # ===== CALCULATE DISPLAY METRICS =====

        # Price vs SMA200 - FIXED
        if not pd.isna(sma200) and sma200 > 0:
            price_vs_sma = (price / sma200 - 1) * 100
        else:
            price_vs_sma = 0.0

        # ===== BUILD RESULT =====

        signals.append({
            'Ticker': ticker,
            'Signal': signal,
            'Entry_Price': price,
            'Recommended_Allocation': allocation * 100,  # Convert to %
            'Sharpe_Ratio': sharpe if not pd.isna(sharpe) else 0,
            'Raw_Return': ret_9m * 100 if not pd.isna(ret_9m) else 0,  # %
            'Daily_Volatility': vol * 100 if not pd.isna(vol) else 0,  # %
            'Price_vs_SMA200': price_vs_sma,  # %
            'Avg_Dollar_Volume': dvol / 1e6,  # Millions
            'Regime': regime_label,
            'Checks_Passed': f"{passed}/{total}",
            'Reason': reason
        })

    # ========== STEP 4: Create Results DataFrame ==========

    signals_df = pd.DataFrame(signals)

    # Sort by signal priority (ENTER > WAIT > NOT READY), then by Sharpe
    signal_order = {"ENTER NOW": 0, "WAIT": 1, "NOT READY": 2}
    signals_df['_sort_key'] = signals_df['Signal'].map(signal_order)
    signals_df = signals_df.sort_values(['_sort_key', 'Sharpe_Ratio'], ascending=[True, False])
    signals_df = signals_df.drop('_sort_key', axis=1)
    signals_df = signals_df.reset_index(drop=True)

    # ========== STEP 5: Print Summary ==========

    print(f"\n{'='*60}")
    print("ENTRY SIGNALS SUMMARY")
    print(f"{'='*60}")

    enter_count = (signals_df['Signal'] == 'ENTER NOW').sum()
    wait_count = (signals_df['Signal'] == 'WAIT').sum()
    not_ready_count = (signals_df['Signal'] == 'NOT READY').sum()

    print(f"ENTER NOW:   {enter_count} stocks")
    print(f"WAIT:        {wait_count} stocks")
    print(f"NOT READY:   {not_ready_count} stocks")

    if enter_count > 0:
        total_allocation = signals_df[signals_df['Signal'] == 'ENTER NOW']['Recommended_Allocation'].sum()
        print(f"\nTotal Recommended Allocation: {total_allocation:.1f}%")

        if total_allocation > 100:
            print(f"   ⚠️  WARNING: Exceeds 100%. Consider prioritizing or scaling down.")

    # ========== STEP 6: Print Detailed Signals ==========

    print(f"\n{'='*60}")
    print("DETAILED ENTRY SIGNALS")
    print(f"{'='*60}\n")

    for _, row in signals_df.iterrows():
        print(f"{row['Ticker']} - {row['Signal']}")
        print(f"  Entry Price: ₹{row['Entry_Price']:.2f}")
        print(f"  Allocation:  {row['Recommended_Allocation']:.1f}% of portfolio")
        print(f"  Sharpe:      {row['Sharpe_Ratio']:.2f}")
        print(f"  Return (9m): {row['Raw_Return']:.1f}%")
        print(f"  Volatility:  {row['Daily_Volatility']:.2f}%")
        print(f"  vs SMA200:   {row['Price_vs_SMA200']:+.1f}%")
        print(f"  Checks:      {row['Checks_Passed']}")
        print(f"  Reason:      {row['Reason']}")
        print()

    # ========== STEP 7: Return DataFrame ==========

    return signals_df


def save_entry_signals(signals_df, filename='entry_signals.csv'):
    """
    Save entry signals to CSV for tracking/alerts.

    Args:
        signals_df (pd.DataFrame): Output from monitor_entry_signals()
        filename (str): CSV filename
    """
    if signals_df.empty:
        print("No signals to save.")
        return

    signals_df.to_csv(filename, index=False)
    print(f"\nEntry signals saved to '{filename}'")

    # Also create a quick action list
    enter_stocks = signals_df[signals_df['Signal'] == 'ENTER NOW']
    if not enter_stocks.empty:
        action_file = filename.replace('.csv', '_action_list.txt')
        with open(action_file, 'w') as f:
            f.write("=" * 60 + "\n")
            f.write("STOCKS TO ENTER NOW\n")
            f.write("=" * 60 + "\n\n")
            for _, row in enter_stocks.iterrows():
                f.write(f"{row['Ticker']}\n")
                f.write(f"  Buy at: ₹{row['Entry_Price']:.2f}\n")
                f.write(f"  Allocate: {row['Recommended_Allocation']:.1f}%\n")
                f.write(f"  Sharpe: {row['Sharpe_Ratio']:.2f}\n\n")

        print(f"Action list saved to '{action_file}'")

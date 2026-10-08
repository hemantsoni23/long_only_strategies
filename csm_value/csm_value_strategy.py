"""
csm_value_strategy.py -- CSM Earnings-Yield on the Elendel chassis.
Derived from Old_live_strategies/csm_elendel_strategy.py by _generate_elendel_chassis.py: ONLY the ranking signal (E/P on point-in-time quarterly results) and the universe
(liquidity ranks 301-1000, no SMA-200 trend filter, no absolute-momentum gate) differ; position sizing, hysteresis, stops, Crash Guard, overlays and live exit interface are Elendel's.
"""
import os
import sys

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fundamentals_loader import load_results, monthly_frame   # point-in-time quarterly results read straight from the raw NSE XBRL JSON


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class CSMValue:
    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        # Ranking signal: E/P (TTM net profit / market cap) among names with positive TTM profit AND rising latest-quarter profit; point-in-time quarterly results
        results_df          = None,  # optional pre-built results table (fundamentals_loader.load_results); default reads the raw JSON directory
        results_max_age_days = 140,  # a quarterly result stays 'current' this long after its filing date
        require_profit_growth = True,  # latest quarter's yoy net profit must be rising
        max_ep              = 0.50,  # data-error / one-off guard: ignore E/P above 50%
        min_eligible        = 60,    # fewer fundamentals-eligible names than this in a month -> no signal that month
        use_ca_mask         = True,  # corporate-action mask (price cliffs): see calculate_factors
        book_size_cr        = None,  # capacity-aware sizing: assumed book size in Rs crore. None = off (no liquidity cap on position size)
        max_adv_participation = 0.10,  # with book_size_cr: a position may not exceed this share of the stock's 63-day median daily traded value (the excess weight stays in cash)
        min_cooldown_days   = 0,     # re-entry churn control: minimum calendar days a name is blocked after ANY stop, including profitable ones (the loss-scaled cooldown gives profitable stops 0 days)
        max_oneoff_share    = None,  # earnings-quality filter: drop names whose trailing-12m other income + exceptional gains exceed this share of trailing-12m pre-tax profit (banks exempt). None = off
        profit_basis        = 'total',  # 'total' = reported net profit; 'owners_consistent' = profit attributable to owners where every quarter of a figure reports it, else the total line for all of them; 'core' = reported profit less other income and exceptional items (25% tax); 'owners' = legacy mixed fallback (ablation only)
        restore_units       = True,  # restore filed share counts to today's units (matches the split-adjusted prices). False = the old leaky behaviour, for ablation only
        ca_tol              = 0.03,  # a one-day move within this of a clean split/bonus cliff (-33%, -50%, -60%, -67%, -75%, -80%, -90%) counts as a corporate action
        abs_momentum_lookback_months = 12,  # kept only for the engine's bookkeeping: the value strategy has NO absolute-momentum gate (momentum_returns is set to a constant positive)
        abs_momentum_lag_months      = 1,
        # Universe
        top_n               = 15,
        min_price           = 20.0,
        universe_top_n_min = 301,   # liquidity ranks 301-1000 (the 300 most liquid names excluded): chosen on the TRAIN window by train_test_protocol.py (a near tie with a floor of 1)
        universe_top_n_max      = 1000,
        max_circuit_days    = 5,
        buffer_ratio        = 0.2,
        # Stops
        atr_period          = 14,
        atr_multiplier      = 3.0,
        atr_cap_percentile  = 0.75,
        atr_cap_window      = 63,
        hard_stop_from_entry    = 0.15,
        hard_stop_from_peak     = 0.20,
        stop_slippage_pct       = 0.003,
        # Overlays
        use_crash_guard         = True,
        crash_guard_cooldown    = 10,
        corr_guard_threshold    = 0.8,
        stop_cooldown_days      = 20,   # block re-entry N calendar days after stop on same ticker
        min_hold_days           = 5,    # TRADING days before stop can fire (V1 fix #1)
        atr_multiplier_high_vol = 2.0,  # tighter chandelier when benchmark vol is elevated (moot: chandelier off)
        risk_pct_per_trade      = 0.01,  # risk-budget sizing: weight = risk_pct_per_trade / hard_stop_from_entry, same convention the breakout strategies (HR/VCP/Donchian) already run live -- see POSITION_SIZING_BREAKOUT_VS_MOMENTUM.md Fix 1
        max_weight_per_stock    = 0.05,  # kept at the original default -- a controlled A/B test showed raising this (to let the risk-budget cap below bind) worsens Sharpe/Sortino/MaxDD/Calmar here, because momentum's wide 15% stop reflects genuinely imprecise entries (unlike breakout's structurally-tight ones), so a bigger position just amplifies that risk rather than monetizing earned safety -- see POSITION_SIZING_BREAKOUT_VS_MOMENTUM.md's own Fix 1 -> Fix 3 dependency. risk_pct_per_trade below is kept available to opt into once/if entry precision is improved (Fix 3).
        vol_target              = 0.15,
        # Entry-reason tagging
        post_cooldown_window_days = 90, # entry within N days of a prior stop → POST_COOLDOWN
        # Chassis A/B flags -- default False reproduces batch v2.4 exactly
        apply_atr_cap           = False,  # cap ATR at rolling q75/63d
        atr_prev_day            = False,  # use day i-1 ATR in the loop
        min_hold_trading        = False,  # count min-hold in trading days, not calendar
        # Execution-layer features
        use_liquid_mf           = True,   # idle cash is swept into a liquid fund (6.5%), as in Zenith; the Elendel default (False) leaves it at 0%
        liquid_mf_annual_rate   = 0.065,
        cooldown_mode           = 'loss_scaled', # 'flat' | 'loss_scaled'
        cooldown_floor_days     = 10,     # loss_scaled: min cooldown for a losing stop
        cooldown_cap_days       = 60,     # loss_scaled: max cooldown
        leverage_bull           = 1.0,    # exposure multiplier, benchmark > SMA200
        leverage_bear           = 0.8,    # exposure multiplier, benchmark < SMA200
        leverage_panic          = 0.5,    # exposure multiplier when monthly bench vol >
                                          # its own expanding 95th-pct threshold; overwrites
                                          # leverage_bull as the base, bear then tightens
                                          # further via min(). Independent of Crash Guard.
        rebalance_exit_buffer_months = 1, # exit only after N+1 consecutive signal drops
        stop_fill_mode          = 'close_next_open', # 'close_next_open' = stop checked on the daily close, exit at next open | 'stop' = resting intraday stop order | 'next_open' = intraday-low breach, exit at next open
        # Risk & alpha features
        use_crystallisation     = False,  # sell fraction at +trigger, breakeven stop
        crystallise_trigger     = 0.10,
        crystallise_fraction    = 0.5,
        use_staleness_gate      = False,  # block entries with old signal age
        stale_threshold_months  = 5,
        use_time_stop           = False,  # exit if < min_gain after N trading days
        time_stop_days          = 30,
        time_stop_min_gain      = 0.03,
        use_cg_quality_gate     = False,  # post-Crash-Guard re-entry needs bench > EMA20
        # Low-turnover / long-hold features
        use_trade_deadband      = True,   # skip re-trading if weight delta < min_trade_pct
        min_trade_pct           = 0.0025,
        scale_update_days       = 5,      # throttle vol_scale/corr_scale recompute frequency
        scale_update_move_pct   = 0.05,   # ...or sooner if the raw value drifts this much
        use_chandelier_floor    = True,   # moot here -- chandelier is off (see use_chandelier)
        use_swap_gap            = True,   # new candidate must rank >= swap_gap places better
        swap_gap                = 10,     # to displace a held name
        quarterly_entries       = False,  # gate new entries to every 3rd month-end
        stop_only_exits         = False,  # disable rank-based REBALANCE exits entirely
        use_chandelier           = False, # no ATR trailing stop; only hard stops remain
        **kwargs,
    ):
        self.prices               = prices_df
        self.volumes              = volumes_df
        self.highs                = highs_df  if highs_df  is not None else pd.DataFrame()
        self.lows                 = lows_df   if lows_df   is not None else pd.DataFrame()
        self.opens                = opens_df  if opens_df  is not None else pd.DataFrame()
        self.benchmark            = benchmark_series

        self.components            = ('EP',)
        self._results_in           = results_df
        self.results_max_age_days  = results_max_age_days
        self.require_profit_growth = require_profit_growth
        self.max_ep                = max_ep
        self.min_eligible          = min_eligible
        self.use_ca_mask           = use_ca_mask
        self.restore_units         = restore_units
        self.profit_basis          = profit_basis
        self.max_oneoff_share      = max_oneoff_share
        self.book_size_cr          = book_size_cr
        self.max_adv_participation = max_adv_participation
        self.min_cooldown_days     = min_cooldown_days
        self.ca_tol                = ca_tol
        self.abs_momentum_lookback_months = abs_momentum_lookback_months
        self.abs_momentum_lag_months      = abs_momentum_lag_months

        self.top_n                = top_n
        self.min_price            = min_price
        self.universe_top_n_min = universe_top_n_min
        self.universe_top_n_max       = universe_top_n_max
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
        self.risk_pct_per_trade       = risk_pct_per_trade
        self.max_weight_per_stock     = max_weight_per_stock
        self.vol_target               = vol_target
        self.post_cooldown_window_days = post_cooldown_window_days
        self.apply_atr_cap            = apply_atr_cap
        self.atr_prev_day             = atr_prev_day
        self.min_hold_trading         = min_hold_trading

        self.use_liquid_mf            = use_liquid_mf
        self.liquid_mf_annual_rate    = liquid_mf_annual_rate
        self.cooldown_mode            = cooldown_mode
        self.cooldown_floor_days      = cooldown_floor_days
        self.cooldown_cap_days        = cooldown_cap_days
        self.leverage_bull            = leverage_bull
        self.leverage_bear            = leverage_bear
        self.leverage_panic           = leverage_panic
        self.rebalance_exit_buffer_months = rebalance_exit_buffer_months
        self.stop_fill_mode           = stop_fill_mode
        self.use_crystallisation      = use_crystallisation
        self.crystallise_trigger      = crystallise_trigger
        self.crystallise_fraction     = crystallise_fraction
        self.use_staleness_gate       = use_staleness_gate
        self.stale_threshold_months   = stale_threshold_months
        self.use_time_stop            = use_time_stop
        self.time_stop_days           = time_stop_days
        self.time_stop_min_gain       = time_stop_min_gain
        self.use_cg_quality_gate      = use_cg_quality_gate

        self.use_trade_deadband       = use_trade_deadband
        self.min_trade_pct            = min_trade_pct
        self.scale_update_days        = scale_update_days
        self.scale_update_move_pct    = scale_update_move_pct
        self.use_chandelier_floor     = use_chandelier_floor
        self.use_swap_gap             = use_swap_gap
        self.swap_gap                 = swap_gap
        self.quarterly_entries        = quarterly_entries
        self.stop_only_exits          = stop_only_exits
        self.use_chandelier           = use_chandelier

        self.factors              = None
        self.factor_legs          = {}    # {component: universe-filtered component DataFrame}
        self._legs_unfiltered     = {}    # {component: raw component DataFrame} for component IC
        self.momentum_returns     = None
        self.positions            = None
        self.all_ranks            = None
        self._signal_age          = None  # consecutive months in entry zone (V2, §4.3)
        self.results              = None
        self.position_metadata    = []
        self.reject_log           = []
        self._reject_seen         = set()
        self.atr                  = None
        self._regime_daily        = None

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty
        print(f"CSM CSMValue Earnings-Yield initialised  |  top_n={top_n}  buffer={buffer_ratio}"
              f"  signal=E/P(profit growth>0={require_profit_growth})"
              f"  abs_mom_gate={self.abs_momentum_lookback_months}m(lag{self.abs_momentum_lag_months})"
              f"  ATR-stops={'YES' if has_h and has_l else 'FALLBACK-2%'}"
              f"  chandelier={'OFF (signal-driven exits)' if not use_chandelier else 'ON'}"
              f"  opens={'YES' if has_o else 'FALLBACK-close'}"
              f"  crash_guard={'ON' if use_crash_guard else 'OFF'}"
              f"  stop_cooldown={stop_cooldown_days}d"
              f"  min_hold={min_hold_days} {'trading' if min_hold_trading else 'calendar'}-days"
              f"  atr_mult={atr_multiplier}/{atr_multiplier_high_vol}(hv)"
              f"  atr_cap={'ON' if apply_atr_cap else 'OFF'}"
              f"  atr_prev_day={'ON' if atr_prev_day else 'OFF'}"
              f"  universe_top_n_min={universe_top_n_min}"
              f"  universe_top_n_max={universe_top_n_max}")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER  (identical to batch v2.4)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, monthly_avg_dvol, daily_prices):
        """Universe eligibility mask: price floor, liquidity rank band, circuit-day limit, falling-knife gate (all lookahead-safe via .shift).  Unlike Elendel there is NO SMA-200 trend filter."""
        price_mask = monthly_prices.shift(1) > self.min_price

        daily_dvol        = self.prices * self.volumes
        median_dvol_daily = daily_dvol.rolling(window=63, min_periods=21).median().shift(1)
        monthly_dvol      = median_dvol_daily.resample('ME').last().reindex(monthly_prices.index)
        dvol_rank         = monthly_dvol.rank(axis=1, ascending=False, method='min')
        liquidity_mask    = (dvol_rank >= self.universe_top_n_min) & (dvol_rank <= self.universe_top_n_max)

        circuit_mask = pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)
        if not self.highs.empty and not self.lows.empty:
            is_circuit   = (self.highs == self.lows).shift(1)
            circuit_cnt  = is_circuit.rolling(window=63, min_periods=1).sum()
            monthly_circ = circuit_cnt.resample('ME').last().reindex(monthly_prices.index).fillna(0)
            circuit_mask = monthly_circ <= self.max_circuit_days

        monthly_ret = monthly_prices.pct_change(fill_method=None)
        crash_mask  = monthly_ret.shift(1) >= -0.15

        return price_mask & liquidity_mask & circuit_mask & crash_mask

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION  (CSMElendel composite — blueprint §3.2)
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """E/P = TTM net profit / (price x shares) among names with positive and rising earnings, cross-sectionally z-scored. No trend condition, no absolute-momentum gate."""
        print(f"Calculating CSMValue E/P factor (point-in-time quarterly results, max age {self.results_max_age_days}d) ...")

        if self.benchmark is None:
            raise ValueError("CSMValue requires a benchmark_series (regime / vol scaling); none was provided.")

        monthly_prices = self.prices.resample('ME').last()

        # Dollar-volume for the universe filter
        daily_dvol       = self.prices * self.volumes
        monthly_avg_dvol = daily_dvol.resample('ME').mean()

        prices_ff = self.prices.ffill()
        bench_ff  = self.benchmark.reindex(self.prices.index).ffill()

        valid_universe = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)

        # E/P, point-in-time: latest quarterly result filed on/before each month-end (expires after results_max_age_days), TTM net profit / (month-end price x shares outstanding)
        # ── Corporate-action mask (price side), in the spirit of the runner's mask_corporate_actions ───────────────────────────────────────────────
        # A corporate-action "cliff" is a one-day move that matches a clean split/bonus (-33%, -50%, -60%, -67%, -75%, -80%, -90%, or a clean reverse-split jump) or a day the runner already
        # NaN'd (move outside [-40%, +300%]).  Two uses:
        #  (a) a split seen in the filings is restored to today's units ONLY if the price series was adjusted for it (no cliff in the prices around it); if the vendor left it unadjusted the
        #      prices and the filings are already in the same units, so nothing is restored;
        #  (b) a stock-month is excluded when a cliff occurred AFTER the latest filing used for it: the filed share count is then stale relative to the price.
        px_ca = self.prices
        r1 = px_ca.pct_change(fill_method=None)
        masked_day = px_ca.isna() & px_ca.shift(1).notna() & px_ca.shift(-1).notna()
        ratios_ca = (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0)
        cliff_ca = masked_day.copy()
        for c_ in ratios_ca:
            cliff_ca |= (r1 - (1.0 / c_ - 1.0)).abs() <= self.ca_tol          # forward split / bonus: price falls to 1/c
            cliff_ca |= (r1 - (c_ - 1.0)).abs() <= self.ca_tol * c_          # reverse split: price rises c-fold
        R_ca, M_ca, D_ca = r1.values, masked_day.values, px_ca.index
        col_ca = {s_: i_ for i_, s_ in enumerate(px_ca.columns)}
        def cliff_checker(sym, a, b, ratio):
            j = col_ca.get(sym)
            if j is None or a is None or b is None:
                return False
            i0, i1 = D_ca.searchsorted(pd.Timestamp(a)), D_ca.searchsorted(pd.Timestamp(b), side='right')
            if i1 <= i0:
                return False
            seg, msk = R_ca[i0:i1, j], M_ca[i0:i1, j]
            if ratio >= 1.0:
                return bool(msk.any() or np.nanmin(np.append(seg, 0.0)) <= -0.8 * (1.0 - 1.0 / ratio))
            return bool(msk.any() or np.nanmax(np.append(seg, 0.0)) >= 0.8 * (1.0 / ratio - 1.0))
        res = (load_results(symbols=list(self.prices.columns), cliff_checker=(cliff_checker if self.use_ca_mask else None), restore_units=self.restore_units, profit_basis=self.profit_basis)
               if self._results_in is None else self._results_in)
        idx = monthly_prices.index
        npttm  = monthly_frame(res, 'np_ttm', idx, self.prices.columns, self.results_max_age_days)
        shares = monthly_frame(res, 'shares_adj', idx, self.prices.columns, self.results_max_age_days)   # shares in today's (split-adjusted) units to match the split-adjusted prices
        growth = monthly_frame(res, 'sg_np', idx, self.prices.columns, self.results_max_age_days)
        ep = (npttm / (monthly_prices * shares)).replace([np.inf, -np.inf], np.nan)
        ok = (npttm > 0) & ep.notna() & (ep <= self.max_ep)
        self.ca_stale_mask = pd.DataFrame(False, index=idx, columns=self.prices.columns)
        if self.use_ca_mask:
            filed_ns = monthly_frame(res.assign(filed_ns=res.filed.astype('int64').astype('float64')), 'filed_ns', idx, self.prices.columns, self.results_max_age_days)
            cc = cliff_ca.fillna(False).astype('int32').cumsum().values
            pos_me = D_ca.searchsorted(idx.values, side='right') - 1
            Lns = filed_ns.values
            valid_L = ~np.isnan(Lns)
            L_dt = np.where(valid_L, Lns, 0).astype('int64').astype('datetime64[ns]')
            pos_L = D_ca.searchsorted(L_dt.reshape(-1), side='right').reshape(Lns.shape) - 1
            pos_L = np.clip(pos_L, 0, len(D_ca) - 1)
            cols_ix = np.arange(cc.shape[1])[None, :].repeat(len(idx), axis=0)
            stale = (cc[pos_me[:, None].repeat(cc.shape[1], axis=1), cols_ix] - cc[pos_L, cols_ix]) > 0
            self.ca_stale_mask = pd.DataFrame(stale & valid_L, index=idx, columns=self.prices.columns)
            ok &= ~self.ca_stale_mask
            print(f"  [corporate-action mask] stock-months with a price cliff after the latest filing excluded: {int((self.ca_stale_mask & (npttm > 0)).sum().sum()):,}")
        if self.require_profit_growth:
            ok &= (growth > 0)
        if self.max_oneoff_share is not None:
            oo = monthly_frame(res, 'oneoff_share', idx, self.prices.columns, self.results_max_age_days)
            ok &= (oo <= self.max_oneoff_share)          # NaN (no positive pre-tax profit) fails the test
        ep_unf = ep.where(ok)
        ep_masked = ep_unf.where(valid_universe)
        ep_masked = ep_masked.where(ep_masked.notna().sum(axis=1) >= self.min_eligible, np.nan)     # too thin a month -> no signal

        def _zscore(df):
            return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)

        self.factors           = _zscore(ep_masked)
        self._legs_unfiltered  = {'EP': ep_unf}
        self.factor_legs       = {'EP': ep_masked}

        # No absolute-momentum gate for a value strategy: a constant positive "return" keeps every ranked name eligible and the engine's bookkeeping unchanged.
        self.momentum_returns = valid_universe.astype(float).where(valid_universe)

        self._prepare_stop_indicators(monthly_prices)
        # 63-day median traded value (Rs), lagged one day, at each month-end: used by the optional capacity cap in get_positions()
        self._adv_monthly = ((self.prices * self.volumes).rolling(63, min_periods=21).median().shift(1).resample('ME').last().reindex(monthly_prices.index))
        self.factors.dropna(how='all', inplace=True)
        self.momentum_returns.dropna(how='all', inplace=True)

        # ATR (Wilder EWM; True Range = max(H-L, |H-PrevC|, |L-PrevC|)), capped at its own rolling 75th percentile so a crash-day spike can't blow the chandelier open (1-day shift applied at point of use)
        close_p = self.prices
        if not self.highs.empty and not self.lows.empty:
            _h, _l, _pc = self.highs.ffill(), self.lows.ffill(), close_p.shift(1)
            _tr = (_h - _l).abs().combine((_h - _pc).abs(), np.maximum).combine((_l - _pc).abs(), np.maximum)
        else:
            _tr = close_p.diff().abs() * np.sqrt(np.pi / 2)
        _atr_raw = _tr.ewm(com=self.atr_period - 1, adjust=False).mean()
        if self.apply_atr_cap:
            _atr_cap = _atr_raw.rolling(
                window      = self.atr_cap_window,
                min_periods = max(1, self.atr_cap_window // 3),
            ).quantile(self.atr_cap_percentile)
            self.atr = _atr_raw.clip(upper=_atr_cap)
        else:
            self.atr = _atr_raw          # batch v2.4 behaviour: uncapped

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
    # STOP / RE-ENTRY DECISION LOGIC  (shared by backtest loop AND get_exit_signals — §0)
    # ──────────────────────────────────────────────────────────────────────────

    def _cooldown_days_for(self, pnl_pct):
        """Re-entry cooldown after a STOP_HIT: the base rule below, but never shorter than min_cooldown_days (default 0 = unchanged)."""
        return max(self._cooldown_days_base(pnl_pct), self.min_cooldown_days)

    def _cooldown_days_base(self, pnl_pct):
        """Re-entry cooldown after a STOP_HIT: 'flat' = fixed days; 'loss_scaled' = proportional to the loss (a profitable exit gets none, a big loss gets up to cooldown_cap_days)."""
        if self.cooldown_mode == 'loss_scaled':
            if pd.isna(pnl_pct) or pnl_pct >= 0:
                return 0
            return int(np.clip(self.stop_cooldown_days * abs(pnl_pct) / 10.0,
                               self.cooldown_floor_days, self.cooldown_cap_days))
        return self.stop_cooldown_days

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False, close_only=False):
        """Three-layer stop (effective_stop = max(chandelier, entry_hard, peak_hard); atr_stop only ratchets up). Returns (should_exit, fill_price, stop_level, updated_holding, exit_detail) with exit_detail in {CHANDELIER, ENTRY_HARD, PEAK_HARD, FORCE_60, GAP_DOWN_OPEN}. close_only=True: peak and trigger use the close only (no intraday high/low); the caller fills at the next open, so fill_price is NaN."""
        if pd.isna(curr_close) or curr_close <= 0:
            return False, np.nan, holding.get('atr_stop', np.nan), holding, ''
        if close_only:
            curr_low = curr_high = curr_close

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
                return True, float(fill), float(synthetic_stop), holding, 'FORCE_60'

        # Seed effective stop using old peak before updating it
        peak_hard      = peak_price * (1.0 - self.hard_stop_from_peak)
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop}

        # Update peak using intraday high (Chandelier Exit anchors to true daily high)
        bar_high = curr_high if (not pd.isna(curr_high) and curr_high > 0) else curr_close
        new_peak = max(peak_price, bar_high)
        if new_peak > peak_price:
            holding['peak_price'] = new_peak

        # chandelier trail (skipped entirely if use_chandelier=False)
        _atr_mult = self.atr_multiplier_high_vol if high_vol else self.atr_multiplier
        if self.use_chandelier and not pd.isna(curr_atr) and curr_atr > 0:
            _chand_raw = new_peak - _atr_mult * curr_atr
            if self.use_chandelier_floor:
                chandelier = float(np.clip(_chand_raw, new_peak * 0.70, new_peak * 0.97))
            else:
                chandelier = float(max(_chand_raw, new_peak * 0.70))   # cap only, no floor
            atr_stop = max(atr_stop, chandelier)   # ratchet up only

        # L2 + L3 recalculated with updated peak
        entry_hard     = entry_price * (1.0 - self.hard_stop_from_entry) if not pd.isna(entry_price) else -np.inf
        peak_hard      = new_peak * (1.0 - self.hard_stop_from_peak)
        effective_stop = max(atr_stop, entry_hard, peak_hard)
        holding        = {**holding, 'atr_stop': effective_stop, 'peak_price': new_peak}

        # Trigger check via intraday low
        check_price = curr_low if (not pd.isna(curr_low) and curr_low > 0) else curr_close
        if check_price > effective_stop:
            return False, np.nan, effective_stop, holding, ''

        # Which layer is the binding one at trigger time?
        _eps = 1e-9 * max(1.0, effective_stop)
        if effective_stop <= entry_hard + _eps:
            detail = 'ENTRY_HARD'
        elif effective_stop <= peak_hard + _eps:
            detail = 'PEAK_HARD'
        else:
            detail = 'CHANDELIER'   # ratcheted chandelier dominates

        if close_only:
            return True, np.nan, float(effective_stop), holding, detail

        # Fill: gap-down → fill at open; intraday breach → stop × (1−slippage)
        _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
        if _open <= effective_stop:
            fill   = _open
            detail = 'GAP_DOWN_OPEN'
        else:
            fill = effective_stop * (1.0 - self.stop_slippage_pct)
        return True, float(fill), float(effective_stop), holding, detail

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION  (batch v2.4 logic: abs-momentum gate + hysteresis)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self):
        """Monthly cross-sectional ranking with hysteresis: a held stock stays until its rank drops beyond top_n × (1 + buffer_ratio); absolute-momentum gate excludes non-positive long-leg raw returns regardless of rank."""
        if self.factors is None:
            raise ValueError("Call calculate_factors() first.")

        _effective_cap = min(self.risk_pct_per_trade / self.hard_stop_from_entry, self.max_weight_per_stock)
        print(f"Generating Positions  "
              f"top_n={self.top_n}  buffer={self.buffer_ratio}  "
              f"abs_momentum_gate=ON  max_wt={self.max_weight_per_stock:.0%} "
              f"(risk-budget cap={_effective_cap:.1%} from {self.risk_pct_per_trade:.0%} risk / {self.hard_stop_from_entry:.0%} stop)")

        # Volatility for inverse-vol weighting (shift 1 before resample)
        daily_ret   = self.prices.pct_change(fill_method=None)
        monthly_vol = (daily_ret.rolling(21).std().shift(1)
                       .resample('ME').last()
                       .reindex(self.factors.index))

        all_ranks      = self.factors.rank(axis=1, ascending=False, method='first')
        self.all_ranks = all_ranks   # kept for Rank_At_Entry / reject logging

        position_list = []
        prev_held     = set()

        entry_threshold = self.top_n
        exit_threshold  = int(self.top_n * (1 + self.buffer_ratio))

        for month_idx, (date, row_ranks) in enumerate(all_ranks.iterrows()):
            valid_ranks = row_ranks.dropna()

            if valid_ranks.empty:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                prev_held = set()
                continue

            # ── Absolute momentum gate ────────────────────────────────────────
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

            # ── Hysteresis selection ──────────────────────────────────────────
            # quarterly_entries: only every 3rd month-end accepts new entries; existing holdings can still be dropped any month
            _entries_allowed = (not self.quarterly_entries) or (month_idx % 3 == 0)

            kept_held      = []
            new_candidates = []
            for stock, rank in valid_ranks.items():
                if stock in prev_held:
                    if rank <= exit_threshold:
                        kept_held.append((stock, rank))
                else:
                    if _entries_allowed and rank <= entry_threshold:
                        new_candidates.append((stock, rank))

            current_selection = [s for s, r in kept_held]

            if self.use_swap_gap and new_candidates:
                # a new candidate only displaces a held name if it ranks >= swap_gap places better; free slots fill normally
                kept_held_sorted      = sorted(kept_held, key=lambda x: -x[1])       # worst rank first
                new_candidates_sorted = sorted(new_candidates, key=lambda x: x[1])   # best rank first
                free_slots = max(0, self.top_n - len(current_selection))
                worst_ptr  = 0
                for stock, rank in new_candidates_sorted:
                    if free_slots > 0:
                        current_selection.append(stock)
                        free_slots -= 1
                        continue
                    if worst_ptr >= len(kept_held_sorted):
                        break   # no incumbents left to evict, no free slots
                    worst_stock, worst_rank = kept_held_sorted[worst_ptr]
                    if (worst_rank - rank) >= self.swap_gap:
                        current_selection.remove(worst_stock)
                        current_selection.append(stock)
                        worst_ptr += 1
                    else:
                        break   # this and all weaker candidates need an even bigger gap
            else:
                current_selection += [s for s, r in new_candidates]

            prev_held = set(current_selection)

            if not current_selection:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                continue

            # ── Inverse-vol weighting (two-pass clip + renorm) ───────────────
            sel_vols = monthly_vol.loc[date, current_selection].fillna(0.02).replace(0, 0.02)
            inv_vol  = 1.0 / sel_vols
            raw_w    = inv_vol / inv_vol.sum()

            # Risk-budget cap: weight = risk_pct_per_trade / hard_stop_from_entry, same convention
            # the breakout strategies (HR/VCP/Donchian) already run live -- ties the per-name
            # ceiling to the actual entry-stop distance instead of an arbitrary flat constant.
            # max_weight_per_stock remains an outer safety ceiling only (see POSITION_SIZING_
            # BREAKOUT_VS_MOMENTUM.md Fix 1 + Fix 2).
            cap = min(self.risk_pct_per_trade / self.hard_stop_from_entry, self.max_weight_per_stock)
            for _ in range(2):
                raw_w = raw_w.clip(upper=cap)
                total = raw_w.sum()
                if total > 0:
                    raw_w = raw_w / total   # renormalize
            raw_w = raw_w.clip(upper=cap)   # final safety clip

            # Capacity-aware sizing (optional): position <= max_adv_participation x the name's median daily traded value, for a book of book_size_cr crore.
            # The weight removed here is NOT redistributed; it stays in cash (liquid fund).
            if self.book_size_cr is not None:
                _adv = self._adv_monthly.loc[date].reindex(raw_w.index)
                raw_w = np.minimum(raw_w, (self.max_adv_participation * _adv / (self.book_size_cr * 1e7)).fillna(0.0))

            full_w = pd.Series(0.0, index=self.factors.columns, name=date)
            full_w.update(raw_w)
            position_list.append(full_w)

        self.positions = pd.concat(position_list, axis=1).T
        self.positions.index = all_ranks.index

        # signal age: consecutive months inside the entry zone (rank <= top_n and positive abs-momentum); NaN outside the zone
        _mom_pos = (self.momentum_returns.reindex(all_ranks.index)
                    .reindex(columns=all_ranks.columns) > 0)
        _zone    = (all_ranks <= entry_threshold) & _mom_pos
        _csum    = _zone.cumsum()
        _age     = _csum - _csum.where(~_zone).ffill().fillna(0)
        self._signal_age = _age.where(_zone)

        return self.positions

    # ──────────────────────────────────────────────────────────────────────────
    # LIVE EXIT SIGNAL EVALUATOR  (parity rule §0 — same _check_stop_exit path)
    # ──────────────────────────────────────────────────────────────────────────

    def get_exit_signals(self,
                         portfolio:      dict,
                         live_data:      dict,
                         benchmark_vol:  float = None,
                         today          = None,
                         bars_held:      dict  = None) -> dict:
        """
        Evaluate all exit rules for currently held positions on one live bar.
        Mirrors _run_backtest_core()'s Crash Guard + per-stock stop check.

        NOT covered here (caller is responsible): rebalance exits (diff
        get_positions() output between rebalance dates), Correlation Guard
        and Vol Targeting (both scale-only, never trigger exits).

        Parameters
        ----------
        portfolio : dict
            ticker → {
                'entry_price' : float,
                'entry_date'  : date | str,      # ISO-8601 entry date
                'peak_price'  : float,           # highest close/high seen since entry
                'atr_stop'    : float,           # current chandelier stop level
                                                 # (MUST be persisted by caller and
                                                 #  passed back each bar — it only
                                                 #  ratchets UP, never resets)
                'weight'      : float,
            }
        live_data : dict
            ticker → {
                'close' : float,                 # required
                'high'  : float,                 # optional; defaults to close
                'low'   : float,                 # optional; defaults to close
                'open'  : float,                 # optional; defaults to close
                'atr'   : float,                 # optional; defaults to close × 0.02.
                                                 # Supply YESTERDAY's capped ATR to
                                                 # match the backtest convention.
            }
        benchmark_vol : float, optional
            Today's benchmark rolling-21d daily return std-dev (raw daily std).
            If None, Crash Guard and high-vol detection are skipped.
        today : date-like, optional
            Today's date. Defaults to datetime.date.today().
        bars_held : dict, optional
            ticker → TRADING days held so far. When provided, min-hold uses it
            (matches the V1 trading-days fix). Falls back to calendar days from
            entry_date when absent.

        Returns
        -------
        dict with four keys:
            'exits' : ticker → {'reason', 'detail', 'fill_price', 'stop_level'}
            'holds' : ticker → {'updated_peak', 'updated_atr_stop', 'stop_level'}
            'crash_guard_fired' : bool
            'high_vol'          : bool
        """
        import datetime as _dt

        # always coerce -- isinstance(x, date) is also true for Timestamp, and Timestamp - date raises, silently disabling min-hold
        if today is None:
            today = _dt.date.today()
        else:
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
                    'detail'     : 'BENCH_PANIC',
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

            _close = float(bar.get('close', np.nan))
            if pd.isna(_close) or _close <= 0:
                continue   # no usable price — holding state unchanged

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

            # ── Circuit day guard: only with REAL intraday H/L data ──────────
            # When the caller passes only {'close': ltp}, high==low always and the guard would silently suppress every stop -- skip unless real H/L keys are present.
            _has_real_hl = ('high' in bar) and ('low' in bar)
            if _has_real_hl and _high == _low:
                _atr_stop = float(pos.get('atr_stop', np.nan))
                holds[ticker] = {
                    'updated_peak'     : float(pos.get('peak_price', _close)),
                    'updated_atr_stop' : _atr_stop,
                    'stop_level'       : _atr_stop,
                }
                continue

            # ── Min-hold guard: TRADING days when supplied, else calendar ────
            if bars_held is not None and ticker in bars_held:
                _days_held = int(bars_held[ticker])
            else:
                entry_date_raw = pos.get('entry_date', '')
                try:
                    _entry_dt  = pd.Timestamp(str(entry_date_raw)[:10]).date()
                    _days_held = (today - _entry_dt).days
                except Exception:
                    _days_held = 999   # unknown → treat as past grace period

            holding_state = {
                'entry_price' : float(pos.get('entry_price', np.nan)),
                'entry_date'  : pos.get('entry_date', ''),
                'peak_price'  : float(pos.get('peak_price',  _close)),
                'atr_stop'    : float(pos.get('atr_stop',    np.nan)),
                'weight'      : float(pos.get('weight',       0.0)),
            }
            if pd.isna(holding_state['atr_stop']) or holding_state['atr_stop'] <= 0:
                holding_state['atr_stop'] = 0.0

            should_exit, fill_px, stop_lvl, updated_h, detail = self._check_stop_exit(
                stock      = ticker,
                curr_close = _close,
                curr_low   = _low,
                curr_atr   = _atr,
                curr_open  = _open,
                holding    = holding_state,
                curr_high  = _high,
                high_vol   = high_vol,
                close_only = self.stop_fill_mode == 'close_next_open',
            )

            if _days_held < self.min_hold_days:
                should_exit = False

            if should_exit:
                exits[ticker] = {
                    'reason'     : 'STOP_HIT',
                    'detail'     : detail,
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

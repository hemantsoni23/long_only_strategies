"""
csm_quad_sector_rotation_strategy.py
=====================================
CSM Quad Sector Rotation — a sector-timed fork of csm_quad_momentum_strategy.py
(CSMQuadMomentum). Same chassis (universe filter, 3-layer stop, Crash/Corr
Guard, vol targeting, regime leverage, swap-gap anti-churn, signal-driven
exits — no ATR trailing stop by default) and the identical dual-lookback
(6m/12m Sharpe, lag 1) stock-level factor. The one real change: stock
selection is scoped to a fixed budget of GUARANTEED slots per eligible
sector (`sector_top_k` sectors x `stocks_per_sector` stocks each) instead of
a flat top_n rank over the whole universe.

Why a budget, not a filter: this repo already has five prior sector-rotation
attempts. The one that forked this exact same chassis (csm_sector_rotation/,
forked from csm_batch) used a sector-eligibility AND-gate -- pick the top-K
sectors, then let a flat top_n rank draw freely from whatever's left. Its
surviving trade log shows why that failed: only 9/11 sectors ever traded in
23 years, 2 of the largest sectors never traded at all, and one sector alone
carried 41% of all trades. A separate, independent line of research
(sector_rotation/v4-v6) instead used a FIXED per-sector stock quota and
reached the best risk-adjusted result of any prior attempt in this repo
(v6: Sharpe 1.32, Calmar 1.21) precisely because diversification is enforced
by construction, not by a filter. This strategy follows that second,
empirically-better pattern.

Sector layer (the new part, in _compute_sector_bands() and get_positions()):
  - Sector-level factor: the SAME dual-lookback (6m/12m) Sharpe momentum
    formula used at the stock level, applied to a synthetic equal-weight
    daily-return index per Sector_clean bucket.
  - Entry/exit band asymmetry (ported from sector_rotation/v6's proven
    N_SECTORS/N_SECTORS_EXIT mechanic, which fixed a smoothing regression in
    v5 -- do NOT time-smooth the sector composite, it makes MaxDD/Calmar
    worse even when CAGR holds): a sector must rank in the top
    `sector_top_k` to admit NEW entries, but an already-held sector's
    positions are only force-exited once it falls below the wider
    `sector_top_k_exit` band.
  - Depth floor (`min_sector_constituents` via `stocks_per_sector`): a
    sector only counts as entry-eligible in months where it has at least
    `stocks_per_sector` universe-eligible, positive-abs-momentum members --
    otherwise the next-ranked sector is promoted, keeping the effective
    eligible-sector count at sector_top_k whenever the broader universe
    supports it.
  - Within-sector stock ranking reuses csm_quad's own factor/hysteresis/
    swap-gap logic verbatim, just scoped to each sector's own member
    columns instead of the whole universe -- the stock-picking signal is
    deliberately unchanged so this build isolates "does guaranteed sector
    allocation help" as the one controlled variable, not confounded with a
    different in-sector signal (unlike v4-v6, which paired sector momentum
    with a different stock-level signal).

Known, accepted limitation (matches every prior sector-rotation attempt in
this repo): instruments_clean.csv's Sector_clean labels are today's
classification applied retroactively across the whole backtest history --
there is no point-in-time sector data source in this repo. Genuine sector
reclassifications do happen but are rare enough, and no fix is attempted
here; report this caveat alongside any result from this strategy.

Not yet done: get_exit_signals() does not evaluate sector-cascade exits (a
held sector falling below sector_top_k_exit), so a live caller using it
directly would not exactly replicate the backtest's sector-exit behavior.
The backtest loop itself IS correct (it reads self.positions, which already
encodes the sector cascade) -- this gap only matters for a live deployment,
which is out of scope for this baseline.

Strategy logic only -- data loading, the backtest loop, logging, and IC
diagnostics live in csm_quad_sector_rotation_backtest.py.
"""

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

class CSMQuadSectorRotation:
    """
    Sector-timed dual-lookback cross-sectional momentum: the csm_quad chassis
    (universe filter, 3-layer stop, overlays, signal-driven exits) with stock
    selection budgeted across a fixed number of eligible sectors. Positions hold
    until the
    monthly rank decays past the hysteresis buffer, not until price pulls
    back from a peak.

    Per-position state lives in active_holdings[ticker]:
        entry_date, entry_idx, entry_price, peak_price, atr_stop (only ever
        set by the two hard-stop levels here, since use_chandelier=False),
        stop_pct, atr_at_entry, weight, min_price, max_price, entry_reason,
        rank_at_entry, score_at_entry, leg_scores, regime_at_entry
    """

    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        sector_map          = None,   # REQUIRED: pd.Series, ticker -> Sector_clean (see
                                       # load_sector_map()). This is the strategy's new edge.
        # Sector-timing layer (the new part)
        sector_lookback_months       = 12,  # sector-level factor uses the SAME 6m/12m
        sector_lookback_short_months = 6,   # dual-Sharpe formula as the stock-level factor
        sector_lag_months            = 1,
        sector_top_k                 = 3,   # ENTRY band: sector must be top-K (of ~11) to admit new stocks
        sector_top_k_exit            = 6,   # EXIT band (wider): held sector positions only force-exit
                                             # once the sector falls below this rank
        stocks_per_sector            = 6,   # fixed guaranteed slots per eligible sector -- the
                                             # actual concentration fix (see module docstring);
                                             # also doubles as the per-sector depth floor
        # Factor — dual composite (V2 decision: quad retired, see blueprint §4.7)
        lookbacks           = (6, 12),
        leg_lags            = None,     # dict {lookback: lag_months}; default all 1 (V1 / CONFIG_A)
        # Universe
        min_price           = 20.0,
        universe_top_n_min = 1,
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
        max_weight_per_stock    = 0.05,
        vol_target              = 0.15,
        # Entry-reason tagging
        post_cooldown_window_days = 90, # entry within N days of a prior stop → POST_COOLDOWN
        # Chassis A/B flags -- default False reproduces batch v2.4 exactly
        apply_atr_cap           = False,  # cap ATR at rolling q75/63d
        atr_prev_day            = False,  # use day i-1 ATR in the loop
        min_hold_trading        = False,  # count min-hold in trading days, not calendar
        # Execution-layer features
        use_liquid_mf           = False,  # idle cash earns liquid-MF rate instead of RFR
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
        stop_fill_mode          = 'stop', # 'stop' = resting stop order | 'next_open' = exit at next open
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

        if sector_map is None:
            raise ValueError(
                "CSMQuadSectorRotation requires sector_map -- a ticker->sector pd.Series "
                "(see load_sector_map()). This is the strategy's core edge, not an "
                "optional overlay."
            )
        self.sector_map                   = sector_map.reindex(prices_df.columns)
        self.sector_lookback_months       = sector_lookback_months
        self.sector_lookback_short_months = sector_lookback_short_months
        self.sector_lag_months            = sector_lag_months
        self.sector_top_k                 = sector_top_k
        self.sector_top_k_exit            = max(sector_top_k_exit, sector_top_k)
        self.stocks_per_sector            = stocks_per_sector

        self.lookbacks            = tuple(sorted(lookbacks))
        if leg_lags is None:
            leg_lags = {L: 1 for L in self.lookbacks}
        self.leg_lags             = {int(L): int(leg_lags.get(L, 1)) for L in self.lookbacks}

        # top_n has no direct meaning here (the budget is sector_top_k x
        # stocks_per_sector, which can vary as sectors clear/fail the depth
        # floor) -- kept as an attribute purely because shared backtest/IC
        # code (copied verbatim from csm_quad) prints strategy.top_n.
        self.top_n                = sector_top_k * stocks_per_sector
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
        self.factor_legs          = {}    # {lookback: universe-filtered leg DataFrame}
        self._legs_unfiltered     = {}    # {lookback: raw leg DataFrame} for component IC
        self.momentum_returns     = None
        self.positions            = None
        self.all_ranks            = None   # within-SECTOR rank (see get_positions()) --
                                            # not comparable across sectors, only used for
                                            # per-stock entry-context/logging
        self._signal_age          = None  # not tracked in this fork (see module docstring)
        self.sector_factors       = None
        self.sector_entry_ok      = None
        self.sector_exit_ok       = None
        self.sector_rank          = None
        self.sector_exit_flag     = {}    # ticker -> True if this ticker's CURRENT holding
                                           # period was dropped because its SECTOR fell below
                                           # sector_top_k_exit (vs. an in-sector rank decline);
                                           # cleared False the next time the ticker is selected
        self.results              = None
        self.position_metadata    = []
        self.reject_log           = []
        self._reject_seen         = set()
        self.atr                  = None
        self._regime_daily        = None

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty
        n_mapped = int(self.sector_map.notna().sum())
        _lag_str = ",".join(f"{L}m:lag{self.leg_lags[L]}" for L in self.lookbacks)
        print(f"CSM Quad Sector Rotation initialised  |  "
              f"sector_top_k={sector_top_k}(entry)/{self.sector_top_k_exit}(exit)"
              f"  stocks_per_sector={stocks_per_sector}  buffer={buffer_ratio}"
              f"  mapped_tickers={n_mapped}/{len(self.sector_map)}"
              f"  legs=[{_lag_str}]"
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
        """
        Boolean mask for stocks eligible to enter the ranked universe.
        Filters (all lookahead-safe via .shift):
          1. Price > min_price (prev month)
          2. 63d rolling median dollar-vol rank ≤ universe_top_n_max
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
        liquidity_mask    = (dvol_rank >= self.universe_top_n_min) & (dvol_rank <= self.universe_top_n_max)

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
    # FACTOR CALCULATION  (quad composite — blueprint §3.2)
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """
        Quad composite Sharpe momentum factor:
            score = mean over L in lookbacks of  Sharpe_L  (clipped ±5)
            Sharpe_L = [ P(t-lag_L) / P(t-lag_L-L) - 1 ] / (rolling L-month vol, lagged, annualised)

        Per-leg lags come from self.leg_lags (all 1 in V1; V2 zero-lag is a
        config change). The absolute-momentum gate stays on the longest leg's
        raw return (12m by default).
        """
        _lag_str = ", ".join(f"{L}m(lag={self.leg_lags[L]})" for L in self.lookbacks)
        print(f"Calculating Quad-Lookback Factors: {_lag_str} ...")

        monthly_prices = self.prices.resample('ME').last()
        monthly_ret    = monthly_prices.pct_change(fill_method=None)

        # Dollar-volume for the universe filter
        daily_dvol       = self.prices * self.volumes
        monthly_avg_dvol = daily_dvol.resample('ME').mean()

        legs_raw = {}
        for L in self.lookbacks:
            lag   = self.leg_lags[L]
            ret_L = (monthly_prices.shift(lag) / monthly_prices.shift(lag + L)) - 1
            vol_L = (monthly_ret.rolling(window=L).std().shift(lag)
                     * np.sqrt(12)).replace(0, np.nan)
            legs_raw[L] = (ret_L / vol_L).clip(upper=5.0, lower=-5.0)

        # Composite: NaN if any leg is NaN (requires full history — implicit IPO filter)
        self.factors = sum(legs_raw.values()) / float(len(legs_raw))

        # Absolute momentum gate: longest leg's raw return
        L_max = max(self.lookbacks)
        lag_max = self.leg_lags[L_max]
        self.momentum_returns = (monthly_prices.shift(lag_max)
                                 / monthly_prices.shift(lag_max + L_max)) - 1

        valid_universe        = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)
        self._legs_unfiltered = legs_raw
        self.factor_legs      = {L: legs_raw[L].where(valid_universe) for L in self.lookbacks}
        self.factors          = self.factors.where(valid_universe)
        self.momentum_returns = self.momentum_returns.where(valid_universe)

        self._prepare_stop_indicators(monthly_prices)
        self.factors.dropna(how='all', inplace=True)
        self.momentum_returns.dropna(how='all', inplace=True)

        # ATR (Wilder EWM): True Range = max(H-L, |H-PrevC|, |L-PrevC|)
        # V1 fix #2: cap at rolling 63d 75th percentile of its own distribution
        # so a crash-day TR spike cannot blow the chandelier wide open. The
        # 1-day shift is applied at point of use in the backtest loop.
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
    # SECTOR-LEVEL MOMENTUM  (the new part — see module docstring)
    # ──────────────────────────────────────────────────────────────────────────

    def _compute_sector_bands(self):
        """
        Sector-level dual-lookback (6m/12m) Sharpe momentum on a synthetic
        equal-weight daily index per Sector_clean bucket -- the SAME formula
        calculate_factors() uses at the stock level. Returns three (date x
        sector) frames:

          sector_rank     : for diagnostics/reporting only.
          sector_entry_ok : rank <= sector_top_k AND positive raw sector
                             return (mirrors the stock-level absolute-momentum
                             gate) AND the sector currently has >= stocks_per_sector
                             universe-eligible, positive-abs-momentum members
                             (the depth floor -- a sector that can't fill its
                             own quota doesn't count as effectively eligible;
                             the next-ranked sector is promoted instead, since
                             get_positions() just skips a sector where
                             sector_entry_ok is False that month).
          sector_exit_ok  : rank <= sector_top_k_exit (wider band) AND positive
                             raw sector return -- NO depth requirement, since
                             this band only ever RETAINS existing holdings,
                             never admits new ones. A sector held at all is
                             cascade-exited once it fails even this looser test.

        Unmapped tickers (no known sector) are excluded from every sector's
        synthetic index -- excluded, not guessed at.
        """
        sectors = sorted(self.sector_map.dropna().unique())
        daily_ret = self.prices.pct_change(fill_method=None)

        sector_daily_ret  = pd.DataFrame(index=self.prices.index, columns=sectors, dtype=float)
        sector_member_map = {}
        for s in sectors:
            members = [t for t in self.sector_map.index[self.sector_map == s] if t in daily_ret.columns]
            sector_member_map[s] = members
            if members:
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

        sector_factors = (factor_long_sec + factor_short_sec) / 2.0
        sector_factors = sector_factors.reindex(self.factors.index)
        ret_long_sec   = ret_long_sec.reindex(self.factors.index)

        sector_rank = sector_factors.rank(axis=1, ascending=False, method='first')

        # Depth: how many universe-eligible, abs-mom-positive members does
        # each sector actually have this month? self.factors/momentum_returns
        # are already universe-filtered by calculate_factors().
        depth = pd.DataFrame(0, index=self.factors.index, columns=sectors, dtype=int)
        for s in sectors:
            members = [t for t in sector_member_map[s] if t in self.factors.columns]
            if not members:
                continue
            _f_ok = self.factors[members].notna()
            _m_ok = self.momentum_returns[members].gt(0)
            depth[s] = (_f_ok & _m_ok).sum(axis=1)

        sector_abs_ok    = ret_long_sec > 0
        sector_entry_ok  = (sector_rank <= self.sector_top_k) & sector_abs_ok & (depth >= self.stocks_per_sector)
        sector_exit_ok   = (sector_rank <= self.sector_top_k_exit) & sector_abs_ok

        self.sector_factors = sector_factors
        n_entry = sector_entry_ok.sum(axis=1)
        print(f"Sector bands: avg {n_entry.mean():.2f} of {len(sectors)} sectors entry-eligible/month  "
              f"(top_k={self.sector_top_k}, depth>={self.stocks_per_sector}, exit band top_k={self.sector_top_k_exit})")
        return sector_entry_ok, sector_exit_ok, sector_rank

    # ──────────────────────────────────────────────────────────────────────────
    # STOP / RE-ENTRY DECISION LOGIC  (shared by backtest loop AND get_exit_signals — §0)
    # ──────────────────────────────────────────────────────────────────────────

    def _cooldown_days_for(self, pnl_pct):
        """Re-entry cooldown after a STOP_HIT (§5.2). 'flat': fixed days for
        every stop. 'loss_scaled': proportional to the loss — a profitable
        chandelier exit (trend simply ended) gets NO cooldown; a −25% disaster
        gets up to cooldown_cap_days."""
        if self.cooldown_mode == 'loss_scaled':
            if pd.isna(pnl_pct) or pnl_pct >= 0:
                return 0
            return int(np.clip(self.stop_cooldown_days * abs(pnl_pct) / 10.0,
                               self.cooldown_floor_days, self.cooldown_cap_days))
        return self.stop_cooldown_days

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False):
        """
        Three-layer stop for one stock on one bar. atr_stop persists across
        calls and only ratchets up.

          effective_stop = max(chandelier, entry_hard, peak_hard)

        Trigger checked via intraday low. Fill: gap-down -> open price;
        intraday breach -> stop * (1 - slippage).

        Returns (should_exit, fill_price, stop_level, updated_holding,
        exit_detail), where exit_detail is 'CHANDELIER' | 'ENTRY_HARD' |
        'PEAK_HARD' | 'FORCE_60' | 'GAP_DOWN_OPEN'.
        """
        if pd.isna(curr_close) or curr_close <= 0:
            return False, np.nan, holding.get('atr_stop', np.nan), holding, ''

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

        # Fill: gap-down → fill at open; intraday breach → stop × (1−slippage)
        _open = curr_open if (not pd.isna(curr_open) and curr_open > 0) else curr_close
        if _open <= effective_stop:
            fill   = _open
            detail = 'GAP_DOWN_OPEN'
        else:
            fill = effective_stop * (1.0 - self.stop_slippage_pct)
        return True, float(fill), float(effective_stop), holding, detail

    # ──────────────────────────────────────────────────────────────────────────
    # POSITION GENERATION  (per-sector budgeted ranking — see module docstring)
    # ──────────────────────────────────────────────────────────────────────────

    def get_positions(self):
        """
        Monthly ranking, budgeted per sector instead of a flat top_n pool.

        For each of the ~11 sectors, independently:
          - Absolute momentum gate + universe filter (both already baked into
            self.factors/self.momentum_returns being NaN where ineligible).
          - Rank ONLY that sector's own member stocks (a stock's rank here is
            never compared across sectors — that's the whole point).
          - A held stock stays until its IN-SECTOR rank drops beyond
            stocks_per_sector × (1 + buffer_ratio) (same hysteresis formula
            csm_quad uses globally, just scoped per sector).
          - New entries only accepted if the sector is currently entry-eligible
            (top sector_top_k, positive raw return, passes the depth floor).
          - Swap-gap anti-churn (self.use_swap_gap/self.swap_gap) applies
            within each sector's own candidate pool, identical mechanic to
            csm_quad's global version.
          - If the sector has fallen below the wider EXIT band
            (sector_top_k_exit), every held name in it is force-exited this
            month regardless of its own in-sector rank (self.sector_exit_flag
            records this so the backtest's trade log can tag it SECTOR_EXIT
            instead of the generic RANK_DECAY/SIGNAL_DROP).

        Selections from all sectors are then pooled and weighted together
        (inverse-vol, two-pass clip+renorm at max_weight_per_stock) exactly
        as csm_quad does — sizing itself is sector-agnostic.
        """
        if self.factors is None:
            raise ValueError("Call calculate_factors() first.")

        sector_entry_ok, sector_exit_ok, sector_rank = self._compute_sector_bands()
        self.sector_entry_ok = sector_entry_ok
        self.sector_exit_ok  = sector_exit_ok
        self.sector_rank     = sector_rank
        self.sector_exit_flag = {}

        print(f"Generating Positions  sector_top_k={self.sector_top_k}(entry)/"
              f"{self.sector_top_k_exit}(exit)  stocks_per_sector={self.stocks_per_sector}  "
              f"buffer={self.buffer_ratio}  abs_momentum_gate=ON  max_wt={self.max_weight_per_stock:.0%}")

        # Volatility for inverse-vol weighting (shift 1 before resample)
        daily_ret   = self.prices.pct_change(fill_method=None)
        monthly_vol = (daily_ret.rolling(21).std().shift(1)
                       .resample('ME').last()
                       .reindex(self.factors.index))

        sectors = sorted(self.sector_map.dropna().unique())
        sector_members = {
            s: [t for t in self.sector_map.index[self.sector_map == s] if t in self.factors.columns]
            for s in sectors
        }

        # within-sector rank matrix (NOT comparable across sectors) -- kept
        # for Rank_At_Entry / reject-log / entry-context logging, same role
        # csm_quad's self.all_ranks plays, just sector-scoped.
        local_rank_full = pd.DataFrame(np.nan, index=self.factors.index, columns=self.factors.columns)

        position_list       = []
        prev_held_by_sector = {s: set() for s in sectors}

        local_entry_threshold = self.stocks_per_sector
        local_exit_threshold  = int(self.stocks_per_sector * (1 + self.buffer_ratio))

        for month_idx, date in enumerate(self.factors.index):
            row_factors = self.factors.loc[date]
            row_mom     = (self.momentum_returns.loc[date]
                           if date in self.momentum_returns.index else pd.Series(dtype=float))
            pos_mom_stocks = set(row_mom.dropna().loc[lambda s: s > 0].index)

            _entries_allowed = (not self.quarterly_entries) or (month_idx % 3 == 0)

            current_selection      = []
            next_held_by_sector    = {}

            for s in sectors:
                members = sector_members[s]
                prev_held_in_sector = prev_held_by_sector.get(s, set())

                if not members:
                    next_held_by_sector[s] = set()
                    continue

                local_factors = row_factors[members].dropna()
                local_factors = local_factors[local_factors.index.isin(pos_mom_stocks)]
                local_rank    = local_factors.rank(ascending=False, method='first')
                for t, r in local_rank.items():
                    local_rank_full.at[date, t] = r

                _entry_ok = bool(sector_entry_ok.at[date, s]) if s in sector_entry_ok.columns else False
                _exit_ok  = bool(sector_exit_ok.at[date, s])  if s in sector_exit_ok.columns  else False

                if not _exit_ok:
                    # Sector fell below even the wider exit band -- cascade-exit
                    # every held name in it, regardless of its own rank. Flag is
                    # keyed by TICKER ONLY (not date) and read by
                    # _record_closed_trade() at whatever later daily bar the
                    # backtest loop actually executes the trade on (STEP F can
                    # defer this by a month or more via
                    # rebalance_exit_buffer_months) -- a date-keyed flag would
                    # need to re-derive that exact execution date, which is
                    # fragile; ticker-only + "clear on next selection" (below)
                    # is correct regardless of execution timing.
                    for t in prev_held_in_sector:
                        self.sector_exit_flag[t] = True
                    next_held_by_sector[s] = set()
                    continue

                kept_held      = []
                new_candidates = []
                for stock, rank in local_rank.items():
                    if stock in prev_held_in_sector:
                        if rank <= local_exit_threshold:
                            kept_held.append((stock, rank))
                        # else: ordinary in-sector rank decay (RANK_DECAY path,
                        # NOT a sector_exit_flag case)
                    else:
                        if _entry_ok and _entries_allowed and rank <= local_entry_threshold:
                            new_candidates.append((stock, rank))

                sel = [t for t, r in kept_held]

                if self.use_swap_gap and new_candidates:
                    kept_held_sorted      = sorted(kept_held, key=lambda x: -x[1])
                    new_candidates_sorted = sorted(new_candidates, key=lambda x: x[1])
                    free_slots = max(0, self.stocks_per_sector - len(sel))
                    worst_ptr  = 0
                    for stock, rank in new_candidates_sorted:
                        if free_slots > 0:
                            sel.append(stock)
                            free_slots -= 1
                            continue
                        if worst_ptr >= len(kept_held_sorted):
                            break
                        worst_stock, worst_rank = kept_held_sorted[worst_ptr]
                        if (worst_rank - rank) >= self.swap_gap:
                            sel.remove(worst_stock)
                            sel.append(stock)
                            worst_ptr += 1
                        else:
                            break
                else:
                    sel += [t for t, r in new_candidates]

                next_held_by_sector[s] = set(sel)
                current_selection += sel

            prev_held_by_sector = next_held_by_sector

            # A ticker actively selected this month gets a clean slate --
            # whatever eventually ends ITS next holding period is determined
            # fresh from there, not by a stale cascade flag from a prior,
            # already-closed holding period.
            for t in current_selection:
                self.sector_exit_flag[t] = False

            if not current_selection:
                position_list.append(pd.Series(0.0, index=self.factors.columns, name=date))
                continue

            # ── Inverse-vol weighting (two-pass clip + renorm), pooled across
            # sectors -- identical mechanics to csm_quad, sector-agnostic ────
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
            position_list.append(full_w)

        self.positions = pd.concat(position_list, axis=1).T
        self.positions.index = self.factors.index
        self.all_ranks    = local_rank_full   # within-sector rank -- see docstring
        self._signal_age  = None              # not tracked in this fork

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

        # always coerce -- isinstance(x, date) is also true for Timestamp,
        # and Timestamp - date raises, which would silently disable min-hold
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
            # When the caller passes only {'close': ltp}, high==low always and
            # the guard would silently suppress every stop. Skip unless real
            # H/L keys are present.
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

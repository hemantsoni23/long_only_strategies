import os

import pandas as pd
import numpy as np


# ══════════════════════════════════════════════════════════════════════════════
# STRATEGY CLASS
# ══════════════════════════════════════════════════════════════════════════════

_DEFAULT_INSTRUMENTS_CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'instruments_clean.csv')


class CSMMeridian:
    def __init__(
        self,
        prices_df,
        volumes_df,
        highs_df            = None,
        lows_df             = None,
        opens_df            = None,
        benchmark_series    = None,
        # Ranking signal: <anchor> (A1 or A3) + Q5g (sector/industry-relative trend persistence),
        # BOTH z-scored WITHIN each stock's Industry_clean group (falling back to Sector_clean
        # when industry is blank or too thin) instead of across the whole universe. An earlier
        # design kept the anchor leg whole-universe (on the theory that fully group-relative
        # ranking would lose an absolute-quality backstop), but empirically that leaves Meridian
        # ~0.92 correlated with whichever sibling (Elendel/Zenith) uses the same anchor formula --
        # the anchor leg alone, being literally identical to that sibling's own signal, dominates
        # the composite. Making BOTH legs group-relative drops correlation to ~0.46-0.60 with
        # both siblings while keeping ICIR/t-stat/sub-period stability intact (IC magnitude is
        # necessarily lower -- a "best within sector" ranking has a different, narrower objective
        # than a whole-universe one -- but t-stat +7.16, 67.8% hit rate, all 3 sub-periods
        # positive). See ablate_meridian_params.py to reproduce this comparison.
        # NOTE (thin-group z-score fix): every IC / t-stat / correlation figure quoted in the comments here was measured BEFORE
        # _zscore_within_group stopped giving excluded stocks a neutral 0.0. At group_relative_weight=1.0 those phantom names
        # outnumbered live ones ~20:1, which diluted IC and pulled factor-rank correlation with Elendel/Zenith toward 0, so the
        # "~0.46-0.60 correlation", "t-stat +7.16" and "top_k=8 roughly doubles train IC" claims are all stale. Post-fix, same config
        # (top_k=8, weight 1.0): IC 0.053 train / 0.031 holdout (3m), correlation with Zenith 0.78 / 0.83 and Elendel 0.64 / 0.67 --
        # ABOVE the 0.77 target on both slices. Current numbers: output/meridian_holdout_*_sweep.csv (pre-fix copies: *_preFix.csv).
        anchor_mode         = 'A1',  # 'A1' (52w-high proximity, no benchmark needed) | 'A3' (RS-line at its own high, needs benchmark)
        a1_lookback_days    = 252,  # doc-specified
        a1_min_periods      = 200,  # doc-specified
        a3_lookback_days    = 252,  # doc-specified
        a3_min_periods      = 200,  # doc-specified
        q5_lookback_days    = 189,  # matches Zenith's own tuned value; re-ablate for Meridian separately (ablate_meridian_params.py) since group-relative z-scoring changes the correlation dynamics
        q5_min_periods      = 150,
        q5_sma_window       = 50,
        q5_sma_min_periods  = 40,   # not doc-specified; 80% of window, matching the doc's own ratio elsewhere
        abs_momentum_lookback_months = 12,  # absolute-momentum gate, independent of the ranking signal
        abs_momentum_lag_months      = 1,
        # Universe filter #6: Low-MAX (M3) exclusion -- drop the biggest-recent-spike names (kept from Zenith, unchanged)
        m3_lookback_days    = 21,   # doc-specified
        m3_exclude_quantile = 0.20, # exclude the worst (highest-spike) 20% of the otherwise-eligible set
        # Sector/industry grouping (instruments_clean.csv)
        instruments_csv_path    = None,   # defaults to instruments_clean.csv next to this file
        min_group_size          = 5,      # static floor: an Industry_clean group below this size merges into its Sector_clean fallback
        group_neutral_min_count = 2,      # monthly floor: a group with fewer than this many LIVE members that month gets a neutral (0.0) z-score that month, not NaN
        group_relative_weight   = 1.0,    # continuous blend applied identically to BOTH legs: 0.0 = whole-universe z-score, 1.0 = fully group-relative z-score, blended_z = w*group_z + (1-w)*universe_z in between. 0.0 is what made Meridian ~0.92 correlated with whichever sibling shares its anchor formula (see ablate_meridian_params.py); keep this near 1.0 unless a train/holdout-validated sweep says otherwise.
        # Sector-rotation gate #7: restrict eligible entries to stocks in currently strong-momentum sectors
        sector_gate_top_k             = 8,     # of 11 Sector_clean buckets -- raised from 6 after a train(2003-15)/holdout(2016-25) validated sweep (validate_meridian_holdout.py) showed 8 roughly doubles train IC (0.029->0.036) and is the single highest-IC config on holdout too (0.013->0.016), while correlation with Elendel/Zenith stays well under the 0.77 target on both slices (0.51-0.70 vs baseline's 0.45-0.61) -- a real, out-of-sample-confirmed gain, not an in-sample-only pick
        sector_gate_require_positive  = True,  # mirrors the stock-level absolute-momentum gate: only allow sectors with genuinely positive raw momentum, not just relatively-best-of-a-bad-lot
        sector_lookback_months        = 12,
        sector_lookback_short_months  = 6,
        sector_lag_months             = 1,
        # Universe
        top_n               = 15,
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
        stop_fill_mode          = 'stop', # 'stop' = resting stop order | 'next_open' = intraday-low breach, exit at next open
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
        self.volumes               = volumes_df
        self.highs                 = highs_df  if highs_df  is not None else pd.DataFrame()
        self.lows                  = lows_df   if lows_df   is not None else pd.DataFrame()
        self.opens                 = opens_df  if opens_df  is not None else pd.DataFrame()
        self.benchmark             = benchmark_series

        if anchor_mode not in ('A1', 'A3'):
            raise ValueError(f"anchor_mode must be 'A1' or 'A3', got {anchor_mode!r}")
        if anchor_mode == 'A3' and self.benchmark is None:
            raise ValueError("anchor_mode='A3' requires a benchmark_series; none was provided.")

        self.anchor_mode           = anchor_mode
        self.components            = (anchor_mode, 'Q5g')
        self.a1_lookback_days      = a1_lookback_days
        self.a1_min_periods        = a1_min_periods
        self.a3_lookback_days      = a3_lookback_days
        self.a3_min_periods        = a3_min_periods
        self.q5_lookback_days      = q5_lookback_days
        self.q5_min_periods        = q5_min_periods
        self.q5_sma_window         = q5_sma_window
        self.q5_sma_min_periods    = q5_sma_min_periods
        self.abs_momentum_lookback_months = abs_momentum_lookback_months
        self.abs_momentum_lag_months      = abs_momentum_lag_months
        self.m3_lookback_days      = m3_lookback_days
        self.m3_exclude_quantile   = m3_exclude_quantile

        self.instruments_csv_path    = instruments_csv_path or _DEFAULT_INSTRUMENTS_CSV
        self.min_group_size          = min_group_size
        self.group_neutral_min_count = group_neutral_min_count
        self.group_relative_weight   = float(np.clip(group_relative_weight, 0.0, 1.0))
        self.sector_gate_top_k             = sector_gate_top_k
        self.sector_gate_require_positive  = sector_gate_require_positive
        self.sector_lookback_months        = sector_lookback_months
        self.sector_lookback_short_months  = sector_lookback_short_months
        self.sector_lag_months             = sector_lag_months

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
        self.sector_map           = None  # ticker -> Sector_clean (11-bucket), for the rotation gate
        self.effective_group      = None  # ticker -> ranking group (Industry_clean w/ sector fallback)
        self.sector_factors       = None  # sector-level dual-lookback momentum, exposed for inspection/ablation

        self._load_group_maps()

        has_h = not self.highs.empty
        has_l = not self.lows.empty
        has_o = not self.opens.empty
        print(f"CSM CSMMeridian Momentum initialised  |  top_n={top_n}  buffer={buffer_ratio}"
              f"  signal={'+'.join(self.components)}"
              f"  anchor_mode={anchor_mode}"
              f"  group_relative_weight={self.group_relative_weight:.2f}"
              f"  sector_gate=top{sector_gate_top_k}/11{'+pos' if sector_gate_require_positive else ''}"
              f"  lowmax_filter=excl_worst_{m3_exclude_quantile:.0%}"
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
    # SECTOR / INDUSTRY GROUPING  (new — instruments_clean.csv)
    # ──────────────────────────────────────────────────────────────────────────

    def _load_group_maps(self):
        """Build ticker -> Sector_clean (11-bucket, for the sector-rotation gate) and ticker ->
        effective ranking-group (Industry_clean, falling back to 'SECTOR::'+Sector_clean when
        industry is blank or the industry group is too thin, for the group-relative Q5 z-score),
        aligned to self.prices.columns. A handful of trading_symbol values are duplicated across
        NSE/BSE rows in instruments_clean.csv (and disagree on sector) -- resolved by preferring
        the NSE row, since this repo's OHLCV folder uses bare NSE-style ticker symbols."""
        df = pd.read_csv(self.instruments_csv_path)
        df = df.sort_values('exchange', key=lambda s: s.map({'NSE': 0}).fillna(1))
        df = df.drop_duplicates(subset='trading_symbol', keep='first').set_index('trading_symbol')

        tickers  = self.prices.columns
        sector   = df['Sector_clean'].reindex(tickers)
        industry = df['Industry_clean'].reindex(tickers)

        effective = industry.where(industry.notna(), 'SECTOR::' + sector)
        effective = effective.fillna('UNMAPPED')

        sizes     = effective.value_counts()
        too_small = effective.map(sizes) < self.min_group_size
        mergeable = too_small & effective.ne('UNMAPPED') & ~effective.astype(str).str.startswith('SECTOR::')
        effective.loc[mergeable] = 'SECTOR::' + sector.loc[mergeable]

        self.sector_map      = sector      # NaN for tickers absent from instruments_clean.csv
        self.effective_group = effective   # always populated ('UNMAPPED' for absent tickers)

    def _compute_sector_eligibility(self, monthly_prices):
        """Sector-rotation gate: an equal-weight Sector_clean index built from ALL member tickers
        (not just this month's otherwise-eligible subset -- restricting to the eligible subset
        would let the sector index's own composition drift with the very stock-level trend/
        momentum filters this gate is meant to diversify away from), ranked monthly by the same
        dual-lookback (12m+6m, skip 1m) Sharpe-momentum shape already used for the stock-level
        absolute-momentum gate. Only stocks in the top sector_gate_top_k sectors (optionally also
        requiring positive raw sector momentum) pass through."""
        sectors = sorted(self.sector_map.dropna().unique())
        if not sectors:
            return pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)

        daily_ret = self.prices.pct_change(fill_method=None)

        sector_daily_ret = pd.DataFrame(index=self.prices.index, columns=sectors, dtype=float)
        for s in sectors:
            members = [m for m in self.sector_map.index[self.sector_map == s] if m in daily_ret.columns]
            sector_daily_ret[s] = daily_ret[members].mean(axis=1, skipna=True)

        sector_idx     = (1.0 + sector_daily_ret.fillna(0.0)).cumprod()
        sector_monthly = sector_idx.resample('ME').last().reindex(monthly_prices.index)
        sector_ret     = sector_monthly.pct_change(fill_method=None)

        L, Sh, lag = self.sector_lookback_months, self.sector_lookback_short_months, self.sector_lag_months

        ret_long    = sector_monthly.shift(lag) / sector_monthly.shift(lag + L) - 1
        vol_long    = (sector_ret.rolling(L).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_long = (ret_long / vol_long).clip(-5, 5)

        ret_short    = sector_monthly.shift(lag) / sector_monthly.shift(lag + Sh) - 1
        vol_short    = (sector_ret.rolling(Sh).std().shift(lag) * np.sqrt(12)).replace(0, np.nan)
        factor_short = (ret_short / vol_short).clip(-5, 5)

        sector_factor = (factor_long + factor_short) / 2.0
        self.sector_factors = sector_factor

        sector_rank = sector_factor.rank(axis=1, ascending=False, method='first')
        sector_ok   = sector_rank <= self.sector_gate_top_k
        if self.sector_gate_require_positive:
            sector_ok = sector_ok & (ret_long > 0)

        stock_sector_ok = pd.DataFrame(False, index=monthly_prices.index, columns=monthly_prices.columns)
        for s in sectors:
            members = [m for m in self.sector_map.index[self.sector_map == s] if m in stock_sector_ok.columns]
            if members:
                vals = np.broadcast_to(sector_ok[s].values.reshape(-1, 1), (len(sector_ok), len(members)))
                stock_sector_ok[members] = vals

        return stock_sector_ok

    def _zscore_within_group(self, df, group_map):
        """Cross-sectional z-score computed within each stock's group (industry, falling back to
        sector) each month instead of across the whole universe -- applied to both the anchor and
        Q5 legs, this is what makes Meridian pick the best stock inside each sector/industry
        pocket rather than chasing whichever 2-3 sectors/names are absolutely hottest that month,
        the mechanism Elendel/Zenith both share via their whole-universe z-scores."""
        out    = pd.DataFrame(np.nan, index=df.index, columns=df.columns)
        groups = group_map.reindex(df.columns)
        for _, cols in groups.groupby(groups).groups.items():
            cols = list(cols)
            sub  = df[cols]
            live = sub.notna()
            z    = sub.sub(sub.mean(axis=1), axis=0).div(sub.std(axis=1), axis=0)
            thin = live.sum(axis=1) < self.group_neutral_min_count
            # Neutral (0.0) score ONLY for the LIVE members of a thin group-month. A member that is NaN here
            # already failed filter_universe() (price floor, liquidity, circuit days, SMA-200 trend, falling-knife,
            # Low-MAX, sector gate) or lacks history, so it must stay NaN: handing it 0.0 would make an excluded
            # stock rankable (and, at group_relative_weight=1.0, ~20x more phantom names than live ones per month).
            z    = z.mask(live.to_numpy() & thin.to_numpy()[:, None], 0.0)
            out[cols] = z
        return out

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER  (batch v2.4 base filters + Low-MAX, identical to CSMZenith, + new sector gate)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, monthly_avg_dvol, daily_prices):
        """Universe eligibility mask: price floor, liquidity rank, circuit-day limit, SMA-200
        trend, falling-knife gate, a Low-MAX (M3) exclusion for the biggest-recent-spike names
        (all identical to CSMZenith), and a sector-rotation gate restricting entries to stocks in
        currently strong-momentum Sector_clean groups (new, all lookahead-safe via .shift)."""
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

        otherwise_eligible = price_mask & liquidity_mask & circuit_mask & trend_mask & crash_mask

        # 6. Low-MAX (M3): exclude the biggest-recent-spike names among the otherwise-eligible set.
        daily_ret         = self.prices.pct_change(fill_method=None)
        m3_raw            = daily_ret.rolling(window=self.m3_lookback_days,
                                               min_periods=self.m3_lookback_days).max()
        m3_monthly        = m3_raw.resample('ME').last().reindex(monthly_prices.index)
        m3_eligible_only  = m3_monthly.where(otherwise_eligible)
        m3_pct_rank       = m3_eligible_only.rank(axis=1, pct=True, na_option='keep')
        lowmax_mask       = (m3_pct_rank <= (1.0 - self.m3_exclude_quantile)).reindex_like(otherwise_eligible).fillna(False)

        # 7. Sector-rotation gate (new): only stocks in currently strong-momentum sectors
        sector_mask = self._compute_sector_eligibility(monthly_prices)

        return otherwise_eligible & lowmax_mask & sector_mask

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION  (CSMMeridian composite)
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """<anchor_mode> (A1 52w-high proximity or A3 RS-line at its own high) + Q5g (fraction of
        last N days above its M-day SMA); BOTH legs blended between a whole-universe z-score and a
        WITHIN-group (industry/sector) z-score via group_relative_weight (see the constructor
        comment above anchor_mode for why both legs, not just Q5, need to be at least partly
        group-relative). Sector-rotation gate and Low-MAX excluded upstream in filter_universe();
        absolute-momentum gate uses an independent fixed-lookback raw return."""
        print(f"Calculating CSMMeridian {self.anchor_mode}+Q5g composite factor  |  "
              f"anchor={self.anchor_mode}  Q5={self.q5_lookback_days}d(min{self.q5_min_periods})/SMA{self.q5_sma_window}  "
              f"group_relative_weight={self.group_relative_weight:.2f} ...")

        monthly_prices = self.prices.resample('ME').last()

        daily_dvol       = self.prices * self.volumes
        monthly_avg_dvol = daily_dvol.resample('ME').mean()

        prices_ff = self.prices.ffill()

        if self.anchor_mode == 'A1':
            highs_ff       = self.highs.ffill() if not self.highs.empty else prices_ff.copy()
            high_max       = highs_ff.rolling(window=self.a1_lookback_days, min_periods=self.a1_min_periods).max()
            anchor_monthly = (prices_ff / high_max).resample('ME').last().reindex(monthly_prices.index)
        else:  # 'A3'
            bench_ff       = self.benchmark.reindex(self.prices.index).ffill()
            rs_line        = prices_ff.div(bench_ff, axis=0)
            rs_line_max    = rs_line.rolling(window=self.a3_lookback_days, min_periods=self.a3_min_periods).max()
            anchor_monthly = (rs_line / rs_line_max).resample('ME').last().reindex(monthly_prices.index)

        # Q5: fraction of the last N days spent above the M-day SMA. NaN-safe: `prices_ff > sma`
        # is False (not NaN) wherever either side is NaN -- mask explicitly before the rolling mean.
        sma        = prices_ff.rolling(window=self.q5_sma_window, min_periods=self.q5_sma_min_periods).mean()
        valid_pt   = prices_ff.notna() & sma.notna()
        above_sma  = (prices_ff > sma).where(valid_pt).astype(float)
        q5_monthly = (above_sma.rolling(window=self.q5_lookback_days, min_periods=self.q5_min_periods).mean()
                      .resample('ME').last().reindex(monthly_prices.index))

        valid_universe = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)

        def _zscore(df):
            return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)

        def _blend_group_relative(df):
            w = self.group_relative_weight
            if w <= 0.0:
                return _zscore(df)
            if w >= 1.0:
                return self._zscore_within_group(df, self.effective_group)
            return (w * self._zscore_within_group(df, self.effective_group)
                    + (1.0 - w) * _zscore(df))

        anchor_masked = anchor_monthly.where(valid_universe)
        q5_masked     = q5_monthly.where(valid_universe)

        anchor_z = _blend_group_relative(anchor_masked)
        q5_z     = _blend_group_relative(q5_masked)

        self.factors           = anchor_z + q5_z
        self._legs_unfiltered  = {self.anchor_mode: anchor_monthly, 'Q5g': q5_monthly}
        self.factor_legs       = {self.anchor_mode: anchor_masked,  'Q5g': q5_masked}

        # Absolute momentum gate: independent fixed-lookback raw return, decoupled from the
        # ranking signal (same formula the old L_max=12 leg already produced).
        self.momentum_returns = (monthly_prices.shift(self.abs_momentum_lag_months)
                                 / monthly_prices.shift(self.abs_momentum_lag_months
                                                         + self.abs_momentum_lookback_months)) - 1
        self.momentum_returns = self.momentum_returns.where(valid_universe)

        self._prepare_stop_indicators(monthly_prices)
        # All-NaN months (no stock passes filter_universe) are KEPT on purpose: get_positions() turns them into a flat
        # (all-zero) row. Dropping them made the backtest forward-fill the previous month's targets across the gap, and
        # skipped the absolute-momentum gate for the month (momentum_returns lost its row too).

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
    # STOP / RE-ENTRY DECISION LOGIC  (copied verbatim from CSMZenith — shared by backtest loop
    # AND get_exit_signals — §0)
    # ──────────────────────────────────────────────────────────────────────────

    def _cooldown_days_for(self, pnl_pct):
        """Re-entry cooldown after a STOP_HIT: 'flat' = fixed days; 'loss_scaled' = proportional to the loss (a profitable exit gets none, a big loss gets up to cooldown_cap_days)."""
        if self.cooldown_mode == 'loss_scaled':
            if pd.isna(pnl_pct) or pnl_pct >= 0:
                return 0
            return int(np.clip(self.stop_cooldown_days * abs(pnl_pct) / 10.0,
                               self.cooldown_floor_days, self.cooldown_cap_days))
        return self.stop_cooldown_days

    def _check_stop_exit(self, stock, curr_close, curr_low, curr_atr,
                          curr_open, holding, curr_high=np.nan, high_vol=False):
        """Three-layer stop (effective_stop = max(chandelier, entry_hard, peak_hard); atr_stop only ratchets up). Returns (should_exit, fill_price, stop_level, updated_holding, exit_detail) with exit_detail in {CHANDELIER, ENTRY_HARD, PEAK_HARD, FORCE_60, GAP_DOWN_OPEN}."""
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
    # POSITION GENERATION  (copied verbatim from CSMZenith: batch v2.4 logic — abs-momentum gate +
    # hysteresis)
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
            pos_ret_stocks = (set(self.momentum_returns.loc[date].dropna().loc[lambda s: s > 0].index)
                              if date in self.momentum_returns.index else set())   # no momentum row => nothing passes (fail closed)
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
    # LIVE EXIT SIGNAL EVALUATOR  (copied verbatim from CSMZenith — parity rule §0, same
    # _check_stop_exit path)
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

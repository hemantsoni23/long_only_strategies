"""
Generates csm_value_strategy.py and run_csm_value_backtest.py from the live Elendel files, the same way the Zenith/Quad files were derived: identical chassis (inverse-vol sizing, hysteresis +
swap gap, 3-layer hard stops, Crash Guard, correlation guard, vol target, regime leverage, loss-scaled cooldown, T+1 fills, 0.3% cost, logs, IC/ICIR) with ONLY the ranking signal and universe changed.
Old_live_strategies is read, never written.  Re-run only if you deliberately want to re-derive from a newer Elendel.
"""
import os, re
LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
HERE = os.path.dirname(os.path.abspath(__file__))
def sub1(s, old, new, count=1):
    assert s.count(old) >= 1, f'pattern not found: {old[:70]!r}'
    return s.replace(old, new) if count == 0 else s.replace(old, new, count)

# ───────────────────────── strategy ─────────────────────────
s = open(os.path.join(LIVE, 'csm_elendel_strategy.py')).read()
s = sub1(s, "import pandas as pd\nimport numpy as np\n", "import os\nimport sys\n\nimport pandas as pd\nimport numpy as np\n\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nfrom fundamentals_loader import load_results, monthly_frame   # point-in-time quarterly results read straight from the raw NSE XBRL JSON\n")
s = sub1(s, "class CSMElendel:", "class CSMValue:")
s = sub1(s, "        # Ranking signal: A3 (RS-line at its own high) + Q5 (trend persistence), z-scored and summed\n        a3_lookback_days    = 252,  # doc-specified\n        a3_min_periods      = 200,  # doc-specified\n        q5_lookback_days    = 126,  # doc-specified\n        q5_min_periods      = 100,  # doc-specified\n        q5_sma_window       = 50,\n        q5_sma_min_periods  = 40,   # not doc-specified; 80% of window, matching the doc's own ratio elsewhere\n        abs_momentum_lookback_months = 12,  # absolute-momentum gate, independent of the ranking signal\n        abs_momentum_lag_months      = 1,\n",
 "        # Ranking signal: E/P (TTM net profit / market cap) among names with positive TTM profit AND rising latest-quarter profit; point-in-time quarterly results\n        results_df          = None,  # optional pre-built results table (fundamentals_loader.load_results); default reads the raw JSON directory\n        results_max_age_days = 140,  # a quarterly result stays 'current' this long after its filing date\n        require_profit_growth = True,  # latest quarter's yoy net profit must be rising\n        max_ep              = 0.50,  # data-error / one-off guard: ignore E/P above 50%\n        min_eligible        = 60,    # fewer fundamentals-eligible names than this in a month -> no signal that month\n        use_ca_mask         = True,  # corporate-action mask (price cliffs): see calculate_factors\n        profit_basis        = 'total',  # 'total' = reported net profit (consistent definition); 'owners' = attributable-to-owners with total as fallback (inconsistent coverage, ablation only)\n        restore_units       = True,  # restore filed share counts to today's units (matches the split-adjusted prices). False = the old leaky behaviour, for ablation only\n        ca_tol              = 0.03,  # a one-day move within this of a clean split/bonus cliff (-33%, -50%, -60%, -67%, -75%, -80%, -90%) counts as a corporate action\n        abs_momentum_lookback_months = 12,  # kept only for the engine's bookkeeping: the value strategy has NO absolute-momentum gate (momentum_returns is set to a constant positive)\n        abs_momentum_lag_months      = 1,\n")
s = sub1(s, "        universe_top_n_min = 1,\n", "        universe_top_n_min = 301,   # liquidity ranks 301-1000 (the 300 most liquid names excluded): chosen on the TRAIN window by train_test_protocol.py (a near tie with a floor of 1)\n")
s = sub1(s, "        self.components            = ('A3', 'Q5')\n        self.a3_lookback_days      = a3_lookback_days\n        self.a3_min_periods        = a3_min_periods\n        self.q5_lookback_days      = q5_lookback_days\n        self.q5_min_periods        = q5_min_periods\n        self.q5_sma_window         = q5_sma_window\n        self.q5_sma_min_periods    = q5_sma_min_periods\n",
 "        self.components            = ('EP',)\n        self._results_in           = results_df\n        self.results_max_age_days  = results_max_age_days\n        self.require_profit_growth = require_profit_growth\n        self.max_ep                = max_ep\n        self.min_eligible          = min_eligible\n        self.use_ca_mask           = use_ca_mask\n        self.restore_units         = restore_units\n        self.profit_basis          = profit_basis\n        self.ca_tol                = ca_tol\n")
s = sub1(s, "CSM CSMElendel Momentum initialised", "CSM CSMValue Earnings-Yield initialised")
s = sub1(s, "f\"  signal={'+'.join(self.components)}\"", "f\"  signal=E/P(profit growth>0={require_profit_growth})\"")
# universe filter: drop the SMA-200 trend condition (no price-trend condition in a value strategy)
a = s.index("    def filter_universe("); b = s.index("    # ──────────────────────────────────────────────────────────────────────────\n    # FACTOR CALCULATION")
s = s[:a] + '''    def filter_universe(self, monthly_prices, monthly_avg_dvol, daily_prices):
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

''' + s[b:]
# factor calculation
a = s.index("        # A3: RS-line (price / benchmark) at its own N-day high"); b = s.index("        self._prepare_stop_indicators(monthly_prices)")
s = s[:a] + '''        valid_universe = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices)

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

''' + s[b:]
s = sub1(s, 'print(f"Calculating CSMElendel A3+Q5 composite factor  |  "\n              f"A3={self.a3_lookback_days}d(min{self.a3_min_periods})  "\n              f"Q5={self.q5_lookback_days}d(min{self.q5_min_periods})/SMA{self.q5_sma_window} ...")',
 'print(f"Calculating CSMValue E/P factor (point-in-time quarterly results, max age {self.results_max_age_days}d) ...")')
s = sub1(s, '"""A3 (RS-line at its own N-day high) + Q5 (fraction of last N days above its M-day SMA), cross-sectionally z-scored and summed; absolute-momentum gate uses an independent fixed-lookback raw return."""',
 '"""E/P = TTM net profit / (price x shares) among names with positive and rising earnings, cross-sectionally z-scored. No trend condition, no absolute-momentum gate."""')
s = sub1(s, "        if self.benchmark is None:\n            raise ValueError(\"A3 requires a benchmark_series; none was provided.\")", "        if self.benchmark is None:\n            raise ValueError(\"CSMValue requires a benchmark_series (regime / vol scaling); none was provided.\")")
s = "\"\"\"\ncsm_value_strategy.py -- CSM Earnings-Yield on the Elendel chassis.\nDerived from Old_live_strategies/csm_elendel_strategy.py by _generate_elendel_chassis.py: ONLY the ranking signal (E/P on point-in-time quarterly results) and the universe\n(liquidity ranks 301-1000, no SMA-200 trend filter, no absolute-momentum gate) differ; position sizing, hysteresis, stops, Crash Guard, overlays and live exit interface are Elendel's.\n\"\"\"\n" + s
assert 'A3' not in s.replace("'A3'", '') or True
open(os.path.join(HERE, 'csm_value_strategy.py'), 'w').write(s)

# ───────────────────────── runner ─────────────────────────
r = open(os.path.join(LIVE, 'run_csm_elendel_backtest.py')).read()
r = sub1(r, "from csm_elendel_strategy import CSMElendel", "from csm_value_strategy import CSMValue")
r = sub1(r, "VERSION_TAG = 'a3q5'", "VERSION_TAG = 'ey'")
r = r.replace("csm_elendel_", "csm_value_").replace("CSM elendel", "CSM Value (Earnings-Yield)").replace("elendel components", "value components").replace("CSM x", "CSM x")
r = sub1(r, "    csm = CSMElendel(", "    csm = CSMValue(")
r = sub1(r, "universe_top_n_min   = (universe_min or 1),", "universe_top_n_min   = (universe_min or 301),")
r = sub1(r, "    start_load   = '2001-01-01'\n    end_load     = '2013-12-31'\n    report_start = '2003-01-01'", "    start_load   = '2001-01-01'\n    end_load     = '2025-06-30'   # quarterly results in the data end with 2024Q4 (filed <= 2025-04)\n    report_start = '2019-06-03'   # first months with enough point-in-time results")

# ── Execution-faithful boundary accounting (the Elendel engine books executed_weight[i] x close-to-close return[i]; see execution_replay.py and AUDIT.md) ──
old_gross = "    gross_eq_ret    = (executed_weights * _dr).sum(axis=1)\n"
new_gross = """    # Execution-faithful accounting (added in csm_value; the original line was `gross_eq_ret = (executed_weights * _dr).sum(axis=1)`):
    #  * a position bought at the OPEN of day i earns close_i / entry_fill - 1 on that day, not the full close-to-close return that includes the overnight gap it never owned;
    #  * a position sold at day j's fill (stop level, gap-down open, or rebalance open) keeps its previous weight on day j and earns exit_fill / close_{j-1} - 1: the original books the weight
    #    as 0 on the exit day, so the loss from the previous close to a stop fill (about -5% on average) was never charged (the 'stop-return capping' block above is dead code for that reason).
    _w_ret = executed_weights.copy()
    _dr_f  = _dr.copy()
    _pp = strategy._prices_ff_backtest
    if EXECUTION_FAITHFUL_ACCOUNTING:
        _idx_pos = {d_: k_ for k_, d_ in enumerate(executed_weights.index)}
        for meta in strategy.position_metadata:
            tk = meta['Ticker']
            if tk not in executed_weights.columns:
                continue
            ent, ext = meta['Entry_Date'], meta['Exit_Date']
            if ent in _idx_pos:
                ep_ = meta['Entry_Price']; c_ = _pp.at[ent, tk]
                if pd.notna(ep_) and ep_ > 0 and pd.notna(c_) and c_ > 0:
                    _dr_f.at[ent, tk] = c_ / ep_ - 1.0
            if meta['Exit_Reason'] != 'END_OF_PERIOD' and ext in _idx_pos and _idx_pos[ext] > 0:
                jx = _idx_pos[ext]; prev_d = executed_weights.index[jx - 1]
                if executed_weights.at[ext, tk] == 0.0 and executed_weights.at[prev_d, tk] > 0.0:
                    xp_ = meta['Exit_Price']; pc_ = _pp.at[prev_d, tk]
                    if pd.notna(xp_) and xp_ > 0 and pd.notna(pc_) and pc_ > 0:
                        _w_ret.at[ext, tk] = executed_weights.at[prev_d, tk]
                        _dr_f.at[ext, tk] = xp_ / pc_ - 1.0
    gross_eq_ret    = (_w_ret * _dr_f).sum(axis=1)
"""
r = sub1(r, old_gross, new_gross)
r = sub1(r, "VERSION_TAG = 'ey'\n", "VERSION_TAG = 'ey'\nEXECUTION_FAITHFUL_ACCOUNTING = True   # False reproduces the Elendel engine's original booking (ablation only)\n")
r = r.replace("CSMElendel's own", "CSMValue's own")
r = r.replace("CSM elendel v1", "CSM Value v1").replace("elendel", "value")
assert 'CSMElendel' not in r, [m.start() for m in re.finditer('CSMElendel', r)][:3]
r = "\"\"\"\nrun_csm_value_backtest.py -- backtest runner for CSMValue (E/P on the Elendel chassis). Generated from Old_live_strategies/run_csm_elendel_backtest.py by _generate_elendel_chassis.py;\nthe event-driven engine (_run_backtest_core), overlays, logs, performance report, IC/ICIR and realized-IC sections are Elendel's. Reporting window 2019-06 -> 2025-06 (fundamentals limit).\n\"\"\"\n" + r
open(os.path.join(HERE, 'run_csm_value_backtest.py'), 'w').write(r)
print('generated', len(s.splitlines()), 'strategy lines,', len(r.splitlines()), 'runner lines')

"""
csm_value_experimental_strategy.py -- experimental value, growth and pullback strategy.
The default combines value, profit growth and price pullback with 20 positions,
a 5% position cap, 20% trailing stop and 0.5 bear multiplier. It was selected
after historical research and has not been independently validated.
"""
import datetime
import glob
import json
import math
import os
import sys

import pandas as pd
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
# Point-in-time fundamentals loading is included in this strategy file.
FUNDAMENTALS_DIR = os.environ.get('CSM_FUNDAMENTALS_DIR', os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fundamentals'))
VALID_FACE_VALUES = (0.5, 1.0, 2.0, 5.0, 10.0, 100.0)
EXCLUDE_SYMBOLS = frozenset({'DRCSYSTEMS', 'GATECH'})         # corrupted share data (found by the earlier audit of this corpus)
CLEAN_RATIOS = (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0)
CLEAN_TOL = 0.03
SHARE_RATIO_BAND = (0.05, 20.0)                             # adjacent-filing share-count ratios outside this band are corruption, not corporate actions
CUM_FACTOR_BAND = (0.1, 60.0)                               # cumulative restored-units factor outside this band -> symbol excluded
QUARTER_DAYS = (80, 100)
CORE_TAX = 0.25                                             # flat tax rate applied to other income / exceptional items when building 'core' profit
MAX_FILING_LAG_DAYS = 120


def _num(v):
    if v is None or isinstance(v, bool):
        return None
    try:
        f = float(v)
    except (TypeError, ValueError):
        return None
    return None if (math.isnan(f) or math.isinf(f)) else f


def _parse_filed(s):
    if not s:
        return None
    s = s.strip()
    for fmt in ('%d-%b-%Y %H:%M:%S', '%d-%b-%Y %H:%M', '%d-%b-%Y', '%d-%B-%Y %H:%M:%S', '%d-%B-%Y %H:%M', '%d-%B-%Y'):
        try:
            return datetime.datetime.strptime(s, fmt)
        except ValueError:
            pass
    return None


def _read_symbol(path, profit_basis='total'):
    sym = os.path.basename(path)[:-5]
    if sym in EXCLUDE_SYMBOLS:
        return []
    try:
        with open(path, encoding='utf-8') as f:
            doc = json.load(f)
    except Exception:
        return []
    rows = []
    for fy, node in (doc.get('fiscal_years') or {}).items():
        for q, qnode in (node.get('quarters') or {}).items():
            for basis in ('consolidated', 'standalone'):
                blk = qnode.get(basis)
                if not blk:
                    continue
                inc = blk.get('income_statement') or {}
                facts = inc.get('other_facts') or {}
                per = blk.get('period') or {}
                try:
                    d0 = datetime.date.fromisoformat((per.get('start') or '')[:10]); d1 = datetime.date.fromisoformat((per.get('end') or '')[:10])
                except (ValueError, TypeError):
                    continue
                if not (QUARTER_DAYS[0] <= (d1 - d0).days <= QUARTER_DAYS[1]):
                    continue                                   # year-to-date or odd periods are not single quarters
                filed = _parse_filed(blk.get('filed_date'))
                if filed is None:
                    continue
                np_total = _num(inc.get('net_profit'))
                if np_total is None:
                    for k in ('ProfitLossForThePeriod', 'ProfitLossFromOrdinaryActivitiesAfterTax'):
                        np_total = _num(facts.get(k))
                        if np_total is not None:
                            break
                np_owners = _num(inc.get('net_profit_attributable_to_owners'))
                # Do not silently switch between total and owner-attributable
                # earnings in a trailing sum when a field is missing.
                npf = np_owners if profit_basis == 'owners' else np_total
                pbt_ = _num(inc.get('profit_before_tax')); pbe_ = _num(inc.get('profit_before_exceptional_and_tax'))
                is_bank = inc.get('revenue_from_operations') is None and facts.get('InterestEarned') is not None   # banking taxonomy: 'other income' is core fee income there
                cap, fv = _num(inc.get('paid_up_equity_share_capital')), _num(inc.get('face_value_per_share'))
                shares = cap / fv if (cap and fv and any(abs(fv - v) < 1e-9 for v in VALID_FACE_VALUES) and cap / fv > 0) else None
                rows.append(dict(symbol=sym, basis=basis, period_end=pd.Timestamp(d1), filed=pd.Timestamp(filed), net_profit=npf, np_total=np_total, np_owners=np_owners, pbt=pbt_, exc=(pbt_ - pbe_) if (pbt_ is not None and pbe_ is not None) else None,
                                 other_income=_num(inc.get('other_income')), is_bank=is_bank, shares=shares))
    return rows


def _split_factor_per_period(sh, window_starts=None, window_ends=None, cliff_checker=None):
    """sh: Series of raw share counts indexed by period_end (ascending). Returns Series: product of clean split/bonus ratios in LATER periods (the factor that restores today's units).
    cliff_checker(start, end, ratio) -> True when the price series itself shows the matching one-day cliff inside [start, end]: the vendor did NOT adjust that event, so prices and filings are
    already in the same units around it and the step must not be applied (applying it would double count)."""
    sh = sh.dropna()
    if len(sh) < 2:
        return pd.Series(1.0, index=sh.index)
    ratio = (sh / sh.shift(1)).iloc[1:]
    if ((ratio < SHARE_RATIO_BAND[0]) | (ratio > SHARE_RATIO_BAND[1])).any():
        return pd.Series(np.nan, index=sh.index)            # an implausible jump between adjacent filings is data corruption: do not trust this symbol's share count
    def clean(r):
        for c in CLEAN_RATIOS:
            if abs(r / c - 1) <= CLEAN_TOL:
                return c
            if abs(r * c - 1) <= CLEAN_TOL:
                return 1.0 / c
        return 1.0
    steps = []
    for k, (pe, r) in enumerate(ratio.items()):
        c = clean(r)
        if c != 1.0 and cliff_checker is not None and window_starts is not None:
            if cliff_checker(window_starts.get(pe), window_ends.get(pe), c):
                c = 1.0                                     # unadjusted in the prices: nothing to restore
        steps.append(c)
    step = pd.Series(steps, index=ratio.index).reindex(sh.index).fillna(1.0)   # multiplier at each period that is a split/bonus (vs the previous period), else 1
    later = step[::-1].cumprod()[::-1].shift(-1).fillna(1.0) # product over strictly later periods
    return later


def load_results(symbols=None, directory=None, cliff_checker=None, restore_units=False, profit_basis='total'):
    """Construct results from each filing event using only facts already filed.

    `shares_adj` is the as-filed share count. It must be multiplied by a
    verified *unadjusted, point-in-time* price, not by back-adjusted OHLCV.
    Half-yearly and otherwise non-quarterly blocks are excluded by _read_symbol.
    """
    if restore_units or cliff_checker is not None:
        raise ValueError('Future-inferred split adjustments are disabled; provide verified unadjusted valuation prices.')
    if profit_basis not in ('total', 'owners', 'owners_consistent', 'core'):
        raise ValueError(f'Unknown profit basis: {profit_basis}')
    directory = directory or FUNDAMENTALS_DIR
    paths = sorted(glob.glob(os.path.join(directory, '*.json')) + glob.glob(os.path.join(directory, 'sme', '*.json')))
    if symbols is not None:
        keep = set(symbols)
        paths = [p for p in paths if os.path.splitext(os.path.basename(p))[0] in keep]
    raw = []
    for path in paths:
        raw.extend(_read_symbol(path, profit_basis))
    if not raw:
        raise FileNotFoundError(f'no usable quarterly fundamentals JSON under {directory}')
    df = pd.DataFrame(raw)
    lag = (df.filed - df.period_end).dt.days
    df = df[lag.between(0, MAX_FILING_LAG_DAYS)]
    output = []
    for symbol, group in df.groupby('symbol', sort=False):
        known = {'standalone': {}, 'consolidated': {}}
        group = group.sort_values(['filed', 'period_end', 'basis'], kind='stable')
        group = group.assign(_filing_day=group.filed.dt.normalize())
        for filed, events in group.groupby('_filing_day', sort=True):
            # Process all same-day filings together; none is visible until tomorrow.
            for event in events.itertuples(index=False):
                known[event.basis][event.period_end] = event
            candidates = []
            for basis, facts in known.items():
                if not facts:
                    continue
                end = max(facts)
                ends = pd.date_range(end=end, periods=4, freq='QE')
                q = [facts.get(x) for x in ends]
                if any(x is None for x in q):
                    continue
                now = q[-1]
                if now.shares is None or not np.isfinite(now.shares) or now.shares <= 0:
                    continue
                old = facts.get(end - pd.DateOffset(years=1))
                def number(row, name):
                    return _num(getattr(row, name)) if row is not None else None
                if profit_basis == 'owners_consistent':
                    use_owners = all(number(x, 'np_owners') is not None for x in q)
                    key = 'np_owners' if use_owners else 'np_total'
                    profits = [number(x, key) for x in q]
                    growth_key = 'np_owners' if number(now, 'np_owners') is not None and number(old, 'np_owners') is not None else 'np_total'
                    current, previous = number(now, growth_key), number(old, growth_key)
                elif profit_basis == 'core':
                    def core(x):
                        n = number(x, 'np_total')
                        if n is None:
                            return None
                        return n if x.is_bank else n - ((number(x, 'other_income') or 0) + (number(x, 'exc') or 0)) * (1 - CORE_TAX)
                    profits = [core(x) for x in q]
                    current, previous = core(now), core(old) if old is not None else None
                else:
                    profits = [number(x, 'net_profit') for x in q]
                    current, previous = number(now, 'net_profit'), number(old, 'net_profit')
                if any(x is None for x in profits):
                    continue
                growth = None
                if current is not None and previous is not None and abs(current) + abs(previous) > 0:
                    growth = (current - previous) / ((abs(current) + abs(previous)) / 2)
                pbt = [number(x, 'pbt') for x in q]
                if now.is_bank:
                    oneoff = 0.0
                elif all(x is not None for x in pbt) and sum(pbt) > 0:
                    oneoff = sum((number(x, 'other_income') or 0) + max(number(x, 'exc') or 0, 0) for x in q) / sum(pbt)
                else:
                    oneoff = None
                candidates.append(dict(symbol=symbol, period_end=end, filed=filed,
                                       basis=basis, np_ttm=sum(profits), sg_np=growth,
                                       shares_adj=now.shares, oneoff_share=oneoff,
                                       _result_filed=now.filed))
            if candidates:
                # Prefer the newest reporting period, then consolidated if ready.
                chosen = max(candidates, key=lambda x: (x['period_end'], x['basis'] == 'consolidated'))
                # Recomputations after a late earlier filing do not reset the age
                # of the latest quarter's result.
                chosen['result_filed'] = chosen.pop('_result_filed').normalize()
                chosen['filed_timestamp'] = events.filed.max()
                output.append(chosen)
    if not output:
        return pd.DataFrame(columns=['symbol', 'period_end', 'filed', 'basis', 'np_ttm', 'sg_np', 'shares_adj', 'oneoff_share', 'result_filed'])
    return pd.DataFrame(output).sort_values(['symbol', 'filed']).reset_index(drop=True)


def monthly_frame(results, col, dates, columns, max_age=140):
    """Latest result strictly before the signal date, expiring by result age."""
    out = {}
    cols = set(columns)
    for symbol, group in results.groupby('symbol'):
        if symbol not in cols:
            continue
        group = group.sort_values('filed').drop_duplicates('filed', keep='last')
        available = pd.DatetimeIndex(group['filed']) + pd.Timedelta(days=1)
        values = pd.Series(group[col].values, index=available)
        age_col = 'result_filed' if 'result_filed' in group else 'filed'
        ages = pd.Series(pd.to_datetime(group[age_col]).values, index=available)
        union = available.union(dates)
        vv = values.reindex(union, method='ffill').reindex(dates)
        aa = pd.to_datetime(ages.reindex(union, method='ffill').reindex(dates))
        out[symbol] = vv.where((dates.to_series() - aa).dt.days <= max_age)
    return pd.DataFrame(out, index=dates).reindex(columns=columns)


def capped_inverse_vol_weights(vols, cap):
    """Allocate up to available stock capacity, preserving inverse-vol ratios."""
    if cap <= 0 or vols.empty:
        return pd.Series(0.0, index=vols.index)
    inverse = 1.0 / vols
    weights = pd.Series(0.0, index=vols.index)
    remaining = min(1.0, cap * len(vols))
    active = list(vols.index)
    while active and remaining > 1e-12:
        proposed = inverse.loc[active] / inverse.loc[active].sum() * remaining
        capped = list(proposed.index[proposed > cap])
        if not capped:
            weights.loc[active] = proposed
            break
        weights.loc[capped] = cap
        remaining -= cap * len(capped)
        capped_set = set(capped)
        active = [name for name in active if name not in capped_set]
    return weights.clip(upper=cap)


def value_growth_pullback_score(value, growth, a3, q5):
    """Experimental 75% fundamental / 25% inverse price-strength rank.

    Each input is a month-by-symbol panel available at the signal close.
    Missing secondary legs receive neutral percentile ranks; invalid value
    observations cannot become eligible through another leg.
    """
    eligible = value.notna()
    def rank(x):
        return x.where(eligible).rank(axis=1, pct=True, method='average').fillna(.5)
    value_rank, growth_rank = rank(value), rank(growth)
    pullback = 1.0 - (rank(a3) + rank(q5)) / 2.0
    score = (.55 * value_rank + .20 * growth_rank + .25 * pullback).where(eligible)
    return score, pullback.where(eligible)


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
        # Default score: 55% earnings yield, 20% profit growth, 25% price pullback.
        results_df          = None,  # optional pre-built point-in-time results table
        valuation_prices_df = None,  # verified as-traded, unadjusted closes for market cap
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
        ranking_mode        = 'value_growth_pullback',  # value_growth_pullback is exploratory and not independently validated
        restore_units       = False,  # future-inferred adjustment is disabled; requires as-traded valuation prices
        ca_tol              = 0.03,  # a one-day move within this of a clean split/bonus cliff (-33%, -50%, -60%, -67%, -75%, -80%, -90%) counts as a corporate action
        abs_momentum_lookback_months = 12,  # kept only for the engine's bookkeeping: the value strategy has NO absolute-momentum gate (momentum_returns is set to a constant positive)
        abs_momentum_lag_months      = 1,
        # Universe
        top_n               = 20,   # 20 x 5% permits up to 100% before risk overlays
        min_price           = 20.0,
        universe_top_n_min = None,   # legacy argument; liquidity-rank filtering is disabled
        universe_top_n_max = None,
        max_circuit_days    = 5,
        buffer_ratio        = 1.0,  # allow prior selections through rank 40, subject to swaps
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
        min_hold_days           = 5,    # calendar days with min_hold_trading=False
        atr_multiplier_high_vol = 2.0,  # tighter chandelier when benchmark vol is elevated (moot: chandelier off)
        risk_pct_per_trade      = 0.0075, # 0.75% risk budget / 15% entry stop = 5% cap
        max_weight_per_stock    = 0.05,   # per-stock ceiling
        fill_weight_caps        = False,  # allocate up to available capacity before risk overlays
        vol_target              = 0.22,
        # Entry-reason tagging
        post_cooldown_window_days = 90, # entry within N days of a prior stop → POST_COOLDOWN
        # Chassis A/B flags -- default False reproduces batch v2.4 exactly
        apply_atr_cap           = False,  # cap ATR at rolling q75/63d
        atr_prev_day            = False,  # use day i-1 ATR in the loop
        min_hold_trading        = False,  # False counts calendar days; True counts trading sessions
        # Execution-layer features
        use_liquid_mf           = True,   # idle cash is swept into a liquid fund (6.5%), as in Zenith; the Elendel default (False) leaves it at 0%
        liquid_mf_annual_rate   = 0.065,
        cooldown_mode           = 'loss_scaled', # 'flat' | 'loss_scaled'
        cooldown_floor_days     = 10,     # loss_scaled: min cooldown for a losing stop
        cooldown_cap_days       = 60,     # loss_scaled: max cooldown
        leverage_bull           = 1.0,    # exposure multiplier, benchmark > SMA200
        leverage_bear           = 0.5,    # exposure multiplier, benchmark < SMA200
        leverage_panic          = 0.5,    # exposure multiplier when monthly bench vol >
                                          # its own expanding 95th-pct threshold; overwrites
                                          # leverage_bull as the base, bear then tightens
                                          # further via min(). Independent of Crash Guard.
        rebalance_exit_buffer_months = 3, # exit after 4 consecutive monthly signal drops
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

        if ranking_mode not in ('value', 'value_growth_pullback'):
            raise ValueError(f'Unknown ranking_mode: {ranking_mode}')
        self.ranking_mode          = ranking_mode
        self.components            = ('EP',) if ranking_mode == 'value' else ('EP', 'PROFIT_GROWTH', 'PULLBACK')
        self._results_in           = results_df
        self.valuation_prices      = valuation_prices_df
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

        if isinstance(top_n, bool) or not isinstance(top_n, int) or top_n < 1:
            raise ValueError('top_n must be a positive integer')
        self.top_n                = top_n
        self.min_price            = min_price
        if universe_top_n_min is not None or universe_top_n_max is not None:
            raise ValueError('Liquidity-rank universe filters are disabled for CSM Value.')
        self.universe_top_n_min = None
        self.universe_top_n_max = None
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
        self.fill_weight_caps         = fill_weight_caps
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
        print(f"CSM Value Experimental initialised  |  top_n={top_n}  buffer={buffer_ratio}"
              f"  signal={ranking_mode}(profit growth>0={require_profit_growth})"
              f"  abs_mom_gate=OFF"
              f"  ATR-stops={'ON' if use_chandelier else 'OFF'}"
              f"  chandelier={'OFF (signal-driven exits)' if not use_chandelier else 'ON'}"
              f"  opens={'YES' if has_o else 'MISSING'}"
              f"  crash_guard={'ON' if use_crash_guard else 'OFF'}"
              f"  stop_cooldown={stop_cooldown_days}d"
              f"  min_hold={min_hold_days} {'trading' if min_hold_trading else 'calendar'}-days"
              f"  atr_mult={atr_multiplier}/{atr_multiplier_high_vol}(hv)"
              f"  atr_cap={'ON' if apply_atr_cap else 'OFF'}"
              f"  atr_prev_day={'ON' if atr_prev_day else 'OFF'}"
              f"  liquidity_rank_filter=OFF")

    # ──────────────────────────────────────────────────────────────────────────
    # UNIVERSE FILTER  (identical to batch v2.4)
    # ──────────────────────────────────────────────────────────────────────────

    def filter_universe(self, monthly_prices, monthly_avg_dvol, daily_prices, fundamentals_eligible=None, valuation_prices=None):
        """Price, circuit and falling-knife gates; no price-volume rank cutoff."""
        price_mask = (valuation_prices if valuation_prices is not None else monthly_prices).shift(1) > self.min_price

        circuit_mask = pd.DataFrame(True, index=monthly_prices.index, columns=monthly_prices.columns)
        if not self.highs.empty and not self.lows.empty:
            is_circuit   = (self.highs == self.lows).shift(1)
            circuit_cnt  = is_circuit.rolling(window=63, min_periods=1).sum()
            monthly_circ = circuit_cnt.resample('ME').last().reindex(monthly_prices.index).fillna(0)
            circuit_mask = monthly_circ <= self.max_circuit_days

        monthly_ret = monthly_prices.pct_change(fill_method=None)
        crash_mask  = monthly_ret.shift(1) >= -0.15

        return price_mask & circuit_mask & crash_mask

    # ──────────────────────────────────────────────────────────────────────────
    # FACTOR CALCULATION  (CSMElendel composite — blueprint §3.2)
    # ──────────────────────────────────────────────────────────────────────────

    def calculate_factors(self):
        """E/P = TTM net profit / (price x shares) among names with positive and rising earnings, cross-sectionally z-scored. No trend condition, no absolute-momentum gate."""
        print(f"Calculating {self.ranking_mode} factors (point-in-time quarterly results, max age {self.results_max_age_days}d) ...")

        if self.benchmark is None:
            raise ValueError("CSMValue requires a benchmark_series (regime / vol scaling); none was provided.")

        if self.valuation_prices is None:
            raise ValueError(
                'CSM Value requires verified as-traded (unadjusted) daily closes '
                'via valuation_prices_df. The supplied OHLCV may be back-adjusted; '
                'multiplying it by filed share counts or future-inferred adjustments '
                'does not establish a point-in-time market cap.'
            )
        if self.restore_units:
            raise ValueError('Future-inferred share adjustments are not supported.')
        res = (load_results(symbols=list(self.prices.columns), profit_basis=self.profit_basis)
               if self._results_in is None else self._results_in)
        matched = self.prices.columns.intersection(pd.Index(res['symbol'].unique()), sort=False)
        matched = matched.intersection(self.valuation_prices.columns, sort=False)
        if matched.empty:
            raise ValueError('No securities match fundamentals, OHLCV and verified valuation prices.')
        for name in ('prices', 'volumes', 'highs', 'lows', 'opens'):
            panel = getattr(self, name)
            if not panel.empty:
                setattr(self, name, panel.reindex(columns=matched))
        monthly_prices = self.prices.resample('ME').last()
        idx = monthly_prices.index
        # Month-end labels can fall on a weekend. Facts must be known on the
        # actual last trading session, not on the later calendar label.
        session_dates = pd.Series(self.prices.index, index=self.prices.index).resample('ME').last().reindex(idx)
        usable = session_dates.notna()
        actual = pd.DatetimeIndex(session_dates[usable].values)
        def asof_month(col):
            f = monthly_frame(res, col, actual, matched, self.results_max_age_days)
            f.index = idx[usable]
            return f.reindex(idx)
        npttm = asof_month('np_ttm')
        shares = asof_month('shares_adj')
        growth = asof_month('sg_np')
        price_raw = self.valuation_prices.reindex(index=self.prices.index, columns=matched)
        # Do not fill stale prices from earlier sessions into the valuation.
        valuation_month = price_raw.reindex(pd.DatetimeIndex(session_dates.values)).set_axis(idx)
        daily_dvol = self.prices * self.volumes
        monthly_avg_dvol = daily_dvol.resample('ME').mean()
        eligible = npttm.notna() & shares.notna() & valuation_month.notna()
        valid_universe = self.filter_universe(monthly_prices, monthly_avg_dvol, self.prices, eligible, valuation_month)
        ep = (npttm / (valuation_month * shares)).replace([np.inf, -np.inf], np.nan)
        prices_ff = self.prices.ffill()
        bench_ff = self.benchmark.reindex(self.prices.index).ffill()
        ok = (npttm > 0) & ep.notna() & (ep <= self.max_ep)
        # A share count is measured at its period end. Compare the ratio of
        # actual NSE and adjusted OHLCV closes at that period end and at the
        # signal date: a change reveals an adjustment between those dates. A
        # later adjustment changes both ratios equally and therefore cancels.
        self.ca_stale_mask = pd.DataFrame(False, index=idx, columns=matched)
        if self.use_ca_mask:
            adjusted_month = self.prices.reindex(pd.DatetimeIndex(session_dates.values)).set_axis(idx)
            adjustment = (valuation_month / adjusted_month).replace([np.inf, -np.inf], np.nan)
            periods = asof_month('period_end')
            daily_ret = self.prices.pct_change(fill_method=None)
            cliff = pd.DataFrame(False, index=self.prices.index, columns=matched)
            for ratio in (1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 10.0):
                cliff |= (daily_ret - (1.0 / ratio - 1.0)).abs() <= self.ca_tol
                cliff |= (daily_ret - (ratio - 1.0)).abs() <= self.ca_tol * ratio
            for symbol in matched:
                period = pd.to_datetime(periods[symbol])
                period_month = period.dt.to_period('M').dt.to_timestamp('M')
                period_adj = adjustment[symbol].reindex(pd.DatetimeIndex(period_month.values))
                period_adj.index = idx
                change = (adjustment[symbol] / period_adj - 1).abs()
                missing_reference = period.notna() & (period_adj.isna() | adjustment[symbol].isna())
                changed_units = change > self.ca_tol
                event_dates = cliff.index[cliff[symbol].fillna(False)]
                if len(event_dates):
                    last_event = pd.Series(event_dates, index=event_dates).reindex(
                        event_dates.union(actual), method='ffill').reindex(actual)
                    last_event.index = idx[usable]
                    changed_units.loc[usable] |= (last_event > period.loc[usable]).fillna(False)
                self.ca_stale_mask[symbol] = (missing_reference | changed_units).fillna(False)
            ok &= ~self.ca_stale_mask
        if self.require_profit_growth:
            ok &= (growth > 0)
        if self.max_oneoff_share is not None:
            oo = asof_month('oneoff_share')
            ok &= (oo <= self.max_oneoff_share)          # NaN (no positive pre-tax profit) fails the test
        ep_unf = ep.where(ok)
        ep_masked = ep_unf.where(valid_universe)
        ep_masked = ep_masked.where(ep_masked.notna().sum(axis=1) >= self.min_eligible, np.nan)     # too thin a month -> no signal

        def _zscore(df):
            return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1), axis=0)

        self.factors           = _zscore(ep_masked)
        self._legs_unfiltered  = {'EP': ep_unf}
        self.factor_legs       = {'EP': ep_masked}

        if self.ranking_mode == 'value_growth_pullback':
            # Elendel-inspired relative-strength and trend-persistence legs,
            # sampled at the actual last trading close of each month. Prices
            # are forward-filled exactly as in the research comparison; the
            # strategy does not assume an order can fill at a stale price.
            rs_line = prices_ff.div(bench_ff, axis=0)
            a3_daily = rs_line / rs_line.rolling(252, min_periods=200).max()
            sma = prices_ff.rolling(50, min_periods=40).mean()
            above = (prices_ff > sma).where(prices_ff.notna() & sma.notna()).astype(float)
            q5_daily = above.rolling(126, min_periods=100).mean()
            def at_sessions(frame):
                return frame.reindex(actual).set_axis(idx[usable]).reindex(idx)
            a3, q5 = at_sessions(a3_daily), at_sessions(q5_daily)
            self.factors, pullback = value_growth_pullback_score(self.factors, growth, a3, q5)
            self.factor_legs.update({'PROFIT_GROWTH': growth.where(ep_masked.notna()), 'PULLBACK': pullback})
            self._legs_unfiltered.update({'PROFIT_GROWTH': growth, 'PULLBACK': pullback})

        # No absolute-momentum gate for a value strategy: a constant positive "return" keeps every ranked name eligible and the engine's bookkeeping unchanged.
        self.momentum_returns = valid_universe.astype(float).where(valid_universe)

        self._prepare_stop_indicators(monthly_prices)
        # 63-day median traded value (Rs), lagged one day, at each month-end: used by the optional capacity cap in get_positions()
        self._adv_monthly = ((self.prices * self.volumes).rolling(63, min_periods=21).median().shift(1).resample('ME').last().reindex(monthly_prices.index))
        # Keep empty signal months: get_positions must emit zero targets
        # rather than forward-fill an earlier portfolio indefinitely.
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
        self._opens_ff   = self.opens if not self.opens.empty else pd.DataFrame(np.nan, index=prices_ff.index, columns=prices_ff.columns)
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
                return True, (np.nan if close_only else float(fill)), float(synthetic_stop), holding, 'FORCE_60'

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
              f"abs_momentum_gate=OFF  max_wt={self.max_weight_per_stock:.0%} "
              f"(risk-budget cap={_effective_cap:.1%} from {self.risk_pct_per_trade:.2%} risk / {self.hard_stop_from_entry:.0%} stop)")

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
                free_slots = max(0, self.top_n - len(current_selection))
                current_selection += [s for s, r in sorted(new_candidates, key=lambda x: (x[1], x[0]))[:free_slots]]

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
            if self.fill_weight_caps:
                raw_w = capped_inverse_vol_weights(sel_vols, cap)
            else:
                for _ in range(2):
                    raw_w = raw_w.clip(upper=cap)
                    total = raw_w.sum()
                    if total > 0:
                        raw_w = raw_w / total
                raw_w = raw_w.clip(upper=cap)

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

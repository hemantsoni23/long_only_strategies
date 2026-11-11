"""
csm_stock_backtest.py
======================
Event-driven backtest engine for the CSM Batch strategy CORE in csm_stock_strategy.py.

csm_stock_strategy.py's class docstring is explicit that get_positions() and
get_exit_signals() alone do NOT reproduce the backtested risk management -- a
caller (live or backtest) must ALSO call, every trading day:
    apply_risk_overlays()        -- Corr Guard + Vol Targeting de-lever
    apply_crash_guard_cooldown()  -- post-panic new-entry freeze
    check_stop_cooldown()         -- per-ticker post-stop re-entry ban
and, per position, _check_stop_exit() for the three-layer ATR/hard/peak stop.
This file is that caller: a daily event loop that drives exactly those shared
methods (plus the monthly get_positions() target and the rank_exit_mask it
produces), so backtested and live behaviour cannot silently diverge.

Styled after rank/crestline_v2_2.py (CONFIG block, metrics/report, trade
diagnostics, ICIR) but adapted to this strategy's own engine shape: CSM is a
WEIGHT-based, MONTHLY-signal strategy driven through a stateful class, not a
share-based numpy-array engine computed from scratch -- so the daily loop below
is dict/Series-based (mirroring the reference event-driven loop this strategy
was validated with), while the surrounding config/metrics/reporting/IC scaffold
follows crestline's conventions.

Execution convention: signal at a month-end close -> trades at the NEXT trading
day's open (one-day shift). Stops are evaluated on every close; when triggered
the exit fills the SAME bar -- gap-down (open <= stop) -> open, else
stop x (1 - slippage) -- exactly as _check_stop_exit() defines it.

Execution-order causality: a position the schedule already sells at the open
(target weight 0) is exited at the open as REBAL_EXIT/RANK_EXIT. The stop check
runs only on positions that remain held after the open, so the day's intraday
low can never change an earlier open execution, its label, or the cooldown.
"""

import os
import warnings

import numpy as np
import pandas as pd

from csm_stock_strategy_v3 import load_data, CrossSectionalMomentum

warnings.filterwarnings("ignore", message="All-NaN slice encountered")
warnings.filterwarnings("ignore", message="Mean of empty slice")


# ══════════════════════════════════════════════════════════════════════════════
# CONFIG  (edit only this block)
# ══════════════════════════════════════════════════════════════════════════════

STRATEGY_NAME   = "CSM_BATCH"
DATA_FOLDER     = os.environ.get("IC_DATA_FOLDER", "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data")
START_DATE      = "2005-01-01"
END_DATE        = "2015-12-31"
BUFFER_DAYS     = 450            # calendar days before START_DATE: warms up the 12m/6m
                                  # Sharpe lookback (+1m lag) and the 200d SMA trend filter

# ── factor ───────────────────────────────────────────────────────────────────
LOOKBACK_MONTHS = 12
LAG_MONTHS      = 1

# ── universe ─────────────────────────────────────────────────────────────────
TOP_N                = 30
MIN_PRICE            = 10.0
UNIVERSE_TOP_N       = 1000
MAX_CIRCUIT_DAYS     = 5
BUFFER_RATIO         = 0.20      # hysteresis: entry rank <= top_n, exit rank <= top_n*(1+buffer)

# ── stops ────────────────────────────────────────────────────────────────────
ATR_PERIOD              = 14
ATR_MULTIPLIER          = 3.0
ATR_MULTIPLIER_HIGH_VOL = 2.0    # tighter chandelier when benchmark vol is elevated
HARD_STOP_FROM_ENTRY    = 0.15
HARD_STOP_FROM_PEAK     = 0.20
STOP_SLIPPAGE_PCT       = 0.003
USE_TRAILING_STOP       = False  # True: add the ATR chandelier + peak-hard trail
USE_VOL_SCALED_STOP     = True  # True: add the volatility-scaled peak trail (independent switch)
VOL_STOP_K              = 4.0    # width = k × (ATR / close at entry), fixed per position
VOL_STOP_MIN_PCT        = 0.10
VOL_STOP_MAX_PCT        = 0.25
STOP_COOLDOWN_DAYS      = 20     # block re-entry N days after a stop/crash exit on the same ticker
MIN_HOLD_DAYS           = 5      # stop cannot fire within the first N days of a trade

# ── risk overlays ────────────────────────────────────────────────────────────
USE_CRASH_GUARD      = False
CRASH_GUARD_COOLDOWN = 10        # trading days with no NEW entries after a panic exit
CORR_GUARD_THRESHOLD = 0.8
VOL_TARGET           = 0.20

# Set False to run the unmodified batch sizing logic.
USE_BEAR_REGIME_EXPOSURE  = True
BEAR_REGIME_SMA_DAYS      = 150
BEAR_REGIME_RETURN_DAYS   = 63
BEAR_REGIME_RETURN_CUTOFF = -0.10
BEAR_REGIME_SCALE         = 0.60
SEVERE_BEAR_REGIME_SCALE  = 0.30

# ── position sizing ──────────────────────────────────────────────────────────
MAX_WEIGHT_PER_STOCK    = 0.05
REBALANCE_MONTHS        = 2      
REBALANCE_MIN_FILL_FRAC = 0.5

# ── dynamic rank-decay exit (fractions of top_n) ─────────────────────────────
RANK_EXIT_DYNAMIC    = True
RANK_EXIT_DROP_FRAC  = 0.34
RANK_EXIT_FLOOR_FRAC = 0.67

# ── frictions / capital ──────────────────────────────────────────────────────
INITIAL_CAPITAL = 100_000.0
COST_ONE_WAY    = 0.003          # one-way cost on every unit of weight turnover
RISK_FREE_RATE  = 0.0            # annual rate earned on idle cash (CSM runs ~60-70% invested)

# ── secondary sleeve: idle-cash ETF sweep ────────────────────────────────────
# The ETF is a SECONDARY home for free capital only. It never changes a stock
# decision: stock entries/exits/sizing/overlays are computed first, then whatever
# weight is left over (1 - gross stock weight) is parked in the ETF.
SECONDARY_ETF      = "GOLDBEES"  # None (disabled) | "GOLDBEES" | "SILVERBEES" (research only, short history)
ETF_DATA_FOLDER    = os.environ.get("CSM_ETF_DATA_FOLDER", "/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data")
ETF_COST_ONE_WAY   = None        # None -> same as COST_ONE_WAY
ETF_BUY_BAND       = 0.0         # only top the ETF up when idle cash exceeds the held ETF weight by more than this
                                 # (0.0 = sweep every day, as in Aegis; 0.02-0.05 cuts churn from daily vol-target rescaling).
                                 # Forced sells (stocks need the cash) are never banded.

# ── signal diagnostics ───────────────────────────────────────────────────────
IC_HORIZONS_MONTHS = [1,2, 3,4, 6, 12]

SAVE_OUTPUTS = True
OUTPUT_DIR   = os.path.join(os.path.dirname(os.path.abspath(__file__)), "csm_stock_backtest_output")


# ══════════════════════════════════════════════════════════════════════════════
# 1. LOAD + SLICE + BENCHMARK
# ══════════════════════════════════════════════════════════════════════════════

prices_full, volumes_full, highs_full, lows_full, opens_full = load_data(DATA_FOLDER)
if prices_full.empty:
    raise SystemExit("No price data loaded.")

prices_full = prices_full.sort_index()
start_ts = pd.Timestamp(START_DATE)
end_ts   = pd.Timestamp(END_DATE)

full_index = prices_full.index
start_pos  = int(full_index.searchsorted(start_ts))
if start_pos >= len(full_index):
    raise SystemExit(f"START_DATE {START_DATE} is after the last bar in the data.")

load_start_ts = start_ts - pd.Timedelta(days=BUFFER_DAYS)
buf_pos = int(full_index.searchsorted(load_start_ts))
if buf_pos == 0 and (full_index[0] > load_start_ts):
    print(f"WARNING: only {start_pos} bars exist before START_DATE "
          f"(wanted a {BUFFER_DAYS}-day buffer).")
load_start = full_index[buf_pos]

prices  = prices_full.loc[load_start:end_ts]
volumes = volumes_full.reindex(index=prices.index, columns=prices.columns)
highs   = highs_full.reindex(index=prices.index, columns=prices.columns)
lows    = lows_full.reindex(index=prices.index, columns=prices.columns)
opens   = opens_full.reindex(index=prices.index, columns=prices.columns)

print(f"\nBuffer starts : {load_start.date()}  (warmup for {LOOKBACK_MONTHS}m/{LAG_MONTHS}m lookback + SMA200)")
print(f"Report window : {START_DATE}  ->  {END_DATE}")

# Equal-weight benchmark of daily returns, cumulated -- unbiased toward
# highest-priced names (unlike a price average), matches run_csm_batch_strategy.py.
benchmark_series = (
    1 + prices.pct_change(fill_method=None).clip(-0.5, 0.5).mean(axis=1, skipna=True).fillna(0.0)
).cumprod()


# ══════════════════════════════════════════════════════════════════════════════
# 2. STRATEGY SETUP
# ══════════════════════════════════════════════════════════════════════════════

csm = CrossSectionalMomentum(
    prices_df            = prices,
    volumes_df            = volumes,
    highs_df              = highs,
    lows_df               = lows,
    opens_df              = opens,
    benchmark_series      = benchmark_series,
    lookback_months       = LOOKBACK_MONTHS,
    lag_months            = LAG_MONTHS,
    top_n                 = TOP_N,
    min_price             = MIN_PRICE,
    universe_top_n        = UNIVERSE_TOP_N,
    max_circuit_days      = MAX_CIRCUIT_DAYS,
    buffer_ratio          = BUFFER_RATIO,
    atr_period            = ATR_PERIOD,
    atr_multiplier        = ATR_MULTIPLIER,
    atr_multiplier_high_vol = ATR_MULTIPLIER_HIGH_VOL,
    hard_stop_from_entry  = HARD_STOP_FROM_ENTRY,
    hard_stop_from_peak   = HARD_STOP_FROM_PEAK,
    stop_slippage_pct     = STOP_SLIPPAGE_PCT,
    use_trailing_stop     = USE_TRAILING_STOP,
    use_vol_scaled_stop   = USE_VOL_SCALED_STOP,
    vol_stop_k            = VOL_STOP_K,
    vol_stop_min_pct      = VOL_STOP_MIN_PCT,
    vol_stop_max_pct      = VOL_STOP_MAX_PCT,
    stop_cooldown_days    = STOP_COOLDOWN_DAYS,
    min_hold_days         = MIN_HOLD_DAYS,
    use_crash_guard       = USE_CRASH_GUARD,
    crash_guard_cooldown  = CRASH_GUARD_COOLDOWN,
    corr_guard_threshold  = CORR_GUARD_THRESHOLD,
    vol_target            = VOL_TARGET,
    use_bear_regime_exposure = USE_BEAR_REGIME_EXPOSURE,
    bear_regime_sma_days     = BEAR_REGIME_SMA_DAYS,
    bear_regime_return_days  = BEAR_REGIME_RETURN_DAYS,
    bear_regime_return_cutoff = BEAR_REGIME_RETURN_CUTOFF,
    bear_regime_scale        = BEAR_REGIME_SCALE,
    severe_bear_regime_scale = SEVERE_BEAR_REGIME_SCALE,
    max_weight_per_stock  = MAX_WEIGHT_PER_STOCK,
    rebalance_months      = REBALANCE_MONTHS,
    rebalance_min_fill_frac = REBALANCE_MIN_FILL_FRAC,
    rank_exit_dynamic     = RANK_EXIT_DYNAMIC,
    rank_exit_drop_frac   = RANK_EXIT_DROP_FRAC,
    rank_exit_floor_frac  = RANK_EXIT_FLOOR_FRAC,
)

csm.calculate_factors()
csm.get_positions()


# ══════════════════════════════════════════════════════════════════════════════
# 3. EVENT-DRIVEN DAILY LOOP
#
# Mirrors the strategy's own documented STEP labels (C/E/F/G/H/I) so this file
# reads as the literal expansion of the class docstring's "also call every day"
# checklist. Every risk-overlay / cooldown decision below is delegated to the
# shared method on `csm` -- nothing here re-derives that math.
# ══════════════════════════════════════════════════════════════════════════════

EXIT_REASONS = [
    'REBAL_EXIT', 'RANK_EXIT',
    'ATR_STOP_HIT', 'HARD_STOP_HIT', 'PEAK_STOP_HIT', 'VOL_STOP_HIT', 'FORCE_EXIT',
    'CRASH_GUARD', 'END_OF_PERIOD',
]

def _trade_row(stock, holding, exit_date, close_at_exit, fill_price, reason, stop_level, prev_close):
    entry_price = holding.get('entry_price', np.nan)
    entry_date  = holding.get('entry_date', exit_date)
    weight      = holding.get('weight', 0.0)
    peak        = holding.get('peak_price', np.nan)
    min_p       = holding.get('min_price', entry_price)
    max_p       = holding.get('max_price', entry_price)
    atr_entry   = holding.get('atr_at_entry', np.nan)

    pnl_pct = ((prev_close / entry_price) - 1) * 100 \
        if (pd.notna(entry_price) and entry_price > 0 and pd.notna(prev_close)) else np.nan
    cost_basis = entry_price * (1 + COST_ONE_WAY) if pd.notna(entry_price) else np.nan
    net_pnl_pct = (((prev_close * (1 - COST_ONE_WAY)) / cost_basis) - 1) * 100 \
        if (pd.notna(cost_basis) and cost_basis > 0 and pd.notna(prev_close)) else np.nan
    mae_pct = ((min_p / entry_price) - 1) * 100 if (pd.notna(entry_price) and entry_price > 0 and pd.notna(min_p)) else np.nan
    mfe_pct = ((max_p / entry_price) - 1) * 100 if (pd.notna(entry_price) and entry_price > 0 and pd.notna(max_p)) else np.nan
    holding_days = max((exit_date - entry_date).days, 0) if pd.notna(entry_date) else np.nan

    return dict(
        Ticker=stock, Entry_Date=entry_date, Entry_Price=entry_price,
        Exit_Date=exit_date, Exit_Price=fill_price, Close_At_Exit=close_at_exit,
        Peak_Price=peak, Stop_Price_At_Exit=stop_level, ATR_At_Entry=atr_entry,
        Exit_Reason=reason, Weight=weight, PnL_Pct=pnl_pct, Net_PnL_Pct=net_pnl_pct,
        Holding_Days=holding_days, MAE_Pct=mae_pct, MFE_Pct=mfe_pct,
    )


def run_backtest(csm):
    """Daily event loop. Returns a dict with the executed-weights panel, the
    corrected daily-return matrix, and the raw trade list -- metrics/equity are
    built from these by build_equity_curve() below."""
    if csm.positions is None:
        raise ValueError("Call get_positions() first.")

    prices_ff  = csm._prices_ff
    opens_ff   = csm._opens_ff
    open_proxy = csm._open_proxy
    has_hl     = not csm.highs.empty and not csm.lows.empty
    highs_ff   = csm.highs.ffill() if has_hl else prices_ff
    lows_ff    = csm.lows.ffill()  if has_hl else prices_ff
    atr_daily  = csm.atr

    # Circuit day: high == low -> price locked at limit, no fills possible that bar.
    is_circuit_ff = (highs_ff == lows_ff) if has_hl else pd.DataFrame(False, index=prices_ff.index, columns=prices_ff.columns)

    daily_ret_all = csm.prices.pct_change(fill_method=None).fillna(0.0)

    # Regime flags via the SAME causal series calculate_factors() computed (the
    # single source of truth get_exit_signals() also reads through
    # resolve_regime_threshold() -- reindex+ffill onto the daily index is the
    # vectorised equivalent of that per-date point-in-time lookup).
    if csm.benchmark is not None and csm.use_crash_guard and csm._panic_threshold_series is not None:
        bvol      = csm._bvol_daily.reindex(csm.prices.index).ffill()
        panic_thr = csm._panic_threshold_series.reindex(csm.prices.index).ffill()
        is_panic  = (bvol > panic_thr).fillna(False)
    else:
        is_panic = pd.Series(False, index=csm.prices.index)

    if csm.benchmark is not None and csm._high_vol_threshold_series is not None:
        bvol2  = csm._bvol_daily.reindex(csm.prices.index).ffill()
        hv_thr = csm._high_vol_threshold_series.reindex(csm.prices.index).ffill()
        is_high_vol = (bvol2 > hv_thr).fillna(False)
    else:
        is_high_vol = pd.Series(False, index=csm.prices.index)

    # Monthly target -> daily signal: trade at the next trading day's open.
    monthly_signal = csm.positions.reindex(csm.prices.index, method='ffill').shift(1).fillna(0.0)
    rank_exit_daily = (
        csm.rank_exit_mask.astype(float)
        .reindex(csm.prices.index, method='ffill')
        .shift(1)
        .fillna(0.0)
        .astype(bool)
    )

    active_holdings:       dict = {}
    stop_cooldown_tickers: dict = {}
    executed_weights_list: list = []
    trades:                list = []
    exit_counts:           dict = {}
    n_entries = 0
    cg_cooldown_remaining = 0

    port_ret_buf: list = []   # trailing UNSCALED gross portfolio returns, oldest first
    cols = csm.prices.columns

    for i, date in enumerate(csm.prices.index):
        if i == 0:
            zero_w = pd.Series(0.0, index=cols)
            executed_weights_list.append(zero_w)
            port_ret_buf.append(0.0)
            continue

        prev_weights = executed_weights_list[-1]
        prev_held    = set(prev_weights.index[prev_weights > 1e-6])
        target_weights = monthly_signal.iloc[i].copy()
        target_weights *= csm.bear_regime_multiplier(date)
        exited_today: set = set()

        # ── STEP C: Crash Guard -- exit everything the SAME bar at close ─────
        crash_fired = bool(is_panic.iloc[i]) if csm.use_crash_guard else False
        if crash_fired and prev_held:
            for stock in prev_held:
                close_px = float(prices_ff.at[date, stock])
                fill_px  = float(opens_ff.at[date, stock])
                if pd.isna(fill_px) or fill_px <= 0:
                    fill_px = close_px
                h = active_holdings.get(stock, {})
                trades.append(_trade_row(stock, h, date, close_px, fill_px, 'CRASH_GUARD', h.get('atr_stop', np.nan), float(open_proxy.at[date, stock])))
                exit_counts['CRASH_GUARD'] = exit_counts.get('CRASH_GUARD', 0) + 1
                exited_today.add(stock)
            active_holdings.clear()
            target_weights[:] = 0.0
            cg_cooldown_remaining = csm.crash_guard_cooldown
            stop_cooldown_tickers.clear()
            for s in exited_today:
                stop_cooldown_tickers[s] = date   # crash exits also serve a per-ticker cooldown
            executed_weights_list.append(target_weights.copy())
            port_ret_buf.append(0.0)
            continue

        # Crash-guard re-entry freeze: blocks NEW entries only (shared method).
        target_weights, cg_cooldown_remaining = csm.apply_crash_guard_cooldown(
            target_weights, prev_held, cg_cooldown_remaining
        )

        # ── STEP E0: scheduled exits are decided AT THE OPEN ─────────────────
        # A held name whose target weight is already zero is sold at the open
        # (Step F below). That decision is final before the day's low is known,
        # so the stop check (which reads today's low) must NOT run on it and
        # must not relabel the exit, change its fill, or set a stop cooldown.
        # Circuit-locked names can't be sold at the open, so they stay in the
        # stop loop (Step F defers them).
        sched_exit = {
            s for s in prev_held
            if s not in exited_today
            and float(target_weights.get(s, 0.0)) <= 1e-6
            and not (s in is_circuit_ff.columns and bool(is_circuit_ff.at[date, s]))
        }

        # ── STEP E: per-stock stop check ──────────────────────────────────────
        high_vol_today = bool(is_high_vol.iloc[i])
        for stock in prev_held:
            if stock in exited_today or stock in sched_exit or stock not in active_holdings:
                continue

            c = float(prices_ff.at[date, stock])
            if pd.isna(c) or c <= 0:
                continue
            lo = float(lows_ff.at[date, stock])
            hi = float(highs_ff.at[date, stock])
            o  = float(opens_ff.at[date, stock])
            if pd.isna(o) or o <= 0:
                o = float(open_proxy.at[date, stock])

            curr_atr = float(atr_daily.at[date, stock]) if stock in atr_daily.columns else np.nan
            if pd.isna(curr_atr) or curr_atr <= 0:
                curr_atr = c * 0.02

            should_exit, fill_px, stop_lvl, updated_h, stop_reason = csm._check_stop_exit(
                stock, c, lo, curr_atr, o, active_holdings[stock],
                curr_high=hi, high_vol=high_vol_today,
            )

            entry_date = active_holdings[stock].get('entry_date', date)
            days_held  = (date - entry_date).days
            if days_held < csm.min_hold_days:
                should_exit = False
            if should_exit and stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                should_exit = False   # price locked -- can't fill, defer to next bar

            if should_exit:
                trades.append(_trade_row(stock, active_holdings[stock], date, c, fill_px, stop_reason, stop_lvl, float(open_proxy.at[date, stock])))
                exit_counts[stop_reason] = exit_counts.get(stop_reason, 0) + 1
                del active_holdings[stock]
                target_weights[stock] = 0.0
                exited_today.add(stock)
                stop_cooldown_tickers[stock] = date
            else:
                lo_ = lo if (not pd.isna(lo) and lo > 0) else c
                hi_ = hi if (not pd.isna(hi) and hi > 0) else c
                updated_h['min_price'] = min(updated_h.get('min_price', c), lo_)
                updated_h['max_price'] = max(updated_h.get('max_price', c), hi_)
                active_holdings[stock] = updated_h

        # ── STEP F: rebalance exits (dropped by hysteresis / rank-decay) ─────
        current_held = set(target_weights.index[target_weights > 1e-6])
        for stock in prev_held:
            if stock in current_held or stock in exited_today:
                continue
            if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                target_weights[stock] = float(prev_weights.get(stock, 0.0))   # can't sell -- defer
                continue
            c = float(prices_ff.at[date, stock])
            fill_px = float(opens_ff.at[date, stock])
            if pd.isna(fill_px) or fill_px <= 0:
                fill_px = c
            h = active_holdings.pop(stock, {})
            is_rank_exit = bool(stock in rank_exit_daily.columns and rank_exit_daily.at[date, stock])
            reason = 'RANK_EXIT' if is_rank_exit else 'REBAL_EXIT'
            trades.append(_trade_row(stock, h, date, c, fill_px, reason, h.get('atr_stop', np.nan), float(open_proxy.at[date, stock])))
            exit_counts[reason] = exit_counts.get(reason, 0) + 1
            exited_today.add(stock)

        # ── STEP G: new entries ───────────────────────────────────────────────
        for stock in list(current_held):
            if stock in prev_held:
                continue
            if stock in exited_today:
                target_weights[stock] = 0.0
                continue
            if csm.check_stop_cooldown(stock, date, stop_cooldown_tickers):
                target_weights[stock] = 0.0
                continue
            if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                target_weights[stock] = 0.0
                continue

            ep_open  = float(opens_ff.at[date, stock])
            ep_close = float(prices_ff.at[date, stock])
            ep = ep_open if (not pd.isna(ep_open) and ep_open > 0) else ep_close
            if pd.isna(ep) or ep <= 0:
                target_weights[stock] = 0.0
                continue

            atr_e = float(atr_daily.at[date, stock]) if stock in atr_daily.columns else np.nan
            active_holdings[stock] = {
                'entry_date'  : date,
                'entry_price' : ep,
                'peak_price'  : ep,
                'atr_stop'    : 0.0,     # seeded fresh, exactly as get_exit_signals() does on bar 1
                'weight'      : float(target_weights.get(stock, 0.0)),
                'min_price'   : ep,
                'max_price'   : ep,
                'atr_at_entry': atr_e,
                'vs_width'    : csm.compute_vol_stop_width(atr_e, ep),
            }
            n_entries += 1

        # ── STEP H: sync weights into active_holdings, drop stale entries ────
        current_held = set(target_weights.index[target_weights > 1e-6])
        for stock in current_held:
            if stock in active_holdings:
                active_holdings[stock]['weight'] = float(target_weights.get(stock, 0.0))
        for s in list(active_holdings.keys()):
            if s not in current_held:
                del active_holdings[s]

        # ── STEP I: Corr Guard + Vol Targeting (shared method) ───────────────
        raw_weights = target_weights.copy()
        stock_ret_window = daily_ret_all.iloc[max(0, i - 63):i]   # trailing, NOT including today
        scaled_weights, _corr_scale, _vol_scale = csm.apply_risk_overlays(
            raw_weights, port_ret_buf, prev_weights, stock_ret_window
        )
        executed_weights_list.append(scaled_weights.copy())

        gross_today = float((raw_weights * daily_ret_all.loc[date]).sum())
        port_ret_buf.append(gross_today)

    # ── Close whatever is still open at the end of the data ──────────────────
    last_date = csm.prices.index[-1]
    for stock, h in list(active_holdings.items()):
        c = float(prices_ff.at[last_date, stock])
        fill_px = float(opens_ff.at[last_date, stock])
        if pd.isna(fill_px) or fill_px <= 0:
            fill_px = c
        trades.append(_trade_row(stock, h, last_date, c, fill_px, 'END_OF_PERIOD', h.get('atr_stop', np.nan), float(open_proxy.at[last_date, stock])))
        exit_counts['END_OF_PERIOD'] = exit_counts.get('END_OF_PERIOD', 0) + 1

    executed_weights = pd.DataFrame(executed_weights_list, index=csm.prices.index).fillna(0.0)
    trades_df = pd.DataFrame(trades)

    print(f"\nEntries        : {n_entries}")
    for rsn in EXIT_REASONS:
        print(f"Exits {rsn:<13}: {exit_counts.get(rsn, 0)}")

    return dict(executed_weights=executed_weights, daily_ret_all=daily_ret_all, trades_df=trades_df,
                exit_counts=exit_counts, n_entries=n_entries)



# ══════════════════════════════════════════════════════════════════════════════
# 3b. SECONDARY ETF SLEEVE  (idle-cash sweep, weight-based)
# ══════════════════════════════════════════════════════════════════════════════

def load_secondary_etf(folder, name, index):
    """Raw ETF OHLCV aligned to the stock calendar. Returns dict of aligned Series:
         ok        - bar is tradable (close>0, volume>0, valid high/low, high != low)
         ret       - close-to-close return on the last-observed-close mark (valuation only)
         overnight - prev mark -> today's open return (earned by a portion sold at the open)
         first     - first date with a usable close (nothing is held before it)
    Marks are forward-filled for valuation; a trade ONLY happens on a raw tradable bar."""
    path = os.path.join(folder or "", f"{name}.csv")
    if not os.path.exists(path):
        raise FileNotFoundError(f"SECONDARY_ETF={name!r} needs {path} (set ETF_DATA_FOLDER)")
    raw = pd.read_csv(path)
    raw.columns = [str(c).strip().lower() for c in raw.columns]
    dcol = "timestamp" if "timestamp" in raw else "datetime"
    need = {dcol, "open", "high", "low", "close", "volume"}
    if need - set(raw.columns):
        raise ValueError(f"{path} is missing columns: {sorted(need - set(raw.columns))}")
    d = pd.to_datetime(raw[dcol], errors="raise")
    if getattr(d.dt, "tz", None) is not None:
        d = d.dt.tz_localize(None)          # keep the exchange-local calendar date (no UTC shift)
    raw[dcol] = d.dt.normalize()
    raw = raw.drop_duplicates(dcol, keep="last").set_index(dcol).sort_index()
    raw = raw[["open", "high", "low", "close", "volume"]].apply(pd.to_numeric, errors="coerce")
    a = raw.reindex(index)
    for c in ("open", "high", "low", "close"):
        a[c] = a[c].mask(a[c] <= 0)
    mark = a["close"].ffill()
    ok = (a["close"] > 0) & (a["volume"] > 0) & (a["high"] > 0) & (a["low"] > 0) & (a["high"] != a["low"])
    ret = mark.pct_change(fill_method=None).fillna(0.0)
    on = (a["open"] / mark.shift(1) - 1.0).where(a["open"].notna() & mark.shift(1).notna(), 0.0).fillna(0.0)
    valid = a["close"].dropna()
    if valid.empty:
        raise ValueError(f"{name} has no usable close on the strategy calendar")
    return dict(path=path, ok=ok.fillna(False), ret=ret.clip(-0.5, 0.5), overnight=on.clip(-0.5, 0.5), first=valid.index[0])


def apply_etf_sweep(idle, etf, cost_one_way, buy_band=0.0):
    """Park idle capital (fraction of equity, indexed by date) in the ETF.

    Timing mirrors the stock engine (weights on row t earn day-t return):
      * ETF weight held at the close of t-1 is `prev`.
      * If today's idle weight < prev, the excess is SOLD AT TODAY'S OPEN (stocks need the cash at
        their own open fill). That slice earns only the overnight prev-close->open move. Sells are
        never banded; if today's bar is not tradable the sale is still assumed (it is funding a stock
        order the engine already filled) and counted in `forced_untradable`.
      * The kept slice earns today's full close-to-close ETF return.
      * At today's close, idle cash above the held weight is BOUGHT only if the bar is tradable and the
        shortfall exceeds `buy_band`; otherwise it stays as plain cash (earning RISK_FREE_RATE).
      * Nothing is held before the ETF's first usable close.
    Returns DataFrame: etf_w (end-of-day weight), etf_contrib (return contribution), etf_cost,
    etf_turnover, plus the count of forced untradable sells."""
    dates = idle.index
    idle_v = idle.clip(lower=0.0).to_numpy()
    ret, on, ok = etf["ret"].reindex(dates).to_numpy(), etf["overnight"].reindex(dates).to_numpy(), etf["ok"].reindex(dates).to_numpy()
    active = (dates >= etf["first"])
    n = len(dates)
    w_end, contrib, cost, turn = np.zeros(n), np.zeros(n), np.zeros(n), np.zeros(n)
    prev, forced_untradable = 0.0, 0
    for t in range(n):
        if not active[t]:
            continue
        keep = min(prev, idle_v[t])
        sold = prev - keep
        c_t = keep * ret[t] + sold * on[t]
        tr = sold
        if sold > 1e-12 and not ok[t]:
            forced_untradable += 1
        new = keep
        gap = idle_v[t] - keep
        if gap > buy_band and gap > 1e-12 and ok[t]:
            new = idle_v[t]
            tr += gap
        contrib[t], cost[t], turn[t], w_end[t] = c_t, tr * cost_one_way, tr, new
        prev = new
    out = pd.DataFrame(dict(etf_w=w_end, etf_contrib=contrib, etf_cost=cost, etf_turnover=turn), index=dates)
    out.attrs["forced_untradable_sells"] = forced_untradable
    return out

# ══════════════════════════════════════════════════════════════════════════════
# 4. EQUITY CURVE  (entry/exit-day fill correction, then slice to the report window)
# ══════════════════════════════════════════════════════════════════════════════

def build_equity_curve(run_out, initial_capital, cost_one_way, risk_free_rate, etf=None, etf_cost_one_way=None, etf_buy_band=0.0):
    """
    Corrects the entry-day / exit-day bars in the return matrix so each trade's
    contribution to the equity curve runs strictly from its entry FILL to its
    exit FILL (not the full close-to-close bar, which would double count the
    overnight gap before the trade was actually placed, or the move after it
    was actually sold). Mirrors the reference event-driven engine's correction.
    """
    executed_weights = run_out['executed_weights']
    trades_df        = run_out['trades_df']
    prices            = csm.prices

    _dr = run_out['daily_ret_all'].copy()
    if not trades_df.empty:
        for _, meta in trades_df.iterrows():
            ticker      = meta['Ticker']
            if ticker not in _dr.columns:
                continue
            entry_date  = meta['Entry_Date']
            exit_date   = meta['Exit_Date']
            entry_price = meta['Entry_Price']
            fill_price  = meta['Exit_Price']

            if entry_date == exit_date:
                if exit_date in _dr.index:
                    _dr.at[exit_date, ticker] = 0.0
                continue

            if entry_date in _dr.index and pd.notna(entry_price) and entry_price > 0:
                close_entry = prices.at[entry_date, ticker] if entry_date in prices.index else np.nan
                if pd.notna(close_entry) and close_entry > 0:
                    _dr.at[entry_date, ticker] = (close_entry / entry_price) - 1.0

            if exit_date in _dr.index:
                _dr.at[exit_date, ticker] = 0.0

    daily_rfr       = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0
    gross_eq_ret    = (executed_weights * _dr).sum(axis=1)
    total_w         = executed_weights.sum(axis=1)
    idle_w          = (1.0 - total_w).clip(lower=0.0)
    turnover        = executed_weights.diff().abs().sum(axis=1).fillna(0.0)
    txn_cost        = turnover * cost_one_way

    # Free capital: either plain cash at RISK_FREE_RATE, or swept into the secondary ETF.
    if etf is not None:
        etf_cost = cost_one_way if etf_cost_one_way is None else float(etf_cost_one_way)
        sweep    = apply_etf_sweep(idle_w, etf, etf_cost, etf_buy_band)
        plain_w  = (idle_w - sweep['etf_w']).clip(lower=0.0)       # idle cash the ETF could not absorb
        cash_ret = plain_w * daily_rfr
        net_returns = gross_eq_ret + sweep['etf_contrib'] + cash_ret - txn_cost - sweep['etf_cost']
    else:
        sweep    = None
        cash_ret = idle_w * daily_rfr
        net_returns = gross_eq_ret + cash_ret - txn_cost

    equity_curve    = (1.0 + net_returns).cumprod()
    portfolio_value = equity_curve * initial_capital
    nheld           = (executed_weights > 1e-6).sum(axis=1)
    expo            = total_w

    return dict(equity_curve=equity_curve, portfolio_value=portfolio_value, net_returns=net_returns,
                turnover=turnover, nheld=nheld, expo=expo, executed_weights=executed_weights,
                etf_expo=(sweep['etf_w'] if sweep is not None else pd.Series(0.0, index=net_returns.index)),
                etf_turnover=(sweep['etf_turnover'] if sweep is not None else pd.Series(0.0, index=net_returns.index)),
                etf_cost_series=(sweep['etf_cost'] if sweep is not None else pd.Series(0.0, index=net_returns.index)),
                etf_forced_untradable=(sweep.attrs['forced_untradable_sells'] if sweep is not None else 0))


def slice_to_report_window(eq_out, trades_df, start_date, end_date, initial_capital):
    """Rebase the equity curve to START_DATE (excludes the warmup buffer) and
    filter the trade log to trades entered within the report window."""
    net_returns = eq_out['net_returns']
    mask = (net_returns.index >= pd.Timestamp(start_date)) & (net_returns.index <= pd.Timestamp(end_date))
    net_returns_r = net_returns.loc[mask]
    equity_curve_r = (1.0 + net_returns_r).cumprod()
    portfolio_value_r = equity_curve_r * initial_capital

    out = dict(eq_out)
    out['net_returns']     = net_returns_r
    out['equity_curve']    = equity_curve_r
    out['portfolio_value'] = portfolio_value_r
    out['turnover']        = eq_out['turnover'].loc[mask]
    out['nheld']           = eq_out['nheld'].loc[mask]
    out['expo']            = eq_out['expo'].loc[mask]
    out['etf_expo']        = eq_out['etf_expo'].loc[mask]
    out['etf_turnover']    = eq_out['etf_turnover'].loc[mask]
    out['etf_cost_series'] = eq_out['etf_cost_series'].loc[mask]

    tdf = trades_df.copy()
    if not tdf.empty:
        tdf = tdf[tdf['Entry_Date'] >= pd.Timestamp(start_date)].reset_index(drop=True)
    out['trades_df'] = tdf
    return out


# ══════════════════════════════════════════════════════════════════════════════
# 5. METRICS + REPORT
# ══════════════════════════════════════════════════════════════════════════════

def metrics(res, initial_capital, risk_free_rate):
    eq_s, net_returns = res['equity_curve'], res['net_returns']
    eq0 = pd.concat([pd.Series([1.0], index=[eq_s.index[0] - pd.Timedelta(days=1)]), eq_s])
    yrs = (eq_s.index[-1] - eq_s.index[0]).days / 365.25
    cagr = eq_s.iloc[-1] ** (1 / yrs) - 1.0 if yrs > 0 else np.nan
    vol  = net_returns.std() * np.sqrt(252)
    dd   = eq0 / eq0.cummax() - 1.0
    rf_d = (1 + risk_free_rate) ** (1 / 252) - 1
    down = np.sqrt((np.minimum(net_returns - rf_d, 0.0) ** 2).mean()) * np.sqrt(252)
    mret = eq_s.resample("ME").last().pct_change().dropna()
    port_val = eq_s * initial_capital
    avg_eq = port_val.mean()

    return dict(
        CAGR=cagr * 100, Vol=vol * 100,
        Sharpe0=net_returns.mean() / net_returns.std() * np.sqrt(252) if net_returns.std() > 0 else np.nan,
        SharpeEx=(net_returns.mean() - rf_d) / net_returns.std() * np.sqrt(252) if net_returns.std() > 0 else np.nan,
        Sortino=((net_returns.mean() - rf_d) * 252) / down if down > 0 else np.nan,
        MaxDD=dd.min() * 100, Calmar=cagr / abs(dd.min()) if dd.min() < 0 else np.nan,
        WinMo=(mret > 0).mean() * 100,
        AvgHold=res['nheld'].mean(), AvgExpo=res['expo'].mean() * 100,
        Turnover=res['turnover'].sum() / 2 / yrs * 100 if yrs > 0 else np.nan,
        CostDrag=(res['turnover'] * COST_ONE_WAY).sum() / yrs * 100 if yrs > 0 else np.nan,
        AvgETFExpo=res['etf_expo'].mean() * 100,
        ETFCostDrag=res['etf_cost_series'].sum() / yrs * 100 if yrs > 0 else np.nan,
    )


def year_returns(eq_s):
    ye = eq_s.resample("YE").last()
    prev = pd.concat([pd.Series([1.0]), ye.iloc[:-1]]).to_numpy()
    return pd.Series(ye.to_numpy() / prev - 1, index=ye.index.year) * 100


def year_drawdowns(eq_s):
    eq0 = pd.concat([pd.Series([1.0], index=[eq_s.index[0] - pd.Timedelta(days=1)]), eq_s])
    dd = (eq0 / eq0.cummax() - 1).iloc[1:]
    return dd.groupby(dd.index.year).min() * 100


def trade_diagnostics(tr):
    """Exit-reason and holding-period breakdown on NET trade P&L."""
    if tr.empty:
        return None, None
    tr = tr.copy()
    tr["win"] = tr.Net_PnL_Pct > 0
    by_reason = tr.groupby("Exit_Reason").agg(
        N=("win", "size"), Win_Pct=("win", lambda x: x.mean() * 100),
        AvgRet_Pct=("Net_PnL_Pct", "mean"), MedRet_Pct=("Net_PnL_Pct", "median"),
        MedDays=("Holding_Days", "median"), MAE_Pct=("MAE_Pct", "median"), MFE_Pct=("MFE_Pct", "median"),
    )
    bins = pd.cut(tr.Holding_Days, [-1, 30, 60, 120, 100000], labels=["<=30d", "31-60d", "61-120d", ">120d"])
    by_hold = tr.groupby(bins, observed=True).agg(
        N=("win", "size"), Win_Pct=("win", lambda x: x.mean() * 100), AvgRet_Pct=("Net_PnL_Pct", "mean"),
    )
    return by_reason, by_hold


def compute_icir(csm, horizons_months):
    """Spearman rank-IC of the composite Sharpe factor vs forward H-month
    return, measured at every month-end the factor was computed (decoupled
    from the rebalance_months cadence -- this measures the SIGNAL's own
    predictive power, not the portfolio construction built on top of it)."""
    monthly_close = csm.prices.resample('ME').last()
    rows = []
    for h in horizons_months:
        ics = []
        for date in csm.factors.index:
            if date not in monthly_close.index:
                continue
            loc = monthly_close.index.get_loc(date)
            if loc + h >= len(monthly_close.index):
                continue
            fwd_date = monthly_close.index[loc + h]
            row = csm.factors.loc[date].dropna()
            if len(row) < 20:
                continue
            c0 = monthly_close.loc[date, row.index]
            c1 = monthly_close.loc[fwd_date, row.index]
            valid = c0.notna() & c1.notna() & (c0 > 0)
            if valid.sum() < 20:
                continue
            fwd_ret = (c1[valid] / c0[valid]) - 1.0
            ic = row[valid].corr(fwd_ret, method='spearman')
            if pd.notna(ic):
                ics.append(ic)
        ics = np.array(ics)
        n_obs = len(ics)
        if n_obs >= 2 and ics.std(ddof=1) > 0:
            ic_mean, ic_std = ics.mean(), ics.std(ddof=1)
            icir = ic_mean / ic_std
            rows.append(dict(Horizon_Months=h, N=n_obs, MeanIC=ic_mean, StdIC=ic_std, ICIR=icir,
                              tStat=icir * np.sqrt(n_obs), PctPos=(ics > 0).mean() * 100))
        else:
            rows.append(dict(Horizon_Months=h, N=n_obs, MeanIC=np.nan, StdIC=np.nan, ICIR=np.nan,
                              tStat=np.nan, PctPos=np.nan))
    return pd.DataFrame(rows).set_index("Horizon_Months")


def trade_pnl_stats(tr):
    if tr.empty:
        return dict(n_trades=0, win_rate=np.nan, profit_factor=np.nan, avg_win=np.nan,
                    avg_loss=np.nan, payoff_ratio=np.nan, avg_holding_days=np.nan)
    pnl = tr['Net_PnL_Pct'].dropna().to_numpy()
    wins, losses = pnl[pnl > 0], pnl[pnl < 0]
    n_trades = len(pnl)
    win_rate = len(wins) / n_trades * 100 if n_trades else np.nan
    profit_factor = wins.sum() / abs(losses.sum()) if len(losses) and losses.sum() < 0 else np.nan
    avg_win = wins.mean() if len(wins) else np.nan
    avg_loss = abs(losses.mean()) if len(losses) else np.nan
    payoff_ratio = avg_win / avg_loss if avg_loss else np.nan
    avg_holding_days = tr['Holding_Days'].dropna().mean()
    return dict(n_trades=n_trades, win_rate=win_rate, profit_factor=profit_factor,
                avg_win=avg_win, avg_loss=avg_loss, payoff_ratio=payoff_ratio,
                avg_holding_days=avg_holding_days)


# ══════════════════════════════════════════════════════════════════════════════
# 6. RUN
# ══════════════════════════════════════════════════════════════════════════════

if SAVE_OUTPUTS:
    os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"\nRunning {STRATEGY_NAME}  (top_n={TOP_N}, rebalance every {REBALANCE_MONTHS}m, "
      f"crash_guard={'ON' if USE_CRASH_GUARD else 'OFF'}, trailing_stop={'ON' if USE_TRAILING_STOP else 'OFF'}, "
      f"vol_scaled_stop={'ON' if USE_VOL_SCALED_STOP else 'OFF'}) ...")

run_out = run_backtest(csm)
etf_data = None
if SECONDARY_ETF:
    assert SECONDARY_ETF in ("GOLDBEES", "SILVERBEES"), SECONDARY_ETF
    etf_data = load_secondary_etf(ETF_DATA_FOLDER, SECONDARY_ETF, csm.prices.index)
    if etf_data['first'] > pd.Timestamp(START_DATE):
        print(f"WARNING: {SECONDARY_ETF} first usable close is {etf_data['first'].date()}, after START_DATE; "
              f"idle cash before then earns RISK_FREE_RATE only.")

# Baseline (idle cash at RISK_FREE_RATE) is always computed so the sleeve's effect is visible.
eq_base = build_equity_curve(run_out, INITIAL_CAPITAL, COST_ONE_WAY, RISK_FREE_RATE)
res_base = slice_to_report_window(eq_base, run_out['trades_df'], START_DATE, END_DATE, INITIAL_CAPITAL)
eq_out_full = build_equity_curve(run_out, INITIAL_CAPITAL, COST_ONE_WAY, RISK_FREE_RATE,
                                 etf=etf_data, etf_cost_one_way=ETF_COST_ONE_WAY, etf_buy_band=ETF_BUY_BAND)
res = slice_to_report_window(eq_out_full, run_out['trades_df'], START_DATE, END_DATE, INITIAL_CAPITAL)
m_base = metrics(res_base, INITIAL_CAPITAL, RISK_FREE_RATE)

m = metrics(res, INITIAL_CAPITAL, RISK_FREE_RATE)
yr = year_returns(res['equity_curve'])
yr_dd = year_drawdowns(res['equity_curve'])
trades_df = res['trades_df']
stats = trade_pnl_stats(trades_df)

W = 60
print("\n" + "=" * W)
print(f" {STRATEGY_NAME} BACKTEST")
print(f" {res['equity_curve'].index[0].date()} -> {res['equity_curve'].index[-1].date()}")
print(f" cost {COST_ONE_WAY*100:.1f}% one-way   RFR {RISK_FREE_RATE*100:.1f}%   capital {INITIAL_CAPITAL:,.0f}")
print("=" * W)

ec = run_out['exit_counts']
rows = [
    ("CAGR %",              f"{m['CAGR']:.1f}"),
    ("Volatility %",        f"{m['Vol']:.1f}"),
    ("Sharpe (rf=0)",       f"{m['Sharpe0']:.2f}"),
    ("Sharpe (rf=cash)",    f"{m['SharpeEx']:.2f}"),
    ("Sortino",             f"{m['Sortino']:.2f}"),
    ("Max Drawdown %",      f"{m['MaxDD']:.1f}"),
    ("Calmar",              f"{m['Calmar']:.2f}"),
    ("Winning Months %",    f"{m['WinMo']:.1f}"),
    ("Avg Holdings",        f"{m['AvgHold']:.1f}"),
    ("Avg Exposure % (stocks)", f"{m['AvgExpo']:.0f}"),
    (f"Avg {SECONDARY_ETF or 'ETF'} Exposure %", f"{m['AvgETFExpo']:.0f}"),
    ("Turnover %/yr (1-way)", f"{m['Turnover']:.0f}"),
    ("Est. Cost Drag %/yr (stocks)", f"{m['CostDrag']:.2f}"),
    ("Est. Cost Drag %/yr (ETF)", f"{m['ETFCostDrag']:.2f}"),
    ("Entries",             f"{run_out['n_entries']}"),
]
for rsn in EXIT_REASONS:
    rows.append((f"Exits: {rsn}", f"{ec.get(rsn, 0)}"))
rows += [
    ("Closed Trades",        f"{stats['n_trades']}"),
    ("Avg Holding Period (days)", f"{stats['avg_holding_days']:.1f}" if pd.notna(stats['avg_holding_days']) else "n/a"),
    ("Trade Win Rate % (net)", f"{stats['win_rate']:.1f}" if pd.notna(stats['win_rate']) else "n/a"),
    ("Profit Factor (net)",  f"{stats['profit_factor']:.2f}" if pd.notna(stats['profit_factor']) else "n/a"),
    ("Avg Win % (net)",      f"{stats['avg_win']:.2f}" if pd.notna(stats['avg_win']) else "n/a"),
    ("Avg Loss % (net)",     f"{stats['avg_loss']:.2f}" if pd.notna(stats['avg_loss']) else "n/a"),
    ("Payoff Ratio",         f"{stats['payoff_ratio']:.2f}" if pd.notna(stats['payoff_ratio']) else "n/a"),
]
label_w = max(len(r[0]) for r in rows) + 2
for label, val in rows:
    print(f" {label:<{label_w}}{val:>15}")

if SECONDARY_ETF:
    print("\n" + "=" * W)
    print(f" SECONDARY SLEEVE IMPACT  ({SECONDARY_ETF} sweep vs idle cash @ RFR {RISK_FREE_RATE*100:.1f}%)")
    print("=" * W)
    cmp_rows = [("CAGR %", "CAGR"), ("Volatility %", "Vol"), ("Sharpe (rf=0)", "Sharpe0"), ("Sortino", "Sortino"),
                ("Max Drawdown %", "MaxDD"), ("Calmar", "Calmar")]
    print(f" {'':<18}{'No ETF':>12}{SECONDARY_ETF:>14}{'Delta':>10}")
    for label, key in cmp_rows:
        print(f" {label:<18}{m_base[key]:>12.2f}{m[key]:>14.2f}{m[key]-m_base[key]:>+10.2f}")
    print(f" ETF forced sells on untradable bars: {eq_out_full['etf_forced_untradable']}")
    print(f" ETF turnover (1-way, %/yr of equity): {res['etf_turnover'].sum() / ((res['equity_curve'].index[-1] - res['equity_curve'].index[0]).days / 365.25) * 100:.0f}")

print("\n" + "=" * W)
print(" CALENDAR-YEAR RETURN % / MAX DRAWDOWN %")
print("=" * W)
yr_tab = pd.DataFrame({"Return%": yr, "MaxDD%": yr_dd})
print(yr_tab.round(1).to_string())

by_reason, by_hold = trade_diagnostics(trades_df)
if by_reason is not None:
    print("\n" + "=" * W)
    print(" TRADE DIAGNOSTICS (net of cost) -- by exit reason")
    print("=" * W)
    print(by_reason.round(1).to_string())
    print("\n by holding period")
    print(by_hold.round(1).to_string())

print("\n" + "=" * W)
print(" FACTOR RANK-IC / ICIR vs FORWARD RETURNS (gross, universe-filtered pool)")
print("=" * W)
icir_tab = compute_icir(csm, IC_HORIZONS_MONTHS)
print(icir_tab.round(3).to_string())

if SAVE_OUTPUTS:
    res['equity_curve'].rename(STRATEGY_NAME).to_csv(os.path.join(OUTPUT_DIR, "equity_curve.csv"))
    trades_df.to_csv(os.path.join(OUTPUT_DIR, "trade_log_full.csv"), index=False)
    yr_tab.to_csv(os.path.join(OUTPUT_DIR, "yearly_returns.csv"))
    if SECONDARY_ETF:
        pd.DataFrame({"stock_exposure": res['expo'], "etf_exposure": res['etf_expo'],
                      "etf_turnover": res['etf_turnover'], "etf_cost": res['etf_cost_series'],
                      "ret_with_etf": res['net_returns'], "ret_no_etf": res_base['net_returns']}
                     ).to_csv(os.path.join(OUTPUT_DIR, "etf_sleeve_daily.csv"))
    icir_tab.to_csv(os.path.join(OUTPUT_DIR, "icir_report.csv"))
    if by_reason is not None:
        by_reason.to_csv(os.path.join(OUTPUT_DIR, "exit_reason_summary.csv"))
    print(f"\n[Saved] equity_curve.csv, trade_log_full.csv, yearly_returns.csv, icir_report.csv, "
          f"exit_reason_summary.csv  ->  {OUTPUT_DIR}")
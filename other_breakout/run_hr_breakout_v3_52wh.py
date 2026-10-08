"""
run_hr_breakout_backtest.py
===========================
Runner for the HR Breakout Strategy.
Loads OHLCV data, instantiates the strategy, runs the event-driven backtest,
slices results to the reporting window, and prints the performance report.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from hr_breakout_v3_52wh import load_data, HRBreakoutStrategy


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════

def plot_performance(results, benchmark_series=None, save_prefix='hr_breakout'):
    equity           = results['equity_curve']
    dd               = (equity / equity.cummax()) - 1
    executed_weights = results.get('executed_weights', None)

    fig = plt.figure(figsize=(16, 20))
    gs  = fig.add_gridspec(4, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='HR Breakout', color='#2ca02c', linewidth=1.5)
    ax1.set_yscale('log')
    if benchmark_series is not None:
        bench_rb = benchmark_series / benchmark_series.iloc[0]
        ax1.plot(bench_rb.index, bench_rb, label='Benchmark (EW)',
                 color='gray', linestyle='--', alpha=0.7)
    ax1.set_title('1. Cumulative Growth (Log Scale)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', linestyle='--', alpha=0.3)
    ax1.set_ylabel('Portfolio Value')

    # Panel 2: Relative Strength vs Benchmark
    ax2 = fig.add_subplot(gs[1, 0])
    if benchmark_series is not None:
        ba = benchmark_series.reindex(equity.index).ffill()
        rs = (equity / equity.iloc[0]) / (ba / ba.iloc[0])
        ax2.plot(rs.index, rs, color='purple', linewidth=1.2)
        ax2.set_title('2. Relative Strength vs Benchmark', fontsize=12, fontweight='bold')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.set_ylabel('Ratio')
    else:
        ax2.text(0.5, 0.5, 'No Benchmark', ha='center', va='center')

    # Panel 3: Active Positions
    ax3 = fig.add_subplot(gs[1, 1])
    if executed_weights is not None:
        pos_count = (executed_weights > 1e-6).sum(axis=1)
    else:
        pos_count = pd.Series(0, index=equity.index)
    ax3.fill_between(pos_count.index, pos_count, step='post',
                     color='#9467bd', alpha=0.5)
    ax3.plot(pos_count.index, pos_count, color='#9467bd',
             linewidth=0.8, drawstyle='steps-post')
    ax3.set_title('3. Active Positions (Daily Count)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Count')
    ax3.set_ylim(bottom=0)
    ax3.grid(True, axis='y', linestyle='--', alpha=0.3)

    # Panel 4: Drawdown
    ax4 = fig.add_subplot(gs[2, :])
    ax4.fill_between(dd.index, dd, 0, color='#d62728', alpha=0.3)
    ax4.plot(dd.index, dd, color='#d62728', linewidth=1)
    ax4.set_title('4. Drawdown Profile', fontsize=12, fontweight='bold')
    ax4.grid(True, linestyle='--', alpha=0.3)
    ax4.set_ylabel('Drawdown')

    # Panel 5: Monthly Return Distribution
    ax5 = fig.add_subplot(gs[3, :])
    monthly_ret = equity.resample('M').last().pct_change().dropna()
    ax5.hist(monthly_ret * 100, bins=50, color='teal', edgecolor='black', alpha=0.7)
    ax5.axvline(0, color='black', linestyle='--', linewidth=1)
    mean_ret = monthly_ret.mean() * 100
    ax5.axvline(mean_ret, color='blue', linestyle=':', label=f'Mean: {mean_ret:.2f}%')
    ax5.set_title('5. Monthly Return Distribution', fontsize=12, fontweight='bold')
    ax5.set_xlabel('Monthly Return (%)')
    ax5.legend()
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()
    perf_file = f'{save_prefix}_performance.png'
    plt.savefig(perf_file, dpi=150)
    print(f"[Graphics] Saved  →  {perf_file}")
    plt.close()

    # Monthly heatmap
    try:
        hm_df              = pd.DataFrame({'Return': monthly_ret})
        hm_df['Year']      = hm_df.index.year
        hm_df['Month']     = hm_df.index.month
        heatmap_data       = hm_df.pivot(index='Year', columns='Month', values='Return')
        plt.figure(figsize=(14, max(6, len(heatmap_data) * 0.55)))
        sns.heatmap(heatmap_data * 100, annot=True, fmt='.1f',
                    cmap='RdYlGn', center=0, cbar=False)
        plt.title('Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        hm_file = f'{save_prefix}_heatmap.png'
        plt.savefig(hm_file, dpi=150)
        print(f"[Graphics] Saved  →  {hm_file}")
        plt.close()
    except Exception as e:
        print(f"[Graphics] Heatmap failed: {e}")


def print_yearly_returns(portfolio_value):
    yearly_last = portfolio_value.resample('Y').last()
    yearly      = yearly_last.pct_change()
    # First year has no prior year-end to diff against — anchor it to the
    # series' own starting value (₹ initial capital) instead of leaving NaN.
    if len(yearly) > 0 and pd.isna(yearly.iloc[0]):
        yearly.iloc[0] = (yearly_last.iloc[0] / portfolio_value.iloc[0]) - 1.0
    # Yearly max drawdown: worst drop below the all-time-running peak reached
    # while inside that calendar year (running max carries over from prior
    # years, so a drawdown that started in year N-1 and bottomed in year N
    # is correctly attributed to year N).
    running_max = portfolio_value.cummax()
    dd          = (portfolio_value / running_max) - 1.0
    yearly_dd   = dd.resample('Y').min()

    print("\n" + "=" * 34)
    print("  Yearly Returns & Drawdown")
    print("=" * 34)
    print(f"{'Year':<6} | {'Return':>8} | {'Max DD':>8}")
    print("-" * 32)
    for dt, ret in yearly.items():
        if pd.notna(ret):
            ydd = yearly_dd.get(dt, float('nan'))
            ydd_str = f"{ydd*100:>7.2f}%" if pd.notna(ydd) else f"{'N/A':>8}"
            print(f"{dt.year:<6} | {ret*100:>7.2f}% | {ydd_str}")
    print("=" * 34)


# ══════════════════════════════════════════════════════════════════════════════
# SIGNAL IC / ICIR / T-STAT
# ══════════════════════════════════════════════════════════════════════════════

def compute_ic_stats_multi(strategy, horizons=(5, 15, 20, 30, 45, 60)):
    """
    Daily cross-sectional Information Coefficient of the entry signal itself
    (trend gate + 52w-high breakout) — not the momentum ranking factor, not
    the realised trade log. Tests whether firing the signal (vs. not firing
    it, within the same universe+trend-gate-eligible pool on the same day)
    actually predicts better forward returns, across several forward-return
    horizons at once.

    Mirrors backtest_event_driven()'s STEP B exactly for universe/trend/regime:
      regime_pass   = bench_ok.iloc[i]                       (skip day if False)
      universe_mask = strategy._universe_mask_df.iloc[i]     (already T-1 — the
                      frame bakes in .shift(1) internally, so row i IS T-1 data
                      for bar i; indexing it at i-1 here would be T-2, a bug)
      trend_mask    = strategy._trend_gate(i, universe_mask) (same call, same args)
      eligible      = universe_mask & trend_mask
      signal        = prev_close > high_52w * (1 + breakout_buffer)   (binary, 0/1)
      fwd_ret       = close[i + h] / close[i] - 1                     (forward h-day return)
      IC_i          = Spearman rank correlation(signal, fwd_ret) across eligible stocks

    Gap/cooldown/slot-ranking/position-sizing are intentionally NOT applied —
    those are portfolio/execution frictions, not signal-quality properties.
    This isolates "does the signal know something" from "can we harvest it
    given constraints," which is the standard scope for an IC test.

    The expensive part — universe_mask & trend_gate per day — is shared
    across all horizons in one pass rather than recomputed per horizon.

    Returns {horizon: (mean_ic, icir, t_stat, n_obs)}. ICIR = mean(IC) /
    std(IC); t_stat = ICIR * sqrt(n_obs) — standard significance test for
    whether the average IC is distinguishable from zero.
    """
    prices_np   = strategy._prices_np
    high52_np   = strategy._high_52w_np
    universe_df = strategy._universe_mask_df
    bench_ok    = strategy._compute_regime_flags()
    n_dates, n_stocks = prices_np.shape
    buffer = strategy.breakout_buffer

    ic_values = {h: [] for h in horizons}

    for i in range(1, n_dates - 1):
        if not bool(bench_ok.iloc[i]):
            continue   # regime off — real strategy takes no new entries this day

        idx = i - 1
        u_mask = universe_df.iloc[i]   # already T-1 data (shift baked in upstream)
        if u_mask.sum() < 5:
            continue

        trend_mask = strategy._trend_gate(i, u_mask)
        eligible   = (u_mask & trend_mask).values
        if eligible.sum() < 5:
            continue

        prev_close = prices_np[idx]
        hi52       = high52_np[idx]
        curr_close = prices_np[i]
        base_valid = eligible & ~np.isnan(prev_close) & ~np.isnan(hi52) & (hi52 > 0) \
                     & ~np.isnan(curr_close) & (curr_close > 0)
        if base_valid.sum() < 5:
            continue

        signal_all = (prev_close > hi52 * (1.0 + buffer))

        for h in horizons:
            if i + h >= n_dates:
                continue
            fwd_ret = (prices_np[i + h] / curr_close) - 1.0
            valid   = base_valid & ~np.isnan(fwd_ret)
            if valid.sum() < 5:
                continue
            sig = signal_all[valid].astype(float)
            if sig.std() == 0:
                continue   # no cross-sectional variation (all fired or none fired)
            ic = pd.Series(sig).corr(pd.Series(fwd_ret[valid]), method='spearman')
            if pd.notna(ic):
                ic_values[h].append(ic)

    results = {}
    for h in horizons:
        ic_arr = np.array(ic_values[h])
        n_obs  = len(ic_arr)
        if n_obs < 2:
            results[h] = (0.0, 0.0, 0.0, n_obs)
            continue
        mean_ic = float(ic_arr.mean())
        std_ic  = float(ic_arr.std(ddof=1))
        icir    = mean_ic / std_ic if std_ic > 0 else 0.0
        t_stat  = icir * np.sqrt(n_obs)
        results[h] = (mean_ic, icir, t_stat, n_obs)
    return results


def print_ic_stats(strategy, horizons=(5, 15, 20, 30, 45, 60)):
    results = compute_ic_stats_multi(strategy, horizons=horizons)
    print("\n" + "=" * 60)
    print("  Signal IC / ICIR / t-stat — multiple forward horizons")
    print("=" * 60)
    print(f"{'Horizon':>8} | {'Mean IC':>9} | {'ICIR':>9} | {'t-stat':>8} | {'N':>6} | Sig.")
    print("-" * 60)
    for h in horizons:
        mean_ic, icir, t_stat, n_obs = results[h]
        sig = "Yes" if abs(t_stat) >= 2.0 else "No"
        print(f"{h:>6}d  | {mean_ic:>9.4f} | {icir:>9.4f} | {t_stat:>8.3f} | {n_obs:>6} | {sig}")
    print("=" * 60)
    return results


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════
#
# NOTE: there is deliberately no report-start slice/rebase step, and no
# in-loop warmup_days counter either. main() loads an extra calendar year
# BEFORE start_load purely so indicators have real historical lookback,
# calls calculate_factors() on that wider range, then strategy.trim_to_window()
# cuts the buffer back off. The reporting window (start_load → end_load) is
# therefore fully warmed up from its very first bar, with zero dead/warmup
# days inside it and zero post-hoc re-slicing of the results.


# ══════════════════════════════════════════════════════════════════════════════
# BACKTEST ENGINE
# (moved from HRBreakoutStrategy — strategy instance passed as first argument)
# ══════════════════════════════════════════════════════════════════════════════

def backtest_event_driven(
        strategy,
        initial_capital  = 100_000.0,
        transaction_cost = 0.003,
        risk_free_rate   = 0.06,
) -> dict:
    """
    Main event-driven daily backtest loop.

    Execution model (all T-1 safe):
      Signal   : computed on bar T-1 data
      Entry    : executed at T open (bar i open)
      Exit     : evaluated at T open (bar i) using T-1 OHLCV for stop checks
      Warmup   : first 252 trading days → no new entries
    """
    if strategy.atr is None:
        raise ValueError("Call calculate_factors() first.")

    print(f"[Backtest] Starting — universe rank {strategy.universe_min_n}–{strategy.universe_top_n} | capital ₹{initial_capital:,.0f}")

    prices_ff  = strategy._prices_ff
    opens_ff   = strategy._opens_ff
    open_proxy = strategy._open_proxy
    highs_ff   = strategy._highs_ff
    lows_ff    = strategy._lows_ff
    atr_daily  = strategy.atr

    # Circuit-breaker mask: True on days where high == low
    if not strategy.highs.empty and not strategy.lows.empty:
        is_circuit = (highs_ff == lows_ff)
    else:
        is_circuit = pd.DataFrame(False, index=prices_ff.index,
                                  columns=prices_ff.columns)

    # Regime flags (precomputed for all bars at once — no lookahead, uses .shift(1))
    bench_ok = strategy._compute_regime_flags()

    daily_rfr = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0
    dates     = prices_ff.index
    n_dates   = len(dates)

    # ── Mutable state ─────────────────────────────────────────────────────
    active_holdings:       dict = {}   # ticker → holding dict
    stop_cooldown_tickers: dict = {}   # ticker → date of STOP_HIT
    executed_weights_list        = []
    strategy.position_metadata       = []

    n_stop, n_time_stop = 0, 0
    all_stocks          = list(prices_ff.columns)
    # Running portfolio value used for risk-based position sizing.
    # Updated at the end of each bar using the equity curve return for that bar.
    # Starts at initial_capital and compounds with each bar's portfolio return.
    running_portfolio_value = initial_capital

    for i, date in enumerate(dates):

        # ── First bar: seed with zeros ────────────────────────────────────
        if i == 0:
            executed_weights_list.append(
                pd.Series(0.0, index=all_stocks)
            )
            continue

        exited_today: set = set()
        prev_weights = executed_weights_list[i - 1]

        # ── STEP A: Exit evaluation ───────────────────────────────────────
        # Execution model (T-1 consistent):
        #   prev_close : T-1 close — used for peak update, profit check,
        #                anomaly guard (no today's close in any calculation)
        #   curr_atr   : T-1 ATR   — used for chandelier ratchet
        #   today_open : T open    — the actual fill price on exit
        #   today_low  : T low     — intraday stop trigger check
        for stock in list(active_holdings.keys()):

            prev_close = float(prices_ff.iloc[i - 1][stock]) \
                         if stock in prices_ff.columns else np.nan
            if pd.isna(prev_close) or prev_close <= 0:
                continue

            today_high = float(highs_ff.at[date, stock]) \
                         if stock in highs_ff.columns else prev_close
            today_low  = float(lows_ff.at[date, stock]) \
                         if stock in lows_ff.columns else prev_close
            today_open = float(opens_ff.at[date, stock]) \
                         if stock in opens_ff.columns else np.nan
            if pd.isna(today_open) or today_open <= 0:
                today_open = float(open_proxy.at[date, stock]) \
                             if stock in open_proxy.columns else prev_close

            # B: use T-1 ATR — consistent with T-1 discipline everywhere else
            curr_atr = float(atr_daily.iloc[i - 1][stock]) \
                       if stock in atr_daily.columns else np.nan
            if pd.isna(curr_atr) or curr_atr <= 0:
                curr_atr = prev_close * 0.02

            h = active_holdings[stock]
            entry_date_val = h.get('entry_date', date)
            days_held      = (date - entry_date_val).days
            h['days_held'] = days_held

            # Circuit day: locked price → defer exit decisions, but only up to
            # circuit_lockout_max consecutive locked days. Beyond that, force an
            # exit at the last valid open to bound suspension/halt risk (PANTH case).
            if stock in is_circuit.columns and bool(is_circuit.at[date, stock]):
                h['circuit_days'] = h.get('circuit_days', 0) + 1
                _CIRCUIT_TIMEOUT_DAYS = 10   # hardcoded, backtest only
                if h['circuit_days'] < _CIRCUIT_TIMEOUT_DAYS:
                    # Still within tolerance — defer normally
                    continue
                # Exceeded cap: force exit at today's open (best available price
                # after an extended lock; may be stale but bounds the damage)
                strategy._record_closed_trade(
                    ticker             = stock,
                    holding            = h,
                    exit_date          = date,
                    exit_price         = today_open,
                    fill_price         = today_open,
                    exit_reason        = 'CIRCUIT_TIMEOUT',
                    stop_price_at_exit = h.get('atr_stop', np.nan),
                )
                del active_holdings[stock]
                exited_today.add(stock)
                continue
            # Not a circuit day — reset counter so non-consecutive locks don't accumulate
            h['circuit_days'] = 0

            # ── Time stop (checked first, after time_stop_min_days, profit < threshold) ─
            # C: profit measured against T-1 close (last settled price),
            #    not today's close which isn't known at decision time.
            # Threshold = -5%: only exits genuinely broken trades. Flat or slightly
            # negative positions get more time to develop (aligned with 30d+ IC edge).
            # Uses strategy.time_stop_min_profit — same parameter as the live
            # system (get_exit_signals) so backtest and live are always in sync.
            if days_held >= strategy.time_stop_min_days:
                open_profit = (prev_close / h['entry_price']) - 1.0 \
                              if h['entry_price'] > 0 else 0.0
                if open_profit < strategy.time_stop_min_profit:
                    strategy._record_closed_trade(
                        ticker             = stock,
                        holding            = h,
                        exit_date          = date,
                        exit_price         = today_open,
                        fill_price         = today_open,
                        exit_reason        = 'TIME_STOP',
                        stop_price_at_exit = h.get('atr_stop', np.nan),
                    )
                    del active_holdings[stock]
                    exited_today.add(stock)
                    n_time_stop += 1
                    continue   # no STOP_HIT lockout on TIME_STOP

            # ── Chandelier / trailing stop ────────────────────────────────
            # D: pass prev_close as curr_close so peak update and anomaly
            #    guard inside _check_stop_exit both use T-1 data
            should_exit, fill_px, stop_lvl, updated_h = strategy._check_stop_exit(
                stock      = stock,
                curr_close = prev_close,
                curr_low   = today_low,
                curr_atr   = curr_atr,
                curr_open  = today_open,
                holding    = h,
                curr_high  = today_high,
            )

            if should_exit:
                strategy._record_closed_trade(
                    ticker             = stock,
                    holding            = h,
                    exit_date          = date,
                    exit_price         = prev_close,
                    fill_price         = fill_px,
                    exit_reason        = 'STOP_HIT',
                    stop_price_at_exit = stop_lvl,
                )
                del active_holdings[stock]
                exited_today.add(stock)
                stop_cooldown_tickers[stock] = date   # lockout: stop_cooldown_days calendar days
                n_stop += 1
            else:
                # MAE/MFE tracking: use only T-1 prev_close — the last
                # settled price known before bar T opens. today_low and
                # today_high are intraday T data and must not feed into
                # any calculation in this strategy.
                updated_h['min_price'] = min(updated_h.get('min_price', prev_close), prev_close)
                updated_h['max_price'] = max(updated_h.get('max_price', prev_close), prev_close)
                active_holdings[stock] = updated_h

        # ── STEP B: New entry signals ─────────────────────────────────────
        # Skip entirely during warmup period
        if i < strategy.warmup_days:
            curr_weights = pd.Series(
                {s: active_holdings[s]['weight'] for s in active_holdings},
                dtype=float
            ).reindex(all_stocks, fill_value=0.0)
            executed_weights_list.append(curr_weights)
            continue

        # Check regime: both must pass
        regime_pass = bool(bench_ok.iloc[i])
        # regime_pass = True  # --- IGNORE --- force regime pass for backtest

        # Build universe and trend gate masks (T-1 data)
        # Use the pre-built mask from calculate_factors() — avoids redundant
        # per-bar ranking. filter_universe() is kept for the live system path.
        universe_mask = strategy._universe_mask_df.iloc[i]
        trend_mask    = strategy._trend_gate(i, universe_mask)
        eligible      = universe_mask & trend_mask

        # Scan for HR signals on eligible stocks
        candidates = []
        if regime_pass:
            for stock in all_stocks:
                if not eligible.get(stock, False):
                    continue
                if stock in active_holdings:
                    continue
                if stock in exited_today:
                    continue

                # Stop cooldown: calendar-day gap since STOP_HIT must exceed stop_cooldown_days
                if stock in stop_cooldown_tickers:
                    gap = (date - stop_cooldown_tickers[stock]).days
                    if gap < strategy.stop_cooldown_days:
                        continue
                    else:
                        del stop_cooldown_tickers[stock]

                # HR signal
                signal, cluster_top = strategy._find_hr_signal(stock, i)
                if not signal:
                    continue

                # Entry execution filter: gap cancel
                today_open = float(opens_ff.at[date, stock]) \
                             if stock in opens_ff.columns else np.nan
                if pd.isna(today_open) or today_open <= 0:
                    today_open = float(open_proxy.at[date, stock]) \
                                 if stock in open_proxy.columns else np.nan

                prev_close_val = float(open_proxy.at[date, stock]) \
                                 if stock in open_proxy.columns else np.nan

                if not pd.isna(today_open) and not pd.isna(prev_close_val) \
                        and prev_close_val > 0:
                    gap_up = (today_open / prev_close_val) - 1.0
                    if gap_up > strategy.entry_gap_cancel_pct:
                        continue  # gap cancel

                # Circuit day check
                if stock in is_circuit.columns and bool(is_circuit.at[date, stock]):
                    continue

                # Compute 30-day momentum for ranking
                mom = float(strategy._mom_30d.iloc[i - 1][stock]) \
                      if stock in strategy._mom_30d.columns else -np.inf
                if pd.isna(mom):
                    mom = -np.inf

                candidates.append((stock, mom, today_open))

        # Rank candidates by 30-day momentum (descending) and fill up to max_positions
        candidates.sort(key=lambda x: x[1], reverse=True)
        slots_available = strategy.max_positions - len(active_holdings)

        for stock, mom, entry_open in candidates[:max(0, slots_available)]:
            if stock in active_holdings:
                continue

            entry_price = entry_open
            if pd.isna(entry_price) or entry_price <= 0:
                entry_price = float(prices_ff.iloc[i - 1][stock]) \
                              if stock in prices_ff.columns else np.nan
            if pd.isna(entry_price) or entry_price <= 0:
                continue

            # Use T-1 ATR (prior bar) for initial stop — consistent with
            # the T-1 signal discipline applied everywhere else in the loop
            curr_atr_entry = float(atr_daily.iloc[i - 1][stock]) \
                             if stock in atr_daily.columns else np.nan
            if pd.isna(curr_atr_entry) or curr_atr_entry <= 0:
                curr_atr_entry = entry_price * 0.02

            # Dynamic chandelier multiplier, fixed at entry from ATR%
            atr_pct_entry  = curr_atr_entry / entry_price
            entry_atr_mult = strategy._dynamic_atr_multiplier(atr_pct_entry)

            # Initial stop: max(entry × (1−10%), entry − dynamic_mult×ATR)
            initial_atr_stop = max(
                entry_price * (1.0 - strategy.hard_stop_from_entry),
                entry_price - entry_atr_mult * curr_atr_entry,
            )
            stop_dist = entry_price - initial_atr_stop

            # ── Risk-based position sizing ────────────────────────────
            # weight = risk_pct_per_trade / stop_pct
            # A trade risking 1% of portfolio with a 5% stop → 20% weight
            # A trade risking 1% of portfolio with a 10% stop → 10% weight
            # Clamped to [position_floor, position_ceil]
            stop_pct_entry = stop_dist / entry_price if entry_price > 0 else np.nan
            if pd.isna(stop_pct_entry) or stop_pct_entry <= 0:
                # Fallback: use position_floor if stop distance is invalid
                position_weight = strategy.position_floor
            else:
                position_weight = strategy.risk_pct_per_trade / stop_pct_entry
                position_weight = float(np.clip(
                    position_weight,
                    strategy.position_floor,
                    strategy.position_ceil,
                ))

            active_holdings[stock] = {
                'entry_date'      : date,
                'entry_price'     : entry_price,
                'peak_price'      : entry_price,
                'atr_stop'        : initial_atr_stop,
                'stop_pct'        : stop_pct_entry,
                'atr_at_entry'    : curr_atr_entry,
                'atr_multiplier'  : entry_atr_mult,
                'weight'          : position_weight,
                # intended_weight stores the pre-normalisation risk-based weight.
                # 'weight' may be scaled down if total > 100% (normalisation step).
                # Trade log uses intended_weight so it always reflects the original
                # risk-based sizing intent rather than the post-normalisation value.
                'intended_weight' : position_weight,
                'min_price'       : entry_price,
                'max_price'       : entry_price,
                'days_held'       : 0,
            }

        # ── Build executed weights ────────────────────────────────────────
        raw_weights = pd.Series(0.0, index=all_stocks)
        for stock, h in active_holdings.items():
            raw_weights[stock] = h['weight']

        # Normalise if total exceeds 100%
        total_w = raw_weights.sum()
        if total_w > 1.0:
            raw_weights = raw_weights / total_w
            # Sync post-normalisation weights back into active_holdings so
            # bar_return (used for running_portfolio_value) uses the same
            # weights as the equity curve — prevents oversizing on next entry.
            for stock in active_holdings:
                active_holdings[stock]['weight'] = float(raw_weights[stock])

        executed_weights_list.append(raw_weights.copy())

        # Update running portfolio value for next bar's sizing decisions.
        # Use the bar's portfolio return = sum(weight × stock_return_today).
        # stock_return_today = (today_close / prev_close) - 1 for held stocks.
        bar_return = 0.0
        for stock, h in active_holdings.items():
            if stock not in prices_ff.columns:
                continue
            today_close = float(prices_ff.iloc[i][stock])                           if i < len(prices_ff) else np.nan
            prev_close  = float(prices_ff.iloc[i - 1][stock])                           if i > 0 else np.nan
            if pd.isna(today_close) or pd.isna(prev_close) or prev_close <= 0:
                continue
            bar_return += h['weight'] * ((today_close / prev_close) - 1.0)
        running_portfolio_value *= (1.0 + bar_return)

    # ── Close any positions still open at end of data ─────────────────────
    last_date = dates[-1]
    for stock, h in active_holdings.items():
        last_close = float(prices_ff.at[last_date, stock]) \
                     if stock in prices_ff.columns else np.nan
        last_open  = float(opens_ff.at[last_date, stock]) \
                     if stock in opens_ff.columns else np.nan
        if pd.isna(last_open) or last_open <= 0:
            last_open = last_close
        strategy._record_closed_trade(
            ticker             = stock,
            holding            = h,
            exit_date          = last_date,
            exit_price         = last_close,
            fill_price         = last_open,
            exit_reason        = 'END_OF_DATA',
            stop_price_at_exit = h.get('atr_stop', np.nan),
        )
    active_holdings.clear()

    print(f"\n[HR Breakout] Stop exits    : {n_stop}")
    print(f"[HR Breakout] Time stops    : {n_time_stop}")

    # ── Assemble executed-weights DataFrame ───────────────────────────────
    executed_weights = pd.DataFrame(
        executed_weights_list, index=dates
    ).fillna(0.0)

    # ── Correct entry and exit day returns to use actual fill prices ─────
    #
    # Problem: _dr = prices.pct_change() uses close-to-close every day.
    #
    # On ENTRY day: equity curve captures (close_entry / close_prev) - 1
    #               but we actually entered at open_entry.
    #               Correct return = (close_entry / open_entry) - 1
    #
    # On EXIT day:  equity curve captures (close_exit / close_prev) - 1
    #               but we actually exited at fill_price (open or stop level).
    #               Correct return = (fill_price / close_prev) - 1
    #
    _dr = strategy.prices.pct_change(fill_method=None).fillna(0.0)

    for meta in strategy.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        entry_price = meta['Entry_Price']   # actual entry fill (open of entry day)
        exit_date   = meta['Exit_Date']
        exit_price  = meta['Exit_Price']    # actual exit fill (open or stop level)

        if ticker not in _dr.columns:
            continue

        # ── Entry day correction ──────────────────────────────────────────
        # Replace close-to-close return with open-to-close return
        # so the equity curve starts from our actual entry price.
        # Skip for 1-day trades (entry_date == exit_date): the exit
        # correction below already sets the correct return for that bar;
        # applying entry correction first would be overwritten anyway.
        if entry_date != exit_date and entry_date in _dr.index \
                and pd.notna(entry_price) and entry_price > 0:
            entry_loc  = _dr.index.get_loc(entry_date)
            close_entry = strategy.prices.iloc[entry_loc].get(ticker, np.nan)
            if pd.notna(close_entry) and close_entry > 0:
                # open-to-close return on entry day
                corrected_entry_ret = (close_entry / entry_price) - 1.0
                _dr.at[entry_date, ticker] = corrected_entry_ret

        # ── Exit day correction ───────────────────────────────────────────
        # Replace close-to-close return with prev-close-to-fill return
        # so the equity curve ends at our actual exit fill price.
        if exit_date in _dr.index and pd.notna(exit_price) and exit_price > 0:
            exit_loc = _dr.index.get_loc(exit_date)
            if exit_loc == 0:
                continue
            prev_c = strategy.prices.iloc[exit_loc - 1].get(ticker, np.nan)
            if pd.notna(prev_c) and prev_c > 0:
                # prev-close-to-fill return on exit day
                corrected_exit_ret = (exit_price / prev_c) - 1.0
                _dr.at[exit_date, ticker] = corrected_exit_ret

    # ── Portfolio returns ─────────────────────────────────────────────────
    entries  = (executed_weights > 1e-6) & (executed_weights.shift(1).fillna(0) <= 1e-6)
    exits    = (executed_weights <= 1e-6) & (executed_weights.shift(1).fillna(0) > 1e-6)

    gross_ret   = (executed_weights * _dr).sum(axis=1)
    total_w     = executed_weights.sum(axis=1)
    cash_w      = (1.0 - total_w).clip(lower=0.0)
    cash_ret    = cash_w * daily_rfr
    # Transaction cost: charge on actual weight at entry and exit bars.
    # Use actual executed weights — correct for risk-based sizing where each
    # position has a different weight rather than a fixed position_ceil.
    w_chg    = (executed_weights         * entries.astype(float)
                + executed_weights.shift(1).fillna(0) * exits.astype(float))
    txn_cost = w_chg.sum(axis=1) * transaction_cost
    net_returns = gross_ret + cash_ret - txn_cost

    equity_curve    = (1.0 + net_returns).cumprod()
    portfolio_value = equity_curve * initial_capital

    # ── Performance metrics ───────────────────────────────────────────────
    n_years  = (equity_curve.index[-1] - equity_curve.index[0]).days / 365.25
    cagr     = (equity_curve.iloc[-1]) ** (1.0 / n_years) - 1.0 if n_years > 0 else 0.0
    ann_vol  = net_returns.std() * np.sqrt(252)

    _excess  = net_returns - daily_rfr
    sharpe   = (np.sqrt(252) * _excess.mean() / net_returns.std()
                if net_returns.std() > 0 else 0.0)
    _dn      = net_returns.clip(upper=0.0)
    _dndev   = np.sqrt((_dn ** 2).mean())
    sortino  = (np.sqrt(252) * net_returns.mean() / _dndev if _dndev > 0 else 0.0)

    _rmax   = equity_curve.cummax()
    _dd     = (equity_curve / _rmax) - 1.0
    max_dd  = _dd.min()
    calmar  = cagr / abs(max_dd) if max_dd != 0 else 0.0

    _mret    = portfolio_value.resample('M').last().pct_change().dropna()
    win_rate = (_mret > 0).mean()
    # Turnover: sum of absolute daily weight changes, halved (entry+exit each
    # contribute one leg), annualised. Gives true portfolio turnover rate.
    weight_changes = executed_weights.diff().abs()
    ann_turn = float(weight_changes.sum().sum()) / 2.0 / n_years if n_years > 0 else 0.0

    daily_win_rate = (net_returns > 0).mean()

    strategy.results = {
        'equity_curve'       : equity_curve,
        'portfolio_value'    : portfolio_value,   # rupee-denominated (equity_curve × initial_capital)
        'net_returns'        : net_returns,
        'executed_weights'   : executed_weights,
        'total_return'       : float(equity_curve.iloc[-1] - 1.0),
        'cagr'               : cagr,
        'sharpe'             : sharpe,
        'sortino'            : sortino,
        'calmar'             : calmar,
        'max_drawdown'       : max_dd,
        'ann_volatility'     : ann_vol,
        'win_rate'           : win_rate,
        'daily_win_rate'     : daily_win_rate,
        'ann_turnover'       : ann_turn,
    }

    print(f"\n[HR Breakout] CAGR={cagr*100:.2f}%  "
          f"Sharpe={sharpe:.2f}  MaxDD={max_dd*100:.2f}%")
    return strategy.results




def get_trade_log(strategy) -> pd.DataFrame:
    """
    Build a trade-log DataFrame from strategy.position_metadata.
    Must be called after backtest_event_driven().
    """
    if not strategy.position_metadata:
        print("Warning: No trade metadata. Run backtest() first.")
        return pd.DataFrame()

    # Use portfolio_value (rupee-denominated) not equity_curve (indexed to 1.0)
    # equity_curve starts at 1.0 and was causing port_val to be off by initial_capital factor
    portfolio_value_series = strategy.results['portfolio_value'] if strategy.results else None
    executed_weights       = strategy.results['executed_weights'] if strategy.results else None
    prices_ffill           = strategy.prices.ffill()

    _equity_lookup = portfolio_value_series.ffill() if portfolio_value_series is not None else None

    rows = []
    for meta in strategy.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        exit_date   = meta['Exit_Date']
        entry_price = meta['Entry_Price']
        exit_price  = meta['Exit_Price']

        if pd.isna(exit_price) and ticker in prices_ffill.columns:
            exit_price = (prices_ffill.at[exit_date, ticker]
                          if exit_date in prices_ffill.index
                          else prices_ffill[ticker].iloc[-1])

        # Use intended_weight from metadata — this is the pre-normalisation
        # risk-based weight and correctly reflects the sizing intent.
        # Do NOT overwrite with executed_weights which may be scaled down
        # by the normalisation step when total exposure exceeds 100%.
        weight = meta.get('Intended_Weight', meta['Weight'])
        if weight == 0 or pd.isna(weight):
            # Fallback: read from executed_weights if metadata weight is missing
            if executed_weights is not None and ticker in executed_weights.columns:
                ew_col  = executed_weights[ticker]
                window  = ew_col.loc[(ew_col.index > entry_date) & (ew_col.index <= exit_date)]
                nonzero = window[window > 1e-9]
                if not nonzero.empty:
                    weight = float(nonzero.iloc[0])

        port_val = np.nan
        if _equity_lookup is not None:
            # Use the equity value ON the entry bar itself (not the bar
            # after). get_loc with method= was removed in pandas 2.0.
            if entry_date in _equity_lookup.index:
                port_val = float(_equity_lookup.loc[entry_date])
            else:
                # entry_date not an exact index date — find nearest prior
                idx_pos = _equity_lookup.index.searchsorted(entry_date, side='right') - 1
                if idx_pos >= 0:
                    port_val = float(_equity_lookup.iloc[idx_pos])

        qty = np.nan
        if pd.notna(entry_price) and entry_price > 0 \
                and pd.notna(port_val) and weight > 0:
            qty = (weight * port_val) / entry_price

        pnl_pct = ((exit_price / entry_price) - 1) * 100 \
                  if (pd.notna(entry_price) and entry_price > 0
                      and pd.notna(exit_price) and exit_price > 0) else np.nan

        pnl_abs = qty * (exit_price - entry_price) \
                  if (pd.notna(qty) and pd.notna(entry_price)
                      and pd.notna(exit_price)) else np.nan

        holding_days = max((exit_date - entry_date).days, 1)

        rows.append({
            'Ticker'             : ticker,
            'Entry_Date'         : entry_date,
            'Entry_Price'        : meta['Entry_Price'],
            'Exit_Date'          : exit_date,
            'Exit_Price'         : round(exit_price,              4) if pd.notna(exit_price)              else np.nan,
            'Close_At_Exit'      : meta.get('Close_At_Exit',      np.nan),
            'Peak_Price'         : meta.get('Peak_Price',         np.nan),
            'Stop_Price_At_Exit' : meta.get('Stop_Price_At_Exit', np.nan),
            'Stop_Pct'           : meta.get('Stop_Pct',           np.nan),
            'ATR_At_Entry'       : meta.get('ATR_At_Entry',       np.nan),
            'Exit_Reason'        : meta['Exit_Reason'],
            'Intended_Weight'    : round(meta.get('Intended_Weight', weight), 6),
            'Weight'             : round(weight,                   6),
            'Quantity'           : round(qty,                      4) if pd.notna(qty)     else np.nan,
            'Position_Size'      : round(weight * port_val,        2) if (pd.notna(port_val) and weight > 0) else 0.0,
            'Portfolio_Value'    : round(port_val,                 2) if pd.notna(port_val) else np.nan,
            'PnL_Pct'            : round(pnl_pct,                  4) if pd.notna(pnl_pct) else np.nan,
            'PnL_Abs'            : round(pnl_abs,                  2) if pd.notna(pnl_abs) else np.nan,
            'Holding_Days'       : holding_days,
            'MAE_Pct'            : meta.get('MAE_Pct',             np.nan),
            'MFE_Pct'            : meta.get('MFE_Pct',             np.nan),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values('Entry_Date').reset_index(drop=True)
        df.index += 1
        df.index.name = 'Trade_ID'

    wins   = (df['PnL_Pct'] > 0).sum()  if not df.empty else 0
    losses = (df['PnL_Pct'] < 0).sum()  if not df.empty else 0
    total  = len(df)
    if total > 0:
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {losses}"
              f" | Win Rate: {wins/total*100:.1f}%")
        print(f"[Trade Log] Worst: {df['PnL_Pct'].min():.2f}%"
              f"  Best: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
    return df



def main(load_start=None, load_end=None, universe=None):
    # ── 1. Load Data ─────────────────────────────────────────────────────────
    data_folder = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
    print("Loading data...")
    prices, volumes, highs, lows, opens = load_data(data_folder)

    if prices.empty:
        print("Error: No data loaded.")
        return

    start_load   = '2015-01-01'   # True first day of the reporting/trading window
    end_load     = '2025-12-31'

    if load_start and load_end:
        start_load   = load_start
        end_load     = load_end

    # Warmup comes from data BEFORE start_load, not from bars inside it.
    # Load an extra calendar year ahead of start_load purely so EMA-200,
    # the 252-day high, RS, ATR, etc. have real historical lookback by the
    # time the reporting window begins — strategy.trim_to_window() below
    # cuts this buffer back off once indicators are computed on it, so the
    # reporting window itself has zero dead/warmup days inside it.
    data_load_start = (pd.Timestamp(start_load) - pd.DateOffset(years=1)).strftime('%Y-%m-%d')

    prices  = prices.loc[data_load_start:end_load]
    volumes = volumes.loc[data_load_start:end_load]
    if not highs.empty:  highs  = highs.loc[data_load_start:end_load]
    if not lows.empty:   lows   = lows.loc[data_load_start:end_load]
    if not opens.empty:  opens  = opens.loc[data_load_start:end_load]

    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()}  →  {prices.index.max().date()}"
          f"  (buffer from {data_load_start}, reporting window starts {start_load})")

    # ── 2. Instantiate Strategy ───────────────────────────────────────────────
    strategy = HRBreakoutStrategy(
        prices_df             = prices,
        volumes_df            = volumes,
        highs_df              = highs,
        lows_df               = lows,
        opens_df              = opens,
        # Universe
        universe_top_n        = 500,
        universe_min_n        = 1,          # set >1 to slice a band e.g. 1001 for rank 1001-1500
        min_price             = 10.0,
        max_circuit_days      = 5,
        prior_month_min_ret   = -0.15,
        # Regime
        benchmark_sma_period  = 50,
        benchmark_streak_max  = 5,
        # Trend gate
        ema_fast              = 50,
        ema_mid               = 150,
        ema_slow              = 200,
        ema_slope_window      = 20,
        high_band_pct         = 0.75,
        rs_lookback           = 126,
        rs_top_pct            = 0.25,
        # 52-Week High Breakout Signal (cluster formation disabled)
        breakout_buffer       = 0.005,
        entry_gap_cancel_pct  = 0.03,
        momentum_rank_window  = 30,
        max_positions         = 10,
        # Position sizing
        risk_pct_per_trade    = 0.01,       # 1% of portfolio risked per trade
        position_ceil         = 0.15,       # max weight cap per position
        position_floor        = 0.02,       # min weight floor per position
        # Stops
        atr_period            = 14,
        atr_multiplier_max    = 2.5,        # chandelier mult for calm (low ATR%) names
        atr_multiplier_min    = 1.5,        # chandelier mult for volatile (high ATR%) names
        atr_pct_calm          = 0.020,      # ATR/price <= this -> full atr_multiplier_max
        atr_pct_volatile      = 0.045,      # ATR/price >= this -> full atr_multiplier_min
        chandelier_clamp_min  = 0.12,       # chandelier never closer than 12% to peak (widened to extend holding)
        chandelier_clamp_max  = 0.30,       # chandelier never farther than 30% from peak
        hard_stop_from_entry  = 0.15,
        hard_stop_from_peak   = 0.15,
        stop_slippage_pct     = 0.0,
        # Lockout / time stop
        stop_cooldown_days    = 20,
        min_hold_days         = 20,         # chandelier suppressed for first 20 days — only entry floor active
        time_stop_min_days    = 45,         # raised from 30d — only exits genuinely broken trades
        time_stop_min_profit  = -0.05,      # raised from 0% — flat trades get more time to work
        # warmup comes from the data_load_start buffer (trimmed off below),
        # not from an in-loop counter eating into the reporting window.
        warmup_days           = 0,
    )

    # ── 3. Pre-compute indicators on the buffer-inclusive data ───────────────
    strategy.calculate_factors()

    # strategy._bench_series is the equal-weight benchmark of only price-floor
    # eligible stocks, built inside calculate_factors() from the raw universe.
    # This is the correct comparison series for this strategy.
    benchmark_series = strategy._bench_series

    # Cut the data_load_start buffer back off. Every EMA/ATR/52w-high/RS
    # value at start_load was already computed using the real pre-start_load
    # history, so the trimmed window is fully warmed up from its first bar —
    # no further warmup_days are needed in the event loop.
    strategy.trim_to_window(start_load)
    benchmark_series = benchmark_series.loc[pd.Timestamp(start_load):]

    # ── 4. Generate positions (optional — live system path) ───────────────────
    # strategy.get_positions()

    # ── 5. Backtest ───────────────────────────────────────────────────────────
    results = backtest_event_driven(
        strategy,
        initial_capital  = 100_000,
        transaction_cost = 0.003,
        risk_free_rate   = 0.0,
    )

    # Rebase benchmark to the same ₹100,000 start as the equity curve
    results['benchmark'] = benchmark_series / benchmark_series.iloc[0] * 100_000

    # ── 6. Trade log ──────────────────────────────────────────────────────────
    detailed_log = pd.DataFrame()
    try:
        detailed_log = get_trade_log(strategy)
        if not detailed_log.empty:
            detailed_log.to_csv('hr_detailed_trade_log.csv', index=False)
            print(f"\n[Logs] hr_detailed_trade_log.csv  ({len(detailed_log)} trades)")
    except Exception as e:
        print(f"\n[Logs] Warning: Trade log failed: {e}")

    # ── 7. Daily backtest log CSV ─────────────────────────────────────────────
    _eq  = results['equity_curve']
    _ret = results['net_returns']
    _w   = results['executed_weights']
    _dd  = (_eq / _eq.cummax()) - 1.0
    daily_log = pd.DataFrame(index=_eq.index)
    daily_log['Portfolio_Value'] = results['portfolio_value']
    daily_log['Net_Return']      = _ret
    daily_log['Positions']       = (_w > 1e-6).sum(axis=1)
    daily_log['Exposure']        = _w.sum(axis=1)
    daily_log['Drawdown']        = _dd
    daily_log.to_csv('hr_backtest_logs.csv')
    print(f"[Logs] hr_backtest_logs.csv  ({len(daily_log)} rows)")

    # ── 8. Populate trade-basis metrics ──────────────────────────────────────
    for key in [
        'trade_win_rate', 'total_trades_count', 'avg_trade_return',
        'median_trade_return', 'avg_holding_days', 'best_trade', 'worst_trade',
        'avg_win_pct', 'avg_loss_pct', 'payoff_ratio', 'profit_factor',
        'profit_factor_dollar', 'pct_stops', 'pct_time_stops', 'pct_end_data',
        'avg_stop_pct', 'avg_mae', 'avg_mfe',
    ]:
        results.setdefault(key, 0.0)

    if not detailed_log.empty:
        dl      = detailed_log
        wins    = (dl['PnL_Pct'] > 0).sum()
        losses  = (dl['PnL_Pct'] < 0).sum()
        total_t = len(dl)

        results['trade_win_rate']      = wins / total_t if total_t > 0 else 0.0
        results['total_trades_count']  = total_t
        results['avg_trade_return']    = dl['PnL_Pct'].mean()
        results['median_trade_return'] = dl['PnL_Pct'].median()
        results['avg_holding_days']    = dl['Holding_Days'].mean()
        results['best_trade']          = dl['PnL_Pct'].max()
        results['worst_trade']         = dl['PnL_Pct'].min()
        results['avg_stop_pct']        = dl['Stop_Pct'].mean()
        results['avg_mae']             = dl['MAE_Pct'].mean()
        results['avg_mfe']             = dl['MFE_Pct'].mean()

        avg_win  = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].mean() if wins   > 0 else 0.0
        avg_loss = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().mean() if losses > 0 else 0.0
        results['avg_win_pct']   = avg_win
        results['avg_loss_pct']  = avg_loss
        results['payoff_ratio']  = avg_win / avg_loss if avg_loss > 0 else float('inf')

        gw_pct = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].sum()
        gl_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().sum()
        results['profit_factor'] = gw_pct / gl_pct if gl_pct > 0 else float('inf')

        gw_abs = dl.loc[dl['PnL_Abs'] > 0, 'PnL_Abs'].sum()
        gl_abs = dl.loc[dl['PnL_Abs'] < 0, 'PnL_Abs'].abs().sum()
        results['profit_factor_dollar'] = gw_abs / gl_abs if gl_abs > 0 else float('inf')

        reason_counts = dl['Exit_Reason'].value_counts()
        results['pct_stops']      = reason_counts.get('STOP_HIT',   0) / total_t * 100
        results['pct_time_stops'] = reason_counts.get('TIME_STOP',  0) / total_t * 100
        results['pct_end_data']   = reason_counts.get('END_OF_DATA',0) / total_t * 100

    # ── 9. Performance Report ─────────────────────────────────────────────────
    W   = 38
    SEP = "=" * W

    print(f"\n{SEP}")
    print(f"  HR BREAKOUT  —  PERFORMANCE REPORT")
    print(SEP)

    print(f"\n── Portfolio Metrics ─────────────────")
    print(f"  CAGR              : {results['cagr']*100:>8.2f}%")
    print(f"  Total Return      : {results['total_return']*100:>8.2f}%")
    print(f"  Ann Volatility    : {results['ann_volatility']*100:>8.2f}%")
    print(f"  Max Drawdown      : {results['max_drawdown']*100:>8.2f}%")
    print(f"  Sharpe Ratio      : {results['sharpe']:>9.3f}")
    print(f"  Sortino Ratio     : {results['sortino']:>9.3f}")
    print(f"  Calmar Ratio      : {results['calmar']:>9.3f}")
    print(f"  Final Portfolio   : ₹{results['portfolio_value'].iloc[-1]:>12,.2f}")

    print(f"\n── Win Rate (3 views) ────────────────")
    print(f"  Daily Win Rate    : {results['daily_win_rate']*100:>8.2f}%")
    print(f"  Monthly Win Rate  : {results['win_rate']*100:>8.2f}%")
    if results['total_trades_count'] > 0:
        print(f"  Trade Win Rate    : {results['trade_win_rate']*100:>8.2f}%"
              f"  ({results['total_trades_count']} trades)")
    else:
        print(f"  Trade Win Rate    : {'N/A':>8}")

    print(f"\n── Trade Statistics ──────────────────")
    if results['total_trades_count'] > 0:
        print(f"  Total Trades      : {results['total_trades_count']:>8}")
        print(f"  Avg Trade Return  : {results['avg_trade_return']:>8.2f}%")
        print(f"  Median Trade Ret  : {results['median_trade_return']:>8.2f}%")
        print(f"  Best Trade        : {results['best_trade']:>8.2f}%")
        print(f"  Worst Trade       : {results['worst_trade']:>8.2f}%")
        print(f"  Avg Win  (trade)  : {results['avg_win_pct']:>8.2f}%")
        print(f"  Avg Loss (trade)  : -{results['avg_loss_pct']:>7.2f}%")
        print(f"  Payoff Ratio      : {results['payoff_ratio']:>9.3f}  (avg win / avg loss)")
        print(f"  Profit Factor (%) : {results['profit_factor']:>9.3f}  (equal-weighted)")
        print(f"  Profit Factor (₹) : {results['profit_factor_dollar']:>9.3f}  (rupee-weighted)")
        print(f"  Avg Holding Days  : {results['avg_holding_days']:>8.1f}")
        print(f"  Avg Stop Pct      : {results.get('avg_stop_pct', 0):>8.2f}%")
        print(f"  Avg MAE           : {results.get('avg_mae', 0):>8.2f}%")
        print(f"  Avg MFE           : {results.get('avg_mfe', 0):>8.2f}%")
    else:
        print("  No completed trades in reporting period.")

    print(f"\n── Exit Breakdown ────────────────────")
    if results['total_trades_count'] > 0:
        print(f"  Stop Hit          : {results['pct_stops']:>8.1f}%")
        print(f"  Time Stop         : {results['pct_time_stops']:>8.1f}%")
        print(f"  End of Data       : {results.get('pct_end_data', 0):>8.1f}%")

    print(f"\n── Turnover ──────────────────────────")
    if 'ann_turnover' in results:
        print(f"  Ann Turnover      : {results['ann_turnover']*100:>8.2f}%")

    # ── 10. Yearly returns + charts ───────────────────────────────────────────
    print_yearly_returns(results['portfolio_value'])
    plot_performance(results, results['benchmark'])

    # ── 11. Signal IC / ICIR / t-stat (multiple forward horizons) ────────────
    ic_by_horizon = print_ic_stats(strategy, horizons=(5, 15, 20, 30, 45, 60))

    return {
        'cagr'           : results['cagr'] * 100,
        'drawdown'       : results['max_drawdown'] * 100,
        'trade_win_rate' : results['trade_win_rate'] * 100,
        'calmar'         : results['calmar'],
        'ic_by_horizon'  : ic_by_horizon,
    }


if __name__ == "__main__":
    main()
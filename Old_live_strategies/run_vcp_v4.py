"""
run_vcp_breakout.py
===================
Runner for the VCP / SEPA Breakout Strategy.
Loads OHLCV data, instantiates the strategy, runs the event-driven backtest,
slices results to the reporting window, and prints the performance report.

All config lives here. vcp_breakout.py is never edited directly.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from vcp_v4 import load_data, VCPBreakoutStrategy


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════

def plot_performance(results, benchmark_series=None, save_prefix='vcp_breakout'):
    equity           = results['equity_curve']
    dd               = (equity / equity.cummax()) - 1
    executed_weights = results.get('executed_weights', None)

    fig = plt.figure(figsize=(16, 20))
    gs  = fig.add_gridspec(4, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='VCP Breakout', color='#2ca02c', linewidth=1.5)
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
    monthly_ret = equity.resample('ME').last().pct_change().dropna()
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
    print(f"[Graphics] Saved → {perf_file}")
    plt.close()

    # Monthly heatmap
    try:
        hm_df         = pd.DataFrame({'Return': monthly_ret})
        hm_df['Year'] = hm_df.index.year
        hm_df['Month']= hm_df.index.month
        heatmap_data  = hm_df.pivot(index='Year', columns='Month', values='Return')
        plt.figure(figsize=(14, max(6, len(heatmap_data) * 0.55)))
        sns.heatmap(heatmap_data * 100, annot=True, fmt='.1f',
                    cmap='RdYlGn', center=0, cbar=False)
        plt.title('Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        hm_file = f'{save_prefix}_heatmap.png'
        plt.savefig(hm_file, dpi=150)
        print(f"[Graphics] Saved → {hm_file}")
        plt.close()
    except Exception as e:
        print(f"[Graphics] Heatmap failed: {e}")


def print_yearly_returns(portfolio_value):
    yearly = portfolio_value.resample('YE').last().pct_change()

    # Drawdown series computed off the running (all-time) peak, then take
    # the worst (minimum) drawdown observed within each calendar year.
    dd_series    = (portfolio_value / portfolio_value.cummax()) - 1
    yearly_maxdd = dd_series.resample('YE').min()

    print("\n" + "=" * 34)
    print("  Yearly Returns & Drawdown")
    print("=" * 34)
    print(f"{'Year':<6} | {'Return':>8} | {'Max DD':>8}")
    print("-" * 32)
    for dt, ret in yearly.items():
        if pd.notna(ret):
            mdd = yearly_maxdd.get(dt, float('nan'))
            mdd_str = f"{mdd*100:>7.2f}%" if pd.notna(mdd) else f"{'N/A':>8}"
            print(f"{dt.year:<6} | {ret*100:>7.2f}% | {mdd_str}")
    print("=" * 34)


# ══════════════════════════════════════════════════════════════════════════════
# SLICE & REBASE HELPER
# ══════════════════════════════════════════════════════════════════════════════

def slice_results(res, start_date, risk_free_rate=0.0):
    """
    Trim results to the reporting window and recompute all metrics on the
    sliced data so the report reflects only the declared period.
    """
    eq = res['equity_curve']

    if start_date not in eq.index:
        idx = eq.index.searchsorted(start_date)
        if idx >= len(eq):
            print(f"WARNING: start_date {start_date} is after data end — not slicing.")
            return res
        start_date = eq.index[idx]

    res['equity_curve']     = eq.loc[start_date:]
    res['equity_curve']     = res['equity_curve'] / res['equity_curve'].iloc[0] * 100_000
    res['portfolio_value']  = res['equity_curve']
    if 'benchmark' in res:
        bm = res['benchmark'].loc[start_date:]
        res['benchmark'] = bm / bm.iloc[0] * 100_000
    res['net_returns']      = res['net_returns'].loc[start_date:]
    res['executed_weights'] = res['executed_weights'].loc[start_date:]

    eq  = res['equity_curve']
    ret = res['net_returns']

    n_years   = (eq.index[-1] - eq.index[0]).days / 365.25
    daily_rfr = (1 + risk_free_rate) ** (1 / 252) - 1

    res['cagr']          = (eq.iloc[-1] / eq.iloc[0]) ** (1 / n_years) - 1 if n_years > 0 else 0
    res['total_return']  = eq.iloc[-1] / eq.iloc[0] - 1
    res['ann_volatility']= ret.std() * np.sqrt(252)

    excess         = ret - daily_rfr
    res['sharpe']  = (np.sqrt(252) * excess.mean() / ret.std()
                      if ret.std() != 0 else 0)

    _dn            = ret.clip(upper=0.0)
    _dndev         = np.sqrt((_dn ** 2).mean())
    res['sortino'] = (np.sqrt(252) * ret.mean() / _dndev if _dndev > 0 else 0)

    running_max         = eq.cummax()
    dd_series           = (eq / running_max) - 1
    res['max_drawdown'] = dd_series.min()
    res['calmar']       = (res['cagr'] / abs(res['max_drawdown'])
                           if res['max_drawdown'] != 0 else 0)

    monthly_res     = res['portfolio_value'].resample('ME').last().pct_change()
    res['win_rate'] = (monthly_res.dropna() > 0).mean()

    if 'executed_weights' in res and n_years > 0:
        # Skip first row — .diff() at slice boundary produces full weight values
        # (diff vs NaN) rather than real weight changes.
        wc = res['executed_weights'].diff().abs().iloc[1:]
        res['ann_turnover'] = float(wc.sum().sum()) / 2.0 / n_years

    res['daily_win_rate'] = (ret > 0).mean()

    # Initialise trade-basis metrics (populated after trade log is built)
    for key in [
        'trade_win_rate', 'total_trades_count', 'avg_trade_return',
        'median_trade_return', 'avg_holding_days', 'best_trade', 'worst_trade',
        'avg_win_pct', 'avg_loss_pct', 'payoff_ratio', 'profit_factor',
        'profit_factor_dollar', 'pct_hard_stops', 'pct_trail_stops',
        'pct_stale', 'pct_end_data', 'avg_mae', 'avg_mfe',
    ]:
        res.setdefault(key, 0.0)

    # Save daily backtest log CSV
    log                    = pd.DataFrame(index=eq.index)
    log['Portfolio_Value'] = res['portfolio_value']
    log['Net_Return']      = ret
    w                      = res['executed_weights']
    log['Positions']       = (w > 1e-6).sum(axis=1)
    log['Exposure']        = w.sum(axis=1)
    log['Drawdown']        = dd_series
    log.to_csv('vcp_backtest_logs.csv')
    print(f"[Logs] vcp_backtest_logs.csv  ({len(log)} rows)")

    return res


# ══════════════════════════════════════════════════════════════════════════════
# BACKTEST ENGINE  (standalone — strategy instance passed as first argument)
# ══════════════════════════════════════════════════════════════════════════════

def backtest_event_driven(
        strategy,
        initial_capital  = 100_000.0,
        transaction_cost = 0.003,
        risk_free_rate   = 0.0,
        cash_yield       = None,    # annual yield on idle cash (liquid fund); None = risk_free_rate, the old behaviour
) -> dict:
    """
    Main event-driven daily backtest loop for VCP/SEPA strategy.

    Execution model (all T-1 safe):
      Signal  : TT + VCP conditions evaluated on T-1 data
      Entry   : T open (next bar's open)
      Exit 1  : Stop (hard/trail) — T low triggers; fill at T open or stop level
      Exit 2  : Stale trade — fill at T open
      Exit 3  : End of data — fill at last close
      Warmup  : first warmup_days bars → no new entries
    """
    if not hasattr(strategy, '_prices_ff'):
        raise ValueError("Call calculate_factors() first.")

    print(f"[Backtest] Starting — universe rank {strategy.universe_min_n}–"
          f"{strategy.universe_top_n} | capital ₹{initial_capital:,.0f}")

    prices_ff  = strategy._prices_ff
    opens_ff   = strategy._opens_ff
    open_proxy = strategy._open_proxy
    highs_ff   = strategy._highs_ff
    lows_ff    = strategy._lows_ff

    # Circuit-breaker mask: high == low on the day
    if not strategy.highs.empty and not strategy.lows.empty:
        is_circuit = (highs_ff == lows_ff)
    else:
        is_circuit = pd.DataFrame(False, index=prices_ff.index,
                                  columns=prices_ff.columns)

    # Regime flag (precomputed, vectorised, no lookahead)
    regime_on = strategy._compute_regime_flags()

    # Simple close-to-close returns — used ONLY to drive the running
    # portfolio-value estimate that feeds next-bar sizing decisions.
    # (Final reported performance still uses the precise entry/exit-corrected
    # returns computed after the loop — this is a sizing-time approximation.)
    simple_daily_ret = prices_ff.pct_change(fill_method=None).fillna(0.0)

    daily_rfr  = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0
    daily_cash = ((1.0 + cash_yield) ** (1.0 / 252) - 1.0) if cash_yield is not None else daily_rfr
    dates      = prices_ff.index
    all_stocks = list(prices_ff.columns)

    # ── Fast numpy lookups ──────────────────────────────────────────────────
    # Pandas .iloc[i].get(stock) inside a hot per-stock loop is the single
    # biggest cost in the old loop (row extraction + dict-like lookup on every
    # call). Converting the handful of DataFrames actually read bar-by-bar to
    # plain numpy arrays + a stock→column-index map turns each lookup into a
    # single O(1) array index — no pandas overhead per access.
    col_idx      = {s: j for j, s in enumerate(all_stocks)}
    prices_arr   = prices_ff.to_numpy(dtype=float)
    highs_arr    = highs_ff.to_numpy(dtype=float)
    lows_arr     = lows_ff.to_numpy(dtype=float)
    opens_arr    = opens_ff.to_numpy(dtype=float)
    openpx_arr   = open_proxy.to_numpy(dtype=float)
    circuit_arr  = is_circuit.to_numpy(dtype=bool)
    atr_arr      = strategy._atr14.to_numpy(dtype=float)
    dvol_arr     = strategy._dvol_avg63.to_numpy(dtype=float)

    def _v(arr, row, stock, default=np.nan):
        j = col_idx.get(stock)
        if j is None:
            return default
        return arr[row, j]

    # ── Mutable state ─────────────────────────────────────────────────────────
    active_holdings:       dict = {}   # ticker → holding dict
    lockout_until:         dict = {}   # ticker → pd.Timestamp (re-entry allowed after)
    executed_weights_list        = []
    strategy.position_metadata   = []

    # Running portfolio value — updated once per bar, used for NEXT bar's
    # sizing decisions (liquidity cap conversion). No lookahead: the value
    # used to size day i's entries reflects capital through end of day i-1.
    running_value = float(initial_capital)

    n_hard_stops  = 0
    n_trail_stops = 0
    n_stale_exits = 0

    for i, date in enumerate(dates):

        # First bar: seed with zeros
        if i == 0:
            executed_weights_list.append(pd.Series(0.0, index=all_stocks))
            continue

        exited_today: set = set()

        # ── STEP A: Exit evaluation ───────────────────────────────────────────
        for stock in list(active_holdings.keys()):

            today_close = float(_v(prices_arr, i, stock, np.nan))
            if pd.isna(today_close) or today_close <= 0:
                continue

            today_high  = float(_v(highs_arr, i, stock, today_close))
            today_low   = float(_v(lows_arr,  i, stock, today_close))
            today_open  = float(_v(opens_arr, i, stock, np.nan))
            if pd.isna(today_open) or today_open <= 0:
                today_open = float(_v(openpx_arr, i, stock, today_close))

            h          = active_holdings[stock]
            entry_date = h['entry_date']
            days_held  = (date - entry_date).days

            # Circuit day: locked price — defer all exit decisions
            _CIRCUIT_TIMEOUT_DAYS = 10   # hardcoded, backtest only
            if bool(_v(circuit_arr, i, stock, False)):
                h['circuit_days'] = h.get('circuit_days', 0) + 1
                if h['circuit_days'] < _CIRCUIT_TIMEOUT_DAYS:
                    continue
                # Extended lock — force exit to bound suspension risk
                strategy._record_closed_trade(
                    ticker      = stock,
                    holding     = h,
                    exit_date   = date,
                    exit_price  = today_open,
                    fill_price  = today_open,
                    exit_reason = 'CIRCUIT_TIMEOUT',
                    hard_stop   = h['hard_stop'],
                )
                del active_holdings[stock]
                exited_today.add(stock)
                continue
            h['circuit_days'] = 0   # reset on non-circuit day

            # T-1 settled close — peak update and profit check
            prev_close = float(_v(prices_arr, i - 1, stock, np.nan))

            # Compute effective stop (updates peak + trail state in h)
            eff_stop = strategy._effective_stop(h, prev_close, days_held)
            active_holdings[stock] = h

            # ── Exit 1: Hard / Trailing Stop ──────────────────────────────────
            # Triggered when today's low breaches effective stop.
            # Fill at today's open if open <= stop, else at stop level.
            if not pd.isna(today_low) and today_low <= eff_stop:
                fill        = today_open if today_open <= eff_stop else eff_stop
                exit_reason = 'TRAIL_STOP' if h.get('trail_active', False) else 'HARD_STOP'
                strategy._record_closed_trade(
                    ticker      = stock,
                    holding     = h,
                    exit_date   = date,
                    exit_price  = today_close,
                    fill_price  = float(fill),
                    exit_reason = exit_reason,
                    hard_stop   = h['hard_stop'],
                )
                del active_holdings[stock]
                exited_today.add(stock)
                lockout_until[stock] = date + pd.Timedelta(days=strategy.lockout_days)
                if exit_reason == 'TRAIL_STOP':
                    n_trail_stops += 1
                else:
                    n_hard_stops  += 1
                continue

            # ── Exit 2: Stale Trade ────────────────────────────────────────────
            # Held >= stale_days calendar days AND return < stale_ret_pct.
            # Profit measured on T-1 settled close, fill at today's open.
            _BACKTEST_STALE_RET = strategy.stale_ret_pct   # uses class param (live parity)
            if days_held >= strategy.stale_days:
                entry_px = h['entry_price']
                ret      = (prev_close / entry_px) - 1.0 \
                           if (not pd.isna(prev_close) and entry_px > 0) else 0.0
                if ret < _BACKTEST_STALE_RET:
                    strategy._record_closed_trade(
                        ticker      = stock,
                        holding     = h,
                        exit_date   = date,
                        exit_price  = today_open,
                        fill_price  = today_open,
                        exit_reason = 'STALE',
                        hard_stop   = h['hard_stop'],
                    )
                    del active_holdings[stock]
                    exited_today.add(stock)
                    n_stale_exits += 1
                    continue

            # Still holding — update MAE/MFE trackers using T-1 settled close
            if not pd.isna(prev_close) and prev_close > 0:
                h['min_price'] = min(h.get('min_price', prev_close), prev_close)
                h['max_price'] = max(h.get('max_price', prev_close), prev_close)
            active_holdings[stock] = h

        # ── STEP B: New entry signals ─────────────────────────────────────────
        skip_entries = (i < strategy.warmup_days) or (not bool(regime_on.iloc[i]))

        if not skip_entries:
            # Universe + Trend Template + VCP masks — all precomputed once for
            # the whole history in _precompute_signal_matrices(); this is now
            # a single row lookup instead of a per-day/per-stock recomputation.
            eligible = (strategy._universe_mask_matrix.iloc[i - 1]
                        & strategy._trend_mask_matrix.iloc[i - 1]
                        & strategy._vcp_signal_matrix.iloc[i - 1])

            # Exclude already-held / exited-today / locked-out — vectorised
            # (these sets are always small: bounded by max_positions/turnover,
            # so building a mask from them costs nothing).
            if active_holdings:
                held = pd.Series(True, index=list(active_holdings.keys()))
                eligible = eligible & ~held.reindex(all_stocks, fill_value=False)
            if exited_today:
                exited_s = pd.Series(True, index=list(exited_today))
                eligible = eligible & ~exited_s.reindex(all_stocks, fill_value=False)
            if lockout_until:
                locked = [s for s, until in lockout_until.items() if date < until]
                if locked:
                    lock_s = pd.Series(True, index=locked)
                    eligible = eligible & ~lock_s.reindex(all_stocks, fill_value=False)

            eligible_stocks = eligible[eligible].index

            # RS scores for ranking (T-1 cross-sectional) — computed over ALL
            # stocks with a valid 1y return (matches original basis exactly,
            # separate from TT8's universe-restricted percentile), then
            # restricted to the eligible set for candidate selection.
            ret_row_full = strategy._ret_1y.iloc[i - 1].dropna()
            if len(ret_row_full) > 0:
                rs_scores_full = ret_row_full.rank(pct=True) * 100
            else:
                rs_scores_full = pd.Series(dtype=float)
            candidate_rs = rs_scores_full.reindex(eligible_stocks).dropna() \
                                         .sort_values(ascending=False)
            candidates = list(candidate_rs.items())   # already RS-descending

            slots_available = strategy.max_positions - len(active_holdings)

            # Collect fully-sized candidates first; commit only after
            # portfolio-level normalisation (STEP C below).
            new_entries = []

            for stock, rs in candidates[:max(0, slots_available)]:

                # Entry fill at today's open
                today_open_entry = float(_v(opens_arr, i, stock, np.nan))
                if pd.isna(today_open_entry) or today_open_entry <= 0:
                    today_open_entry = float(_v(openpx_arr, i, stock, np.nan))
                if pd.isna(today_open_entry) or today_open_entry <= 0:
                    continue

                # Gap-cancel: skip if open gaps >entry_gap_cancel_pct above prior close
                prev_c = float(_v(openpx_arr, i, stock, np.nan))
                if pd.notna(prev_c) and prev_c > 0:
                    if (today_open_entry / prev_c) - 1.0 > strategy.entry_gap_cancel_pct:
                        continue

                # Circuit day: no fill
                if bool(_v(circuit_arr, i, stock, False)):
                    continue

                entry_price = today_open_entry

                # ── ATR-based distance (dynamic multiplier, HR chandelier logic) ──
                # _dynamic_atr_multiplier: calm stocks → higher mult (wider in %),
                # volatile stocks → lower mult (tighter in %). Reused below both
                # for the trailing-stop distance and for risk-sizing math.
                curr_atr = float(_v(atr_arr, i - 1, stock, np.nan))
                if pd.isna(curr_atr) or curr_atr <= 0:
                    curr_atr = entry_price * 0.02   # 2% fallback
                atr_pct_entry      = curr_atr / entry_price
                entry_atr_mult     = strategy._dynamic_atr_multiplier(atr_pct_entry)
                trail_atr_distance = entry_atr_mult * curr_atr

                hard_stop = entry_price * (1.0 - strategy.hard_stop_pct)

                # ── Risk-based position sizing ──────────────────────────────────
                # Notional-only: this stop distance sizes the position but is NOT
                # the actual exit stop (the real exit stays the flat hard_stop
                # above; trailing kicks in separately once activated).
                # initial_stop = tighter of the flat floor or the ATR distance.
                atr_stop     = entry_price - trail_atr_distance
                initial_stop = max(hard_stop, atr_stop)
                stop_pct     = (entry_price - initial_stop) / entry_price

                if stop_pct > 0:
                    risk_weight = strategy.risk_pct_per_trade / stop_pct
                else:
                    risk_weight = strategy.weight_min   # invalid stop distance → floor

                risk_weight = min(max(risk_weight, strategy.weight_min), strategy.weight_max)

                # Liquidity cap acts only as an upper bound — never forces the
                # weight below weight_min (the floor always wins).
                dvol_val = float(_v(dvol_arr, i - 1, stock, np.nan))
                if pd.notna(dvol_val) and dvol_val > 0 and running_value > 0:
                    liquidity_limit = (strategy.liquidity_cap_pct * dvol_val) / running_value
                    intended_weight = max(strategy.weight_min, min(risk_weight, liquidity_limit))
                else:
                    intended_weight = risk_weight

                obs = strategy._obs_enrichment(stock, i, entry_price)

                new_entries.append({
                    'stock'             : stock,
                    'entry_date'        : date,
                    'entry_price'       : entry_price,
                    'hard_stop'         : hard_stop,
                    'trail_atr_distance': trail_atr_distance,
                    'intended_weight'   : intended_weight,
                    'obs'               : obs,
                })

            # ── STEP C: Portfolio-level normalisation (new entries only) ─────────
            # Existing holdings keep the weight they were already assigned —
            # only today's new entries get scaled down if they'd push total
            # exposure over 100%.
            existing_total  = sum(h['weight'] for h in active_holdings.values())
            available_room  = max(0.0, 1.0 - existing_total)
            sum_intended    = sum(e['intended_weight'] for e in new_entries)

            if sum_intended > available_room and sum_intended > 0:
                scale = available_room / sum_intended
            else:
                scale = 1.0

            for e in new_entries:
                final_weight = e['intended_weight'] * scale
                if final_weight < 1e-4:
                    # Normalised away to ~nothing (book already full) — don't
                    # open a meaningless position or consume a max_positions slot.
                    continue
                active_holdings[e['stock']] = {
                    'entry_date'        : e['entry_date'],
                    'entry_price'       : e['entry_price'],
                    'hard_stop'         : e['hard_stop'],
                    'trail_stop'        : e['hard_stop'],   # initialised to hard stop
                    'trail_active'      : False,
                    'peak_price'        : e['entry_price'],
                    'trail_atr_distance': e['trail_atr_distance'],
                    'weight'            : final_weight,
                    'intended_weight'   : e['intended_weight'],
                    'min_price'         : e['entry_price'],
                    'max_price'         : e['entry_price'],
                    'circuit_days'      : 0,
                    'obs'               : e['obs'],
                }

        # ── Build executed weights ────────────────────────────────────────────
        raw_weights = pd.Series(0.0, index=all_stocks)
        for stock, h in active_holdings.items():
            raw_weights[stock] = h['weight']

        total_w = raw_weights.sum()
        if total_w > 1.0:
            # Safety net only — STEP C normalisation should already prevent this.
            raw_weights = raw_weights / total_w

        # ── Running portfolio value update (drives NEXT bar's sizing) ─────────
        prior_weights = executed_weights_list[-1]
        day_ret   = float((prior_weights * simple_daily_ret.iloc[i]).sum())
        cash_ret  = float(max(0.0, 1.0 - prior_weights.sum()) * daily_cash)
        txn_today = float((raw_weights - prior_weights).abs().sum() * transaction_cost)
        running_value *= (1.0 + day_ret + cash_ret - txn_today)
        running_value = max(running_value, 1e-6)   # guard against runaway drawdown

        executed_weights_list.append(raw_weights.copy())

    # ── Close any positions still open at end of data ─────────────────────────
    last_date = dates[-1]
    for stock, h in active_holdings.items():
        last_close = float(prices_ff.at[last_date, stock]) \
                     if stock in prices_ff.columns else np.nan
        last_open  = float(opens_ff.at[last_date, stock]) \
                     if stock in opens_ff.columns else np.nan
        if pd.isna(last_open) or last_open <= 0:
            last_open = last_close
        strategy._record_closed_trade(
            ticker      = stock,
            holding     = h,
            exit_date   = last_date,
            exit_price  = last_close,
            fill_price  = last_open,
            exit_reason = 'END_OF_DATA',
            hard_stop   = h['hard_stop'],
        )
    active_holdings.clear()

    print(f"[VCP] Hard stops    : {n_hard_stops}")
    print(f"[VCP] Trail stops   : {n_trail_stops}")
    print(f"[VCP] Stale exits   : {n_stale_exits}")

    # ── Assemble executed-weights DataFrame ───────────────────────────────────
    executed_weights = pd.DataFrame(
        executed_weights_list, index=dates
    ).fillna(0.0)

    # ── Per-trade return correction (entry day + exit day) ────────────────────
    # Entry day: replace close-to-close with open-to-close
    # Exit day : replace close-to-close with prev-close-to-fill
    _dr = strategy.prices.pct_change(fill_method=None).fillna(0.0)

    for meta in strategy.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        entry_price = meta['Entry_Price']
        exit_date   = meta['Exit_Date']
        exit_price  = meta['Exit_Price']

        if ticker not in _dr.columns:
            continue

        if entry_date in _dr.index and pd.notna(entry_price) and entry_price > 0:
            entry_loc   = _dr.index.get_loc(entry_date)
            close_entry = strategy.prices.iloc[entry_loc].get(ticker, np.nan)
            if pd.notna(close_entry) and close_entry > 0:
                _dr.at[entry_date, ticker] = (close_entry / entry_price) - 1.0

        if exit_date in _dr.index and pd.notna(exit_price) and exit_price > 0:
            exit_loc = _dr.index.get_loc(exit_date)
            if exit_loc > 0:
                prev_c = strategy.prices.iloc[exit_loc - 1].get(ticker, np.nan)
                if pd.notna(prev_c) and prev_c > 0:
                    _dr.at[exit_date, ticker] = (exit_price / prev_c) - 1.0

    # ── Portfolio returns ─────────────────────────────────────────────────────
    gross_ret   = (executed_weights * _dr).sum(axis=1)
    total_w     = executed_weights.sum(axis=1)
    cash_w      = (1.0 - total_w).clip(lower=0.0)
    cash_ret    = cash_w * daily_cash

    # Transaction cost on actual weight change (entries/exits), not a flat
    # per-trade weight — needed now that position weights vary by trade.
    w_diff = executed_weights.diff()
    w_diff.iloc[0] = executed_weights.iloc[0]   # first row: change from 0
    txn_cost = w_diff.abs().sum(axis=1) * transaction_cost

    net_returns = gross_ret + cash_ret - txn_cost

    equity_curve    = (1.0 + net_returns).cumprod()
    portfolio_value = equity_curve * initial_capital

    # ── Performance metrics ───────────────────────────────────────────────────
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

    _mret    = portfolio_value.resample('ME').last().pct_change().dropna()
    win_rate = (_mret > 0).mean()

    # Turnover: abs weight changes / 2 / years
    weight_changes = executed_weights.diff().abs()
    ann_turn       = float(weight_changes.sum().sum()) / 2.0 / n_years \
                     if n_years > 0 else 0.0

    strategy.results = {
        'equity_curve'    : equity_curve,
        'portfolio_value' : portfolio_value,
        'net_returns'     : net_returns,
        'executed_weights': executed_weights,
        'total_return'    : float(equity_curve.iloc[-1] - 1.0),
        'cagr'            : cagr,
        'sharpe'          : sharpe,
        'sortino'         : sortino,
        'calmar'          : calmar,
        'max_drawdown'    : max_dd,
        'ann_volatility'  : ann_vol,
        'win_rate'        : win_rate,
        'daily_win_rate'  : (net_returns > 0).mean(),
        'ann_turnover'    : ann_turn,
    }

    print(f"\n[VCP] CAGR={cagr*100:.2f}%  Sharpe={sharpe:.2f}  MaxDD={max_dd*100:.2f}%")
    return strategy.results


# ══════════════════════════════════════════════════════════════════════════════
# TRADE LOG  (standalone — strategy instance passed as first argument)
# ══════════════════════════════════════════════════════════════════════════════

def get_trade_log(strategy) -> pd.DataFrame:
    """
    Build a trade-log DataFrame from strategy.position_metadata.
    Must be called after backtest_event_driven().
    """
    if not strategy.position_metadata:
        print("Warning: No trade metadata. Run backtest_event_driven() first.")
        return pd.DataFrame()

    equity_curve     = strategy.results['equity_curve']     if strategy.results else None
    executed_weights = strategy.results['executed_weights'] if strategy.results else None
    prices_ffill     = strategy.prices.ffill()

    _equity_lookup = (equity_curve.ffill() * 100_000) if equity_curve is not None else None

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

        weight = meta['Weight']
        if executed_weights is not None and ticker in executed_weights.columns:
            ew_col  = executed_weights[ticker]
            window  = ew_col.loc[(ew_col.index > entry_date) & (ew_col.index <= exit_date)]
            nonzero = window[window > 1e-9]
            if not nonzero.empty:
                weight = float(nonzero.iloc[0])

        port_val = np.nan
        if _equity_lookup is not None:
            if entry_date in _equity_lookup.index:
                port_val = float(_equity_lookup.loc[entry_date])
            else:
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
            'Ticker'        : ticker,
            'Entry_Date'    : entry_date,
            'Entry_Price'   : meta['Entry_Price'],
            'Exit_Date'     : exit_date,
            'Exit_Price'    : round(exit_price, 4)       if pd.notna(exit_price)  else np.nan,
            'Close_At_Exit' : meta.get('Close_At_Exit',  np.nan),
            'Hard_Stop'     : meta.get('Hard_Stop',      np.nan),
            'Trail_Stop'    : meta.get('Trail_Stop',     np.nan),
            'Trail_Active'  : meta.get('Trail_Active',   False),
            'Exit_Reason'   : meta['Exit_Reason'],
            'Weight'        : round(weight, 6),
            'Intended_Weight': meta.get('Intended_Weight', weight),
            'Quantity'      : round(qty, 4)              if pd.notna(qty)         else np.nan,
            'Position_Size' : round(weight * port_val, 2)
                              if (pd.notna(port_val) and weight > 0)              else 0.0,
            'Portfolio_Value': round(port_val, 2)        if pd.notna(port_val)    else np.nan,
            'PnL_Pct'       : round(pnl_pct, 4)         if pd.notna(pnl_pct)     else np.nan,
            'PnL_Abs'       : round(pnl_abs, 2)         if pd.notna(pnl_abs)     else np.nan,
            'Holding_Days'  : holding_days,
            'MAE_Pct'       : meta.get('MAE_Pct',        np.nan),
            'MFE_Pct'       : meta.get('MFE_Pct',        np.nan),
            # Observational enrichment
            'ATR_Ratio'     : meta.get('ATR_Ratio',      np.nan),
            'Dist_52w_High' : meta.get('Dist_52w_High',  np.nan),
            'Dist_SMA50'    : meta.get('Dist_SMA50',     np.nan),
            'Dist_SMA200'   : meta.get('Dist_SMA200',    np.nan),
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values('Entry_Date').reset_index(drop=True)
        df.index += 1
        df.index.name = 'Trade_ID'

    wins   = (df['PnL_Pct'] > 0).sum() if not df.empty else 0
    losses = (df['PnL_Pct'] < 0).sum() if not df.empty else 0
    total  = len(df)
    if total > 0:
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {losses}"
              f" | Win Rate: {wins/total*100:.1f}%")
        print(f"[Trade Log] Worst: {df['PnL_Pct'].min():.2f}%"
              f"  Best: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
    return df


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main(load_start=None, load_end=None, start_report=None, universe=None):
    # ── 1. Load Data ──────────────────────────────────────────────────────────
    data_folder = "/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data"
    print("Loading data...")
    prices, volumes, highs, lows, opens = load_data(data_folder)

    if prices.empty:
        print("Error: No data loaded.")
        return

    start_load   = '2002-01-01'
    end_load     = '2025-12-31'
    report_start = '2003-01-01'

    if load_start and load_end and start_report:
        start_load   = load_start
        end_load     = load_end
        report_start = start_report

    prices  = prices.loc[start_load:end_load]
    volumes = volumes.loc[start_load:end_load]
    if not highs.empty:  highs  = highs.loc[start_load:end_load]
    if not lows.empty:   lows   = lows.loc[start_load:end_load]
    if not opens.empty:  opens  = opens.loc[start_load:end_load]

    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()}  →  {prices.index.max().date()}")

    # ── 2. Instantiate Strategy ───────────────────────────────────────────────
    strategy = VCPBreakoutStrategy(
        prices_df              = prices,
        volumes_df             = volumes,
        highs_df               = highs,
        lows_df                = lows,
        opens_df               = opens,
        # Universe
        universe_top_n         = 1000,
        universe_min_n         = 500,
        min_price              = 10.0,
        max_circuit_days       = 5,
        ca_drop_thresh         = 0.40,
        ca_gain_thresh         = 3.00,
        # Regime
        bench_sma_period       = 50,
        bench_consec_days      = 5,
        # Trend Template
        sma_fast               = 50,
        sma_mid                = 150,
        sma_slow               = 200,
        sma_slope_lookback     = 20,
        high_52w_period        = 252,
        within_52w_high_pct    = 0.25,
        rs_period              = 252,
        rs_min_percentile      = 75,
        # VCP Signal
        vcp_base_window        = 15,
        vcp_base_tight_pct     = 0.15,
        vcp_vol_contract_pct   = 0.80,
        vcp_vol_base_window    = 30,
        vcp_breakout_window    = 20,
        vcp_near_high_pct      = 0.10,
        # Entry execution
        max_positions          = 10,
        entry_gap_cancel_pct   = 0.03,
        # Position sizing (risk-based)
        risk_pct_per_trade    = 0.01,
        weight_min             = 0.02,
        weight_max             = 0.20,
        liquidity_cap_pct      = 0.10,
        # Exits
        hard_stop_pct          = 0.15,
        trail_activate_pct     = 0.10,
        trail_pct              = 0.05,
        trail_floor_pct        = 0.001,
        trail_atr_mult_max     = 2.5,
        trail_atr_mult_min     = 1.5,
        trail_atr_pct_calm     = 0.020,
        trail_atr_pct_volatile = 0.045,
        min_hold_days          = 15,
        stale_days             = 60,
        stale_ret_pct          = 0.05,
        lockout_days           = 30,
        warmup_days            = 252,
    )

    # ── 3. Pre-compute indicators ─────────────────────────────────────────────
    strategy.calculate_factors()
    benchmark_series = strategy._bench_series

    # ── 4. Backtest ───────────────────────────────────────────────────────────
    results = backtest_event_driven(
        strategy,
        initial_capital  = 100_000,
        transaction_cost = 0.003,
        risk_free_rate   = 0.0,
        cash_yield       = 0.065,   # idle cash in a liquid fund (was 0%); live, the idle balance must actually be swept there
    )
    results['benchmark'] = benchmark_series

    # ── 5. Trade log ──────────────────────────────────────────────────────────
    report_start_dt = pd.Timestamp(report_start)
    detailed_log    = pd.DataFrame()
    try:
        _full_log = get_trade_log(strategy)
        if not _full_log.empty:
            detailed_log = _full_log[
                _full_log['Entry_Date'] >= report_start_dt
            ].copy()
            detailed_log.to_csv('vcp_detailed_trade_log.csv', index=False)
            print(f"\n[Logs] vcp_detailed_trade_log.csv  "
                  f"({len(detailed_log)} trades from {report_start_dt.date()})")
    except Exception as e:
        print(f"\n[Logs] Warning: Trade log failed: {e}")

    # ── 6. Slice to reporting period ──────────────────────────────────────────
    results = slice_results(results, report_start, risk_free_rate=0.0)

    # ── 7. Populate trade-basis metrics ──────────────────────────────────────
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
        results['avg_mae']             = dl['MAE_Pct'].mean()
        results['avg_mfe']             = dl['MFE_Pct'].mean()

        avg_win  = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].mean() if wins   > 0 else 0.0
        avg_loss = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().mean() if losses > 0 else 0.0
        results['avg_win_pct']  = avg_win
        results['avg_loss_pct'] = avg_loss
        results['payoff_ratio'] = avg_win / avg_loss if avg_loss > 0 else float('inf')

        gw_pct = dl.loc[dl['PnL_Pct'] > 0, 'PnL_Pct'].sum()
        gl_pct = dl.loc[dl['PnL_Pct'] < 0, 'PnL_Pct'].abs().sum()
        results['profit_factor'] = gw_pct / gl_pct if gl_pct > 0 else float('inf')

        gw_abs = dl.loc[dl['PnL_Abs'] > 0, 'PnL_Abs'].sum()
        gl_abs = dl.loc[dl['PnL_Abs'] < 0, 'PnL_Abs'].abs().sum()
        results['profit_factor_dollar'] = gw_abs / gl_abs if gl_abs > 0 else float('inf')

        reason_counts = dl['Exit_Reason'].value_counts()
        results['pct_hard_stops']  = reason_counts.get('HARD_STOP',  0) / total_t * 100
        results['pct_trail_stops'] = reason_counts.get('TRAIL_STOP', 0) / total_t * 100
        results['pct_stale']       = reason_counts.get('STALE',      0) / total_t * 100
        results['pct_end_data']    = reason_counts.get('END_OF_DATA',0) / total_t * 100

    # ── 8. Performance Report ─────────────────────────────────────────────────
    W   = 38
    SEP = "=" * W

    print(f"\n{SEP}")
    print(f"  VCP BREAKOUT  —  PERFORMANCE REPORT")
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
        print(f"  Avg MAE           : {results.get('avg_mae', 0):>8.2f}%")
        print(f"  Avg MFE           : {results.get('avg_mfe', 0):>8.2f}%")
    else:
        print("  No completed trades in reporting period.")

    print(f"\n── Exit Breakdown ────────────────────")
    if results['total_trades_count'] > 0:
        print(f"  Hard Stop         : {results['pct_hard_stops']:>8.1f}%")
        print(f"  Trail Stop        : {results['pct_trail_stops']:>8.1f}%")
        print(f"  Stale             : {results['pct_stale']:>8.1f}%")
        print(f"  End of Data       : {results.get('pct_end_data', 0):>8.1f}%")

    print(f"\n── Turnover ──────────────────────────")
    if 'ann_turnover' in results:
        print(f"  Ann Turnover      : {results['ann_turnover']*100:>8.2f}%")

    # ── 9. Yearly returns + charts ────────────────────────────────────────────
    print_yearly_returns(results['portfolio_value'])
    bench_slice = results.get(
        'benchmark',
        benchmark_series.reindex(results['equity_curve'].index).ffill()
    )
    plot_performance(results, bench_slice)

    return {
        'cagr'           : results['cagr'] * 100,
        'drawdown'       : results['max_drawdown'] * 100,
        'trade_win_rate' : results['trade_win_rate'] * 100,
        'calmar'         : results['calmar'],
    }


if __name__ == "__main__":
    main()
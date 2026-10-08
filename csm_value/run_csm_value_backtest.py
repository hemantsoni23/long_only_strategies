"""
run_csm_value_backtest.py -- backtest runner for CSMValue (E/P on the Elendel chassis). Generated from Old_live_strategies/run_csm_elendel_backtest.py by _generate_elendel_chassis.py;
the event-driven engine (_run_backtest_core), overlays, logs, performance report, IC/ICIR and realized-IC sections are Elendel's. Reporting window 2019-06 -> 2025-06 (fundamentals limit).
"""
import os
import sys

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from csm_value_strategy import CSMValue


VERSION_TAG = 'ey'
# Which booking is the HEADLINE.  False = the Elendel engine's own booking, directly comparable with the Elendel / Zenith / Quad backtests (CSM Value FULL window: 38.5% CAGR, -12.6% max DD).
# True = execution-faithful booking (charges the gap to the real fill; AUDIT.md: 20.0% / -23.0%).  Both are always computed and both are printed in the 'Accounting cross-check' block.
EXECUTION_FAITHFUL_ACCOUNTING = False
data_folder_path = '/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data'


OUTPUT_DIR = os.path.join(_HERE, 'output')


def _out(name):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    return os.path.join(OUTPUT_DIR, name)


# ══════════════════════════════════════════════════════════════════════════════
# PLOTTING
# ══════════════════════════════════════════════════════════════════════════════

def plot_performance(results, benchmark_series=None):
    equity           = results['equity_curve']
    dd               = (equity / equity.cummax()) - 1
    executed_weights = results.get('executed_weights', None)

    fig = plt.figure(figsize=(16, 20))
    gs  = fig.add_gridspec(4, 2)

    # Panel 1: Equity Curve
    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(equity.index, equity, label='CSM Value (Earnings-Yield)', color='#1f77b4', linewidth=1.5)
    ax1.set_yscale('log')
    if benchmark_series is not None:
        bench_rb = benchmark_series / benchmark_series.iloc[0]
        ax1.plot(bench_rb.index, bench_rb, label='Benchmark', color='gray',
                 linestyle='--', alpha=0.7)
    ax1.set_title('1. Cumulative Growth (Log Scale)', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, which='both', linestyle='--', alpha=0.3)
    ax1.set_ylabel('Portfolio Value')

    # Panel 2: Relative Strength
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
    ax3.fill_between(pos_count.index, pos_count, step='post', color='#9467bd', alpha=0.5)
    ax3.plot(pos_count.index, pos_count, color='#9467bd', linewidth=0.8, drawstyle='steps-post')
    ax3.set_title('3. Active Positions (Daily Count)', fontsize=12, fontweight='bold')
    ax3.grid(True, axis='y', linestyle='--', alpha=0.3)
    ax3.set_ylabel('Count')

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
    plt.savefig(_out(f'csm_value_{VERSION_TAG}_performance.png'), dpi=150)
    plt.close(fig)
    print(f"[Graphics] Saved  →  {_out(f'csm_value_{VERSION_TAG}_performance.png')}")

    # Heatmap
    try:
        hm_df              = pd.DataFrame({'Return': monthly_ret})
        hm_df['Year']      = hm_df.index.year
        hm_df['Month']     = hm_df.index.month
        heatmap_data       = hm_df.pivot(index='Year', columns='Month', values='Return')
        plt.figure(figsize=(14, max(6, len(heatmap_data) * 0.55)))
        sns.heatmap(heatmap_data * 100, annot=True, fmt='.1f',
                    cmap='RdYlGn', center=0, cbar=False)
        plt.title('CSM Value (Earnings-Yield) Momentum — Monthly Returns Heatmap (%)', fontsize=14, fontweight='bold')
        plt.tight_layout()
        plt.savefig(_out(f'csm_value_{VERSION_TAG}_heatmap.png'), dpi=150)
        plt.close()
        print(f"[Graphics] Saved  →  {_out(f'csm_value_{VERSION_TAG}_heatmap.png')}")
    except Exception as e:
        print(f"[Graphics] Heatmap failed: {e}")


def compute_drawdown_stats(dd_series):
    """Episode-based drawdown stats: an episode is one contiguous run below a prior equity high; Avg DD (mean of each episode's own trough) separates one bad stretch from routine pain that MaxDD alone can't show."""
    underwater = dd_series < -1e-12
    episode_id = (~underwater).cumsum().where(underwater)
    if episode_id.notna().sum() == 0:
        return {'avg_drawdown': 0.0, 'avg_drawdown_underwater': 0.0, 'n_episodes': 0}
    episode_depths = dd_series.groupby(episode_id).min()
    return {
        'avg_drawdown':            float(episode_depths.mean()),
        'avg_drawdown_underwater': float(dd_series[underwater].mean()),
        'n_episodes':              int(episode_depths.shape[0]),
    }


def print_yearly_returns(portfolio_value, dd_series=None):
    yearly = portfolio_value.resample('YE').last().pct_change()
    print("\n" + "=" * 48)
    print("  Yearly Returns" + ("  +  Drawdown" if dd_series is not None else ""))
    print("=" * 48)
    if dd_series is not None:
        print(f"{'Year':<6} | {'Return':>8} | {'Yr MaxDD':>9} | {'Yr AvgDD':>9}")
    else:
        print(f"{'Year':<6} | {'Return':>8}")
    print("-" * 48)
    for dt, ret in yearly.items():
        if pd.isna(ret):
            continue
        if dd_series is not None:
            _yr_dd = dd_series[dd_series.index.year == dt.year]
            _yr_max = _yr_dd.min() if len(_yr_dd) else np.nan
            _underwater = _yr_dd[_yr_dd < -1e-12]
            _yr_avg = _underwater.mean() if len(_underwater) else 0.0
            print(f"{dt.year:<6} | {ret*100:>7.2f}% | {_yr_max*100:>8.2f}% | {_yr_avg*100:>8.2f}%")
        else:
            print(f"{dt.year:<6} | {ret*100:>7.2f}%")
    print("=" * 48)
    if dd_series is not None:
        print("  (Yr MaxDD: worst drawdown-from-all-time-peak TOUCHED during the")
        print("   year, not reset each Jan 1. Yr AvgDD: mean depth on days the")
        print("   year was actually underwater -- 0.00% means it stayed at highs.)")


# ══════════════════════════════════════════════════════════════════════════════
# SLICE & REBASE HELPER
# ══════════════════════════════════════════════════════════════════════════════

def slice_results(res, start_date, risk_free_rate=0.06):
    """Trim results to the reporting window and recompute all metrics so the report reflects only the declared period."""
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
    res['net_returns']      = res['net_returns'].loc[start_date:]
    res['executed_weights'] = res['executed_weights'].loc[start_date:]
    for _k in ('turnover', 'vol_scale', 'corr_scale', 'regime', 'n_cooldown_tickers'):
        if _k in res:
            res[_k] = res[_k].loc[start_date:]

    eq  = res['equity_curve']
    ret = res['net_returns']

    n_years   = (eq.index[-1] - eq.index[0]).days / 365.25
    daily_rfr = (1 + risk_free_rate) ** (1 / 252) - 1

    res['cagr']          = (eq.iloc[-1] / eq.iloc[0]) ** (1 / n_years) - 1 if n_years > 0 else 0
    res['total_return']  = eq.iloc[-1] / eq.iloc[0] - 1
    res['ann_volatility'] = ret.std() * np.sqrt(252)

    excess               = ret - daily_rfr
    res['sharpe']        = (np.sqrt(252) * excess.mean() / ret.std()
                            if ret.std() != 0 else 0)

    _dn                  = ret.clip(upper=0.0)
    _dndev               = np.sqrt((_dn ** 2).mean())
    res['sortino']       = (np.sqrt(252) * ret.mean() / _dndev if _dndev > 0 else 0)

    running_max          = eq.cummax()
    dd_series            = (eq / running_max) - 1
    res['dd_series']     = dd_series
    res['max_drawdown']  = dd_series.min()
    res['calmar']        = (res['cagr'] / abs(res['max_drawdown'])
                            if res['max_drawdown'] != 0 else 0)
    res.update(compute_drawdown_stats(dd_series))

    monthly_res          = res['portfolio_value'].resample('ME').last().pct_change()
    res['win_rate']      = (monthly_res.dropna() > 0).mean()

    if 'turnover' in res and n_years > 0:
        res['ann_turnover'] = res['turnover'].sum() / n_years

    res['daily_win_rate'] = (ret > 0).mean()

    # Trade-basis placeholders (populated in main() after detailed log)
    for _k in ('trade_win_rate', 'total_trades_count', 'avg_trade_return',
               'avg_win_pct', 'avg_loss_pct', 'payoff_ratio', 'avg_holding_days',
               'avg_trading_days_held', 'best_trade', 'worst_trade',
               'profit_factor', 'profit_factor_dollar', 'median_trade_return',
               'avg_stop_pct', 'avg_mae', 'avg_mfe'):
        res[_k] = 0.0

    # ── Daily portfolio log ────────────────────────────────────────────
    log = pd.DataFrame(index=eq.index)
    log['Portfolio_Value'] = res['portfolio_value']
    log['Net_Return']      = ret
    w = res['executed_weights']
    log['Positions']       = (w > 1e-6).sum(axis=1)
    log['Exposure']        = w.sum(axis=1)
    log['Drawdown']        = dd_series
    for _k, _col in (('vol_scale', 'Vol_Scale'), ('corr_scale', 'Corr_Scale'),
                     ('regime', 'Regime'), ('n_cooldown_tickers', 'N_Cooldown_Tickers')):
        if _k in res:
            log[_col] = res[_k].reindex(log.index)
    log.to_csv(_out(f'csm_value_{VERSION_TAG}_daily_log.csv'))
    print(f"[Logs] {_out(f'csm_value_{VERSION_TAG}_daily_log.csv')}  ({len(log)} rows)")

    return res


# ══════════════════════════════════════════════════════════════════════════════
# REJECT LOG COUNTERFACTUALS
# ══════════════════════════════════════════════════════════════════════════════

def add_reject_counterfactuals(reject_df, prices):
    """Fill Fwd_Return_21d / Fwd_Return_63d for each reject row: what the blocked entry would have returned over the next 21/63 trading days."""
    if reject_df.empty:
        return reject_df
    prices_ff = prices.ffill()
    idx       = prices_ff.index
    positions = idx.get_indexer(pd.DatetimeIndex(reject_df['Date']))

    for horizon in (21, 63):
        fwd = []
        for ticker, p in zip(reject_df['Ticker'], positions):
            j = p + horizon
            if p >= 0 and j < len(idx) and ticker in prices_ff.columns:
                p0 = prices_ff.iat[p, prices_ff.columns.get_loc(ticker)]
                p1 = prices_ff.iat[j, prices_ff.columns.get_loc(ticker)]
                fwd.append(round((p1 / p0 - 1) * 100, 2)
                           if (pd.notna(p0) and p0 > 0 and pd.notna(p1)) else np.nan)
            else:
                fwd.append(np.nan)
        reject_df[f'Fwd_Return_{horizon}d'] = fwd
    return reject_df


# ══════════════════════════════════════════════════════════════════════════════
# DATA LOADER  (identical to batch v2.4 — same data source)
# ══════════════════════════════════════════════════════════════════════════════

def load_data(folder_path):
    """Loads OHLCV CSVs from folder_path; entries/exits fill at next-day open, falling back to prev-close if no open column exists."""
    import glob
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

            def _clean_price(s):
                s = _clean(s)
                return s.mask(s <= 0)

            if 'close' in df.columns:
                price_list.append(_clean_price(df['close'].rename(symbol)))
            else:
                print(f"Warning: 'close' missing in {filename}")

            if 'volume' in df.columns:
                volume_list.append(_clean(df['volume'].rename(symbol)))

            if 'high' in df.columns:
                high_list.append(_clean_price(df['high'].rename(symbol)))

            if 'low' in df.columns:
                low_list.append(_clean_price(df['low'].rename(symbol)))

            if 'open' in df.columns:
                open_list.append(_clean_price(df['open'].rename(symbol)))

        except Exception as e:
            print(f"Error loading {filename}: {e}")

    if not price_list:
        return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(),
                pd.DataFrame(), pd.DataFrame())

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


def mask_corporate_actions(prices, highs, lows, opens, lower=-0.40, upper=3.00):
    """NaN out OHLC on any day a stock's close-to-close move falls outside [lower, upper] --
    catches un-adjusted splits/bonuses and raw data glitches (e.g. a zero-volume placeholder
    row) before they corrupt returns or signals. Same convention as the research bake-off's
    `sr_panel.mask_corporate_actions` (1-day move < -40% or > +300%)."""
    daily_ret = prices.pct_change(fill_method=None)
    bad = (daily_ret < lower) | (daily_ret > upper)
    n_bad = int(bad.to_numpy().sum())
    print(f"[Data] Corporate-action mask: {n_bad} (ticker, day) cells with a 1-day move "
          f"outside [{lower:+.0%}, {upper:+.0%}] -- masked to NaN")

    prices = prices.mask(bad)
    if not highs.empty: highs = highs.mask(bad.reindex(columns=highs.columns, fill_value=False))
    if not lows.empty:  lows  = lows.mask(bad.reindex(columns=lows.columns, fill_value=False))
    if not opens.empty: opens = opens.mask(bad.reindex(columns=opens.columns, fill_value=False))
    return prices, highs, lows, opens


def build_benchmark(prices):
    """Equal-weight benchmark; skipna avoids diluting returns toward zero before most tickers have listed (data starts 2001 with <500 names)."""
    return (1 + prices.pct_change(fill_method=None)
                                .clip(-0.5, 0.5)
                                .mean(axis=1, skipna=True)
                                .fillna(0.0)).cumprod()


# ══════════════════════════════════════════════════════════════════════════════
# BACKTEST LOGGING HELPERS  (signal-month / entry-context / regime lookups)
# ══════════════════════════════════════════════════════════════════════════════

def _signal_month_for(strategy, date):
    """Last factor month-end strictly BEFORE `date` -- the month-end whose signal is tradable on `date` (positions are shifted 1 trading day)."""
    if strategy.factors is None or strategy.factors.empty:
        return None
    idx = strategy.factors.index
    pos = idx.searchsorted(date, side='left')
    return idx[pos - 1] if pos > 0 else None


def _entry_context(strategy, date, ticker):
    """Rank / composite score / per-leg scores / signal age at the signal month-end driving an entry (or reject) on `date`."""
    sig = _signal_month_for(strategy, date)
    rank = score = age = np.nan
    leg_scores = {L: np.nan for L in strategy.components}
    if sig is not None:
        if strategy.all_ranks is not None and ticker in strategy.all_ranks.columns:
            rank = strategy.all_ranks.at[sig, ticker]
        if ticker in strategy.factors.columns:
            score = strategy.factors.at[sig, ticker]
        for L in strategy.components:
            leg = strategy.factor_legs.get(L)
            if leg is not None and ticker in leg.columns:
                leg_scores[L] = leg.at[sig, ticker]
        if (strategy._signal_age is not None and sig in strategy._signal_age.index
                and ticker in strategy._signal_age.columns):
            age = strategy._signal_age.at[sig, ticker]
    return sig, rank, score, leg_scores, age


def _regime_at(strategy, date):
    if strategy._regime_daily is not None and date in strategy._regime_daily.index:
        return strategy._regime_daily.loc[date]
    return ''


def _log_reject(strategy, date, ticker, reason):
    """One reject row per (ticker, signal-month, reason) -- the monthly signal re-requests an entry every day, so dedupe to avoid spam."""
    sig = _signal_month_for(strategy, date)
    key = (ticker, sig if sig is not None else date, reason)
    if key in strategy._reject_seen:
        return
    strategy._reject_seen.add(key)
    _, rank, score, _, _ = _entry_context(strategy, date, ticker)
    strategy.reject_log.append({
        'Date'          : date,
        'Ticker'        : ticker,
        'Rank'          : round(float(rank), 1)  if pd.notna(rank)  else np.nan,
        'Score'         : round(float(score), 4) if pd.notna(score) else np.nan,
        'Reject_Reason' : reason,
    })


def _record_closed_trade(strategy, ticker, holding, exit_date,
                          exit_price, fill_price, exit_reason,
                          stop_price_at_exit, exit_detail='', exit_idx=None):
    """Append one closed-trade record to strategy.position_metadata (called for every exit: STOP_HIT, REBALANCE, CRASH_GUARD, END_OF_PERIOD)."""
    entry_price  = holding.get('entry_price', np.nan)
    entry_date   = holding.get('entry_date',  pd.NaT)
    peak_price   = holding.get('peak_price',  np.nan)
    stop_pct     = holding.get('stop_pct',     np.nan)
    atr_at_entry = holding.get('atr_at_entry', np.nan)
    weight       = holding.get('weight',        0.0)
    min_price    = holding.get('min_price',     entry_price)
    max_price    = holding.get('max_price',     entry_price)

    # Actual fill: for stop exits use fill_price; for others use exit_price
    _stop_reasons = {'STOP_HIT', 'CRASH_GUARD'}
    actual_fill = fill_price if exit_reason in _stop_reasons else exit_price

    mae_pct = ((min_price / entry_price) - 1) * 100 if (entry_price and entry_price > 0) else np.nan
    mfe_pct = ((max_price / entry_price) - 1) * 100 if (entry_price and entry_price > 0) else np.nan

    # ── Exit_Detail resolution for non-stop exits ─────────────────────────
    if exit_reason == 'CRASH_GUARD':
        exit_detail = 'BENCH_PANIC'
    elif exit_reason == 'END_OF_PERIOD':
        exit_detail = 'END_OF_PERIOD'
    elif exit_reason == 'PARTIAL_EXIT':
        exit_detail = 'CRYSTALLISE'
    elif exit_reason == 'TIME_STOP':
        exit_detail = 'TIME_STOP'
    elif exit_reason == 'REBALANCE':
        # RANK_DECAY: still has a valid factor + positive abs-mom, but rank slid past the exit threshold. SIGNAL_DROP: fell out of the universe filter or failed the abs-momentum gate.
        sig = _signal_month_for(strategy, exit_date)
        exit_detail = 'SIGNAL_DROP'
        if sig is not None and ticker in strategy.factors.columns:
            _f = strategy.factors.at[sig, ticker]
            _m = (strategy.momentum_returns.at[sig, ticker]
                  if (sig in strategy.momentum_returns.index
                      and ticker in strategy.momentum_returns.columns) else np.nan)
            if pd.notna(_f) and pd.notna(_m) and _m > 0:
                exit_detail = 'RANK_DECAY'

    # ── Exit-side context ─────────────────────────────────────────────────
    sig_exit     = _signal_month_for(strategy, exit_date)
    rank_at_exit = np.nan
    if sig_exit is not None and strategy.all_ranks is not None \
            and ticker in strategy.all_ranks.columns:
        rank_at_exit = strategy.all_ranks.at[sig_exit, ticker]

    entry_idx = holding.get('entry_idx', None)
    trading_days_held = (int(exit_idx - entry_idx)
                         if (exit_idx is not None and entry_idx is not None)
                         else np.nan)

    leg_scores = holding.get('leg_scores', {}) or {}

    rec = {
        'Ticker'            : ticker,
        'Entry_Date'        : entry_date,
        'Entry_Price'       : round(entry_price,       4) if pd.notna(entry_price)       else np.nan,
        'Exit_Date'         : exit_date,
        'Exit_Price'        : round(actual_fill,       4) if pd.notna(actual_fill)       else np.nan,
        'Close_At_Exit'     : round(exit_price,        4) if pd.notna(exit_price)        else np.nan,
        'Peak_Price'        : round(peak_price,        4) if pd.notna(peak_price)        else np.nan,
        'Stop_Price_At_Exit': round(stop_price_at_exit,4) if pd.notna(stop_price_at_exit) else np.nan,
        'Stop_Pct'          : round(stop_pct * 100,    2) if pd.notna(stop_pct)          else np.nan,
        'ATR_At_Entry'      : round(atr_at_entry,      4) if pd.notna(atr_at_entry)      else np.nan,
        'Exit_Reason'       : exit_reason,
        'Exit_Detail'       : exit_detail,
        'Entry_Reason'      : holding.get('entry_reason', ''),
        'Rank_At_Entry'     : holding.get('rank_at_entry', np.nan),
        'Rank_At_Exit'      : round(float(rank_at_exit), 1) if pd.notna(rank_at_exit) else np.nan,
        'Score_At_Entry'    : holding.get('score_at_entry', np.nan),
        'Regime_At_Entry'   : holding.get('regime_at_entry', ''),
        'Regime_At_Exit'    : _regime_at(strategy, exit_date),
        'Signal_Age_Months' : holding.get('signal_age_months', np.nan),
        'Trading_Days_Held' : trading_days_held,
        'Weight'            : round(weight,             6),
        'MAE_Pct'           : round(mae_pct,            2) if pd.notna(mae_pct)           else np.nan,
        'MFE_Pct'           : round(mfe_pct,            2) if pd.notna(mfe_pct)           else np.nan,
    }
    for L in strategy.components:
        _v = leg_scores.get(L, np.nan)
        rec[f'{L}_At_Entry'] = round(float(_v), 4) if pd.notna(_v) else np.nan

    strategy.position_metadata.append(rec)


# ══════════════════════════════════════════════════════════════════════════════
# EVENT-DRIVEN BACKTEST
# ══════════════════════════════════════════════════════════════════════════════

def _run_backtest_core(
    strategy,
    initial_capital:   float,
    transaction_cost:  float,
    risk_free_rate:    float,
    use_ltp_filter:    bool  = False,
    max_entry_gap_pct: float = 0.02,
    label:             str   = "Event-Driven",
) -> dict:
    """Core event-driven loop shared by backtest_event_driven()/live_backtest(); Vol Targeting and Correlation Guard run in-loop over past data only. use_ltp_filter (live_backtest only) skips new entries that gapped up more than max_entry_gap_pct."""
    if strategy.positions is None:
        raise ValueError("Call get_positions() first.")

    print("\n" + "=" * 65)
    print(f"[CSM Value (Earnings-Yield) Momentum]  {label} Backtest starting")
    print("=" * 65)
    print(f"  Capital        : ₹{initial_capital:,.0f}")
    print(f"  Txn cost       : {transaction_cost*100:.3f}% one-way")
    print(f"  RFR            : {risk_free_rate*100:.1f}% p.a.")
    print(f"  Stop (entry)   : −{strategy.hard_stop_from_entry*100:.0f}%  [Layer 2]")
    print(f"  Stop (peak)    : −{strategy.hard_stop_from_peak*100:.0f}%  [Layer 3]")
    print(f"  Chandelier     : {'OFF -- signal-only exit, hard stops are the only backstop' if not strategy.use_chandelier else f'peak − {strategy.atr_multiplier}×ATR(capped) [Layer 1]'}")
    print(f"  Crash Guard    : {'ON' if strategy.use_crash_guard else 'OFF'}"
          f"  cooldown={strategy.crash_guard_cooldown} days")
    print(f"  Corr Guard     : threshold={strategy.corr_guard_threshold}")
    print(f"  Stop cooldown  : {strategy.stop_cooldown_days} days per ticker after STOP_HIT")
    print(f"  Min hold       : {strategy.min_hold_days} "
          f"{'TRADING' if strategy.min_hold_trading else 'calendar'} days before stop can fire")
    print(f"  ATR mult       : {strategy.atr_multiplier} normal / {strategy.atr_multiplier_high_vol} high-vol")
    print(f"  Vol target     : {strategy.vol_target*100:.0f}%  (de-leverage only)")
    if use_ltp_filter:
        print(f"  LTP filter     : skip entry if open > prev_close × {1+max_entry_gap_pct:.3f}")
    _v34 = []
    if strategy.use_liquid_mf:                       _v34.append(f"MF@{strategy.liquid_mf_annual_rate*100:.1f}%")
    if strategy.cooldown_mode != 'flat':             _v34.append(f"cooldown={strategy.cooldown_mode}")
    if strategy.leverage_bear != 1.0 or strategy.leverage_bull != 1.0:
                                                 _v34.append(f"lev={strategy.leverage_bull}/{strategy.leverage_bear}")
    if strategy.rebalance_exit_buffer_months > 0:    _v34.append(f"rebbuf={strategy.rebalance_exit_buffer_months}m")
    if strategy.stop_fill_mode != 'stop':            _v34.append(f"fill={strategy.stop_fill_mode}")
    if strategy.use_crystallisation:                 _v34.append(f"cryst@{strategy.crystallise_trigger:.0%}/{strategy.crystallise_fraction:.0%}")
    if strategy.use_staleness_gate:                  _v34.append(f"stale>={strategy.stale_threshold_months}m")
    if strategy.use_time_stop:                       _v34.append(f"tstop={strategy.time_stop_days}d/{strategy.time_stop_min_gain:.0%}")
    if strategy.use_cg_quality_gate:                 _v34.append("cg_quality")
    print(f"  V3/V4 features : {', '.join(_v34) if _v34 else 'NONE (baseline)'}")
    print("=" * 65)

    # ── Pre-compute static arrays ─────────────────────────────────────────
    prices_ff  = strategy._prices_ff
    opens_ff   = strategy._opens_ff
    open_proxy = strategy._open_proxy          # prev-close; used for LTP gap check
    highs_ff   = strategy.highs.ffill() if not strategy.highs.empty else prices_ff.copy()
    lows_ff    = strategy.lows.ffill()  if not strategy.lows.empty  else prices_ff.copy()

    # Circuit breaker: True on bars where high == low (stock locked at price limit)
    if not strategy.highs.empty and not strategy.lows.empty:
        is_circuit_ff = (highs_ff == lows_ff)
    else:
        is_circuit_ff = pd.DataFrame(False, index=prices_ff.index, columns=prices_ff.columns)

    # All daily returns (needed for rolling vol/corr computations)
    _dr_all = strategy.prices.pct_change(fill_method=None).fillna(0.0)

    # ── Panic / high-vol regime flags ─────────────────────────────────────
    if strategy.benchmark is not None and strategy.use_crash_guard:
        if strategy._panic_threshold_series is not None:
            bvol_daily  = strategy._bvol_daily.reindex(strategy.prices.index).ffill()
            _expand_thr = strategy._panic_threshold_series.reindex(strategy.prices.index).ffill()
            is_panic    = (bvol_daily > _expand_thr).fillna(False)
        else:
            is_panic = pd.Series(False, index=strategy.prices.index)
    else:
        is_panic = pd.Series(False, index=strategy.prices.index)

    if strategy.benchmark is not None and strategy._panic_threshold_series is not None:
        _bench_vol_75 = strategy._bvol_daily.reindex(strategy.prices.index).ffill()
        _expand_75 = (
            _bench_vol_75.expanding(min_periods=63).quantile(0.75).shift(1).ffill()
        )
        is_high_vol = (_bench_vol_75 > _expand_75).fillna(False)
    else:
        is_high_vol = pd.Series(False, index=strategy.prices.index)

    # ── Daily regime label series (logging v1: BULL/BEAR/HIGH_VOL/PANIC) ─
    if strategy.benchmark is not None:
        _b    = strategy.benchmark.reindex(strategy.prices.index).ffill()
        _bsma = _b.rolling(200, min_periods=150).mean()
        _bear = (_b.shift(1) < _bsma.shift(1)).fillna(False)
        # post-Crash-Guard re-entry quality gate (bench > EMA20)
        _ema20       = _b.ewm(span=20, adjust=False).mean()
        _above_ema20 = (_b.shift(1) > _ema20.shift(1)).fillna(False)
    else:
        _bear        = pd.Series(False, index=strategy.prices.index)
        _above_ema20 = pd.Series(True,  index=strategy.prices.index)

    # Monthly panic-leverage throttle: independent of Crash Guard, checked
    # once per month and held via ffill, for vol stretches that never spike
    # enough on any single day to trip Crash Guard's own daily threshold.
    if (strategy.benchmark is not None and strategy._panic_threshold_series is not None
            and strategy._bench_vol_monthly is not None):
        _monthly_thr   = strategy._panic_threshold_series.reindex(
            strategy._bench_vol_monthly.index).ffill()
        _monthly_panic = (strategy._bench_vol_monthly > _monthly_thr).fillna(False)
        _is_panic_lev  = _monthly_panic.reindex(strategy.prices.index, method='ffill').fillna(False)
    else:
        _is_panic_lev = pd.Series(False, index=strategy.prices.index)
    _regime_vals = np.where(is_panic.values,    'PANIC',
                   np.where(is_high_vol.values, 'HIGH_VOL',
                   np.where(_bear.values,       'BEAR', 'BULL')))
    strategy._regime_daily = pd.Series(_regime_vals, index=strategy.prices.index)

    # Monthly signal → daily (shifted 1 trading day so T signal trades T+1)
    monthly_signal = (
        strategy.positions
        .reindex(strategy.prices.index, method='ffill')
        .shift(1)
        .fillna(0.0)
    )

    # ── Mutable state ─────────────────────────────────────────────────────
    active_holdings:        dict = {}
    stop_cooldown_tickers:  dict = {}
    _last_stop_date:        dict = {}   # ticker → last STOP/CG exit date (entry-reason tag)
    executed_weights_list        = []
    strategy.position_metadata       = []
    strategy.reject_log              = []
    strategy._reject_seen            = set()
    strategy._backtest_initial_capital = initial_capital

    # atr_prev_day=True: day i uses day i-1's ATR instead of same-day
    if strategy.atr is not None:
        _atr_src  = strategy.atr.shift(1) if strategy.atr_prev_day else strategy.atr
        atr_daily = _atr_src.reindex(strategy.prices.index)
    else:
        atr_daily = None

    n_stop, n_crash, n_rebalance = 0, 0, 0
    cg_cooldown_remaining: int   = 0
    in_cg_recovery: bool         = False   # post-Crash-Guard quality gate state
    _pending_stop:  dict         = {}      # stop_fill_mode='next_open'
    _drop_pending:  dict         = {}      # rebalance exit buffer
    _crystallised:  set          = set()   # positions running at reduced weight
    daily_rfr = (1.0 + risk_free_rate) ** (1.0 / 252) - 1.0
    # idle cash earns liquid-MF rate when enabled (else RFR)
    daily_cash_rate = ((1.0 + strategy.liquid_mf_annual_rate) ** (1.0 / 252) - 1.0
                       if strategy.use_liquid_mf else daily_rfr)

    # Rolling buffers for in-loop Vol Targeting and Corr Guard.
    _port_ret_buf:  list = []   # past gross portfolio returns (position legs only)
    _weight_buf:    list = []   # list of pd.Series (executed weights, past bars)
    VOL_WIN  = 21               # rolling window for vol estimate (annualised)
    CORR_WIN = 21               # rolling window for corr guard ratio

    # scale-update throttling state (only used when
    # strategy.use_trade_deadband=True; otherwise raw scale applies daily)
    _last_applied_scale:    float = 1.0
    _last_scale_update_idx: int   = 0

    # Daily diagnostics (logging v1)
    _vol_scale_list, _corr_scale_list, _n_cooldown_list = [], [], []

    # ── Main daily loop ───────────────────────────────────────────────────
    for i, date in enumerate(strategy.prices.index):

        # First bar: seed buffers with zeros, nothing to do
        if i == 0:
            _zero_w = pd.Series(0.0, index=strategy.prices.columns)
            executed_weights_list.append(_zero_w)
            _port_ret_buf.append(0.0)
            _weight_buf.append(_zero_w)
            _vol_scale_list.append(1.0)
            _corr_scale_list.append(1.0)
            _n_cooldown_list.append(0)
            continue

        prev_weights   = executed_weights_list[i - 1]
        prev_held      = set(prev_weights.index[prev_weights > 1e-6])
        target_weights = monthly_signal.iloc[i].copy()
        exited_today: set = set()

        # ── STEP C: Crash Guard ───────────────────────────────────────────
        in_panic = is_panic.iloc[i]
        if strategy.use_crash_guard and in_panic:
            for stock in prev_held:
                _close = float(prices_ff.at[date, stock])
                _fill  = float(opens_ff.at[date, stock])
                if pd.isna(_fill) or _fill <= 0:
                    _fill = _close
                _h = active_holdings.get(stock, {})
                _record_closed_trade(
                    strategy,
                    ticker             = stock,
                    holding            = _h,
                    exit_date          = date,
                    exit_price         = _close,
                    fill_price         = _fill,
                    exit_reason        = 'CRASH_GUARD',
                    stop_price_at_exit = _h.get('atr_stop', np.nan),
                    exit_idx           = i,
                )
                exited_today.add(stock)
                n_crash += 1
            active_holdings.clear()
            target_weights[:] = 0.0
            cg_cooldown_remaining = strategy.crash_guard_cooldown
            in_cg_recovery = True
            _pending_stop.clear()
            _drop_pending.clear()
            _crystallised.clear()
            stop_cooldown_tickers.clear()
            for _cg_stock in exited_today:
                # CG cooldown stays flat: loss size reflects the market, not the stock
                stop_cooldown_tickers[_cg_stock] = (date, strategy.stop_cooldown_days)
                _last_stop_date[_cg_stock]       = date
            _zero_w = target_weights.copy()
            executed_weights_list.append(_zero_w)
            _port_ret_buf.append(0.0)
            _weight_buf.append(_zero_w)
            _vol_scale_list.append(1.0)
            _corr_scale_list.append(1.0)
            _n_cooldown_list.append(len(stop_cooldown_tickers))
            continue

        # ── Crash Guard cooldown ──────────────────────────────────────────
        if cg_cooldown_remaining > 0:
            cg_cooldown_remaining -= 1
            for stock in list(target_weights.index):
                if stock not in prev_held and target_weights[stock] > 1e-6:
                    target_weights[stock] = 0.0
                    _log_reject(strategy, date, stock, 'CG_COOLDOWN')
        elif in_cg_recovery:
            # after the time cooldown, still require benchmark
            # quality (bench > EMA20) before accepting new entries.
            if strategy.use_cg_quality_gate and not bool(_above_ema20.iloc[i]):
                for stock in list(target_weights.index):
                    if stock not in prev_held and target_weights[stock] > 1e-6:
                        target_weights[stock] = 0.0
                        _log_reject(strategy, date, stock, 'CG_QUALITY')
            else:
                in_cg_recovery = False

        # ── STEP E0: pending next-open stop fills (stop_fill_mode='next_open')
        # Yesterday's breach exits at today's open, modelling live trading without a resting stop order -- the gap vs 'stop' mode quantifies the value of the limit-order mechanism.
        if strategy.stop_fill_mode == 'next_open' and _pending_stop:
            for stock in list(_pending_stop.keys()):
                if stock in exited_today or stock not in active_holdings:
                    del _pending_stop[stock]
                    continue
                if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                    continue   # locked — defer fill another day
                _stop_lvl, _po_detail = _pending_stop.pop(stock)
                _po_close = float(prices_ff.at[date, stock])
                _po_fill  = float(opens_ff.at[date, stock])
                if pd.isna(_po_fill) or _po_fill <= 0:
                    _po_fill = _po_close
                _po_entry = active_holdings[stock].get('entry_price', np.nan)
                _record_closed_trade(
                    strategy,
                    ticker             = stock,
                    holding            = active_holdings[stock],
                    exit_date          = date,
                    exit_price         = _po_close,
                    fill_price         = _po_fill,
                    exit_reason        = 'STOP_HIT',
                    stop_price_at_exit = _stop_lvl,
                    exit_detail        = _po_detail,
                    exit_idx           = i,
                )
                del active_holdings[stock]
                target_weights[stock] = 0.0
                exited_today.add(stock)
                n_stop += 1
                _po_pnl = ((_po_fill / _po_entry) - 1) * 100 \
                          if (pd.notna(_po_entry) and _po_entry > 0) else np.nan
                _cd = strategy._cooldown_days_for(_po_pnl)
                if _cd > 0:
                    stop_cooldown_tickers[stock] = (date, _cd)
                _last_stop_date[stock] = date
                _crystallised.discard(stock)

        # ── STEP E: Daily stop check ──────────────────────────────────────
        for stock in prev_held:
            if stock in exited_today or stock not in active_holdings:
                continue

            today_close = float(prices_ff.at[date, stock])
            today_low   = float(lows_ff.at[date, stock])
            today_high  = float(highs_ff.at[date, stock])
            today_open  = float(opens_ff.at[date, stock])
            if pd.isna(today_open) or today_open <= 0:
                today_open = float(open_proxy.at[date, stock])

            if pd.isna(today_close) or today_close <= 0:
                continue

            curr_atr = np.nan
            if atr_daily is not None and stock in atr_daily.columns:
                curr_atr = float(atr_daily.at[date, stock])
            if pd.isna(curr_atr) or curr_atr <= 0:
                curr_atr = today_close * 0.02

            # min-hold in TRADING days (loop index difference); min_hold_trading=False = batch calendar days.
            if strategy.min_hold_trading:
                _entry_idx = active_holdings[stock].get('entry_idx', i)
                _bars_held = i - _entry_idx
            else:
                _entry_dt  = active_holdings[stock].get('entry_date', date)
                _bars_held = (date - _entry_dt).days

            should_exit, fill_px, stop_lvl, updated_h, _detail = strategy._check_stop_exit(
                stock, today_close, today_low, curr_atr, today_open,
                active_holdings[stock], curr_high=today_high,
                high_vol=bool(is_high_vol.iloc[i]),
            )
            if _bars_held < strategy.min_hold_days:
                should_exit = False

            # Circuit day: price locked at limit — no fills possible, defer to next bar
            if should_exit and stock in is_circuit_ff.columns \
                    and bool(is_circuit_ff.at[date, stock]):
                should_exit = False

            # next_open mode: don't fill today — queue for tomorrow's open
            if should_exit and strategy.stop_fill_mode == 'next_open':
                _pending_stop[stock] = (float(stop_lvl), _detail)
                should_exit = False

            if should_exit:
                _entry_px = active_holdings[stock].get('entry_price', np.nan)
                _record_closed_trade(
                    strategy,
                    ticker             = stock,
                    holding            = active_holdings[stock],
                    exit_date          = date,
                    exit_price         = today_close,
                    fill_price         = fill_px,
                    exit_reason        = 'STOP_HIT',
                    stop_price_at_exit = stop_lvl,
                    exit_detail        = _detail,
                    exit_idx           = i,
                )
                del active_holdings[stock]
                target_weights[stock] = 0.0
                exited_today.add(stock)
                n_stop += 1
                _pnl_stop = ((fill_px / _entry_px) - 1) * 100 \
                            if (pd.notna(_entry_px) and _entry_px > 0) else np.nan
                _cd_days = strategy._cooldown_days_for(_pnl_stop)
                if _cd_days > 0:
                    stop_cooldown_tickers[stock] = (date, _cd_days)
                _last_stop_date[stock] = date
                _crystallised.discard(stock)
            else:
                _low  = today_low  if (not pd.isna(today_low)  and today_low  > 0) else today_close
                _high = today_high if (not pd.isna(today_high) and today_high > 0) else today_close
                updated_h['min_price'] = min(updated_h.get('min_price', today_close), _low)
                updated_h['max_price'] = max(updated_h.get('max_price', today_close), _high)
                active_holdings[stock] = updated_h

                # ── profit crystallisation ───────────────────────
                if strategy.use_crystallisation and not updated_h.get('crystallised', False):
                    _entry_p = updated_h.get('entry_price', np.nan)
                    if (pd.notna(_entry_p) and _entry_p > 0
                            and (today_close / _entry_p - 1) >= strategy.crystallise_trigger):
                        _sold_h = dict(updated_h)
                        _sold_h['weight'] = (float(target_weights.get(stock, 0.0))
                                             * strategy.crystallise_fraction)
                        _record_closed_trade(
                            strategy,
                            ticker             = stock,
                            holding            = _sold_h,
                            exit_date          = date,
                            exit_price         = today_close,
                            fill_price         = today_close,
                            exit_reason        = 'PARTIAL_EXIT',
                            stop_price_at_exit = updated_h.get('atr_stop', np.nan),
                            exit_idx           = i,
                        )
                        updated_h['crystallised'] = True
                        # Remaining half: hard floor at breakeven
                        updated_h['atr_stop'] = max(updated_h.get('atr_stop', 0.0), _entry_p)
                        active_holdings[stock] = updated_h
                        _crystallised.add(stock)

                # ── time stop (dead-position recycler) ───────────
                if strategy.use_time_stop and stock in active_holdings:
                    _bars_ts = i - active_holdings[stock].get('entry_idx', i)
                    if _bars_ts >= strategy.time_stop_days:
                        _entry_p = active_holdings[stock].get('entry_price', np.nan)
                        _prev_c  = float(prices_ff.at[strategy.prices.index[i - 1], stock])
                        if (pd.notna(_entry_p) and _entry_p > 0 and _prev_c > 0
                                and (_prev_c / _entry_p - 1) < strategy.time_stop_min_gain):
                            _record_closed_trade(
                                strategy,
                                ticker             = stock,
                                holding            = active_holdings[stock],
                                exit_date          = date,
                                exit_price         = today_close,
                                fill_price         = today_close,
                                exit_reason        = 'TIME_STOP',
                                stop_price_at_exit = active_holdings[stock].get('atr_stop', np.nan),
                                exit_idx           = i,
                            )
                            del active_holdings[stock]
                            target_weights[stock] = 0.0
                            exited_today.add(stock)
                            _crystallised.discard(stock)

        # ── STEP F: Rebalance exits ───────────────────────────────────────
        current_held = set(target_weights.index[target_weights > 1e-6])
        # clear pending drops for stocks the signal wants again
        if strategy.rebalance_exit_buffer_months > 0 and _drop_pending:
            for _stk in list(_drop_pending):
                if _stk in current_held:
                    _drop_pending.pop(_stk)
        for stock in prev_held:
            if stock in current_held or stock in exited_today:
                continue
            # stop-only exits -- a position never leaves via rank-based REBALANCE; it holds at its last weight (slot stays occupied) until a stop / Crash Guard / time stop forces it out.
            if strategy.stop_only_exits and stock in active_holdings:
                target_weights[stock] = float(prev_weights.get(stock, 0.0))
                continue
            # Circuit day: can't sell — restore previous weight and defer to next bar
            if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                target_weights[stock] = float(prev_weights.get(stock, 0.0))
                continue
            # rebalance exit buffer -- first signal-month drop is deferred (position kept at previous weight, stops stay live); exit only when a NEWER signal month still drops it.
            if strategy.rebalance_exit_buffer_months > 0 and stock in active_holdings:
                _sig_now = _signal_month_for(strategy, date)
                _pend    = _drop_pending.get(stock)
                if _pend is None or _pend == _sig_now:
                    _drop_pending[stock] = _sig_now
                    target_weights[stock] = float(prev_weights.get(stock, 0.0))
                    continue
                _drop_pending.pop(stock, None)
            _close = float(prices_ff.at[date, stock])
            _fill  = float(opens_ff.at[date, stock])
            if pd.isna(_fill) or _fill <= 0:
                _fill = _close
            _h    = active_holdings.pop(stock, {})
            _crystallised.discard(stock)
            _record_closed_trade(
                strategy,
                ticker             = stock,
                holding            = _h,
                exit_date          = date,
                exit_price         = _close,
                fill_price         = _fill,
                exit_reason        = 'REBALANCE',
                stop_price_at_exit = _h.get('atr_stop', np.nan),
                exit_idx           = i,
            )
            exited_today.add(stock)
            n_rebalance += 1

        # ── STEP G: New entries ───────────────────────────────────────────
        for stock in list(current_held):
            if stock not in prev_held:
                if stock in exited_today:
                    target_weights[stock] = 0.0
                    continue

                # Per-ticker stop cooldown (flat or loss-scaled)
                if stock in stop_cooldown_tickers:
                    _cd_date, _cd_len = stop_cooldown_tickers[stock]
                    _gap = (date - _cd_date).days
                    if _gap < _cd_len:
                        target_weights[stock] = 0.0
                        _log_reject(strategy, date, stock, 'COOLDOWN')
                        continue
                    else:
                        del stop_cooldown_tickers[stock]

                # Circuit day: price locked, can't enter
                if stock in is_circuit_ff.columns and bool(is_circuit_ff.at[date, stock]):
                    target_weights[stock] = 0.0
                    _log_reject(strategy, date, stock, 'CIRCUIT_DAY')
                    continue

                _ep_open  = float(opens_ff.at[date, stock])
                _ep_close = float(prices_ff.at[date, stock])
                _ep = _ep_open if (_ep_open > 0 and not pd.isna(_ep_open)) else _ep_close

                # LTP gap filter (live_backtest only)
                if use_ltp_filter and max_entry_gap_pct > 0:
                    _prev_close = float(open_proxy.at[date, stock])   # prev-close
                    if (not pd.isna(_prev_close) and _prev_close > 0
                            and not pd.isna(_ep_open) and _ep_open > 0):
                        if (_ep_open / _prev_close) - 1.0 > max_entry_gap_pct:
                            target_weights[stock] = 0.0
                            _log_reject(strategy, date, stock, 'GAP_UP')
                            continue

                # Initial stop sizing
                _atr_entry = np.nan
                if atr_daily is not None and stock in atr_daily.columns:
                    _atr_entry = float(atr_daily.at[date, stock])
                if strategy.use_chandelier:
                    if not pd.isna(_atr_entry) and _atr_entry > 0:
                        raw_dist  = strategy.atr_multiplier * _atr_entry
                        stop_dist = float(np.clip(raw_dist, 0.03 * _ep, 0.30 * _ep))
                    else:
                        stop_dist = strategy.hard_stop_from_entry * _ep
                    initial_atr_stop = max(
                        _ep - stop_dist,
                        _ep * (1.0 - strategy.hard_stop_from_entry),
                        _ep * (1.0 - strategy.hard_stop_from_peak),
                    )
                else:
                    # use_chandelier=False: seed from hard stops only -- no ATR-distance term, or a calm-ATR name would still open at a tighter-than-intended stop despite the flag.
                    initial_atr_stop = max(
                        _ep * (1.0 - strategy.hard_stop_from_entry),
                        _ep * (1.0 - strategy.hard_stop_from_peak),
                    )

                # Entry context (logging v1 + V2 signal age)
                _, _rank_e, _score_e, _legs_e, _age_e = _entry_context(strategy, date, stock)

                # staleness gate -- block entries whose signal has been in the entry zone too long (end-stage momentum)
                if (strategy.use_staleness_gate and pd.notna(_age_e)
                        and _age_e >= strategy.stale_threshold_months):
                    target_weights[stock] = 0.0
                    _log_reject(strategy, date, stock, 'STALE_SIGNAL')
                    continue
                _entry_reason = 'NEW_SIGNAL'
                if stock in _last_stop_date and \
                        (date - _last_stop_date[stock]).days <= strategy.post_cooldown_window_days:
                    _entry_reason = 'POST_COOLDOWN'

                active_holdings[stock] = {
                    'entry_date'     : date,
                    'entry_idx'      : i,
                    'entry_price'    : _ep,
                    'peak_price'     : _ep,
                    'atr_stop'       : initial_atr_stop,
                    'stop_pct'       : (_ep - initial_atr_stop) / _ep,
                    'atr_at_entry'   : _atr_entry,
                    'weight'         : float(target_weights.get(stock, 0.0)),
                    'min_price'      : _ep,
                    'max_price'      : _ep,
                    'entry_reason'   : _entry_reason,
                    'rank_at_entry'  : round(float(_rank_e), 1)  if pd.notna(_rank_e)  else np.nan,
                    'score_at_entry' : round(float(_score_e), 4) if pd.notna(_score_e) else np.nan,
                    'leg_scores'     : _legs_e,
                    'regime_at_entry': strategy._regime_daily.iloc[i],
                    'signal_age_months': int(_age_e) if pd.notna(_age_e) else np.nan,
                }

        # ── STEP H: Sync weight into active_holdings ──────────────────────
        # crystallised positions run at (1 − fraction) of signal weight
        if strategy.use_crystallisation and _crystallised:
            for _ct in list(_crystallised):
                if target_weights.get(_ct, 0.0) > 1e-9:
                    target_weights[_ct] *= (1.0 - strategy.crystallise_fraction)
        # buffered holds may push gross weight above 1 — renormalize
        # so the buffer never creates implicit leverage
        if strategy.rebalance_exit_buffer_months > 0:
            _tw_sum = float(target_weights.sum())
            if _tw_sum > 1.0:
                target_weights = target_weights / _tw_sum
        current_held = set(target_weights.index[target_weights > 1e-6])
        for stock in current_held:
            if stock in active_holdings:
                active_holdings[stock]['weight'] = float(target_weights.get(stock, 0.0))
        for _stk in list(active_holdings.keys()):
            if _stk not in current_held:
                del active_holdings[_stk]
                _crystallised.discard(_stk)

        # ── STEP I: In-loop Vol Targeting & Corr Guard ────────────────────
        raw_weights = target_weights.copy()

        corr_scale = 1.0
        if len(_port_ret_buf) >= CORR_WIN:
            _pbuf   = np.array(_port_ret_buf[-CORR_WIN:])
            _p_vol  = float(_pbuf.std())         # portfolio std (daily)
            _pw     = _weight_buf[-1]             # previous day's weights (past)
            _w_sum  = float(_pw.sum())
            if _w_sum > 0 and _p_vol > 0:
                _hist_start = max(0, i - CORR_WIN)
                _s_std = _dr_all.iloc[_hist_start:i].std()   # per-stock std
                _avg_s_vol = float((_s_std * _pw).sum() / _w_sum)
                if _avg_s_vol > 0 and (_p_vol / _avg_s_vol) > strategy.corr_guard_threshold:
                    corr_scale = 0.5

        vol_scale = 1.0
        if len(_port_ret_buf) >= VOL_WIN:
            _win = _port_ret_buf[-63:] if len(_port_ret_buf) >= 63 else _port_ret_buf[-VOL_WIN:]
            _rv  = float(np.std(_win)) * np.sqrt(252)
            if _rv > 0:
                vol_scale = min(1.0, strategy.vol_target / _rv)

        # throttle how often the combined risk-scale (corr x vol)
        # actually changes, instead of applying a freshly recomputed value
        # every single day -- most of that daily jiggle carries no signal
        # and just charges transaction cost across every held name.
        _raw_combined_scale = corr_scale * vol_scale
        if strategy.use_trade_deadband:
            _days_since_update = i - _last_scale_update_idx
            _moved_enough = (abs(_raw_combined_scale - _last_applied_scale)
                              >= strategy.scale_update_move_pct)
            if _days_since_update >= strategy.scale_update_days or _moved_enough:
                _last_applied_scale    = _raw_combined_scale
                _last_scale_update_idx = i
            _combined_scale = _last_applied_scale
        else:
            _combined_scale = _raw_combined_scale

        # regime leverage: panic overwrites the bull-default base, bear then
        # tightens further via min() -- never loosens a panic cut
        _lev = strategy.leverage_panic if bool(_is_panic_lev.iloc[i]) else strategy.leverage_bull
        if bool(_bear.iloc[i]):
            _lev = min(_lev, strategy.leverage_bear)
        scaled_weights = raw_weights * (_combined_scale * _lev)

        # trade deadband -- a name held both yesterday and today
        # skips re-trading a weight change smaller than min_trade_pct (pure
        # cost saving; fresh entries and exits are never deadbanded, only
        # continuing-holding weight drift).
        if strategy.use_trade_deadband:
            _prev_exec = executed_weights_list[i - 1]
            _continuing = prev_held & current_held
            for _stk in _continuing:
                _prev_w = float(_prev_exec.get(_stk, 0.0))
                _new_w  = float(scaled_weights.get(_stk, 0.0))
                if abs(_new_w - _prev_w) < strategy.min_trade_pct:
                    scaled_weights[_stk] = _prev_w

        executed_weights_list.append(scaled_weights.copy())

        # Update rolling buffers (AFTER recording scaled_weights)
        _dr_today = _dr_all.loc[date]
        _gross_pos_ret = float((raw_weights * _dr_today).sum())
        _port_ret_buf.append(_gross_pos_ret)
        _weight_buf.append(scaled_weights.copy())

        _vol_scale_list.append(vol_scale)
        _corr_scale_list.append(corr_scale)
        _n_cooldown_list.append(len(stop_cooldown_tickers))

    # ── Close positions still open at end of period ───────────────────────
    _last_date = strategy.prices.index[-1]
    _last_i    = len(strategy.prices.index) - 1
    for stock, _h in active_holdings.items():
        _close = float(prices_ff.at[_last_date, stock])
        _fill  = float(opens_ff.at[_last_date, stock])
        if pd.isna(_fill) or _fill <= 0:
            _fill = _close
        _record_closed_trade(
            strategy,
            ticker             = stock,
            holding            = _h,
            exit_date          = _last_date,
            exit_price         = _close,
            fill_price         = _fill,
            exit_reason        = 'END_OF_PERIOD',
            stop_price_at_exit = _h.get('atr_stop', np.nan),
            exit_idx           = _last_i,
        )
    active_holdings.clear()
    strategy._prices_ff_backtest = prices_ff

    print(f"\n[{label}] Stop exits    : {n_stop}")
    print(f"[{label}] Crash Guard   : {n_crash}")
    print(f"[{label}] Rebal exits   : {n_rebalance}")
    print(f"[{label}] Entry rejects : {len(strategy.reject_log)}")

    # ── Build executed-weights DataFrame ──────────────────────────────────
    executed_weights = pd.DataFrame(
        executed_weights_list, index=strategy.prices.index
    ).fillna(0.0)

    # ── Stop-return capping (equity curve consistent with trade-log fills) ─
    _dr = _dr_all.copy()
    for meta in strategy.position_metadata:
        if meta['Exit_Reason'] not in {'STOP_HIT', 'CRASH_GUARD'}:
            continue
        ticker     = meta['Ticker']
        exit_date  = meta['Exit_Date']
        exit_price = meta['Exit_Price']
        if ticker not in _dr.columns or pd.isna(exit_price) or exit_price <= 0:
            continue
        if exit_date not in _dr.index:
            continue
        exit_loc = _dr.index.get_loc(exit_date)
        if exit_loc == 0:
            continue
        prev_close = strategy.prices.iloc[exit_loc - 1].get(ticker, np.nan)
        if pd.isna(prev_close) or prev_close <= 0:
            continue
        capped_ret = (exit_price / prev_close) - 1.0
        raw_ret    = _dr.at[exit_date, ticker]
        if not pd.isna(raw_ret) and raw_ret < capped_ret:
            _dr.at[exit_date, ticker] = capped_ret

    # ── Portfolio returns & equity curve ──────────────────────────────────
    # Execution-faithful accounting (added in csm_value; the original line was `gross_eq_ret = (executed_weights * _dr).sum(axis=1)`):
    #  * a position bought at the OPEN of day i earns close_i / entry_fill - 1 on that day, not the full close-to-close return that includes the overnight gap it never owned;
    #  * a position sold at day j's fill (stop level, gap-down open, or rebalance open) keeps its previous weight on day j and earns exit_fill / close_{j-1} - 1: the original books the weight
    #    as 0 on the exit day, so the loss from the previous close to a stop fill (about -5% on average) was never charged (the 'stop-return capping' block above is dead code for that reason).
    _w_ret = executed_weights.copy()
    _dr_f  = _dr.copy()
    _pp = strategy._prices_ff_backtest
    if True:   # always computed so both bookings can be reported; EXECUTION_FAITHFUL_ACCOUNTING only chooses which one is the headline
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
    gross_eng_ret   = (executed_weights * _dr).sum(axis=1)        # the Elendel engine's own booking
    gross_faith_ret = (_w_ret * _dr_f).sum(axis=1)                # execution-faithful booking (see AUDIT.md)
    gross_eq_ret    = gross_faith_ret if EXECUTION_FAITHFUL_ACCOUNTING else gross_eng_ret
    total_w         = executed_weights.sum(axis=1)
    cash_w          = (1.0 - total_w).clip(lower=0.0)
    cash_ret        = cash_w * daily_cash_rate
    w_chg           = executed_weights.diff().abs().sum(axis=1)
    txn_cost        = w_chg * transaction_cost
    net_returns     = gross_eq_ret + cash_ret - txn_cost
    strategy._net_by_booking = {'engine': gross_eng_ret + cash_ret - txn_cost, 'faithful': gross_faith_ret + cash_ret - txn_cost}

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

    _rmax    = equity_curve.cummax()
    _dd      = (equity_curve / _rmax) - 1.0
    max_dd   = _dd.min()
    calmar   = cagr / abs(max_dd) if max_dd != 0 else 0.0

    _mret    = portfolio_value.resample('ME').last().pct_change().dropna()
    win_rate = (_mret > 0).mean()
    ann_turn = w_chg.sum() / n_years if n_years > 0 else 0.0
    _pos_diff_events = (strategy.positions.diff().abs() > 1e-4).sum(axis=1).sum()
    sig_turn = (_pos_diff_events / 2.0) / n_years if n_years > 0 else 0.0

    strategy.results = {
        'equity_curve'       : equity_curve,
        'portfolio_value'    : portfolio_value,
        'net_returns'        : net_returns,
        'executed_weights'   : executed_weights,
        'turnover'           : w_chg,
        'total_return'       : float(equity_curve.iloc[-1] - 1.0),
        'cagr'               : cagr,
        'sharpe'             : sharpe,
        'sortino'            : sortino,
        'calmar'             : calmar,
        'max_drawdown'       : max_dd,
        'ann_volatility'     : ann_vol,
        'win_rate'           : win_rate,
        'ann_turnover'       : ann_turn,
        'ann_signal_turnover': sig_turn,
        # Daily diagnostics for the value daily log
        'vol_scale'          : pd.Series(_vol_scale_list,  index=strategy.prices.index),
        'corr_scale'         : pd.Series(_corr_scale_list, index=strategy.prices.index),
        'regime'             : strategy._regime_daily.copy(),
        'n_cooldown_tickers' : pd.Series(_n_cooldown_list, index=strategy.prices.index),
    }

    print(f"\n[{label}] CAGR={cagr*100:.2f}%  "
          f"Sharpe={sharpe:.2f}  MaxDD={max_dd*100:.2f}%")
    return strategy.results


def backtest_event_driven(
    strategy,
    initial_capital  = 100_000.0,
    transaction_cost = 0.001,
    risk_free_rate   = 0.06,
):
    """Event-driven backtest -- all overlays applied inside the loop using past data only, no post-loop vectorised pass."""
    return _run_backtest_core(
        strategy,
        initial_capital   = initial_capital,
        transaction_cost  = transaction_cost,
        risk_free_rate    = risk_free_rate,
        use_ltp_filter    = False,
        max_entry_gap_pct = 0.0,
        label             = "Event-Driven",
    )


def live_backtest(
    strategy,
    initial_capital   = 100_000.0,
    transaction_cost  = 0.001,
    risk_free_rate    = 0.06,
    max_entry_gap_pct = 0.02,
):
    """Live-market replica of backtest_event_driven with an LTP gap filter; blocked gap-ups are logged to the reject log as GAP_UP."""
    return _run_backtest_core(
        strategy,
        initial_capital   = initial_capital,
        transaction_cost  = transaction_cost,
        risk_free_rate    = risk_free_rate,
        use_ltp_filter    = True,
        max_entry_gap_pct = max_entry_gap_pct,
        label             = "Live",
    )


# ══════════════════════════════════════════════════════════════════════════════
# TRADE / REJECT LOGS  (logging v1)
# ══════════════════════════════════════════════════════════════════════════════

def get_trade_log(strategy):
    """Build a trade-log DataFrame from strategy.position_metadata; call after backtest_event_driven() or live_backtest()."""
    if not strategy.position_metadata:
        print("Warning: No trade metadata. Run backtest() first.")
        return pd.DataFrame()

    equity_curve     = strategy.results['equity_curve']     if strategy.results else None
    executed_weights = strategy.results['executed_weights'] if strategy.results else None
    prices_ffill     = strategy.prices.ffill()

    rows = []
    for meta in strategy.position_metadata:
        ticker      = meta['Ticker']
        entry_date  = meta['Entry_Date']
        exit_date   = meta['Exit_Date']
        entry_price = meta['Entry_Price']
        exit_price  = meta['Exit_Price']   # fill price (stop or close)

        # Recover NaN exit via forward-fill
        if pd.isna(exit_price) and ticker in prices_ffill.columns:
            exit_price = (prices_ffill.at[exit_date, ticker]
                          if exit_date in prices_ffill.index
                          else prices_ffill[ticker].iloc[-1])

        # Read actual executed weight (first non-zero after entry_date)
        weight = meta['Weight']
        if executed_weights is not None and ticker in executed_weights.columns:
            ew_col  = executed_weights[ticker]
            window  = ew_col.loc[(ew_col.index > entry_date) & (ew_col.index <= exit_date)]
            nonzero = window[window > 1e-9]
            if not nonzero.empty:
                weight = float(nonzero.iloc[0])

        # Portfolio value on first execution day (T+1)
        port_val = np.nan
        if equity_curve is not None:
            future_idx = equity_curve.index[equity_curve.index > entry_date]
            if len(future_idx) > 0:
                port_val = float(equity_curve.loc[future_idx[0]])

        # Quantity and rupee P&L
        qty = np.nan
        if pd.notna(entry_price) and entry_price > 0 and pd.notna(port_val) and weight > 0:
            qty = (weight * port_val) / entry_price

        pnl_pct = ((exit_price / entry_price) - 1) * 100 \
                  if (pd.notna(entry_price) and entry_price > 0
                      and pd.notna(exit_price) and exit_price > 0) else np.nan

        pnl_abs = qty * (exit_price - entry_price) \
                  if (pd.notna(qty) and pd.notna(entry_price)
                      and pd.notna(exit_price)) else np.nan

        holding_days = max((exit_date - entry_date).days, 1) \
                       if pd.notna(entry_date) else np.nan

        row = {
            'Ticker'            : ticker,
            'Entry_Date'        : entry_date,
            'Entry_Price'       : entry_price,
            'Exit_Date'         : exit_date,
            'Exit_Price'        : round(exit_price,              4) if pd.notna(exit_price)              else np.nan,
            'Close_At_Exit'     : meta.get('Close_At_Exit',      np.nan),
            'Peak_Price'        : meta.get('Peak_Price',         np.nan),
            'Stop_Price_At_Exit': meta.get('Stop_Price_At_Exit', np.nan),
            'Stop_Pct'          : meta.get('Stop_Pct',           np.nan),
            'ATR_At_Entry'      : meta.get('ATR_At_Entry',       np.nan),
            'Entry_Reason'      : meta.get('Entry_Reason',       ''),
            'Exit_Reason'       : meta['Exit_Reason'],
            'Exit_Detail'       : meta.get('Exit_Detail',        ''),
            'Rank_At_Entry'     : meta.get('Rank_At_Entry',      np.nan),
            'Rank_At_Exit'      : meta.get('Rank_At_Exit',       np.nan),
            'Score_At_Entry'    : meta.get('Score_At_Entry',     np.nan),
            'Regime_At_Entry'   : meta.get('Regime_At_Entry',    ''),
            'Regime_At_Exit'    : meta.get('Regime_At_Exit',     ''),
            'Signal_Age_Months' : meta.get('Signal_Age_Months',  np.nan),
            'Weight'            : round(weight,                   6),
            'Quantity'          : round(qty,                      4) if pd.notna(qty)     else np.nan,
            'Position_Size'     : round(weight * port_val,        2) if (pd.notna(port_val) and weight > 0) else 0.0,
            'Portfolio Value'   : round(port_val, 2) if pd.notna(port_val) else np.nan,
            'PnL_Pct'           : round(pnl_pct,                  4) if pd.notna(pnl_pct) else np.nan,
            'PnL_Abs'           : round(pnl_abs,                  2) if pd.notna(pnl_abs) else np.nan,
            'Holding_Days'      : holding_days,
            'Trading_Days_Held' : meta.get('Trading_Days_Held',  np.nan),
            'MAE_Pct'           : meta.get('MAE_Pct',             np.nan),
            'MFE_Pct'           : meta.get('MFE_Pct',             np.nan),
        }
        for L in strategy.components:
            _col = f'{L}_At_Entry'
            row[_col] = meta.get(_col, np.nan)
        rows.append(row)

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values('Entry_Date').reset_index(drop=True)
        df.index += 1
        df.index.name = 'Trade_ID'

    wins   = (df['PnL_Pct'] > 0).sum()
    losses = (df['PnL_Pct'] < 0).sum()
    total  = len(df)
    if total > 0:
        print(f"[Trade Log] {total} trades | Wins: {wins} | Losses: {losses}"
              f" | Win Rate: {wins/total*100:.1f}%")
        print(f"[Trade Log] Worst trade: {df['PnL_Pct'].min():.2f}%"
              f"  Best trade: {df['PnL_Pct'].max():.2f}%")
        print(f"[Trade Log] Exit reasons: {df['Exit_Reason'].value_counts().to_dict()}")
        print(f"[Trade Log] Exit details: {df['Exit_Detail'].value_counts().to_dict()}")
    return df


def get_reject_log(strategy):
    """Reject log DataFrame: one row per blocked entry, deduped per (ticker, signal-month, reason); forward returns are filled by the runner/analysis script."""
    if not strategy.reject_log:
        return pd.DataFrame(columns=['Date', 'Ticker', 'Rank', 'Score', 'Reject_Reason'])
    df = pd.DataFrame(strategy.reject_log).sort_values('Date').reset_index(drop=True)
    return df


# ══════════════════════════════════════════════════════════════════════════════
# IC / ICIR  —  Information Coefficient Analysis
# ══════════════════════════════════════════════════════════════════════════════

def _newey_west_tstat(x, lag):
    """Newey-West-corrected t-stat for the mean of a series that may be serially correlated
    (e.g. an IC series sampled monthly from an h-month forward return, which overlaps its
    neighbours by h-1 months). Bartlett kernel, lag=0 reduces to the plain t-stat -- exactly
    right for a 1-month-forward IC series, where consecutive samples don't overlap at all.
    Same idea as the research docs' own NW-t column ("corrected for the fact that 63-day
    returns measured every month overlap")."""
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    n = len(x)
    if n < 2:
        return 0.0, 0.0
    mean   = x.mean()
    d      = x - mean
    gamma0 = float(np.sum(d * d)) / (n - 1)   # ddof=1, so lag=0 exactly matches a plain t-stat
    lag    = max(0, min(int(lag), n - 1))
    lrv    = gamma0
    for k in range(1, lag + 1):
        gamma_k = float(np.mean(d[k:] * d[:-k]))
        weight  = 1.0 - k / (lag + 1)
        lrv    += 2 * weight * gamma_k
    lrv = max(lrv, 1e-12)
    se  = float(np.sqrt(lrv / n))
    t   = float(mean / se) if se > 0 else 0.0
    return t, se


def calculate_ic(strategy, forward_periods: int = 1, method: str = 'spearman',
                 report_start: str = None,
                 per_component: bool = True) -> dict:
    """Filtered-universe IC/ICIR for the value composite factor (same methodology as batch v2.4); per-component IC covers each leg under the same universe-eligible mask."""
    from scipy import stats as _scipy_stats

    if strategy.factors is None:
        raise ValueError("Call calculate_factors() first.")

    monthly_prices = strategy.prices.ffill().resample('ME').last()
    fwd_ret = (monthly_prices
               .pct_change(forward_periods, fill_method=None)
               .shift(-forward_periods))

    corr_fn = (
        lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation
        if method == 'spearman'
        else _scipy_stats.pearsonr(x, y)[0]
    )

    # ── (A) Combined factor IC — universe-filtered cross-section ──────────
    ic_records = []
    for date in strategy.factors.index:
        if date not in fwd_ret.index:
            continue
        f      = strategy.factors.loc[date].dropna()
        r      = fwd_ret.loc[date].dropna()
        common = f.index.intersection(r.index)
        if len(common) < 5:
            continue
        ic_records.append({
            'Date'     : date,
            'IC'       : corr_fn(f[common].values, r[common].values),
            'N_stocks' : len(common),
        })

    ic_series = pd.DataFrame(ic_records).set_index('Date')['IC'].dropna()
    ic_rep    = ic_series.loc[report_start:] if report_start else ic_series
    n         = len(ic_rep)

    ic_mean = ic_rep.mean()
    ic_std  = ic_rep.std()
    icir    = ic_mean / ic_std if ic_std > 0 else 0.0
    pos_pct = (ic_rep > 0).mean()
    t_stat  = ic_mean / (ic_std / np.sqrt(n)) if (n > 0 and ic_std > 0) else 0.0
    # NW lag = forward_periods - 1: consecutive monthly samples of an h-month forward return
    # overlap by h-1 months. forward_periods=1 -> lag=0 -> nw_t_stat == t_stat exactly.
    nw_lag             = max(0, forward_periods - 1)
    nw_t_stat, nw_se   = _newey_west_tstat(ic_rep.values, nw_lag)

    # ── (B) Factor decay across multiple horizons ─────────────────────────
    decay = {}
    for h in [1, 3, 6, 12]:
        fwd_h     = monthly_prices.pct_change(h, fill_method=None).shift(-h)
        ic_h_list = []
        for date in strategy.factors.index:
            if date not in fwd_h.index:
                continue
            f      = strategy.factors.loc[date].dropna()
            r      = fwd_h.loc[date].dropna()
            common = f.index.intersection(r.index)
            if len(common) < 5:
                continue
            ic_h_list.append(corr_fn(f[common].values, r[common].values))
        _arr = np.array(ic_h_list)
        _m, _s = float(np.nanmean(_arr)), float(np.nanstd(_arr))
        _h_nw_t, _ = _newey_west_tstat(_arr, max(0, h - 1))
        decay[h] = {'ic_mean': _m, 'icir': _m / _s if _s > 0 else 0.0, 'nw_t_stat': _h_nw_t}

    # ── (C) Per-leg component IC (universe-filtered) ─────────────────────
    component_ic = {}
    if per_component and strategy._legs_unfiltered:
        idx       = strategy.factors.index
        _uni_mask = strategy.factors.notna()   # True for universe-eligible stocks

        for L in strategy.components:
            comp_df = strategy._legs_unfiltered[L].reindex(idx)
            _ic_c = []
            for date in idx:
                if date not in fwd_ret.index:
                    continue
                uni_stocks = _uni_mask.loc[date]
                uni_stocks = uni_stocks[uni_stocks].index
                f = comp_df.loc[date].reindex(uni_stocks).dropna()
                r = fwd_ret.loc[date].dropna()
                common = f.index.intersection(r.index)
                if len(common) < 5:
                    continue
                _ic_c.append(corr_fn(f[common].values, r[common].values))
            _arr = np.array(_ic_c)
            _m, _s = float(np.nanmean(_arr)), float(np.nanstd(_arr))
            component_ic[L] = {
                'ic_mean': _m,
                'ic_std' : _s,
                'icir'   : _m / _s if _s > 0 else 0.0,
                'pos_pct': float((_arr > 0).mean()) if len(_arr) else 0.0,
            }

    # ── Print report ─────────────────────────────────────────────────────
    total_factor_months = len(strategy.factors.index)
    print("\n" + "=" * 68)
    print(f" FILTERED-UNIVERSE IC / ICIR  —  CSM Value (Earnings-Yield) Momentum  "
          f"({method.upper()}, {forward_periods}m forward)")
    print("=" * 68)
    print(f"  Total factor months  : {total_factor_months}")
    print(f"  IC-computable months : {n}  (>= 5 stocks eligible)")
    print(f"  Excluded months      : {total_factor_months - n}  (bear market / warmup)")
    print(f"  ──────────────────────────────────────────────────────────")
    print(f"  IC Mean (factor)     : {ic_mean:+.4f}")
    print(f"  IC Std               : {ic_std:.4f}")
    print(f"  ICIR                 : {icir:+.3f}   (> 0.2 useful for top-{strategy.top_n} book)")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic (plain)  : {t_stat:+.2f}   (> 2.0 = statistically significant)")
    print(f"  t-statistic (NW,lag={nw_lag}): {nw_t_stat:+.2f}   (Newey-West-corrected for the "
          f"{forward_periods}m-forward IC series' {max(0, forward_periods-1)}-month sample overlap "
          f"-- the honest one when forward_periods>1)")
    print(f"\n  Factor Decay (IC across forward horizons, NW-t at each horizon's own lag=h-1):")
    print(f"  {'Horizon':>8}  {'IC Mean':>10}  {'ICIR':>8}  {'NW-t':>7}")
    if decay:
        peak_h = max(decay, key=lambda h: decay[h]['ic_mean'])
        for h, d in decay.items():
            tag = " ← peak (sweet spot)" if h == peak_h else ""
            print(f"  {h:>6}m  {d['ic_mean']:>+10.4f}  {d['icir']:>8.3f}  {d['nw_t_stat']:>+7.2f}{tag}")
    if component_ic:
        print(f"\n  Per-Leg IC (universe-filtered, {method}, {forward_periods}m):")
        print(f"  {'Component':<14}  {'IC Mean':>10}  {'ICIR':>8}  {'Hit%':>7}")
        for cname, d in component_ic.items():
            print(f"  {cname:<14}  {d['ic_mean']:>+10.4f}  "
                  f"{d['icir']:>8.3f}  {d['pos_pct']*100:>6.1f}%")
    print("=" * 68)

    return {
        'ic_series'       : ic_series,
        'ic_mean'         : ic_mean,
        'ic_std'          : ic_std,
        'icir'            : icir,
        'ic_positive_pct' : pos_pct,
        't_stat'          : t_stat,
        'nw_t_stat'       : nw_t_stat,
        'nw_lag'          : nw_lag,
        'factor_decay'    : decay,
        'component_ic'    : component_ic,
    }


def calculate_realized_ic(strategy, method: str = 'spearman',
                           report_start: str = None) -> dict:
    """Realized IC -- correlation between factor score at entry and trade PnL, grouped by entry month; measures intra-portfolio ranking quality."""
    from scipy import stats as _scipy_stats

    if not strategy.position_metadata:
        raise ValueError("No position_metadata — run backtest first.")
    if strategy.factors is None:
        raise ValueError("Call calculate_factors() first.")

    corr_fn = (
        lambda x, y: _scipy_stats.spearmanr(x, y, nan_policy='omit').correlation
        if method == 'spearman'
        else _scipy_stats.pearsonr(x, y)[0]
    )

    rows = []
    for meta in strategy.position_metadata:
        ep  = meta.get('Entry_Price', np.nan)
        xp  = meta.get('Exit_Price',  np.nan)
        if pd.isna(ep) or ep <= 0 or pd.isna(xp) or xp <= 0:
            continue
        rows.append({
            'Ticker'    : meta['Ticker'],
            'Entry_Date': pd.Timestamp(meta['Entry_Date']),
            'PnL_Pct'   : (xp / ep - 1) * 100.0,
        })
    if not rows:
        print("[Realized IC] No usable trades in position_metadata.")
        return {}

    trades = pd.DataFrame(rows)
    if report_start:
        trades = trades[trades['Entry_Date'] >= pd.Timestamp(report_start)]

    factor_idx = strategy.factors.index
    def _last_me(d):
        valid = factor_idx[factor_idx <= d]
        return valid[-1] if len(valid) > 0 else pd.NaT

    trades['Entry_Month'] = trades['Entry_Date'].apply(_last_me)
    trades = trades.dropna(subset=['Entry_Month'])

    ic_records = []
    min_trades = 2

    for month, grp in trades.groupby('Entry_Month'):
        if len(grp) < min_trades:
            continue
        if month not in factor_idx:
            continue
        factor_row = strategy.factors.loc[month]
        scores, returns = [], []
        for _, row in grp.iterrows():
            ticker = row['Ticker']
            if ticker in factor_row.index and not pd.isna(factor_row[ticker]):
                scores.append(factor_row[ticker])
                returns.append(row['PnL_Pct'])
        if len(scores) < min_trades:
            continue
        ic_records.append({
            'Date'    : month,
            'IC'      : corr_fn(np.array(scores), np.array(returns)),
            'N_trades': len(scores),
        })

    if not ic_records:
        print("[Realized IC] Not enough monthly groups (need >= 2 entries with factor scores).")
        return {}

    ric_df     = pd.DataFrame(ic_records).set_index('Date')
    ric_series = ric_df['IC'].dropna()
    n          = len(ric_series)
    n_trades   = int(ric_df['N_trades'].sum())

    ric_mean = ric_series.mean()
    ric_std  = ric_series.std()
    ricir    = ric_mean / ric_std if ric_std > 0 else 0.0
    pos_pct  = (ric_series > 0).mean()
    t_stat   = ric_mean / (ric_std / np.sqrt(n)) if (n > 0 and ric_std > 0) else 0.0

    print("\n" + "=" * 68)
    print(f" REALIZED IC / ICIR  —  CSM Value (Earnings-Yield) Momentum  ({method.upper()})")
    print("=" * 68)
    print(f"  Months with >= {min_trades} entries : {n}")
    print(f"  Total trades used    : {n_trades}")
    print(f"  Avg trades / month   : {n_trades/n:.1f}")
    print(f"  IC Mean (Realized)   : {ric_mean:+.4f}   (> 0.05 meaningful)")
    print(f"  IC Std               : {ric_std:.4f}")
    print(f"  ICIR (Realized)      : {ricir:+.3f}   (> 0.2 usable for top-{strategy.top_n})")
    print(f"  IC > 0 hit rate      : {pos_pct*100:.1f}%")
    print(f"  t-statistic          : {t_stat:+.2f}   (> 2.0 = significant)")
    print("=" * 68)

    return {
        'realized_ic_series' : ric_series,
        'ic_mean'            : ric_mean,
        'ic_std'             : ric_std,
        'icir'               : ricir,
        'ic_positive_pct'    : pos_pct,
        't_stat'             : t_stat,
        'n_months'           : n,
        'n_trades'           : n_trades,
    }


def plot_ic(ic_results: dict, filename: str = 'csm_value_factor_ic.png'):
    """Three/four-panel IC chart (monthly IC, cumulative IC, decay, per-leg)."""
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt

    ic_s     = ic_results.get('ic_series', pd.Series(dtype=float))
    ic_roll  = ic_s.rolling(12).mean()
    decay    = ic_results.get('factor_decay', {})
    comp_ic  = ic_results.get('component_ic', {})

    n_panels = 3 + (1 if comp_ic else 0)
    fig, axes = plt.subplots(n_panels, 1, figsize=(13, 5 * n_panels))
    if n_panels == 1:
        axes = [axes]

    ax = axes[0]
    colors = ['#2ca02c' if v > 0 else '#d62728' for v in ic_s]
    ax.bar(ic_s.index, ic_s, color=colors, width=20, alpha=0.7)
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axhline(ic_results.get('ic_mean', 0), color='blue', linestyle='--',
               label=f"Mean IC = {ic_results.get('ic_mean', 0):+.4f}")
    ax.plot(ic_roll.index, ic_roll, color='navy', linewidth=1.5,
            label='12m Rolling IC')
    ax.set_title(
        f"Monthly IC (Spearman | ICIR = {ic_results.get('icir', 0):.3f} | "
        f"t = {ic_results.get('t_stat', 0):+.2f})",
        fontsize=12, fontweight='bold'
    )
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    ax.set_ylabel('IC')

    ax2 = axes[1]
    cumIC = ic_s.cumsum()
    ax2.plot(cumIC.index, cumIC, color='#1f77b4', linewidth=1.5)
    ax2.axhline(0, color='black', linewidth=0.8)
    ax2.set_title('Cumulative IC  (positive slope = persistent predictive edge)',
                  fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_ylabel('Cumulative IC')

    ax3 = axes[2]
    if decay:
        horizons  = list(decay.keys())
        ic_means  = [decay[h]['ic_mean'] for h in horizons]
        icirs     = [decay[h]['icir']    for h in horizons]
        x = np.arange(len(horizons))
        w = 0.35
        ax3.bar(x - w/2, ic_means, w, label='IC Mean', color='steelblue',  alpha=0.8)
        ax3.bar(x + w/2, icirs,    w, label='ICIR',    color='darkorange', alpha=0.8)
        ax3.axhline(0, color='black', linewidth=0.8)
        ax3.set_xticks(x)
        ax3.set_xticklabels([f'{h}m' for h in horizons])
        ax3.set_title('Factor Decay: IC Mean and ICIR at Multiple Forward Horizons',
                      fontsize=12, fontweight='bold')
        ax3.legend(fontsize=9)
        ax3.grid(True, alpha=0.3, axis='y')

    if comp_ic and n_panels == 4:
        ax4 = axes[3]
        names   = list(comp_ic.keys())
        c_means = [comp_ic[c]['ic_mean'] for c in names]
        c_icirs = [comp_ic[c]['icir']    for c in names]
        x = np.arange(len(names))
        w = 0.35
        ax4.bar(x - w/2, c_means, w, label='IC Mean', color='mediumseagreen', alpha=0.8)
        ax4.bar(x + w/2, c_icirs, w, label='ICIR',    color='coral',          alpha=0.8)
        ax4.axhline(0, color='black', linewidth=0.8)
        ax4.set_xticks(x)
        ax4.set_xticklabels(names)
        ax4.set_title('Per-Leg IC (universe-filtered, value components)',
                      fontsize=12, fontweight='bold')
        ax4.legend(fontsize=9)
        ax4.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.close(fig)
    print(f"[IC] Saved IC analysis to '{filename}'")


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main(load_start=None, load_end=None, start_report=None, mode=None, universe_min=None, universe_max=None):
    # ── 1. Load Data (same source as batch / individual strategies) ──────────
    data_folder = data_folder_path
    print(f"Loading data from {data_folder} ...")
    prices, volumes, highs, lows, opens = load_data(data_folder)

    if prices.empty:
        print("Error: No data loaded.")
        return

    # IN-SAMPLE defaults: warmup from 2001, report 2003–2012
    start_load   = '2001-01-01'
    end_load     = '2025-06-30'   # quarterly results in the data end with 2024Q4 (filed <= 2025-04)
    report_start = '2019-06-03'   # first months with enough point-in-time results

    if load_start and load_end and start_report:
        start_load   = load_start
        end_load     = load_end
        report_start = start_report

    prices  = prices.loc[start_load:end_load]
    volumes = volumes.loc[start_load:end_load]
    if not highs.empty: highs = highs.loc[start_load:end_load]
    if not lows.empty:  lows  = lows.loc[start_load:end_load]
    if not opens.empty: opens = opens.loc[start_load:end_load]

    prices, highs, lows, opens = mask_corporate_actions(prices, highs, lows, opens)

    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()}  →  {prices.index.max().date()}")

    # ── 2. Benchmark: equal-weight average of DAILY RETURNS, cumulated ───────
    print("Building equal-weight benchmark...")
    benchmark_series = build_benchmark(prices)   # rebased at 1.0

    print(universe_min, universe_max)

    # Frozen config -- no tuning args; params come from CSMValue's own
    # defaults. Only universe_max size is overridable, for capacity studies.
    csm = CSMValue(
        prices_df            = prices,
        volumes_df           = volumes,
        highs_df             = highs,
        lows_df              = lows,
        opens_df             = opens,
        benchmark_series     = benchmark_series,
        universe_top_n_min   = (universe_min or 301),
        universe_top_n_max       = (universe_max or 1000),
    )

    # ── 4. Calculate Factors & Positions ─────────────────────────────────────
    csm.calculate_factors()
    csm.get_positions()

    # ── 5. Backtest ───────────────────────────────────────────────────────────
    BACKTEST_MODE = mode or "event_driven"   # "event_driven" | "live"

    _bt_kwargs = dict(
        initial_capital  = 100_000,
        transaction_cost = 0.003,
        risk_free_rate   = 0.0,
    )
    if BACKTEST_MODE == "live":
        results = live_backtest(csm, **_bt_kwargs, max_entry_gap_pct=0.02)
    else:
        results = backtest_event_driven(csm, **_bt_kwargs)

    # ── 6. Slice to reporting period ──────────────────────────────────────────
    print(f"\nSlicing results to {report_start}...")
    results = slice_results(results, report_start, risk_free_rate=0.0)

    # ── 7. Trade log (logging v1) ─────────────────────────────────────────────
    report_start_dt = pd.Timestamp(report_start)
    detailed_log = pd.DataFrame()
    try:
        _full_log = get_trade_log(csm)
        if not _full_log.empty:
            detailed_log = _full_log[
                _full_log['Entry_Date'] >= report_start_dt
            ].copy()
            detailed_log.to_csv(_out(f'csm_value_{VERSION_TAG}_trade_log.csv'), index=False)
            print(f"\n[Logs] {_out(f'csm_value_{VERSION_TAG}_trade_log.csv')}  "
                  f"({len(detailed_log)} trades from {report_start_dt.date()})")
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', 260)
            print("\nSample Trades (first 5):")
            print(detailed_log.head(5).to_string(index=False))
    except Exception as e:
        print(f"\n[Logs] Warning: Trade log failed: {e}")

    # ── 7b. Reject log + forward-return counterfactuals ───────────────
    try:
        reject_df = get_reject_log(csm)
        if not reject_df.empty:
            reject_df = reject_df[reject_df['Date'] >= report_start_dt].copy()
        reject_df = add_reject_counterfactuals(reject_df, prices)
        reject_df.to_csv(_out(f'csm_value_{VERSION_TAG}_reject_log.csv'), index=False)
        print(f"\n[Logs] {_out(f'csm_value_{VERSION_TAG}_reject_log.csv')}  ({len(reject_df)} rejects)")
        if not reject_df.empty:
            print("\nReject counterfactuals by reason (mean fwd return of blocked entries):")
            _cf = (reject_df.groupby('Reject_Reason')
                   .agg(N=('Ticker', 'size'),
                        Fwd21_Mean=('Fwd_Return_21d', 'mean'),
                        Fwd63_Mean=('Fwd_Return_63d', 'mean'))
                   .round(2))
            print(_cf.to_string())
            print("  (negative mean ⇒ the filter blocked losers — it is helping)")
    except Exception as e:
        print(f"\n[Logs] Warning: Reject log failed: {e}")

    # ── 8. Trade-basis metrics from the filtered log ──────────────────────────
    if not detailed_log.empty:
        dl      = detailed_log
        wins    = (dl['PnL_Pct'] > 0).sum()
        losses  = (dl['PnL_Pct'] < 0).sum()
        total_t = len(dl)

        results['trade_win_rate']        = wins / total_t if total_t > 0 else 0.0
        results['total_trades_count']    = total_t
        results['avg_trade_return']      = dl['PnL_Pct'].mean()
        results['median_trade_return']   = dl['PnL_Pct'].median()
        results['avg_holding_days']      = dl['Holding_Days'].mean()
        results['avg_trading_days_held'] = dl['Trading_Days_Held'].mean()
        results['best_trade']            = dl['PnL_Pct'].max()
        results['worst_trade']           = dl['PnL_Pct'].min()
        results['avg_stop_pct']          = dl['Stop_Pct'].mean()
        results['avg_mae']               = dl['MAE_Pct'].mean()
        results['avg_mfe']               = dl['MFE_Pct'].mean()

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

    # ── 9. Performance Report ─────────────────────────────────────────────────
    W = 38
    SEP = "=" * W

    print(f"\n{SEP}")
    print(f"  CSM Value (Earnings-Yield) v1  —  PERFORMANCE REPORT")
    print(f"  ({report_start} → {end_load}, mode={BACKTEST_MODE})")
    print(SEP)

    print(f"\n── Portfolio Metrics ─────────────────")
    print(f"  CAGR              : {results['cagr']*100:>8.2f}%")
    print(f"  Total Return      : {results['total_return']*100:>8.2f}%")
    print(f"  Ann Volatility    : {results['ann_volatility']*100:>8.2f}%")
    print(f"  Max Drawdown      : {results['max_drawdown']*100:>8.2f}%")
    print(f"  Avg Drawdown      : {results.get('avg_drawdown', 0)*100:>8.2f}%"
          f"  ({results.get('n_episodes', 0)} episodes; mean of each episode's own trough)")
    print(f"  Avg DD (underwater): {results.get('avg_drawdown_underwater', 0)*100:>7.2f}%"
          f"  (mean depth on days actually below the running peak)")
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
        print(f"  Avg Holding Days  : {results['avg_holding_days']:>8.1f}  (calendar)")
        print(f"  Avg Trading Days  : {results['avg_trading_days_held']:>8.1f}  (exchange sessions)")
        print(f"  Avg Stop Pct      : {results.get('avg_stop_pct', 0):>8.2f}%  (initial ATR stop at entry)")
        print(f"  Avg MAE           : {results.get('avg_mae', 0):>8.2f}%  (max adverse excursion)")
        print(f"  Avg MFE           : {results.get('avg_mfe', 0):>8.2f}%  (max favorable excursion)")
    else:
        print("  No completed trades in reporting period.")

    if not detailed_log.empty:
        print(f"\n── Exit Breakdown (Reason → Detail) ──")
        _br = (detailed_log.groupby(['Exit_Reason', 'Exit_Detail'])
               .agg(N=('PnL_Pct', 'size'), AvgPnL=('PnL_Pct', 'mean'))
               .round(2))
        print(_br.to_string())

        print(f"\n── Entry Reason Breakdown ────────────")
        _er = (detailed_log.groupby('Entry_Reason')
               .agg(N=('PnL_Pct', 'size'),
                    AvgPnL=('PnL_Pct', 'mean'),
                    WinRate=('PnL_Pct', lambda s: (s > 0).mean() * 100))
               .round(2))
        print(_er.to_string())

        print(f"\n── Regime At Entry Breakdown ─────────")
        _rr = (detailed_log.groupby('Regime_At_Entry')
               .agg(N=('PnL_Pct', 'size'), AvgPnL=('PnL_Pct', 'mean'))
               .round(2))
        print(_rr.to_string())

    print(f"\n── Turnover ──────────────────────────")
    if 'ann_turnover' in results:
        print(f"  Ann Turnover      : {results['ann_turnover']*100:>8.2f}%  (daily weight changes × txn cost)")
    if 'ann_signal_turnover' in results:
        print(f"  Signal Turnover   : {results['ann_signal_turnover']:>8.1f}  round-trips/year (monthly rebal only)")

    # ── 9b. Accounting cross-check (both bookings, same trades) ─────────────────────────────────────────────
    try:
        print(f"\n── Accounting cross-check ({report_start} → {end_load}, Sharpe rf 0) ──")
        print("  engine booking = executed weight x same-day close-to-close return (as the Elendel / Zenith / Quad backtests);")
        print("  execution-faithful = also charges the gap from the previous close to the real stop/sell fill and drops the overnight gap before an open fill (AUDIT.md).")
        for _k, _lab in (('engine', 'engine booking'), ('faithful', 'execution-faithful booking')):
            _r = csm._net_by_booking[_k].loc[report_start:end_load]
            _eq = (1 + _r).cumprod(); _yrs = (_r.index[-1] - _r.index[0]).days / 365.25
            print(f"  {_lab:<28} CAGR {(_eq.iloc[-1] ** (1 / _yrs) - 1) * 100:6.2f}%   MaxDD {((_eq / _eq.cummax()) - 1).min() * 100:7.2f}%   Sharpe {np.sqrt(252) * _r.mean() / _r.std():5.2f}")
        print("  HEADLINE above uses: " + ("execution-faithful booking" if EXECUTION_FAITHFUL_ACCOUNTING else "engine booking") + "  (EXECUTION_FAITHFUL_ACCOUNTING)")
    except Exception as e:
        print(f"[Accounting] cross-check failed: {e}")

    # ── 10. Visualisation ─────────────────────────────────────────────────────
    print_yearly_returns(results['portfolio_value'], dd_series=results.get('dd_series'))
    bench_slice = benchmark_series.reindex(results['equity_curve'].index).ffill()
    plot_performance(results, bench_slice)

    # ── 11. IC / ICIR Analysis ────────────────────────────────────────────────
    try:
        ic_results = calculate_ic(
            csm,
            forward_periods = 1,
            method          = 'spearman',
            report_start    = report_start,
            per_component   = True,
        )
        plot_ic(ic_results, filename=_out(f'csm_value_{VERSION_TAG}_factor_ic.png'))
        calculate_realized_ic(csm, method='spearman', report_start=report_start)
    except Exception as e:
        print(f"[IC] Warning: IC analysis failed: {e}")

    return {
            'cagr'           : results['cagr'] * 100,
            'drawdown'       : results['max_drawdown'] * 100,
            'trade_win_rate' : results['trade_win_rate'] * 100,
            'calmar'         : results['calmar'],
            'sharpe'         : results['sharpe']
    }


if __name__ == "__main__":
    main()

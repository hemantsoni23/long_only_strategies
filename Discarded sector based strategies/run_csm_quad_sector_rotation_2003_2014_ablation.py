"""
run_csm_quad_sector_rotation_2003_2014_ablation.py
====================================================
Stage 3 (STRATEGY_VALIDATION_PLAYBOOK.md) parameter + universe-size ablation
for CSM Quad Sector Rotation (CSMQuadSectorRotation), restricted to 2003-2014
only (load from 2001-01-01 for factor warmup -- matches this strategy's own
IS convention in run_csm_quad_sector_rotation_vs_baseline.py -- report
2003-01-01 -> 2014-12-31). Everything from 2015 onward stays an untouched
holdout for a later Stage 4 OOS run, per the playbook's "all Stage 3 tuning
is IS-only" rule (Sec 3.3 gate, Sec 4).

One-lever-at-a-time ladder (playbook Sec 3.2: +-20%/+-40%, 5 points incl.
current), same methodology as csm_quad/run_marketcap_tier_ladder.py and
csm_residual/run_csm_residual_2003_2014_ablation.py, over NINE knobs centered
on CSMQuadSectorRotation's own class defaults
(csm_quad_sector_rotation_strategy.py):

  Sector layer (the new, strategy-defining knobs):
    sector_top_k       (default 3)   -- entry band: top-K of ~11 sectors
    stocks_per_sector  (default 6)   -- guaranteed quota per eligible sector
    sector_top_k_exit  (default 6)   -- exit band (wider than entry)
  Chassis knobs (same set csm_quad's own tier ladder ablates):
    buffer_ratio, hard_stop_from_entry, hard_stop_from_peak, vol_target,
    max_weight_per_stock
  Universe:
    universe_top_n_max (default 1000) -- universe_top_n_min held fixed at its
    own class default (1); this strategy inherits csm_quad's min/max BAND
    universe filter, not a single top-N cutoff, so "universe top_n" is swept
    as the max edge of that band, matching how universe_top_n was swept as a
    single knob for csm_residual (which does use a single top-N cutoff).

sector_top_k / stocks_per_sector / sector_top_k_exit are small integers, so a
literal +-20%/+-40% grid collapses to repeated values (e.g. round(3*0.8)==
round(3*1.2)==3) -- their grids below are hand-chosen 5-point integer spans
centered on the default instead, same "5 points incl. current" spirit as the
percentage grids, without meaningless duplicates.

Selection / cliff-flagging rules are identical to the other two ladders in
this repo (playbook Sec 3.3 guardrail: disqualify a "winner" that regresses
Sharpe/Calmar >15%, stability/avg-DD-depth >20%, or turnover >25% vs
BASELINE; cliff = adjacent-pair Sharpe swing >0.4).

Outputs (written next to this script):
  csm_quad_sector_rotation_2003_2014_ablation_summary.csv
  csm_quad_sector_rotation_2003_2014_selected.json
  csm_quad_sector_rotation_trade_log_TUNED.csv
"""

import gc
import json
import os
import sys

import numpy as np
import pandas as pd

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from csm_quad_sector_rotation_strategy import CSMQuadSectorRotation
from csm_quad_sector_rotation_backtest import (
    load_data, load_sector_map, build_benchmark, backtest_event_driven,
    get_trade_log, compute_drawdown_stats, data_folder_path, sector_csv_path,
)

# Matches this strategy's own validated IS convention (run_csm_quad_sector_rotation_vs_baseline.py):
# load_start='2001-01-01' for the dual 6m/12m stock+sector factor warmup. End capped at 2014-12-31
# per the requested 2003-2014 test window -- 2015 onward stays untouched.
START_LOAD, END_LOAD, REPORT_START = '2001-01-01', '2014-12-31', '2003-01-01'
TXN_COST, RFR = 0.003, 0.0

# playbook Sec 3.2: +-20%/+-40%, 5 points incl. current -- centered on
# CSMQuadSectorRotation's own class defaults (csm_quad_sector_rotation_strategy.py:93-180).
PARAM_GRID = {
    'sector_top_k':         [1,    2,    3,    4,    5],     # hand-chosen integer span (see module docstring)
    'stocks_per_sector':    [4,    5,    6,    7,    8],      # hand-chosen integer span
    'sector_top_k_exit':    [4,    5,    6,    7,    8],      # hand-chosen integer span
    'buffer_ratio':         [0.12, 0.16, 0.20, 0.24, 0.28],
    'hard_stop_from_entry': [0.09, 0.12, 0.15, 0.18, 0.21],
    'hard_stop_from_peak':  [0.12, 0.16, 0.20, 0.24, 0.28],
    'vol_target':           [0.09, 0.12, 0.15, 0.18, 0.21],
    'max_weight_per_stock': [0.03, 0.04, 0.05, 0.06, 0.07],
    'universe_top_n_max':   [600,  800,  1000, 1200, 1400],
}
DEFAULTS = {k: v[2] for k, v in PARAM_GRID.items()}   # index 2 = current/baseline value

CLIFF_SHARPE_DELTA = 0.4
GUARDRAIL = dict(sharpe=0.15, calmar=0.15, stability=0.20, avg_dd_depth=0.20, turnover=0.25)
HOLD_DAYS_CAUTION_FRAC = 0.30   # flag (not block) if avg holding days drops >30% vs baseline


def run_one(label, overrides, data, sector_map, report_start, save_logs=False):
    prices, volumes, highs, lows, opens, benchmark = data
    print(f"\n{'#' * 70}\n# RUN {label}  overrides={overrides}\n{'#' * 70}")
    csm = CSMQuadSectorRotation(
        prices_df        = prices,
        volumes_df       = volumes,
        highs_df         = highs,
        lows_df          = lows,
        opens_df         = opens,
        benchmark_series = benchmark,
        sector_map       = sector_map,
        **overrides,
    )
    csm.calculate_factors()
    csm.get_positions()
    res = backtest_event_driven(csm, initial_capital=100_000,
                                 transaction_cost=TXN_COST, risk_free_rate=RFR)

    eq = res['equity_curve']
    s  = eq.index[eq.index.searchsorted(report_start)]
    eq = eq.loc[s:]
    eq = eq / eq.iloc[0]
    ret = res['net_returns'].loc[s:]
    n_years = (eq.index[-1] - eq.index[0]).days / 365.25
    cagr = float(eq.iloc[-1] ** (1 / n_years) - 1) if n_years > 0 else np.nan

    running_max = eq.cummax()
    dd_series   = eq / running_max - 1
    dd          = float(dd_series.min())
    sharpe      = float(np.sqrt(252) * ret.mean() / ret.std()) if ret.std() > 0 else np.nan
    calmar      = float(cagr / abs(dd)) if dd != 0 and pd.notna(cagr) else np.nan
    dd_stats    = compute_drawdown_stats(dd_series)

    ann_turnover = np.nan
    if 'turnover' in res:
        t = res['turnover'].loc[s:]
        ann_turnover = float(t.sum() / n_years) if n_years > 0 else np.nan

    monthly_ret = eq.resample('ME').last().pct_change()
    stability   = float(monthly_ret.rolling(12).sum().std())

    tl_all = get_trade_log(csm)
    if not tl_all.empty:
        tl_all = tl_all[tl_all['Entry_Date'] >= pd.Timestamp(report_start)].copy()
    n_trades = len(tl_all)
    if n_trades > 0:
        wins     = tl_all['PnL_Pct'] > 0
        wr       = float(wins.mean() * 100)
        avg_hold = float(tl_all['Holding_Days'].mean())
        n_sectors_traded = int(tl_all['Sector'].nunique()) if 'Sector' in tl_all.columns else np.nan
    else:
        wr = avg_hold = np.nan
        n_sectors_traded = np.nan

    if save_logs:
        tl_all.to_csv(os.path.join(_HERE, f'csm_quad_sector_rotation_trade_log_{label}.csv'), index=False)

    row = {
        'Run':         label,
        'CAGR_pct':    round(cagr * 100, 3)  if pd.notna(cagr)   else np.nan,
        'MaxDD_pct':   round(dd * 100, 3),
        'Calmar':      round(calmar, 4)      if pd.notna(calmar) else np.nan,
        'Sharpe':      round(sharpe, 4)      if pd.notna(sharpe) else np.nan,
        'AvgDD_pct':          round(dd_stats['avg_drawdown'] * 100, 3),
        'AvgDDUnderwater_pct': round(dd_stats['avg_drawdown_underwater'] * 100, 3),
        'AnnTurnover': round(ann_turnover, 4) if pd.notna(ann_turnover) else np.nan,
        'Stability':   round(stability, 5)    if pd.notna(stability) else np.nan,
        'Trades':      n_trades,
        'WR_pct':      round(wr, 2)           if pd.notna(wr) else np.nan,
        'AvgHoldDays': round(avg_hold, 2)      if pd.notna(avg_hold) else np.nan,
        'SectorsTraded': n_sectors_traded,
    }
    print(f"[{label}] {row}")
    del csm, res, tl_all
    gc.collect()
    return row


def _regression(candidate, baseline, key, higher_is_better, use_abs=False):
    """Fractional regression of candidate vs baseline on `key`. Positive = worse."""
    b, c = baseline.get(key), candidate.get(key)
    if b is None or c is None or pd.isna(b) or pd.isna(c) or b == 0:
        return 0.0
    if use_abs:
        b, c = abs(b), abs(c)
    raw = (c - b) / abs(b)
    return -raw if higher_is_better else raw


def guardrail_ok(candidate, baseline):
    """playbook Sec 3.3: every ablation cell must clear all 5 regression caps
    vs baseline to be eligible as a 'winner' -- never optimise a single scalar."""
    return (
        _regression(candidate, baseline, 'Sharpe',    True)                    <= GUARDRAIL['sharpe']
        and _regression(candidate, baseline, 'Calmar', True)                   <= GUARDRAIL['calmar']
        and _regression(candidate, baseline, 'Stability', False)               <= GUARDRAIL['stability']
        and _regression(candidate, baseline, 'AvgDD_pct', False, use_abs=True) <= GUARDRAIL['avg_dd_depth']
        and _regression(candidate, baseline, 'AnnTurnover', False)             <= GUARDRAIL['turnover']
    )


def select_knob_winner(non_baseline_pts, baseline):
    """playbook Sec 3.3 selection rule: among grid points that clear the
    guardrail, keep the best Calmar (tie-break CAGR); if none clear it,
    the ablation is inconclusive -> return None (NO_CHANGE)."""
    survivors = [r for r in non_baseline_pts if guardrail_ok(r, baseline)]
    if not survivors:
        return None
    return max(survivors, key=lambda r: (
        r['Calmar'] if pd.notna(r['Calmar']) else -np.inf,
        r['CAGR_pct'] if pd.notna(r['CAGR_pct']) else -np.inf,
    ))


def cliff_flags(points_sorted_by_value):
    """playbook Sec 3.2: flag any adjacent-pair |Sharpe delta| > 0.4 as a
    cliff (overfit to that exact value) across the 5 grid points."""
    flags = []
    for a, b in zip(points_sorted_by_value, points_sorted_by_value[1:]):
        sa, sb = a.get('Sharpe'), b.get('Sharpe')
        flags.append(bool(pd.notna(sa) and pd.notna(sb) and abs(sb - sa) > CLIFF_SHARPE_DELTA))
    return flags


def main():
    print("Loading data (once)...")
    prices, volumes, highs, lows, opens = load_data(data_folder_path)
    prices  = prices.loc[START_LOAD:END_LOAD]
    volumes = volumes.loc[START_LOAD:END_LOAD]
    highs   = highs.loc[START_LOAD:END_LOAD] if not highs.empty else highs
    lows    = lows.loc[START_LOAD:END_LOAD]  if not lows.empty  else lows
    opens   = opens.loc[START_LOAD:END_LOAD] if not opens.empty else opens
    print(f"Prices shape : {prices.shape}")
    print(f"Date range   : {prices.index.min().date()} -> {prices.index.max().date()}  "
          f"(report from {REPORT_START}, everything after {END_LOAD} untouched)")

    benchmark = build_benchmark(prices)
    sector_map = load_sector_map(sector_csv_path)
    data = (prices, volumes, highs, lows, opens, benchmark)

    all_rows = []

    baseline = run_one('BASELINE', {}, data, sector_map, REPORT_START)
    all_rows.append({**baseline, 'Param': 'BASELINE', 'Value': None, 'Cliff': False})

    knob_winners = {}
    for knob, grid in PARAM_GRID.items():
        pts = []
        for val in grid:
            if val == DEFAULTS[knob]:
                row = dict(baseline)          # reuse -- don't re-run the identical config
            else:
                row = run_one(f'{knob}={val}', {knob: val}, data, sector_map, REPORT_START)
            pts.append({**row, 'Param': knob, 'Value': val})

        flags = cliff_flags(pts)
        for i, r in enumerate(pts):
            left  = flags[i - 1] if i > 0 else False
            right = flags[i]     if i < len(flags) else False
            all_rows.append({**r, 'Cliff': bool(left or right)})

        non_baseline = [r for r in pts if r['Value'] != DEFAULTS[knob]]
        winner = select_knob_winner(non_baseline, baseline)
        knob_winners[knob] = winner
        hold_flag = ''
        if winner is not None and pd.notna(winner.get('AvgHoldDays')) and pd.notna(baseline.get('AvgHoldDays')) \
                and baseline['AvgHoldDays'] > 0 \
                and (baseline['AvgHoldDays'] - winner['AvgHoldDays']) / baseline['AvgHoldDays'] > HOLD_DAYS_CAUTION_FRAC:
            hold_flag = '  [CAUTION: avg holding days dropped >30%]'
        print(f"  {knob} winner: {winner['Value'] if winner else 'NO_CHANGE'}{hold_flag}")

    changed = {k: w['Value'] for k, w in knob_winners.items() if w is not None}
    print(f"\n>>> per-knob winners: {changed or 'NONE (all NO_CHANGE)'}")

    if changed:
        combined = run_one('TUNED', changed, data, sector_map, REPORT_START, save_logs=True)
        if guardrail_ok(combined, baseline):
            tuned_params, tuned_row, tuned_label = changed, combined, 'TUNED_COMBINED'
        else:
            print("  combined TUNED failed the guardrail recheck -- "
                  "falling back to the single best-Calmar knob winner")
            best_knob = max(changed, key=lambda k: (
                knob_winners[k]['Calmar'] if pd.notna(knob_winners[k]['Calmar']) else -np.inf))
            tuned_params = {best_knob: changed[best_knob]}
            tuned_row = run_one('TUNED', tuned_params, data, sector_map, REPORT_START, save_logs=True)
            tuned_label = f'TUNED_FALLBACK_{best_knob}'
    else:
        tuned_row = run_one('TUNED', {}, data, sector_map, REPORT_START, save_logs=True)
        tuned_params, tuned_label = {}, 'NO_CHANGE'

    all_rows.append({**tuned_row, 'Param': 'TUNED', 'Value': str(tuned_params) or 'NO_CHANGE', 'Cliff': False})

    selected = {
        'window':              [START_LOAD, END_LOAD, REPORT_START],
        'selected_params':     tuned_params,
        'knobs_changed':       list(tuned_params.keys()),
        'selection_label':     tuned_label,
        'metrics_baseline':    baseline,
        'metrics_tuned':       tuned_row,
    }

    summary = pd.DataFrame(all_rows)
    summary.to_csv(os.path.join(_HERE, 'csm_quad_sector_rotation_2003_2014_ablation_summary.csv'), index=False)
    with open(os.path.join(_HERE, 'csm_quad_sector_rotation_2003_2014_selected.json'), 'w') as f:
        json.dump(selected, f, indent=2, default=str)

    print("\n" + "=" * 90)
    print(f" CSM QUAD SECTOR ROTATION ABLATION  --  {REPORT_START} -> {END_LOAD}  |  txn 0.3%  |  RFR 0%")
    print("=" * 90)
    print(summary.to_string(index=False))
    print(f"\nSelected: {tuned_params or 'NO_CHANGE'}  ({tuned_label})")
    print("\nSaved: csm_quad_sector_rotation_2003_2014_ablation_summary.csv, "
          "csm_quad_sector_rotation_2003_2014_selected.json")


if __name__ == '__main__':
    main()

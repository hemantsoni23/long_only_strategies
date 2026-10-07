"""
run_csm_pead_backtest.py -- PEAD Confirmed-Drift, reported exactly like the Elendel-chassis strategies.

PEAD is event-driven (entries are triggered by each company's own result date), so it keeps its own event loop (`PEADStrategy.simulate`, like the HR/VCP breakout strategies) rather than
the monthly-rebalance Elendel engine.  Everything the user sees is Elendel's: the same performance report (portfolio metrics, 3 win-rate views, trade statistics with MAE/MFE,
exit / entry-reason / regime breakdowns, turnover), yearly returns with yearly max/avg drawdown, 5-panel performance chart + monthly heatmap, daily log, Elendel-column trade log,
and an IC/ICIR section (event-level: signal vs forward return across filing months, with a factor-decay table).

    python3 run_csm_pead_backtest.py [--start 2020-09-01] [--end 2025-06-30]
Report formatting code is generated from the Elendel runner (`elendel_style_report.py`, see _generate_report_style.py).  Fundamentals limit the window to ~2020-09 .. 2025-06.
"""
import argparse
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import elendel_style_report as esr                                               # noqa: E402
from run_pead_backtest import load_all                                           # noqa: E402
from pead_strategy import PEADStrategy                                           # noqa: E402

OUT = os.path.join(HERE, 'output'); os.makedirs(OUT, exist_ok=True)
esr.configure('CSM PEAD Confirmed-Drift', 'csm_pead', OUT)


def regime_series(bench, index):
    """BULL / BEAR / HIGH_VOL / PANIC exactly as the Elendel engine labels them (benchmark SMA200, expanding 75th / 95th percentile of 21d benchmark vol, all lagged)."""
    b = bench.reindex(index).ffill(); r = b.pct_change(fill_method=None)
    bvol = r.rolling(21).std().shift(1)
    panic = (bvol > bvol.expanding(min_periods=126).quantile(0.95)).fillna(False)
    hv = (bvol > bvol.expanding(min_periods=63).quantile(0.75).shift(1)).fillna(False)
    bear = (b.shift(1) < b.rolling(200, min_periods=150).mean().shift(1)).fillna(False)
    return pd.Series(np.where(panic, 'PANIC', np.where(hv, 'HIGH_VOL', np.where(bear, 'BEAR', 'BULL'))), index=index)


def build_results(st, bench, end=None):
    res = st.simulate(end=end)
    eq = res['equity'].copy(); w = res['executed_weights']
    out = dict(equity_curve=eq / eq.iloc[0], portfolio_value=eq / eq.iloc[0], net_returns=res['net_returns'], executed_weights=w,
               turnover=w.diff().abs().sum(axis=1).fillna(0.0), regime=regime_series(bench, eq.index))
    out['cagr'] = 0
    return out, res


def elendel_trade_log(st, res, regime, start):
    """Trades in the Elendel trade-log columns (PnL %, MAE/MFE from daily lows/highs between entry and exit, regimes, stop levels)."""
    tr = res['trades'].copy()
    tr = tr[tr.Entry_Date >= pd.Timestamp(start)].reset_index(drop=True)
    if tr.empty:
        return pd.DataFrame()
    P = st.prices; lows = st.lows.ffill() if not st.lows.empty else P.ffill(); highs = st.highs.ffill() if not st.highs.empty else P.ffill()
    eq = res['equity']; rows = []
    for t in tr.itertuples():
        seg = slice(t.Entry_Date, t.Exit_Date)
        lo = lows.loc[seg, t.Ticker].iloc[1:]; hi = highs.loc[seg, t.Ticker].iloc[1:]
        mae = (lo.min() / t.Entry_Price - 1) * 100 if len(lo) else np.nan
        mfe = (hi.max() / t.Entry_Price - 1) * 100 if len(hi) else np.nan
        peak = hi.max() if len(hi) else np.nan
        stop_lvl = t.Entry_Price * (1 - st.hard_stop)
        xi = st._dates.get_loc(t.Exit_Date); gap = t.Reason == 'STOP_HIT' and st._O[xi, st._cols[t.Ticker]] <= stop_lvl
        pv = float(eq.loc[t.Entry_Date]); size = t.Shares * t.Entry_Price
        pnl_pct = (t.Exit_Price / t.Entry_Price - 1) * 100
        rows.append({
            'Ticker': t.Ticker, 'Entry_Date': t.Entry_Date, 'Entry_Price': t.Entry_Price, 'Exit_Date': t.Exit_Date, 'Exit_Price': round(t.Exit_Price, 4),
            'Close_At_Exit': float(st._C[xi, st._cols[t.Ticker]]), 'Peak_Price': peak, 'Stop_Price_At_Exit': stop_lvl, 'Stop_Pct': st.hard_stop * 100, 'ATR_At_Entry': np.nan,
            'Entry_Reason': 'PEAD_CONFIRMED', 'Exit_Reason': t.Reason,
            'Exit_Detail': ('HOLD_EXPIRED' if t.Reason == 'TIME_STOP' else ('GAP_DOWN_OPEN' if gap else 'ENTRY_HARD')),
            'Rank_At_Entry': np.nan, 'Rank_At_Exit': np.nan, 'Score_At_Entry': t.Score,
            'Regime_At_Entry': regime.get(t.Entry_Date, ''), 'Regime_At_Exit': regime.get(t.Exit_Date, ''), 'Signal_Age_Months': np.nan,
            'Weight': size / pv, 'Quantity': t.Shares, 'Position_Size': round(size, 2), 'Portfolio Value': round(pv, 2),
            'PnL_Pct': round(pnl_pct, 4), 'PnL_Abs': round(t.Shares * (t.Exit_Price - t.Entry_Price), 2),
            'Holding_Days': max((t.Exit_Date - t.Entry_Date).days, 1), 'Trading_Days_Held': t.Days_Held, 'MAE_Pct': mae, 'MFE_Pct': mfe,
            'SUE_At_Entry': t.SUE, 'EAR_At_Entry': t.EAR, 'Signal_Date': t.Signal_Date, 'Filed': t.Filed})
    df = pd.DataFrame(rows).sort_values('Entry_Date').reset_index(drop=True); df.index += 1; df.index.name = 'Trade_ID'
    n = len(df); wins = (df.PnL_Pct > 0).sum()
    print(f"[Trade Log] {n} trades | Wins: {wins} | Losses: {(df.PnL_Pct < 0).sum()} | Win Rate: {wins/n*100:.1f}%")
    print(f"[Trade Log] Worst trade: {df.PnL_Pct.min():.2f}%  Best trade: {df.PnL_Pct.max():.2f}%")
    print(f"[Trade Log] Exit reasons: {df.Exit_Reason.value_counts().to_dict()}")
    print(f"[Trade Log] Exit details: {df.Exit_Detail.value_counts().to_dict()}")
    return df


def _nw_t(x, lag):
    x = np.asarray(pd.Series(x).dropna(), dtype=float); n = len(x)
    if n < 6:
        return np.nan
    d = x - x.mean(); s = (d * d).mean()
    for j in range(1, min(lag, n - 1) + 1):
        s += 2 * (1 - j / (lag + 1)) * (d[j:] * d[:-j]).mean()
    return x.mean() / np.sqrt(max(s, 1e-18) / n)


def event_ic(st, start, end, horizons=(20, 40, 60)):
    """Event-level IC / ICIR: within each filing month (>= 30 liquid events with valid SUE & EAR) the Spearman rank correlation between a signal known on the signal day and the stock's forward
    return from the entry close (next day) -- the analogue of the Elendel factor IC for a strategy that has no monthly cross-section."""
    ev = st.events[st.events.liquid & st.events.sue_eps.notna() & st.events.ear.notna()].copy()
    ev = ev[(ev.sig_date >= pd.Timestamp(start)) & (ev.sig_date <= pd.Timestamp(end))]
    z = lambda x: (x - x.mean()) / x.std()
    ev['month'] = ev.sig_date.dt.to_period('M')
    ev['SUE'] = ev.sue_eps; ev['EAR'] = ev.ear; ev['SUE+EAR'] = ev.groupby('month').sue_eps.transform(z) + ev.groupby('month').ear.transform(z)
    C = st._C; cj = ev.symbol.map(st._cols).astype(int).values; e = ev.sig_idx.values + 1
    print("\n" + "=" * 68)
    print(f" EVENT-LEVEL IC / ICIR  —  {esr.LABEL}  (SPEARMAN, filing-month cross-sections)")
    print("=" * 68)
    print(f"  Events used          : {len(ev):,}  (liquid universe, valid SUE & EAR, {start} → {end})")
    out = {}
    for h in horizons:
        ok = e + h < len(st._dates)
        fwd = np.full(len(ev), np.nan); fwd[ok] = C[e[ok] + h, cj[ok]] / C[e[ok], cj[ok]] - 1
        ev[f'f{h}'] = np.clip(fwd, -0.6, 3.0)
    for name in ('SUE', 'EAR', 'SUE+EAR'):
        print(f"\n  Signal: {name}")
        print(f"   Horizon     IC Mean      ICIR    Hit%   NW-t   months")
        for h in horizons:
            g = ev.dropna(subset=[f'f{h}']).groupby('month')
            ics = g.apply(lambda d: d[name].corr(d[f'f{h}'], method='spearman') if len(d) >= 30 else np.nan).dropna()
            if len(ics) < 6:
                continue
            tag = ' ← peak' if False else ''
            print(f"   {h:>3}d      {ics.mean():+.4f}    {ics.mean()/ics.std():6.3f}   {(ics>0).mean()*100:4.0f}%  {_nw_t(ics, max(h//21 - 1, 0)):+5.2f}   {len(ics)}")
            out[(name, h)] = ics
    print("=" * 68)
    return out


def main(start='2020-09-01', end='2025-06-30'):
    prices, volumes, highs, lows, opens, bench = load_all()
    st = PEADStrategy(prices_df=prices, volumes_df=volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=bench)
    st.calculate_factors(); st.get_positions()
    results, raw = build_results(st, bench, end)
    results = esr.slice_results(results, start, risk_free_rate=0.0)   # rf 0 as in the Elendel runner
    results['equity_curve'] = results['equity_curve'].loc[:end];
    detailed_log = elendel_trade_log(st, raw, results['regime'], start)
    if not detailed_log.empty:
        detailed_log = detailed_log[detailed_log.Exit_Date <= pd.Timestamp(end)]
        detailed_log.to_csv(os.path.join(OUT, 'csm_pead_trade_log.csv'))
        print(f"\n[Logs] {os.path.join(OUT, 'csm_pead_trade_log.csv')}  ({len(detailed_log)} trades from {start})")
    esr.print_report(results, detailed_log, start, end, 'event_driven')
    esr.print_yearly_returns(results['portfolio_value'], dd_series=results.get('dd_series'))
    bench_slice = bench.reindex(results['equity_curve'].index).ffill()
    esr.plot_performance(results, bench_slice)
    event_ic(st, start, end)
    return dict(cagr=results['cagr'] * 100, drawdown=results['max_drawdown'] * 100, sharpe=results['sharpe'], calmar=results['calmar'])


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--start', default='2020-09-01'); ap.add_argument('--end', default='2025-06-30')
    a = ap.parse_args(); main(a.start, a.end)

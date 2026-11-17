"""Descriptive, point-in-time technical features for ESR-qualified events.

This is an event study, NOT a portfolio backtest. All features use at most the
signal close. Future returns use the next open and exit 20/60 sessions later,
assuming both opens exist and charging 0.30% each way. No slots, stops,
market impact, position sizing or cash are modeled. Events can overlap.
"""
from pathlib import Path
import sys

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'csm_esr'))
from backtest_data import load_all
from esr_strategy import CSMESRStrategy

OUT = Path(__file__).resolve().parent
END = pd.Timestamp('2024-12-31')
START = pd.Timestamp('2020-09-01')
COST = .003


def present(values, minimum):
    a = np.asarray(values, dtype=float)
    a = a[np.isfinite(a)]
    return a if len(a) >= minimum else np.array([])


def event_features(st):
    close = st.prices.to_numpy()
    high = st.highs.reindex(index=st.prices.index, columns=st.prices.columns).to_numpy()
    low = st.lows.reindex(index=st.prices.index, columns=st.prices.columns).to_numpy()
    volume = st.volumes.reindex(index=st.prices.index, columns=st.prices.columns).to_numpy()
    opening = st._O
    market = pd.Series(st._bench, index=st._dates)
    market_sma = market.rolling(200, min_periods=150).mean().to_numpy()
    rows = []
    for event in st.candidates.itertuples(index=False):
        s = int(event.sig_idx)
        j = st._cols[event.symbol]
        c = close[s, j]
        entry_i = s + 1
        if not np.isfinite(c) or c <= 0:
            continue
        row = {'symbol': event.symbol, 'filed': event.filed, 'signal_date': event.sig_date,
               'available_date': event.available_date, 'base_date': event.reaction_base_date,
               'entry_date': st._dates[entry_i], 'sue': event.sue_eps, 'ear': event.ear,
               'esr_score': event.score}
        for n, minimum in ((50, 40), (200, 160)):
            window = present(close[max(0, s - n + 1):s + 1, j], minimum)
            row[f'above_sma{n}'] = (bool(c > window.mean()) if len(window) else None)
        highs = present(high[max(0, s - 251):s + 1, j], 200)
        row['high52_proximity'] = c / highs.max() if len(highs) and highs.max() > 0 else np.nan
        h, l = high[s, j], low[s, j]
        row['close_location'] = ((c - l) / (h - l) if np.isfinite(h) and np.isfinite(l) and h > l and l <= c <= h else np.nan)
        # First two post-filing trading sessions; pre-filing reference excludes
        # the filing date, whose time may be after the close or intraday.
        pre_end = int(st._dates.searchsorted(event.filed, side='left'))
        pre_vol = present(volume[max(0, pre_end - 20):pre_end, j], 15)
        post_vol = present(volume[s - 1:s + 1, j], 2)
        row['post_volume_ratio'] = (post_vol.mean() / pre_vol.mean()
                                    if len(pre_vol) and len(post_vol) and pre_vol.mean() > 0 else np.nan)
        value = close[max(0, s - 62):s + 1, j] * volume[max(0, s - 62):s + 1, j]
        valid_value = present(value, 40)
        row['median_traded_value_63'] = np.median(valid_value) if len(valid_value) else np.nan
        # Pre-filing trend: both endpoints and the whole volatility sample are
        # before the filing date, so it does not reuse ESR's reaction interval.
        k = pre_end - 1
        if k >= 63 and close[k, j] > 0 and close[k - 63, j] > 0:
            win = close[k - 63:k + 1, j]
            with np.errstate(invalid='ignore', divide='ignore'):
                daily = win[1:] / win[:-1] - 1
            observations = present(daily, 50)
            vol = np.std(observations, ddof=1) * np.sqrt(252) if len(observations) else np.nan
            ret = close[k, j] / close[k - 63, j] - 1
            row['pre_return_63'] = ret
            row['pre_risk_adjusted_63'] = ret / vol if np.isfinite(vol) and vol > 0 else np.nan
        else:
            row['pre_return_63'] = row['pre_risk_adjusted_63'] = np.nan
        if s >= 20:
            win = close[s - 20:s + 1, j]
            with np.errstate(invalid='ignore', divide='ignore'):
                daily = win[1:] / win[:-1] - 1
            observed = present(daily, 15)
            row['volatility_20'] = np.std(observed, ddof=1) * np.sqrt(252) if len(observed) else np.nan
        else:
            row['volatility_20'] = np.nan
        row['market_above_sma200'] = (bool(st._bench[s] > market_sma[s])
                                      if np.isfinite(market_sma[s]) else None)
        for horizon in (20, 60):
            end_i = entry_i + horizon
            enter = opening[entry_i, j]
            leave = opening[end_i, j] if end_i < len(st._dates) else np.nan
            row[f'return_{horizon}d_net'] = ((leave / enter) * (1 - COST) / (1 + COST) - 1
                                             if np.isfinite(enter) and enter > 0 and np.isfinite(leave) and leave > 0 else np.nan)
        rows.append(row)
    return pd.DataFrame(rows)


def grouped(data):
    checks = [
        ('Stock above 50-day average', 'above_sma50', True, False),
        ('Stock above 200-day average', 'above_sma200', True, False),
        ('Within 10% of 52-week high', 'high52_proximity', lambda x: x >= .9, lambda x: x < .9),
        ('Reaction volume at least 1.5x pre-filing average', 'post_volume_ratio', lambda x: x >= 1.5, lambda x: x < 1.5),
        ('Positive 63-session pre-filing return', 'pre_return_63', lambda x: x > 0, lambda x: x <= 0),
        ('Positive risk-adjusted pre-filing return', 'pre_risk_adjusted_63', lambda x: x > 0, lambda x: x <= 0),
        ('Signal closes in upper half of its daily range', 'close_location', lambda x: x >= .5, lambda x: x < .5),
        ('Internal market above 200-day average', 'market_above_sma200', True, False),
    ]
    result = []
    for name, column, positive, negative in checks:
        valid = data[column].notna()
        for label, criterion in (('yes', positive), ('no', negative)):
            mask = criterion(data[column]) if callable(criterion) else data[column].eq(criterion)
            sample = data.loc[valid & mask]
            row = {'feature': name, 'group': label, 'events': len(sample)}
            for horizon in (20, 60):
                values = sample[f'return_{horizon}d_net'].dropna()
                row[f'n_{horizon}d'] = len(values)
                row[f'mean_{horizon}d_pct'] = values.mean() * 100 if len(values) else np.nan
                row[f'median_{horizon}d_pct'] = values.median() * 100 if len(values) else np.nan
                row[f'win_{horizon}d_pct'] = values.gt(0).mean() * 100 if len(values) else np.nan
            result.append(row)
    return pd.DataFrame(result)


def main():
    prices, volumes, highs, lows, opens, benchmark = load_all(load_end=str(END.date()))
    st = CSMESRStrategy(prices, volumes, highs_df=highs, lows_df=lows, opens_df=opens, benchmark_series=benchmark)
    st.calculate_factors()
    data = event_features(st)
    data = data[data.signal_date.between(START, END)].reset_index(drop=True)
    data.to_csv(OUT / 'qualified_events.csv', index=False, float_format='%.8f')
    summary = grouped(data)
    summary.to_csv(OUT / 'feature_groups.csv', index=False, float_format='%.6f')
    print('\nQualified events in report window:', len(data))
    print('Valid entry and 20/60 session open:', data.return_20d_net.notna().sum(), data.return_60d_net.notna().sum())
    print(summary.round(2).to_string(index=False))
    print('\nFor interpretation: selected qualifying events only; equal event weight; overlapping events; no stops, cash, slot limits or market impact.')

if __name__ == '__main__':
    main()

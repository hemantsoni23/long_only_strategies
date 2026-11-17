"""Construct earnings-surprise events from quarterly JSON snapshots.

The JSON snapshot does not preserve every earlier version of a filing. We never
backdate a value beyond the filing date supplied by that snapshot, but cannot
establish whether the snapshot itself was later revised without another source.
EPS comparisons are rejected when the filed share counts differ by over 3%.
This conservative guard limits split/bonus distortions, but is not proof that
the source has not retrospectively restated an EPS figure.
"""
import datetime
import glob
import json
import os
import re

import numpy as np
import pandas as pd

FUNDAMENTALS_DIR = os.environ.get(
    'CSM_FUNDAMENTALS_DIR',
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fundamentals'),
)
RESEARCH_END = pd.Timestamp('2024-12-31')
SHARE_TOLERANCE = 0.03
VALID_FACE_VALUES = (0.5, 1.0, 2.0, 5.0, 10.0, 100.0)
EVENT_COLUMNS = ['symbol', 'basis', 'period_end', 'filed', 'sue_eps', 'dm_ebit', 'sg_np']


def _number(value):
    if isinstance(value, bool):
        return np.nan
    try:
        value = float(value)
        return value if np.isfinite(value) else np.nan
    except (TypeError, ValueError):
        return np.nan


def _parse_date(value):
    try:
        # pandas dayfirst=True can silently turn ISO 2020-11-05 into 11 May.
        iso = isinstance(value, str) and re.match(r'^\d{4}-\d{2}-\d{2}', value.strip())
        return pd.Timestamp(pd.to_datetime(value, dayfirst=not bool(iso))).normalize()
    except (TypeError, ValueError):
        return pd.NaT


def _read_facts(directory, symbols):
    paths = sorted(glob.glob(os.path.join(directory, '*.json')) +
                   glob.glob(os.path.join(directory, 'sme', '*.json')))
    if symbols is not None:
        symbols = set(symbols)
        paths = [p for p in paths if os.path.splitext(os.path.basename(p))[0] in symbols]
    rows = []
    for path in paths:
        symbol = os.path.splitext(os.path.basename(path))[0]
        try:
            with open(path, encoding='utf-8') as stream:
                doc = json.load(stream)
        except (OSError, ValueError):
            continue
        for year in (doc.get('fiscal_years') or {}).values():
            for quarter in (year.get('quarters') or {}).values():
                for basis in ('standalone', 'consolidated'):
                    block = quarter.get(basis)
                    if not block:
                        continue
                    period = block.get('period') or {}
                    try:
                        start = datetime.date.fromisoformat((period.get('start') or '')[:10])
                        end = datetime.date.fromisoformat((period.get('end') or '')[:10])
                    except (ValueError, TypeError):
                        continue
                    if not 80 <= (end - start).days <= 100:
                        continue
                    filed = _parse_date(block.get('filed_date'))
                    period_end = pd.Timestamp(end)
                    if (pd.isna(filed) or filed > RESEARCH_END or
                            not 0 <= (filed - period_end).days <= 120 or
                            not period_end.is_quarter_end):
                        continue
                    inc = block.get('income_statement') or {}
                    capital, face = _number(inc.get('paid_up_equity_share_capital')), _number(inc.get('face_value_per_share'))
                    shares = capital / face if (capital > 0 and face in VALID_FACE_VALUES) else np.nan
                    pbt, interest = _number(inc.get('profit_before_tax')), _number(inc.get('finance_costs'))
                    rows.append({'symbol': symbol, 'basis': basis, 'period_end': period_end,
                                 'filed_date': filed, 'eps': _number(inc.get('basic_eps')),
                                 'shares': shares, 'net_profit': _number(inc.get('net_profit')),
                                 'revenue': _number(inc.get('revenue_from_operations')),
                                 'ebit': pbt + interest})
    return pd.DataFrame(rows)


def _feature(known, period_end):
    current = known.get(period_end)
    if current is None or not np.isfinite(current['shares']) or current['shares'] <= 0:
        return None
    shares = current['shares']
    def eps_at(offset):
        quarter_end = (period_end.to_period('Q') - offset).end_time.normalize()
        row = known.get(quarter_end)
        if row is None or not np.isfinite(row['shares']) or row['shares'] <= 0:
            return np.nan
        if abs(row['shares'] / shares - 1) > SHARE_TOLERANCE:
            return np.nan
        return row['eps']
    eps = [eps_at(i) for i in range(13)]
    surprise = eps[0] - eps[4]
    prior = np.array([eps[i] - eps[i + 4] for i in range(1, 9)], dtype=float)
    prior = prior[np.isfinite(prior)]
    sd = prior.std(ddof=1) if len(prior) >= 4 else np.nan
    sue = surprise / sd if np.isfinite(surprise) and np.isfinite(sd) and sd > 0 else np.nan
    old = known.get(period_end - pd.DateOffset(years=1))
    growth = margin_change = np.nan
    if old:
        a, b = current['net_profit'], old['net_profit']
        if np.isfinite(a) and np.isfinite(b) and abs(a) + abs(b) > 0:
            growth = (a - b) / ((abs(a) + abs(b)) / 2)
        if all(np.isfinite(x) for x in (current['ebit'], old['ebit'], current['revenue'], old['revenue'])) and current['revenue'] and old['revenue']:
            margin_change = current['ebit'] / current['revenue'] - old['ebit'] / old['revenue']
    return {'sue_eps': sue, 'dm_ebit': margin_change, 'sg_np': growth}


def build_events(facts=None, directory=None, symbols=None):
    """Emit the first valid SUE for each quarter, using facts filed by then.

    Same-day facts are processed together; the strategy makes them usable no
    earlier than the next day. Consolidated wins only when both bases are
    available at the same event, never because of a later filing.
    """
    f = _read_facts(directory or FUNDAMENTALS_DIR, symbols) if facts is None else facts.copy()
    if f.empty:
        return pd.DataFrame(columns=EVENT_COLUMNS)
    if symbols is not None:
        f = f[f.symbol.isin(symbols)].copy()
    f['filed_date'] = pd.to_datetime(f.filed_date).dt.normalize()
    f['period_end'] = pd.to_datetime(f.period_end).dt.normalize()
    f = f[(f.filed_date <= RESEARCH_END) & ((f.filed_date - f.period_end).dt.days.between(0, 120))]
    events = []
    for symbol, group in f.groupby('symbol', sort=False):
        known = {'standalone': {}, 'consolidated': {}}
        emitted = set()
        for filed, batch in group.sort_values(['filed_date', 'period_end', 'basis'], kind='stable').groupby('filed_date', sort=True):
            for record in batch.to_dict('records'):
                if record['basis'] in known:
                    known[record['basis']][record['period_end']] = record
            periods = sorted(set(batch.period_end))
            for period_end in periods:
                newest = max((p for history in known.values() for p in history), default=period_end)
                if period_end in emitted or period_end < newest:
                    continue
                possible = []
                for basis in ('standalone', 'consolidated'):
                    # A new earnings event must correspond to this quarter's filing,
                    # not a later update to some other quarter.
                    if not ((batch.basis == basis) & (batch.period_end == period_end)).any():
                        continue
                    features = _feature(known[basis], period_end)
                    if features is not None and np.isfinite(features['sue_eps']):
                        possible.append({'symbol': symbol, 'basis': basis, 'period_end': period_end,
                                         'filed': filed, **features})
                if possible:
                    events.append(possible[-1])
                    emitted.add(period_end)
    return pd.DataFrame(events, columns=EVENT_COLUMNS).sort_values(['filed', 'symbol']).reset_index(drop=True)

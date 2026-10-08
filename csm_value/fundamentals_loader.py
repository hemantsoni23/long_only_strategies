"""
fundamentals_loader.py -- point-in-time quarterly results for CSM Value, read DIRECTLY from the raw NSE XBRL JSON files (no intermediate cache, no other project).

Source   : one JSON per symbol in FUNDAMENTALS_DIR (default /Users/hemantsoni/Documents/stocks_fundamentals/fundamentals, override with the CSM_FUNDAMENTALS_DIR env var or the `directory`
           argument): fiscal_years -> quarters -> consolidated / standalone -> income_statement, period, filed_date.  Whole corpus parses in ~4 s.
Coverage : results for FY2018-19 onward only (NSE XBRL).  Nothing earlier exists in this data, so TTM earnings are first available in 2019.

What a row holds (one per symbol and period_end, keyed by the filing that reported it):
    filed       filing date (a result is usable from this date; the strategy trades the NEXT close after it is known)
    np_ttm      sum of the last 4 consecutive quarters' net profit.  profit_basis='total' (default): the reported net profit line, the same definition in every quarter of every company.
                'owners_consistent': owners' profit only where all four quarters of a figure report it, else the total line for all four.  'core': reported profit less other income and exceptional items (25% tax; banks unchanged).
                'owners': profit attributable to owners when reported, else total -- NOT recommended: owners' profit is reported for only 80% of consolidated and 10% of standalone filings and
                1,053 of ~1,600 consolidated companies mix both definitions across quarters, which corrupts trailing sums and year-on-year growth.  Kept for ablation.
    sg_np       symmetric yoy growth of the latest quarter's net profit: (x - x_4q_ago) / mean(|x|, |x_4q_ago|)
    shares_adj  shares outstanding in TODAY'S UNITS (see below)
    oneoff_share  trailing-12m (other income + exceptional gains) / trailing-12m pre-tax profit (0 for banks, NaN if pre-tax profit is not positive); used by the optional one-off filter

Why `shares_adj`: the OHLCV prices are retroactively split/bonus-adjusted (e.g. HDFCBANK shows ~Rs 550 in 2019 although it traded above Rs 1,100 after its 2019 split).  A filing's share count
is in the units of its own date, so (adjusted price x filed shares) is wrong by every later split/bonus -- and it is wrong in a way that leaks the future: stocks that later split look
2-10x cheaper in the past.  We restore consistent units by multiplying each filing's share count by the clean split/bonus ratios visible in LATER filings of the same company
(a jump in paid-up capital / face value of exactly 1.5, 2, 2.5, 3, 4, 5 or 10 times, or the reciprocal).  This only undoes the adjustment already baked into the prices; it reveals nothing
about returns.  Genuine issuance (rights, QIP, mergers) is not a clean ratio and is deliberately left alone.
Known residual: splits after the last filing in the data (2025-26) cannot be seen from the filings, so those stocks keep a unit mismatch; see README.
"""
import datetime
import glob
import json
import math
import os

import numpy as np
import pandas as pd

FUNDAMENTALS_DIR = os.environ.get('CSM_FUNDAMENTALS_DIR', '/Users/hemantsoni/Documents/stocks_fundamentals/fundamentals')
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
    for fmt in ('%d-%b-%Y %H:%M', '%d-%b-%Y', '%d-%B-%Y %H:%M', '%d-%B-%Y'):
        try:
            return datetime.datetime.strptime(s, fmt).date()
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
                if profit_basis == 'total':
                    npf = _num(inc.get('net_profit'))
                    if npf is None:
                        npf = _num(inc.get('net_profit_attributable_to_owners'))
                else:
                    npf = _num(inc.get('net_profit_attributable_to_owners'))
                    if npf is None:
                        npf = _num(inc.get('net_profit'))
                if npf is None:
                    for k in ('ProfitLossForThePeriod', 'ProfitLossFromOrdinaryActivitiesAfterTax'):
                        npf = _num(facts.get(k))
                        if npf is not None:
                            break
                np_total = _num(inc.get('net_profit'))
                if np_total is None:
                    np_total = npf
                np_owners = _num(inc.get('net_profit_attributable_to_owners'))
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


def load_results(symbols=None, directory=None, cliff_checker=None, restore_units=True, profit_basis='total'):
    """Point-in-time results table (see module docstring). `symbols`: optional iterable restricting the universe.
    `cliff_checker(symbol, start, end, ratio)`: optional price-based test (see _split_factor_per_period); when given, splits that the price vendor left unadjusted are not restored."""
    directory = directory or FUNDAMENTALS_DIR
    paths = sorted(glob.glob(os.path.join(directory, '*.json')))
    if symbols is not None:
        keep = set(symbols); paths = [p for p in paths if os.path.basename(p)[:-5] in keep]
    raw = []
    for p in paths:
        raw.extend(_read_symbol(p, profit_basis))
    if not raw:
        raise FileNotFoundError(f'no usable fundamentals JSON under {directory}')
    df = pd.DataFrame(raw)
    out = []
    for sym, g in df.groupby('symbol'):
        # company-level share count per period (the capital is the same under both bases), split-adjusted to today's units
        sh = g.groupby('period_end').shares.median().sort_index()
        filed_by_pe = g.groupby('period_end').filed.max()
        pes = list(sh.dropna().index)
        w_start = {pes[i]: pes[i - 1] for i in range(1, len(pes))}                       # the action happened between the previous period end ...
        w_end = {pe: filed_by_pe.get(pe, pe) + pd.Timedelta(days=20) for pe in pes}       # ... and shortly after the filing that first shows it
        chk = (lambda a, b, c, _s=sym: cliff_checker(_s, a, b, c)) if cliff_checker is not None else None
        adj = _split_factor_per_period(sh, w_start, w_end, chk) if restore_units else pd.Series(1.0, index=sh.dropna().index)   # restore_units=False reproduces the old (leaky) behaviour; ablation only
        shares_adj = (sh * adj)
        if adj.notna().all() and not (adj.min() >= CUM_FACTOR_BAND[0] and adj.max() <= CUM_FACTOR_BAND[1]):
            shares_adj = shares_adj * np.nan
        per_basis = {}
        bank = bool(g.is_bank.any())
        for basis, b in g.groupby('basis'):
            b = b.sort_values('period_end').drop_duplicates('period_end', keep='last')
            grid = pd.date_range(b.period_end.min(), b.period_end.max(), freq='QE')
            b = b.set_index('period_end').reindex(grid)
            tot, own = b['np_total'], b['np_owners']
            oi, exc, pbt = b['other_income'], b['exc'].fillna(0.0), b['pbt']
            if profit_basis == 'owners_consistent':
                # owners' profit only where all the quarters used by a figure report it; otherwise the total line for ALL of them (never a mix inside one figure)
                own4 = own.notna().rolling(4, min_periods=4).sum() == 4
                ttm = np.where(own4, own.rolling(4, min_periods=4).sum(), tot.rolling(4, min_periods=4).sum())
                use_own_g = own.notna() & own.shift(4).notna()
                q_now, q_old = own.where(use_own_g, tot), own.shift(4).where(use_own_g, tot.shift(4))
                ttm = pd.Series(ttm, index=b.index)
            elif profit_basis == 'core':
                # core profit: reported net profit less other income and exceptional items, taxed at a flat 25% (banks keep their reported profit)
                core = tot if bank else tot - (oi.fillna(0.0) + exc) * (1 - CORE_TAX)
                ttm = core.rolling(4, min_periods=4).sum()
                q_now, q_old = core, core.shift(4)
            else:
                npf = b['net_profit']
                ttm = npf.rolling(4, min_periods=4).sum()
                q_now, q_old = npf, npf.shift(4)
            o = pd.DataFrame(index=b.index)
            o['filed'] = b['filed']
            o['np_ttm'] = ttm
            o['sg_np'] = (q_now - q_old) / ((q_now.abs() + q_old.abs()) / 2).replace(0, np.nan)
            # share of trailing-12-month pre-tax profit that is other income or exceptional gain (0 for banks; NaN when TTM pre-tax profit is not positive)
            pbt_ttm = pbt.rolling(4, min_periods=4).sum()
            gains = oi.fillna(0.0).rolling(4, min_periods=4).sum() + exc.clip(lower=0.0).rolling(4, min_periods=4).sum()
            o['oneoff_share'] = 0.0 if bank else (gains / pbt_ttm.where(pbt_ttm > 0))
            o['basis'] = basis
            per_basis[basis] = o
        for basis in ('standalone', 'consolidated'):          # consolidated wins where it has a valid TTM
            if basis in per_basis:
                o = per_basis[basis].copy(); o['pref'] = 1 if basis == 'consolidated' else 0
                o['symbol'] = sym; o['period_end'] = o.index
                o['shares_adj'] = shares_adj.reindex(o.index).values
                out.append(o.reset_index(drop=True))
    r = pd.concat(out, ignore_index=True)
    r = r[r.filed.notna() & r.np_ttm.notna() & (r.shares_adj > 0) & ((r.filed - r.period_end).dt.days.between(0, MAX_FILING_LAG_DAYS))]
    r = r.sort_values(['symbol', 'period_end', 'pref']).drop_duplicates(['symbol', 'period_end'], keep='last')
    r = r.sort_values(['symbol', 'filed'])
    r = r[r.period_end >= r.groupby('symbol').period_end.cummax()]          # drop out-of-order late filings (causal: filing order)
    return r.drop(columns='pref').reset_index(drop=True)


def monthly_frame(results, col, dates, columns, max_age=140):
    """Wide frame (dates x columns): `col` from the latest result filed on/before each date, NaN once that result is older than max_age days."""
    out = {}
    cols = set(columns)
    for s, g in results.groupby('symbol'):
        if s not in cols:
            continue
        g = g.sort_values('filed').drop_duplicates('filed', keep='last')
        v = pd.Series(g[col].values, index=pd.DatetimeIndex(g['filed'].values))
        a = pd.Series(g['filed'].values, index=pd.DatetimeIndex(g['filed'].values))
        u = v.index.union(dates)
        vv = v.reindex(u, method='ffill').reindex(dates)
        aa = pd.to_datetime(a.reindex(u, method='ffill').reindex(dates))
        out[s] = vv.where((dates.to_series() - aa).dt.days <= max_age)
    return pd.DataFrame(out, index=dates).reindex(columns=columns)

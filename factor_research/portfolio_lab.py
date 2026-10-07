"""
portfolio_lab.py -- translate a monthly score into a simple long-only top-N book so that IC findings
can be sanity-checked in return space.  Deliberately minimal (equal weight, monthly rebalance, no
stops / regime overlays / hysteresis) so that differences between scores are due to the SCORE,
not to execution machinery.  Costs: `cost` one-way applied to replaced weight (live runs use 0.3%).
"""
import numpy as np
import pandas as pd

SPLIT = pd.Timestamp('2014-12-31')


def topn_book(score, mask, fwd1, n=15, cost=0.003):
    """score/mask/fwd1: monthly frames. Returns DataFrame[gross, net, turnover, ew_mkt]."""
    s = score.where(mask)
    r = fwd1.where(mask)
    rows = []
    prev = set()
    dates = [d for d in s.index if d in r.index]
    for d in dates:
        row = s.loc[d].dropna()
        ret = r.loc[d]
        row = row[ret.reindex(row.index).notna()]
        if len(row) < max(60, 3 * n):
            prev = set()
            continue
        pick = set(row.nlargest(n).index)
        gross = ret[list(pick)].clip(-0.9, 3.0).mean()
        turn = 1.0 - len(pick & prev) / n if prev else 1.0
        rows.append((d, gross, gross - 2 * cost * turn, turn, ret.clip(-0.9, 3.0).mean()))
        prev = pick
    out = pd.DataFrame(rows, columns=['date', 'gross', 'net', 'turnover', 'ew_mkt']).set_index('date')
    return out


def stats(ret, label='', rf_annual=0.06, periods=12):
    ret = ret.dropna()
    if len(ret) < 24:
        return {}
    eq = (1 + ret).cumprod()
    yrs = len(ret) / periods
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = ret.std() * np.sqrt(periods)
    rf_m = (1 + rf_annual) ** (1 / periods) - 1
    sharpe = (ret - rf_m).mean() / ret.std() * np.sqrt(periods) if ret.std() > 0 else np.nan
    dd = (eq / eq.cummax() - 1).min()
    return dict(cagr=cagr, vol=vol, sharpe=sharpe, maxdd=dd, calmar=cagr / abs(dd) if dd < 0 else np.nan,
                hit_vs_mkt=np.nan)


def book_report(book, label):
    out = {'label': label}
    for tag, sl in (('all', slice(None)), ('disc', book.index <= SPLIT), ('hold', book.index > SPLIT)):
        b = book[sl]
        st = stats(b['net'])
        if not st:
            continue
        out.update({f'{k}_{tag}': v for k, v in st.items() if k != 'hit_vs_mkt'})
        out[f'hit_vs_mkt_{tag}'] = (b['net'] > b['ew_mkt']).mean()
        out[f'excess_ann_{tag}'] = ((1 + b['net']).prod() ** (12 / len(b)) - 1) - ((1 + b['ew_mkt']).prod() ** (12 / len(b)) - 1)
    out['turnover'] = book['turnover'].mean()
    return out

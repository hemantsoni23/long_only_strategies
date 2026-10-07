"""index_lab.py -- research on index / ETF universes (sector rotation, asset-class rotation, factor-index rotation, timing).
Conventions as in evaluate.py: signal at month-end close t, entry/exit at close of t+1 (ETF T+1 fill proxy); cost one-way per unit turnover."""
import numpy as np, pandas as pd
from assets import load_indices, load_etfs
from evaluate import rank_ic, nw_tstat, SPLIT

CASH_ANNUAL = 0.06


def prep():
    I = load_indices()['close']
    cal = I['Nifty_50'].dropna().index
    I = I.reindex(cal).ffill(limit=5)
    E = load_etfs()
    Ec = E['close']; Ec.index = pd.to_datetime(Ec.index).normalize()
    Ec = Ec[~Ec.index.duplicated(keep='last')].reindex(cal).ffill(limit=5)
    Ev = E['volume']; Ev.index = pd.to_datetime(Ev.index).normalize()
    Ev = Ev[~Ev.index.duplicated(keep='last')].reindex(cal)
    return I, Ec, Ev, cal


def month_ends(cal):
    s = pd.Series(cal, index=cal)
    return pd.DatetimeIndex(s.groupby([cal.year, cal.month]).max().values)


def fwd_returns(C, cal, sig, horizons=(1, 3, 6)):
    """close(t+1 after sig[k+h]) / close(t+1 after sig[k]) - 1  (ffilled prices)"""
    pos = cal.get_indexer(sig); entry = pos + 1
    ok = entry < len(cal)
    C = C.reindex(cal)
    Cv = C.ffill().values
    out = {}
    for h in horizons:
        arr = np.full((len(sig), C.shape[1]), np.nan)
        for k in range(len(sig) - h):
            if ok[k] and ok[k + h]:
                arr[k] = Cv[entry[k + h]] / Cv[entry[k]] - 1
        out[h] = pd.DataFrame(arr, index=sig, columns=C.columns)
    return out


def rm(x, w, mp=0.8): return x.rolling(w, min_periods=int(w * mp))


def asset_factors(C, bench=None):
    """series-level versions of the stock factors (daily frame in, month-end frames out are taken by caller)"""
    r = C.pct_change(fill_method=None)
    f = {}
    f['mom_1m'] = C / C.shift(21) - 1
    f['mom_3_0'] = C / C.shift(63) - 1
    f['mom_6_1'] = C.shift(21) / C.shift(126) - 1
    f['mom_12_1'] = C.shift(21) / C.shift(252) - 1
    f['mom_6_0'] = C / C.shift(126) - 1
    f['mom_12_0'] = C / C.shift(252) - 1
    f['sharpe_6_1'] = f['mom_6_1'] / rm(r, 126).std()
    f['sharpe_12_1'] = f['mom_12_1'] / rm(r, 252).std()
    f['hi_252'] = C / rm(C, 252).max()
    sma50 = rm(C, 50).mean()
    ab = (C > sma50).where(C.notna() & sma50.notna()).astype('float64')
    f['q5_126'] = ab.rolling(126, min_periods=100).mean()
    f['q5_63'] = ab.rolling(63, min_periods=50).mean()
    f['dist_sma200'] = C / rm(C, 200).mean() - 1
    f['lowvol_126'] = -rm(r, 126).std()
    f['low_ulcer_126'] = -np.sqrt(rm((C / rm(C, 126).max() - 1) ** 2, 126).mean())
    f['rev_1m'] = -(C / C.shift(21) - 1)
    if bench is not None:
        rs = C.div(bench, axis=0)
        f['rs_3_0'] = rs / rs.shift(63) - 1
        f['rs_6_1'] = rs.shift(21) / rs.shift(126) - 1
        f['rs_near_high'] = rs / rm(rs, 252).max()
    return f


def ic_table(F, FWD, min_n=8, horizons=(1, 3, 6)):
    rows = []
    for n, fr in F.items():
        row = {'factor': n}
        for h in horizons:
            ic, cnt = rank_ic(fr, FWD[h], min_n=min_n)
            ic = ic.dropna()
            if len(ic) < 24: continue
            mu, sd = ic.mean(), ic.std()
            row.update({f'ic_{h}': mu, f'icir_{h}': mu / sd, f'hit_{h}': (ic > 0).mean(), f't_{h}': nw_tstat(ic, max(h - 1, 0)),
                        f'ic_disc_{h}': ic[ic.index <= SPLIT].mean(), f'ic_hold_{h}': ic[ic.index > SPLIT].mean()})
            row['n_months'] = len(ic); row['avg_n'] = float(cnt[ic.index].mean())
        rows.append(row)
    return pd.DataFrame(rows).set_index('factor')


def stats(ret, periods=12, rf=CASH_ANNUAL):
    ret = ret.dropna()
    eq = (1 + ret).cumprod(); yrs = len(ret) / periods
    cagr = eq.iloc[-1] ** (1 / yrs) - 1
    vol = ret.std() * np.sqrt(periods)
    rfm = (1 + rf) ** (1 / periods) - 1
    sh = (ret - rfm).mean() / ret.std() * np.sqrt(periods)
    dd = (eq / eq.cummax() - 1).min()
    return dict(cagr=cagr, vol=vol, sharpe=sh, maxdd=dd, calmar=cagr / abs(dd) if dd < 0 else np.nan, months=len(ret))


def run_book(score, fwd1, k=3, cost=0.001, abs_filter=None, cash_m=None, label=''):
    """top-k equal-weight of assets by score each month. abs_filter: frame of bool (asset eligible). Unfilled slots -> cash."""
    rets, prev = [], {}
    for d in score.index:
        if d not in fwd1.index: continue
        s = score.loc[d].dropna()
        if abs_filter is not None:
            s = s[abs_filter.loc[d].reindex(s.index).fillna(False)]
        r1 = fwd1.loc[d]
        s = s[r1.reindex(s.index).notna()]
        if score.loc[d].dropna().empty or r1.dropna().empty: continue
        pick = list(s.nlargest(k).index)
        w = {a: 1.0 / k for a in pick}
        cm = cash_m.loc[d] if cash_m is not None and d in cash_m.index else (1 + CASH_ANNUAL) ** (1 / 12) - 1
        gross = sum(w[a] * r1[a] for a in pick) + (1 - sum(w.values())) * cm
        names = set(w) | set(prev)
        turn = sum(abs(w.get(a, 0) - prev.get(a, 0)) for a in names)
        rets.append((d, gross - cost * turn, turn))
        prev = w
    df = pd.DataFrame(rets, columns=['date', 'net', 'turn']).set_index('date')
    return df

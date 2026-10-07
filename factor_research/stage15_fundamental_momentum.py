"""
stage15_fundamental_momentum.py -- literature-driven test: earnings / fundamental momentum x price momentum.

Why: the momentum literature in ../momentum/ (Griffin-Ji-Martin 2005, Chan-Jegadeesh-Lakonishok 1996 via Da-Liu-Schaumburg,
Novy-Marx 2012/'Fundamental momentum', Asness 1997, Sadka 2006) says price momentum and earnings momentum are related but not
redundant (time-series corr < 0.4) and that the combination roughly doubles the univariate spread. Every OHLCV factor tested so far
is 0.6-0.9 correlated with the live books; fundamentals are the only source in the user's data that is plausibly orthogonal.

Data: ../upstox_data_folder/pit_harness/cache/facts_quarterly.parquet  (NSE XBRL quarterly results with `filed_date`; period_end
2018Q1..2024Q4).  A quarter is usable only from its filed_date (signal at month-end t needs filed_date <= t; entry t+1 close, as in all
other stages).  Seasonal-difference signals need 8 quarters of history => first usable signal ~mid-2020.  Fundamentals stop at 2024Q4
(filed ~Feb-2025), so the test window is 2020-06 .. ~2025-03 (~58 monthly signals): SHORT and one regime. Treat as a screen.

Signals (all point-in-time):
  sue_eps      (EPS_q - EPS_q-4) / std(prior 4-8 seasonal diffs)            Chan-Jegadeesh-Lakonishok SUE
  sue_np       same on net profit
  sg_np        symmetric yoy growth of net profit  (np-np4)/((|np|+|np4|)/2)
  surge_rev    revenue seasonal-diff / std                                    revenue surprise
  dm_ebit      yoy change in EBIT margin (pp)
  dm_net       yoy change in net margin
  accel_np     sg_np - sg_np(prev quarter)                                    earnings acceleration
  em_ttm_p     sum of last 4 seasonal EPS diffs / price                       Novy-Marx earnings momentum (price-scaled)
  ear3         announcement return: close[d-1]->close[d+2] around filing, less equal-weight market
  ep_ttm       TTM EPS / price                                                value proxy
  d_fii4, d_dii4, d_prom4   4-quarter change in FII / DII / promoter holding  (visible at sh_filed)
  *_fresh      same signal only within 75 days of filing (PEAD drift window)
"""
import os
import pickle
import warnings

import numpy as np
import pandas as pd

from data import load_panels
from evaluate import composite, zscore, rank_ic, nw_tstat, winsor_rows
from portfolio_lab import topn_book, stats

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = '/Users/hemantsoni/Documents/upstox_data_folder/pit_harness/cache/facts_quarterly.parquet'
MAX_AGE = 140          # days a quarter's number stays "current"
FRESH = 75
START = pd.Timestamp('2020-06-01')
HOLD = pd.Timestamp('2023-01-01')


# ───────────────────────────── per-quarter features ─────────────────────────────
def pick_basis(f):
    n = f.groupby(['symbol', 'basis']).size().unstack(fill_value=0)
    n['pick'] = np.where(n.get('consolidated', 0) >= n.get('standalone', 0), 'consolidated', 'standalone')
    keep = n['pick'].reset_index().rename(columns={'pick': 'basis'})
    return f.merge(keep, on=['symbol', 'basis'])


def sym_growth(a, b):
    return (a - b) / ((a.abs() + b.abs()) / 2).replace(0, np.nan)


def seasonal_surprise(x):
    d4 = x - x.shift(4)
    sd = d4.shift(1).rolling(8, min_periods=4).std()
    return d4 / sd.where(sd > 0)


def quarter_features(g):
    g = g.sort_values('period_end').drop_duplicates('period_end', keep='last')
    grid = pd.date_range(g.period_end.min(), g.period_end.max(), freq='QE')
    g = g.set_index('period_end').reindex(grid)
    o = pd.DataFrame(index=g.index)
    o['filed'] = g['filed_date']
    eps, npf, rev, ebit = g['eps'], g['net_profit'], g['revenue'], g['ebit']
    o['sue_eps'] = seasonal_surprise(eps)
    o['sue_np'] = seasonal_surprise(npf)
    o['sg_np'] = sym_growth(npf, npf.shift(4))
    o['surge_rev'] = seasonal_surprise(rev)
    o['dm_ebit'] = ebit / rev.replace(0, np.nan) - (ebit / rev.replace(0, np.nan)).shift(4)
    o['dm_net'] = npf / rev.replace(0, np.nan) - (npf / rev.replace(0, np.nan)).shift(4)
    o['accel_np'] = o['sg_np'] - o['sg_np'].shift(1)
    d4 = eps - eps.shift(4)
    o['dEPS_ttm'] = d4.rolling(4, min_periods=4).sum()
    o['eps_ttm'] = eps.rolling(4, min_periods=4).sum()
    o['np_ttm'] = npf.rolling(4, min_periods=4).sum()
    o['rev_ttm'] = rev.rolling(4, min_periods=4).sum()
    o['ebit_ttm'] = ebit.rolling(4, min_periods=4).sum()
    o['shares'] = g['shares_out']
    o['equity'] = g['equity']
    for c in ('fii_pct', 'dii_pct', 'promoter_pct'):
        o[c] = g[c]
    o['d_fii4'] = g['fii_pct'] - g['fii_pct'].shift(4)
    o['d_dii4'] = g['dii_pct'] - g['dii_pct'].shift(4)
    o['d_prom4'] = g['promoter_pct'] - g['promoter_pct'].shift(4)
    o['sh_filed'] = g['sh_filed']
    return o


def build_quarter_table():
    f = pd.read_parquet(FACTS)
    f = pick_basis(f)
    rows = []
    for s, g in f.groupby('symbol'):
        o = quarter_features(g)
        o['symbol'] = s
        o['period_end'] = o.index
        rows.append(o.reset_index(drop=True))
    q = pd.concat(rows, ignore_index=True)
    q = q[q.filed.notna() & ((q.filed - q.period_end).dt.days.between(0, 120))]
    return q


# ───────────────────────────── announcement returns ─────────────────────────────
def announcement_returns(q, C, bench_ret):
    idx = C.index
    lc = C.ffill()
    bc = (1 + bench_ret).cumprod().values
    col = {s: i for i, s in enumerate(C.columns)}
    out = np.full(len(q), np.nan)
    f = q.filed.values
    syms = q.symbol.values
    pos = idx.searchsorted(f)                      # first trading day >= filing date
    Cv = lc.values
    for k in range(len(q)):
        j = col.get(syms[k])
        if j is None:
            continue
        a, b = pos[k] - 1, pos[k] + 2
        if a < 0 or b >= len(idx):
            continue
        p0, p1 = Cv[a, j], Cv[b, j]
        if not (p0 > 0 and p1 > 0):
            continue
        r = p1 / p0 - 1
        if r < -0.6 or r > 2.0:
            continue
        out[k] = r - (bc[b] / bc[a] - 1)
    return out


# ───────────────────────────── to monthly PIT frames ─────────────────────────────
def to_monthly(q, col, sig, vis_col='filed', max_age=MAX_AGE, fresh=None):
    cols = {}
    for s, g in q.groupby('symbol'):
        g = g[g[col].notna() & g[vis_col].notna()].sort_values(vis_col)
        if g.empty:
            continue
        g = g[g.period_end >= g.period_end.cummax()]       # drop out-of-order late filings
        g = g.drop_duplicates(vis_col, keep='last')
        v = pd.Series(g[col].values, index=pd.DatetimeIndex(g[vis_col].values))
        age_src = pd.Series(g[vis_col].values, index=pd.DatetimeIndex(g[vis_col].values))
        u = v.index.union(sig)
        vv = v.reindex(u, method='ffill').reindex(sig)
        aa = age_src.reindex(u, method='ffill').reindex(sig)
        age = (sig.to_series() - pd.to_datetime(aa)).dt.days
        lim = fresh if fresh else max_age
        vv = vv.where(age <= lim)
        cols[s] = vv
    return pd.DataFrame(cols, index=sig)


# ───────────────────────────── evaluation helpers ─────────────────────────────
def eval_sig(name, S, mask, FWD, base=None, uname=''):
    row = {'universe': uname, 'signal': name}
    Sm = S.where(mask)
    row['avg_n'] = Sm.loc[Sm.index >= START].notna().sum(axis=1).replace(0, np.nan).mean()
    for h in (1, 2, 3, 6):
        ic, _ = rank_ic(Sm, FWD[h].where(mask))
        ic = ic[(ic.index >= START)].dropna()
        if len(ic) < 12:
            continue
        row[f'ic{h}'] = ic.mean(); row[f'icir{h}'] = ic.mean() / ic.std()
        row[f'hit{h}'] = (ic > 0).mean(); row[f't{h}'] = nw_tstat(ic, max(h - 1, 0))
        if h == 3:
            row['ic3_a'] = ic[ic.index < HOLD].mean(); row['ic3_b'] = ic[ic.index >= HOLD].mean()
            row['n_months'] = len(ic)
            valid = Sm.notna() & FWD[3].where(mask).notna()
            R = winsor_rows(FWD[3].where(valid))
            ex = R.sub(R.mean(axis=1), axis=0)
            pct = Sm.where(valid).rank(axis=1, pct=True)
            t20 = ex.where(pct > 0.8).mean(axis=1)[ic.index].dropna()
            row['top20_ex3'] = t20.mean(); row['top20_beat_mkt'] = (t20 > 0).mean()
    if base is not None:
        bc, _ = rank_ic(Sm, base.where(mask))
        row['corr_elendel'] = bc[bc.index >= START].mean()
        fp = Sm.rank(axis=1, pct=True); bp = base.where(mask).rank(axis=1, pct=True)
        fz = fp.sub(fp.mean(axis=1), axis=0); bz = bp.sub(bp.mean(axis=1), axis=0)
        beta = (fz * bz).sum(axis=1) / (bz ** 2).sum(axis=1)
        res = fz.sub(bz.mul(beta, axis=0))
        for h in (3, 6):
            ic_r, _ = rank_ic(res, FWD[h].where(mask))
            ic_r = ic_r[ic_r.index >= START].dropna()
            row[f'inc_ic{h}'] = ic_r.mean(); row[f'inc_t{h}'] = nw_tstat(ic_r, h - 1)
    return row


def main():
    st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
    sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
    P = load_panels()
    C = P['close']
    print('[s15] building quarter features ...', flush=True)
    q = build_quarter_table()
    q = q[q.symbol.isin(C.columns)].reset_index(drop=True)
    print(f'[s15] {len(q)} quarter rows, {q.symbol.nunique()} symbols', flush=True)
    q['ear3'] = announcement_returns(q, C, P['bench_ret'])

    sigs = {}
    for c in ('sue_eps', 'sue_np', 'sg_np', 'surge_rev', 'dm_ebit', 'dm_net', 'accel_np', 'ear3'):
        sigs[c] = to_monthly(q, c, sig)
        sigs[c + '_fresh'] = to_monthly(q, c, sig, fresh=FRESH)
    Cm = C.ffill().reindex(sig)
    de = to_monthly(q, 'dEPS_ttm', sig); et = to_monthly(q, 'eps_ttm', sig)
    sigs['em_ttm_p'] = (de / Cm).replace([np.inf, -np.inf], np.nan)
    sigs['ep_ttm'] = (et / Cm).replace([np.inf, -np.inf], np.nan)
    for c in ('d_fii4', 'd_dii4', 'd_prom4'):
        sigs[c] = to_monthly(q, c, sig, vis_col='sh_filed', max_age=200)
    # composite fundamental momentum (z-average of the surprise family, computed per universe later)
    sigs = {k: v.reindex(columns=C.columns) for k, v in sigs.items()}
    pickle.dump(sigs, open(os.path.join(HERE, '.cache', 'stage15_sigs.pkl'), 'wb'))

    rows = []
    for un in ('U1_liquid1000', 'U3_top300', 'U2_live_trend'):
        mask = U[un]
        base = composite(F, ['a3_rs_high', 'q5_126'], mask)
        for k, S in sigs.items():
            rows.append(eval_sig(k, S, mask, FWD, base, un))
        for k in ('mom_12_1', 'q5_126', 'a3_rs_high'):
            rows.append(eval_sig('PRICE:' + k, F[k], mask, FWD, base, un))
        rows.append(eval_sig('PRICE:elendel_base', base, mask, FWD, None, un))
        fam = (zscore(sigs['sue_eps'].where(mask)) + zscore(sigs['surge_rev'].where(mask)) + zscore(sigs['dm_ebit'].where(mask))
               + zscore(sigs['ear3'].where(mask)))
        rows.append(eval_sig('FUND_composite(sue_eps+surge_rev+dm_ebit+ear3)', fam, mask, FWD, base, un))
    res = pd.DataFrame(rows)
    res.to_csv(os.path.join(HERE, 'results', 'stage15_fund_ic.csv'), index=False, float_format='%.4f')
    pd.set_option('display.width', 250, 'display.max_columns', 40, 'display.max_rows', 200)
    cols = ['signal', 'avg_n', 'n_months', 'ic3', 'icir3', 'hit3', 't3', 'ic3_a', 'ic3_b', 'ic1', 'ic6', 'top20_ex3', 'corr_elendel', 'inc_ic3', 'inc_t3']
    for un in ('U1_liquid1000', 'U3_top300'):
        print('\n=====', un)
        print(res[res.universe == un][cols].round(3).to_string(index=False))


if __name__ == '__main__':
    main()

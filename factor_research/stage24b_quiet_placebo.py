"""stage24b -- post-look #1/#2 of NEW_MOMENTUM_AUDIT_PREREG.md.
 (1) placebo for quiet_mom_12_1: trend/(1+clip(permuted surge)) vs the real thing, proxy top-15 book (U2), bases TRUE Elendel / Zenith.
 (2) open-price sanity: per-stock mean overnight / intraday log return (annualised) by liquidity tier."""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from stage24_new_factor_audit import load_factors
from evaluate import composite, zscore, SPLIT
from portfolio_lab import topn_book, stats

sig, ALL, FWD, U = load_factors()
m = U['U2_live_trend']
trend = ALL['mom_12_1'].where(m)
surge = ALL['volsurge_21_252'].where(m).clip(0.2, 5.0)
elen = composite(ALL, ['a3_rs_high', 'q5_126'], m); zen = composite(ALL, ['a1_52wh', 'q5_189'], m)
bases = {'elen': elen, 'zen': zen}


def evalsc(score):
    out = {}
    bk = topn_book(score, m, FWD[1]); n = bk['net']
    out['stand_all'] = stats(n).get('sharpe'); out['stand_hold'] = stats(n[n.index > SPLIT]).get('sharpe')
    for bn, b in bases.items():
        for w in (0.5, 1.0):
            sc = zscore(b) + w * zscore(score)
            k = topn_book(sc, m, FWD[1])['net']
            out[f'{bn}_w{w}_all'] = stats(k).get('sharpe'); out[f'{bn}_w{w}_hold'] = stats(k[k.index > SPLIT]).get('sharpe')
            out[f'{bn}_w{w}_disc'] = stats(k[k.index <= SPLIT]).get('sharpe')
    return out


real = evalsc(trend / (1 + surge))
rng = np.random.default_rng(11)
rows = []
vals = surge.values
for d in range(60):
    perm = np.empty_like(vals)
    for i in range(vals.shape[0]):
        row = vals[i]; ok = ~np.isnan(row); p = row.copy(); p[ok] = rng.permutation(row[ok]); perm[i] = p
    S = pd.DataFrame(perm, index=surge.index, columns=surge.columns)
    rows.append(evalsc(trend / (1 + S)))
    if (d + 1) % 20 == 0: print(f'placebo {d+1}/60', flush=True)
pl = pd.DataFrame(rows)
summ = pd.DataFrame({'real': pd.Series(real), 'placebo_mean': pl.mean(), 'placebo_p95': pl.quantile(0.95),
                     'p_value(placebo>=real)': (pl >= pd.Series(real)).mean()})
summ.to_csv(os.path.join(HERE, 'results', 'stage24b_quiet_placebo.csv'), float_format='%.4f')
print(summ.round(3).to_string())

# plain-trend and sharpe-trend reference
print('\nreference (same metrics):')
ref = pd.DataFrame({'mom_12_1': evalsc(trend), 'mom_12_1_sharpe': evalsc(ALL['mom_12_1_sharpe'].where(m))})
print(ref.round(3).to_string())

# ---- (2) open-price sanity
from data import load_panels
P = load_panels(); O, C = P['open'], P['close']
ovn = np.log(O / C.shift(1)).clip(-0.15, 0.15); intr = np.log(C / O).clip(-0.15, 0.15)
rank_dv = (C * P['volume']).rolling(63, min_periods=40).median().iloc[-60:].mean().rank(ascending=False)
last = O.iloc[-756:]
mo = ovn.iloc[-756:].mean() * 252; mi = intr.iloc[-756:].mean() * 252
eq_open_prev = ((O == C.shift(1)).iloc[-756:]).mean(); eq_open_close = ((O == C).iloc[-756:]).mean()
tiers = pd.cut(rank_dv, [0, 300, 1000, 2000, 6000], labels=['1-300', '301-1000', '1001-2000', '2000+'])
df = pd.DataFrame({'ovn_ann': mo, 'intr_ann': mi, 'open==prevclose': eq_open_prev, 'open==close': eq_open_close, 'tier': tiers}).dropna()
print('\nOpen-price sanity, last 3y, by liquidity tier (mean across stocks of per-stock annualised log returns; sd across stocks)')
print(df.groupby('tier').agg(n=('ovn_ann', 'size'), ovn_mean=('ovn_ann', 'mean'), ovn_sd=('ovn_ann', 'std'), intr_mean=('intr_ann', 'mean'), intr_sd=('intr_ann', 'std'),
                            open_eq_prevclose=('open==prevclose', 'mean'), open_eq_close=('open==close', 'mean')).round(3).to_string())
print('corr across stocks of per-stock mean overnight vs mean intraday:', round(df['ovn_ann'].corr(df['intr_ann']), 3))

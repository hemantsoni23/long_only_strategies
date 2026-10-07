"""
stage17_more_literature.py -- four more ideas from the momentum/ folder that stage15/16 did not cover.

 A. Aggregate-liquidity state (Avramov-Cheng-Hameed 2016): momentum is WEAKER after illiquid market states.
    market illiquidity = cross-sectional median of log Amihud (21d) over the liquid-1000 universe, state = lagged value vs its expanding
    67th percentile.  Tested as conditional IC / proxy-book return of the Elendel score, and as an exposure rule on the real engine returns.
 B. Dispersion state (du Plessis 2013; Daniel-Moskowitz): cross-sectional dispersion of 12-1 returns as a state variable (same tests).
 C. Factor momentum (Ehsani-Linnainmaa 2017; Arnott et al.): follow the factors that worked over the trailing 12 months.
    All 122 factors in `state.pkl`, top-K by trailing-12m top-minus-bottom-quintile spread (only spreads already realised at t), z-score sum.
 D. Size / low-coverage (Hong-Lim-Stein 2000 'Bad News Travels Slowly'; also GJM 2005): momentum by liquidity tier, including tiers BELOW the
    live universe (ranks 1000-2000).
Full sample 2003-2026 for A/B/C/D (price-only, no fundamentals needed).
"""
import os, sys, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/momentum_gold')
from gold_idle_cash import GoldIdleCashOverlay
from data import load_panels
from evaluate import composite, zscore, rank_ic, nw_tstat, winsor_rows
from portfolio_lab import topn_book, stats

HERE = os.path.dirname(os.path.abspath(__file__)); M = GoldIdleCashOverlay.metrics
pd.set_option('display.width', 250, 'display.max_columns', 40)
st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb')); sig, F, FWD, U = st['sig'], st['F'], st['FWD'], st['U']
P = load_panels(); C = P['close']; V = P['volume']
U1 = U['U1_liquid1000']
base = composite(F, ['a3_rs_high', 'q5_126'], U1)
ic3, _ = rank_ic(base.where(U1), FWD[3].where(U1)); ic3 = ic3.dropna()
bk = topn_book(base, U1, FWD[1], n=15)                      # proxy book, monthly net returns
print(f'proxy Elendel book (U1) {bk.index[0].date()}..{bk.index[-1].date()}  Sharpe {stats(bk["net"])["sharpe"]:.2f}  IC3 {ic3.mean():.3f}')

def state_table(name, s, lo_q=1/3, hi_q=2/3):
    """s: monthly state series (value known at month-end t). Expanding terciles (no look-ahead)."""
    s = s.reindex(sig)
    lo = s.expanding(36).quantile(lo_q).shift(1); hi = s.expanding(36).quantile(hi_q).shift(1)
    lab = pd.Series(np.where(s > hi, 'high', np.where(s < lo, 'low', 'mid')), index=sig).where(s.notna() & hi.notna())
    rows = []
    for k in ('low', 'mid', 'high'):
        m = lab == k
        b = bk['net'][bk.index.isin(m[m].index)]; i = ic3[ic3.index.isin(m[m].index)]
        rows.append({'state': f'{name}={k}', 'months': len(b), 'IC3': i.mean(), 'hit3': (i > 0).mean(),
                     'book_ret_pm%': b.mean() * 100, 'book_sharpe': stats(b)['sharpe'] if len(b) >= 24 else np.nan,
                     'mkt_pm%': bk['ew_mkt'][b.index].mean() * 100})
    return pd.DataFrame(rows), lab

# ───────────── A. aggregate illiquidity
ret = C.ffill().pct_change(fill_method=None).abs().where(lambda x: x < 0.4)
amihud = (ret / (C * V).replace(0, np.nan)).rolling(21, min_periods=15).mean()
am_m = amihud.reindex(sig)
mkt_ill = np.log(am_m.where(U1)).median(axis=1)
tab, labA = state_table('mkt_illiq', mkt_ill)
print('\n=== A. aggregate illiquidity state (lagged), proxy Elendel book + IC3'); print(tab.round(3).to_string(index=False))

# ───────────── B. dispersion
mom = F['mom_12_1']
disp = mom.where(U1).std(axis=1) / mom.where(U1).abs().median(axis=1)
tabB, labB = state_table('xs_dispersion', disp)
print('\n=== B. cross-sectional dispersion of 12-1 returns'); print(tabB.round(3).to_string(index=False))
mret = P['bench_ret']
mvol = mret.rolling(63).std().reindex(sig) * np.sqrt(252)
tabV, labV = state_table('mkt_vol63', mvol)
print('\n=== (reference) market volatility state'); print(tabV.round(3).to_string(index=False))

# engine rule: halve exposure when illiquidity state is high (state at month-end applies from the next day)
lf = 1.065 ** (1 / 252) - 1
print('\n=== A/B on REAL engine returns (2005+): exposure 50% when lagged state is high, remainder in liquid fund')
for name in ('elendel', 'zenith', 'quad'):
    r = pickle.load(open(f'/Users/hemantsoni/Documents/long_only_strategies/momentum_gold/.cache/engine_{name}.pkl', 'rb'))['net_returns'].loc['2005-01-01':]
    out = {'engine as is': r}
    for nm, lab in (('illiq high', labA), ('dispersion high', labB), ('mkt-vol high', labV)):
        d = (lab == 'high').reindex(r.index.union(lab.index)).ffill().shift(1).reindex(r.index).fillna(False).astype(bool)
        s = pd.Series(np.where(d, 0.5, 1.0), index=r.index)
        out[f'50% when {nm} ({d.mean():.0%} of days)'] = r * s + (1 - s) * lf
    print(f'\n{name.upper()}')
    mb = M(r)
    for k, v in out.items():
        m = M(v); print(f"  {k:<44} CAGR {m['cagr']*100:5.1f}%  Sharpe {m['sharpe']:5.2f}  MaxDD {m['max_drawdown']*100:6.1f}%")

# ───────────── C. factor momentum
print('\n=== C. factor momentum (122 factors, U1)')
names = list(F.keys())
R1 = winsor_rows(FWD[1].where(U1))
spread = {}
for n in names:
    s = F[n].where(U1); pct = s.rank(axis=1, pct=True)
    top = R1.where(pct > 0.8).mean(axis=1); bot = R1.where(pct <= 0.2).mean(axis=1)
    spread[n] = (top - bot)
spread = pd.DataFrame(spread)                         # row s = spread realised over the month AFTER signal date s
trail = spread.shift(1).rolling(12, min_periods=12).mean()      # at t: spreads of signals s<=t-1 (realised by t)
Z = {n: zscore(F[n].where(U1)) for n in names}
rows = []
for K in (3, 5, 10, 20):
    sc = pd.DataFrame(0.0, index=sig, columns=base.columns)
    for d in sig:
        if d not in trail.index or trail.loc[d].notna().sum() < 50: sc.loc[d] = np.nan; continue
        pick = trail.loc[d].dropna().nlargest(K).index
        acc = None
        for n in pick:
            z = Z[n].loc[d]
            acc = z if acc is None else acc.add(z, fill_value=0)
        sc.loc[d] = acc
    sc = sc.where(U1)
    r = {'K': K}
    for h in (1, 3, 6):
        ic, _ = rank_ic(sc, FWD[h].where(U1)); ic = ic.dropna(); r[f'IC{h}'] = ic.mean()
        if h == 3: r['ICIR3'] = ic.mean() / ic.std(); r['hit3'] = (ic > 0).mean(); r['t3'] = nw_tstat(ic, 2); r['n'] = len(ic)
    b = topn_book(sc, U1, FWD[1], n=15); b0 = bk[bk.index.isin(b.index)]
    s1, s0 = stats(b['net']), stats(b0['net']); d = (b['net'] - b0['net']).dropna()
    r.update({'book_cagr': s1['cagr'], 'book_sharpe': s1['sharpe'], 'base_sharpe': s0['sharpe'], 'maxdd': s1['maxdd'], 'turnover': b['turnover'].mean(),
              'd_t_vs_base': d.mean() / (d.std() / np.sqrt(len(d)))})
    for tag, sl in (('disc', b.index <= '2014-12-31'), ('hold', b.index > '2014-12-31')):
        r[f'sharpe_{tag}'] = stats(b['net'][sl]).get('sharpe', float('nan'))
    rows.append(r)
base_sub = bk[bk.index >= trail.dropna(how='all').index[0]]
print(pd.DataFrame(rows).round(3).to_string(index=False))
print(f"base Elendel proxy over same dates: Sharpe {stats(base_sub['net'])['sharpe']:.2f}  disc {stats(base_sub['net'][base_sub.index<='2014-12-31'])['sharpe']:.2f}  hold {stats(base_sub['net'][base_sub.index>'2014-12-31'])['sharpe']:.2f}")
# how often does it pick the Elendel legs / what does it pick (last 24 months)
last = trail.dropna(how='all').iloc[-1].nlargest(10)
print('top-10 factors by trailing-12m spread at the last date:', ', '.join(f'{k}({v*100:.1f}%)' for k, v in last.items()))

# ───────────── D. liquidity tiers incl. below the live universe
print('\n=== D. momentum by liquidity tier (Elendel score; tiers below rank 1000 are OUTSIDE the live universe)')
dv = (C * V).rolling(63, min_periods=21).median().shift(1).reindex(sig)
rk = dv.rank(axis=1, ascending=False, method='min')
Cs = C.ffill().reindex(sig)
circ = ((P['high'] == P['low']) & P['high'].notna()).astype('float64').rolling(63, min_periods=1).sum().shift(1).reindex(sig)
ok = (Cs > 20) & (circ <= 5) & Cs.notna()
trend = (Cs > C.ffill().rolling(200).mean().reindex(sig))
rows = []
for lab, lo_, hi_ in (('1-300', 0, 300), ('301-600', 300, 600), ('601-1000', 600, 1000), ('1001-1500', 1000, 1500), ('1501-2000', 1500, 2000), ('1001-2000', 1000, 2000)):
    m = ok & (rk > lo_) & (rk <= hi_)
    b_ = composite(F, ['a3_rs_high', 'q5_126'], m)
    mt = m & trend
    r = {'tier': lab, 'names': m.sum(axis=1).mean()}
    ic, _ = rank_ic(b_.where(m), FWD[3].where(m)); ic = ic.dropna(); r.update({'IC3': ic.mean(), 'ICIR3': ic.mean() / ic.std(), 'hit3': (ic > 0).mean(), 't3': nw_tstat(ic, 2)})
    b = topn_book(b_, mt, FWD[1], n=15)
    s1 = stats(b['net']); r.update({'top15_cagr': s1.get('cagr'), 'sharpe': s1.get('sharpe'), 'maxdd': s1.get('maxdd'), 'excess_vs_tier_mkt_pm%': (b['net'] - b['ew_mkt']).mean() * 100})
    for tag, sl in (('disc', b.index <= '2014-12-31'), ('hold', b.index > '2014-12-31')):
        r[f'sharpe_{tag}'] = stats(b['net'][sl]).get('sharpe', float('nan'))
    rows.append(r)
print(pd.DataFrame(rows).round(3).to_string(index=False))
print('(tier market = equal-weight of the tier names; capacity is not modelled: ADV falls ~10x by rank 1500)')

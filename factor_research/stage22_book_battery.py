"""
stage22_book_battery.py -- executes the gates pre-registered in INDUSTRY_BOOK_PREREG.md for the primary spec D1 (and reports its
pre-registered neighbours).  Nothing here is tuned: D1 is fixed, every sweep value was named in advance, every cell is reported.

Run:  python3 stage22_book_battery.py        (about a minute)    -> results/stage22_*.csv, results/stage22_book_battery.txt
"""
import os
import sys
import warnings
from dataclasses import replace

import numpy as np
import pandas as pd
from scipy.stats import norm

warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from industry_book import Spec, load_book_data, metrics, run, simulate, window, vol_overlay   # noqa: E402
from industry_lib import permute_within                                        # noqa: E402

RES = os.path.join(HERE, 'results')
os.makedirs(RES, exist_ok=True)
OUT = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    OUT.append(s)


bd = load_book_data()
VT = float(os.environ.get('VT', '0'))
SUF = '' if VT == 0 else '_vt%d' % round(VT * 100)
D1 = Spec(vol_target=VT)
P('SPEC UNDER TEST: D1 with vol_target =', VT, '(0 = base D1)')
res0 = run(bd, D1, track_episodes=True)
W0 = res0['ret'].index[0] + pd.DateOffset(months=D1.H)           # first date with all H tranches built
HALF = pd.Timestamp('2012-12-31')
END = res0['ret'].index[-1]
faith = pd.read_csv(os.path.join(os.path.dirname(HERE), 'csm_value', 'output', 'faithful_engine_returns.csv'), index_col=0, parse_dates=True)
TRIO = faith[['elendel_faithful', 'zenith_faithful', 'quad_faithful']].mean(axis=1)
TRIALS = []                                                      # (label, monthly Sharpe) of every book cell evaluated


def perf(r, a=None, b=None):
    rr = window(r, a if a is not None else W0, b)
    m0, m6 = metrics(rr, 0.0), metrics(rr, 0.06)
    return dict(cagr=m0['cagr'], vol=m0['vol'], sharpe=m0['sharpe'], sharpe6=m6['sharpe'], maxdd=m0['maxdd'], calmar=m0['calmar'])


def monthly(r):
    return (1 + window(r, W0)).resample('ME').prod() - 1


def cell(label, sp, **kw):
    res = run(bd, sp, **kw)
    r = res['ret']
    mr = monthly(r)
    TRIALS.append((label, mr.mean() / mr.std()))
    p = perf(r)
    p.update(names=res['info'].names.mean(), expo=res['info'].exposure.mean(), turn_yr=res['info'].turnover_oneway.mean() * 1200)
    return res, p


def fmt(p):
    return (f"CAGR {p['cagr']*100:5.1f}%  vol {p['vol']*100:4.1f}%  Sharpe {p['sharpe']:.2f} (rf6 {p['sharpe6']:.2f})  MaxDD {p['maxdd']*100:6.1f}%  Calmar {p['calmar']:.2f}")


# ───────── 1. headline + benchmarks (identical accounting) ─────────
P('=' * 110); P('1. HEADLINE, window', W0.date(), '->', END.date(), '(D1 fully built); A = to 2012-12-31, B = 2013-01-01 onward'); P('=' * 110)
rows = []
specs = {'D1 core (L3,n8,m2,H6)': D1,
         'D2 focused (L3,n5,m2,H3)': replace(D1, n_ind=5, H=3),
         'D3 slow (L6,n8,m2,H6)': replace(D1, L=6),
         'EW pool U2 + gate': replace(D1, mode='ew_pool'),
         'EW pool U2 no gate': replace(D1, mode='ew_pool', gate=False),
         'EW pool U1 no gate': replace(D1, mode='ew_pool', gate=False, pool='U1_liquid1000')}
rets = {}
for nm, sp in specs.items():
    res, p = cell('headline:' + nm, sp)
    rets[nm] = res['ret']
    for tag, (a, b) in {'full': (None, None), 'A': (None, HALF), 'B': (HALF + pd.Timedelta(days=1), None)}.items():
        q = perf(res['ret'], a, b); q.update(book=nm, window=tag); rows.append(q)
    P(f'{nm:<28}', fmt(p), f"| names {p['names']:.0f} expo {p['expo']:.2f} turn {p['turn_yr']:.0f}%/yr")
for c in ['elendel_faithful', 'zenith_faithful', 'quad_faithful']:
    rets[c] = faith[c]
rets['faithful trio (EW)'] = TRIO
for nm in ['elendel_faithful', 'zenith_faithful', 'quad_faithful', 'faithful trio (EW)']:
    p = perf(rets[nm]); P(f'{nm:<28}', fmt(p))
    for tag, (a, b) in {'full': (None, None), 'A': (None, HALF), 'B': (HALF + pd.Timedelta(days=1), None)}.items():
        q = perf(rets[nm], a, b); q.update(book=nm, window=tag); rows.append(q)
pd.DataFrame(rows).to_csv(os.path.join(RES, 'stage22_headline%s.csv' % SUF), index=False, float_format='%.4f')
base = perf(rets['D1 core (L3,n8,m2,H6)'])
zen = perf(rets['zenith_faithful'])
ewg = perf(rets['EW pool U2 + gate'])

# ───────── 2. null distributions (B1-B3) ─────────
P('\n' + '=' * 110); P('2. NULLS  (Sharpe rf0 over the fully-built window; p = (1+#null>=real)/(N+1))'); P('=' * 110)
N_RS, N_RI, N_SH = 200, 200, 100
nulls = {}


def draw(mode, i, **kw):
    rng = np.random.default_rng(10_000 + i)
    if mode == 'shuffle':
        code = permute_within(bd.eng.ind_code, bd.eng.sec_code, rng)
        r = run(bd, D1, rng=rng, ind_code=code)['ret']
    else:
        r = run(bd, replace(D1, mode=mode), rng=rng)['ret']
    return r


for mode, N in (('rand_stock', N_RS), ('rand_ind', N_RI), ('shuffle', N_SH)):
    vals = {'full': [], 'A': [], 'B': []}
    for i in range(N):
        r = draw(mode, i)
        vals['full'].append(perf(r)['sharpe']); vals['A'].append(perf(r, None, HALF)['sharpe']); vals['B'].append(perf(r, HALF + pd.Timedelta(days=1))['sharpe'])
    nulls[mode] = {k: np.array(v) for k, v in vals.items()}
real_sh = {'full': perf(rets['D1 core (L3,n8,m2,H6)'])['sharpe'], 'A': perf(rets['D1 core (L3,n8,m2,H6)'], None, HALF)['sharpe'], 'B': perf(rets['D1 core (L3,n8,m2,H6)'], HALF + pd.Timedelta(days=1))['sharpe']}
nrows = []
for mode, lab in (('rand_stock', 'B1 random-stock book'), ('rand_ind', 'B2 random-industry book'), ('shuffle', 'B3 shuffled-label book')):
    for w in ('full', 'A', 'B'):
        v = nulls[mode][w]
        pv = (1 + (v >= real_sh[w]).sum()) / (len(v) + 1)
        nrows.append(dict(null=lab, window=w, real=real_sh[w], null_mean=v.mean(), null_p95=np.quantile(v, .95), null_max=v.max(), n=len(v), p=pv))
nd = pd.DataFrame(nrows); P(nd.round(3).to_string(index=False)); nd.to_csv(os.path.join(RES, 'stage22_nulls%s.csv' % SUF), index=False, float_format='%.4f')

# ───────── 3. dose-response of industry selectivity ─────────
P('\n' + '=' * 110); P('3. DOSE-RESPONSE: more selective industry ranking should help if the signal is monetisable'); P('=' * 110)
drows = []
for n in (3, 4, 5, 6, 8, 10, 12, 15):
    sp = replace(D1, n_ind=n)
    _, p = cell(f'dose n_ind={n}', sp)
    rs = [perf(run(bd, replace(sp, mode='rand_ind'), rng=np.random.default_rng(500 + i))['ret'])['sharpe'] for i in range(40)]
    drows.append(dict(n_ind=n, sharpe=p['sharpe'], cagr=p['cagr'], maxdd=p['maxdd'], rand_ind_mean=np.mean(rs), rand_ind_p95=np.quantile(rs, .95), premium=p['sharpe'] - np.mean(rs), names=p['names']))
dd = pd.DataFrame(drows); P(dd.round(3).to_string(index=False)); dd.to_csv(os.path.join(RES, 'stage22_dose_response%s.csv' % SUF), index=False, float_format='%.4f')

# ───────── 4. one-at-a-time sensitivity (B5) ─────────
P('\n' + '=' * 110); P('4. ONE-AT-A-TIME SENSITIVITY (all pre-registered values, all reported)'); P('=' * 110)
grid = {'L': [1, 2, 3, 4, 6, 9, 12], 'skip': [0, 1], 'n_ind': [5, 6, 8, 10, 12], 'm': [1, 2, 3, 4], 'H': [1, 3, 4, 5, 6, 7, 9, 12],
        'score': ['a1', 'lowvol', 'rand'], 'gate': [True, False], 'pool': ['U2_live_trend', 'U1_liquid1000', 'U7_midsmall_301_1000', 'U3_top300', 'U4_top250'],
        'weighting': ['eq', 'dv'], 'require_pos': [True, False], 'min_members': [8, 10, 15], 'cash_rate': [0.065, 0.0]}
srows = []
for par, vals in grid.items():
    for v in vals:
        sp = replace(D1, **{par: v})
        _, p = cell(f'sens {par}={v}', sp)
        p.update(param=par, value=v); srows.append(p)
sd = pd.DataFrame(srows)
P(sd[['param', 'value', 'cagr', 'vol', 'sharpe', 'sharpe6', 'maxdd', 'calmar', 'names', 'turn_yr']].round(3).to_string(index=False))
sd.to_csv(os.path.join(RES, 'stage22_sensitivity%s.csv' % SUF), index=False, float_format='%.4f')
plateau = {'L': [2, 3, 4], 'n_ind': [6, 8, 10], 'm': [1, 2, 3], 'H': [5, 6, 7]}
swing = {k: sd[(sd.param == k) & (sd.value.isin(v))].sharpe.tolist() + [base['sharpe']] for k, v in plateau.items()}
swing = {k: max(v) - min(v) for k, v in swing.items()}
P('\nB5 plateau (Sharpe swing across +-20% neighbours, gate <= 0.4):', {k: round(v, 3) for k, v in swing.items()})

# ───────── 5. split A / B (B4) ─────────
P('\n' + '=' * 110); P('5. BIDIRECTIONAL SPLIT (Playbook Stage 4) with the fixed D1'); P('=' * 110)
rA, rB = perf(rets['D1 core (L3,n8,m2,H6)'], None, HALF), perf(rets['D1 core (L3,n8,m2,H6)'], HALF + pd.Timedelta(days=1))
P('A (%s..%s):' % (W0.date(), HALF.date()), fmt(rA)); P('B (2013-01-01..%s):' % END.date(), fmt(rB))
split_ok = {}
for name, IS, OOS in (('Split A (IS=A, OOS=B)', rA, rB), ('Split B (IS=B, OOS=A)', rB, rA)):
    ratio = dict(sharpe=OOS['sharpe'] / IS['sharpe'], calmar=OOS['calmar'] / IS['calmar'], cagr=OOS['cagr'] / IS['cagr'], maxdd=abs(OOS['maxdd']) / abs(IS['maxdd']))
    ok = ratio['sharpe'] >= 0.6 and ratio['calmar'] >= 0.6 and ratio['cagr'] >= 0.5 and ratio['maxdd'] <= 1.5 and OOS['sharpe'] > 0
    split_ok[name] = ok
    P(f"{name}: OOS/IS Sharpe {ratio['sharpe']:.2f} (>=0.6) | Calmar {ratio['calmar']:.2f} (>=0.6) | CAGR {ratio['cagr']:.2f} (>=0.5) | MaxDD {ratio['maxdd']:.2f}x (<=1.5) | OOS Sharpe>0 -> {'PASS' if ok else 'FAIL'}")

# ───────── 6. costs (B6) ─────────
P('\n' + '=' * 110); P('6. COST STRESS (per side)'); P('=' * 110)
crow = []
for c in (0.003, 0.006, 0.010):
    _, p = cell(f'cost {c}', replace(D1, side_cost=c)); _, b = cell(f'ewgate cost {c}', replace(D1, mode='ew_pool', side_cost=c))
    crow.append(dict(side_cost=c, book_cagr=p['cagr'], book_sharpe=p['sharpe'], ew_gate_cagr=b['cagr'], ew_gate_sharpe=b['sharpe'], zen_cagr=zen['cagr']))
cd = pd.DataFrame(crow); P(cd.round(3).to_string(index=False))
c06 = cd[cd.side_cost == 0.006].iloc[0]
cost_ok = (c06.book_sharpe >= 0.7 * base['sharpe']) and (c06.book_cagr > max(c06.zen_cagr, c06.ew_gate_cagr))

# ───────── 7. concentration (B7) ─────────
P('\n' + '=' * 110); P('7. CONCENTRATION'); P('=' * 110)
r0 = window(rets['D1 core (L3,n8,m2,H6)'], W0)
yr = (1 + r0).groupby(r0.index.year).prod() - 1
best3 = yr.nlargest(3).index.tolist()
rx = r0[~r0.index.year.isin(best3)]
mx = metrics(rx, 0.0)
P('calendar-year returns (%):', (yr * 100).round(1).to_dict()); P('best 3 years removed:', best3, '-> CAGR %.1f%% Sharpe %.2f (full CAGR %.1f%%)' % (mx['cagr'] * 100, mx['sharpe'], base['cagr'] * 100))
eps = pd.DataFrame(res0['episodes'], columns=['name', 'start', 'end', 'pnl'])
pos = eps[eps.pnl > 0].pnl.sort_values(ascending=False)
top10 = pos.head(10).sum() / pos.sum()
P('holding episodes: %d, win rate %.1f%%, top-10 episodes = %.1f%% of positive P&L, top-10 names: %s' % (len(eps), (eps.pnl > 0).mean() * 100, top10 * 100, eps.loc[pos.head(10).index, 'name'].tolist()))
conc_ok = (mx['sharpe'] > 0.5) and (mx['cagr'] >= 0.5 * base['cagr']) and (top10 <= 0.40)

# ───────── 8. risk (B8) ─────────
P('\n' + '=' * 110); P('8. RISK (the stated goal: proper return with low DD)'); P('=' * 110)
risk_ok = (base['maxdd'] >= ewg['maxdd']) and (base['calmar'] >= zen['calmar'])
P(f"D1 MaxDD {base['maxdd']*100:.1f}% vs EW-pool+gate {ewg['maxdd']*100:.1f}% vs faithful Zenith {zen['maxdd']*100:.1f}%;  Calmar D1 {base['calmar']:.2f} vs Zenith {zen['calmar']:.2f}")
eq = (1 + r0).cumprod(); ddn = eq / eq.cummax() - 1
ep = []
under = ddn < -0.20
P('drawdown episodes deeper than -20%:')
start = None
for d, v in under.items():
    if v and start is None: start = d
    if (not v) and start is not None:
        seg = ddn[start:d]; ep.append((start.date(), seg.idxmin().date(), round(seg.min() * 100, 1))); start = None
if start is not None:
    seg = ddn[start:]; ep.append((start.date(), seg.idxmin().date(), round(seg.min() * 100, 1)))
P(ep)

# ───────── 9. break-even + blend (B9) ─────────
P('\n' + '=' * 110); P('9. DIVERSIFICATION vs the FAITHFUL live trio'); P('=' * 110)
j = pd.concat([r0, TRIO], axis=1).dropna(); j.columns = ['new', 'trio']
rho = j.corr().iloc[0, 1]
pn0, pt0 = metrics(j.new, 0.0)['sharpe'], metrics(j.trio, 0.0)['sharpe']; pn6, pt6 = metrics(j.new, 0.06)['sharpe'], metrics(j.trio, 0.06)['sharpe']
P(f'corr(D1, trio) daily {rho:.2f}; break-even rf0: Sharpe_new {pn0:.2f} vs rho*Sharpe_trio {rho*pt0:.2f} -> {pn0 > rho*pt0};  rf6: {pn6:.2f} vs {rho*pt6:.2f} -> {pn6 > rho*pt6}')
brow = []
for w in (0.0, 0.1, 0.2, 0.3, 0.5, 1.0):
    b = (1 - w) * j.trio + w * j.new; m = metrics(b, 0.0)
    brow.append(dict(w_new=w, cagr=m['cagr'], vol=m['vol'], sharpe=m['sharpe'], sharpe6=metrics(b, 0.06)['sharpe'], maxdd=m['maxdd']))
bl = pd.DataFrame(brow); P(bl.round(3).to_string(index=False)); bl.to_csv(os.path.join(RES, 'stage22_blend%s.csv' % SUF), index=False, float_format='%.4f')
b0 = bl[bl.w_new == 0].iloc[0]
blend_ok = all((bl[bl.w_new == w].iloc[0].sharpe > b0.sharpe) and (bl[bl.w_new == w].iloc[0].maxdd >= b0.maxdd) for w in (0.2, 0.3)) and (pn0 > rho * pt0)

# ───────── 10. deflated Sharpe (B10) ─────────
P('\n' + '=' * 110); P('10. DEFLATED SHARPE (monthly returns, Bailey & Lopez de Prado)'); P('=' * 110)
mr = monthly(rets['D1 core (L3,n8,m2,H6)'])
T = len(mr); sr = mr.mean() / mr.std(); sk = mr.skew(); ku = mr.kurt() + 3
var_sr = np.var([s for _, s in TRIALS])
em = 0.5772156649


def dsr(N):
    sr0 = np.sqrt(var_sr) * ((1 - em) * norm.ppf(1 - 1 / N) + em * norm.ppf(1 - 1 / (N * np.e)))
    return norm.cdf((sr - sr0) * np.sqrt(T - 1) / np.sqrt(1 - sk * sr + (ku - 1) / 4 * sr ** 2)), sr0 * np.sqrt(12)


P(f'T={T} months, monthly SR={sr:.3f} (annualised {sr*np.sqrt(12):.2f}), skew {sk:.2f}, kurt {ku:.1f}; {len(TRIALS)} book cells evaluated in this run, SR variance across cells {var_sr:.5f}')
dsr_res = {N: dsr(N) for N in (20, 100, 300)}
for N, (d, s0) in dsr_res.items():
    P(f'  N_trials={N}: expected-max annual SR under the null {s0:.2f} -> DSR {d:.3f}')
dsr_ok = dsr_res[100][0] >= 0.5

# ───────── 11. delay sanity (B11, informational) ─────────
P('\n' + '=' * 110); P('11. DELAY SANITY (signal executed one extra month late)'); P('=' * 110)
Clag = np.vstack([np.zeros((1, res0['C'].shape[1]), dtype=np.float32), res0['C'][:-1]])
rlag = simulate(bd, Clag, D1)['ret']
if D1.vol_target > 0:
    rlag, _ = vol_overlay(rlag, D1)
pl = perf(rlag); P('lagged by 1 month:', fmt(pl), '| base', fmt(base))

# ───────── scoreboard ─────────
P('\n' + '=' * 110); P('SCOREBOARD (pre-registered gates for D1)'); P('=' * 110)
sb = []


def gate(name, ok, detail):
    sb.append(dict(gate=name, result='PASS' if ok else 'FAIL', detail=detail)); P(f'{name:<4} {"PASS" if ok else "FAIL"}   {detail}')


pp = {(r.null, r.window): r.p for r in nd.itertuples()}
gate('B1', all(pp[('B1 random-stock book', w)] <= 0.05 for w in ('full', 'A', 'B')), 'p vs random-stock book: ' + ', '.join(f"{w} {pp[('B1 random-stock book', w)]:.3f}" for w in ('full', 'A', 'B')))
gate('B2', pp[('B2 random-industry book', 'full')] <= 0.05, 'p vs random-industry book (full): %.3f ; halves A %.3f B %.3f' % (pp[('B2 random-industry book', 'full')], pp[('B2 random-industry book', 'A')], pp[('B2 random-industry book', 'B')]))
gate('B3', pp[('B3 shuffled-label book', 'full')] <= 0.05, 'p vs shuffled-label book (full): %.3f' % pp[('B3 shuffled-label book', 'full')])
gate('B4', all(split_ok.values()), str(split_ok))
gate('B5', max(swing.values()) <= 0.4, str({k: round(v, 3) for k, v in swing.items()}))
gate('B6', cost_ok, f"0.6%/side: Sharpe {c06.book_sharpe:.2f} (base {base['sharpe']:.2f}), CAGR {c06.book_cagr*100:.1f}% vs EW-pool {c06.ew_gate_cagr*100:.1f}% / Zenith {c06.zen_cagr*100:.1f}%")
gate('B7', conc_ok, f"ex-best-3-years Sharpe {mx['sharpe']:.2f}, CAGR {mx['cagr']*100:.1f}%; top-10 episodes {top10*100:.0f}% of positive P&L")
gate('B8', risk_ok, f"MaxDD {base['maxdd']*100:.1f}% vs EW-pool {ewg['maxdd']*100:.1f}%; Calmar {base['calmar']:.2f} vs Zenith {zen['calmar']:.2f}")
gate('B9', blend_ok, f"rho {rho:.2f}; break-even {pn0:.2f} > {rho*pt0:.2f}; blend Sharpe 20% {bl[bl.w_new==0.2].iloc[0].sharpe:.2f}, 30% {bl[bl.w_new==0.3].iloc[0].sharpe:.2f} vs trio {b0.sharpe:.2f}")
gate('B10', dsr_ok, 'DSR(N=100) %.3f' % dsr_res[100][0])
P('B11  info   delayed-signal Sharpe %.2f vs base %.2f (%s)' % (pl['sharpe'], base['sharpe'], 'information decays: as expected' if pl['sharpe'] < base['sharpe'] else 'NO DECAY: suspicious'))
sbd = pd.DataFrame(sb); sbd.to_csv(os.path.join(RES, 'stage22_scoreboard%s.csv' % SUF), index=False)
verdict = 'PASS' if (sbd.result == 'PASS').all() else 'FAIL'
kill = [g for g in ('B1', 'B2', 'B4', 'B9') if sbd[sbd.gate == g].result.iloc[0] == 'FAIL']
P('\nVERDICT for D1:', verdict, '| KILL-rule gates failed:', kill if kill else 'none')
open(os.path.join(RES, 'stage22_book_battery%s.txt' % SUF), 'w').write('\n'.join(OUT))

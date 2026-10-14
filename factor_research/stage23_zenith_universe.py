"""
stage23_zenith_universe.py -- INDUSTRY_BOOK_PREREG.md section 7 (Amendment 2): Zenith as the base, "worth-it" control vs simpler books, universe robustness.
    python3 stage23_zenith_universe.py     -> results/stage23_*.csv, results/stage23_report.txt
"""
import os, sys, time, pickle, warnings
import numpy as np, pandas as pd
warnings.filterwarnings('ignore')
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from industry_book import Spec, BookData, run, metrics, window
from data import load_panels
from factors import Ctx, rmean
RES = os.path.join(HERE, 'results'); os.makedirs(RES, exist_ok=True)
lines = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s, flush=True); lines.append(s)

st = pickle.load(open(os.path.join(HERE, '.cache', 'state.pkl'), 'rb'))
UN = pickle.load(open(os.path.join(HERE, '.cache', 'extra_universes.pkl'), 'rb'))
X = Ctx(load_panels()); sig, F = st['sig'], st['F']
faith = pd.read_csv(os.path.join(os.path.dirname(HERE), 'csm_value', 'output', 'faithful_engine_returns.csv'), index_col=0, parse_dates=True)
ZEN = faith['zenith_faithful']
HALF = pd.Timestamp('2012-12-31')
VT = 0.15


def band(lo, hi):
    Cf = X.Cf
    have = Cf.reindex(sig).notna(); price_ok = Cf.reindex(sig) > 20
    rank = X.DV.rolling(63, min_periods=21).median().reindex(sig).rank(axis=1, ascending=False, method='min')
    circ = ((X.H == X.L) & X.H.notna()).astype('float64').rolling(63, min_periods=1).sum().reindex(sig) <= 5
    U1 = have & price_ok & (rank >= lo) & (rank <= hi) & circ
    return U1, U1 & (Cf > rmean(Cf, 200)).reindex(sig)


U1b, U2b = band(1, 1000)
assert U1b.equals(st['U']['U1_liquid1000']) and U2b.equals(st['U']['U2_live_trend']), 'band(1,1000) must equal the cached base universes'
bd = BookData(X, sig, {'U1_liquid1000': U1b, 'U2_live_trend': U2b}, UN, F)
base = run(bd, Spec(vol_target=VT))
W0 = base['ret'].index[0] + pd.DateOffset(months=6)
WIN = {'full': (W0, None), '<=2012': (W0, HALF), '>=2013': (HALF + pd.Timedelta(days=1), None), '2015+': (pd.Timestamp('2015-01-01'), None)}


def perf(r, w):
    a, b = WIN[w]; rr = window(r, a, b); m0, m6 = metrics(rr, 0.0), metrics(rr, 0.06)
    return dict(cagr=m0['cagr'], vol=m0['vol'], sharpe=m0['sharpe'], sharpe6=m6['sharpe'], maxdd=m0['maxdd'], calmar=m0['calmar'])


# ═════════════ B. Zenith base ═════════════
P('=' * 110); P('B. ZENITH AS THE BASE  (comparator: zenith_faithful; same overlays on every book: gate 0.5x, 15% vol target, 6.5% cash, H=6, 0.3%/side)'); P('=' * 110)
books = {}
t0 = time.time()
books['D1v_A1'] = run(bd, Spec(vol_target=VT))['ret']
books['D1v_ZenScore'] = run(bd, Spec(score='zen', vol_target=VT))['ret']
books['noInd_top16_Zen'] = run(bd, Spec(mode='topn', score='zen', vol_target=VT))['ret']
books['noInd_top16_A1'] = run(bd, Spec(mode='topn', score='a1', vol_target=VT))['ret']
books['EW_pool'] = run(bd, Spec(mode='ew_pool', vol_target=VT))['ret']
rnd = [run(bd, Spec(mode='rand_ind', vol_target=VT), rng=np.random.default_rng(1000 + i))['ret'] for i in range(20)]
books['randInd_mean20'] = pd.concat(rnd, axis=1).mean(axis=1)
P(f'  {len(books)-1+20} book runs in {time.time()-t0:.0f}s')

rows = []
P('\n-- standalone and vs Zenith (daily returns, rf0 Sharpe)')
for name, r in books.items():
    j = pd.concat([r, ZEN], axis=1).dropna(); j.columns = ['new', 'zen']
    rho = j.corr().iloc[0, 1]
    for w in WIN:
        p = perf(r, w); rows.append(dict(book=name, window=w, kind='standalone', weight=1.0, rho_zen=rho, **p))
    pz = {w: perf(ZEN, w) for w in WIN}
    P(f"  {name:<18} rho(Zenith) {rho:.2f} | full: CAGR {perf(r,'full')['cagr']*100:5.1f}% Sharpe {perf(r,'full')['sharpe']:.2f} (rf6 {perf(r,'full')['sharpe6']:.2f}) MaxDD {perf(r,'full')['maxdd']*100:6.1f}% | "
      f"halves Sharpe {perf(r,'<=2012')['sharpe']:.2f} / {perf(r,'>=2013')['sharpe']:.2f}  MaxDD {perf(r,'<=2012')['maxdd']*100:.1f} / {perf(r,'>=2013')['maxdd']*100:.1f}")
    for w in (0.1, 0.2, 0.3, 0.5):
        b = (1 - w) * j.zen + w * j.new
        for wn in WIN:
            rows.append(dict(book=name, window=wn, kind='blend', weight=w, rho_zen=rho, **perf(b, wn)))
P('  Zenith faithful alone: ' + ' | '.join(f"{w}: CAGR {perf(ZEN,w)['cagr']*100:.1f}% Sharpe {perf(ZEN,w)['sharpe']:.2f} MaxDD {perf(ZEN,w)['maxdd']*100:.1f}%" for w in ('full', '<=2012', '>=2013')))
tab = pd.DataFrame(rows); tab.to_csv(os.path.join(RES, 'stage23_zenith_blends.csv'), index=False, float_format='%.4f')

P('\n-- blend with Zenith: delta vs Zenith alone (Sharpe rf0 / MaxDD pts), by half')
dz = {w: perf(ZEN, w) for w in WIN}
for name in books:
    out = []
    for w in (0.2, 0.3):
        for wn in ('<=2012', '>=2013'):
            r = tab[(tab.book == name) & (tab.kind == 'blend') & (tab.weight == w) & (tab.window == wn)].iloc[0]
            out.append(f"w{int(w*100)} {wn}: dSh {r.sharpe-dz[wn]['sharpe']:+.2f} dDD {100*(r.maxdd-dz[wn]['maxdd']):+.1f}")
    P(f'  {name:<18} ' + ' | '.join(out))

# single-year dependence of blend benefit (w=0.3)
P('\n-- share of the blend benefit (log excess over Zenith, w=0.3) from the single best calendar year')
shares = {}
for name in ('D1v_A1', 'D1v_ZenScore', 'noInd_top16_Zen', 'EW_pool'):
    j = pd.concat([books[name], ZEN], axis=1).dropna(); j.columns = ['new', 'zen']; j = window(j, W0)
    b = 0.7 * j.zen + 0.3 * j.new
    ex = (np.log1p(b) - np.log1p(j.zen)).groupby(j.index.year).sum()
    shares[name] = ex.max() / ex.sum() if ex.sum() > 0 else float('nan')
    P(f'  {name:<18} total log excess {ex.sum()*100:+.1f} pts; best year {ex.idxmax()} = {ex.max()*100:+.1f} pts ({shares[name]*100:.0f}% of total); years with negative excess: {(ex<0).sum()} of {len(ex)}')

# gates B
def half_delta(name, w=0.3):
    return {wn: (tab[(tab.book == name) & (tab.kind == 'blend') & (tab.weight == w) & (tab.window == wn)].iloc[0]) for wn in ('<=2012', '>=2013')}
a1, zs = perf(books['D1v_A1'], '<=2012'), perf(books['D1v_ZenScore'], '<=2012')
a2, zs2 = perf(books['D1v_A1'], '>=2013'), perf(books['D1v_ZenScore'], '>=2013')
switch = (zs['sharpe'] >= a1['sharpe'] and zs2['sharpe'] >= a2['sharpe'] and zs['maxdd'] >= a1['maxdd'] and zs2['maxdd'] >= a2['maxdd'])
P(f"\nB2 score rule (Zenith composite instead of A1 only if Sharpe >= in both halves and MaxDD not worse in either): "
  f"halves Sharpe A1 {a1['sharpe']:.2f}/{a2['sharpe']:.2f} vs Zen {zs['sharpe']:.2f}/{zs2['sharpe']:.2f}; MaxDD A1 {a1['maxdd']*100:.1f}/{a2['maxdd']*100:.1f} vs Zen {zs['maxdd']*100:.1f}/{zs2['maxdd']*100:.1f} -> {'SWITCH to Zenith score' if switch else 'KEEP A1'}")
chosen = 'D1v_ZenScore' if switch else 'D1v_A1'


def better(name, other):
    ok = True
    for w in (0.2, 0.3):
        dn, do = half_delta(name, w), half_delta(other, w)
        for wn in ('<=2012', '>=2013'):
            ok &= (dn[wn].sharpe > do[wn].sharpe) and (dn[wn].maxdd >= do[wn].maxdd)
    return ok


P(f"B3 worth-it control: {chosen} blend beats noInd_top16_Zen (Sharpe & MaxDD, w 20/30%, both halves): {better(chosen,'noInd_top16_Zen')};  beats EW_pool: {better(chosen,'EW_pool')};  beats randInd_mean20: {better(chosen,'randInd_mean20')}")
B3 = better(chosen, 'noInd_top16_Zen') and better(chosen, 'EW_pool')
improves = all((half_delta(chosen, w)[wn].sharpe > dz[wn]['sharpe']) and (half_delta(chosen, w)[wn].maxdd >= dz[wn]['maxdd']) for w in (0.2, 0.3) for wn in ('<=2012', '>=2013'))
P(f'D(4) {chosen} blended 20-30% with Zenith improves Sharpe AND MaxDD in both halves: {improves};  D(5) best-year share of benefit {shares[chosen]*100:.0f}% (<=60% needed): {shares[chosen] <= 0.6}')

# ═════════════ C. Universe robustness ═════════════
P('\n' + '=' * 110); P('C. UNIVERSE ROBUSTNESS  (baskets AND stock pool from the same dollar-volume-rank band; D1v spec unchanged; 30 random-industry draws each)'); P('=' * 110)
BANDS = [(1, 300), (1, 500), (1, 1000), (301, 1000), (1, 1500), (1, 2000)]
crow = []
for lo, hi in BANDS:
    t1 = time.time()
    if (lo, hi) == (1, 1000):
        U1, U2, b = U1b, U2b, bd
    else:
        U1, U2 = band(lo, hi)
        b = BookData(X, sig, {'U1_liquid1000': U1, 'U2_live_trend': U2}, UN, F)
    sp = Spec(vol_target=VT)
    res = run(b, sp); r = res['ret']
    ew = run(b, Spec(mode='ew_pool', vol_target=VT))['ret']
    rd = [run(b, Spec(mode='rand_ind', vol_target=VT), rng=np.random.default_rng(5000 + i))['ret'] for i in range(30)]
    sh_rd = np.array([perf(x, 'full')['sharpe'] for x in rd]); sh = perf(r, 'full')['sharpe']
    usable = (b.cnt_now >= sp.min_members).sum(axis=1)
    msk = (sig >= pd.Timestamp('2005-01-01'))
    C = res['C']; dvv = b.eng.dv.values
    picks = np.concatenate([dvv[k, C[k] > 0] for k in range(len(sig)) if msk[k]]); picks = picks[np.isfinite(picks)]
    row = dict(band=f'{lo}-{hi}', usable_ind=usable[msk].mean(), names=res['info'].names.mean(), turnover_yr=res['info'].turnover_oneway.mean() * 1200,
               sharpe=sh, sharpe6=perf(r, 'full')['sharpe6'], cagr=perf(r, 'full')['cagr'], maxdd=perf(r, 'full')['maxdd'],
               sharpe_A=perf(r, '<=2012')['sharpe'], sharpe_B=perf(r, '>=2013')['sharpe'], ew_sharpe=perf(ew, 'full')['sharpe'], ew_cagr=perf(ew, 'full')['cagr'],
               edge_sharpe=sh - perf(ew, 'full')['sharpe'], rand_mean_sharpe=sh_rd.mean(), p_rand=(sh_rd >= sh).mean(),
               ew_sharpe_A=perf(ew, '<=2012')['sharpe'], ew_sharpe_B=perf(ew, '>=2013')['sharpe'],
               dv_med_cr=np.median(picks) / 1e7, dv_p10_cr=np.percentile(picks, 10) / 1e7)
    crow.append(row)
    P(f"  {row['band']:<9} usable ind {row['usable_ind']:5.1f}  names {row['names']:4.0f}  turn {row['turnover_yr']:4.0f}%/yr | D1v CAGR {row['cagr']*100:5.1f}% Sharpe {sh:.2f} (rf6 {row['sharpe6']:.2f}) MaxDD {row['maxdd']*100:6.1f}% "
      f"| halves {row['sharpe_A']:.2f}/{row['sharpe_B']:.2f} | EW-pool Sharpe {row['ew_sharpe']:.2f} CAGR {row['ew_cagr']*100:.1f}% edge {row['edge_sharpe']:+.2f} | rand-ind mean {row['rand_mean_sharpe']:.2f} p={row['p_rand']:.2f} "
      f"| pick DV median Rs {row['dv_med_cr']:.1f} cr, p10 {row['dv_p10_cr']:.2f} cr  ({time.time()-t1:.0f}s)")
    if (lo, hi) != (1, 1000):
        del b
ct = pd.DataFrame(crow); ct.to_csv(os.path.join(RES, 'stage23_universe_bands.csv'), index=False, float_format='%.4f')
beats = int((ct.sharpe > ct.ew_sharpe).sum()); big = int((ct.sharpe > 1.0).sum())
C_pass = beats >= 4 and big >= 4
P(f'\nC robustness: D1v beats its own EW-pool Sharpe in {beats}/6 bands; Sharpe(rf0) > 1.0 in {big}/6 -> {"PASS" if C_pass else "FAIL"}')
bs = ct[ct.band == '1-1000'].iloc[0]
for _, r in ct.iterrows():
    if r.band == '1-1000': continue
    rep = (r.sharpe_A >= bs.sharpe_A + 0.10) and (r.sharpe_B >= bs.sharpe_B + 0.10) and (r.dv_med_cr >= bs.dv_med_cr)
    P(f'   band {r.band} replaces 1-1000? Sharpe halves {r.sharpe_A:.2f}/{r.sharpe_B:.2f} vs base {bs.sharpe_A:.2f}/{bs.sharpe_B:.2f}; pick DV {r.dv_med_cr:.1f} vs {bs.dv_med_cr:.1f} cr -> {rep}')

open(os.path.join(RES, 'stage23_report.txt'), 'w').write('\n'.join(lines) + '\n')

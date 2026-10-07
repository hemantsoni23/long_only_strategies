"""Pre-registered gold sleeve rules (fixed textbook parameters, no grid search). Monthly decision at month-end close t, trade at close t+1,
return = strict (observed-price-only) next-month gold return; off-gold capital earns 6% cash. One-way cost 0.15% on exposure change."""
import numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from gold_data import *
from portfolio_lab import stats
CASH_M = 1.06**(1/12)-1; COST = 0.0015
rm = lambda x,w,mp=0.8: x.rolling(w,min_periods=int(w*mp))

def build_signals(g, I):
    """daily frames -> dict of month-end exposure rules in [0,1]; g has the data gap as NaN."""
    r = g.pct_change(fill_method=None)
    sma50, sma100, sma200 = rm(g,50).mean(), rm(g,100).mean(), rm(g,200).mean()
    ab50 = (g>sma50).where(g.notna()&sma50.notna()).astype(float)
    q5 = ab50.rolling(126,min_periods=100).mean()
    tsm = g.shift(21)/g.shift(252)-1
    vol63 = rm(r,63).std()*np.sqrt(252)
    N5 = I['Nifty_500'].reindex(g.index).ffill(); eq_stress = (N5 < rm(N5,200).mean())
    exp = {}
    exp['G0 buy&hold'] = pd.Series(1.0,index=g.index).where(g.notna())
    exp['G1 TSMOM 12-1 binary'] = (tsm>0.06).astype(float).where(tsm.notna())          # beats 6% cash
    exp['G2 SMA200 binary'] = (g>sma200).astype(float).where(sma200.notna())
    exp['G3 persistence-scaled (q5_126)'] = q5
    exp['G4 vol-target 12% (no momentum)'] = (0.12/vol63).clip(upper=1.0).where(vol63.notna())
    exp['G5 persistence x vol-target'] = (q5*(0.12/vol63).clip(upper=1.0))
    exp['G6 hedge-conditional'] = pd.Series(np.where(eq_stress.reindex(g.index).fillna(False), 1.0, q5), index=g.index).where(q5.notna())
    # G7: drawdown-band trend: long by default; exit if >8% below 126d high; re-enter on a new 21d high (stateful)
    hi126 = rm(g,126).max(); hi21 = rm(g,21).max().shift(1)
    state = np.full(len(g), np.nan); cur = 1.0
    gv = g.values; h126 = hi126.values; h21 = hi21.values
    for i in range(len(g)):
        if np.isnan(gv[i]) or np.isnan(h126[i]): cur = 1.0; continue
        if cur==1.0 and gv[i] <= 0.92*h126[i]: cur = 0.0
        elif cur==0.0 and not np.isnan(h21[i]) and gv[i] > h21[i]: cur = 1.0
        state[i] = cur
    exp['G7 drawdown-band (long by default)'] = pd.Series(state,index=g.index)
    return exp

def run_rule(expo_m, fwd, cost=COST):
    """expo_m, fwd: monthly series indexed by signal date. Returns net monthly return series."""
    d = pd.concat([expo_m,fwd],axis=1,keys=['e','r']).dropna()
    turn = d.e.diff().abs().fillna(d.e.abs())
    net = d.e*d.r + (1-d.e)*CASH_M - cost*turn
    return net, d.e

if __name__ == '__main__':
    gold, vol, I, Ec, cal = load_gold(); sig = L.month_ends(cal)
    fwd = monthly_fwd_strict(gold, cal, sig)
    exp_d = build_signals(gold, I)
    expm = {k: v.reindex(sig) for k,v in exp_d.items()}
    nets, expos = {}, {}
    for k,e in expm.items(): nets[k], expos[k] = run_rule(e, fwd)
    common = None
    for k,v in nets.items(): common = v.index if common is None else common.intersection(v.index)
    common = common[(common>='2008-03-31')&(common<='2026-06-30')]
    N = pd.DataFrame({k:v.reindex(common) for k,v in nets.items()}); E = pd.DataFrame({k:v.reindex(common) for k,v in expos.items()})
    N.to_csv('results/gold_rules_monthly.csv',float_format='%.6f'); E.to_csv('results/gold_rules_exposure.csv',float_format='%.4f')
    # bucket
    S = pd.read_csv('results/stage14_monthly_returns.csv',index_col=0,parse_dates=True)
    B = S[['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']].mean(axis=1)
    key = lambda s: s.set_axis(s.index.to_period('M'))
    NB = N.copy(); NB.index = NB.index.to_period('M'); Bk = key(B).reindex(NB.index)
    ok = Bk.notna(); NB, Bk = NB[ok], Bk[ok]
    segA = NB.index <= pd.Period('2010-12'); segB = NB.index >= pd.Period('2015-01')
    worst10 = Bk <= Bk.quantile(0.10); worst20 = Bk <= Bk.quantile(0.20)
    rows=[]
    b0 = stats(Bk)
    for k in NB.columns:
        x = NB[k]; s = stats(x)
        row = dict(rule=k, months=len(x), cagr=s['cagr'], vol=s['vol'], sharpe=s['sharpe'], maxdd=s['maxdd'], calmar=s['calmar'],
                   avg_exposure=E[k].mean(), turnover_yr=E[k].diff().abs().sum()/(len(E)/12), corr_bucket=np.corrcoef(x,Bk)[0,1],
                   worst10_ret=x[worst10].mean(), worst20_ret=x[worst20].mean())
        for w in (0.10,):
            p = (1-w)*Bk + w*x; ps = stats(p)
            row.update(blend_dSharpe=ps['sharpe']-b0['sharpe'], blend_dMaxDD=ps['maxdd']-b0['maxdd'], blend_dCAGR=ps['cagr']-b0['cagr'])
            for tag,m in (('A',segA),('B',segB)):
                pb = stats(Bk[m]); pp = stats(((1-w)*Bk+w*x)[m])
                row[f'blend_dSharpe_{tag}'] = pp['sharpe']-pb['sharpe']; row[f'blend_dMaxDD_{tag}'] = pp['maxdd']-pb['maxdd']
        for tag,m in (('A',segA),('B',segB)):
            ss = stats(x[m]); row[f'sharpe_{tag}']=ss['sharpe']; row[f'maxdd_{tag}']=ss['maxdd']; row[f'cagr_{tag}']=ss['cagr']
        rows.append(row)
    R = pd.DataFrame(rows).set_index('rule'); R.to_csv('results/gold_rules_scorecard.csv',float_format='%.4f')
    pd.set_option('display.width',280); pd.set_option('display.max_columns',40)
    print('months (bucket-overlap):',len(NB),' segA months',int(segA.sum()),' segB months',int(segB.sum()),'  bucket worst-10% months:',int(worst10.sum()))
    print(R[['cagr','vol','sharpe','maxdd','calmar','avg_exposure','turnover_yr','corr_bucket','worst10_ret','worst20_ret']].round(3).to_string())
    print('\n-- sleeve value in the bucket at 10%% weight (bucket alone: Sharpe %.3f MaxDD %.3f CAGR %.3f)'%(b0['sharpe'],b0['maxdd'],b0['cagr']))
    print(R[['blend_dSharpe','blend_dMaxDD','blend_dCAGR','blend_dSharpe_A','blend_dMaxDD_A','blend_dSharpe_B','blend_dMaxDD_B','sharpe_A','sharpe_B','maxdd_A','maxdd_B']].round(3).to_string())

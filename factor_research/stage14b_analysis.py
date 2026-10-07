import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from stage14_roadmap import *   # IDEAS, F, FWD, U, allU, sig, bull, chassis, book, make_score, CASH_M, PER
rng = np.random.default_rng(7)
S = pd.read_csv('results/stage14_monthly_returns.csv', index_col=0, parse_dates=True)
S = S.loc[:'2026-06-30']
br = pd.read_csv('results/stage14_breakout_monthly_aligned.csv',index_col=0,parse_dates=True)
S = S.join(br, how='left')
raw = pickle.load(open('.cache/stage14_raw_books.pkl','rb'))
HOLD = pd.Timestamp('2014-12-31')
def st(r):
    r = r.dropna()
    if len(r)<24: return {}
    return stats(r)
# ---------------- A. core table ----------------
rows=[]
for c in S.columns:
    r = S[c].dropna()
    a, d, h = st(r), st(r[r.index<=HOLD]), st(r[r.index>HOLD])
    rows.append(dict(idea=c, start=r.index[0].date(), months=len(r), cagr=a['cagr'], vol=a['vol'], sharpe=a['sharpe'], maxdd=a['maxdd'], calmar=a['calmar'],
        cagr_hold=h.get('cagr'), sharpe_hold=h.get('sharpe'), maxdd_hold=h.get('maxdd'), cagr_disc=d.get('cagr'), sharpe_disc=d.get('sharpe'),
        worst_12m=(1+r).rolling(12).apply(np.prod,raw=True).min()-1, pct_pos_yrs=(r.groupby(r.index.year).apply(lambda x:(1+x).prod()-1)>0).mean()))
core = pd.DataFrame(rows).set_index('idea'); core.to_csv('results/stage14_core.csv', float_format='%.4f')
pd.set_option('display.width',280); pd.set_option('display.max_columns',40); pd.set_option('display.max_colwidth',44)
print(core.round(3).to_string())
# ---------------- B. block bootstrap vs control ----------------
def sharpe(x): return (x - CASH_M).mean()/x.std()*np.sqrt(12) if x.std()>0 else np.nan
def boot(df, f, reps=4000, blk=6):
    n=len(df); out=[]
    arr=df.values
    for _ in range(reps):
        idx=[]; 
        while len(idx)<n:
            s=rng.integers(0,n); L_=min(rng.geometric(1/blk), n)
            idx.extend([(s+k)%n for k in range(L_)])
        idx=np.array(idx[:n]); out.append(f(arr[idx]))
    return np.array(out)
ctrl = S['Elendel (control)']
rows=[]
for c in S.columns:
    if c=='Elendel (control)': continue
    df = pd.concat([S[c],ctrl],axis=1).dropna()
    df = df[df.index>='2008-04-30']
    if len(df)<60: continue
    sh = lambda a: ((a[:,0]-CASH_M).mean()/a[:,0].std()*np.sqrt(12))
    dsh = lambda a: ((a[:,0]-CASH_M).mean()/a[:,0].std() - (a[:,1]-CASH_M).mean()/a[:,1].std())*np.sqrt(12)
    bs = boot(df, sh); bd = boot(df, dsh)
    hold = df[df.index>HOLD]
    bdh = boot(hold, dsh)
    rows.append(dict(idea=c, sharpe=sh(df.values), sh_lo=np.percentile(bs,5), sh_hi=np.percentile(bs,95), d_sharpe_vs_ctrl=dsh(df.values), p_beats_ctrl=(bd>0).mean(),
                     d_sharpe_hold=dsh(hold.values), p_beats_ctrl_hold=(bdh>0).mean(), corr_ctrl=df.corr().iloc[0,1], n=len(df)))
BT = pd.DataFrame(rows).set_index('idea'); BT.to_csv('results/stage14_bootstrap.csv', float_format='%.4f')
print('\n--- bootstrap vs control (2008-04+)'); print(BT.round(3).to_string())
# ---------------- C. portfolio marginal value ----------------
BUCKET = ['Elendel (control)','Zenith','csm_absolute score','Residual mom (live-like)']
common = S.loc['2008-04-30':].dropna(subset=BUCKET)
B = common[BUCKET].mean(axis=1)
def pstats(r):
    s=stats(r); h=stats(r[r.index>HOLD]); return dict(cagr=s['cagr'],vol=s['vol'],sharpe=s['sharpe'],maxdd=s['maxdd'],calmar=s['calmar'],sharpe_hold=h['sharpe'],maxdd_hold=h['maxdd'],cagr_hold=h['cagr'])
base = pstats(B); print('\nBUCKET (EW of 4 live-like books, chassis applied):', {k:round(v,3) for k,v in base.items()})
rows=[]
cands=[c for c in S.columns if c not in BUCKET]
for c in cands:
    x = S[c].reindex(B.index)
    ok = x.notna()
    if ok.sum()<100: continue
    Bm = B[ok]; xm = x[ok]
    bb = pstats(Bm)
    for w in (0.2,0.35):
        p = (1-w)*Bm + w*xm
        ps = pstats(p)
        shf = lambda a,w=w: (((1-w)*a[:,0]+w*a[:,1]).mean()-CASH_M)/((1-w)*a[:,0]+w*a[:,1]).std()*np.sqrt(12)
        bshf = lambda a: (a[:,0].mean()-CASH_M)/a[:,0].std()*np.sqrt(12)
        dd = pd.concat([Bm,xm],axis=1).values
        bsamp = boot(pd.DataFrame(dd), lambda a,w=w: shf(a)-bshf(a), reps=2000)
        rows.append(dict(idea=c, w=w, window_start=Bm.index[0].date(), corr_to_bucket=np.corrcoef(Bm,xm)[0,1],
            d_cagr=ps['cagr']-bb['cagr'], d_sharpe=ps['sharpe']-bb['sharpe'], d_maxdd=ps['maxdd']-bb['maxdd'], d_calmar=ps['calmar']-bb['calmar'],
            d_sharpe_hold=ps['sharpe_hold']-bb['sharpe_hold'], d_maxdd_hold=ps['maxdd_hold']-bb['maxdd_hold'], p_sharpe_up=(bsamp>0).mean(),
            base_sharpe=bb['sharpe'], base_maxdd=bb['maxdd'], new_sharpe=ps['sharpe'], new_maxdd=ps['maxdd'], new_cagr=ps['cagr']))
PM = pd.DataFrame(rows); PM.to_csv('results/stage14_portfolio_marginal.csv', index=False, float_format='%.4f')
print('\n--- marginal value in a blend with the live-like bucket'); print(PM[PM.w==0.2].round(3).to_string(index=False))

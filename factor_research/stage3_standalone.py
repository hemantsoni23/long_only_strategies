import pickle, numpy as np, pandas as pd
from evaluate import composite, SPLIT
from portfolio_lab import topn_book, stats
from factors import FAMILY
st = pickle.load(open('.cache/state.pkl','rb'))
F, FWD, U = st['F'], st['FWD'], st['U']
out=[]
for uname in ['U1_liquid1000','U2_live_trend']:
    mask=U[uname]
    ref = {'ELEN':topn_book(composite(F,['a3_rs_high','q5_126'],mask),mask,FWD[1])['net'],
           'ZEN':topn_book(composite(F,['a1_52wh','q5_189'],mask),mask,FWD[1])['net']}
    for n,fr in list(F.items()):
        bk = topn_book(fr,mask,FWD[1])
        if len(bk)<60: continue
        net=bk['net']; d=net[net.index<=SPLIT]; h=net[net.index>SPLIT]
        sd,sh=stats(d),stats(h); sa=stats(net)
        out.append(dict(universe=uname,factor=n,family=FAMILY[n],cagr=sa['cagr'],sharpe=sa['sharpe'],maxdd=sa['maxdd'],
            sharpe_disc=sd.get('sharpe'),sharpe_hold=sh.get('sharpe'),cagr_disc=sd.get('cagr'),cagr_hold=sh.get('cagr'),
            turnover=bk['turnover'].mean(),
            hit_vs_mkt=(bk['net']>bk['ew_mkt']).mean(),
            corr_elen=net.corr(ref['ELEN']),corr_zen=net.corr(ref['ZEN']),
            n_months=len(bk)))
    for k,v in ref.items():
        s=stats(v); out.append(dict(universe=uname,factor='BOOK_'+k,family='LIVE',cagr=s['cagr'],sharpe=s['sharpe'],maxdd=s['maxdd'],
            sharpe_disc=stats(v[v.index<=SPLIT]).get('sharpe'),sharpe_hold=stats(v[v.index>SPLIT]).get('sharpe'),
            cagr_disc=stats(v[v.index<=SPLIT]).get('cagr'),cagr_hold=stats(v[v.index>SPLIT]).get('cagr'),turnover=np.nan,hit_vs_mkt=np.nan,corr_elen=np.nan,corr_zen=np.nan,n_months=len(v)))
    print(uname,'done',flush=True)
pd.DataFrame(out).to_csv('results/stage3_standalone_books.csv',index=False,float_format='%.4f')

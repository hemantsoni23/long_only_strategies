import pickle, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
from data import load_panels
from evaluate import evaluate_factor, composite, zscore, SPLIT
from portfolio_lab import topn_book, stats
st = pickle.load(open('.cache/state.pkl','rb')); F,FWD,U,sig = st['F'],st['FWD'],st['U'],st['sig']
UN = pickle.load(open('.cache/extra_universes.pkl','rb')); allU = dict(U); allU.update(UN)
P = load_panels(); b = P['bench']
bull = (b > b.rolling(200,min_periods=150).mean()).reindex(sig).fillna(True)
cash_m = (1.06)**(1/12)-1

PACKS = {
 'P1_quality_intraday_trend':   ['intra_over_252','low_ulcer_252'],
 'P2_low_risk_sleeve':          ['lowvol_126','low_ulcer_252'],
 'P3_sharpe_mom_painaware':     ['csm_abs_dual_sharpe','low_pain_126'],
 'P4_residual_plus_persistence':['mom_resid_12_1','q5_126'],
 'P5_long_anchor_painaware':    ['hi_3y','low_pain_126'],
 'P6_tight_range_trend':        ['tight_close_15','q5_126'],
 'P7_intraday_plus_momentum':   ['intra_over_126','mom_resid_sharpe'],
 'P8_persistence_alone':        ['q5_126'],
}
REF = {'LIVE_elendel':['a3_rs_high','q5_126'], 'LIVE_zenith':['a1_52wh','q5_189'], 'csm_absolute_score':['csm_abs_dual_sharpe']}
UNIVS = ['U1_liquid1000','U4_top250','U7_midsmall_301_1000','U3_top300']
rows=[]; brows=[]
for u in UNIVS:
    m = allU[u]
    elen = composite(F,REF['LIVE_elendel'],m)
    elen_book = topn_book(elen,m,FWD[1],n=15)['net']
    allp = {**REF, **PACKS}
    for pn, comps in allp.items():
        sc = composite(F, comps, m) if len(comps)>1 else F[comps[0]].where(m)
        r,_ = evaluate_factor(pn, sc, m, FWD, base_rank=elen); r['universe']=u; r['components']='+'.join(comps); rows.append(r)
        for n in (15,):
            bk = topn_book(sc,m,FWD[1],n=n)
            for gate in ('none','sma200_gate50'):
                net = bk['net'].copy()
                if gate!='none':
                    expo = np.where(bull.reindex(net.index).values,1.0,0.5)
                    net = expo*bk['net'] + (1-expo)*cash_m
                s=stats(net); sd=stats(net[net.index<=SPLIT]); sh=stats(net[net.index>SPLIT])
                brows.append(dict(universe=u,pack=pn,gate=gate,n=n,cagr=s['cagr'],vol=s['vol'],sharpe=s['sharpe'],maxdd=s['maxdd'],calmar=s['calmar'],
                    sharpe_disc=sd.get('sharpe'),sharpe_hold=sh.get('sharpe'),cagr_disc=sd.get('cagr'),cagr_hold=sh.get('cagr'),maxdd_hold=sh.get('maxdd'),
                    turnover=bk['turnover'].mean(),hit_vs_mkt=(bk['net']>bk['ew_mkt']).mean(),corr_elen_book=net.corr(elen_book) if pn!='LIVE_elendel' else 1.0))
    print(u,'done',flush=True)
pd.DataFrame(rows).to_csv('results/stage11_packs_ic.csv',index=False,float_format='%.5f')
pd.DataFrame(brows).to_csv('results/stage11_packs_books.csv',index=False,float_format='%.4f')
pd.set_option('display.width',260); pd.set_option('display.max_columns',50); pd.set_option('display.max_rows',200)
d=pd.DataFrame(rows)
for u in UNIVS:
    print('=====',u); print(d[d.universe==u][['factor','ic_1','ic_3','icir_3','hit_3','t_3','ic_6','ic_12','peak_h_ic','ic_disc_3','ic_hold_3','top20_winmed_3','corr_elendel','inc_ic_3','rank_autocorr_1m']].round(3).to_string(index=False))
bb=pd.DataFrame(brows)
for u in UNIVS:
    print('===== books',u); print(bb[(bb.universe==u)][['pack','gate','cagr','sharpe','maxdd','calmar','sharpe_disc','sharpe_hold','cagr_hold','maxdd_hold','turnover','corr_elen_book']].round(3).to_string(index=False))

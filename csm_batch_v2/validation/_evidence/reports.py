"""Write six concise Markdown reports, predominantly metric/threshold tables."""
from pathlib import Path
import hashlib,json
import numpy as np
import pandas as pd
E=Path(__file__).resolve().parent;DEST=E.parent;ROOT=DEST.parent
D=json.loads((E/'data_audit.json').read_text()); unchanged=json.loads((E/'data_unchanged.json').read_text());parity=json.loads((E/'parity.json').read_text()); behavior=json.loads((E/'behavior.json').read_text())
C={w:pd.read_csv(E/f'{w}_cells.csv').set_index('cell') for w in ('early','late','full')}
S={w:pd.read_csv(E/f'{w}_signal_summary.csv') for w in ('early','late')}; B={w:pd.read_csv(E/f'{w}_signal_breadth.csv').iloc[0] for w in ('early','late')};Q={w:pd.read_csv(E/f'{w}_signal_quantiles.csv') for w in ('early','late')};FF={w:pd.read_csv(E/f'{w}_signal_ffill.csv') for w in ('early','late')}
X=pd.read_csv(E/'exit_summary.csv').set_index('reason');R=pd.read_csv(E/'exit_rotations.csv'); O=pd.read_csv(E/'outliers.csv'); trades=pd.read_csv(E/'full_trades.csv',parse_dates=['Entry_Date','Exit_Date'])
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def f(x,n=2):
 try:
  x=float(x)
  return f'{x:.{n}f}' if np.isfinite(x) else 'N/A'
 except (ValueError,TypeError):return str(x)
def table(headers,rows):
 def cell(x):return str(x).replace('|','/').replace('\n',' ')
 return '| '+' | '.join(headers)+' |\n| '+' | '.join(['---']*len(headers))+' |\n'+''.join('| '+' | '.join(cell(x) for x in row)+' |\n' for row in rows)+'\n'
def save(name,text): (DEST/name).write_text(text)
def sig(w,rung,h):return S[w].query('rung == @rung and horizon == @h').iloc[0]
def direction(ok):return 'PASS' if ok else 'FAIL'
def common():
 return table(['Universe card','Setting'],[['Source',f"{D['files']:,} raw OHLCV CSVs; {D['first']} to {D['last']}"],['Eligibility','₹10 price floor; liquidity top 1,000; 252 prior observed bars; circuit, SMA-200 and prior-month return filters'],['Portfolio / costs','30 names; 2-month rebalance; 0.3% per weight turnover; cash rate 0%'],['Windows',f"Early 2001–2012; late 2013–{D['last']}; full 2002–{C['full'].loc['baseline','end']}"],['Accounting convention','Exit-day gains/losses omitted at user request'],['Stage 1 status','Data adjustment unresolved; survivorship coverage flagged']])
# Stage 1
rows=[['CSV files',f"{D['files']:,}",'—','Observed'],['Data period',f"{D['first']} → {D['last']}",'—','Observed'],['Early warmup',f"{(pd.Timestamp(C['early'].loc['baseline','start'])-pd.Timestamp(C['early'].loc['baseline','load_start'])).days} calendar days",'450 calendar days requested','INCOMPLETE'],['Symbols last seen >183 days before panel end',f"{D['last_seen_before_cutoff']} / {D['files']} ({D['last_seen_pct']:.2f}%)",'Flag proxy <2%','FLAG; delistings unverified'],['Extreme sorted adjacent valid-close changes ≤−40% or ≥+300%',f"{D['extreme_close_changes']:,}",'No unadjusted jumps','FAIL / needs action review'],['Duplicate dates among positive-close rows',f"{D['counts'].get('duplicate_dates',0):,}",'Loader keeps last exact timestamp','Check data'],['Nonpositive / non-finite close or missing date',f"{D['counts'].get('nonpositive_or_missing',0):,}",'0','FAIL'],['Out-of-order valid rows',f"{D['counts'].get('out_of_order',0):,}",'Sorted panel','Sorted by loader'],['Listing age',f"Early {int(B['early'].under252)}/{int(B['early'].eligible_symbol_months):,}; late {int(B['late'].under252)}/{int(B['late'].eligible_symbol_months):,} below 252","≥252 prior observed bars",'PASS observed-count test'],['Liquidity rolling window','63 days; min_periods=21','min_periods required','PASS'],['Early breadth: months <8',f"{int(B['early'].below8)} / {int(B['early'].months)} ({B['early'].below8_pct:.2f}%)",'Exclude each month','FAIL breadth'],['Late breadth: months <8',f"{int(B['late'].below8)} / {int(B['late'].months)} ({B['late'].below8_pct:.2f}%)",'Exclude each month','PASS'],['Source CSVs added/removed/metadata-changed',f"{unchanged['added']} / {unchanged['removed']} / {unchanged['metadata_changed']}",'0 / 0 / 0','PASS metadata check']]
text='# Stage 1 — Data integrity & universe\n\n**Verdict: FAIL / UNRESOLVED**\n\n'+common()+table(['Check','Measured','Playbook bar','Result'],rows)
text+=table(['Window','Months','Mean names','Median names','Minimum names','Months <8'],[[w,int(B[w].months),f(B[w].mean_names),f(B[w].median_names),int(B[w].min_names),int(B[w].below8)] for w in ('early','late')])
text+='### Synthetic behavior checks\n\n'+table(['Check','Measured','Expected / rule','Result'],[['Stop uses prior peak',f"Same-day trigger {behavior['stop_prior_peak']['same_day_triggered']}; next-day trigger {behavior['stop_prior_peak']['next_day_triggered']}",'False / True','PASS'],['Missing current-day open',f"Forward-filled to {behavior['missing_open']['filled_open']}",'Do not assume stale quote executable','FLAG'],['Rebalance guard',f"{behavior['guard']['raw_ranked']} ranked; {behavior['guard']['positive_momentum']} positive; {behavior['guard']['old_weights_retained']} prior weights retained",'Raw-pool shortage guard; thin positive selection allowed','FLAG'],['Force vs existing stop',f"Existing stop 85; reported fill {behavior['force_vs_standing']['reported_fill']:.2f}",'Standing stop fill model 84.745 if crossed without a gap','FLAG']])
text+='| Interpretation | Limitation |\n| --- | --- |\n| Survivorship | Last observation is a proxy; it does not prove delisting or coverage. |\n| Corporate actions | Adjacent observations may cross gaps; large changes are flags, not confirmed splits or errors. |\n| Listing history | Counts non-null prices in the loaded buffer; full exchange listing history is not independently verified. |\n| Source check | File sizes and modification times compared before/after; content hashes are in `_evidence/data_manifest.csv`. |\n| Stop example | Actual intraday gaps may change fills; the synthetic case compares the two programmed models. |\n'
save('01_DATA_INTEGRITY.md',text)
# Stage 2
text='# Stage 2 — Core signal diagnostics\n\n**Verdict: FAIL / INCOMPLETE**\n\n'+common()
rows=[]
for w in ('early','late'):
 for rung in ['L0_raw','L1_price','L2_liquidity','L3_tradeable','L4_positive','L5_top30']:
  q=sig(w,rung,3);rows.append([w,rung,int(q.months),f(q.mean_ic,4),f(q.icir,3),f(q.nw_t),f(q.excluded_pct)+'%'])
text+='### Filter ladder — three-month forward return\n\n'+table(['Window','Rung','Months','Mean IC','ICIR','NW-t','Excluded'],rows)
rows=[]
for w in ('early','late'):
 for h in [1,3,6,12]:
  a=sig(w,'L0_raw',h);b=sig(w,'L3_tradeable',h);rows.append([w,h,f(a.mean_ic,4),f(a.nw_t),f(b.mean_ic,4),f(b.nw_t),f(b.excluded_pct)+'%'])
text+='### Horizon decay\n\n'+table(['Window','Months forward','L0 IC','L0 NW-t','L3 IC','L3 NW-t','L3 excluded'],rows)
rows=[]
for w in ('early','late'):
 for h in [1,3,6,12]:
  b=sig(w,'L3_tradeable',h);qs=Q[w].query('horizon == @h').sort_values('quintile'); vals=[f(x)+'%' for x in qs.mean_return_pct]
  rows.append([w,h]+vals+[f'{int(b.quintile_increasing)}/4 ({25*int(b.quintile_increasing)}%)',f(b.spread_nw_t),direction(b.quintile_increasing>=4 and b.spread_nw_t>=2)])
text+='### L3 quantiles\n\n'+table(['Window','Horizon','Q1','Q2','Q3','Q4','Q5','Increasing pairs','Spread NW-t','≥80% and ≥2'],rows)
rows=[]
for w in ('early','late'):
 q=sig(w,'L3_tradeable',3);r=sig(w,'L0_raw',3);z=FF[w].query("rung == 'L3_tradeable' and horizon == 3").iloc[0]
 rows += [[w,'L0 / L3 NW-t',f'{f(r.nw_t)} / {f(q.nw_t)}','both ≥2',direction(r.nw_t>=2 and q.nw_t>=2)], [w,'L3 months excluded',f(q.excluded_pct)+'%','≤15%',direction(q.excluded_pct<=15)],[w,'Top two years share of signed IC',f(q.top2_year_share_pct)+'%','≤50%','PASS' if q.top2_year_share_pct<=50 else 'CONCENTRATED'],[w,'Equal / traded-value-weighted IC',f'{f(q.mean_ic,4)} / {f(q.weighted_liquidity_ic,4)}','market-value weighting requested','INCOMPLETE: no point-in-time market cap'],[w,'Raw / forward-filled IC',f'{f(z.raw_ic,4)} / {f(z.ffill_ic,4)}',f'delta {f(z.difference,5)}','PROXY ONLY: delistings unverified']]
text+='### Three-month gate checks\n\n'+table(['Window','Check','Measured','Bar','Result'],rows)
text+='| Method | Setting |\n| --- | --- |\n| Signal | Spearman rank correlation; month-end close-to-close forward returns. |\n| NW-t | Bartlett Newey–West lag = horizon; missing calendar months remain gaps. |\n| Ranking | L3 includes trend, falling-knife and age; L5 is top 30 before hysteresis. |\n| Weighting | Traded-value weights are a liquidity proxy, not market-cap weights. |\n| Survivorship | IC is a potentially survivorship-biased upper bound; forward-fill sensitivity is not verified delisting treatment. |\n| Stage result | Three-month early breadth and both windows’ monotonicity fail; data prerequisites remain unresolved. |\n'
save('02_SIGNAL_DIAGNOSTICS.md',text)
# Stage 3
text='# Stage 3 — Universe, parameter robustness & ablation\n\n**Verdict: FAIL / DATA-CONDITIONAL**\n\n'+common()
labels=['top_100','top_250','top_500','top_750','top_1000','top_1500','band_0_500','band_500_1000','band_1000_1500','band_1000_2000']
for w in ('early','late'):
 d=C[w]; rows=[]
 for k in labels:
  a=d.loc[k];rows.append([k,f(a.sharpe),f(a.calmar),f(a.cagr_pct)+'%',f(a.maxdd_pct)+'%',f(a.vol_pct)+'%'])
 text+=f'### {w.title()} window: universe sweep\n\n'+table(['Liquidity rank','Sharpe','Calmar','CAGR','Max DD','Volatility'],rows)
 core=d.loc[[f'top_{n}' for n in (250,500,750,1000,1500)]];ranges=[core.sharpe.max()-core.sharpe.min(),core.calmar.max()-core.calmar.min(),core.cagr_pct.max()-core.cagr_pct.min(),core.maxdd_pct.max()-core.maxdd_pct.min()]
 text+=table(['Core top-250–1500 metric','Range','Pass bar','Result'],[[n,f(v),bar,direction(v<=lim)] for n,v,lim,bar in zip(['Sharpe','Calmar','CAGR (pp)','Max DD (pp)'],ranges,[.35,.5,8,10],['≤0.35','≤0.50','≤8 pp','≤10 pp'])]+[['Any core Sharpe ≤0',int((core.sharpe<=0).sum()),'0',direction((core.sharpe>0).all())]])
 bs=S[w].query("horizon == 3 and rung.str.startswith('band_')",engine='python');text+=table(['3m signal liquidity band','Mean IC','ICIR','NW-t','Months excluded'],[[r.rung,f(r.mean_ic,4),f(r.icir,3),f(r.nw_t),f(r.excluded_pct)+'%'] for r in bs.itertuples(index=False)])
 coreic=bs.set_index('rung').loc[[f'band_0_{n}' for n in (250,500,750,1000,1500)]];icir_range=coreic.icir.max()-coreic.icir.min();text+=table(['IC robustness measure','Measured','Reference','Result'],[['Core ICIR range',f(icir_range,3),'≤0.35 Sharpe analogue',direction(icir_range<=.35)]])
text+='### Parameter sweeps — Sharpe\n\n';params=[x for x in C['early'].index if x.startswith(('lookback_','rebalance_','positions_','stop_','regime_'))];text+=table(['Setting','Early','Late'],[[x,f(C['early'].loc[x,'sharpe']),f(C['late'].loc[x,'sharpe'])] for x in params])
pairs=[('Lookback 10 vs 14 months','lookback_10','lookback_14'),('Positions 24 vs 36','positions_24','positions_36'),('Hard stop 12% vs 18%','stop_0.12','stop_0.18'),('Regime cutoff −8% vs −12%','regime_-0.08','regime_-0.12')];rows=[]
for w in ('early','late'):
 for name,a,b in pairs:
  diff=abs(C[w].loc[a,'sharpe']-C[w].loc[b,'sharpe']);rows.append([w,name,f(diff),'≤0.40',direction(diff<=.4)])
 rows.append([w,'Rebalance ±20%','N/A: monthly integer rounds to 2','five points requested','INCOMPLETE'])
text+=table(['Window','Approximate ±20% setting','Sharpe range','Bar','Result'],rows)
for w in ('early','late'):
 d=C[w];base=d.loc['baseline'];cols=['sharpe','calmar','stability','average_dd_pct','turnover_pct'];rows=[]
 for key in ['baseline','ablate_rank_exit','ablate_vol_stop','ablate_bear_exposure','ablate_vol_target','ablate_corr_guard','ablate_positive_momentum']:
  r=d.loc[key];vals=[];fails=[]
  for col in cols:
   val=float(r[col]);bv=float(base[col]);delta=(val/bv-1)*100 if bv else np.nan;vals.append(f'{f(val)} ({delta:+.1f}%)' if np.isfinite(delta) else f'{f(val)} (N/A)')
   if (val<.85*bv if col in ['sharpe','calmar'] else val>(1.25 if col=='turnover_pct' else 1.20)*bv):fails.append(col)
  rows.append([key]+vals+[', '.join(fails) or 'None'])
 text+=f'### {w.title()} ablation — value (relative change vs baseline)\n\n'+table(['Cell','Sharpe','Calmar','12m return std','Avg DD depth %','Annual turnover %','Regression flags'],rows)
rows=[]
for r in O.itertuples(index=False):rows.append([r.cell,r.date,f(r.portfolio_day_pct)+'%',r.ticker,f(r.previous_close)+' → '+f(r.close),f(r.stock_day_pct)+'%',f(r.sharpe)+' → '+f(r.zero_day_sharpe)])
text+='### Extreme-day sensitivity\n\n'+table(['Cell','Date','Portfolio day','Candidate name','Close before → after','Stock day','Sharpe → zero whole day'],rows)
text+='| Method / limitation | Setting |\n| --- | --- |\n| Sweep | Lookback 7/10/12/14/17 months; positions 18/24/30/36/42; stops 9/12/15/18/21%; regime cutoffs −6/−8/−10/−12/−14%. |\n| Rebalance | Integer monthly cadence 1/2/3; ±20% of 2 rounds to 2. |\n| Ablation | Six leave-one-out components; Sharpe/Calmar ≤15% regression; stability/DD ≤20%; turnover ≤25%. No winner selected. |\n| Extreme-day test | Sets the entire portfolio day to zero without recomputing holdings; not an adjusted backtest. Candidate ticker is based on trade dates, not exact intraday attribution. |\n| Costs | Same 0.3% one-way cost in every liquidity band; wider-band performance has a capacity caveat. Turnover is half the absolute weight-change sum. |\n| Status | Numerical cliffs and data-quality issues prevent a robustness pass. |\n'
save('03_ROBUSTNESS_ABLATION.md',text)
# Stage 4
text='# Stage 4 — Bidirectional IS/OOS validation\n\n**Verdict: FAIL / NOT BLIND**\n\n'+common()
rows=[]
for w,label in [('early','2001–2012'),('late',f"2013–{C['late'].loc['baseline','end']}"),('full',f"2002–{C['full'].loc['baseline','end']}")]:
 a=C[w].loc['baseline'];rows.append([label,f(a.sharpe),f(a.sortino),f(a.calmar),f(a.cagr_pct)+'%',f(a.maxdd_pct)+'%',f(a.beta),f(a.alpha_pct)+'%',f(a.trade_win_pct)+'%',f(a.profit_factor_pct),'N/A',f(a.payoff),f(a.hold_days)])
text+='### Scorecard\n\n'+table(['Window','Sharpe','Sortino','Calmar','CAGR','Max DD','Beta','Alpha / yr','Trade win','PF (%)','PF ($)','Payoff','Avg hold days'],rows)
rows=[]
for name,iw,ow in [('A','early','late'),('B','late','early')]:
 a=C[iw].loc['baseline'];b=C[ow].loc['baseline'];checks=[('Sharpe OOS / IS',b.sharpe/a.sharpe,.6,'≥0.60','min'),('Calmar OOS / IS',b.calmar/a.calmar,.6,'≥0.60','min'),('CAGR OOS / IS',b.cagr_pct/a.cagr_pct,.5,'≥0.50','min'),('Max DD OOS / IS',abs(b.maxdd_pct/a.maxdd_pct),1.5,'≤1.50','max'),('OOS Sharpe',b.sharpe,0,'>0','positive'),('OOS L0 3m NW-t',sig(ow,'L0_raw',3).nw_t,1.5,'≥1.50','min'),('OOS L3 3m NW-t',sig(ow,'L3_tradeable',3).nw_t,1.5,'≥1.50','min')]
 for metric,value,limit,bar,kind in checks:rows.append([name,f'{iw} → {ow}',metric,f(value,3),bar,direction(value>0 if kind=='positive' else (value>=limit if kind=='min' else value<=limit))])
split_verdict='FAIL' if any(x[-1]=='FAIL' for x in rows) else 'PASS'
text+='### Playbook split gates\n\n'+table(['Direction','IS → OOS','Metric','Measured','Bar','Result'],rows)
text+=table(['Validation condition','Evidence','Verdict'],[['Replay vs original runner',f"{parity['reference_rows']} rows; max difference {parity['max_abs_equity_difference']:.3g}",'PASS' if parity['same_dates'] and parity['max_abs_equity_difference']<1e-10 else 'FAIL'],['Strategy file SHA-256',H(ROOT/'csm_stock_strategy.py'),'VERSION'],['Backtest file SHA-256',H(ROOT/'csm_stock_backtest.py'),'VERSION'],['Both split directions clear all numeric gates','A and B above',split_verdict],['Previously untouched OOS','Both halves previously viewed','NOT BLIND'],['Independent tuning per direction','Baseline fixed before sweeps; no winner selected','No independent tuning claimed'],['Stress regime A OOS','2018, 2020, 2022 present','COVERED'],['Stress regime B OOS','2008 present','COVERED'],['Full sample','2002 → latest complete year','INFORMATIONAL ONLY'],['Profit factor in currency','No reliable share-level P&L','N/A'],['Beta / alpha benchmark','Runner’s observed-stock equal-weight benchmark; return clipping ±50%','PROXY']])
text+=table(['OOS-look log','Date / result'],[['Prior review','2026-11-02: both full split windows and 2002–2025 viewed; user modified strategy during earlier review; modification count unknown'],['This validation','2026-11-03: both full split windows and 2002–2025 full period viewed; no strategy changes'],['Post-look modification count','Unknown from available record; fresh untouched holdout not established']])
save('04_IS_OOS_VALIDATION.md',text)
# Stage 5
text='# Stage 5 — Exit quality\n\n**Verdict: DIAGNOSTIC / INCOMPLETE**\n\n'+common();rows=[]
for key in ['HARD_STOP_HIT','VOL_STOP_HIT','FORCE_EXIT','RANK_EXIT','REBAL_EXIT','CRASH_GUARD','ATR_STOP_HIT','PEAK_STOP_HIT']:
 if key in X.index:
  a=X.loc[key];n=int(a.exits);available=int(a.available_both);verdict=a.verdict;confidence='≥30' if n>=30 else '<30; directional'
  rows.append([key,n,available,f(a.mean20_pct)+'%',f(a.mean60_pct)+'%',f(a.mean20_60_pct)+'%',verdict,confidence])
 else:rows.append([key,0,0,'N/A','N/A','N/A','Not triggered','<30'])
text+='### Post-exit continuation\n\n'+table(['Reason','Exits','20d & 60d available','20d excess','60d excess','Mean excess','Rule verdict','Sample'],rows)
text+='### Rotation comparisons — entered vs exited on same date\n\n'+table(['Exit reason','Horizon','Matched dates','Entered mean','Exited mean','Difference'],[[r.reason,f'{int(r.horizon_days)}d',int(r.dates),f(r.entered_mean_pct)+'%',f(r.exited_mean_pct)+'%',f(r.difference_pp)+' pp'] for r in R.itertuples(index=False)])
end=trades[trades.Exit_Reason=='END_OF_PERIOD'];outside=int((end.Exit_Date.dt.to_period('M')!=trades.Exit_Date.max().to_period('M')).sum());share=len(end)/len(trades)*100
text+=table(['Check','Measured','Bar','Result'],[['END_OF_PERIOD outside final month',f'{outside} / {len(trades)}','<5%','PASS' if outside/len(trades)<.05 else 'FAIL'],['END_OF_PERIOD total',f'{len(end)} / {len(trades)} ({share:.2f}%)','<5%','PASS' if share<5 else 'FAIL'],['FORCE_EXIT trades',int(X.loc['FORCE_EXIT','exits']) if 'FORCE_EXIT' in X.index else 0,'≥30','DIRECTIONAL'],['Paired REBAL_EXIT','Same-date entry and exit groups','true replacement pairs','INCOMPLETE']])
text+='| Method / limitation | Setting |\n| --- | --- |\n| Excess return | Post-exit close-to-close return less equal-weight signal-eligible universe; 20d and 60d. |\n| Benchmark | Daily constituent returns clipped ±50%; final membership carried forward after final factor month. |\n| Verdict rule | Mean ≤−1% working; ≥+1% too early; otherwise neutral. |\n| Rotation | Mean entries versus exits on same date; no one-to-one replacement mapping. |\n| Data | Raw prices and missing/delisted endpoints limit reliability; fewer than 30 trades is directional only. |\n'
save('05_EXIT_QUALITY.md',text)
# Verdict (one short row per stage)
e3=sig('early','L3_tradeable',3);l3=sig('late','L3_tradeable',3);e=C['early'].loc['baseline'];l=C['late'].loc['baseline'];cliff=abs(C['late'].loc['positions_24','sharpe']-C['late'].loc['positions_36','sharpe'])
rows=[['1','[Data integrity](01_DATA_INTEGRITY.md)','FAIL',f"{D['extreme_close_changes']} extreme price changes; delisting proxy {D['last_seen_pct']:.2f}% vs 2% flag"],['2','[Signal diagnostics](02_SIGNAL_DIAGNOSTICS.md)','FAIL',f"Early excluded {e3.excluded_pct:.2f}% vs ≤15%; early/late monotonic {int(e3.quintile_increasing)*25}% / {int(l3.quintile_increasing)*25}% vs ≥80%"],['3','[Robustness](03_ROBUSTNESS_ABLATION.md)','FAIL / CONDITIONAL',f'Late ±20% position-count Sharpe swing {cliff:.2f} vs ≤0.40; extreme TIL price observation'],['4','[IS/OOS](04_IS_OOS_VALIDATION.md)','FAIL / NOT BLIND',f"Reverse-split drawdown ratio {abs(e.maxdd_pct/l.maxdd_pct):.2f} vs ≤1.50"],['5','[Exit quality](05_EXIT_QUALITY.md)','INCOMPLETE','Stop verdicts and same-date rotation tables computed; true paired replacement and clean prices unavailable']]
text='# Stages 1–5 — final verdict\n\n**OVERALL: NOT VALIDATED**\n\n'+table(['Stage','Test','Verdict','Key result'],rows)
text+=table(['Reference figure','Measured','Interpretation'],[['Full-sample CAGR / Sharpe / max DD',f"{f(C['full'].loc['baseline','cagr_pct'])}% / {f(C['full'].loc['baseline','sharpe'])} / {f(C['full'].loc['baseline','maxdd_pct'])}%",'Informational; raw data and user-specified accounting'],['Historical holdouts','Both periods previously viewed','Not independently blind'],['Source folder metadata changed',f"{unchanged['metadata_changed']} files; {unchanged['added']} added; {unchanged['removed']} removed",'Read-only audit'],['Replay versus original runner',f"Max absolute equity difference {parity['max_abs_equity_difference']:.3g}",'PASS' if parity['same_dates'] and parity['max_abs_equity_difference']<1e-10 else 'FAIL']])
text+='| Next required step | Requirement |\n| --- | --- |\n| Data | Verify corporate actions and delisted names in a separate read-only or derived dataset. |\n| Validation | Re-run failed checks on clean data and establish an independent holdout. |\n'
save('VERDICT.md',text)
print('WROTE',', '.join(x.name for x in DEST.glob('*.md')))

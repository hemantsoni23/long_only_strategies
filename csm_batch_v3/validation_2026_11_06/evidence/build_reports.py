"""Generate stage reports from the updated v3 validation evidence."""
from pathlib import Path
import json
import numpy as np,pandas as pd
E=Path(__file__).resolve().parent;D=E.parent
read=lambda n,**k:pd.read_csv(E/n,**k)
def fmt(x,n=3):
 if pd.isna(x):return '—'
 if isinstance(x,(float,np.floating)):return f'{x:.{n}f}'
 return str(x)
def table(d,n=3):
 lines=['| '+' | '.join(map(str,d.columns))+' |','| '+' | '.join('---' for _ in d.columns)+' |']
 for row in d.itertuples(index=False,name=None):lines.append('| '+' | '.join(fmt(x,n).replace('|','/') for x in row)+' |')
 return '\n'.join(lines)
def write(n,s):(D/n).write_text(s.strip()+'\n')
def base(w,mode='universe'):
 d=read(f'{w}_{mode}_cells.csv');return d[d.cell=='baseline'].iloc[0]
def sig(w,r,h=3):
 d=read(f'signal_{w}_summary.csv');return d[(d.rung==r)&(d.horizon==h)].iloc[0]
def utable(w):
 d=read(f'{w}_universe_cells.csv');b=d[d.cell=='baseline'].iloc[0];br=read(f'signal_{w}_band_breadth.csv').set_index('band');rows=[]
 for _,r in d[d.cell!='baseline'].iterrows():
  k=('band_0_'+r.cell.split('_')[1] if r.cell.startswith('top_') else r.cell);z=sig(w,k);x=br.loc[k];rows.append({'Liquidity rank':r.cell.replace('top_','1–').replace('band_','').replace('_','–'),'CAGR %':r.cagr_pct,'Sharpe':r.sharpe,'Δ Sharpe':r.sharpe-b.sharpe,'Max DD %':r.maxdd_pct,'Calmar':r.calmar,'Δ Calmar':r.calmar-b.calmar,'3m IC':z.mean_ic,'NW-t':z.nw_t,'Median pool':x['median'],'Months <8 %':x.below8_pct,'ETF exposure %':r.etf_exposure_pct})
 return pd.DataFrame(rows)
def dispersion(w):
 d=read(f'{w}_universe_cells.csv').set_index('cell').loc[[f'top_{n}' for n in [250,500,750,1000,1500]]];return {'Period':w,'Sharpe range':d.sharpe.max()-d.sharpe.min(),'Calmar range':d.calmar.max()-d.calmar.min(),'CAGR range pp':d.cagr_pct.max()-d.cagr_pct.min(),'MaxDD range pp':d.maxdd_pct.max()-d.maxdd_pct.min(),'Min Sharpe':d.sharpe.min()}
def annual(w):
 d=read(f'{w}_universe_yearly.csv');d=d[d.cell.isin(['top_250','top_500','top_750','top_1000','top_1500','band_500_1000','band_1000_1500','band_1000_2000'])];return d.pivot(index='year',columns='cell',values='return_pct').reset_index().rename(columns=lambda x:str(x).replace('top_','1–').replace('band_','').replace('_','–'))
def costs(w):
 d=read(f'{w}_cost_stress.csv');return d[d.cell.isin(['baseline','top_500','band_500_1000','band_1000_1500','band_1000_2000'])][['cell','one_way_cost_pct','cagr_pct','sharpe','maxdd_pct','calmar']]
def ladder(w):
 d=read(f'signal_{w}_summary.csv');d=d[(d.horizon==3)&~d.rung.str.startswith('band_')];return d[['rung','n_months','mean_ic','icir','t_stat','nw_t','positive_ic_pct','average_names','months_lt8_pct']]
def horizons(w):
 d=read(f'signal_{w}_summary.csv');d=d[d.rung=='L3_tradeable'];a=read(f'signal_{w}_accuracy_monthly.csv');rows=[]
 for _,r in d.iterrows():
  z=a[a.horizon==r.horizon];rows.append({'Horizon months':r.horizon,'IC months':r.n_months,'IC':r.mean_ic,'ICIR':r.icir,'t-stat':r.t_stat,'NW-t':r.nw_t,'Positive IC %':r.positive_ic_pct,'Top30 above median %':z.stock_above_pool_median_pct.mean(),'Top30 positive %':z.stock_positive_pct.mean(),'Top30 excess pp':100*z.top_excess.mean(),'Ordered quintile pairs /4':r.monotone_pairs,'Q5−Q1 NW-t':r.spread_nw_t})
 return pd.DataFrame(rows)
def params(w):
 d=read(f'{w}_sweep_cells.csv');d=d[~d.cell.str.startswith('ablate_')];return d[['cell','cagr_pct','sharpe','calmar','maxdd_pct','turnover_pct','etf_exposure_pct']]
def ablations(w):
 d=read(f'{w}_sweep_cells.csv');d=d[(d.cell=='baseline')|d.cell.str.startswith('ablate_')].copy();b=d[d.cell=='baseline'].iloc[0]
 for x in ['sharpe','calmar','stability','average_dd_pct','turnover_pct']:d['delta_'+x]=100*(d[x]/b[x]-1) if b[x]!=0 else np.nan
 cols=['cell','sharpe','delta_sharpe','calmar','delta_calmar','stability','delta_stability','average_dd_pct','delta_average_dd_pct','turnover_pct','delta_turnover_pct'];d=d[cols];d.columns=['Cell','Sharpe','Δ %','Calmar','Δ %','12m σ','Δ %','Avg DD %','Δ %','Turnover %','Δ %'];return d
def swings(w):
 d=read(f'{w}_sweep_cells.csv').set_index('cell');sets={'Lookback 10–14':['lookback_10','lookback_12','lookback_14'],'Positions 24–36':['positions_24','positions_30','positions_36'],'Hard stop 12–18%':['stop_0.12','stop_0.15','stop_0.18'],'Bear cutoff −8% to −12%':['regime_-0.08','regime_-0.10','regime_-0.12']};rows=[]
 for n,ix in sets.items():
  z=d.loc[ix].sharpe;v=z.max()-z.min();rows.append({'Parameter':n,'Min Sharpe':z.min(),'Max Sharpe':z.max(),'Swing':v,'≤0.4': 'PASS' if v<=.4 else 'FAIL'})
 return pd.DataFrame(rows)
def ratio_table(a,am,b,bm):
 x=base(a,am);y=base(b,bm);l0=sig(b,'L0_composite').nw_t;l3=sig(b,'L3_tradeable').nw_t;checks=[('Sharpe OOS/IS',y.sharpe/x.sharpe,'≥0.60'),('Calmar OOS/IS',y.calmar/x.calmar,'≥0.60'),('CAGR OOS/IS',y.cagr_pct/x.cagr_pct,'≥0.50'),('Max DD OOS/IS',abs(y.maxdd_pct)/abs(x.maxdd_pct),'≤1.50'),('OOS Sharpe',y.sharpe,'>0'),('OOS L0 IC NW-t',l0,'≥1.50'),('OOS L3 IC NW-t',l3,'≥1.50'),('OOS L3 IC months <8 %',sig(b,'L3_tradeable').months_lt8_pct,'≤15')];rows=[]
 for name,v,g in checks:
  passed=v>=float(g[1:]) if g.startswith('≥') else v<=float(g[1:]) if g.startswith('≤') else v>float(g[1:]);status='PASS' if passed else ('CAUTION' if name in ('Sharpe OOS/IS','Calmar OOS/IS') and .4<=v<.6 else 'FAIL');rows.append({'Metric':name,'Value':v,'Gate':g,'Verdict':status})
 rows += [{'Metric':'Δ Sharpe (OOS − IS)','Value':y.sharpe-x.sharpe,'Gate':'informational','Verdict':'—'},{'Metric':'Δ Calmar (OOS − IS)','Value':y.calmar-x.calmar,'Gate':'informational','Verdict':'—'}];return pd.DataFrame(rows)
A=json.loads((E/'data_audit.json').read_text());F=json.loads((E/'fingerprint_result.json').read_text());X=json.loads((E/'execution_tests.json').read_text());P=json.loads((E/'strategy_parity.json').read_text());EA=json.loads((E/'etf_audit.json').read_text());B=base('late');Z=sig('late','L3_tradeable');L0=sig('late','L0_composite');U=dispersion('late');pr=read('prefix_tests.csv');stop=read('stop_open_ordering.csv');ex=read('exit_summary.csv');rot=read('exit_rotations.csv');endtr=read('late_universe_trades.csv',parse_dates=['Entry_Date','Exit_Date']);endn=int((endtr.Exit_Reason=='END_OF_PERIOD').sum());rank=ex[ex.reason=='RANK_EXIT'].iloc[0];volstop=ex[ex.reason=='VOL_STOP_HIT'].iloc[0];
header="""**Scope.** Updated `csm_stock_strategy_v3.py` and `csm_stock_backtest_v3.py`: 30-stock weight-based momentum strategy, two-month rebalance, bear-regime scaling, volatility and correlation guards, and default GOLDBEES idle-capital sweep. Costs are 0.30% one-way on stock turnover and ETF turnover. Stock exit-day gains/losses are omitted as requested. All historical results use a verified fixed OHLCV snapshot through 2026-10-30 and an exact copy of GOLDBEES data. Main validation runs use flat-start portfolios after indicator warmup; Stage 4 also shows the source’s warmup-active convention.\n"""
stage1=header+f"""
# Stage 1 — Universe, data and year robustness

**Verdict: PASS core-universe dispersion in both reference windows; caution for source adjustment, survivorship and the 501–1000 anomaly.** A band 500–1000 means ranks >500 and ≤1000. Liquidity rank uses shifted 63-day median traded value, minimum 21 observations; entry filters include price, 252 observed listing bars, circuit days, trend and falling-knife rules. ETF exposure is part of every portfolio.

## 2015–2025 universe sweep

{table(utable('late'))}

## 2005–2014 universe sweep

{table(utable('early'))}

## Core-universe dispersion: 1–250, 1–500, 1–750, 1–1000, 1–1500

{table(pd.DataFrame([dispersion('early'),dispersion('late')]))}

| Measure | Pass | Caution | Major divergence |
| --- | --- | --- | --- |
| Sharpe range | ≤0.35 | 0.35–0.60 | >0.60 |
| Calmar range | ≤0.50 | 0.50–0.90 | >0.90 |
| CAGR range | ≤8 pp | 8–15 pp | >15 pp |
| MaxDD range | ≤10 pp | 10–18 pp | >18 pp |
| Any core Sharpe | >0 | — | ≤0 |

## Annual returns (%) by universe

{table(annual('early'),2)}

{table(annual('late'),2)}

## Leave one year out: baseline

These are fixed daily return series with one calendar year removed and remaining observations stitched together; CAGR is annualized using 252 trading days. They are not new backtests.

{table(read('early_leave_one_year_out.csv'),2)}

{table(read('leave_one_year_out.csv'),2)}

## Transaction-cost stress (stocks and ETF)

{table(costs('late'),3)}

The cost sensitivity recomputes both stock and ETF charges from the same target-weight path; stop slippage remains fixed, and market impact is not modeled.

## Source-data checks

| Check | Result | Interpretation |
| --- | --- | --- |
| Stock files / last valid bar | {A['files']} / {A['last']} | Fixed test snapshot |
| Symbols last seen >183 days before panel end | {A['last_seen_before_cutoff']} / {A['files']} ({A['last_seen_pct']:.2f}%) | <2% flag; proxy, not verified delistings |
| Extreme adjacent valid-close changes ≤−40% or ≥+300% | {A['extreme_close_changes']} | Suspected actions/data anomalies, not individually verified |
| Duplicate-date observations | {A['counts'].get('duplicate_dates',0)} | Audit counts same-date rows; loader keeps last exact duplicate timestamp |
| First valid GOLDBEES close | {EA['first_valid_close']} | No ETF sleeve before availability |
| GOLDBEES largest observation gap | {EA['longest_gap_last_observation']} → {EA['longest_gap_next_observation']} ({EA['longest_gap_calendar_days']} calendar days) | No ETF rows for 2011–2014; marks are forward-filled and untradable sales may be forced |
| Snapshot hash mismatches | 0 / 5205 | See [snapshot verification](evidence/snapshot_verification.json) |

Corporate-action adjustment is not verified; returns are subject to source artifacts. See [Stage 3](stage3_robustness_lookahead.md) for TIL sensitivity and [ETF coverage](evidence/etf_coverage.csv).
"""
write('stage1_universe.md',stage1)
stage2=header+f"""
# Stage 2 — Signal IC, accuracy and decay

**Verdict: PASS basic IC, FAIL quantile ordering; concentration flagged.** The configured 2015–2025 3-month L0 NW-t is {L0.nw_t:.2f} and L3 NW-t is {Z.nw_t:.2f}; each must be ≥2.0. Quantile ordering is {int(Z.monotone_pairs)}/4 (75%, below the 80% gate) and its spread NW-t is {Z.spread_nw_t:.2f}. Interpret the gate in conjunction with the unresolved data-adjustment caveat in Stage 1.

IC is cross-sectional Spearman correlation between the stock factor and its subsequent return. NW uses lag equal to the forward horizon (in months); ordinary t-statistics are displayed separately. The ETF does not enter the stock-factor IC.

## 3-month filter ladder: 2015–2025

{table(ladder('late'),4)}

## 3-month filter ladder: 2005–2014

{table(ladder('early'),4)}

L0 is the raw factor, L1 adds price, L2 adds liquidity/circuit/listing age, L3 adds trend and falling-knife, L4 adds positive 12-month momentum, and L5 is the top-30 ranked portion. L5 measures ranking within the small selected group, not the portfolio P&L.

## Forward horizons and theoretical stock-selection accuracy

### 2015–2025

{table(horizons('late'),4)}

### 2005–2014

{table(horizons('early'),4)}

Accuracy is the average fraction of theoretical top-30 stocks above their eligible-pool median or above zero; excess is their equal-weight forward return minus the pool average. This is not an executed portfolio: hysteresis, stops, costs and ETF are excluded. Quintile returns are equal-weighted; the 3-month ordered-pairs gate is ≥80% and Q5−Q1 NW-t gate is ≥2.

### Quintile returns: 2015–2025

{table(read('signal_late_quintiles.csv'),3)}

## Equal-weight vs liquidity-weighted IC proxy

{table(pd.concat([read('signal_early_summary.csv').query("rung == 'L3_tradeable'"),read('signal_late_summary.csv').query("rung == 'L3_tradeable'")])[['window','horizon','mean_ic','weighted_liquidity_ic','top2_year_share_pct']],4)}

Liquidity weighting uses median traded value as a proxy; point-in-time market-cap weights were unavailable. Top-two-year share divides the two largest signed annual IC sums by total signed IC and is flagged above 50%.

## Time decay: 3-month L3 IC

{table(pd.concat([read('signal_'+w+'_decay.csv') for w in ['early','late','playbook_early','playbook_late']]),4)}

The late-window comparison is 2023–2025 vs 2015–2022. The playbook-late comparison uses recent 2024–July 2026 signal months with outcomes observed through October 2026, versus earlier years. These historical windows have been examined and are not blind tests. NW-t for the difference uses HAC lag 3. A non-significant result does not prove stability.

### Yearly signal behavior: 2015–2025

{table(read('signal_late_years.csv'),4)}

### Three-year blocks

{table(read('signal_late_chunks.csv'),4)}

## Raw vs forward-filled outcomes

{table(read('signal_late_ffill.csv'),4)}

Forward-fill comparison is a missing-data sensitivity; small differences do not prove the absence of delisting or survivorship bias. [Detailed IC series](evidence/signal_late_series.csv) · [All filter and horizon results](evidence/signal_late_summary.csv).
"""
write('stage2_signal.md',stage2)
rawprobe=read('late_probe_cells.csv').set_index('cell');cleanprobe=read('late_probe_cells_no_TIL.csv').set_index('cell');probe=[]
for cell in ['band_500_1000','positions_36','positions_42']:
 for label,d in [('Raw snapshot',rawprobe),('Exclude TIL in memory',cleanprobe)]:
  r=d.loc[cell];probe.append({'Cell':cell,'Data sensitivity':label,'CAGR %':r.cagr_pct,'Sharpe':r.sharpe,'Calmar':r.calmar,'MaxDD %':r.maxdd_pct})
base_late=base('late');etfdiag=json.loads((E/'late_etf_sale_diagnostics.json').read_text());e=X['integrated_stock_stop_and_etf_open'];a=e['later_low_90'];b=e['later_low_80'];
stage3=header+f"""
# Stage 3 — Robustness, ablation and lookahead

**Verdict: FAIL no-lookahead tests.** The earlier scheduled-open exit ordering is fixed in the ordinary non-circuit synthetic case, but two opening-time causal problems remain.

| Test | Held constant / changed later | Observed | Result |
| --- | --- | --- | --- |
| Scheduled open exit | Same open 100; later stock low 90 vs 80 | Both {X['scheduled_exit']['later_low_90']['reason']} at {X['scheduled_exit']['later_low_90']['exit_price']:.2f}; next-day weight {X['scheduled_exit']['later_low_90']['next_day_weight']:.2f} in both | PASS |
| Stock circuit test at open | Same open 100; later high/low nonzero range vs equal | First-day stock weight {X['circuit_at_open']['later_full_day_range_nonzero']['day1_weight']:.2f} vs {X['circuit_at_open']['later_full_day_range_zero']['day1_weight']:.2f} | FAIL |
| Stock stop and ETF funding | Same opening purchase of B, weight {e['same_open_stock_buy_B']:.2f}; A's later low 90 vs 80 | ETF assumed opening sale {a['etf_open_sale_weight']:.2f} vs {b['etf_open_sale_weight']:.2f}; ETF contribution {100*a['etf_daily_contribution']:.2f}% vs {100*b['etf_daily_contribution']:.2f}% | FAIL |

The last row runs the actual stock event loop and ETF sweep: the later stop changes end-of-day stock weight, which changes the ETF sale treated as occurring earlier at the open. This is independent of the intentionally omitted exit-day stock P&L. The circuit test uses the whole day’s high and low to decide an opening fill. These are deterministic counterexamples, not claims that every historical event is affected. [Test code](evidence/test_execution.py) · [Detailed results](evidence/execution_tests.json).

## Historical ETF sale / stock-stop overlap, 2015–2025

| Measure | Count |
| --- | --- |
| Days with modeled ETF sale | {etfdiag['days_with_etf_sale']} |
| Days with a stock stop and modeled ETF sale | {etfdiag['days_with_etf_sale_and_stock_stop']} |
| Days with a stock stop | {etfdiag['days_with_stock_stop']} |
| ETF sale days flagged untradable | {etfdiag['untradable_etf_sale_days']} |

This overlap identifies potentially affected days; it does not prove that each sale was caused by a later stop or measure the resulting bias. [Daily overlap data](evidence/late_etf_open_sales.csv).

## Actual-class parity and prefix tests

| Check | Measured |
| --- | --- |
| Baseline reconstructed equity maximum absolute difference | {P['max_equity_difference']:.3g} |
| Maximum target weight difference | {P['max_target_weight_difference']:.3g} |
| Warmup stock exposure | {P['warmup_weight_max']:.3g} |
| Prefix tests passing | {int((pr.result=='PASS').sum())} / {len(pr)} |

{table(pr,6)}

Prefix tests compare factor eligibility, factor values, target weights, ATR and regime values through each cutoff. They do not verify opening execution timing.

## Parameter sweeps: 2015–2025

{table(params('late'),3)}

## Parameter sweeps: 2005–2014

{table(params('early'),3)}

## ±20% Sharpe sensitivity

### 2015–2025

{table(swings('late'),3)}

### 2005–2014

{table(swings('early'),3)}

Integer lookbacks 10 and 14 are approximations to ±20% around 12. The rebalance tests 1, 2 and 3 months are discrete ±50% stresses; the ±20% gate cannot be evaluated exactly.

## Ablation scorecards

Each row includes all five playbook measures and relative changes from baseline. Lower return instability, average drawdown depth and turnover are preferable. Limits: Sharpe/Calmar regression >15%; instability/average drawdown worsening >20%; turnover increase >25%.

### 2015–2025

{table(ablations('late'),3)}

### 2005–2014

{table(ablations('early'),3)}

## TIL raw-price sensitivity

| Observation | Value |
| --- | --- |
| TIL close, 2017-12-06 → 2017-12-07 | ₹2.85 → ₹146.50 (+5,040.35%) |
| 501–1000 portfolio return on 2017-12-07 | +253.63% |

{table(pd.DataFrame(probe),3)}

The exclusion is retrospective and is not an adjusted-data backtest: the ticker is removed only in memory, then universe ranks, benchmark, positions, stock engine and ETF sleeve are recomputed. Compare the raw and excluded 501–1000 and 42-position cells to identify sensitivity to this price series; do not treat the cleaned result as proof of investability.

[Early sweep](evidence/early_sweep_cells.csv) · [Late sweep](evidence/late_sweep_cells.csv) · [2001–2012 sweep](evidence/playbook_early_sweep_cells.csv) · [2013–latest sweep](evidence/playbook_late_sweep_cells.csv).
"""
write('stage3_robustness_lookahead.md',stage3)
def score(w,mode):
 x=base(w,mode);return {'Window':w,'First stock entry':x.first_entry,'CAGR %':x.cagr_pct,'Sharpe':x.sharpe,'Sortino':x.sortino,'Max DD %':x.maxdd_pct,'Calmar':x.calmar,'Vol %':x.vol_pct,'Stock exposure %':x.exposure_pct,'ETF exposure %':x.etf_exposure_pct,'ETF cost drag %/yr':x.etf_cost_drag_pct,'Trades':x.trades}
def etfcmp(w,mode):return read(f'{w}_{mode}_baseline_etf_comparison.csv').iloc[0]
cmp=pd.DataFrame([etfcmp(w,m) for w,m in [('early','universe'),('late','universe'),('playbook_early','baseline'),('playbook_late','baseline'),('full','baseline')]])
stage4=header+f"""
# Stage 4 — IS/OOS, ETF sleeve and full-sample results

**Verdict: NOT VALIDATED.** The numerical comparisons below are retrospective, not blind OOS. The v2 strategy family and both periods have already been inspected; complete development and post-OOS modification history are unavailable. Unresolved timing and source-data issues also block promotion regardless of ratio results. Parameter/ablation sweeps were rerun separately for each period; no configuration was selected or changed after viewing them.

| Comparison | Flat-start period | Warmup |
| --- | --- | --- |
| Reference early | 2005-01-01–2014-12-31 | 450 calendar days where available |
| Reference late | 2015-01-01–2025-12-31 | 450 calendar days |
| Playbook early | 2001-01-01–2012-12-31 | Up to 450 calendar days, limited by data |
| Playbook late | 2013-01-01–2026-10-30 | 450 calendar days |
| Full descriptive | 2002-01-01–2025-12-31 | Up to 450 calendar days |

Stock selection and holdings start flat; the ETF sweep is also prevented from buying before each report start. The baseline cannot invest in GOLDBEES before its first data point in {EA['first_valid_close']}; the supplied file also has no observations in 2011–2014.

## Breadth and ETF coverage

{table(pd.concat([read(f'signal_{w}_breadth.csv') for w in ['early','late','playbook_early','playbook_late']]),3)}

{table(read('etf_coverage.csv'),3)}

The supplied ETF file has **zero observations in 2011–2014**: its last pre-gap close is {EA['longest_gap_last_observation']} and the next is {EA['longest_gap_next_observation']}. The engine forward-fills the last mark for valuation during this gap and may assume sales on untradable bars. This makes early-window and full-sample ETF performance, and split comparisons containing the gap, unreliable even if their numerical ratios pass. The late-only 2015–2025 sample does not include this gap.

{table(read('etf_annual_coverage.csv'),0)}

## Baseline scorecards

{table(pd.DataFrame([score(w,m) for w,m in [('early','universe'),('late','universe'),('playbook_early','baseline'),('playbook_late','baseline'),('full','baseline')]]),3)}

## Additional trade and benchmark scorecard

{table(pd.DataFrame([{'window':w,'trade_win_pct':base(w,m).trade_win_pct,'profit_factor_pct_units':base(w,m).profit_factor_pct,'payoff':base(w,m).payoff,'hold_days':base(w,m).hold_days,'beta_proxy':base(w,m).beta,'alpha_pct_proxy':base(w,m).alpha_pct} for w,m in [('early','universe'),('late','universe'),('playbook_early','baseline'),('playbook_late','baseline'),('full','baseline')]]),3)}

Win rate, profit factor and payoff use per-trade percentage returns; dollar-weighted profit factor is unavailable. Beta and annual alpha use an equal-weight raw-stock return proxy with daily returns clipped to ±50%, not an independently verified investable index.

## ETF sweep vs idle cash on the same stock-weight path

{table(cmp[['window','cash_cagr','cash_sharpe','cash_calmar','cash_maxdd','etf_cagr','etf_sharpe','etf_calmar','etf_maxdd','etf_first_usable','etf_exposure_pct','etf_cost_drag_pct','forced_untradable']],3)}

`etf_first_usable` is the sweep activation bound (the later of the first usable close in the loaded panel and the report start); an actual purchase also requires a tradable bar. It is not necessarily ETF inception or the first actual purchase. `forced_untradable` counts sales the backtest assumes even when its completed-bar tradability test is false. ETF cost drag is estimated from traded weight, not actual market impact. Both runs share the same simulated stock decisions; differences are the modeled ETF, its costs and the cash return convention.

## Flat-start vs source-main warmup convention, 2015–2025

{table(read('native_main_comparison.csv'),3)}

The source main permits positions during warmup, while the split tests reset stock and ETF holdings. Its reported trade log excludes entries made before the report starts. Main-comparable results are provided to explain why the two conventions can disagree.

## Source-configured 2005–2015 period

{table(read('native_default_comparison.csv'),3)}

The first row uses the current source `START_DATE` and `END_DATE` with its warmup-active convention; the second resets at the same start. The actual source-default ETF exposure during the 2011–2014 missing-data gap is summarized below.

{table(pd.DataFrame([json.loads((E/'native_default_etf_gap.json').read_text())]).drop(columns=['method']),3)}

The gap calculation uses the source-default warmup-active portfolio, so it need not equal the independently flat-start splits. ETF weight during the missing interval was very small in this run; the major limitation is that the model could not buy the intended ETF through the missing years, so it cannot establish what a continuously available sweep would have earned.

## Reference split A: 2005–2014 IS → 2015–2025 OOS

{table(ratio_table('early','universe','late','universe'),3)}

## Reference split B: 2015–2025 IS → 2005–2014 OOS

{table(ratio_table('late','universe','early','universe'),3)}

## Playbook split A: 2001–2012 IS → 2013–2026 OOS

{table(ratio_table('playbook_early','baseline','playbook_late','baseline'),3)}

## Playbook split B: 2013–2026 IS → 2001–2012 OOS

{table(ratio_table('playbook_late','baseline','playbook_early','baseline'),3)}

OOS/IS Sharpe and Calmar 0.40–0.60 are caution and below 0.40 fail; CAGR must be ≥0.50, drawdown depth ≤1.5×, OOS Sharpe positive, and L0/L3 OOS NW-t ≥1.5. The IC breadth row repeats the Stage 2 ≤15% exclusion gate; it is not an extra Stage 4 ratio threshold. Δ means OOS minus IS. A fresh frozen configuration and genuinely untouched OOS evidence would still be needed even if retrospective numeric gates passed. The early window includes 2008; the later window includes 2018, 2020 and 2022. ETF inception changes the opportunity set across the early split.

## Full-sample calendar years, informational only

{table(read('full_baseline_yearly.csv')[['year','return_pct','sharpe','maxdd_pct']],3)}

[Early playbook sweep](evidence/playbook_early_sweep_cells.csv) · [Late playbook sweep](evidence/playbook_late_sweep_cells.csv) · [ETF data audit](evidence/etf_audit.json).
"""
write('stage4_is_oos.md',stage4)
stopn=int(stop.scheduled_zero_target.sum()) if len(stop) else 0
ex['sample_quality']=np.where(ex.available_both<30,'directional (<30)','≥30')
stage5=header+f"""
# Stage 5 — Exit quality

**Verdict: diagnostic only.** Volatility-stop mean benchmark-relative continuation is {volstop.mean20_60_pct:+.2f}% across 20 and 60 days on {int(volstop.available_both)} exits, above the +1% too-early threshold. Rank exits are neutral at {rank.mean20_60_pct:+.2f}% on {int(rank.available_both)} exits. Interpret the per-reason table using the playbook thresholds and the execution-timing caveats in Stage 3.

| Check | Result | Gate |
| --- | --- | --- |
| Total exits, including artificial end-of-period | {len(endtr)} | — |
| END_OF_PERIOD share | {endn}/{len(endtr)} ({100*endn/len(endtr):.2f}%) | <5% outside final month |
| END_OF_PERIOD before final month | {int(((endtr.Exit_Reason=='END_OF_PERIOD')&(endtr.Exit_Date<pd.Timestamp('2025-12-01'))).sum())} | Expected 0 |
| Stop exits with zero prior-bar target | {stopn}/{len(stop)} | Candidate ordering conflicts only; eligibility to exit must be checked individually |

## Per-exit forward outcome

{table(ex,3)}

Post-exit benchmark is the equal-weight signal-eligible universe, with daily constituent returns clipped at ±50%; its final membership is carried forward. The mean is the average of 20- and 60-trading-day benchmark-relative returns on exits with both values. For stops, ≤−1% suggests working; ≥+1% suggests too early; between is neutral. Rank exits use the same diagnostic shape but call for a different review. Buckets under 30 are directional only. END_OF_PERIOD rows are excluded entirely. Raw source data and unresolved adjustment issues affect this analysis.

## Same-date entrant vs exit group comparison

{table(rot,3)}

This compares same-date group averages, not individually matched replacements. ETF performance is not attributed to stock exit rules. [Exit observations](evidence/exit_forward.csv) · [Trade log](evidence/late_universe_trades.csv).
"""
write('stage5_exits.md',stage5)
early=base('early');rev=ratio_table('late','universe','early','universe');play_b=ratio_table('playbook_late','baseline','playbook_early','baseline');early_bread=read('signal_playbook_early_breadth.csv').iloc[0];dec=read('signal_late_decay.csv').iloc[0];dec2=read('signal_playbook_late_decay.csv').iloc[0];latecmp=etfcmp('late','universe');range_severity='PASS' if U['Sharpe range']<=.35 and U['Calmar range']<=.5 and U['CAGR range pp']<=8 and U['MaxDD range pp']<=10 and U['Min Sharpe']>0 else 'CAUTION/FAIL';
verdict=header+f"""
# Final verdict — updated CSM Batch v3

**NOT VALIDATED.** The previously reported scheduled-open exit issue passes its specific regression test, but stock circuit handling and the new GOLDBEES sleeve still show opening-time lookahead. The source has unresolved corporate-action and survivorship limitations; historical return figures therefore cannot support promotion.

| Stage | Verdict | Key numbers | Report |
| --- | --- | --- | --- |
| 1. Universes | **{range_severity} core; data anomaly** | 2015–2025 core Sharpe range {U['Sharpe range']:.3f}, Calmar range {U['Calmar range']:.3f}; 501–1000 band is sensitive to the raw TIL jump; GOLDBEES has no 2011–2014 bars | [Stage 1](stage1_universe.md) |
| 2. Signal | **IC pass; quantile fail** | 2015–2025 L0 NW-t {L0.nw_t:.2f}, L3 {Z.nw_t:.2f}; ordered quintile pairs {int(Z.monotone_pairs)}/4; top-two-year signed-IC share {Z.top2_year_share_pct:.1f}% | [Stage 2](stage2_signal.md) |
| 3. Robustness & lookahead | **FAIL** | Scheduled-exit regression PASS; circuit-at-open FAIL; integrated stock-stop/ETF-open-sale FAIL | [Stage 3](stage3_robustness_lookahead.md) |
| 4. IS/OOS | **Not blind; not validated** | Reference Sharpe {early.sharpe:.2f} → {B.sharpe:.2f}; Calmar {early.calmar:.2f} → {B.calmar:.2f}; reverse MaxDD ratio {abs(early.maxdd_pct/B.maxdd_pct):.2f}× (limit 1.50×) | [Stage 4](stage4_is_oos.md) |
| 5. Exit quality | **Diagnostic** | {endn}/{len(endtr)} END_OF_PERIOD records; volatility-stop continuation {volstop.mean20_60_pct:+.2f}% on {int(volstop.available_both)} observations (too early); rank exit {rank.mean20_60_pct:+.2f}% (neutral) | [Stage 5](stage5_exits.md) |

For 2015–2025, the configured ETF simulation reports CAGR {B.cagr_pct:.2f}%, Sharpe {B.sharpe:.2f} and max drawdown {B.maxdd_pct:.2f}%; the same stock-weight path with idle cash reports CAGR {latecmp.cash_cagr:.2f}% and Sharpe {latecmp.cash_sharpe:.2f}. The ETF timing issue means the improvement is not established as executable.

The user-requested omission of exit-day stock P&L was preserved. The source strategy files and source data folders were only read. Stock tests used the same fixed snapshot through 2026-10-30 as the previous validation; GOLDBEES was copied and hashed separately. The supplied ETF file has no observations in 2011–2014, making early-period and full-sample ETF metrics unreliable. [Scope, configuration and reproducibility](validation.md).
"""
write('VERDICT.md',verdict)
summary=header+f"""
# Updated CSM Batch v3 validation

The [final verdict](VERDICT.md) summarizes the five stage reports. The current stock strategy has changed from the previous v3 validation; it no longer uses that version’s ADX/high52 gates or its corporate-action mask, and it now has a GOLDBEES sleeve. Returns are therefore not directly comparable as a one-variable change:

1. [Universe and data](stage1_universe.md)
2. [Signal and decay](stage2_signal.md)
3. [Robustness, ablation and lookahead](stage3_robustness_lookahead.md)
4. [Bidirectional IS/OOS and ETF](stage4_is_oos.md)
5. [Exit quality](stage5_exits.md)

| Default setting | Value |
| --- | --- |
| Factor | 12/6-month risk-normalized momentum, one-month lag |
| Stock universe | Liquidity ranks 1–1000, price >₹10, ≥252 observed listing bars; trend, circuit and falling-knife filters |
| Sizing / cadence | 30 stocks, inverse-volatility sizing, 2-month rebalance, maximum stock weight 5% |
| Risk | Bear scaling 60% / 30%, 20% vol target, correlation guard; 15% hard entry stop and 4× ATR-based volatility trail |
| Secondary sleeve | GOLDBEES, idle-cash sweep; ETF one-way cost 0.30%; buy band zero |
| Signal filter configuration | The prior ADX/52-week-high gates are not part of the current strategy source |

| Reviewed artifact | SHA-256 |
| --- | --- |
| Strategy | `{F['strategy_sha256']}` |
| Backtest | `{F['backtest_sha256']}` |
| GOLDBEES source and copied data | `{F['etf_source_sha256']}` |

[Stock snapshot manifest](evidence/snapshot_manifest.csv) · [Snapshot verification](evidence/snapshot_verification.json) · [Source fingerprint](evidence/fingerprint_result.json) · [Raw results and scripts](evidence/). The fixed stock snapshot is `/private/tmp/csm_batch_v3_validation_snapshot/ohlcv`; it ends 2026-10-30 to preserve an apples-to-apples comparison and avoid the prior session's concurrently changing data source. Its 5,205 files were verified against the stored SHA-256 manifest. The original source is read only; source metadata before/after is tracked separately.
"""
write('validation.md',summary)
print('Wrote 7 reports')

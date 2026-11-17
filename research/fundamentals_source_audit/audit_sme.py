"""Read-only audit of SME report periods, source continuity, and strategy coverage."""
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
DATA = ROOT / 'fundamentals_data' / 'sme'
sys.path.insert(0, str(ROOT / 'csm_value'))
import fundamentals_loader as loader

paths = sorted(DATA.glob('*.json'))
syms = {p.stem for p in paths}
prices = {p.stem for p in Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data').glob('*.csv')}
inventory = pd.read_csv(OUT / 'filings_inventory.csv')
inv = inventory[inventory.group == 'SME'].copy()
inv['end'] = pd.to_datetime(inv.end)
inv['filed_dt'] = inv.filed.map(loader._parse_filed)
inv['lag'] = (pd.to_datetime(inv.filed_dt) - inv.end).dt.days
inv['period_type'] = pd.cut(inv.days, [-1, 105, 195, 370], labels=['quarter', 'half_year', 'annual'])
print('SME_FILES', len(paths), 'OHLCV_OVERLAP', len(syms & prices))
print('PERIOD_TYPES_BY_YEAR\n', pd.crosstab(inv.year, inv.period_type).to_string())
print('LATE_2025_ONWARD\n', inv[inv.year >= 2025].groupby('submission_type').apply(
    lambda x: pd.Series({'rows': len(x), 'late': (x.lag > 120).sum(),
                         'late_symbols': x.loc[x.lag > 120, 'symbol'].nunique()}), include_groups=False).to_string())

rows=[]
for path in paths:
    doc=json.loads(path.read_text())
    for fy,node in (doc.get('fiscal_years') or {}).items():
        for basis in ('standalone','consolidated'):
            ann=(node.get('annual') or {}).get(basis) or {}
            blocks=[((node.get('quarters') or {}).get(q) or {}).get(basis) or {} for q in ('Q2','Q4')]
            if not ann or not all(blocks):
                continue
            try:
                dates=[((pd.Timestamp(b['period']['end']) - pd.Timestamp(b['period']['start'])).days,
                        pd.Timestamp(b['period']['start']), pd.Timestamp(b['period']['end'])) for b in blocks]
                if any(not (150 <= days <= 195) for days,_,_ in dates) or dates[0][2] + pd.Timedelta(days=1) != dates[1][1]:
                    continue
            except (KeyError, ValueError, TypeError):
                continue
            for field in ('revenue_from_operations','net_profit'):
                vals=[(x.get('income_statement') or {}).get(field) for x in [*blocks,ann]]
                if any(not isinstance(x,(int,float)) for x in vals):
                    continue
                h1,h2,annual=vals
                total=h1+h2
                rows.append(dict(symbol=path.stem,fy=fy,basis=basis,field=field,h1=h1,h2=h2,annual=annual,
                                 error=abs(total-annual)/max(abs(total),abs(annual),1),
                                 annual_filed=ann.get('filed_date'),h1_filed=blocks[0].get('filed_date'),
                                 h2_filed=blocks[1].get('filed_date'),
                                 h2_source=(blocks[1].get('source_filing') or {}).get('url')))
r=pd.DataFrame(rows)
r.to_csv(OUT/'sme_halfyear_reconciliation.csv', index=False)
print('HALF_YEAR_RECONCILIATION')
for key,g in r.groupby(['fy','field']):
    print(key,'rows',len(g),'within_1pct',round((g.error<=.01).mean()*100,1),
          'over_10pct',int((g.error>.1).sum()))
print('SUSPICIOUS_RECONCILIATION\n',r[r.error>.1].sort_values('error',ascending=False).head(20).to_string(index=False))

results=loader.load_results(symbols=syms)
print('LOADER_RESULTS',len(results),'SYMBOLS',results.symbol.nunique())
print('RESULTS_BY_PERIOD_YEAR\n',results.groupby(results.period_end.dt.year).agg(rows=('symbol','size'),symbols=('symbol','nunique')).to_string())
trades=pd.read_csv(ROOT/'csm_value/output/csm_value_ey_trade_log.csv')
trades=trades[trades.Ticker.isin(syms)]
print('SAVED_CLOSED_TRADES',len(trades),'SYMBOLS',trades.Ticker.nunique())
print('SME_LOADER_NAMES',','.join(sorted(results.symbol.unique())))

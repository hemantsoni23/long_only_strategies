"""Read-only verification of missing banking filings and a revised-filing example."""
import json
import sys
import tempfile
from datetime import date
from pathlib import Path

import requests
from lxml import etree

ROOT=Path(__file__).resolve().parents[2]
SOURCE=Path('/Users/hemantsoni/Documents/upstox_data_folder/Fundamentals')
sys.path.insert(0,str(SOURCE))
from update_integrated_fundamentals import nse_session, list_filings, financial_block

results=[]
with nse_session() as session, tempfile.TemporaryDirectory() as temp:
 for symbol in ('HDFCBANK','SBIN','ICICIBANK'):
  company=json.loads((ROOT/'fundamentals_data'/f'{symbol}.json').read_text())
  rows=list_filings(session,symbol,company['company_name'])
  choices=[r for r in rows if (r.get('qe_Date') or '').upper()=='31-MAR-2025' and r.get('consolidated')=='Standalone' and r.get('xbrl')]
  if not choices: raise ValueError(f'no March 2025 standalone filing for {symbol}')
  row=next((r for r in choices if r.get('type_Sub')=='Original'),choices[0]);url=row['xbrl']
  response=session.get(url,timeout=30);response.raise_for_status();path=Path(temp)/(symbol+'.xml');path.write_bytes(response.content)
  root=etree.fromstring(response.content);facts={}
  for e in root.iter():
   if e.get('contextRef')=='OneD' and (e.text or '').strip():
    facts.setdefault(etree.QName(e).localname,e.text.strip())
  try:
   financial_block(path,row,'quarterly',date(2025,3,31));status='accepted'
  except Exception as exc: status=f'{type(exc).__name__}: {exc}'
  item={'symbol':symbol,'source_url':url,'broadcast_Date':row.get('broadcast_Date'),
        'submission_type':row.get('type_Sub'),'updater_result':status,
        'RevenueFromOperations':facts.get('RevenueFromOperations'),'InterestEarned':facts.get('InterestEarned'),
        'ProfitLossForThePeriod':facts.get('ProfitLossForThePeriod'),
        'ProfitLossFromOrdinaryActivitiesAfterTax':facts.get('ProfitLossFromOrdinaryActivitiesAfterTax')}
  results.append(item); print(json.dumps(item),flush=True)
 symbol='PFC'; company=json.loads((ROOT/'fundamentals_data'/f'{symbol}.json').read_text());rows=list_filings(session,symbol,company['company_name'])
 q=[r for r in rows if (r.get('qe_Date') or '').upper()=='31-MAR-2026' and r.get('consolidated')=='Consolidated']
 print('PFC MARCH2026 ALL VERSIONS',json.dumps([{k:r.get(k) for k in ('qe_Date','consolidated','broadcast_Date','revised_Date','type_Sub','xbrl')} for r in q]),flush=True)
 results.append({'symbol':'PFC','all_march_2026_consolidated_versions':[{k:r.get(k) for k in ('qe_Date','consolidated','broadcast_Date','revised_Date','type_Sub','xbrl')} for r in q]})
(Path(__file__).resolve().parent/'banking_and_revisions.json').write_text(json.dumps(results,indent=2)+'\n')

"""Spot-check local JSON facts against their official NSE XBRL source files."""
import json
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor
from lxml import etree
import requests

ROOT=Path(__file__).resolve().parents[2]
OUT=Path(__file__).resolve().parent
SAMPLES=[('TCS','FY2024-25','Q4','consolidated'),('TCS','FY2025-26','Q2','consolidated'),
         ('RELIANCE','FY2025-26','Q2','consolidated'),('PFC','FY2025-26','Q3','consolidated'),
         ('DEVIT','FY2025-26','Q2','consolidated'),('INDIANHUME','FY2024-25','Q4','standalone'),
         ('ZUARI','FY2025-26','Q2','consolidated'),('AUSOMENT','FY2025-26','Q3','consolidated'),
         ('UMIYA-MRO','FY2025-26','Q2','consolidated'),('DJML','FY2025-26','Q2','consolidated')]
MAP={'revenue_from_operations':['RevenueFromOperations'], 'net_profit':['ProfitLossForPeriod','ProfitLossForPeriodFromContinuingOperations'],
     'basic_eps':['BasicEarningsLossPerShareFromContinuingAndDiscontinuedOperations','BasicEarningsLossPerShareFromContinuingOperations'],
     'paid_up_equity_share_capital':['PaidUpValueOfEquityShareCapital'],'face_value_per_share':['FaceValueOfEquityShareCapital'],
     'exceptional_items':['ExceptionalItemsBeforeTax'],'other_income':['OtherIncome']}

def check(sample):
 sym,fy,q,scope=sample
 path=ROOT/'fundamentals_data'/f'{sym}.json'
 if not path.exists(): path=ROOT/'fundamentals_data'/'sme'/f'{sym}.json'
 d=json.loads(path.read_text()); b=d['fiscal_years'][fy]['quarters'][q][scope];url=b['source_filing']['url']
 u=urlparse(url)
 if u.scheme!='https' or u.hostname!='nsearchives.nseindia.com': raise ValueError(f'Unexpected source {url}')
 r=requests.get(url,headers={'User-Agent':'Mozilla/5.0','Referer':'https://www.nseindia.com/'},timeout=30);r.raise_for_status()
 root=etree.fromstring(r.content);tags={}
 for e in root.iter():
  if e.get('contextRef')=='OneD' and (e.text or '').strip():
   name=etree.QName(e).localname;tags.setdefault(name,[]).append({'value':e.text.strip(),'unit':e.get('unitRef'),'decimals':e.get('decimals')})
 results={}
 for key, raw in MAP.items():
  tag=next((x for x in raw if x in tags),None)
  value=tags[tag][0] if tag else None
  local=(b.get('income_statement') or {}).get(key)
  try: match=float(value['value'])==float(local)
  except (ValueError, TypeError, KeyError): match=(value is None and local is None)
  results[key]={'local':local,'tag':tag,'xbrl':value,'match':match, 'duplicate_values':tags.get(tag,[])}
 return {'symbol':sym,'fy':fy,'quarter':q,'scope':scope,'url':url,'filed_date':b.get('filed_date'),
         'period':b.get('period'), 'rounding':tags.get('LevelOfRoundingUsedInFinancialStatements'),
         'facts':results}

with ThreadPoolExecutor(max_workers=3) as p:
 results=list(p.map(check,SAMPLES))
(OUT/'nse_spot_checks.json').write_text(json.dumps(results,indent=2)+'\n')
for x in results:
 diffs=[k for k,v in x['facts'].items() if not v['match']]
 print(x['symbol'],x['fy'],x['quarter'],x['scope'],'mismatches',diffs,'rounding',x['rounding'],
       'profit',x['facts']['net_profit']['local'],'other',x['facts']['other_income']['local'],'exceptional',x['facts']['exceptional_items']['local'])

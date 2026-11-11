"""Check source metadata and reviewed code hashes without writing into source."""
from pathlib import Path
import hashlib,json,sys
P=Path(__file__).resolve().parent;ROOT=P.parents[1];DATA=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
state={'data':{p.name:[p.stat().st_size,p.stat().st_mtime_ns] for p in sorted(DATA.glob('*.csv'))},'strategy_sha256':digest(ROOT/'csm_stock_strategy_v3.py'),'backtest_sha256':digest(ROOT/'csm_stock_backtest_v3.py'),'filters_sha256':digest(ROOT/'csm_signal_filters.py')}
if sys.argv[1]=='before':
 (P/'fingerprint_before.json').write_text(json.dumps(state));print('Captured',len(state['data']),'files')
else:
 before=json.loads((P/'fingerprint_before.json').read_text());a=before['data'];b=state['data'];result={'before_files':len(a),'after_files':len(b),'added':len(b.keys()-a.keys()),'removed':len(a.keys()-b.keys()),'metadata_changed':sum(a[k]!=b[k] for k in a.keys()&b.keys()),'filters_unchanged':before['filters_sha256']==state['filters_sha256'],'filters_sha256':state['filters_sha256'],'strategy_unchanged':before['strategy_sha256']==state['strategy_sha256'],'backtest_unchanged':before['backtest_sha256']==state['backtest_sha256'],'strategy_sha256':state['strategy_sha256'],'backtest_sha256':state['backtest_sha256']};(P/'fingerprint_result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))

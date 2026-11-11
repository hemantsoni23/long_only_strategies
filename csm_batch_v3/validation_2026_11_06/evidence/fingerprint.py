"""Read-only fingerprints of source metadata, ETF contents, and strategy code."""
from pathlib import Path
import hashlib,json,sys
E=Path(__file__).resolve().parent;R=E.parents[1];src=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');etf=Path('/Users/hemantsoni/Documents/upstox_data_folder/gold_silver_ohlcv_data/GOLDBEES.csv')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
d={'data':{p.name:[p.stat().st_size,p.stat().st_mtime_ns] for p in sorted(src.glob('*.csv'))},'strategy':sha(R/'csm_stock_strategy_v3.py'),'backtest':sha(R/'csm_stock_backtest_v3.py'),'filters':sha(R/'csm_signal_filters.py'),'etf_source':sha(etf),'etf_copy':sha(E/'GOLDBEES.csv')}
if sys.argv[1]=='before':(E/'fingerprint_before.json').write_text(json.dumps(d));print('Captured',len(d['data']),'source files')
else:
 b=json.loads((E/'fingerprint_before.json').read_text());old=b['data'];new=d['data'];r={'before_files':len(old),'after_files':len(new),'added':len(new.keys()-old.keys()),'removed':len(old.keys()-new.keys()),'metadata_changed':sum(old[k]!=new[k] for k in old.keys()&new.keys())}
 for k in ['strategy','backtest','filters','etf_source','etf_copy']:r[k+'_sha256']=d[k];r[k+'_unchanged']=b[k]==d[k]
 r['etf_snapshot_matches_initial_source']=b['etf_copy']==b['etf_source'];(E/'fingerprint_result.json').write_text(json.dumps(r,indent=2));print(json.dumps(r,indent=2))

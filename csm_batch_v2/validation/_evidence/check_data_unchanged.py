from pathlib import Path
import json,pandas as pd
P=Path(__file__).resolve().parent;DATA=Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data');m=pd.read_csv(P/'data_manifest.csv',keep_default_na=False);before={str(r.symbol)+'.csv':(int(r.size),int(r.mtime_ns)) for r in m.itertuples()};after={p.name:(p.stat().st_size,p.stat().st_mtime_ns) for p in DATA.glob('*.csv')}
summary={'before_count':len(before),'after_count':len(after),'added':len(after.keys()-before.keys()),'removed':len(before.keys()-after.keys()),'metadata_changed':sum(before[k]!=after[k] for k in before.keys()&after.keys())};(P/'data_unchanged.json').write_text(json.dumps(summary,indent=2));print(summary)

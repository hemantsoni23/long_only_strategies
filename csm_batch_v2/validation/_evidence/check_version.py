from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;ROOT=P.parents[1];old=json.loads((P/'version.json').read_text());new={n:hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in old};result={'before':old,'after':new,'unchanged':old==new};(P/'version_check.json').write_text(json.dumps(result,indent=2));print(result)
if old!=new:raise SystemExit('Strategy or backtest changed during the run; rerun validation.')

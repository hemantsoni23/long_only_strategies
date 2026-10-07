"""assets.py -- index / ETF loaders (daily close panels, cached)."""
import glob, os
import pandas as pd

ROOT = '/Users/hemantsoni/Documents/upstox_data_folder'
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.cache')


def _read(path):
    df = pd.read_csv(path)
    dc = [c for c in df.columns if c.lower() in ('datetime', 'date', 'timestamp')][0]
    idx = pd.to_datetime(df[dc], utc=False, errors='coerce')
    try:
        idx = idx.dt.tz_localize(None)
    except Exception:
        pass
    df.index = idx.dt.normalize()
    df = df[~df.index.duplicated(keep='last')].sort_index()
    return df


def load_folder(folder, fields=('close',)):
    os.makedirs(CACHE, exist_ok=True)
    tag = folder
    out = {}
    for f in fields:
        p = os.path.join(CACHE, f'{tag}_{f}.parquet')
        if os.path.exists(p):
            out[f] = pd.read_parquet(p)
    if len(out) == len(fields):
        return out
    cols = {f: {} for f in fields}
    for path in sorted(glob.glob(os.path.join(ROOT, folder, '*.csv'))):
        name = os.path.basename(path)[:-4]
        try:
            df = _read(path)
        except Exception as e:
            continue
        for f in fields:
            if f in df:
                s = df[f].where(df[f] > 0) if f != 'volume' else df[f]
                cols[f][name] = s
    for f in fields:
        out[f] = pd.DataFrame(cols[f]).sort_index()
        out[f].to_parquet(os.path.join(CACHE, f'{tag}_{f}.parquet'))
    return out


def load_indices():
    return load_folder('index_data', ('close', 'high', 'low'))


def load_etfs():
    d = load_folder('etf_ohlcv_data', ('close', 'volume'))
    return d


if __name__ == '__main__':
    I = load_indices()['close']
    print(I.shape, I.index.min(), I.index.max())
    cov = pd.DataFrame({'start': I.apply(lambda s: s.first_valid_index()), 'end': I.apply(lambda s: s.last_valid_index()), 'n': I.notna().sum()})
    pd.set_option('display.max_rows', 400); pd.set_option('display.width', 200)
    print(cov.sort_values('n', ascending=False).to_string())
    E = load_etfs()
    print(E['close'].shape)

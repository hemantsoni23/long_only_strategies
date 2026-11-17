"""Download NSE's public month-end traded closes for CSM Value valuation.

The date calendar is derived from the existing Upstox data. Output is a compact
long CSV (date,symbol,series,close); it does not replace the OHLCV data used
for signals, stops or fills. Missing archive dates cause a non-zero exit.
"""
import argparse
import calendar
import csv
import io
import os
from pathlib import Path
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import requests

HERE = Path(__file__).resolve().parent
DEFAULT_OHLCV = Path('/Users/hemantsoni/Documents/upstox_data_folder/ohlcv_data')
DEFAULT_OUTPUT = HERE / 'data' / 'nse_monthly_prices.csv'
ALLOWED_SERIES = {'EQ', 'BE', 'BZ', 'SM', 'ST'}


def month_end_sessions(folder, start, end):
    dates = set()
    for symbol in ('RELIANCE', 'TCS', 'HDFCBANK'):
        path = Path(folder) / f'{symbol}.csv'
        if path.exists():
            frame = pd.read_csv(path, usecols=['datetime'], parse_dates=['datetime'])
            dates.update(frame['datetime'].dropna().dt.normalize())
    if not dates:
        raise FileNotFoundError(f'No RELIANCE, TCS or HDFCBANK calendar data in {folder}')
    dates = pd.DatetimeIndex(sorted(dates))
    dates = dates[(dates >= pd.Timestamp(start)) & (dates <= pd.Timestamp(end))]
    return pd.Series(dates, index=dates).resample('ME').last().dropna().tolist()


def fetch_date(date):
    day = pd.Timestamp(date)
    full = f'https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{day:%d%m%Y}.csv'
    month = calendar.month_abbr[day.month].upper()
    legacy = f'https://nsearchives.nseindia.com/content/historical/EQUITIES/{day:%Y}/{month}/cm{day:%d}{month}{day:%Y}bhav.csv.zip'
    urls = (full, legacy) if day.year >= 2020 else (legacy, full)
    errors = []
    for url in urls:
        for attempt in range(2):
            try:
                response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=25)
                if response.status_code != 200:
                    errors.append(f'{response.status_code} {url}')
                    break
                content = response.content
                if zipfile.is_zipfile(io.BytesIO(content)):
                    with zipfile.ZipFile(io.BytesIO(content)) as archive:
                        files = [n for n in archive.namelist() if n.lower().endswith('.csv')]
                        if len(files) != 1:
                            raise ValueError('archive does not contain exactly one CSV')
                        content = archive.read(files[0])
                rows = list(csv.DictReader(io.StringIO(content.decode('utf-8-sig'))))
                parsed = []
                for row in rows:
                    row = {k.strip().upper(): (v.strip() if isinstance(v, str) else v) for k, v in row.items() if k}
                    symbol, series = row.get('SYMBOL'), row.get('SERIES')
                    if not symbol or series not in ALLOWED_SERIES:
                        continue
                    raw_date = row.get('DATE1') or row.get('TIMESTAMP')
                    if pd.to_datetime(raw_date, dayfirst=True, errors='coerce') != day:
                        raise ValueError(f'file contains incorrect date {raw_date}')
                    close = float(row.get('CLOSE_PRICE') or row.get('CLOSE'))
                    if close > 0:
                        parsed.append((day.strftime('%Y-%m-%d'), symbol, series, close))
                if not parsed:
                    raise ValueError('no usable equity rows')
                return parsed
            except (requests.RequestException, ValueError, zipfile.BadZipFile) as exc:
                errors.append(str(exc))
                if attempt == 0:
                    time.sleep(0.5)
    raise RuntimeError(f'NSE archive unavailable for {day.date()}: {errors[-3:]}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ohlcv', type=Path, default=DEFAULT_OHLCV)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--start', default='2018-01-01')
    parser.add_argument('--end', default=pd.Timestamp.today().strftime('%Y-%m-%d'))
    parser.add_argument('--workers', type=int, default=3)
    args = parser.parse_args()
    sessions = month_end_sessions(args.ohlcv, args.start, args.end)
    print(f'Downloading {len(sessions)} NSE monthly sessions, {sessions[0].date()} to {sessions[-1].date()}', flush=True)
    with ThreadPoolExecutor(max_workers=max(1, min(args.workers, 4))) as pool:
        parts = list(pool.map(fetch_date, sessions))
    # Avoid silently selecting one of multiple trading series for a symbol.
    frame = pd.DataFrame([row for part in parts for row in part], columns=['datetime', 'symbol', 'series', 'close'])
    duplicate = frame.duplicated(['datetime', 'symbol'], keep=False)
    if duplicate.any():
        print(f'Excluding {int(duplicate.sum())} ambiguous multi-series rows', flush=True)
        frame = frame.loc[~duplicate]
    args.output.parent.mkdir(parents=True, exist_ok=True)
    temp = args.output.with_suffix('.tmp')
    frame.to_csv(temp, index=False)
    os.replace(temp, args.output)
    print(f'Wrote {len(frame):,} observations for {frame.symbol.nunique():,} symbols to {args.output}', flush=True)


if __name__ == '__main__':
    main()

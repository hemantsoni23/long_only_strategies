"""Build decay_check's OWN panel cache from the raw Upstox CSVs (does not touch factor_research/.cache).
Same cleaning as factor_research/data.py (dup dates, non-positive prices, +-40%/+300% corporate-action mask)."""
import sys, os
sys.path.insert(0, '/Users/hemantsoni/Documents/long_only_strategies/factor_research')
import data
HERE = os.path.dirname(os.path.abspath(__file__))
if __name__ == '__main__':
    P = data._build_panels()
    for f, df in P.items():
        df.astype('float32').to_parquet(os.path.join(HERE, '.cache', f'{f}.parquet'))
    c = P['close']; n = c.notna().sum(axis=1)
    print(c.shape, c.index.min().date(), c.index.max().date())
    print(n.tail(45).to_string())

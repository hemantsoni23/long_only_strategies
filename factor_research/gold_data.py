"""gold_data.py -- gold ETF series with the 2011-2014 source gap treated as MISSING (never forward-filled into returns)."""
import numpy as np, pandas as pd
import index_lab as L

def load_gold(ticker='GOLDBEES'):
    I, Ec, Ev, cal = L.prep()          # Ec is ffilled with limit=5 only -> the 4-year hole stays NaN
    return Ec[ticker], Ev[ticker], I, Ec, cal

def monthly_fwd_strict(close, cal, sig):
    """close(t+1 after sig[k+1]) / close(t+1 after sig[k]) - 1 using ONLY observed prices (NaN if either end is in a data gap)."""
    c = close.reindex(cal).values
    pos = cal.get_indexer(sig); entry = pos + 1
    out = np.full(len(sig), np.nan)
    for k in range(len(sig) - 1):
        if entry[k + 1] < len(cal):
            a, b = c[entry[k]], c[entry[k + 1]]
            if np.isfinite(a) and np.isfinite(b):
                out[k] = b / a - 1
    return pd.Series(out, index=sig)

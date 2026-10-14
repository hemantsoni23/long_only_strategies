"""
industry_cap_strategies.py
==========================
CSMZenithIndCap / CSMElendelIndCap -- the live Zenith / Elendel engines with ONE change: at most `industry_cap_k` names per Industry_clean label in the held book.

Implementation reuses the engine's own D4 concentration-cap hook (Zenith: `sector_cap_frac` + `_get_sector_map`), pointing it at Industry_clean instead of Sector_clean:
    sector_cap_frac = (K - 0.5) / top_n   ->   ceil(frac * top_n) = K names per group.
Names without an industry label are uncapped (each gets its own unique group).  Elendel has no D4 block, but its get_positions is otherwise identical to Zenith's, so the
Elendel subclass borrows Zenith's get_positions; test_industry_cap.py proves that with K = 0 both subclasses reproduce the unmodified engines exactly.

Nothing in Old_live_strategies is edited or copied; classes are imported.  `label_seed` permutes the industry labels across the labelled tickers (placebo: same group sizes, no meaning).
"""
import os
import sys

import numpy as np
import pandas as pd

LIVE = '/Users/hemantsoni/Documents/long_only_strategies/Old_live_strategies'
if LIVE not in sys.path:
    sys.path.insert(0, LIVE)

from csm_zenith_strategy import CSMZenith          # noqa: E402
from csm_elendel_strategy import CSMElendel        # noqa: E402

INSTRUMENTS = '/Users/hemantsoni/Documents/long_only_strategies/instruments_clean.csv'


class _LabelMap:
    """Minimal mapping with the only method the D4 block uses: .get(ticker, default). Unlabelled / unknown tickers get a unique group (never capped together)."""

    def __init__(self, labels):
        self.labels = labels

    def get(self, ticker, default=None):
        lab = self.labels.get(ticker)
        return lab if isinstance(lab, str) else f'__solo__{ticker}'


def industry_labels(label_seed=None, path=INSTRUMENTS):
    ins = (pd.read_csv(path).dropna(subset=['trading_symbol']).drop_duplicates('trading_symbol')
           .set_index('trading_symbol')['Industry_clean'])
    ins = ins.dropna()
    ins = ins[ins.astype(str).str.strip() != '']
    lab = ins.to_dict()
    if label_seed is not None:
        keys = list(lab.keys())
        vals = np.array([lab[k] for k in keys], dtype=object)
        rng = np.random.default_rng(label_seed)
        vals = vals[rng.permutation(len(vals))]
        lab = dict(zip(keys, vals))
    return lab


class _IndCapMixin:
    industry_cap_k = 0

    def _init_cap(self, industry_cap_k, label_seed):
        self.industry_cap_k = industry_cap_k
        self.sector_cap_frac = 0.0 if industry_cap_k <= 0 else (industry_cap_k - 0.5) / self.top_n
        self.sector_map = _LabelMap(industry_labels(label_seed))
        print(f"  [industry cap] K = {industry_cap_k}" + ("  (== live engine)" if industry_cap_k <= 0 else "")
              + (f"  PLACEBO labels seed={label_seed}" if label_seed is not None else ''))

    def _get_sector_map(self):
        return self.sector_map


class CSMZenithIndCap(_IndCapMixin, CSMZenith):
    def __init__(self, *args, industry_cap_k=0, label_seed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_cap(industry_cap_k, label_seed)


class CSMElendelIndCap(_IndCapMixin, CSMElendel):
    get_positions = CSMZenith.get_positions            # identical to Elendel's apart from the D4 block (verified by test_industry_cap.py)

    def __init__(self, *args, industry_cap_k=0, label_seed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_cap(industry_cap_k, label_seed)

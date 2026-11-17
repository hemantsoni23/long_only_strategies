"""Compatibility imports for older research scripts.

The point-in-time fundamentals logic now lives in csm_value_strategy.py.
The experimental pair has its own copy and does not import this module.
"""
from csm_value_strategy import (
    FUNDAMENTALS_DIR, VALID_FACE_VALUES, EXCLUDE_SYMBOLS, CLEAN_RATIOS,
    CLEAN_TOL, SHARE_RATIO_BAND, CUM_FACTOR_BAND, QUARTER_DAYS, CORE_TAX,
    MAX_FILING_LAG_DAYS, _num, _parse_filed, _read_symbol,
    _split_factor_per_period, load_results, monthly_frame,
)

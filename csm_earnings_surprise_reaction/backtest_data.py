"""Load the fundamentals-matched prices for the strategy's backtest."""
import os
import sys

import pandas as pd

from earnings_surprise_reaction_fundamentals import RESEARCH_END

VALUE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'csm_value')
sys.path.insert(0, VALUE_DIR)
import run_csm_value_backtest as value_runner  # noqa: E402


def load_all(load_start='2001-01-01', load_end='2024-12-31'):
    """Use the existing matched-universe loader, mask and benchmark unchanged."""
    if pd.Timestamp(load_end) > RESEARCH_END:
        raise ValueError(f'Earnings Surprise & Reaction research is limited to {RESEARCH_END.date()}.')
    prices, volumes, highs, lows, opens = value_runner.load_data(value_runner.data_folder_path)
    select = lambda frame: frame.loc[load_start:load_end] if not frame.empty else frame
    prices, volumes, highs, lows, opens = map(select, (prices, volumes, highs, lows, opens))
    prices, highs, lows, opens = value_runner.mask_corporate_actions(prices, highs, lows, opens)
    benchmark = value_runner.build_benchmark(prices)
    return prices, volumes, highs, lows, opens, benchmark

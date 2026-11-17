"""Checks for the research-only exit gate and position-cap settings."""
import importlib.util
import unittest
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd

path = Path(__file__).with_name('risk_exit_experiments.py')
spec = importlib.util.spec_from_file_location('risk_exit_experiments', path)
study = importlib.util.module_from_spec(spec)
spec.loader.exec_module(study)


class ExperimentTest(unittest.TestCase):
    def test_monthly_trend_gate_uses_only_available_closes(self):
        days = pd.bdate_range('2024-01-01', '2024-05-31')
        prices = pd.DataFrame({'A': np.arange(len(days)) + 100.0}, index=days)

        def run(p):
            labels = p.resample('ME').last().index
            return study.monthly_sma50_gate(SimpleNamespace(
                prices=p, factors=pd.DataFrame(index=labels, columns=p.columns)))

        before = run(prices.loc[:'2024-03-29'])
        altered = prices.copy()
        altered.loc['2024-04-01':] = 1.0
        after = run(altered)
        pd.testing.assert_frame_equal(before, after.loc[before.index])
        self.assertTrue(bool(before.loc['2024-03-31', 'A']))
        self.assertFalse(bool(before.loc['2024-01-31', 'A']))

    def test_weight_scenarios_raise_both_constraints(self):
        for name, expected in [('weight_8pct', .08), ('weight_10pct', .10)]:
            cfg = study.CASES[name]
            self.assertAlmostEqual(min(cfg['max_weight_per_stock'],
                                       cfg['risk_pct_per_trade'] / .15), expected)

    def test_runner_profile_matches_exploratory_study_case(self):
        self.assertEqual(study.rb.RISK_PROFILES['default'], {})
        profile = study.rb.RISK_PROFILES['exploratory_10_12_bear50']
        for key, expected in study.CASES['combined_10_12_bear50'].items():
            self.assertEqual(profile[key], expected)
        self.assertEqual(profile['top_n'], 10)


if __name__ == '__main__':
    unittest.main()

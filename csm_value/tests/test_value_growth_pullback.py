import sys
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from csm_value_strategy import value_growth_pullback_score


class ValueGrowthPullbackTest(unittest.TestCase):
    def test_value_eligibility_and_neutral_missing_components(self):
        idx=pd.DatetimeIndex(['2024-06-28'])
        cols=['A','B','C']
        value=pd.DataFrame([[1.,2.,np.nan]],index=idx,columns=cols)
        growth=pd.DataFrame([[np.nan,1.,99.]],index=idx,columns=cols)
        a3=pd.DataFrame([[np.nan,.9,9.]],index=idx,columns=cols)
        q5=pd.DataFrame([[np.nan,.8,9.]],index=idx,columns=cols)
        score,pullback=value_growth_pullback_score(value,growth,a3,q5)
        self.assertAlmostEqual(score.loc[idx[0],'A'],.55*.5+.20*.5+.25*.5)
        self.assertAlmostEqual(pullback.loc[idx[0],'A'],.5)
        self.assertTrue(pd.isna(score.loc[idx[0],'C']))
        self.assertTrue(pd.isna(pullback.loc[idx[0],'C']))

    def test_later_inputs_do_not_change_prior_ranks(self):
        idx=pd.DatetimeIndex(['2024-06-28','2024-07-31'])
        base=pd.DataFrame([[1.,2.],[3.,4.]],index=idx,columns=['A','B'])
        before=value_growth_pullback_score(base,base,base,base)[0]
        later=base.copy();later.loc[idx[1]]=[100.,-100.]
        after=value_growth_pullback_score(later,later,later,later)[0]
        pd.testing.assert_series_equal(before.iloc[0],after.iloc[0])


if __name__=='__main__':unittest.main()

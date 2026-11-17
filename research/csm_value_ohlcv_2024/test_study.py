import unittest
from types import SimpleNamespace

import numpy as np
import pandas as pd

from study import candidate_factors, overlays


class StudyCausalityTest(unittest.TestCase):
    def test_ohlcv_features_do_not_change_when_future_prices_change(self):
        dates=pd.bdate_range('2019-01-01','2021-02-28')
        a=np.arange(len(dates),dtype=float)
        prices=pd.DataFrame({'AAA':100+a/10,'BBB':100+a/20},index=dates)
        labels=prices.resample('ME').last().index
        def calculate(p):
            return overlays(SimpleNamespace(prices=p,factors=pd.DataFrame(1.,index=labels,columns=p.columns)))
        original=calculate(prices)
        modified=prices.copy();modified.loc['2021-01-01':]*=10
        altered=calculate(modified)
        for name in original:
            pd.testing.assert_frame_equal(original[name].loc[:'2020-12-31'],altered[name].loc[:'2020-12-31'])

    def test_value_eligibility_and_missing_secondary_are_handled(self):
        base=pd.DataFrame([[1.,2.,np.nan]],index=[pd.Timestamp('2020-12-31')],columns=['A','B','C'])
        signal=pd.DataFrame([[np.nan,4.,99.]],index=base.index,columns=base.columns)
        result=candidate_factors(base,{'momentum_12_1':signal},'momentum_12_1')
        self.assertTrue(pd.notna(result.loc[base.index[0],'A']))
        self.assertTrue(pd.isna(result.loc[base.index[0],'C']))
        self.assertAlmostEqual(result.loc[base.index[0],'A'],.75*.5+.25*.5)


if __name__=='__main__':unittest.main()

from common import transform_data
import common.constants as cn
from common.data_provider import DataProvider
from common_python.testing import helpers

import numpy as np
import os
import pandas as pd
import unittest


IGNORE_TEST = False


class TestDataTransformer(unittest.TestCase):

  def setUp(self):
    if IGNORE_TEST:
      return
    self._init()

  def _init(self):
    self.provider = DataProvider()
    self.provider.do()

  def testMakeTrinaryData(self):
    if IGNORE_TEST:
      return
    df = transform_data.makeTrinaryData(
        df=self.provider.df_normalized)
    columns = self.provider.df_normalized.columns
    self.assertTrue(helpers.isValidDataFrame(df, columns))

  def testAggregateGenes(self):
    if IGNORE_TEST:
      return
    provider = DataProvider()
    provider.do()
    df = transform_data.aggregateGenes(provider=provider)
    self.assertTrue(helpers.isValidDataFrame(df,
        provider.df_normalized.columns))

  def testNormalizeSample(self):
    if IGNORE_TEST:
      return
    provider = DataProvider(is_normalize=False)
    provider.do()
    df = provider.dfs_data[0]
    df_result = transform_data.trinaryReadsDF(df_sample=df)
    # See if number of "-1" is excessive
    dff = df_result + df_result.applymap(lambda v: -np.abs(v))
    frac_minus1 = -dff.sum().sum()  \
        /(2*len(df_result)*len(df_result.columns))
    self.assertLess(frac_minus1, 0.2)

  def testCalcTrinaryComparison(self):
    if IGNORE_TEST:
      return
    df_in = pd.DataFrame({'a': [4, 0.20, 1]})
    df_expected = pd.DataFrame({'a': [1, -1, 0]})
    df_out = transform_data.calcTrinaryComparison(df_in)
    self.assertTrue(df_out.equals(df_expected))
    #
    df_out = transform_data.calcTrinaryComparison(df_in,
        ser_ref=df_in['a'])
    trues = [v == 0 for v in df_out['a']]
    self.assertTrue(all(trues))


if __name__ == '__main__':
  unittest.main()

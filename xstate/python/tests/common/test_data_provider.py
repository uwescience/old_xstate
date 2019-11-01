from common import data_provider
import common.constants as cn
from common_python.testing import helpers
from common_python.util.persister import Persister

import copy
import numpy as np
import os
import pandas as pd
import unittest


IGNORE_TEST = False
SIZE = 4


class TestDataProvider(unittest.TestCase):

  def setUp(self):
    self.provider = data_provider.DataProvider()
 
  def tearDown(self):
    persister = Persister(cn.DATA_PROVIDER_PERSISTER_PATH)
    persister.remove()

  def init(self):
    self.df_data = self.provider._makeDFFromCSV(
        data_provider.FILENAME_READS)
    self.df_gene_description =  \
        self.provider._makeGeneDescriptionDF()
    self.provider.df_gene_description = self.df_gene_description
    self.df_data = self.df_data.set_index(cn.GENE_ID)

  def makeData(self, size=SIZE):
    df_data = pd.DataFrame({'a': range(10)})
    self.provider.dfs_data = [df_data for _ in range(SIZE)]

  def checkDF(self, df, is_check_index=True):
    """
    Verifies DataFrames
    :param pd.DataFrame df:
    :param bool is_check_index: checks that index is GENE
    """
    # Non-zero length
    self.assertGreater(len(df), 0)
    # Has the right index
    if is_check_index:
      b = set(df.index).issubset( self.df_gene_description.index)
      if not b:
        import pdb; pdb.set_trace()
      self.assertTrue(b)
    # No nan values
    trues = [not np.nan in df[c] for c in df.columns]
    self.assertTrue(all(trues))
  
  def testEquals(self):
    if IGNORE_TEST:
      return
    self.assertTrue(self.provider.equals(self.provider))
    provider = copy.deepcopy(self.provider)
    self.provider.do()
    self.assertFalse(self.provider.equals(provider))
    self.assertTrue(self.provider.equals(self.provider))

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.init()
    self.assertTrue("data" in self.provider._data_dir)

  def testmakeDFFromCSV(self):
    if IGNORE_TEST:
      return
    self.init()
    df = self.provider._makeDFFromCSV(data_provider.FILENAME_HYPOXIA)
    self.assertGreater(len(df), 0)

  def testMakeDataDFS(self):
    if IGNORE_TEST:
      return
    def test(**kwargs):
      dfs = self.provider._makeDataDFS(**kwargs)
      self.assertEqual(len(dfs), data_provider.NUM_REPL)
      for df in dfs:
        self.assertGreater(len(df), 0)
      return dfs
    #
    self.provider.do()
    dfs1 = test()
    dfs2 = test(is_normalize=False)
    for idx in range(len(dfs1)):
      df1 = dfs1[idx]
      df2 = dfs2[idx]
      for index in df1.index:
        self.assertTrue(np.isclose(np.mean(df1.loc[index, :]), 0))
        trues = [v >= 0 for v in df2.loc[index, :]]
        self.assertTrue(all(trues))
    #
    dfs = self.provider._makeDataDFS(is_normalize=False)

  def testMakeHypoxiaDF(self):
    if IGNORE_TEST:
      return
    self.init()
    df = self.provider._makeHypoxiaDF()
    expected_columns = [
        cn.STD, cn.CV, cn.HOURS, cn.SAMPLE, cn.MEAN, 0, 1, 2]
    trues = [c in df.columns for c in expected_columns]
    self.assertTrue(all(trues))
    self.assertGreater(len(df), 0)

  def testMakeGeneDescriptionDF(self):
    if IGNORE_TEST:
      return
    self.init()
    df = self.provider._makeGeneDescriptionDF()
    self.checkDF(df)

  def testGetNumRepl(self):
    if IGNORE_TEST:
      return
    self.init()
    self.provider.dfs_data = range(3)
    self.assertEqual(self.provider._getNumRepl(), 3)

  def testMakeMeanDF(self):
    if IGNORE_TEST:
      return
    self.init()
    self.makeData()
    df = self.provider._makeMeanDF()
    self.assertTrue(df.equals(self.provider.dfs_data[0]))

  def testMakeStdDF(self):
    if IGNORE_TEST:
      return
    self.init()
    self.makeData()
    df = self.provider._makeStdDF()
    self.assertTrue(np.isclose(df.sum().sum(), 0))

  def testReduceDF(self):
    if IGNORE_TEST:
      return
    self.init()
    df = self.provider._reduceDF(self.df_data)
    self.assertGreater(len(self.df_data), len(df))
    difference = set(df.columns).symmetric_difference(
        self.df_data.columns)
    self.assertEqual(len(difference), 0)

  def testDo(self):
    if IGNORE_TEST:
      return
    self.init()
    self.provider.do()
    self.assertEqual(len(self.provider.dfs_data),
        data_provider.NUM_REPL)
    [self.checkDF(df) for df in self.provider.dfs_data]
    dfs = [
        self.provider.df_gene_description,
        self.provider.df_mean,
        self.provider.df_std,
        self.provider.df_cv,
        self.provider.df_normalized,
        self.provider.df_gene_expression_state,
        ]
    dfs.extend(self.provider.dfs_data)
    [self.checkDF(df) for df in dfs]
    dfs = [
        self.provider.df_kegg_gene_pathways, 
        self.provider.df_go_terms, 
        self.provider.df_ec_terms, 
        self.provider.df_ko_terms, 
        self.provider.df_kegg_pathways, 
        ]
    [self.checkDF(df, is_check_index=False) for df in dfs]
    columns = self.provider.df_stage_matrix.columns
    diff = set(columns).symmetric_difference(
        [cn.STAGE_NAME, cn.STAGE_COLOR])
    self.assertEqual(len(diff), 0)
    self.assertGreater(len(self.provider.df_stage_matrix), 0)

  def testPersistence(self):
    if IGNORE_TEST:
      return
    self.provider.do()
    provider = data_provider.DataProvider()
    provider.do()
    self.provider.equals(provider)

  def testNormalizeReadsDF(self):
    if IGNORE_TEST:
      return
    provider = data_provider.DataProvider(is_normalize=False,
        is_only_qgenes=False)
    provider.do()
    df = provider.dfs_data[0]
    df_normalized = provider.normalizeReadsDF(df)
    self.assertTrue(helpers.isValidDataFrame(df_normalized,
        df.columns))
    self.assertEqual(len(df), len(df_normalized))
    ser_length = provider.df_gene_description[cn.LENGTH]


if __name__ == '__main__':
  unittest.main()

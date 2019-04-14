from common import data_provider
import common.constants as cn
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
    Verifies that the index are genes.
    """
    # Non-zero length
    self.assertGreater(len(df), 0)
    # Has the right index
    if is_check_index:
      b = set(df.index).issubset( self.df_gene_description.index)
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
    self.init()
    self.provider.df_gene_description =  \
        self.provider._makeGeneDescriptionDF()
    dfs = self.provider._makeDataDFS()
    self.assertEqual(len(dfs), data_provider.NUM_REPL)
    for df in dfs:
      self.assertGreater(len(df), 0)

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

  def testMakeDataDFS(self):
    if IGNORE_TEST:
      return
    self.init()
    dfs = self.provider._makeDataDFS()
    self.assertEqual(len(dfs), data_provider.NUM_REPL)
    [self.checkDF(df) for df in dfs]

  def testDo(self):
    if IGNORE_TEST:
      return
    self.init()
    self.provider.do()
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
    self.checkDF(self.provider.df_go_terms, is_check_index=False)
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


if __name__ == '__main__':
  unittest.main()

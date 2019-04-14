from terms.term_matrix import TermMatrix
from common_python.testing import helpers
import common.constants as cn

import numpy as np
import os
import pandas as pd
import unittest


IGNORE_TEST = False
IS_PLOT = False


class TestTermMatrix(unittest.TestCase):

  def setUp(self):
    self.matrix = TermMatrix(is_plot=IS_PLOT)

  def testConstructor(self):
    if IGNORE_TEST:
      return
    self.assertTrue(helpers.isValidDataFrame(self.matrix.df_matrix,
        self.matrix.df_matrix.columns))

  def testMakeTimeAggregationMatrix(self):
    if IGNORE_TEST:
      return
    df = self.matrix.makeTimeAggregationMatrix()
    self.assertTrue(helpers.isValidDataFrame(df,
        self.matrix.df_matrix.columns))
    self.assertEqual(len(df), cn.NUM_TIMES)

  def testPlotAggregation(self):
    if IGNORE_TEST:
      return
    # Only smoke tests
    self.matrix.plotTimeAggregation(is_up_regulated=False)
    self.matrix.plotTimeAggregation(is_up_regulated=True)


if __name__ == '__main__':
  unittest.main()

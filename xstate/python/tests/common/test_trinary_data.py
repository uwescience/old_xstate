import common.constants as cn
from common.trinary_data import TrinaryData
from common_python.testing import helpers

import numpy as np
import os
import pandas as pd
import unittest


IGNORE_TEST = False


class TestTrinaryData(unittest.TestCase):

  def setUp(self):
    self.trinary = TrinaryData()

  def testConstructor(self):
    self.assertIsNone(self.trinary.df_X)

  def testInit(self):
    self.trinary.init()
    self.assertTrue(helpers.isValidDataFrame(self.trinary.df_X,
        self.trinary.df_X.columns))
    self.assertEqual(len(self.trinary.df_X.columns),
        len(self.trinary.features))
    self.assertEqual(len(self.trinary.df_X),
        len(self.trinary.ser_state))
    
    

if __name__ == '__main__':
  unittest.main()
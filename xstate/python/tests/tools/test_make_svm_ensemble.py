import common.constants as cn
from tools import make_svm_ensemble
from common_python.testing import helpers

import os
import unittest

IGNORE_TEST = False
TEST_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_PATH = os.path.join(TEST_DIR, "test_make_svm_ensemble.pcl")


class TestMakeSVMEnsemble(unittest.TestCase):

  def deleteFiles(self):
    if os.path.isfile(TEST_PATH):
      os.remove(TEST_PATH)

  def setUp(self):
    self.deleteFiles()

  def tearDown(self):
    self.deleteFiles()

  def testMake(self):
    if IGNORE_TEST:
      return
    make_svm_ensemble.make(file_path=TEST_PATH)
    self.assertTrue(os.path.isfile(TEST_PATH))
      

if __name__ == '__main__':
  unittest.main()

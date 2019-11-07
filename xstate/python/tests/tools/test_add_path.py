import common.constants as cn
from tools import add_path

import os
import sys
import unittest

IGNORE_TEST = False


class TestFunctions(unittest.TestCase):

  def setUp(self):
    pass


  def testAddPaths(self):
    if IGNORE_TEST:
      return
    paths = list(sys.path)
    add_path.add_paths()
    self.assertEqual(len(paths) + 2, len(sys.path))
      

if __name__ == '__main__':
  unittest.main()

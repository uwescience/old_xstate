from plots import util_plots

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import unittest


IGNORE_TEST = False
IS_PLOT = False


class TestFunctions(unittest.TestCase):

  def testPlotStateTransitions(self):
    if IGNORE_TEST:
      return
    # Smoke test only
    util_plots.plotStateTransitions(is_plot=IS_PLOT)

  def testPlotThresholdHeatmap(self):
    if IGNORE_TEST:
      return
    # Smoke test only
    util_plots.plotThresholdHeatmap(is_plot=IS_PLOT)

  def testPlotClusteredHeatmap(self):
    if IGNORE_TEST:
      return
    # Smoke test only
    util_plots.plotClusteredHeatmap(is_plot=IS_PLOT)

if __name__ == '__main__':
  unittest.main()

""" Functions that transform DataFrames. """

from common import constants as cn
from common.data_provider import DataProvider

import pandas as pd
import numpy as np


def makeTrinaryData(df=None, min_abs=1.0, is_include_nan=True):
  """
  Thresholds data based on its absolute magnitude.
  Values are assigned as -1, 0, 1
  :param pd.DataFrame df: default is provider.df_normalized
  :param float min_abs: minimal absolute value to threshold.
  :param bool is_include_nan: Include nan values; else set to 0
  :return pd.DataFrame: same index and columns as df
  """
  if df is None:
    provider = DataProvider()
    provider.do()
    df = provider.df_normalized
  df_result = df.copy()
  df_result = df_result.applymap(
      lambda v: 0 if np.abs(v) < min_abs else -1 if v < 0 else 1)
  if is_include_nan:
      df_result = df_result.applymap(
         lambda v: np.nan if v==0 else v)
  return df_result

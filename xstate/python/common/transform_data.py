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

def aggregateGenes(provider=None):
  """
  Combines genes that are perfectly correlated in time for trinary
  values.
  :param DataProvider provider:
  :return pd.DataFrame: names are combined for aggregated
      genes.
  """
  if provider is None:
    provider = DataProvider()
    provider.do()
  df = provider.df_normalized
  df_trinary = makeTrinaryData(df, is_include_nan=False)
  dfg = df_trinary.groupby(df_trinary.columns.tolist())
  groups = dfg.groups
  data = {}
  for key, genes in groups.items():
    label = "--".join(genes)
    data[label] = list(key)
  df = pd.DataFrame(data)
  df_result = df.T
  df_result.columns = df_trinary.columns
  return df_result

def normalizeSample(csv_file, df_sample=None):
  """
  Normalizes one or more samples of readcounts. Normalizations involve:
  (a) adjusting for gene length, (b) library size, (c) log2, (d) ratio w.r.t. T0.
  Data may come from an existing dataframe or a CSV file.
  :param str csv_file: File in "samples" directory.
      columns are: "GENE_ID", instance ids
  :param pd.DataFrame df: columns are genes, index are instances, values are readcounts
  :param bool is_convert_to_trinary: return trinary values
  :return pd.DataFrame: columns are genes, indexes are instances, trinary values
  At least one of df_sample and csv_path must be non-null
  """
  provider = DataProvider(is_normalize=False)
  provider.do()
  if df_sample is None:
    path = os.join(cn.SAMPLES_DIR, csv_file)
    df_sample = pd.read_csv(csv_path)
    df_sample = df_sample.T
  #
  df_normalized = normalizeGeneReads(df_sample)
  # Compute trinary values relative to original reads
 
def normalizeGeneReadsDF(df):
  """
  Adjusts read counts for each gene based on length and library size.
  :param pd.DataFrame df: 
      index are genes, columns are instances, values are readcounts
  :return pd.DataFrame: 
      index are genes, columns are instances, values are readcounts
  """
  provider = DataProvider()
  provider.do()
  # Adjust for library size
  ser_tot = df.sum(axis=0)
  df_result = df/ser_tot
  # Adjust for gene length
  for gene in df.index:
    df_result.loc[gene, :] = df_result.loc[gene,:] \
        / provider.df_gene_description.loc[gene, cn.LENGTH]
  #
  return df_result

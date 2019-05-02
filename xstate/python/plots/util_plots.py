"""Commonly used plot routines."""

from common.data_provider import DataProvider
from common import transform_data
from common import constants as cn
from common_python.dataframe import util_dataframe
from common_python.plots import util_plots as cup
from common_python.statistics import util_statistics

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.cluster import KMeans


CLUSTER = "cluster"

def getDF(df):
  """
  Returns a dataframe
  """
  if df is None:
    provider = getProvider(None)
    df = provider.df_noramlized
  return df

def getProvider(provider):
  """
  Returns a provider
  """
  if provider is None:
    provider = DataProvider()
    provider.do()
  return provider

def plotStateTransitions(provider=None, ymax=10e3, ax=None,
    is_plot=True):
  """
  Plots vertical lines for state transitions.
  :param DataProvider provider:
  """
  provider = getProvider(provider)
  df_stages = provider.df_stage_matrix
  if ax is None:
    ax = plt.gca()
  ax.set_xlabel("times")
  # Add the states
  dfg = df_stages.groupby(cn.STAGE_NAME)
  timepoints = df_stages.index.tolist()
  for key in dfg.groups:
    timepoint = dfg.groups[key][-1]
    xval = timepoints.index(timepoint) + 1
    ax.plot([xval, xval], [0, ymax], 'b--')
  if is_plot:
    plt.show()

def plotThresholdHeatmap(provider=None, df=None, 
        ax=None, is_plot=True, min_abs=1.0, **kwargs):
  """
  Plots normalized thresholded expression levels.
  :param DataProvider provider: 
  :param pd.DataFrame df: dataframe to plot with trinary values
  :param plt.Axis ax:
  :param bool is_plot: shows plot if True
  :param float min_abs: minimum absolute for threshold
  :param dict kwargs: plotting options
  """
  # Data setup
  provider = getProvider(provider)
  if df is None:
    df = provider.df_normalized
    df_plot = transform_data.thresholdData(df, min_abs=min_abs)
  else:
    df_plot = df.copy()
  df_stages = provider.df_stage_matrix.copy()
  # Plot construct
  if ax is None:
    plt.figure(figsize=(16, 10))
    ax = plt.gca()
  if not 'title' in kwargs.keys():
      title = "Normalized Data"
  else:
      title = kwargs["title"]
  plot_kwargs = {
    cup.XLABEL: "times",
    cup.YLABEL: "gene",
    cup.TITLE: title,
    }
  cup.plotTrinaryHeatmap(df_plot, ax=ax, **plot_kwargs, is_plot=False)
  columns = df_plot.columns
  ax.set_xticks(np.arange(len(columns)))
  ax.set_xticklabels(columns)
  plotStateTransitions(provider=provider, ax=ax, 
      ymax=len(df_plot), is_plot=False)
  if is_plot:
    plt.show()

def plotClusteredHeatmap(provider=None, ncluster=5, **kwargs):
  """
  Plots a heatmap where categorical axes are grouped with similar values.
  :param DataProvider provider: 
  :param int ncluser: number of clusters
  :param dict kwargs: plot parameters
  """
  provider = getProvider(provider)
  df = transform_data.thresholdData(provider.df_normalized, is_include_nan=False)
  df = util_dataframe.pruneSmallRows(df, min_abs=1.0)
  kmeans = KMeans(n_clusters=ncluster, random_state=0).fit(df)
  df[CLUSTER] = kmeans.labels_
  df = df.sort_values(CLUSTER)
  del df[CLUSTER]
  df = df.applymap(
      lambda v: np.nan if np.isclose(v, 0) else v)
  plotThresholdHeatmap(provider=provider, df=df,
      title="Clustered Differential Expression", **kwargs)

def plotClustermap(provider=None, is_up_regulated=True, 
    is_plot=True):
  """
  Plots a heatmap where categorical axes are grouped with similar values.
  :param DataProvider provider: 
  :param bool is_up_regulated: Test for up regulated genes
  :param bool is_plot: plot the result
  """
  provider = getProvider(provider)
  df = provider.df_normalized
  if not is_up_regulated:
    df = df.applymap(lambda v: -v)
  df_filtered = util_statistics.filterZeroVarianceRows(df)
  df_log = util_statistics.calcLogSL(df_filtered)
  # Construct a cluster map
  cg = sns.clustermap(df_log, col_cluster=False, 
      cbar_kws={"ticks":[0,5]}, cmap="Blues")
  # Set the labels
  cg.ax_heatmap.set_xlabel("Time")
  # Adjust for clustermap
  xticks = cg.ax_heatmap.get_xticks() - 0.5
  cg.ax_heatmap.set_xticks(xticks)
  if is_up_regulated:
    direction = "Up"
  else:
    direction = "Down"
  title = "-log10 zscores of %s-Regulated gene counts" % (direction)
  cg.ax_heatmap.set_title(title)
  # Don't show the genes
  cg.ax_heatmap.set_yticklabels([])
  cg.ax_heatmap.set_yticks([])
  # Add the state transitions
  plotStateTransitions(ymax=len(df_log),
      ax=cg.ax_heatmap, is_plot=False)
  #
  if is_plot:
    plt.show()

"""Normalized Trinary Data."""
"""
df_X - feature matrix with numeric column names.
       T0 is deleted
ser_state - state values
features - names of genes
state_dict - dictionary mapping string names to numbers
"""

import common.constants as cn
from common.data_provider import DataProvider
import common.transform_data as transform_data

class TrinaryData(object):

  def __init__(self, provider=None):
    if provider is None:
      provider = DataProvider()
      provider.do()
    self.provider = provider
    self.df_X = None  # Feature matrix indexed by number
    self.features = None
    self.ser_state = None
    self.state_dict = None

  def init(self):
    self.df_X = transform_data.aggregateGenes(provider=self.provider)
    self.df_X = self.df_X.T
    self.df_X = self.df_X.drop(index="T0")
    self.features = self.df_X.columns
    self.df_X.columns = range(len(self.features))
    # Create class information
    ser_state = self.provider.df_stage_matrix[cn.STAGE_NAME]
    ser_state = ser_state.drop(index="T0")
    ser_state = ser_state.copy()
    ser_state[ser_state == 'Normoxia'] = 'Resuscitation'
    # Create converter from state name to numeric index
    states = ser_state.unique()
    self.state_dict = {k: v for v, k in enumerate(states)}
    self.ser_state = ser_state.apply(lambda k: self.state_dict[k] )

  def getX(self):
    if self.df_X is None:
      self.init()
    return self.df_X

  def getState(self):
    if self.ser_state is None:
      self.init()
    return self.ser_state

  def getFeature(self):
    if self.features is None:
      self.init()
    return self.features

  def getStateDict(self):
    if self.state_dict is None:
      self.init()
    return self.state_dict

def makeFeatureColumns(provider):
    df_X = transform_data.aggregateGenes(provider=provider)
    df_X = df_X.T
    return df_X.columns.tolist()


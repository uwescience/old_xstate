"""Normalized Trinary Data."""
"""
df_X - feature matrix with numeric column names.
       T0 is deleted
ser_y - state values
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
    self.ser_y = None
    self.state_dict = None
    self.init()

  def init(self):
    self.df_X = transform_data.aggregateGenes(provider=self.provider)
    self.df_X = self.df_X.T
    self.df_X = self.df_X.drop(index="T0")
    self.features = self.df_X.columns.tolist()
    self.df_X.columns = range(len(self.features))
    # Create class information
    ser_y = self.provider.df_stage_matrix[cn.STAGE_NAME]
    ser_y = ser_y.drop(index="T0")
    ser_y = ser_y.copy()
    ser_y[ser_y == 'Normoxia'] = 'Resuscitation'
    # Create converter from state name to numeric index
    states = ser_y.unique()
    self.state_dict = {k: v for v, k in enumerate(states)}
    self.ser_y = ser_y.apply(lambda k: self.state_dict[k] )

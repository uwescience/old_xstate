"""Creates an SVM classifier from the time course expression data."""

from common import constants as cn
from common.trinary_data import TrinaryData
from common_python.classifier import classifier_ensemble
from common import transform_data

import os
import numpy as np
import pandas as pd

import numpy as np
import pandas as pd

def make(num_features=15, num_classifiers=50, 
    file_path=cn.ENSEMBLE_PATH):
  """
  Creates a classifier ensemble from the time course data,
  and fits the classifier.
  :param int num_features: number of features in the ensemble
  :param int num_classifiers: number of classifiers
  :param str file_path: path where classifier is exported
  :return  ClassifierEnsemble:
  """
  data = TrinaryData()
  data.df_X.head()`
  svm_ensemble = classifier_ensemble.ClassifierEnsemble(
          classifier_ensemble.ClassifierDescriptorSVM(), 
          filter_high_rank=num_features, size=num_classifiers)
  data.df_X.columns = data.features
  svm_ensemble.fit(data.df_X, data.ser_y)
  svm_ensemble.exportEnsembleFile(file_path)

if __name__ == '__main__':
  # Do arg parse with errors

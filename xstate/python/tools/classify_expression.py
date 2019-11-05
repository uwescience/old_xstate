"""Classifies expression data."""

from common import constants as cn
from common import transform_data
from tools import make_svm_ensemble

import argparse
import os
import numpy as np
import pandas as pd


def processExpressionData(data_path, parameter_file=cn.ENSEMBLE_PATH):
  """
  Performs classification on expression data.
  Expression data is structured as a comma separated variable (CSV)
  file. Rows are instances to classify. Columns are genes.
  The first row (header row) contains the names of genes for columns.
  :param str data_path: path to the expression data
  :param str parameter_file: path containing ensemble parameters
  Writes classifications to standard out.
  """
  svm_ensemble = make_svm_ensemble.make(file_path=parameter_file,
      is_force=False)
  df_trinary = transform_data.trinaryReadsDF(csv_file=data_path)
  return svm_ensemble.predict(df_trinary)


if __name__ == '__main__':
  # Do arg parse with errors
  desc = 'Classifies gene expression data.'
  parser = argparse.ArgumentParser(description=desc)
  parser.add_argument('--pfile', '-p',
       help='classifier parameter file',
      default=cn.ENSEMBLE_PATH)
  parser.add_argument('dfile',
      help='path to file containing expression data',
      type=str)
  args = parser.parse_args()
  result = processExpressionData(args.dfile, pfile=args.pfile)
  import pdb; pdb.set_trace()
  print(result)

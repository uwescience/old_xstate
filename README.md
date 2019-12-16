<img src="https://api.travis-ci.org/uwescience/xstate.svg?branch=master" width="100"/>
   
# xstate: State Analysis for Gene Expression

## Developer Usage Notes
1. Execute ``source setup_env.sh`` at the directory root
1. Run python codes from the directory src/python

## Installation
1. Use ``git clone --recursive-submodules https://github.com/uwescience/xstate.git``

## Installation and Usage

1. Install python 3.6 or higher
1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). To see if git is already installed on your machine:
   - Open a terminal session.
   - Type ``git --version``. If a git version number is returned, then git is installed.
1. Install [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
1. Clone the repository using ``git clone --recursive https://github.com/uwescience/xstate.git``
1. Change directory to the repo using ``cd xstate``
1. Create a miniconda virtual environment  with dependencies
using ``conda env create -f environment.yml``

Update the classifiers:
1. Start a new terminal session and change directory to ``xstate``.
1. Activate the virtual environment using ``conda activate xstate``
1. From the top level repository directory, ``python xstate/xstate/python/tools/make_svm_classifier.py``. (On windows, use ``\`` instead of ``/``.
1. Deactivate the virtual environment using ``conda deactivate``

Run a classification:
1. Start a new terminal session, change directory to ``xstate``, and activate the virtual environment.
1. From the top level repository directory, ``python xstate/xstate/python/tools/classify_expression.py <data_file>``. (On windows, use ``\`` instead of ``/``. Note: It is assumed that \<data file\> is
in the ``samples`` directory under ``data``. To change the directory,
use the ``--dir`` option.
1. Deactivate the virtual environment.

<img src="https://api.travis-ci.org/uwescience/xstate.svg?branch=master" width="100"/>
   
# xstate: State Analysis for Gene Expression

## Developer Usage Notes
1. Execute ``source setup_env.sh`` at the directory root
1. Run python codes from the directory src/python

## Installation
1. Use git clone --recursive <repository path>

## Installation and Usage

1. Install python 3.6 or higher
1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). To see if git is already installed on your machine:
   - Open a terminal session.
   - Type ``git --version``. If a git version number is returned, then git is installed.
1. Install [miniconda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/)
1. Clone the repository using ``git clone https://github.com/ModelEngineering/xstate.git``
1. Use git clone --recursive https://github.com/uwescience/xstate.git``
1. Change directory to the repo using ``cd xstate``
1. Create a miniconda virtual environment  with dependencies
using ``conda env create -f environment.yml``
1. Start a new terminal session and change directory to ``xstate``.
1. Activate the virtual environment using ``conda activate sbmllint``
1. Install Tellurium using ``pip install tellurium``
1. Deactivate the virtual environment using ``conda deactivate``

To do GAMES and moiety analysis from the command line for a file path:
1. Start a new terminal session.
1. Change directory to the cloned repository.
1. Activate the virtual environment
1. There are copies of several BioModels files in ``data/biomodels`` or ``data\biomodels`` in Windows.
Use ``/`` or ``\``  as appropriate for your system in the following instructions.
   - To run games for a file in this directory, use
``python xstate/tools/games.py data/biomodels/<file name>``
   - To run moiety analysi for a file in this directory, use
``python xstate/tools/moiety\_analysis.py data/biomodels/<file name>``
1. Deactivate the virtual environment

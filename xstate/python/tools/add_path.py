"""Ensures that the correct root path is present."""
import os
import sys

def getRootDir():
  root_dir = os.path.dirname(os.path.abspath(__file__))
  for _ in range(4):  # Root is 3 directories up
    root_dir = os.path.dirname(root_dir)
  return root_dir

def add_paths():
  root_dir = getRootDir()
  code_dir = root_dir
  for name in ["xstate", "python"]:
    code_dir = os.path.join(code_dir, name)
  sys.path.insert(0, code_dir)
  common_dir = os.path.join(root_dir, "common_python")
  sys.path.insert(0, common_dir)


add_paths()

"""Creates categorization data sets."""

"""
Category data sets:
  kegg_pathways: FILE_KEGG_PATHWAY FILE_KEGG_DESCRIPTION
  kegg_gene_pathway: FILE_KEGG_GENE, FILE_KEGG_PATHWAY
  kegg_gene_ec: FILE_KEGG_GENE, FILE_KEGG_EC
  kegg_gene_ko: FILE_KEGG_GENE, FILE_KEGG_KO
"""


import common.constants as cn
import common_python.constants as cpn
from common_python.bioinformatics import kegg_extractor

import os

# Files
FILE_KEGG_PATHWAYS = "kegg_pathways.csv"
FILE_KEGG_GENE_PATHWAY = "kegg_gene_pathway.csv"
FILE_KEGG_GENE_EC = "kegg_gene_ec.csv"
FILE_KEGG_GENE_KO = "kegg_gene_ko.csv"
FILES_KEGG = [
    FILE_KEGG_PATHWAYS,
    FILE_KEGG_GENE_PATHWAY,
    FILE_KEGG_GENE_EC,
    FILE_KEGG_GENE_KO,
    ]
    
# Names
MTV = "mtv"

def makePath(filename, directory):
  return os.path.join(directory, filename)

def writeFile(path, df_base, columns, directory):
  df = df_base[columns]
  df = df.copy()
  df = df.drop_duplicates()
  df.to_csv(makePath(path, directory), index=False)

def make(max_count=-1, directory=cn.DATA_DIR):
  extractor = kegg_extractor.KeggExtractor(MTV)
  # Do pathways
  df_pathways = extractor.listPathway()
  writeFile(FILE_KEGG_PATHWAYS, df_pathways, 
      df_pathways.columns, directory)
  # Other files
  df_base = extractor.getAllPathwayGenes(max_count=max_count)
  writeFile(FILE_KEGG_GENE_PATHWAY, df_base, 
      [cpn.KEGG_GENE, cpn.KEGG_PATHWAY], directory)
  writeFile(FILE_KEGG_GENE_EC, df_base, 
      [cpn.KEGG_GENE, cpn.KEGG_EC], directory)
  writeFile(FILE_KEGG_GENE_KO, df_base, 
      [cpn.KEGG_GENE, cpn.KEGG_KO], directory)


if __name__ == '__main__':
  make()

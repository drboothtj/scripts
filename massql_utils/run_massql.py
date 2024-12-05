'''
Runs massql query provided on a provided massql file
  Arguments:
    argv[1]: path to .mzml file
    argv[2]: query as string
NOTE: In future maybe make args easier to use
origional code procided by Dr. Sam Williams
''' 
from sys import argv
import os
from massql import msql_engine

def main(mzml: str, query: str) -> None:
  '''
  main routine
    arguments:
      mzml: path to .mzml file to query
      query: query string for massql
    returns:
      None
  '''
  results = msql_engine.process_query(query, mzml)
  output_path = os.path.basename(mzml) + '.tsv'
  #print(output_path)
  results.to_csv(output_path, sep='\t', index=False)

mzml = argv[1]
query = argv[2]
main(mzml, query)


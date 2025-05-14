'''
convert hmm .tbl into an actually readable format...
tested on output from hmmer3 - unsure of backwards compatability
adapted from code by Sam Williams (github.com/Sam-Will)
  arguments:
    [1]: search string for hmm.tbls - e.g. ('*.tbl')
    [2]: path for the output file (default: 'hmm_summary.csv')
'''
from sys import argv
from glob import glob
from typing import List
import re

def write_lines_to_csv(lines: List[str], filename: str) -> None:
  '''
  write file to a .csv
    arguments:
      lines: list of lines to be written
      filename: path for the output file
    returns:
      None
  '''
  with open(filename, "w") as write_file:
    for line in lines:
      write_file.writelines(line)
    

def get_data_from_tbl(tbl:str) -> List[str]:
  '''
  takes a single .tbl file from hmmer and 
  returns a list of strings with comma seperated data
    arguments: 
      tbl: path to .tbl file
    returns:
      data_line: list of strings of comma seperated data lines
  '''
  with open(tbl, "r") as tbl_file:
    cleaned_lines = []
    lines = tbl_file.readlines()
    for line in lines:
      if line[0] != '#':
        cleaned_line = tbl + ','
        cleaned_line += re.sub(' +', ',', line.strip()) + '\n'
        cleaned_lines.append(cleaned_line)
    return cleaned_lines

def main(search_string: str, output_filename: str) -> None:
  '''
  main routine
    arguments:
      search_string: 
        the search string for files of interest (e.g. '*.txt')
    returns:
      None
  '''
  file_paths = glob(search_string)
  write_lines = []
  for _file in file_paths:
    lines = get_data_from_tbl(_file)
    if len(lines) > 0:
      write_lines.append(lines)
  write_lines_to_csv(write_lines, output_filename)


search_string = argv[1]
#get default if no output
try:
  output_filename = argv[2]
except IndexError:
  output_filename = 'hmm_summary.csv' 
main(search_string, output_filename)


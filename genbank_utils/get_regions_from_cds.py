'''
extact the region or surrounding area from a cds
  arguments: 
    argv[1]: search string for gbks IMPORTANT: use quotes (e.g. '*.gbk')
    argv[2]: path to text file with CDS names
'''

from sys import argv
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.SeqFeature import SeqFeature, FeatureLocation
import glob


def get_code_from_gbk(file:str):
  '''
  read a genbank file
  '''
  with open(file, 'r') as gbk:
    for record in SeqIO.parse(gbk, 'genbank'):
      for feature in record.features:
        if feature.type == 'CDS':
          locus_tag = (feature.qualifiers['locus_tag'][0])
          return locus_tag.split('_')[0]

def read_txt(text_file):
  '''
  read text file and return lines
  '''
  with open(text_file, 'r') as file:
    lines = file.readlines()
    lines = [line.strip() for line in lines]
    return lines

def get_region(cds, file):
  '''
  ...
  '''
  with open(file, 'r') as gbk:
    records = SeqIO.parse(file, 'genbank')
  for record in records:
    for feature in record.features:
      if 'locus_tag' in feature.qualifiers:
        if feature.qualifiers['locus_tag'][0] == cds:
          start = feature.location.start - 20000
          end = feature.location.end + 20000
          seq = record.seq[start:end]
          sub_record = SeqRecord(
            seq,
            id=record.id,
            name=record.name,
            description=record.description + f" [sub-sequence {start}-{end}]",
            annotations=record.annotations)          
          sub_features = []
          for feature in record.features:
            if feature.location and feature.location.start >= start and feature.location.end <= end:
              new_location = FeatureLocation(feature.location.start - start, feature.location.end - start, feature.location.strand)
              new_feature = SeqFeature(location=new_location, type=feature.type, qualifiers=feature.qualifiers)
              sub_features.append(new_feature)
            sub_record.features = sub_features          
          return sub_record

def write_gbk(region, filename):
  '''
  writes the provided region to a file
  '''
  with open(filename, 'w') as output:
    SeqIO.write(region, output, 'genbank')

def main(files, cdses):
  '''
  main routine
    args: 
      files: a list of files from the search string
  '''
  #get codes from each genbank file
  codes = []
  for file in files:
    print('getting code from ' + file)
    codes.append({
      'name' : file,
      'code' : get_code_from_gbk(file)
    })
  #now match code and save region
  for cds in cdses:
    target_code = cds.split('_')[0]
    target_gbk = [_dict['name'] for _dict in codes if _dict['code']== target_code]
    if len(target_gbk) == 0:
      print('WARNING: No genbank contains code: ' + target_code)
    if len(target_gbk) > 1:
      print(f'WARNING: The code {target_code} is present in multiple files, skipping.')
    if len(target_gbk) == 1:
      print(f'INFO: Getting {target_code} from {target_gbk[0]}.')
      region = get_region(cds, target_gbk[0])
      filename = (cds + '_region.gbk')
      write_gbk(region, filename)
    
search_string = argv[1]
cdses = read_txt(argv[2])
files = glob.glob(search_string)
main(files, cdses)

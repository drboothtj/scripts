'''
takes two blast results files (.tsv) and identifies the entrys specific to one file
	[1]: family_tsv:
		 a .tsv file containing BLAST hits to family members (excluding genus of interest)
	[2]: genus_tsv:
		a .tsv file containing BLAST hits to the genus of interest
'''
from sys import argv
import csv
def read_tsv(path):
	'''
	reads .tsv from file
		arguments:
			path: path to .tsv file
		returns:
			lines: lines from the .tsv as a list
	'''
	with open(path) as tsv_file:
		tsv_data = csv.reader(tsv_file, delimiter = "\t")
		lines = [line for line in tsv_data]
	return lines

def get_genes(lines):
	'''
	gets a list of genes from tsv lines, default blastp output format
		arguments:
			lines: lines from a blastp .tsv file
		returns:
			gene_set: a set of gene names
	'''
	gene_set = set()
	for line in lines:
		gene_set.add(line[0])
	return gene_set

def compare_gene_sets(set1, set2):
	shared_members = set1.intersection(set2)
	set1_length = len(set1)
	set2_length = len(set2)
	number_of_shared = len(shared_members)
	print(f'Set 1 contains: {set1_length} members')
	print(f'Set 2 contains: {set2_length} members')
	print(f'{number_of_shared} are present in both sets')

def main(family_tsv, genus_tsv):
	print(f'comparing {family_tsv} and {genus_tsv}')
	family_tsv_lines = read_tsv(family_tsv)
	family_genes = get_genes(family_tsv_lines)
	genus_tsv_lines = read_tsv(genus_tsv)
	genus_genes = get_genes(genus_tsv_lines)
	compare_gene_sets(family_genes, genus_genes)

family_tsv = argv[1]
genus_tsv = argv[2]
main(family_tsv, genus_tsv)


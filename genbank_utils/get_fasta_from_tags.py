'''
Read a text list of locus tags and get them from .gbks in a directory. Only suitable for one locus per genome.
See get_fasta_from_genbank_multiple.py for multiple sequences per genome (slower!)

Arguments:
	argv[1]: file name of a txt file containing a list of locus tags
	argv[2:]: path to directory with genbank files, note: use quotes!
'''
import glob
from Bio import SeqIO
from sys import argv
import sys

def read_file(filename):
	'''
	read file with specified filename and return lines as list
	'''
	#print('reading ', filename)
	with open(filename, 'r') as f:
		lines =	f.read()
	return lines

def get_sequence(filename, annotations):
	'''
	searches a genbank file for a specific annotation or list of annotations
	'''
	records = read_file(filename)
	#print(filename)
	for record in SeqIO.parse(filename, 'genbank'):
		for feature in record.features:
			try:
				if feature.qualifiers['locus_tag'][0] in annotations:
					name = feature.qualifiers['locus_tag'][0]
					dna_sequence = str(feature.extract(record.seq))
					protein_sequence = str(feature.qualifiers['translation'][0])					
					return name, dna_sequence, protein_sequence
			except:
				pass

def write_fna(sequences):
	'''
	writes a nucleotide fasta file from a sequence tuple generated by this script 
	'''
	with open ('dna_sequences.fna', 'w') as f:
		for sequence in sequences:
			f.write(f">{sequence[0]}\n")
			f.write(f"{sequence[1]}\n")

def write_faa(sequences):
	'''
	writes a nucleotide fasta file from a sequence tuple generated by this script 
	'''
	with open('protein_sequences.faa', 'w') as f:
		for sequence in sequences:
			f.write(f">{sequence[0]}\n")
			f.write(f"{sequence[2]}\n")

def main(locus, target_files):
	#get list of annotations from .txt
	annotation_names = read_file(locus_file)

	#find each annotation from each genbank file... very slow method!
	files = []
	for _file in target_files: #handel wildcards without needing quotes
		files.extend(glob.glob(_file))

	assert len(files) != 0, 'No target files, remember to use a wildcard!'

	sequences = []
	for filename in files:
		if len(annotation_names) > 0:
			try:
				sequence = get_sequence(filename, annotation_names)
				sequences.append(sequence)
				annotation_names.remove(sequence[0])
        break
			except:
				pass

	sequences = [sequence for sequence in sequences if sequence is not None]
	assert len(sequences) != 0, 'No sequences found!'
	write_fna(sequences)
	write_faa(sequences)

locus = argv[1]
target_files = argv[2:]
main(locus, target_files)

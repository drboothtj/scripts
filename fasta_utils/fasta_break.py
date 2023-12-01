import getphylo.io as io

'''
Splits a fasta file into unique files per record.
    Arguments:
        argv[1]: path to fasta file to be split
'''
from sys import argv

filename = argv[1]

lines = io.read_file(filename)

joined = ''.join(lines)
unjoined = joined.split('>')

for line in unjoined[1:]:
    new_filename = line.split(' ')[0] + '.fasta'
    name = '>' + line
    new_lines = [name]
    new_lines.append(line.split(' ')[1])
    io.write_to_file(new_filename, new_lines)


'''
Splits a fasta file into unique files per record.
    Arguments:
        argv[1]: path to fasta file to be split
'''
from sys import argv

def write_file(lines, filename):
    '''
    write list to file 
        arguments: 
            lines: lines to be written
	    filename: file to write to
        returns: 
            none
    '''
    with open(filename, 'w') as _file:
        for line in lines:
            _file.write(line)

def read_file(filename):
    '''
    read a file to list
    '''
    with open(filename) as _file:
        lines_to_read = _file.readlines()
        lines = [line for line in lines_to_read]
    return lines

filename = argv[1]

lines = read_file(filename)

joined = ''.join(lines)
unjoined = joined.split('>')

for line in unjoined[1:]:
    #print(line[0:100])
    new_filename = line.split('\n')[0] + '.fasta'
    name = '>' + line
    new_lines = [name]
    new_lines.append(line.split('\n')[1])
    write_file(new_lines, new_filename)


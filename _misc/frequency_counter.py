'''
python script to count word frequency from a text file

	argv[1]: the name of the file to read
'''
from collections import Counter
from sys import argv

def read_lines(filename):
	with open(filename) as file:
		lines = file.readlines()
	return lines


filename = argv[1]
lines = read_lines(filename)
lines = [line.strip() for line in lines]
counts = Counter(lines)
counts = counts.most_common()

for word in counts:
	print(f'{word[0]}: {word[1]}')


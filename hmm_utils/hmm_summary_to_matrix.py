'''
convert tbls to a matrix
'''

from sys import argv
class Source():
    '''
    '''
    def __init__(self, name, lines):
        '''
        '''
        self.name = name
        self.lines = lines
        self.hits = self.get_hits(lines)
        self.best_hits = self.get_best_hits(self.hits)

    def get_hits(self, lines):
        '''
        '''
        hits = []
        for line in lines:
            name = line.split(',')[1]
            hmm = line.split(',')[3]
            e_value = line.split(',')[5]
            hit = Hit(name, hmm, e_value)
            hits.append(hit)
        return hits
            

    def get_best_hits(self, hits):
        '''
        '''
        best_hits = {}
        for hit in hits: 
            if hit.name not in best_hits or hit.e_value < best_hits[hit.name].e_value:
                best_hits[hit.name] = hit
        return list(best_hits.values())


class Hit():
    '''
    '''
    def __init__(self, name, hmm, e_value):
        '''
        '''
        self.name =name
        self.hmm = hmm
        self.e_value = e_value

    def __repr__(self):
        return f"Hit(name={self.name}, score={self.e_value}, hmm={self.hmm})"

def write_lines(lines, filename):
    '''
    '''
    with open(filename, 'w') as writefile:
        for line in lines:
            print(line)
            writefile.writelines(line + '\n')

def read_lines(filename):
    '''
    '''
    with open(filename, 'r') as readfile:
        lines = readfile.readlines()
    return lines

def main(filename: str) -> None:
    '''
    main routine
        arguments:
            filename: path to hmm_summary.csv (SEE OTHER SCRIPT IN THIS DIR)
    '''
    lines = read_lines(filename)
    sources = {}
    for line in lines:
        source = line.split(',')[0] 
        if source in sources:
            sources[source].append(line)
        else:
            sources[source] = [line]

    new_sources = []
    possible_hits = []
    for source in sources:
        new_source = Source(source, sources.get(source))
        possible_hits.extend([hit.hmm for hit in new_source.best_hits])
        new_sources.append(new_source)
    
    lines = ["-," + ",".join(possible_hits)]
    
    for source in new_sources:
        hits = [hit.hmm for hit in source.best_hits]
        pattern = ['1' if hit in hits else '0' for hit in possible_hits]
        line = [source.name]
        line.extend(pattern)
        line = ",".join(line)
        lines.append(line)
    write_lines(lines, 'output.csv')

filename = argv[1]
main(filename)

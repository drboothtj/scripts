'''
search a protein sequence against the nr database and get the most common genus from the top 10 hits
        arguments:
                argv[1]:
                        protein sequence as a string
                argv[2]: 
                        (optional) the RID of an existing search
                        useful if a search has already been initiated/completed
'''

import requests
import time
import re
from collections import Counter
from sys import argv
from bs4 import BeautifulSoup

def do_blastp(query: str) -> str:
        '''
        get blastp results from the blastp API
                arguments: 
                        query: a protein sequence as a string
                returns:
                        rid: the RID as a string
        '''
        url = "https://blast.ncbi.nlm.nih.gov/Blast.cgi"
        params = {
            "CMD": "Put",
            "PROGRAM": "blastp",
            "DATABASE": "nr",
            "QUERY": query,
            "FORMAT_TYPE": "XML",
            "MAX_TARGET_SEQS": 10 # I am not sure this is working...
        }
        response = requests.post(url, data=params)
        soup = BeautifulSoup(response.text, "html.parser")
        rid = soup.find("input", {"name": "RID"})["value"]
        print("Request ID:", rid)
        return rid

def check_blastp_results(rid: str) -> str:
        '''
        check for blastp results for a specific RID
                arguments:
                        rid: the RID as a string
                returns:
                        r.text: the XML output from blastp
        '''
        while True:
                r = requests.get(f"https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Get&FORMAT_TYPE=XML&RID={rid}")
                if "<Iteration_hits>" in r.text:
                        print("Results ready!")
                        break
                print(f"Waiting for results for rid: {rid}...")
                time.sleep(10)  # Wait before checking again
        return r.text

def parse_results(results):
        '''
        extracts the first 10 species names from the blastp XML
                arguments:
                        results: the XML output from blastP
                returns:
                        hit_species[0:10]: species binomials from the first 10 hit proteins
        '''
        hit_defs = re.findall(r"<Hit_def>(.*?)</Hit_def>", results)        
        hit_species = []
        for hit in hit_defs:
                match = re.search(r"\[(.*?)\]", hit)
                hit_species.append(match.group(1))
        return(hit_species[0:10])

query = argv[1]
try:
        rid = argv[2]
except:
        rid = do_blastp(query)
results = check_blastp_results(rid)
hit_species = parse_results(results)
genus_counter =(Counter([species.split()[0] for species in hit_species]))
print(genus_counter.most_common(1)[0][0])

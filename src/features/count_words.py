import json, re

def main():
    # load data
    
    path = '../data/processed/extracted_text'
    
    with open(path, 'r') as infile:
        data = list(map(json.loads, infile))
        print('data loaded is', data)
        infile.close()
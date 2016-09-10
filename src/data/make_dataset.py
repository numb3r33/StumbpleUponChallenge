import pandas as pd
import numpy as np
import json

from unidecode import unidecode

def extract_domain(url):
    # extract domains
    domain = url.lower().split('/')[2]
    domain_parts = domain.split('.')

    # e.g. co.uk
    if domain_parts[-2] not in ['com', 'co']:
        return '.'.join(domain_parts[-2:])
    else:
        return '.'.join(domain_parts[-3:])


def load_csv(filename):
    return pd.read_table(filename)

def parse_data(df):
    data = []
    columns = df.columns
    
    for key, row in df.iterrows():
        item = {}
        
        for column in columns:
            item[column] = row[column]
        
        # parse url
        
        item['real_url'] = row['url'].lower()
        item['domain'] = extract_domain(row['url'])
        item['tld'] = item['domain'].split('.')[-1]
        
        
        # parse boilerplate
        boilerplate = json.loads(row['boilerplate'])
        
        for f in ['title', 'url', 'body']:
            item[f] = boilerplate[f] if f in boilerplate else u''
            item[f] = unidecode(item[f]) if item[f] else ''
        
        if 'label' in row:
            item['label'] = row['label']
        else:
            item['label'] = np.nan
            
        data.append(item)
    
    return data

def get_train():
    train = load_csv('../data/raw/train.tsv')
    
    return (parse_data(train))

def get_test():
    test = load_csv('../data/raw/test.tsv')
    
    return (parse_data(test))



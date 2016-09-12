import pandas as pd
import os
import sys

basepath = os.path.expanduser('~/Desktop/src/Stumbleupon_classification_challenge/')
sys.path.append(os.path.join(basepath, 'src'))


def load_dataset():
	train = pd.read_csv(os.path.join(basepath, 'data/raw/train.tsv'), delimiter='\t')
	test = pd.read_csv(os.path.join(basepath, 'data/raw/test.tsv'), delimiter='\t')
	sample_sub = pd.read_csv(os.path.join(basepath, 'data/raw/sampleSubmission.csv'))

	return train, test, sample_sub


def fetch_urlid(data):
    return data['urlid']

def delete_urlid(data):
    del data['urlid']

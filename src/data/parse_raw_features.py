import os, sys
import re

from sklearn.externals import joblib

from bs4 import BeautifulSoup
from collections import defaultdict

basepath = os.path.expanduser('~/Desktop/src/Stumbleupon_classification_challenge/')
sys.path.append(os.path.join(basepath, 'src'))


from data import load_datasets


class Parse():
	TAGS = ['h1', 'h2', 'h3', 'h4', 'span',\
			'a', 'label_', 'meta-title', 'meta-description','li']
	
	@staticmethod
	def read_html(urlid):
		with open(os.path.join(basepath, 'data/raw/raw_content/'+str(urlid)), 'r', encoding='utf-8', errors='ignore') as infile:
			html = infile.read()
			infile.close()
		return html
	
	@staticmethod
	def parse_html(html):
		return BeautifulSoup(html, 'lxml')
	
	@staticmethod
	def remove_tags(html, tags):
		for tag in tags:
			for el in html.find_all(tag):
				el.extract()

		return html
 
	@staticmethod
	def tag_content(html, tag):
		def process(s):
			s = s.lower()
			s = s.strip()
			s = re.sub(r'[^a-z0-9]+', ' ', s)
			return s

		tags_component = tag.split('-')
		attrs = {}
		
		if len(tags_component) > 1:
			tag_name = tags_component[0]
			attrs['name'] = tags_component[1]
		else:
			tag_name = tags_component[0]
		
		for el in html.find_all(tag_name, attrs):
			if len(attrs.keys()) > 0:    
				return process(el.get('content', ''))
			else:
				return process(el.text) if el.text else ''        
		return '' # could not find the tag
		
	def __init__(self, key='urlid'):
		self.key = key
	
	def fit(self, X, y=None):
		return self
	
	def transform(self, df):
		urlids = df[self.key]
		tags_content_dict = defaultdict(list)
		
		for urlid in urlids.values:
			html = self.read_html(urlid)
			html = self.parse_html(html)
			html = self.remove_tags(html, ['style', 'script'])
			
			for tag in self.TAGS:
				tags_content_dict[tag].append(self.tag_content(html, tag))
		
		for tag in self.TAGS:
			df[tag] = tags_content_dict[tag]
		
		return df


def main():
	try:
		# load pickle from the disk
		train = joblib.load(os.path.join(basepath, 'data/processed/train_raw_content.pkl'))
		test = joblib.load(os.path.join(basepath, 'data/processed/test_raw_content.pkl'))
		
		return train, test
	except:
		# parse raw content
		train, test, sample_sub = load_datasets.load_dataset()

		parse_train = Parse()
		train = parse_train.transform(train)

		parse_test = Parse()
		test = parse_test.transform(test)

		# dump the parsed data in the processed folder

		joblib.dump(train, os.path.join(basepath, 'data/processed/train_raw_content.pkl'))
		joblib.dump(test, os.path.join(basepath, 'data/processed/test_raw_content.pkl'))
	 	
	 	return train, test
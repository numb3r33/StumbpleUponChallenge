import numpy as np
import pandas as pd
import os, sys
import re, json

import warnings
warnings.filterwarnings('ignore')

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.decomposition import TruncatedSVD
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import f_classif, chi2, SelectKBest
from sklearn.metrics import roc_auc_score
from sklearn.externals import joblib

from nltk import word_tokenize
from nltk.stem.snowball import SnowballStemmer


from bs4 import BeautifulSoup
from collections import defaultdict

basepath = os.path.expanduser('~/Desktop/src/Stumbleupon_classification_challenge/')
sys.path.append(os.path.join(basepath, 'src'))

np.random.seed(2)

from data import parse_raw_features
from models import train_test_split, cross_val_scheme
from helpers import util

# intialize Porter Stemmer


# add some custom stopwords to the list of stopwords 
custom_stopwords = ['i', 'http', 'www']
ENGLISH_STOP_WORDS = set(ENGLISH_STOP_WORDS) | set(custom_stopwords)

def stem_tokens(x):
	return ' '.join([sns.stem(word) for word in word_tokenize(x)])

def preprocess_string(s):
	return stem_tokens(s)

class Weights(BaseEstimator, TransformerMixin):
	def __init__(self, weight):
		self.weight = weight
	
	def fit(self, X, y=None):
		return self
	
	def transform(self, X):
		return self.weight * X


def create_pipeline():
	strip_non_words = FunctionTransformer(remove_non_alphanumeric, validate=False)

	pipeline = Pipeline([
			('strip', strip_non_words),
			('union', FeatureUnion([
					('h1_', Pipeline([
						('var', VarSelect(keys='h1')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50))
					])),
					('h2_', Pipeline([
						('var', VarSelect(keys='h2')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50))
					])),
					('h3_', Pipeline([
						('var', VarSelect(keys='h3')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50))
					])),
					('h4_', Pipeline([
						('var', VarSelect(keys='h4')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50))
					])),
					('meta_title', Pipeline([
						('var', VarSelect(keys='meta-title')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50)),
						('weight', Weights(weight=5))
					])),
					('meta_description', Pipeline([
						('var', VarSelect(keys='meta-description')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50)),
						('weight', Weights(weight=3))
					])),
					('span_', Pipeline([
						('var', VarSelect(keys='span')),
						('tfidf', TfidfVectorizer(min_df=2, ngram_range=(1, 2), tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50))
					])),
					('lsa_body', Pipeline([
						('var', VarSelect(keys='body')),
						('tfidf', TfidfVectorizer(min_df=2, ngram_range=(1, 2), tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS, preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=100)),
						('weight', Weights(weight=20))
					])),
					('lsa_title', Pipeline([
						('var', VarSelect(keys='title')),
						('tfidf', TfidfVectorizer(ngram_range=(1, 2), min_df=2, tokenizer=LemmaTokenizer(), stop_words=ENGLISH_STOP_WORDS,preprocessor=preprocess_string, strip_accents='unicode', norm='l2', sublinear_tf=True)),
						('svd', TruncatedSVD(n_components=50)),
						('weight', Weights(weight=5))
					])),
				])),
			('scale', MinMaxScaler()),
			('feat', SelectKBest(chi2, k=100)),
			('model', LogisticRegression())
		])
	return pipeline

def fit_model(X, y):
	pipeline = create_pipeline()
	pipeline.fit(X, y)

	return pipeline

def train_model():
	train, test = parse_raw_features()
	try:
		pipeline = joblib.load(os.path.join(basepath, 'data/processed/pipeline_raw/model_raw.pkl'))
		return pipeline
	except:

		feature_df = train[train.columns[26:]]
		feature_df['label'] = train.label

		features = list(train.columns[27:])

		X = feature_df[features]
		y = feature_df.label

		pipeline = fit_model(X, y)

		# store this model on the disk
		joblib.dump(pipeline, os.path.join(basepath, 'data/processed/pipeline_raw/model_raw.pkl'))

		return pipeline
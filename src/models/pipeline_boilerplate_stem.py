import numpy as np
import os, sys
import re, json

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import FunctionTransformer
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2, SelectKBest
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import KFold


from nltk.stem.snowball import SnowballStemmer
from nltk import word_tokenize

basepath = os.path.expanduser('~/Desktop/src/Stumbleupon_classification_challenge/')
sys.path.append(os.path.join(basepath, 'src'))

np.random.seed(4)

from data import load_datasets
from helper import util

sns = SnowballStemmer(language='english')

def create_pipeline():
	strip_non_words = FunctionTransformer(util.remove_non_alphanumeric, validate=False)

	# Lemma Tokenizer

	pipeline_lemma = Pipeline([
		('strip', strip_non_words),
		('union', FeatureUnion([
			('body', Pipeline([
				('var', util.VarSelect(keys='body_bp')),
				('tfidf', TfidfVectorizer(strip_accents='unicode', tokenizer=util.LemmaTokenizer(),
										 ngram_range=(1, 2), min_df=3, sublinear_tf=True)),
				('svd', TruncatedSVD(n_components=100))
			])),
			('title', Pipeline([
				('var', util.VarSelect(keys='title_bp')),
				('tfidf', TfidfVectorizer(strip_accents='unicode', tokenizer=util.LemmaTokenizer(),
										 ngram_range=(1, 2), min_df=3, sublinear_tf=True)),
				('svd', TruncatedSVD(n_components=100))
			])),
			('url', Pipeline([
				('var', util.VarSelect(keys='url_component')),
				('tfidf', TfidfVectorizer(strip_accents='unicode', tokenizer=util.LemmaTokenizer(),
										 ngram_range=(1,2), min_df=3, sublinear_tf=True)),
				('svd', TruncatedSVD(n_components=50))
			]))
		])),
		('scaler', MinMaxScaler()),
		('selection', SelectKBest(chi2, k=100)),
		('model', LogisticRegression())
	])

	return pipeline

def fit_model(X, y):
	pipeline = create_pipeline()
	pipeline.fit(X, y)

	return pipeline

def train_model():

	try:
		pipeline = joblib.load(os.path.join(basepath, 'data/processed/pipeline_boilerplate_stem/model_stem.pkl'))
		return pipeline
	except:
		train, test, sample_sub = load_datasets.load_dataset()

		train['boilerplate'] = util.convert_to_json(train.boilerplate)
		train['body_bp'] = util.get_component(train.boilerplate, 'body')
		train['title_bp'] = util.get_component(train.boilerplate, 'title')
		train['url_component'] = util.get_component(train.boilerplate, 'url')
		
		features = ['body_bp', 'title_bp', 'url_component']

		X = train[features]
		y = train.label

		pipeline = fit_model(train, test)

		joblib.dump(pipeline, os.path.join(basepath, 'data/processed/pipeline_boilerplate_stem/model_stem.pkl'))
		return pipeline
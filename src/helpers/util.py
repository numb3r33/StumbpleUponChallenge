import json

from sklearn.preprocessing import LabelEncoder
from sklearn.base import BaseEstimator, TransformerMixin

from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer
from nltk import word_tokenize



sns = SnowballStemmer(language='english')
por = PorterStemmer()


def encode_variable(train, test):
    """
    Convert categorical variable to numerical form
    
    train: Values of the variable in the training set
    test: Values of the variable  in the test set
    
    """
    
    data = pd.concat((train, test), axis=0)
    
    lbl = LabelEncoder()
    lbl.fit(data)
    
    train_ = lbl.transform(train)
    test_ = lbl.transform(test)
    
    return train_, test_


def store(filename, data):
    """
    Pickle data onto disk
    
    filename: filename that you want to give to this dump
    data: actual data that you want to dump.
    """
    
    import pickle
    
    with open(os.path.join(basepath, 'data/processed/') + filename, 'wb') as outfile:
        pickle.dump(data, outfile, protocol=pickle.HIGHEST_PROTOCOL)
        outfile.close()
        
def load(filename):
    """
    Load data from disk
    
    filename: filename of the pickled data that you want to load
    """
    
    import pickle
    
    with open(os.path.join(basepath, 'data/processed/') + filename, 'rb') as infile:
        data = pickle.load(infile)
        infile.close()
        
        return data


class LemmaTokenizer(object):
    def __init__(self):
        self.wnl = WordNetLemmatizer()
    
    def __call__(self, doc):
        return [self.wnl.lemmatize(t) for t in word_tokenize(doc)]

class StemTokenizer(object):
    def __init__(self):
        self.sns = sns
    
    def __call__(self, doc):
        return [self.sns.stem(t) for t in word_tokenize(doc)]


class VarSelect(BaseEstimator, TransformerMixin):
    def __init__(self, keys):
        self.keys = keys
        
    def fit(self, X, y=None):
        return self
    
    def transform(self, df):
        return df[self.keys]

def remove_non_alphanumeric(df):
    return df.replace(r'[^A-Za-z0-9]+', ' ', regex=True)


def convert_to_json(boilerplate):
    return list(map(json.loads, boilerplate))

def get_component(boilerplate, key):
    """
    Get value for a particular key in boilerplate json,
    if present return the value else return an empty string
    
    boilerplate: list of boilerplate text in json format
    key: key for which we want to fetch value e.g. body, title and url
    """
    
    return np.array([bp[key] if key in bp and bp[key] else u'' for bp in boilerplate])  


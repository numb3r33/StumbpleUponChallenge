from urllib.parse import urlparse
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS

from nltk.stem.snowball import SnowballStemmer
from nltk.stem.porter import PorterStemmer

sn_stem = SnowballStemmer(language='english')
p_stem = PorterStemmer()

def url_depth(url):
    """
    Takes in a url and calculates depth
    e.g. www.guardian.co.uk/a has depth 1, whereas www.guardian.co.uk/a/b has depth 2
    
    url - url of the webpage
    """
    
    parsed_url = urlparse(url)
    path = parsed_url.path

    return len(list(filter(lambda x: len(x)> 0, path.split('/'))))


def extract_top_level_domain(url):
    """
    Extracts top level domain from a given url
    
    url: Url of the webpage in the dataset
    """
    parsed_url = urlparse(url)
    top_level = parsed_url[1].split('.')[-1]
    
    return top_level



def convert_to_json(text):
    return json.loads(text)

def extract_body(json_):
    return json_['body'].lower() if json_['body'] else u''

def remove_stopwords(text):
    return ' '.join([word for word in text.split(' ') if word not in ENGLISH_STOP_WORDS])


def stem_words(sentence, stemmer):
    return ' '.join([stemmer.stem(word) for word in sentence.split(' ')])

def stemming(sentences, stemmer):
    return [stem_words(sentence, stemmer) for sentence in sentences]

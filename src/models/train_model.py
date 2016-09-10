import numpy as np

from sklearn.cross_validation import KFold
from .predict_model import predict

import gensim

def get_scores(data, labels):
    
    scores = []

    for train_idx, test_idx in KFold(len(labels), 10):
        score = predict(data[train_idx], labels[train_idx], data[test_idx])
        scores.append(score)

    score = predict(data[:len(labels)], labels, data[len(labels):])
    scores.append(score)

    return np.hstack(scores)


def get_lda(name, n):
    data = get_featureset(name, tf_idf=False, norm=None, stem=False,
                          stopwords=True)

    corpus = gensim.matutils.Scipy2Corpus(data)
    lda = LdaModel(corpus, num_topics=n)
    data = gensim.matutils.corpus2csc(lda[corpus]).T

    return data

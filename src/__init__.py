import numpy as np

from data import make_dataset, DATASETS
from features import parse_raw_content, count_words
from features import feature_sets as fs
from models import train_model
from sklearn.decomposition import TruncatedSVD as SVD

def save(filename, data):
    import pickle
    with open('../data/processed/'+filename, 'wb') as outfile:
        pickle.dump(data, outfile, pickle.HIGHEST_PROTOCOL)
        outfile.close()
        
def preprocess_and_train(labels):
    scores = {}
    
    PREPROCESSING = {
        'raw': lambda: fs.get_featureset(dataset, tf_idf=False),
        'tfidf': lambda: fs.get_featureset(dataset),
        'nostem': lambda: fs.get_featureset(dataset, stem=False),
        'svd50': lambda: SVD(50).fit_transform(fs.get_featureset(dataset)),
        'svd100': lambda: SVD(100).fit_transform(fs.get_featureset(dataset)),
        'lda': lambda: train_model.get_lda(dataset, 100),
    }
    
    for dataset in DATASETS.DATASETS:
        for method in PREPROCESSING:
            # name of feature set
            name = method + ':' + dataset

            # check if we calulated this score before
            if name in scores:
                continue

            # we can only do iton some datasets
            if method == 'lda':
                if 'dataset' not in DATASETS.LDA_DATASETS:
                    continue

            print(name)

            # get the data
            data = PREPROCESSING[method]()

            # train model
            scores[name] = train_model.get_scores(data, labels)

            # save it
            save('scores', scores)

def main(dataset=False):
    train = make_dataset.get_train()
    test = make_dataset.get_test()
    labels = np.array([item['label'] for item in train])
    
    
    if dataset:
        parse_raw_content.main(train, test)
        count_words.main()
    
    preprocess_and_train(labels)

if __name__ == '__main__':
    main()


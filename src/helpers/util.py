from sklearn.preprocessing import LabelEncoder

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
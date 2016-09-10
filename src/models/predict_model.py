from sklearn.linear_model import LogisticRegression

def predict(train, labels, test):
    model = LogisticRegression()
    model.fit(train, labels)

    return model.predict_proba(test)[:, -1]

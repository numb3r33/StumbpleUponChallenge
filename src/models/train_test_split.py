from sklearn.cross_validation import train_test_split

def tr_ts_split(X, y, **params):
	X_train, X_test, y_train, y_test = train_test_split(X, y, **params)
	return (X_train, X_test, y_train, y_test)
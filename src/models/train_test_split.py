from sklearn.cross_validation import train_test_split

def tr_ts_split(train_size, **params):
	itrain, itest = train_test_split(range(train_size),**params)
	return (itrain, itest)
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.metrics import roc_auc_score

def cv_scheme(est, X_train, y_train, is_news, **params):
	cv = StratifiedKFold(is_news, **params)

	scores = []

	for itrain, itest in cv:
		Xtr = X_train.iloc[itrain]
		ytr = y_train.iloc[itrain]
		
		Xts = X_train.iloc[itest]
		yts = y_train.iloc[itest]
		
		est.fit(Xtr, ytr)
		
		y_pred = est.predict_proba(Xts)[:, 1]
		
		scores.append(roc_auc_score(yts, y_pred))

	scores = np.array(scores)
	mean_scores = scores.mean()
	std_scores = scores.std()

	return (scores, mean_scores, std_scores)
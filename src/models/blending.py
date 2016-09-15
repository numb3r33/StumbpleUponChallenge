import numpy as np

from sklearn.cross_validation import KFold
from sklear.linear_model import LogisticRegression

class Blending(object):
	def __init__(self, models):
		self.models = models # dict
		
	def predict(self, X, X_test, y=None):
		cv = KFold(len(X), n_folds=3, shuffle=True, random_state=10)
		
		dataset_blend_train = np.zeros((X.shape[0], len(self.models.keys())))
		dataset_blend_test = np.zeros((X_test.shape[0], len(self.models.keys())))
		
		for index, key in enumerate(self.models.keys()):
			dataset_blend_test_index = np.zeros((X_test.shape[0], len(cv)))
			
			model = self.models[key][1]
			feature_list = self.models[key][0]
			
			print('Training model of type: ', key)
			
			for i , (itrain, itest) in enumerate(cv):
				Xtr = X.iloc[itrain][feature_list]
				ytr = y.iloc[itrain]

				Xte = X.iloc[itest][feature_list]
				yte = y.iloc[itest]

				y_preds = model.predict_proba(Xte)[:, 1]
				
				dataset_blend_train[itest, index] = y_preds
				dataset_blend_test_index[:, i] = model.predict_proba(X_test)[:, 1]
				
			dataset_blend_test[:, index] = dataset_blend_test_index.mean(1)
			 
		print('\nBlending')
		clf = LogisticRegression()
		clf.fit(dataset_blend_train, y)
		
		y_submission = clf.predict_proba(dataset_blend_test)[:, 1]
		y_submission = (y_submission - y_submission.min()) / (y_submission.max() - y_submission.min())
		
		return y_submission
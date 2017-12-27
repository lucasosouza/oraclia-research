import datetime
import pandas as pd
import numpy as np
from collections import defaultdict

from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import StratifiedShuffleSplit

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

class Backtester():

	def __init__(self, df):
		self.df = df

	def create_labels(self, forward=10, profit_margin=.05, stop_loss=.05):
	    
	    for row in range(self.df.shape[0]-forward):

	        # initialize max and min ticks
	        max_uptick = 0
	        min_downtick = 0 

	        # move all days forward
	        for i in range(1,forward+1):
	            delta = (self.df.ix[row+i, 'Adj Close'] / self.df.ix[row, 'Adj Close'])-1
	            if delta > max_uptick:
	                max_uptick = delta
	            if delta < min_downtick:
	                min_downtick = delta

	        # evaluate ticks against predefined strategy parameters
	        if max_uptick >= profit_margin and min_downtick <= -stop_loss:
	            self.df.ix[row,'Label'] = 1
	        else:
	            self.df.ix[row,'Label'] = 0        

	    self.df.dropna(inplace=True)

	def prep_data(self):
		features = [x for x in self.df.columns if x != "Label"]
		X = self.df[features].values
		y = self.df['Label'].values
		return X,y

	def score(self, X, y):
		clf = GBC(random_state=42)
		cv = StratifiedShuffleSplit(n_splits=10, test_size=.1, random_state=42)
		scores = cross_val_score(clf, X, y, cv=cv, scoring='precision')
		return (scores.mean() - scores.std())
	
	def evaluate(self, forward, profit_margin, stop_loss):
		self.create_labels(forward=forward, profit_margin=profit_margin, stop_loss=stop_loss)		
		score = self.score(*self.prep_data())
		print("span: {}, profit_margin: {:.3f}, stop_loss: {:.3f} --  score: {:.3f}".format(
			forward, profit_margin, stop_loss, score))
		return score

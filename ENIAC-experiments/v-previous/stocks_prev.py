import datetime
import pandas_datareader.data as web
import pandas as pd
import numpy as np
from collections import defaultdict

from sklearn.ensemble import GradientBoostingClassifier as GBC
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


def download_stock_data():
	start_date = datetime.datetime(2012,1,1)
	end_date = datetime.datetime(2016,8,31) 
	symbol = "PETR4.SA"
	return web.DataReader(symbol, 'yahoo', start_date, end_date)

def create_new_variables(df):
	df['Delta'] = (df['Adj Close'] / df['Adj Close'].shift(1))-1
	df['Signal'] = df['Delta']>0
	return df.dropna()

def backward_filling(df, backward=30): 
	backward = 30
	for column in ['Delta', 'Volume']:
	    for i in range(1,backward+1):
	        new_column = "{} -d{}".format(column, i)
	        for row in range(backward, df.shape[0]):
	            df.ix[row, new_column] = df.ix[row-i, column]
	return df.dropna()

class Backtester():

	def __init__(self):
		self.df = download_stock_data()
		self.df = create_new_variables(self.df)
		self.df = backward_filling(self.df, backward=30)

	def forward_filling(self, forward=10, profit_margin=.05, stop_loss=.05):
		for row in range(self.ldf.shape[0]-forward):
		    # initialize max and min ticks
		    max_uptick = 0
		    min_downtick = 0 
		    
		    for i in range(1,forward+1):
		        delta = (self.ldf.ix[row+i, 'Adj Close'] / self.ldf.ix[row, 'Adj Close'])-1
		        if delta > max_uptick:
		            max_uptick = delta
		        if delta < min_downtick:
		            min_downtick = delta
		        	    
		    # evaluate ticks against predefined strategy parameters
		    if max_uptick >= profit_margin and min_downtick <= -stop_loss:
		        self.ldf.ix[row,'Label'] = 1
		    else:
		        self.ldf.ix[row,'Label'] = 0        

		self.ldf = self.ldf.dropna()

	def prep_data(self):
		X = self.ldf.drop('Label', axis=1)
		y = self.ldf['Label']
		return train_test_split(X, y, test_size=0.3, stratify=y)

	def score(self, X_train, X_test, y_train, y_test):
		clf = GBC().fit(X_train, y_train)
		return precision_score(y_test, clf.predict(X_test))

	def evaluate(self, forward, profit_margin, stop_loss):
		self.ldf = self.df.copy(deep=True)
		self.forward_filling(forward=forward, profit_margin=profit_margin, stop_loss=stop_loss)
		score = self.score(*self.prep_data())
		print "span: {}, profit_margin: {:.3f}, stop_loss: {:.3f} --  score: {:.3f}".format(
			forward, profit_margin, stop_loss, score)
		return score


# coding: utf-8

# ## Loading up required libraries and configurations

# In[1]:

import quandl
import pandas_datareader.data as web
import datetime
import pandas as pd
import numpy as np
from collections import defaultdict
from IPython.display import display
import scipy as sp
from operator import methodcaller
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pickle

import data_transform
import simulator

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score
from sklearn.neighbors import KNeighborsClassifier as kNN
from sklearn.decomposition import PCA


""""
usage of this API key is monitored
don't use this key for any other work, neither make it available on the web by any means
if you would like to access the same API for a different project,
create an account in quandl.com (it is free) and generate your own API key
""" 
quandl.ApiConfig.api_key = "1513txcURR4fYyP5VDU3"


# Set basic parameters
start_date_train='1992-1-1'
end_date_train='2014-12-31'
start_date_test = '2015-01-02'
end_date_test='2016-10-28'

# Set iterative parameters
# different profit per day .9%, 2%, 4%
strategies = {
    'Conservative': (10, .09)
}

# Set stocks to be used in experiment
# stocks = ['ITUB4', 'BBDC4', 'ABEV3', 'PETR4', 'VALE5', 'VALE3', 'BBAS3', 'PETR3', 
#          'BVMF3', 'ITSA4', 'BRFS3', 'UGPA3', 'CIEL3', 'KROT3', 'BBSE3', 'CCRO3']
# stocks = ['PETR4', 'VALE5']
stocks = ['ITUB4', 'BBDC4', 'ABEV3', 'PETR4', 'VALE5']

# create indices
indices = []
for strategy in strategies.keys():
    for symbol in stocks:
        indices.append((strategy, symbol))

# iterate
# results = pd.DataFrame(index=pd.MultiIndex.from_tuples(indices))
results = pd.DataFrame(index=pd.MultiIndex.from_tuples(indices), columns=['CV_Precision_Mean', 'CV_Precision_CI', 
    'CV_Success%', 'Test_Precision', 'Test_Success%', 'Profits'])

# Download basic data
try: 
    with open('market_data.p', 'rb') as f:
        market_df = pickle.load(f)
except:
    market_df = data_transform.download_market_data(start_date=start_date_train, end_date=end_date_test)
    with open('market_data.p', 'wb') as f:
        pickle.dump(market_df, f)


for strategy, (span, profit) in strategies.items():
    # initialize data structures
    data = {}
    test_data = {}
    analysts=[]

    # train classifiers
    for symbol in stocks:

        ##### Get Data ##################################

        # try to load existing data, else import it
        try:
            # load
            with open(strategy + '_' + symbol + '_train.p', 'rb') as f:
                data = pickle.load(f)
        except:
            # create
            print('Downloading training data for {}'.format(symbol))
            data[symbol + '_X'], data[symbol + '_y'], column_names = \
                data_transform.gen_data(symbol, market_df, start_date_train, end_date_train, span=span, profit=profit)
            # save for reuse
            with open(strategy + '_' + symbol + '_train.p', 'wb') as f:
                pickle.dump(data, f)

        # try to load existing test data, else import it
        try:
            # load
            with open(strategy + '_' + symbol + '_test.p', 'rb') as f:
                test_data = pickle.load(f)
        except:
            # create
            print('Downloading testing data for {}'.format(symbol))
            test_data[symbol + '_X'], test_data[symbol + '_y'], test_column_names = \
                data_transform.gen_data(symbol, market_df, start_date_test, end_date_test, span=span, profit=profit)
            # save for reuse
            with open(strategy + '_' + symbol + '_test.p', 'wb') as f:
                pickle.dump(test_data, f)

        # define X and y training and testing sets
        X, y = data[symbol + '_X'], data[symbol + '_y']
        X_test, y_test = test_data[symbol + '_X'], test_data[symbol + '_y']


        ##### Training ##################################

        # scale
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        data[symbol + '_scaler'] = scaler

        # predict
        pca = PCA(n_components=10, random_state=42)
        X = pca.fit_transform(X)

        clf = kNN()
        clf.fit(X, y)
        data[symbol + '_pca'] = pca
        data[symbol + '_clf'] = clf

        ##### Cross Validating ##################################

        # validate
        cv = StratifiedShuffleSplit(n_splits=10, test_size=.1, random_state=42)
        scores = cross_val_score(clf, X, y, cv=cv, scoring='precision')

        # save results
        row = (strategy, symbol)
        try:
            results.loc[row, 'CV_Success%'] = np.bincount(y)[1] / len(y) 
            results.loc[row, 'CV_Precision_Mean'] = scores.mean()
            results.loc[row, 'CV_Precision_CI'] = scores.std()*2
        except:
            pass
        print("CV Precision for {}, {}: {:0.2f} (+/- {:0.2f})".format(strategy, symbol, scores.mean(), scores.std() * 2))

        ##### Testing ##################################

        # scale
        X_test = data[symbol + '_scaler'].transform(X_test)

        # predict
        X_test = data[symbol + '_pca'].transform(X_test)
        y_pred = data[symbol + '_clf'].predict(X_test)
        
        # evaluate
        precision = precision_score(y_test, y_pred)

        # save results
        try: 
            results.loc[row, 'Test_Success%'] = np.bincount(y_test)[1] / len(y_test) 
            results.loc[row, 'Test_Precision'] = precision
        except:
            pass
        print("Test Precision for {}, {}: {:0.2f}".format(strategy, symbol, precision))

        ##### Creat analysts ##################################

        # create analysts
        backtest_data = data_transform.prep_backtest_data(symbol, market_df, '2014-6-30', end_date_test, base=60)
        analysts.append(simulator.Analyst(symbol, backtest_data, clf, scaler, pca, scores.mean() - (2 * scores.std()) ) )

##### Simulate ##################################

# create operator
trading_days = list(data_transform.get_stock_data('PETR4', start_date_test, end_date_test).index)
span = 10
profit = .09

for loss in np.arange(-0.04,-0.14,-0.001):

    # loss = loss
    scores = []
    for idx in range(5):
        op = simulator.Operator((span, profit, loss), analysts, capital=100000, 
                                start_date=start_date_test, end_date=end_date_test, op_days=trading_days)
        op.run()
        scores.append(op.capital / 100000.0 - 1)

    avg_score = sum(scores)/len(scores)
    print("Span: {}, Profit: {:.2f}, Loss: {:.2f}, Return: {:.2f}".format(
            span,profit,loss, avg_score))

# save results
# results.to_pickle('experiment_results.p')

# coding: utf-8
# Using a neural network to predict stock prices, using only basic data

from sklearn import neural_network
from matplotlib import pyplot as plt
import datetime
import pandas_datareader.data as web
import pandas as pd
import numpy as np

def import_data():
    start_date = datetime.datetime(2016,1,1)
    end_date = datetime.datetime(2016,6,20) 
    symbol = "PETR4.SA"
    df = web.DataReader(symbol, 'yahoo', start_date, end_date)
    return df

# separate X and y
def get_xy(lag=0):
    X = df[df.columns - ['Adj Close']][lag:]
    y = df['Adj Close'].shift(lag)[lag:].reindex(X.index)
    #normalize X
    X = (X - X.min()) / (X.max() - X.min())
    return X, y

# separate training and testing data
def split(array, n):
    return array[:n], array[n:]

def train_test_data(X,y, test_percent=.3):
    length = int(X.shape[0] * (1-test_percent))
    X_train, X_test = split(X,length)
    y_train, y_test = split(y,length)
    return X_train, y_train, X_test, y_test

def predict(X,y):
    X_train, y_train, X_test, y_test = train_test_data(X,y, test_percent=.2)
    reg = neural_network.MLPRegressor()
    reg.fit(X_train, y_train)
    y_pred = reg.predict(X_test)
    return y, y_train, y_pred

def plot(y, y_train, y_pred, i=99):
    y_pred_full = list(y_train) + list(y_pred)
    y_pred_full= pd.Series(y_pred_full, index=y.index)
    ax = y[:80].plot()
    y_pred_full[:80].plot(ax = ax)
    ax.legend(['Actual', 'Predicted'])
    plt.savefig('/Users/lucasosouza/Desktop/oraculo/images/fig' + str(i) + '.png')
    plt.clf()

# ax = y.ix['2016-03-01':'2016-06-10'].plot()
    
#fig, axes = plt.subplots(nrows=5, ncols=1)
#for i in range(1, 8, 2):
df = import_data()
X,y = get_xy(lag=1)
y, y_train, y_pred = predict(X,y)
#ax = axes[i]
plot(y, y_train, y_pred)

# same as regression code
# still not making a lot of sense
# doesn't seem like I can predict very well... forget price
# you were in the right direction
# predict daily return (the movement) instead of price
# but use a regressor instead of a classifier




# Apply classification algorithms to predict future prices
# Try classification and regression methods

import numpy as np
import pandas as pd
import datetime

from sklearn.feature_selection import SelectKBest
from sklearn.linear_model import LinearRegression
from sklearn import svm
from sklearn.metrics import accuracy_score

from pprint import pprint
import matplotlib.pyplot as plt

# start by importing the file
df = pd.read_csv("~/Desktop/oraculo/petr4_feat.csv", index_col="Date",na_values="nan", parse_dates=True)

def get_xy(df, num_days=1):
    X = df[df.columns - ['daily_return']]
    y = df['daily_return'].shift(num_days)
    # normalize features in X
    X = (X - X.min()) / (X.max() - X.min())
    # remove na
    X = X.dropna()
    y = y.dropna()
    # reindex and return
    X,y = X.align(y, join='inner', axis=0)
    return X,y

def evaluate_features(X,y):
    # feature select
    feature_selector = SelectKBest(k=X.shape[1])
    feature_selector.fit(X,y)
    # print scores
    scores = zip(X.columns, feature_selector.scores_)
    sorted(scores, key=lambda x:-x[1])
    # print pvalues
    pvalues=zip(X.columns, feature_selector.pvalues_)
    sorted(pvalues, key=lambda x:x[1])

def regress(X,y):
    # pulling up a regressor
    regressor = LinearRegression()
    regressor.fit(X,y)
    # evaluate coefficients
    #coefficients = zip(X.columns, regressor.coef_)
    #sorted(coefficients, key=lambda x:-x[1])
    # plot # to be implemented
    return regressor

# print('Variance score: %.2f' % regressor.score(X, y))

#okay I start getting some good news with one day ahead, I can get a linear regression model 
# that explains 58% of the variance

# let's push this even further and try up to 5 days ahead, listing the scores

def evaluate_prediction_power(df, num_days=1):
    """"
        Applies a shift to the model for the number of days given, default to 1, and feed the data to
        a linear regression model. Evaluate the results using score and print it.
    """
    scores = {}
    print "Num days: {}".format(range(num_days))
    for i in range(num_days):
        X,y = get_xy(df, num_days=i)
        regressor = learn(X,y)
        scores[i] = regressor.score(X,y)
    return scores

def plot(X, y, regressor):
    ytest = regressor.predict(X)
    plt.plot(y[-100:], color="blue", linewidth=1)
    plt.plot(ytest[-100:], color="red", linewidth=1)
    
""" removed starter code
pprint(evaluate_prediction_power(df,num_days=90))
X, y = get_xy(df)
regressor = regress(X,y)
plot(X,y,regressor)
"""

# regression is a poor predictor 
# I want to use a classifier
# I will have more options to work with
# to do that, I first need to convert my data into a format that a classifier
# I will start with 0 or 1. 0 drops, 1 increases

def convert_to_classes(y):
    """"
        Convert y value into labels that can be used in a classifier
    """
    return y.apply(lambda x: float_to_category(x))

def float_to_category(n):
    """
        Classify return label into 7 classes, possible range of returns:
        n<-5%, -5%<n<-3%, -3%<n<-1%, -1%<n<1%, 1%<n<3%, 3%<n<5%, n>5%
    """
    separators = [-.05, -.03, -.01, .01, .03, .05]
    series = np.zeros(7)
    for idx, sep in enumerate(separators):
        if n < sep: 
            series[idx] = 1
            return series
    series[-1] = 1
    return series

# how to do this?
# first I need to convert this into seven different ys
# input a number - convert it to a Series with 7 columns


def classify(X,y):
    clf = svm.SVC()
    clf.fit(X,y)
    return clf

def split(array, n):
    return array[:n], array[n:]

# separate train and test data - needs to keep order - use 30% for testing
def train_test_data(X,y, test_percent=.3):
    length = int(X.shape[0] * (1-test_percent))
    Xtrain, Xtest = split(X,length)
    ytrain, ytest = split(y,length)
    return Xtrain, ytrain, Xtest, ytest

def learn(df):
    X,y = get_xy(df)
    y = convert_to_classes(y)
    Xtrain, ytrain, Xtest, ytest = train_test_data(X,y)
    clf = classify(Xtrain, ytrain)
    ypred = clf.predict(Xtest)
    print "Accuracy: {:.2%}".format(accuracy_score(ytest, ypred))
    import pdb;pdb.set_trace()

learn(df)

### one vs all classifier test

# what?? there was a lot of code here that just disappeared
# that is probably from Rodeo
# really??? really???









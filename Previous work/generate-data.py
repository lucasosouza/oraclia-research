
# coding: utf-8

# ## Loading up required libraries and configurations

# In[1]:

import quandl
import pandas_datareader.data as web
import datetime
import pandas as pd
import sklearn
import numpy as np
from collections import defaultdict
from IPython.display import display
import scipy as sp
from operator import methodcaller
import time

#set reload
get_ipython().magic('reload_ext autoreload')
get_ipython().magic('autoreload 1')

# evaluate usage
pd.options.mode.chained_assignment = None  # default='warn'


# In[2]:

import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic('matplotlib inline')


# In[3]:

""""
usage of this API key is monitored
don't use this key for any other work, neither make it available on the web by any means
if you would like to access the same API for a different project,
create an account in quandl.com (it is free) and generate your own API key
""" 
quandl.ApiConfig.api_key = "1513txcURR4fYyP5VDU3"


# In[4]:

ibx50 = ['ABEV3','BBAS3','BBDC3','BBDC4','BBSE3','BRFS3','BRKM5','BRML3','BVMF3',
         'CCRO3','CIEL3','CMIG4','CPFE3','CSAN3','CSNA3','CTIP3','EGIE3','EMBR3',
         'ENBR3','EQTL3','ESTC3','FIBR3','GGBR4','GOAU4','HYPE3','ITSA4','ITUB4',
         'JBSS3','KLBN1','KROT3','LAME4','LREN3','MRVE3','MULT3','NATU3','PCAR4',
         'PETR3','PETR4','QUAL3','RADL3','RUMO3','SBSP3','SMLE3','SUZB5','UGPA3',
         'USIM5','VALE3','VALE5','VIVT4','WEGE3']


# ## Generate Dataset

# In[5]:

get_ipython().magic('aimport data_transform')
get_ipython().magic('aimport simulator')


# In[6]:

start_date='1992-1-1'
end_date='2016-12-31'
market_df = data_transform.download_market_data(start_date=start_date, end_date=end_date)


# In[7]:

span = 5 # 10
profit = .05 # .09


# In[8]:

for col in market_df.columns:
    print(col, sum(market_df[col] == 0) / market_df.shape[0])


# In[9]:

market_df['BM&F Gold gramme'][-30:]


# In[10]:

# create analysts
data = {}
# stocks= ['ABEV3', 'BBDC4', 'ITUB4', 'PETR4', 'VALE5'] 
#stocks = ['ITUB4', 'BBDC4', 'ABEV3', 'PETR4', 'VALE5', 'VALE3', 'BBAS3', 'PETR3', 
#          'BVMF3', 'ITSA4', 'BRFS3', 'UGPA3', 'CIEL3', 'KROT3', 'BBSE3', 'CCRO3']
stocks = ['PETR4', 'VALE5']


# represents around 25% of IBOV
analysts = []
start_date='1992-1-1'
end_date_train =  '2014-12-31'
start_date_test = '2015-01-01'
for symbol in stocks:
    data[symbol + '_X'], data[symbol + '_y'], column_names =     data_transform.gen_data(symbol, market_df, start_date, end_date_train, span=span, profit=profit)

# took about 2 minutes to compute in local machine


# In[11]:

# analyze dimensions
data[stocks[0]].shape, data[stocks[0]].shape


# In[12]:

# save dataset
import pickle
with open('data.p', 'wb') as f:
    pickle.dump(data, f)
    
# 257mb file


# ## Validating

# In[13]:

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import StandardScaler

for symbol in stocks:
    # get data
    X, y = data[symbol + '_X'], data[symbol + '_y']

    # scale
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    data[symbol + '_scaler'] = scaler

    # predict
    clf = RandomForestClassifier()
    clf.fit(X, y)
    data[symbol + '_clf'] = clf

    # validate
    cv = StratifiedShuffleSplit(n_splits=10, test_size=.1, random_state=42)
    scores = cross_val_score(clf, X, y, cv=cv, scoring='precision')

    # print results
    print("Precision for {}: {:0.2f} (+/- {:0.2f})".format(symbol, scores.mean(), scores.std() * 2))


# In[14]:

pred = clf.predict(X)
sum(pred) / len(pred), sum(y)/len(y)
# 15% of the cases is true, vs 16% of the second case


# ## Testing

# In[15]:

# what if I try to predict in a set of the data and train in other
# this is what I did 
# now I need to generate data to test
# create analysts
test_data = {}
stocks= ['ABEV3', 'BBDC4', 'ITUB4', 'PETR4', 'VALE5'] # represents around 25% of IBOV
start_date_test = '2015-01-01'
end_date_test =  '2016-12-31'
for symbol in stocks:
    test_data[symbol + '_X'], test_data[symbol + '_y'], test_column_names =     data_transform.gen_data(symbol, market_df, start_date_test, end_date_test, span=span, profit=profit)

# took about 2 minutes to compute in local machine


# In[16]:

from sklearn.metrics import precision_score

# get data
for symbol in stocks:
    X_test, y_test = test_data[symbol + '_X'], test_data[symbol + '_y']

    # scale
    X_test = data[symbol + '_scaler'].transform(X_test)

    # predict
    y_pred = data[symbol + '_clf'].predict(X_test)
    
    # evaluate
    precision = precision_score(y_test, y_pred)

    print("Precision for {}: {:0.2f}".format(symbol, precision))


# That is a ridiculous low precision. Which means I can look into the past, I just can't look into the future. How the hell did I get good results, by sheer luck? 
# 

# In[17]:

# save test_data
import pickle
with open('test_data.p', 'wb') as f:
    pickle.dump(test_data, f)



# In[ ]:




# features_generator.py

import pandas as pd 
import pandas.io.data as web
import datetime
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


# First: import the data you need using pandas web module

# How long do I go back to ?
# I will use data from the last 6 years, which represent more or less the same state we are in today

# start_date = datetime.datetime(2010,1,1)
# end_date = datetime.datetime(2016,6,20) 
# symbol = "PETR4.SA"
# df = web.DataReader(symbol, 'yahoo', start_date, end_date)

# Pick 5 technical indicators that I will feed into my classification algorithm at the first moment
# try not to use features that are 100% correlated, such as price * 2 . It makes no sense

# df['Adj Close'].plot()
# df.to_csv("~/Desktop/oraculo/petr4.csv")
df = pd.read_csv("~/Desktop/oraculo/petr4.csv", index_col="Date",na_values="nan", parse_dates=True)
# Standard moving average (rolling mean)

df['sma10'] = df['Adj Close'].rolling(window=10, center=False).mean()
df['sma50'] = df['Adj Close'].rolling(window=50, center=False).mean()

# Bollinger Bands (based on rolling std)

## calculate rolling std
std10 = df['Adj Close'].rolling(window=10, center=False).std()
std20 = df['Adj Close'].rolling(window=20, center=False).std()

## calculate bollinger band - using 2 std
df['bb10_lower'] = df['sma10'] - 2 * std10
df['bb10_upper'] = df['sma10'] + 2 * std10


df['bb20_lower'] = df['sma20'] - 2 * std20
df['bb20_upper'] = df['sma20'] + 2 * std20

## plot and visualize

fields = ['Adj Close','bb20_lower', 'bb20_upper']
df.ix['2015-01-01':'2016-03-30'][fields].plot()
plt.savefig('/Users/lucasosouza/Desktop/oraculo/images/bbfig.png')

fields = ['Adj Close','sma10', 'sma50']
df.ix['2015-01-01':'2016-03-30'][fields].plot()
plt.savefig('/Users/lucasosouza/Desktop/oraculo/images/smafig.png')


# Volume / Price

df['volume_price'] = df['Volume'] / df['Adj Close']

# Daily Returns
## is given by today price less yesterday price minus one

df['daily_return'] = (df['Adj Close'] / df['Adj Close'].shift(1)) - 1
df.ix['2015-01-01':'2016-03-30']['daily_return'].plot()
plt.savefig('/Users/lucasosouza/Desktop/oraculo/images/bbfig.png')

# Momentum 
# using a 5 and 10 day momentum
# equals a daily return like, but looking a few days earlier

df['momentum5'] = (df['Adj Close'] / df['Adj Close'].shift(5))
df['momentum10'] = (df['Adj Close'] / df['Adj Close'].shift(10))

### other technical indicators that could be applied here??
# try to implement candlestick
# and elliot wave
# these two will add more to the work, since they are generally considered to be
# good technical indicators amongst the community

# Candlestick



# Elliot Wave



# feature_columns = ['sma10', 'sma20', 'bb10_lower', 'bb10_upper', 'bb20_lower', 
# 'bb20_upper', 'volume_price', 'daily_return', 'momentum5', 'momentum10']

# Export to use as input for a machine learning algorithm

df.to_csv("~/Desktop/oraculo/petr4_feat.csv")
# y is Adj Close
# remaining are features

# doing the matrix
cols = ['Adj', 'Volume']
cm = np.corrcoef(df[cols].values.T)
cm
# sns.set(style='whitegrid', context='notebook')
#sns.set(font_scale=1.5)
#hm = sns.heatmap(cm, cbar=True, annot=True, square=True, fmt='.2f',
#                annot_kws = {'size':15}, yticklabels=cols, xticklabels=cols)
#plt.show()

df['daily_return'].plt()


# This scrapper can be replaced by a function already available in pandas library, at: pandas.io
# usage: 
# start = datetime.datetime(2010, 1, 1)
# end = datetime.datetime(2013, 1, 27)
# df = web.DataReader("PETR4.SA", 'yahoo', start, end)

# Attempt 1 
# Scrapping data from the Bovespa website on brazilian stocks

import pandas as pd

# constants
BASE_URL = "http://real-chart.finance.yahoo.com/table.csv?s="

# functions
def break_date(date):
	# date format expected: 2016-03-01
	year = int(date[:4])
	month = int(date[5:7])-1
	day =  int(date[8:10])
	return year, month, day

def start_date_to_url(date):
	# example: &a=0&b=3&c=2000
	year, month, day = break_date(date)
	return "&a=" + str(day) + "&b=" + str(month) + "&c=" + str(year)

def end_date_to_url(date):
	# example: &d=5&e=19&f=2016
	year, month, day = break_date(date)
	return "&d=" + str(day) + "&e=" + str(month) + "&f=" + str(year)

def compose_yahoo_url(symbol, start_date, end_date):
	# example: http://real-chart.finance.yahoo.com/table.csv?s=PETR4.SA&d=5&e=19&f=2016&a=0&b=3&c=2000&ignore=.csv
	# removed &g=d
	url = BASE_URL + symbol + ".SA" + end_date_to_url(end_date) + start_date_to_url(start_date) + "&ignore=.csv"
	return url

def retrieve_stock_data(symbol, start_date, end_date):
	data_source = compose_yahoo_url(symbol, start_date, end_date)
	data_csv = req.get(data_source)
	# df = pd.read_csv(data_csv.text, index_col="Date", usecols=["Date", "Adj Close"], na_values="nan", parse_dates = True)
	# print "Df size is: {}".format(df.shape)
	import pdb;pdb.set_trace()
	# df = df.rename(columns={"Adj Close": symbol})

# parameters
symbols = []
symbol="PETR4"
start_date="2016-01-01"
end_date="2016-03-30"

if __name__ == "__main__":
	retrieve_stock_data(symbol, start_date, end_date)
# 

# Predict stock price using neural network

# import data
start_date = datetime.datetime(2016,1,1)
end_date = datetime.datetime(2016,6,20) 
symbol = "PETR4.SA"
df = web.DataReader(symbol, 'yahoo', start_date, end_date)

# create neural network regressor





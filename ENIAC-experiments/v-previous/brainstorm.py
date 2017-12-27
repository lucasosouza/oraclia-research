class Operation():
    def __init__(price, qty, start_date, end_date=None):
        self.price = price
        self.qty = qty
        self.start_date = start_date
        
    def close(self, end_date, sell_price):
        self.end_date = end_date
        self.gain_loss = self.price / sell_price        

class Operator():
    def __init__(data, clf, strategy, initial_capital=0, start_date='2015-01-01', end_date='2015-12-31'):
        self.data = data.copy()
        self.clf = clf
        self.capital = initial_capital
        self.stocks = 0.0
        self.period = pd.date_range(start=start_date, end=end_date, freq='D')
        self.operations = []
        self.strategy = strategy
    
    def run(self):
        for day in self.period:
            # needs to be a working day
            if day in self.data.index:
                # check if there any open operations that needs to be closed
                self.check_operations(day)
                # try to predict
                label = clf.predict(self.data.loc[day])
                if label:
                    if self.capital > 0:
                        self.buy(day)
                            
    def check_operations(self, day):
        for operation in self.operations:
            span, profit, loss = self.strategy
            if not self.end_date:
                valuation = operation.price / self.data.loc[day, 'Adj Close']
                if valuation >= profit or valuation <= loss:
                    self.sell(operation, day)
    
    def buy(self, day):
        price = self.data.loc[day, 'Adj Close']
        qty = self.capital / price
        # update stocks and capital
        self.stocks += qty
        self.capital = 0
        # open operation
        self.operations.append(Operation(price = price, qty = qty, start_date = day))
        
    def sell(self, day, operation):
        price = self.data.loc[day, 'Adj Close']
        # update stocks and capital
        self.capital += self.stocks * price
        self.stocks = 0 
        # close operation
        operation.close(day, price)
        
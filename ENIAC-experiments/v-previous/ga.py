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
        # apply PCA
        pca = PCA(n_components = 10, random_state=42)
        X_transformed = pca.fit_transform(X)
        
        #predict
        clf = GBC(random_state=42)
        cv = StratifiedShuffleSplit(n_splits=10, test_size=.1, random_state=42)
        scores = cross_val_score(clf, X_transformed, y, cv=cv, scoring='precision')

        # return score
        return (scores.mean())

    def evaluate(self, forward, profit_margin, stop_loss):
        self.create_labels(forward=forward, profit_margin=profit_margin, stop_loss=stop_loss)       
        score = self.score(*self.prep_data())
        print("span: {}, profit_margin: {:.3f}, stop_loss: {:.3f} --  score: {:.3f}".format(
            forward, profit_margin, stop_loss, score))
        return score


class Strategy():

    def __init__(self, span = 7, profit_margin = .06, stop_loss = .04):
        self.span = span
        self.profit_margin = profit_margin
        self.stop_loss = stop_loss
        self.mutations = [
            self.increase_span,
            self.decrease_span,
            self.increase_stop_loss,
            self.decrease_stop_loss,
            self.increase_profit_margin,
            self.decrease_profit_margin
        ]

    def mutate(self):
        np.random.choice(self.mutations)()

    def inform_params(self):
        return self.span, self.profit_margin, self.stop_loss

    def report(self):
        print("span: {}, profit_margin: {:.3f}, stop_loss: {:.3f}".format(
            self.span, self.profit_margin, self.stop_loss))

    # add a random component to mutation
    # allow 'wild' mutations

    def increase_span(self):
        self.span += 2

    def decrease_span(self):
        self.span -= 2

    def increase_profit_margin(self):
        self.profit_margin = self.profit_margin * 1.3

    def decrease_profit_margin(self):
        self.profit_margin = self.profit_margin * .7

    def increase_stop_loss(self):
        self.stop_loss = self.stop_loss * 1.3

    def decrease_stop_loss(self):
        self.stop_loss = self.stop_loss * .7

class GA():

    def __init__(self, df):
        """ Seed 2 initial strategies and an instance of backtester """

        self.backtester = Backtester(df.copy())

        self.strategies = pd.DataFrame(np.zeros((2,2)), columns = ['strat', 'score'])
        self.strategies['strat'] = self.strategies['strat'].apply(lambda x:Strategy())
        self.strategies['score'] = self.strategies['strat'].apply(self.evaluate)


    def fit(self, cycles):
        """ Run evolution for n cycles """
        i = 0
        while i < cycles:
            self.reproduce()
            # self.select()

            i += 1

    def best_strategy(self):
        """ Sort and return top perform in available strategies """

        self.strategies =  self.strategies.sort_values(by='score', ascending=False)
        self.strategies.iloc[0, 0].report()
        print("score: {:.4f}".format(self.strategies.iloc[0, 1]))

    def evaluate(self, strat):
        """ To implement: 
            Should evaluate only for those which value is zero, to avoid the cost of re-evaluating 
        """
        return self.backtester.evaluate(*strat.inform_params())

    def reproduce(self):
        """ Create new strategy based on its parents. """

        # sort and take top two performers in the list
        parents = self.strategies.sort_values(by='score', ascending=False).iloc[:2, 0]

        # create six offsprings
        for _ in range(6):
            stratN = self.crossover(*parents)
            stratN.mutate()
            # setting with enlargement using index based selection (not available for position based)
            self.strategies.ix[self.strategies.shape[0]] = (stratN, self.evaluate(stratN))

            # remove identical offspring, there is no use

    def crossover(self, stratA, stratB):
        """ Choose between parents attributes randomly. Return new strategy """

        span = np.random.choice([stratA.span, stratB.span])
        stop_loss = np.random.choice([stratA.stop_loss, stratB.stop_loss])
        profit_margin = np.random.choice([stratA.profit_margin, stratB.profit_margin])
        return Strategy(span=span, stop_loss=stop_loss, profit_margin=profit_margin)

    def select(self):
        """ Remove strategies which are bad performers 
            Define bad as 50 percent worst than best """

        # define cut off score as 50% of the max score
        cut_off = self.strategies['score'].max() * .75
        # remove strategies with scores below the cut-off
        self.strategies = self.strategies[self.strategies['score'] >= cut_off]


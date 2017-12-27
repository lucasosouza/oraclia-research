
import numpy as np
from operator import methodcaller
import pandas as pd

from stocks import Backtester

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

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
		self.span += 1

	def decrease_span(self):
		self.span -= 1

	def increase_profit_margin(self):
		self.profit_margin = self.profit_margin * 1.15

	def decrease_profit_margin(self):
		self.profit_margin = self.profit_margin * .85

	def increase_stop_loss(self):
		self.stop_loss = self.stop_loss * 1.15

	def decrease_stop_loss(self):
		self.stop_loss = self.stop_loss * .85


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


# my GA works
# now I need to work on integrating GA with the learning algorithm
# what I want to optimize with GA are the parameters for the strategy to be used to label observations
# in the supervised learning problem
# that is the deal I'm after

#ga = GA()
#ga.fit(20)
#ga.best_strategy()
# import pdb;pdb.set_trace()



	





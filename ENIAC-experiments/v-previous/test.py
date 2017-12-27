import numpy as np
from operator import methodcaller


class Strategy():

	def __init__(self, span = 10, stop_loss = .05, profit_margin = .05):
		self.span = span
		self.stop_loss = stop_loss
		self.profit_margin = profit_margin
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

	def report(self):
		print "span: {}, stop_loss: {:.3f}, self.profit_margin: {:.3f}".format(
			self.span, self.stop_loss, self.profit_margin)

	def increase_span(self):
		self.span += 1

	def decrease_span(self):
		self.span -= 1

	def increase_stop_loss(self):
		self.stop_loss = self.stop_loss * 1.15

	def decrease_stop_loss(self):
		self.stop_loss = self.stop_loss * .85

	def increase_profit_margin(self):
		self.profit_margin = self.profit_margin * 1.15

	def decrease_profit_margin(self):
		self.profit_margin = strat.profit_margin * .85


strat = Strategy()
strat.report()
for _ in range(10):
	strat.mutate()
strat.report()



import json
import spade
from datetime import datetime
import pandas_datareader.data as web
import pandas as pd
import numpy as np
from blackboard import *

class DataWrangler(spade.Agent.Agent):
	"""Manager of the data wrangling layer"""

	# 1st behavior: receive request DATA MANAGER. Makes preprocessed
	class ReceiveRequestBehav(spade.Behaviour.Behaviour):
		"""
			Receives request from DATA MANAGER. Captures and preprocess data and make it available in the blackboard.

			For now, it only prints a message that the data is available, the DATA Manager will operate under the assumption the data instantly has been made available instantly and with no errors.
		"""
		
		def _process(self):					
			"""Checks for received messages from DATA MANAGER, stating the data is ready, retrieve it from blackboard and present to the user"""

			received_message = self._receive(True)
			if received_message.getPerformative() == "request":
				print "Data Wrangler got request"

				try:
					BLACKBOARD['features'], BLACKBOARD['labels'] = self.myAgent.process()
					print("Data preprocessed and available.")

				except Exception as error:
					print('caught this error: ' + repr(error))

	def _setup(self):
		print "Data Wrangler initialized"
		self.setDefaultBehaviour(self.ReceiveRequestBehav())

	def process(self):
		print "BLACKBOARD: ", BLACKBOARD
		raw_data = self.capture(BLACKBOARD["symbol"], 
			BLACKBOARD["start_date"], BLACKBOARD["end_date"])
		return self.preprocess(raw_data)

	def capture(self, symbol, start_date, end_date):
		symbol = symbol + ".SA"
		date_format = "%Y-%m-%d"
		start_date = datetime.strptime(start_date, date_format)
		end_date = datetime.strptime(end_date, date_format)
		return web.DataReader(symbol, 'yahoo', start_date, end_date)

	def preprocess(self, raw_data, lag=1):
		X = raw_data[raw_data.columns - ['Adj Close']][lag:]
		y = raw_data['Adj Close'].shift(lag)[lag:].reindex(X.index)
		return X,y



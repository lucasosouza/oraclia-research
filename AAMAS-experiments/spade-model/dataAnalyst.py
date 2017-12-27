
import json
import spade
import pandas as pd
import numpy as np
from time import sleep
from sklearn.metrics import r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from blackboard import *

class DataAnalyst(spade.Agent.Agent):
	"""Data analyst responsible for the stock price prediction"""

	class ReceiveBehav(spade.Behaviour.Behaviour):
		"""This behaviour will receive and reply a call for proposal from DATA MANAGER"""

		def _process(self):					
			"""Checks for cfps from DATA MANAGER, and if any, submit a proposal"""

			received_message = self._receive(True)
			performative = received_message.getPerformative()
			if performative == "call-for-proposal":
				print "Data Analyst got call-for-proposal"
				sleep(1)

				try:
					# calculate performance
					performance = self.myAgent.predict()

					#submits proposal
					self.msg = spade.ACLMessage.ACLMessage()
					self.msg.setPerformative("propose")
					self.msg.setOntology("stockMarket")
					self.msg.setLanguage("text")
					self.msg.addReceiver(
						spade.AID.aid( name="{}@127.0.0.1".format("data_manager"), 
							addresses=["xmpp://{}@127.0.0.1".format("data_manager")])
					)
					self.msg.setContent(performance)
					self.myAgent.send(self.msg)				
					print "Data Analyst sending proposal: ", self.myAgent.__class__

				except Exception as error:
					print('caught this error: ' + repr(error))

			#Checks for proposal accepted from DATA MANAGER, and if available makes prediction data available in the blackboard
			elif performative == "accept-proposal":
				print "Data Analyst was awarded contract"

				# make the predictions available at the blackboard
				BLACKBOARD['predictions'] = self.myAgent.pred

				# inform the DATA MANAGER
				self.msg = spade.ACLMessage.ACLMessage()
				self.msg.setPerformative("confirm")
				self.msg.setOntology("stockMarket")
				self.msg.setLanguage("text")
				self.msg.addReceiver(
					spade.AID.aid( name="{}@127.0.0.1".format("data_manager"), 
						addresses=["xmpp://{}@127.0.0.1".format("data_manager")])
				)
				self.msg.setContent("Data is ready.")
				self.myAgent.send(self.msg)				

	def _setup(self):
		print "Data Analyst initialized"
		self.setDefaultBehaviour(self.ReceiveBehav())

	def retrieve_data(self):
		# try to capture the data 10 times, with 10sec interval
		for _ in range(10):
			try:
				return BLACKBOARD['features'], BLACKBOARD['labels']
			except:
				sleep(10)
		return None, None

	def split_test_data(self, X, y, test_percent=.3):
	    length = int(X.shape[0] * (1-test_percent))
	    X_train, X_test = X[:length], X[length:]
	    y_train, y_test = y[:length], y[length:]
	    BLACKBOARD['train_labels'] = y_train
	    return X_train, y_train, X_test, y_test

	def normalize(self, X):
		return (X - X.min()) / (X.max() - X.min())

	def handle_nulls(self, X, y):
		return X.fillna(method="ffill"), y.fillna(method="ffill")

	def predict(self):
		X, y = self.retrieve_data()
		X = self.normalize(X)
		X_train, y_train, X_test, y_test = self.split_test_data(X,y)
		print "Learning..."
		reg = self.learn(X_train, y_train)
		print "Predicting..."
		self.pred = reg.predict(X_test)
		return r2_score(self.pred, y_test)

	def learn(self, X_train, y_train):
		pass

class SvrDataAnalyst(DataAnalyst):

	def learn(self, X_train, y_train):
		reg = MLPRegressor()
		reg.fit(X_train, y_train)
		return reg

class NnDataAnalyst(DataAnalyst):

	def learn(self, X_train, y_train):
		reg = SVR()
		reg.fit(X_train, y_train)
		return reg

# adding more analysts: bus error; segmentation fault





	




from time import sleep
import spade
from blackboard import *
import json
from matplotlib import pyplot as plt
import pandas as pd

class FundManager(spade.Agent.Agent):
	"""Manager of the investment layer"""

	class ReceiveBehav(spade.Behaviour.Behaviour):
		"""This behaviour will receive information from DATA MANAGER"""

		def _process(self):					
			"""Checks for received messages from DATA MANAGER, stating the data is ready, retrieve it from blackboard and present to the user"""

			received_message = self._receive(True)
			performative = received_message.getPerformative()

			if performative == 'request':
				try:
					print "Fund Manager got request"

					# loads content into BLACKBOARD
					content = json.loads(received_message.content)
					BLACKBOARD.update(content)

					# create and send message
					self.msg = spade.ACLMessage.ACLMessage()
					self.msg.setPerformative("request")
					self.msg.setOntology("stockMarket")
					self.msg.setLanguage("text")
					self.msg.addReceiver(
						spade.AID.aid(name="data_manager@127.0.0.1", 
							addresses=["xmpp://data_manager@127.0.0.1"])
					)
					self.msg.setContent("Get predictions.")
					self.myAgent.send(self.msg)
					print "Fund Manager sending request"
				except Exception as error:
					print error

			elif performative == 'confirm':
				try:
					print "Output is ready."
					self.myAgent.inform()
					self.myAgent.clean_board()
				except Exception as error:
					print error

	def _setup(self):
		# initialize
		print "Fund Manager initialized"
		self.setDefaultBehaviour(self.ReceiveBehav())

	def inform(self):
		self.plot(BLACKBOARD['labels'], BLACKBOARD['train_labels'], BLACKBOARD['predictions']) 

	def clean_board(self):
		for entry in BLACKBOARD.copy():
			del BLACKBOARD[entry]

	def plot(self, y, y_train, y_pred):
	    y_pred_full = list(y_train) + list(y_pred)
	    y_pred_full= pd.Series(y_pred_full, index=y.index)
	    ax = y.plot()
	    y_pred_full.plot(ax = ax)
	    ax.legend(['Actual', 'Predicted'])
	    plt.savefig('{}{}-{}-{}.png'.format(BLACKBOARD['path_to_images'], BLACKBOARD['symbol'], BLACKBOARD['start_date'], BLACKBOARD['end_date']))
	    plt.clf()



	



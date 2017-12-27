import spade
from blackboard import *

class DataManager(spade.Agent.Agent):
	"""Manager of the data analysis layer"""

	class ReceiveBehav(spade.Behaviour.Behaviour):
		"""This behaviour will receive requests from FUND MANAGER"""

		def _process(self):					
			"""Checks for received messages from FUND MANAGER, and if any, forward to data analysts as call for proposals and to DATA WRANGLER to collect the data"""

			received_message = self._receive(True)
			performative = received_message.getPerformative()

			if performative == "request":
				try:
					print "Data Manager got request"

					## Message to DATA WRANGLER
					self.msg = spade.ACLMessage.ACLMessage()
					self.msg.setPerformative("request")
					self.msg.setOntology("stockMarket")
					self.msg.setLanguage("text")
					self.msg.addReceiver(
						spade.AID.aid(name="data_wrangler@127.0.0.1", 
							addresses=["xmpp://data_wrangler@127.0.0.1"])
					)
					self.msg.setContent(received_message.getContent())
					self.myAgent.send(self.msg)				

					## Message to data analysts
					# create message and add recipients
					self.msg = spade.ACLMessage.ACLMessage()
					#receivers = ['data_analyst_nn', 'data_analyst_svr']
					self.receivers = ['data_analyst_nn']
					for receiver in self.receivers:
						self.msg.addReceiver(
							spade.AID.aid(name="{}@127.0.0.1".format(receiver), 
								addresses=["xmpp://{}@127.0.0.1".format(receiver)])
						)

					# add counters to check later if all proposals have been received
					self.myAgent.received_proposals = {}
					
					# set remaining parameters
					self.msg.setPerformative("call-for-proposal")
					self.msg.setOntology("stockMarket")
					self.msg.setLanguage("text")
					self.msg.setContent(received_message.getContent())

					#send
					self.myAgent.send(self.msg)
				except Exception as error:
					print error


			elif performative == "propose":
				print "Data Manager received proposal"

				# saves the message content to agents' received proposals 
				self.myAgent.received_proposals[received_message.sender] =  float(received_message.content)
				print "Received Proposals: ", self.myAgent.received_proposals

				try:
					# check if all expected proposals have been received
					if len(self.myAgent.received_proposals) == len(self.receivers):
						# evaluate and choose best agents
						winner = sorted(self.myAgent.received_proposals.items(), key=lambda x:-x[1])[0][0]
						# send a return message awarding the winner
						print "We have a winner: ", winner
						self.msg = spade.ACLMessage.ACLMessage()
						self.msg.setPerformative("accept-proposal")
						self.msg.setOntology("stockMarket")
						self.msg.setLanguage("text")
						self.msg.addReceiver(winner)
						self.msg.setContent("The contract is yours, congratulations!")
						self.myAgent.send(self.msg)
				except Exception as error:
					print error				

			elif performative == "confirm":
				print "Data Manager received contracted product"

				# check if content says data is ready, else handle the error
				if received_message.content == "Data is ready.":
					# inform the fund manager the data is available
					self.msg = spade.ACLMessage.ACLMessage()
					self.msg.setPerformative("confirm")
					self.msg.setOntology("stockMarket")
					self.msg.setLanguage("text")
					self.msg.addReceiver(
						spade.AID.aid( name="{}@127.0.0.1".format("fund_manager"), 
							addresses=["xmpp://{}@127.0.0.1".format("fund_manager")])
					)
					self.msg.setContent("Data is available at blackboard")
					self.myAgent.send(self.msg)	

	def _setup(self):
		print "Data Manager initialized"
		self.setDefaultBehaviour(self.ReceiveBehav())



	



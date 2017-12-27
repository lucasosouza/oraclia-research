import spade

# identification in SPADE
# identification = spade.AID.aid(name="agent@myhost.myprovider.com", addresses=["xmpp://agent@myhost.myprovider.com"])

class BasicAgent(spade.Agent.Agent):
	""" Model Agent """

	def _setup(self):
		print "My agent is about to start the show..."


class SenderAgent(spade.Agent.Agent):
	""" Model Agent """

	def _setup(self):
		print "My agent is about to start the show..."

class ReceiverAgent(spade.Agent.Agent):

	def _setup(self):
		# Add the "ReceiveBehav" as the default behaviour
		rb = self.ReceiveBehav()
		self.setDefaultBehaviour(rb)
		
		# Prepare template for "AnotherBehav"
		cooking_template = spade.Behaviour.ACLTemplate()
		cooking_template.setOntology("cooking")
		mt = spade.Behaviour.MessageTemplate(cooking_template)

		# Add the behaviour WITH the template
		ab = self.AnotherBehav()
		self.addBehaviour(ab, mt)				

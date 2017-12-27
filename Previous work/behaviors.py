import spade

class SimpleBehav(spade.Behaviour.Behaviour):
	""" Simple behavior """

	def onStart(self):
		print "Starting behaviour . . ."
		self.counter = 0

	def _process(self):
		print "Counter:", self.counter
		self.counter = self.counter + 1
		time.sleep(1)

class PeriodicBehav(spade.Behaviour.PeriodicBehaviour):
	""" PeriodicBehavior """

	def onStart(self):
		print "Starting behaviour . . ."
		self.counter = 0

	def _onTick(self):
	 	print "Counter:", self.counter
	 	self.counter = self.counter + 1
		if int(self.counter) == 5: sys.exit()


class SenderBehav(spade.Behaviour.PeriodicBehaviour):
	""" Periodically sends a message """

	def onStart(self):
		print "Starting sending behaviour . . ."

	def _onTick(self):
		# First, form the receiver AID
		receiver = spade.AID.aid(name="receiver@127.0.0.1", 
                                 addresses=["xmpp://receiver@127.0.0.1"])
		
		# Second, build the message
		self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
		self.msg.setPerformative("inform")        # Set the "inform" FIPA performative
		self.msg.setOntology("myOntology")        # Set the ontology of the message content
		self.msg.setLanguage("OWL-S")	          # Set the language of the message content
		self.msg.addReceiver(receiver)            # Add the message receiver
		self.msg.setContent("Hello World")        # Set the message content
		
		# Third, send the message with the "send" method of the agent
		self.myAgent.send(self.msg)		

class OneShotBehav(spade.Behaviour.OneShotBehaviour):
	def onStart(self):
		print "Starting behaviour . . ."

	def _process(self):
		print "Hello World from a OneShot"

	def onEnd(self):
		print "Ending behaviour . . ."

class TimeOutBehav(spade.Behaviour.TimeOutBehaviour):
    def onStart(self):
            print "Starting behaviour . . ."

    def timeOut(self):
            print "The timeout has ended"

    def onEnd(self):
            print "Ending behaviour . . ."


class InformBehav(spade.Behaviour.OneShotBehaviour):

	def _process(self):
		# First, form the receiver AID
		receiver = spade.AID.aid(name="receiver@127.0.0.1", 
                                 addresses=["xmpp://receiver@127.0.0.1"])
		
		# Second, build the message
		self.msg = spade.ACLMessage.ACLMessage()  # Instantiate the message
		self.msg.setPerformative("inform")        # Set the "inform" FIPA performative
		self.msg.setOntology("myOntology")        # Set the ontology of the message content
		self.msg.setLanguage("OWL-S")	          # Set the language of the message content
		self.msg.addReceiver(receiver)            # Add the message receiver
		self.msg.setContent("Hello World")        # Set the message content
		
		# Third, send the message with the "send" method of the agent
		self.myAgent.send(self.msg)

class ReceiveBehav(spade.Behaviour.Behaviour):
	"""This behaviour will receive all kind of messages"""

	def onStart(self):
		print "Start receiving behaviour..."		

	def _process(self):		# keeps running
		self.msg = None	

		# Blocking receive for 10 seconds
		self.msg = self._receive(True, 10)
		
		# Check wether the message arrived
		if self.msg:
			print self.msg.content
		else:
			print "I waited but got no message"

	def onEnd(self):
		print "Ending receiving behaviour..."		


# class ReceiveBehav(spade.Behaviour.Behaviour):
# 		"""This behaviour will receive all kind of messages"""

# 		def _process(self):
# 			self.msg = None
			
# 			# Blocking receive for 10 seconds
# 			self.msg = self._receive(True, 10)
			
# 			# Check wether the message arrived
# 			if self.msg:
# 				print "I got a message!"
# 			else:
# 				print "I waited but got no message"

class AnotherBehav(spade.Behaviour.Behaviour):
	"""This behaviour will receive only messages of the 'cooking' ontology"""

	def _process(self):
		self.msg = None
		
		# Blocking receive indefinitely
		self.msg = self._receive(True)
		
		# Check wether the message arrived
		if self.msg:
			print "I got a cooking message!"
		else:
			print "I waited but got no cooking message"	

class ModifyBehav(spade.Behaviour.OneShotBehaviour):
    def onStart(self):
        print "Starting behaviour . . ."

    def _process(self):
        print "I'm going to modify my data"
        aad = spade.AMS.AmsAgentDescription()
        aad.ownership = "FREE"
        result = self.myAgent.modifyAgent(aad)
        if result:
                print "Modification OK"
        print "I'm going to check the modification"
        search = self.myAgent.searchAgent(aad)
        print search

    def onEnd(self):
        print "Ending behaviour . . ."

class SearchBehav(spade.Behaviour.OneShotBehaviour):
    def onStart(self):
        print "Starting behaviour . . ."

    def _process(self):
        print "I'm going to search for an agent"
        aad = spade.AMS.AmsAgentDescription()
        search = self.myAgent.searchAgent(aad)
        print search

    def onEnd(self):
        print "Ending behaviour . . ."


class AddServiceBehav(spade.Behaviour.OneShotBehaviour):
    def onStart(self):
        print "Starting Add Service behaviour . . ."

	def _process(self):
		print "I'm going to register a service"
		# create a service
		sd = spade.DF.ServiceDescription()
		sd.setName("test")
		sd.setType("testservice")
		# create set of services and add the one created
		dad = spade.DF.DfAgentDescription()
		dad.addService(sd)
		# configure set of services and registar
		dad.setAID(self.myAgent.getAID())
		res = self.myAgent.registerService(dad)
		print "Service Registered:",str(res)

    def onEnd(self):
        print "Ending Add Service behaviour . . ."


# FSMBehaviour
# EventBehaviour


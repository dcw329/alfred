import configparser
import logging
import random
import re
import string
import sleekxmpp
import sys

from markov import Markov

# ensure unicode is handled properly incase python is not v3.0
if sys.version_info < (3, 0):
	reload(sys)
	sys.setdefaultencoding('utf8')
else:
	raw_input = input

animalsounds = ["meow", "woof", "moo"]
animalsounds_set = set(animalsounds)

class CubeBot (sleekxmpp.ClientXMPP):

	def __init__ (self, jid, password, room, nick, fileName):
		sleekxmpp.ClientXMPP.__init__(self, jid, password)
		self.room = room
		self.nick = nick

		#initialize markov chain with input file
		inputFile = open(fileName)
		self.markov = Markov(inputFile)

		self.add_event_handler("session_start", self.start)
		self.add_event_handler("groupchat_message", self.messageHandler)

	#begin receiving/responding
	def start(self, event):
		self.get_roster()
		self.send_presence()
		self.plugin['xep_0045'].joinMUC(self.room, self.nick) #enable group chat

	"""
	some utility functions to process the message text
	"""
	def removeItems(self, message):
		#do all the operations!
		message = self.removeParens(message)
		message = self.removeUsernames(message)
		message = self.removeAsteriskWords(message) #could return ""
		return message

	def removeParens(self, message):
		return [re.sub('[\(\)]', '', x) for x in message]

	def removeUsernames(self, message):
		#if the first word is a username (ie, ends in ':'), remove it
		try:
			if message[0].endswith(':'):
				message.remove(message[0])
		except IndexError:
			#means we've got an empty message
			return
		return message

	def removeAsteriskWords(self, message):
		#users correct typos with *word or word* generally
		#we don't want alfred repeating those
		#TODO add a spellchecker so alfred can exhibit this behavior correctly
		try:
			if len(message) == 1: #one word
				if ' '.join(message).find('*') != -1: #contains an asterisk
					#return an empty string
					return ""
				else:
					return message
			else:
				return message
		except TypeError: #we have an empty message
			return

	def botNickInText(self, message):
		#strip punctuation from message_body
		regex = re.compile('[%s]' % re.escape(string.punctuation))
		message_no_punct = []
		for word in message:
		 	message_no_punct.append(regex.sub('', word).lower())
		return self.nick in message_no_punct or (self.nick + "s") in message_no_punct

	
	def mosttimes(self):
		return random.random() > 0.3

	def sometimes(self):
		return random.random() > 0.7
	
 	#parse incoming messages
	def messageHandler(self, msg):

		#preprocess input
		human_nick = msg['mucnick'] # whoever we're responding to
		response = "" #initialize response
		original_message_body = msg['body'].split()
		message_body = self.removeItems(original_message_body)

		if message_body == []:
			return

		#always make sure the message we're replying to didn't come from self
		if human_nick != self.nick:

			if human_nick == 'viraj' and message_body == ["alfred", "exit"]:
				self.cleanShutDown()

			#reply if username is mentioned
			if self.botNickInText(original_message_body):
				response = self.markov.generateText()
				self.chatty = random.randint(0, 3)

			#reply if animal sounds are mentioned :)
			elif any( word in animalsounds_set for word in message_body ):
				response = random.choice(animalsounds)

			else: #username is not mentioned
				self.markov.addNewSentence(message_body)

			#send finished response if it's been modified
			self.sendMessage(msg, response)

	def cleanShutDown(self):
		logging.info("Saving cache and quitting")
		self.markov.saveCache()
		sys.exit()
	
	def sendMessage(self, msg, response):
		if response != "":
			self.send_message(mto=msg['from'].bare, mbody=response, mtype='groupchat')
			logging.info("REPLY: " + response)


if __name__ == '__main__':

	#read config file
	config = configparser.ConfigParser()
	config.read('config.conf')

	jid 	= config.get('alfred', 'jid')
	pw 		= config.get('alfred', 'password')
	server 	= config.get('alfred', 'server')
	nick 	= config.get('alfred', 'nick')
	fileName = config.get('alfred', 'textFileName')

	#setup logging
	logging.basicConfig(level=logging.INFO, format='%(levelname)-8s %(message)s')

    # Setup the bot and register plugins.
	xmpp = CubeBot(jid, pw, server, nick, fileName)
	xmpp.register_plugin('xep_0030') # Service Discovery
	xmpp.register_plugin('xep_0045') # Multi-User Chat
	xmpp.register_plugin('xep_0199') # XMPP Ping

    # Connect to the XMPP server and start processing XMPP stanzas.
	if xmpp.connect(('obnauticus.com', 5222)):
		xmpp.process(block=True)
		print("Done")
	else:
		print("Unable to connect.")

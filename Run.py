#THIS COPYBOT PROGRAM IS WRITTEN IN PYTHON 2.7
#Credit to Bad Nidalee for the video I based this simple chatbot on
#"How to build your own chat bot for Twitch in 30 minutes! (Python)"
#https://www.youtube.com/watch?v=T8DLwACpe3o

import string
import socket
from Settings import HOST, PORT, PASS, IDENT, CHANNEL
import random
import urllib, json

def openSocket():
	s = socket.socket()
	s.connect((HOST, PORT))
	s.send("PASS " + PASS + "\r\n")
	s.send("NICK " + IDENT + "\r\n")
	s.send("JOIN #" + CHANNEL + "\r\n")
	return s
	
def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
	s.send(messageTemp + "\r\n")
	print("Sent: " + messageTemp)

def joinRoom(s):
	readbuffer = ""
	Loading = True
	while Loading:
		readbuffer = readbuffer + s.recv(1024)
		temp = string.split(readbuffer, "\n")
		readbuffer = temp.pop()
		
		for line in temp:
			print(line)
			Loading = loadingComplete(line)
	#sendMessage(s, "Kappa") #sends a message after connected to room
	
def loadingComplete(line):
	if("End of /NAMES list" in line):
		return False
	else:
		return True

def getUser(line):
	separate = line.split(":", 2)
	user = separate[1].split("!", 1)[0]
	return user

def getMessage(line):
	separate = line.split(":", 2)
	message = separate[2]
	return message

#randomizes word order in a sentence
def scramble(sentence):
   split = sentence.split()  # Split the string into a list of words
   random.shuffle(split)  # This shuffles the list in-place.
   return ' '.join(split)  # Turn the list back into a string

#main program
#this url returns the current chatters in the channel in json format
url = "https://tmi.twitch.tv/group/user/"+CHANNEL+"/chatters"
response = urllib.urlopen(url)
data = json.loads(response.read())

s = openSocket()
joinRoom(s)
readbuffer = ""

#grab a random user when we start the program
random_user_index=random.randint(0,len(data["chatters"]["viewers"])-1)
user_2_copy = data["chatters"]["viewers"][random_user_index]
#user_2_copy="username" #or just input the user's name here
print "The user I am copying is: " + user_2_copy

while True:

	readbuffer = readbuffer + s.recv(1024)
	temp = string.split(readbuffer, "\n")
	readbuffer = temp.pop()
		
	for line in temp:
		#keep bot connected if twitch pings it
		if "PING" in line:
			s.send(line.replace("PING", "PONG"))
			break
		user = getUser(line) #get the user that sent the last message to the chat
		if user == user_2_copy:
			message = getMessage(line) #get our user's message
			#uncomment the line below to randomly capitalize letters in message
			#message = "".join( random.choice([c.upper(), c ]) for c in message )
			sendMessage(s, message) #send message to chat :)
			break
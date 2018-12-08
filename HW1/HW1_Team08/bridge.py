import sys
import BridgeKeys
import argparse
import socket
from datetime import datetime
import pickle
from cryptography.fernet import Fernet
import hashlib
import json
from watson_developer_cloud import TextToSpeechV1
import os


#Watson Username/Password/URL
watsonUN = BridgeKeys.watson_username
watsonPass = BridgeKeys.watson_password
watsonURL = BridgeKeys.watson_url

#Setup for Watson
text_to_speech = TextToSpeechV1(
	url = watsonURL,
	username = watsonUN,
	password = watsonPass)

#Command Line Arguments
#bridge.py -svr-p <SERVER_PORT> -svr <SERVER_IP> -p <BRIDGE_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>
parser = argparse.ArgumentParser()
parser.add_argument("-svr-p", dest = "serverPort", help = "server port")
parser.add_argument("-svr", dest = "serverIP", help = "server IP address")
parser.add_argument("-p", dest = "bridgePort", help = "bridge port")
parser.add_argument("-b", dest = "backlogSize", help = "backlog size")
parser.add_argument("-z", dest = "socketSize", help = "socket size")

args = parser.parse_args()

#Command Line Value Storage
serverPort = int(args.serverPort)
serverIP = args.serverIP
bridgePort = int(args.bridgePort)
backlogSize = int(args.backlogSize)
socketSize = int(args.socketSize)

connect = 0
#Setup for Bridge/Server Socket
socketBS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Setup for Client/Bridge Socket
HOST = '0.0.0.0'
PORT = bridgePort
socketCB = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

socketCB.bind((HOST,PORT))
#//////////////////////Checkpoint 01///////////////////////
print ('[',datetime.now().strftime('%H:%M:%S'),']','Created socket at 0.0.0.0 on port ',str(bridgePort))

socketCB.listen(backlogSize)
#////////////////////Checkpoint 02////////////////////////
print('[',datetime.now().strftime('%H:%M:%S'),']','Listening for client connections')
	
conn, addr = socketCB.accept()
#/////////////////Checkpoint 03///////////////
print('[',datetime.now().strftime('%H:%M:%S'),']','Accepted client connection from ',addr[0],'on port ',str(addr[1]))

while(1):
	print('LOOP START')
	pickled = conn.recv(socketSize)
	unpickled = pickle.loads(pickled)
	#////////////////Checkpoint 04////////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Received data: ', unpickled)
	
	encryptedTweet = unpickled[0]
	key = unpickled[1]
	hash = unpickled[2]
	#Decrypt the Tweet
	f = Fernet(key)
	tweet = f.decrypt(encryptedTweet)
	#///////////////Checkpoint 05////////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Decrypt: Key: ',key,'| Plaintext: ',tweet)
	#Verify Checksum
	m = hashlib.md5()
	m.update(tweet)
	if m.hexdigest() == hash:
		print('Checksum verified')
	else:
		print('Checksums are different')
	
	#Send string to IBMWatson for text to speech
	with open('Question.wav', 'wb') as audio_file:
		audio_file.write(
			text_to_speech.synthesize(tweet.decode('utf-8'), 'audio/wav', 
				'en-US_AllisonVoice').get_result().content)
	#////////////Checkpoint 06////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Speaking Question: ',tweet)
	os.system('aplay Question.wav')
	os.remove('Question.wav')
	#Connect to the Server
	#////////////////Checkpoint 07//////////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Connecting to ', serverIP, 'on port', serverPort)
	if connect == 0:
		socketBS.connect((serverIP, serverPort))
		connect = 1
	
	#Sending Pickled Data
	#///////////////Checkpoint 08//////////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Sending data: ',pickled)
	socketBS.send(pickled)
	
	#Receive Answer From Server
	answer = socketBS.recv(socketSize)
	#//////////////Checkpoint 09/////////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Received data:',answer)
	
	#Decrypt Answer
	unpickAnswer = pickle.loads(answer)
	
	trueAnswer = f.decrypt(unpickAnswer[0].encode('utf-8'))
	answerHash = unpickAnswer[2]
	
	#////////////Checkpoint 10///////////////////
	print ('[',datetime.now().strftime('%H:%M:%S'),']','Decrypt: UsingKey:', key, '| Plaintext:',trueAnswer)
	
	#Verify Checksum
	m.update(trueAnswer)
	if m.hexdigest() == answerHash:
		print('Checksum verified')
	else:
		print('Checksums are different')
	
	#Send Answer to Client
	conn.sendall(answer)
	
	#Send Answer to IBM Watson for TTS
	with open('Answer.wav', 'wb') as audio_file:
		audio_file.write(
			text_to_speech.synthesize(trueAnswer.decode('utf-8'), 'audio/wav', 
				'en-US_AllisonVoice').get_result().content)
	#Speak Final Answer
	#////////////////Checkpoint 11/////////////
	print('[',datetime.now().strftime('%H:%M:%S'),']','Speaking Answer:',trueAnswer)
	os.system('aplay Answer.wav')
	os.remove('Answer.wav')
	
conn.close()
socketBS.close()

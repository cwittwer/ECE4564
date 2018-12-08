
import tweepy
import hashlib
import socket
import re
import pickle
import sys
import json
import ClientKeys
from tweepy.streaming import StreamListener
from tweepy import Stream
import argparse
from cryptography.fernet import Fernet
from datetime import datetime 

#consumer key, consumer secret, access token, access secret
ckey= ClientKeys.consumer_key
csecret= ClientKeys.consumer_secret
atoken= ClientKeys.access_token
asecret= ClientKeys.access_token_secret

#command line arguments
#client.py -brg <bridge_IP> -p <bridge_PORT> -z <SOCKET_SIZE> -t "<HASHTAG>"
parser = argparse.ArgumentParser()
parser.add_argument("-brg", dest = "bridgeIP", help = "bridge IP address")
parser.add_argument("-p", dest = "bridgePort", help = "bridge port")
parser.add_argument("-z", dest = "socketSize", help = "Socket size")
parser.add_argument("-t", dest = "hashtag", help = "Twitter hashtag to search for")

args = parser.parse_args()

#setup the socket and connections
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#hostIP = ''
bridgeIP = args.bridgeIP
bridgePort = int(args.bridgePort)
backlog = 5
size = int(args.socketSize)
start = 1
tweet = ''

#s.bind((hostIP, port))
#Checkpoint 01
print('[',datetime.now().strftime('%H:%M:%S'),']','Connecting to:', bridgeIP, 'on port', bridgePort)
s.connect((bridgeIP, bridgePort))

key = Fernet.generate_key()
f = Fernet(key)

auth = tweepy.OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)
api = tweepy.API(auth, wait_on_rate_limit=True)

"""
Create class GetTweetListener, inheriting from StreamListener to listen to stream, then sends the 
recieved tweet to the bridge
"""
class GetTweetListener(StreamListener):

	def on_data(self, data):
		global tweet
		tweetdata = json.loads(data)
		tweet = tweetdata["text"]
		tweet = tweet.replace("#ECE4564T08", "")
		tweet = tweet.replace("  ", " ")
		#Checkpoint 03
		print('[',datetime.now().strftime('%H:%M:%S'),']','New Tweet:', tweet)
		return(False)

	def on_error(self, status):
		print(status)
	
	def on_status(self, status):
		print(status.text)

def buildPackage(tweetMessage):
	hash=md5Hash(tweetMessage)
	key, encryptedTweet = encryptTweet(tweetMessage)
	return (encryptedTweet, key, hash)
	
def md5Hash(tweetMessage):
	m=hashlib.md5()
	m.update(tweetMessage.encode('utf-8'))
	return m.hexdigest()
	
def encryptTweet(tweetMessage):
	encryptedTweet = f.encrypt(tweetMessage.encode('utf-8'))
	#checkpoint 04
	print('[',datetime.now().strftime('%H:%M:%S'),']','Encrypt: Generated Key:', key, '| Ciphertext:', encryptedTweet)
	return key, encryptedTweet
	
def decryptTweet(encryptedAnswer):
	answer = f.decrypt(encryptedAnswer.encode('utf-8'))
	#checkpoint 05
	print('[',datetime.now().strftime('%H:%M:%S'),']','Decrypt: Using Key:', key.decode(), '| Plaintext:', answer.decode())
	return answer



while(1):
	if start:
		#checkpoint 02
		print('[',datetime.now().strftime('%H:%M:%S'),']','Listenening for tweets that contain:', args.hashtag)
		#grabbing tweet from twitter with hashtag determined by command line args
		getTweetListener = GetTweetListener()
		getTweet = Stream(api.auth, getTweetListener)
		getTweet.filter(track=[args.hashtag])
		start = 0
	
	q = None
	q = pickle.dumps(buildPackage(tweet), protocol=2)
	
	#Checkpoint 05
	s.send(q)
	print('[',datetime.now().strftime('%H:%M:%S'),']','Sending data:', q)

	answer = s.recv(size)
	data = pickle.loads(answer)
	#Checkpoint 07
	print('[',datetime.now().strftime('%H:%M:%S'),']','Received data:', data)
	decryptTweet(data[0])
	start = 1

s.close()
	

	
	



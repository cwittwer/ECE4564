import hashlib
import socket
import pickle
import sys
import json
import ServerKeys
import argparse
import wolframalpha
from cryptography.fernet import Fernet
from datetime import datetime

#command line arguments
#server.py -p <SERVER_PORT> -b <BACKLOG_SIZE> -z <SOCKET_SIZE>
parser = argparse.ArgumentParser()
parser.add_argument("-p", dest = "serverPort", help = "bridge port")
parser.add_argument("-b", dest = "backlogSize", help = "backlog size")
parser.add_argument("-z", dest = "socketSize", help = "Socket size")

args = parser.parse_args()

#setup Wolfram Alpha
app_id = ServerKeys.wolfram_alpha_app_id
wolfclient = wolframalpha.Client(app_id)

host = socket.gethostbyname(socket.gethostname())
port = int(args.serverPort)
backlog = int(args.backlogSize)
size = int(args.socketSize)


def buildPackage(message, key):
	hash=md5Hash(message)
	key, encryptedData = encryptData(message, key)
	return (encryptedData, key, hash)

def md5Hash(message):
	h=hashlib.md5()
	h.update(message.encode('utf-8'))
	#checkpoint 09
	print('[',datetime.now().strftime('%H:%M:%S'),']','Generated md5 Checksum:', h.hexdigest())
	return h.hexdigest()

def encryptData(message, key):
	f = Fernet(key)
	encryptedData = f.encrypt(message.encode())
	#checkpoint 08
	print('[',datetime.now().strftime('%H:%M:%S'),']','Encrypt: Key:', key, '| Ciphertext:', encryptedData)
	return key, encryptedData

def decryptData(encryptedData, key):
	f = Fernet(key)
	print('Encrypted Data:   ', encryptedData)
	answer = f.decrypt(encryptedData.encode())
	answer = bytes.decode(answer)
	return answer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
#checkpoint 01
print('[',datetime.now().strftime('%H:%M:%S'),']','Created socket at', host, 'on port', port)
s.listen(backlog)
#checkpoint 02
print('[',datetime.now().strftime('%H:%M:%S'),']','Listening for client connections')
c, addr = s.accept()
#checkpoint 03
print('[',datetime.now().strftime('%H:%M:%S'),']','Accepted client connection from', addr, 'on port', port)

while 1:
	question = c.recv(size)
	data = pickle.loads(question)
	#checkpoint 04
	print('[',datetime.now().strftime('%H:%M:%S'),']','Recieved Data:', data)

	question = decryptData(data[0], data[1])
	#checkpoint 05
	print('[',datetime.now().strftime('%H:%M:%S'),']','Decrpyt: Key:', data[1], '| Plaintext', question)
	#checkpoint 06
	print('[',datetime.now().strftime('%H:%M:%S'),']','Sending question to WolframAlpha:', question)
	res = wolfclient.query(question)
	answer = next(res.results).text
	#checkpoint 07
	print('[',datetime.now().strftime('%H:%M:%S'),']','Recieved answer from WolframAlpha:', answer)
	package = pickle.dumps(buildPackage(answer, data[1]), protocol=2)

	if package:
		#checkpoint 10
		print('[',datetime.now().strftime('%H:%M:%S'),']','Sending answer:', package)
		c.send(package)
c.close()
s.close()

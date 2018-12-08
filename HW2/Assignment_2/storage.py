#STORAGE FILE

import bluetooth
import argparse
from datetime import datetime 
import threading
import json
from subprocess import check_output
import MongoDB as mongo
import LED as led
import sys
from time import sleep
 
# command line arguments
# storage.py -p <Port Number> -b <Backlog> -z <Socket Size>
parser = argparse.ArgumentParser()
parser.add_argument("-p", dest = "port", help = "port number")
parser.add_argument("-b", dest = "backlog", help = "backlog size")
parser.add_argument("-z", dest = "socketsize", help = "Socket size")

args = parser.parse_args()

port = int(args.port)
backlog = int(args.backlog)
socket = int(args.socketsize)

db = mongo.mongo()
lights = led.LED()

class bd_thread(threading.Thread):
	def __init__(self, server_sock, backlog, socket, port):
		threading.Thread.__init__(self)
		self.server_sock = server_sock
		self.backlog = backlog
		self.socket = socket
		self.port = port
	def run(self):
		server_sock.listen(backlog)
		while(1):
			print('[',datetime.now().strftime('%H:%M:%S'),']','Listening for client connections')
			client_sock, address = server_sock.accept()
			print('[',datetime.now().strftime('%H:%M:%S'),']','Accepted client connection from ' + str(address) + 'on port ' + str(port))
			data = client_sock.recv(socket)
			message = json.loads(data.decode('utf-8'))
			print('[',datetime.now().strftime('%H:%M:%S'),']','Received Payload: ', message)
			
			if message['Action'] == 'ADD':
				response = db.ADD(message)
				send = json.dumps(response)
				client_sock.send(send)
			elif message['Action'] == 'BUY':
				response = db.BUY(message)
				send = json.dumps(response)
				client_sock.send(send)
			elif message['Action'] == 'SELL':
				response = db.SELL(message)
				send = json.dumps(response)
				client_sock.send(send)
			elif message['Action'] == 'DELETE':
				response = db.DELETE(message)
				send = json.dumps(response)
				client_sock.send(send)
			elif message['Action'] == 'COUNT':
				response = db.COUNT(message)
				send = json.dumps(response)
				client_sock.send(send)
			elif message['Action'] == 'LIST':
				response = db.LIST(message)
				send = json.dumps(response)
				client_sock.send(send)
			else:
				response = {'Msg' : 'Error: action not found'}
				send = json.dumps(response)
				client_sock.send(send)
				
		client_sock.close()
	
class GPIO_thread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
	def run(self):
		while(1):
			count_books = db.COUNT_INT()
			red = count_books // 100
			green_remain = count_books % 100
			green = green_remain // 10
			blue_remain = green_remain % 10
			blue = blue_remain
			lights.blink_red(red)
			lights.blink_green(green)
			lights.blink_blue(blue)
			sleep(10)

def read_local_bdaddr():
	addr_info = str(check_output(["hcitool","dev"]),"UTF-8")
	chunks = addr_info.split('\t')
	bdaddr = chunks[-1][:-1]
	return bdaddr

def sendmessage(answer, targetAddress):
	server_sock.connect((targetAddress, port))
	server_sock.send(answer)

bd_addr = read_local_bdaddr()

server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

server_sock.bind((bd_addr, port))
print('[',datetime.now().strftime('%H:%M:%S'),']','Created socket at ', bd_addr , 'on port', port)

try:
	socket_thread = bd_thread(server_sock, backlog, socket, port)
	gpio_thread = GPIO_thread()
	socket_thread.start()
	gpio_thread.start()
	while socket_thread.isAlive():
		socket_thread.join(1)
		while gpio_thread.isAlive():
			gpio_thread.join(1)
except KeyboardInterrupt:	
	server_sock.close()
	lights.led_cleanup()
	db.DROP_DB()
	socket_thread.exit()
	gpio_thread.exit()
	sys.exit()
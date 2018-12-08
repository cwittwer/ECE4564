import bluetooth
import pika
import argparse
from datetime import datetime
import json

#Command line arguments
#python3 processor.py -storage <Storage Bluetooth Mac Addr> -p <Storage Port Number> -z <Socket Size>

parse = argparse.ArgumentParser()
parse.add_argument("-storage", dest="storage", help="storage addr")
parse.add_argument("-p", dest="port", help="port number")
parse.add_argument("-z", dest="size", help="socket size")

args = parse.parse_args()

storage = args.storage
port = int(args.port)
size = int(args.size)

#Setup RabbitMQ Receive
credentials = pika.PlainCredentials('admin', 'password')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='0.0.0.0', credentials=credentials))
channel = connection.channel()
channel.queue_declare(queue='rpc_queue')
result = channel.queue_declare(exclusive=True)
callback_queue = result.method.queue

#		Checkpoint 1
print('[',datetime.now().strftime('%H:%M:%S'),']','Created rabbitmq at 0.0.0.0')

def on_request(ch, method, props, body):
	thing = json.loads(body.decode('utf-8'))
	#		Checkpoint 3
	print('[',datetime.now().strftime('%H:%M:%S'),']','Received request payload',thing)
	
	#		Checkpoint 4
	print('[',datetime.now().strftime('%H:%M:%S'),']','Connecting to ',storage,' on port ',port)
	bt = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
	bt.connect((storage, port))
	bt.send(body)
	
	ans = bt.recv(size)
	printans = json.loads(ans.decode('utf-8'))
	#		Checkpoint 5
	print('[',datetime.now().strftime('%H:%M:%S'),']','Received answer payload',printans)
	
	bt.close()

	ch.basic_publish(exchange='',
					routing_key=props.reply_to,
					properties=pika.BasicProperties(correlation_id=props.correlation_id),
					body=ans)
	ch.basic_ack(delivery_tag = method.delivery_tag)
	print('END OF ON_REQUEST, SHOULD BE LISTENING AGAIN')
	
	
channel.basic_qos(prefetch_count=0)
channel.basic_consume(on_request, queue='rpc_queue')
#		Checkpoint 2
print('[',datetime.now().strftime('%H:%M:%S'),']','Awaiting client requests')
channel.start_consuming()


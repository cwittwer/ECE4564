#
#File built with the help of RabbitMQ tutorials site
#https://www.rabbitmq.com/tutorials/tutorial-six-python.html

#!/usr/bin/env/python
import pika
import uuid
import argparse
from datetime import datetime
import json

parser = argparse.ArgumentParser()

parser.add_argument('-proc', dest = 'procIP', help = 'processor IP')
parser.add_argument('-action', dest = 'action', help = 'what you want to do')
parser.add_argument('-book', dest = 'book', help = 'Book info')
parser.add_argument('--count', dest = 'count', help = 'count')

args = parser.parse_args()

IP = str(args.procIP)
action = str(args.action)
book = json.loads(args.book)
if (args.count is not None):
    count = int(args.count)


def build_package(action, book):
        if (action == 'ADD' or action == 'DELETE' or action == 'COUNT'):
                print('[',datetime.now().strftime('%H:%M:%S'),']','Action is valid.')
                package = {'Action': action, 'Msg': { 'Book Info': book}}
                package = json.dumps(package)
                return package
        elif (action == 'BUY' or action == 'SELL'):
                print('[',datetime.now().strftime('%H:%M:%S'),']','Action is valid.')
                package = {'Action': action, 'Msg': { 'Book Info': book, 'Count': count} }
                package = json.dumps(package)
                return package
        elif (action == 'LIST'):
                print('[',datetime.now().strftime('%H:%M:%S'),']','Action is valid.')
                package = {'Action': action, 'Msg': {}}
                package = json.dumps(package)
                printf
                return package
        else:
                print('[',datetime.now().strftime('%H:%M:%S'),']','Action is invalid.')
                return None

                
class FibonacciRpcClient(object):
    
        def __init__(self):
                self.credentials = pika.PlainCredentials( 'admin','password' )
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=IP, credentials = self.credentials))

                self.channel = self.connection.channel()

                result = self.channel.queue_declare(exclusive=True)
                self.callback_queue = result.method.queue

                self.channel.basic_consume(self.on_response, no_ack=True,queue=self.callback_queue)

        def on_response(self, ch, method, props, body):
                if self.corr_id == props.correlation_id:
                        self.response = body

        def call(self, n):
                self.response = None
                self.corr_id = str(uuid.uuid4())
                self.channel.basic_publish(exchange='',
                                           routing_key='rpc_queue',
                                           properties=pika.BasicProperties(
                                                 reply_to = self.callback_queue,
                                                 correlation_id = self.corr_id,
                                                 ),
                                           body=str(n))
                
                while self.response is None:
                    self.connection.process_data_events()
                return self.response


fibonacci_rpc = FibonacciRpcClient()

send = build_package(action, book)

if (send != None):
    response = fibonacci_rpc.call(send)
    print('[',datetime.now().strftime('%H:%M:%S'),']','Request payload: ', response)
    message = json.loads(response.decode('utf-8'))
    if (action == 'ADD' or action == 'BUY' or action == 'SELL' or action == 'DELETE' or action == 'COUNT'):
        print('[',datetime.now().strftime('%H:%M:%S'),']', action, '-', (message['Msg']))
    elif (action == 'LIST'):
        print('[',datetime.now().strftime('%H:%M:%S'),']',action, '-', (message['Books']))










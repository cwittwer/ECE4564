#STORAGE FILE

import argparse
from datetime import datetime 
import threading
import json
from subprocess import check_output
import MongoDB as mongo
import sys
from time import sleep

app = Flask(__name__)
db = mongo.mongo()

@app.route('/Book/list', methods=['GET'])
def LIST();
	response = db.LIST()
	return json.dumps(response)
	
@app.route('/Book/count', methods=['GET'])
def COUNT();
	author = request.args.get('Author')
	name = request.args.get('Name')
	response = db.COUNT(name, author)
	return  response;
@app.route('/Book/delete', methods=['DELETE'])
def DELETE():
	response = db.DELETE(request.json)
	return response
@app.route('/Book/buy', methods=['PUT'])
def BUY():
	response = db.BUY(request.json)
	return response
@app.route('/Book/sell', methods=['PUT'])
def SELL():
	response = db.SELL(request.json)
	return response
@app.route('/Book/add', methods=['POST'])
def ADD():
	response = db.ADD(request.json)
	return response
	
try:
    # From this link: https://github.com/jstasiak/python-zeroconf/blob/master/examples/registration.py
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
        
    desc = {'path':'/home/pi'}

    #Get the local IP address of the Pi running led.py
    localip = socket.inet_aton("127.0.0.1")
    
    info = ServiceInfo("_http._tcp.local.",
                       "Team08STORAGE._http._tcp.local.",
                       socket.inet_aton("127.0.0.1"), 5000, 0, 0, desc,"STORAGE.local.")
    
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    print("Zeroconf service registered.")
    
    #Flask:
    app.run(host='0.0.0.0', debug=False)
        
        
except KeyboardInterrupt:
    pass

finally:
    db.DROP_DB()
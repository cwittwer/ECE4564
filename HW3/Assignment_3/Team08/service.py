from zeroconf import ServiceBrowser, ServiceInfo, ServiceStateChange, Zeroconf
import socket
from pymongo import MongoClient
import AuthDB as auth
from flask import Flask, Response, request, abort
import pycurl
import subprocess
import time
from functools import wraps

LED_ADDRESS = ''
STO_ADDRESS = ''

#authDB Setup
db = auth.AuthDB()

#Get LED IP
def on_service_state_change_LED(zeroconf, service_type, name, state_change):
	if (name=='Team08LED._http._tcp.local.'):
		if state_change is ServiceStateChange.Added:
			info = zeroconf.get_service_info(service_type, name)
			if info:
				global LED_ADDRESS
				LED_ADDRESS = socket.inet_ntoa(info.address)
zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change_LED])
time.sleep(1)
zeroconf.close()
print('LED_ADDRESS Retrieved')

#Zeroconf setup
desc = {'path': '/home/pi/'}
info = ServiceInfo("_http._tcp.local.",
					"Team08SERVICE._http._tcp.local.",
					socket.inet_aton("127.0.0.1"), 5000, 0, 0,
					desc, "Team08SERVICE.local.")
zeroconf = Zeroconf()
zeroconf.register_service(info)
zeroconf.close()
print('Zeroconf Registered')
#Get Storage IP
def on_service_state_change_STO(zeroconf, service_type, name, state_change):
	if (name=='Team08STORAGE._http._tcp.local.'):
		if state_change is ServiceStateChange.Added:
			info = zeroconf.get_service_info(service_type, name)
			if info:
				global STO_ADDRESS
				STO_ADDRESS = socket.inet_ntoa(info.address)
zeroconf = Zeroconf()
browser = ServiceBrowser(zeroconf, "_http._tcp.local.", handlers=[on_service_state_change_STO])
time.sleep(1)
zeroconf.close()
print('STORAGE_ADDRESS Retrieved')

#Auth functions
def check_auth(username, password):
	cursor = db.find()
	ans = False
	for document in cursor:
		if (username==document['username'] and password==document['password']):
				ans = True
				break
	if (ans):
		print ('Authentication Success')
	else:
		print ('Authentication Failure')

def authenticate():
	return Response('Access Denied.  Please log in to continue.',
					401,{'WWW-Authenticate': 'Basic realm="Login Required"'})

def requires_auth(f):
	@wraps(f)
	def decorated(*args, **kwargs):
		auth = request.authorization
		if not auth and not check_auth(auth.username, auth.password):
			return authenticate()
		return f(*args, **kwargs)
	return decorated
	

#Flask
app = Flask(__name__)


#Handle curl requests

@app.route('/add_user', methods=['POST'])
def add_user():
	if not request.json or not 'username' and 'password' in request.json:
		abort(400)
	db.ADD_USER(request.json)

@app.route('/upload/led', methods=['POST'])
@requires_auth
def upload_led():
	thing = request.args.get('file')
	with open('led.sh', 'w') as f:
		c.setopt(c.WRITEFUNCTION, f.write)
		c.perform()
	subprocess.call(['temp.sh', LED_ADDRESS])
	
@app.route('/upload/storage', methods=['POST'])
@requires_auth
def upload_storage():
	thing = request.args.get('file')
	with open('storage.sh', 'w') as f:
		c.setopt(c.WRITEFUNCTION, f.write)
		c.perform()
	subprocess.call(['temp.sh', STO_ADDRESS])

app.run(host='0.0.0.0', debug=True)

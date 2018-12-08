#!/usr/bin/env python3

import sys
import time
import logging
import socket
import json
import requests
from zeroconf import ServiceInfo, Zeroconf
from flask import Flask, request, url_for
import LED_PWM.py as PWM

# some helpful example code was found here: 
# https://learn.adafruit.com/raspipe-a-raspberry-pi-pipeline-viewer-part-2/miniature-web-applications-in-python-with-flask
app = Flask(__name__)

status=''
color=''
intensity=''
blueInt=0
greenInt=0
redInt=0
statusNum=0


redPin   = 36
greenPin = 38
bluePin  = 40

lights = PWM.LED_PWM()

@app.route('/LED/on', methods=['POST'])
def LED_ON():
	global statusNum
	statusNum = 1
	lights.blink(redPin, redInt)
	lights.blink(greenPin, greenInt)
	lights.blink(bluePin, blueInt)
	
@app.route('/LED/off', methods=['POST'])
def LED_OFF():
	global statusNum
	statusNum = 0
	lights.turnOff(redPin)
	lights.turnOff(bluePin)
	lights.turnOff(greenPin)
	return "LED off"
	
@app.route('/LED/info', methods=['GET'])
def LED_INFO():
	ledstatus = {"blue" : blueInt, "green":greenInt, "red":redInt, "status"=statusNum }
    return json.dumps(ledstatus)
	
	
@app.route('/LED', methods=['GET','POST'])
def LED_CHANGE():
	# LED color if status is "on"
	global color
	color = str(request.json['color'])
	global intensity
	intensity = float(request.json['intensity'])
	#set the intensity of the led from the request
	if color == "red":
		lights.blink(redPin, intensity)
		global redInt
		redInt = intensity
		return "successfully set red's intensity to %d" % intensity 
	elif color == "green":
		lights.blink(greenPin, intesity)
		global greenInt
		greenInt = intensity
		return "successfully set green's intensity to %d" % intensity 
	elif color == "blue":
		lights.blink(bluePin, intensity)
		global blueInt
		blueInt = intensity
		return "successfully set blue's intensity to %d" % intensity 
	else:
		return "Invalid color obtained."
	
		
    
    #"Status and color of LED obtained through a GET request"
    elif request.method == 'GET':
        ledstatus = {"blue" : blueInt, "green":greenInt, "red":redInt, "status"=statusNum }
        return json.dumps(ledstatus)        


#Get the IP address of the Pi that is running led.py
def get_ip_address():
    ip_address = '';
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address

try:
    # From this link: https://github.com/jstasiak/python-zeroconf/blob/master/examples/registration.py
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) > 1:
        assert sys.argv[1:] == ['--debug']
        logging.getLogger('zeroconf').setLevel(logging.DEBUG)
        
    desc = {'path':'/home/pi'}

    #Get the local IP address of the Pi running led.py
    localip = socket.inet_aton(get_ip)
    
    info = ServiceInfo("_http._tcp.local.",
                       "Team08LED._http._tcp.local.",
                       localip, 5000, 0, 0, desc, 'Change LED brightness'
                       )
    
    zeroconf = Zeroconf()
    zeroconf.register_service(info)
    print("Zeroconf service registered.")
    
    #Flask:
    app.run(host='0.0.0.0', debug=True)
        
        
except KeyboardInterrupt:
    pass

finally:
    lights.turnOff(redPin)
    lights.turnOff(bluePin)
	lights.turnOff(greenPin)

    lights.led_cleanup()
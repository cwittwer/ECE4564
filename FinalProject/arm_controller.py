import socket
import sys
import RPi.GPIO as GPIO
from time import sleep

control = False
led = False

def Setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    GPIO.setup(12, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(15, GPIO.OUT)
    GPIO.setup(29, GPIO.OUT)
    GPIO.setup(32, GPIO.OUT)
    GPIO.setup(36, GPIO.OUT)
    GPIO.setup(35, GPIO.OUT)
    GPIO.setup(37, GPIO.OUT)
    GPIO.setup(38, GPIO.OUT)
    GPIO.setup(40, GPIO.OUT)

def Stop():
    GPIO.output(11, GPIO.LOW)
    GPIO.output(12, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(15, GPIO.LOW)
    GPIO.output(29, GPIO.LOW)
    GPIO.output(32, GPIO.LOW)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)

#shoulder functions
def ShoulderRight():
    GPIO.output(11, True)
    GPIO.output(12, False)
    
def ShoulderLeft():
    GPIO.output(11, False)
    GPIO.output(12, True)

#arm functions
def ArmDown():
    GPIO.output(13, True)
    GPIO.output(15, False)
    
def ArmUp():
    GPIO.output(13, False)
    GPIO.output(15, True)

#elbow functions
def ElbowUp():
    GPIO.output(32, True)
    GPIO.output(36, False)
    
def ElbowDown():
    GPIO.output(32, False)
    GPIO.output(36, True)

#wrist functions
def WristDown():
    GPIO.output(35, True)
    GPIO.output(37, False)
    
def WristUp():
    GPIO.output(35, False)
    GPIO.output(37, True)

#finger functions
def FingerOut():
    GPIO.output(38, True)
    GPIO.output(40, False)
    
def FingerIn():
    GPIO.output(38, False)
    GPIO.output(40, True)

def LEDon():
    GPIO.output(29, True)

def LEDoff():
    GPIO.output(29, False)

try:
    host = '0.0.0.0'
    port = 55548
    backlog = 5
    size = 1024

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(backlog)
    c, addr = s.accept()

    Setup()

    while 1:
        datar = c.recv(size)
        data = datar.decode('utf-8')
        print(datar.decode('utf-8'))
        if data == 'LED':
            if led == True:
                LEDoff()
                led = False
            else:
                LEDon()
                led = True
        elif data == 'arm':
            control = True
        elif data == 'tracks':
            control = False
            Stop()
        elif data == 'Elbow down':
            ElbowDown()
        elif data == 'Elbow up':
            ElbowUp()
        elif data == 'Elbow stop':
            GPIO.output(32, GPIO.LOW)
            GPIO.output(36, GPIO.LOW)   
        elif data == 'Shoulder right':
            ShoulderRight()
        elif data == 'Shoulder left':
            ShoulderLeft()
        elif data == 'Shoulder stop':
            GPIO.output(11, GPIO.LOW)
            GPIO.output(12, GPIO.LOW)
        elif data == 'Arm down':
            ArmDown()
        elif data == 'Arm up':
            ArmUp()
        elif data == 'Arm stop':
            GPIO.output(13, GPIO.LOW)
            GPIO.output(15, GPIO.LOW)
        elif data == 'Fingers Open':
            FingerOut()
        elif data == 'Fingers Close':
            FingerIn()
        elif data == 'Fingers stop':
            GPIO.output(38, GPIO.LOW)
            GPIO.output(40, GPIO.LOW)
        elif data == 'Wrist down':
            WristDown()
        elif data == 'Wrist up':
            WristUp()
        elif data == 'Wrist stop':
            GPIO.output(35, GPIO.LOW)
            GPIO.output(37, GPIO.LOW)
except KeyboardInterrupt:
    c.close()
    s.close()
    GPIO.cleanup()
    GPIO.setwarnings(False)
